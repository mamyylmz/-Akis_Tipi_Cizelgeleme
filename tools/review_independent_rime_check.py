"""Independent re-implementation of the authors' RIME.m (Heidari's repository,
"Last update: Feb 11 2023"), written by the reviewer from the MATLAB source only,
then compared draw-for-draw with src/algorithms/rime.py.

Reviewer adaptation, chosen to match the project contract (not copied from rime.py):
Max_iter = ceil((max_fes - N) / N); the last sweep stops when the FE budget ends.
"""
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from problem import Problem, MAX_FES  # noqa: E402
from algorithms.rime import rime  # noqa: E402


def matlab_round(v):           # half away from zero (v >= 0 here)
    return math.floor(v + 0.5)


def rime_matlab(p, max_fes, seed, N=30, W=5):
    rng = np.random.default_rng(seed)
    D, lb, ub = p.dim, np.asarray(p.lb, float), np.asarray(p.ub, float)
    fes, curve = 0, []
    pop = rng.random((N, D)) * (ub - lb) + lb                    # initialization.m
    rates = np.zeros(N)
    best, best_rate = np.zeros(D), np.inf
    for i in range(N):                                           # lines 52-59
        rates[i] = p.evaluate(pop[i]); fes += 1
        if rates[i] < best_rate:
            best_rate, best = rates[i], pop[i].copy()
    max_iter = math.ceil((max_fes - N) / N)
    it = 1
    while fes < max_fes:                                         # line 61
        factor = (rng.random() - 0.5) * 2 * math.cos(math.pi * it / (max_iter / 10)) \
            * (1 - matlab_round(it * W / max_iter) / W)          # line 62
        E = math.sqrt(it / max_iter)                             # line 63
        new = pop.copy()                                         # line 64
        norm = rates / np.linalg.norm(rates)                     # line 65, normr
        for i in range(N):
            for j in range(D):
                if rng.random() < E:                             # lines 69-72
                    new[i, j] = best[j] + factor * ((ub[j] - lb[j]) * rng.random() + lb[j])
                if rng.random() < norm[i]:                       # lines 74-77
                    new[i, j] = best[j]
        for i in range(N):
            if fes >= max_fes:
                break
            new[i] = np.where(new[i] > ub, ub, np.where(new[i] < lb, lb, new[i]))  # line 84
            f = p.evaluate(new[i]); fes += 1
            if f < rates[i]:                                     # lines 87-94
                rates[i], pop[i] = f, new[i].copy()
                if f < best_rate:
                    best_rate, best = f, pop[i].copy()
            curve.append((fes, best_rate))
        it += 1
    return best_rate, best, fes


ok = True
for name in ("ta001", "ta011", "ta021"):
    p = Problem(name)
    for seed in (2026, 2027, 2055):
        for budget in (MAX_FES[name], 1001, 137):
            ref_f, ref_x, ref_fes = rime_matlab(p, budget, seed)
            r = rime(p, budget, seed, pop_size=30, w=5)
            same = (r["best_f"] == ref_f and np.array_equal(r["best_x"], ref_x)
                    and r["n_fes"] == ref_fes == budget)
            ok &= same
            print(f"{name} seed={seed} FE={budget}: bağımsız={ref_f:.0f} rime.py={r['best_f']:.0f} "
                  f"best_x aynı={np.array_equal(r['best_x'], ref_x)} n_fes={r['n_fes']} -> "
                  f"{'PASS' if same else 'FAIL'}")
print("GENEL:", "PASS" if ok else "FAIL")
