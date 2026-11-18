# PFSP Model ve Veri Doğrulama Raporu — 18.11.2026

**Kapsam:** Şeref rolüne ait K1 (veri), K2 (problem modeli), M3 model metodu ve DE teknik hazırlığı.  
**Durum:** Üretim ve otomatik/çift-hesap doğrulaması tamamlandı. Formal ekip üyesi bağımsız incelemesi ayrıca yapılmalıdır.

## 1. Kaynaklar

- Taillard üretim algoritması ve tohumlar: <https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/flowshop2.txt>
- Taillard güncel sınırlar ve yayımlanmış referans permütasyonlar: <https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/flowshop.dir/best_lb_up.txt>
- Taillard 1993 DOI: `10.1016/0377-2217(93)90182-M`
- DE 1997 DOI: `10.1023/A:1008202821328`
- Kaynak erişim tarihi: 18.11.2026. Taillard sınır sayfası güncellemesi: 03.06.2026.

## 2. Veri üretimi ve bütünlük

Üç zorunlu örnek OR-Library `flowshop2.txt` içindeki özgün Park–Miller üretici ve tohumlarla deterministik üretilmiştir. Üretim sırası özgün prosedürde makine→iş; depoda saklama yönü iş→makinedir.

| Örnek | Tohum | Boyut | SHA-256 |
|---|---:|---:|---|
| ta001 | 873654221 | 20×5 | `68164a1350ad2252e224b3fc36872ec65556f04cb6cd6914abaa455910867bf2` |
| ta011 | 587595453 | 20×10 | `e291f3f94885af40c9b9509cd9e939d66d4455d3611db55b42b3bfb801cf6656` |
| ta021 | 479340445 | 20×20 | `2fbd5446f94ebb5bfcf81fc0fcc4f5624294bfc4532c7f46354e76e832810f59` |

`ta001` üretimi, OR-Library'nin aynı dosyada yayımladığı 5×20 doğrulama matrisiyle birebir karşılaştırılmıştır: **PASS**.

`src/problem.py` yükleme sırasında veri dosyası SHA-256 değerini `reference_solutions.json` ile karşılaştırır; dosya değişirse sessizce devam etmez.

## 3. 5×3 küçük örnek — bağımsız hesap

Resmî Problem 7 belgesindeki iş süreleri ve `(J4,J2,J1,J5,J3)` sırası kullanılmıştır. Üretim kodundan bağımsız 2-B DP tamamlanma matrisi:

```text
[[ 1,  5,  7],
 [ 3,  8, 12],
 [ 6, 12, 14],
 [ 9, 14, 17],
 [13, 15, 20]]
```

**Cmax = 20 — PASS.** Ayrıntılı kayıt: `docs/test_logs/09_small_example_independent_schedule.txt`.

## 4. Taillard referans permütasyon doğrulaması

Taillard güncel dosyasındaki 1-tabanlı permütasyonlar `reference_solutions.json` içine hem 1- hem 0-tabanlı olarak kaydedilmiştir. `problem.py` bu permütasyonları sabit Cmax döndürmeden normal hesap yolundan geçirir.

| Örnek | Referans permütasyon (1-tabanlı) | Beklenen | Üretim Cmax | Bağımsız 2-B DP | Sonuç |
|---|---|---:|---:|---:|---|
| ta001 | 3 17 15 8 9 6 5 14 16 7 11 13 18 19 1 4 2 10 20 12 | 1278 | 1278 | 1278 | PASS |
| ta011 | 18 5 2 12 9 10 4 14 15 17 13 3 6 19 8 20 11 7 1 16 | 1582 | 1582 | 1582 | PASS |
| ta021 | 16 18 14 7 13 8 15 9 6 20 17 12 10 11 5 1 2 4 3 19 | 2297 | 2297 | 2297 | PASS |

Ek olarak her üç örnekte 25'er rastgele permütasyon üretim `objective()` hesabı ve testteki bağımsız 2-B DP ile karşılaştırılmıştır: **75/75 eşleşme — PASS**.

## 5. Random-key ve geçersiz girdi kontrolleri

- `decode(x) = np.argsort(x, kind="stable")`.
- Eşit anahtarlar deterministik sırayı korur: PASS.
- Decode eksiksiz 0…n−1 permütasyonu üretir: PASS.
- Tekrarlı, eksik ve aralık dışı doğrudan permütasyonlar `objective()` tarafından reddedilir: PASS.
- Arama sınırı `[0,1]^n`; `clip()` boyut kontrolü yapar.
- PFSP için ek kısıt/ceza yoktur; `constraints()` boş dizi döndürür.

## 6. FE bütçeleri ve RPD

`INSTANCES = [ta001, ta011, ta021]`. `MAX_FES` sırasıyla 20.000, 30.000, 40.000'dir. `details()` Cmax yanında

`RPD = 100 * (Cmax - Cref) / Cref`

hesabını döndürür. Üç referans permütasyonda RPD = 0: PASS.

## 7. DE doğrulaması

`src/algorithms/de.py`, Storn–Price `DE/rand/1/bin` stratejisini ortak API ile uygular.

- Randomness: yalnızca `np.random.default_rng(seed)`.
- Mutasyon: `x_r1 + F*(x_r2-x_r3)`.
- Binom çaprazlama ve zorunlu `j_rand` bileşeni.
- Açgözlü seçim.
- Her `problem.evaluate()` çağrısı FE sayılır; exact `max_fes` kullanım testi PASS.
- Aynı seed aynı `best_x` ve `best_f`: PASS.
- `main.py` içindeki değiştirilmemiş `check_algorithm()` fonksiyonuyla DE sözleşmesi: PASS.
- Başlangıç parametreleri: `NP=5D`, `F=0.5`, `CR=0.9`; Taillard örneklerine göre tune edilmemiştir.

DE henüz `main.py::ALGORITHMS` içine eklenmemiştir. Bu bilinçli olarak entegrasyon aşamasına bırakılmıştır; `main.py` şu anda yalnızca ders paketindeki PSO'yu kayıtlı gösterir.

## 8. Çalıştırılan testler

| Komut | Sonuç |
|---|---|
| `python tools/generate_taillard_instances.py` | PASS; deterministik üretim ve ta001 resmî anchor kontrolü |
| `python -m unittest discover -s tests -v` | **10/10 PASS** |
| `python src/problem.py` | ta001/ta011/ta021 referans doğrulaması PASS |
| `python src/main.py --check` | Problem üç örnekte PASS; PSO PASS; 5 algoritma henüz olmadığı için beklenen uyarı |
| `main.check_algorithm(DE, ...)` | PASS |
| `python docs/check_literature.py` | PASS; yerel bağlantılar ve Bilal literatür yapısal kontrolleri korunuyor |
| `python src/main.py --runs 1` | Ayrı geçici kopyada entegrasyon smoke testi PASS; sonuçlar nihai deney olarak repoya alınmadı |

Tam çıktı kayıtları `docs/test_logs/` altındadır.

## 9. Kapsam sınırı

Bu rapor **PFSP veri/model/DE teknik çıktısını** doğrular. Diğer dört algoritmanın tamamlanması, beş algoritmanın `main.py` entegrasyonu, 30×5×3 nihai koşu, Wilcoxon/Friedman/Nemenyi analizleri ve final makale sonuçları bu raporla tamamlanmış sayılmaz.

Formal ekip kontrol planına göre Burak kod/API, Tarık bağımsız model/seed/FE, Bilal kaynak biçimi incelemesini yapmalıdır. Bu rapor onların adına sahte bir onay üretmez.
