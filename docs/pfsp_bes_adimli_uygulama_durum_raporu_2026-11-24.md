# PFSP · PR #5, PSO ve deney durumu

**Tarih:** 24.11.2026
**İncelenen dal:** `work/tarik`
**Çıktıların yayımlandığı commit:** `17973e6575084c4b92cbd561097a7fb4930b6d39`
**Durum:** Deney çıktıları mevcut; merge öncesi validator düzeltmesi bağımsız inceleme bekliyor. Güncel kabul kararı [kalite durumunda](quality_status.md), aktif görevler [Tarık work listesinde](../worklists/tarik.md) tutulur.

## Beş adımın durumu

| Adım | Durum | Kanıt ve sınır |
| --- | --- | --- |
| 1 · PR #5 teknik kararı | Önceki sürüm kabul edildi | `c3c2b38f66485370a0dd8104577732ba43a7cf1b` için tarihsel P0=0/P1=0 kararı kalite belgesindedir. Birleştirme commit'i `a37ef0e241517a446355a58869a14837fa7427bf`. Bu kabul yeni düzeltmenin bağımsız incelemesi değildir. |
| 2 · PSO yöntem metni | Mevcut | [Yöntem metni](../paper/method_pso.md), çalıştırıcı ve manifest aynı parametreleri kullanır. Atalet ağırlığı kaynağı yayıncı özeti düzeyinde doğrulanmıştır; FE zamanlaması ve parametre seçimi proje uygulamasıdır. |
| 3 · 45 koşuluk dry-run | Kanıt mevcut | [Pilot paket](evidence/method-freeze-dry-run-df8ac61/README.md): method-freeze `df8ac616165dc0105c83429e5ed000f34045aafa`, 15 CSV / 45 koşu / 1.350.000 FE. Final results verisinden ayrı. |
| 4 · 450 final koşu | Çıktılar mevcut | [Manifest](../results/tables/experiment_manifest.json): `73ce39c78a6263ce6f252267edeff0515157aca1`, temiz başlangıç, seed 2026–2055, 15 CSV / 450 koşu / 13.500.000 FE. |
| 5 · Validator, istatistik ve grafik | Düzeltme inceleme bekliyor | [Deney doğrulama kaydı](../results/verification.json), 9 istatistik tablosu ve 18 grafik mevcut. Validator düzeltmesi sonrası öz kontrol 450/450 ve ilgili testler 14/14 başarılı; yeni sürümün bağımsız kabulü beklenir. |

## PSO parametreleri

`pop_size=30`, `w_max=0.9`, `w_min=0.4`, `c1=2.0`, `c2=2.0`, `v_frac=0.2`: çalıştırıcı, fonksiyon varsayılanları, yöntem metni ve manifest ile eşleşir. FE tabanlı ağırlık dış tur başında hesaplanır; hız [−0.2, 0.2], konum [0, 1] aralığındadır.

## Düzeltme ve yeniden kontrol

Validator, FE değerlerini `int()` ile keserek kabul ediyordu. Sonlu tam sayı kontrolü ve kesirli/NaN/Inf/boolean history FE regresyonları eklendi. Yerel benchmark dosyaları, Git'te kayıtlı LF biçimine getirildi; beklenen SHA'lar veya sayısal veriler değiştirilmedi. PSO açıklamasındaki bütün parametreleri kaynak önerisi sayan ifade kaldırıldı.

Bağımsız incelemeci şu kontrolleri yeni sürümde yeniden çalıştırmalı:

```text
python -B -m unittest tests/test_experiment_manifest.py tests/test_experiment_validation.py tests/test_statistical_gate.py -v
python -B tools/check_experiment_outputs.py --raw-dir results/raw --runs 30 --seed-base 2026
python -B tools/check_repo_integrity.py
python -B docs/check_literature.py
```

Deneyin özgün manifesti ve verification kaydı değiştirilmedi. Düzeltme algoritma davranışını, problem modelini veya sayısal benchmark verisini değiştirmez. Bu rapor yönetici freeze/merge onayının yerine geçmez.
