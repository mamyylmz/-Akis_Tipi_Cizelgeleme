"""Run from workspace root: python docs/check_literature.py."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
GUIDE = "docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md"
FILES = ["paper/literature_matrix.md", "paper/gap_analysis.md",
         "paper/introduction_draft.md", "paper/outline.md",
         "docs/journal_shortlist.md", "docs/gantt_plan.md",
         "paper/source_audit.md", "sprintler/06_TESLIM_KANIT_SABLONU.md",
         "sprintler/07_Bilal_Literatur_Teslim_Kaniti.md", GUIDE,
         "README.md", "AGENTS.md"]

def inspect():
    texts = {name: (ROOT / name).read_text(encoding="utf-8-sig") for name in FILES}
    # Include operational instructions in link and version checks as well.
    for folder in ("sprintler", "kişiyeözeldosyaları"):
        for path in sorted((ROOT / folder).glob("*.md")):
            texts[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8-sig")
    article_template = texts[GUIDE].split("# BÖLÜM III: PFSP MAKALE TASLAĞI", 1)[1].split("# BÖLÜM IV:", 1)[0]
    expected_headings = re.findall(r"^#{2,3} (.+)$", article_template, re.M)
    actual_headings = re.findall(r"^#{2,3} (.+)$", texts["paper/outline.md"], re.M)
    journal_section = texts[GUIDE].split("## 18. Hedef Dergi Seçim Prosedürü", 1)[1].split("## 19.", 1)[0]
    allowed_journals = set(re.findall(r"dergipark\.org\.tr/(?:tr|en)/pub/([a-z0-9]+)", journal_section))
    candidate_rows = [line for line in texts["docs/journal_shortlist.md"].splitlines()
                      if re.match(r"\| [12] —", line)]
    selected_journals = set(re.findall(r"dergipark\.org\.tr/(?:tr|en)/pub/([a-z0-9]+)", "\n".join(candidate_rows)))
    body = "\n".join(line for line in texts[FILES[2]].splitlines()
                     if line.strip() and not line.startswith(("#", "**")))
    body = re.sub(r"\[[^\]]*\]\([^\n]*?\)(?=\s|$)", "", body)
    words = len(body.split())
    rows = [line for line in texts[FILES[0]].splitlines()
            if re.match(r"\| L\d\d \|", line)]
    main = [line for line in rows if "[DOI]" in line]
    dois = [line.split("[DOI](", 1)[1].split(" |", 1)[0] for line in main]
    broken = []
    for name, content in texts.items():
        for target in re.findall(r"\]\(([^\s)]+)\)", content):
            if "://" not in target and not (ROOT / name).parent.joinpath(target.split("#")[0]).exists():
                broken.append([name, target])
    checks = {"introduction_500_700": 500 <= words <= 700,
              "12_unique_dois": len(dois) == len(set(dois)) == 12,
              "two_12_row_tables": len(rows) == 24,
              "unbroken_tables": not re.search(r"\|\n\s*\n\| L\d", texts[FILES[0]]),
              "local_file_links": not broken,
              "guide_article_headings_match": bool(expected_headings) and actual_headings == expected_headings,
              "journals_in_guide": len(candidate_rows) == 2 and len(selected_journals) == 2 and selected_journals <= allowed_journals}
    result = {"word_count": words, "checks": checks, "broken_links": broken,
              "guide_heading_count": len(expected_headings),
              "selected_journals": sorted(selected_journals),
              "sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in texts}}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return all(checks.values())

if __name__ == "__main__":
    raise SystemExit(0 if inspect() else 1)
