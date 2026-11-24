# Makale Hazırlık Durumu

**Tarih:** 22.11.2026

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

1. Method-freeze kararının commit kimliğiyle kaydedilmesi.
2. Experiment-freeze ve 450 final koşu.
3. Descriptive statistics, Wilcoxon+Holm, Friedman ve anlamlıysa Nemenyi/CD.
4. Final convergence/box plotlar, en iyi çözümler ve büyük örnek Gantt.
5. Results/Discussion/Conclusion.
6. Yazar kimlikleri, ORCID, kurum, CRediT, conflict/data/code/AI beyanları.

## Ders sürümü ve NASE sürümü

Ders için ortak kılavuzdaki yapı korunur: Giriş, Literatür, Materyal ve Metot, Deneysel Çalışmalar, Sonuç ve Tartışma.

NASE gönderim sürümünde literatür Introduction içine entegre edilir; deneysel bulgular Results and Discussion altında birleştirilir; Conclusion ayrı tutulur. Güncel format ayrıntıları `docs/journal_shortlist.md` dosyasındadır.
