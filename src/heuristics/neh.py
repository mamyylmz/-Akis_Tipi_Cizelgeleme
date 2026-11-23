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


def makespan(processing_times: np.ndarray, permutation: Iterable[int]) -> int:
    """Compute PFSP makespan independently from src.problem.Problem."""
    p = np.asarray(processing_times, dtype=np.int64)
    if p.ndim != 2 or p.shape[0] < 1 or p.shape[1] < 1:
        raise ValueError("processing_times must be a non-empty 2-D matrix")

    perm = np.asarray(list(permutation), dtype=np.int64)
    if perm.shape != (p.shape[0],):
        raise ValueError("permutation length must equal number of jobs")
    if np.unique(perm).size != p.shape[0] or np.any((perm < 0) | (perm >= p.shape[0])):
        raise ValueError("permutation must contain every job exactly once")

    completion = np.zeros(p.shape[1], dtype=np.int64)
    for job in perm:
        completion[0] += p[job, 0]
        for machine in range(1, p.shape[1]):
            completion[machine] = (
                max(completion[machine], completion[machine - 1])
                + p[job, machine]
            )
    return int(completion[-1])


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
    p = np.asarray(processing_times, dtype=np.int64)
    if p.ndim != 2 or p.shape[0] < 1 or p.shape[1] < 1:
        raise ValueError("processing_times must be a non-empty 2-D matrix")
    if np.any(p <= 0):
        raise ValueError("processing times must be positive")

    n_jobs = p.shape[0]
    totals = p.sum(axis=1)
    priority = sorted(range(n_jobs), key=lambda job: (-int(totals[job]), job))

    sequence: list[int] = []
    current_cmax = 0

    for job in priority:
        best_sequence = None
        best_cmax = None
        for position in range(len(sequence) + 1):
            candidate = sequence[:position] + [job] + sequence[position:]
            # Partial NEH insertion only schedules the jobs selected so far.
            partial = p[candidate]
            partial_perm = np.arange(len(candidate), dtype=np.int64)
            candidate_cmax = makespan(partial, partial_perm)
            if best_cmax is None or candidate_cmax < best_cmax:
                best_cmax = candidate_cmax
                best_sequence = candidate
        sequence = best_sequence
        current_cmax = int(best_cmax)

    result_perm = np.asarray(sequence, dtype=np.int64)
    # Defensive independent recomputation on the original matrix.
    final_cmax = makespan(p, result_perm)
    if final_cmax != current_cmax:
        raise RuntimeError("internal NEH makespan inconsistency")

    return {
        "permutation": result_perm,
        "cmax": final_cmax,
        "time": time.perf_counter() - t0,
    }
