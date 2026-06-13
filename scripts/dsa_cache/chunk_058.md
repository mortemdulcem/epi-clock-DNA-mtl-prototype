Varsayım, izleme (monitoring) ve hata (exception) yönetiminin, doğru çalışmayı test etmek için yeterli bilgi sağlayacağı yönündedir.

Sistem etkin yedeklilik (active redundancy, hot spare) kullanıyor mu?  
Etkin yedeklilikte, bir koruma grubundaki (protection group) tüm düğümler (bir veya daha fazla düğümün “etkin” olduğu ve kalanların yedek yedekler olarak hizmet ettiği düğüm grubu) paralel olarak aynı girdileri alır ve işler; bu sayede yedek yedekler etkin düğüm(ler)le eşzamanlı durum (synchronous state) korur.

Y

H

Etkin yedeklilik, uygulama sunucusunda ve mesaj kuyruğunda kullanılmaktadır.

Etkin yedeklilik, zaman sunucularından toplanması gereken bilgilerin, sunucu hatası nedeniyle kaybedilmesi olasılığını azaltmak için pasif bir yaklaşıma kıyasla tercih edilmiştir. Bu, aslında QA-3’te belirlenmiş gereksinimi de aşmaktadır. Ayrıca, ortak kipli (common-mode) bir hata olmayacağını varsayıyoruz.
(devam ediyor)

183

N/A

8.4 Taktik Tabanlı Analiz (Tactics-Based Analysis)

Hatalardan
kurtarma
(hazırlık
ve onarım)

N

Risk

Tasarım Kararları ve Konumu

Gerekçe ve
Varsayımlar

184

Sistem pasif yedeklilik (passive redundancy, warm spare) kullanıyor mu?  
Pasif yedeklilikte, girdi trafiğini yalnızca koruma grubunun etkin üyeleri işler; görevlerinden biri de yedek yedeklere periyodik durum güncellemeleri sağlamaktır.

N

N/A

Etkin yedeklilik tercih edilmiştir.

N/A

Sistem, bir hata durumunda daha önce kaydedilmiş iyi bir duruma (“rollback line”) geri dönebilecek şekilde geri alma (rollback) kullanıyor mu?

Y

M

İşlem (transaction) yönetimi Spring çerçevesi (Spring framework) aracılığıyla desteklenmektedir.

Spring, bu sistemin ihtiyaç duyduğu türde işlemler için yeterli desteği sağlamaktadır.

Bölüm 8—Tasarım Sürecinde Analiz

Taktik
Grubu

Taktik Sorusu

Destekleniyor mu?
(Y/N)

8.5

Yansıtıcı Sorular (Reflective Questions)

185

Tablo 8.2’deki sorular bir görüşme ortamında kullanıldığında, mimarın görüşlerine göre sistemin mimarisi tarafından her bir taktiğin desteklenip desteklenmediğini kaydedebiliriz. Örneğin, tabloda yer alan sorular, Bölüm 4’te sunulan FCAPS sistemi için verilmiş tasarım kararları temel alınarak yanıtlanmıştır. Tabloda gösterilen cevapların oldukça kısa olduğuna dikkat edin; bunun nedeni bunun bir örnek olmasıdır; gerçek dünya uygulamalarında daha ayrıntılı açıklamalar teşvik edilir. Eğer mevcut bir sistemi analiz ediyorsak, ek olarak şu konuları da inceleyebiliriz:

§ Bu taktiğin kullanılmasında (ya da kullanılmamasında) herhangi bir bariz risk olup olmadığı. Taktiğin kullanıldığı durumda, burada sistemde nasıl gerçekleştirildiğini (örneğin özel yazılım kodu, çerçeveler (frameworks) ya da dışarıdan üretilmiş bileşenler aracılığıyla) kaydedebiliriz. Örneğin, etkin yedeklilik taktiğinin, uygulama sunucusunu ve veritabanı gibi diğer kritik bileşenleri çoğaltarak kullanıldığını (Bölüm 4’te sunulan durum çalışmasında olduğu gibi) not edebiliriz.  
§ Taktiği gerçekleştirmek için alınan belirli tasarım kararları ve gerçekleştirilmiş (realization) halinin kod tabanında (code base) nerede bulunabileceği. Bu bilgi, denetim (audit) ve mimari yeniden yapılandırma (architecture reconstruction) amaçları için yararlıdır. Bir önceki maddeyi örnekleyerek sürdürecek olursak, kaç adet uygulama sunucusu kopyası oluşturulduğunu ve bu kopyaların nerede konumlandığını (örneğin bir veri merkezinde aynı rafta, farklı raflarda, farklı veri merkezlerinde) sorgulayabiliriz.  
§ Bu taktiğin gerçekleştirilmesinde yapılan her türlü gerekçe veya varsayım. Örneğin, ortak kipli (common-mode) bir hatanın olmayacağını varsayabilir, bu yüzden kopyaların aynı donanım üzerinde çalışan, birbirinin aynı sanal makineler olmasını kabul edilebilir bulabiliriz.

Görüşme temelli bu yaklaşım kulağa basit gelebilir, ancak gerçekte oldukça güçlü ve ufuk açıcı olabilir. Bir mimar olarak günlük faaliyetlerinizde her zaman geri çekilip büyük resme bakmaya zaman ayırmayabilirsiniz. Tablo 8.2’de gösterilenler gibi bir dizi görüşme sorusu sizi tam da bunu yapmaya zorlar. Bu yaklaşım aynı zamanda oldukça verimlidir: Tek bir kalite niteliği (quality attribute) için tipik bir görüşme 30 ila 90 dakika sürer.

Yedi en önemli sistem kalite niteliğini—kullanılabilirlik (availability), birlikte işlerlik (interoperability), değiştirilebilirlik (modifiability), performans (performance), güvenlik (security), test edilebilirlik (testability) ve kullanılabilirlik (usability)—kapsayan taktik tabanlı soru kümeleri (questionnaire) Ek B’de bulunabilir. Ek olarak, diğer (daha temel) soru kümelerini bir araya getirerek, yeni bir kalite endişesi (quality concern) kümesini ele almak üzere yeni bir soru seti oluşturmanın nasıl yapılabileceğine örnek olarak, DevOps üzerine sekizinci bir soru kümesi de ekledik.

> **💬 Çevirmen notu:** Buradaki “soru kümesi (questionnaire)” ifadesi, her kalite niteliği için hazırlanmış yarı-yapılandırılmış görüşme formunu ifade ediyor; mimari inceleme sırasında sistematik olarak kullanılmak üzere tasarlanmışlardır.

8.5

Yansıtıcı Sorular (Reflective Questions)

Taktik temelli görüşmelere benzer şekilde, bazı araştırmacılar tasarımı desteklemek için yansıtıcı sorular sorma (ve yanıtlama) pratiğini savunmuştur. 

186

Bölüm 8—Tasarım Sürecinde Analiz
