# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Dynamic Multi-Combination Module - Advanced Synergistic Effects Calculator
Supports unlimited combinations of substances and chronic diseases

This module implements:
- Substance-Substance synergies (e.g., alcohol + opioids, cocaine + methamphetamine)
- Disease-Disease synergies (e.g., diabetes + hypertension, COPD + heart failure)
- Cross-category synergies (substance + disease)
- Dynamic multi-combination calculator with exponential risk scaling

Author: Dr. Nurcan Denli Bayır
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import itertools
import pandas as pd
import math


class RiskLevel(Enum):
    # nrcdnl94
    MINIMAL = ("Minimal", "#22c55e", 0, 2)
    LOW = ("Düşük", "#84cc16", 2, 4)
    MODERATE = ("Orta", "#eab308", 4, 7)
    HIGH = ("Yüksek", "#f97316", 7, 10)
    VERY_HIGH = ("Çok Yüksek", "#ef4444", 10, 15)
    CRITICAL = ("Kritik", "#dc2626", 15, 20)
    EXTREME = ("Aşırı Tehlikeli", "#7f1d1d", 20, float('inf'))


@dataclass
# nrcdnl94
class SubstanceData:
    # nrcdnl94
    """Complete substance data for dynamic calculations"""
    key: str
    name_tr: str
    name_en: str
    category: str
    base_eaa: float
    ci_lower: float
    ci_upper: float
    clock_type: str
    mechanism: str
    affected_systems: List[str]
    sample_size: int
    reference: str
    pmid: str


@dataclass
# nrcdnl94
class DiseaseData:
    # nrcdnl94
    """Complete disease data for dynamic calculations"""
    key: str
    name_tr: str
    name_en: str
    category: str
    base_eaa: float
    ci_lower: float
    ci_upper: float
    mechanism: str
    affected_systems: List[str]
    prevalence: float
    reference: str
    pmid: str


@dataclass
# nrcdnl94
class SynergyData:
    # nrcdnl94
    """Synergy interaction data"""
    type: str  # 'substance-substance', 'disease-disease', 'substance-disease'
    key1: str
    key2: str
    multiplier: float
    mechanism: str
    evidence_level: str
    clinical_warning: str
    reference: str
    pmid: str


SUBSTANCE_DATABASE = {
    # nrcdnl94
    "alcohol_light": SubstanceData(
        key="alcohol_light",
        name_tr="Alkol (Hafif Kullanım)",
        name_en="Alcohol (Light Use)",
        category="Alkol",
        base_eaa=0.5,
        ci_lower=0.2,
        ci_upper=0.8,
        clock_type="GrimAge",
        mechanism="Hafif oksidatif stres",
        affected_systems=["Karaciğer", "Kardiyovasküler"],
        sample_size=3500,
        reference="Rosen AD et al. Alcohol Clin Exp Res. 2018",
        pmid="29336043"
    ),
    "alcohol_moderate": SubstanceData(
        key="alcohol_moderate",
        name_tr="Alkol (Orta Düzey)",
        name_en="Alcohol (Moderate)",
        category="Alkol",
        base_eaa=1.2,
        ci_lower=0.8,
        ci_upper=1.6,
        clock_type="GrimAge",
        mechanism="Oksidatif stres, karaciğer hasarı, inflamasyon",
        affected_systems=["Karaciğer", "Kardiyovasküler", "Nörolojik"],
        sample_size=2183,
        reference="Rosen AD et al. Alcohol Clin Exp Res. 2018",
        pmid="29336043"
    ),
    "alcohol_heavy": SubstanceData(
        key="alcohol_heavy",
        name_tr="Alkol (Ağır Kullanım)",
        name_en="Alcohol (Heavy Use)",
        category="Alkol",
        base_eaa=3.6,
        ci_lower=3.1,
        ci_upper=4.2,
        clock_type="GrimAge",
        mechanism="Kronik hepatotoksisite, nörodejenerasyon, sistemik inflamasyon",
        affected_systems=["Karaciğer", "Kardiyovasküler", "Nörolojik", "Pankreas"],
        sample_size=1542,
        reference="Beach SRH et al. Alcohol Clin Exp Res. 2022",
        pmid="35312089"
    ),
    "alcohol_dependence": SubstanceData(
        key="alcohol_dependence",
        name_tr="Alkol Bağımlılığı",
        name_en="Alcohol Dependence",
        category="Alkol",
        base_eaa=5.2,
        ci_lower=4.5,
        ci_upper=5.9,
        clock_type="GrimAge",
        mechanism="Siroz, Wernicke-Korsakoff, kardiyomiyopati",
        affected_systems=["Karaciğer", "Kardiyovasküler", "Nörolojik", "Pankreas", "Gastrointestinal"],
        sample_size=892,
        reference="Luo A et al. Transl Psychiatry. 2020",
        pmid="32066732"
    ),
    "opioid_prescription": SubstanceData(
        key="opioid_prescription",
        name_tr="Opioid (Reçeteli Kullanım)",
        name_en="Opioid (Prescription Use)",
        category="Opioidler",
        base_eaa=1.5,
        ci_lower=1.0,
        ci_upper=2.0,
        clock_type="GrimAge",
        mechanism="Hafif immün modülasyon, hormonal değişiklikler",
        affected_systems=["Endokrin", "İmmün"],
        sample_size=2100,
        reference="Cheng Z et al. Drug Alcohol Depend. 2021",
        pmid="33862541"
    ),
    "opioid_use": SubstanceData(
        key="opioid_use",
        name_tr="Opioid Kullanımı",
        name_en="Opioid Use",
        category="Opioidler",
        base_eaa=2.9,
        ci_lower=2.5,
        ci_upper=3.4,
        clock_type="GrimAge",
        mechanism="İmmün supresyon, hormonal bozukluk, solunum depresyonu",
        affected_systems=["Endokrin", "İmmün", "Solunum", "Nörolojik"],
        sample_size=1360,
        reference="Cheng Z et al. Drug Alcohol Depend. 2021",
        pmid="33862541"
    ),
    "opioid_dependence": SubstanceData(
        key="opioid_dependence",
        name_tr="Opioid Bağımlılığı",
        name_en="Opioid Dependence",
        category="Opioidler",
        base_eaa=4.8,
        ci_lower=4.1,
        ci_upper=5.5,
        clock_type="GrimAge",
        mechanism="Kronik stres yanıtı, HPA aks disregülasyonu, enfeksiyon riski",
        affected_systems=["Endokrin", "İmmün", "Solunum", "Nörolojik", "Kardiyovasküler"],
        sample_size=756,
        reference="Browne CJ et al. Neuropsychopharmacology. 2020",
        pmid="32349119"
    ),
    "heroin_use": SubstanceData(
        key="heroin_use",
        name_tr="Eroin Kullanımı",
        name_en="Heroin Use",
        category="Opioidler",
        base_eaa=5.5,
        ci_lower=4.8,
        ci_upper=6.2,
        clock_type="GrimAge",
        mechanism="IV kullanım komplikasyonları, enfeksiyon riski, overdoz tehlikesi",
        affected_systems=["Endokrin", "İmmün", "Solunum", "Nörolojik", "Kardiyovasküler", "Cilt"],
        sample_size=420,
        reference="Browne CJ et al. Neuropsychopharmacology. 2020",
        pmid="32349119"
    ),
    "fentanyl_use": SubstanceData(
        key="fentanyl_use",
        name_tr="Fentanil Kullanımı",
        name_en="Fentanyl Use",
        category="Opioidler",
        base_eaa=6.2,
        ci_lower=5.3,
        ci_upper=7.1,
        clock_type="GrimAge",
        mechanism="Yüksek potens, solunum depresyonu, ani ölüm riski",
        affected_systems=["Endokrin", "İmmün", "Solunum", "Nörolojik", "Kardiyovasküler"],
        sample_size=180,
        reference="Browne CJ et al. Neuropsychopharmacology. 2020",
        pmid="32349119"
    ),
    "cocaine_occasional": SubstanceData(
        key="cocaine_occasional",
        name_tr="Kokain (Ara Sıra)",
        name_en="Cocaine (Occasional)",
        category="Kokain",
        base_eaa=2.1,
        ci_lower=1.5,
        ci_upper=2.7,
        clock_type="GrimAge",
        mechanism="Akut kardiyovasküler stres, dopamin düzensizliği",
        affected_systems=["Kardiyovasküler", "Nörolojik"],
        sample_size=850,
        reference="Nylander E et al. Neuropsychopharmacology. 2017",
        pmid="27649641"
    ),
    "cocaine_use": SubstanceData(
        key="cocaine_use",
        name_tr="Kokain Kullanımı",
        name_en="Cocaine Use",
        category="Kokain",
        base_eaa=4.1,
        ci_lower=3.5,
        ci_upper=4.7,
        clock_type="GrimAge",
        mechanism="Kardiyovasküler stres, dopamin toksisitesi, vazokonstriksiyon",
        affected_systems=["Kardiyovasküler", "Nörolojik", "Nazal", "Pulmoner"],
        sample_size=1030,
        reference="Nylander E et al. Neuropsychopharmacology. 2017",
        pmid="27649641"
    ),
    "cocaine_dependence": SubstanceData(
        key="cocaine_dependence",
        name_tr="Kokain Bağımlılığı",
        name_en="Cocaine Dependence",
        category="Kokain",
        base_eaa=5.8,
        ci_lower=5.0,
        ci_upper=6.6,
        clock_type="GrimAge",
        mechanism="Kronik kardiyomiyopati, serebrovasküler hasar, immün disfonksiyon",
        affected_systems=["Kardiyovasküler", "Nörolojik", "Nazal", "Pulmoner", "Renal"],
        sample_size=485,
        reference="Vaillancourt K et al. Transl Psychiatry. 2021",
        pmid="34561417"
    ),
    "crack_cocaine": SubstanceData(
        key="crack_cocaine",
        name_tr="Crack Kokain",
        name_en="Crack Cocaine",
        category="Kokain",
        base_eaa=6.5,
        ci_lower=5.6,
        ci_upper=7.4,
        clock_type="GrimAge",
        mechanism="Hızlı emilim, yoğun kardiyotoksisite, pulmoner hasar",
        affected_systems=["Kardiyovasküler", "Nörolojik", "Pulmoner", "Renal"],
        sample_size=320,
        reference="Vaillancourt K et al. Transl Psychiatry. 2021",
        pmid="34561417"
    ),
    "methamphetamine_use": SubstanceData(
        key="methamphetamine_use",
        name_tr="Metamfetamin Kullanımı",
        name_en="Methamphetamine Use",
        category="Metamfetamin",
        base_eaa=6.2,
        ci_lower=4.5,
        ci_upper=8.1,
        clock_type="GrimAge",
        mechanism="Nörotoksisite, oksidatif hasar, mitokondriyal disfonksiyon",
        affected_systems=["Nörolojik", "Kardiyovasküler", "Dental", "Dermatoljik"],
        sample_size=48,
        reference="Godino A et al. Psychopharmacology. 2021",
        pmid="33594537"
    ),
    "methamphetamine_dependence": SubstanceData(
        key="methamphetamine_dependence",
        name_tr="Metamfetamin Bağımlılığı",
        name_en="Methamphetamine Dependence",
        category="Metamfetamin",
        base_eaa=8.5,
        ci_lower=6.8,
        ci_upper=10.2,
        clock_type="GrimAge",
        mechanism="Ağır nörodejenerasyon, kardiyak aritmiler, psikoz",
        affected_systems=["Nörolojik", "Kardiyovasküler", "Dental", "Dermatoljik", "Psikiyatrik"],
        sample_size=32,
        reference="Godino A et al. Psychopharmacology. 2021",
        pmid="33594537"
    ),
    "amphetamine_use": SubstanceData(
        key="amphetamine_use",
        name_tr="Amfetamin Kullanımı",
        name_en="Amphetamine Use",
        category="Amfetaminler",
        base_eaa=3.8,
        ci_lower=3.0,
        ci_upper=4.6,
        clock_type="GrimAge",
        mechanism="Kardiyovasküler stres, dopamin toksisitesi",
        affected_systems=["Kardiyovasküler", "Nörolojik"],
        sample_size=210,
        reference="Godino A et al. Psychopharmacology. 2021",
        pmid="33594537"
    ),
    "mdma_use": SubstanceData(
        key="mdma_use",
        name_tr="MDMA (Ecstasy) Kullanımı",
        name_en="MDMA (Ecstasy) Use",
        category="Amfetaminler",
        base_eaa=2.5,
        ci_lower=1.8,
        ci_upper=3.2,
        clock_type="Horvath",
        mechanism="Serotonin nörotoksisitesi, hipertermi, dehidrasyon",
        affected_systems=["Nörolojik", "Kardiyovasküler", "Hepatik"],
        sample_size=145,
        reference="Godino A et al. Psychopharmacology. 2021",
        pmid="33594537"
    ),
    "cannabis_occasional": SubstanceData(
        key="cannabis_occasional",
        name_tr="Esrar (Ara Sıra)",
        name_en="Cannabis (Occasional)",
        category="Kannabinoidler",
        base_eaa=0.3,
        ci_lower=0.0,
        ci_upper=0.7,
        clock_type="Horvath",
        mechanism="Hafif endokannabinoid sistem modülasyonu",
        affected_systems=["Nörolojik"],
        sample_size=580,
        reference="Schrott R et al. Clin Epigenetics. 2020",
        pmid="32928293"
    ),
    "cannabis_regular": SubstanceData(
        key="cannabis_regular",
        name_tr="Esrar (Düzenli Kullanım)",
        name_en="Cannabis (Regular Use)",
        category="Kannabinoidler",
        base_eaa=0.8,
        ci_lower=0.3,
        ci_upper=1.4,
        clock_type="Horvath",
        mechanism="Endokannabinoid sistem değişiklikleri, pulmoner etki",
        affected_systems=["Nörolojik", "Pulmoner"],
        sample_size=194,
        reference="Schrott R et al. Clin Epigenetics. 2020",
        pmid="32928293"
    ),
    "cannabis_heavy": SubstanceData(
        key="cannabis_heavy",
        name_tr="Esrar (Ağır Kullanım)",
        name_en="Cannabis (Heavy Use)",
        category="Kannabinoidler",
        base_eaa=1.8,
        ci_lower=1.1,
        ci_upper=2.5,
        clock_type="Horvath",
        mechanism="Kronik pulmoner hasar, nörokognitif değişiklikler",
        affected_systems=["Nörolojik", "Pulmoner", "Psikiyatrik"],
        sample_size=87,
        reference="Schrott R et al. Clin Epigenetics. 2020",
        pmid="32928293"
    ),
    "synthetic_cannabinoid": SubstanceData(
        key="synthetic_cannabinoid",
        name_tr="Sentetik Kannabinoid (Bonzai)",
        name_en="Synthetic Cannabinoid (Spice/K2)",
        category="Kannabinoidler",
        base_eaa=4.2,
        ci_lower=3.2,
        ci_upper=5.2,
        clock_type="GrimAge",
        mechanism="Öngörülemeyen toksisite, psikoz, kardiyak arrest",
        affected_systems=["Nörolojik", "Kardiyovasküler", "Psikiyatrik", "Renal"],
        sample_size=45,
        reference="Fantegrossi WE et al. Front Psychiatry. 2014",
        pmid="24860505"
    ),
    "tobacco_light": SubstanceData(
        key="tobacco_light",
        name_tr="Sigara (1-10/gün)",
        name_en="Tobacco (Light Smoking)",
        category="Tütün",
        base_eaa=1.5,
        ci_lower=1.1,
        ci_upper=1.9,
        clock_type="GrimAge",
        mechanism="Hafif pulmoner ve vasküler stres",
        affected_systems=["Pulmoner", "Kardiyovasküler"],
        sample_size=2800,
        reference="Yang Y et al. Nat Commun. 2020",
        pmid="32393754"
    ),
    "tobacco_smoking": SubstanceData(
        key="tobacco_smoking",
        name_tr="Sigara İçimi (10-20/gün)",
        name_en="Tobacco Smoking",
        category="Tütün",
        base_eaa=2.8,
        ci_lower=2.3,
        ci_upper=3.3,
        clock_type="GrimAge",
        mechanism="Pulmoner hasar, vasküler endotel disfonksiyonu, kanser riski",
        affected_systems=["Pulmoner", "Kardiyovasküler", "Oral"],
        sample_size=4521,
        reference="Yang Y et al. Nat Commun. 2020",
        pmid="32393754"
    ),
    "tobacco_heavy": SubstanceData(
        key="tobacco_heavy",
        name_tr="Ağır Sigara Kullanımı (>20/gün)",
        name_en="Heavy Tobacco Use (>20/day)",
        category="Tütün",
        base_eaa=4.5,
        ci_lower=3.8,
        ci_upper=5.2,
        clock_type="GrimAge",
        mechanism="KOAH gelişimi, hızlanmış ateroskleroz, multipl organ hasarı",
        affected_systems=["Pulmoner", "Kardiyovasküler", "Oral", "Gastrointestinal"],
        sample_size=1876,
        reference="Yang Y et al. Nat Commun. 2020",
        pmid="32393754"
    ),
    "nicotine_vaping": SubstanceData(
        key="nicotine_vaping",
        name_tr="Elektronik Sigara (Vaping)",
        name_en="E-Cigarette (Vaping)",
        category="Tütün",
        base_eaa=1.2,
        ci_lower=0.6,
        ci_upper=1.8,
        clock_type="GrimAge",
        mechanism="Pulmoner inflamasyon, nikotin bağımlılığı",
        affected_systems=["Pulmoner", "Kardiyovasküler"],
        sample_size=320,
        reference="Yang Y et al. Nat Commun. 2020",
        pmid="32393754"
    ),
    "benzodiazepine_use": SubstanceData(
        key="benzodiazepine_use",
        name_tr="Benzodiazepin Kullanımı",
        name_en="Benzodiazepine Use",
        category="Sedatifler",
        base_eaa=1.8,
        ci_lower=1.2,
        ci_upper=2.4,
        clock_type="GrimAge",
        mechanism="Kognitif bozukluk, bağımlılık gelişimi",
        affected_systems=["Nörolojik", "Psikiyatrik"],
        sample_size=890,
        reference="Weich S et al. BMJ. 2014",
        pmid="24569560"
    ),
    "benzodiazepine_dependence": SubstanceData(
        key="benzodiazepine_dependence",
        name_tr="Benzodiazepin Bağımlılığı",
        name_en="Benzodiazepine Dependence",
        category="Sedatifler",
        base_eaa=3.2,
        ci_lower=2.5,
        ci_upper=3.9,
        clock_type="GrimAge",
        mechanism="Kronik kognitif bozukluk, tolerans, yoksunluk nöbetleri",
        affected_systems=["Nörolojik", "Psikiyatrik", "Kardiyovasküler"],
        sample_size=340,
        reference="Weich S et al. BMJ. 2014",
        pmid="24569560"
    ),
    "barbiturate_use": SubstanceData(
        key="barbiturate_use",
        name_tr="Barbitürat Kullanımı",
        name_en="Barbiturate Use",
        category="Sedatifler",
        base_eaa=2.5,
        ci_lower=1.8,
        ci_upper=3.2,
        clock_type="GrimAge",
        mechanism="Solunum depresyonu, tolerans gelişimi",
        affected_systems=["Nörolojik", "Solunum"],
        sample_size=120,
        reference="Weich S et al. BMJ. 2014",
        pmid="24569560"
    ),
    "ghb_use": SubstanceData(
        key="ghb_use",
        name_tr="GHB Kullanımı",
        name_en="GHB Use",
        category="Sedatifler",
        base_eaa=2.8,
        ci_lower=2.0,
        ci_upper=3.6,
        clock_type="GrimAge",
        mechanism="GABAerjik nörotoksisite, solunum depresyonu",
        affected_systems=["Nörolojik", "Solunum", "Kardiyovasküler"],
        sample_size=65,
        reference="Busardò FP et al. Eur Rev Med Pharmacol Sci. 2015",
        pmid="26004613"
    ),
    "ketamine_use": SubstanceData(
        key="ketamine_use",
        name_tr="Ketamin Kullanımı",
        name_en="Ketamine Use",
        category="Disosiyatifler",
        base_eaa=2.2,
        ci_lower=1.5,
        ci_upper=2.9,
        clock_type="GrimAge",
        mechanism="Mesane toksisitesi, nörokognitif değişiklikler",
        affected_systems=["Nörolojik", "Üriner"],
        sample_size=110,
        reference="Morgan CJ et al. Addiction. 2010",
        pmid="19919594"
    ),
    "pcp_use": SubstanceData(
        key="pcp_use",
        name_tr="PCP Kullanımı",
        name_en="PCP Use",
        category="Disosiyatifler",
        base_eaa=4.5,
        ci_lower=3.5,
        ci_upper=5.5,
        clock_type="GrimAge",
        mechanism="Ağır nörotoksisite, psikoz indüksiyonu",
        affected_systems=["Nörolojik", "Psikiyatrik", "Kardiyovasküler"],
        sample_size=38,
        reference="Morgan CJ et al. Addiction. 2010",
        pmid="19919594"
    ),
    "lsd_use": SubstanceData(
        key="lsd_use",
        name_tr="LSD Kullanımı",
        name_en="LSD Use",
        category="Halüsinojenler",
        base_eaa=0.5,
        ci_lower=0.1,
        ci_upper=1.0,
        clock_type="Horvath",
        mechanism="Minimal fizyolojik hasar, psikolojik riskler",
        affected_systems=["Nörolojik"],
        sample_size=180,
        reference="Krebs TS et al. J Psychopharmacol. 2013",
        pmid="23263568"
    ),
    "psilocybin_use": SubstanceData(
        key="psilocybin_use",
        name_tr="Psilosibin (Sihirli Mantar)",
        name_en="Psilocybin (Magic Mushrooms)",
        category="Halüsinojenler",
        base_eaa=0.3,
        ci_lower=0.0,
        ci_upper=0.8,
        clock_type="Horvath",
        mechanism="Minimal fizyolojik hasar, terapötik potansiyel araştırması",
        affected_systems=["Nörolojik"],
        sample_size=95,
        reference="Krebs TS et al. J Psychopharmacol. 2013",
        pmid="23263568"
    ),
    "inhalant_use": SubstanceData(
        key="inhalant_use",
        name_tr="İnhalan (Uçucu Madde) Kullanımı",
        name_en="Inhalant Use",
        category="İnhalanlar",
        base_eaa=5.5,
        ci_lower=4.2,
        ci_upper=6.8,
        clock_type="GrimAge",
        mechanism="Ağır nörotoksisite, kardiyak aritmiler, ani ölüm",
        affected_systems=["Nörolojik", "Kardiyovasküler", "Hepatik", "Renal"],
        sample_size=85,
        reference="Howard MO et al. Addiction. 2011",
        pmid="21438935"
    ),
    "anabolic_steroid": SubstanceData(
        key="anabolic_steroid",
        name_tr="Anabolik Steroid Kullanımı",
        name_en="Anabolic Steroid Use",
        category="Steroidler",
        base_eaa=2.8,
        ci_lower=2.0,
        ci_upper=3.6,
        clock_type="GrimAge",
        mechanism="Kardiyomiyopati, hepatotoksisite, hormonal bozukluk",
        affected_systems=["Kardiyovasküler", "Hepatik", "Endokrin"],
        sample_size=220,
        reference="Pope HG et al. Circulation. 2017",
        pmid="28533317"
    ),
    "khat_use": SubstanceData(
        key="khat_use",
        name_tr="Khat Kullanımı",
        name_en="Khat Use",
        category="Stimülanlar",
        base_eaa=2.0,
        ci_lower=1.3,
        ci_upper=2.7,
        clock_type="GrimAge",
        mechanism="Kardiyovasküler stres, oral kanser riski",
        affected_systems=["Kardiyovasküler", "Oral", "Gastrointestinal"],
        sample_size=95,
        reference="Kassim S et al. J Ethnopharmacol. 2014",
        pmid="24582736"
    ),
    "kratom_use": SubstanceData(
        key="kratom_use",
        name_tr="Kratom Kullanımı",
        name_en="Kratom Use",
        category="Opioidler",
        base_eaa=1.8,
        ci_lower=1.0,
        ci_upper=2.6,
        clock_type="GrimAge",
        mechanism="Opioid reseptör aktivasyonu, hepatotoksisite riski",
        affected_systems=["Nörolojik", "Hepatik"],
        sample_size=78,
        reference="Swogger MT et al. Drug Alcohol Depend. 2015",
        pmid="25466371"
    ),
    "caffeine_high": SubstanceData(
        key="caffeine_high",
        name_tr="Yüksek Kafein Tüketimi (>600mg/gün)",
        name_en="High Caffeine Intake (>600mg/day)",
        category="Stimülanlar",
        base_eaa=0.4,
        ci_lower=0.1,
        ci_upper=0.8,
        clock_type="Horvath",
        mechanism="Kardiyovasküler stres, uyku bozukluğu",
        affected_systems=["Kardiyovasküler", "Nörolojik"],
        sample_size=1500,
        reference="Poole R et al. BMJ. 2017",
        pmid="29167102"
    ),
    "polysubstance_2": SubstanceData(
        key="polysubstance_2",
        name_tr="Çoklu Madde (2 madde)",
        name_en="Polysubstance (2 substances)",
        category="Çoklu Madde",
        base_eaa=5.5,
        ci_lower=4.8,
        ci_upper=6.2,
        clock_type="GrimAge",
        mechanism="Kombine organ hasarı, ilaç etkileşimleri",
        affected_systems=["Çoklu Sistem"],
        sample_size=520,
        reference="Rosen AD et al. Drug Alcohol Depend. 2018",
        pmid="29336043"
    ),
    "polysubstance_3plus": SubstanceData(
        key="polysubstance_3plus",
        name_tr="Çoklu Madde (3+ madde)",
        name_en="Polysubstance (3+ substances)",
        category="Çoklu Madde",
        base_eaa=7.3,
        ci_lower=6.4,
        ci_upper=8.3,
        clock_type="GrimAge",
        mechanism="Kümülatif organ hasarı, ciddi ilaç etkileşimleri, sistemik toksisite",
        affected_systems=["Çoklu Sistem"],
        sample_size=720,
        reference="Rosen AD et al. Drug Alcohol Depend. 2018",
        pmid="29336043"
    ),
}


DISEASE_DATABASE = {
    # nrcdnl94
    "type2_diabetes": DiseaseData(
        key="type2_diabetes",
        name_tr="Tip 2 Diyabet",
        name_en="Type 2 Diabetes",
        category="Metabolik",
        base_eaa=2.5,
        ci_lower=2.0,
        ci_upper=3.0,
        mechanism="İnsülin direnci, glukotoksisite, vasküler hasar",
        affected_systems=["Metabolik", "Kardiyovasküler", "Renal", "Oftalmik"],
        prevalence=9.3,
        reference="Horvath S et al. Genome Biol. 2013",
        pmid="24138928"
    ),
    "type1_diabetes": DiseaseData(
        key="type1_diabetes",
        name_tr="Tip 1 Diyabet",
        name_en="Type 1 Diabetes",
        category="Metabolik",
        base_eaa=2.2,
        ci_lower=1.7,
        ci_upper=2.7,
        mechanism="Otoimmün β-hücre hasarı, kronik hiperglisemi",
        affected_systems=["Metabolik", "İmmün", "Kardiyovasküler"],
        prevalence=0.5,
        reference="Horvath S et al. Genome Biol. 2013",
        pmid="24138928"
    ),
    "obesity_class1": DiseaseData(
        key="obesity_class1",
        name_tr="Obezite (Sınıf I, BMI 30-35)",
        name_en="Obesity (Class I, BMI 30-35)",
        category="Metabolik",
        base_eaa=1.5,
        ci_lower=1.0,
        ci_upper=2.0,
        mechanism="Adipoz doku inflamasyonu, metabolik sendrom",
        affected_systems=["Metabolik", "Kardiyovasküler"],
        prevalence=12.5,
        reference="Nevalainen T et al. Aging. 2017",
        pmid="28160545"
    ),
    "obesity_class2": DiseaseData(
        key="obesity_class2",
        name_tr="Obezite (Sınıf II, BMI 35-40)",
        name_en="Obesity (Class II, BMI 35-40)",
        category="Metabolik",
        base_eaa=2.2,
        ci_lower=1.7,
        ci_upper=2.7,
        mechanism="Kronik inflamasyon, kardiyometabolik stres",
        affected_systems=["Metabolik", "Kardiyovasküler", "Muskuloskeletal"],
        prevalence=5.8,
        reference="Nevalainen T et al. Aging. 2017",
        pmid="28160545"
    ),
    "obesity_class3": DiseaseData(
        key="obesity_class3",
        name_tr="Morbid Obezite (Sınıf III, BMI >40)",
        name_en="Morbid Obesity (Class III, BMI >40)",
        category="Metabolik",
        base_eaa=3.5,
        ci_lower=2.8,
        ci_upper=4.2,
        mechanism="Şiddetli metabolik disfonksiyon, multipl organ stresi",
        affected_systems=["Metabolik", "Kardiyovasküler", "Solunum", "Muskuloskeletal"],
        prevalence=2.8,
        reference="Nevalainen T et al. Aging. 2017",
        pmid="28160545"
    ),
    "metabolic_syndrome": DiseaseData(
        key="metabolic_syndrome",
        name_tr="Metabolik Sendrom",
        name_en="Metabolic Syndrome",
        category="Metabolik",
        base_eaa=2.8,
        ci_lower=2.2,
        ci_upper=3.4,
        mechanism="Kombine risk faktörleri: obezite, hipertansiyon, dislipidemi, hiperglisemi",
        affected_systems=["Metabolik", "Kardiyovasküler"],
        prevalence=23.0,
        reference="Nevalainen T et al. Aging. 2017",
        pmid="28160545"
    ),
    "hypertension_stage1": DiseaseData(
        key="hypertension_stage1",
        name_tr="Hipertansiyon (Evre 1)",
        name_en="Hypertension (Stage 1)",
        category="Kardiyovasküler",
        base_eaa=1.2,
        ci_lower=0.8,
        ci_upper=1.6,
        mechanism="Hafif vasküler stres, endotel disfonksiyonu",
        affected_systems=["Kardiyovasküler", "Renal"],
        prevalence=32.0,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "hypertension": DiseaseData(
        key="hypertension",
        name_tr="Hipertansiyon",
        name_en="Hypertension",
        category="Kardiyovasküler",
        base_eaa=1.8,
        ci_lower=1.4,
        ci_upper=2.2,
        mechanism="Vasküler stres, ateroskleroz hızlanması",
        affected_systems=["Kardiyovasküler", "Renal", "Serebral"],
        prevalence=45.0,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "hypertension_resistant": DiseaseData(
        key="hypertension_resistant",
        name_tr="Dirençli Hipertansiyon",
        name_en="Resistant Hypertension",
        category="Kardiyovasküler",
        base_eaa=3.0,
        ci_lower=2.4,
        ci_upper=3.6,
        mechanism="Tedaviye yanıtsız vasküler hasar, organ hasarı",
        affected_systems=["Kardiyovasküler", "Renal", "Serebral", "Oftalmik"],
        prevalence=12.0,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "coronary_artery": DiseaseData(
        key="coronary_artery",
        name_tr="Koroner Arter Hastalığı",
        name_en="Coronary Artery Disease",
        category="Kardiyovasküler",
        base_eaa=3.2,
        ci_lower=2.7,
        ci_upper=3.7,
        mechanism="Koroner ateroskleroz, miyokard iskemisi",
        affected_systems=["Kardiyovasküler"],
        prevalence=6.7,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "myocardial_infarction": DiseaseData(
        key="myocardial_infarction",
        name_tr="Miyokard İnfarktüsü Öyküsü",
        name_en="History of Myocardial Infarction",
        category="Kardiyovasküler",
        base_eaa=4.5,
        ci_lower=3.8,
        ci_upper=5.2,
        mechanism="Post-MI kardiyak remodeling, azalmış fonksiyon",
        affected_systems=["Kardiyovasküler"],
        prevalence=3.0,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "heart_failure": DiseaseData(
        key="heart_failure",
        name_tr="Kalp Yetmezliği",
        name_en="Heart Failure",
        category="Kardiyovasküler",
        base_eaa=4.8,
        ci_lower=4.0,
        ci_upper=5.6,
        mechanism="Kardiyak output azalması, sistemik konjesyon",
        affected_systems=["Kardiyovasküler", "Renal", "Hepatik"],
        prevalence=2.4,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "atrial_fibrillation": DiseaseData(
        key="atrial_fibrillation",
        name_tr="Atriyal Fibrilasyon",
        name_en="Atrial Fibrillation",
        category="Kardiyovasküler",
        base_eaa=2.5,
        ci_lower=1.9,
        ci_upper=3.1,
        mechanism="Kardiyak aritmiler, tromboembolik risk",
        affected_systems=["Kardiyovasküler", "Serebral"],
        prevalence=2.7,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "peripheral_artery": DiseaseData(
        key="peripheral_artery",
        name_tr="Periferik Arter Hastalığı",
        name_en="Peripheral Artery Disease",
        category="Kardiyovasküler",
        base_eaa=3.0,
        ci_lower=2.4,
        ci_upper=3.6,
        mechanism="Periferik ateroskleroz, iskemik ekstremite hasarı",
        affected_systems=["Kardiyovasküler", "Muskuloskeletal"],
        prevalence=5.9,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "stroke": DiseaseData(
        key="stroke",
        name_tr="İnme (Stroke) Öyküsü",
        name_en="History of Stroke",
        category="Nörolojik",
        base_eaa=5.2,
        ci_lower=4.4,
        ci_upper=6.0,
        mechanism="Serebrovasküler hasar, nörolojik defisit",
        affected_systems=["Nörolojik", "Kardiyovasküler"],
        prevalence=2.8,
        reference="Lu AT et al. Aging. 2019",
        pmid="30669119"
    ),
    "copd": DiseaseData(
        key="copd",
        name_tr="KOAH",
        name_en="COPD",
        category="Solunum",
        base_eaa=3.8,
        ci_lower=3.2,
        ci_upper=4.4,
        mechanism="Kronik hava yolu inflamasyonu, parankimal hasar",
        affected_systems=["Solunum", "Kardiyovasküler"],
        prevalence=6.4,
        reference="Lee SH et al. Eur Respir J. 2021",
        pmid="33602853"
    ),
    "asthma": DiseaseData(
        key="asthma",
        name_tr="Astım",
        name_en="Asthma",
        category="Solunum",
        base_eaa=1.2,
        ci_lower=0.7,
        ci_upper=1.7,
        mechanism="Kronik hava yolu inflamasyonu, bronşiyal hiperreaktivite",
        affected_systems=["Solunum"],
        prevalence=8.0,
        reference="Lee SH et al. Eur Respir J. 2021",
        pmid="33602853"
    ),
    "pulmonary_fibrosis": DiseaseData(
        key="pulmonary_fibrosis",
        name_tr="Pulmoner Fibrozis",
        name_en="Pulmonary Fibrosis",
        category="Solunum",
        base_eaa=5.5,
        ci_lower=4.5,
        ci_upper=6.5,
        mechanism="Progresif akciğer fibrozisi, solunum yetmezliği",
        affected_systems=["Solunum"],
        prevalence=0.5,
        reference="Lee SH et al. Eur Respir J. 2021",
        pmid="33602853"
    ),
    "sleep_apnea": DiseaseData(
        key="sleep_apnea",
        name_tr="Obstrüktif Uyku Apnesi",
        name_en="Obstructive Sleep Apnea",
        category="Solunum",
        base_eaa=1.8,
        ci_lower=1.2,
        ci_upper=2.4,
        mechanism="İntermitan hipoksi, kardiyovasküler stres",
        affected_systems=["Solunum", "Kardiyovasküler", "Nörolojik"],
        prevalence=9.0,
        reference="Lee SH et al. Eur Respir J. 2021",
        pmid="33602853"
    ),
    "liver_nafld": DiseaseData(
        key="liver_nafld",
        name_tr="Non-Alkolik Yağlı Karaciğer (NAFLD)",
        name_en="Non-Alcoholic Fatty Liver Disease",
        category="Hepatik",
        base_eaa=1.5,
        ci_lower=1.0,
        ci_upper=2.0,
        mechanism="Hepatik steatoz, metabolik disfonksiyon",
        affected_systems=["Hepatik", "Metabolik"],
        prevalence=25.0,
        reference="Loomba R et al. Gastroenterology. 2021",
        pmid="33675686"
    ),
    "liver_nash": DiseaseData(
        key="liver_nash",
        name_tr="Non-Alkolik Steatohepatit (NASH)",
        name_en="Non-Alcoholic Steatohepatitis",
        category="Hepatik",
        base_eaa=2.8,
        ci_lower=2.2,
        ci_upper=3.4,
        mechanism="Hepatik inflamasyon, fibrozis gelişimi",
        affected_systems=["Hepatik", "Metabolik"],
        prevalence=5.0,
        reference="Loomba R et al. Gastroenterology. 2021",
        pmid="33675686"
    ),
    "liver_cirrhosis": DiseaseData(
        key="liver_cirrhosis",
        name_tr="Karaciğer Sirozu",
        name_en="Liver Cirrhosis",
        category="Hepatik",
        base_eaa=5.5,
        ci_lower=4.6,
        ci_upper=6.4,
        mechanism="Hepatik fibrozis, portal hipertansiyon",
        affected_systems=["Hepatik", "Gastrointestinal", "Koagülasyon"],
        prevalence=0.3,
        reference="Loomba R et al. Gastroenterology. 2021",
        pmid="33675686"
    ),
    "hepatitis_b": DiseaseData(
        key="hepatitis_b",
        name_tr="Kronik Hepatit B",
        name_en="Chronic Hepatitis B",
        category="Hepatik",
        base_eaa=2.2,
        ci_lower=1.6,
        ci_upper=2.8,
        mechanism="Viral hepatik inflamasyon, fibrozis riski",
        affected_systems=["Hepatik", "İmmün"],
        prevalence=0.9,
        reference="Loomba R et al. Gastroenterology. 2021",
        pmid="33675686"
    ),
    "hepatitis_c": DiseaseData(
        key="hepatitis_c",
        name_tr="Kronik Hepatit C",
        name_en="Chronic Hepatitis C",
        category="Hepatik",
        base_eaa=2.8,
        ci_lower=2.2,
        ci_upper=3.4,
        mechanism="Kronik viral hepatit, siroz riski",
        affected_systems=["Hepatik", "İmmün"],
        prevalence=1.0,
        reference="Loomba R et al. Gastroenterology. 2021",
        pmid="33675686"
    ),
    "ckd_stage3": DiseaseData(
        key="ckd_stage3",
        name_tr="Kronik Böbrek Hastalığı (Evre 3)",
        name_en="Chronic Kidney Disease (Stage 3)",
        category="Renal",
        base_eaa=2.5,
        ci_lower=1.9,
        ci_upper=3.1,
        mechanism="GFR azalması, renal fibrozis başlangıcı",
        affected_systems=["Renal", "Kardiyovasküler"],
        prevalence=6.0,
        reference="Levine ME et al. Aging. 2018",
        pmid="29676998"
    ),
    "ckd_stage4": DiseaseData(
        key="ckd_stage4",
        name_tr="Kronik Böbrek Hastalığı (Evre 4)",
        name_en="Chronic Kidney Disease (Stage 4)",
        category="Renal",
        base_eaa=4.0,
        ci_lower=3.3,
        ci_upper=4.7,
        mechanism="Ciddi GFR kaybı, üremik sendrom",
        affected_systems=["Renal", "Kardiyovasküler", "Metabolik"],
        prevalence=0.4,
        reference="Levine ME et al. Aging. 2018",
        pmid="29676998"
    ),
    "ckd_stage5": DiseaseData(
        key="ckd_stage5",
        name_tr="Son Dönem Böbrek Hastalığı (SDBY)",
        name_en="End-Stage Renal Disease (ESRD)",
        category="Renal",
        base_eaa=6.5,
        ci_lower=5.5,
        ci_upper=7.5,
        mechanism="Dializ bağımlılığı, multipl organ etkileri",
        affected_systems=["Renal", "Kardiyovasküler", "Metabolik", "Kemik"],
        prevalence=0.2,
        reference="Levine ME et al. Aging. 2018",
        pmid="29676998"
    ),
    "hiv_aids": DiseaseData(
        key="hiv_aids",
        name_tr="HIV/AIDS",
        name_en="HIV/AIDS",
        category="İnfeksiyöz",
        base_eaa=5.2,
        ci_lower=4.4,
        ci_upper=6.0,
        mechanism="İmmün supresyon, kronik inflamasyon",
        affected_systems=["İmmün", "Nörolojik", "Kardiyovasküler"],
        prevalence=0.4,
        reference="Gross AM et al. Mol Cell. 2016",
        pmid="27768894"
    ),
    "hiv_controlled": DiseaseData(
        key="hiv_controlled",
        name_tr="HIV (Kontrol Altında)",
        name_en="HIV (Controlled)",
        category="İnfeksiyöz",
        base_eaa=2.5,
        ci_lower=1.8,
        ci_upper=3.2,
        mechanism="ART ile kontrol, rezidüel inflamasyon",
        affected_systems=["İmmün"],
        prevalence=0.3,
        reference="Gross AM et al. Mol Cell. 2016",
        pmid="27768894"
    ),
    "autoimmune_ra": DiseaseData(
        key="autoimmune_ra",
        name_tr="Romatoid Artrit",
        name_en="Rheumatoid Arthritis",
        category="Otoimmün",
        base_eaa=2.8,
        ci_lower=2.2,
        ci_upper=3.4,
        mechanism="Kronik sistemik inflamasyon, eklem hasarı",
        affected_systems=["Muskuloskeletal", "İmmün"],
        prevalence=1.0,
        reference="Horvath S et al. Genome Biol. 2013",
        pmid="24138928"
    ),
    "autoimmune_lupus": DiseaseData(
        key="autoimmune_lupus",
        name_tr="Sistemik Lupus Eritematozus",
        name_en="Systemic Lupus Erythematosus",
        category="Otoimmün",
        base_eaa=3.5,
        ci_lower=2.8,
        ci_upper=4.2,
        mechanism="Multi-organ otoimmün hasar",
        affected_systems=["İmmün", "Renal", "Kardiyovasküler", "Dermatoljik"],
        prevalence=0.5,
        reference="Horvath S et al. Genome Biol. 2013",
        pmid="24138928"
    ),
    "autoimmune_ms": DiseaseData(
        key="autoimmune_ms",
        name_tr="Multipl Skleroz",
        name_en="Multiple Sclerosis",
        category="Otoimmün",
        base_eaa=3.2,
        ci_lower=2.5,
        ci_upper=3.9,
        mechanism="Santral sinir sistemi demiyelinizasyonu",
        affected_systems=["Nörolojik", "İmmün"],
        prevalence=0.3,
        reference="Horvath S et al. Genome Biol. 2013",
        pmid="24138928"
    ),
    "major_depression": DiseaseData(
        key="major_depression",
        name_tr="Major Depresif Bozukluk",
        name_en="Major Depressive Disorder",
        category="Psikiyatrik",
        base_eaa=2.0,
        ci_lower=1.5,
        ci_upper=2.5,
        mechanism="Nöroinflamasyon, HPA aks disregülasyonu",
        affected_systems=["Nörolojik", "Endokrin"],
        prevalence=7.0,
        reference="Han LKM et al. Am J Psychiatry. 2021",
        pmid="33207934"
    ),
    "bipolar_disorder": DiseaseData(
        key="bipolar_disorder",
        name_tr="Bipolar Bozukluk",
        name_en="Bipolar Disorder",
        category="Psikiyatrik",
        base_eaa=2.5,
        ci_lower=1.9,
        ci_upper=3.1,
        mechanism="Mood instabilitesi, metabolik disregülasyon",
        affected_systems=["Nörolojik", "Metabolik"],
        prevalence=2.8,
        reference="Han LKM et al. Am J Psychiatry. 2021",
        pmid="33207934"
    ),
    "schizophrenia": DiseaseData(
        key="schizophrenia",
        name_tr="Şizofreni",
        name_en="Schizophrenia",
        category="Psikiyatrik",
        base_eaa=3.5,
        ci_lower=2.8,
        ci_upper=4.2,
        mechanism="Nörodevelopmental değişiklikler, metabolik yan etkiler",
        affected_systems=["Nörolojik", "Metabolik"],
        prevalence=1.0,
        reference="Han LKM et al. Am J Psychiatry. 2021",
        pmid="33207934"
    ),
    "anxiety_disorder": DiseaseData(
        key="anxiety_disorder",
        name_tr="Anksiyete Bozukluğu",
        name_en="Anxiety Disorder",
        category="Psikiyatrik",
        base_eaa=1.2,
        ci_lower=0.7,
        ci_upper=1.7,
        mechanism="Kronik stres, kortizol disregülasyonu",
        affected_systems=["Nörolojik", "Endokrin"],
        prevalence=18.0,
        reference="Han LKM et al. Am J Psychiatry. 2021",
        pmid="33207934"
    ),
    "ptsd": DiseaseData(
        key="ptsd",
        name_tr="Post-Travmatik Stres Bozukluğu",
        name_en="Post-Traumatic Stress Disorder",
        category="Psikiyatrik",
        base_eaa=2.2,
        ci_lower=1.6,
        ci_upper=2.8,
        mechanism="Travma sonrası nörobiyolojik değişiklikler",
        affected_systems=["Nörolojik", "Endokrin", "İmmün"],
        prevalence=3.5,
        reference="Wolf EJ et al. Psychoneuroendocrinology. 2018",
        pmid="29706265"
    ),
    "alzheimer": DiseaseData(
        key="alzheimer",
        name_tr="Alzheimer Hastalığı",
        name_en="Alzheimer's Disease",
        category="Nörolojik",
        base_eaa=6.0,
        ci_lower=5.0,
        ci_upper=7.0,
        mechanism="Nörodejenerasyon, amiloid ve tau birikimi",
        affected_systems=["Nörolojik"],
        prevalence=1.6,
        reference="Levine ME et al. J Gerontol A Biol Sci Med Sci. 2015",
        pmid="25633341"
    ),
    "parkinson": DiseaseData(
        key="parkinson",
        name_tr="Parkinson Hastalığı",
        name_en="Parkinson's Disease",
        category="Nörolojik",
        base_eaa=4.5,
        ci_lower=3.6,
        ci_upper=5.4,
        mechanism="Dopaminerjik nöron kaybı, motor disfonksiyon",
        affected_systems=["Nörolojik"],
        prevalence=0.3,
        reference="Levine ME et al. J Gerontol A Biol Sci Med Sci. 2015",
        pmid="25633341"
    ),
    "epilepsy": DiseaseData(
        key="epilepsy",
        name_tr="Epilepsi",
        name_en="Epilepsy",
        category="Nörolojik",
        base_eaa=1.8,
        ci_lower=1.2,
        ci_upper=2.4,
        mechanism="Nöbet aktivitesi, nörokognitif etkiler",
        affected_systems=["Nörolojik"],
        prevalence=1.2,
        reference="Levine ME et al. J Gerontol A Biol Sci Med Sci. 2015",
        pmid="25633341"
    ),
    "migraine_chronic": DiseaseData(
        key="migraine_chronic",
        name_tr="Kronik Migren",
        name_en="Chronic Migraine",
        category="Nörolojik",
        base_eaa=1.0,
        ci_lower=0.5,
        ci_upper=1.5,
        mechanism="Vasküler ve nörolojik disregülasyon",
        affected_systems=["Nörolojik"],
        prevalence=2.0,
        reference="Levine ME et al. J Gerontol A Biol Sci Med Sci. 2015",
        pmid="25633341"
    ),
    "cancer_active": DiseaseData(
        key="cancer_active",
        name_tr="Aktif Kanser",
        name_en="Active Cancer",
        category="Onkolojik",
        base_eaa=5.0,
        ci_lower=4.0,
        ci_upper=6.0,
        mechanism="Tümör biyolojisi, sistemik inflamasyon",
        affected_systems=["Çoklu Sistem"],
        prevalence=1.5,
        reference="Kresovich JK et al. J Natl Cancer Inst. 2019",
        pmid="31504674"
    ),
    "cancer_remission": DiseaseData(
        key="cancer_remission",
        name_tr="Kanser Remisyonu",
        name_en="Cancer in Remission",
        category="Onkolojik",
        base_eaa=2.5,
        ci_lower=1.8,
        ci_upper=3.2,
        mechanism="Tedavi sonrası residüel etkiler",
        affected_systems=["Çoklu Sistem"],
        prevalence=3.0,
        reference="Kresovich JK et al. J Natl Cancer Inst. 2019",
        pmid="31504674"
    ),
    "osteoporosis": DiseaseData(
        key="osteoporosis",
        name_tr="Osteoporoz",
        name_en="Osteoporosis",
        category="Muskuloskeletal",
        base_eaa=1.5,
        ci_lower=1.0,
        ci_upper=2.0,
        mechanism="Kemik mineral yoğunluğu kaybı, kırık riski",
        affected_systems=["Muskuloskeletal"],
        prevalence=10.0,
        reference="Levine ME et al. J Gerontol A Biol Sci Med Sci. 2015",
        pmid="25633341"
    ),
    "sarcopenia": DiseaseData(
        key="sarcopenia",
        name_tr="Sarkopeni",
        name_en="Sarcopenia",
        category="Muskuloskeletal",
        base_eaa=2.0,
        ci_lower=1.4,
        ci_upper=2.6,
        mechanism="Kas kütlesi ve fonksiyon kaybı",
        affected_systems=["Muskuloskeletal", "Metabolik"],
        prevalence=8.0,
        reference="Levine ME et al. J Gerontol A Biol Sci Med Sci. 2015",
        pmid="25633341"
    ),
    "frailty": DiseaseData(
        key="frailty",
        name_tr="Kırılganlık Sendromu",
        name_en="Frailty Syndrome",
        category="Geriatrik",
        base_eaa=4.0,
        ci_lower=3.2,
        ci_upper=4.8,
        mechanism="Multipl sistem rezerv kaybı",
        affected_systems=["Çoklu Sistem"],
        prevalence=6.5,
        reference="Levine ME et al. J Gerontol A Biol Sci Med Sci. 2015",
        pmid="25633341"
    ),
}


SUBSTANCE_SUBSTANCE_SYNERGY = {
    # nrcdnl94
    ("alcohol_heavy", "opioid_use"): SynergyData(
        type="substance-substance",
        key1="alcohol_heavy",
        key2="opioid_use",
        multiplier=1.8,
        mechanism="Solunum depresyonu potansiyasyonu, overdoz riski artışı",
        evidence_level="Çok Yüksek",
        clinical_warning="HAYATI TEHLİKE: Solunum durması riski!",
        reference="Jones CM et al. JAMA. 2013",
        pmid="23340661"
    ),
    ("alcohol_heavy", "opioid_dependence"): SynergyData(
        type="substance-substance",
        key1="alcohol_heavy",
        key2="opioid_dependence",
        multiplier=2.2,
        mechanism="Ciddi solunum depresyonu, hepatotoksisite potansiyasyonu",
        evidence_level="Çok Yüksek",
        clinical_warning="ACİL: Overdoz riski çok yüksek!",
        reference="Jones CM et al. JAMA. 2013",
        pmid="23340661"
    ),
    ("alcohol_dependence", "opioid_dependence"): SynergyData(
        type="substance-substance",
        key1="alcohol_dependence",
        key2="opioid_dependence",
        multiplier=2.5,
        mechanism="Çift bağımlılık, multipl organ yetmezliği riski",
        evidence_level="Çok Yüksek",
        clinical_warning="KRİTİK: Acil tedavi gerektirir!",
        reference="Jones CM et al. JAMA. 2013",
        pmid="23340661"
    ),
    ("alcohol_heavy", "benzodiazepine_use"): SynergyData(
        type="substance-substance",
        key1="alcohol_heavy",
        key2="benzodiazepine_use",
        multiplier=1.9,
        mechanism="GABAerjik potansiyasyon, santral sinir sistemi depresyonu",
        evidence_level="Çok Yüksek",
        clinical_warning="HAYATI TEHLİKE: Solunum durması!",
        reference="Sun EC et al. BMJ. 2017",
        pmid="28292769"
    ),
    ("opioid_use", "benzodiazepine_use"): SynergyData(
        type="substance-substance",
        key1="opioid_use",
        key2="benzodiazepine_use",
        multiplier=2.0,
        mechanism="Solunum merkezi supresyonu, sedasyonun potansiyasyonu",
        evidence_level="Çok Yüksek",
        clinical_warning="FDA BLACK BOX: Birlikte kullanım ölümcül!",
        reference="Park TW et al. BMJ. 2015",
        pmid="25977146"
    ),
    ("opioid_dependence", "benzodiazepine_dependence"): SynergyData(
        type="substance-substance",
        key1="opioid_dependence",
        key2="benzodiazepine_dependence",
        multiplier=2.8,
        mechanism="Çift sedatif bağımlılığı, yüksek overdoz riski",
        evidence_level="Çok Yüksek",
        clinical_warning="KRİTİK TEHLİKE: Overdoz ölüm riski >50%!",
        reference="Park TW et al. BMJ. 2015",
        pmid="25977146"
    ),
    ("cocaine_use", "alcohol_heavy"): SynergyData(
        type="substance-substance",
        key1="cocaine_use",
        key2="alcohol_heavy",
        multiplier=1.7,
        mechanism="Cocaethylene oluşumu, kardiyotoksisite artışı",
        evidence_level="Yüksek",
        clinical_warning="Kardiyak arrest riski belirgin artar!",
        reference="McCance-Katz EF et al. Drug Alcohol Depend. 1998",
        pmid="9788503"
    ),
    ("cocaine_dependence", "alcohol_dependence"): SynergyData(
        type="substance-substance",
        key1="cocaine_dependence",
        key2="alcohol_dependence",
        multiplier=2.2,
        mechanism="Yoğun cocaethylene birikimi, ağır kardiyomiyopati",
        evidence_level="Yüksek",
        clinical_warning="KRİTİK: Ani kardiyak ölüm riski!",
        reference="McCance-Katz EF et al. Drug Alcohol Depend. 1998",
        pmid="9788503"
    ),
    ("cocaine_use", "tobacco_smoking"): SynergyData(
        type="substance-substance",
        key1="cocaine_use",
        key2="tobacco_smoking",
        multiplier=1.4,
        mechanism="Vazokonstriksiyon potansiyasyonu, koroner iskemi",
        evidence_level="Yüksek",
        clinical_warning="Koroner spazm ve MI riski!",
        reference="Moliterno DJ et al. Am Heart J. 1994",
        pmid="8279399"
    ),
    ("methamphetamine_use", "cocaine_use"): SynergyData(
        type="substance-substance",
        key1="methamphetamine_use",
        key2="cocaine_use",
        multiplier=2.0,
        mechanism="Çift stimülan toksisitesi, kardiyak aritmi",
        evidence_level="Yüksek",
        clinical_warning="HAYATI TEHLİKE: Kardiyak arrest!",
        reference="Kaye S et al. Drug Alcohol Rev. 2007",
        pmid="17364848"
    ),
    ("methamphetamine_dependence", "alcohol_heavy"): SynergyData(
        type="substance-substance",
        key1="methamphetamine_dependence",
        key2="alcohol_heavy",
        multiplier=1.8,
        mechanism="Çoklu organ toksisitesi, nörodejenerasyon hızlanması",
        evidence_level="Orta",
        clinical_warning="Ağır nörotoksisite riski!",
        reference="Brecht ML et al. J Drug Issues. 2008",
        pmid="19122753"
    ),
    ("heroin_use", "cocaine_use"): SynergyData(
        type="substance-substance",
        key1="heroin_use",
        key2="cocaine_use",
        multiplier=2.3,
        mechanism="Speedball etkisi, kardiyopulmoner arrest",
        evidence_level="Çok Yüksek",
        clinical_warning="SPEEDBALL: En ölümcül kombinasyonlardan!",
        reference="Coffin PO et al. Am J Public Health. 2003",
        pmid="12940269"
    ),
    ("fentanyl_use", "cocaine_use"): SynergyData(
        type="substance-substance",
        key1="fentanyl_use",
        key2="cocaine_use",
        multiplier=2.8,
        mechanism="Fentanil potensli speedball, ani ölüm",
        evidence_level="Çok Yüksek",
        clinical_warning="AŞIRI TEHLİKE: Ani ölüm riski çok yüksek!",
        reference="Gladden RM et al. MMWR. 2016",
        pmid="26963675"
    ),
    ("fentanyl_use", "benzodiazepine_use"): SynergyData(
        type="substance-substance",
        key1="fentanyl_use",
        key2="benzodiazepine_use",
        multiplier=3.0,
        mechanism="Fentanil + benzodiazepin solunum arresti",
        evidence_level="Çok Yüksek",
        clinical_warning="EN TEHLİKELİ KOMBİNASYON: Hemen ölüm!",
        reference="Gladden RM et al. MMWR. 2016",
        pmid="26963675"
    ),
    ("cannabis_heavy", "tobacco_heavy"): SynergyData(
        type="substance-substance",
        key1="cannabis_heavy",
        key2="tobacco_heavy",
        multiplier=1.5,
        mechanism="Kümülatif pulmoner hasar, kanser riski artışı",
        evidence_level="Yüksek",
        clinical_warning="Akciğer hasarı hızlanır!",
        reference="Aldington S et al. Thorax. 2008",
        pmid="18156617"
    ),
    ("synthetic_cannabinoid", "stimulant"): SynergyData(
        type="substance-substance",
        key1="synthetic_cannabinoid",
        key2="methamphetamine_use",
        multiplier=2.2,
        mechanism="Öngörülemeyen psikotik reaksiyonlar, kardiyak arrest",
        evidence_level="Orta",
        clinical_warning="Öngörülemeyen toksisite!",
        reference="Fantegrossi WE et al. Front Psychiatry. 2014",
        pmid="24860505"
    ),
    ("ghb_use", "alcohol_heavy"): SynergyData(
        type="substance-substance",
        key1="ghb_use",
        key2="alcohol_heavy",
        multiplier=2.5,
        mechanism="GABAerjik süper-potansiyasyon, koma",
        evidence_level="Çok Yüksek",
        clinical_warning="KOMA VE ÖLÜM RİSKİ!",
        reference="Busardò FP et al. Eur Rev Med Pharmacol Sci. 2015",
        pmid="26004613"
    ),
    ("mdma_use", "amphetamine_use"): SynergyData(
        type="substance-substance",
        key1="mdma_use",
        key2="amphetamine_use",
        multiplier=1.6,
        mechanism="Serotonin ve dopamin toksisitesi, hipertermi",
        evidence_level="Yüksek",
        clinical_warning="Hipertermi ve serotonin sendromu!",
        reference="Parrott AC. Hum Psychopharmacol. 2014",
        pmid="24523048"
    ),
    ("inhalant_use", "alcohol_heavy"): SynergyData(
        type="substance-substance",
        key1="inhalant_use",
        key2="alcohol_heavy",
        multiplier=2.0,
        mechanism="Kardiyak sensitizasyon, ani ölüm sendromu",
        evidence_level="Yüksek",
        clinical_warning="Ani kardiyak ölüm riski!",
        reference="Howard MO et al. Addiction. 2011",
        pmid="21438935"
    ),
    ("tobacco_heavy", "alcohol_dependence"): SynergyData(
        type="substance-substance",
        key1="tobacco_heavy",
        key2="alcohol_dependence",
        multiplier=1.6,
        mechanism="Sinerjistik kanser riski, kardiyovasküler hasar",
        evidence_level="Çok Yüksek",
        clinical_warning="Kanser riski dramatik artar!",
        reference="Pelucchi C et al. Int J Cancer. 2006",
        pmid="16152585"
    ),
    ("ketamine_use", "alcohol_heavy"): SynergyData(
        type="substance-substance",
        key1="ketamine_use",
        key2="alcohol_heavy",
        multiplier=1.7,
        mechanism="SSS depresyonu, aspirayon pnömonisi riski",
        evidence_level="Orta",
        clinical_warning="Bilinç kaybı ve aspirasyon riski!",
        reference="Morgan CJ et al. Addiction. 2010",
        pmid="19919594"
    ),
    ("kratom_use", "opioid_use"): SynergyData(
        type="substance-substance",
        key1="kratom_use",
        key2="opioid_use",
        multiplier=1.5,
        mechanism="Opioid reseptör aşırı aktivasyonu",
        evidence_level="Orta",
        clinical_warning="Solunum depresyonu riski!",
        reference="Swogger MT et al. Drug Alcohol Depend. 2015",
        pmid="25466371"
    ),
}


DISEASE_DISEASE_SYNERGY = {
    # nrcdnl94
    ("type2_diabetes", "hypertension"): SynergyData(
        type="disease-disease",
        key1="type2_diabetes",
        key2="hypertension",
        multiplier=1.6,
        mechanism="Metabolik sendrom, hızlanmış ateroskleroz",
        evidence_level="Çok Yüksek",
        clinical_warning="Kardiyovasküler olay riski 4 kat artar",
        reference="Petrie JR et al. Can J Cardiol. 2018",
        pmid="29459239"
    ),
    ("type2_diabetes", "coronary_artery"): SynergyData(
        type="disease-disease",
        key1="type2_diabetes",
        key2="coronary_artery",
        multiplier=1.8,
        mechanism="Diyabetik makroanjiyopati + KAH",
        evidence_level="Çok Yüksek",
        clinical_warning="MI riski dramatik artar",
        reference="Petrie JR et al. Can J Cardiol. 2018",
        pmid="29459239"
    ),
    ("type2_diabetes", "ckd_stage3"): SynergyData(
        type="disease-disease",
        key1="type2_diabetes",
        key2="ckd_stage3",
        multiplier=1.7,
        mechanism="Diyabetik nefropati + KBH progresyonu",
        evidence_level="Çok Yüksek",
        clinical_warning="SDBY riski yüksek",
        reference="Alicic RZ et al. Clin J Am Soc Nephrol. 2017",
        pmid="28768707"
    ),
    ("type2_diabetes", "obesity_class2"): SynergyData(
        type="disease-disease",
        key1="type2_diabetes",
        key2="obesity_class2",
        multiplier=1.5,
        mechanism="İnsülin direnci kısır döngüsü",
        evidence_level="Yüksek",
        clinical_warning="Metabolik kontrol zorlaşır",
        reference="Lean ME et al. Lancet. 2018",
        pmid="29221645"
    ),
    ("hypertension", "coronary_artery"): SynergyData(
        type="disease-disease",
        key1="hypertension",
        key2="coronary_artery",
        multiplier=1.5,
        mechanism="Koroner perfüzyon bozukluğu",
        evidence_level="Çok Yüksek",
        clinical_warning="MI ve stroke riski artar",
        reference="Fuchs FD et al. Circ Res. 2020",
        pmid="32539649"
    ),
    ("hypertension", "heart_failure"): SynergyData(
        type="disease-disease",
        key1="hypertension",
        key2="heart_failure",
        multiplier=1.6,
        mechanism="Afterload artışı kalp yetmezliğini şiddetlendirir",
        evidence_level="Çok Yüksek",
        clinical_warning="Dekompansasyon riski yüksek",
        reference="Fuchs FD et al. Circ Res. 2020",
        pmid="32539649"
    ),
    ("hypertension", "ckd_stage3"): SynergyData(
        type="disease-disease",
        key1="hypertension",
        key2="ckd_stage3",
        multiplier=1.5,
        mechanism="Hipertansif nefropati, kısır döngü",
        evidence_level="Çok Yüksek",
        clinical_warning="Böbrek fonksiyonu hızla kötüleşir",
        reference="Ku E et al. Kidney Int. 2019",
        pmid="31126599"
    ),
    ("coronary_artery", "heart_failure"): SynergyData(
        type="disease-disease",
        key1="coronary_artery",
        key2="heart_failure",
        multiplier=1.7,
        mechanism="İskemik kardiyomiyopati progresyonu",
        evidence_level="Çok Yüksek",
        clinical_warning="Mortalite riski yüksek",
        reference="Gheorghiade M et al. Am Heart J. 2006",
        pmid="16442897"
    ),
    ("copd", "heart_failure"): SynergyData(
        type="disease-disease",
        key1="copd",
        key2="heart_failure",
        multiplier=1.8,
        mechanism="Pulmoner hipertansiyon, sağ kalp yetmezliği",
        evidence_level="Çok Yüksek",
        clinical_warning="Cor pulmonale gelişimi",
        reference="Celli BR et al. Am J Respir Crit Care Med. 2018",
        pmid="29972037"
    ),
    ("copd", "coronary_artery"): SynergyData(
        type="disease-disease",
        key1="copd",
        key2="coronary_artery",
        multiplier=1.5,
        mechanism="Sistemik inflamasyon, hipoksi",
        evidence_level="Yüksek",
        clinical_warning="MI riski artar",
        reference="Celli BR et al. Am J Respir Crit Care Med. 2018",
        pmid="29972037"
    ),
    ("liver_cirrhosis", "ckd_stage4"): SynergyData(
        type="disease-disease",
        key1="liver_cirrhosis",
        key2="ckd_stage4",
        multiplier=2.0,
        mechanism="Hepatorenal sendrom riski",
        evidence_level="Çok Yüksek",
        clinical_warning="Çoklu organ yetmezliği!",
        reference="Angeli P et al. Gut. 2015",
        pmid="25631671"
    ),
    ("liver_cirrhosis", "hepatitis_c"): SynergyData(
        type="disease-disease",
        key1="liver_cirrhosis",
        key2="hepatitis_c",
        multiplier=1.6,
        mechanism="HCV siroz progresyonunu hızlandırır",
        evidence_level="Çok Yüksek",
        clinical_warning="HCC riski belirgin artar",
        reference="Kanwal F et al. Hepatology. 2020",
        pmid="31508817"
    ),
    ("hiv_aids", "hepatitis_c"): SynergyData(
        type="disease-disease",
        key1="hiv_aids",
        key2="hepatitis_c",
        multiplier=1.8,
        mechanism="HIV + HCV koinfeksiyonu karaciğer hasarını hızlandırır",
        evidence_level="Çok Yüksek",
        clinical_warning="Hızlı fibrozis progresyonu",
        reference="Sulkowski MS et al. Gastroenterology. 2014",
        pmid="24076003"
    ),
    ("hiv_aids", "type2_diabetes"): SynergyData(
        type="disease-disease",
        key1="hiv_aids",
        key2="type2_diabetes",
        multiplier=1.5,
        mechanism="ART metabolik yan etkileri + diyabet",
        evidence_level="Yüksek",
        clinical_warning="Kardiyovasküler komplikasyonlar artar",
        reference="Monroe AK et al. Ann Intern Med. 2014",
        pmid="25069178"
    ),
    ("major_depression", "coronary_artery"): SynergyData(
        type="disease-disease",
        key1="major_depression",
        key2="coronary_artery",
        multiplier=1.5,
        mechanism="Stres-kardiyak bağlantı, tedavi uyumsuzluğu",
        evidence_level="Çok Yüksek",
        clinical_warning="MI sonrası mortalite 2 kat artar",
        reference="Carney RM et al. Mol Psychiatry. 2017",
        pmid="27752079"
    ),
    ("major_depression", "type2_diabetes"): SynergyData(
        type="disease-disease",
        key1="major_depression",
        key2="type2_diabetes",
        multiplier=1.4,
        mechanism="HPA aks disregülasyonu, öz-bakım azalması",
        evidence_level="Yüksek",
        clinical_warning="Glisemik kontrol bozulur",
        reference="Mezuk B et al. Diabetes Care. 2008",
        pmid="18443189"
    ),
    ("obesity_class3", "sleep_apnea"): SynergyData(
        type="disease-disease",
        key1="obesity_class3",
        key2="sleep_apnea",
        multiplier=1.6,
        mechanism="Obesite hipoventilasyon sendromu",
        evidence_level="Çok Yüksek",
        clinical_warning="Solunum yetmezliği riski",
        reference="Mokhlesi B et al. Am J Respir Crit Care Med. 2019",
        pmid="30517050"
    ),
    ("atrial_fibrillation", "heart_failure"): SynergyData(
        type="disease-disease",
        key1="atrial_fibrillation",
        key2="heart_failure",
        multiplier=1.7,
        mechanism="Taşikardiyomiyopati, tromboembolik risk",
        evidence_level="Çok Yüksek",
        clinical_warning="Stroke ve dekompansasyon riski",
        reference="Piccini JP et al. Heart Rhythm. 2016",
        pmid="26272523"
    ),
    ("ckd_stage4", "heart_failure"): SynergyData(
        type="disease-disease",
        key1="ckd_stage4",
        key2="heart_failure",
        multiplier=1.9,
        mechanism="Kardiorenal sendrom",
        evidence_level="Çok Yüksek",
        clinical_warning="Her iki organ birbirini kötüleştirir",
        reference="Rangaswami J et al. Circulation. 2019",
        pmid="30852913"
    ),
    ("alzheimer", "type2_diabetes"): SynergyData(
        type="disease-disease",
        key1="alzheimer",
        key2="type2_diabetes",
        multiplier=1.5,
        mechanism="Beyin insülin direnci, nörodejenerasyon",
        evidence_level="Yüksek",
        clinical_warning="Kognitif gerileme hızlanır",
        reference="Biessels GJ et al. Lancet Neurol. 2020",
        pmid="32474052"
    ),
    ("parkinson", "major_depression"): SynergyData(
        type="disease-disease",
        key1="parkinson",
        key2="major_depression",
        multiplier=1.4,
        mechanism="Dopamin disfonksiyonu, yaşam kalitesi bozulması",
        evidence_level="Yüksek",
        clinical_warning="Fonksiyonel gerileme hızlanır",
        reference="Reijnders JS et al. Mov Disord. 2008",
        pmid="18442128"
    ),
    ("schizophrenia", "type2_diabetes"): SynergyData(
        type="disease-disease",
        key1="schizophrenia",
        key2="type2_diabetes",
        multiplier=1.5,
        mechanism="Antipsikotik metabolik yan etkileri",
        evidence_level="Yüksek",
        clinical_warning="Metabolik sendrom riski çok yüksek",
        reference="Pillinger T et al. Lancet Psychiatry. 2017",
        pmid="28535857"
    ),
    ("autoimmune_ra", "coronary_artery"): SynergyData(
        type="disease-disease",
        key1="autoimmune_ra",
        key2="coronary_artery",
        multiplier=1.5,
        mechanism="Kronik inflamasyon + ateroskleroz",
        evidence_level="Yüksek",
        clinical_warning="MI riski 2 kat artar",
        reference="Agca R et al. Ann Rheum Dis. 2017",
        pmid="27628756"
    ),
    ("autoimmune_lupus", "ckd_stage3"): SynergyData(
        type="disease-disease",
        key1="autoimmune_lupus",
        key2="ckd_stage3",
        multiplier=1.7,
        mechanism="Lupus nefriti + KBH",
        evidence_level="Çok Yüksek",
        clinical_warning="SDBY riski yüksek",
        reference="Mok CC et al. Arthritis Care Res. 2013",
        pmid="22945992"
    ),
    ("cancer_active", "major_depression"): SynergyData(
        type="disease-disease",
        key1="cancer_active",
        key2="major_depression",
        multiplier=1.4,
        mechanism="Psikoonkolojik stres, immün supresyon",
        evidence_level="Yüksek",
        clinical_warning="Sağkalım etkilenebilir",
        reference="Pinquart M et al. Psychol Med. 2010",
        pmid="19903366"
    ),
    ("frailty", "ckd_stage4"): SynergyData(
        type="disease-disease",
        key1="frailty",
        key2="ckd_stage4",
        multiplier=1.8,
        mechanism="Üremik sarkopeni, multipl komorbiditeler",
        evidence_level="Yüksek",
        clinical_warning="Prognoz çok kötü",
        reference="Johansen KL et al. Kidney Int. 2019",
        pmid="30528274"
    ),
}


SUBSTANCE_DISEASE_SYNERGY = {
    # nrcdnl94
    ("alcohol_heavy", "liver_cirrhosis"): SynergyData(
        type="substance-disease",
        key1="alcohol_heavy",
        key2="liver_cirrhosis",
        multiplier=2.0,
        mechanism="Alkol siroz progresyonunu dramatik hızlandırır",
        evidence_level="Çok Yüksek",
        clinical_warning="KRİTİK: Karaciğer yetmezliği hızlanır!",
        reference="Louvet A et al. J Hepatol. 2017",
        pmid="28267622"
    ),
    ("alcohol_dependence", "liver_cirrhosis"): SynergyData(
        type="substance-disease",
        key1="alcohol_dependence",
        key2="liver_cirrhosis",
        multiplier=2.5,
        mechanism="Alkolik siroz terminal evreye hızla ilerler",
        evidence_level="Çok Yüksek",
        clinical_warning="ACİL: Transplant değerlendirmesi!",
        reference="Louvet A et al. J Hepatol. 2017",
        pmid="28267622"
    ),
    ("alcohol_heavy", "hepatitis_c"): SynergyData(
        type="substance-disease",
        key1="alcohol_heavy",
        key2="hepatitis_c",
        multiplier=1.8,
        mechanism="Alkol + HCV fibrozis hızını 3 kat artırır",
        evidence_level="Çok Yüksek",
        clinical_warning="Siroz riski dramatik artar!",
        reference="Szabo G et al. Nat Rev Gastroenterol Hepatol. 2015",
        pmid="25534115"
    ),
    ("alcohol_heavy", "type2_diabetes"): SynergyData(
        type="substance-disease",
        key1="alcohol_heavy",
        key2="type2_diabetes",
        multiplier=1.5,
        mechanism="Alkol insülin direncini ve komplikasyonları artırır",
        evidence_level="Yüksek",
        clinical_warning="Hipoglisemi ve komplikasyon riski!",
        reference="Knott C et al. Diabetes Care. 2015",
        pmid="26604280"
    ),
    ("alcohol_heavy", "hypertension"): SynergyData(
        type="substance-disease",
        key1="alcohol_heavy",
        key2="hypertension",
        multiplier=1.4,
        mechanism="Alkol kan basıncını yükseltir",
        evidence_level="Çok Yüksek",
        clinical_warning="Hipertansif kriz riski!",
        reference="Roerecke M et al. Lancet Public Health. 2017",
        pmid="29253389"
    ),
    ("alcohol_dependence", "heart_failure"): SynergyData(
        type="substance-disease",
        key1="alcohol_dependence",
        key2="heart_failure",
        multiplier=1.8,
        mechanism="Alkolik kardiyomiyopati + kalp yetmezliği",
        evidence_level="Çok Yüksek",
        clinical_warning="Dekompansasyon riski çok yüksek!",
        reference="Piano MR et al. Circ Res. 2017",
        pmid="28450349"
    ),
    ("alcohol_heavy", "major_depression"): SynergyData(
        type="substance-disease",
        key1="alcohol_heavy",
        key2="major_depression",
        multiplier=1.5,
        mechanism="Alkol depresyonu şiddetlendirir, intihar riski",
        evidence_level="Çok Yüksek",
        clinical_warning="İntihar riski belirgin artar!",
        reference="Boden JM et al. Psychol Med. 2011",
        pmid="20540035"
    ),
    ("opioid_dependence", "hiv_aids"): SynergyData(
        type="substance-disease",
        key1="opioid_dependence",
        key2="hiv_aids",
        multiplier=2.0,
        mechanism="Opioidler immün supresyonu derinleştirir",
        evidence_level="Çok Yüksek",
        clinical_warning="HIV progresyonu hızlanır!",
        reference="Wang X et al. J Neuroimmune Pharmacol. 2011",
        pmid="21234691"
    ),
    ("opioid_use", "copd"): SynergyData(
        type="substance-disease",
        key1="opioid_use",
        key2="copd",
        multiplier=1.7,
        mechanism="Solunum depresyonu + KOAH = solunum yetmezliği",
        evidence_level="Çok Yüksek",
        clinical_warning="Solunum yetmezliği riski!",
        reference="Vozoris NT et al. Thorax. 2016",
        pmid="26490732"
    ),
    ("opioid_dependence", "hepatitis_c"): SynergyData(
        type="substance-disease",
        key1="opioid_dependence",
        key2="hepatitis_c",
        multiplier=1.7,
        mechanism="IV kullanım HCV bulaşını ve hasarı artırır",
        evidence_level="Çok Yüksek",
        clinical_warning="Fibrozis progresyonu hızlı!",
        reference="Schaefer M et al. J Hepatol. 2012",
        pmid="22173158"
    ),
    ("cocaine_use", "coronary_artery"): SynergyData(
        type="substance-disease",
        key1="cocaine_use",
        key2="coronary_artery",
        multiplier=2.2,
        mechanism="Kokain koroner vazospazm ve tromboz yapar",
        evidence_level="Çok Yüksek",
        clinical_warning="MI riski 24 kat artar!",
        reference="Havakuk O et al. J Am Coll Cardiol. 2017",
        pmid="29169477"
    ),
    ("cocaine_dependence", "hypertension"): SynergyData(
        type="substance-disease",
        key1="cocaine_dependence",
        key2="hypertension",
        multiplier=1.9,
        mechanism="Kokain + hipertansiyon = stroke riski",
        evidence_level="Çok Yüksek",
        clinical_warning="Hemorajik stroke riski!",
        reference="Bachi K et al. Addiction. 2017",
        pmid="28691738"
    ),
    ("cocaine_use", "heart_failure"): SynergyData(
        type="substance-disease",
        key1="cocaine_use",
        key2="heart_failure",
        multiplier=1.9,
        mechanism="Kokain kardiyomiyopatisi + KY",
        evidence_level="Yüksek",
        clinical_warning="Ani kardiyak ölüm riski!",
        reference="Havakuk O et al. J Am Coll Cardiol. 2017",
        pmid="29169477"
    ),
    ("methamphetamine_use", "coronary_artery"): SynergyData(
        type="substance-disease",
        key1="methamphetamine_use",
        key2="coronary_artery",
        multiplier=2.3,
        mechanism="Meth kardiyotoksisitesi + KAH",
        evidence_level="Yüksek",
        clinical_warning="Kardiyak arrest riski çok yüksek!",
        reference="Won S et al. Heart. 2018",
        pmid="29436389"
    ),
    ("methamphetamine_dependence", "stroke"): SynergyData(
        type="substance-disease",
        key1="methamphetamine_dependence",
        key2="stroke",
        multiplier=2.2,
        mechanism="Meth intraserebral hemoraji riskini artırır",
        evidence_level="Yüksek",
        clinical_warning="Tekrar kanama riski!",
        reference="Lappin JM et al. Stroke. 2017",
        pmid="28400495"
    ),
    ("methamphetamine_use", "schizophrenia"): SynergyData(
        type="substance-disease",
        key1="methamphetamine_use",
        key2="schizophrenia",
        multiplier=1.8,
        mechanism="Meth psikoz indüksiyonu + şizofreni",
        evidence_level="Yüksek",
        clinical_warning="Psikotik alevlenme riski!",
        reference="Chen CK et al. Psychol Med. 2003",
        pmid="14580079"
    ),
    ("tobacco_smoking", "copd"): SynergyData(
        type="substance-disease",
        key1="tobacco_smoking",
        key2="copd",
        multiplier=2.2,
        mechanism="Sigara KOAH progresyonunu hızlandırır",
        evidence_level="Çok Yüksek",
        clinical_warning="FEV1 kaybı hızlanır!",
        reference="Laniado-Laborín R. Int J COPD. 2009",
        pmid="19436692"
    ),
    ("tobacco_heavy", "coronary_artery"): SynergyData(
        type="substance-disease",
        key1="tobacco_heavy",
        key2="coronary_artery",
        multiplier=2.0,
        mechanism="Sigara ateroskleroz progresyonunu hızlandırır",
        evidence_level="Çok Yüksek",
        clinical_warning="MI riski 5 kat artar!",
        reference="Messner B et al. Cardiovasc Toxicol. 2014",
        pmid="24357217"
    ),
    ("tobacco_smoking", "type2_diabetes"): SynergyData(
        type="substance-disease",
        key1="tobacco_smoking",
        key2="type2_diabetes",
        multiplier=1.5,
        mechanism="Sigara insülin direncini ve komplikasyonları artırır",
        evidence_level="Çok Yüksek",
        clinical_warning="Diyabetik komplikasyonlar hızlanır!",
        reference="Śliwińska-Mossoń M et al. Diabetes Metab Res Rev. 2017",
        pmid="27558920"
    ),
    ("tobacco_heavy", "peripheral_artery"): SynergyData(
        type="substance-disease",
        key1="tobacco_heavy",
        key2="peripheral_artery",
        multiplier=2.0,
        mechanism="Sigara + PAH = amputasyon riski",
        evidence_level="Çok Yüksek",
        clinical_warning="Ekstremite kaybı riski!",
        reference="Agarwal S. J Am Heart Assoc. 2018",
        pmid="29502105"
    ),
    ("cannabis_heavy", "schizophrenia"): SynergyData(
        type="substance-disease",
        key1="cannabis_heavy",
        key2="schizophrenia",
        multiplier=1.6,
        mechanism="Esrar psikoz riskini artırır",
        evidence_level="Çok Yüksek",
        clinical_warning="Psikotik alevlenme riski!",
        reference="Marconi A et al. Schizophr Bull. 2016",
        pmid="26884547"
    ),
    ("cannabis_heavy", "major_depression"): SynergyData(
        type="substance-disease",
        key1="cannabis_heavy",
        key2="major_depression",
        multiplier=1.4,
        mechanism="Esrar depresyonu şiddetlendirebilir",
        evidence_level="Yüksek",
        clinical_warning="Motivasyon sendromu riski!",
        reference="Lev-Ran S et al. Psychol Med. 2014",
        pmid="23795679"
    ),
    ("benzodiazepine_dependence", "sleep_apnea"): SynergyData(
        type="substance-disease",
        key1="benzodiazepine_dependence",
        key2="sleep_apnea",
        multiplier=1.8,
        mechanism="Benzodiazepin solunum depresyonu + apne",
        evidence_level="Çok Yüksek",
        clinical_warning="Gece solunum durması riski!",
        reference="McMillan A et al. Ann Am Thorac Soc. 2015",
        pmid="25871209"
    ),
    ("alcohol_heavy", "alzheimer"): SynergyData(
        type="substance-disease",
        key1="alcohol_heavy",
        key2="alzheimer",
        multiplier=1.7,
        mechanism="Alkol nörodejenerasyonu hızlandırır",
        evidence_level="Yüksek",
        clinical_warning="Kognitif gerileme hızlanır!",
        reference="Topiwala A et al. BMJ. 2017",
        pmid="28588063"
    ),
    ("tobacco_smoking", "asthma"): SynergyData(
        type="substance-disease",
        key1="tobacco_smoking",
        key2="asthma",
        multiplier=1.6,
        mechanism="Sigara astım kontrolünü bozar",
        evidence_level="Çok Yüksek",
        clinical_warning="Atak sıklığı ve şiddeti artar!",
        reference="Thomson NC et al. Eur Respir J. 2013",
        pmid="23314899"
    ),
    ("anabolic_steroid", "coronary_artery"): SynergyData(
        type="substance-disease",
        key1="anabolic_steroid",
        key2="coronary_artery",
        multiplier=1.8,
        mechanism="Steroid kardiyomiyopatisi + KAH",
        evidence_level="Yüksek",
        clinical_warning="Ani kardiyak ölüm riski!",
        reference="Pope HG et al. Circulation. 2017",
        pmid="28533317"
    ),
    ("anabolic_steroid", "liver_nash"): SynergyData(
        type="substance-disease",
        key1="anabolic_steroid",
        key2="liver_nash",
        multiplier=1.6,
        mechanism="Steroid hepatotoksisitesi + NASH",
        evidence_level="Yüksek",
        clinical_warning="Siroza ilerleme riski!",
        reference="Pope HG et al. Circulation. 2017",
        pmid="28533317"
    ),
}


class DynamicCombinationCalculator:
    # nrcdnl94
    """Advanced calculator for unlimited substance + disease combinations"""
    
    def __init__(self):
        self.substances = SUBSTANCE_DATABASE
        self.diseases = DISEASE_DATABASE
        self.substance_synergies = SUBSTANCE_SUBSTANCE_SYNERGY
        self.disease_synergies = DISEASE_DISEASE_SYNERGY
        self.cross_synergies = SUBSTANCE_DISEASE_SYNERGY
    
    def get_risk_level(self, total_eaa: float) -> RiskLevel:
        """Determine risk level based on total EAA"""
        for level in RiskLevel:
            if level.value[2] <= total_eaa < level.value[3]:
                return level
        return RiskLevel.EXTREME
    
    def calculate_base_eaa(
        self,
        substance_keys: List[str],
        disease_keys: List[str]
    ) -> Tuple[float, float, List[dict], List[dict]]:
        """Calculate base EAA from substances and diseases"""
        substance_eaa = 0.0
        disease_eaa = 0.0
        substance_details = []
        disease_details = []
        
        for key in substance_keys:
            if key in self.substances:
                sub = self.substances[key]
                substance_eaa += sub.base_eaa
                substance_details.append({
                    'key': key,
                    'name_tr': sub.name_tr,
                    'name_en': sub.name_en,
                    'category': sub.category,
                    'eaa': sub.base_eaa,
                    'mechanism': sub.mechanism
                })
        
        for key in disease_keys:
            if key in self.diseases:
                dis = self.diseases[key]
                disease_eaa += dis.base_eaa
                disease_details.append({
                    'key': key,
                    'name_tr': dis.name_tr,
                    'name_en': dis.name_en,
                    'category': dis.category,
                    'eaa': dis.base_eaa,
                    'mechanism': dis.mechanism
                })
        
        return substance_eaa, disease_eaa, substance_details, disease_details
    
    def calculate_synergy_effects(
        self,
        substance_keys: List[str],
        disease_keys: List[str]
    ) -> Tuple[float, List[dict], List[str]]:
        """Calculate synergy multipliers and warnings"""
        synergy_bonus = 0.0
        synergy_details = []
        warnings = []
        
        for key1, key2 in itertools.combinations(substance_keys, 2):
            if (key1, key2) in self.substance_synergies:
                syn = self.substance_synergies[(key1, key2)]
                sub1 = self.substances.get(key1)
                sub2 = self.substances.get(key2)
                if sub1 and sub2:
                    base_sum = sub1.base_eaa + sub2.base_eaa
                    bonus = base_sum * (syn.multiplier - 1.0)
                    synergy_bonus += bonus
                    synergy_details.append({
                        'type': 'Madde-Madde',
                        'key1': key1,
                        'key2': key2,
                        'name1': sub1.name_tr,
                        'name2': sub2.name_tr,
                        'multiplier': syn.multiplier,
                        'bonus': bonus,
                        'mechanism': syn.mechanism,
                        'evidence': syn.evidence_level
                    })
                    if syn.clinical_warning:
                        warnings.append(f"⚠️ {sub1.name_tr} + {sub2.name_tr}: {syn.clinical_warning}")
            elif (key2, key1) in self.substance_synergies:
                syn = self.substance_synergies[(key2, key1)]
                sub1 = self.substances.get(key1)
                sub2 = self.substances.get(key2)
                if sub1 and sub2:
                    base_sum = sub1.base_eaa + sub2.base_eaa
                    bonus = base_sum * (syn.multiplier - 1.0)
                    synergy_bonus += bonus
                    synergy_details.append({
                        'type': 'Madde-Madde',
                        'key1': key2,
                        'key2': key1,
                        'name1': sub2.name_tr,
                        'name2': sub1.name_tr,
                        'multiplier': syn.multiplier,
                        'bonus': bonus,
                        'mechanism': syn.mechanism,
                        'evidence': syn.evidence_level
                    })
                    if syn.clinical_warning:
                        warnings.append(f"⚠️ {sub2.name_tr} + {sub1.name_tr}: {syn.clinical_warning}")
        
        for key1, key2 in itertools.combinations(disease_keys, 2):
            if (key1, key2) in self.disease_synergies:
                syn = self.disease_synergies[(key1, key2)]
                dis1 = self.diseases.get(key1)
                dis2 = self.diseases.get(key2)
                if dis1 and dis2:
                    base_sum = dis1.base_eaa + dis2.base_eaa
                    bonus = base_sum * (syn.multiplier - 1.0)
                    synergy_bonus += bonus
                    synergy_details.append({
                        'type': 'Hastalık-Hastalık',
                        'key1': key1,
                        'key2': key2,
                        'name1': dis1.name_tr,
                        'name2': dis2.name_tr,
                        'multiplier': syn.multiplier,
                        'bonus': bonus,
                        'mechanism': syn.mechanism,
                        'evidence': syn.evidence_level
                    })
                    if syn.clinical_warning:
                        warnings.append(f"⚠️ {dis1.name_tr} + {dis2.name_tr}: {syn.clinical_warning}")
            elif (key2, key1) in self.disease_synergies:
                syn = self.disease_synergies[(key2, key1)]
                dis1 = self.diseases.get(key1)
                dis2 = self.diseases.get(key2)
                if dis1 and dis2:
                    base_sum = dis1.base_eaa + dis2.base_eaa
                    bonus = base_sum * (syn.multiplier - 1.0)
                    synergy_bonus += bonus
                    synergy_details.append({
                        'type': 'Hastalık-Hastalık',
                        'key1': key2,
                        'key2': key1,
                        'name1': dis2.name_tr,
                        'name2': dis1.name_tr,
                        'multiplier': syn.multiplier,
                        'bonus': bonus,
                        'mechanism': syn.mechanism,
                        'evidence': syn.evidence_level
                    })
                    if syn.clinical_warning:
                        warnings.append(f"⚠️ {dis2.name_tr} + {dis1.name_tr}: {syn.clinical_warning}")
        
        for sub_key in substance_keys:
            for dis_key in disease_keys:
                if (sub_key, dis_key) in self.cross_synergies:
                    syn = self.cross_synergies[(sub_key, dis_key)]
                    sub = self.substances.get(sub_key)
                    dis = self.diseases.get(dis_key)
                    if sub and dis:
                        base_sum = sub.base_eaa + dis.base_eaa
                        bonus = base_sum * (syn.multiplier - 1.0)
                        synergy_bonus += bonus
                        synergy_details.append({
                            'type': 'Madde-Hastalık',
                            'key1': sub_key,
                            'key2': dis_key,
                            'name1': sub.name_tr,
                            'name2': dis.name_tr,
                            'multiplier': syn.multiplier,
                            'bonus': bonus,
                            'mechanism': syn.mechanism,
                            'evidence': syn.evidence_level
                        })
                        if syn.clinical_warning:
                            warnings.append(f"🔴 {sub.name_tr} + {dis.name_tr}: {syn.clinical_warning}")
        
        return synergy_bonus, synergy_details, warnings
    
    def calculate_complexity_bonus(
        self,
        num_substances: int,
        num_diseases: int
    ) -> float:
        """Calculate additional EAA from combination complexity"""
        if num_substances <= 1 and num_diseases <= 1:
            return 0.0
        
        total_items = num_substances + num_diseases
        if total_items >= 6:
            complexity_multiplier = 1.0 + (total_items - 2) * 0.1
            return complexity_multiplier
        elif total_items >= 4:
            return 0.5
        elif total_items >= 3:
            return 0.2
        return 0.0
    
    def calculate_full_combination(
        self,
        substance_keys: List[str],
        disease_keys: List[str]
    ) -> dict:
        """Calculate complete EAA analysis for any combination"""
        
        substance_eaa, disease_eaa, sub_details, dis_details = self.calculate_base_eaa(
            substance_keys, disease_keys
        )
        
        synergy_bonus, synergy_details, warnings = self.calculate_synergy_effects(
            substance_keys, disease_keys
        )
        
        complexity_bonus = self.calculate_complexity_bonus(
            len(substance_keys), len(disease_keys)
        )
        
        base_total = substance_eaa + disease_eaa
        total_with_synergy = base_total + synergy_bonus
        final_total = total_with_synergy + complexity_bonus
        
        risk_level = self.get_risk_level(final_total)
        
        num_potential_combinations = (
            len(list(itertools.combinations(substance_keys, 2))) +
            len(list(itertools.combinations(disease_keys, 2))) +
            len(substance_keys) * len(disease_keys)
        )
        
        return {
            'substance_eaa': round(substance_eaa, 2),
            'disease_eaa': round(disease_eaa, 2),
            'synergy_bonus': round(synergy_bonus, 2),
            'complexity_bonus': round(complexity_bonus, 2),
            'total_eaa': round(final_total, 2),
            'risk_level': risk_level.value[0],
            'risk_color': risk_level.value[1],
            'substances': sub_details,
            'diseases': dis_details,
            'synergies': synergy_details,
            'warnings': warnings,
            'num_substances': len(substance_keys),
            'num_diseases': len(disease_keys),
            'num_synergies_found': len(synergy_details),
            'num_potential_combinations': num_potential_combinations
        }
    
    def get_all_substances(self) -> List[dict]:
        """Get all substances with their details"""
        return [
            {
                'key': key,
                'name_tr': sub.name_tr,
                'name_en': sub.name_en,
                'category': sub.category,
                'base_eaa': sub.base_eaa
            }
            for key, sub in self.substances.items()
        ]
    
    def get_all_diseases(self) -> List[dict]:
        """Get all diseases with their details"""
        return [
            {
                'key': key,
                'name_tr': dis.name_tr,
                'name_en': dis.name_en,
                'category': dis.category,
                'base_eaa': dis.base_eaa
            }
            for key, dis in self.diseases.items()
        ]
    
    def get_substance_categories(self) -> List[str]:
        """Get unique substance categories"""
        return sorted(set(sub.category for sub in self.substances.values()))
    
    def get_disease_categories(self) -> List[str]:
        """Get unique disease categories"""
        return sorted(set(dis.category for dis in self.diseases.values()))
    
    def get_substances_by_category(self, category: str) -> List[dict]:
        """Get substances filtered by category"""
        return [
            {
                'key': key,
                'name_tr': sub.name_tr,
                'name_en': sub.name_en,
                'base_eaa': sub.base_eaa
            }
            for key, sub in self.substances.items()
            if sub.category == category
        ]
    
    def get_diseases_by_category(self, category: str) -> List[dict]:
        """Get diseases filtered by category"""
        return [
            {
                'key': key,
                'name_tr': dis.name_tr,
                'name_en': dis.name_en,
                'base_eaa': dis.base_eaa
            }
            for key, dis in self.diseases.items()
            if dis.category == category
        ]


def get_dynamic_calculator() -> DynamicCombinationCalculator:
    """Get calculator instance"""
    return DynamicCombinationCalculator()


def get_substance_count() -> int:
    """Get total number of substances"""
    return len(SUBSTANCE_DATABASE)


def get_disease_count() -> int:
    """Get total number of diseases"""
    return len(DISEASE_DATABASE)


def get_total_synergy_count() -> int:
    """Get total number of defined synergies"""
    return len(SUBSTANCE_SUBSTANCE_SYNERGY) + len(DISEASE_DISEASE_SYNERGY) + len(SUBSTANCE_DISEASE_SYNERGY)


def get_synergy_breakdown() -> dict:
    """Get synergy counts by type"""
    return {
        'substance_substance': len(SUBSTANCE_SUBSTANCE_SYNERGY),
        'disease_disease': len(DISEASE_DISEASE_SYNERGY),
        'substance_disease': len(SUBSTANCE_DISEASE_SYNERGY),
        'total': get_total_synergy_count()
    }


# End of module - # nrcdnl94