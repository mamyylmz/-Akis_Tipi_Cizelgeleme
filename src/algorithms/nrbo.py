# -*- coding: utf-8 -*-
"""Newton-Raphson-Based Optimizer (NRBO) for the shared YMM4142 API.

Primary source:
R. Sowmya, M. Premkumar and P. Jangir, "Newton-Raphson-based optimizer: A new
population-based metaheuristic algorithm for continuous optimization
problems," Engineering Applications of Artificial Intelligence, 128, 107532,
2024. doi:10.1016/j.engappai.2023.107532

Source-access status (2026-11-18): the Elsevier full text was NOT accessed.
Every line below was compared with the authors' own MATLAB code (NRBO.m,
SearchRule.m, Main.m; header "Authors, Inventors, and Programmers: Dr. Sowmya
R, Dr. M. Premkumar, and Dr. Pradeep Jangir"), from the second author's
GitHub repository mpremme/Newton-Raphson-Based-Optimizer-NRBO- (created
2024-01-21); an independent copy (lexiangrui/CUMCM2025 code/NRBO/NRBO.m) is
identical. Equation numbers refer to the open-access restatement in
Sci. Rep. 2026, PMC13310854 (Eqs. 17-35), which matches the authors' code.
Reference copy: docs/test_logs/22_nrbo_author_matlab_reference.m

Faithful details taken from the authors' code:
- DF = 0.6, N = 30 (Main.m).
- In SearchRule, mean(Xa + X_n) is the mean over the dimensions of one row
  vector, i.e. a scalar; in TAO, mean(Position) is the population mean vector.
- Worst_Pos is only replaced when a fitness becomes larger than Worst_Cost.
  With greedy replacement this never happens, so the initial worst is kept.
- Best_Pos is updated immediately after each improving particle.
- The NRSR denominator is not guarded. MATLAB's max/min ignore NaN, so the
  final bound step maps NaN to LB and +/-Inf to UB/LB. np.fmax/np.fmin
  reproduce exactly this behaviour; no NaN ever reaches problem.evaluate().

Project adaptation (not part of the source):
- delta = (1 - 2*it/MaxIt)^5 uses it/MaxIt -> fes/max_fes, as in pso.py.
- The loop stops exactly when fes == max_fes, even inside the population.
"""
from __future__ import annotations

import time

import numpy as np


def _search_rule(rng, best, worst, x, rho):
    """Newton-Raphson Search Rule, SearchRule.m with Flag = 1 (Eqs. 19-21, 26-27)."""
    D = x.shape[0]
    del_x = rng.random(D) * np.abs(best - x)                       # Eq.(19)
    nrsr = rng.standard_normal() * ((best - worst) * del_x) / (
        2.0 * (best + worst - 2.0 * x))                            # Eq.(20)
    xa = x - nrsr + rho                                            # Flag == 1
    r1 = rng.random()
    r2 = rng.random()
    m = np.mean(xa + x)                                            # scalar, as in MATLAB
    yp = r1 * (m + r1 * del_x)                                     # Eq.(26)
    yq = r2 * (m - r2 * del_x)                                     # Eq.(27)
    return rng.standard_normal() * ((yp - yq) * del_x) / (2.0 * (yp + yq - 2.0 * x))


def nrbo(problem, max_fes, seed, pop_size=30, DF=0.6):
    """NRBO with exact FE budget accounting.

    Args:
        problem: Object exposing dim, lb, ub, evaluate(x).
        max_fes: Maximum number of objective-function evaluations.
        seed: Reproducibility seed; all randomness comes from default_rng(seed).
        pop_size: Population size N (authors' Main.m: 30).
        DF: Deciding factor, probability of applying TAO (authors' code: 0.6).

    Returns:
        dict with best_x, best_f, history, n_fes, time.
    """
    t0 = time.perf_counter()

    # (A) Shared preparation.
    rng = np.random.default_rng(seed)
    D = int(problem.dim)
    lb = np.asarray(problem.lb, dtype=float)
    ub = np.asarray(problem.ub, dtype=float)

    if D < 1 or lb.shape != (D,) or ub.shape != (D,):
        raise ValueError("Invalid problem dimension or bounds")
    N = int(pop_size)
    if N < 2:
        raise ValueError("pop_size must be at least 2 (randperm(N, 2))")
    if max_fes < 1:
        raise ValueError("max_fes must be positive")
    if not (0.0 <= DF <= 1.0):
        raise ValueError("DF must be in [0, 1]")

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

    def bound(x):
        # MATLAB min(max(x, LB), UB): NaN -> LB, +Inf -> UB, -Inf -> LB.
        return np.fmin(np.fmax(x, lb), ub)

    # (B) Initialisation (Eq. 17).
    X = lb + rng.random((N, D)) * (ub - lb)
    fit = np.full(N, np.inf)
    for i in range(N):
        if fes >= max_fes:
            break
        fit[i] = evaluate(X[i])

    order = np.argsort(fit, kind="stable")
    best_score = fit[order[0]]
    best_pos = X[order[0]].copy()
    worst_cost = fit[order[-1]]
    worst_pos = X[order[-1]].copy()

    # (C) Main loop: FE-based condition.
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        while fes < max_fes:
            delta = (1.0 - 2.0 * fes / max_fes) ** 5               # Eq.(29)

            for i in range(N):
                if fes >= max_fes:
                    break
                xi = X[i]
                r_a, r_b = rng.choice(N, size=2, replace=False)     # randperm(N, 2)
                rho = (rng.random() * (best_pos - xi)
                       + rng.random() * (X[r_a] - X[r_b]))          # Eq.(25)

                nrsr = _search_rule(rng, best_pos, worst_pos, xi, rho)
                X1 = xi - nrsr + rho                                # Eq.(23)
                X2 = best_pos - nrsr + rho                          # Eq.(24)

                # Eq.(28) and (22), fresh a1, a2 for every dimension.
                X3 = xi - delta * (X2 - X1)
                a1 = rng.random(D)
                a2 = rng.random(D)
                x_update = a1 * (a1 * X1 + (1.0 - a2) * X2) + (1.0 - a2) * X3

                # Trap Avoidance Operator (Eqs. 30-35).
                if rng.random() < DF:
                    theta1 = -1.0 + 2.0 * rng.random()
                    theta2 = -0.5 + rng.random()
                    beta = 1.0 if rng.random() < 0.5 else 0.0
                    u1 = beta * 3.0 * rng.random() + (1.0 - beta)
                    u2 = beta * rng.random() + (1.0 - beta)
                    base = x_update if u1 < 0.5 else best_pos
                    x_new = (base
                             + theta1 * (u1 * best_pos - u2 * xi)
                             + theta2 * delta * (u1 * X.mean(axis=0) - u2 * xi))
                else:
                    x_new = x_update

                x_new = bound(x_new)
                f_new = evaluate(x_new)

                if f_new < fit[i]:
                    X[i] = x_new
                    fit[i] = f_new
                    if f_new < best_score:
                        best_pos = x_new.copy()
                        best_score = f_new
                if fit[i] > worst_cost:
                    worst_pos = X[i].copy()
                    worst_cost = fit[i]

    # (D) Shared result block.
    return {
        "best_x": best_x,
        "best_f": best_f,
        "history": history,
        "n_fes": fes,
        "time": time.perf_counter() - t0,
    }


if __name__ == "__main__":
    # SMOKE TEST ONLY: sphere function, not a PFSP result.
    class Sphere:
        dim = 10
        lb = np.full(10, -5.0)
        ub = np.full(10, 5.0)

        @staticmethod
        def evaluate(x):
            return float(np.sum(np.asarray(x) ** 2))

    a = nrbo(Sphere(), max_fes=10_000, seed=1)
    c = nrbo(Sphere(), max_fes=10_000, seed=1)
    print(f"[smoke/sphere] best_f={a['best_f']:.6e}, n_fes={a['n_fes']}")
    print("[smoke/sphere] same-seed reproducible="
          f"{a['best_f'] == c['best_f'] and np.array_equal(a['best_x'], c['best_x'])}")
