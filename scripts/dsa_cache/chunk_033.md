Bu modüller; güvenlik, günlükleme (logging) ve G/Ç (I/O) gibi, farklı katmanlara yayılan işlevselliklere sahiptir.

**Servis arayüzleri (service interfaces)**  
SS  

Bu modüller, istemciler tarafından tüketilen servisleri dışa açar.

**İş modülleri (business modules)**  
SS  

Bu modüller, iş operasyonlarını uygular.

**İş varlıkları (business entities)**  
SS  

Bu varlıklar, alan modelini (domain model) oluşturur.

**Veritabanı erişim modülü (DB access module)**  

Bu modül, iş varlıklarının (nesnelerin) ilişkisel veritabanında kalıcılığından (persistence) sorumludur. Nesne yönelimli-ilişkisel eşlemeyi (object-oriented to relational mapping) gerçekleştirir ve uygulamanın geri kalanını kalıcılığa ilişkin ayrıntılardan yalıtır.

---

## 4.3 Tasarım Süreci

**Öğe (Element)** | **Sorumluluk (Responsibility)**
------------------|----------------------------------
**Zaman sunucusu erişim modülü (Time server access module)** | Bu modül, zaman sunucularıyla iletişimden sorumludur. Farklı türde zaman sunucularıyla iletişimi desteklemek için zaman sunucularıyla olan işlemleri soyutlar ve yalıtır (bkz. QA-2).

Şekil 4.4’teki dağıtım diyagramı (deployment diagram), önceki diyagramdaki modüllerle ilişkili bileşenlerin nereye dağıtılacağını gösteren bir yerleştirme görünümünü (allocation view) taslak olarak sunar.

Öğelerin sorumlulukları şöyle özetlenebilir:

**Öğe (Element)** | **Sorumluluk (Responsibility)**
------------------|----------------------------------
**Kullanıcı iş istasyonu (User workstation)** | Uygulamanın istemci tarafı mantığını barındıran, kullanıcıya ait PC.
**Uygulama sunucusu (Application server)** | Uygulamanın sunucu tarafı mantığını barındıran ve aynı zamanda web sayfalarını sunan sunucu.
**Veritabanı sunucusu (Database server)** | Mevcut (legacy) ilişkisel veritabanını barındıran sunucu.
**Zaman sunucusu (Time server)** | (Harici) zaman sunucularının kümesi.

Ayrıca, diyagramdaki bazı öğeler arasındaki, kayda değer olduğu düşünülen ilişkiler hakkındaki bilgiler aşağıdaki tabloda özetlenmiştir:

**İlişki (Relationship)** | **Açıklama (Description)**
--------------------------|---------------------------
Web/uygulama sunucusu ile veritabanı sunucusu arasında | Veritabanıyla iletişim JDBC protokolü kullanılarak gerçekleştirilecektir.
Web/uygulama sunucusu ile zaman sunucusu arasında | SNMP protokolü kullanılmaktadır (en azından başlangıçta).

```uml
pc :User Workstation

«Java Web Start»
Client-Side
Application

«replicated»
database :Database Server

«replicated»
:Application Server
«JDBC»
Server-Side Application

«SNMP»
:Time Server
```

**ŞEKİL 4.4** FCAPS sistemi için başlangıç dağıtım diyagramı (Anahtar: UML)

---

## 4.3.2.6 Adım 7: Mevcut Tasarımın Analizini Gerçekleştirme ve Yinelemeyi Gözden Geçirme  
Amaç ve Tasarım Amacının Gerçekleştirilmesi

Aşağıdaki tablo, Bölüm 3.8.2’de tartışılan Kanban panosu tekniği kullanılarak tasarım ilerlemesini özetlemektedir.

|                     | Henüz Ele Alınmadı (Not Addressed) | Kısmen Ele Alındı (Partially Addressed) | Tamamen Ele Alındı (Completely Addressed) | Yineleme Sırasında Verilen Tasarım Kararları (Design Decisions Made During the Iteration) |
|---------------------|-------------------------------------|-----------------------------------------|-------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| **UC-1**            |                                     |                                         |                                           | Seçilen referans mimari (reference architecture), bu işlevselliği destekleyecek modülleri kurar.                              |
| **UC-2**            |                                     |                                         |                                           | Seçilen referans mimari, bu işlevselliği destekleyecek modülleri kurar.                                                       |
| **UC-7**            |                                     |                                         |                                           | Seçilen referans mimari, bu işlevselliği destekleyecek modülleri kurar.                                                       |
| **QA-1**            |                                     |                                         |                                           | Senaryoyla ilişkili kullanım durumuna (use case) katılan öğelerin belirlenmesi gerektiği için ilgili bir karar verilmemiştir. |
| **QA-2**            |                                     |                                         |                                           | Zaman sunucularıyla iletişimi kapsülleyen, sunucu uygulamasının veri katmanında bir zaman sunucusu erişim modülü eklenmiştir. Bu bileşenin ve arayüzlerinin ayrıntıları henüz tanımlanmamıştır. |
| **QA-3**            |                                     |                                         |                                           | Çoğaltılması (replicate) gereken, dağıtım deseninden (deployment pattern) türetilen öğelerin belirlenmesi.                    |
| **QA-4**            |                                     |                                         |                                           | Senaryoyla ilişkili kullanım durumuna katılan öğelerin belirlenmesi gerektiği için ilgili bir karar verilmemiştir.            |
| **CON-1**           |                                     |                                         |                                           | Sistemin 3 katman (3-tier) kullanılarak yapılandırılması, birden çok istemcinin uygulama sunucusuna bağlanmasına izin verecektir. Eşzamanlı erişimle ilgili kararlar henüz verilmemiştir. |
| **CON-2**           |                                     |                                         |                                           | Java Web Start teknolojisinin kullanımı, Zengin İstemci’ye (Rich Client) bir web tarayıcısı üzerinden erişilerek indirilebilmesini sağlar. Zengin İstemci Java ile programlandığından, bu durum Windows, OSX ve Linux altında çalışmayı destekler. |

> **💬 Çevirmen notu:** CON-* kısıtlar (constraints), QA-* kalite senaryoları (quality attribute scenarios), UC-* ise kullanım durumlarını (use cases) temsil ediyor.

|                     | Henüz Ele Alınmadı (Not Addressed) | Kısmen Ele Alındı (Partially Addressed) | Tamamen Ele Alındı (Completely Addressed) | Yineleme Sırasında Verilen Tasarım Kararları (Design Decisions Made During the Iteration) |
|---------------------|-------------------------------------|-----------------------------------------|-------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| **CON-3**           |                                     |                                         |                                           | Uygulamayı fiziksel olarak 3 katmanlı (3-tier) dağıtım deseni kullanarak yapılandırmak ve veritabanını, uygulama sunucusunun veri katmanında veritabanı erişim bileşenleri sağlayarak yalıtmak. |
| **CON-4**           |                                     |                                         |                                           | Java Web Start teknolojisinin kullanımı, istemcinin yalnızca ilk seferde ve ardından yükseltmeler olduğunda indirilmesini gerektirir. Bu, sınırlı bant genişliğine sahip bağlantıları desteklemek için yararlıdır. Sunum (presentation) ve iş mantığı (business logic) katmanları arasındaki iletişimle ilgili daha fazla karar verilmesi gerekmektedir. |
| **CON-5**           |                                     |                                         |                                           | İlgili bir karar verilmemiştir.                                                                                                |
| **CON-6**           |                                     |                                         |                                           | İlgili bir karar verilmemiştir.                                                                                                |
| **CRN-1**           |                                     |                                         |                                           | Referans mimarilerin ve dağıtım deseninin seçimi.                                                                              |
| **CRN-2**           |                                     |                                         |                                           | Bu noktaya kadar dikkate alınan teknolojiler, geliştiricilerin bilgisini göz önüne almaktadır. Diğer teknolojilerin (örneğin, zaman sunucularıyla iletişim) hâlâ seçilmesi gerekmektedir. |
| **CRN-3**           |                                     |                                         |                                           | İlgili bir karar verilmemiştir.                                                                                                |

---

## 4.3.3 Yineleme 2: Birincil İşlevselliği Destekleyecek Yapıların Belirlenmesi

Bu bölüm, FCAPS sistemi için tasarım sürecinin ikinci yinelemesinde, ADD (Attribute-Driven Design, nitelik temelli tasarım) adımlarının her birinde gerçekleştirilen etkinliklerin sonuçlarını sunar. Bu yinelemede, birinci yinelemede kullanılan genel ve kaba taneli (coarse-grained) işlevsellik tanımlarından, uygulamayı yönlendirecek ve dolayısıyla geliştirme ekiplerinin oluşumunu belirleyecek daha ayrıntılı kararlara geçiyoruz.

Genelden özele bu geçiş kasıtlıdır ve ADD yönteminin içine gömülmüştür. Her şeyi en baştan tasarlayamayız; bu nedenle tasarımın sistematik şekilde yapılmasını, önce en büyük risklerin ele alınmasını ve oradan giderek daha ince ayrıntılara ilerlenmesini sağlamak için hangi kararları ne zaman vereceğimiz konusunda disiplinli olmamız gerekir. İlk yinelemedeki hedefimiz, genel bir sistem yapısı kurmaktı. Bu hedef yerine getirildiğine göre, bu ikinci yineleme için yeni hedefimiz, ekip oluşumunu, arayüzleri ve geliştirme görevlerinin nasıl dağıtılabileceğini, dışarıya verilebileceğini (outsourced) ve sprint’ler içinde uygulanabileceğini etkileyen uygulama birimleri (units of implementation) hakkında muhakeme etmektir.

---

4.3.3.1  
### Adım 2: Yineleme Hedefini Sürücüleri Seçerek Belirleme

Bu yinelemenin hedefi, birincil işlevselliği destekleyecek yapıların belirlenmesi şeklindeki genel mimari kaygıyı ele almaktır. Bu öğelerin belirlenmesi, yalnızca işlevselliğin nasıl desteklendiğini anlamak için değil, aynı zamanda CRN-3’ü — yani, işin geliştirme ekibi üyelerine tahsis edilmesini (allocation of work) — ele almak için de yararlıdır.

Bu ikinci yinelemede, CRN-3’e ek olarak, mimar sistemin birincil kullanım durumlarını dikkate alır:

- UC-1  
- UC-2  
- UC-7  

---

4.3.3.2  
### Adım 3: Ayrıntılandırılacak Bir veya Daha Fazla Sistem Öğesini Seçme

Bu yinelemede ayrıntılandırılacak öğeler, önceki yinelemede seçilen iki referans mimarinin tanımladığı farklı katmanlarda bulunan modüllerdir. Genel olarak, bu sistemde işlevselliğin desteklenmesi, farklı katmanlarda bulunan modüllerle ilişkili bileşenlerin iş birliğini gerektirir.

---

4.3.3.3  
### Adım 4: Seçilen Sürücüleri Karşılayacak Bir veya Daha Fazla Tasarım Kavramı Seçme
