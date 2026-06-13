Farklı projeler, riske farklı tepkiler gerektirir. Neyse ki biz mimarlar olarak
mimarileri analiz etmek için elimizin altında çok çeşitli araçlara sahibiz. Biraz
planlamayla, risk toleransımızı hem bütçe ve zaman kısıtlarımızı karşılayan
hem de makul düzeyde güvence sağlayan bir analiz teknikleri kümesiyle
eşleştirebiliriz. Buradaki nokta, analizin pahalı veya karmaşık olmak zorunda
olmadığıdır. Sadece düşünülmüş sorular sormak bile bir analiz biçimidir ve bu
alıştırma oldukça ucuzdur. Basit bir prototip inşa etmek daha pahalıdır, fakat
büyük bir proje bağlamında, Bölüm 5’te gördüğümüz gibi, riskleri keşfetme ve
hafifletme biçimi nedeniyle bu analiz tekniği ek maliyete fazlasıyla değebilir.

Hâlihazırda yaygın kullanımda olan (nispeten ekonomik, nispeten düşük
törenli) analiz tekniklerine örnek olarak tasarım gözden geçirmeleri (design
review) ve senaryo temelli analizler (scenario-based analysis), kod gözden
geçirmeleri (code review), eşli programlama (pair programming) ve Scrum
geriye dönük değerlendirme toplantıları (Scrum retrospective) verilebilir. Biraz
daha maliyetli olmakla birlikte yaygın olarak kullanılan diğer analiz teknikleri
arasında prototipler (atılabilir veya evrimsel) ve benzetimler (simülasyonlar)
yer alır.

Maliyet ve karmaşıklığın en üst düzeyinde, sistemlerimizin biçimsel
modellerini (formal model) inşa edebilir ve bunları gecikme (latency), güvenlik
(security) veya emniyet (safety) gibi özellikler açısından analiz edebiliriz. Bir
aday gerçekleştirim (candidate implementation) ya da nihayet sahaya sürülmüş
(fielded) bir sistem ortaya çıktığında, çalışan sistemleri enstrümante etmeyi
(instrumentation) ve veri toplamayı da içeren deneyler gerçekleştirebiliriz; ideali,
sistemin gerçekçi kullanım biçimlerini yansıtan yürütümlerinden veri toplamaktır.

Tablo 8.1’de gösterildiği gibi, bu tekniklerin maliyeti tipik olarak yazılım
geliştirme yaşam döngüsü (software development life cycle) boyunca ilerledikçe
artar. Bir prototip ya da deney, bir kontrol listesinden (checklist) daha pahalıdır;
kontrol listesi de deneyime dayalı bir benzetimden (experience-based analogy)
daha pahalıdır. Bu beklenen maliyet, analiz sonuçlarından duyabileceğiniz
güvenle oldukça güçlü şekilde koreledir. Ne yazık ki bedava öğle yemeği diye
bir şey yok!

---

# 8. Bölüm — Tasarım Sürecinde Analiz

## TABLO 8.1

### Yazılım Yaşam Döngüsünün Farklı Aşamalarında Analiz

| Yaşam Döngüsü Aşaması | Analiz Biçimi                             | Maliyet      | Güven          |
|-----------------------|-------------------------------------------|-------------:|----------------|
| Gereksinimler         | Deneyime dayalı benzetim (analogy)       | Düşük        | Düşük–yüksek   |
| Gereksinimler         | Kabaca hesap (back-of-the-envelope) analizi | Düşük     | Düşük–orta     |
| Mimari                | Düşünce deneyi / yansıtıcı sorular        | Düşük        | Düşük–orta     |
| Mimari                | Kontrol listesi temelli analiz            | Düşük        | Orta           |
| Mimari                | Taktik temelli analiz (tactics-based)     | Düşük        | Orta           |
| Mimari                | Senaryo temelli analiz (scenario-based)   | Düşük–orta   | Orta           |
| Mimari                | Analitik model                            | Düşük–orta   | Orta           |
| Mimari                | Simülasyon                                | Orta         | Orta           |
| Mimari                | Prototip                                  | Orta         | Orta–yüksek    |
| Gerçekleştirim        | Deney                                     | Orta–yüksek  | Orta–yüksek    |
| Sahadaki sistem       | Enstrümantasyon (instrumentation)         | Orta–yüksek  | Yüksek         |

## 8.4 Taktik Temelli Analiz (Tactics-Based Analysis)

Mimari taktikler (architectural tactics) (Bölüm 2.5.4’te tartışılmıştı) şu ana dek
tasarım ögeleri (design primitives) olarak sunuldu. Ancak bu sınıflandırmalar
(bu taksonomiler), bir kalite niteliğini (quality attribute) yönetmeye yönelik
mimari tasarım olasılıklarının tüm uzayını kapsayacak biçimde tasarlandığından,
onları bir analiz bağlamında da kullanabiliriz. Daha spesifik olarak, onları
mülakatlar veya anketler için birer rehber olarak kullanabiliriz. Bu mülakatlar,
bir analist olarak sizin, ele alınan veya alınmamış mimari yaklaşımlar hakkında
hızlı içgörü kazanmanıza yardımcı olur.

Örneğin, Şekil 8.1’de gösterilen erişilebilirlik (availability) taktiklerini
ele alalım.

> **💬 Çevirmen notu:** Buradaki “taktik”ler, belirli bir kalite niteliğini artırmak için uygulanabilen tekrarlanabilir, küçük mimari karar kalıplarıdır; “desen”den (pattern) daha ince tanelidir.

## 8.4 Taktik Temelli Analiz

### Erişilebilirlik (Availability) Taktikleri

- Hatalardan Kurtulma (Recover from Faults)
- Hataları Tespit Etme (Detect Faults)
- Hazırlık ve Onarım (Preparation and Repair)
  - Ping / Echo
  - İzleme (Monitor)
  - Kalp atışı (Heartbeat)
  - Zaman damgası (Timestamp)
  - Hata (Fault)
  - Etkin yedeklilik (Active Redundancy)
  - Pasif yedeklilik (Passive Redundancy)
  - Yedek (Spare)
  - Sağlamlık kontrolü (Sanity Checking)
  - İstisna işleme (Exception Handling)
  - Koşul izleme (Condition Monitoring)
  - Geri alma (Rollback)
  - Oylama (Voting)
  - Yazılım yükseltme (Software Upgrade)
  - İstisna tespiti (Exception Detection)
  - Yeniden deneme (Retry)
  - Öz test (Self-Test)
  - Hataları Önleme (Prevent Faults)
  - Yeniden devreye alma (Reintroduction)
  - Gölge (Shadow)
  - Servisten çıkarma (Removal from Service)
  - Durum yeniden eşzamanlama (State Resynchronization)
  - İşlemler (Transactions)
  - Kademeli yeniden başlatma (Escalating Restart)
  - Öngörücü model (Predictive Model)
  - Sürekli iletim (Non-Stop Forwarding)
  - İstisna önleme (Exception Prevention)
  - Hatanın maskelenmesi veya onarımın yapılması (Fault Masked or Repair Made)
  - Yeterlilik kümesini artırma (Increase Competence Set)
  - Hatalı davranışı yok sayma (Ignore Faulty Behavior)
  - Bozulma (Degradation)
  - Yeniden yapılandırma (Reconfiguration)

**Şekil 8.1** Erişilebilirlik taktikleri

Bu taktiklerin her biri, yüksek erişilebilirlikte bir sistem tasarlamak isteyen
mimar için bir tasarım seçeneğidir. Ancak geriye dönük olarak kullanıldıklarında,
erişilebilirlik için tüm tasarım uzayının bir sınıflandırmasını temsil ederler ve
dolayısıyla mimar tarafından verilmiş ve verilmemiş kararlar hakkında içgörü
edinmenin bir yolu olabilirler. Bunu yapmak için, her bir taktiği basitçe bir
mülakat sorusuna dönüştürürüz. Örneğin, Tablo 8.2’deki (kısmi) taktik
esinli erişilebilirlik soruları kümesini ele alın.

## TABLO 8.2

### Örnek Taktik Temelli Erişilebilirlik Soruları

| Taktik Grubu | Taktik Sorusu | Destekleniyor mu? (E/H) | Risk | Tasarım Kararları ve Konum | Gerekçe ve Varsayımlar |
|--------------|---------------|--------------------------|------|----------------------------|------------------------|
| Hataları tespit et | Sistem, bir bileşenin veya bağlantının ya da ağ tıkanıklığının (congestion) hatasını tespit etmek için ping/echo kullanıyor mu? | E | D | Sunucu, zaman sunucularının “canlı” olup olmadığını görmek için periyodik olarak onlara ping gönderir. | Sistem, bir bileşenin veya bağlantının ya da ağ tıkanıklığının hatasını tespit etmek için ping/echo kullanıyor mu? |
| Hataları tespit et | Sistem, diğer sistem parçalarının sağlık durumunu izleyen bir bileşen kullanıyor mu? Bir sistem izleyicisi (system monitor), ağdaki veya hizmet reddi (denial-of-service) saldırısı gibi diğer paylaşımlı kaynaklardaki hata ya da tıkanıklığı tespit edebilir. | H | Uygulanamaz | Bu sistemde bu uygulanmadı. Sistemi izlemek için başka tekniklere güveneceğiz. Örneğin, bellek tüketimi veya işlemci yükü bilgisi işletim sisteminden elde edilebilir. | İşletim sisteminin sağladığı bilginin ötesindeki bilginin kritik olmadığı varsayılmaktadır. |
| Hataları tespit et | Sistem, bir bileşenin veya bağlantının ya da ağ tıkanıklığının hatasını tespit etmek için bir sistem izleyici ile bir süreç arasında periyodik mesaj alışverişi anlamına gelen bir kalp atışı (heartbeat) kullanıyor mu? | E | D | Sunucu, istemcilere periyodik olarak bir kalp atışı gönderir. | Sunucunun, istemcilerden gelen ping isteklerini işlemek zorunda olmaması. Zaman sunucularının kalp atışı yaklaşımını uygulamak için değiştirilmesi mümkün değildir. |
| Hataları tespit et | Sistem, dağıtık sistemlerdeki yanlış olay sıralarını tespit etmek için zaman damgası (timestamp) kullanıyor mu? | E | O | Sunucudan istemcilere gönderilen olayların bir zaman damgası vardır; çünkü bunların alındıkları sıraya göre işlenmeleri gerekir. | İstemcilerin, ağın durumunun doğru bir gösterimini sergilemeleri istenmektedir; bu da sunucudan gelen tüm bildirimleri almalarını ve bunları doğru sırada işlemelerini içerir. |
| Hataları tespit et | Sistem, çoğaltılmış (replicated) bileşenlerin aynı sonuçları ürettiğini kontrol etmek için oylama (voting) kullanıyor mu? Kopyalanmış bileşenler, özdeş replikalar, işlevsel olarak yedekli ya da analitik olarak yedekli olabilir. | H | Uygulanamaz | Bu sistem tarafından buna gerek duyulmamaktadır. | — |
| Hataları tespit et | Sistem, normal yürütme akışını değiştiren bir sistem durumunu tespit etmek için istisna tespiti (exception detection) kullanıyor mu? Örneğin sistem istisnaları, parametre sınırları (parameter fences), parametre tip kontrolü, zaman aşımları (timeouts)? | E | D | Standart Java istisna yönetimi kullanılır ve tüm istisnalar bir günlük dosyasına (log) gönderilir. Zaman aşımları, istekler sunucuya gönderildiğinde istemci tarafında uygulanır. | Varsayım, Java’daki istisna mekanizmasının ve zaman aşımı kullanımının ihtiyaç duyulan her şeyi sağladığıdır. |
| Hataları tespit et | Sistem, doğru çalıştığını test etmek için kendi kendine test (self-test) yapabiliyor mu? | H | Uygulanamaz | Bu, özgün tasarımımızda dikkate alınmamıştı. | — |
