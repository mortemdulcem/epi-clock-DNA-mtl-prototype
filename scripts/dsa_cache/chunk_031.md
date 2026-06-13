Bir kullanıcı, normal çalışma sırasında belirli bir zaman sunucusunun olay geçmişini görüntüler. Son 24 saate ait olay listesi 1 saniye içinde görüntülenir.

UC-3

QA-6

Güvenlik (Security)

Bir kullanıcı, normal çalışma sırasında sistemde bir değişiklik yapar. Kimin, hangi zamanda bu işlemi yaptığını bilmek her zaman (%100) mümkün olacaktır.

Tümü (All)

### 4.2.3 Kısıtlar (Constraints)

Son olarak, sistem ve onun gerçekleştirimine (implementation) ilişkin bir dizi kısıt toplanmıştır. Bunlar aşağıdaki tabloda sunulmaktadır.

| ID     | Kısıt (Constraint)                                                                                                                                              |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CON-1  | En az 50 eşzamanlı kullanıcının desteklenmesi gerekir.                                                                                                          |
| CON-2  | Sisteme, farklı platformlardaki (Windows, OSX ve Linux) bir web tarayıcısı (Chrome V3.0+, Firefox V4+, IE8+) üzerinden erişilmelidir.                          |
| CON-3  | Mevcut bir ilişkisel veritabanı sunucusu kullanılmalıdır. Bu sunucu, veritabanını barındırmak dışında başka amaçlarla kullanılamaz.                             |
| CON-4  | Kullanıcı iş istasyonlarına olan ağ bağlantısı düşük bant genişliğine sahip olabilir, ancak genel olarak güvenilirdir.                                          |
| CON-5  | Zaman sunucularının veriyi atmasına yol açtığından, performans verileri en fazla 5 dakikalık aralıklarla toplanmalıdır.                                        |
| CON-6  | Son 30 güne ait olaylar saklanmalıdır.                                                                                                                          |

80 Bölüm 4—Vaka Çalışması: FCAPS Sistemi

### 4.2.4 Mimari Kaygılar (Architectural Concerns)

Bu bir “greenfield” geliştirme olduğu için (yani tamamen sıfırdan yeni bir sistem geliştirildiği için), başlangıçta yalnızca birkaç genel mimari kaygı belirlenmiştir; bunlar aşağıdaki tabloda gösterilmektedir.

| ID     | Kaygı (Concern)                                                                                                                                                               |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CRN-1  | Genel, başlangıç düzeyinde bir sistem yapısının oluşturulması.                                                                                                                |
| CRN-2  | Ekip üyelerinin Java teknolojileri (Spring, JSF, Swing, Hibernate, Java Web Start ve JMS çatıları (frameworks) ve Java dili) konusundaki bilgisinden yararlanmak.            |
| CRN-3  | Geliştirme ekibinin üyelerine işin (görevlerin) atanması.                                                                                                                      |

Bu girdi kümeleri göz önüne alındığında, artık Bölüm 3.2’de anlatıldığı gibi tasarım sürecini açıklamaya geçmeye hazırız. Bu bölümde, gereksinim toplama sürecinin yalnızca nihai sonuçlarını sunuyoruz. Bu gereksinimleri toplama işi önemsiz değildir, ancak bu bölümün kapsamı dışındadır.

## 4.3 Tasarım Süreci (The Design Process)

Artık gereksinimler ve iş (işletme) kaygıları dünyasından tasarım dünyasına sıçrama yapmaya hazırız. Bu, bir mimarın belki de en önemli görevidir: gereksinimleri tasarım kararlarına çevirmek. Elbette, başka birçok karar ve görev de önemlidir, ancak mimar olmanın özü, geniş kapsamlı sonuçlara sahip tasarım kararları vermektir.

### 4.3.1 ADD Adım 1: Girdileri Gözden Geçirme

nitelik temelli tasarım (Attribute-Driven Design, ADD) yöntemi içindeki ilk adım, girdilerin gözden geçirilmesini ve hangi gereksinimlerin sürücü (driver) olarak ele alınacağını (yani hangilerinin tasarım iş listesine (design backlog) dahil edileceğini) belirlemeyi içerir. Girdiler aşağıdaki tabloda özetlenmiştir.

| Kategori                         | Ayrıntılar                                                                                                                                                                             |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tasarım amacı (Design purpose)   | Bu, olgun (mature) bir alanda geliştirilen bir greenfield sistemdir. Amaç, sistemin inşasını desteklemek için yeterince ayrıntılı bir tasarım üretmektir.                             |
| Birincil işlevsel gereksinimler  | Bölüm 4.2.1’de sunulan kullanım senaryolarından (use cases) birincil olanlar şu şekilde belirlenmiştir:  UC-1: Çekirdek işi doğrudan desteklediği için  UC-2: Çekirdek işi doğrudan desteklediği için  UC-7: Bununla ilişkili teknik konular nedeniyle (bkz. QA-4) |

4.3 Tasarım Süreci

| Kategori                               | Ayrıntılar                                                                                                                                                                                                                  |
|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Kalite niteliği senaryoları (quality attribute scenarios) | Senaryolar Bölüm 4.2.2’de açıklanmıştır. Şimdi (Bölüm 2.4.2’de tartışıldığı gibi) aşağıdaki şekilde önceliklendirilmişlerdir: |

| Senaryo ID | Müşteri için önemi (Importance to the Customer) | Mimara göre gerçekleştirme zorluğu (Difficulty of Implementation According to the Architect) |
|------------|--------------------------------------------------|------------------------------------------------------------------------------------------------|
| QA-1       | Yüksek (High)                                   | Yüksek (High)                                                                                  |
| QA-2       | Yüksek (High)                                   | Orta (Medium)                                                                                  |
| QA-3       | Yüksek (High)                                   | Yüksek (High)                                                                                  |
| QA-4       | Yüksek (High)                                   | Yüksek (High)                                                                                  |
| QA-5       | Orta (Medium)                                   | Orta (Medium)                                                                                  |
| QA-6       | Orta (Medium)                                   | Düşük (Low)                                                                                    |

Bu listeden yalnızca QA-1, QA-2, QA-3 ve QA-4 sürücü (driver) olarak seçilmiştir.

| Kategori      | Ayrıntılar                                                                                               |
|---------------|----------------------------------------------------------------------------------------------------------|
| Kısıtlar      | Bölüm 4.2.3’te tartışılan tüm kısıtlar sürücü olarak dahil edilmiştir.                                   |
| Mimari kaygılar | Bölüm 4.2.4’te tartışılan tüm mimari kaygılar sürücü olarak dahil edilmiştir.                          |

### 4.3.2 Yineleme 1: Genel Bir Sistem Yapısının Oluşturulması

Bu bölüm, tasarım sürecinin ilk yinelemesinde ADD’in her bir adımında gerçekleştirilen etkinliklerin sonuçlarını sunmaktadır.

#### 4.3.2.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu, bir greenfield sistem tasarımındaki ilk yinelemedir; dolayısıyla yineleme hedefi, genel bir sistem yapısı oluşturma mimari kaygısı CNR-1’e ulaşmaktır (bkz. Bölüm 3.3.1).

Bu yineleme genel bir mimari kaygı tarafından yönlendiriliyor olsa da, mimar sistemin genel yapısını etkileyebilecek tüm sürücüleri akılda tutmalıdır. Özellikle, mimar aşağıdakilere dikkat etmelidir:

- QA-1: Performans (Performance)
- QA-2: Değiştirilebilirlik (Modifiability)
- QA-3: Kullanılabilirlik (Availability)
- QA-4: Performans (Performance)
- CON-2: Sisteme farklı platformlarda—Windows, OSX ve Linux—bir web tarayıcısı üzerinden erişilmelidir
- CON-3: İlişkisel bir veritabanı sunucusu kullanılmalıdır
- CON-4: Kullanıcı iş istasyonlarına ağ bağlantısı düşük bant genişliğine sahip olabilir ve güvenilir olmayabilir
- CRN-2: Ekibin Java teknolojileri konusundaki bilgisinden yararlanmak

82 Bölüm 4—Vaka Çalışması: FCAPS Sistemi

Time server

Açıklama (Legend):

ŞEKİL 4.2 FCAPS sistemi için bağlam diyagramı (context diagram)

#### 4.3.2.2 Adım 3: Ayrıntılandırılacak Bir veya Daha Fazla Sistem Ögesinin Seçilmesi

Bu bir greenfield geliştirme çalışmasıdır; bu nedenle bu durumda ayrıntılandırılacak öge, Şekil 4.2’de gösterilen tüm FCAPS sistemidir. Bu durumda ayrıntılandırma, parçalarına ayırma (decomposition) yoluyla gerçekleştirilir.

#### 4.3.2.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramının Seçilmesi

Bu ilk yinelemede, tüm sistemin yapılandırılması hedefi göz önüne alındığında, tasarım kavramları Bölüm 3.3.1’de sunulan yol haritasına göre seçilmiştir. Aşağıdaki tablo, tasarım kararlarının seçimini özetlemektedir. Bu vaka çalışmasında kullanılan tüm tasarım kavramlarının Ek A’da da açıklanmış olduğunu unutmayın.

| Tasarım Kararları ve Konumu                                         | Gerekçe (Rationale)                                                                                                                                                                                                                                                                                                                                                                                                      |
|----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sistemin istemci (client) kısmını Mantıksal olarak Zengin İstemci Uygulaması başvuru mimarisi (Rich Client Application reference architecture) kullanarak yapılandırma | Zengin İstemci Uygulaması (Rich Client Application, RCA) başvuru mimarisi (bkz. Bölüm A.1.2), kullanıcıların PC’lerine kurulmuş uygulamaların geliştirilmesini destekler. Bu uygulamalar, ağ topolojisini ve performans grafiklerini (UC-1) göstermek için gereken zengin kullanıcı arayüzü yeteneklerini destekler. Bu yetenekler, her ne kadar bu tasarım kararı sürücü olmasa da QA‑5’in gerçekleştirilmesine de yardımcı olur. Bu tür uygulamalar bir web tarayıcısında çalışmamakla birlikte (CON-2), Java Web Start gibi bir teknoloji kullanılarak bir web tarayıcısından kurulabilirler. |

> **💬 Çevirmen notu:** “Rich Client Application (RCA) reference architecture” burada bir mimari stil/başvuru mimarisi olarak kullanılıyor; kalıp isim olarak bırakılıp Türkçesi açıklama şeklinde verildi.

4.3 Tasarım Süreci

| Tasarım Kararları ve Konumu | Gerekçe (Rationale) |
|-----------------------------|----------------------|
| Elenen alternatifler (Discarded alternatives): |  |
| Alternatif                 | Elenme Nedeni (Reason for Discarding)                                                                                                                                                                                                 |
| Zengin İnternet uygulamaları (Rich Internet Applications, RIA) | Bu başvuru mimarisi (bkz. Bölüm A.1.3), web tarayıcısı içinde çalışan zengin kullanıcı arayüzlü uygulamaların geliştirilmesine yöneliktir. Bu tür bir uygulama zengin bir kullanıcı arayüzünü destekler ve kolayca yükseltilebilir olsa da, RIA çalıştırmak için gereken eklentilerin, Java Sanal Makinesi’ne (Java Virtual Machine) kıyasla daha az yaygın olduğu düşünülmüştür; bu nedenle bu seçenek elenmiştir. |
| Web uygulamaları (Web applications) |  |
