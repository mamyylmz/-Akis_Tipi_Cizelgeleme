import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from test_problem import ROOT, Problem
from experiment_validation import (
    expected_manifest, read_manifest, validate_results,
)
from main import ALGORITHMS, ALPHA, SEED_BASE


class TestFinalAcceptanceRegressions(unittest.TestCase):
    def test_manifest_preserves_provenance_and_rejects_changes(self):
        expected = expected_manifest(ROOT, ALGORITHMS, 1, SEED_BASE, ALPHA)
        self.assertEqual(len(expected["files"]), 15)
        self.assertEqual(len(expected["data_sha256"]), 3)
        for field, invalid in (("commit", "bad"), ("data_sha256", {}),
                               ("seeds", [0]), ("files", []), ("algorithms", {})):
            with self.subTest(field=field):
                path = Path("in-memory-manifest.json")
                with patch.object(Path, "read_text", return_value=json.dumps(expected)):
                    self.assertEqual(read_manifest(path, ROOT, ALGORITHMS, SEED_BASE, ALPHA), expected)
                with patch.object(Path, "read_text",
                                  return_value=json.dumps({**expected, field: invalid})):
                    with self.assertRaisesRegex(ValueError, field):
                        read_manifest(path, ROOT, ALGORITHMS, SEED_BASE, ALPHA)

    def test_csv_rejects_corrupt_runs_and_incomplete_coverage(self):
        p = Problem("ta001")
        keys = p.encode_permutation(p.reference_permutation)
        row = {
            "run": 1, "seed": 2026, "n_fes": 20_000, "time": 1.0,
            "best_f": 1278, **p.details(keys), "best_x": json.dumps(keys.tolist()),
            "history_fes": "[1, 20000]", "history_f": "[1300, 1278]",
        }
        manifest = {"files": ["ta001/RIME.csv"], "algorithms": {"RIME": {}},
                    "max_fes": {"ta001": 20_000}, "seeds": [2026], "runs": 1}
        folder = Path.cwd() / "raw-validation-fixture"
        path = folder / manifest["files"][0]

        def open_csv(rows):
            stream = StringIO()
            writer = csv.DictWriter(stream, row.keys())
            writer.writeheader()
            writer.writerows(rows)
            stream.seek(0)
            return stream

        with patch.object(Path, "rglob", return_value=[]):
            with self.assertRaisesRegex(ValueError, "coverage"):
                validate_results(folder, manifest)
        with (patch.object(Path, "rglob", return_value=[path]),
              patch("experiment_validation.Problem", return_value=p)):
            with patch.object(Path, "open", return_value=open_csv([row])):
                validate_results(folder, manifest)
            corrupt = [
                [row, row],
                [{**row, "run": 2}],
                [{**row, "seed": 0}],
                [{**row, "n_fes": 1}],
                [{**row, "best_f": -1}],
                [{**row, "best_x": json.dumps([2] * p.dim)}],
                [{**row, "history_fes": "[20000, 20000]"}],
                [{**row, "history_f": "[1200, 1278]"}],
            ]
            for rows in corrupt:
                with self.subTest(rows=rows), patch.object(Path, "open", return_value=open_csv(rows)):
                    with self.assertRaises(ValueError):
                        validate_results(folder, manifest)

    def test_taillard_checker_rejects_crlf_even_with_same_matrices(self):
        with tempfile.TemporaryDirectory(prefix="pfsp-hash-test-") as root:
            folder = Path(root) / "data" / "taillard"
            folder.mkdir(parents=True)
            for path in (ROOT / "data" / "taillard").iterdir():
                if path.name in {"ta001.txt", "ta011.txt", "ta021.txt", "reference_solutions.json"}:
                    (folder / path.name).write_bytes(path.read_bytes())
            command = [sys.executable, "-B", str(ROOT / "tools/review_independent_taillard_check.py"), root]
            env = dict(os.environ, PYTHONIOENCODING="utf-8")
            valid = subprocess.run(command, capture_output=True, env=env, check=False)
            self.assertEqual(valid.returncode, 0, valid.stderr)
            path = folder / "ta001.txt"
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
            invalid = subprocess.run(command, capture_output=True, env=env, check=False)
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn(b"GENEL: FAIL", invalid.stdout)

    def test_missing_required_algorithm_fails_runner(self):
        import main

        incomplete = {name: entry for name, entry in ALGORITHMS.items() if name != "RIME"}
        with patch.object(main, "ALGORITHMS", incomplete), patch.object(main, "check_problem"):
            with self.assertRaises(main.KontrolHatasi):
                main.run_checks()

    def test_nrbo_near_singular_steps_remain_finite_at_evaluation(self):
        from algorithms.nrbo import nrbo
        from test_audit_burak_task6 import FormulaProblem, scripted_rng

        for epsilon in (-1e-10, 1e-10):
            with self.subTest(epsilon=epsilon):
                import numpy as np

                initial = np.array([[.5 + epsilon, .5 - epsilon], [.2, .2], [.8, .8]])
                candidates = []
                for _ in range(2):
                    rng = scripted_rng(
                        [initial, .3, .15, np.array([.2, .3]), .3, .6,
                         np.array([.7, .6]), np.array([.55, .45]), .8],
                        [.5, -.4], indices=[np.array([1, 2])],
                    )
                    problem = FormulaProblem([2, 1, 3, 4])
                    with patch("algorithms.nrbo.np.random.default_rng", return_value=rng):
                        result = nrbo(problem, 4, 2026, pop_size=3)
                    self.assertEqual(result["n_fes"], 4)
                    self.assertTrue(np.all(np.isfinite(problem.candidates[-1])))
                    self.assertTrue(np.all((problem.candidates[-1] >= 0)
                                           & (problem.candidates[-1] <= 1)))
                    candidates.append(problem.candidates[-1])
                np.testing.assert_array_equal(*candidates)
