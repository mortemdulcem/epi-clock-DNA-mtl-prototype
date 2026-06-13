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
aşama, ön satış (pre-sales) ve geliştirme ile işletmedir (development and operations).

Pre-Sales  
Architecture Design

Architecture Design

ŞEKİL 9.1 Proje geliştirmenin iki ana aşaması
