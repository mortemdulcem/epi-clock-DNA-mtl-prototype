Bu bölümde tartışılan mimari tasarım yöntemleri aşağıdaki kaynaklarda bulunabilir:
- P. Eeles, P. Cripps. *The Process of Software Architecting*. Addison-Wesley Professional, 2009.
- C. Hofmeister, P. Kruchten, R. Nord, H. Obbink, A. Ran, P. America. “A General Model of Software Architecture Design Derived from Five Industrial Approaches”, *Journal of Systems and Software*, 80:106–126, 2007.
- A. Lattanze. *Architecting Software Intensive Systems: A Practitioner’s Guide*. CRC Press, 2009.
- P. Kruchten. *The Rational Unified Process: An Introduction*, 3. baskı, Addison-Wesley, 2003.
- Microsoft, *Application Architecture Guide*, 2. baskı. Microsoft Press, 2009.
- N. Rozanski, E. Woods. *Software Systems Architecture*. Addison Wesley, 2005.

# 8  
Tasarım Sürecinde Analiz

Her ne kadar bu kitap mimari tasarıma odaklanmış olsa da, tasarım ve analizin aynı madalyonun iki yüzü olduğuna her zaman inandık. Tasarım, karar verme sürecidir; analiz ise bu kararları anlamaya yönelik süreçtir ki böylece tasarım değerlendirilebilsin. Bu yakın ilişkiyi yansıtmak için, şimdi tasarım sürecinde mimari kararları neden, ne zaman ve nasıl analiz etmemiz gerektiğine odaklanıyoruz. Çeşitli analiz tekniklerine bakacağız, ne zaman uygulanabileceklerini tartışacağız ve maliyetlerini ve faydalarını inceleyeceğiz.

## 8.1  
Analiz ve Tasarım

Analiz, karmaşık bir varlığı anlamak amacıyla onu bileşen parçalarına ayırma sürecidir. Analizin karşıtı sentezdir. Dolayısıyla analiz ve tasarım iç içe geçmiş etkinliklerdir. Tasarım süreci boyunca, analiz etkinliği çeşitli yönlere gönderme yapabilir:

- Tasarlamak üzere olduğunuz çözümün hedeflediği problemi anlamak için tasarım sürecine giren girdileri incelemek. Bu, Bölüm 3.2.2’de tartışıldığı gibi sürücülere (drivers) öncelik verilmesini de içerir. Bu tür analiz, ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) 1. ve 2. adımlarında gerçekleştirilir.
- Bir tasarım problemini çözmek için belirlediğiniz alternatif tasarım kavramlarını inceleyerek en uygun olanı seçmek. Bu durumda analiz, seçimleriniz için somut kanıtlar sunmanızı zorlar. Bu etkinlik, ADD’nin 4. adımında gerçekleştirilir ve Bölüm 3.2.4’te tartışılmıştır.
- Tasarım süreci (veya bir yineleme) sırasında alınan kararların uygunluğunu güvence altına almak. Bu, ADD’nin 7. adımında gerçekleştirdiğiniz analiz türüdür.

Mimariyi tasarlarken aldığınız kararlar, yalnızca kalite niteliği (quality attribute) tepkilerini elde etmek açısından kritik değildir; çoğu zaman, bu kararları daha sonraki bir zamanda düzeltmenin maliyeti önemli derecede yüksek olabilir, çünkü bu kararlar sistemin birçok bölümünü etkileyebilir. Bu nedenlerle, sorunların tanımlanabilmesi, mümkünse nicelleştirilebilmesi ve hızlıca düzeltilebilmesi için tasarım sürecinde analiz yapılması gereklidir. Unutmayın, fazla özgüvenli olmak ve içgüdülerinizi takip etmek en iyi fikir olmayabilir (bkz. kenar yazı “‘İnanıyorum’ Yeterince İyi Değil”). Neyse ki, bu noktaya kadar verdiğimiz önerileri takip ettiyseniz, tasarım sürecini yürütürken ürettiğiniz taslaklar ve görünümlerden (views) yararlanarak, analizi ya kendi başınıza ya da akranlarınızın yardımıyla yürütebiliyor olmalısınız.

### “‘İnanıyorum’ Yeterince İyi Değil”

Mimarinizi tasarlarken sistematik bir yaklaşım izliyor, yerleşik kaynaklardaki tasarım kavramlarını kullanıyor ve yapılarınızı temsil eden güzel görünümlü diyagramlara sahip olsanız bile, aldığınız kararların gerçekten belirli bir kalite niteliği senaryosunu (quality attribute scenario) tatmin edeceğini garanti eden hiçbir şey yoktur. Bazı kalite nitelikleri sisteminizin başarısı için kritiktir; özellikle bu tür kararlar söz konusu olduğunda “İnanıyorum” gerekçesi yeterince iyi değildir. Uygulamada çalışan yazılım mimarları üzerine yapılan çalışmalar, çoğunun tasarım kararlarını verirken “yeterlilik” yaklaşımını benimsediğini göstermiştir — yani ihtiyaçlarını karşıladığı ilk bakışta görünen kararı benimserler. Çoğu kez, bu kararları destekleyecek içgüdüleri, inançları ve (kaçınılmaz olarak sınırlı olan) deneyimleri dışında hiçbir gerekçeleri yoktur. Böylece, önemli kararlar çoğu kez yetersiz akıl yürütme sonrasında alınır; bu da bir sisteme risk katabilir.

Sisteminize kritik olan sürücüler (drivers) için, yalnızca içgüdünüze güvenmek, benzetmelere ve geçmişe dayanmak ya da sürücülerin karşılandığından emin olmak için birkaç yüzeysel test yapmak yerine, hem kendinize hem de kuruluşunuza daha ayrıntılı bir analiz yapma borcunuz vardır. Aşağıdaki seçenekler, analizinizin derinliğini artıracak ve böylece alınan kararlar için gerekçenizi güçlendirecektir:

- Analitik modeller (analytic models). Bu yerleşik matematiksel modeller, performans veya erişilebilirlik (availability) gibi kalite niteliklerini incelemenizi sağlar. Erişilebilirlik için Markov ve istatistiksel modelleri; performans için ise kuyruk (queuing) kuramı ve gerçek zamanlı çizelgeleme kuramını (real-time scheduling theory) içerirler. Analitik modeller — özellikle performansı ele alanlar — oldukça olgundur (mature), ancak yeterince kullanılabilmeleri için kayda değer eğitim ve öğrenim gerektirebilir.

> **💬 Çevirmen notu:** Buradaki “analitik modeller” ifadesiyle kastedilen, genellikle kapalı formüllere veya iyi tanımlanmış algoritmalara dayalı, önceden kanıtlanmış matematiksel model aileleridir; bunlar, kod yazmadan önce sistem davranışını yaklaşık olarak hesaplamaya yarar.
