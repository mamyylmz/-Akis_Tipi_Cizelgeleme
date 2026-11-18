> Güncel ortak standart: [PFSP Ortak Proje ve Makale Çalışma Kılavuzu](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md). Yetki sırası: resmî ders belgeleri → ilgili dergi kuralları → ortak kılavuz → kişisel yönerge → sprint kararı. Eski durum notları tarihsel kayıttır; güncel Bilal teslim durumu sprintler/07_Bilal_Literatur_Teslim_Kaniti.md dosyasındadır.

# AKIŞ TİPİ ÇİZELGELEME — BILAL / KİŞİSEL PROJE YÖNERGESİ

**Sürüm:** 1.0 · 15 Kasım 2026  
**Hedef okur:** Bilal ve onunla çalışacak yapay zekâ asistanı  
**Kapsam:** Ortak bilimsel/resmî kurallar + yalnızca Bilal için ayrıntılı görev, yetki ve kabul standardı  
**Kullanım:** Bu dosyanın tamamını tek başına yeni bir sohbet/agent context'ine ekleyin; ek bir ortak yönerge olmadan temel bağlamı içerir.

> **Kullanıcıya not:** Bu dosya **Bilal** için hazırlanmıştır. Temel işin akademik kaynakların doğruluğu, bilimsel yazımın tutarlılığı, hedef derginin biçim kuralları ve Gantt/sunum görselleridir. Sayısal sonuç uydurmak veya başkasının kodunu onaylamak senin görevin değildir.

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

## G. SANA ÖZEL YETKİ VE SORUMLULUKLAR — BİLAL

### G1. Sahibi olduğun işler (EKİP KARARI)

| Görev kodu | Sorumluluğun | Nihai çıktı | Bağımsız kontrol |
|---|---|---|---|
| M1 | Literatür taraması ve literatür matrisi | Birincil hakemli kaynaklar, DOI ve karşılaştırma tablosu | Muhammed ve Şeref |
| M2 | Makale Giriş bölümü | Problem bağlamı, boşluk, amaç ve katkı iddiaları | Muhammed ve Şeref |
| M7 | Kaynakça ve dergi şablonu | Tutarlı kaynakça, gerçek atıf, güncel şablon ve kontrol listesi | Muhammed ve Şeref |
| K9 | İş çizelgesi/Gantt görselleştirme | Kod/grafik, en iyi permütasyonun zamansal Gantt diyagramı | Tarık ve Şeref |
| S1 | Sunum slayt tasarımı | Okunabilir, kaynağı belirtilmiş sunum taslağı | Muhammed ve Tarık |

Diğer bölümlerin kaynak ve biçim denetiminde yardımcı olabilirsin. Bu denetim başkasının metnini kendi adına yazma veya katkı puanı sahiplenme anlamına gelmez.

### G2. Yetkilerin ve sınırların

- **Yetkin:** DOI/atıf doğrulanamıyorsa P1 ret ver; kaynak yanlış yorumlanmışsa sayfa ve alıntı temeliyle düzeltme iste; güncel dergi şablonu ve yazar/ORCID kurallarını kontrol et; şeklin lisansını sor; Gantt grafiğinin görsel kalitesini gözden geçir.
- **Sınırın:** sayısal deney sonuçlarını kendin uydurma; kod denetimini gerçek teknik inceleme olmadan onaylama; modelin doğru olduğunu yalnızca şemadan çıkarma; dergiye tek başına gönderim yapma; diğer ekip üyelerinin görevlerini yeniden dağıtma.
- **İletişim:** araştırma sorusu, makale kapsamı ve dergi seçimi için Muhammed; model açıklamalarının teknik kesinliği için Şeref; CSV ve grafiklerin sayısal doğruluğu için Tarık; algoritmaların özgün denklemi konusunda gerektiğinde Burak.

### G3. Literatür taraması metodolojisi

1. Arama soruları oluştur: `("permutation flow shop" OR "PFSP") AND (makespan OR Cmax) AND (metaheuristic OR "random key" OR "local search")`; ayrıca klasik NEH, Taillard ve algoritma özgün yayınları.
2. Google Scholar, Scopus/Web of Science (erişim varsa), ScienceDirect, IEEE Xplore, Springer, DergiPark/TR Dizin üzerinden hakemli yayınları ayıkla. Blog, sadece GitHub kodu veya başlığından ibaret kayıtlar özgün hakemli algoritma yayını yerine geçmez.
3. Temel ve güncel kaynakları birlikte kullan: Taillard (1993), NEH (1983), Bean (1994, random keys) ve 2022+ güncel meta-sezgisel yayınlar.
4. Her makale için `yazar/yıl/başlık/dergi/DOI`, `amaç (Cmax mi başka metrik mi)`, `test verisi`, `algoritma`, `maxFEs/iterasyon`, `koşu sayısı`, `en iyi/ortalama`, `istatistiksel test`, `kaynakta gerçekten raporlandı mı?`, `araştırma boşluğu` alanlarını doldur.
5. Erişilmeyen bilgiler için `RAPORLANMAMIŞ` veya `ERİŞİLEMEDİ` kullan; başkasının sonuç tablosunu tahmin etme veya birim dönüştürmeden alıntılama.
6. Literatür sentezini 'X bunu yaptı, Y bunu yaptı' listesi değil, yöntem aileleri ve metodolojik boşluklar üzerinden kur; olmayan boşluğu varmış gibi yazma.
7. Kaynakça yönetiminde Zotero gibi araçtan yararlan; bibliyografik bilgiler ve DOI birincil sayfadan tekrar doğrulansın.

### G4. Makale için yazım ve içerik sözleşmen

- **Giriş:** problemin endüstriyel karşılığı → NP-zorluk ve sıralama yapısı → meta-sezgisel aileler → literatürde gerçek karşılaştırma sorunu → bu çalışmanın amacı → katkılar. `Cmax` yerine `ΣCj` yazma.
- **Literatür:** özgün atıf ve matris; yöntem karşılaştırmalarında FE/koşu/istatistik uyumluluğunu belirt; çok farklı bütçeli çalışmaların sonuçlarını doğrudan üstünlük kanıtı olarak kullanma.
- **Kaynakça:** metinde atıf yapılan her kaynağın kaynakçada bulunduğunu, yazar/yıl/DOI/doğruluk ve hedef dergi biçimini kontrol et.
- **Özet:** 150–250 kelimelik Türkçe özet ve uyumlu İngilizce Abstract taslağını lider hazırlayacak; sen dil ve kaynak/terim tutarlılığı incelemesi yaparsın. Deneyler gerçekleşmeden sayısal sonuç yazılmaz.
- **Etik:** benzerlik/özgünlük, görsel kaynağı ve kullanım izni, yapay zekâ kullanım beyanı, gerçek yazar katkıları, ORCID/doğru kurum alanları; danışman onayı olmadan gönderim yok.
- **Dergi:** hedef derginin güncel amaç/kapsam, yazım şablonu, dil, telif, etik, ücret ve süre açıklamalarını resmî siteden kontrol ederek teslim et. DergiPark hesabı açılması yayına kabul anlamına gelmez.

### G5. PFSP Gantt görselleştirme doğrulaması

1. Grafik gerçekten `problem.py` tarafından kullanılan işlem süreleri ve **en iyi çözüm permütasyonu** ile üretilmeli.
2. Her makinede işlemler çakışmaz; her iş her makinede tam bir kez vardır; işler aynı makine sırasıyla ve aynı permütasyonla ilerler.
3. Her çubuk başlangıç/bitiş süreleri `C[i,j]` özyinelemesiyle uyumlu olmalı; son bitiş = `Cmax`.
4. Grafiğin üstünde `instance`, algoritma, seed/çözüm kimliği, `Cmax`, zaman birimi ve açıklayıcı lejant bulunmalı.
5. Renkleri ayırt edemeyen okuyucu için okunabilir etiketler/çizgiler kullan; makale için yeterli çözünürlük; görsel/veri kaynakları belirtilir.
6. Tarık ham sonuçla, Şeref matematiksel çizelgeyle doğrulamadan grafiği 'kesin' diye teslim etme.

### G6. Öz kontrol — göndermeden önce

- [ ] Her kritik olgunun birincil kaynak DOI veya gerçek deney sonucu var.
- [ ] Kaynakça ile metin içi atıflar birebir eşleşiyor.
- [ ] En az üç güncel algoritmanın özgün yayın tarihleri ve hakemli niteliği doğrulandı.
- [ ] Karşılaştırma metninde farklı FE bütçeleri aynı kabul edilmiyor.
- [ ] 'Global optimum' ifadesi, BKS kanıtlanmamışsa kullanılmıyor.
- [ ] Amaç `Cmax`; olmayan deney sonucu/p-değeri/performans artışı iddiası yok.
- [ ] Gantt Cmax/iş-makine sıralaması teknik kaynakla uyumlu.
- [ ] Şablon, makale uzunluğu, özet/anahtar kelime, yazar/ORCID, etik alanları kontrol edildi.
- [ ] Görsellerin kaynak/izin durumu açık.
- [ ] Kaynak referansları ve kontrol edilen sürüm/tarih belgeli.
- [ ] Açık P0/P1 yok; taslaksa açıkça `TASLAK/DOĞRULANMADI` etiketi var.

### G7. İnceleme ve teslim biçimin

Her akademik teslimde `kaynak matrisi linki`, `kapsanan arama dönemi/veritabanları`, `incelemeye alınan çalışma sayısı`, `DOI doğrulama kaydı`, `bulduğun gerçek araştırma boşlukları`, `teslim dosyasının sürümü`, `öz kontrol sonucu` ve `istenen bağımsız inceleme` bilgilerini yaz. Makale/yazım çıktılarını önce Muhammed'in editöryal ve Şeref'in teknik incelemesine gönder; gerçek PASS gelince tamamlandı etiketi kullan. Gantt için Tarık ve Şeref onayı gerekir.

### G8. Kendi yapay zekâ oturumuna çalışma talimatın

Bana literatür veya makale hazırlarken doğrulanmamış atıf üretme; makale başlığını, DOI'yi, yayın yılını ve sonuçları mümkünse resmî yayıncı sayfasından doğrula. Araştırma boşluğu iddiasını 'henüz bulunamadı' ile 'literatürde yok' arasında ayrıştır. Gantt için gerçek iş süreleri ve permütasyon gelmeden sahte grafik üretme. Nihai metin dışında **kaynak doğrulama tablosu ve doğrulanmamış kalan ifadeler listesini** ayrıca ver.

