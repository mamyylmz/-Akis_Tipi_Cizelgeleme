# Yöntem Notları: DBO ve NRBO

**Sürüm 1.0 · 23.11.2026 · Burak** · Durum: P1 kanıtına göre finalleştirildi; Şeref'in bağımsız incelemesi bekleniyor. Bu dosyada sonuç yoktur; yalnızca yöntem, denklem ve parametre notları vardır. Makalenin §3.3.3 ve §3.3.5 alt başlıklarına ([outline.md](outline.md)) kaynak olacaktır.

**Denklem ↔ yazar kodu ↔ proje kodu eşlemesi** satır düzeyinde [docs/dbo_nrbo_equation_mapping.md](../docs/dbo_nrbo_equation_mapping.md) dosyasındadır. Bu dosyadaki her iddia oradaki tabloya dayanır.

**Kaynağa erişim düzeyi:** İki özgün makalenin de yayıncı tam metni **açılmadı** (ikisi de açık erişimde değil ya da otomatik erişime kapalı). Künye ve DOI, Bilal'in [literature_matrix.md](literature_matrix.md) (L06, L08) ve [source_audit.md](source_audit.md) kayıtlarında yayıncı sayfasından doğrulanmış.
- **DBO:** Özgün denklem numaraları (1)–(7) doğrulandı: yazar kodundaki `% Equation (n)` yorumları ve iki bağımsız açık erişim makalesi aynı numaralamayı veriyor. Denklem gövdeleri bu iki ikincil kaynakla, kod ise yazarın MATLAB koduyla satır satır karşılaştırıldı.
- **NRBO:** Özgün denklem numaraları `DOĞRULANAMADI` (yazar kodunda numara yok, ikincil kaynak kendi numaralamasını kullanıyor). Bileşenler adlarıyla (NRSR, ΔX, ρ, X1, X2, X3, δ, TAO) yazarların MATLAB koduyla satır satır eşlendi. Aşağıdaki numaralar ikincil kaynak [S1]'e aittir; makale metninde **özgün numara olarak yazılmayacak**, kendi makale numaralarımız kullanılacaktır.

## 3.3.3. Dung Beetle Optimizer (DBO)

**Birincil kaynak.** Xue, J., & Shen, B. (2023). Dung beetle optimizer: A new meta-heuristic algorithm for global optimization. *The Journal of Supercomputing, 79*, 7305–7336. https://doi.org/10.1007/s11227-022-04959-6

**Denklem kontrolü için ikincil kaynaklar.** [DBO-S1] Wang, X. ve ark. (2024). An Adaptive Spiral Strategy Dung Beetle Optimization Algorithm. *Biomimetics, 9*(9), 519, §2. https://doi.org/10.3390/biomimetics9090519 · [DBO-S2] Wang ve ark. (2024). A Sinh–Cosh-Enhanced DBO Algorithm Applied to Global Optimization Problems. *Biomimetics, 9*(5), 271, §2. https://doi.org/10.3390/biomimetics9050271

**Arama mekanizması.** Popülasyon dört role ayrılır. Her rolün kendi güncelleme kuralı vardır:

| Rol | Pay (N=30) | Kural | İşlev |
|---|---|---|---|
| Top yuvarlayan | %20 (6) | Denk. (1) ya da dans, Denk. (2) | En kötüden uzaklaşarak keşif |
| Yumurtlayan (brood ball) | %20 (6) | Denk. (3)–(4) | Yerel en iyi X\* çevresinde daralan bölgede sömürü |
| Küçük (yiyecek arayan) | %25 (7) | Denk. (5)–(6) | Global en iyi X^b çevresinde arama |
| Hırsız | %35 (11) | Denk. (7) | X^b çevresinde sömürü |

**Denklemler** (numaralar özgün makalenin numaralarıdır; t: iterasyon, T_max: en büyük iterasyon):

1. Yuvarlama: `x_i(t+1) = x_i(t) + α·k·x_i(t−1) + b·Δx`, `Δx = |x_i(t) − X^w|`. α ∈ {1, −1} sapma göstergesi, k ∈ (0, 0.2] sapma katsayısı, b ∈ (0, 1) sabit, X^w global en kötü.
2. Dans (engel, olasılık 1 − 0.9): `x_i(t+1) = x_i(t) + tan(θ)·|x_i(t) − x_i(t−1)|`, θ ∈ (0, π]. θ = π/2 ya da π ise konum değişmez.
3. Yumurtlama bölgesi: `Lb* = max(X*·(1−R), Lb)`, `Ub* = min(X*·(1+R), Ub)`, `R = 1 − t/T_max`.
4. Yumurtlayan: `B_i(t+1) = X* + b1·(B_i(t) − Lb*) + b2·(B_i(t) − Ub*)`, b1 ve b2 ∈ U(0,1)^D. Sonuç [Lb\*, Ub\*] içine kırpılır.
5. Yiyecek bölgesi: `Lb^b = max(X^b·(1−R), Lb)`, `Ub^b = min(X^b·(1+R), Ub)`.
6. Küçük böcek: `x_i(t+1) = x_i(t) + C1·(x_i(t) − Lb^b) + C2·(x_i(t) − Ub^b)`, C1 ~ N(0,1) skaler, C2 ∈ U(0,1)^D.
7. Hırsız: `x_i(t+1) = X^b + S·g·(|x_i(t) − X*| + |x_i(t) − X^b|)`, g ~ N(0,1)^D.

> **Yazar kodu ile karşılaştırma (18.11.2026).** Yazarların MATLAB demo kodu ("Programmed by Jian-kai Xue, Updated 28 Nov. 2022", File Exchange #121318) GitHub kopyalarından alındı. İki bağımsız kopya birebir aynı. Yazar kodu referansı: MATLAB Central File Exchange #121318 (`https://www.mathworks.com/matlabcentral/fileexchange/121318-dung-beetle-optimizer-a-new-meta-heuristic-algorithm`). Depoda üçüncü taraf kaynak kod kopyası tutulmaz. Koddan doğrulananlar:
> - Denk. (3)/(5)'te üst sınır `X·(1+R)`. İki ikincil kaynak da üst sınırı `X·(1−R)` olarak basıyor; bu, alt sınırla aynı ifade ve sıfır genişlikte bir bölge verir. Aynı ifadenin iki bağımsız kaynakta bulunması, hatanın özgün metinden gelmiş olabileceğini düşündürüyor. Özgün metindeki hali `DOĞRULANAMADI`; proje kodu yazar kodunu izliyor.
> - Denk. (7)'de mutlak değerler var ve S = 0.5 (`./2`).
> - α = −1 olasılığı 0.1.
> - θ, 1–180 derece arasından tamsayı olarak çekiliyor.
> - Yuvarlama/dans kararı iterasyon başına bir kez veriliyor.
> - Grup indisleri 6/6/7/11, kabul açgözlü.
>
> **Bilinçli tek sapma:** Makale metni θ = π/2 ya da π olduğunda konumun güncellenmediğini söylüyor. Yazar kodu bu durumda önce `x = pX` atıyor, sonra satırı `tan` güncellemesiyle eziyor. Bizim kod makale metnini izliyor.
>
> Yayıncı tam metni hâlâ açılmadı. Kodun özgün makaleyle eşleştiği, yazarın kendi kodu üzerinden doğrulandı.

**Parametreler (kaynak değerleri):** N = 30, k = 0.1, b = 0.3, S = 0.5, yuvarlama/dans olasılığı 0.9, α = −1 olasılığı 0.1. Hepsi yazar kodunda doğrulandı.

**Projeye uyarlama.** `t/T_max` yerine `fes/max_fes` kullanılıyor. Her yeni konum değerlendirilir (1 FE). Her böcek, yeni konumu daha iyiyse onu tutar (açgözlü kabul). Kod: [src/algorithms/dbo.py](../src/algorithms/dbo.py).

## 3.3.5. Newton–Raphson-Based Optimizer (NRBO)

**Birincil kaynak.** Sowmya, R., Premkumar, M., & Jangir, P. (2024). Newton-Raphson-based optimizer: A new population-based metaheuristic algorithm for continuous optimization problems. *Engineering Applications of Artificial Intelligence, 128*, 107532. https://doi.org/10.1016/j.engappai.2023.107532

**Denklem kontrolü için ikincil kaynaklar.** [S1] Sci. Rep. (2026), PMC13310854, orijinal NRBO bölümü, Denk. 17–35. [S2] Sci. Rep. (2025), PMC12000557, TAO bölümü.

**Yazar kodu ile karşılaştırma (18.11.2026).** Yazarların MATLAB kodu (`NRBO.m`, `SearchRule.m`, `Main.m`; başlıkta "Authors, Inventors, and Programmers: Dr. Sowmya R, Dr. M. Premkumar, and Dr. Pradeep Jangir"), ikinci yazarın GitHub deposundan alındı: `mpremme/Newton-Raphson-Based-Optimizer-NRBO-`, 21.01.2024'te açılmış. Bağımsız bir kopya birebir aynı. Yazar kodu referansı: `https://github.com/mpremme/Newton-Raphson-Based-Optimizer-NRBO-`. Depoda üçüncü taraf kaynak kod kopyası tutulmaz.

**Arama mekanizması.** NRBO iki kurala dayanır. Newton–Raphson Arama Kuralı (NRSR), türevsiz bir Newton adımı kurar: ikinci türevi merkezi farkla yaklaştırır ve fonksiyon değeri yerine konumları kullanır. Tuzaktan Kaçınma Operatörü (TAO), DF olasılığıyla uygulanan, en iyi çözüme ve popülasyon ortalamasına dayalı bir sıçramadır.

**Denklemler** ([S1] makalesinin kendi numaralarıyla, yazar koduyla eşleştirildi; bu numaralar özgün makalenin numaraları değildir ve 18.11.2026 okumasından alınmıştır, bkz. eşleme belgesi §3):

- Başlangıç (17): `X_n = lb + rand·(ub − lb)`.
- Adım (19): `ΔX = rand(1,D)·|X_best − X_n|`.
- İlk NRSR adımı (20): `NRSR = randn·((X_best − X_worst)·ΔX) / (2·(X_best + X_worst − 2·X_n))`, ardından `X_a = X_n − NRSR + ρ`.
- Yardımcı noktalar (26–27): `y_p = r1·(m + r1·ΔX)`, `y_q = r2·(m − r2·ΔX)`. Burada `m = mean(X_a + X_n)` boyutlar üzerinden alınan **tek bir sayı**dır (MATLAB'da satır vektörünün ortalaması).
- Asıl NRSR: `NRSR = randn·((y_p − y_q)·ΔX) / (2·(y_p + y_q − 2·X_n))`.
- ρ (25): `ρ = rand·(X_best − X_n) + rand·(X_r1 − X_r2)`. İki indis `randperm(N,2)` ile, birbirinden farklı çekilir.
- (23)–(24): `X1 = X_n − NRSR + ρ`, `X2 = X_best − NRSR + ρ`.
- (28): `X3 = X_n − δ·(X2 − X1)`. [S1]'deki fazladan `a·` çarpanı yazar kodunda yok.
- Uyarlamalı katsayı (29): `δ = (1 − 2t/T_max)^5`. Bu katsayı ikinci yarıda negatife döner ve sonda −1 olur.
- Yeni konum (22), her boyut için sırayla çekilen yeni a1, a2 ile: `X_new = a1·(a1·X1 + (1−a2)·X2) + (1−a2)·X3`. Python uygulaması çekiliş sırasını yazar kodundaki boyut-başına `a1` ardından `a2` düzeniyle eşler.
- TAO (30–35), rand < DF ise: `X_TAO = (μ1 < 0.5 ise X_new, değilse X_best) + θ1·(μ1·X_best − μ2·X_n) + θ2·δ·(μ1·mean(X) − μ2·X_n)`.
  - `mean(X)` popülasyon ortalaması vektörüdür.
  - `β ∈ {0,1}`, olasılık 0.5; `μ1 = 3β·rand + (1−β)`, `μ2 = β·rand + (1−β)`.
  - `θ1 ∈ U(−1,1)`, `θ2 ∈ U(−0.5,0.5)`.
- Kabul: yeni konum daha iyiyse alınır. En iyi çözüm hemen güncellenir. En kötü çözüm yalnızca daha kötü bir değer görülünce değişir; açgözlü kabul yüzünden bu hiç olmaz, yani başlangıçtaki en kötü korunur.

**Parametreler (yazar kodu):** N = 30, DF = 0.6.

**Payda sıfır olduğunda.** Yazar kodunda bir önlem yok. MATLAB'daki `min(max(x, LB), UB)` NaN'ı alt sınıra, +Inf'i üst sınıra, −Inf'i alt sınıra çeker. Bizim kod aynı davranışı `np.fmax/np.fmin` ile uyguluyor; NaN hiçbir zaman değerlendirmeye ulaşmıyor. Testte, sınırların eşit olduğu bir problemle 2970 NRSR adımının hepsinde 0/0 oluşturuldu; bunların hiçbiri değerlendirmeye geçmedi.

**Projeye uyarlama.** `t/T_max` yerine `fes/max_fes` kullanılıyor. Her yeni konum değerlendirilir (1 FE). Kod: [src/algorithms/nrbo.py](../src/algorithms/nrbo.py). Test: [tests/test_nrbo.py](../tests/test_nrbo.py).

**Durum:** Yazar koduyla satır düzeyinde eşleştirildi; kod değişikliği gerekmedi. Final kabul Şeref'in bağımsız incelemesinden sonra verilecektir.

## Özgün / proje uyarlaması ayrımı (23.11.2026)

Ayrıntılı gerekçeler [docs/algorithm_interface.md §10](../docs/algorithm_interface.md) ve [eşleme belgesi §4](../docs/dbo_nrbo_equation_mapping.md)'te. Makale için özet:

**Özgün kaynağa (metin ya da yazar kodu) bağlı kalınanlar**
- DBO, θ = 90°/180°: konum güncellenmiyor. Bu, makale metnini izliyor ve yazar kodundan bilinçli bir sapma (D1).
- NRBO a1/a2 çekiliş sırası: boyut başına önce `a1`, sonra `a2` çekiliyor, yazar kodundaki gibi (N2).
- NRBO paydası: önlem yok, yazar kodundaki gibi. NaN ve ±Inf, MATLAB'daki gibi sınıra çekiliyor (N3).

**Proje uyarlamaları** (eşit FE altında karşılaştırma için)
- DBO'daki `R` ve NRBO'daki `δ`: `t/T_max` yerine `fes/max_fes` kullanılıyor. Hesaplanma noktaları yazar koduyla aynı (D2, N1).
- FE bütçesi grup ya da popülasyon ortasında bitebilir; döngü tam `max_fes`'te duruyor.
- DBO grup payları genel N için formülle hesaplanıyor; N = 30'da 6/6/7/11, özgünle aynı.
- DBO bölge sınırları min/max ile sıralanıyor. PFSP'de koordinatlar [0, 1] aralığında olduğu için bunun hiçbir etkisi yok.
