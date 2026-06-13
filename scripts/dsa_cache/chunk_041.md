Ham Veri Depolama (Raw Data Storage) bileşeni tanımlanmış ve sorumlulukları
belirlenmiştir. Hangi depolama teknolojisinin kullanılacağıyla ilgili ayrıntılı
kararlar henüz verilmemiştir.

---

# 5. Bölüm — Vaka Çalışması: Büyük Veri Sistemi

|                  | Durum              |
|------------------|--------------------|
| CRN-2            | Ele Alınmadı       |
| 5.3.3            |                    |
| Kısmen Ele Alındı|                    |
| Tamamen Ele Alındı |                 |

## Yineleme Sırasında Alınan Tasarım Kararları

**QA-8**

Ad Hoc ve Statik Toplu Görünümler (Ad Hoc and Static Batch Views) bileşenleri
tanımlanmış ve sorumlulukları belirlenmiştir. Hangi depolama teknolojilerinin
kullanılacağıyla ilgili ayrıntılı kararlar henüz verilmemiştir.

**QA-10**

Sistem bileşenlerini gerçekleştirmek için seçilen tüm teknolojilerin, hata toleransı
(fault tolerance) yapılandırması sağlayarak ve tekil hata noktası (single point of
failure) içermeyerek QA-10’u desteklemesine karar verilmiştir.

**CON-2**

Kurumsal BI Aracı (Corporate BI Tool) bileşeni tanımlanmıştır. Bu kısıtın nasıl
karşılanacağıyla ilgili ayrıntılı kararlar henüz verilmemiştir.

**CRN-1**

Sistemin genel mantıksal yapısı oluşturulmuş, ancak fiziksel yapı hâlâ
tanımlanmalıdır.

Bu adımda ilgili bir karar alınmamıştır.

---

## Yineleme 2: Teknolojilerin Seçimi

Bu bölüm, tasarım sürecinin ikinci yinelemesinde, nitelik temelli tasarımın (Attribute-Driven Design, ADD) her adımında gerçekleştirilen
etkinliklerin sonuçlarını sunmaktadır.

Teknoloji seçimleri çoğu zaman sistem mimarisini etkiler; bu da mimari tasarımın
en erken aşamalarında teknolojileri seçmemiz gerektiği anlamına gelir. Teknoloji
seçimi, teknoloji ailelerinin belirlenmesi ve seçilmesiyle başlar; bu aileler daha
sonra belirli teknolojilerle somutlaştırılır. Teknoloji aileleriyle başlamak, belirli
teknolojileri birbirleriyle değiştirilebilir kılmamıza olanak tanır ve böylece tedarikçi bağımlılığından (vendor lock-in) kaçınmak için doğru düzeyde teknoloji
bağımsızlığını (technology agnosticism) koruruz (sonuç olarak gelecekte bir teknolojiyi daha iyisiyle değiştirme riski ve maliyeti azalır).

Bu yinelemede, Büyük Veri (Big Data) “greenfield” sistemleri tasarlarken
optimal yapıtaşlarını seçmemize yardımcı olacak bir teknoloji ağacı göstereceğiz.

---

## 5.3 Tasarım Süreci

### 5.3.3.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefinin Belirlenmesi

Bu yinelemenin hedefi, CRN-2’yi (ekibin Apache Büyük Veri ekosistemi
bilgisinden yararlanmak) ele almaktır; bunun için, özellikle CON-1’i (açık kaynak
teknolojileri tercih et) akılda tutarak, Bölüm 5.2’de tanımlanan sistem gereksinimlerini destekleyecek teknolojileri seçmek gerekir.

### 5.3.3.2 Adım 3: Ayrıntılandırılacak Bir veya Daha Fazla Sistem Bileşeninin Seçilmesi

Önceki yinelemede seçilen başvuru mimarisi (Lambda mimarisi), teknoloji ailelerinin ve bunlarla ilişkili belirli teknolojilerin seçimini kolaylaştıracak bileşenlere
ayrıştırılmıştı. Bu bileşenler şunları içerir:

- Veri Akışı (Data Stream)
- Ham Veri Depolama (Raw Data Storage)
- Ad Hoc ve Statik Görünümler Ön-hesaplama (Ad Hoc and Static Views Precomputing)
- Ad Hoc ve Statik Toplu Görünümler (Ad Hoc and Static Batch Views)
- Gerçek Zamanlı Görünümler (Real-Time Views)
- Gösterge Paneli/Görselleştirme Aracı (Dashboard/Visualization Tool)

### 5.3.3.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramının Seçilmesi

Bu yinelemede kullanılan tasarım kavramları, dışarıda geliştirilmiş bileşenlerdir.
Başlangıçta teknoloji aileleri seçilir ve ayrıntılandırılacak bileşenlerle ilişkilendirilir. Bir teknoloji ailesi, ortak işlevsel amaçlara sahip teknolojiler kümesini
temsil eder (bkz. Bölüm 2.5.5). Aile adları işlevlerini yansıtır ve bazı belirli
teknolojiler aynı anda birden fazla aileye ait olabilir; ancak bu tür bir sınıflandırma,
sonuçta daha az yeniden iş ve değişikliklere daha iyi hazırlık sağlayacak rasyonel
tasarım kararları almamıza yardımcı olur.

Yazılım endüstrisinin geçmişi, teknoloji uygulamalarının, onların aileleriyle temsil edilen örüntü (pattern) ve prensiplerden çok daha hızlı biçimde ortaya çıktığını,
evrildiğini ve ortadan kaybolduğunu göstermektedir.

Şekil 5.5, Büyük Veri alanı için aile gruplarını, teknoloji ailelerini (düz metinle)
ve bunlarla ilişkili belirli teknolojileri (italik metinle) göstermektedir. Bu
teknolojilerin birçoğu hakkında daha fazla ayrıntı, Smart Decisions Game’in
tasarım kavramları kataloğunda bulunabilir (bkz. “Further Reading” bölümü).

---

# 5. Bölüm — Vaka Çalışması: Büyük Veri Sistemi

## Büyük Veri Analitiği Kataloğu

**Veri Toplayıcı (Data Collector)**  
- Apache Flume  
- Logstash  
- Fluentd  

**Mesajlaşma (Messaging)**  
- Apache Kafka  

**Entegrasyon (Integration)**  
- RabbitMQ  

**Dağıtık Mesaj Aracısı (Distributed Message Broker)**  
- Amazon SQS  
- Apache ActiveMQ  

**ETL/ELT**  
- StreamSets  

**ETL/Veri Entegrasyon Motoru (ETL/Data Integration Engine)**  
- Talend  
- Informatica  

**Dağıtık Dosya Sistemi (Distributed File System)**  
- HDFS  
- CassandraFS  
- Riak  

**Anahtar-Değer (Key-Value)**  
- Redis  
- Berkeley DB  

**Belge Yönelimli (Document-Oriented)**  
- MongoDB  
- CouchDB  

**NoSQL Veritabanı (NoSQL Database)**  
- HBase  

**Sütun Ailesi (Column-Family)**  
- Cassandra  

**Graf Yönelimli (Graph-Oriented)**  
- Neo4J  
- OrientDB  

**MPP Analitik İlişkisel VTYS (MPP Analytic RDBMS)**  
- HP Vertica  
- Teradata  
- MS PDW  
- Amazon Redshift  

**Analitik İlişkisel VTYS (Analytic RDBMS)**  
- MS SQL Server  

**Geleneksel Analitik İlişkisel VTYS (Traditional Analytic RDBMS)**  
- Oracle RDBMS  
- IBM DB2  

**BI Platformu (BI Platform)**  
- QlikView  
- Microstrategy  
- Tableau  
- Tibco JasperSoft  
- Pentaho  
- Splunk  

**Görselleştirme ve Raporlama (Visualization & Reporting)**  
- İnteraktif Gösterge Paneli (Interactive Dashboard)  
  - Kibana  
  - Zoomdata  
- Grafik Kütüphanesi (Graphic Library)  
  - D3.js  
  - GoJS  
  - Highcharts  

**Etkileşimli Sorgu Motoru (Interactive Query Engine)**  
- Impala  
- Apache Hive (Stinger)  
- Spark SQL  

**Arama ve Sorgu (Search & Query)**  
- Splunk  
- Elasticsearch  

**Dağıtık Arama Motoru (Distributed Search Engine)**  
- Apache Solr  

**Dağıtık Hesaplama Motoru (Distributed Computing Engine)**  
- Hadoop MapReduce  
- Apache Spark  
- Apache Tez  

**İşleme (Processing)**  
- Olay Akışı İşleyici (Event Stream Processor)  
  - Apache Storm  
  - Spark Streaming  
  - Apache Samza  
  - Amazon Kinesis  

**Veri İşleme Çatısı (Data Processing Framework)**  
- Cascading  
- Apache Crunch  
- Apache Hive  
- Amazon Pig  

Açıklama (Legend):  
- Düz metin – teknoloji ailesi  
- İtalik metin – belirli teknoloji

**ŞEKİL 5.5** Büyük Veri analitiği tasarım kavramları kataloğuna bir örnek  
(Kaynak: Softserve)

---

## 5.3 Tasarım Süreci

BI Platformu (BI Platform) aile grubu ve ilişkili teknolojiler, bu tasarım
çalışmasında daha fazla ele alınmamaktadır; çünkü kurumsal BI aracı hedef
sistemden haricidir.

---

### Tasarım Kararları ve Konumu

#### Veri Akışı (Data Stream) bileşeni için Veri Toplayıcı (Data Collector) ailesini seç

**Gerekçe ve Varsayımlar**

Veri Toplayıcı (Data Collector), günlük (log) verilerini daha sonra kullanılmak
üzere toplayan, birleştiren ve aktaran bir teknoloji ailesi (ve mimari desen)dir.
Genellikle Veri Toplayıcı uygulamaları, popüler olay kaynakları ve hedefleriyle
bütünleşmek için hazır eklentiler (out-of-the-box plug-in) sunar.

Hedefler, bu yinelemede ele alınacak olan Ham Veri Depolama (Raw Data Storage)
ve Gerçek Zamanlı Görünümler (Real-Time Views) bileşenleridir.

**Alternatif** | **Elenme Nedeni**
--------------|--------------------
**ETL Motoru (ETL Engine)** | ETL motorlarının temel amacı, olay başına (per-event) işlemlerden ziyade toplu (batch) dönüşümler gerçekleştirmektir. Bu da gerçek zamanlı performans ve ölçeklenebilirlik ölçütlerini (QA-1, QA-2) karşılamayı son derece zor, hatta imkânsız hâle getirir.
**Dağıtık Mesaj Aracısı (Distributed Message Broker)** | Bu teknoloji ailesi tek başına Veri Akışı (Data Stream) bileşenini gerçekleştirmek için kullanılabilse de, genişletilebilirlik (QA-9) için daha az destek sunar ve bu nedenle veri toplayıcının tamamlayıcısı olarak kullanılmaya daha uygundur. Bu, örneğin Apache Flume (Veri Toplayıcı) ve Apache Kafka’nın (Dağıtık Mesaj Aracısı) birleşimi olan Flavka kullanılarak gerçekleştirilebilir.

#### Ham Veri Depolama (Raw Data Storage) bileşeni için Dağıtık Dosya Sistemi (Distributed File System) ailesini seç
