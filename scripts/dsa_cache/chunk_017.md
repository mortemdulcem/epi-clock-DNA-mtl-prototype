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

### 3.2.1 Adım 1: Girdileri Gözden Geçir
