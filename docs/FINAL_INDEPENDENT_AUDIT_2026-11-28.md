# PFSP bağımsız kısmi son denetim ve teslim kapıları — 28 Kasım 2026

**Kaynak:** `develop` HEAD `a14ad757bbc4b83af1262021953aa31f8608b777`; yalnız dokümantasyon düzeltmeleri için `work/final-independent-audit-2026-11-28`. **Karar: CONDITIONAL / NOT READY FOR JOURNAL SUBMISSION.**

## 1. Bu incelemede gerçekten yapılan işlemler

- GitHub'daki `develop` ve `main` karşılaştırıldı. `develop` ile `main` geçmişi ayrışmıştır (`develop` main'e göre 96 commit ileride, 4 commit geride). Bu nedenle otomatik/force push veya kontrolsüz merge yapılmadı.
- `develop` üzerinde `results/raw/{ta001,ta011,ta021}/{DBO,DE,NRBO,PSO,RIME}.csv` içerikleri GitHub'dan **tek tek** okundu; 15/15 CSV okunabildi.
- CSV sütunları parse edilerek her dosyada 30 koşu, run 1–30, seed 2026–2055, benchmark'a göre 20k/30k/40k FE ve sonlu Cmax doğrulandı. **450/450 koşu, 13.500.000/13.500.000 raporlanan FE; bu kapsamda ihlal 0.** Bu, algoritma yeniden üretimi veya SHA-256 doğrulaması değildir.
- Ham CSV'den bağımsız hesaplanan min/mean sonuçları makaledeki Table 4 ile eşleştirildi:
  - ta001: DBO 1297/1301.300000, DE 1288/1296.700000, NRBO 1296/1299.900000, PSO 1297/1299.700000, RIME 1297/1297.133333.
  - ta011: DBO 1622/1673.200000, DE 1618/1626.766667, NRBO 1622/1680.433333, PSO 1594/1639.666667, RIME 1586/1622.633333.
  - ta021: DBO 2333/2406.066667, DE 2318/2349.900000, NRBO 2379/2426.566667, PSO 2318/2379.600000, RIME 2319/2354.100000.
- `paper/support/schedule_ta001.csv`, `schedule_ta011.csv`, `schedule_ta021.csv` üzerindeki toplam **700 işlem** için zaman aralıkları tarandı: 100/200/400 işlem, her dosyada 20 iş, sırasıyla 5/10/20 makine, `max(finish)`=1288/1586/2318; kayıtlı işlemlerde makine çakışması, işin ardışık makine öncelik ihlali ve negatif/boş zaman aralığı **0**. Bu doğrudan süre verisiyle yapılan ayrı invariant kontrolüdür; benchmark matrisinden süreleri yeniden oluşturma testi yerine geçmez.
- `paper/manuscript_nase_en.md` üzerindeki sonuç/istatistik/beyanlar ve `docs/MANAGER_FINAL_GATE_2026-11-25.md` sınırları yeniden okundu.
- Resmî https://dergipark.org.tr/en/pub/nase/writing-rules sayfası doğrudan kontrol edildi; başvuruda **İngilizce ve resmî Word şablonu** isteniyor. `docs/journal_shortlist.md` bu kaynakla yeniden uyumlaştırıldı.

## 2. Kalan görevler, yapılanlar ve kabul durumu

| Öncelik | Görev | Bu turdaki çıktı | Durum |
| --- | --- | --- | --- |
| P0 | Final veri matrisi ve makale sonuçları çapraz kontrol | 15/15 CSV, 450/450 run, 13.5m FE, 15 grup min/mean tekrar hesaplandı | **PASS (sınırlı bağımsız kontrol)** |
| P0 | Gantt zaman çakışması/öncelik kontrolü | 700/700 işlem; 0 ihlal; 3 Cmax eşleşti | **PASS (zaman çizelgesi invariantları)** |
| P0 | Yazar katkısı, sıralama, iletişim/ORCID | Taslak katkı tablosu makalede var, gerçek yazar beyanı eksik | **BLOCKED — insan onayı** |
| P0 | Etik, COI, funding, AI, data/code beyanı | Taslak metin var; tasdik yok | **BLOCKED — yazar/danışman** |
| P1 | Deney donanım doğrulama | Manifestte CPU/RAM/yük/power mode yok | **BLOCKED — birincil operatör kaydı** |
| P1 | EXPERIMENT-FREEZE ön onay kanıtı | METHOD-FREEZE SHA ve temiz deney checkout mevcut; ön onay zaman kaydı yok | **PROTOCOL DEVIATION — geriye dönük onay üretilemez** |
| P1 | Tam bağımsız QA (86+ test, hash, bağımsız model/veri Cmax, istatistikler) | Test sözleşmesi ve komutlar mevcut | **PASS via GitHub CI** — Ubuntu + Windows Python 3.12, her platformda 90/90 test; ham hash ve makale asset kontrolleri PASS |
| P1 | NASE dil kuralı doğrulama | Resmî Author Guidelines kontrolü; doküman düzeltildi | **PASS** |
| P1 | Resmî NASE Word şablonunda bütün makale | İngilizce Markdown taslak var, resmî DOCX dosyası henüz yok | **BLOCKED — layout/author data** |
| P1 | Danışmanın yöntem/sonuç ve hedef dergi onayı | İmzalı onay yok | **BLOCKED — danışman** |
| P2 | Dergi şablonunda PDF export, görsel çözünürlüğü ve equation editör QC | Son sürüm DOCX yok | **NOT READY** |
| P2 | `develop` → `main` kontrollü PR/CI | Dallar ayrışmış, onaylar eksik | **NOT ATTEMPTED** |

## 3. Bilimsel ihtiyat

- Sonuçlar üç adet 20-iş benchmarkı ve sabit parametreler için geçerli; evrensel üstünlük iddiası kurulmaz.
- ta001'de NEH=1286, deneylerde gözlenen en iyi meta-sezgisel sonuç 1288'den daha iyidir.
- Wilcoxon rank-sum `ranksums` fonksiyonunun bağ (tie) düzeltmesi yok; veriden en küçük medyanla referans seçimi post-selection riskidir. Friedman'da ortak seed'in blok kabul edilmesi algoritmalar arasında ortak random effect kanıtı sağlamaz. Test sonuçları bağımsız metodoloji onayı olmadan confirmatory olarak yorumlanmamalı.
- `main` dalının mevcut HEAD'i `30ed382...` ve iki revert içeriyor. Nihai çıktı için `develop` esas alındı. Revert'leri force push ile geçersiz kılmak veya otomatik merge etmek önerilmez.

## 4. Yeniden çalıştırılacak kabul komutları

```bash
python -m unittest discover -s tests -v
python src/problem.py
python src/main.py --check
python tools/run_neh_baseline.py
python docs/check_literature.py
python tools/check_repo_integrity.py
python tools/check_experiment_outputs.py --raw-dir results/raw --runs 30 --seed-base 2026
python -B tools/prepare_paper_assets.py --check
```

**Bu oturumda GitHub CI #125 doğrulandı:** https://github.com/mamyylmz/-Akis_Tipi_Cizelgeleme/actions/runs/46145535110 — PR branch commit `f130e037d1ba2b7df93e9bb8d07002e52446a292`; Ubuntu/Python 3.12 **90/90 OK**, Windows/Python 3.12 **90/90 OK**. Her iki job'da PFSP model, NEH, `src/main.py --check`, repo integrity, literature, full raw CSV verification ve `prepare_paper_assets.py --check` adımları başarılı. Loglarda `PAPER CHECK: PASS (raw hashes, table recalculation, manuscript blocks, citations, abstracts, schedules)` görüldü. Bu kanıt, bu oturumda yerel Python repo checkout'u olmamasına rağmen GitHub-hosted testlerin gerçekten çalıştığını doğrular. Yine de bağımsız akademik hakem/istatistik metodoloji incelemesi değildir. `python src/main.py` varsayılan final deneyleri yeniden yazabileceğinden kontrollü olmayan çalışma dizininde kullanılmamalıdır.

## 5. Teslim kararı

Ders makalesi bilimsel içerik ve kaydedilmiş deney açısından büyük ölçüde hazırlanmış durumda. Bu incelemeyle belgelenen CSV ve çizelge kontrolü doğruluk güvencesini artırdı; ancak başarılı otomatik CI tek başına dış bağımsız akademik review değildir; gerçek yazar beyanları, CPU/RAM, danışman onayı ve resmî Word şablonuna aktarım çözülmeden dergi gönderim onayı ya da `main` sürüm kabulü verilmez.
