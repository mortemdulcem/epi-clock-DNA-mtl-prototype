§ Satış öncesi (pre-sales) aşamasında projenin kapsamı belirlenir ve bir iş gerekçesi (business case) oluşturulur. Bu aşamaya “satış öncesi” desek de, “satış” yapıp yapmadıklarından bağımsız olarak her organizasyonda gerçekleşir. Bu aşamanın sık rastlanan ve önemli çıktılarından biri, projenin maliyeti ve süresine ilişkin bir tahmindir. Bu tahmin, müşteriler (veya fon sağlayanlar) tarafından projeyi sürdürmek isteyip istemediklerine karar vermek için kullanılır.

§ Geliştirme ve işletim (operations) aşaması, satış öncesi teklifin müşteri tarafından kabul edilmesiyle başlar. Geliştirme, Agile, RUP (Rational Unified Process) veya TSP (Team Software Process) gibi farklı metodolojiler izlenerek gerçekleştirilebilir. Sistem (veya bir parçası) geliştirildiğinde işletime alınır. DevOps gibi daha yeni yaklaşımlar, genellikle geliştirme ve işletim arasında bulunan boşluğu azaltmayı amaçlar.

Mimari tasarım, şimdi tartışacağımız üzere bu iki temel aşamada önemli bir rol oynar.

## 9.1.1 Satış Öncesinde Mimari Tasarım

Birçok türde geliştirme projesinde, özellikle de özel (custom) yazılım geliştirme bağlamında, organizasyonların satış öncesi (pre-sales) aşamada proje süresi ve maliyetine ilişkin ilk tahmini sağlaması gerekir. Çoğu zaman satış öncesi faaliyetler kısa bir zaman aralığında gerçekleştirilmek zorundadır ve bu süreci bilgilendirecek bilgi miktarı her zaman sınırlıdır. Örneğin, bu aşamada genellikle yalnızca üst düzey gereksinimler veya özellikler (detaylı kullanım senaryoları (use case) yerine) mevcuttur.

Sınırlı bilgiyle ilgili sorun, üretilen tahminin çoğu zaman önemli belirsizlik içermesidir; bu durum Şekil 9.2’de gösterilen belirsizlik konisi (cone of uncertainty) ile betimlenmiştir. Belirsizlik konisi, bir projedeki tahminleri çevreleyen belirsizliğe işaret eder; genellikle maliyet ve zaman çizelgesi (schedule) tahminleri için kullanılır, ancak risk için de geçerlidir. Proje ilerledikçe tüm bu tahminler daha iyi hale gelir ve koni daralır. Proje bittiğinde belirsizlik sıfırdır. Herhangi bir geliştirme metodolojisi için temel mesele, belirsizlik konisini projenin yaşam döngüsünün daha erken safhalarında nasıl daraltacağıdır.

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
