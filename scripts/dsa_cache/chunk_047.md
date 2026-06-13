Batch Görünümleri
bileşeninde veri modeli
olarak yıldız şemasını
(star schema) kullanın

Önceki iterasyonda, Batch Görünümleri (Batch Views) bileşenleri için tek teknoloji olarak Impala’yı seçtik; bu seçim hem statik raporları (UC-3, 6) hem de ad hoc sorgulamayı (UC-4) etkiler. Yıldız şeması tekniği iki nedenle seçildi:

- Impala analitik sorgular için tasarlanmıştır; bu nedenle yıldız şeması veri modelleme için doğal olarak iyi destek sağlar.
- BI araçlarıyla birlikte ad hoc sorgulama, sorgu karmaşıklığını basitleştirmek ve bunun sonucu olarak daha hızlı sorgu performansına izin vermek için verinin iyi modellenmesini gerektirir.

Bizim durumumuzda, yıldız şeması, büyük tablolar arasındaki join’lerden kaçınmak amacıyla küçük boyutlu (satır sayısı açısından) boyut tablolarına sahip olacak şekilde tasarlandı; zira bu tür join’ler tipik olarak yüksek miktarda sistem kaynağı tüketir ve sorgu yürütme performansını etkiler. Küçük boyutlu tablolar belleğe sığabilir ve join’ler daha etkin şekilde gerçekleştirilebilir.

#### 5.3.5.5

Alternatif

Elendiği Neden

Düz tablolar
(flat tables)

Düz tablolar tipik olarak tüm ölçüleri ve boyut özniteliklerini içeren, geniş ve denormalize tablolar biçiminde temsil edilir.

Düz tablolar, büyük veri hacimleri üzerinde sorgu çalıştırılırken önemli performans sorunlarına yol açabilir.

### Adım 6: Görünümleri Taslak Haline Getir ve Tasarım Kararlarını Kaydet

Şekil 5.9, Impala ve Parquet kullanılarak gerçekleştirilen yıldız şeması veri modelini göstermektedir.

Şekil 5.10’daki ekran görüntüsü, kurumsal bir BI aracı üzerinden olası bir görünümü göstermek için Tableau ile gerçekleştirilmiş örnek bir statik raporu sunar. Rapor, Parquet’te depolanan ve ODBC arayüzü üzerinden Impala tarafından sağlanan test verisi kullanılarak oluşturulmuştur.

---

Şekil 5.9 Yıldız şeması, Impala ve Parquet ile gerçekleştirilmiş

```text
dim_request
request_id          <pi>
request_method
request_url
request_protocol

dim_user_agent
user_agent_id <pi>  int
user_agent_full     string
browser             string
device_type         string
os                  string

dim_referrer
referrer_id   <pi>  int
referrer_url        string
referrer_site       string

dim_city
city_id       <pi>  int
city                string
region              string
country             string

dim_zip_code
zip_code_id  <pi>   int
zip_code            string

dim_message
message_id   <pi>   int
message_url         string

fact_access
client_ip           string
request_id   <fi5>  int
referrer_id  <fi4>  int
user_agent_id<fi1>  int
city_id      <fi2>  int
zip_code_id  <fi3>  int
latitude            string
longitude           string
event_timestamp     Timestamp
server_host         string
requst_time         int
response_code       smallint
response_size       int

fact_error
event_timestamp     Timestamp
message_id   <fi1>  int
server_host         string
client_ip           string
level               string
```

> **💬 Çevirmen notu:** `request_id`, `user_agent_id` gibi `<pi>` ve `<fiX>` işaretleri birincil anahtar (primary key) ve yabancı anahtar (foreign key) göstergeleridir.

Şekil 5.10 Tableau ile gerçekleştirilmiş örnek statik rapor

---

## 5.4 Özet

### 5.3.5.6 Adım 7: Mevcut Tasarımın Analizini Gerçekleştir ve İterasyonu Gözden Geçir

#### Tasarım Amacı ve Amacın Gerçekleştirilmesi

Aşağıdaki Kanban tablosu, iterasyon sırasında kaydedilen tasarım ilerlemesini ve alınan kararları özetlemektedir. Önceki iterasyonda tamamen ele alınmış sürücülerin (driver) burada gösterilmediğine dikkat edin.

|                    | Adreslenmedi | Kısmen Adreslendi | Tamamen Adreslendi | İterasyon Sırasında Alınan Tasarım Kararları |
|--------------------|-------------:|-------------------:|--------------------:|---------------------------------------------|
| UC-3               |              | ✔                 |                     | Bu kullanım senaryosunda kullanılan Sunum Katmanının (Serving Layer) iyileştirilmesi. Bu kullanım senaryolarına katılan diğer ögelerle ilgili kararların hâlâ verilmesi gerekmektedir. |
| UC-4               |              | ✔                 |                     |                                             |
| QA-4               |              |                   | ✔                   | Parquet ve yıldız şeması kullan. Performans testleri hâlâ gereklidir ve bu nedenle yeni bir kaygı (concern) ortaya çıkmıştır: CRN-4: Performans testleri geliştir. |
| QA-5               |              |                   | ✔                   |                                             |
| QA-8               |              |                   | ✔                   |                                             |
| CRN-1              | ✔            |                   |                     | İlgili bir karar alınmamıştır.              |
| CRN-3              |              | ✔                 |                     | Sunum Katmanındaki ögeler için veri modelleme ve kavram kanıtlama (proof-of-concept) prototipleri geliştirilmiştir, ancak aynı etkinliğin Hız Katmanındaki (Speed Layer) ögeler için de tamamlanması gerekmektedir. |

## 5.4 Özet

Bu bölümde, görece yeni bir alan olan Büyük Veri (Big Data) için ADD 3.0’ın (Attribute-Driven Design) kullanımına ilişkin kapsamlı bir örnek sunduk. Bu örneğin gösterdiği gibi, mimari tasarım, kalite niteliklerinin (quality attributes) sağlanmasını temin etmek için çok sayıda ayrıntılı kararın alınmasını gerektirebilir.

Ayrıca bu örnek, çok sayıda kararın birçok farklı desen (pattern) ve teknoloji bilgisine dayandığını da gösterir. Alan ne kadar yeni ise, o alan için önceden var olan bilgi (örneğin tasarım kavramları kataloğu, desen kitapları ve referans mimariler) bulunmama olasılığı o kadar yüksektir. Böyle bir durumda, ya kendi muhakemenize ve deneyiminize güvenmeli ya da deneyler yapıp prototipler inşa etmelisiniz. Her iki durumda da bu kararların verilmesi gerekir.

Bu ADD örneği, Bölüm 4’te sunulan örnekten şu açıdan da farklıdır: Arayüz belirtimlerini türetmenin bir aracı olarak dizge diyagramları (sequence diagram) oluşturmaya nispeten az zaman ve çaba harcadık. Burada sunulan örnek, bileşen sayısı sınırlı, görece basit bir veri akışı (data-flow) mimarisine dayanıyordu; bu nedenle bileşenler arasındaki ilişkileri anlamak için dizge diyagramlarına ihtiyaç yoktu. Ögeler arasındaki “sözleşmeler” (contracts), İterasyon 3’ün adım 5’inde (Bölüm 5.3.4.4’te açıklanan) örneklendirildiği üzere, değiş tokuş edilen bilgi tarafından belirlendi.

---

Bölüm 5—Vaka Çalışması: Büyük Veri Sistemi

## 5.5 Ek Okumalar

Veri ambarı (data warehouse) tasarımı kapsamlı biçimde incelenmiştir. İki iyi yaklaşım R. Kimball ve M. Ross, *The Data Warehouse Toolkit*, 3. baskı, Wiley, 2013; ve W. Inmon, *Building the Data Warehouse*, 4. baskı, Wiley, 2005’te belgelenmiştir.

Lambda mimarisi ilk olarak N. Marz ve J. Warren, *Big Data: Principles and Best Practices of Scalable Realtime Data Systems*, Manning, 2015’te sunulmuştur.

Ölçeklenebilirlik için nasıl mühendislik yapılacağına dair iyi bir tartışma M. Abbott ve M. Fisher, *The Art of Scalability: Scalable Web Architecture, Processes, and Organizations for the Modern Enterprise*, Addison-Wesley, 2010’da bulunabilir.

P. Sadalage ve M. Fowler, *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*, Addison-Wesley, 2009.

Mimari tasarım sürecinin bir parçası olarak ne zaman ve nasıl prototip yapılacağına ilişkin bir tartışma H-M Chen, R. Kazman ve S. Haziyev, “Strategic Prototyping for Developing Big Data Systems”, *IEEE Software*, Mart/Nisan 2016’da bulunabilir.

Bu vaka çalışmasında kullanılan birçok referans mimari ve teknolojiyi içeren bir tasarım kavramları kataloğu, Smart Decisions Game’in bir parçasıdır ve H. Cervantes, S. Haziyev, O. Hrytsay ve R. Kazman, “Smart Decisions Game”, http://smartdecisionsgame.com adresinde bulunabilir.

---

# 6 Vaka Çalışması: Bankacılık Sistemi

Bölüm 4 ve 5’in her ikisi de sıfırdan geliştirme (greenfield development) örnekleriydi. Gerçekte, bu tür geliştirme nispeten nadirdir. Çoğu zaman, bir mimar olarak siz, sıfırdan bir sistem yaratmak yerine mevcut bir sistemi evrimleştirme üzerinde çalışırsınız. Bu bölümde, olgun bir alandaki (Bölüm 3.3.3’te tartışıldığı gibi) bir brownfield sistem için ADD 3.0’ın kullanımına ilişkin bir örnek sunuyoruz. Önce iş bağlamını (business context) sunuyor, ardından projenin mevcut mimari dokümantasyonunu inceliyoruz. Bunu, sistemi evrimleştirmek için ADD iterasyonları sırasında gerçekleştirilen etkinliklerin adım adım özeti izliyor. Bu gerçek bir sistemdir, ancak aktörlerin kimliklerinin korunması için bazı ayrıntılar değiştirilmiştir.

## 6.1 İş Vaka Analizi (Business Case)
