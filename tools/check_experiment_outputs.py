from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

import sys
sys.path.insert(0, str(SRC))

from problem import INSTANCES, MAX_FES, Problem  # noqa: E402

ALGORITHMS = ("PSO", "DE", "DBO", "RIME", "NRBO")
REQUIRED_COLUMNS = {
    "run", "seed", "best_f", "objective", "cmax", "rpd", "violation",
    "feasible", "permutation", "n_fes", "time", "best_x",
    "history_fes", "history_f",
}


def validate(raw_dir: Path, runs: int = 30, seed_base: int = 2026) -> list[str]:
    errors: list[str] = []
    expected_seeds = list(range(seed_base, seed_base + runs))

    for instance in INSTANCES:
        problem = Problem(instance)
        for algorithm in ALGORITHMS:
            path = raw_dir / instance / f"{algorithm}.csv"
            if not path.exists():
                errors.append(f"MISSING {path}")
                continue
            df = pd.read_csv(path)
            missing = REQUIRED_COLUMNS - set(df.columns)
            if missing:
                errors.append(f"{path}: missing columns {sorted(missing)}")
                continue
            if len(df) != runs:
                errors.append(f"{path}: rows={len(df)} expected={runs}")
                continue
            if df["run"].tolist() != list(range(1, runs + 1)):
                errors.append(f"{path}: run sequence mismatch")
            if df["seed"].tolist() != expected_seeds:
                errors.append(f"{path}: seed sequence mismatch")

            for row_no, row in df.iterrows():
                prefix = f"{path}:run={row_no + 1}"
                if int(row["n_fes"]) != MAX_FES[instance]:
                    errors.append(f"{prefix}: n_fes={row['n_fes']}")
                if not bool(row["feasible"]):
                    errors.append(f"{prefix}: infeasible")
                if not np.isfinite(float(row["best_f"])):
                    errors.append(f"{prefix}: non-finite best_f")
                    continue
                try:
                    x = np.asarray(json.loads(row["best_x"]), dtype=float)
                    hfes = [int(v) for v in json.loads(row["history_fes"])]
                    hval = [float(v) for v in json.loads(row["history_f"])]
                except Exception as exc:
                    errors.append(f"{prefix}: JSON decode failed: {exc}")
                    continue
                if x.shape != (problem.dim,):
                    errors.append(f"{prefix}: best_x shape={x.shape}")
                    continue
                if np.any(~np.isfinite(x)) or np.any(x < problem.lb) or np.any(x > problem.ub):
                    errors.append(f"{prefix}: invalid best_x")
                permutation = problem.decode(x)
                if sorted(permutation.tolist()) != list(range(problem.dim)):
                    errors.append(f"{prefix}: invalid permutation")
                observed = float(problem.evaluate(x))
                if not np.isclose(observed, float(row["best_f"]), rtol=0, atol=1e-12):
                    errors.append(
                        f"{prefix}: best_f mismatch csv={row['best_f']} recomputed={observed}"
                    )
                if not hfes or hfes[-1] != MAX_FES[instance]:
                    errors.append(f"{prefix}: history final FE mismatch")
                if len(hfes) != len(hval):
                    errors.append(f"{prefix}: history lengths differ")
                if any(a >= b for a, b in zip(hfes, hfes[1:])):
                    errors.append(f"{prefix}: history FE not increasing")
                if any(a < b for a, b in zip(hval, hval[1:])):
                    errors.append(f"{prefix}: history best value increased")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=ROOT / "results" / "raw")
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--seed-base", type=int, default=2026)
    args = parser.parse_args()

    errors = validate(args.raw_dir, args.runs, args.seed_base)
    if errors:
        print("\n".join(errors))
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print("PASS: 15 CSV / 450 run satisfy the final experiment contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
