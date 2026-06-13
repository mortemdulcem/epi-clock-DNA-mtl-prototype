Tam Metin Arama için son log verileri üzerinde Dağıtık Arama Motoru (Elasticsearch) ve Etkileşimli Gösterge Paneli (Kibana) kullan.
Beklemede: İndeksleri modelle ve bir kavram kanıtı (proof-of-concept) oluştur.

UC-3  
UC-4  

Batch Görünümler (Batch Views) elemanları için Etkileşimli Sorgu Motoru (Interactive Query Engine, Impala) kullan.
Beklemede: Veriyi ve tipik raporları modelle.
(devam ediyor)

---

### 5. Bölüm — Büyük Veri Sistemi Üzerine Vaka Çalışması

|                  | Not Addressed | Partially Addressed | Completely Addressed |
|------------------|---------------|---------------------|----------------------|
| **Bu Yineleme Sırasında Verilen Tasarım Kararları** |               |                     |                      |

UC-6  

Bu kullanım durumu (use case), mimari bakış açısından UC-3’e benzemesine rağmen, birincil olmadığı için bu yinelemede dışarıda bırakılmıştır.

QA-1  

Veri Akışı (Data Stream) elemanı için Veri Toplayıcı (Data Collector, Apache Flume) kullan.  
Beklemede: Konfigürasyon, kavram kanıtı (proof-of-concept) ve performans testleri.

QA-2  
QA-3  

Dağıtık Arama Motoru (Elasticsearch) ve Etkileşimli Gösterge Paneli (Kibana) kullan.  
Beklemede: Kavram kanıtı (proof-of-concept) ve performans testleri.

QA-4  

Statik Batch Görünümler (Static Batch Views) elemanı için Etkileşimli Sorgu Motoru (Impala) kullan.  
Beklemede: Veriyi modelle, kavram kanıtı (proof-of-concept) ve performans testleri.

QA-5  

Ad Hoc Batch Görünümler (Ad Hoc Batch Views) elemanı için Etkileşimli Sorgu Motoru (Impala) kullan.  
Beklemede: Veriyi modelle, kavram kanıtı (proof-of-concept) ve performans testleri.

QA-6  

Gerçek Zamanlı Görünümler (Real-Time Views) elemanı için Dağıtık Arama Motoru (Elasticsearch) kullan.  
Beklemede: Kapasite planlaması yap.

QA-7  

Ham Veri Depolama (Raw Data Storage) elemanı için Dağıtık Dosya Sistemi (Distributed File System, HDFS) kullan.  
Beklemede: Dosya formatını seç ve kapasite planlaması yap.

QA-8  

Batch Görünümler (Batch Views) için depolama katmanı olarak Dağıtık Dosya Sistemi (HDFS) kullan.  
Beklemede: Dosya formatını seç ve kapasite planlaması yap.

QA-9  

Veri Akışı (Data Stream) elemanı için Veri Toplayıcı (Apache Flume) kullan.  
Beklemede: Konfigürasyon ve kavram kanıtı (proof-of-concept).

QA-10  

Tüm sistem elemanlarında hata toleransı (fault tolerance) kullan.  
Beklemede: Stres testi.

QA-11  

Farklı ortamlar için dağıtım (deployment) sürecini otomatikleştirmek amacıyla Puppet betikleri kullan.

---

## 5.3 Tasarım Süreci

|                  | Not Addressed | Partially Addressed | Completely Addressed |
|------------------|---------------|---------------------|----------------------|
| **Bu Yineleme Sırasında Verilen Tasarım Kararları** |               |                     |                      |

CON-1  

Seçilen tüm teknolojiler açık kaynak (open source) olacaktır.

CON-2  

ODBC arayüzü ile Etkileşimli Sorgu Motoru (Impala) kullan.

CON-3  

Seçilen tüm teknolojiler, Puppet betikleri kullanılarak hem özel bulut (private cloud, VMware) hem de genel bulut (public cloud, AWS) ortamlarına dağıtılabilir.

CRN-1  

İlgili bir karar verilmemiştir.

CRN-2  

Apache Büyük Veri ekosisteminden gelen teknolojiler seçilmiş ve başvuru mimarisi (reference architecture) içindeki farklı elemanlarla ilişkilendirilmiştir.

---

## 5.3.4 Yineleme 3: Veri Akışı Elemanının İyileştirilmesi

Bu bölüm, tasarım sürecinin üçüncü yinelemesinde, nitelik temelli tasarım (Attribute-Driven Design, ADD) adımlarının her birinde gerçekleştirilen faaliyetlerin sonuçlarını sunar.  
Bu yinelemede verilen bazı tasarım kararları, salt kavramsal düzeyde ele alınamayacağı için bir kavram kanıtı (proof-of-concept) prototipi oluşturulmasını gerektirmektedir. Büyük Veri alanının genç olması ve teknolojilerin hızla evrilmesi nedeniyle, temel elemanlara yönelik kavram kanıtları, teknoloji risklerini (örneğin uyumsuzluk, düşük performans, tatmin edici olmayan güvenilirlik, vaat edilen özelliklerdeki kısıtlar) azaltmak ve tasarım ile geliştirme sürecinin erken bir aşamasında alternatiflere geçiş yapma seçeneğine sahip olmak için gereklidir. Bu da, daha sonra yapılacak yeniden işleme (rework) ihtiyacını önleyerek genel zaman ve bütçe tasarrufu sağlar.

### 5.3.4.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu yinelemenin amacı, Veri Toplayıcı (Data Collector) elemanı için kullanılacak teknoloji olarak Apache Flume’un seçimiyle ilişkili çeşitli kaygıları ele almaktır. Apache Flume, Şekil 5.7’de gösterilen gayriresmî diyagramda tasvir edilen bir başvuru yapısı—bir veri akışı modeli (data-flow model)—sağlar.  

Flume’un yapısındaki elemanlar şunlardır:

- Kaynak (source): Web sunucuları gibi haricî veri kaynakları tarafından kendisine iletilen olayları (event) tüketir.
- Kanal (channel): Kaynak tarafından alınan olayları depolar.
- Sink: Olayları kanaldan alır ve bunları haricî bir depoya (yani hedefe) yazar.

Apache Flume’un seçimi, ele alınması gereken birtakım özgül mimari kaygıları gündeme getirir:

- Haricî kaynaklardan veri alma mekanizmasının seçilmesi
- Kaynak (Source) elemanında kullanılacak belirli girdi formatlarının seçilmesi
- Olayların saklanacağı dosya veri formatının seçilmesi
- Olayların kanal içinde yönlendirilmesi (channeling) için kullanılacak mekanizmanın seçilmesi
- Veri Kaynağı (Data Source) elemanları için bir dağıtım topolojisinin (deployment topology) belirlenmesi

Bu özgül mimari kaygıların ele alınması, aşağıdaki kalite niteliklerinin (quality attributes) karşılanmasına katkı sağlayacaktır:

- QA-1 (Performans)
- QA-7 (Ölçeklenebilirlik)
- QA-9 (Genişletilebilirlik)
- QA-10 (Kullanılabilirlik / Erişilebilirlik)

### 5.3.4.2 Adım 3: İyileştirilecek Bir veya Daha Fazla Sistem Elemanını Seçme

Bu yinelemede odak, Flume’un yapısındaki elemanlar üzerindedir.

### 5.3.4.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı Seçme

Bu yinelemede kararların çoğu somutlaştırma (instantiation) ile ilgilidir; zira esas olarak Flume tarafından hâlihazırda tanımlanmış elemanların yapılandırılmasını içerirler. Seçime dayalı tek tasarım kararı, kullanılabilirlik (availability) ve performans kalite niteliklerini karşılamak için taktikler (tactics) seçmeyi içerir.

---

## 5.3 Tasarım Süreci (devam)

### Verilen Tasarım Kararları ve Konumu

**Karar:** Flume’u ajan/toplayıcı (agent/collector) konfigürasyonunda kullan. Ajanlar web sunucularıyla aynı yerde (co-located) konuşlandırılır ve toplayıcı (collector) Veri Akışı (Data Stream) elemanında çalışır.

**Gerekçe ve Varsayımlar:**  
Bir Flume örneği iki modda çalışabilir: Ajan (agent) olarak (doğrudan veri kaynaklarıyla aynı yerde) veya toplayıcı (collector) olarak (birden fazla ajandan veri akışlarını birleştirir ve hedeflere yazar).  
Bu iki moddan hareketle Flume farklı konfigürasyonlarda kullanılabilir. Karar, Flume’u hem ajan hem toplayıcı konfigürasyonunda kullanmaktır: Ajanlar veri kaynaklarıyla aynı yerde konumlandırılır ve Toplayıcı (Collector) Veri Akışı elemanında çalışır.

**Alternatif**

- Flume ajanları her web sunucusundadır ve olayları doğrudan sink’lere yazar (toplayıcı yok).

**Elendiği Neden**

- Hedeflere (HDFS ve Elasticsearch) 300+ eşzamanlı bağlantıdan yoğun trafik üretir. HDFS üzerinde her web sunucusu için çok sayıda dosya oluşturur; bu, HDFS gibi dağıtık bir dosya sistemi için (birden çok web sunucusundan veriyi birleştiren daha büyük dosyalar yerine) optimal değildir.

**Alternatif**

- Flume toplayıcıları olayları doğrudan web sunucularından alır (ajan yoktur) ve sink’lere yazar.

**Elendiği Neden**

- Failover modu desteklemez. Bir toplayıcı düğümünün çökmesi durumunda, bağlı web sunucuları alıcıyı kaybedecektir.

---

**Karar:** Yük dengelemeli (load-balanced), failover destekli katmanlı (tiered) bir konfigürasyon kullanarak “hesaplamaların birden çok kopyasını sürdürme (maintaining multiple copies of computations)” taktiğini tanıt.

**Gerekçe ve Varsayımlar:**  
Olası topoloji alternatifleri arasından, performans (QA-1, saniyede 15.000 olay) ve kullanılabilirlik (QA-10, tekil hata noktası olmaması) kalite niteliği senaryolarına dayanarak seçilen topoloji, yük dengelemeli ve failover destekli katmanlı bir topolojidir.

**Alternatif**

- Toplayıcının çoğaltılmaması

**Elendiği Neden**

- Bu, performans ve kullanılabilirliği düşürecektir.

> **💬 Çevirmen notu:** “Maintaining multiple copies of computations” taktiği, kritik iş yüklerinin birden fazla düğümde paralel olarak yürütülmesi ve gerektiğinde bunlardan birinin devreye girerek hizmet sürekliliğini sağlaması yaklaşımını ifade eder.
