> Bu belge, ekipteki herkesin proje boyunca kullanacağı ortak çalışma standardıdır. Makale Yazım Kılavuzu ve Taslağı biçimi esas alınmış; Problem 7’ye özgü matematiksel model, veri ve algoritma şartları, Git/GitHub çalışma düzeni, kaynak doğrulama, test ve deney kabul kriterleri, makale iskeleti ve teslim kontrol şablonları aynı belgede birleştirilmiştir. Kişisel yönergeler bu ortak kılavuzu tamamlar; bu belgedeki ortak kuralları azaltamaz veya geçersiz kılamaz.
>
> Kullanım: Mavi rehber kutuları ekip için açıklama ve kabul ölçütleridir. Makale taslağı bölümündeki \[köşeli parantezli\] alanlar gerçek içerikle değiştirilir. Bilinmeyen veya henüz doğrulanmamış bir veri asla tahmin edilerek doldurulmaz; “doğrulama bekliyor” olarak işaretlenir. Test veya kontrol sonuçları başarısızsa kriter değiştirilmez; hata düzeltilir ve aynı kontrol yeniden çalıştırılır.

# BÖLÜM I: ORTAK PROJE KILAVUZU

## 1. Belgenin Yetki Hiyerarşisi ve Kullanım Kuralı

Projede farklı belgeler, kişisel yapay zekâ contextleri ve sprint görevleri kullanılacağı için çelişki halinde hangi bilginin esas alınacağı aşağıdaki sırayla belirlenir:

> 1\. Ders sorumlusunun resmî problem belgesi, proje paketi, başlangıç rehberi ve makale yazım kılavuzu.
>
> 2\. Seçilen derginin güncel yazım ve gönderim kuralları. Yalnızca makale biçimi ve gönderim koşullarında resmî ders kılavuzuyla birlikte değerlendirilir; dersin zorunlu deney kurallarını değiştirmez.
>
> 3\. Bu PFSP Ortak Proje ve Makale Çalışma Kılavuzu.
>
> 4\. Kişiye özel ekip yönergesi.
>
> 5\. Güncel sprint/görev dosyası ve proje yöneticisinin yazılı kararları.
>
> Bir kişisel context veya yapay zekâ çıktısı bu hiyerarşide daha üstteki bir kuralla çelişiyorsa üstteki kural uygulanır. Çelişki sessizce çözülmez; görev sahibine ve proje yöneticisine açıkça bildirilir.

## 2. Proje Kimliği, Amaç ve Başarı Tanımı

| **Alan**             | **Ortak karar / zorunlu kapsam**                                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| Problem              | Permutation Flow Shop Scheduling Problem (PFSP) – işlerin tüm makinelerde aynı sırayı izlediği permütasyon akış tipi çizelgeleme. |
| Amaç                 | Makespan minimizasyonu: son işin son makinedeki tamamlanma zamanı Cmax en küçük yapılacaktır.                                     |
| Çözüm gösterimi      | Sürekli meta-sezgiseller için random-key vektörü; sıralama numpy.argsort mantığıyla permütasyona dönüştürülür.                    |
| Zorunlu testler      | Taillard ta001 (20×5), ta011 (20×10), ta021 (20×20).                                                                              |
| Zorunlu algoritmalar | DE, PSO, DBO, RIME, NRBO – toplam tam olarak beş meta-sezgisel.                                                                   |
| Referans sezgisel    | NEH ayrıca kodlanır; beş meta-sezgisel algoritmadan biri sayılmaz.                                                                |
| Deney                | Her algoritma × her zorunlu örnek için en az 30 bağımsız koşu; aynı test örneğinde eşit maxFEs.                                   |
| İstatistik           | Wilcoxon sıra toplamı + Holm; genel karşılaştırma için Friedman ve Nemenyi.                                                       |
| Kod tabanı           | Python; ders paketindeki proje şablonu ve Akis_Tipi_Cizelgeleme deposu.                                                           |
| İlk ekip teslimi     | 18 Kasım 2026 Çarşamba, 19.00.                                                                                                    |
| Makale hedef tarihi  | 3 Aralık 2026 – grubun nihai makale sürümü. DergiPark gönderim tarihi ayrıca ders sorumlusu/danışman talimatıyla teyit edilir.    |

> Terminoloji uyarısı: Dosya adında veya bazı metinlerde “toplam tamamlanma süresi” ifadesi görülebilir; bu projede matematiksel amaç Cmax (makespan) minimizasyonudur. ΣCj / total flow time farklı bir amaç fonksiyonudur ve makalede birbirine karıştırılmayacaktır.

## 3. Ekip Yapısı ve Ortak Sorumluluk Arayüzleri

Kişisel görevlerin ayrıntısı ayrı yönergelerde tutulur. Ortak kılavuzda herkesin bilmesi gereken yalnızca bileşen sahipliği, beklenen çıktı ve bağımsız inceleme ilişkileridir.

| **Bileşen / çıktı**                                        | **Birincil sorumlu** | **Bağımsız kontrol / ilişki**                              |
|------------------------------------------------------------|----------------------|------------------------------------------------------------|
| Proje yönetimi, entegrasyon, RIME, nihai kabul             | Muhammed             | RIME: Burak + Tarık; akademik bütünlük: Bilal.             |
| DBO, NRBO, teknik kod standardı                            | Burak                | Matematiksel uygunluk: Şeref; yürütme ve test: Tarık.      |
| Taillard verileri, problem.py, model doğrulama, DE         | Şeref                | Model ve sayısal doğrulama: Tarık; DE kod inceleme: Burak. |
| PSO, test/deney altyapısı, istatistik                      | Tarık                | PSO teknik inceleme: Burak; model uyumu: Şeref.            |
| Literatür matrisi, kaynak denetimi, makale belge altyapısı | Bilal                | Akademik bütünlük: Muhammed; teknik ifadeler: Şeref.       |

> Hiç kimse kendi ürettiği çıktının tek başına nihai onay mercii değildir. “Çalışıyor”, “doğru”, “kaynak gerçek” veya “test geçti” beyanı, bağımsız kanıt olmadan kabul edilmez.

## 4. Ortak İş Akışı: Üretim → Öz Kontrol → Bağımsız Kontrol → Kabul

| **Aşama**           | **Ne yapılır?**                                                    | **Sonraki aşamaya geçiş şartı**                         |
|---------------------|--------------------------------------------------------------------|---------------------------------------------------------|
| A. Üretim           | Görev sahibi kodu, belgeyi, veri setini veya analizi üretir.       | Dosya/commit/rapor somut olarak mevcut olmalı.          |
| B. Öz kontrol       | Görev sahibi kendi kriter listesini en az bir kez uygular.         | PASS/FAIL ve kanıt kaydedilmeli.                        |
| C. Bağımsız kontrol | Belirlenen başka üye kaynağı/testi/kodu bağımsız doğrular.         | P0/P1 açık hata kalmamalı.                              |
| D. Düzeltme         | Hata varsa beklenen/gerçekleşen/düzeltme/kabul şartı yazılır.      | Aynı kriter yeniden uygulanmalı; kriter gevşetilmemeli. |
| E. Kabul            | Proje yöneticisi veya atanmış kabul sahibi kanıtlara göre kapatır. | Çıktı sonraki görevin doğrulanmış girdisi olabilir.     |

## 5. Hata Öncelikleri ve Düzeltme Talebi Standardı

| **Seviye**       | **Tanım**                                                | **Örnek**                                                                                 | **Kural**                                           |
|------------------|----------------------------------------------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------------|
| P0 – Engelleyici | Sonucun güvenilirliğini veya çalıştırılabilirliği bozar. | Yanlış Cmax, sahte veri/kaynak, algoritmanın çalışmaması, testin gerçeği ölçmemesi.       | Kapatılmadan ilgili akış ilerleyemez.               |
| P1 – Önemli      | Teslim veya bilimsel doğruluk kriterini karşılamaz.      | Eksik DOI doğrulaması, yanlış FE hesabı, eksik kabul kanıtı, resmî şablona uymayan bölüm. | Tam kabul verilmez; düzeltilip yeniden test edilir. |
| P2 – Küçük       | Temel sonucu bozmaz ama kaliteyi düşürür.                | Biçim, tekrar, küçük isimlendirme veya açıklama kusuru.                                   | Nihai teslimden önce kapatılır.                     |

> Düzeltme kaydı en az şu dört alanı içermelidir: Beklenen sonuç; gerçekleşen sonuç; düzeltilmesi gereken nokta; yeniden kabul şartı. Bir hata düzeltildikten sonra eski PASS kanıtı geçerli sayılmaz; yeni sürüm yeniden kontrol edilir.

## 6. Git/GitHub ve Dosya Yönetimi Standardı

Ortak depo adı: Akis_Tipi_Cizelgeleme. Her görev mümkün olduğunca ayrı branch/PR ile yürütülür. Doğrudan main üzerinde kontrolsüz değişiklik yapılmaz.

> • Çalışmaya başlamadan önce son sürüm alınır; yalnızca ilgili görev dosyaları değiştirilir.
>
> • Commit mesajı yapılan işi açıklar: “DBO: exploration aşaması eklendi” gibi. “son”, “düzeltme”, “yeni” gibi belirsiz mesajlardan kaçınılır.
>
> • Kod, veri ve deney sonucunun hangi commit ile üretildiği mümkün olduğunca kaydedilir.
>
> • Şifre, API anahtarı, kişisel gizli bilgi ve gereksiz büyük dosyalar depoya eklenmez.
>
> • results/ altındaki ham deney sonuçları sonradan elle düzenlenmez. Düzeltme gerekiyorsa deney yeniden çalıştırılır veya yeni sürüm dosyası üretilir.
>
> • Makale için kullanılan tablo/şekiller mümkün olduğunca results/ içindeki ham veriden betikle tekrar üretilebilir olmalıdır.

## 7. Akademik Kaynak ve “Yalancı Veri” Önleme Protokolü

Literatürdeki veya ekip tarafından üretilen hiçbir sayı, kaynak veya sonuç doğrulanmadan makaleye gerçek veri olarak giremez.

| **Kontrol**              | **Zorunlu doğrulama**                                                                                                                          |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Kaynak kimliği           | Başlık, yazarlar, yıl, yayın yeri ve DOI özgün yayıncı/DOI kaydı veya güvenilir bibliyografik kaynaktan eşleştirilir.                          |
| Özgün algoritma kaynağı  | Blog, ikincil makale veya GitHub deposu özgün yayın yerine kullanılamaz.                                                                       |
| Sayısal literatür sonucu | Tablodan alınan sayı için test örneği, amaç fonksiyonu, FE/iterasyon bütçesi ve koşu sayısı bağlamı kaydedilir.                                |
| Veri seti                | Taillard örnekleri güvenilir kaynaktan alınır; boyutlar ve bilinen değerler çapraz kontrol edilir.                                             |
| Ekip deney sonucu        | Ham sonuç dosyası, seed, algoritma, problem örneği, FE bütçesi ve kod sürümüyle izlenebilir olmalıdır.                                         |
| Şüpheli kaynak           | Matematiksel/istatistiksel tutarsızlık varsa kaynak tamamen “yanlış” ilan edilmez; tutarsızlık not edilir ve sayısal kanıt olarak kullanılmaz. |

> Yapay zekâ tarafından önerilen DOI, makale, yazar, BKS, deney sonucu veya dergi bilgisi kaynak doğrulaması yapılmadan kullanılamaz. “Kaynak gerçek görünüyor” doğrulama değildir.

## 8. Ortak Zaman Planı ve Kilometre Taşları

| **Tarih**             | **Hedef**                                | **Kabul ölçütü**                                                                                                                |
|-----------------------|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| 18 Kasım 2026 – 19.00 | İlk ekip sprint teslimi                  | Her görev için mevcut çıktı, öz kontrol, bağımsız kontrol durumu ve açık P0/P1 listesi.                                         |
| 19–23 Kasım           | Model ve beş algoritmanın üretim sürümü  | problem.py doğrulanmış; beş algoritma ortak arayüzde çalışıyor; main.py --check tek başına yeterli kanıt sayılmıyor.            |
| 24–27 Kasım           | Tam deneylerin yürütülmesi               | 3 zorunlu örnek × 5 algoritma × ≥30 koşu; seed ve ham sonuçlar saklanmış.                                                       |
| 28–30 Kasım           | İstatistik, tablolar, şekiller, tartışma | Özet istatistikler + Wilcoxon/Holm + Friedman/Nemenyi + yakınsama/kutu grafiklerinin üretimi.                                   |
| 1 Aralık              | Tam makale iç inceleme                   | Bütün ana bölümler mevcut; sonuç iddiaları tablolara ve testlere bağlı.                                                         |
| 2 Aralık              | Düzeltme ve yeniden doğrulama            | Açık P0/P1 yok; kaynakça/şekil/tablo/kod tutarlılığı kontrol edilmiş.                                                           |
| 3 Aralık              | Nihai makale                             | Grubun teslim edilebilir makale sürümü. DergiPark gönderim takvimi danışman/ders sorumlusu talimatına göre ayrıca teyit edilir. |

# BÖLÜM II: TEKNİK UYGULAMA VE KALİTE KAPILARI

## 9. Matematiksel Model ve Problem Doğrulama Standardı

Bir permütasyon π için tamamlanma zamanları makine ve iş öncüllerine göre özyinelemeli hesaplanır. Amaç, son işin son makinedeki tamamlanma zamanını Cmax olarak en küçüklemektir.

> Temel bağıntı: C(i,j) = max(C(i−1,j), C(i,j−1)) + p(π_i,j). Sınır durumlarında ilk iş ve ilk makine için uygun başlangıç değerleri kullanılır. Random-key çözümü, anahtarların sıralanmasıyla geçerli bir iş permütasyonuna dönüştürülür.

Tablo. Zorunlu doğrulama testleri

| **Test**                    | **Beklenen**                                                    | **Kabul koşulu**                                                     |
|-----------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------|
| 5 iş × 3 makine örneği      | (J4, J2, J1, J5, J3) sırası için Cmax = 20.                     | Aynı veri ve sıra bağımsız hesapla da 20 vermeli.                    |
| ta001 referansı             | Bilinen referans permütasyonu değerlendirildiğinde Cmax = 1278. | Referans permütasyon kaynağı ve kullanılan veri sürümü kaydedilmeli. |
| Decode                      | Her random-key vektörü eksiksiz, tekrarsız permütasyon üretir.  | 0..n−1 işlerinin her biri tam bir kez bulunmalı.                     |
| Deterministik değerlendirme | Aynı permütasyon aynı Cmax değerini verir.                      | Tekrar değerlendirmelerde değişmemeli.                               |
| Veri boyutları              | ta001 20×5; ta011 20×10; ta021 20×20.                           | Dosya yükleyici boyutu ve işlem sürelerini doğru okumalı.            |

## 10. Test Örnekleri, maxFEs ve RPD

| **Örnek**                 | **Boyut**     | **Bilinen en iyi değer (ders belgesindeki yaklaşık/referans)** | **maxFEs** | **Durum**    |
|---------------------------|---------------|----------------------------------------------------------------|------------|--------------|
| ta001                     | 20×5          | 1278                                                           | 20 000     | Zorunlu      |
| ta011                     | 20×10         | 1582                                                           | 30 000     | Zorunlu      |
| ta021                     | 20×20         | 2297                                                           | 40 000     | Zorunlu      |
| ta031                     | 50×5          | ≈2724                                                          | 50 000     | İsteğe bağlı |
| ta041                     | 50×10         | Güncel kaynakta doğrulanacak                                   | 60 000     | İsteğe bağlı |
| ta051 veya 100 işli örnek | 50×20 / 100×m | Güncel kaynakta doğrulanacak                                   | 100 000    | Ek çalışma   |

> RPD hesaplarında kullanılan BKS/UB değerinin kaynağı ve erişim tarihi makalede belirtilir. Bilinen değerler zamanla güncellenebileceği için yalnızca eski bir tabloda görülmesi yeterli değildir.

## 11. Algoritma Gerçekleme Standardı

| **Algoritma** | **Tür** | **Sorumlu bileşen** | **Ortak zorunluluk**                                                                  |
|---------------|---------|---------------------|---------------------------------------------------------------------------------------|
| DE            | Klasik  | Şeref               | Sıfırdan gerçekleme; random-key uzayında sınır yönetimi; FE ve seed uyumu.            |
| PSO           | Klasik  | Tarık               | Sıfırdan/şablondaki örneğin kaynağı açık olacak şekilde gerçekleme; FE ve seed uyumu. |
| DBO           | Güncel  | Burak               | Özgün yayındaki arama mekanizmasına sadık gerçekleme.                                 |
| RIME          | Güncel  | Muhammed            | Özgün yayındaki exploration/exploitation mekanizmasına sadık gerçekleme.              |
| NRBO          | Güncel  | Burak               | Özgün yayındaki Newton–Raphson tabanlı güncelleme mantığına sadık gerçekleme.         |

> • Hazır meta-sezgisel paketler nihai deney sonuçlarını üretmek için kullanılmaz; yalnızca doğrulama amacıyla karşılaştırılabilir.
>
> • Her algoritmanın rastgele sayıları np.random.default_rng(seed) üzerinden yönetilir.
>
> • Aynı seed ve aynı girdi altında tekrarlanabilirlik test edilir.
>
> • Durdurma ölçütü iterasyon sayısı değil, test örneğine ait maxFEs sınırıdır.
>
> • Özgün yayında olmayan yerel arama/repair/hybrid mekanizması ana karşılaştırmaya gizlice eklenmez. Böyle bir geliştirme ayrı deney olarak raporlanır.
>
> • Her algoritma sorumlusu makaledeki kendi Metot alt başlığını da hazırlar ve kullanılan denklemleri kendi gösterimiyle açıklar.

## 12. Deney Protokolü

| **Kural**             | **Uygulama**                                                                                                            |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------|
| Bağımsız koşu         | Her algoritma × her zorunlu test örneği için en az 30.                                                                  |
| Seed                  | Her koşunun seed değeri kaydedilir; ortak seed listesi kullanılması tercih edilir.                                      |
| FE adaleti            | Aynı örnekte tüm algoritmalar aynı maxFEs ile durur.                                                                    |
| Parametreler          | Özgün yayındaki önerilen değerler kullanılır; ayar yapılırsa tüm algoritmalara eşit ayar bütçesi tanınır ve raporlanır. |
| Ham sonuç             | Koşu bazında en iyi Cmax, RPD, süre, seed ve gerektiğinde yakınsama geçmişi saklanır.                                   |
| Raporlanan istatistik | En iyi, en kötü, ortalama, medyan, standart sapma, uygun çözüm oranı, ortalama süre.                                    |
| İstatistiksel test    | Wilcoxon sıra toplamı (α=0,05, Holm düzeltmeli); genel sıralama Friedman + Nemenyi.                                     |
| Grafikler             | Yakınsama, box plot, CD diyagramı ve PFSP için Gantt/çizelge görselleştirmesi.                                          |

> Minimum zorunlu çalışma sayısı: 5 algoritma × 3 test örneği × 30 koşu = 450 algoritma koşusu. FE değerlendirmelerinin toplam sayısı ta001 için 3 000 000, ta011 için 4 500 000, ta021 için 6 000 000; üçü birlikte 13 500 000 amaç fonksiyonu değerlendirmesidir.

## 13. Test ve Denetim Katmanları

| **Katman**  | **Örnek testler**                                                                                            | **Başarısızlık halinde**                  |
|-------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| Veri        | Dosya varlığı, boyut, satır/sütun, işlem süresi aralığı, checksum/sürüm kaydı.                               | Deney başlamaz.                           |
| Model       | 5×3 Cmax=20, ta001 referansı, decode permütasyon, deterministik evaluation.                                  | Tüm algoritma sonuçları geçersiz sayılır. |
| Algoritma   | Sınırlar, FE sayacı, seed tekrarlanabilirliği, NaN/inf, population shape, best-so-far monotonluğu (uygunsa). | İlgili algoritma tam deneye alınmaz.      |
| Entegrasyon | main.py --check + ayrıca beş algoritmanın gerçekten kayıtlı/çalışır olduğu bağımsız kontrol.                 | Check tek başına PASS sayılmaz.           |
| Deney       | 30 koşunun eksiksizliği, seed çakışmaları, FE eşitliği, ham dosya sayısı.                                    | Eksik koşular yeniden üretilir.           |
| İstatistik  | Girdilerin doğru algoritma/örneğe ait olması, p-değerleri ve Holm sıralaması, Friedman giriş matrisi.        | Tablo/yorum yayımlanmaz.                  |
| Makale      | Tablodaki sayı = ham sonuçlardan üretilen sayı; kaynakça = metin atıfları; iddia = kanıt.                    | Bölüm P1/P0 olarak iade edilir.           |

## 14. Sonuçların Görselleştirilmesi: PFSP İçin Özel Kurallar

> • Yakınsama eğrileri aynı FE ekseninde karşılaştırılmalıdır; yalnızca iterasyon ekseni adil karşılaştırma sağlamaz.
>
> • Box plotlar 30 koşu sonu Cmax veya RPD dağılımını göstermelidir; kullanılan ölçüt başlıkta açık yazılır.
>
> • En iyi permütasyon Gantt diyagramında makineler yatay eksen/satırlar, işler renk/etiket olarak gösterilebilir. İşlem başlangıç ve bitiş zamanları modelden yeniden hesaplanmalıdır.
>
> • Gantt çizimi gerçek model verisinden üretilir; örnek/sentetik işlem süreleri nihai sonuç gibi sunulmaz.
>
> • Şekiller mümkünse betikle ve ham CSV/JSON sonuçlarından yeniden üretilebilir olmalıdır.

# BÖLÜM III: PFSP MAKALE TASLAĞI

> Bu bölüm, ortak makale çalışma alanıdır. Köşeli parantez içindeki yer tutucular gerçek bilgiyle değiştirilir. Bir sonuç henüz üretilmediyse sayı tahmin edilmez. Makale tamamen bittikten sonra seçilen derginin resmî Word şablonuna aktarılır; biçim çelişkisinde derginin güncel şablonu esas alınır.

## Başlık

\[Türkçe başlık: PFSP + meta-sezgisel karşılaştırma + çalışmanın gerçek katkısı\]

\[English title\]

> Başlık 10–20 kelime civarında, açıklayıcı ve sonuçlar belli olduktan sonra son hâline getirilecek. Sonuç elde edilmeden “X en iyi algoritmadır” gibi bulgu iddiası başlığa yazılmayacaktır.

## Yazar Künyeleri

Abdullah ELEN¹,\*; Muhammed YILMAZ¹; \[diğer yazarlar katkı puanı ve danışman onayına göre\]

¹ \[Yazılım Mühendisliği Bölümü, ilgili fakülte, Bandırma Onyedi Eylül Üniversitesi, Balıkesir, Türkiye\]

\* Sorumlu yazar: \[danışmanın dergi hesabında kullandığı e-posta\]

> Yazar sırası ders kılavuzuna göre: 1. danışman, 2. takım lideri; 3. sıradan sonrası gerçek katkı puanına göre azalan sıralama ve danışman nihai onayı. Beş kişilik grupta 100/5 = 20 yalnızca eşit katkı referansıdır; herkesin otomatik katkı puanı değildir. Her yazarın ORCID’i gönderim öncesinde doğrulanmalıdır.

## Özet

\[150–250 kelimelik tek paragraf: bağlam → boşluk/amaç → beş algoritma ve Taillard örnekleri → eşit FE/30 koşu/istatistik → sayısal ana bulgu → sonuç.\]

Anahtar Kelimeler: permutation flow shop scheduling, makespan, meta-sezgisel optimizasyon, \[güncel algoritma\], istatistiksel karşılaştırma

## Abstract

\[Türkçe özetin akademik İngilizce karşılığı; yeni bilgi eklenmez.\]

Keywords: permutation flow shop scheduling, makespan, metaheuristic optimization, \[recent algorithm\], statistical comparison

## 1. Giriş

> Önerilen 6 paragraf: (1) üretim çizelgeleme bağlamı ve PFSP önemi; (2) PFSP’nin kombinatoryal/NP-zor yapısı ve Cmax; (3) klasik sezgiseller ve meta-sezgiseller; (4) güncel çalışmaların sentezi; (5) doğrulanmış araştırma boşluğu; (6) çalışmanın amacı, katkıları ve makale düzeni. Her güçlü literatür iddiası kaynağa dayanır. Sonuçlar burada uydurulmaz veya önden ilan edilmez.

\[Giriş metni\]

## 2. Literatür Taraması

\[PFSP, makespan, Taillard benchmarks, NEH, random-key, klasik meta-sezgiseller ve 2022+ güncel algoritmalar üzerine sentez.\]

Tablo 1. İlgili çalışmaların literatür matrisi

| **Kaynak** | **Yöntem** | **Test örneği**   | **FE / koşu** | **En iyi / ortalama** | **İstatistik** | **Not / boşluk**              |
|------------|------------|-------------------|---------------|-----------------------|----------------|-------------------------------|
| \[1\]      | \[yöntem\] | \[Taillard/VFR…\] | \[değer\]     | \[değer\]             | \[var/yok\]    | \[bizim çalışmayla ilişkisi\] |
| \[…\]      | \[…\]      | \[…\]             | \[…\]         | \[…\]                 | \[…\]          | \[…\]                         |

> Literatür tablosunda başka çalışmaların sayıları karşılaştırılırken amaç fonksiyonunun aynı olduğundan emin olun. Cmax ile total flow time, farklı Taillard örneği, farklı FE bütçesi veya farklı koşu sayısı doğrudan eşdeğer değildir.

## 3. Materyal ve Metot

### 3.1. Problemin Tanımı ve Matematiksel Modeli

\[PFSP tanımı; n iş, m makine, p_ij işlem süreleri; ortak iş sırası π; tamamlanma zamanı özyinelemesi; amaç min Cmax.\]

> Bu bölüm Şeref’in doğrulanmış problem.py modeliyle birebir tutarlı olmalıdır. Modelde olmayan bir kısıt veya algoritmada kullanılan ama makalede açıklanmayan bir dönüşüm bulunmamalıdır.

### 3.2. Çözüm Gösterimi ve Kısıt Yönetimi

\[Random-key x∈\[0,1\]^n → argsort(x) → permütasyon π. PFSP yapısı nedeniyle geçerli permütasyon üretildiği ve özel ceza fonksiyonu gerekmemesi açıklanır. Sınır yönetimi algoritma seviyesinde ortak kuralla açıklanır.\]

### 3.3. Karşılaştırılan Meta-Sezgisel Algoritmalar

### 3.3.1. Diferansiyel Evrim (DE)

\[Özgün kaynak; başlatma; exploration/exploitation; temel güncelleme denklemleri; parametreler; bu projedeki sınır ve random-key kullanımı. Algoritma sorumlusu yazar.\]

### 3.3.2. Parçacık Sürü Optimizasyonu (PSO)

\[Özgün kaynak; başlatma; exploration/exploitation; temel güncelleme denklemleri; parametreler; bu projedeki sınır ve random-key kullanımı. Algoritma sorumlusu yazar.\]

### 3.3.3. Dung Beetle Optimizer (DBO)

\[Özgün kaynak; başlatma; exploration/exploitation; temel güncelleme denklemleri; parametreler; bu projedeki sınır ve random-key kullanımı. Algoritma sorumlusu yazar.\]

### 3.3.4. RIME

\[Özgün kaynak; başlatma; exploration/exploitation; temel güncelleme denklemleri; parametreler; bu projedeki sınır ve random-key kullanımı. Algoritma sorumlusu yazar.\]

### 3.3.5. Newton-Raphson-Based Optimizer (NRBO)

\[Özgün kaynak; başlatma; exploration/exploitation; temel güncelleme denklemleri; parametreler; bu projedeki sınır ve random-key kullanımı. Algoritma sorumlusu yazar.\]

### 3.4. Deney Düzeneği ve Performans Ölçütleri

\[Taillard ta001, ta011, ta021; maxFEs; 30 bağımsız koşu; seed politikası; popülasyon ve parametreler; donanım/yazılım ortamı; Cmax, RPD, süre ve özet istatistikler.\]

Tablo 2. Deney ve algoritma parametreleri

| **Algoritma** | **Popülasyon** | **Parametreler** | **Kaynak / gerekçe** |
|---------------|----------------|------------------|----------------------|
| DE            | \[N\]          | \[F, CR…\]       | \[özgün kaynak\]     |
| PSO           | \[N\]          | \[w, c1, c2…\]   | \[özgün kaynak\]     |
| DBO           | \[N\]          | \[…\]            | \[özgün kaynak\]     |
| RIME          | \[N\]          | \[…\]            | \[özgün kaynak\]     |
| NRBO          | \[N\]          | \[…\]            | \[özgün kaynak\]     |

### 3.5. İstatistiksel Analiz

\[Wilcoxon sıra toplamı, α=0,05 ve Holm düzeltmesi; genel karşılaştırma için Friedman ve Nemenyi. Testlerin hangi veri matrisi üzerinde ve hangi hipotezle uygulandığı açıklanır.\]

## 4. Deneysel Çalışmalar

### 4.1. Deney Ortamı ve Parametre Ayarları

\[Python/kütüphane sürümleri, CPU/RAM, parametre tablosu, maxFEs, 30 koşu.\]

### 4.2. Doğrulama

\[5×3 örnek ve ta001 referans doğrulamasının kanıtı. Kodun doğru Cmax hesapladığı gösterilir.\]

### 4.3. Sayısal Sonuçlar

\[Her zorunlu örnek için en iyi, en kötü, ortalama, medyan, std, RPD, süre tablosu.\]

### 4.4. Yakınsama Analizi

\[Aynı FE ekseninde medyan/ortalama yakınsama eğrileri; erken/geç arama davranışı.\]

### 4.5. Kararlılık Analizi

\[30 koşu dağılımlarının box plotları ve yorum.\]

### 4.6. İstatistiksel Karşılaştırma

\[Wilcoxon/Holm ve Friedman/Nemenyi sonuçları. Anlamlı fark ile yalnızca sayısal fark birbirinden ayrılır.\]

### 4.7. En İyi Çözüm ve Gantt Gösterimi

\[En iyi permütasyon, Cmax ve PFSP Gantt diyagramı; işlem zamanları modelden yeniden hesaplanır.\]

### 4.8. Hesaplama Maliyeti

\[Ortalama süreler; FE eşitliğine rağmen algoritmik maliyet farklarının yorumu.\]

> Deneysel bölümde hiçbir sayı elle tahmin edilmez. Tablodaki değerlerin ham results/ dosyasından yeniden üretilebilir olması gerekir. Bir kaynak veya koşu şüpheliyse sonuç “doğrulama bekliyor” olarak işaretlenir, makalede kesin bulguya dönüştürülmez.

## 5. Sonuç ve Tartışma

\[Ana bulgu → nedenleri → literatürle adil karşılaştırma → kısıtlılıklar → uygulama önerisi ve gelecek çalışmalar.\]

> Algoritmanın bir testte en düşük değeri bulması “genel olarak daha iyi” demek değildir. Genelleme için tüm örnekler, 30 koşuluk dağılımlar ve istatistiksel testler birlikte yorumlanmalıdır. Random-key düz bölgeleri veya problem-özel yerel arama gibi neden-sonuç iddiaları yalnızca deney tasarımı bunu destekliyorsa yazılır.

## Beyanlar

Yazar Katkı Beyanı: \[Gerçek görev ve katkı kayıtlarına göre CRediT veya derginin istediği format.\]

Çıkar Çatışması Beyanı: \[Derginin istediği ifade.\]

Etik Kurul Onayı: \[İnsan/hayvan deneyi bulunmadığı için derginin istediği standart ifade; dergi kuralı kontrol edilir.\]

Veri ve Kod Erişilebilirliği: \[Depo erişim durumu ve sonuçların paylaşım politikası.\]

Yapay Zekâ Kullanım Beyanı: \[Kullanılan araçlar ve amaçları; bilimsel sonuçların sorumluluğu yazarlardadır.\]

Teşekkür: \[Varsa.\]

## Kaynaklar

\[Seçilen derginin istediği atıf stiline göre. DOI varsa eklenir; metin içi atıf ile kaynakça birebir eşleşir.\]

> Okunmamış bir kaynak başka makalenin kaynakçasından kopyalanarak kullanılmaz. Bilal’in literatür matrisi başlangıç kaynağıdır; makalede kullanılacak her kritik kaynak için kimlik ve ilgili iddia ayrıca doğrulanır.

## Ekler

Ek A: \[Beş algoritmanın sözde kodları veya ayrıntılı parametreleri\]

Ek B: \[Ek test örnekleri ve sonuç tabloları\]

Ek C: \[En iyi permütasyonlar / karar değişkenleri / tekrar üretme komutları\]

# BÖLÜM IV: TESLİM, DENETİM VE GÖNDERİM

## 15. Görev Teslim Kanıtı Şablonu

> Her önemli görev tesliminde aşağıdaki alanlar doldurulur. Bu kayıt Markdown, GitHub Issue/PR veya ortak raporda tutulabilir.

| **Alan**              | **Doldurulacak bilgi**                      |
|-----------------------|---------------------------------------------|
| Görev / kod           | \[örn. K2 problem.py doğrulama\]            |
| Sorumlu               | \[ad\]                                      |
| Sürüm / commit        | \[commit hash veya dosya sürümü\]           |
| Üretilen çıktılar     | \[dosya yolları / linkler\]                 |
| Öz kontrol            | \[PASS/FAIL + çalıştırılan kontroller\]     |
| Bilinen açık sorunlar | \[P0/P1/P2 listesi veya “yok”\]             |
| Bağımsız incelemeci   | \[ad\]                                      |
| İnceleme sonucu       | \[PASS/FAIL + kanıt\]                       |
| Düzeltme varsa        | \[ne değişti ve hangi kontrol tekrarlandı\] |
| Nihai durum           | \[KABUL / DÜZELTME GEREKİYOR / BLOKE\]      |

## 16. Düzeltme Talebi Şablonu

Hata ID: \[PFSP-K2-001\] Öncelik: \[P0/P1/P2\] Görev: \[kod/başlık\]

Beklenen: \[ne olması gerekiyordu?\]

Gerçekleşen: \[ne bulundu?\]

Kanıt: \[test çıktısı / satır / kaynak / ekran görüntüsü değilse tercih edilen metin/log\]

Düzeltilmesi gereken: \[somut değişiklik\]

Yeniden kabul şartı: \[hangi aynı test/kontrol tekrar geçmeli?\]

## 17. Makale İç İnceleme Kontrol Listesi

☐ Başlık ve amaç gerçekten yapılan çalışmayı yansıtıyor; sonuç bilinmeden yazılmış abartılı iddia yok.

☐ Cmax ile toplam akış/tamamlanma süresi kavramları karıştırılmamış.

☐ Taillard örnek adları, boyutları, BKS/UB değerleri ve maxFEs doğru ve kaynaklı.

☐ Beş algoritmanın özgün kaynakları doğrulanmış; en az üçü 2022+ şartını karşılıyor.

☐ Her algoritmanın Metot alt bölümü gerçek koda ve kullanılan parametrelere uyuyor.

☐ 30 koşu, seed ve FE protokolü makale ile results/ arasında tutarlı.

☐ Tablolardaki en iyi/ortalama/medyan/std değerleri ham sonuçtan yeniden üretilebiliyor.

☐ İstatistiksel test sonuçları doğru veri matrisi üzerinde uygulanmış ve doğru yorumlanmış.

☐ Literatür karşılaştırmasında farklı FE/koşu/amaç fonksiyonu koşulları açıkça belirtilmiş.

☐ Her şekil ve tablo metinde atıf alıyor; başlıklar açıklayıcı ve numaralar sıralı.

☐ Metin içi atıflar ile kaynakça birebir eşleşiyor; uydurma DOI veya erişilemeyen kaynak yok.

☐ Yapay zekâ kullanımı, katkı, çıkar çatışması ve veri/kod beyanları dergi gereğine göre tamamlanmış.

☐ Açık P0 veya P1 bulunmuyor.

## 18. Hedef Dergi Seçim Prosedürü

Ders kılavuzunda aday olarak verilen DergiPark dergilerinden biri danışmanla birlikte seçilir. Seçim yapılırken amaç-kapsam, yayın dili, makale türü, şablon, etik ve gönderim dosyaları güncel DergiPark sayfasından tekrar kontrol edilir.

| **No** | **Ders kılavuzundaki aday**          |
|--------|--------------------------------------|
| 1      | dergipark.org.tr/tr/pub/yalvac       |
| 2      | dergipark.org.tr/tr/pub/kujs         |
| 3      | dergipark.org.tr/tr/pub/kastamonujes |
| 4      | dergipark.org.tr/tr/pub/nase         |
| 5      | dergipark.org.tr/en/pub/cumfad       |
| 6      | dergipark.org.tr/tr/pub/cujast       |
| 7      | dergipark.org.tr/tr/pub/tjse         |
| 8      | dergipark.org.tr/tr/pub/tmaed        |
| 9      | dergipark.org.tr/tr/pub/ijedt        |
| 10     | dergipark.org.tr/tr/pub/gbad         |
| 11     | dergipark.org.tr/tr/pub/adufmbd      |

> Bu liste ders kılavuzundan gelir. Güncel kapsam ve gönderim şartları zamanla değişebileceği için nihai seçim tarihinde resmî dergi sayfası tekrar kontrol edilir. Kılavuz dışı bir dergiye yönelmek istenirse ders sorumlusunun açık onayı alınmadan nihai hedef olarak kabul edilmez.

## 19. Gönderim Öncesi Son Kontrol Listesi

☐ Seçilen derginin güncel Word şablonu ve yazım kuralları kullanıldı.

☐ Bu kılavuzdaki bütün rehber metinleri ve \[yer tutucular\] nihai makaleden kaldırıldı.

☐ Tüm yazarların ad, kurum, ORCID ve yazar sırası doğrulandı; nihai sıra danışman tarafından onaylandı.

☐ Makale içinde raporlanan bütün sayılar nihai results/ sürümüyle eşleşiyor.

☐ Kod ve veri doğrulama testleri son commit üzerinde tekrar çalıştırıldı.

☐ Açık P0/P1 bulunmuyor; P2’ler kapatıldı veya açıkça kabul edildi.

☐ Kaynakça ve DOI kontrolü son kez yapıldı.

☐ Şekil ve tablolar okunabilir; Gantt gerçek işlem sürelerinden üretildi.

☐ Yapay zekâ kullanım beyanı gerçek kullanım biçimini yansıtıyor.

☐ Danışman incelemesi tamamlandı.

☐ DergiPark gönderim tarihi ve istenen ek belgeler danışman/ders sorumlusu ile teyit edildi.

☐ Gönderim yapıldıysa onay ekranı/e-postası saklandı.

## 20. Ekip İçin Kısa “Yapma” Listesi

> • Eksik sonucu tamamlanmış gibi göstermeyin.
>
> • Kaynağı açmadan veya DOI’yi doğrulamadan literatür iddiası yazmayın.
>
> • Bir test geçmediğinde testi kaldırmayın, beklentiyi düşürmeyin veya sonucu elle değiştirmeyin.
>
> • Ham deney CSV/JSON dosyalarını daha iyi görünmesi için elle düzenlemeyin.
>
> • main.py --check başarılı diye bütün projenin doğru olduğunu varsaymayın.
>
> • İstatistiksel anlamlılık yoksa “daha iyi” ifadesini mutlak üstünlük gibi kullanmayın.
>
> • Özgün makalede olmayan bir operatörü ana algoritmaya gizlice eklemeyin.
>
> • Yapay zekâ tarafından üretilen kodu anlamadan teslim etmeyin; herkes kendi sorumlu olduğu kodu açıklayabilmelidir.
>
> • Başka grubun kodunu veya makalesini kullanmayın.
>
> • Son gün ilk kez birleştirme yapmayın; makale ve kod sürekli entegre edilmelidir.

## 21. Ortak Kılavuz Revizyon Kaydı

| **Sürüm** | **Tarih**  | **Değişiklik**                                                                            | **Onay**         |
|-----------|------------|-------------------------------------------------------------------------------------------|------------------|
| v1.0      | 18.11.2026 | Problem 7 için ortak proje, teknik kalite, makale taslağı ve teslim protokolü ilk sürümü. | Proje yöneticisi |
| \[v1.x\]  | \[tarih\]  | \[değişiklik özeti\]                                                                      | \[onaylayan\]    |

> Bu belge yaşayan bir kılavuzdur; ancak kriter değişikliği geçmiş başarısız bir testi “geçmiş” göstermek için geriye dönük yapılamaz. Resmî ders veya dergi şartı değişirse revizyon kaydıyla güncellenir.
