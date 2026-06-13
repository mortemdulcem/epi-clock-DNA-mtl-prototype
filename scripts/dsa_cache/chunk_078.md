Erişimi iptal etmeyi sistem destekliyor mu?  
Buna bir örnek, bir saldırıdan şüphelenildiğinde, normalde meşru olan kullanıcılar ve kullanımlar için bile hassas kaynaklara erişimin sınırlandırılmasıdır.

15  

Erişimi kilitlemeyi sistem destekliyor mu?  
Buna bir örnek, bir kaynağa erişmek için tekrarlanan başarısız denemeler olduğunda o kaynağa erişimin sınırlandırılmasıdır.

16  

Aktörleri bilgilendirmeyi sistem destekliyor mu?  
Buna bir örnek, bir saldırıdan şüphelenildiğinde veya saldırı tespit edildiğinde operatörlerin, diğer personelin ya da iş birliği yapan sistemlerin bilgilendirilmesidir.

17  

Saldırılardan
kurtulma

Sistem bir denetim izi (audit trail) tutmayı destekliyor mu?  
Buna bir örnek, bir saldırganın eylemlerini geriye dönük izleyebilmek ve kimliğini belirleyebilmek için kullanıcı ve sistem eylemlerinin ve bunların etkilerinin kaydının tutulmasıdır.

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Güvenlik

259  

Gerekçe ve
Varsayımlar

260  

Ek B—Taktik Tabanlı Anketler

## B.7 Test Edilebilirlik (Testability)

| # | Taktik Grubu                        | Taktik Sorusu |
|---|-------------------------------------|---------------|
| 1 | Sistem durumunu denetle ve gözle (control and observe system state) | Sistem ya da sistem bileşenleri test etmeyi ve izlemeyi kolaylaştırmak için özelleşmiş arayüzler sağlıyor mu? |

2  

Sistem, bir arayüzü geçen bilginin daha sonra test amaçlı kullanılabilmesi için kaydedilmesini sağlayan mekanizmalar sunuyor mu (kayıt/oynatma – record/playback)?

3  

Sistemin, alt sistemin ya da modüllerin durumu, test etmeyi kolaylaştırmak için tek bir yerde saklanıyor mu (yerelleştirilmiş durum depolama – localized state storage)?

4  

Veri kaynaklarını soyutlayabiliyor musunuz; örneğin, arayüzleri soyutlayarak? Arayüzleri soyutlamak, test verisini daha kolay ikame etmenize olanak tanır.

5  

Sistem, deney yapmak veya test etmek için, deneyin sonuçlarını geri almaktan endişe etmeden, yalıtılmış (sandbox) biçimde çalıştırılabiliyor mu?

6  

Sistemin, bir programın ne zaman ve nerede hatalı bir durumda olduğunu belirtmek için yürütülebilir iddialar (executable assertions) kullanan kodu var mı?

7  

### Karmaşıklığı sınırla

Sistem, yapısal karmaşıklık sınırlı olacak şekilde tasarlandı mı?  
Örnekler: döngüsel bağımlılıklardan kaçınma, bağımlılıkları azaltma ve bağımlılık enjeksiyonu (dependency injection) gibi tekniklerin kullanılması.

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

### B.8 Kullanılabilirlik (Usability)

| # | Taktik Grubu | Taktik Sorusu |
|---|--------------|---------------|
| 8 |              | Sistem, belirlenimsizliğin (nondeterminism) az sayıda veya hiç kaynağını içeriyor mu? Bu, kısıtsız paralellikten (unconstrained parallelism) kaynaklanan davranışsal karmaşıklığı sınırlandırmaya yardımcı olur; bu da test etmeyi basitleştirir. |

## B.8 Kullanılabilirlik (Usability)

| # | Taktik Grubu                  | Taktik Sorusu |
|---|------------------------------|---------------|
| 1 | Kullanıcı inisiyatifini destekleme (supporting user initiative) | Sistem, işlemleri iptal etmeyi destekliyor mu? |

2  

Sistem, işlemleri geri almayı (undo) destekliyor mu?

3  

Sistem, işlemlerin duraklatılıp (pause) daha sonra devam ettirilmesini destekliyor mu?  
Örneğin, bir web tarayıcısında bir dosya indirmesini duraklatmak ve kullanıcının tamamlanmamış (ve başarısız olmuş) bir indirmeyi yeniden denemesine izin vermek.

4  

Sistem, işlemlerin nesne gruplarına uygulanmasını (birleştirme – aggregation) destekliyor mu?  
Örneğin, bir dosya gezgini penceresinde seçili bir dizi dosyanın toplam boyutunu görmenize izin veriyor mu?

Destekleniyor mu?
(E/H)

(Devam eder)

261  

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

262  

Ek B—Taktik Tabanlı Anketler

| # | Taktik Grubu                 | Taktik Sorusu |
|---|-----------------------------|---------------|
| 5 | Sistem inisiyatifini destekleme (support system initiative) | Sistem, kullanıcının yürüttüğü görevlere dayanarak (bir görev modeli – task model – tutarak) kullanıcıya yardım sağlıyor mu? Örnekler şunlardır:  |

- Girdi verisinin doğrulanması  
- Kullanıcı arayüzündeki (UI) değişikliklere kullanıcının dikkatinin çekilmesi  
- UI tutarlılığının korunması  
- UI’nin sağladığı işlevleri bulmalarına yardımcı olmak için kullanıcıya araç çubukları ve menüler eklenmesi  
- Kullanıcıların temel kullanıcı senaryolarını gerçekleştirmelerinde onlara yol göstermek için sihirbazlar (wizards) veya diğer tekniklerin kullanılması  

6  

Sistem, kullanıcı sınıfına göre UI’de ayarlamalar yapmayı (bir kullanıcı modeli – user model – tutarak) destekliyor mu?  
Örnekler arasında UI özelleştirmesini (yerelleştirme – localization dahil) ve erişilebilirlik desteğini sağlamak yer alır.

7  

Sistem, sistem özelliklerine dayanarak (bir sistem modeli – system model – tutarak) kullanıcıya uygun geri bildirim sağlıyor mu?  
Örnekler şunlardır:

- Uzun süren istekler işlenirken kullanıcıyı engellemekten kaçınmak  
- Eylem ilerlemesine ilişkin geri bildirim sağlamak (örn. ilerleme çubukları – progress bars)  
- Hataları yöneterek, hassas verileri açığa çıkarmadan kullanıcı dostu hata mesajları göstermek  
- Ekran boyutu ve çözünürlüğe göre UI’yi ayarlamak  

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Gerekçe ve
Varsayımlar

## B.9 DevOps

| # | Taktik Grubu | Taktik Sorusu |
|---|--------------|---------------|
| 1 | Test edilebilirlik: sistem durumunu denetle ve gözle (Testability: control and observe system state) | Sistem ya da sistem bileşenleri test etmeyi ve izlemeyi kolaylaştırmak için özelleşmiş arayüzler sağlıyor mu? |

2  

Sistem, bir arayüzü geçen bilginin daha sonra test amaçlı kullanılabilmesi için kaydedilmesini sağlayan mekanizmalar sunuyor mu (kayıt/oynatma – record/playback)?

3  

Sistem, deney yapmak veya test etmek için, deneyin sonuçlarını geri almaktan endişe etmeden, yalıtılmış (sandbox) biçimde çalıştırılabiliyor mu?

4  

### Performans: kaynakları yönet (Performance: manage resources)

Sistem, kaynakları kesintisiz bir şekilde artırabiliyor mu (örneğin CPU, bellek, ağ bant genişliği)?

5  

Sistem eşzamanlılık (concurrency) ekleyebiliyor mu?  
Örneğin, daha fazla hizmet isteğinin aynı anda işlenebilmesi için paralel işlem akışlarının (parallel processing streams) kesintisiz şekilde eklenmesini destekliyor mu?

6  

Sistem, sık erişilen verilere yönelik paylaşım çatışmasını (contention) azaltmak için verinin birden çok kopyasını tutuyor mu (örneğin veritabanlarını çoğaltarak ya da önbellekler kullanarak)?

(Devam eder)

264  

Ek B—Taktik Tabanlı Anketler

7  

Sistem, sık erişilen hesaplama kaynaklarına yönelik paylaşım çatışmasını azaltmak için hesaplamaların birden çok kopyasını tutuyor mu (örneğin bir sunucu çiftliğinde – server farm – sunucu havuzu – server pool – bulundurarak)?

8  

Sistem, özellikle kıt kaynakları, açık bir zamanlama politikasına (scheduling policy) göre tahsis edilebilmeleri için zamanlıyor mu?

9  

### Performans: kaynak talebini denetle (Performance: control resource demand)

Sistem, hizmet isteklerine yanıt verme ek yükünü azaltıyor mu; örneğin aracıları kaldırarak veya kaynakları birlikte konumlandırarak (co-location)?

10  

Girdileriniz sürekli bir veri akışı ise, sistem örnekleme oranını yönetiyor mu?  
Yani, veri örneklemesini değişen oranlarda (ve buna eşlik eden doğruluk/özgünlük – accuracy/fidelity – değişimiyle) yapabilmeniz mümkün mü?

11  

Sistem, olaylara verdiği yanıtı izliyor ve sınırlandırıyor mu?  
Yani, sistem belirli bir zaman aralığında yanıt verdiği olay sayısını sınırlandırarak, gerçekten servis verdiği olaylar için öngörülebilir yanıtlar sağlamayı garanti altına alıyor mu?

12  

Sunulan hizmet için, mevcut kaynaklardan daha fazla istek olabileceği göz önünde bulundurulduğunda, sistem olayları önceliklendiriyor mu?

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

Gerekçe
ve
Varsayımlar

B.9  

13  

### Değiştirilebilirlik: bağımlılığı azalt (Modifiability: reduce coupling)

14  

Taktik Sorusu

Destekleniyor mu?
(E/H)

Risk

Tasarım
Kararları
ve
Konum

DevOps

265  

Gerekçe
ve
Varsayımlar
