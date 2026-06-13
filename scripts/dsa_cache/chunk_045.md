### 5.3.4.4 Adım 5: Mimari Öğeleri Örnekle, Sorumlulukları Ata ve Arayüzleri Tanımla

Bu yinelemede verilen örnekleme (instantiation) tasarım kararları aşağıdaki tabloda özetlenmektedir:

| Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar | Alternatif | Elenme Nedeni |
| --- | --- | --- | --- |
| Apache HTTP Sunucusu’ndan erişim (access) ve hata (error) günlüklerini girdi formatı olarak kullan | Sistem gereksinimleri, web sunucu yükü, kullanıcı aktiviteleri ve hatalar gibi günlüklerin (logların) toplanmasını ve analiz edilmesini içerir. Gerçekte veri kaynağı türlerinin sayısı onlarca (hatta bazen yüzlerce) olabilir. Kanıt niteliğinde kavram kanıtlama (proof-of-concept) geliştirmesi için tek bir veri kaynağı türü dikkate alınmıştır: bir Apache HTTP sunucusu (“web sunucusu”). Toplanacak veriler; erişim günlüğü (access log) üzerinden izlenecek kullanıcı aktivitelerini ve hata günlüğü (error log) üzerinden toplanacak sistem hatalarını içerir. Web sunucusu erişim günlüğü, sunucu tarafından işlenen tüm istekleri kaydeder. Bir günlük girdisi şu şekilde görünebilir: `143.21.52.246 - - [19/Jun/2014:12:15:17 +0000] "GET /test.html HTTP/1.1" 200 341 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) Gecko/20110421 Firefox/6.0a1".` Bu örnek şu veri alanlarından oluşur: istemci IP adresi, istemci kimliği, kullanıcı ID’si, zaman damgası (timestamp), istek metodu, istek URL’si, istek protokolü, yanıt kodu, yanıt boyutu, yönlendiren (referrer), kullanıcı aracısı (user agent). Web sunucusu hata günlüğü ise tanı (diagnostic) bilgisi gönderir ve kullanıcı isteklerini işlerken karşılaştığı hataları kaydeder. Örneğin: `[19/Jun/2014:14:23:15 +0000] [error] [client 50.83.180.156] Directory index forbidden by rule: /home/httpd/` Bu örnek şu veri alanlarından oluşur: zaman damgası, önem düzeyi (severity level), istemci IP adresi, mesaj. Daha ileri veri modelleme ve teknoloji yapılandırması (technology configuration) bu iki günlük türüne ve tanımlanan alanlara dayanacaktır. | — | — |
| Günlük dosyalarını Flume ajanının kaynak öğesindeki bir IP portu üzerinden yönlendir (pipe); Flume ajanında IP portu üzerinden (örneğin syslog kullanarak) veri akışını yapılandır | Apache Flume, günlük verilerini bir IP portu üzerinden yönlendirecek şekilde yapılandırılır (örneğin syslog kullanılarak). | Bir günlük dosyasından okuma (örn. `tail -F access_log` komutunu çalıştırarak) | Bu seçenek en basit gibi görünür, ancak olay teslimini garanti etmez (olaylar kaybolabilir); bu da Flume kullanıcı rehberinde açıkça belirtilmiştir. |

> **💬 Çevirmen notu:** Burada “pipe” ve “piped” ifadeleri, logların bir dosyadan okunmak yerine bir ağ portuna akıtılması ve Flume’un bu porttan okuması anlamında kullanılıyor.

---

#### 5.3 Tasarım Süreci

| Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar |
| --- | --- |
| Ajanlar ve toplayıcı (collector) için olay yönlendirme (event channeling) yöntemlerini belirle; nihai kararı prototipleme ile ver | Source (Kaynak) öğesinden alınan olaylar Channel (Kanal) öğesinde ara depolanır (staged). Flume şu anda kanalı yapılandırmak için üç olası seçenek sunmaktadır: 1. **Bellek kanalı (Memory channel):** Bellek içi kuyruk; daha hızlıdır, ancak bir Flume süreci çöktüğünde bellek kuyruğunda kalan olaylar kurtarılamaz. 2. **Dosya kanalı (File channel):** Kalıcıdır ve yerel dosya sistemi tarafından yedeklenir. 3. **Apache Kafka:** Kafka’nın dağıtık ve yüksek erişilebilirlikte bir kanal olarak görev yaptığı bir yaklaşımdır. Bu seçenekler arasındaki seçim, aslında performans ile erişilebilirlik (availability) (veya bazen dayanıklılık/durabilite olarak adlandırılır) arasındaki “klasik” ödünleşimidir (tradeoff). Açıkça belirtilmiş bir dayanıklılık (durability) senaryomuz olmasa da, gelecekteki sistem genişlemesiyle (UC-6, güvenlik raporları) birlikte bu gereksinimin daha kritik hâle geleceğini biliyoruz. Bu, mimari bir endişeye (architectural concern) örnektir; çünkü herhangi bir gereksinim dokümanında görünmez, fakat mimarın yine de ele alması gerekir. Bu seçenekler ve performans sonuçlarına ilişkin kamuya açık bir bilgi bulunmadığı göz önüne alındığında, bu durum prototipleme yapıp sonuçlara göre karar vermek için iyi bir adaydır. Prototipleme ve performans ölçümünün bir diğer gerekçesi de gerekli donanım kaynaklarını hesaplama ihtiyacıdır. Sonuç olarak yeni bir endişe tanımlanmış ve iş listesine (backlog) eklenmiştir: ■■ **CRN-3:** Veri modelleme ve kilit sistem öğeleri için kavram kanıtlama (proof-of-concept) prototipleri geliştirme |
| HDFS sink içinde ham veriyi depolamak için belirli bir dosya formatı olarak Avro seç | Hadoop tabanlı bir çözüme tasarım yapılırken verilmesi gereken kararlardan biri, en uygun dosya formatının seçilmesidir. Hadoop, saklanan verilere ve kullanım senaryolarına bağlı olarak farklı işlevler, sıkıştırma ve performans sonuçları sunan çeşitli formatları destekler. Bu durumda temel senaryolar, performans (QA-1, saniyede 15.000 olay), ölçeklenebilirlik (QA-7, yaklaşık 60 TB ham veri) ve genişletilebilirlik (QA-9, yeni veri kaynaklarının eklenmesi) gibi kalite nitelikleri (quality attributes) ile ilgilidir. Bu gereksinimleri dosya formatı özelliklerine dönüştürdüğümüzde; bunlar, performans (Data Stream’in veriyi ne kadar hızlı itebileceği), sıkıştırma faktörü (daha az depolama alanı) ve şema evriminin (schema evolution) kolaylığı (yeni günlük formatları eklerken veya mevcut olanları değiştirirken) tarafından etkilenecektir. Avro’yu seçiyoruz; çünkü zengin veri yapıları destekler, iyi sıkıştırma seviyeleri sunar (Snappy sıkıştırma kodlayıcısı ile) ve şema değişikliklerine uyum sağlayabilecek kadar esnektir (verinin şemasıyla birlikte saklandığı, kendini tanımlayan bir format kullanarak). |

| Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar | Alternatif | Elenme Nedeni |
| --- | --- | --- | --- |
| — | — | Metin dosyası (düz metin, CSV, XML, JSON) | Sıkıştırma oranı, ikili (binary) dosya formatlarına (örn. Avro) kıyasla zayıftır. Ayrıca, HDFS bloğu boyutundan daha büyük dosyalar depolanırken gerekli olan blok sıkıştırmayı (block compression) desteklemez. |
| — | — | SequenceFile | Esnek şema evrimini desteklemez. İkili anahtar/değer (key/value) çiftlerinden oluşur ve verinin yanında üstveri (metadata) saklamaz. |
| — | — | RCFile | Bu Hadoop sütunlu (columnar) dosya formatı şema evrimini desteklemez ve yazma işlemleri, sütunsal olmayan formatlara göre daha fazla CPU ve bellek gerektirir. |
| — | — | ORCFile | İyileştirilmiş RCFile, daha iyi sıkıştırma ve daha hızlı sorgulama sunar; fakat şema evrimi açısından RCFile ile aynı dezavantajlara sahiptir ve yazma performansı pahasına çalışır. |
| — | — | Parquet | Parquet, kısmen şema evrimini destekleyen sütunlu bir dosya formatıdır; ancak yine de yazma işlemleri, sütunsal olmayan dosya formatlarına kıyasla daha yavaştır. |

---

### 5.3.4.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 5.8, örnekleme kararlarının sonucunu göstermektedir.

**Öğe** | **Sorumluluk**
---|---
Flume ajanı | Bir web sunucusu tarafından üretilen günlük olaylarını tüketmek, metin tabanlı günlük girdilerini ayrı alanlara bölmek ve ayrıştırılmış (parsed) olay kayıtlarını bir toplayıcıya iletmek.
Flume toplayıcısı (collector) | Birden fazla ajan’dan olay kayıtlarını yük dengeleme (load-balanced) ve hataya dayanıklı (fault-tolerant) bir biçimde toplamak ve bunları kalıcılık (persistency) ve daha ileri işleme (processing) için hedeflere (HDFS ve Elasticsearch) iletmek.

Aşağıdaki şema, katmanlar ve başlıca Flume bileşenleri arasındaki veri akışını göstermektedir:

- **Uygulama Katmanı (Application Tier)**
- **Flume Collector Katmanı (Flume Collector Tier)**
- **Depolama Katmanı (Storage Tier)**

```text
WebServer 1 (Data Source)

Flume Agent
  netcat src (access)
  Memory channel (access)
  netcat src (error)
  Memory channel (error)
  avro sink (access)
  avro sink (error)

BATCH Layer

Data Stream Collector
  Flume Agent
    Memory channel (access)
    netcat src (error)
    Memory channel (error)
    avro src (access)
    avro sink (access)
      + log parsing
    avro sink (error)
    avro src (error)
    netcat src (error)
    Memory channel (error)
    replicating
    Memory channel
    ES sink (access)
    Memory channel
    HDFS sink (error)

HDFS
ES
```

> **💬 Çevirmen notu:** Şekil 5.8’deki metin, Flume konfigürasyonundaki `source`/`channel`/`sink` elemanlarını ve bunların HDFS ile Elasticsearch’e (ES) veri gönderen akışını özetleyen bir bileşen/görünüm (view) taslağıdır.
