#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "src/problem.py", "src/main.py",
    "src/algorithms/de.py", "src/algorithms/pso.py", "src/algorithms/dbo.py",
    "src/algorithms/rime.py", "src/algorithms/nrbo.py",
    "src/heuristics/neh.py",
    "data/README.md", "data/taillard/ta001.txt", "data/taillard/ta011.txt",
    "data/taillard/ta021.txt", "data/taillard/reference_solutions.json",
    "paper/outline.md", "paper/STATUS.md",
    "docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md",
    "docs/KALITE_KARARLARI.md", "docs/GIT_WORKFLOW.md", "docs/quality_status.md",
    "worklists/README.md",
    "tools/run_neh_baseline.py", "tools/verify_final_schedule.py",
    "tests/test_neh.py", "tests/test_schedule_verifier.py",
]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    meta_path = ROOT / "data/taillard/reference_solutions.json"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        for name, info in meta.get("instances", {}).items():
            path = ROOT / f"data/taillard/{name}.txt"
            if path.is_file() and sha256(path) != info.get("sha256"):
                errors.append(f"benchmark hash mismatch: {name}")

    problem_text = (ROOT / "src/problem.py").read_text(encoding="utf-8") if (ROOT / "src/problem.py").is_file() else ""
    if "ornek_10d" in problem_text or "sum(z ** 2)" in problem_text or "küre fonksiyonu" in problem_text.lower():
        errors.append("src/problem.py still contains sphere-example implementation text")

    result_files = [p for p in (ROOT / "results").rglob("*") if p.is_file() and p.name not in {".gitkeep", "README.md"}] if (ROOT / "results").exists() else []
    manifest = ROOT / "results/tables/experiment_manifest.json"
    if result_files and not manifest.is_file():
        errors.append("results contain files without experiment_manifest.json: " + ", ".join(str(p.relative_to(ROOT)) for p in result_files[:10]))

    try:
        tracked = subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8"
        ).splitlines()
    except (OSError, subprocess.CalledProcessError):
        tracked = []
    tracked_caches = [
        p for p in tracked
        if "__pycache__/" in p or p.endswith((".pyc", ".pyo"))
    ]
    if tracked_caches:
        errors.append("generated Python cache artifacts are tracked: " + ", ".join(tracked_caches[:10]))

    for rel in ("sprintler", "kisiyeozeldosyalar", "docs/test_logs", "docs/experiments"):
        if (ROOT / rel).exists():
            errors.append(f"stale/historical repository area still present: {rel}")

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
    print("Historical repo clutter: PASS")
    print("Result provenance policy: PASS")
    print("No Python cache artifacts: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
