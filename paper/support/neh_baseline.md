# NEH klasik baseline

**Tarih:** 23.11.2026  
**Uygulama:** `src/heuristics/neh.py`  
**Kaynak:** Nawaz, Enscore Jr. ve Ham (1983), DOI `10.1016/0305-0483(83)90088-9`.

NEH, beş meta-sezgisel algoritmadan ayrı, deterministik klasik referanstır. Her benchmark için yalnız bir kez uygulanır; 30 bağımsız koşuya dahil edilmez.

## Yöntem

1. Her işin bütün makinelerdeki toplam işlem süresi hesaplanır.
2. İşler toplam işlem süresi azalan sırada önceliklendirilir.
3. Sıradaki iş mevcut kısmi çizelgenin tüm olası konumlarına ayrı ayrı eklenir.
4. En küçük kısmi Cmax değerini veren konum tutulur.
5. Bütün işler eklenene kadar devam edilir.

Deterministik proje tie-break'i:
- eşit toplam işlem süresinde düşük iş indeksi önce işlenir;
- eşit insertion Cmax değerinde en erken insertion konumu seçilir.

## Zorunlu Taillard sonuçları

| Örnek | Referans Cmax | NEH Cmax | RPD (%) | NEH permütasyonu (1-based) |
|---|---:|---:|---:|---|
| ta001 | 1278 | **1286** | **0.625978** | 3 17 9 8 15 14 11 16 13 19 6 4 5 18 1 2 10 7 20 12 |
| ta011 | 1582 | **1680** | **6.194690** | 18 5 2 17 3 6 12 9 15 10 20 13 8 14 19 11 4 7 1 16 |
| ta021 | 2297 | **2410** | **4.919460** | 16 15 10 8 9 12 13 11 5 1 20 14 17 2 18 6 7 19 3 4 |

Bu Cmax değerleri bağımsız PFSP recurrence ile yeniden hesaplandı. Runtime donanıma bağlı olduğundan kalıcı sayısal sonuç olarak elle yazılmayacak; `python tools/run_neh_baseline.py` her çalıştırmada Cmax/RPD/permutation ile birlikte gerçek runtime'ı üretir. CI çıktısı ayrıca kabul kanıtıdır.

## Küçük örnek

Dersin 5×3 doğrulama örneğinde verilen `J4,J2,J1,J5,J3` sırası Cmax=20'dir. NEH aynı işlem sürelerinde deterministik olarak Cmax=19 veren başka bir sıra bulur. Bu, ders örneğinin “optimum çözüm” olduğu iddiası değildir; ders sırası yalnız model doğrulama örneğidir.
