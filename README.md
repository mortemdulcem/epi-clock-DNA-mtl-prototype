# 🧬 EpiClock Prototype

## DNA Methylation-Based Epigenetic Age Acceleration Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

---

## ⚠️ PROTOTYPE DISCLAIMER

**This is a PROTOTYPE/DEMONSTRATION platform** that uses **SIMULATED DATA** to demonstrate the analytical workflow and methodology for epigenetic age acceleration analysis in substance dependence.

- Epigenetic clock coefficients are simulated based on published research statistics
- Reference database contains synthetic profiles generated from meta-analysis statistics
- For research or clinical use, obtain actual coefficients through proper academic channels

---

## 🎯 Overview

EpiClock Prototype is an advanced computational platform for detecting and quantifying epigenetic age acceleration (EAA) in addiction using DNA methylation clocks. The platform implements cutting-edge analytical methods suitable for clinical research and forensic applications.

### Key Features

#### 🧪 Epigenetic Clocks (5 Major Clocks)
- **Horvath Clock** (353 CpG sites) - Multi-tissue age predictor
- **Hannum Clock** (71 CpG sites) - Blood-based age predictor
- **PhenoAge** (513 CpG sites) - Mortality-calibrated age predictor
- **GrimAge** (1030 CpG sites) - Mortality risk predictor
- **DunedinPACE** (173 CpG sites) - Pace of aging predictor

#### 🫀 Tissue-Specific Clocks (12 Tissues)
- Brain regions: Prefrontal Cortex, Hippocampus, Cerebellum
- Organs: Heart, Lung, Liver, Kidney, Muscle
- Other: Blood, Saliva, Skin, Adipose

#### 🔐 Forensic Features
- Blockchain audit trail with SHA-256 hash chain
- Chain of custody tracking
- Daubert criteria compliance
- Postmortem validation algorithms

#### 📊 Advanced Analytics
- Ensemble ML model (Random Forest, XGBoost, ElasticNet)
- Multi-omics integration (MOFA/PLS)
- GSEA pathway analysis
- Mediation and moderation analysis
- Longitudinal EAA tracking

---

## 📈 Research Background

Based on: *"Detection of Epigenetic Age Acceleration in Addiction Using DNA Methylation Clocks: An End-to-End Computational Approach"*

### Substance-Specific EAA Effects (GrimAge Clock)

| Substance | EAA (years) | 95% CI |
|-----------|-------------|--------|
| Polysubstance | +7.3 | 6.4 - 8.3 |
| Methamphetamine | +6.2 | 4.5 - 8.1 |
| Cocaine | +4.1 | 3.5 - 4.7 |
| Alcohol | +3.6 | 3.1 - 4.2 |
| Opioids | +2.9 | 2.5 - 3.4 |
| Cannabis | +0.8 | 0.3 - 1.4 |

### Reference Database
- **10,542** DNA methylation profiles
- **15** independent datasets
- **6** substance categories + controls

---

## 🚀 Installation

### Requirements

```bash
python >= 3.11
streamlit >= 1.28
```

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/epiclock-prototype.git
cd epiclock-prototype

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py --server.port 5000
```

---

## 📁 Project Structure

```
epiclock-prototype/
├── app.py                      # Main Streamlit application
├── modules/                    # Core analysis modules
│   ├── epigenetic_clocks.py   # Epigenetic clock implementations
│   ├── ml_models.py           # Machine learning ensemble
│   ├── data_processing.py     # DNA methylation data processing
│   ├── statistics.py          # Statistical analysis
│   ├── visualization.py       # Plotly/Matplotlib visualizations
│   ├── reference_database.py  # Reference database
│   ├── tissue_clocks.py       # Tissue-specific clocks
│   ├── audit.py               # Blockchain audit trail
│   ├── multiomics.py          # Multi-omics integration
│   └── ...                    # Additional modules
├── data/                       # Data directory
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🔬 Analysis Modules

1. **Individual Analysis** - Single sample epigenetic age calculation
2. **Batch Analysis** - Multi-sample processing
3. **Reference Database** - Population comparison
4. **Differential Methylation** - CpG-level analysis
5. **Mediation Analysis** - Mechanistic pathways
6. **Model Performance** - Validation metrics
7. **Longitudinal Tracking** - Time-series analysis
8. **GSEA Pathway Analysis** - Biological enrichment
9. **Clinical Decision Support** - Treatment recommendations
10. **Multi-Omics Integration** - Cross-platform analysis
11. **Postmortem Validation** - Forensic applications
12. **Tissue-Specific Clocks** - Multi-tissue analysis
13. **Blockchain Audit** - Forensic chain of custody

---

## 📜 License

This project is provided for **academic and research purposes only**.

For clinical applications, please ensure compliance with:
- Institutional Review Board (IRB) requirements
- Data privacy regulations (HIPAA, GDPR)
- Professional licensing requirements

---

## 👨‍🔬 Author

**Academic Credentials:**
- Forensic Medicine, Ph.D., M.D.
- Software Engineering, M.Sc.
- Health Law, J.D., M.D.

---

## 📚 Citations

If you use this platform in your research, please cite the underlying methodology:

```bibtex
@article{epiclock2024,
  title={Detection of Epigenetic Age Acceleration in Addiction 
         Using DNA Methylation Clocks: An End-to-End Computational Approach},
  year={2024},
  note={Prototype demonstration platform}
}
```

---

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

---

*This platform demonstrates the complete analytical architecture and can integrate real coefficients and data when obtained through proper licensing channels.*
