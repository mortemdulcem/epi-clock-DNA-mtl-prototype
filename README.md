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

## 👩‍🔬 Author

<div align="center">

### **Dr. Nurcan Denli Bayır**

<img src="https://img.shields.io/badge/Forensic%20Medicine-Ph.D.%20%7C%20M.D.-darkred?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQxIDAtOC0zLjU5LTgtOHMzLjU5LTggOC04IDggMy41OSA4IDgtMy41OSA4LTggOHoiLz48L3N2Zz4=" alt="Forensic Medicine"/>
<img src="https://img.shields.io/badge/Software%20Engineering-M.Sc.-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik05LjQgMTYuNkw0LjggMTJsNC42LTQuNkw4IDZsLTYgNiA2IDYgMS40LTEuNHptNS4yIDBsNC42LTQuNi00LjYtNC42TDE2IDZsNiA2LTYgNi0xLjQtMS40eiIvPjwvc3ZnPg==" alt="Software Engineering"/>
<img src="https://img.shields.io/badge/Health%20Law-J.D.%20%7C%20M.D.-darkgreen?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAxTDMgNXY2YzAgNS41NSAzLjg0IDEwLjc0IDkgMTIgNS4xNi0xLjI2IDktNi40NSA5LTEyVjVsLTktNHoiLz48L3N2Zz4=" alt="Health Law"/>

</div>

---

#### 🎓 Academic Credentials

| Degree | Field | Specialization |
|--------|-------|----------------|
| **Ph.D., M.D.** | Forensic Medicine | Molecular Forensics & Epigenetics |
| **M.Sc.** | Software Engineering | Computational Biology & Bioinformatics |
| **J.D., M.D.** | Health Law | Medical Jurisprudence & Bioethics |

---

#### 🏛️ Professional Affiliations

- **Smart University** - Faculty of Medicine, Department of Forensic Medicine
- **Computational Forensics & Epigenetics Research Laboratory** - Principal Investigator
- **International Association of Forensic Sciences** - Member
- **European Society of Legal Medicine** - Member

---

#### 🔬 Research Focus Areas

| Domain | Expertise |
|--------|-----------|
| **Epigenetic Chronology** | DNA Methylation Clock Development & Validation |
| **Forensic Molecular Biology** | Postmortem Interval Estimation, Tissue-Specific Biomarkers |
| **Computational Forensics** | Machine Learning in Forensic Medicine, Multi-omics Integration |
| **Addiction Epigenetics** | Substance-Induced Biological Aging, EAA Quantification |
| **Legal Medicine** | Expert Witness Testimony, Daubert Standard Compliance |

---

#### 📫 Contact & Profiles

[![GitHub](https://img.shields.io/badge/GitHub-mortemdulcem-181717?style=flat-square&logo=github)](https://github.com/mortemdulcem)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Profile-00CCBB?style=flat-square&logo=researchgate)](https://researchgate.net)
[![ORCID](https://img.shields.io/badge/ORCID-Researcher-A6CE39?style=flat-square&logo=orcid)](https://orcid.org)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Citations-4285F4?style=flat-square&logo=googlescholar)](https://scholar.google.com)

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

---

<div align="center">

---

## 🧬 EpiClock Prototype

<img src="https://img.shields.io/badge/Version-1.0.0-brightgreen?style=for-the-badge" alt="Version"/>
<img src="https://img.shields.io/badge/Status-Active%20Development-blue?style=for-the-badge" alt="Status"/>
<img src="https://img.shields.io/badge/License-Academic-orange?style=for-the-badge" alt="License"/>

---

### Developed by

# **Dr. Nurcan Denli Bayır**

<table>
<tr>
<td align="center"><img src="https://img.shields.io/badge/🔬-Forensic%20Medicine-darkred?style=flat-square" alt=""/><br/><b>Ph.D., M.D.</b></td>
<td align="center"><img src="https://img.shields.io/badge/💻-Software%20Engineering-blue?style=flat-square" alt=""/><br/><b>M.Sc.</b></td>
<td align="center"><img src="https://img.shields.io/badge/⚖️-Health%20Law-darkgreen?style=flat-square" alt=""/><br/><b>J.D., M.D.</b></td>
</tr>
</table>

---

**Smart University - Faculty of Medicine**

*Department of Forensic Medicine*

**Computational Forensics & Epigenetics Research Laboratory**

*Principal Investigator*

---

> *"Advancing forensic science through computational epigenetics and molecular chronology"*

---

<img src="https://img.shields.io/badge/🧬-DNA%20Methylation-purple?style=flat-square" alt=""/>
<img src="https://img.shields.io/badge/🔐-Blockchain%20Forensics-black?style=flat-square" alt=""/>
<img src="https://img.shields.io/badge/🤖-Machine%20Learning-orange?style=flat-square" alt=""/>
<img src="https://img.shields.io/badge/⚗️-Epigenetic%20Clocks-teal?style=flat-square" alt=""/>

---

[![GitHub](https://img.shields.io/badge/GitHub-mortemdulcem-181717?style=for-the-badge&logo=github)](https://github.com/mortemdulcem)
[![Repository](https://img.shields.io/badge/Repository-EpiClock%20Prototype-blue?style=for-the-badge&logo=github)](https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype)

---

**© 2024 Dr. Nurcan Denli Bayır. All Rights Reserved.**

*For academic and research purposes only.*

---

<sub>
<i>This platform represents the integration of forensic medicine, computational biology, and legal medicine 
in the pursuit of understanding epigenetic age acceleration in substance dependence.</i>
</sub>

</div>
