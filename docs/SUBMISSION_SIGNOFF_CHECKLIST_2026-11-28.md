# PFSP yazar/danışman kabul ve teslim kanıt paketi — 28.11.2026

**Durum: ONAY BEKLİYOR.** Bu belge boş alanları doldurmak, kaynak bağlantısını eklemek ve kişisel onayları doğrulanabilir şekilde kaydetmek içindir. Yazar veya danışman yerine imza/çıkar çatışması/finansman/etik onayı verilmez. Mevcut `paper/manuscript_nase_en.md` İngilizce bilimsel metni korunur; bu dosya editöryal son kapıdır.

## A. Kanıtlanmış teknik temel

- Final deney checkout'u: `73ce39c78a6263ce6f252267edeff0515157aca1`.
- Final deney: 15 CSV, 450 koşu, 13.500.000 FE; seed 2026–2055.
- Başarılı PR QA: https://github.com/mamyylmz/-Akis_Tipi_Cizelgeleme/actions/runs/46145535110 — Ubuntu/Windows Python 3.12, **90 test/platform PASS** ve `PAPER CHECK: PASS`. Bu, bağımsız bilimsel hakem onayı değildir.
- Ön denetim: `docs/FINAL_INDEPENDENT_AUDIT_2026-11-28.md`.
- Deney öncesi açık EXPERIMENT-FREEZE yönetici onayının ayrı zaman damgası bulunamamıştır. Bu **protokol sapması** korunur; sonradan “önceden onaylı” yazılmaz.

## B. Yazar katkı ve kimlik onay tablosu

Dergi için e-posta, ORCID, kurum adresi, gerçek CRediT katkıları ve yazılı onay zorunludur. Aşağıdaki katkı ifadeleri yalnız çalışma taslağıdır.

| Taslak sıra | Ad-soyad | Taslak rol | ORCID/e-posta | İmzalı onay |
| --- | --- | --- | --- | --- |
| 1 | Abdullah ELEN | Supervision — danışman tarafından doğrulanacak | BEKLİYOR | BEKLİYOR |
| 2 | Muhammed YILMAZ | Project administration; RIME/NEH, bağımsız schedule, DE/PFSP metodoloji entegrasyonu, validation, editing | BEKLİYOR | BEKLİYOR |
| 3 | Burak Münteha ELLİK | DBO/NRBO software, methodology | BEKLİYOR | BEKLİYOR |
| 4 | Şeref TEKMAN | İlk benchmark/model desteği; gerçekleşen model validation katkısı doğrulanacak | BEKLİYOR | BEKLİYOR |
| 5 | Tarık KARAOĞLAN | PSO, experiment runner, formal analysis, validation | BEKLİYOR | BEKLİYOR |
| 6 | Bilal Erkan TAŞKIN | Literature, manuscript drafting/editing, visualization | BEKLİYOR | BEKLİYOR |

**Sorumlu yazar:** [KİM?] — [KURUMSAL E-POSTA] — [ORCID] — [DANIŞMAN ONAYI/BAĞLANTI].

Her yazar için kaydedilecek asgari kanıt: katkı onayı bağlantısı (GitHub comment/kurumsal e-posta), ORCID ve e-posta doğrulama, sıralama onayı, sorumlu yazar teyidi. `Şeref` kapsamındaki devredilen NEH/DE/model ve final schedule işleri otomatik olarak iki kişiye birden yazılamaz.

## C. Makale beyanları — yalnız insan tarafından doğrulanır

Her yazarın açık beyanı + kanıt bağlantısı gerekir:

1. **Çıkar çatışması:** var/yok, varsa ilgili taraflar ve etkiler; [ONAY/URL/TARİH].
2. **Finansman ve teşekkür:** proje/grant numarası; yoksa açık “harici finansman yok” teyidi; [ONAY/URL/TARİH].
3. **AI araçları:** kullanılan tüm araçlar, hangi aşamalarda kullanıldığı ve yazarın doğrulama sorumluluğu; [ONAY/URL/TARİH]. ChatGPT/Codex taslağı `paper/manuscript_nase_en.md` içinde mevcut, diğer araçlar doğrulanmadı.
4. **Etik:** kamuya açık sayısal benchmarklarda insan/hayvan verisi yok; derginin etik kurul istisnası/kurum politikasını danışman doğrulasın; [ONAY/URL/TARİH].
5. **Veri/kod erişimi ve lisans:** kamuya açık repo izinleri, üçüncü taraf veriler, yeniden dağıtım koşulları; DOI yoksa DOI uydurulmaz; [ONAY/URL/TARİH].
6. **Özgünlük ve daha önce yayımlanmama/başka dergiye eşzamanlı gönderilmeme:** tüm yazarların açık teyidi; [ONAY/URL/TARİH].

## D. Tarık'ın deney makinesi kanıtı

Manifestte OS/Python ve paket sürümleri var; **CPU/RAM/arka plan yükü/enerji modu yok**. Gerçek deneyin yapıldığı **aynı makineden** elde edilecek birincil kayıt veya o tarihten kalmış log gereklidir:

| Alan | Birincil değer / kaynak | Teyit |
| --- | --- | --- |
| CPU modeli, çekirdek/saat bilgisi | [BELİRLENECEK] | [TARIK] |
| RAM toplamı / hız / kullanılabilir RAM | [BELİRLENECEK] | [TARIK] |
| İşletim sistemi / sürüm | Manifestte Windows-10-10.0.19045-SP0; operatör doğrulayacak | [TARIK] |
| Güç modu, CPU sınırlaması, çalışan diğer yükler | [BELİRLENECEK] | [TARIK] |
| Ölçülen süre metodolojisi ve süreç paralelliği | [BELİRLENECEK] | [TARIK] |
| Kayıt tarihi, log/dosya ve güvenilirlik | [BAĞLANTI] | [TARIK] |

**Önemli:** Bugün çalıştırılan `systeminfo`/`Get-CimInstance` komutu, deney gününde sistem donanımı veya güç modunun aynı olduğunu **kanıtlamaz**. Geriye dönük doğrulama varsa kaynağı, yoksa “not recorded / unverified” sınırlaması yazılmalıdır. Deney süresi için donanımlar arası üstünlük genellemesi yapılmaz.

## E. Bilimsel metodoloji, kaynak ve istatistik imzası

- [ ] Tarık + Şeref + danışman: `ranksums` bağ düzeltmesi eksikliği; Friedman ortak-seed blok varsayımı; datadan seçilen referans ve Holm ailesi. P-değerleri yazardan onay almadan değiştirilmedi.
- [ ] Burak + danışman: DBO/NRBO denklem-kod eşleşmeleri ve erişilemeyen kaynak denklem numarası sınırları.
- [ ] Muhammed + danışman: RIME FE uyarlaması, DE/NEH sınırları ve Cmax'nin toplam tamamlanma süresiyle karıştırılmaması.
- [ ] Tüm yazarlar: NEH ta001=1286 iken gözlenen en iyi meta-sezgisel 1288; sonuç anlatımı bu farkı saklamaz.
- [ ] Danışman: hedef dergi, yazar listesi, etik gereklilik ve gönderim izni.

## F. NASE biçim ve dosya kabulü

Resmî kurallar: https://dergipark.org.tr/en/pub/nase/writing-rules — İngilizce; resmî Manuscript Template (https://dergipark.org.tr/en/download/journal-file/29916); tek sütun, TNR 10 pt, 1.15 aralık, kenarlar 2.5 cm, title 12 pt, abstract 150–300, 5–8 keyword, 9 pt referans, Word Equation Editor ile numaralı denklemler. Çift-kör hakemlik ile kimlik alanlarının yerleşimi derginin güncel yönergelerine göre kontrol edilmelidir.

- [ ] Resmî DOCX şablonuna makalenin **tam** İngilizce metni, 16 sayısal blok, görseller, denklemler ve kaynaklar aktarılacak.
- [ ] Yazar e-postaları, ORCID, adresler, beyanlar doğrulanmış gerçek kayıtlarla doldurulacak.
- [ ] Word render/PDF export ile hiçbir tablo, şekil, denklem veya sayfa taşması olmaması kontrol edilecek.
- [ ] NASE başvuru kuralı, danışman imzası ve varsa kör değerlendirme için kimliksiz dosya ayrı doğrulanacak.

**Kapanış kapısı:** En az iki platformda teknik CI PASS, bağımsız bilimsel değerlendirme, tüm yazar/danışman onayları, resmî DOCX/PDF görsel QA ve `develop`→`main` PR'da kontrollü entegrasyon. Bunlar olmadan `READY FOR SUBMISSION` veya `P0/P1=0` denilmez.
