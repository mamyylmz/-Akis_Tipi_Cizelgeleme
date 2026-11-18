> Güncel ortak standart: [PFSP Ortak Proje ve Makale Çalışma Kılavuzu](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md). Yetki sırası: resmî ders belgeleri → ilgili dergi kuralları → ortak kılavuz → kişisel yönerge → sprint kararı. Eski durum notları tarihsel kayıttır; güncel Bilal teslim durumu sprintler/07_Bilal_Literatur_Teslim_Kaniti.md dosyasındadır.

# 18 KASIM 2026 KİŞİYE ÖZEL İLK SPRINT GÖREVİ

**Sürüm:** 1.0 (15.11.2026) · **Durum:** Ekip içi görev ataması; henüz teslim/PR oluşturulmadı

**Öncelik kuralı:** Bu belge, önceki bireysel yönergenin **sadece kısa dönem tarih ve teslim kapsamını** somutlaştırır; görev/otorite sınırlarını değiştirmez. 03.12.2026 makale deadline'ı, önceki Ocak 2027 varsayımsal planının yerine geçer. Kendi tam kişisel yönergeni ve resmî ders belgelerini de kullan.

**Görev sahibi:** Burak

**Rol:** Teknik lider / DBO ve NRBO sahibi

**İlk teslim:** 18.11.2026 Çarşamba 19.00 (Türkiye saati)

**Nihai makale:** 03.12.2026 (saat henüz belirtilmedi)

## BU SPRINTTE SENİN GÖREVLERİN

1. **Şablon sözleşmesi:** `src/main.py` ve `src/algorithms/pso.py` içindeki fonksiyon imzası, `best_x/best_f/history/n_fes/time` çıktı alanları ve FE sayım kurallarını incele. `docs/algorithm_interface.md` içinde ortak sözleşmeyi kaydet.
2. **DBO (`K4`)**: Özgün DBO makalesini ve DOI'sini doğrula; adımları ve parametrelerini kendi sözlerinle yaz. `src/algorithms/dbo.py` dosyasının ilk çalışan sürümünü yaz; model hazır değilse temiz bir basit amaç fonksiyonunda smoke test yap ve bunun PFSP doğrulaması olmadığını belirt. Bağımsız testte 2 aynı-seed koşusunun sonucu aynı olsun, FE bütçesi aşılmasın.
3. **NRBO (`K5`)**: Özgün NRBO kaynağını incele; doğru güncelleme denklemleri ve parametre açıklaması, uygulama planı, dosya iskeleti çıkar. Henüz bitmemiş implementasyonu PASS olarak adlandırma; `NotImplementedError` veya açık durum kaydı kullan.
4. **Bağımsız gözden geçirme:** Şeref'in problem modeli ve Muhammed'in RIME tasarım/uygulamasına odaklı en az bir somut teknik inceleme yap. Gördüğün hatayı dosya+satır, beklenen/gerçek değer, düzeltme önerisiyle kaydet.
5. **Makale katkısı:** `paper/method_dbo_nrbo.md` içinde DBO ve NRBO için birincil yayın, arama mekanizması, denklem ve parametre notlarını yaz; sonuç icat etme.

## TESLİM EDECEĞİN KANITLAR

`docs/algorithm_interface.md`, `src/algorithms/dbo.py`, `src/algorithms/nrbo.py` (iskelet), `paper/method_dbo_nrbo.md`, `tests/test_dbo.py`

## BİREYSEL ÖZ-KONTROL LİSTESİ

- [ ] Ortak algoritma arayüzünün tam gereklilikleri belgeli.
- [ ] DBO'nun kütüphane kopyası olmayan doğrulanabilir ilk uygulaması ve en az iki seed/FE testi var.
- [ ] DBO PFSP testi mümkünse gerçek modele bağlandı; değilse açıkça smoke-only etiketlendi.
- [ ] NRBO'da kaynak+denklem+uygulama planı mevcut; tamamlanmadıysa dürüst `KISMİ`.
- [ ] Şeref ve Tarık inceleme kanıtı bulunuyor; kendi kodunu kendin onaylamadın.

## BAĞIMSIZ İNCELEME VE SONUÇ

Şeref özgün denklemleri ve model uyumunu, Tarık FE/seed/test disiplinini kontrol eder.

**Teslim süreci:** 18 Kasım 14.00 inceleme, 17.00 düzeltme, 19.00 nihai kabul. Başarısızlığı saklama: görev kısmi ise tam değil `KISMİ`, çalışmayan bölüm varsa `BLOKE` bildir.

## 18 KASIM SONRASI, 3 ARALIK HEDEFİNİN PARÇASI

19–22 Kasım: DBO ve NRBO’yu tamamla, benchmarkla ilk çalıştırma; 23 Kasım: entegrasyon geçidi; 24–27 Kasım: hatalı deney koşularına teknik destek; 28–30 Kasım: yöntem metni son sürüm.

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
