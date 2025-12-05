# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
Synergistic Effects Module - Addiction + Chronic Disease Interactions
Calculates combined epigenetic age acceleration from substance use and chronic diseases

This module implements evidence-based synergistic multipliers for combinations of:
- Substance use disorders (alcohol, opioids, cocaine, methamphetamine, cannabis, tobacco)
- Chronic diseases (cardiovascular, metabolic, hepatic, pulmonary, infectious, neurological)

Author: Dr. Nurcan Denli Bayır
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import pandas as pd


class SubstanceType(Enum):
    # nrcdnl94
    ALCOHOL = "Alkol"
    OPIOIDS = "Opioidler"
    COCAINE = "Kokain"
    METHAMPHETAMINE = "Metamfetamin"
    CANNABIS = "Esrar"
    TOBACCO = "Sigara/Nikotin"
    POLYSUBSTANCE = "Çoklu Madde"


@dataclass
# nrcdnl94
class SubstanceEAAEffect:
    # nrcdnl94
    """Substance use EAA effect data"""
    substance_type: SubstanceType
    substance_name: str
    substance_name_en: str
    base_eaa: float
    ci_lower: float
    ci_upper: float
    clock_type: str
    mechanism: str
    sample_size: int
    reference: str
    pmid: str


@dataclass
# nrcdnl94
class SynergyInteraction:
    # nrcdnl94
    """Synergistic interaction between substance and disease"""
    substance_key: str
    disease_key: str
    synergy_multiplier: float
    mechanism: str
    evidence_level: str
    reference: str
    pmid: str


SUBSTANCE_EAA_DATABASE = {
    # nrcdnl94
    "alcohol_moderate": SubstanceEAAEffect(
        substance_type=SubstanceType.ALCOHOL,
        substance_name="Alkol (Orta Düzey)",
        substance_name_en="Alcohol (Moderate)",
        base_eaa=1.2,
        ci_lower=0.8,
        ci_upper=1.6,
        clock_type="GrimAge",
        mechanism="Oksidatif stres, karaciğer hasarı, inflamasyon",
        sample_size=2183,
        reference="Rosen AD et al. Alcohol Clin Exp Res. 2018",
        pmid="29336043"
    ),
    "alcohol_heavy": SubstanceEAAEffect(
        substance_type=SubstanceType.ALCOHOL,
        substance_name="Alkol (Ağır Kullanım)",
        substance_name_en="Alcohol (Heavy Use)",
        base_eaa=3.6,
        ci_lower=3.1,
        ci_upper=4.2,
        clock_type="GrimAge",
        mechanism="Kronik hepatotoksisite, nörodejenerasyon, sistemik inflamasyon",
        sample_size=1542,
        reference="Beach SRH et al. Alcohol Clin Exp Res. 2022",
        pmid="35312089"
    ),
    "alcohol_dependence": SubstanceEAAEffect(
        substance_type=SubstanceType.ALCOHOL,
        substance_name="Alkol Bağımlılığı",
        substance_name_en="Alcohol Dependence",
        base_eaa=5.2,
        ci_lower=4.5,
        ci_upper=5.9,
        clock_type="GrimAge",
        mechanism="Siroz, Wernicke-Korsakoff, kardiyomiyopati",
        sample_size=892,
        reference="Luo A et al. Transl Psychiatry. 2020",
        pmid="32066732"
    ),
    "opioid_use": SubstanceEAAEffect(
        substance_type=SubstanceType.OPIOIDS,
        substance_name="Opioid Kullanımı",
        substance_name_en="Opioid Use",
        base_eaa=2.9,
        ci_lower=2.5,
        ci_upper=3.4,
        clock_type="GrimAge",
        mechanism="İmmün supresyon, hormonal bozukluk, solunum depresyonu",
        sample_size=1360,
        reference="Cheng Z et al. Drug Alcohol Depend. 2021",
        pmid="33862541"
    ),
    "opioid_dependence": SubstanceEAAEffect(
        substance_type=SubstanceType.OPIOIDS,
        substance_name="Opioid Bağımlılığı",
        substance_name_en="Opioid Dependence",
        base_eaa=4.8,
        ci_lower=4.1,
        ci_upper=5.5,
        clock_type="GrimAge",
        mechanism="Kronik stres yanıtı, HPA aks disregülasyonu, enfeksiyon riski",
        sample_size=756,
        reference="Browne CJ et al. Neuropsychopharmacology. 2020",
        pmid="32349119"
    ),
    "cocaine_use": SubstanceEAAEffect(
        substance_type=SubstanceType.COCAINE,
        substance_name="Kokain Kullanımı",
        substance_name_en="Cocaine Use",
        base_eaa=4.1,
        ci_lower=3.5,
        ci_upper=4.7,
        clock_type="GrimAge",
        mechanism="Kardiyovasküler stres, dopamin toksisitesi, vazokonstriksiyon",
        sample_size=1030,
        reference="Nylander E et al. Neuropsychopharmacology. 2017",
        pmid="27649641"
    ),
    "cocaine_dependence": SubstanceEAAEffect(
        substance_type=SubstanceType.COCAINE,
        substance_name="Kokain Bağımlılığı",
        substance_name_en="Cocaine Dependence",
        base_eaa=5.8,
        ci_lower=5.0,
        ci_upper=6.6,
        clock_type="GrimAge",
        mechanism="Kronik kardiyomiyopati, serebrovasküler hasar, immün disfonksiyon",
        sample_size=485,
        reference="Vaillancourt K et al. Transl Psychiatry. 2021",
        pmid="34561417"
    ),
    "methamphetamine_use": SubstanceEAAEffect(
        substance_type=SubstanceType.METHAMPHETAMINE,
        substance_name="Metamfetamin Kullanımı",
        substance_name_en="Methamphetamine Use",
        base_eaa=6.2,
        ci_lower=4.5,
        ci_upper=8.1,
        clock_type="GrimAge",
        mechanism="Nörotoksisite, oksidatif hasar, mitokondriyal disfonksiyon",
        sample_size=48,
        reference="Godino A et al. Psychopharmacology. 2021",
        pmid="33594537"
    ),
    "methamphetamine_dependence": SubstanceEAAEffect(
        substance_type=SubstanceType.METHAMPHETAMINE,
        substance_name="Metamfetamin Bağımlılığı",
        substance_name_en="Methamphetamine Dependence",
        base_eaa=8.5,
        ci_lower=6.8,
        ci_upper=10.2,
        clock_type="GrimAge",
        mechanism="Ağır nörodejenerasyon, kardiyak aritmiler, psikoz",
        sample_size=32,
        reference="Godino A et al. Psychopharmacology. 2021",
        pmid="33594537"
    ),
    "cannabis_regular": SubstanceEAAEffect(
        substance_type=SubstanceType.CANNABIS,
        substance_name="Esrar (Düzenli Kullanım)",
        substance_name_en="Cannabis (Regular Use)",
        base_eaa=0.8,
        ci_lower=0.3,
        ci_upper=1.4,
        clock_type="Horvath",
        mechanism="Endokannabinoid sistem değişiklikleri, pulmoner etki",
        sample_size=194,
        reference="Schrott R et al. Clin Epigenetics. 2020",
        pmid="32928293"
    ),
    "cannabis_heavy": SubstanceEAAEffect(
        substance_type=SubstanceType.CANNABIS,
        substance_name="Esrar (Ağır Kullanım)",
        substance_name_en="Cannabis (Heavy Use)",
        base_eaa=1.8,
        ci_lower=1.1,
        ci_upper=2.5,
        clock_type="Horvath",
        mechanism="Kronik pulmoner hasar, nörokognitif değişiklikler",
        sample_size=87,
        reference="Schrott R et al. Clin Epigenetics. 2020",
        pmid="32928293"
    ),
    "tobacco_smoking": SubstanceEAAEffect(
        substance_type=SubstanceType.TOBACCO,
        substance_name="Sigara İçimi",
        substance_name_en="Tobacco Smoking",
        base_eaa=2.8,
        ci_lower=2.3,
        ci_upper=3.3,
        clock_type="GrimAge",
        mechanism="Pulmoner hasar, vasküler endotel disfonksiyonu, kanser riski",
        sample_size=4521,
        reference="Yang Y et al. Nat Commun. 2020",
        pmid="32393754"
    ),
    "tobacco_heavy": SubstanceEAAEffect(
        substance_type=SubstanceType.TOBACCO,
        substance_name="Ağır Sigara Kullanımı (>20/gün)",
        substance_name_en="Heavy Tobacco Use (>20/day)",
        base_eaa=4.5,
        ci_lower=3.8,
        ci_upper=5.2,
        clock_type="GrimAge",
        mechanism="KOAH gelişimi, hızlanmış ateroskleroz, multipl organ hasarı",
        sample_size=1876,
        reference="Yang Y et al. Nat Commun. 2020",
        pmid="32393754"
    ),
    "polysubstance": SubstanceEAAEffect(
        substance_type=SubstanceType.POLYSUBSTANCE,
        substance_name="Çoklu Madde Kullanımı",
        substance_name_en="Polysubstance Use",
        base_eaa=7.3,
        ci_lower=6.4,
        ci_upper=8.3,
        clock_type="GrimAge",
        mechanism="Kümülatif organ hasarı, ilaç etkileşimleri, sistemik toksisite",
        sample_size=720,
        reference="Rosen AD et al. Drug Alcohol Depend. 2018",
        pmid="29336043"
    ),
}

SUBSTANCE_DISEASE_SYNERGY = {
    # nrcdnl94
    ("alcohol_heavy", "liver_cirrhosis"): SynergyInteraction(
        substance_key="alcohol_heavy",
        disease_key="liver_cirrhosis",
        synergy_multiplier=1.8,
        mechanism="Alkol siroz progresyonunu hızlandırır, hepatosellüler hasar katlanır",
        evidence_level="Yüksek",
        reference="Louvet A et al. J Hepatol. 2017",
        pmid="28267622"
    ),
    ("alcohol_dependence", "liver_cirrhosis"): SynergyInteraction(
        substance_key="alcohol_dependence",
        disease_key="liver_cirrhosis",
        synergy_multiplier=2.2,
        mechanism="Bağımlılık düzeyinde alkol karaciğer yetmezliğini dramatik şekilde hızlandırır",
        evidence_level="Yüksek",
        reference="Louvet A et al. J Hepatol. 2017",
        pmid="28267622"
    ),
    ("alcohol_heavy", "hepatitis_c"): SynergyInteraction(
        substance_key="alcohol_heavy",
        disease_key="hepatitis_c",
        synergy_multiplier=1.6,
        mechanism="Alkol + HCV kombinasyonu fibrozis hızını 3 kat artırır",
        evidence_level="Yüksek",
        reference="Szabo G et al. Nat Rev Gastroenterol Hepatol. 2015",
        pmid="25534115"
    ),
    ("alcohol_heavy", "hepatitis_b"): SynergyInteraction(
        substance_key="alcohol_heavy",
        disease_key="hepatitis_b",
        synergy_multiplier=1.5,
        mechanism="Alkol HBV replikasyonunu artırır, karaciğer hasarını şiddetlendirir",
        evidence_level="Orta",
        reference="Szabo G et al. Nat Rev Gastroenterol Hepatol. 2015",
        pmid="25534115"
    ),
    ("alcohol_heavy", "type2_diabetes"): SynergyInteraction(
        substance_key="alcohol_heavy",
        disease_key="type2_diabetes",
        synergy_multiplier=1.4,
        mechanism="Alkol insülin direncini artırır, diyabetik komplikasyonları hızlandırır",
        evidence_level="Orta",
        reference="Knott C et al. Diabetes Care. 2015",
        pmid="26604280"
    ),
    ("alcohol_heavy", "hypertension"): SynergyInteraction(
        substance_key="alcohol_heavy",
        disease_key="hypertension",
        synergy_multiplier=1.3,
        mechanism="Alkol kan basıncını yükseltir, kardiyovasküler riski artırır",
        evidence_level="Yüksek",
        reference="Roerecke M et al. Lancet Public Health. 2017",
        pmid="29253389"
    ),
    ("alcohol_heavy", "heart_failure"): SynergyInteraction(
        substance_key="alcohol_heavy",
        disease_key="heart_failure",
        synergy_multiplier=1.5,
        mechanism="Alkolik kardiyomiyopati kalp yetmezliğini şiddetlendirir",
        evidence_level="Yüksek",
        reference="Piano MR et al. Circ Res. 2017",
        pmid="28450349"
    ),
    ("opioid_dependence", "hiv_aids"): SynergyInteraction(
        substance_key="opioid_dependence",
        disease_key="hiv_aids",
        synergy_multiplier=1.9,
        mechanism="Opioidler immün supresyonu derinleştirir, HIV progresyonunu hızlandırır",
        evidence_level="Yüksek",
        reference="Wang X et al. J Neuroimmune Pharmacol. 2011",
        pmid="21234691"
    ),
    ("opioid_use", "hiv_aids"): SynergyInteraction(
        substance_key="opioid_use",
        disease_key="hiv_aids",
        synergy_multiplier=1.5,
        mechanism="Opioidler CD4+ T hücre fonksiyonunu bozar",
        evidence_level="Yüksek",
        reference="Wang X et al. J Neuroimmune Pharmacol. 2011",
        pmid="21234691"
    ),
    ("opioid_dependence", "hepatitis_c"): SynergyInteraction(
        substance_key="opioid_dependence",
        disease_key="hepatitis_c",
        synergy_multiplier=1.6,
        mechanism="IV opioid kullanımı HCV bulaşını ve karaciğer hasarını artırır",
        evidence_level="Yüksek",
        reference="Schaefer M et al. J Hepatol. 2012",
        pmid="22173158"
    ),
    ("cocaine_use", "coronary_artery"): SynergyInteraction(
        substance_key="cocaine_use",
        disease_key="coronary_artery",
        synergy_multiplier=2.0,
        mechanism="Kokain koroner vazospazm ve tromboz riskini dramatik artırır",
        evidence_level="Yüksek",
        reference="Havakuk O et al. J Am Coll Cardiol. 2017",
        pmid="29169477"
    ),
    ("cocaine_dependence", "coronary_artery"): SynergyInteraction(
        substance_key="cocaine_dependence",
        disease_key="coronary_artery",
        synergy_multiplier=2.5,
        mechanism="Kronik kokain kardiyak iskemi ve MI riskini 24 kat artırır",
        evidence_level="Yüksek",
        reference="Havakuk O et al. J Am Coll Cardiol. 2017",
        pmid="29169477"
    ),
    ("cocaine_use", "hypertension"): SynergyInteraction(
        substance_key="cocaine_use",
        disease_key="hypertension",
        synergy_multiplier=1.7,
        mechanism="Kokain + hipertansiyon stroke riskini çok yükseltir",
        evidence_level="Yüksek",
        reference="Bachi K et al. Addiction. 2017",
        pmid="28691738"
    ),
    ("cocaine_use", "heart_failure"): SynergyInteraction(
        substance_key="cocaine_use",
        disease_key="heart_failure",
        synergy_multiplier=1.8,
        mechanism="Kokain kardiyomiyopatisi kalp yetmezliğini hızlandırır",
        evidence_level="Orta",
        reference="Havakuk O et al. J Am Coll Cardiol. 2017",
        pmid="29169477"
    ),
    ("methamphetamine_use", "coronary_artery"): SynergyInteraction(
        substance_key="methamphetamine_use",
        disease_key="coronary_artery",
        synergy_multiplier=2.2,
        mechanism="Meth kardiyotoksik, koroner hastalıkla sinerjik etki gösterir",
        evidence_level="Orta",
        reference="Won S et al. Heart. 2018",
        pmid="29436389"
    ),
    ("methamphetamine_use", "stroke"): SynergyInteraction(
        substance_key="methamphetamine_use",
        disease_key="stroke",
        synergy_multiplier=2.0,
        mechanism="Meth intraserebral hemoraji riskini belirgin artırır",
        evidence_level="Orta",
        reference="Lappin JM et al. Stroke. 2017",
        pmid="28400495"
    ),
    ("tobacco_smoking", "copd"): SynergyInteraction(
        substance_key="tobacco_smoking",
        disease_key="copd",
        synergy_multiplier=2.0,
        mechanism="Sigara KOAH'ın primer nedeni, devam etmesi progresyonu hızlandırır",
        evidence_level="Çok Yüksek",
        reference="Laniado-Laborín R. Int J Chron Obstruct Pulmon Dis. 2009",
        pmid="19436692"
    ),
    ("tobacco_heavy", "copd"): SynergyInteraction(
        substance_key="tobacco_heavy",
        disease_key="copd",
        synergy_multiplier=2.5,
        mechanism="Ağır sigara KOAH'ta hızlı FEV1 kaybına yol açar",
        evidence_level="Çok Yüksek",
        reference="Laniado-Laborín R. Int J Chron Obstruct Pulmon Dis. 2009",
        pmid="19436692"
    ),
    ("tobacco_smoking", "asthma"): SynergyInteraction(
        substance_key="tobacco_smoking",
        disease_key="asthma",
        synergy_multiplier=1.6,
        mechanism="Sigara astım kontrolünü bozar, atak sıklığını artırır",
        evidence_level="Yüksek",
        reference="Thomson NC et al. Eur Respir J. 2013",
        pmid="23314899"
    ),
    ("tobacco_smoking", "coronary_artery"): SynergyInteraction(
        substance_key="tobacco_smoking",
        disease_key="coronary_artery",
        synergy_multiplier=1.8,
        mechanism="Sigara ateroskleroz progresyonunu hızlandırır",
        evidence_level="Çok Yüksek",
        reference="Messner B et al. Cardiovasc Toxicol. 2014",
        pmid="24357217"
    ),
    ("tobacco_heavy", "coronary_artery"): SynergyInteraction(
        substance_key="tobacco_heavy",
        disease_key="coronary_artery",
        synergy_multiplier=2.2,
        mechanism="Ağır sigara + KAH kombinasyonu MI riskini 5 kat artırır",
        evidence_level="Çok Yüksek",
        reference="Messner B et al. Cardiovasc Toxicol. 2014",
        pmid="24357217"
    ),
    ("tobacco_smoking", "type2_diabetes"): SynergyInteraction(
        substance_key="tobacco_smoking",
        disease_key="type2_diabetes",
        synergy_multiplier=1.4,
        mechanism="Sigara insülin direncini artırır, diyabetik komplikasyonları hızlandırır",
        evidence_level="Yüksek",
        reference="Śliwińska-Mossoń M et al. Diabetes Metab Res Rev. 2017",
        pmid="27558920"
    ),
    ("tobacco_smoking", "hypertension"): SynergyInteraction(
        substance_key="tobacco_smoking",
        disease_key="hypertension",
        synergy_multiplier=1.5,
        mechanism="Sigara + hipertansiyon kardiyovasküler riski katlar",
        evidence_level="Yüksek",
        reference="Virdis A et al. Curr Pharm Des. 2010",
        pmid="20236064"
    ),
    ("polysubstance", "hiv_aids"): SynergyInteraction(
        substance_key="polysubstance",
        disease_key="hiv_aids",
        synergy_multiplier=2.0,
        mechanism="Çoklu madde kullanımı immün sistemi çökertir, HIV progresyonunu hızlandırır",
        evidence_level="Yüksek",
        reference="Carrico AW et al. AIDS. 2014",
        pmid="24378753"
    ),
    ("polysubstance", "hepatitis_c"): SynergyInteraction(
        substance_key="polysubstance",
        disease_key="hepatitis_c",
        synergy_multiplier=1.8,
        mechanism="Çoklu madde karaciğer hasarını şiddetlendirir",
        evidence_level="Orta",
        reference="Schaefer M et al. J Hepatol. 2012",
        pmid="22173158"
    ),
    ("polysubstance", "major_depression"): SynergyInteraction(
        substance_key="polysubstance",
        disease_key="major_depression",
        synergy_multiplier=1.6,
        mechanism="Çoklu madde + depresyon nöroinflamatuvar döngüyü şiddetlendirir",
        evidence_level="Orta",
        reference="Hser YI et al. Addiction. 2015",
        pmid="25664682"
    ),
    ("alcohol_dependence", "major_depression"): SynergyInteraction(
        substance_key="alcohol_dependence",
        disease_key="major_depression",
        synergy_multiplier=1.5,
        mechanism="Alkol bağımlılığı + depresyon karşılıklı olarak kötüleşir",
        evidence_level="Yüksek",
        reference="Boden JM et al. Psychol Med. 2011",
        pmid="20540035"
    ),
    ("opioid_dependence", "major_depression"): SynergyInteraction(
        substance_key="opioid_dependence",
        disease_key="major_depression",
        synergy_multiplier=1.4,
        mechanism="Opioid bağımlılığı + depresyon tedavi yanıtını azaltır",
        evidence_level="Orta",
        reference="Sullivan MD et al. JAMA Psychiatry. 2018",
        pmid="29238794"
    ),
    ("methamphetamine_dependence", "schizophrenia"): SynergyInteraction(
        substance_key="methamphetamine_dependence",
        disease_key="schizophrenia",
        synergy_multiplier=1.8,
        mechanism="Meth psikoz riskini artırır, şizofrenide prognozu kötüleştirir",
        evidence_level="Orta",
        reference="Chen CK et al. Psychol Med. 2003",
        pmid="14580079"
    ),
    ("cannabis_heavy", "schizophrenia"): SynergyInteraction(
        substance_key="cannabis_heavy",
        disease_key="schizophrenia",
        synergy_multiplier=1.5,
        mechanism="Esrar şizofreni başlangıcını erkene çeker, semptomları şiddetlendirir",
        evidence_level="Yüksek",
        reference="Marconi A et al. Schizophr Bull. 2016",
        pmid="26884547"
    ),
    ("alcohol_heavy", "alzheimer"): SynergyInteraction(
        substance_key="alcohol_heavy",
        disease_key="alzheimer",
        synergy_multiplier=1.6,
        mechanism="Alkol nörodejenerasyonu hızlandırır, Alzheimer progresyonunu artırır",
        evidence_level="Orta",
        reference="Topiwala A et al. BMJ. 2017",
        pmid="28588063"
    ),
}


class SynergisticEffectCalculator:
    # nrcdnl94
    """Calculator for combined substance use and chronic disease EAA effects"""
    
    def __init__(self):
        self.substance_database = SUBSTANCE_EAA_DATABASE
        self.synergy_database = SUBSTANCE_DISEASE_SYNERGY
    
    def get_substance_eaa(self, substance_key: str) -> Optional[float]:
        """Get base EAA for a substance"""
        if substance_key in self.substance_database:
            return self.substance_database[substance_key].base_eaa
        return None
    
    def get_synergy_multiplier(self, substance_key: str, disease_key: str) -> Optional[float]:
        """Get synergy multiplier for substance-disease combination"""
        key = (substance_key, disease_key)
        if key in self.synergy_database:
            return self.synergy_database[key].synergy_multiplier
        return None
    
    def calculate_combined_eaa(
        self, 
        substance_keys: List[str], 
        disease_keys: List[str],
        disease_eaa_dict: Dict[str, float]
    ) -> Dict:
        """
        Calculate total EAA considering:
        1. Substance base effects
        2. Disease base effects
        3. Synergistic interactions between substances and diseases
        
        Args:
            substance_keys: List of substance identifiers
            disease_keys: List of disease identifiers
            disease_eaa_dict: Dictionary mapping disease_key to its EAA effect
        
        Returns:
            Dict with detailed breakdown of EAA contributions
        """
        result = {
            'substance_eaa': 0.0,
            'disease_eaa': 0.0,
            'synergy_bonus': 0.0,
            'total_eaa': 0.0,
            'substances': [],
            'diseases': [],
            'synergies': [],
            'risk_level': '',
            'warning_messages': []
        }
        
        for sub_key in substance_keys:
            if sub_key in self.substance_database:
                sub = self.substance_database[sub_key]
                result['substance_eaa'] += sub.base_eaa
                result['substances'].append({
                    'key': sub_key,
                    'name': sub.substance_name,
                    'name_en': sub.substance_name_en,
                    'eaa': sub.base_eaa,
                    'mechanism': sub.mechanism
                })
        
        for dis_key in disease_keys:
            if dis_key in disease_eaa_dict:
                eaa = disease_eaa_dict[dis_key]
                result['disease_eaa'] += eaa
                result['diseases'].append({
                    'key': dis_key,
                    'eaa': eaa
                })
        
        for sub_key in substance_keys:
            for dis_key in disease_keys:
                synergy_key = (sub_key, dis_key)
                if synergy_key in self.synergy_database:
                    synergy = self.synergy_database[synergy_key]
                    
                    sub_eaa = self.get_substance_eaa(sub_key) or 0
                    dis_eaa = disease_eaa_dict.get(dis_key, 0)
                    combined_base = sub_eaa + dis_eaa
                    
                    synergy_effect = combined_base * (synergy.synergy_multiplier - 1)
                    result['synergy_bonus'] += synergy_effect
                    
                    result['synergies'].append({
                        'substance': sub_key,
                        'disease': dis_key,
                        'multiplier': synergy.synergy_multiplier,
                        'bonus_eaa': round(synergy_effect, 2),
                        'mechanism': synergy.mechanism,
                        'evidence': synergy.evidence_level,
                        'reference': synergy.reference
                    })
                    
                    if synergy.synergy_multiplier >= 2.0:
                        result['warning_messages'].append(
                            f"⚠️ YÜKSEK RİSK: {self.substance_database[sub_key].substance_name} + "
                            f"hastalık kombinasyonu çok riskli (çarpan: x{synergy.synergy_multiplier})"
                        )
        
        result['total_eaa'] = round(
            result['substance_eaa'] + result['disease_eaa'] + result['synergy_bonus'], 
            2
        )
        result['substance_eaa'] = round(result['substance_eaa'], 2)
        result['disease_eaa'] = round(result['disease_eaa'], 2)
        result['synergy_bonus'] = round(result['synergy_bonus'], 2)
        
        if result['total_eaa'] >= 15:
            result['risk_level'] = 'Çok Yüksek'
        elif result['total_eaa'] >= 10:
            result['risk_level'] = 'Yüksek'
        elif result['total_eaa'] >= 5:
            result['risk_level'] = 'Orta-Yüksek'
        elif result['total_eaa'] >= 3:
            result['risk_level'] = 'Orta'
        else:
            result['risk_level'] = 'Düşük-Orta'
        
        return result
    
    def get_substance_summary_table(self) -> pd.DataFrame:
        """Get summary table of all substances and their EAA effects"""
        data = []
        for key, sub in self.substance_database.items():
            data.append({
                'Anahtar': key,
                'Madde': sub.substance_name,
                'Madde (EN)': sub.substance_name_en,
                'Tür': sub.substance_type.value,
                'EAA (yıl)': sub.base_eaa,
                '95% GA Alt': sub.ci_lower,
                '95% GA Üst': sub.ci_upper,
                'Saat': sub.clock_type,
                'n': sub.sample_size
            })
        return pd.DataFrame(data).sort_values('EAA (yıl)', ascending=False)
    
    def get_synergy_summary_table(self) -> pd.DataFrame:
        """Get summary table of all synergistic interactions"""
        data = []
        for (sub_key, dis_key), synergy in self.synergy_database.items():
            sub_name = self.substance_database[sub_key].substance_name if sub_key in self.substance_database else sub_key
            data.append({
                'Madde': sub_name,
                'Hastalık': dis_key,
                'Sinerjik Çarpan': synergy.synergy_multiplier,
                'Kanıt Düzeyi': synergy.evidence_level,
                'Mekanizma': synergy.mechanism[:60] + '...' if len(synergy.mechanism) > 60 else synergy.mechanism,
                'Referans': synergy.reference
            })
        return pd.DataFrame(data).sort_values('Sinerjik Çarpan', ascending=False)
    
    def get_high_risk_combinations(self, min_multiplier: float = 1.8) -> List[Dict]:
        """Get list of high-risk substance-disease combinations"""
        high_risk = []
        for (sub_key, dis_key), synergy in self.synergy_database.items():
            if synergy.synergy_multiplier >= min_multiplier:
                sub_name = self.substance_database[sub_key].substance_name if sub_key in self.substance_database else sub_key
                high_risk.append({
                    'substance': sub_name,
                    'disease': dis_key,
                    'multiplier': synergy.synergy_multiplier,
                    'mechanism': synergy.mechanism,
                    'evidence': synergy.evidence_level
                })
        return sorted(high_risk, key=lambda x: x['multiplier'], reverse=True)


def get_synergistic_calculator() -> SynergisticEffectCalculator:
    """Get singleton instance of calculator"""
    return SynergisticEffectCalculator()


def get_substance_count() -> int:
    """Get total number of substances in database"""
    return len(SUBSTANCE_EAA_DATABASE)


def get_synergy_count() -> int:
    """Get total number of synergistic interactions"""
    return len(SUBSTANCE_DISEASE_SYNERGY)


def get_substance_options() -> Dict[str, str]:
    """Get substance options for UI selection"""
    return {sub.substance_name: key for key, sub in SUBSTANCE_EAA_DATABASE.items()}


# End of module - # nrcdnl94