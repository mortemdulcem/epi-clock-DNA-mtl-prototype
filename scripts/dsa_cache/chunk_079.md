Modifiability: bağlamayı erteleme (defer binding)

15  

Sistem işlevselliği tutarlı biçimde kapsülleyebiliyor mu? Bu tipik olarak, inceleme altındaki işlevselliğin yalıtılmasını ve buna açık (explicit) bir arayüzün tanıtılmasını içerir.  

Sistem, birden çok benzer hizmet sağladığınız durumlarda, ortak hizmetleri soyutluyor mu? Örneğin, bu teknik genellikle sisteminizi işletim sistemleri, donanım veya diğer çevre (environment) değişkenleri arasında taşınabilir (portable) yapmak istediğinizde kullanılır.  

Sistem, önemli işlevselliklerin bağlanmasını (binding) düzenli olarak yaşam döngüsünün ileriki safhalarına erteliyor mu ki bu işlevler daha sonra, hatta belki son kullanıcılar tarafından değiştirilebilsin? Örneğin, sistemin işlevselliğini genişletmek için eklentiler (plug-ins), ilave modüller (add-ons) veya kullanıcı betiklerini (user scripting) kullanıyor musunuz?  

16  

Kullanılabilirlik (availability): hataları tespit etmek (detect faults)  

Sistem, diğer sistem parçalarının sağlık durumunu izlemek için bir bileşen kullanıyor mu? Bir sistem izleyicisi (system monitor), ağdaki veya diğer paylaşılan kaynaklardaki (örneğin bir hizmet engelleme saldırısından – denial-of-service attack – kaynaklanan) arıza veya tıkanıklığı (congestion) tespit edebilir.  

17  

Normal yürütme akışını değiştiren bir sistem durumunu tespit etmek için istisna tespitini (exception detection) kullanıyor musunuz? (Örneğin sistem istisnası, parametre sınırı – parameter fence, parametre tür denetimi – parameter typing, zaman aşımı – timeout gibi.)  

(Devamı)

---

# Ek B — Taktik Temelli Anketler

| Taktik Grubu | # | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar |
|-------------|---|---------------|--------------------------|------|----------------------------|------------------------|
|             | 18 | Sistem, çoğaltılmış (replicated) bileşenlerin aynı sonuçları ürettiğini denetlemek için oylama (voting) kullanıyor mu? Çoğaltılmış bileşenler, özdeş kopyalar, işlevsel olarak yedek (functionally redundant) ya da analitik olarak yedek (analytically redundant) olabilir. | | | | |
| Kullanılabilirlik (availability): hatalardan kurtulma (recover from faults) (hazırlık ve onarım – preparation and repair) | 19 | Sistem, bir hata durumunda önceden kaydedilmiş iyi bir duruma (“rollback line”) geri dönebilmek için geri alma (rollback) kullanıyor mu? | | | | |
|             | 20 | Sistem etkin yedeklilik (active redundancy, hot spare) kullanıyor mu? Etkin yedeklilikte, bir koruma grubundaki (protection group; bir veya daha fazla düğümün “aktif” olduğu ve geri kalanların yedek (spare) olarak hizmet verdiği düğüm grubu) tüm düğümler aynı girdileri paralel olarak alır ve işler; bu sayede yedek düğümler, aktif düğüm(ler) ile eşzamanlı durumu (synchronous state) koruyabilir. | | | | |
|             | 21 | Sistem, arızalardan sonraki yeniden yapılandırma (reconfiguration) için tutarlı politika ve mekanizmalara sahip mi; yani işlevselliğin olabildiğince fazlasını korurken, sorumlulukları çalışmaya devam eden kaynaklara yeniden atayabiliyor mu? | | | | |
|             | 22 | Sistem, hatalarla başa çıkmak için istisna işleme (exception handling) kullanıyor mu? Tipik olarak, işleme ya hatanın rapor edilmesini ya da ele alınmasını içerir; bu da potansiyel olarak istisnaya neden olan sebebin düzeltilmesi ve işlemin yeniden denenmesi yoluyla hatanın maskelemesini (masking) sağlayabilir. | | | | |

---

## B.10 Daha Fazla Okuma

Anketlerin türetildiği taktik kataloğu, L. Bass, P. Clements ve R. Kazman, *Software Architecture in Practice* (3. baskı), 2012 içinde bulunabilir.  

SEI ATAM’lerinden elde edilen kalite niteliği (quality attribute) verilerinin analizi ve uygulamada en yaygın görülen niteliklerin hangileri olduğunu gösteren çalışma için bkz. I. Ozkaya, L. Bass, R. Sangwan ve R. Nord, “Making Practical Use of Quality Attribute Information”, *IEEE Software*, Mart/Nisan 2008; ve daha sonraki çalışma için bkz. S. Bellomo, I. Gorton ve R. Kazman, “Insights from 15 Years of ATAM Data: Towards Agile Architecture”, *IEEE Software*, 32:5, 38-45, Eylül/Ekim 2015.  

DevOps taktikleri kümesi, H-M Chen, R. Kazman, S. Haziyev, V. Kropov ve D. Chtchourov tarafından “Architectural Support for DevOps in a Neo-Metropolis BDaaS Platform”, *IEEE 34th Symposium on Reliable Distributed Systems Workshop (SRDSW)*, Montreal, Kanada, Eylül 2015’te geliştirilmiş ve sunulmuştur.  

---

Bu sayfa bilerek boş bırakılmıştır.

---

# Sözlük (Glossary)

**Ara Tasarımlar için Etkin İncelemeler (Active Reviews for Intermediate Design, ARID) yöntemi**  
Mimari tasarımın (veya bir bölümünün) tipik olarak tasarımı kullanacak mühendislerden oluşan bir grup değerlendiriciye sunulduğu bir yöntemdir. Sunumdan sonra bir senaryo kümesi seçilir. Değerlendiriciler, mimarideki öğeleri kullanarak bu senaryoları karşılamaya çalışırlar. Değerlendiricilerden, arayüzleri tanımlamak amacıyla kod veya sözde kod (pseudocode) yazmaları ya da ardışıklık diyagramları (sequence diagrams) oluşturmaları istenir. Bu yöntem, öğe etkileşim tasarımına (element interaction design) hazırlık amacıyla kullanılabilir.  

**ADD**  
Bkz. Nitelik Güdümlü Tasarım (Attribute Driven Design) yöntemi.  

**ADL**  
Bkz. Mimari Tanımlama Dili (Architecture Description Language).  

**Analiz (analysis)**  
Karmaşık bir varlığı anlamak amacıyla onu bileşen parçalarına ayırma süreci. Analiz, tasarım sürecinin farklı anlarında kullanılır; örneğin girdiler tasarım kararları vermek için analiz edilir ve ortaya çıkan mimari de, ilişkili sürücüleri (drivers) karşılamak için uygun olup olmadığını ölçmek amacıyla analiz edilir.  

**Uygulama çatısı (application framework)**  
Yeniden kullanılabilir bir yazılım öğesi; desenler (patterns) ve taktiklerden (tactics) oluşturulmuştur ve geniş bir uygulama yelpazesinde yinelenen alan (domain) ve kalite niteliği (quality attribute) kaygılarını ele alan genel işlevsellik sağlar. Çatı (framework) olarak da adlandırılır.  

> **💬 Çevirmen notu:** “Application framework” için Türkçede yaygın kullanım “uygulama çatısı/framework’ü”dür; metinde “çatısı (framework)” biçimiyle her iki kullanımı da görünür kılmaya çalıştım.

**Mimari kaygı (architectural concern)**  
Mimari tasarımın bir parçası olarak ele alınması gereken, ancak geleneksel bir gereksinim olarak ifade edilmeyen ek bir boyut. Örneklere genel kaygılar (örneğin genel bir sistem yapısı oluşturma) ve daha özel kaygılar (örneğin istisnaları yönetme veya günlük (log) üretme) dahildir. Diğer mimari kaygılar, genellikle müşteriler tarafından ifade edilmeyen iç gereksinimler ile mimari değerlendirmeler gibi analiz faaliyetlerinden doğan sorunları içerir.  

**Mimari tasarım (architectural design)**  
Fikirleri ihtiyaçlar dünyasından (mimari sürücüler – architectural drivers) çözümler dünyasına, yapılar cinsinden çevirmek için karar verme etkinliği.  

**Mimari sürücüler (architectural drivers)**  
Tasarım amacı, mimari açıdan önemli gereksinimler (architecturally significant requirements) ve tasarım sürecine girdi olarak hizmet eden mimari kaygılar. Bu hususlar sistemin başarısı açısından kritik önemdedir ve bu nedenle mimariyi yönlendirir ve şekillendirir.  

**Mimari değerlendirme (architectural evaluation)**  
Mimari kararların değerini analiz etmek ve değerlendirmek için kullanılan bir teknik.  

**Mimari desen (architectural pattern)**  
Bkz. Desenler (Mimari ve Tasarım) [Patterns (Architectural and Design)].  

**Mimari açıdan önemli gereksinim (architecturally significant requirement, ASR)**  
Yazılım mimarisi açısından özel bir öneme sahip olan sistem gereksinimi. ASR’ler kalite niteliklerini, birincil işlevsel gereksinimleri ve kısıtları (constraints) içerir.  

**Mimari Tanımlama Dili (Architecture Description Language, ADL)**  
Bir mimariyi belgeleme gösterimi. ADL’ler tipik olarak bir mimariyi tanımlamak için hem grafik bir gösterim hem de (biçimsel olarak tanımlanmış) metinsel bir gösterim kullanır; esas olarak hesaplamaya yönelik (çalışma zamanı – runtime) bileşenleri, bunlar arasındaki etkileşimleri ve mimarinin özelliklerini tarif ederler.  

**Mimari Takas Analizi Yöntemi (Architecture Tradeoff Analysis Method, ATAM)**  
Senaryolar tarafından güdümlü, mimarileri analiz etmek için yerleşik bir yöntemdir. Amacı, kalite niteliği gereksinimleri ve iş hedefleri ışığında mimari kararların sonuçlarını değerlendirmektir.  

**ARID**  
Bkz. Ara Tasarımlar için Etkin İncelemeler (Active Reviews for Intermediate Design) yöntemi.  

**ASR**  
Bkz. Mimari açıdan önemli gereksinim (architecturally significant requirement).  

**ATAM**  
Bkz. Mimari Takas Analizi Yöntemi (Architecture Tradeoff Analysis Method).
