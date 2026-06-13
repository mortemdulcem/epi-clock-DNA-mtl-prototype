Referans mimariler, belirli türdeki uygulamalar için genel bir mantıksal yapı sağlayan taslaklardır. Bir referans mimarisi, bir veya daha fazla mimari desen (architectural pattern) üzerine eşlenmiş bir referans modeldir (reference model). İş ve teknik bağlamlarda kendini kanıtlamıştır ve kullanımını kolaylaştıran bir dizi destekleyici yapıt (artifact) ile birlikte gelir.

Web uygulamalarının geliştirilmesi için bir referans mimarisi örneği, bir sonraki sayfadaki Şekil 2.3’te gösterilmektedir. Bu referans mimarisi, bu tür uygulamalar için temel katmanları—sunum (presentation), iş (business) ve veri (data)—belirlemenin yanı sıra, bu katmanlar içinde yer alan öğe türlerini ve bu öğelerin sorumluluklarını da tanımlar; örneğin, UI bileşenleri, iş bileşenleri, veri erişim bileşenleri (data access components), servis aracıları (service agents) vb. Ayrıca bu referans mimarisi, ele alınması gereken güvenlik (security) ve iletişim (communication) gibi kesen ilgileri (cross-cutting concerns) de tanıtır. Bu örneğin gösterdiği gibi, uygulamanız için bir referans mimarisi seçtiğinizde, tasarım sırasında ele almanız gereken bir dizi meseleyi de benimsemiş olursunuz. İletişim veya güvenlikle ilgili açık bir gereksiniminiz olmasa bile, bu öğelerin referans mimarisinin parçası olması, onlar hakkında tasarım kararları vermenizi gerektirir.

Referans mimariler mimari stillerle (architectural styles) karıştırılabilir, ancak bu iki kavram farklıdır. Mimari stiller (örneğin “Boru ve Filtre (Pipe and Filter)” ve “İstemci–Sunucu (Client–Server)”), bir uygulamayı mantıksal veya fiziksel olarak yapılandırırken faydalı olan, belirli bir topolojideki bileşen ve bağlaç (connector) türlerini tanımlar. Bu tür stiller teknoloji ve alan (domain) bağımsızdır. Buna karşılık, referans mimariler belirli alanlardaki uygulamalar için bir yapı sunar ve farklı stilleri barındırabilir. Ayrıca, mimari stiller akademide popüler olma eğilimindeyken, referans mimariler uygulayıcılar tarafından tercih edilmektedir—ki bu da, tasarım kavramları listemizde onları tercih etmemizin nedenlerinden biridir.

Pek çok referans mimarisi bulunmasına rağmen, bunların kapsamlı bir listesini içeren herhangi bir katalogdan haberdar değiliz.

## 2.5.2 Mimari Tasarım Desenleri

Tasarım desenleri (design patterns), tanımlanmış bir bağlamda yinelenen tasarım problemlerine yönelik kavramsal çözümlerdir. Tasarım desenleri başlangıçta örnekleme (instantiation), yapılandırma ve davranış gibi nesne ölçeğindeki kararlara odaklanırken, günümüzde farklı ayrıntı düzeylerindeki (granularity) kararlara hitap eden desen katalogları mevcuttur. Buna ek olarak, güvenlik veya tümleştirme (integration) gibi kalite niteliklerini (quality attributes) ele almak için özel desenler de vardır.

Bazı kişiler, mimari desen (architectural pattern) olarak gördükleri şey ile daha ince taneli (fine-grained) tasarım desenleri arasında bir ayrım yapılması gerektiğini savunsa da, bunun yalnızca ölçeğe bağlanabilecek ilkeli (prensip temelli) bir fark olduğuna inanmıyoruz. Bir deseni, kullanımı bazı mimari sürücülerin (architectural drivers; bkz. Bölüm 2.2) doyurulmasını doğrudan ve önemli ölçüde etkilediğinde mimari kabul ediyoruz.

Şekil 2.4, sistemi yapılandırmak için yararlı bir mimari desen olan Katmanlar (Layers) desenine bir örnek göstermektedir. Bu tür bir deseni seçtiğinizde, sisteminiz için kaç katmana ihtiyaç duyacağınıza karar vermelisiniz. Şekil 2.5, performansı artırmak için yararlı olan ve eşzamanlılığı (concurrency) destekleyen bir deseni göstermektedir. Bu desenin de somutlaştırılması (instantiation), yani belirli problem ve tasarım bağlamına uyarlanması gerekir. Somutlaştırma Bölüm 3’te ele alınmaktadır.

Her ne kadar referans mimariler bir tür desen olarak değerlendirilebilse de, bir uygulamayı yapılandırmadaki önemli rolleri ve teknoloji yığınları (technology stacks) ile daha doğrudan bağlantılı olmaları nedeniyle, onları ayrı ele almayı tercih ediyoruz. Ayrıca, bir referans mimari genellikle başka desenleri de içerir ve sık sık bu desenleri kısıtlar. Örneğin, Şekil 2.3’te gösterilen web uygulamaları için referans mimari, Katmanlar desenini içerir, ancak aynı zamanda kaç katmanın kullanılması gerektiğini de belirler. Bu referans mimarisi ayrıca Uygulama Cephe (Application Facade) ve Veri Erişim Bileşenleri (Data Access Components) gibi diğer desenleri de içerir.

## 2.5.3 Dağıtım Desenleri (Deployment Patterns)

Ayrı olarak ele almayı tercih ettiğimiz bir diğer desen türü dağıtım desenleridir (deployment patterns). Bu desenler, sistemi fiziksel olarak nasıl yapılandırıp dağıtacağımıza (deploy) dair modeller sağlar. Şekil 2.6’da gösterilen desen gibi bazı dağıtım desenleri, sistemi katmanlar (tiers; fiziksel düğümler) açısından ele alarak ilk fiziksel yapıyı kurmak için yararlıdır. Şekil 2.7’deki Yük Dengelemeli Küme (Load-Balanced Cluster) gibi daha uzmanlaşmış dağıtım desenleri ise, erişilebilirlik (availability), performans ve güvenlik gibi kalite niteliklerini sağlamak için kullanılır.

Genel olarak, sistem için ilk yapı, referans mimarilerden (ve diğer desenlerden) elde edilen mantıksal öğelerin, dağıtım desenleri tarafından tanımlanan fiziksel öğelerle eşleştirilmesiyle elde edilir.

## 2.5.4 Taktikler (Tactics)

Mimarlar, belirli kalite nitelikleri için istenen bir tepkiye (response) ulaşmak amacıyla temel tasarım teknikleri kümelerini kullanabilirler. Bu mimari tasarım asal öğelerine (primitives) taktikler (tactics) diyoruz. Taktikler, tıpkı tasarım desenleri gibi, mimarların yıllardır kullandığı tekniklerdir. Biz taktikleri icat etmiyoruz; yalnızca mimarların onlarca yıldır kalite niteliği tepki hedeflerini yönetmek için pratikte gerçekte ne yaptığını yakalıyoruz.

```
Olaylar
gelir

        Performansı
        denetlemek için
        taktikler

Yanıt,
zaman
kısıtları
içinde
üretilir
```

Şekil 2.8 Taktikler olaylar ile yanıtlar arasında arabuluculuk yapar.
