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
