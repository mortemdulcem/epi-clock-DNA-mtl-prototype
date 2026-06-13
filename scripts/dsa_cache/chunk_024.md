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
