from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from algorithms.nrbo import _search_rule, nrbo  # noqa: E402
from problem import MAX_FES, Problem  # noqa: E402


class CountingProblem:
    """Wraps a problem; counts calls and flags non-finite or out-of-bound x."""

    def __init__(self, inner):
        self.inner = inner
        self.dim, self.lb, self.ub = inner.dim, inner.lb, inner.ub
        self.calls = 0
        self.bad = 0

    def evaluate(self, x):
        self.calls += 1
        x = np.asarray(x, dtype=float)
        if (not np.all(np.isfinite(x))) or np.any(x < self.lb) or np.any(x > self.ub):
            self.bad += 1
        return self.inner.evaluate(x)


class DegenerateProblem:
    """lb == ub: every position is the same point, so best = worst = x and the
    NRSR denominator is exactly 0 (0/0 -> NaN) at every step. Checks that no
    NaN/Inf reaches evaluate()."""

    dim = 5
    lb = np.full(5, 0.5)
    ub = np.full(5, 0.5)

    def __init__(self):
        self.bad = 0
        self.calls = 0

    def evaluate(self, x):
        self.calls += 1
        x = np.asarray(x, dtype=float)
        if (not np.all(np.isfinite(x))) or np.any(x != 0.5):
            self.bad += 1
        return 1.0


class TestNewtonRaphsonBasedOptimizer(unittest.TestCase):
    def test_contract_budget_and_reproducibility_on_pfsp(self):
        p = Problem("ta001")
        r1 = nrbo(p, max_fes=600, seed=123)
        r2 = nrbo(p, max_fes=600, seed=123)
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
        a = nrbo(p, max_fes=900, seed=2027)
        b = nrbo(p, max_fes=900, seed=2027)
        c = nrbo(p, max_fes=900, seed=2028)
        self.assertEqual(a["best_f"], b["best_f"])
        self.assertTrue(np.array_equal(a["best_x"], b["best_x"]))
        self.assertEqual(a["history"], b["history"])
        self.assertFalse(np.array_equal(a["best_x"], c["best_x"]))

    def test_independent_fe_counter_and_bounds_for_odd_budgets(self):
        for budget in (1, 29, 30, 31, 137, 1001):
            wrapped = CountingProblem(Problem("ta001"))
            r = nrbo(wrapped, max_fes=budget, seed=5)
            self.assertEqual(wrapped.calls, budget, budget)
            self.assertEqual(r["n_fes"], budget, budget)
            self.assertEqual(wrapped.bad, 0, budget)

    def test_full_course_budget_ta001(self):
        p = Problem("ta001")
        wrapped = CountingProblem(p)
        r = nrbo(wrapped, max_fes=MAX_FES["ta001"], seed=2026)
        self.assertEqual(wrapped.calls, 20_000)
        self.assertEqual(wrapped.bad, 0)
        self.assertEqual(r["n_fes"], 20_000)
        perm = p.decode(r["best_x"])
        self.assertEqual(p.objective(perm), r["best_f"])
        self.assertGreaterEqual(r["best_f"], p.reference_value)

    def test_search_rule_zero_denominator_gives_nan(self):
        # Precondition for the next test: the case really is 0/0.
        rng = np.random.default_rng(0)
        x = np.full(5, 0.5)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = _search_rule(rng, x.copy(), x.copy(), x, np.zeros(5))
        self.assertTrue(np.all(np.isnan(out)))

    def test_zero_denominator_never_produces_nan_candidates(self):
        deg = DegenerateProblem()
        r = nrbo(deg, max_fes=3000, seed=11)
        self.assertEqual(deg.calls, 3000)
        self.assertEqual(deg.bad, 0)
        self.assertEqual(r["n_fes"], 3000)

    def test_invalid_parameters_are_rejected(self):
        p = Problem("ta001")
        with self.assertRaises(ValueError):
            nrbo(p, max_fes=100, seed=1, DF=1.5)
        with self.assertRaises(ValueError):
            nrbo(p, max_fes=100, seed=1, pop_size=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
