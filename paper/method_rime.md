# RIME yöntemi ve PFSP uyarlaması

## Kaynak ve doğrulama

Birincil kaynak: Su, H., Zhao, D., Heidari, A. A., Liu, L., Zhang, X., Mafarja, M., & Chen, H. (2023). **RIME: A physics-based optimization.** *Neurocomputing, 532*, 183–214. DOI: 10.1016/j.neucom.2023.02.010.

Uygulama ayrıca yazarların kamuya açık `RIME.m` koduyla çapraz kontrol edilmiştir. Yazar kodunda popülasyon başlangıcı, soft-rime search, hard-rime puncture, boundary absorption ve positive greedy selection sırası esas alınmıştır.

## Projedeki temsil

RIME sürekli arama uzayında çalışır. PFSP çözümü ortak proje sözleşmesine göre `x in [0,1]^n` random-key vektörüdür. `Problem.evaluate(x)` vektörü stable `argsort` ile permütasyona çözer ve Cmax hesaplar. RIME doğrudan permütasyon veya Cmax kodu içermez; yalnız `problem.dim/lb/ub/evaluate` kullanır.

## Mekanizmalar

1. **Başlatma:** N ajan [lb, ub] içinde uniform örneklenir.
2. **Soft-rime search:** Yazar kodundaki RimeFactor ile en iyi çözüm çevresinde yeni aday oluşturulur.
3. **Hard-rime puncture:** normalize edilmiş uygunluk oranına göre bazı boyutlar doğrudan global best değerine taşınır.
4. **Positive greedy selection:** Yeni aday yalnız mevcut ajandan daha iyiyse popülasyona alınır.
5. **Boundary absorption:** Proje sözleşmesine uygun olarak adaylar değerlendirmeden önce `np.clip` ile [lb, ub] aralığına alınır.

## FE-bütçeli uyarlama

Özgün RIME uygulaması iterasyon sayısını kullanır; ders projesi ise kesin FE bütçesi ister. Bu nedenle:
- başlangıç değerlendirmeleri FE sayılır,
- sonraki her ajan değerlendirmesi bir FE sayılır,
- son popülasyon turu bütçe ortasında kesilebilir,
- ilerleme oranı, kalan bütçeye sığan tam/kısmi popülasyon turlarının sayısına göre `iteration / max_iter` olarak hesaplanır,
- `n_fes == max_fes` zorunludur.

Bu dönüşüm, yazar kodundaki arama mekanizmasını korurken dersin eşit FE karşılaştırması şartını sağlar. İterasyon tabanlı özgün deney sonuçlarıyla birebir performans eşdeğerliği iddia edilmez.

## Varsayılan parametreler

- `pop_size = 30`: ekipte diğer popülasyon tabanlı yöntemlerle ortak deney ölçeği için kullanılır.
- `w = 5`: yazarın kamuya açık MATLAB kodundaki soft-rime parametresidir.

Nihai makalede kullanılan değerler `src/main.py::ALGORITHMS` ile aynı olmalıdır.

## Kabul kontrolleri

`tests/test_rime.py` şu kontrolleri yapar:
- aynı seed ile birebir tekrar üretim,
- farklı seed ile farklı arama akışı,
- 1/7/29/30/31/73/121/137/1001 FE bütçelerinde exact FE,
- sınır dışı/NaN adayın değerlendirmeye ulaşmaması,
- `best_f == problem.evaluate(best_x)`,
- history'nin monoton artmayan en iyi-değer dizisi olması,
- ta001 üzerinde tam 20.000 FE,
- dönen random-key çözümünün geçerli PFSP permütasyonuna çözülmesi.

Kısa/pilot koşular bilimsel performans sonucu değildir.
