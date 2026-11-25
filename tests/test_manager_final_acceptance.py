"""Independent manager acceptance checks for immutable PFSP final evidence.

This test does not run stochastic optimization again. It validates recorded
outputs and reconstruction invariants without editing the scientific dataset.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from main import ALGORITHMS, FINAL_ALGORITHMS  # noqa: E402
from check_experiment_outputs import validate  # noqa: E402
from verify_final_schedule import verify  # noqa: E402


class TestManagerFinalAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "results/tables/experiment_manifest.json").read_text(encoding="utf-8"))
        cls.proof = json.loads((ROOT / "results/verification.json").read_text(encoding="utf-8"))

    def test_freeze_provenance_and_effective_parameters(self):
        m, proof = self.manifest, self.proof
        self.assertEqual(m, proof["manifest"])
        self.assertEqual(m["experiment_commit"], "73ce39c78a6263ce6f252267edeff0515157aca1")
        self.assertEqual(proof["sha"], m["experiment_commit"])
        self.assertIs(m["git_dirty_at_start"], False)
        self.assertEqual((m["n_runs"], m["seed_base"]), (30, 2026))
        self.assertEqual(set(m["algorithms"]), set(FINAL_ALGORITHMS))
        self.assertEqual(m["algorithm_parameters"], {name: params for name, (_, params) in ALGORITHMS.items()})
        self.assertEqual(m["max_fes"], {"ta001": 20000, "ta011": 30000, "ta021": 40000})
        self.assertEqual((proof["csv"], proof["runs"], proof["fes"]), (15, 450, 13500000))
        self.assertEqual(m["algorithm_parameters"]["RIME"], {"pop_size": 30, "w": 5})

    def test_raw_csv_hashes_and_exact_run_matrix(self):
        expected_paths = {
            f"raw/{instance}/{algorithm}.csv"
            for instance in ("ta001", "ta011", "ta021")
            for algorithm in FINAL_ALGORITHMS
        }
        self.assertEqual(set(self.proof["raw_sha256"]), expected_paths)
        total_fe = 0
        for rel in sorted(expected_paths):
            path = ROOT / "results" / rel
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             self.proof["raw_sha256"][rel], rel)
            with path.open("r", encoding="utf-8", newline="") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), 30, rel)
            self.assertEqual([int(row["seed"]) for row in rows], list(range(2026, 2056)), rel)
            self.assertEqual([int(row["run"]) for row in rows], list(range(1, 31)), rel)
            expected_fe = self.manifest["max_fes"][rel.split("/")[1]]
            for row in rows:
                self.assertEqual(int(row["n_fes"]), expected_fe, rel)
                total_fe += expected_fe
        self.assertEqual(total_fe, 13_500_000)

    def test_complete_validator_recomputes_all_final_objectives(self):
        errors = validate(ROOT / "results/raw", runs=30, seed_base=2026)
        self.assertEqual(errors, [], "\n".join(errors[:20]))

    def test_independent_cmax_and_gantt_source_for_all_winners(self):
        for instance in ("ta001", "ta011", "ta021"):
            rows = []
            for algorithm in FINAL_ALGORITHMS:
                with (ROOT / f"results/raw/{instance}/{algorithm}.csv").open(
                    encoding="utf-8", newline=""
                ) as fh:
                    rows.extend(csv.DictReader(fh))
            minimum = min(int(float(row["cmax"])) for row in rows)
            winners = [row for row in rows if int(float(row["cmax"])) == minimum]
            self.assertTrue(winners)
            for row in winners:
                result = verify(instance, row["permutation"].split(), minimum)
                self.assertEqual(result["cmax"], minimum)
            times_path = ROOT / f"paper/support/schedule_{instance}.csv"
            with times_path.open(encoding="utf-8", newline="") as fh:
                schedule = list(csv.DictReader(fh))
            n_machines = {"ta001": 5, "ta011": 10, "ta021": 20}[instance]
            self.assertEqual(len(schedule), 20 * n_machines)
            first_perm = [int(schedule[pos * n_machines]["job"]) for pos in range(20)]
            result = verify(instance, first_perm, minimum)
            for i, record in enumerate(schedule):
                pos, machine = divmod(i, n_machines)
                self.assertEqual(int(record["start"]), int(result["start"][pos, machine]))
                self.assertEqual(int(record["finish"]), int(result["finish"][pos, machine]))


if __name__ == "__main__":
    unittest.main()
