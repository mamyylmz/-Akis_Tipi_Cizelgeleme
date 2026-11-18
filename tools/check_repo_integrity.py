#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "src/problem.py",
    "src/algorithms/de.py",
    "tests/test_problem.py",
    "tests/test_de.py",
    "data/README.md",
    "data/taillard/ta001.txt",
    "data/taillard/ta011.txt",
    "data/taillard/ta021.txt",
    "data/taillard/reference_solutions.json",
    "paper/method_model.md",
    "docs/model_validation_report_2026-11-18.md",
    "docs/NEGATIF_KOMUTLAR_VE_KALITE_KARARLARI.md",
    "sprintler/08_Seref_Modelleme_Teslim_Kaniti.md",
]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    # Verify benchmark hashes from the metadata file.
    meta_path = ROOT / "data/taillard/reference_solutions.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        for name, info in meta.get("instances", {}).items():
            path = ROOT / f"data/taillard/{name}.txt"
            if path.is_file() and sha256(path) != info.get("sha256"):
                errors.append(f"benchmark hash mismatch: {name}")

    # No stale sphere example is allowed in the actual problem model.
    problem_text = (ROOT / "src/problem.py").read_text(encoding="utf-8") if (ROOT / "src/problem.py").is_file() else ""
    if "ornek_10d" in problem_text or "sum(z ** 2)" in problem_text or "küre fonksiyonu" in problem_text.lower():
        errors.append("src/problem.py still contains sphere-example implementation text")

    # Final experiment results must not be fabricated by smoke tests.
    result_files = [p for p in (ROOT / "results").rglob("*") if p.is_file() and p.name != ".gitkeep"] if (ROOT / "results").exists() else []
    if result_files:
        errors.append("non-placeholder files exist under results/: " + ", ".join(str(p.relative_to(ROOT)) for p in result_files[:10]))

    # Generated Python caches should not be included in the delivered archive.
    caches = list(ROOT.rglob("__pycache__")) + list(ROOT.rglob("*.pyc"))
    if caches:
        errors.append("generated Python cache files/directories present")

    # Every local Markdown link must resolve to a real file/directory. External URLs and pure anchors are skipped.
    for md in ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            resolved = (md.parent / file_part).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository: {md.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link: {md.relative_to(ROOT)} -> {target}")

    if errors:
        print("REPO INTEGRITY: FAIL")
        for e in errors:
            print("-", e)
        return 1
    print("REPO INTEGRITY: PASS")
    print(f"Required files: {len(REQUIRED)}/{len(REQUIRED)}")
    print("Benchmark hashes: PASS")
    print("Local Markdown links: PASS")
    print("No smoke/final result contamination: PASS")
    print("No Python cache artifacts: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
