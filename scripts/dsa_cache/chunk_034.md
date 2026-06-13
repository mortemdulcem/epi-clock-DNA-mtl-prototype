Bu yinelemede, bu örnekte mimari tasarım desenleri (architectural design patterns) olan çeşitli tasarım kavramları, *Pattern Oriented Software Architecture, Volume 4* kitabından seçilir. Aşağıdaki tablo tasarım kararlarını özetlemektedir. Aşağıdaki tablodaki kalın yazılmış sözcükler bu kitaptaki mimari desenlere (architectural patterns) karşılık gelir ve Ek A’da bulunabilir.

**Tasarım Kararları ve Konumu** | **Gerekçe ve Varsayımlar**
---|---
Uygulama için bir Alan Modeli (Domain Model) oluştur | İşlevsel (fonksiyonel) bir ayrıştırmaya başlamadan önce, sistem için başlangıç niteliğinde bir alan modeli (domain model) oluşturmak, alandaki başlıca varlıkları ve bunların ilişkilerini tanımlamak gereklidir. Bunun için iyi bir alternatif yoktur. Bir alan modeli eninde sonunda oluşturulmak zorundadır; aksi takdirde, alttan alta, optimal olmayan bir biçimde ortaya çıkar; bu da anlaşılması ve bakımı zor, geçici çözümlerden oluşan (ad hoc) bir mimariye yol açar.
İşlevsel gereksinimlere karşılık gelen Alan Nesnelerini (Domain Objects) tanımla | Uygulamanın her bir ayrı işlevsel öğesinin, kendi içinde tamamlanmış bir yapı taşı—bir alan nesnesi (domain object)—içinde kapsüllenmesi gerekir. Olası bir alternatif, alan nesnelerini hiç dikkate almamak ve doğrudan katmanları modüllere ayrıştırmaktır; ancak bu, bir gereksinimin gözden kaçırılması riskini artırır.

## 4.3 Tasarım Süreci

**Tasarım Kararları ve Konumu** | **Gerekçe ve Varsayımlar**
---|---
Alan Nesnelerini genel ve uzmanlaşmış Bileşenlere (Components) ayrıştır | Alan nesneleri, işlevselliğin tam kümelerini temsil eder, ancak bu işlevsellik katmanlar içinde yer alan daha ince taneli (fine-grained) öğeler tarafından desteklenir. Bu desendeki “bileşenler (components)” bizim modül (module) olarak adlandırdığımız şeylere karşılık gelmektedir. Modüllerin uzmanlaşması, bulundukları katmanlarla ilişkilidir (örneğin, UI modülleri). İşlevselliği desteklemek için katmanların modüllere ayrıştırılmasına iyi bir alternatif yoktur.
Spring framework ve Hibernate kullan | Spring, kurumsal uygulama (enterprise application) geliştirmeyi desteklemek için yaygın olarak kullanılan bir framework’tür. Hibernate, Spring ile iyi bütünleşen bir nesne-ilişkisel eşleme (object-relational mapping, ORM) framework’üdür. Uygulama geliştirme için değerlendirilen bir alternatif JEE idi. Spring, daha “hafif” (lightweight) olarak değerlendirildiği ve geliştirme ekibi zaten Spring’e aşina olduğu için, daha yüksek ve daha erken ortaya çıkan bir üretkenlik sağlayacağından, nihai olarak seçilmiştir. Diğer ORM framework’leri dikkate alınmamıştır; çünkü geliştirme ekibi zaten Hibernate’e aşinaydı ve onun performansından memnundu.

### 4.3.3.4 Adım 5: Mimari Ögeleri Örnekle, Sorumlulukları Ayır ve Arayüzleri Tanımla

Bu yinelemede verilen örnekleme (instantiation) tasarım kararları aşağıdaki tabloda özetlenmektedir:

**Tasarım Kararları ve Konumu** | **Gerekçe**
---|---
Yalnızca başlangıç niteliğinde bir alan modeli oluştur | Birincil kullanım senaryolarında (use case) yer alan varlıkların tanımlanması ve modellenmesi gerekir, ancak tasarımın bu aşamasını hızlandırmak için yalnızca başlangıç niteliğinde bir alan modeli oluşturulur.
Sistem kullanım senaryolarını alan nesnelerine eşle | Alan nesnelerinin başlangıç niteliğinde bir tanımlaması, sistemin kullanım senaryoları analiz edilerek yapılabilir. CRN-3’ü ele almak için, Bölüm 4.2.1’deki tüm kullanım senaryoları için alan nesneleri tanımlanır.
Alan nesnelerini katmanlara dağıtarak katmana özgü, açık bir arayüze sahip modülleri tanımla | Bu teknik, tüm işlevleri (functionalities) destekleyen modüllerin tanımlanmasını garanti eder. Mimar bu görevi sadece birincil kullanım senaryoları için yerine getirecektir. Bu, bir başka ekip üyesinin geri kalan modülleri tanımlamasına olanak tanır; böylece iş ekip üyeleri arasında paylaştırılmış olur. Modül kümesi oluşturulduktan sonra mimar, bu modülleri test etme ihtiyacını fark eder ve burada yeni bir mimari kaygı (architectural concern) tanımlanır: **CRN-4: Modüllerin çoğunluğu birim testi (unit test) ile test edilmelidir.** Bu kaygı yalnızca “modüllerin çoğunluğunu” kapsamaktadır; çünkü kullanıcı arayüzü işlevselliğini gerçekleştiren modüllerin, bağımsız olarak test edilmeleri zordur.

**Tasarım Kararları ve Konumu** | **Gerekçe**
---|---
Modüllerle ilişkili bileşenleri Spring framework kullanarak bağla | Bu framework, tersine denetim (inversion of control, IoC) yaklaşımı kullanır; bu sayede farklı yönlerin (aspects) desteklenmesi ve modüllerin birim testine tabi tutulabilmesi (CRN-4) mümkün olur.
Veri katmanındaki bir modülle framework’leri ilişkilendir | ORM eşlemesi (mapping), veri katmanında yer alan modüllerin içine kapsüllenmiştir. Daha önce seçilmiş olan Hibernate framework’ü bu modüllerle ilişkilendirilir.

Yöntemin bu adımında yapılar ve arayüzler tanımlanır, ancak bunlar bir sonraki adımda kayda geçirilir.

### 4.3.3.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

5. adımda verilen kararlara bir sonuç olarak çeşitli diyagramlar oluşturulur.

- Şekil 4.5, sistem için başlangıç niteliğinde bir alan modelini göstermektedir.
- Şekil 4.6, Bölüm 4.2.1’deki kullanım senaryosu modeline göre örneklenen alan nesnelerini göstermektedir.
- Şekil 4.7, iş nesnelerinden (business objects) türetilmiş ve birincil kullanım senaryolarıyla ilişkilendirilmiş modülleri içeren bir modül görünümünün (module view) taslağını göstermektedir. Açık arayüzler (explicit interfaces) gösterilmemiştir, ancak bunların var olduğu varsayılmıştır.

Şekil 4.7’de tanımlanan ögelerin sorumlulukları, 95. sayfada başlayan tabloda özetlenmektedir.

## 4.3 Tasarım Süreci

```text
0..*

-

Event

Time Server

Region

-

name

generates

deviceName
ipAddress
model

1

-parent

0..* -

date
payload
severity
type
0..*

1..*
acknowledges

1

1

Configuration
-

Performance Data

configurationParameters

-

User

delay: DataSet
jitter: DataSet
offset: DataSet

-

login
password
permissions
type
```

**ŞEKİL 4.5** Başlangıç alan modeli (Anahtar: UML)

```text
«domain object»
Network Status Monitoring

«domain object»
Event history

«domain object»
Fault Detection

responsibilities

responsibilities

responsibilities

UC-1

UC-2

UC-3

«domain object»
Time Server Management

«domain object»
Time Server Configuration

«domain object»
System Access

responsibilities

UC-4

UC-5
UC-6

responsibilities
UC-10

«domain object»
Performance Data and Information Display

«domain object»
Performance and Data Collection

«domain object»
User Management

responsibilities

responsibilities
UC-11

responsibilities

responsibilities
UC-8
UC-9

UC-7
```

**ŞEKİL 4.6** Kullanım senaryosu modeliyle ilişkilendirilmiş alan nesneleri (Anahtar: UML)

> **💬 Çevirmen notu:** “responsibilities” etiketleri, her domain nesnesinin hangi kullanım senaryolarının gerçekleştirilmesinden sorumlu olduğunu gösterir. UC-1, UC-2 vb. kullanım senaryosu (use case) kimlikleridir.

```text
Client Side

«Layer»
Presentation CS

NetworkStatusMonitoringView

«Layer»
Business logic CS

NetworkStatusMonitoringController

«Layer»
Data CS
RequestManager

Server Side

«Layer»
Services SS

«facade»
RequestService

«Layer»
Business Logic SS
TopologyController
DomainEntities

TimeServerEventsController

DataCollectionController

«Layer»
Data SS

RegionDataMapper

TimeServerDataMapper

EventDataMapper

TimeServerConnector
```

**ŞEKİL 4.7** Birincil kullanım senaryolarını destekleyen modüller (Anahtar: UML)

## 4.3 Tasarım Süreci

**Öge** | **Sorumluluk**
---|---
NetworkStatusMonitoringView | Ağ gösterimini (network representation) görüntüler ve olaylar alındığında bu gösterimi günceller. Bu bileşen, başvuru mimarisindeki (reference architecture) hem UI bileşenlerini hem de UI işlem (process) bileşenlerini somutlaştırır.
NetworkStatusMonitoringController |
