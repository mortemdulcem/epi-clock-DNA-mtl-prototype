Dağıtım desenleri (deployment pattern), sistemi fiziksel açıdan nasıl yapılandıracağınıza dair yol gösterir (Bkz. Bölüm 2.5.3). Yazılım sisteminin dağıtımına ilişkin iyi kararlar; performans, kullanılabilirlik (usability), erişilebilirlik (availability) ve güvenlik gibi önemli kalite niteliklerine (quality attribute) ulaşmak için gereklidir. Bu bölüm, Microsoft Application Architecture Guide içinde yer alan katalogdan bir özet niteliğindedir.

## A.2.1 Dağıtılmamış Dağıtım (Nondistributed Deployment)

Dağıtılmamış dağıtımda (nondistributed deployment), farklı katmanlardaki modüllerin tüm bileşenleri, veri depolama işlevselliği dışında, tek bir sunucu üzerinde yer alır (Şekil A.6). Bileşenler yerel olarak iletişim kurduğundan, ağ haberleşmesi gecikmelerinin olmaması performansı iyileştirebilir. Ancak performans, kaynak çekişmesi (resource contention) gibi sistemin diğer yönlerinden de etkilenebilir. Ayrıca bu tür bir uygulama, sistem kaynaklarının en büyük tüketicilerinin tepe kullanımını desteklemek zorundadır. Ölçeklenebilirlik (scalability) ve bakılabilirlik (maintainability), tüm bileşenlerin aynı fiziksel donanımı paylaşması nedeniyle olumsuz etkilenebilir.

**ŞEKİL A.6** Dağıtılmamış dağıtıma örnek (Anahtar: UML)

## A.2.2 Dağıtılmış Dağıtım (Distributed Deployment)

Dağıtılmış dağıtımda (distributed deployment), uygulamanın bileşenleri ayrı fiziksel katmanlarda (tier) bulunur (Şekil A.7). Genellikle belirli katmanlarla ilişkilendirilen bileşenler farklı katmanlarda dağıtılır. Katmanlar, barındırdıkları bileşenlerin gereksinimlerini en iyi karşılayacak şekilde farklı biçimlerde yapılandırılabilir.

Dağıtılmış dağıtım, ölçeklenebilirliği kolaylaştırır; ancak katman eklenmesi, ek maliyet, ağ gecikmesi, karmaşıklık ve dağıtım (deployment) çabasını da beraberinde getirir. Güvenliği artırmak için daha fazla katman da eklenebilir. Her bir katmana göre farklı güvenlik politikaları uygulanabilir ve katmanlar arasına güvenlik duvarları (firewall) yerleştirilebilir. Aşağıdaki alt bölümler, Bölüm A.1’deki referans mimarilerle birlikte kullanılabilecek çeşitli dağıtılmış dağıtım alternatiflerini açıklamaktadır.

**ŞEKİL A.7** Dağıtılmış dağıtıma örnek (Anahtar: UML)

### İki Katmanlı Dağıtım (Two-Tier Deployment, İstemci-Sunucu)

İki katmanlı dağıtım (two-tier deployment), dağıtılmış dağıtımın en temel yerleşim biçimidir. İstemci ve sunucu genellikle, Şekil A.8’de gösterildiği gibi, farklı fiziksel katmanlarda konuşlandırılır.

**ŞEKİL A.8** İki katmanlı dağıtım deseni (Two-tier deployment pattern) (Anahtar: UML)

### Üç Katmanlı Dağıtım (Three-Tier Deployment)

Üç katmanlı dağıtımda (three-tier deployment), uygulama, veritabanını barındıran katmandan ayrı bir katmanda konuşlandırılır (Şekil A.9’da gösterildiği gibi). Bu, web uygulamaları için çok yaygın bir fiziksel yerleşimdir.

**ŞEKİL A.9** Üç katmanlı dağıtım deseni (Three-tier deployment pattern) (Anahtar: UML)

### Dört Katmanlı Dağıtım (Four-Tier Deployment)

Dört katmanlı dağıtımda (four-tier deployment), Şekil A.10’da gösterildiği üzere, web sunucusu ile uygulama sunucusu farklı katmanlarda konuşlandırılır. Bu ayrım genellikle güvenliği iyileştirmek için yapılır; web sunucusu herkese açık bir ağda yer alabilirken, uygulama korunan bir ağda bulunur. Ayrıca katmanlar arasına güvenlik duvarları yerleştirilebilir.

**ŞEKİL A.10** Dört katmanlı dağıtım deseni (Four-tier deployment pattern) (Anahtar: UML)

## A.2.3 Performans Desenleri: Yük Dengelemeli Küme (Load-Balanced Cluster)

Yük Dengelemeli Küme (Load-Balanced Cluster) deseninde, uygulama, iş yükünü paylaşan birden fazla sunucu üzerinde konuşlandırılır (Şekil A.11’de gösterildiği gibi). İstemci istekleri bir yük dengeleyici (load balancer) tarafından alınır ve mevcut yük durumuna göre çeşitli sunuculara yönlendirilir. Farklı uygulama sunucuları aynı anda birçok isteği işleyebilir; bu da performans iyileştirmeleri sağlar.

**ŞEKİL A.11** Yük dengeli küme dağıtım deseni (Load-balanced cluster deployment pattern) (Anahtar: UML)

## A.3 Mimari Tasarım Desenleri (Architectural Design Patterns)

Bu bölüm, Bölüm 4’teki örnek olay incelemesinde kullanılan mimari tasarım desenlerini (Bkz. Bölüm 2.5.2) içermektedir. Burada sunulan desenler, *Pattern-Oriented Software Architecture: A Pattern Language for Distributed Computing, Volume 4* kitabına dayanmaktadır. Parantez içindeki numaralar [örneğin, Domain Model (182)] deseni kitabın hangi sayfasında bulacağınızı göstermektedir.

Bu bölümde desenler için, desenler topluluğunda yaygın olan, bize özgü bir gösterim biçimi kullandığımıza dikkat edin. Sembolleri, ilk diyagrama (Layers) eşlik eden bir lejantta tanımlıyoruz ve bu sembolleri bölüm boyunca kullanıyoruz.

### A.3.1 Yapısal Desenler (Structural Patterns)

Bu desenler, sistemi yapılandırmak için kullanılır, ancak referans mimarilere kıyasla daha az ayrıntı sunarlar.

---

**Adı**  
Layers

**Problem ve bağlam**

Bir Alan Modelini (Domain Model, 182) ekipler arasında paylaştırılabilecek modül kümelerine dönüştürürken, birkaç konuyu desteklememiz gerekir: modüllerin bağımsız geliştirilmesi, modüllerin bağımsız evrimi ve modüller arasındaki etkileşim.

**Çözüm**

Geliştirilmekte olan yazılım için, her katmanın belirgin ve özel bir sorumluluğa sahip olduğu iki veya daha fazla katman tanımlayın. Katmanlamayı daha etkili kılmak için katmanlar arasındaki etkileşimler güçlü biçimde kısıtlanmalıdır. Aşağıda gösterilen en katı katmanlama biçimi, yalnızca tek yönlü bağımlılıklara izin verir ve katman atlayarak erişimi (layer-bridging) yasaklar.

**Yapı**

**Sonuçlar ve ilişkili desenler**

Genellikle, bir katman içindeki her kendi kendine yeterli ve tutarlı sorumluluk ayrı bir alan nesnesi (domain object) olarak gerçekleştirilir. Alan nesneleri, bağımsız olarak geliştirilebilen ve evrilebilen konteynerlerdir (modüller).

---

**Adı**  
Domain Object (Alan Nesnesi)

**Problem ve bağlam**

Bir Alan Modelini (Domain Model, 182) Layers (185) biçiminde gerçekleştirirken, temel kaygılardan biri, kendi kendine yeterli ve bütünlüklü (cohesive) uygulama sorumluluklarını birbirinden ayrıştırmaktır.

**Çözüm**

Her bir belirgin, önemsiz olmayan (nontrivial) uygulama işlevini, alan nesnesi (domain object) denilen kendi kendine yeterli bir yapıtaşı içinde kapsülleştirin.

---

**Adı**  
Domain Object (Alan Nesnesi)

**Yapı**

**Sonuçlar ve ilişkili desenler**

Bir uygulamanın sorumluluklarının alan nesnelerine bölümlenmesi, bir veya daha fazla ayrıntı düzeyi (granularity) ölçütüne dayanır. İşletme özelliklerini, alan kavramlarını veya altyapı bileşenlerini kapsülleyen farklı türlerde alan nesneleri olabilir. Örneğin, alan nesneleri bir gelir vergisi hesaplaması veya para birimi dönüşümü gibi bir işlev ya da bir banka hesabı veya kullanıcı gibi bir alan kavramı olabilir. Alan nesneleri, diğer alan nesnelerini de bir araya getirebilir (aggregate).

Alan nesnelerini tasarlarken, belirli bir işlevselliği dışarıya sunan Açık Arayüzü (Explicit Interface, 281) bu işlevselliği gerçekleştiren Kapsüllenmiş Gerçeklemeden (Encapsulated Implementation, 313) ayırmanız gerekir. Arayüz ile gerçekleştirim ayrımı, modülerleştirmenin kilit unsurudur. Bu ayrım, bağımlılıkları en aza indirir—her alan nesnesi yalnızca açık arayüzlere bağımlıdır, kapsüllenmiş gerçekleştirimlere değil. Bu da bir alan nesnesinin gerçekleştirimini, diğer alan nesnelerinden bağımsız olarak oluşturup evriltmeyi mümkün kılar.

### A.3.2 Arayüz Bölümlendirme (Interface Partitioning)

**Adı**  
Explicit Interface (Açık Arayüz)
