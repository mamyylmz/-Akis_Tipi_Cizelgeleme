from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from algorithms.rime import _matlab_round_nonnegative, _normalized_rates, rime  # noqa: E402
from problem import MAX_FES, Problem  # noqa: E402


class CountingProblem:
    def __init__(self, inner):
        self.inner = inner
        self.dim = inner.dim
        self.lb = inner.lb
        self.ub = inner.ub
        self.calls = 0
        self.bad = 0

    def evaluate(self, x):
        self.calls += 1
        x = np.asarray(x, dtype=float)
        if (not np.all(np.isfinite(x))) or np.any(x < self.lb) or np.any(x > self.ub):
            self.bad += 1
        return self.inner.evaluate(x)


class TestRIME(unittest.TestCase):
    def test_contract_budget_seed_bounds_and_best(self):
        p = Problem("ta001")
        a = rime(p, 600, 123)
        b = rime(p, 600, 123)
        c = rime(p, 600, 124)
        for key in ("best_x", "best_f", "history", "n_fes", "time"):
            self.assertIn(key, a)
        self.assertEqual(a["n_fes"], 600)
        self.assertEqual(a["best_f"], b["best_f"])
        np.testing.assert_array_equal(a["best_x"], b["best_x"])
        self.assertEqual(a["history"], b["history"])
        self.assertFalse(np.array_equal(a["best_x"], c["best_x"]))
        self.assertTrue(np.all((p.lb <= a["best_x"]) & (a["best_x"] <= p.ub)))
        self.assertEqual(p.evaluate(a["best_x"]), a["best_f"])
        self.assertEqual(a["history"][-1], (600, a["best_f"]))
        self.assertTrue(
            all(x[0] < y[0] and x[1] >= y[1] for x, y in zip(a["history"], a["history"][1:]))
        )
        self.assertCountEqual(p.decode(a["best_x"]).tolist(), range(p.dim))

    def test_exact_odd_and_tiny_budgets(self):
        for budget in (1, 7, 29, 30, 31, 73, 121, 137, 1001):
            wrapped = CountingProblem(Problem("ta001"))
            result = rime(wrapped, budget, 2026)
            self.assertEqual(wrapped.calls, budget)
            self.assertEqual(result["n_fes"], budget)
            self.assertEqual(wrapped.bad, 0)
            self.assertEqual(result["history"][-1][0], budget)

    def test_reference_helpers(self):
        self.assertEqual(_matlab_round_nonnegative(0.5), 1.0)
        self.assertEqual(_matlab_round_nonnegative(1.5), 2.0)
        np.testing.assert_allclose(_normalized_rates(np.array([3.0, 4.0])), [0.6, 0.8])

    def test_full_course_budget_ta001(self):
        p = Problem("ta001")
        wrapped = CountingProblem(p)
        result = rime(wrapped, MAX_FES["ta001"], 2026)
        self.assertEqual(wrapped.calls, 20_000)
        self.assertEqual(wrapped.bad, 0)
        self.assertEqual(result["n_fes"], 20_000)
        self.assertEqual(p.objective(p.decode(result["best_x"])), result["best_f"])
        self.assertGreaterEqual(result["best_f"], p.reference_value)

    def test_invalid_parameters(self):
        p = Problem("ta001")
        invalid = (
            {"max_fes": 0, "seed": 1},
            {"max_fes": 100, "seed": 1, "pop_size": 0},
            {"max_fes": 100, "seed": 1, "w": 0},
        )
        for kwargs in invalid:
            with self.assertRaises(ValueError):
                rime(p, **kwargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
