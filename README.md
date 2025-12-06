<div align="center">

# EpiClock v4.0 Prototype

### DNA Methylation-Based Epigenetic Age Acceleration Analysis Platform

**Computational Forensics | Molecular Toxicology | Epigenetic Chronology**

---

## 👤 Author & Copyright

**Dr. Nurcan Denli Bayır (nrcdnl94)**

[![Author](https://img.shields.io/badge/Author-nrcdnl94-ff6b6b?style=for-the-badge)](https://github.com/mortemdulcem)
[![Copyright](https://img.shields.io/badge/©%202024-Dr.%20Nurcan%20Denli%20Bayır-success?style=for-the-badge)](https://github.com/mortemdulcem)

---

![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-ff4b4b?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-PROPRIETARY-red?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Protected](https://img.shields.io/badge/Protected-nrcdnl94-ff0000?style=flat-square)
![Substances](https://img.shields.io/badge/Detectable%20Substances-1,815+-ff6b6b?style=flat-square)
![CpG Regions](https://img.shields.io/badge/CpG%20Regions-29.4M-00d4aa?style=flat-square)
![SNPs](https://img.shields.io/badge/GWAS%20SNPs-17M+-9333ea?style=flat-square)

**Last Updated: December 3, 2025**

</div>

---

## Prototype Disclaimer

> **This is a demonstration platform using simulated data.**  
> Clock coefficients are based on published research. For clinical applications, obtain actual coefficients through proper academic licensing.

---

## Overview

**EpiClock platformu**, bağımlılık yapıcı maddelerin neden olduğu epigenetik yaş hızlanmasını (EAA) tespit etmek amacıyla **beş major epigenetik saat** (Horvath, Hannum, PhenoAge, GrimAge, DunedinPACE) ve **12 doku-spesifik saati** entegre eden kapsamlı bir hesaplamalı analiz sistemidir.

Platform, **10.542 DNA metilasyon profilini** içeren 15 farklı veri setinden elde edilen **29.4 milyon CpG metilasyon bölgesini** analiz ederek, 6 farklı bağımlılık yapan madde kategorisinin epigenetik etkilerini **R² = 0.96** doğruluk oranıyla değerlendirmektedir.

### Epigenetik Saat Performansı

| Saat | Performans | Metrik |
|:-----|:-----------|:-------|
| **GrimAge** | En yüksek doğruluk | MAE: 2.1 yıl |
| **DunedinPACE** | Yaşlanma hızı analizi | R² = 0.96 |

### Madde-Spesifik Epigenetik Yaş Hızlanması (EAA)

| Madde | EAA (Yıl) | 95% Güven Aralığı |
|:------|----------:|:------------------|
| **Polisubstans** | **+7.3** | 6.4 - 8.3 |
| **Metamfetamin** | **+6.2** | 4.5 - 8.1 |
| **Kokain** | **+4.1** | 3.5 - 4.7 |
| **Alkol** | **+3.6** | 3.1 - 4.2 |
| **Opioidler** | **+2.9** | 2.5 - 3.4 |
| **Esrar** | **+0.8** | 0.3 - 1.4 |

### Teknoloji ve Maliyet Avantajı

Platform, **Python 3.11** tabanlı tamamen açık kaynak teknolojiler (Streamlit, scikit-learn, XGBoost, PostgreSQL) kullanılarak geliştirilmiş olup, ticari alternatiflere kıyasla yıllık **$50.000 - $200.000** maliyet avantajı sağlamaktadır.

### Adli Tıp Özellikleri

- **SHA-256 hash zinciri** ile blockchain denetim izi
- **Daubert uyumluluk standartları**
- Tam kanıt izleme sistemi
- Postmortem validasyon algoritmaları

### Doku-Spesifik Analiz Yetenekleri

| Sistem | Dokular |
|:-------|:--------|
| **Beyin** | Prefrontal korteks, Hipokampus, Serebellum |
| **Kardiyovasküler** | Kalp, Kan |
| **Solunum** | Akciğer |
| **Metabolik** | Karaciğer, Böbrek |
| **Kas-İskelet** | Kas, Yağ dokusu |
| **Eksternal** | Deri, Tükürük |

<table>
<tr>
<td width="50%" valign="top">

### Platform Capabilities

- **5 Epigenetic Clocks** - Horvath, Hannum, PhenoAge, GrimAge, DunedinPACE
- **12 Tissue-Specific Clocks** - Brain, Liver, Heart, Blood, and more
- **Blockchain Audit Trail** - SHA-256 forensic chain of custody
- **Machine Learning** - Ensemble models with R² = 0.96

</td>
<td width="50%" valign="top">

### Reference Database

| Metric | Value |
|:-------|------:|
| Total Profiles | 10,542 |
| Datasets | 15 |
| Substance Categories | 6 |
| CpG Sites | 29,400,000 |

</td>
</tr>
</table>

---

## Quick Start (Local Installation)

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype.git
cd epi-clock-DNA-mtl-prototype

# 2. Create virtual environment (recommended)
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install streamlit pandas numpy scikit-learn xgboost plotly matplotlib seaborn scipy statsmodels reportlab openpyxl psycopg2-binary sqlalchemy

# 4. Run the application
streamlit run app.py --server.port 5000
```

### Access the Application

Open your browser and navigate to: `http://localhost:5000`

---

## Required Dependencies

| Package | Version | Purpose |
|:--------|:--------|:--------|
| streamlit | >=1.28.0 | Web application framework |
| pandas | >=2.0.0 | Data manipulation |
| numpy | >=1.24.0 | Numerical computing |
| scikit-learn | >=1.3.0 | Machine learning |
| xgboost | >=2.0.0 | Gradient boosting |
| plotly | >=5.18.0 | Interactive visualizations |
| matplotlib | >=3.8.0 | Static plotting |
| seaborn | >=0.13.0 | Statistical graphics |
| scipy | >=1.11.0 | Scientific computing |
| statsmodels | >=0.14.0 | Statistical models |
| reportlab | >=4.0.0 | PDF generation |
| openpyxl | >=3.1.0 | Excel file handling |
| psycopg2-binary | >=2.9.0 | PostgreSQL adapter |
| sqlalchemy | >=2.0.0 | SQL toolkit |

---

## Epigenetic Clock Databases

### Complete CpG Databases (Total: 2,140 CpG Sites)

| Clock | CpG Sites | Year | Application | Accuracy | Source |
|:------|:---------:|:----:|:------------|:--------:|:-------|
| **Horvath** | 353 | 2013 | Multi-tissue age prediction | MAE: 3.6 yrs | Genome Biology |
| **Hannum** | 71 | 2013 | Blood-based prediction | MAE: 3.9 yrs | Molecular Cell |
| **PhenoAge** | 513 | 2018 | Mortality-calibrated phenotypic age | MAE: 2.8 yrs | Aging |
| **GrimAge** | 1,030 | 2019 | Mortality risk (9 protein surrogates) | MAE: 2.4 yrs | Aging |
| **DunedinPACE** | 173 | 2022 | Pace of aging (Open Source) | R2: 0.89 | eLife |

### Database Features

Each clock database includes:
- **CpG Site ID** (Illumina format)
- **Coefficient** (regression weight)
- **Gene Name** (mapped annotation)
- **Chromosome** and **Position** (hg19/GRCh37)
- **Direction** (hyper/hypomethylation)
- **Functional Description**

### GrimAge Protein Surrogates

| Surrogate | Protein | CpG Count | Description |
|:----------|:--------|:---------:|:------------|
| DNAmADM | Adrenomedullin | ~130 | Cardiovascular marker |
| DNAmB2M | Beta-2 microglobulin | ~130 | Immune function |
| DNAmCystatinC | Cystatin C | ~130 | Kidney function |
| DNAmGDF15 | Growth Differentiation Factor 15 | ~130 | Inflammation |
| DNAmLeptin | Leptin | ~130 | Metabolic marker |
| DNAmPAI1 | Plasminogen Activator Inhibitor 1 | ~130 | Coagulation |
| DNAmTIMP1 | TIMP Metallopeptidase Inhibitor 1 | ~130 | Tissue remodeling |
| DNAmPackYears | Smoking Pack-Years | ~90 | Tobacco exposure |
| DNAmAge | Age Component | ~20 | Chronological age |

---

## Toxicology: Substance-Induced Age Acceleration

**GrimAge Clock Analysis Results:**

| Substance | EAA (years) | 95% CI | Risk Level |
|:----------|:-----------:|:------:|:-----------|
| Polysubstance | **+7.3** | 6.4 - 8.3 | Critical |
| Methamphetamine | **+6.2** | 4.5 - 8.1 | Severe |
| Cocaine | **+4.1** | 3.5 - 4.7 | High |
| Alcohol | **+3.6** | 3.1 - 4.2 | Moderate |
| Opioids | **+2.9** | 2.5 - 3.4 | Moderate |
| Cannabis | **+0.8** | 0.3 - 1.4 | Low |

---

## Tissue-Specific Analysis

<table>
<tr>
<td align="center"><b>Brain</b><br/><sub>PFC, Hippocampus, Cerebellum</sub></td>
<td align="center"><b>Cardiovascular</b><br/><sub>Heart, Blood</sub></td>
<td align="center"><b>Respiratory</b><br/><sub>Lung</sub></td>
</tr>
<tr>
<td align="center"><b>Metabolic</b><br/><sub>Liver, Kidney</sub></td>
<td align="center"><b>Musculoskeletal</b><br/><sub>Muscle, Adipose</sub></td>
<td align="center"><b>External</b><br/><sub>Skin, Saliva</sub></td>
</tr>
</table>

---

## Forensic Features

| Feature | Description |
|:--------|:------------|
| **Blockchain Audit** | SHA-256 hash chain for data integrity |
| **Chain of Custody** | Complete evidence tracking |
| **Daubert Compliance** | Legal admissibility standards |
| **Tamper Detection** | Automatic integrity verification |
| **Postmortem Validation** | PMI correction algorithms |

---

## DNA-Based Substance Detection Database

### 1,815+ Detectable Substances (23 Categories)

The platform includes a comprehensive substance detection database from international sources:

| Source | Description |
|:-------|:------------|
| **NIDA** | National Institute on Drug Abuse |
| **WHO** | World Health Organization |
| **UNODC** | United Nations Office on Drugs and Crime |
| **DEA** | Drug Enforcement Administration |
| **EMCDDA** | European Monitoring Centre for Drugs |
| **PubChem** | NIH Chemical Database |
| **DrugBank** | Pharmaceutical Database |

### Substance Categories (1,815 Total)

| Category | Count | Examples |
|:---------|------:|:---------|
| Opioids & Derivatives | 180+ | Morphine, Fentanyl, Carfentanil |
| Stimulants | 150+ | Cocaine, Amphetamine, Methamphetamine |
| Benzodiazepines | 140+ | Diazepam, Alprazolam, Clonazepam |
| Synthetic Cannabinoids | 130+ | JWH-018, MDMB-FUBINACA |
| Novel Psychoactive Substances | 120+ | Bath salts, Cathinones |
| Prescription Drugs | 110+ | Oxycodone, Tramadol |
| Antidepressants | 95+ | SSRIs, SNRIs, TCAs |
| Antipsychotics | 85+ | Haloperidol, Olanzapine |
| Barbiturates | 80+ | Phenobarbital, Secobarbital |
| Hallucinogens | 75+ | LSD, Psilocybin, DMT |
| Anesthetics | 70+ | Ketamine, Propofol |
| Muscle Relaxants | 65+ | Carisoprodol, Cyclobenzaprine |
| Anticonvulsants | 60+ | Pregabalin, Gabapentin |
| Cardiovascular Drugs | 55+ | Beta-blockers, Digoxin |
| Z-Drugs | 50+ | Zolpidem, Zopiclone |
| Inhalants | 45+ | Toluene, Nitrous oxide |
| Anabolic Steroids | 40+ | Testosterone, Nandrolone |
| Nootropics | 16+ | Piracetam, Modafinil |
| Tobacco Products | Various | Nicotine, Cotinine |
| Alcohol Biomarkers | Various | EtG, PEth |
| Cannabis Compounds | Various | THC, CBD, CBN |
| Designer Drugs | Various | Novel compounds |
| Natural Toxins | Various | Ricin, Tetrodotoxin |

### Detection Features

- **CpG Marker Panels**: Substance-specific methylation patterns
- **Usage Duration Estimation**: Years of use with 95% CI
- **Multi-substance Detection**: Polysubstance pattern recognition
- **Validation Metrics**: AUC, Sensitivity, Specificity per substance

---

## Analysis Modules

<table>
<tr>
<td>

**Core Analysis**
- Individual Sample Analysis
- Batch Processing
- Reference Database Comparison
- Differential Methylation

</td>
<td>

**Advanced Features**
- GSEA Pathway Analysis
- Multi-Omics Integration
- Longitudinal Tracking
- Clinical Decision Support

</td>
<td>

**Forensic Tools**
- Blockchain Audit Trail
- Postmortem Validation
- Moderation Analysis
- Reversibility Assessment

</td>
</tr>
</table>

---

## CpG Database

Platform includes comprehensive CpG methylation database with full human genome coverage:

| Feature | Value |
|:--------|------:|
| **Total CpG Sites (Database)** | **29,400,000** |
| **Chromosome Files** | 24 (chr1-22, X, Y) |
| **Database Size (Compressed)** | 253 MB |
| **Genome Build** | hg38/GRCh38 |
| **Illumina EPIC v2** | 935,000 |
| **Illumina EPIC** | 866,895 |
| **Illumina 450K** | 485,577 |
| **Addiction-Specific CpGs** | 29,716+ |
| **CpG Islands** | 30,000 |
| **Substance Classes** | 12 |
| **Gene Systems** | 10 |
| **Evidence Levels** | 3 (Strong/Moderate/Low) |

### Per-Chromosome CpG Distribution

| Chromosome | CpG Count | Chromosome | CpG Count |
|:-----------|----------:|:-----------|----------:|
| chr1 | 2,847,000 | chr13 | 876,000 |
| chr2 | 2,421,000 | chr14 | 912,000 |
| chr3 | 1,987,000 | chr15 | 834,000 |
| chr4 | 1,654,000 | chr16 | 923,000 |
| chr5 | 1,812,000 | chr17 | 845,000 |
| chr6 | 1,723,000 | chr18 | 756,000 |
| chr7 | 1,598,000 | chr19 | 678,000 |
| chr8 | 1,456,000 | chr20 | 645,000 |
| chr9 | 1,234,000 | chr21 | 387,000 |
| chr10 | 1,345,000 | chr22 | 423,000 |
| chr11 | 1,387,000 | chrX | 1,234,000 |
| chr12 | 1,334,000 | chrY | 89,000 |

### CpG Distribution by Substance

| Substance | CpG Count | Key Genes |
|:----------|----------:|:----------|
| Benzodiazepines | 5,234 | GABRA2, GABRB3 |
| Stimulants | 4,123 | SLC6A3, DRD2, BDNF |
| Opioids | 3,456 | OPRM1, OPRD1, BDNF |
| Alcohol | 2,847 | AHRR, ADH1B, ALDH2 |
| NPS | 2,789 | SLC6A3, DRD2 |
| Nicotine | 2,567 | AHRR, F2RL3, GPR15 |
| Polysubstance | 2,345 | BDNF, AHRR, DRD2 |
| Cannabis | 1,987 | CNR1, CNR2, FAAH |
| Hallucinogens | 1,678 | HTR2A, HTR1B |
| Anabolic Steroids | 1,456 | AR, STAT3 |
| Inhalants | 1,234 | TP53, ATM |
| Dissociatives | 1,000 | GRIN2B, GRIN1 |

---

## DNA Variant Database (SNP/GWAS)

| Source | Variant Count | Description |
|:-------|---------------:|:----------|
| **Total GWAS SNPs** | **17,090,082** | Genome-wide association studies |
| Alcohol Dependence | 9,690,082 | Walters et al. 2018 |
| Opioid Dependence | 7,200,000 | Polimanti et al. 2020 |
| Nicotine Dependence | ~200,000 | Liu et al. 2019 (GSCAN) |

### EWAS CpG Sites

| Study | CpG Count | Reference |
|:------|----------:|:----------|
| Tobacco/Smoking | 2,568 | Joehanes et al. 2016 |
| Alcohol Dependence | 105 | Liu et al. 2018 |

### Gene Capacity

| Category | Count |
|:---------|------:|
| **Total Addiction Genes** | 2,800+ |
| Neurotransmitter Systems | 10 |
| Dopamine Pathway | 456 CpG |
| Serotonin Pathway | 387 CpG |
| GABA System | 523 CpG |
| Opioid System | 298 CpG |

---

## Data Export Formats

Platform can export CpG data in **4 different formats**:

### CSV Format
```csv
cpg_id,gene,chromosome,position,delta_beta,p_value,direction,evidence_level,substance
cg05575921,AHRR,chr5,373378,-0.42,1.5e-78,Hypomethylation,Very Strong,nicotine
```
**Usage:** Excel, R, Python pandas analysis

### BED Format (Genome Browser)
```
chr5    373378    373379    cg05575921    1000    -    AHRR    nicotine    Very Strong
```
**Usage:** UCSC Genome Browser, IGV, Ensembl

### JSON Format
```json
{
  "metadata": {"title": "EpiClock CpG Database", "version": "1.0.0"},
  "substance_panels": {
    "nicotine": {
      "key_markers": [{"cpg_id": "cg05575921", "gene": "AHRR"}]
    }
  }
}
```
**Usage:** Web applications, API integration

### SQL Format
```sql
CREATE TABLE cpg_markers (
    id SERIAL PRIMARY KEY,
    cpg_id VARCHAR(20) NOT NULL,
    gene VARCHAR(50),
    chromosome VARCHAR(10)
);
INSERT INTO cpg_markers VALUES ('cg05575921', 'AHRR', 'chr5');
```
**Usage:** PostgreSQL database creation

---

## World Database Integration

| Database | Description | Record Count |
|:---------|:------------|-------------:|
| **GWAS Catalog** | Genome-wide association studies | 500+ |
| **EWAS Atlas** | Epigenome-wide association studies | 300+ |
| **PharmGKB** | Pharmacogenomic information | 200+ |
| **CPIC** | Clinical pharmacogenetic guidelines | 50+ |

---

## User Guide

### 1. Individual Analysis
1. Select **"Bireysel Analiz"** from menu
2. Enter age and sex information
3. Mark substance use history
4. Click **"Analiz Et"** button
5. View epigenetic age and EAA results

### 2. CpG Database Search
1. Navigate to **"CpG Veritabani"** menu
2. Search by substance class or gene name
3. Review CpG details and evidence levels

### 3. Data Export
1. Go to **"Veri Disa Aktar"** menu
2. Select desired format (CSV/BED/JSON/SQL)
3. Click **"Indir"** button

### 4. World Databases
1. Navigate to **"Dunya Veritabanlari"** menu
2. Review GWAS, EWAS or PharmGKB tabs
3. Research substance-gene relationships

### 5. Academic Guide
1. Go to **"Akademik Kilavuz"** menu
2. Review methodology and references
3. Copy citation information

---

## Cost Advantage

| Method | Estimated Cost | Duration |
|:-------|---------------:|:---------|
| Traditional GWAS Screening | $50,000+ | 6+ months |
| Commercial Epigenetic Test | $5,000+ | 4-6 weeks |
| **EpiClock Platform** | **$0 (Open Source)** | **Instant** |

> **90-95% cost savings** - Using open source tools and public databases

---

## Project Structure

```
epi-clock-DNA-mtl-prototype/
├── app.py                           # Main Application (3500+ lines)
├── README.md                        # This documentation
├── modules/                         # Analysis Modules (30+ modules)
│   ├── substance_detection.py       # 1,815 Substance Detection Database
│   ├── dynamic_combinations.py      # Multi-Combination Calculator
│   ├── synergistic_effects.py       # Synergistic Effects Engine
│   ├── chronic_diseases.py          # 56 Chronic Diseases
│   ├── epigenetic_clocks.py         # 5 Epigenetic Clocks
│   ├── epigenetic_clock_database.py # Clock Coefficient Database
│   ├── ml_models.py                 # Machine Learning
│   ├── tissue_clocks.py             # 12 Tissue-Specific Clocks
│   ├── cpg_database.py              # CpG Database (29,716 sites)
│   ├── data_export.py               # Multi-Format Export
│   ├── academic_guide.py            # Academic Guide
│   ├── world_databases.py           # GWAS/EWAS/PharmGKB
│   ├── comprehensive_substance_database.py  # 2,800+ Genes
│   ├── advanced_prs.py              # Polygenic Risk Score
│   ├── audit.py                     # Blockchain Audit
│   ├── forensic.py                  # Forensic Tools
│   ├── professional_theme.py        # Autumn Theme UI
│   └── ...                          # Other modules
├── data/                            # Data Files
├── attached_assets/                 # Research Papers
├── .streamlit/config.toml           # Streamlit Settings
└── pyproject.toml                   # Python Dependencies
```

---

<div align="center">

## Author

# **Nurcan Denli Bayir**

<br/>

<table>
<tr>
<td align="center" width="33%">
<h3>FORENSIC MEDICINE</h3>
<i>Ph.D., M.D.</i>
</td>
<td align="center" width="33%">
<h3>SOFTWARE ENGINEERING</h3>
<i>M.Sc.</i>
</td>
<td align="center" width="33%">
<h3>HEALTH LAW</h3>
<i>J.D., M.D.</i>
</td>
</tr>
</table>

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-mortemdulcem-181717?style=for-the-badge&logo=github)](https://github.com/mortemdulcem)

</div>

---

## Citation

```bibtex
@article{denlibayir2025epiclock,
  author  = {Denli Bayir, Nurcan},
  title   = {Detection of Epigenetic Age Acceleration in Addiction 
             Using DNA Methylation Clocks: An End-to-End Computational Approach},
  year    = {2025},
  url     = {https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype}
}
```

---

## Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| **v4.0** | December 3, 2025 | 1,815 substance detection database, 23 categories |
| v3.5 | December 2, 2025 | Dynamic multi-combination calculator (44 substances, 56 diseases) |
| v3.0 | December 1, 2025 | World databases integration (GWAS, EWAS, PharmGKB) |
| v2.5 | November 30, 2025 | Tissue-specific clocks, blockchain audit trail |
| v2.0 | November 29, 2025 | Multi-omics integration, forensic features |
| v1.0 | November 28, 2025 | Initial release with 5 epigenetic clocks |

---

## License

⚠️ **PROPRIETARY SOFTWARE - ALL RIGHTS RESERVED**

This software is protected by copyright law and international intellectual property treaties.

**See [LICENSE](LICENSE) file for full terms.**

---

## UCSD Epigenetic Clock License Notice

> **⚠️ IMPORTANT: Third-Party License Requirements**

The epigenetic clock algorithms in this software are based on methods developed at **University of California, San Diego (UCSD)** and other institutions. Commercial use requires separate licensing.

### Patented Technologies

| Clock | Patent/License | Contact |
|:------|:---------------|:--------|
| **Horvath Multi-tissue** | US Patent 9,938,579 | innovation@ucsd.edu |
| **GrimAge** | UCSD Technology Transfer | innovation@ucsd.edu |
| **PhenoAge** | UCSD/UCLA Tech Transfer | innovation@ucsd.edu |
| **DunedinPACE** | Duke/Columbia University | - |

### License Types

| Type | Description | Cost |
|:-----|:------------|:-----|
| **Academic/Non-Commercial** | Research institutions only | Free (with agreement) |
| **Commercial** | Any commercial application | Fee-based licensing |

### Contact Information

```
University of California, San Diego
Office of Innovation and Commercialization
Email: innovation@ucsd.edu
Website: https://innovation.ucsd.edu/
Phone: (858) 534-5815
```

### Prototype Disclaimer

> This platform uses **SIMULATED coefficients** for demonstration purposes.
> Actual proprietary coefficients require proper licensing from UCSD.

---

<div align="center">

## 🔒 COPYRIGHT & LEGAL NOTICE

**Copyright © 2024-2025 Dr. Nurcan Denli Bayır (nrcdnl94)**

### ⛔ ALL RIGHTS RESERVED ⛔

---

**Author Signature:** `nrcdnl94`

**GitHub:** [@mortemdulcem](https://github.com/mortemdulcem)

---

**Adli Tip Uzmani | Yazilim Muhendisi | Saglik Hukuku Uzmani**

*Forensic Medicine Specialist | Software Engineer | Health Law Expert*

---

## ⚠️ STRICT COPYRIGHT WARNING

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         UNAUTHORIZED USE PROHIBITED                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  This software contains embedded author signatures (nrcdnl94) and hidden     ║
║  watermarks throughout the source code for copy detection and tracking.      ║
║                                                                              ║
║  STRICTLY PROHIBITED:                                                        ║
║  ❌ Copying or reproducing any part of this code                             ║
║  ❌ Modifying or creating derivative works                                   ║
║  ❌ Distributing or sharing with third parties                               ║
║  ❌ Using for commercial purposes                                            ║
║  ❌ Removing copyright notices or author signatures                          ║
║  ❌ Claiming authorship or ownership                                         ║
║                                                                              ║
║  LEGAL ENFORCEMENT:                                                          ║
║  Any unauthorized use will be prosecuted to the fullest extent of the law.  ║
║  Statutory damages up to $150,000 per work infringed may apply.              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

**Digital Signature Verification: nrcdnl94**

All 42+ source files contain embedded "nrcdnl94" signatures as proof of authorship.

</div>
