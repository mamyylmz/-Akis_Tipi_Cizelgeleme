# 18 Kasım 2026 — Bağımsız Paket Kontrolü

Bu dosya, Bilal'in revize paketinin proje yöneticisinin talebiyle yapılan son kalite kontrolünün kısa özetidir.

## Değiştirilmeyen test

`docs/check_literature.py` dosyası **değiştirilmedi**. Başlangıç SHA-256:

`dc3f5d92deb3ca27c5acfc75e7b45644764ba61818d425288bdb5042ea5cda21`

Aynı test düzeltmelerden sonra tekrar çalıştırılmıştır.

## Ek kontroller

- ZIP/dosya bütünlüğü ve yerel bağlantılar.
- Markdown başlık anchor'ları.
- 12 DOI/künye gerçekliği ve kaynak iddiaları.
- L10 yayımlanmış tablo anomalisinin görünür tutulması.
- L12 açık PDF üzerinde 900 saniye ve 10 seed/koşu kontrolü.
- NASE ve CUJAST resmî DergiPark kapsam/yazım/gönderim bilgileri.
- Ortak kılavuz ile makale outline başlıklarının eşleşmesi.
- Resmî 5×3 Problem 7 örneğinin bağımsız makespan hesabı (Cmax=20).
- Üretilmiş `__pycache__`/`.pyc` dosyalarının repodan temizlenmesi.

## Sonuç

Bilal'in ilk sprint tesliminde açık P0/P1 bırakılmamıştır. Paket sonraki ekip adımına girdi olarak kullanılabilir. Projenin uygulama/deney aşaması ayrı kabul kapılarına tabidir.
