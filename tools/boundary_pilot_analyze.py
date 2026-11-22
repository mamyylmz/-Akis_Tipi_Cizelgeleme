"""Summarise tools/boundary_pilot.py output (PILOT ONLY, not final data).

Usage: python tools/boundary_pilot_analyze.py <runs.csv> <out.md>

Per algorithm x instance and mode: mean / median / sd RPD, boundary and tie
metrics. Paired comparison against clip (same seed) with the Wilcoxon
signed-rank test (zero_method="zsplit", two-sided), Holm-corrected over all
comparisons. Mean Friedman-style rank of the three modes over the 15
algorithm x instance blocks (rank 1 = lowest mean RPD).
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from scipy.stats import rankdata, wilcoxon

ALGOS = ["PSO", "DE", "DBO", "NRBO", "RIME"]
MODES = ["clip", "reflect", "random"]


def holm(pvals):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    m = len(p)
    for k, idx in enumerate(order):
        running = max(running, (m - k) * p[idx])
        adj[idx] = min(1.0, running)
    return adj


def main(csv_path, md_path):
    df = pd.read_csv(csv_path)
    n_seeds = df["seed"].nunique()
    lines = [f"Koşu sayısı: {len(df)} · seed: {df['seed'].min()}–{df['seed'].max()} ({n_seeds}) · "
             "tam ders bütçesi · **PİLOT, final veri değil**", ""]

    # 1) Boundary / tie metrics (averaged over seeds, instances)
    lines += ["### Sınır ve eşitlik ölçüleri (3 örnek × seed ortalaması)", "",
              "| Algoritma | Yöntem | En iyi çözümde sınırdaki anahtar | Adaylarda sınırdaki anahtar | "
              "Eşit anahtarlı aday | Benzersiz permütasyon / FE |",
              "|---|---|---:|---:|---:|---:|"]
    for a in ALGOS:
        for m in MODES:
            s = df[(df.algorithm == a) & (df["mode"] == m)]
            lines.append(f"| {a} | {m} | {100*s.best_x_bound_frac.mean():.1f}% | "
                         f"{100*s.cand_bound_frac.mean():.1f}% | {100*s.cand_tie_frac.mean():.1f}% | "
                         f"{100*s.unique_perm_frac.mean():.1f}% |")
    lines.append("")

    # 2) RPD table + paired tests
    tests = []
    rows = []
    for inst in sorted(df.instance.unique()):
        for a in ALGOS:
            base = df[(df.instance == inst) & (df.algorithm == a) & (df["mode"] == "clip")].sort_values("seed")
            row = {"inst": inst, "alg": a}
            for m in MODES:
                s = df[(df.instance == inst) & (df.algorithm == a) & (df["mode"] == m)].sort_values("seed")
                row[m] = (s.rpd.mean(), s.rpd.median(), s.rpd.std(ddof=1), s.best_f.min())
                if m != "clip":
                    diff = s.rpd.to_numpy() - base.rpd.to_numpy()
                    if np.all(diff == 0):
                        p = 1.0
                    else:
                        p = float(wilcoxon(s.rpd.to_numpy(), base.rpd.to_numpy(),
                                           zero_method="zsplit").pvalue)
                    tests.append((inst, a, m, p, float(np.mean(diff))))
            rows.append(row)
    adj = holm([t[3] for t in tests])
    padj = {(t[0], t[1], t[2]): (t[3], q, t[4]) for t, q in zip(tests, adj)}

    lines += ["### RPD (%) — ortalama / medyan / ss · en iyi Cmax", "",
              "| Örnek | Algoritma | clip | reflect | random | reflect − clip (p, Holm) | random − clip (p, Holm) |",
              "|---|---|---|---|---|---|---|"]
    for r in rows:
        cells = []
        for m in MODES:
            mean, med, sd, best = r[m]
            cells.append(f"{mean:.2f} / {med:.2f} / {sd:.2f} · {best:.0f}")
        comp = []
        for m in ("reflect", "random"):
            p, q, d = padj[(r["inst"], r["alg"], m)]
            cell = f"{d:+.2f} (p={p:.3f}, q={q:.3f})"
            comp.append(f"**{cell}**" if q < 0.05 else cell)
        lines.append(f"| {r['inst']} | {r['alg']} | " + " | ".join(cells) + " | " + " | ".join(comp) + " |")
    lines.append("")

    # 3) Mean rank of the modes over the 15 blocks
    ranks = {m: [] for m in MODES}
    for r in rows:
        means = [r[m][0] for m in MODES]
        rk = rankdata(means)
        for m, v in zip(MODES, rk):
            ranks[m].append(v)
    lines += ["### Yöntemlerin ortalama sırası (15 algoritma × örnek bloğu, 1 = en düşük ortalama RPD)", "",
              "| Yöntem | Ortalama sıra | Kaç blokta en iyi |", "|---|---:|---:|"]
    for m in MODES:
        wins = sum(1 for v in ranks[m] if v == 1)
        lines.append(f"| {m} | {np.mean(ranks[m]):.2f} | {wins} |")
    lines.append("")
    sig = [(k, v) for k, v in padj.items() if v[1] < 0.05]
    lines.append(f"Holm düzeltmesinden sonra anlamlı fark (q < 0,05): {len(sig)} / {len(padj)} karşılaştırma.")
    for (inst, a, m), (p, q, d) in sorted(sig):
        lines.append(f"- {inst} {a} {m}: ortalama RPD farkı {d:+.2f} puan (q={q:.4f})")
    open(md_path, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
