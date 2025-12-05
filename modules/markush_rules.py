"""
================================================================================
EpiClock Prototype v4.0 - Markush Structure Rules & Pattern Recognition Engine
================================================================================
Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır
Digital Signature: nrcdnl94
ALL RIGHTS RESERVED - PROPRIETARY AND CONFIDENTIAL

MARKUSH YAPILARI VE YAPISAL KURAL TABANLI TANIMLAMA
============================================================================
Bu modül, bilinen maddeleri değil "kimyasal olarak mümkün olan" TÜM
kombinasyonları tanımlamak için Markush yapı kuralları kullanır.

Ana Sınıflar:
1. Nitazenler (Benzimidazol Opioidler) - En Yüksek Risk
2. Fenetiilaminler (2C-x, DOx, NBOMe Serisi)
3. Triptaminler (DMT ve Analogları)
4. Tasarımcı Benzodiazepinler
5. Disosiyatifler (Arilsikloheksilaminler)
6. Sentetik Kannabinoidler
7. Sentetik Katinonlar
8. Fentanil Analogları

Patent Literature'dan Markush Yapı Tanımları:
- IUPAC Nomenclature Guidelines
- USPTO Patent Chemical Notation
- EPO Markush Structure Guidelines
================================================================================
"""

# nrcdnl94 - Author Signature

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set, Callable
from enum import Enum
import re
import numpy as np
from itertools import product

# nrcdnl94
class RiskLevel(Enum):
    """Risk Seviyeleri"""
    UNKNOWN = "Bilinmeyen"
    LOW = "Düşük"
    MODERATE = "Orta"
    HIGH = "Yüksek"
    VERY_HIGH = "Çok Yüksek"
    EXTREME = "Aşırı (Ölümcül)"

class StructureClass(Enum):
    """Yapısal Sınıflar"""
    NITAZENE = "Nitazen (Benzimidazol Opioid)"
    PHENETHYLAMINE_2C = "Fenetilamin 2C Serisi"
    PHENETHYLAMINE_DOX = "Fenetilamin DOx Serisi"
    PHENETHYLAMINE_NBOME = "Fenetilamin NBOMe Serisi"
    TRYPTAMINE = "Triptamin"
    BENZODIAZEPINE_DESIGNER = "Tasarımcı Benzodiazepin"
    DISSOCIATIVE_ACH = "Disosiyatif (Arilsiklohekzilamin)"
    SYNTHETIC_CANNABINOID = "Sentetik Kannabinoid"
    SYNTHETIC_CATHINONE = "Sentetik Katinon"
    FENTANYL_ANALOG = "Fentanil Analoğu"
    UNKNOWN_NPS = "Bilinmeyen NPS"

@dataclass
# nrcdnl94
class MarkushRule:
    """Markush Yapı Kuralı Tanımı"""
    rule_id: str
    rule_name: str
    structure_class: StructureClass
    core_scaffold: str
    core_smarts: str  # SMARTS pattern
    required_groups: List[Dict]  # Zorunlu gruplar
    variable_positions: List[Dict]  # Değişken pozisyonlar
    excluded_combinations: List[str]  # İzin verilmeyen kombinasyonlar
    potency_modifiers: Dict[str, float]  # Potens değiştiriciler
    risk_level: RiskLevel
    detection_notes: str
    forensic_markers: List[str]

@dataclass
# nrcdnl94
class StructuralMatch:
    """Yapısal Eşleşme Sonucu"""
    matched: bool
    structure_class: StructureClass
    matched_rule: str
    core_scaffold: str
    identified_substituents: List[str]
    potency_estimate: float
    risk_level: RiskLevel
    confidence: float
    warnings: List[str]
    recommended_tests: List[str]


# ============================================================================
# MARKUSH KURAL TANIMLARI - YAPISAL İSKELETLER
# ============================================================================

MARKUSH_RULES: Dict[str, MarkushRule] = {}

# ============================================================================
# 1. NİTAZENLER (BENZİMİDAZOL OPİOİDLER) - EN YÜKSEK RİSK
# ============================================================================

MARKUSH_RULES["NITAZENE_CORE"] = MarkushRule(
    rule_id="NITAZENE_CORE",
    rule_name="Nitazen (Benzimidazol Opioid) Ana Kuralı",
    structure_class=StructureClass.NITAZENE,
    core_scaffold="Benzimidazol halkası + Dietilaminoetil yan zinciri",
    core_smarts="[nH]1cnc2ccccc12",  # Benzimidazol SMARTS
    required_groups=[
        {"position": "5", "group": "NO2", "description": "Nitro grubu (aktivite için kritik)", "required": True},
        {"position": "N1", "group": "CH2CH2N(Et)2", "description": "Dietilaminoetil", "required": True}
    ],
    variable_positions=[
        {
            "position": "benzyl_para",
            "allowed_groups": ["H", "OCH3", "OC2H5", "OCH(CH3)2", "OC3H7", "OC4H9", "F", "Cl", "Br", "CH3", "C2H5"],
            "potency_effect": {"OCH(CH3)2": 10.0, "OC2H5": 5.0, "OCH3": 2.0, "H": 1.0}
        },
        {
            "position": "5",
            "allowed_groups": ["NO2", "CN", "Cl", "F"],
            "potency_effect": {"NO2": 1.0, "CN": 0.8, "Cl": 0.3, "F": 0.2}
        },
        {
            "position": "N-alkyl",
            "allowed_groups": ["N(C2H5)2", "N(CH3)2", "N(iPr)2", "pyrrolidino", "piperidino", "morpholino"],
            "potency_effect": {"N(C2H5)2": 1.0, "N(iPr)2": 0.9, "piperidino": 0.7}
        }
    ],
    excluded_combinations=["5-H + benzyl-H"],  # En az bir aktivatör olmalı
    potency_modifiers={
        "5-NO2 + para-isopropoxy": 1000.0,  # Etonitazene
        "5-NO2 + para-ethoxy": 500.0,  # Isotonitazene
        "5-NO2 + para-methoxy": 200.0,  # Metonitazene
        "5-CN + para-ethoxy": 100.0,  # Clonitazene benzeri
        "base": 100.0  # Morfin referansı
    },
    risk_level=RiskLevel.EXTREME,
    detection_notes="Standart fentanil test şeritleri ÇALIŞMAZ! Özel nitazen immunoassay gerekir.",
    forensic_markers=["benzimidazole_core", "5-nitro_fragment", "diethylaminoethyl_chain"]
)

# Nitazen alt kuralları
NITAZENE_SUBSTITUENTS = {
    "benzyl_para_substituents": [
        ("H", "unsubstituted", 1.0),
        ("OCH3", "methoxy", 200.0),
        ("OC2H5", "ethoxy", 500.0),
        ("OCH(CH3)2", "isopropoxy", 1000.0),
        ("OC3H7", "propoxy", 300.0),
        ("OC4H9", "butoxy", 150.0),
        ("F", "fluoro", 50.0),
        ("Cl", "chloro", 40.0),
        ("Br", "bromo", 30.0),
        ("CH3", "methyl", 80.0),
        ("C2H5", "ethyl", 120.0),
        ("CF3", "trifluoromethyl", 60.0)
    ],
    "position_5_substituents": [
        ("NO2", "nitro", 1.0),
        ("CN", "cyano", 0.8),
        ("Cl", "chloro", 0.3),
        ("F", "fluoro", 0.2),
        ("Br", "bromo", 0.25),
        ("NH2", "amino", 0.1)
    ],
    "amine_substituents": [
        ("N(C2H5)2", "diethylamino", 1.0),
        ("N(CH3)2", "dimethylamino", 0.6),
        ("N(iPr)2", "diisopropylamino", 0.9),
        ("pyrrolidino", "pyrrolidino", 0.7),
        ("piperidino", "piperidino", 0.75),
        ("morpholino", "morpholino", 0.5),
        ("N(C3H7)2", "dipropylamino", 0.8)
    ]
}

# ============================================================================
# 2. FENETİLAMİNLER (2C-x, DOx, NBOMe SERİSİ)
# ============================================================================

MARKUSH_RULES["PHENETHYLAMINE_2C"] = MarkushRule(
    rule_id="PHENETHYLAMINE_2C",
    rule_name="2C Serisi Fenetilamin",
    structure_class=StructureClass.PHENETHYLAMINE_2C,
    core_scaffold="Fenetilamin + 2,5-dimetoksi",
    core_smarts="NCCc1ccc(OC)cc1OC",  # 2,5-dimethoxyphenethylamine
    required_groups=[
        {"position": "2", "group": "OCH3", "description": "2-metoksi (sabit)", "required": True},
        {"position": "5", "group": "OCH3", "description": "5-metoksi (sabit)", "required": True}
    ],
    variable_positions=[
        {
            "position": "4",
            "allowed_groups": ["Br", "I", "Cl", "F", "CH3", "C2H5", "C3H7", "SCH3", "SC2H5", 
                              "NO2", "NH2", "CF3", "CN", "CHO", "COCH3"],
            "potency_effect": {"I": 1.5, "Br": 1.0, "Cl": 0.8, "C3H7": 1.2, "SCH3": 1.3}
        },
        {
            "position": "N",
            "allowed_groups": ["H", "CH3"],
            "potency_effect": {"H": 1.0, "CH3": 0.5}
        },
        {
            "position": "alpha",
            "allowed_groups": ["H", "CH3"],
            "potency_effect": {"H": 1.0, "CH3": 2.0}  # DOx oluşur
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "4-I": 1.5,  # 2C-I
        "4-Br": 1.0,  # 2C-B
        "4-Cl": 0.7,  # 2C-C
        "4-C2H5": 0.8,  # 2C-E
        "4-SCH3": 1.3,  # 2C-T-2
        "alpha-CH3": 2.0  # DOx conversion
    },
    risk_level=RiskLevel.HIGH,
    detection_notes="GC-MS ile tespit. 4-pozisyon substitüentine göre fragmentasyon değişir.",
    forensic_markers=["2,5-dimethoxyphenyl", "phenethylamine_chain"]
)

MARKUSH_RULES["PHENETHYLAMINE_DOX"] = MarkushRule(
    rule_id="PHENETHYLAMINE_DOX",
    rule_name="DOx Serisi (2,5-Dimetoksi Amfetamin)",
    structure_class=StructureClass.PHENETHYLAMINE_DOX,
    core_scaffold="Amfetamin + 2,5-dimetoksi",
    core_smarts="CC(N)Cc1ccc(OC)cc1OC",  # 2,5-dimethoxy amphetamine
    required_groups=[
        {"position": "2", "group": "OCH3", "description": "2-metoksi (sabit)", "required": True},
        {"position": "5", "group": "OCH3", "description": "5-metoksi (sabit)", "required": True},
        {"position": "alpha", "group": "CH3", "description": "Alfa-metil (amfetamin)", "required": True}
    ],
    variable_positions=[
        {
            "position": "4",
            "allowed_groups": ["CH3", "Br", "I", "Cl", "F", "C2H5", "C3H7", "NO2", "NH2"],
            "potency_effect": {"I": 3.0, "Br": 2.0, "CH3": 1.0, "C2H5": 1.5}
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "4-I": 3.0,  # DOI - çok potent
        "4-Br": 2.0,  # DOB
        "4-CH3": 1.0,  # DOM (STP)
        "4-C2H5": 1.5,  # DOET
        "4-F": 0.8,  # DOF
        "4-Cl": 1.2  # DOC
    },
    risk_level=RiskLevel.VERY_HIGH,
    detection_notes="Çok uzun etkili (16-30 saat). GC-MS ile tespit.",
    forensic_markers=["2,5-dimethoxyphenyl", "amphetamine_alpha_methyl"]
)

MARKUSH_RULES["PHENETHYLAMINE_NBOME"] = MarkushRule(
    rule_id="PHENETHYLAMINE_NBOME",
    rule_name="NBOMe Serisi (N-Benzilmetoksi Fenetilamin)",
    structure_class=StructureClass.PHENETHYLAMINE_NBOME,
    core_scaffold="2C-x + N-2-metoksibenzil",
    core_smarts="NCCc1ccc(OC)cc1OC.COc1ccccc1CN",  # 2C core + methoxybenzyl
    required_groups=[
        {"position": "2", "group": "OCH3", "description": "2-metoksi", "required": True},
        {"position": "5", "group": "OCH3", "description": "5-metoksi", "required": True},
        {"position": "N", "group": "CH2-C6H4-OCH3", "description": "N-2-metoksibenzil (KRİTİK)", "required": True}
    ],
    variable_positions=[
        {
            "position": "4",
            "allowed_groups": ["I", "Br", "Cl", "F", "CH3", "C2H5", "NO2", "H", "N", "C3H7"],
            "potency_effect": {"I": 10.0, "N": 8.0, "Br": 5.0, "Cl": 3.0}
        },
        {
            "position": "N-benzyl_ortho",
            "allowed_groups": ["OCH3", "OC2H5", "F", "Cl", "H"],
            "potency_effect": {"OCH3": 1.0, "F": 1.1}
        },
        {
            "position": "N-benzyl_type",
            "allowed_groups": ["NBOMe", "NBOH", "NBF", "NBCl"],
            "potency_effect": {"NBOMe": 1.0, "NBOH": 0.7, "NBF": 0.9}
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "25I-NBOMe": 10.0,  # En potent
        "25N-NBOMe": 8.0,
        "25B-NBOMe": 5.0,
        "25C-NBOMe": 3.0,
        "25E-NBOMe": 2.0
    },
    risk_level=RiskLevel.EXTREME,
    detection_notes="ÇOK POTENT! LSD'den 10x güçlü olabilir. Blotter kağıdında µg dozlar. ÖLÜMCÜL OLABİLİR!",
    forensic_markers=["2-methoxybenzyl", "dimethoxyphenethylamine", "halogenated_phenyl"]
)

# ============================================================================
# 3. TRİPTAMİNLER (DMT VE ANALOGLARI)
# ============================================================================

MARKUSH_RULES["TRYPTAMINE_CORE"] = MarkushRule(
    rule_id="TRYPTAMINE_CORE",
    rule_name="Triptamin Ana Kuralı",
    structure_class=StructureClass.TRYPTAMINE,
    core_scaffold="İndol halkası + Etilamin yan zinciri",
    core_smarts="NCCc1c[nH]c2ccccc12",  # Tryptamine SMARTS
    required_groups=[
        {"position": "indole", "group": "intact", "description": "İndol halkası", "required": True},
        {"position": "side_chain", "group": "ethylamine", "description": "Etilamin zinciri", "required": True}
    ],
    variable_positions=[
        {
            "position": "4",
            "allowed_groups": ["H", "OH", "OAc", "OPO3H2", "OCH3", "F", "Br", "Cl"],
            "potency_effect": {"OH": 1.0, "OAc": 1.0, "OPO3H2": 0.8, "OCH3": 0.5}
        },
        {
            "position": "5",
            "allowed_groups": ["H", "OH", "OCH3", "Br", "Cl", "F", "CH3"],
            "potency_effect": {"OCH3": 3.0, "OH": 1.5, "Br": 0.8}
        },
        {
            "position": "6",
            "allowed_groups": ["H", "F", "Cl", "Br", "OCH3"],
            "potency_effect": {"H": 1.0, "F": 0.9}
        },
        {
            "position": "7",
            "allowed_groups": ["H", "CH3", "C2H5", "F"],
            "potency_effect": {"H": 1.0, "C2H5": 1.1}
        },
        {
            "position": "N",
            "allowed_groups": ["N(CH3)2", "N(C2H5)2", "N(iPr)2", "N(C3H7)2", 
                              "N-allyl2", "N-cyclohexyl", "pyrrolidino"],
            "potency_effect": {"N(CH3)2": 1.0, "N(iPr)2": 0.8, "N(C2H5)2": 0.9}
        },
        {
            "position": "alpha",
            "allowed_groups": ["H", "CH3"],
            "potency_effect": {"H": 1.0, "CH3": 1.5}  # α-methyltryptamines
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "5-MeO-DMT": 4.0,  # Çok potent
        "4-HO-DMT": 1.0,  # Psilocin eşdeğeri
        "4-AcO-DMT": 1.0,  # Psilocin prodrug
        "5-MeO-MiPT": 2.0,
        "4-HO-MET": 0.8,
        "5-MeO-DiPT": 1.5,
        "alpha-MT": 1.5  # Alfa-metiltriptamin
    },
    risk_level=RiskLevel.HIGH,
    detection_notes="MAO inhibitörleri ile birlikte ÖLÜMCÜL olabilir. Ayahuasca kombinasyonu.",
    forensic_markers=["indole_core", "tryptamine_fragmentation", "N-alkyl_pattern"]
)

# Triptamin substitüent kombinasyonları
TRYPTAMINE_SUBSTITUENTS = {
    "ring_4_substituents": [
        ("H", "unsubstituted", 0.5),
        ("OH", "4-hydroxy", 1.0),  # Psilocin türü
        ("OAc", "4-acetoxy", 1.0),  # Prodrug
        ("OPO3H2", "4-phosphoryloxy", 0.8),  # Psilosibin
        ("OCH3", "4-methoxy", 0.6),
        ("F", "4-fluoro", 0.7),
        ("Br", "4-bromo", 0.5),
        ("Cl", "4-chloro", 0.4)
    ],
    "ring_5_substituents": [
        ("H", "unsubstituted", 1.0),
        ("OH", "5-hydroxy", 1.5),  # Bufotenin
        ("OCH3", "5-methoxy", 3.0),  # 5-MeO güçlü
        ("Br", "5-bromo", 0.8),
        ("Cl", "5-chloro", 0.7),
        ("F", "5-fluoro", 0.9),
        ("CH3", "5-methyl", 0.6)
    ],
    "n_substituents": [
        ("N(CH3)2", "dimethyl", 1.0),  # DMT
        ("N(C2H5)2", "diethyl", 0.9),  # DET
        ("N(iPr)2", "diisopropyl", 0.8),  # DiPT
        ("N(C3H7)2", "dipropyl", 0.7),  # DPT
        ("N(CH3)(iPr)", "methyl-isopropyl", 0.85),  # MiPT
        ("N(CH3)(C2H5)", "methyl-ethyl", 0.9),  # MET
        ("N-allyl2", "diallyl", 0.6),  # DALT
        ("N(cyclohexyl)2", "dicyclohexyl", 0.5),
        ("pyrrolidino", "pyrrolidino", 0.7)
    ]
}

# ============================================================================
# 4. TASARIMCI BENZODİAZEPİNLER
# ============================================================================

MARKUSH_RULES["BENZODIAZEPINE_DESIGNER"] = MarkushRule(
    rule_id="BENZODIAZEPINE_DESIGNER",
    rule_name="Tasarımcı Benzodiazepin",
    structure_class=StructureClass.BENZODIAZEPINE_DESIGNER,
    core_scaffold="1,4-Benzodiazepin halkası",
    core_smarts="c1ccc2c(c1)C=NC(=O)CN2",  # 1,4-benzodiazepine
    required_groups=[
        {"position": "core", "group": "benzodiazepine", "description": "1,4-BZD halkası", "required": True}
    ],
    variable_positions=[
        {
            "position": "7",
            "allowed_groups": ["Cl", "Br", "F", "NO2", "H", "CF3"],
            "potency_effect": {"Cl": 1.0, "Br": 1.5, "F": 1.2, "NO2": 2.0, "CF3": 1.3}
        },
        {
            "position": "2'-phenyl",
            "allowed_groups": ["H", "F", "Cl", "Br", "NO2", "CF3"],
            "potency_effect": {"F": 1.3, "Cl": 1.1, "H": 1.0}
        },
        {
            "position": "triazolo_fusion",
            "allowed_groups": ["none", "triazolo", "imidazo", "pyrazolo", "oxazolo"],
            "potency_effect": {"triazolo": 3.0, "imidazo": 2.0, "none": 1.0}
        },
        {
            "position": "1-N",
            "allowed_groups": ["H", "CH3", "C2H5"],
            "potency_effect": {"CH3": 1.2, "H": 1.0}
        },
        {
            "position": "thieno_replacement",
            "allowed_groups": ["benzene", "thiophene"],
            "potency_effect": {"thiophene": 0.8, "benzene": 1.0}  # Etizolam tipi
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "triazolo + 7-Cl + 2'-F": 4.0,  # Flualprazolam tipi
        "triazolo + 7-NO2 + 2'-Cl": 5.0,  # Clonazolam
        "triazolo + 7-Br + 2'-F": 6.0,  # Flubromazolam
        "thieno + triazolo": 0.8,  # Etizolam
        "imidazo + 7-Cl": 2.5  # Midazolam tipi
    },
    risk_level=RiskLevel.VERY_HIGH,
    detection_notes="Standart BZD immunoassay ile TESPİT EDİLMEYEBİLİR! LC-MS/MS gerekir.",
    forensic_markers=["benzodiazepine_core", "triazolo_fragment", "halogenated_phenyl"]
)

# Benzodiazepin substitüent kombinasyonları
BENZODIAZEPINE_SUBSTITUENTS = {
    "position_7": [
        ("Cl", "chloro", 1.0),
        ("Br", "bromo", 1.5),
        ("F", "fluoro", 1.2),
        ("NO2", "nitro", 2.0),
        ("H", "unsubstituted", 0.5),
        ("CF3", "trifluoromethyl", 1.3)
    ],
    "phenyl_ortho": [
        ("H", "unsubstituted", 1.0),
        ("F", "2'-fluoro", 1.3),
        ("Cl", "2'-chloro", 1.1),
        ("Br", "2'-bromo", 1.0)
    ],
    "ring_fusion": [
        ("none", "simple_BZD", 1.0),
        ("triazolo", "triazolobenzodiazepine", 3.0),
        ("imidazo", "imidazobenzodiazepine", 2.0),
        ("pyrazolo", "pyrazolobenzodiazepine", 1.5),
        ("oxazolo", "oxazolobenzodiazepine", 1.3)
    ],
    "thieno_swap": [
        ("benzene", "benzodiazepine", 1.0),
        ("thiophene", "thienodiazepine", 0.8)  # Etizolam
    ]
}

# ============================================================================
# 5. DİSOSİYATİFLER (ARİLSİKLOHEKZİLAMİNLER)
# ============================================================================

MARKUSH_RULES["DISSOCIATIVE_ACH"] = MarkushRule(
    rule_id="DISSOCIATIVE_ACH",
    rule_name="Disosiyatif (Arilsiklohekzilamin)",
    structure_class=StructureClass.DISSOCIATIVE_ACH,
    core_scaffold="Siklohekzan + Aromatik halka + Amin",
    core_smarts="NC1CCCCC1c1ccccc1",  # Basic arylcyclohexylamine
    required_groups=[
        {"position": "cyclohexyl", "group": "C6H11", "description": "Siklohekzan halkası", "required": True},
        {"position": "aryl", "group": "phenyl/chlorophenyl", "description": "Aromatik halka", "required": True},
        {"position": "amine", "group": "NR2", "description": "Amin grubu", "required": True}
    ],
    variable_positions=[
        {
            "position": "aryl_ortho",
            "allowed_groups": ["H", "Cl", "F", "Br", "CH3", "OCH3", "CF3"],
            "potency_effect": {"Cl": 1.0, "F": 1.1, "OCH3": 1.5, "H": 0.8}
        },
        {
            "position": "aryl_meta",
            "allowed_groups": ["H", "OCH3", "OH", "F", "Cl", "CH3"],
            "potency_effect": {"OCH3": 2.0, "OH": 1.5, "H": 1.0}  # MXE, 3-MeO-PCP
        },
        {
            "position": "amine",
            "allowed_groups": ["NH(CH3)", "NH(C2H5)", "piperidino", "pyrrolidino", "morpholino", "NH2"],
            "potency_effect": {"piperidino": 1.5, "NH(CH3)": 1.0, "morpholino": 0.8}
        },
        {
            "position": "cyclohexyl_C2",
            "allowed_groups": ["H", "=O", "OH"],
            "potency_effect": {"=O": 0.8, "H": 1.2, "OH": 0.7}  # Ketamin vs PCP
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "2-Cl + piperidino": 1.5,  # PCP
        "2-Cl + NH(CH3) + C2=O": 1.0,  # Ketamin
        "3-MeO + piperidino": 2.0,  # 3-MeO-PCP
        "3-MeO + NH(C2H5) + C2=O": 1.8,  # MXE
        "3-OH + piperidino": 1.5,  # 3-HO-PCP
        "2-F + NH(CH3) + C2=O": 0.9  # 2-FDCK
    },
    risk_level=RiskLevel.HIGH,
    detection_notes="NMDA antagonist. Ketamin immunoassay bazı türevleri kaçırabilir.",
    forensic_markers=["cyclohexyl_core", "aryl_fragment", "amine_pattern"]
)

# ============================================================================
# 6. SENTETİK KANNABİNOİDLER
# ============================================================================

MARKUSH_RULES["SYNTHETIC_CANNABINOID"] = MarkushRule(
    rule_id="SYNTHETIC_CANNABINOID",
    rule_name="Sentetik Kannabinoid",
    structure_class=StructureClass.SYNTHETIC_CANNABINOID,
    core_scaffold="İndol/İndazol + Naftoil/Kinolin + N-alkil zincir",
    core_smarts="c1ccc2c(c1)[nH]cc2",  # İndol veya indazol
    required_groups=[
        {"position": "core", "group": "indole/indazole", "description": "Heteroaromatik çekirdek", "required": True},
        {"position": "N1", "group": "N-alkyl", "description": "N-alkil zincir (C4-C8)", "required": True}
    ],
    variable_positions=[
        {
            "position": "core_type",
            "allowed_groups": ["indole", "indazole", "pyrrole", "7-azaindole"],
            "potency_effect": {"indazole": 1.5, "indole": 1.0, "7-azaindole": 1.2}
        },
        {
            "position": "C3_linker",
            "allowed_groups": ["carbonyl", "carboxamide", "carboxylate", "none"],
            "potency_effect": {"carboxamide": 2.0, "carbonyl": 1.0, "carboxylate": 1.5}
        },
        {
            "position": "terminal_group",
            "allowed_groups": ["naphthyl", "quinolinyl", "adamantyl", "cumyl", "cyclohexyl", "tert-leucinate"],
            "potency_effect": {"naphthyl": 1.0, "adamantyl": 1.2, "tert-leucinate": 3.0}
        },
        {
            "position": "N1_chain",
            "allowed_groups": ["pentyl", "hexyl", "butyl", "cyclohexylmethyl", "4-fluorobenzyl", "cumyl"],
            "potency_effect": {"pentyl": 1.0, "5-fluoropentyl": 2.5, "cyclohexylmethyl": 1.2}
        },
        {
            "position": "ring_halogen",
            "allowed_groups": ["H", "F", "Cl", "Br"],
            "potency_effect": {"F": 1.3, "H": 1.0}
        },
        {
            "position": "terminal_fluorine",
            "allowed_groups": ["H", "F"],
            "potency_effect": {"F": 2.5, "H": 1.0}  # 5F- türevler
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "indazole + carboxamide + tert-leucinate + 5F-pentyl": 50.0,  # MDMB-4en-PINACA tipi
        "indazole + carboxamide + adamantyl + pentyl": 10.0,  # AKB-48
        "indole + carbonyl + naphthyl + pentyl": 5.0,  # JWH-018
        "indazole + carboxamide + cumyl + 5F-pentyl": 40.0,  # 5F-CUMYL-PINACA
        "base_THC": 1.0
    },
    risk_level=RiskLevel.EXTREME,
    detection_notes="THC immunoassay İLE TESPİT EDİLMEZ! Özel SC paneli gerekir. Toksisite değişken.",
    forensic_markers=["indole_indazole_core", "N-alkyl_chain", "carbonyl_linker", "terminal_aryl"]
)

# ============================================================================
# 7. SENTETİK KATİNONLAR
# ============================================================================

MARKUSH_RULES["SYNTHETIC_CATHINONE"] = MarkushRule(
    rule_id="SYNTHETIC_CATHINONE",
    rule_name="Sentetik Katinon",
    structure_class=StructureClass.SYNTHETIC_CATHINONE,
    core_scaffold="Beta-keto fenetilamin (Katinon iskeleti)",
    core_smarts="CC(N)C(=O)c1ccccc1",  # Cathinone
    required_groups=[
        {"position": "beta", "group": "C=O", "description": "Beta-keto grubu", "required": True},
        {"position": "alpha", "group": "CH", "description": "Alfa karbon", "required": True},
        {"position": "amine", "group": "N", "description": "Amin azotu", "required": True}
    ],
    variable_positions=[
        {
            "position": "ring_4",
            "allowed_groups": ["H", "CH3", "F", "Cl", "Br", "OCH3", "methylenedioxy"],
            "potency_effect": {"methylenedioxy": 1.5, "CH3": 1.0, "F": 1.2}
        },
        {
            "position": "alpha",
            "allowed_groups": ["H", "CH3", "C2H5", "C3H7"],
            "potency_effect": {"C3H7": 1.5, "C2H5": 1.3, "CH3": 1.0}  # α-PVP benzeri
        },
        {
            "position": "amine",
            "allowed_groups": ["NH2", "NH(CH3)", "NH(C2H5)", "pyrrolidino", "piperidino"],
            "potency_effect": {"pyrrolidino": 2.5, "piperidino": 2.0, "NH(CH3)": 1.0}
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "4-methylenedioxy + pyrrolidino + alpha-propyl": 5.0,  # MDPV
        "4-methyl + NH(CH3)": 1.2,  # Mephedrone
        "H + pyrrolidino + alpha-pentyl": 4.0,  # α-PVP (Flakka)
        "4-F + pyrrolidino + alpha-butyl": 3.5,  # 4F-α-PHP
        "4-Cl + pyrrolidino + alpha-propyl": 3.0
    },
    risk_level=RiskLevel.VERY_HIGH,
    detection_notes="Amfetamin immunoassay bazıları yakalayabilir ama hepsi değil. LC-MS/MS önerilir.",
    forensic_markers=["beta-keto_fragment", "phenyl_ring", "pyrrolidino_pattern"]
)

# ============================================================================
# 8. FENTANİL ANALOGLARI
# ============================================================================

MARKUSH_RULES["FENTANYL_ANALOG"] = MarkushRule(
    rule_id="FENTANYL_ANALOG",
    rule_name="Fentanil Analoğu",
    structure_class=StructureClass.FENTANYL_ANALOG,
    core_scaffold="4-Anilidopiperidin + N-feniletil",
    core_smarts="c1ccc(CCN2CCC(Nc3ccccc3)CC2)cc1",  # Fentanyl core
    required_groups=[
        {"position": "piperidine", "group": "4-anilido", "description": "4-Anilidopiperidin", "required": True},
        {"position": "N-phenethyl", "group": "phenethyl", "description": "N-feniletil", "required": True}
    ],
    variable_positions=[
        {
            "position": "acyl",
            "allowed_groups": ["propionyl", "acetyl", "butyryl", "isobutyryl", "valeryl", 
                              "cyclopropyl", "furanoyl", "benzoyl", "phenylacetyl"],
            "potency_effect": {"propionyl": 1.0, "acetyl": 0.15, "cyclopropyl": 1.2, 
                              "furanoyl": 1.5, "butyryl": 0.25, "benzoyl": 0.1}
        },
        {
            "position": "anilide_para",
            "allowed_groups": ["H", "F", "Cl", "CH3", "OCH3", "C2H5"],
            "potency_effect": {"F": 1.5, "CH3": 1.3, "H": 1.0, "Cl": 0.9}
        },
        {
            "position": "phenethyl_ring",
            "allowed_groups": ["H", "2-F", "3-F", "4-F", "2-Cl", "3-Cl", "4-Cl", "2-CH3", "4-CH3", "4-OCH3"],
            "potency_effect": {"4-F": 1.3, "2-F": 0.9, "H": 1.0}
        },
        {
            "position": "piperidine_3",
            "allowed_groups": ["H", "3-CH3-cis", "3-CH3-trans", "3-allyl"],
            "potency_effect": {"3-CH3-trans": 6.0, "3-CH3-cis": 3.0, "H": 1.0}  # 3-Methylfentanyl
        },
        {
            "position": "piperidine_4",
            "allowed_groups": ["anilido", "carbomethoxy", "carboethoxy"],
            "potency_effect": {"carbomethoxy": 100.0, "anilido": 1.0}  # Carfentanil!
        }
    ],
    excluded_combinations=[],
    potency_modifiers={
        "propionyl + H + H + H + anilido": 1.0,  # Fentanil (referans)
        "acetyl + H + H + H + anilido": 0.15,  # Acetylfentanyl
        "propionyl + F + 4-F + 3-CH3-trans + anilido": 10.0,  # Çok potent analog
        "propionyl + H + H + H + carbomethoxy": 100.0,  # Carfentanil
        "furanoyl + F + H + H + anilido": 2.0,  # Furanylfentanyl
        "cyclopropyl + F + H + H + anilido": 1.5  # Cyclopropylfentanyl
    },
    risk_level=RiskLevel.EXTREME,
    detection_notes="Fentanil immunoassay bazı analogları yakalamayabilir. Nalokson doz aşımı tedavisinde ÇOKLU DOZ gerekebilir!",
    forensic_markers=["norfentanyl", "4-ANPP_precursor", "phenethyl_fragment", "piperidine_core"]
)


# ============================================================================
# YAPISAL EŞLEŞTİRME VE TANIMLAMA FONKSİYONLARI
# ============================================================================

def match_structure(smiles: str = None, 
                   fragments: List[float] = None,
                   molecular_weight: float = None,
                   structure_hints: List[str] = None) -> List[StructuralMatch]:
    """
    Bilinmeyen yapıyı Markush kurallarıyla eşleştir
    nrcdnl94
    """
    
    matches = []
    
    for rule_id, rule in MARKUSH_RULES.items():
        match_score = 0.0
        identified_subs = []
        warnings = []
        
        # SMILES eşleştirmesi
        if smiles:
            # Basit pattern matching
            core_patterns = {
                "NITAZENE_CORE": ["benzimidazole", "N(C2H5)2", "NO2"],
                "PHENETHYLAMINE_2C": ["dimethoxyphenyl", "NCCc"],
                "PHENETHYLAMINE_NBOME": ["methoxybenzyl", "dimethoxy"],
                "TRYPTAMINE_CORE": ["indole", "NCCc", "c1c[nH]c2"],
                "BENZODIAZEPINE_DESIGNER": ["diazepine", "C=NC(=O)"],
                "DISSOCIATIVE_ACH": ["cyclohexyl", "phenyl", "amine"],
                "SYNTHETIC_CANNABINOID": ["indole", "indazole", "naphthoyl"],
                "SYNTHETIC_CATHINONE": ["C(=O)c1ccc", "NC"],
                "FENTANYL_ANALOG": ["piperidine", "anilido", "phenethyl"]
            }
            
            for pattern in core_patterns.get(rule_id, []):
                if pattern.lower() in smiles.lower():
                    match_score += 20
                    identified_subs.append(f"Core: {pattern}")
        
        # MW eşleştirmesi
        if molecular_weight:
            mw_ranges = {
                "NITAZENE_CORE": (380, 500),
                "PHENETHYLAMINE_2C": (180, 350),
                "PHENETHYLAMINE_NBOME": (350, 500),
                "TRYPTAMINE_CORE": (160, 350),
                "BENZODIAZEPINE_DESIGNER": (280, 450),
                "DISSOCIATIVE_ACH": (200, 350),
                "SYNTHETIC_CANNABINOID": (280, 500),
                "SYNTHETIC_CATHINONE": (170, 350),
                "FENTANYL_ANALOG": (280, 500)
            }
            
            mw_range = mw_ranges.get(rule_id, (100, 600))
            if mw_range[0] <= molecular_weight <= mw_range[1]:
                match_score += 15
                identified_subs.append(f"MW: {molecular_weight} in range")
        
        # Yapısal ipuçları
        if structure_hints:
            hint_keywords = {
                "NITAZENE_CORE": ["nitazene", "benzimidazole", "opioid", "nitro"],
                "PHENETHYLAMINE_2C": ["2c", "phenethylamine", "methoxy", "hallucinogen"],
                "PHENETHYLAMINE_NBOME": ["nbome", "benzyl", "blotter"],
                "TRYPTAMINE_CORE": ["tryptamine", "dmt", "indole", "psychedelic"],
                "BENZODIAZEPINE_DESIGNER": ["benzo", "diazepine", "sedative", "triazolo"],
                "DISSOCIATIVE_ACH": ["ketamine", "pcp", "dissociative", "nmda"],
                "SYNTHETIC_CANNABINOID": ["cannabinoid", "spice", "jwh", "indazole"],
                "SYNTHETIC_CATHINONE": ["cathinone", "bath salt", "pvp", "stimulant"],
                "FENTANYL_ANALOG": ["fentanyl", "opioid", "anilido", "piperidine"]
            }
            
            for hint in structure_hints:
                for keyword in hint_keywords.get(rule_id, []):
                    if keyword.lower() in hint.lower():
                        match_score += 25
                        identified_subs.append(f"Hint: {keyword}")
                        break
        
        # Fragment eşleştirmesi
        if fragments:
            # Karakteristik fragman m/z değerleri
            fragment_patterns = {
                "NITAZENE_CORE": [100, 72, 146, 175],
                "PHENETHYLAMINE_2C": [91, 166, 181, 151],
                "PHENETHYLAMINE_NBOME": [121, 91, 150, 278],
                "TRYPTAMINE_CORE": [130, 143, 58, 44],
                "BENZODIAZEPINE_DESIGNER": [269, 241, 313, 77],
                "DISSOCIATIVE_ACH": [91, 77, 180, 207],
                "SYNTHETIC_CANNABINOID": [127, 155, 214, 284],
                "SYNTHETIC_CATHINONE": [91, 105, 77, 119],
                "FENTANYL_ANALOG": [189, 146, 105, 245]
            }
            
            rule_frags = fragment_patterns.get(rule_id, [])
            for frag in fragments:
                for ref_frag in rule_frags:
                    if abs(frag - ref_frag) < 2:  # 2 Da tolerans
                        match_score += 10
                        identified_subs.append(f"Fragment: {frag}")
                        break
        
        # Eşik kontrolü
        if match_score >= 20:
            # Potens tahmini
            potency_estimate = 1.0
            for mod, mult in rule.potency_modifiers.items():
                if any(mod.lower() in s.lower() for s in identified_subs):
                    potency_estimate *= mult
            
            # Uyarılar
            if rule.risk_level == RiskLevel.EXTREME:
                warnings.append("AŞIRI TEHLİKELİ! Özel önlemler gerekli.")
            if rule.risk_level == RiskLevel.VERY_HIGH:
                warnings.append("Çok yüksek risk. Dikkatli yaklaşın.")
            if "fentanil" in rule.structure_class.value.lower():
                warnings.append("Nalokson hazır tutun!")
            if "nbome" in rule.structure_class.value.lower():
                warnings.append("µg dozlar ÖLÜMCÜL olabilir!")
            
            matches.append(StructuralMatch(
                matched=True,
                structure_class=rule.structure_class,
                matched_rule=rule.rule_name,
                core_scaffold=rule.core_scaffold,
                identified_substituents=identified_subs,
                potency_estimate=round(potency_estimate, 2),
                risk_level=rule.risk_level,
                confidence=min(100, match_score),
                warnings=warnings + [rule.detection_notes],
                recommended_tests=rule.forensic_markers
            ))
    
    # Skora göre sırala
    matches.sort(key=lambda x: x.confidence, reverse=True)
    
    return matches


def generate_all_possible_variants(rule_id: str, max_per_position: int = 5) -> List[Dict]:
    """
    Bir Markush kuralı için tüm olası varyantları üret
    nrcdnl94
    """
    
    rule = MARKUSH_RULES.get(rule_id)
    if not rule:
        return []
    
    variants = []
    
    # Her değişken pozisyon için kombinasyonlar
    position_options = []
    position_names = []
    
    for pos_info in rule.variable_positions:
        pos_name = pos_info["position"]
        allowed = pos_info["allowed_groups"][:max_per_position]  # Limitle
        position_options.append(allowed)
        position_names.append(pos_name)
    
    # Kartezyen çarpım
    for combo in product(*position_options):
        variant = {
            "rule_id": rule_id,
            "structure_class": rule.structure_class.value,
            "core_scaffold": rule.core_scaffold,
            "substitution_pattern": {}
        }
        
        potency = 1.0
        
        for i, (pos_name, sub) in enumerate(zip(position_names, combo)):
            variant["substitution_pattern"][pos_name] = sub
            
            # Potens hesapla
            pos_info = rule.variable_positions[i]
            potency_effect = pos_info.get("potency_effect", {})
            if sub in potency_effect:
                potency *= potency_effect[sub]
        
        variant["potency_estimate"] = round(potency, 2)
        variant["risk_level"] = rule.risk_level.value
        
        variants.append(variant)
    
    return variants


def get_markush_statistics() -> Dict:
    """Markush kural istatistikleri - nrcdnl94"""
    
    stats = {
        "total_rules": len(MARKUSH_RULES),
        "total_possible_variants": 0,
        "by_class": {},
        "by_risk_level": {},
        "highest_potency_rules": []
    }
    
    for rule_id, rule in MARKUSH_RULES.items():
        # Sınıf sayımı
        class_name = rule.structure_class.value
        stats["by_class"][class_name] = stats["by_class"].get(class_name, 0) + 1
        
        # Risk seviyesi
        risk = rule.risk_level.value
        stats["by_risk_level"][risk] = stats["by_risk_level"].get(risk, 0) + 1
        
        # Olası varyant sayısı hesapla
        variant_count = 1
        for pos in rule.variable_positions:
            variant_count *= len(pos["allowed_groups"])
        stats["total_possible_variants"] += variant_count
        
        # En yüksek potens kuralları
        max_potency = max(rule.potency_modifiers.values()) if rule.potency_modifiers else 1.0
        if max_potency >= 10:
            stats["highest_potency_rules"].append({
                "rule": rule.rule_name,
                "max_potency": max_potency,
                "class": class_name
            })
    
    # Sırala
    stats["highest_potency_rules"] = sorted(
        stats["highest_potency_rules"], 
        key=lambda x: x["max_potency"], 
        reverse=True
    )[:10]
    
    return stats


# nrcdnl94 - End of Markush Rules Module
# Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır - All Rights Reserved
