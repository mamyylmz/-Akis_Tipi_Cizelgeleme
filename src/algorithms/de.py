# -*- coding: utf-8 -*-
"""Differential Evolution (DE/rand/1/bin) for the shared YMM4142 API.

Primary source:
R. Storn and K. Price, "Differential Evolution – A Simple and Efficient
Heuristic for Global Optimization over Continuous Spaces," Journal of Global
Optimization, 11, 341–359, 1997. doi:10.1023/A:1008202821328

Project defaults are taken from the paper's Section 4 rules of thumb for D=20:
NP=5*D=100, F=0.5, CR=0.9. These are not tuned on the Taillard instances.
"""
from __future__ import annotations

import time

import numpy as np


def de(problem, max_fes, seed, pop_size=None, F=0.5, CR=0.9):
    """DE/rand/1/bin with exact function-evaluation budget accounting.

    Args:
        problem: Object exposing dim, lb, ub, evaluate(x).
        max_fes: Maximum number of objective-function evaluations.
        seed: Reproducibility seed; all randomness comes from default_rng(seed).
        pop_size: Population size. If None, use 5*D as the source-paper lower
            rule-of-thumb, with a minimum of 4. If max_fes is smaller than the
            requested size, the population is reduced to max_fes so that every
            individual is evaluated. This only happens with small test budgets;
            course budgets (>= 20,000 FE) are not affected.
        F: Differential weight. 0.5 is the source paper's usual initial choice.
        CR: Binomial crossover probability. 0.9 is one of the paper's suggested
            high-CR first trials for fast convergence.

    The population is updated generation by generation, as in Storn & Price
    (1997): mutation and crossover read only generation G (X_gen); selected
    trial vectors form generation G+1. If the FE budget ends mid-generation,
    the selections made so far are kept.
    """
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    D = int(problem.dim)
    lb = np.asarray(problem.lb, dtype=float)
    ub = np.asarray(problem.ub, dtype=float)

    if D < 1 or lb.shape != (D,) or ub.shape != (D,):
        raise ValueError("Invalid problem dimension or bounds")
    if max_fes < 4:
        raise ValueError("DE requires at least 4 function evaluations")
    if not (0.0 < F <= 2.0):
        raise ValueError("F must be in (0, 2]")
    if not (0.0 <= CR <= 1.0):
        raise ValueError("CR must be in [0, 1]")

    requested_n = max(4, 5 * D) if pop_size is None else int(pop_size)
    if requested_n < 4:
        raise ValueError("pop_size must be at least 4")
    N = min(requested_n, int(max_fes))

    fes = 0
    best_x = None
    best_f = np.inf
    history = []
    log_every = max(1, max_fes // 100)

    def evaluate(x):
        nonlocal fes, best_x, best_f
        f = float(problem.evaluate(x))
        fes += 1
        if f < best_f:
            best_f = f
            best_x = np.asarray(x, dtype=float).copy()
        if fes % log_every == 0 or fes == max_fes:
            history.append((fes, best_f))
        return f

    X = lb + rng.random((N, D)) * (ub - lb)
    Fvals = np.full(N, np.inf, dtype=float)
    for i in range(N):
        if fes >= max_fes:
            break
        Fvals[i] = evaluate(X[i])

    all_indices = np.arange(N)
    while fes < max_fes:
        X_gen = X.copy()            # generation G; X becomes generation G+1
        for i in range(N):
            if fes >= max_fes:
                break

            pool = np.delete(all_indices, i)
            r1, r2, r3 = rng.choice(pool, size=3, replace=False)

            # DE/rand/1 mutation: v = x_r1,G + F * (x_r2,G - x_r3,G)
            mutant = X_gen[r1] + F * (X_gen[r2] - X_gen[r3])
            mutant = np.clip(mutant, lb, ub)

            # Binomial crossover with one forced mutant component j_rand.
            j_rand = int(rng.integers(0, D))
            mask = rng.random(D) < CR
            mask[j_rand] = True
            trial = np.where(mask, mutant, X_gen[i])
            trial = np.clip(trial, lb, ub)

            f_trial = evaluate(trial)
            if f_trial <= Fvals[i]:
                X[i] = trial
                Fvals[i] = f_trial

    return {
        "best_x": best_x,
        "best_f": best_f,
        "history": history,
        "n_fes": fes,
        "time": time.perf_counter() - t0,
    }


if __name__ == "__main__":
    class Sphere:
        dim = 10
        lb = np.full(10, -5.0)
        ub = np.full(10, 5.0)

        @staticmethod
        def evaluate(x):
            return float(np.sum(np.asarray(x) ** 2))

    a = de(Sphere(), max_fes=5_000, seed=123, pop_size=50)
    b = de(Sphere(), max_fes=5_000, seed=123, pop_size=50)
    print(f"best_f={a['best_f']:.6e}, n_fes={a['n_fes']}")
    print(f"same-seed reproducible={a['best_f'] == b['best_f'] and np.array_equal(a['best_x'], b['best_x'])}")
