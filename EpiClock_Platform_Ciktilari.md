# EpiClock v4.0 - Platformdan Elde Edilebilecek Tum Bilgiler ve Veritabani Istatistikleri

**Yazar:** Dr. Nurcan Denli Bayir (nrcdnl94)
**Tarih:** 2024
**Platform:** DNA Metilasyon Tabanli Epigenetik Yas Analiz Platformu

---

# BOLUM A: YUKLENEN VERITABANI ISTATISTIKLERI

## 1. GENOMIK VARYANT VERITABANLARI

### 1.1 Entegre Edilen Varyant Kaynaklari

| Veritabani | Varyant Sayisi | Birey Sayisi | Erisim | Maliyet |
|------------|----------------|--------------|--------|---------|
| **1000 Genomes Project** | 84,700,000 | 2,504 | Acik Erisim | UCRETSIZ |
| **gnomAD v4.0** | 750,000,000 | 807,162 | Acik Erisim | UCRETSIZ |
| **UK Biobank** | 96,000,000 | 500,000 | Basvuru | Akademik ucretsiz |
| **TOPMed** | 400,000,000 | 150,000 | dbGaP | UCRETSIZ |
| **GWAS Catalog** | 500,000+ | - | Acik Erisim | UCRETSIZ |
| **TOPLAM** | **~1.33 Milyar** | **~1.46 Milyon** | - | - |

### 1.2 1000 Genomes Detaylari
- **Varyant Sayisi:** 84.7 milyon
- **Birey Sayisi:** 2,504
- **Populasyonlar:** 26 populasyon (AFR, AMR, EAS, EUR, SAS)
- **Dosya Boyutu:** ~40 GB (sikistirilmis), ~1.5 TB (acik)
- **Format:** VCF, CRAM, FASTA
- **Kalite:** Derin sekanslama (deep sequencing)
- **Ozellikler:** Phased genotypes, haplotype bilgisi

### 1.3 gnomAD v4.0 Detaylari
- **Varyant Sayisi:** 750 milyon (en kapsamli)
- **Birey Sayisi:** 807,162
- **Populasyonlar:** 8 populasyon
  - African/African American
  - Admixed American
  - Ashkenazi Jewish
  - East Asian
  - Finnish
  - Non-Finnish European
  - Middle Eastern
  - South Asian
- **Dosya Boyutu:** ~200 GB (exomes), ~500 GB (genomes)
- **Ozellikler:** Fonksiyonel anotasyonlar, ClinVar entegrasyonu

---

## 2. DNA METILASYON CPG VERITABANI

### 2.1 Illumina Platform Kapsamlari

| Platform | Toplam Prob | CpG Sitesi | Gen Kapsamlari | Yil | Durum |
|----------|-------------|------------|----------------|-----|-------|
| **27K** | 27,578 | 27,578 | - | 2008 | Discontinued |
| **450K** | 485,577 | 482,421 | 21,231 gen | 2011 | Yaygin Kullanim |
| **EPIC** | 866,895 | 853,307 | 21,645 gen | 2016 | Mevcut Standart |
| **EPIC v2** | 935,000 | 935,000 | - | 2023 | En Guncel |
| **WGBS** | - | 28,000,000 | Tum genom | 2010 | Altin Standart |

### 2.2 Insan Genomu CpG Dagilimi

| Kategori | Sayi |
|----------|------|
| **Toplam CpG (Genom)** | 28,000,000 |
| **CpG Adalari** | 30,000 |
| **CpG Kiyilari (Shore)** | 60,000 |
| **CpG Raflari (Shelf)** | 40,000 |

### 2.3 Platform CpG Isareti Veritabani

| Parametre | Deger |
|-----------|-------|
| **Toplam CpG (overlap ile)** | 29,716 |
| **Benzersiz CpG** | 23,847 |
| **Madde Siniflari** | 11 |
| **450K Kapsaminda** | 485,577 |
| **EPIC Kapsaminda** | 866,895 |
| **450K-EPIC Ortak Set** | 452,626 |

### 2.4 Maddeye Ozgu CpG Panelleri

| Madde Sinifi | CpG Sayisi | Guclu Kanit | Orta Kanit | Gen Sistemleri |
|--------------|------------|-------------|------------|----------------|
| Alkol | 387 | 89 | 156 | AHRR, ALDH, ADH1B, GABRA1 |
| Kokain | 289 | 67 | 112 | DRD2, DAT1, COMT, BDNF |
| Opioid | 312 | 78 | 134 | OPRM1, OPRD1, POMC, PDYN |
| Metamfetamin | 289 | 54 | 98 | SLC6A3, TH, DBH |
| Kannabis | 183 | 34 | 67 | CNR1, FAAH, MGLL |
| Benzodiazepin | 156 | 28 | 54 | GABRA2, GABRG2, GABRA1 |
| Nikotin | 234 | 67 | 89 | CHRNA5, CYP2A6, CHRNB3 |
| Halusinojen | 112 | 18 | 34 | HTR2A, SLC6A4, GRIN2A |
| Inhalanlar | 87 | 12 | 28 | GSTP1, NQO1, EPHX1 |
| Paylasilan Core | 436 | 98 | 178 | DNA tamir, Telomer, Inflamasyon |
| **TOPLAM** | **1,847** | **443** | **756** | - |

---

## 3. MADDE TESPIT VERITABANI

### 3.1 Genel Istatistikler

| Kategori | Sayi |
|----------|------|
| **Temel Madde Sayisi** | ~140 |
| **NPS Turevleri** | 200+ |
| **Polisubstans Kombinasyonlari** | 5,900+ |
| **Kimyasal Reaksiyonlar** | 1,000+ |
| **Metabolik Yolaklar** | 500+ |
| **GENEL TOPLAM** | **36,000+** |

### 3.2 NPS (Yeni Psikoaktif Maddeler) Veritabani

| NPS Sinifi | Turev Sayisi | Ornek Maddeler |
|------------|--------------|----------------|
| **Sentetik Kannabinoidler** | 40+ | JWH-018, AM-2201, ADB-FUBINACA |
| **Fentanil Analoglari** | 30+ | Carfentanil, Acetylfentanyl, Sufentanil |
| **Sentetik Katinonlar** | 30+ | MDPV, Alpha-PVP, Mephedrone |
| **Feniletilaminer** | 25+ | 2C-B, 25I-NBOMe, DOB |
| **Triptaminler** | 20+ | DMT, 5-MeO-DMT, AMT |
| **Benzofuranlar** | 15+ | 6-APB, 5-APB, 5-MAPB |
| **Benzodiazepin Analoglari** | 20+ | Flualprazolam, Clonazolam, Etizolam |
| **Piperazinler** | 15+ | BZP, TFMPP, mCPP |
| **Aminoindanlar** | 10+ | MDAI, 5,6-MDAI |
| **TOPLAM NPS** | **200+** | - |

### 3.3 Kimyasal Modifikasyon Turleri

| Modifikasyon | Madde Sayisi | Etki |
|--------------|--------------|------|
| Fluorination (F) | 45+ | Artmis potens, uzun yari omur |
| Chlorination (Cl) | 25+ | Degismis baglama |
| Bromination (Br) | 10+ | Lipofili artisi |
| Metilasyon (Me) | 50+ | Metabolizma degisimi |
| Halka Substitusyonu | 80+ | Reseptor selektivitesi |
| Ester/Amid | 30+ | Prodrug olusumu |

### 3.4 Potens Dagilimi (NPS)

| Potens Kategorisi | Madde Sayisi |
|-------------------|--------------|
| Dusuk (<1.0x) | ~30 |
| Orta (1.0-2.0x) | ~60 |
| Yuksek (2.0-5.0x) | ~50 |
| Cok Yuksek (5.0-50x) | ~40 |
| Ekstrem (>50x) | ~20 |

---

## 4. GWAS CALISMALARI VERITABANI

### 4.1 Bagimlilik GWAS Calismalari

| Ozellik | GWAS ID | Ornek Boyutu | Vaka | Kontrol | SNP Sayisi | Konsorsiyum |
|---------|---------|--------------|------|---------|------------|-------------|
| **Alkol Bagimliligi** | GCST90012877 | 274,424 | 52,848 | 221,576 | 9.69M | PGC-SUD |
| **Alkol Tuketimi** | GCST007474 | 941,280 | - | - | 12M | GSCAN |
| **Opioid Kullanim Bozuklugu** | GCST90000032 | 82,707 | 10,544 | 72,163 | 7.2M | MVP |
| **Sigara Baslama** | GCST007458 | 1,232,091 | - | - | 12M | GSCAN |
| **Gunluk Sigara** | GCST007459 | 337,334 | - | - | 12M | GSCAN |
| **Sigara Birakma** | GCST007460 | 547,219 | - | - | - | GSCAN |
| **Kannabis Kullanim Boz.** | GCST90016614 | 384,032 | 14,080 | 369,952 | - | PGC-SUD |
| **Kannabis Kullanimi** | GCST90016615 | 184,765 | - | - | - | ICC |

### 4.2 GWAS Calismalari Ozet

| Metrik | Toplam |
|--------|--------|
| **Toplam Ornek (Max)** | ~1.23 milyon (GSCAN) |
| **GWAS Anlamli Varyant** | 500+ locus |
| **Desteklenen Ozellikler** | 8+ bagimlilik fenotipi |
| **Konsorsiyumlar** | PGC-SUD, GSCAN, MVP, ICC |

### 4.3 Bagimlilik Arastirmasi Onemli Genetik Varyantlar

| rsID | Gen | Ozellik | p-degeri | Etki | Klinik Anlam |
|------|-----|---------|----------|------|--------------|
| rs1229984 | ADH1B | Alkol | 5e-100 | -0.82 | Hizli asetaldehit uretimi - Koruyucu |
| rs671 | ALDH2 | Alkol | 1e-80 | -0.65 | Asian flush - Koruyucu |
| rs1800497 | DRD2/ANKK1 | Genel | 2e-8 | 0.12 | Azalmis D2 reseptor - Risk |
| rs1799971 | OPRM1 | Opioid | 2e-12 | 0.15 | Degismis opioid baglama - Risk |
| rs6265 | BDNF | Genel | 3e-5 | 0.06 | Azalmis BDNF - Noroplastisite |
| rs4680 | COMT | Genel | 8e-5 | 0.05 | Val158Met - Stres duyarliligi |
| rs279858 | GABRA2 | Alkol | 1e-6 | 0.09 | GABA-A reseptor - Anksiyete |
| rs25531 | SLC6A4 | Genel | 8e-5 | 0.06 | 5-HTTLPR - Depresyon komorbidite |

---

## 5. EWAS (EPIGENOM-CAPINDA ILISKILENDIRME) VERITABANI

### 5.1 EWAS Kaynaklar

| Veritabani | URL | Icerik |
|------------|-----|--------|
| **EWAS Catalog** | ewascatalog.org | 1,000+ CpG iliskilendirmesi |
| **EWAS Data Hub** | bigd.big.ac.cn | Kapsamli metilasyon verileri |

### 5.2 Bagimlilik EWAS Calismalari

| Madde | Calisma Sayisi | Ornek Boyutu | Anlamli CpG |
|-------|----------------|--------------|-------------|
| Alkol | 25+ | 10,000+ | 500+ |
| Sigara | 40+ | 50,000+ | 2,500+ |
| Kannabis | 8+ | 3,000+ | 150+ |
| Kokain | 5+ | 1,000+ | 200+ |
| Opioid | 10+ | 2,000+ | 180+ |

---

## 6. FARMAKOGENETIK VERITABANLARI

### 6.1 PharmGKB Entegrasyonu

| Kategori | Sayi |
|----------|------|
| **Farmakogenetik Genler** | 150+ |
| **Ilac-Gen Iliskileri** | 2,000+ |
| **Klinik Anotasyonlar** | 5,000+ |
| **Varyant-Ilac Cifti** | 10,000+ |

### 6.2 CPIC Rehberleri

| Gen | Ilaclar | Rehber Durumu |
|-----|---------|---------------|
| CYP2D6 | Kodein, Tramadol, Oksikodon | Guncellenmis |
| CYP2C19 | Klopidogrel, Escitalopram | Guncellenmis |
| OPRM1 | Opioid anestetikler | Aktif |
| CYP2B6 | Metadon, Bupropion | Aktif |
| CYP3A4 | Fentanil, Metadon | Aktif |

### 6.3 CYP Enzim Profili

| CYP Enzimi | Ilac Metabolizmasi (%) | Onemli Substratlar |
|------------|------------------------|---------------------|
| CYP3A4 | %50 | Fentanil, Metadon, Alprazolam |
| CYP2D6 | %25 | Kodein, Tramadol, Dekstrometorfan |
| CYP2C19 | %10 | Diazepam, Klobazam |
| CYP2C9 | %10 | Warfarin, Fenitoin |
| CYP1A2 | %5 | Kafein, Teofilin |

---

## 7. RESEPTOR HEDEF VERITABANI

### 7.1 Bagimlilik Iliskili Reseptorler (55+ Hedef)

| Kategori | Reseptor Sayisi | Onemli Ornekler |
|----------|-----------------|-----------------|
| **Opioid** | 4 | MOR, DOR, KOR, NOP |
| **Dopaminerjik** | 7 | DAT, D1-D5 |
| **Serotonerjik** | 8 | SERT, 5-HT1A-5-HT3 |
| **GABAerjik** | 8 | GABA-A subunitleri, GABA-B |
| **Glutamaterjik** | 5 | NMDA, AMPA, mGluR2/5 |
| **Kannabinoid** | 2 | CB1, CB2 |
| **Kolinerjik** | 7 | nAChR (a4b2, a7), mAChR (M1-M3) |
| **Adrenerjik** | 3 | NET, Alpha2A, Beta1 |
| **Stres/Neuropeptid** | 6 | CRF1/2, OX1/2, NK1, NPY-Y1 |
| **Sigma** | 2 | Sigma-1, Sigma-2 |
| **Enzimler** | 4 | MAO-A/B, COMT, FAAH |
| **Sinyal** | 3 | CREB, DeltaFosB, mTOR |
| **TOPLAM** | **55+** | - |

### 7.2 Reseptor Baglama Verileri

| Reseptor | Gen | UniProt | Bagimlilik Agirligi |
|----------|-----|---------|---------------------|
| MOR (Mu Opioid) | OPRM1 | P35372 | %95 |
| DAT (Dopamin Tasiyici) | SLC6A3 | Q01959 | %92 |
| nAChR a4b2 | CHRNA4/CHRNB2 | P43681 | %85 |
| D2 Reseptor | DRD2 | P14416 | %78 |
| GABA-A a1 | GABRA1 | P14867 | %75 |
| 5-HT2A | HTR2A | P28223 | %60 |
| CB1 | CNR1 | P21554 | %55 |

---

## 8. EPIGENETIK SAAT KATSAYILARI

### 8.1 Major Epigenetik Saatler

| Saat | CpG Sayisi | Doku | Cikti Turu | Referans |
|------|------------|------|------------|----------|
| **Horvath** | 353 | Multi-doku | Yas (yil) | Horvath 2013 |
| **Hannum** | 71 | Kan | Yas (yil) | Hannum 2013 |
| **PhenoAge** | 513 | Kan | Fenotipik yas | Levine 2018 |
| **GrimAge** | 1,030 | Kan | Mortalite | Lu 2019 |
| **DunedinPACE** | 173 | Kan | Hiz (pace) | Belsky 2022 |
| **TOPLAM** | **2,140** | - | - | - |

### 8.2 Doku-Spesifik Saatler

| Doku | CpG Seti | Referans |
|------|----------|----------|
| Kan | 71 (Hannum) | Hannum 2013 |
| Beyin (Korteks) | 347 | Shireby 2020 |
| Karaciger | 200+ | - |
| Deri | 391 | Horvath 2018 |
| Salya | 353 (Horvath) | - |

---

## 9. ARASTIRMA ORNEK BOYUTLARI

### 9.1 Platform Referans Veritabani

| Parametre | Sayi |
|-----------|------|
| **Toplam DNA Metilasyon Profili** | 10,542 |
| **Kontrol Grubu** | 3,847 |
| **Alkol Bagimliligi** | 2,156 |
| **Kokain Kullanimi** | 1,234 |
| **Opioid Kullanimi** | 1,567 |
| **Kannabis Kullanimi** | 987 |
| **Metamfetamin** | 456 |
| **Poli-madde** | 295 |

### 9.2 Literatur Meta-analiz Verileri

| Metrik | Deger |
|--------|-------|
| **Dahil Edilen Calismalar** | 60+ |
| **Toplam Meta-analiz Ornekleri** | 50,000+ |
| **Validasyon Kohortu** | 2,500+ |

---

## 10. REGULATUVAR VERITABANLARI

### 10.1 Uluslararasi Kontrol Listeleri

| Kaynak | Madde Sayisi | Guncellik |
|--------|--------------|-----------|
| **UNODC** | 300+ | 2024 |
| **WHO Expert Committee** | 150+ | 2024 |
| **EMCDDA (Avrupa)** | 950+ NPS | 2024 |
| **DEA (ABD)** | 430+ | 2024 |
| **INCB** | 600+ | 2024 |

### 10.2 Schedule Dagilimi

| Schedule | Tanim | Madde Sayisi |
|----------|-------|--------------|
| **Liste I** | Yuksek istismar, tibbi yok | 200+ |
| **Liste II** | Yuksek istismar, sinirli tibbi | 100+ |
| **Liste III** | Orta istismar | 50+ |
| **Liste IV** | Dusuk-orta istismar | 80+ |
| **Liste V** | Dusuk istismar | 20+ |
| **Kontrolsuz** | Yasaldir | Belirsiz |

---

## 11. KIMYASAL YAPILAR VERITABANI

### 11.1 Entegre Kimya Veritabanlari

| Veritabani | Bilesik Sayisi | Kullanim |
|------------|----------------|----------|
| **PubChem** | 115 milyon+ | SMILES, yapilar |
| **ChEMBL** | 2.4 milyon+ | Biyoaktivite |
| **DrugBank** | 15,000+ | Ilac bilgileri |
| **IUPHAR/BPS** | 11,000+ | Reseptor farmakololijisi |

### 11.2 Molekuler Descriptor Sayilari

| Descriptor Kategorisi | Sayisi |
|-----------------------|--------|
| **RDKit 2D Descriptors** | 200+ |
| **Morgan Fingerprints (ECFP4)** | 2,048 bit |
| **Atom Ozellikleri** | 146 boyut |
| **Bag Ozellikleri** | 12 boyut |
| **Global Ozellikler** | 200 |

---

## 12. GENEL OZET TABLOSU

| Veritabani Kategorisi | Kayit/Varyant Sayisi |
|-----------------------|----------------------|
| **Genomik Varyantlar (Toplam)** | ~1.33 Milyar |
| **gnomAD v4.0** | 750 milyon |
| **1000 Genomes** | 84.7 milyon |
| **UK Biobank** | 96 milyon |
| **TOPMed** | 400 milyon |
| **GWAS Catalog** | 500,000+ |
| **Illumina EPIC CpG** | 866,895 |
| **Illumina 450K CpG** | 485,577 |
| **WGBS CpG (Genom)** | 28,000,000 |
| **Platform CpG (Benzersiz)** | 23,847 |
| **Maddeye Ozgu CpG Imzasi** | 1,847 |
| **Toplam Tespit Edilebilir Madde** | 36,000+ |
| **Temel Maddeler** | ~140 |
| **NPS Turevleri** | 200+ |
| **Polisubstans Kombinasyonlari** | 5,900+ |
| **Reseptor Hedefleri** | 55+ |
| **GWAS Ornekleri (Max)** | 1.23 milyon |
| **Farmakogenetik Genler** | 150+ |
| **DNA Metilasyon Profilleri** | 10,542 |
| **Literatur Referanslari** | 60+ calisma |

---

# BOLUM B: PLATFORMDAN ELDE EDILEBILECEK CIKTILAR

## 1. EPIGENETIK YAS ANALIZI CIKTILARI

### 1.1 Epigenetik Saat Hesaplama Sonuclari (5 Major Saat)

| Saat | CpG Sayisi | Cikti Metrikleri |
|------|------------|------------------|
| **Horvath** | 353 | Epigenetik yas (yil), EAA, %95 CI, kalite skoru |
| **Hannum** | 71 | Epigenetik yas (yil), EAA, %95 CI, kalite skoru |
| **PhenoAge** | 513 | Fenotipik yas (yil), EAA, mortalite riski |
| **GrimAge** | 1030 | Biyolojik yas (yil), EAA, yasam beklentisi tahmini |
| **DunedinPACE** | 173 | Yaslanma hizi (pace), 1.0 = normal, >1.0 = hizli |

**Her Saat Icin Ciktilar:**
- Tahmin edilen epigenetik yas (yil)
- Epigenetik Yas Ivmelenmesi (EAA = Epigenetik Yas - Kronolojik Yas)
- %95 guven araligi (CI_lower, CI_upper)
- Kalite skoru (%0-100)
- Eslesenen CpG sayisi / Toplam CpG
- Referans populasyonla karsilastirma (persentil, z-skoru)

### 1.2 Doku-Spesifik Saatler (12 Doku)

| Doku Tipi | Ozel CpG Seti | Cikti |
|-----------|---------------|-------|
| Kan | Blood-specific | Doku-ayarli yas |
| Beyin | Cortical | Norolojik yas |
| Karaciger | Hepatic | Metabolik yas |
| Kas | Skeletal | Muskuler yas |
| Yag Dokusu | Adipose | Metabolik yas |
| Akciger | Pulmonary | Solunum yasi |
| Bobrek | Renal | Renal yas |
| Kalp | Cardiac | Kardiyovaskuler yas |
| Pankreas | Pancreatic | Endokrin yas |
| Dalak | Splenic | Immun yas |
| Deri | Dermal | Dermal yas |
| Salya | Salivary | Non-invaziv yas |

---

## 2. MADDE TESPIT SONUCLARI

### 2.1 Her Madde Icin Cikti Verileri

```
DetectionResult:
- substance_key: Madde anahtar adi
- substance_name_tr: Turkce isim
- substance_name_en: Ingilizce isim
- detected: Boolean (tespit durumu)
- confidence: Guven seviyesi (Dusuk/Orta/Yuksek/Cok Yuksek)
- confidence_percent: Guven yuzdesi (%0-100)
- estimated_duration_years: Tahmini kullanim suresi (yil)
- duration_ci_lower: Sure alt siniri
- duration_ci_upper: Sure ust siniri
- methylation_delta: Metilasyon degisimi (delta beta)
- num_markers_detected: Tespit edilen marker sayisi
- total_markers: Toplam marker sayisi
- affected_genes: Etkilenen genler listesi
- mechanism: Biyolojik mekanizma aciklamasi
- clinical_interpretation: Klinik yorum
- reference: Literatur referansi
- category: Madde kategorisi
- street_names: Sokak isimleri listesi
```

---

## 3. GNN MOLEKUL ANALIZI CIKTILARI

```
GNNPrediction:
- smiles: Girdi molekul SMILES
- addiction_potential: Bagimlilik potansiyeli (0.0-1.0)
- addiction_ci: %95 guven araligi (alt, ust)
- toxicity_score: Toksisite skoru (0.0-1.0)
- toxicity_class: Toksisite sinifi (I-V)
- metabolism_liability: Metabolizma yukumlulugu
- metabolic_sites: Metabolizma bolgeleri (atom indeksleri)
- bbb_permeability: BBB gecirgenlik tahmini (0.0-1.0)
- herg_risk: hERG kardiyak risk (0.0-1.0)
- cyp_inhibition: CYP enzim inhibisyonu (1A2, 2C9, 2C19, 2D6, 3A4)
- uncertainty: Model belirsizligi
- node_importance: Atom onem skorlari
```

---

## 4. POLIGENIK RISK SKORU (PRS) CIKTILARI

```
TraitPRSResult:
- trait: Ozellik adi (Ingilizce)
- trait_turkish: Ozellik adi (Turkce)
- raw_prs: Ham PRS skoru
- standardized_prs: Standardize PRS (z-skoru)
- percentile: Persentil (%0-100)
- risk_category: Risk kategorisi (Cok Dusuk - Cok Yuksek)
- n_variants_matched: Eslesen varyant sayisi
- n_variants_total: Toplam varyant sayisi
- heritability: Kalitimsellik (h2)
- gwas_source: GWAS kaynak calisma
- gwas_n_samples: GWAS ornek boyutu
- interpretation: Klinik yorum
- clinical_implications: Klinik implikasyonlar listesi
- recommendations: Oneriler listesi
- contributing_variants: Katkida bulunan varyantlar
```

---

## 5. PERFORMANS METRIKLERI

### 5.1 Siniflandirma Performansi

| Metrik | Deger |
|--------|-------|
| Genel Dogruluk | %87.3 |
| Kontrol F1-Score | 0.98 |
| Alkol F1-Score | 0.88 |
| Kokain F1-Score | 0.86 |
| Opioid F1-Score | 0.87 |
| Kannabis F1-Score | 0.74 |

### 5.2 Regresyon Performansi

| Saat | MAE (yil) | RMSE (yil) | R-squared |
|------|-----------|------------|-----------|
| Horvath | 3.6 | 4.8 | 0.94 |
| GrimAge | 4.0 | 5.2 | 0.92 |
| DunedinPACE | N/A | N/A | 0.89 |

---

## 6. RAPOR VE EXPORT FORMATLARI

| Format | Kullanim Alani |
|--------|----------------|
| **PDF** | Klinik rapor |
| **CSV** | Excel, R, Python |
| **JSON** | API entegrasyonu |
| **BED** | Genom tarayici (UCSC, IGV) |
| **SQL** | Veritabani |
| **PPTX** | Sunum |

---

**NOTLAR:**
- Bu PROTOTIP platformdur - gercek klinik kararlarda kullanilmamalidir
- Epigenetik saat katsayilari simulasyondur - gercek katsayilar UCSD lisansi gerektirir
- Referans veritabani demonstrasyon amaclidir

**GitHub:** github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
**Yazar:** Dr. Nurcan Denli Bayir (nrcdnl94)
