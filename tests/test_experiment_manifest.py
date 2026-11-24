from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import main  # noqa: E402


class TestExperimentManifest(unittest.TestCase):
    def test_manifest_contains_reproducibility_fields(self):
        provenance = {"commit": "a" * 40, "dirty": False}
        with patch.object(main, "_git_provenance", return_value=provenance):
            manifest = main._build_experiment_manifest(3)

        self.assertEqual(manifest["experiment_commit"], "a" * 40)
        self.assertFalse(manifest["git_dirty_at_start"])
        self.assertEqual(manifest["n_runs"], 3)
        self.assertEqual(manifest["seed_base"], 2026)
        self.assertEqual(manifest["instances"], ["ta001", "ta011", "ta021"])
        self.assertEqual(
            manifest["max_fes"],
            {"ta001": 20_000, "ta011": 30_000, "ta021": 40_000},
        )
        self.assertEqual(set(manifest["algorithms"]), {"PSO", "DE", "DBO", "RIME", "NRBO"})
        self.assertEqual(set(manifest["algorithm_parameters"]), set(manifest["algorithms"]))
        for key in ("os", "python", "numpy", "scipy", "pandas"):
            self.assertTrue(manifest["environment"][key])

    def test_save_settings_writes_manifest_automatically(self):
        provenance = {"commit": "c" * 40, "dirty": False}
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(main, "TAB_DIR", Path(tmp)):
                with patch.object(main, "_git_provenance", return_value=provenance):
                    manifest = main._build_experiment_manifest(3)
                    main._save_settings(3, manifest)
            saved = json.loads((Path(tmp) / "experiment_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(saved, manifest)
            self.assertEqual(saved["algorithm_parameters"], {
                "PSO": {"pop_size": 30, "w_max": 0.9, "w_min": 0.4,
                        "c1": 2.0, "c2": 2.0, "v_frac": 0.2},
                "DE": {"pop_size": 100, "F": 0.5, "CR": 0.9},
                "DBO": {"pop_size": 30, "k": 0.1, "b": 0.3, "S": 0.5,
                        "roll_prob": 0.9, "deviation_prob": 0.1},
                "RIME": {"pop_size": 30, "w": 5},
                "NRBO": {"pop_size": 30, "DF": 0.6},
            })
            self.assertTrue((Path(tmp) / "parametre_ayarlari.csv").exists())
            self.assertTrue((Path(tmp) / "deney_ayarlari.json").exists())

    def test_final_run_requires_clean_git_and_exact_five_algorithms(self):
        good = {
            "experiment_commit": "b" * 40,
            "git_dirty_at_start": False,
        }
        main._validate_final_experiment_preconditions(main.N_RUNS, good)

        dirty = dict(good, git_dirty_at_start=True)
        with self.assertRaises(main.KontrolHatasi):
            main._validate_final_experiment_preconditions(main.N_RUNS, dirty)

        missing_commit = dict(good, experiment_commit=None)
        with self.assertRaises(main.KontrolHatasi):
            main._validate_final_experiment_preconditions(main.N_RUNS, missing_commit)

    def test_pilot_does_not_require_clean_git(self):
        pilot = {"experiment_commit": None, "git_dirty_at_start": True}
        main._validate_final_experiment_preconditions(3, pilot)


if __name__ == "__main__":
    unittest.main(verbosity=2)
