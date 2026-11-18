# -*- coding: utf-8 -*-
"""
===============================================================================
 YMM4142 - Optimizasyon Teorisi | 2026-2027 Güz Yarıyılı | Final Projesi
 ALGORİTMA ŞABLONU   (GÖREV 2: her algoritma sorumlusu bu dosyayı kopyalar)
===============================================================================

NASIL KULLANILIR?
  1. Bu dosyayı kopyalayıp algoritmanızın kısa adıyla, küçük harflerle kaydedin:
         src/algorithms/dbo.py
  2. Fonksiyonun adını DOSYA ADIYLA AYNI yapın:   def dbo(problem, max_fes, seed, ...)
  3. Algoritmanın parametrelerini fonksiyonun argümanları olarak, özgün
     makaledeki varsayılan değerleriyle ekleyin.
  4. (B) ve (C) bölümlerini özgün makaleye göre doldurun. Her güncelleme
     denkleminin yanına makaledeki denklem numarasını yorum olarak yazın.
  5. (A) ve (D) bölümlerine DOKUNMAYIN.
  6. "python src/algorithms/dbo.py" ile tek başına deneyin.
  7. main.py'deki ALGORITHMS sözlüğüne algoritmanızı ekleyin.

Kurallar ve dönüş değerinin açıklaması için pso.py dosyasının başındaki
"HER ALGORİTMANIN UYMASI GEREKEN KURALLAR" bölümünü mutlaka okuyun.

KAYNAK (özgün makale — zorunlu):
  [1] [Yazarlar], "[Makale başlığı]," [Dergi], vol. [x], pp. [x-y], [Yıl],
      doi: [DOI].
"""

import time

import numpy as np


def sablon_algoritma(problem, max_fes, seed, pop_size=30):
    """[Algoritmanın tam adı (KISALTMA)] — [Yazar, Yıl].

    Args:
        problem  : problem.py içindeki Problem nesnesi.
        max_fes  : Amaç fonksiyonu değerlendirme bütçesi.
        seed     : Rastgele tohum.
        pop_size : Popülasyon büyüklüğü.
        [diğer parametreler ve anlamları]

    Returns:
        dict: "best_x", "best_f", "history", "n_fes", "time" anahtarlı sözlük.
    """
    t0 = time.perf_counter()

    # =========================================================================
    # (A) HAZIRLIK  —  DEĞİŞTİRMEYİN
    # =========================================================================
    rng = np.random.default_rng(seed)
    D = problem.dim
    lb = np.asarray(problem.lb, dtype=float)
    ub = np.asarray(problem.ub, dtype=float)

    fes = 0
    best_x = None
    best_f = np.inf
    history = []
    log_every = max(1, max_fes // 100)

    def evaluate(x):
        nonlocal fes, best_x, best_f
        f = float(problem.evaluate(x))
        fes += 1
        if f < best_f:
            best_f, best_x = f, x.copy()
        if fes % log_every == 0 or fes == max_fes:
            history.append((fes, best_f))
        return f

    # =========================================================================
    # (B) BAŞLATMA  —  ALGORİTMAYA ÖZGÜ
    # =========================================================================
    N = pop_size
    X = lb + rng.random((N, D)) * (ub - lb)        # rastgele başlangıç popülasyonu
    F = np.full(N, np.inf)
    for i in range(N):
        if fes >= max_fes:
            break
        F[i] = evaluate(X[i])

    # TODO: Algoritmanızın başlangıçta ihtiyaç duyduğu diğer yapılar
    #       (ör. en iyi/en kötü bireyler, hafıza, alt popülasyonlar).

    # =========================================================================
    # (C) ANA DÖNGÜ  —  ALGORİTMAYA ÖZGÜ (döngü koşulu DEĞİŞTİRİLMEZ)
    # =========================================================================
    while fes < max_fes:

        # İterasyona bağlı parametreler için t/T yerine fes/max_fes kullanın:
        oran = fes / max_fes                        # 0'dan 1'e ilerler

        for i in range(N):
            if fes >= max_fes:
                break

            # TODO: Özgün makaledeki güncelleme denklemleriyle yeni çözümü üretin.
            #       Rastgele sayıları YALNIZCA rng ile üretin: rng.random(D),
            #       rng.normal(...), rng.integers(...)
            raise NotImplementedError("sablon_algoritma: (C) bölümünü doldurun.")
            x_yeni = X[i]                           # Denklem (x)

            x_yeni = np.clip(x_yeni, lb, ub)        # sınır kontrolü (zorunlu)
            f_yeni = evaluate(x_yeni)               # değerlendirme (zorunlu)

            # TODO: Seçim / güncelleme kuralı (ör. açgözlü seçim):
            if f_yeni < F[i]:
                X[i], F[i] = x_yeni, f_yeni

    # =========================================================================
    # (D) SONUÇ  —  DEĞİŞTİRMEYİN
    # =========================================================================
    return {
        "best_x": best_x,
        "best_f": best_f,
        "history": history,
        "n_fes": fes,
        "time": time.perf_counter() - t0,
    }


if __name__ == "__main__":

    class Kure:
        dim = 10
        lb = np.full(10, -5.0)
        ub = np.full(10, 5.0)

        def evaluate(self, x):
            return float(np.sum(x ** 2))

    r1 = sablon_algoritma(Kure(), max_fes=10_000, seed=1)
    r2 = sablon_algoritma(Kure(), max_fes=10_000, seed=1)
    print(f"En iyi değer       : {r1['best_f']:.6e}   (optimum 0)")
    print(f"Kullanılan FE      : {r1['n_fes']} / 10000")
    print(f"Tekrarlanabilir mi : {r1['best_f'] == r2['best_f']}")
