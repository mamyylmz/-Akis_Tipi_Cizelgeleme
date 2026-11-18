# -*- coding: utf-8 -*-
"""PFSP problem model for YMM4142 Problem 7.

Objective: minimize makespan (Cmax) for a common job permutation on all machines.
Continuous optimizers use random keys x in [0, 1]^n; stable argsort decodes x to
an integer permutation. The problem has no additional feasibility constraints.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "taillard"
REFERENCE_FILE = DATA_DIR / "reference_solutions.json"

# Kept for API compatibility with the course template. PFSP constraints() is empty,
# therefore this multiplier never changes the fitness value.
PENALTY = 1e6
FEASIBILITY_TOL = 1e-6

INSTANCES = ["ta001", "ta011", "ta021"]
MAX_FES = {"ta001": 20_000, "ta011": 30_000, "ta021": 40_000}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_reference_metadata() -> dict:
    if not REFERENCE_FILE.exists():
        raise FileNotFoundError(f"Reference metadata not found: {REFERENCE_FILE}")
    return json.loads(REFERENCE_FILE.read_text(encoding="utf-8"))


class Problem:
    """Permutation Flow Shop Scheduling Problem (PFSP) with Cmax objective."""

    def __init__(self, instance: str):
        if instance not in INSTANCES:
            raise ValueError(f"Unknown PFSP instance: {instance!r}; expected one of {INSTANCES}")
        self.name = instance
        self.data = self._load_data(instance)
        self.processing_times = self.data["processing_times"]
        self.n_jobs = int(self.processing_times.shape[0])
        self.n_machines = int(self.processing_times.shape[1])
        self.dim = self.n_jobs

        # Random-key search space. Every vector in this box decodes to a valid
        # permutation; ties are resolved deterministically with stable argsort.
        self.lb = np.zeros(self.dim, dtype=float)
        self.ub = np.ones(self.dim, dtype=float)
        self.reference_value = int(self.data["bks"])
        self.reference_permutation = np.asarray(
            self.data["reference_permutation_0_based"], dtype=int
        )

    def _load_data(self, instance: str) -> dict:
        path = DATA_DIR / f"{instance}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Taillard instance file not found: {path}")

        meta = _load_reference_metadata()["instances"][instance]
        raw = path.read_bytes()
        observed_hash = _sha256(raw)
        expected_hash = meta.get("sha256")
        if not expected_hash:
            raise ValueError(f"{instance}: SHA-256 missing in reference metadata")
        if observed_hash != expected_hash:
            raise ValueError(
                f"SHA-256 mismatch for {instance}: expected {expected_hash}, got {observed_hash}"
            )

        lines = [line.strip() for line in raw.decode("utf-8").splitlines() if line.strip()]
        if not lines:
            raise ValueError(f"Empty instance file: {path}")
        try:
            n_jobs, n_machines = (int(v) for v in lines[0].split())
        except Exception as exc:
            raise ValueError(f"Invalid header in {path}; expected '<jobs> <machines>'") from exc

        if len(lines[1:]) != n_jobs:
            raise ValueError(
                f"{instance}: expected {n_jobs} job rows, found {len(lines[1:])}"
            )
        matrix = []
        for row_no, line in enumerate(lines[1:], start=1):
            row = [int(v) for v in line.split()]
            if len(row) != n_machines:
                raise ValueError(
                    f"{instance}: row {row_no} has {len(row)} values; expected {n_machines}"
                )
            matrix.append(row)

        p = np.asarray(matrix, dtype=np.int64)
        if np.any((p < 1) | (p > 99)):
            raise ValueError(f"{instance}: processing times must be integers in [1, 99]")
        if (n_jobs, n_machines) != (meta["jobs"], meta["machines"]):
            raise ValueError(
                f"{instance}: dimensions disagree with metadata: "
                f"file={(n_jobs, n_machines)}, metadata={(meta['jobs'], meta['machines'])}"
            )
        perm = np.asarray(meta["reference_permutation_0_based"], dtype=int)
        if sorted(perm.tolist()) != list(range(n_jobs)):
            raise ValueError(f"{instance}: invalid reference permutation in metadata")

        return {
            "processing_times": p,
            "jobs": n_jobs,
            "machines": n_machines,
            "seed": int(meta["seed"]),
            "bks": int(meta["bks"]),
            "sha256": observed_hash,
            "reference_permutation_0_based": perm.tolist(),
        }

    def decode(self, x: np.ndarray) -> np.ndarray:
        """Decode continuous random keys to a deterministic job permutation."""
        arr = np.asarray(x, dtype=float)
        if arr.shape != (self.dim,):
            raise ValueError(f"x must have shape ({self.dim},), got {arr.shape}")
        if not np.all(np.isfinite(arr)):
            raise ValueError("x contains NaN or infinity")
        return np.argsort(arr, kind="stable").astype(np.int64)

    def _validate_permutation(self, permutation: np.ndarray) -> np.ndarray:
        arr = np.asarray(permutation)
        if arr.shape != (self.n_jobs,):
            raise ValueError(
                f"permutation must contain {self.n_jobs} jobs, got shape {arr.shape}"
            )
        if not np.issubdtype(arr.dtype, np.integer):
            if not np.all(np.equal(arr, np.floor(arr))):
                raise ValueError("permutation contains non-integer values")
        arr = arr.astype(np.int64, copy=False)
        if np.any((arr < 0) | (arr >= self.n_jobs)):
            raise ValueError("permutation contains out-of-range job indices")
        if np.unique(arr).size != self.n_jobs:
            raise ValueError("permutation contains duplicate or missing jobs")
        return arr

    def objective(self, z: np.ndarray) -> float:
        """Compute Cmax for a decoded job permutation using O(n*m) DP."""
        permutation = self._validate_permutation(z)
        completion = np.zeros(self.n_machines, dtype=np.int64)
        p = self.processing_times
        for job in permutation:
            completion[0] += p[job, 0]
            for machine in range(1, self.n_machines):
                completion[machine] = (
                    max(completion[machine], completion[machine - 1])
                    + p[job, machine]
                )
        return float(completion[-1])

    def constraints(self, z: np.ndarray) -> np.ndarray:
        # Random-key decoding always yields a complete permutation; no extra
        # penalty constraints are needed for this PFSP formulation.
        self._validate_permutation(z)
        return np.zeros(0, dtype=float)

    def evaluate(self, x: np.ndarray) -> float:
        z = self.decode(self.clip(x))
        return self.objective(z)

    def details(self, x: np.ndarray) -> dict:
        z = self.decode(self.clip(x))
        cmax = self.objective(z)
        rpd = 100.0 * (cmax - self.reference_value) / self.reference_value
        return {
            "objective": cmax,
            "cmax": cmax,
            "rpd": float(rpd),
            "violation": 0.0,
            "feasible": True,
            "permutation": " ".join(str(int(v) + 1) for v in z),
        }

    def clip(self, x: np.ndarray) -> np.ndarray:
        arr = np.asarray(x, dtype=float)
        if arr.shape != (self.dim,):
            raise ValueError(f"x must have shape ({self.dim},), got {arr.shape}")
        return np.clip(arr, self.lb, self.ub)

    def encode_permutation(self, permutation: np.ndarray) -> np.ndarray:
        """Return random keys that decode exactly to the given permutation.

        This helper is for validation/reproducibility, not an optimization step.
        """
        perm = self._validate_permutation(permutation)
        x = np.empty(self.n_jobs, dtype=float)
        x[perm] = np.arange(self.n_jobs, dtype=float) / max(1, self.n_jobs - 1)
        return x


if __name__ == "__main__":
    print("PFSP model verification")
    failures = 0
    for name in INSTANCES:
        p = Problem(name)
        x_ref = p.encode_permutation(p.reference_permutation)
        d = p.details(x_ref)
        ok = d["cmax"] == float(p.reference_value)
        print(
            f"{name}: {p.n_jobs}x{p.n_machines}, "
            f"Cmax={d['cmax']:.0f}, reference={p.reference_value}, "
            f"RPD={d['rpd']:.6f}% -> {'PASS' if ok else 'FAIL'}"
        )
        failures += 0 if ok else 1
    raise SystemExit(1 if failures else 0)
