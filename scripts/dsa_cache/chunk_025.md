öğeler ve bunların özellikleri arasındaki ilişkilere yönelik kararlar almayı da
gerektirir. Yine Katmanlar (Layers) desenini ele alalım. İki katmanın bağlı olduğuna karar verebilirsiniz, ancak bu katmanlar sonunda bileşenlere tahsis edilecek ve bu bileşenler de donanıma tahsis edilecektir. Böyle bir durumda, katmanlar bileşenlere tahsis edildikten sonra, bu katmanlar arasındaki iletişimin nasıl
gerçekleşeceğine karar vermeniz gerekir: İletişim eşzamanlı (synchronous) mı yoksa eşzamanlı olmayan (asynchronous) mı? Herhangi bir türde ağ (network) iletişimi içeriyor mu? Hangi tür protokol kullanılıyor? Ne kadar bilgi aktarılıyor ve hangi hızda? Bu tasarım kararları, performans gibi belirli kalite niteliklerine (quality attributes) ulaşma açısından önemli bir etkiye sahip olabilir.

## 3.6 Arayüzlerin (Interface) Tanımlanması

Arayüzler (interfaces), öğelerin dışarıdan görülebilen özellikleridir; öğelerin işbirliği yapmasını ve bilgi alışverişinde bulunmasını sağlayan sözleşmesel bir belirtim (contractual specification) oluştururlar. İki tür arayüz vardır: dışsal (external) ve içsel (internal).

### 3.6.1 Dışsal Arayüzler (External Interfaces)

Dışsal arayüzler; geliştirmekte olduğunuz sistemin ihtiyaç duyduğu diğer sistemlerin arayüzlerini ve sisteminizin diğer sistemlere sunduğu arayüzleri içerir. Gerekli (required) arayüzler, genellikle belirtimlerini etkileme gücünüz olmadığı için sisteminiz açısından bir kısıtın parçasıdır. Sağlanan (provided) arayüzlerin ise resmi olarak tanımlanması gerekir; bu da içsel arayüzleri tanımlamaya benzer biçimde, dış sistemler ile sisteminiz arasındaki etkileşimleri ele alıp bunları daha büyük bir yapının öğeleri olarak görerek yapılabilir.

Tasarım sürecinin başında bir sistem bağlamının (system context) kurulması, dışsal arayüzleri belirlemek için yararlıdır. Bu bağlam, Şekil 3.3’te gösterildiği gibi bir sistem bağlam diyagramı (system context diagram) kullanılarak temsil edilebilir. Dış varlıklar ile geliştirilmekte olan sistem arayüzler üzerinden etkileşime girdiğinden, her dış sistem için en az bir dışsal arayüz (şekildeki her ilişki) bulunmalıdır.

### 3.6.2 İçsel Arayüzler (Internal Interfaces)

İçsel arayüzler, tasarım kavramlarının somutlandırılması (instantiation) sonucunda ortaya çıkan öğeler arasındaki arayüzlerdir. İlişkileri ve arayüz ayrıntılarını belirlemek için, genellikle öğelerin çalışma zamanında (runtime) bilgiyi nasıl değiştokuş ettiğini anlamanız gerekir. Bunu, UML etkileşim şemaları (UML sequence diagrams) gibi modelleme araçlarının yardımıyla başarabilirsiniz (Şekil 3.4). Bu araçlar, kullanım durumlarını (use cases) veya kalite niteliği senaryolarını (quality attribute scenarios) desteklemek için yürütme sırasında öğeler arasında değiş tokuş edilen bilgiyi modellemenize imkân verir.

Bu tür bir analiz, öğeler arasındaki ilişkileri belirlemek için de kullanışlıdır: Eğer iki öğenin doğrudan bilgi alışverişinde bulunması gerekiyorsa, bu öğeler arasında bir ilişki var demektir. Değiş tokuş edilen bilgi, arayüz belirtiminin bir parçası haline gelir. Arayüzler tipik olarak, parametreleri, dönüş değerleri ve muhtemelen özel durumları (exceptions) ile birlikte belirtilmiş bir dizi işlemden (örneğin metotlardan) ve ön/son koşullardan (pre- and postconditions) oluşur. Ancak bazı arayüzler, bir bileşenin bir dosyaya ya da veritabanına bilgi yazdığı ve diğer bir bileşenin daha sonra bu bilgiye eriştiği türde, başka bilgi değiş tokuş mekanizmalarını da içerebilir. Arayüzler, hizmet kalitesi (quality of service) anlaşmaları da koyabilir. Örneğin, arayüzde tanımlanan bir işlemin yürütülmesinin, bir performans kalite niteliği senaryosunu tatmin etmek için zamansal kısıtları olabilir.

Arayüzlerin belirlenmesi, genellikle tüm tasarım yinelemeleri (design iterations) boyunca aynı ayrıntı düzeyinde yapılmaz. Örneğin, sıfırdan (greenfield) bir sistemin tasarımına başlarken, ilk yinelemeleriniz yalnızca katmanlar gibi soyut öğeler üretecek; bu öğeler daha sonraki yinelemelerde ayrıntılandırılacaktır. Katmanlar gibi soyut öğelerin arayüzleri genellikle eksik belirtilmiştir (underspecified). Örneğin, erken bir yinelemede, yalnızca kullanıcı arayüzü (UI) katmanının iş mantığı (business logic) katmanına “komutlar” gönderdiğini ve iş mantığı katmanının da “sonuçlar” geri gönderdiğini belirtmekle yetinebilirsiniz. Tasarım sürecinde ilerledikçe, özellikle belirli kullanım durumlarını ve kalite niteliği senaryolarını ele almak için yapılar oluşturduğunuzda, etkileşime katılan belirli öğelerin arayüzlerini ayrıntılandırmanız gerekecektir.

Bazı özel durumlarda, arayüzlerin belirlenmesi oldukça sadeleşir. Örneğin, Bölüm 5’te sunduğumuz Büyük Veri (Big Data) vaka çalışmasında, arayüzler seçilen teknolojiler tarafından zaten tanımlanmıştır. Arayüzlerin belirtimi bu durumda nispeten önemsiz bir görev haline gelir; zira seçilen teknolojiler birlikte çalışacak biçimde tasarlanmıştır ve dolayısıyla birçok arayüz varsayımını ve kararını zaten “içine işlemiş” durumdadır.

Son olarak, sistem öğesinin tüm içsel arayüzlerinin tasarım sürecinin bir parçası olarak belirlenmeyeceğini göz önünde bulundurmanız gerekir (bkz. yan bilgi kutusu “Eleman Etkileşim Tasarımında Arayüzlerin Belirlenmesi”).

> **💬 Çevirmen notu:** Burada “arayüz” hem programlama dili düzeyindeki API’leri hem de bileşenler, katmanlar ve sistemler arası etkileşim noktalarını kapsayacak geniş bir anlamda kullanılıyor.

---

## 3.6 Arayüzlerin Tanımlanması

Aşağıda, Bölüm 4’teki FCAPS vaka çalışmasından Kullanım Durumu UC-2 (Arıza Tespit et / Detect Fault) için başlangıç niteliğinde bir etkileşim diyagramı (sequence diagram) verilmiştir. Bu diyagram, bir aktör ile UC-2’ye katılan beş bileşen arasındaki etkileşimleri gösterir. Bu diyagramı oluştururken, değiş tokuş edilen bilgiyi, çağrılan metotları ve iletilen ve döndürülen değerleri belirleriz.

:TimeServerConnector

:TimeServerConfigurationController

:TimeServerDataMapper

:Time Server

:TopologyController

Time Server  
addEventListener(this)  
trap()  
eventReceived(event)  
publish(event)  
retrieve(id) :TimeServer  
:TimeServer  
addEvent()  

update(TimeServer)  

:true  

Anahtar: UML  

Bu etkileşimden, etkileşen öğelerin arayüzleri için başlangıç niteliğinde metotlar
belirlenebilir:

**Ad:** `TimeServerConnector`

| Metot adı                       | Açıklama                                                                                 |
|---------------------------------|------------------------------------------------------------------------------------------|
| `boolean addEventListener(:EventListener)` | Bu metot, iş mantığı bileşenlerinin, TimeServer’lardan alınan olaylar için dinleyici olarak kendilerini kaydetmelerine imkân verir. |

**Şekil 3.4** Arayüzleri belirlemek için kullanılan bir etkileşim diyagramı

1. Bu örnekle ilgili daha fazla ayrıntı Bölüm 4’te sunulmaktadır.

---

(62. sayfadan devam)

birlikte çalışabilir (interoperate) olmalarını sağlamakta ve bu nedenle pek çok arayüz varsayımını ve kararını baştan “gömülü” (baked in) olarak içermektedir.

Son olarak, sistem öğesinin tüm içsel arayüzlerinin, tasarım sürecinin bir parçası olarak belirlenmeyeceğini göz önünde bulundurmanız gerekir (bkz. yan bilgi kutusu “Eleman Etkileşim Tasarımında Arayüzlerin Belirlenmesi”).
