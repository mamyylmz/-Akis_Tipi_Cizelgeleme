# Görev 6 · Bağımsız DBO ve NRBO denetimi

**Tarih:** 19.11.2026 · **İncelenen Git sürümü:** ed32526  
**Perspektifler:** Şeref — özgün yöntem ve matematik. Tarık — arayüz, FE, seed ve entegrasyon.  
**Genel kabul:** **BLOKE.** Yazar MATLAB koduna dayalı sayısal dallar ve mevcut dört algoritmanın teknik kontrolleri geçti. Tam yayın eşleştirmesi, Windows veri bütünlüğü ve RIME entegrasyonu açık.

Bu rapor güncel Git kopyasında baştan yapılan denetimi kaydeder. Teslim edilen dosyalar bu rapor ve [bağımsız denetim paketi](../tests/test_audit_burak_task6.py). Ekip kaynakları ve testleri dosya düzeyinde değişmedi. İncelemede [arayüz tanımı](../docs/algorithm_interface.md), [kalite kararları](../docs/KALITE_KARARLARI.md), [yöntem notları](../paper/method_dbo_nrbo.md), [smoke kaydı](../docs/test_logs/19_burak_dbo_nrbo_smoke.txt) ve [sürüm kaydı](../docs/test_logs/20_burak_sha256.txt) kullanıldı.

```text
76dfbe67de948e6b38b616f4d77697527d93f08658b9d7a76e3de2a23a67b580  tests\test_audit_burak_task6.py
d226087d887c508a3c36867670b9cca0dce950ddb604351354f013d2edc60a1b  src\algorithms\dbo.py
ece8d023cdbe600f7fed58c0ed6c4bff9552ece1550458e6c4675a125ca55c3e  src\algorithms\nrbo.py
b6c0752b2eb031c2dfee4b2a44c7e8694131f876dd9f90355e844867ca359750  src\main.py
8d943437632f9f0f182014ed25ed5e9830e4e9a941addaf59d8ce927fd6749c1  docs\test_logs\21_dbo_author_matlab_reference.m
3b6cfad1ddf210486cee5a3f8db38c5b27a5acfbe4a9ffcf207ea38d6ea414fd  docs\test_logs\22_nrbo_author_matlab_reference.m
```

## A · Şeref perspektifi

`21_…m` ve `22_…m` dosyaları erişilebilir ve satır eşleştirmesi yapıldı. DBO yayıncısı özeti sunuyor. NRBO yayıncı bağlantısından tam denklemlere erişilemedi. Denklem numaraları yerel yöntem notu ve yazar koduna dayanır. [DBO özgün yayını](https://link.springer.com/article/10.1007/s11227-022-04959-6) · [NRBO özgün yayını](https://doi.org/10.1016/j.engappai.2023.107532)

| Kontrol | Kanıt ve gözlenen fark | Karar |
| --- | --- | --- |
| DBO yuvarlama/dans, Denk. 1–2 | [Python 127–150](../src/algorithms/dbo.py#L127) ve [MATLAB 39–72](../docs/test_logs/21_dbo_author_matlab_reference.m#L39). Yuvarlamada önceki konum terimi, sapma işareti, en kötüye uzaklık ve ortak geçiş çekilişi eşleşiyor. 45° testi önceki konuma göre beklenen adımı doğruladı. Python 90° ve 180° için konumu koruyor. MATLAB koruma atamasını tanjant satırıyla eziyor. | **PASSED** proje davranışı, **FARK** MATLAB açı dalı |
| DBO yumurtlama, beslenme ve çalma, Denk. 3–7 | [Python 153–200](../src/algorithms/dbo.py#L153) ve [MATLAB 74–118](../docs/test_logs/21_dbo_author_matlab_reference.m#L74). Sabit çekilişlerde iç bölge sınırları, skaler normal / vektör uniform beslenme ve vektör normal çalma adayı beklenen vektörle eşleşti. Python daralmayı yuvarlama grubundan sonra tüketilen FE oranıyla güncelliyor, MATLAB iterasyon oranını kullanıyor. | **PASSED** yerel formüller, **FARK** zamanlama |
| NRBO NRSR ve aday birleştirme, yöntem notundaki Denk. 19–29 | [Python 42–54, 123–144](../src/algorithms/nrbo.py#L42) ve [MATLAB 56–79, 148–172](../docs/test_logs/22_nrbo_author_matlab_reference.m#L56). İki kesir, skaler ortalama, işaret, rho ve üç adayın birleşimi sabit çekilişlerle karşılaştırıldı. Python boyut katsayılarını iki vektör halinde, MATLAB boyut başına ardışık çekiyor. Dağılım yapısı aynı, çekiliş sırası farklı. | **PASSED** sayısal dal |
| NRBO TAO ve sınırlar, yöntem notundaki Denk. 30–35 | [Python 105–107, 146–174](../src/algorithms/nrbo.py#L146) ve [MATLAB 82–119](../docs/test_logs/22_nrbo_author_matlab_reference.m#L82). TAO kapalı, TAO güncellenmiş aday tabanlı ve TAO en iyi aday tabanlı vakalar geçti. 0/0 vakasında değerlendirmeye giden aday alt sınırda sonlu. Yakın-sıfır payda için ayrı eşik veya epsilon kuralı bulunmadı ve bu varyant ayrı sayısal kabul vakası olarak ölçülmedi. | **PASSED** üç TAO dalı ve tam tekillik |
| NRBO delta zamanlaması | Python her dış tur başında bir kez tüketilmiş FE oranıyla hesaplıyor ve tur boyunca sabit tutuyor. MATLAB her iterasyon başında iterasyon oranını kullanıyor. Önceki rapordaki aday başına yeniden hesaplama ifadesi bu sürüm için yanlıştı. | **FARK** ilerleme tanımı |
| Özgün makale uyumu | Tam özgün metin ve denklem numarası doğrulaması açık. Sabit çekiliş testleri yazar kodu ve belgelenen PFSP uyarlaması düzeyinde. | **BLOKE** |
| Random-key ve sınır | [Model](../src/problem.py) kırpma sonrası eşit anahtarlarda iş indeksi sırasını koruyor. 5×3 referansı 20 ve ta001 referansı 1278 olarak bağımsız doğrulandı. Uç anahtar sayısı ve eşitlik tablosu aşağıda. | **PASSED** |

## B · Tarık perspektifi

Ders arayüzünü uygulayan bağımsız sarmalayıcı her değerlendirmeyi sayar, bütçe aşımında durur ve amaç değerini ayrı DP ile hesaplar. Aday şekli, finiteness, sınırlar ve dönen en iyi anahtarın değerlendirilmiş adaylar arasında oluşu kontrol edildi. Her yakınsama noktası, bağımsız sayacın o FE’ye kadarki en iyi değeriyle karşılaştırıldı. Her algoritma 5×3 ve ta001 üzerinde 7, 73, 121 FE ile çalıştı. Her hücrede seed 2026 iki kez ve seed 2027 bir kez kullanıldı. Aynı seed için adaylar, yakınsama, en iyi sıra ve Cmax eşleşti. Farklı seed için aday akışı değişti. Alt süreç sınırı algoritma başına 30 saniye.

| Madde | Gözlenen | Karar |
| --- | --- | --- |
| PSO, DE, DBO, NRBO | Dördü de `main.py` kayıt parametreleriyle geçti. Gerçek çağrı = n_fes = bütçe. Sonlu sonuçlar ve bağımsız Cmax eşleşmesi sağlandı. | **PASSED** doğrulanmış veriyle |
| RIME ve beşli kayıt | Modül ve kayıt yok. İki senaryo bu nedenle atlandı. | **BLOKE** |
| Standart Windows veri bütünlüğü | Üç benchmark Git indeksinde LF, çalışma ağacında CRLF. Her dosyada 21 CRLF, LF’ye çevrildiğinde kayıtlı SHA-256 birebir eşleşti. Normal çalıştırıcı bu üç örneği hash nedeniyle reddetti. | **FAIL** |

### Seed 2026 ölçüm tablosu

| Algoritma | Problem | Gerçek FE | En iyi Cmax | Uç anahtar / toplam | Eşit anahtarlı aday | Benzersiz permütasyon |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| PSO | 5x3 | 7 | 20 | 0/35 | 0 | 6 |
| PSO | 5x3 | 73 | 19 | 6/365 | 0 | 42 |
| PSO | 5x3 | 121 | 19 | 23/605 | 0 | 51 |
| PSO | ta001 | 7 | 1481 | 0/140 | 0 | 7 |
| PSO | ta001 | 73 | 1343 | 18/1460 | 3 | 73 |
| PSO | ta001 | 121 | 1341 | 118/2420 | 23 | 121 |
| DE | 5x3 | 7 | 20 | 0/35 | 0 | 6 |
| DE | 5x3 | 73 | 19 | 33/365 | 5 | 51 |
| DE | 5x3 | 121 | 19 | 70/605 | 13 | 67 |
| DE | ta001 | 7 | 1481 | 0/140 | 0 | 7 |
| DE | ta001 | 73 | 1359 | 0/1460 | 0 | 73 |
| DE | ta001 | 121 | 1359 | 60/2420 | 15 | 121 |
| DBO | 5x3 | 7 | 20 | 0/35 | 0 | 6 |
| DBO | 5x3 | 73 | 19 | 33/365 | 8 | 42 |
| DBO | 5x3 | 121 | 19 | 87/605 | 15 | 51 |
| DBO | ta001 | 7 | 1481 | 0/140 | 0 | 7 |
| DBO | ta001 | 73 | 1368 | 134/1460 | 25 | 73 |
| DBO | ta001 | 121 | 1357 | 392/2420 | 65 | 121 |
| NRBO | 5x3 | 7 | 20 | 0/35 | 0 | 6 |
| NRBO | 5x3 | 73 | 19 | 52/365 | 7 | 44 |
| NRBO | 5x3 | 121 | 19 | 109/605 | 18 | 50 |
| NRBO | ta001 | 7 | 1481 | 0/140 | 0 | 7 |
| NRBO | ta001 | 73 | 1324 | 352/1460 | 37 | 66 |
| NRBO | ta001 | 121 | 1324 | 644/2420 | 71 | 109 |

Ta001 ve 121 FE’de DBO için %16,20, NRBO için %26,61 uç anahtar gözlendi. DBO bu koşuda 121, NRBO 109 benzersiz sıra verdi. Bu kısa koşular, kırpmanın çözüm kalitesine nedensel etkisini tek başına ölçmez.

### Test kanıtı ve tekrar

- `python -B tests/test_audit_burak_task6.py` → **10 senaryo, 8 başarılı, 2 BLOKE/SKIPPED**. Algoritma tanılaması ancak LF karşılığı kayıtlı SHA-256 ile eşleşirse onu kullanır.
- `python -B -m unittest discover -s tests -v` → **51 senaryo, 3 başarısız alt kontrol, 29 hata, 2 atlanan**. Başarısızlık ve hataların nedeni benchmark hash uyuşmazlığı.
- `python -B src/main.py --check` → **FAIL**, üç benchmark için SHA-256 uyuşmazlığı.
- Aşağıdaki bellek içi tanılama → **51 senaryo, 49 başarılı, 2 atlanan**. Çalıştırıcının model ve dört kayıtlı algoritma kontrolleri de bu koşulda geçti.
- Ölçümleri yeniden almak için `python -B tests/test_audit_burak_task6.py --audit-worker DBO`. Aynı komut PSO, DE ve NRBO için kullanılabilir.

Bellek içi tanılama kodu, repo kökünde Python’a standart girdiden verilebilir. Sadece kayıtlı SHA-256 ile eşleşen benchmark baytlarını değiştirir.

```python
import hashlib, json, sys, unittest
from pathlib import Path
from unittest.mock import patch
data = (Path.cwd() / "data" / "taillard").resolve()
metadata = json.loads((data / "reference_solutions.json").read_text())["instances"]
read = Path.read_bytes
def canonical(path):
    raw = read(path)
    if path.parent == data and path.suffix == ".txt" and path.stem in metadata:
        lf = raw.replace(b"\r\n", b"\n")
        if hashlib.sha256(lf).hexdigest() == metadata[path.stem]["sha256"]:
            return lf
    return raw
with patch.object(Path, "read_bytes", canonical):
    suite = unittest.defaultTestLoader.discover("tests")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    import main
    main.run_checks()
```

**Kabulü kapatma koşulları:** Özgün tam metinle denklem eşleştirmesini tamamla, benchmark çalışma ağacı satır sonlarını düzelt ve standart çalıştırmayı yeniden doğrula, RIME modülü ve kaydı geldiğinde beşli senaryoyu yeniden çalıştır. Ekip adına bağımsız kabul kaydı bekliyor.
