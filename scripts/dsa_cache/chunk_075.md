Hibernate, nesnelerin ilişkisel bir veritabanında kolayca kalıcı hale getirilmesini sağlar (ve farklı veritabanı (database) motorlarını destekler). Nesne–ilişkisel eşleme (object-relational mapping) kuralları, hibernate.cfg adlı bir XML dosyasında bildirime dayalı (declarative) olarak ya da kalıcı hale getirilmesi gereken sınıfların içinde yer alan notasyonlar (annotation) kullanılarak tanımlanır.

Hibernate, işlemleri (transaction) destekler ve veritabanından nesneleri almak için kullanılan HQL (Hibernate Query Language) adlı bir sorgu dili sağlar. Hibernate, performansı artırmak için çok seviyeli önbellekleme (multilevel caching) şemalarından yararlanır. Ayrıca, performansı artırmak ve kaynak tüketimini azaltmak için bağımlı nesnelerin tembel edinimini (lazy acquisition) sağlayan mekanizmalar sunar. Bu mekanizmalar yapılandırma (configuration) dosyalarında bildirime dayalı olarak (declarative) yapılandırılır.

### Yapı

Bu diyagram, yapılandırma dosyasındaki bilgileri kullanarak Hibernate çalışma zamanı (runtime) tarafından bir veritabanına kalıcı hale getirilen (persisted) bir varlığı (entity) göstermektedir (Anahtar: UML).

### Uygulanan tasarım desenleri (design pattern) ve taktikler (tactic)

**Desenler (Patterns):**

- Data Mapper
- Resource Cache
- Lazy Acquisition

**Taktikler (Tactics):**

- Uygunluk (availability): İşlemler (Transactions)
- Performans (performance): Verinin birden çok kopyasını tutma (önbellek, cache)

---

### A.6

| Framework Adı | Özet | Sayfa |
|--------------|------|-------|
| Hibernate    |      | 245   |

#### Yararlar (Benefits)

- Nesnelerin ilişkisel veritabanında kalıcı hale getirilmesini büyük ölçüde basitleştirir.

#### Sınırlamalar (Limitations)

- Karmaşık API
- JDBC (Java Database Connectivity)’den daha yavaş
- Eski (legacy) veritabanı şemalarına eşlemek güçtür.

---

### A.5.4 Java Web Start Framework

| Framework Adı | Java Web Start Framework |
|---------------|--------------------------|
| Teknoloji ailesi | Dağıtım mekanizması (deployment mechanism) |
| Dil | Java |
| URL | http://docs.oracle.com/javase/tutorial/deployment/webstart/ |

**Amaç (Purpose)**

Platformdan bağımsız, güvenli ve sağlam bir dağıtım teknolojisi sağlamak.

**Genel Bakış (Overview)**

Bir web tarayıcısı kullanarak son kullanıcılar standart (applet olmayan) Java uygulamalarını başlatabilir ve Java Web Start, bu uygulamaların en son sürümünün çalıştırıldığından emin olur. Bir uygulamayı başlatmak için kullanıcılar sayfadaki bir bağlantıya tıklar. Eğer uygulama ilk kez kullanılıyorsa, Java Web Start uygulamayı indirir. Uygulama daha önce kullanılmışsa, Java Web Start yerel kopyanın en güncel sürüm olup olmadığını doğrular ve onu başlatır ya da en yeni sürümü indirir.

### Yapı

Mevcut değil.

### Uygulanan tasarım desenleri (design pattern) ve taktikler (tactic)

- **Taktikler (Tactics):**
  - Güvenlik (security): Erişimi kısıtlama (limit access, sandbox)
  - Performans (performance): Verinin birden çok kopyasını tutma (önbellek, cache)

### Yararlar (Benefits)

- Uygulamalar bir korumalı alan (sandbox) içinde çalışır; ancak yerel dosyaları okuyup yazabilir.
- Uygulama önbelleğe alındığı için, bir kez indirildikten sonra başlangıç süresi büyük ölçüde kısalır.

### Sınırlamalar (Limitations)

- İlk başlatma biraz zaman alabilir.

---

### Özet (Summary)

Bu ekte, kurumsal uygulamalar (enterprise applications) uygulama alanı için bir tasarım kavramları kataloğu sunduk. Bu tür kataloglar, kurum düzeyinde faydalı varlıklar haline gelebilir ve 5. Bölüm’de kullandığımız Büyük Veri (Big Data) ya da mobil geliştirme gibi diğer uygulama alanları için de katalogların kolaylıkla hayal edilebileceğini söyleyebiliriz.

Burada sunulan katalog, 4. Bölüm’deki örnek olay incelemesinde (case study) kullanılan tasarım kavramlarını içerdiği için tükenmiş (exhaustive) olmak üzere tasarlanmamıştır. Gerçek bir katalog ise, daha fazla sayıda tasarım kavramı ve daha ayrıntılı açıklamalar içerir ve bir yazılım geliştirme organizasyonu için değerli bir varlık olurdu.

---

### A.7 Daha Fazla Okuma (Further Reading)

Referans mimariler (reference architecture) ve dağıtım desenleri (deployment pattern), Microsoft, *Application Architecture Guide* (2. baskı), Ekim 2009’dan alınmıştır.  
Taktikler kataloğu (tactics catalog) esas olarak L. Bass, P. Clements ve R. Kazman’ın *Software Architecture in Practice* (3. baskı), 2012 eserine dayanmaktadır. Bu taktiklerin bazıları daha önce şu kaynaklarda tanımlanmıştır: F. Bachmann, L. Bass ve R. Nord, “Modifiability Tactics”, SEI/CMU Technical Report CMU/SEI-2007-TR-002, 2007 ve J. Scott ve R. Kazman, “Realizing and Refining Architectural Tactics: Availability”, CMU/SEI-2009-TR-006, 2009.

Mimari desenler (architectural pattern), R. Buschmann, K. Henney ve D. Schmidt, *Pattern-Oriented Software Architecture, Volume 4*, Wiley, 2007’den alınmıştır.  
Spring framework’ü C. Walls, *Spring in Action* (4. baskı), Manning Publications, 2014’te ele alınmaktadır.  
Swing framework’ü J. Elliot, R. Eckstein, D. Wood ve B. Cole, *Java Swing* (2. baskı), O’Reilly Media, 2002’de ele alınmaktadır.  
Hibernate framework’ü ise C. Bauer ve G. King, *Java Persistence with Hibernate*, Manning Publications, 2015’te ele alınmaktadır.

---

# B Taktik Tabanlı (tactics-based) Anketler (Questionnaire)

Bu ekte, en önemli yedi kalite niteliği (quality attribute) için taktik tabanlı anketler sunuyoruz: uygunluk (availability), birlikte çalışabilirlik (interoperability), değiştirilebilirlik (modifiability), performans (performance), güvenlik (security), test edilebilirlik (testability) ve kullanılabilirlik (usability). Bu yedinin en önemlileri olduğunu nereden biliyoruz? Bu karar, SEI ATAM (Architecture Tradeoff Analysis Method) verilerinde, 15 yılı aşkın bir süre boyunca paydaşlardan (stakeholder) toplanan kalite niteliklerinin analizine dayanılarak verilmiştir.

Bu “ilk yedi”ye ek olarak, DevOps için de bir taktik tabanlı anket sunuyoruz; bu anket, kullanımınızı kendinize göre uyarlamanın ne kadar kolay olduğunu göstermek için değiştirilebilirlik, uygunluk, performans ve test edilebilirlikten gelen taktiklerin bir birleşimidir.

> **💬 Çevirmen notu:** ATAM, mimari kararların kalite nitelikleri üzerindeki etkisini inceleyen, SEI tarafından geliştirilmiş yapılandırılmış bir değerlendirme yöntemidir.

---

## B.1 Anketlerin Kullanılması

Bu anketler, her bir soruyu sırasıyla mimara yönelten ve yanıtları kaydeden bir analist tarafından, hafif (lightweight) bir mimari gözden geçirme (architecture review) aracı olarak kullanılabilir. Alternatif olarak, anketler, mimarinizi kendi başınıza incelemek için kullanabileceğiniz yansıtıcı (reflective) sorular kümesi olarak da kullanılabilir. Her iki durumda da, bu anketleri kullanmak için şu dört adımı izleyin:

1. Her taktik sorusu için, “Supported (Destekleniyor)” sütununu, taktik mimaride destekleniyorsa **Y**, aksi takdirde **N** ile doldurun. “Tactics Question (Taktik Sorusu)” sütunundaki taktik adı kalın (bold) olarak gösterilir.
2. “Supported” sütunundaki yanıt **Y** ise, “Design Decisions and Location (Tasarım Kararları ve Konumu)” sütununda, taktiği desteklemek için alınan belirli tasarım kararlarını açıklayın ve bu kararların mimaride nerede (hangi yerde) ortaya çıktığını (konumlandığını) belirtin. Örneğin, bu taktiği hangi kod modüllerinin, framework’lerin ya da paketlerin gerçekleştirdiğini (implement) belirtin.
3. “Risk” sütununda, taktiğin uygulanmasındaki beklenen/deneyimlenen zorluk ya da riski, (H = yüksek, M = orta, L = düşük) ölçeğini kullanarak belirtin. Örneğin, uygulanması orta zorlukta veya riskte olan (ya da henüz uygulanmadıysa orta zorlukta olacağı öngörülen) bir taktik M ile etiketlenir.
4. “Rationale (Gerekçe)” sütununda, alınan tasarım kararlarına ilişkin gerekçeyi (bu taktiği kullanmama kararı dahil) açıklayın. Bu kararın sonuçlarını kısaca açıklayın. Örneğin, kararın gerekçesini ve sonuçlarını maliyet, zaman çizelgesi (schedule), evrim (evolution) vb. üzerindeki etkileri açısından açıklayabilirsiniz.

---

## B.2 Uygunluk (Availability)

| # | Taktik Grubu (Tactics Group) | Taktik Sorusu (Tactics Question) |
|---|------------------------------|----------------------------------|
| 1 | Hata tespiti (Detect faults) | Sistem, bir bileşenin ya da bağlantının hatasını veya ağ tıkanıklığını (network congestion) tespit etmek için ping/echo kullanıyor mu? |
| 2 |                              |                                  |
