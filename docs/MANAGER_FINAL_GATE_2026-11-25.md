# Proje yöneticisi final entegrasyon ve kalite kapısı — 25.11.2026

**Durum: TEKNİK ENTEGRASYON İNCELEMESİ; AKADEMİK/YAYIN KABULÜ BEKLİYOR.**
Bu kayıt uygulanan kontrolleri ve kalan imzalı insan kararlarını ayırır. Tamamlanmamış onaylar PASS olarak etiketlenmez.

## 1. Yetkili commit zinciri

| Konu | Kayıt | Yönetici kararı |
| --- | --- | --- |
| DBO/NRBO akademik P1 | PR #8, merge `d3f71b480ac40778f899dcc51c5cade360fd9075` | Önceki bağımsız inceleme kapsamında kapalı; erişilemeyen orijinal NRBO denklem numaraları doğrulanmış sayılmaz |
| Şeref kapsamının devri | PR #9, merge `26c4b89a9e80108e14a52514c239ca44fef25ef9` | NEH, DE/PFSP yöntem metni, bağımsız schedule/Cmax araçları yönetici tarafından tamamlandı; yazar katkıları buna göre taslakta düzeltildi |
| Deney altyapısı / PR #5 | merge `a37ef0e241517a446355a58869a14837fa7427bf` | Kabul edilmiş |
| METHOD-FREEZE | `df8ac616165dc0105c83429e5ed000f34045aafa` | Yönetici tarafından yöntem/davranış başlangıcı olarak onaylandı |
| 45 koşuluk dry-run | `ef03abafe12d5c07403771d83f89358514cf5533` | 15 CSV, 45 koşu, 1.350.000 FE raporlanmış; pilot kanıt ayrı, final bilimsel veri değil |
| Deney hazırlığı | PR #10, merge `73ce39c78a6263ce6f252267edeff0515157aca1` | Son final deneyin temiz başlangıç SHA'sı; manifest kanıtı var |
| 450 koşuluk sonuçlar | PR #11, merge `3589e6ba4c4d48db46a6c9271cdba91737f3daf2` | Final veri, manifest, hash ve validator entegrasyonu; P0/P1 doğrulama ayrıca yapıldı |
| Bilal makale | PR #12, merge `764a2e1ba40c29e4257e13b816cbe38b5198e390` | Ders makalesi, İngilizce NASE taslağı, sayısal tablolar, Gantt'lar; yönetici incelemesinde bulunan dil/katkı/durum hataları düzeltildi |
| Yönetici bağımsız testler | `tests/test_manager_final_acceptance.py` | CI + ikinci bağımsız inceleme için tekrar çalıştırılabilir sözleşme |

**Protokol istisnası:** `73ce39...` temiz deney checkout'u manifestte kayıtlı olmakla birlikte, 450 koşu **başlamadan önce** verilen açık yönetici EXPERIMENT-FREEZE onayını gösteren ayrı bir zaman damgalı kanıt tespit edilemedi. Sonradan ön onay verilmiş gibi tarih yazılamaz. Kod/manifest/hash zinciri kanıtıyla sonuçlar teknik incelemeye alınmıştır; bu governance sapması final bağımsız QA'ya bildirilir.

## 2. Yönetici görevlerinin teknik durumları

- **P1 ve PR #5:** Kapalı; önceki kabul/merge zinciri kaydedildi.
- **RIME son yöntem ve parametre:** `paper/method_rime.md`, `src/algorithms/rime.py`, manifest ve `src/main.py` için `pop_size=30, w=5`. Soft/hard-rime, greedy seçim, sınır ve exact FE açıklaması uyumludur; iterasyon→FE uyarlaması gizlenmemiştir.
- **METHOD-FREEZE ve deney kimliği:** Sürüm değişiklikleri izlenebilir. Deney sonrası PSO kod farkı yalnız açıklama/yorum satırıdır; validator düzeltmesi bilimsel ham veri üzerinde işlem yapmaz.
- **Results/Discussion:** 15 CSV, 450 koşu, 13.500.000 FE ve 3 benchmark; ham hashleri `results/verification.json`; testler `tools/check_experiment_outputs.py` ve `tests/test_manager_final_acceptance.py`. Tablo ve anlatım `paper/outline.md` / `paper/manuscript_nase_en.md` içinde gerçek kayıtlara bağlanır.
- **Final en iyi çizelgeler:** ta001=1288 (DE), ta011=1586 (RIME), ta021=2318 (DE/PSO eşit). Üç seçili Gantt bağımsız `verify_final_schedule.py` ile Cmax/çakışma/iş önceliği açısından doğrulanır. Bunlar **gözlenen minima**, kanıtlanmış optimum değildir.
- **NEH karşılaştırması:** ta001=1286, ta011=1680, ta021=2410. ta001'de NEH, 450 koşuluk meta-sezgisel taramada gözlenen minimum 1288'den daha iyidir; bu ayrım tartışmada korunmalıdır.
- **İstatistik:** Friedman p değerleri: ta001=0.0200975631, ta011=2.1052029617e-11, ta021=1.7514143841e-14. Sonuçlar `results/verification.json` içinde. Her üçünde Nemenyi/CD koşulu sağlanır. Ayrık Cmax bağları ve rank-sum/Friedman varsayımları ile veriden seçilen referansın sınırları metinde açıkça raporlanmalıdır.

## 3. Kabul kapısı matrisi

| Kapı | Durum | Dayanak |
| --- | --- | --- |
| PFSP model/veri SHA ve referans permütasyon | KABUL | Mevcut teknik CI ve önceki model onayı |
| Beş algoritma, seed, FE, sınırlar | KABUL | Contract testleri; kaynak/uyarlama notları |
| Final 450 ham CSV / manifest / SHA-256 | KABUL için yeniden doğrulanır | Bilal numerical-block check + manager final test + bağımsız QA |
| Final en iyi Cmax/Gantt | KABUL için yeniden doğrulanır | Üretim modelinden bağımsız verifier ve schedule CSV |
| Ders makalesi sayısal/tablo tutarlılığı | KABUL için yeniden doğrulanır | `tools/prepare_paper_assets.py --check` |
| İngilizce NASE metni | DÜZELTİLDİ; dergi şablonu bekliyor | Tüm veri tablolarında İngilizce etiketler, kaynak sayılarında değişiklik yok |
| Yazar adları/iletişim/ORCID | **ONAY BEKLİYOR** | E-posta/ORCID ve sorumlu yazar teyit edilmedi |
| Yazar sırası ve gerçek CRediT | **ONAY BEKLİYOR** | Şeref'in devredilen görevleri taslakta düzeltildi; tüm yazarların onayı yok |
| COI/funding/AI/etik/data-code erişimi | **ONAY BEKLİYOR** | İnsan beyanı üretilemez; taslaklar kesin kayıt değil |
| Deney cihazı CPU/RAM/yük bilgisi | **KANIT BEKLİYOR** | Manifest işletim sistemi/yazılım içeriyor, CPU/RAM yok |
| Resmî NASE DOCX/dil/görsel danışman kontrolü | **ONAY BEKLİYOR** | Markdown metni gönderilebilir DOCX değildir |
| Önceden verilmiş EXPERIMENT-FREEZE onay kanıtı | **PROTOKOL SAPMASI KAYITLI** | Temiz SHA var, pre-run yönetici onayı ayrı gösterilemedi |
| Harici bağımsız final QA | **BEKLİYOR** | [Devir paketi](INDEPENDENT_QA_HANDOFF.md) hazır |

## 4. Main/promosyon kararı

**`develop -> main` bugün otomatik onaylanamaz.** Kurum/dergi beyanları, yazar doğrulamaları, CPU/RAM, resmî DOCX ve bağımsız inceleme tamamlanmadan projeye `P0=0/P1=0 final release` denilmez. `main` geçmişi yeniden yazılmaz; yukarıdaki kanıtlar kapatılınca normal PR ve Ubuntu/Windows CI ile ilerlenir.

Teknik testlerin PASS olması akademik beyan onayının yerine geçmez. Nihai uygunluk kuralları, sonuçları güzelleştirmek için değiştirilmez.
