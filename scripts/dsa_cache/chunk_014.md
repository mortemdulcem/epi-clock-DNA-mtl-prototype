Taktikler (tactics), bir kalite niteliği (quality attribute) tepkisinin kontrolünü etkileyen tasarım kararlarıdır. Örneğin, düşük gecikmeye (latency) veya yüksek işlem hacmine (throughput) sahip bir sistem tasarlamak istiyorsanız, olayların (hizmet isteklerinin) gelişini düzenleyecek bir dizi tasarım kararı alabilirsiniz; bunun sonucu olarak, Şekil 2.8’de gösterildiği gibi belirli zaman kısıtları içinde üretilen tepkiler elde edersiniz.

Taktikler desenlerden (pattern) hem daha basit hem de daha ilkel (primitive) yapıdadır. Tek bir kalite niteliği tepkisinin kontrolüne odaklanırlar (elbette bu tepkiyi diğer kalite niteliği hedefleriyle değiştokuş edebilirler). Desenler ise buna karşılık, tipik olarak birden çok kuvveti—yani birden çok kalite niteliği hedefini—çözmeye ve dengelemeye odaklanır. Bir benzetmeyle, bir taktiğin atom, bir desenin ise molekül olduğunu söyleyebiliriz.

Taktikler, tasarım hakkında yukarıdan aşağıya düşünmeyi sağlayan bir yol sunar. Bir taktik sınıflandırması, bir kalite niteliğinin başarılmasıyla ilişkili bir dizi tasarım hedefiyle başlar ve mimara, içinden seçim yapabileceği bir dizi seçenek sunar. Bu seçeneklerin daha sonra desenler, çerçeveler (framework) ve kodun bir bileşimiyle somutlaştırılması gerekir.

Örneğin Şekil 2.9’da performans için tasarım hedefleri “Kaynak İsteğini Kontrol Et” (“Control Resource Demand”) ve “Kaynakları Yönet” (“Manage Resources”) şeklindedir. “İyi” performansa sahip bir sistem oluşturmak isteyen bir mimarın bu seçeneklerden bir veya daha fazlasını seçmesi gerekir. Yani, mimarın kaynak isteğini kontrol etmenin mümkün olup olmadığına ve kaynakları yönetmenin mümkün olup olmadığına karar vermesi gerekir. Bazı sistemlerde, sisteme gelen olaylar bir şekilde yönetilebilir, önceliklendirilebilir veya sınırlandırılabilir. Bu mümkün değilse mimar, kabul edilebilir zaman kısıtları içinde tepkiler üretmeye çalışırken sadece kaynakları yönetebilir. “Kaynakları Yönet” kategorisi içinde mimar, kaynakları artırmayı, eşzamanlılığı (concurrency) devreye sokmayı, hesaplamaların birden çok kopyasını sürdürmeyi, verinin birden çok kopyasını sürdürmeyi vb. seçebilir. Bu taktiklerin daha sonra somutlaştırılması gerekir. Örneğin mimar, eşzamanlılığı devreye sokmak (ve yönetmek) için Yarı-Senkron/Yarı-Asenkron (Half-Sync/Half-Async) desenini (bkz. Şekil 2.5) ya da hesaplamaların birden çok kopyasını sürdürmek için Yük Dengelemeli Küme (Load-Balanced Cluster) dağıtım desenini (deployment pattern) (bkz. Şekil 2.7) seçebilir.

3. Bölüm’de göreceğimiz gibi, taktiklerin ve desenlerin seçimi, birleştirilmesi ve uyarlanması, ADD sürecinin (nitelik temelli tasarım, Attribute-Driven Design, ADD) temel adımlarından bazılarıdır. Kullanılabilirlik (availability), birlikte çalışabilirlik (interoperability), değiştirilebilirlik (modifiability), performans, güvenlik (security), test edilebilirlik (testability) ve kullanılabilirlik (usability) kalite nitelikleri için mevcut taktik sınıflandırmaları vardır.

## 2.5.5 Haricen Geliştirilmiş Bileşenler

Desenler ve taktikler doğaları gereği soyuttur. Ancak bir yazılım mimarisi tasarlarken bu tasarım kavramlarını somutlaştırmanız ve gerçek uygulamaya daha yakın hale getirmeniz gerekir. Bunu başarmanın iki yolu vardır: Taktiklerden ve desenlerden elde edilen elemanları kodlayabilir ya da mimarideki bu elemanlardan bir veya daha fazlasıyla teknolojileri ilişkilendirebilirsiniz. Bu “satın al mı yoksa geliştir mi” (buy versus build) seçimi, bir mimar olarak vereceğiniz en önemli kararlardan biridir.

Teknolojileri, geliştirme projesinin parçası olarak oluşturulmadıkları için haricen geliştirilen bileşenler olarak kabul ederiz. Birkaç tür haricen geliştirilen bileşen vardır:

- **Teknoloji aileleri (technology families).** Bir teknoloji ailesi, ortak işlevsel amaçlara sahip belirli teknolojilerden oluşan bir grubu temsil eder. Belirli bir ürün veya çerçeve seçilene kadar yer tutucu (placeholder) olarak hizmet edebilir. Örneğin ilişkisel veritabanı yönetim sistemi (relational database management system, RDBMS) veya nesne yönelimli–ilişkisel eşleyici (object-oriented to relational mapper, ORM). Şekil 2.10, Büyük Veri (Big Data) alanındaki farklı teknoloji ailelerini (normal metinle) göstermektedir.
- **Ürünler (products).** Bir ürün (veya yazılım paketi), tasarlanmakta olan sisteme entegre edilebilen ve yalnızca küçük çaplı yapılandırma veya kodlama gerektiren, bağımsız bir işlevsel yazılım parçasını ifade eder. Örneğin, Oracle veya Microsoft SQL Server gibi bir ilişkisel veritabanı yönetim sistemi bir üründür. Şekil 2.10, Büyük Veri alanındaki farklı ürünleri (italik olarak) göstermektedir.
- **Uygulama çerçeveleri (application frameworks, framework).** Bir uygulama çerçevesi (veya kısaca çerçeve, framework), tekrar eden alan ve kalite niteliği kaygılarını, geniş bir uygulama yelpazesi boyunca ele alan genel işlevsellik sağlayan ve desenler ile taktiklerden oluşturulmuş, yeniden kullanılabilir bir yazılım elemanıdır. Dikkatle seçilip doğru şekilde uygulandıklarında çerçeveler, programcıların üretkenliğini artırır. Bunu, programcıların temel iş mantığına ve son kullanıcı değerine odaklanmasını sağlayarak, alttaki teknolojilere ve bunların gerçekleştirimlerine (implementation) odaklanma gereğini azaltarak yaparlar. Ürünlerin aksine, çerçeve işlevleri genellikle uygulama kodundan çağrılır veya bir tür yönelimli yaklaşım (aspect-oriented approach) kullanılarak “enjekte edilir”. Çerçeveler genellikle XML dosyaları veya Java’daki açıklamalar (annotations) gibi diğer yaklaşımlar üzerinden kapsamlı yapılandırma gerektirir. Bir çerçeve örneği, Java’da nesne yönelimli–ilişkisel eşleme (object-oriented to relational mapping) yapmak için kullanılan Hibernate’dir. Birkaç tür çerçeve vardır: Spring gibi tam yığın (full-stack) çerçeveler genellikle başvuru mimarileriyle (reference architecture) ilişkilidir ve başvuru mimarisinin farklı elemanları boyunca genel kaygıları ele alırken, JSF gibi tam yığın olmayan çerçeveler belirli işlevsel veya kalite niteliği kaygılarını ele alır.
- **Platformlar (platforms).** Bir platform, uygulamaları geliştirmek ve çalıştırmak için tam bir altyapı sağlar. Platform örnekleri arasında Java, .Net ve Google Cloud bulunur.

Haricen geliştirilen bileşenlerin seçimi, tasarım sürecinin temel bir yönü olup, sayılarının çokluğu nedeniyle zorlayıcı bir görev olabilir. Haricen geliştirilen bileşenleri seçerken göz önünde bulundurmanız gereken birkaç ölçüt şunlardır:

- **Ele aldığı problem.** Nesne yönelimli–ilişkisel eşleme için bir çerçeve gibi belirli bir şeyi mi, yoksa bir platform gibi daha genel bir şeyi mi ele alıyor?
- **Maliyet.** Lisans maliyeti nedir ve ücretsizse, destek ve eğitim maliyeti nedir?
- **Lisans türü.** Lisans, proje hedefleriyle uyumlu mu?

## 2.5 Tasarım Kavramları: Yapılar Oluşturmak için Yapı Taşları

### Büyük Veri Analitiği Kataloğu

- Apache Flume — **Veri Toplayıcı (Data Collector)**
- Logstash  
- Fluentd  
- Apache Kafka  

- **Mesajlaşma (Messaging)**  

- **Tümleştirme (Integration)**  

- RabbitMQ — **Dağıtık Mesaj Aracısı (Distributed Message Broker)**  
- Amazon SQS  
- Apache ActiveMQ  
- StreamSets  

- **ETL/ELT**  

- Talend — **ETL/Veri Tümleştirme Motoru (ETL/Data Integration Engine)**  
- Informatica  
- HDFS  

> **💬 Çevirmen notu:** Şekildeki liste, Büyük Veri ekosistemindeki teknoloji aileleri (ör. “Messaging”) ile bu ailelere ait ürünleri (ör. RabbitMQ, Kafka, Talend) birlikte göstermektedir; metin içinde anlatılan “teknoloji ailesi vs. ürün” ayrımı burada görselleştirilmektedir.
