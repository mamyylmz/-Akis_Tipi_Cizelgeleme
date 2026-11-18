> Güncel ortak standart: [PFSP Ortak Proje ve Makale Çalışma Kılavuzu](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md). Yetki sırası: resmî ders belgeleri → ilgili dergi kuralları → ortak kılavuz → kişisel yönerge → sprint kararı. Eski durum notları tarihsel kayıttır; güncel Bilal teslim durumu sprintler/07_Bilal_Literatur_Teslim_Kaniti.md dosyasındadır.

# 18 KASIM 2026 KİŞİYE ÖZEL İLK SPRINT GÖREVİ

**Sürüm:** 1.0 (15.11.2026) · **Durum:** Ekip içi görev ataması; henüz teslim/PR oluşturulmadı

**Öncelik kuralı:** Bu belge, önceki bireysel yönergenin **sadece kısa dönem tarih ve teslim kapsamını** somutlaştırır; görev/otorite sınırlarını değiştirmez. 03.12.2026 makale deadline'ı, önceki Ocak 2027 varsayımsal planının yerine geçer. Kendi tam kişisel yönergeni ve resmî ders belgelerini de kullan.

**Görev sahibi:** Bilal

**Rol:** Literatür / kaynak doğrulama / bilimsel yazım / Gantt sahibi

**İlk teslim:** 18.11.2026 Çarşamba 19.00 (Türkiye saati)

**Nihai makale:** 03.12.2026 (saat henüz belirtilmedi)

## BU SPRINTTE SENİN GÖREVLERİN

1. **Birincil literatür (`M1`)**: En az **8 doğrulanabilir akademik kaynak** için literatür matrisi hazırla (hedef 10–12): Taillard 1993, NEH 1983, random-key Bean 1994, seçilen 5 algoritmanın özgün yayınları ve mümkünse 2022+ PFSP karşılaştırma yazıları. Her kaynak için tam künye, DOI veya resmî yayın sayfası, gerçekten okunan özet/metin, yöntem ve ilgisi. DOI uydurulamaz.
2. **Araştırma boşluğu:** `paper/literature_matrix.csv` veya `.md` ile birlikte `paper/gap_analysis.md` dosyasında kaynaklarla desteklenmiş 2–3 araştırma sorusu adayı yaz; doğrulanmadan 'literatürde ilk' iddiası kurma.
3. **Giriş (`M2`)**: `paper/introduction_draft.md` içine 500–700 kelimelik atıflı ilk taslak: PFSP tanımı, Cmax, NP-zorluk, random-key temsil, adil FE karşılaştırmasının bilimsel gerekçesi, çalışma amacı; nihai deney sonuçlarını içermez.
4. **Makale iskeleti (`M7`)**: Kılavuzdaki bütün başlıkları, yazar/ORCID ve etik/AI beyanı kontrol alanlarını içeren `paper/outline.md`; en az iki hedef dergi için resmî amaç-kapsam ve şablon linki, uygunluk ve biçim tablosu. Resmî site teyidi yapılamazsa 'doğrulanmadı' yaz.
5. **Gantt (`K9`) hazırlığı**: Küçük 5×3 örnek üzerinde doğru görsel oluşturmak için Şeref'ten gerçek başlangıç/bitiş zamanlarını iste; veri gelmezse yalnızca şema taslağı ve çizim planı hazırla; uydurma Gantt üretme.

## TESLİM EDECEĞİN KANITLAR

`paper/literature_matrix.csv` veya `.md`, `paper/gap_analysis.md`, `paper/introduction_draft.md`, `paper/outline.md`, `docs/journal_shortlist.md`, `docs/gantt_plan.md`

## BİREYSEL ÖZ-KONTROL LİSTESİ

- [ ] En az 8 gerçek birincil akademik kaynak kaynağı ve DOI/künye doğrulaması mevcut.
- [ ] Matris kaynakların ne yaptığını ve sınırlarını doğru açıklıyor; çelişen yayın bilgileri işaretli.
- [ ] 500–700 kelimelik Giriş taslağında her özgül iddiaya gerçek kaynak verilmiş.
- [ ] Makale iskeleti hazır, sonuç/abstract alanlarında uydurma veri yok.
- [ ] Dergi önerilerinde kaynaklar resmî siteye dayalı, erişim tarihi kayıtlı.
- [ ] Muhammed ve Şeref kaynak/model denetimi yaptı.

## BAĞIMSIZ İNCELEME VE SONUÇ

Muhammed akademik bütünlük ve araştırma sorusunu, Şeref matematiksel terminolojiyi ve model referanslarını kontrol eder.

**Teslim süreci:** 18 Kasım 14.00 inceleme, 17.00 düzeltme, 19.00 nihai kabul. Başarısızlığı saklama: görev kısmi ise tam değil `KISMİ`, çalışmayan bölüm varsa `BLOKE` bildir.

## 18 KASIM SONRASI, 3 ARALIK HEDEFİNİN PARÇASI

19–23 Kasım: literatür matrisini genişlet, Gantt çizim uygulamasını tamamla; 24–29 Kasım: sonuçlarla destekli tartışmaya kaynak katkısı; 30 Kasım–2 Aralık: makale şablon, kaynakça, dil kontrolü.

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
