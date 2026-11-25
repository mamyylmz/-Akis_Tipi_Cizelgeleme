# Makale Hazırlık Durumu

**25.11.2026 · Bilal teslimi yönetici teknik denetiminde düzeltildi; dış bağımsız inceleme ve yazar/danışman onayları BEKLİYOR.** Bu durum proje kabulü veya gönderim onayı değildir.

## Birleştirilmiş içerik

- Tek ders makalesi [outline.md](outline.md): 30 zorunlu başlık korunarak giriş, literatür, yöntemler, deney/istatistik, gerçek sonuçlar, tartışma, iki özet, kaynakça, beyanlar ve ekler birleştirildi.
- [İngilizce NASE taslağı](manuscript_nase_en.md): resmî İngilizce dil şartına uygun bilimsel içerik taslağı; 16 sayısal blok aynı kaynaktan ve kaynaklar eşleşiyor. [Türkçe düzen taslağı](manuscript_nase.md) başvuru metni değildir. Ders metni esas alınır; NASE kopyası `python -B tools/prepare_paper_assets.py --nase` ile türetilir.
- [Final çizelge desteği](support/final_best_schedules.md): üç seçili minimum, bütün minimum eşitlikleri, verifier zaman CSV'leri ve Gantt'lar. Zamanlar elle üretilmedi.
- [Belge aracı](../tools/prepare_paper_assets.py): ham hash, tablo yeniden hesaplama, 16 sayısal blok, iki sürüm eşleşmesi, kaynakça, özet ve çizelge kontrolü.
- Giriş taslağı, literatür matrisi, kaynak audit'i ve sahip yöntem dosyaları değiştirilmedi. Ham sonuçlar ve model/veri dosyaları değişmedi. Bilal teslimi GitHub'da commit/push edilmiştir.

## Veri ve kabul sınırı

Deney sürümü `73ce39c78a6263ce6f252267edeff0515157aca1`: 15 CSV, 450 koşu, 13500000 FE, seed 2026–2055. [Manifest](../results/tables/experiment_manifest.json) ve [verification.json](../results/verification.json) temel kayıtlardır; pilotlar karıştırılmadı. Kontrol tabanı `3589e6b` deney commit'iyle karıştırılmaz. Bu iki sürümün algoritma/model/veri farkında yalnız PSO açıklama ve yorum değişikliği görüldü; davranış değişikliği bulunmadı.

Yönetici, [final kabul kaydında](../docs/MANAGER_FINAL_GATE_2026-11-25.md) doğrulama kaynaklarını ve gerçekleşen entegrasyonu ayrı tutar. Yeni `tests/test_manager_final_acceptance.py` manifest/hash/450 FE sözleşmesi ile Gantt kaynaklarını ayrıca kontrol eder. Bu, dış bağımsız QA veya yazar/danışman onayı değildir. PR birleştirilmesi tek başına belgelenmiş kabul kararı yerine geçirilmemiştir.

## Öz kontrol

| Komut / kontrol | Gerçek sonuç |
| --- | --- |
| `python docs/check_literature.py` | Giriş 557 kelime, 12 DOI, 24 matris satırı, 30 başlık; yapısal kontroller başarılı |
| `python tools/check_repo_integrity.py` | 24/24 gerekli dosya, benchmark hashleri, yerel bağlantılar başarılı |
| `python tools/check_experiment_outputs.py --raw-dir results/raw --runs 30 --seed-base 2026` | 15 CSV / 450 koşu başarılı |
| `python -m unittest discover -s tests -v` | 86/86 başarılı; mevcut testler değiştirilmedi |
| Üç çözümde `python tools/verify_final_schedule.py --instance … --permutation … --expected-cmax …` | 1288 / 1586 / 2318; sıfır çakışma ve öncelik ihlali |
| `python -B tools/prepare_paper_assets.py --check` | 16 sayısal blok; 13 kaynak; yetim/atıfsız 0/0; hashler ve çizelgeler eşleşiyor |
| Özet / Abstract | Her iki sürümde 209 / 221 kelime; her dilde 6 anahtar kelime |

Otomatik öz kontrol insan bağımsız incelemesi değildir. Tablolar kaynak hassasiyeti veya açık gösterim yuvarlamasıyla aktarılır; sonuç anlatımı tablolarla ayrıca karşılaştırılmıştır.

## Teyitler ve kalan işler

**Teyit edildi:** Bilal'in 25.11.2026 mesajıyla altı yazarın ad-soyadı ve ortak kurum/fakülte/bölümü; danışman 1., takım lideri 2. sıra. İngilizce NASE metni gönderim için temel taslaktır; Türkçe NASE kopyası yalnız iç düzen kontrolüdür.

**P0:** Bu belge çalışmasında yeni veri/model bozulması bulunmadı; proje geneli için yeni kabul kararı verilmedi.

**P1 / İNCELEME BEKLİYOR:**

1. Yönetici teknik validator/manifest/çizelge testlerini tamamladı; harici bağımsız incelemeci [devir paketindeki](../docs/INDEPENDENT_QA_HANDOFF.md) kapıları yeniden doğrulamalı. Deney öncesi açık EXPERIMENT-FREEZE yönetici onayına dair tarihli kayıt bulunamadığı sınırlaması ayrıca açıklanmıştır.
2. Tarık/Şeref: rank-sum bağ düzeltmesi yokluğu, seed bloklaması ve veriden seçilen referansın yorum sınırları incelenmeli. P-değerleri korunmuştur; bu bir doğrulanmış yeni kod hatası veya otomatik kabul kapatması değildir.
3. Yöntem sahipleri/danışman: birleşik yöntem ve sonuç anlatımının, kaynak erişim sınırlarının bağımsız incelemesi.
4. Her yazar: e-posta, ORCID, fiilî CRediT katkısı; danışman: diğer yazarların nihai sırası/puanı ve sorumlu yazar onayı.
5. Tarık: deney CPU/RAM ve süre ölçüm koşulları.
6. Bütün yazarlar: “çıkar çatışması yoktur / dış finansman alınmamıştır” taslakları, teşekkür, AI kullanım kapsamı ve veri/kod erişim beyanı.
7. Danışman: nihai NASE dil/dergi seçimi ve etik izin gerekliliği; resmî DOCX şablonuna aktarım ve son biçim denetimi.

**P2:** İngilizce NASE metninin nihai teknik/redaksiyon incelemesi ve Word şablonuna aktarımı bekler. README'nin artık yanlış olan “final koşular üretilmedi” ifadesi düzeltildi. İngilizce NASE sayısal tablolarının Türkçe başlık/değer etiketleri de kaynak veriler korunarak İngilizceye çevrildi. DOCX aktarımında uzun SHA/permütasyon tabloları, denklem düzenleyicisi ve Gantt okunabilirliği kontrol edilecek. [NASE kuralları](../docs/journal_shortlist.md) gönderim günü tekrar doğrulanacak.
