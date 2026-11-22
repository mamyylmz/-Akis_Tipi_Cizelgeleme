# Tarık — Work List

**Branch:** `work/tarik`

1. Burak/Şeref akademik P1 kapanışını gördükten sonra PR #5 final audit durumunu güncelle; kod değişmediyse tüm eski testleri gereksiz tekrar etme, yalnız etkilenen kapıyı teyit et.
2. PR #5 kabul edilince deney runner/manifest/validator altyapısını `develop`e taşı.
3. PSO yöntem bölümünü inertia-weight kaynağı ve gerçek `src/main.py` parametreleriyle tamamla.
4. Method-freeze sonrası 5×3×3 dry-run; pipeline ve 15 CSV kapsamını kontrol et.
5. Experiment-freeze sonrası seed 2026–2055 ile 450 final koşuyu çalıştır.
6. Final validator: 15 CSV / 450 run / exact FE / best_x-Cmax-RPD-permutation/history.
7. Descriptive statistics, Wilcoxon rank-sum + Holm, Friedman + Nemenyi/CD, convergence ve box plotları üret.
8. Final deney ortamı, runtime ve yeniden üretim komutlarını makale için teslim et.

**Kabul:** final CSV'ler elle değiştirilmemiş; manifest freeze commit'e bağlı; tüm istatistikler ham final sonuçlardan yeniden üretilebilir.
