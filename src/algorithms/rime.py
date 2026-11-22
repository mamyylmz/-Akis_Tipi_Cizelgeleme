"""Su et al. RIME (doi:10.1016/j.neucom.2023.02.010), with a strict FE budget."""
import time

import numpy as np


def rime(problem, max_fes, seed, pop_size=30, w=5):
    """Apply soft-rime search, hard-rime puncture and greedy selection."""
    started = time.perf_counter()
    if max_fes < 1 or pop_size < 1 or w < 1:
        raise ValueError("max_fes, pop_size and w must be positive")
    rng = np.random.default_rng(seed)
    lo, hi = np.asarray(problem.lb), np.asarray(problem.ub)
    size = min(pop_size, max_fes)
    population = rng.uniform(lo, hi, size=(size, problem.dim))
    scores = np.empty(size)
    history = []
    n_fes = 0
    best_f = np.inf
    best_x = None

    def evaluate(candidate):
        nonlocal n_fes, best_f, best_x
        value = float(problem.evaluate(candidate))
        n_fes += 1
        if value < best_f:
            best_f, best_x = value, candidate.copy()
        if n_fes % max(1, max_fes // 100) == 0 or n_fes == max_fes:
            history.append((n_fes, best_f))
        return value

    for index, candidate in enumerate(population):
        scores[index] = evaluate(candidate)

    while n_fes < max_fes:
        # FE progress replaces iteration progress in Eq. (3).
        progress = n_fes / max_fes
        decay = 1 - np.floor(w * progress + 0.5) / w
        factor = rng.uniform(-1, 1) * np.cos(np.pi * progress / 10) * decay
        anchor = best_x.copy()
        norm = np.linalg.norm(scores)
        puncture = np.abs(scores) / norm if norm else np.zeros_like(scores)
        for index in range(min(size, max_fes - n_fes)):
            candidate = population[index].copy()
            soft = rng.random(problem.dim) < np.sqrt(progress)
            adhesion = rng.random(problem.dim)
            candidate[soft] = (anchor + factor * (lo + adhesion * (hi - lo)))[soft]
            hard = rng.random(problem.dim) < puncture[index]
            candidate[hard] = anchor[hard]
            candidate = np.clip(candidate, lo, hi)
            score = evaluate(candidate)
            if score < scores[index]:
                scores[index] = score
                population[index] = candidate

    return {"best_x": best_x, "best_f": best_f, "history": history,
            "n_fes": n_fes, "time": time.perf_counter() - started}
