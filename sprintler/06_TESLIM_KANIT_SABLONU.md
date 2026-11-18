# Teslim Kanıtı Şablonu

**Sürüm 1.1 · 18.11.2026**

Şablon [ortak kılavuzun](../docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md) §15–16 teslim ve düzeltme alanlarıyla uyumludur; resmî ders belgesi değildir.

| Alan | Doldurulacak bilgi |
| --- | --- |
| Görev / sahip | Görev kimliği ve sorumlu |
| Sürüm / SHA | Commit SHA veya dosya sürümü ve SHA-256 kayıt bağlantısı |
| Değişen dosyalar | Bağlantılar ve değişiklik gerekçesi |
| Beklenen / gözlenen | Kontrol başına beklenen ve gerçek sonuç |
| Komut / kayıt | Tekrarlanabilir komut ve çıktı dosyası |
| Öz-kontrol | PASS / FAIL, kapsamı ve sınırları |
| Bağımsız denetçi kararı | İncelemeci, tekrarladığı kritik kontrol, tarih ve karar; yoksa BEKLİYOR |
| Açık P0 / P1 / P2 | Kimlik, eksik, sahibi ve kapanış kanıtı |
| İstenen düzeltme / yeni tarih | Somut eylem ve hedef tarih |
| Yeniden kabul şartı | Düzeltmeden sonra aynı sürüm üzerinde tekrarlanacak kontrol ve beklenen sonuç |
| Nihai durum | KABUL / DÜZELTME GEREKİYOR / BLOKE; kısmi kapsamı ayrıca belirt |

P0/P1 varken tam kabul verilmez. Teknik kontrol PASS sonucu, bilimsel doğrulama veya bağımsız kabul yerine geçmez. İnceleme talebi yazılmış olması gönderildiği anlamına gelmez.
