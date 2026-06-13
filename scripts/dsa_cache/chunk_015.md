Dağıtık Dosya Sistemi (Distributed File System)

CassandraFS  
Riak  

Anahtar-Değer (Key-Value)

Redis  
Berkeley DB  
MongoDB  

Belge Yönelimli (Document-Oriented)

CouchDB  

NoSQL Veritabanı (NoSQL Database)

HBase  

Sütun-Ailesi (Column-Family)

Veri Depolama (Data Storage)

Cassandra  
Neo4J  

Graf Yönelimli (Graph-Oriented)

OrientDB  
HP Vertica  
Teradata  

MPP Analitik İlişkisel Veritabanı (MPP Analytic RDBMS)

MS PDW  
Amazon Redshift  

Analitik İlişkisel Veritabanı (Analytic RDBMS)

MS SQL Server  

Geleneksel Analitik İlişkisel Veritabanı (Traditional Analytic RDBMS)

Oracle RDBMS  
IBM DB2  

QlikView  
Microstrategy  

BI Platformu (BI Platform)

Tableau  
Tibco JasperSoft  
Pentaho  
Splunk  

Görselleştirme ve Raporlama (Visualization & Reporting)

Etkileşimli Gösterge Paneli (Interactive Dashboard)

Kibana  
Zoomdata  
D3.js  

Grafik Kütüphanesi (Graphic Library)

GoJS  
Highcharts  
Impala  

Etkileşimli Sorgu Motoru (Interactive Query Engine)

İşleme ve Analitik (Processing and Analytics)

Apache Hive (Stinger)  
Spark SQL  

Arama ve Sorgu (Search & Query)

Splunk  
Elasticsearch  

Dağıtık Arama Motoru (Distributed Search Engine)

Apache Solr  
Hadoop MapReduce  

Dağıtık Hesaplama Motoru (Distributed Computing Engine)

Apache Spark  
Apache Tez  
Apache Storm  

İşleme (Processing)

Olay Akışı İşleyici (Event Stream Processor)

Spark Streaming  
Apache Samza  
Amazon Kinesis  
Cascading  

Açıklama (Legend):  
Düz metin – bir teknoloji ailesi  
İtalik metin – belirli bir teknoloji

Veri İşleme Çatısı (Data Processing Framework)

Apache Crunch  
Apache Hive  
Amazon Pig  

ŞEKİL 2.10 Büyük Veri (Big Data) uygulama alanı için bir teknoloji aile ağacı

---

38. Bölüm 2—Mimari Tasarım

- **Destek (Support).** İyi destekleniyor mu? Teknoloji hakkında kapsamlı dokümantasyon var mı? Danışabileceğiniz geniş bir kullanıcı veya geliştirici topluluğu mevcut mu?
- **Öğrenme eğrisi (Learning curve).** Bu teknolojiyi öğrenmek ne kadar zor? Kuruluşunuzda bu teknolojide uzmanlaşmış kişiler var mı? Uygun eğitimler mevcut mu?
- **Olgunluk (Maturity).** Piyasaya yeni çıkmış, heyecan verici ama görece kararsız veya yeterince desteklenmeyen bir teknoloji mi?
- **Popülerlik (Popularity).** Görece yaygın bir teknoloji mi? Olumlu referanslar veya olgun kuruluşlarca benimsenmesi söz konusu mu? Bu teknolojiyi derinlemesine bilen kişileri işe almak kolay olacak mı? Etkin bir geliştirici topluluğu veya kullanıcı grubu var mı?
- **Uyumluluk ve entegrasyon kolaylığı (Compatibility and ease of integration).** Projede kullanılan diğer teknolojilerle uyumlu mu? Projeye kolayca entegre edilebilir mi?
- **Kritik kalite nitelikleri (quality attributes) için destek.** Performans gibi nitelikleri kısıtlıyor mu? Güvenli ve sağlam (robust) mı?
- **Boyut (Size).** Bu teknolojinin kullanımı, geliştirilen uygulamanın boyutu üzerinde olumsuz bir etki yaratacak mı?

Ne yazık ki bu soruların yanıtları her zaman kolay bulunamaz ve belirli bir teknolojinin seçimi, biraz araştırma yapmanızı ya da en nihayetinde seçim sürecine yardımcı olacak prototipler oluşturmanızı gerektirebilir. Bu ölçütler, toplam sahip olma maliyetiniz (total cost of ownership) üzerinde önemli bir etkiye sahip olacaktır.

## 2.6 Mimari Tasarım Kararları (Architecture Design Decisions)

Bu bölümün başında söylediğimiz gibi, tasarım karar verme sürecidir. Ancak bir karar verme eylemi, tek bir an değil, bir süreçtir. Deneyimli mimarlar, bir tasarım zorluğuyla karşılaştıklarında genellikle bir “aday” kararlar kümesi (Şekil 2.1’de gösterildiği gibi) oluştururlar; bu kümeden en iyi adayı seçer ve onu somutlaştırırlar. Bu “en iyi” adayı, deneyimlerine, kısıtlara veya prototipleme ya da benzetim (simulation) gibi bir tür analiz yaklaşımına dayanarak seçebilirler. Gerçekte mimar, çoğunlukla bir seçim yapar ve “at düşünceye kadar binmeye devam eder” — yani, bir karara bağlanır ve ancak bu karar projenin başarısını tehlikeye atıyor gibi göründüğünde onu tekrar ele alır. Bu kararların ciddi sonuçları vardır!

Anımsayın ki tasarımın erken safhalarında kararlar, aşağı yönde önemli sonuçlara sahip olacak en büyük ve en kritik seçimlere odaklanır: referans mimariler, temel teknolojiler (örneğin çatı (framework)lar) ve desenler (pattern). Referans mimariler, dağıtım desenleri (deployment pattern) ve diğer tür desenler geniş ölçüde tartışılmıştır — desenler ve desen dilleri (pattern language) üretimine ve doğrulanmasına adanmış çok sayıda kitap, web sitesi ve konferans vardır. Buna karşın,
