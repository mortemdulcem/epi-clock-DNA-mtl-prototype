§ Kapsülle: Kapsülleme, bir modüle açık (explicit) bir arayüz kazandırır. Bu arayüz, bir API’yi ve “bir girdi parametresi üzerinde sözdizimsel bir dönüşüm gerçekleştirip bunu dahili bir temsile dönüştürmek” gibi buna bağlı sorumlulukları içerir.
§ Aracı kullan (use an intermediary): Sorumluluk A ile sorumluluk B arasında bir bağımlılık olduğunda (örneğin A’nın gerçekleştirilebilmesi için önce B’nin gerçekleştirilmesi gerekiyorsa), bu bağımlılık bir aracı kullanılarak kırılabilir.

### A.4 Taktikler (tactics)

§ Bağımlılıkları kısıtla (restrict dependencies): Belirli bir modülün etkileşime girdiği ya da bağımlı olduğu modülleri kısıtla.
§ Yeniden düzenle (refactor): İki modül, en azından kısmen birbirinin kopyası olduğu için aynı değişiklikten etkileniyorsa yeniden düzenleme yapılır.
§ Ortak servisleri soyutla (abstract common services): İki modül tam olarak aynı olmasa da benzer servisler sağlıyorsa, bu servisleri daha genel (soyut) bir biçimde yalnızca bir kez gerçekleştirmek maliyet açısından daha etkin olabilir.

#### Geç Bağla (Defer Binding)

§ Geç bağla (defer binding): Kararların geliştirme zamanından sonra bağlanmasına (kesinleştirilmesine) izin ver.

### A.4.4 Performans Taktikleri (Performance Tactics)

Şekil A.15, performansa ulaşmak için kullanılan taktikleri özetlemektedir.

#### Performans Taktikleri

Events  
Arrive  

Kaynak Talebini Denetle (Control Resource Demand)  

Kaynakları Yönet (Manage Resources)  

Örnekleme oranını yönet (Manage sampling rate)  

Kaynakları artır (Increase resources)  

Olay tepkisini sınırla (Limit event response)  

Eşzamanlılık (concurrency) ekle (Introduce concurrency)  

Olaylara öncelik ver (Prioritize events)  

Hesaplamaların birden çok kopyasını tut (Maintain multiple  
copies of computations)  

Ek yükü azalt (Reduce overhead)  

Yürütme sürelerini sınırla (Bound execution times)  

Verinin birden çok kopyasını tut (Maintain multiple  
copies of data)  

Kaynak verimliliğini artır (Increase resource  
efficiency)  

Kuyruk boyutlarını sınırla (Bound queue sizes)  

Kaynakları zamanla (Schedule resources)  

Response  
Generated  
within  
Time  
Constraints  

ŞEKİL A.15 Performans taktikleri

---

#### Kaynak Talebini Denetle (Control Resource Demand)

§ Örnekleme oranını yönet (manage sampling rate): Bir veri akışının yakalandığı örnekleme frekansını düşürmek mümkünse, talep azaltılabilir; ancak bu genellikle belirli bir doğruluk (fidelity) kaybı pahasına olur.
§ Olay tepkisini sınırla (limit event response): Olayları yalnızca belirli bir azami hıza kadar işle; böylece olaylar gerçekten işlendiğinde daha öngörülebilir bir işlemeyi güvence altına al.
§ Olaylara öncelik ver (prioritize events): Tüm olaylar aynı derecede önemli değilse, olayların ne kadar önemli olduklarına göre sıralandığı bir öncelik şeması uygulayabilirsin.
§ Ek yükü azalt (reduce overhead): Aracıların (modifiye edilebilirlik için önemlidir) kullanımı, bir olay akışını işlerken tüketilen kaynakları artırır; bunları kaldırmak gecikmeyi (latency) iyileştirir.
§ Yürütme sürelerini sınırla (bound execution times): Bir olaya yanıt vermek için kullanılan yürütme süresine bir sınır koy.
§ Kaynak verimliliğini artır (increase resource efficiency): Kritik alanlarda kullanılan algoritmaların iyileştirilmesi gecikmeyi azaltacaktır.

#### Kaynakları Yönet (Manage Resources)

§ Kaynakları artır (increase resources): Daha hızlı işlemciler, ek işlemciler, ek bellek ve daha hızlı ağlar, gecikmeyi azaltma potansiyeline sahiptir.
§ Eşzamanlılığı artır (increase concurrency): İstekler paralel işlenebiliyorsa, bloklanmış zaman azaltılabilir. Eşzamanlılık, farklı olay akışlarını farklı iş parçacıklarında (thread) işleyerek veya farklı etkinlik kümelerini işlemek için ek iş parçacıkları oluşturarak sağlanabilir.
§ Hesaplamaların birden çok kopyasını tut (maintain multiple copies of computations): Replikaların amacı, tüm hesaplamaların tek bir sunucuda gerçekleşmesi durumunda ortaya çıkacak çekişmeyi (contention) azaltmaktır.
§ Verinin birden çok kopyasını tut (maintain multiple copies of data): Verinin kopyalarını (bunlardan biri diğerinin alt kümesi olabilir) farklı erişim hızlarına sahip depolama birimleri üzerinde tut.
§ Kuyruk boyutlarını sınırla (bound queue sizes): Kuyruğa alınmış gelişlerin (arrivals) azami sayısını ve buna bağlı olarak bu gelişleri işlemekte kullanılacak kaynakları denetle.
§ Kaynakları zamanla (schedule resources): Bir kaynak için çekişme olduğunda, bu kaynağın zamanlanması gerekir.

### A.4.5 Güvenlik Taktikleri (Security Tactics)

Şekil A.16, güvenliğe ulaşmak için kullanılan taktikleri özetlemektedir.

#### Güvenlik Taktikleri

Attack  

Saldırıları Tespit Et (Detect Attacks)  

Saldırılara Diren (Resist Attacks)  

Saldırılara  
Tepki Ver (React to  
Attacks)  

Saldırılardan  
Kurtul (Recover  
from Attacks)  

İzinsiz girişi tespit et (Detect  
Intrusion)  

Aktörleri tanımla (Identify  
Actors)  

Erişimi geri al (Revoke  
Access)  

Denetim izi tut (Maintain  
Audit Trail)  

Servis kesintisini tespit et (Detect Service  
Denial)  

Aktörleri kimlik doğrulamasından geçir (Authenticate  
Actors)  

Bilgisayarı kilitle (Lock  
Computer)  

Mesaj bütünlüğünü doğrula (Verify Message  
Integrity)  

Aktörleri yetkilendir (Authorize  
Actors)  

Aktörleri bilgilendir (Inform  
Actors)  

Mesaj gecikmesini tespit et (Detect Message  
Delay)  

Erişimi sınırla (Limit Access)  

Bkz.  
Kullanılabilirlik (See  
Availability)  

Sistem  
Tespit Eder,  
Direnir,  
Tepki Verir  
veya Kurtulur (System  
Detects,  
Resists,  
Reacts,  
or Recovers)  

Maruziyeti sınırla (Limit Exposure)  
Veriyi şifrele (Encrypt Data)  

Girdiyi doğrula (Validate Input)  
Varlıkları ayır (Separate  
Entities)  
Varsayılan ayarları değiştir (Change Default  
Settings)  

ŞEKİL A.16 Güvenlik taktikleri

---

#### Saldırıları Tespit Et (Detect Attacks)

§ İzinsiz girişi tespit et (detect intrusion): Bir sistem içindeki ağ trafiği ya da servis istek desenlerini, bir veritabanında saklanmış bir dizi imza ya da bilinen kötü niyetli davranış desenleriyle karşılaştır.
§ Servis kesintisini tespit et (detect service denial): Bir sisteme gelen ağ trafiğinin desenini ya da imzasını, bilinen servis reddi (denial-of-service, DoS) saldırılarının tarihsel profilleriyle karşılaştır.
§ Mesaj bütünlüğünü doğrula (verify message integrity): Mesajların, kaynak dosyalarının, dağıtım (deployment) dosyalarının ve yapılandırma dosyalarının bütünlüğünü doğrulamak için sağlama toplamı (checksum) ya da hash değeri gibi teknikler kullan.
§ Mesaj gecikmesini tespit et (detect message delay): Bir mesajın iletilmesinin ne kadar sürdüğünü kontrol ederek, şüpheli zamanlama davranışı tespit etmek mümkündür.

#### Saldırılara Diren (Resist Attacks)

§ Aktörleri tanımla (identify actors): Sisteme yapılan herhangi bir harici girdinin kaynağını belirle.
§ Aktörleri kimlik doğrulamasından geçir (authenticate actors): Bir aktörün (kullanıcı ya da uzak bir bilgisayar) gerçekten iddia ettiği kişi/varlık olduğundan emin ol.
§ Aktörleri yetkilendir (authorize actors): Kimliği doğrulanmış bir aktörün, veriye veya servislere erişme ve bunları değiştirme hakkına sahip olduğundan emin ol.
§ Erişimi sınırla (limit access): İşlemciler, bellek ve ağ bağlantıları gibi bir sistemin hangi kısımlarına kimlerin ve nelerin erişebileceğini denetle.
§ Maruziyeti sınırla (limit exposure): Örneğin bir sistemle ilgili gerçekleri gizleyerek (“security by obscurity”) ya da kritik kaynakları bölüp dağıtarak (“bütün yumurtalarını aynı sepete koyma”), başarılı bir saldırının olasılığını azalt veya potansiyel hasarın miktarını sınırla.
§ Veriyi şifrele (encrypt data): Veriye ve iletişime (communication) bir tür şifreleme uygula.
§ Girdiyi doğrula (validate input): Bir kullanıcıdan veya harici bir sistemden gelen girdiyi, sisteme kabul etmeden önce doğrula.
§ Varlıkları ayır (separate entities): Farklı ağlara bağlı farklı sunucular üzerinde fiziksel ayrım, sanal makineler veya “air gap” kullan.
§ Varsayılan ayarları değiştir (change default settings): Kullanıcıyı, varsayılan olarak atanmış ayarları değiştirmeye zorla.

#### Saldırılara Tepki Ver (React to Attacks)

§ Erişimi geri al (revoke access): Bir saldırıdan şüphelenildiğinde, normalde meşru kullanıcılar ve kullanım durumları için bile hassas kaynaklara erişimi sınırla.
§ Bilgisayarı kilitle (lock computer): Bir kaynağa erişmek için tekrarlanan başarısız girişimler varsa, bu kaynağa erişimi sınırla.
§ Aktörleri bilgilendir (inform actors): Bir saldırıdan şüphelenildiğinde veya saldırı tespit edildiğinde, operatörleri, diğer personeli veya işbirliği yapan sistemleri bilgilendir.

#### Saldırılardan Kurtul (Recover from Attacks)

Başarısız olan kaynakların kurtarılması için kullanılabilirlik taktiklerine ek olarak, saldırılardan kurtulmak için bir denetim (audit) gerçekleştirilebilir.

§ Denetim izi tut (maintain audit trail): Bir saldırganın eylemlerinin izini sürmeye ve onu tanımlamaya yardımcı olmak için, kullanıcı ve sistem eylemlerinin ve bunların etkilerinin kaydını tut.

### A.4.6 Test Edilebilirlik Taktikleri (Testability Tactics)

Şekil A.17, test edilebilirliğe ulaşmak için kullanılan taktikleri özetlemektedir.

#### Test Edilebilirlik Taktikleri

Sistem Durumunu Denetle ve Gözle (Control and Observe  
System State)  

Tests  
Executed  

Karmaşıklığı sınırla (Limit Complexity)  

Özel amaçlı  
arayüzler (Specialized  
Interfaces)  

Yapısal karmaşıklığı sınırla (Limit Structural  
Complexity)  

Kayıt/geri oynatma (Record/  
Playback)  

Belirsizliği (nondeterminism) sınırla (Limit  
Nondeterminism)  

Faults  
Detected  

Durum saklamayı yerelleştir (Localize State  
Storage)  
Veri kaynaklarını soyutla (Abstract Data  
Sources)  
Korumalı alan (sandbox) (Sandbox)  
Çalıştırılabilir savlar (executable assertions) (Executable  
Assertions)  

ŞEKİL A.17 Test edilebilirlik taktikleri

---

#### Sistem Durumunu Denetle ve Gözle (Control and Observe System State)
