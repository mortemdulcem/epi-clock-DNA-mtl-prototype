hiyerarşideki (seviye 1) zaman sunucuları, hassas zaman sağlayan donanımlarla (örneğin, sezyum osilatör, GPS sinyali) donatılmıştır. Hiyerarşide daha aşağı seviyelerde bulunan zaman sunucuları, üst seviyelerdeki sunuculardan veya eşlerinden zaman istemek için NTP (Network Time Protocol) kullanır.

Ağdaki birçok ekipman, zaman sunucuları tarafından sağlanan zamana bağımlıdır; bu nedenle şirket için önceliklerden biri, zaman sunucularında ortaya çıkan sorunları düzeltmektir. Bu tür sorunlar, zaman sunucularında yeniden başlatma gibi fiziksel bakım yapmak üzere bir teknisyenin sahaya gönderilmesini gerektirebilir. Şirketin bir diğer önceliği ise, senkronizasyon çerçevesinin performansını izlemek için zaman sunucularından veri toplamaktı.

İlk dağıtım planlarında, şirketin belirli bir modelden 100 zaman sunucusunu sahaya sürme isteği vardı. NTP’nin yanı sıra zaman sunucuları, üç temel işlem sağlayan Basit Ağ Yönetim Protokolü’nü (Simple Network Management Protocol, SNMP) de destekler:

- `set()` işlemleri: yapılandırma değişkenlerini değiştirme (örneğin, bağlı eşler).
- `get()` işlemleri: yapılandırma değişkenlerini veya performans verilerini alma.
- `trap()` işlemleri: GPS sinyalinin kaybı veya geri gelmesi ya da zaman referansındaki değişiklikler gibi olağandışı olaylara ilişkin bildirimler.

Şirketin hedeflerine ulaşmak için zaman sunucuları için bir yönetim sistemi geliştirilmesi gerekiyordu. Bu sistemin, ağ yönetimi için standart bir model olan FCAPS modeline uyması gerekiyordu. Kısaltmadaki harfler şunları ifade eder:

- **Fault management (arızayla yönetim)**. Arıza yönetiminin amacı, ağda meydana gelen arızaları tanımak, izole etmek, düzeltmek ve kaydetmektir. Bu durumda bu arızalar, zaman sunucuları tarafından üretilen tuzaklara (trap) veya yönetim sistemi ile zaman sunucuları arasındaki iletişimin kaybı gibi diğer sorunlara karşılık gelir.
- **Configuration management (yapılandırma yönetimi)**. Bu, ağ cihazlarından yapılandırmaları toplama ve depolamayı içerir; böylece cihazların yapılandırılmasını basitleştirir ve cihaz yapılandırmalarında yapılan değişiklikleri izlemenin yolunu sağlar. Bu sistemde, tek tek yapılandırma değişkenlerini değiştirmenin yanı sıra, belirli bir yapılandırmayı birden fazla zaman sunucusuna dağıtabilmek gereklidir.
- **Accounting (hesaplama/hesap yönetimi)**. Buradaki amaç, cihaz bilgilerini toplamaktır. Bu bağlamda bu, cihaz donanım ve gömülü yazılım (firmware) sürümlerini, donanım ekipmanını ve sistemin diğer bileşenlerini takip etmeyi içerir.
- **Performance management (performans yönetimi)**. Bu kategori, mevcut ağın verimliliğini belirlemeye odaklanır. Performans verileri toplanıp analiz edilerek ağ sağlığı izlenebilir. Bu durumda, zaman sunucularından gecikme (delay), ofset (offset) ve jitter ölçümleri toplanır.
- **Security management (güvenlik yönetimi)**. Bu, ağdaki varlıklara erişimi kontrol etme sürecidir. Bu durumda iki önemli kullanıcı türü vardır: teknisyenler ve yöneticiler (administrators). Teknisyenler, tuzak bilgilerini ve yapılandırmaları görüntüleyebilir ancak değişiklik yapamaz; yöneticiler ise teknisyenlerle aynı bilgileri görüntüleyebilir, ayrıca yapılandırmalarda değişiklik yapabilir ve ağa zaman sunucusu ekleyip çıkarabilirler.

> **💬 Çevirmen notu:** FCAPS, ağ yönetiminde yaygın kullanılan bir sınıflandırma çerçevesidir ve beş temel yönetim alanını sistematikleştirir.

Bir kez başlangıç ağı dağıtıldıktan sonra, şirket bunu, potansiyel olarak SNMP dışındaki yönetim protokollerini destekleyebilecek yeni model zaman sunucuları ekleyerek genişletmeyi planlamıştır.

Bu bölümün geri kalanı, ADD 3.0 (Attribute-Driven Design 3.0) kullanılarak oluşturulmuş bu sistemin bir tasarımını açıklamaktadır.

---

## 4.2 Sistem Gereksinimleri

Gereksinim ortaya çıkarma (requirement elicitation) etkinlikleri daha önce gerçekleştirilmişti ve aşağıda toplanan en ilgili gereksinimlerin bir özeti verilmektedir.

### 4.2.1 Kullanım Senaryosu (Use Case) Modeli

Şekil 4.1’deki kullanım senaryosu modeli, sistemde FCAPS modelini destekleyen en ilgili kullanım senaryolarını göstermektedir. Diğer kullanım senaryoları gösterilmemiştir.

**ŞEKİL 4.1** FCAPS sistemi için kullanım senaryosu modeli

---

Bu kullanım senaryolarının her biri aşağıdaki tabloda açıklanmıştır:

| Kullanım Senaryosu | Açıklama |
| --- | --- |
| **UC-1: Ağ durumunu izle** | Kullanıcı, tüm ağın hiyerarşik bir gösteriminde zaman sunucularını izler. Sorunlu cihazlar ve bunların gruplanmış olduğu mantıksal bölgeler vurgulanır. Kullanıcı ağ gösterimini genişletebilir ve daraltabilir. Bu gösterim, arızalar tespit edildikçe veya onarıldıkça sürekli olarak güncellenir. |
| **UC-2: Arıza tespiti** | Yönetim sistemi periyodik olarak zaman sunucuları ile iletişime geçerek onların “canlı” olup olmadığını kontrol eder. Bir zaman sunucusu yanıt vermezse ya da bir problemi veya normal çalışma durumuna geri dönüşü işaret eden bir tuzak (trap) alınırsa, olay depolanır ve kullanıcıların gördüğü ağ gösterimi buna göre güncellenir. |
| **UC-3: Olay geçmişini göster** | Belirli bir zaman sunucusu veya bir grup zaman sunucusu ile ilişkili depolanmış olaylar görüntülenir. Bunlar tür veya öncelik derecesi gibi çeşitli ölçütlere göre filtrelenebilir. |
| **UC-4: Zaman sunucularını yönet** | Yönetici, ağa bir zaman sunucusu ekler veya ağdan bir zaman sunucusunu çıkarır. |
| **UC-5: Zaman sunucusunu yapılandır** | Yönetici, belirli bir zaman sunucusuyla ilişkili yapılandırma parametrelerini değiştirir. Parametreler cihaza gönderilir ve yerel olarak da depolanır. |
| **UC-6: Yapılandırmayı geri yükle** | Yerel olarak depolanmış bir yapılandırma, bir veya daha fazla zaman sunucusuna gönderilir. |
| **UC-7: Performans verisi topla** | Ağ performans verileri (gecikme, ofset ve jitter), zaman sunucularından periyodik olarak toplanır. |
| **UC-8: Bilgi görüntüle** | Kullanıcı, zaman sunucusu hakkında depolanmış bilgileri — yapılandırma değerleri ve sunucu adı gibi diğer parametreleri — görüntüler. |
| **UC-9: Performans verisini görselleştir** | Kullanıcı, ağ performans ölçümlerini (gecikme, ofset, jitter) ağ performansını görmek ve analiz etmek için grafiksel bir biçimde görüntüler. |
| **UC-10: Sisteme giriş yap** | Kullanıcı, bir giriş/parola ekranı aracılığıyla sisteme giriş yapar. Başarılı girişten sonra kullanıcıya rolüne göre farklı seçenekler sunulur. |
| **U-11: Kullanıcıları yönet** | Yönetici, kullanıcı ekler veya çıkarır ya da kullanıcı izinlerini değiştirir. |

### 4.2.2 Kalite Niteliği Senaryoları (Quality Attribute Scenarios)

Bu kullanım senaryolarına ek olarak, bir dizi kalite niteliği (quality attribute) senaryosu ortaya çıkarılmış ve belgelenmiştir. Bunların içinden en ilgili altı tanesi aşağıdaki tabloda sunulmuştur. Her senaryo için ayrıca ilişkili olduğu kullanım senaryosunu da belirtiyoruz.

| ID | Kalite Niteliği | Senaryo | İlişkili Kullanım Senaryosu |
| --- | --- | --- | --- |
| **QA-1** | Performans | Birçok zaman sunucusu, tepe yük sırasında yönetim sistemine tuzaklar gönderir; tuzakların %100’ü başarıyla işlenir ve depolanır. | UC-2 |
| **QA-2** | Değiştirilebilirlik (Modifiability) | Sisteme bir güncellemenin parçası olarak yeni bir zaman sunucusu yönetim protokolü eklenir. Protokol, sistemin çekirdek bileşenlerinde herhangi bir değişiklik yapılmadan başarıyla eklenir. | — |
| **QA-3** | Kullanılabilirlik (Availability) | Normal çalışma sırasında yönetim sisteminde bir arıza oluşur. Yönetim sistemi 30 saniyeden kısa sürede çalışmaya yeniden başlar. | Tümü |
| **QA-4** | Performans | Yönetim sistemi, tepe yük sırasında bir zaman sunucusundan performans verisi toplar. Yönetim sistemi, tüm performans verisini 5 dakika içinde toplar ve bu sırada tüm kullanıcı isteklerini işler; böylece CON-5’ten kaynaklanan veri kaybı yaşanmaz. | UC-7 |
| **QA-5** | Performans, kullanılabilirlik (usability) |  |  |
