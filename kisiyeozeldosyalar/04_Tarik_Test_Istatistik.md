> Güncel ortak standart: [PFSP Ortak Proje ve Makale Çalışma Kılavuzu](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md). Yetki sırası: resmî ders belgeleri → ilgili dergi kuralları → ortak kılavuz → kişisel yönerge → sprint kararı. Eski durum notları tarihsel kayıttır; güncel Bilal teslim durumu sprintler/07_Bilal_Literatur_Teslim_Kaniti.md dosyasındadır.

# AKIŞ TİPİ ÇİZELGELEME — TARIK / KİŞİSEL PROJE YÖNERGESİ

**Sürüm:** 1.0 · 15 Kasım 2026  
**Hedef okur:** Tarık ve onunla çalışacak yapay zekâ asistanı  
**Kapsam:** Ortak bilimsel/resmî kurallar + yalnızca Tarık için ayrıntılı görev, yetki ve kabul standardı  
**Kullanım:** Bu dosyanın tamamını tek başına yeni bir sohbet/agent context'ine ekleyin; ek bir ortak yönerge olmadan temel bağlamı içerir.

> **Kullanıcıya not:** Bu dosya **Tarık** için hazırlanmıştır. Temel görevin sonuçların bağımsız doğruluğunu kanıtlamak, adil deneyleri yürütmek ve PSO algoritmasını geliştirmektir; deneyin sayısal raporu senin kontrolündedir.

## A. BU BELGE NASIL KULLANILIR? — BİR YAPAY ZEKÂ OTURUMU İÇİN BAĞLAM

Bu belge, YMM4142 Optimizasyon Teorisi kapsamında **onaylı Problem 7 (PFSP)** projesinin **beş kişilik onaylı ekibinde** tek bir katılımcı için hazırlanmış çalışma yönergesidir. Bu belgeyi okuyan yapay zekâ asistanı:

1. Belgedeki **ORTAK / RESMÎ** gereklilikleri ve **EKİP KARARI** ile belirlenen iç kuralları ayırır. Resmî ders dosyası, danışmanın yazılı kararı veya hedef derginin güncel kuralı ile çelişen ekip kararını kendi başına uygulamaz; çelişkiyi açıkça bildirir.
2. Buradaki görev tanımını bağlam kabul eder; kodun, kayıtların, onayın, takvimin veya deneylerin fiilen tamamlandığını **varsaymaz**. Güncel depoyu, dosyayı, test raporunu görmeden “PASS”, “gönderildi”, “onaylandı” veya “yayına hazır” demez.
3. Bu kişinin kendi sınırları içindeki işlere öncelik verir. Başka üyelerin özel yetki ayrıntılarını üretmez, işlerini onlara devretmez; bağımlılık varsa yalnızca ilgili iş arayüzü üzerinden iletişim önerir.
4. Yeni görevde önce ilgili kabul kriterini ve gerekli kanıtı tanımlar, sonra uygular, **öz kontrol** yapar ve somut bir teslim/iyileştirme raporu sunar. Test edilmemiş çıktıyı test edildi diye göstermez.
5. Bilinmeyen kaynak, DOI, deney sonucu, performans, teslim tarihi, yazar katkısı veya GitHub durumu **uydurmaz**. Erişilemeyen veri için `DOĞRULANAMADI` yazar; engeli ve somut sonraki adımı belirtir.
6. Bu metin başka bir bağlamda tek başına kullanılabilir; ancak resmî belgelerin veya gerçek kaynak kodun **yerini almaz**. Uygulama öncesinde ilgili en yeni dosya, GitHub commit ve varsa danışman bildirimi esas alınır.

## B. ORTAK PROJE KİMLİĞİ VE KAPSAMI

- **Ders:** YMM4142 – Optimizasyon Teorisi; 2026–2027 güz yarıyılı; Bandırma Onyedi Eylül Üniversitesi.
- **Ders sorumlusu/danışman:** Doç. Dr. Abdullah ELEN; ders paketinde verilen GitHub kullanıcı adı: `abdullahelen`.
- **Proje:** **Problem 7 — Permütasyon Akış Tipi Çizelgelemede Makespan Minimizasyonu (PFSP)**; İngilizce: *Permutation Flow Shop Scheduling Problem with Makespan Minimization*.
- **Onay:** Problem 7'nin seçilmesine ve grubun **5 öğrenci** olmasına öğretim üyesinden onay alınmıştır. Ekip üyeleri: **Muhammed, Burak, Şeref, Tarık, Bilal**.
- **GitHub depo adı:** `Akis_Tipi_Cizelgeleme`; mevcut olduğu kullanıcı tarafından bildirilmiştir. Depo URL'si, erişim yetkileri, en son SHA ve branch protection ayarları **gerçek depodan doğrulanmalıdır**. Depoya bu yönergeyle kendiliğinden dosya yüklenmiş değildir.
- **Çalışma dili:** Python; dersin `YMM4142-ProjePaketi.zip` içindeki `SourceCode/` şablonu esas alınır. Makale Türkçe hazırlanabilir; hedef derginin kuralları, Türkçe/İngilizce özet ve makale dili önceliklidir.
- **Hedefler:** (1) resmî puanlama ölçütlerini eksiksiz karşılamak, (2) istatistiksel olarak geçerli ve tekrarlanabilir deney, (3) bilimsel katkı ve uygun bir ulusal mühendislik dergisine gönderim. **Dergiye gönderim**, hakemli **kabul** ile aynı şey değildir; kabul garanti değildir.

### Ortak araştırma sorusu ve yayın stratejisi (EKİP KARARI; henüz doğrulanmış sonuç değil)

**Ana araştırma sorusu:** "Sürekli uzayda çalışan klasik ve 2022 sonrası meta-sezgisel algoritmalar, PFSP makespan problemlerinde ortak `random-key` gösterimi ve eşit FE bütçesi altında hangi çözüm kalitesi ve kararlılığı sağlar?"  
**Yayın katkısı için aday ikinci soru:** "Permütasyon-özel bir insertion/swap yerel arama eklendiğinde, özgün sürüme göre istatistiksel olarak anlamlı fark oluşuyor mu?" Bu ikinci soru, zorunlu beş algoritmanın içine değişiklik sokmadan **ayrı deney** olarak ele alınır. Sonuç oluşmadan "geliştirme üstün" iddiası kurulmaz.

Araştırma hipotezleri: **H1** güncel ve klasik yöntemlerin kalite/kararlılık farkı; **H2** random-key temsili nedeniyle eşdeğer permütasyonların ve düz bölgelerin performansa etkisi; **H3** problem-özel aramanın ayrı deneyde sağlayabileceği katkı. H2'nin sıkı biçimde test edilmesi için gösterim/arama davranışına yönelik ayrı ölçüm tasarımı gerekir; yalnızca beş algoritmanın sonuçlarını karşılaştırmak H2'yi kanıtlamaz. Yayın yeniliği literatür taraması ve sonuçlarla gerekçelendirilmeden kesinleştirilmez.

**Akademik kaynak başlangıçları:** Taillard/flowshop benchmark: `https://people.brunel.ac.uk/~mastjjb/jeb/orlib/flowshopinfo.html`; güncel BKS/permutasyon örnekleri için kaynak-erişim tarihi doğrulanarak `https://zenodo.org/records/18272308`; DergiPark konu sınıflandırması: `https://dergipark.org.tr/tr/pub/subjects`. Bağlantılardaki veriler değişebilir; her kullanımda sürüm ve erişim tarihi tutulur.

### Ortak rol haritası — yalnızca iletişim için

| Kişi | Ekipte görünür iletişim rolü |
|---|---|
| Muhammed | Proje lideri ve nihai teslim koordinatörü |
| Burak | Teknik lider ve algoritma kod inceleme noktası |
| Şeref | Veri / matematiksel model doğrulama noktası |
| Tarık | Bağımsız test / deney ve istatistik doğrulama noktası |
| Bilal | Literatür / atıf ve makale biçimi kontrol noktası |

Bu özet, görev veya otorite devretmez. Diğer kişilerin ayrıntılı iş paketleri yalnızca kendi yönergelerinde yer alır; bir görevin sahipliği ilgili görev kodu ve atanmış sorumlu üzerinden takip edilir.

## C. TEKNİK VE BİLİMSEL SÖZLEŞME (ORTAK / RESMÎ)

### C1. Problemin doğru tanımı

- `n` iş ve `m` makine vardır. Her iş makineleri 1…m sırasıyla gezer; her makine aynı anda yalnızca bir iş işler; işler bölünmez, sırayı geçmez.
- Karar değişkeni işler arasındaki **permütasyon** `π`'dir. Dersin çözüm gösteriminde `[0,1]` aralığındaki `n` boyutlu sürekli `x` vektörü, `numpy.argsort(x)` ile permütasyona çevrilir (`random-key`). Eşit anahtarlarda belirlenimci sıra korunacaksa `kind="stable"` kullanımı tüm algoritmalar için ortaklaştırılır ve belgelenir.
- Hesap: `C[i,j] = max(C[i-1,j], C[i,j-1]) + p[π_i,j]`, sınır koşulları `C[0,j]=C[i,0]=0` olacak şekilde uygun 1-indeks tanımıyla; uygulamada 0-indeks dikkatle düzenlenir.
- **Amaç `min Cmax`**: son işin son makinede bitişi. `Σ C_j` (*total flow time*) **farklı bir amaçtır**; hiçbir tabloda veya makale iddiasında karıştırılmaz.
- Rastgele anahtarların çözümlemesi geçerli permütasyon üretir; problem belgesinde yapısal ceza fonksiyonu gerekmez, `constraints()` boş dizi döndürebilir.
- Çözüm ölçütü: `RPD (%) = 100 × (Cmax - BKS) / BKS`; `BKS`, kullanılan örnek için **en iyi bilinen çözüm** değeridir, her zaman kanıtlanmış optimum değildir. Referans ve erişim tarihi kaydedilir.

### C2. Zorunlu benchmark ve deney bütçesi

| Örnek | Boyut | Algoritma başına/koşu başına maxFEs | Zorunluluk |
|---|---|---:|---|
| ta001 | 20 iş × 5 makine | 20.000 | Zorunlu |
| ta011 | 20 iş × 10 makine | 30.000 | Zorunlu |
| ta021 | 20 iş × 20 makine | 40.000 | Zorunlu |
| ta031 | 50 × 5 | 50.000 | İsteğe bağlı |
| ta041 | 50 × 10 | 60.000 | İsteğe bağlı |
| ta051 veya 100 işli örnek | 50 × 20 / 100 × m | 100.000 | Ek puan adayı |

- **Tam beş meta-sezgisel algoritma**, her zorunlu örnek için **en az 30 bağımsız koşu**: asgari `3 × 5 × 30 = 450` koşu; `13.500.000` amaç fonksiyonu değerlendirmesi. İsteğe bağlı, referans NEH ve parametre ayarlama maliyetleri bu sayıya dahil değildir.
- Ekip algoritma seti: **DE, PSO, DBO, RIME, NRBO**. Algoritmaların **kişiye özel sahipliği**, yalnızca ilgili rol yönergesinde ve gerekli inceleme arayüzlerinde ayrıntılandırılır; tüm kişiler kimin hangi işi neden aldığına ilişkin tam görev matrisini bilmek zorunda değildir. Özgün yayın, DOI, 2022+ yayın koşulu ve danışman onayına ilişkin belgesel kanıt korunmalıdır.
- En az **3 algoritmanın 2022 veya sonrasında hakemli dergi/konferansta yayımlanmış** özgün yayını doğrulanmış olmalı; sonradan yayımlanan basit varyantlar farklı algoritma diye sayılmaz. Güncel üçlü için adaylar DBO, RIME, NRBO'dur; yayın künyesi ve tarih ilk araştırma aşamasında doğrulanır.
- Orijinal algoritmalar kaynak makalelerindeki mekanizmaya sadık biçimde gerçeklenir. `mealpy`, `pymoo`, `niapy`, `DEAP` vb. hazır meta-sezgisel optimizasyon araçları sonuç üretmek için kullanılmaz; yalnızca kendi gerçeklemenizi çapraz kontrol etmek için kullanılabilir.
- NEH (`Nawaz–Enscore–Ham`) **ayrı klasik sezgisel karşılaştırmadır**, beş meta-sezgiselin yerine geçmez. Orijinal beş algoritmaya dersin onaylamadığı yerel arama eklenmez; böyle geliştirme varsa **ayrı ek puan/ablation deneyi** olarak, eşit FE sayımıyla raporlanır.
- Rastgelelik `np.random.default_rng(seed)` ile yönetilir; her koşunun seed değeri saklanır. Aynı koşu ve seed tekrarlandığında aynı sayısal sonuç elde edilmelidir (ortamdan kaynaklı farklılık varsa tespit ve rapor edilir).
- Her algoritma için gerçek amaç değerlendirmeleri (başlangıç popülasyonu ve arama içi değerlendirmeler dahil) sayılır; `n_fes ≤ maxFEs`; eşit bütçe, yöntem ve erken sonlandırma kuralları önceden yazılı olmalıdır.

### C3. Zorunlu doğrulama ve sonuçlar

- Mini örnek: Beş iş × üç makine, `J4,J2,J1,J5,J3` sıralaması için `Cmax = 20`. İşlem süreleri dersin Problem 7 dokümanındaki örnekten alınır.
- `ta001` için **doğrulanmış** iyi bilinen permütasyon girdiğinde `Cmax = 1278` kontrolü; yalnızca sayıyı sabit kodlamak kabul edilmez. Veri kaynağındaki dizi/indeks formatı doğrulanır.
- Her raporlanan `best_x` tekrar `decode/evaluate` içinden geçirildiğinde kaydedilmiş `best_f` değerini verir. Gantt gösterimi aynı sırayı, işlem çakışması olmadan gösterir ve bitişi `Cmax` ile aynıdır.
- Her algoritma/örnek için en iyi, en kötü, ortalama, medyan, standart sapma, uygun çözüm oranı ve ortalama çalışma süresi; ayrıca `RPD`, seed, `n_fes`, en iyi çözüm ve yakınsama geçmişi gerekçesine uygun şekilde saklanır.
- Ders paketi **Wilcoxon sıra toplamı** (α=0,05, Holm düzeltmesi), **Friedman** ve **Nemenyi** analizini öngörür. İstatistik testinin varsayımları, özellikle az sayıda problem örneği ve seed'lerin bağımsız blok sayılması meselesi kontrol edilir; bir testin sonuç verdiği, her genellemenin geçerli olduğu anlamına gelmez. Resmî testler çalıştırılır, yöntemsel sınırlılık dürüstçe raporlanır ve gerekirse danışman görüşü alınır.
- Her örnek için yakınsama, box plot, en iyi permütasyonun **Gantt diyagramı**; grafik ve tablolardaki değerler ham CSV ile birebir uyumlu olmalıdır.

### C4. Kaynak yazılım şablonunun bilinen durumu

- Yüklenmiş `YMM4142-ProjePaketi.zip/SourceCode/` içinde `src/main.py`, `src/problem.py`, `src/stat_tests.py`, `src/visualization.py`, `src/algorithms/pso.py`, `src/algorithms/sablon_algoritma.py`, `data/`, `results/` ve `README.md` bulunur.
- **Yüklenen başlangıç paketinde** `problem.py` PFSP değil **örnek küre (sphere) optimizasyonudur**; PFSP modeliyle değiştirilmeden geçerli sonuç üretmez.
- **Yüklenen başlangıç paketinde** `src/main.py --check` algoritma sayısı beşten az olsa dahi uyarı vererek başarıyla bitebilir. Bu komut **tek başına kabul kanıtı değildir**. Gerçek beş algoritma, üç Taillard örneği, 30 koşu ve dosya doğruluğu ayrıca test edilir.
- `pso.py` paketle gelen örnek koddur. Nihai uygulama Python ile ve ders şablonu temel alınarak oluşturulmalı; kodun hangi kısmının öğretmen şablonu olduğu gizlenmemeli.
- Uzak GitHub deposunun güncel durumu bu paketten türetilemez. Güncel commit kontrolü gereklidir.

## D. AKADEMİK, PUANLAMA VE TESLİM KURALLARI

- Resmî grup notu rubriği: modelleme/doğrulama **15**, algoritmalar **20**, deney/istatistik **20**, yazılım/tekrarlanabilirlik **15**, makale/gönderim **15**, sunum **10**, proje yönetimi **5**; toplam **100**. Koşullara bağlı **en fazla +5** ek puan olanağı var.
- Kodlama görevleri **K1–K10 = 45**, makale **M1–M9 = 40**, sunum **S1–S6 = 15** iş yükü puanı. Her görevde **tam bir S** (sorumlu) bulunmalı, gerçek katkı veren K olarak belirtilmeli. İnceleyici olmak **otomatik K puanı değildir**; yaptığı somut katkı kanıtlanmalıdır.
- Beş kişilik ekip onaylıdır. Eşit katkı için matematiksel referans `100/5 = 20` olsa da herkesin fiilen 20 puan aldığı veya resmî Excel'in otomatik 5 kişilik olduğu **varsayılmaz**. Görev sahibi/katkı ve tamamlanma oranları gerçek kayıtlardan hesaplanır; 8 öğrenci sütunlu resmî Excel'in beş kişilik kullanımı danışman kararıyla netleşir.
- **Yazar sırası ilkesi:** Ders belgesindeki başlangıç kuralı danışman birinci, takım lideri ikinci; diğer öğrencilerin nihai sırası **gerçek katkı puanları** ve danışman kararıyla belirlenir. Yönetici için hazırlanan operasyonel plan bir ön sıralama içerir; bu sıralama diğer rol yönergelerinde görev rekabetine neden olmayacak şekilde detaylandırılmaz. Gerçek katkı, hedef derginin yazarlık şartları, tüm yazarların rızası ve danışman onayı olmadan sıralama kesinleşmez. Katkı göstermeyen kişi yalnızca unvanı/rolü nedeniyle otomatik yazar olmamalıdır.
- Makalede **gerçek ve birincil kaynaklar**, doğrulanmış DOI, deneyle desteklenen iddialar, yeniden üretilebilirlik ve **yapay zekâ kullanım beyanı** bulunmalıdır. Kaynak, sayısal değer, p-değeri, görsel veya sonuç **uydurulmaz**. Tüm üyeler kendi kodunu ve makale katkısını açıklayabilir olmalı.
- Her yazarın DergiPark/ORCID bilgisi, isim/kurum bilgisi doğru olmalı; dergi kapsamı, güncel şablonu, yazarlık/etik/izin kuralları ve danışman gönderim onayı nihai gönderimden önce doğrulanır.
- Proje süresi resmî belgelerde **beş hafta**. M1: öneri formu+matris; M2: `problem.py` doğrulaması; M3: 1–2 sayfa ara rapor, demo, `main.py --check`; M4: 30 koşuluk tam sonuçlar; M5: proje/sunum/makale gönderimi. **Resmî son gün “son ders haftasının son günü”** şeklindedir. Önceki planın 6 Ocak 2027 tarihi teyitsiz planlama üst sınırıdır; bir tarih kesin sayılmadan ders sorumlusunun duyurusu/akademik takvim kontrol edilir. Bu belge hazırlanırken hangi kilometre taşlarının tamamlandığı **bilinmiyor**.
- Son teslim: GitHub private depo ve commit geçmişi, doğru Python kodu/README, ham sonuç CSV ve grafikler, makale hedef dergi şablonunda, DergiPark gönderim teyidi, 15 dk sunum + 5 dk soru-cevap (herkes konuşur), nihai görev matrisleri/katkı hesaplayıcı.

## E. HERKES İÇİN ZORUNLU KALİTE GÜVENCE AKIŞI (EKİP KARARI)

### E1. İş açılışı ve durumlar

Her iş için tekil `görev kodu`, sorumlu, kabul kriteri, teslim tarihi, kaynak/PR/commit ve bağımsız inceleyici kaydedilir. Durumlar:

`PLANLANDI → ÇALIŞILIYOR → ÖZ_KONTROL → İNCELEME_İSTENDİ → (DÜZELTME / ONAY) → BİRLEŞTİRİLDİ`.

Bloke olan görev için tamamlanmış çıktı taklidi yapılmaz; **ENGEL BİLDİRİMİ** açılarak engelin sebebi, kanıtı, etkisi ve istenen yardım bildirilir.

### E2. Üreten kişinin öz kontrolü — liderine göndermeden önce

1. Kendi görev kodu ve kabul kriterlerini tek tek kontrol et; tüm zorunlular **PASS** olmalı. PASS sağlayamıyorsan çalışma `DÜZELTME_GEREKİYOR` konumunda kalır, **nihai teslim olarak gönderilmez**.
2. Çıktıya gerçek dosya/PR bağlantısı, **commit SHA veya belge sürümü**, kaynak listesi, çalıştırılan komutlar, girdi koşulları, test kayıtları ve beklenen/gerçekleşen değerleri ekle.
3. Bilimsel sayılar ham veriyle, makale alıntıları birincil kaynakla, kod çalışması bağımsız tekrar testle uyumlu mu denetle.
4. Geçerli/yürütülebilir çıktı ile “eksik ama üzerinde çalışılıyor” notunu ayır. Başarı iddiasını kanıtsız yapma.
5. Çıktıyı önce atanmış **bağımsız incelemeciye** gönder. İlgili inceleme geçmeden yöneticiye “tamamlandı” deme.

### E3. Bağımsız kontrol ve nihai kabul

- İncelemeci yalnızca beyana değil dosyaya, DOI'ye, ham CSV'ye veya test komutuna bakar; en az bir kritik kontrolü kendi başına yeniden uygular.
- Her görev için **en az bir bağımsız inceleme**; Muhammed'in kendi ürettiği materyallerde **iki bağımsız onay**. Muhammed'in lider olması kendi çıktısına otomatik onay hakkı vermez.
- Yönetici nihai bütünlüğü ve teslim sınırını denetler. Model doğrulamasında Şeref'in, FE/test doğrulamasında Tarık'ın, bilimsel kaynakta Bilal'in, özgün algoritma denkleminde Burak'ın incelemesi önemlidir; nihai yetki gerçek inceleme delillerine dayanır.
- `P0` veya `P1` açıkken merge/teslim yapılmaz. `P2` son teslimden önce kapatılır. Başarısız testin üstü çizilmez; düzeltme commit'i üzerinden **yeniden test** yapılır.
- `main` doğrudan push'a kapalı çalışma hedefidir: ayrı branch + PR + uygun review. GitHub kuralının gerçekten açık olup olmadığı depo ayarlarından doğrulanmalı; yalnızca metin kuralı teknik enforcement değildir.
- Ekipte yöneticinin veya bir görevlisinin çalışmaması hâlinde inceleme başka ehil kişiyle yeniden planlanabilir; değişiklik görev kaydına işlenmeden yetki devredilmiş sayılmaz.

### E4. Hata önceliği ve standart geri bildirim

| Sınıf | Örnek | Sonuç |
|---|---|---|
| **P0 / ENGELLEYİCİ** | yanlış `Cmax`, sahte/uydurma kaynak veya sonuç, farklı amaç fonksiyonu, FE aşımı, çalışmayan zorunlu test, eksik beş algoritma | Hemen durdur; doğrudan lider ve ilgili teknik noktaya engel bildir, tam yeniden doğrula |
| **P1 / ÖNEMLİ** | DOI doğrulanamadı, eksik test kanıtı, 30 koşudan az, hatalı p-değeri yorumu, yanlış grafik/veri eşleşmesi | Onaylama; gerekçeli düzeltme iste, yeni sürümde yeniden kontrol et |
| **P2 / KÜÇÜK** | yazım, etiket, format, README açıklaması | Gerekçeli kayıt; finalden önce kapanış |

**Zorunlu düzeltme kaydı biçimi:**

```
ID: PFSP-[GÖREV]-[SIRA]
Seviye: P0 | P1 | P2
Sorumlu: ...       İnceleyen: ...
Girdi / ortam / dosya veya commit SHA: ...
Beklenen davranış: ...
Gözlenen davranış: ...
Kanıt (komut, log, CSV satırı, DOI, sayfa): ...
Kök neden (biliniyorsa): ...
İstenen somut düzeltme: ...
Tekrar test adımları ve geçme koşulu: ...
Durum: AÇIK | DÜZELTİLDİ | YENİDEN_TEST | KAPALI
```

### E5. Her dosya/çıktıyla birlikte zorunlu teslim özeti

```
GÖREV / ÜRETEN / DOSYA VEYA PR / COMMIT VEYA BELGE SÜRÜMÜ
KABUL KRİTERLERİ: ... (her biri PASS/FAIL/DOĞRULANAMADI)
ÇALIŞTIRILAN KONTROLLER: ... (komut, kaynak, sonuç ve kanıt)
BİLİNEN SINIRLAR / AÇIK HATALAR: ...
ÖZ KONTROL: PASS | FAIL
BAĞIMSIZ İNCELEME: Kim, neyi yeniden yaptı, sonuç ...
NİHAİ DURUM: İNCELEME BEKLİYOR | DÜZELTME | ONAYLI
```

## F. ORTAK REFERANSLAR VE KARAR ÖNCELİĞİ

1. Birincil resmî ders belgeleri: `Problem7_Akis_Tipi_Cizelgeleme.docx`, `Baslangic_Rehberi.docx`, `Proje_Oneri_Basvuru_Formu.docx`, `Makale_Yazim_Kilavuzu_ve_Taslagi.docx`, `Katki_Puani_Hesaplayici.xlsx` ve bunları içeren `YMM4142-ProjePaketi.zip`.
2. Gerçek uygulama: `YMM4142-ProjePaketi.zip/SourceCode/` şablonu ve `Akis_Tipi_Cizelgeleme` GitHub deposunun en son **kontrol edilmiş commit'i**.
3. Algoritma bilimi: DE, PSO, DBO, RIME, NRBO özgün hakemli yayınları; benchmark: Taillard 1993, OR-Library ve özgün referans veri.
4. Hedef derginin güncel yayın/etik/yazarlık kuralları, danışmanın açık onayı ve resmî ders duyuruları.
5. Önceki ekip yönetim paketi ve bu role özel yönerge **operasyonel süreç belgesidir**; resmî kaynakla çatışırsa resmî kaynak üstündür.

İletişim prensibi: Bir kişi başka birinin bütün sorumluluklarını bilmek zorunda değildir; bağımlı olunan çıktının **arayüzü, kabul koşulu, istenecek kanıt ve kime bildirileceği** bilinmesi yeterlidir.

## G. SANA ÖZEL YETKİ VE SORUMLULUKLAR — TARIK

### G1. Sahibi olduğun işler (EKİP KARARI)

| Görev kodu | Sorumluluk | Somut çıktı | Bağımsız kontrol |
|---|---|---|---|
| K7 | PSO algoritması ve yöntem açıklaması | PSO/PFSP kodu, birim testleri, kaynak notları | Burak (yöntem) + Şeref (model) |
| K8 | Tam deney, istatistik ve karşılaştırma | 15 zorunlu sonuç CSV'si; tablolar; test raporu | Şeref (sayısal) + Muhammed (kapsam) |
| M4 | Makalenin Deneysel Çalışmalar bölümü | Sayısal tablolar, analizler ve görseller | Şeref + Muhammed |
| S4 | Sunumda sonuçların anlatımı | İstatistik yorumları ve grafikler | Şeref + Bilal |

Ayrıca bağımsız test incelemecisi olarak kendine iletilen kod/model PR'larının doğruluğunu sınarsın. Bu, başkasının yönteminin veya veri setinin sahibi olman anlamına gelmez.

### G2. Yetki ve sınırların

- **Yetkin:** FE/seed/30 koşu eksikse P0 veya P1 ret yaz; `--check` PASS olsa da bağımsız doğrulama iste; sonuçlar yeniden üretilemiyorsa deney kabulünü durdur; istatistik varsayımına itiraz et.
- **Sınırın:** hiçbir CSV veya p-değerini manuel 'iyileştirme'; diğer algoritma denklemlerini kendi başına değiştirme; istatistiksel anlamlılığı tek başına yayın kabulü/üstünlük kanıtı diye yorumlama; kendi PSO testini kendi kendine onaylama.
- **İletişim:** matematiksel model ve BKS/permütasyon için Şeref; algoritma arayüzü/teknik review için Burak; teslim kapsamı, çıktı dondurma ve karar için Muhammed; grafik ve makale sunum biçimi için Bilal.

### G3. `--check` dışındaki gerçek kabul kontrolleri

Ders şablonunda `main.py --check` **tek PSO ve sphere problemiyle başarılı dönebilir**. Bu yüzden kontrol aracını şunlarla tamamla:

1. `problem.py`'nin gerçekten PFSP modelini kullandığını ve `ta001`,`ta011`,`ta021` üçlüsünün yüklendiğini **bağımsız model testiyle** doğrula.
2. Algoritma kayıt listesinin **tam beş** algoritmadan oluştuğunu kontrol et. Dosya varlığı değil, import+çalışma sonuçları gerekli.
3. Her algoritma için doğru dönme alanları ve yeniden hesaplanan `best_f`, sınır ve permütasyon uygunluğu; seed deterministikliği, azalan best-so-far, FE sınırlaması.
4. Üç örneğin her biri için her algoritmanın **en az 30 gerçek bağımsız koşu** sonucu olmalı: **15 CSV × 30 satır = 450 koşu** (CSV şema değişirse eşdeğer kanıt). Seed ve metadata eksiksiz.
5. FE bütçesi: 20000/30000/40000, aşım yok; toplam zorunlu değerlendirme **13.500.000**. Eksik gerçekleşen FE varsa açık gerekçe ve ortak stop politikasını raporla.
6. CSV'lerde mükerrer kayıt, NaN/Inf, uyuşmayan `best_x/best_f`, hatalı instance name, farklı parametre veya eksik donanım/zaman kaydı olamaz.
7. `--only-analysis` eksik dosyaları es geçebileceği için sonuç varlığı kontrolünü ayrıca yap; sırf grafik oluştu diye tam deney tamamlandı deme.

### G4. PSO geliştirme öz kontrolün

- [ ] Dersin `pso.py` örneğinin niteliğini/kaynağını koruyarak PFSP'ye gerçek uyarlama yapıldı.
- [ ] PSO orijinal yayın ve kullanılan varyantın hız/konum güncellemesi doğru açıklandı.
- [ ] `seed`, başlangıç popülasyonu, FE ve `maxFEs` doğru.
- [ ] Tüm `best_x`/`best_f` tekrar değerlendirilebilir, algoritma `problem.py` dışında kendi Cmax hesabını kullanmıyor.
- [ ] Aynı seed sonucu tekrar ediyor; model birim testleri ve entegrasyon testleri geçti.
- [ ] Kendi testlerin Burak ve Şeref tarafından bağımsız kontrol edilecek şekilde teslim edildi.

### G5. İstatistik ve hesaplama dürüstlüğü

- Dersin `stat_tests.py` modülünü incele, **Wilcoxon sıra toplamı + Holm**, **Friedman + Nemenyi** raporlamasını doğrula. Kütüphane fonksiyonu adı ve grup tasarımı gerçek teste uygun olmalı.
- Wilcoxon **sıra toplamı** bağımsız örnekler içindir; aynı seed'in farklı algoritmalara verilmesi otomatik eşleştirilmiş deney demek değildir. 'Signed-rank' ile karıştırma.
- Friedman için uygun **blok birimi** tanımla. Yalnızca 3 zorunlu problemde 30 seed'i '30 bağımsız problem' gibi kullanma; kaynak şablon bunu yapıyorsa yöntemsel uyarı ve danışman değerlendirmesi yaz. Makalede testin varsayımı ve kapsamı ifade edilir.
- İstatistikler ham veriden üretilir. `p<0.05` yoksa farklı sonuç varmış gibi yorumlama. Çoklu karşılaştırmada Holm düzeltmesi atlanmaz; dağılım farkı pratik önem kadar etki büyüklüğüyle de değerlendirilebilir (ek analiz).
- Ortalamaları/periyotları raporlarken aynı makinedeki süre karşılaştırması ve FE normalize edilmiş yakınsama kullan; ön testler ile nihai test sonuçlarını karıştırma.

### G6. Her deney için saklanacak minimum metadata

`instance`, `algorithm`, `run_id`, `seed`, `max_fes`, `n_fes`, `best_f`, `best_x` (veya yeniden çözülür biçim), `duration_sec`, `parameter_config`, `code_sha`, `python_version`, `machine_cpu` ve yakınsama eğrisi referansı. Parametre ayarlaması yapılmışsa bağımsız tuning bütçesi ve kararı ayrı tutulur.

### G7. Öz kontrol / teslim ve inceleme protokolün

1. PSO kodunu kod incelemesi için Burak ve Şeref'e gönder; onay olmadan 'tamamlandı' deme.
2. Tüm koşular öncesi dondurulmuş commit üzerinde model ve algoritma kısa testlerini PASS et; deneyi aynı sürümle başlat.
3. Tüm ham sonuçları sağlam ve sürümlü sakla; deney bitmeden sonuçları seçerek raporlamaya başlama.
4. En az iki rastgele kayıt için `best_x→Cmax` yeniden hesaplama, CSV toplamlarının doğrulanması, tablo↔grafik eşleşmesi ve bağımsız istatistik yeniden hesaplama yap.
5. Şeref'e sayısal/matematiksel çapraz kontrol, Muhammed'e eksiksiz deney/kapsam kontrolü için kanıtlı dosya ver. P0/P1 varsa gönderim yerine sorunu raporla.

### G8. Kendi yapay zekâ oturumuna çalışma talimatın

Bana yardım ederken **kanıt ve deney adaleti** önceliklidir. Dosya ve gerçek test olmadan PASS yazma. İstenen çıktıda test ortamı, komut, seed, FE, beklenen/gerçekleşen, sonuç CSV ve hata önceliklendirmesi açık olsun. `main.py --check` tek başına yeterli değil. Yayın sonuçlarının istatistiksel kapsamını olduğundan geniş göstermeme konusunda uyar.

