"""Task 6 independent PFSP algorithm audit."""
import hashlib
import importlib
import importlib.util
import inspect
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

import numpy as np

from test_problem import ROOT, Problem, SMALL_P, SMALL_PERM, independent_makespan


ALGORITHM_NAMES = ("PSO", "DE", "DBO", "NRBO", "RIME")
FIELDS = {"best_x", "best_f", "history", "n_fes", "time"}
SEEDS = (2026, 2027)
BUDGETS = (7, 73, 121)


class CountedProblem:
    """Expose only the course API and independently score every candidate."""

    def __init__(self, matrix, budget, checks):
        self.matrix = matrix
        self.dim = len(matrix)
        self.lb = np.zeros(self.dim)
        self.ub = np.ones(self.dim)
        self.budget = budget
        self.checks = checks
        self.candidates = []
        self.permutations = set()
        self.scores = []

    def evaluate(self, x):
        self.checks.assertLess(len(self.scores), self.budget, "FE budget exceeded")
        candidate = np.asarray(x, dtype=float)
        self.checks.assertEqual(candidate.shape, (self.dim,))
        self.checks.assertTrue(np.isfinite(candidate).all(), "nonfinite candidate")
        self.checks.assertTrue(np.all((self.lb <= candidate) & (candidate <= self.ub)),
                               "candidate outside declared bounds")
        keys = tuple(candidate.tolist())
        order = tuple(sorted(range(self.dim), key=keys.__getitem__))
        score = independent_makespan(self.matrix, order)
        self.candidates.append(keys)
        self.permutations.add(order)
        self.scores.append(score)
        return float(score)


def benchmark_bytes(path):
    """Use LF only for diagnostics and only if it restores the recorded digest."""
    raw = path.read_bytes()
    metadata = json.loads((path.parent / "reference_solutions.json").read_text(encoding="utf-8"))
    expected = metadata["instances"][path.stem]["sha256"]
    normalized = raw.replace(b"\r\n", b"\n")
    if hashlib.sha256(raw).hexdigest() == expected:
        return raw
    if hashlib.sha256(normalized).hexdigest() != expected:
        raise ValueError(f"Benchmark content does not match recorded SHA-256: {path.name}")
    return normalized

def problem_matrix(instance):
    if instance == "5x3":
        return SMALL_P.copy()
    path = ROOT / "data" / "taillard" / f"{instance}.txt"
    raw = benchmark_bytes(path)
    return np.array([[int(value) for value in line.split()]
                     for line in raw.decode("utf-8").splitlines()[1:]])


def audit_run(checks, algorithm, params, matrix, budget, seed):
    problem = CountedProblem(matrix, budget, checks)
    inspect.signature(algorithm).bind(problem=problem, max_fes=budget, seed=seed, **params)
    result = algorithm(problem=problem, max_fes=budget, seed=seed, **params)
    checks.assertIsInstance(result, dict)
    checks.assertTrue(FIELDS.issubset(result))
    checks.assertEqual(len(problem.scores), budget)
    checks.assertIsInstance(result["n_fes"], (int, np.integer))
    checks.assertEqual(result["n_fes"], budget)
    checks.assertTrue(np.isfinite(result["time"]))
    checks.assertGreaterEqual(result["time"], 0)
    best = np.asarray(result["best_x"])
    checks.assertEqual(best.shape, (problem.dim,))
    checks.assertTrue(np.isfinite(best).all())
    keys = tuple(best.tolist())
    checks.assertIn(keys, problem.candidates)
    order = tuple(sorted(range(problem.dim), key=keys.__getitem__))
    checks.assertCountEqual(order, range(problem.dim))
    checks.assertTrue(np.isfinite(result["best_f"]))
    checks.assertEqual(result["best_f"], independent_makespan(matrix, order))
    checks.assertEqual(result["best_f"], min(problem.scores))

    history = result["history"]
    checks.assertGreaterEqual(len(history), 2)
    running_best = np.minimum.accumulate(problem.scores)
    previous_fe = 0
    for fe, value in history:
        checks.assertIsInstance(fe, (int, np.integer))
        checks.assertGreater(fe, previous_fe)
        checks.assertLessEqual(fe, budget)
        checks.assertTrue(np.isfinite(value))
        checks.assertEqual(value, running_best[fe - 1])
        previous_fe = fe
    checks.assertEqual(tuple(history[-1]), (budget, result["best_f"]))
    return problem, (keys, order, result["best_f"], history)


def worker(name):
    from main import ALGORITHMS

    module = importlib.import_module(f"algorithms.{name.lower()}")
    default = getattr(module, name.lower())
    algorithm, params = ALGORITHMS.get(name, (default, {}))
    checks = unittest.TestCase()
    summaries = []
    for instance in ("5x3", "ta001"):
        matrix = problem_matrix(instance)
        for budget in BUDGETS:
            try:
                first, result = audit_run(checks, algorithm, params, matrix, budget, SEEDS[0])
                second, repeated = audit_run(checks, algorithm, params, matrix, budget, SEEDS[0])
                other, _ = audit_run(checks, algorithm, params, matrix, budget, SEEDS[1])
                checks.assertEqual(first.candidates, second.candidates)
                checks.assertEqual(result, repeated)
                checks.assertNotEqual(first.candidates, other.candidates)
            except Exception as error:
                raise RuntimeError(f"{name}, {instance}, budget={budget}") from error
            ends = sum(key in (0.0, 1.0) for row in first.candidates for key in row)
            summaries.append({
                "instance": instance, "fe": budget, "cmax": float(result[2]),
                "boundary_keys": ends, "total_keys": budget * len(matrix),
                "unique_permutations": len(first.permutations),
                "tied_candidates": sum(len(set(row)) < len(row) for row in first.candidates),
            })
    print(json.dumps(summaries))


class TestAuditBurakTask6(unittest.TestCase):
    def check_algorithm(self, name):
        if importlib.util.find_spec(f"algorithms.{name.lower()}") is None:
            self.skipTest(f"BLOKE: algorithms/{name.lower()}.py is missing")
        completed = subprocess.run(
            [sys.executable, "-B", str(Path(__file__).resolve()), "--audit-worker", name],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        summaries = json.loads(completed.stdout)
        self.assertEqual(len(summaries), 2 * len(BUDGETS))

    def test_pso_fe_seed_and_results(self):
        self.check_algorithm("PSO")

    def test_de_fe_seed_and_results(self):
        self.check_algorithm("DE")

    def test_dbo_fe_seed_and_results(self):
        self.check_algorithm("DBO")

    def test_nrbo_fe_seed_and_results(self):
        self.check_algorithm("NRBO")

    def test_rime_fe_seed_and_results(self):
        self.check_algorithm("RIME")

    def test_five_algorithms_are_registered(self):
        from main import ALGORITHMS

        missing = sorted(set(ALGORITHM_NAMES) - ALGORITHMS.keys())
        if missing:
            self.skipTest(f"BLOKE: missing main.py registrations: {', '.join(missing)}")
        self.assertCountEqual(ALGORITHMS, ALGORITHM_NAMES)
        for name, (algorithm, params) in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                inspect.signature(algorithm).bind(problem=None, max_fes=7, seed=2026, **params)

    def test_model_reference_and_boundary_ties(self):
        self.assertEqual(independent_makespan(SMALL_P, SMALL_PERM), 20)
        path = ROOT / "data" / "taillard" / "ta001.txt"
        model_bytes = benchmark_bytes(path)
        real_read_bytes = Path.read_bytes
        with patch.object(Path, "read_bytes",
                          lambda p: model_bytes if p == path else real_read_bytes(p)):
            model = Problem("ta001")
        keys = np.tile([1.2, -0.2, 0.4, 1.0, 0.0], 4)
        expected_keys = np.tile([1.0, 0.0, 0.4, 1.0, 0.0], 4)
        expected_order = sorted(range(model.dim), key=expected_keys.__getitem__)
        np.testing.assert_array_equal(model.clip(keys), expected_keys)
        np.testing.assert_array_equal(model.decode(expected_keys), expected_order)
        self.assertEqual(model.evaluate(keys),
                         independent_makespan(model.processing_times, expected_order))
        self.assertEqual(model.objective(model.reference_permutation), 1278)
        self.assertEqual(independent_makespan(model.processing_times,
                                              model.reference_permutation), 1278)


class FormulaProblem:
    dim = 2
    lb = np.zeros(dim)
    ub = np.ones(dim)

    def __init__(self, scores):
        self.scores = iter(scores)
        self.candidates = []

    def evaluate(self, x):
        self.candidates.append(np.array(x, copy=True))
        return next(self.scores)


def scripted_rng(uniform, normal, *, angles=(), indices=()):
    rng = Mock()
    rng.random.side_effect = uniform
    rng.standard_normal.side_effect = normal
    rng.integers.side_effect = angles
    rng.choice.side_effect = indices
    return rng


class TestAuthorCodeFormulas(unittest.TestCase):
    def test_dbo_all_roles_and_previous_position(self):
        for angle in (45, 90, 180):
            with self.subTest(angle=angle):
                self.check_dbo(angle)

    def check_dbo(self, angle):
        from algorithms.dbo import dbo

        initial = np.array([[.2, .3], [.4, .5], [.6, .7], [.7, .8]])
        # Draws correspond to MATLAB (1), (4), (6), (7), and (2).
        b1, b2, c2, g = (np.array(v) for v in
                         ([.1, .2], [.3, .4], [.5, .6], [-.25, .25]))
        rng = scripted_rng([initial, .2, .05, b1, b2, c2, .95],
                           [-.25, g], angles=[angle])
        problem = FormulaProblem([1, 2, 3, 4, 0, 5, 6, 7, 8])
        with patch("algorithms.dbo.np.random.default_rng", return_value=rng):
            dbo(problem, 9, 2026, pop_size=4)

        rolled = np.array([.33, .42])
        # The Python adaptation measures R after the first rolling FE.
        radius = 4 / 9
        lo, hi = rolled * (1 - radius), rolled * (1 + radius)
        brood = np.clip(rolled + b1 * (initial[1] - lo) + b2 * (initial[1] - hi), lo, hi)
        global_best = initial[0]
        lo, hi = global_best * (1 - radius), global_best * (1 + radius)
        forager = initial[2] - .25 * (initial[2] - lo) + c2 * (initial[2] - hi)
        thief = global_best + .5 * g * (
            np.abs(initial[3] - rolled) + np.abs(initial[3] - global_best)
        )
        dance = rolled + [0.13, 0.12] if angle == 45 else rolled
        np.testing.assert_allclose(problem.candidates[4:], [rolled, brood, forager, thief, dance],
                                   rtol=0, atol=1e-12)
        self.assertEqual(rng.standard_normal.call_args_list, [call(), call(2)])
        rng.integers.assert_called_once_with(1, 181)

    def test_nrbo_nrsr_and_tao_branches(self):
        for branch in ("no_tao", "update_base", "best_base"):
            with self.subTest(branch=branch):
                self.check_nrbo(branch)

    def check_nrbo(self, branch):
        from algorithms.nrbo import nrbo

        initial = np.array([[.31, .36], [.22, .18], [.52, .71]])
        x, best, worst = initial
        draw, a1, a2 = np.array([.2, .3]), np.array([.7, .6]), np.array([.55, .45])
        uniform = [initial, .3, .15, draw, .3, .6, a1, a2]
        uniform.append(.8 if branch == "no_tao" else .2)
        if branch != "no_tao":
            uniform.extend([.65, .25, .1 if branch == "update_base" else .9, .1, .4])
        rng = scripted_rng(uniform, [.5, -.4], indices=[np.array([1, 2])])
        problem = FormulaProblem([2, 1, 3, 4])
        with patch("algorithms.nrbo.np.random.default_rng", return_value=rng):
            nrbo(problem, 4, 2026, pop_size=3)

        rho = .3 * (best - x) + .15 * (best - worst)
        d = [draw[j] * abs(best[j] - x[j]) for j in range(2)]
        first = [.5 * (best[j] - worst[j]) * d[j] / (2 * (best[j] + worst[j] - 2 * x[j]))
                 for j in range(2)]
        mean = sum(2 * x[j] - first[j] + rho[j] for j in range(2)) / 2
        expected = []
        for j in range(2):
            yp, yq = .3 * (mean + .3 * d[j]), .6 * (mean - .6 * d[j])
            step = -.4 * (yp - yq) * d[j] / (2 * (yp + yq - 2 * x[j]))
            x1, x2 = x[j] - step + rho[j], best[j] - step + rho[j]
            delta = -.03125  # (1 - 2 * 3 / 4)**5
            x3 = x[j] - delta * (x2 - x1)
            value = a1[j] * (a1[j] * x1 + (1 - a2[j]) * x2) + (1 - a2[j]) * x3
            if branch != "no_tao":
                u1, u2, base = (.3, .4, value) if branch == "update_base" else (1, 1, best[j])
                value = (base + .3 * (u1 * best[j] - u2 * x[j])
                         - .25 * delta * (u1 * sum(initial[:, j]) / 3 - u2 * x[j]))
            expected.append(min(1, max(0, value)))
        np.testing.assert_allclose(problem.candidates[-1], expected, rtol=0, atol=1e-12)
        rng.choice.assert_called_once_with(3, size=2, replace=False)

    def test_nrbo_singular_rule_is_bounded_before_evaluation(self):
        from algorithms.nrbo import nrbo

        initial = np.full((2, 2), .5)
        rng = scripted_rng([initial, .2, .2, np.full(2, .3), .2, .2, np.full(2, .3), np.full(2, .4), .9],
                           [1, 1], indices=[np.array([0, 1])])
        problem = FormulaProblem([1, 1, 1])
        with patch("algorithms.nrbo.np.random.default_rng", return_value=rng):
            nrbo(problem, 3, 2026, pop_size=2)
        np.testing.assert_array_equal(problem.candidates[-1], [0, 0])

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--audit-worker":
        worker(sys.argv[2])
    else:
        unittest.main(verbosity=2)
