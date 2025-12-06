# EpiClock v4.0 - Platformdan Elde Edilebilecek Tum Bilgiler

**Yazar:** Dr. Nurcan Denli Bayir (nrcdnl94)
**Tarih:** 2024
**Platform:** DNA Metilasyon Tabanli Epigenetik Yas Analiz Platformu

---

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
| Kasik | Skeletal | Muskuler yas |
| Yag Dokusu | Adipose | Metabolik yas |
| Akcigar | Pulmonary | Solunum yasi |
| Bobrek | Renal | Renal yas |
| Kalp | Cardiac | Kardiyovaskuler yas |
| Pankreas | Pancreatic | Endokrin yas |
| Dalak | Splenic | Immun yas |
| Deri | Dermal | Dermal yas |
| Salya | Salivary | Non-invaziv yas |

**Capraz-Doku Normalizasyon:**
- Doku-spesifik kalibrasyon katsayilari
- Doku yas uyumsuzluk analizi
- Multi-doku karsilastirma grafigi

---

## 2. MADDE TESPIT VE SINIFLANDIRMA

### 2.1 Tespit Edilebilir Madde Kategorileri

| Kategori | Madde Sayisi | Ornek Maddeler |
|----------|--------------|----------------|
| Alkol | 1 | Etanol |
| Opioidler | 15+ | Morfin, Fentanil, Heroin, Oksikodon, Metadon |
| Stimulanlar | 12+ | Kokain, Metamfetamin, Amfetamin, MDMA |
| Benzodiazepinler | 10+ | Diazepam, Alprazolam, Lorazepam |
| Kannabinoidler | 5+ | THC, CBD, Sentetik kannabinoidler |
| Halusinojenler | 8+ | LSD, Psilosibin, DMT, Ketamin |
| NPS (Yeni Psikoaktif Maddeler) | 200+ | Fentanil analoglari, Sentetik katinon |
| Nikotin | 1 | Nikotin/Sigara |
| Coklu Madde | Kombinasyonlar | Polisubstans kullanimi |

### 2.2 Her Madde Icin Cikti Verileri

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

### 2.3 Maddeye Ozgu CpG Imzalari

**Toplam Tanimlanan CpG:** 1,847 benzersiz CpG sitesi

| Madde | CpG Sayisi | Ornek Genler |
|-------|------------|--------------|
| Alkol | 387 | AHRR, ALDH, ADH1B, GABRA1 |
| Kokain | 289 | DRD2, DAT1, COMT, BDNF |
| Opioid | 312 | OPRM1, OPRD1, POMC, PDYN |
| Metamfetamin | 289 | SLC6A3, TH, DBH |
| Kannabis | 183 | CNR1, FAAH, MGLL |
| Paylasilan Core | 436 | DNA tamir, Telomer, Inflamasyon |

---

## 3. GRAPH NEURAL NETWORK (GNN) MOLEKUL ANALIZI

### 3.1 SMILES Girisinden Elde Edilen Ciktilar

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
- hash_chain: Blockchain dogrulama hash
- timestamp: Analiz zaman damgasi
```

### 3.2 Molekuler Graf Ozellikleri

**Atom Ozellikleri (146 boyut):**
- Atom numarasi (one-hot, 118 element)
- Derece (0-6)
- Formal yuk (-3 ile +3)
- Hibridizasyon (SP, SP2, SP3, SP3D, SP3D2)
- Aromatiklik (True/False)
- Hidrojen sayisi (0-4)
- Halka uyeligi (True/False)

**Bag Ozellikleri (12 boyut):**
- Bag tipi (tek, cift, uc, aromatik)
- Konjugasyon durumu
- Halka icinde olma
- Stereo konfigurasyonu

---

## 4. GELISMIS OZELLIK MUHENDISLIGI

### 4.1 Kimyasal Descriptorler

| Kategori | Ozellikler | Cikti |
|----------|------------|-------|
| **Yapısal** | Molekul agirligi, Atom sayisi, Bag sayisi | Numerik degerler |
| **Lipofili** | cLogP, cLogD | Degerler + yorum |
| **Polarite** | TPSA, HBD, HBA | Numerik + BBB tahmini |
| **Esneklik** | Rotatable bonds, Ring count | Sayisal degerler |
| **Fingerprints** | Morgan/ECFP4 (2048-bit) | Bit vektoru |

### 4.2 Farmakokinetik Profil

```
PharmacokineticsResult:
- bbb_permeability: BBB gecirgenlik (Dusuk/Orta/Yuksek)
- absorption: Absorpsiyon tahmini
- half_life_category: Yari omur (Cok kisa/Kisa/Orta/Uzun)
- bioavailability: Biyoyararlanim (%)
- protein_binding: Plazma protein baglama (%)
- volume_of_distribution: Dagilim hacmi (L/kg)
- clearance: Klerens tahmini
```

### 4.3 CYP Enzim Profili

| CYP Enzimi | Cikti | Klinik Anlami |
|------------|-------|---------------|
| CYP1A2 | Inhibitor/Substrate/Inducer | Ilac etkilesimi |
| CYP2C9 | Inhibitor/Substrate/Inducer | Warfarin metabolizmasi |
| CYP2C19 | Inhibitor/Substrate/Inducer | PPI metabolizmasi |
| CYP2D6 | Inhibitor/Substrate/Inducer | Opioid metabolizmasi |
| CYP3A4 | Inhibitor/Substrate/Inducer | Cogu ilac metabolizmasi |

---

## 5. RESEPTOR HEDEF PROFILI (55+ Hedef)

### 5.1 Reseptor Kategorileri

| Kategori | Reseptorler | Bagimlilik Agirligi |
|----------|-------------|---------------------|
| **Opioid** | MOR, DOR, KOR, NOP | %25-95 |
| **Dopaminerjik** | DAT, D1, D2, D3, D4, D5 | %50-92 |
| **Serotonerjik** | SERT, 5-HT1A, 5-HT1B, 5-HT2A, 5-HT2C, 5-HT3 | %30-60 |
| **GABAerjik** | GABA-A (alpha1-5, gamma2, delta), GABA-B | %45-75 |
| **Glutamaterjik** | NMDA NR1/NR2B, AMPA, mGluR2/5 | %40-60 |
| **Kannabinoid** | CB1, CB2 | %25-55 |
| **Kolinerjik** | nAChR (a4b2, a7, a3b4), mAChR (M1, M2) | %30-85 |
| **Adrenerjik** | NET, Alpha2A, Beta1 | %35-65 |
| **Stres/Neuropeptid** | CRF1/2, OX1/2, NK1, NPY-Y1 | %40-65 |
| **Sigma** | Sigma-1, Sigma-2 | %35-50 |
| **Enzimler** | MAO-A/B, COMT, FAAH | %40-45 |
| **Sinyal** | CREB, DeltaFosB, mTOR | %35-55 |

### 5.2 Her Reseptor Icin Cikti

```
ReceptorProfile:
- receptor_name: Reseptor adi
- gene: Gen sembolu
- uniprot: UniProt ID
- addiction_weight: Bagimlilik agirligi (0.0-1.0)
- mechanism: Biyolojik mekanizma
- ligands: Bilinen ligand listesi
- source: Veri kaynagi (IUPHAR, DrugBank, ChEMBL)
```

---

## 6. REGULATUVAR SINIFLANDIRMA

### 6.1 UN/WHO/EMCDDA Schedule

| Schedule | Abuse Skoru | Tanim | Ornekler |
|----------|-------------|-------|----------|
| I | %95 | Yuksek istismar, tibbi kullanim yok | Heroin, LSD, MDMA |
| II | %85 | Yuksek istismar, sinirli tibbi | Morfin, Fentanil, Kokain |
| III | %65 | Orta istismar, tibbi kullanim var | Buprenorfin, Ketamin |
| IV | %45 | Dusuk-orta istismar | Benzodiazepinler, Tramadol |
| V | %25 | Dusuk istismar | Pregabalin, Dusuk doz kodein |
| Unscheduled | %10 | Kontrolsuz | Kafein |

### 6.2 Istismar Potansiyeli Hesaplama

```
AbusePotentialResult:
- abuse_score: Istismar potansiyeli (0.0-1.0)
- confidence_interval: %95 CI
- schedule_prediction: Tahmini schedule (I-V)
- risk_category: Risk kategorisi
- receptor_contribution: Reseptor katkisi
- pk_contribution: Farmakokinetik katkisi
- chemical_contribution: Kimyasal ozellik katkisi
- references: Literatur referanslari
```

---

## 7. POLIGENIK RISK SKORU (PRS)

### 7.1 Hesaplanan PRS Ozellikleri

| Ozellik | GWAS Kaynak | SNP Sayisi |
|---------|-------------|------------|
| Alkol bagimliligi | GSCAN, MVP | 99+ |
| Opioid kullanim bozuklugu | MVP | 50+ |
| Kannabis kullanim bozuklugu | iPSYCH | 40+ |
| Nikotin bagimliligi | TAG, GSCAN | 55+ |
| Depresyon | PGC-MDD | 102+ |
| Anksiyete | ANGST | 45+ |
| ADHD | PGC-ADHD | 12+ |
| Sizofreni | PGC-SCZ | 128+ |

### 7.2 PRS Cikti Yapisi

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

## 8. KRONIK HASTALIK ETKILESIM ANALIZI

### 8.1 Desteklenen Hastaliklar

| Kategori | Hastaliklar |
|----------|-------------|
| Metabolik | Tip 2 Diyabet, Obezite, Metabolik Sendrom |
| Kardiyovaskuler | Hipertansiyon, Koroner Arter Hastaligi, Kalp Yetmezligi |
| Solunum | KOAH, Astim, Akciger Kanseri |
| Norolojik | Alzheimer, Parkinson, MS |
| Hepatik | Karaciger Sinozu, Hepatit, Yaglanma |
| Renal | Kronik Bobrek Hastaligi |
| Psikiyatrik | Depresyon, Anksiyete, PTSD |
| Onkolojik | Cesitli kanser turleri |

### 8.2 Hastalik-EAA Etki Verileri

```
DiseaseEAAEffect:
- disease_name: Hastalik adi
- category: Hastalik kategorisi
- eaa_effect: EAA etkisi (yil)
- ci_lower: Alt guven siniri
- ci_upper: Ust guven siniri
- sample_size: Arastirma ornek boyutu
- clock_type: Kullanilan saat
- reference: Literatur referansi
- pmid: PubMed ID
- mechanism: Biyolojik mekanizma
- reversibility: Tersine cevrilebilirlik (Evet/Kismi/Hayir)
```

---

## 9. MEDIYASYON VE MODERASYON ANALIZI

### 9.1 Fizyolojik Mediyatorler

| Mediyator | Mediyasyon % | Olcum Metodu |
|-----------|--------------|--------------|
| Insulin Direnci (HOMA-IR) | %34 | Glukoz + Insulin |
| HPA Eksen (Kortizol/ACTH) | %29 | Serum kortizol |
| Sistemik Inflamasyon (CRP/IL-6) | %37 | CRP, IL-6, TNF-alpha |
| **Toplam Indirekt Etki** | **%61** | - |
| **Direkt Etki** | **%39** | - |

### 9.2 Psikolojik Moderatorler

| Moderator | Olcek | Etki |
|-----------|-------|------|
| Duygu Duzenleme | DERS (Difficulties in Emotion Regulation Scale) | 3.7x fark |
| Oz-Kontrol | SCS-B (Brief Self-Control Scale) | %54 azalma |

### 9.3 Moderasyon Analizi Ciktilari

```
ModerationResult:
- moderator_name: Moderator adi
- main_effect: Ana etki (beta)
- interaction_effect: Etkilesim etkisi (beta)
- simple_slopes: Farkli seviyelerde etkiler
  - low_level: Dusuk seviye etkisi
  - mean_level: Ortalama seviye etkisi
  - high_level: Yuksek seviye etkisi
- johnson_neyman_threshold: Anlamlilik esigi
- r_squared: Aciklanan varyans
- delta_r_squared: Etkilesim katkisi
```

---

## 10. POSTMORTEM VE ADLI ANALIZ

### 10.1 PMI Duzeltme Algoritmasi

```
PMICorrectionResult:
- original_age: Orijinal epigenetik yas
- corrected_age: Duzeltilmis yas
- pmi_hours: PMI suresi (saat)
- tissue_ph: Doku pH degeri
- correction_factor: Duzeltme faktoru
- quality_category: Kalite kategorisi (Mukemmel/Iyi/Orta/Zayif)
- reliability_score: Guvenilirlik skoru (%0-100)
```

### 10.2 Adli Uygulama Ciktilari

- Kronik madde kullanim gecmisi tahmini
- Madde turu siniflandirmasi (%87.3 dogruluk)
- Kullanim suresi tahmini (yil)
- Doku kalitesi degerlendirmesi
- Daubert kriterleri uyumluluk raporu

---

## 11. BLOCKCHAIN AUDIT TRAIL

### 11.1 Audit Kayit Yapisi

```
AuditLogEntry:
- log_id: Kayit ID
- timestamp: Zaman damgasi
- user_id: Kullanici ID
- action: Islem turu (Ornek Girisi, Analiz, Rapor, Erisim)
- data_payload: Islem verisi (JSON)
- previous_hash: Onceki blok hash
- current_hash: Mevcut blok hash (SHA-256)
```

### 11.2 Zincir Dogrulama

```
ChainValidationResult:
- is_valid: Gecerlilik durumu (True/False)
- total_blocks: Toplam blok sayisi
- validated_blocks: Dogrulanan blok sayisi
- first_invalid_block: Ilk gecersiz blok (varsa)
- error_message: Hata mesaji
- validation_timestamp: Dogrulama zamani
- validation_hash: Dogrulama hash
```

---

## 12. RAPOR VE VERI EXPORT

### 12.1 PDF Klinik Rapor Icerigi

1. Hasta/Ornek Bilgileri
2. Epigenetik Saat Sonuclari (5 saat)
3. Madde Tespit Sonuclari
4. Risk Degerlendirmesi
5. Klinik Yorumlar ve Oneriler
6. Gorselletirmeler (Radar, Bar, Scatter)
7. Teknik Detaylar ve Kalite Metrikleri
8. Referanslar

### 12.2 Veri Export Formatlari

| Format | Kullanim Alani | Icerik |
|--------|----------------|--------|
| CSV | Excel, R, Python | Tablo verileri |
| BED | Genom tarayici (UCSC, IGV) | CpG koordinatlari |
| JSON | API entegrasyonu | Yapisal veri |
| SQL | Veritabani | Sema + INSERT statements |

---

## 13. VERITABANI ISTATISTIKLERI

### 13.1 Platform Veritabani Boyutlari

| Veritabani | Kayit Sayisi |
|------------|--------------|
| CpG Markerlari | 850,000+ |
| Madde Paneli | 36,000+ |
| NPS Turevleri | 200+ |
| GWAS Loci | 500+ |
| EWAS Markerlari | 1,000+ |
| PharmGKB Genleri | 150+ |
| Reseptor Hedefleri | 55+ |

### 13.2 Genom Kapsamı

| Platform | CpG Kapsamı |
|----------|-------------|
| Illumina 450K | 485,512 |
| Illumina EPIC | 865,859 |
| Ortak Set | 452,626 |

---

## 14. GORSELLESTIRME CIKTILARI

### 14.1 Plotly Interaktif Grafikler

1. **Kronolojik vs Epigenetik Yas Scatter Plot**
   - Korelasyon gosterimi
   - Grup renklendirmesi
   - Regresyon cizgisi

2. **EAA Karsilastirma Bar Chart**
   - Madde gruplari karsilastirmasi
   - Guven araliklari

3. **Radar/Spider Chart**
   - 5 saat karsilastirmasi
   - Multi-boyutlu profil

4. **Heatmap**
   - CpG metilasyon desenleri
   - Gen kume analizi

5. **Longitudinal Trend Grafigi**
   - Zaman serisi EAA
   - Mudahale etkileri

### 14.2 Matplotlib Statik Grafikler

- Yayin kalitesi figurler
- PDF export destegi
- Ozellestirilmis tema

---

## 15. ENTEGRE VERITABANLARI

### 15.1 Genomik Veritabanlari

| Veritabani | Icerik | Kaynak |
|------------|--------|--------|
| GWAS Catalog | Bagimlilik genetik varyantlari | EBI/NHGRI |
| EWAS Atlas | Epigenetik isletler | Bristol |
| ClinVar | Klinik varyant yorumlari | NCBI |
| gnomAD | Populasyon frekans verileri | Broad |
| PharmGKB | Farmakogenetik iliskiler | Stanford |
| CPIC | Klinik rehberler | PharmGKB |

### 15.2 Kimyasal Veritabanlari

| Veritabani | Icerik |
|------------|--------|
| PubChem | Kimyasal yapilar |
| ChEMBL | Biyoaktivite verileri |
| DrugBank | Ilac bilgileri |
| IUPHAR/BPS | Reseptor farmakololijisi |

### 15.3 Regulatuvar Veritabanlari

| Kaynak | Icerik |
|--------|--------|
| UNODC | Uluslararasi kontrol listeleri |
| WHO | Uzman komite raporlari |
| EMCDDA | Avrupa NPS izleme |
| DEA | ABD schedule listeleri |

---

## 16. KALITE KONTROL METRIKLERI

### 16.1 DNA Metilasyon QC

- Bisulfit donusum orani (>%95 gerekli)
- Deteksiyon p-degeri kontrolu
- Cinsiyet tahmini ve dogrulama
- Genetik kimlik kontrolu (SNP)
- Batch etkisi degerlendirmesi

### 16.2 Analiz QC

- Ornek kalite skoru (%0-100)
- CpG kapsam orani
- Missing data yuzdesi
- Outlier tespiti
- Replikasyon tutarliligi

---

## 17. PERFORMANS METRIKLERI

### 17.1 Siniflandirma Performansi

| Metrik | Deger |
|--------|-------|
| Genel Dogruluk | %87.3 |
| Kontrol F1-Score | 0.98 |
| Alkol F1-Score | 0.88 |
| Kokain F1-Score | 0.86 |
| Opioid F1-Score | 0.87 |
| Kannabis F1-Score | 0.74 |

### 17.2 Regresyon Performansi

| Saat | MAE (yil) | RMSE (yil) | R-squared |
|------|-----------|------------|-----------|
| Horvath | 3.6 | 4.8 | 0.94 |
| GrimAge | 4.0 | 5.2 | 0.92 |
| DunedinPACE | N/A | N/A | 0.89 |

---

## 18. API VE ENTEGRASYON

### 18.1 Desteklenen Girdi Formatlari

- IDAT dosyalari (Illumina raw)
- Beta deger matrisi (CSV)
- GEO Series Matrix
- VCF dosyalari (genetik varyantlar)
- SMILES string (molekul)

### 18.2 Cikti Formatlari

- JSON (API response)
- CSV (tablo)
- PDF (rapor)
- PNG/SVG (grafik)
- BED (genom koordinat)
- SQL (veritabani)

---

**NOTLAR:**
- Bu PROTOTIP platformdur - gercek klinik kararlarda kullanilmamalidir
- Epigenetik saat katsayilari simulasyondur - gercek katsayilar UCSD lisansi gerektirir
- Referans veritabani demonstrasyon amaclidir

**GitHub:** github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
**Yazar:** Dr. Nurcan Denli Bayir (nrcdnl94)
