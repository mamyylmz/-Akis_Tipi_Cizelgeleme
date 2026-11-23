"""Independent final schedule/Cmax verifier tests."""
import json
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from verify_final_schedule import independent_schedule, load_matrix, verify  # noqa: E402


class TestFinalScheduleVerifier(unittest.TestCase):
    def test_small_hand_schedule(self):
        p = np.array([
            [3, 4, 2],
            [2, 3, 4],
            [4, 1, 3],
            [1, 4, 2],
            [3, 2, 3],
        ], dtype=np.int64)
        perm = np.array([3, 1, 0, 4, 2])
        start, finish = independent_schedule(p, perm)
        self.assertEqual(int(finish[-1, -1]), 20)
        self.assertTrue(np.all(start[1:, :] >= finish[:-1, :]))
        self.assertTrue(np.all(start[:, 1:] >= finish[:, :-1]))

    def test_three_reference_permutations(self):
        meta = json.loads(
            (ROOT / "data/taillard/reference_solutions.json").read_text(encoding="utf-8")
        )
        for name, record in meta["instances"].items():
            with self.subTest(instance=name):
                result = verify(
                    name,
                    record["reference_permutation_1_based"],
                    expected_cmax=record["bks"],
                )
                self.assertEqual(result["cmax"], record["bks"])
                self.assertEqual(result["finish"].shape, load_matrix(name).shape)

    def test_neh_baseline_permutations(self):
        expected = {
            "ta001": (1286, [3, 17, 9, 8, 15, 14, 11, 16, 13, 19, 6, 4, 5, 18, 1, 2, 10, 7, 20, 12]),
            "ta011": (1680, [18, 5, 2, 17, 3, 6, 12, 9, 15, 10, 20, 13, 8, 14, 19, 11, 4, 7, 1, 16]),
            "ta021": (2410, [16, 15, 10, 8, 9, 12, 13, 11, 5, 1, 20, 14, 17, 2, 18, 6, 7, 19, 3, 4]),
        }
        for name, (cmax, perm) in expected.items():
            with self.subTest(instance=name):
                result = verify(name, perm, expected_cmax=cmax)
                self.assertEqual(result["cmax"], cmax)
                self.assertTrue(np.all(result["start"][1:, :] >= result["finish"][:-1, :]))
                self.assertTrue(np.all(result["start"][:, 1:] >= result["finish"][:, :-1]))

    def test_rejects_wrong_expected_cmax(self):
        meta = json.loads(
            (ROOT / "data/taillard/reference_solutions.json").read_text(encoding="utf-8")
        )
        rec = meta["instances"]["ta001"]
        with self.assertRaisesRegex(ValueError, "Cmax mismatch"):
            verify("ta001", rec["reference_permutation_1_based"], rec["bks"] + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
