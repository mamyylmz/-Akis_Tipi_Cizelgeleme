# Görev 6 · Hata analizi ve düzeltme listesi

**Tarih:** 19.11.2026  
**İncelenen sürüm:** `ed32526`  
**Denetim:** Şeref perspektifi (matematiksel uygunluk), Tarık perspektifi (teknik doğrulama)  
**Genel karar:** **BLOKE.** Standart Windows çalıştırması başarısız. RIME ve beşli kayıt denetimi çalıştırılamadı. DBO ve NRBO teknik kontrolleri doğrulanmış veriyle başarılı, özgün yayın uyumu açık.

Kanıt olarak [Görev 6 denetimi](audit_burak_task6_2026-11-19.md) ve [bağımsız test dosyası](../tests/test_audit_burak_task6.py) kullanıldı. İki farklı seed için Cmax değerleri aynı test sarmalayıcısıyla yeniden ölçüldü. Proje kabul kuralları için [ortak kılavuz §9–14](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md) ve [kalite kararları](../docs/KALITE_KARARLARI.md) esas alındı. Aşağıdaki yeni sayısal öneriler ekip kararı gerektirir.

## 1. Yönetici özeti ve kabul durumu

| Bileşen | Durum | Kanıt / kapsam |
| --- | --- | --- |
| PSO | PASSED | 5×3 ve ta001 üzerinde 7, 73, 121 FE, aday akışı, sonluluk ve bağımsız Cmax. |
| DE | PASSED | Aynı teknik kontroller ve kayıtlı parametrelerle yürütme. |
| DBO | PASSED teknik / BLOKE tam matematiksel kabul | Dört rol ve dans örnekleri sabit çekilişlerle geçti. 90°/180° davranışı ve daralma zamanlaması yerel MATLAB kodundan farklı. |
| NRBO | PASSED teknik / BLOKE tam matematiksel kabul | NRSR, TAO’nun iki tabanı, TAO kapalı dalı ve tam tekillik testleri geçti. Yakın-sıfır vaka ve özgün yayın doğrulaması açık. |
| RIME | BLOKE / SKIPPED | Modül ve kayıt eksik. Algoritma davranışı hakkında test sonucu yok. |
| `src/main.py` | PASSED dört kayıt / BLOKE beşli kabul | Dört kayıt, doğrulanmış LF verisiyle duman kontrolünde geçti. RIME kaydı eksik. |
| Windows benchmark dosyaları | FAILED | Çalışma ağacındaki üç ham veri dosyası beklenen SHA-256 değerine uymuyor. Normal koşuda yükleyici reddediyor. |
| Random-key çözümleyici | PASSED | Çözüm sınırları, geçerli permütasyon ve açık eşitlik kuralı doğrulandı. Uçlarda birikme performans izleme maddesi. |

**Standart tam paket:** 51 senaryo, 3 başarısız alt kontrol, 29 hata, 2 atlanan.  
**Bağımsız Görev 6 paketi:** 10 senaryo, 8 başarılı, 2 atlanan.  
**Doğrulanmış LF baytlarıyla bellek içi tam paket:** 51 senaryo, 49 başarılı, 2 atlanan. Bu çalıştırma hatayı izole eden tanılamadır. Standart Windows çalıştırmasının kabulünü kapatmaz.

## 2. Test istatistikleri ve minimum kabul eşikleri

### Karşılaştırmalı kabul tablosu

| Kriter | Mevcut ölçülen değer | Minimum / hedef | Sapma ve durum |
| --- | --- | --- | --- |
| Ham veri SHA-256 | 0/3 eşleşme. LF tanılamasında 3/3. | Standart temiz checkout’ta 3/3 ham bayt eşleşmesi. | Standart durumda −3, FAILED. |
| Kayıt ve arayüz | 4/5 kayıt. Çalışan dört algoritmada ortak imza ve zorunlu alanlar doğrulandı. | PSO, DE, DBO, NRBO ve RIME için 5/5 modül, kayıt ve geçerli dönüş. | −1 kayıt, BLOKE. |
| FE bütçesi | Dört algoritma × iki problem × üç bütçe × üç koşu = **72 koşu**. Her koşuda gerçekleşen FE = `n_fes` = 7/73/121. | Her koşuda birebir eşitlik. Eksik sayım ve aşım 0. | 0/72 ihlal, PASSED erişilen dört algoritmada. |
| Aynı seed | 24 eşleşmiş çiftte aday akışı, yakınsama, en iyi anahtar, permütasyon ve Cmax birebir eşleşti. | Aynı ortam/parametrelerde sapma **%0**. | **0/24 (%0)**, PASSED. |
| Farklı seed | Eşleştirilen 24 senaryonun tamamında 2026 ve 2027 aday akışları farklı. | Bu sabit denetim çiftinde 24/24 farklı akış. En iyi Cmax eşit olabilir. | 24/24, PASSED. |
| Geçerlilik, sonluluk ve sonlanma | 72/72 koşu geçti. Toplam 4.824 amaç çağrısında geçersiz veya sonlu olmayan aday gözlenmedi. | 0 bütçe aşımı, 0 NaN/Inf, 0 sınır dışı aday. İşler birer kez. Denetimde alt süreç başına ≤30 s. | 0 ihlal ve zaman aşımı, PASSED. |
| Bağımsız Cmax ve yakınsama | 72/72 en iyi amaç değeri ve tüm kaydedilen yakınsama noktaları bağımsız sayaçla eşleşti. Referanslar 5×3 = 20, ta001 = 1278. | Amaç hatası 0, yakınsama noktası hatası 0, referanslar tam eşit. | PASSED. |
| DBO/NRBO sayısal formülleri | DBO açı 45°/90°/180° ve dört rol, NRBO üç TAO durumu, tam tekillik geçti. | Kabul edilen kaynak/uyarlama için dal başına beklenen vektörle eşleşme. Mevcut fixture toleransı mutlak ≤10⁻¹² ve göreli 0. | Yerel fixture PASSED. Kaynakta açık farklar var. |
| Yayın ve yakın-sıfır payda | Özgün tam denklem teyidi ve ayrı yakın-sıfır deneyi yok. | İki algoritmada ilgili tüm denklem/dalların kaynak eşleştirmesi. Yakın-sıfır politikasına göre sonlu ve sınır içi aday, sabit çekilişte deterministik sonuç. | BLOKE / doğrulama açığı. |
| Uç anahtar ve çeşitlilik | ta001, 121 FE, seed 2026. DBO %16,20 ve 121/121 benzersiz sıra. NRBO %26,61 ve 109/121 benzersiz sıra. | Zorunlu eşik **%0 sınır dışı anahtar**. Tam 0/1 oranı için proje eşiği yok. Önerilen izleme tetikleyicisi ≥%20 uç anahtar **ve** <%95 benzersiz sıra. | NRBO önerilen tetikleyiciyi geçti. Algoritma kabulünde performans reddi doğurmaz. |
| Standart kapanış | 51 senaryoda 3 başarısız alt kontrol, 29 hata, 2 atlama. | Mevcut paket için **51/51**, 0 hata, 0 başarısızlık, 0 atlama. Eklenen testler de geçmeli. Standart `--check` başarılı. | FAILED/BLOKE. |

72 koşu ve 4.824 değerlendirme, bütçe/seed denetiminin dört algoritmadaki toplamıdır. Sabit denklem fixture’ları, ekip regresyon testleri ve aşağıdaki ilave Cmax ölçümü bu sayıya dahil edilmedi.

### Cmax dağılımı · iki farklı seed

Her satırda iki bağımsız seed (2026 ve 2027) ve bir bütçe kullanıldı. Aynı seed ile yapılan deterministik tekrar dağılıma eklenmedi. Standart sapma örneklem formülüyle hesaplandı (n−1). Bunlar kısa doğrulama koşularına ait tanımlayıcı değerlerdir. Projenin bilimsel performans karşılaştırması için kılavuzdaki en az 30 koşu ve örnek başına eşit FE bütçesi uygulanmalı. **1278**, referans permütasyonunun doğrulama hedefidir. 7–121 FE’de her algoritmanın ulaşması gereken bir performans eşiği tanımlanmadı.

| Algoritma | Problem | FE | Seed 2026 | Seed 2027 | Min | Ortalama | Örneklem SS |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PSO | 5x3 | 7 | 20 | 19 | 19 | 19,50 | 0,71 |
| PSO | 5x3 | 73 | 19 | 19 | 19 | 19,00 | 0,00 |
| PSO | 5x3 | 121 | 19 | 19 | 19 | 19,00 | 0,00 |
| PSO | ta001 | 7 | 1481 | 1478 | 1478 | 1479,50 | 2,12 |
| PSO | ta001 | 73 | 1343 | 1370 | 1343 | 1356,50 | 19,09 |
| PSO | ta001 | 121 | 1341 | 1339 | 1339 | 1340,00 | 1,41 |
| DE | 5x3 | 7 | 20 | 19 | 19 | 19,50 | 0,71 |
| DE | 5x3 | 73 | 19 | 19 | 19 | 19,00 | 0,00 |
| DE | 5x3 | 121 | 19 | 19 | 19 | 19,00 | 0,00 |
| DE | ta001 | 7 | 1481 | 1478 | 1478 | 1479,50 | 2,12 |
| DE | ta001 | 73 | 1359 | 1370 | 1359 | 1364,50 | 7,78 |
| DE | ta001 | 121 | 1359 | 1352 | 1352 | 1355,50 | 4,95 |
| DBO | 5x3 | 7 | 20 | 19 | 19 | 19,50 | 0,71 |
| DBO | 5x3 | 73 | 19 | 19 | 19 | 19,00 | 0,00 |
| DBO | 5x3 | 121 | 19 | 19 | 19 | 19,00 | 0,00 |
| DBO | ta001 | 7 | 1481 | 1478 | 1478 | 1479,50 | 2,12 |
| DBO | ta001 | 73 | 1368 | 1351 | 1351 | 1359,50 | 12,02 |
| DBO | ta001 | 121 | 1357 | 1370 | 1357 | 1363,50 | 9,19 |
| NRBO | 5x3 | 7 | 20 | 19 | 19 | 19,50 | 0,71 |
| NRBO | 5x3 | 73 | 19 | 19 | 19 | 19,00 | 0,00 |
| NRBO | 5x3 | 121 | 19 | 19 | 19 | 19,00 | 0,00 |
| NRBO | ta001 | 7 | 1481 | 1478 | 1478 | 1479,50 | 2,12 |
| NRBO | ta001 | 73 | 1324 | 1347 | 1324 | 1335,50 | 16,26 |
| NRBO | ta001 | 121 | 1324 | 1321 | 1321 | 1322,50 | 2,12 |

### Uç anahtarlar · seed 2026, 121 FE

Payda, her değerlendirilen adayın bütün anahtar bileşenleridir. Eşit aday sütunu, en az iki eşit bileşeni olan vektör sayısıdır. Bu ölçüm, finalde kaydedilen en iyi vektörün uç oranından farklı bir ölçümdür.

| Algoritma | 5×3 uç anahtar | 5×3 eşit / benzersiz aday | ta001 uç anahtar | ta001 eşit / benzersiz aday |
| --- | ---: | ---: | ---: | ---: |
| PSO | 23/605 (%3,80) | 0 / 51 | 118/2420 (%4,88) | 23 / 121 |
| DE | 70/605 (%11,57) | 13 / 67 | 60/2420 (%2,48) | 15 / 121 |
| DBO | 87/605 (%14,38) | 15 / 51 | 392/2420 (%16,20) | 65 / 121 |
| NRBO | 109/605 (%18,02) | 18 / 50 | 644/2420 (%26,61) | 71 / 109 |

## 3. Kök neden analizi

1. **Windows hash hataları, P0.** `git ls-files --eol` üç veri dosyasında `i/lf w/crlf attr/` gösterdi. Etkin `core.autocrlf=true` ve veri dosyaları için sabit LF kuralı bulunmuyor. Her dosyadaki 21 CRLF’nin LF karşılığı kayıtlı hash ile tam eşleşti. [`Problem._load_data`, 60–75](../src/problem.py#L60) çalışma ağacı baytlarını okuyor ve ayrıştırmadan önce SHA-256 karşılaştırması yapıyor. Bu nedenle [`check_problem`, 90](../src/main.py#L90) ve model kuran 29 test senaryosu/alt kontrolü veri yüklemede duruyor. Bağımsız [`test_data_loading`, 22–40](../tests/test_model_validation.py#L22) üç dosyada aynı farkı doğrudan yakalıyor. Temel neden Git checkout dönüşümü. Hash’i kaldırmak veya beklenen değeri CRLF’ye göre değiştirmek platformlar arası veri bütünlüğünü çözmez.
2. **RIME ve beşli kapı, P0.** `src/algorithms/rime.py` ve [`ALGORITHMS`, 64–70](../src/main.py#L64) kaydı eksik. Bağımsız denetimin [modül ve kayıt kontrolleri, 143–178](../tests/test_audit_burak_task6.py#L143) iki senaryoyu atlıyor. [`run_checks`, 173–195](../src/main.py#L173) eksik sayıyı uyarı olarak veriyor ve mevcut kayıtları çalıştırıyor. Duman kontrolü dört kayıtla tamamlanabildiğinden beşli kabulün ayrıca zorunlu tutulması gerekiyor.
3. **DBO açı davranışı ve zamanlama, P1.** [`dbo`, 142–154](../src/algorithms/dbo.py#L142) 90°/180° için adımı atlıyor ve daralmayı yuvarlama grubundan sonraki FE oranıyla başlatıyor. [Yazar MATLAB kodu, 59–75](../docs/test_logs/21_dbo_author_matlab_reference.m#L59) koruma atamasının ardından tanjant satırını çalıştırıyor ve iterasyon oranı kullanıyor. Bunlar gözlenen davranış farkları. Hangi davranışın özgün metne ve proje uyarlamasına uygun olduğu birincil denklem ile belgelenmeli.
4. **NRBO zamanlama ve payda, P1.** [`nrbo`, 123–156](../src/algorithms/nrbo.py#L123) dış tur başında FE tabanlı `delta` hesaplıyor. [MATLAB, 56–79](../docs/test_logs/22_nrbo_author_matlab_reference.m#L56) iterasyon tabanlı ve boyut katsayılarını farklı sırayla çekiyor. [`_search_rule`, 42–54](../src/algorithms/nrbo.py#L42) iki bölümde de payda küçükken bölmeye devam ediyor. [`bound`, 105–107](../src/algorithms/nrbo.py#L105) sonuçtaki NaN/Inf’i uçlara eşliyor. Tam tekillik testinde sonlu aday doğrulandı. Sıfıra yakın pozitif/negatif paydanın büyüttüğü sonlu adımları ve olası uç birikimini ayıran test eksik. Bu, kanıt açığı ve sayısal risk olarak kalmalı.
5. **Uçta birikme, P2.** [DBO aday sınırları, 148–193](../src/algorithms/dbo.py#L148) ve [NRBO son sınır işlemi, 105–107 ve 160](../src/algorithms/nrbo.py#L105) taşmayı uçlarda topluyor. [`Problem.evaluate` ve `decode`, 119–126 ve 164–166](../src/problem.py#L119) kırpılmış eşit anahtarları kararlı sıralamayla çözüyor. Farklı vektörler aynı sıraya dönüşebilir. Erişilen dört algoritmada FE sayımı veya RNG izolasyonu hatası görülmedi. 121 FE ölçümleri uç birikiminin Cmax üzerindeki nedensel etkisini belirlemiyor.

## 4. Önceliklendirilmiş düzeltme listesi

### P0-01 · Git checkout’ta LF ve ham veri bütünlüğü

- **Mevcut Hatalı Davranış** — Windows checkout, üç benchmark’ın ham baytlarını CRLF’ye dönüştürüyor.
- **Olması Gereken Çözüm** — Git entegrasyon sorumlusu ile benchmark metinleri için örneğin `data/taillard/ta*.txt text eol=lf` kuralı tanımlayın. Kuralı temiz Windows checkout’ta veya yalnız ilgili dosyaların güvenli yeniden alınmasıyla uygulayın. Kanonik hash ve yükleyicinin katı kontrolü korunsun.
- **Doğrulama Kriteri** — `git ls-files --eol -- data/taillard` ile üç veri dosyası LF. Ham SHA-256 3/3 eşleşmeli. Bellek içi normalizasyon olmadan ilgili testler ve duman kontrolü geçmeli.

### P0-02 · RIME teslimi ve beşli entegrasyon

- **Mevcut Hatalı Davranış** — RIME modülü/kaydı yok. İki denetim senaryosu çalışmıyor.
- **Olması Gereken Çözüm** — RIME sorumlusu modülü ortak imzayla tamamlasın, Burak entegrasyon sorumluluğunda kayıt ve parametreleri doğrulasın. Teslim kapısı, beşli kayıt denetimindeki skip’i kapanmamış kabul maddesi saysın.
- **Doğrulama Kriteri** — Kayıt 5/5. RIME, 5×3 ve ta001’de 7/73/121 FE, 2026/2027 seed denetimi, aday sonluluğu, geçerli permütasyon ve bağımsız Cmax/FE kontrollerini geçsin. Standart tam pakette 0 skip.

### P1-01 · DBO açı ve daralma sözleşmesi

- **Mevcut Hatalı Davranış** — 90°/180° ve daralma zamanlamasında kaynak uygulama ile proje davranışı ayrışıyor. Özgün metin karşılığı henüz doğrulanmadı.
- **Olması Gereken Çözüm** — Özgün denklem/metin ve yazar kodunu satır numarasıyla eşleyin. 90°/180° davranışı ile FE tabanlı daralmanın gerekçesini proje sözleşmesinde kaydedin. Kaynakla birebir eşleşme zorunluysa sözleşmedeki karara göre uyarlamayı düzeltin.
- **Doğrulama Kriteri** — Şeref kaynak/uyarlama eşleştirmesini doğrulasın. 45°/90°/180° ve dört rol testleri, seçilen sözleşmenin beklenen vektörlerine mutlak tolerans ≤10⁻¹² ile uysun. FE bütçesi sapması 0.

### P1-02 · NRBO payda ve delta sözleşmesi

- **Mevcut Hatalı Davranış** — Sıfıra yakın payda büyük adımlar üretebilir. Mevcut tam tekillik testi, yakın-sıfır davranışını kapsamıyor. Katsayı ilerlemesi ve çekiliş sırası MATLAB’dan farklı.
- **Olması Gereken Çözüm** — Özgün NRSR/TAO denklemlerini ve proje uyarlamasını belgeleyin. Her iki payda için 0, küçük pozitif ve küçük negatif vakaları ayrı ölçün. Sayısal koruma gerekirse ölçeğe bağlı eşik ile geri dönüş kuralını açıkça tanımlayın ve etkisini kıyaslayın.
- **Doğrulama Kriteri** — Üç TAO vakası, normal adım, tam tekillik ve her iki kesrin yakın-sıfır vakaları deterministik geçsin. Değerlendirmeye giren NaN/Inf ve sınır dışı aday sayısı 0, FE farkı 0. Şeref beklenen adayları bağımsız referansla teyit etsin.

### P2-01 · Uç birikme etkisini ölçme

- **Mevcut Hatalı Davranış** — Uçlarda kümelenme gözlendi. Ta001’de NRBO için %26,61 ve 109/121 benzersiz sıra, kısa koşudaki bir ölçüm.
- **Olması Gereken Çözüm** — Kırpmayı kontrol grubu olarak tutun. Yansıtma veya yeniden örnekleme gibi adayları aynı seed ve eşit FE ile kıyaslayın. Uç anahtar, eşitlik ve benzersiz sıra oranı yanında Cmax/RPD, medyan ve dağılımı ölçün. Nihai çalışmada kılavuzdaki en az 30 koşu ve üç zorunlu benchmark kullanılmalı.
- **Doğrulama Kriteri** — FE/seed ve sınır sözleşmesinde sıfır ihlal. Önerilen izleme tetikleyicisini aşan koşuları raporlayın. Yöntem değişimi için Cmax/RPD faydasını ve düzeltmenin etkisini eşleştirilmiş karşılaştırmayla gösterin. Proje tarafından onaylanmış kalite eşiği oluşana kadar uç oranı kabul kararı olarak kullanılmamalı.
