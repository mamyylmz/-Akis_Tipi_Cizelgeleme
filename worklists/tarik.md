# Tarık — Work List

**Branch:** `work/tarik`

1. Tamamlandı: DBO/NRBO akademik P1 kapandı ve PR #5 teknik kabulü kaydedildi.
2. Tamamlandı: PR #5 deney çalıştırıcısı, manifest ve CSV doğrulayıcısı `develop` dalına alındı. NEH kabul edildi.
3. Tamamlandı: [PSO yöntem metni](../paper/method_pso.md) etkin parametreler ve atalet ağırlığı kaynağıyla eşleştirildi.
4. Mevcut: `df8ac616165dc0105c83429e5ed000f34045aafa` için [5×3×3 dry-run kanıtı](../docs/evidence/method-freeze-dry-run-df8ac61/README.md); 15 CSV / 45 pilot koşu final veriden ayrı.
5. Mevcut: [manifest](../results/tables/experiment_manifest.json) deney sürümü `73ce39c78a6263ce6f252267edeff0515157aca1`; seed 2026–2055, 450 final koşu.
6. Yönetici teknik kontrolünde: validator'ın kesirli/NaN/Inf FE düzeltmesi ve regresyonları geçerli; `tests/test_manager_final_acceptance.py` 450/450 yeniden doğrulama, ham hashler ve final Gantt doğrulamasını yapar. Dış bağımsız incelemeci bu sonucu ayrıca teyit etmelidir.
7. Mevcut: betimsel istatistikler, Wilcoxon rank-sum + Holm, Friedman + Nemenyi/CD, convergence ve box plotları. Güncel kabul sınırı [kalite durumunda](../docs/quality_status.md).
8. Tamamlanan: manifestte Windows, Python/NumPy/SciPy/Pandas ve runtime kayıtları var. **Eksik birincil delil:** CPU/RAM modeli ve deney çalışırken makine/yük/ölçüm koşulları Tarık tarafından teyit edilmeli.

**Kabul:** final CSV'ler elle değiştirilmemiş; manifest freeze commit'e bağlı; tüm istatistikler ham final sonuçlardan yeniden üretilebilir.
