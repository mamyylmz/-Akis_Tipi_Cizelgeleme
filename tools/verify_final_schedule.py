#!/usr/bin/env python3
"""Independent PFSP schedule/Cmax verifier for final result permutations.

This module intentionally does not import src.problem. It parses the benchmark
matrix and recomputes start/finish times with an independent recurrence.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_matrix(instance: str) -> np.ndarray:
    path = ROOT / "data" / "taillard" / f"{instance}.txt"
    lines = path.read_text(encoding="utf-8").splitlines()
    n_jobs, n_machines = map(int, lines[0].split())
    matrix = np.asarray([list(map(int, row.split())) for row in lines[1:]], dtype=np.int64)
    if matrix.shape != (n_jobs, n_machines):
        raise ValueError(f"invalid benchmark shape: {matrix.shape}")
    return matrix


def independent_schedule(processing_times: np.ndarray, permutation) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(processing_times, dtype=np.int64)
    perm = np.asarray(permutation, dtype=np.int64)
    if perm.shape != (p.shape[0],):
        raise ValueError("invalid permutation length")
    if np.unique(perm).size != p.shape[0] or np.any((perm < 0) | (perm >= p.shape[0])):
        raise ValueError("permutation must contain every job exactly once")

    start = np.zeros((p.shape[0], p.shape[1]), dtype=np.int64)
    finish = np.zeros_like(start)
    for i, job in enumerate(perm):
        for m in range(p.shape[1]):
            job_ready = finish[i, m - 1] if m else 0
            machine_ready = finish[i - 1, m] if i else 0
            start[i, m] = max(job_ready, machine_ready)
            finish[i, m] = start[i, m] + p[job, m]
    return start, finish


def verify(instance: str, permutation_1_based, expected_cmax: int | None = None) -> dict:
    p = load_matrix(instance)
    perm = np.asarray([int(v) - 1 for v in permutation_1_based], dtype=np.int64)
    start, finish = independent_schedule(p, perm)
    cmax = int(finish[-1, -1])

    if expected_cmax is not None and cmax != int(expected_cmax):
        raise ValueError(f"Cmax mismatch: independently computed {cmax}, expected {expected_cmax}")
    if np.any(start[1:, :] < finish[:-1, :]):
        raise ValueError("machine overlap detected")
    if np.any(start[:, 1:] < finish[:, :-1]):
        raise ValueError("job precedence violation detected")

    return {"permutation": perm, "start": start, "finish": finish, "cmax": cmax}


def write_schedule_csv(path: Path, result: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["position", "job", "machine", "start", "finish"]
        )
        writer.writeheader()
        perm, start, finish = result["permutation"], result["start"], result["finish"]
        for i, job in enumerate(perm):
            for m in range(start.shape[1]):
                writer.writerow({
                    "position": i + 1,
                    "job": int(job) + 1,
                    "machine": m + 1,
                    "start": int(start[i, m]),
                    "finish": int(finish[i, m]),
                })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True)
    parser.add_argument("--permutation", required=True, help="space-separated 1-based job ids")
    parser.add_argument("--expected-cmax", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = verify(args.instance, args.permutation.split(), args.expected_cmax)
    if args.output:
        write_schedule_csv(args.output, result)
    print(f"{args.instance}: independent Cmax={result['cmax']} -> PASS")


if __name__ == "__main__":
    main()
