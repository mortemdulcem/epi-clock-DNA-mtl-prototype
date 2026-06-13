Sunum katmanına, ağ gösterimini
görüntülemek için gerekli bilgileri
sağlamaktan sorumludur.

**RequestManager**

Sunucu tarafı mantık ile
iletişimden sorumludur.

**RequestService**

İstemcilerden gelen istekleri alan
bir cephe (facade) sağlar.

**TopologyController**

Topolojik bilgiyle ilgili iş
mantığını (business logic) içerir.

**DomainEntities**

Etki alanı modelinden (domain model) kuruluşları (entity) içerir
(sunucu tarafı).

**TimeServerEventsController**

Olayların yönetimiyle ilgili iş
mantığını içerir.

**DataCollectionController**

Veri toplama ve
depolamayı gerçekleştirecek mantığı içerir.

**RegionDataMapper**

Bölgelerle ilgili kalıcılık (persistence)
işlemlerinden (CRUD) sorumludur.

**TimeServerDataMapper**

Zaman sunucularıyla ilgili kalıcılık
işlemlerinden (CRUD) sorumludur.

**EventDataMapper**

Olaylarla ilgili kalıcılık
işlemlerinden (CRUD) sorumludur.

**TimeServerConnector**

Zaman sunucuları ile iletişimden
sorumludur. Farklı türdeki zaman sunucularıyla iletişimi desteklemek için
zaman sunucularıyla yapılan işlemleri
soyutlar ve yalıtır (bkz. QA-2).

---

## 4.3 Tasarım Süreci

Aşağıdaki UC-1 ve UC-2 sıralama (sequence) diyagramları, arayüzleri tanımlamak için yöntemin önceki adımında (Bölüm 3.6’da tartışıldığı gibi) oluşturulmuştur. UC-7 için de benzer bir diyagram oluşturulmuştur, ancak yer kısıtı nedeniyle burada gösterilmemektedir.

### UC-1: Ağ Durumunu İzleme

Şekil 4.8, UC-1 (ağ durumunu izleme) için başlangıç niteliğinde bir sıralama diyagramı göstermektedir. Diyagram, kullanıcı sisteme başarıyla giriş yaptıktan sonra, başlangıçta topolojinin kullanıcı gösteriminin nasıl görüntülendiğini gösterir. Uygulama başlatıldığında, topoloji sunucudaki `TopologyController`dan istenir. Bu öğe, `RegionDataMapper` aracılığıyla kök bölgeyi (root region) alır ve istemciye döndürür. İstemci daha sonra `Region` sınıfı içindeki ilişkileri dolaşarak görünümü doldurabilir.

```
Client
:NetworkStatusMonitoringView

Server

:NetworkStatusMonitoringController

:RequestManager

:RequestService

:TopologyController

:RegionDataMapper

Technician

launch()
initialize()
requestTopology()
sendRequest(Request)
requestTopology()
retrieve(id) :Region
:Region
:Region
:Response
:Region
:boolean
getRootRegion() :Region

populateView()

interact()
```

**ŞEKİL 4.8** Kullanım durumu UC-1 için sıralama diyagramı (Anahtar: UML)

Sıralama diyagramında tanımlanan etkileşimlerden, etkileşimde bulunan
öğelerin arayüzleri için başlangıç yöntemleri tanımlanabilir:

---

### 4.3 Tasarım Süreci

#### Yöntem Adı

**Öğe: NetworkStatusMonitoringController**

`boolean initialize()`

Kullanıcıların etkileşimde bulunabilmesi için
ağ gösterimini açar.

`Region getRootRegion()`

Kök bölgeye ve bu nesnenin komşularına (tuzaklar
(traps) hariç) bir başvuru (reference) döndürür.

**Öğe: RequestManager**

`Region requestTopology()`

Topolojiyi ister. Bu yöntem, tüm topolojide
dolaşmanın mümkün olduğu kök bölgeye bir
başvuru döndürür.

**Öğe: RequestService**

`Response sendRequest(Request req)`

Bu yöntem bir isteği alır. Servis arayüzünde
sadece bu yöntem dışa açılmıştır. Bu durum,
mevcut servis arayüzünü değiştirmek zorunda
kalmadan gelecekte diğer işlevleri eklemeyi
kolaylaştırır.

**Öğe: TopologyController**

`Region requestTopology()`

Topolojiyi ister. Bu yöntem, tüm topolojide
dolaşmanın mümkün olduğu kök bölgeye bir
başvuru döndürür.

**Öğe: RegionDataMapper**

`Region retrieve(int id)`

Bir `Region`ı, kimliğinden (id) döndürür.

---

```
:TimeServerConnector

:TimeServerConfigurationController

:TimeServerDataMapper

:Time Server

:TopologyController

Time Server
addEventListener(this)
trap()
eventReceived(event)
publish(event)
retrieve(id) :TimeServer
:TimeServer
addEvent()

update(TimeServer)

:true
```

**ŞEKİL 4.9** Kullanım durumu UC-2 için sıralama diyagramı (Anahtar: UML)

### UC-2: Hata Algılama

Şekil 4.9, UC-2 (hata algılama) için başlangıç niteliğinde bir sıralama diyagramı göstermektedir ve sadece sunucu tarafındaki bileşenleri gösterir. Etkileşim, bir `TimeServer`ın bir tuzak (trap) göndermesiyle başlar; bu tuzak `TimeServerConnector` tarafından alınır. Tuzak bir `Event`e dönüştürülür ve `TimeServerConfigurationController`a gönderilir. `Event`, istemcilere yayınlanmak üzere `TopologyController`a eşzamansız (asynchronous) olarak gönderilir ve ardından kalıcı hale getirilir (persist edilir).

Bu etkileşimden, etkileşimde bulunan öğelerin arayüzleri için başlangıç
yöntemleri tanımlanabilir:

---

### 4.3 Tasarım Süreci

#### Yöntem Adı

**Öğe: TimeServerConnector**

`boolean addEventListener(EventListener el)`

Bu yöntem, iş mantığındaki bileşenlerin,
zaman sunucularından alınan olaylara dinleyici
(listener) olarak kendilerini kaydetmelerine
olanak tanır.

**Öğe: TimeServerConfigurationController**

`boolean eventReceived(Event evt)`

Bir olay alındığında çağrılan geriçağırım
(callback) yöntemidir.

**Öğe: TopologyController**

`publish(Event evt)`

Bu yöntem, yeni bir olay gerçekleştiğini
istemcilere bildirir.

**Öğe: TimeServerDataMapper**

`TimeServer retrieve(int id)`

Kimliğiyle (id) tanımlanan bir `TimeServer`ı
alır.

`boolean update(TimeServer ts)`

Bir `TimeServer`daki değişiklikleri kalıcı
hale getirir.

---

### 4.3.3.6 Adım 7: Mevcut Tasarımın Analizini Yap ve İterasyonu Gözden Geçir  
Amaç ve Tasarım Amacının Gerçekleşme Düzeyi

Bu iterasyonda alınan kararlar, işlevselliğin sistemde nasıl desteklendiğine dair
başlangıç niteliğinde bir anlayış sağlamıştır. Birincil kullanım durumlarıyla ilişkili modüller mimar tarafından, geri kalan işlevsellikle ilişkili modüller ise ekipteki başka bir üye tarafından tanımlanmıştır. Modüllerin tam listesinden, CRN-3’ü ele almak için bir iş atama tablosu (burada gösterilmemiştir) oluşturulmuştur.

Ayrıca, modül tanımlama çalışmasının bir parçası olarak yeni bir mimari kaygı (architectural concern) tanımlanmış ve Kanban panosuna eklenmiştir. Önceki iterasyonda tamamen ele alınan sürücüler (drivers) tablodan çıkarılmıştır.

---

### 4. Bölüm — FCAPS Sistemi: Vaka Çalışması

|                     | Henüz Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı |
|---------------------|--------------------|-------------------|---------------------|
| **Iterasyon Sırasında Alınan Tasarım Kararları** |                    |                   |                     |
| UC-1                |                    |                   | Katmanlar boyunca modüller ve bu kullanım durumunu destekleyecek ön taslak arayüzler tanımlanmıştır. |
| UC-2                |                    |                   | Katmanlar boyunca modüller ve bu kullanım durumunu destekleyecek ön taslak arayüzler tanımlanmıştır. |
| UC-7                |                    |                   | Katmanlar boyunca modüller ve bu kullanım durumunu destekleyecek ön taslak arayüzler tanımlanmıştır. |
| QA-1                |                    |                   | İlişkili kullanım durumunu (UC-2) destekleyen öğeler tanımlanmıştır. |
| QA-2                |                    |                   | İlişkili kullanım durumunu (UC-5) destekleyen öğeler tanımlanmıştır. |
| QA-3                |                    |                   | İlgili karar alınmamıştır. |
| QA-4                |                    |                   | İlişkili kullanım durumunu (UC-7) destekleyen öğeler tanımlanmıştır. |
| CON-1               |                    |                   | İlgili karar alınmamıştır. |
| CON-4               |                    |                   | İlgili karar alınmamıştır. |
| CON-5               |                    |                   | Verileri toplamaktan sorumlu modüller tanımlanmıştır. |
| CON-6               |                    |                   | Veri depolamadan sorumlu modüller tanımlanmıştır. |
| CRN-2               |                    |                   | Ek teknolojiler, ekibin bilgisi dikkate alınarak tanımlanmış ve seçilmiştir. |
| CRN-3               |                    |                   |  |
| CRN-4               |                    |                   |  |
