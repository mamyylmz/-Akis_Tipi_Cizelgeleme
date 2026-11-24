# Tarık — Work List

**Branch:** `work/tarik`

1. Tamamlandı: DBO/NRBO akademik P1 kapandı ve PR #5 teknik kabulü kaydedildi.
2. Tamamlandı: PR #5 deney çalıştırıcısı, manifest ve CSV doğrulayıcısı `develop` dalına alındı. NEH kabul edildi.
3. Tamamlandı: [PSO yöntem metni](../paper/method_pso.md) etkin parametreler ve atalet ağırlığı kaynağıyla eşleştirildi.
4. Method-freeze sonrası 5×3×3 dry-run; pipeline ve 15 CSV kapsamını kontrol et.
5. Experiment-freeze sonrası seed 2026–2055 ile 450 final koşuyu çalıştır.
6. Final validator: 15 CSV / 450 run / exact FE / best_x-Cmax-RPD-permutation/history.
7. Descriptive statistics, Wilcoxon rank-sum + Holm, Friedman + Nemenyi/CD, convergence ve box plotları üret.
8. Final deney ortamı, runtime ve yeniden üretim komutlarını makale için teslim et.

**Kabul:** final CSV'ler elle değiştirilmemiş; manifest freeze commit'e bağlı; tüm istatistikler ham final sonuçlardan yeniden üretilebilir.
