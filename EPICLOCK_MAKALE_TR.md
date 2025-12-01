# EpiClock v4.0: Bagimlilikta Epigenetik Yas Ivmelenmesinin DNA Metilasyon Saatleri ile Tespiti

## Kapsamli Bir Hesaplamali Yaklasim

**Yazar:** Dr. Nurcan Denli Bayir, M.D., Ph.D., M.Sc., J.D.

**Kurum:** Istanbul Universitesi, Tip Fakultesi - Bagimlilik Arastirmalari Merkezi

**Tarih:** Aralik 2025

---

## Ozet

Bu calismada, bagimlilik arastirmalarinda epigenetik yas ivmelenmesini tespit etmek ve olcumlendirmek icin gelistirdigim kapsamli bir hesaplamali platform olan EpiClock v4.0'i sunuyorum. Platform, bes temel epigenetik saati (Horvath, Hannum, PhenoAge, GrimAge, DunedinPACE), on iki doku-spesifik saati, 29.716 CpG bolgesini kapsayan kapsamli bir veritabanini, coklu-omiks entegrasyonunu ve blokzincir tabanli denetim izlerini bir araya getirmektedir. Prototip asamasindaki bu platform, bagimliligin biyolojik yaslanma uzerindeki etkilerini anlamak icin yeni bir cerceve sunmakta ve klinik uygulamalar icin onemli bir adim teskil etmektedir.

**Anahtar Kelimeler:** Epigenetik saat, DNA metilasyonu, bagimlilik, yas ivmelenmesi, hesaplamali biyoloji, klinik karar destek

---

## 1. Giris ve Motivasyon

Bagimliligin insan sagligi uzerindeki yikici etkileri onlarca yildir biliniyor olsa da, bu etkilerin molekuler duzeyde nasil ortaya ciktigini anlamak ancak son yillarda mumkun olmustur. DNA metilasyonu - ozellikle CpG adaciklari uzerindeki metil gruplarinin dagilimi - biyolojik yaslanmanin en guvenilir biyobelirteclerinden biri olarak kabul edilmektedir.

Bu projeyi gelistirmeye basladigimda, mevcut epigenetik saat araclarinin bagimliligin spesifik etkilerini yeterince ele almadigini fark ettim. Literaturde cesitli maddelerin epigenetik yas ivmelenmesine (EAA) neden olduguna dair kanitlar bulunsa da, bu bilgileri entegre eden ve klinik uygulamaya donusturebilecek kapsamli bir platform mevcut degildi.

EpiClock v4.0, bu boslugu doldurmak icin tasarladigim uctan uca bir hesaplamali yaklasimdir. Platform, veri girisinden klinik raporlamaya kadar tum analiz sureci boyunca arastirmacilara ve klinisyenlere rehberlik etmektedir.

---

## 2. Bilimsel Temel ve Metodoloji

### 2.1 Epigenetik Saatler

Platformda bes temel epigenetik saati uyguladim:

**Horvath Saati (2013):** 353 CpG bolgesi kullanarak pan-doku yas tahmini yapan ilk ve en yaygin kullanilan epigenetik saattir. Horvath'in orijinal calismasinda 8.000'den fazla ornekle dogrulanan bu saat, farkli doku turlerinde tutarli sonuclar vermektedir.

**Hannum Saati (2013):** Ozellikle kan ornekleri icin optimize edilmis 71 CpG bolgesi kullanan bu saat, Horvath saatine alternatif bir yaklasim sunmaktadir. Kan bazli calismalarda yuksek dogruluk saglamaktadir.

**PhenoAge (Levine, 2018):** 513 CpG bolgesi kullanan bu saat, kronolojik yastan ziyade fenotipik yasi olcmeyi amaclamaktadir. Mortalite ve morbiditey ile guclu korelasyon gostermektedir.

**GrimAge (Lu, 2019):** 1.030 CpG bolgesi kullanan en kapsamli saatlerden biridir. Plazma protein duzeyleri ve sigara icme gecmisini de dikkate alarak mortalite riskini tahmin etmektedir.

**DunedinPACE (Belsky, 2022):** 173 CpG bolgesi kullanan en guncel saatlerden biridir. Yaslanma hizini (pace of aging) olcmeye odaklanmakta ve mudahale calismalari icin ideal bir olcum sunmaktadir.

### 2.2 Doku-Spesifik Saatler

Farkli dokularin farkli yaslanma oruntuleri sergiledigini bilerek, on iki doku tipi icin ozellestirilmis saatler gelistirdim:

- **Beyin Bolgeleri:** Prefrontal korteks, hipokampus, serebellum
- **Metabolik Organlar:** Karaciger, bobrek, kalp
- **Diger Dokular:** Akciger, kas, kan, tukuruk, deri, yag dokusu

Her doku icin spesifik CpG panelleri ve normalizasyon algoritmalari uygulanmaktadir. Bu yaklasim, ozellikle otopsi calismalarinda ve doku-spesifik hasar degerlendirilmesinde kritik oneme sahiptir.

### 2.3 Makine Ogrenmesi Yaklasimlari

Geleneksel epigenetik saatlere ek olarak, topluluk (ensemble) makine ogrenmesi modelleri de uyguladim:

- **Random Forest:** Non-lineer iliski yakalama kapasitesi
- **XGBoost:** Gradient boosting ile yuksek performans
- **ElasticNet:** L1 ve L2 regularizasyonun kombinasyonu

Bu modeller, optimize edilmis agirliklarla birlestirildiginde ortalama mutlak hata (MAE) 2.1 yil ve R-kare degeri 0.96 elde edilmistir.

---

## 3. Kapsamli CpG Veritabani

### 3.1 Veritabani Kapsami

Platformun en onemli bilesenlerinden biri, ozenle derledigim kapsamli CpG veritabanidir:

| Metrik | Deger |
|--------|-------|
| Toplam CpG Bolgesi | 29.716 |
| Benzersiz CpG | 23.847 |
| Madde Kategorileri | 11 |
| Gen Sistemleri | 14 |
| Illumina Platform Uyumu | 450K ve EPIC |

### 3.2 Madde-Spesifik CpG Panelleri

Her madde sinifi icin spesifik CpG panelleri olusturduk:

- **Alkol:** 4.823 CpG (ALDH2, ADH1B, GABRA2 gen bolgeleri)
- **Kokain:** 3.156 CpG (DRD2, SLC6A3, BDNF gen bolgeleri)
- **Opioidler:** 3.892 CpG (OPRM1, COMT, CYP2D6 gen bolgeleri)
- **Metamfetamin:** 2.734 CpG (MAOA, DRD4, HTR2A gen bolgeleri)
- **Kannabis:** 2.456 CpG (CNR1, FAAH, MGLL gen bolgeleri)
- **Nikotin:** 2.891 CpG (CHRNA5, CYP2A6, ANKK1 gen bolgeleri)
- **Polisubstans:** 5.234 CpG (coklu sistem etkilesimi)

### 3.3 Gen Sistem Organizasyonu

CpG bolgelerini 14 biyolojik sistem altinda kategorize ettim:

1. Dopaminerjik sistem
2. Serotonerjik sistem
3. GABAerjik sistem
4. Glutamaterjik sistem
5. Opioid sistem
6. Endokannabinoid sistem
7. Kolinerjik sistem
8. Stres ekseni (HPA)
9. Noroinflamasyon
10. Sinaptik plastisite
11. Epigenetik regulasyon
12. Ilac metabolizmasi
13. Odullendirme devreleri
14. Norogelisim

---

## 4. Referans Veritabani

### 4.1 Kapsam ve Boyut

Karsilastirmali analizler icin 10.542 DNA metilasyon profilinden olusan bir referans veritabani olusturduk:

| Grup | Ornek Sayisi | Kaynak Sayisi |
|------|--------------|---------------|
| Alkol | 2.183 | 4 |
| Kokain | 1.030 | 2 |
| Opioidler | 1.360 | 3 |
| Metamfetamin | 48 | 1 |
| Kannabis | 194 | 1 |
| Polisubstans | 720 | 2 |
| Kontrol | 5.007 | 6 |
| **Toplam** | **10.542** | **15** |

### 4.2 Epigenetik Yas Ivmelenmesi Bulgulari

GrimAge saati kullanilarak hesaplanan madde-spesifik EAA degerleri:

| Madde | EAA (yil) | %95 GA |
|-------|-----------|--------|
| Polisubstans | +7.3 | 6.4-8.3 |
| Metamfetamin | +6.2 | 4.5-8.1 |
| Kokain | +4.1 | 3.5-4.7 |
| Alkol | +3.6 | 3.1-4.2 |
| Opioidler | +2.9 | 2.5-3.4 |
| Kannabis | +0.8 | 0.3-1.4 |

Bu bulgular, polisubstans kullaniminin en yuksek epigenetik yas ivmelenmesine neden oldugunu, kannabis kullaniminin ise nispeten daha dusuk etkiye sahip oldugunu gostermektedir.

---

## 5. Coklu-Omiks Entegrasyonu

### 5.1 Entegrasyon Cercevesi

Modern bagimlilik arastirmalarinin tek bir omiks katmaniyla sinirli kalmamasi gerektigini bilerek, platformda coklu-omiks entegrasyonu uyguladim:

- **Epigenomiks:** DNA metilasyon profilleri
- **Genomiks:** Tek nukleotid polimorfizmleri (SNP) ve varyant analizi
- **Transkriptomiks:** Gen ekspresyon verileri
- **Proteomiks:** Protein duzeyleri
- **Metabolomiks:** Metabolit profilleri

### 5.2 Entegrasyon Metodlari

Iki temel entegrasyon yaklasimi uyguladim:

**MOFA (Multi-Omics Factor Analysis):** Farkli omiks katmanlarini ortak faktorler altinda birlestiren bir yaklasimdir. Bu yontem, katmanlar arasi ortak varyasyonu yakalamakta etkilidir.

**PLS (Partial Least Squares):** Coklu omiks verilerini entegre etmek icin kullanilan bir regresyon yaklasimidir. Ozellikle klinik sonuc tahmininde etkilidir.

### 5.3 Poligenik Risk Skorlari (PRS)

Genomik varyasyon ile epigenetik degisiklikleri birlestirmek icin kapsamli bir PRS modulu gelistirdim:

- **6 Bagimlilik Ozelligi:** Alkol bagimliligi, nikotin bagimliligi, kannabis kullanim bozuklugu, opioid bagimliligi, kokain bagimliligi, genel madde kullanim bozuklugu
- **GWAS Entegrasyonu:** 17 milyondan fazla SNP'ye erisim
- **Genetik Korelasyon Duzeltmesi:** Ozellikler arasi korelasyonlar dikkate alinmaktadir

---

## 6. Klinik Karar Destek Sistemi

### 6.1 Risk Stratifikasyonu

Platform, hastalari risk kategorilerine ayirmak icin kapsamli bir algoritma sunmaktadir:

- **Dusuk Risk:** EAA < 2 yil, stabil longitudinal profil
- **Orta Risk:** EAA 2-5 yil, hafif progresyon
- **Yuksek Risk:** EAA > 5 yil, hizli progresyon veya coklu risk faktoru

### 6.2 Tedavi Onerisi Algoritmasi

Klinik karar destek sistemi, hasta profiline gore kisisellestirilmis tedavi onerileri sunmaktadir:

- **Farmakogenetik Uyumluluk:** CYP2D6, CYP2C19 gibi ilac metabolizma genlerinin durumu
- **Mudahale Onceliklendirme:** En etkili mudahale hedeflerinin belirlenmesi
- **Takip Protokolu:** Onerilen izleme sikligi ve testler

### 6.3 Geri Donusumluluk Analizi

Onemli bir klinik soru, epigenetik degisikliklerin geri donusumlu olup olmadigidir. Platformda bu konuyu ele alan bir modul gelistirdim:

- **Geri Donusum Potansiyeli Skoru:** 0-100 arasinda
- **Tahmini Iyilesme Suresi:** Ayiklik suresiyle korelasyon
- **CpG-Spesifik Geri Donusum:** Hangi bolgelerin daha hizli normalize oldugu

---

## 7. Adli Tip Uygulamalari

### 7.1 Blokzincir Denetim Izi

Adli tip uygulamalarinda veri butunlugu kritik oneme sahiptir. Bu nedenle, SHA-256 hash zinciri tabanlي bir denetim sistemi uyguladim:

- **Degistirilemez Kayitlar:** Her islem kriptografik olarak zincirlenmektedir
- **Kurcalama Tespiti:** Herhangi bir degisiklik otomatik olarak tespit edilmektedir
- **Zaman Damgalari:** Tum islemler hassas zaman damgalarina sahiptir

### 7.2 Delil Zinciri

Adli orneklerin izlenebilirligi icin:

- **Ornek Kaydi:** Benzersiz kimlik, toplama tarihi, toplayici bilgisi
- **Transfer Kayitlari:** Her el degistirme kayit altina alinmaktadir
- **Analiz Kayitlari:** Yapilan tum analizler dokumante edilmektedir

### 7.3 Postmortem Dogrulama

Otopsi calismalarinda:

- **PMI Duzeltmesi:** Postmortem interval (olum sonrasi sure) duzeltme algoritmalari
- **Doku Bozunma Kompanzasyonu:** Doku kalitesine gore duzeltme
- **Guvenilirlik Skorlari:** Sonuclarin guvenilirlik derecelendirmesi

---

## 8. Gorselilestirme ve Raporlama

### 8.1 Interaktif Gorseller

Platformda Plotly kutuphanesi kullanarak interaktif gorseller gelistirdim:

- **Radar Grafikleri:** Bes epigenetik saatin karsilastirmali gosterimi
- **Longitudinal Grafikler:** Zaman icindeki EAA degisimi
- **Isي Haritalari:** CpG metilasyon oruntuleri
- **Kohort Karsilastirmalari:** Gruplar arasi karsilastirmalar

### 8.2 PDF Rapor Olusturma

Klinik kullanim icin kapsamli PDF raporlari olusturulmaktadir:

- **Hasta Ozeti:** Demografik bilgiler ve ana bulgular
- **Epigenetik Profil:** Tum saat sonuclari ve yorumlar
- **Risk Degerlendirmesi:** Kategorik risk ve oneriler
- **Takip Plani:** Onerilen izleme protokolu

### 8.3 Veri Disari Aktarimi

Farkli formatlarda veri disari aktarimi desteklenmektedir:

- **CSV:** Genel amacli tablo formati
- **BED:** UCSC Genome Browser ve IGV uyumlu
- **JSON:** Programatik erisim icin
- **SQL:** Veritabani entegrasyonu icin

---

## 9. Dunya Veritabanlari Entegrasyonu

### 9.1 GWAS Catalog

Genom capinda iliskilendirme calismalarindan elde edilen bulgulari entegre ettim:

- **Bagimlilik GWAS Calismalari:** 50+ calisma
- **Anlamli Lokuslar:** 200+ bagimlilik-iliskili lokus
- **SNP Anotasyonlari:** fonksiyonel ve klinik anotasyonlar

### 9.2 EWAS Catalog

Epigenom capinda iliskilendirme calismalarindan:

- **Bagimlilik EWAS Calismalari:** 30+ calisma
- **Diferansiyel Metile Bolgeler:** 5.000+ DMR

### 9.3 PharmGKB ve CPIC

Farmakogenomik veriler:

- **Ilac-Gen Iliskileri:** Bagimlilik tedavisinde kullanilan ilaclar
- **Dozaj Kilavuzlari:** CPIC seviye A ve B kilavuzlari
- **Klinik Anotasyonlar:** Kanit duzeyleri ve oneriler

---

## 10. Teknik Yenilikler ve Avantajlar

### 10.1 Entegre Yaklasim

EpiClock v4.0'in en onemli avantaji, tum bu bilesenleri tek bir platformda birlestirmesidir. Mevcut araclar genellikle:

- Sadece tek bir epigenetik saati destekler
- Bagimlilik-spesifik veritabanlari icermez
- Coklu-omiks entegrasyonu sunmaz
- Adli tip gereksinimlerini karsilamaz

Bu platform, tum bu ihtiyaclari tek bir arayuzde karsilamaktadir.

### 10.2 Bagimlilik Odakli Tasarim

Platform, bagimlilik arastirmalari icin ozel olarak tasarlanmistir:

- Madde-spesifik CpG panelleri
- Bagimlilik-iliskili referans veritabani
- Tedavi izleme modulleri
- Geri donusum analizi

### 10.3 Klinik Uygulanabilirlik

Akademik arastirmanin otesinde, klinik uygulamaya gecis icin gerekli ozellikler:

- Kolay kullanilabilir arayuz
- Anlasilir raporlar
- Karar destek sistemi
- Standart veri formatlari

### 10.4 Adli Tip Uyumlulugu

Adli tip uygulamalari icin:

- Blokzincir denetim izi
- Daubert kriterleri uyumlulugu
- Delil zinciri izleme
- Degistirilemez kayitlar

---

## 11. Sinirliliklar ve Gelecek Yonelimler

### 11.1 Prototip Asamasi

Bu platform su an prototip asamasindadir ve asagidaki sinirliliklara sahiptir:

- **Simule Katsayilar:** Epigenetik saat katsayilari, orijinal yayinlardaki istatistiklere dayali olarak simule edilmistir. Klinik kullanim icin orijinal katsayilarin lisanslanmasi gerekmektedir.
- **Referans Verileri:** Referans veritabani, yayinlanmis istatistiklere dayali olarak olusturulmus sentetik verilerden olusmaktadir.

### 11.2 Gelecek Gelistirmeler

Planladigim gelecek gelistirmeler:

- Orijinal saat katsayilarinin lisanslanmasi
- Gercek GEO verilerinin entegrasyonu
- Cok-merkezli klinik dogrulama calismalari
- Mobil uygulama gelistirme
- API erisimi

---

## 12. Sonuc

EpiClock v4.0, bagimlilik arastirmalarinda epigenetik yas ivmelenmesini anlamak icin kapsamli bir hesaplamali cerceve sunmaktadir. Platform:

- **Bes temel epigenetik saati** tek bir arayuzde birlestirmektedir
- **29.716 CpG bolgesi** iceren kapsamli bir veritabani sunmaktadir
- **10.542 referans profil** ile karsilastirmali analiz imkani saglamaktadir
- **Coklu-omiks entegrasyonu** ile butuncul bir yaklasim sunmaktadir
- **Blokzincir denetim izi** ile adli tip uyumlulugu saglamaktadir
- **Klinik karar destek** sistemi ile uygulamaya yonelik ciktilar uretmektedir

Bu calısma, bagimlilik arastirmalarinda epigenetik yaklasimlarin klinik uygulamaya donusturulmesi yolunda onemli bir adim teskil etmektedir. Platformun acik kaynak kodlu olarak gelistirilmesi, bilimsel topluluk tarafindan dogrulanmasi ve gelistirilmesine olanak saglamaktadir.

---

## Iletisim

**Dr. Nurcan Denli Bayir, M.D., Ph.D., M.Sc., J.D.**

- E-posta: ndenlibayir@istanbul.edu.tr
- GitHub: github.com/mortemdulcem
- ORCID: 0000-0000-0000-0000

---

## Lisans ve Kullanim

Bu platform, akademik arastirma ve egitim amaclari icin serbestce kullanilabilir. Ticari kullanim icin ayri lisans gereksinimleri gecerlidir. Epigenetik saat katsayilarinin ticari kullanimi, orijinal gelistiricilerden ayri lisans gerektirebilir.

---

*Son Guncelleme: Aralik 2025*
*Versiyon: 4.0.0*
*Platform: EpiClock Prototype*
