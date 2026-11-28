# Muhammed — Final yönetici iş listesi

**Kapsam:** Proje yöneticisi, metodoloji/entegrasyon ve kalite kabulü. **Çalışma branch'i:** `work/manager-final-acceptance` (nihai `develop` PR önce); `main` yalnız bütün P0/P1 kapıları kapanınca.

- [x] DBO/NRBO P1 ve PR #5 yönetici kabulünü önceki PR/CI kayıtlarından doğrula.
- [x] RIME kaynak/uyarlama ve nihai `pop_size=30,w=5` parametre eşleşmesini kontrol et.
- [x] METHOD-FREEZE `df8ac616165dc0105c83429e5ed000f34045aafa` ve final deneydeki temiz `73ce39c78a6263ce6f252267edeff0515157aca1` provenance'ını ayır; onay olmayan pre-run EXPR-FREEZE kaydını uydurma.
- [x] Bilal'in sayısal/şekil/metin entegrasyonunu kontrol et ve bulunan İngilizce tablo, README ve görev atıf hatalarını düzelt.
- [x] Final 15 CSV/450 koşu/13.5M FE için ek bağımsız sözleşme testi ve CI adımı ekle; üç final Cmax/Gantt eşleşmesini denetle.
- [x] Sonuç/tartışma içinde NEH ta001 1286 < en iyi meta 1288 ve istatistiksel çıkarım/genelleme sınırlarını koru.
- [x] Yazar/etik/finansman/erişim/AI teyitlerinin gerçek durumunu belirle; birincil onaylar gelmeden PASS yazma.
- [x] [Yönetici kabul kapısı](../docs/MANAGER_FINAL_GATE_2026-11-25.md) ve [ikinci QA devir dosyası](../docs/INDEPENDENT_QA_HANDOFF.md) oluştur.
- [ ] Tüm yazarların e-posta/ORCID/CRediT/sıra/çıkar çatışması/finansman/AI teyitlerini al ve danışmanla kesinleştir.
- [ ] Tarık'ın deney CPU/RAM/yük/ölçüm koşullarını doğrulanabilir kayıtla tamamla.
- [ ] Resmî İngilizce NASE DOCX şablonuna geçişi ve son danışman/redaksiyon onayını bitir.
- [ ] Dış bağımsız QA'yı geçir, varsa kalan P0/P1 bulgularını kapat; ardından yalnız normal PR ile `develop -> main` promosyonunu yap.

**Durum:** Sayısal/teknik doğrulama için CI dayanakları mevcut; dergi ve nihai `main` release'i **BLOCKED**. Dış inceleme bağımsız olarak henüz yapılmadı.
