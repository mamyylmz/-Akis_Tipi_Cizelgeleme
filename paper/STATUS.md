# Makale Hazırlık Durumu

**Tarih:** 24.11.2026

## Hazır / kullanılabilir girdiler

- Giriş taslağı.
- 12 kaynaklık literatür matrisi ve kaynak audit'i.
- Ana araştırma sorusu: eşit FE altında beş algoritmanın çözüm kalitesi ve kararlılığı.
- PFSP matematiksel model ve random-key gösterimi — final metin tamamlandı.
- RIME yöntem notu.
- DBO/NRBO yöntem metni — akademik P1 yönetici bağımsız kabulüyle kapandı.
- 5×3 doğrulama örneği ve Cmax=20 zaman çizelgesi.
- DE ve [PSO final yöntem metinleri](method_pso.md).
- NEH deterministik baseline ve üç Taillard sonucu kabul edildi.
- PR #5 deney çalıştırıcısı, manifest ve CSV doğrulayıcısı `develop` dalına alındı.
- Final en iyi çözüm için bağımsız schedule/Cmax doğrulayıcı.
- Taillard benchmark provenance ve 1278/1582/2297 referans kontrolleri.

## Makaleyi bloke eden işler

1. Validator düzeltmesinin bağımsız incelemesi; güncel kabul sınırı [kalite durumunda](../docs/quality_status.md).
2. Final en iyi çözümlerin Gantt çıktıları ve mevcut tablo/grafiklerin makaleye aktarımı.
3. Results/Discussion/Conclusion.
4. Yazar kimlikleri, ORCID, kurum, CRediT, conflict/data/code/AI beyanları.

[Method-freeze dry-run kanıtı](../docs/evidence/method-freeze-dry-run-df8ac61/README.md) `df8ac616165dc0105c83429e5ed000f34045aafa` sürümüne bağlıdır; 45 pilot koşu final veri değildir. [Final manifest](../results/tables/experiment_manifest.json) `73ce39c78a6263ce6f252267edeff0515157aca1` sürümünden 450 koşuyu kaydeder. Betimsel istatistikler, Wilcoxon+Holm, Friedman, üç benchmark için Nemenyi/CD ve yakınsama/kutu grafikleri mevcuttur.

## Ders sürümü ve NASE sürümü

Ders için ortak kılavuzdaki yapı korunur: Giriş, Literatür, Materyal ve Metot, Deneysel Çalışmalar, Sonuç ve Tartışma.

NASE gönderim sürümünde literatür Introduction içine entegre edilir; deneysel bulgular Results and Discussion altında birleştirilir; Conclusion ayrı tutulur. Güncel format ayrıntıları `docs/journal_shortlist.md` dosyasındadır.
