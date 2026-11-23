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


def _parse_bool(value) -> bool:
    """Parse only explicit boolean representations; never use bool("False")."""
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (int, np.integer)) and int(value) in (0, 1):
        return bool(value)
    if isinstance(value, (float, np.floating)) and np.isfinite(value) and value in (0.0, 1.0):
        return bool(int(value))
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    raise ValueError(f"invalid boolean value: {value!r}")


def _parse_permutation(value, n_jobs: int) -> list[int]:
    if not isinstance(value, str):
        raise ValueError(f"permutation must be a space-separated string, got {type(value).__name__}")
    parts = value.split()
    if len(parts) != n_jobs:
        raise ValueError(f"permutation length={len(parts)} expected={n_jobs}")
    try:
        permutation = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError("permutation contains a non-integer token") from exc
    if sorted(permutation) != list(range(1, n_jobs + 1)):
        raise ValueError("permutation is not a complete 1-based job ordering")
    return permutation


def _finite_float(row, field: str, prefix: str, errors: list[str]) -> float | None:
    try:
        value = float(row[field])
    except (TypeError, ValueError):
        errors.append(f"{prefix}: {field} is not numeric: {row[field]!r}")
        return None
    if not np.isfinite(value):
        errors.append(f"{prefix}: {field} is non-finite")
        return None
    return value


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

            try:
                df = pd.read_csv(path)
            except Exception as exc:
                errors.append(f"{path}: CSV read failed: {exc}")
                continue

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

                try:
                    n_fes = int(row["n_fes"])
                except (TypeError, ValueError):
                    errors.append(f"{prefix}: n_fes is not an integer")
                    n_fes = None
                if n_fes != MAX_FES[instance]:
                    errors.append(f"{prefix}: n_fes={row['n_fes']} expected={MAX_FES[instance]}")

                try:
                    feasible = _parse_bool(row["feasible"])
                except ValueError as exc:
                    errors.append(f"{prefix}: {exc}")
                    feasible = False
                if not feasible:
                    errors.append(f"{prefix}: infeasible")

                best_f = _finite_float(row, "best_f", prefix, errors)
                objective = _finite_float(row, "objective", prefix, errors)
                cmax = _finite_float(row, "cmax", prefix, errors)
                rpd = _finite_float(row, "rpd", prefix, errors)
                violation = _finite_float(row, "violation", prefix, errors)

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
                    continue

                decoded = problem.decode(x)
                if sorted(decoded.tolist()) != list(range(problem.dim)):
                    errors.append(f"{prefix}: invalid decoded permutation")

                try:
                    recorded_perm = _parse_permutation(row["permutation"], problem.n_jobs)
                except ValueError as exc:
                    errors.append(f"{prefix}: {exc}")
                    recorded_perm = None
                expected_perm = (decoded + 1).tolist()
                if recorded_perm is not None and recorded_perm != expected_perm:
                    errors.append(
                        f"{prefix}: permutation mismatch csv={recorded_perm} recomputed={expected_perm}"
                    )

                recomputed = float(problem.evaluate(x))
                if best_f is not None and not np.isclose(recomputed, best_f, rtol=0, atol=1e-12):
                    errors.append(
                        f"{prefix}: best_f mismatch csv={best_f} recomputed={recomputed}"
                    )
                for field, value in (("objective", objective), ("cmax", cmax)):
                    if value is not None and not np.isclose(value, recomputed, rtol=0, atol=1e-12):
                        errors.append(
                            f"{prefix}: {field} mismatch csv={value} recomputed={recomputed}"
                        )

                expected_rpd = 100.0 * (recomputed - problem.reference_value) / problem.reference_value
                if rpd is not None and not np.isclose(rpd, expected_rpd, rtol=0, atol=1e-10):
                    errors.append(
                        f"{prefix}: rpd mismatch csv={rpd} recomputed={expected_rpd}"
                    )
                if violation is not None and not np.isclose(violation, 0.0, rtol=0, atol=1e-12):
                    errors.append(f"{prefix}: violation={violation} expected=0")

                if not hfes or hfes[-1] != MAX_FES[instance]:
                    errors.append(f"{prefix}: history final FE mismatch")
                if len(hfes) != len(hval):
                    errors.append(f"{prefix}: history lengths differ")
                if any(a >= b for a, b in zip(hfes, hfes[1:])):
                    errors.append(f"{prefix}: history FE not increasing")
                if any((not np.isfinite(v)) for v in hval):
                    errors.append(f"{prefix}: history contains non-finite best value")
                if any(a < b for a, b in zip(hval, hval[1:])):
                    errors.append(f"{prefix}: history best value increased")
                if best_f is not None and hval and not np.isclose(hval[-1], best_f, rtol=0, atol=1e-12):
                    errors.append(
                        f"{prefix}: history final best={hval[-1]} does not match best_f={best_f}"
                    )

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
    expected = len(INSTANCES) * len(ALGORITHMS) * args.runs
    print(
        f"PASS: {len(INSTANCES) * len(ALGORITHMS)} CSV / {expected} run "
        "satisfy the experiment contract"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
