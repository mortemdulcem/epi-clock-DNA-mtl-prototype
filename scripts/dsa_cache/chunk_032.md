Bu referans mimari (bkz. Bölüm A.1.1), bir web tarayıcısı üzerinden erişilen uygulamaların geliştirilmesine yöneliktir. Bu referans mimari dağıtım ve güncellemeyi kolaylaştırsa da, zengin bir kullanıcı arayüzü deneyimi sunmanın zor olması nedeniyle elenmiştir.

### Mobil
### uygulamalar

Bu referans mimari (bkz. Bölüm A.1.4), elde taşınabilir (handheld) cihazlara dağıtılan uygulamaların geliştirilmesine yöneliktir. Bu seçenek, bu tür cihazların sisteme erişim için kullanılmasının öngörülmemesi nedeniyle elenmiştir.

### Sistemin sunucu kısmını Service Application referans mimarisi kullanarak mantıksal olarak yapılandırma

Servis uygulamaları (service applications) (bkz. Bölüm A.1.5), bir kullanıcı arayüzü sağlamaz; bunun yerine, diğer uygulamalar tarafından tüketilen servisleri sunarlar. Mimar bu referans mimariye aşina olduğu ve gereksinimleri tam olarak karşılamaya yeterli olduğunu düşündüğü için başka hiçbir alternatif değerlendirilmemiş ve elenmemiştir.

### Uygulamayı üç katmanlı dağıtım deseni (three-tier deployment pattern) kullanarak fiziksel olarak yapılandırma

Sisteme bir web tarayıcısı üzerinden erişilmesi gerektiği (CON-2) ve var olan bir veritabanı sunucusunun da kullanılması gerektiği (CON-3) için üç katmanlı bir dağıtım (deployment) uygundur (bkz. Bölüm A.2.2).

Bu noktada, QA-3’ü desteklemek için hem web/uygulama katmanında hem de veritabanı katmanında bir tür çoğaltmaya (replication) ihtiyaç olacağı açıktır, ancak bu konuya daha sonra (3. yinelemede) değinilecektir.

Elenen alternatifler, n != 3 olan diğer n katmanlı (n‑tier) desenleri içermektedir. İki katmanlı alternatif, sisteme mevcut bir eski (legacy) veritabanı sunucusunun dâhil edilmesi gerektiği ve CON-3’e göre bu sunucunun başka hiçbir amaçla kullanılamayacağı için elenmiştir. n > 3 olan tüm alternatifler, bu noktada çözüm için başka sunuculara ihtiyaç duyulmadığı için elenmiştir.

---

### Tasarım Kararları
### ve Konumu

### Gerekçe

#### İstemci uygulamasının kullanıcı arayüzünü Swing Java çatısı (framework) ve diğer Java teknolojilerini kullanarak oluşturma

Java Rich Client’lar geliştirmek için standart çatı, taşınabilirliği (CON-2) güvence altına alır ve geliştiricilerin zaten aşina olduğu teknolojidir (CRN-3).

Elenen alternatifler: Eclipse SWT (Standard Widget Toolkit) çatısı değerlendirilmiştir, ancak geliştiriciler ona bu kadar aşina değildir.

#### Uygulamayı Java Web Start teknolojisini kullanarak dağıtma

Uygulamaya erişim, yükleyiciyi başlatan bir web tarayıcısı (CON-2) aracılığıyla sağlanır. Bu teknoloji ayrıca güncellemeyi de kolaylaştırır, çünkü istemci kodu yalnızca yeni bir sürüm mevcut olduğunda yeniden yüklenir. Güncellemelerin sık gerçekleşmesi beklenmediğinden, bu düşük bant genişlikli (CON-4) durumlar için faydalıdır.

Alternatif, applet kullanımı olurdu; ancak applet’lerin, web sayfası her yüklendiğinde yeniden yüklenmesi gerekir, bu da bant genişliği gereksinimlerini artırır.

---

## 4.3.2.4 Adım 5: Mimari Öğeleri Örneklendirme, Sorumlulukları Tahsis Etme ve Arayüzleri Tanımlama

Örneklendirme (instantiation) ile ilgili ele alınan ve verilen tasarım kararları aşağıdaki tabloda özetlenmiştir:

### Tasarım Kararı ve
### Konumu

### Gerekçe

#### Zengin istemci uygulamasındaki yerel veri kaynaklarını kaldırma

Ağın genellikle güvenilir olması nedeniyle veriyi yerel olarak saklamaya gerek olmadığı düşünülmektedir. Ayrıca, sunucu ile iletişim veri katmanında (data layer) yürütülmektedir. İstemci içindeki bileşenler arasındaki iç iletişim yerel metot çağrıları üzerinden yönetilir ve özel bir desteğe ihtiyaç duymaz.

#### Service Application referans mimarisinin veri katmanında zaman sunucularına erişime adanmış bir modül oluşturma

Referans mimarideki service agents bileşeni, zaman sunucularına erişimi soyutlayacak şekilde uyarlanmıştır. Bu, QA-2’nin gerçekleştirilmesini daha da kolaylaştıracak ve UC-2 ile UC-7’nin gerçekleştirilmesinde kritik bir rol oynayacaktır.

Bu örneklendirme kararlarının sonuçları bir sonraki adımda kayıt altına alınmıştır. Bu ilk yinelemede, işlevselliği ve arayüzleri tam olarak tanımlamak için genellikle çok erkendir. Bir sonraki yineleme, işlevselliği daha ayrıntılı tanımlamaya ayrılmıştır ve bu aşamada arayüzler tanımlanmaya başlanacaktır.

---

## 4.3.2.5 Adım 6: Görünümleri Taslak Olarak Çizme ve Tasarım Kararlarını Kaydetme

Şekil 4.3’teki diyagram, istemci ve sunucu uygulamaları için seçilen iki referans mimarinin modül görünümünün (module view) bir taslağını göstermektedir. Bunlar artık aldığımız tasarım kararlarına göre uyarlanmıştır.

---

## 4.3 Tasarım Süreci

### İstemci Tarafı

`«Layer»` Presentation CS  

`«Layer»` Cross-cutting CS  
`«Swing»` UI Modules  

UI Process Modules  

Security Module CS  

`«Layer»` Business logic CS  

Business Modules CS  

Op. Mgmt. Module CS  

Business Entities CS  

`«Layer»` Data CS  

`«Module»` Communication Modules  

### Sunucu Tarafı

`«Layer»` Services SS  

`«Layer»` Cross-cutting SS  

Service Interfaces  
Security Module SS  

`«Layer»` Business Logic SS  
Business Modules SS  

Business Entities SS  

`«Layer»` Data SS  

Op. Mgmt. Module SS  

Communication Module SS  
DB Access Module  

Time Server Access Module  

**ŞEKİL 4.3** Seçilen referans mimarilerden elde edilen modüller (Anahtar: UML)

---

Bu taslak bir CASE aracı kullanılarak oluşturulmuştur. Araçta her bir öğe seçilmekte ve sorumluluklarına ilişkin kısa bir açıklama kaydedilmektedir. Bu noktadaki açıklamaların oldukça kaba olduğunu, yalnızca temel işlevsel sorumlulukları belirttiğini ve ayrıntı içermediğini not ediniz. Aşağıdaki tablo, kaydedilen bilgileri özetlemektedir:

| Öğe                       | Sorumluluk |
|--------------------------|------------|
| **Presentation client side (CS)** | Bu katman, kullanıcı etkileşimini kontrol eden ve kullanım durumu (use case) kontrol akışını yöneten modülleri içerir. |
| **Business logic CS**    | Bu katman, istemci tarafında yerel olarak yürütülebilen iş mantığı (business logic) işlemlerini gerçekleştiren modülleri içerir. |
| **Data CS**              | Bu katman, sunucu ile iletişimden sorumlu modülleri içerir. |
| **Cross-cutting CS**     | Bu “katman”, güvenlik, kayıt (logging) ve G/Ç (I/O) gibi farklı katmanlara yayılan işlevselliğe sahip modülleri içerir. QA-6 bir sürücü olmasa bile, onun başarılmasına yardımcı olur. |
| **UI modules**           | Bu modüller, kullanıcı arayüzünü oluşturur (render) ve kullanıcı girdilerini alır. |
| **UI process modules**   | Bu modüller, tüm sistem kullanım durumlarının (ekranlar arası gezinme dâhil) kontrol akışından sorumludur. |
| **Business modules CS**  | Bu modüller ya yerel olarak gerçekleştirilebilen iş operasyonlarını uygular ya da sunucu tarafındaki işlevselliği ortaya çıkarır. |
| **Business entities CS** | Bu varlıklar, alan (domain) modelini oluşturur. Sunucu tarafındakilere göre daha az ayrıntılı olabilirler. |
| **Communication modules CS** | Bu modüller, sunucu tarafında çalışan uygulama tarafından sağlanan servisleri tüketir. |
| **Services server side (SS)** | Bu katman, istemciler tarafından tüketilen servisleri ortaya çıkaran modülleri içerir. |
| **Business Logic SS**    | Bu katman, sunucu tarafında işlenmesi gereken iş mantığı işlemlerini gerçekleştiren modülleri içerir. |
| **Data SS**              | Bu katman, veri kalıcılığından (persistence) ve zaman sunucuları ile iletişimden sorumlu modülleri içerir. |
| **Cross-cutting SS**     |  |

> **💬 Çevirmen notu:** “CS” (client side) istemci tarafını, “SS” (server side) sunucu tarafını ifade etmektedir; katman adlarında bu kısaltmalar korunmuştur.
