> Güncel ortak standart: [PFSP Ortak Proje ve Makale Çalışma Kılavuzu](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md). Yetki sırası: resmî ders belgeleri → ilgili dergi kuralları → ortak kılavuz → kişisel yönerge → sprint kararı. Eski durum notları tarihsel kayıttır; güncel Bilal teslim durumu sprintler/07_Bilal_Literatur_Teslim_Kaniti.md dosyasındadır.

# PFSP - 18 KASIM 2026 İLK EKİP TESLİM PLANI

**Kapsam:** 5 kişilik onaylı ekip, Problem 7, makale tamamlanma deadline 03.12.2026. 18.11.2026 Çarşamba 19.00 ilk somut ara teslim. 3 Aralık için gün/saat düzeyi belirtilmedi; daha erken son gönderim gerekirse danışman duyurusu üstündür. Resmî ders belgelerindeki proje final tesliminden farklı bir iç tarihtir; karışıklık bırakmayın.

| Görev sahibi | 18 Kasım zorunlu/öncelikli çıktılar | İnceleme | Kanıt / kabul |
|---|---|---|---|
| Muhammed | yönetim panosu; araştırma planı; RIME başlangıç uygulaması | Burak, Tarık, Bilal | güncel commit, plan, smoke testi ve dürüst durum |
| Burak | ortak API; DBO çalışan prototip; NRBO yöntem+iskelet | Şeref, Tarık | DOI/denklem, çalışan test, açık kısmi durum |
| Şeref | ta001/ta011/ta021 kaynakları; PFSP problem.py; mini test Cmax 20 | Burak, Tarık | dosya hash, validasyon ve sayısal test |
| Tarık | deney protokolü; testler; PSO pilotu | Burak, Şeref | seed/FE testi, pilot raporu |
| Bilal | ≥8 birincil kaynak; matris; 500–700 kelimelik giriş; makale iskeleti | Muhammed, Şeref | DOI doğrulama, atıf denetimi, belgesel iz |

## Kontrol takvimi (Türkiye saati)

| Tarih / saat | Kontrol |
|---|---|
| 16 Kasım 12.00 | Üyeler iş kabulü, repo erişimi, engel bildirimi |
| 16 Kasım 21.00 | Dosya bağlantıları ve ilk durum raporu |
| 17 Kasım 22.00 | Bireysel öz-kontrolün tamamlanması |
| 18 Kasım 14.00 | İncelemeye dosya/PR/sürüm teslimi |
| 18 Kasım 17.00 | Ret raporuna göre düzeltme ve yeniden kontrol |
| 18 Kasım 19.00 | Yönetici nihai kabul tablosu ve derste sunulacak kanıtlar |

## 19 Kasım–3 Aralık hızlandırılmış program

| Aralık | Teknik | Makale |
|---|---|---|
| 19–21 Kasım | DE/PSO/RIME/DBO/NRBO gerçek uygulamaları tamamlama | Yöntem alt başlıkları ve literatür matrisi |
| 22–23 Kasım | Beş algoritma entegrasyon ve bağımsız FE/seed test kapısı | Materyal ve metot bölümü |
| 24–27 Kasım | 3 benchmark × 5 algoritma × 30 koşu; ham sonuç kayıtları ve tekrarlı doğrulama | Deney taslak tablolarının gerçek verilerle doldurulması |
| 28–30 Kasım | Wilcoxon sıra toplamı/Holm, Friedman/Nemenyi, RPD/NEH/Gantt, hatalı koşuların retesti | Deneyler, tartışma ve sonucun yazılması; giriş revizyonu |
| 1 Aralık | Sonuç/makale/kod çapraz incelemesi | Tam makale taslağı danışmana verilir (ekip içi hedef) |
| 2 Aralık | Yeniden üretim, açık P0/P1 kapama | Tam metin ve dergi şablonu son kontrolleri |
| 3 Aralık | Nihai durum raporu | Makale tamamlanır; ayrıca dergiye gönderim gereksinimi/tarihi danışmanla teyit edilir |

**Koruma kuralı:** İlk üç hafta yerine 18 gün kalmıştır; nice-to-have problem-özel hibrit/ek benchmark çalışması zorunlu testler ve tam makale tamamlanmadan önceliklenmez.

# ORTAK PROJE BAĞLAMI VE DEĞİŞMEZ KURALLAR

- **Proje:** YMM4142 Optimizasyon Teorisi, onaylı Problem 7 — Permütasyon Akış Tipi Çizelgeleme Problemi (PFSP), amaç **makespan / Cmax minimizasyonu**; toplam akış süresi ΣCj ile karıştırma.
- **Ekip:** Muhammed (proje yöneticisi, makale baş editörü, RIME), Burak (teknik lider, DBO/NRBO), Şeref (veri, matematiksel model, DE), Tarık (test, istatistik, PSO), Bilal (literatür, makale, Gantt). Beş kişilik çalışma öğretim üyesince onaylandı.
- **GitHub depo adı:** `Akis_Tipi_Cizelgeleme`. Depo durumunu son commit üzerinden doğrula; dosya varlığını çalışma kanıtı sayma. Kod Python ve dersin mevcut şablonuna uygun olmalı.
- **Seçilen 5 algoritma:** DE, PSO, DBO, RIME, NRBO. En az 3'ü 2022+ hakemli özgün yayına dayanır; her algoritmanın gerçek DOI/künye ve denklemleri doğrulanır. NEH yalnızca ek klasik referans, beşli sayıya dahil değil.
- **Benchmark:** ta001 = 20×5 / 20.000 FE, ta011 = 20×10 / 30.000 FE, ta021 = 20×20 / 40.000 FE. Nihai deney: algoritma başına test başına en az 30 bağımsız koşu, toplam 450 koşu ve 13,5 milyon FE. Seeds kaydedilir, `np.random.default_rng(seed)` kullanılır. Ara koşularla nihai bilimsel üstünlük iddiası kurulmaz.
- **Modelin gerçek hesabı:** `decode(x)=argsort(x)` ve `C[i,j]=max(C[i-1,j],C[i,j-1])+p[pi[i],j]`. Her aday eksiksiz ve tekrarsız permütasyon oluşturmalıdır. PFSP'de ek ceza ihlali normalde yoktur.
- **Kritik doğrulamalar:** 5 iş×3 makine belgelenmiş örnekte `(J4,J2,J1,J5,J3)` → Cmax=20. Kaynağı ve permütasyonu gerçekten doğrulanmış ta001 referansı ile Cmax=1278; elde değilse testi başarılı göstermeden engel kaydı aç. Dizin/indeks sırasını doğrula.
- **Örnek şablon tuzakları:** Kaynak paketin `problem.py` dosyası sphere/küre örneğidir, PFSP değildir. `python src/main.py --check` tek PSO+örnek problemle bile başarılı dönebildiğinden tek başına nihai kabul kanıtı olamaz. `--only-analysis` bazı eksik dosyaları atlayabilir; dosya varlığı ayrıca kontrol edilir.
- **Hazır meta-sezgisel optimizasyon kütüphaneleri** nihai deneyde kullanılmaz; özgün algoritmalar ekip tarafından gerçeklenir. Kaynakların doğrulanmamış bilgilerini ve uydurulmuş sonuçları raporlamayın.
- **İki tarih:** Ekip içi ilk teslim **18.11.2026 Çarşamba 19.00 (Türkiye saati)**. **Tam makalenin bitiş tarihi 03.12.2026**; saat ilan edilmediği için ekip 02.12'yi iç kontrol hedefi alır. Bu tarihler önceki Ocak 2027 planı yerine geçer; dergiye gönderimin ayrıca resmî gerekliliği varsa danışmanla takvimlendirilir.
- **Resmî kaynak önceliği:** Problem7_Akis_Tipi_Cizelgeleme.docx, Proje_Oneri_Basvuru_Formu.docx, Makale_Yazim_Kilavuzu_ve_Taslagi.docx, Baslangic_Rehberi.docx, YMM4142-ProjePaketi.zip. Kişisel yönergeler ekip operasyon kuralıdır; resmî belgeyle çelişirse resmî olan üstün gelir.

## Ortak ön-kabul süreci

1. **Kendi kontrolü:** Sorumlu tüm maddeleri test eder, tam sonuçları ve sürümü kaydeder. Eksikse `DÜZELTME_GEREKİYOR` veya `BLOKE`, hiçbir zaman `TAMAMLANDI` değil.
2. **Kanıtla inceleme:** 18 Kasım 14.00'e kadar özgün kaynak/kod/rapor, commit SHA ya da dosya sürümü, komutlar ve test sonuçları bağımsız incelemeciye gider. İncelemeci asgari bir kritik testi bizzat tekrarlar.
3. **Düzeltme ve yeniden test:** 18 Kasım 17.00'ye kadar tespit edilen P0/P1'ler kapatılır. Düzeltilen commit üzerinde yeniden test olmadan kabul verilmez.
4. **Nihai rapor:** 18 Kasım 19.00'da yöneticinin kabul panosu güncellenir; teslim edilmiş olmayan işler dürüstçe `BLOKE` olarak listelenir, saklanmaz. Yönetici de kendi kodunu tek başına onaylayamaz.
5. **Rapor biçimi:** `Görev / sahip / sürüm-SHA / dosyalar / beklenen-gözlenen / komut-kayıt / öz-kontrol PASS-FAIL / bağımsız denetçi kararı / açık hata-P0-P1-P2 / istenen düzeltme / yeni tarih`.

**P0:** Sahte sonuç, yanlış amaç/model, FE aşımı, yanlış veri veya çoğaltılamayan kritik hesap; **P1:** eksik DOI/test/kanıt, kurala aykırı uygulama; **P2:** biçim ve küçük anlatım eksikleri. P0/P1 varken tam kabul yok. İnceleme esnasında engel raporu yöneticiye hemen ulaşabilir; bu, tamamlanmış eser teslimi anlamına gelmez.

**18 Kasım ara saatleri:** 16 Kasım 12.00 görev/ortam teyidi; 16 Kasım 21.00 ilerleme; 17 Kasım 22.00 öz-kontrol; 18 Kasım 14.00 incelemeciye teslim; 18 Kasım 17.00 düzeltmeler; 18 Kasım 19.00 yöneticinin derlemesi.
