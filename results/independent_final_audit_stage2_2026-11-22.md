# Bağımsız son kontrol · Aşama 2 kapanış raporu

**Tarih:** 22.11.2026  
**Başlangıç SHA:** `9ac8f92fc3282ab2f03aacb80b783f0024299ac5`  
**Final uygulama ve test SHA:** `274c1c1e45b18379a6d1524b50726ef49b648e93`  
**Nihai karar:** **DÜZELTME_GEREKİYOR** · **P0 = 0, P1 = 1**.

[Aşama 1 raporundaki](independent_final_audit_stage1_2026-11-22.md) üç P0 ve üç P1 teknik bulgu kapandı. Daha önce açık kaydedilen DBO/NRBO özgün makale denklem uygunluğu, proje genel kabulü için tek P1 olarak izleniyor. Beş algoritmanın teknik çıkış kapısı başarılı. Mevcut kabul testlerinin ölçütleri korunarak ayrı regresyon dosyası eklendi.

## Düzeltmeler ve regresyon kanıtı

| Aşama 1 bulgusu | Uygulanan düzeltme ve kanıt |
| --- | --- |
| P0-01 · Windows/LF-SHA | [Git öznitelikleri](../.gitattributes) benchmark’ları LF olarak sabitliyor. Windows çalışma ağacında ham hash 3/3 eşleşti. Sadece CRLF’ye dönüştürülen bir kopya aynı matrisi içerse de regresyonda reddedildi. |
| P0-02 · Beş algoritma | [RIME](../src/algorithms/rime.py) ortak FE arayüzüyle eklendi. [Çalıştırıcı](../src/main.py) zorunlu beşli küme eksikse hata veriyor. Eksik kayıt regresyonu ve mevcut beş algoritmalı bağımsız FE, seed, bounds, best_f ve history testleri geçti. |
| P0-03 · CSV doğrulama | [Doğrulayıcı](../src/experiment_validation.py) dosya kapsamını, koşu/seed/FE sayısını, random key ve permütasyonu, bağımsız Cmax ve yakınsamayı doğruluyor. Eksik dosya, çift koşu, yanlış seed/run/FE, geçersiz anahtar, yanlış amaç değeri ve bozuk yakınsama regresyonda reddedildi. |
| P1-01 · Manifest | Commit, kaynak ve veri hash’leri, algoritma parametreleri, seed planı, FE bütçeleri ve beklenen CSV yolları kaydediliyor. Analiz ayarları ve parametre tablosu da manifest ile karşılaştırılıyor. Commit, seed, kapsam, veri hash’i veya algoritma uyuşmazlığı regresyonda reddedildi. |
| P1-02 · Yanıltıcı Taillard PASS | [Bağımsız kontrol](../tools/review_independent_taillard_check.py) ham SHA ve seed eşleşmesini genel karara katıyor. CRLF fixture’ı genel FAIL ve sıfır dışı çıkış verdi. Geçerli ham veri PASS. |
| P1-03 · Belge ve çıktı politikası | Kalite belgesi bağlantısı düzeltildi. Önceki PSO smoke verisi [tarihsel arşive](../docs/test_logs/legacy_pso_smoke/) taşındı. Depo bütünlüğü üst düzey Markdown denetim kanıtlarını kabul ediyor ve `results/` içindeki deney çıktılarını kontrol etmeyi sürdürüyor. Her iki depo/belge aracı geçti. |

[Ek regresyonlar](../tests/test_final_acceptance_regressions.py) NRBO’da ilk bölmenin paydası sıfırın iki tarafına yaklaştırıldığında değerlendirme adayının sonlu, sınır içinde ve deterministik kaldığını da doğruladı. Tam sıfır ve TAO dal testleri mevcut pakette yeniden geçti. İkinci kesrin ayrı yakın-sıfır stres vakası ve özgün makalelerle tam denklem eşleştirmesi bu kanıttan çıkarılamaz.

RIME, yayındaki soft-rime, hard-rime ve açgözlü kabul kurallarını FE bütçesine uyarlıyor. Faz açısı yayındaki Denklem (4) esas alınarak `π·ilerleme/10` seçildi. Yazarın MATLAB dosyasında faz açısı `10·π·ilerleme` biçiminde yazılmış. Bu farklılık için kullanılan referans kararı kaydedildi. [Özgün RIME makalesi](https://aliasgharheidari.com/assets/files/RIME-A-physics-basedoptimization-neurocomputing-2023.pdf) · [Yazar MATLAB kodu](https://raw.githubusercontent.com/aliasgharheidaricom/RIME-A-physics-based-optimization/main/RIME.m)

## Final testler

| Komut veya kontrol | Sonuç |
| --- | --- |
| `python -B -m unittest discover -s tests -v` | **PASS**, 56/56, 0 hata, 0 atlama. Bağımsız Görev 6 paketi ve yeni 5 regresyon dahil. |
| `python -B src/main.py --check` | **PASS**, 3 benchmark ve 5/5 algoritma. |
| `python -B src/problem.py` | **PASS**, Cmax 1278 / 1582 / 2297. |
| `python -B tools/review_independent_taillard_check.py .` | **PASS**, ham SHA, bağımsız matris ve Cmax 3/3. |
| `python -B tools/check_repo_integrity.py` | **PASS**, gerekli dosyalar, SHA, bağlantılar, önbellek ve çıktı politikası. |
| `python -B docs/check_literature.py` | **PASS**, yapı ve yerel bağlantılar. Bu araç özgün denklem uygunluğunu ölçmüyor. |
| `python -B src/main.py --runs 1 --output-dir <dizin>` | **PASS**, 15 CSV, her birinde tek koşu, toplam 450.000 raporlanan FE. Manifest yayımlandı. |
| `python -B src/main.py --only-analysis --output-dir <dizin>` | **PASS**, aynı manifest ve 15 CSV doğrulandı, analiz yeniden üretildi. |

## 5 algoritma × 3 benchmark × 1 koşu

Seed **2026**. Hücrelerde doğrulanan en iyi Cmax yer alıyor. Bir koşuluk sonuçlar entegrasyon kanıtıdır.

| Benchmark | Algoritma başına FE | PSO | DE | DBO | NRBO | RIME |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ta001 | 20.000 | 1297 | 1297 | 1324 | 1302 | 1297 |
| ta011 | 30.000 | 1625 | 1626 | 1690 | 1660 | 1614 |
| ta021 | 40.000 | 2358 | 2349 | 2357 | 2402 | 2329 |

Yerel kanıt dizini Windows geçici dosya alanında bırakıldı. İçinde `raw/`, `tables/experiment_manifest.json` ve `figures/` var.

```text
C:\Users\Tarik\AppData\Local\Temp\pfsp-final-573bb868d4224d61bbf70d729ec4ee47
```

## Açık kabul maddesi

**P1 · Özgün DBO/NRBO denklem uygunluğu.** [Önceki Görev 6 denetiminde](audit_burak_task6_2026-11-19.md) kaydedilen MATLAB farkları ve özgün yayın eşleştirmesi henüz tam kabul kanıtına bağlanmadı. DBO yayıncısının erişilebilir sayfası özet sunuyor. NRBO için erişilen yayıncı materyali de bu çalışmada tam denklem eşleştirmesine yeterli olmadı. Kapanış için özgün denklem ve uyarlama kararlarının Şeref tarafından kaynak satırıyla doğrulanması gerekiyor. [DBO yayını](https://doi.org/10.1007/s11227-022-04959-6) · [NRBO yayını](https://doi.org/10.1016/j.engappai.2023.107532)

Kabul kapısı P0=0, P1=0 ve tüm zorunlu kontrollerin PASS olmasını gerektirir. Otomatik ve entegrasyon kontrolleri başarılı. Akademik P1 açık olduğundan genel karar **DÜZELTME_GEREKİYOR**.
