# 3.3.1. Diferansiyel Evrim (DE)

**Durum:** Makaleye aktarılabilir yöntem metni · 23.11.2026  
**Uygulama:** `src/algorithms/de.py`  
**Varyant:** DE/rand/1/bin

## Kaynak ve amaç

Diferansiyel Evrim, Storn ve Price tarafından sürekli uzayda global optimizasyon için geliştirilen popülasyon tabanlı bir yöntemdir. Bu çalışmada özgün çalışmadaki **DE/rand/1/bin** varyantı kullanılmıştır.

Birincil kaynak: R. Storn ve K. Price, “Differential Evolution – A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces,” *Journal of Global Optimization*, 11, 341–359, 1997. DOI: `10.1023/A:1008202821328`.

## Başlatma

PFSP'deki her aday random-key vektörü olarak tutulur:

[
x_i=(x_{i1},...,x_{iD}),\qquad x_{ij}\in[0,1].
]

Başlangıç popülasyonu `np.random.default_rng(seed)` ile bağımsız uniform dağılımdan üretilir. Problem boyutu üç zorunlu benchmarkta da `D=20` olduğundan varsayılan popülasyon büyüklüğü `NP=5D=100`dür. Kaynak çalışma NP için yaklaşık `3D–10D` aralığını pratik bir başlangıç kuralı olarak verir; proje `5D` seçimini deney öncesinde sabitler.

## Mutasyon

Her hedef vektör `x_i,G` için, hedef indeksinden ve birbirinden farklı üç indeks `r1,r2,r3` seçilir:

[
v_{i,G+1}=x_{r1,G}+F(x_{r2,G}-x_{r3,G}).
]

Projede `F=0.5` kullanılır. Mutant vektör `[0,1]^D` sınırına kırpılır.

## Binom çaprazlama

Her boyut için mutant bileşenin seçilme olasılığı `CR`'dir. En az bir mutant bileşenin aktarılmasını garanti etmek için rastgele `j_rand` boyutu zorunlu seçilir:

[
u_{ij,G+1}=
\begin{cases}
v_{ij,G+1}, & rand_j\le CR\ \text{veya}\ j=j_{rand},\\
x_{ij,G}, & \text{aksi halde}.
\end{cases}
]

Projede `CR=0.9` kullanılır.

## Seçim ve nesil semantiği

Deneme vektörü hedef vektörden daha iyi veya eşit amaç değerine sahipse bir sonraki nesle geçer:

[
x_{i,G+1}=
\begin{cases}
u_{i,G+1}, & f(u_{i,G+1})\le f(x_{i,G}),\\
x_{i,G}, & \text{aksi halde}.
\end{cases}
]

Uygulama **generational** DE'dir: mutasyon ve çaprazlama sırasında bütün ebeveyn okumaları `X_gen` adlı değişmez G neslinden yapılır. Böylece bir hedefin güncellenmesi aynı nesildeki sonraki hedeflerin mutant üretimini etkilemez.

## PFSP uyarlaması ve FE bütçesi

DE sürekli vektör üzerinde çalışır; amaç fonksiyonu çağrısında ortak random-key çözümleyicisi kararlı `argsort` ile iş permütasyonunu üretir. Mutasyon sonrası sınır dışı değerler `[0,1]` aralığına kırpılır.

Başlangıç popülasyonundaki değerlendirmeler dahil her `problem.evaluate()` çağrısı bir FE olarak sayılır. Ana deneylerde bütçe örneğe göre 20.000 / 30.000 / 40.000 FE'dir. Bütçe bir neslin ortasında sona ererse o ana kadar tamamlanan seçimler korunur ve `n_fes == max_fes` koşulu sağlanır.

## Deney parametreleri

| Parametre | Değer | Gerekçe |
|---|---:|---|
| Varyant | DE/rand/1/bin | Storn & Price (1997) |
| NP | 100 | D=20 için 5D; kaynakta verilen 3D–10D pratik aralığının içinde |
| F | 0.5 | kaynak çalışmadaki başlangıç önerilerinden biri |
| CR | 0.9 | hızlı yakınsama için kaynak çalışmada önerilen yüksek CR denemelerinden biri |
| Seed | 2026–2055 | ortak deney protokolü |
| Sınır | [0,1] | random-key çözüm uzayı |

Bu parametreler Taillard sonuçlarına bakılarak sonradan ayarlanmamıştır; final experiment-freeze sonrasında değiştirilemez.
