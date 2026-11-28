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


class ScriptedRng:
    """Returns pre-set draws in call order: random() and standard_normal()."""

    def __init__(self, uniform, normal):
        self.uniform = list(uniform)
        self.normal = list(normal)

    def random(self, size=None):
        v = self.uniform.pop(0)
        return np.full(size, v, dtype=float) if size is not None else float(v)

    def standard_normal(self, size=None):
        return float(self.normal.pop(0))


def expected_search_rule(best, worst, x, rho, u_del, n1, r1, r2, n2):
    """Independent scalar (D=1) evaluation of SearchRule.m, Flag = 1."""
    d = u_del * abs(best - x)
    first = n1 * ((best - worst) * d) / (2 * (best + worst - 2 * x))
    xa = x - first + rho
    m = xa + x                      # mean over one dimension
    yp, yq = r1 * (m + r1 * d), r2 * (m - r2 * d)
    return n2 * ((yp - yq) * d) / (2 * (yp + yq - 2 * x))


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

    def check_near_zero(self, best, worst, x, rho, u_del, n1, r1, r2, n2, which, sign):
        rng = ScriptedRng([u_del, r1, r2], [n1, n2])
        a = lambda v: np.array([v], dtype=float)  # noqa: E731
        out = _search_rule(rng, a(best), a(worst), a(x), a(rho))
        exp = expected_search_rule(best, worst, x, rho, u_del, n1, r1, r2, n2)
        # The denominator under test really is tiny and has the intended sign.
        d = u_del * abs(best - x)
        den1 = best + worst - 2 * x
        xa = x - n1 * ((best - worst) * d) / (2 * den1) + rho
        m = xa + x
        den2 = r1 * (m + r1 * d) + r2 * (m - r2 * d) - 2 * x
        den = den1 if which == 1 else den2
        self.assertTrue(0 < abs(den) < 1e-9 and np.sign(den) == sign, den)
        self.assertTrue(np.all(np.isfinite(out)))
        np.testing.assert_allclose(out, [exp], rtol=1e-12, atol=0)
        return float(out[0])

    def test_first_denominator_near_zero_positive_and_negative(self):
        eps = 1e-12
        for sign in (1, -1):
            with self.subTest(sign=sign):
                # best + worst - 2x = sign * eps
                self.check_near_zero(best=0.7 + sign * eps, worst=0.3, x=0.5, rho=0.05,
                                     u_del=0.5, n1=1.0, r1=0.3, r2=0.6, n2=1.0,
                                     which=1, sign=sign)

    def test_second_denominator_near_zero_positive_and_negative(self):
        eps = 1e-12
        best, worst, x, rho, u_del, n1 = 0.6, 0.9, 0.4, 0.05, 0.5, 1.0
        d = u_del * abs(best - x)
        m = (x - n1 * ((best - worst) * d) / (2 * (best + worst - 2 * x)) + rho) + x
        for sign in (1, -1):
            with self.subTest(sign=sign):
                # With r1 = r2 = r: yp + yq - 2x = 2*r*m - 2x = sign * eps.
                r = (2 * x + sign * eps) / (2 * m)
                out = self.check_near_zero(best, worst, x, rho, u_del, n1, r, r, 1.0,
                                           which=2, sign=sign)
                self.assertGreater(abs(out), 1e6)   # huge but finite step

    def test_large_finite_steps_in_real_runs_are_bounded_before_evaluation(self):
        # Measured on ta001/ta021 (seeds 2026-2028): 0.16-0.45 % of NRSR components
        # exceed the whole range (|NRSR| > 1). They must be clipped, never evaluated raw.
        import algorithms.nrbo as module
        large = [0]
        original = module._search_rule

        def spy(*args):
            out = original(*args)
            large[0] += int(np.sum(np.abs(out[np.isfinite(out)]) > 1))
            return out

        wrapped = CountingProblem(Problem("ta021"))
        module._search_rule = spy
        try:
            r = nrbo(wrapped, max_fes=10_000, seed=2026)
        finally:
            module._search_rule = original
        self.assertGreater(large[0], 0)
        self.assertEqual(wrapped.calls, 10_000)
        self.assertEqual(wrapped.bad, 0)
        self.assertEqual(r["n_fes"], 10_000)

    def test_invalid_parameters_are_rejected(self):
        p = Problem("ta001")
        with self.assertRaises(ValueError):
            nrbo(p, max_fes=100, seed=1, DF=1.5)
        with self.assertRaises(ValueError):
            nrbo(p, max_fes=100, seed=1, pop_size=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
