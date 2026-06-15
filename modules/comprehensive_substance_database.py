# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Comprehensive Substance Abuse and Addiction Database
World Literature Integration Module

Data Sources:
- WHO Classification of Psychoactive Substances
- UNODC World Drug Report 2024
- DEA Controlled Substances Schedules
- EMCDDA Drug Profiles
- INCB International Control List
- PGC-SUD GWAS Meta-analyses
- EWAS Catalog Methylation Studies
- PharmGKB Pharmacogenomics

Author: Dr. Nurcan Denli Bayır
Platform: EpiClock Prototype
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class SubstanceClass(Enum):
    # nrcdnl94
    """WHO/UNODC Substance Classification"""
    OPIOIDS = "Opioidler"
    STIMULANTS = "Stimulanlar"
    DEPRESSANTS = "Depresanlar"
    HALLUCINOGENS = "Halüsinojenler"
    CANNABINOIDS = "Kannabinoidler"
    INHALANTS = "İnhalanlar"
    NICOTINE = "Nikotin/Tütün"
    CAFFEINE = "Kafein"
    NOVEL_PSYCHOACTIVE = "Yeni Psikoaktif Maddeler (NPS)"


class AddictionPotential(Enum):
    # nrcdnl94
    """Addiction liability classification"""
    VERY_HIGH = ("Çok Yüksek", 5, "Hızlı tolerans, şiddetli yoksunluk")
    HIGH = ("Yüksek", 4, "Belirgin bağımlılık yapıcı")
    MODERATE = ("Orta", 3, "Düzenli kullanımda bağımlılık riski")
    LOW = ("Düşük", 2, "Sınırlı bağımlılık potansiyeli")
    MINIMAL = ("Minimal", 1, "Nadir bağımlılık")


class LegalStatus(Enum):
    # nrcdnl94
    """International legal status"""
    SCHEDULE_I = "Liste I (Tıbbi kullanımı yok, yüksek kötüye kullanım)"
    SCHEDULE_II = "Liste II (Yüksek kötüye kullanım, tıbbi kullanım var)"
    SCHEDULE_III = "Liste III (Orta düzeyde kötüye kullanım)"
    SCHEDULE_IV = "Liste IV (Düşük kötüye kullanım)"
    SCHEDULE_V = "Liste V (Minimal kötüye kullanım)"
    UNSCHEDULED = "Kontrolsüz"
    PRESCRIPTION = "Reçeteye Tabi"
    OTC = "Reçetesiz Satılır"


@dataclass
# nrcdnl94
class SubstanceProfile:
    # nrcdnl94
    """Complete substance profile with genetic/epigenetic data"""
    name: str
    turkish_name: str
    class_type: SubstanceClass
    addiction_potential: AddictionPotential
    legal_status: LegalStatus
    
    mechanism_of_action: str
    primary_targets: List[str]
    receptor_affinity: Dict[str, str]
    
    gwas_genes: List[str] = field(default_factory=list)
    methylation_cpgs: List[str] = field(default_factory=list)
    pharmacogenes: List[str] = field(default_factory=list)
    
    eaa_effect_years: float = 0.0
    eaa_95ci: tuple = (0.0, 0.0)
    
    withdrawal_symptoms: List[str] = field(default_factory=list)
    treatment_options: List[str] = field(default_factory=list)
    
    street_names: List[str] = field(default_factory=list)
    detection_window: Dict[str, str] = field(default_factory=dict)


OPIOID_SUBSTANCES = {
    # nrcdnl94
    'morphine': SubstanceProfile(
        name="Morphine",
        turkish_name="Morfin",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="Mu-opioid reseptör tam agonisti",
        primary_targets=['OPRM1', 'OPRD1', 'OPRK1'],
        receptor_affinity={'OPRM1': 'Ki=1.8 nM', 'OPRD1': 'Ki=90 nM', 'OPRK1': 'Ki=317 nM'},
        gwas_genes=['OPRM1', 'OPRD1', 'OPRK1', 'COMT', 'ABCB1', 'CYP2D6', 'CYP3A4'],
        methylation_cpgs=['cg23480021', 'cg02722814', 'cg05575921', 'cg01940273'],
        pharmacogenes=['CYP2D6', 'CYP3A4', 'OPRM1', 'COMT', 'ABCB1', 'UGT2B7'],
        eaa_effect_years=2.9,
        eaa_95ci=(2.5, 3.4),
        withdrawal_symptoms=['Kas ağrısı', 'İshal', 'Bulantı', 'Anksiyete', 'Uykusuzluk', 'Terleme'],
        treatment_options=['Metadon', 'Buprenorfin', 'Naltrexon', 'Klonidin'],
        street_names=['M', 'Miss Emma', 'Monkey', 'White stuff'],
        detection_window={'İdrar': '2-4 gün', 'Kan': '12 saat', 'Saç': '90 gün'}
    ),
    
    'heroin': SubstanceProfile(
        name="Heroin (Diacetylmorphine)",
        turkish_name="Eroin",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="Morfine hızla metabolize olur, mu-opioid agonisti",
        primary_targets=['OPRM1'],
        receptor_affinity={'OPRM1': 'Prodrug → Morfin'},
        gwas_genes=['OPRM1', 'OPRD1', 'PDYN', 'PENK', 'COMT', 'DRD2', 'DRD4'],
        methylation_cpgs=['cg23480021', 'cg02722814', 'cg19859270', 'cg00574958'],
        pharmacogenes=['CYP2D6', 'CYP3A4', 'OPRM1', 'UGT2B7', 'ABCB1'],
        eaa_effect_years=3.8,
        eaa_95ci=(3.2, 4.5),
        withdrawal_symptoms=['Şiddetli kas ağrısı', 'Kemik ağrısı', 'İshal', 'Kusma', 'Soğuk terleme', 'Bacak huzursuzluğu'],
        treatment_options=['Metadon', 'Buprenorfin/Nalokson', 'Naltrexon XR'],
        street_names=['H', 'Smack', 'Dope', 'Horse', 'Junk', 'Brown sugar'],
        detection_window={'İdrar': '2-7 gün', 'Kan': '6 saat', 'Saç': '90 gün'}
    ),
    
    'fentanyl': SubstanceProfile(
        name="Fentanyl",
        turkish_name="Fentanil",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="Sentetik mu-opioid tam agonisti, morfinden 50-100x güçlü",
        primary_targets=['OPRM1'],
        receptor_affinity={'OPRM1': 'Ki=0.39 nM (yüksek afinite)'},
        gwas_genes=['OPRM1', 'CYP3A4', 'CYP3A5', 'ABCB1', 'COMT'],
        methylation_cpgs=['cg23480021', 'cg02722814'],
        pharmacogenes=['CYP3A4', 'CYP3A5', 'OPRM1', 'ABCB1'],
        eaa_effect_years=4.2,
        eaa_95ci=(3.5, 5.0),
        withdrawal_symptoms=['Çok şiddetli yoksunluk', 'Kas spazmları', 'Şiddetli anksiyete'],
        treatment_options=['Buprenorfin (yüksek doz)', 'Metadon', 'Hastane detoksu'],
        street_names=['China White', 'Apache', 'Dance Fever', 'Murder 8'],
        detection_window={'İdrar': '1-3 gün', 'Kan': '12 saat', 'Saç': '90 gün'}
    ),
    
    'oxycodone': SubstanceProfile(
        name="Oxycodone",
        turkish_name="Oksikodon",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="Semi-sentetik mu ve kappa opioid agonisti",
        primary_targets=['OPRM1', 'OPRK1'],
        receptor_affinity={'OPRM1': 'Ki=18 nM', 'OPRK1': 'Ki=677 nM'},
        gwas_genes=['OPRM1', 'CYP2D6', 'CYP3A4', 'ABCB1', 'COMT'],
        pharmacogenes=['CYP2D6', 'CYP3A4', 'OPRM1', 'UGT2B7'],
        eaa_effect_years=2.8,
        eaa_95ci=(2.3, 3.4),
        street_names=['Oxy', 'OC', 'Hillbilly heroin', 'Percs'],
        detection_window={'İdrar': '3-4 gün', 'Kan': '24 saat', 'Saç': '90 gün'}
    ),
    
    'methadone': SubstanceProfile(
        name="Methadone",
        turkish_name="Metadon",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="Sentetik mu-opioid agonisti, NMDA antagonisti",
        primary_targets=['OPRM1', 'GRIN1', 'GRIN2B'],
        receptor_affinity={'OPRM1': 'Ki=3.4 nM', 'NMDA': 'Antagonist'},
        gwas_genes=['OPRM1', 'CYP2B6', 'CYP3A4', 'CYP2D6', 'ABCB1'],
        pharmacogenes=['CYP2B6', 'CYP3A4', 'CYP2D6', 'OPRM1', 'ABCB1', 'KCNH2'],
        treatment_options=['Yavaş azaltma', 'Buprenorfine geçiş'],
        street_names=['Methadose', 'Dollies', 'Fizzies'],
        detection_window={'İdrar': '7-10 gün', 'Kan': '24-36 saat', 'Saç': '90 gün'}
    ),
    
    'buprenorphine': SubstanceProfile(
        name="Buprenorphine",
        turkish_name="Buprenorfin",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_III,
        mechanism_of_action="Parsiyel mu-agonist, kappa-antagonist",
        primary_targets=['OPRM1', 'OPRK1', 'OPRD1'],
        receptor_affinity={'OPRM1': 'Parsiyel agonist', 'OPRK1': 'Antagonist'},
        gwas_genes=['OPRM1', 'CYP3A4', 'CYP2C8', 'ABCB1'],
        pharmacogenes=['CYP3A4', 'CYP2C8', 'OPRM1', 'UGT1A1'],
        treatment_options=['Opioid bağımlılığı tedavisinde kullanılır'],
        street_names=['Bupe', 'Subs', 'Strips'],
        detection_window={'İdrar': '7-14 gün', 'Kan': '24 saat', 'Saç': '90 gün'}
    ),
    
    'tramadol': SubstanceProfile(
        name="Tramadol",
        turkish_name="Tramadol",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_IV,
        mechanism_of_action="Zayıf mu-agonist + SNRI aktivitesi",
        primary_targets=['OPRM1', 'SLC6A4', 'SLC6A2'],
        receptor_affinity={'OPRM1': 'Zayıf', 'SERT': 'İnhibisyon', 'NET': 'İnhibisyon'},
        gwas_genes=['OPRM1', 'CYP2D6', 'CYP3A4', 'SLC6A4'],
        pharmacogenes=['CYP2D6', 'CYP3A4', 'CYP2B6', 'OPRM1'],
        street_names=['Trams', 'Ultras', 'Chill pills'],
        detection_window={'İdrar': '2-4 gün', 'Kan': '12-24 saat'}
    ),
    
    'codeine': SubstanceProfile(
        name="Codeine",
        turkish_name="Kodein",
        class_type=SubstanceClass.OPIOIDS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="Prodrug, CYP2D6 ile morfine dönüşür",
        primary_targets=['OPRM1'],
        receptor_affinity={'OPRM1': 'Prodrug'},
        gwas_genes=['OPRM1', 'CYP2D6', 'UGT2B7'],
        pharmacogenes=['CYP2D6', 'UGT2B7', 'OPRM1', 'ABCB1'],
        street_names=['Captain Cody', 'Cody', 'Lean', 'Purple drank'],
        detection_window={'İdrar': '1-3 gün', 'Kan': '12 saat'}
    )
}


STIMULANT_SUBSTANCES = {
    # nrcdnl94
    'cocaine': SubstanceProfile(
        name="Cocaine",
        turkish_name="Kokain",
        class_type=SubstanceClass.STIMULANTS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="DAT, NET, SERT blokajı (triple reuptake inhibitör)",
        primary_targets=['SLC6A3', 'SLC6A2', 'SLC6A4'],
        receptor_affinity={'DAT': 'IC50=0.5 μM', 'NET': 'IC50=0.8 μM', 'SERT': 'IC50=2.0 μM'},
        gwas_genes=['SLC6A3', 'DRD2', 'DRD4', 'COMT', 'DBH', 'BDNF', 'CHRNA5'],
        methylation_cpgs=['cg03636183', 'cg19859270', 'cg05575921', 'cg21566642'],
        pharmacogenes=['CYP3A4', 'BCHE', 'CES1', 'COMT', 'DBH'],
        eaa_effect_years=4.1,
        eaa_95ci=(3.5, 4.7),
        withdrawal_symptoms=['Depresyon', 'Yorgunluk', 'Uyku bozukluğu', 'Aşırı iştah', 'Anhedoni'],
        treatment_options=['Disulfiram', 'N-asetilsistein', 'Modafinil', 'Topiramat'],
        street_names=['Coke', 'Blow', 'Snow', 'Powder', 'White'],
        detection_window={'İdrar': '2-4 gün', 'Kan': '12-24 saat', 'Saç': '90 gün'}
    ),
    
    'methamphetamine': SubstanceProfile(
        name="Methamphetamine",
        turkish_name="Metamfetamin",
        class_type=SubstanceClass.STIMULANTS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="Veziküler DA/NE salınımı, MAO inhibisyonu, DAT reversal",
        primary_targets=['SLC6A3', 'SLC18A2', 'MAOA', 'MAOB'],
        receptor_affinity={'DAT': 'Substrat', 'VMAT2': 'İnhibitör', 'TAAR1': 'Agonist'},
        gwas_genes=['SLC6A3', 'DRD2', 'DRD4', 'COMT', 'MAOA', 'BDNF', 'OPRM1'],
        methylation_cpgs=['cg05575921', 'cg03636183', 'cg21566642', 'cg06126421'],
        pharmacogenes=['CYP2D6', 'CYP3A4', 'COMT', 'DBH', 'SLC6A3'],
        eaa_effect_years=6.2,
        eaa_95ci=(4.5, 8.1),
        withdrawal_symptoms=['Şiddetli depresyon', 'Psikoz', 'Anhedoni', 'Aşırı uyku', 'Paranoya'],
        treatment_options=['Bupropion', 'Naltrexon', 'Mirtazapin', 'N-asetilsistein'],
        street_names=['Meth', 'Crystal', 'Ice', 'Glass', 'Tina', 'Speed'],
        detection_window={'İdrar': '3-7 gün', 'Kan': '1-3 gün', 'Saç': '90 gün'}
    ),
    
    'amphetamine': SubstanceProfile(
        name="Amphetamine",
        turkish_name="Amfetamin",
        class_type=SubstanceClass.STIMULANTS,
        addiction_potential=AddictionPotential.HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="DA/NE salınımı, DAT reversal, VMAT2 inhibisyonu",
        primary_targets=['SLC6A3', 'SLC6A2', 'SLC18A2'],
        receptor_affinity={'DAT': 'Substrat', 'NET': 'Substrat'},
        gwas_genes=['SLC6A3', 'DRD2', 'DRD4', 'COMT', 'DBH', 'SNAP25'],
        pharmacogenes=['CYP2D6', 'CYP3A4', 'COMT', 'SLC6A3'],
        eaa_effect_years=3.5,
        eaa_95ci=(2.8, 4.2),
        street_names=['Speed', 'Uppers', 'Bennies', 'Black beauties'],
        detection_window={'İdrar': '2-4 gün', 'Kan': '12-24 saat'}
    ),
    
    'mdma': SubstanceProfile(
        name="MDMA (3,4-Methylenedioxymethamphetamine)",
        turkish_name="Ekstazi",
        class_type=SubstanceClass.STIMULANTS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="Serotonin salınımı > Dopamin > Norepinefrin",
        primary_targets=['SLC6A4', 'SLC6A3', 'SLC6A2', 'HTR2A'],
        receptor_affinity={'SERT': 'Substrat (primer)', 'DAT': 'Substrat', 'NET': 'Substrat'},
        gwas_genes=['SLC6A4', 'HTR2A', 'COMT', 'TPH2', 'BDNF'],
        pharmacogenes=['CYP2D6', 'CYP3A4', 'CYP2B6', 'CYP1A2', 'COMT'],
        eaa_effect_years=1.8,
        eaa_95ci=(1.2, 2.5),
        street_names=['Ecstasy', 'Molly', 'X', 'E', 'Adam', 'Love drug'],
        detection_window={'İdrar': '2-4 gün', 'Kan': '24-48 saat'}
    ),
    
    'methylphenidate': SubstanceProfile(
        name="Methylphenidate",
        turkish_name="Metilfenidat",
        class_type=SubstanceClass.STIMULANTS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="DAT ve NET inhibitörü (reuptake bloker)",
        primary_targets=['SLC6A3', 'SLC6A2'],
        receptor_affinity={'DAT': 'Ki=34 nM', 'NET': 'Ki=339 nM'},
        gwas_genes=['SLC6A3', 'DRD4', 'SNAP25', 'COMT', 'ADRA2A'],
        pharmacogenes=['CES1', 'SLC6A3', 'DRD4', 'COMT', 'ADRA2A'],
        treatment_options=['ADHD tedavisi'],
        street_names=['Ritalin', 'Kiddie coke', 'Vitamin R'],
        detection_window={'İdrar': '1-2 gün', 'Kan': '12 saat'}
    ),
    
    'cathinone': SubstanceProfile(
        name="Synthetic Cathinones",
        turkish_name="Sentetik Katinonlar",
        class_type=SubstanceClass.STIMULANTS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="DAT/NET/SERT substratları veya inhibitörleri",
        primary_targets=['SLC6A3', 'SLC6A2', 'SLC6A4'],
        receptor_affinity={'DAT': 'Değişken', 'NET': 'Değişken', 'SERT': 'Değişken'},
        gwas_genes=['SLC6A3', 'DRD2', 'COMT'],
        eaa_effect_years=4.5,
        eaa_95ci=(3.5, 5.8),
        street_names=['Bath salts', 'Flakka', 'Cloud 9', 'Vanilla sky'],
        detection_window={'İdrar': '2-4 gün', 'Kan': '24 saat'}
    )
}


DEPRESSANT_SUBSTANCES = {
    # nrcdnl94
    'alcohol': SubstanceProfile(
        name="Ethanol",
        turkish_name="Alkol",
        class_type=SubstanceClass.DEPRESSANTS,
        addiction_potential=AddictionPotential.HIGH,
        legal_status=LegalStatus.UNSCHEDULED,
        mechanism_of_action="GABA-A pozitif modülatör, NMDA antagonist, opioid salınımı",
        primary_targets=['GABRA1', 'GABRA2', 'GRIN1', 'GRIN2B', 'OPRM1'],
        receptor_affinity={'GABA-A': 'Pozitif modülatör', 'NMDA': 'Antagonist'},
        gwas_genes=['ADH1B', 'ADH1C', 'ALDH2', 'GABRA2', 'CHRM2', 'DRD2', 'OPRM1', 'GCKR'],
        methylation_cpgs=['cg05575921', 'cg23193759', 'cg03636183', 'cg06126421', 'cg21161138'],
        pharmacogenes=['ADH1B', 'ADH1C', 'ALDH2', 'CYP2E1', 'OPRM1', 'GABRA2'],
        eaa_effect_years=3.6,
        eaa_95ci=(3.1, 4.2),
        withdrawal_symptoms=['Tremor', 'Terleme', 'Anksiyete', 'Nöbet', 'Delirium tremens', 'Halüsinasyon'],
        treatment_options=['Disulfiram', 'Naltrexon', 'Akamprosat', 'Gabapentin', 'Topiramat'],
        street_names=['Booze', 'Hooch', 'Sauce', 'Spirits'],
        detection_window={'Nefes': '12-24 saat', 'İdrar': '12-48 saat', 'Kan': '12 saat'}
    ),
    
    'benzodiazepines': SubstanceProfile(
        name="Benzodiazepines",
        turkish_name="Benzodiazepinler",
        class_type=SubstanceClass.DEPRESSANTS,
        addiction_potential=AddictionPotential.HIGH,
        legal_status=LegalStatus.SCHEDULE_IV,
        mechanism_of_action="GABA-A reseptör pozitif allosterik modülatör",
        primary_targets=['GABRA1', 'GABRA2', 'GABRA3', 'GABRA5', 'GABRG2'],
        receptor_affinity={'GABA-A': 'PAM (Cl- kanalı frekansını artırır)'},
        gwas_genes=['GABRA2', 'GABRA4', 'GABRG2', 'OPRM1'],
        pharmacogenes=['CYP3A4', 'CYP2C19', 'CYP2D6', 'UGT2B15', 'GABRA2'],
        eaa_effect_years=2.1,
        eaa_95ci=(1.5, 2.8),
        withdrawal_symptoms=['Nöbet (hayati tehlike)', 'Rebound anksiyete', 'Uykusuzluk', 'Tremor', 'Panik'],
        treatment_options=['Yavaş tapering', 'Diazepam protokolü', 'Fenobarbital'],
        street_names=['Benzos', 'Downers', 'Bars (Xanax)', 'Tranks'],
        detection_window={'İdrar': '3-30 gün', 'Kan': '1-3 gün'}
    ),
    
    'barbiturates': SubstanceProfile(
        name="Barbiturates",
        turkish_name="Barbitüratlar",
        class_type=SubstanceClass.DEPRESSANTS,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="GABA-A reseptör agonist, Cl- kanalı süresini uzatır",
        primary_targets=['GABRA1', 'GABRB2', 'GABRB3'],
        receptor_affinity={'GABA-A': 'Direkt aktivatör (yüksek dozda)'},
        gwas_genes=['GABRA1', 'GABRB2', 'CYP2C9', 'CYP2C19'],
        pharmacogenes=['CYP2C9', 'CYP2C19', 'CYP3A4'],
        withdrawal_symptoms=['Nöbet', 'Delirium', 'Hipertermi', 'Ölüm riski'],
        treatment_options=['Yavaş tapering', 'Fenobarbital geçişi'],
        street_names=['Barbs', 'Reds', 'Yellow jackets', 'Downers'],
        detection_window={'İdrar': '1-3 hafta', 'Kan': '1-2 gün'}
    ),
    
    'ghb': SubstanceProfile(
        name="GHB (Gamma-Hydroxybutyrate)",
        turkish_name="GHB",
        class_type=SubstanceClass.DEPRESSANTS,
        addiction_potential=AddictionPotential.HIGH,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="GABA-B agonist, GHB reseptör agonist",
        primary_targets=['GABBR1', 'GABBR2', 'HCAR1'],
        receptor_affinity={'GABA-B': 'Agonist', 'GHB-R': 'Agonist'},
        gwas_genes=['GABBR1', 'GABBR2', 'ALDH5A1'],
        withdrawal_symptoms=['Psikoz', 'Tremor', 'Taşikardi', 'Delirium', 'Nöbet'],
        treatment_options=['Benzodiazepin', 'Baklofen', 'Fenobarbital'],
        street_names=['G', 'Liquid ecstasy', 'Fantasy', 'Soap'],
        detection_window={'İdrar': '12 saat', 'Kan': '4-8 saat'}
    ),
    
    'z_drugs': SubstanceProfile(
        name="Z-Drugs (Zolpidem, Zopiclone)",
        turkish_name="Z-İlaçları",
        class_type=SubstanceClass.DEPRESSANTS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_IV,
        mechanism_of_action="GABA-A α1 subünit selektif pozitif modülatör",
        primary_targets=['GABRA1'],
        receptor_affinity={'GABA-A α1': 'Selektif PAM'},
        gwas_genes=['GABRA1', 'GABRA2'],
        pharmacogenes=['CYP3A4', 'CYP2C9', 'CYP1A2'],
        street_names=['Ambien', 'Stillnox'],
        detection_window={'İdrar': '1-2 gün', 'Kan': '6-8 saat'}
    )
}


CANNABINOID_SUBSTANCES = {
    # nrcdnl94
    'cannabis': SubstanceProfile(
        name="Cannabis (THC)",
        turkish_name="Esrar/Marihuana",
        class_type=SubstanceClass.CANNABINOIDS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="CB1 ve CB2 reseptör parsiyel agonist",
        primary_targets=['CNR1', 'CNR2'],
        receptor_affinity={'CB1': 'Ki=40 nM', 'CB2': 'Ki=36 nM'},
        gwas_genes=['CNR1', 'FAAH', 'MGLL', 'COMT', 'AKT1', 'DRD2'],
        methylation_cpgs=['cg05575921', 'cg23193759', 'cg21161138'],
        pharmacogenes=['CYP2C9', 'CYP3A4', 'CNR1', 'FAAH', 'COMT', 'AKT1'],
        eaa_effect_years=0.8,
        eaa_95ci=(0.3, 1.4),
        withdrawal_symptoms=['İrritabilite', 'Uyku güçlüğü', 'Azalmış iştah', 'Rüya değişiklikleri', 'Anksiyete'],
        treatment_options=['N-asetilsistein', 'Gabapentin', 'Bilişsel davranışçı terapi'],
        street_names=['Weed', 'Pot', 'Grass', 'Mary Jane', 'Ganja', 'Dope'],
        detection_window={'İdrar': '3-30 gün', 'Kan': '1-2 gün', 'Saç': '90 gün'}
    ),
    
    'synthetic_cannabinoids': SubstanceProfile(
        name="Synthetic Cannabinoids (Spice/K2)",
        turkish_name="Sentetik Kannabinoidler",
        class_type=SubstanceClass.CANNABINOIDS,
        addiction_potential=AddictionPotential.HIGH,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="CB1 tam agonist (THC'den 10-800x güçlü)",
        primary_targets=['CNR1', 'CNR2'],
        receptor_affinity={'CB1': 'Tam agonist (yüksek afinite)'},
        gwas_genes=['CNR1', 'FAAH', 'AKT1'],
        eaa_effect_years=3.2,
        eaa_95ci=(2.5, 4.0),
        withdrawal_symptoms=['Şiddetli anksiyete', 'Psikoz', 'Nöbet', 'Taşikardi'],
        treatment_options=['Benzodiazepin', 'Antipsikotik'],
        street_names=['Spice', 'K2', 'Scooby snax', 'Black mamba', 'Joker'],
        detection_window={'İdrar': '3-4 gün', 'Kan': '24 saat'}
    )
}


HALLUCINOGEN_SUBSTANCES = {
    # nrcdnl94
    'lsd': SubstanceProfile(
        name="LSD (Lysergic acid diethylamide)",
        turkish_name="LSD",
        class_type=SubstanceClass.HALLUCINOGENS,
        addiction_potential=AddictionPotential.LOW,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="5-HT2A parsiyel agonist, D2 agonist",
        primary_targets=['HTR2A', 'HTR2C', 'DRD2'],
        receptor_affinity={'5-HT2A': 'Ki=1.1 nM', 'D2': 'Ki=500 nM'},
        gwas_genes=['HTR2A', 'HTR2C', 'DRD2', 'COMT'],
        pharmacogenes=['CYP3A4', 'CYP2D6', 'HTR2A'],
        street_names=['Acid', 'Tabs', 'Blotter', 'Lucy', 'Dots'],
        detection_window={'İdrar': '1-3 gün', 'Kan': '6-12 saat'}
    ),
    
    'psilocybin': SubstanceProfile(
        name="Psilocybin",
        turkish_name="Psilosibin (Sihirli Mantar)",
        class_type=SubstanceClass.HALLUCINOGENS,
        addiction_potential=AddictionPotential.LOW,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="Psilocine dönüşür, 5-HT2A agonist",
        primary_targets=['HTR2A', 'HTR2C', 'HTR1A'],
        receptor_affinity={'5-HT2A': 'Ki=6 nM', '5-HT1A': 'Ki=190 nM'},
        gwas_genes=['HTR2A', 'HTR1A', 'COMT'],
        pharmacogenes=['CYP3A4', 'UGT1A10', 'HTR2A'],
        street_names=['Shrooms', 'Magic mushrooms', 'Boomers', 'Caps'],
        detection_window={'İdrar': '24 saat', 'Kan': '6 saat'}
    ),
    
    'ketamine': SubstanceProfile(
        name="Ketamine",
        turkish_name="Ketamin",
        class_type=SubstanceClass.HALLUCINOGENS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_III,
        mechanism_of_action="NMDA reseptör antagonisti, opioid aktivite",
        primary_targets=['GRIN1', 'GRIN2A', 'GRIN2B', 'OPRM1', 'OPRD1'],
        receptor_affinity={'NMDA': 'Ki=0.5 μM', 'Mu-opioid': 'Zayıf'},
        gwas_genes=['GRIN1', 'GRIN2A', 'GRIN2B', 'BDNF', 'COMT'],
        pharmacogenes=['CYP3A4', 'CYP2B6', 'CYP2C9'],
        eaa_effect_years=2.0,
        eaa_95ci=(1.4, 2.7),
        treatment_options=['Tedaviye dirençli depresyon için kullanılır'],
        street_names=['Special K', 'K', 'Vitamin K', 'Kit kat', 'Cat valium'],
        detection_window={'İdrar': '3-5 gün', 'Kan': '24 saat'}
    ),
    
    'pcp': SubstanceProfile(
        name="PCP (Phencyclidine)",
        turkish_name="PCP",
        class_type=SubstanceClass.HALLUCINOGENS,
        addiction_potential=AddictionPotential.MODERATE,
        legal_status=LegalStatus.SCHEDULE_II,
        mechanism_of_action="NMDA antagonist, DAT inhibitör, sigma agonist",
        primary_targets=['GRIN1', 'SLC6A3', 'SIGMAR1'],
        receptor_affinity={'NMDA': 'Antagonist', 'DAT': 'İnhibitör', 'Sigma-1': 'Agonist'},
        gwas_genes=['GRIN1', 'GRIN2A', 'SLC6A3', 'SIGMAR1'],
        pharmacogenes=['CYP3A4', 'CYP2D6'],
        street_names=['Angel dust', 'Rocket fuel', 'Wet', 'Sherman'],
        detection_window={'İdrar': '7-14 gün', 'Kan': '24 saat'}
    ),
    
    'dmt': SubstanceProfile(
        name="DMT (N,N-Dimethyltryptamine)",
        turkish_name="DMT",
        class_type=SubstanceClass.HALLUCINOGENS,
        addiction_potential=AddictionPotential.MINIMAL,
        legal_status=LegalStatus.SCHEDULE_I,
        mechanism_of_action="5-HT2A agonist, sigma-1 agonist",
        primary_targets=['HTR2A', 'SIGMAR1', 'TAAR1'],
        receptor_affinity={'5-HT2A': 'Ki=75 nM', 'Sigma-1': 'Ki=14 μM'},
        gwas_genes=['HTR2A', 'SIGMAR1', 'MAOA'],
        pharmacogenes=['MAOA', 'MAOB', 'CYP2D6'],
        street_names=['Spirit molecule', 'Dimitri', 'Businessman\'s trip'],
        detection_window={'İdrar': '24 saat', 'Kan': '2 saat'}
    )
}


NICOTINE_SUBSTANCES = {
    # nrcdnl94
    'nicotine': SubstanceProfile(
        name="Nicotine",
        turkish_name="Nikotin",
        class_type=SubstanceClass.NICOTINE,
        addiction_potential=AddictionPotential.VERY_HIGH,
        legal_status=LegalStatus.UNSCHEDULED,
        mechanism_of_action="Nikotinik asetilkolin reseptör (nAChR) agonist",
        primary_targets=['CHRNA4', 'CHRNB2', 'CHRNA5', 'CHRNA3', 'CHRNB4'],
        receptor_affinity={'α4β2 nAChR': 'Ki=1 nM', 'α7 nAChR': 'Ki=1.7 μM'},
        gwas_genes=['CHRNA5', 'CHRNA3', 'CHRNB4', 'CHRNA4', 'CHRNB2', 'CYP2A6', 'CYP2B6', 'EGLN2', 'DBH'],
        methylation_cpgs=['cg05575921', 'cg03636183', 'cg21566642', 'cg05951221', 'cg01940273', 'cg23576855'],
        pharmacogenes=['CYP2A6', 'CYP2B6', 'CHRNA5', 'CHRNA3', 'CHRNB4', 'COMT', 'DRD2'],
        eaa_effect_years=4.6,
        eaa_95ci=(4.0, 5.3),
        withdrawal_symptoms=['İrritabilite', 'Anksiyete', 'Konsantrasyon güçlüğü', 'Artmış iştah', 'Depresyon'],
        treatment_options=['Vareniklin', 'Bupropion', 'Nikotin replasmanı (yama/sakız)', 'Sitisin'],
        street_names=['Cigs', 'Smokes', 'Sticks', 'Cancer sticks'],
        detection_window={'İdrar': '3-4 gün (kotinin)', 'Kan': '1-3 gün', 'Saç': '90 gün'}
    )
}


NEUROTRANSMITTER_GENE_SYSTEMS = {
    # nrcdnl94
    'dopamine_system': {
        'description': 'Dopamin sentezi, transportu, reseptörleri ve sinyal iletimi',
        'n_genes': 267,
        'key_genes': {
            'receptors': ['DRD1', 'DRD2', 'DRD3', 'DRD4', 'DRD5'],
            'transporter': ['SLC6A3'],
            'synthesis': ['TH', 'DDC', 'GCH1', 'PCBD1'],
            'degradation': ['COMT', 'MAOA', 'MAOB'],
            'signaling': ['DARPP-32/PPP1R1B', 'GNAL', 'GNAO1', 'ARRB1', 'ARRB2']
        },
        'addiction_relevance': 'Ödül ve pekiştirmenin temel mekanizması, tüm bağımlılık yapıcı maddeler dolaylı/doğrudan dopamin artırır'
    },
    
    'serotonin_system': {
        'description': '5-HT sentezi, transportu ve reseptörleri',
        'n_genes': 142,
        'key_genes': {
            'receptors': ['HTR1A', 'HTR1B', 'HTR2A', 'HTR2C', 'HTR3A', 'HTR4', 'HTR6', 'HTR7'],
            'transporter': ['SLC6A4'],
            'synthesis': ['TPH1', 'TPH2'],
            'degradation': ['MAOA', 'MAOB']
        },
        'addiction_relevance': 'Duygudurum, dürtüsellik, MDMA/halüsinojen etkileri'
    },
    
    'opioid_system': {
        'description': 'Opioid reseptörleri ve endojen ligandlar',
        'n_genes': 98,
        'key_genes': {
            'receptors': ['OPRM1', 'OPRD1', 'OPRK1', 'OPRL1'],
            'ligands': ['PDYN', 'PENK', 'POMC'],
            'signaling': ['ARRB2', 'GRK2', 'GRK3']
        },
        'addiction_relevance': 'Opioid bağımlılığı, ağrı modülasyonu, alkol ödülü'
    },
    
    'gaba_system': {
        'description': 'GABA reseptörleri ve metabolizması',
        'n_genes': 156,
        'key_genes': {
            'gabaa_receptors': ['GABRA1', 'GABRA2', 'GABRA3', 'GABRA4', 'GABRA5', 'GABRA6',
                               'GABRB1', 'GABRB2', 'GABRB3', 'GABRG1', 'GABRG2', 'GABRG3'],
            'gabab_receptors': ['GABBR1', 'GABBR2'],
            'transporters': ['SLC6A1', 'SLC6A11', 'SLC6A12'],
            'metabolism': ['GAD1', 'GAD2', 'ABAT']
        },
        'addiction_relevance': 'Alkol, benzodiazepin, barbitürat etkileri'
    },
    
    'glutamate_system': {
        'description': 'Glutamat reseptörleri ve transporterleri',
        'n_genes': 189,
        'key_genes': {
            'nmda_receptors': ['GRIN1', 'GRIN2A', 'GRIN2B', 'GRIN2C', 'GRIN2D'],
            'ampa_receptors': ['GRIA1', 'GRIA2', 'GRIA3', 'GRIA4'],
            'mglur_receptors': ['GRM1', 'GRM2', 'GRM3', 'GRM5', 'GRM7', 'GRM8'],
            'transporters': ['SLC1A1', 'SLC1A2', 'SLC1A3']
        },
        'addiction_relevance': 'Sinaptik plastisite, öğrenme, PCP/ketamin etkileri'
    },
    
    'cannabinoid_system': {
        'description': 'Endokannabinoid sistemi',
        'n_genes': 67,
        'key_genes': {
            'receptors': ['CNR1', 'CNR2'],
            'synthesis': ['DAGLA', 'DAGLB', 'NAPEPLD'],
            'degradation': ['FAAH', 'MGLL'],
            'related': ['TRPV1', 'GPR55']
        },
        'addiction_relevance': 'Kannabis etkileri, retrograd sinyal, ödül modülasyonu'
    },
    
    'cholinergic_system': {
        'description': 'Asetilkolin reseptörleri',
        'n_genes': 143,
        'key_genes': {
            'nicotinic': ['CHRNA3', 'CHRNA4', 'CHRNA5', 'CHRNA7', 'CHRNB2', 'CHRNB4'],
            'muscarinic': ['CHRM1', 'CHRM2', 'CHRM3', 'CHRM4', 'CHRM5'],
            'metabolism': ['CHAT', 'ACHE', 'BCHE']
        },
        'addiction_relevance': 'Nikotin bağımlılığı, kognitif fonksiyon'
    },
    
    'adrenergic_system': {
        'description': 'Norepinefrin reseptörleri ve transportu',
        'n_genes': 110,
        'key_genes': {
            'receptors': ['ADRA1A', 'ADRA2A', 'ADRA2B', 'ADRB1', 'ADRB2'],
            'transporter': ['SLC6A2'],
            'synthesis': ['DBH', 'PNMT']
        },
        'addiction_relevance': 'Stres yanıtı, yoksunluk belirtileri, stimulan etkileri'
    }
}


EPIGENETIC_REGULATION_GENES = {
    # nrcdnl94
    'dna_methylation': {
        'writers': ['DNMT1', 'DNMT3A', 'DNMT3B'],
        'erasers': ['TET1', 'TET2', 'TET3'],
        'readers': ['MECP2', 'MBD1', 'MBD2', 'MBD3', 'MBD4']
    },
    
    'histone_modification': {
        'acetylation': {
            'writers': ['KAT2A', 'KAT2B', 'KAT5', 'EP300', 'CREBBP'],
            'erasers': ['HDAC1', 'HDAC2', 'HDAC3', 'HDAC4', 'HDAC5', 'HDAC6', 
                       'HDAC7', 'HDAC8', 'HDAC9', 'HDAC10', 'HDAC11',
                       'SIRT1', 'SIRT2', 'SIRT3', 'SIRT6', 'SIRT7']
        },
        'methylation': {
            'writers': ['EZH2', 'SUV39H1', 'G9A/EHMT2', 'SETDB1', 'DOT1L'],
            'erasers': ['KDM1A', 'KDM1B', 'KDM2A', 'KDM4A', 'KDM5A', 'KDM6A', 'KDM6B']
        }
    },
    
    'chromatin_remodeling': ['SWI/SNF', 'SMARCA4', 'SMARCA2', 'ARID1A', 'ARID1B'],
    
    'transcription_factors': {
        'creb_family': ['CREB1', 'CREB3', 'CREB5', 'ATF1', 'ATF2', 'ATF3', 'ATF4'],
        'fos_jun': ['FOS', 'FOSB', 'FOSL1', 'FOSL2', 'JUN', 'JUNB', 'JUND'],
        'nfkb': ['NFKB1', 'NFKB2', 'RELA', 'RELB', 'REL'],
        'nuclear_receptors': ['NR3C1', 'NR3C2', 'NR4A1', 'NR4A2', 'NR4A3']
    }
}


STRESS_HPA_GENES = {
    # nrcdnl94
    'crh_system': ['CRH', 'CRHR1', 'CRHR2', 'CRHBP', 'UCN', 'UCN2', 'UCN3'],
    'glucocorticoid': ['NR3C1', 'NR3C2', 'FKBP5', 'FKBP4', 'HSP90AA1'],
    'vasopressin_oxytocin': ['AVP', 'AVPR1A', 'AVPR1B', 'OXT', 'OXTR', 'CD38'],
    'cortisol_metabolism': ['HSD11B1', 'HSD11B2', 'CYP11A1', 'CYP11B1', 'CYP17A1']
}


NEUROPLASTICITY_GENES = {
    # nrcdnl94
    'neurotrophic_factors': {
        'neurotrophins': ['NGF', 'BDNF', 'NTF3', 'NTF4'],
        'receptors': ['NTRK1', 'NTRK2', 'NTRK3', 'NGFR'],
        'gdnf_family': ['GDNF', 'NRTN', 'ARTN', 'PSPN']
    },
    
    'synaptic_plasticity': {
        'ltp': ['CAMK2A', 'CAMK2B', 'PRKCA', 'PRKCB', 'MAPK1', 'MAPK3', 'CREB1'],
        'ltd': ['PPP1CA', 'PPP2CA', 'PTEN', 'CALM1'],
        'structural': ['ARC', 'HOMER1', 'SHANK1', 'SHANK2', 'SHANK3', 'DLG4']
    },
    
    'immediate_early_genes': ['FOS', 'FOSB', 'JUN', 'EGR1', 'EGR2', 'EGR3', 'ARC', 'HOMER1']
}


GWAS_CATALOG_ADDICTION = {
    # nrcdnl94
    'alcohol_dependence': {
        'study_id': 'GCST90012877',
        'pmid': '30643251',
        'citation': 'Walters et al. 2018 Nat Neurosci',
        'n_samples': 274424,
        'n_snps': 9690082,
        'top_loci': [
            {'rsid': 'rs1229984', 'gene': 'ADH1B', 'p': 9.8e-94, 'or': 0.75, 'chr': 4},
            {'rsid': 'rs671', 'gene': 'ALDH2', 'p': 1.2e-45, 'or': 0.65, 'chr': 12},
            {'rsid': 'rs1260326', 'gene': 'GCKR', 'p': 2.1e-15, 'or': 1.08, 'chr': 2},
            {'rsid': 'rs11940694', 'gene': 'KLB', 'p': 7.8e-12, 'or': 1.07, 'chr': 4},
            {'rsid': 'rs2066702', 'gene': 'ADH1C', 'p': 3.2e-11, 'or': 0.82, 'chr': 4}
        ]
    },
    
    'opioid_dependence': {
        'study_id': 'GCST90000032',
        'pmid': '32042166',
        'citation': 'Polimanti et al. 2020 MVP',
        'n_samples': 82707,
        'n_snps': 7200000,
        'top_loci': [
            {'rsid': 'rs1799971', 'gene': 'OPRM1', 'p': 1.5e-9, 'or': 1.15, 'chr': 6},
            {'rsid': 'rs78589099', 'gene': 'FURIN', 'p': 4.2e-8, 'or': 0.91, 'chr': 15},
            {'rsid': 'rs1799972', 'gene': 'OPRM1', 'p': 2.1e-7, 'or': 1.12, 'chr': 6}
        ]
    },
    
    'nicotine_dependence': {
        'study_id': 'GCST007474',
        'pmid': '30643251',
        'citation': 'Liu et al. 2019 GSCAN',
        'n_samples': 1232091,
        'n_snps': 12000000,
        'top_loci': [
            {'rsid': 'rs16969968', 'gene': 'CHRNA5', 'p': 2.3e-194, 'or': 1.35, 'chr': 15},
            {'rsid': 'rs1051730', 'gene': 'CHRNA3', 'p': 1.8e-180, 'or': 1.32, 'chr': 15},
            {'rsid': 'rs588765', 'gene': 'CHRNA5', 'p': 5.4e-120, 'or': 1.25, 'chr': 15},
            {'rsid': 'rs6495308', 'gene': 'CHRNA3', 'p': 2.1e-98, 'or': 1.22, 'chr': 15},
            {'rsid': 'rs4105144', 'gene': 'CYP2A6', 'p': 8.7e-45, 'or': 0.85, 'chr': 19}
        ]
    },
    
    'cannabis_use_disorder': {
        'study_id': 'GCST90016614',
        'pmid': '32747698',
        'citation': 'Johnson et al. 2020 Lancet Psychiatry',
        'n_samples': 384032,
        'top_loci': [
            {'rsid': 'rs56372821', 'gene': 'FOXP2', 'p': 2.8e-10, 'or': 1.12, 'chr': 7},
            {'rsid': 'rs1409568', 'gene': 'CHRNA2', 'p': 4.1e-9, 'or': 1.09, 'chr': 8}
        ]
    },
    
    'cocaine_dependence': {
        'study_id': 'GCST003085',
        'pmid': '28967357',
        'citation': 'Cabana-Domínguez et al. 2019',
        'n_samples': 4300,
        'top_loci': [
            {'rsid': 'rs2629540', 'gene': 'NCAM1', 'p': 3.5e-6, 'or': 1.28, 'chr': 11},
            {'rsid': 'rs806379', 'gene': 'CNR1', 'p': 8.2e-5, 'or': 1.15, 'chr': 6}
        ]
    }
}


EWAS_CATALOG_ADDICTION = {
    # nrcdnl94
    'tobacco_smoking': {
        'n_publications': 30,
        'n_cpgs': 2568,
        'top_cpgs': [
            {'cpg': 'cg05575921', 'gene': 'AHRR', 'delta_beta': -0.21, 'p': 1.2e-156, 'direction': 'hypomethylated'},
            {'cpg': 'cg03636183', 'gene': 'F2RL3', 'delta_beta': -0.15, 'p': 3.4e-98, 'direction': 'hypomethylated'},
            {'cpg': 'cg21566642', 'gene': '2q37.1', 'delta_beta': -0.08, 'p': 2.1e-67, 'direction': 'hypomethylated'},
            {'cpg': 'cg05951221', 'gene': '2q37.1', 'delta_beta': -0.07, 'p': 8.9e-54, 'direction': 'hypomethylated'},
            {'cpg': 'cg01940273', 'gene': '2q37.1', 'delta_beta': -0.06, 'p': 1.5e-48, 'direction': 'hypomethylated'}
        ],
        'biomarker_auc': 0.96
    },
    
    'alcohol_use_disorder': {
        'n_publications': 6,
        'n_cpgs': 105,
        'top_cpgs': [
            {'cpg': 'cg05575921', 'gene': 'AHRR', 'delta_beta': -0.08, 'p': 2.3e-12, 'tissue': 'blood'},
            {'cpg': 'cg23193759', 'gene': 'AHRR', 'delta_beta': -0.05, 'p': 5.6e-9, 'tissue': 'blood'},
            {'cpg': 'cg06126421', 'gene': 'IER3', 'delta_beta': 0.03, 'p': 1.2e-7, 'tissue': 'NAc'}
        ],
        'tissues': ['Peripheral blood', 'Nucleus accumbens', 'DLPFC']
    },
    
    'opioid_dependence': {
        'n_publications': 4,
        'n_cpgs': 78,
        'top_cpgs': [
            {'cpg': 'cg23480021', 'gene': 'OPRM1', 'delta_beta': 0.05, 'p': 3.2e-8, 'tissue': 'brain'},
            {'cpg': 'cg02722814', 'gene': 'PARG', 'delta_beta': -0.04, 'p': 7.8e-7, 'tissue': 'blood'},
            {'cpg': 'cg19859270', 'gene': 'NTN1', 'delta_beta': 0.03, 'p': 2.1e-6, 'tissue': 'brain'}
        ]
    },
    
    'methamphetamine': {
        'n_publications': 2,
        'geo_accession': 'GSE154971',
        'top_pathways': ['Circadian entrainment', 'CAV2 signaling']
    }
}


PHARMACOGENOMICS_ADDICTION = {
    # nrcdnl94
    'opioid_therapy': {
        'CYP2D6': {
            'drug_examples': ['Codeine', 'Tramadol', 'Hydrocodone', 'Oxycodone'],
            'phenotypes': {
                'poor_metabolizer': 'Reduced efficacy for prodrugs, consider alternatives',
                'intermediate_metabolizer': 'Reduced efficacy, monitor response',
                'normal_metabolizer': 'Standard dosing',
                'ultrarapid_metabolizer': 'Increased toxicity risk, use alternatives or lower dose'
            },
            'cpic_guideline': 'Yes - Codeine, Tramadol'
        },
        'OPRM1': {
            'rs1799971': {
                'A118G': 'Reduced opioid sensitivity, may need higher doses',
                'clinical_use': 'Naltrexone response prediction'
            }
        },
        'CYP3A4': {
            'drug_examples': ['Fentanyl', 'Methadone', 'Buprenorphine'],
            'note': 'Major metabolizing enzyme, drug interactions common'
        }
    },
    
    'alcohol_therapy': {
        'ADH1B': {
            'rs1229984': 'His48Arg - Protective, faster acetaldehyde accumulation',
            'frequency_asian': 0.70,
            'frequency_european': 0.05
        },
        'ALDH2': {
            'rs671': 'Glu504Lys - "Asian flush", 6-10x higher esophageal cancer risk if drinking',
            'frequency_asian': 0.30,
            'frequency_european': 0.001
        },
        'OPRM1': {
            'rs1799971': 'May predict naltrexone response',
            'evidence_level': 'Moderate'
        }
    },
    
    'nicotine_therapy': {
        'CYP2A6': {
            'role': 'Primary nicotine metabolism (70-80%)',
            'phenotypes': {
                'poor_metabolizer': 'Lower nicotine intake, easier cessation, lower NRT dose',
                'normal_metabolizer': 'Standard cessation approach',
                'ultrarapid_metabolizer': 'Higher dependence, varenicline may be preferred'
            }
        },
        'CHRNA5': {
            'rs16969968': 'Risk allele associated with heavier smoking, may benefit from combined therapy'
        }
    },
    
    'stimulant_therapy': {
        'DBH': {
            'C-1021T': 'Affects disulfiram response in cocaine dependence',
            'evidence': 'Preliminary'
        },
        'COMT': {
            'Val158Met': 'Affects dopamine levels, may influence stimulant response',
            'evidence': 'Mixed'
        }
    }
}


def get_all_substances() -> Dict[str, Dict]:
    """Return all substance databases combined"""
    return {
        'opioids': OPIOID_SUBSTANCES,
        'stimulants': STIMULANT_SUBSTANCES,
        'depressants': DEPRESSANT_SUBSTANCES,
        'cannabinoids': CANNABINOID_SUBSTANCES,
        'hallucinogens': HALLUCINOGEN_SUBSTANCES,
        'nicotine': NICOTINE_SUBSTANCES
    }


def get_substance_count() -> Dict[str, int]:
    """Get count of substances by category"""
    all_subs = get_all_substances()
    return {category: len(substances) for category, substances in all_subs.items()}


def search_substance(query: str) -> List[SubstanceProfile]:
    """Search for substances by name or property"""
    results = []
    all_subs = get_all_substances()
    query_lower = query.lower()
    
    for category, substances in all_subs.items():
        for key, profile in substances.items():
            if (query_lower in profile.name.lower() or 
                query_lower in profile.turkish_name.lower() or
                query_lower in key.lower() or
                any(query_lower in sn.lower() for sn in profile.street_names)):
                results.append(profile)
    
    return results


def get_genes_by_system(system: str) -> Dict[str, List[str]]:
    """Get genes for a specific neurotransmitter system"""
    if system in NEUROTRANSMITTER_GENE_SYSTEMS:
        return NEUROTRANSMITTER_GENE_SYSTEMS[system]['key_genes']
    return {}


def get_gwas_for_trait(trait: str) -> Dict:
    """Get GWAS data for addiction trait"""
    trait_lower = trait.lower().replace(' ', '_')
    for key, data in GWAS_CATALOG_ADDICTION.items():
        if trait_lower in key:
            return data
    return {}


def get_methylation_markers(substance_type: str) -> List[Dict]:
    """Get methylation markers for substance type"""
    if substance_type in EWAS_CATALOG_ADDICTION:
        return EWAS_CATALOG_ADDICTION[substance_type].get('top_cpgs', [])
    return []


def get_pharmacogenes(drug_class: str) -> Dict:
    """Get pharmacogenomic information for drug class"""
    if drug_class in PHARMACOGENOMICS_ADDICTION:
        return PHARMACOGENOMICS_ADDICTION[drug_class]
    return {}


def get_database_statistics() -> Dict[str, Any]:
    """Get comprehensive database statistics"""
    all_subs = get_all_substances()
    
    total_substances = sum(len(v) for v in all_subs.values())
    total_genes = sum(sys['n_genes'] for sys in NEUROTRANSMITTER_GENE_SYSTEMS.values())
    total_gwas_snps = sum(d.get('n_snps', 0) for d in GWAS_CATALOG_ADDICTION.values())
    total_ewas_cpgs = sum(d.get('n_cpgs', 0) for d in EWAS_CATALOG_ADDICTION.values())
    
    return {
        'total_substances': total_substances,
        'substance_categories': len(all_subs),
        'neurotransmitter_systems': len(NEUROTRANSMITTER_GENE_SYSTEMS),
        'total_addiction_genes': total_genes,
        'gwas_studies': len(GWAS_CATALOG_ADDICTION),
        'gwas_snps_analyzed': total_gwas_snps,
        'ewas_studies': len(EWAS_CATALOG_ADDICTION),
        'ewas_cpgs_identified': total_ewas_cpgs,
        'pharmacogene_categories': len(PHARMACOGENOMICS_ADDICTION),
        'data_sources': [
            'WHO ICD-11 Classification',
            'UNODC World Drug Report 2024',
            'DEA Controlled Substances Schedules',
            'NHGRI-EBI GWAS Catalog',
            'EWAS Catalog (MRC-IEU)',
            'PharmGKB',
            'CPIC Guidelines',
            'PGC-SUD Consortium',
            '1000 Genomes Project',
            'gnomAD v4'
        ]
    }


# End of module - # nrcdnl94