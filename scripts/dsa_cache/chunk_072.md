Arızalı Davranışı
Yok Say
(Azaltım - Degradation)
Yeniden
Yapılandırma (Reconfiguration)

ŞEKİL A.12 Kullanılabilirlik taktikleri (availability tactics)

Hataları Önle (Prevent Faults)

Yeniden
Devreye Alma
(Reintroduction)

Gölge
(Shadow)

Hizmetten
Çıkarma
(Removal from
Service)

Durum
Yeniden
Eşzamanlama
(State
Resynchronization)

İşlemler
(Transactions)

Kademeli
Yeniden Başlatma
(Escalating
Restart)

Öngörücü
Model
(Predictive
Model)

Sürekli
İletim
(Non-Stop
Forwarding)

İstisna
Önleme
(Exception
Prevention)
Yeterlilik
Kümesini Artır
(Increase
Competence Set)

Hata
Maske
lendi
veya
Onarım
Yapıldı
(Fault
Masked
or
Repair
Made)

## A.4 Taktikler (Tactics)

### Hataları Tespit Et (Detect Faults)

- § Ping/echo: Düğümler arasında, ilişkilendirilmiş ağ yolundaki erişilebilirliği ve gidiş‑dönüş gecikmesini belirlemek için kullanılan, eşzamansız bir istek/yanıt mesaj çifti.
- § Monitor (izleyici): Sistem parçalarının sağlık durumunu izlemek için kullanılan bir bileşen. Bir sistem izleyicisi, ağda ya da hizmet reddi (denial-of-service) saldırısı gibi diğer paylaşılan kaynaklarda oluşan arıza veya tıkanıklığı tespit edebilir.
- § Heartbeat (kalp atışı): Bir sistem izleyicisi ile izlenen bir süreç arasında periyodik mesaj alışverişi gerçekleşmesi.
- § Timestamp (zaman damgası): Özellikle dağıtık mesaj geçişi (message-passing) sistemlerinde, olayların hatalı sıralarını tespit etmek.
- § Sanity checking (makullük denetimi): Bir bileşenin işlemlerinin veya çıktılarının geçerliliğini ya da makullüğünü denetlemek; tipik olarak iç tasarım bilgisine, sistemin durumuna veya incelenen bilginin doğasına dayanır.
- § Condition monitoring (koşul izleme): Bir süreçteki veya aygıttaki koşulları denetlemek ya da tasarım sırasında yapılmış varsayımları doğrulamak.
- § Voting (oylama): Kopyalanmış (replicated) bileşenlerin aynı sonuçları ürettiğini kontrol etmek. Çoğaltma (replication), işlevsel yedeklilik (functional redundancy), analitik yedeklilik (analytic redundancy) gibi çeşitli türleri vardır.
- § Exception detection (istisna tespiti): Sistem istisnası, parametre sınırları (parameter fence), parametre tip kontrolü (parameter typing) veya zaman aşımı (timeout) gibi normal yürütme akışını değiştiren bir sistem durumunu tespit etmek.
- § Self-test (öz test): Bir bileşenin kendi doğru çalışmasını test etmesine yönelik prosedür.

### Hatalardan Kurtul (Hazırlık ve Onarım)  
(Recover from Faults – Preparation and Repair)

- § Active redundancy (etkin yedeklilik, hot spare): Bir koruma grubundaki tüm düğümler, yedek düğüm ya da düğümlerin etkin düğüm(ler) ile eşzamanlı durumunu (synchronous state) korumasına izin verecek biçimde, aynı girdileri paralel olarak alır ve işler.
- § Passive redundancy (pasif yedeklilik, warm spare): Koruma grubunun yalnızca etkin üyeleri giriş trafiğini işler; görevlerinden biri de periyodik durum güncellemeleri ile yedek düğüm(ler)i beslemektir.
- § Spare (yedek, cold spare): Bir koruma grubunun yedek düğümleri, bir yana geçme (failover) gerçekleşene kadar hizmet dışı durumda kalır; bu noktada, yedek düğüm hizmete alınmadan önce bir “power-on-reset” prosedürü başlatılır.
- § Exception handling (istisna işleme): İstisnayı raporlayarak veya işleyerek onunla başa çıkmak; gerekirse istisnanın nedenini düzelterek ve tekrar deneyerek hatayı maskelemek.
- § Rollback (geri alma): “Rollback line” olarak adlandırılan, bilinen iyi bir önceki duruma geri dönmek.
- § Software upgrade (yazılım yükseltmesi): Hizmete etki etmeyecek bir şekilde, çalışmakta olan sistemde yürütülebilir kod imajlarının yükseltilmesini gerçekleştirmek.
- § Retry (yeniden deneme): Bir arıza geçiciyse (transient), işlemi yeniden denemek başarıya ulaşılmasını sağlayabilir.
- § Ignore faulty behavior (arızalı davranışı yok sayma): Mesajların sahte (spurious) olduğu belirlendiğinde, bu kaynaktan gönderilen mesajları yok saymak.
- § Degradation (azaltım/degradasyon): Bileşen arızalarının varlığında, daha az kritik işlevleri bırakıp en kritik sistem işlevlerini sürdürmek.
- § Reconfiguration (yeniden yapılandırma): Mümkün olduğunca çok işlevselliği koruyarak, sorumlulukları çalışmaya devam eden kaynaklara yeniden atamak.

### Hatalardan Kurtul (Yeniden Devreye Alma)  
(Recover from Faults – Reintroduction)

- § Shadow (gölge): Daha önce arızalanmış veya hizmet sırasında yükseltilmiş bir bileşeni, bileşeni tekrar etkin role döndürmeden önce tanımlanmış bir süre boyunca “gölge kipinde (shadow mode)” çalıştırmak.
- § State resynchronization (durum yeniden eşzamanlama): Pasif yedeklilik; bu, etkin yedekliliğin tamamlayıcı (partner) taktiği olup, durum bilgisinin etkin bileşenlerden yedek bileşenlere gönderilmesini içerir.
- § Escalating restart (kademeli yeniden başlatma): Yeniden başlatılan bileşen(ler)in incelik (granularity) düzeyini değiştirerek ve etkilenen hizmet seviyesini en aza indirerek hatalardan kurtulmak.
- § Non-stop forwarding (sürekli iletim): İşlevsellik, denetleyici (supervisory) ve veri (data) varyantlarına bölünür. Bir denetleyici (supervisor) arızalanırsa, yönlendirici (router), protokol bilgisinin kurtarılması ve doğrulanması sırasında, bilinen rotalar boyunca paketleri iletmeyi sürdürür.

### Hataları Önle (Prevent Faults)

- § Removal from service (hizmetten çıkarma): Potansiyel sistem arızalarını hafifletmek amacıyla, bir sistem bileşenini geçici olarak hizmet dışı duruma almak.
- § Transactions (işlemler): Dağıtık bileşenler arasında değiş tokuş edilen eşzamansız mesajların atomik, tutarlı (consistent), yalıtılmış (isolated) ve kalıcı (durable) olmasını sağlamak için durum güncellemelerini paketlemek.
- § Predictive model (öngörücü model): Bir sürecin sağlık durumunu izleyerek sistemin nominal parametreler içinde çalıştığından emin olmak; gelecekteki olası hataların habercisi olan koşullar tespit edildiğinde düzeltici işlem yapmak.
- § Exception prevention (istisna önleme): Bir hatayı maskeleyerek ya da akıllı işaretçiler (smart pointers), soyut veri tipleri (abstract data types) ve sarmalayıcılar (wrappers) kullanarak sistem istisnalarının oluşmasını engellemek.
- § Increase competence set (yeterlilik kümesini artırma): Bir bileşeni, normal çalışmasının bir parçası olarak daha fazla durumu—hatayı—ele alacak şekilde tasarlamak.

### A.4.2 Birlikte Çalışabilirlik Taktikleri (Interoperability Tactics)

Şekil A.13, birlikte çalışabilirliğe (interoperability) ulaşmak için kullanılan taktikleri özetler.

## A.4 Taktikler

Birlikte Çalışabilirlik Taktikleri (Interoperability Tactics)

Bilgi
Alışverişi
İsteği
(Information
Exchange
Request)

Konumlandır
(Locate)

Arayüzleri
Yönet
(Manage Interfaces)

Servisi
Keşfet
(Discover
Service)

Yönlendir/Orkestre Et
(Orchestrate)

İstek
Doğru
İşlenmiş
(Request
Correctly
Handled)

Arayüzü
Uyarlama
(Tailor Interface)

ŞEKİL A.13 Birlikte çalışabilirlik taktikleri (interoperability tactics)

### Konumlandır (Locate)

- § Discover service (servisi keşfet): Bilinen bir dizin servisi (directory service) içinde arama yaparak bir servisi bulmak. Bu konumlandırma sürecinde birden fazla dolaylılık (indirection) düzeyi olabilir; yani bilinen bir konum, başka bir konuma işaret edebilir ve bu ikinci konum da servis için aranabilir.

### Arayüzleri Yönet (Manage Interfaces)

- § Orchestrate (orkestrasyon): Servis çağrılarının sevkini (invocation) koordine etmek, yönetmek ve sıralamak için bir denetim mekanizması kullanmak. Orkestrasyon, sistemlerin karmaşık bir görevi yerine getirmek için karmaşık biçimde etkileşime girmesi gerektiğinde kullanılır.
- § Tailor interface (arayüzü uyarlama): Çeviri (translation), arabellekleme (buffering) veya veri yumuşatma (data smoothing) gibi yetenekleri bir arayüze eklemek ya da arayüzden çıkarmak.

### A.4.3 Değiştirilebilirlik Taktikleri (Modifiability Tactics)

Şekil A.14, değiştirilebilirliğe (modifiability) ulaşmak için kullanılan taktikleri özetler.

Değiştirilebilirlik Taktikleri (Modifiability Tactics)

Değişiklik
Gelir
(Change
Arrives)

Bir Modülün
Boyutunu Azalt
(Reduce Size
of a Module)

Bağlılığı
(Cohesion)
Artır
(Increase
Cohesion)

Bağımlılığı
(Coupling)
Azalt
(Reduce
Coupling)

Modülü
Böl
(Split Module)

Anlamsal
Tutarlılığı
Artır
(Increase
Semantic
Coherence)

Sarmala
(Encapsulate)

Bağlamayı
Eritele
(Defer
Binding)

Ara
Bileşen
Kullan
(Use an
Intermediary)

Değişiklik
Zaman ve
Bütçe İçinde
Yapılır
(Change Made
within Time
and Budget)

Bağımlılıkları
Kısıtla
(Restrict
Dependencies)

Yeniden
Yapılandır
(Refactor)

Ortak
Servisleri
Soyutla
(Abstract Common
Services)

ŞEKİL A.14 Değiştirilebilirlik taktikleri (modifiability tactics)

#### Bir Modülün Boyutunu Azalt (Reduce Size of a Module)

- § Split module (modülü böl): Değiştirilen modül çok fazla yetenek içeriyorsa, değişiklik maliyetleri muhtemelen yüksek olacaktır. Modülü birden çok daha küçük modüle ayrıştırmak, gelecekteki değişikliklerin ortalama maliyetini azaltmalıdır.

#### Bağlılığı Artır (Increase Cohesion)

- § Increase semantic coherence (anlamsal tutarlılığı artır): Bir modüldeki A ve B sorumlulukları aynı amaca hizmet etmiyorsa, bunlar farklı modüllerde yer almalıdır. Bu, yeni bir modül oluşturmayı ya da bir sorumluluğu mevcut bir modüle taşımayı gerektirebilir.

#### Bağımlılığı Azalt (Reduce Coupling)
