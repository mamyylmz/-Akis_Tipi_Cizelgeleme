# Taillard PFSP verileri — kaynak, biçim ve bütünlük

Bu klasör YMM4142 Problem 7 için zorunlu Taillard örneklerini içerir: `ta001`, `ta011`, `ta021`.

## Kaynak ve üretim

- Özgün benchmark: E. Taillard, *Benchmarks for basic scheduling problems*, European Journal of Operational Research 64(2), 278–285, 1993. DOI: `10.1016/0377-2217(93)90182-M`.
- OR-Library üretim kodu/tohumları: <https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/flowshop2.txt>
- Güncel sınırlar ve yayımlanmış referans permütasyonlar: <https://mistic.iict-heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/flowshop.dir/best_lb_up.txt>
- Erişim tarihi: **18.11.2026**. Sınır sayfasındaki güncelleme: **03.06.2026**.

Veri elle uydurulmamış veya başka bir çalışmadan kopyalanmamıştır. `tools/generate_taillard_instances.py`, OR-Library'deki Park–Miller üretecini ve resmî tohumları uygular. Üreteç önce makine-major matrisi oluşturur, proje dosyalarını ise **iş-satır / makine-sütun** (`p[job, machine]`) biçiminde yazar. `ta001` üretimi ayrıca OR-Library `flowshop2.txt` içindeki yayımlanmış 5×20 doğrulama matrisiyle birebir karşılaştırılır.

## Dosya biçimi

Her `taXXX.txt` dosyasında:

1. İlk satır: `<iş_sayısı> <makine_sayısı>`
2. Sonraki `n` satır: bir işin M1…Mm işlem süreleri
3. İş ve makine indeksleri kod içinde 0-tabanlıdır; makalede J1…Jn / M1…Mm gösterimi kullanılır.
4. İşlem süreleri 1–99 arası tamsayıdır.

## Zorunlu örnekler

| Örnek | Tohum | Boyut | Referans Cmax | maxFEs | SHA-256 |
|---|---:|---:|---:|---:|---|
| ta001 | 873654221 | 20×5 | 1278 | 20 000 | `68164a1350ad2252e224b3fc36872ec65556f04cb6cd6914abaa455910867bf2` |
| ta011 | 587595453 | 20×10 | 1582 | 30 000 | `e291f3f94885af40c9b9509cd9e939d66d4455d3611db55b42b3bfb801cf6656` |
| ta021 | 479340445 | 20×20 | 2297 | 40 000 | `2fbd5446f94ebb5bfcf81fc0fcc4f5624294bfc4532c7f46354e76e832810f59` |

`reference_solutions.json`, kaynak sayfasında yayımlanmış 1-tabanlı referans permütasyonları ve kodda kullanılan 0-tabanlı karşılıklarını içerir. Bu değerler `problem.py` tarafından yeniden hesaplanır; yalnızca Cmax sayısını sabit döndürmek kabul edilmez.

## Yeniden üretim ve doğrulama

```bash
python tools/generate_taillard_instances.py
python -m unittest discover -s tests -v
python src/problem.py
```

İlk komut aynı dosyaları deterministik olarak yeniden üretmelidir. İkinci komut veri, decode ve makespan için bağımsız testleri; üçüncü komut yayımlanmış referans permütasyonları üzerinden ta001/ta011/ta021 Cmax doğrulamasını yürütür.
