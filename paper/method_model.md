# 3.1–3.2. PFSP problem modeli, çözüm gösterimi ve doğrulama

**Durum:** Makaleye aktarılabilir final yöntem metni · 23.11.2026  
**Uygulama:** `src/problem.py`

## 3.1. Problemin Tanımı ve Matematiksel Modeli

Permütasyon Akış Tipi Çizelgeleme Probleminde (PFSP) `n` iş, aynı `m` makineyi `M1,...,Mm` sırasıyla ziyaret eder. Her makine aynı anda yalnız bir işi işler, bir iş aynı anda yalnız bir makinede bulunur, işlemler bölünmez ve bütün makinelerde ortak iş sırası kullanılır. Karar değişkeni işlerin permütasyonudur:

[
\pi=(\pi_1,...,\pi_n).
]

`p_{j,k}`, j işinin k makinesindeki işlem süresini göstersin. Sınır değerleri `C_{0,k}=0` ve `C_{i,0}=0` olmak üzere tamamlanma zamanları

[
C_{i,k}=\max\{C_{i-1,k},C_{i,k-1}\}+p_{\pi_i,k}
]

ile hesaplanır. Amaç, son işin son makinedeki tamamlanma zamanını, yani makespan değerini en aza indirmektir:

[
\min_\pi C_{max}(\pi)=C_{n,m}.
]

Bu amaç toplam tamamlanma süresi `ΣC_j` değildir.

### Benchmarklar

Zorunlu Taillard örnekleri aşağıdadır.

| Örnek | Boyut | Tohum | Proje referans Cmax | maxFEs |
|---|---:|---:|---:|---:|
| ta001 | 20×5 | 873654221 | 1278 | 20.000 |
| ta011 | 20×10 | 587595453 | 1582 | 30.000 |
| ta021 | 20×20 | 479340445 | 2297 | 40.000 |

İşlem süreleri `data/taillard/*.txt` içinde job-major biçimde tutulur. Dosya SHA-256 değerleri metadata ile bağlanmıştır. Referans değerler çalışma boyunca “referans/BKS” olarak adlandırılır; ayrıca optimum olduğu kanıtlanmadıkça “global optimum” denmez.

## 3.2. Çözüm Gösterimi ve Kısıt Yönetimi

Beş meta-sezgisel algoritmanın tamamında ortak random-key gösterimi kullanılır:

[
x=(x_1,...,x_n),\qquad x_i\in[0,1].
]

Sürekli vektör, artan anahtar sırasıyla iş permütasyonuna dönüştürülür:

[
\pi=\operatorname{argsort}(x).
]

Uygulama eşit anahtarlarda deterministik davranmak için `np.argsort(..., kind="stable")` kullanır. Böylece bütün algoritmalar aynı temsil ve çözümleme mekanizmasına sahiptir.

Random-key çözümleyicisi her işi tam bir kez içeren permütasyon ürettiğinden normal optimizasyon akışında ek ceza kısıtı gerekmez. Bununla birlikte modelin `objective()` metodu doğrudan verilen permütasyonlarda uzunluk, indeks aralığı, tamsayı olma ve tekrarsızlık kontrollerini yapar. `evaluate()` ve `details()`, anahtarları çözümlemeden önce `[0,1]` sınırına kırpar. Doğrudan `decode()` çağrısı sonlu anahtarları verilen değerleriyle sıralar.

### Performans ölçütü

Referansa göre bağıl yüzde sapma

[
RPD=100\times\frac{C_{max}-C_{ref}}{C_{ref}}
]

olarak hesaplanır. `C_ref`, ilgili örneğin proje metadata'sındaki referans değeridir.

## Model doğrulaması

Model birden çok bağımsız kapıyla doğrulanmıştır:

1. Ders belgesindeki 5×3 örnekte `J4,J2,J1,J5,J3` sırası bağımsız zaman çizelgesi hesabıyla `Cmax=20` üretir.
2. ta001, ta011 ve ta021 ham veri dosyaları beklenen SHA-256 değerleriyle doğrulanır.
3. Metadata içindeki referans permütasyonlar bağımsız DP hesabında sırasıyla 1278, 1582 ve 2297 üretir.
4. Random-key encode/decode geçişi referans permütasyonu kayıpsız geri üretir.
5. Eksik, tekrarlı, aralık dışı ve tamsayı olmayan permütasyonlar reddedilir.
6. İş-makine öncelik ve çakışma koşulları bağımsız schedule verifier ile tekrar kontrol edilir.
7. Linux ve Windows CI üzerinde aynı benchmark hashleri ve model kontrolleri çalıştırılır.

Küçük örneğin doğrulanmış zaman tablosu `paper/support/small_example_schedule.md` dosyasındadır. Final deneyden seçilecek en iyi çözümler `tools/verify_final_schedule.py` ile üretim modelinden bağımsız biçimde tekrar hesaplanacaktır.

## Kaynaklar

- E. Taillard, “Benchmarks for basic scheduling problems,” *European Journal of Operational Research*, 64(2), 278–285, 1993. DOI: `10.1016/0377-2217(93)90182-M`.
- J. C. Bean, “Genetic algorithms and random keys for sequencing and optimization,” *ORSA Journal on Computing*, 6(2), 154–160, 1994. DOI: `10.1287/ijoc.6.2.154`.
