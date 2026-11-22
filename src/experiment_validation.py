"""Provenance and validation for experiment artifacts."""
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np

from problem import DATA_DIR, INSTANCES, MAX_FES, Problem


def git_revision(root):
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def expected_manifest(root, algorithms, runs, seed_base, alpha):
    return {
        "schema_version": 1,
        "commit": git_revision(root),
        "source_sha256": {
            path.relative_to(root).as_posix(): hashlib.sha256(
                path.read_bytes().replace(b"\r\n", b"\n")
            ).hexdigest()
            for path in sorted((root / "src").rglob("*.py"))
        },
        "data_sha256": {
            name: hashlib.sha256((DATA_DIR / f"{name}.txt").read_bytes()).hexdigest()
            for name in INSTANCES
        },
        "algorithms": {name: params for name, (_, params) in algorithms.items()},
        "runs": runs,
        "alpha": alpha,
        "seeds": list(range(seed_base, seed_base + runs)),
        "max_fes": MAX_FES,
        "files": sorted(f"{name}/{algorithm}.csv"
                        for name in INSTANCES for algorithm in algorithms),
    }


def read_manifest(path, root, algorithms, seed_base, alpha):
    manifest = json.loads(path.read_text(encoding="utf-8"))
    runs = manifest.get("runs")
    if type(runs) is not int or runs < 1:
        raise ValueError("Invalid manifest run count")
    expected = expected_manifest(root, algorithms, runs, seed_base, alpha)
    for field, value in expected.items():
        if manifest.get(field) != value:
            raise ValueError(f"Experiment manifest mismatch: {field}")
    return manifest


def independent_cmax(matrix, order):
    completion = [[0] * (matrix.shape[1] + 1) for _ in range(len(order) + 1)]
    for i, job in enumerate(order, 1):
        for j, duration in enumerate(matrix[job], 1):
            completion[i][j] = max(completion[i-1][j], completion[i][j-1]) + int(duration)
    return completion[-1][-1]


def validate_row(row, problem, budget, run, seed):
    if (int(row["run"]), int(row["seed"]), int(row["n_fes"])) != (run, seed, budget):
        raise ValueError("run, seed or evaluation budget mismatch")
    keys = np.asarray(json.loads(row["best_x"]), dtype=float)
    if keys.shape != (problem.dim,) or not np.all(np.isfinite(keys) & (keys >= 0) & (keys <= 1)):
        raise ValueError("invalid random keys")
    order = sorted(range(problem.dim), key=keys.__getitem__)
    score = independent_cmax(problem.processing_times, order)
    if ([int(job) - 1 for job in row["permutation"].split()] != order
            or any(float(row[key]) != score for key in ("best_f", "cmax", "objective"))):
        raise ValueError("permutation or objective mismatch")
    elapsed = float(row["time"])
    rpd = 100 * (score - problem.reference_value) / problem.reference_value
    if (row["feasible"] != "True" or float(row["violation"]) != 0
            or not math.isfinite(elapsed) or elapsed < 0
            or not math.isclose(float(row["rpd"]), rpd, abs_tol=1e-12)):
        raise ValueError("invalid run details")
    fes = json.loads(row["history_fes"])
    values = json.loads(row["history_f"])
    if (len(fes) != len(values) or len(fes) < 2
            or any(type(fe) is not int or fe < 1 for fe in fes)
            or any(a >= b for a, b in zip(fes, fes[1:]))
            or fes[-1] != budget or values[-1] != score
            or any(not math.isfinite(value) for value in values)
            or any(a < b for a, b in zip(values, values[1:]))):
        raise ValueError("invalid convergence history")


def validate_results(raw_dir, manifest):
    actual = {path.relative_to(raw_dir).as_posix() for path in raw_dir.rglob("*.csv")}
    files = set(manifest["files"])
    if actual != files:
        raise ValueError(f"CSV coverage mismatch: missing={sorted(files-actual)}, extra={sorted(actual-files)}")
    for name, budget in manifest["max_fes"].items():
        problem = Problem(name)
        for algorithm in manifest["algorithms"]:
            path = Path(raw_dir) / name / f"{algorithm}.csv"
            with path.open(encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream)
                if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
                    raise ValueError(f"{path}: invalid CSV header")
                rows = list(reader)
            if len(rows) != manifest["runs"]:
                raise ValueError(f"{path}: incorrect row count")
            for run, (row, seed) in enumerate(zip(rows, manifest["seeds"]), 1):
                try:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("CSV row does not match header")
                    validate_row(row, problem, budget, run, seed)
                except (ValueError, TypeError, KeyError, OverflowError) as error:
                    raise ValueError(f"{path}:{run + 1}: {error}") from error
