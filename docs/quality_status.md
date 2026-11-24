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
- NEH klasik baseline: **KABUL**. Deterministik implementasyon, testler ve ta001/ta011/ta021 sonuçları hazır; Ubuntu/Windows CI PASS.
- Bağımsız schedule/Cmax verifier: **KABUL**. Küçük 5×3 örnek, üç Taillard referans permütasyonu ve üç NEH permütasyonu üretim `Problem` sınıfından bağımsız yeniden hesaplanarak doğrulandı.

## DBO/NRBO P1 kapanış sınırı

Kabul kararı şunları doğrular:
- DBO Denklem (1)–(7) numaralandırması yazar kodu ve açık erişim yöntem kaynaklarıyla tutarlıdır.
- NRBO NRSR/TAO bileşenleri resmi yazar koduyla proje koduna eşlenmiştir.
- FE tabanlı `R`/`delta` proje uyarlamasıdır.

Kabul kararı şunları **iddia etmez**:
- kapalı NRBO özgün makalesindeki denklem numaralarının doğrulandığını;
- DBO özgün PDF'sindeki `Ub = X(1±R)` baskısının doğrudan okunduğunu.

## PR #5 · Bağımsız teknik karar

**24.11.2026 · İncelenen SHA:** `c3c2b38f66485370a0dd8104577732ba43a7cf1b`
**Karar:** **P0=0 / P1=0 — KABUL** (deney çalıştırıcısı, manifest ve CSV doğrulama kapsamı).

Akademik P1 kapanışı yukarıdaki 23.11.2026 yönetici kaydına dayanır. Bağımsız tekrar çalıştırmada algoritma sözleşmesi 4/4, manifest 4/4 ve CSV doğrulayıcısı 7/7 geçti. `python -B src/main.py --check` üç benchmark ve beş algoritma için başarılı. Bu kayıt yerel teknik incelemenin sonucudur. GitHub PR birleştirme ve uzak CI durumu bu incelemede teyit edilmedi. Method-freeze kararının SHA kaydı ve üç koşuluk dry-run ayrı kapılardır.

## Kalan proje blokları

- PSO yöntem metni hazır. Method-freeze kararı bekliyor.
- Tarık PR #5 için teknik kabul kaydı tamamlandı. Uzak PR entegrasyon durumu teyit bekliyor.
- Method-freeze ve experiment-freeze.
- 450 final koşu.
- Final istatistik/şekil ve final en iyi-çözüm Gantt uygulaması.
- Makalenin gerçek Results/Discussion/Conclusion ve beyanları.
- NASE final biçim uyarlaması.

## Main kuralı

`main`e yalnız final kalite kapısı P0=0/P1=0 ve final deney provenance doğrulandıktan sonra `develop -> main` PR ile geçilir.
