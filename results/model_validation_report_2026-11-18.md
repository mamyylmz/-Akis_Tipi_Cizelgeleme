# Bağımsız PFSP model doğrulama raporu

**Tarih:** 18.11.2026  
**Görev / sahip:** PFSP modelinin bağımsız test edilmesi / Tarık  
**Ortam:** Windows, Python 3.11.9, NumPy 2.2.6

## Değişen dosyalar ve sürüm

- [tests/test_model_validation.py](../tests/test_model_validation.py) — Beş ayrı `unittest` senaryosu.
- [results/model_validation_report_2026-11-18.md](model_validation_report_2026-11-18.md) — Teslim ve terminal kaydı.

| Dosya | SHA-256 |
| --- | --- |
| `tests/test_model_validation.py` | `b3a379e037e358d3f19db1f268379b40d34bbadf03aa5e5c4fbc7564c505414c` |
| `src/problem.py` | `1b10abe0dfe77a5ba46a65dc56b166370fc4b7193c6d6ad3dc9929086e5736b9` |
| `data/taillard/reference_solutions.json` | `a436211905d950b4c7ab09fd92d9eb50e38c80a0b12d40331bd5c5780e6698f3` |

## Beklenen ve gözlenen sonuçlar

| Senaryo | Beklenen | Gözlenen | Durum |
| --- | --- | --- | --- |
| Veri okuma | ta001 20×5, ta011 20×10, ta021 20×20. Hücreler 1–99 arası tam sayı, dosya SHA-256 değerleri dokümana uygun. | Üç dosyanın başlığı, satır ve sütun sayısı ile SHA-256 değerleri eşleşti. Modelin okuduğu her hücre dosyadan bağımsız okunan karşılığıyla aynı. | PASSED |
| Geçerli permütasyon | Her iş bir kez bulunmalı. Eksik veya tekrarlayan işler reddedilmeli. | ta011 çıktısında 20 iş birer kez yer aldı. Raporlanan 1 tabanlı sıra, decode edilen 0 tabanlı sırayla uyumlu. Eksik ve tekrarlı girişler `ValueError` üretti. | PASSED |
| 5 iş × 3 makine | J4, J2, J1, J5, J3 için Cmax = 20. | Proje örneği test verisi olarak yüklendi. Modelin `objective` ve `evaluate` sonuçları ile bağımsız 2 boyutlu dinamik programlama 20 verdi. | PASSED |
| ta001 referansı | Projedeki referans sırasıyla Cmax = 1278. Referans eksikse SKIPPED. | İki indeks gösterimi aynı sırayı verdi. Model ve bağımsız hesap 1278 üretti. Dosya ve permütasyon eksikliği ayrı ayrı simüle edildiğinde SKIPPED görüldü. | PASSED |
| Determinizm | Sabit anahtarlar, eşit anahtarlar dahil, aynı sıra ve Cmax üretmeli. | Üç örneğin her birinde 5 tekrarda sıra, Cmax ve `details` çıktısı birebir eşleşti. Sıra ve Cmax bağımsız hesapla da doğrulandı. | PASSED |

Referans sırası (1 tabanlı): `3 17 15 8 9 6 5 14 16 7 11 13 18 19 1 4 2 10 20 12`. Kaynak kaydı ve benchmark dosyalarının SHA-256 değerleri için [veri README’si](../data/README.md) ve [referans metadata’sı](../data/taillard/reference_solutions.json).

## Komutlar ve terminal çıktısı

```text
> python -B tests/test_model_validation.py
> python -B -m unittest discover -s tests -v
test_data_loading (__main__.TestIndependentModelValidation.test_data_loading) ... ok
test_determinism (__main__.TestIndependentModelValidation.test_determinism) ... ok
test_documented_five_jobs_three_machines (__main__.TestIndependentModelValidation.test_documented_five_jobs_three_machines) ... ok
test_ta001_reference_makespan (__main__.TestIndependentModelValidation.test_ta001_reference_makespan) ... ok
test_valid_permutation (__main__.TestIndependentModelValidation.test_valid_permutation) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.075s

OK
test_contract_budget_and_reproducibility_on_pfsp (test_de.TestDifferentialEvolution.test_contract_budget_and_reproducibility_on_pfsp) ... ok
test_default_population_rule_is_compatible_with_20_job_problem (test_de.TestDifferentialEvolution.test_default_population_rule_is_compatible_with_20_job_problem) ... ok
test_data_loading (test_model_validation.TestIndependentModelValidation.test_data_loading) ... ok
test_determinism (test_model_validation.TestIndependentModelValidation.test_determinism) ... ok
test_documented_five_jobs_three_machines (test_model_validation.TestIndependentModelValidation.test_documented_five_jobs_three_machines) ... ok
test_ta001_reference_makespan (test_model_validation.TestIndependentModelValidation.test_ta001_reference_makespan) ... ok
test_valid_permutation (test_model_validation.TestIndependentModelValidation.test_valid_permutation) ... ok
test_invalid_permutations_are_rejected (test_problem.TestPFSPProblem.test_invalid_permutations_are_rejected) ... ok
test_metadata_reference_permutations_are_complete (test_problem.TestPFSPProblem.test_metadata_reference_permutations_are_complete) ... ok
test_production_and_independent_makespan_match_random_permutations (test_problem.TestPFSPProblem.test_production_and_independent_makespan_match_random_permutations) ... ok
test_reference_permutations_recompute_published_values (test_problem.TestPFSPProblem.test_reference_permutations_recompute_published_values) ... ok
test_required_instance_dimensions_and_budgets (test_problem.TestPFSPProblem.test_required_instance_dimensions_and_budgets) ... ok
test_small_documented_example_is_20 (test_problem.TestPFSPProblem.test_small_documented_example_is_20) ... ok
test_stable_random_key_decode_is_valid_and_deterministic (test_problem.TestPFSPProblem.test_stable_random_key_decode_is_valid_and_deterministic) ... ok
test_ta001_matches_or_library_published_verification_matrix (test_problem.TestPFSPProblem.test_ta001_matches_or_library_published_verification_matrix) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.265s

OK
```

Referans eksikliği, yalnızca ta001 referans senaryosunda `Path.read_text` çağrısı bellek içi `unittest.mock.patch` ile değiştirilerek denendi. İlk denemede `FileNotFoundError`, ikinci denemede yalnızca `bks` alanını içeren JSON kullanıldı.

```text
test_ta001_reference_makespan (test_model_validation.TestIndependentModelValidation.test_ta001_reference_makespan) ... skipped 'Doğrulama Bekliyor (Referans permütasyon henüz temin edilmedi)'

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK (skipped=1)
test_ta001_reference_makespan (test_model_validation.TestIndependentModelValidation.test_ta001_reference_makespan) ... skipped 'Doğrulama Bekliyor (Referans permütasyon henüz temin edilmedi)'

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK (skipped=1)
missing file: SKIPPED
missing permutation: SKIPPED
```

```text
> python -B src/main.py --check
[1] KONTROL
    problem.py  [ta001] ..................... TAMAM (boyut=20, maxFEs=20000)
    problem.py  [ta011] ..................... TAMAM (boyut=20, maxFEs=30000)
    problem.py  [ta021] ..................... TAMAM (boyut=20, maxFEs=40000)
    UYARI: ALGORITHMS sözlüğünde 1 algoritma var; final projesinde 5 algoritma zorunludur.
    PSO        ................................ TAMAM

    Tüm kontroller başarılı.
```

## Kabul durumu

- **Otomatik doğrulama:** 5/5 yeni senaryo ve 15/15 tam paket başarılı. Eksik referans için iki deneme de beklenen atlama durumunu verdi.
- **Bağımsız ekip denetçisi:** BEKLİYOR. Kabul için ekip denetçisinin aynı sürümde en az bir kritik kontrolü yeniden çalıştırıp sonucu kaydetmesi gerekiyor.
- **Açık konular:** Bu çalıştırmada model senaryoları P0/P1 bulgusu üretmedi. Ders çalıştırıcısı genel proje kapsamında beş algoritmadan birinin kayıtlı olduğunu bildirdi. README ve AGENTS’ta adı geçen `docs/NEGATIF_KOMUTLAR_VE_KALITE_KARARLARI.md` yerine depoda bulunan `docs/KALITE_KARARLARI.md` esas alındı.
- **Nihai durum:** Modelin otomatik doğrulaması tamamlandı. Ekip kabulü bekliyor.


## İkinci aşama · Sınır, kısıt ve entegrasyon doğrulaması

**Tarih:** 18.11.2026  
**Değişen dosyalar:** [tests/test_model_validation.py](../tests/test_model_validation.py) ve bu rapor. Yukarıdaki SHA-256 kaydı ilk aşamaya aittir.  
**İkinci aşama test dosyası SHA-256:** `385f38ee25bc1598c27ed38c1bb205c5bd8879cb19c37e48f10d99244db8614f`

İncelemede ortak kılavuzun §9–14 hükümleri, sprint kabul ölçütleri, [yöntem metni](../paper/method_model.md), [Gantt tablosu](../docs/gantt_plan.md) ve çalıştırıcı sözleşmesi esas alındı. Kılavuzda 50 ve 100 işli örnekler isteğe bağlı veya ek çalışma olarak tanımlanıyor. Bu çalışmada `data/` altında doğrulanmış üç zorunlu örnek bulundu.

| Senaryo | Beklenen ve gözlenen sonuç |
| --- | --- |
| Sınır boyutları ve eşit süreler | 1×1 için 1, 1×3 için 199, 3×1 için iki sırada 142. Eşit süreli 3×4 matrisinde iki sırada 594, 20×20 matrisinde 3861. Model ve beklenen değerler eşleşti. |
| Hatalı benchmark biçimi | Boş dosya, yanlış başlık/boyut, eksik/fazla satır veya hücre, tam sayı olmayan süre ve aralık dışı süreler için beklenen `ValueError` alındı. Geçerli hash ile biçim kontrollerine ulaşıldı. Süre sınırları 1 ve 99 kabul edildi, 0 ve 100 reddedildi. |
| Dosya bütünlüğü ve bozuk referans | Eksik dosya `FileNotFoundError` üretti. Hash ve boyut uyuşmazlıkları ile tekrarlı, eksik veya aralık dışı referans indeksleri `ValueError` üretti. |
| Geçersiz permütasyon | Eksik, tekrarlı, negatif, aralık dışı, kesirli ve yanlış şekilli sıralar `objective`, `constraints` ve `encode_permutation` tarafından reddedildi. |
| Random-key hataları | Yanlış şekil ve NaN üç giriş noktasında da reddedildi. Sonsuz değerler `decode` tarafından reddedildi. `evaluate` ve `details` aynı değerleri kırpma sonrası kabul etti. Bu son test gözlenen davranışı kaydeder. |
| Tam çizelge ve kısıtlar | Belgelenmiş 5×3 örneğinde 15 operasyon ve 2×2 örneğinde dört operasyon için bağımsız başlangıç ve bitiş tabloları elle hesaplanan değerlerle eşleşti. Makinede çakışma, iş önceliği, ortak sıra ve ilk/ara/son boşluklar kontrol edildi. Her makinede işlem ve boşta kalma toplamı sırasıyla 20 ve 8 olan Cmax değerlerine eşitti. Üretim modelinin karşılaştırılabilir çıktısı Cmax, operasyon tablosu ise bağımsız test hesabından geliyor. |
| 5×3 örneğinin bütün permütasyonları | 120 sıranın her birinde model Cmax değeri makine bazlı bağımsız hesapla eşleşti. Birden fazla farklı Cmax gözlendi. |
| API, fizibilite ve RPD | Üç zorunlu örnekte referans ve doğal iş sırası için encode/decode, `evaluate`, `details` ve RPD formülü uyumlu. Geçerli sıralarda kısıt vektörü boş, ihlal 0 ve `feasible=True`. |
| Kayıtlı algoritma entegrasyonu | PSO, seed 20261118 ile iki koşuda 73 çağrı yaptı ve `n_fes=73` bildirdi. En iyi sıra, bağımsız Cmax ve yakınsama geçmişi tutarlı. Mevcut DE testleri regresyon paketinde geçti. |

### Performans gözlemi

Windows 10, AMD64 Family 25 Model 80, Python 3.11.9 ve NumPy 2.2.6. Her işlem bir kez ısıtıldı. Süre, `timeit.repeat(number=100, repeat=5)` ile alınan beş grubun çağrı başına medyanıdır. Bellek, ayrı bir tek çağrı için `tracemalloc` tepe değeridir ve süreç RSS’i ölçülmedi. Değerlendirmede referans permütasyonunun sabit random-key vektörü, yüklemede model kurucusu kullanıldı. Proje belgelerinde sayısal kabul eşiği bulunmadığından sonuçlar gözlem olarak kaydedildi.

| Örnek | Yükleme, µs | Yükleme tepe, B | Değerlendirme, µs | Değerlendirme tepe, B |
| --- | ---: | ---: | ---: | ---: |
| ta001 (20×5) | 427,15 | 15026 | 62,51 | 6128 |
| ta011 (20×10) | 507,54 | 15026 | 103,09 | 6128 |
| ta021 (20×20) | 619,36 | 15026 | 200,33 | 6128 |

### Tekrarlanabilir komutlar ve sonuçlar

- `python -B tests/test_model_validation.py` → 15 test, tamamı başarılı (5 ilk aşama, 10 ikinci aşama).
- `python -B -m unittest discover -s tests -v` → 25 test, tamamı başarılı.

```text
test_contract_budget_and_reproducibility_on_pfsp (test_de.TestDifferentialEvolution.test_contract_budget_and_reproducibility_on_pfsp) ... ok
test_default_population_rule_is_compatible_with_20_job_problem (test_de.TestDifferentialEvolution.test_default_population_rule_is_compatible_with_20_job_problem) ... ok
test_data_loading (test_model_validation.TestIndependentModelValidation.test_data_loading) ... ok
test_determinism (test_model_validation.TestIndependentModelValidation.test_determinism) ... ok
test_documented_five_jobs_three_machines (test_model_validation.TestIndependentModelValidation.test_documented_five_jobs_three_machines) ... ok
test_ta001_reference_makespan (test_model_validation.TestIndependentModelValidation.test_ta001_reference_makespan) ... ok
test_valid_permutation (test_model_validation.TestIndependentModelValidation.test_valid_permutation) ... ok
test_all_small_instance_permutations (test_model_validation.TestSecondStageModelValidation.test_all_small_instance_permutations) ... ok
test_benchmark_integrity_and_reference_errors (test_model_validation.TestSecondStageModelValidation.test_benchmark_integrity_and_reference_errors) ... ok
test_course_api_and_rpd (test_model_validation.TestSecondStageModelValidation.test_course_api_and_rpd) ... ok
test_infinite_random_keys_follow_current_clipping_behavior (test_model_validation.TestSecondStageModelValidation.test_infinite_random_keys_follow_current_clipping_behavior) ... ok
test_invalid_permutations_across_public_methods (test_model_validation.TestSecondStageModelValidation.test_invalid_permutations_across_public_methods) ... ok
test_malformed_benchmark_files (test_model_validation.TestSecondStageModelValidation.test_malformed_benchmark_files) ... ok
test_objective_boundary_dimensions_and_equal_times (test_model_validation.TestSecondStageModelValidation.test_objective_boundary_dimensions_and_equal_times) ... ok
test_random_key_shape_and_nan_errors (test_model_validation.TestSecondStageModelValidation.test_random_key_shape_and_nan_errors) ... ok
test_registered_algorithms_use_real_evaluation_budget (test_model_validation.TestSecondStageModelValidation.test_registered_algorithms_use_real_evaluation_budget) ... ok
test_schedule_against_hand_calculated_operations (test_model_validation.TestSecondStageModelValidation.test_schedule_against_hand_calculated_operations) ... ok
test_invalid_permutations_are_rejected (test_problem.TestPFSPProblem.test_invalid_permutations_are_rejected) ... ok
test_metadata_reference_permutations_are_complete (test_problem.TestPFSPProblem.test_metadata_reference_permutations_are_complete) ... ok
test_production_and_independent_makespan_match_random_permutations (test_problem.TestPFSPProblem.test_production_and_independent_makespan_match_random_permutations) ... ok
test_reference_permutations_recompute_published_values (test_problem.TestPFSPProblem.test_reference_permutations_recompute_published_values) ... ok
test_required_instance_dimensions_and_budgets (test_problem.TestPFSPProblem.test_required_instance_dimensions_and_budgets) ... ok
test_small_documented_example_is_20 (test_problem.TestPFSPProblem.test_small_documented_example_is_20) ... ok
test_stable_random_key_decode_is_valid_and_deterministic (test_problem.TestPFSPProblem.test_stable_random_key_decode_is_valid_and_deterministic) ... ok
test_ta001_matches_or_library_published_verification_matrix (test_problem.TestPFSPProblem.test_ta001_matches_or_library_published_verification_matrix) ... ok

----------------------------------------------------------------------
Ran 25 tests in 1.927s

OK
```

```text
> python -B src/main.py --check
[1] KONTROL
    problem.py  [ta001] ..................... TAMAM (boyut=20, maxFEs=20000)
    problem.py  [ta011] ..................... TAMAM (boyut=20, maxFEs=30000)
    problem.py  [ta021] ..................... TAMAM (boyut=20, maxFEs=40000)
    UYARI: ALGORITHMS sözlüğünde 1 algoritma var; final projesinde 5 algoritma zorunludur.
    PSO        ................................ TAMAM

    Tüm kontroller başarılı.
```

### Açık konular ve kabul durumu

- **Model sözleşmesi:** Sonlu anahtar koşulunun `evaluate` ve `details` için de geçerli olması istenirse, sonsuz anahtarların kırpma öncesinde reddedilmesi için ayrı bir düzeltme ve doğrulama gerekir. Genel amaçlı sıfır süre desteği ile `int64`/`float` hassasiyet sınırlarının ötesindeki sayısal aralık için proje sözleşmesi bekleniyor.
- **Ölçeklenebilirlik ve Gantt:** Depodaki veri ile ölçüm 20×20’ye kadar yapıldı. Üretim kodunda operasyon başlangıç/bitiş tablosu üreten bir fonksiyon tespit edilmedi. Kısıt kanıtı bağımsız çizelgeye ve model Cmax karşılaştırmasına dayanıyor.
- **Proje entegrasyonu:** Çalıştırıcıda yalnız PSO kayıtlı. Beş algoritmalı entegrasyon kabulü için kayıt tamamlandıktan sonra bu kontrol yeniden yapılmalı.
- **Kabul:** İkinci aşama otomatik doğrulaması tamamlandı. Bağımsız ekip denetçisinin aynı sürümde kritik bir kontrolü yeniden çalıştırması bekleniyor.
