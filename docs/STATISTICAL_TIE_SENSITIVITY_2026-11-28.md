# Ek istatistiksel duyarlılık incelemesi — 28.11.2026

**Nitelik:** Keşifsel / rapora ek. Bu analiz, final ham verilerini, orijinal analizleri, p-değerlerini, deney protokolünü veya nihai makale sayısal bloklarını değiştirmez.

## Motivasyon

Ders protokolü iki taraflı `scipy.stats.ranksums` + Holm kullanır. Bu test bağları (eşit Cmax değerlerini) özel olarak düzeltmez. 20 işli PFSP'nin ayrık makespan değerlerinde, özellikle ta001'de, çok sayıda bağ bulunur. Bağlara ortalama sıra ve varyans düzeltmesi uygulayan bağımsız örneklem Mann–Whitney U normal yaklaşımı bu varsayımın duyarlılığını görünür kılar.

## Yeniden hesaplama

`python tools/exploratory_tie_sensitivity.py` ham `results/raw` CSV'lerinden Cmax okuyup şu adımları uygular: pooled average ranks; U = rank_sum_x - n(n+1)/2; tie-adjusted variance = nm/12 * [(N+1) - sum(t³-t)/(N(N-1))]; z = (U-nm/2)/sqrt(var); p = erfc(|z|/sqrt(2)); referansa karşı 4 p-değerine Holm düzeltmesi. Süreklilik düzeltmesi **uygulanmaz**. NASE metnindeki referans seçme kuralı aynen kullanılır: en küçük gözlenen medyan, eşitlikte alfabetik ad.

| Örnek | Referans | Karşılaştırma | Tie-aware p (yaklaşık) | Holm p (yaklaşık) |
| --- | --- | --- | ---: | ---: |
| ta001 | DBO | DBO–DE | 0.003541 | **0.014164** |
| ta001 | DBO | DBO–NRBO | 0.377269 | 0.410711 |
| ta001 | DBO | DBO–PSO | 0.205355 | 0.410711 |
| ta001 | DBO | DBO–RIME | 0.019251 | 0.057753 |
| ta011 | RIME | RIME–DBO | 9.52e-9 | 2.86e-8 |
| ta011 | RIME | RIME–DE | 0.009285 | 0.011739 |
| ta011 | RIME | RIME–NRBO | 2.19e-9 | 8.74e-9 |
| ta011 | RIME | RIME–PSO | 0.005870 | 0.011739 |
| ta021 | DE | DE–DBO | 4.96e-9 | 1.49e-8 |
| ta021 | DE | DE–NRBO | 4.25e-11 | 1.70e-10 |
| ta021 | DE | DE–PSO | 0.001546 | 0.003092 |
| ta021 | DE | DE–RIME | 0.976393 | 0.976393 |

## Yorum ve sınırlar

1. **ta001 duyarlı:** Mevcut bağ düzeltmesiz `ranksums` + Holm tablosu DBO–DE için düzeltilmiş p=0.34 bildirirken bu alternatif tie-aware yaklaşım p≈0.0142 bulur. Bu, eşitliklerin çokluğu nedeniyle istatistiksel yöntem seçiminin sonuç yorumunu etkilediğinin kanıtıdır; aynı hipotez için farklı tekniklerin sonuçları otomatik birbirinin yerine konamaz. Veri veya eski p-değeri “yanlış” diye sessizce değiştirilmez.
2. **ta011:** RIME karşılaştırmalarının dördü de bu keşifsel yöntemde Holm eşiğini geçer. **ta021:** DE–RIME ayrımı gözlenmez; DE–PSO keşifsel karşılaştırmasında fark vardır. Tek veri üzerinde çok analiz arasından en avantajlı p-değerini seçmek bilimsel olarak uygun değildir.
3. Referans **veriden seçilmektedir**; bir referansa karşı 4 Holm karşılaştırması, referans seçimi nedeniyle tam ön-belirlenmiş confirmatory aile kabulünü otomatik sağlamaz.
4. `ranksums` ve Mann–Whitney bağımsız örneklem yaklaşımı, aynı sayısal seed'leri algoritmalara vermenin neden olduğu ortak rassal etkiyi kanıtlamaz. Alternatif eşleştirilmiş test ancak deney tasarımına uygun pairing varsayımıyla düşünülebilir.
5. `p<0.05` mutlak performans büyüklüğünü, optimallik ispatını veya algoritma evrensel üstünlüğünü ifade etmez. Çoklu benchmark sayısı ve etki büyüklükleri ayrı sınırlamalardır.
6. Kod basit iki taraflı **asemptotik normal yaklaşımı** kullanır; küçük/bağ yoğun örneklerde kesin permütasyon testiyle eşdeğer değildir. Süreklilik düzeltmesi alternatifleri ve güven aralıkları ek robustness araştırması olarak düşünülebilir.

**Karar:** Analizi `tools/exploratory_tie_sensitivity.py` ile tekrar üretilebilir, mevcut deneylerden ayrıştırılmış bir hassasiyet eki olarak sakla. Nihai makalede hangi test ailesinin önceden belirlenmiş olduğu ve bağ/selection sınırlaması açık kalmalı. Yöntem değişikliği için bilimsel danışman onayı gerekir; kodu/CSV'yi sonradan değiştirip önceki testlerin sonucuymuş gibi sunma.
