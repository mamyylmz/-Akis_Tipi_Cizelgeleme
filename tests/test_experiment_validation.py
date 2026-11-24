from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TOOLS = ROOT / "tools"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(TOOLS))

from check_experiment_outputs import ALGORITHMS, _parse_bool, validate  # noqa: E402
from problem import INSTANCES, MAX_FES, Problem  # noqa: E402


def valid_row(instance: str) -> dict:
    problem = Problem(instance)
    x = problem.encode_permutation(problem.reference_permutation)
    best_f = float(problem.evaluate(x))
    details = problem.details(x)
    return {
        "run": 1,
        "seed": 2026,
        "best_f": best_f,
        **details,
        "n_fes": MAX_FES[instance],
        "time": 0.01,
        "best_x": json.dumps(x.tolist()),
        "history_fes": json.dumps([MAX_FES[instance]]),
        "history_f": json.dumps([best_f]),
    }


class ExperimentFixture:
    def __init__(self, root: Path):
        self.root = root
        for instance in INSTANCES:
            out = root / instance
            out.mkdir(parents=True, exist_ok=True)
            row = valid_row(instance)
            for algorithm in ALGORITHMS:
                pd.DataFrame([row]).to_csv(out / f"{algorithm}.csv", index=False)

    def mutate(self, instance: str, algorithm: str, field: str, value) -> None:
        path = self.root / instance / f"{algorithm}.csv"
        df = pd.read_csv(path)
        # Corruption tests intentionally inject values that may violate the
        # inferred pandas dtype (e.g. string "False" into a bool column).
        if isinstance(value, str):
            df[field] = df[field].astype(object)
        df.loc[0, field] = value
        df.to_csv(path, index=False)


class TestExperimentOutputValidator(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raw = Path(self.tmp.name)
        self.fixture = ExperimentFixture(self.raw)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_15_file_fixture_passes(self):
        self.assertEqual(validate(self.raw, runs=1, seed_base=2026), [])

    def test_explicit_false_is_rejected(self):
        self.fixture.mutate("ta001", "PSO", "feasible", "False")
        errors = validate(self.raw, runs=1, seed_base=2026)
        self.assertTrue(any("infeasible" in error for error in errors), errors)

    def test_noninteger_or_nonfinite_fe_is_rejected(self):
        for value in (20000.5, float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                self.fixture.mutate("ta001", "PSO", "n_fes", str(value))
                errors = validate(self.raw, runs=1, seed_base=2026)
                self.assertTrue(any("n_fes is not an integer" in e for e in errors), errors)

    def test_invalid_history_fe_is_rejected(self):
        for history in ([20000.5], [0.5, 20000], [float("nan"), 20000],
                        [float("inf"), 20000], [True, 20000]):
            with self.subTest(history=history):
                self.fixture.mutate("ta001", "PSO", "history_fes", json.dumps(history))
                best_f = valid_row("ta001")["best_f"]
                self.fixture.mutate("ta001", "PSO", "history_f", json.dumps([best_f] * len(history)))
                errors = validate(self.raw, runs=1, seed_base=2026)
                self.assertTrue(any("history_fes" in e for e in errors), errors)

    def test_objective_and_cmax_corruption_are_rejected(self):
        self.fixture.mutate("ta001", "DE", "objective", 999999)
        self.fixture.mutate("ta011", "DBO", "cmax", 999999)
        errors = validate(self.raw, runs=1, seed_base=2026)
        self.assertTrue(any("objective mismatch" in error for error in errors), errors)
        self.assertTrue(any("cmax mismatch" in error for error in errors), errors)

    def test_rpd_corruption_is_rejected(self):
        self.fixture.mutate("ta021", "RIME", "rpd", 12.345)
        errors = validate(self.raw, runs=1, seed_base=2026)
        self.assertTrue(any("rpd mismatch" in error for error in errors), errors)

    def test_permutation_corruption_is_rejected(self):
        self.fixture.mutate("ta001", "NRBO", "permutation", " ".join(map(str, range(20, 0, -1))))
        errors = validate(self.raw, runs=1, seed_base=2026)
        self.assertTrue(any("permutation mismatch" in error for error in errors), errors)

    def test_nonzero_violation_is_rejected(self):
        self.fixture.mutate("ta011", "PSO", "violation", 1.0)
        errors = validate(self.raw, runs=1, seed_base=2026)
        self.assertTrue(any("violation=" in error for error in errors), errors)

    def test_boolean_parser_is_strict(self):
        self.assertTrue(_parse_bool(True))
        self.assertTrue(_parse_bool("true"))
        self.assertFalse(_parse_bool(False))
        self.assertFalse(_parse_bool("False"))
        self.assertFalse(_parse_bool(0))
        self.assertTrue(_parse_bool(1))
        for invalid in ("yes", "no", "", 2, -1, None):
            with self.subTest(value=invalid):
                with self.assertRaises(ValueError):
                    _parse_bool(invalid)


if __name__ == "__main__":
    unittest.main(verbosity=2)
