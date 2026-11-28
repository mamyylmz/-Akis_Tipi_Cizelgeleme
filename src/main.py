# -*- coding: utf-8 -*-
"""
===============================================================================
 YMM4142 - Optimizasyon Teorisi | 2026-2027 Güz Yarıyılı | Final Projesi
 main.py  —  DENEY ÇALIŞTIRICI (ders paketi)
===============================================================================

Bu dosya problemi ve beş algoritmayı çalıştırır, sonuçları kaydeder, istatistik
tablolarını ve grafikleri üretir. Bu dosyada yalnızca aşağıdaki "DENEY
AYARLARI" bölümünü düzenlemeniz gerekir:
    1. Algoritmalarınızı içe aktarın (import satırları),
    2. ALGORITHMS sözlüğüne ekleyin.

KULLANIM (proje kök dizininde):
    python src/main.py                    # kontrol + deneyler + analiz
    python src/main.py --runs 3           # hızlı deneme (3 koşu)
    python src/main.py --check            # yalnızca problem ve algoritma kontrolü
    python src/main.py --only-analysis    # deneyleri tekrar koşturmadan analiz

ÇALIŞMA ADIMLARI
    [1] KONTROL : problem.py ve her algoritma kurallara uyuyor mu? Hata varsa
                  ne yapmanız gerektiği yazılır ve program durur.
    [2] DENEY   : Her test örneği × her algoritma × N_RUNS koşu.
                  k. koşu tüm algoritmalarda aynı tohumla (SEED_BASE + k) başlar.
                  Sonuçlar: results/raw/<test_örneği>/<ALGORİTMA>.csv
    [3] ANALİZ  : results/tables/ altına istatistik tabloları (CSV),
                  results/figures/ altına grafikler (PDF + PNG).
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import scipy

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))

import stat_tests as st                                  # noqa: E402
import visualization as vz                               # noqa: E402
from problem import INSTANCES, MAX_FES, Problem         # noqa: E402

# =============================================================================
#                              DENEY AYARLARI
# =============================================================================
# 1) Algoritmalarınızı içe aktarın (dosya adı ve fonksiyon adı aynıdır):
from algorithms.pso import pso                           # noqa: E402
from algorithms.de import de                             # noqa: E402
from algorithms.dbo import dbo                           # noqa: E402
from algorithms.nrbo import nrbo                         # noqa: E402
from algorithms.rime import rime                         # noqa: E402
# from algorithms.ga import ga
# ...

# 2) Algoritmaları ve parametrelerini buraya ekleyin.
#    Biçim:  "RAPORDAKİ_ADI": (fonksiyon, {parametre: değer, ...})
#    Parametreler özgün makalelerden alınır ve makalede tablo olarak raporlanır.
ALGORITHMS = {
    "PSO": (pso, {"pop_size": 30, "w_max": 0.9, "w_min": 0.4, "c1": 2.0, "c2": 2.0, "v_frac": 0.2}),
    "DE": (de, {"pop_size": 100, "F": 0.5, "CR": 0.9}),
    "DBO": (dbo, {"pop_size": 30, "k": 0.1, "b": 0.3, "S": 0.5,
                  "roll_prob": 0.9, "deviation_prob": 0.1}),
    "NRBO": (nrbo, {"pop_size": 30, "DF": 0.6}),
    "RIME": (rime, {"pop_size": 30, "w": 5}),
    # "GA":  (ga,  {"pop_size": 50, "pc": 0.9, "pm": 0.1}),
}
FINAL_ALGORITHMS = ("PSO", "DE", "DBO", "RIME", "NRBO")

N_RUNS = 30          # her algoritma, her test örneğinde bağımsız koşu sayısı
SEED_BASE = 2026     # k. koşunun tohumu: SEED_BASE + k
ALPHA = 0.05         # istatistiksel anlamlılık düzeyi
# =============================================================================

RAW_DIR = ROOT / "results" / "raw"
TAB_DIR = ROOT / "results" / "tables"
FIG_DIR = ROOT / "results" / "figures"
REQUIRED_KEYS = {"best_x", "best_f", "history", "n_fes", "time"}


class KontrolHatasi(Exception):
    """Öğrenciye ne yapması gerektiğini söyleyen hata."""


# =============================================================================
# [1] KONTROLLER
# =============================================================================
def check_problem(name: str) -> Problem:
    """problem.py'nin kurallara uyup uymadığını kontrol eder."""
    try:
        p = Problem(name)
    except Exception as e:
        raise KontrolHatasi(f"Problem('{name}') oluşturulamadı: {e}\n"
                            "  -> _load_data() ve __init__() fonksiyonlarını kontrol edin.")
    if not isinstance(p.dim, (int, np.integer)) or p.dim < 1:
        raise KontrolHatasi(f"problem.dim pozitif bir tam sayı olmalı (şu an: {p.dim!r}).")
    lb, ub = np.asarray(p.lb, float), np.asarray(p.ub, float)
    if lb.shape != (p.dim,) or ub.shape != (p.dim,):
        raise KontrolHatasi(f"lb ve ub uzunluğu dim={p.dim} olmalı "
                            f"(şu an: {lb.shape}, {ub.shape}).")
    if np.any(lb >= ub):
        raise KontrolHatasi("Her değişken için lb < ub olmalı.")
    if name not in MAX_FES:
        raise KontrolHatasi(f"MAX_FES sözlüğünde '{name}' için bütçe tanımlı değil.")
    rng = np.random.default_rng(0)
    for _ in range(5):
        x = lb + rng.random(p.dim) * (ub - lb)
        f = p.evaluate(x)
        if not isinstance(f, (float, np.floating)) or not np.isfinite(f):
            raise KontrolHatasi(f"problem.evaluate(x) sonlu bir float döndürmeli "
                                f"(şu an: {f!r}).\n  -> objective() ve constraints() "
                                "fonksiyonlarında NaN/sonsuz üreten işlemleri kontrol edin.")
        d = p.details(x)
        for key in ("objective", "violation", "feasible"):
            if key not in d:
                raise KontrolHatasi(f"problem.details(x) '{key}' anahtarını içermeli.")
    return p


def check_algorithm(alg_name: str, func, params: dict, problem: Problem) -> None:
    """Bir algoritmanın kurallara uyup uymadığını küçük bir bütçeyle kontrol eder."""
    budget = 600
    try:
        r1 = func(problem, budget, 123, **params)
        r2 = func(problem, budget, 123, **params)
    except NotImplementedError as e:
        raise KontrolHatasi(f"Algoritma henüz tamamlanmamış: {e}")
    except TypeError as e:
        raise KontrolHatasi(f"Fonksiyon çağrılamadı: {e}\n  -> İmza şöyle olmalı: "
                            f"def {func.__name__}(problem, max_fes, seed, ...) ve "
                            "ALGORITHMS'deki parametre adları fonksiyondakilerle aynı olmalı.")
    except Exception:
        raise KontrolHatasi("Algoritma çalışırken hata verdi:\n" + traceback.format_exc())

    if not isinstance(r1, dict) or not REQUIRED_KEYS.issubset(r1):
        eksik = REQUIRED_KEYS - set(r1 if isinstance(r1, dict) else [])
        raise KontrolHatasi(f"Dönüş değeri bir sözlük olmalı ve şu anahtarları içermeli: "
                            f"{sorted(REQUIRED_KEYS)} (eksik: {sorted(eksik)}).")
    if r1["n_fes"] > budget:
        raise KontrolHatasi(f"FE bütçesi aşıldı: {r1['n_fes']} > {budget}.\n"
                            "  -> Her değerlendirmeden önce 'if fes >= max_fes: break' kontrolü yapın.")
    if r1["n_fes"] < budget:
        raise KontrolHatasi(f"Bütçenin tamamı kullanılmadı: {r1['n_fes']} < {budget}.\n"
                            "  -> Ana döngü koşulu 'while fes < max_fes' olmalı.")
    bx = np.asarray(r1["best_x"], dtype=float)
    if bx.shape != (problem.dim,):
        raise KontrolHatasi(f"best_x uzunluğu {problem.dim} olmalı (şu an: {bx.shape}).")
    if np.any(bx < problem.lb - 1e-12) or np.any(bx > problem.ub + 1e-12):
        raise KontrolHatasi("best_x sınırların dışında.\n"
                            "  -> Her yeni çözümü değerlendirmeden önce np.clip(x, lb, ub) uygulayın.")
    f_check = problem.evaluate(bx)
    if not np.isclose(f_check, r1["best_f"], rtol=1e-9, atol=1e-12):
        raise KontrolHatasi(f"best_f ({r1['best_f']}) ile problem.evaluate(best_x) "
                            f"({f_check}) uyuşmuyor.\n  -> En iyi çözümü (A) bölümündeki "
                            "evaluate() yardımcısı tutmalı; (D) bölümünü değiştirmeyin.")
    h = r1["history"]
    if len(h) < 2 or h[-1][0] != r1["n_fes"]:
        raise KontrolHatasi("history listesi en az 2 kayıt içermeli ve son kaydın FE değeri "
                            "n_fes'e eşit olmalı.\n  -> (A) bölümündeki evaluate() yardımcısını "
                            "değiştirmeyin.")
    hv = np.array([v for _, v in h], dtype=float)
    if np.any(np.diff(hv) > 1e-12):
        raise KontrolHatasi("history'deki en iyi değerler hiç artmamalı (azalmayan değil, "
                            "artmayan dizi olmalı).")
    if r1["best_f"] != r2["best_f"]:
        raise KontrolHatasi("Aynı tohumla iki koşu farklı sonuç verdi (tekrarlanamaz).\n"
                            "  -> Rastgele sayıları yalnızca rng = np.random.default_rng(seed) "
                            "ile üretin; np.random.rand() veya random modülünü kullanmayın.")


def run_checks() -> dict[str, Problem]:
    print("\n[1] KONTROL")
    hatalar = []
    problems = {}
    for name in INSTANCES:
        try:
            problems[name] = check_problem(name)
            print(f"    problem.py  [{name}] ..................... TAMAM "
                  f"(boyut={problems[name].dim}, maxFEs={MAX_FES[name]})")
        except KontrolHatasi as e:
            hatalar.append(f"problem.py [{name}]: {e}")
    if hatalar:
        _fail(hatalar)

    if len(ALGORITHMS) != 5:
        print(f"    UYARI: ALGORITHMS sözlüğünde {len(ALGORITHMS)} algoritma var; "
              "final projesinde 5 algoritma zorunludur.")
    first = problems[INSTANCES[0]]
    for alg_name, (func, params) in ALGORITHMS.items():
        try:
            check_algorithm(alg_name, func, params, first)
            print(f"    {alg_name:<10} ................................ TAMAM")
        except KontrolHatasi as e:
            hatalar.append(f"{alg_name} ({func.__module__}.py): {e}")
    if hatalar:
        _fail(hatalar)
    return problems


def _fail(hatalar: list[str]) -> None:
    print("\n" + "=" * 78)
    print(" KONTROL BAŞARISIZ — aşağıdaki hataları düzeltip tekrar çalıştırın")
    print("=" * 78)
    for h in hatalar:
        print("\n HATA: " + h)
    sys.exit(1)


# =============================================================================
# [2] DENEYLER
# =============================================================================
def _jsonable(v):
    if isinstance(v, (np.bool_, bool)):
        return bool(v)
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    return v


def _git_provenance() -> dict:
    """Return the exact Git revision and tracked-worktree cleanliness."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--verify", "HEAD"],
            cwd=ROOT, text=True, encoding="utf-8", stderr=subprocess.DEVNULL,
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=ROOT, text=True, encoding="utf-8", stderr=subprocess.DEVNULL,
        )
        return {"commit": commit, "dirty": bool(status.strip())}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "dirty": None}


def _build_experiment_manifest(n_runs: int) -> dict:
    provenance = _git_provenance()
    return {
        "experiment_commit": provenance["commit"],
        "git_dirty_at_start": provenance["dirty"],
        "n_runs": int(n_runs),
        "seed_base": SEED_BASE,
        "instances": list(INSTANCES),
        "max_fes": dict(MAX_FES),
        "algorithms": list(ALGORITHMS),
        "algorithm_parameters": {
            name: {key: _jsonable(value) for key, value in params.items()}
            for name, (_, params) in ALGORITHMS.items()
        },
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "pandas": pd.__version__,
        },
    }


def _validate_final_experiment_preconditions(n_runs: int, manifest: dict) -> None:
    """Protect the 30-run scientific dataset from ambiguous provenance."""
    if n_runs != N_RUNS:
        return

    if len(ALGORITHMS) != len(FINAL_ALGORITHMS) or set(ALGORITHMS) != set(FINAL_ALGORITHMS):
        raise KontrolHatasi(
            "Final deney için algoritma kaydı tam olarak "
            f"{FINAL_ALGORITHMS} kümesini içermeli; şu an {tuple(ALGORITHMS)}."
        )

    commit = manifest.get("experiment_commit")
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-fA-F]{40}", commit) is None:
        raise KontrolHatasi(
            "Final deney commit SHA'sı okunamadı. Deneyi bir Git checkout içinde çalıştırın."
        )
    if manifest.get("git_dirty_at_start") is not False:
        raise KontrolHatasi(
            "Final 30-run deney temiz bir Git çalışma ağacından başlamalı. "
            "Değişiklikleri commit edin veya pilot için --runs 3 kullanın."
        )


def run_experiments(problems: dict[str, Problem], n_runs: int) -> None:
    print(f"\n[2] DENEY  ({n_runs} koşu)")
    manifest = _build_experiment_manifest(n_runs)
    _validate_final_experiment_preconditions(n_runs, manifest)
    _save_settings(n_runs, manifest)

    for name, p in problems.items():
        out = RAW_DIR / name
        out.mkdir(parents=True, exist_ok=True)
        for alg_name, (func, params) in ALGORITHMS.items():
            rows = []
            t0 = time.perf_counter()
            for k in range(n_runs):
                seed = SEED_BASE + k
                r = func(p, MAX_FES[name], seed, **params)
                det = {key: _jsonable(val) for key, val in p.details(r["best_x"]).items()}
                rows.append({
                    "run": k + 1, "seed": seed,
                    "best_f": float(r["best_f"]),
                    **det,
                    "n_fes": int(r["n_fes"]), "time": float(r["time"]),
                    "best_x": json.dumps(np.asarray(r["best_x"], float).tolist()),
                    "history_fes": json.dumps([int(a) for a, _ in r["history"]]),
                    "history_f": json.dumps([float(b) for _, b in r["history"]]),
                })
                print(f"\r    {name:<14} {alg_name:<8} koşu {k + 1:>3}/{n_runs}", end="")
            pd.DataFrame(rows).to_csv(out / f"{alg_name}.csv", index=False)
            print(f"   ({time.perf_counter() - t0:.1f} s)")


def _save_settings(n_runs: int, manifest: dict) -> None:
    """Persist both paper settings and machine-readable experiment provenance."""
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    rows = [{"Algoritma": a, "Parametreler": json.dumps(prm, ensure_ascii=False)}
            for a, (_, prm) in ALGORITHMS.items()]
    pd.DataFrame(rows).to_csv(TAB_DIR / "parametre_ayarlari.csv", index=False)

    with open(TAB_DIR / "deney_ayarlari.json", "w", encoding="utf-8") as fp:
        json.dump({"N_RUNS": n_runs, "SEED_BASE": SEED_BASE, "ALPHA": ALPHA,
                   "INSTANCES": INSTANCES, "MAX_FES": MAX_FES}, fp,
                  ensure_ascii=False, indent=2)

    with open(TAB_DIR / "experiment_manifest.json", "w", encoding="utf-8") as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=2, sort_keys=True)


# =============================================================================
# [3] ANALİZ
# =============================================================================
def run_analysis() -> None:
    print("\n[3] ANALİZ")
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    for name in INSTANCES:
        try:
            res = st.load_results(name, RAW_DIR)
        except FileNotFoundError as e:
            print(f"    {name}: {e}")
            continue
        res = {a: res[a] for a in res if a in ALGORITHMS} or res
        print(f"\n    --- {name} ---  algoritmalar: {', '.join(res)}")

        desc = st.descriptive_table(res)
        desc.to_csv(TAB_DIR / f"{name}_istatistikler.csv", float_format="%.10g")
        with pd.option_context("display.float_format", "{:.6g}".format,
                               "display.width", 120):
            print(desc.to_string())

        vz.plot_convergence(res, name, out_dir=FIG_DIR)
        vz.plot_boxplot(res, name, out_dir=FIG_DIR)

        if len(res) >= 2:
            wt = st.wilcoxon_table(res, alpha=ALPHA)
            wt.to_csv(TAB_DIR / f"{name}_wilcoxon.csv", index=False, float_format="%.4g")
            print("\n" + wt.to_string(index=False))
        if len(res) >= 3:
            fr = st.friedman_test(res)
            st.friedman_table(fr).to_csv(TAB_DIR / f"{name}_friedman.csv", float_format="%.4g")
            print(f"\n    Friedman: chi2 = {fr['statistic']:.3f}, p = {fr['p_value']:.3g}")
            if fr["p_value"] < ALPHA:
                cd = st.nemenyi_cd(fr["k"], fr["n_blocks"], alpha=ALPHA)
                vz.plot_cd_diagram(fr["mean_ranks"], cd, name, out_dir=FIG_DIR)
        else:
            print("    (Friedman testi ve CD diyagramı için en az 3 algoritma gerekir.)")
    print(f"\n    Tablolar : {TAB_DIR}\n    Grafikler: {FIG_DIR}")


# =============================================================================
def main() -> None:
    ap = argparse.ArgumentParser(description="YMM4142 final projesi deney çalıştırıcı")
    ap.add_argument("--runs", type=int, default=N_RUNS, help="koşu sayısı (varsayılan 30)")
    ap.add_argument("--check", action="store_true", help="yalnızca kontrolleri çalıştır")
    ap.add_argument("--only-analysis", action="store_true",
                    help="deneyleri koşturmadan mevcut sonuçları analiz et")
    args = ap.parse_args()

    if args.only_analysis:
        run_analysis()
        return
    problems = run_checks()
    if args.check:
        print("\n    Tüm kontroller başarılı.")
        return
    run_experiments(problems, args.runs)
    run_analysis()
    print("\nTamamlandı.")


if __name__ == "__main__":
    main()
