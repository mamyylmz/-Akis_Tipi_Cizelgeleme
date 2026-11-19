# Tarık — test / deney / istatistik teslim kanıtı

**Branch:** `work/tarik`  
**Taban:** `develop`. RIME kabul edilip `develop` içine alındıktan sonra final 5/5 algoritma registry sözleşmesi çalıştırılabilir.

## Tamamlanan çıktılar

- `docs/experiment_protocol.md`
- `tests/test_contract.py`
- `docs/first_pilot_runs.md`
- `tools/check_experiment_outputs.py`
- Mevcut `src/algorithms/pso.py` kaynakları Kennedy–Eberhart 1995 + Shi–Eberhart 1998 olarak açıkça belirtmektedir.
- Mevcut PSO pre-freeze sonuçları final sonuçlardan ayrılmıştır.

## Kabul kriterleri

Contract testi:
- registry = tam olarak PSO/DE/DBO/RIME/NRBO,
- 73 FE için tüm algoritmalarda gerçek evaluate çağrısı = n_fes = bütçe,
- aynı seed deterministik,
- best_x sınır/şekil/permutation geçerli,
- best_f bağımsız yeniden değerlendirmeyle aynı,
- history son FE ve monotonluk kurallarına uygun,
- maxFEs sözlüğü değişmemiş.

Final sonuç validator:
- 15 CSV,
- her CSV 30 satır,
- toplam 450 koşu,
- seed 2026..2055,
- exact maxFEs,
- feasible/finite,
- best_x ve permutation doğrulaması,
- best_f yeniden hesaplama,
- history bütünlüğü.

## Negatif kararlar

- Pre-freeze PSO 30-run dosyaları final bilimsel veri sayılmaz.
- Eksik algoritmayla 450-run başlatılmaz.
- CSV/p-değerleri elle düzeltilmez.
- Freeze sonrası algoritma/model/veri değişirse ilgili final sonuçlar yeniden üretilir.
- `main.py --check` tek başına nihai kabul değildir.

## Bağımsız inceleme

Burak PSO mekanizmasını ve algoritma sözleşmesini; Şeref model/Cmax kontrollerini; Muhammed deney kapsamı ve freeze politikasını incelemelidir. Üreten kişinin kendi onayı merge için yeterli değildir.
