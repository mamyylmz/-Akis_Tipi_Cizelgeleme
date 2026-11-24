# PFSP · PR #5, PSO ve deney hazırlığı durum raporu

**Tarih:** 24.11.2026
**İncelenen dal:** `work/tarik`
**Teknik denetimin başlangıç commit’i:** `c3c2b38f66485370a0dd8104577732ba43a7cf1b`
**Belgelerin ve son kalite kontrollerinin commit’i:** `ad45575b1d5968d0d6b29217d1008fbda07ee17c`
**Durum:** Adım 1 ve 2 tamamlandı. Adım 3 yönetici onayını bekliyor. Adım 4 ve 5 için final deney çıktıları henüz oluşmadı.

## Beş adımın durumu

| Adım | Durum | Yapılan işlem veya bekleme nedeni |
| --- | --- | --- |
| 1 · PR #5 teknik kararı | Tamamlandı | DBO/NRBO akademik P1 kapanışı 23 Kasım tarihli yönetici kaydından doğrulandı. Algoritma sözleşmesi 4/4, manifest 4/4 ve CSV doğrulayıcısı 7/7 geçti. Yerel teknik kapsam için `P0=0 / P1=0 — KABUL` işlendi. GitHub PR birleştirme ve uzak CI sonucu teyit edilmedi. |
| 2 · PSO yöntem metni | Tamamlandı | Başlatma, hız ve konum denklemleri, güncelleme sırası, sınır yönetimi ve FE hesabı Python koduyla eşleştirildi. Atalet ağırlığı için Shi ve Eberhart (1998) kaynağı eklendi. FE tabanlı zamanlama proje uyarlaması olarak belgelendi. |
| 3 · 45 koşuluk dry-run | Başlatılmadı | Yönetici method-freeze’in henüz onaylanmadığını bildirdi ve dry-run’ı başlatmama talimatı verdi. Bildirilen develop HEAD `a37ef0e241517a446355a58869a14837fa7427bf` freeze olarak kullanılmadı. Onaylı METHOD-FREEZE SHA gerekli. |
| 4 · 450 final koşu | Başlatılmadı | Dry-run ve validator başarısı, ardından EXPERIMENT-FREEZE onayı gerekiyor. Final CSV veya deney manifesti üretilmedi. |
| 5 · Validator, istatistik ve grafik | Araçlar hazır, final uygulama bekliyor | Mevcut validator testleri geçti. Final CSV doğrulaması, Wilcoxon sıra toplamı + Holm, Friedman ve koşula bağlı Nemenyi ile yakınsama ve kutu grafikleri 450 koşunun doğrulanmış ham çıktılarıyla üretilecek. Bu aşamada final tablo, p-değeri veya grafik üretilmedi. |

[PR #5 teknik kaydı](https://github.com/mamyylmz/-Akis_Tipi_Cizelgeleme/blob/ad45575b1d5968d0d6b29217d1008fbda07ee17c/docs/quality_status.md) · [PSO yöntem metni](https://github.com/mamyylmz/-Akis_Tipi_Cizelgeleme/blob/ad45575b1d5968d0d6b29217d1008fbda07ee17c/paper/method_pso.md) · [Shi ve Eberhart, 1998](https://doi.org/10.1109/ICEC.1998.699146)

## PSO kod ve metin eşleştirmesi

| Parametre | Doğrulanan değer | Kod kaynağı |
| --- | --- | --- |
| `pop_size` | 30 | `src/main.py` PSO kaydı |
| `w_max` | 0.9 | Çalıştırıcı kaydı |
| `w_min` | 0.4 | Çalıştırıcı kaydı |
| `c1` | 2.0 | Çalıştırıcı kaydı |
| `c2` | 2.0 | Çalıştırıcı kaydı |
| `v_frac` | 0.2 | `src/algorithms/pso.py` fonksiyon varsayılanı |

Atalet ağırlığı dış tur başında `w_max − (w_max − w_min) × fes / max_fes` ile hesaplanır ve o tur boyunca sabit kalır. İlk güncelleme başlangıç sürüsünün değerlendirilmesinden sonra yapılır. PFSP anahtar uzayında hız bileşenleri [−0,2, 0,2], konum bileşenleri [0, 1] aralığına kırpılır.

## Çalıştırılan kalite kontrolleri

| Komut | Sonuç |
| --- | --- |
| `python -B -m unittest discover -s tests` | 90/90 başarılı. |
| `python -B src/main.py --check` | Üç benchmark, beş algoritma başarılı. |
| `python -B src/problem.py` | Referans Cmax 1278, 1582, 2297. |
| `python -B tools/run_neh_baseline.py` | NEH Cmax 1286, 1680, 2410. |
| `python -B tools/check_repo_integrity.py` | Başarılı, benchmark hash’leri ve yerel bağlantılar dahil. |
| `python -B docs/check_literature.py` | Başarılı, mevcut makale yapısı ve kaynakça kontrolleri dahil. |

Kontroller `work/tarik` commit’inde çalıştırıldı. Bu kanıt, yeni bir develop SHA’sının yönetici tarafından freeze olarak onaylandığı anlamına gelmez.

## Devam kapıları

1. Yönetici **METHOD-FREEZE SHA** kaydını açıkça onaylamalı. Sadece onaylı sürümde 5 algoritma × 3 benchmark × 3 seed dry-run çalıştırılır. Beklenen değerler **15 CSV, 45 koşu, seed 2026–2028 ve 1.350.000 FE**. Manifest aynı freeze SHA’yı kaydetmeli ve validator tamamen geçmeli.
2. Başarılı dry-run ardından **EXPERIMENT-FREEZE** onayı gerekir. Temiz checkout, beş algoritma, üç benchmark hash’i ve değiştirilmemiş FE bütçeleri denetlenir. Final ölçütleri **15 CSV, 450 koşu, seed 2026–2055 ve 13.500.000 FE**.
3. Final CSV’ler elle değiştirilmeden proje içi validator ile doğrulanır. Wilcoxon sıra toplamı + Holm ve Friedman sonuçları doğrulanmış veriden üretilir. Protokol uyarınca Nemenyi, Friedman anlamlıysa uygulanır. Yakınsama ve kutu grafikleri aynı sonuç verisine bağlanır.

Raporun yerel kopyası ayrı results dizininde saklanır. Repo kopyası docs altındadır. Repo results dizini freeze sonrasındaki bilimsel çıktılara ayrılmıştır.
