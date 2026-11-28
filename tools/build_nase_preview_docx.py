"""Build a review-only DOCX preview from the English PFSP manuscript.

This is not the official NASE journal template and does not certify final equations.
"""
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper/manuscript_nase_en.md"

def text_only(s):
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", s)
    s = re.sub(r"</?[^>]+>", "", s)
    return s.replace("**", "").replace("__", "").replace(chr(96), "").strip()

def append_table(doc, lines):
    rows = [[text_only(c.strip()) for c in ln.strip().strip("|").split("|")] for ln in lines]
    if len(rows) > 1 and all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in rows[1]):
        rows.pop(1)
    count = max(len(x) for x in rows)
    table = doc.add_table(rows=0, cols=count)
    table.style = "Table Grid"
    for index, row in enumerate(rows):
        cells = table.add_row().cells
        for j, c in enumerate(cells):
            c.text = row[j] if j < len(row) else ""
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(7 if count >= 6 else 8)
                    run.bold = index == 0

def build():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = sec.bottom_margin = Cm(2.5)
    sec.left_margin = sec.right_margin = Cm(2.5)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(10)
    normal.paragraph_format.line_spacing = 1.15
    for name in ("Heading 1", "Heading 2", "Heading 3"):
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(10)
        style.font.bold = True
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    i = 0
    title_seen = False
    tables = images = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("<!--") or line.startswith("-->") or line.startswith("<a id="):
            continue
        if line.startswith("|"):
            block = [line]
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            append_table(doc, block)
            tables += 1
            continue
        image = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if image:
            path = (SOURCE.parent / image.group(2)).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                raise FileNotFoundError(f"Missing figure: {image.group(2)}")
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(str(path), width=Inches(5.75))
            cap = doc.add_paragraph(text_only(image.group(1)))
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            images += 1
            continue
        if line.startswith("# "):
            if not title_seen:
                doc.add_heading(text_only(line[2:]), 0)
                title_seen = True
            else:
                doc.add_heading(text_only(line[2:]), 1)
        elif line.startswith("## "):
            doc.add_heading(text_only(line[3:]), 1)
        elif line.startswith("### "):
            doc.add_heading(text_only(line[4:]), 2)
        elif line.startswith("- "):
            doc.add_paragraph(text_only(line[2:]), style="List Bullet")
        else:
            doc.add_paragraph(text_only(line))
    foot = sec.footer.paragraphs[0]
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    foot.add_run("UNAPPROVED EDITORIAL PREVIEW — NOT THE OFFICIAL NASE TEMPLATE").font.size = Pt(8)
    out = ROOT / "dist/PFSP_NASE_REVIEW_PREVIEW.docx"
    out.parent.mkdir(exist_ok=True)
    doc.save(out)
    if tables < 12 or images < 10:
        raise RuntimeError(f"Incomplete manuscript assets: tables={tables}, images={images}")
    print(f"DOCX PREVIEW PASS: tables={tables}, images={images}; {out}")

if __name__ == "__main__":
    build()
