Kuruluşunuzda atılabilecek sonraki adımları da düşünebilirsiniz. Değişim için bir araç olabilirsiniz. Şirketiniz mimariye “inanmıyor” olsa bile, bu kitapta ve nitelik temelli tasarımda (Attribute-Driven Design, ADD) somutlaşan fikirlerin çoğunu yine de uygulayabilirsiniz. Gereksinimleriniz için tepki hedefleri (response goals) talep ederek, gereksinimlerinizin net olduğundan emin olun. Sıkıştırılmış teslim tarihleri ve takvim baskılarıyla karşı karşıya olsanız bile, kullanılan başlıca mimari tasarım kavramları konusunda uzlaşmaya çalışın. Meslektaşlarınızla, bir beyaz tahtanın etrafında toplanarak hızlı ve gayriresmî tasarım gözden geçirmeleri yapın ve kendinize yansıtıcı sorular sorun. Bu “sonraki adımlar”ın hiçbiri göz korkutucu veya son derece zaman alıcı olmak zorunda değil. Ve biz, sanayi deneyimimizin de gösterdiği üzere, bunların kendi kendini pekiştiren bir yapıda olduğuna inanıyoruz. Daha iyi tasarımlar, daha iyi sonuçlara yol açacak, bu da sizi, ekibinizi ve kuruluşunuzu aynı şeyleri daha fazla yapmak istemeye yönlendirecektir.

Son olarak, yerel yazılım mühendisliği topluluğunuza ve hatta dünya çapındaki yazılım mimarları topluluğuna katkıda bulunabilirsiniz. Örneğin, yerel bir yazılım mühendisliği buluşmasında mimari oyunu oynayabilir ve ardından deneyimlerinizi paylaşabilirsiniz. Gerçek dünya projelerinde, bir mimar olarak başarılarınız ve başarısızlıklarınız hakkında vaka çalışmaları (case study) sunabilirsiniz. Örneğin en iyi öğretme yolu olduğuna güçlü biçimde inanıyoruz; bu kitapta üç vaka çalışması sunmuş olsak da, daha fazlası her zaman daha iyidir. Günümüz web’inde kendi kendine yayıncılık son derece kolaydır. Mutlu mimarileştirmeler!

## 10.3 Ek Okuma

Bu bölümde yer alan uzun Fred Brooks alıntısı, düşündürücü kitabı The Design of Design: Essays from a Computer Scientist (Pearson, 2010) içinden alınmıştır. Bu bölümdeki, bu kitaptaki ve genel olarak yazılım mimarisi alanındaki pek çok fikri, tasarım bilimi üzerine olan öncü eser, Herbert Simon’ın The Sciences of the Artificial (MIT Press, 1969) adlı kitabına kadar götürmek mümkündür.

# A  
Bir Tasarım Kavramları Kataloğu

Bu bölüm, kurumsal uygulamalar alanıyla ilişkili tasarım kavramlarını gruplayan bir katalogdan bir alıntı sunmaktadır; bunlara Bölüm 4’te sunulan vaka çalışmasındaki uygulama da dahildir. Yalnızca tek tür tasarım kavramını listeleyen, örneğin desen katalogları gibi, geleneksel katalogların aksine, burada sunulan katalog, ilişkili tasarım kavramlarının farklı türlerini bir araya getirmektedir. Bu durumda katalog, örnek mimariler (reference architectures), dağıtım desenleri (deployment patterns), tasarım desenleri (design patterns), taktikler (tactics) ve dışarıda geliştirilmiş bileşenleri (çerçeveler, frameworks) içermektedir. Ayrıca, bu katalogda yer alan tasarım kavramları, gerçek hayattaki tasarımda olduğu gibi, farklı kaynaklardan derlenmiştir. Tasarım kavramları oldukça özlü bir biçimde sunulmuştur ve daha fazla ayrıntı arayan okur, bölüm sonunda verilen kaynakları kullanarak özgün kaynaklara başvurmalıdır.

## A.1 Örnek Mimariler (Reference Architectures)

Örnek mimariler, bir uygulamanın nasıl yapılandırılacağına dair bir plan sunar (bkz. Bölüm 2.5.1). Bu bölüm, Microsoft Application Architecture Guide içindeki katalog temel alınarak hazırlanmıştır.

> **💬 Çevirmen notu:** “Reference architecture” terimi, belirli bir alan için sık kullanılan, yeniden kullanılabilir mimari çözüm şablonu anlamında kullanılır; somut bir sistemin değil, o tür sistemlerin “tipik” yapısının tarifidir.

---

## A.1.1 Web Uygulamaları

Bu web uygulaması genellikle bir web tarayıcısı tarafından başlatılır; tarayıcı bir sunucu ile HTTP protokolü üzerinden iletişim kurar. Uygulamanın büyük kısmı sunucuda bulunur ve mimarisi tipik olarak üç katmandan oluşur: sunum, iş ve veri katmanları. Sunum katmanı, kullanıcı etkileşimini yönetmekten sorumlu modülleri içerir. İş katmanı, iş mantığıyla ilgili yönleri ele alan modülleri içerir. Veri katmanı, verinin yerel ya da uzaktan depolanmasını yöneten modülleri içerir. Buna ek olarak, katmanlar arasında ortak olan belirli işlevler, kesme boyutlu kaygılar (cross-cutting concerns) olarak organize edilir. Bu kesme boyutlu işlevsellik, güvenlik, günlükleme (logging) ve hata yönetimi (exception management) ile ilgili yönleri içerir. Şekil A.1, web uygulamalarındaki modüllerle ilişkili bileşenleri göstermektedir.

Aşağıdaki tablo, bu örnek mimaride bulunan bileşenlerin sorumluluklarını özetlemektedir:

| Bileşen Adı          | Sorumluluk |
|----------------------|------------|
| Tarayıcı (Browser)   | İstemci makinede çalışan bir web tarayıcısı. |
| Kullanıcı arayüzü (User interface) | Bu bileşenler, kullanıcı etkileşimlerini almak ve kullanıcılara bilgi sunmaktan sorumludur. Butonlar ve metin alanları gibi kullanıcı arayüzü (UI) elemanlarını içerirler. |
| UI süreç mantığı (UI process logic) | Bu bileşenler, uygulamanın kullanım senaryolarının (use cases) kontrol akışını yönetmekten sorumludur. Ayrıca veri doğrulama, iş mantığıyla etkileşimleri orkestre etme ve iş katmanından gelen veriyi kullanıcı arayüzü bileşenlerine sağlama gibi yönlerden de sorumludurlar. |
| Uygulama cepheyi (Application facade) | Bu bileşen opsiyoneldir. İş mantığı bileşenlerine yönelik basitleştirilmiş bir arayüz (facade) sağlar. |
| İş akışı (Business workflow) | Bu bileşenler, birden çok kullanım senaryosunun yürütülmesini içerebilen, uzun süreli iş süreçlerini yönetmekten sorumludur. |
| İş mantığı (Business logic) | Bu bileşenler, uygulama verisini alma ve işleme ve bu veri üzerinde iş kurallarını uygulamadan sorumludur. |
| İş varlıkları (Business entities) | Bu bileşenler, iş alanına (business domain) ait varlıkları ve bunlara ilişkin iş mantığını temsil ederler. |
| Veri erişimi (Data access) | Bu bileşenler, kalıcılık (persistence) mekanizmalarını kapsüller ve bilgi almada ve saklamada kullanılan ortak işlemleri sağlar. |
| Yardımcılar ve yardımcı araçlar (Helpers and utilities) | Bu bileşenler, veri katmanındaki diğer modüllere ortak olan ancak hiçbirine özgü olmayan işlevselliği içerir. |
| Servis ajanları (Service agents) | Bu bileşenler, dış servislerle veri alışverişinde kullanılan iletişim mekanizmalarını soyutlar. |
| Güvenlik (Security) | Bu bileşenler, yetkilendirme (authorization) ve kimlik doğrulama (authentication) gibi güvenlik yönlerini ele alan kesme boyutlu işlevselliği içerir. |
| İşlem yönetimi (Operation management) | Bu bileşenler, hata yönetimi (exception management), günlükleme (logging), ölçümleme (instrumentation) ve doğrulama (validation) gibi kesme boyutlu işlevselliği içerir. |
| İletişim (Communication) | Bu bileşenler, katmanlar ve fiziksel katmanlar (tiers) arasındaki iletişim mekanizmalarını ele alan kesme boyutlu işlevselliği içerir. |

**ŞEKİL A.1** Web uygulaması örnek mimarisi (Anahtar: UML)

Web uygulaması türünü kullanmayı şu durumlarda düşünmelisiniz:

- Zengin bir kullanıcı arayüzüne ihtiyaç duymuyorsanız.  
- Uygulamayı, istemci makineye herhangi bir şey kurarak dağıtmak istemiyorsanız.  
- Kullanıcı arayüzünün taşınabilirliğine ihtiyaç duyuyorsanız.  
- Uygulamanızın İnternet üzerinden erişilebilir olması gerekiyorsa.  
- İstemci tarafında asgari düzeyde kaynak kullanmak istiyorsanız.

## A.1.2 Zengin İstemci Uygulamaları (Rich Client Applications)
