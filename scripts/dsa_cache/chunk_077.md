Sistemde, anlamsal tutarlılığı (semantic coherence) artırmak tutarlı biçimde destekleniyor mu? Örneğin, bir modüldeki sorumluluklar aynı amaca hizmet etmiyorsa, bunların farklı modüllere yerleştirilmesi gerekir. Bu, yeni bir modül oluşturmayı veya bir sorumluluğu mevcut bir modüle taşımayı içerebilir.

3

Bağlılığı
(coupling)
azaltma

Sistem, işlevselliği tutarlı bir biçimde kapsülüyor mu (encapsulate)? Bu tipik olarak, incelenen işlevselliği yalıtmayı ve ona açık (explicit) bir arayüz tanıtmayı içerir.

Destekleniyor mu?
(E/H)

(devamı)

254

#

Ek B—Taktik Tabanlı Anketler

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| 4 | Sistem, modüllerin çok sıkı bir şekilde birbirine bağlanmasını engellemek için tutarlı biçimde bir aracı (intermediary) kullanıyor mu? Örneğin, A somut C işlevselliğini çağırıyorsa, A ile C arasında aracılık yapan soyut bir B tanıtabilirsiniz. |  |  |  |  |
| 5 | Modüller arasındaki bağımlılıkları sistematik bir şekilde kısıtlıyor musunuz? Yoksa herhangi bir sistem modülü, herhangi başka bir modülle serbestçe etkileşime girebiliyor mu? |  |  |  |  |
| 6 | İki veya daha fazla ilgisiz modül birlikte değiştiğinde—yani düzenli olarak aynı değişikliklerden etkilendiğinde—paylaşılan işlevselliği, ayrı bir modülde ortak kod olarak yalıtmak için düzenli olarak yeniden düzenleme (refactoring) yapıyor musunuz? |  |  |  |  |
| 7 | Birden fazla benzer hizmet sağladığınız durumlarda, sistem ortak hizmetleri soyutluyor mu (abstract)? Örneğin, bu teknik genellikle sisteminizi işletim sistemleri, donanımlar veya diğer ortam (environment) varyasyonları arasında taşınabilir kılmak istediğinizde kullanılır. |  |  |  |  |
| 8 | Bağlamayı (binding) erteleme | Sistem, önemli işlevselliğin bağlanmasını (binding) düzenli olarak erteliyor mu; böylece bu işlevsellik yaşam döngüsünde daha sonra, hatta belki de son kullanıcılar tarafından bile değiştirilebilir oluyor mu? Örneğin, sistemin işlevselliğini genişletmek için eklentiler (plug-ins), eklenti modülleri (add-ons) veya kullanıcı betikleme (user scripting) kullanıyor musunuz? |  |  |  |  |

B.5

B.5

#

1

257

Performans

Performans

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Kaynak talebini kontrol etme (control resource demand) | Girdileriniz sürekli bir veri akışıysa, sistem örnekleme oranını (sampling rate) yönetiyor mu? Yani, verileri farklı oranlarda örneklemek (ve buna bağlı doğruluk/sadakat değişiklikleriyle birlikte) mümkün mü? |  |  |  |  |
| 2 | Sistem, olay yanıtını (event response) izliyor ve sınırlandırıyor mu? Sistem, hizmet verilen olaylar için öngörülebilir yanıtlar sağlamak amacıyla, belirli bir zaman aralığında yanıt verdiği olay sayısını sınırlandırıyor mu? |  |  |  |  |
| 3 | Kullanılabilir kaynaklardan daha fazla hizmet isteğiniz olabileceği göz önüne alındığında, sistem olaylara öncelik veriyor mu? |  |  |  |  |
| 4 | Sistem, örneğin aracıları kaldırarak veya kaynakları birlikte konumlandırarak (co-locating) hizmet isteklerine yanıt verme ek yükünü (overhead) azaltıyor mu? |  |  |  |  |
| 5 | Sistem yürütme süresini (execution time) izleyip sınırlandırıyor mu? Daha genel olarak, hizmet isteklerine yanıt verirken harcanan herhangi bir kaynağın (ör. bellek, CPU, depolama, bant genişliği, bağlantılar, kilitler) miktarını sınırlandırıyor musunuz? |  |  |  |  |
| 6 | Kaynak verimliliğini artırıyor musunuz? Örneğin, gecikmeyi (latency) azaltmak ve iş hacmini (throughput) iyileştirmek için kritik alanlardaki algoritmaların verimliliğini düzenli olarak artırıyor musunuz? |  |  |  |  |

(devamı)

256

#

7

Ek B—Taktik Tabanlı Anketler

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Kaynakları yönetme (manage resources) | Sistem, kaynakları (ör. CPU, bellek, ağ bant genişliği) kesintisiz biçimde (seamlessly) artırabiliyor mu? |  |  |  |  |
| 8 | Sistem eşzamanlılık (concurrency) tanıtabiliyor mu? Örneğin, daha fazla hizmet isteğinin eşzamanlı olarak işlenebilmesi için paralel işlem akışlarının (parallel processing streams) kesintisiz eklenmesini destekliyor mu? |  |  |  |  |
| 9 | Sistem, sık erişilen veriler için çekişmeyi (contention) azaltmak amacıyla verilerin birden fazla kopyasını (ör. veritabanı çoğaltma veya önbellekler kullanarak) tutuyor mu? |  |  |  |  |
| 10 | Sistem, sık erişilen hesaplama kaynakları için çekişmeyi azaltmak amacıyla hesaplamaların birden fazla kopyasını (ör. bir sunucu çiftliğinde (server farm) sunucu havuzu tutarak) sürdürüyor mu? |  |  |  |  |
| 11 | Sistem kuyruk boyutlarını sınırlandırıyor mu? Yani, hizmet beklerken bir kuyruğa yerleştirilen olayların sayısını sınırlıyor musunuz? |  |  |  |  |
| 12 | Sistem kaynakları, özellikle de kıt (scarce) kaynakları, açık bir zamanlama (scheduling) politikasına göre tahsis edilebilmeleri için zamanlıyor mu (schedule)? |  |  |  |  |

B.6

B.6

#

1

Güvenlik

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Saldırıları tespit etme (detecting attacks) | Sistem, aktörlerin (actors) tanımlanmasını destekliyor mu? Örnek: Sisteme gelen herhangi bir dış girdinin kaynağını tanımlamak. |  |  |  |  |
| 2 | Sistem, aktörlerin kimlik doğrulamasını (authentication) destekliyor mu? Örnek: Bir aktörün (bir kullanıcı veya uzak bir bilgisayar) gerçekten iddia ettiği kişi veya varlık olduğunu güvence altına almak. |  |  |  |  |
| 3 | Sistem, mesaj bütünlüğünün (message integrity) doğrulanmasını destekliyor mu? Örnek: Mesajların, kaynak dosyaların, dağıtım dosyalarının ve yapılandırma dosyalarının bütünlüğünü doğrulamak için sağlama toplamı (checksum) veya özet değerleri (hash values) gibi tekniklerin kullanılması. |  |  |  |  |
| 4 | Sistem, mesaj gecikmelerinin tespitini destekliyor mu? Örnek: Bir mesajın iletilmesinin ne kadar sürdüğünü kontrol etmek. |  |  |  |  |
| 5 | Sistem, saldırıların tespitini (intrusion detection) destekliyor mu? Örnek: Bir sistemdeki ağ trafiğini veya hizmet isteği kalıplarını, bir veritabanında saklanan imzalar ya da bilinen kötü niyetli davranış kalıplarıyla karşılaştırmak. |  |  |  |  |
| 6 | Sistem, hizmet reddi (denial-of-service) saldırılarının tespitini destekliyor mu? Örnek: Sisteme gelen ağ trafiğinin kalıbını veya imzasını, bilinen hizmet reddi saldırılarının tarihsel profilleriyle karşılaştırmak. |  |  |  |  |

(devamı)

258

#

Ek B—Taktik Tabanlı Anketler

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| Saldırılara direnme (resisting attacks) | Sistem, aktörlerin yetkilendirilmesini (authorization) destekliyor mu? Örnek: Kimliği doğrulanmış bir aktörün veriye veya hizmetlere erişme ve bunları değiştirme hakkına sahip olduğundan emin olmak. |  |  |  |  |
| 8 | Sistem, erişimin sınırlandırılmasını (limiting access) destekliyor mu? Örnek: Bir sistemin hangi bölümlerine (işlemciler, bellek ve ağ bağlantıları gibi) kimlerin ve nelerin erişebileceğini kontrol etmek. |  |  |  |  |
| 9 | Sistem, maruziyetin sınırlandırılmasını (limiting exposure) destekliyor mu? Örnek: Bir sistemle ilgili gerçekleri gizleyerek (“security by obscurity”) veya kritik kaynakları bölüp dağıtarak (“tüm yumurtaları aynı sepete koyma” ilkesi) başarılı bir saldırı olasılığını azaltmak veya potansiyel zararın miktarını kısıtlamak. |  |  |  |  |
| 10 | Sistem, veri şifrelemeyi (data encryption) destekliyor mu? Örnek: Verilere ve iletişime bir tür şifreleme uygulamak. |  |  |  |  |
| 11 | Sistem girdiyi tutarlı, sistem çapında bir şekilde doğruluyor mu (input validation)? Örnek: Dış girdinin filtrelenmesi, kanonik hale getirilmesi (canonicalization) ve kaçış karakterleriyle işlenmesi (escaping) gibi işlemleri gerçekleştirmek için bir güvenlik çerçevesi (security framework) veya doğrulama sınıfı kullanmak. |  |  |  |  |

B.6

#

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konumu | Gerekçe ve Varsayımlar |
|-------------|---------------|--------------------------|------|-----------------------------|------------------------|
| 12 | Sistem tasarımı, varlıkların ayrımını (separation of entities) dikkate alıyor mu? Örnek: Farklı ağlara bağlı farklı sunucuların fiziksel olarak ayrılması, sanal makinelerin kullanımı veya “air gap” (fiziksel ağ yalıtımı). |  |  |  |  |
| 13 | Sistem, varsayılan ayarlardaki (default settings) değişiklikleri destekliyor mu? Örnek: Kullanıcıyı, varsayılan olarak atanmış ayarları değiştirmeye zorlamak. |  |  |  |  |
| 14 | Saldırılara tepki verme (reacting to attacks) |  |  |  |  |
