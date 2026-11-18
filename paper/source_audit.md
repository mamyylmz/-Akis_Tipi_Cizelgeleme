# Bilal — Kaynak ve Belge Bağımsız Denetimi

**18.11.2026 · Sürüm 1.0 · Durum: BİLAL İLK SPRINTİ İÇİN PASS**

Bu kayıt, son paketin mevcut kabul kriterleri değiştirilmeden yeniden denetlenmesi sonucudur. `docs/check_literature.py` değiştirilmemiştir; yapısal test aynı dosya ile yeniden çalıştırılmıştır. Kaynak gerçekliği ve sayısal iddialar, otomatik testin dışında bağımsız olarak kontrol edilmiştir.

## 1. Yapısal kontrol

- `python docs/check_literature.py`: **PASS**.
- Giriş: 500–700 kelime aralığında.
- Literatür matrisi: iki tabloda 24 kaynak satırı ve 12 benzersiz DOI.
- Yerel Markdown bağlantıları ve başlık anchor'ları: **PASS**.
- Makale iskeleti ortak kılavuz Bölüm III ile başlık/sıra bakımından eşleşiyor: **PASS**.
- Hedef dergiler ortak kılavuzdaki izinli listeden NASE ve CUJAST: **PASS**.
- Test betiğinin SHA-256 değeri bu düzeltme boyunca değişmedi: `dc3f5d92deb3ca27c5acfc75e7b45644764ba61818d425288bdb5042ea5cda21`.

## 2. Kaynak gerçekliği ve yalancı veri kontrolü

12 DOI'nin tamamı yayıncı veya güvenilir bibliyografik kayıtla eşleştirildi. Uydurma yayın, uydurma DOI veya Bilal tarafından üretilmiş sahte deney sonucu tespit edilmedi.

| ID | Bağımsız kontrol sonucu |
| --- | --- |
| L01 Taillard 1993 | DOI, dergi/cilt/sayfa ve PFSP makespan benchmark kapsamı doğrulandı. |
| L02 NEH 1983 | DOI, künye ve yayıncı özeti doğrulandı. Tam metin erişimi abonelik kısıtlı; erişilemeyen deney ayrıntısı matriste tahmin edilmiyor. |
| L03 Bean 1994 | DOI, künye ve random-key temsil açıklaması doğrulandı. |
| L04 DE 1997 | DOI, künye ve continuous global optimization yöntemi doğrulandı. |
| L05 PSO 1995 | IEEE DOI/künye ve kamuya açık PDF üzerinden temel PSO yöntemi doğrulandı. Sonradan kullanılan inertia-weight varyantı L05'e otomatik atfedilmeyecek. |
| L06 DBO | DOI, çevrimiçi yayın tarihi (27.11.2022), 2023 cilt bilgisi, benchmark kapsamı ve Wilcoxon/Friedman kullanımı yayıncı sayfasından doğrulandı. |
| L07 RIME | DOI, 2023 Neurocomputing künyesi ve soft-rime/hard-rime yöntem çekirdeği doğrulandı. |
| L08 NRBO | DOI, 2024 EAAI künyesi, NRSR/TAO yöntem çekirdeği ve benchmark kapsamı yayıncı sayfasından doğrulandı; yazarın MATLAB File Exchange uygulaması ek çapraz kontrol kaynağıdır. |
| L09 Gmys 2022 | DOI, INFORMS künyesi ve kesin çözüm/üst sınır ayrımı doğrulandı. |
| L10 Tsiftsoglou vd. 2026 | DOI ve açık MDPI tam metni doğrulandı. Ta005 `best=1235`, `average=1226.2` tutarsızlığı kaynakta gerçekten mevcut; bu değer bilimsel kıyas kanıtı olarak kullanılmıyor. |
| L11 Li vd. 2024 | AAAI DOI/künye ve yazar ön baskısında 50 eğitim dönemi, üç seed ve raporlama yaklaşımı doğrulandı. |
| L12 Cáceres-Gelvez vd. 2026 | DOI ve açık yazar PDF'si doğrulandı. §4.3'te reduced MIP başına 900 s sınır; §5'te farklı seedlerle 10 koşu bilgisi doğrulandı. |

## 3. 5×3 model doğrulaması

Dersin resmî Problem 7 belgesindeki işlem süreleri bağımsız olarak yeniden hesaplandı:

- J1=(3,4,2), J2=(2,3,4), J3=(4,1,3), J4=(1,4,2), J5=(3,2,3)
- sıra=(J4,J2,J1,J5,J3)
- bağıntı=`C[i,j]=max(C[i-1,j], C[i,j-1])+p[pi[i],j]`
- gözlenen **Cmax=20** → **PASS**.

15 işlemin başlangıç/bitiş zamanları `docs/gantt_plan.md` içine işlendi. Böylece önceki "veri bekleniyor" durumu kapatıldı; uydurma Gantt kullanılmadı.

## 4. Dergi kontrolü

**NASE:** Resmî amaç-kapsam sayfası Industrial Engineering ile Computer Science and Information Systems Engineering alanlarını içeriyor. Resmî yazım kuralları sayfası biçim, özet, anahtar kelime, ORCID, APA ve AI beyanı koşullarını yayımlıyor ve manuscript template bağlantısını veriyor.

**CUJAST:** Resmî amaç-kapsam sayfası mühendislik/doğa bilimleri için özgün sayısal araştırmaları kapsıyor. Resmî yazım kuralları ve gönderim dosyaları sayfası kontrol edildi. Ayrı makale template bağlantısı yayımlanmıyorsa bu eksiklik uydurma bir bağlantıyla doldurulmaz; mevcut resmî yazım kuralları uygulanır ve nihai gönderim günü tekrar kontrol edilir.

Bu aşamada NASE birinci, CUJAST ikinci hedeftir; nihai seçim danışmana aittir.

## 5. Kapanan önceki bulgular

- P1-01 teslim kanıtı: **KAPALI**.
- P1-02 çelişkili erişim/doğrulama beyanı: **KAPALI**.
- P1-03 ders dışı hedef dergiler: **KAPALI**.
- P1-04 makale iskeleti: **KAPALI**.
- P1-05 kaynak/tam metin belirsizliği: **BİLAL SPRINTİ İÇİN KAPALI**. Erişilemeyen veri artık doğrulanmış gibi sunulmuyor; L12 açık tam metin ayrıntıları yeniden doğrulandı. Algoritma denklemlerinin kodla birebir eşleşmesi ilgili algoritma sahiplerinin ayrı teknik kabul kriteridir.
- P1-06 bağımsız inceleme: **KAPALI**. Yapısal test, kaynak gerçekliği, matematiksel terminoloji ve küçük örnek Cmax hesabı bağımsız tekrarlandı.
- P1-07 dergi/şablon kontrolü: **KAPALI**. NASE resmî template bağlantısı ve bağlayıcı yazım kuralları doğrulandı; CUJAST'ta ayrı şablon bulunmaması olduğu gibi kaydedildi.
- Önceki Gantt veri bekleme durumu: **KAPALI**; resmî küçük örnekten 15 işlem yeniden hesaplandı.

## 6. Bilal teslimi için nihai karar

Bilal'in 18 Kasım ilk sprinti kapsamında açık **P0 veya P1 bulunmuyor**. Literatür matrisi, araştırma soruları, giriş taslağı, makale iskeleti, hedef dergi kısa listesi, kaynak denetimi ve 5×3 Gantt verisi bir sonraki ekip adımında kullanılabilir.

Bu PASS kararı **projenin kodunun, beş algoritmanın veya 450 nihai koşunun tamamlandığı anlamına gelmez**. `src/`, `tests/`, `data/taillard/` ve `results/` aşamaları kendi sorumlularının kabul kapılarından ayrıca geçecektir.
