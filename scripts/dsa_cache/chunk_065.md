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
