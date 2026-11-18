# PFSP Araştırma Boşluğu ve Soru Adayları

**Sürüm 0.4 · 18.11.2026 · Literatür ve kapsam ön incelemesi PASS**

Bu taslak, [literatür matrisindeki](literature_matrix.md) 12 birincil yayına dayanır. Tarama, yöntem kaynaklarını ve seçilmiş PFSP çalışmalarını kapsıyor. Sorular, bu kaynaklarda görülen deney tasarımlarından türetildi. Güncel PFSP taramasına taklit öğrenmesi ve karma tamsayılı programlama ile yerel arama çalışmaları eklendi. Tarama hedeflidir ve yayın yeniliğini tek başına kanıtlamaz.

## 1. Eşit değerlendirme bütçesinde çözüm kalitesi ve kararlılık

**Soru.** DE, PSO, DBO, RIME ve NRBO, aynı random-key çözümleyici ve örnek başına eşit amaç fonksiyonu değerlendirme (FE) bütçesi altında hangi makespan kalitesi ve koşular arası kararlılığı sağlar?

**Dayanak.** Taillard, ortak örnekler ve tarihsel referans sınırları sağlar. Tsiftsoglou ve arkadaşları ortak kodlama ve iyileştirme adımları kullanır ve örnek başına 10 bağımsız koşu bildirir. Çalışmanın §5.2 bölümünde ortak bir FE sınırı belirtilmez. Bu gözlem, ilgili karşılaştırma bölümüyle sınırlıdır. [Taillard, L01](https://doi.org/10.1016/0377-2217(93)90182-M) · [Tsiftsoglou ve arkadaşları, L10, §5.2](https://www.mdpi.com/1999-4893/19/4/283)

Li ve arkadaşlarının yazar ön baskısı üç farklı tohum kullanıp makespan farkı ve süreyi raporlar. Bu tasarım, farklı hesaplama kaynaklarının ayrı kaydedilmesine örnektir. Bizim sorumuz üç örnekte ortak çözümleyici ve FE sınırı altında beş seçili yöntemin davranışıyla sınırlıdır. [Li ve ark., L11, ön baskı v2 §5.1](https://arxiv.org/html/2210.17178v2)

**Ölçüm.** ta001, ta011 ve ta021 üzerinde sırasıyla 20.000, 30.000 ve 40.000 FE sınırıyla algoritma başına en az 30 bağımsız koşu. Her örnekte en iyi ve medyan Cmax, referansa göre yüzde sapma (RPD) ve koşular arası yayılım raporlanır. Başlangıç popülasyonu değerlendirmeleri FE hesabına dahil edilir. Otuz tekrar aynı örnekteki değişkenliği ölçer. Örnek düzeyindeki yorum üç benchmark ile sınırlıdır.

## 2. Random-key çözümlemesinde tekrarlanan permütasyonlar

**Soru.** Değerlendirilen random-key vektörleri arasındaki kaç aday aynı iş sırasına çözülüyor ve bu oran algoritmaya ve aramanın aşamasına göre nasıl değişiyor?

**Dayanak.** Bean'in gerçek değerli anahtar gösteriminde, anahtarların göreli sırası çözümü belirleyebilir. Projedeki sıralama tabanlı çözümleyicide aynı göreli sırayı koruyan farklı vektörler aynı permütasyonu üretir. Bu özellikten hareketle, tekrarlanan iş sıralarının deneydeki sıklığını ölçmeyi öneriyoruz. [Bean, L03](https://doi.org/10.1287/ijoc.6.2.154)

**Ölçüm.** Ek kayıt açılırsa her FE için çözülmüş permütasyon kimliği ve değerlendirme sırası tutulur. Koşu ve FE dilimi başına benzersiz permütasyon sayısı ve önceki permütasyonları yeniden ziyaret etme oranı karşılaştırılır. Bu gözlemsel ölçüm temsilin nedensel etkisini belirlemek için tek başına yetersizdir. Nedensel yorum için kontrollü bir temsil karşılaştırması gerekir.

## 3. Ekleme veya takas aramasının ek katkısı

**Soru.** Seçilen bir yönteme eklenen permütasyon temelli yerel arama, aynı toplam FE sınırında yöntemin özgün sürümüne göre Cmax dağılımını nasıl değiştiriyor?

**Dayanak.** Tsiftsoglou ve arkadaşları hibrit yöntemlerde ortak komşuluk araması ve Path Relinking kullanır. Bu tasarım, projemizde yerel arama eklemesinin katkısını ölçmek için aynı yöntemin iki sürümünü karşılaştırma fikrine dayanak sağlar. [Tsiftsoglou ve arkadaşları, L10, §4.5 ve §5.2](https://www.mdpi.com/1999-4893/19/4/283)

**Ölçüm.** İsteğe bağlı ayrı deneyde özgün ve hibrit sürümler aynı başlangıç düzeni, örnekler ve toplam FE sınırıyla çalıştırılır. Komşu çizelge değerlendirmeleri FE'ye dahil edilir. Cmax ve yayılım yanında, bütçenin yerel aramada kullanılan payı kaydedilir.

## Makale kapsamı ve inceleme

Birinci soru, planlanan zorunlu deneyle yanıtlanabildiği için makalenin ana sorusu olarak öneriliyor. İkinci soru ek değerlendirme kayıtlarına, üçüncü soru ayrı deney koşularına bağlıdır. Üçünde de deney sonuçları açık.

Öz kontrol ve proje yöneticisinin talep ettiği bağımsız belge denetiminde soruların Cmax hedefine uygunluğu, kaynak atıfları ve ölçüm gereksinimleri kontrol edildi. Ana araştırma sorusu olarak 1. soru kullanılabilir. Modelin gerçek `problem.py` uygulaması, FE sayacı ve deney kayıtları bu literatür paketinde bulunmadığı için bunların kod düzeyindeki kabulü Şeref ve Tarık'ın teknik sprintlerinde ayrıca yapılacaktır; bu durum Bilal'in literatür teslimini bloke etmez.
