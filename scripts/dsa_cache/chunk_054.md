171

Bu beş ana adıma ek olarak, Microsoft ekibinin ele aldığı teknik, mimarinin gözden geçirilmesini ve tasarımın temsil edilmesi ile iletişimini önermektedir. Bu teknik belirli bir geliştirme sürecinden bağımsızdır ve yalnızca, Çevik (Agile) bir süreç kullanıldığında yinelemelerin mimari ve geliştirme faaliyetlerini birleştirmesi gerektiğine dair bir öneri sunar.

Microsoft ekibinin sunduğu teknik çok ayrıntılı değildir; ancak bu tekniğin tartışılması Microsoft’un kitabının yalnızca küçük bir bölümünü oluşturur. Kitabın geri kalanı, web, zengin istemci (rich client), zengin internet (rich internet) ve mobil uygulamalar gibi farklı türdeki uygulamalar için dikkate alınması gereken hususlar hakkında pragmatik ve ayrıntılı bilgiler sağlar. Örneğin, kitap iş katmanının (business layer) tasarımına özgü yönlere ayrılmış bir bölüme sahiptir. Bilgilerin önemli bir kısmı teknoloji bağımsız olsa da, Microsoft kendi teknolojilerinin bu süreçte nasıl kullanılabileceğini göstermek konusunda da son derece iyi bir iş çıkarmıştır. Ayrıca, kitap bir dizi referans mimari (reference architecture) için ele alınması gereken kaygılar hakkında kapsamlı bir tartışma sunar.

Bu teknik amaç bakımından ADD’ye (Attribute-Driven Design, nitelik temelli tasarım) benzer, ancak gerçek tasarım adımlarının nasıl uygulanacağı açısından daha az ayrıntılıdır. ADD bir alternatif olarak kullanılabilir, ancak Microsoft’un kitabını, tasarım sırasında ele almanız gereken pek çok somut mimari kaygıyı saptamak ve özellikle kitapta ele alınan uygulama türlerinden birini tasarlıyorsanız sunulan tüm pratik tavsiyelerden yararlanmak için elinizin altında bulundurmak iyi bir fikirdir. Microsoft’un kitabında sunulan fikirler, bu kitabın çeşitli yönlerini oluştururken bize ilham vermiştir.

## 7.6 Bakış Açısı ve Perspektif Yöntemi (Viewpoints and Perspectives Method)

Bakış açısı ve perspektif yöntemi, Nick Rozanski ve Eoin Woods tarafından yazılan *Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives* adlı kitapta açıklanmaktadır. Kitabın başlığında vurgulanan iki kritik kavram, bakış açıları (viewpoints) ve perspektiflerdir (perspectives); yazarlar bunları şu şekilde tanımlar:

- **Bakış açısı (viewpoint)**, bir tür görünüm (view) oluşturmaya yönelik desenler (patterns), şablonlar (templates) ve kurallar (conventions) koleksiyonudur. Bakış açısı, kaygıları bu bakış açısından yansıtılan paydaşları (stakeholders) ve bu bakış açısına ait görünümleri oluşturmak için kullanılacak yönergeleri, ilkeleri ve şablon modelleri tanımlar. Tanımlanan bakış açıları arasında işlevsel (functional), bilgi (information), eşzamanlılık (concurrency), geliştirme (development), dağıtım (deployment) ve işletimsel (operational) bakış açıları yer alır.
- **Mimari perspektif (architectural perspective)**, bir sistemin mimari görünümlerinin tamamı boyunca dikkate alınması gereken bir dizi kalite özelliğini (quality properties) sergilemesini sağlamak için kullanılan etkinlikler, taktikler (tactics) ve yönergeler koleksiyonudur. Rozanski ve Woods’un kitabında ele alınan başlıca perspektifler güvenlik (security), performans ve ölçeklenebilirlik (performance and scalability), kullanılabilirlik ve dayanıklılık (availability and resilience) ile evrim (evolution) perspektifleridir.

> **💬 Çevirmen notu:** Rozanski & Woods yaklaşımında “viewpoint” bir çeşit “görünüm türü” için tarif seti, “perspective” ise kalite niteliklerini o türlerin tümü boyunca ele alan enine bir kaygı kümesi olarak düşünülebilir. Bu, kitapta ADD’deki senaryo ve taktik kavramlarıyla ilişkilendiriliyor.

Perspektifler, belirli bir perspektifin farklı bakış açılarında uygulanabilmesi nedeniyle bakış açılarına ortogonaldir (orthogonal). Örneğin, güvenlik perspektifi; işlevsel, bilgi ve işletimsel bakış açılarındaki unsurları içerir.

Mimari, Şekil 7.6’da gösterilen mimari tanımlama sürecinde oluşturulur. Bu süreçteki adımlar aşağıda özetlenmiştir:

1. **Girdileri birleştirin.** İlk girdileri anlayın, doğrulayın ve iyileştirin.
2. **Senaryoları belirleyin.** Sistemin en önemli gereksinimlerini örnekleyen bir dizi senaryo belirleyin.
3. **İlgili mimari stilleri belirleyin.** Sistemin genel organizasyonu için temel olarak kullanılabilecek bir ya da daha fazla kanıtlanmış mimari stili belirleyin.
4. **Aday bir mimari üretin.** Sistemin başlıca kaygılarını (gereksinimler ve hedefler) yansıtan ve daha ileri mimari değerlendirme ve iyileştirmeye temel oluşturabilecek ilk taslak mimariyi oluşturun.
5. **Mimari seçenekleri keşfedin.** Sistem için çeşitli mimari olasılıkları inceleyin ve bunlar arasından seçim yapmak için temel kararları alın.
6. **Mimariyi paydaşlarla değerlendirin.** Mimariyi kilit paydaşlarınızla birlikte bir değerlendirmeden geçirin, sorunları veya eksiklikleri yakalayın ve mimari için paydaşların onayını alın.
7. Bu noktada iki adım paralel olarak yürütülür:  
   A. **Mimariyi yeniden çalışın.** Değerlendirme sırasında ortaya çıkan tüm kaygıları ele alın.  
   B. **Gereksinimleri yeniden gözden geçirin.** Mimari değerlendirmeler ışığında, sistemin özgün gereksinimlerinde yapılması gerekebilecek değişiklikleri değerlendirin.

Bu yöntem, mimari stillerden elde edilen ya da en azından onlara dayanan bir aday mimari oluşturulmasını önermektedir. Bu aday mimari, bir değerlendirme yapıldıktan sonra kabul edilebilir görülene dek bir dizi yineleme yoluyla daha da iyileştirilir.

ADD ile karşılaştırıldığında, bu yöntem 4. ve 5. adımların nasıl yürütüleceğine dair adım adım bir rehber sunmaz. Bununla birlikte, bu yaklaşımın bir faydası, tanımladığı altı bakış açısının bizim yaklaşımımızdaki genel mimari kaygılarla ilişkilendirilebilmesidir. Ayrıca, taktikler ile perspektifler ilişkilidir ve perspektiflerin farklı bakış açıları boyunca uygulanması fikri değerlidir; senaryo temelli bir yaklaşıma da tamamlayıcı olabilir. Örneğin, sürücüler (drivers) listenizde yalnızca bir güvenlik senaryosu varsa, yalnızca bu belirli senaryoyu destekleyen öğeleri dikkate alabilirsiniz. Oysa bir güvenlik perspektifini düşünmek, doğrudan bu belirli senaryoyla ilişkili olmayıp dağıtım (deployment) veya işletim (operation) gibi farklı kaygı alanlarına yayılan güvenlikle ilgili tasarım kararları alırken yararlı olabilir.

## 7.7 Özet

Bu bölümde çeşitli tasarım yöntemlerini inceledik ve bunları ADD ile karşılaştırdık. Görüldüğü gibi, seçebileceğiniz bir dizi yöntem mevcut. Peki neden bu alternatifler yerine, ya da onlara ek olarak, ADD’yi kullanmalısınız? Temel olarak, ADD mimari tasarım etkinliğini gerçekleştirmek için gerekli adımlar ve yönlendirmeler bakımından daha somut ve özeldir. Buraya kadar okuduğunuza göre, muhtemelen buna ikna olmuş olmalısınız.

ADD özellikle tasarıma odaklanır ve bu nedenle (geleceğin) mimarına daha ayrıntılı bir rehberlik sunar. Bu, ADD’nin bir zayıflığı değildir. Diğer birçok yöntem mimari yaşam döngüsünün diğer evrelerinde size rehberlik edebilir; örneğin, mimari gereksinimlerin ortaya çıkarılması ve önceliklendirilmesi için QAW (Quality Attribute Workshop), bir mimarinin analiz edilmesi için ATAM (Architecture Tradeoff Analysis Method), bir mimarinin dokümantasyonu için Views and Beyond tekniği. Bu kitapta, bu tür yöntemlerin ADD ile nasıl sorunsuz şekilde bütünleştirilebileceğini çeşitli bölümlerde tartıştık.

Tüm açıklığıyla belirtmek gerekirse, ADD 3.0 bu bölümde anlatılan tüm yaklaşımlardan esinlenmiş, onlardan yararlanmış ve onlara bir teşekkür borçludur.

## 7.8 Ek Okuma (Further Reading)
