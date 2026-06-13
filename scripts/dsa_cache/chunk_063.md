Yazılım sisteminin geliştirilmesi farklı yöntemler kullanılarak gerçekleştirilebilir. Ancak mimari tasarım, seçilen geliştirme yönteminden bağımsız olarak gerçekleştirilir. Bu nedenle, ADD (Attribute-Driven Design, nitelik temelli tasarım) gibi bir tasarım yöntemi, farklı geliştirme yöntemleriyle birlikte kullanılabilir. Şimdi, endüstride yaygın olarak kullanılan bazı geliştirme yöntemleriyle mimari tasarım arasındaki ilişkiyi tartışacağız.

### 9.1.2.1 Çevik (Agile) Yöntemler

Yazılım mimarisi ile çeviklik (agility) arasındaki ilişki, son on yıldır tartışma konusu olmuştur. Her ne kadar biz ve birçok araştırma, mimari uygulamalar ile Çevik (Agile) uygulamaların aslında birbirleriyle iyi hizalandığını göstersek de, bu görüş her zaman evrensel biçimde kabul görmemiştir.

Özgün Agile Manifesto’ya göre çevik uygulamalar şu değerlere vurgu yapar: “Süreçler ve araçlardan ziyade bireyler ve etkileşimler, kapsamlı dokümantasyondan ziyade çalışan yazılım, sözleşme müzakeresinden ziyade müşteriyle iş birliği ve bir planı takip etmekten ziyade değişime yanıt vermek”. Bu değerlerin hiçbirisi, doğası gereği mimari uygulamalarla çelişmez. Peki o zaman neden —en azından bazı çevrelerde— bu iki uygulama kümesinin birbiriyle bağdaşmaz olduğuna dair bir inanç ortaya çıkmıştır? Meselenin özü, Çevik uygulamalar ile mimari uygulamaların farklılaştığı tek ilkedir.

Agile Manifesto’nun ilk yaratıcıları, manifestonun arkasında yatan 12 ilkeyi tanımlamışlardır. Bu 12 ilkeden 11’i mimari uygulamalarla tamamen uyumludur; uyumlu olmayan yalnızca bir tanesidir: “En iyi mimariler, gereksinimler ve tasarımlar kendini örgütleyen (self-organizing) takımlardan ortaya çıkar.” Bu ilke küçük ve belki orta ölçekli projeler için geçerli olmuş olabilir, ancak büyük projelerde —özellikle karmaşık gereksinimlere ve dağıtık geliştirmeye sahip olanlarda— başarılı olduğuna dair herhangi bir örnekten haberdar değiliz. Sorunun kalbinde şu vardır: Yazılım mimarisi tasarımı “en başta yapılan” (up-front) bir iştir. Bir projeye her zaman doğrudan kod yazarak ve en az düzeyde, hatta hiç en başta analiz veya tasarım yapmadan başlayabilirsiniz. Buna, Şekil 9.3b’de gösterildiği gibi, türeyen (emergent) yaklaşım diyoruz. Bazı durumlarda —küçük sistemler, atılacak (throw-away) prototipler, müşteri gereksinimleri hakkında çok az fikir sahibi olduğunuz sistemler— bu, gerçekte en uygun karar olabilir. Diğer uçta ise, bütün gereksinimleri baştan toplamaya, bundan ideal mimariyi türetmeye, ardından da bu mimariyi gerçekleştirip test etmeye ve dağıtmaya çalışabilirsiniz. Şekil 9.3a’da gösterilen bu sözde En Baştan Büyük Tasarım yaklaşımı (Big Design Up Front, BDUF), genellikle klasik Şelale (Waterfall) yazılım geliştirme modeliyle ilişkilendirilir. Şelale modeli, geçtiğimiz on yıl içinde karmaşıklığı ve katılığı nedeniyle gözden düşmüştür; bu da çok sayıda iyi belgelenmiş maliyet aşımları, takvim (zaman) aşımları ve müşteri memnuniyetsizliği vakasına yol açmıştır. Mimari tasarım açısından bakıldığında, BDUF yaklaşımının olumsuz tarafı, kapsamlı biçimde belgelenmiş ancak test edilmemiş ve uygun olmayabilecek bir tasarım üretebilmesidir. Bu durum, tasarımdaki problemlerin genellikle geç fark edilmesi ve çok miktarda yeniden çalışma gerektirmesi, ya da özgün tasarımın en sonunda görmezden gelinmesi ve gerçek mimarinin hiç belgelenmemesi nedeniyle ortaya çıkar.

  
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
