# Method-freeze dry-run · Pilot kanıtı

**Tarih:** 24.11.2026
**Sonuç:** PASS
**Deney SHA:** `df8ac616165dc0105c83429e5ed000f34045aafa`
**Kapsam:** 5 algoritma × 3 Taillard benchmark × 3 seed

Bu paket proje yöneticisinin talebiyle `work/tarik` üzerinde yayımlanan teknik dry-run kanıtıdır. Final deney verisi `results/` politikası uyarınca EXPERIMENT-FREEZE sonrasında ayrı üretilecek. [Pilot kanıt paketi](pilot_evidence.zip)

| Kontrol | Gözlenen |
| --- | --- |
| Manifest | Onaylı commit, temiz başlangıç çalışma ağacı ve beş algoritmanın etkin parametreleri doğrulandı. |
| Ham veri | 15 CSV, 45 koşu. Her CSV’de seed 2026, 2027, 2028. Analiz öncesi ve sonrası SHA-256 eşleşti. |
| FE | ta001: 20.000, ta011: 30.000, ta021: 40.000 FE/koşu. Toplam 1.350.000 FE. |
| Validator | PASS, 15 CSV ve 45 koşu. |
| Test paketi | 84/84 PASS. Hata ve atlama yok. |
| İstatistik | Üç benchmark için tanımlayıcı istatistikler, Wilcoxon sıra toplamı + Holm ve Friedman tabloları. |
| Grafikler | 6 yakınsama, 6 kutu ve 2 koşullu CD dosyası (PDF/PNG). |
| Açık P0/P1/P2 | Yok. |

| Benchmark | Friedman p | Nemenyi/CD |
| --- | ---: | --- |
| ta001 | 0,40600585 | Üretilmedi |
| ta011 | 0,01735127 | Üretildi |
| ta021 | 0,08228404 | Üretilmedi |

Arşiv, ham CSV’leri değiştirilmeden, manifesti, istatistik tablolarını, grafikleri ve ham dosya SHA-256 değerlerini içeren `verification.json` dosyasını barındırır. Paketleme sonrası arşiv içindeki 15 ham CSV hash’i doğrulandı. 450 final koşu için EXPERIMENT-FREEZE kararı bekleniyor.
