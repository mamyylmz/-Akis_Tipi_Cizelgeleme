# Şeref — Work List

**Branch:** `work/seref`

1. Burak'ın DBO/NRBO özgün denklem eşleme tablosunu **bağımsız** incele; doğrulanmayan maddeyi PASS sayma.
2. P1 kapanırsa `docs/quality_status.md` için kısa bağımsız karar kanıtı üret.
3. NEH klasik baseline'ı `src/heuristics/neh.py` altında deterministik olarak uygula ve `tests/test_neh.py` ekle.
4. NEH için ta001/ta011/ta021 permütasyon, Cmax, RPD ve runtime üret; 30 koşu yapma.
5. `paper/method_model.md` içeriğini final makale 3.1/3.2 metnine dönüştür; DE yöntem alt bölümünü özgün kaynak + gerçek kod parametreleriyle tamamla.
6. Final deney sonrası en iyi çözüm/Gantt Cmax'larını bağımsız yeniden hesapla.

**Kabul:** DBO/NRBO P1 bağımsız kapanmış; NEH deterministik ve testli; DE/model metni gerçek kodla aynı.
