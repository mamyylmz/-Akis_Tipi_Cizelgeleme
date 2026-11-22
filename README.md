# PFSP — Akış Tipi Çizelgeleme Çalışma Alanı

Amaç, Permütasyon Akış Tipi Çizelgeleme Probleminde **makespan (Cmax) minimizasyonudur**. Depo artık hem araştırma/makale belgelerini hem de ders şablonuna dayalı teknik model altyapısını içerir.

## Başlangıç

1. [Ortak proje ve makale kılavuzu](docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md)
2. [Negatif komutlar ve kalite kararları](docs/KALITE_KARARLARI.md)
3. [Ekip planı](sprintler/00_EKIP_ILK_SPRINT_VE_3_ARALIK_PLANI.md)
4. [Makale iskeleti](paper/outline.md) ve [kaynak denetimi](paper/source_audit.md)
5. [Bilal teslim kanıtı](sprintler/07_Bilal_Literatur_Teslim_Kaniti.md)
6. [Şeref/modelleme teslim kanıtı](sprintler/08_Seref_Modelleme_Teslim_Kaniti.md)
7. [Model doğrulama raporu](docs/model_validation_report_2026-11-18.md)

## Teknik yapı

| Yol | İçerik |
|---|---|
| `src/problem.py` | PFSP modeli, random-key decode, Cmax, RPD ve veri doğrulama |
| `src/algorithms/de.py` | DE/rand/1/bin uygulaması; Şeref'in algoritma çıktısı |
| `src/algorithms/pso.py` | Ders paketindeki PSO örneği |
| `src/main.py` | Ders paketindeki deney çalıştırıcı; beş zorunlu algoritma kayıtlıdır |
| `tests/test_problem.py` | Veri, decode, bağımsız Cmax ve referans permütasyon testleri |
| `tests/test_de.py` | DE FE/seed/API testleri |
| `data/taillard/` | ta001, ta011, ta021 ve referans çözüm metadata'sı |
| `tools/generate_taillard_instances.py` | Resmî tohumlardan deterministik veri üretimi |
| `paper/` | Literatür ve makale çalışma dosyaları |
| `docs/` | Ortak standart, dergi, Gantt, kalite ve doğrulama kayıtları |
| `sprintler/` | Sprint atamaları ve teslim kanıtları |

## Temel kontroller

```bash
python tools/generate_taillard_instances.py
python -m unittest discover -s tests -v
python src/problem.py
python src/main.py --check
python docs/check_literature.py
```

`python src/main.py --check` **tek başına final kabul değildir**. Bağımsız algoritma sözleşmesi ve deney çıktısı doğrulaması da çalıştırılır.

## Deney sonuçları hakkında uyarı

Depodaki `results/` nihai 30 koşuluk deneyler tamamlanana kadar bilimsel sonuç kaynağı değildir. Tek koşuluk smoke testler geçici kopyada çalıştırılır ve repoya nihai sonuç olarak yazılmaz.

Önceki PSO smoke çıktıları `docs/test_logs/legacy_pso_smoke/` altında tarihsel kanıt olarak saklanır. Yeni deneyi boş bir çıktı dizinine yazmak için `python -B src/main.py --runs 1 --output-dir <dizin>` kullanılır. Aynı çıktı dizini için `--only-analysis --output-dir <dizin>` manifesti ve tüm ham CSV'leri doğrular.