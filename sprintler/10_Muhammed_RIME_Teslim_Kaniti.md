# Muhammed — RIME teslim kanıtı

**Branch:** `feature/rime`  
**Görev:** RIME uygulaması, kaynak eşleştirmesi, testler ve beşli registry entegrasyonu.

## Üretilen dosyalar

- `src/algorithms/rime.py`
- `tests/test_rime.py`
- `paper/method_rime.md`
- `src/main.py`: RIME importu ve `ALGORITHMS["RIME"]` kaydı

## Kaynak

Su vd. (2023), *RIME: A physics-based optimization*, Neurocomputing 532, 183–214, DOI 10.1016/j.neucom.2023.02.010. Uygulama yazarların kamuya açık `RIME.m` koduyla çapraz kontrol edildi.

## Öz-kontrol

Yerel izole doğrulamada:
- 5/5 RIME unittest PASS,
- aynı seed deterministik,
- farklı seed arama akışı farklı,
- odd/tiny FE bütçeleri exact,
- ta001 tam 20.000 FE,
- sınır/NaN ihlali 0,
- best_x/best_f bağımsız yeniden değerlendirme PASS.

Bu kayıt, Burak/Tarık bağımsız incelemesinin yerine geçmez. Merge öncesi repo üzerinde tam test paketi ve `python src/main.py --check` tekrar çalıştırılmalıdır.

## Açık kabul kapısı

RIME üretimi tamamlandı. Bağımsız denetim beklenir:
- Burak: yöntem/kaynak/kod uyumu,
- Tarık: seed/FE/bounds/best_f/history ve 5/5 registry.
