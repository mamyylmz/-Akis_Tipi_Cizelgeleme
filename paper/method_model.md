# Materyal ve Metot — PFSP problem modeli ve doğrulama

**Durum:** Şeref/K1–K2–M3 teknik çıktısı · 18.11.2026  
**Amaç:** Bu metin, makalenin `3.1 Problemin Tanımı ve Matematiksel Modeli`, `3.2 Kısıt Yönetimi ve Çözüm Gösterimi` ve doğrulama kısmına girdi sağlar. Deney sonucu değildir.

## 1. Problemin tanımı

Permütasyon Akış Tipi Çizelgeleme Probleminde (PFSP) `n` iş aynı `m` makineyi M1,…,Mm sırasıyla ziyaret eder. Her makine aynı anda tek bir işi işleyebilir, bir iş aynı anda yalnızca bir makinede bulunabilir, işlem kesintiye uğramaz ve bütün makinelerde **ortak iş sırası** kullanılır. Karar değişkeni işlerin permütasyonu `π=(π1,…,πn)`'dir.

Bu çalışmanın amacı **makespan** değerini, yani ortak sıradaki son işin son makinede tamamlandığı zamanı en aza indirmektir:

\[
\min_{\pi} C_{\max}(\pi)=C_{n,m}.
\]

Burada `p_{j,k}`, `j` işinin `k` makinesindeki işlem süresidir. Tamamlanma zamanları sınır değerleri `C_{0,k}=0` ve `C_{i,0}=0` olmak üzere

\[
C_{i,k}=\max\{C_{i-1,k},\;C_{i,k-1}\}+p_{\pi_i,k}
\]

bağıntısıyla hesaplanır. Bu amaç **toplam tamamlanma süresi / toplam akış süresi** `ΣC_j` değildir; kod, deney ve makalede `Cmax` ile `ΣC_j` birbirinin yerine kullanılmaz.

## 2. Çözüm gösterimi ve kısıtlar

Seçilen meta-sezgisellerin çoğu sürekli uzayda çalıştığı için ortak gösterim **random-key** yöntemidir. Bir aday çözüm

\[
x=(x_1,\ldots,x_n),\qquad 0\le x_i\le1
\]

olarak tutulur ve `π = argsort(x)` ile permütasyona dönüştürülür. Uygulamada eşit anahtarların deterministik ele alınması için NumPy `argsort(..., kind="stable")` kullanılır. Aynı decode işlemi bütün algoritmalara uygulanarak gösterim kaynaklı farklılık engellenir.

Random-key sıralaması her iş indeksini tam bir kez içerdiğinden bu modelde ek ceza kısıtı yoktur; `constraints()` boş dizi döndürür. Yine de `objective()` fonksiyonu doğrudan çağrıldığında eksik, tekrarlı veya aralık dışı permütasyonları reddeder. Böylece bozuk bir test/entegrasyon girdisinin sessizce geçmesi önlenir.

## 3. Veri ve benchmarklar

Taillard örnekleri, OR-Library'de yayımlanan özgün üretim algoritması ve tohumlar kullanılarak yeniden üretilmiştir. İşlem süreleri 1–99 aralığında tamsayıdır. Projedeki veri dosyaları `p[job,machine]` yönünde, yani her satır bir iş olacak şekilde saklanır.

| Örnek | Boyut | Tohum | Referans Cmax | maxFEs |
|---|---:|---:|---:|---:|
| ta001 | 20×5 | 873654221 | 1278 | 20 000 |
| ta011 | 20×10 | 587595453 | 1582 | 30 000 |
| ta021 | 20×20 | 479340445 | 2297 | 40 000 |

Veri kaynağı: OR-Library `flowshop2.txt`. Güncel referans değer ve permütasyon kaynağı: Taillard PFSP `best_lb_up.txt` (sayfada güncelleme 03.06.2026; erişim 18.11.2026). Dosya SHA-256 değerleri `data/README.md` içinde kayıtlıdır.

## 4. Performans ölçütü

Farklı örneklerdeki sonuçların ortak ölçekte raporlanması için bağıl yüzde sapma (RPD) kullanılır:

\[
RPD=100\times\frac{C_{\max}-C_{ref}}{C_{ref}}.
\]

`C_ref`, bu proje için kayıt altına alınmış referans/BKS değeridir. Bir değer kaynakta açıkça optimum olarak kanıtlanmadıkça yalnızca "referans" veya "BKS" olarak adlandırılır.

## 5. Model doğrulama protokolü

Model doğruluğu tek bir testle kabul edilmez:

1. Ders belgesindeki 5 iş × 3 makine örneğinde `(J4,J2,J1,J5,J3)` sırası bağımsız 2-B DP hesabıyla `Cmax=20` vermelidir.
2. Üretilen ta001 matrisi, OR-Library'deki yayımlanmış ta001 doğrulama matrisiyle birebir eşleşmelidir.
3. Ta001, ta011 ve ta021 için Taillard'ın yayımladığı referans permütasyonlar `problem.py` üzerinden sırasıyla `1278`, `1582` ve `2297` üretmelidir.
4. Aynı permütasyonlar üretim kodundan farklı bir 2-B dinamik programlama uygulamasıyla tekrar hesaplanmalı ve aynı sonuç alınmalıdır.
5. Rastgele en az 25 permütasyonda üretim ve bağımsız hesap yolları aynı Cmax değerini vermelidir.
6. Random-key decode sonucu eksiksiz/tekrarsız permütasyon olmalı; eşit anahtarlarda deterministik sıra korunmalıdır.
7. Veri dosyasının SHA-256 değeri metadata ile uyuşmazsa model yüklenmemelidir.

`python -m unittest discover -s tests -v` ve `python src/problem.py` bu kontrollerin otomatik kısmını yürütür. `python src/main.py --check` yararlı bir duman testidir ancak tek başına bilimsel kabul kanıtı değildir.

## 6. DE hazırlığı

Klasik yöntemlerden Diferansiyel Evrim için Storn ve Price (1997) temel alınmıştır (DOI `10.1023/A:1008202821328`). Projede `DE/rand/1/bin` uygulanır. Kaynak makalenin kontrol değişkenleri için verdiği pratik önerilerden hareketle ilk, ayarlanmamış değerler `NP=5D`, `F=0.5`, `CR=0.9` olarak kodlanmıştır. Bu değerler Taillard testlerine göre optimize edilmiş değildir; sonraki deneylerde değiştirilirse bütün algoritmalara eşit ayarlama bütçesi uygulanmalı ve raporda açıkça belirtilmelidir.

DE kodu ortak API'yi kullanır; bütün amaç değerlendirmeleri FE sayacına dahil edilir, aynı seed aynı sonucu üretir ve yeni adaylar `[0,1]^D` sınırına alınır. DE'nin bu aşamadaki teknik doğrulaması `tests/test_de.py` ile yapılır; nihai deney kabulü Tarık'ın ortak deney/test kapısına tabidir.

## 7. Kaynaklar

- E. Taillard, “Benchmarks for basic scheduling problems,” *European Journal of Operational Research*, 64(2), 278–285, 1993. DOI: `10.1016/0377-2217(93)90182-M`.
- R. Storn and K. Price, “Differential Evolution – A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces,” *Journal of Global Optimization*, 11, 341–359, 1997. DOI: `10.1023/A:1008202821328`.
- J. C. Bean, “Genetic algorithms and random keys for sequencing and optimization,” *ORSA Journal on Computing*, 6(2), 154–160, 1994. DOI: `10.1287/ijoc.6.2.154`.
