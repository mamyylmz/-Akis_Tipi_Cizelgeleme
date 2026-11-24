# 3.3.2. Parçacık Sürü Optimizasyonu (PSO)

**Durum:** Makaleye aktarılabilir yöntem metni · 24.11.2026

**Uygulama:** `src/algorithms/pso.py`

**Varyant:** FE ilerlemesine göre doğrusal azalan atalet ağırlıklı PSO

## Kaynak ve amaç

Parçacık Sürü Optimizasyonu, parçacığın kendi en iyi konumunu ve sürünün en iyi konumunu kullanır. Shi ve Eberhart (1998) hız denklemine atalet ağırlığını eklemiştir. Bu projede doğrusal ağırlık zamanlaması, tüketilen amaç fonksiyonu değerlendirmelerine göre tanımlanır. Sürü büyüklüğü, katsayılar ve hız sınırı aşağıdaki uygulama ayarlarıdır.

- J. Kennedy ve R. Eberhart, “Particle Swarm Optimization,” *Proceedings of ICNN’95*, 4, 1942–1948, 1995. DOI: [10.1109/ICNN.1995.488968](https://doi.org/10.1109/ICNN.1995.488968).
- Y. Shi ve R. Eberhart, “A Modified Particle Swarm Optimizer,” *Proceedings of the 1998 IEEE International Conference on Evolutionary Computation*, 69–73, 1998. DOI: [10.1109/ICEC.1998.699146](https://doi.org/10.1109/ICEC.1998.699146). Atalet ağırlığının tanıtıldığı yayıncı özetiyle doğrulandı.

## Başlatma

Her parçacık D boyutlu bir random-key konumu ve hız vektörü taşır. Başlangıç konumları `U(lb, ub)`, hızları `U(−v_max, v_max)` dağılımından bileşen bazında çekilir. Hız sınırı `v_max = v_frac × (ub − lb)` olarak hesaplanır. Bütün çekilişler `np.random.default_rng(seed)` ile yapılır. Başlangıç değerlendirmeleri FE bütçesine dahildir. Değerlendirilen başlangıç konumları kişisel en iyileri oluşturur. Sürü en iyisi, bunların en düşük amaç değerine sahip olanıdır.

## Hız ve konum güncellemesi

Her dış turun başında atalet ağırlığı, o ana kadar tüketilen FE sayısıyla hesaplanır ve tur boyunca sabit kalır. İlk ağırlık başlangıç değerlendirmelerinden sonra hesaplanır.

```text
w = w_max − (w_max − w_min) × fes / max_fes
v_i ← w × v_i + c1 × r1 × (pbest_i − x_i) + c2 × r2 × (gbest − x_i)
v_i ← clip(v_i, −v_max, v_max)
x_i ← clip(x_i + v_i, lb, ub)
```

Her parçacık güncellemesinde `r1` ve `r2` birbirinden bağımsız D boyutlu uniform vektörler olarak çekilir. Çarpımlar bileşen bazındadır. Kişisel en iyi ve sürü en iyisi kesin iyileşmede güncellenir. Tur içinde iyileşen sürü en iyisi, sonraki parçacıklar tarafından kullanılabilir. Ortak PFSP modeli anahtarları kararlı sıralamayla iş permütasyonuna dönüştürür ve Cmax değerini hesaplar.

## FE bütçesi ve deney parametreleri

Her `problem.evaluate()` çağrısı bir FE olarak sayılır. Başlatma ve sürü güncellemelerinde bütçe her çağrıdan önce kontrol edilir. Bütçe tur ortasında dolabilir. Yakınsama kaydı FE sayısını ve o ana kadarki en iyi Cmax değerini tutar. Son kayıt bütçenin dolduğu FE’de yazılır.

| Parametre | Değer | Uygulama |
|---|---:|---|
| Sürü büyüklüğü (`pop_size`) | 30 | Çalıştırıcı ve manifest ayarı |
| Atalet uç değerleri | w_max=0.9, w_min=0.4 | FE oranına bağlı doğrusal zamanlama |
| Bilişsel ve sosyal katsayılar | c1=2.0, c2=2.0 | Çalıştırıcı ve manifest ayarı |
| Hız aralığı çarpanı (`v_frac`) | 0.2 | Çalıştırıcı ve manifest ayarı, önceki fonksiyon varsayılanıyla aynı |
| Hız ve konum sınırları | [−0.2, 0.2] ve [0, 1] | PFSP random-key uzayında |
| Bütçe | 20.000 / 30.000 / 40.000 FE | ta001 / ta011 / ta021 |
| Final seed planı | 2026–2055 | Ortak deney protokolü |
