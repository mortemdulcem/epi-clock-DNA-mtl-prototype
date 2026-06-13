```mermaid
flowchart LR
    subgraph SPEED[HIZ KATMANI (SPEED Layer)]
        direction LR
        WSN[WebServer N<br/>(Veri Kaynağı)]
        WS2[WebServer 2<br/>(Veri Kaynağı)]
        NCN[netcat kaynağı<br/>(erişim)]
        NC2[netcat kaynağı<br/>(erişim)]
        FA[Flume Aracısı<br/>(Flume Agent)]
        MC1[Hafıza kanalı<br/>(Memory channel)]
        MC2[Hafıza kanalı<br/>(Memory channel)]
        ESsinkE[ES alıcısı (sink)<br/>(hata)]
        ES[(Elasticsearch)]
        HDFSs[HDFS alıcısı (sink)<br/>(erişim)]
        AvroAcc[avro alıcısı (sink)<br/>(erişim)]
        AvroErr[avro alıcısı (sink)<br/>(hata)]
        LB[LB + failover]
        HDFS[(HDFS)]

        WSN -->|erişim| NCN
        WS2 -->|erişim| NC2
        NCN --> FA
        NC2 --> FA
        FA --> MC1
        FA --> MC2
        MC1 -->|json| ESsinkE --> ES
        MC1 --> HDFSs --> HDFS
        MC2 --> AvroAcc
        MC2 --> AvroErr
        FA --> LB
    end
```

Açıklama:
- Düğümler arası veri akışı
- Aynı düğüm içindeki Flume bileşenleri arasındaki veri akışı

+ log ayrıştırma (log parsing)

---

Şekil 5.8 Üçüncü yinelemenin somut tasarım kararları

---

## 5.3 Tasarım Süreci

### 5.3.4.6 Adım 7: Geçerli Tasarımın Analizini Gerçekleştir ve Yinelemeyi Gözden Geçir  
Amaç ve Tasarım Amacına Ulaşım

Aşağıdaki Kanban tablosu, tasarım ilerlemesini ve yineleme sırasında verilen
kararları özetlemektedir. Bir önceki yinelemede tamamen ele alınmış olan sürücüler
(drivers) gösterilmemiştir.

|                      | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Verilen Tasarım Kararları |
|----------------------|--------------|-------------------|--------------------|----------------------------------------------|
| UC-1                 |              |                   |                    |                                              |
| UC-2                 |              |                   |                    |                                              |
| UC-3                 |              |                   |                    |                                              |
| UC-4                 |              |                   |                    |                                              |
| CRN-3                |              |                   |                    | Veri Akışı (Data Stream) elemanının iyileştirilmesi. Bu kullanım senaryolarına katılan diğer elemanlar hakkında hâlâ karar verilmesi gerekmektedir. |
| QA-1                 |              |                   | ✔                  | Flume yük dengelemeli (load-balanced), failover katmanlı (tiered) yapılandırma seçilmiştir. |
| QA-9                 |              |                   | ✔                  | Ham veriyi depolamak için Flume ve Avro formatının kullanılması. |
| QA-10                |              |                   | ✔                  | Flume yük dengelemeli, failover katmanlı yapılandırma seçilmiştir. Bu senaryoya katılan diğer elemanlar hakkında hâlâ karar verilmesi gerekmektedir. |
| CRN-1                |              |                   |                    | Flume toplayıcı (collector) ve depolama için katmanlar tanımlanmıştır. Bu yinelemede tanıtılmış yeni bir mimari konudur: veri modelleme ve kilit sistem elemanları için kavram kanıtlama (proof‑of‑concept) prototiplerinin geliştirilmesi. Bu noktada ilgili bir karar verilmemiştir. |

> **💬 Çevirmen notu:** “CRN” burada metnin önceki kısımlarında tanımlanmış mimari kaygı/konu (concern) kimlikleridir; tablo bir Kanban durum panosu olarak okunmalıdır.

---

### 5.3.5 Yineleme 4: Sunum Katmanının (Serving Layer) İyileştirilmesi

Bu bölümde, tasarım sürecinin dördüncü yinelemesinde, nitelik temelli tasarımın
(Attribute‑Driven Design, ADD) her adımında gerçekleştirilen etkinliklerin
sonuçlarını sunuyoruz.

Bu yinelemede iyileştirme için Batch Katmanı değil, Sunum Katmanı (Serving Layer)
seçilmiştir; çünkü gereksinimlere ulaşamama riski bu katman için daha yüksektir.
Bu katman doğrudan UC-3 ve UC-4 kullanım senaryoları ile, performans ve
ölçeklenebilirliğin kritik faktörler olduğu bir dizi kalite niteliği (quality attribute)
senaryosuna dahildir.

Önceki yinelemede olduğu gibi, tasarım etkinlikleri prototiplerin oluşturulmasını
içermektedir. Bu yinelemede, kullanıcı arayüzü (UI) prototipleri de oluşturulmuştur.
Bunun en az iki nedeni vardır:

- Kullanıcılardan erken geri bildirim alınmasını kolaylaştıracak, bu da
  gereksinimlerin güncellenmesine yardımcı olabilecektir.
- Veri görselleştirme senaryoları, çoğu zaman veri modelleme üzerinde etkiye
  sahiptir.

---

## 5.3 Tasarım Süreci

### 5.3.5.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu yinelemenin amacı, veri modelleme ve kilit sistem elemanları için kavram
kanıtlama (proof‑of‑concept) prototiplerinin geliştirilmesi (CRN-3) şeklinde yeni
tanımlanan mimari kaygıyı ele almak ve böylece tarihsel verinin analizi ve
görselleştirilmesiyle ilişkili birincil kullanım senaryolarını ve sistem gereksinimlerini
karşılamaktır. Bu kullanım senaryoları şunları içerir:

- UC-3
- UC-4

Bu kullanım senaryolarıyla ilişkili kalite niteliği senaryoları şunlardır:

- QA-4 (Performans)
- QA-5 (Performans)
- QA-7 (Ölçeklenebilirlik)
- QA-8 (Ölçeklenebilirlik)

### 5.3.5.2 Adım 3: İyileştirilecek Bir veya Daha Fazla Sistem Elemanını Seçme

Bu yinelemede iyileştirilen elemanlar, tarihsel veriyi destekleyen elemanlardır; bunlar
Sunum Katmanı (Serving Layer) elemanları olan Ad Hoc ve Statik Batch
Görünümlerini (Ad Hoc and Static Batch Views) içerir. Her iki tip eleman da aynı
teknolojiyi (Impala) kullandığından, bu yinelemede verilen kararlar her iki tür elemanı
da etkiler.

### 5.3.5.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı Seçme

Önceki yinelemede olduğu gibi, buradaki tasarım etkinlikleri, elemanlarla ilişkilendirilen
teknolojilerin yapılandırılmasını içermektedir. Bu nedenle yeni tasarım kavramları
seçilmemiştir ve tüm kararlar somutlama (instantiation) kategorisine aittir.

### 5.3.5.4 Adım 5: Mimari Elemanları Somutlaştırma, Sorumlulukları Atama ve Arayüzleri Tanımlama

Bu yinelemede, tasarım kavramları seçilen teknolojilerin en iyi uygulamalarına
(dayanarak) somutlaştırılır.

**Tasarım Kararı ve Yeri**

**Gerekçe ve Varsayımlar**

**Batch Görünümlerinde Impala için dosya formatı olarak Parquet seçilmesi**

Batch Görünümleri için bir dosya formatı seçme süreci, önceki yinelemede ham veri
depolama için bir format seçtiğimiz sürece benzerdir. Ancak veri kullanım senaryosu
biraz farklıdır. Önceki durumda konu, hızlı yazma, veriyi etkin biçimde depolama ve
veri formatlarını genişletme idi. Bu durumda odak, hızlı sorgulama üzerinedir (QA-4,
5 saniyeden kısa rapor yükleme; QA-5, 2 dakikadan kısa ad hoc sorgu yürütme
süresi); buna karşın ölçeklenebilirlik (QA-8, yaklaşık 90 TB birikimli veri) ve
genişletilebilirlik (QA-9, yeni veri kaynaklarının eklenmesi) sürücüleri hâlâ
geçerlidir. Mevcut tüm alternatifler içinde Parquet dosya formatı, bu gereksinimleri
karşılamak için en umut verici seçenek gibi görünmektedir.

---

**Tasarım Kararı ve Yeri**

**Gerekçe ve Varsayımlar**

**Batch Görünümlerinde Impala için dosya formatı olarak Parquet seçilmesi**

Parquet’te, sütun bazlı (columnar) bir yapı, bilgisayar kümeleri üzerinde ilişkisel
tabloları temsil eder ve ad hoc veri keşfi ve statik raporlar için önemli olan hızlı sorgu
işleme amacıyla tasarlanmıştır. Buna ek olarak Parquet, ikinci yinelemede etkileşimli
sorgu motoru için birincil teknoloji olarak seçtiğimiz Impala için optimize edilmiştir.
Son olarak, iyi bir sıkıştırma oranı sağlar ve yapının sonuna yeni sütunlar ekleyerek
bazı şema genişletmelerine izin verir.

**Alternatif**

**Elendiği Neden**

Metin dosyası  
(düz metin, CSV, XML,
JSON)

- Okumalar için yavaştır, özellikle de tekil sütunlar sorgulanırken.  
- Ayrıca, HDFS bloğu boyutundan büyük dosyalar depolanırken gerekli olan blok
  sıkıştırmayı desteklemez.

SequenceFile

- Okumalar için yavaştır, özellikle de tekil sütunlar sorgulanırken.

RCFile

- Hadoop’da benimsenen ilk sütun bazlı dosya formatıdır.  
- Şema evrimini (schema evolution) desteklemez.

ORCFile

- RCFile’dan daha iyi sıkıştırma ve daha hızlı sorgulama sunar, ancak şema evrimi
  açısından RCFile ile aynı dezavantajlara sahiptir.  
- Parquet ile karşılaştırıldığında sıkıştırma oranı daha iyidir, fakat sorgu performansı
  daha yavaştır.  
- Diğer önemli bir kısıt, Impala tarafından desteklenmemesidir.

Avro

- Avro her ne kadar Hadoop için en iyi çok amaçlı (multipurpose) depolama formatı
  olarak kabul edilse de, sorgu performansı RCFile, ORCFile ve Parquet gibi sütun
  bazlı formatlarla karşılaştırıldığında fark edilir derecede daha yavaştır.

---

## 5.3 Tasarım Süreci

**Tasarım Kararı ve Yeri**

**Gerekçe ve Varsayımlar**
