# PFSP — Akış Tipi Çizelgeleme

YMM4142 Optimizasyon Teorisi Problem 7 için Permütasyon Akış Tipi Çizelgeleme Problemi (PFSP) çalışma deposu. Amaç makespan / Cmax minimizasyonudur.

## Güncel durum

- Beş meta-sezgisel `develop` üzerinde entegre: DE, PSO, DBO, RIME, NRBO.
- Zorunlu Taillard örnekleri: ta001, ta011, ta021.
- Final deney protokolü: 5 × 3 × 30 = 450 koşu, toplam 13.500.000 FE.
- Final 450 koşu henüz üretilmedi.
- NEH klasik referans sezgiseli ve üç Taillard sonucu hazır. [Yöntem ve sonuçlar](paper/support/neh_baseline.md).
- DBO/NRBO için özgün makale-denklem ↔ kod eşleştirmesi proje düzeyinde açık P1'dir.
- Tarık'ın deney/validator geliştirmeleri PR #5 üzerindedir ve akademik P1 kapanışını beklemektedir.

Güncel iş dağılımı: [worklists/](worklists/README.md).  
Makale hazırlık durumu: [paper/STATUS.md](paper/STATUS.md).  
Kalite durumu: [docs/quality_status.md](docs/quality_status.md).

## Repo yapısı

| Yol | Amaç |
|---|---|
| `src/` | PFSP modeli, algoritmalar, deney ve analiz kodu |
| `tests/` | model, algoritma ve sözleşme testleri |
| `data/taillard/` | doğrulanmış benchmark dosyaları ve referans metadata |
| `paper/` | makale taslakları, yöntem metinleri ve destek materyali |
| `docs/` | güncel proje standardı, Git akışı, kalite ve dergi kuralları |
| `worklists/` | yalnız güncel kişisel görev listeleri |
| `results/` | yalnız experiment-freeze sonrası doğrulanmış bilimsel çıktılar |
| `tools/` | yeniden üretim ve bağımsız doğrulama araçları |

## Temel kontroller

```bash
python -m unittest discover -s tests -v
python src/problem.py
python src/main.py --check
python docs/check_literature.py
python tools/check_repo_integrity.py
```

`main.py --check` tek başına bilimsel kabul değildir.

## Branch akışı

- `work/<isim>`: kişisel geliştirme
- `develop`: bağımsız kontrolden geçen entegrasyon
- `main`: yalnız milestone/final kabul edilmiş sürüm

Normal akış: `work/<isim> -> PR -> develop -> final kalite kapısı -> main`.

`main` geçmişinde 22 Kasım'da doğrudan yapılmış iki audit commit'i ve bunların revert commit'leri vardır. Geçmiş yeniden yazılmayacaktır; finalde `develop -> main` PR ile uzlaştırılacaktır.

## Results politikası

Pre-freeze smoke/pilot sonuçları repoda tutulmaz. `results/` yalnız sabitlenmiş deney commit'inden üretilmiş, manifest ile bağlanmış ve validator kapısından geçmiş final sonuçları içerir. Pilot kanıtlar CI loglarında veya Git geçmişinde kalır.
