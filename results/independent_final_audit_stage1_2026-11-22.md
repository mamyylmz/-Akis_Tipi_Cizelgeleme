# Bağımsız son kontrol · Aşama 1 hata ve çözüm raporu

**Tarih:** 22.11.2026
**İncelenen başlangıç SHA:** `9ac8f92fc3282ab2f03aacb80b783f0024299ac5`
**Karar:** **DÜZELTME_GEREKİYOR** · **P0 = 3, P1 = 3**
**Kapsam:** Aşama 1 test ve inceleme kanıtı. Düzeltmeler ve regresyon ekleri ekip onayını bekliyor.

## Test sonuçları

| Kontrol | Sonuç |
| --- | --- |
| `python -B -m unittest discover -s tests -v` | 51 test, 3 başarısız alt kontrol, 29 hata, 2 atlama. Başarısızlıklar ve hatalar benchmark SHA-256 uyuşmazlığından kaynaklandı. |
| `python -B tests/test_audit_burak_task6.py` | 8 geçti, 2 atlandı. PSO, DE, DBO ve NRBO için FE, seed, sınırlar, `best_f` ve `history` kontrolleri geçti. RIME ve beşli kayıt atlandı. DBO/NRBO sabit çekilişli dal testleri geçti. |
| `python -B src/main.py --check` | Başarısız. Üç benchmark ham bayt hash kontrolünde reddedildi. |
| Kayıtlı SHA-256 ile doğrulanmış LF baytlarıyla bellek içi tekrar | 49 geçti, 2 atlandı. Tanılama, standart Windows çalıştırma hatasını izole etti. |
| Geçici dizinde tam bütçeli entegrasyon ve analiz | 4 algoritma × 3 benchmark × 1 koşu, 12 CSV ve CSV’lerde bildirilen toplam 360.000 FE. Seed, bütçe, sınırlar, bağımsız Cmax ve yakınsama sonu kontrol edildi. 5×3×1, RIME eksikliği nedeniyle bloke. |
| Negatif CSV deneyleri | Okuyucu çift koşu satırını, `n_fes=1`, `best_f=-1` ve bir algoritmaya düşen eksik sonuç kapsamını kabul etti. |
| `python -B tools/review_independent_taillard_check.py .` | Matrisler ve 1278/1582/2297 Cmax değerleri doğru. Üç ham SHA uyuşmazlığına rağmen araç genel PASS bildirdi. |
| `python -B tools/check_repo_integrity.py` ve `python -B docs/check_literature.py` | Kalite belgesi yolu kırık. Bütünlük aracı ayrıca hash uyuşmazlıklarını ve `results/` yer tutucu dışı dosyaları işaretledi. |

## Hatalar, kök nedenler ve önerilen düzeltmeler

### P0-01 · Windows checkout’ta LF ve SHA-256

- **Bulgu ve kök neden:** Git indeksinde LF, çalışma ağacında CRLF var. Üç benchmark’ın her birindeki 21 CRLF satır sonu LF’ye çevrildiğinde kayıtlı SHA-256 tam eşleşti. [Modelin veri yükleyicisi](../src/problem.py#L60) ayrıştırmadan önce ham baytları doğruluyor.
- **Çözüm:** Benchmark metinlerine `.gitattributes` ile LF kuralı uygula. Çalışma kopyasını güvenli biçimde LF baytlarıyla yenile. Kayıtlı hash ve mevcut doğrulama kuralı korunsun.
- **Regresyon ve kabul:** Temiz Windows checkout’ta ham hash 3/3 eşleşmeli. Değişmiş içerik ve eksik hash reddedilmeli. Standart paket ve duman kontrolü normalizasyon gerektirmeden geçmeli.

### P0-02 · RIME ve beşli entegrasyon

- **Bulgu ve kök neden:** İncelenen sürümde RIME modülü ve [çalıştırıcı kaydı](../src/main.py#L64) yok. Çalıştırıcı algoritma sayısındaki eksiği uyarıyla bildirip mevcut kayıtları çalıştırıyor.
- **Çözüm:** RIME’ı ortak arayüz ve onaylı parametrelerle entegre et. Beşli kabul kapısında eksik kayıt başarısızlık olarak değerlendirilsin.
- **Regresyon ve kabul:** 5/5 kayıt. RIME için FE, seed, sınırlar, sonluluk, `best_f` ve `history` denetimleri geçmeli. Tam bütçeli 5×3×1 entegrasyonu 15 geçerli CSV üretmeli.

### P0-03 · CSV doğrulama kapısı

- **Bulgu ve kök neden:** [`load_results()`](../src/stat_tests.py#L70) CSV’leri okuyor, JSON alanlarını açıyor ve sıralıyor. Koşu kimliği, seed, FE, Cmax, yakınsama ve beklenen dosya kapsamını doğrulamıyor.
- **Çözüm:** Analiz öncesinde manifest kapsamına göre dosyaları ve satırları doğrula. Hatalı sonuçlar için dosya ve satırı gösteren hata üret.
- **Regresyon ve kabul:** Eksik dosya, çift koşu, yanlış seed veya FE, geçersiz anahtar, bozuk yakınsama ve bağımsız Cmax uyuşmazlığı reddedilmeli. Geçerli 15 CSV ve `--only-analysis` akışı geçmeli.

### P1-01 · Deney manifesti

- **Bulgu ve kök neden:** [`_save_settings()`](../src/main.py#L251) temel ayarları ve parametre tablosunu yazıyor. Commit, veri hash’leri ve beklenen çıktı kapsamını birbirine bağlayan doğrulama yok.
- **Çözüm:** Commit SHA, veri hash’leri, algoritma parametreleri, seed planı, FE bütçeleri ve beklenen dosya listesini sürümlü bir manifestte kaydet.
- **Regresyon ve kabul:** Geçerli manifest kabul edilmeli. Eksik veya uyumsuz manifest, ayar ya da CSV ile analiz başlamamalı.

### P1-02 · Bağımsız Taillard aracında yanıltıcı PASS

- **Bulgu ve kök neden:** [Bağımsız Taillard aracı](../tools/review_independent_taillard_check.py) SHA sonucunu yazıyor. Son genel karar ham hash uyuşmazlığını başarısızlığa dönüştürmüyor.
- **Çözüm:** Ham SHA eşleşmesini genel karar ve çıkış koduna dahil et.
- **Regresyon ve kabul:** Matris ve referans Cmax değişmese bile ham hash farklıysa FAIL ve sıfır dışı çıkış. Geçerli ham veriyle PASS ve sıfır çıkış.

### P1-03 · Belge bağlantısı ve depo çıktı politikası

- **Bulgu ve kök neden:** [README](../README.md) ve [depo bütünlüğü aracı](../tools/check_repo_integrity.py) mevcut olmayan kalite belgesi yolunu kullanıyor. Bütünlük aracının yer tutucu kuralı, `results/` altında tutulması istenen denetim raporlarıyla çakışıyor.
- **Çözüm:** Gerçek kalite belgesi yolunu proje belgelerinde ve araçta tutarlı kullan. Denetim raporları ile deney çıktılarının yerleşim kuralını kılavuza göre belirle. İzinsiz deney çıktılarının kontrolünü koru.
- **Regresyon ve kabul:** Bağlantı denetimi ve depo bütünlüğü aracı geçmeli. Politika dışı deney çıktısı ve bozuk bağlantı hâlâ reddedilmeli.

## Kapanış kapısı

Aşama 2, açık onaydan sonra başlar. Mevcut kabul ölçütleri korunur. Standart paket, bağımsız kontroller ve 15 koşuluk entegrasyon yeniden çalıştırılır. KABUL için P0=0, P1=0 ve tüm zorunlu kontroller PASS olmalıdır. Başlangıç ve final SHA’ları kapanış raporuna kaydedilir.

DBO ve NRBO teknik denetimi ile yazar koduna dayalı sayısal dal testleri geçti. Özgün makalelere tam denklem uygunluğu Aşama 1’de doğrulanmadı. Önceki matematiksel denetimin kapsamı ve açık maddeleri [Görev 6 raporunda](audit_burak_task6_2026-11-19.md) yer alır.
