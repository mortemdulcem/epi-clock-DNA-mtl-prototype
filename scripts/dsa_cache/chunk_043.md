Logstash ve Fluentd oldukça popüler teknolojiler olmasına rağmen (belki de Flume kadar popülerdir) ve gereksinimleri karşılayacak olsalar da bir seçim yapmamız ve yalnızca birini belirlememiz gerekir. Flume’u seçmek için ek bir argüman, üç büyük Hadoop dağıtım satıcısı tarafından desteklenmesidir.

Bu teknoloji için, bu tür kullanım senaryosunu (QA-7, yaklaşık 60 TB ham veriyi depolama) desteklemek üzere tasarlanmış olduğundan, güvenle HDFS’i seçebiliriz. HDFS içinde verileri depolamak için kullanılabilecek metin dosyası (text file), SequenceFile, RCFile, ORCFile, Avro ve Parquet gibi bir dizi Hadoop dosya formatı da vardır. Dosya formatı seçimi üçüncü yinelemede ele alınacaktır.

| Alternatif   | Elenme Nedeni                                                                                     |
|-------------|----------------------------------------------------------------------------------------------------|
| CassandraFS | Bu teknoloji bir NoSQL veritabanına (Cassandra) bağımlıdır, oysa biz yalnızca dağıtık dosya sistemi (Distributed File System) seçtik. |

## 5.3 Tasarım Süreci

| Tasarım Kararı ve Konumu                                                                 | Gerekçe |
|------------------------------------------------------------------------------------------|--------|
| Hem Static Batch Views hem de Ad Hoc Batch Views elemanları için Interactive Query Engine ailesinden Impala kullan | Birincil aday teknoloji olarak Impala’yı seçiyoruz; rekabetçi performans sunuyor (her ne kadar en üst Analitik RDBMS platformları kadar hızlı olmasa da) ve kurumsal bir BI aracıyla bağlantı için bir ODBC arayüzü sağlıyor. Olası performans sorunlarını akılda tutarak, bu teknoloji seçiminin QA-4’ü (5 saniyeden az rapor yükleme süresi) ve QA-5’i (2 dakikadan az ad hoc sorgu yürütme süresi) karşıladığından emin olmak için sonraki yinelemelerde bir kavram kanıtlama (proof-of-concept) planlıyoruz. |
| Real-Time Views elemanları için Distributed Search Engine ailesinden Elasticsearch kullan. Dashboard/Visualization Tool elemanı için Interactive Dashboard ailesinden Kibana kullan. | Birincil aday teknoloji olarak Elasticsearch’ü seçiyoruz, çünkü aynı zamanda Kibana adında etkileşimli bir pano (interactive dashboard) şeklinde bir görselleştirme aracı da sunuyor. Kibana rol tabanlı güvenlik içermeyen görece basit bir pano olmasına rağmen (en azından bu çözüm tasarlanırken), UC-1, UC-2 kullanım senaryolarını ve QA-2’yi (1 dakikadan kısa periyotla otomatik yenilenen pano) karşılamaktadır. Elasticsearch ayrıca zaman serilerini sorgulamak, filtrelemek ve görselleştirmek için Kibana tarafından desteklenen alan‑özgül bir dil (domain-specific language) olan Query DSL sağlar. |
| Views Precomputing elemanları için Data Processing Framework ailesinden Hive kullan | Birincil aday teknoloji olarak Hive’ı seçiyoruz; ancak QA-4’ün (15 dakikadan az gecikme) karşılandığından emin olmak için sonraki bir yinelemede bir kavram kanıtlama prototipi oluşturmamız gerekecek. Hive, bu yinelemede zaten seçilmiş olan Impala gibi SQL benzeri bir dil sunar; böylece veri dönüşüm betiklerini yazarken veri ambarı tasarımcılarının yetkinliklerinden yararlanmamıza olanak tanır. |

| Alternatif          | Elenme Nedeni                                                                                                                                                      |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Apache Hive (Stinger) | Stinger girişimi sayesinde Hive performansını iyileştirmiş olsa da, sorguların hızı hâlâ Impala ve Spark SQL gibi diğer alternatiflere kıyasla yavaştır.            |
| Spark SQL           | Spark, Büyük Veri (Big Data) analitiği için çok umut verici bir teknolojidir, ancak bir BI aracı için SQL adaptörü rolünde kullanılması Spark SQL için en uygun kullanım olmayabilir. Dezavantajı, yüksek bellek gereksinimleri ve önbelleğe alınmamış veriler üzerindeki uzun sorgu süreleridir. Buna karşılık, Impala tam olarak bu senaryo için tasarlanmış ve optimize edilmiştir. |
| Splunk              | Splunk da indeksleme ve görselleştirme yetenekleri sunar (Elasticsearch ve Kibana’dan daha fazla özellik sağlar); ancak CON-1 bizi açık kaynaklı bir çözümü tercih etmeye yönlendirir. |
| Cascading veya Apache Pig | Mevcut geliştirme ekibinin SQL becerilerinden yararlanarak geliştirme süresini en aza indirmek için Cascading ve Pig’i eledik.                                         |

Veri, elemanlar arasında değiş tokuş edilirken, sonraki yinelemelerde daha kesin biçimde tanımlanacaktır. Bu verinin formatı, elemanlar arasındaki “arayüzleri (interfaces)” oluşturur.

### 5.3.3.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 5.6, somutlaştırma (instantiation) kararlarının sonucunu göstermektedir. Diyagramda görülen elemanların sorumlulukları, 1. yinelemenin 6. adımında tartışılmıştı. Aşağıdaki tablo, bu elemanlar için seçilen teknoloji ailelerini ve aday özgül teknolojileri özetlemektedir:

| Eleman                      | Teknoloji Ailesi               | Aday Teknoloji  |
|----------------------------|---------------------------------|-----------------|
| Data Stream                | Data Collector                  | Apache Flume    |
| Raw Data Storage           | Distributed File System         | HDFS            |
| Ad Hoc Views Precomputing  | Data Processing Framework       | Apache Hive     |
| Static Views Precomputing  | Data Processing Framework       | Apache Hive     |
| Ad Hoc Batch Views         | Interactive Query Engine        | Impala          |
| Static Batch Views         | Interactive Query Engine        | Impala          |
| Real-Time Views            | Distributed Search Engine       | Elasticsearch   |
| Dashboard/Visualization Tool | Interactive Dashboard         | Kibana          |

```text
BATCH Katmanı
Dağıtık dosya
sistemi (HDFS)

Raw Data
Storage

Data Collector
(Flume)

SERVING Katmanı
Data processing
framework (Hive)
Ad Hoc Views
Precomputing

Interactive Query
Engine (Impala)

Ad Hoc
Batch Views

Data processing
framework (Hive)

Interactive Query
Engine (Impala)

Static Views
Precomputing

Static
Batch Views

Kurumsal
BI Aracı

SPEED Katmanı

Data Stream

Distributed
Search Engine
(Elasticsearch)

Veri
Kaynakları

Real-Time Views
Gösterim:
Katman
Sınırı
Eleman
Sınırı

Veri Akışı
(yön belirtilmiş)
Sorgu Sonuç Akışı

Teknoloji ailesi + (Özgül teknoloji)

ŞEKİL 5.6 Yineleme 2 somutlaştırma tasarım kararları

(Kibana)

Dashboard/
Visualization
Tool
```

> **💬 Çevirmen notu:** Şekil 5.6, Lambda mimarisi benzeri üç katmanlı (Batch, Serving, Speed) bir Büyük Veri çözümündeki mantıksal elemanları, bunların veri akışlarını ve seçilen somut teknolojileri (Flume, HDFS, Hive, Impala, Elasticsearch, Kibana) üst üste gösteren bir mimari diyagramdır.

Bir sonraki tablo, seçilen teknolojilere bağlı olarak elemanlar arasındaki ilişkileri açıklamaktadır:

| Kaynak Eleman                 | Hedef Eleman                          | İlişki Açıklaması                                                                 |
|------------------------------|---------------------------------------|-----------------------------------------------------------------------------------|
| Data Sources (loglar)        | Data Stream (Flume)                   | Bir sonraki yinelemede tanımlanacaktır                                            |
| Data Stream (Flume)          | Raw Data Storage (HDFS)               | Flume HDFS sink üzerinden ağ iletişimi (push)                                     |
| Raw Data Storage (HDFS)      | Views Precomputing (Apache Hive)      | Hive tarafından kapsüllenmiş yerel ve ağ iletişimi                                |
| Views Precomputing (Apache Hive) | Batch Views (Impala)              | Hive tarafından kapsüllenmiş yerel ve ağ iletişimi                                |
| Batch Views (Impala)         | Corporate BI Tool                     | ODBC API üzerinden ağ iletişimi (pull)                                            |
| Data Stream (Flume)          | Real-Time Views (Elasticsearch)       | Flume Elasticsearch sink üzerinden ağ iletişimi (push)                            |
| Real-Time Views (Elasticsearch) | Dashboard/Visualization Tool (Kibana) | Elasticsearch API üzerinden ağ iletişimi (pull)                                |

### 5.3.3.6 Adım 7: Mevcut Tasarımın Analizini Yap ve Yineleme Hedefini ile Tasarım Amacının Gerçekleşmesini Gözden Geçir

Aşağıdaki Kanban tablosu, yineleme sırasında tasarım ilerlemesini ve alınan kararları özetlemektedir. Önceki yinelemede tamamen ele alınmış sürücülerin gösterilmediğine dikkat edin.

|                    | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Alınan Tasarım Kararları                                                                                                  |
|--------------------|-------------|-------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| UC-1               |             |                   |                    | Gerçek zamanlı izleme bilgilerini göstermek için Distributed Search Engine (Elasticsearch) ve Interactive Dashboard (Kibana) kullan. Bekleyen: İndeksleri modellemek ve bir UI taslak arayüz (mockup) oluşturmak. |
| UC-2               |             |                   |                    |                                                                                                                                               |
