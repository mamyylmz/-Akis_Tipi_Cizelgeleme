# DBO ve NRBO: Özgün Yayın ↔ Yazar Kodu ↔ Proje Kodu Eşlemesi (P1 kanıtı)

**Tarih:** 23.11.2026 · **Hazırlayan:** Burak · **Bağımsız inceleme:** Şeref (bekliyor) · **P1 durumu:** `KISMİ`, Şeref'in incelemesine kadar.

Bu belge [quality_status.md](quality_status.md) dosyasındaki açık P1'in ("DBO/NRBO özgün yayın denklem eşleştirmesi") kapanış kanıtıdır. Karar kodları (D1, D2, N1–N3) [algorithm_interface.md §10](algorithm_interface.md) ile aynıdır.

## 1. Kaynağa erişim düzeyi

| Kaynak | Erişim | Ne için kullanıldı |
|---|---|---|
| **[DBO-P]** Xue & Shen (2023), *J. Supercomput.* 79:7305–7336, doi:10.1007/s11227-022-04959-6 | Yayıncı tam metni **açılmadı** (açık erişim değil). Künye yayıncı sayfasından doğrulandı ([source_audit.md](../paper/source_audit.md), L06). İnternette izinsiz bir tam metin kopyası (Scribd) var; telif nedeniyle **kullanılmadı**. | Künye |
| **[DBO-K]** Yazarın MATLAB demo kodu, "Programmed by Jian-kai Xue, Updated 28 Nov. 2022", File Exchange #121318 | Tam erişim (GitHub kopyaları, 18.11.2026'da iki kopyanın birebir aynı olduğu doğrulandı). Repoda tutulan kopya git geçmişinde: `git show 3fe65d8:docs/test_logs/21_dbo_author_matlab_reference.m` | Güncelleme satırları; **yazar her satıra kendi makalesinin denklem numarasını yorum olarak yazmış** (`% Equation (1)` … `(7)`) |
| **[DBO-S1]** Wang ve ark. (2024), *Biomimetics* 9(9):519, §2, doi:10.3390/biomimetics9090519 | Açık erişim; 18.11.2026'da okundu. 23.11.2026'da MDPI otomatik erişimi reddetti (HTTP 403), yeniden okunamadı | Denklem gövdeleri ve parametreler |
| **[DBO-S2]** Wang ve ark. (2024), *Biomimetics* 9(5):271, §2, doi:10.3390/biomimetics9050271, PMC11117920 | Açık erişim; 23.11.2026'da PMC'den okundu (metin çıkarımı; mutlak değer çizgileri çıkarımda kaybolmuş olabilir) | Denklem gövdeleri, parametreler ve θ metni: ikinci bağımsız teyit |
| **[NRBO-P]** Sowmya, Premkumar & Jangir (2024), *EAAI* 128:107532, doi:10.1016/j.engappai.2023.107532 | Yayıncı tam metni **açılmadı**. ScienceDirect otomatik erişimi reddetti (HTTP 403); açık erişim olup olmadığı da doğrulanamadı. Künye yayıncı sayfasından doğrulandı (L08) | Künye |
| **[NRBO-K]** Yazarların MATLAB kodu (`NRBO.m`, `SearchRule.m`, `Main.m`), github.com/mpremme/Newton-Raphson-Based-Optimizer-NRBO- (ikinci yazarın deposu); File Exchange #158066 (v1.0.1, 21.01.2024) | Tam erişim. Repoda tutulan kopya git geçmişinde: `git show 3fe65d8:docs/test_logs/22_nrbo_author_matlab_reference.m` (satır 1–128 `NRBO.m`, 130–173 `SearchRule.m`) | Bütün güncelleme satırları. Kodda **denklem numarası yorumu yok** |
| **[NRBO-S1]** Aljumah ve ark. (2026), *Sci. Rep.* 16:19639, doi:10.1038/s41598-026-58397-y, PMC13310854, "Standard NRBO algorithm" bölümü | Açık erişim. 18.11.2026'da denklemler okundu ve numaralar (17)–(35) kaydedildi. 23.11.2026'da HTML'de yalnız numaralar ve düzyazı okunabildi (denklemler görsel); PDF bot korumasına takıldı | Denklem numaraları (yalnız bu makalenin kendi numaraları) |

**Sonuç:**
- **DBO'nun özgün denklem numaraları (1)–(7) doğrulandı.** Üç bağımsız kanıt aynı numaralamayı veriyor: yazar kodundaki yorumlar [DBO-K], [DBO-S1] ve [DBO-S2]. Denklem gövdeleri tam metinden değil; ikincil kaynaklardan ve yazar kodundan doğrulandı.
- **NRBO'nun özgün denklem numaraları: `DOĞRULANAMADI`.** Yazar kodunda numara yok, ikincil kaynak [NRBO-S1] kendi numaralamasını kullanıyor ve özgün numaralara atıf yapmıyor. Bu yüzden aşağıdaki tabloda NRBO bileşenleri **adlarıyla** (NRSR, ΔX, ρ, X1, X2, X3, δ, TAO) ve yazar kodu satırıyla eşlenmiştir; [NRBO-S1] numarası yalnız yardımcı bir sütundur.
- Makale metninde NRBO denklemleri kendi makalemizin numaralarıyla verilmeli ve kaynak olarak bileşen adıyla [NRBO-P] gösterilmelidir; özgün denklem numarası **yazılmamalıdır**.

## 2. DBO eşlemesi

Proje kodu: [src/algorithms/dbo.py](../src/algorithms/dbo.py). "Yazar kodu" sütunu [DBO-K] kopyasının satırlarıdır.

| Özgün denk. | İfade (ikincil kaynaklar + yazar kodu) | Yazar kodu | Proje kodu | Eşleşme |
|---|---|---|---|---|
| (1) Yuvarlama | `x_i(t+1) = x_i(t) + α·k·x_i(t−1) + b·Δx`, `Δx = |x_i(t) − X^w|` | 41–42 (X^w = `x(B,:)`), 50–56 | [dbo.py:128](../src/algorithms/dbo.py#L128), [138–140](../src/algorithms/dbo.py#L138-L140) | Aynı. k = 0.1, b = 0.3; P(α = −1) = 0.1 yalnız yazar kodunda var ([DBO-S2] olasılık vermiyor) |
| — yuvarlama/dans kararı | Olasılık 0.9 ([DBO-S2] Algoritma 1, adım 5) | 43 (iterasyon başına tek `r2`), 48 | [dbo.py:133](../src/algorithms/dbo.py#L133) | Aynı, iterasyon başına bir kez |
| (2) Dans | `x_i(t+1) = x_i(t) + tan(θ)·|x_i(t) − x_i(t−1)|`, θ ∈ (0, π]; "θ = 0, π/2, π iken konum güncellenmez" ([DBO-S1], [DBO-S2]) | 59–65 | [dbo.py:142–151](../src/algorithms/dbo.py#L142-L151) | θ ∈ {1, …, 180}° aynı. **D1:** 90°/180°'de proje kodu metni izler, yazar kodu izlemez (bkz. §4) |
| (3) Yumurtlama bölgesi | `Lb* = max(X*·(1−R), Lb)`, `Ub* = min(X*·(1+R), Ub)`, `R = 1 − t/T_max` | 72–80 | [dbo.py:160–168](../src/algorithms/dbo.py#L160-L168) | Aynı (yazar kodu). Ub için bkz. §4, not 1. **D2:** `t/T_max → fes/max_fes` |
| (4) Yumurtlayan | `B_i(t+1) = X* + b1·(B_i(t) − Lb*) + b2·(B_i(t) − Ub*)`, b1, b2 ∈ U(0,1)^D | 87–90 (sonuç `[Xnew1, Xnew2]`'ye kırpılıyor) | [dbo.py:176–180](../src/algorithms/dbo.py#L176-L180) | Aynı, `[Lb*, Ub*]`'ye kırpma dahil |
| (5) Yiyecek bölgesi | `Lb^b = max(X^b·(1−R), Lb)`, `Ub^b = min(X^b·(1+R), Ub)` | 82–85 | [dbo.py:169–171](../src/algorithms/dbo.py#L169-L171) | Aynı. Ub için bkz. §4, not 1 |
| (6) Küçük böcek | `x_i(t+1) = x_i(t) + C1·(x_i(t) − Lb^b) + C2·(x_i(t) − Ub^b)`, C1 ~ N(0,1) skaler, C2 ∈ U(0,1)^D | 93–98 | [dbo.py:187–190](../src/algorithms/dbo.py#L187-L190) | Aynı |
| (7) Hırsız | `x_i(t+1) = X^b + S·g·(|x_i(t) − X*| + |x_i(t) − X^b|)`, g ~ N(0,1)^D, S = 0.5 | 102–106 (`./2` = S) | [dbo.py:197–199](../src/algorithms/dbo.py#L197-L199) | Aynı. Mutlak değerler yazar kodunda var; [DBO-S2] metin çıkarımında görünmüyor (bkz. §4, not 2) |
| Grup payları | %20 / %20 / %25 / kalan; N = 30 için 6/6/7/11 ([DBO-S2] §2.4) | 16, 20, 87, 93, 102 (12, 13:19, 20:pop sabit yazılmış) | [dbo.py:36–45](../src/algorithms/dbo.py#L36-L45) | N = 30'da aynı. Genel N formülü proje uyarlaması |
| Açgözlü kabul ve X^b | `x(t−1)` = önceki iterasyonun tutulan konumları | 108–122 | [dbo.py:203–208](../src/algorithms/dbo.py#L203-L208) | Aynı |
| Parametreler | N = 30, k = 0.1, b = 0.3, S = 0.5 | — | [main.py:68](../src/main.py#L68) ve [dbo.py](../src/algorithms/dbo.py) varsayılanları | Aynı |

## 3. NRBO eşlemesi

Proje kodu: [src/algorithms/nrbo.py](../src/algorithms/nrbo.py). "Yazar kodu" sütunu [NRBO-K] kopyasının satırlarıdır. Özgün denklem numarası: `DOĞRULANAMADI` (§1).

| Bileşen | İfade (yazar kodu) | [NRBO-S1] no.¹ | Yazar kodu | Proje kodu | Eşleşme |
|---|---|---|---|---|---|
| Başlangıç | `X_n = lb + rand·(ub − lb)` | (17) | 36 | [nrbo.py:110](../src/algorithms/nrbo.py#L110) | Aynı |
| En iyi / en kötü | Sıralamayla başlangıç en iyi ve en kötü | — | 45–49 | [nrbo.py:117–121](../src/algorithms/nrbo.py#L117-L121) | Aynı (kararlı sıralama) |
| δ | `δ = (1 − 2t/T_max)^5`, iterasyon başında | (29) | 57 | [nrbo.py:128](../src/algorithms/nrbo.py#L128) | **N1:** `t/T_max → fes/max_fes` |
| ρ | `ρ = rand·(X_best − X_n) + rand·(X_r1 − X_r2)`, r1 ≠ r2 (`randperm(N,2)`) | (25) | 62–66 | [nrbo.py:134–136](../src/algorithms/nrbo.py#L134-L136) | Aynı |
| ΔX | `ΔX = rand(1,D)·|X_best − X_n|` | (19) | 156 | [nrbo.py:45](../src/algorithms/nrbo.py#L45) | Aynı |
| İlk NRSR adımı | `randn·((X_best − X_worst)·ΔX) / (2·(X_best + X_worst − 2·X_n))`, `X_a = X_n − NRSR + ρ` | (20) | 159–166 | [nrbo.py:46–48](../src/algorithms/nrbo.py#L46-L48) | Aynı (`Flag = 1` dalı) |
| y_p, y_q | `y_p = r1·(m + r1·ΔX)`, `y_q = r2·(m − r2·ΔX)`, `m = mean(X_a + X_n)` **skaler** | (26)–(27) | 169–171 | [nrbo.py:49–53](../src/algorithms/nrbo.py#L49-L53) | Aynı |
| NRSR | `randn·((y_p − y_q)·ΔX) / (2·(y_p + y_q − 2·X_n))` | (18)/(21)² | 172 | [nrbo.py:54](../src/algorithms/nrbo.py#L54) | Aynı. Payda için önlem yok (**N3**) |
| X1, X2 | `X1 = X_n − NRSR + ρ`, `X2 = X_best − NRSR + ρ` | (23)–(24) | 71–72 | [nrbo.py:139–140](../src/algorithms/nrbo.py#L139-L140) | Aynı |
| X3 | `X3 = X_n − δ·(X2 − X1)` | (28) | 77 | [nrbo.py:146](../src/algorithms/nrbo.py#L146) | Yazar koduyla aynı. [NRBO-S1]'deki fazladan `a·` çarpanı yazar kodunda yok (§4, not 3) |
| Yeni konum | `X_new = a1·(a1·X1 + (1−a2)·X2) + (1−a2)·X3`, a1, a2 boyut başına | (22) | 76–80 | [nrbo.py:147–150](../src/algorithms/nrbo.py#L147-L150) | Aynı. **N2:** çekiliş sırası `a1_j, a2_j` |
| TAO | rand < DF ise: `(μ1 < 0.5 ? X_new : X_best) + θ1·(μ1·X_best − μ2·X_n) + θ2·δ·(μ1·mean(X) − μ2·X_n)`; β ∈ {0,1}, μ1 = 3β·rand + (1−β), μ2 = β·rand + (1−β), θ1 ∈ U(−1,1), θ2 ∈ U(−0.5,0.5) | (30)–(35) | 83–95 | [nrbo.py:153–164](../src/algorithms/nrbo.py#L153-L164) | Aynı. `mean(X)` popülasyon ortalaması vektörü, güncel X ile |
| Sınır | `min(max(X_new, LB), UB)` | — | 98 | [nrbo.py:105–107](../src/algorithms/nrbo.py#L105-L107), [166](../src/algorithms/nrbo.py#L166) | Aynı davranış: NaN → LB, ±Inf → sınır (**N3**) |
| Kabul, en iyi ve en kötü | Açgözlü; en iyi hemen güncellenir; en kötü yalnız daha kötü bir değer görülünce değişir | 104–119 | [nrbo.py:169–177](../src/algorithms/nrbo.py#L169-L177) | Aynı |
| Parametreler | N = 30, DF = 0.6 | — | 29 (DF); `Main.m` (N) | [main.py:69](../src/main.py#L69) | Aynı |

¹ [NRBO-S1] makalesinin **kendi** numaraları; özgün [NRBO-P] numaraları değildir. 18.11.2026 okumasından alındı. 23.11.2026'da denklem görselleri yeniden açılamadığı için **bu oturumda yeniden doğrulanmadı**. Şeref'in tarayıcıdan PMC13310854'ü açıp bu sütunu kontrol etmesi gerekiyor.
² Düzyazıdan (18) "NRSR is based on the following formula" ve (21) "weighted differences" okunuyor; asıl NRSR'nin (18) mi (21) mi olduğu görsel açılmadan ayırt edilemiyor.

## 4. Özgün / proje uyarlaması ayrımı

| Kod | Konu | Sınıf | Açıklama |
|---|---|---|---|
| D1 | DBO dans, θ = 90°/180° | **Özgün metin** (yazar kodundan bilinçli sapma) | İki bağımsız ikincil kaynak "θ = 0, π/2, π iken konum güncellenmez" diyor; proje kodu bunu izliyor. Yazar kodu koruma satırını (60–62) hemen ardından `tan` güncellemesiyle eziyor (65). θ = 0 hiç çekilmediği için yalnız 90° ve 180° etkileniyor |
| D2 | DBO `R` | **Proje uyarlaması** | `t/T_max → fes/max_fes` (ders şablonu kuralı). Hesaplanma noktası (yuvarlama grubundan sonra, iterasyon başına bir kez) yazar koduyla aynı |
| — | DBO bölge sınırlarında min/max sıralaması | **Proje uyarlaması** | Yalnız negatif koordinatlarda etkili. PFSP'de `lb = 0`, `ub = 1` ([problem.py:53–54](../src/problem.py#L53-L54)), dolayısıyla `X·(1−R) ≤ X·(1+R)` her zaman doğru ve sıralama hiçbir şey değiştirmiyor |
| — | DBO genel N için grup payları | **Proje uyarlaması** | N = 30'da 6/6/7/11, özgünle aynı. Yazar kodu bu değerleri sabit yazmış |
| N1 | NRBO `δ` | **Proje uyarlaması** | `t/T_max → fes/max_fes`. Hesaplanma noktası iterasyon başı, yazar koduyla aynı |
| N2 | NRBO a1/a2 sırası | **Özgün (yazar kodu)** | Boyut başına `a1`, ardından `a2`. RNG değerleri MATLAB ile birebir değil, yalnız çekiliş sırası aynı |
| N3 | NRBO payda | **Özgün (yazar kodu)** | Önlem yok. `np.fmin/np.fmax` MATLAB'ın `min/max` NaN davranışını aynen uyguluyor; bu bir uygulama ayrıntısı, davranış değişikliği değil |
| — | Bütçenin grup/popülasyon içinde bitmesi | **Proje uyarlaması** | `fes == max_fes` olunca döngü grup ortasında da duruyor (eşit FE kuralı) |

Notlar:
1. **DBO Ub üst sınırı.** [DBO-S2] (3) ve (5)'te üst sınırı `X·(1−R)` olarak basıyor. Bu, alt sınırla aynı ifade; sıfır genişlikte bir bölge verir ve (4)'teki kırpma her yumurtlayanı tek bir noktaya çeker. Yazar kodu `X·(1+R)` kullanıyor (78, 83). 18.11 taslağı bunu "ikincil kaynakta yazım hatası" diye niteliyordu. Ancak iki bağımsız ikincil kaynağın aynı hatayı taşıması, hatanın **özgün makale metninden** gelmiş olabileceğini düşündürüyor. Özgün metin açılmadığı için bu `DOĞRULANAMADI`. Proje kodu yazar kodunu izliyor.
2. **DBO (7) mutlak değerleri.** Yazar kodunda var (103). [DBO-S1] 18.11 okumasında vardı; [DBO-S2]'nin metin çıkarımında görünmüyor (çıkarımda kaybolmuş olabilir). Proje kodu yazar kodunu izliyor.
3. **NRBO X3'teki `a·`.** [NRBO-S1] (28)'de fazladan bir `a·` çarpanı var (18.11 okuması); yazar kodunda yok. Proje kodu yazar kodunu izliyor.

## 5. Sonuç

- **Kod değişikliği gerekmiyor.** Her güncelleme satırı yazar koduyla aynı ya da §4'te sınıflandırılmış bir kararla ayrılıyor. Parametreler kaynak ile kod arasında aynı ([main.py:68–69](../src/main.py#L68-L69)). Kod değişmediği için regresyon kapısı gerekmiyor; yine de birim testleri 23.11.2026'da yeniden çalıştırıldı (teslim kaydına bakınız).
- **Açık kalan, erişimden kaynaklanan sınırlar** (kod kararını etkilemiyor): DBO Ub `(1±R)` ifadesinin özgün metindeki hali, NRBO özgün denklem numaraları, [NRBO-S1] sütununun yeniden okunması.
- Önerilen P1 kapanışı: Şeref §1'deki erişim beyanını ve §2–§3'ten en az bir satır grubunu bağımsız olarak doğrularsa, akademik P1 **erişim sınırı açıkça beyan edilmiş olarak** kapatılabilir. `DOĞRULANAMADI` maddeleri makale metninde de bu şekilde kalır.
