# Bilal — Literatür ve Makale Teslim Kanıtı

**Sürüm 1.2 · 18.11.2026 · Durum: ONAYLI — İLK SPRINT KABUL EDİLDİ**

Görevler: M1, M2, M7 ve K9. Sorumlu: Bilal. Nihai bağımsız denetim proje yöneticisinin talebiyle yapılmış; sonuçlar [kaynak ve belge bağımsız denetimi](../paper/source_audit.md) dosyasına kaydedilmiştir. Git SHA yerine bu paket sürümü ve `docs/literature_check_result.json` SHA-256 kayıtları kullanılmaktadır.

## Teslim edilen çıktılar

- [Literatür matrisi](../paper/literature_matrix.md): 12 birincil yayın; DOI/künye ve erişim sınırları kayıtlı.
- [Araştırma boşluğu](../paper/gap_analysis.md): üç soru adayı; 1. soru zorunlu deneyin ana araştırma sorusu olarak öneriliyor.
- [Giriş taslağı](../paper/introduction_draft.md): 500–700 kelime kabul aralığında, sonuç uydurmuyor.
- [Makale iskeleti](../paper/outline.md): ortak kılavuz Bölüm III başlıklarıyla eşleşiyor.
- [Hedef dergiler](../docs/journal_shortlist.md): NASE birinci, CUJAST ikinci; resmî DergiPark kaynakları kontrol edildi.
- [5×3 Gantt verisi ve planı](../docs/gantt_plan.md): resmî Problem 7 küçük örneğinden 15 işlem yeniden hesaplandı; Cmax=20 doğrulandı.
- [Kaynak bağımsız denetimi](../paper/source_audit.md): sahte DOI/veri, L10 anomali kaydı ve önceki P1 kapanışları.

## Öz-kontrol ve bağımsız kontrol

Çalışma kökünde mevcut test dosyası değiştirilmeden çalıştırılır:

`python docs/check_literature.py`

Beklenen sonuç: tüm `checks` alanları `true`, çıkış kodu `0`.

Ek bağımsız kontroller:

| Kontrol | Sonuç |
| --- | --- |
| 12 DOI'nin yayın kimliği | PASS — uydurma kaynak tespit edilmedi |
| L10 yayımlanmış sayısal tutarsızlığın görünür tutulması | PASS |
| L12 900 s ve 10 seed/koşu bilgilerinin açık PDF'den teyidi | PASS |
| NASE/CUJAST ders listesi + güncel resmî kapsam/yazım sayfaları | PASS |
| Ortak kılavuz ↔ makale iskeleti başlık eşleşmesi | PASS |
| Yerel dosya/anchor bağlantıları | PASS |
| Resmî 5×3 örnek bağımsız hesabı | PASS — Cmax=20 |
| Gantt için uydurma zaman değeri | YOK |
| Açık P0/P1 | YOK |

`docs/check_literature.py` SHA-256: `dc3f5d92deb3ca27c5acfc75e7b45644764ba61818d425288bdb5042ea5cda21`. Bu düzeltme turunda test dosyası değiştirilmemiştir.

## Önceki bulguların kapanışı

| Kimlik | Nihai durum |
| --- | --- |
| P1-01 Eksik teslim kanıtı | KAPALI |
| P1-02 Çelişkili doğrulama beyanı | KAPALI |
| P1-03 Ders dışı dergi adayları | KAPALI |
| P1-04 Ders iskeleti | KAPALI |
| P1-05 Kaynak/tam metin belirsizliği | Bilal sprinti için KAPALI; erişilemeyen ayrıntılar tahmin edilmiyor, yöntem denklem-kod denetimi algoritma sahiplerinin teknik kapısına ait |
| P1-06 Bağımsız inceleme | KAPALI |
| P1-07 Dergi/şablon kontrolü | KAPALI |
| Gantt veri bekleme | KAPALI; resmî küçük örnekten hesaplandı |

## Sprint sonrası sınır

Bu kabul yalnızca Bilal'in 18 Kasım literatür/makale/Gantt görevlerini kapatır. Aşağıdakiler henüz tamamlanmış sayılmaz ve sonraki ekip adımlarına aittir:

- `problem.py` ve Taillard veri dosyalarının Şeref tarafından doğrulanması,
- DE/PSO/DBO/RIME/NRBO kodlarının ilgili sorumlularca tamamlanması ve özgün yöntemle eşleştirilmesi,
- FE/seed sözleşmesi ve Tarık testleri,
- 30 koşu × 5 algoritma × 3 benchmark nihai deneyleri,
- gerçek results/ üzerinden istatistik, şekil, sonuç/tartışma ve özet.

**Nihai Bilal sprint kararı: PASS / ONAYLI. Bir sonraki bağımlı ekip adımına geçilebilir.**
