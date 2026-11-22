# Güncel Kalite ve Kabul Durumu

**Tarih:** 22.11.2026  
**Kaynak branch:** `develop`

## Kabul edilmiş teknik temel

- PFSP model/data doğrulaması kabul edilmiş.
- Taillard LF/SHA bütünlüğü Linux + Windows CI ile doğrulanmış.
- DE, PSO, DBO, RIME, NRBO `develop` üzerinde entegre.
- RIME kaynak/kod ve 5/5 contract kapısı kabul edilmiş.
- DBO/NRBO runtime/FE/seed/bounds testleri mevcut teknik kapılardan geçmiş.

## Açık P1

**DBO/NRBO özgün yayın denklem eşleştirmesi.** Tarık'ın 22.11.2026 kapanış raporu teknik P0'ları kapatmış, ancak özgün makale denklem ↔ proje yöntemi eşleştirmesini P1 olarak açık bırakmıştır.

Kapanış:
1. Burak özgün DBO ve NRBO yayınlarından denklem numarası / kaynak satırı / proje kodu eşleme tablosunu tamamlar.
2. Şeref bu eşlemeyi bağımsız olarak inceler.
3. Kod değişikliği gerekmiyorsa yalnız akademik P1 kapanır; kod değişirse ilgili regresyon kapısı tekrar çalışır.
4. Tarık PR #5 final kararını bu kanıta göre KABUL/P0=0/P1=0 olarak günceller.

## Kalan proje blokları

- NEH klasik baseline eksik.
- DE ve PSO için final makale yöntem metinleri eksik.
- Final experiment-freeze oluşturulmadı.
- 450 final koşu ve final manifest yok.
- Final istatistik/şekil/Gantt yok.
- Makalenin deneysel sonuçlar, tartışma, sonuç ve beyan bölümleri tamamlanmadı.
- NASE gönderim sürümü için İngilizce 4 ana bölümlü dergi uyarlaması yapılmadı.

## Main notu

`main` ile `develop` geçmişi diverged durumdadır; 22 Kasım'da main'e doğrudan giren audit commit'leri daha sonra revert edilmiştir. Tarihçe yeniden yazılmayacaktır. Finalde `develop -> main` PR/merge ile uzlaştırılacaktır.
