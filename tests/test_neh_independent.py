"""Independent NEH baselines and method-level edge cases."""
import random
import unittest
from unittest.mock import Mock, patch

import numpy as np

from test_problem import Problem
from algorithms.de import de
from heuristics.neh import makespan, neh


def independent_schedule(matrix, order):
    """Build the full completion grid in machine-major order."""
    completion = [[0] * (matrix.shape[1] + 1) for _ in range(len(order) + 1)]
    for machine in range(1, matrix.shape[1] + 1):
        for row, job in enumerate(order, 1):
            completion[row][machine] = (
                max(completion[row - 1][machine], completion[row][machine - 1])
                + int(matrix[job, machine - 1])
            )
    return completion[-1][-1]


def independent_neh(matrix):
    order = []
    priority = sorted(range(len(matrix)), key=lambda job: (-sum(map(int, matrix[job])), job))
    for job in priority:
        candidates = [order[:i] + [job] + order[i:] for i in range(len(order) + 1)]
        order = min(candidates, key=lambda candidate: independent_schedule(matrix, candidate))
    return order


class TestNEHIndependentAcceptance(unittest.TestCase):
    def test_published_1983_example(self):
        matrix = np.array([[5, 9, 8, 10, 1], [9, 3, 10, 1, 8],
                           [9, 4, 5, 8, 6], [4, 8, 8, 7, 2]])
        result = neh(matrix)
        self.assertEqual(result["permutation"].tolist(), [3, 2, 0, 1])
        self.assertEqual(result["cmax"], 54)
        self.assertEqual(independent_schedule(matrix, result["permutation"]), 54)

    def test_exact_taillard_baselines_and_seed_independence(self):
        expected = {
            "ta001": (1286, [3, 17, 9, 8, 15, 14, 11, 16, 13, 19, 6, 4, 5, 18, 1, 2, 10, 7, 20, 12]),
            "ta011": (1680, [18, 5, 2, 17, 3, 6, 12, 9, 15, 10, 20, 13, 8, 14, 19, 11, 4, 7, 1, 16]),
            "ta021": (2410, [16, 15, 10, 8, 9, 12, 13, 11, 5, 1, 20, 14, 17, 2, 18, 6, 7, 19, 3, 4]),
        }
        python_state, numpy_state = random.getstate(), np.random.get_state()
        self.addCleanup(random.setstate, python_state)
        self.addCleanup(np.random.set_state, numpy_state)
        for name, (cost, one_based) in expected.items():
            matrix = Problem(name).processing_times
            order = [job - 1 for job in one_based]
            self.assertEqual(independent_neh(matrix), order)
            self.assertEqual(independent_schedule(matrix, order), cost)
            for seed in (0, 1, 2026, 2055, 4294967295):
                with self.subTest(instance=name, seed=seed):
                    random.seed(seed)
                    np.random.seed(seed)
                    result = neh(matrix)
                    self.assertEqual(result["permutation"].tolist(), order)
                    self.assertEqual(result["cmax"], cost)

    def test_generated_matrices_match_classic_independent_insertion(self):
        rng = np.random.default_rng(20261123)
        for case in range(100):
            n, m = rng.integers(1, 10, size=2)
            matrix = rng.integers(1, 7, size=(n, m))
            with self.subTest(case=case, jobs=n, machines=m):
                order = independent_neh(matrix)
                result = neh(matrix)
                self.assertEqual(result["permutation"].tolist(), order)
                self.assertEqual(result["cmax"], independent_schedule(matrix, order))

    def test_invalid_values_are_rejected_without_truncation(self):
        for matrix in ([[1.9], [2.1]], [[-2]], [[0]], [[np.nan]], [[np.inf]],
                       [["1"]], [[True]], [[1 + 2j]]):
            with self.subTest(matrix=matrix):
                with self.assertRaises(ValueError):
                    neh(matrix)
                with self.assertRaises(ValueError):
                    makespan(matrix, range(len(matrix)))
        for order in ([.9, 1.9], [0, np.inf], [0, 0], [0, 2], [0]):
            with self.subTest(order=order), self.assertRaises(ValueError):
                makespan([[2], [3]], order)

    def test_integer_valued_inputs_and_large_totals(self):
        self.assertEqual(makespan([[2.0], [3.0]], [0.0, 1.0]), 5)
        large = np.iinfo(np.int64).max
        matrix = [[large], [large]]
        self.assertEqual(makespan(matrix, [0, 1]), 2 * large)
        self.assertEqual(neh(matrix)["cmax"], 2 * large)

    def test_de_recombination_threshold_is_strict_except_for_forced_index(self):
        problem = Mock(dim=2, lb=np.zeros(2), ub=np.ones(2))
        problem.evaluate.return_value = 0.0
        rng = Mock()
        rng.random.side_effect = [
            np.array([[.1, .2], [.7, .8], [.5, .5], [.5, .5]]),
            np.array([.9, .9]),
        ]
        rng.choice.return_value = [1, 2, 3]
        rng.integers.return_value = 0
        with patch("algorithms.de.np.random.default_rng", return_value=rng):
            result = de(problem, max_fes=5, seed=2026, pop_size=4, CR=.9)
        self.assertEqual(result["n_fes"], 5)
        np.testing.assert_allclose(problem.evaluate.call_args.args[0], [.7, .2])

    def test_direct_model_decode_preserves_unclipped_order(self):
        problem = Problem("ta001")
        keys = np.full(problem.dim, .5)
        keys[:2] = [-1.0, -2.0]
        self.assertEqual(problem.decode(keys)[:2].tolist(), [1, 0])
        clipped_order = problem.decode(problem.clip(keys))
        self.assertEqual(clipped_order[:2].tolist(), [0, 1])
        self.assertEqual(problem.evaluate(keys),
                         independent_schedule(problem.processing_times, clipped_order))
        self.assertEqual(problem.details(keys)["permutation"].split()[:2], ["1", "2"])
