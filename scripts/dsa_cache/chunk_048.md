2010 yılında, bir Latin Amerika ülkesinin hükümeti, bankacılık kurumlarının hesap ekstrelerini dijital olarak imzalamasını zorunlu kılan bir düzenleme yayımladı. Bu düzenlemeye uyum sağlamak için “ACME Bankası”, başlıca amacı dijital olarak imzalanmış hesap ekstrelerinin üretilmesi olan ve BankStat adını vereceğimiz bir yazılım sisteminin geliştirilmesini sipariş etti.

Şekil 6.1, BankStat sisteminin nasıl çalıştığını gösteren bir bağlam diyagramı (context diagram) sunmaktadır. Sistemin çekirdeğinde, ham hesap ekstresi bilgisini bir veri kaynağından (harici bir veritabanı) alan ve ardından bu veriler üzerinde bir dizi doğrulama gerçekleştirerek hesap ekstrelerini üreten ve bunları harici bir sağlayıcı tarafından dijital imzaya hazırlan hale getiren bir yığın (batch) işlem bulunmaktadır. Ekstreler sağlayıcıya gönderilir ve sağlayıcı imzalanmış hesap ekstrelerini geri döner. Bu ekstreler, daha sonra müşterilere ekstrelerin gönderilmesini de içeren ek işlemler için BankStat tarafından saklanır. Bu yığın işlem, ayda bir kez otomatik olarak tetiklenir ve çalışması sırasında yaklaşık 2 milyon hesap ekstresi işlenir.

Bu sistem için aşağıdaki kalite niteliği senaryoları (quality attribute scenarios) birincil öneme sahiptir:

- **Güvenilirlik (Reliability):** Normal çalışma koşulları altında, yığın işlem her zaman %100 olarak baştan sona eksiksiz olarak yürütülür.
- **Performans (Performance):** Normal çalışma koşulları altında, yığın işlem başladığında 2 milyon hesap ekstresi en fazla bir saat içinde okunur, işlenir ve imzalama sağlayıcısına gönderilir.
- **Kullanılabilirlik (Availability):** Normal işleme sırasında, veri kaynağından bilgi okurken veya bilgiyi dijital imza için gönderirken bir hata oluşabilir. Bu durumda, yöneticiye bir bildirim gönderilir ve yönetici süreci elle yeniden başlatır. Süreç yeniden başlatıldığında, yalnızca henüz işlenmemiş olan bilgiler işleme tabi tutulur.

Hükümet tarafından konulan zaman kısıtları nedeniyle, sistemin yalnızca çekirdek yığın işlemi geliştirilerek üretime alınmıştır. Bununla birlikte, bu ilk sürüm, hesap ekstresi işlemenin durumunu izlemek, hatalı ekstrelerin yeniden işlenmesini talep etmek ve rapor üretmek için gerekli olan kullanıcı dostu bir arayüz sağlamamıştır. İlk sürümde, süreç yalnızca bir konsoldan elle başlatılıp durdurulabiliyordu. Sisteminin ikinci sürümü için ACME Bankası, bu eksikliklerin daha iyi ele alınabilmesi amacıyla BankStat sisteminin genişletilmesini talep etmiştir.

  
ŞEKİL 6.1 BankStat sistemi için bağlam diyagramı (context diagram)


## 6.1 İş Gerekçesi (Business Case)

Sistemin ikinci sürümü için mimari sürücüler (architectural drivers) aşağıdaki alt bölümlerde sunulmaktadır.

### 6.1.1 Kullanım Durumu (Use Case) Modeli

Şekil 6.2, BankStat’in ikinci sürümü için kullanım durumu modelini göstermektedir. Bu kullanım durumları aşağıda daha ayrıntılı olarak açıklanmaktadır:

| Kullanım Durumu | Açıklama |
|-----------------|----------|
| **UC-1: Ekstre sorgulama ve yeniden işleme (Query and reprocess statements)** | Kullanıcı elle belirli sayıda ekstreden yeniden işleme talep eder. Kullanıcı, yeniden işlenmesi gereken ekstreleri sorgulamak ve seçmek için ölçütler belirtir. Örneğin, ilgilendiği bir dönemi veya ekstrelerin durumunu (örneğin işlenmiş, imzalanmış, imzalanmamış) seçebilir. |
| **UC-2: Oturum açma (Log in)** | Kullanıcı sisteme oturum açar. |
| **UC-3: Rapor üretme (Generate report)** | Kullanıcı, süreçle ilgili raporlar üretir. |
| **UC-4: Kullanıcı kayıtlarını sorgulama (Query users log)** | Yönetici, belirli bir kullanıcının veya bir kullanıcı grubunun aktivitelerini göstermek için kullanıcı kayıtlarını sorgular. Bilgi, tarihler veya işlem türleri gibi ölçütler kullanılarak filtrelenebilir. |

ŞEKİL 6.2 BankStat sistemi için kullanım durumları (Anahtar: UML)

### 6.1.2 Kalite Niteliği Senaryoları (Quality Attribute Scenarios)

Aşağıdaki tablo, sistemin bu genişletmesi için dikkate alınan yeni kalite niteliği senaryosunu göstermektedir.

| ID   | Kalite Niteliği (Quality Attribute) | Senaryo | İlişkili Kullanım Durumu |
|------|-------------------------------------|---------|---------------------------|
| QA-1 | Güvenlik (Security)                | Bir kullanıcı herhangi bir anda sistem üzerinde herhangi bir işlem gerçekleştirir ve kullanıcının gerçekleştirdiği işlemlerin %100’ü, sistem tarafından işlem günlüğünde kaydedilir. | UC-4 |

### 6.1.3 Kısıtlar (Constraints)

Aşağıdaki tablo, sistemin bu genişletmesi için dikkate alınan kısıtları göstermektedir.

| ID    | Kısıt |
|-------|-------|
| CON-1 | Kullanıcıların hesapları ve yetkileri, bankadaki çeşitli uygulamalar tarafından kullanılan mevcut bir kullanıcı dizin sunucusu (user directory server) tarafından yönetilecektir. |
| CON-2 | Veri kaynağıyla iletişim JDBC kullanılarak gerçekleştirilecektir. |
| CON-3 | Dijital imza sağlayıcı sistemiyle iletişim web servisleri (web services) kullanılarak gerçekleştirilecektir. Bu web servisleri, hükümet tarafından belirlenmiş spesifikasyonlara uyan bir XML formatında bilgiyi alır ve geri döner. |
| CON-4 | Sisteme bir web tarayıcısı üzerinden erişilmelidir; ancak erişim yalnızca bankanın intraneti üzerinden mümkündür. |

### 6.1.4 Mimari Kaygılar (Architectural Concerns)

Aşağıdaki tablo, sistemin bu genişletmesi için başlangıçta dikkate alınan kaygıları göstermektedir.

| ID    | Kaygı |
|-------|-------|
| CRN-1 | Geliştirme ekibinin uzmanlığından yararlanmak için sistem Java ve Java ile ilişkili teknolojiler kullanılarak programlanmalıdır. |
| CRN-2 | Yeni işlevselliğin eklenmesi, mümkün olduğunca mevcut yığın işlem çekirdeğinde değişiklik yapılmasını önlemelidir. |

## 6.2 Mevcut Mimari Dokümantasyon (Existing Architectural Documentation)

Bu bölüm, mimaride yapılacak değişiklikler için ilgili bilgileri sağlayan sistem görünüşlerinin (views) basitleştirilmiş bir sürümünü sunmaktadır.

### 6.2.1 Modül Görünümü (Module View)

Şekil 6.3’te gösterilen paket diyagramı, sistem katmanlarını ve bu katmanların içerdiği modülleri betimlemektedir.

ŞEKİL 6.3 BankStat sistemindeki mevcut modüller ve katmanlar (Anahtar: UML)

Bu diyagramda gösterilen öğelerin sorumlulukları aşağıdaki tabloda açıklanmaktadır.

| Öğe | Sorumluluk |
|-----|------------|
| **Yığın İşleme Katmanı (Batch Processing Layer)** | Bu katman, yığın işlemini gerçekleştiren modülleri içerir. Bu bileşenler Spring Batch çatısı (framework) kullanılarak geliştirilmiştir. |
| **Veri Erişim Katmanı (Data Access Layer)** | Bu katman, Yığın İşleme Katmanı’ndaki modüller tarafından kullanılan yerel bir veritabanına veri kaydeden ve bu veritabanından veri alan modülleri içerir. |
| **İletişim Katmanı (Communications Layer)** | Bu katman, harici dijital imza sağlayıcısı ve hesap ekstresi veri kaynağıyla iletişimi destekleyen modülleri içerir. |
| **Yığın İş Koordinatörü (Batch Job Coordinator)** | Bu modül, yığın işlemin yürütülmesini koordine etmekten sorumludur; buna sürecin başlatılması ve bu sürece ilişkin farklı adımların çağrılması dahildir. |
| **İş Adımları (Job Steps)** | Bu modül, yığın işinin parçası olan “adımları” içerir. Bu adımlar, veri kaynağından alınan bilgilerin doğrulanması ve hesap ekstrelerinin üretilmesi gibi faaliyetleri gerçekleştirir. Bu tür adımlar genellikle veriyi okur, işler ve yazar. Veri, yerel veritabanından okunur ve yine bu veritabanına yazılır. |
| **Yerel Veritabanı Bağlayıcısı (Local Database Connector)** | Bu modül, yığın işlemi yürütülürken iş adımlarının bilgi alışverişi için kullandığı yerel veritabanına erişmekten sorumludur. Bu veritabanına, harici veri kaynağından ayırt etmek için “yerel” diyoruz; bu veritabanı yalnızca yerel (yani uygulama tarafından dahili olarak) kullanılır; farklı bir düğüme yerleştirilmiş olsa bile (bkz. bir sonraki bölüm). |

> **💬 Çevirmen notu:** “Batch process / batch job” kavramı, büyük hacimli verinin zamanlanmış toplu işlenmesi anlamına geldiği için “yığın işlem” ve “yığın iş” terimleri korunarak çevrilmiştir; bu terimler kitap boyunca tutarlı biçimde kullanılacaktır.
