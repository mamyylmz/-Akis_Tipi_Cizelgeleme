> Güncel ortak standart: [PFSP Ortak Proje ve Makale Çalışma Kılavuzu](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md). Yetki sırası: resmî ders belgeleri → ilgili dergi kuralları → ortak kılavuz → kişisel yönerge → sprint kararı. Eski durum notları tarihsel kayıttır; güncel Bilal teslim durumu sprintler/07_Bilal_Literatur_Teslim_Kaniti.md dosyasındadır.

# 18 KASIM 2026 KİŞİYE ÖZEL İLK SPRINT GÖREVİ

**Sürüm:** 1.0 (15.11.2026) · **Durum:** Ekip içi görev ataması; henüz teslim/PR oluşturulmadı

**Öncelik kuralı:** Bu belge, önceki bireysel yönergenin **sadece kısa dönem tarih ve teslim kapsamını** somutlaştırır; görev/otorite sınırlarını değiştirmez. 03.12.2026 makale deadline'ı, önceki Ocak 2027 varsayımsal planının yerine geçer. Kendi tam kişisel yönergeni ve resmî ders belgelerini de kullan.

**Görev sahibi:** Şeref

**Rol:** Veri ve matematiksel model doğrulama / DE sahibi

**İlk teslim:** 18.11.2026 Çarşamba 19.00 (Türkiye saati)

**Nihai makale:** 03.12.2026 (saat henüz belirtilmedi)

## BU SPRINTTE SENİN GÖREVLERİN

1. **Gerçek veri (`K1`)**: Taillard'ın ta001, ta011, ta021 örneklerini güvenilir orijinal kaynaktan `data/` içine al; satır/sütun, indeksleme, kaynak bağlantısı/erişim tarihi ve SHA256 değerini `data/README.md` içine yaz. Veri içeriği doğru olduğundan emin ol; veriyi uydurma.
2. **Asıl matematiksel model (`K2`)**: Örnek sphere işlevlerini gerçek PFSP `src/problem.py` ile değiştir. `decode(x)=np.argsort(x, kind='stable')` veya eşdeğer deterministik uygun sıralama; gerçek amaç yalnızca Cmax; `constraints()` boş dizi. `Problem`, `INSTANCES`, `MAX_FES`, `details` şablon sözleşmesine uysun.
3. **Birim testleri:** 5×3 örnek veri üzerinden verilen permütasyon için Cmax=20; üç benchmark için doğru boyut, tekrar etmeyen `argsort`, örnek bir permütasyon için iki hesap yolunun aynı sonucu üretmesi. Ta001 için 1278 kontrolünü yalnızca gerçek referans permütasyonu varsa PASS işaretle; yoksa doğrulama açığı olarak belirt.
4. **Metot (`M3`)**: `paper/method_model.md` dosyasında amaç fonksiyonu, Cmax yinelemesi, varsayımlar, random-key, RPD, FE ve model doğrulamayı kendi cümlelerinle yaz.
5. **DE hazırlığı (`K6`)**: DE özgün kaynağının parametre ve uygulama notunu oluştur; `de.py` ilk iskeletini API uyumlu hazırla. Tamamlanmamış algoritmayı çalışır olarak sunma.

## TESLİM EDECEĞİN KANITLAR

`data/taillard/*`, `data/README.md`, `src/problem.py`, `tests/test_problem.py`, `paper/method_model.md`, `src/algorithms/de.py` (plan/iskelet)

## BİREYSEL ÖZ-KONTROL LİSTESİ

- [ ] `src/problem.py` sphere örneği değil gerçek PFSP modelidir.
- [ ] Doğru kaynaklı 3 benchmark ve dosya checksum'ları kayıtlıdır.
- [ ] 5×3 küçük örneğin Cmax=20 birim testi PASS.
- [ ] Decode, sabit seed, indeksleme, `maxFEs` ve RPD hesapları sayısal olarak denetlenebilir.
- [ ] ta001/1278 kontrolü ancak kaynak permütasyonla PASS; aksi hâlde açık engel raporu.
- [ ] Burak ve Tarık bağımsız inceleme notu yazdı.

## BAĞIMSIZ İNCELEME VE SONUÇ

Burak kod/API, Tarık bağımsız makespan ve seed testleri yapar. Bilal veri referansını doğrular.

**Teslim süreci:** 18 Kasım 14.00 inceleme, 17.00 düzeltme, 19.00 nihai kabul. Başarısızlığı saklama: görev kısmi ise tam değil `KISMİ`, çalışmayan bölüm varsa `BLOKE` bildir.

## 18 KASIM SONRASI, 3 ARALIK HEDEFİNİN PARÇASI

19–21 Kasım: DE’yi tamamla ve bağımsız test et; 22–23 Kasım: tüm algoritmaların modelle entegrasyonuna yardım et; 24–30 Kasım: sonuç/permütasyon yeniden hesaplama.

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
