# Git Branch ve Pull Request Çalışma Düzeni

Bu belge 19.11.2026 tarihinden itibaren proje için geçerli Git çalışma düzenidir.

## Kalıcı branch'ler

| Branch | Sahip / amaç | Doğrudan push |
|---|---|---|
| `main` | Yalnız kabul edilmiş, yeniden üretilebilir proje durumu | Hayır |
| `develop` | Bağımsız incelemeden geçmiş çalışmaların ortak entegrasyonu | Normalde hayır |
| `work/muhammed` | Muhammed'in aktif çalışma alanı | Muhammed |
| `work/burak` | Burak'ın aktif çalışma alanı | Burak |
| `work/seref` | Şeref'in aktif çalışma alanı | Şeref |
| `work/tarik` | Tarık'ın aktif çalışma alanı | Tarık |
| `work/bilal` | Bilal'in aktif çalışma alanı | Bilal |

`backup/*` ve eski `feature/*` branch'leri tarihsel/geçiş kaydıdır; yeni geliştirme bunlara yapılmaz.

## Günlük çalışma akışı

Her ekip üyesi normalde yalnız kendi `work/<isim>` branch'ine push eder.

Başlangıçta:

```bash
git fetch origin
git switch work/<isim>
git pull --ff-only origin work/<isim>
```

Çalışma tamamlandığında:

1. Öz-kontrol ve ilgili testler çalıştırılır.
2. Commit/push yalnız kendi `work/<isim>` branch'ine yapılır.
3. Pull Request hedefi `develop` olur.
4. Belirlenen bağımsız incelemeci en az bir kritik kontrolü tekrarlar.
5. P0/P1 açık ise PR merge edilmez.
6. Kabul edilen PR `develop` içine alınır.
7. Belirli bir milestone tamamen kabul edildiğinde `develop -> main` PR'ı açılır.

## main'e kabul kuralı

`main` yalnız aşağıdaki şartlarda ilerler:

- ilgili kod/belge gerçekten mevcut,
- zorunlu testler PASS,
- bağımsız inceleme tamam,
- P0 = 0,
- P1 = 0,
- kaynak/DOI/veri iddiaları doğrulanmış,
- deney verisiyse kullanılan commit ve seed/FE koşulları kayıtlı.

Bir dosyanın mevcut olması tek başına kabul kanıtı değildir.

## Yasaklar

- `main`e doğrudan normal geliştirme push'u yapılmaz.
- Başkasının `work/*` branch'ine izinsiz push yapılmaz.
- Test başarısızlığını gizlemek için test, seed, maxFEs veya kabul kriteri değiştirilmez.
- Pilot/smoke verisi final bilimsel veri diye kullanılmaz.
- CSV, p-değeri veya sonuç tablosu elle düzeltilmez.
- Normal ekip çalışmasında force-push/history rewrite yapılmaz.
- Başarısız/eksik çalışma `TAMAMLANDI` diye işaretlenmez.

## Commit mesajları

Önerilen biçim:

```text
feat: ...
fix: ...
test: ...
docs: ...
chore: ...
```

Örnekler:

```text
feat: RIME soft-rime ve hard-rime mekanizmalarını ekle
test: NRBO exact FE ve seed kontrollerini ekle
docs: deney protokolünü güncelle
```

## Deney freeze

Nihai 450 koşudan önce kabul edilmiş `develop` sürümü bir freeze commit/tag ile sabitlenir. Freeze sonrasında algoritma, problem modeli veya benchmark verisi değişirse etkilenen final deneyleri yeniden üretilir.

## Geçmiş branch'ler

19.11.2026 öncesindeki commit geçmişi yeniden yazılmaz. Sonradan oluşturulmuş branch'ler geçmişte kullanılmış gibi sunulmaz. `backup/pre-governance-2026-11-19` eski durumun güvenli snapshot'ıdır.
