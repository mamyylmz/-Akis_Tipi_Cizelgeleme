"""Exploratory tie-sensitive two-sample Mann-Whitney check for recorded PFSP Cmax.

Does not rewrite published results, raw data or experiment manifest.
All p-values are descriptive sensitivity analyses, not confirmatory inference.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
INSTANCES = ("ta001", "ta011", "ta021")
ALGORITHMS = ("DBO", "DE", "NRBO", "PSO", "RIME")


def load_cmax(instance: str, algorithm: str) -> list[float]:
    path = ROOT / "results" / "raw" / instance / f"{algorithm}.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        values = [float(row["cmax"]) for row in csv.DictReader(stream)]
    if len(values) != 30 or not all(math.isfinite(v) for v in values):
        raise ValueError(f"Invalid recorded final results: {path}")
    return values


def tie_adjusted_rank_sum(x: list[float], y: list[float]) -> dict[str, float]:
    """Normal approximation, average ties, variance correction, no continuity fix.

    Independent-samples U is not interchangeable with paired Wilcoxon signed-rank.
    A reference selected by observed medians creates post-selection multiplicity.
    """
    n, m = len(x), len(y)
    if not n or not m:
        raise ValueError("Both samples must be nonempty")
    pooled = sorted([(v, 0) for v in x] + [(v, 1) for v in y])
    rank_sum_x = 0.0
    tie_term = 0
    idx = 0
    while idx < len(pooled):
        nxt = idx + 1
        while nxt < len(pooled) and pooled[nxt][0] == pooled[idx][0]:
            nxt += 1
        rank = (idx + 1 + nxt) / 2
        rank_sum_x += rank * sum(group == 0 for _, group in pooled[idx:nxt])
        size = nxt - idx
        tie_term += size**3 - size
        idx = nxt

    U = rank_sum_x - n * (n + 1) / 2
    N = n + m
    variance = (n * m / 12) * ((N + 1) - tie_term / (N * (N - 1)))
    if variance <= 0:
        return {"U": U, "z": 0.0, "p": 1.0}
    z = (U - n * m / 2) / math.sqrt(variance)
    p = math.erfc(abs(z) / math.sqrt(2))
    return {"U": U, "z": z, "p": p}


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    sorted_keys = sorted(pvalues, key=lambda key: (pvalues[key], key))
    adjusted: dict[str, float] = {}
    prior = 0.0
    for index, key in enumerate(sorted_keys):
        prior = max(prior, min(1.0, pvalues[key] * (len(sorted_keys) - index)))
        adjusted[key] = prior
    return adjusted


def main() -> None:
    results = {}
    for instance in INSTANCES:
        by_algorithm = {alg: load_cmax(instance, alg) for alg in ALGORITHMS}
        reference = min(ALGORITHMS, key=lambda alg: (median(by_algorithm[alg]), alg))
        comparisons = {
            alg: tie_adjusted_rank_sum(by_algorithm[reference], by_algorithm[alg])
            for alg in ALGORITHMS if alg != reference
        }
        corrected = holm_adjust({alg: comparison["p"] for alg, comparison in comparisons.items()})
        for alg, row in comparisons.items():
            row["holm_p"] = corrected[alg]
            row["exploratory_reject_0_05"] = corrected[alg] < 0.05
        results[instance] = {"reference": reference, "comparisons": comparisons}

    # Regression checks on the key sensitivity finding, not a substitution for paper inference.
    ta001 = results["ta001"]
    assert ta001["reference"] == "DBO"
    assert 0.003 < ta001["comparisons"]["DE"]["p"] < 0.004
    assert ta001["comparisons"]["DE"]["holm_p"] < 0.05
    assert ta001["comparisons"]["RIME"]["holm_p"] > 0.05
    print(json.dumps({"analysis": "exploratory_tie_corrected_mann_whitney", "continuity_correction": False,
                      "post_selection_reference": True, "results": results},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
