# Makale İskeleti

**Sürüm 0.5 · 18.11.2026 · Ortak kılavuza uyumlu, bağımsız belge denetimi PASS**

Kaynak: [PFSP Ortak Proje ve Makale Çalışma Kılavuzu](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md), Bölüm III. Aşağıdaki başlık adları ve sırası bu bölümle birebir eşleşir. Bu belge, resmî DOCX'in ayrıca okunmuş olduğu iddiasını taşımaz. Dergi uyarlaması nihai makale sürümünde yapılacak. Yer tutucular gerçek kanıt geldikçe doldurulacak.

## Başlık

**Türkçe çalışma başlığı:** Permütasyon Akış Tipi Çizelgelemede Beş Meta-Sezgisel Algoritmanın Eşit Değerlendirme Bütçesiyle Makespan Açısından Karşılaştırılması

**English title:** Comparing Five Metaheuristic Algorithms for Permutation Flow Shop Makespan under Equal Evaluation Budgets

Son başlık gerçek bulgulara göre kesinleştirilecek.

## Yazar Künyeleri

Kılavuzdaki sıra: danışman Abdullah ELEN; takım lideri Muhammed YILMAZ; diğer yazarlar gerçek katkı puanına göre ve danışman onayıyla. Bu çalışma listesi nihai yazarlık onayı değildir.

| Sıra / rol | Ad | Kurum / bölüm | E-posta | ORCID |
| --- | --- | --- | --- | --- |
| 1 / danışman | Abdullah ELEN | [teyit] | [teyit] | [teyit] |
| 2 / takım lideri | Muhammed YILMAZ | [teyit] | [teyit] | [teyit] |
| Katkıya göre | Burak [soyadı] | [teyit] | [teyit] | [teyit] |
| Katkıya göre | Şeref [soyadı] | [teyit] | [teyit] | [teyit] |
| Katkıya göre | Tarık [soyadı] | [teyit] | [teyit] | [teyit] |
| Katkıya göre | Bilal [soyadı] | [teyit] | [teyit] | [teyit] |

Kılavuzdaki kurum taslağı: Yazılım Mühendisliği Bölümü, [ilgili fakülte], Bandırma Onyedi Eylül Üniversitesi, Balıkesir, Türkiye. Her yazar için doğrulanacak. Sorumlu yazar danışman; dergi hesabındaki e-posta doğrulanacak. Eşit katkı referansı %20'dir; gerçek katkı puanı değildir.

## Özet

[150–250 kelime, tek paragraf: bağlam, boşluk/amaç, beş algoritma, Taillard, eşit FE, 30 koşu, istatistik, doğrulanmış ana bulgu ve sonuç. Gerçek sonuç bekleniyor.]

**Anahtar Kelimeler:** permütasyon akış tipi çizelgeleme, makespan, meta-sezgisel optimizasyon, [güncel algoritma], istatistiksel karşılaştırma.

## Abstract

[Türkçe özetin akademik İngilizce karşılığı; ek bulgu içermez.]

**Keywords:** permutation flow shop scheduling, makespan, metaheuristic optimization, [recent algorithm], statistical comparison.

## 1. Giriş

[Giriş taslağı](introduction_draft.md). Üretim bağlamı, PFSP/Cmax ve NP-zorluk, klasik ve güncel yöntemler, doğrulanmış boşluk, amaç/katkı ve makale düzeni.

## 2. Literatür Taraması

[Literatür matrisi](literature_matrix.md) ve [araştırma soruları](gap_analysis.md). Tablo 1 bu matristen üretilecek: kaynak, yöntem, test örneği, FE/koşu, en iyi/ortalama, istatistik ve boşluk. Farklı amaç/bütçe/örnek koşulları eşdeğer gösterilmeyecek.

## 3. Materyal ve Metot

Aşağıdaki yöntem açıklamaları uygulama kodu ve özgün kaynaklarla eşleştirilecek. Kod ve tam metin denetimi bekleyen ayrıntılar tamamlanmış kabul edilmez.

### 3.1. Problemin Tanımı ve Matematiksel Modeli

n iş, m makine, işlem süreleri p ve ortak permütasyon π. Amaç min Cmax; toplam akış süresi değildir. `C[i,j] = max(C[i-1,j], C[i,j-1]) + p[pi[i],j]`; sıfır sınır değerleri; Cmax son işin son makinedeki tamamlanması. Şeref'in doğrulanmış modeliyle karşılaştırılacak.

### 3.2. Çözüm Gösterimi ve Kısıt Yönetimi

Random-key x∈[0,1]^n, kararlı argsort ile geçerli permütasyon; eşit anahtarlarda deterministik çözüm. PFSP için ek ceza gerekmemesinin gerekçesi, sınır yönetimi ve aynı sıraya çözülen adayların FE sayımı açıklanacak.

### 3.3. Karşılaştırılan Meta-Sezgisel Algoritmalar

Tam olarak beş meta-sezgisel aşağıdadır. NEH ayrıca klasik referanstır. Her yöntem için başlatma, arama mekanizması, özgün denklemler, parametreler, sınır yönetimi ve random-key uyarlaması açıklanacak. Hazır optimizasyon paketleriyle nihai sonuç üretilmeyecek; ek yerel arama ana yönteme gizlice eklenmeyecek.

### 3.3.1. Diferansiyel Evrim (DE)

[Sorumlu: Şeref; kaynak: L04, literatür matrisi. Özgün denklemler ve uygulama eşleşmesi doğrulandıktan sonra başlatma, keşif/sömürü, güncellemeler, parametreler, sınır ve random-key kullanımı yazılacak.]

### 3.3.2. Parçacık Sürü Optimizasyonu (PSO)

[Sorumlu: Tarık; kaynak: L05, literatür matrisi. Özgün denklemler ve uygulama eşleşmesi doğrulandıktan sonra başlatma, keşif/sömürü, güncellemeler, parametreler, sınır ve random-key kullanımı yazılacak.]

### 3.3.3. Dung Beetle Optimizer (DBO)

[Sorumlu: Burak; kaynak: L06, literatür matrisi. Özgün denklemler ve uygulama eşleşmesi doğrulandıktan sonra başlatma, keşif/sömürü, güncellemeler, parametreler, sınır ve random-key kullanımı yazılacak.]

### 3.3.4. RIME

[Sorumlu: Muhammed; kaynak: L07, literatür matrisi. Özgün denklemler ve uygulama eşleşmesi doğrulandıktan sonra başlatma, keşif/sömürü, güncellemeler, parametreler, sınır ve random-key kullanımı yazılacak.]

### 3.3.5. Newton-Raphson-Based Optimizer (NRBO)

[Sorumlu: Burak; kaynak: L08, literatür matrisi. Özgün denklemler ve uygulama eşleşmesi doğrulandıktan sonra başlatma, keşif/sömürü, güncellemeler, parametreler, sınır ve random-key kullanımı yazılacak.]

### 3.4. Deney Düzeneği ve Performans Ölçütleri

Taillard ta001 (20×5, 20.000 FE), ta011 (20×10, 30.000 FE), ta021 (20×20, 40.000 FE). Veri kaynağı, SHA-256, matris yönü ve sürüm kaydedilecek. Her algoritma/örnek için ≥30 bağımsız koşu; asgari 450 koşu ve tam bütçede 13,5 milyon FE. Tohumlar np.random.default_rng(seed) ile yönetilecek; ortak tohum listesi kaydedilecek.

Cmax, RPD = 100 × (Cmax − referans) / referans, süre, en iyi/en kötü/ortalama/medyan/std ve uygun çözüm oranı raporlanacak. 1278/1582/2297 ders referanslarıdır; güncel BKS/UB kaynağı ve erişim tarihi doğrulanacak, optimum kanıtı sayılmayacak.

Tablo 2. Deney ve algoritma parametreleri

| Algoritma | Popülasyon | Parametreler | Kaynak / gerekçe |
| --- | --- | --- | --- |
| DE | [bekliyor] | F, CR [bekliyor] | L04 |
| PSO | [bekliyor] | Özgün 1995 kuralı veya açıkça kaynaklandırılmış varyant [kodla eşleştirilecek] | L05 + gerekiyorsa varyant kaynağı |
| DBO | [bekliyor] | [bekliyor] | L06 |
| RIME | [bekliyor] | [bekliyor] | L07 |
| NRBO | [bekliyor] | [bekliyor] | L08 |

Özgün öneriler veya tüm yöntemlere eşit ayar bütçesi kaydedilecek. Donanım/yazılım ortamı 4.1'de ayrıntılandırılacak.

Yapay zekâ kullanım kaydı: ChatGPT/Codex belge düzenleme ve kaynak tarama desteğinde kullanıldı. Araç/kapsam ve insan doğrulaması yazarlarca kesinleştirilecek; Beyanlar ile tutarlı tutulacak.

### 3.5. İstatistiksel Analiz

Wilcoxon sıra toplamı, α=0,05 ve Holm düzeltmesi; Friedman ve Nemenyi. Hipotezler, gözlem birimi, girdi matrisi, varsayımlar ve üç benchmarkın çıkarım sınırı açıklanacak. İşaretli sıralar testiyle karıştırılmayacak.

## 4. Deneysel Çalışmalar

Doğrulanmış deney çıktıları henüz mevcut değil. Tablolar/şekiller ham results/ kayıtlarından üretilecek; yer tutucular sayısal sonuç değildir.

### 4.1. Deney Ortamı ve Parametre Ayarları

CPU/RAM, işletim sistemi, Python/kütüphane sürümleri, kod sürümü, Tablo 2, maxFEs ve ≥30 koşu. Parametreler, tohum listesi, yeniden üretim komutları ve ham dosya yolları eklenecek.

### 4.2. Doğrulama

5×3 kaynak matrisi ve (J4,J2,J1,J5,J3) için beklenen Cmax=20; ta001 için kaynaklı referans permütasyonu ile beklenen Cmax=1278. Veriler gelmeden PASS yazılmayacak. Decode, geçersiz permütasyon, seed, FE ve raporlanan best_x/best_f/n_fes bağımsız denetlenecek. main.py --check tek başına kabul değildir; --only-analysis çıktılarının eksiksizliği ayrıca doğrulanacak.

### 4.3. Sayısal Sonuçlar

| Örnek | Yöntem | Koşu | En iyi Cmax | En kötü | Ortalama | Medyan | Std | RPD | Uygun çözüm oranı | Ortalama süre | FE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [veri bekleniyor] | | | | | | | | | | | |

Her zorunlu örnek için beş yöntem ve ayrı NEH referansı; sonuçlar ham koşulardan türetilecek.

### 4.4. Yakınsama Analizi

Ortak FE ekseninde ortalama/medyan yakınsama, yayılım ve erken/geç arama davranışı. İterasyon ekseni eşit FE'nin yerini almaz.

### 4.5. Kararlılık Analizi

Her yöntem/örnek için ≥30 koşu sonu Cmax veya RPD box plotları; dağılım, yayılım ve aykırı değerler. Ölçüt şekil başlığında belirtilecek.

### 4.6. İstatistiksel Karşılaştırma

Wilcoxon/Holm, Friedman/Nemenyi sonuç tabloları ve CD diyagramı. Sayısal fark ile anlamlı fark ayrılacak; gerçek veri olmadan p-değeri yazılmayacak.

### 4.7. En İyi Çözüm ve Gantt Gösterimi

En iyi permütasyon, bağımsız yeniden hesaplanan Cmax, 15 işlemlik küçük örnek zaman tablosu ve doğrulanmış Gantt. Başlangıç/bitiş, öncelik ve çakışma denetimi. [Doğrulanmış küçük örnek zaman çizelgesi](support/small_example_schedule.md).

### 4.8. Hesaplama Maliyeti

Ortalama süreler, yayılım ve eşit FE altında algoritmaların ek hesap maliyetleri; aynı donanım/koşullar üzerinden değerlendirilecek.

## 5. Sonuç ve Tartışma

[Gerçek ana bulgu, kanıtla desteklenen nedenler, NEH/literatürle adil karşılaştırma, üç örneğin sınırlılığı, uygulama ve gelecek çalışmalar. Tek koşu veya tek örnekten genel üstünlük çıkarılmayacak.]

## Beyanlar

- Yazar Katkı Beyanı: [gerçek görev/katkı kaydı, CRediT veya dergi biçimi].
- Çıkar Çatışması Beyanı: [yazarlardan teyit].
- Etik Kurul Onayı: [insan/hayvan deneyi kapsamı ve dergi şartına göre teyit edilen ifade].
- Veri ve Kod Erişilebilirliği: [depo erişimi, sürüm ve sonuç paylaşım politikası].
- Yapay Zekâ Kullanım Beyanı: [ChatGPT/Codex kullanım kapsamı ve insan denetimi; bilimsel sorumluluk yazarlarda].
- Teşekkür ve finansman: [varsa, yazarlardan teyit].

## Kaynaklar

[Dergi stiline göre kaynakça; DOI ve metin içi atıflar karşılıklı denetlenecek. Kritik iddialar özgün kaynakla doğrulanacak.]

## Ekler

Ek A: [beş algoritmanın sözde kodları ve ayrıntılı parametreleri].

Ek B: [ek test örnekleri ve sonuç tabloları].

Ek C: [en iyi permütasyonlar, tohum listesi, FE tanımı, yeniden üretim komutları].
