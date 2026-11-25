"""Derive paper-only assets from immutable final results; --check is read-only.

Never writes results/, src/ or data/. Numerical blocks in both manuscripts are
rendered from the existing tables; full-precision raw values are cross-checked.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from verify_final_schedule import verify

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
INSTANCES = ("ta001", "ta011", "ta021")
ALGORITHMS = ("DBO", "DE", "NRBO", "PSO", "RIME")
sys.path.insert(0, str(ROOT / "src"))
import stat_tests as st


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                       "| " + " | ".join(["---"] * len(headers)) + " |"] +
                      ["| " + " | ".join(map(str, row)) + " |" for row in rows])


def best_runs(instance):
    frames = []
    for alg in ALGORITHMS:
        df = pd.read_csv(ROOT / f"results/raw/{instance}/{alg}.csv")
        df["algorithm"] = alg
        frames.append(df)
    data = pd.concat(frames)
    return data.loc[data.cmax == data.cmax.min()].sort_values(["run", "algorithm"])


def blocks():
    manifest = read_json("results/tables/experiment_manifest.json")
    evidence = read_json("results/verification.json")
    metadata = read_json("data/taillard/reference_solutions.json")
    assert manifest == evidence["manifest"]
    assert manifest["experiment_commit"] == evidence["sha"]
    assert (manifest["n_runs"], manifest["seed_base"]) == (30, 2026)
    settings = read_json("results/tables/deney_ayarlari.json")
    assert settings["MAX_FES"] == manifest["max_fes"]
    for row in csv.DictReader((ROOT / "results/tables/parametre_ayarlari.csv").open(encoding="utf-8-sig")):
        assert json.loads(row["Parametreler"]) == manifest["algorithm_parameters"][row["Algoritma"]]
    # Hashes are checked against the experiment evidence, not silently refreshed.
    for rel, digest in evidence["raw_sha256"].items():
        assert hashlib.sha256((ROOT / "results" / rel).read_bytes()).hexdigest() == digest, rel
    out = {}
    out["parameters"] = table(["Algoritma", "Popülasyon", "Etkin parametreler"], [
        [alg, manifest["algorithm_parameters"][alg]["pop_size"], "; ".join(
            f"{k}={v}" for k, v in manifest["algorithm_parameters"][alg].items() if k != "pop_size")]
        for alg in ALGORITHMS])
    out["benchmarks"] = table(["Örnek", "Boyut", "Veri üretim tohumu", "Referans", "FE/koşu", "SHA-256"], [
        [inst, f"20×{metadata['instances'][inst]['machines']}", metadata["instances"][inst]["seed"],
         metadata["instances"][inst]["bks"], manifest["max_fes"][inst],
         "`" + metadata["instances"][inst]["sha256"] + "`"] for inst in INSTANCES])
    out["environment"] = table(["Alan", "Manifest değeri"], list(manifest["environment"].items()) +
                               [["CPU", "[TEYİT BEKLİYOR]"], ["RAM", "[TEYİT BEKLİYOR]"]])
    rows, runtime, friedman, pairs, convergence = [], [], [], [], []
    for inst in INSTANCES:
        raw = st.load_results(inst)
        saved = pd.read_csv(ROOT / f"results/tables/{inst}_istatistikler.csv", index_col=0)
        calculated = st.descriptive_table(raw)
        np.testing.assert_allclose(saved.loc[calculated.index, calculated.columns], calculated, rtol=1e-8)
        bks = metadata["instances"][inst]["bks"]
        for alg in ALGORITHMS:
            v = saved[alg]
            rows.append([inst, alg, 30, int(v["En iyi"]), int(v["En kötü"]),
                         f"{v['Ortalama']:.6f}", f"{v['Medyan']:.6f}", f"{v['Std. sapma']:.6f}",
                         f"{raw[alg].rpd.mean():.6f}", f"{v['Uygunluk oranı (%)']:.0f}"])
            runtime.append([inst, alg, f"{v['Ort. süre (s)']:.6f}", f"{raw[alg].time.std(ddof=1):.6f}"])
            curves = np.asarray(raw[alg].history_f.tolist())
            fes = np.asarray(raw[alg].history_fes.iloc[0])
            values = []
            for fraction in (0.25, 0.5, 1):
                idx = np.flatnonzero(fes <= manifest["max_fes"][inst] * fraction)[-1]
                values.append(f"{np.median(curves[:, idx]):.1f}")
            convergence.append([inst, alg, *values])
        wil = pd.read_csv(ROOT / f"results/tables/{inst}_wilcoxon.csv", dtype=str)
        actual_wil = st.wilcoxon_table(raw)
        for col in ("z", "p-değeri", "p (Holm)"):
            np.testing.assert_allclose(wil[col].astype(float), actual_wil[col], rtol=0.0006, atol=1e-15)
        assert list(wil["Sonuç"]) == list(actual_wil["Sonuç"])
        out[f"wilcoxon_{inst}"] = table(list(wil.columns), wil.values.tolist())
        fr = st.friedman_test(raw)
        assert np.isclose(fr["p_value"], evidence["friedman"][inst]["p_value"], rtol=1e-8, atol=0)
        ranks = pd.read_csv(ROOT / f"results/tables/{inst}_friedman.csv", index_col=0)
        np.testing.assert_allclose(ranks.iloc[:, 0], fr["mean_ranks"].loc[ranks.index], atol=0.00051)
        out[f"ranks_{inst}"] = table(["Algoritma", *ranks.columns], [[a, *ranks.loc[a]] for a in ranks.index])
        cd = st.nemenyi_cd(fr["k"], fr["n_blocks"])
        friedman.append([inst, f"{fr['statistic']:.6f}", format(fr["p_value"], ".12g"), 30, 5, f"{cd:.6f}"])
        significant = []
        for i, a in enumerate(ALGORITHMS):
            for b in ALGORITHMS[i + 1:]:
                if abs(fr["mean_ranks"][a] - fr["mean_ranks"][b]) > cd:
                    significant.append(a + " / " + b)
        pairs.append([inst, "; ".join(significant) or "Yok"])
    out["statistics"] = table(["Örnek", "Yöntem", "n", "En iyi", "En kötü", "Ortalama", "Medyan", "Std. sapma", "Ort. RPD (%)", "Uygun (%)"], rows)
    out["runtime"] = table(["Örnek", "Yöntem", "Ort. süre (s)", "Süre std. (s)"], runtime)
    out["convergence"] = table(["Örnek", "Yöntem", "%25 FE medyanı", "%50 FE medyanı", "%100 FE medyanı"], convergence)
    out["friedman"] = table(["Örnek", "Friedman istatistiği", "p", "Blok", "Yöntem", "CD"], friedman)
    out["nemenyi"] = table(["Örnek", "CD'yi aşan sıra farkı çiftleri"], pairs)
    best = []
    for inst in INSTANCES:
        for _, r in best_runs(inst).iterrows():
            verify(inst, r.permutation.split(), int(r.cmax))
            best.append([inst, r.algorithm, int(r.run), int(r.seed), int(r.cmax), f"{r.rpd:.6f}", r.permutation])
    out["best"] = table(["Örnek", "Yöntem", "Run", "Seed", "Cmax", "RPD (%)", "Permütasyon (1 tabanlı)"], best)
    neh_text = (PAPER / "support/neh_baseline.md").read_text(encoding="utf-8")
    neh_times = re.findall(r"\*\*(\d+\.\d+) s\*\*", neh_text)
    assert len(neh_times) == 3
    neh_rows = []
    for line in neh_text.splitlines():
        if line.startswith("| ta"):
            cells = [c.strip().replace("**", "") for c in line.strip("|").split("|")]
            verify(cells[0], cells[4].split(), int(cells[2]))
            neh_rows.append(cells[:4] + [neh_times[len(neh_rows)]])
    out["neh"] = table(["Örnek", "Referans Cmax", "NEH Cmax", "RPD (%)", "CI referans süre (s)"], neh_rows)
    return out


def marked(key, content):
    return f"<!-- data:{key} -->\n{content}\n<!-- /data:{key} -->"


def nase_text():
    """Keep the course manuscript canonical; only rearrange for the journal."""
    source = (PAPER / "outline.md").read_text(encoding="utf-8")
    parts = re.split(r"^#{2,3} (.+)\n", source, flags=re.M)
    sections = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}
    result = ["# NASE Türkçe İçerik/Düzen Taslağı — Gönderime Uygun Değil\n",
              "**Durum: YALNIZ TÜRKÇE İÇ KONTROL KOPYASI; İngilizce NASE yazım kuralına göre doğrudan gönderilemez. İngilizce çalışma metni: [manuscript_nase_en.md](manuscript_nase_en.md).** "
              "Bu dosya [ders makalesinden](outline.md) `python -B tools/prepare_paper_assets.py --nase` "
              "ile türetilir; bağımsız bir sonuç veya yöntem kaynağı değildir.\n",
              "**Biçim ve gönderim kontrol notu:** [Resmî NASE kuralları](https://dergipark.org.tr/en/pub/nase/writing-rules) "
              "25.11.2026 tarihinde kontrol edildi. DOCX şablonuna aktarımda tek sütun, 10 pt Times New Roman, "
              "1.15 satır aralığı ve 2.5 cm kenar boşluğu uygulanmalıdır. Başlık 12 pt; özet, anahtar kelimeler "
              "ve kaynakça 9 pt; abstract 150–300 kelime, anahtar kelimeler 5–8 adet olmalıdır. "
              "Yazar soyadları büyük harfle; her yazar için kurum/fakülte/bölüm, e-posta ve ORCID gereklidir. "
              "APA 6 yazar–yıl atıfları ve alfabetik kaynakça korunmalıdır. Şekil ve tablolar metinde anılmalı, "
              "denklemler ardışık numaralarla Word denklem düzenleyicisine aktarılmalıdır. Markdown dosyası "
              "sayfa/font ayarlarını uygulamaz; resmî şablona son aktarım ve görsel kontrol **İNCELEME BEKLİYOR**. "
              "Danışman Türkçe/İngilizce seçimini kesinleştirmeli ve gönderim günü kurallar yeniden kontrol edilmelidir.\n"]
    for heading in ("Başlık", "Yazar Künyeleri", "Özet", "Abstract"):
        result.append(f"## {heading}\n\n{sections[heading]}")
    result.append("## 1. Introduction\n\n" + sections["1. Giriş"] +
                  "\n\n### 1.1. Literatür ve araştırma sorusu\n\n" + sections["2. Literatür Taraması"])
    result.append("## 2. Materials and Methods\n\n" + sections["3. Materyal ve Metot"])
    for heading, body in sections.items():
        if heading.startswith("3.") and heading != "3. Materyal ve Metot":
            result.append("### 2." + heading[2:] + "\n\n" + body)
    result.append("## 3. Results and Discussion\n\n" + sections["4. Deneysel Çalışmalar"])
    for heading, body in sections.items():
        if heading.startswith("4.") and heading != "4. Deneysel Çalışmalar":
            result.append("### 3." + heading[2:] + "\n\n" + body)
    conclusion, discussion = sections["5. Sonuç ve Tartışma"].split("\n\n", 1)
    result.append("### 3.9. Tartışma ve sınırlılıklar\n\n" + discussion)
    result.append("## 4. Conclusion\n\n" + conclusion +
                  "\n\nÇıkarımlar üç örnek ve sabit konfigürasyonla sınırlıdır; geniş PFSP ailesine "
                  "genel üstünlük iddiası taşınmaz. İnsan incelemesi ve yazar beyanları gönderim öncesinde tamamlanmalıdır.")
    for heading, label in (("Beyanlar", "Declarations"), ("Kaynaklar", "References"), ("Ekler", "Appendices")):
        result.append(f"## {label}\n\n{sections[heading]}")
    return "\n\n".join(result) + "\n"


def generate_schedules():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    support = PAPER / "support"
    sections = ["# Final en iyi çözümler ve bağımsız zaman çizelgeleri\n",
                "Kaynak: final 450 koşu; deney commit'i `73ce39c78a6263ce6f252267edeff0515157aca1`. "
                "En küçük Cmax seçilir; eşitlikte en küçük run, sonra alfabetik algoritma adı kullanılır. "
                "Aşağıda bütün minimum eşitlikleri listelenmiştir. Zamanlar yalnız bağımsız verifier'dan üretilir. "
                "Bu sayısal kontrol, ekip bağımsız inceleme/onayının yerine geçmez.\n",
                marked("best", blocks()["best"])]
    for inst in INSTANCES:
        row = best_runs(inst).iloc[0]
        perm = row.permutation
        command = [sys.executable, "-B", "tools/verify_final_schedule.py", "--instance", inst,
                   "--permutation", perm, "--expected-cmax", str(int(row.cmax)),
                   "--output", f"paper/support/schedule_{inst}.csv"]
        subprocess.run(command, cwd=ROOT, check=True)
        result = verify(inst, perm.split(), int(row.cmax))
        start, finish = result["start"], result["finish"]
        assert not np.any(start[1:] < finish[:-1])
        assert not np.any(start[:, 1:] < finish[:, :-1])
        fig, ax = plt.subplots(figsize=(13, max(4, start.shape[1] * 0.38)))
        cmap = plt.get_cmap("tab20")
        for pos, job in enumerate(result["permutation"]):
            for m in range(start.shape[1]):
                left, right = start[pos, m], finish[pos, m]
                ax.barh(m + 1, right - left, left=left, height=0.76, color=cmap(int(job)), edgecolor="black", linewidth=0.25)
                if right - left > row.cmax * 0.012:
                    ax.text((left + right) / 2, m + 1, str(job + 1), ha="center", va="center", fontsize=5)
        ax.set(yticks=range(1, start.shape[1] + 1), ylabel="Makine", xlabel="Zaman (benchmark birimi)", xlim=(0, int(row.cmax)))
        ax.invert_yaxis()
        ax.legend(handles=[Patch(facecolor=cmap(i), label=f"J{i + 1}") for i in range(20)], ncol=10,
                  loc="upper center", bbox_to_anchor=(0.5, -0.12), fontsize=7, frameon=False)
        fig.tight_layout()
        fig.savefig(support / f"gantt_{inst}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        sections += [f"\n## {inst}\n", f"Seçim: {row.algorithm}, run {int(row.run)}, seed {int(row.seed)}. "
                     f"Bağımsız Cmax={int(row.cmax)}; {start.size} işlem; makine çakışması=0; iş önceliği ihlali=0.\n",
                     f"[Verifier zaman tablosu](schedule_{inst}.csv) · [Ham koşular](../../results/raw/{inst}/{row.algorithm}.csv)\n",
                     f"![{inst} doğrulanmış Gantt](gantt_{inst}.png)\n",
                     "```powershell\npython tools/verify_final_schedule.py --instance " + inst +
                     ' --permutation "' + perm + '" --expected-cmax ' + str(int(row.cmax)) + "\n```\n"]
    sections += ["\nYeniden üretim: `python -B tools/prepare_paper_assets.py --generate`. "
                 "Bu komut yalnız bu özet, üç zaman CSV'si ve üç Gantt PNG'sini yazar. "
                 "Ham deney CSV'leri ve kabul kayıtları değiştirilmez.\n"]
    (support / "final_best_schedules.md").write_text("\n".join(sections), encoding="utf-8")


def check():
    expected = blocks()
    assert (PAPER / "manuscript_nase.md").read_text(encoding="utf-8") == nase_text(), "NASE diverged from course source"
    for filename in ("outline.md", "manuscript_nase.md", "manuscript_nase_en.md"):
        text = (PAPER / filename).read_text(encoding="utf-8")
        found = re.findall(r"<!-- data:(\w+) -->\n(.*?)\n<!-- /data:\1 -->", text, re.S)
        assert {k for k, _ in found} == set(expected), (filename, "missing numerical blocks")
        for key, value in found:
            assert value == expected[key], (filename, key, "numerical mismatch")
        refs = set(re.findall(r'<a id="ref-([A-Z0-9]+)"></a>', text))
        used = set(re.findall(r'\]\(#ref-([A-Z0-9]+)\)', text))
        assert refs == used and len(refs) == 13, (filename, refs - used, used - refs)
        assert len(re.findall(r'<a id="ref-', text)) == 13
        ai_method = re.search(r"\*\*Yapay zekâ kullanım açıklaması:\*\* (.*?)(?=\n\n)", text, re.S).group(1)
        ai_declaration = re.search(r"\*\*Yapay Zekâ Kullanım Beyanı:\*\* (.*?)(?=\n\n)", text, re.S).group(1)
        assert ai_method == ai_declaration, (filename, "AI statements differ")
        for heading in (("Abstract",) if filename == "manuscript_nase_en.md" else ("Özet", "Abstract")):
            match = re.search(r"^## " + heading + r"\n\n(.*?)(?=\n\n\*\*)", text, re.M | re.S)
            assert match, (filename, heading)
            count = len(match.group(1).split())
            assert 170 <= count <= 240, (filename, heading, count)
            print(f"{filename} {heading}: {count} words")
        for label in (("Keywords",) if filename == "manuscript_nase_en.md" else ("Anahtar Kelimeler", "Keywords")):
            keywords = re.search(r"\*\*" + label + r":\*\* (.+)", text).group(1).split(";")
            assert 5 <= len(keywords) <= 8
            print(f"{filename} {label}: {len(keywords)}")
        print(f"{filename}: {len(found)} numerical blocks; 13 references; orphan/unused = 0/0")
    for inst in INSTANCES:
        row = best_runs(inst).iloc[0]
        result = verify(inst, row.permutation.split(), int(row.cmax))
        times = pd.read_csv(PAPER / f"support/schedule_{inst}.csv")
        np.testing.assert_array_equal(times.start, result["start"].ravel())
        np.testing.assert_array_equal(times.finish, result["finish"].ravel())
        np.testing.assert_array_equal(times.job, np.repeat(result["permutation"] + 1, result["start"].shape[1]))
        np.testing.assert_array_equal(times.machine, np.tile(np.arange(1, result["start"].shape[1] + 1), 20))
        assert (PAPER / f"support/gantt_{inst}.png").is_file()
    print("PAPER CHECK: PASS (raw hashes, table recalculation, manuscript blocks, citations, abstracts, schedules)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--nase", action="store_true", help="derive the journal draft from outline.md")
    args = parser.parse_args()
    if args.generate:
        generate_schedules()
    if args.nase:
        (PAPER / "manuscript_nase.md").write_text(nase_text(), encoding="utf-8")
    if args.check:
        check()
    if not (args.generate or args.check or args.nase):
        parser.error("select --generate, --nase and/or --check")
