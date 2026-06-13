Modüller, tüm kullanım durumları (use case) ile ilişkilendirilmiş ve bir iş atama matrisi (work assignment matrix) oluşturulmuştur (gösterilmemiştir). Bu yeni yinelemede (iteration) tanıtılan modüllerin birim-testinin (unit testing) yapılmasına yönelik mimari kaygı, modüllerle ilişkili bileşenleri bağlamak için bir kontrolün tersine çevrilmesi (inversion of control) yaklaşımının kullanılmasıyla kısmen çözülmüştür.

## 4.3 Tasarım Süreci

### 4.3.4 Yineleme 3: Kalite Niteliği Senaryosu Sürücüsünün (QA-3) Ele Alınması

Bu bölüm, tasarım sürecinin üçüncü yinelemesinde nitelik temelli tasarımın (Attribute-Driven Design, ADD) her bir adımında gerçekleştirilen etkinliklerin sonuçlarını sunmaktadır. 1. ve 2. yinelemede alınan temel yapısal kararlara dayanarak artık en önemli bazı kalite niteliklerinin (quality attribute) yerine getirilmesi üzerinde düşünmeye başlayabiliriz. Bu yineleme, bu kalite niteliği senaryolarından yalnızca birine odaklanmaktadır.

#### 4.3.4.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu yineleme için mimar, QA-3 kalite niteliği senaryosuna odaklanmaktadır:

> Çalışma sırasında yönetim sisteminde bir arıza oluşur. Yönetim sistemi 30 saniyeden kısa sürede çalışmaya devam eder.

#### 4.3.4.2 Adım 3: Ayrıntılandırmak Üzere Sistemden Bir veya Daha Fazla Eleman Seçme

Bu kullanılabilirlik (availability) senaryosu için ayrıntılandırılacak elemanlar, birinci yineleme sırasında belirlenen fiziksel düğümlerdir:

- Uygulama sunucusu (application server)  
- Veritabanı sunucusu (database server)

#### 4.3.4.3 Adım 4: Seçilen Sürücüleri Karşılayan Bir veya Daha Fazla Tasarım Kavramı Seçme

Bu yinelemede kullanılan tasarım kavramları aşağıdaki gibidir:

| Tasarım Kararları ve Yeri | Gerekçe ve Varsayımlar |
| --- | --- |
| Uygulama sunucusunu ve veritabanı gibi diğer kritik bileşenleri çoğaltarak aktif yedeklilik (active redundancy) taktiğini tanıt | Kritik elemanlar çoğaltılarak (replication) sistem, çoğaltılan elemanlardan birinin arızasına işlevselliği etkilemeden dayanabilir. |
| Mesaj kuyruğu (message queue) teknoloji ailesinden bir eleman tanıt | Zaman sunucularından alınan tuzaklar (trap), mesaj kuyruğuna yerleştirilir ve sonra uygulama tarafından alınır. Kuyruğun kullanılması, tuzakların QA-1’deki gibi sırayla işlenmesini ve iletilmesini garanti edecektir. |

#### 4.3.4.4 Adım 5: Mimari Elemanları Örnekle, Sorumlulukları Tahsis Et ve Arayüzleri Tanımla

Örnekleme (instantiation) tasarım kararları aşağıdaki tabloda özetlenmiştir:

| Tasarım Kararları ve Yeri | Gerekçe |
| --- | --- |
| Mesaj kuyruğunu ayrı bir düğüme yerleştir (deploy) | Mesaj kuyruğunun ayrı bir düğüme yerleştirilmesi, bir uygulama arızası durumunda hiçbir tuzağın kaybolmamasını garanti edecektir. Bu düğüm, aktif yedeklilik taktiği kullanılarak çoğaltılır; ancak ağ cihazlarından gelen olayları yalnızca bir kopya alır ve işler. |
| Uygulama sunucusunda aktif yedeklilik ve yük dengeleme (load balancing) kullan | Herhangi bir anda iki uygulama sunucusu kopyası etkin olduğundan, yükü kopyalar arasında dağıtmak ve dengelemek mantıklıdır. Bu taktik, Yük Dengeli Küme (Load-Balanced Cluster) deseninin (pattern) kullanımıyla elde edilebilir (Bkz. Bölüm A.2.3). Bu, yeni bir mimari kaygıyı, CRN-5’i tanıtır: Kopyalarda durumu yönet (Manage state in replicas). |
| Yük dengeleme ve yedekliliği teknolojik destek kullanarak gerçekleştir | Yük dengeleme ve yedekliliğe yönelik birçok teknolojik seçenek, daha az olgun ve desteklenmesi daha zor olacak özel geliştirilmiş (ad hoc) bir çözüme gerek kalmadan uygulanabilir. |

Bu örnekleme kararlarının sonuçları bir sonraki adımda kaydedilmektedir.

#### 4.3.4.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 4.10, sisteme yedekliliğin eklenmesini içeren ayrıntılandırılmış (refined) bir dağıtım diyagramı (deployment diagram) göstermektedir.

```text
Server1 :ApplicationServer
«JDBC»
«replicated»
:LoadBalancer

pc :UserWorkstation

«replicated»
:Database Server

«HTTP»

«JDBC»

Server2 :ApplicationServer

«replicated»
:TrapReceiver
device1 :TimeServer
Relocatable IP address

FIGURE 4.10 Refined deployment diagram (Key: UML)

«SNMP»
```

Aşağıdaki tablo, daha önce (1. yinelemede) listelenmemiş elemanlara yönelik sorumlulukları açıklamaktadır:

| Eleman | Sorumluluk |
| --- | --- |
| LoadBalancer | İstemcilerden gelen istekleri uygulama sunucularına aktarır (ve yükü dengeler). Yük dengeleyici ayrıca istemcilere tekil bir IP adresi sunar. |
| TrapReceiver | Ağ cihazlarından tuzakları alır, bunları olaylara dönüştürür ve bu olayları kalıcı bir mesaj kuyruğuna koyar. |

Şekil 4.11’de gösterilen UML sıra diyagramı (sequence diagram), bu yinelemede tanıtılan TrapReceiver’ın, UC-2’yi (arızayı algıla — detect fault) desteklemek üzere dağıtım diyagramında gösterilen diğer elemanlarla nasıl mesaj alışverişi yaptığını göstermektedir. UC-2 hem QA-3 (kullanılabilirlik) hem de QA-1 (performans) ile ilişkilidir. Bu diyagramın amacı, fiziksel düğümler arasında gerçekleşen iletişimi göstermek olduğundan, metot isimleri yalnızca ön taslak niteliğindedir; sonraki yinelemelerde ayrıntılandırılacaktır.

```text
:NetworkDevice

:TrapReceiver

:ApplicationServer

pc :UserWorkstation

trap()

transformAndEnqueue(Event)
consume()
event()
publish(Event)

updateView()

FIGURE 4.11 Sequence diagram illustrating the messages exchanged between
the physical nodes to support UC-2 (Key: UML)
```

### 4.3.4.6 Adım 7: Mevcut Tasarımın Analizini Gerçekleştir ve Yineleme Hedefini ve Tasarım Amacının Gerçekleşmesini Gözden Geçir

Bu yinelemede QA-3’ü ele almak için önemli tasarım kararları alınmış ve bu kararlar QA-1’i de etkilemiştir. Aşağıdaki tablo, farklı sürücülerin durumunu ve yineleme boyunca alınan kararları özetlemektedir. Önceki yinelemede tamamen ele alınmış olan sürücüler tablodan çıkarılmıştır.

| Sürücü | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Boyunca Alınan Tasarım Kararları |
| --- | :---: | :---: | :---: | --- |
| QA-1 |  | X |  | Ayrı bir çoğaltılmış tuzak alıcı (trap receiver) düğümünün tanıtılması, uygulama sunucusunda bir arıza olması durumunda bile tuzakların %100’ünün işlenmesine yardımcı olabilir. Ayrıca, tuzak alımı ayrı bir düğümde gerçekleştirildiğinden, bu yaklaşım uygulama sunucusu işlem yükünü azaltır ve böylece performansa yardımcı olur. Belirli teknolojiler henüz seçilmediğinden, bu sürücü “kısmen ele alındı” olarak işaretlenmiştir. |
| QA-2 | X |  |  | İlgili bir karar alınmamıştır. |
| QA-3 |  | X |  | Uygulama sunucusunu yedekli hale getirerek sistemin arıza olasılığını azaltıyoruz. Ayrıca, yük dengeleyici arızalanırsa, pasif bir kopya gereken süre içinde etkinleştirilir. Belirli teknolojiler (örneğin mesaj kuyruğu) henüz seçilmediğinden, bu sürücü “kısmen ele alındı” olarak işaretlenmiştir. |
| QA-4 | X |  |  | İlgili bir karar alınmamıştır. |
| CON-1 |  |  | X | Uygulama sunucusunun çoğaltılması ve bir yük dengeleyicinin kullanılması, birden çok kullanıcı isteğinin desteklenmesine yardımcı olacaktır. |
| CON-4 | X |  |  | İlgili bir karar alınmamıştır. |
| CON-5 | X |  |  | İlgili bir karar alınmamıştır. |
| CON-6 | X |  |  | İlgili bir karar alınmamıştır. |
| CRN-2 | X |  |  | İlgili bir karar alınmamıştır. |
| CRN-4 | X |  |  | İlgili bir karar alınmamıştır. Bu yeni mimari kaygı bu yinelemede tanıtılmaktadır: kopyalarda durumu yönet (manage state in replicas). Bu noktada, ilgili bir karar alınmamıştır. |

## 4.4 Özet

> **💬 Çevirmen notu:** QA-* (quality attribute), CON-* (constraint — kısıt) ve CRN-* (concern — mimari kaygı) etiketleri, mimari sürücüleri sınıflandırmak için kullanılan adlandırma şemasıdır; ilerideki bölümlerde bu şema üzerine tekrar dönülmektedir.
