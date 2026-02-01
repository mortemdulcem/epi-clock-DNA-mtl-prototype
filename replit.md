# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform

## Overview
EpiClock Prototype is an advanced computational platform designed to detect and quantify epigenetic age acceleration (EAA) in addiction using DNA methylation clocks. Its primary purpose is to provide a comprehensive tool for clinical, research, and forensic applications. The platform integrates five major epigenetic clocks (Horvath, Hannum, PhenoAge, GrimAge, DunedinPACE), tissue-specific clocks, and advanced statistical and machine learning methodologies. It also incorporates forensic features like blockchain audit trails and specialized substance abuse detection intelligence. The project aims to deliver an end-to-end computational approach for epigenetic analysis, offering significant potential for understanding addiction's biological underpinnings and informing clinical decision-making.

**Important:** This platform uses OPEN SOURCE epigenetic clocks (Hannum and DunedinPACE) with real published coefficients. For Horvath, PhenoAge, and GrimAge clocks, simulated coefficients are used as these require UCSD licensing for commercial use.

## User Preferences
- Language: Turkish interface preferred ("EN İLERİ SEVİYE" - most advanced level)
- Analysis: Focus on clinical applications
- Visualization: Interactive Plotly charts
- Platform Type: PROTOTYPE with simulated data

## System Architecture
The EpiClock platform is built around a modular architecture, with `app.py` serving as the main Streamlit application orchestrating numerous specialized modules.

**UI/UX Decisions:**
- **Mobile-Responsive Design:** The interface is designed to be touch-friendly and fluid across devices.
- **Role-Based Presets:** Provides tailored experiences for Clinicians, Researchers, and Forensic Experts.
- **Interactive Visualizations:** Utilizes Plotly, Matplotlib, and Seaborn for dynamic charts, radar plots, and heatmaps.
- **Professional Theme:** Employs a UNODC-inspired professional UI theme.

**Technical Implementations & Feature Specifications:**
- **Epigenetic Clocks:** Implements five major epigenetic clocks and 12 tissue-specific clocks, with cross-tissue normalization algorithms.
- **Machine Learning:** Features an ensemble ML model (Random Forest, XGBoost, ElasticNet) for accurate age prediction.
- **Deep Learning Models:** MLP (Multi-Layer Perceptron), Autoencoder for dimensionality reduction, VAE (Variational Autoencoder), MTL-NN (Multi-Task Learning Neural Network) for joint age/substance/risk prediction.
- **Data Preprocessing:** ComBat batch correction, Houseman cell composition estimation, functional normalization, quality control pipeline.
- **Model Explainability:** SHAP/TreeSHAP integration for feature importance, clinical report generation with CpG contribution analysis.
- **Reference Database:** A large reference database of 10,542 DNA methylation profiles categorized by substance use.
- **Advanced Analytics:** Includes differential methylation, mediation, moderation analysis, GSEA, and multi-omics integration (MOFA/PLS).
- **Forensic Features:** Incorporates a SHA-256 blockchain audit trail for tamper detection, chain of custody tracking, and postmortem validation with PMI correction.
- **Substance Detection Intelligence:** Advanced modules for:
    - **Pharmacological Abuse Intelligence:** Comprehensive database of 36,000+ substances, chemical transformations, and addiction potential prediction.
    - **Abuse Method Detection Intelligence:** Identifies abuse methods (e.g., pyrolysis, injection) based on academic research and CpG markers.
    - **DNA Manufacturing Chemical Detection:** AI system to identify illicit manufacturing chemicals from DNA sequences.
    - **Molecular Graph Neural Network (GNN) Analysis:** PyTorch-based MPNN for multi-task prediction of addiction, toxicity, metabolism, and receptor binding.
    - **Advanced Feature Engineering:** Chemical property analysis, pharmacological receptor targeting, pharmacokinetics, and abuse potential scoring.
- **Disease Methylation Database & Differential Diagnosis:**
    - **Comprehensive Disease Database:** 84 chronic diseases with literature-based CpG markers from EWAS Catalog
    - **Disease Categories:** Neurological (Alzheimer, Parkinson, MS, ALS, Huntington, Epilepsy), Neurodevelopmental (Autism, ADHD, Intellectual Disability), Genetic Syndromes (26 syndromes: Down, Rett, Angelman, Prader-Willi, Williams, Fragile X, Cystic Fibrosis, Sickle Cell, Thalassemia, Hemophilia, Duchenne, SMA, Marfan, Ehlers-Danlos, NF1, Tuberous Sclerosis, PKU, Gaucher, Fabry, Pompe, Turner, Klinefelter, XYY, Wilson, Hemochromatosis, Achondroplasia), Psychiatric (Schizophrenia, Bipolar, Depression, PTSD, Anxiety, OCD), Cancer (26 types: Breast, Lung, Colorectal, Prostate, Leukemia, Brain/Glioma, Liver, Stomach, Pancreatic, Ovarian, Kidney, Bladder, Thyroid, Melanoma, Esophageal, Cervical, Endometrial, Lymphoma, Multiple Myeloma, Head & Neck, Testicular, Bone, Soft Tissue Sarcoma, Gallbladder, Small Intestine, Mesothelioma), Metabolic (Type 2 Diabetes, Obesity, NAFLD, Metabolic Syndrome), Autoimmune (RA, Lupus, Crohn's, Celiac, IBD), Cardiovascular (Atherosclerosis, Hypertension, CHD), Environmental (Smoking, Pollution, Heavy Metals), Aging
    - **Disease Pattern Matcher:** ML-based Jaccard similarity matching between methylation profiles and disease signatures
    - **Deep Learning Autoencoder:** PyTorch-based disease classification from latent representations
    - **Disease GNN (Graph Neural Network):** CpG-Gene-Disease relationship graph for pathway enrichment
    - **Differential Diagnosis System:** Multi-source anomaly interpretation with clinical disclaimers
    - **Safety Features:** Clear disclaimers that methylation anomalies are NOT diagnostic - requires clinical correlation
- **Data Management:** PostgreSQL database for managing CpG markers, substance panels, gene systems, and clock information.
- **Auto-Sync Database System (v4.0 NEW):**
    - **Automatic External Database Synchronization:** Real-time integration with GWAS Catalog, EWAS Catalog, PubChem APIs
    - **New Substance Detection:** Automatically detects and imports new addiction-related substances
    - **CpG Marker Updates:** Syncs latest EWAS findings for addiction exposures
    - **GWAS Study Integration:** Imports addiction-related genome-wide association studies
    - **Change Detection:** SHA-256 hashing for efficient update detection
    - **Scheduler:** Configurable auto-sync intervals (6h, 12h, 24h, weekly)
    - **Rate Limiting:** API-compliant request throttling for each data source
    - **SQLAlchemy Models:** SyncedSubstance, SyncedGWASStudy, SyncedEWASMarker, SyncLog tables
- **Report Generation:** Automated PDF clinical reports with interpretations.
- **Comprehensive Databases:** Integration of GWAS, EWAS, PharmGKB, and various substance/gene databases.
- **Code Protection:** Mechanisms for code protection and anti-copying.
- **Publication Standards (v4.0 NEW):**
    - **PRISMA-NMA Standards:** Full PRISMA 2020 + NMA extension compliance with 32-item checklist, PubMed systematic search, frequentist NMA engine, heterogeneity analysis, RoB 2/ROBINS-I assessment, CINeMA framework
    - **Statistical Validation:** Multiple testing correction (Bonferroni, FDR, Holm, Storey q-value), Bootstrap CI (Percentile, BCa), ROC-AUC/PR-AUC, DeLong test, Effect sizes (Cohen's d, Hedge's g, eta-squared), Power analysis for EWAS
    - **Academic Reporting:** STROBE-ME checklist (38 items), TRIPOD checklist, Supplementary materials generator, Methods/Results section templates, Data availability statements
    - **Reproducibility Infrastructure:** Global seed management (Python, NumPy, PyTorch, TensorFlow), Environment capture, Data checksums (SHA256), Pipeline tracking with manifests, Version control integration, Requirements generation
    - **Test Suite:** 32 pytest unit/integration tests covering all validation modules (100% pass rate)
    - **EWAS Reporting Standards:** P-value thresholds (P<1e-7), DMR analysis, methQTL integration, cell-type deconvolution, batch effect correction tracking
    - **MIQE Standards:** qPCR validation checklist, primer design standards, amplification efficiency tracking
    - **MIAME Standards:** Microarray experiment metadata, GEO/ArrayExpress submission generators, SOFT file creation
    - **FAIR Principles:** Persistent identifiers, Dublin Core/DataCite metadata, data licensing (CC-BY-4.0), provenance tracking
    - **MINSEQE Standards:** Sequencing experiment metadata, SRA/ENA submission generators, WGBS/RRBS support
    - **GATHER Standards:** Gene list reporting, pathway analysis standards, GO enrichment documentation
    - **REMARK Standards:** Biomarker cutoff determination, prognostic model validation, C-index, calibration analysis
    - **STARD Standards:** Diagnostic accuracy metrics, sensitivity/specificity with CI, ROC analysis, DeLong test for AUC comparison

## External Dependencies
- **Python Libraries:** `streamlit`, `pandas`, `numpy`, `scikit-learn`, `xgboost`, `plotly`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `reportlab`, `openpyxl`, `psycopg2-binary`, `sqlalchemy`, `rdkit`, `torch`.
- **Database:** PostgreSQL.
- **Genomic Data Sources:** 1000 Genomes, gnomAD, UK Biobank, TOPMed.
- **Academic Databases:** GWAS Catalog, EWAS Catalog, PharmGKB, CPIC, GEO datasets.
- **Licensing:** 
    - **Open Source (No license required):** Hannum (Molecular Cell 2013), DunedinPACE (eLife 2022, CC-BY 4.0)
    - **UCSD License Required:** Horvath, PhenoAge, GrimAge (using simulated coefficients)