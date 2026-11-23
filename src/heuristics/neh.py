# -*- coding: utf-8 -*-
"""Nawaz-Enscore-Ham (NEH) constructive heuristic for PFSP makespan.

Primary source:
M. Nawaz, E. E. Enscore Jr., I. Ham,
"A heuristic algorithm for the m-machine, n-job flow-shop sequencing problem,"
Omega, 11(1), 91-95, 1983.
doi:10.1016/0305-0483(83)90088-9

The source abstract states the central priority rule: jobs with larger total
processing time receive higher priority. The standard NEH construction then
inserts jobs one by one into the position yielding the smallest partial
makespan.

Project determinism:
- equal total-processing-time jobs are ordered by ascending zero-based job id;
- equal insertion makespans keep the earliest insertion position.

NEH is a deterministic classical baseline. It is NOT one of the five
metaheuristics and is not repeated 30 times.
"""
from __future__ import annotations

import time
from typing import Iterable

import numpy as np


def _integer_values(values, label):
    """Validate the numeric domain before any integer conversion."""
    array = np.asarray(values)
    if array.dtype.kind == "f":
        if (not np.all(np.isfinite(array))
                or not np.all(array == np.trunc(array))):
            raise ValueError(f"{label} must contain finite integers")
    elif array.dtype.kind not in "iu":
        raise ValueError(f"{label} must contain finite integers")
    return array


def _processing_matrix(processing_times):
    p = _integer_values(processing_times, "processing_times")
    if p.ndim != 2 or p.shape[0] < 1 or p.shape[1] < 1:
        raise ValueError("processing_times must be a non-empty 2-D matrix")
    if np.any(p <= 0):
        raise ValueError("processing times must be positive")
    return [[int(duration) for duration in row] for row in p]


def _makespan(matrix, order):
    completion = [0] * len(matrix[0])
    for job in order:
        completion[0] += matrix[job][0]
        for machine in range(1, len(completion)):
            completion[machine] = (
                max(completion[machine], completion[machine - 1])
                + matrix[job][machine]
            )
    return completion[-1]


def makespan(processing_times: np.ndarray, permutation: Iterable[int]) -> int:
    """Compute PFSP makespan independently from src.problem.Problem."""
    matrix = _processing_matrix(processing_times)
    perm = _integer_values(list(permutation), "permutation")
    if perm.shape != (len(matrix),):
        raise ValueError("permutation length must equal number of jobs")
    order = [int(job) for job in perm]
    if set(order) != set(range(len(matrix))):
        raise ValueError("permutation must contain every job exactly once")
    return _makespan(matrix, order)


def neh(processing_times: np.ndarray) -> dict:
    """Return deterministic NEH sequence, makespan and runtime.

    Returns:
        {
          "permutation": zero-based numpy array,
          "cmax": int,
          "time": seconds,
        }
    """
    t0 = time.perf_counter()
    matrix = _processing_matrix(processing_times)
    totals = [sum(row) for row in matrix]
    priority = sorted(range(len(matrix)), key=lambda job: (-totals[job], job))

    sequence: list[int] = []
    current_cmax = 0

    for job in priority:
        best_sequence = None
        best_cmax = None
        for position in range(len(sequence) + 1):
            candidate = sequence[:position] + [job] + sequence[position:]
            candidate_cmax = _makespan(matrix, candidate)
            if best_cmax is None or candidate_cmax < best_cmax:
                best_cmax = candidate_cmax
                best_sequence = candidate
        sequence = best_sequence
        current_cmax = int(best_cmax)

    result_perm = np.asarray(sequence, dtype=np.int64)
    # Recheck the final permutation on the original validated matrix.
    final_cmax = _makespan(matrix, sequence)
    if final_cmax != current_cmax:
        raise RuntimeError("internal NEH makespan inconsistency")

    return {
        "permutation": result_perm,
        "cmax": final_cmax,
        "time": time.perf_counter() - t0,
    }
