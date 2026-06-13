## 📝 Çevirmen Eki — Üst Ekstremite Yaralanmaları (Upper Extremities)

### 🔬 İleri ve Niş Bilgiler

#### 1. Güncel araç güvenlik sistemleri ve üst ekstremite yaralanmaları

Bölüm ağırlıklı olarak klasik (çoğunlukla sürücü hava yastığı ve emniyet kemeri dönemine ait) veriler üzerine kurulu. Oysa günümüzde:

- **Çok kademeli / akıllı hava yastıkları (multi‑stage, smart airbags)**:
  - Çarpma hızı, emniyet kemeri kullanım durumu, işgalci sınıflandırma sensörleri (occupant classification) ve oturma pozisyonuna göre açılma hızı ve basıncı modüle edilebiliyor.
  - Özellikle **ince yapılı, kısa boylu ve direksiyona çok yakın oturan sürücülerde** (çoğunlukla kadın ve yaşlı sürücüler) üst ekstremiteye gelen erken faz darbenin şiddetini azaltmak için sensör temelli tetik algoritmaları geliştirildi.
  - Bu sistemler, erken dönem “agresif” hava yastıklarının rapor edilen önkol ve el yaralanmalarını belirgin ölçüde azaltmış durumda; ancak **düşük hızlı çarpmalarda** nispeten “hafif” ama fonksiyonel olarak önemli el-bilek travmaları tamamen ortadan kalkmış değil.

- **Yan hava yastıkları ve perde (curtain) sistemleri**:
  - Ön kol, omuz ve klavikula yaralanmalarının önemli bir kısmı artık **yan çarpışmalarda** (T‑bone) ve devrilmelerde (rollover) ortaya çıkıyor.
  - Ön cam ile birlikte perde hava yastığı, özellikle **dışta (outboard) oturan yolcunun** omuz/klavikula bölgesine yeni bir yükleme paterni getiriyor. Klavikula üzerinden “kuşaklama” yapan emniyet kemeri ve perde airbag birlikte:
    - Klavikula kırığı,
    - Akromiyoklaviküler eklem yaralanmaları,
    - Distal klavikula osteolizinin travma sonrası hızlanmış formu
    açısından risk oluşturabiliyor.

- **Direksiyon kolon tasarımları**:
  - Daha eski literatürde direksiyon kolonunun rijitliği ve geri çekilme (collapse) miktarı üst ekstremite yaralanmalarında kritik bir faktörken, modern kolonların **enerji emici tasarımları** ve direksiyonun çarpışma sırasında kontrollü geri çekilmesi, humerus ve önkol kırığı sıklığını sınırlamış durumda.
  - Buna karşın, **sürücünün direksiyonu sıkı kavramış olması**:
    - Humerus spiral kırığı,
    - Proksimal humerus metafiz kırığı,
    - Glenohumeral çıkık ve labrum yaralanmaları
    için halen önemli bir mekanizma. Özellikle frenleme sırasında üst ekstremitenin ekstansiyon + dış rotasyon + abduksiyon kombinasyonunda kilitlendiği durumlarda bu risk daha da artıyor.

#### 2. Üst ekstremite için özgül biyomekanik ve deneysel modeller

Bölüm, Messerer ve tarihsel çalışmalar üzerinden ilerliyor; güncel biyomekanik literatürde ise:

- **Yalnız başına kemik değil, “segment” (kemik + yumuşak doku) düzeyinde deneyler**:
  - Hem taze donmuş kadavra örnekleri hem de hayvan modelinden elde edilen verilerle, özellikle:
    - **Radius‑ulna çiftinin** eksenel yüklenme, bükülme (bending) ve torsiyon altındaki davranışı,
    - **Humerusun** hem eksenel kompresyon hem de “bending‑torsion” kombinasyonlarında kırılma momentleri çalışılıyor.
  - Bu deneyler, klasik “statik” kırılma limitlerinin, **yükleme hızı (strain‑rate)** arttığında anlamlı biçimde yükseldiğini göstermiş durumda (yüksek hızda **dinamik güçlenme**, dynamic strengthening).

- **Kavrama (grip) kuvveti ve bilek pozisyonunun önemi**:
  - Direksiyon, tenis raketi, beyzbol sopası veya golf sopası tutarken:
    - Bileğin ekstansiyon/fleksiyon açısı,
    - Pronasyon/supinasyon derecesi,
    - Kavrama kuvveti,
  üst ekstremitedeki yük transferini belirleyen temel parametreler.
  - Bu nedenle aynı hava yastığı veya aynı darbe şiddeti altında:
    - Direksiyona gevşekçe temas eden bir elde **yumuşak doku kontüzyonu**,
    - Sıkı kavrayan bir elde ise **metakarp kırığı, skafoid kırığı** veya distal radius kırığı görülebiliyor.

- **Ara eklem düzeyi hasarlar**:
  - Klavikula ve humerus kırıkları kadar, **rotator manşet yırtıkları**, Bankart/SLAP lezyonları ve biseps uzun başı tendinopatileri de travma sonrası fonksiyon kaybında önemli; ancak klasik trafik kazası istatistikleri bunları yeterince yakalamıyor.
  - İleri görüntüleme (MR, artrografi) erişimi arttıkça, özellikle **düşük hızlı çarpışmalarda**:
    - “Whiplash” eşdeğeri üst ekstremite yaralanmaları,
    - Mikroinstabilite ve kapsül‑ligament kompleksinin subklinik hasarları
    daha sık tanınmaya başlanmıştır.

- **Sonlu elemanlar (Finite Element) insan modelleri**:
  - GHBMC (Global Human Body Models Consortium) ve THUMS (Total Human Model for Safety) gibi bütüncül insan modellerinde, artık:
    - Humerus, radius, ulna ve eldeki majör kemikler,
    - Omuz kuşağı ve kol kasları (örneğin biseps, triseps, deltoid),
    - Ana ligament yapıları
    detaylı olarak modellenmiş durumda.
  - Bu modeller, örneğin:
    - Hava yastığı açılım fazında **el‑önkol temasının**,
    - Yan çarpışmada **omuz ve klavikula yüklenmesinin**,
    - Motor sporları ve kask‑direksiyon etkileşiminde **üst ekstremiteye gelen sekonder darbenin**
    tahmini için kullanılıyor.
  - Ancak, üst ekstremite özelinde model doğrulaması (validation), alt ekstremite ve toraks kadar iyi çalışılmış değil; dolayısıyla elde edilen sonuçların **analitik destek** ve **deneysel verilerle** teyidi hâlâ şart.

#### 3. Spor travmaları ile otomotiv yaralanmalarının kesişim alanları

Bölüm, spor yaralanmalarının üst ekstremite için daha çok çalışılmış olduğuna değiniyor; burada önemli bir mühendislik ve klinik köprü var:

- **Atma (throwing) biyomekaniği**:
  - Pitching (beyzbol), hentbol, voleybol servis hareketi gibi yüksek hızda humerus rotasyonu gerektiren hareketlerin kinematikleri, otomotiv çarpışmasında:
    - Direksiyonda elleri saat 10‑2 pozisyonunda,
    - Frenleme sırasında kolların ekstansiyon + abduksiyonda kilitlendiği
    senaryolar için benzer kas kuvveti ve tork profilleri gösteriyor.
  - Bu nedenle, bazı humerus kırıklarının **kontaktansız** (ya da minimal kontakla) yalnızca kas kuvvetleri ile oluşabileceğine ilişkin otomotiv literatürü, spor biyomekaniği ile uyumlu.

- **Overuse (tekrar yükleme) vs akut travma**:
  - Özellikle profesyonel sporcularda:
    - Labral yırtıklar,
    - Rotator manşet dejenerasyonu,
    - Ulnar kollateral ligaman (UCL) gevşekliği
    gibi önceden mevcut mikrohasarlar, trafik kazasında görece “küçük” bir travmayla klinik olarak belirgin hale gelebiliyor.
  - Klinik ve adli değerlendirmede, **pre‑existing (önceden var olan) patolojilerin** kazayla ilişkisi dikkatle sorgulanmalı; aksi halde kazaya tüm patolojinin sebebiymiş gibi atıf yapılması mediko‑legal hatalara yol açabiliyor.

#### 4. Cinsiyet, yaş ve kemik kalitesi

Bölüm, kadınlarda daha yüksek AIS2+ üst ekstremite yaralanma riskine değiniyor; güncel bakışta:

- **Düşük kemik mineral yoğunluğu (BMD)**:
  - Özellikle postmenopozal kadınlarda, distal radius ve proksimal humerus kırıkları için **nispeten düşük enerji düzeyinde** bile kırık gelişebiliyor.
  - Bu nedenle, aynı çarpışma şiddetinde:
    - Genç erkek sürücüde yalnızca yumuşak doku kontüzyonu,
    - Yaşlı kadın sürücüde humerus veya distal radius kırığı
    görülebiliyor.
- **Vücut boyu ve “out‑of‑position” (OOP) riskleri**:
  - Kısa boylu sürücüler direksiyona ve hava yastığına daha yakın oturmak zorunda kalıyor. Bu durum:
    - Hava yastığının açılışının erken fazında (yüksek gaz jet ve cover temas fazı),
    - Önkol ve elin daha yüksek hızda darbeye maruz kalmasına
    yol açabiliyor.
  - Modern occupant‑classification sistemleri ve OOP sensörleri bu riskleri azaltmayı hedeflese de, **yanlış pozisyonda oturma** (çok öne eğilme, direksiyonu üstten kavrama gibi) hâlâ önemli bir risk faktörü.

---

### ⚖️ Türkiye / Mediko‑legal & Mühendislik Bağlamı

#### 1. Trafik kazaları ve üst ekstremite yaralanmalarının adli değerlendirilmesi

- **Adli Tıp Kurumu (ATK) uygulamaları**:
  - Üst ekstremite yaralanmalarında:
    - Yaralanmanın niteliği (kırık, çıkık, sinir kesisi vb.),
    - Taraf (dominant/nondominant),
    - Meslek ve günlük aktivitelerde fonksiyonel kısıtlılık
    dikkate alınarak **iş göremezlik oranı** belirleniyor.
  - Örneğin:
    - Dominant elde metakarp kırığı sonrası hareket kısıtlılığı,
    - Dirsek çevresi eklem içi kırık ve kısıtlı fleksiyon‑ekstansiyon,
    - Rotator manşet yırtığına bağlı kronik güç kaybı,
    ciddi ve kalıcı mesleki kısıtlılık yaratabiliyor.
  - ATK’nın *Maluliyet Tespit Rehberi* ve SGK’nın maluliyet oranı belirleme esasları, bu bağlamda başlıca referanslar.

- **Karayolları Trafik Kanunu ve tazminat**:
  - 2918 sayılı **Karayolları Trafik Kanunu** ve ilgili ikincil mevzuat çerçevesinde:
    - Üst ekstremite yaralanmaları, özellikle kalıcı fonksiyon kaybı yaratıyorsa, **sürekli sakatlık (permanent disability)** tazminatı hesaplarında merkezi bir rol oynuyor.
  - Trafik bilirkişiliğinde:
    - Yaralanmanın **araç içi kinematikle uyumlu olup olmadığı**,
    - Emniyet kemeri ve hava yastığı kullanım durumu,
    - Çarpışma yönü ve hızına göre **beklenen yaralanma paterni**,
    değerlendirilerek hem kusur oranı hem de olay kurgusu (koltuk konumu, oturuş şekli, direksiyon kavrama vb.) yeniden inşa ediliyor.

- **İşgücü kaybı ve meslek seçimi**:
  - Özellikle:
    - El becerisine dayalı mesleklerde (cerrah, diş hekimi, ressam, tekstil işçisi),
    - Üst ekstremiteyi yoğun kullanan işlerde (inşaat, montaj hattı, kaynak, makine operatörlüğü),
    küçük görülen üst ekstremite yaralanmaları bile ciddi **meslek değişikliği** veya **erken emeklilik** gerektirebiliyor.
  - Bu nedenle adli ve sigorta süreçlerinde:
    - Yaralanma sonrası **mesleki rehabilitasyon imkânı**,
    - Meslek değiştirme potansiyeli,
    gibi faktörler de değerlendirmeye dahil edilmeli.

#### 2. İş kazaları, İSG ve üst ekstremite

- **6331 sayılı İş Sağlığı ve Güvenliği Kanunu**:
  - Üst ekstremite yaralanmaları, özellikle:
    - Pres ve makine kazaları (el sıkışması, kesilmesi),
    - Yüksekten düşme (FOOSH — fall on outstretched hand),
    - Malzeme taşıma ve elleçleme,
    sırasında iş kazalarının önemli bir bölümünü oluşturuyor.
  - Travma‑biyomekaniği perspektifinden:
    - Klasik FOOSH mekanizması ile **distal radius, skafoid ve dirsek çevresi** kırıkları,
    - Ağır yük düşmesi ile **metakarp ve falanks kırıkları**,
    sık görülüyor.
  - Bu kazalarda, işverenin **makine koruyucuları, kişisel koruyucu donanım ve eğitim** yükümlülükleri yanında:
    - İşin niteliğini,
    - Çalışanın yaşı, deneyimi ve sağlık durumunu
    dikkate alıp almadığı da adli değerlendirmede önem kazanıyor.

- **Meslek hastalığı ve overuse**:
  - Tekrarlayan hareketlerle ilişkili üst ekstremite sorunları (karpal tünel sendromu, lateral epikondilit, rotator manşet tendinopatileri) esasen kronik yüklenme problemleri olmakla birlikte, **akut travma sonrası alevlenme veya belirginleşme** sık görülen bir senaryo.
  - Mediko‑legal açıdan:
    - Mevcut kronik patolojinin kazayla ne ölçüde ağırlaştığı,
    - “İlliyet bağı” (causality) derecesi,
    bilimsel raporlar ve görüntülemeler eşliğinde titizlikle değerlendirilmelidir.

#### 3. Spor yaralanmaları ve adli boyut

- **Spor federasyonları, kulüpler ve sorumluluk**:
  - Özellikle kontak sporlarında (futbol, basketbol, hentbol, güreş) üst ekstremite yaralanmaları yaygındır:
    - Önkol ve el kırıkları,
    - Omuz çıkıkları ve rekürren instabilite,
    - Rotator manşet yırtıkları.
  - Profesyonel sporcularda:
    - Kulüp doktoru,
    - Antrenör,
    - Tesis ve ekipman güvenliğinden sorumlu kişiler,
    belirli koşullarda hukuki sorumlulukla karşı karşıya kalabilmektedir.
  - Değerlendirme aşamasında:
    - Olayın oyun kuralları içinde mi yoksa **kurallara aykırı, aşırı (excessive) müdahale** ile mi gerçekleştiği,
    - Koruyucu ekipman kullanımının (örneğin bileklik, dirseklik) yeterli olup olmadığı,
    dikkate alınmalıdır.

---

### 📚 Eksikler ve İleri Okuma

#### 1. Üst ekstremite travma‑biyomekaniği için temel / klasik kaynaklar

- **Nahum AM, Melvin JW (eds.). Accidental Injury: Biomechanics and Prevention.**  
  Springer.  
  - Üst ekstremite ile ilgili bölümler, kemik kırığı biyomekaniği, hava yastığı ve emniyet kemeri sistemleriyle ilişkili yaralanmaları geniş bir çerçevede ele alır.
- **Yoganandan N, Pintar FA, et al. (eds.). Frontiers in Head and Neck Trauma.**  
  - Daha çok baş‑boyun odaklı olsa da, omuz kuşağı ve klavikula üzerinden iletilen yükler, servikal omurga ile birlikte değerlendirilir; üst ekstremitenin “askı” fonksiyonu açısından önemlidir.
- **American Association for Automotive Medicine (AAAM). Abbreviated Injury Scale (AIS).**  
  - Üst ekstremite yaralanmalarının şiddet sınıflandırması (AIS kodları) için standard referans.

#### 2. Konferans serileri ve teknik kaynaklar

- **SAE (Society of Automotive Engineers) Technical Papers**  
  - Özellikle hava yastığı‑üst ekstremite etkileşimi, Research Arm Injury Device (RAID) kullanımı ve direksiyon/dash panel temaslarına bağlı kol yaralanmaları üzerine çok sayıda teknik bildiri mevcut.  
  - Spesifik makale atıfları yapılmadan kullanılan veriler mutlaka **doğrulanmalı**.
- **Stapp Car Crash Conference Proceedings**  
  - İnsan üst ekstremite segmentlerinde dinamik kırılma limitleri, kadavra testleri ve manken (dummy) kalibrasyonu açısından zengin bir kaynak.  
  - Üst ekstremiteye özgü yeni kriterler (örn. belirli eksenel kuvvet veya bükülme momenti eşikleri) için referans niteliğinde; ancak her bir çalışma kendi sınırları içinde **eleştirel** okunmalı.
- **IRCOBI (International Research Council on the Biomechanics of Injury) Proceedings**  
  - Avrupa merkezli kaza verileri, üst ekstremite yaralanma modelleri, yaya ve bisikletçi kazalarında üst ekstremite yaralanmalarını inceleyen güncel çalışmalar içerir.

#### 3. Regülasyonlar ve test protokolleri (üst ekstremiteyle ilişkili)

- **FMVSS (Federal Motor Vehicle Safety Standards)**  
  - FMVSS 208 (Occupant crash protection) ve ilgili alt standartlar, hava yastığı ve emniyet kemeri sistemleri için temel çerçeveyi belirler. Üst ekstremite için spesifik kriterler sınırlı olsa da, genel işgalci koruma stratejileri üzerinden dolaylı etki söz konusudur.
- **ECE / UNECE Regülasyonları**  
  - Özellikle:
    - **UNECE R94 (frontal çarpışma)**,
    - **UNECE R95 (yan çarpışma)**  
    testlerinde kullanılan mankenler ve ölçüm cihazlarıyla üst ekstremiteye dair veri toplanmakta; ancak yaralanma kriterleri çoğunlukla baş, boyun ve toraksa odaklıdır.
- **Euro‑NCAP Test ve Değerlendirme Protokolleri**  
  - Hem ön hem yan çarpışma testlerinde:
    - Hava yastığı açılımı,
    - Emniyet kemeri geometrisi,
    - Direksiyon kolon hareketi
    üzerinden üst ekstremite yaralanma riski dolaylı olarak değerlendirilmektedir.  
  - Yaya ve bisikletçi koruma testlerinde ise, üst ekstremite daha çok **sekonder** (ikincil) yaralanma olarak karşımıza çıkar; özellikle FOOSH mekanizması ile distal radius ve el kırıkları önemli olabilir.

#### 4. Klinik ve ortopedik kaynaklar

- Üst ekstremite travmalarının tedavi ve rehabilitasyonu için:
  - Standart ortopedi ve travmatoloji kitapları (örneğin **Rockwood and Green’s Fractures in Adults**, **Shoulder and Elbow Surgery** metinleri),
  - Spor travmaları için **Brukner & Khan’s Clinical Sports Medicine** vb.,
  üst ekstremite yaralanmalarının klinik seyri, cerrahi ve konservatif tedavileri açısından referans alınabilir.
- Travma‑biyomekaniği ile klinik ortopediyi birleştiren spesifik makaleler ise çoğu zaman jurnal düzeyinde dağınık olduğundan, iddia edilen her eşik değer ve kriterin kaynağı **mutlaka ayrı ayrı doğrulanmalıdır**.

---

Bu bölüm, klasik literatüre dayalı sağlam bir üst ekstremite yaralanma çerçevesi sunmakla birlikte, modern araç güvenlik sistemleri, yeni nesil sonlu eleman modelleri ve güncel mediko‑legal uygulamalar ışığında, özellikle:

- Cinsiyet ve yaşa bağlı kırılganlık,
- Hava yastığı tasarımı ve “agresiflik” parametreleri,
- Spor ve iş kazalarıyla kesişen karma mekanizmalar,
- Türkiye’de adli değerlendirme ve tazminat süreçleri,

gibi alanlarda güncellenmeye ve derinleştirilmeye açık bir alan olarak görülmelidir.
