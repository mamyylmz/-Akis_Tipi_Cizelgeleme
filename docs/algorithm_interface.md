# Ortak Algoritma Arayüzü (K-API)

**Sürüm 1.0 · 18.11.2026 · Sahibi: Burak (teknik lider)** · Bağımsız inceleme: Tarık (FE/seed), Şeref (model uyumu) — **BEKLİYOR**

Bu belge, beş algoritmanın (DE, PSO, DBO, RIME, NRBO) uyması gereken sözleşmeyi kaydeder. Kaynağı ders şablonudur: [src/main.py](../src/main.py) içindeki `check_algorithm()` ve [src/algorithms/pso.py](../src/algorithms/pso.py) başlığındaki 7 kural. Bu belge şablonu değiştirmez; şablonla çelişirse şablon geçerlidir.

## 1. İmza

```python
def <ad>(problem, max_fes, seed, **parametreler) -> dict
```

- Dosya adı = fonksiyon adı: `src/algorithms/dbo.py` → `dbo`.
- Parametrelerin hepsi anahtar sözcüklü ve varsayılanlıdır. Varsayılanlar özgün yayından gelir; `main.py` içindeki `ALGORITHMS` sözlüğünde aynı adlarla açıkça yazılır ve makalenin parametre tablosuna aynen geçer.
- Geçersiz parametre (`pop_size` çok küçük, olasılık [0,1] dışında vb.) `ValueError` verir; sessizce düzeltilmez.

## 2. Problemden yalnızca şunlar kullanılır

| Öğe | PFSP'deki değeri |
|---|---|
| `problem.dim` | iş sayısı n (zorunlu örneklerde 20) |
| `problem.lb`, `problem.ub` | `zeros(n)`, `ones(n)` |
| `problem.evaluate(x)` | `Cmax(argsort(clip(x), kind="stable"))`, küçük olan iyidir |

Algoritma `decode`, `objective`, `processing_times` gibi PFSP'ye özgü öğelere **dokunmaz**. Permütasyon yerel araması ayrı bir ablation deneyidir, beş algoritmanın içine eklenmez.

## 3. FE sayımı

1. Her `problem.evaluate()` çağrısı bir FE'dir, başlangıç popülasyonu dahil. Çağrı yalnızca algoritma içindeki `evaluate()` yardımcı fonksiyonuyla yapılır. Bu yardımcı sayacı, en iyi çözümü ve `history`'yi günceller.
2. Ana döngü `while fes < max_fes`. Her değerlendirmeden önce `if fes >= max_fes: break` yazılır. Bütçe popülasyonun ya da bir alt grubun ortasında bitebilir.
3. Sonuç: `n_fes == max_fes` (ne az ne çok). `main.py --check` iki yönü de sınar.
4. İterasyona bağlı katsayılar (`t/T`, DBO'nun `R`'si, NRBO'nun `δ`'sı) harcanan FE oranıyla hesaplanır: `t/T → fes/max_fes`. Bu bir uyarlamadır, makalede "uyarlama" olarak yazılır.
   - **Kabul edilen alternatif (20.11.2026, PFSP-RIME-01):** Yazar kodunda katsayı iterasyon indeksine periyodik ya da basamaklı biçimde bağlıysa (RIME'daki `cos(π·it/(Max_iter/10))` ve `round(it·W/Max_iter)` gibi), iterasyon indeksi korunabilir. Koşulları: `Max_iter = ceil((max_fes − N)/N)` olarak hesaplanır, son tur bütçe bitince kesilir ve seçim algoritmanın dosya başlığında ve yöntem notunda belgelenir. Şu an bunu RIME kullanıyor.
5. Sayaç dışında değerlendirme yoktur: "en iyiyi tekrar hesaplama", "yeniden sıralama için değerlendirme" gibi çağrılar da FE'dir.

## 4. Rastgelelik

- Tek kaynak: `rng = np.random.default_rng(seed)`. `np.random.*` ile global durum, `random` modülü ve zamana bağlı tohum kullanılmaz.
- Aynı seed ile iki koşu, `best_f`, `best_x` ve `history` bakımından birebir aynı olmalıdır. Farklı seed farklı RNG akışını başlatmalıdır; ayrık PFSP arama uzayında farklı seed'lerin aynı final `best_x`/permütasyona ulaşması mümkündür ve hata değildir.
- Deney tohumu: `SEED_BASE + k` (`main.py`, `SEED_BASE = 2026`), her algoritmada aynı k. koşu aynı tohumla başlar.

## 5. Sınırlar

- Değerlendirilen her aday önce `np.clip(x, lb, ub)` ile sınırlar içine alınır. Algoritmanın kendi alt bölgesi varsa (DBO'nun yumurtlama bölgesi `[Lb*, Ub*]`) önce o bölgeye, o bölge de `[lb, ub]`'ye kırpılır.
- Kırpma, random-key çözümlemesini bozmaz: `argsort(kind="stable")` eşit anahtarlarda indeks sırasını korur ve her zaman tam bir permütasyon üretir. Sınırda biriken eşit anahtarlar ise düz bölgeler oluşturur (H2 ile ilgili, ayrıca ölçülmeli).

## 6. Dönüş sözlüğü

| Anahtar | Kural |
|---|---|
| `best_x` | uzunluğu `dim`, sınırlar içinde; `problem.evaluate(best_x) == best_f` |
| `best_f` | float, değerlendirilen tüm adayların en küçüğü |
| `history` | `[(fes, best_f_o_ana_kadar), …]`, yaklaşık 100 nokta (`log_every = max(1, max_fes // 100)`), artmayan, son eleman `(max_fes, best_f)` |
| `n_fes` | kullanılan FE (`== max_fes`) |
| `time` | `time.perf_counter()` farkı, saniye |

Fonksiyon ekrana yazmaz, dosya kaydetmez. `if __name__ == "__main__":` bloğundaki küre testi yalnızca **smoke test**'tir; çıktısı PFSP sonucu değildir.

## 7. Kod standardı

- Python, 4 boşluk girinti, snake_case. Denklem değişkenleri kaynaktaki harfleriyle adlandırılabilir (`X_star`, `Lb_star`); her denklemin yanında kaynak denklem numarası yorum olarak yazılır.
- Dosya başlığı: birincil kaynak künyesi + DOI, **kaynağa erişim düzeyi** (tam metin / ikincil kaynak / DOĞRULANAMADI) ve projeye özgü uyarlamalar.
- `mealpy`, `niapy`, `pymoo`, `DEAP` gibi kütüphaneler sonuç üretmek için kullanılmaz.
- Henüz bitmemiş algoritma `NotImplementedError` verir ve `ALGORITHMS`'e eklenmez. `main.py --check` bu durumda "henüz tamamlanmamış" der; bu PASS sayılmaz.

## 8. Kabul testleri (her algoritma için `tests/test_<ad>.py`)

1. ta001'de `max_fes=600`, aynı seed ile iki koşu: `best_f`, `best_x` eşit; `n_fes == 600`; `history[-1][0] == 600`; history artmayan.
2. Bağımsız sayaç: `evaluate`'i saran bir sınıf çağrıları sayar ve sınır dışı adayları yakalar. Tek ve küçük bütçelerde (1, 29, 31, 137 …) `çağrı == max_fes` ve sınır dışı = 0.
3. `best_x` çözümlenince geçerli permütasyon verir; `problem.objective(decode(best_x)) == best_f`.
4. En az bir tam ders bütçesi koşusu (ör. ta001 / 20.000 FE), `best_f ≥ BKS`.
5. Geçersiz parametre `ValueError` verir.

Örnek: [tests/test_dbo.py](../tests/test_dbo.py), [tests/test_de.py](../tests/test_de.py).

## 9. Algoritma durum tablosu (22.11.2026)

| Algoritma | Dosya | `ALGORITHMS`'te | Durum |
|---|---|---|---|
| PSO | `src/algorithms/pso.py` | evet | teknik 5/5 contract kapısı PASS; final makale yöntem/kaynak metni tamamlanacak |
| DE | `src/algorithms/de.py` | evet | nesil tabanlı düzeltme ve teknik 5/5 contract kapısı PASS; final DE yöntem metni tamamlanacak |
| DBO | `src/algorithms/dbo.py` | evet | teknik contract PASS; özgün yayın denklem ↔ kod akademik P1 açık |
| RIME | `src/algorithms/rime.py` | evet | PR #4 ile `develop` içine kabul edildi; kaynak/kod ve 5/5 contract kapısı PASS |
| NRBO | `src/algorithms/nrbo.py` | evet | teknik contract PASS; özgün yayın denklem ↔ kod akademik P1 açık |

## 10. DBO ve NRBO kaynak uyarlama kararları (20.11.2026)

Bu bölümdeki uygulama kararları yazar kodları ve erişilen yöntem kaynaklarıyla karşılaştırılmıştır. DBO yazar kodu: https://www.mathworks.com/matlabcentral/fileexchange/121318-dung-beetle-optimizer-a-new-meta-heuristic-algorithm ; NRBO yazar kodu: https://github.com/mpremme/Newton-Raphson-Based-Optimizer-NRBO- . Özgün yayın denklem ↔ proje kodu eşleştirmesinin son akademik P1 durumu [quality_status.md](quality_status.md) içinde izlenir.

| Kod | Algoritma | Yazar kodu | Bizim kod | Karar ve gerekçe |
|---|---|---|---|---|
| D1 | DBO dans, θ = 90°/180° | Önce `x = pX` atanıyor, sonra satır `tan(θ)` güncellemesiyle eziliyor. 90°'de adım `tan(π/2) ≈ 1,6·10¹⁶` (böcek sınıra fırlıyor), 180°'de `tan(π) ≈ −1,2·10⁻¹⁶` (pratikte hareket yok) | Konum güncellenmiyor | **Makale metni izleniyor.** Yazar kodundaki koruma satırı ölü kod; 90°'deki adım kayan nokta yapaylığı ve sınırda birikmeyi artırır. 180°'de iki davranış pratikte aynı. Etki: dans adımlarının 1/180'i |
| D2 | DBO `R = 1 − t/T_max` | Yuvarlama grubundan sonra, iterasyon başına bir kez; `t` = iterasyon sayısı | Aynı noktada, iterasyon başına bir kez; `t/T_max → fes/max_fes` | **Korunuyor.** Hesaplanma noktası yazar koduyla aynı; FE oranı ders şablonunun kuralı (§3.4). Tarık'ın sabit çekiliş testi bu davranışı doğruluyor |
| N1 | NRBO `δ = (1 − 2t/T_max)^5` | İterasyon başında, `it = 1`'den başlayarak | İterasyon başında, `fes/max_fes` ile. İlk iterasyonda `fes = N`, yani `2N/max_fes ≈ 2/MaxIt`; yazarın `it = 1` başlangıcıyla aynı | **Korunuyor** |
| N2 | NRBO a1, a2 çekiliş sırası | Her boyut için sırayla `a1, a2` | `rng.random((D, 2))` ile satır-major `a1_0,a2_0,a1_1,a2_1,...` sırası | **Kaynak sırasına yaklaştırıldı.** NumPy ve MATLAB RNG değerleri birebir eşleşmese de gereksiz çekiliş-sırası sapması kaldırıldı |
| N3 | NRBO payda sıfır ya da sıfıra yakın | Önlem yok. `min(max(x, LB), UB)` NaN'ı LB'ye, ±Inf'i sınıra çekiyor | Önlem yok; `np.fmin/np.fmax` aynı eşlemeyi yapıyor | **Yazar kodu izleniyor** (önlem eklemek kaynaktan sapma olur). Ölçüm: ta001 ve ta021'de, seed 2026–2028, tam bütçe; payda hiç 0 olmadı, 10⁻⁶'nın altına da inmedi. NRSR bileşenlerinin %0,16–0,45'i aralıktan büyük (`> 1`) ve sınıra kırpılıyor. Bu, sınırda birikmeye katkı yapan bilinen bir etki (P2-01) |

Testler ([tests/test_nrbo.py](../tests/test_nrbo.py)):
- Her iki paydanın küçük artı ve küçük eksi olduğu dört durum, testin içinde ayrıca yazılmış bir hesapla birebir karşılaştırılıyor (göreli tolerans 10⁻¹²).
- Tam sıfır paydası (0/0) ayrı bir testte sınanıyor.
- Gerçek bir ta021 koşusunda dev adımların oluştuğu ve hiçbirinin sınırlanmadan değerlendirmeye girmediği doğrulanıyor.
