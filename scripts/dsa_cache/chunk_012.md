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
