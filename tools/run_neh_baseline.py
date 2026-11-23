#!/usr/bin/env python3
"""Generate the deterministic NEH baseline for the three mandatory instances."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from heuristics.neh import neh  # noqa: E402
from problem import INSTANCES, Problem  # noqa: E402


def rows():
    for name in INSTANCES:
        problem = Problem(name)
        result = neh(problem.processing_times)
        cmax = int(result["cmax"])
        yield {
            "instance": name,
            "jobs": problem.n_jobs,
            "machines": problem.n_machines,
            "reference_cmax": int(problem.reference_value),
            "neh_cmax": cmax,
            "rpd": 100.0 * (cmax - problem.reference_value) / problem.reference_value,
            "runtime_seconds": float(result["time"]),
            "permutation_1_based": " ".join(str(int(v) + 1) for v in result["permutation"]),
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = list(rows())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)

    for row in data:
        print(
            f"{row['instance']}: Cmax={row['neh_cmax']}, "
            f"RPD={row['rpd']:.6f}%, runtime={row['runtime_seconds']:.6f}s, "
            f"perm={row['permutation_1_based']}"
        )


if __name__ == "__main__":
    main()
