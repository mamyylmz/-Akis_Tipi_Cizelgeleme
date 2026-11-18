from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from problem import INSTANCES, MAX_FES, Problem  # noqa: E402


SMALL_P = np.array([
    [3, 4, 2],
    [2, 3, 4],
    [4, 1, 3],
    [1, 4, 2],
    [3, 2, 3],
], dtype=int)
SMALL_PERM = np.array([3, 1, 0, 4, 2], dtype=int)  # J4,J2,J1,J5,J3

TA001_MACHINE_MAJOR = np.array([
    [54,83,15,71,77,36,53,38,27,87,76,91,14,29,12,77,32,87,68,94],
    [79,3,11,99,56,70,99,60,5,56,3,61,73,75,47,14,21,86,5,77],
    [16,89,49,15,89,45,60,23,57,64,7,1,63,41,63,47,26,75,77,40],
    [66,58,31,68,78,91,13,59,49,85,85,9,39,41,56,40,54,77,51,31],
    [58,56,20,85,53,35,53,41,69,13,86,72,8,49,47,87,58,18,68,28],
], dtype=int)


def independent_makespan(processing_times: np.ndarray, permutation: np.ndarray) -> int:
    """Independent 2-D dynamic-programming implementation used only in tests."""
    p = np.asarray(processing_times, dtype=int)
    perm = np.asarray(permutation, dtype=int)
    n, m = len(perm), p.shape[1]
    c = np.zeros((n + 1, m + 1), dtype=np.int64)
    for i in range(1, n + 1):
        job = perm[i - 1]
        for j in range(1, m + 1):
            c[i, j] = max(c[i - 1, j], c[i, j - 1]) + p[job, j - 1]
    return int(c[n, m])


class TestPFSPProblem(unittest.TestCase):
    def test_small_documented_example_is_20(self):
        self.assertEqual(independent_makespan(SMALL_P, SMALL_PERM), 20)

    def test_required_instance_dimensions_and_budgets(self):
        expected = {
            "ta001": (20, 5, 20_000),
            "ta011": (20, 10, 30_000),
            "ta021": (20, 20, 40_000),
        }
        self.assertEqual(INSTANCES, ["ta001", "ta011", "ta021"])
        for name, (n, m, budget) in expected.items():
            p = Problem(name)
            self.assertEqual((p.n_jobs, p.n_machines), (n, m))
            self.assertEqual(MAX_FES[name], budget)
            self.assertTrue(np.all((p.processing_times >= 1) & (p.processing_times <= 99)))

    def test_ta001_matches_or_library_published_verification_matrix(self):
        p = Problem("ta001")
        self.assertTrue(np.array_equal(p.processing_times.T, TA001_MACHINE_MAJOR))

    def test_stable_random_key_decode_is_valid_and_deterministic(self):
        p = Problem("ta001")
        x = np.array([0.3, 0.1, 0.1, 0.9, 0.2] + list(np.linspace(0.31, 0.8, 15)))
        perm1 = p.decode(x)
        perm2 = p.decode(x.copy())
        self.assertTrue(np.array_equal(perm1, perm2))
        self.assertEqual(sorted(perm1.tolist()), list(range(20)))
        # Equal keys at indices 1 and 2 retain their original order under stable sort.
        self.assertLess(int(np.where(perm1 == 1)[0][0]), int(np.where(perm1 == 2)[0][0]))

    def test_invalid_permutations_are_rejected(self):
        p = Problem("ta001")
        duplicate = np.arange(20)
        duplicate[-1] = 0
        with self.assertRaises(ValueError):
            p.objective(duplicate)
        with self.assertRaises(ValueError):
            p.objective(np.arange(19))
        with self.assertRaises(ValueError):
            p.objective(np.arange(20) + 1)

    def test_reference_permutations_recompute_published_values(self):
        for name in INSTANCES:
            p = Problem(name)
            observed_prod = int(p.objective(p.reference_permutation))
            observed_ind = independent_makespan(p.processing_times, p.reference_permutation)
            self.assertEqual(observed_prod, p.reference_value, name)
            self.assertEqual(observed_ind, p.reference_value, name)
            x = p.encode_permutation(p.reference_permutation)
            self.assertTrue(np.array_equal(p.decode(x), p.reference_permutation), name)
            self.assertEqual(int(p.evaluate(x)), p.reference_value, name)
            self.assertAlmostEqual(p.details(x)["rpd"], 0.0, places=12)

    def test_production_and_independent_makespan_match_random_permutations(self):
        rng = np.random.default_rng(20261118)
        for name in INSTANCES:
            p = Problem(name)
            for _ in range(25):
                perm = rng.permutation(p.n_jobs)
                self.assertEqual(
                    int(p.objective(perm)),
                    independent_makespan(p.processing_times, perm),
                    name,
                )

    def test_metadata_reference_permutations_are_complete(self):
        meta = json.loads((ROOT / "data" / "taillard" / "reference_solutions.json").read_text())
        for name in INSTANCES:
            one_based = meta["instances"][name]["reference_permutation_1_based"]
            self.assertEqual(sorted(one_based), list(range(1, 21)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
