# Nihai deney protokolü

**Sorumlu:** Tarık — test, deney ve istatistik  
**Kapsam:** DE, PSO, DBO, RIME, NRBO × ta001, ta011, ta021  
**Durum:** Deney başlamadan önce uygulanacak değişmez sözleşme.

## 1. Deney matrisi

| Instance | Boyut | maxFEs | Koşu/algoritma |
|---|---:|---:|---:|
| ta001 | 20×5 | 20.000 | 30 |
| ta011 | 20×10 | 30.000 | 30 |
| ta021 | 20×20 | 40.000 | 30 |

Toplam: 5 × 3 × 30 = **450 bağımsız koşu**, toplam **13.500.000 FE**.

## 2. Seed politikası

- `SEED_BASE = 2026`.
- Koşu k için seed = `2026 + k`, k=0..29.
- Aynı instance ve run numarasında beş algoritma aynı seed'i kullanır.
- Rastgelelik yalnız `np.random.default_rng(seed)` üzerinden üretilir.
- Seed listesi final sonuçlarla birlikte saklanır.

## 3. Deney öncesi freeze kapısı

Final deneyler yalnız aşağıdaki koşullar sağlandıktan sonra başlar:

1. `ALGORITHMS` tam olarak PSO, DE, DBO, RIME, NRBO içerir.
2. `python -m unittest discover -s tests -v` PASS.
3. `python src/main.py --check` PASS.
4. ta001/ta011/ta021 veri hash kontrolleri PASS.
5. P0/P1 açık değildir.
6. Deney commit SHA'sı `experiment-freeze` olarak kaydedilir.

Freeze sonrasında algoritma/model/veri değişirse daha önce üretilen ilgili final koşular geçersizdir ve yeniden çalıştırılır.

## 4. Ham çıktı sözleşmesi

`results/raw/<instance>/<ALGORITHM>.csv` dosyasında her satır bir koşudur. Zorunlu alanlar:

- `run`
- `seed`
- `best_f`
- `objective`
- `cmax`
- `rpd`
- `violation`
- `feasible`
- `permutation`
- `n_fes`
- `time`
- `best_x`
- `history_fes`
- `history_f`

Kod sürümü CSV satırına gömülmek yerine deney manifestinde tekil olarak tutulur; böylece 450 satırın tamamının aynı freeze commit'ten üretildiği doğrulanır.

## 5. Deney manifesti

Final koşu başlamadan önce `results/tables/experiment_manifest.json` oluşturulur:

```json
{
  "experiment_commit": "<40-char git SHA>",
  "n_runs": 30,
  "seed_base": 2026,
  "instances": ["ta001", "ta011", "ta021"],
  "max_fes": {"ta001": 20000, "ta011": 30000, "ta021": 40000},
  "algorithms": ["PSO", "DE", "DBO", "RIME", "NRBO"],
  "environment": {
    "os": "<exact>",
    "python": "<exact>",
    "numpy": "<exact>",
    "scipy": "<exact>",
    "pandas": "<exact>"
  }
}
```

## 6. Koşu başına kabul kriterleri

Her satır için:

- seed beklenen seed ile aynı,
- `n_fes == MAX_FES[instance]`,
- `feasible == True`,
- `best_f` sonlu,
- `best_x` boyutu n,
- bütün anahtarlar [0,1] içinde,
- decode tam bir 0..n-1 permütasyonu,
- `problem.evaluate(best_x) == best_f`,
- `history_fes[-1] == n_fes`,
- history FE değerleri artan,
- history best değerleri artmayan.

Bir satır başarısızsa o koşu final veri setine alınmaz; hata çözülür ve aynı seed tekrar çalıştırılır. Başarısız satır elle düzeltilmez.

## 7. Pilot ve final sonuç ayrımı

- 1–3 koşuluk smoke/pilot sonuçları yalnız entegrasyon kanıtıdır.
- Mevcut pre-freeze PSO 30-run dosyaları **final bilimsel veri olarak kullanılmaz**.
- Final sonuçlar yalnız experiment-freeze commit'inden beş algoritma birlikte çalıştırılarak üretilir.
- Eski sonuçlar silinmek yerine gerekiyorsa `results/archive/pre_freeze/` altında açıkça etiketlenir.

## 8. İstatistiksel analiz

Her instance için:
- best, worst, mean, median, sample std,
- feasible rate,
- average runtime,
- Cmax ve RPD,
- box plot,
- ortak FE ekseninde convergence plot.

İkili karşılaştırma: ders paketindeki `scipy.stats.ranksums` tabanlı **Wilcoxon rank-sum / Mann–Whitney eşdeğeri** + Holm, alpha=0.05.

Beşli karşılaştırma: Friedman; anlamlıysa Nemenyi kritik fark diyagramı.

Aynı seed kullanımı Friedman bloklarını tanımlar; bu durum rank-sum testini paired teste dönüştürmez. Ders paketindeki protokol değiştirilmez.

## 9. Hata toleransı ve yasaklar

- FE aşımı/eksikliği toleransı: 0.
- NaN/Inf toleransı: 0.
- Geçersiz permütasyon toleransı: 0.
- Eksik koşu toleransı: 0.
- CSV veya p-değerleri elle düzenlenmez.
- Testi geçsin diye test/seed/maxFEs değiştirilmez.
- Bir algoritma düzeltilirse eski sonuçları korunup finalde kullanılmaz.
