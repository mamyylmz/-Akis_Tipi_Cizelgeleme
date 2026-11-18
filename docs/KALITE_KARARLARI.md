# Kalite Kararları

Bu dosyada amaç yalnızca görev tanımlamak değil, yanlış kabul yollarını sistematik olarak kapatmaktır.

## Kaynak ve bilimsel içerik

- **DOĞRULANMAMIŞ bir yayını, DOI'yi, tam metni, tabloyu veya denklemi doğrulanmış gibi yazma.** Yalnızca erişilen düzeyi belirt; erişilemeyen ayrıntı `DOĞRULANAMADI` olarak kalır.
- **Bir dosya pakette yoksa varmış gibi referans verme.** Her yerel bağlantı gerçek dosya üzerinde kontrol edilir.
- **Bir kaynaktaki sayısal tutarsızlığı kendi verimiz gibi düzeltme veya sessizce kullanma.** Kaynak hatası olduğu belirtilir ve sonuç kanıtı olarak kullanılmaz.
- **Dersin izin verdiği dergi listesi dışındaki dergiyi hedef dergi olarak kesinleştirme.** İyi bir dergi olması kural uyumunun yerine geçmez.
- **Güncel BKS/referans değerini 'optimum' diye genelleme.** Kaynağın ifade ettiği statü neyse onu kullan.

## Veri ve model

- **Taillard verisini elle uydurma, internetten kaynağı belirsiz matris kopyalama veya seed/üretim algoritmasını belgesiz bırakma.** Veri deterministik üretilebilir ve hash'lenebilir olmalıdır.
- **Sadece Cmax sabit sayısını test ederek model doğrulaması yapma.** Gerçek referans permütasyonu model üzerinden yeniden hesaplanmalıdır.
- **Tek makespan uygulamasının kendi kendini doğrulamasını bağımsız kontrol sayma.** Testte farklı bir 2-B DP hesap yolu kullanılmalıdır.
- **`ΣCj` ile `Cmax` kavramlarını karıştırma.** Problem 7'nin amacı yalnızca makespan minimizasyonudur.
- **Random-key decode sonucunu geçerli kabul edip kontrolü tamamen atlama.** Doğrudan objective çağrılarında hatalı permütasyonlar açıkça reddedilir.
- **Veri yönünü (machine-major/job-major) belgesiz bırakma.** Depoda kullanılan yön açıkça yazılır ve ta001 resmi matrisiyle kontrol edilir.

## Kod ve test

- **Testi geçsin diye mevcut test kodunu veya kabul kriterini değiştirme.** Üretim kodu test sözleşmesine uydurulur; kriter değişikliği ayrı karar gerektirir.
- **`python src/main.py --check` PASS verdi diye proje/model tam kabul edildi deme.** Bu duman testi beş algoritma eksikken bile uyarıyla geçebilir; bağımsız testler zorunludur.
- **Örnek sphere problemi veya sentetik veriyi PFSP sonucu gibi bırakma.** Örnek kod üretim modelinden tamamen ayrılır.
- **Hazır meta-sezgisel kütüphaneden alınan sonucu ekip algoritmasının sonucu gibi raporlama.** Nihai algoritma ekip tarafından yazılır.
- **FE bütçesini iterasyon sayısıyla eşitleme veya evaluate çağrılarını sayaç dışında bırakma.** Her amaç değerlendirmesi bir FE'dir.
- **Aynı seed'in tekrarlanabilirliğini test etmeden 'reproducible' yazma.** Rastgelelik yalnızca `np.random.default_rng(seed)` üzerinden yürür.

## Teslim ve kalite kapısı

- **P0/P1 açıkken TAMAMLANDI/PASS yazma.** Durum `KISMİ`, `DÜZELTME_GEREKİYOR` veya `BLOKE` olmalıdır.
- **Kendi çıktını tek başına bağımsız ekip incelemesi yapılmış gibi gösterme.** Otomatik/ikinci yöntem doğrulaması ile insan bağımsız incelemesini ayrı raporla.
- **Eski hash/test raporunu yeni dosya sürümüne aitmiş gibi kullanma.** Her düzeltmeden sonra kanıt yeniden üretilir.
- **Bir eksikliği kapatmak için sahte dosya, sahte link, sahte şablon veya sahte test çıktısı üretme.** Eksik gerçekse eksik olarak kaydedilir.
- **Düzeltme sonrası regresyon testi yapmadan kabul verme.** Hem ilgili yeni test hem mevcut testler tekrar çalıştırılır.

Bu kurallar resmî ders belgelerinin yerine geçmez; resmî belgeyle çelişirse resmî kural üstündür.
