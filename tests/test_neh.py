"""Acceptance tests for the deterministic NEH baseline."""
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from problem import INSTANCES, Problem  # noqa: E402
from heuristics.neh import makespan, neh  # noqa: E402


SMALL_P = np.array([
    [3, 4, 2],
    [2, 3, 4],
    [4, 1, 3],
    [1, 4, 2],
    [3, 2, 3],
], dtype=np.int64)


class TestNEH(unittest.TestCase):
    def test_small_instance_is_deterministic_and_valid(self):
        a = neh(SMALL_P)
        b = neh(SMALL_P)
        np.testing.assert_array_equal(a["permutation"], b["permutation"])
        self.assertEqual(a["cmax"], b["cmax"])
        self.assertCountEqual(a["permutation"].tolist(), range(5))
        self.assertEqual(a["cmax"], makespan(SMALL_P, a["permutation"]))
        self.assertEqual(a["cmax"], 19)

    def test_tie_breaks_are_deterministic(self):
        p = np.ones((4, 3), dtype=np.int64)
        result = neh(p)
        self.assertCountEqual(result["permutation"].tolist(), range(4))
        self.assertEqual(result["cmax"], 6)
        np.testing.assert_array_equal(result["permutation"], [3, 2, 1, 0])

    def test_all_taillard_instances_are_valid(self):
        for name in INSTANCES:
            with self.subTest(instance=name):
                problem = Problem(name)
                result = neh(problem.processing_times)
                perm = result["permutation"]
                self.assertEqual(perm.shape, (problem.n_jobs,))
                self.assertCountEqual(perm.tolist(), range(problem.n_jobs))
                self.assertEqual(result["cmax"], problem.objective(perm))

    def test_invalid_inputs(self):
        for p in (np.array([]), np.array([1, 2, 3]), np.array([[1, 0], [2, 3]])):
            with self.subTest(shape=np.shape(p)):
                with self.assertRaises(ValueError):
                    neh(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
