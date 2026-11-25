# Güncel Kalite ve Kabul Durumu

**Tarih:** 24.11.2026
**Kaynak branch:** `develop` + aktif çalışma PR'ları

## Kabul edilmiş teknik temel

- PFSP model/data doğrulaması: kabul.
- Taillard LF/SHA bütünlüğü: Linux + Windows CI PASS.
- DE, PSO, DBO, RIME, NRBO: `develop` üzerinde entegre.
- RIME kaynak/kod ve 5/5 contract kapısı: kabul.
- DBO/NRBO runtime/FE/seed/bounds teknik kapıları: kabul.
- **DBO/NRBO akademik P1:** 23.11.2026'da yönetici bağımsız kaynak/kod incelemesiyle **KAPALI**. Erişilemeyen özgün metin ayrıntıları doğrulanmış gibi gösterilmeyecek.
- NEH klasik baseline: **KABUL**. Deterministik implementasyon, testler ve ta001/ta011/ta021 sonuçları hazır; Ubuntu/Windows CI PASS.
- [PSO yöntem metni](../paper/method_pso.md) tamamlandı. Etkin parametreler çalıştırıcı ve manifestte tanımlı.
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

Akademik P1 kapanışı yukarıdaki 23.11.2026 yönetici kaydına dayanır. Bağımsız tekrar çalıştırmada algoritma sözleşmesi 4/4, manifest 4/4 ve CSV doğrulayıcısı 7/7 geçti. `python -B src/main.py --check` üç benchmark ve beş algoritma için başarılı. PR #5 deney çalıştırıcısı, manifest ve CSV doğrulayıcısı `develop` dalına `a37ef0e241517a446355a58869a14837fa7427bf` birleştirme commit’iyle alındı. Method-freeze kararının SHA kaydı ve üç koşuluk dry-run ayrı kapılardır.

## Güncel deney çıktıları ve düzeltme

- Method-freeze `df8ac616165dc0105c83429e5ed000f34045aafa` için [dry-run paketi](evidence/method-freeze-dry-run-df8ac61/README.md) mevcut: 15 CSV / 45 pilot koşu, final veriden ayrı.
- [Final manifest](../results/tables/experiment_manifest.json) deney sürümü `73ce39c78a6263ce6f252267edeff0515157aca1` ve temiz başlangıç kaydeder: 15 CSV / 450 koşu / 13.500.000 FE, seed 2026–2055. [Doğrulama kaydı](../results/verification.json), 9 istatistik tablosu ve 18 grafik dosyası mevcut.
- Merge öncesi denetimde bulunan kesirli FE kabulü validator'da düzeltildi; kesirli/NaN/Inf ve boolean history FE regresyonları eklendi. Yerel benchmark CRLF sorunu, dosyalar kayıtlı LF/SHA biçimine getirilerek giderildi; referans değerler değiştirilmedi.
- Düzeltmenin öz kontrolü: ilgili testler 14/14, final validator 450/450 başarılı. Yeni düzeltme **bağımsız inceleme bekliyor**; yukarıdaki tarihsel PR #5 kabulü yeni sürüme taşınmaz. Bu kayıt yönetici freeze/merge onayı yerine geçmez.

## Kalan proje blokları

- Yönetici teknik testleri eklendi; kod/CSV/Cmax/Gantt/sayısal makale kontrolü CI ile yeniden doğrulanır. **Dış bağımsız final QA henüz yapılmadı.**
- 450 koşu öncesinde açıkça verilmiş EXPERIMENT-FREEZE yönetici onayı kaydı bulunamamasının protokol istisnası ikinci QA'da değerlendirilmelidir.
- Result/Discussion/Conclusion metni mevcut; gerçek yazar/e-posta/ORCID/CRediT/COI/funding/AI ve veri-kod erişim onayları bekliyor.
- CPU/RAM ve ölçüm ortamı delili, NASE resmî İngilizce DOCX şablonu ve danışman onayı bekliyor.

## Main kuralı

`main`e yalnız final kalite kapısı P0=0/P1=0 ve final deney provenance doğrulandıktan sonra `develop -> main` PR ile geçilir.

## 25.11.2026 — Yönetici final denetimi

- PR #11 `develop`e merge edildi (merge `3589e6ba4c4d48db46a6c9271cdba91737f3daf2`). 15 CSV/450 koşu/13.500.000 FE/seed 2026–2055 manifestte mevcut ve validator ile kontrol edildi.
- Bilal PR #12 ders/NASE taslağı ve Gantt kaynaklarını birleştirir; yönetici İngilizce tablolardaki Türkçe etiketleri, README durumunu ve devredilmiş yazar katkılarını düzeltti.
- `tests/test_manager_final_acceptance.py`: deney SHA/manifest/etkin parametre, ham SHA-256, validator ve kazananların bağımsız Gantt doğrulama regresyonu.
- Kaynak ve sınırlar [yönetici kabul kaydında](MANAGER_FINAL_GATE_2026-11-25.md), ikinci QA süreci [devir belgesinde](INDEPENDENT_QA_HANDOFF.md) yer alır.
- **Teknik CI PASS, nihai yayın izni değildir.** E-posta/ORCID, kesin CRediT/sıra, COI/funding/AI, CPU/RAM, DOCX şablonu ve danışman onayı hâlâ P1 kabul bloğudur. Deney öncesi EXPERIMENT-FREEZE yönetici onayının ayrı zaman damgalı kanıtı bulunamadı; sonradan verilmiş gibi gösterilmez. Bu nedenle `main`e promosyon yapılmaz.
