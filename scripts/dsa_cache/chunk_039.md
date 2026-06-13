### Gerekçe

Şekil 5.2’de gösterilen Lambda mimarisi (Lambda architecture), bir referans mimaridir ve bir veri akışının işlenmesini iki akışa ayırır: gerçek zamanlı veriye erişimi destekleyen “hız katmanı (speed layer)” (UC-1, UC-2, UC-5) ve “batch” ile “serving” katmanlarını bir araya toplayan ve tarihsel veriye erişimi destekleyen katman (UC-3, UC-4, UC-6). (Lambda mimarisinin yaratıcıları bunlara “katman (layer)” der, ancak bu, terimin daha önceki ve daha standart kullanımlarından farklıdır; önceki kullanımlar tipik olarak modüllerin bir gruplamasına karşılık gelir. Burada katmanlar, çalışma zamanı bileşenlerinin (runtime components) gruplarıdır.)

Batch katmanı değiştirilemez (immutable) ilişkisel olmayan tekniklere dayanırken, hız katmanı sıkı gerçek zamanlı işleme gereksinimlerini desteklemek için akış (streaming) tekniklerine dayanır. Buradaki değiştirilemezlik, verinin toplandığında güncellenmediği veya silinmediği anlamına gelir; yani yalnızca ekleme yapılabilir (append-only). Tüm veri toplandığı için hiçbir veri kaybolamaz ve makine veya insan hatası tolere edilebilir. Örneğin, bir yazılım mühendisi işleme veya görüntüleme mantığında zaman zaman bir hata yaparsa, bu sorun çözüldüğünde toplanan veri kullanılarak görünümler (views) baştan tekrar oynatılabilir ve yeniden hesaplanabilir.

Okuyucunun rahatlığı için Lambda mimarisinin temel kavramlarını beş adım üzerinden açıklıyoruz:

1. Birden çok veri kaynağından alınan tüm veriler, işlenmek üzere veri akışı (data stream) bileşeni aracılığıyla hem batch katmanına hem de hız katmanına yönlendirilir.
2. Batch katmanı, master veri kümesi (master dataset) bileşenine karşılık gelen bir “iniş bölgesi” (landing zone) olarak davranır (değiştirilemez, yalnızca ekleme yapılan ham veri kümesi) ve ayrıca batch görünümlerinde kullanılacak bilgileri önceden hesaplar.
3. Serving katmanı, çoğunlukla raporlama çözümleri tarafından gerekli olan düşük gecikmeli sorgulama için optimize edilmiş, önceden hesaplanmış ve birleştirilmiş (aggregated) görünümler içerir.
4. Hız katmanı, batch işlemenin yüksek gecikmesi nedeniyle serving katmanında bulunmayan gerçek zamanlı görünümler (real-time views) aracılığıyla en son veriyi işler ve erişilebilir kılar.
5. Sistem içindeki tüm veri, ister tarihsel ister yeni olsun, sorgulanabilir durumdadır ve bu, Lambda mimarisinin temel ilkesini ifade eder: query = function (batch data + real-time data).

Paralel akışlar “karmaşıklık yalıtımı (complexity isolation)” sağlar; yani her bir akışın tasarım kararları, geliştirilmesi ve icrası bağımsız olarak yapılabilir. Bunun hata toleransını (fault tolerance), ölçeklenebilirliği (scalability) ve değiştirilebilirliği (modifiability) artırdığı gösterilmiştir (bkz. Tablo 5.1).

Şekil 5.3, bu alternatifler arasındaki mimari ödünleşimleri (architectural tradeoff) gösterir ve referans mimariler arasındaki farkları dört nitelik boyutu açısından ortaya koyar: ölçeklenebilirlik, ad hoc analiz desteği, yapılandırılmamış veri işleme yetenekleri ve gerçek zamanlı analiz yetenekleri.

Şekil 5.3’ün gösterdiği üzere, Lambda mimarisi, ölçeklenebilirlik ve ad hoc analiz arasında en iyi ödünleşimi sağlar.

---

### Tasarım Kararı ve Yeri  
Sistem içindeki tüm elemanlar için hata toleransı kullan ve “tekil hata noktası yoktur (no single point of failure)” ilkesini uygula

#### Gerekçe

Hata toleransı, çoğu Büyük Veri (Big Data) teknolojisi için artık standart hâle gelmiştir ve Lambda mimarisi, yukarıda belirtildiği gibi, sağlam ve hata toleranslı bir sistem kurmak için bir dizi tasarım kararını zaten ima eder.

Bununla birlikte, sonraki tüm tasarım ve dağıtım (deployment) kararlarında, tüm aday teknolojilerin, hata toleranslı yapılandırmalar sağlayarak ve “tekil hata noktası yoktur (no single point of failure)” ilkesine uyarak QA-10 gereksinimini destekleyeceğinden emin olmamız gerekecektir.

---

### Alternatifler ve Elenme Nedenleri

| Alternatif            | Elenme Nedeni |
|-----------------------|---------------|
| Geleneksel ilişkisel (traditional relational) | Bu referans mimarisi, karmaşık ad hoc okuma sorguları için son derece verimli kabul edilen geleneksel ilişkisel model ilkelerine ve SQL-tabanlı VTYS’lere (DBMS) dayanır. Ancak ölçeklenebilirlik ve gerçek zamanlı işleme sınırlamaları nedeniyle en az uygun alternatiftir. |
| Genişletilmiş ilişkisel (extended relational) | Bu referans mimarisi tamamen ilişkisel model ilkelerine ve SQL-tabanlı VTYS’lere dayansa da, ölçeklenebilirlik ve genişletilebilirliği artırmak için yoğun biçimde büyük ölçekli paralel işleme (massive parallel processing, MPP) ve bellek içi (in-memory) teknikler kullanır. Yüksek maliyeti ve gerçek zamanlı işleme sınırlamaları nedeniyle daha az uygundur. |
| Saf ilişkisel olmayan (pure nonrelational) | Bu referans mimarisi, ilişkisel model ilkelerine dayanmaz. Sıklıkla NoSQL ve MapReduce gibi teknikler üzerine kuruludur ve yarı yapılandırılmış (semistructured) ve yapılandırılmamış veriyi işleme konusunda etkilidir. Bu alternatif, maliyet ekonomisi ve ölçeklenebilirlik açısından hedefe daha yakın olsa da ad hoc analiz sınırlıdır. |
| Veri rafinerisi (data refinery) | İlişkisel olmayan bir bileşen, yarı yapılandırılmış/yapılandırılmamış veriyi arıtmak için bir extract–transform–load (ETL) süreci yürütür ve temizlenmiş hâlini daha ileri analiz için bir veri ambarına (data warehouse; ilişkisel veritabanı) yükler. Bu çözüm için, yüksek maliyeti ve gerçek zamanlı işleme yetenekleri açısından önemli eksiklikleri nedeniyle daha az uygundur. |

---

## 5.3 Tasarım Süreci

### BATCH Katmanı – SERVING Katmanı – SPEED Katmanı

(Şekil 5.2 Lambda Mimarisi’ni göstermektedir; metin içinde anlatıldığından şekil içeriği ayrıca çevrilmemiştir.)

> **💬 Çevirmen notu:** Şekil 5.3’teki diyagram, metindeki nitelik boyutlarını (ölçeklenebilirlik, ad hoc analiz, yapılandırılmamış veri işleme, gerçek zamanlı analiz) eksenler ve renklerle karşılaştırmalı olarak gösteriyor; metindeki açıklama bu görseli sözel olarak özetlemektedir.

---

## 5.3.2.4 Adım 5: Mimari Elemanları Örnekle, Sorumlulukları Ata ve Arayüzleri Tanımla

Örnekleme (instantiation) ile ilgili ele alınan ve verilen tasarım kararları aşağıdaki tabloda özetlenmiştir.

### Tasarım Kararı ve Yeri  
Sorgu ve Raporlama (Query and Reporting) bileşenini, sürücülerle (drivers) ilişkilendirilmiş iki alt bileşene böl

#### Gerekçe

Lambda mimarisindeki Sorgu ve Raporlama bileşeni (Query and Reporting element), aşağıdaki iki alt bileşene ayrılmıştır. Bu alt bileşenler, ilgili sürücülerle şu şekilde ilişkilendirilir:

- Kurumsal BI aracı (Corporate BI tool) (UC-3, UC-4, QA-4, QA-5, CON-2)  
- Gösterge paneli/görselleştirme aracı (Dashboard/visualization tool) (UC-1, UC-2, QA-2, QA-3)

Bu ayrım, alana (domain) ilişkin bilgi ve araçların kullanılabilirliği tarafından yönlendirilmiştir. Rehber niteliğindeki gerekçe, uygun teknolojileri seçmede esnekliğe sahip olmaktır — bu kullanım senaryalarının, kısıtların ve kalite niteliklerinin (quality attributes) tümünü karşılayacak tek bir “evrensel” araç olması mümkün değildir. Bu nedenle, bize daha fazla tasarım seçeneği sağlaması beklenen bir “sorumluluk ayrımı (separation of concerns)” yapmayı seçiyoruz.

“Standart” Lambda mimarisinden bir diğer fark da, sorgu sonuçlarını birleştirmeye ihtiyaç duymayabileceğimizdir: Kullanım senaryolarımıza göre, sorgular batch görünümler ve gerçek zamanlı görünümler için bağımsız olarak çalıştırılabilir.

---

### Tasarım Kararı ve Yeri  
Ön-Hesaplama (Precomputing) ve Batch Görünümleri (Batch Views) bileşenlerini, Ad Hoc ve Statik Görünümlerle ilişkilendirilmiş alt bileşenlere böl

*(Bu tablonun devamı orijinal metinde sürmektedir; burada karar başlığı verilmiş, gerekçe metni ise bir sonraki parçada gelecektir.)*

---

### Tasarım Kararı ve Yeri  
Master Dataset’in anlamını ve adını Ham Veri Deposu (Raw Data Storage) olarak değiştir

*(Bu karar için de gerekçe, metnin devamında sunulacaktır.)*
