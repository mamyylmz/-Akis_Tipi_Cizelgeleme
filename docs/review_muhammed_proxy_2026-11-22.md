# Muhammed — Şeref/Tarık görevleri vekil teknik ön-denetimi

**Tarih:** 22.11.2026  
**Amaç:** Şeref ve Tarık'a atanmış teknik kontrol listelerini, onların kişisel onayıymış gibi göstermeden proje yöneticisi tarafından yeniden uygulamak.

## Şeref kapsamı — DBO/NRBO matematik ve kaynak

- DBO θ=90°/180° davranışı: proje kodunun "hareket yok" kararı, yayımlanmış DBO yöntem açıklamasındaki özel açı kuralıyla uyumlu. Yazar MATLAB demosunda koruma ataması sonraki tanjant satırıyla ezildiği için demo koduyla metin arasında çelişki var; makale davranışı seçildi ve açıkça belgelendi.
- DBO R katsayısı: özgün iterasyon oranı yerine `fes/max_fes` kullanımı kaynak-identik davranış diye sunulmuyor; eşit-FE proje uyarlamasıdır.
- NRBO delta: aynı biçimde FE-bütçeli açık proje uyarlamasıdır.
- NRBO a1/a2 çekiliş sırası: gereksiz sapma kaldırıldı; artık boyut başına a1 ardından a2 sırasını `rng.random((D,2))` ile tüketir.
- NRBO payda davranışı: yazar kodunda epsilon guard yoktur. 0/0 ve ±near-zero testleri sonlu/sınır içi değerlendirme sözleşmesini doğrular.

## Tarık kapsamı — Windows, seed, FE ve contract

Gerçek GitHub Actions Windows Server 2025 + Ubuntu matrisinde:
- `core.autocrlf=true` Windows checkout,
- Taillard LF ve SHA bütünlüğü,
- full unittest,
- `python src/problem.py`,
- `python src/main.py --check`
çalıştırılmaktadır.

İlk Windows koşusunda bulunan `UnicodeEncodeError`, `PYTHONUTF8=1` ile CI seviyesinde düzeltildi.

RIME için birleşik ağaçta:
- exact FE,
- same-seed reproducibility,
- seed propagation,
- bounds/finite candidates,
- best_f re-evaluation,
- permutation,
- monotonic history,
- 5/5 registry
kontrolleri uygulanmıştır.

## Deney altyapısı P1 kapıları

Dört yönetici P1'i için:
1. otomatik experiment manifest + clean-Git final kapısı,
2. seed invariant düzeltmesi,
3. strict feasible parsing,
4. objective/cmax/rpd/permutation/violation yeniden doğrulaması
kod ve regresyon testleriyle ele alınmıştır.

## Kabul notu

Bu dosya **vekil teknik ön-denetimdir**. Nihai insan kontrolü Tarık tarafından güncel birleşik commit üzerinde tekrar yapılacak. Tarık P0/P1 bulursa düzeltip aynı test paketini yeniden çalıştırmadan final kabul verilmeyecek.
