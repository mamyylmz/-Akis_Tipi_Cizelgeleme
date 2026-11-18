# Şeref Rolü — K1/K2/M3/DE Teslim Kanıtı

**Tarih:** 18.11.2026  
**Fiilî üretim:** Bu sprintte Şeref'e atanmış teknik işler proje yöneticisinin kararıyla ekip adına hazırlanmıştır.  
**Durum:** **ÜRETİM TAMAM / OTOMATİK VE ÇİFT-HESAP DOĞRULAMA PASS / FORMAL EKİP ÇAPRAZ İNCELEMESİ BEKLİYOR**

## Görev / çıktı

| Görev | Çıktı | Durum |
|---|---|---|
| K1 Taillard veri derleme | `data/taillard/ta001.txt`, `ta011.txt`, `ta021.txt`, `reference_solutions.json`, `data/README.md`, generator | PASS |
| K2 PFSP model | `src/problem.py` | PASS |
| K2 bağımsız testler | `tests/test_problem.py` | 8/8 PASS |
| M3 model metodu | `paper/method_model.md` | PASS |
| K6 DE hazırlık/uygulama | `src/algorithms/de.py`, `tests/test_de.py` | 2/2 PASS |
| Veri provenance/hash | `data/README.md`, `docs/test_logs/08_sha256.txt` | PASS |
| Doğrulama raporu | `docs/model_validation_report_2026-11-18.md` | PASS |

## Kritik kabul kanıtları

- 5×3 örnek `(J4,J2,J1,J5,J3)` → **Cmax=20**: PASS.
- ta001 resmî üretim matrisi anchor kontrolü: PASS.
- ta001 yayımlanmış referans permütasyonu → **1278**: PASS.
- ta011 yayımlanmış referans permütasyonu → **1582**: PASS.
- ta021 yayımlanmış referans permütasyonu → **2297**: PASS.
- 75 rastgele permütasyonda üretim Cmax vs bağımsız 2-B DP: 75/75 PASS.
- Stable random-key decode ve geçersiz permütasyon ret testleri: PASS.
- DE exact FE, same-seed repeatability, bounds, history ve ortak API: PASS.
- Kurs `main.py --check`: model + PSO PASS; yalnızca 1/5 algoritma kayıtlı olduğuna dair beklenen uyarı var.
- Entegrasyon `--runs 1` smoke testi geçici kopyada PASS; bu tek koşular nihai bilimsel sonuç değildir ve repoya sonuç olarak alınmamıştır.

## Açık bulgular

### P0
Yok.

### P1
**Formal insan çapraz incelemesi henüz yapılmadı.** Önceden belirlenen süreç gereği Burak kod/API'yi, Tarık bağımsız model/seed/FE'yi, Bilal kaynak/provenance ifadesini kontrol etmelidir. Bu eksiklik üretim kodunu değiştirmeyi gerektiren bir hata değildir; süreç kapısıdır ve ekip üyelerinin adına sahte PASS yazılmamıştır.

### P2
Yok.

## Bağımsız incelemeciler için değiştirilmeyecek kontrol listesi

**Burak:** `src/problem.py`, `src/algorithms/de.py`, ders API sözleşmesi, algoritma kaynak eşlemesi.  
**Tarık:** `python -m unittest discover -s tests -v`, `python src/problem.py`, FE/seed/`best_x` yeniden hesaplama.  
**Bilal:** `data/README.md`, kaynak URL/DOI, 2026-06-03 BKS sayfası, makale metnindeki Cmax/RPD terminolojisi.

İnceleme sonrası hata bulunursa mevcut testler değiştirilmez; üretim dosyası düzeltilir ve bütün regresyon testleri tekrar çalıştırılır.
