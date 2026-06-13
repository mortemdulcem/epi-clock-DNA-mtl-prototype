## 📝 Çevirmen Eki — Travma-Biyomekaniğinde Yöntemler (Methods in Trauma-Biomechanics)

### 🔬 İleri ve Niş Bilgiler

Bu bölüm, klasik yaklaşımları (epidemiyoloji, alan çalışmaları, yaralanma kriterleri, deneysel çalışmalar, sayısal modelleme) sistematik biçimde özetliyor. Güncel travma-biyomekaniği pratiğinde ise, aynı başlıklar çok daha sofistike veri kaynakları ve araçlarla yürütülüyor:

#### 1. Modern veri tabanları, “linked data” ve veri entegrasyonu

Klasik polis/ sigorta kayıtları yanında, bugün özellikle trafik ve travma alanında:

- **NHTSA veri sistemleri**:
  - Eski **NASS** (National Automotive Sampling System) yapısı güncellenerek **Crash Investigation Sampling System (CISS)** ve **Crash Report Sampling System (CRSS)** biçiminde yeniden kurgulandı.  
  - **FARS (Fatality Analysis Reporting System)** hâlâ ölümcül kazaların temel referans kaynağı.
  - **NASS-CDS ve CIREN** (Crash Injury Research and Engineering Network) gibi “in-depth” veri setleri, yaralanma-biyomekanik çalışmalarında, özellikle de **envelope of injury** ve yaralanma tolerans eğrilerinin çıkarılmasında ana referanslar olarak kullanılıyor.

- **Epidemiyolojik verinin klinik kayıtlarla birleştirilmesi**:
  - Travma merkezlerinden elde edilen **elektronik sağlık kayıtları** (EHR/EMR), yoğun bakım veri tabanları ve ölüm kayıtları ile kaza verisinin eşleştirilmesi (record linkage) giderek daha sık uygulanıyor.  
  - Böylece, “kazanın şiddeti – sahadaki bulgular – görüntüleme – cerrahi bulgular – ölüm nedeni” zincirinin daha eksiksiz rekonstrüksiyonu mümkün oluyor.  
  - Bu birleşik veri setleri, **yaralanma kriterleri ve risk fonksiyonlarının** (logistik regresyon, overdispersed Poisson, bayesçi modeller) kalibrasyonunda kritik rol oynuyor.

- **Yaya, bisikletli, mikromobilite** (e-scooter) kazaları için:
  - Yaya/bisiklet veri tabanları, klasik araç-araç çarpışma odaklı veri tabanlarından farklı kodlama şemalarına (örn. spesifik anatomik yaralanma kodları, kask kullanımı, yol altyapısı) ihtiyaç duyuyor.
  - Bu, özellikle **yaya koruması**, **ön kaput sertliği**, **yaya-airbag** sistemleri için biyomekanik model ve test senaryolarının geliştirilmesinde önemli.

#### 2. İleri yaralanma kriterleri ve ölçüm kavramları

Bölümde genel “injury criteria/ injury risk” kavramına atıf var; güncel pratikte ise özellikle baş, boyun ve gövde için daha gelişmiş kriterler kullanılıyor:

- **Baş ve boyun için yeni kriterler**:
  - Klasik **HIC** (Head Injury Criterion) hâlâ kullanımda olsa da, konkusyon ve diffüz aksonal yaralanma gibi **rotasyonel** bileşen ağırlıklı travmalar için yeterli değil.
  - Bu boşluğu doldurmak için:
    - **BrIC / Brain Injury Criterion** (NHTSA tarafından geliştirilen, başın açısal hız bileşenlerine dayanan kriter),
    - **GAMBIT** (Genetically and Algorithmically Modified Brain Injury Threshold),
    - Farklı gruplarca önerilen **Nij türevleri** ve **kritik açısal hız/ivme parametreleri** kullanılıyor.
  - BrIC ve benzeri kriterler özellikle:
    - Yeni nesil otomotiv mankenlerinin (THOR, WorldSID),
    - **American football**, hokey gibi temas sporlarında kask içi sensörler,
    - **Kask standardı** geliştirme çalışmalarında yaygın.

- **Boyun ve gövde kriterleri**:
  - Klasik **Nij** (Neck Injury Criterion), aksiyel yük ve fleksiyon/ekstansiyon momentlerini birleştiren normalize parametre olarak, öncelikle frontal çarpışmalar için kullanılıyor.
  - Yan çarpışmalar ve whiplash için:
    - **NIC**, **Nkm**, **NRC** gibi alternatif boyun kriterleri
    - Omurga yüklerini değerlendirmek için **spinal axial force – bending moment** temelli limit eğrileri ve tolerans diyagramları söz konusu.
  - Gövde için ise:
    - **VC (Viscous Criterion)**,
    - Göğüs deformasyonuna (deflection) bağlı yeni kriterler ve göğüs enerji emilimi temelli metrikler (özellikle Euro-NCAP ve FMVSS bağlamında) öne çıkıyor.

Bu yeni kriterlerin büyük kısmı, **TRID, Stapp, IRCOBI, SAE teknik raporları** ve regülasyon dokümanları içinde geliştirildi; klinik anlamları ve sınır değerleri çoğu zaman “doğrulanmalı” konumda olduğundan, adli değerlendirmede kullanılırken temkinli olunmalı.

#### 3. İleri deneysel modeller: insan yerine geçen sistemler

Bölümün klasik çerçevesi, laboratuvar testleri ve numerik simülasyonu genel seviyede tanımlıyor. Güncel pratikte:

- **Yeni nesil mankenler (ATD, Anthropomorphic Test Devices)**:
  - Klasik Hybrid serisinin ötesinde,  
    - **THOR** (Test device for Human Occupant Restraint),  
    - Yan çarpışma için **WorldSID**,  
    - Çocuk manken ailesi (Q serisi) yaygınlaşmış durumda.
  - Bu mankenler:
    - Daha fazla sensör (ivmeölçer, kuvvet hücreleri, moment sensörleri),
    - Çok eksenli eklem yapıları,
    - Gelişmiş göğüs kafesi ve abdominal yapılar ile,
    - **yaralanma kriterlerinin** daha hassas ölçümünü mümkün kılıyor.

- **Sonlu elemanlar (FE) insan modelleri**:
  - **GHBMC (Global Human Body Models Consortium)** ve  
    - Erkek/kadın, farklı antropometrik seviyeler için detaylı anatomi içeren,
    - Omurga, göğüs kafesi, beyin, iç organlar için yüksek çözünürlüklü modeller sunuyor.
  - **THUMS (Total Human Model for Safety)**, Toyota tarafında geliştirilen ve yaya, sürücü, arkada oturan yolcu gibi farklı duruş senaryoları için optimize edilmiş bir başka önde gelen model.
  - Bu modeller:
    - Klasik ATD’lerin mekanik sınırlılıklarını,
    - Gerçek dokuların **nonlineer, viskoelastik** davranışlarını,
    - Cinsiyet, yaş, beden kitle farklarını dikkate alan **“virtual population”** yaklaşımlarına zemin sağlıyor.
  - Adli rekonstrüksiyon ve ürün sorumluluğu davalarında bu modellerin kullanımı artmakla birlikte,  
    - Mahkemeler önünde kabul edilebilirlik (Daubert standardı, vs.) açısından dikkatli metodolojik raporlama gerekiyor.

- **Hayvan modellerinin güncel konumu**:
  - Etik kısıtlar nedeniyle büyük memeli deneyleri çok azalmış durumda;  
  - Ancak, özellikle **akut fizyolojik yanıtların** (hipotansiyon, beyin ödemi, inflamatuvar yanıt) incelenmesi için, küçük hayvan modelleri ve büyük memeli modellere (domuz, koyun, maymun) ilişkin eski literatür hâlen tolerans limitlerinin alt sınırlarını belirlemede referans kabul ediliyor.
  - Bu veriler, güncel FE ve ATD kalibrasyonunda dolaylı olarak kullanılmaya devam ediyor.

#### 4. Sayısal simülasyon: çok disiplinli ve çok ölçekli yaklaşımlar

Bölümde “numerical simulation” genel bir başlık olarak geçiyor; oysa güncel pratikte:

- **Sonlu elemanlar (FE)**, **multibody (MB)** ve **CFD / FSI** (fluid–structure interaction) kombinasyonları kullanılıyor:
  - Araç kazalarında:
    - Araç deformasyonu için explícit FE,
    - İnsan hareketi için multibody + lokal FE (baş-beyin, boyun),
    - Emniyet kemeri/kilit sistemleri için kablo/beam modelleri.
  - Tıbbi/cerrahi bağlamda:
    - **Damar, kalp, akciğer** gibi yumuşak dokular için FSI,
    - **Konuşlandırılabilir tıbbi cihazlar** (stent, filtre, vb.) için yapısal analizler.
- **Çok ölçekli (multi-scale) modelleme**:
  - Makro düzeyde araç–insan–altyapı etkileşimi,
  - Mezodüzeyde belirli anatomi bölgeleri (örn. servikal omurga segmenti, femur, pelvis),
  - Mikrodüzeyde doku ve hücre ölçeği (örn. beyinde akson demetleri, trabeküler kemik yapısı)  
  birlikte ele alınarak yaralanma mekanizmaları açıklanmaya çalışılıyor.

Bu teknik ilerlemeler, adli rekonstrüksiyonların ve tasarım odaklı mühendislik çalışmalarının, **tek bir yöntem (örn. sadece kinematik rekonstrüksiyon)** üzerinden yürütülmesinin artık yeterli olmadığını; interdisipliner, çok veri kaynaklı yaklaşımın zorunlu olduğunu gösteriyor.

---

### ⚖️ Türkiye / Mediko-legal & Mühendislik Bağlamı

Türkiye’de travma-biyomekaniği ile ilişkili adli, idari ve mühendislik süreçleri, bölümde anlatılan genel çerçeveye benzemekle birlikte bazı özgün özellikler taşıyor:

#### 1. Trafik kazaları, Karayolları Trafik Kanunu ve veriler

- **Karayolları Trafik Kanunu ve ilgili yönetmelikler**, araç güvenliği ve yol kullanıcılarının korunmasına ilişkin temel hukuki çerçeveyi oluşturuyor.
- **Veri kaynakları**:
  - Emniyet Genel Müdürlüğü ve Jandarma Genel Komutanlığı’nın kaza kayıtları (TÜİK ile birlikte yayımlanan istatistikler),
  - **Sigorta şirketleri** ve **Sigorta Bilgi ve Gözetim Merkezi (SBM)** kayıtları,
  - **SGK** kayıtları (özellikle ölüm/ maluliyet, iş kazası niteliğindeki trafik kazaları),
  - Üniversite ve eğitim/araştırma hastanelerinin travma kayıtları.
- Bu veri tabanlarının:
  - Kapsamı, kodlama şemaları ve erişilebilirliği genellikle bilimsel araştırmalar için kısıtlı;  
  - Bu nedenle, **epidemiyolojik kanıt üretimi ve yaralanma risk analizi** çoğu zaman küçük, merkez bazlı, prospektif ya da retrospektif klinik serilere dayanmak zorunda kalıyor.

#### 2. Adli Tıp Kurumu, bilirkişilik ve travma-biyomekaniği

- **Adli Tıp Kurumu (ATK)**:
  - Travma olgularında:
    - Ölüm nedeninin belirlenmesi,
    - Yaşamsal tehlike değerlendirmesi,
    - Kemik kırığı, organ yaralanmalarının niteliği,
    - Sürekli ve geçici maluliyet oranları,
    - İş göremezlik ve tazminat bağlantılı değerlendirmelerde referans kurum.
  - Travma-biyomekaniği açısından:
    - Klasik “mekanik uygunluk” analizleri,
    - **Düşme/ çarpma/ sıkışma/ ezilme** mekanizmalarının değerlendirilmesi,
    - Trafik kazalarında **emniyet kemeri kullanımı**, “sürücü–yolcu ayrımı” gibi soruların yanıtlanmasında fiziksel ve biyomekanik argümanlara başvuruluyor.
- **Bilirkişilik**:
  - Trafik, iş kazası, spor yaralanmaları gibi davalarda:
    - Makine mühendisleri, inşaat/ trafik/ otomotiv mühendisleri,
    - Ortopedi, beyin cerrahisi, adli tıp uzmanları,  
    birlikte rapor hazırlayabiliyor.
  - Travma-biyomekaniği perspektifinden:
    - Kaza rekonstrüksiyonu (hız, çarpma şiddeti, temas yüzeyleri),
    - Yaralanmaların mekanik açıklanabilirliği,
    - Güvenlik donanımlarının (kemer, airbag, bariyer, koruyucu ekipman) işlevi,  
    raporun kritik bileşenleri.
  - Metodoloji açısından:
    - Bölümde anlatılan **“statistik – mekanik rekonstrüksiyon – deneysel/ sayısal simülasyon”** şemasının, pratikte çoğu zaman sadece **kinematik hesaplara ve klinik deneyime** indirgenmesi, önemli bir sınırlılık oluşturuyor.

#### 3. İş kazaları ve 6331 sayılı İş Sağlığı ve Güvenliği Kanunu

- **İş kazaları ve meslek hastalıkları**, travma-biyomekaniği açısından:
  - Yüksekten düşme,
  - Sıkışma, ezilme,  
  - Çarpma (kran, forklift, taşıma sistemleri),
  - Vibrasyon ve aşırı yüklenme,  
  gibi mekanizmalarla karşımıza çıkıyor.
- **6331 sayılı İSG Kanunu** ile:
  - Risk değerlendirmesi, iş ekipmanlarının güvenliği, kişisel koruyucu donanımların zorunlu kullanımı gibi konular kapsamlı şekilde düzenlenmiş durumda.
- Biyomekanik açıdan:
  - Makine koruyucu sistemleri (guard, sensör, acil stop),
  - Ergonomik tasarım,
  - Yük kaldırma limitleri ve iskelet sistemi üzerine binen yükler,  
  hem mühendislik hem de adli değerlendirmede önem kazanıyor.

#### 4. Spor yaralanmaları ve organizasyonlar

- Türkiye Futbol Federasyonu (TFF), Basketbol Federasyonu vb. spor otoriteleri:
  - Sahada meydana gelen travmaların tıbbi kayıtlarını tutmakla birlikte, bunların bilimsel araştırma için standartlaştırılmış veri tabanlarına dönüşmesi sınırlı.
- Özellikle:
  - Temas sporları (futbol, basketbol, güreş, taekwondo, MMA),
  - Kış sporları (kayak, snowboard),
  - Motor sporları,  
  için travma-biyomekaniği perspektifli sistematik veri toplama girişimleri henüz emekleme aşamasında.
- Buna karşın:
  - **FİFA Medical Network** ve IOC’nin (Uluslararası Olimpiyat Komitesi) spor yaralanmalarına yönelik rehberleri,
  - Türkiye’deki spor hekimliği ve ortopedi kliniklerinin kendi kayıtları,  
  literatüre katkı sağlayabilecek önemli kaynaklar.

---

### 📚 Eksikler ve İleri Okuma (Kaynaklı)

Bu bölüm, “yöntemler” başlığı altında temel çerçeveyi iyi vermekle birlikte, bazı güncel alanlar doğal olarak sınırlı kalıyor. Derinleşmek isteyen okur için bazı temel ve güvenilir kaynaklar:

#### 1. Klasik başvuru kitapları

- **Nahum AM, Melvin JW (eds.). Accidental Injury: Biomechanics and Prevention.** Springer.  
  - Travma-biyomekaniği metodolojisi, yaralanma toleransları, deneysel ve sayısal yöntemler için en temel referanslardan.
- **Yoganandan N, Pintar FA, et al. (eds.). Frontiers in Head and Neck Trauma: Clinical and Biomechanical.**  
  - Baş ve boyun travması için hem klinik hem biyomekanik bakış açısını birleştiren kapsamlı bir kaynak.
- **Schmitt KU, Niederer P, Cronin D, et al.** (Bu bölümün de yer aldığı seri; Springer).  
  - Travma-biyomekaniği yöntemleri, yaralanma kriterleri ve uygulamalar için güncel toplu bir çerçeve sunuyor.

#### 2. Yaralanma sınıflama ve değerlendirme sistemleri

- **AAAM – Abbreviated Injury Scale (AIS)**:  
  - Travma şiddetinin kodlanmasında dünya çapında standart.  
  - AIS’e dayalı **ISS (Injury Severity Score)**, **NISS**, **TRISS** vb. skorlar hem epidemyolojik hem adli pratikte yaygın.
- Klinik–biyomekanik köprü için, AIS ile anatomik/ biomekanik eşleştirmeye yönelik AAAM yayınları ve eğitim materyalleri faydalı.

#### 3. Konferanslar ve teknik raporlar (dikkat: spesifik makaleler doğrulanmalı)

- **SAE Technical Papers** ve **Stapp Car Crash Journal**:
  - Motorlu araç kazaları, mankenler, FE modeller, yaralanma kriterleri konularında ana teknik literatür.
- **IRCOBI (International Research Council on the Biomechanics of Injury)** bildirileri:
  - Özellikle Avrupa bağlamında yaralanma biyomekaniği ve güvenlik regülasyonlarının gelişiminde belirleyici.
- **AAAM (Association for the Advancement of Automotive Medicine)** konferansları:
  - Klinik travma verisi ile mühendislik yaklaşımlarının buluştuğu platform.

Bu platformlarda yayımlanan spesifik makalelerin (örneğin yeni BrIC eşikleri, spesifik beyin modeli sonuçları, belirli sporsele yaralanma risk fonksiyonları) kullanımı öncesinde, **“doğrulanmalı”** notuyla, metodoloji ve örneklem sınırlılıkları dikkatle değerlendirilmelidir.

#### 4. Regülasyonlar ve test protokolleri

- **FMVSS (Federal Motor Vehicle Safety Standards)** – ABD:
  - Özellikle FMVSS 208 (ön çarpışma), 214 (yan çarpışma), 301 (yakıt sistemi),  
  manken ve yaralanma kriterleri kullanımını tanımlar.
- **UNECE Regülasyonları** – Avrupa:
  - **R94 (frontal çarpışma)**, **R95 (yan çarpışma)**,  
  **R127 (yaya koruması)** vb. regülasyonlar, test konfigürasyonları ve kullanılacak kriterleri standardize eder.
- **Euro-NCAP protokolleri**:
  - Araçların tüketici güvenlik değerlendirmesinde kullanılan:
    - Ön/yan/arka çarpışma,
    - Yaya/ bisikletli koruması,
    - Aktif güvenlik sistemleri (AEB, LKA, vb.),  
    için güncel test prosedürleri ve skorlamalar.  
  - Bu protokoller, travma-biyomekaniği yöntemlerinin “uygulamaya geçmiş” halini görmek açısından çok öğreticidir.

---

Bu ek, bölümde sunulan genel çerçeveyi güncel araçlar, kriterler ve Türkiye’ye özgü mediko-legal bağlamla tamamlamayı amaçlıyor. Travma-biyomekaniği alanında çalışanlar için, yukarıda sayılan referanslar ve kurumlar, hem ileri düzey araştırma hem de adli/mühendislik uygulamalarında temel dayanak noktalarıdır.
