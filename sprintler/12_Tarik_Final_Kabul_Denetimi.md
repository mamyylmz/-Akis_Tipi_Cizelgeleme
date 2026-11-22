# Tarık — Birleşik Final Kabul Denetimi

**Durum:** ZORUNLU SON KONTROL  
**Branch:** `work/tarik`  
**Amaç:** Muhammed'in vekil teknik ön-denetiminden bağımsız olarak, 20–22 Kasım arasında yapılan bütün blocker/RIME/deney-altyapısı değişikliklerini yeniden test etmek; hata varsa düzeltmek ve aynı kapıyı yeniden çalıştırmak.

> Bu görev tamamlanıp P0=0 ve P1=0 kanıtı verilmeden PR #5 kabul edilmiş sayılmaz.

## 1. Başlangıç ve sürüm kanıtı

Temiz bir çalışma dizininde:

```bash
git fetch origin
git switch work/tarik
git pull --ff-only origin work/tarik
git status --short
git rev-parse HEAD
```

- `git status --short` boş olmalı.
- Başlangıç SHA'sını final raporuna yaz.
- Eski local dosya/sonuçlarla test yapma.

## 2. Okunacak güncel belgeler

- `docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md`
- `docs/GIT_WORKFLOW.md`
- `docs/algorithm_interface.md`
- `docs/experiment_protocol.md`
- `docs/review_muhammed_proxy_2026-11-22.md`
- `paper/method_dbo_nrbo.md`
- `paper/method_rime.md`
- `sprintler/11_Tarik_Test_Istatistik_Teslim_Kaniti.md`

## 3. Windows veri bütünlüğü

Mümkünse gerçek Windows makinesinde, aksi halde GitHub Actions Windows job kanıtını ayrıca kontrol ederek:

```bash
git config core.autocrlf true
git ls-files --eol -- data/taillard
python -m unittest tests.test_model_validation -v
python src/problem.py
```

Beklenen:
- ta001/ta011/ta021 working-tree LF,
- hash 3/3,
- 1278 / 1582 / 2297 PASS,
- CRLF workaround veya hash gevşetmesi yok.

## 4. DBO / NRBO regresyonu

```bash
python -m unittest tests.test_audit_burak_task6 -v
python -m unittest tests.test_nrbo -v
python -m unittest tests.test_dbo -v
```

Özellikle kontrol et:
- DBO θ=45/90/180 fixture,
- DBO FE tabanlı R uyarlaması belgeli,
- NRBO a1/a2 çekiliş sırası boyut başına a1 sonra a2,
- NRBO 0, küçük pozitif ve küçük negatif payda senaryoları,
- NaN/Inf/sınır dışı aday evaluate'a ulaşmıyor,
- exact FE ve determinism korunuyor.

Kaynakla çelişki görürsen PASS verme; kod + test + yöntem notunu birlikte düzelt.

## 5. RIME son bağımsız kontrol

```bash
python -m unittest tests.test_rime -v
python tools/review_independent_rime_check.py
```

Kontrol:
- same-seed best_x/best_f/history birebir,
- seed `default_rng(seed)` kaynağına gerçekten gidiyor,
- 1/7/29/30/31/73/121/137/1001 ve tam ta001 bütçesi exact,
- bounds/finite,
- best_f bağımsız re-evaluation,
- geçerli permutation,
- monoton history,
- yazar RIME.m karşılaştırması.

Farklı seed'in mutlaka farklı final best_x üretmesini şart koşma; bu doğru bir correctness invariant değildir.

## 6. Beş algoritmanın ortak contract kapısı

```bash
python -m unittest tests.test_contract -v
python src/main.py --check
```

Beklenen registry:
- PSO
- DE
- DBO
- RIME
- NRBO

Her biri:
- exact FE,
- same-seed reproducibility,
- seed propagation,
- bounds,
- best_x/best_f,
- permutation,
- history
PASS olmalı.

## 7. Dört P1 düzeltmesinin regresyonu

```bash
python -m unittest tests.test_experiment_manifest -v
python -m unittest tests.test_experiment_validation -v
```

Doğrula:
1. `experiment_manifest.json` runner tarafından otomatik üretiliyor.
2. Final 30-run modunda temiz Git + 40 karakter commit SHA zorunlu.
3. Farklı seed'in farklı final çözüm vermesi zorunluluğu yok; seed aktarımı test ediliyor.
4. `feasible` strict parse ediliyor; `"False"` true sayılamıyor.
5. objective/cmax/best_f yeniden hesapla aynı.
6. RPD yeniden hesapla aynı.
7. kaydedilmiş 1-based permutation decode(best_x)+1 ile aynı.
8. violation = 0.

Test fixture'ını kolaylaştırarak PASS üretme.

## 8. Gerçek 5×3×1 entegrasyon smoke

Bu işlem final bilimsel veri değildir.

Temiz/geçici clone içinde çalıştır:

```bash
python -c "import sys; sys.path.insert(0, 'src'); import main; p=main.run_checks(); main.run_experiments(p, 1)"
python tools/check_experiment_outputs.py --runs 1 --seed-base 2026
```

Beklenen:
- 15 CSV,
- 15 gerçek koşu,
- 5 algoritma × 3 benchmark,
- exact maxFEs,
- validator PASS,
- `results/tables/experiment_manifest.json` mevcut,
- pilot manifestte commit/environment/algoritma/parametre bilgileri mevcut.

Bu çıktıları final 450-run verisi olarak commit etme.

## 9. Tam test paketi

```bash
python -m unittest discover -s tests -v
python src/problem.py
python src/main.py --check
```

Ayrıca PR #5'in en güncel GitHub Actions koşusunda hem Ubuntu hem Windows job'ı PASS olmalı.

## 10. Hata bulunursa

- Testi silme/gevşetme.
- Seed/maxFEs/reference değiştirme.
- CSV'yi elle düzeltme.
- Önce root cause yaz.
- Regression testi ekle veya mevcut testle göster.
- Üretim kodu/belgeyi düzelt.
- İlgili dar testi çalıştır.
- Ardından **9. bölümdeki tam kapıyı baştan çalıştır**.
- Değişiklik yaptıysan yeni SHA'yı final raporunda belirt.

## 11. Final raporu

PR #5 konuşmasına şu formatta yaz:

```text
Tarık Final Kabul Denetimi
Başlangıç SHA:
Final SHA:
Ortam:
Windows/LF: PASS/FAIL
DBO/NRBO: PASS/FAIL
RIME: PASS/FAIL
5/5 contract: PASS/FAIL
Manifest: PASS/FAIL
CSV validator regresyonları: PASS/FAIL
5×3×1 real smoke: PASS/FAIL
Full unittest: <N> test, <fail/error/skip>
problem.py: PASS/FAIL
main.py --check: PASS/FAIL
P0:
P1:
P2:
Düzeltilen hatalar:
Nihai karar: KABUL / DÜZELTME_GEREKİYOR / BLOKE
```

**KABUL koşulu:** P0=0, P1=0 ve yukarıdaki zorunlu kapıların tamamı PASS.

Tarık'ın bu final raporu KABUL ise, 20–22 Kasım entegrasyon değişikliklerini ekip kontrol kapısından geçmiş kabul edeceğiz.
