## 3.8 Tasarım İlerleyişini İzleme

Nitelik temelli tasarım (Attribute-Driven Design, ADD) tasarımı sistematik biçimde yürütmek için açık yönergeler sağlasa da, tasarım ilerleyişini izlemek için bir mekanizma sunmaz. Oysa tasarım gerçekleştirirken yanıtlamak isteyeceğiniz birkaç soru vardır:

- Ne kadar tasarım yapmamız gerekiyor?
- Şu ana kadar ne kadar tasarım yaptık?
- Bitirdik mi?

Backlog’lar ve Kanban panoları gibi çevik (Agile) uygulamalar tasarım ilerleyişini izlemenize ve bu soruları yanıtlamanıza yardımcı olabilir. Bu teknikler elbette yalnızca çevik yöntemlerle sınırlı değildir. Herhangi bir yöntembilim (methodology) kullanan her geliştirme projesi, ilerleyişi izlemelidir.

### 3.8.1 Mimari Backlog Kullanımı

Mimari (veya tasarım) backlog kavramı birçok yazar tarafından önerilmiştir (Bkz. Bölüm 7.1). Bu kavram, Scrum gibi çevik geliştirme yöntemlerinde bulunan backlog’a benzer. Temel fikir, mimari tasarım sürecinin parçası olarak hâlâ gerçekleştirilmesi gereken bekleyen eylemlerin bir listesini oluşturmanız gerektiğidir.

Başlangıçta tasarım backlog’unu mimari sürücülerinizle (architectural driver) doldurmalısınız; ancak mimarinin tasarımını destekleyen diğer etkinlikler de dahil edilebilir. Örneğin:

- Belirli bir teknolojiyi sınamak veya belirli bir kalite niteliği (quality attribute) riskini ele almak için bir prototip oluşturma
- Mevcut varlıkların (asset) araştırılması ve anlaşılması (gerektiğinde tersine mühendislik (reverse engineering) yapılması)
- Tasarımın bir gözden geçirmesinde ortaya çıkarılan sorunlar
- Önceki bir yinelemede gerçekleştirilen kısmi tasarımın gözden geçirilmesi

Örneğin Scrum kullanırken, sprint backlog’u ile tasarım backlog’u birbirinden bağımsız değildir: Sprint backlog’undaki bazı özelliklerin gerçekleştirilmesi için mimari tasarım yapılması gerekebilir; dolayısıyla bunlar mimari tasarım backlog’una girecek maddeler oluştururlar. Bununla birlikte, bu iki backlog ayrı ayrı yönetilebilir. Tasarım backlog’u, genellikle müşteri (veya ürün sahibi) tarafından tartışılmayan ya da önceliklendirilmeyen çeşitli maddeler içerdiği için, dahili olarak bile yönetilebilir.

Ayrıca, kararlar alındıkça ek mimari kaygılar (architectural concern) ortaya çıkabilir. Örneğin bir referans mimari (reference architecture) seçerseniz, muhtemelen ona bağlı özel mimari kaygılar veya bunlardan türetilen kalite niteliği senaryolarını (quality attribute scenario, QAScenario) mimari tasarım backlog’una eklemeniz gerekecektir. Böyle bir kaygıya örnek olarak, bir web uygulaması referans mimarisinde oturumların yönetimi verilebilir.

### 3.8.2 Tasarım Kanban Panosu Kullanımı

Tasarım turlarla ve bu turlar içinde bir dizi yineleme (iteration) olarak yürütüldüğünden, tasarımın ilerleme derecesini izlemenin bir yoluna ihtiyaç duyarsınız. Ayrıca daha fazla tasarım kararı almaya (yani ek yinelemeler gerçekleştirmeye) devam etmeniz gerekip gerekmediğine de karar vermelisiniz. Bu görevi kolaylaştırmak için kullanılabilecek araçlardan biri, Şekil 3.6’da gösterilene benzer bir Kanban panosudur.

Tasarım turunun başında, tasarım sürecine giren girdiler backlog’da birer madde haline gelir. Başlangıçta bu etkinlik ADD’in 1. adımında gerçekleşir; bu tasarım turu için backlog’unuzdaki farklı maddeler, (önceki tasarım turlarında sonuçlandırılmamış ve bu turda ele almak istediğiniz girdiler hariç) panonun “Henüz Ele Alınmadı (Not Yet Addressed)” sütununa eklenmelidir. ADD’in 2. adımında bir tasarım yinelemesine başladığınızda, tasarım yinelemesinin hedefi kapsamında ele almayı planladığınız sürücülere karşılık gelen backlog girdileri “Kısmen Ele Alındı (Partially Addressed)” sütununa taşınmalıdır. Son olarak, bir yinelemeyi tamamladığınızda ve tasarım kararlarınızın analizi belirli bir sürücünün ele alındığını ortaya koyduğunda (ADD’in 7. adımı), ilgili girdi panonun “Tamamen Ele Alındı (Completely Addressed)” sütununa taşınmalıdır. Bir sürücünün “Tamamen Ele Alındı” sütununa taşınmasına olanak verecek açık ölçütler belirlemek önemlidir (bunu Scrum’da kullanılan “Bitti Tanımı (Definition of Done)”na benzer “Ele Alındı Tanımı (Definition of Addressed)” ölçütleri olarak düşünün).

Bir ölçüt, örneğin, sürücünün analiz edilmiş olması veya bir prototipte uygulanmış olması olabilir. Ayrıca, belirli bir yineleme için seçilen sürücüler, o yineleme kapsamında tamamen ele alınamayabilir; bu durumda “Kısmen Ele Alındı” sütununda kalmalıdırlar ve sonraki yinelemelere hazırlanırken bu sürücülerin, o anda var olan öğelere (mimari öğelere) nasıl tahsis edilebileceğini (allocation) düşünmelisiniz.

Panodaki girdileri önceliklerine göre ayırt etmenizi sağlayacak bir teknik seçmek faydalı olabilir. Örneğin, önceliğe bağlı olarak farklı renklerde Post-it notlar kullanabilirsiniz.

Böyle bir panoyla, (en önemli) sürücülerin kaç tanesinin o tasarım turunda ele alınmakta olduğunu veya ele alınmış olduğunu hızlıca görebildiğiniz için tasarımın ilerleyişini görsel olarak izlemek kolaydır. Bu teknik, ek yinelemeler yapmanız gerekip gerekmediğine karar vermenize de yardımcı olur; ideal olarak tasarım turu, sürücülerin çoğunluğu (ya da en azından en yüksek öncelikli olanları) “Tamamen Ele Alındı” sütununun altında yer aldığında sonlandırılır.

> **💬 Çevirmen notu:** Buradaki Kanban panosu, klasik “To Do / In Progress / Done” düzeninin, mimari sürücüler ve ADD adımlarıyla uyarlanmış hâli gibi düşünülebilir; amaç, özellikle mimari seviyedeki ilerlemeyi şeffaflaştırmaktır.
