# PSO pilot / pre-freeze durum kaydı

## Mevcut kanıt

Repoda `results/raw/ta001/PSO.csv`, `ta011/PSO.csv` ve `ta021/PSO.csv` altında 30'ar tam bütçeli PSO koşusu bulunmaktadır. Bu dosyalar beş algoritmanın experiment-freeze commit'inden **önce** üretilmiştir.

Bu nedenle bu sprintte şu sınıflandırma uygulanır:

- PSO'nun gerçek PFSP modeliyle çalıştığını gösterir: **EVET**.
- Seed, maxFEs, ham çıktı ve analiz pipeline'ı için entegrasyon kanıtıdır: **EVET**.
- Beş algoritmanın nihai bilimsel karşılaştırmasında doğrudan kullanılabilir: **HAYIR**.

Örnek mevcut kayıt:
- ta001 run=1, seed=2026, n_fes=20.000, best_f=1297.
- ta011 run=1, seed=2026, n_fes=30.000, best_f=1625.
- ta021 run=1, seed=2026, n_fes=40.000, best_f=2358.

Bu sayılar yalnız mevcut dosyaların okunabildiğini ve pipeline'ın tam FE kullandığını göstermek için kaydedilmiştir; algoritma üstünlüğü iddiası değildir.

## Nihai karar

RIME dahil 5/5 algoritma kabul edilip experiment-freeze oluşturulduktan sonra PSO da diğer dört algoritmayla **aynı freeze commit'ten, aynı seed listesiyle yeniden çalıştırılacaktır**. Pre-freeze sonuçlar final tablolarına karıştırılmayacaktır.
