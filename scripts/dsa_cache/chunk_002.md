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
