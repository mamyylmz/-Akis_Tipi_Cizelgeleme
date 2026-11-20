# Sınır İşleme Pilotu: clip, reflect, random

**20.11.2026 · Burak** · Görev 6 denetimi P2-01'e yanıt ([audit_burak_task6_fix_report.md](../../../results/audit_burak_task6_fix_report.md)).

> **PİLOT. Final bilimsel veri değil.** Final deney 30 seed ile, `experiment-freeze` sürümünden üretilecek ([GIT_WORKFLOW.md](../../GIT_WORKFLOW.md)). Bu veriler yalnızca sınır işleme kararı için kullanılmalı.

## Soru

Adayların sınıra kırpılması (`clip`), random-key anahtarlarının tam 0 ya da 1 değerinde birikmesine ve eşit anahtarlara yol açıyor; eşit anahtarların sırasını iş numarası belirliyor. Başka bir sınır yöntemi bu birikmeyi kaldırır mı, ve bu çözüm kalitesini (RPD) değiştirir mi?

## Tasarım

| Öğe | Değer |
|---|---|
| Algoritmalar | PSO, DE, DBO, NRBO, RIME (`main.py` parametreleriyle) |
| Örnekler ve bütçe | ta001 / 20.000, ta011 / 30.000, ta021 / 40.000 FE (tam ders bütçesi) |
| Seed | 2026–2035 (10); her yöntemde aynı seed'ler, eşleştirilmiş karşılaştırma |
| Koşu sayısı | 5 × 3 × 3 × 10 = **450**, 9 paralel işle 576 s |
| Kod sürümü | `origin/develop` `9ac8f92` + `origin/work/burak` `801004c` + `origin/work/muhammed` `b37a042` (RIME, PR #4) birleşik ağacı |
| Betikler | [tools/boundary_pilot.py](../../../tools/boundary_pilot.py), [tools/boundary_pilot_analyze.py](../../../tools/boundary_pilot_analyze.py) |
| Ham veri | [runs.csv](runs.csv) (SHA-256 `c8a7f6a9267846e4c7d0d2432ebfbe2131bec22823cf62e701cbf6de7fc97b5d`), [run_info.json](run_info.json) |

**Yöntemler:** Üretim kodu değiştirilmedi. Betik algoritma dosyalarının geçici kopyalarında yalnızca *adayı* sınıra geri koyan satırları değiştiriyor (liste betiğin başında). DBO'nun bölge sınırları ve PSO'nun hız sınırı aynen kalıyor.
- **clip:** Sınırı aşan değer sınıra çekilir. Bugünkü davranış.
- **reflect:** Aşan kısım sınırdan içeri yansıtılır (periyot 2·(üst − alt)). Sonlu olmayan değerler clip'e düşer.
- **random:** Aşan bileşen, algoritmanın kendi rastgele sayı üretecinden `U(alt, üst)` ile yeniden atanır. Seed başına tekrarlanabilir.

**Sağlama:** `clip` modu, beş algoritma × üç örnek × iki seed/bütçe (30 durum) için üretim koduyla bit bit aynı: `best_f`, `best_x`, `history`, `n_fes` → [sanity_clip_equals_production.txt](sanity_clip_equals_production.txt). Her koşuda ayrıca FE = bütçe, `best_f` = yeniden hesaplanan Cmax ve değerlendirilen her adayın sonlu ve sınır içinde olduğu doğrulandı.

**İstatistik:** Her algoritma × örnek için yöntemler `clip` ile seed eşleştirmeli Wilcoxon işaretli sıra testiyle (iki yönlü, `zero_method="zsplit"`) karşılaştırıldı, 30 karşılaştırmaya Holm düzeltmesi uygulandı. Ayrıca 15 algoritma × örnek bloğunun ortalama RPD'leri üzerinde Friedman testi yapıldı.

## Sonuçlar

Tam tablolar: [summary.md](summary.md).

1. **Sınırda birikme ve eşitlik tamamen kalkıyor.** clip'te adayların %59–98'inde en az bir eşit anahtar çifti var (DBO %98). reflect ve random'da bu oran %0. Benzersiz permütasyon / FE oranı en çok DBO'da (%39 → %80–84) ve PSO'da (%64 → %87–90) artıyor; DE zaten %100.
2. **Çözüm kalitesinde anlamlı bir fark yok.**
   - Holm düzeltmesinden sonra **0 / 30** karşılaştırma anlamlı.
   - Friedman: χ² = 2,75, **p = 0,25**.
   - Düzeltme öncesi p < 0,05 olan 5 karşılaştırma var ve yönleri karışık:
     - Daha iyi: DBO ta011'de reflect −2,19 ve random −2,21 puan; PSO ta011'de random −1,45 puan.
     - Daha kötü: DE ta011'de random +1,09 puan; DE ta021'de random +0,77 puan.
   - Ortalama sıra: random 1,70, reflect 2,00, clip 2,30. Fark anlamlı değil.
3. **ta001'deki 1297 takılması sınır yönteminden bağımsız.** Koşuların 1297'de bittiği oran: clip %88, reflect %84, random %92. Daha önce (18.11 inceleme notları) bunu eşit anahtarlara bağlamıştım; **bu varsayım desteklenmedi.** 1297, ta001 arama uzayında beş algoritmanın da güçlü biçimde yakalandığı bir yerel optimum. 1297'nin altına inen 6 koşunun 5'i reflect ile (DBO bir kez BKS = 1278'e ulaştı), ama n = 10 ile bu bir eğilimden öte değil.

## Değerlendirme ve öneri

- **Öneri: `clip` korunsun.**
  - Ders şablonunun kuralı açık: `pso.py` başlığı, kural 5, "`x = np.clip(x, lb, ub)`".
  - Bu pilotta alternatiflerin çözüm kalitesine anlamlı bir katkısı görülmedi.
  - Değişiklik beş algoritmanın hepsine dokunur ve 23 Kasım entegrasyon kapısını riske atar.
- **Makale için (H2):** Sınırda birikme ve eşit anahtar oranı, gösterimin bir özelliği olarak raporlanmaya değer. Final deneyde `best_x`'teki sınır oranı ham CSV'den hesaplanabilir. Bu pilotun sınırlı gücü (n = 10, tek pilot) nedeniyle "sınır yöntemi performansı etkilemez" diye genelleme yapılmamalı. Doğru ifade: "bu pilotta anlamlı bir fark gözlenmedi".
- **Yan bulgu:** Algoritmalar arası fark, sınır yönteminden çok daha büyük. ta011'de clip ile ortalama RPD: RIME %2,5 ve DE %2,9; DBO %5,9 ve NRBO %6,5. Final deneyin algoritmaları ayırt edebileceğine işaret ediyor; final iddia için 30 seed'li veri beklenmeli.

## Karar

Sınır işleme kararı Şeref ve Burak'ındır (Görev 6, P2-01). Bu pilot, kararın girdisidir.
