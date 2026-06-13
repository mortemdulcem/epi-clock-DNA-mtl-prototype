Lambda mimarisi (Lambda architecture) ilkelerine göre, Ham Veri Deposu (Raw Data Storage) bileşeni değiştirilemez (immutable) olmalıdır. Dolayısıyla yeni veriler mevcut veriyi değiştirmemeli, sadece veri kümesine eklenmelidir (append). Veriler, ham verilerin Toplu Görünümlere (Batch Views) dönüştürülmesi için yığın (batch) işlemlerle okunacaktır. Bu amaçlar için, güvenle bir Dağıtık Dosya Sistemi (Distributed File System) seçebiliriz.

### Alternatif – Elenme Gerekçesi  
**NoSQL Veritabanı (NoSQL Database)**

NoSQL veritabanları (özellikle sütun aileli (column-family) ve belge odaklı (document-oriented) olanlar) günlük (log) gibi ham verileri depolamak için kullanılabilse de, bu durum kaynak tüketiminde (çoğunlukla önbellekleme mekanizmalarından dolayı bellek tüketimi) gereksiz ek yük oluşturacak ve şema yapılandırma ve evrimleştirme ihtiyacı nedeniyle bakımını zorlaştıracaktır.

**Analitik İlişkisel Veritabanı Yönetim Sistemi (Analytic RDBMS)**

Tüm analitik yeteneklere sahip ilişkisel veritabanları, ilişkisel modele dayanır ve tablolar ile satırlar oluşturur. Bu, karmaşık sorguları yürütmek için çok iyi çalışsa da, yarı-yapısal günlüklerin ham biçimde depolanması için hem kullanışsız hem de pahalı bir seçenektir.  

---

## 5.3 Tasarım Süreci

### Tasarım Kararları ve Konumu  
Statik ve Anlık (Ad Hoc) Toplu Görünümler (Batch Views) bileşenleri için aynı Etkileşimli Sorgu Motoru (Interactive Query Engine) ailesini seç

#### Gerekçe ve Varsayımlar

Önceki yinelemede belirttiğimiz gibi, Toplu Görünümler (Batch Views) bileşeni, iki kullanım senaryosunu desteklemek üzere Statik ve Anlık (Ad Hoc) Toplu Görünümler olarak ayrıştırılmıştır: statik raporların üretilmesi (UC-3, UC-6) ve anlık sorgulamayı (ad hoc querying) desteklemek (UC-4). Ana tasarım kararı, hem Statik hem de Anlık Toplu Görünümler için aynı teknoloji ailesini kullanmaktır; yani Etkileşimli Sorgu Motoru (Interactive Query Engine). Bu motorlar, Dağıtık Dosya Sistemi üzerinde depolanan veriler üzerinde analitik veritabanı (analytic database) yetenekleri sağlar (dolayısıyla bu teknoloji ailesi de örtük olarak seçilmiş olur). Yeterince hızlı bir teknoloji seçersek, bu teknoloji her iki bileşen için de kullanılabilir. Tek bir teknoloji ailesi kullanmanın faydası, raporlama ve veri sorgulama için ayrı depolama teknolojilerine ihtiyaç duymamamızdır.

### Alternatif – Elenme Gerekçesi  
**NoSQL Veritabanı (NoSQL Database)**

Statik Toplu Görünümler (Static Batch Views) bileşeni, veriyi sorgulama ve bir raporlama sistemi (kurumsal BI aracı) içinde gösterme için hazır bir biçimde depolayan Özelleştirilmiş Görünüm (Materialized View) deseni ile uygulanabilir. NoSQL Veritabanı ailesi, iyi ölçeklenebilirlik sağlaması ve açık kaynak olması nedeniyle sıkça bu amaçla kullanılır; böylece QA-8’in (yaklaşık 90 TB birikimli veri) ve CON-1’in (açık kaynak lisansı) gereksinimlerini karşılar.

Ancak NoSQL veritabanları, anlık (ad hoc) sorgular için veri ambarı (data warehouse) olarak kullanılmak üzere iyi birer seçenek değildir; çünkü analitik amaçlar için tasarlanmamışlardır. Bu amaçla kullanılabilseler de, bu kullanım önemli performans cezalarına yol açacaktır.

Bu alternatif bu nedenle elenmiştir; çünkü yalnızca Statik Toplu Görünümler için kullanılabilir, Anlık Toplu Görünümler için ise etkisizdir.

**Analitik İlişkisel Veritabanı Yönetim Sistemi (Analytic RDBMS)**

Anlık (ad hoc) sorgular, SQL-benzeri bir arayüzün desteklediği herhangi bir sorgu olabilir. Sorgu sonucunun “insani” bir sürede (QA-5) döndürülmesi gerekir. Tanımlanan senaryo, bir veri ambarının tam olarak kullanıldığı senaryodur. Bu desen, genellikle Kimball veya Inmon tasarım yaklaşımlarını izleyen Analitik RDBMS teknolojileriyle uygulanır. Aynı anda, yaklaşık 90 TB birikimli veri ölçeklenebilirlik gereksinimini karşılamak oldukça maliyetli olacaktır. MPP (Massively Parallel Processing) analitik veritabanlarındaki terabayt başına maliyet, aynı miktar veri için bir NoSQL veritabanı veya bir dağıtık dosya sisteminden (örneğin Hadoop) anlamlı derecede daha yüksektir (30 kata kadar).

### Tasarım Kararları ve Konumu  
Analitik RDBMS alternatifini ele

#### Gerekçe ve Varsayımlar

Bu alternatif elenmiştir; çünkü hem Statik hem de Anlık Toplu Görünümler için kullanılabilse bile, bu aileyle ilişkili teknolojiler (açık kaynak) Hadoop-tabanlı alternatiflere göre maliyetlidir.

---

### Tasarım Kararları ve Konumu  
Görünümlerin Ön Hesaplama (Precomputing) bileşenleri için Veri İşleme Çatısı (Data Processing Framework) kullan

#### Gerekçe ve Varsayımlar

Ham Veri Deposu (Raw Data Storage) ve Toplu Görünümler (Batch Views) için Dağıtık Dosya Sistemi ailesini zaten seçtiğimize göre, bir sonraki adım Ham Veri Deposu’ndan Toplu Görünümlerde kullanılan formata veri dönüşümü sağlayacak bir çözüm seçmektir.

Karar, Veri İşleme Çatısı’nı (Data Processing Framework) seçmektir; çünkü bu teknoloji ailesi, daha hızlı geliştirme ve daha iyi sürdürülebilirlik sağlayan soyutlamalar kullanarak veri işleme boru hatları (data processing pipelines) oluşturmaya olanak verir.

### Alternatif – Elenme Gerekçesi  

**Dağıtık Hesaplama Motoru (Distributed Computing Engine)**

Çoğu Dağıtık Hesaplama Motoru teknolojisi yığın (batch) veri işleme için tasarlanmıştır, ancak düşük seviye ilkelere (örneğin MapReduce görevleri yazmak) dair önemli düzeyde bilgi gerektirir.

**Olay Akışı İşleyici (Event Stream Processor)**

Bu, gerçek zamanlı akış işlemeye yönelik tasarlanmıştır; yığın (batch) işlemler için etkisizdir.

---

### Tasarım Kararları ve Konumu  
Gerçek Zamanlı Görünümler (Real-Time Views) bileşeni için Dağıtık Arama Motoru (Distributed Search Engine) seç

#### Gerekçe ve Varsayımlar

Gerçek Zamanlı Görünümler bileşeni, son günlükler üzerinde tam metin araması yapmak ve gerçek zamanlı izleme verileriyle bir operasyonel gösterge panelini beslemekten sorumludur (UC-1, UC-2). Dağıtık Arama Motoru (Distributed Search Engine), tam olarak bu tür amaçlara hizmet eden bir teknoloji ailesidir.

### Alternatif – Elenme Gerekçesi  
**NoSQL Veritabanı (NoSQL Database)**

Bazı NoSQL veritabanları anahtar kelime araması veya metin araması sağlar, ancak bunlar, gövdeleme (stemming) ve konum tabanlı arama (geolocation) gibi metin işleme özellikleri de sunan arama motorları kadar güçlü ve hızlı değildir.

**Analitik İlişkisel Veritabanı Yönetim Sistemi (Analytic RDBMS)**

Bazı veritabanları (örneğin MS SQL Server) tam metin arama yetenekleri sağlar; ancak genişletilebilirlik, bakım ve maliyet açılarından daha az tercih edilirler.

**Dağıtık Dosya Sistemi ve Etkileşimli Sorgu Motoru  
(Distributed File System and Interactive Query Engine)**

Bu yaklaşım, geçmiş (historical) yığın verileri için iyi çalışır; ancak veriyi depolama ve işleme gecikmesi, gerçek zamanlı veriler için çok yüksek olacaktır.

---

### Tasarım Kararları ve Konumu  
Sistemin dağıtımını Puppet betikleriyle otomatikleştir

#### Gerekçe ve Varsayımlar

Puppet betikleri, hem Özel Bulut (Private Cloud, örn. VMware) hem de Genel Bulut (Public Cloud, örn. AWS) dağıtımları için kullanılabilir. Bu, CON-3’ün karşılanmasını destekler. Puppet, dağıtım sürecini otomatikleştirmenin yanı sıra bir sistemin yapılandırmasını yönetmeye de olanak verir. Birçok popüler açık kaynak teknolojinin dağıtımını otomatikleştirmek için Puppet topluluğu tarafından yazılmış ön tanımlı betiklerden oluşan bir kütüphane vardır.

> **💬 Çevirmen notu:** Puppet, altyapıyı kod olarak (Infrastructure as Code, IaC) yönetmeye olanak veren, yaygın bir yapılandırma yönetim aracıdır.

---

## 5.3.3.4 Adım 5: Mimari Bileşenleri Örnekle, Sorumlulukları Yükle ve Arayüzleri Tanımla

Bu yinelemede, daha önce seçilen teknoloji aileleriyle belirli teknolojileri ilişkilendirerek örnekleme (instantiation) yapılmaktadır. Göz önünde bulundurulan ve alınan örnekleme tasarım kararları aşağıdaki tabloda özetlenmiştir:

| Tasarım Kararı ve Konumu | Gerekçe |
| --- | --- |
| Veri Akışı (Data Stream) bileşeni için Veri Toplayıcı (Data Collector) ailesinden Apache Flume kullan | İlk aday teknoloji olarak Apache Flume’u seçeceğiz. Çalışma zamanında sadece yapılandırma güncellenerek yeni veri kaynakları eklenmesini sağlayan QA-9’u (yeni veri kaynaklarının sadece bir yapılandırma güncellemesiyle eklenmesi) desteklemek için gerekli yapılandırılabilirliği sağlar. |

### Alternatif – Elenme Gerekçesi  
**Logstash veya Fluentd**

*(devam edecek)*
