§ Mimari değerlendirme (architectural evaluation). Belgede olduğu gibi, projeniz önemsiz bir şey değilse, kendinize ve paydaşlarınıza (stakeholder) mimariyi değerlendirmeniz borcunuzdur; yani alınan kararların kritik gereksinimleri karşılamak için uygun olduğundan emin olmanız gerekir. Test etmeden kod teslim eder miydiniz? Elbette hayır. Benzer şekilde, tasarımı önce “test” etmeden mimariyi ayrıntılandırmak için neden muazzam kaynaklar harcayasınız? Bunu sistemi ilk kez oluştururken veya büyük bir yeniden yapılandırmadan (refactoring) geçirirken yapmak isteyebilirsiniz. Tipik olarak değerlendirme gayriresmî ve kurum içi yapılır, ancak gerçekten önemli projeler için, dış bir ekip tarafından resmî bir değerlendirme yapılması tavsiye edilir.

§ Mimari gerçekleştirim/uygunluk denetimi (architectural implementation/conformance checking). Son olarak, oluşturduğunuz (ve değerlendirdiğiniz) mimariyi gerçekleştirmelisiniz. Bir mimar olarak, sistem büyüdükçe ve gereksinimler evrildikçe tasarımı biraz ayarlamanız gerekebilir. Bu normaldir. Bu ince ayarların yanında, gerçekleştirim sırasında temel sorumluluğunuz, kodun tasarıma uygunluğunu (conformance) sağlamaktır. Geliştiriciler mimariyi sadakatle gerçekleştirmiyorlarsa, siz tasarlamış olduğunuz nitelikleri (qualities) baltalıyor olabilirler. Yine, diğer mühendislik alanlarında yapılanları düşünün. Yeni bir bina için beton temel döküldüğünde, bu temel üzerine oturacak bina, temel önce bir karot numunesi ile test edilmeden —yeterince güçlü, yeterince yoğun, suya ve gazlara karşı yeterince geçirimsiz vb. olup olmadığı kontrol edilmeden— inşa edilmez. Uygunluk denetimi olmaksızın, sonradan inşa edilen şeyin kalitesini güvence altına almanın bir yolu yoktur.

Şekil 1.1’de belirli bir yaşam döngüsü (life-cycle) yöntemini önermediğimizi unutmayın. <<precedes>> kalıp yargısı (stereotype) sadece, bir etkinlikte belirli bir çabanın harcanması gerektiği ve dolayısıyla daha sonraki bir etkinlikteki çabadan önce gelmesi gerektiği anlamına gelir. Örneğin, gereksinimler hakkında hiçbir fikriniz yoksa tasarım etkinliklerini gerçekleştiremezsiniz ve bazı tasarım kararları almadan da bir mimariyi değerlendiremezsiniz.

Bugün ticari yazılımların çoğu bir tür çevik (Agile) yöntem kullanılarak geliştirilir. Bu mimari etkinliklerin hiçbiri çevik uygulamalarla uyumsuz değildir. Bir yazılım mimarı için soru “Çevik mi yapmalıyım yoksa mimari mi?” değil, “Projeye başlamadan önce ne kadar mimari iş yapmalıyım, gereksinimler biraz netleşene kadar ne kadarını ertelemeliyim?” ve “Mimariyi ne kadarını, ne zaman resmî olarak belgelendirmeliyim?” sorularıdır. Çevik (Agile) ve mimari, pek çok yazılım projesi için gayet uyumlu yol arkadaşlarıdır.

Mimari tasarım ile çeşitli yazılım yaşam döngüsü yöntemleri ve süreç modelleri —yinelemeli (iterative) geliştirme dâhil— arasındaki ilişkiyi Bölüm 9’da tartışacağız.

## 1.3 Mimarın Rolü

Bir mimar “sadece” bir tasarımcıdan çok daha fazlasıdır. Bir veya daha fazla kişi tarafından üstlenilebilen bu rolün, başarılı olabilmesi için yerine getirilmesi gereken uzun bir görev, beceri ve bilgi listesi vardır. Bu önkoşullar şunları içerir:

- Liderlik: mentorluk, ekip oluşturma, vizyon belirleme, koçluk
- İletişim: hem teknik hem teknik olmayan, işbirliğini teşvik etme
- Müzakere: iç ve dış paydaşlarla ve onların çelişen ihtiyaç ve beklentileriyle başa çıkma
- Teknik beceriler: yaşam döngüsü (life-cycle) becerileri, teknolojilerde uzmanlık, sürekli öğrenme, kod yazma
- Proje becerileri: bütçeleme, personel, zamanlama yönetimi, risk yönetimi
- Analitik beceriler: mimari analiz (architectural analysis), proje yönetimi ve ölçüm için genel bir analiz zihniyeti (bkz. “Analizin Anlamı” kenar yazısı)

Başarılı bir tasarım, “duvarın üzerinden atılan” durağan bir belge değildir. Yani mimarlar sadece iyi tasarlamakla kalmamalı, aynı zamanda projeyle ilgili her yönün —fikir aşaması ve iş gerekçesinden tasarım ve oluşturma, işletim, bakım ve en sonunda emekliliğe kadar— ayrılmaz bir parçası olmalıdır.

### Analizin Anlamı

Merriam-Webster Sözlüğü’nde analysis kelimesi şu şekilde tanımlanır:

- Bir şeyin parçalarını, bunların ne yaptığını ve birbirleriyle nasıl ilişkili olduklarını öğrenmek için dikkatli biçimde incelenmesi
- Bir şeyin doğası ve anlamına dair bir açıklama

Bu kitapta analysis kelimesini farklı amaçlarla kullanıyoruz ve her iki tanım da geçerlidir. Örneğin, mimari değerlendirme (architectural evaluation) etkinliğinin bir parçası olarak, mevcut bir mimari, ilişkili sürücüleri (drivers) karşılamaya uygun olup olmadığını anlamak için analiz edilir. Tasarım süreci sırasında, girdiler tasarım kararları vermek için analiz edilir. Prototiplerin oluşturulması da bir analiz biçimidir. Aslında analiz, tasarım süreci için o kadar önemlidir ki, bu konuya yalnızca Bölüm 8’i ayırıyoruz. Orada ayrıca analiz ile değerlendirme arasındaki ilişkiyi daha ayrıntılı biçimde tartışıyoruz. Bu kitapta öncelikli odak noktamız, tasarım etkinliği, ona bağlı teknik beceriler ve bunların geliştirme yaşam döngüsüne entegrasyonudur. Bir mimarın hayatının diğer yönlerine daha kapsamlı bir yaklaşım için, Software Architecture in Practice veya Just Enough Software Architecture gibi daha genel bir yazılım mimarisi kitabını okumanızı öneririz.

> **💬 Çevirmen notu:** Burada “analysis” hem tasarım girdilerinin sistematik incelenmesi hem de mevcut mimarinin ölçülüp değerlendirilmesi anlamında, geniş bir şemsiye kavram olarak kullanılıyor.

## 1.4 ADD’nin Kısa Tarihçesi (A Brief History of ADD)
