# Results

Bu dizin yalnız **experiment-freeze sonrası** üretilmiş ve doğrulanmış final bilimsel çıktılar içindir.

Kabul edilen final düzen:
- `raw/<instance>/<algorithm>.csv`
- `tables/experiment_manifest.json`
- `tables/` altında türetilmiş istatistik tabloları
- `figures/` altında ham veriden yeniden üretilebilir şekiller

Kurallar:
- Pre-freeze pilot/smoke sonuçları commit edilmez.
- CSV elle düzeltilmez; hata varsa ilgili seed yeniden çalıştırılır.
- Manifest commit SHA, environment, algoritmalar, parametreler, seed planı ve FE bütçelerini bağlamalıdır.
- Final validator PASS olmadan sonuçlar makaleye alınmaz.
