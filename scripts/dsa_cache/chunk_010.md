1. QAW Sunumu ve Tanışmalar  
QAW (Quality Attribute Workshop) kolaylaştırıcıları, QAW’nin arkasındaki motivasyonu açıklar ve yöntemin her adımını anlatır.

2. İş Hedefleri Sunumu  
Projeye ait iş ile ilgili kaygıları temsil eden bir paydaş (stakeholder), sistemin iş bağlamını, geniş kapsamlı işlevsel gereksinimlerini, kısıtlarını ve bilinen kalite niteliği (quality attribute) gereksinimlerini sunar. İlerleyen QAW adımlarında ayrıntılandırılacak kalite nitelikleri, bu adımda sunulan iş hedeflerinden türetilecek ve bu hedeflere izlenebilir olmalıdır. Bu nedenle, bu iş hedeflerinin önceliklendirilmiş olması gerekir.

3. Mimari Plan Sunumu  
Mimar, sistem mimari planlarını mevcut hâliyle sunar. Mimari çoğu zaman henüz tanımlanmamış olsa da (özellikle sıfırdan geliştirilen (greenfield) sistemler için), mimar çoğunlukla bu erken aşamada bile mimari hakkında oldukça çok şey bilmektedir. Örneğin, halihazırda zorunlu kılınmış teknolojileri, bu sistemin etkileşime geçmesi gereken diğer sistemleri, uyulması gereken standartları, yeniden kullanılabilecek alt sistemleri veya bileşenleri ve benzeri unsurları biliyor olabilir.

4. Mimari Sürücülerin (architectural driver) Belirlenmesi  
Kolaylaştırıcılar, 2. ve 3. adımlarda derledikleri temel mimari sürücü (architectural driver) listelerini paydaşlarla paylaşır ve paydaşlardan açıklama, ekleme, çıkarma ve düzeltme isterler. Buradaki amaç; başlıca işlevsel gereksinimleri, iş sürücülerini (business driver), kısıtları ve kalite niteliklerini kapsayan, damıtılmış bir mimari sürücü listesi üzerinde uzlaşmaya varmaktır.

5. Senaryo Beyin Fırtınası  
Bu bağlam verildikten sonra, her paydaşın artık sistemle ilgili kendi ihtiyaç ve beklentilerini temsil eden bir senaryo ifade etme fırsatı vardır. Kolaylaştırıcılar, her senaryonun açıkça belirtilmiş bir uyarıcı (stimulus) ve yanıt (response) içerdiğinden emin olurlar. Ayrıca, izlenebilirlik ve tamamlık da gözetilir: 4. adımda listelenen her mimari sürücü için en az bir temsilî senaryo bulunmalı ve 2. adımda listelenen tüm iş hedeflerini kapsamalıdır.

6. Senaryo Konsolidasyonu  
Benzer senaryolar, uygun olduğu ölçüde birleştirilir. 7. adımda paydaşlar favori senaryolarına oy verecekleri için, konsolidasyon; özünde aynı kaygıyı dile getiren birden fazla senaryo arasında oyların dağılmasını engellemeye yardımcı olur.

7. Senaryo Önceliklendirme  
Senaryoların önceliklendirilmesi, her paydaşa toplam senaryo sayısının yüzde 30’u kadar oy verilmesiyle gerçekleştirilir. Paydaşlar bu oyları istedikleri senaryo veya senaryolar arasında dağıtabilirler. Tüm paydaşlar oylarını verdikten sonra sonuçlar toplanır ve senaryolar popülerlik sırasına göre sıralanır.

## 2.4 Mimari Sürücüler

8. Senaryo İyileştirme  
En yüksek öncelikli senaryolar iyileştirilir ve detaylandırılır. Kolaylaştırıcılar, paydaşların bu senaryoları altı bölümlü senaryo biçiminde ifade etmelerine yardımcı olur: kaynak (source), uyarıcı (stimulus), artefakt (artifact), ortam (environment), yanıt (response) ve yanıt ölçüsü (response measure).

Dolayısıyla QAW çıktısı, iş hedefleriyle hizalanmış, önceliklendirilmiş bir senaryo listesidir; bu listede en yüksek öncelikli senaryolar incelenmiş ve iyileştirilmiştir. Basit bir sistem için veya bir iterasyonun parçası olarak bir QAW 2–3 saat gibi kısa bir sürede gerçekleştirilebilir; gereksinimlerin tamlığı hedeflendiği karmaşık bir sistemde ise 2 günü bulabilir.

### Fayda Ağacı (Utility Tree)

Hazırda başvurulacak paydaşlar yoksa bile, ne yapacağınıza ve sistemin karşı karşıya olduğu çok sayıdaki zorluğu nasıl önceliklendireceğinize karar vermeniz gerekir. Düşüncelerinizi düzenlemenin bir yolu, bir Fayda Ağacı (Utility Tree) oluşturmaktır. Aşağıdaki şekilde gösterilene benzer bir Fayda Ağacı, kalite niteliği hedeflerinizi ayrıntılı olarak ifade etmenize ve ardından bunları önceliklendirmenize yardımcı olur.

- **Performance (performans)**  
  - **Latency (gecikme)** — (M, M)  
    Kullanıcı, zaman sunucusunun olay geçmişini görüntüler. Son 24 saate ait olay listesi 1 saniye içinde görüntülenir.  
  - **Peak load (zirve yük)** — (H, H)  
    Yönetim sistemi, zirve yük sırasında zaman sunucusundan veri toplar. Tüm veriler 5 dakika içinde toplanır.  
    — (M, H)  
    Zaman sunucuları, zirve yük sırasında yönetim sistemine tuzak (trap) mesajları gönderir. Tuzakların (traps) %100’ü başarıyla işlenir ve depolanır.

- **Usability (kullanılabilirlik)**  
  - **Learnability (öğrenilebilirlik)** — (L, L)  
    Yeni bir kullanıcı, hesabını yapılandırabilir ve 8 saatten az eğitimle sistemi kullanıyor durumda olur.  
  - **Feedback (geribildirim)** — (H, L)  
    Kritik olaylar, 5 saniyeden kısa sürede kullanıcıya raporlanır ve görsel hâle getirilir.

- **Availability (kullanılabilirlik/erişilebilirlik)**  
  - **SW failure (yazılım hatası)** — (H, H)  
    Yönetim sisteminde bir hata oluşur. Yönetim sistemi 30 saniyeden kısa sürede çalışmaya devam eder duruma gelir.  
  - **Network failure (ağ hatası)**  
    (Metin ağ hatası senaryosunu örnek şekilden kısaltarak yansıtıyor; varsayımsal ayrıntı eklenmemiştir.)

- **Security (güvenlik)**  
  - **Authentication (kimlik doğrulama)** — (H, M)  
    Kimlik doğrulama, yetkisiz oturum açma girişimlerinin %99.999’unun tespit edilmesini sağlar.  
  - **Audit trail (denetim izi)** — (H, L)  
    Bir kullanıcı sistem yapılandırmasında değişiklik yapar. Bu değişikliklerin %100’ü kaydedilir.

> **💬 Çevirmen notu:** Parantez içindeki (H, M), (M, L) gibi ikililer genellikle “yüksek/orta/düşük iş önemi” ve “yüksek/orta/düşük teknik risk” şeklinde iki boyutlu önceliklendirme derecesini ifade eder; ayrıntısı aşağıdaki öncelik matrisi kısmında açıklanıyor.

Çalışma biçimi şu şekildedir. Önce bir kâğıda “Utility” (fayda) kelimesini yazın. Sonra, sisteminiz için faydayı oluşturan çeşitli kalite niteliklerini yazın. Örneğin, sistemin iş hedeflerine dayanarak, sistem için en önemli niteliklerin hızlı olması, güvenli olması ve kolay değiştirilebilir olması gerektiğini biliyor olabilirsiniz. Buna karşılık, “Utility”nin altına bu kelimeleri yazarsınız. Sonraki adımda, aslında bu terimlerin her birinin ne anlama geldiğini tam olarak bilmiyor olduğumuz için, en çok kaygı duyduğumuz kalite niteliği yönünü tanımlarız. Örneğin, “performans” belirsiz bir ifadedir; “veritabanı işlemlerinin gecikmesi (latency of database transactions)” ise biraz daha az belirsizdir. Benzer şekilde, “modifiability (değiştirilebilirlik)” belirsizdir; “yeni kodeklerin (codec) eklenmesinin kolaylığı (ease of adding new codecs)” biraz daha az belirsizdir.

Ağacın yaprakları, az önce sıraladığınız kalite niteliği hususlarına ilişkin somut örnekler sağlayan senaryolar biçiminde ifade edilir. Örneğin, “veritabanı işlemlerinin gecikmesi” için şu senaryoyu oluşturabilirsiniz: “Normal koşullar altında 1000 kullanıcı kendi müşteri kayıtlarını aynı anda günceller ve ortalama gecikme 1 saniyedir.”  
“Yeni kodeklerin eklenmesinin kolaylığı” için şu senaryoyu oluşturabilirsiniz: “Müşteri, sisteme yeni bir özel kodek eklenmesini talep eder. Kodek, hiçbir yan etki olmaksızın 2 kişi-haftalık (2 person-weeks) eforla sisteme eklenir.”

Son olarak, oluşturduğunuz senaryoların önceliklendirilmesi gerekir. Bu önceliklendirmeyi, iki boyut boyunca sıralama tekniğini kullanarak yaparız ve bunun sonucunda aşağıdakine benzer bir öncelik matrisi elde ederiz (hücrelerde yer alan numaralar, bir dizi sistem senaryosunun kimlik numaralarıdır).

| İş Önemi / Teknik Risk | L                | M        | H              |
|------------------------|------------------|----------|----------------|
| **L**                  | 5, 6, 17, 20, 22 | 1, 14    | 12, 19         |
| **M**                  | 9, 12, 16        | 8, 20    | 3, 13, 15      |
| **H**                  | 10, 18, 21       | 4, 7     | 2, 11          |
