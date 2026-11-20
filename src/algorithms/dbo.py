# -*- coding: utf-8 -*-
"""Dung Beetle Optimizer (DBO) for the shared YMM4142 algorithm API.

Primary source:
J. Xue and B. Shen, "Dung beetle optimizer: a new meta-heuristic algorithm for
global optimization," The Journal of Supercomputing, 79, 7305-7336, 2023.
doi:10.1007/s11227-022-04959-6

Source-access status (2026-11-18): the publisher full text was NOT accessed.
1) Equations (1)-(7), k=0.1, b=0.3, S=0.5, the 0.9 roll/dance probability and
   the 6/6/7/11 split for N=30 were checked against an open-access restatement:
   X. Wang et al., Biomimetics 9(9):519, 2024, doi:10.3390/biomimetics9090519.
2) Every update line was compared with the authors' MATLAB demo
   ("Programmed by Jian-kai Xue, Updated 28 Nov. 2022", File Exchange #121318),
   obtained from GitHub mirrors (Lancephil/Dung-Beetle-Optimizer Matlab/DBO.m,
   identical to mahao1001/Improved_DBO_IK "Original DBO/DBO.m"). Items marked
   [code] are confirmed there: alpha=-1 with probability 0.1, theta drawn from
   1..180 degrees, Eq.(3)/(5) upper bound X*(1+R), absolute values in Eq.(7),
   one roll/dance draw per iteration, greedy replacement.
Known deviation from the authors' code (kept on purpose, follows the paper
text): for theta = 90 or 180 degrees the position is NOT updated. The MATLAB
demo sets x = pX for those angles but then overwrites it with the tan() update.

Project adaptation (not part of the source paper):
- The time factor t/Tmax is replaced by fes/max_fes, as required by the course
  template (pso.py), so the schedule is identical for every FE budget.
- The loop stops exactly when fes == max_fes, even inside a group.
"""
from __future__ import annotations

import time

import numpy as np


def _group_sizes(n: int) -> tuple[int, int, int, int]:
    """Rolling 20 %, brood 20 %, small 25 % (floor), thief = rest.

    For N=30 this gives 6/6/7/11, the split reported for the source paper.
    """
    n_roll = int(round(0.2 * n))
    n_brood = int(round(0.2 * n))
    n_small = int(np.floor(0.25 * n))
    n_thief = n - n_roll - n_brood - n_small
    return n_roll, n_brood, n_small, n_thief


def dbo(problem, max_fes, seed, pop_size=30, k=0.1, b=0.3, S=0.5,
        roll_prob=0.9, deviation_prob=0.1):
    """Dung Beetle Optimizer with exact FE budget accounting.

    Args:
        problem: Object exposing dim, lb, ub, evaluate(x).
        max_fes: Maximum number of objective-function evaluations.
        seed: Reproducibility seed; all randomness comes from default_rng(seed).
        pop_size: Population size N (source paper: 30).
        k: Deflection coefficient in Eq.(1), source value 0.1, range (0, 0.2].
        b: Constant in Eq.(1), source value 0.3, range (0, 1).
        S: Constant in Eq.(7), source value 0.5.
        roll_prob: Probability of the obstacle-free rolling rule Eq.(1);
            otherwise the dance rule Eq.(2) is used. Source value 0.9.
        deviation_prob: Probability that alpha = -1 in Eq.(1) [code].

    Returns:
        dict with best_x, best_f, history, n_fes, time.
    """
    t0 = time.perf_counter()

    # (A) Shared preparation: identical structure to the course template.
    rng = np.random.default_rng(seed)
    D = int(problem.dim)
    lb = np.asarray(problem.lb, dtype=float)
    ub = np.asarray(problem.ub, dtype=float)

    if D < 1 or lb.shape != (D,) or ub.shape != (D,):
        raise ValueError("Invalid problem dimension or bounds")
    N = int(pop_size)
    if N < 4:
        raise ValueError("pop_size must be at least 4 (one beetle per role)")
    if max_fes < 1:
        raise ValueError("max_fes must be positive")
    if not (0.0 < k <= 0.2):
        raise ValueError("k must be in (0, 0.2]")
    if not (0.0 < b < 1.0):
        raise ValueError("b must be in (0, 1)")
    if not (0.0 <= roll_prob <= 1.0 and 0.0 <= deviation_prob <= 1.0):
        raise ValueError("probabilities must be in [0, 1]")

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

    n_roll, n_brood, n_small, _ = _group_sizes(N)
    roll_idx = range(0, n_roll)
    brood_idx = range(n_roll, n_roll + n_brood)
    small_idx = range(n_roll + n_brood, n_roll + n_brood + n_small)
    thief_idx = range(n_roll + n_brood + n_small, N)

    # (B) Initialisation.
    X = lb + rng.random((N, D)) * (ub - lb)       # current positions x(t)
    fit = np.full(N, np.inf)
    for i in range(N):
        if fes >= max_fes:
            break
        fit[i] = evaluate(X[i])

    pX = X.copy()           # each beetle's retained (best) position
    pFit = fit.copy()
    XX = pX.copy()          # retained positions of the previous iteration: x(t-1)
    g_best = int(np.argmin(pFit))
    Xb = pX[g_best].copy()  # global best position X^b

    # (C) Main loop: the condition is FE-based, never iteration-based.
    while fes < max_fes:
        X_worst = X[int(np.argmax(fit))].copy()   # global worst X^w

        # Ball-rolling beetles: Eq.(1) without obstacle, Eq.(2) dance.
        # As in the authors' code, the roll/dance decision (r2) is drawn once
        # per iteration and applies to the whole rolling group.
        rolling = rng.random() < roll_prob
        for i in roll_idx:
            if fes >= max_fes:
                break
            if rolling:
                alpha = -1.0 if rng.random() < deviation_prob else 1.0
                delta_x = np.abs(pX[i] - X_worst)
                x_new = pX[i] + alpha * k * XX[i] + b * delta_x
            else:
                theta_deg = int(rng.integers(1, 181))      # 1..180 degrees [code]
                if theta_deg in (90, 180):
                    # Decision (docs/algorithm_interface.md §10, D1): follow the
                    # paper text, no update at pi/2 and pi. The MATLAB demo's
                    # guard is overwritten; at 90 deg it would take a step of
                    # tan(pi/2) ~ 1.6e16 and throw the beetle onto a bound.
                    x_new = pX[i].copy()
                else:
                    theta = np.deg2rad(theta_deg)
                    x_new = pX[i] + np.tan(theta) * np.abs(pX[i] - XX[i])
            X[i] = np.clip(x_new, lb, ub)
            fit[i] = evaluate(X[i])
        if fes >= max_fes:
            break

        # R = 1 - t/Tmax, with t/Tmax replaced by the consumed FE ratio.
        # Decision D2 (§10): evaluated at the same point as in the MATLAB demo,
        # i.e. after the rolling group, once per iteration.
        R = 1.0 - fes / max_fes
        X_star = X[int(np.argmin(fit))].copy()    # current local best X*

        # Eq.(3): spawning region around X*; Eq.(5): foraging region around X^b.
        # The min/max ordering only matters for negative coordinates (not in
        # PFSP, where lb = 0); it keeps lower <= upper on test functions.
        lo, hi = X_star * (1.0 - R), X_star * (1.0 + R)
        lb_star = np.clip(np.minimum(lo, hi), lb, ub)
        ub_star = np.clip(np.maximum(lo, hi), lb, ub)
        lo, hi = Xb * (1.0 - R), Xb * (1.0 + R)
        lb_bb = np.clip(np.minimum(lo, hi), lb, ub)
        ub_bb = np.clip(np.maximum(lo, hi), lb, ub)

        # Brood balls: Eq.(4), kept inside the spawning region.
        for i in brood_idx:
            if fes >= max_fes:
                break
            b1 = rng.random(D)
            b2 = rng.random(D)
            x_new = X_star + b1 * (pX[i] - lb_star) + b2 * (pX[i] - ub_star)
            X[i] = np.clip(x_new, lb_star, ub_star)
            fit[i] = evaluate(X[i])

        # Small (foraging) beetles: Eq.(6), C1 ~ N(0,1) scalar, C2 ~ U(0,1)^D.
        for i in small_idx:
            if fes >= max_fes:
                break
            C1 = rng.standard_normal()
            C2 = rng.random(D)
            x_new = pX[i] + C1 * (pX[i] - lb_bb) + C2 * (pX[i] - ub_bb)
            X[i] = np.clip(x_new, lb, ub)
            fit[i] = evaluate(X[i])

        # Thieves: Eq.(7), g ~ N(0,1)^D.
        for i in thief_idx:
            if fes >= max_fes:
                break
            g = rng.standard_normal(D)
            x_new = Xb + S * g * (np.abs(pX[i] - X_star) + np.abs(pX[i] - Xb))
            X[i] = np.clip(x_new, lb, ub)
            fit[i] = evaluate(X[i])

        # Greedy retention [code]; x(t-1) is the retained set before the update.
        XX = pX.copy()
        improved = fit < pFit
        pX[improved] = X[improved]
        pFit[improved] = fit[improved]
        g_best = int(np.argmin(pFit))
        Xb = pX[g_best].copy()

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

    a = dbo(Sphere(), max_fes=10_000, seed=1)
    c = dbo(Sphere(), max_fes=10_000, seed=1)
    print(f"[smoke/sphere] best_f={a['best_f']:.6e}, n_fes={a['n_fes']}")
    print("[smoke/sphere] same-seed reproducible="
          f"{a['best_f'] == c['best_f'] and np.array_equal(a['best_x'], c['best_x'])}")
