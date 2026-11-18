"""Independent acceptance checks for the PFSP model."""
import hashlib
import json
import unittest
from contextlib import contextmanager
from itertools import permutations
from unittest.mock import patch

import numpy as np

from test_problem import ROOT, SMALL_P, SMALL_PERM, Problem, independent_makespan


DATA = ROOT / "data" / "taillard"
EXPECTED_SHAPES = {"ta001": (20, 5), "ta011": (20, 10), "ta021": (20, 20)}
WAITING_FOR_REFERENCE = (
    "Doğrulama Bekliyor (Referans permütasyon henüz temin edilmedi)"
)


class TestIndependentModelValidation(unittest.TestCase):
    def test_data_loading(self):
        readme = (DATA.parent / "README.md").read_text(encoding="utf-8")
        for name, shape in EXPECTED_SHAPES.items():
            with self.subTest(instance=name):
                raw = (DATA / f"{name}.txt").read_bytes()
                header, *rows = raw.decode("utf-8").splitlines()
                self.assertEqual(tuple(map(int, header.split())), shape)
                self.assertEqual(len(rows), shape[0])
                matrix = [list(map(int, row.split())) for row in rows]
                for row in matrix:
                    self.assertEqual(len(row), shape[1])
                    self.assertTrue(all(1 <= duration <= 99 for duration in row))

                documented_row, = (
                    line for line in readme.splitlines()
                    if line.startswith(f"| {name} |")
                )
                documented_hash = documented_row.split("|")[-2].strip().strip("`")
                self.assertEqual(hashlib.sha256(raw).hexdigest(), documented_hash)
                model = Problem(name)
                self.assertEqual((model.n_jobs, model.n_machines), shape)
                self.assertTrue(np.issubdtype(model.processing_times.dtype, np.integer))
                np.testing.assert_array_equal(model.processing_times, matrix)

    def test_valid_permutation(self):
        model = Problem("ta011")
        keys = np.resize([0.7, 0.2, 0.2, 0.4], model.n_jobs)
        decoded = model.decode(keys)
        self.assertTrue(np.issubdtype(decoded.dtype, np.integer))
        self.assertCountEqual(decoded.tolist(), range(model.n_jobs))
        reported = list(map(int, model.details(keys)["permutation"].split()))
        self.assertEqual(reported, (decoded + 1).tolist())

        for invalid in (decoded[:-1], np.append(decoded[:-1], decoded[0])):
            with self.subTest(permutation=invalid.tolist()):
                with self.assertRaises(ValueError):
                    model.objective(invalid)

    def test_documented_five_jobs_three_machines(self):
        fixture = {
            "processing_times": SMALL_P.copy(),
            "bks": 20,
            "reference_permutation_0_based": SMALL_PERM.tolist(),
        }
        with patch.object(Problem, "_load_data", return_value=fixture):
            model = Problem("ta001")
        expected = independent_makespan(SMALL_P, SMALL_PERM)
        keys = model.encode_permutation(SMALL_PERM)
        self.assertEqual(expected, 20)
        self.assertEqual(model.objective(SMALL_PERM), expected)
        self.assertEqual(model.evaluate(keys), expected)

    def test_ta001_reference_makespan(self):
        try:
            metadata = json.loads(
                (DATA / "reference_solutions.json").read_text(encoding="utf-8")
            )
        except FileNotFoundError:
            self.skipTest(WAITING_FOR_REFERENCE)

        reference = metadata["instances"].get("ta001", {})
        zero_based = reference.get("reference_permutation_0_based")
        one_based = reference.get("reference_permutation_1_based")
        if zero_based in (None, []) and one_based in (None, []):
            self.skipTest(WAITING_FOR_REFERENCE)

        # A present but damaged reference must produce a failure.
        for permutation, start in ((zero_based, 0), (one_based, 1)):
            if permutation is not None:
                self.assertIsInstance(permutation, list)
                self.assertTrue(all(type(job) is int for job in permutation))
                self.assertCountEqual(permutation, range(start, start + 20))
        if zero_based is None:
            zero_based = [job - 1 for job in one_based]
        if one_based is not None:
            self.assertEqual(one_based, [job + 1 for job in zero_based])

        model = Problem("ta001")
        permutation = np.array(zero_based)
        expected = independent_makespan(model.processing_times, permutation)
        self.assertEqual(reference["bks"], 1278)
        self.assertEqual(expected, 1278)
        self.assertEqual(model.objective(permutation), expected)
        keys = model.encode_permutation(permutation)
        np.testing.assert_array_equal(model.decode(keys), permutation)
        self.assertEqual(model.evaluate(keys), expected)

    def test_determinism(self):
        for name in EXPECTED_SHAPES:
            with self.subTest(instance=name):
                model = Problem(name)
                keys = np.resize([0.8, 0.1, 0.4, 0.1], model.n_jobs)
                expected_order = sorted(range(model.n_jobs), key=keys.__getitem__)
                expected_cmax = independent_makespan(
                    model.processing_times, np.array(expected_order)
                )
                expected_details = model.details(keys)
                self.assertEqual(expected_details["cmax"], expected_cmax)
                for trial in range(5):
                    with self.subTest(trial=trial + 1):
                        np.testing.assert_array_equal(
                            model.decode(keys.copy()), expected_order
                        )
                        self.assertEqual(model.evaluate(keys.copy()), expected_cmax)
                        self.assertEqual(model.details(keys.copy()), expected_details)


class TestSecondStageModelValidation(unittest.TestCase):
    def test_objective_boundary_dimensions_and_equal_times(self):
        cases = (
            ([[1]], [0], 1),
            ([[99, 1, 99]], [0], 199),
            ([[1], [99], [42]], [0, 1, 2], 142),
            ([[1], [99], [42]], [2, 0, 1], 142),
            ([[99] * 4] * 3, [2, 0, 1], 594),
            ([[99] * 4] * 3, [0, 1, 2], 594),
            ([[99] * 20] * 20, list(range(20)), 3861),
        )
        for matrix, order, expected in cases:
            with self.subTest(shape=np.shape(matrix), order=order):
                model = model_for_matrix(matrix)
                self.assertEqual(model.objective(order), expected)
                self.assertEqual(model.evaluate(model.encode_permutation(order)), expected)

    def test_malformed_benchmark_files(self):
        cases = (
            ("empty", "", "Empty instance"),
            ("missing dimension", "2\n1 2\n3 4", "Invalid header"),
            ("text dimension", "2 x\n1 2\n3 4", "Invalid header"),
            ("zero jobs", "0 2\n1 2", "expected 0 job rows"),
            ("negative jobs", "-2 2\n1 2\n3 4", "expected -2 job rows"),
            ("zero machines", "2 0\n1\n2", "expected 0"),
            ("negative machines", "2 -1\n1\n2", "expected -1"),
            ("missing row", "2 2\n1 2", "expected 2 job rows"),
            ("extra row", "1 2\n1 2\n3 4", "expected 1 job rows"),
            ("short row", "2 2\n1\n3 4", "row 1 has 1 values"),
            ("long row", "2 2\n1 2 3\n3 4", "row 1 has 3 values"),
            ("decimal", "2 2\n1.5 2\n3 4", "invalid literal"),
            ("text", "2 2\nx 2\n3 4", "invalid literal"),
            ("negative time", "2 2\n-1 2\n3 4", "processing times"),
            ("zero time", "2 2\n0 2\n3 4", "processing times"),
            ("time above upper bound", "2 2\n100 2\n3 4", "processing times"),
        )
        for label, raw, message in cases:
            with self.subTest(case=label), benchmark_fixture(raw):
                with self.assertRaisesRegex(ValueError, message):
                    Problem("ta001")

        with benchmark_fixture("2 2\n1 99\n99 1"):
            np.testing.assert_array_equal(Problem("ta001").processing_times, [[1, 99], [99, 1]])

    def test_benchmark_integrity_and_reference_errors(self):
        raw = "2 2\n1 2\n3 4"
        with benchmark_fixture(raw), patch.object(type(DATA), "exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                Problem("ta001")
        cases = (
            ({"sha256": "0" * 64}, "SHA-256 mismatch"),
            ({"machines": 3}, "dimensions disagree"),
            ({"reference_permutation_0_based": [0, 0]}, "invalid reference permutation"),
            ({"reference_permutation_0_based": [0]}, "invalid reference permutation"),
            ({"reference_permutation_0_based": [0, 2]}, "invalid reference permutation"),
        )
        for overrides, message in cases:
            with self.subTest(overrides=overrides), benchmark_fixture(raw, **overrides):
                with self.assertRaisesRegex(ValueError, message):
                    Problem("ta001")

    def test_invalid_permutations_across_public_methods(self):
        model = model_for_matrix(SMALL_P)
        cases = ([0, 1, 2, 3], [0, 1, 2, 3, 3], [-1, 1, 2, 3, 4],
                 [0, 1, 2, 3, 5], [0, 1, 2, 3, 3.5], [[0, 1, 2, 3, 4]])
        for method in (model.objective, model.constraints, model.encode_permutation):
            for order in cases:
                with self.subTest(method=method.__name__, order=order):
                    with self.assertRaises(ValueError):
                        method(order)

    def test_random_key_shape_and_nan_errors(self):
        model = model_for_matrix(SMALL_P)
        for method in (model.decode, model.evaluate, model.details):
            for keys in ([0.5] * 4, [[0.5] * 5], [np.nan] + [0.5] * 4):
                with self.subTest(method=method.__name__, keys=keys):
                    with self.assertRaises(ValueError):
                        method(keys)

    def test_infinite_random_keys_follow_current_clipping_behavior(self):
        model = model_for_matrix(SMALL_P)
        for value, bound in ((np.inf, 1.0), (-np.inf, 0.0)):
            with self.subTest(value=value):
                keys = [value, 0.3, 0.6, 0.2, 0.4]
                with self.assertRaises(ValueError):
                    model.decode(keys)
                bounded_keys = [bound, *keys[1:]]
                self.assertEqual(model.evaluate(keys), model.evaluate(bounded_keys))
                self.assertEqual(model.details(keys), model.details(bounded_keys))

    def test_schedule_against_hand_calculated_operations(self):
        cases = (
            (SMALL_P, SMALL_PERM,
             [[0, 1, 5], [1, 5, 8], [3, 8, 12], [6, 12, 14], [9, 14, 17]],
             [[1, 5, 7], [3, 8, 12], [6, 12, 14], [9, 14, 17], [13, 15, 20]],
             [[0, 0, 0, 0, 0, 7], [1, 0, 0, 0, 0, 5], [5, 1, 0, 0, 0, 0]]),
            ([[1, 4], [6, 1]], [0, 1], [[0, 1], [1, 7]], [[1, 5], [7, 8]],
             [[0, 0, 1], [1, 2, 0]]),
        )
        for matrix, order, expected_start, expected_finish, expected_idle in cases:
            with self.subTest(shape=np.shape(matrix)):
                start, finish = reference_schedule(matrix, order)
                np.testing.assert_array_equal(start, expected_start)
                np.testing.assert_array_equal(finish, expected_finish)
                cmax = expected_finish[-1][-1]
                self.assertEqual(model_for_matrix(matrix).objective(order), cmax)
                self.assertTrue(np.all(start[1:, :] >= finish[:-1, :]))
                self.assertTrue(np.all(start[:, 1:] >= finish[:, :-1]))
                np.testing.assert_array_equal(finish - start, np.asarray(matrix)[order])
                for machine, gaps in enumerate(expected_idle):
                    previous = np.r_[0, finish[:, machine]]
                    following = np.r_[start[:, machine], cmax]
                    np.testing.assert_array_equal(following - previous, gaps)
                    self.assertEqual(sum(gaps) + sum(np.asarray(matrix)[:, machine]), cmax)

    def test_all_small_instance_permutations(self):
        model = model_for_matrix(SMALL_P)
        observed = set()
        for order in permutations(range(len(SMALL_P))):
            with self.subTest(order=order):
                expected = reference_schedule(SMALL_P, order)[1][-1, -1]
                actual = model.objective(order)
                self.assertEqual(actual, expected)
                observed.add(actual)
        self.assertGreater(len(observed), 1)

    def test_course_api_and_rpd(self):
        for name in EXPECTED_SHAPES:
            model = Problem(name)
            for order in (model.reference_permutation, np.arange(model.n_jobs)):
                with self.subTest(instance=name, order=order.tolist()):
                    keys = model.encode_permutation(order)
                    np.testing.assert_array_equal(model.decode(keys), order)
                    expected = independent_makespan(model.processing_times, order)
                    self.assertEqual(model.evaluate(keys), expected)
                    details = model.details(keys)
                    self.assertEqual(details["objective"], expected)
                    self.assertEqual(details["cmax"], expected)
                    self.assertEqual(details["rpd"], 100 * (expected - model.reference_value)
                                     / model.reference_value)
                    self.assertEqual(model.constraints(order).size, 0)
                    self.assertEqual(details["violation"], 0)
                    self.assertIs(details["feasible"], True)

    def test_registered_algorithms_use_real_evaluation_budget(self):
        from main import ALGORITHMS

        self.assertTrue(ALGORITHMS)
        budget, seed = 73, 20261118
        for name, (algorithm, params) in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                model = Problem("ta001")
                with patch.object(model, "evaluate", wraps=model.evaluate) as evaluate:
                    first = algorithm(model, budget, seed, **params)
                    self.assertEqual(evaluate.call_count, first["n_fes"])
                    evaluate.reset_mock()
                    second = algorithm(model, budget, seed, **params)
                    self.assertEqual(evaluate.call_count, second["n_fes"])
                self.assertEqual(first["n_fes"], budget)
                self.assertEqual(second["n_fes"], budget)
                for result in (first, second):
                    keys = result["best_x"]
                    self.assertEqual(keys.shape, (model.dim,))
                    self.assertTrue(np.all((model.lb <= keys) & (keys <= model.ub)))
                    order = model.decode(keys)
                    self.assertCountEqual(order.tolist(), range(model.n_jobs))
                    self.assertEqual(result["best_f"],
                                     independent_makespan(model.processing_times, order))
                    history = result["history"]
                    self.assertEqual(history[-1], (budget, result["best_f"]))
                    self.assertTrue(all(a[0] < b[0] and a[1] >= b[1]
                                        for a, b in zip(history, history[1:])))
                np.testing.assert_array_equal(first["best_x"], second["best_x"])
                self.assertEqual(first["history"], second["history"])


def model_for_matrix(matrix):
    matrix = np.asarray(matrix, dtype=np.int64)
    fixture = {
        "processing_times": matrix,
        "bks": 1,
        "reference_permutation_0_based": list(range(len(matrix))),
    }
    with patch.object(Problem, "_load_data", return_value=fixture):
        return Problem("ta001")


@contextmanager
def benchmark_fixture(text, **metadata_overrides):
    raw = text.encode("utf-8")
    record = {
        "jobs": 2, "machines": 2, "sha256": hashlib.sha256(raw).hexdigest(),
        "seed": 1, "bks": 8, "reference_permutation_0_based": [0, 1],
    }
    record.update(metadata_overrides)
    metadata = {"instances": {"ta001": record}}
    with (patch.object(type(DATA), "exists", return_value=True),
          patch.object(type(DATA), "read_bytes", return_value=raw),
          patch("problem._load_reference_metadata", return_value=metadata)):
        yield


def reference_schedule(matrix, order):
    """Calculate with Python integers, visiting all jobs machine by machine."""
    machine_count = len(matrix[0])
    starts = [[0] * machine_count for _ in order]
    finishes = [[0] * machine_count for _ in order]
    for machine in range(machine_count):
        machine_free = 0
        for position, job in enumerate(order):
            job_ready = finishes[position][machine - 1] if machine else 0
            start = max(machine_free, job_ready)
            machine_free = start + int(matrix[job][machine])
            starts[position][machine] = start
            finishes[position][machine] = machine_free
    return np.array(starts), np.array(finishes)

if __name__ == "__main__":
    unittest.main(verbosity=2)
