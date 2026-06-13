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
