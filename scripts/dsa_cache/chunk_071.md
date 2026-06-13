Katmanlar (Layers, 185) ve bunların bileşeni olan Alan Nesneleri (Domain Objects, 208) tasarlanırken, önemli bir kaygı bileşen (modül) arayüzlerinin nasıl doğru şekilde oluşturulacağıdır. Bir modül, yayımlanmış bir arayüze sahip, kendi içinde bütün bir işlevsellik birimidir (ve kendi içinde bütün bir dağıtım birimidir). İstemciler, kendi işlevselliklerini sunarken mevcut modülleri yapı taşı olarak kullanabilirler. Modülün uygulamasına (implementation) doğrudan erişim, istemcileri modülün iç ayrıntılarına bağımlı hâle getirebilir; bu da nihayetinde bağlaşımı (coupling) artırır ve uygulamanın evrimleşme yeteneğini aşındırır.

### Çözüm

Bir modülün açık (explicit) arayüzünü, uygulamasından ayır. Açık arayüzü modülün istemcilerine aç, ancak uygulamasını özel (private) tut.

---

### Ad

Explicit Interface (Açık Arayüz)

### Yapı

### Sonuçlar ve ilgili desenler

İstemciden açık bir arayüz üzerinden yapılan bir çağrı, uygulamaya iletilir; ancak istemci kodu yalnızca genel (public) arayüze bağımlı olur, uygulamaya değil.  

Böylece açık arayüz, bileşenin arayüzünün uygulamasından ayrılmasını zorunlu kılar. Bu ayrım, bir bileşenin uygulamasının değiştirilebileceği ve arayüzler değişmediği sürece onu kullanan istemcilerin etkilenmeyeceği anlamına gelir.

---

### Ad

Proxy (Vekil)

### Problem ve bağlam

Bir Explicit Interface (Açık Arayüz, 281) belirtirken, bileşen uygulamasının sunduğu hizmetlere doğrudan erişmekten kaçınmak isteyebiliriz; çünkü bu hizmetler değişebilir ya da hatta çalıştırma zamanına kadar bilinmeyebilir.

Modern yazılım sistemlerinin çoğu, bazısını kendinizin, bazısını ise başkalarının oluşturduğu iş birliği içindeki bileşenlerden oluşur. Bileşenleriniz, diğer bileşenler tarafından sunulan hizmetlere erişir ve bu hizmetleri kullanır. Bir bileşenin hizmetlerine doğrudan erişmek pratik olmayabilir, hatta imkânsız olabilir; örneğin uygulama, uzak bir sunucuda bulunduğu için.

### Çözüm

Bileşenle etkileşime yönelik tüm ayrıntıları, vekil (proxy) denen bir temsilci içinde kapsülle ve istemcilerin konu bileşenle (subject component) doğrudan değil, bu proxy üzerinden iletişim kurmasına izin ver.

### Yapı

### Sonuçlar ve ilgili desenler

Bir proxy, hem istemciyi hem de konu bileşenleri, bileşene özgü “ev işleri” (housekeeping) işlevlerini uygulama zorunluluğundan kurtarır. İstemciler açısından, gerçek konu bileşene mi yoksa onun proxy’sine mi bağlı oldukları şeffaftır; çünkü her ikisi de özdeş bir arayüz yayımlar.  

Proxy’nin olumsuz yanlarından biri, her istemci etkileşimine ek bir çalıştırma (execution) süresi eklemesidir; ancak uygulamanız gecikmeye (latency) karşı son derece duyarlı değilse, bu ek yük büyük olasılıkla pek önemli olmayacaktır.

---

## A.3.3 Eşzamanlılık (Concurrency)

### Ad

Half-Sync/Half-Async (Yarı-Senkron/Yarı-Asenkron)

### Problem ve bağlam

Eşzamanlı (concurrent) yazılım geliştirirken kritik bir kaygı, eşzamanlı programlamanın, çalıştırma zamanı verimliliğinden ödün vermeden göreli olarak basit olmasını sağlamaktır.

Eşzamanlı yazılım genellikle hizmet isteklerini hem asenkron hem de senkron olarak işler. Asenkrorluk (asynchrony), düşük seviyeli hizmet isteklerini (olaylar gibi) verimli şekilde işlemek için kullanılırken, senkron işleme, uygulama hizmetlerinin işlenmesini basitleştirmek için kullanılır. Her iki programlama modelinin de faydalarından yararlanmak için, bu iki tür işlemenin koordine edilmesi esastır.

### Çözüm

Eşzamanlı yazılımın hizmetlerini, senkron ve asenkron olmak üzere iki ayrı akışa veya “katmana” ayrıştır ve bunlar arasındaki iletişimi aracılık etmek için bir kuyruklama “katmanı” ekle.

### Yapı

### Sonuçlar ve ilgili desenler

Bu desen, alan işlevselliği ya da veritabanı sorguları gibi karmaşık hizmet isteklerini, ayrı iş parçacıklarında senkron olarak işlemeni sağlar. Benzer şekilde, donanım kesmelerine yanıt veren protokol işleyicileri gibi daha düşük seviyeli sistem hizmetleri, asenkron olarak ele alınır. Senkron katmandaki hizmetlerin, asenkron katmandaki hizmetlerle iletişim kurması gerektiği durumlarda, mesajlarını kuyruklama katmanı aracılığıyla değiştokuş edebilirler.

Half-Sync/Half-Async düzeni, üç farklı yürütme ve iletişim modelini kapsüller hâlde tutmak ve dolayısıyla birbirlerinden bağımsız kılmak için Katmanlar (Layers, 185) kullanır.

---

## A.3.4 Veritabanı Erişimi

### Ad

Data Mapper (Data Access Object [DAO]) (Veri Eşleyici / Veri Erişim Nesnesi)

### Problem ve bağlam

Bir Veritabanı Erişim Katmanı (Database Access Layer, 538) tasarlarken, verinin kalıcı depoda nasıl temsil edildiğinin ayrıntılarından —örneğin hangi özel SQL sorgularının kullanılacağından— uygulamaları yalıtmamız gerekir.

Nesne yönelimli (object-oriented) uygulamalar ve ilişkisel veritabanları, veriyi temsil etmek için farklı soyutlamalar kullanır. Bununla birlikte birçok uygulama, veriyi bu iki “dünya” arasında transfer etmek zorundadır. Nesne yönelimli alan modelinin, ilişkisel veritabanı şemasından habersiz kalması arzu edilir. Böylece bir alan modelindeki değişikliklerin diğerine zincirleme etkide bulunma olasılığı azalır.

### Çözüm

Kalıcı her bir uygulama nesne türü için bir data mapper (veri eşleyici) tanıt. Bu eşleyicinin sorumluluğu, veriyi nesnelerden veritabanına ve tersi yönde transfer etmektir.

### Yapı

### Sonuçlar ve ilgili desenler

Bir data mapper, nesne yönelimli alan modeli ile ilişkisel veritabanı arasında veriyi taşıyan bir arabulucudur (mediator). Bir istemci, uygulama verisini veritabanında depolamak veya geri almak için data mapper’ı kullanabilir. Data mapper gerekli veri dönüşümlerini gerçekleştirir ve iki temsil arasındaki tutarlılığı korur.

Data mapper kullanıldığında, bellekteki nesnelerin bir veritabanının varlığından haberdar olması bile gerekmez. Bu nedenle SQL koduna ihtiyaç duymazlar ve veritabanı şemasından bütünüyle habersiz olabilirler. Ayrıca, ilişkisel veritabanı şeması ile nesne yönelimli alan modeli birbirinden bağımsız olarak evrimleşebilir. Bu da, herhangi bir soyutlama arayüzünün sağladığı ek bir faydayı getirir: Birim testini (unit testing) basitleştirir; çünkü veritabanına yönelik mapper’ların, bellek içi testleri destekleyen sahte (mock) nesnelerle değiştirilmesine olanak tanır.

Data mapper, uygulama nesnelerini basitleştirir ve dış bağımlılıklarını azaltır; bu da onların evrimleşmesini kolaylaştırır.  

Ancak Data Mapper deseninin iki potansiyel olumsuz yanı vardır:  
1. Uygulama nesne modelinde veya veritabanı şemasında yapılan değişiklikler, data mapper’da da değişiklik gerektirebilir.  
2. Ek bir dolaylılık (indirection) düzeyi, her veri erişimine ek yük ve dolayısıyla gecikme (latency) getirir; bu da örneğin, katı gerçek-zamanlı (hard real-time) son teslim sürelerine sahip sistemler için sorun oluşturabilir.

---

## A.4 Taktikler (Tactics)

Taktikler, Bölüm 2.5.4’te sunulmuştu. Burada, yaygın olarak karşılaşılan yedi kalite niteliği (quality attribute) için özetlenmiş bir taktik kataloğu sunuyoruz. Bu katalog, *Software Architecture in Practice* kitabından alınmıştır.

### A.4.1 Kullanılabilirlik (Availability) Taktikleri

Şekil A.12, kullanılabilirliğe ulaşmak için kullanılan taktikleri özetlemektedir.

#### Kullanılabilirlik Taktikleri (Availability Tactics)

**Hatalardan Kurtulma (Recover from Faults)**

**Hataları Algıla (Detect Faults)**

**Hazırlık ve Onarım (Preparation and Repair)**

- Ping / Echo  
- Monitor (İzleme)  
- Heartbeat (Kalp Atışı)  
- Timestamp (Zaman Damgası)  
- Fault (Hata)

- Active Redundancy (Aktif Yedeklilik)  
- Passive Redundancy (Pasif Yedeklilik)  
- Spare (Yedek)

- Sanity Checking (Sağduyu Kontrolü / Basit Tutarlılık Kontrolü)  
- Exception Handling (İstisna İşleme)  
- Condition Monitoring (Durum İzleme)  
- Rollback (Geri Alma)  
- Voting (Oylama)  
- Software Upgrade (Yazılım Yükseltmesi / Güncellemesi)  
- Exception Detection (İstisna Algılama)  
- Retry (Yeniden Deneme)  
- Self-Test (Kendini Test)
