# -*- coding: utf-8 -*-
"""RIME optimizer adapted to the YMM4142 FE-budget contract.

Primary source:
Su, H. et al. (2023), "RIME: A physics-based optimization",
Neurocomputing 532, 183-214. DOI: 10.1016/j.neucom.2023.02.010.

The implementation follows the authors' public MATLAB RIME.m for soft-rime
search, hard-rime puncture and positive greedy selection. The original
iteration budget is mapped to full/partial population sweeps so the course
contract consumes exactly max_fes evaluations.
"""
from __future__ import annotations

import math
import time

import numpy as np


def _matlab_round_nonnegative(x: float) -> float:
    """MATLAB-style round for x >= 0 (half values away from zero)."""
    return float(math.floor(x + 0.5))


def _normalized_rates(rates: np.ndarray) -> np.ndarray:
    """Equivalent of MATLAB normr for the row-vector fitness array."""
    rates = np.asarray(rates, dtype=float)
    norm = float(np.linalg.norm(rates))
    if not np.isfinite(norm) or norm <= 0.0:
        return np.zeros_like(rates)
    return rates / norm


def rime(problem, max_fes, seed, pop_size=30, w=5):
    """Rime Optimization Algorithm (RIME), minimization version."""
    if not isinstance(max_fes, (int, np.integer)) or int(max_fes) <= 0:
        raise ValueError("max_fes must be a positive integer")
    if not isinstance(pop_size, (int, np.integer)) or int(pop_size) < 1:
        raise ValueError("pop_size must be a positive integer")
    if not isinstance(w, (int, np.integer)) or int(w) < 1:
        raise ValueError("w must be a positive integer")

    max_fes = int(max_fes)
    requested_n = int(pop_size)
    w = int(w)
    t0 = time.perf_counter()

    rng = np.random.default_rng(seed)
    dim = int(problem.dim)
    lb = np.asarray(problem.lb, dtype=float)
    ub = np.asarray(problem.ub, dtype=float)
    if lb.shape != (dim,) or ub.shape != (dim,):
        raise ValueError("problem bounds must have shape (problem.dim,)")
    if np.any(lb > ub):
        raise ValueError("problem bounds must satisfy lb <= ub")

    fes = 0
    best_x = None
    best_f = np.inf
    history = []
    log_every = max(1, max_fes // 100)

    def evaluate(x):
        nonlocal fes, best_x, best_f
        x = np.clip(np.asarray(x, dtype=float), lb, ub)
        f = float(problem.evaluate(x))
        fes += 1
        if f < best_f:
            best_f = f
            best_x = x.copy()
        if fes % log_every == 0 or fes == max_fes:
            history.append((fes, best_f))
        return f, x

    # The original RIME initializes N uniformly distributed agents. For tiny
    # contract-test budgets, reduce only the initialization population so no FE
    # is consumed beyond the exact budget.
    n_agents = min(requested_n, max_fes)
    positions = lb + rng.random((n_agents, dim)) * (ub - lb)
    rates = np.full(n_agents, np.inf, dtype=float)
    for i in range(n_agents):
        rates[i], positions[i] = evaluate(positions[i])

    remaining = max_fes - fes
    if remaining > 0:
        max_iter = max(1, int(math.ceil(remaining / n_agents)))
        iteration = 1

        while fes < max_fes:
            progress = iteration / max_iter
            step = _matlab_round_nonnegative(w * progress)
            rime_factor = (
                (rng.random() - 0.5)
                * 2.0
                * math.cos(math.pi * iteration / (max_iter / 10.0))
                * (1.0 - step / w)
            )
            adherence = math.sqrt(progress)
            normalized = _normalized_rates(rates)
            candidates = positions.copy()

            # Soft-rime search (Eq. 3) and hard-rime puncture (Eq. 7).
            # RNG draw order follows the public author MATLAB implementation.
            for i in range(n_agents):
                for j in range(dim):
                    if rng.random() < adherence:
                        adhesion = rng.random()
                        escape_position = (ub[j] - lb[j]) * adhesion + lb[j]
                        candidates[i, j] = (
                            best_x[j] + rime_factor * escape_position
                        )
                    if rng.random() < normalized[i]:
                        candidates[i, j] = best_x[j]

            # Positive greedy selection: only strict improvements replace the
            # corresponding current agent.
            for i in range(n_agents):
                if fes >= max_fes:
                    break
                new_f, bounded = evaluate(candidates[i])
                if new_f < rates[i]:
                    rates[i] = new_f
                    positions[i] = bounded

            iteration += 1

    if not history or history[-1][0] != fes:
        history.append((fes, best_f))

    return {
        "best_x": best_x,
        "best_f": float(best_f),
        "history": history,
        "n_fes": fes,
        "time": time.perf_counter() - t0,
    }
