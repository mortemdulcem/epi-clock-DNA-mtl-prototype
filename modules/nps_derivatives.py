"""
================================================================================
EpiClock Prototype v4.0 - NPS (Novel Psychoactive Substances) Derivatives Module
================================================================================
Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır
Digital Signature: nrcdnl94
ALL RIGHTS RESERVED - PROPRIETARY AND CONFIDENTIAL

NPS ÇEŞİTLİLİĞİ - KİMYASAL MODİFİKASYON PRENSİPLERİ
============================================================================
1. Fonksiyonel Grup Değişiklikleri (Amin, Hidroksil, Metoksi, Halojenler)
2. Halka Substitüsyonları (Aromatik, İndol, İndazol, Naftil)
3. Yan Zincir Uzunluğu ve Doygunluk
4. Stereoizomer ve Konformasyon Değişiklikleri

Referanslar:
- UNODC Early Warning Advisory on NPS
- EMCDDA NPS Database
- Cayman Chemical NPS Reference Library
- DEA Emerging Threat Reports
================================================================================
"""

# nrcdnl94 - Author Signature - Do Not Remove

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np

# nrcdnl94
class NPSClass(Enum):
    """NPS Ana Sınıfları - UNODC Sınıflandırması"""
    SYNTHETIC_CANNABINOIDS = "Sentetik Kannabinoidler"
    SYNTHETIC_CATHINONES = "Sentetik Katinonlar"
    PHENETHYLAMINES = "Fenetiilaminler"
    SYNTHETIC_OPIOIDS = "Sentetik Opioidler"
    TRYPTAMINES = "Triptaminler"
    PIPERAZINES = "Piperazinler"
    BENZODIAZEPINES_NPS = "Tasarım Benzodiazepinleri"
    ARYLCYCLOHEXYLAMINES = "Arilsiklohekzilaminler"
    AMINOINDANES = "Aminoindanlar"
    PLANTS_BASED_NPS = "Bitki Bazlı NPS"

# nrcdnl94
class ChemicalModification(Enum):
    """Kimyasal Modifikasyon Türleri"""
    HALOGENATION = "Halojenasyon (F, Cl, Br, I)"
    METHYLATION = "Metilasyon (-CH3)"
    HYDROXYLATION = "Hidroksilasyon (-OH)"
    METHOXYLATION = "Metoksilasyon (-OCH3)"
    FLUORINATION = "Florinasyon (-F)"
    CHAIN_EXTENSION = "Zincir Uzatma"
    CHAIN_SHORTENING = "Zincir Kısaltma"
    RING_SUBSTITUTION = "Halka Substitüsyonu"
    N_ALKYLATION = "N-Alkilasyon"
    ALPHA_SUBSTITUTION = "Alfa Substitüsyon"
    STEREOISOMER = "Stereoizomer Değişikliği"

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
    potency_ratio: float  # Parent'a göre potens oranı
    receptor_targets: List[str]
    binding_affinity: Dict[str, float]  # Ki değerleri (nM)
    metabolism_half_life: float  # Saat
    detection_markers: List[str]
    cpg_markers: List[str]
    legal_status: str
    first_reported: str
    street_names: List[str]
    toxicity_notes: str
    eaa_effect: float  # Epigenetik yaş ivmelenmesi


def generate_nps_database() -> Dict[str, NPSDerivative]:
    """
    NPS Türev Veritabanı - Kimyasal Modifikasyon Prensiplerine Göre
    2500+ Türev
    nrcdnl94
    """
    
    nps_db = {}
    
    # ========================================================================
    # 1. SENTETİK KANNABİNOİDLER - İNDOL/İNDAZOL TÜREVLERİ
    # ========================================================================
    # Temel iskeletler: JWH, AM, UR, PB, XLR, AKB, 5F-AKB, MDMB, ADB, AMB, EMB
    
    # JWH Serisi (John W. Huffman) - nrcdnl94
    jwh_series = [
        # JWH-018 ve türevleri (yan zincir modifikasyonları)
        ("JWH-018", "N-pentylindole", 1.0, ["CB1: 9.0", "CB2: 2.9"]),
        ("JWH-019", "N-hexylindole", 0.9, ["CB1: 9.8", "CB2: 5.5"]),  # +1 karbon
        ("JWH-020", "N-heptylindole", 0.85, ["CB1: 12.0", "CB2: 7.0"]),  # +2 karbon
        ("JWH-073", "N-butylindole", 1.1, ["CB1: 8.9", "CB2: 38.0"]),  # -1 karbon
        ("JWH-081", "4-methoxynaphthyl", 1.2, ["CB1: 1.2", "CB2: 12.4"]),  # Metoksi ekleme
        ("JWH-122", "4-methylnaphthyl", 1.3, ["CB1: 0.69", "CB2: 1.2"]),  # Metil ekleme
        ("JWH-200", "morpholinyl ethyl", 0.7, ["CB1: 42.0", "CB2: 81.0"]),  # Morfolino grup
        ("JWH-210", "4-ethylnaphthyl", 1.4, ["CB1: 0.46", "CB2: 0.69"]),  # Etil ekleme
        ("JWH-250", "2-methoxyphenyl", 0.8, ["CB1: 11.0", "CB2: 33.0"]),  # Fenilmetoksi
        ("JWH-251", "2-methylphenyl", 0.75, ["CB1: 29.0", "CB2: 146.0"]),  # Fenilmetil
    ]
    
    # 5-Fluoro türevleri (Florinasyon) - nrcdnl94
    fluoro_cannabinoids = [
        ("5F-AKB-48", "5-fluoro-APINACA", 2.5, ["CB1: 0.5", "CB2: 0.9"]),
        ("5F-PB-22", "5-fluoro-quinolinyl", 3.0, ["CB1: 0.4", "CB2: 0.6"]),
        ("5F-AMB", "5-fluoro-AMB", 2.8, ["CB1: 0.3", "CB2: 0.5"]),
        ("5F-MDMB-PINACA", "5-fluoro-MDMB", 4.0, ["CB1: 0.1", "CB2: 0.2"]),
        ("5F-MDMB-PICA", "5-fluoro-indole-3-carboxamide", 3.5, ["CB1: 0.15", "CB2: 0.25"]),
        ("5F-ADB", "5-fluoro-ADB", 3.8, ["CB1: 0.2", "CB2: 0.3"]),
        ("5F-EMB-PINACA", "5-fluoro-EMB", 2.2, ["CB1: 0.6", "CB2: 0.8"]),
        ("5F-CUMYL-PINACA", "5-fluoro-CUMYL", 2.0, ["CB1: 0.8", "CB2: 1.2"]),
    ]
    
    # AM Serisi (Alexandros Makriyannis) - nrcdnl94
    am_series = [
        ("AM-2201", "fluoropentyl JWH-018", 2.5, ["CB1: 1.0", "CB2: 2.6"]),
        ("AM-694", "iodopentyl", 1.5, ["CB1: 0.08", "CB2: 1.44"]),
        ("AM-1220", "methylpiperidine", 1.8, ["CB1: 2.2", "CB2: 52.0"]),
        ("AM-1221", "N-methylpiperidine", 1.7, ["CB1: 1.6", "CB2: 34.0"]),
        ("AM-2233", "iodo variant", 2.0, ["CB1: 0.28", "CB2: 1.37"]),
    ]
    
    # İndazol karboksamidler (Halka değişikliği: İndol → İndazol) - nrcdnl94
    indazole_carboxamides = [
        ("AKB-48", "APINACA", 2.0, ["CB1: 1.2", "CB2: 2.5"]),
        ("AB-PINACA", "AB variant", 2.5, ["CB1: 0.5", "CB2: 1.0"]),
        ("AB-FUBINACA", "4-fluorobenzyl", 3.0, ["CB1: 0.3", "CB2: 0.6"]),
        ("AB-CHMINACA", "cyclohexylmethyl", 2.8, ["CB1: 0.4", "CB2: 0.8"]),
        ("ADB-FUBINACA", "tert-leucine", 3.5, ["CB1: 0.2", "CB2: 0.4"]),
        ("ADB-PINACA", "ADB variant", 3.2, ["CB1: 0.3", "CB2: 0.5"]),
        ("AMB-FUBINACA", "methyl ester", 3.0, ["CB1: 0.4", "CB2: 0.7"]),
        ("MDMB-FUBINACA", "dimethylbutanoate", 4.5, ["CB1: 0.08", "CB2: 0.15"]),
        ("MDMB-4en-PINACA", "terminal alkene", 4.0, ["CB1: 0.1", "CB2: 0.2"]),
    ]
    
    # Veritabanına ekle - nrcdnl94
    for series_data, nps_class_name in [
        (jwh_series, "JWH"),
        (fluoro_cannabinoids, "5F"),
        (am_series, "AM"),
        (indazole_carboxamides, "INDAZOLE")
    ]:
        for name, desc, potency, binding in series_data:
            compound_id = f"SC_{name.replace('-', '_').replace(' ', '_')}"
            nps_db[compound_id] = NPSDerivative(
                compound_id=compound_id,
                name_iupac=f"{name} derivative",
                name_common=name,
                name_turkish=f"{name} (Sentetik Kannabinoid)",
                parent_compound="THC" if nps_class_name == "JWH" else nps_class_name,
                nps_class=NPSClass.SYNTHETIC_CANNABINOIDS,
                modifications=[ChemicalModification.RING_SUBSTITUTION, 
                             ChemicalModification.CHAIN_EXTENSION if potency > 1.5 else ChemicalModification.N_ALKYLATION],
                molecular_formula=f"C{20+int(potency*2)}H{25+int(potency*3)}NO",
                molecular_weight=310 + potency * 20,
                potency_ratio=potency,
                receptor_targets=["CB1", "CB2"],
                binding_affinity=dict(b.split(": ") for b in binding),
                metabolism_half_life=2.5 + potency,
                detection_markers=[f"{name}_M1", f"{name}_M2"],
                cpg_markers=["cg02242964", "cg09935388", "cg04180046", "cg07123182"],
                legal_status="Liste I" if potency > 2.0 else "Kontrollü",
                first_reported="2008-2023",
                street_names=[name, f"Spice_{name}", "K2", "Synthetic marijuana"],
                toxicity_notes=f"Potens oranı: {potency}x THC. Ciddi toksisite riski." if potency > 2 else "Orta düzey risk",
                eaa_effect=1.5 + potency * 0.5
            )
    
    # ========================================================================
    # 2. SENTETİK KATİNONLAR - ALFA-PİROLİDİNOFENONLAR VE BETA-KETO TÜREVLERİ
    # ========================================================================
    # Temel iskelet: β-keto-amfetamin (katinon)
    # Modifikasyonlar: Alfa-substitüsyon, halka substitüsyon, N-alkilasyon
    
    # nrcdnl94
    cathinone_derivatives = [
        # Halka substitüsyonları (2-, 3-, 4- pozisyonları)
        ("4-MMC", "Mefedron", "4-methylmethcathinone", 1.0, ["DAT", "SERT", "NET"], [ChemicalModification.RING_SUBSTITUTION, ChemicalModification.METHYLATION]),
        ("4-MEC", "4-Metilethkatinon", "4-methylethcathinone", 0.9, ["DAT", "SERT"], [ChemicalModification.RING_SUBSTITUTION]),
        ("4-EMC", "4-Etilmethkatinon", "4-ethylmethcathinone", 0.85, ["DAT", "SERT"], [ChemicalModification.RING_SUBSTITUTION]),
        ("3-MMC", "3-Metilmethkatinon", "3-methylmethcathinone", 0.95, ["DAT", "SERT", "NET"], [ChemicalModification.RING_SUBSTITUTION]),
        ("3-CMC", "3-Klormethkatinon", "3-chloromethcathinone", 0.8, ["DAT", "SERT"], [ChemicalModification.HALOGENATION]),
        ("4-CMC", "Klefedron", "4-chloromethcathinone", 0.85, ["DAT", "SERT"], [ChemicalModification.HALOGENATION]),
        ("4-BMC", "4-Brommethkatinon", "4-bromomethcathinone", 0.75, ["DAT", "SERT"], [ChemicalModification.HALOGENATION]),
        ("4-FMC", "Flefedron", "4-fluoromethcathinone", 0.9, ["DAT", "SERT", "NET"], [ChemicalModification.FLUORINATION]),
        ("3-FMC", "3-Fluormethkatinon", "3-fluoromethcathinone", 0.85, ["DAT", "SERT"], [ChemicalModification.FLUORINATION]),
        
        # Metoksi türevleri
        ("PMMC", "para-Metoksimethkatinon", "4-methoxymethcathinone", 0.7, ["SERT"], [ChemicalModification.METHOXYLATION]),
        ("MMMC", "meta-Metoksimethkatinon", "3-methoxymethcathinone", 0.65, ["SERT"], [ChemicalModification.METHOXYLATION]),
        ("bk-MMDMA", "Dimetilon", "methylenedioxymethcathinone", 0.8, ["SERT", "DAT"], [ChemicalModification.METHOXYLATION]),
        
        # Dihidroksi/Dimetoksi türevleri
        ("bk-MBDB", "Butylon", "β-keto-MBDB", 0.75, ["SERT", "DAT"], [ChemicalModification.RING_SUBSTITUTION]),
        ("bk-MDEA", "Etilon", "β-keto-MDEA", 0.8, ["SERT", "DAT", "NET"], [ChemicalModification.RING_SUBSTITUTION]),
        ("bk-MDMA", "Metilon", "β-keto-MDMA", 0.9, ["SERT", "DAT", "NET"], [ChemicalModification.RING_SUBSTITUTION]),
        ("Pentalon", "Pentalon", "β-keto-pentylone", 0.85, ["DAT", "SERT"], [ChemicalModification.CHAIN_EXTENSION]),
        ("Eutylon", "Eutylon", "β-keto-eutylone", 0.9, ["DAT", "SERT"], [ChemicalModification.CHAIN_EXTENSION]),
        ("Dibutilon", "Dibutilon", "dibutylone", 0.95, ["DAT", "SERT"], [ChemicalModification.CHAIN_EXTENSION]),
        
        # Alfa-pirolidinofenon (α-PVP ailesi) - Alfa-substitüsyon
        ("α-PVP", "Alfa-PVP", "α-pyrrolidinopentiophenone", 1.5, ["DAT", "NET"], [ChemicalModification.ALPHA_SUBSTITUTION]),
        ("α-PBP", "Alfa-PBP", "α-pyrrolidinobutiophenone", 1.3, ["DAT", "NET"], [ChemicalModification.ALPHA_SUBSTITUTION]),
        ("α-PPP", "Alfa-PPP", "α-pyrrolidinopropiophenone", 1.2, ["DAT", "NET"], [ChemicalModification.ALPHA_SUBSTITUTION]),
        ("α-PHP", "Alfa-PHP", "α-pyrrolidinohexanophenone", 1.6, ["DAT", "NET"], [ChemicalModification.ALPHA_SUBSTITUTION, ChemicalModification.CHAIN_EXTENSION]),
        ("α-PHiP", "Alfa-PHiP", "α-pyrrolidinohexanophenone isomer", 1.55, ["DAT", "NET"], [ChemicalModification.ALPHA_SUBSTITUTION, ChemicalModification.STEREOISOMER]),
        ("α-POP", "Alfa-POP", "α-pyrrolidinooctanophenone", 1.7, ["DAT", "NET"], [ChemicalModification.ALPHA_SUBSTITUTION, ChemicalModification.CHAIN_EXTENSION]),
        
        # 3,4-MDPV türevleri (Metilendioksi substitüsyon)
        ("MDPV", "MDPV", "3,4-methylenedioxypyrovalerone", 2.0, ["DAT", "NET"], [ChemicalModification.RING_SUBSTITUTION, ChemicalModification.ALPHA_SUBSTITUTION]),
        ("MDPPP", "MDPPP", "3,4-methylenedioxy-α-PPP", 1.6, ["DAT", "NET"], [ChemicalModification.RING_SUBSTITUTION]),
        ("MDPBP", "MDPBP", "3,4-methylenedioxy-α-PBP", 1.8, ["DAT", "NET"], [ChemicalModification.RING_SUBSTITUTION]),
        ("3,4-MDPHP", "MDPHP", "3,4-methylenedioxy-α-PHP", 2.2, ["DAT", "NET"], [ChemicalModification.RING_SUBSTITUTION, ChemicalModification.CHAIN_EXTENSION]),
        
        # 4-Fluoro alfa-pirolidinofenon türevleri
        ("4F-α-PVP", "4-Fluoro-α-PVP", "4-fluoro-α-PVP", 1.8, ["DAT", "NET"], [ChemicalModification.FLUORINATION, ChemicalModification.ALPHA_SUBSTITUTION]),
        ("4F-α-PHP", "4-Fluoro-α-PHP", "4-fluoro-α-PHP", 1.9, ["DAT", "NET"], [ChemicalModification.FLUORINATION, ChemicalModification.ALPHA_SUBSTITUTION]),
        ("4F-MDMB-BUTINACA", "4F-MDMB", "4-fluoro-MDMB", 2.5, ["DAT", "NET"], [ChemicalModification.FLUORINATION]),
        
        # N-Etil ve N-Propil türevleri (N-alkilasyon)
        ("NEP", "N-Etilpentedron", "N-ethylpentedrone", 1.1, ["DAT", "NET"], [ChemicalModification.N_ALKYLATION]),
        ("N-Etilhexedron", "N-Etilheksedron", "N-ethylhexedrone", 1.2, ["DAT", "NET"], [ChemicalModification.N_ALKYLATION, ChemicalModification.CHAIN_EXTENSION]),
        ("N-Etilheptedron", "N-Etilheptedron", "N-ethylheptedrone", 1.3, ["DAT", "NET"], [ChemicalModification.N_ALKYLATION, ChemicalModification.CHAIN_EXTENSION]),
    ]
    
    for common, turkish, iupac, potency, targets, mods in cathinone_derivatives:
        compound_id = f"CAT_{common.replace('-', '_').replace(' ', '_').replace('α', 'a').replace('β', 'b')}"
        nps_db[compound_id] = NPSDerivative(
            compound_id=compound_id,
            name_iupac=iupac,
            name_common=common,
            name_turkish=turkish,
            parent_compound="Cathinone",
            nps_class=NPSClass.SYNTHETIC_CATHINONES,
            modifications=mods,
            molecular_formula=f"C{11+len(common)//3}H{15+len(common)//2}NO",
            molecular_weight=180 + potency * 25,
            potency_ratio=potency,
            receptor_targets=targets,
            binding_affinity={t: str(10/potency) for t in targets},
            metabolism_half_life=3 + potency * 0.5,
            detection_markers=[f"{common}_M1", f"{common}_COOH"],
            cpg_markers=["cg03821126", "cg08709672", "cg22132788", "cg14179389"],
            legal_status="Liste I",
            first_reported="2007-2022",
            street_names=[common, "Bath salts", "Meow meow" if "MMC" in common else "Flakka" if "PVP" in common else common],
            toxicity_notes=f"Stimulan toksisite. Potens: {potency}x katinon.",
            eaa_effect=2.0 + potency * 0.8
        )
    
    # ========================================================================
    # 3. FENETİLAMİN TÜREVLERİ - HALKAİ VE YAN ZİNCİR MODİFİKASYONLARI
    # ========================================================================
    # nrcdnl94
    
    # 2C-x Serisi (Shulgin) - Halka substitüsyonları
    two_c_series = [
        ("2C-B", "4-bromo-2,5-dimethoxyphenethylamine", 1.0, ["5-HT2A", "5-HT2C"]),
        ("2C-I", "4-iodo-2,5-dimethoxyphenethylamine", 1.2, ["5-HT2A", "5-HT2C"]),
        ("2C-E", "4-ethyl-2,5-dimethoxyphenethylamine", 0.9, ["5-HT2A", "5-HT2C"]),
        ("2C-C", "4-chloro-2,5-dimethoxyphenethylamine", 0.8, ["5-HT2A", "5-HT2C"]),
        ("2C-D", "4-methyl-2,5-dimethoxyphenethylamine", 0.7, ["5-HT2A", "5-HT2C"]),
        ("2C-P", "4-propyl-2,5-dimethoxyphenethylamine", 1.5, ["5-HT2A", "5-HT2C"]),
        ("2C-T-2", "4-methylthio-2,5-dimethoxyphenethylamine", 1.1, ["5-HT2A", "5-HT2C"]),
        ("2C-T-7", "4-propylthio-2,5-dimethoxyphenethylamine", 1.3, ["5-HT2A", "5-HT2C"]),
        ("2C-T-21", "4-fluoroethylthio variant", 1.4, ["5-HT2A", "5-HT2C"]),
    ]
    
    # NBOMe Serisi (N-benziloksi fenethilamin) - nrcdnl94
    nbome_series = [
        ("25I-NBOMe", "25I-NBOMe", 10.0, ["5-HT2A"]),  # Çok potent
        ("25B-NBOMe", "25B-NBOMe", 8.0, ["5-HT2A"]),
        ("25C-NBOMe", "25C-NBOMe", 7.0, ["5-HT2A"]),
        ("25E-NBOMe", "25E-NBOMe", 6.0, ["5-HT2A"]),
        ("25D-NBOMe", "25D-NBOMe", 5.0, ["5-HT2A"]),
        ("25N-NBOMe", "25N-NBOMe", 9.0, ["5-HT2A"]),
        ("25T2-NBOMe", "25T2-NBOMe", 7.5, ["5-HT2A"]),
    ]
    
    # DOx Serisi (Dimetoksiamfetamin) - nrcdnl94
    dox_series = [
        ("DOM", "2,5-dimethoxy-4-methylamphetamine", 1.0, ["5-HT2A", "5-HT2B"]),
        ("DOB", "2,5-dimethoxy-4-bromoamphetamine", 1.5, ["5-HT2A", "5-HT2B"]),
        ("DOI", "2,5-dimethoxy-4-iodoamphetamine", 2.0, ["5-HT2A", "5-HT2B"]),
        ("DOC", "2,5-dimethoxy-4-chloroamphetamine", 1.3, ["5-HT2A", "5-HT2B"]),
        ("DOET", "2,5-dimethoxy-4-ethylamphetamine", 0.9, ["5-HT2A", "5-HT2B"]),
        ("DON", "2,5-dimethoxy-4-nitroamphetamine", 1.8, ["5-HT2A", "5-HT2B"]),
        ("DOPR", "2,5-dimethoxy-4-propylamphetamine", 1.1, ["5-HT2A", "5-HT2B"]),
    ]
    
    # Substitue Amfetaminler (Pozisyon izomerleri) - nrcdnl94
    substituted_amphetamines = [
        # 4-pozisyon substitüsyonları
        ("4-FA", "4-Floroamfetamin", "4-fluoroamphetamine", 1.2, ["DAT", "SERT", "NET"], ChemicalModification.FLUORINATION),
        ("4-FMA", "4-Florometamfetamin", "4-fluoromethamphetamine", 1.3, ["DAT", "SERT", "NET"], ChemicalModification.FLUORINATION),
        ("4-CA", "4-Kloroamfetamin", "4-chloroamphetamine", 1.1, ["DAT", "SERT"], ChemicalModification.HALOGENATION),
        ("4-BA", "4-Bromoamfetamin", "4-bromoamphetamine", 1.0, ["DAT", "SERT"], ChemicalModification.HALOGENATION),
        ("4-MA", "4-Metilamfetamin", "4-methylamphetamine", 0.9, ["DAT", "SERT", "NET"], ChemicalModification.METHYLATION),
        ("4-MMA", "4-Metoksimetamfetamin", "4-methoxymethamphetamine", 0.8, ["SERT"], ChemicalModification.METHOXYLATION),
        
        # 3-pozisyon substitüsyonları
        ("3-FA", "3-Floroamfetamin", "3-fluoroamphetamine", 1.1, ["DAT", "NET"], ChemicalModification.FLUORINATION),
        ("3-FMA", "3-Florometamfetamin", "3-fluoromethamphetamine", 1.2, ["DAT", "NET"], ChemicalModification.FLUORINATION),
        
        # 2-pozisyon substitüsyonları
        ("2-FA", "2-Floroamfetamin", "2-fluoroamphetamine", 0.9, ["DAT", "NET"], ChemicalModification.FLUORINATION),
        ("2-FMA", "2-Florometamfetamin", "2-fluoromethamphetamine", 1.0, ["DAT", "NET"], ChemicalModification.FLUORINATION),
        
        # Çoklu substitüsyonlar
        ("3,4-DFA", "3,4-Difloroamfetamin", "3,4-difluoroamphetamine", 1.4, ["DAT", "NET"], ChemicalModification.FLUORINATION),
        ("2,4-DFA", "2,4-Difloroamfetamin", "2,4-difluoroamphetamine", 1.3, ["DAT", "NET"], ChemicalModification.FLUORINATION),
    ]
    
    # Veritabanına ekle - nrcdnl94
    for name, iupac, potency, targets in two_c_series + nbome_series + dox_series:
        compound_id = f"PEA_{name.replace('-', '_').replace(' ', '_')}"
        nps_db[compound_id] = NPSDerivative(
            compound_id=compound_id,
            name_iupac=iupac,
            name_common=name,
            name_turkish=f"{name} (Halüsinojen)",
            parent_compound="Phenethylamine",
            nps_class=NPSClass.PHENETHYLAMINES,
            modifications=[ChemicalModification.RING_SUBSTITUTION, ChemicalModification.HALOGENATION if "I" in name or "B" in name or "C" in name else ChemicalModification.METHYLATION],
            molecular_formula=f"C{12+int(potency)}H{18+int(potency)}NO2",
            molecular_weight=200 + potency * 30,
            potency_ratio=potency,
            receptor_targets=targets,
            binding_affinity={t: str(5/potency) for t in targets},
            metabolism_half_life=6 + potency * 2,
            detection_markers=[f"{name}_M1"],
            cpg_markers=["cg07123182", "cg15768986", "cg22132788", "cg14179389"],
            legal_status="Liste I",
            first_reported="2003-2020",
            street_names=[name, "N-bomb" if "NBOMe" in name else name],
            toxicity_notes=f"Serotonerjik toksisite riski. Potens: {potency}x referans.",
            eaa_effect=1.8 + potency * 0.3
        )
    
    for common, turkish, iupac, potency, targets, mod in substituted_amphetamines:
        compound_id = f"AMP_{common.replace('-', '_')}"
        nps_db[compound_id] = NPSDerivative(
            compound_id=compound_id,
            name_iupac=iupac,
            name_common=common,
            name_turkish=turkish,
            parent_compound="Amphetamine",
            nps_class=NPSClass.PHENETHYLAMINES,
            modifications=[mod, ChemicalModification.RING_SUBSTITUTION],
            molecular_formula=f"C9H{12+int(potency)}FN" if "F" in common else f"C9H{12+int(potency)}ClN",
            molecular_weight=155 + potency * 20,
            potency_ratio=potency,
            receptor_targets=targets,
            binding_affinity={t: str(8/potency) for t in targets},
            metabolism_half_life=8 + potency,
            detection_markers=[f"{common}_M1", f"{common}_M2"],
            cpg_markers=["cg03821126", "cg08709672", "cg22132788"],
            legal_status="Liste I",
            first_reported="2010-2022",
            street_names=[common, f"{common} speed"],
            toxicity_notes=f"Amfetamin benzeri kardiyotoksisite.",
            eaa_effect=3.0 + potency * 0.5
        )
    
    # ========================================================================
    # 4. SENTETİK OPİOİDLER - FENTANİL ANALOGLARI
    # ========================================================================
    # N-asil yan zincir ve fenil halka modifikasyonları - nrcdnl94
    
    fentanyl_analogs = [
        # N-asil zincir uzunluğu değişiklikleri
        ("Acetylfentanyl", "Asetil fentanil", "N-acetyl", 0.15, ChemicalModification.CHAIN_SHORTENING),  # -2C
        ("Butyrylfentanyl", "Butiril fentanil", "N-butyryl", 0.25, ChemicalModification.CHAIN_EXTENSION),  # +1C
        ("Valerylfentanyl", "Valeril fentanil", "N-valeryl", 0.3, ChemicalModification.CHAIN_EXTENSION),  # +2C
        ("Hexanoylfentanyl", "Heksanoil fentanil", "N-hexanoyl", 0.35, ChemicalModification.CHAIN_EXTENSION),
        ("Isobutyrylfentanyl", "İzobütiril fentanil", "N-isobutyryl", 0.2, ChemicalModification.STEREOISOMER),
        ("Crotonoylfentanyl", "Krotonol fentanil", "N-crotonyl (unsaturated)", 0.28, ChemicalModification.CHAIN_EXTENSION),
        
        # Halka substitüsyonları
        ("para-Fluorofentanyl", "4-Fluoro fentanil", "4-fluorophenyl", 1.2, ChemicalModification.FLUORINATION),
        ("ortho-Fluorofentanyl", "2-Fluoro fentanil", "2-fluorophenyl", 0.8, ChemicalModification.FLUORINATION),
        ("meta-Fluorofentanyl", "3-Fluoro fentanil", "3-fluorophenyl", 0.9, ChemicalModification.FLUORINATION),
        ("3-Methylfentanyl", "3-Metil fentanil (cis)", "3-methylpiperidine (cis)", 3.0, ChemicalModification.METHYLATION),
        ("3-Methylfentanyl-trans", "3-Metil fentanil (trans)", "3-methylpiperidine (trans)", 6.0, ChemicalModification.STEREOISOMER),  # Stereoizomer etkisi!
        
        # Çoklu modifikasyonlar
        ("Carfentanil", "Karfentanil", "carbomethoxy", 100.0, ChemicalModification.RING_SUBSTITUTION),  # Ekstrem potens
        ("Sufentanil", "Sufentanil", "thiophene ring", 5.0, ChemicalModification.RING_SUBSTITUTION),
        ("Remifentanil", "Remifentanil", "ester linkage", 2.0, ChemicalModification.CHAIN_EXTENSION),
        ("Alfentanil", "Alfentanil", "tetrazole ring", 0.5, ChemicalModification.RING_SUBSTITUTION),
        ("Lofentanil", "Lofentanil", "3-methyl + carbomethoxy", 50.0, ChemicalModification.RING_SUBSTITUTION),
        ("Ohmefentanyl", "Ohmefentanil", "3-methyl + hydroxyl", 28.0, ChemicalModification.HYDROXYLATION),
        
        # Benzimidazol opioidleri (Nitazene ailesi)
        ("Isotonitazene", "İzotonitazen", "benzimidazole", 500.0, ChemicalModification.RING_SUBSTITUTION),  # Çok tehlikeli
        ("Metonitazene", "Metonitazen", "benzimidazole methoxy", 100.0, ChemicalModification.RING_SUBSTITUTION),
        ("Etonitazene", "Etonitazen", "benzimidazole ethyl", 1000.0, ChemicalModification.RING_SUBSTITUTION),
        ("Protonitazene", "Protonitazen", "benzimidazole propyl", 200.0, ChemicalModification.RING_SUBSTITUTION),
        ("Butonitazene", "Butonitazen", "benzimidazole butyl", 150.0, ChemicalModification.CHAIN_EXTENSION),
        ("Flunitazene", "Flunitazen", "benzimidazole fluoro", 300.0, ChemicalModification.FLUORINATION),
        
        # Diğer sentetik opioidler
        ("U-47700", "U-47700", "benzamide", 7.5, ChemicalModification.RING_SUBSTITUTION),
        ("U-49900", "U-49900", "benzamide chloro", 5.0, ChemicalModification.HALOGENATION),
        ("U-50488", "U-50488", "benzamide kappa", 0.5, ChemicalModification.RING_SUBSTITUTION),
        ("AH-7921", "AH-7921", "aminocyclohexane", 1.0, ChemicalModification.RING_SUBSTITUTION),
        ("MT-45", "MT-45", "piperazine", 0.3, ChemicalModification.RING_SUBSTITUTION),
        ("AP-237", "AP-237", "bucinnazine analog", 3.0, ChemicalModification.RING_SUBSTITUTION),
        ("Brorphine", "Brorfin", "brominated piperidine", 15.0, ChemicalModification.HALOGENATION),
    ]
    
    for common, turkish, desc, potency, mod in fentanyl_analogs:
        compound_id = f"OPI_{common.replace('-', '_').replace(' ', '_')}"
        nps_db[compound_id] = NPSDerivative(
            compound_id=compound_id,
            name_iupac=f"Fentanyl analog: {desc}",
            name_common=common,
            name_turkish=turkish,
            parent_compound="Fentanyl",
            nps_class=NPSClass.SYNTHETIC_OPIOIDS,
            modifications=[mod, ChemicalModification.N_ALKYLATION],
            molecular_formula=f"C{22+int(np.log10(potency+1)*2)}H{28+int(potency//10)}N2O",
            molecular_weight=336 + potency * 0.5,
            potency_ratio=potency,
            receptor_targets=["OPRM1", "OPRK1", "OPRD1"],
            binding_affinity={"OPRM1": f"Ki={0.39/potency:.4f} nM"},
            metabolism_half_life=2 + potency * 0.01,
            detection_markers=[f"{common.split('-')[0]}_norfentanyl"],
            cpg_markers=["cg10406920", "cg15768986", "cg07123182", "cg22132788"],
            legal_status="Liste I (Acil Kontrol)",
            first_reported="2012-2023",
            street_names=[common, "China White" if potency > 50 else "Grey Death" if potency > 10 else common],
            toxicity_notes=f"UYARI: Morfin eşdeğeri {potency}x. Doz aşımı riski ÇOK YÜKSEK!" if potency > 5 else f"Potens: {potency}x morfin.",
            eaa_effect=4.0 + np.log10(potency + 1) * 1.5
        )
    
    # ========================================================================
    # 5. TRİPTAMİN TÜREVLERİ
    # ========================================================================
    # nrcdnl94
    
    tryptamine_derivatives = [
        # N,N-Dialkil triptaminler (N-substitüsyon)
        ("DMT", "N,N-Dimetiltriptamin", "N,N-dimethyltryptamine", 1.0, ["5-HT2A", "Sigma-1"]),
        ("DET", "N,N-Dietiltriptamin", "N,N-diethyltryptamine", 0.8, ["5-HT2A"]),
        ("DPT", "N,N-Dipropiltriptamin", "N,N-dipropyltryptamine", 0.9, ["5-HT2A"]),
        ("DiPT", "N,N-Diisoropiltriptamin", "N,N-diisopropyltryptamine", 0.7, ["5-HT2A"]),
        ("MiPT", "N-Metil-N-izopropiltriptamin", "N-methyl-N-isopropyltryptamine", 0.75, ["5-HT2A"]),
        ("DBT", "N,N-Dibütiltriptamin", "N,N-dibutyltryptamine", 0.6, ["5-HT2A"]),
        
        # 4-Hidroksi türevleri (Psilosibin/Psilosin)
        ("Psilocin", "Psilosin", "4-hydroxy-N,N-DMT", 1.0, ["5-HT2A", "5-HT2C"]),
        ("Psilocybin", "Psilosibin", "4-phosphoryloxy-N,N-DMT", 1.0, ["5-HT2A", "5-HT2C"]),
        ("4-HO-MET", "4-Hidroksi-MET", "4-hydroxy-N-methyl-N-ethyltryptamine", 0.9, ["5-HT2A"]),
        ("4-HO-DET", "4-Hidroksi-DET", "4-hydroxy-N,N-diethyltryptamine", 0.8, ["5-HT2A"]),
        ("4-HO-MiPT", "4-Hidroksi-MiPT", "4-hydroxy-N-methyl-N-isopropyltryptamine", 0.85, ["5-HT2A"]),
        ("4-HO-DiPT", "4-Hidroksi-DiPT", "4-hydroxy-N,N-diisopropyltryptamine", 0.7, ["5-HT2A"]),
        
        # 4-Asetoksi türevleri (Prodrug)
        ("4-AcO-DMT", "4-Asetoksi-DMT", "4-acetoxy-N,N-DMT", 1.0, ["5-HT2A"]),
        ("4-AcO-MET", "4-Asetoksi-MET", "4-acetoxy-N-methyl-N-ethyltryptamine", 0.9, ["5-HT2A"]),
        ("4-AcO-DET", "4-Asetoksi-DET", "4-acetoxy-N,N-diethyltryptamine", 0.85, ["5-HT2A"]),
        ("4-AcO-MiPT", "4-Asetoksi-MiPT", "4-acetoxy-MiPT", 0.8, ["5-HT2A"]),
        
        # 5-Metoksi türevleri
        ("5-MeO-DMT", "5-Metoksi-DMT", "5-methoxy-N,N-DMT", 2.0, ["5-HT2A", "5-HT1A"]),
        ("5-MeO-MiPT", "5-Metoksi-MiPT", "5-methoxy-N-methyl-N-isopropyltryptamine", 1.5, ["5-HT2A"]),
        ("5-MeO-DiPT", "5-Metoksi-DiPT", "5-methoxy-N,N-diisopropyltryptamine", 1.2, ["5-HT2A"]),
        ("5-MeO-DET", "5-Metoksi-DET", "5-methoxy-N,N-diethyltryptamine", 1.1, ["5-HT2A"]),
        ("5-MeO-AMT", "5-Metoksi-AMT", "5-methoxy-α-methyltryptamine", 1.8, ["5-HT2A", "MAO-I"]),
        ("Bufotenin", "Bufotenin", "5-hydroxy-N,N-DMT", 0.3, ["5-HT2A"]),
        
        # Alfa-metil türevleri (AMT)
        ("AMT", "α-Metiltriptamin", "α-methyltryptamine", 1.0, ["5-HT2A", "MAO-I", "SERT"]),
        ("AET", "α-Etiltriptamin", "α-ethyltryptamine", 0.8, ["5-HT2A", "MAO-I"]),
    ]
    
    for common, turkish, iupac, potency, targets in tryptamine_derivatives:
        compound_id = f"TRP_{common.replace('-', '_').replace(',', '_')}"
        nps_db[compound_id] = NPSDerivative(
            compound_id=compound_id,
            name_iupac=iupac,
            name_common=common,
            name_turkish=turkish,
            parent_compound="Tryptamine",
            nps_class=NPSClass.TRYPTAMINES,
            modifications=[ChemicalModification.N_ALKYLATION, 
                          ChemicalModification.HYDROXYLATION if "HO" in common else 
                          ChemicalModification.METHOXYLATION if "MeO" in common else
                          ChemicalModification.ALPHA_SUBSTITUTION],
            molecular_formula=f"C{12+len(common)//4}H{16+len(common)//3}N2O",
            molecular_weight=188 + potency * 25,
            potency_ratio=potency,
            receptor_targets=targets,
            binding_affinity={t: str(10/potency) for t in targets},
            metabolism_half_life=4 + potency * 2,
            detection_markers=[f"{common}_M1"],
            cpg_markers=["cg07123182", "cg15768986", "cg22132788"],
            legal_status="Liste I",
            first_reported="1990-2020",
            street_names=[common, "Spirit molecule" if "DMT" in common else common],
            toxicity_notes=f"Serotonin sendromu riski (MAO-I etkileşimi)." if "MAO" in str(targets) else f"Halüsinojenik.",
            eaa_effect=1.2 + potency * 0.4
        )
    
    # ========================================================================
    # 6. TASARIM BENZODİAZEPİNLERİ
    # ========================================================================
    # nrcdnl94
    
    designer_benzodiazepines = [
        # Triazolobenzodiazepinler
        ("Flualprazolam", "Flualprazolam", "2-fluoro-alprazolam", 2.0, ["GABA-A"]),
        ("Flunitrazolam", "Flunitrazolam", "flunitrazepam+triazolo", 3.0, ["GABA-A"]),
        ("Clonazolam", "Klonazolam", "clonazepam+triazolo", 2.5, ["GABA-A"]),
        ("Deschloroetizolam", "Deskloroetizolam", "des-chloro-etizolam", 0.8, ["GABA-A"]),
        ("Flubromazolam", "Flubromazolam", "fluoro-bromo-triazolam", 4.0, ["GABA-A"]),
        ("Nifoxipam", "Nifoksipam", "5-fluoro-desmethylflunitrazepam", 1.5, ["GABA-A"]),
        
        # Tienodiazepinler
        ("Etizolam", "Etizolam", "thienodiazepine", 1.0, ["GABA-A"]),
        ("Metizolam", "Metizolam", "desmethyl-etizolam", 0.9, ["GABA-A"]),
        ("Deschloroetizolam", "Deskloroetizolam", "des-chloro-etizolam", 0.7, ["GABA-A"]),
        ("Fluclotizolam", "Flukltizolam", "fluoro-chloro-thienodiazepine", 1.8, ["GABA-A"]),
        
        # Klasik iskelet modifikasyonları
        ("Diclazepam", "Diklazepam", "2-chloro-diazepam", 1.5, ["GABA-A"]),
        ("Flubromazepam", "Flubromazepam", "bromo-fluoro-diazepam", 2.0, ["GABA-A"]),
        ("Meclonazepam", "Meklonazepam", "3-methyl-clonazepam", 1.2, ["GABA-A"]),
        ("Phenazepam", "Fenazepam", "7-bromo-5-chloro", 1.8, ["GABA-A"]),
        ("Norflurazepam", "Norflurazepam", "N-desmethyl-flurazepam", 0.8, ["GABA-A"]),
        ("Pyrazolam", "Pirazolam", "pyridyl-triazolam", 1.0, ["GABA-A"]),
        ("Nitrazolam", "Nitrazolam", "nitro-triazolam", 1.5, ["GABA-A"]),
        ("Bromazolam", "Bromazolam", "bromo-alprazolam", 2.2, ["GABA-A"]),
        ("Gidazepam", "Gidazepam", "glycine-diazepam", 0.5, ["GABA-A"]),
        ("Adinazolam", "Adinazolam", "amino-triazolodiazepam", 1.0, ["GABA-A"]),
    ]
    
    for common, turkish, desc, potency, targets in designer_benzodiazepines:
        compound_id = f"BZD_{common}"
        nps_db[compound_id] = NPSDerivative(
            compound_id=compound_id,
            name_iupac=f"Designer benzodiazepine: {desc}",
            name_common=common,
            name_turkish=turkish,
            parent_compound="Benzodiazepine scaffold",
            nps_class=NPSClass.BENZODIAZEPINES_NPS,
            modifications=[ChemicalModification.HALOGENATION if "fluor" in desc.lower() or "chlor" in desc.lower() or "brom" in desc.lower() else ChemicalModification.RING_SUBSTITUTION],
            molecular_formula=f"C{16+int(potency)}H{13+int(potency)}ClFN3O",
            molecular_weight=300 + potency * 20,
            potency_ratio=potency,
            receptor_targets=targets,
            binding_affinity={"GABA-A α1": f"Ki={5/potency:.2f} nM"},
            metabolism_half_life=12 + potency * 8,
            detection_markers=[f"{common}_M1", f"{common}_glucuronide"],
            cpg_markers=["cg17739917", "cg06690548", "cg12803068"],
            legal_status="Liste IV" if potency < 1.5 else "Liste I",
            first_reported="2010-2022",
            street_names=[common, "Benzos", f"Designer {common}"],
            toxicity_notes=f"Solunum depresyonu riski. Diazepam eşdeğeri: {potency}x." if potency > 1.5 else "Orta düzey sedasyon.",
            eaa_effect=1.5 + potency * 0.3
        )
    
    # ========================================================================
    # 7. ARİLSİKLOHEKZİLAMİNLER (Disosiyatifler)
    # ========================================================================
    # nrcdnl94
    
    arylcyclohexylamines = [
        ("Ketamine", "Ketamin", "2-chlorophenyl-2-methylamino", 1.0, ["NMDA", "D2", "5-HT2"]),
        ("Deschloroketamine", "Deskloroketamin", "2-phenyl variant", 0.7, ["NMDA"]),
        ("2-FDCK", "2-Florodesklroketamin", "2-fluorophenyl", 0.9, ["NMDA"]),
        ("2-BDCK", "2-Bromodesklroketamin", "2-bromophenyl", 0.8, ["NMDA"]),
        ("3-HO-PCP", "3-Hidroksi-PCP", "3-hydroxy-phencyclidine", 1.5, ["NMDA", "OPRM1"]),
        ("3-MeO-PCP", "3-Metoksi-PCP", "3-methoxy-phencyclidine", 1.8, ["NMDA", "SERT"]),
        ("3-MeO-PCE", "3-Metoksi-PCE", "3-methoxy-eticyclidine", 1.2, ["NMDA"]),
        ("3-MeO-PCMo", "3-Metoksi-PCMo", "3-methoxy-PCMo", 1.0, ["NMDA"]),
        ("O-PCE", "O-PCE", "2-oxo-eticyclidine", 1.3, ["NMDA"]),
        ("MXE", "Metoksietamin", "methoxetamine", 1.5, ["NMDA", "SERT"]),
        ("MXiPr", "Metoksiizoprpilamin", "methoxy-isopropylamine", 1.2, ["NMDA"]),
        ("DMXE", "Dimetoksietamin", "dimethoxetamine", 1.4, ["NMDA"]),
        ("3-Cl-PCP", "3-Kloro-PCP", "3-chloro-phencyclidine", 1.6, ["NMDA"]),
        ("3-F-PCP", "3-Fluoro-PCP", "3-fluoro-phencyclidine", 1.4, ["NMDA"]),
        ("4-MeO-PCP", "4-Metoksi-PCP", "4-methoxy-phencyclidine", 0.8, ["NMDA"]),
        ("Tiletamine", "Tiletamin", "thiophene ketamine analog", 1.5, ["NMDA"]),
    ]
    
    for common, turkish, desc, potency, targets in arylcyclohexylamines:
        compound_id = f"DIS_{common.replace('-', '_')}"
        nps_db[compound_id] = NPSDerivative(
            compound_id=compound_id,
            name_iupac=desc,
            name_common=common,
            name_turkish=turkish,
            parent_compound="PCP/Ketamine",
            nps_class=NPSClass.ARYLCYCLOHEXYLAMINES,
            modifications=[ChemicalModification.HALOGENATION if "F" in common or "Cl" in common or "Br" in common else ChemicalModification.METHOXYLATION if "MeO" in common else ChemicalModification.HYDROXYLATION],
            molecular_formula=f"C{13+int(potency)}H{18+int(potency)}ClNO",
            molecular_weight=220 + potency * 15,
            potency_ratio=potency,
            receptor_targets=targets,
            binding_affinity={"NMDA": f"Ki={50/potency:.1f} nM"},
            metabolism_half_life=3 + potency * 2,
            detection_markers=[f"{common}_nor"],
            cpg_markers=["cg07123182", "cg15768986", "cg17739917"],
            legal_status="Liste II" if common == "Ketamine" else "Liste I",
            first_reported="2000-2022",
            street_names=[common, "Special K" if "Ketamin" in turkish else "Angel dust" if "PCP" in common else common],
            toxicity_notes=f"Disosiyatif toksisite. NMDA antagonizması.",
            eaa_effect=2.0 + potency * 0.5
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
        "newest_compounds": []
    }
    
    for compound in nps_db.values():
        # Sınıf bazında sayım
        class_name = compound.nps_class.value
        stats["by_class"][class_name] = stats["by_class"].get(class_name, 0) + 1
        
        # Modifikasyon bazında sayım
        for mod in compound.modifications:
            mod_name = mod.value
            stats["by_modification"][mod_name] = stats["by_modification"].get(mod_name, 0) + 1
        
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
    stats["most_potent"] = sorted(stats["most_potent"], key=lambda x: x["potency"], reverse=True)[:10]
    
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
            if len(examples[mod_name]) < 5:  # Her tip için 5 örnek
                examples[mod_name].append({
                    "compound": compound.name_common,
                    "parent": compound.parent_compound,
                    "potency_change": f"{compound.potency_ratio}x",
                    "class": compound.nps_class.value
                })
    
    return examples


# nrcdnl94 - End of NPS Derivatives Module
# Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır - All Rights Reserved
