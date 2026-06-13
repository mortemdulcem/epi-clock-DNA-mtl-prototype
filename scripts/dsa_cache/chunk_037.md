Bu bölümde, olgun bir alanda sıfırdan geliştirilen (greenfield) bir sistemin tasarımında ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) kullanımına dair bir örnek sunduk. Üç yinelemeyi, farklı odaklarla birlikte gösterdik: genel bir kaygının ele alınması, işlevselliğin ele alınması ve bir temel kalite niteliği senaryosunun ele alınması.

Örnek, Bölüm 3.3.1’de tartışılan yol haritasını izledi. İlk yinelemede, sistemi yapılandırmak için iki farklı referans mimarinin (reference architecture) kullanılmış olmasını gözlemlemek ilginçtir. Ayrıca, harici olarak geliştirilmiş bileşenlerin—bu durumda çatıların (framework)—seçimi farklı yinelemelere yayılmıştır. Son olarak örnek, tasarım ilerledikçe yeni mimari kaygıların nasıl ortaya çıktığını göstermektedir.

Bu örnek, mimari kaygıların, birincil kullanım durumlarının (primary use cases) ve kalite niteliği senaryolarının (quality attribute scenario) mimari tasarımın bir parçası olarak nasıl ele alınabileceğini göstermektedir. Gerçek bir sistemde, yüksek öncelikli diğer senaryoları ele alarak tam bir mimari tasarım elde etmek için daha fazla yineleme gerekli olacaktır.

Bu örnekte, mimarın tasarım sırasında bir CASE aracı kullandığı varsayılmıştır; bu nedenle diyagramlar UML kullanılarak üretilmiştir. Bunun kesinlikle zorunlu olmadığını, Bölüm 5’te sunulan vaka çalışmasında göreceğiz. Ayrıca, tasarım sürecinin bir parçası olarak üretilen bilgileri kullanarak taslak görünüm eskizleri (preliminary view sketches) üretmenin görece basit olduğuna dikkat edin.

## 4.5

Ek Okumalar

Ek A, bu vaka çalışmasında kullanılan tüm tasarım kavramlarının açıklamalarını ve bibliyografik atıflarını sağlar.

---

# 5  
Vaka Çalışması: Büyük Veri Sistemi

Serge Haziyev ve Olha Hrytsay ile birlikte

Şimdi, zorlayıcı bir alan olan Büyük Veri (Big Data) için, sıfırdan geliştirilen (greenfield) bir sistemde ADD 3.0 kullanımına ilişkin kapsamlı bir tasarım örneği sunuyoruz. Bu metnin yazıldığı sırada, bu alan görece yeniydi ve hızla evrim geçiriyordu. Bu nedenle, mimarlar yalnızca geçmiş deneyimlerine güvenerek ilerleyemezlerdi. Bunun yerine, tasarım sürecini dönemsel analizler ve stratejik prototipleme (strategic prototyping) ile tamamladılar; bunu şimdi açıklayacağız.

## 5.1

İş Gerekçesi (Business Case)

Bu vaka çalışması, milyonlarca web kullanıcısına popüler içerik ve çevrimiçi hizmetler sunan bir İnternet şirketini kapsamaktadır. Şirket, dışarıya bilgi sağlamanın yanında, altyapısından üretilen (örneğin uygulama ve sunucu günlükleri, sistem metrikleri) çok büyük hacimde günlük (log) verisini toplar ve analiz eder. Bilgisayar tarafından üretilen günlük mesajlarıyla bu şekilde başa çıkma yaklaşımı, günlük yönetimi (log management, bkz. http://en.wikipedia.org/wiki/Log_management_and_intelligence) olarak da adlandırılır.

Çok hızlı altyapı büyümesi nedeniyle, şirketin BT departmanı mevcut kurum içi sistemlerin artık gerekli günlük veri hacmini ve hızını işleyemediğini fark etmektedir. Ayrıca, yeni bir sisteme yönelik talepler, sadece günlüklerden değil, birden çok veri kaynağından toplanabilecek çeşitli veri türlerini kullanmak isteyen ürün yöneticileri ve veri bilimcileri gibi diğer şirket paydaşlarından da gelmektedir.

Şekil 5.1’de gösterilen piyasa-mimari diyagramı (marketecture diagram, sistem yapısının gayriresmî betimi), üç ana kullanıcı grubuna yönelik olarak istenen çözümü işlevsel bir bakış açısından göstermektedir.

- Gerçek zamanlı izleme  
- Tam metin arama  
- Anomali tespiti  

Web Sunucuları  
- Yüzlerce sunucu  
- Birden çok kaynaktan gelen  
  çok büyük günlükler  

- Ham ve birleştirilmiş tarihsel veriler  
- Ad hoc analiz  
- Gerçek zamanlı sorgular  

Gerçek Zamanlı  
Gösterge Paneli (Dashboard)  

7/24 Operasyon,  
Destek Mühendisleri,  
Geliştiriciler  

Ad Hoc  
Raporlar  

Veri Bilimciler /  
Analistler  

- Gerçeğe yakın zamanlı statik raporlar  
- Kurumsal BI aracılığıyla erişilebilir  

Statik Raporlar  

Yönetim  

**Şekil 5.1** Büyük Veri sistemi için piyasa-mimari (marketecture) diyagramı

## 5.2

Sistem Gereksinimleri

Gereksinim çıkarım (requirement elicitation) faaliyetleri daha önce gerçekleştirilmiştir. Toplanan en önemli gereksinimler burada özetlenmiştir. Bunlar, birincil kullanım durumlarından oluşan bir küme, kalite niteliği senaryolarından oluşan bir küme, kısıtlardan oluşan bir küme ve mimari kaygılardan oluşan bir kümeden meydana gelir.

### 5.2.1

Kullanım Durumu Modeli (Use Case Model)

Sistemin birincil kullanım durumları aşağıdaki tabloda açıklanmaktadır.

| Kullanım Durumu | Açıklama |
| --- | --- |
| **UC-1: Çevrimiçi hizmetleri izleme** | Nöbetçi operasyon personeli, gerçek zamanlı bir operasyon gösterge paneli aracılığıyla hizmetlerin ve BT altyapısının (örneğin web sunucu yükü, kullanıcı aktiviteleri ve hatalar) mevcut durumunu izleyebilir; bu panel onların sorunlara hızla tepki vermelerini sağlar. |
| **UC-2: Çevrimiçi hizmet sorunlarını giderme** | Operasyon, destek mühendisleri ve geliştiriciler, günlük örüntülerini arayarak ve günlük mesajlarını filtreleyerek en son toplanan günlükler üzerinde sorun giderme (troubleshooting) ve kök neden analizi (root-cause analysis) yapabilir. |
| **UC-3: Yönetim raporları sağlama** | BT ve ürün yöneticileri gibi kurumsal kullanıcılar, sistem yükünün zamana göre değişimi, ürün kullanımı, hizmet seviyesi anlaşması (service level agreement, SLA) ihlalleri ve sürümlerin kalitesi gibi bilgileri gösteren, kurumsal bir BI (business intelligence, iş zekâsı) aracı içindeki önceden tanımlanmış (statik) raporlar aracılığıyla tarihsel bilgiyi görüntüleyebilir. |
| **UC-4: Veri analitiğini destekleme** | Veri bilimciler ve analistler, ham ve birleştirilmiş tarihsel veriler üzerinde belirli veri örüntülerini ve korelasyonları bulmak için, altyapı kapasite planlamasını ve müşteri memnuniyetini iyileştirmeye yönelik SQL-benzeri sorgularla ad hoc veri analizi yapabilir. |
| **UC-5: Anomali tespiti** | Operasyon ekibi, sistemin herhangi bir alışılmadık davranışı konusunda 7/24 bilgilendirilmelidir. Bu bildirim planını desteklemek için sistem, gerçek zamanlı anomali tespiti ve uyarı mekanizmasını uygulamalıdır (gelecek gereksinim). |
| **UC-6: Güvenlik raporları sağlama** | Güvenlik analistlerine, hedef ve kaynak adresleri, zaman damgası ve kullanıcı oturum açma bilgilerini içeren denetim günlük girdilerini (audit log entries) inceleyerek potansiyel güvenlik ve uyum (compliance) sorunlarını araştırma imkânı sağlanmalıdır (gelecek gereksinim). |

### 5.2.2

Kalite Niteliği Senaryoları

En ilgili kalite niteliği (ham) senaryoları aşağıdaki tabloda sunulmuştur. Her senaryo için, ilişkilendirildiği kullanım durumunu da tanımlıyoruz.

| ID | Kalite Niteliği | Senaryo | İlgili Kullanım Durumu(ları) |
| --- | --- | --- | --- |
| **QA-1** | Performans | Sistem, yaklaşık 300 web sunucusundan saniyede 15.000 olaya kadar veri toplamalıdır. | UC-1, UC-2, UC-5 |
| **QA-2** | Performans | Sistem, nöbetçi operasyon personeli için gerçek zamanlı izleme gösterge panelini < 1 dakikalık gecikmeyle (latency) otomatik olarak yenilemelidir. | UC-1 |
| **QA-3** | Performans | Sistem, son 2 haftalık veriler için, acil durum sorun giderme amacıyla gerçek zamanlı arama sorguları sağlamalı ve sorgu yürütme süresi < 10 saniye olmalıdır. | UC-2 |
| **QA-4** | Performans | Sistem, iş kullanıcıları için dakika başına birleştirme (aggregation) sağlayan gerçeğe yakın zamanlı statik raporları < 15 dakikalık gecikmeyle ve < 5 saniyelik rapor yükleme süresiyle sağlamalıdır. | UC-3, UC-6 |
| **QA-5** | Performans | Sistem, ham ve birleştirilmiş tarihsel veriler üzerinde, önceden tanımlı olmayan (ad hoc) SQL-benzeri, insan-zamanı (human-time) sorgularını < 2 dakikalık sorgu yürütme süresiyle sağlamalıdır. Sonuçlar, sorgulama için < 1 saat içinde kullanılabilir olmalıdır. | UC-4 |
| **QA-6** | Ölçeklenebilirlik (Scalability) | Sistem, acil durum sorun giderme için (günlükler üzerinde tam metin arama yoluyla) erişilebilir olacak şekilde, son 2 haftanın ham verisini depolamalıdır. | UC-2 |
| **QA-7** | Ölçeklenebilirlik (Scalability) |  |  |

> **💬 Çevirmen notu:** “Human-time query” ifadesi, sistemin yüksek hacimli veriye rağmen, sorgu yanıt sürelerinin insanın bekleyebileceği makul sürelerde kalmasını vurgular; burada “insan-zamanı” ibaresi bu vurguyu yansıtmak için korunmuştur.
