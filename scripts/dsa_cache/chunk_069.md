Zengin istemci (rich client) uygulamaları, bir kullanıcının makinesine kurulup o makinede çalıştırılır. Uygulama kullanıcının makinesinde çalıştığı için, kullanıcı arayüzü yüksek performanslı, etkileşimli ve zengin bir kullanıcı deneyimi sağlayabilir. Bir zengin istemci uygulaması, tek başına, bağlı, ara sıra bağlı (occasionally connected) veya bağlantısız kipte çalışabilir. Bağlı olduğunda, tipik olarak diğer uygulamalar tarafından sağlanan uzak servislerle iletişim kurar.

Zengin istemci uygulama modülleri, web uygulamasına benzer şekilde (bkz. Bölüm A.1.1), üç ana katman halinde veya katmanları kesen (cross-cutting) bir gruplaşma biçiminde yapılandırılır. Zengin istemci uygulamalar “ince” (thin) ya da “kalın” (thick) olabilir. İnce istemci (thin client) uygulamalar, esas itibarıyla sunum mantığından oluşur; bu mantık kullanıcı verisini alır ve işlenmek üzere bir sunucuya gönderir. Kalın istemci (thick client) uygulamalar ise iş (business) ve veri mantığını içerir ve tipik olarak yalnızca kalıcı olarak uzakta tutulması gereken bilgiyi alışveriş etmek için bir veri depolama sunucusuna bağlanır. Şekil A.2, zengin istemci uygulamalardaki modüllerle ilişkili bileşenleri sunmaktadır.

Bu tip bir uygulamayı kullanmayı, aşağıdaki durumlarda düşünmelisiniz:
- Uygulamanızı kullanıcıların makinelerine dağıtmak (deploy) istiyorsunuz.
- Uygulamanızın kesintili ya da hiç olmayan ağ bağlantısını desteklemesini istiyorsunuz.
- Uygulamanızın yüksek derecede etkileşimli ve duyarlı olmasını istiyorsunuz.
- Kullanıcının makine kaynaklarından (örneğin bir grafik kartı) yararlanmak istiyorsunuz.

Bu uygulamalar kullanıcının makinesine dağıtıldığından, taşınabilirlikleri daha düşüktür ve dağıtım ile güncelleme daha karmaşıktır. Bununla birlikte, kurulumlarını kolaylaştırmaya yönelik çeşitli teknolojiler mevcuttur.

# A.1 Referans Mimariler

215

**ŞEKİL A.2** Zengin İstemci Uygulaması referans mimarisi (Anahtar: UML)

## A.1.3 Zengin İnternet Uygulamaları

Zengin internet uygulamaları (Rich Internet Applications, RIA) tipik olarak bir tarayıcı içinde çalışır ve Asenkron JavaScript ve XML (AJAX, Asynchronous JavaScript and XML) gibi, tarayıcı tarafından yürütülen kod kullanılarak geliştirilebilir. RIA’lar ayrıca Silverlight gibi bir tarayıcı eklentisi (plug-in) içinde de çalışabilir. Bu uygulamalar, standart web uygulamalarından daha karmaşıktır

216

Ek A—Bir Tasarım Kavramları Kataloğu

ve zengin kullanıcı etkileşimini ve iş mantığını destekler. Ancak, güvenlik kaygıları nedeniyle yerel kaynaklara erişim bakımından genellikle kısıtlanırlar.

Tipik RIA’lar, web uygulamalarında görülen aynı üç katman ve modül yapısı kullanılarak yapılandırılır (bkz. Bölüm A.1.1). RIA’larda bazı iş mantığı istemci makinede yürütülebilir ve bazı veriler yerel olarak saklanabilir. Zengin istemci uygulamalarında olduğu gibi, RIA’lar da görece ince istemciden oldukça kalın istemciye kadar değişen bir yelpazede yer alabilir.

Aşağıdaki tablo, bu referans mimaride (Şekil A.3’te gösterilen) yer alan ve Web Uygulaması referans mimarisinde bulunmayan bileşenlerin sorumluluklarını özetlemektedir:

| Bileşen Adı        | Sorumluluk                                                                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Sunum (Presentation) | Kullanıcı etkileşimini yönetmekten sorumludur (hem UI bileşenlerini hem de UI süreç mantığı bileşenlerini temsil eder).                     |
| Zengin UI motoru (Rich UI engine) | Kullanıcı arayüzü öğelerini eklenti (plug-in) yürütme konteyneri içinde oluşturmaktan (render) sorumludur.                             |
| İşsel işlem (Business processing) | İstemci tarafındaki iş mantığını yönetmekten sorumludur.                                                                         |
| Servis arayüzleri (Service interfaces) | Tarayıcı üzerinde çalışan bileşenler tarafından tüketilen servisleri açığa çıkarmaktan sorumludur.                               |
| Mesaj tipleri (Message types)      | Uygulamanın istemci kısmı ile sunucu kısmı arasında değiş tokuş edilen mesaj türlerini yönetmekten sorumludur.                    |

Bu tip bir uygulamayı kullanmayı, aşağıdaki durumlarda düşünmelisiniz:
- Uygulamanızın zengin bir kullanıcı arayüzüne sahip olmasını, ancak yine de bir tarayıcı içinde çalışmasını istiyorsunuz.
- İşlemenin (processing) bir kısmını istemci tarafında gerçekleştirmek istiyorsunuz.
- Uygulamanızı kullanıcı makinesinde kurulum yapmaya gerek kalmadan, basit bir şekilde dağıtmak ve güncellemek istiyorsunuz.

Ancak, bu tip uygulamalarla ilişkili bazı kısıtlar vardır:
- Uygulama bir korumalı alanda (sandbox) çalışabileceği için yerel kaynaklara erişim sınırlı olabilir.
- Yükleme süresi ihmal edilebilir değildir.
- Eklenti yürütme ortamları tüm platformlarda mevcut olmayabilir.

# A.1 Referans Mimariler

**ŞEKİL A.3** Zengin İnternet Uygulaması referans mimarisi (Anahtar: UML)

217

218

Ek A—Bir Tasarım Kavramları Kataloğu

## A.1.4 Mobil Uygulamalar

Bir mobil uygulama, tipik olarak elde taşınan bir cihazda (handheld device) yürütülür ve genellikle uzakta bulunan bir destek altyapısıyla iş birliği içinde çalışır. Bu uygulamalar, web uygulamasında bulunanlara benzer modüller ve katmanlar kullanılarak yapılandırılır (bkz. Bölüm A.1.1), ancak bu modüllerden türetilen birçok bileşen, ince istemci ya da kalın istemci yaklaşımının izlenmesine bağlı olarak isteğe bağlı olabilir. Şekil A.4’te gösterildiği gibi, asgari düzeyde, kullanıcı etkileşiminden sorumlu bileşenler tipik olarak mevcuttur. Destek altyapısıyla iletişim çoğu zaman güvenilir değildir ve bu uygulamalar normalde, destek altyapısındaki verilerle periyodik olarak eşzamanlanan (synchronize) bir tür yerel veri deposu içerir.

Bu tip bir uygulamayı kullanmayı, aşağıdaki durumlarda düşünmelisiniz:
- Uygulamanızın elde taşınan bir cihazda çalışmasını istiyorsunuz.
- Ağ bağlantısı güvenilir değildir, bu nedenle uygulamanın hem çevrimdışı (offline) hem de ara sıra bağlı kiplere ihtiyaç duyması söz konusudur.

Ancak, bu tip uygulamayla ilişkili önemli bir kısıt vardır:
- Elde taşınan cihazdaki kaynaklar sınırlı olabilir.

## A.1.5 Servis Uygulamaları

Servis uygulamaları, işlevselliği kamusal arayüzler (yani servisler) üzerinden açığa çıkaran, etkileşimsiz uygulamalardır. Servisler, servis tüketici bileşenleri (service consumer components) tarafından, uzaktan ya da servis uygulamasının çalıştığı aynı makineden çağrılabilir. Servisler, Web Servisleri Açıklama Dili (Web Services Description Language, WSDL) gibi bir tanımlama dili kullanılarak tanımlanabilir; işlemler, bir taşıma kanalı (transport channel) üzerinden aktarılan XML tabanlı mesaj şemaları kullanılarak çağrılır. Bunun bir sonucu olarak, servisler birlikte çalışabilirliği (interoperability) teşvik eder.

Diğer referans mimarisi türlerine benzer şekilde, servis uygulamaları katmanlar kullanılarak yapılandırılır (Şekil A.5). Bu uygulamalar etkileşimli olmadığından, sunum katmanına ihtiyaç yoktur. Bu katmanın yerini, servisleri açığa çıkarmaktan ve bilgi alışverişinden sorumlu bileşenleri içeren, RIA’ların sunucu kısmına (bkz. Bölüm A.1.3) benzer bir servis katmanı alır.

# A.1 Referans Mimariler

**ŞEKİL A.4** Mobil Uygulama referans mimarisi (Anahtar: UML)

219

220

Ek A—Bir Tasarım Kavramları Kataloğu

**ŞEKİL A.5** Servis Uygulaması referans mimarisi (Anahtar: UML)

## A.2 Dağıtım Desenleri (Deployment Patterns)

221

Bu tip bir uygulamayı kullanmayı, aşağıdaki durumlarda düşünmelisiniz:
- Uygulamanız insanlar tarafından değil, diğer sistemler tarafından kullanılacak ve bunun bir sonucu olarak bir kullanıcı arayüzüne sahip olmayacak.
- Uygulamanızın ve istemcilerin gevşek bağlı (loosely coupled) olmasını istiyorsunuz.

Servislerin aynı makinede bulunan uygulamalar tarafından tüketildiği durumlar hariç, istemcilerin servis uygulamasıyla iletişim kurabilmesi için ağ bağlantısı gereklidir.

## A.2 Dağıtım Desenleri (Deployment Patterns)
