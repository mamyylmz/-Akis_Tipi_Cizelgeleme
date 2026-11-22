# Repository Guidelines

Bu dosya yapay zekâ ajanları ve ekip üyeleri için kısa yönlendirmedir. Ayrıntılı kuralları burada kopyalama; canonical kaynakları oku.

## Önce oku

1. `docs/PFSP_Ortak_Proje_ve_Makale_Calisma_Kilavuzu.md`
2. `docs/KALITE_KARARLARI.md`
3. `docs/GIT_WORKFLOW.md`
4. `docs/quality_status.md`
5. ilgili `worklists/<isim>.md`

## Teknik sözleşme

- Amaç: PFSP makespan / Cmax minimizasyonu.
- Algoritmalar: DE, PSO, DBO, RIME, NRBO.
- Random-key decode: stable argsort.
- Benchmark: ta001=20k FE, ta011=30k FE, ta021=40k FE.
- Final deney: 30 seed (2026–2055), toplam 450 koşu.
- Seed kaynağı: `np.random.default_rng(seed)`.
- Her objective çağrısı FE sayılır.
- Testi geçsin diye seed, maxFEs, referans değer veya kabul kriteri değiştirilmez.
- P0/P1 açıkken PASS/TAMAMLANDI yazılmaz.
- Pilot/smoke sonuç final bilimsel veri değildir.

## Git

Yalnız kendi `work/<isim>` branch'inde değişiklik yap. Normal hedef `develop` PR'ıdır. `main` ve `develop` üzerine normal geliştirme push'u yapılmaz. Force-push/history rewrite kullanılmaz.

## Repo düzeni

Yeni tarihsel sprint dosyası, terminal logu veya kopya yazar kodu ekleme. Güncel görevler yalnız `worklists/` altında tutulur. Test kanıtı mümkünse CI ve PR üzerinde kalır. `results/` yalnız experiment-freeze sonrası final bilimsel çıktılar içindir.

## Makale

Ders sürümünde `paper/outline.md` ve ortak kılavuz Bölüm III esas alınır. NASE gönderim sürümü için güncel kurallar `docs/journal_shortlist.md` içindedir. Kaynak erişim düzeyi açıkça yazılır; doğrulanmayan denklem veya sayı kesin bilgi olarak kullanılmaz.
