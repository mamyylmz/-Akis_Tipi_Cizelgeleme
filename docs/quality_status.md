# Güncel Kalite ve Kabul Durumu

**Tarih:** 23.11.2026  
**Kaynak branch:** `develop` + aktif çalışma PR'ları

## Kabul edilmiş teknik temel

- PFSP model/data doğrulaması: kabul.
- Taillard LF/SHA bütünlüğü: Linux + Windows CI PASS.
- DE, PSO, DBO, RIME, NRBO: `develop` üzerinde entegre.
- RIME kaynak/kod ve 5/5 contract kapısı: kabul.
- DBO/NRBO runtime/FE/seed/bounds teknik kapıları: kabul.
- **DBO/NRBO akademik P1:** 23.11.2026'da yönetici bağımsız kaynak/kod incelemesiyle **KAPALI**. Erişilemeyen özgün metin ayrıntıları doğrulanmış gibi gösterilmeyecek.
- NEH klasik baseline: implementasyon/test/üç benchmark sonucu hazırlanıyor; Şeref kapsamı yönetici tarafından devralındı.
- Bağımsız schedule/Cmax verifier: final sonuçları üretim `Problem` sınıfından bağımsız yeniden hesaplamak üzere hazırlanıyor.

## DBO/NRBO P1 kapanış sınırı

Kabul kararı şunları doğrular:
- DBO Denklem (1)–(7) numaralandırması yazar kodu ve açık erişim yöntem kaynaklarıyla tutarlıdır.
- NRBO NRSR/TAO bileşenleri resmi yazar koduyla proje koduna eşlenmiştir.
- FE tabanlı `R`/`delta` proje uyarlamasıdır.

Kabul kararı şunları **iddia etmez**:
- kapalı NRBO özgün makalesindeki denklem numaralarının doğrulandığını;
- DBO özgün PDF'sindeki `Ub = X(1±R)` baskısının doğrudan okunduğunu.

## Kalan proje blokları

- PSO final makale yöntem metni.
- Tarık PR #5 deney/manifest/validator entegrasyonu.
- Method-freeze ve experiment-freeze.
- 450 final koşu.
- Final istatistik/şekil ve final en iyi-çözüm Gantt uygulaması.
- Makalenin gerçek Results/Discussion/Conclusion ve beyanları.
- NASE final biçim uyarlaması.

## Main kuralı

`main`e yalnız final kalite kapısı P0=0/P1=0 ve final deney provenance doğrulandıktan sonra `develop -> main` PR ile geçilir.
