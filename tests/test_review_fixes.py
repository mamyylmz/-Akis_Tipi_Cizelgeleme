"""Regression tests for the fixes from docs/review_burak_seref_2026-11-18.md."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import problem as problem_module  # noqa: E402
from algorithms.de import de  # noqa: E402
from problem import Problem  # noqa: E402


def reference_generational_de(p, max_fes, seed, pop_size, F, CR):
    """Independent Storn-Price DE/rand/1/bin: builds generation G+1 from an
    untouched generation G. Draws random numbers in the same order as de.py."""
    rng = np.random.default_rng(seed)
    D, lb, ub = p.dim, p.lb, p.ub
    N = min(pop_size, max_fes)
    fes, best_f, best_x = 0, np.inf, None
    pop = lb + rng.random((N, D)) * (ub - lb)
    cost = np.empty(N)
    for i in range(N):
        cost[i] = p.evaluate(pop[i]); fes += 1
        if cost[i] < best_f:
            best_f, best_x = cost[i], pop[i].copy()
    while fes < max_fes:
        old = pop.copy()
        new_pop, new_cost = old.copy(), cost.copy()
        for i in range(N):
            if fes >= max_fes:
                break
            r1, r2, r3 = rng.choice(np.delete(np.arange(N), i), size=3, replace=False)
            v = np.clip(old[r1] + F * (old[r2] - old[r3]), lb, ub)
            j = int(rng.integers(0, D))
            mask = rng.random(D) < CR
            mask[j] = True
            u = np.clip(np.where(mask, v, old[i]), lb, ub)
            fu = p.evaluate(u); fes += 1
            if fu < best_f:
                best_f, best_x = fu, u.copy()
            if fu <= cost[i]:
                new_pop[i], new_cost[i] = u, fu
        pop, cost = new_pop, new_cost
    return best_f, best_x


class TestReviewFixes(unittest.TestCase):
    def test_de_is_generational_matches_independent_reference(self):
        p = Problem("ta001")
        for seed in (1, 7, 2026):
            r = de(p, max_fes=2_000, seed=seed, pop_size=10, F=0.5, CR=0.9)
            ref_f, ref_x = reference_generational_de(p, 2_000, seed, 10, 0.5, 0.9)
            self.assertEqual(r["best_f"], ref_f, seed)
            self.assertTrue(np.array_equal(r["best_x"], ref_x), seed)

    def test_missing_sha256_in_metadata_is_rejected(self):
        meta = problem_module._load_reference_metadata()
        meta["instances"]["ta001"].pop("sha256")
        with patch("problem._load_reference_metadata", return_value=meta):
            with self.assertRaisesRegex(ValueError, "SHA-256 missing"):
                Problem("ta001")

    def test_de_is_registered_in_main(self):
        from main import ALGORITHMS
        self.assertIn("DE", ALGORITHMS)
        self.assertIs(ALGORITHMS["DE"][0], de)


if __name__ == "__main__":
    unittest.main(verbosity=2)
