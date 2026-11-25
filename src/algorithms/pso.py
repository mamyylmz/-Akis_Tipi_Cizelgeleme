# -*- coding: utf-8 -*-
"""
===============================================================================
 YMM4142 - Optimizasyon Teorisi | 2026-2027 Güz Yarıyılı | Final Projesi
 Ders Sorumlusu: Doç. Dr. Abdullah ELEN
-------------------------------------------------------------------------------
 pso.py  —  ÖRNEK ALGORİTMA: Parçacık Sürü Optimizasyonu (PSO)
===============================================================================

Bu dosya, beş algoritmanızı (GÖREV 2) nasıl yazmanız gerektiğini gösteren
TAM ve ÇALIŞAN bir örnektir. Dosya tek başına çalışır; projedeki hiçbir dosyaya
bağımlı değildir. Deneyin:

        python src/algorithms/pso.py

Kendi algoritmanızı yazarken "sablon_algoritma.py" dosyasını kopyalayıp
algoritmanızın kısa adıyla kaydedin (ör. dbo.py) ve bu dosyayı örnek alın.
PSO, grubunuzun seçtiği beş algoritmadan biriyse bu dosyayı olduğu gibi
kullanabilirsiniz.

-------------------------------------------------------------------------------
 HER ALGORİTMANIN UYMASI GEREKEN KURALLAR (main.py bunları kontrol eder)
-------------------------------------------------------------------------------
 1. Dosyada, dosya adıyla aynı isimde bir fonksiyon bulunur:
        def pso(problem, max_fes, seed, **parametreler) -> dict

 2. Problemden yalnızca şunlar kullanılır:
        problem.dim, problem.lb, problem.ub, problem.evaluate(x)
    problem.evaluate(x) tek bir sayı döndürür; KÜÇÜK olan İYİDİR.
    Kısıtlar bu sayının içinde (ceza olarak) zaten vardır; algoritmada kısıt
    kontrolü YAPILMAZ.

 3. problem.evaluate() her çağrıldığında FE sayacı (fes) 1 artırılır ve
    fes == max_fes olduğunda algoritma DURUR. Döngü koşulu iterasyon sayısı
    değil, FE sayısıdır. Bütçe popülasyonun ortasında bitebilir; bu yüzden
    her değerlendirmeden önce bütçe kontrol edilir.

 4. Rastgele sayılar YALNIZCA şu nesneden üretilir:
        rng = np.random.default_rng(seed)
    np.random.rand(), random.random() gibi kullanımlar YASAKTIR. Aksi hâlde
    aynı tohumla iki koşu farklı sonuç verir ve deneyleriniz tekrarlanamaz.

 5. Üretilen her yeni çözüm, değerlendirilmeden önce sınırlar içine alınır:
        x = np.clip(x, lb, ub)

 6. Fonksiyon şu anahtarlara sahip bir sözlük döndürür:
        "best_x"  : bulunan en iyi çözüm (numpy dizisi, uzunluğu dim)
        "best_f"  : en iyi çözümün uygunluk değeri (float)
        "history" : yakınsama kaydı, [(fes, o_ana_kadarki_en_iyi_f), ...]
                    yaklaşık 100 noktada kaydedilir; SON eleman (max_fes, best_f)
        "n_fes"   : kullanılan toplam FE sayısı (max_fes'i aşamaz)
        "time"    : çalışma süresi (saniye)

 7. Fonksiyon ekrana bir şey yazdırmaz ve dosyaya bir şey kaydetmez.
    Kayıt işlemleri main.py'nin görevidir.

-------------------------------------------------------------------------------
 KAYNAKLAR
-------------------------------------------------------------------------------
 [1] J. Kennedy and R. Eberhart, "Particle swarm optimization," in Proc. IEEE
     Int. Conf. Neural Networks, Perth, Australia, 1995, pp. 1942-1948.
 [2] Y. Shi and R. Eberhart, "A modified particle swarm optimizer," in Proc.
     IEEE Int. Conf. Evolutionary Computation, Anchorage, AK, USA, 1998,
     pp. 69-73.
"""

import time

import numpy as np


def pso(problem, max_fes, seed, pop_size=30, w_max=0.9, w_min=0.4,
        c1=2.0, c2=2.0, v_frac=0.2):
    """Parçacık Sürü Optimizasyonu (doğrusal azalan atalet ağırlıklı sürüm).

    Args:
        problem  : problem.py içindeki Problem nesnesi.
        max_fes  : Amaç fonksiyonu değerlendirme bütçesi.
        seed     : Rastgele tohum (main.py her koşuya farklı bir tohum verir).
        pop_size : Sürüdeki parçacık sayısı.
        w_max    : Başlangıç atalet ağırlığı.
        w_min    : Bitiş atalet ağırlığı.
        c1       : Bilişsel katsayı (parçacığın kendi en iyisine çekimi).
        c2       : Sosyal katsayı (sürünün en iyisine çekimi).
        v_frac   : Hız sınırının arama aralığına oranı: v_max = v_frac*(ub-lb).

        Varsayılan parametre değerleri proje uygulamasının ayarlarıdır;
        tamamının [1] ve [2]'de önerildiği iddia edilmez. [2]'nin yayıncı
        özeti atalet ağırlığının tanıtılmasını doğrular; FE tabanlı doğrusal
        zamanlama projeye özgü uyarlamadır.
        Deneylerde kullanılan değerler main.py'deki ALGORITHMS sözlüğünden
        gelir ve makalenin "Parametre Ayarları" tablosunda aynen raporlanır.

    Returns:
        dict: "best_x", "best_f", "history", "n_fes", "time" anahtarlı sözlük.
    """
    t0 = time.perf_counter()

    # =========================================================================
    # (A) HAZIRLIK  —  her algoritmada aynıdır, DEĞİŞTİRMEYİN
    # =========================================================================
    rng = np.random.default_rng(seed)          # TEK rastgelelik kaynağı
    D = problem.dim
    lb = np.asarray(problem.lb, dtype=float)
    ub = np.asarray(problem.ub, dtype=float)

    fes = 0                                    # FE sayacı
    best_x = None                              # o ana kadarki en iyi çözüm
    best_f = np.inf                            # o ana kadarki en iyi değer
    history = []                               # yakınsama kaydı
    log_every = max(1, max_fes // 100)         # yaklaşık 100 kayıt noktası

    def evaluate(x):
        """Tek bir çözümü değerlendirir; FE sayacını, en iyi çözümü ve
        yakınsama kaydını günceller. Algoritma içinde problem.evaluate()
        DOĞRUDAN çağrılmaz, her zaman bu yardımcı fonksiyon kullanılır."""
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

    # Parçacık konumları arama uzayında düzgün dağılımla rastgele başlatılır.
    X = lb + rng.random((N, D)) * (ub - lb)

    # Hızlar ve hız sınırı. Hız sınırı, parçacıkların bir adımda arama uzayının
    # dışına "fırlamasını" engeller.
    v_max = v_frac * (ub - lb)
    V = rng.uniform(-v_max, v_max, size=(N, D))

    # Başlangıç sürüsünün değerlendirilmesi. Her değerlendirmeden önce bütçe
    # kontrol edilir; değerlendirilemeyen bireyler +sonsuz değerde kalır.
    F = np.full(N, np.inf)
    for i in range(N):
        if fes >= max_fes:
            break
        F[i] = evaluate(X[i])

    # Kişisel en iyiler (pbest) ve sürünün en iyisi (gbest).
    P = X.copy()                               # her parçacığın en iyi konumu
    PF = F.copy()                              # bu konumların değerleri
    g = int(np.argmin(PF))                     # en iyi parçacığın indeksi

    # =========================================================================
    # (C) ANA DÖNGÜ  —  döngü koşulu (fes < max_fes) DEĞİŞTİRİLMEZ
    # =========================================================================
    while fes < max_fes:

        # Atalet ağırlığı İTERASYONA göre değil, harcanan FE ORANINA göre
        # doğrusal olarak azalır. Böylece bütçe ne olursa olsun keşiften
        # (büyük w) sömürüye (küçük w) geçiş aynı oranda gerçekleşir.
        # FE tabanlı bu zamanlama proje uyarlamasıdır.
        # NOT: Kendi algoritmanızda iterasyon sayısına bağlı parametreler varsa
        # (ör. GWO'daki "a" katsayısı, t/T oranı) aynı şekilde fes/max_fes
        # oranını kullanın.
        w = w_max - (w_max - w_min) * fes / max_fes

        for i in range(N):
            if fes >= max_fes:                 # bütçe sürünün ortasında bitebilir
                break

            # Hız güncellemesi [1], [2]:
            #   v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
            r1 = rng.random(D)
            r2 = rng.random(D)
            V[i] = (w * V[i]
                    + c1 * r1 * (P[i] - X[i])      # bilişsel bileşen
                    + c2 * r2 * (P[g] - X[i]))     # sosyal bileşen
            V[i] = np.clip(V[i], -v_max, v_max)

            # Konum güncellemesi ve sınır kontrolü (KURAL 5)
            X[i] = np.clip(X[i] + V[i], lb, ub)

            # Değerlendirme (KURAL 3: her zaman evaluate() üzerinden)
            f = evaluate(X[i])

            # pbest ve gbest güncellemesi (küçük = iyi)
            if f < PF[i]:
                P[i] = X[i].copy()
                PF[i] = f
                if f < PF[g]:
                    g = i

    # =========================================================================
    # (D) SONUÇ  —  her algoritmada aynıdır, DEĞİŞTİRMEYİN
    # =========================================================================
    return {
        "best_x": best_x,
        "best_f": best_f,
        "history": history,
        "n_fes": fes,
        "time": time.perf_counter() - t0,
    }


# =============================================================================
# TEK BAŞINA DENEME:   python src/algorithms/pso.py
# -----------------------------------------------------------------------------
# Algoritmanızı, projenin problemi hazır olmadan önce basit bir test fonksiyonu
# üzerinde deneyebilirsiniz. Gerçek deneyler yalnızca main.py ile yapılır.
# =============================================================================
if __name__ == "__main__":

    class Kure:
        """Test problemi: min sum(x^2), -5 <= x <= 5. Bilinen optimum: f* = 0."""
        dim = 10
        lb = np.full(10, -5.0)
        ub = np.full(10, 5.0)

        def evaluate(self, x):
            return float(np.sum(x ** 2))

    r1 = pso(Kure(), max_fes=10_000, seed=1)
    r2 = pso(Kure(), max_fes=10_000, seed=1)       # aynı tohum
    r3 = pso(Kure(), max_fes=10_000, seed=2)       # farklı tohum

    print(f"En iyi değer        : {r1['best_f']:.6e}   (optimum 0)")
    print(f"Kullanılan FE       : {r1['n_fes']} / 10000")
    print(f"Yakınsama kayıtları : {len(r1['history'])}   son: {r1['history'][-1]}")
    print(f"Süre                : {r1['time']:.3f} s")
    print(f"Tekrarlanabilir mi  : {r1['best_f'] == r2['best_f']}   (aynı tohum -> aynı sonuç olmalı)")
    print(f"Farklı tohum        : {r3['best_f']:.6e}")
