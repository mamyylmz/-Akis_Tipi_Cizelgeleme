from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from algorithms.de import de  # noqa: E402
from problem import Problem  # noqa: E402


class TestDifferentialEvolution(unittest.TestCase):
    def test_contract_budget_and_reproducibility_on_pfsp(self):
        p = Problem("ta001")
        kwargs = {"max_fes": 600, "seed": 123, "pop_size": 40, "F": 0.5, "CR": 0.9}
        r1 = de(p, **kwargs)
        r2 = de(p, **kwargs)
        for key in ("best_x", "best_f", "history", "n_fes", "time"):
            self.assertIn(key, r1)
        self.assertEqual(r1["n_fes"], 600)
        self.assertEqual(r2["n_fes"], 600)
        self.assertEqual(r1["best_f"], r2["best_f"])
        self.assertTrue(np.array_equal(r1["best_x"], r2["best_x"]))
        self.assertTrue(np.all(r1["best_x"] >= p.lb))
        self.assertTrue(np.all(r1["best_x"] <= p.ub))
        self.assertEqual(float(p.evaluate(r1["best_x"])), float(r1["best_f"]))
        self.assertEqual(r1["history"][-1][0], 600)
        values = np.array([v for _, v in r1["history"]], dtype=float)
        self.assertTrue(np.all(np.diff(values) <= 1e-12))
        self.assertEqual(sorted(p.decode(r1["best_x"]).tolist()), list(range(20)))

    def test_default_population_rule_is_compatible_with_20_job_problem(self):
        p = Problem("ta001")
        r = de(p, max_fes=120, seed=7)  # default NP = 5*D = 100
        self.assertEqual(r["n_fes"], 120)
        self.assertTrue(np.isfinite(r["best_f"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
