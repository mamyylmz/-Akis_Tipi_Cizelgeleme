# Bağımsız Teknik İnceleme: Muhammed'in RIME'ı (PR #4)

**20.11.2026 · İnceleyen: Burak (yöntem/kaynak/kod uyumu ve entegrasyon)** · İncelenen: Muhammed · Kapsam: PR #4 açıklamasındaki "Burak: yöntem/kaynak/kod uyumu" ve Görev 6 denetimindeki P0-02'nin Burak'a düşen entegrasyon kısmı.

**İncelenen sürüm:** `origin/work/muhammed` = `b37a042`. `src/algorithms/rime.py` SHA-256: `6a23cbbeb2c80a9b0225e89fdb068b9a12f5a89faa00074682c2bcf294272e14`.

> Not: `src/algorithms/rime.py`, `tests/test_rime.py` ve `paper/method_rime.md` bu dalda değil, PR #4'te. Aşağıdaki araç ([tools/review_independent_rime_check.py](../tools/review_independent_rime_check.py)) RIME'ı içe aktardığı için ancak PR #4 birleştirildikten sonra bu dalda çalışır. Çıktısı, aşağıdaki birleşik ağaçta üretildi.

## 1. Kaynak

- **Makale:** Su, H., Zhao, D., Heidari, A. A., Liu, L., Zhang, X., Mafarja, M., & Chen, H. (2023). RIME: A physics-based optimization. *Neurocomputing, 532*, 183–214. https://doi.org/10.1016/j.neucom.2023.02.010. 2022+ hakemli yayın koşulunu karşılıyor. Yayıncı tam metnini açmadım.
- **Yazar kodu:** Makalenin ortak yazarı A. A. Heidari'nin GitHub deposundan alındı: `aliasgharheidaricom/RIME-A-physics-based-optimization`, 11.02.2023'te açılmış. `RIME.m` başlığı: "Last update: Feb 11 2023". Bağımsız bir kopya (`VG-TechCenter/Rime-optimization-algorithm`) yalnızca başlık yorumu ve fonksiyon adında ayrılıyor. Referans kopya: [30_rime_author_matlab_reference.m](test_logs/30_rime_author_matlab_reference.m). `main.m` varsayılanı N = 30.

## 2. Satır satır karşılaştırma (`RIME.m` ↔ `rime.py`)

| Öğe | RIME.m | rime.py | Sonuç |
|---|---|---|---|
| Başlatma | `rand(N,dim).*(ub-lb)+lb` | `lb + rng.random((n, dim)) * (ub - lb)` | Aynı |
| `RimeFactor` | `(rand-0.5)*2*cos(pi*it/(Max_iter/10))*(1-round(it*W/Max_iter)/W)`, iterasyon başına bir çekiliş | Aynı; `round`, MATLAB gibi yarımları yukarı yuvarlıyor | Aynı |
| `E` | `sqrt(it/Max_iter)` | `sqrt(iteration/max_iter)` | Aynı |
| `normr` | Satır vektörü normalizasyonu | `rates / ||rates||` | Aynı (sıfır norm koruması PFSP'de erişilemez, Cmax > 0) |
| Yumuşak buz (Denk. 3) | `r1 < E` ise `Best + RimeFactor*((Ub-Lb)*rand + Lb)` | Aynı, çekiliş sırası aynı | Aynı |
| Sert buz (Denk. 7) | `r2 < normalized(i)` ise `Best` | Aynı | Aynı |
| En iyi çözüm aday üretimi boyunca | Sabit, yalnızca seçimde güncelleniyor | `best_x`, değerlendirme yardımcısında güncelleniyor. Yeni değer en iyiden iyiyse ajanın değerinden de iyi olduğu için bu, MATLAB'daki iç içe koşulla aynı | Aynı |
| Sınır emilimi | Sınır dışı değer sınıra | `np.clip` | Aynı |
| Seçim | Sıkı `<` | Sıkı `<` | Aynı |
| W | 5 | 5 | Aynı |

**FE uyarlaması:** `Max_iter = ceil((max_fes − N)/N)`; son tur bütçe bitince kesiliyor. `cos(π·it/(Max_iter/10))` terimi iterasyon indeksine bağlı periyodik bir terim olduğu için iterasyon indeksini korumak yazar koduna `fes/max_fes`'ten daha yakın. Makul ve belgelenmiş.

## 3. Bağımsız olarak yeniden yaptığım kontroller

Birleşik ağaç: `origin/develop` (`9ac8f92`) + `origin/work/burak` (`6d0b59f`, PR #6) + `origin/work/muhammed` (`b37a042`, PR #4). Çakışma yok. Tam çıktı: [31_burak_rime_review_merged_tree.txt](test_logs/31_burak_rime_review_merged_tree.txt).

| Kontrol | Beklenen | Gözlenen | Sonuç |
|---|---|---|---|
| Bağımsız yeniden yazım: yalnızca `RIME.m`'den yazdığım sürüm `rime.py` ile karşılaştırıldı. 3 örnek × seed 2026/2027/2055 × FE {tam bütçe, 1001, 137} | `best_f`, `best_x`, `n_fes` birebir aynı | **27/27 aynı** | PASS |
| Tam test paketi | 0 hata, 0 atlama | **59 test OK, 0 atlama**. Tarık'ın Görev 6 paketindeki RIME FE/seed ve 5/5 kayıt testleri artık çalışıyor ve geçiyor | PASS |
| `main.py --check` | 5/5 TAMAM, uyarı yok | PSO, DE, DBO, NRBO, RIME TAMAM; "5 algoritma" uyarısı yok | PASS |

Bağımsız yeniden yazımda FE eşlemesini (`Max_iter = ceil((max_fes − N)/N)`) bilerek Muhammed'inkiyle aynı seçtim. Bu yüzden karşılaştırma mekanizmanın ve çekiliş sırasının doğruluğunu kanıtlıyor, eşleme kararının kendisini değil (o karar §2'de değerlendirildi).

## 4. Bulgular

**P0 ve P1 bulgum yok.**

```
ID: PFSP-RIME-01
Seviye: P2
Sorumlu: Burak (ortak arayüz belgesi)     İnceleyen: —
Dosya: docs/algorithm_interface.md §3.4
Gözlenen: §3.4 yalnızca t/T → fes/max_fes kuralını tanımlıyor. RIME, yazar koduna daha
  yakın olduğu için iterasyon indeksi eşlemesini kullanıyor. İkisi de geçerli, ama belge
  yalnızca birini anlatıyor.
İstenen: §3.4'e "iterasyon indeksi eşlemesi, belgelenmek koşuluyla kabul" maddesi eklensin.
Durum: DÜZELTİLDİ (bu dalda, §3.4)
```

```
ID: PFSP-RIME-02
Seviye: P2 (bilgi)
Sorumlu: Muhammed
Dosya: src/algorithms/rime.py:79
Gözlenen: max_fes < pop_size ise popülasyon max_fes'e küçülüyor. Bu, DE ile aynı davranış
  ve kodda yorum olarak belgelenmiş. Ders bütçelerinde etkisi yok.
İstenen: yok; yalnızca makalenin parametre tablosunda N = 30'un sabit olduğu yazılsın.
Durum: BİLGİ
```

**Gözlem (bulgu değil):** ta001'de tam bütçeyle üç seed'in üçünde de RIME 1297'de bitti. DE, PSO, DBO ve NRBO'da da görülen bu durum, P2-01 sınırda birikme ve eşit anahtar konusuyla ilgili; RIME'a özgü bir hata değil.

## 5. Karar

- **RIME yöntem/kaynak/kod uyumu (Burak): KABUL.**
- **Entegrasyon (`main.py`'deki 5/5 kayıt): KABUL.** Birleşik ağaçta 59/59 test ve `--check` 5/5.
- PR #4'ün birleştirilmesi için Tarık'ın seed/FE/sınır/`best_f`/`history` ve 5/5 kayıt teyidi de gerekiyor (PR #4 açıklaması). Görev 6'daki P0-02, Tarık'ın teyidi ve PR #4'ün birleştirilmesiyle kapanır.
- **Birleştirme sırası önerisi:** PR #6 (`work/burak`) ve PR #4 (`work/muhammed`) çakışmıyor; hangisi önce girerse girsin, diğeri de temiz birleşir. Windows makinelerinde testlerin geçmesi için PR #6'daki `.gitattributes` gerekiyor.
