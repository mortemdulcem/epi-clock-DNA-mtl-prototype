# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform

## Overview
EpiClock Prototype is an advanced computational platform designed to detect and quantify epigenetic age acceleration (EAA) in addiction using DNA methylation clocks. Its primary purpose is to provide a comprehensive tool for clinical, research, and forensic applications. The platform integrates five major epigenetic clocks (Horvath, Hannum, PhenoAge, GrimAge, DunedinPACE), tissue-specific clocks, and advanced statistical and machine learning methodologies. It also incorporates forensic features like blockchain audit trails and specialized substance abuse detection intelligence. The project aims to deliver an end-to-end computational approach for epigenetic analysis, offering significant potential for understanding addiction's biological underpinnings and informing clinical decision-making.

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
- **Epigenetic Clocks:** Implements five major epigenetic clocks and 12 tissue-specific clocks, with cross-tissue normalization algorithms. For Horvath, PhenoAge, and GrimAge clocks, simulated coefficients are used as these require UCSD licensing for commercial use.
- **Machine Learning:** Features an ensemble ML model (Random Forest, XGBoost, ElasticNet) for accurate age prediction, alongside Deep Learning Models (MLP, Autoencoder, VAE, MTL-NN) for advanced predictions and dimensionality reduction.
- **Data Preprocessing:** Includes ComBat batch correction, Houseman cell composition estimation, functional normalization, and a quality control pipeline.
- **Model Explainability:** SHAP/TreeSHAP integration for feature importance, and clinical report generation with CpG contribution analysis.
- **Reference Database:** A large reference database of DNA methylation profiles categorized by substance use.
- **Advanced Analytics:** Includes differential methylation, mediation, moderation analysis, GSEA, and multi-omics integration (MOFA/PLS).
- **Forensic Features:** Incorporates a SHA-256 blockchain audit trail for tamper detection, chain of custody tracking, and postmortem validation with PMI correction.
- **Substance Detection Intelligence:** Advanced modules for:
    - **Pharmacological Abuse Intelligence:** Comprehensive database of substances, chemical transformations, and addiction potential prediction.
    - **Abuse Method Detection Intelligence:** Identifies abuse methods based on academic research and CpG markers.
    - **DNA Manufacturing Chemical Detection:** AI system to identify illicit manufacturing chemicals from DNA sequences.
    - **Molecular Graph Neural Network (GNN) Analysis:** PyTorch-based MPNN for multi-task prediction of addiction, toxicity, metabolism, and receptor binding.
    - **Advanced Feature Engineering:** Chemical property analysis, pharmacological receptor targeting, pharmacokinetics, and abuse potential scoring.
- **Disease Methylation Database & Differential Diagnosis:**
    - **Comprehensive Disease Database:** 207 chronic diseases with literature-based CpG markers from EWAS Catalog across various categories (Neurological, Psychiatric, Endocrine, Renal, Hematological, Neurodevelopmental, Genetic Syndromes, Cancer, Metabolic, Autoimmune, Cardiovascular, Environmental, Aging).
    - **Disease Pattern Matcher:** ML-based Jaccard similarity matching between methylation profiles and disease signatures.
    - **Deep Learning Autoencoder:** PyTorch-based disease classification from latent representations.
    - **Disease GNN (Graph Neural Network):** CpG-Gene-Disease relationship graph for pathway enrichment.
    - **Differential Diagnosis System:** Multi-source anomaly interpretation with clinical disclaimers.
    - **Safety Features:** Clear disclaimers that methylation anomalies are NOT diagnostic and require clinical correlation.
- **Data Management:** PostgreSQL database for managing CpG markers, substance panels, gene systems, and clock information.
- **Auto-Sync Database System:** Real-time integration with external APIs (GWAS Catalog, EWAS Catalog, PubChem) for automatic synchronization of new substances, CpG marker updates, and addiction-related GWAS studies. Features include change detection, configurable scheduling, and API-compliant rate limiting.
- **Report Generation:** Automated PDF clinical reports with interpretations.
- **Comprehensive Databases:** Integration of GWAS, EWAS, PharmGKB, and various substance/gene databases.
- **Publication Standards:** Compliance with PRISMA-NMA, STROBE-ME, TRIPOD, MIQE, MIAME, FAIR, MINSEQE, GATHER, and REMARK standards for academic reporting and reproducibility. Includes statistical validation methods, reproducibility infrastructure, and a comprehensive test suite.

## External Dependencies
- **Python Libraries:** `streamlit`, `pandas`, `numpy`, `scikit-learn`, `xgboost`, `plotly`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `reportlab`, `openpyxl`, `psycopg2-binary`, `sqlalchemy`, `rdkit`, `torch`.
- **Database:** PostgreSQL.
- **Genomic Data Sources:** 1000 Genomes, gnomAD, UK Biobank, TOPMed.
- **Academic Databases:** GWAS Catalog, EWAS Catalog, PharmGKB, CPIC, GEO datasets.
- **Licensing:** Uses OPEN SOURCE epigenetic clocks (Hannum and DunedinPACE) with real published coefficients. Horvath, PhenoAge, and GrimAge clocks use simulated coefficients due to UCSD licensing requirements for commercial use.