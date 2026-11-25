# Bağımsız final QA devir dosyası — 25.11.2026

**Amaç:** Proje yöneticisi entegrasyonundan sonra ikinci, gerçekten bağımsız bir incelemeciye değişmez bilimsel veriyi ve makaleyi denetletmek. Bu dosya kendi başına bir PASS belgesi veya gönderim izni değildir.

## Sürüm/provenance zinciri

- METHOD-FREEZE: `df8ac616165dc0105c83429e5ed000f34045aafa`.
- Pilot: 15 CSV / 45 koşu / 1.350.000 FE; `docs/evidence/method-freeze-dry-run-df8ac61/`.
- **Gerçek final deneyde kullanılan temiz checkout:** `73ce39c78a6263ce6f252267edeff0515157aca1` (manifest ve `results/verification.json`).
- Final sonuçların `develop` entegrasyonu: PR #11, merge `3589e6ba4c4d48db46a6c9271cdba91737f3daf2`.
- Bilal makale entegrasyonu: PR #12, merge `764a2e1ba40c29e4257e13b816cbe38b5198e390` (Ubuntu/Windows PR CI PASS).
- Yönetici inceleme/testleri: `tests/test_manager_final_acceptance.py` ve `docs/MANAGER_FINAL_GATE_2026-11-25.md`. Son onaylı `develop` HEAD ayrıca teyit edilmeli.
- **Önemli:** Final 450 koşu için deneye *başlamadan önce* verilen açık yönetici EXPERIMENT-FREEZE kararının ayrı bir kanıtı tespit edilmedi. Kodun temiz kaynak SHA'sı doğrulanmıştır; geçmişe dönük olarak ön onay verilmiş gibi gösterilmemelidir.

## Yeniden üretilebilir testler

Kök dizinden, temiz checkout üzerinde:

```bash
python -m unittest discover -s tests -v
python src/problem.py
python src/main.py --check
python tools/run_neh_baseline.py
python docs/check_literature.py
python tools/check_repo_integrity.py
python tools/check_experiment_outputs.py --raw-dir results/raw --runs 30 --seed-base 2026
python -B tools/prepare_paper_assets.py --check
```

Deneyleri tekrar çalıştırmadan, mevcut ham verinin hashlerini ve tabloları doğrula. `python src/main.py` **çalıştırma**; varsayılanı 450 bilimsel koşuyu yeniden hesaplayıp sonuç klasörünü yazabilir.

Kontrol kapsamı:
1. Tam 15 CSV, her biri 30 koşu; seed 2026–2055; 450 koşu, 13.500.000 FE.
2. `experiment_manifest.json` ile `verification.json` tam eşleşmesi; 15 SHA-256 ham CSV değeri birebir.
3. `best_x` boyut/sınır, stable decode, permütasyon, Cmax/RPD ve history uyumu.
4. 3 final minimum: ta001 Cmax=1288, ta011 Cmax=1586, ta021 Cmax=2318. Bunlar optimallik ispatı değil, *gözlenen minimum*lardır.
5. `paper/support/schedule_ta*.csv` içindeki işlemleri bağımsız `tools/verify_final_schedule.py` ile yeniden hesapla; makine çakışması/iş öncelik ihlali sıfır.
6. Makalenin sayısal blokları ham veriden programatik türetilmiş ve 3 metinde tutarlı; İngilizce NASE tabloları gerçek değerleri değiştirmeden İngilizce etiketli.
7. RIME son parametreleri `pop_size=30`, `w=5`; diğer dört algoritmanın ayarları manifest/kod/makale eşleşmeli.
8. PSO dosyasında deney commit'i sonrası sadece açıklama/yorum değişikliği vardır; 450 koşunun veri üretim kodu sonradan işlevsel olarak değişmiş kabul edilmemelidir. `git diff` ile ayrıca doğrula.

## Bilimsel yorumda bağımsız inceleme maddeleri

- Üç benchmark ve her algoritma için yalnız sabit parametre düzeni var: genelleme sınırlarını kontrol et.
- Ders gereği Wilcoxon **rank-sum** + Holm kullanılmıştır; `ranksums` bağları (tie) özel düzeltmeyle ele almaz. Ayrık Cmax dağılımlarında p-değerlerinin yorumunu temkinli yaz. Testi doğrudan değiştirmek, doğrulanmış yayımlanan tabloları ve deney-protokolünü değiştirmek olur.
- Aynı seed değerleri yöntemler arasında atanmış olsa da farklı RNG dönüşümleri nedeniyle eşleştirilmiş fiziksel deney gibi yorum yapma. Friedman blok varsayımını ve rank-sum testinin bağımsızlık kabulünü yöntem sınırı olarak açıkla.
- Wilcoxon referansı veriden en küçük medyanla seçilmiştir; post-selection yanlılığı/multiple benchmark karşılaştırmaları tartışılmalı.
- NASE `about-journal` iki dili yayımladığını söylüyor, `writing-rules` ise başvuru için İngilizce şablon istiyor. Uyuşmazlıkta daha kısıtlayıcı güncel yazar kuralı temel alınmış; dergi teyidi olmadan Türkçe kopya gönderilmemeli.

## İnsan onayına bağlı gerçek blokajlar

**Bunları AI veya kod üretemez; doğrulanmadan tamamlandı yazmak yasaktır.**

- Tüm yazarların e-posta/ORCID ve sorumlu yazar onayı; katkı puanına göre kesin sıra.
- Her yazarın fiilî CRediT katkısı; Şeref'ten devralınan NEH/DE/model ve schedule işlerinin gerçek emeğe uygun işlenmesi.
- Çıkar çatışması, finansman, teşekkür, AI araç/kapsam beyanları için ekip onayı.
- Deneyin CPU/RAM ve yük/ölçüm koşullarına dair Tarık'ın birincil kayıtları. Manifest yalnız OS/Python/kütüphane sürümlerini içeriyor.
- Danışmanın hedef dergi ve etik izin kapsamı onayı.
- Resmî NASE DOCX şablonunda son biçim, yazar bilgileri, resim/denklem ve okunabilirlik kontrolü.

## Kabul politikası

Teknik/sayısal CI PASS, **hakemli dergiye hazır** olduğu anlamına gelmez. P0/P1 bilimsel doğruluk ve yayın beyanları kapanmadan `develop -> main` veya dergiye gönderim yapılmamalıdır. Bulgular varsa kaynak CSV/p-değerlerini elle düzeltme; kök neden ve etkilenmiş koşular üzerinden kanıt üret. Final deney algoritması değişirse freeze ve etkilenen bilimsel koşular yeniden gerekir.
