## Önsöz

Bu kitapta, kuram ile uygulama arasındaki boşluğu kapatmaya çalıştığımız, gözden geçirilmiş bir nitelik temelli tasarım (Attribute-Driven Design, ADD) sürümü sunuyoruz. Uzun yıllardır yazılım mimarisi ve yazılım tasarımı öğretiyoruz. Bu süreçte, hiç deneyimi olmayan kişilerin tasarım yapmalarının ne kadar zor olduğunu fark ettik. Bu farkındalık, insanlara tasarım sürecini uygulamada yol gösterecek bir tasarım yol haritası oluşturma motivasyonumuzu artırdı. Yazılım tasarımını öğretmede faydalı olan bir oyun da tasarladık; bu oyun, bu kitaba eşlik eden bir kaynak olarak değerlendirilebilir.

Bu kitabın hedef kitlesi, yazılım mimarilerinin tasarımıyla ilgilenen herkes. Özellikle bu görevi yerine getirmek zorunda olup da şu anda bunu gelişigüzel (ad hoc) yapan uygulayıcılar için yararlı olacağına inanıyoruz. Hâlihazırda yerleşik bir yöntemi izleyerek tasarım yapan deneyimli uygulayıcılar da yeni fikirler bulacaklar—örneğin, tasarım ilerlemesini bir Kanban panosu kullanarak takip etme, bir tasarımı taktik temelli (tactics-based) soru listeleriyle analiz etme ve erken tahmin (estimation) için bir tasarım yöntemini devreye alma gibi. Son olarak, Yazılım Mühendisliği Enstitüsü (Software Engineering Institute) tarafından geliştirilen diğer mimari yöntemlere zaten aşina olanlar, ADD’nin Kalite Nitelikleri Çalıştayı (Quality Attribute Workshop, QAW), Mimari Taviz Analizi Yöntemi (Architecture Tradeoff Analysis Method, ATAM) ve Maliyet Fayda Analizi Yöntemi (Cost Benefit Analysis Method, CBAM) gibi yöntemlerle nasıl ilişkilendirileceğine dair bilgiler bulacaklar. Bu kitap, bilgisayar bilimi veya yazılım mühendisliği programlarındaki öğrenci ve öğretmenler için de faydalı olacaktır. Burada yer verdiğimiz örnek olay çalışmalarının, tasarım sürecinin nasıl yürütüleceğini daha kolay anlamalarına yardımcı olacağına inanıyoruz. Nitekim, derslerimizde benzer örnekleri büyük bir başarıyla kullanıyoruz. Albert Einstein’ın dediği gibi: “Örnek, öğretmenin bir başka yolu değildir; tek yoludur.”

Dileğimiz, bu kitabın size tasarımın bir yöntem izlenerek yapılabileceğini anlamanızda yardımcı olması ve bu farkındalığın gelecekte daha iyi yazılım sistemleri üretmenizi sağlamasıdır.

Kitap aşağıdaki şekilde yapılandırılmıştır.

- Bölüm 1’de yazılım mimarisini ve nitelik temelli tasarım (Attribute-Driven Design, ADD) yöntemini kısaca tanıtıyoruz.
- Bölüm 2’de mimari tasarımı, tasarım sürecinin ana girdileriyle—bizim “mimari sürücüler (architectural drivers)” dediğimiz unsurlarla—birlikte daha ayrıntılı olarak tartışıyor ve bu sürücüleri kanıtlanmış çözümlerle karşılamanıza yardımcı olacak tasarım kavramlarını ele alıyoruz.
- Bölüm 3’te ADD yöntemini ayrıntılı olarak sunuyoruz. Yöntemin her bir adımını ve bu adımların uygun şekilde uygulanması için kullanılabilecek çeşitli teknikleri tartışıyoruz.
- Bölüm 4, bir greenfield sistemin geliştirilmesini gösteren ilk örnek olay çalışmamızdır. Bu örnek olayda, Bölüm 3’te açıklanan kavramların çoğunun tasarım sürecinde nasıl kullanıldığını göstermek için özel çaba sarf ettik; bu nedenle bu örnek olayı, doğası gereği daha “akademik” olarak düşünebilirsiniz (her ne kadar gerçek bir sistemden türetilmiş olsa da).
- Bölüm 5, uygulamada çalışan yazılım mimarlarıyla birlikte yazılmış olan ikinci örnek olay çalışmasını sunar ve bu nedenle çok daha teknik ve ayrıntılıdır. Bu bölüm, pek çok farklı teknolojiyi içeren bir Büyük Veri (Big Data) sisteminin tasarımında ADD’nin nasıl kullanıldığına dair tüm ince ayrıntıları gösterecektir. Bu örnek, Bölüm 4’te kullanılan daha geleneksel alana (domain) karşılık, bizim “yeni” (novel) bir alan olarak gördüğümüz bir alanda sistem geliştirilmesini göstermektedir.
- Bölüm 6, yaygın bir durum olan, bir miras (legacy, “brownfield”) sisteminin bir uzantısının tasarımında ADD’nin kullanımını gösteren daha kısa bir örnek olay çalışmasıdır. Bu örnek, mimari tasarımın yalnızca sistemin ilk sürümü geliştirilirken bir defaya mahsus yapılan bir şey olmadığını, aksine geliştirme sürecinin farklı anlarında gerçekleştirilebilecek bir etkinlik olduğunu göstermektedir.
- Bölüm 7, diğer tasarım yöntemlerini tanıtır. ADD’nin gözden geçirilmiş sürümünde, tasarım sürecini incelemiş diğer yazarların fikirlerini benimsedik ve burada hem onların çalışmalarına saygı duruşu niteliğinde hem de ADD’yi bu yöntemlerle karşılaştırmanın bir aracı olarak yaklaşımlarını kısaca özetliyoruz.
- Bölüm 8, her ne kadar bu bir tasarım kitabı olsa da, analizi ayrıntılı biçimde ele alır. Analiz, doğal olarak tasarımın bir parçası olarak gerçekleştirilir; bu nedenle burada hem tasarım süreci sırasında hem de tasarımın bir bölümü tamamlandıktan sonra kullanılabilecek teknikleri açıklıyoruz. Özellikle, tasarım sürecinde alınan kararları zaman açısından verimli ve basit bir şekilde anlamaya yardımcı olan taktik temelli soru listelerinin kullanımını tanıtıyoruz.
- Bölüm 9, tasarım sürecinin örgütsel düzeyde nasıl konumlandığını açıklar. Örneğin, projenin yaşamının en erken anlarında belli bir miktar mimari tasarım yapılması, tahmin (estimation) amaçları için faydalıdır. Ayrıca ADD’nin farklı yazılım geliştirme yaklaşımlarıyla nasıl ilişkilendirilebileceğini gösteriyoruz.
- Bölüm 10 kitabı sonlandırır.

Ayrıca iki ek (appendix) de içeriyoruz. Ek A, adından da anlaşılacağı üzere, belirli bir uygulama alanı (application domain) için tasarım yapmakta kullanılabilecek farklı türde tasarım kavramlarından oluşan bir Tasarım Kavramları Kataloğu’nu (A Design Concepts Catalog) sunar. Bu katalog, deneyimli ve disiplinli mimarların gerçek dünyada nasıl çalıştığını yansıtan, farklı kaynaklardan derlediğimiz tasarım kavramlarını içerir. Bizim durumumuzda kataloğumuz, Bölüm 4’te sunulan örnek olay çalışmasında kullanılan tasarım kavramlarının bir örneklemini barındırmaktadır. Ek B, en yaygın yedi kalite niteliği (quality attribute) için ve ayrıca DevOps için bir tane olmak üzere, Bölüm 8’de tanıtılan taktik temelli soru listelerinin bir setini sağlar.

Designing Software Architectures kitabının bir kopyasını informit.com’da kaydederek, mevcut oldukça indirmelere, güncellemelere ve düzeltmelere kolayca erişebilirsiniz. Kayıt sürecini başlatmak için informit.com/register adresine gidin ve oturum açın veya bir hesap oluşturun. Ürün ISBN’sini (9780134390789) girin ve Submit’e tıklayın. Süreç tamamlandığında, varsa ek içerikleri “Registered Products” altında bulacaksınız.

Yazarlar, görüş ve yorumlarıyla cömert katkılarda bulunan hakemlerimiz Marty
Barrett, Roger Champagne, Siva Muthu, Robert Nord, Vishal Prabhu, Andriy
Shapochka, David Sisk, Perla Velasco-Elizondo ve Olaf Zimmermann’a teşekkür etmek ister. Ayrıca 5. Bölüm’e katkılarından dolayı Serge Haziyev ve Olha
Hrytsay’e de teşekkür ederiz. Bunlara ek olarak, aralarında Serge, Olha ve
Andriy’nin de bulunduğu Softserve’deki birçok mimara, çalışmalarımıza verdikleri güçlü ve sürekli destek için teşekkür borçluyuz.

Humberto, Quarksoft’taki direktörlere ve mimar grubuna teşekkür etmek
ister; ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) revizyonuna dair birçok fikir ve bu kitapta sunulan örnek olay çalışmalarından biri, bu yöntemi söz konusu şirket bünyesinde uygulamaya koymaktan doğmuştur. Birlikte
çalışma ve fikir alışverişinde bulunma fırsatı yakaladığım diğer şirketlerdeki
mimar ve geliştiricilere de teşekkür ederim; onlardan çok şey öğrendim. Ayrıca,
yıllardır ACE Educators Workshop’ta beni ve diğer akademisyenleri ağırlayan
Software Engineering Institute’teki insanlara teşekkür etmek isterim. Üniversitem
Universidad Autónoma Metropolitana Iztapalapa’ya da, çalışmalarımı her zaman
desteklediği için teşekkür etmek istiyorum. Bu mimari yolculukta yıllardır bana
eşlik eden meslektaşlarım Perla Velasco-Elizondo ve Luis Castro’ya da teşekkürler. Yıllar önce bana uygulayıcı bir mimar olma fırsatını veren Alonso Leal’a
teşekkür ederim. Bu kitabı yazarken paha biçilmez olduğu kanıtlanan birçok
beceriyi bana öğreten Richard S. Hall’a teşekkür ederim. Son olarak, birlikte
çalışmanın ve fikir alışverişinde bulunmanın her zaman bir zevk olduğu, çok iyi
bir insan ve meslektaş olan eş yazarım Rick’e teşekkür etmek isterim.

Rick, Software Engineering Institute’ten James Ivers’a ve onun araştırma
grubuna teşekkür etmek ister. Özellikle, özenli ve ufuk açıcı inceleme yorumları
ve önerileri için Rod Nord’a teşekkür etmek isterim. Ayrıca, yıllardır birlikte
çalıştığım işbirlikçim ve akıl hocam Len Bass’e teşekkür etmek isterim; yazılım
mimarisi yolculuğuna yıllar önce beni başlatan kişidir. Len olmasaydı, bugün
nerede olacağımı kim bilebilir. Buna ek olarak, araştırmalarımı yıllarca kararlılıkla destekleyen ve bana pek çok harika “başarılı olma fırsatı” sunan Linda
Northrop’a teşekkür etmek isterim. Son olarak, her zaman enerjik, olumlu ve
birlikte çalışması gerçek bir zevk olan eş yazarım Humberto’ya teşekkür etmek
isterim.

xvii

Bu sayfa bilerek boş bırakılmıştır.

# 1. Giriş

Bu bölümde yazılım mimarisi konusuna bir giriş sunuyoruz. Kısaca mimarinin ne
olduğunu ve neden yazılım sistemleri geliştirilirken mutlaka dikkate alınması
gereken temel bir unsur olduğunu tartışıyoruz. Ayrıca, yazılım mimarisinin geliştirilmesiyle ilişkili farklı etkinlikleri ele alıyoruz; böylece bu kitabın ana konusu olan mimari tasarım, bu etkinliklerin bağlamında anlaşılabilir. Yine kısaca,
tasarımı oluşturmaktan sorumlu kişi olan mimarın rolünü tartışıyoruz. Son olarak, bu kitapta kapsamlı biçimde ele alacağımız mimari tasarım yöntemi olan
nitelik temelli tasarım (Attribute-Driven Design, ADD) yöntemini tanıtıyoruz.

## 1.1 Güdüler

Bu kitaptaki amacımız, sana yazılım mimarisini sistematik, öngörülebilir, tekrarlanabilir ve maliyet etkin bir biçimde nasıl tasarlayacağını öğretmektir. Eğer
bu kitabı okuyorsan, büyük olasılıkla zaten mimariye ilgi duyuyorsun ve mimar
olmayı hedefliyorsun. İyi haber şu ki bu hedef ulaşabileceğin bir noktada. Seni
bu noktada ikna etmek için, tasarım fikrinden—herhangi bir şeyin tasarımından—
kısaca söz edeceğiz ve mimari tasarımın nasıl ve neden bundan çok da farklı
olmadığını göreceğiz. Çoğu alanda “tasarım”, benzer türden zorlukları ve hususları içerir—paydaş (stakeholder) ihtiyaçlarını karşılama, bütçelere ve takvimlere uyma, kısıtlarla başa çıkma vb. Tasarımın ilkel öğeleri (primitive) ve araçları
alandan alana değişse de, tasarımın hedefleri ve adımları değişmez.

> **💬 Çevirmen notu:** Burada “design primitives” ile kastedilen, bir tasarımın
> üzerinde inşa edildiği temel yapıtaşlarıdır; yazılımda bileşen, konnektör, arayüz
> gibi kavramlar bu tür “ilkel öğe” örnekleridir.

Bu cesaret verici bir bilgidir; çünkü tasarımın yalnızca “büyücülerin”
tekelinde olmadığını gösterir. Yani, tasarım öğretilebilir ve öğrenilebilir. Özellikle mühendislikteki tasarımın çoğu, bilinen tasarım ilkel öğelerini, öngörülebilir
sonuçlar elde edecek (kimi zaman yenilikçi) biçimlerde bir araya getirmekten
ibarettir. Elbette ayrıntılar zordur; ancak bu nedenle yöntemlerimiz vardır. Tasarım gibi yaratıcı bir uğraşın adım adım bir yöntemle yakalanabileceğini hayal
etmek ilk başta zor görünebilir; yine de Parnas ve Clements’in “A Rational Design Process: How and Why to Fake It” başlıklı makalelerinde tartıştıkları gibi
bu yalnızca mümkün değil, aynı zamanda değerlidir. Elbette herkes iyi bir tasarımcı olamaz; tıpkı herkesin bir Thomas Edison ya da LeBron James ya da
Ronaldo olamayacağı gibi. İddiamız, herkesin çok daha iyi bir tasarımcı olabileceğidir; bu kitapta sunduğumuz, yeniden kullanılabilir tasarım bilgisi parçacıklarıyla desteklenen yapılandırılmış yöntemlerin, vasatlıktan mükemmelliğe giden
yolu döşemeye yardımcı olabileceğidir.

Neden yazılım mimarisi tasarımı hakkında bir kitap yazıyoruz? Tasarım
üzerine genel olarak çok şey yazılmış olmasına ve yazılım mimarisi tasarımı
üzerine de bazı yazılar bulunmasına karşın, yalnızca mimari tasarıma adanmış
bir kitap yoktur. Dahası, mimari tasarım hakkında yazılanların çoğu görece soyut kalmaktadır.

Bu kitabı yazmaktaki amacımız, herhangi yetkin bir yazılım mühendisi tarafından uygulanabilecek pratik bir yöntem sunmak ve ayrıca (ve en az bunun
kadar önemli olarak) bu yöntemi somutlaştıran zengin örnek olay çalışmaları
(topluluğu) sağlamaktı. Albert Einstein’ın “Örnek, öğretmenin bir başka yolu
değil, tek yoludur” dediği rivayet edilir. Buna yürekten inanıyoruz. Çoğumuz,
kurallar, adımlar ya da ilkeler kümelerinden çok örneklerden öğreniriz. Elbette,
yaptıklarımızı yapılandırmak ve örnekleri oluşturmak için adımlara, kurallara
ve ilkelere ihtiyaç duyarız; ancak örnekler, günlük kaygılarımıza hitap eder ve
adımları somutlaştırarak bize yardımcı olur.

Bu, mimari tasarımın hiçbir zaman basit olacağı anlamına gelmez. Eğer
karmaşık bir sistem inşa ediyorsan, büyük olasılıkla pazara çıkma süresi, maliyet, performans, evrilebilirlik (evolvability), kullanılabilirlik (usability), erişilebilirlik/süreklilik (availability) gibi pek çok birbirleriyle rekabet eden gücü dengelemeye çalışıyorsun. Bu boyutlardan herhangi birinde sınırları zorluyorsan, mimar
olarak işin daha da karmaşık olacaktır. Bu durum yalnızca yazılımda değil, herhangi bir mühendislik disiplininde böyledir. Büyük gemiler, gökdelenler ya da
diğer karmaşık “sistemlerin” tarihine bakarsan, bu sistemlerin mimarlarının da
uygun kararlar ve ödünleşimler (tradeoff) yapmak için nasıl mücadele ettiklerini görürsün. Evet, mimari tasarım belki hiçbir zaman kolay olmayacak; ancak
amacımız, iyi yetişmiş, iyi eğitimli yazılım mühendislerinin üstesinden gelebileceği, yönetilebilir (tractable) ve başarılabilir bir uğraş haline getirmektir.

## 1.2 Yazılım Mimarisi

Yazılım mimarisinin ne olduğu üzerine çok şey yazılmıştır. Biz, *Software Architecture in Practice* (üçüncü baskı) kitabındaki yazılım mimarisi tanımını benimsiyoruz:

> Bir sistemin yazılım mimarisi, sistem hakkında akıl yürütebilmek için gerekli olan, yazılım ögelerinden, aralarındaki ilişkilerden ve her ikisinin özelliklerinden oluşan yapıların (structures) kümesidir.

İlerleyen bölümlerde göreceğiniz gibi, tasarım yöntemimiz bu tanımı somutlaştırır ve tasarımcının istenen özelliklere sahip bir mimari oluşturmasına yardımcı olur.

### 1.2.1 Yazılım Mimarisi’nin Önemi

Yazılım mimarisinin neden önemli olduğu konusunda da çok şey yazılmıştır. Yine *Software Architecture in Practice*’i izleyerek, mimarinin çok çeşitli nedenlerle önemli olduğunu ve bu nedenlerden benzer biçimde çok çeşitli sonuçların doğduğunu not ediyoruz:

- Bir mimari, bir sistemin yönlendirici kalite niteliklerini (driving quality attributes) engelleyecek veya mümkün kılacak niteliktedir.
- Bir mimaride verilen kararlar, sistem evrimleştikçe değişimi yönetmenize ve değişim hakkında akıl yürütmenize olanak tanır.
- Bir mimarinin analizi, sistem niteliklerinin (qualities) erken safhada öngörülmesini mümkün kılar.
- Belgelenmiş bir mimari, paydaşlar (stakeholders) arasındaki iletişimi güçlendirir.
- Mimari, en erken ve dolayısıyla en temel, değiştirilmesi en zor tasarım kararlarının taşıyıcısıdır.
- Bir mimari, daha sonraki gerçekleştirim (implementation) üzerinde bir dizi kısıt tanımlar.
- Mimari, bir organizasyonun yapısını etkiler ve bunun tersi de geçerlidir.
- Bir mimari, evrimsel hatta atılabilir (throwaway) prototipleme için temel sağlayabilir.
- Mimari, mimarın ve proje yöneticisinin maliyet ve takvim (schedule) hakkında akıl yürütebilmesini sağlayan kilit eserdir (artifact).
- Mimari, bir ürün hattının (product line) kalbini oluşturacak, aktarılabilir ve yeniden kullanılabilir bir model olarak oluşturulabilir.
- Mimari temelli geliştirme (architecture-based development), dikkati yalnızca bileşenlerin yaratılmasına değil, bileşenlerin bir araya getirilmesine (assembly) odaklar.
- Tasarım alternatiflerini sınırlayarak mimari, geliştiricilerin yaratıcılığını belirli bir yöne kanalize eder; tasarım ve sistem karmaşıklığını azaltır.
- Mimari, yeni bir ekip üyesini eğitmek için temel olabilir.

Mimari bütün bu nedenlerle önemliyse — organizasyonun yapısını, sistemin niteliklerini ve sistemin oluşturulması ve evriminde yer alan insanları etkiliyorsa — o halde bu kritik eseri tasarlarken büyük bir özen gösterilmesi gerektiği açıktır.

Ne yazık ki, çoğu zaman durum böyle değildir. Mimari çoğunlukla “evrilir” veya “ortaya çıkar” (“evolve” / “emerge”). Evrime veya ortaya çıkmaya karşı değiliz; “en baştan ayrıntılı büyük tasarım” (big design up front) yaklaşımını savunduğumuz da kesinlikle söylenemez. Ancak, herhangi bir mimari yapmamak, en basit projeler dışında genellikle fazla risklidir. Özenle tasarlanmamış bir köprüden geçmek ya da uçağa binmek ister miydiniz? Elbette istemezdiniz. Oysa her gün hatalı (buggy), pahalı, güvensiz, güvenilir olmayan, arıza yapmaya yatkın ve yavaş yazılımlar kullanıyorsunuz — ve bu istenmeyen özelliklerin çoğundan kaçınmak mümkündür!

Bu kitabın öz mesajı şudur: Mimari tasarımı zor veya korkutucu olmak zorunda değildir; yalnızca “büyücülerin” tekelinde değildir; maliyetli olmak ve tamamen başta yapılmak zorunda da değildir. Bizim görevimiz, bunun nasıl yapılacağını size göstermek ve bunun sizin ulaşabileceğiniz bir şey olduğuna sizi ikna etmektir.

### 1.2.2 Yaşam Döngüsü Etkinlikleri

Yazılım mimarisi tasarımı, yazılım mimarisi yaşam döngüsü etkinliklerinden (software architecture life-cycle activities) biridir (Şekil 1.1). Herhangi bir yazılım proje yaşam döngüsünde olduğu gibi, bu etkinlik de gereksinimlerin bir tasarıma, tasarımın da bir gerçekleştirim (implementation) haline dönüştürülmesiyle ilgilidir. Özellikle mimarın şu konularla ilgilenmesi gerekir:

![Şekil 1.1](/home/runner/workspace/scripts/dsa_figs/sekil_1_1.png){width=12.28cm}


- **Mimari gereksinimler (architectural requirements).** Tüm gereksinimler arasında, yazılım mimarisi açısından özel bir öneme sahip olan birkaçı vardır. Bu mimari açıdan önemli gereksinimler (architecturally significant requirements, ASRs) yalnızca sistemin en önemli işlevselliğini (functionality) ve dikkate alınması gereken kısıtları (constraints) değil, aynı zamanda — ve en önemlisi — yüksek performans, yüksek erişilebilirlik (availability), kolay evrimleşebilirlik ve sarsılmaz (iron-clad) güvenlik gibi kalite niteliklerini (quality attributes) de içerir. Bu gereksinimler, açık bir tasarım amacı ve dış paydaşlar (external stakeholders) için görünmez veya hiç yazıya dökülmemiş olabilecek diğer mimari kaygılarla birlikte, sizi bir mimari yapı ve bileşen kümesini diğerine tercih etmeye yönlendirecektir. Bu ASR’lere ve kaygılara “sürücüler (drivers)” diyeceğiz; çünkü tasarımı “sürdürdükleri”, yani yönlendirdikleri söylenebilir.
- **Mimari tasarım (architectural design).** Tasarım, ihtiyaçlar dünyasından (gereksinimler) kod, çerçeveler (frameworks) ve bileşenlerden oluşan yapılar biçiminde çözümler dünyasına yapılan bir çeviridir. İyi bir tasarım, sürücüleri karşılayan tasarımdır. Mimari tasarım, bu kitabın odak noktasıdır.

> **💬 Çevirmen notu:** Buradaki “sürücü (driver)” kavramı özellikle “mimari sürücü (architectural driver)” bağlamında, mimariyi en çok şekillendiren gereksinim ve kaygıları ifade eder; ilerleyen bölümlerde ayrıntılandırılacaktır.

---

Yazılım Mimarisi  
Yaşam Döngüsü Etkinlikleri

- Mimari Gereksinimler  
  `<<precedes>>`

**Kitabın odak noktası**

- Mimari Tasarım  
  `<<precedes>>`  
  `<<precedes>>`

- Mimari Belgeleme (Architectural Documentation)  
  `<<precedes>>`

- Mimari Değerlendirme (Architectural Evaluation)  

  `<<precedes>>`  

  `<<influences>>`

- Mimari Gerçekleştirim (Architectural Implementation)

**ŞEKİL 1.1** Yazılım mimarisi yaşam döngüsü etkinlikleri

---

- **Mimari belgeleme (architectural documentation).** Yapıların belli bir düzeyde ön belgelemesi (veya eskizler) mimari tasarımın bir parçası olarak oluşturulmalıdır. Ancak bu etkinlik, bu eskizlerden daha resmî bir belgenin üretilmesini ifade eder. Proje küçük ve daha önce benzeri yapılmışsa mimari belgeleme asgari düzeyde kalabilir. Buna karşılık proje büyükse, dağıtık ekipler birlikte çalışıyorsa ya da ciddi teknik zorluklar söz konusuysa, mimari belgeleme bu etkinliğe harcanan çabanın karşılığını fazlasıyla verecektir. Belgeleme genellikle programcılar tarafından kaçınılan ve küçümsenen bir faaliyet olsa da, diğer hemen tüm mühendislik disiplinlerinde standart ve pazarlığa açık olmayan bir çıktıdır. Sisteminiz yeterince büyükse ve görev açısından kritikse (mission critical), belgelenmelidir. Diğer mühendislik disiplinlerinde “plan” (blueprint) — bir tür belgelenmiş tasarım — gerçekleştirim aşamasına ve kaynakların tahsisine geçerken kesinlikle vazgeçilmez bir adımdır.

§ Mimari değerlendirme (architectural evaluation). Belgede olduğu gibi, projeniz önemsiz bir şey değilse, kendinize ve paydaşlarınıza (stakeholder) mimariyi değerlendirmeniz borcunuzdur; yani alınan kararların kritik gereksinimleri karşılamak için uygun olduğundan emin olmanız gerekir. Test etmeden kod teslim eder miydiniz? Elbette hayır. Benzer şekilde, tasarımı önce “test” etmeden mimariyi ayrıntılandırmak için neden muazzam kaynaklar harcayasınız? Bunu sistemi ilk kez oluştururken veya büyük bir yeniden yapılandırmadan (refactoring) geçirirken yapmak isteyebilirsiniz. Tipik olarak değerlendirme gayriresmî ve kurum içi yapılır, ancak gerçekten önemli projeler için, dış bir ekip tarafından resmî bir değerlendirme yapılması tavsiye edilir.

§ Mimari gerçekleştirim/uygunluk denetimi (architectural implementation/conformance checking). Son olarak, oluşturduğunuz (ve değerlendirdiğiniz) mimariyi gerçekleştirmelisiniz. Bir mimar olarak, sistem büyüdükçe ve gereksinimler evrildikçe tasarımı biraz ayarlamanız gerekebilir. Bu normaldir. Bu ince ayarların yanında, gerçekleştirim sırasında temel sorumluluğunuz, kodun tasarıma uygunluğunu (conformance) sağlamaktır. Geliştiriciler mimariyi sadakatle gerçekleştirmiyorlarsa, siz tasarlamış olduğunuz nitelikleri (qualities) baltalıyor olabilirler. Yine, diğer mühendislik alanlarında yapılanları düşünün. Yeni bir bina için beton temel döküldüğünde, bu temel üzerine oturacak bina, temel önce bir karot numunesi ile test edilmeden —yeterince güçlü, yeterince yoğun, suya ve gazlara karşı yeterince geçirimsiz vb. olup olmadığı kontrol edilmeden— inşa edilmez. Uygunluk denetimi olmaksızın, sonradan inşa edilen şeyin kalitesini güvence altına almanın bir yolu yoktur.

Şekil 1.1’de belirli bir yaşam döngüsü (life-cycle) yöntemini önermediğimizi unutmayın. <<precedes>> kalıp yargısı (stereotype) sadece, bir etkinlikte belirli bir çabanın harcanması gerektiği ve dolayısıyla daha sonraki bir etkinlikteki çabadan önce gelmesi gerektiği anlamına gelir. Örneğin, gereksinimler hakkında hiçbir fikriniz yoksa tasarım etkinliklerini gerçekleştiremezsiniz ve bazı tasarım kararları almadan da bir mimariyi değerlendiremezsiniz.

Bugün ticari yazılımların çoğu bir tür çevik (Agile) yöntem kullanılarak geliştirilir. Bu mimari etkinliklerin hiçbiri çevik uygulamalarla uyumsuz değildir. Bir yazılım mimarı için soru “Çevik mi yapmalıyım yoksa mimari mi?” değil, “Projeye başlamadan önce ne kadar mimari iş yapmalıyım, gereksinimler biraz netleşene kadar ne kadarını ertelemeliyim?” ve “Mimariyi ne kadarını, ne zaman resmî olarak belgelendirmeliyim?” sorularıdır. Çevik (Agile) ve mimari, pek çok yazılım projesi için gayet uyumlu yol arkadaşlarıdır.

Mimari tasarım ile çeşitli yazılım yaşam döngüsü yöntemleri ve süreç modelleri —yinelemeli (iterative) geliştirme dâhil— arasındaki ilişkiyi Bölüm 9’da tartışacağız.

## 1.3 Mimarın Rolü

Bir mimar “sadece” bir tasarımcıdan çok daha fazlasıdır. Bir veya daha fazla kişi tarafından üstlenilebilen bu rolün, başarılı olabilmesi için yerine getirilmesi gereken uzun bir görev, beceri ve bilgi listesi vardır. Bu önkoşullar şunları içerir:

- Liderlik: mentorluk, ekip oluşturma, vizyon belirleme, koçluk
- İletişim: hem teknik hem teknik olmayan, işbirliğini teşvik etme
- Müzakere: iç ve dış paydaşlarla ve onların çelişen ihtiyaç ve beklentileriyle başa çıkma
- Teknik beceriler: yaşam döngüsü (life-cycle) becerileri, teknolojilerde uzmanlık, sürekli öğrenme, kod yazma
- Proje becerileri: bütçeleme, personel, zamanlama yönetimi, risk yönetimi
- Analitik beceriler: mimari analiz (architectural analysis), proje yönetimi ve ölçüm için genel bir analiz zihniyeti (bkz. “Analizin Anlamı” kenar yazısı)

Başarılı bir tasarım, “duvarın üzerinden atılan” durağan bir belge değildir. Yani mimarlar sadece iyi tasarlamakla kalmamalı, aynı zamanda projeyle ilgili her yönün —fikir aşaması ve iş gerekçesinden tasarım ve oluşturma, işletim, bakım ve en sonunda emekliliğe kadar— ayrılmaz bir parçası olmalıdır.

### Analizin Anlamı

Merriam-Webster Sözlüğü’nde analysis kelimesi şu şekilde tanımlanır:

- Bir şeyin parçalarını, bunların ne yaptığını ve birbirleriyle nasıl ilişkili olduklarını öğrenmek için dikkatli biçimde incelenmesi
- Bir şeyin doğası ve anlamına dair bir açıklama

Bu kitapta analysis kelimesini farklı amaçlarla kullanıyoruz ve her iki tanım da geçerlidir. Örneğin, mimari değerlendirme (architectural evaluation) etkinliğinin bir parçası olarak, mevcut bir mimari, ilişkili sürücüleri (drivers) karşılamaya uygun olup olmadığını anlamak için analiz edilir. Tasarım süreci sırasında, girdiler tasarım kararları vermek için analiz edilir. Prototiplerin oluşturulması da bir analiz biçimidir. Aslında analiz, tasarım süreci için o kadar önemlidir ki, bu konuya yalnızca Bölüm 8’i ayırıyoruz. Orada ayrıca analiz ile değerlendirme arasındaki ilişkiyi daha ayrıntılı biçimde tartışıyoruz. Bu kitapta öncelikli odak noktamız, tasarım etkinliği, ona bağlı teknik beceriler ve bunların geliştirme yaşam döngüsüne entegrasyonudur. Bir mimarın hayatının diğer yönlerine daha kapsamlı bir yaklaşım için, Software Architecture in Practice veya Just Enough Software Architecture gibi daha genel bir yazılım mimarisi kitabını okumanızı öneririz.

> **💬 Çevirmen notu:** Burada “analysis” hem tasarım girdilerinin sistematik incelenmesi hem de mevcut mimarinin ölçülüp değerlendirilmesi anlamında, geniş bir şemsiye kavram olarak kullanılıyor.

## 1.4 ADD’nin Kısa Tarihçesi (A Brief History of ADD)

Mimarın pek çok görevi ve sorumluluğu olmakla birlikte, bu kitapta odağımızı, bir yazılım mühendisinin “mimar” olarak adlandırılabilmesi için ustalaşması gereken ve tartışmalı da olsa tek en önemli beceriye yöneltiyoruz: tasarım süreci. Mimari tasarımı daha yönetilebilir ve yinelenebilir kılmak için, bu kitapta dikkatimizi büyük ölçüde Nitelik Temelli Tasarım (Attribute-Driven Design, ADD) yöntemine odaklıyoruz; bu yöntem, Şekil 1.1’de gösterilen tasarım etkinliğinin yinelemeli olarak nasıl yürütüleceğine dair adım adım rehberlik sunar. Bölüm 3’te ADD’nin en güncel sürümü olan 3.0 ayrıntılı biçimde anlatılmaktadır; bu nedenle burada, ADD’nin önceki sürümlerine aşina olanlar için biraz arka plan bilgisi veriyoruz. ADD’nin ilk sürümü (ADD 1.0, ilk adıyla “Mimari Temelli Tasarım (Architecture-Based Design, ABD)”) Ocak 2000’de, ikinci sürümü (ADD 2.0) ise Kasım 2006’da yayımlandı. *Software Architecture in Practice* kitabının üçüncü baskısı, bu yöntemi daha az sayıda adımla sunar. Ancak bu tartışma, yeni bir ADD sürümü tanıtmaktan ziyade, yöntemin gerçek adımlarını özetleyen, yeniden paketlenmiş bir sürüm sunmaktadır.

Bildiğimiz kadarıyla ADD, en kapsamlı ve en yaygın kullanılan, belgelenmiş mimari tasarım yöntemidir. (Bölüm 7’de çok sayıda alternatif tasarım yöntemine genel bir bakış sunuyoruz.) ADD ortaya çıktığında, özellikle kalite niteliklerine (quality attributes) ve bunların mimari yapılar (architectural structures) oluşturularak ve görünümler (views) aracılığıyla temsil edilerek nasıl gerçekleştirileceğine odaklanan ilk tasarım yöntemiydi. ADD’nin bir diğer önemli katkısı, mimari çözümlemesini (architecture analysis) ve belgelendirmeyi (documentation) tasarım sürecinin ayrılmaz bir parçası olarak ele almasıdır. ADD’de tasarım etkinlikleri, erken tasarım yinelemelerinde oluşturulan eskizlerin daha ayrıntılı bir mimariye dönüştürülmesini ve tasarımın sürekli değerlendirilmesini içerir.

ADD 2.0, kalite niteliklerini tasarım seçimleriyle ilişkilendirmede yararlı olmakla birlikte, ele alınması gereken birkaç eksikliğe sahipti:

- ADD 2.0, mimara kalite niteliği senaryolarının (quality attribute scenarios) tatminini sağlamak için taktikleri (tactics) ve desenleri (patterns) kullanma ve birleştirme konusunda rehberlik sağlar. Ancak desenler ve taktikler soyutlamalardır ve yöntem bu soyutlamaların somut uygulama teknolojilerine nasıl eşleneceğini açıklamamıştır.
- ADD 2.0, Çevik (Agile) yöntemler geniş çapta benimsenmeden önce geliştirilmiştir ve bu nedenle Çevik bir bağlamda mimari tasarım için bir rehberlik sunmamıştır.
- ADD 2.0, tasarım sürecinin nasıl başlatılacağına dair bir rehberlik sağlamamıştır. Bu eksiklik genel uygulanabilirliğini artırırken, nereden başlayacağını bilmeyen acemi tasarımcılar için zorluklar yaratmıştır. Özellikle, ADD 2.0, ileride bu kitapta tartışacağımız üzere, pek çok mimar için ideal bir başlangıç noktası olan başvuru mimarilerinin (reference architectures) açıkça (yeniden) kullanılmasını teşvik etmemiştir.
- ADD 2.0, farklı tasarım amaçlarını açıkça dikkate almamıştır. Örneğin, tasarım, bir satış öncesi (pre-sales) sürecin parçası olarak ya da “standart” inşaata yönelik tasarımın parçası olarak yapılabilir. Bunlar çok farklı amaçlardır ve ADD’nin farklı şekillerde kullanılmasına yol açacaktır.
- ADD 2.0, tasarımın bazı mimari kaygıların (architectural concerns) (yani içsel gereksinimlerin) ele alınmasını gerektirdiğini, bunun “geleneksel” sürücüler (gereksinimler ve kısıtlar) listesinde ifade edilip edilmemesine bakılmaksızın dikkate almamıştır. Bir kullanıcının bir sistemin “test edilebilir” olmasını istemesi veya sistemin özel test arayüzleri sağlamasını talep etmesi nadirdir; ancak bilge bir mimar, özellikle sistem karmaşıksa ve kontrol edilmesi ve yeniden üretilmesi zor bağlamlarda kullanılıyorsa, böyle bir altyapıyı dahil etmeyi seçebilir.
- ADD 2.0 yinelemeleri, her zaman mimari öğelerin (architectural elements) seçimi ve ayrıştırılması (decomposition) tarafından yönlendirilir. Bunun nedeni, ADD 2.0’ın önce ayrıştırılacak bir öğenin seçilmesini, sonra da sürücülerin belirlenmesini öngörmesidir. ADD 3.0’da, bazen bir tasarım adımının, öğelerin seçimini ve ayrıştırılmasını yönlendiren kritik mimari gereksinimler tarafından yönlendirildiğini kabul ediyoruz.
- ADD 2.0, (başlangıç) belgelendirme ve çözümleme içerir, ancak bunlar tasarım sürecinin açık adımları değildir.

ADD 3.0 bu eksikliklerin tümünü ele almaktadır. Kuşkusuz, ADD 3.0 devrimci değil evrimsel bir sürümdür. ADD 3.0’ın ortaya çıkışı, ADD’yi gerçek dünyada, çok farklı bağlamlarda kullanma girişimlerine bir tepki olarak geliştirilen ADD 2.5’in oluşturulmasıyla tetiklenmiştir.

ADD 2.5’i 2013 yılında yayımladık. O çalışmada, JSF, Spring veya Hibernate gibi uygulama çatılarını (application frameworks) birinci sınıf tasarım kavramları olarak kullanmayı savunduk. Bu değişiklik, ADD 2.0’ın, pratikte kolayca uygulanamayacak kadar soyut olması şeklindeki eksikliğini gidermeyi amaçlamaktaydı. ADD, sürücülerle (drivers) başlar, bunları sistematik olarak tasarım kararlarına bağlar ve ardından bu kararları, haricî olarak geliştirilmiş bileşenler de dahil olmak üzere mevcut uygulama seçeneklerine (implementation options) bağlar. Çevik geliştirme için ADD 3.0, az sayıda tasarım kararının alındığı, ardından potansiyel olarak bir gerçekleştirim “sivrilmesi”nin (implementation spike) takip ettiği hızlı tasarım yinelemelerini teşvik eder. Buna ek olarak, ADD 3.0 başvuru mimarilerinin açıkça (yeniden) kullanımını teşvik eder ve geniş bir taktik, desen, çatı, başvuru mimarisi ve teknoloji seçkisini içeren bir “tasarım kavramları kataloğu” (design concepts catalog) ile birlikte sunulur (bkz. Ek A).

> **💬 Çevirmen notu:** “Implementation spike”, Çevik yöntemlerde belirli bir teknik/çözüm yaklaşımını hızlıca deneyip öğrenmek için yapılan kısa, hedefli uygulama denemesi anlamına gelir.

## 1.5 Özet

Güdülerimizi ve arka planımızı ele aldığımıza göre, artık bu kitabın özüne geçiyoruz. İzleyen birkaç bölümde, tasarımdan ve özel olarak mimari tasarımdan ne kastettiğimizi açıklıyor, ADD’yi tartışıyor ve ADD’nin gerçek dünyada nasıl kullanılabileceğini ayrıntılarıyla gösteren üç vaka çalışması sunuyoruz. Ayrıca çözümlemenin tasarım sürecindeki kritik rolünü tartışıyor ve çözümlemenin tasarım artifaktları (design artifacts) üzerinde nasıl gerçekleştirilebileceğine dair örnekler veriyoruz.

1. Bu, bizim kendi kodlama gösterimimizdir; 2.5 numarası başka yerlerde kullanılmamaktadır.

## 1.6 Ek Okuma

Fred Brooks tasarımın doğası üzerine, tasarımcı ve araştırmacı olarak 50 yıllık
deneyimini yansıtan bir dizi düşünceli deneme kaleme almıştır:
F. P. Brooks, Jr., *The Design of Design: Essays from a Computer Scientist*.
Addison-Wesley, 2010.

Tasarım ve diğer geliştirme etkinlikleri için belgelenmiş bir sürece sahip olmanın
yararlılığı, D. Parnas ve P. Clements, “A Rational Design Process: How and Why
to Fake It”, *IEEE Transactions on Software Engineering*, SE-12, 2, Şubat 1986
makalesinde tartışılmaktadır.

Burada kullanılan yazılım mimarisi tanımı, mimarinin önemine ilişkin argümanlar
ve mimarın rolüyle ilgili görüşlerin tümü şu kaynaktan alınmıştır:
L. Bass, P. Clements ve R. Kazman, *Software Architecture in Practice*, 3. baskı,
Addison-Wesley, 2012.

Mimari geliştirme yaşam döngüsündeki farklı etkinlikleri ele alan birkaç kitap
bulunmaktadır; bunlara G. Fairbanks, *Just Enough Software Architecture: A Risk
Driven Approach*, Marshall & Brainerd, 2010 ve 7. Bölüm’de tasarım yaklaşımları
tanımlanan diğer kitaplar dahildir.

ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) ilk sürümü için erken
bir referans, F. Bachmann, L. Bass, G. Chastek, P. Donohoe ve F. Peruzzi,
*The Architecture Based Design Method*, CMU/SEI-2000-TR-001 çalışmasında
bulunabilir. ADD’nin ikinci sürümü, R. Wojcik, F. Bachmann, L. Bass,
P. Clements, P. Merson, R. Nord ve W. Wood, *Attribute-Driven Design (ADD),
Version 2.0*, CMU/SEI-2006-TR-023 belgesinde tanımlanmıştır. Bu kitapta ADD 2.5
olarak adlandırdığımız ADD sürümü ise H. Cervantes, P. Velasco-Elizondo ve
R. Kazman, “A Principled Way of Using Frameworks in Architectural Design”,
*IEEE Software*, s. 46–53, Mart/Nisan 2013 makalesinde yayımlanmıştır.

# 2
Mimari Tasarım

Şimdi mimari tasarım sürecine dalıyoruz: ne olduğu, neden önemli olduğu,
nasıl çalıştığı (soyut bir düzeyde) ve hangi temel kavramlar ile etkinlikleri
içerdiği. Önce mimari sürücüleri (architectural driver) tartışacağız: Tasarım
kararlarını “yönlendiren” çeşitli etkenler; bunların bazıları gereksinimler olarak
belgelenmiştir, ancak çoğu değildir. Buna ek olarak, tasarım sürecinizin bir
parçası olarak seçeceğiniz, birleştireceğiniz, somutlayacağınız, analiz edeceğiniz
ve belgeleyeceğiniz ana yapı taşları olan tasarım kavramlarına genel bir bakış
sunuyoruz.

## 2.1
Genel Olarak Tasarım

Tasarım hem bir fiildir hem de bir isimdir. Tasarım bir süreçtir, bir etkinliktir,
dolayısıyla bir fiildir. Süreç, bir tasarımın — arzu edilen nihai durumun bir
betiminin — ortaya çıkmasıyla sonuçlanır. Böylece tasarım sürecinin çıktısı,
sonunda gerçekleştireceğiniz şey, yani ad (isim), yapıt (artifact) olur. Tasarlamak,
hedeflere ulaşmak ve gereksinimler ile kısıtları karşılamak için kararlar almak
anlamına gelir. Tasarım sürecinin çıktıları, doğrudan bu hedeflerin, gereksinimlerin
ve kısıtların bir yansımasıdır. Örneğin evler hakkında düşünün. Neden Çin’deki
geleneksel evler, İsviçre ya da Cezayir’dekilerden farklı görünür? Neden bir
“yurt” (göçebe çadırı) bir “yurt” gibi görünür de, bir igloo, dağ evi (chalet) veya
“longhouse”dan (uzun ev) farklıdır?

Bu tarz evlerin mimarileri, yüzyıllar boyunca, kendilerine özgü hedef, gereksinim
ve kısıt kümelerini yansıtacak biçimde evrimleşmiştir. Çin’deki evler; simetrik
iç avlular, havalandırmayı artırmak için gökyüzü boşlukları, güneş toplamak ve
soğuk kuzey rüzgârlarından korunmak için güneye bakan avlular vb. özelliklere
sahiptir. A-çatılı evlerin, zemine kadar inen dik eğimli çatıları vardır; bu da
en az boyama gereksinimi ve yoğun kar yüklerine karşı koruma sağlar (kar
kolayca yere kayar). İglolar buzdan inşa edilir; bu da buzun bolluğunu, diğer
yapı malzemelerinin göreli kıtlığını ve zaman kısıtını (küçük bir igloo bir saatte
inşa edilebilir) yansıtır.

Her durumda, tasarım süreci bir dizi çözüm yaklaşımının seçilmesini ve
uygulanmasını içerir. İglo tasarımları bile değişkenlik gösterebilir. Bazıları
küçük ve geçici seyahat barınağı olarak tasarlanmıştır. Diğerleri, birden fazla
yapının birbirine bağlandığı, tüm toplulukların bir araya gelmesi için tasarlanan
büyük yapılardır. Bazıları süssüz, basit kar kulübeleridir. Diğerleri kürklerle
kaplanmıştır; buzdan “pencereleri” ve hayvan derisinden yapılmış kapıları vardır.

Tasarım süreci, her durumda, tasarımcının karşısındaki çeşitli “kuvvetler”
arasında bir denge kurar. Bazı tasarımların uygulanması ciddi beceri gerektirir
(örneğin, kar bloklarını kendi kendini taşıyan bir kubbe oluşturacak şekilde
oymak ve istiflemek gibi). Diğerleri görece az beceri gerektirir — bir siper (lean-to),
neredeyse herkesin dallar ve kabuk kullanarak inşa edebileceği bir yapıdır. Ancak
bu yapıların sergilediği nitelikler de önemli ölçüde farklılık gösterebilir. Siperler
doğal koşullara karşı çok az koruma sağlar ve kolayca yıkılırken, bir igloo
Arktik fırtınalara dayanabilir ve çatısında duran bir kişinin ağırlığını taşıyabilir.

Tasarım “zor” mudur? Hem evet hem hayır. Yenilikçi tasarım zordur. Geleneksel
bir bisikletin nasıl tasarlanacağı oldukça açıktır; ancak Segway’in tasarımı yeni
bir çığır açmıştır. Neyse ki, tasarımların çoğu yenilikçi değildir; çünkü çoğu
zaman gereksinimlerimiz yenilikçi değildir. Çoğu insan, kendisini güvenilir şekilde
bir yerden başka bir yere götürecek bir bisiklet ister. Bu durum her alanda
geçerlidir. Örneğin evleri düşünün. Phoenix’te yaşayan çoğu insan, kolay ve
ekonomik bir biçimde serin tutulabilecek bir ev isterken, Edmonton’da yaşayan
çoğu insanın öncelikli kaygısı, sıcak tutulabilecek bir evdir. Buna karşılık,
Japonya ve Los Angeles’ta yaşayan insanlar, depremlere dayanabilecek binalar
hususunda kaygılıdır.

Mimar olarak sizin için iyi haber, bu hedeflere güvenilir biçimde ulaşmak
üzere yeniden kullanılabilecek ve birleştirilebilecek, kanıtlanmış pek çok tasarım
ve tasarım parçası (bina blokları) olmasıdır; biz bunlara tasarım kavramları
(design concept) diyoruz. Tasarımınız gerçekten yenilikçi ise — eğer bir sonraki
Sydney Opera Binası’nı tasarlıyorsanız — tasarım süreci muhtemelen “zor”
olacaktır. Örneğin Sydney Opera Binası, ilk bütçe tahmininin 14 katına mal
olmuş ve on yıl gecikmeli olarak teslim edilmiştir. Yazılım mimarilerinin tasarımı
için de durum böyledir.

## 2.2
Yazılım Mimarisi Tasarımı

Yazılım sistemleri için mimari tasarım, genel anlamda tasarımdan farklı değildir: Gereksinimleri ve kısıtları karşılamak için, mevcut beceriler ve malzemelerle kararlar vermeyi içerir. Mimari tasarımda, tasarım amacımızı, gereksinimleri, kısıtları ve mimari kaygıları — bizim mimari sürücüler (architectural drivers) dediğimiz unsurları — Şekil 2.1’de gösterildiği gibi yapılara dönüştürecek kararlar veririz. Bu yapılar daha sonra projeye yön vermek için kullanılır. Analiz ve inşa süreçlerini yönlendirir, yeni bir proje üyesini eğitmek için temel işlevi görür. Ayrıca maliyet ve zaman çizelgesi kestirimi, ekip oluşturma, risk analizi ve azaltımı ve elbette gerçekleştirim (implementation) için de yol gösterir.

![Şekil 2.1](/home/runner/workspace/scripts/dsa_figs/sekil_2_1.png){width=11.82cm}


Bu nedenle mimari tasarım, ürün ve proje hedeflerinize ulaşmak için kritik bir adımdır. Bu hedeflerin bazıları teknik (örneğin bir video oyununda veya e-ticaret web sitesinde düşük ve öngörülebilir gecikme süresine ulaşmak), bazıları ise teknik olmayan hedeflerdir (örneğin iş gücünü istihdamda tutmak, yeni bir pazara girmek, bir teslim tarihini yakalamak). Bir mimar olarak verdiğiniz kararların, bu hedeflere ulaşma üzerinde etkileri olacak ve bazı durumlarda bu hedefler birbiriyle çelişebilecektir. Belirli bir başvuru mimarisinin (reference architecture) seçimi (örneğin Zengin İstemci Uygulaması (Rich Client Application)) gecikme süresi hedeflerinize ulaşmak için iyi bir temel sağlayabilir ve iş gücünüzü istihdamda tutmanıza yardım edebilir; çünkü ekip zaten bu başvuru mimarisine ve onu destekleyen teknoloji yığına (technology stack) aşinadır. Ancak bu seçim, örneğin mobil oyunlar gibi yeni bir pazara girmenize yardımcı olmayabilir.

Genel olarak, tasarım yaparken, bir kalite niteliğini (quality attribute) gerçekleştirmek için bir yapıda yapılan değişiklikler, diğer kalite nitelikleri üzerinde olumsuz etkilere sahip olacaktır. Bu ödünleşimler (tradeoff’lar), her alan için her uygulayıcı mimarın yaşamının bir gerçeğidir. Bu kitapta verilen örneklerde ve vaka çalışmalarında bunu tekrar tekrar göreceğiz. Dolayısıyla mimarın görevi, optimal bir çözüm bulmak değil, tatmin edici bir çözüm bulmaktır (satisficing) — potansiyel olarak çok büyük bir tasarım alternatifleri ve kararlar uzayı içinde, kabul edilebilir bir çözüm bulunana kadar arama yapmaktır.

## 2.2.1 Mimari Tasarım

Grady Booch, “Tüm mimari tasarımdır, fakat her tasarım mimari değildir” demiştir. Bir kararı “mimari” yapan nedir? Bir karar, yerel olmayan sonuçlara sahipse ve bu sonuçlar bir mimari sürücüye ulaşılması açısından önemliyse mimaridir. Dolayısıyla hiçbir karar doğası gereği mimari veya mimari olmayan değildir. Tek bir eleman (element) içindeki arabellekleme (buffering) stratejisi seçimi, sistemin geri kalanını çok az etkiliyorsa, bu durumda o elemanın uygulayıcısı veya bakımını yapan kişi dışında kimseyi ilgilendirmeyen bir gerçekleştirim ayrıntısıdır. Buna karşılık, arabellekleme stratejisi, performans (eğer arabellekleme gecikme, işlem hacmi (throughput) veya titreme (jitter) hedeflerine ulaşmayı etkiliyorsa) veya kullanılabilirlik (availability) (eğer arabellekler yeterince büyük değilse ve bilgi kayboluyorsa) ya da değiştirilebilirlik (modifiability) (eğer farklı dağıtımlarda veya bağlamlarda arabellekleme stratejisini esnek biçimde değiştirmek istiyorsak) üzerinde büyük sonuçlara sahip olabilir. Arabellekleme stratejisinin seçimi, çoğu tasarım seçimi gibi, ne doğası gereği mimaridir ne de doğası gereği mimari değildir. Bunun yerine, bu ayrım bütünüyle mevcut ve öngörülen mimari sürücülere bağlıdır.

## 2.2.2 Eleman Etkileşimi Tasarımı (Element Interaction Design)

Mimari tasarım, genellikle sistemin yapısının bir parçası olan elemanların sadece bir alt kümesinin tanımlanmasıyla sonuçlanır. Bu beklenen bir durumdur; çünkü ilk mimari tasarım sırasında mimar, sistemin birincil işlevselliğine odaklanacaktır. Bir kullanım senaryosunu (use case) “birincil” yapan nedir? İş önemi, risk ve karmaşıklık değerlendirmelerinin birleşimi bu nitelendirmeye etki eder. Elbette kullanıcılarınız için her şey acil ve en yüksek önceliktedir. Daha gerçekçi olan ise, az sayıda kullanım senaryosunun en temel iş değeri sağlaması veya (yanlış yapılmaları durumunda) en büyük riski temsil etmesidir; bu nedenle bunlar birincil kabul edilir.

Her sistemde, birincil olanların ötesinde, karşılanması gereken çok daha fazla kullanım senaryosu vardır. Bu ikincil olmayan (nonprimary) kullanım senaryolarını ve bunların arayüzlerini (interface) destekleyen elemanlar, bizim eleman etkileşimi tasarımı (element interaction design) dediğimiz şeyin bir parçası olarak tanımlanır. Bu tasarım düzeyi genellikle mimari tasarımı izler. Ancak bu elemanların konumu ve ilişkileri, mimari tasarım sırasında alınan kararlarla kısıtlanır. Bu elemanlar, bir bireye veya bir ekibe atanmış iş birimleri (modüller) olabilir; bu nedenle bu tasarım düzeyi, sadece ikincil olmayan işlevselliğin nasıl tahsis edildiğini tanımlamak için değil, aynı zamanda planlama amaçları (örneğin ekip oluşturma ve iletişim, bütçeleme, dış kaynak kullanımı, sürüm planlama, birim ve tümleştirme test planlama) için de önemlidir.

Sistemin ölçeğine ve karmaşıklığına bağlı olarak, mimar eleman etkileşimi tasarımına doğrudan ya da denetleyici (audit eden) bir rol üstlenerek dahil olmalıdır. Bu katılım, elemanlar doğru şekilde tanımlanmadığında, konumlandırılmadığında ve bağlanmadığında sistemin önemli kalite niteliklerinin zedelenmemesini güvence altına alır. Ayrıca mimarın, genelleştirme fırsatlarını fark etmesine de yardımcı olacaktır.

## 2.2.3 Eleman İç Yapısı Tasarımı (Element Internals Design)

Üçüncü bir tasarım düzeyi, eleman etkileşimi tasarımını (element interaction design) izler; buna eleman içyapısı tasarımı (element internals design) diyoruz. Genellikle eleman geliştirme etkinliklerinin bir parçası olarak yürütülen bu tasarım düzeyinde, önceki tasarım düzeyinde tanımlanan elemanların içyapıları, elemanın arayüzünü (interface) karşılayacak şekilde oluşturulur.

Mimari kararlar bu üç tasarım düzeyinin her birinde ortaya çıkabilir ve çıkar. Dahası, mimari tasarım sırasında mimar, belirli bir mimari sürücüye (architectural driver) ulaşmak için eleman içyapısı tasarımı düzeyine kadar inmek zorunda kalabilir. Buna daha önce tartışılan arabellekleme stratejisinin (buffering strategy) seçimi örnek gösterilebilir. Bu anlamda mimari tasarım önemli ölçüde ayrıntı içerebilir; bu da neden onu “üst düzey tasarım (high-level design)” ya da “ayrıntılı tasarım (detailed design)” terimleriyle düşünmeyi sevmediğimizi açıklar (bkz. kenar yazı “Ayrıntılı Tasarım?”).

Mimari tasarım, eleman etkileşimi tasarımından; eleman etkileşimi tasarımı da eleman içyapısı tasarımından önce gelir. Bu mantıksal olarak gereklidir: Elemanların kendileri tanımlanmadan bir elemanın içyapısı tasarlanamaz; birkaç eleman ve aralarındaki bazı etkileşim örüntüleri tanımlanmadan da etkileşim hakkında muhakeme edilemez. Ancak projeler büyüyüp evrildikçe, uygulamada bu etkinlikler arasında ciddi miktarda yineleme (iteration) olur.

### Ayrıntılı Tasarım?

“Ayrıntılı tasarım (detailed design)” terimi, modüllerin içyapısının tasarımına atıfta bulunmak için sıklıkla kullanılır. Yaygın bir kullanım alanı olsa da, “üst düzey tasarım (high-level design)” ile bir tür karşıtlık içinde sunulduğu için, biz bu terimi gerçekten sevmiyoruz. Bunun yerine, daha kesin terimler olan “mimari tasarım (architectural design)”, “eleman etkileşimi tasarımı (element interaction design)” ve “eleman içyapısı tasarımı (element internals design)” ifadelerini tercih ediyoruz.

Sonuçta, sisteminiz karmaşıksa, mimari tasarım oldukça ayrıntılı olabilir. Ve bazı tasarım “ayrıntıları” da mimari nitelik taşıyacaktır. Aynı nedenle, “üst düzey tasarım (high-level design)” ve “alt düzey tasarım (low-level design)” terimlerini de sevmiyoruz. Bu terimlerin gerçekte ne anlama geldiğini kim gerçekten bilebilir? Açıkçası “üst düzey tasarım”, bir şekilde “daha üstte” veya daha soyut olmalı ve “alt düzey tasarım”dan mimari manzarayı daha geniş kapsamlı ele almalıdır; ancak bunun ötesinde bu terimlere herhangi bir kesin anlam yükleyemiyoruz.

Bu yüzden şu öneride bulunuyoruz: “üst (high)”, “alt (low)” veya “ayrıntılı (detailed)” gibi terimleri tümüyle kullanmaktan kaçının. Her zaman “mimari (architectural)”, “eleman etkileşimi (element interaction)” veya “eleman içyapısı (element internals)” tasarımı gibi daha iyi, daha kesin bir seçim vardır!

Verdiğiniz kararların etkisi, tasarım dokümantasyonunuzda aktarmaya çalıştığınız bilgi ve bu bilginin muhtemel hedef kitlesi üzerine dikkatle düşünün; sonra da bu sürece uygun, anlamlı bir ad verin.

## 2.3 Mimari Tasarım Neden Bu Kadar Önemli?

Belirli tasarım kararlarını vermemenin ya da onları yeterince erken vermemenin bir proje için çok yüksek bir maliyeti vardır. Bu durum, pek çok farklı biçimde kendini gösterir. Erken safhalarda, ilk mimari, proje teklifleri (ya da danışmanlık dünyasında bazen dendiği gibi, satış öncesi süreç – pre-sales process) açısından kritiktir. Bir miktar mimari düşünme ve erken tasarım çalışması yapmadan, proje maliyetini, takvimini ve kalitesini güvenle öngöremezsiniz. Daha bu kadar erken bir aşamada bile, mimari; mimari sürücüleri (architectural drivers) gerçekleştirmek için temel yaklaşımları, kaba iş kırılım yapısını (work-breakdown structure) ve sistemi hayata geçirmek için gereken araç, yetkinlik ve teknolojilerin seçimlerini belirleyecektir.

Ek olarak, mimari, Bölüm 9’da tartışacağımız üzere çevikliğin (agility) önemli bir kolaylaştırıcısıdır. Kuruluşunuz Çevik (Agile) süreçleri benimsemiş olsun ya da olmasın, hiç kimsenin gönüllü olarak kırılgan, değiştirilmesi veya genişletilmesi ya da ayarlanması zor bir mimari seçmek isteyeceğini hayal etmek zordur—ama bu yine de sürekli olur. Bu sözde teknik borç (technical debt) çeşitli nedenlerle ortaya çıkar; ama bunların en başında, genellikle paydaş (stakeholder) taleplerince yönlendirilen özelliklere (features) odaklanma ile mimarların ve proje yöneticilerinin iyi mimari uygulamaların yatırım getirisini (return on investment, ROI) ölçememesi gelir. Özellikler anında fayda sağlar. Mimari iyileştirme ise anında maliyet, uzun vadede fayda sağlar. Bu şekilde dile getirildiğinde, neden hiç kimse mimariye “yatırım” yapsın ki? Yanıt basittir: Mimari olmadan, sistemin sağlaması beklenen faydalar çok daha zor elde edilir.

Basitçe söylemek gerekirse, eğer bazı kilit mimari kararları erken vermezseniz ve mimarinizin bozulmasına izin verirseniz, sprint hızını (sprint velocity) koruyamayacaksınız; çünkü değişiklik taleplerine kolaylıkla yanıt veremeyeceksiniz. Bununla birlikte, Agile Manifesto’nun ilk yaratıcılarının öne sürdüğü şu iddia ile kesinlikle hemfikir değiliz: “En iyi mimariler, gereksinimler ve tasarımlar kendi kendini organize eden (self-organizing) takımlardan ortaya çıkar.” Aslında, bu noktadaki itirazımız, tam da bu kitabı yazmış olmamızın nedenidir. İyi mimari tasarım zordur (ve hâlâ nadirdir) ve kendiliğinden “ortaya çıkmaz”. Bu görüşümüz, Çevik topluluk içerisinde giderek artan bir uzlaşıyı yansıtmaktadır. Gittikçe daha fazla biçimde, “ölçekli disiplinli çeviklik (disciplined agility at scale)”, “yürüyen iskelet (walking skeleton)” ve “ölçeklenmiş Çevik çerçeve (scaled Agile framework)” gibi tekniklerin, Çevik düşünce liderleri ve uygulayıcıları tarafından benimsendiğini görüyoruz. Bu tekniklerin her biri, geliştirmenin büyük bir kısmından önce, hatta kimi zaman herhangi bir geliştirmeden bile önce, bir miktar mimari düşünme ve tasarım yapılmasını savunur. Bir kez daha vurgulamak gerekirse: Çevikliği mümkün kılan mimaridir, tersi değil.

Ayrıca, mimari tasarım kararı olmamakla birlikte, mimari diğer bazı kararları da etkiler (ama belirlemez). Bu kararlar kalite niteliklerinin (quality attributes) elde edilmesini doğrudan etkilemez; fakat yine de mimar tarafından verilmesi gerekebilir. Örneğin bu tür kararlar, araçların seçimini; geliştirme ortamının yapılandırılmasını; sürüm, dağıtım (deployment) ve işletim (operations) desteğini ve iş atamalarının yapılmasını içerebilir.

Son olarak, iyi tasarlanmış ve doğru şekilde iletilmiş bir mimari, ekibe rehberlik edecek uzlaşıların sağlanmasının anahtarıdır. Verilecek en önemli uzlaşılar arayüzler (interfaces) ve paylaşılan kaynaklar üzerindekilerdir. Arayüzler üzerinde erken uzlaşmak, bileşen tabanlı geliştirme (component-based development) için önemli, dağıtık geliştirme (distributed development) için ise hayati derecede kritiktir. Bu kararlar er ya da geç verilecektir. Eğer bu kararları erken vermezseniz, sistemin tümleştirilmesi çok daha zor olacaktır. Bölüm 3.6’da, mimari tasarımın bir parçası olarak arayüzlerin nasıl tanımlanacağını—hem diğer sistemlere yönelik dış arayüzleri hem de eleman etkileşimlerinizi aracılık eden iç arayüzleri—tartışacağız.

## 2.4 Mimari Sürücüler (Architectural Drivers)

Mimari tasarıma nitelik temelli tasarım (Attribute-Driven Design, ADD) ile (ya da aslında herhangi bir başka tasarım yöntemiyle) başlamadan önce, ne yaptığınız ve neden yaptığınız hakkında düşünmeniz gerekir. Bu ifade göz kamaştırıcı derecede açık görünse de, şeytan her zamanki gibi ayrıntılardadır. Bu “ne” ve “neden” sorularını mimari sürücüler (architectural drivers) olarak sınıflandırıyoruz. Şekil 2.1’de gösterildiği gibi, bu sürücüler bir tasarım amacını, kalite niteliklerini (quality attributes), birincil işlevselliği, mimari kaygıları ve kısıtları içerir. Bu hususlar sistemin başarısı için kritiktir ve bu nedenle mimariyi yönlendirir ve biçimlendirir.

Diğer önemli gereksinimlerde olduğu gibi, mimari sürücülerin geliştirme yaşam döngüsü boyunca taban çizgisi (baseline) olarak belirlenmesi ve yönetilmesi gerekir.

## 2.4.1 Tasarım Amacı

Öncelikle, elde etmek istediğiniz tasarımın amacını netleştirmeniz gerekir. Bu mimari tasarımı ne zaman ve neden yapıyorsunuz? Kuruluş şu anda en çok hangi iş hedefleriyle ilgileniyor?

1. Mimari tasarımı bir proje teklifinin parçası olarak yapıyor olabilirsiniz (bir danışmanlık organizasyonunda satış öncesi süreç için veya bir şirkette iç proje seçimi ve önceliklendirmesi için; bkz. Bölüm 9.1.1). Proje fizibilitesi, zaman çizelgesi ve bütçesini belirlemenin bir parçası olarak, başlangıç niteliğinde bir mimarinin oluşturulması sık rastlanan bir durumdur. Böylesi bir mimari çok ayrıntılı olmayacaktır; amacı, mimariyi yeterli ayrıntıda anlayıp parçalara ayırarak iş birimlerinin anlaşılmasını ve böylece tahmin edilebilmesini sağlamaktır.
2. Mimari tasarımı, keşif amaçlı bir prototip oluşturma sürecinin parçası olarak yapıyor olabilirsiniz. Bu durumda, mimari tasarım sürecinin amacı yayımlanabilir ya da yeniden kullanılabilir bir sistem oluşturmaktan çok, alanı keşfetmek, yeni teknolojiyi keşfetmek, bir müşterinin önüne hızla geri bildirim almak için çalıştırılabilir bir şey koymak ya da performans ölçeklenebilirliği veya erişilebilirlik için devralma (failover) gibi bir kalite niteliğini keşfetmektir.
3. Mimarinizi geliştirme sırasında tasarlıyor olabilirsiniz. Bu, tamamen yeni bir sistem, yeni bir sistemin önemli bir bölümü veya yeniden düzenlenen (refactor) ya da değiştirilen mevcut bir sistemin bir bölümü için olabilir. Bu durumda amaç, gereksinimleri karşılayacak, sistemin inşasını ve iş atamalarını yönlendirecek ve nihai bir yayına hazırlık yapacak kadar tasarım çalışması yapmaktır.

Bu amaçlar; olgun alanlardaki sıfırdan (greenfield) sistemler, yeni alanlardaki sıfırdan sistemler ve mevcut (brownfield) sistemler için farklı biçimlerde yorumlanabilir ve hayata geçirilebilir. Olgun bir alanda, örneğin satış öncesi süreç görece basit olabilir; mimar, mevcut sistemleri örnek olarak yeniden kullanabilir ve benzeşim (analogy) yoluyla güvenle tahminlerde bulunabilir. Yeni alanlarda ise satış öncesi tahmin süreci çok daha karmaşık ve riskli olacak, sonuçlar da yüksek derecede değişkenlik gösterecektir. Bu koşullarda, riski azaltmak ve belirsizliği düşürmek için sistemin ya da sistemin kilit bir parçasının prototipinin oluşturulması gerekebilir. Pek çok durumda, gereksinimler öğrenildikçe ve benimsendikçe bu mimarinin hızlıca uyarlanması da gerekebilir. Brownfield sistemlerde ise gereksinimler daha iyi anlaşılmış olsa da, mevcut sistemin kendisi, planlamanın isabetli olabilmesi için iyi anlaşılması gereken karmaşık bir nesnedir.

Son olarak, geliştirme ya da bakım sırasında geliştirme organizasyonunun hedefleri mimari tasarım sürecini etkileyebilir. Örneğin, organizasyon yeniden kullanım için tasarım yapmayla, gelecekteki genişletme ya da alt kümeleme için tasarım yapmayla, ölçeklenebilirlik için tasarım yapmayla, sürekli teslim (continuous delivery) için tasarım yapmayla, mevcut proje yeteneklerini ve ekip üyelerinin becerilerini en iyi şekilde kullanacak biçimde tasarım yapmayla ilgileniyor olabilir. Ya da organizasyonun bir tedarikçiyle stratejik bir ilişkisi olabilir. Ya da CIO’nun belirli bir beğenisi ya da hoşnutsuzluğu vardır ve bunu projenize dayatmak istemektedir.

> **💬 Çevirmen notu:** Greenfield, hiç mevcut kod/ürün olmayan sıfırdan geliştirme; brownfield ise var olan bir sistemi dönüştürme/evrimleştirme bağlamında kullanılır.

## 2.4 Mimari Sürücüler

Peki, bu hususları neden listelemeye zahmet ediyoruz? Çünkü hem tasarım sürecini hem de tasarım çıktıları etkilerler. Mimariler, iş hedeflerine ulaşmaya yardımcı olmak için vardır. Mimar, bu hedefler konusunda net olmalı, bunları (müzakere ederek!) iletmeli ve tasarım sürecine başlamadan önce açık bir tasarım amacı belirlemelidir.

## 2.4.2 Kalite Nitelikleri (Quality Attributes)

Software Architecture in Practice kitabında, kalite nitelikleri (quality attributes), bir sistemin paydaşlarının (stakeholders) ihtiyaçlarını ne kadar iyi karşıladığını göstermek için kullanılan ölçülebilir ya da test edilebilir özellikler olarak tanımlanır. Kalite başlı başına öznel bir kavram olma eğiliminde olduğundan, bu özellikler, kalitenin özlü ve nesnel biçimde ifade edilmesini sağlar.

Sürücüler arasında, mimariyi en belirgin biçimde şekillendirenler kalite nitelikleridir. Mimari tasarım yaparken verdiğiniz kritik kararlar, büyük ölçüde, sisteminizin bu yönlendirici kalite niteliği hedeflerini hangi açılardan karşılayacağını veya karşılayamayacağını belirler.

Önemleri göz önüne alındığında, kalite niteliklerinin ortaya çıkarılması (eliciting), belirtilmesi (specifying), önceliklendirilmesi (prioritizing) ve doğrulanması (validating) konusunda özen göstermeniz gerekir. Bu sürücüleri doğru belirlemenin bu kadar çok şeye bağlı olması, görevi göz korkutucu kılıyor gibi görünebilir. Neyse ki, bu konuda size yardımcı olabilecek, iyi anlaşılmış ve yaygın biçimde bilinen bir dizi teknik vardır (bkz. yandaki kutu “Kalite Nitelikleri Çalıştayı ve Fayda Ağacı (Utility Tree)”):

- Kalite Nitelikleri Çalıştayı (Quality Attribute Workshop, QAW), bir grup sistem paydaşını içeren ve kalite niteliklerinin ortaya çıkarılması, belirtilmesi, önceliklendirilmesi ve üzerinde uzlaşıya varılması faaliyetlerinin büyük bölümünü kapsayan, kolaylaştırılmış (facilitated) bir beyin fırtınası oturumudur.
- Görev Dizisi Çalıştayı (Mission Thread Workshop), sistemler sistemi (system of systems) için QAW ile aynı amaca hizmet eder.
- Fayda Ağacı (Utility Tree), mimar tarafından kalite niteliği gereksinimlerini teknik zorluk ve risk düzeylerine göre önceliklendirmek için kullanılabilir.

Kalite niteliği gereksinimlerini tartışmanın, belgelemenin ve önceliklendirmenin en iyi yolunun, bunları bir senaryo (scenario) kümesi olarak ele almak olduğuna inanıyoruz. En temel biçimiyle bir senaryo, sistemin bir uyarana (stimulus) verdiği tepkiyi tanımlar. Peki senaryolar neden en iyi yaklaşımdır? Çünkü diğer tüm yaklaşımlar daha kötüdür! “Performans”, “değiştirilebilirlik (modifiability)” veya “yapılandırılabilirlik (configurability)” gibi terimleri tanımlamak için sonsuz zaman harcanabilir; oysa bu tartışmalar gerçek sistem hakkında çok az ışık tutma eğilimindedir. Bir sistemin “değiştirilebilir” olacağını söylemek anlamsızdır, çünkü her sistem bazı değişiklikler açısından değiştirilebilir, bazıları açısından ise değildir. Buna karşın, belirli bir değişiklik talebine yanıt olarak ulaşmak istediğiniz değiştirilebilirlik tepki ölçüsünü (örneğin geçen süre ya da efor) belirtebilirsiniz. Örneğin, “e-ticaret sisteminde kargo ücretlerini güncelleme değişikliğinin …” diye belirtebilirsiniz.

web sitesinin “1 kişi-gününden daha az emekle tamamlanıp test edilmesi” — yani tartışmaya yer bırakmayan bir ölçüt.

Dolayısıyla, bir kalite niteliği senaryosunun (quality attribute scenario) kalbinde bir uyarıcının (stimulus) bir tepkiyle (response) eşleştirilmesi vardır. Diyelim ki bir video oyunu geliştiriyorsunuz ve şöyle bir işlevsel gereksiniminiz var: “Kullanıcı <C> düğmesine bastığında oyun görünüm kiplerini değiştirmelidir.” Bu işlevsel gereksinim önemliyse, kalite niteliği gereksinimleriyle ilişkilendirilmelidir. Örneğin:

- Bu işlev ne kadar hızlı olmalıdır?
- Bu işlev ne kadar güvenli olmalıdır?
- Bu işlev ne kadar değiştirilebilir (modifiye edilebilir) olmalıdır?

Bu sorunu ele almak için, bir kalite niteliği gereksinimini bir senaryo ile tanımlarız. Bir kalite niteliği senaryosu, bir sistemden bir uyarıcıya karşı nasıl yanıt vermesinin beklendiğini anlatan kısa bir açıklamadır. Örneğin, az önce verilen işlevsel gereksinimi şöyle açıklayıp not düşebiliriz: “Kullanıcı <C> düğmesine bastığında, oyun görünüm kiplerini < 500 ms içinde değiştirmelidir.” Bir senaryo, bir uyarıcıyı (bu durumda <C> düğmesine basılması) bir yanıtla (görünüm kipinin değiştirilmesi) ilişkilendirir ve bu yanıt bir yanıt ölçütü (response measure) (< 500 ms) ile ölçülür. Tam bir kalite niteliği senaryosu üç bileşen daha ekler: uyarıcının kaynağı (stimulus source) (bu durumda kullanıcı), etkilenen artefakt (artifact) (bu durumda, uçtan uca gecikme ile ilgilendiğimiz için artefakt tüm sistemdir) ve ortam (environment) (normal çalışmada mıyız, başlangıçta mı, bozulmuş modda mı, yoksa başka bir kipte mi?). Toplamda, tamamen iyi tanımlanmış bir senaryonun altı parçası vardır; Şekil 2.2’de gösterildiği gibi.

![Şekil 2.2](/home/runner/workspace/scripts/dsa_figs/sekil_2_2.png){width=11.47cm}


1  
Uyarıcı  
Uyarıcının  
Kaynağı  

Artefakt  

Tepki  

Ortam  

ŞEKİL 2.2 Bir kalite niteliği senaryosunun altı parçası  

2  
3  
4  

Tepki  
Ölçütü  

### 2.4 Mimari Sürücüler (Architectural Drivers)

Senaryolar, ele alınan sistemin kalite niteliği davranışına ilişkin test edilebilir, yanlışlanabilir hipotezlerdir. Açık tanımlanmış uyarıcı ve tepkileri olduğu için, bir tasarımı senaryoyu ne ölçüde destekleyebildiği açısından değerlendirebiliriz ve bir prototip ya da tam olarak gerçekleştirilmiş sistem üzerinde ölçümler yapıp, senaryoyu pratikte karşılayıp karşılamadığını test edebiliriz. Eğer analiz (ya da prototipleme sonuçları) senaryonun tepki hedefinin karşılanamayacağını gösterirse, hipotez yanlışlanmış sayılır.

Diğer gereksinimlerde olduğu gibi, senaryolar da önceliklendirilmelidir. Bu, her senaryo ile ilişkilendirilen ve önem derecesi atanan iki boyut dikkate alınarak gerçekleştirilebilir:

- Birinci boyut, sistemin başarısı açısından senaryonun önemine karşılık gelir. Bu, müşteri tarafından derecelendirilir.
- İkinci boyut, senaryo ile ilişkili teknik risk derecesine karşılık gelir. Bu, mimar (architect) tarafından derecelendirilir.

Her iki boyutu derecelendirmek için düşük/orta/yüksek (L/M/H) ölçeği kullanılır. Boyutlar derecelendirildikten sonra, (H, H), (H, M) ya da (M, H) birleşimine sahip senaryolar seçilerek senaryolar önceliklendirilir.

Buna ek olarak, bazı geleneksel gereksinim çıkarım (requirements elicitation) teknikleri kalite niteliği gereksinimlerine odaklanacak şekilde hafifçe uyarlanabilir; örneğin Birleşik Gereksinim Planlama (Joint Requirements Planning, JRP), Birleşik Uygulama Tasarımı (Joint Application Design, JAD), keşif amaçlı prototipleme (discovery prototyping) ve hızlandırılmış sistem çözümlemesi (accelerated systems analysis).

Ancak hangi tekniği kullanırsanız kullanın, ölçülebilir kalite niteliklerinin (quality attributes) önceliklendirilmiş bir listesini oluşturmadan tasarıma başlamayın! Paydaşlar (stakeholders) bazen cehaletlerini öne sürebilir (“Ne kadar hızlı olması gerektiğini bilmiyorum; sadece hızlı olsun!”), ancak hemen her zaman en azından olası tepkilerin bir aralığını ortaya çıkarabilirsiniz. Sistemin “hızlı” olması gerektiğini söylemek yerine, paydaşa 10 saniyelik yanıt süresinin kabul edilebilir olup olmadığını sorun. Eğer bu kabul edilemezse, 5 saniye uygun mu, 1 saniye uygun mu diye sorun. Çoğu durumda kullanıcıların, gereksinimleri hakkında fark ettiklerinden daha fazla şey bildiklerini ve en azından onları belirli bir aralığa “sıkıştırabildiğinizi” göreceksiniz.

> **💬 Çevirmen notu:** Burada “yanıt ölçütü” ile kastedilen, kalite niteliğini sayısal olarak ifade eden hedef değerdir; örn. “< 500 ms”, “%99.9 erişilebilirlik”, “8 saatten kısa kurtarma süresi” gibi.

### Kalite Niteliği Çalıştayı (Quality Attribute Workshop) ve Fayda Ağacı (Utility Tree)

#### Kalite Niteliği Çalıştayı (Quality Attribute Workshop, QAW)

Kalite Niteliği Çalıştayı (Quality Attribute Workshop, QAW), kalite niteliği senaryolarını üretmek, önceliklendirmek ve iyileştirmek için kullanılan, kolaylaştırıcılı (facilitated), paydaş odaklı bir yöntemdir. Bir QAW oturumu ideal olarak yazılım mimarisi tanımlanmadan önce gerçekleştirilir; ancak pratikte, QAW’nin yazılım geliştirme yaşam döngüsünün her aşamasında kullanıldığını gördük. QAW, sistem düzeyindeki kaygılara ve özel olarak yazılımın sistemde oynayacağı role odaklanır. QAW’nin adımları şöyledir:

22 Bölüm 2—Mimari Tasarım

1. QAW Sunumu ve Tanışmalar  
QAW (Quality Attribute Workshop) kolaylaştırıcıları, QAW’nin arkasındaki motivasyonu açıklar ve yöntemin her adımını anlatır.

2. İş Hedefleri Sunumu  
Projeye ait iş ile ilgili kaygıları temsil eden bir paydaş (stakeholder), sistemin iş bağlamını, geniş kapsamlı işlevsel gereksinimlerini, kısıtlarını ve bilinen kalite niteliği (quality attribute) gereksinimlerini sunar. İlerleyen QAW adımlarında ayrıntılandırılacak kalite nitelikleri, bu adımda sunulan iş hedeflerinden türetilecek ve bu hedeflere izlenebilir olmalıdır. Bu nedenle, bu iş hedeflerinin önceliklendirilmiş olması gerekir.

3. Mimari Plan Sunumu  
Mimar, sistem mimari planlarını mevcut hâliyle sunar. Mimari çoğu zaman henüz tanımlanmamış olsa da (özellikle sıfırdan geliştirilen (greenfield) sistemler için), mimar çoğunlukla bu erken aşamada bile mimari hakkında oldukça çok şey bilmektedir. Örneğin, halihazırda zorunlu kılınmış teknolojileri, bu sistemin etkileşime geçmesi gereken diğer sistemleri, uyulması gereken standartları, yeniden kullanılabilecek alt sistemleri veya bileşenleri ve benzeri unsurları biliyor olabilir.

4. Mimari Sürücülerin (architectural driver) Belirlenmesi  
Kolaylaştırıcılar, 2. ve 3. adımlarda derledikleri temel mimari sürücü (architectural driver) listelerini paydaşlarla paylaşır ve paydaşlardan açıklama, ekleme, çıkarma ve düzeltme isterler. Buradaki amaç; başlıca işlevsel gereksinimleri, iş sürücülerini (business driver), kısıtları ve kalite niteliklerini kapsayan, damıtılmış bir mimari sürücü listesi üzerinde uzlaşmaya varmaktır.

5. Senaryo Beyin Fırtınası  
Bu bağlam verildikten sonra, her paydaşın artık sistemle ilgili kendi ihtiyaç ve beklentilerini temsil eden bir senaryo ifade etme fırsatı vardır. Kolaylaştırıcılar, her senaryonun açıkça belirtilmiş bir uyarıcı (stimulus) ve yanıt (response) içerdiğinden emin olurlar. Ayrıca, izlenebilirlik ve tamamlık da gözetilir: 4. adımda listelenen her mimari sürücü için en az bir temsilî senaryo bulunmalı ve 2. adımda listelenen tüm iş hedeflerini kapsamalıdır.

6. Senaryo Konsolidasyonu  
Benzer senaryolar, uygun olduğu ölçüde birleştirilir. 7. adımda paydaşlar favori senaryolarına oy verecekleri için, konsolidasyon; özünde aynı kaygıyı dile getiren birden fazla senaryo arasında oyların dağılmasını engellemeye yardımcı olur.

7. Senaryo Önceliklendirme  
Senaryoların önceliklendirilmesi, her paydaşa toplam senaryo sayısının yüzde 30’u kadar oy verilmesiyle gerçekleştirilir. Paydaşlar bu oyları istedikleri senaryo veya senaryolar arasında dağıtabilirler. Tüm paydaşlar oylarını verdikten sonra sonuçlar toplanır ve senaryolar popülerlik sırasına göre sıralanır.

## 2.4 Mimari Sürücüler

8. Senaryo İyileştirme  
En yüksek öncelikli senaryolar iyileştirilir ve detaylandırılır. Kolaylaştırıcılar, paydaşların bu senaryoları altı bölümlü senaryo biçiminde ifade etmelerine yardımcı olur: kaynak (source), uyarıcı (stimulus), artefakt (artifact), ortam (environment), yanıt (response) ve yanıt ölçüsü (response measure).

Dolayısıyla QAW çıktısı, iş hedefleriyle hizalanmış, önceliklendirilmiş bir senaryo listesidir; bu listede en yüksek öncelikli senaryolar incelenmiş ve iyileştirilmiştir. Basit bir sistem için veya bir iterasyonun parçası olarak bir QAW 2–3 saat gibi kısa bir sürede gerçekleştirilebilir; gereksinimlerin tamlığı hedeflendiği karmaşık bir sistemde ise 2 günü bulabilir.

### Fayda Ağacı (Utility Tree)

Hazırda başvurulacak paydaşlar yoksa bile, ne yapacağınıza ve sistemin karşı karşıya olduğu çok sayıdaki zorluğu nasıl önceliklendireceğinize karar vermeniz gerekir. Düşüncelerinizi düzenlemenin bir yolu, bir Fayda Ağacı (Utility Tree) oluşturmaktır. Aşağıdaki şekilde gösterilene benzer bir Fayda Ağacı, kalite niteliği hedeflerinizi ayrıntılı olarak ifade etmenize ve ardından bunları önceliklendirmenize yardımcı olur.

- **Performance (performans)**  
  - **Latency (gecikme)** — (M, M)  
    Kullanıcı, zaman sunucusunun olay geçmişini görüntüler. Son 24 saate ait olay listesi 1 saniye içinde görüntülenir.  
  - **Peak load (zirve yük)** — (H, H)  
    Yönetim sistemi, zirve yük sırasında zaman sunucusundan veri toplar. Tüm veriler 5 dakika içinde toplanır.  
    — (M, H)  
    Zaman sunucuları, zirve yük sırasında yönetim sistemine tuzak (trap) mesajları gönderir. Tuzakların (traps) %100’ü başarıyla işlenir ve depolanır.

- **Usability (kullanılabilirlik)**  
  - **Learnability (öğrenilebilirlik)** — (L, L)  
    Yeni bir kullanıcı, hesabını yapılandırabilir ve 8 saatten az eğitimle sistemi kullanıyor durumda olur.  
  - **Feedback (geribildirim)** — (H, L)  
    Kritik olaylar, 5 saniyeden kısa sürede kullanıcıya raporlanır ve görsel hâle getirilir.

- **Availability (kullanılabilirlik/erişilebilirlik)**  
  - **SW failure (yazılım hatası)** — (H, H)  
    Yönetim sisteminde bir hata oluşur. Yönetim sistemi 30 saniyeden kısa sürede çalışmaya devam eder duruma gelir.  
  - **Network failure (ağ hatası)**  
    (Metin ağ hatası senaryosunu örnek şekilden kısaltarak yansıtıyor; varsayımsal ayrıntı eklenmemiştir.)

- **Security (güvenlik)**  
  - **Authentication (kimlik doğrulama)** — (H, M)  
    Kimlik doğrulama, yetkisiz oturum açma girişimlerinin %99.999’unun tespit edilmesini sağlar.  
  - **Audit trail (denetim izi)** — (H, L)  
    Bir kullanıcı sistem yapılandırmasında değişiklik yapar. Bu değişikliklerin %100’ü kaydedilir.

> **💬 Çevirmen notu:** Parantez içindeki (H, M), (M, L) gibi ikililer genellikle “yüksek/orta/düşük iş önemi” ve “yüksek/orta/düşük teknik risk” şeklinde iki boyutlu önceliklendirme derecesini ifade eder; ayrıntısı aşağıdaki öncelik matrisi kısmında açıklanıyor.

Çalışma biçimi şu şekildedir. Önce bir kâğıda “Utility” (fayda) kelimesini yazın. Sonra, sisteminiz için faydayı oluşturan çeşitli kalite niteliklerini yazın. Örneğin, sistemin iş hedeflerine dayanarak, sistem için en önemli niteliklerin hızlı olması, güvenli olması ve kolay değiştirilebilir olması gerektiğini biliyor olabilirsiniz. Buna karşılık, “Utility”nin altına bu kelimeleri yazarsınız. Sonraki adımda, aslında bu terimlerin her birinin ne anlama geldiğini tam olarak bilmiyor olduğumuz için, en çok kaygı duyduğumuz kalite niteliği yönünü tanımlarız. Örneğin, “performans” belirsiz bir ifadedir; “veritabanı işlemlerinin gecikmesi (latency of database transactions)” ise biraz daha az belirsizdir. Benzer şekilde, “modifiability (değiştirilebilirlik)” belirsizdir; “yeni kodeklerin (codec) eklenmesinin kolaylığı (ease of adding new codecs)” biraz daha az belirsizdir.

Ağacın yaprakları, az önce sıraladığınız kalite niteliği hususlarına ilişkin somut örnekler sağlayan senaryolar biçiminde ifade edilir. Örneğin, “veritabanı işlemlerinin gecikmesi” için şu senaryoyu oluşturabilirsiniz: “Normal koşullar altında 1000 kullanıcı kendi müşteri kayıtlarını aynı anda günceller ve ortalama gecikme 1 saniyedir.”  
“Yeni kodeklerin eklenmesinin kolaylığı” için şu senaryoyu oluşturabilirsiniz: “Müşteri, sisteme yeni bir özel kodek eklenmesini talep eder. Kodek, hiçbir yan etki olmaksızın 2 kişi-haftalık (2 person-weeks) eforla sisteme eklenir.”

Son olarak, oluşturduğunuz senaryoların önceliklendirilmesi gerekir. Bu önceliklendirmeyi, iki boyut boyunca sıralama tekniğini kullanarak yaparız ve bunun sonucunda aşağıdakine benzer bir öncelik matrisi elde ederiz (hücrelerde yer alan numaralar, bir dizi sistem senaryosunun kimlik numaralarıdır).

| İş Önemi / Teknik Risk | L                | M        | H              |
|------------------------|------------------|----------|----------------|
| **L**                  | 5, 6, 17, 20, 22 | 1, 14    | 12, 19         |
| **M**                  | 9, 12, 16        | 8, 20    | 3, 13, 15      |
| **H**                  | 10, 18, 21       | 4, 7     | 2, 11          |

Görevimiz, mimar olarak, bu tablonun sağ alt kısmına (H, H) odaklanmaktır: yüksek işletme önemine ve yüksek riske sahip senaryolara. Bu senaryoları tatmin edici biçimde ele aldıktan sonra (M, H) veya (H, M) olanlara geçebilir ve ardından tüm sistemin senaryoları ele alınana kadar (ya da çoğu zaman olduğu gibi zamanımız veya bütçemiz tükenene kadar) yukarı ve sola doğru ilerleyebiliriz.

QAW (Quality Attribute Workshop) ve Fayda Ağacı (Utility Tree) tekniklerinin aynı hedefe yönelik iki farklı teknik olduğuna dikkat edilmelidir: En önemli kalite niteliği (quality attribute) gereksinimlerini ortaya çıkarmak ve önceliklendirmek. Bunlar, en kritik mimari sürücülerinizden (architectural driver) bazıları olacaktır. Ancak bu teknikler arasında seçim yapmak için hiçbir neden yoktur. Her ikisi de yararlı ve değerlidir ve deneyimlerimize göre tamamlayıcı güçlü yönlere sahiptirler: QAW, dış paydaşların (stakeholder) gereksinimlerine daha fazla odaklanma eğilimindeyken, Fayda Ağacı iç paydaşların gereksinimlerini ortaya çıkarmada daha başarılı olma eğilimindedir. Tüm bu paydaşları memnun etmek, mimarinizin başarısını garanti altına alma yolunda büyük bir adım olacaktır.

## 2.4.3 Birincil İşlevsellik

İşlevsellik (functionality), sistemin amaçlandığı işi yapabilme yeteneğidir. Kalite niteliklerinin aksine, sistemin yapısının nasıl olduğu normalde işlevselliği etkilemez. Belirli bir sistemin tüm işlevselliğini tek, devasa bir modülde kodlayabilirsiniz ya da bunu pek çok küçük, yüksek bağlaşıklığa sahip modüle düzgün bir şekilde dağıtabilirsiniz. Yalnızca işlevselliği dikkate alırsanız, dışarıdan bakıldığında sistem aynı görünür ve aynı şekilde çalışır. Ancak önemli olan, bu tür bir sistemi değiştirmek istediğinizde ne olduğudur. İlk durumda değişiklikler zor ve maliyetli olacaktır; ikinci durumda ise çok daha kolay ve ucuz olmalıdır. Mimari tasarım açısından önemli olan, işlevselliğin bizzat kendisinden ziyade, işlevselliğin öğelere (elements) nasıl tahsis edildiğidir. İyi bir mimari, en sık yapılan değişikliklerin tek bir öğede ya da az sayıda öğede yerelleştirildiği ve dolayısıyla kolayca yapılabildiği bir mimaridir.

Bir mimari tasarlarken, en azından birincil işlevselliği (primary functionality) dikkate almanız gerekir. Birincil işlevsellik genellikle, sistemin geliştirilmesini motive eden iş hedeflerine ulaşmak için kritik olan işlevsellik olarak tanımlanır. Birincil işlevsellik için diğer ölçütler, yüksek düzeyde teknik zorluk içermesi veya birçok mimari öğenin etkileşimini gerektirmesi olabilir. Kabaca bir kural olarak, kullanım senaryolarınızın (use case) ya da kullanıcı hikâyelerinizin (user story) yaklaşık yüzde 10’unun birincil olması muhtemeldir.

Bir mimari tasarlarken birincil işlevselliği dikkate almanız gereken iki önemli neden vardır:  
1. İşlevselliğin, değiştirilebilirliği (modifiability) ya da yeniden kullanılabilirliği (reusability) teşvik edecek ve aynı zamanda iş atamalarını planlamanıza yardımcı olacak biçimde öğelere (genellikle modüllere) nasıl tahsis edileceğini düşünmeniz gerekir.  
2. Bazı kalite niteliği senaryoları (quality attribute scenario) sistemdeki birincil işlevsellikle doğrudan bağlantılıdır. Örneğin, bir film akış (streaming) uygulamasında birincil kullanım senaryolarından biri elbette bir film izlemektir. Bu kullanım senaryosu, “Kullanıcı oynat’a bastıktan sonra film en fazla 5 saniye içinde akışa başlamalıdır” gibi bir performans kalite niteliği senaryosu ile ilişkilidir. Bu durumda, kalite niteliği senaryosu doğrudan birincil kullanım senaryosu ile ilişkilidir; dolayısıyla bu senaryoyu destekleyecek kararlar almak, aynı zamanda ilişkili işlevselliğin nasıl destekleneceğine dair kararlar almayı da gerektirir. Bu durum tüm kalite nitelikleri için geçerli değildir. Örneğin, bir kullanılabilirlik (availability) senaryosu sistem arızasından kurtulmayı içerebilir ve bu arıza sistemin herhangi bir kullanım senaryosu yürütülürken meydana gelebilir.

Mimari tasarım sırasında işlevselliğin tahsisine ilişkin alınan kararlar, geliştirme ilerledikçe geri kalan işlevselliğin modüllere nasıl tahsis edilmesi gerektiğine dair bir emsal oluşturur. Bu genellikle mimarın işi değildir; bunun yerine, bu etkinlik tipik olarak Bölüm 2.2.2’de açıklanan öğe etkileşim tasarımı (element interaction design) sürecinin bir parçası olarak yürütülür.

Son olarak, işlevselliğin tahsisine ilişkin alınan kötü kararlar teknik borcun (technical debt) birikmesiyle sonuçlanır. (Elbette, bu kararlar yalnızca sonradan bakıldığında kötü olduklarını ortaya koyabilir.) Bu borç, yeniden düzenleme (refactoring) kullanılarak ödenebilir; ancak bu, projenin ilerleme hızını, yani hızını (velocity) etkiler (bkz. “Refactoring” kenar notu).

### Refactoring

Bir yazılım mimarisini (ya da onun bir kısmını) yeniden düzenlerseniz (refactor), yaptığınız şey aynı işlevselliği korumak ancak önemsediğiniz bir kalite niteliğini değiştirmektir. Mimarlar, sistemin bir bölümünün anlaşılması, hata ayıklanması ve bakımı zor olduğunda genellikle yeniden düzenleme yapmayı tercih ederler. Alternatif olarak, sistemin bir bölümü yavaş olduğu, arızaya yatkın olduğu veya güvensiz olduğu için de yeniden düzenleme yapılabilir.

Her durumda yeniden düzenlemenin amacı işlevselliği değiştirmek değil, kalite niteliği tepkisini (quality attribute response) değiştirmektir. (Elbette, işlevselliğe yapılan eklemeler bazen bir yeniden düzenleme çalışması ile birlikte ele alınır, ancak bu yeniden düzenlemenin esas amacı değildir.) Açıkça, aynı işlevselliği koruyup mimariyi farklı kalite niteliği tepkileri elde edecek şekilde değiştirebiliyorsak, bu gereksinim türleri birbirine dik (orthogonal), yani birbirinden bağımsız olarak değişebilir niteliktedir.

## 2.4.4 Mimari Kaygılar

Mimari kaygılar (architectural concern), mimari tasarımın bir parçası olarak dikkate alınması gereken, ancak geleneksel gereksinimler olarak ifade edilmeyen ek yönleri kapsar. Birkaç farklı türde kaygı vardır:

- **Genel kaygılar.** Bunlar, mimari oluştururken ele alınan “genel” konulardır; örneğin genel bir sistem yapısının kurulması, işlevselliğin modüllere tahsisi, modüllerin ekiplere tahsisi, kod tabanının organizasyonu, başlatma ve kapatma (startup/shutdown), teslimatı, dağıtımı (deployment) ve güncellemeleri destekleme gibi konular.
- **Özel kaygılar.** Bunlar, çok sayıda uygulamada ortak olan, daha ayrıntılı sistem-içi konulardır; örneğin hata yönetimi (exception management), bağımlılık yönetimi (dependency management), yapılandırma (configuration), günlükleme (logging), kimlik doğrulama (authentication), yetkilendirme (authorization), önbellekleme (caching) ve benzeri. Bazı özel kaygılar, başvuru mimarilerinde (reference architecture; bkz. Bölüm 2.5.1) ele alınır, ancak diğerleri sisteminize özgü olacaktır. Özel kaygılar, önceki tasarım kararlarının bir sonucu olarak da ortaya çıkar. Örneğin, daha önce web uygulamalarının geliştirilmesi için bir başvuru mimarisi kullanmaya karar verdiyseniz, oturum yönetimi (session management) ile ilgilenmeniz gerekebilir.

> **💬 Çevirmen notu:** “Mimari kaygı (architectural concern)” terimi, hem teknik hem organizasyonel mimari meseleleri kapsayan üst bir şemsiye kavram olarak kullanılmaktadır; yalnızca “sorun” anlamında değil, “dikkate alınması gereken konu” anlamında okunmalıdır.

§ İçsel gereksinimler. Bu gereksinimler genellikle geleneksel gereksinim dokümanlarında açıkça belirtilmez, çünkü müşteriler bunları nadiren ifade eder. İçsel gereksinimler, sistemin geliştirilmesini, dağıtımını, işletimini veya bakımını kolaylaştıran yönleri ele alabilir. Bazen “türetilmiş gereksinimler (derived requirements)” olarak da adlandırılırlar.

§ Konular (issues). Bunlar, bir tasarım gözden geçirmesi (design review, bkz. Bölüm 8.6) gibi analiz faaliyetlerinin bir sonucudur ve bu nedenle başlangıçta mevcut olmayabilir. Örneğin, bir mimari değerlendirme, mevcut tasarımda bazı değişiklikler yapılmasını gerektiren bir riski ortaya çıkarabilir.

Mimari kaygılar (architectural concerns) etrafındaki bazı kararlar önemsiz veya bariz olabilir. Örneğin, bir gömülü sistem için dağıtım yapınız (deployment structure) tek bir işlemci, bir uygulama (app) için tek bir cep telefonu olabilir. Başvuru mimariniz (reference architecture) şirket politikası tarafından kısıtlanmış olabilir. Kimlik doğrulama ve yetkilendirme politikalarınız kurumsal mimariniz (enterprise architecture) tarafından belirlenmiş ve ortak bir çerçevede (framework) gerçekleştirilmiş olabilir. Ancak diğer durumlarda, belirli kaygıları karşılamak için gerekli kararlar o kadar bariz olmayabilir — örneğin, hata yönetimi (exception management), girdi doğrulama (input validation) veya kod tabanının yapılandırılması konularında.

Önceki deneyimlerinden dolayı, tecrübeli mimarlar genellikle belirli bir sistem türüyle ilişkili kaygıların farkındadır ve bunları ele almak için tasarım kararları alma ihtiyacını bilirler. Deneyimsiz mimarlar ise genellikle bu tür kaygıların farkında değildir; bu kaygılar çoğu zaman örtük (tacit) olup açıkça ifade edilmediğinden, onları tasarım sürecinin bir parçası olarak görmeyebilirler ve bu da sıklıkla daha sonra problemlere yol açar.

Mimari kaygılar sıklıkla yeni kalite niteliği senaryolarının (quality attribute scenarios) ortaya çıkmasına yol açar. Örneğin “günlüklemeyi (logging) desteklemek” kaygısı çok belirsizdir ve daha özel hale getirilmesi gerekir. Müşteri tarafından sağlanan kalite niteliği senaryolarında olduğu gibi, bu senaryoların da önceliklendirilmesi gerekir. Ancak bu senaryolarda müşteri; geliştirme ekibinin kendisi, operasyon birimi veya organizasyonun diğer üyeleridir. Tasarım sırasında mimar, hem müşteri tarafından sağlanan kalite niteliği senaryolarını hem de mimari kaygılardan türetilen bu senaryoları dikkate almak zorundadır.

ADD yönteminin (Attribute-Driven Design, nitelik temelli tasarım) gözden geçirilmesindeki hedeflerimizden biri, mimari kaygıların mimari tasarım sürecine yönelik açık girdiler olarak önemini artırmaktı; bu durum Bölüm 4, 5 ve 6’daki örneklerimiz ve vaka çalışmalarımızda vurgulanacaktır.

### 2.4.5 Kısıtlar

Mimari tasarım sürecinin bir parçası olarak geliştirme üzerindeki kısıtları kataloglamanız gerekir. Bu kısıtlar; zorunlu teknolojiler, sisteminizin birlikte çalışması (interoperate) veya tümleşmesi (integrate) gereken diğer sistemler, uyulması gereken kanunlar ve standartlar, geliştiricilerinizin yetenekleri ve kullanılabilirliği, pazarlık edilemez son teslim tarihler (deadline), eski sistem sürümleriyle geriye dönük uyumluluk (backward compatibility) ve benzeri biçimler alabilir. Teknik bir kısıt örneği, açık kaynak teknolojilerin kullanılması iken, teknik olmayan bir kısıt, sistemin Sarbanes-Oxley Yasası’na uymak zorunda olması veya 15 Aralık tarihine kadar teslim edilmesi zorunluluğudur.

Bir kısıt, mimar olarak üzerinde çok az ya da hiç denetiminizin olmadığı bir karardır. Bölüm 1’de belirttiğimiz gibi, göreviniz “satisfice” etmektir: Karşı karşıya olduğunuz kısıtlara rağmen mümkün olan en iyi sistemi tasarlamak. Bazen bir kısıtın gevşetilmesi için tartışma yürütebilirsiniz, ancak çoğu durumda başka seçeneğiniz yoktur ve kısıtların etrafından dolaşarak tasarım yapmanız gerekir.

> **💬 Çevirmen notu:** “Satisfice” burada hem “yeterince iyi olacak şekilde tatmin etmek” hem de “en iyiye değil, kısıtlar altında yeterli olana yönelmek” anlamında, yazarların bilinçli tercih ettiği bir terimdir.

---

## 2.5 Yapıların Oluşturulması için Tasarım Kavramları (Design Concepts)

Tasarım rastgele değil, planlı, kasıtlı, akılcı ve yönlendirilmiş bir etkinliktir. Tasarım süreci ilk başta göz korkutucu görünebilir. Herhangi bir tasarım etkinliğinin başındaki “boş sayfa” ile karşı karşıya kalındığında, olasılıklar uzayı imkânsız ölçüde büyük ve karmaşık görünebilir. Ancak burada bazı yardımcı unsurlar vardır. Yazılım mimarisi topluluğu, onlarca yıl boyunca, yüksek kaliteli ve öngörülebilir sonuçlar veren tasarımlar oluşturmamıza rehberlik edebilecek, genel kabul görmüş tasarım ilkelerinden oluşan bir gövde yaratmış ve geliştirmiştir.

Örneğin, iyi belgelenmiş bazı tasarım ilkeleri belirli kalite niteliklerinin (quality attributes) gerçekleştirilmesine yöneliktir:

§ Yüksek değiştirilebilirlik (modifiability) elde etmeye yardımcı olmak için, yüksek birleşiklik (high cohesion) ve düşük bağlaşıklık (low coupling) anlamına gelen iyi bir modülerlik hedefleyin.  
§ Yüksek kullanılabilirlik (availability) elde etmeye yardımcı olmak için, tek bir hata noktasına (single point of failure) sahip olmaktan kaçının.  
§ Ölçeklenebilirlik (scalability) elde etmeye yardımcı olmak için, kritik kaynaklar için kod içine gömülü (hard-coded) sınırlar bulundurmaktan kaçının.  
§ Güvenlik (security) elde etmeye yardımcı olmak için, kritik kaynaklara erişim noktalarını sınırlayın.  
§ Test edilebilirliği (testability) elde etmeye yardımcı olmak için, durumu (state) dışsallaştırın (externalize state).  
§ … ve benzeri.

Her bir durumda, bu ilkeler, uygulamada söz konusu kalite nitelikleriyle onlarca yıl uğraşmanın sonucunda evrilmiştir. Buna ek olarak, tasarımda ve nihayetinde kodda bu soyut yaklaşımların yeniden kullanılabilir gerçekleştirimlerini geliştirdik. Bu yeniden kullanılabilir gerçekleştirimlere tasarım kavramları (design concepts) diyoruz ve bunlar, mimariyi oluşturan yapıların yaratıldığı yapı taşlarıdır. Farklı türlerde tasarım kavramları vardır ve burada en yaygın kullanılanlardan bazılarını tartışıyoruz: başvuru mimarileri (reference architectures), dağıtım desenleri (deployment patterns), mimari desenler (architectural patterns), taktikler (tactics) ve dışarıdan geliştirilmiş bileşenler (örneğin çerçeveler – frameworks). İlk dört tanesi kavramsal nitelikteyken, sonuncusu betimsel (somut, concrete) niteliktedir.

## 2.5 Tasarım Kavramları: Yapıların Oluşturulması için Yapı Taşları

29

### 2.5.1 Başvuru Mimarileri (Reference Architectures)

Referans mimariler, belirli türdeki uygulamalar için genel bir mantıksal yapı sağlayan taslaklardır. Bir referans mimarisi, bir veya daha fazla mimari desen (architectural pattern) üzerine eşlenmiş bir referans modeldir (reference model). İş ve teknik bağlamlarda kendini kanıtlamıştır ve kullanımını kolaylaştıran bir dizi destekleyici yapıt (artifact) ile birlikte gelir.

Web uygulamalarının geliştirilmesi için bir referans mimarisi örneği, bir sonraki sayfadaki Şekil 2.3’te gösterilmektedir. Bu referans mimarisi, bu tür uygulamalar için temel katmanları—sunum (presentation), iş (business) ve veri (data)—belirlemenin yanı sıra, bu katmanlar içinde yer alan öğe türlerini ve bu öğelerin sorumluluklarını da tanımlar; örneğin, UI bileşenleri, iş bileşenleri, veri erişim bileşenleri (data access components), servis aracıları (service agents) vb. Ayrıca bu referans mimarisi, ele alınması gereken güvenlik (security) ve iletişim (communication) gibi kesen ilgileri (cross-cutting concerns) de tanıtır. Bu örneğin gösterdiği gibi, uygulamanız için bir referans mimarisi seçtiğinizde, tasarım sırasında ele almanız gereken bir dizi meseleyi de benimsemiş olursunuz. İletişim veya güvenlikle ilgili açık bir gereksiniminiz olmasa bile, bu öğelerin referans mimarisinin parçası olması, onlar hakkında tasarım kararları vermenizi gerektirir.

![Şekil 2.3](/home/runner/workspace/scripts/dsa_figs/sekil_2_3.png){width=11.43cm}


Referans mimariler mimari stillerle (architectural styles) karıştırılabilir, ancak bu iki kavram farklıdır. Mimari stiller (örneğin “Boru ve Filtre (Pipe and Filter)” ve “İstemci–Sunucu (Client–Server)”), bir uygulamayı mantıksal veya fiziksel olarak yapılandırırken faydalı olan, belirli bir topolojideki bileşen ve bağlaç (connector) türlerini tanımlar. Bu tür stiller teknoloji ve alan (domain) bağımsızdır. Buna karşılık, referans mimariler belirli alanlardaki uygulamalar için bir yapı sunar ve farklı stilleri barındırabilir. Ayrıca, mimari stiller akademide popüler olma eğilimindeyken, referans mimariler uygulayıcılar tarafından tercih edilmektedir—ki bu da, tasarım kavramları listemizde onları tercih etmemizin nedenlerinden biridir.

Pek çok referans mimarisi bulunmasına rağmen, bunların kapsamlı bir listesini içeren herhangi bir katalogdan haberdar değiliz.

## 2.5.2 Mimari Tasarım Desenleri

Tasarım desenleri (design patterns), tanımlanmış bir bağlamda yinelenen tasarım problemlerine yönelik kavramsal çözümlerdir. Tasarım desenleri başlangıçta örnekleme (instantiation), yapılandırma ve davranış gibi nesne ölçeğindeki kararlara odaklanırken, günümüzde farklı ayrıntı düzeylerindeki (granularity) kararlara hitap eden desen katalogları mevcuttur. Buna ek olarak, güvenlik veya tümleştirme (integration) gibi kalite niteliklerini (quality attributes) ele almak için özel desenler de vardır.

Bazı kişiler, mimari desen (architectural pattern) olarak gördükleri şey ile daha ince taneli (fine-grained) tasarım desenleri arasında bir ayrım yapılması gerektiğini savunsa da, bunun yalnızca ölçeğe bağlanabilecek ilkeli (prensip temelli) bir fark olduğuna inanmıyoruz. Bir deseni, kullanımı bazı mimari sürücülerin (architectural drivers; bkz. Bölüm 2.2) doyurulmasını doğrudan ve önemli ölçüde etkilediğinde mimari kabul ediyoruz.

Şekil 2.4, sistemi yapılandırmak için yararlı bir mimari desen olan Katmanlar (Layers) desenine bir örnek göstermektedir. Bu tür bir deseni seçtiğinizde, sisteminiz için kaç katmana ihtiyaç duyacağınıza karar vermelisiniz. Şekil 2.5, performansı artırmak için yararlı olan ve eşzamanlılığı (concurrency) destekleyen bir deseni göstermektedir. Bu desenin de somutlaştırılması (instantiation), yani belirli problem ve tasarım bağlamına uyarlanması gerekir. Somutlaştırma Bölüm 3’te ele alınmaktadır.

![Şekil 2.4](/home/runner/workspace/scripts/dsa_figs/sekil_2_4.png){width=11.43cm}


![Şekil 2.5](/home/runner/workspace/scripts/dsa_figs/sekil_2_5.png){width=11.78cm}


Her ne kadar referans mimariler bir tür desen olarak değerlendirilebilse de, bir uygulamayı yapılandırmadaki önemli rolleri ve teknoloji yığınları (technology stacks) ile daha doğrudan bağlantılı olmaları nedeniyle, onları ayrı ele almayı tercih ediyoruz. Ayrıca, bir referans mimari genellikle başka desenleri de içerir ve sık sık bu desenleri kısıtlar. Örneğin, Şekil 2.3’te gösterilen web uygulamaları için referans mimari, Katmanlar desenini içerir, ancak aynı zamanda kaç katmanın kullanılması gerektiğini de belirler. Bu referans mimarisi ayrıca Uygulama Cephe (Application Facade) ve Veri Erişim Bileşenleri (Data Access Components) gibi diğer desenleri de içerir.

## 2.5.3 Dağıtım Desenleri (Deployment Patterns)

Ayrı olarak ele almayı tercih ettiğimiz bir diğer desen türü dağıtım desenleridir (deployment patterns). Bu desenler, sistemi fiziksel olarak nasıl yapılandırıp dağıtacağımıza (deploy) dair modeller sağlar. Şekil 2.6’da gösterilen desen gibi bazı dağıtım desenleri, sistemi katmanlar (tiers; fiziksel düğümler) açısından ele alarak ilk fiziksel yapıyı kurmak için yararlıdır. Şekil 2.7’deki Yük Dengelemeli Küme (Load-Balanced Cluster) gibi daha uzmanlaşmış dağıtım desenleri ise, erişilebilirlik (availability), performans ve güvenlik gibi kalite niteliklerini sağlamak için kullanılır.

![Şekil 2.6](/home/runner/workspace/scripts/dsa_figs/sekil_2_6.png){width=11.85cm}


![Şekil 2.7](/home/runner/workspace/scripts/dsa_figs/sekil_2_7.png){width=11.85cm}


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

![Şekil 2.8](/home/runner/workspace/scripts/dsa_figs/sekil_2_8.png){width=11.85cm}


Taktikler (tactics), bir kalite niteliği (quality attribute) tepkisinin kontrolünü etkileyen tasarım kararlarıdır. Örneğin, düşük gecikmeye (latency) veya yüksek işlem hacmine (throughput) sahip bir sistem tasarlamak istiyorsanız, olayların (hizmet isteklerinin) gelişini düzenleyecek bir dizi tasarım kararı alabilirsiniz; bunun sonucu olarak, Şekil 2.8’de gösterildiği gibi belirli zaman kısıtları içinde üretilen tepkiler elde edersiniz.

Taktikler desenlerden (pattern) hem daha basit hem de daha ilkel (primitive) yapıdadır. Tek bir kalite niteliği tepkisinin kontrolüne odaklanırlar (elbette bu tepkiyi diğer kalite niteliği hedefleriyle değiştokuş edebilirler). Desenler ise buna karşılık, tipik olarak birden çok kuvveti—yani birden çok kalite niteliği hedefini—çözmeye ve dengelemeye odaklanır. Bir benzetmeyle, bir taktiğin atom, bir desenin ise molekül olduğunu söyleyebiliriz.

Taktikler, tasarım hakkında yukarıdan aşağıya düşünmeyi sağlayan bir yol sunar. Bir taktik sınıflandırması, bir kalite niteliğinin başarılmasıyla ilişkili bir dizi tasarım hedefiyle başlar ve mimara, içinden seçim yapabileceği bir dizi seçenek sunar. Bu seçeneklerin daha sonra desenler, çerçeveler (framework) ve kodun bir bileşimiyle somutlaştırılması gerekir.

Örneğin Şekil 2.9’da performans için tasarım hedefleri “Kaynak İsteğini Kontrol Et” (“Control Resource Demand”) ve “Kaynakları Yönet” (“Manage Resources”) şeklindedir. “İyi” performansa sahip bir sistem oluşturmak isteyen bir mimarın bu seçeneklerden bir veya daha fazlasını seçmesi gerekir. Yani, mimarın kaynak isteğini kontrol etmenin mümkün olup olmadığına ve kaynakları yönetmenin mümkün olup olmadığına karar vermesi gerekir. Bazı sistemlerde, sisteme gelen olaylar bir şekilde yönetilebilir, önceliklendirilebilir veya sınırlandırılabilir. Bu mümkün değilse mimar, kabul edilebilir zaman kısıtları içinde tepkiler üretmeye çalışırken sadece kaynakları yönetebilir. “Kaynakları Yönet” kategorisi içinde mimar, kaynakları artırmayı, eşzamanlılığı (concurrency) devreye sokmayı, hesaplamaların birden çok kopyasını sürdürmeyi, verinin birden çok kopyasını sürdürmeyi vb. seçebilir. Bu taktiklerin daha sonra somutlaştırılması gerekir. Örneğin mimar, eşzamanlılığı devreye sokmak (ve yönetmek) için Yarı-Senkron/Yarı-Asenkron (Half-Sync/Half-Async) desenini (bkz. Şekil 2.5) ya da hesaplamaların birden çok kopyasını sürdürmek için Yük Dengelemeli Küme (Load-Balanced Cluster) dağıtım desenini (deployment pattern) (bkz. Şekil 2.7) seçebilir.

![Şekil 2.9](/home/runner/workspace/scripts/dsa_figs/sekil_2_9.png){width=8.64cm}


3. Bölüm’de göreceğimiz gibi, taktiklerin ve desenlerin seçimi, birleştirilmesi ve uyarlanması, ADD sürecinin (nitelik temelli tasarım, Attribute-Driven Design, ADD) temel adımlarından bazılarıdır. Kullanılabilirlik (availability), birlikte çalışabilirlik (interoperability), değiştirilebilirlik (modifiability), performans, güvenlik (security), test edilebilirlik (testability) ve kullanılabilirlik (usability) kalite nitelikleri için mevcut taktik sınıflandırmaları vardır.

## 2.5.5 Haricen Geliştirilmiş Bileşenler

Desenler ve taktikler doğaları gereği soyuttur. Ancak bir yazılım mimarisi tasarlarken bu tasarım kavramlarını somutlaştırmanız ve gerçek uygulamaya daha yakın hale getirmeniz gerekir. Bunu başarmanın iki yolu vardır: Taktiklerden ve desenlerden elde edilen elemanları kodlayabilir ya da mimarideki bu elemanlardan bir veya daha fazlasıyla teknolojileri ilişkilendirebilirsiniz. Bu “satın al mı yoksa geliştir mi” (buy versus build) seçimi, bir mimar olarak vereceğiniz en önemli kararlardan biridir.

Teknolojileri, geliştirme projesinin parçası olarak oluşturulmadıkları için haricen geliştirilen bileşenler olarak kabul ederiz. Birkaç tür haricen geliştirilen bileşen vardır:

- **Teknoloji aileleri (technology families).** Bir teknoloji ailesi, ortak işlevsel amaçlara sahip belirli teknolojilerden oluşan bir grubu temsil eder. Belirli bir ürün veya çerçeve seçilene kadar yer tutucu (placeholder) olarak hizmet edebilir. Örneğin ilişkisel veritabanı yönetim sistemi (relational database management system, RDBMS) veya nesne yönelimli–ilişkisel eşleyici (object-oriented to relational mapper, ORM). Şekil 2.10, Büyük Veri (Big Data) alanındaki farklı teknoloji ailelerini (normal metinle) göstermektedir.

![Şekil 2.10](/home/runner/workspace/scripts/dsa_figs/sekil_2_10.png){width=10.27cm}

- **Ürünler (products).** Bir ürün (veya yazılım paketi), tasarlanmakta olan sisteme entegre edilebilen ve yalnızca küçük çaplı yapılandırma veya kodlama gerektiren, bağımsız bir işlevsel yazılım parçasını ifade eder. Örneğin, Oracle veya Microsoft SQL Server gibi bir ilişkisel veritabanı yönetim sistemi bir üründür. Şekil 2.10, Büyük Veri alanındaki farklı ürünleri (italik olarak) göstermektedir.
- **Uygulama çerçeveleri (application frameworks, framework).** Bir uygulama çerçevesi (veya kısaca çerçeve, framework), tekrar eden alan ve kalite niteliği kaygılarını, geniş bir uygulama yelpazesi boyunca ele alan genel işlevsellik sağlayan ve desenler ile taktiklerden oluşturulmuş, yeniden kullanılabilir bir yazılım elemanıdır. Dikkatle seçilip doğru şekilde uygulandıklarında çerçeveler, programcıların üretkenliğini artırır. Bunu, programcıların temel iş mantığına ve son kullanıcı değerine odaklanmasını sağlayarak, alttaki teknolojilere ve bunların gerçekleştirimlerine (implementation) odaklanma gereğini azaltarak yaparlar. Ürünlerin aksine, çerçeve işlevleri genellikle uygulama kodundan çağrılır veya bir tür yönelimli yaklaşım (aspect-oriented approach) kullanılarak “enjekte edilir”. Çerçeveler genellikle XML dosyaları veya Java’daki açıklamalar (annotations) gibi diğer yaklaşımlar üzerinden kapsamlı yapılandırma gerektirir. Bir çerçeve örneği, Java’da nesne yönelimli–ilişkisel eşleme (object-oriented to relational mapping) yapmak için kullanılan Hibernate’dir. Birkaç tür çerçeve vardır: Spring gibi tam yığın (full-stack) çerçeveler genellikle başvuru mimarileriyle (reference architecture) ilişkilidir ve başvuru mimarisinin farklı elemanları boyunca genel kaygıları ele alırken, JSF gibi tam yığın olmayan çerçeveler belirli işlevsel veya kalite niteliği kaygılarını ele alır.
- **Platformlar (platforms).** Bir platform, uygulamaları geliştirmek ve çalıştırmak için tam bir altyapı sağlar. Platform örnekleri arasında Java, .Net ve Google Cloud bulunur.

Haricen geliştirilen bileşenlerin seçimi, tasarım sürecinin temel bir yönü olup, sayılarının çokluğu nedeniyle zorlayıcı bir görev olabilir. Haricen geliştirilen bileşenleri seçerken göz önünde bulundurmanız gereken birkaç ölçüt şunlardır:

- **Ele aldığı problem.** Nesne yönelimli–ilişkisel eşleme için bir çerçeve gibi belirli bir şeyi mi, yoksa bir platform gibi daha genel bir şeyi mi ele alıyor?
- **Maliyet.** Lisans maliyeti nedir ve ücretsizse, destek ve eğitim maliyeti nedir?
- **Lisans türü.** Lisans, proje hedefleriyle uyumlu mu?

## 2.5 Tasarım Kavramları: Yapılar Oluşturmak için Yapı Taşları

### Büyük Veri Analitiği Kataloğu

- Apache Flume — **Veri Toplayıcı (Data Collector)**
- Logstash  
- Fluentd  
- Apache Kafka  

- **Mesajlaşma (Messaging)**  

- **Tümleştirme (Integration)**  

- RabbitMQ — **Dağıtık Mesaj Aracısı (Distributed Message Broker)**  
- Amazon SQS  
- Apache ActiveMQ  
- StreamSets  

- **ETL/ELT**  

- Talend — **ETL/Veri Tümleştirme Motoru (ETL/Data Integration Engine)**  
- Informatica  
- HDFS  

> **💬 Çevirmen notu:** Şekildeki liste, Büyük Veri ekosistemindeki teknoloji aileleri (ör. “Messaging”) ile bu ailelere ait ürünleri (ör. RabbitMQ, Kafka, Talend) birlikte göstermektedir; metin içinde anlatılan “teknoloji ailesi vs. ürün” ayrımı burada görselleştirilmektedir.

Dağıtık Dosya Sistemi (Distributed File System)

CassandraFS  
Riak  

Anahtar-Değer (Key-Value)

Redis  
Berkeley DB  
MongoDB  

Belge Yönelimli (Document-Oriented)

CouchDB  

NoSQL Veritabanı (NoSQL Database)

HBase  

Sütun-Ailesi (Column-Family)

Veri Depolama (Data Storage)

Cassandra  
Neo4J  

Graf Yönelimli (Graph-Oriented)

OrientDB  
HP Vertica  
Teradata  

MPP Analitik İlişkisel Veritabanı (MPP Analytic RDBMS)

MS PDW  
Amazon Redshift  

Analitik İlişkisel Veritabanı (Analytic RDBMS)

MS SQL Server  

Geleneksel Analitik İlişkisel Veritabanı (Traditional Analytic RDBMS)

Oracle RDBMS  
IBM DB2  

QlikView  
Microstrategy  

BI Platformu (BI Platform)

Tableau  
Tibco JasperSoft  
Pentaho  
Splunk  

Görselleştirme ve Raporlama (Visualization & Reporting)

Etkileşimli Gösterge Paneli (Interactive Dashboard)

Kibana  
Zoomdata  
D3.js  

Grafik Kütüphanesi (Graphic Library)

GoJS  
Highcharts  
Impala  

Etkileşimli Sorgu Motoru (Interactive Query Engine)

İşleme ve Analitik (Processing and Analytics)

Apache Hive (Stinger)  
Spark SQL  

Arama ve Sorgu (Search & Query)

Splunk  
Elasticsearch  

Dağıtık Arama Motoru (Distributed Search Engine)

Apache Solr  
Hadoop MapReduce  

Dağıtık Hesaplama Motoru (Distributed Computing Engine)

Apache Spark  
Apache Tez  
Apache Storm  

İşleme (Processing)

Olay Akışı İşleyici (Event Stream Processor)

Spark Streaming  
Apache Samza  
Amazon Kinesis  
Cascading  

Açıklama (Legend):  
Düz metin – bir teknoloji ailesi  
İtalik metin – belirli bir teknoloji

Veri İşleme Çatısı (Data Processing Framework)

Apache Crunch  
Apache Hive  
Amazon Pig  

ŞEKİL 2.10 Büyük Veri (Big Data) uygulama alanı için bir teknoloji aile ağacı

---

38. Bölüm 2—Mimari Tasarım

- **Destek (Support).** İyi destekleniyor mu? Teknoloji hakkında kapsamlı dokümantasyon var mı? Danışabileceğiniz geniş bir kullanıcı veya geliştirici topluluğu mevcut mu?
- **Öğrenme eğrisi (Learning curve).** Bu teknolojiyi öğrenmek ne kadar zor? Kuruluşunuzda bu teknolojide uzmanlaşmış kişiler var mı? Uygun eğitimler mevcut mu?
- **Olgunluk (Maturity).** Piyasaya yeni çıkmış, heyecan verici ama görece kararsız veya yeterince desteklenmeyen bir teknoloji mi?
- **Popülerlik (Popularity).** Görece yaygın bir teknoloji mi? Olumlu referanslar veya olgun kuruluşlarca benimsenmesi söz konusu mu? Bu teknolojiyi derinlemesine bilen kişileri işe almak kolay olacak mı? Etkin bir geliştirici topluluğu veya kullanıcı grubu var mı?
- **Uyumluluk ve entegrasyon kolaylığı (Compatibility and ease of integration).** Projede kullanılan diğer teknolojilerle uyumlu mu? Projeye kolayca entegre edilebilir mi?
- **Kritik kalite nitelikleri (quality attributes) için destek.** Performans gibi nitelikleri kısıtlıyor mu? Güvenli ve sağlam (robust) mı?
- **Boyut (Size).** Bu teknolojinin kullanımı, geliştirilen uygulamanın boyutu üzerinde olumsuz bir etki yaratacak mı?

Ne yazık ki bu soruların yanıtları her zaman kolay bulunamaz ve belirli bir teknolojinin seçimi, biraz araştırma yapmanızı ya da en nihayetinde seçim sürecine yardımcı olacak prototipler oluşturmanızı gerektirebilir. Bu ölçütler, toplam sahip olma maliyetiniz (total cost of ownership) üzerinde önemli bir etkiye sahip olacaktır.

## 2.6 Mimari Tasarım Kararları (Architecture Design Decisions)

Bu bölümün başında söylediğimiz gibi, tasarım karar verme sürecidir. Ancak bir karar verme eylemi, tek bir an değil, bir süreçtir. Deneyimli mimarlar, bir tasarım zorluğuyla karşılaştıklarında genellikle bir “aday” kararlar kümesi (Şekil 2.1’de gösterildiği gibi) oluştururlar; bu kümeden en iyi adayı seçer ve onu somutlaştırırlar. Bu “en iyi” adayı, deneyimlerine, kısıtlara veya prototipleme ya da benzetim (simulation) gibi bir tür analiz yaklaşımına dayanarak seçebilirler. Gerçekte mimar, çoğunlukla bir seçim yapar ve “at düşünceye kadar binmeye devam eder” — yani, bir karara bağlanır ve ancak bu karar projenin başarısını tehlikeye atıyor gibi göründüğünde onu tekrar ele alır. Bu kararların ciddi sonuçları vardır!

Anımsayın ki tasarımın erken safhalarında kararlar, aşağı yönde önemli sonuçlara sahip olacak en büyük ve en kritik seçimlere odaklanır: referans mimariler, temel teknolojiler (örneğin çatı (framework)lar) ve desenler (pattern). Referans mimariler, dağıtım desenleri (deployment pattern) ve diğer tür desenler geniş ölçüde tartışılmıştır — desenler ve desen dilleri (pattern language) üretimine ve doğrulanmasına adanmış çok sayıda kitap, web sitesi ve konferans vardır. Buna karşın,

bu etkinliklerin çıktısı her zaman belgelenmiş desenler (pattern) kümesidir. Bir mimar için seçim etkinliğinin kritik bir parçası, bir desen katalogundaki desenleri yorumlamaktır. Her bir aday desen seçilmeli ve somutlaştırılması (instantiation) analiz edilmelidir. Örneğin, Şekil 2.4’teki Katmanlar (Layers) desenini seçtiyseniz, hâlâ birçok karar vermeniz gerekir: kaç katman olacağı, katmanlamanın ne kadar sıkı (strict) olacağı, hangi belirli hizmetlerin (service) her bir katmana yerleştirileceği, bu işlevler arasındaki arayüzlerin ne olacağı ve benzeri. Şekil 2.7’deki Yük Dengelemeli Küme (Load-Balanced Cluster) dağıtım deseni (deployment pattern) seçildiğinde, kaç sunucunun dengeleneceğine, kaç adet yük dengeleyici (load balancer) kullanacağınıza, bu sunucuların ve yük dengeleyicilerin fiziksel olarak nerede bulunacağına, bu sunucuları hangi tür ağların bağlayacağına, bu ağ bağlantıları üzerinde hangi tür şifreleme (encryption) kullanacağınıza, yük dengeleyicilerin hangi tür sağlık izleme (health monitoring) mekanizmasını uygulayacağına ve benzeri ayrıntılara karar vermeniz gerekir. Bu kararlar önemlidir ve desenin somutlaştırılmış hâlinin başarısını etkileyecektir; bu yüzden analiz edilmeleri gerekir. Ayrıca, bu kararların uygulanmasının (implementation) kalitesi de desenin başarısını etkileyecektir. Bizim sıkça şaka yollu söylediğimiz gibi: mimari verir, uygulama geri alır.

Ayrıca, tasarım kavramlarını sunan pek çok katalog ve web sayfası farklı gelenekler ve gösterimler (notation) kullanır. Bu kitabın odağı, tasarım yöntemi ve bu yöntemin bu harici kaynaklarla nasıl kullanılabileceğidir. Bu nedenle, dış kaynaklardan sadece örnekler alıyor ve burada, ilk sunuldukları hâlleriyle gösteriyoruz. Bu kitap, başka bir tasarım desenleri (design patterns) kataloğu olarak tasarlanmamıştır — sizi bu katalogların varlığından haberdar etmek ve bir mimar için nasıl olağanüstü yararlı kaynaklar olabileceklerini, ancak dikkatle yorumlanıp kullanılmaları gerektiğini göstermek istiyoruz. Aslında, bir mimar olarak birçok işinizden biri, bu katalogları, onların farklı gösterim ve gelenekleriyle birlikte anlamak ve yorumlamaktır. Karşı karşıya kalacağınız gerçeklik budur.

Son olarak, bir tasarım kararı verildikten sonra, bunu nasıl belgeleyeceğinizi düşünmelisiniz. Elbette, hiçbir dokümantasyon yapmayabilirsiniz. Nitekim, uygulamada en yaygın olan budur. Mimari kavramlar genellikle muğlaktır ve “kabile bilgisi” (tribal knowledge) içinde, gayriresmî yollarla iletilir: kişisel iletişimler, e-postalar, adlandırma kuralları ve benzeri. Alternatif olarak, güvenlik açısından kritik (safety-critical) ya da yüksek güvenlikli (high-security) sistemler gibi, talepkâr kalite niteliği (quality attribute) gereksinimleri olan bazı projelerde yapıldığı gibi, tam ve resmî dokümantasyon yaratabilir ve bunu sürdürebilirsiniz. Eğer uçuş kontrol yazılımı tasarlıyorsanız, muhtemelen bu yelpazenin bu ucuna yakın bir yerde olacaksınız. Bu uçlar arasında çok geniş bir olasılık kümesi vardır ve bu alanda, eskizler (sketch) gibi daha az resmî (ve daha az maliyetli) mimari dokümantasyon biçimlerini görürüz (Bölüm 3.7’de tartışacağımız gibi).

Ne zaman, neyi ve nasıl belgeleyeceğinize ilişkin karar, risk temelli olmalıdır. Kendinize şu soruları sormalısınız: Bu kararı belgelemediğim takdirde risk nedir? Gelecekteki geliştiriciler tarafından yanlış yorumlanıp baltalanabilir mi? Sistemde kısa vadeli veya uzun vadeli sorunlara katkıda bulunabilir mi? Örneğin, katmanlamanın gerekçesi dikkatle belgelenmezse, katmanlama kaçınılmaz olarak bozulacak, bütünlüğünü kaybedecek ve artan bağlılığa (coupling) doğru eğilim gösterecektir. Zaman içinde bu eğilim, sistemin teknik borcunu (technical debt) artıracak ve hataları bulup düzeltmeyi veya yeni özellikler eklemeyi zorlaştıracaktır. Bir başka örnek vermek gerekirse, kritik bir kaynağın tahsisine ilişkin gerekçe belgelenmezse, bu kaynak istemeden yarışma (contention) alanı hâline gelebilir ve darboğazlara ve arızalara neden olabilir.

40 Bölüm 2—Mimari Tasarım

2.7

Özet

Bu bölümde, tasarımı, gereksinimleri ve kısıtları karşılamaya yönelik bir kararlar kümesi olarak tanıttık. Ayrıca “mimari” tasarım kavramını tanıttık ve bunun, mimari sürücülerin (architectural driver) karşılanmasına odaklanması dışında, genel tasarımdan farklı olmadığını gösterdik: amaç, birincil işlevsellik, kalite niteliği gereksinimleri, mimari kaygılar (architectural concern) ve kısıtlar. Bir kararı “mimari” yapan nedir? Bir karar, yerel olmayan (nonlocal) sonuçlara sahipse ve bu sonuçlar bir mimari sürücünün başarılmasına etki ediyorsa mimaridir.

Ayrıca mimari tasarımın neden bu kadar önemli olduğunu tartıştık: Çünkü erken, geniş kapsamlı ve değiştirilmesi zor kararların vücut bulmuş hâlidir. Bu kararlar, mimari sürücülerinizi karşılamanıza yardımcı olacak, projenizin iş kırılım yapısının (work-breakdown structure) büyük kısmını belirleyecek ve sistemi gerçekleştirmek için gereken araçları, becerileri ve teknolojileri etkileyecektir. Bu nedenle mimari tasarım kararları dikkatle incelenmelidir; zira sonuçları derindir. Buna ek olarak, mimari çevikliğin (agility) önemli bir kolaylaştırıcısıdır.

Mimari tasarım belirli ilkelere göre yönlendirilir. Örneğin, iyi bir modülerlik (modularity), düşük bağlılık ve yüksek içsel bütünlük (low coupling, high cohesion) elde etmek için, deneyimli bir mimar muhtemelen tasarlanan mimariye bir tür katmanlama (layering) dahil edecektir. Benzer şekilde, yüksek erişilebilirlik/erişilebilirlik oranı (high availability) elde etmek için, bir mimar muhtemelen yedeklilik (redundancy) ve devralma (failover) içeren bir desen seçecektir; örneğin etkin–pasif (active–passive) yedeklilik, burada etkin sunucu gerçek zamanlı güncellemeleri pasif sunucuya gönderir; böylece pasif sunucu, etkin sunucu arızalandığında, durum kaybı olmaksızın onun yerini alabilir.

Referans mimariler (reference architecture), dağıtım desenleri (deployment pattern), mimari desenler (architectural pattern), taktikler (tactic) ve haricen geliştirilmiş bileşenler (externally developed component) gibi tasarım kavramları, tasarımın yapı taşlarıdır ve ADD (Attribute-Driven Design, nitelik temelli tasarım) kullanılarak gerçekleştirilen mimari tasarım için temel oluştururlar. Bölüm 3’teki ADD’nin adım adım açıklamasında göreceğiniz gibi, bir mimarın verdiği en önemli tasarım kararlarının bazıları, tasarım kavramlarının nasıl seçildiği, nasıl somutlaştırıldığı ve nasıl birleştirildiğidir. Ayrıca, Ek A’da burada sunulan tasarım kavramlarının birkaç örneğini içeren bir tasarım kavramları kataloğu sunuyoruz.

Bu temellerden hareketle, bir mimari güvenle ve öngörülebilir biçimde inşa edilebilir.

2.8

Daha Fazla Okuma 41

2.8

Daha Fazla Okuma

Senaryolar ve mimari sürücüler hakkında daha derinlemesine bir anlatımı L. Bass, P. Clements ve R. Kazman’ın Software Architecture in Practice, 3. baskı, Addison-Wesley, 2012 kitabında bulabilirsiniz. Bu kitapta ayrıca, bir mimarinin kalite niteliği (quality attribute) hedeflerine ulaşmasına rehberlik etmek için yararlı olan mimari taktikler (architectural tactics) hakkında kapsamlı bir tartışma da yer almaktadır. Benzer şekilde, bu kitapta QAW (Quality Attribute Workshop) ve Fayda Ağaçları (Utility Trees) da kapsamlı biçimde tartışılmaktadır.

Mission Thread Workshop, R. Kazman, M. Gagliardi ve W. Wood, “Scaling Up Software Architecture Analysis”, Journal of Systems and Software, 85, 1511–1519, 2012; ve M. Gagliardi, W. Wood ve T. Morrow, Introduction to the Mission Thread Workshop, Software Engineering Institute Technical Report CMU/SEI-2013-TR-003, 2013 yayınlarında ele alınmaktadır.

Discovery prototyping, JRP (Joint Requirements Planning), JAD (Joint Application Design) ve hızlandırılmış sistem analizi (accelerated systems analysis) üzerine bir genel bakış, J. Whitten ve L. Bentley, Systems Analysis and Design Methods, 7. baskı, McGraw-Hill, 2007 gibi sistem analizi ve tasarımı üzerine yetkin herhangi bir kitapta bulunabilir. Mimari yaklaşımların Çevik (Agile) yöntemlerle birleşimi 9. bölümde tartışılacaktır.

Bir referans mimarileri (reference architectures) ve dağıtım desenleri (deployment patterns) kataloğu, Microsoft Patterns and Practices Team’in kitabında sunulmuştur: Microsoft® Application Architecture Guide, 2. baskı, Microsoft Press, 2009. Bu kitap ayrıca belgelenen referans mimarilerle ilişkilendirilmiş mimari kaygıların (architectural concerns) kapsamlı bir listesini sunmaktadır.

Dağıtık sistemlerin inşası için mimari tasarım desenlerinin (architectural design patterns) kapsamlı bir koleksiyonu, F. Buschmann, K. Henney ve D. Schmidt, Pattern-Oriented Software Architecture Volume 4: A Pattern Language for Distributed Computing, Wiley, 2007 kitabında bulunabilir. POSA (Patterns Of Software Architecture) serisindeki diğer kitaplar ek desen katalogları sağlamaktadır. Belirli uygulama alanları ve teknolojilerde uzmanlaşmış daha birçok desen kataloğu mevcuttur. Bunlardan birkaç örnek aşağıda listelenmiştir:

- E. Gamma, R. Helm, R. Johnson ve J. Vlissides. Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley, 1995.
- M. Fowler. Patterns of Enterprise Application Architecture. Addison-Wesley, 2003.
- E. Fernandez-Buglioni. Security Patterns in Practice: Designing Secure Architectures Using Software Patterns. Wiley, 2013.
- G. Hohpe ve B. Woolf. Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions. Addison-Wesley, 2004.

Yazılım paketlerinin değerlendirilmesi ve seçimi, A. Jadhav ve R. Sonar, “Evaluating and Selecting Software Packages: A Review”, Journal of Information and Software Technology, 51, 555–563, 2009 makalesinde tartışılmaktadır.

The “bible” for software architecture documentation is P. Clements,
F. Bachmann, L. Bass, D. Garlan, J. Ivers, R. Little, P. Merson, R. Nord, and
J. Stafford, Documenting Software Architectures: Views and Beyond, 2nd ed.,
Addison-Wesley, 2011.
The technology family tree for the Big Data application domain is based on the
Smart Decisions Game by H. Cervantes, S. Haziyev, O. Hrytsay, and R. Kazman,
which can be found at http://smartdecisionsgame.com.

> **💬 Çevirmen notu:** Bu paragraftaki “bible” ifadesi, yazılım mimarisi dokümantasyonu için temel başvuru kaynağı anlamında mecazi olarak kullanılmıştır; sonraki cümleler henüz çevrilmemiş başka bir sayfaya ait, fakat kurallar gereği ilgili olmayan sayfa kırılımı (“42 Chapter 2—Architectural Design”) atılmıştır.

---

# 3  
Mimari Tasarım Süreci

Bu bölümde, bu kitabın odaklandığı tasarım yöntemi olan ADD (Attribute-Driven Design, nitelik temelli tasarım) hakkında ayrıntılı bir tartışma sunuyoruz. Yöntemin genel bir bakışı ve her bir adımının üzerinden geçerek başlıyoruz. Bu genel bakışı, bu adımları gerçekleştirirken dikkate alınması gereken farklı yönlerin daha ayrıntılı tartışmaları izlemektedir. Hangi tür sistem tasarlanıyorsa, farklı türdeki tasarım kavramlarının ne zaman kullanılabileceği konusunda rehberlik sağlayan çeşitli yol haritaları öneriyoruz. Ayrıca tasarım kavramlarının tanımlanması ve seçilmesini, bu tasarım kavramlarından yapılar üretilmesini, arayüzlerin tanımlanmasını, ön dokümantasyonun üretilmesini ve son olarak da tasarım ilerlemesini izlemek için bir tekniği tartışıyoruz.

## 3.1 İlkelere Dayalı Bir Yönteme Duyulan İhtiyaç

2. bölümde tasarımla ilişkili çeşitli kavramları tartıştık. Soru şudur: Tasarımı gerçekte nasıl gerçekleştirirsiniz? Sürücülerin (drivers) karşılandığından emin olacak şekilde tasarım yapmak, ilkelere dayalı (principled) bir yöntem gerektirir. Burada “ilkelere dayalı” derken, yeterli bir tasarım üretmek için gerekli olan tüm ilgili yönleri dikkate alan bir yönteme atıfta bulunuyoruz. Böyle bir yöntem, sürücülerinizin karşılandığını garanti etmek için gerekli olan rehberliği sağlar. Bu amaca maliyet etkin ve tekrarlanabilir bir şekilde ulaşmak için, yeniden kullanılabilir tasarım kavramlarını birleştirmenize ve içselleştirmenize rehberlik eden bir yönteme ihtiyaç duyarsınız.

Tasarımın yeterli biçimde gerçekleştirilmesi önemlidir; çünkü mimari tasarım kararları, bir projenin yaşam döngüsünün farklı noktalarında önemli sonuçlara sahiptir. Örneğin, bir ön satış (pre-sales) aşamasında, uygun bir tasarım maliyet, kapsam ve zaman çizelgesinin daha iyi tahmin edilmesine imkân tanır. Geliştirme sırasında, uygun bir tasarım daha sonraki yeniden işleri (rework) önlemeye yardımcı olur ve geliştirme ile dağıtımı (deployment) kolaylaştırır. Son olarak, mimari tasarımın neyi içerdiğinin net biçimde anlaşılması, teknik borcun (technical debt) çeşitli yönlerini daha iyi yönetmek için gereklidir.

## 3.2 Nitelik Temelli Tasarım (Attribute-Driven Design, ADD) 3.0

Mimari tasarım, bir yazılım projesinin geliştirilmesi boyunca bir dizi tur halinde gerçekleştirilir. Her tasarım turu, bir sprint gibi bir proje artışı (increment) içinde yer alabilir. Bu turların içinde, bir dizi tasarım yinelemesi (design iteration) gerçekleştirilir. ADD yönteminin belki de en önemli özelliği, tasarım yinelemeleri içinde gerçekleştirilmesi gereken görevlere ilişkin ayrıntılı, adım adım rehberlik sağlamasıdır (diğer tasarım yöntemleriyle karşılaştırma için bkz. 7. bölüm). ADD ortaya çıktığında, özellikle kalite niteliklerine odaklanan ve bu niteliklerin farklı türde yapılar seçilerek ve bunların görünümler (views) aracılığıyla temsil edilmesi yoluyla başarılmasına odaklanan ilk yöntemdi. ADD’nin bir diğer önemli katkısı, analiz ve dokümantasyonun tasarım sürecinin ayrılmaz bir parçası olduğunu kabul etmesiydi. ADD yazılım mimarisi alanına önemli ve büyük bir katkı olmasına rağmen, 1.4. bölümde tartışıldığı gibi, uygulayıcı topluluk tarafından benimsenmesinin birtakım içsel zayıflıklar nedeniyle sınırlı kaldığına inanıyoruz.

ADD, 15 yıldan daha uzun süredir başarıyla kullanılmaktadır. Ancak yazılım dünyası, ADD’nin ilk ortaya çıkışından bu yana ve daha da önemlisi 2.0 sürümünün 2006’da yayımlanmasından bu yana dramatik biçimde değişmiştir. Bu nedenle ve 2.0 sürümünün zayıflıklarını gidermek için ADD 3.0’ı oluşturmayı kararlaştırdık. Bundan böyle, bu yönteme kısaca ADD diyeceğiz. Şekil 3.1, ADD ile ilişkili adımları ve artefaktları göstermektedir ve sonraki alt bölümlerde her bir adımın içindeki etkinliklere genel bir bakış sunuyoruz.

![Şekil 3.1](/home/runner/workspace/scripts/dsa_figs/sekil_3_1.png){width=11.75cm}


### 3.2.1 Adım 1: Girdileri Gözden Geçir

Tasarım turuna başlamadan önce, tasarım sürecinin girdilerinin mevcut ve doğru olduğundan emin olmanız gerekir. Öncelikle, yapılacak tasarım faaliyetlerinin amacının ne olduğu konusunda net olmalısınız. Amaç, örneğin, erken tahmin için bir tasarım üretmek, mevcut bir tasarımı sistemin yeni bir artışını (increment) inşa etmek üzere ayrıntılandırmak ya da belirli teknik riskleri azaltmak için bir prototip tasarlayıp üretmek olabilir (tasarım amacına ilişkin tartışma için Bölüm 2.4.1’e bakınız). Ayrıca, tasarım faaliyeti için gereken diğer sürücülerin (driver) de hazır olduğundan emin olmanız gerekir. Bunlar; birincil işlevsel gereksinimler, kalite niteliği senaryoları (quality attribute scenarios), mimari kısıtlar (architectural constraints) ve kaygılardır (concerns). Son olarak, bu ilk tasarım turu değilse veya bu bir “yeşil alan (greenfield)” geliştirme değilse, dikkate almanız gereken ek bir girdi de mevcut mimari tasarımdır.

Bu noktada, birincil işlevsellik ve kalite niteliği senaryolarının, ideal olarak en önemli proje paydaşlarınız (stakeholder) tarafından önceliklendirildiğini varsayıyoruz. (Eğer böyle değilse, bunları ortaya çıkarmak ve önceliklendirmek için kullanabileceğiniz teknikler vardır; Bölüm 2.4.2 ve 2.4.3’te tartışılmıştır.) Mimar olarak siz, artık bu sürücülerin “sahibi” olmalısınız. Örneğin, özgün gereksinim çıkarımı (requirements elicitation) sürecinde önemli paydaşlardan herhangi birinin gözden kaçıp kaçmadığını veya önceliklendirme yapıldığından beri iş koşullarında bir değişiklik olup olmadığını kontrol etmeniz gerekir. Bu sürücüler gerçekten de tasarımı “sürükler” (drive), dolayısıyla onların doğru olması ve önceliklerinin doğru belirlenmesi kritiktir. Bu noktayı yeterince vurgulayamıyoruz. Yazılım mimarisi tasarımı, yazılım mühendisliğindeki çoğu etkinlik gibi, “çöp girerse çöp çıkar (garbage in, garbage out)” sürecidir. Girdiler kötü biçimlendirilmişse, ADD (Attribute-Driven Design) sonuçları iyi olamaz.

Kaba bir kural olarak, tasarım amacına, kısıtlara ve başlangıçtaki mimari kaygılara ek olarak, birincil kullanım senaryolarını (use case) ve en önemli kalite niteliği senaryolarını belirlediyseniz tasarıma başlayabilmelisiniz. Elbette bu, yalnızca bu sürücüler hakkında kararlar alacağınız anlamına gelmez: Diğer kalite niteliği senaryolarını, kullanım senaryolarını ve mimari kaygıları da ele almanız gerekecektir, ancak bunlar daha sonra ele alınabilir.

Sürücüler, farklı tasarım yinelemelerini (iteration) yürütmek için kullanmanız gereken bir mimari tasarım birikim listesi (architectural design backlog) haline gelir. Bu fikri Bölüm 3.8.1’de daha ayrıntılı tartışıyoruz.

## 3.2.2 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bir tasarım turu (design round), yinelemeli bir geliştirme modeli kullanılıyorsa bir geliştirme döngüsü içinde gerçekleştirilen mimari tasarım faaliyetlerini, şelale (waterfall) modeli kullanılıyorsa mimari tasarım faaliyetlerinin tamamını temsil eder. Bir veya daha fazla tur boyunca, belirlenen tasarım amacına uygun bir mimari üretirsiniz.

Bir tasarım turu genellikle, her bir yinelemenin belirli bir hedefe odaklandığı bir dizi tasarım yinelemesi şeklinde yürütülür. Böyle bir hedef tipik olarak, sürücülerin bir alt kümesini tatmin edecek şekilde tasarım yapmayı içerir. Örneğin, bir yineleme hedefi, belirli bir performans senaryosunu destekleyecek öğelerden (element) yapılar (structure) oluşturmak ya da belirli bir kullanım senaryosunun gerçekleştirilmesini mümkün kılmak olabilir. Bu nedenle, tasarım yaparken belirli bir tasarım yinelemesine başlamadan önce bir hedef belirlemeniz gerekir.

Bölüm 3.3’te tartışacağımız üzere, mimarisini tasarladığınız sistemin türüne bağlı olarak ele alınması gereken yineleme hedefleri için “en iyi” —ya da en azından güçlü biçimde önerilen— bir sıralama olabilir. Örneğin, olgun bir alanda (mature domain) yer alan bir yeşil alan (greenfield) sistem için başlangıç hedefiniz genellikle bir referans mimari seçerek sistem için genel bir yapı (overall structure) belirlemektir.

## 3.2.3 Adım 3: Ayrıntılandırmak Üzere Sistemden Bir veya Daha Fazla Öğe Seçme

Sürücüleri tatmin etmek, bir veya daha fazla mimari yapı üretmenizi gerektirir. Bu yapılar, birbiriyle ilişkili öğelerden oluşur ve bu öğeler genellikle önceki bir yinelemede tanımladığınız diğer öğelerin ayrıntılandırılması (refinement) yoluyla elde edilir. Ayrıntılandırma, daha ince taneli (fine-grained) öğelere ayrıştırma (üstten aşağı, top-down yaklaşım), öğeleri daha kaba taneli (coarse-grained) öğelerde birleştirme (alttan yukarı, bottom-up yaklaşım) veya daha önce tanımlanmış öğelerin iyileştirilmesi anlamına gelebilir. Yeşil alan geliştirme için sistem bağlamını (system context) belirleyerek başlayabilir ve ardından ayrıştırma yoluyla ayrıntılandırmak üzere mevcut tek öğeyi —yani sistemin kendisini— seçebilirsiniz. Mevcut sistemler için veya yeşil alan sistemlerdeki daha sonraki tasarım yinelemelerinde, genellikle önceki yinelemelerde tanımlanmış öğeleri ayrıntılandırmayı seçersiniz.

Seçeceğiniz elemanlar, belirli sürücülerin (driver) karşılanmasına dâhil olan elemanlar olacaktır. Bu nedenle, tasarım mevcut bir sistem için yürütülüyorsa, sistemin fiilen inşa edilmiş mimarisinin (as-built architecture) bir parçası olan elemanları iyi anlamanız gerekir. Bu, bir miktar “dedektiflik”, tersine mühendislik (reverse engineering) veya geliştiricilerle görüşmeler yapmayı gerektirebilir.

Adım 2 ve 3’ü, yöntemde göründükleri sırayla sunduk; yani adım 2, adım 3’ten önce gelir. Ancak, bazı durumlarda bu sırayı tersine çevirmeniz gerekebilir. Örneğin, sıfırdan (greenfield) bir sistem tasarlarken veya belirli türde referans mimarileri (reference architectures) ayrıntılandırırken (Bölüm 5’te göstereceğimiz gibi), en azından tasarımın erken aşamalarında sistemin elemanlarına odaklanır, yinelemeye belirli bir elemanı seçerek başlar ve ardından ele almak istediğiniz sürücüleri göz önünde bulundurursunuz.

## 3.2.4 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı (design concept) Seç

Tasarım kavramlarını (design concepts) seçmek, muhtemelen tasarım sürecinde karşılaşacağınız en zor karardır; çünkü yineleme hedefinize ulaşmak için kullanılabilecek tasarım kavramları arasından alternatifleri belirlemenizi ve bu alternatifler arasından seçim yapmanızı gerektirir. Bölüm 2.5’te gördüğümüz gibi, farklı türde tasarım kavramları vardır ve her tür için birçok seçenek bulunabilir. Bu, bir seçim yapmak için analiz edilmesi gereken hatırı sayılır sayıda alternatif ortaya çıkarabilir. Bölüm 3.4’te tasarım kavramlarının belirlenmesini ve seçilmesini daha ayrıntılı olarak ele alıyoruz.

## 3.2.5 Adım 5: Mimari Elemanları Örnekle, Sorumlulukları Tahsis Et ve Arayüzleri Tanımla

Bir veya daha fazla tasarım kavramını seçtikten sonra, seçtiğiniz tasarım kavramlarından elemanları örneklemeyi (instantiate) içeren başka bir tasarım kararı vermelisiniz. Örneğin, bir tasarım kavramı olarak Katmanlar deseni (Layers pattern) seçtiyseniz, desenin kendisi belirli bir sayıyı dayatmadığından, kaç katman kullanılacağına karar vermeniz gerekir. Bu örnekte, katmanlar örneklenen elemanlardır. Bazı durumlarda, örnekleme yapılandırma (configuration) anlamına gelebilir. Örneğin, bir yinelemeyi teknolojileri seçmeye ve bunları tasarımınızdaki elemanlarla ilişkilendirmeye ayırmış olabilirsiniz. Sonraki yinelemelerde, bu elemanları, belirli bir sürücüyü —örneğin bir kalite niteliğini (quality attribute)— desteklemek için nasıl yapılandırılmaları gerektiğine dair daha ince taneli kararlar vererek iyileştirebilirsiniz.

Elemanları örnekledikten sonra, her birine sorumluluklar tahsis etmeniz gerekir. Örneğin, tipik bir web tabanlı kurumsal sistemde, genellikle en az üç katman bulunur: sunum (presentation) katmanı, iş (business) katmanı ve veri (data) katmanı. Bu katmanların sorumlulukları farklıdır: Sunum katmanının sorumlulukları tüm kullanıcı etkileşimlerini yönetmeyi içerirken, veri katmanının sorumlulukları verinin kalıcılığını (persistence) yönetmeyi içerir.

Elemanları örneklemek, bir sürücüyü veya kaygıyı (concern) karşılayan yapılar oluşturmak için gerçekleştirmeniz gereken görevlerden yalnızca biridir. Örneklenmiş elemanların, birbirleriyle iş birliği yapmalarını sağlamak için ayrıca bağlanmaları gerekir. Bu da elemanlar arasında ilişkilerin bulunmasını ve bir tür arayüz (interface) aracılığıyla bilgi alışverişini gerektirir. Arayüz, elemanlar arasında bilginin nasıl akması gerektiğinin sözleşmeye dayalı bir belirtimidir. Bölüm 3.5, farklı türde tasarım kavramlarının nasıl örneklendiği ve yapıların nasıl oluşturulduğu hakkında daha fazla ayrıntı sağlar ve Bölüm 3.6, arayüzlerin nasıl tanımlanabileceğini tartışır.

## 3.2.6 Adım 6: Görünümleri (views) Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Bu noktada, yineleme için tasarım faaliyetlerini tamamlamış durumdasınız. Bununla birlikte, oluşturduğunuz yapıların temsilleri olan görünümlerin korunmasını sağlamak için herhangi bir eylemde bulunmamış olabilirsiniz. Örneğin, bir önceki adımı bir toplantı odasında gerçekleştirdiyseniz, muhtemelen bir beyaz tahta üzerinde bir dizi diyagramla kalmışsınızdır. Bu bilgiler kritiktir ve daha sonra analiz edebilmek ve diğer paydaşlara (stakeholder) iletebilmek için bunları yakalamanız gerekir.

Oluşturduğunuz görünümler hemen hemen kesinlikle eksiktir, bu nedenle bu diyagramların sonraki bir yinelemede yeniden gözden geçirilmesi ve iyileştirilmesi gerekebilir. Bu tipik olarak, ek sürücüleri desteklemek için vereceğiniz diğer tasarım kararlarından doğan elemanları barındırmak amacıyla yapılır. Bu neden, ADD’de (nitelik temelli tasarım, Attribute-Driven Design) görünümleri “taslak olarak çizmekten” söz etmemizi açıklar; yani, ön taslak niteliğinde bir dokümantasyon oluşturmak. Bu görünümlerin daha resmi, daha ayrıntılı dokümantasyonu —üretmeyi seçerseniz— ancak bir dizi tasarım yinelemesi tamamlandıktan sonra gerçekleştirilir (Bölüm 1.2.2’de tartışılan mimari dokümantasyon etkinliğinin bir parçası olarak).

Görünümlerin taslaklarını saklamaya ek olarak, tasarım yinelemesi sırasında alınan önemli kararları ve bu kararlara yol açan nedenleri (yani gerekçeyi, rationale) kaydetmelisiniz; böylece bu kararların daha sonra analizini ve anlaşılmasını kolaylaştırırsınız. Örneğin, önemli ödünleşimlere (tradeoff) ilişkin kararlar bu noktada kaydedilebilir. Bir tasarım yinelemesi sırasında kararlar esas olarak adım 4 ve 5’te verilir. Bölüm 3.7, tasarım sırasında, taslaklar oluşturmayı, tasarım kararlarını ve bunların gerekçelerini kaydetmeyi de kapsayacak şekilde, nasıl ön dokümantasyon yaratılacağına dair daha fazla bilgi sunar.

## 3.2.7 Adım 7: Mevcut Tasarımın Analizini Yap ve Yineleme Hedefini ile Tasarım Amacının Gerçekleşmesini Gözden Geçir

Adım 7’ye geldiğinizde, yineleme için belirlenmiş hedefi ele alan kısmi bir tasarım oluşturmuş olmalısınız. Gerçekten de durumun böyle olduğundan emin olmak iyi bir fikirdir; böylece memnuniyetsiz paydaşlardan ve sonraki yeniden işlerden kaçınırsınız. Analizi, kaydettiğiniz görünüm taslaklarını ve tasarım kararlarını gözden geçirerek kendiniz gerçekleştirebilirsiniz; ancak, bundan da iyisi, bir başkasından tasarımı gözden geçirmesinde size yardımcı olmasını istemektir. Bunu, kuruluşların sıklıkla ayrı bir test/kalite güvence (quality assurance) grubu bulundurmasının aynı nedeniyle yaparız: Başka bir kişi sizin varsayımlarınızı paylaşmayacak ve farklı bir deneyim tabanına ve farklı bir bakış açısına sahip olacaktır. Farklı bir bakış açısına sahip birini sürece dâhil etmek, hem kodda hem de mimaride “hata”ları bulmanıza yardımcı olabilir. Analizi Bölüm 8’de daha derinlemesine tartışıyoruz.

Yineleme sırasında gerçekleştirilen tasarım analiz edildikten sonra, mimarinizin durumunu, belirlenmiş tasarım amacı açısından gözden geçirmelisiniz. Bu, bu noktada, tasarım turu (design round) ile ilişkili sürücüleri tatmin edecek kadar tasarım yinelemesi yapıp yapmadığınızı ve tasarım amacına ulaşılıp ulaşılmadığını ya da gelecekteki proje artımlarında ek tasarım turlarına ihtiyaç olup olmadığını değerlendirmek anlamına gelir. Bölüm 3.8, tasarım ilerlemesini izlemenizi sağlayacak basit teknikleri açıklar.

## 3.2.8 Gerekirse Yinele

> **💬 Çevirmen notu:** “Design round” burada, belirli bir sürücü kümesini hedefleyen, birden çok tasarım yinelemesinden oluşan daha geniş bir tasarım çevrimini ifade eder; tek bir “iteration”dan daha kapsayıcı bir zaman dilimini ima eder.

İdeal olarak, girdinin parçası olarak ele alınan her bir sürücü (driver) için ek yinelemeler yapmalı ve 2’den 7’ye kadar olan adımları tekrar etmelisiniz. Çoğu zaman, zaman ya da kaynak kısıtları nedeniyle bu tür yinelemeleri yapmak mümkün olmaz; bu kısıtlar sizi tasarım faaliyetlerini durdurmaya ve geliştirme sürecindeki bir sonraki faaliyete —tipik olarak gerçekleştirim (implementation)— geçmeye zorlar.

Daha fazla tasarım yinelemesine gerek olup olmadığını değerlendirmek için ölçütler nelerdir? Burada risk bize rehberlik eder. En azından en yüksek önceliğe sahip sürücüleri ele almış olmalısınız. İdeal olarak, kritik sürücülerin sağlandığından veya en azından tasarımın bu sürücüleri karşılayacak kadar “yeterince iyi” olduğundan emin olmalısınız. Son olarak, yinelemeli geliştirme (iterative development) yaparken, her proje yinelemesinde bir tasarım turu yapmayı seçebilirsiniz. İlk turlar sürücüleri ele almaya odaklanmalı, daha sonraki turlar ise sürücü olarak seçilmemiş, fakat yine de ele alınması gereken diğer gereksinimler için tasarım kararları vermeye odaklanmalıdır.

## 3.3 Sistem Tipine Göre Bir Tasarım Yol Haritasını İzlemek

Yazı yazarken, çoğu kişinin korkulu rüyası olan “boş sayfa korkusunu” yaşamış olabilirsiniz. Benzer şekilde, bir mimari tasarlamaya başladığınızda kendinize “Tasarım yapmaya nasıl başlarım?” diye sorduğunuz bir durumla karşı karşıya kalabilirsiniz. Bu soruyu yanıtlayabilmek için hangi tip bir sistem tasarladığınızı göz önünde bulundurmanız gerekir.

Yazılım sistemlerinin tasarımı üç geniş kategoriye ayrılır: (1) olgun (yani iyi bilinen) bir alan (domain) için bir sıfırdan geliştirme (greenfield) sisteminin tasarımı; (2) yeni (yani daha az yerleşik bir altyapıya ve bilgi tabanına sahip) bir alan için bir sıfırdan geliştirme sisteminin tasarımı; ve (3) mevcut bir sistemde değişiklik yapmak için tasarım (brownfield). Bu kategorilerin her biri, tasarım yinelemeleri boyunca yerine getirmeniz gereken hedeflerin sıralanışı bakımından farklı bir yol haritası içerir.

### 3.3.1 Olgun Alanlar için Greenfield Sistemlerin Tasarımı

Olgun bir alan için bir greenfield sistemin tasarımı, “sıfırdan” geliştirilen bir sistem için mimari tasarladığınızda ve bu tür sistemin iyi bilindiği ve anlaşıldığı durumlarda ortaya çıkar; yani, araçlar ve teknolojilerden oluşan yerleşik bir altyapı ve buna bağlı bir bilgi tabanı olduğunda. Olgun alanlara örnekler şunlardır:

- Geleneksel masaüstü uygulamaları
- Bir mobil cihazda çalışan etkileşimli uygulamalar
- Bir web tarayıcısı üzerinden erişilen, bilgiyi ilişkisel bir veritabanında saklayan ve iş süreçlerini kısmen ya da tamamen otomatikleştirmeye destek veren kurumsal (enterprise) uygulamalar

Bu tür uygulamalar nispeten yaygın olduğundan, tasarımlarıyla ilişkili bazı genel mimari kaygılar iyi bilinir, iyi desteklenir ve iyi belgelenmiştir. Eğer bu kategoriye giren yeni bir sistem tasarlıyorsanız, aşağıdaki yol haritasını öneririz (Şekil 3.2’de gösterilmiştir).

![Şekil 3.2](/home/runner/workspace/scripts/dsa_figs/sekil_3_2.png){width=11.64cm}


İlk tasarım yineleme(leri)nizin hedefi, başlangıç niteliğinde bir genel sistem yapısı (overall system structure) kurma yönündeki genel mimari kaygıyı ele almak olmalıdır. Bu bir üç katmanlı istemci–sunucu uygulaması mı, eşler arası (peer-to-peer) bir uygulama mı, arka planda bir Büyük Veri (Big Data) sistemiyle bağlantı kuran bir mobil uygulama mı, vb.? Bu seçeneklerin her biri sizi farklı mimari çözümlere götürecek ve bu çözümler sürücülerinize ulaşmanıza yardımcı olacaktır. Bu yineleme hedefini gerçekleştirmek için bazı tasarım kavramları seçeceksiniz. Özellikle, genellikle bir veya daha fazla başvuru mimarisi (reference architecture) ve dağıtım deseni (deployment pattern) seçersiniz (Bkz. Bölüm 2.5.1 ve 2.5.3). Ayrıca, çerçeveler (framework) gibi dışarıda geliştirilmiş bazı bileşenleri de seçebilirsiniz. Erken yinelemelerde tipik olarak seçilen çerçeve türleri, seçilen başvuru mimarileriyle ilişkili “uçtan uca (full-stack)” çerçeveler ya da başvuru mimarisi tarafından tanımlanan elementlerle ilişkili daha özgül çerçevelerdir (Bkz. Bölüm 2.5.5). Bu ilk yinelemede, tüm sürücülerinizi gözden geçirerek tasarım kavramlarını seçmelisiniz, ancak muhtemelen kısıtlara ve belirli fonksiyonlarla ilişkilendirilmemiş, belirli başvuru mimarilerini tercih eden veya belirli dağıtım yapılandırmalarını gerektiren kalite niteliklerine (quality attribute) daha fazla dikkat edeceksiniz. Örneğin: Eğer Büyük Veri sistemleri için bir başvuru mimarisi seçerseniz, muhtemelen en önemli sürücünüz olarak yüksek veri hacimleriyle birlikte düşük gecikme süresi (low latency with high data volumes) gibi bir kalite niteliğini seçmiş olursunuz. Elbette, bu erken seçimi detaylandırmak için çok sayıda ek karar vereceksiniz; ancak bu sürücü, belirli bir başvuru mimarisinin seçilmesi gibi tasarımınız üzerinde çoktan güçlü bir etki yaratmıştır.

Bir sonraki tasarım yineleme(leri)nizin hedefi, birincil fonksiyonelliği destekleyen yapıları tanımlamak olmalıdır. Bölüm 2.4.3’te belirtildiği gibi, fonksiyonelliğin (yani kullanım senaryolarının (use case) veya kullanıcı hikâyelerinin (user story)) elementlere tahsis edilmesi, değiştirebilirlik (modifiability) ve işin takımlara dağıtılması açısından aşağı akışta kritik sonuçları olduğu için mimari tasarımın önemli bir parçasıdır. Ayrıca, fonksiyonellik tahsis edildikten sonra, onu destekleyen elementler, sonraki yinelemelerde bu fonksiyonelliklerle ilişkili kalite niteliklerini destekleyecek şekilde rafine edilebilir. Örneğin, bir performans senaryosu belirli bir kullanım senaryosu ile ilişkilendirilebilir. Performans hedefini gerçekleştirmek, bu kullanım senaryosunun başarılmasına katılan tüm elementler boyunca tasarım kararları vermeyi gerektirebilir. Fonksiyonelliği tahsis etmek için genellikle başvuru mimarisiyle ilişkilendirilmiş elementleri ayrıştırarak (decompose) rafine edersiniz. Belirli bir kullanım senaryosu, birden fazla elementin tanımlanmasını gerektirebilir. Örneğin, bir web uygulaması başvuru mimarisi seçtiyseniz, bir kullanım senaryosunu desteklemek muhtemelen modülleri tanımlamanızı gerektirecektir.

katmanlar arasında bunu yapmanız gerekir. Son olarak, bu noktada modüllerle ilişkilendirilmiş işlevselliği geliştiricilere (veya geliştirici takımlarına) tahsis etmeyi de düşünmeye başlamış olmalısınız.

Sonraki tasarım yinelemelerinizin amacı, daha önce oluşturduğunuz yapıları ayrıntılandırarak kalan sürücüleri (driver) tam olarak ele almak olmalıdır. Bu sürücüleri, özellikle de kalite niteliklerini (quality attribute) ele almak, büyük olasılıkla üç ana tasarım kavramı kategorisini—taktikler (tactic), desenler (pattern) ve çerçeveler (framework) gibi dışarıda geliştirilmiş bileşenler—ve ayrıca modülerlik, düşük bağlaşım (low coupling) ve yüksek uyumluluk (high cohesion) gibi yaygın kabul görmüş tasarım en iyi uygulamalarını kullanmanızı gerektirecektir. Örneğin, bir web uygulamasındaki arama kullanım durumu (use case) için bir performans gereksinimini (kısmen) karşılamak amacıyla “verinin birden fazla kopyasını koru (maintain multiple copies of data)” taktiğini seçebilir ve bu taktiği, veriyi kalıcılaştırmaktan sorumlu bir elemanın içinde kullanılan bir çerçevede bir önbellek (cache) yapılandırarak uygulayabilirsiniz.

Bu yol haritası başlangıç proje yinelemeleri için uygundur, fakat aynı zamanda erken proje kestirim faaliyetleri için de son derece kullanışlıdır (bkz. Bölüm 9.1.1’de satış öncesi (pre-sales) sırasında mimari tasarım sürecine ilişkin tartışma). Peki neden böyle bir yol haritası oluşturduk? Birincisi, bir mimari tasarıma başlamanın süreci her zaman karmaşıktır. İkincisi, bu yol haritasındaki adımların çoğu çoğunlukla gözden kaçırılır ya da iyi düşünülmüş, yansıtıcı bir şekilde değil de sezgisel ve ad hoc (geçici, plansız) bir biçimde yapılır. Üçüncüsü, farklı türlerde tasarım kavramları vardır ve bunların tasarımın hangi noktasında kullanılmaları gerektiği her zaman açık değildir. Bu yol haritası, en yetkin mimari organizasyonlarda gözlemlediğimiz en iyi uygulamaları kapsar. Basitçe söylemek gerekirse, bir yol haritası kullanmak, özellikle daha az olgun mimarlar için, daha iyi mimarilerle sonuçlanır.

### 3.3.2 Yeni Alanlar için Greenfield Sistemlerin Tasarımı

Yeni (novel) alanlar söz konusu olduğunda, kesin bir yol haritası oluşturmak daha zordur, çünkü başvurabileceğiniz referans mimariler (reference architecture) bulunmayabilir ve kullanabileceğiniz dışarıda geliştirilmiş bileşenler pek az, hatta hiç olmayabilir. Çoğunlukla birinci ilkelerden hareket ediyor ve kendi ev yapımı çözümlerinizi yaratıyorsunuzdur. Ancak bu durumda bile, taktikler ve desenler gibi genel amaçlı tasarım kavramları stratejik prototiplemenin desteğiyle size rehberlik edebilir. Özünde, yineleme hedefleriniz çoğunlukla daha önce oluşturulmuş yapıları sürekli rafine ederek sürücüleri bütünüyle ele almak olacaktır.

Çoğu zaman tasarım hedefiniz, karşı karşıya olduğunuz zorluklara olası çözümleri keşfedebilmek için prototipler oluşturma üzerine odaklanacaktır. Özellikle, performans, ölçeklenebilirlik veya güvenlik gibi konulara yönelik kalite niteliklerine ve tasarım zorluklarına odaklanmanız gerekebilir. Prototiplerin oluşturulmasını Bölüm 3.4.2’de tartışıyoruz.

Elbette “yeni (novel)” kavramı akışkan bir kavramdır. Mobil uygulama geliştirme 10 veya 15 yıl önce yeni bir alandı, ancak artık iyi kurulmuş bir alandır.

### 3.3.3 Mevcut Bir Sistem için Tasarım (Brownfield)

Mevcut bir sistem için mimari tasarım, farklı amaçlarla ortaya çıkabilir. En bariz olanı bakım (maintenance)—yani, yeni gereksinimleri karşılamanız veya sorunları düzeltmeniz gerektiğinde ve bunu yapmak mevcut bir sistemin mimarisinde değişiklik yapılmasını gerektirdiğinde. Ayrıca, bir sistemi yeniden düzenleme (refactoring) amacıyla da mevcut bir sistemde mimari değişiklikler yapıyor olabilirsiniz. Yeniden düzenleme yaparken, teknik borcu azaltmak, teknoloji güncellemeleri getirmek veya kalite niteliği sorunlarını çözmek (örneğin sistem çok yavaş, güvensiz veya sık sık çöküyor) için, mevcut bir sistemin mimarisini işlevlerini değiştirmeksizin değiştirirsiniz.

ADD (Attribute-Driven Design, nitelik temelli tasarım) adım 3 kapsamında tasarım sürecinin bir parçası olarak ayrıştırılacak (decompose) elemanları seçebilmek için önce mevcut sistemin mimarisinde hangi elemanların var olduğunu belirlemeniz gerekir. Bu anlamda, tasarım yinelemelerine başlamadan önceki ilk hedefiniz, sistemin mevcut mimarisini açık bir şekilde anladığınızdan emin olmak olmalıdır.

Sistemin mimarisini oluşturan elemanları, özellikleri ve ilişkileri ve mevcut kod tabanının özelliklerini anladıktan sonra, başlangıç tasarım yinelemesinden sonraki greenfield sistemler için yapılanlara benzer bir tasarım gerçekleştirebilirsiniz. Buradaki tasarım yineleme hedefleriniz, yeni işlevsellik ve kalite nitelikleri de dahil olmak üzere mimari sürücüleri tatmin edecek ve belirli mimari kaygıları ele alacak yapıları tanımlamak ve rafine etmek olacaktır. Bu tasarım yinelemeleri, büyük bir yeniden düzenleme (major refactoring) ile uğraşmıyorsanız, tipik olarak yeni bir genel sistem yapısının oluşturulmasını içermeyecektir.

Önceki tasarım bağlamları tartışmamızın oldukça soyut ve hatta belki de kafa karıştırıcı göründüğü düşünülebilir. Sonraki üç bölümde, olgun bir alandaki (Chapter 4) bir sistemin tasarımına, nispeten yeni bir alandaki (Chapter 5) bir sistemin tasarımına ve mevcut bir sistemi değiştirmeye yönelik (Chapter 6) tasarıma ilişkin örnekler sunacağız. Bu genişletilmiş örnekler, daha önce açıklanan kavramları daha açık ve somut hale getirecektir.

### 3.4 Tasarım Kavramlarını Tanımlama ve Seçme

İngiliz fizikçi Freeman Dyson bir defasında şunu söylemiştir: “İyi bir bilim insanı özgün fikirleri olan kişidir. İyi bir mühendis ise mümkün olduğunca az özgün fikirle çalışan bir tasarım yapan kişidir.” Bu alıntı, yazılım mimarisi tasarımı bağlamında özellikle anlamlıdır: Çoğu zaman tekerleği yeniden icat etmeniz gerekmez ve etmemelisiniz. Bunun yerine, temel tasarım etkinlikleriniz, tasarım yinelemeleri boyunca karşılaştığınız zorlukları ve sürücüleri ele almak için tasarım kavramlarını tanımlamak ve seçmekten ibarettir. Tasarım hâlâ özgün ve yaratıcı bir çabadır, ancak yaratıcılık, bu mevcut çözümlerin uygun şekilde tanımlanması ve daha sonra eldeki probleme uyacak biçimde birleştirilip uyarlanmasında yatar.

> **💬 Çevirmen notu:** Buradaki “tasarım kavramları”, ileride ayrıntılandırılacak olan taktikler, desenler ve dış bileşenler (framework, kütüphane vb.) gibi tekrar kullanılabilir çözüm fikirlerini kapsayan genel bir üst kavram olarak kullanılıyor.

### 3.4.1 Tasarım Kavramlarının Tanımlanması

Tasarım kavramlarının tanımlanması, mevcut çok büyük sayıdaki tasarım kavramı nedeniyle göz korkutucu görünebilir. Belirli herhangi bir konuyu ele almak için kullanabileceğiniz muhtemelen düzinelerce tasarım deseni (design pattern) ve dışarıda geliştirilmiş bileşen vardır. Durumu daha da kötüleştiren şey, bu tasarım kavramlarının popüler basın, araştırma literatürü, kitaplar ve İnternet gibi birçok farklı kaynağa dağılmış olmasıdır. Dahası, pek çok durumda bir kavramın kanonik, herkesçe kabul edilmiş bir tanımı yoktur. Örneğin farklı siteler, Broker deseni (Broker pattern) için büyük ölçüde biçimsel olmayan ve birbirinden farklı tanımlar sunacaktır. Son olarak, yinelemeye (iteration) ait tasarım hedeflerine ulaşmanıza potansiyel olarak yardımcı olabilecek alternatifleri belirledikten sonra, bunlar arasından seçim yapmanız gerekir.

Belirli bir noktada hangi tasarım kavramlarına ihtiyacınız olduğunu belirlemek için, daha önce tasarım yol haritası (design roadmap) hakkında tartıştığımız noktaları göz önünde bulundurmalısınız. Tasarım sürecinin farklı noktaları genellikle farklı türde tasarım kavramları gerektirir. Örneğin, olgun bir alanda sıfırdan (greenfield) bir sistem tasarlıyorsanız, sistemi başlangıçta yapılandırmanıza yardımcı olacak tasarım kavramı türleri başvuru mimarileri (reference architecture) ve dağıtım desenleridir (deployment pattern). Tasarım sürecinde ilerledikçe, tasarım kavramı kategorilerinin tümünü kullanacaksınız: taktikler (tactic), mimari ve tasarım desenleri (architecture and design pattern) ve dışarıda geliştirilmiş bileşenler. Unutmayın ki, belirli bir tasarım problemini ele almak için farklı türde tasarım kavramlarını bir arada kullanabilir ve çoğu zaman kullanacaksınız. Örneğin, bir güvenlik sürücüsünü (security driver) ele alırken bir güvenlik deseni (security pattern), bir güvenlik taktiği (security tactic), bir güvenlik çatısı (security framework) veya bunların bir bileşimini kullanabilirsiniz.

Kullanmak istediğiniz tasarım kavramı türleri konusunda daha net bir fikre sahip olduktan sonra bile, yine de alternatifleri —yani tasarım adaylarını— tanımlamanız gerekir. Bunu yapmanın birkaç yolu vardır; pratikte bunların tek birine değil, bir bileşimini kullanmanız olasıdır:

- **Mevcut en iyi uygulamalardan (best practice) yararlanma.** Gereken tasarım kavramları için alternatifleri, basılı veya çevrimiçi biçimde mevcut olan katalogları kullanarak belirleyebilirsiniz. Desenler (pattern) gibi bazı tasarım kavramları kapsamlı şekilde belgelenmiştir; dışarıda geliştirilmiş bileşenler gibi diğerleri ise daha az ayrıntılı biçimde belgelenmiştir. Bu yaklaşımın faydaları, çok sayıda alternatifi belirleyebilmeniz ve başkalarının önemli bilgi ve deneyimlerinden yararlanabilmenizdir. Dezavantajları ise bilgiyi aramanın ve incelemenin hatırı sayılır miktarda zaman gerektirebilmesi, belgelenmiş bilginin kalitesinin çoğu zaman bilinmemesi ve yazarların varsayımlarının ve önyargılarının bilinmemesidir.

- **Kendi bilgi ve deneyiminizden yararlanma.** Tasarladığınız sistem, geçmişte tasarladığınız diğer sistemlere benziyorsa, muhtemelen daha önce kullandığınız bazı tasarım kavramlarıyla başlamak isteyeceksiniz. Bu yaklaşımın faydası, alternatiflerin tanımlanmasının hızlı ve güvenle yapılabilmesidir. Dezavantajı, ele aldığınız tüm tasarım problemleri için en uygun olmasalar ve daha yeni, daha iyi yaklaşımlar tarafından geride bırakılmış olsalar bile, aynı fikirleri tekrar tekrar kullanmakla sonuçlanabilmenizdir. Deyimin de dediği gibi: “Küçük bir çocuğa bir çekiç verirseniz, bütün dünya ona çivi gibi görünür.”

- **Başkalarının bilgi ve deneyiminden yararlanma.** Bir mimar olarak, yıllar içinde edindiğiniz bir arka plan ve bilgi birikimine sahipsiniz. Bu temel, geçmişte ele aldıkları tasarım problemlerinin türleri farklılık gösteriyorsa, kişiden kişiye değişir. Bu bilgiden, bazı akranlarınızla beyin fırtınası (brainstorming) yoluyla tasarım kavramlarının tanımlanmasını ve seçimini birlikte gerçekleştirerek yararlanabilirsiniz.

### 3.4.2 Tasarım Kavramlarının Seçimi

Alternatif tasarım kavramlarından oluşan bir listeyi belirledikten sonra, eldeki tasarım problemini çözmek için hangisinin en uygun olduğuna karar vermeniz gerekir. Bunu görece basit bir biçimde gerçekleştirebilirsiniz: Her bir alternatifle ilişkili artıları ve eksileri listeleyen bir tablo oluşturur ve bu ölçütler ile sürücüleriniz (drivers) temelinde alternatiflerden birini seçersiniz. Tabloya, alternatifin kullanımına ilişkin maliyet gibi başka ölçütler de dahil edilebilir. Tablo 3.1, farklı başvuru mimarilerinin seçimini desteklemek için kullanılan bu tür bir tablonun örneğini göstermektedir.

Alternatifi seçmek için daha derinlemesine bir analiz yapmanız da gerekebilir. CBAM (Cost Benefit Analysis Method — maliyet fayda analiz yöntemi) veya SWOT (strengths, weaknesses, opportunities, threats — güçlü yönler, zayıf yönler, fırsatlar, tehditler) gibi yöntemler bu analizi gerçekleştirmenize yardımcı olabilir (bkz. “Maliyet Fayda Analiz Yöntemi” yan kutusu).

> **💬 Çevirmen notu:** CBAM, özellikle mimari kararların ekonomik etkisini nicel olarak karşılaştırmak için kullanılan, SEI tarafından geliştirilmiş bir yöntemdir; SWOT ise daha nitel, stratejik değerlendirme sağlar.

  
**TABLO 3.1  
Alternatiflerin Seçimini Desteklemek için Kullanılabilecek Tablo Örneği**

| Alternatifin Adı | Artılar | Eksiler | Maliyet |
| --- | --- | --- | --- |
| Web uygulama | Çeşitli platformlardan standart bir web tarayıcısı kullanılarak erişilebilir<br>Sayfalar hızlı yüklenir<br>Basit dağıtım | “Zengin” etkileşimi desteklemez | Düşük |
| Zengin İnternet uygulaması (Rich Internet application) | “Zengin” kullanıcı etkileşimini destekler<br>Basit dağıtım ve güncelleme | Daha uzun sayfa yükleme süreleri<br>İstemci tarayıcıya bir çalışma ortamının (runtime environment) kurulmasını gerektirir | Orta |
| Mobil uygulama | “Zengin” kullanıcı etkileşimini destekler | Daha az taşınabilirlik<br>Ekran sınırlamaları | Yüksek |

## Maliyet Fayda Analizi Yöntemi (Cost Benefit Analysis Method, CBAM)

CBAM, tasarım alternatiflerinin seçiminde nicel (quantitative) bir yaklaşım kullanan bir yöntemdir. Bu yöntem, mimari stratejilerin (yani tasarım kavramı kombinasyonlarının) kalite niteliği (quality attribute) tepkilerini etkilediğini ve her bir tepki düzeyinin de sistem paydaşlarına (stakeholder) fayda sağladığını, bu faydanın da yararlılık (utility) olarak adlandırıldığını varsayar. Her bir mimari strateji farklı bir yararlılık düzeyi sağlar, fakat aynı zamanda bir maliyeti vardır ve uygulanması zaman alır. CBAM’in arkasındaki fikir, yararlılık düzeyleri ve uygulama maliyetleri incelenerek, belirli mimari stratejilerin bunlara bağlı yatırım getirisi (return on investment, ROI) temelinde seçilebilmesidir. CBAM, bir ATAM’in (architecture tradeoff analysis method) ardından uygulanmak üzere tasarlanmıştır, ancak mimari değerlendirmenin yapıldığı andan önce, yani tasarım sırasında da CBAM kullanılabilir.

CBAM, girdisi olarak önceliklendirilmiş geleneksel kalite niteliği senaryoları (quality attribute scenario) kümesini alır; bu senaryolar daha sonra ek bilgilerle analiz edilir ve rafine edilir. Bu ekleme, her senaryo için birden çok tepki düzeyinin dikkate alınmasıdır:

- En kötü durum senaryosu: Sistemin çalışmak zorunda olduğu asgari eşiği temsil eder (yararlılık = 0).
- En iyi durum senaryosu: Paydaşların bundan sonra ilave yararlılık öngörmediği düzeyi temsil eder (yararlılık = 100).
- Mevcut senaryo: Sistemin halihazırda çalıştığı düzeyi temsil eder (mevcut senaryonun yararlılığı paydaşlar tarafından tahmin edilir).
- Arzulanan senaryo: Paydaşların ulaşmayı umdukları tepki düzeyini temsil eder (arzulanan senaryonun yararlılığı paydaşlar tarafından tahmin edilir).

Bu veri noktaları kullanılarak, şekilde gösterildiği gibi bir yararlılık–tepki eğrisi (utility–response curve) çizebiliriz. Farklı senaryoların her biri için yararlılık–tepki eğrisi çıkarıldıktan sonra, düşünülen çeşitli tasarım alternatifleri ele alınabilir ve bunların beklenen tepki değerleri tahmin edilebilir.

Örneğin, arızaya kadar ortalama süre (mean time to failure) ile ilgileniyorsak üç farklı mimari stratejiyi (örneğin yedeklilik (redundancy) seçeneklerini) düşünebiliriz — örneğin, yedeklilik yok, soğuk yedek (cold spare) ve sıcak yedek (hot spare). Bu stratejilerin her biri için beklenen tepkilerini (yani beklenen arızaya kadar ortalama sürelerini) tahmin edebiliriz. Burada gösterilen grafikte “e”, tahmini tepki ölçümüne göre eğri üzerinde yerleştirilmiş olan bu seçeneklerden birini temsil etmektedir.

Bu tepki tahminleri kullanılarak, her bir mimari stratejinin yararlılık değeri artık interpolasyon (ara değer hesaplama) yoluyla belirlenebilir; bu da beklenen faydasını verir. Her bir mimari stratejinin maliyetleri de ortaya çıkarılır — sıcak yedeğin en maliyetli, onu soğuk yedeğin, onun da ardından yedeklilik olmamasının izlemesi beklenir.

Tüm bu bilgiler ışığında mimari stratejiler, artık maliyete göre beklenen değerlerine dayanarak seçilebilir.

### Şekil: Yararlılık–Tepki Eğrisi

_Şekildeki açıklamalar:_

- b: best (en iyi)
- c: current (mevcut)
- d: desired (arzulanan)
- e: expected (beklenen)
- w: worst (en kötü)

Yararlılık (Utility) ekseninde 0’dan 100’e, tepki (Response) ekseninde ise 1, 2, 3 değerleri boyunca, w (en kötü), c (mevcut), d (arzulanan), b (en iyi) ve e (beklenen) noktaları bir eğri üzerinde gösterilmektedir.

CBAM ilk bakışta göreli olarak karmaşık ve zaman alıcı görünebilse de, bazı tasarım kararlarının maliyetleri, faydaları ve proje zaman çizelgesine etkileri bakımından devasa ekonomik sonuçlar doğurabileceğini göz önünde bulundurmanız gerekir. Bu kararları sadece sezgisel bir yaklaşımla mı, yoksa bu daha rasyonel ve sistematik yaklaşımla mı vereceğinize karar vermelisiniz.

Önceki analiz teknikleri sizi uygun bir seçim yapma konusunda yönlendirmediyse, deneme amaçlı (throwaway) prototipler oluşturmanız ve bunlardan ölçümler toplamanız gerekebilir. Erken aşamada deneme amaçlı prototipler oluşturmak, dışarıdan geliştirilen bileşenlerin seçiminde yardımcı olan yararlı bir tekniktir. Bu tür prototipler genellikle bakım yapılabilirlik veya yeniden kullanım çok fazla gözetilmeden, “hızlı ve biraz da özensiz” biçimde oluşturulur. Bu nedenlerle, deneme amaçlı prototiplerin daha ileri geliştirme için temel olarak kullanılmaması gerektiğini akılda tutmak önemlidir.

Prototip oluşturma, analize kıyasla maliyetli olabilir (kaynaklarımıza göre maliyet oranı 10’a 5 ila 1 arasındadır), ancak bazı senaryolar prototip oluşturmayı güçlü biçimde motive eder. Prototip oluşturup oluşturmayacağınıza karar verirken göz önüne almanız gereken hususlar şunlardır:

- Proje, ortaya çıkan (emerging) teknolojileri mi içeriyor?
- Teknoloji, şirket için yeni mi?
- Seçilen teknolojiyi kullanarak belirli sürücülerin, özellikle kalite niteliklerinin, tatmin edilmesi riskler içeriyor mu (yani tatmin edilip edilemeyeceği anlaşılmamış mı)?
- Seçilen teknolojinin proje sürücülerini tatmin etmek için faydalı olacağını belirli bir kesinlik derecesiyle gösteren, güvenilir içsel veya dışsal bilginin eksikliği var mı?
- Teknolojiyle ilişkili, test edilmesi veya anlaşılması gereken yapılandırma (configuration) seçenekleri var mı?
- Seçilen teknolojinin projede kullanılan diğer teknolojilerle bütünleştirilebileceği (integrate) belirsiz mi?

Bu soruların çoğuna cevabınız “evet” ise, deneme amaçlı bir prototip oluşturmayı ciddi biçimde düşünmelisiniz.

Tasarım kavramlarını (design concept) tanımlayıp seçerken, mimari sürücülerin (architectural driver) parçası olan kısıtları akılda tutmanız gerekir; çünkü bazı kısıtlar belirli alternatifleri seçmenizi engelleyecektir. Örneğin, bir kısıt sistemdeki tüm kütüphane ve çerçevelerin (framework) GPL lisansı kullanmamasını gerektirebilir; dolayısıyla gereksinimlerinize uygun bir çerçeve bulmuş olsanız bile, GPL lisansına sahipse onu göz ardı etmeniz gerekebilir. Ayrıca, önceki yinelemelerde tasarım kavramlarının seçimine ilişkin aldığınız kararların, uyumsuzluklar nedeniyle gelecekte seçebileceğiniz tasarım kavramlarını sınırlayabileceğini akılda tutmanız gerekir. Örneğin, ilk yinelemede kullanım için bir web uygulaması referans mimarisi (web application reference architecture) seçtiyseniz, sonraki bir yinelemede yerel uygulamalar için tasarlanmış bir kullanıcı arayüzü çerçevesini seçemezsiniz.

Son olarak, nitelik temelli tasarım (Attribute-Driven Design, ADD) süreci nasıl yürüteceğinize dair yol gösterse de, uygun tasarım kararları vereceğinizi garanti edemeyeceğini hatırlamanız gerekir. Kapsamlı akıl yürütme ve farklı alternatifleri (sadece akla ilk geleni değil) göz önünde bulundurma, iyi bir çözüm bulma olasılığını artırmanın en iyi yollarıdır. Tasarım sürecinde “analiz yapma” konusunu Bölüm 8’de tartışıyoruz.

## 3.5

Yapıların Üretilmesi

Tasarım kavramlarının (design concept) tek başına mimari sürücülerinizi (architectural driver) karşılamanıza yardımcı olması mümkün değildir; bunun için yapılar (structure) üretmeniz gerekir. Yani, seçilmiş tasarım kavramlarından türeyen elemanları (element) tanımlayıp bunları birbirine bağlamalısınız. Bu süreç, nitelik temelli tasarımda (Attribute-Driven Design, ADD) mimari elemanların somutlanmasıdır (instantiation): elemanların ve aralarındaki ilişkilerin oluşturulması ve bu elemanlarla sorumlulukların ilişkilendirilmesi.

Bir yazılım sisteminin mimarisi, üç ana kategoride gruplanabilen bir dizi yapıdan oluşur:

- **Modül yapıları (module structures):** Geliştirme zamanında var olan dosyalar, modüller ve sınıflar gibi mantıksal ve statik elemanlardan oluşur.
- **Bileşen ve bağlayıcı (component and connector, C&C) yapıları:** Çalışma zamanında var olan süreçler (process) ve iş parçacıkları (thread) gibi dinamik elemanlardan oluşur.
- **Yerleştirim yapıları (allocation structures):** Hem yazılım elemanlarını (bir modül veya C&C yapısından) hem de dosya sistemleri, donanım ve geliştirme ekipleri gibi hem geliştirme zamanında hem çalışma zamanında var olabilen yazılım-dışı elemanları içerir.

Bir tasarım kavramını somutladığınızda, aslında birden fazla yapı üretebilirsiniz. Örneğin, belirli bir iterasyonda Katmanlar desenini (Layers pattern) somutlayabilir ve bunun sonucunda bir Modül yapısı elde edebilirsiniz. Bu deseni somutlarken, katmanların sayısını, aralarındaki ilişkileri ve her bir katmanın özgül sorumluluklarını belirlemeniz gerekir.

Aynı iterasyonun bir parçası olarak, az önce tanımladığınız elemanlar tarafından bir senaryonun nasıl desteklendiğini de inceleyebilirsiniz. Örneğin, mantıksal elemanların çalışma zamanı örneklerini (instance) bir C&C yapısında oluşturabilir ve bunların mesajları nasıl değiş tokuş ettiğini modelleyebilirsiniz (bkz. Bölüm 3.6). Son olarak, her katmanın içindeki modülleri kimin uygulayacağında karar kılmak isteyebilirsiniz ki bu bir yerleştirim (allocation) kararıdır.

## 3.5.1 Elemanların Somutlanması (Instantiating Elements)

Mimari elemanların somutlanması, üzerinde çalıştığınız tasarım kavramının türüne bağlıdır:

- **Referans mimariler (reference architecture).** Referans mimariler söz konusu olduğunda, somutlama genellikle bir tür özelleştirme yaptığınız anlamına gelir. Bu çalışma kapsamında, referans mimaride tanımlanan yapının parçası olan elemanları ekler veya çıkarırsınız. Örneğin, ödemeleri yönetmek için harici bir uygulama ile iletişim kurması gereken bir web uygulaması tasarlıyorsanız, geleneksel sunum, iş (business) ve veri katmanlarına ek olarak bir entegrasyon katmanına da ihtiyaç duyarsınız.

- **Mimari ve tasarım desenleri (architectural and design patterns).** Bu desenler, elemanlardan, bunların ilişkilerinden ve sorumluluklarından oluşan genel bir yapı sağlar. Bu yapı genel (generic) olduğu için, onu kendi özgül probleminize uyarlamanız gerekir. Somutlama genellikle, desen tarafından tanımlanan genel yapının, çözdüğünüz problemin gereksinimlerine uyarlanmış belirli bir yapıya dönüştürülmesini içerir. Örneğin, Boru ve Filtreler (Pipe and Filters) mimari desenini ele alalım. Bu desen, hesaplamanın temel elemanlarını—filtreler—ve bunların ilişkilerini—borular—tanımlar, fakat probleminiz için kaç filtre kullanmanız gerektiğini ya da bu filtrelerin ilişkilerinin ne olacağını belirtmez. Bu deseni, probleminizi çözmek için kaç boru ve filtreye ihtiyaç duyulduğunu tanımlayarak, her bir filtrenin özgül sorumluluklarını belirleyerek ve topolojilerini tanımlayarak somutlarsınız.

> **💬 Çevirmen notu:** Pipe and Filters deseninde “boru” (pipe) veri akış kanalını, “filtre” (filter) ise bu akış üzerinde dönüşüm yapan işlem adımını temsil eder.

- **Dağıtım desenleri (deployment pattern).** Mimari ve tasarım desenlerinde olduğu gibi, dağıtım desenlerinin somutlanması genellikle fiziksel elemanların tanımlanmasını ve belirlenmesini içerir. Örneğin, Yük Dengelemeli Küme (Load-Balanced Cluster) desenini kullanıyorsanız, somutlama kümede yer alacak kopya (replica) sayısını, yük dengeleme algoritmasını ve kopyaların fiziksel konumunu tanımlamayı içerebilir.

- **Taktikler (tactic).** Bu tasarım kavramı belirli bir yapı dayatmaz; dolayısıyla bir taktiği somutlamak için başka tasarım kavramlarını kullanmanız gerekir. Örneğin, aktörlerin kimlik doğrulamasını yapmaya yönelik bir güvenlik taktiği seçebilir ve bunu, özel geliştirilmiş doğaçlama (ad hoc) bir çözüm yaratarak, bir güvenlik desenini kullanarak, ya da bir güvenlik çatısı (framework) gibi dışarıda geliştirilmiş bir bileşeni kullanarak somutlayabilirsiniz.

- **Dışarıda geliştirilmiş bileşenler (externally developed component).** Bu bileşenlerin somutlanması yeni elemanların yaratılmasını gerektirebilir de gerektirmeyebilir de. Örneğin, nesne yönelimli çatıların (object-oriented framework) söz konusu olduğu durumda, somutlama sizden, çatı tarafından tanımlanan temel sınıflardan (base class) kalıtım alan özgül sınıflar oluşturmanızı isteyebilir. Bu, yeni elemanlar ortaya çıkmasına yol açar. Yeni elemanların yaratılmasını gerektirmeyen diğer yaklaşımlar arasında, önceki bir iterasyonda tanımlanmış bir teknoloji ailesi içinden belirli bir teknolojiyi seçmek, önceki bir iterasyonda tanımlanmış elemanlarla belirli bir çatıyı ilişkilendirmek, ya da belirli bir teknolojiyle ilişkilendirilmiş bir elemanın (örneğin bir iş parçacığı havuzundaki iş parçacığı sayısı gibi) yapılandırma seçeneklerini belirtmek sayılabilir.

## 3.5.2 Sorumlulukların İlişkilendirilmesi ve Özelliklerin Belirlenmesi

Tasarım kavramlarını somutlayarak elemanlar oluştururken, bu elemanlara tahsis edilen sorumlulukları da dikkate almanız gerekir. Örneğin, Katmanlar desenini somutlayıp geleneksel üç katmanlı yapıyı kullanmaya karar verirseniz, katmanlardan birinin kullanıcılarla etkileşimleri yönetmekten sorumlu olmasına (genellikle sunum katmanı olarak bilinir) karar verebilirsiniz.

Elemanları somutlarken ve sorumlulukları tahsis ederken, yüksek bağlılık/düşük bağımlılık (high cohesion/low coupling) tasarım ilkesini akılda tutmalısınız: Elemanlar, dar bir sorumluluk kümesiyle tanımlanan ve içsel olarak yüksek bağlılığa sahip olmalı; diğer elemanların uygulama ayrıntılarını bilmemek suretiyle de dışsal olarak düşük bağımlılığa sahip olmalıdır.

Tasarım kavramlarını somutlarken göz önünde bulundurmanız gereken bir başka husus da elemanların özellikleridir (property). Bu, seçilen teknolojilerin yapılandırma seçenekleri, durumluluk (statefulness), kaynak yönetimi, öncelik veya yarattığınız elemanlar fiziksel düğümler ise donanım özellikleri gibi hususları içerebilir. Bu özelliklerin belirlenmesi, hem analiz hem de tasarım gerekçelendirmesinin (design rationale) dokümantasyonunu destekler.

## 3.5.3 Elemanlar Arasındaki İlişkilerin Kurulması (Establishing Relationships Between the Elements)

öğeler ve bunların özellikleri arasındaki ilişkilere yönelik kararlar almayı da
gerektirir. Yine Katmanlar (Layers) desenini ele alalım. İki katmanın bağlı olduğuna karar verebilirsiniz, ancak bu katmanlar sonunda bileşenlere tahsis edilecek ve bu bileşenler de donanıma tahsis edilecektir. Böyle bir durumda, katmanlar bileşenlere tahsis edildikten sonra, bu katmanlar arasındaki iletişimin nasıl
gerçekleşeceğine karar vermeniz gerekir: İletişim eşzamanlı (synchronous) mı yoksa eşzamanlı olmayan (asynchronous) mı? Herhangi bir türde ağ (network) iletişimi içeriyor mu? Hangi tür protokol kullanılıyor? Ne kadar bilgi aktarılıyor ve hangi hızda? Bu tasarım kararları, performans gibi belirli kalite niteliklerine (quality attributes) ulaşma açısından önemli bir etkiye sahip olabilir.

## 3.6 Arayüzlerin (Interface) Tanımlanması

Arayüzler (interfaces), öğelerin dışarıdan görülebilen özellikleridir; öğelerin işbirliği yapmasını ve bilgi alışverişinde bulunmasını sağlayan sözleşmesel bir belirtim (contractual specification) oluştururlar. İki tür arayüz vardır: dışsal (external) ve içsel (internal).

### 3.6.1 Dışsal Arayüzler (External Interfaces)

Dışsal arayüzler; geliştirmekte olduğunuz sistemin ihtiyaç duyduğu diğer sistemlerin arayüzlerini ve sisteminizin diğer sistemlere sunduğu arayüzleri içerir. Gerekli (required) arayüzler, genellikle belirtimlerini etkileme gücünüz olmadığı için sisteminiz açısından bir kısıtın parçasıdır. Sağlanan (provided) arayüzlerin ise resmi olarak tanımlanması gerekir; bu da içsel arayüzleri tanımlamaya benzer biçimde, dış sistemler ile sisteminiz arasındaki etkileşimleri ele alıp bunları daha büyük bir yapının öğeleri olarak görerek yapılabilir.

Tasarım sürecinin başında bir sistem bağlamının (system context) kurulması, dışsal arayüzleri belirlemek için yararlıdır. Bu bağlam, Şekil 3.3’te gösterildiği gibi bir sistem bağlam diyagramı (system context diagram) kullanılarak temsil edilebilir. Dış varlıklar ile geliştirilmekte olan sistem arayüzler üzerinden etkileşime girdiğinden, her dış sistem için en az bir dışsal arayüz (şekildeki her ilişki) bulunmalıdır.

![Şekil 3.3](/home/runner/workspace/scripts/dsa_figs/sekil_3_3.png){width=11.85cm}


### 3.6.2 İçsel Arayüzler (Internal Interfaces)

İçsel arayüzler, tasarım kavramlarının somutlandırılması (instantiation) sonucunda ortaya çıkan öğeler arasındaki arayüzlerdir. İlişkileri ve arayüz ayrıntılarını belirlemek için, genellikle öğelerin çalışma zamanında (runtime) bilgiyi nasıl değiştokuş ettiğini anlamanız gerekir. Bunu, UML etkileşim şemaları (UML sequence diagrams) gibi modelleme araçlarının yardımıyla başarabilirsiniz (Şekil 3.4). Bu araçlar, kullanım durumlarını (use cases) veya kalite niteliği senaryolarını (quality attribute scenarios) desteklemek için yürütme sırasında öğeler arasında değiş tokuş edilen bilgiyi modellemenize imkân verir.

![Şekil 3.4](/home/runner/workspace/scripts/dsa_figs/sekil_3_4.png){width=11.78cm}


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

### Öğe Etkileşim Tasarımında Arayüzlerin Belirlenmesi

Arayüzleri tanımlamak mimari tasarım sürecinin temel bir parçası olmakla birlikte, mimari tasarım sırasında iç arayüzlerin hepsinin belirlenmediğini fark etmek önemlidir. Mimari tasarım sürecinin bir parçası olarak, tipik olarak birincil kullanım örneklerini (use case) mimari sürücülerin (architectural driver) bir parçası olarak ele alır ve bu birincil işlevselliği diğer sürücülerle birlikte destekleyen öğeleri (genellikle modüller) belirlersiniz. Ancak bu süreç, sistemin tüm kullanım örneklerini desteklemesi için gereken tüm öğeleri ve arayüzleri ortaya çıkarmaz. Bu belirginlik eksikliği kasıtlıdır: Mimari soyutlama ile ilgilidir; dolayısıyla özellikle tasarımın en erken aşamalarında bazı bilgilerin ayrıntı düzeyi daha az önemlidir.

Birincil olmayan kullanım örneklerini destekleyen modüllerin belirlenmesi, çoğu zaman tahmin ya da iş atama amaçları için gereklidir. Arayüzlerinin belirlenmesi, modüllerin ayrı ayrı geliştirilebilmesi ve entegre edilebilmesi ile birim testinin yapılabilmesi için de gereklidir. Bu modül belirleme işi proje yaşam döngüsünün erken safhalarında yapılabilir, ancak büyük tasarımın en başta yapılması (big design up front, BDUF) yaklaşımıyla karıştırılmamalıdır. En fazla, belirli bağlamlarda (örneğin erken tahmin ya da iterasyon planlama gibi) kaçınılması zor olan bir BDUF türüdür.

Bir mimar olarak, sistemin ya da sistemin belirli bir sürümünün tüm kullanım örnekleri kümesini destekleyen modüller kümesini belirleyebilirsiniz; ancak birincil olmayan kullanım örneklerini destekleyen modüllerle ilişkili arayüzlerin belirlenmesi tipik olarak sizin sorumluluğunuzda değildir; zira bu, sizin önemli miktarda zamanınızı gerektirir ve genellikle büyük bir mimari etkisi olmaz. Bizim öğe etkileşim tasarımı (element interaction design) adını verdiğimiz bu görev (bkz. Bölüm 2.2.2), genellikle mimari tasarım sona erdikten sonra, fakat modüllerin (çoğunun) geliştirilmesi başlamadan önce yerine getirilir.

Bu görevin geliştirme ekibinin diğer üyeleri tarafından yerine getirilmesi gerekir, ancak siz bu süreçte kritik bir rol oynarsınız; çünkü bu arayüzlerin sizin oluşturduğunuz mimari tasarıma uyması gerekir. Bir mimar olarak, mimariyi arayüzleri belirlemekten sorumlu mühendislere aktarmalı ve onların mevcut tasarım kararlarının gerekçesini anladıklarından emin olmalısınız.

Bu iletişimi sağlamanın iyi bir yolu, ara tasarımlar için etkin gözden geçirmeler (Active Reviews for Intermediate Design, ARID) yöntemini kullanmaktır. Bu yöntemde, mimari tasarım (ya da onun bir bölümü) bir grup gözden geçiren kişiye sunulur — bu durumda, tasarımı kullanacak mühendislerdir. Tasarım sunumundan sonra, katılımcılar tarafından bir dizi senaryo seçilir. Seçilen senaryolar, gözden geçirenlerin mimaride mevcut öğeleri kullanarak bu senaryoları karşılamaya çalıştıkları alıştırmanın çekirdeğini oluşturur.

Standart ARID’de, arayüzleri belirleme amacıyla gözden geçirenlerden kod ya da sözde kod (pseudo-code) yazmaları istenir. Alternatif olarak, mimar mimariyi sunabilir, birincil olmayan işlevsel bir senaryo seçebilir ve katılımcılardan bu senaryoyu destekleyen bileşenlerin arayüzlerini, sıralama diyagramları (sequence diagram) veya benzeri bir yöntem kullanarak belirlemelerini isteyebilir.

Bu çalışmada mimari tasarımın gözden geçirilmesi gerçeğinin ötesinde, bu yaklaşımın ek faydaları da vardır. Özellikle, tek bir toplantıda mimari tasarım ya da onun bir bölümü tüm ekibe sunulur ve arayüzlerin nasıl tanımlanacağına ilişkin (örneğin ayrıntı düzeyi veya parametre geçirme, veri tipleri, hata/istisna yönetimi gibi konularda) uzlaşmalar sağlanabilir.

### 3.7 Tasarım Sırasında Ön Taslak Dokümantasyon Oluşturma

Bir yazılım mimarisi tipik olarak, mimariyi oluşturan farklı yapıları temsil eden bir dizi görünüm (view) olarak dokümante edilir. Bu görünümlerin biçimsel dokümantasyonu tasarım sürecinin bir parçası değildir. Buna karşın, yapılar (structure) tasarımın bir parçası olarak üretilir. Bu yapıların ve bu yapıları oluşturmanıza yol açan tasarım kararlarının, gayriresmî bir biçimde (örneğin kaba eskizler olarak) bile olsa yakalanması, normal tasarım faaliyetlerinin bir parçası olarak yerine getirilmesi gereken bir görevdir.

#### 3.7.1 Görünümlerin Eskizlerini Kaydetme

Belirli bir tasarım problemini ele almak için seçtiğiniz tasarım kavramlarını somutlaştırarak yapılar ürettiğinizde, bu yapıları genellikle zihninizde üretmez, bunun yerine onların bazı eskizlerini oluşturursunuz. En basit durumda, bu eskizleri bir beyaz tahta, bir flipchart ya da hatta bir kâğıt parçası üzerinde üretirsiniz. Alternatif olarak, bu yapıları çizeceğiniz bir modelleme aracı da kullanabilirsiniz. Ürettiğiniz eskizler, mimariniz için yakalamanız gereken ve gerekirse ileride detaylandırabileceğiniz ilk dokümantasyondur.

Eskizler oluştururken, her zaman UML gibi daha biçimsel bir dil kullanmanız gerekmez. Gayriresmî bir gösterim kullanıyorsanız, en azından sembollerin kullanımında tutarlılığı koruma konusunda dikkatli olmalısınız. Er ya da geç, diyagramlarınıza açıklık sağlamak ve belirsizliği önlemek için bir lejant (legend) eklemeniz gerekecektir.

Yapıları oluştururken, öğelere atadığınız sorumlulukları yazıya dökme disiplinini geliştirmelisiniz. Bunun nedenleri basittir: Bir öğeyi tanımladığınız anda, zihninizde o öğe için bazı sorumlulukları da belirlemiş olursunuz. Bu sorumlulukları o anda yazmak, bunları daha sonra hatırlamak zorunda kalmamanızı sağlar. Ayrıca öğelerinizle ilişkili sorumlulukları zaman içinde yavaş yavaş yazmak, bunların tümünü daha sonra topluca derlemekten daha kolaydır.

Tasarım yaparken bu ön taslak dokümantasyonu hazırlamak belli bir disiplin gerektirir. Ancak faydaları emeğe değer — ileride daha ayrıntılı mimari dokümantasyonu nispeten kolay ve hızlı bir şekilde üretebileceksiniz. Bir beyaz tahta, flipchart ya da PowerPoint slaytı kullanıyorsanız, sorumlulukları dokümante etmenin basit bir yolu, ürettiğiniz eskizin fotoğrafını çekip bunu bir belgeye yapıştırmak ve diyagramda gösterilen her bir öğenin sorumluluklarını özetleyen bir tabloyla birlikte sunmaktır (Şekil 3.5 bir örnek sağlar). Bir bilgisayar destekli yazılım mühendisliği (computer-aided software engineering, CASE) aracı kullanıyorsanız, oluşturduğunuz bir öğeyi seçebilir ve söz konusu öğenin özellikler (properties) sayfasında genellikle bulunan metin alanını, onun sorumluluklarını dokümante etmek için kullanabilir ve ardından dokümantasyonu otomatik olarak üretebilirsiniz.

![Şekil 3.5](/home/runner/workspace/scripts/dsa_figs/sekil_3_5.png){width=10.9cm}


Bu diyagram, Bölüm 5’teki vaka çalışmasında genel sistem yapısını gösteren bir modül görünümü (module view) eskizini sunmaktadır.

BATCH Katmanı  
Ham Veri  
Depolama  
Veri  
Akışı  
Veri  
Kaynakları  

SERVING Katmanı  
Anlık (Ad Hoc) Görünümler  
Ön-hesaplama  

Anlık (Ad Hoc)  
Toplu Görünümler  

Statik Görünümler  
Ön-hesaplama  

Statik Toplu  
Görünümler  

SPEED Katmanı  
Gerçek Zamanlı  
Görünümler  

Lejant (Legend):  
Katman  
Sınırı  
Öğe  
Sınırı  

Kurumsal  
BI Aracı  

Pano (Dashboard) /  
Görselleştirme  
Aracı  

Veri Akışı  
(yön belirtilmiş)  
Sorgu Sonuçları Akışı  

> **💬 Çevirmen notu:** Buradaki örnek, sıkça “lambda mimarisi” olarak adlandırılan, batch/serving/speed katmanlarından oluşan veri işleme mimarilerini çağrıştırmaktadır; modül görünümü eskizlerinin, böyle yüksek seviyeli yapıları da sergilemesi amaçlanıyor.

Öğe diyagramı, öğenin sorumluluklarını tanımlayan bir tabloyla tamamlanır:

| Öğe          | Sorumluluk |
|-------------|------------|
| Veri akışı  | Bu öğe, tüm veri kaynaklarından gerçek zamanlı olarak veri toplar ve işlenmek üzere hem yığın katmanına (batch layer) hem de hız katmanına (speed layer) gönderir. |
| Yığın katmanı (batch layer) | Bu katman, ham veriyi depolamaktan ve sunum katmanında (serving layer) saklanacak yığın görünümlerini (batch views) önceden hesaplamaktan sorumludur. |
| ...         | ...        |
| ...         | ...        |

**ŞEKİL 3.5** Örnek ön taslak (preliminary) dokümantasyon

## 3.7 Tasarım Sırasında Ön Taslak Dokümantasyon Oluşturma

Elbette, her şeyi dokümante etmek gerekli değildir. Dokümantasyonun üç amacı vardır: analiz, inşa (construction) ve eğitim. Tasarım yaparken, bir dokümantasyon amacı seçmeli ve ardından risk azaltma (risk mitigation) kaygılarınıza göre bu amacı yerine getirecek şekilde dokümantasyon yapmalısınız. Örneğin, mimari tasarımınızın karşılaması gereken kritik bir kalite niteliği senaryonuz (quality attribute scenario) varsa ve bu gereksinimin bir analizde sağlandığını kanıtlamanız gerekecekse, analizin tatmin edici olabilmesi için ilgili bilgileri dikkatle dokümante etmelisiniz. Alternatif olarak, yeni ekip üyelerini eğitmek zorunda kalacağınızı öngörüyorsanız, sistemin bir bileşen-ve-bağlayıcı (C&C, component-and-connector) görünümünün bir taslağını hazırlamalı; bu taslak, sistemin nasıl çalıştığını ve öğelerin çalışma zamanında nasıl etkileşim kurduğunu göstermeli ve belki de sistemin en azından ana katmanlarını veya alt sistemlerini gösteren kaba bir modül görünümü oluşturmalısınız. Son olarak, dokümantasyon yaparken, tasarımınızın bir gün analiz edilebileceğini akılda tutmak iyi bir fikirdir. Bu nedenle, hangi bilgilerin bu analizi desteklemek için dokümante edilmesi gerektiği hakkında düşünmeniz gerekir (bkz. “Senaryo-Temelli Dokümantasyon” kenar notu).

### Senaryo-Temelli Dokümantasyon

Bir mimari tasarımın analizi, en önemli kullanım durumlarınıza (use case) ve kalite niteliği senaryolarınıza dayanır. Basitçe ifade edersek, bir senaryo seçilir ve siz, mimarinin bu senaryoyu nasıl desteklediğini ve kararlarınızı gerekçelendirerek açıklamak zorundasınız. Tasarım yaparken analize hazırlanmaya başlamak için, bir senaryonun karşılanmasına dahil olan öğeleri içeren yapıları üretmek ve bunları dokümante etmek yararlıdır. Tasarım süreci senaryolar tarafından yönlendirildiği için bu durum doğal olarak ortaya çıkmalıdır; ancak bu noktayı aklınızda sıkıca tutmak her zaman yardımcı olur.

Tasarım süreci sırasında, en azından aşağıdaki öğeleri tek bir belgede yakalamaya çalışmalısınız:

- Birincil sunum: Ürettiğiniz yapıyı temsil eden diyagram  
- Öğelerin sorumlulukları tablosu: Yapıda yer alan öğelerin sorumluluklarını kaydetmenize yardımcı olur  
- İlgili tasarım kararları ve bunların gerekçeleri (bkz. Bölüm 3.7.2)

Ayrıca iki tür ek bilgiyi de yakalayabilirsiniz:

- Öğelerin etkileşiminin çalışma zamanı gösterimi—for example, bir sıralama diyagramı (sequence diagram)
- İlk arayüz (interface) tanımları (bunlar ayrı bir belgede de tutulabilir)

Görüldüğü gibi, bu bilgilerin tümü tasarım sürecinin bir parçası olarak üretilmelidir. Her durumda, sistemde hangi öğelerin bulunacağına ve bunların nasıl etkileşim kuracağına karar vermeniz gerekir. Tek soru, bu bilgileri yazıya dökme zahmetine girip girmeyeceğiniz, yoksa tek temsilinin kodda mı kalacağıdır.

Burada savunduğumuz yaklaşımı izlerseniz, tasarımın sonunda elinizde, her biri belirli bir senaryoyla ilişkilendirilmiş, dokümante edilmiş bir dizi ön taslak görünüm (preliminary view) olacaktır ve bu dokümantasyona az bir maliyetle sahip olursunuz. Bu ön taslak dokümantasyon, tasarımı analiz etmek için, özellikle de senaryo-temelli değerlendirmeler yoluyla, olduğu gibi kullanılabilir.

## 3.7.2 Tasarım Kararlarının Kaydedilmesi

Her tasarım yinelemesinde, yineleme hedefinize ulaşmak için önemli tasarım kararları alırsınız. Daha önce gördüğümüz gibi, bu tasarım kararları şunları içerir:

- Birden fazla alternatif arasından bir tasarım kavramı (design concept) seçmek  
- Seçilen tasarım kavramını örnekleyerek (instantiate ederek) yapılar oluşturmak  
- Öğeler arasında ilişkiler kurmak ve arayüzler tanımlamak  
- Kaynakları tahsis etmek (örneğin, insanlar, donanım, hesaplama)  
- Diğerleri  

Bir mimariyi temsil eden bir diyagramı incelediğinizde, bir düşünme sürecinin nihai ürününü görürsünüz; ancak bu sonuca ulaşmak için hangi kararların alındığını anlamak kolay olmayabilir. Seçilen öğeler, ilişkiler ve özelliklerin temsilinin ötesinde tasarım kararlarını kaydetmek, sonuca nasıl ulaştığınızı anlamaya yardımcı olması açısından temeldir: buna tasarım gerekçesi (design rationale) denir.

Yineleme hedefiniz belirli bir kalite niteliği senaryosunu karşılama ile ilgili olduğunda, aldığınız bazı kararlar, senaryonun tepki ölçütünü (response measure) karşılama yeteneğinizde önemli roller oynar. Dolayısıyla, bunlar kaydetme konusunda en çok özen göstermeniz gereken kararlardır. Bu kararları kaydetmelisiniz; çünkü bunlar, önce oluşturduğunuz tasarımın analizini kolaylaştırmak, sonra uygulamayı kolaylaştırmak ve daha sonra (örneğin bakım sırasında) mimarinin anlaşılmasını desteklemek açısından gereklidir. Ayrıca her tasarım kararı “yeterince iyi”dir, ama nadiren optimumdur; bu nedenle alınan kararları gerekçelendirmeli ve muhtemelen kalan riskleri daha sonra yeniden ele almalısınız.

Tasarım kararlarını kaydetmenin sıkıcı bir iş olduğunu düşünebilirsiniz. Gerçekte, geliştirilen sistemin kritikliğine bağlı olarak kaydedilen bilgi miktarını ayarlayabilirsiniz. Örneğin, asgari bilgi kaydetmek için, Tablo 3.2’de gösterilen gibi basit bir tablo kullanabilirsiniz. Bu asgari düzeyden daha fazlasını kaydetmeye karar verirseniz, aşağıdaki bilgiler yararlı olabilir:

- Kararları gerekçelendirmek için hangi kanıtlar üretildi?  
- Kim ne yaptı?  
- Neden kestirmeler (shortcuts) kullanıldı?  

> **Tablo 3.2 Tasarım Kararlarını Dokümante Etmek İçin Örnek Tablo**

| Sürücü (Driver) | Tasarım Kararları ve Yeri | Gerekçe ve Varsayımlar |
|-----------------|---------------------------|------------------------|
| QA-1            | TimeServerConnector ve FaultDetectionService içinde eşzamanlılık (concurrency) tanıtılması (taktik, tactic) | Birden fazla olayı (tuzak, trap) aynı anda alıp işleyebilmek için sistemde eşzamanlılık tanıtılmalıdır. |
| QA-2            | İletişim katmanında bir mesaj kuyruğu (message queue) tanıtımı yoluyla mesajlaşma deseni (messaging pattern) kullanımı | ...  <br><br>Mesaj kuyruğu kullanımı senaryonun dayattığı performansa aykırı gibi görünse de, bazı mesaj kuyruğu gerçekleştirimleri yüksek performansa sahiptir ve ayrıca bu, QA-3’ü desteklemeye yardımcı olacaktır. <br>... |

- Neden ödünleşimler (tradeoff) yapıldı?  
- Hangi varsayımları yaptınız?  

Ve tıpkı öğeleri tanımlarken onların sorumluluklarını kaydetmenizi önerdiğimiz gibi, tasarım kararlarını da aldığınız anda kaydetmelisiniz. Bunun nedeni basittir: Eğer bu işi sonraya bırakırsanız, neden belirli şeyleri o şekilde yaptığınızı hatırlamayabilirsiniz.

## 3.8 Tasarım İlerleyişini İzleme

Nitelik temelli tasarım (Attribute-Driven Design, ADD) tasarımı sistematik biçimde yürütmek için açık yönergeler sağlasa da, tasarım ilerleyişini izlemek için bir mekanizma sunmaz. Oysa tasarım gerçekleştirirken yanıtlamak isteyeceğiniz birkaç soru vardır:

- Ne kadar tasarım yapmamız gerekiyor?
- Şu ana kadar ne kadar tasarım yaptık?
- Bitirdik mi?

Backlog’lar ve Kanban panoları gibi çevik (Agile) uygulamalar tasarım ilerleyişini izlemenize ve bu soruları yanıtlamanıza yardımcı olabilir. Bu teknikler elbette yalnızca çevik yöntemlerle sınırlı değildir. Herhangi bir yöntembilim (methodology) kullanan her geliştirme projesi, ilerleyişi izlemelidir.

### 3.8.1 Mimari Backlog Kullanımı

Mimari (veya tasarım) backlog kavramı birçok yazar tarafından önerilmiştir (Bkz. Bölüm 7.1). Bu kavram, Scrum gibi çevik geliştirme yöntemlerinde bulunan backlog’a benzer. Temel fikir, mimari tasarım sürecinin parçası olarak hâlâ gerçekleştirilmesi gereken bekleyen eylemlerin bir listesini oluşturmanız gerektiğidir.

Başlangıçta tasarım backlog’unu mimari sürücülerinizle (architectural driver) doldurmalısınız; ancak mimarinin tasarımını destekleyen diğer etkinlikler de dahil edilebilir. Örneğin:

- Belirli bir teknolojiyi sınamak veya belirli bir kalite niteliği (quality attribute) riskini ele almak için bir prototip oluşturma
- Mevcut varlıkların (asset) araştırılması ve anlaşılması (gerektiğinde tersine mühendislik (reverse engineering) yapılması)
- Tasarımın bir gözden geçirmesinde ortaya çıkarılan sorunlar
- Önceki bir yinelemede gerçekleştirilen kısmi tasarımın gözden geçirilmesi

Örneğin Scrum kullanırken, sprint backlog’u ile tasarım backlog’u birbirinden bağımsız değildir: Sprint backlog’undaki bazı özelliklerin gerçekleştirilmesi için mimari tasarım yapılması gerekebilir; dolayısıyla bunlar mimari tasarım backlog’una girecek maddeler oluştururlar. Bununla birlikte, bu iki backlog ayrı ayrı yönetilebilir. Tasarım backlog’u, genellikle müşteri (veya ürün sahibi) tarafından tartışılmayan ya da önceliklendirilmeyen çeşitli maddeler içerdiği için, dahili olarak bile yönetilebilir.

Ayrıca, kararlar alındıkça ek mimari kaygılar (architectural concern) ortaya çıkabilir. Örneğin bir referans mimari (reference architecture) seçerseniz, muhtemelen ona bağlı özel mimari kaygılar veya bunlardan türetilen kalite niteliği senaryolarını (quality attribute scenario, QAScenario) mimari tasarım backlog’una eklemeniz gerekecektir. Böyle bir kaygıya örnek olarak, bir web uygulaması referans mimarisinde oturumların yönetimi verilebilir.

### 3.8.2 Tasarım Kanban Panosu Kullanımı

Tasarım turlarla ve bu turlar içinde bir dizi yineleme (iteration) olarak yürütüldüğünden, tasarımın ilerleme derecesini izlemenin bir yoluna ihtiyaç duyarsınız. Ayrıca daha fazla tasarım kararı almaya (yani ek yinelemeler gerçekleştirmeye) devam etmeniz gerekip gerekmediğine de karar vermelisiniz. Bu görevi kolaylaştırmak için kullanılabilecek araçlardan biri, Şekil 3.6’da gösterilene benzer bir Kanban panosudur.

![Şekil 3.6](/home/runner/workspace/scripts/dsa_figs/sekil_3_6.png){width=12.06cm}


Tasarım turunun başında, tasarım sürecine giren girdiler backlog’da birer madde haline gelir. Başlangıçta bu etkinlik ADD’in 1. adımında gerçekleşir; bu tasarım turu için backlog’unuzdaki farklı maddeler, (önceki tasarım turlarında sonuçlandırılmamış ve bu turda ele almak istediğiniz girdiler hariç) panonun “Henüz Ele Alınmadı (Not Yet Addressed)” sütununa eklenmelidir. ADD’in 2. adımında bir tasarım yinelemesine başladığınızda, tasarım yinelemesinin hedefi kapsamında ele almayı planladığınız sürücülere karşılık gelen backlog girdileri “Kısmen Ele Alındı (Partially Addressed)” sütununa taşınmalıdır. Son olarak, bir yinelemeyi tamamladığınızda ve tasarım kararlarınızın analizi belirli bir sürücünün ele alındığını ortaya koyduğunda (ADD’in 7. adımı), ilgili girdi panonun “Tamamen Ele Alındı (Completely Addressed)” sütununa taşınmalıdır. Bir sürücünün “Tamamen Ele Alındı” sütununa taşınmasına olanak verecek açık ölçütler belirlemek önemlidir (bunu Scrum’da kullanılan “Bitti Tanımı (Definition of Done)”na benzer “Ele Alındı Tanımı (Definition of Addressed)” ölçütleri olarak düşünün).

Bir ölçüt, örneğin, sürücünün analiz edilmiş olması veya bir prototipte uygulanmış olması olabilir. Ayrıca, belirli bir yineleme için seçilen sürücüler, o yineleme kapsamında tamamen ele alınamayabilir; bu durumda “Kısmen Ele Alındı” sütununda kalmalıdırlar ve sonraki yinelemelere hazırlanırken bu sürücülerin, o anda var olan öğelere (mimari öğelere) nasıl tahsis edilebileceğini (allocation) düşünmelisiniz.

Panodaki girdileri önceliklerine göre ayırt etmenizi sağlayacak bir teknik seçmek faydalı olabilir. Örneğin, önceliğe bağlı olarak farklı renklerde Post-it notlar kullanabilirsiniz.

Böyle bir panoyla, (en önemli) sürücülerin kaç tanesinin o tasarım turunda ele alınmakta olduğunu veya ele alınmış olduğunu hızlıca görebildiğiniz için tasarımın ilerleyişini görsel olarak izlemek kolaydır. Bu teknik, ek yinelemeler yapmanız gerekip gerekmediğine karar vermenize de yardımcı olur; ideal olarak tasarım turu, sürücülerin çoğunluğu (ya da en azından en yüksek öncelikli olanları) “Tamamen Ele Alındı” sütununun altında yer aldığında sonlandırılır.

> **💬 Çevirmen notu:** Buradaki Kanban panosu, klasik “To Do / In Progress / Done” düzeninin, mimari sürücüler ve ADD adımlarıyla uyarlanmış hâli gibi düşünülebilir; amaç, özellikle mimari seviyedeki ilerlemeyi şeffaflaştırmaktır.

Bu bölümde, nitelik temelli tasarım (Attribute-Driven Design, ADD) yönteminin 3.0 sürümüne dair ayrıntılı bir örnek yürütme sunduk. Ayrıca, tasarım sürecinin çeşitli adımlarında dikkate alınması gereken birkaç önemli yönü tartıştık. Bu yönler arasında bir backlog’un kullanılması, olası farklı tasarım yol haritaları (greenfield, brownfield ve yeni/alışılmamış bağlamlar için), tasarım kavramlarının tanımlanması ve seçilmesi ve bunların yapıları üretmek için kullanılması, arayüzlerin tanımlanması ve ön dokümantasyonun üretilmesi yer alır.

Genel mimari geliştirme yaşam döngüsü, mimarinin belgelenmesini ve analiz edilmesini tasarım faaliyetlerinden ayrı etkinlikler olarak içerse de, bu etkinliklerin net bir biçimde ayrılmasının yapay ve zararlı olduğunu savunduk. Ön dokümantasyon ve analiz etkinliklerinin, tasarım sürecinin ayrılmaz parçaları olarak düzenli bir biçimde gerçekleştirilmesi gerektiğini vurguluyoruz.

4., 5. ve 6. bölümlerde, ADD 3.0’ı bir dizi genişletilmiş örnek üzerinden somutlayacak, yöntemin hem greenfield hem de brownfield bağlamlarda gerçek dünyada nasıl çalıştığını göstereceğiz.

## 3.10 Ek Okumalar

ADD 3.0’ın bazı kavramları ilk kez şu IEEE Software makalesinde tanıtılmıştır:  
H. Cervantes, P. Velasco ve R. Kazman, “A Principled Way of Using Frameworks in Architectural Design”, IEEE Software, 46–53, Mart/Nisan 2013.

ADD’nin 2.0 sürümü ilk kez şu SEI teknik raporunda belgelenmiştir:  
R. Wojcik, F. Bachmann, L. Bass, P. Clements, P. Merson, R. Nord ve B. Wood, “Attribute-Driven Design (ADD), Version 2.0”, SEI/CMU Technical Report CMU/SEI-2006-TR-023, 2006.

ADD 2.0’ın kullanımına ilişkin genişletilmiş bir örnek şu raporda yer almaktadır:  
W. Wood, “A Practical Example of Applying Attribute-Driven Design (ADD), Version 2.0”, SEI/CMU Technical Report: CMU/SEI-2007-TR-005.

Yazılım mimarilerinin tasarımını desteklemek için bir dizi alternatif yöntem de vardır. Bunlar 7. bölümde daha ayrıntılı biçimde tartışılmakta ve referans verilmektedir.

Bir mimari backlog (architecture backlog) kavramı şu çalışmada ele alınmaktadır:  
C. Hofmeister, P. Kruchten, R. Nord, H. Obbink, A. Ran ve P. America, “A General Model of Software Architecture Design Derived from Five Industrial Approaches”, Journal of Systems and Software, 80:106–126, 2007.

ARID yöntemi (Architecture Review for Intermediate Design) şu kaynakta tartışılmaktadır:  
P. Clements, R. Kazman ve M. Klein, *Evaluating Software Architectures: Methods and Case Studies*, Addison-Wesley, 2002.

CBAM yöntemi (Cost Benefit Analysis Method) şu kaynakta sunulmaktadır:  
L. Bass, P. Clements ve R. Kazman, *Software Architecture in Practice*, 3. baskı, Addison-Wesley, 2013.

Mimarinin nasıl belgelenebileceği konusu, şu kaynakta kapsamlı şekilde ele alınmaktadır:  
P. Clements vd., *Documenting Software Architectures: Views and Beyond*, 2. baskı, Addison-Wesley, 2011. Daha çevik (Agile) dokümantasyon yaklaşımları ise şu kitapta tartışılmaktadır:  
S. Brown, *Software Architecture for Developers*, Lean Publishing, 2015.

Tasarım gerekçesinin (design rationale) yakalanmasının önemi ve zorlukları şu çalışmada tartışılmaktadır:  
A. Tang, M. Ali Babar, I. Gorton ve J. Han, “A Survey of Architecture Design Rationale”, Journal of Systems and Software, 79(12):1792–1804, 2007.

Gerekçenin yakalanmasına yönelik minimalist bir teknik ise şu makalede ele alınmaktadır:  
U. Zdun, R. Capilla, H. Tran ve O. Zimmermann, “Sustainable Architectural Design Decisions”, IEEE Software, 30(6):46–53, 2013.

---

# 4  
Vaka Çalışması: FCAPS Sistemi

Şimdi, olgun bir alanda, greenfield bir sistem için ADD 3.0 kullanımına dair bir vaka çalışması sunacağız. Bu vaka çalışması, üç yinelemeden (iteration) oluşan bir ilk tasarım turunu ayrıntılandırmakta ve gerçek bir örneğe dayanmaktadır. Önce iş bağlamını sunuyor, ardından sistemin gereksinimlerini özetliyoruz. Bunu, ADD yinelemeleri sırasında gerçekleştirilen etkinliklerin adım adım bir özeti izliyor.

## 4.1 İş Senaryosu

2006 yılında, büyük bir telekomünikasyon şirketi, İnternet Protokolü (Internet Protocol, IP) ağını “operatör sınıfı hizmetleri (carrier-class services)” ve daha özelde yüksek kaliteli IP üzerinden ses (voice over IP, VOIP) sistemlerini destekleyecek şekilde genişletmek istedi. Bu hedefe ulaşmanın önemli yönlerinden biri, VOIP sunucularının ve diğer ekipmanların senkronizasyonuydu. Zayıf senkronizasyon, düşük hizmet kalitesi (Quality of Service, QoS), bozulan performans ve mutsuz müşterilerle sonuçlanır. Gerekli senkronizasyon seviyesine ulaşmak için şirket, Ağ Zaman Protokolü’nü (Network Time Protocol, NTP) destekleyen bir zaman sunucuları ağı konuşlandırmak istedi.

Zaman sunucuları, tipik olarak coğrafi bölgelere karşılık gelen gruplar hâlinde organize edilir. Bu bölgeler içinde zaman sunucuları, üst düzeyde konumlandırılan zaman sunucularının alt düzeydekilerin zamanı için referans görevi gördüğü, düzeyler ya da kademeler (strata) hâlinde hiyerarşik olarak düzenlenir.

> **💬 Çevirmen notu:** FCAPS, telekom yönetiminde “Fault, Configuration, Accounting, Performance, Security” alanlarını kapsayan klasik yönetim çerçevesidir; ilerleyen kısımlarda bu bağlam netleşecektir.

hiyerarşideki (seviye 1) zaman sunucuları, hassas zaman sağlayan donanımlarla (örneğin, sezyum osilatör, GPS sinyali) donatılmıştır. Hiyerarşide daha aşağı seviyelerde bulunan zaman sunucuları, üst seviyelerdeki sunuculardan veya eşlerinden zaman istemek için NTP (Network Time Protocol) kullanır.

Ağdaki birçok ekipman, zaman sunucuları tarafından sağlanan zamana bağımlıdır; bu nedenle şirket için önceliklerden biri, zaman sunucularında ortaya çıkan sorunları düzeltmektir. Bu tür sorunlar, zaman sunucularında yeniden başlatma gibi fiziksel bakım yapmak üzere bir teknisyenin sahaya gönderilmesini gerektirebilir. Şirketin bir diğer önceliği ise, senkronizasyon çerçevesinin performansını izlemek için zaman sunucularından veri toplamaktı.

İlk dağıtım planlarında, şirketin belirli bir modelden 100 zaman sunucusunu sahaya sürme isteği vardı. NTP’nin yanı sıra zaman sunucuları, üç temel işlem sağlayan Basit Ağ Yönetim Protokolü’nü (Simple Network Management Protocol, SNMP) de destekler:

- `set()` işlemleri: yapılandırma değişkenlerini değiştirme (örneğin, bağlı eşler).
- `get()` işlemleri: yapılandırma değişkenlerini veya performans verilerini alma.
- `trap()` işlemleri: GPS sinyalinin kaybı veya geri gelmesi ya da zaman referansındaki değişiklikler gibi olağandışı olaylara ilişkin bildirimler.

Şirketin hedeflerine ulaşmak için zaman sunucuları için bir yönetim sistemi geliştirilmesi gerekiyordu. Bu sistemin, ağ yönetimi için standart bir model olan FCAPS modeline uyması gerekiyordu. Kısaltmadaki harfler şunları ifade eder:

- **Fault management (arızayla yönetim)**. Arıza yönetiminin amacı, ağda meydana gelen arızaları tanımak, izole etmek, düzeltmek ve kaydetmektir. Bu durumda bu arızalar, zaman sunucuları tarafından üretilen tuzaklara (trap) veya yönetim sistemi ile zaman sunucuları arasındaki iletişimin kaybı gibi diğer sorunlara karşılık gelir.
- **Configuration management (yapılandırma yönetimi)**. Bu, ağ cihazlarından yapılandırmaları toplama ve depolamayı içerir; böylece cihazların yapılandırılmasını basitleştirir ve cihaz yapılandırmalarında yapılan değişiklikleri izlemenin yolunu sağlar. Bu sistemde, tek tek yapılandırma değişkenlerini değiştirmenin yanı sıra, belirli bir yapılandırmayı birden fazla zaman sunucusuna dağıtabilmek gereklidir.
- **Accounting (hesaplama/hesap yönetimi)**. Buradaki amaç, cihaz bilgilerini toplamaktır. Bu bağlamda bu, cihaz donanım ve gömülü yazılım (firmware) sürümlerini, donanım ekipmanını ve sistemin diğer bileşenlerini takip etmeyi içerir.
- **Performance management (performans yönetimi)**. Bu kategori, mevcut ağın verimliliğini belirlemeye odaklanır. Performans verileri toplanıp analiz edilerek ağ sağlığı izlenebilir. Bu durumda, zaman sunucularından gecikme (delay), ofset (offset) ve jitter ölçümleri toplanır.
- **Security management (güvenlik yönetimi)**. Bu, ağdaki varlıklara erişimi kontrol etme sürecidir. Bu durumda iki önemli kullanıcı türü vardır: teknisyenler ve yöneticiler (administrators). Teknisyenler, tuzak bilgilerini ve yapılandırmaları görüntüleyebilir ancak değişiklik yapamaz; yöneticiler ise teknisyenlerle aynı bilgileri görüntüleyebilir, ayrıca yapılandırmalarda değişiklik yapabilir ve ağa zaman sunucusu ekleyip çıkarabilirler.

> **💬 Çevirmen notu:** FCAPS, ağ yönetiminde yaygın kullanılan bir sınıflandırma çerçevesidir ve beş temel yönetim alanını sistematikleştirir.

Bir kez başlangıç ağı dağıtıldıktan sonra, şirket bunu, potansiyel olarak SNMP dışındaki yönetim protokollerini destekleyebilecek yeni model zaman sunucuları ekleyerek genişletmeyi planlamıştır.

Bu bölümün geri kalanı, ADD 3.0 (Attribute-Driven Design 3.0) kullanılarak oluşturulmuş bu sistemin bir tasarımını açıklamaktadır.

---

## 4.2 Sistem Gereksinimleri

Gereksinim ortaya çıkarma (requirement elicitation) etkinlikleri daha önce gerçekleştirilmişti ve aşağıda toplanan en ilgili gereksinimlerin bir özeti verilmektedir.

### 4.2.1 Kullanım Senaryosu (Use Case) Modeli

Şekil 4.1’deki kullanım senaryosu modeli, sistemde FCAPS modelini destekleyen en ilgili kullanım senaryolarını göstermektedir. Diğer kullanım senaryoları gösterilmemiştir.

![Şekil 4.1](/home/runner/workspace/scripts/dsa_figs/sekil_4_1.png){width=9.28cm}


**ŞEKİL 4.1** FCAPS sistemi için kullanım senaryosu modeli

---

Bu kullanım senaryolarının her biri aşağıdaki tabloda açıklanmıştır:

| Kullanım Senaryosu | Açıklama |
| --- | --- |
| **UC-1: Ağ durumunu izle** | Kullanıcı, tüm ağın hiyerarşik bir gösteriminde zaman sunucularını izler. Sorunlu cihazlar ve bunların gruplanmış olduğu mantıksal bölgeler vurgulanır. Kullanıcı ağ gösterimini genişletebilir ve daraltabilir. Bu gösterim, arızalar tespit edildikçe veya onarıldıkça sürekli olarak güncellenir. |
| **UC-2: Arıza tespiti** | Yönetim sistemi periyodik olarak zaman sunucuları ile iletişime geçerek onların “canlı” olup olmadığını kontrol eder. Bir zaman sunucusu yanıt vermezse ya da bir problemi veya normal çalışma durumuna geri dönüşü işaret eden bir tuzak (trap) alınırsa, olay depolanır ve kullanıcıların gördüğü ağ gösterimi buna göre güncellenir. |
| **UC-3: Olay geçmişini göster** | Belirli bir zaman sunucusu veya bir grup zaman sunucusu ile ilişkili depolanmış olaylar görüntülenir. Bunlar tür veya öncelik derecesi gibi çeşitli ölçütlere göre filtrelenebilir. |
| **UC-4: Zaman sunucularını yönet** | Yönetici, ağa bir zaman sunucusu ekler veya ağdan bir zaman sunucusunu çıkarır. |
| **UC-5: Zaman sunucusunu yapılandır** | Yönetici, belirli bir zaman sunucusuyla ilişkili yapılandırma parametrelerini değiştirir. Parametreler cihaza gönderilir ve yerel olarak da depolanır. |
| **UC-6: Yapılandırmayı geri yükle** | Yerel olarak depolanmış bir yapılandırma, bir veya daha fazla zaman sunucusuna gönderilir. |
| **UC-7: Performans verisi topla** | Ağ performans verileri (gecikme, ofset ve jitter), zaman sunucularından periyodik olarak toplanır. |
| **UC-8: Bilgi görüntüle** | Kullanıcı, zaman sunucusu hakkında depolanmış bilgileri — yapılandırma değerleri ve sunucu adı gibi diğer parametreleri — görüntüler. |
| **UC-9: Performans verisini görselleştir** | Kullanıcı, ağ performans ölçümlerini (gecikme, ofset, jitter) ağ performansını görmek ve analiz etmek için grafiksel bir biçimde görüntüler. |
| **UC-10: Sisteme giriş yap** | Kullanıcı, bir giriş/parola ekranı aracılığıyla sisteme giriş yapar. Başarılı girişten sonra kullanıcıya rolüne göre farklı seçenekler sunulur. |
| **U-11: Kullanıcıları yönet** | Yönetici, kullanıcı ekler veya çıkarır ya da kullanıcı izinlerini değiştirir. |

### 4.2.2 Kalite Niteliği Senaryoları (Quality Attribute Scenarios)

Bu kullanım senaryolarına ek olarak, bir dizi kalite niteliği (quality attribute) senaryosu ortaya çıkarılmış ve belgelenmiştir. Bunların içinden en ilgili altı tanesi aşağıdaki tabloda sunulmuştur. Her senaryo için ayrıca ilişkili olduğu kullanım senaryosunu da belirtiyoruz.

| ID | Kalite Niteliği | Senaryo | İlişkili Kullanım Senaryosu |
| --- | --- | --- | --- |
| **QA-1** | Performans | Birçok zaman sunucusu, tepe yük sırasında yönetim sistemine tuzaklar gönderir; tuzakların %100’ü başarıyla işlenir ve depolanır. | UC-2 |
| **QA-2** | Değiştirilebilirlik (Modifiability) | Sisteme bir güncellemenin parçası olarak yeni bir zaman sunucusu yönetim protokolü eklenir. Protokol, sistemin çekirdek bileşenlerinde herhangi bir değişiklik yapılmadan başarıyla eklenir. | — |
| **QA-3** | Kullanılabilirlik (Availability) | Normal çalışma sırasında yönetim sisteminde bir arıza oluşur. Yönetim sistemi 30 saniyeden kısa sürede çalışmaya yeniden başlar. | Tümü |
| **QA-4** | Performans | Yönetim sistemi, tepe yük sırasında bir zaman sunucusundan performans verisi toplar. Yönetim sistemi, tüm performans verisini 5 dakika içinde toplar ve bu sırada tüm kullanıcı isteklerini işler; böylece CON-5’ten kaynaklanan veri kaybı yaşanmaz. | UC-7 |
| **QA-5** | Performans, kullanılabilirlik (usability) |  |  |

Bir kullanıcı, normal çalışma sırasında belirli bir zaman sunucusunun olay geçmişini görüntüler. Son 24 saate ait olay listesi 1 saniye içinde görüntülenir.

UC-3

QA-6

Güvenlik (Security)

Bir kullanıcı, normal çalışma sırasında sistemde bir değişiklik yapar. Kimin, hangi zamanda bu işlemi yaptığını bilmek her zaman (%100) mümkün olacaktır.

Tümü (All)

### 4.2.3 Kısıtlar (Constraints)

Son olarak, sistem ve onun gerçekleştirimine (implementation) ilişkin bir dizi kısıt toplanmıştır. Bunlar aşağıdaki tabloda sunulmaktadır.

| ID     | Kısıt (Constraint)                                                                                                                                              |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CON-1  | En az 50 eşzamanlı kullanıcının desteklenmesi gerekir.                                                                                                          |
| CON-2  | Sisteme, farklı platformlardaki (Windows, OSX ve Linux) bir web tarayıcısı (Chrome V3.0+, Firefox V4+, IE8+) üzerinden erişilmelidir.                          |
| CON-3  | Mevcut bir ilişkisel veritabanı sunucusu kullanılmalıdır. Bu sunucu, veritabanını barındırmak dışında başka amaçlarla kullanılamaz.                             |
| CON-4  | Kullanıcı iş istasyonlarına olan ağ bağlantısı düşük bant genişliğine sahip olabilir, ancak genel olarak güvenilirdir.                                          |
| CON-5  | Zaman sunucularının veriyi atmasına yol açtığından, performans verileri en fazla 5 dakikalık aralıklarla toplanmalıdır.                                        |
| CON-6  | Son 30 güne ait olaylar saklanmalıdır.                                                                                                                          |

80 Bölüm 4—Vaka Çalışması: FCAPS Sistemi

### 4.2.4 Mimari Kaygılar (Architectural Concerns)

Bu bir “greenfield” geliştirme olduğu için (yani tamamen sıfırdan yeni bir sistem geliştirildiği için), başlangıçta yalnızca birkaç genel mimari kaygı belirlenmiştir; bunlar aşağıdaki tabloda gösterilmektedir.

| ID     | Kaygı (Concern)                                                                                                                                                               |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CRN-1  | Genel, başlangıç düzeyinde bir sistem yapısının oluşturulması.                                                                                                                |
| CRN-2  | Ekip üyelerinin Java teknolojileri (Spring, JSF, Swing, Hibernate, Java Web Start ve JMS çatıları (frameworks) ve Java dili) konusundaki bilgisinden yararlanmak.            |
| CRN-3  | Geliştirme ekibinin üyelerine işin (görevlerin) atanması.                                                                                                                      |

Bu girdi kümeleri göz önüne alındığında, artık Bölüm 3.2’de anlatıldığı gibi tasarım sürecini açıklamaya geçmeye hazırız. Bu bölümde, gereksinim toplama sürecinin yalnızca nihai sonuçlarını sunuyoruz. Bu gereksinimleri toplama işi önemsiz değildir, ancak bu bölümün kapsamı dışındadır.

## 4.3 Tasarım Süreci (The Design Process)

Artık gereksinimler ve iş (işletme) kaygıları dünyasından tasarım dünyasına sıçrama yapmaya hazırız. Bu, bir mimarın belki de en önemli görevidir: gereksinimleri tasarım kararlarına çevirmek. Elbette, başka birçok karar ve görev de önemlidir, ancak mimar olmanın özü, geniş kapsamlı sonuçlara sahip tasarım kararları vermektir.

### 4.3.1 ADD Adım 1: Girdileri Gözden Geçirme

nitelik temelli tasarım (Attribute-Driven Design, ADD) yöntemi içindeki ilk adım, girdilerin gözden geçirilmesini ve hangi gereksinimlerin sürücü (driver) olarak ele alınacağını (yani hangilerinin tasarım iş listesine (design backlog) dahil edileceğini) belirlemeyi içerir. Girdiler aşağıdaki tabloda özetlenmiştir.

| Kategori                         | Ayrıntılar                                                                                                                                                                             |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tasarım amacı (Design purpose)   | Bu, olgun (mature) bir alanda geliştirilen bir greenfield sistemdir. Amaç, sistemin inşasını desteklemek için yeterince ayrıntılı bir tasarım üretmektir.                             |
| Birincil işlevsel gereksinimler  | Bölüm 4.2.1’de sunulan kullanım senaryolarından (use cases) birincil olanlar şu şekilde belirlenmiştir:  UC-1: Çekirdek işi doğrudan desteklediği için  UC-2: Çekirdek işi doğrudan desteklediği için  UC-7: Bununla ilişkili teknik konular nedeniyle (bkz. QA-4) |

4.3 Tasarım Süreci

| Kategori                               | Ayrıntılar                                                                                                                                                                                                                  |
|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Kalite niteliği senaryoları (quality attribute scenarios) | Senaryolar Bölüm 4.2.2’de açıklanmıştır. Şimdi (Bölüm 2.4.2’de tartışıldığı gibi) aşağıdaki şekilde önceliklendirilmişlerdir: |

| Senaryo ID | Müşteri için önemi (Importance to the Customer) | Mimara göre gerçekleştirme zorluğu (Difficulty of Implementation According to the Architect) |
|------------|--------------------------------------------------|------------------------------------------------------------------------------------------------|
| QA-1       | Yüksek (High)                                   | Yüksek (High)                                                                                  |
| QA-2       | Yüksek (High)                                   | Orta (Medium)                                                                                  |
| QA-3       | Yüksek (High)                                   | Yüksek (High)                                                                                  |
| QA-4       | Yüksek (High)                                   | Yüksek (High)                                                                                  |
| QA-5       | Orta (Medium)                                   | Orta (Medium)                                                                                  |
| QA-6       | Orta (Medium)                                   | Düşük (Low)                                                                                    |

Bu listeden yalnızca QA-1, QA-2, QA-3 ve QA-4 sürücü (driver) olarak seçilmiştir.

| Kategori      | Ayrıntılar                                                                                               |
|---------------|----------------------------------------------------------------------------------------------------------|
| Kısıtlar      | Bölüm 4.2.3’te tartışılan tüm kısıtlar sürücü olarak dahil edilmiştir.                                   |
| Mimari kaygılar | Bölüm 4.2.4’te tartışılan tüm mimari kaygılar sürücü olarak dahil edilmiştir.                          |

### 4.3.2 Yineleme 1: Genel Bir Sistem Yapısının Oluşturulması

Bu bölüm, tasarım sürecinin ilk yinelemesinde ADD’in her bir adımında gerçekleştirilen etkinliklerin sonuçlarını sunmaktadır.

#### 4.3.2.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu, bir greenfield sistem tasarımındaki ilk yinelemedir; dolayısıyla yineleme hedefi, genel bir sistem yapısı oluşturma mimari kaygısı CNR-1’e ulaşmaktır (bkz. Bölüm 3.3.1).

Bu yineleme genel bir mimari kaygı tarafından yönlendiriliyor olsa da, mimar sistemin genel yapısını etkileyebilecek tüm sürücüleri akılda tutmalıdır. Özellikle, mimar aşağıdakilere dikkat etmelidir:

- QA-1: Performans (Performance)
- QA-2: Değiştirilebilirlik (Modifiability)
- QA-3: Kullanılabilirlik (Availability)
- QA-4: Performans (Performance)
- CON-2: Sisteme farklı platformlarda—Windows, OSX ve Linux—bir web tarayıcısı üzerinden erişilmelidir
- CON-3: İlişkisel bir veritabanı sunucusu kullanılmalıdır
- CON-4: Kullanıcı iş istasyonlarına ağ bağlantısı düşük bant genişliğine sahip olabilir ve güvenilir olmayabilir
- CRN-2: Ekibin Java teknolojileri konusundaki bilgisinden yararlanmak

82 Bölüm 4—Vaka Çalışması: FCAPS Sistemi

Time server

Açıklama (Legend):

ŞEKİL 4.2 FCAPS sistemi için bağlam diyagramı (context diagram)

#### 4.3.2.2 Adım 3: Ayrıntılandırılacak Bir veya Daha Fazla Sistem Ögesinin Seçilmesi

Bu bir greenfield geliştirme çalışmasıdır; bu nedenle bu durumda ayrıntılandırılacak öge, Şekil 4.2’de gösterilen tüm FCAPS sistemidir. Bu durumda ayrıntılandırma, parçalarına ayırma (decomposition) yoluyla gerçekleştirilir.

![Şekil 4.2](/home/runner/workspace/scripts/dsa_figs/sekil_4_2.png){width=11.71cm}


#### 4.3.2.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramının Seçilmesi

Bu ilk yinelemede, tüm sistemin yapılandırılması hedefi göz önüne alındığında, tasarım kavramları Bölüm 3.3.1’de sunulan yol haritasına göre seçilmiştir. Aşağıdaki tablo, tasarım kararlarının seçimini özetlemektedir. Bu vaka çalışmasında kullanılan tüm tasarım kavramlarının Ek A’da da açıklanmış olduğunu unutmayın.

| Tasarım Kararları ve Konumu                                         | Gerekçe (Rationale)                                                                                                                                                                                                                                                                                                                                                                                                      |
|----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sistemin istemci (client) kısmını Mantıksal olarak Zengin İstemci Uygulaması başvuru mimarisi (Rich Client Application reference architecture) kullanarak yapılandırma | Zengin İstemci Uygulaması (Rich Client Application, RCA) başvuru mimarisi (bkz. Bölüm A.1.2), kullanıcıların PC’lerine kurulmuş uygulamaların geliştirilmesini destekler. Bu uygulamalar, ağ topolojisini ve performans grafiklerini (UC-1) göstermek için gereken zengin kullanıcı arayüzü yeteneklerini destekler. Bu yetenekler, her ne kadar bu tasarım kararı sürücü olmasa da QA‑5’in gerçekleştirilmesine de yardımcı olur. Bu tür uygulamalar bir web tarayıcısında çalışmamakla birlikte (CON-2), Java Web Start gibi bir teknoloji kullanılarak bir web tarayıcısından kurulabilirler. |

> **💬 Çevirmen notu:** “Rich Client Application (RCA) reference architecture” burada bir mimari stil/başvuru mimarisi olarak kullanılıyor; kalıp isim olarak bırakılıp Türkçesi açıklama şeklinde verildi.

4.3 Tasarım Süreci

| Tasarım Kararları ve Konumu | Gerekçe (Rationale) |
|-----------------------------|----------------------|
| Elenen alternatifler (Discarded alternatives): |  |
| Alternatif                 | Elenme Nedeni (Reason for Discarding)                                                                                                                                                                                                 |
| Zengin İnternet uygulamaları (Rich Internet Applications, RIA) | Bu başvuru mimarisi (bkz. Bölüm A.1.3), web tarayıcısı içinde çalışan zengin kullanıcı arayüzlü uygulamaların geliştirilmesine yöneliktir. Bu tür bir uygulama zengin bir kullanıcı arayüzünü destekler ve kolayca yükseltilebilir olsa da, RIA çalıştırmak için gereken eklentilerin, Java Sanal Makinesi’ne (Java Virtual Machine) kıyasla daha az yaygın olduğu düşünülmüştür; bu nedenle bu seçenek elenmiştir. |
| Web uygulamaları (Web applications) |  |

Bu referans mimari (bkz. Bölüm A.1.1), bir web tarayıcısı üzerinden erişilen uygulamaların geliştirilmesine yöneliktir. Bu referans mimari dağıtım ve güncellemeyi kolaylaştırsa da, zengin bir kullanıcı arayüzü deneyimi sunmanın zor olması nedeniyle elenmiştir.

### Mobil
### uygulamalar

Bu referans mimari (bkz. Bölüm A.1.4), elde taşınabilir (handheld) cihazlara dağıtılan uygulamaların geliştirilmesine yöneliktir. Bu seçenek, bu tür cihazların sisteme erişim için kullanılmasının öngörülmemesi nedeniyle elenmiştir.

### Sistemin sunucu kısmını Service Application referans mimarisi kullanarak mantıksal olarak yapılandırma

Servis uygulamaları (service applications) (bkz. Bölüm A.1.5), bir kullanıcı arayüzü sağlamaz; bunun yerine, diğer uygulamalar tarafından tüketilen servisleri sunarlar. Mimar bu referans mimariye aşina olduğu ve gereksinimleri tam olarak karşılamaya yeterli olduğunu düşündüğü için başka hiçbir alternatif değerlendirilmemiş ve elenmemiştir.

### Uygulamayı üç katmanlı dağıtım deseni (three-tier deployment pattern) kullanarak fiziksel olarak yapılandırma

Sisteme bir web tarayıcısı üzerinden erişilmesi gerektiği (CON-2) ve var olan bir veritabanı sunucusunun da kullanılması gerektiği (CON-3) için üç katmanlı bir dağıtım (deployment) uygundur (bkz. Bölüm A.2.2).

Bu noktada, QA-3’ü desteklemek için hem web/uygulama katmanında hem de veritabanı katmanında bir tür çoğaltmaya (replication) ihtiyaç olacağı açıktır, ancak bu konuya daha sonra (3. yinelemede) değinilecektir.

Elenen alternatifler, n != 3 olan diğer n katmanlı (n‑tier) desenleri içermektedir. İki katmanlı alternatif, sisteme mevcut bir eski (legacy) veritabanı sunucusunun dâhil edilmesi gerektiği ve CON-3’e göre bu sunucunun başka hiçbir amaçla kullanılamayacağı için elenmiştir. n > 3 olan tüm alternatifler, bu noktada çözüm için başka sunuculara ihtiyaç duyulmadığı için elenmiştir.

---

### Tasarım Kararları
### ve Konumu

### Gerekçe

#### İstemci uygulamasının kullanıcı arayüzünü Swing Java çatısı (framework) ve diğer Java teknolojilerini kullanarak oluşturma

Java Rich Client’lar geliştirmek için standart çatı, taşınabilirliği (CON-2) güvence altına alır ve geliştiricilerin zaten aşina olduğu teknolojidir (CRN-3).

Elenen alternatifler: Eclipse SWT (Standard Widget Toolkit) çatısı değerlendirilmiştir, ancak geliştiriciler ona bu kadar aşina değildir.

#### Uygulamayı Java Web Start teknolojisini kullanarak dağıtma

Uygulamaya erişim, yükleyiciyi başlatan bir web tarayıcısı (CON-2) aracılığıyla sağlanır. Bu teknoloji ayrıca güncellemeyi de kolaylaştırır, çünkü istemci kodu yalnızca yeni bir sürüm mevcut olduğunda yeniden yüklenir. Güncellemelerin sık gerçekleşmesi beklenmediğinden, bu düşük bant genişlikli (CON-4) durumlar için faydalıdır.

Alternatif, applet kullanımı olurdu; ancak applet’lerin, web sayfası her yüklendiğinde yeniden yüklenmesi gerekir, bu da bant genişliği gereksinimlerini artırır.

---

## 4.3.2.4 Adım 5: Mimari Öğeleri Örneklendirme, Sorumlulukları Tahsis Etme ve Arayüzleri Tanımlama

Örneklendirme (instantiation) ile ilgili ele alınan ve verilen tasarım kararları aşağıdaki tabloda özetlenmiştir:

### Tasarım Kararı ve
### Konumu

### Gerekçe

#### Zengin istemci uygulamasındaki yerel veri kaynaklarını kaldırma

Ağın genellikle güvenilir olması nedeniyle veriyi yerel olarak saklamaya gerek olmadığı düşünülmektedir. Ayrıca, sunucu ile iletişim veri katmanında (data layer) yürütülmektedir. İstemci içindeki bileşenler arasındaki iç iletişim yerel metot çağrıları üzerinden yönetilir ve özel bir desteğe ihtiyaç duymaz.

#### Service Application referans mimarisinin veri katmanında zaman sunucularına erişime adanmış bir modül oluşturma

Referans mimarideki service agents bileşeni, zaman sunucularına erişimi soyutlayacak şekilde uyarlanmıştır. Bu, QA-2’nin gerçekleştirilmesini daha da kolaylaştıracak ve UC-2 ile UC-7’nin gerçekleştirilmesinde kritik bir rol oynayacaktır.

Bu örneklendirme kararlarının sonuçları bir sonraki adımda kayıt altına alınmıştır. Bu ilk yinelemede, işlevselliği ve arayüzleri tam olarak tanımlamak için genellikle çok erkendir. Bir sonraki yineleme, işlevselliği daha ayrıntılı tanımlamaya ayrılmıştır ve bu aşamada arayüzler tanımlanmaya başlanacaktır.

---

## 4.3.2.5 Adım 6: Görünümleri Taslak Olarak Çizme ve Tasarım Kararlarını Kaydetme

Şekil 4.3’teki diyagram, istemci ve sunucu uygulamaları için seçilen iki referans mimarinin modül görünümünün (module view) bir taslağını göstermektedir. Bunlar artık aldığımız tasarım kararlarına göre uyarlanmıştır.

![Şekil 4.3](/home/runner/workspace/scripts/dsa_figs/sekil_4_3.png){width=9.14cm}


---

## 4.3 Tasarım Süreci

### İstemci Tarafı

`«Layer»` Presentation CS  

`«Layer»` Cross-cutting CS  
`«Swing»` UI Modules  

UI Process Modules  

Security Module CS  

`«Layer»` Business logic CS  

Business Modules CS  

Op. Mgmt. Module CS  

Business Entities CS  

`«Layer»` Data CS  

`«Module»` Communication Modules  

### Sunucu Tarafı

`«Layer»` Services SS  

`«Layer»` Cross-cutting SS  

Service Interfaces  
Security Module SS  

`«Layer»` Business Logic SS  
Business Modules SS  

Business Entities SS  

`«Layer»` Data SS  

Op. Mgmt. Module SS  

Communication Module SS  
DB Access Module  

Time Server Access Module  

**ŞEKİL 4.3** Seçilen referans mimarilerden elde edilen modüller (Anahtar: UML)

---

Bu taslak bir CASE aracı kullanılarak oluşturulmuştur. Araçta her bir öğe seçilmekte ve sorumluluklarına ilişkin kısa bir açıklama kaydedilmektedir. Bu noktadaki açıklamaların oldukça kaba olduğunu, yalnızca temel işlevsel sorumlulukları belirttiğini ve ayrıntı içermediğini not ediniz. Aşağıdaki tablo, kaydedilen bilgileri özetlemektedir:

| Öğe                       | Sorumluluk |
|--------------------------|------------|
| **Presentation client side (CS)** | Bu katman, kullanıcı etkileşimini kontrol eden ve kullanım durumu (use case) kontrol akışını yöneten modülleri içerir. |
| **Business logic CS**    | Bu katman, istemci tarafında yerel olarak yürütülebilen iş mantığı (business logic) işlemlerini gerçekleştiren modülleri içerir. |
| **Data CS**              | Bu katman, sunucu ile iletişimden sorumlu modülleri içerir. |
| **Cross-cutting CS**     | Bu “katman”, güvenlik, kayıt (logging) ve G/Ç (I/O) gibi farklı katmanlara yayılan işlevselliğe sahip modülleri içerir. QA-6 bir sürücü olmasa bile, onun başarılmasına yardımcı olur. |
| **UI modules**           | Bu modüller, kullanıcı arayüzünü oluşturur (render) ve kullanıcı girdilerini alır. |
| **UI process modules**   | Bu modüller, tüm sistem kullanım durumlarının (ekranlar arası gezinme dâhil) kontrol akışından sorumludur. |
| **Business modules CS**  | Bu modüller ya yerel olarak gerçekleştirilebilen iş operasyonlarını uygular ya da sunucu tarafındaki işlevselliği ortaya çıkarır. |
| **Business entities CS** | Bu varlıklar, alan (domain) modelini oluşturur. Sunucu tarafındakilere göre daha az ayrıntılı olabilirler. |
| **Communication modules CS** | Bu modüller, sunucu tarafında çalışan uygulama tarafından sağlanan servisleri tüketir. |
| **Services server side (SS)** | Bu katman, istemciler tarafından tüketilen servisleri ortaya çıkaran modülleri içerir. |
| **Business Logic SS**    | Bu katman, sunucu tarafında işlenmesi gereken iş mantığı işlemlerini gerçekleştiren modülleri içerir. |
| **Data SS**              | Bu katman, veri kalıcılığından (persistence) ve zaman sunucuları ile iletişimden sorumlu modülleri içerir. |
| **Cross-cutting SS**     |  |

> **💬 Çevirmen notu:** “CS” (client side) istemci tarafını, “SS” (server side) sunucu tarafını ifade etmektedir; katman adlarında bu kısaltmalar korunmuştur.

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

![Şekil 4.4](/home/runner/workspace/scripts/dsa_figs/sekil_4_4.png){width=11.71cm}


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

Bu yinelemede, bu örnekte mimari tasarım desenleri (architectural design patterns) olan çeşitli tasarım kavramları, *Pattern Oriented Software Architecture, Volume 4* kitabından seçilir. Aşağıdaki tablo tasarım kararlarını özetlemektedir. Aşağıdaki tablodaki kalın yazılmış sözcükler bu kitaptaki mimari desenlere (architectural patterns) karşılık gelir ve Ek A’da bulunabilir.

**Tasarım Kararları ve Konumu** | **Gerekçe ve Varsayımlar**
---|---
Uygulama için bir Alan Modeli (Domain Model) oluştur | İşlevsel (fonksiyonel) bir ayrıştırmaya başlamadan önce, sistem için başlangıç niteliğinde bir alan modeli (domain model) oluşturmak, alandaki başlıca varlıkları ve bunların ilişkilerini tanımlamak gereklidir. Bunun için iyi bir alternatif yoktur. Bir alan modeli eninde sonunda oluşturulmak zorundadır; aksi takdirde, alttan alta, optimal olmayan bir biçimde ortaya çıkar; bu da anlaşılması ve bakımı zor, geçici çözümlerden oluşan (ad hoc) bir mimariye yol açar.
İşlevsel gereksinimlere karşılık gelen Alan Nesnelerini (Domain Objects) tanımla | Uygulamanın her bir ayrı işlevsel öğesinin, kendi içinde tamamlanmış bir yapı taşı—bir alan nesnesi (domain object)—içinde kapsüllenmesi gerekir. Olası bir alternatif, alan nesnelerini hiç dikkate almamak ve doğrudan katmanları modüllere ayrıştırmaktır; ancak bu, bir gereksinimin gözden kaçırılması riskini artırır.

## 4.3 Tasarım Süreci

**Tasarım Kararları ve Konumu** | **Gerekçe ve Varsayımlar**
---|---
Alan Nesnelerini genel ve uzmanlaşmış Bileşenlere (Components) ayrıştır | Alan nesneleri, işlevselliğin tam kümelerini temsil eder, ancak bu işlevsellik katmanlar içinde yer alan daha ince taneli (fine-grained) öğeler tarafından desteklenir. Bu desendeki “bileşenler (components)” bizim modül (module) olarak adlandırdığımız şeylere karşılık gelmektedir. Modüllerin uzmanlaşması, bulundukları katmanlarla ilişkilidir (örneğin, UI modülleri). İşlevselliği desteklemek için katmanların modüllere ayrıştırılmasına iyi bir alternatif yoktur.
Spring framework ve Hibernate kullan | Spring, kurumsal uygulama (enterprise application) geliştirmeyi desteklemek için yaygın olarak kullanılan bir framework’tür. Hibernate, Spring ile iyi bütünleşen bir nesne-ilişkisel eşleme (object-relational mapping, ORM) framework’üdür. Uygulama geliştirme için değerlendirilen bir alternatif JEE idi. Spring, daha “hafif” (lightweight) olarak değerlendirildiği ve geliştirme ekibi zaten Spring’e aşina olduğu için, daha yüksek ve daha erken ortaya çıkan bir üretkenlik sağlayacağından, nihai olarak seçilmiştir. Diğer ORM framework’leri dikkate alınmamıştır; çünkü geliştirme ekibi zaten Hibernate’e aşinaydı ve onun performansından memnundu.

### 4.3.3.4 Adım 5: Mimari Ögeleri Örnekle, Sorumlulukları Ayır ve Arayüzleri Tanımla

Bu yinelemede verilen örnekleme (instantiation) tasarım kararları aşağıdaki tabloda özetlenmektedir:

**Tasarım Kararları ve Konumu** | **Gerekçe**
---|---
Yalnızca başlangıç niteliğinde bir alan modeli oluştur | Birincil kullanım senaryolarında (use case) yer alan varlıkların tanımlanması ve modellenmesi gerekir, ancak tasarımın bu aşamasını hızlandırmak için yalnızca başlangıç niteliğinde bir alan modeli oluşturulur.
Sistem kullanım senaryolarını alan nesnelerine eşle | Alan nesnelerinin başlangıç niteliğinde bir tanımlaması, sistemin kullanım senaryoları analiz edilerek yapılabilir. CRN-3’ü ele almak için, Bölüm 4.2.1’deki tüm kullanım senaryoları için alan nesneleri tanımlanır.
Alan nesnelerini katmanlara dağıtarak katmana özgü, açık bir arayüze sahip modülleri tanımla | Bu teknik, tüm işlevleri (functionalities) destekleyen modüllerin tanımlanmasını garanti eder. Mimar bu görevi sadece birincil kullanım senaryoları için yerine getirecektir. Bu, bir başka ekip üyesinin geri kalan modülleri tanımlamasına olanak tanır; böylece iş ekip üyeleri arasında paylaştırılmış olur. Modül kümesi oluşturulduktan sonra mimar, bu modülleri test etme ihtiyacını fark eder ve burada yeni bir mimari kaygı (architectural concern) tanımlanır: **CRN-4: Modüllerin çoğunluğu birim testi (unit test) ile test edilmelidir.** Bu kaygı yalnızca “modüllerin çoğunluğunu” kapsamaktadır; çünkü kullanıcı arayüzü işlevselliğini gerçekleştiren modüllerin, bağımsız olarak test edilmeleri zordur.

**Tasarım Kararları ve Konumu** | **Gerekçe**
---|---
Modüllerle ilişkili bileşenleri Spring framework kullanarak bağla | Bu framework, tersine denetim (inversion of control, IoC) yaklaşımı kullanır; bu sayede farklı yönlerin (aspects) desteklenmesi ve modüllerin birim testine tabi tutulabilmesi (CRN-4) mümkün olur.
Veri katmanındaki bir modülle framework’leri ilişkilendir | ORM eşlemesi (mapping), veri katmanında yer alan modüllerin içine kapsüllenmiştir. Daha önce seçilmiş olan Hibernate framework’ü bu modüllerle ilişkilendirilir.

Yöntemin bu adımında yapılar ve arayüzler tanımlanır, ancak bunlar bir sonraki adımda kayda geçirilir.

### 4.3.3.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

5. adımda verilen kararlara bir sonuç olarak çeşitli diyagramlar oluşturulur.

- Şekil 4.5, sistem için başlangıç niteliğinde bir alan modelini göstermektedir.

![Şekil 4.5](/home/runner/workspace/scripts/dsa_figs/sekil_4_5.png){width=11.5cm}

- Şekil 4.6, Bölüm 4.2.1’deki kullanım senaryosu modeline göre örneklenen alan nesnelerini göstermektedir.

![Şekil 4.6](/home/runner/workspace/scripts/dsa_figs/sekil_4_6.png){width=11.5cm}

- Şekil 4.7, iş nesnelerinden (business objects) türetilmiş ve birincil kullanım senaryolarıyla ilişkilendirilmiş modülleri içeren bir modül görünümünün (module view) taslağını göstermektedir. Açık arayüzler (explicit interfaces) gösterilmemiştir, ancak bunların var olduğu varsayılmıştır.

![Şekil 4.7](/home/runner/workspace/scripts/dsa_figs/sekil_4_7.png){width=11.22cm}


Şekil 4.7’de tanımlanan ögelerin sorumlulukları, 95. sayfada başlayan tabloda özetlenmektedir.

## 4.3 Tasarım Süreci

```text
0..*

-

Event

Time Server

Region

-

name

generates

deviceName
ipAddress
model

1

-parent

0..* -

date
payload
severity
type
0..*

1..*
acknowledges

1

1

Configuration
-

Performance Data

configurationParameters

-

User

delay: DataSet
jitter: DataSet
offset: DataSet

-

login
password
permissions
type
```

**ŞEKİL 4.5** Başlangıç alan modeli (Anahtar: UML)

```text
«domain object»
Network Status Monitoring

«domain object»
Event history

«domain object»
Fault Detection

responsibilities

responsibilities

responsibilities

UC-1

UC-2

UC-3

«domain object»
Time Server Management

«domain object»
Time Server Configuration

«domain object»
System Access

responsibilities

UC-4

UC-5
UC-6

responsibilities
UC-10

«domain object»
Performance Data and Information Display

«domain object»
Performance and Data Collection

«domain object»
User Management

responsibilities

responsibilities
UC-11

responsibilities

responsibilities
UC-8
UC-9

UC-7
```

**ŞEKİL 4.6** Kullanım senaryosu modeliyle ilişkilendirilmiş alan nesneleri (Anahtar: UML)

> **💬 Çevirmen notu:** “responsibilities” etiketleri, her domain nesnesinin hangi kullanım senaryolarının gerçekleştirilmesinden sorumlu olduğunu gösterir. UC-1, UC-2 vb. kullanım senaryosu (use case) kimlikleridir.

```text
Client Side

«Layer»
Presentation CS

NetworkStatusMonitoringView

«Layer»
Business logic CS

NetworkStatusMonitoringController

«Layer»
Data CS
RequestManager

Server Side

«Layer»
Services SS

«facade»
RequestService

«Layer»
Business Logic SS
TopologyController
DomainEntities

TimeServerEventsController

DataCollectionController

«Layer»
Data SS

RegionDataMapper

TimeServerDataMapper

EventDataMapper

TimeServerConnector
```

**ŞEKİL 4.7** Birincil kullanım senaryolarını destekleyen modüller (Anahtar: UML)

## 4.3 Tasarım Süreci

**Öge** | **Sorumluluk**
---|---
NetworkStatusMonitoringView | Ağ gösterimini (network representation) görüntüler ve olaylar alındığında bu gösterimi günceller. Bu bileşen, başvuru mimarisindeki (reference architecture) hem UI bileşenlerini hem de UI işlem (process) bileşenlerini somutlaştırır.
NetworkStatusMonitoringController |

Sunum katmanına, ağ gösterimini
görüntülemek için gerekli bilgileri
sağlamaktan sorumludur.

**RequestManager**

Sunucu tarafı mantık ile
iletişimden sorumludur.

**RequestService**

İstemcilerden gelen istekleri alan
bir cephe (facade) sağlar.

**TopologyController**

Topolojik bilgiyle ilgili iş
mantığını (business logic) içerir.

**DomainEntities**

Etki alanı modelinden (domain model) kuruluşları (entity) içerir
(sunucu tarafı).

**TimeServerEventsController**

Olayların yönetimiyle ilgili iş
mantığını içerir.

**DataCollectionController**

Veri toplama ve
depolamayı gerçekleştirecek mantığı içerir.

**RegionDataMapper**

Bölgelerle ilgili kalıcılık (persistence)
işlemlerinden (CRUD) sorumludur.

**TimeServerDataMapper**

Zaman sunucularıyla ilgili kalıcılık
işlemlerinden (CRUD) sorumludur.

**EventDataMapper**

Olaylarla ilgili kalıcılık
işlemlerinden (CRUD) sorumludur.

**TimeServerConnector**

Zaman sunucuları ile iletişimden
sorumludur. Farklı türdeki zaman sunucularıyla iletişimi desteklemek için
zaman sunucularıyla yapılan işlemleri
soyutlar ve yalıtır (bkz. QA-2).

---

## 4.3 Tasarım Süreci

Aşağıdaki UC-1 ve UC-2 sıralama (sequence) diyagramları, arayüzleri tanımlamak için yöntemin önceki adımında (Bölüm 3.6’da tartışıldığı gibi) oluşturulmuştur. UC-7 için de benzer bir diyagram oluşturulmuştur, ancak yer kısıtı nedeniyle burada gösterilmemektedir.

### UC-1: Ağ Durumunu İzleme

Şekil 4.8, UC-1 (ağ durumunu izleme) için başlangıç niteliğinde bir sıralama diyagramı göstermektedir. Diyagram, kullanıcı sisteme başarıyla giriş yaptıktan sonra, başlangıçta topolojinin kullanıcı gösteriminin nasıl görüntülendiğini gösterir. Uygulama başlatıldığında, topoloji sunucudaki `TopologyController`dan istenir. Bu öğe, `RegionDataMapper` aracılığıyla kök bölgeyi (root region) alır ve istemciye döndürür. İstemci daha sonra `Region` sınıfı içindeki ilişkileri dolaşarak görünümü doldurabilir.

![Şekil 4.8](/home/runner/workspace/scripts/dsa_figs/sekil_4_8.png){width=11.78cm}


```
Client
:NetworkStatusMonitoringView

Server

:NetworkStatusMonitoringController

:RequestManager

:RequestService

:TopologyController

:RegionDataMapper

Technician

launch()
initialize()
requestTopology()
sendRequest(Request)
requestTopology()
retrieve(id) :Region
:Region
:Region
:Response
:Region
:boolean
getRootRegion() :Region

populateView()

interact()
```

**ŞEKİL 4.8** Kullanım durumu UC-1 için sıralama diyagramı (Anahtar: UML)

Sıralama diyagramında tanımlanan etkileşimlerden, etkileşimde bulunan
öğelerin arayüzleri için başlangıç yöntemleri tanımlanabilir:

---

### 4.3 Tasarım Süreci

#### Yöntem Adı

**Öğe: NetworkStatusMonitoringController**

`boolean initialize()`

Kullanıcıların etkileşimde bulunabilmesi için
ağ gösterimini açar.

`Region getRootRegion()`

Kök bölgeye ve bu nesnenin komşularına (tuzaklar
(traps) hariç) bir başvuru (reference) döndürür.

**Öğe: RequestManager**

`Region requestTopology()`

Topolojiyi ister. Bu yöntem, tüm topolojide
dolaşmanın mümkün olduğu kök bölgeye bir
başvuru döndürür.

**Öğe: RequestService**

`Response sendRequest(Request req)`

Bu yöntem bir isteği alır. Servis arayüzünde
sadece bu yöntem dışa açılmıştır. Bu durum,
mevcut servis arayüzünü değiştirmek zorunda
kalmadan gelecekte diğer işlevleri eklemeyi
kolaylaştırır.

**Öğe: TopologyController**

`Region requestTopology()`

Topolojiyi ister. Bu yöntem, tüm topolojide
dolaşmanın mümkün olduğu kök bölgeye bir
başvuru döndürür.

**Öğe: RegionDataMapper**

`Region retrieve(int id)`

Bir `Region`ı, kimliğinden (id) döndürür.

---

```
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
```

**ŞEKİL 4.9** Kullanım durumu UC-2 için sıralama diyagramı (Anahtar: UML)

### UC-2: Hata Algılama

Şekil 4.9, UC-2 (hata algılama) için başlangıç niteliğinde bir sıralama diyagramı göstermektedir ve sadece sunucu tarafındaki bileşenleri gösterir. Etkileşim, bir `TimeServer`ın bir tuzak (trap) göndermesiyle başlar; bu tuzak `TimeServerConnector` tarafından alınır. Tuzak bir `Event`e dönüştürülür ve `TimeServerConfigurationController`a gönderilir. `Event`, istemcilere yayınlanmak üzere `TopologyController`a eşzamansız (asynchronous) olarak gönderilir ve ardından kalıcı hale getirilir (persist edilir).

![Şekil 4.9](/home/runner/workspace/scripts/dsa_figs/sekil_4_9.png){width=11.89cm}


Bu etkileşimden, etkileşimde bulunan öğelerin arayüzleri için başlangıç
yöntemleri tanımlanabilir:

---

### 4.3 Tasarım Süreci

#### Yöntem Adı

**Öğe: TimeServerConnector**

`boolean addEventListener(EventListener el)`

Bu yöntem, iş mantığındaki bileşenlerin,
zaman sunucularından alınan olaylara dinleyici
(listener) olarak kendilerini kaydetmelerine
olanak tanır.

**Öğe: TimeServerConfigurationController**

`boolean eventReceived(Event evt)`

Bir olay alındığında çağrılan geriçağırım
(callback) yöntemidir.

**Öğe: TopologyController**

`publish(Event evt)`

Bu yöntem, yeni bir olay gerçekleştiğini
istemcilere bildirir.

**Öğe: TimeServerDataMapper**

`TimeServer retrieve(int id)`

Kimliğiyle (id) tanımlanan bir `TimeServer`ı
alır.

`boolean update(TimeServer ts)`

Bir `TimeServer`daki değişiklikleri kalıcı
hale getirir.

---

### 4.3.3.6 Adım 7: Mevcut Tasarımın Analizini Yap ve İterasyonu Gözden Geçir  
Amaç ve Tasarım Amacının Gerçekleşme Düzeyi

Bu iterasyonda alınan kararlar, işlevselliğin sistemde nasıl desteklendiğine dair
başlangıç niteliğinde bir anlayış sağlamıştır. Birincil kullanım durumlarıyla ilişkili modüller mimar tarafından, geri kalan işlevsellikle ilişkili modüller ise ekipteki başka bir üye tarafından tanımlanmıştır. Modüllerin tam listesinden, CRN-3’ü ele almak için bir iş atama tablosu (burada gösterilmemiştir) oluşturulmuştur.

Ayrıca, modül tanımlama çalışmasının bir parçası olarak yeni bir mimari kaygı (architectural concern) tanımlanmış ve Kanban panosuna eklenmiştir. Önceki iterasyonda tamamen ele alınan sürücüler (drivers) tablodan çıkarılmıştır.

---

### 4. Bölüm — FCAPS Sistemi: Vaka Çalışması

|                     | Henüz Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı |
|---------------------|--------------------|-------------------|---------------------|
| **Iterasyon Sırasında Alınan Tasarım Kararları** |                    |                   |                     |
| UC-1                |                    |                   | Katmanlar boyunca modüller ve bu kullanım durumunu destekleyecek ön taslak arayüzler tanımlanmıştır. |
| UC-2                |                    |                   | Katmanlar boyunca modüller ve bu kullanım durumunu destekleyecek ön taslak arayüzler tanımlanmıştır. |
| UC-7                |                    |                   | Katmanlar boyunca modüller ve bu kullanım durumunu destekleyecek ön taslak arayüzler tanımlanmıştır. |
| QA-1                |                    |                   | İlişkili kullanım durumunu (UC-2) destekleyen öğeler tanımlanmıştır. |
| QA-2                |                    |                   | İlişkili kullanım durumunu (UC-5) destekleyen öğeler tanımlanmıştır. |
| QA-3                |                    |                   | İlgili karar alınmamıştır. |
| QA-4                |                    |                   | İlişkili kullanım durumunu (UC-7) destekleyen öğeler tanımlanmıştır. |
| CON-1               |                    |                   | İlgili karar alınmamıştır. |
| CON-4               |                    |                   | İlgili karar alınmamıştır. |
| CON-5               |                    |                   | Verileri toplamaktan sorumlu modüller tanımlanmıştır. |
| CON-6               |                    |                   | Veri depolamadan sorumlu modüller tanımlanmıştır. |
| CRN-2               |                    |                   | Ek teknolojiler, ekibin bilgisi dikkate alınarak tanımlanmış ve seçilmiştir. |
| CRN-3               |                    |                   |  |
| CRN-4               |                    |                   |  |

Modüller, tüm kullanım durumları (use case) ile ilişkilendirilmiş ve bir iş atama matrisi (work assignment matrix) oluşturulmuştur (gösterilmemiştir). Bu yeni yinelemede (iteration) tanıtılan modüllerin birim-testinin (unit testing) yapılmasına yönelik mimari kaygı, modüllerle ilişkili bileşenleri bağlamak için bir kontrolün tersine çevrilmesi (inversion of control) yaklaşımının kullanılmasıyla kısmen çözülmüştür.

## 4.3 Tasarım Süreci

### 4.3.4 Yineleme 3: Kalite Niteliği Senaryosu Sürücüsünün (QA-3) Ele Alınması

Bu bölüm, tasarım sürecinin üçüncü yinelemesinde nitelik temelli tasarımın (Attribute-Driven Design, ADD) her bir adımında gerçekleştirilen etkinliklerin sonuçlarını sunmaktadır. 1. ve 2. yinelemede alınan temel yapısal kararlara dayanarak artık en önemli bazı kalite niteliklerinin (quality attribute) yerine getirilmesi üzerinde düşünmeye başlayabiliriz. Bu yineleme, bu kalite niteliği senaryolarından yalnızca birine odaklanmaktadır.

#### 4.3.4.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu yineleme için mimar, QA-3 kalite niteliği senaryosuna odaklanmaktadır:

> Çalışma sırasında yönetim sisteminde bir arıza oluşur. Yönetim sistemi 30 saniyeden kısa sürede çalışmaya devam eder.

#### 4.3.4.2 Adım 3: Ayrıntılandırmak Üzere Sistemden Bir veya Daha Fazla Eleman Seçme

Bu kullanılabilirlik (availability) senaryosu için ayrıntılandırılacak elemanlar, birinci yineleme sırasında belirlenen fiziksel düğümlerdir:

- Uygulama sunucusu (application server)  
- Veritabanı sunucusu (database server)

#### 4.3.4.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı Seçme

Bu yinelemede kullanılan tasarım kavramları aşağıdaki gibidir:

| Tasarım Kararları ve Yeri | Gerekçe ve Varsayımlar |
| --- | --- |
| Uygulama sunucusunu ve veritabanı gibi diğer kritik bileşenleri çoğaltarak aktif yedeklilik (active redundancy) taktiğini tanıt | Kritik elemanlar çoğaltılarak (replication) sistem, çoğaltılan elemanlardan birinin arızasına işlevselliği etkilemeden dayanabilir. |
| Mesaj kuyruğu (message queue) teknoloji ailesinden bir eleman tanıt | Zaman sunucularından alınan tuzaklar (trap), mesaj kuyruğuna yerleştirilir ve sonra uygulama tarafından alınır. Kuyruğun kullanılması, tuzakların QA-1’deki gibi sırayla işlenmesini ve iletilmesini garanti edecektir. |

#### 4.3.4.4 Adım 5: Mimari Elemanları Örnekle, Sorumlulukları Tahsis Et ve Arayüzleri Tanımla

Örnekleme (instantiation) tasarım kararları aşağıdaki tabloda özetlenmiştir:

| Tasarım Kararları ve Yeri | Gerekçe |
| --- | --- |
| Mesaj kuyruğunu ayrı bir düğüme yerleştir (deploy) | Mesaj kuyruğunun ayrı bir düğüme yerleştirilmesi, bir uygulama arızası durumunda hiçbir tuzağın kaybolmamasını garanti edecektir. Bu düğüm, aktif yedeklilik taktiği kullanılarak çoğaltılır; ancak ağ cihazlarından gelen olayları yalnızca bir kopya alır ve işler. |
| Uygulama sunucusunda aktif yedeklilik ve yük dengeleme (load balancing) kullan | Herhangi bir anda iki uygulama sunucusu kopyası etkin olduğundan, yükü kopyalar arasında dağıtmak ve dengelemek mantıklıdır. Bu taktik, Yük Dengeli Küme (Load-Balanced Cluster) deseninin (pattern) kullanımıyla elde edilebilir (Bkz. Bölüm A.2.3). Bu, yeni bir mimari kaygıyı, CRN-5’i tanıtır: Kopyalarda durumu yönet (Manage state in replicas). |
| Yük dengeleme ve yedekliliği teknolojik destek kullanarak gerçekleştir | Yük dengeleme ve yedekliliğe yönelik birçok teknolojik seçenek, daha az olgun ve desteklenmesi daha zor olacak özel geliştirilmiş (ad hoc) bir çözüme gerek kalmadan uygulanabilir. |

Bu örnekleme kararlarının sonuçları bir sonraki adımda kaydedilmektedir.

#### 4.3.4.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 4.10, sisteme yedekliliğin eklenmesini içeren ayrıntılandırılmış (refined) bir dağıtım diyagramı (deployment diagram) göstermektedir.

![Şekil 4.10](/home/runner/workspace/scripts/dsa_figs/sekil_4_10.png){width=11.82cm}


```text
Server1 :ApplicationServer
«JDBC»
«replicated»
:LoadBalancer

pc :UserWorkstation

«replicated»
:Database Server

«HTTP»

«JDBC»

Server2 :ApplicationServer

«replicated»
:TrapReceiver
device1 :TimeServer
Relocatable IP address

FIGURE 4.10 Refined deployment diagram (Key: UML)

«SNMP»
```

Aşağıdaki tablo, daha önce (1. yinelemede) listelenmemiş elemanlara yönelik sorumlulukları açıklamaktadır:

| Eleman | Sorumluluk |
| --- | --- |
| LoadBalancer | İstemcilerden gelen istekleri uygulama sunucularına aktarır (ve yükü dengeler). Yük dengeleyici ayrıca istemcilere tekil bir IP adresi sunar. |
| TrapReceiver | Ağ cihazlarından tuzakları alır, bunları olaylara dönüştürür ve bu olayları kalıcı bir mesaj kuyruğuna koyar. |

Şekil 4.11’de gösterilen UML sıra diyagramı (sequence diagram), bu yinelemede tanıtılan TrapReceiver’ın, UC-2’yi (arızayı algıla — detect fault) desteklemek üzere dağıtım diyagramında gösterilen diğer elemanlarla nasıl mesaj alışverişi yaptığını göstermektedir. UC-2 hem QA-3 (kullanılabilirlik) hem de QA-1 (performans) ile ilişkilidir. Bu diyagramın amacı, fiziksel düğümler arasında gerçekleşen iletişimi göstermek olduğundan, metot isimleri yalnızca ön taslak niteliğindedir; sonraki yinelemelerde ayrıntılandırılacaktır.

![Şekil 4.11](/home/runner/workspace/scripts/dsa_figs/sekil_4_11.png){width=11.82cm}


```text
:NetworkDevice

:TrapReceiver

:ApplicationServer

pc :UserWorkstation

trap()

transformAndEnqueue(Event)
consume()
event()
publish(Event)

updateView()

FIGURE 4.11 Sequence diagram illustrating the messages exchanged between
the physical nodes to support UC-2 (Key: UML)
```

### 4.3.4.6 Adım 7: Mevcut Tasarımın Analizini Gerçekleştir ve Yineleme Hedefini ve Tasarım Amacının Gerçekleşmesini Gözden Geçir

Bu yinelemede QA-3’ü ele almak için önemli tasarım kararları alınmış ve bu kararlar QA-1’i de etkilemiştir. Aşağıdaki tablo, farklı sürücülerin durumunu ve yineleme boyunca alınan kararları özetlemektedir. Önceki yinelemede tamamen ele alınmış olan sürücüler tablodan çıkarılmıştır.

| Sürücü | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Boyunca Alınan Tasarım Kararları |
| --- | :---: | :---: | :---: | --- |
| QA-1 |  | X |  | Ayrı bir çoğaltılmış tuzak alıcı (trap receiver) düğümünün tanıtılması, uygulama sunucusunda bir arıza olması durumunda bile tuzakların %100’ünün işlenmesine yardımcı olabilir. Ayrıca, tuzak alımı ayrı bir düğümde gerçekleştirildiğinden, bu yaklaşım uygulama sunucusu işlem yükünü azaltır ve böylece performansa yardımcı olur. Belirli teknolojiler henüz seçilmediğinden, bu sürücü “kısmen ele alındı” olarak işaretlenmiştir. |
| QA-2 | X |  |  | İlgili bir karar alınmamıştır. |
| QA-3 |  | X |  | Uygulama sunucusunu yedekli hale getirerek sistemin arıza olasılığını azaltıyoruz. Ayrıca, yük dengeleyici arızalanırsa, pasif bir kopya gereken süre içinde etkinleştirilir. Belirli teknolojiler (örneğin mesaj kuyruğu) henüz seçilmediğinden, bu sürücü “kısmen ele alındı” olarak işaretlenmiştir. |
| QA-4 | X |  |  | İlgili bir karar alınmamıştır. |
| CON-1 |  |  | X | Uygulama sunucusunun çoğaltılması ve bir yük dengeleyicinin kullanılması, birden çok kullanıcı isteğinin desteklenmesine yardımcı olacaktır. |
| CON-4 | X |  |  | İlgili bir karar alınmamıştır. |
| CON-5 | X |  |  | İlgili bir karar alınmamıştır. |
| CON-6 | X |  |  | İlgili bir karar alınmamıştır. |
| CRN-2 | X |  |  | İlgili bir karar alınmamıştır. |
| CRN-4 | X |  |  | İlgili bir karar alınmamıştır. Bu yeni mimari kaygı bu yinelemede tanıtılmaktadır: kopyalarda durumu yönet (manage state in replicas). Bu noktada, ilgili bir karar alınmamıştır. |

## 4.4 Özet

> **💬 Çevirmen notu:** QA-* (quality attribute), CON-* (constraint — kısıt) ve CRN-* (concern — mimari kaygı) etiketleri, mimari sürücüleri sınıflandırmak için kullanılan adlandırma şemasıdır; ilerideki bölümlerde bu şema üzerine tekrar dönülmektedir.

Bu bölümde, olgun bir alanda sıfırdan geliştirilen (greenfield) bir sistemin tasarımında ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) kullanımına dair bir örnek sunduk. Üç yinelemeyi, farklı odaklarla birlikte gösterdik: genel bir kaygının ele alınması, işlevselliğin ele alınması ve bir temel kalite niteliği senaryosunun ele alınması.

Örnek, Bölüm 3.3.1’de tartışılan yol haritasını izledi. İlk yinelemede, sistemi yapılandırmak için iki farklı referans mimarinin (reference architecture) kullanılmış olmasını gözlemlemek ilginçtir. Ayrıca, harici olarak geliştirilmiş bileşenlerin—bu durumda çatıların (framework)—seçimi farklı yinelemelere yayılmıştır. Son olarak örnek, tasarım ilerledikçe yeni mimari kaygıların nasıl ortaya çıktığını göstermektedir.

Bu örnek, mimari kaygıların, birincil kullanım durumlarının (primary use cases) ve kalite niteliği senaryolarının (quality attribute scenario) mimari tasarımın bir parçası olarak nasıl ele alınabileceğini göstermektedir. Gerçek bir sistemde, yüksek öncelikli diğer senaryoları ele alarak tam bir mimari tasarım elde etmek için daha fazla yineleme gerekli olacaktır.

Bu örnekte, mimarın tasarım sırasında bir CASE aracı kullandığı varsayılmıştır; bu nedenle diyagramlar UML kullanılarak üretilmiştir. Bunun kesinlikle zorunlu olmadığını, Bölüm 5’te sunulan vaka çalışmasında göreceğiz. Ayrıca, tasarım sürecinin bir parçası olarak üretilen bilgileri kullanarak taslak görünüm eskizleri (preliminary view sketches) üretmenin görece basit olduğuna dikkat edin.

## 4.5

Ek Okumalar

Ek A, bu vaka çalışmasında kullanılan tüm tasarım kavramlarının açıklamalarını ve bibliyografik atıflarını sağlar.

---

# 5  
Vaka Çalışması: Büyük Veri Sistemi

Serge Haziyev ve Olha Hrytsay ile birlikte

Şimdi, zorlayıcı bir alan olan Büyük Veri (Big Data) için, sıfırdan geliştirilen (greenfield) bir sistemde ADD 3.0 kullanımına ilişkin kapsamlı bir tasarım örneği sunuyoruz. Bu metnin yazıldığı sırada, bu alan görece yeniydi ve hızla evrim geçiriyordu. Bu nedenle, mimarlar yalnızca geçmiş deneyimlerine güvenerek ilerleyemezlerdi. Bunun yerine, tasarım sürecini dönemsel analizler ve stratejik prototipleme (strategic prototyping) ile tamamladılar; bunu şimdi açıklayacağız.

## 5.1

İş Gerekçesi (Business Case)

Bu vaka çalışması, milyonlarca web kullanıcısına popüler içerik ve çevrimiçi hizmetler sunan bir İnternet şirketini kapsamaktadır. Şirket, dışarıya bilgi sağlamanın yanında, altyapısından üretilen (örneğin uygulama ve sunucu günlükleri, sistem metrikleri) çok büyük hacimde günlük (log) verisini toplar ve analiz eder. Bilgisayar tarafından üretilen günlük mesajlarıyla bu şekilde başa çıkma yaklaşımı, günlük yönetimi (log management, bkz. http://en.wikipedia.org/wiki/Log_management_and_intelligence) olarak da adlandırılır.

Çok hızlı altyapı büyümesi nedeniyle, şirketin BT departmanı mevcut kurum içi sistemlerin artık gerekli günlük veri hacmini ve hızını işleyemediğini fark etmektedir. Ayrıca, yeni bir sisteme yönelik talepler, sadece günlüklerden değil, birden çok veri kaynağından toplanabilecek çeşitli veri türlerini kullanmak isteyen ürün yöneticileri ve veri bilimcileri gibi diğer şirket paydaşlarından da gelmektedir.

Şekil 5.1’de gösterilen piyasa-mimari diyagramı (marketecture diagram, sistem yapısının gayriresmî betimi), üç ana kullanıcı grubuna yönelik olarak istenen çözümü işlevsel bir bakış açısından göstermektedir.

![Şekil 5.1](/home/runner/workspace/scripts/dsa_figs/sekil_5_1.png){width=9.98cm}


- Gerçek zamanlı izleme  
- Tam metin arama  
- Anomali tespiti  

Web Sunucuları  
- Yüzlerce sunucu  
- Birden çok kaynaktan gelen  
  çok büyük günlükler  

- Ham ve birleştirilmiş tarihsel veriler  
- Ad hoc analiz  
- Gerçek zamanlı sorgular  

Gerçek Zamanlı  
Gösterge Paneli (Dashboard)  

7/24 Operasyon,  
Destek Mühendisleri,  
Geliştiriciler  

Ad Hoc  
Raporlar  

Veri Bilimciler /  
Analistler  

- Gerçeğe yakın zamanlı statik raporlar  
- Kurumsal BI aracılığıyla erişilebilir  

Statik Raporlar  

Yönetim  

**Şekil 5.1** Büyük Veri sistemi için piyasa-mimari (marketecture) diyagramı

## 5.2

Sistem Gereksinimleri

Gereksinim çıkarım (requirement elicitation) faaliyetleri daha önce gerçekleştirilmiştir. Toplanan en önemli gereksinimler burada özetlenmiştir. Bunlar, birincil kullanım durumlarından oluşan bir küme, kalite niteliği senaryolarından oluşan bir küme, kısıtlardan oluşan bir küme ve mimari kaygılardan oluşan bir kümeden meydana gelir.

### 5.2.1

Kullanım Durumu Modeli (Use Case Model)

Sistemin birincil kullanım durumları aşağıdaki tabloda açıklanmaktadır.

| Kullanım Durumu | Açıklama |
| --- | --- |
| **UC-1: Çevrimiçi hizmetleri izleme** | Nöbetçi operasyon personeli, gerçek zamanlı bir operasyon gösterge paneli aracılığıyla hizmetlerin ve BT altyapısının (örneğin web sunucu yükü, kullanıcı aktiviteleri ve hatalar) mevcut durumunu izleyebilir; bu panel onların sorunlara hızla tepki vermelerini sağlar. |
| **UC-2: Çevrimiçi hizmet sorunlarını giderme** | Operasyon, destek mühendisleri ve geliştiriciler, günlük örüntülerini arayarak ve günlük mesajlarını filtreleyerek en son toplanan günlükler üzerinde sorun giderme (troubleshooting) ve kök neden analizi (root-cause analysis) yapabilir. |
| **UC-3: Yönetim raporları sağlama** | BT ve ürün yöneticileri gibi kurumsal kullanıcılar, sistem yükünün zamana göre değişimi, ürün kullanımı, hizmet seviyesi anlaşması (service level agreement, SLA) ihlalleri ve sürümlerin kalitesi gibi bilgileri gösteren, kurumsal bir BI (business intelligence, iş zekâsı) aracı içindeki önceden tanımlanmış (statik) raporlar aracılığıyla tarihsel bilgiyi görüntüleyebilir. |
| **UC-4: Veri analitiğini destekleme** | Veri bilimciler ve analistler, ham ve birleştirilmiş tarihsel veriler üzerinde belirli veri örüntülerini ve korelasyonları bulmak için, altyapı kapasite planlamasını ve müşteri memnuniyetini iyileştirmeye yönelik SQL-benzeri sorgularla ad hoc veri analizi yapabilir. |
| **UC-5: Anomali tespiti** | Operasyon ekibi, sistemin herhangi bir alışılmadık davranışı konusunda 7/24 bilgilendirilmelidir. Bu bildirim planını desteklemek için sistem, gerçek zamanlı anomali tespiti ve uyarı mekanizmasını uygulamalıdır (gelecek gereksinim). |
| **UC-6: Güvenlik raporları sağlama** | Güvenlik analistlerine, hedef ve kaynak adresleri, zaman damgası ve kullanıcı oturum açma bilgilerini içeren denetim günlük girdilerini (audit log entries) inceleyerek potansiyel güvenlik ve uyum (compliance) sorunlarını araştırma imkânı sağlanmalıdır (gelecek gereksinim). |

### 5.2.2

Kalite Niteliği Senaryoları

En ilgili kalite niteliği (ham) senaryoları aşağıdaki tabloda sunulmuştur. Her senaryo için, ilişkilendirildiği kullanım durumunu da tanımlıyoruz.

| ID | Kalite Niteliği | Senaryo | İlgili Kullanım Durumu(ları) |
| --- | --- | --- | --- |
| **QA-1** | Performans | Sistem, yaklaşık 300 web sunucusundan saniyede 15.000 olaya kadar veri toplamalıdır. | UC-1, UC-2, UC-5 |
| **QA-2** | Performans | Sistem, nöbetçi operasyon personeli için gerçek zamanlı izleme gösterge panelini < 1 dakikalık gecikmeyle (latency) otomatik olarak yenilemelidir. | UC-1 |
| **QA-3** | Performans | Sistem, son 2 haftalık veriler için, acil durum sorun giderme amacıyla gerçek zamanlı arama sorguları sağlamalı ve sorgu yürütme süresi < 10 saniye olmalıdır. | UC-2 |
| **QA-4** | Performans | Sistem, iş kullanıcıları için dakika başına birleştirme (aggregation) sağlayan gerçeğe yakın zamanlı statik raporları < 15 dakikalık gecikmeyle ve < 5 saniyelik rapor yükleme süresiyle sağlamalıdır. | UC-3, UC-6 |
| **QA-5** | Performans | Sistem, ham ve birleştirilmiş tarihsel veriler üzerinde, önceden tanımlı olmayan (ad hoc) SQL-benzeri, insan-zamanı (human-time) sorgularını < 2 dakikalık sorgu yürütme süresiyle sağlamalıdır. Sonuçlar, sorgulama için < 1 saat içinde kullanılabilir olmalıdır. | UC-4 |
| **QA-6** | Ölçeklenebilirlik (Scalability) | Sistem, acil durum sorun giderme için (günlükler üzerinde tam metin arama yoluyla) erişilebilir olacak şekilde, son 2 haftanın ham verisini depolamalıdır. | UC-2 |
| **QA-7** | Ölçeklenebilirlik (Scalability) |  |  |

> **💬 Çevirmen notu:** “Human-time query” ifadesi, sistemin yüksek hacimli veriye rağmen, sorgu yanıt sürelerinin insanın bekleyebileceği makul sürelerde kalmasını vurgular; burada “insan-zamanı” ibaresi bu vurguyu yansıtmak için korunmuştur.

Sistem son 60 güne ait ham veriyi saklamalıdır (günde yaklaşık 1 TB ham veri, toplamda yaklaşık 60 TB).

UC-4

Senaryo

İlgili
Kullanım Durumu

(devamı)

110

Bölüm 5—Vaka Çalışması: Büyük Veri Sistemi

ID

Kalite
Niteliği

Senaryo

İlgili
Kullanım Durumu

QA-8

Ölçeklenebilirlik (scalability)

Sistem, 1 yıl boyunca dakika bazında
toplanmış (aggregate) veriyi (yaklaşık
40 TB) ve 10 yıl boyunca saat bazında
toplanmış veriyi (yaklaşık 50 TB) saklamalıdır.

UC-3, 4, 6

QA-9

Genişletilebilirlik (extensibility)

Sistem, yeni veri kaynaklarının sadece
bir yapılandırma güncellenerek, devam
eden veri toplama işlemini kesintiye
uğratmadan eklenmesini desteklemelidir.

UC-1, 2, 5

QA-10

Kullanılabilirlik (availability)

Sistem, herhangi bir tekil düğüm veya
bileşen arızalandığında kesinti olmaksızın çalışmaya devam etmelidir.

Tüm
kullanım
durumları

QA-11

Konuşlandırılabilirlik (deployability)

Sistemin konuşlandırma prosedürü
tamamen otomatikleştirilmeli ve geliştirme, test ve üretim ortamları gibi bir
dizi ortamı desteklemelidir.

Tüm
kullanım
durumları

### 5.2.3 Kısıtlar (constraints)

Sistemle ilişkili kısıtlar aşağıdaki tabloda sunulmaktadır.

ID  

Kısıt

CON-1

Sistem esas olarak (maliyet nedenleriyle) açık kaynak teknolojilerden
oluşmalıdır. Özel mülkiyet (proprietary) teknoloji kullanmanın değer/
maliyet oranının çok daha yüksek olduğu bileşenler için, özel mülkiyet
teknolojisi kullanılabilir.

CON-2

Sistem, statik raporlar için (örneğin, MicroStrategy, QlikView, Tableau)
SQL arabirimli kurumsal BI (iş zekâsı) aracını kullanmalıdır.

CON-3

Sistem iki belirli konuşlandırma ortamını desteklemelidir:
özel bulut (VMware vSphere Hypervisor ile) ve genel bulut
(Amazon Web Services). Konuşlandırma sağlayıcısını mümkün olduğunca
bağımsız (vendor-agnostic) tutmak için mimari ve teknoloji kararları
buna göre verilmelidir.

### 5.2.4 Mimari Kaygılar (architectural concerns)

Ele alınan başlangıç mimari kaygılar aşağıdaki tabloda gösterilmiştir.

ID  

Kaygı

CRN-1

Bu bir sıfırdan geliştirilen (greenfield) sistem olduğundan, başlangıç
için genel bir yapı oluşturulması.

CRN-2

Ekibin Apache Büyük Veri ekosistemi konusundaki bilgisinden
yararlanma.

## 5.3 Tasarım Süreci

111

### 5.3 Tasarım Süreci

Gereksinimleri sıraladığımıza göre, şimdi ADD (Attribute-Driven Design, nitelik temelli tasarım) yönteminin ilk yinelemesine başlamaya hazırız. Bu, nispeten yeni bir alanda, sıfırdan geliştirilen bir sistemdir. Bu nedenle, olgun alanlardaki sıfırdan sistemler için tasarım yol haritasını (Bölüm 3.3.1’de tartışıldığı gibi) izliyoruz; ancak Büyük Veri alanına özgü, teknolojilerin hızlı ortaya çıkışı ve evrimi gibi belirsizlikleri ele almak için bazı uyarlamalarla.

#### 5.3.1 ADD Adım 1: Girdileri Gözden Geçirme

Yöntemin ilk adımı girdilerin gözden geçirilmesini içerir. Bunlar aşağıdaki tabloda özetlenmiştir.

Kategori  

Ayrıntılar

Tasarım
amacı

Bu, nispeten yeni bir alandaki sıfırdan (greenfield) bir sistemdir. Kuruluş, geliştiricilerin gerçek dünyadan hızlı biçimde geri bildirim alıp sistemi değiştirmeye devam edebilmesi için kısa yinelemeli çevik (Agile) bir süreç izleyecektir. Aynı zamanda, mimari sürücüleri (architectural driver) karşılamaya yönelik bilinçli kararlar vermek ve gereksiz yeniden çalışmayı (rework) önlemek için bir mimari tasarıma ihtiyaç vardır.

Birincil
işlevsel
gereksinimler

Bölüm 5.2.1’de sunulan kullanım durumları arasından aşağıdakiler
birincil olarak belirlenmiştir:
- UC-1  
- UC-2  
- UC-3  
- UC-4  

Kalite
niteliği
senaryoları

Aşağıdaki tablo, birincil kalite niteliği (quality attribute) senaryolarının, müşteri ve mimar tarafından sıralanan önceliklerini (Bölüm 3.3.2’de tartışıldığı gibi) göstermektedir. Daha düşük öncelikli kalite niteliği senaryolarının da mevcut olduğuna dikkat edin, fakat burada gösterilmemiştir.

Senaryo
ID

Müşteri
İçin Önem

Mimarın Değerlendirmesine Göre
Gerçekleştirme Zorluğu

QA-1

Yüksek

Yüksek

QA-2

Yüksek

Orta

QA-3
QA-4
QA-5
QA-6
QA-7
QA-8
QA-9
QA-10

Orta
Yüksek
Orta
Orta
Orta
Yüksek
Yüksek
Yüksek

Orta
Yüksek
Yüksek
Orta
Orta
Orta
Orta
Orta

QA-11

Orta

Yüksek
(devamı)

112

Bölüm 5—Vaka Çalışması: Büyük Veri Sistemi

Kategori  

Ayrıntılar

Kısıtlar

Bkz. Bölüm 5.2.3.

Mimari
kaygılar

Bölüm 5.2.4’te sunulan mimari kaygıların tümü sürücü (driver)
olarak dâhil edilmiştir.

> **💬 Çevirmen notu:** Burada “sürücü (driver)” terimi, mimariyi yönlendiren gereksinim, kısıt ve kaygıları ifade eden “architectural driver” kavramının kısaltılmış kullanımıdır.

### 5.3.2 Yineleme 1: Referans Mimari ve Genel Sistem Yapısı

Bu bölüm, tasarım sürecinin ilk yinelemesinde ADD yönteminin her adımında gerçekleştirilen faaliyetlerin sonuçlarını sunmaktadır.

#### 5.3.2.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu, sıfırdan geliştirilen bir sistemin tasarımındaki ilk yinelemedir; dolayısıyla yinelemenin hedefi, sistem için başlangıç niteliğinde genel bir yapı oluşturmaktır (CRN-1). Bu ilk yineleme genel bir mimari kaygı tarafından yönlendiriliyor olsa da, mimar tüm sürücüleri, özellikle de kısıtları ve kalite niteliklerini aklında tutmalıdır:

- CON-1: Uygun olduğu her durumda açık kaynak teknolojilerden yararlan  
- CON-2: Statik raporlar için SQL arabirimli kurumsal BI aracını kullan  
- CON-3: İki konuşlandırma ortamı: özel ve genel bulutlar  
- QA-1, 2, 3, 4, 5: Performans  
- QA-6, 7, 8: Ölçeklenebilirlik  
- QA-9: Genişletilebilirlik  
- QA-10: Kullanılabilirlik  
- QA-11: Konuşlandırılabilirlik  

#### 5.3.2.2 Adım 3: Sistemin Ayrıntılandırılacak Bir veya Daha Fazla Ögesini Seçme

Yine, bu bir sıfırdan geliştirme (greenfield development) olduğundan ve başlangıç yinelemesinde bulunduğumuzdan, ayrıntılandırılacak öge tüm sistemdir.

#### 5.3.2.3 Adım 4: Seçilen Sürücüleri Karşılayacak Bir veya Daha Fazla Tasarım Kavramı Seçme

Bu yinelemede tasarım kavramları, çeşitli veri analitiği referans mimarilerinden seçilmektedir (bu tür referans mimarilerin bir listesi, Smart Decisions Game tasarım kavramları kataloğunda bulunabilir; daha fazla bilgi için “Daha Fazla Okuma” bölümüne bakınız).

## 5.3 Tasarım Süreci

Tasarım
Kararları ve
Konumu

Uygulamayı
Lambda
(referans)
mimarisinin
bir örneği
(instance) olarak
inşa et

### Gerekçe

Şekil 5.2’de gösterilen Lambda mimarisi (Lambda architecture), bir referans mimaridir ve bir veri akışının işlenmesini iki akışa ayırır: gerçek zamanlı veriye erişimi destekleyen “hız katmanı (speed layer)” (UC-1, UC-2, UC-5) ve “batch” ile “serving” katmanlarını bir araya toplayan ve tarihsel veriye erişimi destekleyen katman (UC-3, UC-4, UC-6). (Lambda mimarisinin yaratıcıları bunlara “katman (layer)” der, ancak bu, terimin daha önceki ve daha standart kullanımlarından farklıdır; önceki kullanımlar tipik olarak modüllerin bir gruplamasına karşılık gelir. Burada katmanlar, çalışma zamanı bileşenlerinin (runtime components) gruplarıdır.)

![Şekil 5.2](/home/runner/workspace/scripts/dsa_figs/sekil_5_2.png){width=11.85cm}


Batch katmanı değiştirilemez (immutable) ilişkisel olmayan tekniklere dayanırken, hız katmanı sıkı gerçek zamanlı işleme gereksinimlerini desteklemek için akış (streaming) tekniklerine dayanır. Buradaki değiştirilemezlik, verinin toplandığında güncellenmediği veya silinmediği anlamına gelir; yani yalnızca ekleme yapılabilir (append-only). Tüm veri toplandığı için hiçbir veri kaybolamaz ve makine veya insan hatası tolere edilebilir. Örneğin, bir yazılım mühendisi işleme veya görüntüleme mantığında zaman zaman bir hata yaparsa, bu sorun çözüldüğünde toplanan veri kullanılarak görünümler (views) baştan tekrar oynatılabilir ve yeniden hesaplanabilir.

Okuyucunun rahatlığı için Lambda mimarisinin temel kavramlarını beş adım üzerinden açıklıyoruz:

1. Birden çok veri kaynağından alınan tüm veriler, işlenmek üzere veri akışı (data stream) bileşeni aracılığıyla hem batch katmanına hem de hız katmanına yönlendirilir.
2. Batch katmanı, master veri kümesi (master dataset) bileşenine karşılık gelen bir “iniş bölgesi” (landing zone) olarak davranır (değiştirilemez, yalnızca ekleme yapılan ham veri kümesi) ve ayrıca batch görünümlerinde kullanılacak bilgileri önceden hesaplar.
3. Serving katmanı, çoğunlukla raporlama çözümleri tarafından gerekli olan düşük gecikmeli sorgulama için optimize edilmiş, önceden hesaplanmış ve birleştirilmiş (aggregated) görünümler içerir.
4. Hız katmanı, batch işlemenin yüksek gecikmesi nedeniyle serving katmanında bulunmayan gerçek zamanlı görünümler (real-time views) aracılığıyla en son veriyi işler ve erişilebilir kılar.
5. Sistem içindeki tüm veri, ister tarihsel ister yeni olsun, sorgulanabilir durumdadır ve bu, Lambda mimarisinin temel ilkesini ifade eder: query = function (batch data + real-time data).

Paralel akışlar “karmaşıklık yalıtımı (complexity isolation)” sağlar; yani her bir akışın tasarım kararları, geliştirilmesi ve icrası bağımsız olarak yapılabilir. Bunun hata toleransını (fault tolerance), ölçeklenebilirliği (scalability) ve değiştirilebilirliği (modifiability) artırdığı gösterilmiştir (bkz. Tablo 5.1).

Şekil 5.3, bu alternatifler arasındaki mimari ödünleşimleri (architectural tradeoff) gösterir ve referans mimariler arasındaki farkları dört nitelik boyutu açısından ortaya koyar: ölçeklenebilirlik, ad hoc analiz desteği, yapılandırılmamış veri işleme yetenekleri ve gerçek zamanlı analiz yetenekleri.

![Şekil 5.3](/home/runner/workspace/scripts/dsa_figs/sekil_5_3.png){width=11.82cm}


Şekil 5.3’ün gösterdiği üzere, Lambda mimarisi, ölçeklenebilirlik ve ad hoc analiz arasında en iyi ödünleşimi sağlar.

---

### Tasarım Kararı ve Yeri  
Sistem içindeki tüm elemanlar için hata toleransı kullan ve “tekil hata noktası yoktur (no single point of failure)” ilkesini uygula

#### Gerekçe

Hata toleransı, çoğu Büyük Veri (Big Data) teknolojisi için artık standart hâle gelmiştir ve Lambda mimarisi, yukarıda belirtildiği gibi, sağlam ve hata toleranslı bir sistem kurmak için bir dizi tasarım kararını zaten ima eder.

Bununla birlikte, sonraki tüm tasarım ve dağıtım (deployment) kararlarında, tüm aday teknolojilerin, hata toleranslı yapılandırmalar sağlayarak ve “tekil hata noktası yoktur (no single point of failure)” ilkesine uyarak QA-10 gereksinimini destekleyeceğinden emin olmamız gerekecektir.

---

### Alternatifler ve Elenme Nedenleri

| Alternatif            | Elenme Nedeni |
|-----------------------|---------------|
| Geleneksel ilişkisel (traditional relational) | Bu referans mimarisi, karmaşık ad hoc okuma sorguları için son derece verimli kabul edilen geleneksel ilişkisel model ilkelerine ve SQL-tabanlı VTYS’lere (DBMS) dayanır. Ancak ölçeklenebilirlik ve gerçek zamanlı işleme sınırlamaları nedeniyle en az uygun alternatiftir. |
| Genişletilmiş ilişkisel (extended relational) | Bu referans mimarisi tamamen ilişkisel model ilkelerine ve SQL-tabanlı VTYS’lere dayansa da, ölçeklenebilirlik ve genişletilebilirliği artırmak için yoğun biçimde büyük ölçekli paralel işleme (massive parallel processing, MPP) ve bellek içi (in-memory) teknikler kullanır. Yüksek maliyeti ve gerçek zamanlı işleme sınırlamaları nedeniyle daha az uygundur. |
| Saf ilişkisel olmayan (pure nonrelational) | Bu referans mimarisi, ilişkisel model ilkelerine dayanmaz. Sıklıkla NoSQL ve MapReduce gibi teknikler üzerine kuruludur ve yarı yapılandırılmış (semistructured) ve yapılandırılmamış veriyi işleme konusunda etkilidir. Bu alternatif, maliyet ekonomisi ve ölçeklenebilirlik açısından hedefe daha yakın olsa da ad hoc analiz sınırlıdır. |
| Veri rafinerisi (data refinery) | İlişkisel olmayan bir bileşen, yarı yapılandırılmış/yapılandırılmamış veriyi arıtmak için bir extract–transform–load (ETL) süreci yürütür ve temizlenmiş hâlini daha ileri analiz için bir veri ambarına (data warehouse; ilişkisel veritabanı) yükler. Bu çözüm için, yüksek maliyeti ve gerçek zamanlı işleme yetenekleri açısından önemli eksiklikleri nedeniyle daha az uygundur. |

---

## 5.3 Tasarım Süreci

### BATCH Katmanı – SERVING Katmanı – SPEED Katmanı

(Şekil 5.2 Lambda Mimarisi’ni göstermektedir; metin içinde anlatıldığından şekil içeriği ayrıca çevrilmemiştir.)

> **💬 Çevirmen notu:** Şekil 5.3’teki diyagram, metindeki nitelik boyutlarını (ölçeklenebilirlik, ad hoc analiz, yapılandırılmamış veri işleme, gerçek zamanlı analiz) eksenler ve renklerle karşılaştırmalı olarak gösteriyor; metindeki açıklama bu görseli sözel olarak özetlemektedir.

---

## 5.3.2.4 Adım 5: Mimari Elemanları Örnekle, Sorumlulukları Ata ve Arayüzleri Tanımla

Örnekleme (instantiation) ile ilgili ele alınan ve verilen tasarım kararları aşağıdaki tabloda özetlenmiştir.

### Tasarım Kararı ve Yeri  
Sorgu ve Raporlama (Query and Reporting) bileşenini, sürücülerle (drivers) ilişkilendirilmiş iki alt bileşene böl

#### Gerekçe

Lambda mimarisindeki Sorgu ve Raporlama bileşeni (Query and Reporting element), aşağıdaki iki alt bileşene ayrılmıştır. Bu alt bileşenler, ilgili sürücülerle şu şekilde ilişkilendirilir:

- Kurumsal BI aracı (Corporate BI tool) (UC-3, UC-4, QA-4, QA-5, CON-2)  
- Gösterge paneli/görselleştirme aracı (Dashboard/visualization tool) (UC-1, UC-2, QA-2, QA-3)

Bu ayrım, alana (domain) ilişkin bilgi ve araçların kullanılabilirliği tarafından yönlendirilmiştir. Rehber niteliğindeki gerekçe, uygun teknolojileri seçmede esnekliğe sahip olmaktır — bu kullanım senaryalarının, kısıtların ve kalite niteliklerinin (quality attributes) tümünü karşılayacak tek bir “evrensel” araç olması mümkün değildir. Bu nedenle, bize daha fazla tasarım seçeneği sağlaması beklenen bir “sorumluluk ayrımı (separation of concerns)” yapmayı seçiyoruz.

“Standart” Lambda mimarisinden bir diğer fark da, sorgu sonuçlarını birleştirmeye ihtiyaç duymayabileceğimizdir: Kullanım senaryolarımıza göre, sorgular batch görünümler ve gerçek zamanlı görünümler için bağımsız olarak çalıştırılabilir.

---

### Tasarım Kararı ve Yeri  
Ön-Hesaplama (Precomputing) ve Batch Görünümleri (Batch Views) bileşenlerini, Ad Hoc ve Statik Görünümlerle ilişkilendirilmiş alt bileşenlere böl

*(Bu tablonun devamı orijinal metinde sürmektedir; burada karar başlığı verilmiş, gerekçe metni ise bir sonraki parçada gelecektir.)*

---

### Tasarım Kararı ve Yeri  
Master Dataset’in anlamını ve adını Ham Veri Deposu (Raw Data Storage) olarak değiştir

*(Bu karar için de gerekçe, metnin devamında sunulacaktır.)*

Bu öğeler, her biri iki alt öğeye ayrılır:

- Ad Hoc Görünümler Ön Hesaplama (Ad Hoc Views Precomputing) ve Ad Hoc Yığın Görünümler (Ad Hoc Batch Views) (UC-4, QA-5)  
- Statik Görünümler Ön Hesaplama (Static Views Precomputing) ve Statik Yığın Görünümler (Static Batch Views) (UC‑3, QA-4, CON-2)

Bu alt bölümlendirmenin gerekçesi, önceki durumda olduğu gibi aynıdır: En uygun desenleri ve teknolojileri seçme konusunda bize daha fazla esneklik sağlar. Sonraki tasarım yinelemelerinde, bu iki kaygıyı eşzamanlı olarak ele alan tek bir yaklaşım keşfedersek, bu öğeleri birleştirmek kolay olacaktır.

Bu yalnızca bir isim değişikliği değildir; aynı zamanda anlamsal bir değişikliktir. QA-7’ye göre sistem en az 60 gün boyunca ham veriyi saklamalıdır. Dolayısıyla daha eski veriler arşivlenebilir ve başka depolama teknolojileri kullanılarak saklanabilir (hatta silinebilir). Ana Veri Kümesi (Master Dataset) daha fazla sorumluluk üstlenir: Hem ham veri depolamasını hem de arşivlenmiş veriyi içerir. Bu durumu basitleştirmek için, arşivlenmiş verinin incelenmesi ele alınmayacaktır.

Bu ilk yinelemede işlevselliği ve arayüzleri tam olarak tanımlamak için genellikle çok erkendir.

### 5.3.2.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 5.4, önceki somutlaştırma tasarım kararlarının sonucunu göstermektedir. Sonraki sayfada başlayan tablo, her bir öğenin sorumluluklarını özetlemektedir.

![Şekil 5.4](/home/runner/workspace/scripts/dsa_figs/sekil_5_4.png){width=10.87cm}


## 5.3 Tasarım Süreci

BATCH Katmanı  
Ham Veri  
Depolama  
Veri  
Akışı

SERVING Katmanı  
Ad Hoc Görünümler  
Ön Hesaplama

Ad Hoc  
Yığın Görünümler

Statik Görünümler  
Ön Hesaplama

Statik Yığın  
Görünümler

Kurumsal  
BI Aracı

SPEED Katmanı

Veri  
Kaynakları

Gerçek Zamanlı  
Görünümler

Açıklama (Legend):

- Katman Sınırı  
- Öğe Sınırı  
- Gösterge Paneli / Görselleştirme Aracı (Dashboard / Visualization Tool)  
- Veri Akışı (yönü belirtilmiş)  
- Sorgu Sonuçları Akışı

**ŞEKİL 5.4** Lambda mimarisinin somutlaştırılması

| Öğe | Sorumluluk |
| --- | ---------- |
| **Veri Kaynakları (Data Sources)** | Günlükler ve sistem metrikleri üreten web sunucuları (örneğin Apache erişim ve hata günlükleri, Linux sysstat). |
| **Veri Akışı (Data Stream)** | Bu öğe, tüm veri kaynaklarından verileri gerçek zamanlı olarak toplar ve işlenmek üzere hem Batch Katmanı’na hem de Speed Katmanı’na yönlendirir. |
| **Batch Katmanı (Batch Layer)** | Bu katman, ham veriyi depolamaktan ve Serving Katmanı’nda saklanacak yığın görünümleri (batch views) önceden hesaplamaktan sorumludur. |
| **Serving Katmanı (Serving Layer)** | Bu katman, yığın görünümlerini rastgele yazma olmayan, ancak yığın güncellemelerini ve rastgele okumaları destekleyen bir veri deposunda açığa çıkarır; böylece bu görünümler düşük gecikmeli sorgulanabilir. |
| **Speed Katmanı (Speed Layer)** | Bu katman, yığın işlemenin yüksek gecikmesi nedeniyle henüz Serving Katmanı’nda bulunmayan güncel verilere, bir dizi gerçek zamanlı görünüm (real-time views) aracılığıyla erişim sağlar ve bu verileri işler. |
| **Ham Veri Depolama (Raw Data Storage)** | Bu öğe, Batch Katmanı’nın bir parçasıdır ve belirlenmiş bir süre boyunca (QA-7) ham veriyi (değişmez, yalnızca ekleme yapılabilir) depolamaktan sorumludur. |
| **Ad Hoc Görünümler Ön Hesaplama (Ad Hoc Views Precomputing)** | Bu öğe, Batch Katmanı’nın bir parçasıdır ve Ad Hoc Yığın Görünümlerini önceden hesaplamaktan sorumludur. Ön hesaplama, ham veri üzerinde, onu insan-zamanında (human-time) hızlı sorgulamaya uygun bir duruma dönüştüren yığın işlemlerini temsil eder. |
| **Statik Görünümler Ön Hesaplama (Static Views Precomputing)** | Bu öğe, Batch Katmanı’nın bir parçasıdır ve Statik Yığın Görünümlerini önceden hesaplamaktan sorumludur. Ön hesaplama, ham veri üzerinde, onu insan-zamanında hızlı sorgulamaya uygun bir duruma dönüştüren yığın işlemlerini temsil eder. |

---

## Bölüm 5 – Vaka Çalışması: Büyük Veri Sistemi

| Öğe | Sorumluluk |
| --- | ---------- |
| **Ad Hoc Yığın Görünümler (Ad Hoc Batch Views)** | Bu öğe, Serving Katmanı’nın bir parçasıdır ve veri bilimcileri/analistler tarafından yürütülen ad hoc düşük gecikmeli sorgular (QA-5) için optimize edilmiş, önceden hesaplanmış ve birleştirilmiş verileri içerir. |
| **Statik Yığın Görünümler (Static Batch Views)** | Bu öğe, Serving Katmanı’nın bir parçasıdır ve kurumsal bir BI aracı tarafından üretilen önceden tanımlı düşük gecikmeli sorgular (QA-4) için optimize edilmiş, önceden hesaplanmış ve birleştirilmiş verileri içerir. |
| **Gerçek Zamanlı Görünümler (Real-Time Views)** | Bu öğe, Speed Katmanı’nın bir parçasıdır ve işletme ve mühendislik personeli tarafından yürütülen ad hoc, düşük gecikmeli arama sorguları (QA-3) için optimize edilmiş, indekslenmiş günlükleri içerir. |
| **Kurumsal BI Aracı (Corporate BI Tool)** | Bu iş zekâsı aracı, farklı departmanlarda kullanılmak üzere lisanslanmıştır. Araç, SQL arayüzünü (ODBC veya JDBC gibi) destekler ve bu sistem de dâhil olmak üzere birden fazla veri kaynağına bağlanabilir (UC-3, UC-4, CON-2). |
| **Gösterge Paneli / Görselleştirme Aracı (Dashboard / Visualization Tool)** | Operasyon ekibi, çevrimiçi servisleri izlemek, günlüklerdeki önemli mesajları aramak ve potansiyel sorunlara hızlı bir biçimde tepki vermek için bu gerçek zamanlı operasyonel gösterge panelini kullanır (UC-1, UC-2). |

### 5.3.2.6 Adım 7: Geçerli Tasarımın Analizini Yap ve Yineleme Hedefini ve Tasarım Amacının Gerçekleşmesini Gözden Geçir

Bu yinelemede alınan kararlar, tüm sistemin yapısını etkileyen önemli erken aşama hususlarını ele almaktadır. Seçilen referans mimari, tasarım süresini ve çabasını önemli ölçüde tasarruf ettiren, kanıtlanmış bir başlangıç parçalanması (decomposition) ve veri akışı sunduğundan, “boş bir sayfadan” başlamanıza gerek yoktur. Aday teknolojilerin seçilmesi için daha fazla tasarım kararı alınması ve kullanım durumlarının (use case) ve kalite niteliklerinin (quality attribute) nasıl destekleneceğine ilişkin daha fazla detay sağlanması gerekecektir.

Aşağıdaki tablo, Bölüm 3.8.2’de tartışılan Kanban panosu (Kanban board) tekniği kullanılarak tasarım ilerlemesini özetlemektedir.

> **💬 Çevirmen notu:** Kanban panosu burada, her gereksinimin durumunu “ele alınmadı / kısmen / tamamen ele alındı” biçiminde görselleştirmek için kullanılıyor.

|  | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Verilen Tasarım Kararları |
| --- | ----------- | ----------------- | ------------------ | -------------------------------------------- |
| **UC-1** |  | X |  | Gerçek zamanlı verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi gösterge paneli teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **UC-2** |  | X |  | Gerçek zamanlı verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi arama teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **UC-3** |  | X |  | Tarihsel verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi depolama ve sorgu teknolojilerinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |

|  | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Verilen Tasarım Kararları |
| --- | ----------- | ----------------- | ------------------ | -------------------------------------------- |
| **UC-4** |  | X |  | Tarihsel verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi depolama ve sorgu teknolojilerinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **UC-5** | X |  |  | Bu kullanım durumu, bu yinelemede birincil olmayan (nonprimary) olarak göz ardı edilmiştir; ancak Lambda mimarisi bunu desteklemektedir ve sonraki yinelemelerde ele alacağız. |
| **UC-6** | X |  |  | Bu kullanım durumu, bu yinelemede birincil olmayan olarak göz ardı edilmiştir; ancak mimari bakış açısından UC-3’e benzerdir. |
| **QA-1** |  | X |  | Veri Akışı (Data Stream) öğesi için potansiyel veri kaynakları belirlenmiştir. Veri akışı öğesi için hangi teknolojilerin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-3** |  | X |  | Gerçek Zamanlı Görünümler (Real-Time Views) öğesi tanımlanmıştır. Hangi depolama ve sorgu teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-4** |  | X |  | Statik Yığın Görünümler (Static Batch Views) öğesi tanımlanmış ve sorumlulukları belirlenmiştir. Hangi depolama teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-5** |  | X |  | Ad Hoc Yığın Görünümler (Ad Hoc Batch Views) öğesi tanımlanmış ve sorumlulukları belirlenmiştir. Hangi depolama ve sorgu teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-6** |  | X |  | Gerçek Zamanlı Görünümler öğesinin sorumlulukları belirlenmiştir. Hangi depolama ve sorgu teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-7** |  |  |  |  |

Ham Veri Depolama (Raw Data Storage) bileşeni tanımlanmış ve sorumlulukları
belirlenmiştir. Hangi depolama teknolojisinin kullanılacağıyla ilgili ayrıntılı
kararlar henüz verilmemiştir.

---

# 5. Bölüm — Vaka Çalışması: Büyük Veri Sistemi

|                  | Durum              |
|------------------|--------------------|
| CRN-2            | Ele Alınmadı       |
| 5.3.3            |                    |
| Kısmen Ele Alındı|                    |
| Tamamen Ele Alındı |                 |

## Yineleme Sırasında Alınan Tasarım Kararları

**QA-8**

Ad Hoc ve Statik Toplu Görünümler (Ad Hoc and Static Batch Views) bileşenleri
tanımlanmış ve sorumlulukları belirlenmiştir. Hangi depolama teknolojilerinin
kullanılacağıyla ilgili ayrıntılı kararlar henüz verilmemiştir.

**QA-10**

Sistem bileşenlerini gerçekleştirmek için seçilen tüm teknolojilerin, hata toleransı
(fault tolerance) yapılandırması sağlayarak ve tekil hata noktası (single point of
failure) içermeyerek QA-10’u desteklemesine karar verilmiştir.

**CON-2**

Kurumsal BI Aracı (Corporate BI Tool) bileşeni tanımlanmıştır. Bu kısıtın nasıl
karşılanacağıyla ilgili ayrıntılı kararlar henüz verilmemiştir.

**CRN-1**

Sistemin genel mantıksal yapısı oluşturulmuş, ancak fiziksel yapı hâlâ
tanımlanmalıdır.

Bu adımda ilgili bir karar alınmamıştır.

---

## Yineleme 2: Teknolojilerin Seçimi

Bu bölüm, tasarım sürecinin ikinci yinelemesinde, nitelik temelli tasarımın (Attribute-Driven Design, ADD) her adımında gerçekleştirilen
etkinliklerin sonuçlarını sunmaktadır.

Teknoloji seçimleri çoğu zaman sistem mimarisini etkiler; bu da mimari tasarımın
en erken aşamalarında teknolojileri seçmemiz gerektiği anlamına gelir. Teknoloji
seçimi, teknoloji ailelerinin belirlenmesi ve seçilmesiyle başlar; bu aileler daha
sonra belirli teknolojilerle somutlaştırılır. Teknoloji aileleriyle başlamak, belirli
teknolojileri birbirleriyle değiştirilebilir kılmamıza olanak tanır ve böylece tedarikçi bağımlılığından (vendor lock-in) kaçınmak için doğru düzeyde teknoloji
bağımsızlığını (technology agnosticism) koruruz (sonuç olarak gelecekte bir teknolojiyi daha iyisiyle değiştirme riski ve maliyeti azalır).

Bu yinelemede, Büyük Veri (Big Data) “greenfield” sistemleri tasarlarken
optimal yapıtaşlarını seçmemize yardımcı olacak bir teknoloji ağacı göstereceğiz.

---

## 5.3 Tasarım Süreci

### 5.3.3.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefinin Belirlenmesi

Bu yinelemenin hedefi, CRN-2’yi (ekibin Apache Büyük Veri ekosistemi
bilgisinden yararlanmak) ele almaktır; bunun için, özellikle CON-1’i (açık kaynak
teknolojileri tercih et) akılda tutarak, Bölüm 5.2’de tanımlanan sistem gereksinimlerini destekleyecek teknolojileri seçmek gerekir.

### 5.3.3.2 Adım 3: Ayrıntılandırılacak Bir veya Daha Fazla Sistem Bileşeninin Seçilmesi

Önceki yinelemede seçilen başvuru mimarisi (Lambda mimarisi), teknoloji ailelerinin ve bunlarla ilişkili belirli teknolojilerin seçimini kolaylaştıracak bileşenlere
ayrıştırılmıştı. Bu bileşenler şunları içerir:

- Veri Akışı (Data Stream)
- Ham Veri Depolama (Raw Data Storage)
- Ad Hoc ve Statik Görünümler Ön-hesaplama (Ad Hoc and Static Views Precomputing)
- Ad Hoc ve Statik Toplu Görünümler (Ad Hoc and Static Batch Views)
- Gerçek Zamanlı Görünümler (Real-Time Views)
- Gösterge Paneli/Görselleştirme Aracı (Dashboard/Visualization Tool)

### 5.3.3.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramının Seçilmesi

Bu yinelemede kullanılan tasarım kavramları, dışarıda geliştirilmiş bileşenlerdir.
Başlangıçta teknoloji aileleri seçilir ve ayrıntılandırılacak bileşenlerle ilişkilendirilir. Bir teknoloji ailesi, ortak işlevsel amaçlara sahip teknolojiler kümesini
temsil eder (bkz. Bölüm 2.5.5). Aile adları işlevlerini yansıtır ve bazı belirli
teknolojiler aynı anda birden fazla aileye ait olabilir; ancak bu tür bir sınıflandırma,
sonuçta daha az yeniden iş ve değişikliklere daha iyi hazırlık sağlayacak rasyonel
tasarım kararları almamıza yardımcı olur.

Yazılım endüstrisinin geçmişi, teknoloji uygulamalarının, onların aileleriyle temsil edilen örüntü (pattern) ve prensiplerden çok daha hızlı biçimde ortaya çıktığını,
evrildiğini ve ortadan kaybolduğunu göstermektedir.

Şekil 5.5, Büyük Veri alanı için aile gruplarını, teknoloji ailelerini (düz metinle)

![Şekil 5.5](/home/runner/workspace/scripts/dsa_figs/sekil_5_5.png){width=10.27cm}

ve bunlarla ilişkili belirli teknolojileri (italik metinle) göstermektedir. Bu
teknolojilerin birçoğu hakkında daha fazla ayrıntı, Smart Decisions Game’in
tasarım kavramları kataloğunda bulunabilir (bkz. “Further Reading” bölümü).

---

# 5. Bölüm — Vaka Çalışması: Büyük Veri Sistemi

## Büyük Veri Analitiği Kataloğu

**Veri Toplayıcı (Data Collector)**  
- Apache Flume  
- Logstash  
- Fluentd  

**Mesajlaşma (Messaging)**  
- Apache Kafka  

**Entegrasyon (Integration)**  
- RabbitMQ  

**Dağıtık Mesaj Aracısı (Distributed Message Broker)**  
- Amazon SQS  
- Apache ActiveMQ  

**ETL/ELT**  
- StreamSets  

**ETL/Veri Entegrasyon Motoru (ETL/Data Integration Engine)**  
- Talend  
- Informatica  

**Dağıtık Dosya Sistemi (Distributed File System)**  
- HDFS  
- CassandraFS  
- Riak  

**Anahtar-Değer (Key-Value)**  
- Redis  
- Berkeley DB  

**Belge Yönelimli (Document-Oriented)**  
- MongoDB  
- CouchDB  

**NoSQL Veritabanı (NoSQL Database)**  
- HBase  

**Sütun Ailesi (Column-Family)**  
- Cassandra  

**Graf Yönelimli (Graph-Oriented)**  
- Neo4J  
- OrientDB  

**MPP Analitik İlişkisel VTYS (MPP Analytic RDBMS)**  
- HP Vertica  
- Teradata  
- MS PDW  
- Amazon Redshift  

**Analitik İlişkisel VTYS (Analytic RDBMS)**  
- MS SQL Server  

**Geleneksel Analitik İlişkisel VTYS (Traditional Analytic RDBMS)**  
- Oracle RDBMS  
- IBM DB2  

**BI Platformu (BI Platform)**  
- QlikView  
- Microstrategy  
- Tableau  
- Tibco JasperSoft  
- Pentaho  
- Splunk  

**Görselleştirme ve Raporlama (Visualization & Reporting)**  
- İnteraktif Gösterge Paneli (Interactive Dashboard)  
  - Kibana  
  - Zoomdata  
- Grafik Kütüphanesi (Graphic Library)  
  - D3.js  
  - GoJS  
  - Highcharts  

**Etkileşimli Sorgu Motoru (Interactive Query Engine)**  
- Impala  
- Apache Hive (Stinger)  
- Spark SQL  

**Arama ve Sorgu (Search & Query)**  
- Splunk  
- Elasticsearch  

**Dağıtık Arama Motoru (Distributed Search Engine)**  
- Apache Solr  

**Dağıtık Hesaplama Motoru (Distributed Computing Engine)**  
- Hadoop MapReduce  
- Apache Spark  
- Apache Tez  

**İşleme (Processing)**  
- Olay Akışı İşleyici (Event Stream Processor)  
  - Apache Storm  
  - Spark Streaming  
  - Apache Samza  
  - Amazon Kinesis  

**Veri İşleme Çatısı (Data Processing Framework)**  
- Cascading  
- Apache Crunch  
- Apache Hive  
- Amazon Pig  

Açıklama (Legend):  
- Düz metin – teknoloji ailesi  
- İtalik metin – belirli teknoloji

**ŞEKİL 5.5** Büyük Veri analitiği tasarım kavramları kataloğuna bir örnek  
(Kaynak: Softserve)

---

## 5.3 Tasarım Süreci

BI Platformu (BI Platform) aile grubu ve ilişkili teknolojiler, bu tasarım
çalışmasında daha fazla ele alınmamaktadır; çünkü kurumsal BI aracı hedef
sistemden haricidir.

---

### Tasarım Kararları ve Konumu

#### Veri Akışı (Data Stream) bileşeni için Veri Toplayıcı (Data Collector) ailesini seç

**Gerekçe ve Varsayımlar**

Veri Toplayıcı (Data Collector), günlük (log) verilerini daha sonra kullanılmak
üzere toplayan, birleştiren ve aktaran bir teknoloji ailesi (ve mimari desen)dir.
Genellikle Veri Toplayıcı uygulamaları, popüler olay kaynakları ve hedefleriyle
bütünleşmek için hazır eklentiler (out-of-the-box plug-in) sunar.

Hedefler, bu yinelemede ele alınacak olan Ham Veri Depolama (Raw Data Storage)
ve Gerçek Zamanlı Görünümler (Real-Time Views) bileşenleridir.

**Alternatif** | **Elenme Nedeni**
--------------|--------------------
**ETL Motoru (ETL Engine)** | ETL motorlarının temel amacı, olay başına (per-event) işlemlerden ziyade toplu (batch) dönüşümler gerçekleştirmektir. Bu da gerçek zamanlı performans ve ölçeklenebilirlik ölçütlerini (QA-1, QA-2) karşılamayı son derece zor, hatta imkânsız hâle getirir.
**Dağıtık Mesaj Aracısı (Distributed Message Broker)** | Bu teknoloji ailesi tek başına Veri Akışı (Data Stream) bileşenini gerçekleştirmek için kullanılabilse de, genişletilebilirlik (QA-9) için daha az destek sunar ve bu nedenle veri toplayıcının tamamlayıcısı olarak kullanılmaya daha uygundur. Bu, örneğin Apache Flume (Veri Toplayıcı) ve Apache Kafka’nın (Dağıtık Mesaj Aracısı) birleşimi olan Flavka kullanılarak gerçekleştirilebilir.

#### Ham Veri Depolama (Raw Data Storage) bileşeni için Dağıtık Dosya Sistemi (Distributed File System) ailesini seç

Lambda mimarisi (Lambda architecture) ilkelerine göre, Ham Veri Deposu (Raw Data Storage) bileşeni değiştirilemez (immutable) olmalıdır. Dolayısıyla yeni veriler mevcut veriyi değiştirmemeli, sadece veri kümesine eklenmelidir (append). Veriler, ham verilerin Toplu Görünümlere (Batch Views) dönüştürülmesi için yığın (batch) işlemlerle okunacaktır. Bu amaçlar için, güvenle bir Dağıtık Dosya Sistemi (Distributed File System) seçebiliriz.

### Alternatif – Elenme Gerekçesi  
**NoSQL Veritabanı (NoSQL Database)**

NoSQL veritabanları (özellikle sütun aileli (column-family) ve belge odaklı (document-oriented) olanlar) günlük (log) gibi ham verileri depolamak için kullanılabilse de, bu durum kaynak tüketiminde (çoğunlukla önbellekleme mekanizmalarından dolayı bellek tüketimi) gereksiz ek yük oluşturacak ve şema yapılandırma ve evrimleştirme ihtiyacı nedeniyle bakımını zorlaştıracaktır.

**Analitik İlişkisel Veritabanı Yönetim Sistemi (Analytic RDBMS)**

Tüm analitik yeteneklere sahip ilişkisel veritabanları, ilişkisel modele dayanır ve tablolar ile satırlar oluşturur. Bu, karmaşık sorguları yürütmek için çok iyi çalışsa da, yarı-yapısal günlüklerin ham biçimde depolanması için hem kullanışsız hem de pahalı bir seçenektir.  

---

## 5.3 Tasarım Süreci

### Tasarım Kararları ve Konumu  
Statik ve Anlık (Ad Hoc) Toplu Görünümler (Batch Views) bileşenleri için aynı Etkileşimli Sorgu Motoru (Interactive Query Engine) ailesini seç

#### Gerekçe ve Varsayımlar

Önceki yinelemede belirttiğimiz gibi, Toplu Görünümler (Batch Views) bileşeni, iki kullanım senaryosunu desteklemek üzere Statik ve Anlık (Ad Hoc) Toplu Görünümler olarak ayrıştırılmıştır: statik raporların üretilmesi (UC-3, UC-6) ve anlık sorgulamayı (ad hoc querying) desteklemek (UC-4). Ana tasarım kararı, hem Statik hem de Anlık Toplu Görünümler için aynı teknoloji ailesini kullanmaktır; yani Etkileşimli Sorgu Motoru (Interactive Query Engine). Bu motorlar, Dağıtık Dosya Sistemi üzerinde depolanan veriler üzerinde analitik veritabanı (analytic database) yetenekleri sağlar (dolayısıyla bu teknoloji ailesi de örtük olarak seçilmiş olur). Yeterince hızlı bir teknoloji seçersek, bu teknoloji her iki bileşen için de kullanılabilir. Tek bir teknoloji ailesi kullanmanın faydası, raporlama ve veri sorgulama için ayrı depolama teknolojilerine ihtiyaç duymamamızdır.

### Alternatif – Elenme Gerekçesi  
**NoSQL Veritabanı (NoSQL Database)**

Statik Toplu Görünümler (Static Batch Views) bileşeni, veriyi sorgulama ve bir raporlama sistemi (kurumsal BI aracı) içinde gösterme için hazır bir biçimde depolayan Özelleştirilmiş Görünüm (Materialized View) deseni ile uygulanabilir. NoSQL Veritabanı ailesi, iyi ölçeklenebilirlik sağlaması ve açık kaynak olması nedeniyle sıkça bu amaçla kullanılır; böylece QA-8’in (yaklaşık 90 TB birikimli veri) ve CON-1’in (açık kaynak lisansı) gereksinimlerini karşılar.

Ancak NoSQL veritabanları, anlık (ad hoc) sorgular için veri ambarı (data warehouse) olarak kullanılmak üzere iyi birer seçenek değildir; çünkü analitik amaçlar için tasarlanmamışlardır. Bu amaçla kullanılabilseler de, bu kullanım önemli performans cezalarına yol açacaktır.

Bu alternatif bu nedenle elenmiştir; çünkü yalnızca Statik Toplu Görünümler için kullanılabilir, Anlık Toplu Görünümler için ise etkisizdir.

**Analitik İlişkisel Veritabanı Yönetim Sistemi (Analytic RDBMS)**

Anlık (ad hoc) sorgular, SQL-benzeri bir arayüzün desteklediği herhangi bir sorgu olabilir. Sorgu sonucunun “insani” bir sürede (QA-5) döndürülmesi gerekir. Tanımlanan senaryo, bir veri ambarının tam olarak kullanıldığı senaryodur. Bu desen, genellikle Kimball veya Inmon tasarım yaklaşımlarını izleyen Analitik RDBMS teknolojileriyle uygulanır. Aynı anda, yaklaşık 90 TB birikimli veri ölçeklenebilirlik gereksinimini karşılamak oldukça maliyetli olacaktır. MPP (Massively Parallel Processing) analitik veritabanlarındaki terabayt başına maliyet, aynı miktar veri için bir NoSQL veritabanı veya bir dağıtık dosya sisteminden (örneğin Hadoop) anlamlı derecede daha yüksektir (30 kata kadar).

### Tasarım Kararları ve Konumu  
Analitik RDBMS alternatifini ele

#### Gerekçe ve Varsayımlar

Bu alternatif elenmiştir; çünkü hem Statik hem de Anlık Toplu Görünümler için kullanılabilse bile, bu aileyle ilişkili teknolojiler (açık kaynak) Hadoop-tabanlı alternatiflere göre maliyetlidir.

---

### Tasarım Kararları ve Konumu  
Görünümlerin Ön Hesaplama (Precomputing) bileşenleri için Veri İşleme Çatısı (Data Processing Framework) kullan

#### Gerekçe ve Varsayımlar

Ham Veri Deposu (Raw Data Storage) ve Toplu Görünümler (Batch Views) için Dağıtık Dosya Sistemi ailesini zaten seçtiğimize göre, bir sonraki adım Ham Veri Deposu’ndan Toplu Görünümlerde kullanılan formata veri dönüşümü sağlayacak bir çözüm seçmektir.

Karar, Veri İşleme Çatısı’nı (Data Processing Framework) seçmektir; çünkü bu teknoloji ailesi, daha hızlı geliştirme ve daha iyi sürdürülebilirlik sağlayan soyutlamalar kullanarak veri işleme boru hatları (data processing pipelines) oluşturmaya olanak verir.

### Alternatif – Elenme Gerekçesi  

**Dağıtık Hesaplama Motoru (Distributed Computing Engine)**

Çoğu Dağıtık Hesaplama Motoru teknolojisi yığın (batch) veri işleme için tasarlanmıştır, ancak düşük seviye ilkelere (örneğin MapReduce görevleri yazmak) dair önemli düzeyde bilgi gerektirir.

**Olay Akışı İşleyici (Event Stream Processor)**

Bu, gerçek zamanlı akış işlemeye yönelik tasarlanmıştır; yığın (batch) işlemler için etkisizdir.

---

### Tasarım Kararları ve Konumu  
Gerçek Zamanlı Görünümler (Real-Time Views) bileşeni için Dağıtık Arama Motoru (Distributed Search Engine) seç

#### Gerekçe ve Varsayımlar

Gerçek Zamanlı Görünümler bileşeni, son günlükler üzerinde tam metin araması yapmak ve gerçek zamanlı izleme verileriyle bir operasyonel gösterge panelini beslemekten sorumludur (UC-1, UC-2). Dağıtık Arama Motoru (Distributed Search Engine), tam olarak bu tür amaçlara hizmet eden bir teknoloji ailesidir.

### Alternatif – Elenme Gerekçesi  
**NoSQL Veritabanı (NoSQL Database)**

Bazı NoSQL veritabanları anahtar kelime araması veya metin araması sağlar, ancak bunlar, gövdeleme (stemming) ve konum tabanlı arama (geolocation) gibi metin işleme özellikleri de sunan arama motorları kadar güçlü ve hızlı değildir.

**Analitik İlişkisel Veritabanı Yönetim Sistemi (Analytic RDBMS)**

Bazı veritabanları (örneğin MS SQL Server) tam metin arama yetenekleri sağlar; ancak genişletilebilirlik, bakım ve maliyet açılarından daha az tercih edilirler.

**Dağıtık Dosya Sistemi ve Etkileşimli Sorgu Motoru  
(Distributed File System and Interactive Query Engine)**

Bu yaklaşım, geçmiş (historical) yığın verileri için iyi çalışır; ancak veriyi depolama ve işleme gecikmesi, gerçek zamanlı veriler için çok yüksek olacaktır.

---

### Tasarım Kararları ve Konumu  
Sistemin dağıtımını Puppet betikleriyle otomatikleştir

#### Gerekçe ve Varsayımlar

Puppet betikleri, hem Özel Bulut (Private Cloud, örn. VMware) hem de Genel Bulut (Public Cloud, örn. AWS) dağıtımları için kullanılabilir. Bu, CON-3’ün karşılanmasını destekler. Puppet, dağıtım sürecini otomatikleştirmenin yanı sıra bir sistemin yapılandırmasını yönetmeye de olanak verir. Birçok popüler açık kaynak teknolojinin dağıtımını otomatikleştirmek için Puppet topluluğu tarafından yazılmış ön tanımlı betiklerden oluşan bir kütüphane vardır.

> **💬 Çevirmen notu:** Puppet, altyapıyı kod olarak (Infrastructure as Code, IaC) yönetmeye olanak veren, yaygın bir yapılandırma yönetim aracıdır.

---

## 5.3.3.4 Adım 5: Mimari Bileşenleri Örnekle, Sorumlulukları Yükle ve Arayüzleri Tanımla

Bu yinelemede, daha önce seçilen teknoloji aileleriyle belirli teknolojileri ilişkilendirerek örnekleme (instantiation) yapılmaktadır. Göz önünde bulundurulan ve alınan örnekleme tasarım kararları aşağıdaki tabloda özetlenmiştir:

| Tasarım Kararı ve Konumu | Gerekçe |
| --- | --- |
| Veri Akışı (Data Stream) bileşeni için Veri Toplayıcı (Data Collector) ailesinden Apache Flume kullan | İlk aday teknoloji olarak Apache Flume’u seçeceğiz. Çalışma zamanında sadece yapılandırma güncellenerek yeni veri kaynakları eklenmesini sağlayan QA-9’u (yeni veri kaynaklarının sadece bir yapılandırma güncellemesiyle eklenmesi) desteklemek için gerekli yapılandırılabilirliği sağlar. |

### Alternatif – Elenme Gerekçesi  
**Logstash veya Fluentd**

*(devam edecek)*

Logstash ve Fluentd oldukça popüler teknolojiler olmasına rağmen (belki de Flume kadar popülerdir) ve gereksinimleri karşılayacak olsalar da bir seçim yapmamız ve yalnızca birini belirlememiz gerekir. Flume’u seçmek için ek bir argüman, üç büyük Hadoop dağıtım satıcısı tarafından desteklenmesidir.

Bu teknoloji için, bu tür kullanım senaryosunu (QA-7, yaklaşık 60 TB ham veriyi depolama) desteklemek üzere tasarlanmış olduğundan, güvenle HDFS’i seçebiliriz. HDFS içinde verileri depolamak için kullanılabilecek metin dosyası (text file), SequenceFile, RCFile, ORCFile, Avro ve Parquet gibi bir dizi Hadoop dosya formatı da vardır. Dosya formatı seçimi üçüncü yinelemede ele alınacaktır.

| Alternatif   | Elenme Nedeni                                                                                     |
|-------------|----------------------------------------------------------------------------------------------------|
| CassandraFS | Bu teknoloji bir NoSQL veritabanına (Cassandra) bağımlıdır, oysa biz yalnızca dağıtık dosya sistemi (Distributed File System) seçtik. |

## 5.3 Tasarım Süreci

| Tasarım Kararı ve Konumu                                                                 | Gerekçe |
|------------------------------------------------------------------------------------------|--------|
| Hem Static Batch Views hem de Ad Hoc Batch Views elemanları için Interactive Query Engine ailesinden Impala kullan | Birincil aday teknoloji olarak Impala’yı seçiyoruz; rekabetçi performans sunuyor (her ne kadar en üst Analitik RDBMS platformları kadar hızlı olmasa da) ve kurumsal bir BI aracıyla bağlantı için bir ODBC arayüzü sağlıyor. Olası performans sorunlarını akılda tutarak, bu teknoloji seçiminin QA-4’ü (5 saniyeden az rapor yükleme süresi) ve QA-5’i (2 dakikadan az ad hoc sorgu yürütme süresi) karşıladığından emin olmak için sonraki yinelemelerde bir kavram kanıtlama (proof-of-concept) planlıyoruz. |
| Real-Time Views elemanları için Distributed Search Engine ailesinden Elasticsearch kullan. Dashboard/Visualization Tool elemanı için Interactive Dashboard ailesinden Kibana kullan. | Birincil aday teknoloji olarak Elasticsearch’ü seçiyoruz, çünkü aynı zamanda Kibana adında etkileşimli bir pano (interactive dashboard) şeklinde bir görselleştirme aracı da sunuyor. Kibana rol tabanlı güvenlik içermeyen görece basit bir pano olmasına rağmen (en azından bu çözüm tasarlanırken), UC-1, UC-2 kullanım senaryolarını ve QA-2’yi (1 dakikadan kısa periyotla otomatik yenilenen pano) karşılamaktadır. Elasticsearch ayrıca zaman serilerini sorgulamak, filtrelemek ve görselleştirmek için Kibana tarafından desteklenen alan‑özgül bir dil (domain-specific language) olan Query DSL sağlar. |
| Views Precomputing elemanları için Data Processing Framework ailesinden Hive kullan | Birincil aday teknoloji olarak Hive’ı seçiyoruz; ancak QA-4’ün (15 dakikadan az gecikme) karşılandığından emin olmak için sonraki bir yinelemede bir kavram kanıtlama prototipi oluşturmamız gerekecek. Hive, bu yinelemede zaten seçilmiş olan Impala gibi SQL benzeri bir dil sunar; böylece veri dönüşüm betiklerini yazarken veri ambarı tasarımcılarının yetkinliklerinden yararlanmamıza olanak tanır. |

| Alternatif          | Elenme Nedeni                                                                                                                                                      |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Apache Hive (Stinger) | Stinger girişimi sayesinde Hive performansını iyileştirmiş olsa da, sorguların hızı hâlâ Impala ve Spark SQL gibi diğer alternatiflere kıyasla yavaştır.            |
| Spark SQL           | Spark, Büyük Veri (Big Data) analitiği için çok umut verici bir teknolojidir, ancak bir BI aracı için SQL adaptörü rolünde kullanılması Spark SQL için en uygun kullanım olmayabilir. Dezavantajı, yüksek bellek gereksinimleri ve önbelleğe alınmamış veriler üzerindeki uzun sorgu süreleridir. Buna karşılık, Impala tam olarak bu senaryo için tasarlanmış ve optimize edilmiştir. |
| Splunk              | Splunk da indeksleme ve görselleştirme yetenekleri sunar (Elasticsearch ve Kibana’dan daha fazla özellik sağlar); ancak CON-1 bizi açık kaynaklı bir çözümü tercih etmeye yönlendirir. |
| Cascading veya Apache Pig | Mevcut geliştirme ekibinin SQL becerilerinden yararlanarak geliştirme süresini en aza indirmek için Cascading ve Pig’i eledik.                                         |

Veri, elemanlar arasında değiş tokuş edilirken, sonraki yinelemelerde daha kesin biçimde tanımlanacaktır. Bu verinin formatı, elemanlar arasındaki “arayüzleri (interfaces)” oluşturur.

### 5.3.3.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 5.6, somutlaştırma (instantiation) kararlarının sonucunu göstermektedir. Diyagramda görülen elemanların sorumlulukları, 1. yinelemenin 6. adımında tartışılmıştı. Aşağıdaki tablo, bu elemanlar için seçilen teknoloji ailelerini ve aday özgül teknolojileri özetlemektedir:

![Şekil 5.6](/home/runner/workspace/scripts/dsa_figs/sekil_5_6.png){width=12.49cm}


| Eleman                      | Teknoloji Ailesi               | Aday Teknoloji  |
|----------------------------|---------------------------------|-----------------|
| Data Stream                | Data Collector                  | Apache Flume    |
| Raw Data Storage           | Distributed File System         | HDFS            |
| Ad Hoc Views Precomputing  | Data Processing Framework       | Apache Hive     |
| Static Views Precomputing  | Data Processing Framework       | Apache Hive     |
| Ad Hoc Batch Views         | Interactive Query Engine        | Impala          |
| Static Batch Views         | Interactive Query Engine        | Impala          |
| Real-Time Views            | Distributed Search Engine       | Elasticsearch   |
| Dashboard/Visualization Tool | Interactive Dashboard         | Kibana          |

```text
BATCH Katmanı
Dağıtık dosya
sistemi (HDFS)

Raw Data
Storage

Data Collector
(Flume)

SERVING Katmanı
Data processing
framework (Hive)
Ad Hoc Views
Precomputing

Interactive Query
Engine (Impala)

Ad Hoc
Batch Views

Data processing
framework (Hive)

Interactive Query
Engine (Impala)

Static Views
Precomputing

Static
Batch Views

Kurumsal
BI Aracı

SPEED Katmanı

Data Stream

Distributed
Search Engine
(Elasticsearch)

Veri
Kaynakları

Real-Time Views
Gösterim:
Katman
Sınırı
Eleman
Sınırı

Veri Akışı
(yön belirtilmiş)
Sorgu Sonuç Akışı

Teknoloji ailesi + (Özgül teknoloji)

ŞEKİL 5.6 Yineleme 2 somutlaştırma tasarım kararları

(Kibana)

Dashboard/
Visualization
Tool
```

> **💬 Çevirmen notu:** Şekil 5.6, Lambda mimarisi benzeri üç katmanlı (Batch, Serving, Speed) bir Büyük Veri çözümündeki mantıksal elemanları, bunların veri akışlarını ve seçilen somut teknolojileri (Flume, HDFS, Hive, Impala, Elasticsearch, Kibana) üst üste gösteren bir mimari diyagramdır.

Bir sonraki tablo, seçilen teknolojilere bağlı olarak elemanlar arasındaki ilişkileri açıklamaktadır:

| Kaynak Eleman                 | Hedef Eleman                          | İlişki Açıklaması                                                                 |
|------------------------------|---------------------------------------|-----------------------------------------------------------------------------------|
| Data Sources (loglar)        | Data Stream (Flume)                   | Bir sonraki yinelemede tanımlanacaktır                                            |
| Data Stream (Flume)          | Raw Data Storage (HDFS)               | Flume HDFS sink üzerinden ağ iletişimi (push)                                     |
| Raw Data Storage (HDFS)      | Views Precomputing (Apache Hive)      | Hive tarafından kapsüllenmiş yerel ve ağ iletişimi                                |
| Views Precomputing (Apache Hive) | Batch Views (Impala)              | Hive tarafından kapsüllenmiş yerel ve ağ iletişimi                                |
| Batch Views (Impala)         | Corporate BI Tool                     | ODBC API üzerinden ağ iletişimi (pull)                                            |
| Data Stream (Flume)          | Real-Time Views (Elasticsearch)       | Flume Elasticsearch sink üzerinden ağ iletişimi (push)                            |
| Real-Time Views (Elasticsearch) | Dashboard/Visualization Tool (Kibana) | Elasticsearch API üzerinden ağ iletişimi (pull)                                |

### 5.3.3.6 Adım 7: Mevcut Tasarımın Analizini Yap ve Yineleme Hedefini ile Tasarım Amacının Gerçekleşmesini Gözden Geçir

Aşağıdaki Kanban tablosu, yineleme sırasında tasarım ilerlemesini ve alınan kararları özetlemektedir. Önceki yinelemede tamamen ele alınmış sürücülerin gösterilmediğine dikkat edin.

|                    | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Alınan Tasarım Kararları                                                                                                  |
|--------------------|-------------|-------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| UC-1               |             |                   |                    | Gerçek zamanlı izleme bilgilerini göstermek için Distributed Search Engine (Elasticsearch) ve Interactive Dashboard (Kibana) kullan. Bekleyen: İndeksleri modellemek ve bir UI taslak arayüz (mockup) oluşturmak. |
| UC-2               |             |                   |                    |                                                                                                                                               |

Tam Metin Arama için son log verileri üzerinde Dağıtık Arama Motoru (Elasticsearch) ve Etkileşimli Gösterge Paneli (Kibana) kullan.
Beklemede: İndeksleri modelle ve bir kavram kanıtı (proof-of-concept) oluştur.

UC-3  
UC-4  

Batch Görünümler (Batch Views) elemanları için Etkileşimli Sorgu Motoru (Interactive Query Engine, Impala) kullan.
Beklemede: Veriyi ve tipik raporları modelle.
(devam ediyor)

---

### 5. Bölüm — Büyük Veri Sistemi Üzerine Vaka Çalışması

|                  | Not Addressed | Partially Addressed | Completely Addressed |
|------------------|---------------|---------------------|----------------------|
| **Bu Yineleme Sırasında Verilen Tasarım Kararları** |               |                     |                      |

UC-6  

Bu kullanım durumu (use case), mimari bakış açısından UC-3’e benzemesine rağmen, birincil olmadığı için bu yinelemede dışarıda bırakılmıştır.

QA-1  

Veri Akışı (Data Stream) elemanı için Veri Toplayıcı (Data Collector, Apache Flume) kullan.  
Beklemede: Konfigürasyon, kavram kanıtı (proof-of-concept) ve performans testleri.

QA-2  
QA-3  

Dağıtık Arama Motoru (Elasticsearch) ve Etkileşimli Gösterge Paneli (Kibana) kullan.  
Beklemede: Kavram kanıtı (proof-of-concept) ve performans testleri.

QA-4  

Statik Batch Görünümler (Static Batch Views) elemanı için Etkileşimli Sorgu Motoru (Impala) kullan.  
Beklemede: Veriyi modelle, kavram kanıtı (proof-of-concept) ve performans testleri.

QA-5  

Ad Hoc Batch Görünümler (Ad Hoc Batch Views) elemanı için Etkileşimli Sorgu Motoru (Impala) kullan.  
Beklemede: Veriyi modelle, kavram kanıtı (proof-of-concept) ve performans testleri.

QA-6  

Gerçek Zamanlı Görünümler (Real-Time Views) elemanı için Dağıtık Arama Motoru (Elasticsearch) kullan.  
Beklemede: Kapasite planlaması yap.

QA-7  

Ham Veri Depolama (Raw Data Storage) elemanı için Dağıtık Dosya Sistemi (Distributed File System, HDFS) kullan.  
Beklemede: Dosya formatını seç ve kapasite planlaması yap.

QA-8  

Batch Görünümler (Batch Views) için depolama katmanı olarak Dağıtık Dosya Sistemi (HDFS) kullan.  
Beklemede: Dosya formatını seç ve kapasite planlaması yap.

QA-9  

Veri Akışı (Data Stream) elemanı için Veri Toplayıcı (Apache Flume) kullan.  
Beklemede: Konfigürasyon ve kavram kanıtı (proof-of-concept).

QA-10  

Tüm sistem elemanlarında hata toleransı (fault tolerance) kullan.  
Beklemede: Stres testi.

QA-11  

Farklı ortamlar için dağıtım (deployment) sürecini otomatikleştirmek amacıyla Puppet betikleri kullan.

---

## 5.3 Tasarım Süreci

|                  | Not Addressed | Partially Addressed | Completely Addressed |
|------------------|---------------|---------------------|----------------------|
| **Bu Yineleme Sırasında Verilen Tasarım Kararları** |               |                     |                      |

CON-1  

Seçilen tüm teknolojiler açık kaynak (open source) olacaktır.

CON-2  

ODBC arayüzü ile Etkileşimli Sorgu Motoru (Impala) kullan.

CON-3  

Seçilen tüm teknolojiler, Puppet betikleri kullanılarak hem özel bulut (private cloud, VMware) hem de genel bulut (public cloud, AWS) ortamlarına dağıtılabilir.

CRN-1  

İlgili bir karar verilmemiştir.

CRN-2  

Apache Büyük Veri ekosisteminden gelen teknolojiler seçilmiş ve başvuru mimarisi (reference architecture) içindeki farklı elemanlarla ilişkilendirilmiştir.

---

## 5.3.4 Yineleme 3: Veri Akışı Elemanının İyileştirilmesi

Bu bölüm, tasarım sürecinin üçüncü yinelemesinde, nitelik temelli tasarım (Attribute-Driven Design, ADD) adımlarının her birinde gerçekleştirilen faaliyetlerin sonuçlarını sunar.  
Bu yinelemede verilen bazı tasarım kararları, salt kavramsal düzeyde ele alınamayacağı için bir kavram kanıtı (proof-of-concept) prototipi oluşturulmasını gerektirmektedir. Büyük Veri alanının genç olması ve teknolojilerin hızla evrilmesi nedeniyle, temel elemanlara yönelik kavram kanıtları, teknoloji risklerini (örneğin uyumsuzluk, düşük performans, tatmin edici olmayan güvenilirlik, vaat edilen özelliklerdeki kısıtlar) azaltmak ve tasarım ile geliştirme sürecinin erken bir aşamasında alternatiflere geçiş yapma seçeneğine sahip olmak için gereklidir. Bu da, daha sonra yapılacak yeniden işleme (rework) ihtiyacını önleyerek genel zaman ve bütçe tasarrufu sağlar.

### 5.3.4.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu yinelemenin amacı, Veri Toplayıcı (Data Collector) elemanı için kullanılacak teknoloji olarak Apache Flume’un seçimiyle ilişkili çeşitli kaygıları ele almaktır. Apache Flume, Şekil 5.7’de gösterilen gayriresmî diyagramda tasvir edilen bir başvuru yapısı—bir veri akışı modeli (data-flow model)—sağlar.  

![Şekil 5.7](/home/runner/workspace/scripts/dsa_figs/sekil_5_7.png){width=10.58cm}


Flume’un yapısındaki elemanlar şunlardır:

- Kaynak (source): Web sunucuları gibi haricî veri kaynakları tarafından kendisine iletilen olayları (event) tüketir.
- Kanal (channel): Kaynak tarafından alınan olayları depolar.
- Sink: Olayları kanaldan alır ve bunları haricî bir depoya (yani hedefe) yazar.

Apache Flume’un seçimi, ele alınması gereken birtakım özgül mimari kaygıları gündeme getirir:

- Haricî kaynaklardan veri alma mekanizmasının seçilmesi
- Kaynak (Source) elemanında kullanılacak belirli girdi formatlarının seçilmesi
- Olayların saklanacağı dosya veri formatının seçilmesi
- Olayların kanal içinde yönlendirilmesi (channeling) için kullanılacak mekanizmanın seçilmesi
- Veri Kaynağı (Data Source) elemanları için bir dağıtım topolojisinin (deployment topology) belirlenmesi

Bu özgül mimari kaygıların ele alınması, aşağıdaki kalite niteliklerinin (quality attributes) karşılanmasına katkı sağlayacaktır:

- QA-1 (Performans)
- QA-7 (Ölçeklenebilirlik)
- QA-9 (Genişletilebilirlik)
- QA-10 (Kullanılabilirlik / Erişilebilirlik)

### 5.3.4.2 Adım 3: İyileştirilecek Bir veya Daha Fazla Sistem Elemanını Seçme

Bu yinelemede odak, Flume’un yapısındaki elemanlar üzerindedir.

### 5.3.4.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı Seçme

Bu yinelemede kararların çoğu somutlaştırma (instantiation) ile ilgilidir; zira esas olarak Flume tarafından hâlihazırda tanımlanmış elemanların yapılandırılmasını içerirler. Seçime dayalı tek tasarım kararı, kullanılabilirlik (availability) ve performans kalite niteliklerini karşılamak için taktikler (tactics) seçmeyi içerir.

---

## 5.3 Tasarım Süreci (devam)

### Verilen Tasarım Kararları ve Konumu

**Karar:** Flume’u ajan/toplayıcı (agent/collector) konfigürasyonunda kullan. Ajanlar web sunucularıyla aynı yerde (co-located) konuşlandırılır ve toplayıcı (collector) Veri Akışı (Data Stream) elemanında çalışır.

**Gerekçe ve Varsayımlar:**  
Bir Flume örneği iki modda çalışabilir: Ajan (agent) olarak (doğrudan veri kaynaklarıyla aynı yerde) veya toplayıcı (collector) olarak (birden fazla ajandan veri akışlarını birleştirir ve hedeflere yazar).  
Bu iki moddan hareketle Flume farklı konfigürasyonlarda kullanılabilir. Karar, Flume’u hem ajan hem toplayıcı konfigürasyonunda kullanmaktır: Ajanlar veri kaynaklarıyla aynı yerde konumlandırılır ve Toplayıcı (Collector) Veri Akışı elemanında çalışır.

**Alternatif**

- Flume ajanları her web sunucusundadır ve olayları doğrudan sink’lere yazar (toplayıcı yok).

**Elendiği Neden**

- Hedeflere (HDFS ve Elasticsearch) 300+ eşzamanlı bağlantıdan yoğun trafik üretir. HDFS üzerinde her web sunucusu için çok sayıda dosya oluşturur; bu, HDFS gibi dağıtık bir dosya sistemi için (birden çok web sunucusundan veriyi birleştiren daha büyük dosyalar yerine) optimal değildir.

**Alternatif**

- Flume toplayıcıları olayları doğrudan web sunucularından alır (ajan yoktur) ve sink’lere yazar.

**Elendiği Neden**

- Failover modu desteklemez. Bir toplayıcı düğümünün çökmesi durumunda, bağlı web sunucuları alıcıyı kaybedecektir.

---

**Karar:** Yük dengelemeli (load-balanced), failover destekli katmanlı (tiered) bir konfigürasyon kullanarak “hesaplamaların birden çok kopyasını sürdürme (maintaining multiple copies of computations)” taktiğini tanıt.

**Gerekçe ve Varsayımlar:**  
Olası topoloji alternatifleri arasından, performans (QA-1, saniyede 15.000 olay) ve kullanılabilirlik (QA-10, tekil hata noktası olmaması) kalite niteliği senaryolarına dayanarak seçilen topoloji, yük dengelemeli ve failover destekli katmanlı bir topolojidir.

**Alternatif**

- Toplayıcının çoğaltılmaması

**Elendiği Neden**

- Bu, performans ve kullanılabilirliği düşürecektir.

> **💬 Çevirmen notu:** “Maintaining multiple copies of computations” taktiği, kritik iş yüklerinin birden fazla düğümde paralel olarak yürütülmesi ve gerektiğinde bunlardan birinin devreye girerek hizmet sürekliliğini sağlaması yaklaşımını ifade eder.

### 5.3.4.4 Adım 5: Mimari Öğeleri Örnekle, Sorumlulukları Ata ve Arayüzleri Tanımla

Bu yinelemede verilen örnekleme (instantiation) tasarım kararları aşağıdaki tabloda özetlenmektedir:

| Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar | Alternatif | Elenme Nedeni |
| --- | --- | --- | --- |
| Apache HTTP Sunucusu’ndan erişim (access) ve hata (error) günlüklerini girdi formatı olarak kullan | Sistem gereksinimleri, web sunucu yükü, kullanıcı aktiviteleri ve hatalar gibi günlüklerin (logların) toplanmasını ve analiz edilmesini içerir. Gerçekte veri kaynağı türlerinin sayısı onlarca (hatta bazen yüzlerce) olabilir. Kanıt niteliğinde kavram kanıtlama (proof-of-concept) geliştirmesi için tek bir veri kaynağı türü dikkate alınmıştır: bir Apache HTTP sunucusu (“web sunucusu”). Toplanacak veriler; erişim günlüğü (access log) üzerinden izlenecek kullanıcı aktivitelerini ve hata günlüğü (error log) üzerinden toplanacak sistem hatalarını içerir. Web sunucusu erişim günlüğü, sunucu tarafından işlenen tüm istekleri kaydeder. Bir günlük girdisi şu şekilde görünebilir: `143.21.52.246 - - [19/Jun/2014:12:15:17 +0000] "GET /test.html HTTP/1.1" 200 341 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) Gecko/20110421 Firefox/6.0a1".` Bu örnek şu veri alanlarından oluşur: istemci IP adresi, istemci kimliği, kullanıcı ID’si, zaman damgası (timestamp), istek metodu, istek URL’si, istek protokolü, yanıt kodu, yanıt boyutu, yönlendiren (referrer), kullanıcı aracısı (user agent). Web sunucusu hata günlüğü ise tanı (diagnostic) bilgisi gönderir ve kullanıcı isteklerini işlerken karşılaştığı hataları kaydeder. Örneğin: `[19/Jun/2014:14:23:15 +0000] [error] [client 50.83.180.156] Directory index forbidden by rule: /home/httpd/` Bu örnek şu veri alanlarından oluşur: zaman damgası, önem düzeyi (severity level), istemci IP adresi, mesaj. Daha ileri veri modelleme ve teknoloji yapılandırması (technology configuration) bu iki günlük türüne ve tanımlanan alanlara dayanacaktır. | — | — |
| Günlük dosyalarını Flume ajanının kaynak öğesindeki bir IP portu üzerinden yönlendir (pipe); Flume ajanında IP portu üzerinden (örneğin syslog kullanarak) veri akışını yapılandır | Apache Flume, günlük verilerini bir IP portu üzerinden yönlendirecek şekilde yapılandırılır (örneğin syslog kullanılarak). | Bir günlük dosyasından okuma (örn. `tail -F access_log` komutunu çalıştırarak) | Bu seçenek en basit gibi görünür, ancak olay teslimini garanti etmez (olaylar kaybolabilir); bu da Flume kullanıcı rehberinde açıkça belirtilmiştir. |

> **💬 Çevirmen notu:** Burada “pipe” ve “piped” ifadeleri, logların bir dosyadan okunmak yerine bir ağ portuna akıtılması ve Flume’un bu porttan okuması anlamında kullanılıyor.

---

#### 5.3 Tasarım Süreci

| Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar |
| --- | --- |
| Ajanlar ve toplayıcı (collector) için olay yönlendirme (event channeling) yöntemlerini belirle; nihai kararı prototipleme ile ver | Source (Kaynak) öğesinden alınan olaylar Channel (Kanal) öğesinde ara depolanır (staged). Flume şu anda kanalı yapılandırmak için üç olası seçenek sunmaktadır: 1. **Bellek kanalı (Memory channel):** Bellek içi kuyruk; daha hızlıdır, ancak bir Flume süreci çöktüğünde bellek kuyruğunda kalan olaylar kurtarılamaz. 2. **Dosya kanalı (File channel):** Kalıcıdır ve yerel dosya sistemi tarafından yedeklenir. 3. **Apache Kafka:** Kafka’nın dağıtık ve yüksek erişilebilirlikte bir kanal olarak görev yaptığı bir yaklaşımdır. Bu seçenekler arasındaki seçim, aslında performans ile erişilebilirlik (availability) (veya bazen dayanıklılık/durabilite olarak adlandırılır) arasındaki “klasik” ödünleşimidir (tradeoff). Açıkça belirtilmiş bir dayanıklılık (durability) senaryomuz olmasa da, gelecekteki sistem genişlemesiyle (UC-6, güvenlik raporları) birlikte bu gereksinimin daha kritik hâle geleceğini biliyoruz. Bu, mimari bir endişeye (architectural concern) örnektir; çünkü herhangi bir gereksinim dokümanında görünmez, fakat mimarın yine de ele alması gerekir. Bu seçenekler ve performans sonuçlarına ilişkin kamuya açık bir bilgi bulunmadığı göz önüne alındığında, bu durum prototipleme yapıp sonuçlara göre karar vermek için iyi bir adaydır. Prototipleme ve performans ölçümünün bir diğer gerekçesi de gerekli donanım kaynaklarını hesaplama ihtiyacıdır. Sonuç olarak yeni bir endişe tanımlanmış ve iş listesine (backlog) eklenmiştir: ■■ **CRN-3:** Veri modelleme ve kilit sistem öğeleri için kavram kanıtlama (proof-of-concept) prototipleri geliştirme |
| HDFS sink içinde ham veriyi depolamak için belirli bir dosya formatı olarak Avro seç | Hadoop tabanlı bir çözüme tasarım yapılırken verilmesi gereken kararlardan biri, en uygun dosya formatının seçilmesidir. Hadoop, saklanan verilere ve kullanım senaryolarına bağlı olarak farklı işlevler, sıkıştırma ve performans sonuçları sunan çeşitli formatları destekler. Bu durumda temel senaryolar, performans (QA-1, saniyede 15.000 olay), ölçeklenebilirlik (QA-7, yaklaşık 60 TB ham veri) ve genişletilebilirlik (QA-9, yeni veri kaynaklarının eklenmesi) gibi kalite nitelikleri (quality attributes) ile ilgilidir. Bu gereksinimleri dosya formatı özelliklerine dönüştürdüğümüzde; bunlar, performans (Data Stream’in veriyi ne kadar hızlı itebileceği), sıkıştırma faktörü (daha az depolama alanı) ve şema evriminin (schema evolution) kolaylığı (yeni günlük formatları eklerken veya mevcut olanları değiştirirken) tarafından etkilenecektir. Avro’yu seçiyoruz; çünkü zengin veri yapıları destekler, iyi sıkıştırma seviyeleri sunar (Snappy sıkıştırma kodlayıcısı ile) ve şema değişikliklerine uyum sağlayabilecek kadar esnektir (verinin şemasıyla birlikte saklandığı, kendini tanımlayan bir format kullanarak). |

| Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar | Alternatif | Elenme Nedeni |
| --- | --- | --- | --- |
| — | — | Metin dosyası (düz metin, CSV, XML, JSON) | Sıkıştırma oranı, ikili (binary) dosya formatlarına (örn. Avro) kıyasla zayıftır. Ayrıca, HDFS bloğu boyutundan daha büyük dosyalar depolanırken gerekli olan blok sıkıştırmayı (block compression) desteklemez. |
| — | — | SequenceFile | Esnek şema evrimini desteklemez. İkili anahtar/değer (key/value) çiftlerinden oluşur ve verinin yanında üstveri (metadata) saklamaz. |
| — | — | RCFile | Bu Hadoop sütunlu (columnar) dosya formatı şema evrimini desteklemez ve yazma işlemleri, sütunsal olmayan formatlara göre daha fazla CPU ve bellek gerektirir. |
| — | — | ORCFile | İyileştirilmiş RCFile, daha iyi sıkıştırma ve daha hızlı sorgulama sunar; fakat şema evrimi açısından RCFile ile aynı dezavantajlara sahiptir ve yazma performansı pahasına çalışır. |
| — | — | Parquet | Parquet, kısmen şema evrimini destekleyen sütunlu bir dosya formatıdır; ancak yine de yazma işlemleri, sütunsal olmayan dosya formatlarına kıyasla daha yavaştır. |

---

### 5.3.4.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 5.8, örnekleme kararlarının sonucunu göstermektedir.

![Şekil 5.8](/home/runner/workspace/scripts/dsa_figs/sekil_5_8.png){width=9.67cm}


**Öğe** | **Sorumluluk**
---|---
Flume ajanı | Bir web sunucusu tarafından üretilen günlük olaylarını tüketmek, metin tabanlı günlük girdilerini ayrı alanlara bölmek ve ayrıştırılmış (parsed) olay kayıtlarını bir toplayıcıya iletmek.
Flume toplayıcısı (collector) | Birden fazla ajan’dan olay kayıtlarını yük dengeleme (load-balanced) ve hataya dayanıklı (fault-tolerant) bir biçimde toplamak ve bunları kalıcılık (persistency) ve daha ileri işleme (processing) için hedeflere (HDFS ve Elasticsearch) iletmek.

Aşağıdaki şema, katmanlar ve başlıca Flume bileşenleri arasındaki veri akışını göstermektedir:

- **Uygulama Katmanı (Application Tier)**
- **Flume Collector Katmanı (Flume Collector Tier)**
- **Depolama Katmanı (Storage Tier)**

```text
WebServer 1 (Data Source)

Flume Agent
  netcat src (access)
  Memory channel (access)
  netcat src (error)
  Memory channel (error)
  avro sink (access)
  avro sink (error)

BATCH Layer

Data Stream Collector
  Flume Agent
    Memory channel (access)
    netcat src (error)
    Memory channel (error)
    avro src (access)
    avro sink (access)
      + log parsing
    avro sink (error)
    avro src (error)
    netcat src (error)
    Memory channel (error)
    replicating
    Memory channel
    ES sink (access)
    Memory channel
    HDFS sink (error)

HDFS
ES
```

> **💬 Çevirmen notu:** Şekil 5.8’deki metin, Flume konfigürasyonundaki `source`/`channel`/`sink` elemanlarını ve bunların HDFS ile Elasticsearch’e (ES) veri gönderen akışını özetleyen bir bileşen/görünüm (view) taslağıdır.

```mermaid
flowchart LR
    subgraph SPEED[HIZ KATMANI (SPEED Layer)]
        direction LR
        WSN[WebServer N<br/>(Veri Kaynağı)]
        WS2[WebServer 2<br/>(Veri Kaynağı)]
        NCN[netcat kaynağı<br/>(erişim)]
        NC2[netcat kaynağı<br/>(erişim)]
        FA[Flume Aracısı<br/>(Flume Agent)]
        MC1[Hafıza kanalı<br/>(Memory channel)]
        MC2[Hafıza kanalı<br/>(Memory channel)]
        ESsinkE[ES alıcısı (sink)<br/>(hata)]
        ES[(Elasticsearch)]
        HDFSs[HDFS alıcısı (sink)<br/>(erişim)]
        AvroAcc[avro alıcısı (sink)<br/>(erişim)]
        AvroErr[avro alıcısı (sink)<br/>(hata)]
        LB[LB + failover]
        HDFS[(HDFS)]

        WSN -->|erişim| NCN
        WS2 -->|erişim| NC2
        NCN --> FA
        NC2 --> FA
        FA --> MC1
        FA --> MC2
        MC1 -->|json| ESsinkE --> ES
        MC1 --> HDFSs --> HDFS
        MC2 --> AvroAcc
        MC2 --> AvroErr
        FA --> LB
    end
```

Açıklama:
- Düğümler arası veri akışı
- Aynı düğüm içindeki Flume bileşenleri arasındaki veri akışı

+ log ayrıştırma (log parsing)

---

Şekil 5.8 Üçüncü yinelemenin somut tasarım kararları

---

## 5.3 Tasarım Süreci

### 5.3.4.6 Adım 7: Geçerli Tasarımın Analizini Gerçekleştir ve Yinelemeyi Gözden Geçir  
Amaç ve Tasarım Amacına Ulaşım

Aşağıdaki Kanban tablosu, tasarım ilerlemesini ve yineleme sırasında verilen
kararları özetlemektedir. Bir önceki yinelemede tamamen ele alınmış olan sürücüler
(drivers) gösterilmemiştir.

|                      | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Verilen Tasarım Kararları |
|----------------------|--------------|-------------------|--------------------|----------------------------------------------|
| UC-1                 |              |                   |                    |                                              |
| UC-2                 |              |                   |                    |                                              |
| UC-3                 |              |                   |                    |                                              |
| UC-4                 |              |                   |                    |                                              |
| CRN-3                |              |                   |                    | Veri Akışı (Data Stream) elemanının iyileştirilmesi. Bu kullanım senaryolarına katılan diğer elemanlar hakkında hâlâ karar verilmesi gerekmektedir. |
| QA-1                 |              |                   | ✔                  | Flume yük dengelemeli (load-balanced), failover katmanlı (tiered) yapılandırma seçilmiştir. |
| QA-9                 |              |                   | ✔                  | Ham veriyi depolamak için Flume ve Avro formatının kullanılması. |
| QA-10                |              |                   | ✔                  | Flume yük dengelemeli, failover katmanlı yapılandırma seçilmiştir. Bu senaryoya katılan diğer elemanlar hakkında hâlâ karar verilmesi gerekmektedir. |
| CRN-1                |              |                   |                    | Flume toplayıcı (collector) ve depolama için katmanlar tanımlanmıştır. Bu yinelemede tanıtılmış yeni bir mimari konudur: veri modelleme ve kilit sistem elemanları için kavram kanıtlama (proof‑of‑concept) prototiplerinin geliştirilmesi. Bu noktada ilgili bir karar verilmemiştir. |

> **💬 Çevirmen notu:** “CRN” burada metnin önceki kısımlarında tanımlanmış mimari kaygı/konu (concern) kimlikleridir; tablo bir Kanban durum panosu olarak okunmalıdır.

---

### 5.3.5 Yineleme 4: Sunum Katmanının (Serving Layer) İyileştirilmesi

Bu bölümde, tasarım sürecinin dördüncü yinelemesinde, nitelik temelli tasarımın
(Attribute‑Driven Design, ADD) her adımında gerçekleştirilen etkinliklerin
sonuçlarını sunuyoruz.

Bu yinelemede iyileştirme için Batch Katmanı değil, Sunum Katmanı (Serving Layer)
seçilmiştir; çünkü gereksinimlere ulaşamama riski bu katman için daha yüksektir.
Bu katman doğrudan UC-3 ve UC-4 kullanım senaryoları ile, performans ve
ölçeklenebilirliğin kritik faktörler olduğu bir dizi kalite niteliği (quality attribute)
senaryosuna dahildir.

Önceki yinelemede olduğu gibi, tasarım etkinlikleri prototiplerin oluşturulmasını
içermektedir. Bu yinelemede, kullanıcı arayüzü (UI) prototipleri de oluşturulmuştur.
Bunun en az iki nedeni vardır:

- Kullanıcılardan erken geri bildirim alınmasını kolaylaştıracak, bu da
  gereksinimlerin güncellenmesine yardımcı olabilecektir.
- Veri görselleştirme senaryoları, çoğu zaman veri modelleme üzerinde etkiye
  sahiptir.

---

## 5.3 Tasarım Süreci

### 5.3.5.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu yinelemenin amacı, veri modelleme ve kilit sistem elemanları için kavram
kanıtlama (proof‑of‑concept) prototiplerinin geliştirilmesi (CRN-3) şeklinde yeni
tanımlanan mimari kaygıyı ele almak ve böylece tarihsel verinin analizi ve
görselleştirilmesiyle ilişkili birincil kullanım senaryolarını ve sistem gereksinimlerini
karşılamaktır. Bu kullanım senaryoları şunları içerir:

- UC-3
- UC-4

Bu kullanım senaryolarıyla ilişkili kalite niteliği senaryoları şunlardır:

- QA-4 (Performans)
- QA-5 (Performans)
- QA-7 (Ölçeklenebilirlik)
- QA-8 (Ölçeklenebilirlik)

### 5.3.5.2 Adım 3: İyileştirilecek Bir veya Daha Fazla Sistem Elemanını Seçme

Bu yinelemede iyileştirilen elemanlar, tarihsel veriyi destekleyen elemanlardır; bunlar
Sunum Katmanı (Serving Layer) elemanları olan Ad Hoc ve Statik Batch
Görünümlerini (Ad Hoc and Static Batch Views) içerir. Her iki tip eleman da aynı
teknolojiyi (Impala) kullandığından, bu yinelemede verilen kararlar her iki tür elemanı
da etkiler.

### 5.3.5.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı Seçme

Önceki yinelemede olduğu gibi, buradaki tasarım etkinlikleri, elemanlarla ilişkilendirilen
teknolojilerin yapılandırılmasını içermektedir. Bu nedenle yeni tasarım kavramları
seçilmemiştir ve tüm kararlar somutlama (instantiation) kategorisine aittir.

### 5.3.5.4 Adım 5: Mimari Elemanları Somutlaştırma, Sorumlulukları Atama ve Arayüzleri Tanımlama

Bu yinelemede, tasarım kavramları seçilen teknolojilerin en iyi uygulamalarına
(dayanarak) somutlaştırılır.

**Tasarım Kararı ve Yeri**

**Gerekçe ve Varsayımlar**

**Batch Görünümlerinde Impala için dosya formatı olarak Parquet seçilmesi**

Batch Görünümleri için bir dosya formatı seçme süreci, önceki yinelemede ham veri
depolama için bir format seçtiğimiz sürece benzerdir. Ancak veri kullanım senaryosu
biraz farklıdır. Önceki durumda konu, hızlı yazma, veriyi etkin biçimde depolama ve
veri formatlarını genişletme idi. Bu durumda odak, hızlı sorgulama üzerinedir (QA-4,
5 saniyeden kısa rapor yükleme; QA-5, 2 dakikadan kısa ad hoc sorgu yürütme
süresi); buna karşın ölçeklenebilirlik (QA-8, yaklaşık 90 TB birikimli veri) ve
genişletilebilirlik (QA-9, yeni veri kaynaklarının eklenmesi) sürücüleri hâlâ
geçerlidir. Mevcut tüm alternatifler içinde Parquet dosya formatı, bu gereksinimleri
karşılamak için en umut verici seçenek gibi görünmektedir.

---

**Tasarım Kararı ve Yeri**

**Gerekçe ve Varsayımlar**

**Batch Görünümlerinde Impala için dosya formatı olarak Parquet seçilmesi**

Parquet’te, sütun bazlı (columnar) bir yapı, bilgisayar kümeleri üzerinde ilişkisel
tabloları temsil eder ve ad hoc veri keşfi ve statik raporlar için önemli olan hızlı sorgu
işleme amacıyla tasarlanmıştır. Buna ek olarak Parquet, ikinci yinelemede etkileşimli
sorgu motoru için birincil teknoloji olarak seçtiğimiz Impala için optimize edilmiştir.
Son olarak, iyi bir sıkıştırma oranı sağlar ve yapının sonuna yeni sütunlar ekleyerek
bazı şema genişletmelerine izin verir.

**Alternatif**

**Elendiği Neden**

Metin dosyası  
(düz metin, CSV, XML,
JSON)

- Okumalar için yavaştır, özellikle de tekil sütunlar sorgulanırken.  
- Ayrıca, HDFS bloğu boyutundan büyük dosyalar depolanırken gerekli olan blok
  sıkıştırmayı desteklemez.

SequenceFile

- Okumalar için yavaştır, özellikle de tekil sütunlar sorgulanırken.

RCFile

- Hadoop’da benimsenen ilk sütun bazlı dosya formatıdır.  
- Şema evrimini (schema evolution) desteklemez.

ORCFile

- RCFile’dan daha iyi sıkıştırma ve daha hızlı sorgulama sunar, ancak şema evrimi
  açısından RCFile ile aynı dezavantajlara sahiptir.  
- Parquet ile karşılaştırıldığında sıkıştırma oranı daha iyidir, fakat sorgu performansı
  daha yavaştır.  
- Diğer önemli bir kısıt, Impala tarafından desteklenmemesidir.

Avro

- Avro her ne kadar Hadoop için en iyi çok amaçlı (multipurpose) depolama formatı
  olarak kabul edilse de, sorgu performansı RCFile, ORCFile ve Parquet gibi sütun
  bazlı formatlarla karşılaştırıldığında fark edilir derecede daha yavaştır.

---

## 5.3 Tasarım Süreci

**Tasarım Kararı ve Yeri**

**Gerekçe ve Varsayımlar**

Batch Görünümleri
bileşeninde veri modeli
olarak yıldız şemasını
(star schema) kullanın

Önceki iterasyonda, Batch Görünümleri (Batch Views) bileşenleri için tek teknoloji olarak Impala’yı seçtik; bu seçim hem statik raporları (UC-3, 6) hem de ad hoc sorgulamayı (UC-4) etkiler. Yıldız şeması tekniği iki nedenle seçildi:

- Impala analitik sorgular için tasarlanmıştır; bu nedenle yıldız şeması veri modelleme için doğal olarak iyi destek sağlar.
- BI araçlarıyla birlikte ad hoc sorgulama, sorgu karmaşıklığını basitleştirmek ve bunun sonucu olarak daha hızlı sorgu performansına izin vermek için verinin iyi modellenmesini gerektirir.

Bizim durumumuzda, yıldız şeması, büyük tablolar arasındaki join’lerden kaçınmak amacıyla küçük boyutlu (satır sayısı açısından) boyut tablolarına sahip olacak şekilde tasarlandı; zira bu tür join’ler tipik olarak yüksek miktarda sistem kaynağı tüketir ve sorgu yürütme performansını etkiler. Küçük boyutlu tablolar belleğe sığabilir ve join’ler daha etkin şekilde gerçekleştirilebilir.

#### 5.3.5.5

Alternatif

Elendiği Neden

Düz tablolar
(flat tables)

Düz tablolar tipik olarak tüm ölçüleri ve boyut özniteliklerini içeren, geniş ve denormalize tablolar biçiminde temsil edilir.

Düz tablolar, büyük veri hacimleri üzerinde sorgu çalıştırılırken önemli performans sorunlarına yol açabilir.

### Adım 6: Görünümleri Taslak Haline Getir ve Tasarım Kararlarını Kaydet

Şekil 5.9, Impala ve Parquet kullanılarak gerçekleştirilen yıldız şeması veri modelini göstermektedir.

![Şekil 5.9](/home/runner/workspace/scripts/dsa_figs/sekil_5_9.png){width=11.71cm}


Şekil 5.10’daki ekran görüntüsü, kurumsal bir BI aracı üzerinden olası bir görünümü göstermek için Tableau ile gerçekleştirilmiş örnek bir statik raporu sunar. Rapor, Parquet’te depolanan ve ODBC arayüzü üzerinden Impala tarafından sağlanan test verisi kullanılarak oluşturulmuştur.

![Şekil 5.10](/home/runner/workspace/scripts/dsa_figs/sekil_5_10.png){width=11.85cm}


---

Şekil 5.9 Yıldız şeması, Impala ve Parquet ile gerçekleştirilmiş

```text
dim_request
request_id          <pi>
request_method
request_url
request_protocol

dim_user_agent
user_agent_id <pi>  int
user_agent_full     string
browser             string
device_type         string
os                  string

dim_referrer
referrer_id   <pi>  int
referrer_url        string
referrer_site       string

dim_city
city_id       <pi>  int
city                string
region              string
country             string

dim_zip_code
zip_code_id  <pi>   int
zip_code            string

dim_message
message_id   <pi>   int
message_url         string

fact_access
client_ip           string
request_id   <fi5>  int
referrer_id  <fi4>  int
user_agent_id<fi1>  int
city_id      <fi2>  int
zip_code_id  <fi3>  int
latitude            string
longitude           string
event_timestamp     Timestamp
server_host         string
requst_time         int
response_code       smallint
response_size       int

fact_error
event_timestamp     Timestamp
message_id   <fi1>  int
server_host         string
client_ip           string
level               string
```

> **💬 Çevirmen notu:** `request_id`, `user_agent_id` gibi `<pi>` ve `<fiX>` işaretleri birincil anahtar (primary key) ve yabancı anahtar (foreign key) göstergeleridir.

Şekil 5.10 Tableau ile gerçekleştirilmiş örnek statik rapor

---

## 5.4 Özet

### 5.3.5.6 Adım 7: Mevcut Tasarımın Analizini Gerçekleştir ve İterasyonu Gözden Geçir

#### Tasarım Amacı ve Amacın Gerçekleştirilmesi

Aşağıdaki Kanban tablosu, iterasyon sırasında kaydedilen tasarım ilerlemesini ve alınan kararları özetlemektedir. Önceki iterasyonda tamamen ele alınmış sürücülerin (driver) burada gösterilmediğine dikkat edin.

|                    | Adreslenmedi | Kısmen Adreslendi | Tamamen Adreslendi | İterasyon Sırasında Alınan Tasarım Kararları |
|--------------------|-------------:|-------------------:|--------------------:|---------------------------------------------|
| UC-3               |              | ✔                 |                     | Bu kullanım senaryosunda kullanılan Sunum Katmanının (Serving Layer) iyileştirilmesi. Bu kullanım senaryolarına katılan diğer ögelerle ilgili kararların hâlâ verilmesi gerekmektedir. |
| UC-4               |              | ✔                 |                     |                                             |
| QA-4               |              |                   | ✔                   | Parquet ve yıldız şeması kullan. Performans testleri hâlâ gereklidir ve bu nedenle yeni bir kaygı (concern) ortaya çıkmıştır: CRN-4: Performans testleri geliştir. |
| QA-5               |              |                   | ✔                   |                                             |
| QA-8               |              |                   | ✔                   |                                             |
| CRN-1              | ✔            |                   |                     | İlgili bir karar alınmamıştır.              |
| CRN-3              |              | ✔                 |                     | Sunum Katmanındaki ögeler için veri modelleme ve kavram kanıtlama (proof-of-concept) prototipleri geliştirilmiştir, ancak aynı etkinliğin Hız Katmanındaki (Speed Layer) ögeler için de tamamlanması gerekmektedir. |

## 5.4 Özet

Bu bölümde, görece yeni bir alan olan Büyük Veri (Big Data) için ADD 3.0’ın (Attribute-Driven Design) kullanımına ilişkin kapsamlı bir örnek sunduk. Bu örneğin gösterdiği gibi, mimari tasarım, kalite niteliklerinin (quality attributes) sağlanmasını temin etmek için çok sayıda ayrıntılı kararın alınmasını gerektirebilir.

Ayrıca bu örnek, çok sayıda kararın birçok farklı desen (pattern) ve teknoloji bilgisine dayandığını da gösterir. Alan ne kadar yeni ise, o alan için önceden var olan bilgi (örneğin tasarım kavramları kataloğu, desen kitapları ve referans mimariler) bulunmama olasılığı o kadar yüksektir. Böyle bir durumda, ya kendi muhakemenize ve deneyiminize güvenmeli ya da deneyler yapıp prototipler inşa etmelisiniz. Her iki durumda da bu kararların verilmesi gerekir.

Bu ADD örneği, Bölüm 4’te sunulan örnekten şu açıdan da farklıdır: Arayüz belirtimlerini türetmenin bir aracı olarak dizge diyagramları (sequence diagram) oluşturmaya nispeten az zaman ve çaba harcadık. Burada sunulan örnek, bileşen sayısı sınırlı, görece basit bir veri akışı (data-flow) mimarisine dayanıyordu; bu nedenle bileşenler arasındaki ilişkileri anlamak için dizge diyagramlarına ihtiyaç yoktu. Ögeler arasındaki “sözleşmeler” (contracts), İterasyon 3’ün adım 5’inde (Bölüm 5.3.4.4’te açıklanan) örneklendirildiği üzere, değiş tokuş edilen bilgi tarafından belirlendi.

---

Bölüm 5—Vaka Çalışması: Büyük Veri Sistemi

## 5.5 Ek Okumalar

Veri ambarı (data warehouse) tasarımı kapsamlı biçimde incelenmiştir. İki iyi yaklaşım R. Kimball ve M. Ross, *The Data Warehouse Toolkit*, 3. baskı, Wiley, 2013; ve W. Inmon, *Building the Data Warehouse*, 4. baskı, Wiley, 2005’te belgelenmiştir.

Lambda mimarisi ilk olarak N. Marz ve J. Warren, *Big Data: Principles and Best Practices of Scalable Realtime Data Systems*, Manning, 2015’te sunulmuştur.

Ölçeklenebilirlik için nasıl mühendislik yapılacağına dair iyi bir tartışma M. Abbott ve M. Fisher, *The Art of Scalability: Scalable Web Architecture, Processes, and Organizations for the Modern Enterprise*, Addison-Wesley, 2010’da bulunabilir.

P. Sadalage ve M. Fowler, *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*, Addison-Wesley, 2009.

Mimari tasarım sürecinin bir parçası olarak ne zaman ve nasıl prototip yapılacağına ilişkin bir tartışma H-M Chen, R. Kazman ve S. Haziyev, “Strategic Prototyping for Developing Big Data Systems”, *IEEE Software*, Mart/Nisan 2016’da bulunabilir.

Bu vaka çalışmasında kullanılan birçok referans mimari ve teknolojiyi içeren bir tasarım kavramları kataloğu, Smart Decisions Game’in bir parçasıdır ve H. Cervantes, S. Haziyev, O. Hrytsay ve R. Kazman, “Smart Decisions Game”, http://smartdecisionsgame.com adresinde bulunabilir.

---

# 6 Vaka Çalışması: Bankacılık Sistemi

Bölüm 4 ve 5’in her ikisi de sıfırdan geliştirme (greenfield development) örnekleriydi. Gerçekte, bu tür geliştirme nispeten nadirdir. Çoğu zaman, bir mimar olarak siz, sıfırdan bir sistem yaratmak yerine mevcut bir sistemi evrimleştirme üzerinde çalışırsınız. Bu bölümde, olgun bir alandaki (Bölüm 3.3.3’te tartışıldığı gibi) bir brownfield sistem için ADD 3.0’ın kullanımına ilişkin bir örnek sunuyoruz. Önce iş bağlamını (business context) sunuyor, ardından projenin mevcut mimari dokümantasyonunu inceliyoruz. Bunu, sistemi evrimleştirmek için ADD iterasyonları sırasında gerçekleştirilen etkinliklerin adım adım özeti izliyor. Bu gerçek bir sistemdir, ancak aktörlerin kimliklerinin korunması için bazı ayrıntılar değiştirilmiştir.

## 6.1 İş Vaka Analizi (Business Case)

2010 yılında, bir Latin Amerika ülkesinin hükümeti, bankacılık kurumlarının hesap ekstrelerini dijital olarak imzalamasını zorunlu kılan bir düzenleme yayımladı. Bu düzenlemeye uyum sağlamak için “ACME Bankası”, başlıca amacı dijital olarak imzalanmış hesap ekstrelerinin üretilmesi olan ve BankStat adını vereceğimiz bir yazılım sisteminin geliştirilmesini sipariş etti.

Şekil 6.1, BankStat sisteminin nasıl çalıştığını gösteren bir bağlam diyagramı (context diagram) sunmaktadır. Sistemin çekirdeğinde, ham hesap ekstresi bilgisini bir veri kaynağından (harici bir veritabanı) alan ve ardından bu veriler üzerinde bir dizi doğrulama gerçekleştirerek hesap ekstrelerini üreten ve bunları harici bir sağlayıcı tarafından dijital imzaya hazırlan hale getiren bir yığın (batch) işlem bulunmaktadır. Ekstreler sağlayıcıya gönderilir ve sağlayıcı imzalanmış hesap ekstrelerini geri döner. Bu ekstreler, daha sonra müşterilere ekstrelerin gönderilmesini de içeren ek işlemler için BankStat tarafından saklanır. Bu yığın işlem, ayda bir kez otomatik olarak tetiklenir ve çalışması sırasında yaklaşık 2 milyon hesap ekstresi işlenir.

![Şekil 6.1](/home/runner/workspace/scripts/dsa_figs/sekil_6_1.png){width=11.82cm}


Bu sistem için aşağıdaki kalite niteliği senaryoları (quality attribute scenarios) birincil öneme sahiptir:

- **Güvenilirlik (Reliability):** Normal çalışma koşulları altında, yığın işlem her zaman %100 olarak baştan sona eksiksiz olarak yürütülür.
- **Performans (Performance):** Normal çalışma koşulları altında, yığın işlem başladığında 2 milyon hesap ekstresi en fazla bir saat içinde okunur, işlenir ve imzalama sağlayıcısına gönderilir.
- **Kullanılabilirlik (Availability):** Normal işleme sırasında, veri kaynağından bilgi okurken veya bilgiyi dijital imza için gönderirken bir hata oluşabilir. Bu durumda, yöneticiye bir bildirim gönderilir ve yönetici süreci elle yeniden başlatır. Süreç yeniden başlatıldığında, yalnızca henüz işlenmemiş olan bilgiler işleme tabi tutulur.

Hükümet tarafından konulan zaman kısıtları nedeniyle, sistemin yalnızca çekirdek yığın işlemi geliştirilerek üretime alınmıştır. Bununla birlikte, bu ilk sürüm, hesap ekstresi işlemenin durumunu izlemek, hatalı ekstrelerin yeniden işlenmesini talep etmek ve rapor üretmek için gerekli olan kullanıcı dostu bir arayüz sağlamamıştır. İlk sürümde, süreç yalnızca bir konsoldan elle başlatılıp durdurulabiliyordu. Sisteminin ikinci sürümü için ACME Bankası, bu eksikliklerin daha iyi ele alınabilmesi amacıyla BankStat sisteminin genişletilmesini talep etmiştir.

  
ŞEKİL 6.1 BankStat sistemi için bağlam diyagramı (context diagram)


## 6.1 İş Gerekçesi (Business Case)

Sistemin ikinci sürümü için mimari sürücüler (architectural drivers) aşağıdaki alt bölümlerde sunulmaktadır.

### 6.1.1 Kullanım Durumu (Use Case) Modeli

Şekil 6.2, BankStat’in ikinci sürümü için kullanım durumu modelini göstermektedir. Bu kullanım durumları aşağıda daha ayrıntılı olarak açıklanmaktadır:

![Şekil 6.2](/home/runner/workspace/scripts/dsa_figs/sekil_6_2.png){width=10.02cm}


| Kullanım Durumu | Açıklama |
|-----------------|----------|
| **UC-1: Ekstre sorgulama ve yeniden işleme (Query and reprocess statements)** | Kullanıcı elle belirli sayıda ekstreden yeniden işleme talep eder. Kullanıcı, yeniden işlenmesi gereken ekstreleri sorgulamak ve seçmek için ölçütler belirtir. Örneğin, ilgilendiği bir dönemi veya ekstrelerin durumunu (örneğin işlenmiş, imzalanmış, imzalanmamış) seçebilir. |
| **UC-2: Oturum açma (Log in)** | Kullanıcı sisteme oturum açar. |
| **UC-3: Rapor üretme (Generate report)** | Kullanıcı, süreçle ilgili raporlar üretir. |
| **UC-4: Kullanıcı kayıtlarını sorgulama (Query users log)** | Yönetici, belirli bir kullanıcının veya bir kullanıcı grubunun aktivitelerini göstermek için kullanıcı kayıtlarını sorgular. Bilgi, tarihler veya işlem türleri gibi ölçütler kullanılarak filtrelenebilir. |

ŞEKİL 6.2 BankStat sistemi için kullanım durumları (Anahtar: UML)

### 6.1.2 Kalite Niteliği Senaryoları (Quality Attribute Scenarios)

Aşağıdaki tablo, sistemin bu genişletmesi için dikkate alınan yeni kalite niteliği senaryosunu göstermektedir.

| ID   | Kalite Niteliği (Quality Attribute) | Senaryo | İlişkili Kullanım Durumu |
|------|-------------------------------------|---------|---------------------------|
| QA-1 | Güvenlik (Security)                | Bir kullanıcı herhangi bir anda sistem üzerinde herhangi bir işlem gerçekleştirir ve kullanıcının gerçekleştirdiği işlemlerin %100’ü, sistem tarafından işlem günlüğünde kaydedilir. | UC-4 |

### 6.1.3 Kısıtlar (Constraints)

Aşağıdaki tablo, sistemin bu genişletmesi için dikkate alınan kısıtları göstermektedir.

| ID    | Kısıt |
|-------|-------|
| CON-1 | Kullanıcıların hesapları ve yetkileri, bankadaki çeşitli uygulamalar tarafından kullanılan mevcut bir kullanıcı dizin sunucusu (user directory server) tarafından yönetilecektir. |
| CON-2 | Veri kaynağıyla iletişim JDBC kullanılarak gerçekleştirilecektir. |
| CON-3 | Dijital imza sağlayıcı sistemiyle iletişim web servisleri (web services) kullanılarak gerçekleştirilecektir. Bu web servisleri, hükümet tarafından belirlenmiş spesifikasyonlara uyan bir XML formatında bilgiyi alır ve geri döner. |
| CON-4 | Sisteme bir web tarayıcısı üzerinden erişilmelidir; ancak erişim yalnızca bankanın intraneti üzerinden mümkündür. |

### 6.1.4 Mimari Kaygılar (Architectural Concerns)

Aşağıdaki tablo, sistemin bu genişletmesi için başlangıçta dikkate alınan kaygıları göstermektedir.

| ID    | Kaygı |
|-------|-------|
| CRN-1 | Geliştirme ekibinin uzmanlığından yararlanmak için sistem Java ve Java ile ilişkili teknolojiler kullanılarak programlanmalıdır. |
| CRN-2 | Yeni işlevselliğin eklenmesi, mümkün olduğunca mevcut yığın işlem çekirdeğinde değişiklik yapılmasını önlemelidir. |

## 6.2 Mevcut Mimari Dokümantasyon (Existing Architectural Documentation)

Bu bölüm, mimaride yapılacak değişiklikler için ilgili bilgileri sağlayan sistem görünüşlerinin (views) basitleştirilmiş bir sürümünü sunmaktadır.

### 6.2.1 Modül Görünümü (Module View)

Şekil 6.3’te gösterilen paket diyagramı, sistem katmanlarını ve bu katmanların içerdiği modülleri betimlemektedir.

![Şekil 6.3](/home/runner/workspace/scripts/dsa_figs/sekil_6_3.png){width=11.78cm}


ŞEKİL 6.3 BankStat sistemindeki mevcut modüller ve katmanlar (Anahtar: UML)

Bu diyagramda gösterilen öğelerin sorumlulukları aşağıdaki tabloda açıklanmaktadır.

| Öğe | Sorumluluk |
|-----|------------|
| **Yığın İşleme Katmanı (Batch Processing Layer)** | Bu katman, yığın işlemini gerçekleştiren modülleri içerir. Bu bileşenler Spring Batch çatısı (framework) kullanılarak geliştirilmiştir. |
| **Veri Erişim Katmanı (Data Access Layer)** | Bu katman, Yığın İşleme Katmanı’ndaki modüller tarafından kullanılan yerel bir veritabanına veri kaydeden ve bu veritabanından veri alan modülleri içerir. |
| **İletişim Katmanı (Communications Layer)** | Bu katman, harici dijital imza sağlayıcısı ve hesap ekstresi veri kaynağıyla iletişimi destekleyen modülleri içerir. |
| **Yığın İş Koordinatörü (Batch Job Coordinator)** | Bu modül, yığın işlemin yürütülmesini koordine etmekten sorumludur; buna sürecin başlatılması ve bu sürece ilişkin farklı adımların çağrılması dahildir. |
| **İş Adımları (Job Steps)** | Bu modül, yığın işinin parçası olan “adımları” içerir. Bu adımlar, veri kaynağından alınan bilgilerin doğrulanması ve hesap ekstrelerinin üretilmesi gibi faaliyetleri gerçekleştirir. Bu tür adımlar genellikle veriyi okur, işler ve yazar. Veri, yerel veritabanından okunur ve yine bu veritabanına yazılır. |
| **Yerel Veritabanı Bağlayıcısı (Local Database Connector)** | Bu modül, yığın işlemi yürütülürken iş adımlarının bilgi alışverişi için kullandığı yerel veritabanına erişmekten sorumludur. Bu veritabanına, harici veri kaynağından ayırt etmek için “yerel” diyoruz; bu veritabanı yalnızca yerel (yani uygulama tarafından dahili olarak) kullanılır; farklı bir düğüme yerleştirilmiş olsa bile (bkz. bir sonraki bölüm). |

> **💬 Çevirmen notu:** “Batch process / batch job” kavramı, büyük hacimli verinin zamanlanmış toplu işlenmesi anlamına geldiği için “yığın işlem” ve “yığın iş” terimleri korunarak çevrilmiştir; bu terimler kitap boyunca tutarlı biçimde kullanılacaktır.

### Bildirimler Yöneticisi (Notifications Manager)

Bu modül, günlükleri (logları) yönetir ve harici sistemle iletişim hatası gibi sorunlar ortaya çıktığında bildirimler gönderir.

### Veri Kaynağı Bağdaştırıcısı (Data Source Connector)

Bu modül, ham banka hesap özeti bilgisini sağlayan harici veritabanına bağlanmaktan sorumludur.

### Sayısal İmza Sağlayıcı Bağdaştırıcısı (Digital Signature Provider Connector)

Bu modül, banka hesap özetlerinin sayısal olarak imzalanmasını gerçekleştiren harici sisteme erişmekten sorumludur.

## 6.2.2 Yerleştirim Görünümü (Allocation View)

Şekil 6.4’te gösterilen yerleştirim (deployment) diyagramı, düğümlerden (node) ve bunların ilişkilerinden oluşan bir yerleştirim görünümü sunmaktadır.

![Şekil 6.4](/home/runner/workspace/scripts/dsa_figs/sekil_6_4.png){width=11.71cm}


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

6.3.2.5

### Adım 6: Görünümleri Taslak Olarak Çizme ve Tasarım Kararlarını Kaydetme

Şekil 6.5’te gösterilen dağıtım diyagramı (deployment diagram), uygulamaya ev sahipliği yapacak yeni sunucuyu ve harici kullanıcı dizini sunucusunu, ayrıca bunların mevcut düğümlerle olan bağlantılarını göstermektedir.  

![Şekil 6.5](/home/runner/workspace/scripts/dsa_figs/sekil_6_5.png){width=10.23cm}

Yeni eklenen öğelerin sorumlulukları aşağıdaki tabloda açıklanmıştır.

**Öğe** | **Sorumluluk**
--- | ---
Web/App Sunucusu | Uygulamanın etkileşimli kısmına ev sahipliği yapar.
Kimlik Doğrulama Sunucusu (Auth Server) | Bankadaki birden fazla uygulama için kullanıcıları ve izinleri yöneten mevcut sunucu (CON-1).

Şekil 6.6’da gösterilen paket diyagramı (package diagram), başvuru mimarisinin (reference architecture) nasıl somutlaştırıldığını (instantiate edildiğini) ve birincil kullanım senaryosunu (UC-1) desteklemek için tanıtılan modülleri göstermektedir. Aynı zamanda, bu yeni eklenen öğelerin, önceki sistem sürümünden gelen mevcut katmanlar ve modüllerle nasıl bütünleştirildiğini de göstermektedir.

![Şekil 6.6](/home/runner/workspace/scripts/dsa_figs/sekil_6_6.png){width=10.69cm}


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

![Şekil 6.7](/home/runner/workspace/scripts/dsa_figs/sekil_6_7.png){width=15.0cm}


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

Son yirmi yılda, çok sayıda mimari tasarım yöntemi önerilmiş ve dokümante
edilmiştir. Bu bölümde, en iyi bilinen yöntemlerden bazılarını kısaca sunuyor ve
bunları nitelik temelli tasarım (Attribute-Driven Design, ADD) ile ilişkilendirip
karşılaştırıyoruz. Bir “genel mimari tasarım modeli” ile başlıyor, ardından beş
tasarım yöntemini kısaca tanıtıyoruz. Bölümü, ADD’in bu diğer yöntemlerden
nasıl ayrıştığını tartışarak bitiriyoruz.

## 7.1 Yazılım Mimarisi Tasarımının Genel Bir Modeli

Hofmeister ve çalışma arkadaşları, “A General Model of Software Architecture
Design Derived from Five Industrial Approaches” başlıklı makalelerinde, beş
endüstriyel yazılım mimarisi tasarım yöntemini karşılaştırmış ve bunların ortak
özelliklerinden, genel bir yazılım mimarisi tasarım yaklaşımı türetmiştir. İnceledikleri beş model şunlardır: ADD 2.0, Siemens 4 views, RUP’un 4+1 Views’u,
Business Architecture Process and Organization (BAPO) ve Architecture Separation of Concerns (ASC).

Şekil 7.1’de gösterilen türetilmiş genel model, incelenen beş modelin

![Şekil 7.1](/home/runner/workspace/scripts/dsa_figs/sekil_7_1.png){width=10.55cm}

tamamında bulunan üç ana etkinlikten oluşur:

- **Mimari analiz (architectural analysis).** Bu etkinlikte, gereksinimler
(“kaygılar (concerns)” olarak adlandırılır) ve sistem bağlamı, mimari açıdan
önemli gereksinimlerin (architecturally significant requirements, ASR)
belirlenmesi için girdi olarak kullanılır.
- **Mimari sentez (architectural synthesis).** Bu etkinlik, mimari tasarımın
çekirdeği olarak tanımlanır. Bir dizi ASR için mimari çözümler önerir; böylece problem uzayından çözüm uzayına geçilir. Bu etkinliğin çıktıları, gerekçe
(rationale) bilgilerini de içeren, kısmi veya tam mimari tasarımlar hâlindeki
aday mimari çözümlerdir.
- **Mimari değerlendirme (architectural evaluation).** Bu etkinlik, mimari
kararların doğru olup olmadığını güvence altına alır. Aday mimari çözümler,
ASR’lara göre ölçülür. Farklı mimari çözümlere yönelik birkaç değerlendirme
beklenir, fakat nihai sonuç, doğrulanmış (validated) mimaridir.

Hofmeister ve çalışma arkadaşları, bu etkinliklerin sıralı biçimde işlemediğini,
tersine, mimarların bir etkinlikten diğerine küçük “sıçramalarla” ilerlediğini açıklar. İlerleme, mimarların ele alması gereken daha küçük ihtiyaçlar, konular,
sorunlar ve fikirlerden oluşan örtük ya da açık bir birikim (backlog) tarafından
yönlendirilir (Şekil 7.2).

![Şekil 7.2](/home/runner/workspace/scripts/dsa_figs/sekil_7_2.png){width=11.78cm}


Hofmeister vd. tarafından sunulan bu genel model, kasıtlı olarak ayrıntılı
değildir; çünkü ADD dâhil, diğer tasarım süreçlerinde bulunan özgül teknikleri
soyutlar. Bu nedenle model, ADD’i temsil edebildiği gibi, daha geniş bir mimari
geliştirme kapsamını da kapsar: Mimari gereksinimlerin toplanması ve analizinin
QAW (Quality Attribute Workshop) gibi yöntemlerle yapılması, mimari sentezin
makalede sunulan yöntemler gibi yöntemlerle gerçekleştirilmesi ve mimari değerlendirmenin ATAM (Architecture Tradeoff Analysis Method) gibi yöntemlerle
yürütülmesi bu kapsamın içindedir.

> **💬 Çevirmen notu:** Buradaki model, “süreç”ten çok, farklı mimari
> yöntemlerin ortak çekirdeğini gösteren soyut bir “etkinlik çerçevesi”
> olarak okunmalıdır.

## 7.2 Mimari Merkezli Tasarım Yöntemi

Mimari Merkezli Tasarım Yöntemi (Architecture-Centric Design Method,
ACDM), mimarinin tüm yaşam döngüsünü kapsayan bir yazılım mimarisi
geliştirme yöntemidir. Bu yinelemeli (iterative) yöntem, Şekil 7.3’te gösterildiği

![Şekil 7.3](/home/runner/workspace/scripts/dsa_figs/sekil_7_3.png){width=11.92cm}

gibi 8 aşamadan oluşur.

3. aşama, tasarıma odaklanır; ilk mimari tasarımın oluşturulduğu veya
iyileştirildiği yerdir. Yeni sistemler için bu sürecin ilk yinelemesi, “varsayımsal”
ya da başlangıç mimarisinin hızlı biçimde oluşturulmasını teşvik eder. Bu yineleme, önce sistem bağlamının kurulması ve ardından yinelemeli bir biçimde
ayrıştırma (decomposition) yapılarak yapılar (structures) üretilmesiyle ilerler.

ACDM’de ayrıştırma, kalite niteliği senaryoları (quality attribute scenarios) ve
kısıtlar tarafından yönlendirilir; ancak işlevsel gereksinimler de dikkate alınır.
Sonraki yinelemelerde, mimari gözden geçirmede (4. aşama) ortaya çıkarılan
sorunlar da girdi görevi görür. ACDM, ayrıştırmayı desteklemek için desenlerin
(patterns) kullanılmasını ve süreç boyunca birden fazla bakış açısının (statik,
dinamik) kullanılmasını önerir. Ayrıştırma gerçekleştiğinde, sorumluluklar
öğelerle ilişkilendirilir ve arayüzler tanımlanır.

ACDM, 8 aşaması içinde mimari geliştirme yaşam döngüsünün tamamını
(gereksinimler, tasarım, değerlendirme ve dokümantasyon) kapsadığı için,
ADD’den daha geniş bir kapsama sahiptir. ACDM’in 3. aşaması, ADD’in karşılığıdır. Bununla birlikte, ACDM bu kritik adımın nasıl yapılacağı konusunda,
ADD’e kıyasla daha az ayrıntılı rehberlik sunar. Ancak ADD ve ACDM birlikte
kullanılabilir. Bunu yapmak için, ACDM’in 3. aşamasında doğrudan ADD’i
kullanmanız yeterlidir.

## 7.3 Rational Unified Process’te Mimari Etkinlikler

Rational Unified Process (RUP), on yılı aşkın süredir yaygın olarak kullanılan bir
yazılım geliştirme süreç çerçevesidir. Çerçeve kapsamlıdır ve incelediğimiz sürüm
(7.0.1), biri büyük projeler (burada tartışma için kullanılan), diğeri küçük projeler
için olmak üzere iki “çeşit” sunar. RUP’ta her proje yinelemeli (iterative) olarak
geliştirilir ve yinelemeler dört ardışık faz boyunca yürütülür:

- **Başlatma (Inception).** Bu fazda proje tasarlanır ve fizibilitesi değerlendirilir.
- **Geliştirme (Elaboration).** Bu fazda, projenin başarılı biçimde yürütülmesi için gerekli birçok unsur ele alınır. Bu unsurlardan biri de mimarinin
tasarımıdır.
- **İnşa (Construction).** Bu fazda, sistem yinelemeli olarak inşa edilir.
- **Geçiş (Transition).** Bu fazda, tamamlanan sistem geliştirme ortamından
son kullanıcı ortamına aktarılır.

RUP için mimari, sistem oluşturmanın temel bir yönüdür ve özellikle başlatma
ve geliştirme fazlarında mimariyle ilişkili etkinlikler tanımlanmıştır. Başlatma
fazında RUP, amacı sistemin fizibilitesini göstermek için mimari bir kavram kanıtı
(architectural proof-of-concept) oluşturmak ve değerlendirmek olan “mimari
sentez gerçekleştirme (perform architectural synthesis)” adlı bir etkinlik tanımlar. Bu etkinlik; sistem bağlamını tanımlama, mimari analiz gerçekleştirme
(ki bu aslında aday bir mimarinin tanımlanmasına karşılık gelir), mimari bir
kavram kanıtı (bir prototip) oluşturma ve bu kavram kanıtının uygulanabilirliğini
değerlendirme gibi görevleri içerir.

Geliştirme (elaboration) fazı, yazılım mimarisiyle ilişkili iki etkinlik içerir:

§ Aday bir mimari tanımla. Bu etkinlikte, yazılım mimarisinin ilk taslağı oluşturulur. Buna, mimari açıdan anlamlı (architecturally significant) öğelerin tanımlanması, bir dizi analiz mekanizmasının belirlenmesi, sistemin başlangıç katmanlamasının ve örgütlenmesinin tanımlanması ve mevcut yineleme (iteration) için kullanım durumu (use case) gerçekleştirimlerinin (realization) tanımlanması dahildir. Temel görevler mimari analiz ve kullanım durumu analizi gerçekleştirmektir; diğer görevler arasında işlem analizi (operation analysis) yapmak ve güvenlik desenlerini (security pattern) belirlemek yer alır.

§ Mimarinin iyileştirilmesi (refine the architecture). Bu etkinlik, bir yineleme için mimarinin tamamlanmasına odaklanır. Analiz öğelerinden tasarım öğelerini ve analiz mekanizmalarından tasarım mekanizmalarını tanımlayarak analiz etkinliklerinden tasarım etkinliklerine geçişi içerir. Buna ek olarak, çalıştırma zamanı (runtime) ve dağıtım (deployment) mimarisi ile, tasarım ile uygulama (implementation) arasındaki geçişi kolaylaştıracak bir uygulama modeli tanımlanır. Bunu başarmak için RUP (Rational Unified Process), tasarım mekanizmalarını belirleme, tasarım öğelerini belirleme, işlem analizi gerçekleştirme, mevcut tasarım öğelerini içeriye alma, uygulama modelini yapılandırma ve çalıştırma zamanı mimarisini tanımlama, dağıtımı betimleme ve mimariyi gözden geçirme gibi görevlerin gerçekleştirilmesini önerir.

RUP, mimari geliştirme için kapsamlı ve ayrıntılı bir süreç sunar. Ayrıca analiz, tasarım ve uygulama yönleri arasında net ayrımlar yapar. Başlangıçta, mimari analiz görevlerinde kavramsal düzeyde tasarlanır, ardından tasarım ve uygulama görevlerinde somutlaştırılır. Örneğin, başlangıçta kalıcılık (persistence) gibi bir analiz mekanizması tanımlanabilir. Bu, bir VTYS (DBMS) gibi bir tasarım mekanizmasına dönüştürülür ve bu da daha sonra belirli bir Oracle veya MySQL veritabanı gibi bir uygulama mekanizmasına dönüştürülür.

RUP içindeki süreç doğası gereği yinelemelidir; başlangıç ve ayrıntılandırma (inception ve elaboration) safhalarında tanımlanan mimari etkinliklerin pek çok yinelemesi gerçekleştirilebilir. RUP tarafından tanımlanan sürecin güzel bir yönü, sistem bağlamını tanımlama ve sistem için hem mantıksal hem de fiziksel olarak başlangıç yapısını oluşturma gibi mimari kaygılar (architectural concern) konusunda ayrıntılı kılavuzluk sağlamasıdır. RUP içindeki mimari süreç, kullanım durumlarına güçlü bir şekilde odaklanır. Nitelikler (quality attributes) her ne kadar “tamamlayıcı gereksinimler (supplementary requirements)” olarak anılsa da, mimari tasarım sürecini kullanım durumları kadar yönlendirmez. Ayrıca, bu süreç açıkça çalıştırılabilir bir mimari prototipin oluşturulmasını da ele alır.

RUP içindeki mimari süreç kapsamlı olsa da, tasarımın gerçekleştirilmesi için somut adımlar bakımından ADD (Attribute-Driven Design, nitelik temelli tasarım) kadar ayrıntı vermez. Bu anlamda, ADD ve RUP birbirini tamamlayan yöntemler olarak görülebilir ve ADD, diğer daha ayrıntılı mimari odaklı yöntemler (QAW, ATAM ve CBAM gibi) gibi RUP içine entegre edilebilir.

## 7.4 Yazılım Mimarlığı Süreci

Peter Eeles ve Peter Cripps, IBM’de mimar olarak çalışan yazarlardır ve *The Process of Software Architecting* adlı kitapta mimariye nasıl yaklaştıklarını anlatırlar. Süreçleri, tüm mimari yaşam döngüsünü kapsar ve herhangi bir yazılım geliştirme yönteminden bağımsızdır; ancak kitapta RUP ile birlikte kullanımına dair çeşitli atıflar yapılır.

Eeles ve Cripps’in tanımladığı süreç üç temel etkinliği içerir: “gereksinimleri tanımla (define requirements)”, “mantıksal mimari oluştur (create logical architecture)” ve “fiziksel mimari oluştur (create physical architecture)”. Mimari tasarımın gerçekleştirildiği etkinlikler son iki etkinliktir. Yazarlara göre mantıksal mimari, “gereksinimlerden çözüme geçerken bir basamak taşıdır—mimariyi büyük ölçüde teknolojiden bağımsız şekilde ele alan ilk adımdır. Fiziksel mimari ise daha özeldir ve teknolojiyi hesaba katar.” Mantıksal mimarinin ve fiziksel mimarinin oluşturulması aynı görevleri içerir (bkz. Şekil 7.4); ancak fiziksel mimarinin oluşturulmasında odak, şaşırtıcı olmayacak biçimde, mimarinin fiziksel yönleri üzerindedir.

![Şekil 7.4](/home/runner/workspace/scripts/dsa_figs/sekil_7_4.png){width=10.34cm}


**ŞEKİL 7.4** “mantıksal mimari oluştur” ve “fiziksel mimari oluştur” etkinliklerindeki görevler

## 168

# 7. Bölüm—Diğer Tasarım Yöntemleri

Bu süreç, farklı türde mimarların varlığını kabul eder: baş mimar (lead architect), uygulama mimarı (application architect), altyapı mimarı (infrastructure architect) ve veri mimarı (data architect). Ayrıca, en önemli mimari öğelerle ilişkili ve baş mimarın sorumluluğunda olan “taslak çıkarma (outlining)” görevleri ile, göreve bağlı olarak diğer mimarların sorumluluğunda olan, daha az önemli öğelere odaklanan “ayrıntılandırma (detailing)” görevleri arasında bir ayrım yapar. Örneğin, taslak çıkarma görevleri alt sistemler ve bileşenlerle uğraşırken, ayrıntılandırma görevleri arayüzler ve işlem imzaları (operation signatures) ile uğraşır.

Eeles ve Cripps tarafından tanımlanan yöntem, iki farklı modele de vurgu yapar: (1) sorumlulukları ve ilişkileri olan bileşenlerden ve istenen işlevselliği sunmak için bu bileşenlerin işbirliklerinden oluşan işlevsel model (functional model) ve (2) düğümlerin (node) konfigürasyonunu, bunlar arasındaki iletişim bağlantılarını ve düğümlerde dağıtılan bileşenleri gösteren dağıtım modeli (deployment model). Hem işlevsel gereksinimler hem de kalite niteliği (quality attribute) gereksinimleri, hem işlevsel hem de dağıtım modellerini etkiler. Yazarlar, sistem niteliklerine ulaşmak için yazılım ve donanımı eşit ortaklar (peer) olarak ele alan “sistem mühendisliği felsefesini (systems engineering philosophy)” benimsediklerini belirtir.

Aşağıdaki liste, tasarımla ilişkili olan mantıksal (logical) ve fiziksel (physical) mimariyi oluşturma etkinliklerindeki görevlerin amaçlarını özetler. Görevden birincil derecede sorumlu rol parantez içinde, diğer mimar türleri ise ikincil rolde yer alabilir:

- Mimari varlıkları gözden geçir (baş mimar). Geliştirilmekte olan sisteme uygulanabilecek, yeniden kullanılabilir mimari varlıkları belirle.
- Mimari genel görünümü tanımla (baş mimar). Geliştirilmekte olan sistemin başlıca öğelerini, işlevsel ve dağıtım bakış açısından tanımla ve açıkla.
- Mimari kararları belgele (baş mimar). Mimarinin biçimlendirilmesinde alınan kilit kararları ve bunların arkasındaki gerekçeleri yakala. Bu adım, seçeneklerin değerlendirilmesini ve tercih edilen bir seçeneğin seçilmesini içerir.
- İşlevsel öğelerin taslağını çıkar (uygulama mimarı). Geliştirilmekte olan sistemin başlıca işlevsel öğelerini (alt sistemler ve bileşenler) belirle.
- Dağıtım öğelerinin taslağını çıkar (altyapı mimarı). Geliştirilmekte olan sistemin dağıtılacağı konumları ve her konumdaki düğümleri belirle.
- Mimarinin doğrulanması (baş mimar). Mimari iş ürünlerinin tutarlı olduğunu doğrula ve mimari iş ürünleri boyunca yatay kesen (cross-cutting) kaygıların tutarlı biçimde ele alındığından emin ol.
- Mimari kavram kanıtı (proof-of-concept) inşa et (baş mimar). Mimarlar tarafından tasavvur edildiği şekliyle, böyle bir çözümün var olup olmadığını belirlemek amacıyla, mimari açıdan önemli gereksinimleri (architecturally significant requirements) karşılayan (kavramsal da olabilir) en az bir çözüm sentezle.
- İşlevsel öğeleri ayrıntılandır (uygulama mimarı). İşlevsel öğeleri, ayrıntılı tasarıma devredilebilecek noktaya kadar rafine et. Bu, bileşen arayüzlerinin ayrıntılı bir biçimde tanımlanmasını (örneğin, işlem imzaları, ön ve son koşullar) ve bunun için sıralama diyagramlarının (sequence diagram) kullanılmasını içerir.
- Dağıtım öğelerini ayrıntılandır (altyapı mimarı). Dağıtım öğelerini, ayrıntılı tasarıma devredilebilecek noktaya kadar rafine et. Bu, bileşenlerin düğümlere atanmasını ve düğümler ile konumlar arasındaki bağlantıların tanımlanmasını içerir.

RUP’a (Rational Unified Process) benzer bir ruhla, Process of Software Architecting (Yazılım Mimarisi Süreci) bir çerçevedir ve üzerinde çalışılan projenin türüne göre uyarlanması gerekir. Örneğin, kurulması gereken mantıksal mimarinin miktarı değişebilir; öyle ki, bazı durumlarda, tasarlanan sistem mevcut olanlara çok benziyorsa hiçbir mantıksal mimari oluşturulmayabilir. Ayrıca, geliştirim (elaboration) aşaması mantıksal mimariyi, inşa (construction) aşaması ise fiziksel mimariyi vurgular. Son olarak, mantıksal ve fiziksel mimariler art arda (sekansiyel) olarak oluşturulmak zorunda değildir ve süreç, bazı teknoloji seçimlerinin erken aşamada yapılabileceğini kabul eder.

Process of Software Architecting kapsamlı bir çerçevedir ve bu kitap, farklı görevlerin nasıl icra edileceğine dair ayrıntılı bir örnek sunar. Mantıksal/fiziksel mimariyi oluşturmayla ilgili görevler, 3.3. Bölüm’de tartışılan yol haritası ile birleştirilmiş ADD (Attribute-Driven Design, nitelik temelli tasarım) adımlarına benzer. Ancak Process of Software Architecting, yinelemeleri (iteration) belirli senaryolarla yönlendirmeye daha az vurgu yapar ve tasarım kararlarının fiilen nasıl verileceğine dair daha az rehberlik sağlar.

## 7.5 Mimari ve Tasarım için Bir Teknik

Application Architecture Guide, ikinci baskı (Microsoft) kitabında, Microsoft bir mimari eskizleme tekniği önerir. Bu teknik, yinelemeli (iterative) olarak gerçekleştirilen beş adımdan oluşur (Şekil 7.5):

![Şekil 7.5](/home/runner/workspace/scripts/dsa_figs/sekil_7_5.png){width=11.01cm}


1. Mimari hedefleri belirle. Bu hedefler ve kısıtlar tasarım sürecini şekillendirir, kapsam sağlar ve ne zaman “işinin bittiğini” belirlemeye yardımcı olur. Örneklere; bir prototip inşa etmek, teknolojileri keşfetmek ve bir mimari geliştirmek dahildir. Ayrıca, bu noktada mimarinin tüketicileri (paydaşlar, kullanıcılar, geliştiriciler vb.) belirlenir ve tasarım etkinliklerine ayrılacak kapsam, süre ve kaynaklar belirlenir.
2. Anahtar senaryoları belirle. Anahtar senaryolar; sorunları, mimari açıdan önemli kullanım durumlarını (architecturally significant use case), kalite nitelikleri ile işlevselliğin kesişim noktalarını veya kalite nitelikleri arasındaki ödünleşimleri (tradeoff) temsil eder.
3. Uygulama genel görünümünü oluştur. Bu adım, uygulamanın tamamlandığında nasıl görüneceğine dair bir genel görünüm yaratmaya karşılık gelir. Bu adımın sonunda süreç, mimarinin “tahtaya çizilmesini (whiteboarding)” önerir; yani mimarinin gayriresmî bir temsilinin oluşturulmasını. Bu adım aşağıdaki etkinlikler kümesine ayrılır:
   a. Uygulama tipini belirleme: bir referans mimarinin seçilmesini içerir.  
   b. Dağıtım kısıtlarını belirleme: bir dağıtım topolojisinin (deployment topology) seçilmesini içerir.  
   c. Önemli mimari tasarım stillerini belirleme.  
   d. İlgili teknolojileri belirleme: uygulama tipi ve kısıtlara dayanarak.
4. Anahtar konuları belirle. Anahtar konular, kalite nitelikleri ve yatay kesen kaygılar (crosscutting concern) olarak gruplanır. Yatay kesen kaygılar; tüm katmanlara, bileşenlere ve katmanlar-arası dilimlere (tiers) uygulanabilen tasarım özellikleridir. Örnekler şunlardır:
   a. Kimlik doğrulama ve yetkilendirme (authentication and authorization)  
   b. Önbellekleme (caching)  
   c. İletişim (communication)  
   d. Yapılandırma yönetimi (configuration management) (yapılandırılabilir olması gereken bilgiler)  
   e. Hata yönetimi (exception management)  
   f. Günlükleme ve ölçümleme (logging and instrumentation)  
   g. Doğrulama (validation) (girdi verisinin doğrulanması)
5. Aday çözümleri tanımla. Aday mimariler; bir uygulama tipi, dağıtım mimarisi (deployment architecture), mimari stil, teknoloji seçimleri, kalite nitelikleri ve yatay kesen kaygıları içerir. Bir aday mimari, gereksinimleri ve konuları (issues) karşılarsa bir temel mimari (baseline architecture) hâline gelir ve sonraki yinelemelerde rafine edilir.

**ŞEKİL 7.5** Mimari ve tasarım tekniğinin yinelemeli adımları

## 7.6 Görünüm Noktaları (Viewpoint) ve Perspektifler Yöntemi (Viewpoints and Perspectives Method)

171

Bu beş ana adıma ek olarak, Microsoft ekibinin ele aldığı teknik, mimarinin gözden geçirilmesini ve tasarımın temsil edilmesi ile iletişimini önermektedir. Bu teknik belirli bir geliştirme sürecinden bağımsızdır ve yalnızca, Çevik (Agile) bir süreç kullanıldığında yinelemelerin mimari ve geliştirme faaliyetlerini birleştirmesi gerektiğine dair bir öneri sunar.

Microsoft ekibinin sunduğu teknik çok ayrıntılı değildir; ancak bu tekniğin tartışılması Microsoft’un kitabının yalnızca küçük bir bölümünü oluşturur. Kitabın geri kalanı, web, zengin istemci (rich client), zengin internet (rich internet) ve mobil uygulamalar gibi farklı türdeki uygulamalar için dikkate alınması gereken hususlar hakkında pragmatik ve ayrıntılı bilgiler sağlar. Örneğin, kitap iş katmanının (business layer) tasarımına özgü yönlere ayrılmış bir bölüme sahiptir. Bilgilerin önemli bir kısmı teknoloji bağımsız olsa da, Microsoft kendi teknolojilerinin bu süreçte nasıl kullanılabileceğini göstermek konusunda da son derece iyi bir iş çıkarmıştır. Ayrıca, kitap bir dizi referans mimari (reference architecture) için ele alınması gereken kaygılar hakkında kapsamlı bir tartışma sunar.

Bu teknik amaç bakımından ADD’ye (Attribute-Driven Design, nitelik temelli tasarım) benzer, ancak gerçek tasarım adımlarının nasıl uygulanacağı açısından daha az ayrıntılıdır. ADD bir alternatif olarak kullanılabilir, ancak Microsoft’un kitabını, tasarım sırasında ele almanız gereken pek çok somut mimari kaygıyı saptamak ve özellikle kitapta ele alınan uygulama türlerinden birini tasarlıyorsanız sunulan tüm pratik tavsiyelerden yararlanmak için elinizin altında bulundurmak iyi bir fikirdir. Microsoft’un kitabında sunulan fikirler, bu kitabın çeşitli yönlerini oluştururken bize ilham vermiştir.

## 7.6 Bakış Açısı ve Perspektif Yöntemi (Viewpoints and Perspectives Method)

Bakış açısı ve perspektif yöntemi, Nick Rozanski ve Eoin Woods tarafından yazılan *Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives* adlı kitapta açıklanmaktadır. Kitabın başlığında vurgulanan iki kritik kavram, bakış açıları (viewpoints) ve perspektiflerdir (perspectives); yazarlar bunları şu şekilde tanımlar:

- **Bakış açısı (viewpoint)**, bir tür görünüm (view) oluşturmaya yönelik desenler (patterns), şablonlar (templates) ve kurallar (conventions) koleksiyonudur. Bakış açısı, kaygıları bu bakış açısından yansıtılan paydaşları (stakeholders) ve bu bakış açısına ait görünümleri oluşturmak için kullanılacak yönergeleri, ilkeleri ve şablon modelleri tanımlar. Tanımlanan bakış açıları arasında işlevsel (functional), bilgi (information), eşzamanlılık (concurrency), geliştirme (development), dağıtım (deployment) ve işletimsel (operational) bakış açıları yer alır.
- **Mimari perspektif (architectural perspective)**, bir sistemin mimari görünümlerinin tamamı boyunca dikkate alınması gereken bir dizi kalite özelliğini (quality properties) sergilemesini sağlamak için kullanılan etkinlikler, taktikler (tactics) ve yönergeler koleksiyonudur. Rozanski ve Woods’un kitabında ele alınan başlıca perspektifler güvenlik (security), performans ve ölçeklenebilirlik (performance and scalability), kullanılabilirlik ve dayanıklılık (availability and resilience) ile evrim (evolution) perspektifleridir.

> **💬 Çevirmen notu:** Rozanski & Woods yaklaşımında “viewpoint” bir çeşit “görünüm türü” için tarif seti, “perspective” ise kalite niteliklerini o türlerin tümü boyunca ele alan enine bir kaygı kümesi olarak düşünülebilir. Bu, kitapta ADD’deki senaryo ve taktik kavramlarıyla ilişkilendiriliyor.

Perspektifler, belirli bir perspektifin farklı bakış açılarında uygulanabilmesi nedeniyle bakış açılarına ortogonaldir (orthogonal). Örneğin, güvenlik perspektifi; işlevsel, bilgi ve işletimsel bakış açılarındaki unsurları içerir.

Mimari, Şekil 7.6’da gösterilen mimari tanımlama sürecinde oluşturulur. Bu süreçteki adımlar aşağıda özetlenmiştir:

![Şekil 7.6](/home/runner/workspace/scripts/dsa_figs/sekil_7_6.png){width=11.75cm}


1. **Girdileri birleştirin.** İlk girdileri anlayın, doğrulayın ve iyileştirin.
2. **Senaryoları belirleyin.** Sistemin en önemli gereksinimlerini örnekleyen bir dizi senaryo belirleyin.
3. **İlgili mimari stilleri belirleyin.** Sistemin genel organizasyonu için temel olarak kullanılabilecek bir ya da daha fazla kanıtlanmış mimari stili belirleyin.
4. **Aday bir mimari üretin.** Sistemin başlıca kaygılarını (gereksinimler ve hedefler) yansıtan ve daha ileri mimari değerlendirme ve iyileştirmeye temel oluşturabilecek ilk taslak mimariyi oluşturun.
5. **Mimari seçenekleri keşfedin.** Sistem için çeşitli mimari olasılıkları inceleyin ve bunlar arasından seçim yapmak için temel kararları alın.
6. **Mimariyi paydaşlarla değerlendirin.** Mimariyi kilit paydaşlarınızla birlikte bir değerlendirmeden geçirin, sorunları veya eksiklikleri yakalayın ve mimari için paydaşların onayını alın.
7. Bu noktada iki adım paralel olarak yürütülür:  
   A. **Mimariyi yeniden çalışın.** Değerlendirme sırasında ortaya çıkan tüm kaygıları ele alın.  
   B. **Gereksinimleri yeniden gözden geçirin.** Mimari değerlendirmeler ışığında, sistemin özgün gereksinimlerinde yapılması gerekebilecek değişiklikleri değerlendirin.

Bu yöntem, mimari stillerden elde edilen ya da en azından onlara dayanan bir aday mimari oluşturulmasını önermektedir. Bu aday mimari, bir değerlendirme yapıldıktan sonra kabul edilebilir görülene dek bir dizi yineleme yoluyla daha da iyileştirilir.

ADD ile karşılaştırıldığında, bu yöntem 4. ve 5. adımların nasıl yürütüleceğine dair adım adım bir rehber sunmaz. Bununla birlikte, bu yaklaşımın bir faydası, tanımladığı altı bakış açısının bizim yaklaşımımızdaki genel mimari kaygılarla ilişkilendirilebilmesidir. Ayrıca, taktikler ile perspektifler ilişkilidir ve perspektiflerin farklı bakış açıları boyunca uygulanması fikri değerlidir; senaryo temelli bir yaklaşıma da tamamlayıcı olabilir. Örneğin, sürücüler (drivers) listenizde yalnızca bir güvenlik senaryosu varsa, yalnızca bu belirli senaryoyu destekleyen öğeleri dikkate alabilirsiniz. Oysa bir güvenlik perspektifini düşünmek, doğrudan bu belirli senaryoyla ilişkili olmayıp dağıtım (deployment) veya işletim (operation) gibi farklı kaygı alanlarına yayılan güvenlikle ilgili tasarım kararları alırken yararlı olabilir.

## 7.7 Özet

Bu bölümde çeşitli tasarım yöntemlerini inceledik ve bunları ADD ile karşılaştırdık. Görüldüğü gibi, seçebileceğiniz bir dizi yöntem mevcut. Peki neden bu alternatifler yerine, ya da onlara ek olarak, ADD’yi kullanmalısınız? Temel olarak, ADD mimari tasarım etkinliğini gerçekleştirmek için gerekli adımlar ve yönlendirmeler bakımından daha somut ve özeldir. Buraya kadar okuduğunuza göre, muhtemelen buna ikna olmuş olmalısınız.

ADD özellikle tasarıma odaklanır ve bu nedenle (geleceğin) mimarına daha ayrıntılı bir rehberlik sunar. Bu, ADD’nin bir zayıflığı değildir. Diğer birçok yöntem mimari yaşam döngüsünün diğer evrelerinde size rehberlik edebilir; örneğin, mimari gereksinimlerin ortaya çıkarılması ve önceliklendirilmesi için QAW (Quality Attribute Workshop), bir mimarinin analiz edilmesi için ATAM (Architecture Tradeoff Analysis Method), bir mimarinin dokümantasyonu için Views and Beyond tekniği. Bu kitapta, bu tür yöntemlerin ADD ile nasıl sorunsuz şekilde bütünleştirilebileceğini çeşitli bölümlerde tartıştık.

Tüm açıklığıyla belirtmek gerekirse, ADD 3.0 bu bölümde anlatılan tüm yaklaşımlardan esinlenmiş, onlardan yararlanmış ve onlara bir teşekkür borçludur.

## 7.8 Ek Okuma (Further Reading)

Bu bölümde tartışılan mimari tasarım yöntemleri aşağıdaki kaynaklarda bulunabilir:
- P. Eeles, P. Cripps. *The Process of Software Architecting*. Addison-Wesley Professional, 2009.
- C. Hofmeister, P. Kruchten, R. Nord, H. Obbink, A. Ran, P. America. “A General Model of Software Architecture Design Derived from Five Industrial Approaches”, *Journal of Systems and Software*, 80:106–126, 2007.
- A. Lattanze. *Architecting Software Intensive Systems: A Practitioner’s Guide*. CRC Press, 2009.
- P. Kruchten. *The Rational Unified Process: An Introduction*, 3. baskı, Addison-Wesley, 2003.
- Microsoft, *Application Architecture Guide*, 2. baskı. Microsoft Press, 2009.
- N. Rozanski, E. Woods. *Software Systems Architecture*. Addison Wesley, 2005.

# 8  
Tasarım Sürecinde Analiz

Her ne kadar bu kitap mimari tasarıma odaklanmış olsa da, tasarım ve analizin aynı madalyonun iki yüzü olduğuna her zaman inandık. Tasarım, karar verme sürecidir; analiz ise bu kararları anlamaya yönelik süreçtir ki böylece tasarım değerlendirilebilsin. Bu yakın ilişkiyi yansıtmak için, şimdi tasarım sürecinde mimari kararları neden, ne zaman ve nasıl analiz etmemiz gerektiğine odaklanıyoruz. Çeşitli analiz tekniklerine bakacağız, ne zaman uygulanabileceklerini tartışacağız ve maliyetlerini ve faydalarını inceleyeceğiz.

## 8.1  
Analiz ve Tasarım

Analiz, karmaşık bir varlığı anlamak amacıyla onu bileşen parçalarına ayırma sürecidir. Analizin karşıtı sentezdir. Dolayısıyla analiz ve tasarım iç içe geçmiş etkinliklerdir. Tasarım süreci boyunca, analiz etkinliği çeşitli yönlere gönderme yapabilir:

- Tasarlamak üzere olduğunuz çözümün hedeflediği problemi anlamak için tasarım sürecine giren girdileri incelemek. Bu, Bölüm 3.2.2’de tartışıldığı gibi sürücülere (drivers) öncelik verilmesini de içerir. Bu tür analiz, ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) 1. ve 2. adımlarında gerçekleştirilir.
- Bir tasarım problemini çözmek için belirlediğiniz alternatif tasarım kavramlarını inceleyerek en uygun olanı seçmek. Bu durumda analiz, seçimleriniz için somut kanıtlar sunmanızı zorlar. Bu etkinlik, ADD’nin 4. adımında gerçekleştirilir ve Bölüm 3.2.4’te tartışılmıştır.
- Tasarım süreci (veya bir yineleme) sırasında alınan kararların uygunluğunu güvence altına almak. Bu, ADD’nin 7. adımında gerçekleştirdiğiniz analiz türüdür.

Mimariyi tasarlarken aldığınız kararlar, yalnızca kalite niteliği (quality attribute) tepkilerini elde etmek açısından kritik değildir; çoğu zaman, bu kararları daha sonraki bir zamanda düzeltmenin maliyeti önemli derecede yüksek olabilir, çünkü bu kararlar sistemin birçok bölümünü etkileyebilir. Bu nedenlerle, sorunların tanımlanabilmesi, mümkünse nicelleştirilebilmesi ve hızlıca düzeltilebilmesi için tasarım sürecinde analiz yapılması gereklidir. Unutmayın, fazla özgüvenli olmak ve içgüdülerinizi takip etmek en iyi fikir olmayabilir (bkz. kenar yazı “‘İnanıyorum’ Yeterince İyi Değil”). Neyse ki, bu noktaya kadar verdiğimiz önerileri takip ettiyseniz, tasarım sürecini yürütürken ürettiğiniz taslaklar ve görünümlerden (views) yararlanarak, analizi ya kendi başınıza ya da akranlarınızın yardımıyla yürütebiliyor olmalısınız.

### “‘İnanıyorum’ Yeterince İyi Değil”

Mimarinizi tasarlarken sistematik bir yaklaşım izliyor, yerleşik kaynaklardaki tasarım kavramlarını kullanıyor ve yapılarınızı temsil eden güzel görünümlü diyagramlara sahip olsanız bile, aldığınız kararların gerçekten belirli bir kalite niteliği senaryosunu (quality attribute scenario) tatmin edeceğini garanti eden hiçbir şey yoktur. Bazı kalite nitelikleri sisteminizin başarısı için kritiktir; özellikle bu tür kararlar söz konusu olduğunda “İnanıyorum” gerekçesi yeterince iyi değildir. Uygulamada çalışan yazılım mimarları üzerine yapılan çalışmalar, çoğunun tasarım kararlarını verirken “yeterlilik” yaklaşımını benimsediğini göstermiştir — yani ihtiyaçlarını karşıladığı ilk bakışta görünen kararı benimserler. Çoğu kez, bu kararları destekleyecek içgüdüleri, inançları ve (kaçınılmaz olarak sınırlı olan) deneyimleri dışında hiçbir gerekçeleri yoktur. Böylece, önemli kararlar çoğu kez yetersiz akıl yürütme sonrasında alınır; bu da bir sisteme risk katabilir.

Sisteminize kritik olan sürücüler (drivers) için, yalnızca içgüdünüze güvenmek, benzetmelere ve geçmişe dayanmak ya da sürücülerin karşılandığından emin olmak için birkaç yüzeysel test yapmak yerine, hem kendinize hem de kuruluşunuza daha ayrıntılı bir analiz yapma borcunuz vardır. Aşağıdaki seçenekler, analizinizin derinliğini artıracak ve böylece alınan kararlar için gerekçenizi güçlendirecektir:

- Analitik modeller (analytic models). Bu yerleşik matematiksel modeller, performans veya erişilebilirlik (availability) gibi kalite niteliklerini incelemenizi sağlar. Erişilebilirlik için Markov ve istatistiksel modelleri; performans için ise kuyruk (queuing) kuramı ve gerçek zamanlı çizelgeleme kuramını (real-time scheduling theory) içerirler. Analitik modeller — özellikle performansı ele alanlar — oldukça olgundur (mature), ancak yeterince kullanılabilmeleri için kayda değer eğitim ve öğrenim gerektirebilir.

> **💬 Çevirmen notu:** Buradaki “analitik modeller” ifadesiyle kastedilen, genellikle kapalı formüllere veya iyi tanımlanmış algoritmalara dayalı, önceden kanıtlanmış matematiksel model aileleridir; bunlar, kod yazmadan önce sistem davranışını yaklaşık olarak hesaplamaya yarar.

§ Kontrol listeleri (checklist). Kontrol listeleri, ele alınması gereken belirli kararların sistematik bir biçimde unutulmadığından emin olmanızı sağlayan yararlı araçlardır. Belirli kalite nitelikleri (quality attribute) için kamuya açık alanda mevcut kontrol listeleri vardır — örneğin OWASP kontrol listesi, web uygulamalarının kara kutu güvenlik (black box security) testlerini gerçekleştirmenize rehberlik eder. Ayrıca, kuruluşunuz, geliştirdiğiniz uygulama alanlarına özgü tescilli (proprietary) kontrol listeleri geliştirebilir. Kısa süre sonra ele alacağımız taktik temelli anketler (tactics-based questionnaire), taktiklerin (tactic) kullanımına dayalı olarak en önemli kalite nitelikleri için bir tür kontrol listesidir.

§ Düşünce deneyleri (thought experiment), yansıtıcı sorular (reflective question) ve kaba taslak (back-of-the-envelope) analizler. Düşünce deneyleri, küçük bir tasarımcı grubunun önemli senaryoları çalışarak potansiyel sorunları belirlediği, biçimsel olmayan analizlerdir. Örneğin, ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) 5. adımı içinde üretilmiş bir sıra diyagramını (sequence diagram) kullanabilir ve diyagramda modellenen senaryoyu destekleyen nesnelerin etkileşiminin bir meslektaşınızla birlikte üzerinden geçmesini (walk-through) yapabilirsiniz. Yansıtıcı sorular (ayrıntılı olarak Bölüm 8.5’te tartışılmaktadır), karar verme sürecine dahil edilen varsayımları sorgulayan sorulardır. Kaba taslak analizler (back-of-the-envelope analysis), analitik modellere göre daha az hassas, ancak hızlıca gerçekleştirilebilen yaklaşık hesaplamalardır. Genellikle diğer benzer sistemlere yönelik analogilere veya önceki deneyime dayanan bu hesaplamalar, arzu edilen kalite niteliği tepkileri (quality attribute response) için kabaca bir tahmin elde etmekte kullanışlıdır. Örneğin, bir boru hattındaki (pipeline) çok sayıda işlemin gecikmelerini (latency) toplayarak uçtan uca gecikmeye dair kabaca bir tahmin türetebilirsiniz.

§ Prototipler, benzetimler (simulation) ve deneyler. Bir tasarımı analiz etmek için kullanılan salt kavramsal teknikler, bazen belirli tasarım kararlarının uygun olup olmadığını veya belirli bir teknolojiyi diğerine tercih etmeniz gerekip gerekmediğini doğru biçimde anlamak için yetersiz kalır. Bu tür durumlarda, prototipler, benzetimler veya deneyler oluşturmak, daha iyi bir anlayış elde etmek için son derece değerli bir seçenek olabilir. Örneğin, daha önce anlatılan gecikmeye dair kaba taslak tahminde, birçok işlemin aynı kaynakları paylaştığını (dolayısıyla bu kaynaklar için rekabet ettiğini) hesaba katmamış olabilirsiniz; bu nedenle, bu işlemlerin bireysel gecikmelerini basitçe toplayıp doğru sonuçlar elde etmeyi bekleyemeyiz. Prototipler ve benzetimler sistem dinamiklerine ilişkin daha derin bir anlayış sağlar, ancak proje planında dikkate alınması gereken önemli bir çaba gerektirebilir.

Her zamanki gibi, bu tekniklerin hiçbirinin diğerlerinden doğası gereği daha iyi olduğunu söyleyemeyiz. Düşünce deneyleri ve kaba taslak hesaplamalar ucuzdur ve tasarım sürecinin erken safhalarında yapılabilir; ancak geçerlilikleri sorgulanabilir olabilir. Prototipler, benzetimler ve deneyler genellikle çok daha yüksek sadakatli (high-fidelity) sonuçlar üretir, ancak çok daha yüksek maliyetle. Hangi tekniğin kullanılacağına ilişkin seçim bağlama, söz konusu riske ve kalite niteliklerinizin önceliklerine bağlıdır.

Yine de, bu tekniklerden herhangi birini uygulamak, “Ben inanıyorum” (tasarımımın uygun olduğuna) noktasından, belgelenmiş kanıt ve gerekçelendirmeyle desteklenen bir yaklaşıma geçmekte yardımcı olacaktır.

---

# 8.2 Neden Analiz Ederiz?

Analiz ve tasarım aynı madalyonun iki yüzüdür. Tasarım, karar verme (süreci)dir. Analiz ise, bu kararların maliyet, takvim ve kalite açısından sonuçlarını anlama (süreci)dir. Mantıklı hiçbir mimar, özellikle de önemsiz olmayan herhangi bir kararı, o kararın etkilerini — kısa vadeli etkilerini ve mümkünse uzun vadeli sonuçlarını — anlamaya çalışmadan vermez. Elbette mimarlar, büyük bir projenin tasarımı süresince binlerce karar verir ve açıkça bunların hepsi önemli değildir. Ayrıca, önemli olan kararların tümü kalite niteliklerinin taşıyıcısı (carrier of quality attribute) değildir. Bazıları hangi tedarikçinin seçileceğiyle, hangi kodlama kuralının (coding convention) izleneceğiyle, hangi programcının işe alınacağı veya işten çıkarılacağıyla, hangi IDE’nin kullanılacağıyla ilgili olabilir — kuşkusuz önemli kararlardır, ancak doğrudan bir kalite niteliği sonucuna bağlanmış kararlar değillerdir.

Elbette bu kararlardan bazılarının, kalite niteliklerinin başarılması üzerinde etkisi olacaktır. Mimar geliştirmeyi katmanlar veya modüller ya da her ikisinden oluşan bir sistem hâline ayırdığında, bu karar, bir değişikliğin kod tabanında nasıl dalgalanacağına, yeni bir özellik eklerken veya bir hatayı düzeltirken kimin kiminle konuşması gerektiğine, geliştirme işinin bir kısmını dağıtmanın veya dış kaynağa (outsourcing) vermenin ne kadar kolay veya zor olduğuna, yazılımı farklı bir platforma taşımayı ne kadar kolaylaştırdığına ve benzeri hususlara etki edecektir. Mimar dağıtık bir kaynak yönetim sistemi seçtiğinde, bu sistemin hangi servislerin “master”, hangilerinin “slave” olduğunu nasıl belirlediği, hataları nasıl tespit ettiği ve kaynak yetersizliğini (resource starvation) nasıl belirlediği, sistemin erişilebilirliğini (availability) etkileyecektir.

Peki tasarım sürecinde ne zaman ve neden analiz yaparız? Öncelikle, analiz yaparız çünkü yapabiliriz. Bir mimari belirtim (architecture specification) — ister sadece bir beyaz tahta çizimi olsun, ister daha biçimsel olarak belgelenmiş ve dolaşıma sokulmuş bir şey — kalite niteliklerine ilişkin içgörü sağlayan bir analizi destekleyen ilk eserdir. Evet, gereksinimleri de analiz edebiliriz, ancak onları çoğunlukla tutarlılık ve tamlık açısından analiz ederiz. Bu gereksinimleri, tasarım kararlarından kaynaklanan yapılara dönüştürünceye kadar, bu kararların gerçek sonuçları, maliyet ve faydaları ve aralarındaki ödünleşimler (trade-off) hakkında söyleyebileceğimiz pek bir şey yoktur.

İkinci olarak — ve daha da önemlisi — analiz yaparız çünkü bu, kararları bilgilendirmenin ve riski yönetmenin ihtiyatlı bir yoludur. Hiçbir tasarım tamamen risksiz değildir, ancak üstlendiğimiz risklerin paydaşlarımızın (stakeholder) beklentileri ve toleranslarıyla orantılı olmasını sağlamak isteriz. Bir bankacılık uygulaması veya askerî bir uygulama için paydaşlarımız düşük risk seviyeleri talep edecek ve daha yüksek güven düzeyleri için buna göre ödeme yapmaya istekli olmalıdırlar. Zamanlama baskısının yüksek, bütçelerin kısıtlı olduğu bir girişim (startup) şirketinde ise çok daha yüksek risk seviyelerini kabul etmeye hazır olabiliriz. Yazılım mühendisliğinde her önemli kararda olduğu gibi, cevap nettir: Duruma bağlıdır.

Son olarak, analiz değerlendirme (evaluation) için anahtardır. Değerlendirme, bir şeyin değerini belirleme sürecidir. Şirketler, hisse fiyatlarını belirlemek için değerlendirilir. Bir şirketin çalışanları, zamlarını belirlemek için yılda bir kez değerlendirilir. Her iki durumda da, değerlendirme, şirketin veya çalışanın özelliklerinin analizine dayanır.

> **💬 Çevirmen notu:** Yazar burada analiz → değerlendirme → karar zincirini vurguluyor: Analiz, mimari kararlarınızın kalite nitelikleri, maliyet ve zaman üzerindeki etkilerini ölçülebilir hale getirerek, mimariyi savunulabilir ve paydaşlara karşı gerekçelendirilebilir kılar.

---

# 8.3 Analiz Teknikleri

Farklı projeler, riske farklı tepkiler gerektirir. Neyse ki biz mimarlar olarak
mimarileri analiz etmek için elimizin altında çok çeşitli araçlara sahibiz. Biraz
planlamayla, risk toleransımızı hem bütçe ve zaman kısıtlarımızı karşılayan
hem de makul düzeyde güvence sağlayan bir analiz teknikleri kümesiyle
eşleştirebiliriz. Buradaki nokta, analizin pahalı veya karmaşık olmak zorunda
olmadığıdır. Sadece düşünülmüş sorular sormak bile bir analiz biçimidir ve bu
alıştırma oldukça ucuzdur. Basit bir prototip inşa etmek daha pahalıdır, fakat
büyük bir proje bağlamında, Bölüm 5’te gördüğümüz gibi, riskleri keşfetme ve
hafifletme biçimi nedeniyle bu analiz tekniği ek maliyete fazlasıyla değebilir.

Hâlihazırda yaygın kullanımda olan (nispeten ekonomik, nispeten düşük
törenli) analiz tekniklerine örnek olarak tasarım gözden geçirmeleri (design
review) ve senaryo temelli analizler (scenario-based analysis), kod gözden
geçirmeleri (code review), eşli programlama (pair programming) ve Scrum
geriye dönük değerlendirme toplantıları (Scrum retrospective) verilebilir. Biraz
daha maliyetli olmakla birlikte yaygın olarak kullanılan diğer analiz teknikleri
arasında prototipler (atılabilir veya evrimsel) ve benzetimler (simülasyonlar)
yer alır.

Maliyet ve karmaşıklığın en üst düzeyinde, sistemlerimizin biçimsel
modellerini (formal model) inşa edebilir ve bunları gecikme (latency), güvenlik
(security) veya emniyet (safety) gibi özellikler açısından analiz edebiliriz. Bir
aday gerçekleştirim (candidate implementation) ya da nihayet sahaya sürülmüş
(fielded) bir sistem ortaya çıktığında, çalışan sistemleri enstrümante etmeyi
(instrumentation) ve veri toplamayı da içeren deneyler gerçekleştirebiliriz; ideali,
sistemin gerçekçi kullanım biçimlerini yansıtan yürütümlerinden veri toplamaktır.

Tablo 8.1’de gösterildiği gibi, bu tekniklerin maliyeti tipik olarak yazılım
geliştirme yaşam döngüsü (software development life cycle) boyunca ilerledikçe
artar. Bir prototip ya da deney, bir kontrol listesinden (checklist) daha pahalıdır;
kontrol listesi de deneyime dayalı bir benzetimden (experience-based analogy)
daha pahalıdır. Bu beklenen maliyet, analiz sonuçlarından duyabileceğiniz
güvenle oldukça güçlü şekilde koreledir. Ne yazık ki bedava öğle yemeği diye
bir şey yok!

---

# 8. Bölüm — Tasarım Sürecinde Analiz

## TABLO 8.1

### Yazılım Yaşam Döngüsünün Farklı Aşamalarında Analiz

| Yaşam Döngüsü Aşaması | Analiz Biçimi                             | Maliyet      | Güven          |
|-----------------------|-------------------------------------------|-------------:|----------------|
| Gereksinimler         | Deneyime dayalı benzetim (analogy)       | Düşük        | Düşük–yüksek   |
| Gereksinimler         | Kabaca hesap (back-of-the-envelope) analizi | Düşük     | Düşük–orta     |
| Mimari                | Düşünce deneyi / yansıtıcı sorular        | Düşük        | Düşük–orta     |
| Mimari                | Kontrol listesi temelli analiz            | Düşük        | Orta           |
| Mimari                | Taktik temelli analiz (tactics-based)     | Düşük        | Orta           |
| Mimari                | Senaryo temelli analiz (scenario-based)   | Düşük–orta   | Orta           |
| Mimari                | Analitik model                            | Düşük–orta   | Orta           |
| Mimari                | Simülasyon                                | Orta         | Orta           |
| Mimari                | Prototip                                  | Orta         | Orta–yüksek    |
| Gerçekleştirim        | Deney                                     | Orta–yüksek  | Orta–yüksek    |
| Sahadaki sistem       | Enstrümantasyon (instrumentation)         | Orta–yüksek  | Yüksek         |

## 8.4 Taktik Temelli Analiz (Tactics-Based Analysis)

Mimari taktikler (architectural tactics) (Bölüm 2.5.4’te tartışılmıştı) şu ana dek
tasarım ögeleri (design primitives) olarak sunuldu. Ancak bu sınıflandırmalar
(bu taksonomiler), bir kalite niteliğini (quality attribute) yönetmeye yönelik
mimari tasarım olasılıklarının tüm uzayını kapsayacak biçimde tasarlandığından,
onları bir analiz bağlamında da kullanabiliriz. Daha spesifik olarak, onları
mülakatlar veya anketler için birer rehber olarak kullanabiliriz. Bu mülakatlar,
bir analist olarak sizin, ele alınan veya alınmamış mimari yaklaşımlar hakkında
hızlı içgörü kazanmanıza yardımcı olur.

Örneğin, Şekil 8.1’de gösterilen erişilebilirlik (availability) taktiklerini

![Şekil 8.1](/home/runner/workspace/scripts/dsa_figs/sekil_8_1.png){width=9.6cm}

ele alalım.

> **💬 Çevirmen notu:** Buradaki “taktik”ler, belirli bir kalite niteliğini artırmak için uygulanabilen tekrarlanabilir, küçük mimari karar kalıplarıdır; “desen”den (pattern) daha ince tanelidir.

## 8.4 Taktik Temelli Analiz

### Erişilebilirlik (Availability) Taktikleri

- Hatalardan Kurtulma (Recover from Faults)
- Hataları Tespit Etme (Detect Faults)
- Hazırlık ve Onarım (Preparation and Repair)
  - Ping / Echo
  - İzleme (Monitor)
  - Kalp atışı (Heartbeat)
  - Zaman damgası (Timestamp)
  - Hata (Fault)
  - Etkin yedeklilik (Active Redundancy)
  - Pasif yedeklilik (Passive Redundancy)
  - Yedek (Spare)
  - Sağlamlık kontrolü (Sanity Checking)
  - İstisna işleme (Exception Handling)
  - Koşul izleme (Condition Monitoring)
  - Geri alma (Rollback)
  - Oylama (Voting)
  - Yazılım yükseltme (Software Upgrade)
  - İstisna tespiti (Exception Detection)
  - Yeniden deneme (Retry)
  - Öz test (Self-Test)
  - Hataları Önleme (Prevent Faults)
  - Yeniden devreye alma (Reintroduction)
  - Gölge (Shadow)
  - Servisten çıkarma (Removal from Service)
  - Durum yeniden eşzamanlama (State Resynchronization)
  - İşlemler (Transactions)
  - Kademeli yeniden başlatma (Escalating Restart)
  - Öngörücü model (Predictive Model)
  - Sürekli iletim (Non-Stop Forwarding)
  - İstisna önleme (Exception Prevention)
  - Hatanın maskelenmesi veya onarımın yapılması (Fault Masked or Repair Made)
  - Yeterlilik kümesini artırma (Increase Competence Set)
  - Hatalı davranışı yok sayma (Ignore Faulty Behavior)
  - Bozulma (Degradation)
  - Yeniden yapılandırma (Reconfiguration)

**Şekil 8.1** Erişilebilirlik taktikleri

Bu taktiklerin her biri, yüksek erişilebilirlikte bir sistem tasarlamak isteyen
mimar için bir tasarım seçeneğidir. Ancak geriye dönük olarak kullanıldıklarında,
erişilebilirlik için tüm tasarım uzayının bir sınıflandırmasını temsil ederler ve
dolayısıyla mimar tarafından verilmiş ve verilmemiş kararlar hakkında içgörü
edinmenin bir yolu olabilirler. Bunu yapmak için, her bir taktiği basitçe bir
mülakat sorusuna dönüştürürüz. Örneğin, Tablo 8.2’deki (kısmi) taktik
esinli erişilebilirlik soruları kümesini ele alın.

## TABLO 8.2

### Örnek Taktik Temelli Erişilebilirlik Soruları

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar |
|--------------|---------------|--------------------------|------|----------------------------|------------------------|
| Hataları tespit et | Sistem, bir bileşenin veya bağlantının ya da ağ tıkanıklığının (congestion) hatasını tespit etmek için ping/echo kullanıyor mu? | E | D | Sunucu, zaman sunucularının “canlı” olup olmadığını görmek için periyodik olarak onlara ping gönderir. | Sistem, bir bileşenin veya bağlantının ya da ağ tıkanıklığının hatasını tespit etmek için ping/echo kullanıyor mu? |
| Hataları tespit et | Sistem, diğer sistem parçalarının sağlık durumunu izleyen bir bileşen kullanıyor mu? Bir sistem izleyicisi (system monitor), ağdaki veya hizmet reddi (denial-of-service) saldırısı gibi diğer paylaşımlı kaynaklardaki hata ya da tıkanıklığı tespit edebilir. | H | Uygulanamaz | Bu sistemde bu uygulanmadı. Sistemi izlemek için başka tekniklere güveneceğiz. Örneğin, bellek tüketimi veya işlemci yükü bilgisi işletim sisteminden elde edilebilir. | İşletim sisteminin sağladığı bilginin ötesindeki bilginin kritik olmadığı varsayılmaktadır. |
| Hataları tespit et | Sistem, bir bileşenin veya bağlantının ya da ağ tıkanıklığının hatasını tespit etmek için bir sistem izleyici ile bir süreç arasında periyodik mesaj alışverişi anlamına gelen bir kalp atışı (heartbeat) kullanıyor mu? | E | D | Sunucu, istemcilere periyodik olarak bir kalp atışı gönderir. | Sunucunun, istemcilerden gelen ping isteklerini işlemek zorunda olmaması. Zaman sunucularının kalp atışı yaklaşımını uygulamak için değiştirilmesi mümkün değildir. |
| Hataları tespit et | Sistem, dağıtık sistemlerdeki yanlış olay sıralarını tespit etmek için zaman damgası (timestamp) kullanıyor mu? | E | O | Sunucudan istemcilere gönderilen olayların bir zaman damgası vardır; çünkü bunların alındıkları sıraya göre işlenmeleri gerekir. | İstemcilerin, ağın durumunun doğru bir gösterimini sergilemeleri istenmektedir; bu da sunucudan gelen tüm bildirimleri almalarını ve bunları doğru sırada işlemelerini içerir. |
| Hataları tespit et | Sistem, çoğaltılmış (replicated) bileşenlerin aynı sonuçları ürettiğini kontrol etmek için oylama (voting) kullanıyor mu? Kopyalanmış bileşenler, özdeş replikalar, işlevsel olarak yedekli ya da analitik olarak yedekli olabilir. | H | Uygulanamaz | Bu sistem tarafından buna gerek duyulmamaktadır. | — |
| Hataları tespit et | Sistem, normal yürütme akışını değiştiren bir sistem durumunu tespit etmek için istisna tespiti (exception detection) kullanıyor mu? Örneğin sistem istisnaları, parametre sınırları (parameter fences), parametre tip kontrolü, zaman aşımları (timeouts)? | E | D | Standart Java istisna yönetimi kullanılır ve tüm istisnalar bir günlük dosyasına (log) gönderilir. Zaman aşımları, istekler sunucuya gönderildiğinde istemci tarafında uygulanır. | Varsayım, Java’daki istisna mekanizmasının ve zaman aşımı kullanımının ihtiyaç duyulan her şeyi sağladığıdır. |
| Hataları tespit et | Sistem, doğru çalıştığını test etmek için kendi kendine test (self-test) yapabiliyor mu? | H | Uygulanamaz | Bu, özgün tasarımımızda dikkate alınmamıştı. | — |

Varsayım, izleme (monitoring) ve hata (exception) yönetiminin, doğru çalışmayı test etmek için yeterli bilgi sağlayacağı yönündedir.

Sistem etkin yedeklilik (active redundancy, hot spare) kullanıyor mu?  
Etkin yedeklilikte, bir koruma grubundaki (protection group) tüm düğümler (bir veya daha fazla düğümün “etkin” olduğu ve kalanların yedek yedekler olarak hizmet ettiği düğüm grubu) paralel olarak aynı girdileri alır ve işler; bu sayede yedek yedekler etkin düğüm(ler)le eşzamanlı durum (synchronous state) korur.

Y

H

Etkin yedeklilik, uygulama sunucusunda ve mesaj kuyruğunda kullanılmaktadır.

Etkin yedeklilik, zaman sunucularından toplanması gereken bilgilerin, sunucu hatası nedeniyle kaybedilmesi olasılığını azaltmak için pasif bir yaklaşıma kıyasla tercih edilmiştir. Bu, aslında QA-3’te belirlenmiş gereksinimi de aşmaktadır. Ayrıca, ortak kipli (common-mode) bir hata olmayacağını varsayıyoruz.
(devam ediyor)

183

N/A

8.4 Taktik Tabanlı Analiz (Tactics-Based Analysis)

Hatalardan
kurtarma
(hazırlık
ve onarım)

N

Risk

Tasarım Kararları ve Konumu

Gerekçe ve
Varsayımlar

184

Sistem pasif yedeklilik (passive redundancy, warm spare) kullanıyor mu?  
Pasif yedeklilikte, girdi trafiğini yalnızca koruma grubunun etkin üyeleri işler; görevlerinden biri de yedek yedeklere periyodik durum güncellemeleri sağlamaktır.

N

N/A

Etkin yedeklilik tercih edilmiştir.

N/A

Sistem, bir hata durumunda daha önce kaydedilmiş iyi bir duruma (“rollback line”) geri dönebilecek şekilde geri alma (rollback) kullanıyor mu?

Y

M

İşlem (transaction) yönetimi Spring çerçevesi (Spring framework) aracılığıyla desteklenmektedir.

Spring, bu sistemin ihtiyaç duyduğu türde işlemler için yeterli desteği sağlamaktadır.

Bölüm 8—Tasarım Sürecinde Analiz

Taktik
Grubu

Taktik Sorusu

Destekleniyor mu?
(Y/N)

8.5

Yansıtıcı Sorular (Reflective Questions)

185

Tablo 8.2’deki sorular bir görüşme ortamında kullanıldığında, mimarın görüşlerine göre sistemin mimarisi tarafından her bir taktiğin desteklenip desteklenmediğini kaydedebiliriz. Örneğin, tabloda yer alan sorular, Bölüm 4’te sunulan FCAPS sistemi için verilmiş tasarım kararları temel alınarak yanıtlanmıştır. Tabloda gösterilen cevapların oldukça kısa olduğuna dikkat edin; bunun nedeni bunun bir örnek olmasıdır; gerçek dünya uygulamalarında daha ayrıntılı açıklamalar teşvik edilir. Eğer mevcut bir sistemi analiz ediyorsak, ek olarak şu konuları da inceleyebiliriz:

§ Bu taktiğin kullanılmasında (ya da kullanılmamasında) herhangi bir bariz risk olup olmadığı. Taktiğin kullanıldığı durumda, burada sistemde nasıl gerçekleştirildiğini (örneğin özel yazılım kodu, çerçeveler (frameworks) ya da dışarıdan üretilmiş bileşenler aracılığıyla) kaydedebiliriz. Örneğin, etkin yedeklilik taktiğinin, uygulama sunucusunu ve veritabanı gibi diğer kritik bileşenleri çoğaltarak kullanıldığını (Bölüm 4’te sunulan durum çalışmasında olduğu gibi) not edebiliriz.  
§ Taktiği gerçekleştirmek için alınan belirli tasarım kararları ve gerçekleştirilmiş (realization) halinin kod tabanında (code base) nerede bulunabileceği. Bu bilgi, denetim (audit) ve mimari yeniden yapılandırma (architecture reconstruction) amaçları için yararlıdır. Bir önceki maddeyi örnekleyerek sürdürecek olursak, kaç adet uygulama sunucusu kopyası oluşturulduğunu ve bu kopyaların nerede konumlandığını (örneğin bir veri merkezinde aynı rafta, farklı raflarda, farklı veri merkezlerinde) sorgulayabiliriz.  
§ Bu taktiğin gerçekleştirilmesinde yapılan her türlü gerekçe veya varsayım. Örneğin, ortak kipli (common-mode) bir hatanın olmayacağını varsayabilir, bu yüzden kopyaların aynı donanım üzerinde çalışan, birbirinin aynı sanal makineler olmasını kabul edilebilir bulabiliriz.

Görüşme temelli bu yaklaşım kulağa basit gelebilir, ancak gerçekte oldukça güçlü ve ufuk açıcı olabilir. Bir mimar olarak günlük faaliyetlerinizde her zaman geri çekilip büyük resme bakmaya zaman ayırmayabilirsiniz. Tablo 8.2’de gösterilenler gibi bir dizi görüşme sorusu sizi tam da bunu yapmaya zorlar. Bu yaklaşım aynı zamanda oldukça verimlidir: Tek bir kalite niteliği (quality attribute) için tipik bir görüşme 30 ila 90 dakika sürer.

Yedi en önemli sistem kalite niteliğini—kullanılabilirlik (availability), birlikte işlerlik (interoperability), değiştirilebilirlik (modifiability), performans (performance), güvenlik (security), test edilebilirlik (testability) ve kullanılabilirlik (usability)—kapsayan taktik tabanlı soru kümeleri (questionnaire) Ek B’de bulunabilir. Ek olarak, diğer (daha temel) soru kümelerini bir araya getirerek, yeni bir kalite endişesi (quality concern) kümesini ele almak üzere yeni bir soru seti oluşturmanın nasıl yapılabileceğine örnek olarak, DevOps üzerine sekizinci bir soru kümesi de ekledik.

> **💬 Çevirmen notu:** Buradaki “soru kümesi (questionnaire)” ifadesi, her kalite niteliği için hazırlanmış yarı-yapılandırılmış görüşme formunu ifade ediyor; mimari inceleme sırasında sistematik olarak kullanılmak üzere tasarlanmışlardır.

8.5

Yansıtıcı Sorular (Reflective Questions)

Taktik temelli görüşmelere benzer şekilde, bazı araştırmacılar tasarımı desteklemek için yansıtıcı sorular sorma (ve yanıtlama) pratiğini savunmuştur. 

186

Bölüm 8—Tasarım Sürecinde Analiz

süreç. Bu sürecin ardındaki fikir, problem çözerken düşündüğümüz biçim ile
yansıma (reflection) sırasında düşündüğümüz biçimin aslında farklı olmasıdır.
Bu nedenle, araştırmacılar tasarımda, hem alınan kararları sorgulayan hem de
önyargılarımızı incelemeye zorlayan ayrı bir “yansıma (reflection)” etkinliği
önermişlerdir.

Mimarlar, tüm insanlar gibi, önyargılara tabidir. Örneğin, onaylama önyargısına (confirmation bias)—yeni bilgiyi, kendi önkabullerimizi doğrulayacak
şekilde yorumlama eğilimine—ve çapa önyargısına (anchoring bias)—bir problemi incelerken aldığımız ilk bilgiye aşırı derecede güvenme, bu bilgiyi sonraki
tüm bilgileri süzmek ve yargılamak için kullanma eğilimine—tabiyiz. Yansıtıcı
(reflective) sorular, bu tür önyargıları sistematik bir şekilde ortaya çıkarmaya
yardımcı olur; bu da varsayımlarımızı ve dolayısıyla tasarımlarımızı gözden
geçirmemize yol açabilir.

Yansıtıcı sorular üzerine yaptıkları araştırmada Razavian ve diğerleri, bağlam
(context) ve gereksinimler (requirements) üzerinde (Belirlenen bağlamlar ve gereksinimler ilgili, eksiksiz ve doğru mu?), tasarım problemleri üzerinde (Uygun ve eksiksiz biçimde ifade edilmişler mi?), tasarım çözümleri üzerinde (Gereksinimler göz önüne alındığında uygunlar mı?) ve tasarım kararları üzerinde
(Kurallı ve gerekçelendirilmişler mi?) düşünülmesi gerektiğini ve düşünülebileceğini ileri sürmüştür. Önerdikleri yansıtıcı sorulardan bazı örnekler şunlardır:

§ Hangi varsayımlar yapılmıştır? Bu varsayımlar tasarım problemini etkiler mi? Varsayımlar çözüm seçeneğini etkiler mi? Bir kararda bir varsayım kabul edilebilir midir?
§ Belirli olayların gerçekleşme riskleri nelerdir? Bu riskler tasarım problemlerine nasıl yol açar? Riskler bir çözümün uygulanabilirliğini nasıl etkiler?
Bir kararın riski kabul edilebilir midir? Riskleri azaltmak (mitigate) için ne
yapılabilir?
§ Bağlamların dayattığı kısıtlar nelerdir? Bu kısıtlar tasarım problemlerine
nasıl yol açar? Kısıtlar çözüm seçeneklerini nasıl sınırlar? Bir karar alınırken bazı kısıtlar gevşetilebilir mi?
§ Bu sistemin bağlamları ve gereksinimleri nelerdir? Bu bağlam ne anlama
gelir? Tasarım problemleri nelerdir? Çözülmesi gereken önemli problemler hangileridir? Bu problem ne anlama gelir? Bu problem için hangi
potansiyel çözümler vardır? Bu kararda takip edilmesi gereken başka problemler var mıdır?
§ Hangi bağlamlardan ödün verilebilir (kompromize edilebilir)? Bir problem farklı biçimde çerçevelenebilir mi? Çözüm seçenekleri nelerdir? Bir
çözüm seçeneğinden ödün verilebilir mi? Her bir çözümün artıları ve eksileri adil biçimde ele alınıyor mu? Ödünleşimler (tradeoff) sonrası en
iyi (optimal) çözüm nedir?

Elbette bu soruların hepsini kullanmak zorunda değilsiniz ve bu tekniği verdiğiniz her karar için uygulamazsınız. Ancak yerinde kullanıldığında bu tür
sorular, verdiğiniz kararlar üzerinde bilinçli (mindful) bir şekilde düşünmenize
yardımcı olabilir.

## 8.6 Senaryo Tabanlı Tasarım Gözden Geçirmeleri

Senaryo tabanlı kapsamlı tasarım gözden geçirmeleri, örneğin ATAM gibi olanlar, genellikle tasarım sürecinin dışında yürütülmüştür. ATAM, kapsamlı bir
mimari değerlendirme (architecture evaluation) örneğidir (bkz. “ATAM” kenar
kutusu).

ATAM incelemesi, ilk tasarlandığında, bir “kilometre taşı (milestone)” incelemesiydi. Bir mimar veya diğer anahtar paydaş (stakeholder), analiz yapılacak
yeterli düzeyde mimari ya da mimari tanım olduğuna inandığında bir ATAM
toplantısı düzenlenebilirdi. Bu, bir mimari tasarım tamamlandığında fakat henüz pek az ya da hiç gerçekleştirim (implementation) yapılmamışken gerçekleşebilirdi. Daha yaygın olarak, mevcut bir sistem hali hazırda kullanımdayken
ve bazı paydaşlar, mimariye bağlanmadan, onu evrimleştirmeden, satın almadan vb. önce mimarinin risklerine ilişkin nesnel bir değerlendirme istediklerinde ortaya çıkardı.

> **ATAM**  
> ATAM—Architecture Tradeoff Analysis Method (Mimari Ödünleşim Analizi Yöntemi), senaryolar tarafından yönlendirilen, yerleşik bir mimari
> analiz yöntemidir. Amacı, mimari kararların sonuçlarını kalite niteliği
> (quality attribute) gereksinimleri ve iş hedefleri ışığında değerlendirmektir.
> 
> ATAM, bir değerlendirmede üç grubu bir araya getirir:
> 
> § Eğitilmiş bir değerlendirme ekibi  
> § Bir mimarinin “karar vericileri”  
> § Mimarinin paydaşlarını temsil edenler  
> 
> ATAM, paydaşların, potansiyel olarak sorunlu mimari kararları—yani riskleri—ortaya çıkaracak doğru soruları sormalarına yardımcı olur. Keşfedilen bu riskler daha sonraki tasarım, ileri analiz, prototipleme ve gerçekleştirim gibi risk azaltma (risk mitigation) etkinliklerinin odağı yapılabilir.
> Ayrıca, çoğu zaman tasarım ödünleşimleri (design tradeoffs) de tanımlanır—yöntemin adındaki “tradeoff” buradan gelir. ATAM’ın amacı kesin
> analizler sağlamak değildir: Bu yöntem tipik olarak ikişer günlük iki
> toplantı şeklinde uygulanır ve bu (nispeten) kısa zaman dilimi, herhangi
> belirli bir endişe alanında derinlemesine inceleme yapmaya olanak vermez.
> Ancak bu tür derin analizler, ATAM sonrasında ve ATAM’ın yönlendirmesiyle yürütülebilecek risk azaltma etkinliklerinin bir parçası olarak uygundur.
> 
> ATAM, yazılım geliştirme yaşam döngüsü boyunca kullanılabilir. Örneğin şu durumlarda kullanılabilir:
> 
> § Bir mimari tanımlandıktan sonra, fakat henüz çok az ya da hiç kod yokken  
> § Olası mimari alternatifleri değerlendirmek için  
> § Mevcut bir sistemin mimarisini değerlendirmek için  
> 
> ATAM değerlendirmesinin çıktıları şunlardır:

> **💬 Çevirmen notu:** ATAM, SEI (Software Engineering Institute) tarafından geliştirilmiş yaygın bir mimari değerlendirme yöntemidir; uygulamada genellikle atölye (workshop) formatında yürütülür.

---

8.6

Senaryo Tabanlı Tasarım Gözden Geçirmeleri

---

8.6

Bölüm 8—Tasarım Sürecinde Analiz

§ Mimariye ilişkin özlü bir sunum. Mimari bir saat içinde sunulur.  
§ İncelenen sistem için iş hedeflerinin özlü bir şekilde ifade edilmesi. ATAM sırasında sunulan iş hedefleri, çoğu zaman toplantıya katılan bazı katılımcılar tarafından ilk kez görülür ve bu hedefler çıktılarda yakalanır (kayıt altına alınır).  
§ Senaryolar şeklinde ifade edilmiş, önceliklendirilmiş bir kalite niteliği (quality attribute) gereksinimleri kümesi.  
§ Mimari kararların kalite gereksinimlerine eşlenmesi. İncelenen her bir kalite niteliği senaryosu için, onu gerçekleştirmeye yardımcı olan mimari kararlar belirlenir ve kaydedilir.  
§ Duyarlılık (sensitivity) ve ödünleşim (tradeoff) noktalarından oluşan bir küme. Bu mimari kararların bir veya daha fazla kalite niteliği üzerinde belirgin bir etkisi vardır.  
§ Riskler ve risk olmayanlardan oluşan bir küme. Risk, kalite niteliği gereksinimleri ışığında istenmeyen sonuçlara yol açabilecek bir mimari karar olarak tanımlanır. Risk olmayan (non-risk) ise, analiz sonucunda güvenli kabul edilen mimari karardır. Belirlenen riskler, mimari risk azaltma planının temelini oluşturur.  
§ Risk temalarından oluşan bir küme. Değerlendirme ekibi, keşfedilen tüm riskler kümesini inceleyerek, mimarideki (hatta belki mimari süreç ve ekipteki) sistemik zayıflıkları açığa çıkaran kapsayıcı temaları belirler. Bu zayıflıklar ele alınmadan bırakılırsa, projenin iş hedeflerine ulaşma yeteneğini tehdit edecektir.

ATAM tabanlı bir değerlendirmenin somut olmayan sonuçları da vardır: paydaşlar (stakeholder) arasında gelişen bir topluluk hissi, mimar ile paydaşlar arasında açılan iletişim kanalları, mimarinin ve onun güçlü/zayıf yanlarının daha iyi anlaşılması. Bu sonuçlar ölçülmesi güç olmakla birlikte, diğerleri kadar önemlidir ve çoğu zaman en uzun ömürlü çıktılar bunlardır.

Bir ATAM değerlendirmesi dört aşamada gerçekleşir. İlk aşama (aşama 0) ve son aşama (aşama 3) yönetseldir: başta değerlendirmeyi kurmak/planlamak ve sonunda sonuçları ve devam edecek faaliyetleri raporlamak. Orta aşamalar (aşamalar 1 ve 2) ise asıl analizin yapıldığı kısımdır. 1 ve 2. aşamalarda gerçekleştirilen adımlar şunlardır:

1. ATAM’ı sun  
2. İş yönlendiricilerini (business drivers) sun  
3. Mimarinin sunulması  
4. Mimari yaklaşımların tanımlanması  
5. Bir kalite niteliği fayda ağacı (utility tree) üret  
6. Mimari yaklaşımların analizi  
7. Senaryo beyin fırtınası ve önceliklendirme  
8. Mimari yaklaşımların analizi  
9. Sonuçların sunulması  

### 8.6 Senaryo Tabanlı Tasarım Gözden Geçirmeleri

1. aşamada, 1–6. adımları küçük ve içsel bir paydaş grubu ile uygularız — tipik olarak sadece mimar, proje yöneticisi ve belki bir veya iki kıdemli geliştirici. 2. aşamada ise daha geniş bir paydaş grubunu davet ederiz — 1. aşamaya katılan herkes artı müşteri temsilcileri, son kullanıcı temsilcileri, kalite güvence (QA), operasyon gibi dış paydaşlar. 2. aşamada 1–6. adımları gözden geçirir ve 7–9. adımları gerçekleştiririz.

Asıl analiz 6. adımda yapılır; burada mimari yaklaşımları, mimardan, tek tek, en yüksek öncelikli senaryoları tanımlanmış mimari yaklaşımlara eşlemesini isteyerek analiz ederiz. Bu adım sırasında analistler, kalite niteliklerine dair bilgileriyle motive olarak derinleştirici sorular sorar ve riskler keşfedilip belgelendirilir.

Mimari “bittikten” sonra ondan ayrı ve farklı bir değerlendirme etkinliğinin yapılması fikri, bugün çoğu organizasyonun çalışma biçimiyle pek uyuşmaz. Bugün çoğu yazılım organizasyonu bir tür Çevik (Agile) ya da yinelemeli (iterative) geliştirme uygulamaktadır. Çevik süreçlerde ayrı, yekpare bir “mimari aşaması” yoktur. Bunun yerine mimari ve geliştirme, bir dizi sprint içinde birlikte yaratılır. Örneğin, Bölüm 2’de tartışıldığı gibi, birçok Çevik düşünce lideri, “ölçekli disiplinli çeviklik (disciplined agility at scale)”, “yürüyen iskelet (walking skeleton)” ve “ölçekli Çevik çerçeve (scaled Agile framework)” gibi uygulamaları savunmaktadır; bunların tümü, mimarilerin sürekli olarak nispeten küçük artışlarla evrimleştiği ve en kritik riskleri ele aldığı fikrini benimser. Bu, küçük bir kavram kanıtı (proof-of-concept) ya da asgari uygulanabilir ürün (minimum viable product, MVP) geliştirilmesi ya da stratejik prototipleme (strategic prototyping) yapılmasıyla desteklenebilir.

Bu yazılım geliştirme görüşüyle daha iyi hizalanmak için, ATAM’a dayalı hafif bir senaryo tabanlı akran gözden geçirme (peer review) yöntemi önerilmiştir. Hafif bir ATAM değerlendirmesi yarım günlük bir toplantıda gerçekleştirilebilir. Ayrıca, yalnızca proje üyeleri kullanılarak, içsel olarak da yürütülebilir. Elbette dış bir gözden geçirme daha fazla nesnellik sağlar ve daha iyi sonuçlar üretebilir, ancak bu çalışma, maliyet, takvim ya da fikri mülkiyet (intellectual property, IP) kısıtları nedeniyle fazla pahalı veya uygulanamaz olabilir. Bu nedenle hafif bir ATAM, maliyetli ama daha nesnel ve kapsamlı bir ATAM ile hiç analiz yapmama ya da yalnızca geçici (ad hoc) analiz yapma arasında makul bir orta yol sağlar.

Proje üyelerinin kendi projeleri üzerinde gerçekleştirdiği hafif bir ATAM değerlendirmesi için örnek bir program Tablo 8.3’te verilmiştir.

### Tablo 8.3 Hafif Bir ATAM Değerlendirmesi için Tipik Gündem

| Adım | Ayrılan Süre | Notlar |
| --- | --- | --- |
| 1. İş yönlendiricilerini sun | 0,25 saat | Katılımcıların sistemin ve onun iş hedeflerinin ve önceliklerinin farkında oldukları varsayılmaktadır. Bunların herkesin zihninde taze olduğundan ve sürpriz olmadığından emin olmak için kısa bir gözden geçirme amacıyla on beş dakika ayrılmıştır. |
| 2. Mimarinin sunulması | 0,5 saat | Tüm katılımcıların sistemle aşina oldukları varsayılır; bu nedenle mimarinin kısa bir genel görünümü sunulur ve belgelendirilmiş mimari görünüşler (architecture views) üzerinden 1 veya 2 senaryo izlenir. |
| 3. Mimari yaklaşımların tanımlanması | 0,25 saat | Belirli kalite niteliği kaygıları için mimari yaklaşımlar mimar tarafından tanımlanır. Bu, 2. adımın bir parçası olarak da yapılabilir. |
| 4. Kalite niteliği fayda ağacının üretilmesi | 0,5 saat | Senaryolar hâlihazırda mevcut olabilir; öyleyse bunları kullanın. Bir fayda ağacı (utility tree) zaten mevcut olabilir; öyleyse ekip bunu gözden geçirir ve gerekiyorsa günceller. |
| 5. Mimari yaklaşımların analizi | 2,0 saat | Yüksek sıralamaya sahip senaryoların mimariye eşlenmesi adımı, sürenin büyük bölümünü tüketir ve gerektikçe genişletilip daraltılabilir. |
| 6. Sonuçların sunulması | 0,5 saat | Değerlendirmenin sonunda ekip, mevcut ve yeni keşfedilen riskleri ve ödünleşimleri gözden geçirir ve öncelikleri tartışır. |
| **TOPLAM** | **4 saat** |  |

Yarım günlük bu tür bir gözden geçirme, çaba açısından, tipik olarak bir geliştirme projesinde yürütülen diğer kalite güvence faaliyetlerine — örneğin kod gözden geçirmeleri, incelemeler (inspections) ve yürütmeler (walk-throughs) — benzer niteliktedir. Bu nedenle, özellikle mimari kararların verildiği, sorgulandığı veya değiştirildiği sprint’lerde, hafif bir ATAM değerlendirmesini bir sprint içine planlamak kolaydır.

### 8.7 Mimari Açıklama Dilleri (Architecture Description Languages)

Eğer geliştirdiğiniz uygulamanın çalışma zamanı performansı (gecikme, veri
işleme hızı), güvenilirlik/erişilebilirlik, emniyet (safety) ya da güvenlik alanlarında katı kalite gereksinimleri varsa, mimari kararlarınızı mimari yapılar biçiminde bir mimari tanımlama dili (architecture description language, ADL) ile
belgelemeniz düşünülebilir. ADL’ler biçimsel, otomatik analize elverişlidir; tam
da bu nedenle burada onlara yer veriyoruz. ADL’ler tipik olarak bir mimariyi
—özellikle hesaplamaya ilişkin (çalışma zamanı) bileşenleri ve bunlar arasındaki
etkileşimleri— ve özelliklerini tanımlamak için hem görsel hem de (biçimsel
olarak tanımlanmış) metinsel gösterim kullanır. Birleşik Modelleme Dili (Unified Modeling Language, UML) endüstriyel uygulamada mimarileri belgelemede en yaygın kullanılan gösterimdir; gerçi o bile evrensel olarak kullanılmamaktadır. Az sayıda endüstriyel proje, mimarilerinin tamamını veya çoğunu
herhangi bir ADL ile tanımlamaya girişmektedir.

Bazı ADL’ler, örneğin AADL, kesin ve karara bağlanabilir (decidable)
anlamlara (semantics) sahip biçimsel modeller olmayı amaçlar. Bu disiplin, ilgi
duyulan özellikler —tipik olarak performans, erişilebilirlik ve emniyet— açısından otomatik olarak denetlenebilmeleri anlamına gelir; ilke olarak diğer kalite
nitelikleri (quality attribute) de desteklenebilir. Dille ve çevresindeki araç takımıyla yetkinleşmek için genellikle dik bir öğrenme eğrisi bulunsa da, biçimselleştirilmiş bir ADL kullanmak çeşitli faydalar sunar. İlk olarak, bir ADL mimari
kararlarınızı belgelemenizi zorunlu kılar; böylece mimari anlayışınızın ne zaman
ve nerede eksik ya da muğlak olduğunu açıkça kabul etmenizi sağlar. Bu fayda
her tür belgeleme ile elde edilir —sizi açık olmaya zorlar— ancak ADL’ler için
özellikle geçerlidir. Bu da ADL’lerin ikinci faydasına götürür: Genellikle, tek
bir düğmeye tıklayarak mimari tanımı çeşitli özellikler açısından analiz edebilen
bir araç takımı ile birlikte gelirler.

Peki neden ADL’ler akademi dışında nadiren kullanılır? Bu isteksizliğin
bir dizi olası nedeni vardır. İlk olarak, bu bizim yaygın uygulama biçimimizde
yer etmemiştir. ADL’ler —UML bile— tipik olarak bilgisayar bilimi ya da yazılım
mühendisliği müfredatında öğretilmez ve çoğu popüler tümleşik geliştirme
ortamında (IDE) iyi desteklenmez. İkinci olarak, ADL’lerin kullanımı zor ve
kullanıcı dostu olmayan, başta büyük bir çaba ve sürdürmek için de yüksek
sürekli emek gerektiren araçlar olarak algılanır. Bu nokta muhtemelen en önemlisidir: Mimarlar ve programcılar genellikle sistemleri hakkında ikinci, paralel
bir bilgi tabanını sürdürmek istemezler. Bazı sistemler için bu doğru tercih
olabilir. Ancak diğerleri —tipik olarak katı ve ödün verilemez kalite niteliği
gereksinimlerine sahip olanlar— için, tasarımın ayrı ve ayrı ayrı analiz edilebilir
bir temsilini bulundurmak en tedbirli hareket tarzı olabilir. Karşılaştırma olsun
diye inşaat mühendisliğinde hiçbir projeye, önce ayrı, analiz edilebilir bir belge
ile temsil edilmeden inşaat izni verilmez.

## 8.8 Özet

Test edilmemiş bir kodu sahaya sürmeyi kimse düşünmez — yine de mimarlar
ve programcılar düzenli olarak analiz edilmemiş mimari kararları uygulamayı
(koda dökmeyi) taahhüt ederler. Neden bu ikilik? Kodun test edilmesi önemli
ise, vermiş olduğunuz tasarım kararlarının “test edilmesi” kat kat daha önemli
olmalıdır; çünkü bu kararlar çoğu zaman uzun vadeli, sistem çapında ve önemli
etkilere sahiptir.

Bu bölümün en önemli mesajı, tasarım ve analizin aslında gerçekten ayrı
etkinlikler olmadığıdır. Verdiğiniz her önemli tasarım kararı analiz edilmelidir.
Bunu sürekli, nispeten kesintisiz bir biçimde, bir sistemi tasarlama ve evrimleştirme sürecinin parçası olarak yapabilmek için çeşitli teknikler uygulanabilir.

İlginç sorular, analiz edip etmemek değil, ne kadar analiz edeceğiniz ve ne
zaman analiz edeceğinizdir. Analiz, iyi tasarım yapmanın ayrılmaz bir parçasıdır
ve sürekli bir süreç olmalıdır.

## 8.9 Ek Okumalar

Burada kullanılan mimari taktik (architectural tactic) kümeleri, L. Bass,
P. Clements ve R. Kazman, *Software Architecture in Practice* (3. baskı),
Addison-Wesley, 2012’de belgelenmiştir. Erişilebilirlik taktikleri ilk kez
J. Scott ve R. Kazman, “Realizing and Refining Architectural Tactics: Availability”, CMU/SEI-2009-TR-006, 2009’da oluşturulmuştur.

Yansıtıcı sorular (reflective questions) fikri ilk kez M. Razavian,
A. Tang, R. Capilla ve P. Lago, “In Two Minds: How Reflections Influence
Software Architecture Design Thinking”, VU University Amsterdam, Teknik
Rapor 2015-001, Nisan 2015’te ortaya konmuştur. Yazılım tasarımcılarının
“satisficing” yaptığı —yani optimal bir çözüm yerine “yeterince iyi” bir çözüm
aradıkları— fikri A. Tang ve H. van Vliet, “Software Designers Satisfice”,
European Conference on Software Architecture (ECSA 2015), 2015’te tartışılmıştır.

ATAM (Architecture Tradeoff Analysis Method) kapsamlı biçimde
P. Clements, R. Kazman ve M. Klein, *Evaluating Software Architectures:
Methods and Case Studies*, Addison-Wesley, 2001’de tanımlanmıştır. Hafif
(lightweight) ATAM ilk olarak L. Bass, P. Clements ve R. Kazman, *Software
Architecture in Practice* (3. baskı), Addison-Wesley, 2012’de sunulmuştur.
Buna ek olarak, ATAM tarzı akran incelemeleri F. Bachmann, “Give the
Stakeholders What They Want: Design Peer Reviews the ATAM Style”,
*Crosstalk*, Kasım/Aralık 2011’de tanımlanmıştır.

Mimari tanımlama dillerinin (architecture description language, ADL)
tarihi, yazılım mimarisinin tarihi kadar eskidir. Uygulamada en yaygın kullanılan
ADL, AADL’dir (Architecture Analysis and Design Language); bu dil
P. Feiler ve D. Gluch, *Model-Based Engineering with AADL: An Introduction
to the SAE Architecture Analysis & Design Language*, Addison-Wesley, 2013’te
tanımlanmıştır. ADL’lere ilişkin bir genel bakış ve endüstriyel gereksinimlerin
analizi I. Malavolta, P. Lago, H. Muccini, P. Pelliccione ve A. Tang, “What
Industry Needs from Architectural Languages: A Survey”, *IEEE Transactions
on Software Engineering*, 39(6):869–891, Haziran 2013’te bulunabilir.

# 9. Kuruluşta Mimari Tasarım Süreci

Bölüm 1, gereksinim toplama, mimari tasarlama, mimariyi değerlendirme ve
uygulama gibi bir dizi yazılım mimarisi yaşam döngüsü etkinliği tanıtmıştı. Bunlara “yaşam döngüsü etkinlikleri” dedik; çünkü tüm kuruluşların bunların hepsini
yapmadığını, yapanların ise bunları farklı biçimlerde uygulayabileceğini ve farklı yaşam döngüsü modellerine ve kurumsal bağlamlara gömebileceğini kabul
ediyoruz. Bu bölüm, yazılım geliştirmeye ilişkin bu yönlere daha yakından bakar
ve mimari tasarımın bunlarla nasıl uyumlandığını ele alır.

## 9.1 Mimari Tasarım ve Geliştirme Yaşam Döngüsü

Şekil 9.1’de gösterildiği gibi, çoğu geliştirme projesinde gerçekleşen iki önemli

![Şekil 9.1](/home/runner/workspace/scripts/dsa_figs/sekil_9_1.png){width=9.63cm}

aşama, ön satış (pre-sales) ve geliştirme ile işletmedir (development and operations).

Pre-Sales  
Architecture Design

Architecture Design

ŞEKİL 9.1 Proje geliştirmenin iki ana aşaması

§ Satış öncesi (pre-sales) aşamasında projenin kapsamı belirlenir ve bir iş gerekçesi (business case) oluşturulur. Bu aşamaya “satış öncesi” desek de, “satış” yapıp yapmadıklarından bağımsız olarak her organizasyonda gerçekleşir. Bu aşamanın sık rastlanan ve önemli çıktılarından biri, projenin maliyeti ve süresine ilişkin bir tahmindir. Bu tahmin, müşteriler (veya fon sağlayanlar) tarafından projeyi sürdürmek isteyip istemediklerine karar vermek için kullanılır.

§ Geliştirme ve işletim (operations) aşaması, satış öncesi teklifin müşteri tarafından kabul edilmesiyle başlar. Geliştirme, Agile, RUP (Rational Unified Process) veya TSP (Team Software Process) gibi farklı metodolojiler izlenerek gerçekleştirilebilir. Sistem (veya bir parçası) geliştirildiğinde işletime alınır. DevOps gibi daha yeni yaklaşımlar, genellikle geliştirme ve işletim arasında bulunan boşluğu azaltmayı amaçlar.

Mimari tasarım, şimdi tartışacağımız üzere bu iki temel aşamada önemli bir rol oynar.

## 9.1.1 Satış Öncesinde Mimari Tasarım

Birçok türde geliştirme projesinde, özellikle de özel (custom) yazılım geliştirme bağlamında, organizasyonların satış öncesi (pre-sales) aşamada proje süresi ve maliyetine ilişkin ilk tahmini sağlaması gerekir. Çoğu zaman satış öncesi faaliyetler kısa bir zaman aralığında gerçekleştirilmek zorundadır ve bu süreci bilgilendirecek bilgi miktarı her zaman sınırlıdır. Örneğin, bu aşamada genellikle yalnızca üst düzey gereksinimler veya özellikler (detaylı kullanım senaryoları (use case) yerine) mevcuttur.

Sınırlı bilgiyle ilgili sorun, üretilen tahminin çoğu zaman önemli belirsizlik içermesidir; bu durum Şekil 9.2’de gösterilen belirsizlik konisi (cone of uncertainty) ile betimlenmiştir. Belirsizlik konisi, bir projedeki tahminleri çevreleyen belirsizliğe işaret eder; genellikle maliyet ve zaman çizelgesi (schedule) tahminleri için kullanılır, ancak risk için de geçerlidir. Proje ilerledikçe tüm bu tahminler daha iyi hale gelir ve koni daralır. Proje bittiğinde belirsizlik sıfırdır. Herhangi bir geliştirme metodolojisi için temel mesele, belirsizlik konisini projenin yaşam döngüsünün daha erken safhalarında nasıl daraltacağıdır.

![Şekil 9.2](/home/runner/workspace/scripts/dsa_figs/sekil_9_2.png){width=11.85cm}


### 9.1 Mimari Tasarım ve Geliştirme Yaşam Döngüsü

195

1.6x

1.25x  
1.15x  
1.1x  
x  
0.9x  
0.85x  
0.8x  

0.6x  
Initial  
Project  
Definition  

Approved  
Project  
Definition  

Requirements  
Specification  

Product  
Design  
Specification  

Detailed  
Design  
Specification  

Accepted  
Software  

**ŞEKİL 9.2** Örnek belirsizlik konisi (example cone of uncertainty)

Mimari uygulamalar satış öncesi aşamada belirsizlik konisini daraltmaya yardımcı olmak için uygulanabilir:

§ Mimari sürücüler (architectural driver) satış öncesi aşamada tanımlanabilir. Bu noktada detaylı kalite niteliği senaryolarını (quality attribute scenario) betimlemek zor olsa da, en önemli kalite nitelikleri (quality attribute) için başlangıç metrikleri ve kısıtlar tanımlanmalıdır.

§ ADD (Attribute-Driven Design, nitelik temelli tasarım) kullanılarak, erken maliyet ve zaman tahminlerinin temeli olarak kullanılacak ilk mimari üretilebilir.

§ Bu ilk mimarinin eskizleri, müşteriyle iletişim için faydalıdır. Ayrıca bu eskizler, bu ilk tasarımın hafif (lightweight) değerlendirmelerini yapmak için de temel olarak kullanılabilir.

İlk bir mimari üretmek, tahminin “standart bileşenler (standard components)” tekniği kullanılarak yapılmasına olanak tanır. Standart bileşenler bir tür vekildir (proxy); örneğin web sayfaları, iş kuralları (business rule), raporlar ve benzeri öğeleri içerir. Standart bileşenlerle tahmin yaparken şirketler tipik olarak, önceden geliştirilmiş sistemlere dahil edilmiş bileşenlere ait ölçümler ve boyut (size) verilerini içeren tarihsel veritabanları oluştururlar. Standart bileşenlerle tahmin yapmak için, çözmeye çalıştığınız problem için gerekli olacak bileşenleri belirlemeniz ve sonra bu bileşenlerin boyutunu tahmin etmek için tarihsel verileri (veya Wideband Delphi gibi başka bir tekniği) kullanmanız gerekir. Toplam boyut daha sonra çabaya (effort) dönüştürülebilir ve bu tahminler birleştirilerek proje düzeyinde süre ve maliyet tahmini üretilebilir.

Bu teknikle tahmin yaratmak için gerekli bileşenlerin belirlenmesi, ADD kullanılarak kısa bir zaman dilimi içinde başarılabilir. Bu yaklaşım, az önce sıfırdan (greenfield) sistem tasarımı için önerdiklerimize benzer:

§ İlk tasarım yinelemenizin (iteration) hedefi, uygulama için ilk genel yapıyı (overall structure) kurma sorununu ele almak olmalıdır. Eğer bir başvuru mimarisi (reference architecture) kullanıyorsanız, bu mimari tahminde kullanılacak standart bileşen türlerini belirler. Bu noktada, özellikle tarihsel verileriniz belirli teknolojilere bağlıysa, projede kullanılacak en ilgili teknolojiler de seçilebilir.

§ İkinci tasarım yinelemenizin hedefi, tahminde dikkate alınması gereken tüm işlevselliği destekleyecek bileşenleri tanımlamak olmalıdır. Sıfırdan sistem tasarımı için tartıştıklarımızın aksine, tahmin üretmek için tasarım yaparken yalnızca birincil işlevselliği (primary functionality) değil, daha fazlasını göz önünde bulundurmanız gerekir. Standart bileşenleri tanımlayabilmek için kapsamın bir parçası olan tüm önemli işlevsel gereksinimleri göz önüne almalı ve bunları ilk yinelemede tanımladığınız yapıya eşlemelisiniz (map). Bunu yapmak, daha doğru bir tahmin elde etmenizi sağlar.

Bu teknik, en önemli işlevsel gereksinimlerin karşılanması için maliyet ve zaman çizelgesini tahmin etmenize yardımcı olacaktır. Ancak bu noktada muhtemelen kalite niteliklerini dikkate almamış olacaksınız. Bunun sonucu olarak, sürücü (driving) kalite niteliklerini ele almak için tasarım kararları vereceğiniz yerleri hedefleyen birkaç yineleme daha yapmalısınız. Satış öncesi süreci gerçekleştirmek için mevcut zaman sınırlıysa, tasarımı çok detaylı işleyemeyeceksiniz; bu nedenle burada almanız gereken kararlar, tahmin üzerinde önemli etkisi olacak kararlardır. Örneğin, performans, erişilebilirlik (availability) ve güvenlik gibi kalite niteliklerini ele almak için yedekli donanımı veya ek standart bileşenleri tanımlamak buna dahildir.

Bu teknik satış öncesi süreçte kullanıldığında, başlangıç niteliğinde bir mimari tasarım üretilir—satış öncesi mimari tasarım (pre-sales architecture design) (bkz. Şekil 9.1). Proje teklifi müşteri tarafından kabul edilir ve proje devam ederse, bu ilk mimari bir sözleşmenin dayanaklarından biri haline gelebilir. Bu mimari, projenin Geliştirme ve İşletim (Development and Operation) aşamasında gerçekleştirilen sonraki mimari tasarım faaliyetlerinde başlangıç noktası olarak kullanılmalıdır. Bu durumda, kahverengi alan (brownfield) sistemleri tasarlamaya ilişkin yol haritası (Section 3.3.3’te tartışılmıştır) kullanılabilir.

Bu ilk mimari için üretilen ön dokümantasyon (preliminary documentation) ayrıca müşteriye sunulan teknik teklifin bir parçası olarak da dahil edilebilir. Son olarak, bu başlangıç mimari tasarım, tercihen tahminleme gerçekleşmeden önce, değerlendirilebilir. Bu, Bölüm 8.6’da sunulan hafif ATAM (Architecture Tradeoff Analysis Method) gibi bir teknik kullanılarak gerçekleştirilebilir.

### 9.1 Mimari Tasarım ve Geliştirme Yaşam Döngüsü

197

## 9.1.2 Geliştirme ve İşletim Sırasında Mimari Tasarım

Yazılım sisteminin geliştirilmesi farklı yöntemler kullanılarak gerçekleştirilebilir. Ancak mimari tasarım, seçilen geliştirme yönteminden bağımsız olarak gerçekleştirilir. Bu nedenle, ADD (Attribute-Driven Design, nitelik temelli tasarım) gibi bir tasarım yöntemi, farklı geliştirme yöntemleriyle birlikte kullanılabilir. Şimdi, endüstride yaygın olarak kullanılan bazı geliştirme yöntemleriyle mimari tasarım arasındaki ilişkiyi tartışacağız.

### 9.1.2.1 Çevik (Agile) Yöntemler

Yazılım mimarisi ile çeviklik (agility) arasındaki ilişki, son on yıldır tartışma konusu olmuştur. Her ne kadar biz ve birçok araştırma, mimari uygulamalar ile Çevik (Agile) uygulamaların aslında birbirleriyle iyi hizalandığını göstersek de, bu görüş her zaman evrensel biçimde kabul görmemiştir.

Özgün Agile Manifesto’ya göre çevik uygulamalar şu değerlere vurgu yapar: “Süreçler ve araçlardan ziyade bireyler ve etkileşimler, kapsamlı dokümantasyondan ziyade çalışan yazılım, sözleşme müzakeresinden ziyade müşteriyle iş birliği ve bir planı takip etmekten ziyade değişime yanıt vermek”. Bu değerlerin hiçbirisi, doğası gereği mimari uygulamalarla çelişmez. Peki o zaman neden —en azından bazı çevrelerde— bu iki uygulama kümesinin birbiriyle bağdaşmaz olduğuna dair bir inanç ortaya çıkmıştır? Meselenin özü, Çevik uygulamalar ile mimari uygulamaların farklılaştığı tek ilkedir.

Agile Manifesto’nun ilk yaratıcıları, manifestonun arkasında yatan 12 ilkeyi tanımlamışlardır. Bu 12 ilkeden 11’i mimari uygulamalarla tamamen uyumludur; uyumlu olmayan yalnızca bir tanesidir: “En iyi mimariler, gereksinimler ve tasarımlar kendini örgütleyen (self-organizing) takımlardan ortaya çıkar.” Bu ilke küçük ve belki orta ölçekli projeler için geçerli olmuş olabilir, ancak büyük projelerde —özellikle karmaşık gereksinimlere ve dağıtık geliştirmeye sahip olanlarda— başarılı olduğuna dair herhangi bir örnekten haberdar değiliz. Sorunun kalbinde şu vardır: Yazılım mimarisi tasarımı “en başta yapılan” (up-front) bir iştir. Bir projeye her zaman doğrudan kod yazarak ve en az düzeyde, hatta hiç en başta analiz veya tasarım yapmadan başlayabilirsiniz. Buna, Şekil 9.3b’de gösterildiği gibi, türeyen (emergent) yaklaşım diyoruz. Bazı durumlarda —küçük sistemler, atılacak (throw-away) prototipler, müşteri gereksinimleri hakkında çok az fikir sahibi olduğunuz sistemler— bu, gerçekte en uygun karar olabilir. Diğer uçta ise, bütün gereksinimleri baştan toplamaya, bundan ideal mimariyi türetmeye, ardından da bu mimariyi gerçekleştirip test etmeye ve dağıtmaya çalışabilirsiniz. Şekil 9.3a’da gösterilen bu sözde En Baştan Büyük Tasarım yaklaşımı (Big Design Up Front, BDUF), genellikle klasik Şelale (Waterfall) yazılım geliştirme modeliyle ilişkilendirilir. Şelale modeli, geçtiğimiz on yıl içinde karmaşıklığı ve katılığı nedeniyle gözden düşmüştür; bu da çok sayıda iyi belgelenmiş maliyet aşımları, takvim (zaman) aşımları ve müşteri memnuniyetsizliği vakasına yol açmıştır. Mimari tasarım açısından bakıldığında, BDUF yaklaşımının olumsuz tarafı, kapsamlı biçimde belgelenmiş ancak test edilmemiş ve uygun olmayabilecek bir tasarım üretebilmesidir. Bu durum, tasarımdaki problemlerin genellikle geç fark edilmesi ve çok miktarda yeniden çalışma gerektirmesi, ya da özgün tasarımın en sonunda görmezden gelinmesi ve gerçek mimarinin hiç belgelenmemesi nedeniyle ortaya çıkar.

![Şekil 9.3](/home/runner/workspace/scripts/dsa_figs/sekil_9_3.png){width=8.08cm}


  
Chapter 9—The Architecture Design Process in the Organization

Design Effort

Design Effort  
Project Iterations  

Time  

(a) BDUF Approach  

Time  

(b) Emergent Approach  

Design Effort  
Project Iterations  

Time  

(c) Iteration 0 Approach  

ŞEKİL 9.3 Mimari tasarıma yönelik üç yaklaşım

Açıkçası, bu uç yaklaşımların hiçbiri, gereksinimlerin bir kısmının (ama tamamının değil) en başta iyi anlaşıldığı, fakat aynı zamanda çok fazla işi çok erken yapma ve bu yüzden kaçınılmaz olarak değiştirilmesi gerekecek bir çözüme kilitlenme riskinin bulunduğu çoğu gerçek dünya projesi için mantıklı değildir. Dolayısıyla gerçekten ilginç soru şudur: Bir proje, gereksinim analizi, risk azaltma (risk mitigation) ve mimari açısından ne kadar en başta çalışma yapmalıdır? Boehm ve Turner, bu sorunun tek bir doğru cevabı olmadığını, ancak herhangi bir proje için bir “tatlı nokta” (sweet spot) bulunabileceğini öne süren kanıtlar sunmuştur. Projedeki “doğru” miktarda iş, birkaç faktöre bağlıdır; bunların en baskını proje büyüklüğüdür; ancak diğer önemli faktörler arasında gereksinimlerin karmaşıklığı, gereksinimlerin oynaklığı (requirements volatility; alanın daha önce benzer biçimde ele alınıp alınmadığına, yani domain precedentedness durumuna bağlıdır) ve geliştirme faaliyetinin ne ölçüde dağıtık olduğu yer alır.

Peki mimarlar doğru miktarda çevikliği (agility) nasıl elde eder? En baştaki çalışma ile, yeniden çalışmaya yol açan teknik borç (technical debt) arasındaki doğru dengeyi nasıl bulurlar?

Küçük ve basit projelerde mimari üzerine en başta yapılacak hiçbir çalışma haklı gösterilemez. Hızla yön değiştirmek ve yeniden düzenleme (refactoring) yapmak kolay ve nispeten ucuzdur. Gereksinimler hakkında belirli bir anlayışın olduğu projelerde, birkaç ADD yinelemesi ile işe başlamalısınız. Bu tasarım yinelemeleri, başlıca mimari örüntülerin (architectural pattern), uygun olduğu durumlarda bir başvuru mimarisinin (reference architecture) ve çatıların (framework) seçimine odaklanabilir. Bu, Şekil 9.3c’de gösterilen 0. yineleme (iteration 0) yaklaşımıdır. Bu yaklaşım, projeyi yapılandırmaya, iş atamalarını ve ekip oluşumunu tanımlamaya ve en kritik kalite niteliklerini (quality attribute) ele almaya yardımcı olacaktır. Gereksinimler değiştiğinde —özellikle de bunlar kalite niteliği gereksinimlerini yönlendiriyorsa— yeni gereksinimleri ele almak için “spike”ların kullanıldığı Çevik deneyleme (Agile experimentation) pratiğini benimseyin. Bir spike, teknik bir soruyu yanıtlamak veya bilgi toplamak amacıyla oluşturulan, zaman kutulu (time-boxed) bir görevdir; bitmiş bir ürün ortaya çıkarması amaçlanmaz. Spike’lar ayrı bir dalda geliştirilir ve başarılı olurlarsa ana kod dalına birleştirilir. Bu yolla, ortaya çıkan gereksinimler memnuniyetle karşılanıp yönetilebilir; aynı zamanda genel geliştirme sürecini aşırı derecede kesintiye uğratmamış olursunuz.

Bununla birlikte, çevik mimari uygulamalar, karmaşıklığın bir kısmını dizginlemeye yardımcı olur; belirsizlik konisini (cone of uncertainty) daraltır ve böylece proje riskini azaltır. Bir başvuru mimarisi (reference architecture), teknoloji bileşen ailelerini ve bunların ilişkilerini tanımlar. Entegrasyonu yönlendirir ve mimariye nerede soyutlama katmanları inşa edilmesi gerektiğini gösterir; böylece, bir aile içinden yeni bir teknoloji, mevcut olanın yerini aldığında gereken yeniden çalışmayı azaltmaya yardım eder. Çevik spike’lar, prototiplerin hızlı biçimde inşa edilmesini ve “hızlı başarısız” (fail fast) olmalarını sağlayarak, ana geliştirme dalına dahil edilecek teknolojilerin nihai seçiminde yol gösterir.

### 9.1.2.2 Rational Unified Process

Rational Birleştirilmiş Süreç (Rational Unified Process, RUP), mimariye güçlü vurgu yapan bir yazılım geliştirme süreç çerçevesidir (process framework). RUP’ta (Bölüm 7.3’te de tartıştığımız) geliştirme projeleri, art arda gerçekleştirilen dört ana faza bölünür; bu fazların her birinin içinde bir dizi yineleme (iteration) yapılır. RUP’un dört fazı şunlardır:

- **Inception (Başlangıç).** İlk fazda amaç, proje paydaşları (stakeholder) arasında uzlaşma sağlamaktır. Bu faz sırasında projenin kapsamı ve bir iş mimarisi (business architecture) tanımlanır. Ayrıca bir aday mimari (candidate architecture) oluşturulur. Bu faz, daha önce tartıştığımız satış öncesi (pre-sales) fazına denktir.
- **Elaboration (Ayrıntılandırma).** İkinci fazda amaç, sistemin mimarisini temel seviye olarak sabitlemek (baseline etmek) ve mimari prototipler üretmektir.
- **Construction (İnşa).** Üçüncü fazda amaç, bir önceki fazda tanımlanan mimariden yola çıkarak sistemi artımlı (incremental) biçimde geliştirmektir.
- **Transition (Geçiş).** Dördüncü fazda amaç, sistemin teslimata hazır olduğundan emin olmaktır. Sistem, geliştirme ortamından nihai işletim ortamına aktarılır (transition).

Elaboration fazından projenin sonuna kadar RUP’un, önceki bölümlerde anlatılan iterasyon 0 yaklaşımını doğası gereği izlediği öne sürülebilir. RUP, mimari tasarıma ilişkin bir miktar rehberlik de sağlar; ancak bu rehberlik, nitelik temelli tasarım (Attribute-Driven Design, ADD)’ın sunduğuna göre çok daha az ayrıntılıdır. Bunun bir sonucu olarak, RUP’u tamamlayıcı olarak ADD kullanılabilir. Inception sırasında, Bölüm 9.1.1’de açıklanan yaklaşım izlenerek aday mimariyi oluşturmak için ADD iterasyonları gerçekleştirilebilir. Ayrıca elaboration fazı boyunca, başlangıç mimarisi, ilave tasarım iterasyonları gerçekleştirmek için başlangıç noktası olarak alınır ve temel alınabilecek (baseline edilebilecek) bir mimari ortaya çıkana kadar bu iterasyonlar sürdürülür. Construction sırasında ise, geliştirme iterasyonlarının bir parçası olarak ek ADD iterasyonları yapılabilir.

### 9.1.2.3 Takım Yazılım Süreci

Takım Yazılım Süreci (Team Software Process, TSP), kalite ve ölçüme güçlü vurgu yapan bir geliştirme sürecidir. Bir TSP yazılım projesi, her biri bir açılış (launch) olarak adlandırılan bir planlama süreciyle başlayan ve kapanış (postmortem) süreciyle sona eren bir dizi geliştirme çevrimi (development cycle) üzerinden ilerler. Her geliştirme çevrimi içinde, farklı fazlara ait etkinlikler gerçekleştirilebilir. Bu fazlar şunları içerir: gereksinimler (requirements, REQ), yüksek seviyeli tasarım (high-level design, HLD), gerçekleştirim (implementation, IMPL) ve test (testing, TEST).

TSP’nin REQ fazı, eksiksiz bir sistem gereksinimleri belirtimi (system requirements specification, SRS) dokümanı üretmeye odaklanır. HLD fazının temel amacı, ürün gerçekleştirimini yönlendirecek yüksek seviyeli bir tasarım üretmektir. Bu yüksek seviyeli tasarım, sistemi oluşturan ve IMPL fazında Kişisel Yazılım Süreci (Personal Software Process, PSP) izlenerek bağımsız olarak tasarlanıp geliştirilecek bileşenleri (yani modülleri) tanımlamalıdır. Son olarak TEST fazı, entegrasyon ve sistem testlerini gerçekleştirmeye ve sistemin teslimatını hazırlamaya odaklanır. Belirli bir projenin yaşam döngüsü modeli (şelale, artımlı) her geliştirme çevriminde hangi fazların icra edildiğiyle tanımlanır: Yinelemeli (iterative) bir proje, tipik olarak tek bir geliştirme çevrimi içinde dört fazın tümüne ait etkinlikleri kapsar.

TSP, yazılım mimarisi geliştirilmesini tam olarak dikkate almaz. Örneğin, TSP’de tanımlanan rollerden hiçbiri yazılım mimarı rolü değildir. REQ fazında kalite niteliklerine (quality attribute) de vurgu yapılmaz. Ayrıca, HLD fazına ilişkin süreç betiği (process script) (bkz. Tablo 9.1), sistem mimarisinin nasıl tasarlanacağı konusunda ayrıntılı bir kılavuz sunmaz. Bu sorunlar, TSP’ye ADD ve diğer mimari uygulamaların dahil edilmesiyle giderilebilir.

ADD, TSP bağlamında doğrudan bir şekilde kullanılabilir. HLD betiğinin birinci adımında, satış öncesi süreç için tartıştığımıza benzer biçimde, genel ürün tasarım kavramını üretmek için ADD kullanılabilir. Ayrıca her geliştirme çevriminde, HLD betiğinin 4. ve 5. adımlarında bir veya daha fazla ADD iterasyonu gerçekleştirilebilir. HLD fazı, mimari tasarım ile öğe etkileşimi tasarımı (element interaction design) arasında bir ayrım da gözetmelidir (Bölüm 2.2.2’de tartışılmıştı). Bir TSP geliştirme çevrimi, öğelerin ve arayüzlerinin tanımlanmasını içeren öğe etkileşimi tasarım aktivitelerini izleyen birkaç ADD iterasyonunu içerebilir. Bu arayüzler, daha sonra geliştirme fazında (IMPL) öğelerin ayrıntılı tasarımı ve geliştirilmesi için kullanılır.

> **💬 Çevirmen notu:** “Process script”, TSP’de belirli bir faz için adım adım yapılacak işleri tanımlayan süreç yönergesi/şablonu anlamında kullanılmaktadır; burada “süreç betiği” olarak çevrilmiştir.

#### Tablo 9.1 TSP Yüksek Seviyeli Tasarım (HLD) Betiği Adımlarının Özeti

| Adım | Etkinlikler                          | Özet                                                                                                                                      |
|------|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| 1    | Yapısal tasarım                      | Genel bir ürün tasarım kavramı üretilir. Bu, sistem mimari bileşenlerini ve ürün bileşenlerini, temel işlevleri ve arayüzleri içerir.     |
| 2    | Geliştirme stratejisi                | Bir geliştirme stratejisi oluşturulur. Strateji, bileşen geliştirme ve entegrasyon sırasını, yeniden kullanım ve test stratejilerini içerir. |
| 3    | Yüksek seviyeli tasarım stratejisi   | Bu adımda sistemin tek bir tasarım çevriminde mi yoksa birden fazla çevrimde mi tasarlanacağına (örneğin her seferinde bir katmana odaklanarak) karar verilir. |
| 4    | İlk çevrim tasarımı                  | Gereksinimler gözden geçirilir ve sınıf tanımları, ilişkiler ve geçiş diyagramları üretilir.                                             |
| 5    | Sonraki tasarım çevrimleri           | Önceki çevrimlerden gelen tasarım sorunları değerlendirilir ve mevcut tasarım gözden geçirilir. Ek sınıf tanımları, ilişkiler ve geçiş diyagramları üretilir. |
| 6    | Entegrasyon ve sistem test stratejileri | Test stratejileri belirlenir.                                                                                                             |
| 7    | Sistem tasarım belirtimi (system design specification, SDS) | Bir tasarım dokümanı üretilir.                                                                                                           |
| 8    | Tasarım üzerinden geçiş (design walkthrough) | Farklı paydaşlarla yüksek seviyeli tasarımın üzerinden geçilir.                                                                           |
| 9    | Tasarım incelemesi (design inspection) | Bu faz sonucunda üretilen materyaller incelenir.                                                                                         |
| 10   | SDS temel durum (baseline)           | Tasarım belirtimi bir temel duruma (baseline’e) alınır.                                                                                  |
| 11   | Kapanış değerlendirmesi (postmortem) | Fazın bir kapanış değerlendirmesi (postmortem) gerçekleştirilir.                                                                         |

### 9.1.2.4 DevOps

DevOps, çevik (Agile) zihniyetin doğal bir uzantısıdır. DevOps, yazılımın sürekli teslimini (continuous delivery) gerçekleştirmeye yardımcı olan bir dizi uygulamaya karşılık gelir. Bu tür uygulamalar, bir sisteme değişiklik yapılması ile bu değişikliğin normal üretim ortamına alınması arasındaki süreyi azaltmayı hedefler; bunu yaparken yüksek kaliteyi de güvence altına alır. Bu terim, “geliştirme” (development) ile “operasyonlar” (operations) arasındaki ayrımı özellikle bulanıklaştırır.

DevOps, doğası gereği mimari uygulamalara bağlı olmamakla birlikte, mimarlar sistemi tasarlarken, inşa ederken ve evrimleştirirken DevOps’u dikkate almazlarsa, sürekli derleme entegrasyonu (continuous build integration), otomatik test yürütümü (automated test execution), yüksek erişilebilirlik (high availability) ve ölçeklenebilir performans (scalable performance) gibi kritik aktiviteler daha zor ve daha az verimli hale gelir. DevOps’u benimseyerek, küçük iterasyonlar desteklenir ve teşvik edilir; böylece şu tür bir ortam yaratılır:

Çevik denemeler (agile spike) oluşturması, yaygınlaştırması (deploy) ve test edilmesi kolay çalışmalardır ve mimara kritik geri bildirim sağlar. Örneğin, sıkı sıkıya bağlı (tightly coupled) bir mimari, sürekli tümleştirme (continuous integration) için bir engel haline gelebilir çünkü küçük değişiklikler bile tüm sistemin yeniden derlenmesini gerektirebilir; bu da bir günde yapılabilecek derleme (build) sayısını sınırlar. Testlerin tam otomasyonu için, sistem kayıt alma, oynatma ve sistem durumunu kontrol etme gibi mimari (sistem çapında) test yetenekleri sağlamalıdır. Yüksek erişilebilirliği desteklemek için sistemin kendini izlemesi (self-monitoring) gerekir; bu da öz-test (self-test), ping/echo, kalp atışı (heartbeat), izleme (monitor), sıcak yedekler (hot spares) vb. mimari yetenekler gerektirir.

Büyük ölçekli sistemlerde, DevOps ancak mimari destekle gerçekleştirilebilir. Herhangi bir ad hoc ya da manuel süreç, böyle bir sistemin büyümesini ve başarısını riske atar. DevOps yaklaşımını benimsemek, mimarın bakış açısında küçük bir değişim gerektirir. Yalnızca sistemi tasarlamak yerine, artık tüm dağıtım hattının (deployment pipeline) tasarımını da düşünmek zorundasınız. Hat değiştirilebilir mi ve bu değişiklikler tek düğmeyle yaygınlaştırılabilir mi? Hat ölçeklendirmeye elverişli mi? Test edilmesi kolay mı? Neyse ki, bu soruların hepsine iyi yanıtlar vardır ve bunlar ayrı bir düşünce tarzı ya da strateji gerektirmez. ADD (Attribute-Driven Design, nitelik temelli tasarım), DevOps hedeflerine ulaşmak için bir sistemi tasarlamada, diğer herhangi bir sürücü (driver) için tasarımda olduğu gibi, tam olarak aynı yollarla ve tam olarak aynı tasarım ilkelini (design primitive) kullanarak yardımcı olabilir. DevOps’un başarıyla gerçekleştirilebilmesi için dikkate alınması gereken farklı yönler, sistem sürücülerinin bir parçası olarak, mimari kaygı (architectural concern) ya da kalite niteliği (quality attribute) şeklinde dahil edilebilir. Bir sistemde değiştirilebilirlik (modifiability) veya test edilebilirlik (testability) ya da ölçeklenebilirlik (scalability) ya da yüksek erişilebilirlik (high availability) elde etmemize yardımcı olan tasarım kavramları, dağıtım hattına da uygulanabilir. Gertrude Stein’i biraz yanlış alıntılayacak olursak: “Mimari mimaridir mimaridir (Architecture is architecture is architecture).”

## 9.2 Organizasyonel Yönler

Belirli bir geliştirme yönteminin seçimine ve bu yönteme ADD gibi bir tasarım yönteminin eklenmesine ek olarak, bir yazılım geliştirme organizasyonu tasarım etkinliklerini kolaylaştırmak üzere tasarım sürecinin diğer yönlerini de destekleyebilir. Burada bu yönlerden bazılarını kısaca tartışıyoruz.

### 9.2.1 Bireysel Olarak mı Yoksa Takım Olarak mı Tasarım Yapmak?

Büyük ve karmaşık projelerde, tasarımın gerçekleştirilmesinden bir mimari takımın sorumlu olması gerektiği apaçık görünür. Ancak daha küçük projelerde bile, tasarım sürecine birden fazla kişinin katılmasının önemli avantajlar sağladığını görebilirsiniz. Yalnızca tek bir kişinin mimar olacağına, diğerlerinin ise (eşli programlama (pair programming) uygulamasında olduğu gibi) gözlemci olacağına karar verebilirsiniz

veya grubun tasarım kararlarında etkin biçimde işbirliği yapmasına izin verebilirsiniz (yine de bu durumda bile bir baş mimar (lead architect) bulundurmanızı öneririz).

Bu yaklaşımın çeşitli faydaları vardır:

- İki (veya daha fazla) kafa, özellikle çözmeye çalıştığınız tasarım problemi daha önce ele aldıklarınızdan farklıysa, bir kafadan daha iyi olabilir.
- Farklı insanlar, mimarinin tasarımında yararlı olabilecek farklı uzmanlık alanlarına sahip olabilir. Örneğin, ayrı yazılım ve altyapı mimarlarına sahip olabilirsiniz ya da farklı alanlara (domain) veya farklı türde tasarım kavramlarına uzmanlaşmış kişileriniz olabilir.
- Tasarım kararları alınırken eşzamanlı olarak üzerinde düşünülür ve gözden geçirilir ve bunun bir sonucu olarak anında düzeltilebilir.
- Daha az deneyimli kişiler tasarım sürecine katılabilir; bu da mükemmel bir mentorluk pratiği olabilir.

Ancak bu yaklaşımda bazı güçlüklerin de farkında olmalısınız:

- Komiteyle tasarım (design by committee), makul bir sürede uzlaşma sağlanamazsa karmaşık hale gelebilir. Uzlaşı arayışı “analiz felci (analysis paralysis)”ne yol açabilir.
- Tasarımın maliyeti artar ve çoğu durumda tasarım için gereken süre de uzar.
- Lojistiğin yönetimi karmaşık olabilir, çünkü bu yaklaşım bir grup insanın düzenli olarak erişilebilir olmasını gerektirir.
- Kişilik ve politika çatışmalarıyla karşılaşabilirsiniz; bu, kırgınlık, incinmiş duygular veya tasarım kararlarının en uzun ve en yüksek sesle bağıran kişi tarafından güçlü biçimde etkilenmesi (“zorbalıkla tasarım (design by bullying)”) ile sonuçlanabilir.

> **💬 Çevirmen notu:** “Design by committee” ve “design by bullying” ifadeleri, tasarım kararlarının ya çok kalabalık ve verimsiz bir komite tarafından, ya da baskın bir kişi tarafından sağlıksız şekilde yönlendirilmesini ima eden yerleşik deyimlerdir.

### 9.2.2 Kuruluşunuzda Bir Tasarım Kavramları Kataloğu Kullanmak

Tasarım kavramları (design concept), sürücüleri (driver) tatmin etmek için tasarım sürecinde kullanılır (Bkz. Bölüm 2.5). Genel olarak sürücüler, yinelenen tasarım problemleri olarak görülebilir. Bir uygulamanın yapılandırılması, işlevselliğin tahsisi veya belirli bir kalite niteliğinin karşılanması gibi kaygılar söz konusu olduğunda, bu sürücüler büyük olasılıkla daha önce başka sistemlerde ele alınmıştır. Dahası, insanlar bu tasarım problemlerini ele almanın yollarını belgelemek veya bu amaçla hizmet eden bileşenler geliştirmek için zaman harcamışlardır. Bölüm 3.4’te gördüğümüz gibi, tasarım kavramlarının seçimi, tasarım sürecinin en zorlu yönlerinden biridir. Bilginin birçok yere dağılmış olması bu problemi daha da kötüleştirir: Mimarlar genellikle çeşitli desen (pattern) ve taktik (tactic) kataloglarına bakmak ve hangi tasarım kavramlarının dikkate alınabileceğini ve kullanılabileceğini bulmak için kapsamlı araştırma yapmak zorundadır.

Bu sorunu çözmenin olası yollarından biri, tasarım kavramları kataloglarının oluşturulmasıdır. Bu kataloglar, belirli uygulama alanları (application domain) için tasarım kavramı koleksiyonlarını bir araya getirir. Bu tür katalogların amacı, tasarım gerçekleştirilirken tasarım kavramlarının belirlenmesini ve seçimini kolaylaştırmaktır. Ayrıca, organizasyon genelinde tasarımların tutarlılığını artırmada da faydalıdırlar. Örneğin, tasarımcılardan mümkün olduğunca belirli bir katalogda yer alan teknolojileri kullanmaları istenebilir; bu da kestirim yapmayı kolaylaştırır, öğrenme eğrilerini kısaltır ve yeniden kullanım (reuse) fırsatlarına yol açabilir. Kataloglar eğitim amaçları için de yararlı olabilir.

Bir tasarım kavramları kataloğu örneği Ek A’da yer almaktadır. Bu katalog, kurumsal uygulamaların (enterprise application) tasarımına yöneliktir. Büyük Veri (Big Data) alanı için benzer bir katalog, Şekil 2.10’da (Bölüm 2.5.5) gösterilen teknoloji ailelerinden ve belirli teknolojilerden oluşturulabilir.

Bu katalogların oluşturulması hatırı sayılır bir çaba gerektirir ve bir kez oluşturulduğunda, organizasyona yeni tasarım kavramları ve özellikle yeni teknolojiler girdikçe ya da kullanımdan kaldırıldıkça katalogların bakımı yapılmalıdır. Ancak bu çaba buna değer; çünkü bu kataloglar değerli bir organizasyonel varlıktır.

## 9.3 Özet

Bu bölümde, ADD’nin (Attribute-Driven Design, ADD) çeşitli örgütsel yönlerle ilişkili olarak nasıl kullanılabileceğini tartıştık. ADD, bir proje daha satış öncesi teklif aşamasındayken, standart bileşenleri kullanarak kestirim (tahmin) yapmayı kolaylaştırmak için kullanılabilir.
Proje geliştikçe, ADD herhangi bir modern yazılım geliştirme yaşam döngüsü yöntemi ile birlikte kullanılabilir. Genel olarak ADD, mimari tasarımın nasıl yapılacağına dair ayrıntılı rehberlik sunmayan yaşam döngüsü yöntemlerine değerli bir tamamlayıcıdır.
Ayrıca tasarım ekibinin bileşimi ve tasarım süreci boyunca yararlı olan tasarım kavramları kataloğu gibi kurumsal varlıkların geliştirilmesi gibi ilgili bazı konuları da kısaca gözden geçirdik.

## 9.4 Ek Okumalar

Örgütsel yapı ve bunun yazılım mimarisi üzerindeki etkileri, kurumsal mimari yönetimi (enterprise architecture management) alanında ele alınmaktadır. Kurumsal mimari çerçeveleri (enterprise architecture frameworks), F. Ahlemann vd. (Ed.), *Strategic Enterprise Architecture Management: Challenges, Best Practices, and Future Developments*, Springer-Verlag Berlin Heidelberg, 2012’de tartışılmaktadır.
Mimari ile Çevik (Agile) yöntemler arasındaki ilişkiye bakan güzel bir makale derlemesi, Nisan 2010 tarihli *IEEE Software* dergisinin bu konuya ayrılmış özel sayısında bulunabilir.
Bir dizi çalışma, mimari ve çeviklik (agility) yöntemlerinin birbirlerini nasıl tamamladığına ve desteklediğine bakmıştır; örneğin S. Bellomo, I. Gorton ve R. Kazman, “Insights from 15 Years of ATAM Data: Towards Agile Architecture”, *IEEE Software*, Eylül/Ekim 2015; ve S. Bellomo, R. Nord ve I. Ozkaya, “A Study of Enabling Factors for Rapid Fielding: Combined Practices to Balance Speed and Stability”, *Proceedings of ICSE 2013*, 982–991, 2013.
Barry Boehm ve Richard Turner, çeviklik ile “disiplin” (yalnızca mimari değil) arasındaki ilişki konusuna ampirik bir bakış sunmuşlardır: *Balancing Agility and Discipline: A Guide for the Perplexed* (Boston: Addison-Wesley, 2004).
Çevik sprint’lerde belirsizliği gidermenin bir aracı olarak mimari “spike”ler oluşturma pratiği, T. C. N. Graham, R. Kazman ve C. Walmsley, “Agility and Experimentation: Practical Techniques for Resolving Architectural Tradeoffs”, *Proceedings of the 29th International Conference on Software Engineering (ICSE 29)*, (Minneapolis, MN), Mayıs 2007’de tartışılmaktadır. Spike’lere ilişkin genel bir tartışma https://www.scrumalliance.org/community/articles/2013/march/spikes-and-the-effort-to-grief-ratio adresinde bulunabilir.
Pek çok uygulayıcı ve araştırmacı, Çevik yöntemler ile mimari uygulamaların nasıl bir araya geldiği konusunda derinlemesine düşünmüştür. Bu düşüncenin en iyi örneklerinden bazıları şu kaynaklarda bulunabilir:
- S. Brown. *Software Architecture for the Developers*. LeanPub, 2013.
- J. Bloomberg. *The Agile Architecture Revolution*. Wiley CIO, 2013.
- Dean Leffingwell. “Scaled Agile Framework”. http://scaledagileframework.com/
- A. Cockburn. “Walking Skeleton”. http://alistair.cockburn.us/Walking+skeleton
- “Manifesto for Agile Software Development”. http://agilemanifesto.org/
- Scott Ambler ve Mark Lines. “Scaling Agile Software Development: Disciplined Agility at Scale”. http://disciplinedagileconsortium.org/Resources/Documents/ScalingAgileSoftwareDevelopment.pdf

Kestirim tekniklerine, standart bileşenler kullanılarak yapılan kestirim de dâhil olmak üzere, kapsamlı bir şekilde S. McConnell, *Software Estimation: Demystifying the Black Art*, Microsoft Press, 2006’da yer verilmektedir.
Takım Yazılım Süreci’ne (Team Software Process, TSP) genel bir bakış W. Humphrey, *The Team Software ProcessSM (TSPSM)*, Teknik Rapor CMU/SEI-2000-TR-023, Kasım 2000’de bulunabilir. TSP ile ilgili ayrıntılı bilgiler Humphrey’nin bu süreç hakkında yazdığı çeşitli kitaplarda bulunabilir.
ADD 2.0’ın (ve diğer mimari geliştirme yöntemlerinin) RUP (Rational Unified Process) ile entegrasyonu, R. Kazman, P. Kruchten, R. Nord ve J. Tomayko, “Integrating Software-Architecture-Centric Methods into the Rational Unified Process”, Teknik Rapor CMU/SEI-2004-TR-011, Temmuz 2004’te tartışılmaktadır.
DevOps konusunda, L. Bass, I. Weber ve L. Zhu, *DevOps: A Software Architect’s Perspective*, Addison-Wesley, 2015 gibi artık bir dizi iyi kitap bulunmaktadır. DevOps için bir mimari taktikler (architectural tactics) kümesi, H-M Chen, R. Kazman, S. Haziyev, V. Kropov ve D. Chtchourov, “Architectural Support for DevOps in a Neo-Metropolis BDaaS Platform”, *IEEE 34th Symposium on Reliable Distributed Systems Workshop (SRDSW)*, Montreal, Kanada, Eylül 2015’te tanımlanmıştır.
Mimari bilgi temsili ve yönetimi (architecture knowledge representation and management) problemine önemli ölçüde dikkat gösterilmiştir. Bu alana dair iyi bir genel bakış için P. Kruchten, P. Lago ve H. Van Vliet, “Building Up and Reasoning About Architectural Knowledge”, *Quality of Software Architectures*, Springer, 2006’ya bakınız. Mimari bilgi yönetimi araçlarına (architecture knowledge management tools) ilişkin bir bakış için ise A. Tang, P. Avgeriou, A. Jansen, R. Capilla ve M. Ali Babar, “A Comparative Study of Architecture Knowledge Management Tools”, *Journal of Systems and Software*, 83(3):352–370, 2010’a bakınız.

# 10 Son Sözler

Bu bölümde, tasarımın doğası ve tasarım için neden yöntemlere ihtiyaç duyduğumuz üzerine bir kez daha düşünüyoruz. Ne de olsa bu, kitabın temel noktasıdır! Ayrıca, bu kitabı okuyarak edindiğiniz bilgi ve becerilerle bundan sonra neler yapabileceğinize dair birkaç söz bırakıyoruz.

## 10.1 Yöntemlere Duyulan İhtiyaç Üzerine

Bu son bölüme kadar geldiğinize göre, profesyonel bir yazılım mimarı olmaya kararlı olduğunuzu varsayabiliriz. Profesyonel olmak, her tür bağlamda (en azından) yeterli ve tekrarlanabilir bir performans sergileyebilmek demektir. Bu performans düzeyine ulaşmak için yöntemlere ihtiyaç duyarsınız.
Hepimiz, yanlış yaptığımızda ciddi sonuçları olan karmaşık görevleri yerine getirirken yöntemlere ihtiyaç duyarız. Şunu düşünün: Jet pilotları ve cerrahlar, dünyadaki en çok eğitim almış profesyonel gruplardan ikisidir; yine de yaptıkları her önemli görev için kontrol listeleri ve standartlaştırılmış prosedürler kullanırlar. Neden? Çünkü hata yapmanın sonuçları ciddidir.
Muhtemelen yaşam ve ölüm sonuçları olan sistemlerin mimarisini tasarlamayacaksınız. Yine de özellikle büyük ve karmaşık olduklarında, tasarladığınız sistemler kurumunuzun sağlığı ve refahı üzerinde sonuçlara sahip olabilir. Eğer yalnızca atılıp atılacağı belli bir prototip ya da bir...

önemsiz bir sistem tasarlıyorsanız, belki açık bir mimari tasarım adımı atlanabilir. Geçmişte defalarca tasarladığınız bir sistemin n’inci varyantını tasarlıyorsanız, mimari tasarım önceki deneyimlerinizden kes-yapıştır olmaktan pek fazlası olmayabilir.

Ancak oluşturmak ya da evrimleştirmekle görevlendirildiğiniz sistem önemsiz değilse ve oluşturulmasıyla ilişkili bir risk varsa, yazılım geliştirme yaşam döngüsünün bu en kritik adımında elinizden gelenin en iyisini yapmak kendinize, kurumunuza ve mesleğinize karşı borcunuzdur. Bu hedefe ulaşmak için bir yönteme ihtiyacınız vardır. Yöntemler, yeknesaklığı, tutarlılığı ve tamlığı güvence altına almaya yardımcı olur. Yöntemler, doğru adımları atmanıza ve doğru soruları sormanıza yardım eder.

Elbette hiçbir yöntem, uygun eğitim ve öğrenimin yerini tutamaz. Kimse yalnızca bir yöntem veya kontrol listesiyle donanmış bir acemi pilota bir 787’nin kumandasını ya da ameliyathanede neşter tutan bir birinci sınıf tıp öğrencisine güvenmez. Ancak bir yöntem, yüksek kaliteli sonuçları tekrar tekrar üretmenin anahtarıdır. Ve nihayetinde, yazılım mühendisliği profesyonelleri olarak hepimizin arzuladığı şey budur.

Fred Brooks, tasarım süreci hakkında şunları söylemiştir:

> Tasarım sürecinin herhangi bir biçimde sistematikleştirilmesi, “Haydi kod yazmaya ya da inşa etmeye başlayalım” yaklaşımına kıyasla büyük bir ilerlemedir. Bu, bir tasarım projesinin planlanması için açık adımlar sağlar. Bir çizelgenin planlanması ve ilerlemenin yargılanması için açıkça tanımlanabilir dönüm noktaları sunar. Proje organizasyonunu ve personel tahsisini önerir. Tasarım ekibi içinde iletişime yardımcı olur, yapılan etkinlikler için herkese ortak bir sözlük sunar. Ekip ile yöneticisi ve yönetici ile diğer paydaşlar (stakeholder) arasındaki iletişimi son derece kolaylaştırır. Acemilere kolayca öğretilebilir. İlk tasarım görevleriyle yüz yüze gelen acemilere nereden başlayacaklarını söyler.

Tasarım rastlantıya bırakılamayacak kadar önemlidir. Ayrıca tasarımda ustalaşmanın, “Ayağına tekrar tekrar kurşun sıkmak”tan daha iyi bir yolu olmalıdır. Nobel Ödüllü bilim insanı Herbert Simon 1969’da şöyle yazmıştır: “Tasarım (design) … tüm mesleki eğitimin özüdür; meslekleri bilimlerden ayıran başlıca işarettir. Mühendislik okulları kadar mimarlık, işletme, eğitim, hukuk ve tıp okulları da tasarım süreciyle temelden ilgilidir.” Simon devamında, mesleki yetkinlik eksikliğinin, üniversitelerin müfredatlarında tasarıma görece az önem verilmesinden kaynaklandığını belirtir. Bu eğilim, memnuniyetle belirtmeliyiz ki, yavaş yavaş tersine dönmektedir; ancak yaklaşık 50 yıl sonra bile hâlâ kaygı nedeni olmaya devam etmektedir.

Bu kitapta size mimari tasarım (architectural design) yapmak için sahada sınanmış bir yöntem—ADD 3.0 (Attribute-Driven Design 3.0, nitelik temelli tasarım)—sunduk. Yöntemler, acemilere rehberlik sağladıkları ve uzmanlara güven verdikleri için kullanışlıdır. İyi bir yöntemde olduğu gibi, ADD 3.0’ın bir dizi adımı vardır ve bu adımlar, önceki ADD sürümlerine göre bir miktar güncellenmiştir. Ama en az bunun kadar önemli olan, daha geniş mimari yaşam döngüsüne odaklanmış olmamız ve tasarım sürecine yapılacak bazı değişikliklerin, mimar olarak yaşamınızı nasıl daha iyi hâle getirebileceğini ve size daha iyi çıktılar sağlayabileceğini göstermiş olmamızdır. Örneğin, düşünmeniz gereken girdi kümesini tasarım amacını (design purpose) ve mimari kaygıları (architectural concern) içerecek şekilde genişlettik. Bu daha geniş bakış açısı, yalnızca müşterinizin gereksinimlerini karşılayan değil, aynı zamanda ekibinizin ve kurumunuzun iş ihtiyaçlarıyla uyumlu bir mimari oluşturmanıza yardımcı olur. Ek olarak, tasarımın “tasarım kavramları katalogu (design concepts catalog)” tarafından yönlendirilmesi gerektiğini ve yönlendirilebileceğini gösterdik—başvuru mimarileri (reference architecture), desenler (pattern), taktikler (tactic) ve çerçeveler (framework) ile teknoloji aileleri gibi dışarıda geliştirilmiş bileşenlerden oluşan, yeniden kullanılabilir mimari bilgiden meydana gelen bir külliyat. Bu kavramlar kataloglandığında, tasarım daha öngörülebilir ve tekrarlanabilir hâle getirilebilir. Son olarak, tasarımın belgelenmesi gerektiğini—belki çizimler hâlinde gayriresmî olarak—ve alınan kararların tutarlı bir şekilde analiz edilmesi uygulamasının eşlik etmesi gerektiğini savunduk.

Kendimizi yazılım mühendisi (software engineer) olarak düşünüyorsak, “mühendis” unvanını ciddiye almamız gerekir. Hiçbir makine, elektrik ya da inşaat mühendisi, sağlam ilkelere ve bileşenlere dayanmayan veya analiz edilmemiş ve belgelenmemiş bir tasarıma önemli kaynaklar tahsis etmez. Yazılım mühendisliğinin genel olarak ve yazılım mimarisinin özel olarak benzer hedeflere ulaşmaya çalışması gerektiğini düşünüyoruz. Bizler yaratıcılığın her şeyden önemli olduğu “artist”ler değiliz; biz mühendissiz ve bu nedenle öngörülebilirlik ve tekrarlanabilirlik en çok değer verdiğimiz hedefler olmalıdır.

## 10.2 Sonraki Adımlar

Buradan nereye gitmelisiniz? Bu soruya dört yanıt görüyoruz. Birinci yanıt, bir birey olarak becerilerinizi ve bir mimar olarak deneyiminizi geliştirmek için neler yapabileceğinize odaklanır. İkinci yanıt, çalışma arkadaşlarınızı mimari tasarım hakkında daha bilinçli düşünmeye nasıl dahil edebileceğiniz etrafında döner. Üçüncü yanıt, kurumunuzun mimari tasarıma daha açık bir bağlılıkla nereye gidebileceğiyle ilgilidir. Dördüncü yanıt ise topluluğunuza ve daha geniş yazılım mimarları topluluğuna nasıl katkıda bulunabileceğinizle ilgilidir.

Birey olarak ilerlemeniz konusunda size verebileceğimiz tavsiye basittir: pratik yapın. Sahip olmaya değer diğer karmaşık beceriler gibi, bir mimar olarak yetkinliğiniz hemen oluşmayacaktır; ancak zamanla özgüveniniz istikrarlı bir biçimde artmalıdır. “Yapıyormuş gibi yap, yapana kadar (Fake it till you make it)” size verebileceğimiz en iyi tavsiyedir. Başvurabileceğiniz bir yönteme ve hazır bir ortak tasarım kavramları kaynağına sahip olmak, “yapıyormuş gibi” yaparken ve öğrenirken üzerine inşa edebileceğiniz sağlam bir temel sunar.

Becerilerinizi geliştirmenize ve çalışma arkadaşlarınızı sürece dahil etmenize yardımcı olmak için bir mimari oyunu geliştirdik. “Smart Decisions” (Akıllı Kararlar) adlı bu oyun http://www.smartdecisionsgame.com adresinde bulunabilir. Bu oyun, mimari tasarım sürecini ADD 3.0 kullanarak simüle eder ve bu yöntem hakkında eğlenceli, baskıdan uzak bir şekilde öğrenmeyi teşvik eder. Oyun, şu anda Bölüm 5’teki genişletilmiş tasarım örneğine benzer şekilde Büyük Veri Analitiği (Big Data Analytics) uygulama alanına odaklanmaktadır; ancak diğer uygulama alanlarına da kolayca uyarlanabilir.

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

Arızalı Davranışı
Yok Say
(Azaltım - Degradation)
Yeniden
Yapılandırma (Reconfiguration)

ŞEKİL A.12 Kullanılabilirlik taktikleri (availability tactics)

Hataları Önle (Prevent Faults)

Yeniden
Devreye Alma
(Reintroduction)

Gölge
(Shadow)

Hizmetten
Çıkarma
(Removal from
Service)

Durum
Yeniden
Eşzamanlama
(State
Resynchronization)

İşlemler
(Transactions)

Kademeli
Yeniden Başlatma
(Escalating
Restart)

Öngörücü
Model
(Predictive
Model)

Sürekli
İletim
(Non-Stop
Forwarding)

İstisna
Önleme
(Exception
Prevention)
Yeterlilik
Kümesini Artır
(Increase
Competence Set)

Hata
Maske
lendi
veya
Onarım
Yapıldı
(Fault
Masked
or
Repair
Made)

## A.4 Taktikler (Tactics)

### Hataları Tespit Et (Detect Faults)

- § Ping/echo: Düğümler arasında, ilişkilendirilmiş ağ yolundaki erişilebilirliği ve gidiş‑dönüş gecikmesini belirlemek için kullanılan, eşzamansız bir istek/yanıt mesaj çifti.
- § Monitor (izleyici): Sistem parçalarının sağlık durumunu izlemek için kullanılan bir bileşen. Bir sistem izleyicisi, ağda ya da hizmet reddi (denial-of-service) saldırısı gibi diğer paylaşılan kaynaklarda oluşan arıza veya tıkanıklığı tespit edebilir.
- § Heartbeat (kalp atışı): Bir sistem izleyicisi ile izlenen bir süreç arasında periyodik mesaj alışverişi gerçekleşmesi.
- § Timestamp (zaman damgası): Özellikle dağıtık mesaj geçişi (message-passing) sistemlerinde, olayların hatalı sıralarını tespit etmek.
- § Sanity checking (makullük denetimi): Bir bileşenin işlemlerinin veya çıktılarının geçerliliğini ya da makullüğünü denetlemek; tipik olarak iç tasarım bilgisine, sistemin durumuna veya incelenen bilginin doğasına dayanır.
- § Condition monitoring (koşul izleme): Bir süreçteki veya aygıttaki koşulları denetlemek ya da tasarım sırasında yapılmış varsayımları doğrulamak.
- § Voting (oylama): Kopyalanmış (replicated) bileşenlerin aynı sonuçları ürettiğini kontrol etmek. Çoğaltma (replication), işlevsel yedeklilik (functional redundancy), analitik yedeklilik (analytic redundancy) gibi çeşitli türleri vardır.
- § Exception detection (istisna tespiti): Sistem istisnası, parametre sınırları (parameter fence), parametre tip kontrolü (parameter typing) veya zaman aşımı (timeout) gibi normal yürütme akışını değiştiren bir sistem durumunu tespit etmek.
- § Self-test (öz test): Bir bileşenin kendi doğru çalışmasını test etmesine yönelik prosedür.

### Hatalardan Kurtul (Hazırlık ve Onarım)  
(Recover from Faults – Preparation and Repair)

- § Active redundancy (etkin yedeklilik, hot spare): Bir koruma grubundaki tüm düğümler, yedek düğüm ya da düğümlerin etkin düğüm(ler) ile eşzamanlı durumunu (synchronous state) korumasına izin verecek biçimde, aynı girdileri paralel olarak alır ve işler.
- § Passive redundancy (pasif yedeklilik, warm spare): Koruma grubunun yalnızca etkin üyeleri giriş trafiğini işler; görevlerinden biri de periyodik durum güncellemeleri ile yedek düğüm(ler)i beslemektir.
- § Spare (yedek, cold spare): Bir koruma grubunun yedek düğümleri, bir yana geçme (failover) gerçekleşene kadar hizmet dışı durumda kalır; bu noktada, yedek düğüm hizmete alınmadan önce bir “power-on-reset” prosedürü başlatılır.
- § Exception handling (istisna işleme): İstisnayı raporlayarak veya işleyerek onunla başa çıkmak; gerekirse istisnanın nedenini düzelterek ve tekrar deneyerek hatayı maskelemek.
- § Rollback (geri alma): “Rollback line” olarak adlandırılan, bilinen iyi bir önceki duruma geri dönmek.
- § Software upgrade (yazılım yükseltmesi): Hizmete etki etmeyecek bir şekilde, çalışmakta olan sistemde yürütülebilir kod imajlarının yükseltilmesini gerçekleştirmek.
- § Retry (yeniden deneme): Bir arıza geçiciyse (transient), işlemi yeniden denemek başarıya ulaşılmasını sağlayabilir.
- § Ignore faulty behavior (arızalı davranışı yok sayma): Mesajların sahte (spurious) olduğu belirlendiğinde, bu kaynaktan gönderilen mesajları yok saymak.
- § Degradation (azaltım/degradasyon): Bileşen arızalarının varlığında, daha az kritik işlevleri bırakıp en kritik sistem işlevlerini sürdürmek.
- § Reconfiguration (yeniden yapılandırma): Mümkün olduğunca çok işlevselliği koruyarak, sorumlulukları çalışmaya devam eden kaynaklara yeniden atamak.

### Hatalardan Kurtul (Yeniden Devreye Alma)  
(Recover from Faults – Reintroduction)

- § Shadow (gölge): Daha önce arızalanmış veya hizmet sırasında yükseltilmiş bir bileşeni, bileşeni tekrar etkin role döndürmeden önce tanımlanmış bir süre boyunca “gölge kipinde (shadow mode)” çalıştırmak.
- § State resynchronization (durum yeniden eşzamanlama): Pasif yedeklilik; bu, etkin yedekliliğin tamamlayıcı (partner) taktiği olup, durum bilgisinin etkin bileşenlerden yedek bileşenlere gönderilmesini içerir.
- § Escalating restart (kademeli yeniden başlatma): Yeniden başlatılan bileşen(ler)in incelik (granularity) düzeyini değiştirerek ve etkilenen hizmet seviyesini en aza indirerek hatalardan kurtulmak.
- § Non-stop forwarding (sürekli iletim): İşlevsellik, denetleyici (supervisory) ve veri (data) varyantlarına bölünür. Bir denetleyici (supervisor) arızalanırsa, yönlendirici (router), protokol bilgisinin kurtarılması ve doğrulanması sırasında, bilinen rotalar boyunca paketleri iletmeyi sürdürür.

### Hataları Önle (Prevent Faults)

- § Removal from service (hizmetten çıkarma): Potansiyel sistem arızalarını hafifletmek amacıyla, bir sistem bileşenini geçici olarak hizmet dışı duruma almak.
- § Transactions (işlemler): Dağıtık bileşenler arasında değiş tokuş edilen eşzamansız mesajların atomik, tutarlı (consistent), yalıtılmış (isolated) ve kalıcı (durable) olmasını sağlamak için durum güncellemelerini paketlemek.
- § Predictive model (öngörücü model): Bir sürecin sağlık durumunu izleyerek sistemin nominal parametreler içinde çalıştığından emin olmak; gelecekteki olası hataların habercisi olan koşullar tespit edildiğinde düzeltici işlem yapmak.
- § Exception prevention (istisna önleme): Bir hatayı maskeleyerek ya da akıllı işaretçiler (smart pointers), soyut veri tipleri (abstract data types) ve sarmalayıcılar (wrappers) kullanarak sistem istisnalarının oluşmasını engellemek.
- § Increase competence set (yeterlilik kümesini artırma): Bir bileşeni, normal çalışmasının bir parçası olarak daha fazla durumu—hatayı—ele alacak şekilde tasarlamak.

### A.4.2 Birlikte Çalışabilirlik Taktikleri (Interoperability Tactics)

Şekil A.13, birlikte çalışabilirliğe (interoperability) ulaşmak için kullanılan taktikleri özetler.

## A.4 Taktikler

Birlikte Çalışabilirlik Taktikleri (Interoperability Tactics)

Bilgi
Alışverişi
İsteği
(Information
Exchange
Request)

Konumlandır
(Locate)

Arayüzleri
Yönet
(Manage Interfaces)

Servisi
Keşfet
(Discover
Service)

Yönlendir/Orkestre Et
(Orchestrate)

İstek
Doğru
İşlenmiş
(Request
Correctly
Handled)

Arayüzü
Uyarlama
(Tailor Interface)

ŞEKİL A.13 Birlikte çalışabilirlik taktikleri (interoperability tactics)

### Konumlandır (Locate)

- § Discover service (servisi keşfet): Bilinen bir dizin servisi (directory service) içinde arama yaparak bir servisi bulmak. Bu konumlandırma sürecinde birden fazla dolaylılık (indirection) düzeyi olabilir; yani bilinen bir konum, başka bir konuma işaret edebilir ve bu ikinci konum da servis için aranabilir.

### Arayüzleri Yönet (Manage Interfaces)

- § Orchestrate (orkestrasyon): Servis çağrılarının sevkini (invocation) koordine etmek, yönetmek ve sıralamak için bir denetim mekanizması kullanmak. Orkestrasyon, sistemlerin karmaşık bir görevi yerine getirmek için karmaşık biçimde etkileşime girmesi gerektiğinde kullanılır.
- § Tailor interface (arayüzü uyarlama): Çeviri (translation), arabellekleme (buffering) veya veri yumuşatma (data smoothing) gibi yetenekleri bir arayüze eklemek ya da arayüzden çıkarmak.

### A.4.3 Değiştirilebilirlik Taktikleri (Modifiability Tactics)

Şekil A.14, değiştirilebilirliğe (modifiability) ulaşmak için kullanılan taktikleri özetler.

Değiştirilebilirlik Taktikleri (Modifiability Tactics)

Değişiklik
Gelir
(Change
Arrives)

Bir Modülün
Boyutunu Azalt
(Reduce Size
of a Module)

Bağlılığı
(Cohesion)
Artır
(Increase
Cohesion)

Bağımlılığı
(Coupling)
Azalt
(Reduce
Coupling)

Modülü
Böl
(Split Module)

Anlamsal
Tutarlılığı
Artır
(Increase
Semantic
Coherence)

Sarmala
(Encapsulate)

Bağlamayı
Eritele
(Defer
Binding)

Ara
Bileşen
Kullan
(Use an
Intermediary)

Değişiklik
Zaman ve
Bütçe İçinde
Yapılır
(Change Made
within Time
and Budget)

Bağımlılıkları
Kısıtla
(Restrict
Dependencies)

Yeniden
Yapılandır
(Refactor)

Ortak
Servisleri
Soyutla
(Abstract Common
Services)

ŞEKİL A.14 Değiştirilebilirlik taktikleri (modifiability tactics)

#### Bir Modülün Boyutunu Azalt (Reduce Size of a Module)

- § Split module (modülü böl): Değiştirilen modül çok fazla yetenek içeriyorsa, değişiklik maliyetleri muhtemelen yüksek olacaktır. Modülü birden çok daha küçük modüle ayrıştırmak, gelecekteki değişikliklerin ortalama maliyetini azaltmalıdır.

#### Bağlılığı Artır (Increase Cohesion)

- § Increase semantic coherence (anlamsal tutarlılığı artır): Bir modüldeki A ve B sorumlulukları aynı amaca hizmet etmiyorsa, bunlar farklı modüllerde yer almalıdır. Bu, yeni bir modül oluşturmayı ya da bir sorumluluğu mevcut bir modüle taşımayı gerektirebilir.

#### Bağımlılığı Azalt (Reduce Coupling)

§ Kapsülle: Kapsülleme, bir modüle açık (explicit) bir arayüz kazandırır. Bu arayüz, bir API’yi ve “bir girdi parametresi üzerinde sözdizimsel bir dönüşüm gerçekleştirip bunu dahili bir temsile dönüştürmek” gibi buna bağlı sorumlulukları içerir.
§ Aracı kullan (use an intermediary): Sorumluluk A ile sorumluluk B arasında bir bağımlılık olduğunda (örneğin A’nın gerçekleştirilebilmesi için önce B’nin gerçekleştirilmesi gerekiyorsa), bu bağımlılık bir aracı kullanılarak kırılabilir.

### A.4 Taktikler (tactics)

§ Bağımlılıkları kısıtla (restrict dependencies): Belirli bir modülün etkileşime girdiği ya da bağımlı olduğu modülleri kısıtla.
§ Yeniden düzenle (refactor): İki modül, en azından kısmen birbirinin kopyası olduğu için aynı değişiklikten etkileniyorsa yeniden düzenleme yapılır.
§ Ortak servisleri soyutla (abstract common services): İki modül tam olarak aynı olmasa da benzer servisler sağlıyorsa, bu servisleri daha genel (soyut) bir biçimde yalnızca bir kez gerçekleştirmek maliyet açısından daha etkin olabilir.

#### Geç Bağla (Defer Binding)

§ Geç bağla (defer binding): Kararların geliştirme zamanından sonra bağlanmasına (kesinleştirilmesine) izin ver.

### A.4.4 Performans Taktikleri (Performance Tactics)

Şekil A.15, performansa ulaşmak için kullanılan taktikleri özetlemektedir.

#### Performans Taktikleri

Events  
Arrive  

Kaynak Talebini Denetle (Control Resource Demand)  

Kaynakları Yönet (Manage Resources)  

Örnekleme oranını yönet (Manage sampling rate)  

Kaynakları artır (Increase resources)  

Olay tepkisini sınırla (Limit event response)  

Eşzamanlılık (concurrency) ekle (Introduce concurrency)  

Olaylara öncelik ver (Prioritize events)  

Hesaplamaların birden çok kopyasını tut (Maintain multiple  
copies of computations)  

Ek yükü azalt (Reduce overhead)  

Yürütme sürelerini sınırla (Bound execution times)  

Verinin birden çok kopyasını tut (Maintain multiple  
copies of data)  

Kaynak verimliliğini artır (Increase resource  
efficiency)  

Kuyruk boyutlarını sınırla (Bound queue sizes)  

Kaynakları zamanla (Schedule resources)  

Response  
Generated  
within  
Time  
Constraints  

ŞEKİL A.15 Performans taktikleri

---

#### Kaynak Talebini Denetle (Control Resource Demand)

§ Örnekleme oranını yönet (manage sampling rate): Bir veri akışının yakalandığı örnekleme frekansını düşürmek mümkünse, talep azaltılabilir; ancak bu genellikle belirli bir doğruluk (fidelity) kaybı pahasına olur.
§ Olay tepkisini sınırla (limit event response): Olayları yalnızca belirli bir azami hıza kadar işle; böylece olaylar gerçekten işlendiğinde daha öngörülebilir bir işlemeyi güvence altına al.
§ Olaylara öncelik ver (prioritize events): Tüm olaylar aynı derecede önemli değilse, olayların ne kadar önemli olduklarına göre sıralandığı bir öncelik şeması uygulayabilirsin.
§ Ek yükü azalt (reduce overhead): Aracıların (modifiye edilebilirlik için önemlidir) kullanımı, bir olay akışını işlerken tüketilen kaynakları artırır; bunları kaldırmak gecikmeyi (latency) iyileştirir.
§ Yürütme sürelerini sınırla (bound execution times): Bir olaya yanıt vermek için kullanılan yürütme süresine bir sınır koy.
§ Kaynak verimliliğini artır (increase resource efficiency): Kritik alanlarda kullanılan algoritmaların iyileştirilmesi gecikmeyi azaltacaktır.

#### Kaynakları Yönet (Manage Resources)

§ Kaynakları artır (increase resources): Daha hızlı işlemciler, ek işlemciler, ek bellek ve daha hızlı ağlar, gecikmeyi azaltma potansiyeline sahiptir.
§ Eşzamanlılığı artır (increase concurrency): İstekler paralel işlenebiliyorsa, bloklanmış zaman azaltılabilir. Eşzamanlılık, farklı olay akışlarını farklı iş parçacıklarında (thread) işleyerek veya farklı etkinlik kümelerini işlemek için ek iş parçacıkları oluşturarak sağlanabilir.
§ Hesaplamaların birden çok kopyasını tut (maintain multiple copies of computations): Replikaların amacı, tüm hesaplamaların tek bir sunucuda gerçekleşmesi durumunda ortaya çıkacak çekişmeyi (contention) azaltmaktır.
§ Verinin birden çok kopyasını tut (maintain multiple copies of data): Verinin kopyalarını (bunlardan biri diğerinin alt kümesi olabilir) farklı erişim hızlarına sahip depolama birimleri üzerinde tut.
§ Kuyruk boyutlarını sınırla (bound queue sizes): Kuyruğa alınmış gelişlerin (arrivals) azami sayısını ve buna bağlı olarak bu gelişleri işlemekte kullanılacak kaynakları denetle.
§ Kaynakları zamanla (schedule resources): Bir kaynak için çekişme olduğunda, bu kaynağın zamanlanması gerekir.

### A.4.5 Güvenlik Taktikleri (Security Tactics)

Şekil A.16, güvenliğe ulaşmak için kullanılan taktikleri özetlemektedir.

#### Güvenlik Taktikleri

Attack  

Saldırıları Tespit Et (Detect Attacks)  

Saldırılara Diren (Resist Attacks)  

Saldırılara  
Tepki Ver (React to  
Attacks)  

Saldırılardan  
Kurtul (Recover  
from Attacks)  

İzinsiz girişi tespit et (Detect  
Intrusion)  

Aktörleri tanımla (Identify  
Actors)  

Erişimi geri al (Revoke  
Access)  

Denetim izi tut (Maintain  
Audit Trail)  

Servis kesintisini tespit et (Detect Service  
Denial)  

Aktörleri kimlik doğrulamasından geçir (Authenticate  
Actors)  

Bilgisayarı kilitle (Lock  
Computer)  

Mesaj bütünlüğünü doğrula (Verify Message  
Integrity)  

Aktörleri yetkilendir (Authorize  
Actors)  

Aktörleri bilgilendir (Inform  
Actors)  

Mesaj gecikmesini tespit et (Detect Message  
Delay)  

Erişimi sınırla (Limit Access)  

Bkz.  
Kullanılabilirlik (See  
Availability)  

Sistem  
Tespit Eder,  
Direnir,  
Tepki Verir  
veya Kurtulur (System  
Detects,  
Resists,  
Reacts,  
or Recovers)  

Maruziyeti sınırla (Limit Exposure)  
Veriyi şifrele (Encrypt Data)  

Girdiyi doğrula (Validate Input)  
Varlıkları ayır (Separate  
Entities)  
Varsayılan ayarları değiştir (Change Default  
Settings)  

ŞEKİL A.16 Güvenlik taktikleri

---

#### Saldırıları Tespit Et (Detect Attacks)

§ İzinsiz girişi tespit et (detect intrusion): Bir sistem içindeki ağ trafiği ya da servis istek desenlerini, bir veritabanında saklanmış bir dizi imza ya da bilinen kötü niyetli davranış desenleriyle karşılaştır.
§ Servis kesintisini tespit et (detect service denial): Bir sisteme gelen ağ trafiğinin desenini ya da imzasını, bilinen servis reddi (denial-of-service, DoS) saldırılarının tarihsel profilleriyle karşılaştır.
§ Mesaj bütünlüğünü doğrula (verify message integrity): Mesajların, kaynak dosyalarının, dağıtım (deployment) dosyalarının ve yapılandırma dosyalarının bütünlüğünü doğrulamak için sağlama toplamı (checksum) ya da hash değeri gibi teknikler kullan.
§ Mesaj gecikmesini tespit et (detect message delay): Bir mesajın iletilmesinin ne kadar sürdüğünü kontrol ederek, şüpheli zamanlama davranışı tespit etmek mümkündür.

#### Saldırılara Diren (Resist Attacks)

§ Aktörleri tanımla (identify actors): Sisteme yapılan herhangi bir harici girdinin kaynağını belirle.
§ Aktörleri kimlik doğrulamasından geçir (authenticate actors): Bir aktörün (kullanıcı ya da uzak bir bilgisayar) gerçekten iddia ettiği kişi/varlık olduğundan emin ol.
§ Aktörleri yetkilendir (authorize actors): Kimliği doğrulanmış bir aktörün, veriye veya servislere erişme ve bunları değiştirme hakkına sahip olduğundan emin ol.
§ Erişimi sınırla (limit access): İşlemciler, bellek ve ağ bağlantıları gibi bir sistemin hangi kısımlarına kimlerin ve nelerin erişebileceğini denetle.
§ Maruziyeti sınırla (limit exposure): Örneğin bir sistemle ilgili gerçekleri gizleyerek (“security by obscurity”) ya da kritik kaynakları bölüp dağıtarak (“bütün yumurtalarını aynı sepete koyma”), başarılı bir saldırının olasılığını azalt veya potansiyel hasarın miktarını sınırla.
§ Veriyi şifrele (encrypt data): Veriye ve iletişime (communication) bir tür şifreleme uygula.
§ Girdiyi doğrula (validate input): Bir kullanıcıdan veya harici bir sistemden gelen girdiyi, sisteme kabul etmeden önce doğrula.
§ Varlıkları ayır (separate entities): Farklı ağlara bağlı farklı sunucular üzerinde fiziksel ayrım, sanal makineler veya “air gap” kullan.
§ Varsayılan ayarları değiştir (change default settings): Kullanıcıyı, varsayılan olarak atanmış ayarları değiştirmeye zorla.

#### Saldırılara Tepki Ver (React to Attacks)

§ Erişimi geri al (revoke access): Bir saldırıdan şüphelenildiğinde, normalde meşru kullanıcılar ve kullanım durumları için bile hassas kaynaklara erişimi sınırla.
§ Bilgisayarı kilitle (lock computer): Bir kaynağa erişmek için tekrarlanan başarısız girişimler varsa, bu kaynağa erişimi sınırla.
§ Aktörleri bilgilendir (inform actors): Bir saldırıdan şüphelenildiğinde veya saldırı tespit edildiğinde, operatörleri, diğer personeli veya işbirliği yapan sistemleri bilgilendir.

#### Saldırılardan Kurtul (Recover from Attacks)

Başarısız olan kaynakların kurtarılması için kullanılabilirlik taktiklerine ek olarak, saldırılardan kurtulmak için bir denetim (audit) gerçekleştirilebilir.

§ Denetim izi tut (maintain audit trail): Bir saldırganın eylemlerinin izini sürmeye ve onu tanımlamaya yardımcı olmak için, kullanıcı ve sistem eylemlerinin ve bunların etkilerinin kaydını tut.

### A.4.6 Test Edilebilirlik Taktikleri (Testability Tactics)

Şekil A.17, test edilebilirliğe ulaşmak için kullanılan taktikleri özetlemektedir.

#### Test Edilebilirlik Taktikleri

Sistem Durumunu Denetle ve Gözle (Control and Observe  
System State)  

Tests  
Executed  

Karmaşıklığı sınırla (Limit Complexity)  

Özel amaçlı  
arayüzler (Specialized  
Interfaces)  

Yapısal karmaşıklığı sınırla (Limit Structural  
Complexity)  

Kayıt/geri oynatma (Record/  
Playback)  

Belirsizliği (nondeterminism) sınırla (Limit  
Nondeterminism)  

Faults  
Detected  

Durum saklamayı yerelleştir (Localize State  
Storage)  
Veri kaynaklarını soyutla (Abstract Data  
Sources)  
Korumalı alan (sandbox) (Sandbox)  
Çalıştırılabilir savlar (executable assertions) (Executable  
Assertions)  

ŞEKİL A.17 Test edilebilirlik taktikleri

---

#### Sistem Durumunu Denetle ve Gözle (Control and Observe System State)

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

Hibernate, nesnelerin ilişkisel bir veritabanında kolayca kalıcı hale getirilmesini sağlar (ve farklı veritabanı (database) motorlarını destekler). Nesne–ilişkisel eşleme (object-relational mapping) kuralları, hibernate.cfg adlı bir XML dosyasında bildirime dayalı (declarative) olarak ya da kalıcı hale getirilmesi gereken sınıfların içinde yer alan notasyonlar (annotation) kullanılarak tanımlanır.

Hibernate, işlemleri (transaction) destekler ve veritabanından nesneleri almak için kullanılan HQL (Hibernate Query Language) adlı bir sorgu dili sağlar. Hibernate, performansı artırmak için çok seviyeli önbellekleme (multilevel caching) şemalarından yararlanır. Ayrıca, performansı artırmak ve kaynak tüketimini azaltmak için bağımlı nesnelerin tembel edinimini (lazy acquisition) sağlayan mekanizmalar sunar. Bu mekanizmalar yapılandırma (configuration) dosyalarında bildirime dayalı olarak (declarative) yapılandırılır.

### Yapı

Bu diyagram, yapılandırma dosyasındaki bilgileri kullanarak Hibernate çalışma zamanı (runtime) tarafından bir veritabanına kalıcı hale getirilen (persisted) bir varlığı (entity) göstermektedir (Anahtar: UML).

### Uygulanan tasarım desenleri (design pattern) ve taktikler (tactic)

**Desenler (Patterns):**

- Data Mapper
- Resource Cache
- Lazy Acquisition

**Taktikler (Tactics):**

- Uygunluk (availability): İşlemler (Transactions)
- Performans (performance): Verinin birden çok kopyasını tutma (önbellek, cache)

---

### A.6

| Framework Adı | Özet | Sayfa |
|--------------|------|-------|
| Hibernate    |      | 245   |

#### Yararlar (Benefits)

- Nesnelerin ilişkisel veritabanında kalıcı hale getirilmesini büyük ölçüde basitleştirir.

#### Sınırlamalar (Limitations)

- Karmaşık API
- JDBC (Java Database Connectivity)’den daha yavaş
- Eski (legacy) veritabanı şemalarına eşlemek güçtür.

---

### A.5.4 Java Web Start Framework

| Framework Adı | Java Web Start Framework |
|---------------|--------------------------|
| Teknoloji ailesi | Dağıtım mekanizması (deployment mechanism) |
| Dil | Java |
| URL | http://docs.oracle.com/javase/tutorial/deployment/webstart/ |

**Amaç (Purpose)**

Platformdan bağımsız, güvenli ve sağlam bir dağıtım teknolojisi sağlamak.

**Genel Bakış (Overview)**

Bir web tarayıcısı kullanarak son kullanıcılar standart (applet olmayan) Java uygulamalarını başlatabilir ve Java Web Start, bu uygulamaların en son sürümünün çalıştırıldığından emin olur. Bir uygulamayı başlatmak için kullanıcılar sayfadaki bir bağlantıya tıklar. Eğer uygulama ilk kez kullanılıyorsa, Java Web Start uygulamayı indirir. Uygulama daha önce kullanılmışsa, Java Web Start yerel kopyanın en güncel sürüm olup olmadığını doğrular ve onu başlatır ya da en yeni sürümü indirir.

### Yapı

Mevcut değil.

### Uygulanan tasarım desenleri (design pattern) ve taktikler (tactic)

- **Taktikler (Tactics):**
  - Güvenlik (security): Erişimi kısıtlama (limit access, sandbox)
  - Performans (performance): Verinin birden çok kopyasını tutma (önbellek, cache)

### Yararlar (Benefits)

- Uygulamalar bir korumalı alan (sandbox) içinde çalışır; ancak yerel dosyaları okuyup yazabilir.
- Uygulama önbelleğe alındığı için, bir kez indirildikten sonra başlangıç süresi büyük ölçüde kısalır.

### Sınırlamalar (Limitations)

- İlk başlatma biraz zaman alabilir.

---

### Özet (Summary)

Bu ekte, kurumsal uygulamalar (enterprise applications) uygulama alanı için bir tasarım kavramları kataloğu sunduk. Bu tür kataloglar, kurum düzeyinde faydalı varlıklar haline gelebilir ve 5. Bölüm’de kullandığımız Büyük Veri (Big Data) ya da mobil geliştirme gibi diğer uygulama alanları için de katalogların kolaylıkla hayal edilebileceğini söyleyebiliriz.

Burada sunulan katalog, 4. Bölüm’deki örnek olay incelemesinde (case study) kullanılan tasarım kavramlarını içerdiği için tükenmiş (exhaustive) olmak üzere tasarlanmamıştır. Gerçek bir katalog ise, daha fazla sayıda tasarım kavramı ve daha ayrıntılı açıklamalar içerir ve bir yazılım geliştirme organizasyonu için değerli bir varlık olurdu.

---

### A.7 Daha Fazla Okuma (Further Reading)

Referans mimariler (reference architecture) ve dağıtım desenleri (deployment pattern), Microsoft, *Application Architecture Guide* (2. baskı), Ekim 2009’dan alınmıştır.  
Taktikler kataloğu (tactics catalog) esas olarak L. Bass, P. Clements ve R. Kazman’ın *Software Architecture in Practice* (3. baskı), 2012 eserine dayanmaktadır. Bu taktiklerin bazıları daha önce şu kaynaklarda tanımlanmıştır: F. Bachmann, L. Bass ve R. Nord, “Modifiability Tactics”, SEI/CMU Technical Report CMU/SEI-2007-TR-002, 2007 ve J. Scott ve R. Kazman, “Realizing and Refining Architectural Tactics: Availability”, CMU/SEI-2009-TR-006, 2009.

Mimari desenler (architectural pattern), R. Buschmann, K. Henney ve D. Schmidt, *Pattern-Oriented Software Architecture, Volume 4*, Wiley, 2007’den alınmıştır.  
Spring framework’ü C. Walls, *Spring in Action* (4. baskı), Manning Publications, 2014’te ele alınmaktadır.  
Swing framework’ü J. Elliot, R. Eckstein, D. Wood ve B. Cole, *Java Swing* (2. baskı), O’Reilly Media, 2002’de ele alınmaktadır.  
Hibernate framework’ü ise C. Bauer ve G. King, *Java Persistence with Hibernate*, Manning Publications, 2015’te ele alınmaktadır.

---

# B Taktik Tabanlı (tactics-based) Anketler (Questionnaire)

Bu ekte, en önemli yedi kalite niteliği (quality attribute) için taktik tabanlı anketler sunuyoruz: uygunluk (availability), birlikte çalışabilirlik (interoperability), değiştirilebilirlik (modifiability), performans (performance), güvenlik (security), test edilebilirlik (testability) ve kullanılabilirlik (usability). Bu yedinin en önemlileri olduğunu nereden biliyoruz? Bu karar, SEI ATAM (Architecture Tradeoff Analysis Method) verilerinde, 15 yılı aşkın bir süre boyunca paydaşlardan (stakeholder) toplanan kalite niteliklerinin analizine dayanılarak verilmiştir.

Bu “ilk yedi”ye ek olarak, DevOps için de bir taktik tabanlı anket sunuyoruz; bu anket, kullanımınızı kendinize göre uyarlamanın ne kadar kolay olduğunu göstermek için değiştirilebilirlik, uygunluk, performans ve test edilebilirlikten gelen taktiklerin bir birleşimidir.

> **💬 Çevirmen notu:** ATAM, mimari kararların kalite nitelikleri üzerindeki etkisini inceleyen, SEI tarafından geliştirilmiş yapılandırılmış bir değerlendirme yöntemidir.

---

## B.1 Anketlerin Kullanılması

Bu anketler, her bir soruyu sırasıyla mimara yönelten ve yanıtları kaydeden bir analist tarafından, hafif (lightweight) bir mimari gözden geçirme (architecture review) aracı olarak kullanılabilir. Alternatif olarak, anketler, mimarinizi kendi başınıza incelemek için kullanabileceğiniz yansıtıcı (reflective) sorular kümesi olarak da kullanılabilir. Her iki durumda da, bu anketleri kullanmak için şu dört adımı izleyin:

1. Her taktik sorusu için, “Supported (Destekleniyor)” sütununu, taktik mimaride destekleniyorsa **Y**, aksi takdirde **N** ile doldurun. “Tactics Question (Taktik Sorusu)” sütunundaki taktik adı kalın (bold) olarak gösterilir.
2. “Supported” sütunundaki yanıt **Y** ise, “Design Decisions and Location (Tasarım Kararları ve Konumu)” sütununda, taktiği desteklemek için alınan belirli tasarım kararlarını açıklayın ve bu kararların mimaride nerede (hangi yerde) ortaya çıktığını (konumlandığını) belirtin. Örneğin, bu taktiği hangi kod modüllerinin, framework’lerin ya da paketlerin gerçekleştirdiğini (implement) belirtin.
3. “Risk” sütununda, taktiğin uygulanmasındaki beklenen/deneyimlenen zorluk ya da riski, (H = yüksek, M = orta, L = düşük) ölçeğini kullanarak belirtin. Örneğin, uygulanması orta zorlukta veya riskte olan (ya da henüz uygulanmadıysa orta zorlukta olacağı öngörülen) bir taktik M ile etiketlenir.
4. “Rationale (Gerekçe)” sütununda, alınan tasarım kararlarına ilişkin gerekçeyi (bu taktiği kullanmama kararı dahil) açıklayın. Bu kararın sonuçlarını kısaca açıklayın. Örneğin, kararın gerekçesini ve sonuçlarını maliyet, zaman çizelgesi (schedule), evrim (evolution) vb. üzerindeki etkileri açısından açıklayabilirsiniz.

---

## B.2 Uygunluk (Availability)

| # | Taktik Grubu (Tactics Group) | Taktik Sorusu (Tactics Question) |
|---|------------------------------|----------------------------------|
| 1 | Hata tespiti (Detect faults) | Sistem, bir bileşenin ya da bağlantının hatasını veya ağ tıkanıklığını (network congestion) tespit etmek için ping/echo kullanıyor mu? |
| 2 |                              |                                  |

## B.2 Kullanılabilirlik (Availability)

### Hataları Tespit Et (detect faults)

**Taktik Soru 2**

Sistem, sistemin diğer parçalarının sağlık durumunu izlemek için bir bileşen kullanıyor mu?  
Bir sistem monitörü (system monitor), ağda veya hizmet reddi (denial-of-service) saldırısı gibi diğer paylaşılan kaynaklarda meydana gelen arıza veya tıkanıklığı tespit edebilir.

**Taktik Soru 3**

Sistem, bir bileşenin ya da bağlantının arızasını veya ağ tıkanıklığını tespit etmek için kalp atışı (heartbeat) kullanıyor mu — yani bir sistem monitörü ile bir süreç arasında periyodik ileti alışverişi?

**Taktik Soru 4**

Sistem, dağıtık sistemlerdeki yanlış olay sıralarını tespit etmek için zaman damgası (time stamp) kullanıyor mu (Bölüm A.4.1’deki gibi)?

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

**Taktik Soru 5**

Sistem herhangi bir akıl sağlığı kontrolü (sanity checking) yapıyor mu: Bir bileşenin işlemlerinin veya çıktılarının geçerliliğini ya da makullüğünü denetlemek gibi?

**Taktik Soru 6**

Sistem, bir süreçte veya aygıtta koşul izleme (condition monitoring) yapıyor mu, ya da tasarım sırasında yapılmış varsayımları doğruluyor mu?

**Taktik Soru 7**

Sistem, çoğaltılmış bileşenlerin aynı sonuçları ürettiğini kontrol etmek için oylama (voting) kullanıyor mu? Çoğaltılmış bileşenler özdeş kopyalar, işlevsel olarak yedek (functionally redundant) veya analitik olarak yedek (analytically redundant) olabilir.

**Taktik Soru 8**

Sistem, normal yürütme akışını değiştiren bir sistem durumunu tespit etmek için istisna tespiti (exception detection) kullanıyor mu (örneğin sistem istisnası, parametre sınırı, parametre tür denetimi, zaman aşımı)?

**Taktik Soru 9**

Sistem, kendi doğru çalışmasını test etmek için öz test (self-test) yapabiliyor mu?

---

### Hatalardan Kurtul (Recover from faults)  
*(hazırlık ve onarım — preparation and repair)*

Kullanılabilirlik

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

**Taktik Soru 10**

Sistem, etkin yedeklilik (active redundancy, hot spare) kullanıyor mu?  
Etkin yedeklilikte, koruma grubundaki (protection group — bir veya daha fazla düğümün “aktif” olduğu, geri kalanların yedek parça (spare) olarak hizmet verdiği düğüm grubu) tüm düğümler, aynı girdileri paralel olarak alır ve işler; bu da yedek parçaların aktif düğüm(ler) ile eşzamanlı durum (synchronous state) tutmasını sağlar.

**Taktik Soru 11**

Sistem, pasif yedeklilik (passive redundancy, warm spare) kullanıyor mu?  
Pasif yedeklilikte, koruma grubunun yalnızca aktif üyeleri girdi trafiğini işler; görevlerinden biri de yedek parçalara periyodik durum güncellemeleri sağlamaktır.

---

### Ekler B — Taktik Temelli Anketler

**Taktik Soru 12**

Sistem, yedek parçalar (spares, cold spares) kullanıyor mu?  
Burada, bir koruma grubunun yedek parçaları, bir devretme (failover) gerçekleşene kadar hizmet dışı durumda kalır; bu noktada, yedek parçanın hizmete alınmasından önce, üzerinde bir açılış-sıfırlama (power-on-reset) prosedürü başlatılır.

**Taktik Soru 13**

Sistem, hatalarla başa çıkmak için istisna işleme (exception handling) kullanıyor mu? Tipik olarak, işleme ya hatanın raporlanmasını ya da ele alınmasını içerir; bu, istisnanın nedenini düzelterek ve yeniden deneyerek hatayı maskeleyebilmeyi de içerebilir.

**Taktik Soru 14**

Sistem, bir hata durumunda daha önce kaydedilmiş iyi bir duruma (geri alma çizgisi — “rollback line”) dönebilmesini sağlamak için geri alma (rollback) kullanıyor mu?

**Taktik Soru 15**

Sistem, yürütülebilir kod imajlarına hizmet kesintisine yol açmadan (non-service-affecting manner) hizmet içi yazılım güncellemesi (in-service software upgrade) gerçekleştirebiliyor mu?

**Taktik Soru 16**

Sistem, bileşen veya bağlantı arızasının geçici olabileceği durumlarda sistematik olarak yeniden deneme (retry) yapıyor mu?

**Taktik Soru 17**

Sistem, hatalı davranışı basitçe yok sayabiliyor mu (örneğin, bir kaynaktan gelen mesajların asılsız/sahte (spurious) olduğu belirlendiğinde bu mesajları yok saymak)?

**Taktik Soru 18**

Sistem, kaynaklar tehlikeye girdiğinde bir bozunma (degradation) politikası uyguluyor mu; bileşen arızaları varlığında en kritik sistem işlevlerini sürdürüp, daha az kritik işlevleri bırakacak şekilde?

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

**Taktik Soru 19**

Sistem, arıza sonrasında yeniden yapılandırma (reconfiguration) için tutarlı politika ve mekanizmalara sahip mi; çalışır durumda kalan kaynaklara sorumlulukları yeniden atarken olabildiğince fazla işlevselliği koruyacak şekilde?

**Taktik Grubu: Hatalardan Kurtul (faults’tan kurtulma)**  
*(yeniden devreye alma — reintroduction)*

**Taktik Soru 20**

Sistem, daha önce arızalanmış veya hizmet içi güncellenmiş bir bileşeni, bileşeni yeniden aktif rolüne döndürmeden önce tanımlı bir süre için “gölge kip”te (shadow mode) çalıştırabiliyor mu?

**Taktik Soru 21**

Sistem etkin veya pasif yedeklilik kullanıyorsa, durum yeniden eşleme (state resynchronization) de kullanıyor mu; yani durum bilgisini aktif bileşenlerden yedek bileşenlere gönderiyor mu?

**Taktik Soru 22**

Sistem, artan yeniden başlatma (escalating restart) kullanıyor mu — yani yeniden başlatılan bileşen(ler)in inceliğini (granularity) değiştirerek ve etkilenen hizmet düzeyini en aza indirerek hatalardan kurtuluyor mu?

**Taktik Soru 23**

Sistemin mesaj işleme ve yönlendirme kısımları, işlevselliğin denetim (supervisory) ve veri düzlemlerine (data plane) bölündüğü kesintisiz iletim (nonstop forwarding, Bölüm A.4.1’deki gibi) kullanabiliyor mu? Bu durumda, bir denetleyici arızalanırsa, yönlendirici, protokol bilgisinin geri kazanılması ve doğrulanması sırasında bilinen rotalar boyunca paket iletimine devam eder.

**Taktik Soru 24**

Sistem, olası sistem arızalarını azaltmak amacıyla, bileşenleri hizmetten çekerek (service dışı duruma — out-of-service state — geçici olarak alarak) devre dışı bırakabiliyor mu?

Destekleniyor mu? (E/H)

Kullanılabilirlik

Hataları Önle (Prevent faults)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

### Ekler B — Taktik Temelli Anketler (devam)

**Taktik Soru 25**

Sistem, işlemler (transactions) kullanıyor mu — dağıtık bileşenler arasında değiş tokuş edilen eşzamansız mesajların atomik (atomic), tutarlı (consistent), yalıtılmış (isolated) ve kalıcı (durable) olmasını sağlayacak şekilde durum güncellemelerini paketleyerek?

**Taktik Soru 26**

Sistem, bir bileşenin sağlık durumunu izlemek ve sistemin nominal parametreler içinde çalıştığından emin olmak için bir kestirimsel model (predictive model) kullanıyor mu? Olası gelecekteki hatalara işaret eden koşullar tespit edildiğinde, model düzeltici eylemi başlatır.

**Taktik Soru 27**

Sistem, örneğin bir hatayı maskeleyerek, akıllı işaretçiler (smart pointers), soyut veri tipleri (abstract data types) veya sarmalayıcılar (wrappers) kullanarak istisnaların oluşmasını en baştan engelliyor mu?

**Taktik Soru 28**

Sistem, yetkinlik kümesini (competence set) artıracak şekilde tasarlandı mı; örneğin, bir bileşen normal çalışmasının bir parçası olarak daha fazla durumu — hata durumlarını da — ele alacak biçimde tasarlanarak?

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

## B.3 Birlikte Çalışabilirlik (Interoperability)

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

### Taktik Grubu: Konumlandır (Locate)

**Taktik Soru 1**

Sistemin hizmetleri keşfetmek için bir yolu var mı (tipik olarak bir dizin hizmeti — directory service — aracılığıyla)?

### Taktik Grubu: Arabirimleri Yönet (Manage interfaces)

**Taktik Soru 2**

Sistem, hizmetlerin etkinliklerini orkestre etmek için bir yola sahip mi? Yani, hizmet çağrılarını koordine eden, yöneten ve sıralayan bir denetim mekanizması var mı?

**Taktik Soru 3**

Sistem, arabirimleri uyarlamanın (tailor interfaces) bir yoluna sahip mi? Örneğin, bir arabirime çeviri, arabelleğe alma (buffering) veya veri yumuşatma (data smoothing) gibi kabiliyetler ekleyip çıkarabiliyor mu?

---

## B.4 Değiştirilebilirlik (Modifiability)

Destekleniyor mu? (E/H)

Risk

Tasarım Kararları ve Konumu

Gerekçe ve Varsayımlar

### Taktik Grubu: Bir modülün boyutunu azalt (Reduce size of a module)

**Taktik Soru 1**

Modülleri bölerek daha basit hale getiriyor musunuz? Örneğin, büyük ve karmaşık bir modülünüz varsa, bunu iki (veya daha fazla) daha küçük ve daha basit modüle bölebiliyor musunuz?

### Taktik Grubu: Bağlılığı artır (Increase cohesion)

Sistemde, anlamsal tutarlılığı (semantic coherence) artırmak tutarlı biçimde destekleniyor mu? Örneğin, bir modüldeki sorumluluklar aynı amaca hizmet etmiyorsa, bunların farklı modüllere yerleştirilmesi gerekir. Bu, yeni bir modül oluşturmayı veya bir sorumluluğu mevcut bir modüle taşımayı içerebilir.

3

Bağlılığı
(coupling)
azaltma

Sistem, işlevselliği tutarlı bir biçimde kapsülüyor mu (encapsulate)? Bu tipik olarak, incelenen işlevselliği yalıtmayı ve ona açık (explicit) bir arayüz tanıtmayı içerir.

Destekleniyor mu?
(E/H)

(devamı)

254

#

Ek B—Taktik Tabanlı Anketler

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| 4 | Sistem, modüllerin çok sıkı bir şekilde birbirine bağlanmasını engellemek için tutarlı biçimde bir aracı (intermediary) kullanıyor mu? Örneğin, A somut C işlevselliğini çağırıyorsa, A ile C arasında aracılık yapan soyut bir B tanıtabilirsiniz. |  |  |  |  |
| 5 | Modüller arasındaki bağımlılıkları sistematik bir şekilde kısıtlıyor musunuz? Yoksa herhangi bir sistem modülü, herhangi başka bir modülle serbestçe etkileşime girebiliyor mu? |  |  |  |  |
| 6 | İki veya daha fazla ilgisiz modül birlikte değiştiğinde—yani düzenli olarak aynı değişikliklerden etkilendiğinde—paylaşılan işlevselliği, ayrı bir modülde ortak kod olarak yalıtmak için düzenli olarak yeniden düzenleme (refactoring) yapıyor musunuz? |  |  |  |  |
| 7 | Birden fazla benzer hizmet sağladığınız durumlarda, sistem ortak hizmetleri soyutluyor mu (abstract)? Örneğin, bu teknik genellikle sisteminizi işletim sistemleri, donanımlar veya diğer ortam (environment) varyasyonları arasında taşınabilir kılmak istediğinizde kullanılır. |  |  |  |  |
| 8 | Bağlamayı (binding) erteleme | Sistem, önemli işlevselliğin bağlanmasını (binding) düzenli olarak erteliyor mu; böylece bu işlevsellik yaşam döngüsünde daha sonra, hatta belki de son kullanıcılar tarafından bile değiştirilebilir oluyor mu? Örneğin, sistemin işlevselliğini genişletmek için eklentiler (plug-ins), eklenti modülleri (add-ons) veya kullanıcı betikleme (user scripting) kullanıyor musunuz? |  |  |  |  |

B.5

B.5

#

1

257

Performans

Performans

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Kaynak talebini kontrol etme (control resource demand) | Girdileriniz sürekli bir veri akışıysa, sistem örnekleme oranını (sampling rate) yönetiyor mu? Yani, verileri farklı oranlarda örneklemek (ve buna bağlı doğruluk/sadakat değişiklikleriyle birlikte) mümkün mü? |  |  |  |  |
| 2 | Sistem, olay yanıtını (event response) izliyor ve sınırlandırıyor mu? Sistem, hizmet verilen olaylar için öngörülebilir yanıtlar sağlamak amacıyla, belirli bir zaman aralığında yanıt verdiği olay sayısını sınırlandırıyor mu? |  |  |  |  |
| 3 | Kullanılabilir kaynaklardan daha fazla hizmet isteğiniz olabileceği göz önüne alındığında, sistem olaylara öncelik veriyor mu? |  |  |  |  |
| 4 | Sistem, örneğin aracıları kaldırarak veya kaynakları birlikte konumlandırarak (co-locating) hizmet isteklerine yanıt verme ek yükünü (overhead) azaltıyor mu? |  |  |  |  |
| 5 | Sistem yürütme süresini (execution time) izleyip sınırlandırıyor mu? Daha genel olarak, hizmet isteklerine yanıt verirken harcanan herhangi bir kaynağın (ör. bellek, CPU, depolama, bant genişliği, bağlantılar, kilitler) miktarını sınırlandırıyor musunuz? |  |  |  |  |
| 6 | Kaynak verimliliğini artırıyor musunuz? Örneğin, gecikmeyi (latency) azaltmak ve iş hacmini (throughput) iyileştirmek için kritik alanlardaki algoritmaların verimliliğini düzenli olarak artırıyor musunuz? |  |  |  |  |

(devamı)

256

#

7

Ek B—Taktik Tabanlı Anketler

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Kaynakları yönetme (manage resources) | Sistem, kaynakları (ör. CPU, bellek, ağ bant genişliği) kesintisiz biçimde (seamlessly) artırabiliyor mu? |  |  |  |  |
| 8 | Sistem eşzamanlılık (concurrency) tanıtabiliyor mu? Örneğin, daha fazla hizmet isteğinin eşzamanlı olarak işlenebilmesi için paralel işlem akışlarının (parallel processing streams) kesintisiz eklenmesini destekliyor mu? |  |  |  |  |
| 9 | Sistem, sık erişilen veriler için çekişmeyi (contention) azaltmak amacıyla verilerin birden fazla kopyasını (ör. veritabanı çoğaltma veya önbellekler kullanarak) tutuyor mu? |  |  |  |  |
| 10 | Sistem, sık erişilen hesaplama kaynakları için çekişmeyi azaltmak amacıyla hesaplamaların birden fazla kopyasını (ör. bir sunucu çiftliğinde (server farm) sunucu havuzu tutarak) sürdürüyor mu? |  |  |  |  |
| 11 | Sistem kuyruk boyutlarını sınırlandırıyor mu? Yani, hizmet beklerken bir kuyruğa yerleştirilen olayların sayısını sınırlıyor musunuz? |  |  |  |  |
| 12 | Sistem kaynakları, özellikle de kıt (scarce) kaynakları, açık bir zamanlama (scheduling) politikasına göre tahsis edilebilmeleri için zamanlıyor mu (schedule)? |  |  |  |  |

B.6

B.6

#

1

Güvenlik

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Saldırıları tespit etme (detecting attacks) | Sistem, aktörlerin (actors) tanımlanmasını destekliyor mu? Örnek: Sisteme gelen herhangi bir dış girdinin kaynağını tanımlamak. |  |  |  |  |
| 2 | Sistem, aktörlerin kimlik doğrulamasını (authentication) destekliyor mu? Örnek: Bir aktörün (bir kullanıcı veya uzak bir bilgisayar) gerçekten iddia ettiği kişi veya varlık olduğunu güvence altına almak. |  |  |  |  |
| 3 | Sistem, mesaj bütünlüğünün (message integrity) doğrulanmasını destekliyor mu? Örnek: Mesajların, kaynak dosyaların, dağıtım dosyalarının ve yapılandırma dosyalarının bütünlüğünü doğrulamak için sağlama toplamı (checksum) veya özet değerleri (hash values) gibi tekniklerin kullanılması. |  |  |  |  |
| 4 | Sistem, mesaj gecikmelerinin tespitini destekliyor mu? Örnek: Bir mesajın iletilmesinin ne kadar sürdüğünü kontrol etmek. |  |  |  |  |
| 5 | Sistem, saldırıların tespitini (intrusion detection) destekliyor mu? Örnek: Bir sistemdeki ağ trafiğini veya hizmet isteği kalıplarını, bir veritabanında saklanan imzalar ya da bilinen kötü niyetli davranış kalıplarıyla karşılaştırmak. |  |  |  |  |
| 6 | Sistem, hizmet reddi (denial-of-service) saldırılarının tespitini destekliyor mu? Örnek: Sisteme gelen ağ trafiğinin kalıbını veya imzasını, bilinen hizmet reddi saldırılarının tarihsel profilleriyle karşılaştırmak. |  |  |  |  |

(devamı)

258

#

Ek B—Taktik Tabanlı Anketler

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Saldırılara direnme (resisting attacks) | Sistem, aktörlerin yetkilendirilmesini (authorization) destekliyor mu? Örnek: Kimliği doğrulanmış bir aktörün veriye veya hizmetlere erişme ve bunları değiştirme hakkına sahip olduğundan emin olmak. |  |  |  |  |
| 8 | Sistem, erişimin sınırlandırılmasını (limiting access) destekliyor mu? Örnek: Bir sistemin hangi bölümlerine (işlemciler, bellek ve ağ bağlantıları gibi) kimlerin ve nelerin erişebileceğini kontrol etmek. |  |  |  |  |
| 9 | Sistem, maruziyetin sınırlandırılmasını (limiting exposure) destekliyor mu? Örnek: Bir sistemle ilgili gerçekleri gizleyerek (“security by obscurity”) veya kritik kaynakları bölüp dağıtarak (“tüm yumurtaları aynı sepete koyma” ilkesi) başarılı bir saldırı olasılığını azaltmak veya potansiyel zararın miktarını kısıtlamak. |  |  |  |  |
| 10 | Sistem, veri şifrelemeyi (data encryption) destekliyor mu? Örnek: Verilere ve iletişime bir tür şifreleme uygulamak. |  |  |  |  |
| 11 | Sistem girdiyi tutarlı, sistem çapında bir şekilde doğruluyor mu (input validation)? Örnek: Dış girdinin filtrelenmesi, kanonik hale getirilmesi (canonicalization) ve kaçış karakterleriyle işlenmesi (escaping) gibi işlemleri gerçekleştirmek için bir güvenlik çerçevesi (security framework) veya doğrulama sınıfı kullanmak. |  |  |  |  |

B.6

#

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| 12 | Sistem tasarımı, varlıkların ayrımını (separation of entities) dikkate alıyor mu? Örnek: Farklı ağlara bağlı farklı sunucuların fiziksel olarak ayrılması, sanal makinelerin kullanımı veya “air gap” (fiziksel ağ yalıtımı). |  |  |  |  |
| 13 | Sistem, varsayılan ayarlardaki (default settings) değişiklikleri destekliyor mu? Örnek: Kullanıcıyı, varsayılan olarak atanmış ayarları değiştirmeye zorlamak. |  |  |  |  |
| 14 | Saldırılara tepki verme (reacting to attacks) |  |  |  |  |

Erişimi iptal etmeyi sistem destekliyor mu?  
Buna bir örnek, bir saldırıdan şüphelenildiğinde, normalde meşru olan kullanıcılar ve kullanımlar için bile hassas kaynaklara erişimin sınırlandırılmasıdır.

15  

Erişimi kilitlemeyi sistem destekliyor mu?  
Buna bir örnek, bir kaynağa erişmek için tekrarlanan başarısız denemeler olduğunda o kaynağa erişimin sınırlandırılmasıdır.

16  

Aktörleri bilgilendirmeyi sistem destekliyor mu?  
Buna bir örnek, bir saldırıdan şüphelenildiğinde veya saldırı tespit edildiğinde operatörlerin, diğer personelin ya da iş birliği yapan sistemlerin bilgilendirilmesidir.

17  

Saldırılardan
kurtulma

Sistem bir denetim izi (audit trail) tutmayı destekliyor mu?  
Buna bir örnek, bir saldırganın eylemlerini geriye dönük izleyebilmek ve kimliğini belirleyebilmek için kullanıcı ve sistem eylemlerinin ve bunların etkilerinin kaydının tutulmasıdır.

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Güvenlik

259  

Gerekçe ve
Varsayımlar

260  

Ek B—Taktik Tabanlı Anketler

## B.7 Test Edilebilirlik (Testability)

| # | Taktik Grubu                        | Taktik Sorusu |
|---|-------------------------------------|---------------|
| 1 | Sistem durumunu denetle ve gözle (control and observe system state) | Sistem ya da sistem bileşenleri test etmeyi ve izlemeyi kolaylaştırmak için özelleşmiş arayüzler sağlıyor mu? |

2  

Sistem, bir arayüzü geçen bilginin daha sonra test amaçlı kullanılabilmesi için kaydedilmesini sağlayan mekanizmalar sunuyor mu (kayıt/oynatma – record/playback)?

3  

Sistemin, alt sistemin ya da modüllerin durumu, test etmeyi kolaylaştırmak için tek bir yerde saklanıyor mu (yerelleştirilmiş durum depolama – localized state storage)?

4  

Veri kaynaklarını soyutlayabiliyor musunuz; örneğin, arayüzleri soyutlayarak? Arayüzleri soyutlamak, test verisini daha kolay ikame etmenize olanak tanır.

5  

Sistem, deney yapmak veya test etmek için, deneyin sonuçlarını geri almaktan endişe etmeden, yalıtılmış (sandbox) biçimde çalıştırılabiliyor mu?

6  

Sistemin, bir programın ne zaman ve nerede hatalı bir durumda olduğunu belirtmek için yürütülebilir iddialar (executable assertions) kullanan kodu var mı?

7  

### Karmaşıklığı sınırla

Sistem, yapısal karmaşıklık sınırlı olacak şekilde tasarlandı mı?  
Örnekler: döngüsel bağımlılıklardan kaçınma, bağımlılıkları azaltma ve bağımlılık enjeksiyonu (dependency injection) gibi tekniklerin kullanılması.

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

### B.8 Kullanılabilirlik (Usability)

| # | Taktik Grubu | Taktik Sorusu |
|---|--------------|---------------|
| 8 |              | Sistem, belirlenimsizliğin (nondeterminism) az sayıda veya hiç kaynağını içeriyor mu? Bu, kısıtsız paralellikten (unconstrained parallelism) kaynaklanan davranışsal karmaşıklığı sınırlandırmaya yardımcı olur; bu da test etmeyi basitleştirir. |

## B.8 Kullanılabilirlik (Usability)

| # | Taktik Grubu                  | Taktik Sorusu |
|---|------------------------------|---------------|
| 1 | Kullanıcı inisiyatifini destekleme (supporting user initiative) | Sistem, işlemleri iptal etmeyi destekliyor mu? |

2  

Sistem, işlemleri geri almayı (undo) destekliyor mu?

3  

Sistem, işlemlerin duraklatılıp (pause) daha sonra devam ettirilmesini destekliyor mu?  
Örneğin, bir web tarayıcısında bir dosya indirmesini duraklatmak ve kullanıcının tamamlanmamış (ve başarısız olmuş) bir indirmeyi yeniden denemesine izin vermek.

4  

Sistem, işlemlerin nesne gruplarına uygulanmasını (birleştirme – aggregation) destekliyor mu?  
Örneğin, bir dosya gezgini penceresinde seçili bir dizi dosyanın toplam boyutunu görmenize izin veriyor mu?

Destekleniyor mu?
(E/H)

(Devam eder)

261  

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

262  

Ek B—Taktik Tabanlı Anketler

| # | Taktik Grubu                 | Taktik Sorusu |
|---|-----------------------------|---------------|
| 5 | Sistem inisiyatifini destekleme (support system initiative) | Sistem, kullanıcının yürüttüğü görevlere dayanarak (bir görev modeli – task model – tutarak) kullanıcıya yardım sağlıyor mu? Örnekler şunlardır:  |

- Girdi verisinin doğrulanması  
- Kullanıcı arayüzündeki (UI) değişikliklere kullanıcının dikkatinin çekilmesi  
- UI tutarlılığının korunması  
- UI’nin sağladığı işlevleri bulmalarına yardımcı olmak için kullanıcıya araç çubukları ve menüler eklenmesi  
- Kullanıcıların temel kullanıcı senaryolarını gerçekleştirmelerinde onlara yol göstermek için sihirbazlar (wizards) veya diğer tekniklerin kullanılması  

6  

Sistem, kullanıcı sınıfına göre UI’de ayarlamalar yapmayı (bir kullanıcı modeli – user model – tutarak) destekliyor mu?  
Örnekler arasında UI özelleştirmesini (yerelleştirme – localization dahil) ve erişilebilirlik desteğini sağlamak yer alır.

7  

Sistem, sistem özelliklerine dayanarak (bir sistem modeli – system model – tutarak) kullanıcıya uygun geri bildirim sağlıyor mu?  
Örnekler şunlardır:

- Uzun süren istekler işlenirken kullanıcıyı engellemekten kaçınmak  
- Eylem ilerlemesine ilişkin geri bildirim sağlamak (örn. ilerleme çubukları – progress bars)  
- Hataları yöneterek, hassas verileri açığa çıkarmadan kullanıcı dostu hata mesajları göstermek  
- Ekran boyutu ve çözünürlüğe göre UI’yi ayarlamak  

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

## B.9 DevOps

| # | Taktik Grubu | Taktik Sorusu |
|---|--------------|---------------|
| 1 | Test edilebilirlik: sistem durumunu denetle ve gözle (Testability: control and observe system state) | Sistem ya da sistem bileşenleri test etmeyi ve izlemeyi kolaylaştırmak için özelleşmiş arayüzler sağlıyor mu? |

2  

Sistem, bir arayüzü geçen bilginin daha sonra test amaçlı kullanılabilmesi için kaydedilmesini sağlayan mekanizmalar sunuyor mu (kayıt/oynatma – record/playback)?

3  

Sistem, deney yapmak veya test etmek için, deneyin sonuçlarını geri almaktan endişe etmeden, yalıtılmış (sandbox) biçimde çalıştırılabiliyor mu?

4  

### Performans: kaynakları yönet (Performance: manage resources)

Sistem, kaynakları kesintisiz bir şekilde artırabiliyor mu (örneğin CPU, bellek, ağ bant genişliği)?

5  

Sistem eşzamanlılık (concurrency) ekleyebiliyor mu?  
Örneğin, daha fazla hizmet isteğinin aynı anda işlenebilmesi için paralel işlem akışlarının (parallel processing streams) kesintisiz şekilde eklenmesini destekliyor mu?

6  

Sistem, sık erişilen verilere yönelik paylaşım çatışmasını (contention) azaltmak için verinin birden çok kopyasını tutuyor mu (örneğin veritabanlarını çoğaltarak ya da önbellekler kullanarak)?

(Devam eder)

264  

Ek B—Taktik Tabanlı Anketler

7  

Sistem, sık erişilen hesaplama kaynaklarına yönelik paylaşım çatışmasını azaltmak için hesaplamaların birden çok kopyasını tutuyor mu (örneğin bir sunucu çiftliğinde – server farm – sunucu havuzu – server pool – bulundurarak)?

8  

Sistem, özellikle kıt kaynakları, açık bir zamanlama politikasına (scheduling policy) göre tahsis edilebilmeleri için zamanlıyor mu?

9  

### Performans: kaynak talebini denetle (Performance: control resource demand)

Sistem, hizmet isteklerine yanıt verme ek yükünü azaltıyor mu; örneğin aracıları kaldırarak veya kaynakları birlikte konumlandırarak (co-location)?

10  

Girdileriniz sürekli bir veri akışı ise, sistem örnekleme oranını yönetiyor mu?  
Yani, veri örneklemesini değişen oranlarda (ve buna eşlik eden doğruluk/özgünlük – accuracy/fidelity – değişimiyle) yapabilmeniz mümkün mü?

11  

Sistem, olaylara verdiği yanıtı izliyor ve sınırlandırıyor mu?  
Yani, sistem belirli bir zaman aralığında yanıt verdiği olay sayısını sınırlandırarak, gerçekten servis verdiği olaylar için öngörülebilir yanıtlar sağlamayı garanti altına alıyor mu?

12  

Sunulan hizmet için, mevcut kaynaklardan daha fazla istek olabileceği göz önünde bulundurulduğunda, sistem olayları önceliklendiriyor mu?

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Gerekçe
ve
Varsayımlar

B.9  

13  

### Değiştirilebilirlik: bağımlılığı azalt (Modifiability: reduce coupling)

14  

Taktik Sorusu

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

DevOps

265  

Gerekçe
ve
Varsayımlar

Modifiability: bağlamayı erteleme (defer binding)

15  

Sistem işlevselliği tutarlı biçimde kapsülleyebiliyor mu? Bu tipik olarak, inceleme altındaki işlevselliğin yalıtılmasını ve buna açık (explicit) bir arayüzün tanıtılmasını içerir.  

Sistem, birden çok benzer hizmet sağladığınız durumlarda, ortak hizmetleri soyutluyor mu? Örneğin, bu teknik genellikle sisteminizi işletim sistemleri, donanım veya diğer çevre (environment) değişkenleri arasında taşınabilir (portable) yapmak istediğinizde kullanılır.  

Sistem, önemli işlevselliklerin bağlanmasını (binding) düzenli olarak yaşam döngüsünün ileriki safhalarına erteliyor mu ki bu işlevler daha sonra, hatta belki son kullanıcılar tarafından değiştirilebilsin? Örneğin, sistemin işlevselliğini genişletmek için eklentiler (plug-ins), ilave modüller (add-ons) veya kullanıcı betiklerini (user scripting) kullanıyor musunuz?  

16  

Kullanılabilirlik (availability): hataları tespit etmek (detect faults)  

Sistem, diğer sistem parçalarının sağlık durumunu izlemek için bir bileşen kullanıyor mu? Bir sistem izleyicisi (system monitor), ağdaki veya diğer paylaşılan kaynaklardaki (örneğin bir hizmet engelleme saldırısından – denial-of-service attack – kaynaklanan) arıza veya tıkanıklığı (congestion) tespit edebilir.  

17  

Normal yürütme akışını değiştiren bir sistem durumunu tespit etmek için istisna tespitini (exception detection) kullanıyor musunuz? (Örneğin sistem istisnası, parametre sınırı – parameter fence, parametre tür denetimi – parameter typing, zaman aşımı – timeout gibi.)  

(Devamı)

---

# Ek B — Taktik Temelli Anketler

| Taktik Grubu | # | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar |
|-------------|---|---------------|--------------------------|------|----------------------------|------------------------|
|             | 18 | Sistem, çoğaltılmış (replicated) bileşenlerin aynı sonuçları ürettiğini denetlemek için oylama (voting) kullanıyor mu? Çoğaltılmış bileşenler, özdeş kopyalar, işlevsel olarak yedek (functionally redundant) ya da analitik olarak yedek (analytically redundant) olabilir. | | | | |
| Kullanılabilirlik (availability): hatalardan kurtulma (recover from faults) (hazırlık ve onarım – preparation and repair) | 19 | Sistem, bir hata durumunda önceden kaydedilmiş iyi bir duruma (“rollback line”) geri dönebilmek için geri alma (rollback) kullanıyor mu? | | | | |
|             | 20 | Sistem etkin yedeklilik (active redundancy, hot spare) kullanıyor mu? Etkin yedeklilikte, bir koruma grubundaki (protection group; bir veya daha fazla düğümün “aktif” olduğu ve geri kalanların yedek (spare) olarak hizmet verdiği düğüm grubu) tüm düğümler aynı girdileri paralel olarak alır ve işler; bu sayede yedek düğümler, aktif düğüm(ler) ile eşzamanlı durumu (synchronous state) koruyabilir. | | | | |
|             | 21 | Sistem, arızalardan sonraki yeniden yapılandırma (reconfiguration) için tutarlı politika ve mekanizmalara sahip mi; yani işlevselliğin olabildiğince fazlasını korurken, sorumlulukları çalışmaya devam eden kaynaklara yeniden atayabiliyor mu? | | | | |
|             | 22 | Sistem, hatalarla başa çıkmak için istisna işleme (exception handling) kullanıyor mu? Tipik olarak, işleme ya hatanın rapor edilmesini ya da ele alınmasını içerir; bu da potansiyel olarak istisnaya neden olan sebebin düzeltilmesi ve işlemin yeniden denenmesi yoluyla hatanın maskelemesini (masking) sağlayabilir. | | | | |

---

## B.10 Daha Fazla Okuma

Anketlerin türetildiği taktik kataloğu, L. Bass, P. Clements ve R. Kazman, *Software Architecture in Practice* (3. baskı), 2012 içinde bulunabilir.  

SEI ATAM’lerinden elde edilen kalite niteliği (quality attribute) verilerinin analizi ve uygulamada en yaygın görülen niteliklerin hangileri olduğunu gösteren çalışma için bkz. I. Ozkaya, L. Bass, R. Sangwan ve R. Nord, “Making Practical Use of Quality Attribute Information”, *IEEE Software*, Mart/Nisan 2008; ve daha sonraki çalışma için bkz. S. Bellomo, I. Gorton ve R. Kazman, “Insights from 15 Years of ATAM Data: Towards Agile Architecture”, *IEEE Software*, 32:5, 38-45, Eylül/Ekim 2015.  

DevOps taktikleri kümesi, H-M Chen, R. Kazman, S. Haziyev, V. Kropov ve D. Chtchourov tarafından “Architectural Support for DevOps in a Neo-Metropolis BDaaS Platform”, *IEEE 34th Symposium on Reliable Distributed Systems Workshop (SRDSW)*, Montreal, Kanada, Eylül 2015’te geliştirilmiş ve sunulmuştur.  

---

Bu sayfa bilerek boş bırakılmıştır.

---

# Sözlük (Glossary)

**Ara Tasarımlar için Etkin İncelemeler (Active Reviews for Intermediate Design, ARID) yöntemi**  
Mimari tasarımın (veya bir bölümünün) tipik olarak tasarımı kullanacak mühendislerden oluşan bir grup değerlendiriciye sunulduğu bir yöntemdir. Sunumdan sonra bir senaryo kümesi seçilir. Değerlendiriciler, mimarideki öğeleri kullanarak bu senaryoları karşılamaya çalışırlar. Değerlendiricilerden, arayüzleri tanımlamak amacıyla kod veya sözde kod (pseudocode) yazmaları ya da ardışıklık diyagramları (sequence diagrams) oluşturmaları istenir. Bu yöntem, öğe etkileşim tasarımına (element interaction design) hazırlık amacıyla kullanılabilir.  

**ADD**  
Bkz. Nitelik Güdümlü Tasarım (Attribute Driven Design) yöntemi.  

**ADL**  
Bkz. Mimari Tanımlama Dili (Architecture Description Language).  

**Analiz (analysis)**  
Karmaşık bir varlığı anlamak amacıyla onu bileşen parçalarına ayırma süreci. Analiz, tasarım sürecinin farklı anlarında kullanılır; örneğin girdiler tasarım kararları vermek için analiz edilir ve ortaya çıkan mimari de, ilişkili sürücüleri (drivers) karşılamak için uygun olup olmadığını ölçmek amacıyla analiz edilir.  

**Uygulama çatısı (application framework)**  
Yeniden kullanılabilir bir yazılım öğesi; desenler (patterns) ve taktiklerden (tactics) oluşturulmuştur ve geniş bir uygulama yelpazesinde yinelenen alan (domain) ve kalite niteliği (quality attribute) kaygılarını ele alan genel işlevsellik sağlar. Çatı (framework) olarak da adlandırılır.  

> **💬 Çevirmen notu:** “Application framework” için Türkçede yaygın kullanım “uygulama çatısı/framework’ü”dür; metinde “çatısı (framework)” biçimiyle her iki kullanımı da görünür kılmaya çalıştım.

**Mimari kaygı (architectural concern)**  
Mimari tasarımın bir parçası olarak ele alınması gereken, ancak geleneksel bir gereksinim olarak ifade edilmeyen ek bir boyut. Örneklere genel kaygılar (örneğin genel bir sistem yapısı oluşturma) ve daha özel kaygılar (örneğin istisnaları yönetme veya günlük (log) üretme) dahildir. Diğer mimari kaygılar, genellikle müşteriler tarafından ifade edilmeyen iç gereksinimler ile mimari değerlendirmeler gibi analiz faaliyetlerinden doğan sorunları içerir.  

**Mimari tasarım (architectural design)**  
Fikirleri ihtiyaçlar dünyasından (mimari sürücüler – architectural drivers) çözümler dünyasına, yapılar cinsinden çevirmek için karar verme etkinliği.  

**Mimari sürücüler (architectural drivers)**  
Tasarım amacı, mimari açıdan önemli gereksinimler (architecturally significant requirements) ve tasarım sürecine girdi olarak hizmet eden mimari kaygılar. Bu hususlar sistemin başarısı açısından kritik önemdedir ve bu nedenle mimariyi yönlendirir ve şekillendirir.  

**Mimari değerlendirme (architectural evaluation)**  
Mimari kararların değerini analiz etmek ve değerlendirmek için kullanılan bir teknik.  

**Mimari desen (architectural pattern)**  
Bkz. Desenler (Mimari ve Tasarım) [Patterns (Architectural and Design)].  

**Mimari açıdan önemli gereksinim (architecturally significant requirement, ASR)**  
Yazılım mimarisi açısından özel bir öneme sahip olan sistem gereksinimi. ASR’ler kalite niteliklerini, birincil işlevsel gereksinimleri ve kısıtları (constraints) içerir.  

**Mimari Tanımlama Dili (Architecture Description Language, ADL)**  
Bir mimariyi belgeleme gösterimi. ADL’ler tipik olarak bir mimariyi tanımlamak için hem grafik bir gösterim hem de (biçimsel olarak tanımlanmış) metinsel bir gösterim kullanır; esas olarak hesaplamaya yönelik (çalışma zamanı – runtime) bileşenleri, bunlar arasındaki etkileşimleri ve mimarinin özelliklerini tarif ederler.  

**Mimari Takas Analizi Yöntemi (Architecture Tradeoff Analysis Method, ATAM)**  
Senaryolar tarafından güdümlü, mimarileri analiz etmek için yerleşik bir yöntemdir. Amacı, kalite niteliği gereksinimleri ve iş hedefleri ışığında mimari kararların sonuçlarını değerlendirmektir.  

**ARID**  
Bkz. Ara Tasarımlar için Etkin İncelemeler (Active Reviews for Intermediate Design) yöntemi.  

**ASR**  
Bkz. Mimari açıdan önemli gereksinim (architecturally significant requirement).  

**ATAM**  
Bkz. Mimari Takas Analizi Yöntemi (Architecture Tradeoff Analysis Method).

Attribute-Driven Design (ADD) yöntemi Sürücüleri (driver) girdi olarak alan ve çıktı olarak bir mimari üreten, yinelemeli (iterative) bir mimari tasarım yöntemidir. Her yinelemede, önceki yinelemelerde tanımlanmış öğelerin rafine edilmesiyle yapılar üretilir. Bu yapılar, ağırlıklı olarak tasarım kavramlarından (design concept) oluşturulur; bu kavramlar, o yinelemede ele alınmak üzere seçilmiş sürücülerin bir alt kümesini karşılamak için seçilir ve somutlaştırılır (instantiate edilir).

Big Design Up Front (BDUF) Artık büyük ölçüde itibar görmeyen, mimari tasarımın tamamını projenin başında yapmaya çalışmaya dayalı uygulama. Genellikle şelale (waterfall) yazılım geliştirme yaşam döngüsüyle ilişkilendirilir.

Brownfield geliştirme (brownfield development) Mevcut bir varlık (asset) üzerine inşa eden yazılım geliştirme. Greenfield geliştirme (greenfield development) ile karşıtlık içindedir.

Kısıt (constraint) Mimarın çok az kontrol edebildiği ya da hiç kontrol edemediği bir karar. Teknik ya da örgütsel (organizational) olabilir.

Maliyet Fayda Analizi Yöntemi (Cost Benefit Analysis Method, CBAM) Bir mimaride iyileştirme yapmak için seçilen stratejilere maliyet, fayda ve zamanlama etkilerini ilişkilendiren bir yöntem. Bu yöntem, bir sonraki yinelemede uygulanacak en uygun strateji kümesini bulmanın aracı olarak, stratejileri derecelendirmek için kullanılır.

---

Tasarım kavramı (design concept) Mimarinin yapılarını oluşturan yapıtaşları. Referans mimariler (reference architecture), dağıtım desenleri (deployment pattern), mimari desenler (architectural pattern), taktikler (tactic), teknoloji aileleri (technology family) ve dışarıda geliştirilmiş bileşenler (örneğin çerçeveler/framework) dahil olmak üzere farklı türde tasarım kavramları vardır.

Tasarım kavramları kataloğu (design concepts catalog) Belirli bir uygulama alanına (application domain) yönelik tasarım kavramlarının bir koleksiyonu.

Tasarım kararı (design decision) Tasarım sürecinde verilen, seçilen bir tasarım kavramının belirlenmesi ve bu tasarım kavramının somutlaştırılmasını (instantiation) içeren karar.

Tasarım yinelemesi (design iteration) Sürücülerin (drivers) bir alt kümesinin yapılara dönüştürüldüğü tasarım kararları grubudur. Bir tasarım turu (design round) içinde bir veya daha fazla tasarım yinelemesi gerçekleştirilir.

Tasarım deseni (design pattern) bkz. Desenler (mimari ve tasarım).

Tasarım amacı (design purpose) Mimari tasarımın niçin yapıldığı. Örneğin tasarım, satış öncesi (pre-sales) aşamada tahmin için, prototipleme için ya da geliştirme amaçlı yapılabilir.

Tasarım turu (design round) Yinelemeli (iterative) bir geliştirme modeli kullanılıyorsa, bir geliştirme döngüsü (development cycle) içinde gerçekleştirilen mimari tasarım aktiviteleri; şelale model kullanılıyorsa, mimari tasarım aktivitelerinin tümü.

Dağıtım deseni (deployment pattern) Sistemin fiziksel olarak nasıl yapılandırılıp dağıtılacağına ilişkin bir model sağlayan desen.

Geliştirme döngüsü (development cycle) Bir proje artımının (project increment) geliştirilmesi, yani bir proje yinelemesi (project iteration).

DevOps “Geliştirme” (development) ve “işletim”i (operations) birleştiren bir portmanto sözcüktür. DevOps, yazılım projelerini yürütmenin önceki biçimlerinde olduğu gibi, geliştirme ekiplerinin yazılımı geliştirip ardından “duvarın üzerinden” işletime atmasına karşıtlık oluşturur. DevOps’ta iki ekip yakın çalışır ve yazılımı hızlı biçimde değiştirmeyi, derlemeyi, test etmeyi, yayımlamayı ve izlemeyi kolaylaştırmak üzere süreçler, araçlar ve mimariler benimser.

Öğe (element) (yazılım mimarisi tanımında) Mimarinin yapılarını oluşturan parçalardan biri. Öğeler çalışma zamanında (runtime) veya geliştirme zamanında (development time) ya da fiziksel olarak var olabilir. Öğeler ilişkiler (relation) ile birbirine bağlanır.

Öğe etkileşimi tasarımı (element interaction design) Birincil olmayan kullanım durumlarını (nonprimary use cases) desteklemek üzere modüllerin ve bunlarla ilişkili arayüzlerin (interface) tanımlanması. Bu, genellikle mimari tasarım sırasında alınan kararlara uygun olarak, dizge (sequence) diyagramları kullanılarak gerçekleştirilir.

Öğe iç tasarımı (element internals design) Öğe etkileşimi tasarımının bir parçası olarak tanımlanan öğelerin, öğenin arayüzünü tatmin edecek şekilde iç tasarımı.

---

Dışarıda geliştirilmiş bileşen (externally developed component) Doğası gereği somut olan ve sistem geliştirmesinin parçası olarak inşa edilmeyen, bunun yerine edinilip yeniden kullanılan bir tasarım kavramı. Uygulama çerçeveleri (application framework), ürünler ve platformlar bu tür bileşenlere örnektir.

Greenfield geliştirme (greenfield development) Üzerine inşa edilecek çok az ya da hiç eski (legacy) kod tabanı olmadan başlayan yazılım geliştirme.

Somutlaştırma (instantiation) Bir tasarım kavramını ele alınan belirli probleme uyarlama süreci. Seçilen tasarım kavramından öğeler ve ilişkiler oluşturmayı ve öğelerle sorumlulukları ilişkilendirmeyi içerir. Somutlaştırma, tasarım kavramlarının dışarıda geliştirilmiş bileşenler olması durumunda yapılandırmaya (configuration) da atıfta bulunabilir.

Arayüz (interface) Öğelerin, ilişkiler aracılığıyla işbirliği yapmasını ve bilgi alışverişinde bulunmasını sağlayan, öğelerin dışarıdan görülebilir özellikleri. Bu özellikler, öğeler arasında sözleşmesel (contractual) bir belirtim oluşturur.

Marketecture Genellikle tek sayfalık, çoğunlukla resmi olmayan bir yazılım sistem mimarisi gösterimi. Bu gösterim, öncelikle teknik olmayan kişileri hedefler ve bir sistem vizyonunu sunmak için kullanılır.

Asgari uygulanabilir ürün (minimum viable product, MVP) Ürünün sahaya sürülmesini sağlayacak yalnızca çekirdek özellikleri içeren, evrimsel bir prototip. Gerçek kullanıcılarla ürünün sahaya sürülmesi ve kullanım verilerinin toplanması yoluyla bir hipotezi sınamaya odaklanır; bu veriler daha sonra hipotezin onaylanmasına ya da reddedilmesine yardımcı olur.

Desenler (mimari ve tasarım) Belirli bir bağlamda yinelenen tasarım problemlerine yönelik kavramsal çözümler. Bir mimari sürücüyü (architectural driver) ele almak için kullanıldıklarında “mimari desen” (architectural pattern); etkileri yerel düzeyde kaldığında —örneğin öğe iç tasarımında kullanıldıklarında— “tasarım deseni” (design pattern) adını alırlar.

Platform Uygulamaları inşa etmek ve çalıştırmak için üzerine oturulan eksiksiz altyapı.

Satış öncesi (pre-sales) Proje geliştiriminde, projenin kapsamının, iş gerekçesinin (business case) ve ilk planın belirlendiği aşama. Bu aşama, müşterilerin (ya da fon sağlayanların) projeyi sürdürmek isteyip istemediklerine karar vermeleri için kullanılır.

Birincil işlevsel gereksinimler (primary functional requirements) İşlevsellik, sistemin amaçlandığı işi yapabilme yeteneğidir. Birincil işlevsellik, genellikle, sistemin geliştirilmesini motive eden iş hedeflerine ulaşmak için kritik olan işlevsellik olarak tanımlanır.

Ürün (product) Tasarlanmakta olan sisteme entegre edilebilen, yalnızca küçük miktarda yapılandırma ya da kodlama gerektiren, kendi içinde bütün işlevsel bir yazılım parçası. Yazılım paketi (software package) olarak da adlandırılır.

---

Kavramsal ispat (proof of concept, PoC) Bir teknolojiyi hızlıca değerlendirmek için kullanılan bir prototip; böylece bu teknolojinin genellikle performans ve ölçeklenebilirlik gibi kalite nitelikleriyle (quality attribute) ilişkili kritik mimari senaryoları karşılayıp karşılayamayacağı belirlenir.

QAW bkz. Kalite Niteliği Çalıştayı (Quality Attribute Workshop, QAW).

Kalite niteliği (quality attribute) Bir sistemin paydaşlarının (stakeholder) gereksinimlerini ne ölçüde karşıladığını göstermek için kullanılan, ölçülebilir ya da test edilebilir bir sistem özelliği. Kalite nitelikleri işlevselliğe ortogonaldir (yani ondan bağımsız eksenlerde ele alınır).

Kalite niteliği senaryosu (quality attribute scenario) bkz. Senaryo (scenario).

Kalite Niteliği Çalıştayı (Quality Attribute Workshop, QAW) Bir grup sistem paydaşının kalite niteliklerini ortaya çıkarması (elicitation), belirtmesi, önceliklendirmesi ve bu nitelikler üzerinde uzlaşmaya varması için kolaylaştırılmış (facilitated) bir beyin fırtınası oturumu.

Gerekçe (rationale) Bir tasarım kararına yol açan akıl yürütme ve gerekçelendirme zinciri.

Refactoring Bir sistemin mimarisini veya kodunu, işlevselliğini etkilemeden, farklı kalite niteliği (quality attribute) tepkileri elde etmek için değiştirme.

Reference Architecture (referans mimarisi) Uygulama türleri için genel bir mantıksal yapı sağlayan, bir veya daha fazla mimari desen (architectural pattern) ile eşleştirilen bir referans modelinden (reference model) oluşan planlar (blueprints). İş ve teknik bağlamlarda kendini kanıtlamıştır ve genellikle kullanımını kolaylaştıran bir dizi destekleyici yapıtla (artifact) birlikte gelir.

Relation (ilişki) (yazılım mimarisi tanımında) Bir mimarinin yapıları (structures) içinde yer alan parçalardan biri. İlişkiler çalışma zamanında, geliştirme zamanında veya fiziksel olarak var olabilir. İlişkiler, öğeleri birbirine bağlar.

Scenario (senaryo) Sistem tarafından alınan bir uyarıcıyı (stimulus) ve bu uyarıcıya verilen ölçülebilir bir tepkiyi tanımlayan, kalite niteliklerini belirtmeye yönelik bir teknik. Senaryolar, ele alınan sistemin kalite niteliği davranışına ilişkin sınanabilir, yanlışlanabilir hipotezlerdir. Tam olarak geliştirilmiş senaryolar altı bölüm kullanılarak tanımlanır, ancak daha az ayrıntılı (“ham”) senaryolar da tanımlanabilir.

Sketch of a view (bir görünümün krokisi/eskizi) Tasarım sürecinin bir parçası olarak oluşturulan ön aşama dokümantasyon türü. Krokiler, genellikle tasarım etkinliği tamamlandıktan sonra, tam teşekküllü bir görünüme (view) dönüştürülecek şekilde rafine edilebilir.

Software architecture (yazılım mimarisi) “Sistem hakkında akıl yürütmek için gerekli olan ve yazılım öğelerini (software element), bunlar arasındaki ilişkileri (relations) ve her ikisinin de özelliklerini (properties) içeren yapıların (structures) kümesi.”

Spike Teknik bir soruyu yanıtlamak veya bilgi toplamak için oluşturulan, zaman kutulu (time-boxed) görev.

Structure (yapı) Uyumlu bir yazılım öğeleri, ilişkiler ve özellikler kümesi. Yapılar, görünümler (views) içinde temsil edilir.

Tactic (taktik) Bir kalite niteliği tepkisinin kontrolünü etkileyen, kendini kanıtlamış bir tasarım stratejisi.

---

Teknik borç (technical debt) Bir yazılım projesinde, genellikle “hack” olarak adlandırılan ve sistemin uzun vadeli sürdürülebilirliği pahasına, uygulama kolaylığı gibi kısa vadeli kazanımlarla takas edilen kararlar. Bu tür kestirmeler kullanıldığında, yazılım tabanı “borca girer”.

Technology family (teknoloji ailesi) Ortak işlevsel amaçlara sahip teknolojiler grubu.

View (görünüm) Bir mimari yapının (architectural structure) temsili. Bir görünüm genellikle yapının grafiksel bir gösterimini ve diyagramda sunulan bilgiyi tamamlayan ek bilgileri içerir.

---

## Yazarlar Hakkında

**Humberto Cervantes**, Meksiko Şehri’ndeki Universidad Autónoma Metropolitana Iztapalapa’da profesördür. Öncelikli araştırma alanı yazılım mimarisi olup, daha özel olarak tasarım sürecine yardımcı olacak yöntem ve araçların geliştirilmesidir. Bu yöntem ve araçların yazılım endüstrisinde benimsenmesini teşvik etme konusunda aktiftir. 2006’dan bu yana Cervantes, yazılım mimarisiyle ilişkili konularda yazılım geliştirme şirketlerine danışmanlık yapmaktadır. Çok sayıda araştırma makalesi ve popülerleştirme yazısı kaleme almış, ayrıca yazılım mimarisi konusunda İspanyolca yazılmış az sayıdaki kitaptan birinin ortak yazarlığını yapmıştır.

Cervantes, Fransa Grenoble’daki Université Joseph Fourier’den yüksek lisans ve doktora derecelerini almıştır. SEI’den Yazılım Mimarisi Profesyoneli (Software Architecture Professional) ve ATAM Değerlendiricisi (ATAM Evaluator) sertifikalarına sahiptir. Yazılım mühendisliğinin yanı sıra, ailesi ve arkadaşlarıyla vakit geçirmekten, spor yapmaktan ve seyahat etmekten hoşlanır.

**Rick Kazman**, Hawaii Üniversitesi’nde profesör ve Carnegie Mellon University Yazılım Mühendisliği Enstitüsü’nde (Software Engineering Institute, SEI) araştırmacıdır. Başlıca araştırma ilgi alanları yazılım mimarisi, tasarım ve analiz araçları, yazılım görselleştirme ve yazılım mühendisliği ekonomisidir. Kazman, mimari analiz için SAAM (Software Architecture Analysis Method), ATAM (Architecture Tradeoff Analysis Method), CBAM (Cost–Benefit Analysis Method) ve Dali ile Titan araçları da dahil olmak üzere, oldukça etkili birçok yöntem ve araç geliştirmiştir. Yüz elliden fazla hakemli makalenin yazarı ve Software Architecture in Practice, Third Edition (Addison-Wesley, 2013), Evaluating Software Architectures (Addison-Wesley, 2002) ve Ultra-Large-Scale Systems (Software Engineering Institute, 2006) dahil olmak üzere birkaç kitabın ortak yazarıdır.

Kazman, University of Waterloo’dan B.A. (İngilizce/müzik) ve M.Math. (bilgisayar bilimi), York University’den M.A. (İngilizce) ve Carnegie Mellon University’den Ph.D. (hesaplamalı dilbilim, computational linguistics) derecelerini almıştır. Nasıl olup da yazılım mühendisliği araştırmacısı olduğunun cevabı ise herkese göre ayrı bir muammadır. Mimari tasarım yapmadığı ya da mimari hakkında yazmadığı zamanlarda Kazman’ı bisiklete binerken, piyano çalarken, Tae Kwon Do ve Jiu Jitsu çalışırken ya da (daha sık olarak) Hawaii ile Pittsburgh arasında gidip gelirken bulabilirsiniz.