# -*- coding: utf-8 -*-
"""
===============================================================================
 YMM4142 - Optimizasyon Teorisi | 2026-2027 Güz Yarıyılı | Final Projesi
 stat_tests.py  —  İSTATİSTİKSEL ANALİZ YARDIMCI MODÜLÜ (ders paketi)
===============================================================================

Bu dosya ders paketiyle hazır gelir; DEĞİŞTİRMENİZ GEREKMEZ. main.py tarafından
otomatik çağrılır. Fonksiyonları kendi analizleriniz için ayrıca da
kullanabilirsiniz.

(Not: Dosyanın adı bilerek "statistics.py" değildir; o ad Python'un standart
kütüphanesindeki bir modülle çakışır.)

İÇERİK
------
  load_results(instance)          : results/raw/<instance>/*.csv dosyalarını okur.
  descriptive_table(results)      : En iyi, en kötü, ortalama, medyan, std,
                                    uygunluk oranı, ortalama süre tablosu.
  wilcoxon_table(results)         : En iyi algoritmanın diğer dördüyle ikili
                                    karşılaştırması (Wilcoxon sıra toplamı testi
                                    + Holm düzeltmesi, +/=/− işaretleri).
  friedman_test(results)          : Friedman testi ve ortalama sıralar.
  nemenyi_cd(k, n)                : Nemenyi sonrası testi için kritik fark (CD).

HANGİ TEST, NEDEN?
------------------
* Meta-sezgisellerin sonuçları genellikle normal dağılmaz; bu nedenle
  parametrik olmayan testler kullanılır (Derrac vd., 2011).
* Aynı test örneğinde iki algoritmanın 30 koşusu birbirinden BAĞIMSIZ
  örneklemlerdir; bu yüzden ikili karşılaştırmada "Wilcoxon sıra toplamı"
  (rank-sum, Mann-Whitney U ile eşdeğer) testi kullanılır.
* Beş algoritmanın birlikte karşılaştırılmasında Friedman testi kullanılır.
  Tüm algoritmalarda k. koşu aynı tohumla başlatıldığı için koşular "blok"
  olarak alınır. Friedman anlamlı fark gösterirse Nemenyi testi ile hangi
  algoritmaların birbirinden farklı olduğu kritik fark (CD) diyagramıyla
  gösterilir (Demšar, 2006).
* Birden çok ikili test yapıldığında yanlış pozitif riskini kontrol etmek
  için p-değerleri Holm yöntemiyle düzeltilir.

KAYNAKLAR
---------
 J. Derrac, S. García, D. Molina, F. Herrera, "A practical tutorial on the use
 of nonparametric statistical tests ...," Swarm Evol. Comput., 1(1), 3-18, 2011.
 J. Demšar, "Statistical comparisons of classifiers over multiple data sets,"
 J. Mach. Learn. Res., 7, 1-30, 2006.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "results" / "raw"

# Nemenyi testi için iki kuyruklu kritik değerler q_alpha (alpha = 0,05),
# k = 2..10 algoritma için (Demšar, 2006, Tablo 5a).
_Q_005 = {2: 1.960, 3: 2.344, 4: 2.569, 5: 2.728, 6: 2.850,
          7: 2.949, 8: 3.031, 9: 3.102, 10: 3.164}


# =============================================================================
# VERİ OKUMA
# =============================================================================
def load_results(instance: str, raw_dir: Path = RAW_DIR) -> dict[str, pd.DataFrame]:
    """Bir test örneğinin tüm algoritma sonuçlarını okur.

    Returns:
        {algoritma_adı: DataFrame} sözlüğü. Her satır bir koşudur.
        "history_fes" ve "history_f" sütunları listeye çevrilmiş olarak gelir.
    """
    folder = Path(raw_dir) / instance
    if not folder.exists():
        raise FileNotFoundError(f"Sonuç klasörü bulunamadı: {folder}")
    results = {}
    for csv in sorted(folder.glob("*.csv")):
        df = pd.read_csv(csv)
        for col in ("history_fes", "history_f", "best_x"):
            if col in df.columns:
                df[col] = df[col].apply(json.loads)
        results[csv.stem] = df.sort_values("run").reset_index(drop=True)
    if not results:
        raise FileNotFoundError(f"{folder} içinde sonuç dosyası yok.")
    return results


def _values(results: dict[str, pd.DataFrame], column: str = "best_f") -> pd.DataFrame:
    """Algoritmaları sütun, koşuları satır olan bir tablo oluşturur."""
    return pd.DataFrame({alg: df[column].to_numpy() for alg, df in results.items()})


# =============================================================================
# 1) TANIMLAYICI İSTATİSTİKLER
# =============================================================================
def descriptive_table(results: dict[str, pd.DataFrame], column: str = "best_f") -> pd.DataFrame:
    """Makaledeki "sayısal sonuçlar" tablosunu üretir.

    Satırlar: En iyi, En kötü, Ortalama, Medyan, Std. sapma,
              Uygunluk oranı (%), Ort. süre (s)
    Sütunlar: Algoritmalar
    """
    rows = {}
    for alg, df in results.items():
        v = df[column].to_numpy(dtype=float)
        rows[alg] = {
            "En iyi": np.min(v),
            "En kötü": np.max(v),
            "Ortalama": np.mean(v),
            "Medyan": np.median(v),
            "Std. sapma": np.std(v, ddof=1) if len(v) > 1 else 0.0,
            "Uygunluk oranı (%)": 100.0 * df["feasible"].astype(bool).mean()
            if "feasible" in df else np.nan,
            "Ort. süre (s)": df["time"].mean() if "time" in df else np.nan,
        }
    return pd.DataFrame(rows)


# =============================================================================
# 2) WILCOXON SIRA TOPLAMI TESTİ (ikili karşılaştırma)
# =============================================================================
def holm_correction(pvalues: list[float]) -> list[float]:
    """Holm-Bonferroni yöntemiyle düzeltilmiş p-değerleri."""
    p = np.asarray(pvalues, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adjusted = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[idx]))
        adjusted[idx] = running
    return adjusted.tolist()


def wilcoxon_table(results: dict[str, pd.DataFrame], column: str = "best_f",
                   alpha: float = 0.05, reference: str | None = None) -> pd.DataFrame:
    """Referans algoritmayı diğerleriyle Wilcoxon sıra toplamı testiyle karşılaştırır.

    Args:
        reference: Referans algoritma. Verilmezse medyanı en küçük olan seçilir.

    Sonuç sütunu:
        "+" : referans algoritma anlamlı olarak DAHA İYİ
        "=" : anlamlı fark yok
        "−" : referans algoritma anlamlı olarak DAHA KÖTÜ
    """
    data = _values(results, column)
    if reference is None:
        reference = data.median().idxmin()
    ref = data[reference].to_numpy()

    rows, pvals = [], []
    for alg in data.columns:
        if alg == reference:
            continue
        other = data[alg].to_numpy()
        if np.allclose(ref, other):
            stat, p = 0.0, 1.0
        else:
            stat, p = stats.ranksums(ref, other)
        pvals.append(p)
        rows.append({"Karşılaştırma": f"{reference} – {alg}", "z": stat, "p-değeri": p,
                     "_ref_med": np.median(ref), "_oth_med": np.median(other)})

    for row, p_holm in zip(rows, holm_correction(pvals)):
        row["p (Holm)"] = p_holm
        if p_holm >= alpha:
            row["Sonuç"] = "="
        else:
            row["Sonuç"] = "+" if row["_ref_med"] < row["_oth_med"] else "−"
    df = pd.DataFrame(rows).drop(columns=["_ref_med", "_oth_med"])
    return df[["Karşılaştırma", "z", "p-değeri", "p (Holm)", "Sonuç"]]


# =============================================================================
# 3) FRIEDMAN TESTİ VE NEMENYI KRİTİK FARKI
# =============================================================================
def friedman_test(results: dict[str, pd.DataFrame], column: str = "best_f") -> dict:
    """Friedman testi (koşular blok, algoritmalar işlem olarak).

    Returns:
        {"statistic", "p_value", "mean_ranks" (pd.Series, küçük = iyi),
         "n_blocks", "k"}
    """
    data = _values(results, column).dropna()
    k, n = data.shape[1], data.shape[0]
    if k < 3:
        raise ValueError("Friedman testi için en az 3 algoritma gerekir.")
    ranks = data.rank(axis=1, method="average")       # her koşuda 1 = en iyi
    mean_ranks = ranks.mean().sort_values()
    stat, p = stats.friedmanchisquare(*[data[c].to_numpy() for c in data.columns])
    return {"statistic": float(stat), "p_value": float(p),
            "mean_ranks": mean_ranks, "n_blocks": n, "k": k}


def nemenyi_cd(k: int, n: int, alpha: float = 0.05) -> float:
    """Nemenyi testi için kritik fark: CD = q_alpha * sqrt(k(k+1) / (6n))."""
    if alpha != 0.05 or k not in _Q_005:
        raise ValueError("Yalnızca alpha=0.05 ve 2 <= k <= 10 desteklenir.")
    return _Q_005[k] * np.sqrt(k * (k + 1) / (6.0 * n))


def friedman_table(fr: dict) -> pd.DataFrame:
    """Friedman sonuçlarını makaleye hazır tablo hâline getirir."""
    mr = fr["mean_ranks"]
    return pd.DataFrame({"Ortalama Friedman sırası": mr.values,
                         "Genel sıra": np.arange(1, len(mr) + 1)}, index=mr.index)


if __name__ == "__main__":
    print(__doc__)
