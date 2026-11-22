"""Boundary-handling pilot: clip vs reflect vs random re-initialisation.

PILOT ONLY - not final scientific data (docs/GIT_WORKFLOW.md, "Pilot/smoke
verisi final bilimsel veri diye kullanılmaz").

Production code is never modified. The five algorithm files are copied from
<repo>/src/algorithms into a temporary package, and only the lines that put a
CANDIDATE back into its box are replaced by BH(x, lo, hi, rng):

  PSO  X[i] = np.clip(X[i] + V[i], lb, ub)            (velocity unchanged)
  DE   mutant = np.clip(mutant, lb, ub)               (trial clip stays, no-op)
  DBO  X[i] = np.clip(x_new, lb, ub)        x3        (roll, small, thief)
       X[i] = np.clip(x_new, lb_star, ub_star)        (brood, inside its region)
       region bounds (lb_star, ub_star, lb_bb, ub_bb) are NOT changed
  NRBO x_new = bound(x_new)
  RIME x = np.clip(np.asarray(x, dtype=float), lb, ub)   (evaluate helper)

Modes:
  clip     np.fmin(np.fmax(x, lo), hi)  -> identical to the production code
  reflect  mirror the out-of-box part back inside (period 2*(hi-lo));
           non-finite values fall back to clip semantics
  random   out-of-box components -> lo + U(0,1)*(hi-lo), drawn from the
           algorithm's own rng (reproducible per seed)

Usage:
  python tools/boundary_pilot.py <repo_root> <out_dir> [--seeds 10] [--jobs 9]
  python tools/boundary_pilot.py <repo_root> <out_dir> --sanity
"""
from __future__ import annotations

import argparse
import csv
import importlib
import json
import shutil
import sys
import tempfile
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ALGOS = ["PSO", "DE", "DBO", "NRBO", "RIME"]
MODES = ["clip", "reflect", "random"]

REPLACEMENTS = {
    "pso.py": [("X[i] = np.clip(X[i] + V[i], lb, ub)", "X[i] = BH(X[i] + V[i], lb, ub, rng)", 1)],
    "de.py": [("mutant = np.clip(mutant, lb, ub)", "mutant = BH(mutant, lb, ub, rng)", 1)],
    "dbo.py": [("X[i] = np.clip(x_new, lb, ub)", "X[i] = BH(x_new, lb, ub, rng)", 3),
               ("X[i] = np.clip(x_new, lb_star, ub_star)", "X[i] = BH(x_new, lb_star, ub_star, rng)", 1)],
    "nrbo.py": [("x_new = bound(x_new)", "x_new = BH(x_new, lb, ub, rng)", 1)],
    "rime.py": [("x = np.clip(np.asarray(x, dtype=float), lb, ub)",
                 "x = BH(np.asarray(x, dtype=float), lb, ub, rng)", 1)],
}

BH_SOURCE = '''
import numpy as np
MODE = "clip"

def BH(x, lo, hi, rng):
    x = np.asarray(x, dtype=float)
    lo = np.broadcast_to(np.asarray(lo, dtype=float), x.shape)
    hi = np.broadcast_to(np.asarray(hi, dtype=float), x.shape)
    if MODE == "clip":
        return np.fmin(np.fmax(x, lo), hi)
    out = ~((x >= lo) & (x <= hi))          # also True for NaN/Inf
    if not out.any():
        return x.copy()
    if MODE == "reflect":
        y = np.fmin(np.fmax(x, lo), hi)     # fallback for non-finite / zero width
        w = hi - lo
        ok = out & np.isfinite(x) & (w > 0)
        if ok.any():
            r = np.mod(x[ok] - lo[ok], 2.0 * w[ok])
            r = np.where(r > w[ok], 2.0 * w[ok] - r, r)
            y[ok] = lo[ok] + r
        return y
    if MODE == "random":
        y = x.copy()
        y[out] = lo[out] + rng.random(int(out.sum())) * (hi[out] - lo[out])
        return y
    raise ValueError(MODE)
'''


def build_package(repo: Path, tmp: Path) -> None:
    pkg = tmp / "bp_algorithms"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (tmp / "bp_bh.py").write_text(BH_SOURCE)
    for name, reps in REPLACEMENTS.items():
        src = (repo / "src" / "algorithms" / name).read_text(encoding="utf-8")
        for old, new, count in reps:
            found = src.count(old)
            if found != count:
                raise RuntimeError(f"{name}: expected {count} x {old!r}, found {found}")
            src = src.replace(old, new)
        src = src.replace("import numpy as np\n", "import numpy as np\nfrom bp_bh import BH\n", 1)
        (pkg / name).write_text(src, encoding="utf-8")


class Recorder:
    """Course-API problem wrapper; records candidate statistics."""

    def __init__(self, inner):
        self.inner = inner
        self.dim, self.lb, self.ub = inner.dim, inner.lb, inner.ub
        self.n = 0
        self.at_bound = 0
        self.with_tie = 0
        self.perms = set()

    def evaluate(self, x):
        x = np.asarray(x, dtype=float)
        if not (np.all(np.isfinite(x)) and np.all(x >= self.lb) and np.all(x <= self.ub)):
            raise AssertionError("candidate outside bounds or non-finite")
        self.n += 1
        self.at_bound += int(np.sum((x == self.lb) | (x == self.ub)))
        self.with_tie += int(np.unique(x).size < x.size)
        self.perms.add(np.argsort(x, kind="stable").tobytes())
        return self.inner.evaluate(x)


_STATE = {}


def _init(repo: str, tmp: str) -> None:
    sys.path.insert(0, tmp)
    sys.path.insert(0, str(Path(repo) / "src"))
    _STATE["main"] = importlib.import_module("main")
    _STATE["problem"] = importlib.import_module("problem")
    _STATE["bh"] = importlib.import_module("bp_bh")
    _STATE["mods"] = {a: importlib.import_module(f"bp_algorithms.{a.lower()}") for a in ALGOS}


def _run(task):
    alg, inst, mode, seed = task
    bh, problem_mod, main = _STATE["bh"], _STATE["problem"], _STATE["main"]
    bh.MODE = mode
    p = problem_mod.Problem(inst)
    rec = Recorder(p)
    func = getattr(_STATE["mods"][alg], alg.lower())
    params = main.ALGORITHMS[alg][1]
    budget = problem_mod.MAX_FES[inst]
    t0 = time.perf_counter()
    r = func(rec, budget, seed, **params)
    dt = time.perf_counter() - t0
    bx = np.asarray(r["best_x"], dtype=float)
    assert r["n_fes"] == budget == rec.n
    assert float(p.evaluate(bx)) == float(r["best_f"])
    return {
        "algorithm": alg, "instance": inst, "mode": mode, "seed": seed,
        "best_f": r["best_f"],
        "rpd": 100.0 * (r["best_f"] - p.reference_value) / p.reference_value,
        "n_fes": r["n_fes"], "time_s": round(dt, 3),
        "best_x_bound_frac": float(np.mean((bx == p.lb) | (bx == p.ub))),
        "cand_bound_frac": rec.at_bound / (rec.n * p.dim),
        "cand_tie_frac": rec.with_tie / rec.n,
        "unique_perm_frac": len(rec.perms) / rec.n,
    }


def sanity(repo: Path, tmp: Path) -> bool:
    """clip mode must reproduce the production algorithms bit for bit."""
    _init(str(repo), str(tmp))
    _STATE["bh"].MODE = "clip"
    problem_mod, main = _STATE["problem"], _STATE["main"]
    ok = True
    for alg in ALGOS:
        orig_func, params = main.ALGORITHMS[alg]
        patched = getattr(_STATE["mods"][alg], alg.lower())
        for inst in problem_mod.INSTANCES:
            for seed, budget in ((2026, 3000), (2031, 1001)):
                p = problem_mod.Problem(inst)
                a = orig_func(p, budget, seed, **params)
                b = patched(p, budget, seed, **params)
                same = (a["best_f"] == b["best_f"] and np.array_equal(a["best_x"], b["best_x"])
                        and a["history"] == b["history"] and a["n_fes"] == b["n_fes"])
                ok &= same
                print(f"sanity {alg:5s} {inst} seed={seed} FE={budget}: "
                      f"{'AYNI' if same else 'FARKLI'}")
    print("SANITY:", "PASS" if ok else "FAIL")
    return ok


def main_cli() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("out")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--jobs", type=int, default=9)
    ap.add_argument("--sanity", action="store_true")
    args = ap.parse_args()
    repo, out = Path(args.repo).resolve(), Path(args.out).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="bp_"))
    try:
        build_package(repo, tmp)
        if args.sanity:
            raise SystemExit(0 if sanity(repo, tmp) else 1)
        out.mkdir(parents=True, exist_ok=True)
        sys.path.insert(0, str(repo / "src"))
        instances = importlib.import_module("problem").INSTANCES
        seeds = list(range(2026, 2026 + args.seeds))
        tasks = [(a, i, m, s) for i in instances for a in ALGOS for m in MODES for s in seeds]
        t0 = time.time()
        with Pool(args.jobs, initializer=_init, initargs=(str(repo), str(tmp))) as pool:
            rows = pool.map(_run, tasks, chunksize=1)
        rows.sort(key=lambda r: (r["instance"], ALGOS.index(r["algorithm"]),
                                 MODES.index(r["mode"]), r["seed"]))
        with open(out / "runs.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        (out / "run_info.json").write_text(json.dumps({
            "runs": len(rows), "seeds": seeds, "modes": MODES, "algorithms": ALGOS,
            "instances": instances, "wall_clock_s": round(time.time() - t0, 1),
            "note": "PILOT - not final experiment data",
        }, indent=2))
        print(f"{len(rows)} koşu, {time.time() - t0:.0f} s -> {out / 'runs.csv'}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main_cli()
