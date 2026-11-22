# Bağımsız Teknik İnceleme: Şeref'in Modeli ve DE

**18.11.2026 · İnceleyen: Burak (kod/API)** · İncelenen: Şeref · Kapsam: [08_Seref_Modelleme_Teslim_Kaniti.md](../sprintler/08_Seref_Modelleme_Teslim_Kaniti.md)'deki "Burak" kontrol listesi: `src/problem.py`, `src/algorithms/de.py`, ders API sözleşmesi, algoritma kaynak eşlemesi.

İncelenen dosyaların SHA-256 değerleri (git geçmişi yok):

```
1b10abe0dfe77a5ba46a65dc56b166370fc4b7193c6d6ad3dc9929086e5736b9  src/problem.py
6fe35ac3b9a26cadfda0647df17f921d642202e51de65db484d02bec61332f6f  src/algorithms/de.py
34e1c74aea990110afb94202af2e12bf8e863e7e20bd92055cf9691c6525ac44  tests/test_problem.py
c51521f3832885c06d5c8b28f9c1f257c29efe81a3d8be1269857719a12fe287  tests/test_model_validation.py
68164a1350ad2252e224b3fc36872ec65556f04cb6cd6914abaa455910867bf2  data/taillard/ta001.txt
e291f3f94885af40c9b9509cd9e939d66d4455d3611db55b42b3bfb801cf6656  data/taillard/ta011.txt
2fbd5446f94ebb5bfcf81fc0fcc4f5624294bfc4532c7f46354e76e832810f59  data/taillard/ta021.txt
a436211905d950b4c7ab09fd92d9eb50e38c80a0b12d40331bd5c5780e6698f3  data/taillard/reference_solutions.json
```

## 1. Bağımsız olarak yeniden yaptığım kontroller

Şeref'in kodunu ve üretecini (`tools/generate_taillard_instances.py`) **kullanmadan**, kendi yazdığım ayrı bir betikle yaptım: [tools/review_independent_taillard_check.py](../tools/review_independent_taillard_check.py). Çıktı: [23_burak_review_seref_independent.txt](test_logs/23_burak_review_seref_independent.txt).

| Kontrol | Yöntem | Beklenen | Gözlenen | Sonuç |
|---|---|---|---|---|
| Taillard verisi | Taillard (1993) Park–Miller üretecini sıfırdan yazdım; seed'ler 873654221 / 587595453 / 479340445 | Dosyalarla birebir aynı | ta001, ta011, ta021 birebir aynı | PASS |
| Veri yönü | ta001 makine-1'in ilk 5 değeri | 54 83 15 71 77 | 54 83 15 71 77 (dosyada sütun 1) | PASS |
| SHA-256 | Dosyalardan yeniden hesap | Metadata ile aynı | Aynı | PASS |
| Referans permütasyonlar | DP döngüsü yerine olay simülasyonu, ayrıca makine başına çakışma kontrolü | 1278 / 1582 / 2297 | 1278 / 1582 / 2297, çakışma yok | PASS |
| 5×3 örnek | Ayrı bir simülasyon, `(J4,J2,J1,J5,J3)` | 20 | 20 | PASS |
| DE ders sözleşmesi | `main.check_algorithm` (600 FE, seed 123, iki koşu) | TAMAM | TAMAM | PASS |
| Mevcut testler | `python -m unittest discover -s tests` | OK | 38 test OK | PASS |

Kodu okurken doğruladıklarım:
- `decode`: `argsort(kind="stable")`, NaN ya da Inf'i reddediyor.
- `objective`: O(n·m) DP, tekrar eden, eksik ya da aralık dışı işi reddediyor.
- `constraints()` boş dizi döndürüyor.
- `details()` RPD'yi doğru hesaplıyor; permütasyonu 1 tabanlı yazıyor.
- `encode_permutation` ters dönüşümü doğru.
- Testler üretim kodunu 5×3 örnekte ([test_model_validation.py:60-71](../tests/test_model_validation.py#L60-L71)) ve 5×3'ün 120 permütasyonunun hepsinde ayrı bir yolla sınıyor.

**Model ve veri için P0/P1 bulgum yok.**

## 2. Bulgular

```
ID: PFSP-K6-01
Seviye: P2 (P1 adayı: algoritma sadakati; seviyeyi Şeref ve Muhammed belirlesin)
Sorumlu: Şeref       İnceleyen: Burak
Girdi / ortam / dosya: src/algorithms/de.py:77-99 (SHA 6fe35ac3…)
Beklenen davranış: Storn & Price (1997) DE'si nesil tabanlıdır. Mutasyon vektörleri
  x_r1,G, x_r2,G, x_r3,G, G. nesilden alınır. Seçilen deneme vektörü G+1. nesle girer;
  G. nesil o nesil boyunca değişmez.
Gözlenen davranış: X[i] = trial satırı (de.py:98) popülasyonu yerinde güncelliyor.
  Aynı nesilde sonraki bireylerin mutasyonu (de.py:86) güncellenmiş vektörleri
  kullanabiliyor. Bu, asenkron (steady-state) bir DE varyantı.
Kanıt: Kod okuma; de.py:86 X[r1], X[r2], X[r3] okuyor, de.py:98 aynı X'e yazıyor.
  Not: 1997 makalesinin tam metnini bu incelemede açmadım. Nesil tanımı makalenin
  bilinen tanımına dayanıyor.
Kök neden: Mutasyon için neslin başında popülasyonun bir kopyası alınmıyor.
İstenen somut düzeltme: while döngüsünün başında X_gen = X.copy() al; mutasyonda
  X_gen[r1] + F*(X_gen[r2] - X_gen[r3]), çaprazlamada X_gen[i] kullan; seçimi X'e yaz.
  Bütçe neslin ortasında biterse o ana kadarki seçimler geçerli kalır.
  Ya da asenkron davranış bilinçli bir seçimse makalede "asenkron DE" diye yaz.
Tekrar test: tests/test_de.py ve main.py --check yeniden çalışır; ek olarak bir nesil
  içinde mutasyonun yalnızca X_gen'den okuduğunu sınayan bir test.
Durum: AÇIK
```

```
ID: PFSP-K6-02
Seviye: P2
Sorumlu: Şeref       İnceleyen: Burak
Dosya: src/main.py (ALGORITHMS sözlüğü)
Beklenen: DE, beş algoritmadan biri olarak ALGORITHMS'te kayıtlı olmalı.
Gözlenen: DE kayıtlı değil (yalnızca PSO, DBO, NRBO var). DE ders kontrolünü geçiyor
  (yukarıdaki tablo); eklenmesine teknik bir engel yok.
İstenen: from algorithms.de import de ve "DE": (de, {"F": 0.5, "CR": 0.9}) eklensin.
  PFSP-K6-01 kararından sonra eklenmesi daha doğru.
Tekrar test: main.py --check'te DE TAMAM; test_registered_algorithms_use_real_evaluation_budget DE ile geçer.
Durum: AÇIK
```

```
ID: PFSP-K2-01
Seviye: P2
Sorumlu: Şeref       İnceleyen: Burak
Dosya: src/problem.py:68-69
Beklenen: Veri bütünlüğü kontrolü her zaman yapılmalı.
Gözlenen: `if expected_hash and observed_hash != expected_hash` — metadata'da sha256
  alanı yoksa ya da boşsa kontrol sessizce atlanıyor. Şu an üç örneğin de hash'i var,
  yani bugün bir sorun yok.
İstenen: expected_hash yoksa ValueError ver.
Tekrar test: Hash alanı olmayan bir metadata ile Problem("ta001") ValueError verir;
  mevcut testler geçer.
Durum: AÇIK
```

```
ID: PFSP-K6-03
Seviye: P2
Sorumlu: Şeref       İnceleyen: Burak
Dosya: src/algorithms/de.py:50
Gözlenen: N = min(requested_n, max_fes) — bütçe popülasyondan küçükse popülasyon
  sessizce küçülüyor. Ders bütçelerinde (≥ 20.000) etkisi yok; yalnızca küçük
  test bütçelerinde ortaya çıkar.
İstenen: Bu davranışı docstring'e yaz ya da ValueError ver. Ortak arayüz §1 "sessizce
  düzeltilmez" der.
Durum: AÇIK
```

## 3. Gözlem (bulgu değil, ekip kararı gerekiyor)

**Sınırdaki eşit anahtarlar.** `evaluate` önce `clip` uyguluyor, sonra kararlı sıralama yapıyor. Bu model sözleşmesine uygun, hata değil. Ancak ta001'de 5 seed ile tam bütçe denemesinde algoritmaların bulduğu en iyi çözümlerde anahtarların %20–38'i tam 0 ya da 1 değerindeydi. Eşit anahtarların sırasını iş numarası belirliyor; algoritmalar sık sık 1297'de bitiyor. Bu, H2 hipoteziyle ve algoritmalar arası farkın görünürlüğüyle ilgili. Şeref ile Burak'ın 23 Kasım'dan önce bir karara varması gerekiyor: olduğu gibi raporlamak ya da beş algoritmanın hepsinde aynı biçimde sınır işleme yöntemini değiştirmek (yansıtma ya da rastgele yeniden atama).

> **Düzeltme (20.11.2026):** Bu gözlemdeki "algoritmalar 1297'de takılıyor" kısmını eşit anahtarlara bağlamak yanlıştı. 450 koşuluk sınır pilotunda ([boundary_pilot_2026-11-20](experiments/boundary_pilot_2026-11-20/README.md)) eşitlikler tamamen kaldırıldığında da koşuların %84–92'si 1297'de bitti. 1297, ta001'in bir yerel optimumu. Sınırda birikme gerçek, ama bu pilotta çözüm kalitesini anlamlı biçimde etkilemedi (Holm sonrası 0/30, Friedman p = 0,25).

## 4. Karar

- **Model ve veri (`problem.py`, `data/taillard/*`, model testleri): KABUL (Burak'ın kod/API kontrolü).** Tarık'ın bağımsız model/seed/FE kontrolü ve Bilal'in kaynak kontrolü ayrı kapılar; bu karar onların yerine geçmez.
- **DE: DÜZELTME GEREKİYOR (P2).** PFSP-K6-01'in seviyesi Şeref ve Muhammed tarafından netleştirilmeli. PFSP-K6-02 DE'nin beş algoritmalı deneye girmesi için gerekli.

## 5. Düzeltmeler (18.11.2026, Burak tarafından; ekip kararıyla, Şeref'e sonra bildirilecek)

Bulgular, bulguyu yapan kişi (Burak) tarafından düzeltildi. Bu yüzden **kapanış onayını Burak veremez**: Şeref (ya da Tarık) düzeltmeleri incelemeden durumlar KAPALI'ya geçmez.

| ID | Değişiklik | Durum |
|---|---|---|
| PFSP-K6-01 | `de.py`: her neslin başında `X_gen = X.copy()`; mutasyon ve çaprazlama yalnızca `X_gen`'den okuyor, seçim `X`'e yazıyor. Docstring'e nesil tabanlı güncelleme yazıldı | DÜZELTİLDİ / YENİDEN_TEST bekliyor |
| PFSP-K6-02 | `main.py`: `"DE": (de, {"F": 0.5, "CR": 0.9})` eklendi (`pop_size` varsayılanı 5·D = 100) | DÜZELTİLDİ / YENİDEN_TEST bekliyor |
| PFSP-K2-01 | `problem.py`: metadata'da SHA-256 yoksa `ValueError("… SHA-256 missing …")` | DÜZELTİLDİ / YENİDEN_TEST bekliyor |
| PFSP-K6-03 | Davranış değiştirilmedi, docstring'e yazıldı. Gerekçe: `tests/test_model_validation.py`'deki kayıtlı algoritma testi 73 FE ile çalışıyor ve bu küçülmeye dayanıyor. Testi değiştirmek kalite kurallarına aykırı | BELGELENDİ / Şeref kararı |

**Şeref'in test dosyalarına dokunulmadı.** Yeni regresyon testleri ayrı bir dosyada: [tests/test_review_fixes.py](../tests/test_review_fixes.py).
- K6-01 testi DE'yi testin içinde, nesil tabanlı olarak baştan yazıyor ve aynı seed'le birebir aynı sonucu bekliyor (seed 1, 7, 2026).
- Bu testin eski (asenkron) koda karşı **başarısız olduğu** doğrulandı: üç seed'de de eşleşmedi. Yani test iki davranışı gerçekten ayırt ediyor.

**Yeniden test (düzeltilmiş dosyalar üzerinde):**
- `unittest discover`: 41 test OK → [24_burak_review_fixes_unittest_all.txt](test_logs/24_burak_review_fixes_unittest_all.txt).
- `main.py --check`: PSO, DE, DBO, NRBO TAMAM; `problem.py` doğrulaması 1278 / 1582 / 2297 PASS → [25_burak_review_fixes_main_check.txt](test_logs/25_burak_review_fixes_main_check.txt).
- Yeni SHA-256 değerleri: [26_burak_review_fixes_sha256.txt](test_logs/26_burak_review_fixes_sha256.txt). §1'deki hash'ler düzeltme öncesi sürüme ait.

**Not:** DE'nin davranışı değiştiği için, `results/` altında DE ile daha önce üretilmiş bir sonuç varsa artık geçersizdir. Şu an `results/` içinde yalnızca PSO çıktıları var.
