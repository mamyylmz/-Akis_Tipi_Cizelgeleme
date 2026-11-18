#!/usr/bin/env python3
"""Generate the three mandatory Taillard PFSP instances from original seeds.

Source algorithm and seeds:
https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/flowshop2.txt
The generator follows Taillard's Park-Miller RNG and loops machine-major,
then stores the project files job-major (one job per row).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

M = 2_147_483_647
A = 16_807
B = 127_773
C = 2_836

SPECS = {
    "ta001": {"seed": 873_654_221, "jobs": 20, "machines": 5, "bks": 1278},
    "ta011": {"seed": 587_595_453, "jobs": 20, "machines": 10, "bks": 1582},
    "ta021": {"seed": 479_340_445, "jobs": 20, "machines": 20, "bks": 2297},
}

REFERENCE_PERMUTATIONS_1_BASED = {
    "ta001": [3,17,15,8,9,6,5,14,16,7,11,13,18,19,1,4,2,10,20,12],
    "ta011": [18,5,2,12,9,10,4,14,15,17,13,3,6,19,8,20,11,7,1,16],
    "ta021": [16,18,14,7,13,8,15,9,6,20,17,12,10,11,5,1,2,4,3,19],
}

TA001_MACHINE_MAJOR_VERIFICATION = [
    [54,83,15,71,77,36,53,38,27,87,76,91,14,29,12,77,32,87,68,94],
    [79,3,11,99,56,70,99,60,5,56,3,61,73,75,47,14,21,86,5,77],
    [16,89,49,15,89,45,60,23,57,64,7,1,63,41,63,47,26,75,77,40],
    [66,58,31,68,78,91,13,59,49,85,85,9,39,41,56,40,54,77,51,31],
    [58,56,20,85,53,35,53,41,69,13,86,72,8,49,47,87,58,18,68,28],
]


def unif(seed: int, low: int = 1, high: int = 99) -> tuple[int, int]:
    k = seed // B
    seed = A * (seed % B) - k * C
    if seed < 0:
        seed += M
    value_0_1 = seed / M
    value = low + int(value_0_1 * (high - low + 1))
    return seed, value


def generate(seed: int, jobs: int, machines: int) -> list[list[int]]:
    # Original procedure fills d[machine][job]. Project representation is p[job][machine].
    machine_major = [[0] * jobs for _ in range(machines)]
    for machine in range(machines):
        for job in range(jobs):
            seed, value = unif(seed)
            machine_major[machine][job] = value
    return [[machine_major[m][j] for m in range(machines)] for j in range(jobs)]


def serialize(name: str, matrix: list[list[int]]) -> str:
    jobs = len(matrix)
    machines = len(matrix[0])
    lines = [f"{jobs} {machines}"]
    lines.extend(" ".join(str(v) for v in row) for row in matrix)
    return "\n".join(lines) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "data" / "taillard"
    out_dir.mkdir(parents=True, exist_ok=True)

    generated = {}
    for name, spec in SPECS.items():
        matrix = generate(spec["seed"], spec["jobs"], spec["machines"])
        if name == "ta001":
            machine_major = [list(col) for col in zip(*matrix)]
            assert machine_major == TA001_MACHINE_MAJOR_VERIFICATION, (
                "ta001 does not match the OR-Library verification matrix"
            )
        payload = serialize(name, matrix).encode("utf-8")
        path = out_dir / f"{name}.txt"
        path.write_bytes(payload)
        generated[name] = {**spec, "sha256": sha256_bytes(payload)}

    ref = {
        "source_generation": "https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/flowshop2.txt",
        "source_bounds_and_permutations": "https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/flowshop.dir/best_lb_up.txt",
        "bounds_source_update": "2026-06-03",
        "access_date": "2026-11-18",
        "instances": {
            name: {
                **generated[name],
                "reference_permutation_1_based": REFERENCE_PERMUTATIONS_1_BASED[name],
                "reference_permutation_0_based": [v - 1 for v in REFERENCE_PERMUTATIONS_1_BASED[name]],
            }
            for name in SPECS
        },
    }
    (out_dir / "reference_solutions.json").write_text(
        json.dumps(ref, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(generated, indent=2))


if __name__ == "__main__":
    main()
