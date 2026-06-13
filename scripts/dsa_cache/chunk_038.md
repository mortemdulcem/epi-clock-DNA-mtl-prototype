Sistem son 60 güne ait ham veriyi saklamalıdır (günde yaklaşık 1 TB ham veri, toplamda yaklaşık 60 TB).

UC-4

Senaryo

İlgili
Kullanım Durumu

(devamı)

110

Bölüm 5—Vaka Çalışması: Büyük Veri Sistemi

ID

Kalite
Niteliği

Senaryo

İlgili
Kullanım Durumu

QA-8

Ölçeklenebilirlik (scalability)

Sistem, 1 yıl boyunca dakika bazında
toplanmış (aggregate) veriyi (yaklaşık
40 TB) ve 10 yıl boyunca saat bazında
toplanmış veriyi (yaklaşık 50 TB) saklamalıdır.

UC-3, 4, 6

QA-9

Genişletilebilirlik (extensibility)

Sistem, yeni veri kaynaklarının sadece
bir yapılandırma güncellenerek, devam
eden veri toplama işlemini kesintiye
uğratmadan eklenmesini desteklemelidir.

UC-1, 2, 5

QA-10

Kullanılabilirlik (availability)

Sistem, herhangi bir tekil düğüm veya
bileşen arızalandığında kesinti olmaksızın çalışmaya devam etmelidir.

Tüm
kullanım
durumları

QA-11

Konuşlandırılabilirlik (deployability)

Sistemin konuşlandırma prosedürü
tamamen otomatikleştirilmeli ve geliştirme, test ve üretim ortamları gibi bir
dizi ortamı desteklemelidir.

Tüm
kullanım
durumları

### 5.2.3 Kısıtlar (constraints)

Sistemle ilişkili kısıtlar aşağıdaki tabloda sunulmaktadır.

ID  

Kısıt

CON-1

Sistem esas olarak (maliyet nedenleriyle) açık kaynak teknolojilerden
oluşmalıdır. Özel mülkiyet (proprietary) teknoloji kullanmanın değer/
maliyet oranının çok daha yüksek olduğu bileşenler için, özel mülkiyet
teknolojisi kullanılabilir.

CON-2

Sistem, statik raporlar için (örneğin, MicroStrategy, QlikView, Tableau)
SQL arabirimli kurumsal BI (iş zekâsı) aracını kullanmalıdır.

CON-3

Sistem iki belirli konuşlandırma ortamını desteklemelidir:
özel bulut (VMware vSphere Hypervisor ile) ve genel bulut
(Amazon Web Services). Konuşlandırma sağlayıcısını mümkün olduğunca
bağımsız (vendor-agnostic) tutmak için mimari ve teknoloji kararları
buna göre verilmelidir.

### 5.2.4 Mimari Kaygılar (architectural concerns)

Ele alınan başlangıç mimari kaygılar aşağıdaki tabloda gösterilmiştir.

ID  

Kaygı

CRN-1

Bu bir sıfırdan geliştirilen (greenfield) sistem olduğundan, başlangıç
için genel bir yapı oluşturulması.

CRN-2

Ekibin Apache Büyük Veri ekosistemi konusundaki bilgisinden
yararlanma.

## 5.3 Tasarım Süreci

111

### 5.3 Tasarım Süreci

Gereksinimleri sıraladığımıza göre, şimdi ADD (Attribute-Driven Design, nitelik temelli tasarım) yönteminin ilk yinelemesine başlamaya hazırız. Bu, nispeten yeni bir alanda, sıfırdan geliştirilen bir sistemdir. Bu nedenle, olgun alanlardaki sıfırdan sistemler için tasarım yol haritasını (Bölüm 3.3.1’de tartışıldığı gibi) izliyoruz; ancak Büyük Veri alanına özgü, teknolojilerin hızlı ortaya çıkışı ve evrimi gibi belirsizlikleri ele almak için bazı uyarlamalarla.

#### 5.3.1 ADD Adım 1: Girdileri Gözden Geçirme

Yöntemin ilk adımı girdilerin gözden geçirilmesini içerir. Bunlar aşağıdaki tabloda özetlenmiştir.

Kategori  

Ayrıntılar

Tasarım
amacı

Bu, nispeten yeni bir alandaki sıfırdan (greenfield) bir sistemdir. Kuruluş, geliştiricilerin gerçek dünyadan hızlı biçimde geri bildirim alıp sistemi değiştirmeye devam edebilmesi için kısa yinelemeli çevik (Agile) bir süreç izleyecektir. Aynı zamanda, mimari sürücüleri (architectural driver) karşılamaya yönelik bilinçli kararlar vermek ve gereksiz yeniden çalışmayı (rework) önlemek için bir mimari tasarıma ihtiyaç vardır.

Birincil
işlevsel
gereksinimler

Bölüm 5.2.1’de sunulan kullanım durumları arasından aşağıdakiler
birincil olarak belirlenmiştir:
- UC-1  
- UC-2  
- UC-3  
- UC-4  

Kalite
niteliği
senaryoları

Aşağıdaki tablo, birincil kalite niteliği (quality attribute) senaryolarının, müşteri ve mimar tarafından sıralanan önceliklerini (Bölüm 3.3.2’de tartışıldığı gibi) göstermektedir. Daha düşük öncelikli kalite niteliği senaryolarının da mevcut olduğuna dikkat edin, fakat burada gösterilmemiştir.

Senaryo
ID

Müşteri
İçin Önem

Mimarın Değerlendirmesine Göre
Gerçekleştirme Zorluğu

QA-1

Yüksek

Yüksek

QA-2

Yüksek

Orta

QA-3
QA-4
QA-5
QA-6
QA-7
QA-8
QA-9
QA-10

Orta
Yüksek
Orta
Orta
Orta
Yüksek
Yüksek
Yüksek

Orta
Yüksek
Yüksek
Orta
Orta
Orta
Orta
Orta

QA-11

Orta

Yüksek
(devamı)

112

Bölüm 5—Vaka Çalışması: Büyük Veri Sistemi

Kategori  

Ayrıntılar

Kısıtlar

Bkz. Bölüm 5.2.3.

Mimari
kaygılar

Bölüm 5.2.4’te sunulan mimari kaygıların tümü sürücü (driver)
olarak dâhil edilmiştir.

> **💬 Çevirmen notu:** Burada “sürücü (driver)” terimi, mimariyi yönlendiren gereksinim, kısıt ve kaygıları ifade eden “architectural driver” kavramının kısaltılmış kullanımıdır.

### 5.3.2 Yineleme 1: Referans Mimari ve Genel Sistem Yapısı

Bu bölüm, tasarım sürecinin ilk yinelemesinde ADD yönteminin her adımında gerçekleştirilen faaliyetlerin sonuçlarını sunmaktadır.

#### 5.3.2.1 Adım 2: Sürücüleri Seçerek Yineleme Hedefini Belirleme

Bu, sıfırdan geliştirilen bir sistemin tasarımındaki ilk yinelemedir; dolayısıyla yinelemenin hedefi, sistem için başlangıç niteliğinde genel bir yapı oluşturmaktır (CRN-1). Bu ilk yineleme genel bir mimari kaygı tarafından yönlendiriliyor olsa da, mimar tüm sürücüleri, özellikle de kısıtları ve kalite niteliklerini aklında tutmalıdır:

- CON-1: Uygun olduğu her durumda açık kaynak teknolojilerden yararlan  
- CON-2: Statik raporlar için SQL arabirimli kurumsal BI aracını kullan  
- CON-3: İki konuşlandırma ortamı: özel ve genel bulutlar  
- QA-1, 2, 3, 4, 5: Performans  
- QA-6, 7, 8: Ölçeklenebilirlik  
- QA-9: Genişletilebilirlik  
- QA-10: Kullanılabilirlik  
- QA-11: Konuşlandırılabilirlik  

#### 5.3.2.2 Adım 3: Sistemin Ayrıntılandırılacak Bir veya Daha Fazla Ögesini Seçme

Yine, bu bir sıfırdan geliştirme (greenfield development) olduğundan ve başlangıç yinelemesinde bulunduğumuzdan, ayrıntılandırılacak öge tüm sistemdir.

#### 5.3.2.3 Adım 4: Seçilen Sürücüleri Karşılayacak Bir veya Daha Fazla Tasarım Kavramı Seçme

Bu yinelemede tasarım kavramları, çeşitli veri analitiği referans mimarilerinden seçilmektedir (bu tür referans mimarilerin bir listesi, Smart Decisions Game tasarım kavramları kataloğunda bulunabilir; daha fazla bilgi için “Daha Fazla Okuma” bölümüne bakınız).

## 5.3 Tasarım Süreci

Tasarım
Kararları ve
Konumu

Uygulamayı
Lambda
(referans)
mimarisinin
bir örneği
(instance) olarak
inşa et
