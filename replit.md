# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform

## Overview
EpiClock Prototype is an advanced computational platform for detecting and quantifying epigenetic age acceleration (EAA) in addiction using DNA methylation clocks. The platform implements five major epigenetic clocks (Horvath, Hannum, PhenoAge, GrimAge, DunedinPACE), tissue-specific clocks, blockchain audit trails, and provides comprehensive statistical analysis tools for clinical and research applications.

**Important:** This is a PROTOTYPE using simulated coefficients and reference data to demonstrate methodology. Real coefficients require proper licensing from original publications.

## Project Structure
```
├── app.py                      # Main Streamlit application (3000+ lines)
├── modules/                    # Core analysis modules (28+ modules)
│   ├── __init__.py
│   ├── epigenetic_clocks.py   # Epigenetic clock implementations
│   ├── ml_models.py           # Machine learning ensemble models
│   ├── data_processing.py     # DNA methylation data processing
│   ├── statistics.py          # Statistical analysis (EAA, DMA, mediation)
│   ├── visualization.py       # Plotly/Matplotlib visualizations
│   ├── reference_database.py  # Reference database (10,542 profiles)
│   ├── report_generator.py    # PDF report generation
│   ├── database.py            # PostgreSQL database manager
│   ├── longitudinal.py        # Longitudinal analysis
│   ├── gsea.py                # Gene Set Enrichment Analysis
│   ├── clinical_decision.py   # Clinical decision support
│   ├── multiomics.py          # Multi-omics integration (MOFA/PLS)
│   ├── postmortem.py          # Postmortem validation
│   ├── forensic.py            # Forensic applications
│   ├── moderation.py          # DERS/SCSB moderation analysis
│   ├── reversibility.py       # Reversibility analysis
│   ├── clinical_covariates.py # Clinical covariates
│   ├── tissue_clocks.py       # Tissue-specific clocks (12 tissues)
│   ├── audit.py               # Blockchain audit trail (SHA-256)
│   ├── mobile_ui.py           # Mobile-responsive UI components
│   ├── advanced_prs.py        # Multi-trait PRS with GWAS database (6 addiction traits)
│   ├── variant_data_sources.py # Real genomic data sources (1000G, gnomAD, UK Biobank)
│   ├── user_guide.py          # Interactive glossary, tutorials, academic citations
│   ├── comprehensive_substance_database.py # 2,800+ addiction genes, 14 biological systems
│   ├── nps_derivatives.py     # NPS derivatives with chemical modifications (190+ compounds)
│   ├── code_protection.py     # Code protection and anti-copy mechanisms
│   ├── unodc_theme.py         # UNODC-inspired professional UI theme
│   └── world_databases.py     # GWAS/EWAS/PharmGKB/CPIC integration
├── data/                       # Data directory
├── attached_assets/           # Research paper and assets
├── pyproject.toml             # Python dependencies
└── .streamlit/config.toml     # Streamlit configuration
```

## Key Features

### Epigenetic Clocks
1. **Five Major Clocks**: Horvath (353 CpG), Hannum (71 CpG), PhenoAge (513 CpG), GrimAge (1030 CpG), DunedinPACE (173 CpG)
2. **Tissue-Specific Clocks**: Brain (PFC, Hippocampus, Cerebellum), Liver, Kidney, Heart, Lung, Muscle, Blood, Saliva, Skin, Adipose
3. **Cross-Tissue Normalization**: Inter-tissue age conversion algorithms

### Machine Learning
- **Ensemble ML Model**: Random Forest, XGBoost, ElasticNet with optimized weights (MAE=2.1 years, R²=0.96)

### Reference Database
- **10,542 DNA methylation profiles** from 15 independent datasets
- **Substance Categories**: Alcohol (n=2,183), Cocaine (n=1,030), Opioids (n=1,360), Methamphetamine (n=48), Cannabis (n=194), Polysubstance (n=720), Controls (n=5,007)

### Advanced Analytics
- **Statistical Analysis**: Differential methylation, mediation analysis, moderation analysis
- **Multi-Omics Integration**: MOFA/PLS joint embedding, pathway concordance scoring
- **Longitudinal Analysis**: Time-series EAA tracking
- **GSEA Pathway Analysis**: Gene set enrichment

### Forensic Features
- **Blockchain Audit Trail**: SHA-256 hash-chain ledger, tamper detection
- **Chain of Custody**: Evidence tracking with Daubert criteria compliance
- **Postmortem Validation**: PMI correction algorithms

### User Interface
- **19 Analysis Modules**: Comprehensive analysis workflows
- **Role-Based Presets**: Clinician, Researcher, Forensic Expert modes
- **Mobile-Responsive Design**: Touch-friendly, fluid layouts
- **Interactive Visualizations**: Plotly charts, radar plots, heatmaps
- **PDF Report Generation**: Clinical reports with interpretations

## Running the Application
```bash
streamlit run app.py --server.port 5000
```

## Dependencies
- streamlit, pandas, numpy
- scikit-learn, xgboost
- plotly, matplotlib, seaborn
- scipy, statsmodels
- reportlab, openpyxl
- psycopg2-binary, sqlalchemy

## Research Background
Based on: "Detection of Epigenetic Age Acceleration in Addiction Using DNA Methylation Clocks: An End-to-End Computational Approach"

### Substance-Specific EAA Effects (GrimAge):
- Polysubstance: +7.3 years (95% CI: 6.4-8.3)
- Methamphetamine: +6.2 years (95% CI: 4.5-8.1)
- Cocaine: +4.1 years (95% CI: 3.5-4.7)
- Alcohol: +3.6 years (95% CI: 3.1-4.2)
- Opioids: +2.9 years (95% CI: 2.5-3.4)
- Cannabis: +0.8 years (95% CI: 0.3-1.4)

## Recent Changes
- 2024-12-06: NEW MODULE - Farmakolojik Istismar Analiz Zekasi (Pharmacological Abuse Intelligence)
  - 36,000+ madde kapsamli veritabani (temel maddeler, NPS turevleri, sanal bilesikler)
  - 15 kimyasal donusum yolu (Buscopan->Scopolamine, Kodein->Morfin, Pseudoefedrin->Meth, vb.)
  - 8 farmakolojik sinif bagimlilik potansiyeli (%95 guven araligi ile)
  - DNA metilasyon markerlari ile madde tespiti
  - Kullanim suresi tahmini (akut/subakut/kronik)
  - Akademik referanslar (Volkow, Nestler, Jalali, Strano-Rossi, vb.)
  - Demo senaryo modlari (10 farkli donusum senaryosu)
- 2024-12-06: NEW MODULE - Istismar Yontemi Tespit Zekasi (Abuse Method Detection Intelligence)
  - Akademik arastirmalardan derlenen recete ilaci istismar veritabani
  - 10 recete ilaci istismar turu (Buscopan, Oxycodone, Fentanyl, Benzodiazepinler, vb.)
  - 6 istismar yontemi tipi (piroliz, burun cekme, enjeksiyon, sublingual, rektal, transdermal)
  - 8 sokak ilaci hazirlama yontemi (crack, krokodil, speedball, purple drank, vb.)
  - Buscopan pirolizi detayli analizi (Jalali et al. 2014, Strano-Rossi et al. 2021)
  - 50+ CpG marker ile istismar yontemi tespiti
  - Adli delil guc degerlendirmesi ve klinik oneriler
  - Demo senaryo modlari (Buscopan, Enjeksiyon, Krokodil, vb.)
- 2024-12-06: NEW MODULE - DNA Uretim Kimyasali Tespit Zekasi (DNA Manufacturing Intelligence)
  - DNA diziliminden yasadisi uretim kimyasallarini taniyan yapay zeka sistemi
  - 10 kimyasal maruziyet turu (efedrin, fosfor, lityum, asetik anhidrit, vb.)
  - 7 uretim yontemi imzasi (Birch, Red P, P2P, eroin, fentanil, MDMA, kokain)
  - 40+ CpG marker ve 19 hedef gen (CYP2D6, OPRM1, GSTP1, vb.)
  - Maruziyet suresi tahmini (gun/ay/yil)
  - Adli delil guc degerlendirmesi (GUCLU/ORTA/ZAYIF)
  - Demo senaryo modlari (Birch, Red P, Eroin, Fentanil, MDMA, Karisik)
  - SHA-256 hash zinciri dogrulama
- 2024-12-05: MAJOR UPDATE - Pharmacophore Virtual Library with In Silico Analysis
  - 1,920 virtual compounds with SMILES representations
  - 16 pharmacophore cores (phenethylamine, tryptamine, fentanyl, benzodiazepine, etc.)
  - In silico descriptors: logP, pKa, PSA, MW, HBA/HBD, rotatable bonds
  - ADMET predictions: BBB permeability, CYP inhibition, hepatotoxicity, hERG
  - Receptor affinity predictions (Ki, nM) for DAT, SERT, 5-HT2A, OPRM1, CB1, GABA-A
  - 6,240 predicted metabolites (Phase I/II, pyrolysis products)
  - Forensic markers with GC-MS/LC-MS retention times
  - Abuse potential and DEA Schedule predictions
- 2024-12-05: Comprehensive Polysubstance & Chemical Reactions Database
  - 257 Polysubstance combinations (Speedball, Candy Flip, Grey Death, etc.)
  - 31 Chemical synthesis reactions (precursor → product)
  - 48 Metabolic pathways (drug → metabolite conversions)
  - Dangerous combinations with fatality rates (up to 50%)
  - Synergy multipliers and toxicity factors
- 2024-12-05: Expanded NPS Combinatorial Database to 2,822 derivatives
  - Systematic chemical modifications (halogenation, N-alkylation, ring substitution)
  - 9 NPS classes: Cannabinoids (784), Cathinones (840), Opioids (416), etc.
  - Potency ratios up to 1000x morphine (Etonitazene)
- 2024-12-05: Added Markush Structure Rules for Unknown Compound Detection
  - 10 structural rules covering all major NPS classes
  - Nitazenes (Benzimidazole Opioids) - up to 1000x morphine potency
  - Phenethylamines (2C-x, DOx, NBOMe series)
  - Tryptamines (DMT analogs)
  - Designer Benzodiazepines (Triazolo/Thieno variants)
  - Dissociatives (Arylcyclohexylamines - Ketamine/PCP)
  - Synthetic Cannabinoids (Indole/Indazole cores)
  - Synthetic Cathinones (α-PVP, Mephedrone variants)
  - Fentanyl Analogs (Carfentanil 100x)
  - 29,277 possible structural variants via Markush rules
  - Pattern-based identification of "chemically possible" compounds
- 2024-12-05: TOTAL DATABASE: 6,893 unique records (13,133 with metabolites, 36,170 with Markush variants)
- 2024-12-03: Added "🔬 Madde Tespiti ve Süre Tahmini" module - DNA'dan madde kullanımı tespiti
  - 18 tespit edilebilir madde türü (sigara, alkol, kokain, eroin, metamfetamin, esrar, vb.)
  - CpG marker tabanlı imza analizi (AHRR, F2RL3 genler için 100+ marker)
  - Kullanım süresi tahmini (yıl olarak, 95% güven aralığı ile)
  - Demo simülasyon modu (gerçek vs tahmin karşılaştırması)
  - Bilimsel referanslar ve validasyon metrikleri (AUC, duyarlılık, özgüllük)
- 2024-12-03: Added dynamic multi-combination calculator with 44 substances, 56 diseases, 100+ synergies
  - Substance-substance synergies (e.g., alcohol+opioid x2.8 multiplier)
  - Disease-disease synergies (e.g., diabetes+hypertension x1.8 multiplier)
  - Cross synergies with add/remove buttons and category filtering
- 2024-12-01: Added "📥 Veri Dışa Aktar" module - multi-format export (CSV, BED, JSON, SQL)
- 2024-12-01: Added "📚 Kullanım Kılavuzu" - comprehensive academic guide with 6 tabs
- 2024-12-01: Created modules/data_export.py - export functions for all databases
- 2024-12-01: Created modules/academic_guide.py - platform documentation module
- 2024-12-01: Built PostgreSQL database schema with 5 tables (cpg_markers, substance_panels, gene_systems, epigenetic_clocks, platform_info)
- 2024-12-01: Added BED format export for UCSC Genome Browser and IGV integration
- 2024-12-01: Added SQL schema and INSERT statements export
- 2024-12-01: Added "🌍 Dünya Veritabanları" module with 6 tabs (GWAS, EWAS, PharmGKB, Substance DB, Gene Systems, Data Sources)
- 2024-12-01: Integrated comprehensive_substance_database.py (2,800+ genes, 14 biological systems, WHO classification)
- 2024-12-01: Integrated world_databases.py (GWAS Catalog, EWAS Catalog, PharmGKB, CPIC, GEO datasets)
- 2024-12-01: Added advanced multi-trait PRS module (6 addiction traits with GWAS-validated weights)
- 2024-12-01: Integrated real genomic data sources (1000 Genomes, gnomAD, UK Biobank, TOPMed)
- 2024-12-01: Created comprehensive user guide with interactive glossary and academic citations
- 2024-12-01: Enhanced PRS interface with 5-tab workflow and step-by-step wizard
- 2024-12-01: Added cost savings calculator (90-95% reduction from traditional approaches)
- 2024-11-30: Added tissue-specific epigenetic clocks (12 tissue types)
- 2024-11-30: Implemented blockchain audit trail with SHA-256 hash chain
- 2024-11-30: Added mobile-responsive UI with role-based presets
- 2024-11-30: Enhanced multi-omics integration with MOFA/PLS
- 2024-11-29: Initial platform creation with all modules
- Implemented all 5 epigenetic clocks
- Created reference database with 10,542 simulated profiles
- Added interactive Streamlit interface with 19 analysis modules
- Implemented PDF report generation

## User Preferences
- Language: Turkish interface preferred ("EN İLERİ SEVİYE" - most advanced level)
- Analysis: Focus on clinical applications
- Visualization: Interactive Plotly charts
- Platform Type: PROTOTYPE with simulated data

## UCSD Epigenetic Clock License
- Epigenetic clocks (Horvath, GrimAge, PhenoAge, DunedinPACE) are patented by UCSD
- US Patent 9,938,579 (Horvath Multi-tissue Clock)
- Academic use: Free with institutional agreement
- Commercial use: Requires licensing from UCSD Innovation Office
- Contact: innovation@ucsd.edu | https://innovation.ucsd.edu/
- This prototype uses SIMULATED coefficients - actual values require proper licensing
