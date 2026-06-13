### Bildirimler Yöneticisi (Notifications Manager)

Bu modül, günlükleri (logları) yönetir ve harici sistemle iletişim hatası gibi sorunlar ortaya çıktığında bildirimler gönderir.

### Veri Kaynağı Bağdaştırıcısı (Data Source Connector)

Bu modül, ham banka hesap özeti bilgisini sağlayan harici veritabanına bağlanmaktan sorumludur.

### Sayısal İmza Sağlayıcı Bağdaştırıcısı (Digital Signature Provider Connector)

Bu modül, banka hesap özetlerinin sayısal olarak imzalanmasını gerçekleştiren harici sisteme erişmekten sorumludur.

## 6.2.2 Yerleştirim Görünümü (Allocation View)

Şekil 6.4’te gösterilen yerleştirim (deployment) diyagramı, düğümlerden (node) ve bunların ilişkilerinden oluşan bir yerleştirim görünümü sunmaktadır.

Şekilde gösterilen öğelerin sorumlulukları aşağıdaki tabloda açıklanmaktadır.

| Öğe                        | Sorumluluk |
|----------------------------|------------|
| Veri Kaynağı Sunucusu (Data Source Server) | Bu sunucu, banka hesap özetlerini üretmek için kullanılan ham veriyi içeren bir veritabanını barındırır. |
| BankStat Sunucusu (BankStat Server) | Bu sunucu, Veri Kaynağı Sunucusu’ndan bilgi almaktan, bu bilgiyi doğrulamaktan ve imzalanmak üzere Sayısal İmza Sunucusu’na göndermekten sorumlu ana toplu işlem (batch process) bileşenini barındırır. |
| Veritabanı Sunucusu (Database Server) | Bu sunucu, BankStat Sunucusu’ndaki toplu işlem tarafından, toplu işlemin yürütülmesinde kullanılan durumu ve bilgiyi tutmak için yerel olarak kullanılan bir veritabanını barındırır. |
| Sayısal İmza Sunucusu (Digital Signature Server) | Harici bir kuruluş tarafından sağlanan bu sunucu, banka hesap özetlerini almak, sayısal olarak imzalamak ve geri göndermekten sorumludur. Sunucu, XML bilgi alan ve üreten web servisleri sağlar. |

## 6.3 Tasarım Süreci (The Design Process)

Burada, ADD (Attribute-Driven Design, nitelik temelli tasarım) yönteminin farklı adımları üzerinden tasarım sürecini açıklıyoruz (Bölüm 3.2’de tartışıldığı gibi). Bu, mevcut sistemde çok büyük bir değişiklik olmadığından, mimar tasarım faaliyetlerinin yalnızca tek bir ADD yinelemesi (iterasyonu) gerektireceğini öngörmektedir.

## 6.3.1 ADD Adım 1: Girdileri Gözden Geçirme (Review Inputs)

ADD yönteminin ilk adımı, girdilerin gözden geçirilmesini içerir. Bunlar aşağıdaki tabloda özetlenmiştir.

| Kategori                         | Ayrıntılar |
|----------------------------------|-----------|
| Tasarım amacı (Design purpose)   | Bu, olgun bir alanda bir “brownfield” sistemdir. Amaç, bir sonraki sistem sürümü için tasarım yapmaktır. |
| Birincil işlevsel gereksinimler (Primary functional requirements) | Bu sürüm için birincil kullanım durumu (use case) UC-1’dir. |
| Kalite niteliği senaryoları (Quality attribute scenarios) | Sistemin bu genişletmesi yalnızca birkaç kalite niteliği senaryosunu içerir; bu nedenle bunların tümü birincil olarak ele alınmaktadır. |
| Kısıtlar (Constraints)           | Bkz. Bölüm 6.1.3. |
| Mimari kaygılar (Architectural concerns) | Bkz. Bölüm 6.1.4. |
| Mevcut mimari tasarım (Existing architecture design) | Bu bir brownfield geliştirme olduğundan, ek bir girdi de bir önceki bölümde açıklanan mevcut mimari tasarımdır. |

> **💬 Çevirmen notu:** “Brownfield” geliştirme, sıfırdan (greenfield) değil, var olan bir sistemin üzerine/yanına geliştirme yapılmasını ifade eder.

## 6.3.2 Yineleme 1: Yeni Sürücülerin Desteklenmesi (Iteration 1: Supporting the New Drivers)

Bu bölüm, örnekte gerçekleştirilen tek yinelemede ADD’in her bir adımında yapılan faaliyetlerin sonuçlarını sunmaktadır.

### 6.3.2.1 Adım 2: Yineleme Hedefini Sürücüleri Seçerek Belirleme (Establish Iteration Goal by Selecting Drivers)

Ele alınması gereken sürücü (driver) sayısı sınırlı olduğundan, mimar tek bir yinelemenin yeterli olduğuna karar vermiştir. Bu yinelemenin amacı, mevcut tasarımı Bölüm 6.1’de listelenen tüm yeni sürücüleri destekleyecek şekilde değiştirmektir.

### 6.3.2.2 Adım 3: Ayrıntılandırılacak Bir veya Daha Fazla Sistem Öğesini Seçme (Choose One or More Elements of the System to Refine)

Ayrıntılandırılacak öğeler, BankStat içindeki ana modülleri ve sistemin yerleştirildiği düğümü (BankStat Sunucusu) içerir. Bu modüllerin ayrıntılandırılmasına ek olarak, uygulamanın barındırıldığı fiziksel düğüm de ayrıntılandırma için bir adaydır.

### 6.3.2.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı Seçme (Choose One or More Design Concepts That Satisfy the Selected Drivers)

Aşağıdaki tablo, tasarım kavramlarının seçilmesine ilişkin alınan tasarım kararlarını özetlemektedir.

| Tasarım Kararları ve Konumu (Design Decisions and Location) | Gerekçe (Rationale) |
|-------------------------------------------------------------|---------------------|
| Web Uygulaması Referans Mimarisi’ni (Web Application Reference Architecture) kullan | Sisteme eklenen kullanım durumları, bir web tarayıcısı üzerinden etkileşim gerektirmektedir (CON-4). Zengin kullanıcı etkileşimine dair bir gereksinim olmadığından, Web Uygulaması mimarisi seçilmiştir (bkz. Bölüm A.1.1). <br><br>Elenen alternatifler: <br>■■ Zengin İnternet uygulaması (Rich Internet Application, bkz. Bölüm A.1.3), çünkü ek geliştirme çabası gerektirecek ve zengin kullanıcı arayüzüne yönelik gereksinim bulunmamaktadır. |
| Yetkilendirme ve kimlik doğrulamayı yönetmek için Spring Security çerçevesini (framework) seç | Güvenlik karmaşık bir konudur ve onu desteklemek için ad hoc (geçici/özel amaçlı) kod yazmak zor ve hataya açıktır. Bu uygulamanın ihtiyaçları arasında yetkilendirme, kimlik doğrulama ve etkinlik günlüğü (activity log) bulunmaktadır. Bu özelliklerin tümü Spring Security çerçevesinde mevcuttur; ayrıca mevcut kullanıcı dizini sunucusuyla (user directory server) kolayca bütünleştirilebilir (CON-1) ve Java ile ilgilidir (CRN-1). <br><br>Elenen alternatifler: <br>■■ Ad hoc kod: Zorlu, hataya açık, geliştirilmesi için önemli miktarda zaman gerektirir. <br>■■ Diğer çerçeveler: Çözümün ilk sürümü hâlihazırda Spring teknolojileri kullanılarak geliştirilmiştir. Bu nedenle, Spring platformundan diğer teknolojileri kullanmaya devam etmek mantıklıdır; çünkü bunlar mevcut çerçevelerle kolayca bütünleştirilebilir. |
| Banka hesap özetlerinin durumuna ilişkin bilgiyi elde etmek için Paylaşılan Veritabanı Bütünleştirme deseni (Shared Database Integration pattern) kullan | Sistemin etkileşimli kısmı, banka hesap özeti işlemlerinin durumunu göstermek için, toplu işlem tarafından yerel olarak kullanılan veritabanını sorgulamalıdır. Toplu (batch) ve etkileşimli kısımlar, aynı veritabanında tutulan veriyi paylaşan iki farklı uygulama (veya alt sistem) olarak görülebilir. Paylaşılan Veritabanı Bütünleştirme deseni, bu bağlamda bu sistemler arasındaki etkileşimi desteklemek için kullanılabilir. Bu yaklaşım, mevcut sistem bölümlerinde değişiklik yapılmasını gerektirmez (CRN-2). <br><br>Elenen alternatifler: <br>■■ Bilginin bir API üzerinden elde edilmesi; bu ise mevcut modüllerde değişiklik yapılmasını gerektirecek ve performans üzerinde olumsuz etki yaratacaktır. |
| Üç katmanlı yerleştirim modelini (three-tier deployment model) kullanarak yerleştirme yap | Uygulamanın web kısmının yerleştirilmesi ayrı bir sunucuda yapılacaktır. Bu nedenle, uygulamanın bu bölümünün yerleştirilmesi, üç katmanlı yerleştirim modelinin bir örneği olarak görülebilir (bkz. Bölüm A.2.2). Bu yaklaşımın faydası, toplu işlemi barındıran sunucunun etkileşimli istekleri işlemek zorunda kalmaması, dolayısıyla performansın zarar görmemesidir. <br><br>Elenen alternatifler: <br>■■ Uygulamanın, toplu işlemin barındırıldığı aynı sunucuda barındırılması. Bu, bazı sunucu maliyetlerinden tasarruf sağlayabilir; ancak toplu işlemin veya etkileşimli işlevlerin performansını sınırlayabilir. |

## 6.3.2.4 Adım 5: Mimari Öğeleri Örnekleme, Sorumlulukları Atama ve Arayüzleri Tanımlama (Instantiate Architectural Elements, Allocate Responsibilities, and Define Interfaces)

Örneklenmiş tasarım kararları ve bunlara ilişkin değerlendirmeler aşağıdaki tabloda özetlenmiştir.

| Tasarım Kararı ve Konumu (Design Decision and Location) | Gerekçe (Rationale) |
|---------------------------------------------------------|---------------------|
| Web uygulamasını ayrı bir sunucuda barındır | Bu tercih, toplu işlem sunucusunda performans düşüşlerini önler ve güvenliği artırır (QA-1). |
| Spring Security’yi harici bir kullanıcı dizini sunucusunu kullanacak şekilde yapılandır | Bu, CON-1’i ele almak içindir. |
