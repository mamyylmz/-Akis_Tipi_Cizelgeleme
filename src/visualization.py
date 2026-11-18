# -*- coding: utf-8 -*-
"""
===============================================================================
 YMM4142 - Optimizasyon Teorisi | 2026-2027 Güz Yarıyılı | Final Projesi
 visualization.py  —  YAYIN KALİTESİNDE GRAFİK YARDIMCI MODÜLÜ (ders paketi)
===============================================================================

Bu dosya ders paketiyle hazır gelir; DEĞİŞTİRMENİZ GEREKMEZ. main.py tarafından
otomatik çağrılır ve grafikleri results/figures/ klasörüne hem PDF (vektörel,
makale için) hem de 600 dpi PNG olarak kaydeder.

İÇERİK
------
  plot_convergence(results, instance) : Yakınsama eğrileri (30 koşunun medyanı
                                        ve çeyrekler açıklığı).
  plot_boxplot(results, instance)     : Kutu grafikleri (her nokta bir koşu).
  plot_cd_diagram(mean_ranks, cd, instance) : Kritik fark (CD) diyagramı.

Biçim kuralları (makale kılavuzundaki "Profesyonel şekil hazırlama kuralları"):
renk körlüğüne uygun Okabe-Ito paleti, renkle birlikte farklı işaretçiler,
şekil içinde başlık yok, eksen adları açık, bir algoritmanın rengi tüm
grafiklerde aynı.

Problemin fiziksel görselleştirmesi (kafes çizimi, ışıma diyagramı, I-V eğrisi,
şebeke çizimi vb.) probleme özgü olduğu için bu modülde yoktur; grubunuz
tarafından ayrıca hazırlanmalıdır.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")                     # ekran gerektirmeden dosyaya çizim
import matplotlib.pyplot as plt           # noqa: E402
import numpy as np                        # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "results" / "figures"

COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00",
          "#56B4E9", "#F0E442", "#000000"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9, "legend.fontsize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans",          # Türkçe karakterler için
})


def _style(algorithms: list[str]) -> dict[str, tuple[str, str]]:
    """Her algoritmaya sabit bir (renk, işaretçi) atar. Sıralama alfabetiktir;
    böylece aynı algoritma tüm grafiklerde aynı görünür."""
    return {a: (COLORS[i % len(COLORS)], MARKERS[i % len(MARKERS)])
            for i, a in enumerate(sorted(algorithms))}


def _save(fig, name: str, out_dir: Path = FIG_DIR) -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = [out_dir / f"{name}.pdf", out_dir / f"{name}.png"]
    fig.savefig(paths[0])
    fig.savefig(paths[1], dpi=600)
    plt.close(fig)
    return paths


def _use_log(values: np.ndarray) -> bool:
    """Değerler pozitif ve iki mertebeden fazla yayılıyorsa log ölçek önerilir."""
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    return v.size > 0 and np.all(v > 0) and v.max() / v.min() > 100


# =============================================================================
# 1) YAKINSAMA EĞRİLERİ
# =============================================================================
def plot_convergence(results: dict, instance: str, log_scale: bool | None = None,
                     width_cm: float = 8.5, out_dir: Path = FIG_DIR) -> list[Path]:
    """30 koşunun medyan yakınsama eğrisi ve çeyrekler açıklığı (gölge).

    Args:
        results  : stat_tests.load_results() çıktısı.
        log_scale: None ise otomatik seçilir.
        width_cm : Şekil genişliği (tek sütun ≈ 8,5 cm, çift sütun ≈ 17 cm).
    """
    style = _style(list(results))
    fig, ax = plt.subplots(figsize=(width_cm / 2.54, width_cm / 2.54 * 0.68))
    all_vals = []
    for alg, df in sorted(results.items()):
        fes = np.asarray(df["history_fes"].iloc[0], dtype=float)
        curves = np.array([h for h in df["history_f"]], dtype=float)
        med = np.median(curves, axis=0)
        q1, q3 = np.percentile(curves, [25, 75], axis=0)
        c, m = style[alg]
        ax.plot(fes, med, color=c, marker=m, markevery=max(1, len(fes) // 8),
                ms=3.5, lw=1.2, label=alg)
        ax.fill_between(fes, q1, q3, color=c, alpha=0.15, lw=0)
        all_vals.append(med)
    if log_scale is None:
        log_scale = _use_log(np.concatenate(all_vals))
    if log_scale:
        ax.set_yscale("log")
    # FE eksenini okunaklı ölçekle (ör. 0, 1, 2 ... × 10^4)
    p10 = int(np.floor(np.log10(max(fes.max(), 1))))
    if p10 >= 3:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v / 10 ** p10:g}"))
        ax.set_xlabel(f"Amaç fonksiyonu değerlendirme sayısı (FE, ×10$^{{{p10}}}$)")
    else:
        ax.set_xlabel("Amaç fonksiyonu değerlendirme sayısı (FE)")
    ax.set_ylabel("En iyi uygunluk değeri" + (" (log ölçek)" if log_scale else ""))
    ax.legend(ncol=min(5, len(results)), loc="lower center",
              bbox_to_anchor=(0.5, 1.0), handlelength=1.5, columnspacing=0.8)
    return _save(fig, f"{instance}_yakinsama", out_dir)


# =============================================================================
# 2) KUTU GRAFİKLERİ
# =============================================================================
def plot_boxplot(results: dict, instance: str, column: str = "best_f",
                 width_cm: float = 8.5, out_dir: Path = FIG_DIR) -> list[Path]:
    """Koşu sonu değerlerinin kutu grafikleri; her nokta bir koşudur."""
    style = _style(list(results))
    algs = sorted(results)
    data = [results[a][column].to_numpy(dtype=float) for a in algs]
    rng = np.random.default_rng(0)                    # nokta saçılımı için
    fig, ax = plt.subplots(figsize=(width_cm / 2.54, width_cm / 2.54 * 0.62))
    bp = ax.boxplot(data, patch_artist=True, widths=0.55, showfliers=False,
                    medianprops=dict(color="black", lw=1.1))
    for patch, a in zip(bp["boxes"], algs):
        patch.set_facecolor(style[a][0])
        patch.set_alpha(0.55)
    for i, d in enumerate(data, start=1):
        ax.scatter(i + rng.uniform(-0.13, 0.13, len(d)), d, s=5, color="black",
                   alpha=0.5, zorder=3, lw=0)
    ax.set_xticks(range(1, len(algs) + 1))
    ax.set_xticklabels(algs)
    ax.set_ylabel("Koşu sonu uygunluk değeri")
    if _use_log(np.concatenate(data)):
        ax.set_yscale("log")
    ax.yaxis.grid(alpha=0.3)
    return _save(fig, f"{instance}_kutu", out_dir)


# =============================================================================
# 3) KRİTİK FARK (CD) DİYAGRAMI
# =============================================================================
def _cliques(ranks: np.ndarray, cd: float) -> list[tuple[int, int]]:
    """Aralarındaki fark CD'den küçük olan ardışık algoritma grupları
    (sıralanmış dizide [i, j] indeks aralıkları; yalnızca en geniş olanlar)."""
    n = len(ranks)
    spans = []
    for i in range(n):
        j = i
        while j + 1 < n and ranks[j + 1] - ranks[i] < cd:
            j += 1
        if j > i:
            spans.append((i, j))
    return [s for s in spans
            if not any(o != s and o[0] <= s[0] and s[1] <= o[1] for o in spans)]


def plot_cd_diagram(mean_ranks, cd: float, instance: str,
                    width_cm: float = 12.0, out_dir: Path = FIG_DIR) -> list[Path]:
    """Nemenyi sonrası testine ait kritik fark diyagramı.

    Args:
        mean_ranks: stat_tests.friedman_test()["mean_ranks"] (pd.Series).
        cd        : stat_tests.nemenyi_cd(k, n) değeri.

    Okuma: Eksen ortalama Friedman sırasıdır (küçük = iyi). Kalın yatay
    çizgiyle birleştirilen algoritmalar arasında anlamlı fark YOKTUR.
    """
    mr = mean_ranks.sort_values()
    names, ranks = list(mr.index), mr.to_numpy(dtype=float)
    k = len(ranks)
    style = _style(names)
    half = (k + 1) // 2
    cliques = _cliques(ranks, cd)
    top = 0.3 + 0.2 * len(cliques)          # etiketlerin başladığı derinlik

    fig, ax = plt.subplots(figsize=(width_cm / 2.54, 1.0 + 0.3 * (half + len(cliques) / 2)))
    ax.set_xlim(0.4, k + 0.6)
    ax.set_ylim(-(top + 0.5 * half + 0.3), 1.6)
    ax.axis("off")

    ax.plot([1, k], [0, 0], color="black", lw=1)            # sıra ekseni
    for t in range(1, k + 1):
        ax.plot([t, t], [0, 0.12], color="black", lw=1)
        ax.text(t, 0.2, str(t), ha="center", va="bottom", fontsize=8)

    # CD ölçeği
    ax.plot([1, 1 + cd], [1.2, 1.2], color="black", lw=1.4)
    for x in (1, 1 + cd):
        ax.plot([x, x], [1.1, 1.3], color="black", lw=1.4)
    ax.text(1 + cd / 2, 1.35, f"CD = {cd:.2f}", ha="center", va="bottom", fontsize=8)

    # Algoritma etiketleri: iyi yarı solda, kötü yarı sağda
    for i, (name, r) in enumerate(zip(names, ranks)):
        c = style[name][0]
        if i < half:
            y, xe, ha = -top - i * 0.5, 0.55, "right"
        else:
            y, xe, ha = -top - (k - 1 - i) * 0.5, k + 0.45, "left"
        ax.plot([r, r, xe], [0, y, y], color=c, lw=1.1)
        ax.text(xe + (-0.05 if ha == "right" else 0.05), y, f"{name} ({r:.2f})",
                ha=ha, va="center", fontsize=8)

    # Anlamlı fark olmayan gruplar (eksenin hemen altında, üst üste binmeden)
    for n_, (i, j) in enumerate(cliques):
        yy = -0.18 - 0.2 * n_
        ax.plot([ranks[i] - 0.04, ranks[j] + 0.04], [yy, yy], color="black",
                lw=2.4, solid_capstyle="butt", zorder=5)
    return _save(fig, f"{instance}_cd", out_dir)
