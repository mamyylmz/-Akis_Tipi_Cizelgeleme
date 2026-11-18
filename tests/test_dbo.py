from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from algorithms.dbo import _group_sizes, dbo  # noqa: E402
from problem import MAX_FES, Problem  # noqa: E402


class CountingProblem:
    """Wraps a problem and counts evaluate() calls independently of DBO."""

    def __init__(self, inner):
        self.inner = inner
        self.dim, self.lb, self.ub = inner.dim, inner.lb, inner.ub
        self.calls = 0
        self.out_of_bounds = 0

    def evaluate(self, x):
        self.calls += 1
        x = np.asarray(x, dtype=float)
        if np.any(x < self.lb) or np.any(x > self.ub):
            self.out_of_bounds += 1
        return self.inner.evaluate(x)


class TestDungBeetleOptimizer(unittest.TestCase):
    def test_contract_budget_and_reproducibility_on_pfsp(self):
        p = Problem("ta001")
        r1 = dbo(p, max_fes=600, seed=123)
        r2 = dbo(p, max_fes=600, seed=123)
        for key in ("best_x", "best_f", "history", "n_fes", "time"):
            self.assertIn(key, r1)
        self.assertEqual(r1["n_fes"], 600)
        self.assertEqual(r1["best_f"], r2["best_f"])
        self.assertTrue(np.array_equal(r1["best_x"], r2["best_x"]))
        self.assertTrue(np.all(r1["best_x"] >= p.lb))
        self.assertTrue(np.all(r1["best_x"] <= p.ub))
        self.assertEqual(float(p.evaluate(r1["best_x"])), float(r1["best_f"]))
        self.assertEqual(r1["history"][-1][0], 600)
        values = np.array([v for _, v in r1["history"]], dtype=float)
        self.assertTrue(np.all(np.diff(values) <= 1e-12))
        self.assertEqual(sorted(p.decode(r1["best_x"]).tolist()), list(range(20)))

    def test_second_seed_pair_and_different_seeds(self):
        p = Problem("ta011")
        a = dbo(p, max_fes=900, seed=2027)
        b = dbo(p, max_fes=900, seed=2027)
        c = dbo(p, max_fes=900, seed=2028)
        self.assertEqual(a["best_f"], b["best_f"])
        self.assertTrue(np.array_equal(a["best_x"], b["best_x"]))
        self.assertEqual(a["history"], b["history"])
        self.assertFalse(np.array_equal(a["best_x"], c["best_x"]))

    def test_independent_fe_counter_and_bounds_for_odd_budgets(self):
        for budget in (1, 29, 30, 31, 137, 1001):
            wrapped = CountingProblem(Problem("ta001"))
            r = dbo(wrapped, max_fes=budget, seed=5)
            self.assertEqual(wrapped.calls, budget, budget)
            self.assertEqual(r["n_fes"], budget, budget)
            self.assertEqual(wrapped.out_of_bounds, 0, budget)

    def test_full_course_budget_ta001(self):
        p = Problem("ta001")
        wrapped = CountingProblem(p)
        r = dbo(wrapped, max_fes=MAX_FES["ta001"], seed=2026)
        self.assertEqual(wrapped.calls, 20_000)
        self.assertEqual(r["n_fes"], 20_000)
        # Recompute objective independently from the decoded permutation.
        perm = p.decode(r["best_x"])
        self.assertEqual(p.objective(perm), r["best_f"])
        self.assertGreaterEqual(r["best_f"], p.reference_value)

    def test_group_split_matches_source_for_n30(self):
        self.assertEqual(_group_sizes(30), (6, 6, 7, 11))
        for n in range(4, 101):
            sizes = _group_sizes(n)
            self.assertEqual(sum(sizes), n)
            self.assertTrue(all(s >= 1 for s in sizes), (n, sizes))

    def test_invalid_parameters_are_rejected(self):
        p = Problem("ta001")
        with self.assertRaises(ValueError):
            dbo(p, max_fes=100, seed=1, k=0.5)
        with self.assertRaises(ValueError):
            dbo(p, max_fes=100, seed=1, pop_size=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
