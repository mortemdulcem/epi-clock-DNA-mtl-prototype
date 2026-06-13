## B.2 Kullanılabilirlik (Availability)

### Hataları Tespit Et (detect faults)

**Taktik Soru 2**

Sistem, sistemin diğer parçalarının sağlık durumunu izlemek için bir bileşen kullanıyor mu?  
Bir sistem monitörü (system monitor), ağda veya hizmet reddi (denial-of-service) saldırısı gibi diğer paylaşılan kaynaklarda meydana gelen arıza veya tıkanıklığı tespit edebilir.

**Taktik Soru 3**

Sistem, bir bileşenin ya da bağlantının arızasını veya ağ tıkanıklığını tespit etmek için kalp atışı (heartbeat) kullanıyor mu — yani bir sistem monitörü ile bir süreç arasında periyodik ileti alışverişi?

**Taktik Soru 4**

Sistem, dağıtık sistemlerdeki yanlış olay sıralarını tespit etmek için zaman damgası (time stamp) kullanıyor mu (Bölüm A.4.1’deki gibi)?

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

**Taktik Soru 5**

Sistem herhangi bir akıl sağlığı kontrolü (sanity checking) yapıyor mu: Bir bileşenin işlemlerinin veya çıktılarının geçerliliğini ya da makullüğünü denetlemek gibi?

**Taktik Soru 6**

Sistem, bir süreçte veya aygıtta koşul izleme (condition monitoring) yapıyor mu, ya da tasarım sırasında yapılmış varsayımları doğruluyor mu?

**Taktik Soru 7**

Sistem, çoğaltılmış bileşenlerin aynı sonuçları ürettiğini kontrol etmek için oylama (voting) kullanıyor mu? Çoğaltılmış bileşenler özdeş kopyalar, işlevsel olarak yedek (functionally redundant) veya analitik olarak yedek (analytically redundant) olabilir.

**Taktik Soru 8**

Sistem, normal yürütme akışını değiştiren bir sistem durumunu tespit etmek için istisna tespiti (exception detection) kullanıyor mu (örneğin sistem istisnası, parametre sınırı, parametre tür denetimi, zaman aşımı)?

**Taktik Soru 9**

Sistem, kendi doğru çalışmasını test etmek için öz test (self-test) yapabiliyor mu?

---

### Hatalardan Kurtul (Recover from faults)  
*(hazırlık ve onarım — preparation and repair)*

Kullanılabilirlik

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

**Taktik Soru 10**

Sistem, etkin yedeklilik (active redundancy, hot spare) kullanıyor mu?  
Etkin yedeklilikte, koruma grubundaki (protection group — bir veya daha fazla düğümün “aktif” olduğu, geri kalanların yedek parça (spare) olarak hizmet verdiği düğüm grubu) tüm düğümler, aynı girdileri paralel olarak alır ve işler; bu da yedek parçaların aktif düğüm(ler) ile eşzamanlı durum (synchronous state) tutmasını sağlar.

**Taktik Soru 11**

Sistem, pasif yedeklilik (passive redundancy, warm spare) kullanıyor mu?  
Pasif yedeklilikte, koruma grubunun yalnızca aktif üyeleri girdi trafiğini işler; görevlerinden biri de yedek parçalara periyodik durum güncellemeleri sağlamaktır.

---

### Ekler B — Taktik Temelli Anketler

**Taktik Soru 12**

Sistem, yedek parçalar (spares, cold spares) kullanıyor mu?  
Burada, bir koruma grubunun yedek parçaları, bir devretme (failover) gerçekleşene kadar hizmet dışı durumda kalır; bu noktada, yedek parçanın hizmete alınmasından önce, üzerinde bir açılış-sıfırlama (power-on-reset) prosedürü başlatılır.

**Taktik Soru 13**

Sistem, hatalarla başa çıkmak için istisna işleme (exception handling) kullanıyor mu? Tipik olarak, işleme ya hatanın raporlanmasını ya da ele alınmasını içerir; bu, istisnanın nedenini düzelterek ve yeniden deneyerek hatayı maskeleyebilmeyi de içerebilir.

**Taktik Soru 14**

Sistem, bir hata durumunda daha önce kaydedilmiş iyi bir duruma (geri alma çizgisi — “rollback line”) dönebilmesini sağlamak için geri alma (rollback) kullanıyor mu?

**Taktik Soru 15**

Sistem, yürütülebilir kod imajlarına hizmet kesintisine yol açmadan (non-service-affecting manner) hizmet içi yazılım güncellemesi (in-service software upgrade) gerçekleştirebiliyor mu?

**Taktik Soru 16**

Sistem, bileşen veya bağlantı arızasının geçici olabileceği durumlarda sistematik olarak yeniden deneme (retry) yapıyor mu?

**Taktik Soru 17**

Sistem, hatalı davranışı basitçe yok sayabiliyor mu (örneğin, bir kaynaktan gelen mesajların asılsız/sahte (spurious) olduğu belirlendiğinde bu mesajları yok saymak)?

**Taktik Soru 18**

Sistem, kaynaklar tehlikeye girdiğinde bir bozunma (degradation) politikası uyguluyor mu; bileşen arızaları varlığında en kritik sistem işlevlerini sürdürüp, daha az kritik işlevleri bırakacak şekilde?

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

**Taktik Soru 19**

Sistem, arıza sonrasında yeniden yapılandırma (reconfiguration) için tutarlı politika ve mekanizmalara sahip mi; çalışır durumda kalan kaynaklara sorumlulukları yeniden atarken olabildiğince fazla işlevselliği koruyacak şekilde?

**Taktik Grubu: Hatalardan Kurtul (faults’tan kurtulma)**  
*(yeniden devreye alma — reintroduction)*

**Taktik Soru 20**

Sistem, daha önce arızalanmış veya hizmet içi güncellenmiş bir bileşeni, bileşeni yeniden aktif rolüne döndürmeden önce tanımlı bir süre için “gölge kip”te (shadow mode) çalıştırabiliyor mu?

**Taktik Soru 21**

Sistem etkin veya pasif yedeklilik kullanıyorsa, durum yeniden eşleme (state resynchronization) de kullanıyor mu; yani durum bilgisini aktif bileşenlerden yedek bileşenlere gönderiyor mu?

**Taktik Soru 22**

Sistem, artan yeniden başlatma (escalating restart) kullanıyor mu — yani yeniden başlatılan bileşen(ler)in inceliğini (granularity) değiştirerek ve etkilenen hizmet düzeyini en aza indirerek hatalardan kurtuluyor mu?

**Taktik Soru 23**

Sistemin mesaj işleme ve yönlendirme kısımları, işlevselliğin denetim (supervisory) ve veri düzlemlerine (data plane) bölündüğü kesintisiz iletim (nonstop forwarding, Bölüm A.4.1’deki gibi) kullanabiliyor mu? Bu durumda, bir denetleyici arızalanırsa, yönlendirici, protokol bilgisinin geri kazanılması ve doğrulanması sırasında bilinen rotalar boyunca paket iletimine devam eder.

**Taktik Soru 24**

Sistem, olası sistem arızalarını azaltmak amacıyla, bileşenleri hizmetten çekerek (service dışı duruma — out-of-service state — geçici olarak alarak) devre dışı bırakabiliyor mu?

Destekleniyor mu? (E/H)

Kullanılabilirlik

Hataları Önle (Prevent faults)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

### Ekler B — Taktik Temelli Anketler (devam)

**Taktik Soru 25**

Sistem, işlemler (transactions) kullanıyor mu — dağıtık bileşenler arasında değiş tokuş edilen eşzamansız mesajların atomik (atomic), tutarlı (consistent), yalıtılmış (isolated) ve kalıcı (durable) olmasını sağlayacak şekilde durum güncellemelerini paketleyerek?

**Taktik Soru 26**

Sistem, bir bileşenin sağlık durumunu izlemek ve sistemin nominal parametreler içinde çalıştığından emin olmak için bir kestirimsel model (predictive model) kullanıyor mu? Olası gelecekteki hatalara işaret eden koşullar tespit edildiğinde, model düzeltici eylemi başlatır.

**Taktik Soru 27**

Sistem, örneğin bir hatayı maskeleyerek, akıllı işaretçiler (smart pointers), soyut veri tipleri (abstract data types) veya sarmalayıcılar (wrappers) kullanarak istisnaların oluşmasını en baştan engelliyor mu?

**Taktik Soru 28**

Sistem, yetkinlik kümesini (competence set) artıracak şekilde tasarlandı mı; örneğin, bir bileşen normal çalışmasının bir parçası olarak daha fazla durumu — hata durumlarını da — ele alacak biçimde tasarlanarak?

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

---

## B.3 Birlikte Çalışabilirlik (Interoperability)

Destekleniyor mu? (E/H)

Tasarım Kararları ve Risk Konumu

Gerekçe ve Varsayımlar

### Taktik Grubu: Konumlandır (Locate)

**Taktik Soru 1**

Sistemin hizmetleri keşfetmek için bir yolu var mı (tipik olarak bir dizin hizmeti — directory service — aracılığıyla)?

### Taktik Grubu: Arabirimleri Yönet (Manage interfaces)

**Taktik Soru 2**

Sistem, hizmetlerin etkinliklerini orkestre etmek için bir yola sahip mi? Yani, hizmet çağrılarını koordine eden, yöneten ve sıralayan bir denetim mekanizması var mı?

**Taktik Soru 3**

Sistem, arabirimleri uyarlamanın (tailor interfaces) bir yoluna sahip mi? Örneğin, bir arabirime çeviri, arabelleğe alma (buffering) veya veri yumuşatma (data smoothing) gibi kabiliyetler ekleyip çıkarabiliyor mu?

---

## B.4 Değiştirilebilirlik (Modifiability)

Destekleniyor mu? (E/H)

Risk

Tasarım Kararları ve Konumu

Gerekçe ve Varsayımlar

### Taktik Grubu: Bir modülün boyutunu azalt (Reduce size of a module)

**Taktik Soru 1**

Modülleri bölerek daha basit hale getiriyor musunuz? Örneğin, büyük ve karmaşık bir modülünüz varsa, bunu iki (veya daha fazla) daha küçük ve daha basit modüle bölebiliyor musunuz?

### Taktik Grubu: Bağlılığı artır (Increase cohesion)
