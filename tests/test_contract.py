from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from main import ALGORITHMS  # noqa: E402
from problem import MAX_FES, Problem  # noqa: E402


EXPECTED_ALGORITHMS = {"PSO", "DE", "DBO", "RIME", "NRBO"}


class TestAlgorithmContract(unittest.TestCase):
    def test_final_registry_contains_exact_five_algorithms(self):
        self.assertEqual(set(ALGORITHMS), EXPECTED_ALGORITHMS)

    def test_registered_algorithms_exact_budget_seed_and_solution_contract(self):
        budget = 73
        seed = 20261119
        for name, (algorithm, params) in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                p = Problem("ta001")
                with patch.object(p, "evaluate", wraps=p.evaluate) as evaluate:
                    first = algorithm(p, budget, seed, **params)
                    self.assertEqual(evaluate.call_count, budget)
                    evaluate.reset_mock()
                    second = algorithm(p, budget, seed, **params)
                    self.assertEqual(evaluate.call_count, budget)

                for result in (first, second):
                    self.assertEqual(result["n_fes"], budget)
                    x = np.asarray(result["best_x"], dtype=float)
                    self.assertEqual(x.shape, (p.dim,))
                    self.assertTrue(np.all(np.isfinite(x)))
                    self.assertTrue(np.all((p.lb <= x) & (x <= p.ub)))
                    permutation = p.decode(x)
                    self.assertCountEqual(permutation.tolist(), range(p.dim))
                    self.assertEqual(float(p.evaluate(x)), float(result["best_f"]))
                    history = result["history"]
                    self.assertGreaterEqual(len(history), 2)
                    self.assertEqual(history[-1], (budget, result["best_f"]))
                    self.assertTrue(
                        all(a[0] < b[0] for a, b in zip(history, history[1:]))
                    )
                    self.assertTrue(
                        all(a[1] >= b[1] for a, b in zip(history, history[1:]))
                    )

                np.testing.assert_array_equal(first["best_x"], second["best_x"])
                self.assertEqual(first["best_f"], second["best_f"])
                self.assertEqual(first["history"], second["history"])

    def test_different_seed_changes_search_state(self):
        p = Problem("ta001")
        for name, (algorithm, params) in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                first = algorithm(p, 121, 2026, **params)
                second = algorithm(p, 121, 2027, **params)
                self.assertFalse(
                    np.array_equal(first["best_x"], second["best_x"]),
                    f"{name}: fixed audit seeds unexpectedly returned identical best_x",
                )

    def test_course_instance_budgets_are_unchanged(self):
        self.assertEqual(
            MAX_FES,
            {"ta001": 20_000, "ta011": 30_000, "ta021": 40_000},
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
