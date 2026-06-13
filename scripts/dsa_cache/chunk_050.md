6.3.2.5

### Adım 6: Görünümleri Taslak Olarak Çizme ve Tasarım Kararlarını Kaydetme

Şekil 6.5’te gösterilen dağıtım diyagramı (deployment diagram), uygulamaya ev sahipliği yapacak yeni sunucuyu ve harici kullanıcı dizini sunucusunu, ayrıca bunların mevcut düğümlerle olan bağlantılarını göstermektedir.  
Yeni eklenen öğelerin sorumlulukları aşağıdaki tabloda açıklanmıştır.

**Öğe** | **Sorumluluk**
--- | ---
Web/App Sunucusu | Uygulamanın etkileşimli kısmına ev sahipliği yapar.
Kimlik Doğrulama Sunucusu (Auth Server) | Bankadaki birden fazla uygulama için kullanıcıları ve izinleri yöneten mevcut sunucu (CON-1).

Şekil 6.6’da gösterilen paket diyagramı (package diagram), başvuru mimarisinin (reference architecture) nasıl somutlaştırıldığını (instantiate edildiğini) ve birincil kullanım senaryosunu (UC-1) desteklemek için tanıtılan modülleri göstermektedir. Aynı zamanda, bu yeni eklenen öğelerin, önceki sistem sürümünden gelen mevcut katmanlar ve modüllerle nasıl bütünleştirildiğini de göstermektedir.

6.3 Tasarım Süreci

**ŞEKİL 6.5** Ayrıntılandırılmış dağıtım diyagramı (Anahtar: UML)

**ŞEKİL 6.6** UC-1 kullanım senaryosunu desteklemek için tanıtılan modüller (Anahtar: UML)

Bölüm 6—Vaka Çalışması: Bankacılık Sistemi

Yeni eklenen öğelerin sorumlulukları aşağıdaki tabloda açıklanmıştır.

**Öğe** | **Sorumluluk**
--- | ---
Banka Ekstresi Yeniden İşleme Görünümü (Bank Statement Reprocessing View) | Bu modül, kullanıcının işlenmiş banka ekstrelerinin durumunu sorgulamasına imkân veren bir görünüm sağlar. Ayrıca kullanıcıya bu ekstreler arasından yeniden işlenmesi gerekenleri seçme olanağı verir.
Banka Ekstresi Yeniden İşleme Servisi (Bank Statement Reprocessing Service) | Bu modül, görünümden gelen istekleri yönetir; bunlara banka ekstresi bilgisi talep etme, yeniden işlenmesi gereken banka ekstrelerini işaretleme ve toplu işin (batch job) yeniden başlatılmasını tetikleme dahildir.
Güvenlik Yöneticisi (Security Manager) | Spring Security kullanılarak gerçekleştirilmiş olan bu modül, kimlik doğrulama (authentication), yetkilendirme (authorization) ve etkinlik günlüğünü (activity log) (QA-1) ele alır. Ayrıca harici kullanıcı dizini sunucusuyla (CON-1) bütünleştirilmiştir.

Şekil 6.7’de gösterilen sıra diyagramı (sequence diagram), UC-1’in nasıl icra edildiğini göstermektedir. Kullanıcı, banka ekstrelerinin durumunun görüntülenmesini talep eder. Bu bilgi yerel veritabanından Yerel Veritabanı Bağdaştırıcısı (Local Database Connector) tarafından alınır. Görüntülendikten sonra, kullanıcı yeniden işlenecek ekstreleri seçer. Bu banka ekstreleri, yeniden işlenecek şekilde işaretlenir (bir bayrak değeri değiştirilerek) ve bilgi yerel veritabanında güncellenir. Son olarak, toplu iş yeniden başlatılır. Sistemin etkileşimlerinin görünümde Spring Security tarafından kaydedildiğine dikkat edin. Ayrıca, Toplu İş Koordinatörü’nün (Batch Job Coordinator) çağrısının eşzamansız (asynchronous) olduğu, bunun da kullanıcı arayüzünün kilitlenmesi (blocking) sorununu önlediği not edilmelidir.

Sıra diyagramında tanımlanan etkileşimlerden, etkileşim hâlindeki öğelerin arayüzleri için ilk metotlar tanımlanabilir.

**BankStatementReprocessingService**

**Metot Adı** | **Açıklama**
--- | ---
`BankStatement[] getBSStatus(criteria)` | Zaman aralığı veya durum gibi çeşitli ölçütlere göre bir banka ekstresi koleksiyonunu getirir.
`boolean reprocess(BankStatement[])` | Bir banka ekstresi koleksiyonunun yeniden işlenmesini talep eder.

> **💬 Çevirmen notu:** Bu tabloda kullanılan `BankStatement` bir alan nesnesi (domain object) türü olarak düşünülmelidir; metot imzaları mimari seviyede arayüz taslağıdır, ayrıntılı tip tanımları kod aşamasında netleşir.

6.3.2.6

### Adım 7: Mevcut Tasarımın Analizini Yapma ve İterasyon Hedefi ile Tasarım Amacının Gerçekleşmesini Gözden Geçirme

Aşağıdaki Kanban tablosu, çeşitli mimari sürücülerin (architectural driver) durumunu ve bunları ele almak için iterasyon süresince alınan kararları özetlemektedir. Tüm sürücüler tamamen ele alındığından, yalnızca tek bir nitelik temelli tasarım (Attribute-Driven Design, ADD) iterasyonu yeterli olmuştur.

6.3 Tasarım Süreci

**ŞEKİL 6.7** UC-1 kullanım senaryosu için sıra diyagramı (Anahtar: UML)

Bölüm 6—Vaka Çalışması: Bankacılık Sistemi

**Mimari sürücü** | Ele alınma durumu | İterasyon sırasında alınan tasarım kararları
--- | --- | ---
UC-1 | Tamamen ele alındı | Kullanım senaryosunu destekleyen modüller ve arayüzleri, Web Uygulaması Başvuru Mimarisi’ne (Web Application Reference Architecture) dayanarak tanımlandı ve belirlendi.
QA-1 | Tamamen ele alındı | Güvenlik günlükleri (security logs) Spring Security tarafından ele alınmaktadır.
CON-1 | Tamamen ele alındı | Spring Security, mevcut kullanıcı dizini sunucusuna bağlanmakta ve yetkilendirme ile kimlik doğrulamayı desteklemek için bu sunucunun bilgisini kullanmaktadır.
CON-3 | Tamamen ele alındı | Veri kaynağına bağlanan modülde herhangi bir değişiklik yapılmamıştır.
CON-3 | Tamamen ele alındı | Sayısal imza sağlayıcısına bağlanan modülde herhangi bir değişiklik yapılmamıştır.
CON-4 | Tamamen ele alındı | Kullanılan Web Uygulaması Başvuru Mimarisi, özellikle web tarayıcılarından erişimi desteklemektedir.
CRN-1 | Tamamen ele alındı | Seçilen teknolojiler Java ile ilişkilidir.
CRN-2 | Tamamen ele alındı | Mevcut işlevsellikle tümleştirme (entegrasyon), veritabanı üzerinden (Veritabanı Tümleştirme deseni — Database Integration pattern — kullanılarak) yapılmıştır; mevcut işlevsellikte değişiklik yapılmasına gerek kalmamıştır.

## 6.4 Özet

Bu bölümde, nitelik temelli tasarımın (Attribute-Driven Design, ADD) brownfield bir sistem bağlamında kullanımına dair basit (ama gerçek dünyadan) bir örnek sunduk. Bu örneğin gösterdiği gibi, ADD adımları greenfield sistemlerin tasarımı bağlamında olduğu gibi, tam olarak aynı şekilde izlenir. Başlıca fark, tasarım sürecinin girdilerinden birinin mevcut mimari olmasıdır. Bu durum, mimarinin belgelendirilmesinin önemini vurgular: Eğer bu bilgi mevcut olmasaydı, tasarım ve nihai gerçekleştirim (implementasyon) sürecine geçmeden önce, mimarinin uygun bir modelini oluşturmak için, kodun anlaşılması ve tersine mühendisliği (reverse engineering) üzerinde büyük miktarda zaman harcanması gerekirdi.

Brownfield sistemler bağlamında tasarım genellikle, bu örnekle gösterilenden daha kapsamlı değişiklikleri içerir. Bu tür değişiklikler çoğu zaman, tasarım etkinliği sonucunda ortaya çıkan yeni öğeleri ve yeni ilişkileri desteklemek için mevcut mimarinin yeniden düzenlenmesini (refactoring) ve değiştirilmesini gerektirir. Mevcut bir mimariyi değiştirmek, çoğu zaman brownfield sistemler bağlamında tasarım yapmanın en zorlu yönüdür. Brownfield sistemlerde, sistemin bazı kısımlarına ilişkin ayrıntılı bilginin kaybolmuş olması fazlasıyla yaygındır. Bu süreç karmaşık olabileceği ve yapılacak değişikliklerin sonuçlarına dair bir miktar belirsizlik bulunduğu için, bu değişiklikleri koda işlemeden önce önerilen tasarım değişikliklerinin analiz edilmesini öneriyoruz.

## 6.5 Ek Okumalar

Paylaşımlı Veritabanı Tümleştirme deseni (Shared Database Integration pattern), G. Hohpe ve B. Woolf’un şu kitabında tartışılmaktadır:  
*Enterprise Integration Patterns: Designing, Building and Deploying Messaging Solutions*, Addison Wesley Professional, 2003.

Yazılım bakımı ve evrimi konusunda derinlemesine tartışmalar, F. Brooks’un klasik kitabı *The Mythical Man Month*, Addison-Wesley, 1995’te ve ayrıca M. M. Lehman’ın “On Understanding Laws, Evolution, and Conservation in the Large-Program Life Cycle” başlıklı makalesinde bulunabilir (*Journal of Systems and Software*, 1:213–221, 2010).

Bu sayfa özellikle boş bırakılmıştır.

# 7 Diğer Tasarım Yöntemleri
