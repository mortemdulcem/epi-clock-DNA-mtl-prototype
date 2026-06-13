§ Özelleştirilmiş arayüzler (specialized interfaces): Bir bileşenin değişken
değerlerini bir test harness’i (test koşum takımı) aracılığıyla ya da normal çalıştırma sırasında kontrol et veya yakala.

§ Kayıt/yeniden yürütme (record/playback): Bir arayüzden geçen bilgiyi yakala
ve bunu daha ileri testler için girdi olarak kullan.

§ Durum saklamayı yerelleştir (localize state storage): Bir sistemi, altsistemi
veya modülü bir test için keyfi bir durumda başlatmak istiyorsan, bu durumun tek bir yerde saklanması en uygunudur.

§ Veri kaynaklarını soyutla (abstract data sources): Arayüzleri soyutlamak,
test verisini daha kolay ikame etmene olanak tanır.

§ Kum havuzu (sandbox): Deneyin sonuçlarını geri alabilme kaygısından
kurtulmuş bir şekilde deneyselliğe olanak tanımak için sistemi gerçek
dünyadan yalıt.

§ Çalıştırılabilir savlar (executable assertions): Savlar (assertion’lar) genellikle elle kodlanır ve bir programın hatalı durumda olduğunu göstermek
için istenen yerlere yerleştirilir.

---

## Karmaşıklığı Sınırla (Limit Complexity)

§ Yapısal karmaşıklığı sınırla (limit structural complexity): Bileşenler arasındaki döngüsel bağımlılıklardan kaçın veya bunları çöz, dış ortama olan
bağımlılıkları yalıt ve kapsülle, ve genel olarak bileşenler arasındaki
bağımlılıkları azalt.

§ Belirsizliği (nondeterminism) sınırla (limit nondeterminism): Kısıtsız
paralellik gibi tüm belirsizlik kaynaklarını bul ve bunları olabildiğince ortadan kaldır.

---

## A.4.7 Kullanılabilirlik Taktikleri (Usability Tactics)

Şekil A.18, kullanılabilirliğe (usability) ulaşmak için taktikleri özetlemektedir.

### Kullanıcı Girişimini Destekle (Support User Initiative)

§ İptal (cancel): Sistem, iptal isteğini dinlemelidir; iptal edilen komut
sonlandırılmalıdır; kullanılan kaynaklar serbest bırakılmalıdır; ve işbirliği
yapan bileşenler bilgilendirilmelidir.

§ Duraklat/sürdür (pause/resume): Kaynakları geçici olarak serbest bırak ki
diğer görevlere yeniden tahsis edilebilsinler.

§ Geri al (undo): Kullanıcının isteği üzerine önceki bir durumun geri
yüklenebilmesi için sistem durumuna ilişkin yeterli miktarda bilgi tut.

§ Kümelendirme (aggregate): Daha düşük seviyeli nesneleri bir grupta
topla ki, bir kullanıcı işlemi bu gruba uygulanabilsin; böylece kullanıcı
ayrıntılı angaryadan kurtulur.

---

### Kullanılabilirlik Taktikleri

Support User
Initiative  
User
Request  

Support System
Initiative  

Cancel  

Maintain Task Model  

Undo  

Maintain User Model  

Pause/Resume  

Maintain System Model  

Aggregate  

**ŞEKİL A.18** Kullanılabilirlik taktikleri

User Given
Appropriate
Feedback and
Assistance

---

## A.5 Haricen Geliştirilmiş Bileşenler (Externally Developed Components)

Haricen geliştirilmiş bileşenler, çerçeveler (framework) dahil olmak üzere,
Bölüm 2.5.5’te tartışılmıştı. Burada, Bölüm 4’teki vaka çalışmasında kullanılan
Java çerçevelerinden küçük bir örnek sunuyoruz. Her çerçeve çok kısaca
tanımlanmakta ve belirli teknoloji aileleri, desenler (pattern) ve taktiklerle
ilişkilendirilmektedir. Farklı çerçevelere ilişkin tüm ayrıntılar, verilen URL’ler
ziyaret edilerek bulunabilir.

### A.5.1 Spring Framework

| Öğe                     | Açıklama |
|-------------------------|---------|
| **Çerçeve adı (Framework Name)** | Spring Framework |
| **Teknoloji ailesi (Technology family)** | Bağımlılık enjeksiyonu ve yönlendirilen yönelimli programlama (aspect-oriented programming, AOP) konteyneri |
| **Dil (Language)**      | Java |
| **URL**                 | http://projects.spring.io/spring-framework/ |

**Amaç (Purpose)**  
Uygulama çerçevesi, bir uygulamayı oluşturan nesnelerin birbirine bağlanmasına olanak tanır. Ayrıca AOP aracılığıyla farklı kaygıları (concern) destekler.

**Genel Bakış (Overview)**  
Spring konteyneri, standart Java nesnelerini, yani POJO’ları (Plain Old Java Objects) “Application Context” (Uygulama Bağlamı) adı verilen bir XML dosyasındaki bilgileri ya da Java kodundaki anotasyonları kullanarak birbirine bağlar. Bu, nesne bağımlılıklarının konteyner tarafından enjekte edildiği “Denetimin Tersine Çevrilmesi ve Bağımlılık Enjeksiyonu (Inversion of Control and Dependency Injection)” desenidir.

Çerçeve, konteyner nesneleri birbirine bağladığında Java nesneleri arasına vekiller (proxy) olarak sokulan AOP kullanarak çeşitli yönleri (aspect) destekler. Desteklenen yönler şunlardır:

- Güvenlik (Security)  
- İşlem yönetimi (transaction management)  
- Nesne arayüzlerinin yayımlanması; böylece nesnelere uzaktan erişilebilir — örneğin Web Servisleri (Web Services) aracılığıyla

---

| Öğe                     | Açıklama |
|-------------------------|---------|
| **Çerçeve adı (Framework Name)** | Spring Framework |

**Yapı (Structure)**  
Bu diyagram, iki nesnenin çerçevedeki iki önemli unsurla — Spring konteyneri ve application context (uygulama bağlamı) — nasıl bağlandığını gösterir. (Anahtar: UML)

**Uygulanan tasarım desenleri (design patterns) ve taktikler (tactics)**  

- **Desenler (Patterns)**  
  - Denetimin Tersine Çevrilmesi ve Bağımlılık Enjeksiyonu (Inversion of Control and Dependency Injection)  
  - Fabrika (Factory)  
  - Vekil (Proxy)

- **Taktikler (Tactics)**  
  - Kullanılabilirlik (availability): İşlemler (transactions)  
  - Test edilebilirlik (testability): Veri kaynaklarını soyutla (abstract data sources) (arayüz ve uygulamanın ayrılması)

**Yararlar (Benefits)**  

- Mükemmel araç desteği  
- Web UI (Spring MVC, JSF), kalıcılık (persistence) (JPA, Hibernate, iBatis) ve entegrasyon (integration) (JMS) gibi diğer çerçevelerle kolay entegrasyon  
- Apache License 2.0

**Sınırlamalar (Limitations)**  

- Karmaşık çerçeve

---

## A.5 Haricen Geliştirilmiş Bileşenler

### A.5.2 Swing Framework

| Öğe                     | Açıklama |
|-------------------------|---------|
| **Çerçeve adı (Framework Name)** | Swing Framework |
| **Teknoloji ailesi (Technology family)** | Yerel kullanıcı arayüzü (local user interface) |
| **Dil (Language)**      | Java |
| **URL**                 | http://docs.oracle.com/javase/tutorial/uiswing/index.html |

**Amaç (Purpose)**  
Taşınabilir yerel (web olmayan) kullanıcı arayüzlerinin oluşturulmasını destekleyen çerçeve.

**Genel Bakış (Overview)**  
Swing çerçevesi, JFrame (pencereler), JMenu, JTree, JButton, JList ve JTable
gibi kullanıcı arayüzü bileşenlerinden oluşan bir kütüphane sunar. Bu
bileşenler, Model-Görünüm-Kontrolcü (Model View Controller, MVC) ve
Gözlemci (Observer) desenleri etrafında inşa edilmiştir.

JTable gibi bileşenler hem görünüm hem kontrolcü rolünü oynar ve her birinin kendisine karşılık gelen bir model sınıfı (örneğin, `TableModel`) vardır.

Bileşenler, farklı olayları yönetmek için gözlemcilerin (observer) — “dinleyici” (listener) olarak adlandırılır — kaydedilmesine izin verir. Örneğin, JButton bileşenleri, gözlemci olarak `ActionListener`ların kaydedilmesine izin verir; böylece butona tıklandığında bir geri çağırım (callback) metodu (`actionPerformed`) çağrılır.

**Yapı (Structure)**  
Bu diyagram, çerçevenin sınıflarının küçük bir bölümünü temsil eder (Anahtar: UML).

**Uygulanan tasarım desenleri ve taktikler (Implemented design patterns and tactics)**  

- **Desenler (Patterns):**  
  - Model-Görünüm-Kontrolcü (Model View Controller)  
  - Gözlemci (Observer)  
  - Bileşik (Composite) ve Yineleyici (Iterator) gibi diğerleri

**Yararlar (Benefits)**  

- Taşınabilir (herhangi bir işletim sisteminde çalışabilir)  
- Java API’sinin parçası  
- İyi araç desteği

**Sınırlamalar (Limitations)**  

- Yerel (native) UI öğelerini kullanmaktan daha yavaştır  
- Yerel UI öğeleriyle aynı görünüm ve his (look and feel) sunmaz

---

## A.5.3 Hibernate Framework

| Öğe                     | Açıklama |
|-------------------------|---------|
| **Çerçeve adı (Framework Name)** | Hibernate |
| **Teknoloji ailesi (Technology family)** | Nesne yönelimli–ilişkisel eşleyici (object-oriented to relational mapper) |
| **Dil (Language)**      | Java |
| **URL**                 | http://hibernate.org/ |

**Amaç (Purpose)**  
Nesnelerin bir ilişkisel veritabanında kalıcı hale getirilmesini (persistence) basitleştirmek.

**Genel Bakış (Overview)**  
*(Metin burada kesiliyor; devamı bir sonraki parçada geliyor.)*
