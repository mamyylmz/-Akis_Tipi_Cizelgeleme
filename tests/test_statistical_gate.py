"""Regression for the project's conditional Friedman post-hoc step."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import main


class TestNemenyiGate(unittest.TestCase):
    def test_friedman_is_reported_and_nemenyi_requires_strict_significance(self):
        instance = "ta001"
        results = dict.fromkeys(main.FINAL_ALGORITHMS, object())
        ranks = pd.Series({name: rank for rank, name in enumerate(results, 1)})
        for p_value in (0.049, 0.05, 0.051, float("nan")):
            with self.subTest(p_value=p_value):
                friedman = {"statistic": 1.0, "p_value": p_value,
                            "mean_ranks": ranks, "k": 5, "n_blocks": 3}
                with (patch.object(main, "INSTANCES", [instance]),
                      patch.object(Path, "mkdir"),
                      patch.object(main.st, "load_results", return_value=results),
                      patch.object(main.st, "descriptive_table", return_value=pd.DataFrame()),
                      patch.object(main.st, "wilcoxon_table", return_value=pd.DataFrame()),
                      patch.object(main.st, "friedman_test", return_value=friedman) as test,
                      patch.object(main.st, "friedman_table", return_value=pd.DataFrame()) as table,
                      patch.object(pd.DataFrame, "to_csv") as write_csv,
                      patch.object(main.st, "nemenyi_cd", return_value=1.25) as cd,
                      patch.object(main.vz, "plot_convergence"),
                      patch.object(main.vz, "plot_boxplot"),
                      patch.object(main.vz, "plot_cd_diagram") as plot,
                      patch("builtins.print")):
                    main.run_analysis()
                test.assert_called_once_with(results)
                table.assert_called_once_with(friedman)
                self.assertIn(main.TAB_DIR / f"{instance}_friedman.csv",
                              [call.args[0] for call in write_csv.call_args_list])
                if p_value < 0.05:
                    cd.assert_called_once_with(5, 3, alpha=0.05)
                    plot.assert_called_once_with(ranks, 1.25, instance, out_dir=main.FIG_DIR)
                else:
                    cd.assert_not_called()
                    plot.assert_not_called()
