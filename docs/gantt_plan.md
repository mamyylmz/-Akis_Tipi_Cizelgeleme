# 5×3 PFSP Örneği İçin Doğrulanmış Gantt Verisi ve Çizim Planı

**Sürüm 1.0 · 18.11.2026 · Durum: VERİ VE Cmax DOĞRULANDI**

Kaynak, ders sorumlusunun `Problem7_Akis_Tipi_Cizelgeleme.docx` belgesindeki doğrulama örneğidir. İşlem süreleri satırlar J1–J5, sütunlar M1–M3 olacak biçimde aşağıdadır. Kaynakta zaman birimi özel olarak adlandırılmadığı için tabloda **zaman birimi** ifadesi kullanılır.

| İş | M1 | M2 | M3 |
| --- | ---: | ---: | ---: |
| J1 | 3 | 4 | 2 |
| J2 | 2 | 3 | 4 |
| J3 | 4 | 1 | 3 |
| J4 | 1 | 4 | 2 |
| J5 | 3 | 2 | 3 |

Doğrulama permütasyonu: **(J4, J2, J1, J5, J3)**.

Kullanılan bağıntılar:

`S[i,j] = max(C[i-1,j], C[i,j-1])`

`C[i,j] = S[i,j] + p[pi[i],j]`

Sıfırıncı iş sırası ve sıfırıncı makine için sınır tamamlanma değerleri 0 kabul edilmiştir.

## Bağımsız hesaplanan 15 işlem

| Sıra | İş | Makine | İşlem süresi | Başlangıç | Bitiş |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | J4 | M1 | 1 | 0 | 1 |
| 1 | J4 | M2 | 4 | 1 | 5 |
| 1 | J4 | M3 | 2 | 5 | 7 |
| 2 | J2 | M1 | 2 | 1 | 3 |
| 2 | J2 | M2 | 3 | 5 | 8 |
| 2 | J2 | M3 | 4 | 8 | 12 |
| 3 | J1 | M1 | 3 | 3 | 6 |
| 3 | J1 | M2 | 4 | 8 | 12 |
| 3 | J1 | M3 | 2 | 12 | 14 |
| 4 | J5 | M1 | 3 | 6 | 9 |
| 4 | J5 | M2 | 2 | 12 | 14 |
| 4 | J5 | M3 | 3 | 14 | 17 |
| 5 | J3 | M1 | 4 | 9 | 13 |
| 5 | J3 | M2 | 1 | 14 | 15 |
| 5 | J3 | M3 | 3 | 17 | 20 |

Tamamlanma matrisi:

| İş sırası | M1 C | M2 C | M3 C |
| --- | ---: | ---: | ---: |
| J4 | 1 | 5 | 7 |
| J2 | 3 | 8 | 12 |
| J1 | 6 | 12 | 14 |
| J5 | 9 | 14 | 17 |
| J3 | 13 | 15 | **20** |

Son hücre `C[5,3] = 20` olduğundan **Cmax = 20** elde edilmiştir. Bu değer ders belgesindeki beklenen doğrulama sonucu ile aynıdır.

## Kontrol kriterleri ve sonuç

- Her makinede 5 işlem var: **PASS**.
- Her iş üç makinede birer kez işleniyor: **PASS**.
- Aynı makinedeki işlemler çakışmıyor: **PASS**.
- Her iş M1 → M2 → M3 sırasını koruyor: **PASS**.
- Tüm makinelerde ortak iş permütasyonu J4 → J2 → J1 → J5 → J3: **PASS**.
- Son işlemin son makinedeki bitişi 20: **PASS**.

## Makale görseli üretim kuralı

Makaledeki Gantt şekli bu tablodaki başlangıç/bitiş değerlerinden betikle üretilmelidir. Yatay eksen zaman, dikey şeritler M1–M3 olmalıdır. Her çubuğun başlangıcı `Başlangıç`, genişliği `Bitiş-Başlangıç` olmalı; iş etiketi çubuk üzerinde gösterilmelidir. Sağ uçta Cmax=20 işaretlenir. Excel veya elle değiştirilmiş zaman değerleri kullanılmaz.

Bu küçük örneğin doğrulanması **Bilal'in K9 görselleştirme hazırlığı için tamamlanmıştır**. Büyük Taillard örneklerinin nihai Gantt/çözüm görselleştirmesi, gerçek `results/` çıktıları oluştuğunda ayrıca üretilecektir.
