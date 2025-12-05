"""
================================================================================
EpiClock Prototype v4.0 - NPS (Novel Psychoactive Substances) Derivatives Module
================================================================================
Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır
Digital Signature: nrcdnl94
ALL RIGHTS RESERVED - PROPRIETARY AND CONFIDENTIAL

KOMBİNATORYAL NPS VERİTABANI - 1500+ TÜREV
============================================================================
Sistematik Kimyasal Modifikasyon Prensipleri:
1. Fonksiyonel Grup Değişiklikleri (Amin, Hidroksil, Metoksi, Halojenler)
2. Halka Substitüsyonları (2-, 3-, 4- pozisyonları)
3. Yan Zincir Uzunluğu (C1-C8) ve Doygunluk
4. Stereoizomer ve Konformasyon Değişiklikleri

Referanslar:
- UNODC Early Warning Advisory on NPS
- EMCDDA NPS Database
- Cayman Chemical NPS Reference Library
- DEA Emerging Threat Reports
- PubChem Substance Database
================================================================================
"""

# nrcdnl94 - Author Signature - Do Not Remove

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
from itertools import product
import numpy as np
import hashlib

# nrcdnl94
class NPSClass(Enum):
    """NPS Ana Sınıfları - UNODC Sınıflandırması"""
    SYNTHETIC_CANNABINOIDS = "Sentetik Kannabinoidler"
    SYNTHETIC_CATHINONES = "Sentetik Katinonlar"
    PHENETHYLAMINES = "Fenetiilaminler"
    SYNTHETIC_OPIOIDS = "Sentetik Opioidler"
    TRYPTAMINES = "Triptaminler"
    BENZODIAZEPINES_NPS = "Tasarım Benzodiazepinleri"
    ARYLCYCLOHEXYLAMINES = "Arilsiklohekzilaminler"
    PIPERAZINES = "Piperazinler"
    AMINOINDANES = "Aminoindanlar"
    PLANTS_BASED_NPS = "Bitki Bazlı NPS"

# nrcdnl94
class ChemicalModification(Enum):
    """Kimyasal Modifikasyon Türleri"""
    HALOGENATION_F = "Florinasyon (-F)"
    HALOGENATION_Cl = "Klorinasyon (-Cl)"
    HALOGENATION_Br = "Brominasyon (-Br)"
    HALOGENATION_I = "İyodinasyon (-I)"
    METHYLATION = "Metilasyon (-CH3)"
    ETHYLATION = "Etilasyon (-C2H5)"
    PROPYLATION = "Propilasyon (-C3H7)"
    BUTYLATION = "Bütilasyon (-C4H9)"
    HYDROXYLATION = "Hidroksilasyon (-OH)"
    METHOXYLATION = "Metoksilasyon (-OCH3)"
    ETHOXYLATION = "Etoksilasyon (-OC2H5)"
    NITRATION = "Nitrasyon (-NO2)"
    AMINATION = "Aminasyon (-NH2)"
    CHAIN_EXTENSION = "Zincir Uzatma"
    CHAIN_SHORTENING = "Zincir Kısaltma"
    RING_SUBSTITUTION = "Halka Substitüsyonu"
    N_ALKYLATION = "N-Alkilasyon"
    ALPHA_SUBSTITUTION = "Alfa Substitüsyon"
    STEREOISOMER_R = "R-Stereoizomer"
    STEREOISOMER_S = "S-Stereoizomer"
    CIS_ISOMER = "cis-İzomer"
    TRANS_ISOMER = "trans-İzomer"
    RING_FUSION = "Halka Füzyonu"
    METHYLENEDIOXY = "Metilendioksi (-OCH2O-)"

@dataclass
# nrcdnl94
class NPSDerivative:
    """NPS Türev Yapısı - nrcdnl94"""
    compound_id: str
    name_iupac: str
    name_common: str
    name_turkish: str
    parent_compound: str
    nps_class: NPSClass
    modifications: List[ChemicalModification]
    molecular_formula: str
    molecular_weight: float
    potency_ratio: float
    receptor_targets: List[str]
    binding_affinity: Dict[str, float]
    metabolism_half_life: float
    detection_markers: List[str]
    cpg_markers: List[str]
    legal_status: str
    first_reported: str
    street_names: List[str]
    toxicity_notes: str
    eaa_effect: float


# ============================================================================
# KOMBİNATORYAL KURAL TABLOLARI - nrcdnl94
# ============================================================================

# Halka pozisyonları
RING_POSITIONS = ["2", "3", "4", "5", "6", "7"]

# Halojen substitüsyonları
HALOGENS = {
    "F": (ChemicalModification.HALOGENATION_F, 19, 1.2),
    "Cl": (ChemicalModification.HALOGENATION_Cl, 35.5, 1.1),
    "Br": (ChemicalModification.HALOGENATION_Br, 80, 1.0),
    "I": (ChemicalModification.HALOGENATION_I, 127, 0.9)
}

# Alkil grupları
ALKYL_GROUPS = {
    "methyl": (ChemicalModification.METHYLATION, 15, "CH3"),
    "ethyl": (ChemicalModification.ETHYLATION, 29, "C2H5"),
    "propyl": (ChemicalModification.PROPYLATION, 43, "C3H7"),
    "isopropyl": (ChemicalModification.PROPYLATION, 43, "CH(CH3)2"),
    "butyl": (ChemicalModification.BUTYLATION, 57, "C4H9"),
    "isobutyl": (ChemicalModification.BUTYLATION, 57, "CH2CH(CH3)2"),
    "tert-butyl": (ChemicalModification.BUTYLATION, 57, "C(CH3)3"),
    "pentyl": (ChemicalModification.CHAIN_EXTENSION, 71, "C5H11"),
    "hexyl": (ChemicalModification.CHAIN_EXTENSION, 85, "C6H13"),
    "heptyl": (ChemicalModification.CHAIN_EXTENSION, 99, "C7H15"),
    "octyl": (ChemicalModification.CHAIN_EXTENSION, 113, "C8H17"),
    "cyclohexyl": (ChemicalModification.RING_SUBSTITUTION, 83, "C6H11"),
    "cyclopentyl": (ChemicalModification.RING_SUBSTITUTION, 69, "C5H9"),
    "benzyl": (ChemicalModification.RING_SUBSTITUTION, 91, "CH2C6H5"),
    "phenyl": (ChemicalModification.RING_SUBSTITUTION, 77, "C6H5")
}

# Oksi grupları
OXY_GROUPS = {
    "hydroxy": (ChemicalModification.HYDROXYLATION, 17, "OH"),
    "methoxy": (ChemicalModification.METHOXYLATION, 31, "OCH3"),
    "ethoxy": (ChemicalModification.ETHOXYLATION, 45, "OC2H5"),
    "methylenedioxy": (ChemicalModification.METHYLENEDIOXY, 44, "OCH2O")
}

# N-substitüsyonları
N_SUBSTITUTIONS = {
    "N-methyl": ("NMe", 14),
    "N-ethyl": ("NEt", 28),
    "N-propyl": ("NPr", 42),
    "N-isopropyl": ("NiPr", 42),
    "N-butyl": ("NBu", 56),
    "N,N-dimethyl": ("NMe2", 28),
    "N,N-diethyl": ("NEt2", 56),
    "N,N-dipropyl": ("NPr2", 84),
    "N,N-diisopropyl": ("NiPr2", 84),
    "pyrrolidino": ("pyrr", 54),
    "piperidino": ("pip", 68),
    "morpholino": ("morph", 70)
}


def generate_nps_database() -> Dict[str, NPSDerivative]:
    """
    Kombinatoryal NPS Türev Veritabanı Generator
    1500+ Sistematik Türev
    nrcdnl94
    """
    
    nps_db = {}
    
    # ========================================================================
    # 1. SENTETİK KANNABİNOİDLER (~350 türev)
    # ========================================================================
    # nrcdnl94
    
    # Ana iskeletler
    cannabinoid_scaffolds = [
        ("JWH", "naphthoylindole", 320, ["CB1", "CB2"]),
        ("AM", "naphthoylindole", 340, ["CB1", "CB2"]),
        ("UR", "tetramethylcyclopropyl", 360, ["CB1", "CB2"]),
        ("PB", "quinolinyl", 330, ["CB1", "CB2"]),
        ("XLR", "fluoropentyl", 350, ["CB1", "CB2"]),
        ("AKB", "indazole-carboxamide", 370, ["CB1", "CB2"]),
        ("AB", "indazole-carboxamide", 365, ["CB1", "CB2"]),
        ("MDMB", "dimethylbutanoate", 390, ["CB1", "CB2"]),
        ("ADB", "tert-leucinate", 380, ["CB1", "CB2"]),
        ("AMB", "methyl-butanoate", 375, ["CB1", "CB2"]),
        ("EMB", "ethyl-butanoate", 385, ["CB1", "CB2"]),
        ("CUMYL", "cumyl-indazole", 400, ["CB1", "CB2"])
    ]
    
    # Yan zincir modifikasyonları
    sc_chains = ["pentyl", "hexyl", "butyl", "propyl", "cyclohexylmethyl", "4-fluorobenzyl", "cumyl"]
    sc_ring_mods = ["", "4-F", "5-F", "4-Cl", "4-Br", "4-Me", "4-OMe", "5-Cl"]
    sc_core_mods = ["indole", "indazole", "7-azaindole", "pyrrole"]
    
    for scaffold, desc, base_mw, targets in cannabinoid_scaffolds:
        for chain in sc_chains:
            for ring_mod in sc_ring_mods:
                for core in sc_core_mods[:2]:  # İndol ve indazol
                    # Potens hesapla
                    potency = 1.0
                    if "5-F" in ring_mod or "5F" in chain:
                        potency *= 2.5
                    if "MDMB" in scaffold or "ADB" in scaffold:
                        potency *= 3.0
                    if core == "indazole":
                        potency *= 1.2
                    if "hexyl" in chain:
                        potency *= 0.9
                    if "4-F" in ring_mod:
                        potency *= 1.3
                    
                    name_parts = []
                    if ring_mod:
                        name_parts.append(ring_mod)
                    name_parts.append(scaffold)
                    if chain != "pentyl":
                        name_parts.append(chain[:3].upper())
                    if core == "indazole" and "indole" in desc:
                        name_parts.append("INAZ")
                    
                    name = "-".join(name_parts) if len(name_parts) > 1 else scaffold
                    compound_id = f"SC_{name.replace('-', '_').replace(' ', '_')}"
                    
                    if compound_id not in nps_db:
                        mods = [ChemicalModification.RING_SUBSTITUTION]
                        if "F" in ring_mod:
                            mods.append(ChemicalModification.HALOGENATION_F)
                        if "Cl" in ring_mod:
                            mods.append(ChemicalModification.HALOGENATION_Cl)
                        if "Br" in ring_mod:
                            mods.append(ChemicalModification.HALOGENATION_Br)
                        if chain in ["hexyl", "heptyl"]:
                            mods.append(ChemicalModification.CHAIN_EXTENSION)
                        
                        nps_db[compound_id] = NPSDerivative(
                            compound_id=compound_id,
                            name_iupac=f"{scaffold} {desc} derivative",
                            name_common=name,
                            name_turkish=f"{name} (Sentetik Kannabinoid)",
                            parent_compound=scaffold,
                            nps_class=NPSClass.SYNTHETIC_CANNABINOIDS,
                            modifications=mods,
                            molecular_formula=f"C{22+len(chain)//2}H{28+len(chain)//2}N2O",
                            molecular_weight=base_mw + len(chain) * 7,
                            potency_ratio=round(potency, 2),
                            receptor_targets=targets,
                            binding_affinity={"CB1": round(10/potency, 2), "CB2": round(20/potency, 2)},
                            metabolism_half_life=2.5 + potency * 0.5,
                            detection_markers=[f"{scaffold}_M1", f"{scaffold}_M2"],
                            cpg_markers=["cg02242964", "cg09935388", "cg04180046", "cg07123182"],
                            legal_status="Liste I" if potency > 2.0 else "Kontrollü",
                            first_reported="2008-2024",
                            street_names=[name, "Spice", "K2", "Synthetic weed"],
                            toxicity_notes=f"THC'den {potency:.1f}x daha potent. Ciddi toksisite riski." if potency > 2 else "Orta düzey risk",
                            eaa_effect=1.5 + potency * 0.4
                        )
    
    # ========================================================================
    # 2. SENTETİK KATİNONLAR (~280 türev)
    # ========================================================================
    # nrcdnl94
    
    # Ana iskeletler
    cathinone_scaffolds = [
        ("methcathinone", "MC", 163, ["DAT", "SERT", "NET"]),
        ("ethcathinone", "EC", 177, ["DAT", "SERT", "NET"]),
        ("buphedrone", "BUP", 177, ["DAT", "NET"]),
        ("pentedrone", "PEN", 191, ["DAT", "NET"]),
        ("hexedrone", "HEX", 205, ["DAT", "NET"]),
        ("α-PVP", "PVP", 231, ["DAT", "NET"]),
        ("α-PHP", "PHP", 245, ["DAT", "NET"]),
        ("α-PBP", "PBP", 217, ["DAT", "NET"]),
        ("α-PPP", "PPP", 203, ["DAT", "NET"]),
        ("MDPV", "MDPV", 275, ["DAT", "NET"])
    ]
    
    # Halka substitüsyonları
    cat_ring_positions = ["3", "4"]
    cat_ring_groups = ["", "F", "Cl", "Br", "Me", "OMe", "Et"]
    cat_methylenedioxy = [False, True]
    cat_n_subs = ["N-Me", "N-Et", "N-iPr", "N,N-diMe", "pyrrolidino"]
    cat_stereo = ["", "R", "S"]
    
    for scaffold, abbrev, base_mw, targets in cathinone_scaffolds:
        for pos in cat_ring_positions:
            for group in cat_ring_groups:
                for md in cat_methylenedioxy:
                    for n_sub in cat_n_subs[:3]:  # İlk 3'ü
                        for stereo in cat_stereo[:2]:  # Rasemat ve R
                            if md and group:  # Metilendioksi varsa diğer grup yok
                                continue
                            
                            potency = 1.0
                            if "PVP" in scaffold or "PHP" in scaffold:
                                potency *= 1.8
                            if md:
                                potency *= 1.2
                            if group == "F":
                                potency *= 1.3
                            if "pyrrolidino" in n_sub:
                                potency *= 1.5
                            if stereo == "S":
                                potency *= 1.1
                            
                            name_parts = []
                            if stereo:
                                name_parts.append(f"({stereo})")
                            if group:
                                name_parts.append(f"{pos}-{group}")
                            if md:
                                name_parts.append("3,4-MD")
                            name_parts.append(abbrev)
                            if n_sub != "N-Me":
                                name_parts.append(n_sub.replace("N-", "").replace(",", ""))
                            
                            name = "-".join(name_parts) if len(name_parts) > 1 else abbrev
                            compound_id = f"CAT_{name.replace('-', '_').replace('(', '').replace(')', '').replace(',', '')}"
                            
                            if compound_id not in nps_db:
                                mods = [ChemicalModification.ALPHA_SUBSTITUTION]
                                if group == "F":
                                    mods.append(ChemicalModification.HALOGENATION_F)
                                elif group == "Cl":
                                    mods.append(ChemicalModification.HALOGENATION_Cl)
                                elif group == "Br":
                                    mods.append(ChemicalModification.HALOGENATION_Br)
                                elif group == "Me":
                                    mods.append(ChemicalModification.METHYLATION)
                                elif group == "OMe":
                                    mods.append(ChemicalModification.METHOXYLATION)
                                if md:
                                    mods.append(ChemicalModification.METHYLENEDIOXY)
                                if stereo == "R":
                                    mods.append(ChemicalModification.STEREOISOMER_R)
                                elif stereo == "S":
                                    mods.append(ChemicalModification.STEREOISOMER_S)
                                
                                nps_db[compound_id] = NPSDerivative(
                                    compound_id=compound_id,
                                    name_iupac=f"{scaffold} derivative",
                                    name_common=name,
                                    name_turkish=f"{name} (Sentetik Katinon)",
                                    parent_compound="Cathinone",
                                    nps_class=NPSClass.SYNTHETIC_CATHINONES,
                                    modifications=mods,
                                    molecular_formula=f"C{11+len(group)}H{15+len(group)}NO",
                                    molecular_weight=base_mw + (19 if group=="F" else 35 if group=="Cl" else 0),
                                    potency_ratio=round(potency, 2),
                                    receptor_targets=targets,
                                    binding_affinity={t: round(15/potency, 2) for t in targets},
                                    metabolism_half_life=3 + potency * 0.5,
                                    detection_markers=[f"{abbrev}_M1", f"{abbrev}_COOH"],
                                    cpg_markers=["cg03821126", "cg08709672", "cg22132788", "cg14179389"],
                                    legal_status="Liste I",
                                    first_reported="2007-2024",
                                    street_names=[name, "Bath salts", "Flakka" if "PVP" in scaffold else "Meow meow"],
                                    toxicity_notes=f"Stimulan toksisite. Potens: {potency:.1f}x katinon.",
                                    eaa_effect=2.0 + potency * 0.6
                                )
    
    # ========================================================================
    # 3. FENETİLAMİNLER (~250 türev)
    # ========================================================================
    # nrcdnl94
    
    # 2C-x serisi
    two_c_substituents = ["B", "I", "E", "C", "D", "P", "T-2", "T-7", "T-21", "N", "G", "H", "O", "TFM", "YN"]
    
    for sub in two_c_substituents:
        for stereo in ["", "R", "S"]:
            potency = 1.0
            if sub in ["I", "B", "P"]:
                potency *= 1.5
            if sub in ["T-7", "T-21"]:
                potency *= 1.3
            
            name = f"2C-{sub}"
            if stereo:
                name = f"({stereo})-{name}"
            compound_id = f"PEA_2C_{sub.replace('-', '_')}"
            if stereo:
                compound_id += f"_{stereo}"
            
            if compound_id not in nps_db:
                mods = [ChemicalModification.RING_SUBSTITUTION, ChemicalModification.METHOXYLATION]
                if sub in ["B", "Br"]:
                    mods.append(ChemicalModification.HALOGENATION_Br)
                elif sub in ["I"]:
                    mods.append(ChemicalModification.HALOGENATION_I)
                elif sub in ["C", "Cl"]:
                    mods.append(ChemicalModification.HALOGENATION_Cl)
                elif sub in ["F", "TFM"]:
                    mods.append(ChemicalModification.HALOGENATION_F)
                
                nps_db[compound_id] = NPSDerivative(
                    compound_id=compound_id,
                    name_iupac=f"4-substituted-2,5-dimethoxyphenethylamine",
                    name_common=name,
                    name_turkish=f"{name} (Halüsinojen Fenetilamin)",
                    parent_compound="Phenethylamine",
                    nps_class=NPSClass.PHENETHYLAMINES,
                    modifications=mods,
                    molecular_formula="C12H19NO2X",
                    molecular_weight=210 + potency * 20,
                    potency_ratio=round(potency, 2),
                    receptor_targets=["5-HT2A", "5-HT2C"],
                    binding_affinity={"5-HT2A": round(5/potency, 2)},
                    metabolism_half_life=6 + potency * 1.5,
                    detection_markers=[f"2C-{sub}_M1"],
                    cpg_markers=["cg07123182", "cg15768986", "cg22132788"],
                    legal_status="Liste I",
                    first_reported="2003-2024",
                    street_names=[name, "Nexus" if sub=="B" else name],
                    toxicity_notes="Serotonerjik halüsinojen.",
                    eaa_effect=1.5 + potency * 0.3
                )
    
    # NBOMe serisi
    nbome_bases = ["25I", "25B", "25C", "25E", "25D", "25N", "25H", "25T2", "25P", "25G"]
    nbome_types = ["NBOMe", "NBOH", "NBF", "NBCl", "NBBr"]
    
    for base in nbome_bases:
        for nbtype in nbome_types:
            potency = 5.0  # NBOMe'ler çok potent
            if base == "25I":
                potency *= 2.0
            if base == "25N":
                potency *= 1.8
            if nbtype == "NBOH":
                potency *= 0.7
            
            name = f"{base}-{nbtype}"
            compound_id = f"PEA_{name.replace('-', '_')}"
            
            if compound_id not in nps_db:
                nps_db[compound_id] = NPSDerivative(
                    compound_id=compound_id,
                    name_iupac=f"N-benzyl-phenethylamine derivative",
                    name_common=name,
                    name_turkish=f"{name} (NBOMe Serisi)",
                    parent_compound="Phenethylamine",
                    nps_class=NPSClass.PHENETHYLAMINES,
                    modifications=[ChemicalModification.RING_SUBSTITUTION, ChemicalModification.N_ALKYLATION],
                    molecular_formula="C18H22INO3",
                    molecular_weight=420 + potency * 5,
                    potency_ratio=round(potency, 2),
                    receptor_targets=["5-HT2A"],
                    binding_affinity={"5-HT2A": round(0.5/potency, 3)},
                    metabolism_half_life=8 + potency,
                    detection_markers=[f"{base}_M1"],
                    cpg_markers=["cg07123182", "cg15768986", "cg22132788"],
                    legal_status="Liste I (Acil)",
                    first_reported="2010-2024",
                    street_names=[name, "N-bomb", "Smiles"],
                    toxicity_notes=f"ÇOK POTENT! LSD'den {potency:.0f}x daha güçlü. Ölümcül olabilir.",
                    eaa_effect=2.0 + potency * 0.2
                )
    
    # DOx serisi
    dox_subs = ["M", "B", "I", "C", "ET", "N", "PR", "AM", "F", "Cl"]
    
    for sub in dox_subs:
        for stereo in ["", "R", "S"]:
            potency = 1.0
            if sub == "I":
                potency *= 2.0
            if sub == "B":
                potency *= 1.5
            if stereo == "R":
                potency *= 1.2
            
            name = f"DO{sub}"
            if stereo:
                name = f"({stereo})-{name}"
            compound_id = f"PEA_DO{sub}"
            if stereo:
                compound_id += f"_{stereo}"
            
            if compound_id not in nps_db:
                nps_db[compound_id] = NPSDerivative(
                    compound_id=compound_id,
                    name_iupac=f"2,5-dimethoxy-4-substituted amphetamine",
                    name_common=name,
                    name_turkish=f"{name} (DOx Serisi)",
                    parent_compound="Amphetamine",
                    nps_class=NPSClass.PHENETHYLAMINES,
                    modifications=[ChemicalModification.RING_SUBSTITUTION, ChemicalModification.ALPHA_SUBSTITUTION],
                    molecular_formula="C12H19NO2X",
                    molecular_weight=225 + potency * 15,
                    potency_ratio=round(potency, 2),
                    receptor_targets=["5-HT2A", "5-HT2B"],
                    binding_affinity={"5-HT2A": round(3/potency, 2)},
                    metabolism_half_life=12 + potency * 4,
                    detection_markers=[f"DO{sub}_M1"],
                    cpg_markers=["cg07123182", "cg15768986"],
                    legal_status="Liste I",
                    first_reported="1970-2024",
                    street_names=[name, "STP" if sub=="M" else name],
                    toxicity_notes="Çok uzun etkili halüsinojen (16-30 saat).",
                    eaa_effect=1.8 + potency * 0.4
                )
    
    # Substitue amfetaminler
    amp_positions = ["2", "3", "4"]
    amp_groups = ["F", "Cl", "Br", "Me", "OMe", "Et", "CF3"]
    amp_bases = ["amphetamine", "methamphetamine"]
    
    for base in amp_bases:
        abbrev = "A" if base == "amphetamine" else "MA"
        for pos in amp_positions:
            for group in amp_groups:
                for stereo in ["", "R", "S"]:
                    potency = 1.0
                    if group == "F":
                        potency *= 1.3
                    if group == "Cl":
                        potency *= 1.1
                    if pos == "4":
                        potency *= 1.2
                    if base == "methamphetamine":
                        potency *= 1.5
                    
                    name = f"{pos}-{group}-{abbrev}"
                    if stereo:
                        name = f"({stereo})-{name}"
                    compound_id = f"AMP_{pos}_{group}_{abbrev}"
                    if stereo:
                        compound_id += f"_{stereo}"
                    
                    if compound_id not in nps_db:
                        mods = [ChemicalModification.RING_SUBSTITUTION]
                        if group == "F":
                            mods.append(ChemicalModification.HALOGENATION_F)
                        elif group == "Cl":
                            mods.append(ChemicalModification.HALOGENATION_Cl)
                        elif group == "Br":
                            mods.append(ChemicalModification.HALOGENATION_Br)
                        elif group == "Me":
                            mods.append(ChemicalModification.METHYLATION)
                        elif group == "OMe":
                            mods.append(ChemicalModification.METHOXYLATION)
                        
                        nps_db[compound_id] = NPSDerivative(
                            compound_id=compound_id,
                            name_iupac=f"{pos}-substituted-{base}",
                            name_common=name,
                            name_turkish=f"{name} (Substitue Amfetamin)",
                            parent_compound="Amphetamine",
                            nps_class=NPSClass.PHENETHYLAMINES,
                            modifications=mods,
                            molecular_formula="C9H13NX",
                            molecular_weight=135 + (19 if group=="F" else 35 if group=="Cl" else 15),
                            potency_ratio=round(potency, 2),
                            receptor_targets=["DAT", "NET", "SERT"],
                            binding_affinity={"DAT": round(10/potency, 2)},
                            metabolism_half_life=8 + potency * 2,
                            detection_markers=[f"{abbrev}_{group}_M1"],
                            cpg_markers=["cg03821126", "cg08709672"],
                            legal_status="Liste I",
                            first_reported="2010-2024",
                            street_names=[name, f"{group}-speed"],
                            toxicity_notes="Amfetamin benzeri kardiyotoksisite.",
                            eaa_effect=3.0 + potency * 0.5
                        )
    
    # ========================================================================
    # 4. SENTETİK OPİOİDLER (~200 türev)
    # ========================================================================
    # nrcdnl94
    
    # Fentanil analogları - N-asil zincir modifikasyonları
    fent_acyl_chains = ["acetyl", "propionyl", "butyryl", "isobutyryl", "valeryl", "isovaleryl", 
                        "hexanoyl", "heptanoyl", "crotonyl", "cyclopropyl", "cyclobutyl",
                        "benzoyl", "phenylacetyl", "furanoyl", "thiophenecarboxyl"]
    
    # Fentanil analogları - halka modifikasyonları
    fent_ring_mods = ["", "2-F", "3-F", "4-F", "2-Cl", "3-Cl", "4-Cl", 
                      "2-Me", "3-Me", "4-Me", "2-OMe", "4-OMe", "3,4-diF"]
    
    # Fentanil analogları - piperidin modifikasyonları
    fent_piperidine_mods = ["", "3-Me-cis", "3-Me-trans", "4-Me", "3-allyl"]
    
    for acyl in fent_acyl_chains:
        for ring_mod in fent_ring_mods[:8]:  # İlk 8'i
            for pip_mod in fent_piperidine_mods[:3]:  # İlk 3'ü
                potency = 1.0  # Fentanile göre
                
                # Potens hesaplama
                if acyl == "acetyl":
                    potency *= 0.15
                elif acyl == "butyryl":
                    potency *= 0.25
                elif acyl in ["cyclopropyl", "furanoyl"]:
                    potency *= 1.2
                
                if "F" in ring_mod:
                    potency *= 1.3
                if "4-F" in ring_mod:
                    potency *= 1.5
                
                if "3-Me-trans" in pip_mod:
                    potency *= 6.0
                elif "3-Me-cis" in pip_mod:
                    potency *= 3.0
                
                name_parts = []
                if ring_mod:
                    name_parts.append(ring_mod)
                name_parts.append(acyl.replace("yl", ""))
                name_parts.append("fentanyl")
                if pip_mod:
                    name_parts.append(pip_mod)
                
                name = "-".join(name_parts)
                compound_id = f"OPI_FENT_{acyl[:4]}_{ring_mod.replace('-', '').replace(',', '')}_{pip_mod.replace('-', '')}"
                compound_id = compound_id.rstrip("_")
                
                if compound_id not in nps_db and len(compound_id) < 60:
                    mods = [ChemicalModification.N_ALKYLATION]
                    if "F" in ring_mod:
                        mods.append(ChemicalModification.HALOGENATION_F)
                    if "Cl" in ring_mod:
                        mods.append(ChemicalModification.HALOGENATION_Cl)
                    if "trans" in pip_mod:
                        mods.append(ChemicalModification.TRANS_ISOMER)
                    elif "cis" in pip_mod:
                        mods.append(ChemicalModification.CIS_ISOMER)
                    
                    nps_db[compound_id] = NPSDerivative(
                        compound_id=compound_id,
                        name_iupac=f"Fentanyl analog: {acyl}",
                        name_common=name,
                        name_turkish=f"{name} (Fentanil Analoğu)",
                        parent_compound="Fentanyl",
                        nps_class=NPSClass.SYNTHETIC_OPIOIDS,
                        modifications=mods,
                        molecular_formula="C22H28N2O",
                        molecular_weight=336 + len(acyl) * 2,
                        potency_ratio=round(potency, 2),
                        receptor_targets=["OPRM1", "OPRK1", "OPRD1"],
                        binding_affinity={"OPRM1": round(0.39/potency, 3) if potency > 0 else 0.39},
                        metabolism_half_life=2 + potency * 0.1,
                        detection_markers=["norfentanyl", f"{acyl[:4]}_M1"],
                        cpg_markers=["cg10406920", "cg15768986", "cg07123182"],
                        legal_status="Liste I (Acil Kontrol)",
                        first_reported="2012-2024",
                        street_names=[name, "China White" if potency > 10 else name],
                        toxicity_notes=f"Morfin eşdeğeri: {potency*100:.0f}x. DOZ AŞIMI RİSKİ ÇOK YÜKSEK!" if potency > 1 else f"Potens: {potency:.2f}x fentanil",
                        eaa_effect=4.0 + np.log10(max(potency, 0.1) + 1) * 1.5
                    )
    
    # Nitazen serisi (Benzimidazol opioidleri)
    nitazene_bases = ["etonitazene", "isotonitazene", "metonitazene", "protonitazene", 
                      "butonitazene", "flunitazene", "clonitazene", "N-desethyl-isotonitazene"]
    nitazene_mods = ["", "N-pyrrolidino", "N-piperidino", "5-amino", "4-chloro", "4-fluoro"]
    
    for base in nitazene_bases:
        for mod in nitazene_mods[:4]:
            potency = 100.0  # Morfine göre
            if "eto" in base:
                potency *= 10.0
            elif "isoto" in base:
                potency *= 5.0
            elif "flu" in base:
                potency *= 3.0
            elif "proto" in base:
                potency *= 2.0
            
            if "pyrrolidino" in mod:
                potency *= 0.8
            if "fluoro" in mod:
                potency *= 1.2
            
            name = base
            if mod:
                name = f"{mod}-{base}"
            compound_id = f"OPI_NIT_{base[:6]}_{mod.replace('-', '')}"
            compound_id = compound_id.rstrip("_")
            
            if compound_id not in nps_db:
                nps_db[compound_id] = NPSDerivative(
                    compound_id=compound_id,
                    name_iupac=f"Benzimidazole opioid: {base}",
                    name_common=name,
                    name_turkish=f"{name} (Nitazen Serisi)",
                    parent_compound="Benzimidazole",
                    nps_class=NPSClass.SYNTHETIC_OPIOIDS,
                    modifications=[ChemicalModification.RING_FUSION, ChemicalModification.N_ALKYLATION],
                    molecular_formula="C23H30N4O3",
                    molecular_weight=410,
                    potency_ratio=round(potency, 1),
                    receptor_targets=["OPRM1"],
                    binding_affinity={"OPRM1": round(0.01/potency*100, 4)},
                    metabolism_half_life=3,
                    detection_markers=[f"{base[:4]}_M1"],
                    cpg_markers=["cg10406920", "cg15768986"],
                    legal_status="Liste I (Acil Kontrol)",
                    first_reported="2019-2024",
                    street_names=[name, "ISO" if "iso" in base else name],
                    toxicity_notes=f"AŞIRI TEHLİKELİ! Morfinden {potency:.0f}x güçlü!",
                    eaa_effect=5.0 + np.log10(potency) * 0.5
                )
    
    # U-serisi ve diğer sentetik opioidler
    u_series = [
        ("U-47700", 7.5, "benzamide"),
        ("U-49900", 5.0, "benzamide-chloro"),
        ("U-50488", 0.5, "kappa-selective"),
        ("U-51754", 10.0, "benzamide-fluoro"),
        ("U-77891", 3.0, "benzamide-methyl"),
        ("AH-7921", 1.0, "aminocyclohexane"),
        ("MT-45", 0.3, "piperazine"),
        ("AP-237", 3.0, "bucinnazine"),
        ("Brorphine", 15.0, "brominated"),
        ("2-Methyl-AP-237", 4.0, "methyl-bucinnazine"),
        ("Dipyanone", 2.5, "diphenyl"),
        ("Isopropylphenidate", 0.1, "phenidate")
    ]
    
    for name, potency, desc in u_series:
        for mod in ["", "4-F", "4-Cl", "3-Me"]:
            full_name = name
            if mod:
                full_name = f"{mod}-{name}"
            compound_id = f"OPI_{name.replace('-', '_')}_{mod.replace('-', '')}"
            compound_id = compound_id.rstrip("_")
            
            mod_potency = potency
            if "F" in mod:
                mod_potency *= 1.3
            
            if compound_id not in nps_db:
                nps_db[compound_id] = NPSDerivative(
                    compound_id=compound_id,
                    name_iupac=f"Synthetic opioid: {desc}",
                    name_common=full_name,
                    name_turkish=f"{full_name} (Sentetik Opioid)",
                    parent_compound="Synthetic",
                    nps_class=NPSClass.SYNTHETIC_OPIOIDS,
                    modifications=[ChemicalModification.RING_SUBSTITUTION],
                    molecular_formula="C17H22ClNO",
                    molecular_weight=290,
                    potency_ratio=round(mod_potency, 2),
                    receptor_targets=["OPRM1", "OPRK1"],
                    binding_affinity={"OPRM1": round(5/mod_potency, 2)},
                    metabolism_half_life=4,
                    detection_markers=[f"{name[:3]}_M1"],
                    cpg_markers=["cg10406920", "cg15768986"],
                    legal_status="Liste I",
                    first_reported="2015-2024",
                    street_names=[full_name, "Pink" if "47700" in name else full_name],
                    toxicity_notes=f"Morfin eşdeğeri: {mod_potency:.1f}x",
                    eaa_effect=3.5 + mod_potency * 0.2
                )
    
    # ========================================================================
    # 5. TRİPTAMİNLER (~150 türev)
    # ========================================================================
    # nrcdnl94
    
    # N-substitüsyonlar
    trypt_n_subs = ["DMT", "DET", "DPT", "DiPT", "MiPT", "DBT", "EPT", "MPT", "DALT", "MALT"]
    # 4- ve 5- pozisyon modifikasyonları
    trypt_ring_mods = ["", "4-HO", "4-AcO", "4-PO", "5-MeO", "5-HO", "5-Br", "6-F", "7-Et"]
    # Alfa substitüsyonlar
    trypt_alpha = ["", "α-Me", "α-Et"]
    
    for n_sub in trypt_n_subs:
        for ring_mod in trypt_ring_mods:
            for alpha in trypt_alpha[:2]:
                potency = 1.0
                if n_sub == "DMT":
                    potency *= 1.0
                elif n_sub in ["DPT", "DiPT"]:
                    potency *= 0.8
                
                if "5-MeO" in ring_mod:
                    potency *= 2.0
                if "4-HO" in ring_mod or "4-AcO" in ring_mod:
                    potency *= 1.0
                if alpha == "α-Me":
                    potency *= 1.2
                
                name_parts = []
                if ring_mod:
                    name_parts.append(ring_mod)
                if alpha:
                    name_parts.append(alpha)
                name_parts.append(n_sub)
                
                name = "-".join(name_parts)
                compound_id = f"TRP_{ring_mod.replace('-', '')}_{alpha.replace('-', '').replace('α', 'a')}_{n_sub}"
                compound_id = compound_id.replace("__", "_").strip("_")
                
                if compound_id not in nps_db:
                    mods = [ChemicalModification.N_ALKYLATION]
                    if "HO" in ring_mod:
                        mods.append(ChemicalModification.HYDROXYLATION)
                    if "MeO" in ring_mod:
                        mods.append(ChemicalModification.METHOXYLATION)
                    if "AcO" in ring_mod:
                        mods.append(ChemicalModification.RING_SUBSTITUTION)
                    if alpha:
                        mods.append(ChemicalModification.ALPHA_SUBSTITUTION)
                    
                    nps_db[compound_id] = NPSDerivative(
                        compound_id=compound_id,
                        name_iupac=f"Tryptamine derivative: {n_sub}",
                        name_common=name,
                        name_turkish=f"{name} (Triptamin)",
                        parent_compound="Tryptamine",
                        nps_class=NPSClass.TRYPTAMINES,
                        modifications=mods,
                        molecular_formula="C12H16N2O",
                        molecular_weight=188 + len(ring_mod) * 5,
                        potency_ratio=round(potency, 2),
                        receptor_targets=["5-HT2A", "5-HT1A", "Sigma-1"],
                        binding_affinity={"5-HT2A": round(10/potency, 2)},
                        metabolism_half_life=4 + potency * 2,
                        detection_markers=[f"{n_sub}_M1"],
                        cpg_markers=["cg07123182", "cg15768986", "cg22132788"],
                        legal_status="Liste I" if n_sub != "DMT" else "Liste I (Endojen)",
                        first_reported="1990-2024",
                        street_names=[name, "Spirit molecule" if "DMT" in n_sub else name],
                        toxicity_notes="Serotonerjik halüsinojen. MAO-I etkileşimi riski.",
                        eaa_effect=1.2 + potency * 0.3
                    )
    
    # ========================================================================
    # 6. TASARIM BENZODİAZEPİNLERİ (~120 türev)
    # ========================================================================
    # nrcdnl94
    
    benzo_scaffolds = ["triazolo", "tieno", "imidazo", "oxazolo", "pyrazolo"]
    benzo_core_mods = ["", "7-Cl", "7-Br", "7-F", "7-NO2", "8-Cl", "8-Br"]
    benzo_phenyl_mods = ["", "2'-F", "2'-Cl", "4'-F", "2',4'-diF"]
    benzo_n_subs = ["", "N1-Me", "N1-Et", "N1-iPr"]
    
    for scaffold in benzo_scaffolds:
        for core_mod in benzo_core_mods:
            for phenyl_mod in benzo_phenyl_mods[:3]:
                for n_sub in benzo_n_subs[:2]:
                    potency = 1.0
                    if scaffold == "triazolo":
                        potency *= 2.0
                    elif scaffold == "tieno":
                        potency *= 1.0
                    
                    if "Cl" in core_mod:
                        potency *= 1.5
                    if "Br" in core_mod:
                        potency *= 1.8
                    if "F" in phenyl_mod:
                        potency *= 1.3
                    
                    name_parts = []
                    if core_mod:
                        name_parts.append(core_mod)
                    if phenyl_mod:
                        name_parts.append(phenyl_mod)
                    name_parts.append(f"{scaffold}BZD")
                    if n_sub:
                        name_parts.append(n_sub)
                    
                    name = "-".join(name_parts)
                    phenyl_clean = phenyl_mod.replace("-", "").replace(",", "").replace("'", "")
                    core_clean = core_mod.replace("-", "").replace(",", "")
                    compound_id = f"BZD_{scaffold[:5]}_{core_clean}_{phenyl_clean}"
                    compound_id = compound_id.rstrip("_")
                    
                    if compound_id not in nps_db and len(compound_id) < 50:
                        mods = [ChemicalModification.RING_FUSION]
                        if "F" in core_mod or "F" in phenyl_mod:
                            mods.append(ChemicalModification.HALOGENATION_F)
                        if "Cl" in core_mod or "Cl" in phenyl_mod:
                            mods.append(ChemicalModification.HALOGENATION_Cl)
                        if "Br" in core_mod:
                            mods.append(ChemicalModification.HALOGENATION_Br)
                        
                        nps_db[compound_id] = NPSDerivative(
                            compound_id=compound_id,
                            name_iupac=f"Designer benzodiazepine: {scaffold}",
                            name_common=name,
                            name_turkish=f"{name} (Tasarım Benzodiazepin)",
                            parent_compound="Benzodiazepine",
                            nps_class=NPSClass.BENZODIAZEPINES_NPS,
                            modifications=mods,
                            molecular_formula="C17H13ClFN3O",
                            molecular_weight=330 + potency * 10,
                            potency_ratio=round(potency, 2),
                            receptor_targets=["GABA-A"],
                            binding_affinity={"GABA-A": round(5/potency, 2)},
                            metabolism_half_life=12 + potency * 8,
                            detection_markers=[f"{scaffold[:4]}_M1"],
                            cpg_markers=["cg17739917", "cg06690548", "cg12803068"],
                            legal_status="Liste IV" if potency < 1.5 else "Liste I",
                            first_reported="2010-2024",
                            street_names=[name, "Designer benzos"],
                            toxicity_notes=f"Diazepam eşdeğeri: {potency:.1f}x. Solunum depresyonu riski.",
                            eaa_effect=1.5 + potency * 0.3
                        )
    
    # Spesifik tasarım benzodiazepinler
    specific_bzds = [
        ("Flualprazolam", 2.0), ("Clonazolam", 2.5), ("Flubromazolam", 4.0),
        ("Flunitrazolam", 3.0), ("Deschloroetizolam", 0.8), ("Diclazepam", 1.5),
        ("Flubromazepam", 2.0), ("Meclonazepam", 1.2), ("Phenazepam", 1.8),
        ("Pyrazolam", 1.0), ("Nitrazolam", 1.5), ("Bromazolam", 2.2),
        ("Nifoxipam", 1.5), ("Metizolam", 0.9), ("Fluclotizolam", 1.8),
        ("Adinazolam", 1.0), ("Gidazepam", 0.5), ("Cinazepam", 0.8),
        ("Norflurazepam", 0.8), ("Delorazepam", 1.0), ("Ketazolam", 0.6)
    ]
    
    for name, potency in specific_bzds:
        compound_id = f"BZD_{name}"
        if compound_id not in nps_db:
            nps_db[compound_id] = NPSDerivative(
                compound_id=compound_id,
                name_iupac=f"Designer benzodiazepine: {name}",
                name_common=name,
                name_turkish=f"{name} (Tasarım Benzodiazepin)",
                parent_compound="Benzodiazepine",
                nps_class=NPSClass.BENZODIAZEPINES_NPS,
                modifications=[ChemicalModification.RING_FUSION, ChemicalModification.HALOGENATION_F],
                molecular_formula="C17H13ClFN3O",
                molecular_weight=320 + potency * 15,
                potency_ratio=potency,
                receptor_targets=["GABA-A"],
                binding_affinity={"GABA-A": round(5/potency, 2)},
                metabolism_half_life=15 + potency * 10,
                detection_markers=[f"{name[:4]}_M1"],
                cpg_markers=["cg17739917", "cg06690548"],
                legal_status="Liste I",
                first_reported="2010-2024",
                street_names=[name],
                toxicity_notes=f"Diazepam eşdeğeri: {potency:.1f}x",
                eaa_effect=1.5 + potency * 0.3
            )
    
    # ========================================================================
    # 7. ARİLSİKLOHEKZİLAMİNLER (~100 türev)
    # ========================================================================
    # nrcdnl94
    
    ace_scaffolds = ["ketamine", "PCP", "PCE", "PCM", "PCPy", "PCPr"]
    ace_aryl_mods = ["", "2-F", "3-F", "2-Cl", "3-Cl", "2-Me", "3-Me", "2-MeO", "3-MeO", "4-MeO", "2-CF3"]
    ace_amine_mods = ["", "N-Et", "N-Me", "N-allyl"]
    ace_ketone = [True, False]
    
    for scaffold in ace_scaffolds:
        for aryl in ace_aryl_mods:
            for amine in ace_amine_mods[:2]:
                for has_ketone in ace_ketone[:1]:  # Sadece keto
                    potency = 1.0
                    if scaffold == "PCP":
                        potency *= 1.5
                    if "MeO" in aryl:
                        potency *= 1.8
                    if "F" in aryl:
                        potency *= 1.2
                    if not has_ketone:
                        potency *= 0.7
                    
                    name_parts = []
                    if aryl:
                        name_parts.append(aryl)
                    if amine:
                        name_parts.append(amine)
                    if not has_ketone and "ketamine" in scaffold:
                        name_parts.append("deoxo")
                    name_parts.append(scaffold)
                    
                    name = "-".join(name_parts)
                    compound_id = f"DIS_{scaffold[:3]}_{aryl.replace('-', '')}_{amine.replace('-', '')}"
                    compound_id = compound_id.rstrip("_")
                    
                    if compound_id not in nps_db and len(compound_id) < 40:
                        mods = [ChemicalModification.RING_SUBSTITUTION]
                        if "F" in aryl:
                            mods.append(ChemicalModification.HALOGENATION_F)
                        if "Cl" in aryl:
                            mods.append(ChemicalModification.HALOGENATION_Cl)
                        if "MeO" in aryl:
                            mods.append(ChemicalModification.METHOXYLATION)
                        
                        nps_db[compound_id] = NPSDerivative(
                            compound_id=compound_id,
                            name_iupac=f"Arylcyclohexylamine: {scaffold}",
                            name_common=name,
                            name_turkish=f"{name} (Disosiyatif)",
                            parent_compound="PCP/Ketamine",
                            nps_class=NPSClass.ARYLCYCLOHEXYLAMINES,
                            modifications=mods,
                            molecular_formula="C13H17ClNO",
                            molecular_weight=240 + potency * 10,
                            potency_ratio=round(potency, 2),
                            receptor_targets=["NMDA", "D2", "SERT"],
                            binding_affinity={"NMDA": round(50/potency, 1)},
                            metabolism_half_life=3 + potency * 1.5,
                            detection_markers=[f"{scaffold[:3]}_nor"],
                            cpg_markers=["cg07123182", "cg15768986", "cg17739917"],
                            legal_status="Liste II" if scaffold == "ketamine" else "Liste I",
                            first_reported="2000-2024",
                            street_names=[name, "Special K" if "ketamine" in scaffold else "Angel dust"],
                            toxicity_notes="NMDA antagonisti. Disosiyatif etki.",
                            eaa_effect=2.0 + potency * 0.4
                        )
    
    # Spesifik disosiyatifler
    specific_disso = [
        ("MXE", "Methoxetamine", 1.5), ("MXiPr", "Methoxisopropamine", 1.2),
        ("MXPr", "Methoxpropamine", 1.0), ("DMXE", "Dimethoxetamine", 1.4),
        ("3-HO-PCP", "3-hydroxyphencyclidine", 1.5), ("3-MeO-PCP", "3-methoxyphencyclidine", 1.8),
        ("3-MeO-PCE", "3-methoxyeticyclidine", 1.2), ("3-MeO-PCMo", "3-methoxy-morpholino", 1.0),
        ("3-Cl-PCP", "3-chlorophencyclidine", 1.6), ("3-F-PCP", "3-fluorophencyclidine", 1.4),
        ("O-PCE", "2-oxo-eticyclidine", 1.3), ("2-FDCK", "2-fluorodeschloroketamine", 0.9),
        ("2-BDCK", "2-bromodeschloroketamine", 0.8), ("DCK", "Deschloroketamine", 0.7),
        ("HXE", "Hydroxetamine", 0.8), ("DMXE", "Deoxymethoxetamine", 1.4),
        ("Tiletamine", "Thiophene-ketamine", 1.5), ("NPDCK", "N-propyl-DCK", 1.1)
    ]
    
    for name, iupac, potency in specific_disso:
        compound_id = f"DIS_{name.replace('-', '_')}"
        if compound_id not in nps_db:
            nps_db[compound_id] = NPSDerivative(
                compound_id=compound_id,
                name_iupac=iupac,
                name_common=name,
                name_turkish=f"{name} (Disosiyatif)",
                parent_compound="PCP/Ketamine",
                nps_class=NPSClass.ARYLCYCLOHEXYLAMINES,
                modifications=[ChemicalModification.RING_SUBSTITUTION, ChemicalModification.METHOXYLATION],
                molecular_formula="C14H19NO2",
                molecular_weight=233 + potency * 15,
                potency_ratio=potency,
                receptor_targets=["NMDA", "SERT"],
                binding_affinity={"NMDA": round(40/potency, 1)},
                metabolism_half_life=4 + potency * 2,
                detection_markers=[f"{name[:3]}_M1"],
                cpg_markers=["cg07123182", "cg15768986"],
                legal_status="Liste I",
                first_reported="2010-2024",
                street_names=[name],
                toxicity_notes=f"Ketamin benzeri disosiyatif.",
                eaa_effect=2.0 + potency * 0.4
            )
    
    # ========================================================================
    # 8. PİPERAZİNLER (~60 türev)
    # ========================================================================
    # nrcdnl94
    
    pip_bases = ["BZP", "TFMPP", "mCPP", "pCPP", "MeOPP", "pFPP", "DBZP", "oMePP"]
    pip_ring_mods = ["", "4-F", "4-Cl", "4-Br", "3-Me", "4-Me", "3-OMe", "4-OMe", "3-CF3", "4-CF3"]
    
    for base in pip_bases:
        for mod in pip_ring_mods:
            potency = 1.0
            if "TFMPP" in base:
                potency *= 0.7
            if "BZP" in base:
                potency *= 1.0
            if "CF3" in mod:
                potency *= 1.3
            if "F" in mod:
                potency *= 1.2
            
            name = base
            if mod:
                name = f"{mod}-{base}"
            compound_id = f"PIP_{base}_{mod.replace('-', '')}"
            compound_id = compound_id.rstrip("_")
            
            if compound_id not in nps_db:
                mods = [ChemicalModification.RING_SUBSTITUTION]
                if "F" in mod or "F" in base:
                    mods.append(ChemicalModification.HALOGENATION_F)
                if "Cl" in mod:
                    mods.append(ChemicalModification.HALOGENATION_Cl)
                if "Br" in mod:
                    mods.append(ChemicalModification.HALOGENATION_Br)
                
                nps_db[compound_id] = NPSDerivative(
                    compound_id=compound_id,
                    name_iupac=f"Piperazine derivative: {base}",
                    name_common=name,
                    name_turkish=f"{name} (Piperazin)",
                    parent_compound="Piperazine",
                    nps_class=NPSClass.PIPERAZINES,
                    modifications=mods,
                    molecular_formula="C11H14N2",
                    molecular_weight=175 + potency * 20,
                    potency_ratio=round(potency, 2),
                    receptor_targets=["5-HT2A", "DAT", "SERT"],
                    binding_affinity={"5-HT2A": round(100/potency, 1)},
                    metabolism_half_life=5 + potency,
                    detection_markers=[f"{base}_M1"],
                    cpg_markers=["cg03821126", "cg07123182"],
                    legal_status="Liste I",
                    first_reported="2004-2024",
                    street_names=[name, "Party pills", "Legal X"],
                    toxicity_notes="Stimulan + serotonerjik etki.",
                    eaa_effect=1.5 + potency * 0.3
                )
    
    # ========================================================================
    # 9. AMİNOİNDANLAR (~40 türev)
    # ========================================================================
    # nrcdnl94
    
    aminoindans = ["AI", "2-AI", "5-IAI", "5,6-MDAI", "MDAI", "MMAI", "MEAI", "ETAI"]
    ai_mods = ["", "5-F", "6-F", "5-Cl", "6-Cl", "5-Me", "6-Me", "5-OMe"]
    
    for base in aminoindans:
        for mod in ai_mods[:5]:
            potency = 1.0
            if "MDAI" in base:
                potency *= 1.5
            if "IAI" in base:
                potency *= 1.2
            if "F" in mod:
                potency *= 1.1
            
            name = base
            if mod:
                name = f"{mod}-{base}"
            compound_id = f"AI_{base.replace(',', '')}_{mod.replace('-', '')}"
            compound_id = compound_id.rstrip("_")
            
            if compound_id not in nps_db:
                nps_db[compound_id] = NPSDerivative(
                    compound_id=compound_id,
                    name_iupac=f"Aminoindane: {base}",
                    name_common=name,
                    name_turkish=f"{name} (Aminoindan)",
                    parent_compound="Aminoindane",
                    nps_class=NPSClass.AMINOINDANES,
                    modifications=[ChemicalModification.RING_SUBSTITUTION],
                    molecular_formula="C9H11N",
                    molecular_weight=133 + potency * 15,
                    potency_ratio=round(potency, 2),
                    receptor_targets=["SERT", "DAT"],
                    binding_affinity={"SERT": round(50/potency, 1)},
                    metabolism_half_life=4 + potency,
                    detection_markers=[f"{base[:3]}_M1"],
                    cpg_markers=["cg03821126", "cg08709672"],
                    legal_status="Liste I",
                    first_reported="2010-2024",
                    street_names=[name, "Sparkle"],
                    toxicity_notes="MDMA benzeri entaktojen.",
                    eaa_effect=1.8 + potency * 0.4
                )
    
    return nps_db


def get_nps_statistics() -> Dict:
    """NPS Veritabanı İstatistikleri - nrcdnl94"""
    nps_db = generate_nps_database()
    
    stats = {
        "total_compounds": len(nps_db),
        "by_class": {},
        "by_modification": {},
        "potency_distribution": {
            "low (<1.0)": 0,
            "moderate (1.0-2.0)": 0,
            "high (2.0-5.0)": 0,
            "very_high (5.0-50)": 0,
            "extreme (>50)": 0
        },
        "most_potent": [],
        "by_legal_status": {}
    }
    
    for compound in nps_db.values():
        # Sınıf bazında sayım
        class_name = compound.nps_class.value
        stats["by_class"][class_name] = stats["by_class"].get(class_name, 0) + 1
        
        # Modifikasyon bazında sayım
        for mod in compound.modifications:
            mod_name = mod.value
            stats["by_modification"][mod_name] = stats["by_modification"].get(mod_name, 0) + 1
        
        # Yasal durum
        legal = compound.legal_status
        stats["by_legal_status"][legal] = stats["by_legal_status"].get(legal, 0) + 1
        
        # Potens dağılımı
        p = compound.potency_ratio
        if p < 1.0:
            stats["potency_distribution"]["low (<1.0)"] += 1
        elif p < 2.0:
            stats["potency_distribution"]["moderate (1.0-2.0)"] += 1
        elif p < 5.0:
            stats["potency_distribution"]["high (2.0-5.0)"] += 1
        elif p < 50:
            stats["potency_distribution"]["very_high (5.0-50)"] += 1
        else:
            stats["potency_distribution"]["extreme (>50)"] += 1
            stats["most_potent"].append({
                "name": compound.name_common,
                "potency": compound.potency_ratio,
                "class": class_name
            })
    
    # En potent maddeleri sırala
    stats["most_potent"] = sorted(stats["most_potent"], key=lambda x: x["potency"], reverse=True)[:15]
    
    return stats


def get_modification_examples() -> Dict[str, List[Dict]]:
    """Her modifikasyon tipi için örnekler - nrcdnl94"""
    nps_db = generate_nps_database()
    
    examples = {}
    for compound in nps_db.values():
        for mod in compound.modifications:
            mod_name = mod.value
            if mod_name not in examples:
                examples[mod_name] = []
            if len(examples[mod_name]) < 8:
                examples[mod_name].append({
                    "compound": compound.name_common,
                    "parent": compound.parent_compound,
                    "potency_change": f"{compound.potency_ratio}x",
                    "class": compound.nps_class.value
                })
    
    return examples


# nrcdnl94 - End of NPS Derivatives Module
# Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır - All Rights Reserved
