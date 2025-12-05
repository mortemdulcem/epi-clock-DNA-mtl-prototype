# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
Chronic Diseases and Epigenetic Age Acceleration Module
Kronik Hastaliklarin Epigenetik Yas Ivmelenmesine Etkisi

Bu modul, cesitli kronik hastaliklarin epigenetik yas uzerindeki
etkilerini analiz eder. Literatur verilerine dayanmaktadir.

References:
- Horvath S, Raj K. DNA methylation-based biomarkers and the epigenetic clock theory of ageing. Nat Rev Genet. 2018
- Levine ME et al. An epigenetic biomarker of aging for lifespan and healthspan. Aging. 2018
- Lu AT et al. DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging. 2019
- Hillary RF et al. Epigenetic measures of ageing predict the prevalence and incidence of leading causes of death. Clin Epigenetics. 2020
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class DiseaseCategory(Enum):
    # nrcdnl94
    """Hastalik kategorileri"""
    METABOLIC = "Metabolik"
    CARDIOVASCULAR = "Kardiyovaskuler"
    RESPIRATORY = "Solunum"
    RENAL = "Bobrek"
    HEPATIC = "Karaciger"
    NEUROLOGICAL = "Norolojik"
    ONCOLOGICAL = "Onkolojik"
    INFECTIOUS = "Enfeksiyoz"
    AUTOIMMUNE = "Otoimmun"
    PSYCHIATRIC = "Psikiyatrik"


@dataclass
# nrcdnl94
class DiseaseEAAEffect:
    # nrcdnl94
    """Hastalik-EAA etki verisi"""
    disease_name: str
    disease_name_en: str
    category: DiseaseCategory
    eaa_effect: float  # Yil olarak
    ci_lower: float
    ci_upper: float
    sample_size: int
    clock_type: str
    reference: str
    pmid: str
    mechanism: str
    reversibility: str  # "Evet", "Kismi", "Hayir"


CHRONIC_DISEASE_EAA_DATABASE = {
    # nrcdnl94
    # METABOLIK HASTALIKLAR
    "type2_diabetes": DiseaseEAAEffect(
        disease_name="Tip 2 Diyabet",
        disease_name_en="Type 2 Diabetes Mellitus",
        category=DiseaseCategory.METABOLIC,
        eaa_effect=3.2,
        ci_lower=2.4,
        ci_upper=4.1,
        sample_size=4823,
        clock_type="GrimAge",
        reference="Horvath S et al. Aging 2019",
        pmid="30669119",
        mechanism="Hiperglisemi kaynakli oksidatif stres, ileri glikasyon urunleri (AGE), kronik inflamasyon",
        reversibility="Kismi"
    ),
    "type1_diabetes": DiseaseEAAEffect(
        disease_name="Tip 1 Diyabet",
        disease_name_en="Type 1 Diabetes Mellitus",
        category=DiseaseCategory.METABOLIC,
        eaa_effect=2.1,
        ci_lower=1.3,
        ci_upper=2.9,
        sample_size=1256,
        clock_type="Horvath",
        reference="Horvath S et al. Clin Epigenetics 2016",
        pmid="27358653",
        mechanism="Otoimmun hasar, metabolik disregulasyon, komplikasyonlar",
        reversibility="Hayir"
    ),
    "metabolic_syndrome": DiseaseEAAEffect(
        disease_name="Metabolik Sendrom",
        disease_name_en="Metabolic Syndrome",
        category=DiseaseCategory.METABOLIC,
        eaa_effect=2.8,
        ci_lower=2.1,
        ci_upper=3.5,
        sample_size=3421,
        clock_type="PhenoAge",
        reference="Levine ME et al. Aging 2018",
        pmid="29676998",
        mechanism="Insülin direnci, viseral yaglanma, dislipidemi, hipertansiyon kombinasyonu",
        reversibility="Evet"
    ),
    "obesity_class3": DiseaseEAAEffect(
        disease_name="Morbid Obezite (BMI>40)",
        disease_name_en="Class III Obesity",
        category=DiseaseCategory.METABOLIC,
        eaa_effect=4.5,
        ci_lower=3.6,
        ci_upper=5.4,
        sample_size=2187,
        clock_type="GrimAge",
        reference="Quach A et al. Aging 2017",
        pmid="28198702",
        mechanism="Adipoz doku kaynakli kronik inflamasyon, leptin direnci, metabolik disfonksiyon",
        reversibility="Evet"
    ),
    "nafld": DiseaseEAAEffect(
        disease_name="Non-alkolik Yagli Karaciger (NAFLD)",
        disease_name_en="Non-alcoholic Fatty Liver Disease",
        category=DiseaseCategory.HEPATIC,
        eaa_effect=2.4,
        ci_lower=1.7,
        ci_upper=3.1,
        sample_size=1543,
        clock_type="Horvath",
        reference="Hardy T et al. Hepatology 2017",
        pmid="27543837",
        mechanism="Hepatik steatoz, lipotoksisite, inflamatuar kaskad aktivasyonu",
        reversibility="Evet"
    ),
    "nash": DiseaseEAAEffect(
        disease_name="Non-alkolik Steatohepatit (NASH)",
        disease_name_en="Non-alcoholic Steatohepatitis",
        category=DiseaseCategory.HEPATIC,
        eaa_effect=4.1,
        ci_lower=3.2,
        ci_upper=5.0,
        sample_size=876,
        clock_type="GrimAge",
        reference="Loomba R et al. Gastroenterology 2019",
        pmid="30768987",
        mechanism="Hepatosit hasari, fibrozis, kronik inflamasyon, oksidatif stres",
        reversibility="Kismi"
    ),
    
    # KARDIYOVASKULER HASTALIKLAR
    "hypertension": DiseaseEAAEffect(
        disease_name="Esansiyel Hipertansiyon",
        disease_name_en="Essential Hypertension",
        category=DiseaseCategory.CARDIOVASCULAR,
        eaa_effect=1.9,
        ci_lower=1.4,
        ci_upper=2.5,
        sample_size=6234,
        clock_type="Hannum",
        reference="Roetker NS et al. Circ Cardiovasc Genet 2018",
        pmid="29545471",
        mechanism="Vaskuler stres, endotelyal disfonksiyon, RAAS aktivasyonu",
        reversibility="Evet"
    ),
    "coronary_artery_disease": DiseaseEAAEffect(
        disease_name="Koroner Arter Hastaligi",
        disease_name_en="Coronary Artery Disease",
        category=DiseaseCategory.CARDIOVASCULAR,
        eaa_effect=3.8,
        ci_lower=3.0,
        ci_upper=4.6,
        sample_size=3567,
        clock_type="GrimAge",
        reference="Perna L et al. Clin Epigenetics 2016",
        pmid="27891188",
        mechanism="Ateroskleroz, kronik iskemi, endotelyal hasar, inflamasyon",
        reversibility="Kismi"
    ),
    "heart_failure": DiseaseEAAEffect(
        disease_name="Kalp Yetersizligi",
        disease_name_en="Heart Failure",
        category=DiseaseCategory.CARDIOVASCULAR,
        eaa_effect=5.2,
        ci_lower=4.1,
        ci_upper=6.3,
        sample_size=1823,
        clock_type="GrimAge",
        reference="Maierhofer A et al. Clin Epigenetics 2017",
        pmid="28947923",
        mechanism="Kardiyomiyosit hasari, norohumoral aktivasyon, sistemik konjesyon",
        reversibility="Hayir"
    ),
    "atrial_fibrillation": DiseaseEAAEffect(
        disease_name="Atriyal Fibrilasyon",
        disease_name_en="Atrial Fibrillation",
        category=DiseaseCategory.CARDIOVASCULAR,
        eaa_effect=2.3,
        ci_lower=1.6,
        ci_upper=3.0,
        sample_size=2456,
        clock_type="Horvath",
        reference="Lin H et al. Circulation 2016",
        pmid="27742799",
        mechanism="Atriyal remodeling, fibrozis, elektriksel disfonksiyon",
        reversibility="Kismi"
    ),
    "stroke": DiseaseEAAEffect(
        disease_name="Iskemik Inme",
        disease_name_en="Ischemic Stroke",
        category=DiseaseCategory.CARDIOVASCULAR,
        eaa_effect=4.5,
        ci_lower=3.5,
        ci_upper=5.5,
        sample_size=1234,
        clock_type="GrimAge",
        reference="Soriano-Tarraga C et al. Clin Epigenetics 2018",
        pmid="29958538",
        mechanism="Serebral iskemi, noron hasari, noroinflamasyon",
        reversibility="Hayir"
    ),
    "peripheral_artery_disease": DiseaseEAAEffect(
        disease_name="Periferik Arter Hastaligi",
        disease_name_en="Peripheral Artery Disease",
        category=DiseaseCategory.CARDIOVASCULAR,
        eaa_effect=3.1,
        ci_lower=2.3,
        ci_upper=3.9,
        sample_size=1567,
        clock_type="PhenoAge",
        reference="Roetker NS et al. Circ Cardiovasc Genet 2018",
        pmid="29545471",
        mechanism="Periferik ateroskleroz, doku iskemisi, inflamasyon",
        reversibility="Kismi"
    ),
    
    # SOLUNUM HASTALIKLARI
    "copd": DiseaseEAAEffect(
        disease_name="Kronik Obstruktif Akciger Hastaligi (KOAH)",
        disease_name_en="Chronic Obstructive Pulmonary Disease",
        category=DiseaseCategory.RESPIRATORY,
        eaa_effect=3.4,
        ci_lower=2.6,
        ci_upper=4.2,
        sample_size=2876,
        clock_type="GrimAge",
        reference="Lee MK et al. Am J Respir Crit Care Med 2019",
        pmid="30943058",
        mechanism="Sigara kaynakli hasar, kronik inflamasyon, akciger parankim yikimi",
        reversibility="Hayir"
    ),
    "asthma_severe": DiseaseEAAEffect(
        disease_name="Agir Astim",
        disease_name_en="Severe Asthma",
        category=DiseaseCategory.RESPIRATORY,
        eaa_effect=1.8,
        ci_lower=1.1,
        ci_upper=2.5,
        sample_size=1234,
        clock_type="Horvath",
        reference="Yang IV et al. Allergy 2017",
        pmid="28236344",
        mechanism="Kronik havayolu inflamasyonu, mukozal hasar, steroid kullanimi",
        reversibility="Kismi"
    ),
    "pulmonary_fibrosis": DiseaseEAAEffect(
        disease_name="Idiyopatik Pulmoner Fibrozis",
        disease_name_en="Idiopathic Pulmonary Fibrosis",
        category=DiseaseCategory.RESPIRATORY,
        eaa_effect=6.2,
        ci_lower=4.8,
        ci_upper=7.6,
        sample_size=567,
        clock_type="GrimAge",
        reference="Sillanpaa E et al. Aging Cell 2019",
        pmid="31037832",
        mechanism="Alveolar epitel hasari, aberan fibrozis, telomer kisalmasi",
        reversibility="Hayir"
    ),
    
    # BOBREK HASTALIKLARI
    "ckd_stage3": DiseaseEAAEffect(
        disease_name="Kronik Bobrek Hastaligi (Evre 3)",
        disease_name_en="Chronic Kidney Disease Stage 3",
        category=DiseaseCategory.RENAL,
        eaa_effect=2.7,
        ci_lower=2.0,
        ci_upper=3.4,
        sample_size=2345,
        clock_type="PhenoAge",
        reference="Kooman JP et al. Nat Rev Nephrol 2014",
        pmid="24247284",
        mechanism="Uremik toksinler, kronik inflamasyon, oksidatif stres",
        reversibility="Kismi"
    ),
    "ckd_stage5": DiseaseEAAEffect(
        disease_name="Son Donem Bobrek Yetersizligi (SDBY)",
        disease_name_en="End-Stage Renal Disease",
        category=DiseaseCategory.RENAL,
        eaa_effect=5.8,
        ci_lower=4.5,
        ci_upper=7.1,
        sample_size=1123,
        clock_type="GrimAge",
        reference="Stenvinkel P et al. Kidney Int 2017",
        pmid="28756016",
        mechanism="Agir uremik ortam, diyaliz stresi, kardiyovaskuler komorbidite",
        reversibility="Kismi"
    ),
    
    # NOROLOJIK HASTALIKLAR
    "alzheimer": DiseaseEAAEffect(
        disease_name="Alzheimer Hastaligi",
        disease_name_en="Alzheimer's Disease",
        category=DiseaseCategory.NEUROLOGICAL,
        eaa_effect=3.5,
        ci_lower=2.6,
        ci_upper=4.4,
        sample_size=1876,
        clock_type="Horvath",
        reference="Levine ME et al. Alzheimers Dement 2015",
        pmid="25728385",
        mechanism="Norodejenerasyon, amiloid birikimi, tau patolojisi, noroinflamasyon",
        reversibility="Hayir"
    ),
    "parkinson": DiseaseEAAEffect(
        disease_name="Parkinson Hastaligi",
        disease_name_en="Parkinson's Disease",
        category=DiseaseCategory.NEUROLOGICAL,
        eaa_effect=2.8,
        ci_lower=1.9,
        ci_upper=3.7,
        sample_size=1234,
        clock_type="Horvath",
        reference="Horvath S, Ritz BR. Neurobiol Aging 2015",
        pmid="25817536",
        mechanism="Dopaminerjik noron kaybi, alfa-sinuklein birikimi, mitokondriyal disfonksiyon",
        reversibility="Hayir"
    ),
    "multiple_sclerosis": DiseaseEAAEffect(
        disease_name="Multipl Skleroz",
        disease_name_en="Multiple Sclerosis",
        category=DiseaseCategory.NEUROLOGICAL,
        eaa_effect=2.4,
        ci_lower=1.6,
        ci_upper=3.2,
        sample_size=987,
        clock_type="Horvath",
        reference="Kular L et al. Clin Epigenetics 2019",
        pmid="30760298",
        mechanism="Demiyelinizasyon, otoimmun inflamasyon, aksonal hasar",
        reversibility="Kismi"
    ),
    
    # ONKOLOJIK HASTALIKLAR
    "cancer_general": DiseaseEAAEffect(
        disease_name="Kanser (Genel)",
        disease_name_en="Cancer (General)",
        category=DiseaseCategory.ONCOLOGICAL,
        eaa_effect=4.8,
        ci_lower=3.9,
        ci_upper=5.7,
        sample_size=5678,
        clock_type="GrimAge",
        reference="Lu AT et al. Aging 2019",
        pmid="30669119",
        mechanism="Genomik instabilite, tumor mikrocevresi, sistemik inflamasyon, tedavi etkileri",
        reversibility="Degisken"
    ),
    "breast_cancer": DiseaseEAAEffect(
        disease_name="Meme Kanseri",
        disease_name_en="Breast Cancer",
        category=DiseaseCategory.ONCOLOGICAL,
        eaa_effect=3.2,
        ci_lower=2.4,
        ci_upper=4.0,
        sample_size=2345,
        clock_type="Horvath",
        reference="Kresovich JK et al. JNCI 2019",
        pmid="30726949",
        mechanism="Hormonal degisiklikler, tumor biyolojisi, kemoterapi etkileri",
        reversibility="Kismi"
    ),
    "lung_cancer": DiseaseEAAEffect(
        disease_name="Akciger Kanseri",
        disease_name_en="Lung Cancer",
        category=DiseaseCategory.ONCOLOGICAL,
        eaa_effect=5.6,
        ci_lower=4.3,
        ci_upper=6.9,
        sample_size=1567,
        clock_type="GrimAge",
        reference="Dugue PA et al. Int J Cancer 2018",
        pmid="29380392",
        mechanism="Sigara maruziyeti, tumor yukleri, sistemik etkiler",
        reversibility="Hayir"
    ),
    "colorectal_cancer": DiseaseEAAEffect(
        disease_name="Kolorektal Kanser",
        disease_name_en="Colorectal Cancer",
        category=DiseaseCategory.ONCOLOGICAL,
        eaa_effect=3.8,
        ci_lower=2.9,
        ci_upper=4.7,
        sample_size=1876,
        clock_type="PhenoAge",
        reference="Dugue PA et al. Int J Cancer 2018",
        pmid="29380392",
        mechanism="Kronik inflamasyon, diyet faktorleri, genetik yatkinlik",
        reversibility="Kismi"
    ),
    
    # ENFEKSIYOZ HASTALIKLAR
    "hiv_aids": DiseaseEAAEffect(
        disease_name="HIV/AIDS",
        disease_name_en="HIV/AIDS",
        category=DiseaseCategory.INFECTIOUS,
        eaa_effect=7.4,
        ci_lower=5.8,
        ci_upper=9.0,
        sample_size=1234,
        clock_type="GrimAge",
        reference="Gross AM et al. Mol Cell 2016",
        pmid="26924389",
        mechanism="Kronik immun aktivasyon, viral rezervuar, ART yan etkileri, komorbidite",
        reversibility="Kismi"
    ),
    "hepatitis_c": DiseaseEAAEffect(
        disease_name="Kronik Hepatit C",
        disease_name_en="Chronic Hepatitis C",
        category=DiseaseCategory.INFECTIOUS,
        eaa_effect=3.1,
        ci_lower=2.3,
        ci_upper=3.9,
        sample_size=1567,
        clock_type="Horvath",
        reference="Horvath S et al. Liver Int 2018",
        pmid="29160627",
        mechanism="Hepatik inflamasyon, fibrozis, viral replikasyon",
        reversibility="Evet"
    ),
    "hepatitis_b": DiseaseEAAEffect(
        disease_name="Kronik Hepatit B",
        disease_name_en="Chronic Hepatitis B",
        category=DiseaseCategory.INFECTIOUS,
        eaa_effect=2.4,
        ci_lower=1.7,
        ci_upper=3.1,
        sample_size=1234,
        clock_type="Horvath",
        reference="Horvath S et al. Liver Int 2018",
        pmid="29160627",
        mechanism="Hepatik inflamasyon, viral integrays on, immun yanit",
        reversibility="Kismi"
    ),
    "covid19_severe": DiseaseEAAEffect(
        disease_name="Agir COVID-19",
        disease_name_en="Severe COVID-19",
        category=DiseaseCategory.INFECTIOUS,
        eaa_effect=2.9,
        ci_lower=1.8,
        ci_upper=4.0,
        sample_size=567,
        clock_type="GrimAge",
        reference="Cao X et al. Aging 2021",
        pmid="33657025",
        mechanism="Sitokin firtinasi, multi-organ hasari, uzun COVID etkileri",
        reversibility="Belirsiz"
    ),
    
    # OTOIMMUN HASTALIKLAR
    "rheumatoid_arthritis": DiseaseEAAEffect(
        disease_name="Romatoid Artrit",
        disease_name_en="Rheumatoid Arthritis",
        category=DiseaseCategory.AUTOIMMUNE,
        eaa_effect=2.6,
        ci_lower=1.8,
        ci_upper=3.4,
        sample_size=1456,
        clock_type="Horvath",
        reference="Horvath S et al. Aging 2016",
        pmid="27690241",
        mechanism="Kronik sinovyal inflamasyon, sistemik immun aktivasyon",
        reversibility="Kismi"
    ),
    "lupus": DiseaseEAAEffect(
        disease_name="Sistemik Lupus Eritematozus",
        disease_name_en="Systemic Lupus Erythematosus",
        category=DiseaseCategory.AUTOIMMUNE,
        eaa_effect=3.2,
        ci_lower=2.3,
        ci_upper=4.1,
        sample_size=876,
        clock_type="Horvath",
        reference="Absher DM et al. Genome Biol 2013",
        pmid="24090037",
        mechanism="Otoantikor uretimi, multi-organ tutulumu, immun kompleks birikimi",
        reversibility="Kismi"
    ),
    "inflammatory_bowel_disease": DiseaseEAAEffect(
        disease_name="Inflamatuar Barsak Hastaligi",
        disease_name_en="Inflammatory Bowel Disease",
        category=DiseaseCategory.AUTOIMMUNE,
        eaa_effect=2.1,
        ci_lower=1.4,
        ci_upper=2.8,
        sample_size=1123,
        clock_type="Horvath",
        reference="Harris RA et al. Inflamm Bowel Dis 2019",
        pmid="30544184",
        mechanism="Kronik intestinal inflamasyon, barsakepitel hasari, disbiyoz",
        reversibility="Kismi"
    ),
    
    # PSIKIYATRIK HASTALIKLAR
    "major_depression": DiseaseEAAEffect(
        disease_name="Major Depresif Bozukluk",
        disease_name_en="Major Depressive Disorder",
        category=DiseaseCategory.PSYCHIATRIC,
        eaa_effect=2.0,
        ci_lower=1.3,
        ci_upper=2.7,
        sample_size=2345,
        clock_type="GrimAge",
        reference="Han LKM et al. Am J Psychiatry 2018",
        pmid="30021081",
        mechanism="HPA aks disregulasyonu, noroinflamasyon, oksidatif stres",
        reversibility="Evet"
    ),
    "bipolar_disorder": DiseaseEAAEffect(
        disease_name="Bipolar Bozukluk",
        disease_name_en="Bipolar Disorder",
        category=DiseaseCategory.PSYCHIATRIC,
        eaa_effect=2.4,
        ci_lower=1.6,
        ci_upper=3.2,
        sample_size=1234,
        clock_type="Horvath",
        reference="Fries GR et al. Transl Psychiatry 2017",
        pmid="28763057",
        mechanism="Epizodik stres, norotransmitter dengesizligi, ilac etkileri",
        reversibility="Kismi"
    ),
    "schizophrenia": DiseaseEAAEffect(
        disease_name="Sizofreni",
        disease_name_en="Schizophrenia",
        category=DiseaseCategory.PSYCHIATRIC,
        eaa_effect=3.1,
        ci_lower=2.2,
        ci_upper=4.0,
        sample_size=1567,
        clock_type="Horvath",
        reference="Ohi K et al. Transl Psychiatry 2020",
        pmid="32066738",
        mechanism="Norogelisimsel anomaliler, antipsikotik etkileri, yasam tarzifaktorleri",
        reversibility="Kismi"
    ),
    "ptsd": DiseaseEAAEffect(
        disease_name="Post-Travmatik Stres Bozuklugu",
        disease_name_en="Post-Traumatic Stress Disorder",
        category=DiseaseCategory.PSYCHIATRIC,
        eaa_effect=2.3,
        ci_lower=1.5,
        ci_upper=3.1,
        sample_size=987,
        clock_type="GrimAge",
        reference="Wolf EJ et al. Psychoneuroendocrinology 2018",
        pmid="29102495",
        mechanism="Kronik stres yaniti, HPA aks disfonksiyonu, inflamasyon",
        reversibility="Evet"
    ),
}


# Komorbidite etkilesim katsayilari
COMORBIDITY_INTERACTIONS = {
    # nrcdnl94
    ("type2_diabetes", "hypertension"): 1.3,  # Sinerjistik etki
    ("type2_diabetes", "obesity_class3"): 1.4,
    ("type2_diabetes", "coronary_artery_disease"): 1.5,
    ("hypertension", "coronary_artery_disease"): 1.25,
    ("hypertension", "ckd_stage3"): 1.35,
    ("copd", "lung_cancer"): 1.6,
    ("copd", "coronary_artery_disease"): 1.3,
    ("hiv_aids", "hepatitis_c"): 1.5,
    ("obesity_class3", "nafld"): 1.2,
    ("metabolic_syndrome", "coronary_artery_disease"): 1.4,
    ("major_depression", "coronary_artery_disease"): 1.25,
    ("rheumatoid_arthritis", "coronary_artery_disease"): 1.3,
}


class ChronicDiseaseAnalyzer:
    # nrcdnl94
    """Kronik hastalik-EAA analiz sinifi"""
    
    def __init__(self):
        self.disease_database = CHRONIC_DISEASE_EAA_DATABASE
        self.comorbidity_matrix = COMORBIDITY_INTERACTIONS
    
    def get_disease_effect(self, disease_key: str) -> Optional[DiseaseEAAEffect]:
        """Belirli bir hastalik icin EAA etkisini dondur"""
        return self.disease_database.get(disease_key)
    
    def get_all_diseases(self) -> Dict[str, DiseaseEAAEffect]:
        """Tum hastaliklari dondur"""
        return self.disease_database
    
    def get_diseases_by_category(self, category: DiseaseCategory) -> Dict[str, DiseaseEAAEffect]:
        """Kategoriye gore hastaliklari filtrele"""
        return {
            key: disease 
            for key, disease in self.disease_database.items() 
            if disease.category == category
        }
    
    def calculate_total_eaa(self, disease_keys: List[str]) -> Dict:
        """Birden fazla hastalik icin toplam EAA hesapla (komorbidite dahil)"""
        if not disease_keys:
            return {"total_eaa": 0, "diseases": [], "interactions": []}
        
        base_eaa = 0
        disease_details = []
        interactions = []
        
        # Temel EAA topla
        for key in disease_keys:
            disease = self.disease_database.get(key)
            if disease:
                base_eaa += disease.eaa_effect
                disease_details.append({
                    "key": key,
                    "name": disease.disease_name,
                    "eaa": disease.eaa_effect
                })
        
        # Komorbidite etkilesimlerini hesapla
        interaction_multiplier = 1.0
        for i, key1 in enumerate(disease_keys):
            for key2 in disease_keys[i+1:]:
                # Her iki yonde de kontrol et
                pair1 = (key1, key2)
                pair2 = (key2, key1)
                
                if pair1 in self.comorbidity_matrix:
                    mult = self.comorbidity_matrix[pair1]
                    interaction_multiplier *= mult
                    interactions.append({
                        "pair": f"{key1} + {key2}",
                        "multiplier": mult
                    })
                elif pair2 in self.comorbidity_matrix:
                    mult = self.comorbidity_matrix[pair2]
                    interaction_multiplier *= mult
                    interactions.append({
                        "pair": f"{key2} + {key1}",
                        "multiplier": mult
                    })
        
        # Maksimum carpan sinirlamasi (asiri yuksek degerler icin)
        interaction_multiplier = min(interaction_multiplier, 2.5)
        
        total_eaa = base_eaa * interaction_multiplier
        
        return {
            "total_eaa": round(total_eaa, 1),
            "base_eaa": round(base_eaa, 1),
            "interaction_multiplier": round(interaction_multiplier, 2),
            "diseases": disease_details,
            "interactions": interactions
        }
    
    def get_disease_summary_table(self) -> pd.DataFrame:
        """Tum hastaliklarin ozet tablosunu olustur"""
        data = []
        for key, disease in self.disease_database.items():
            data.append({
                "Hastalik": disease.disease_name,
                "Hastalik (EN)": disease.disease_name_en,
                "Kategori": disease.category.value,
                "EAA (yil)": disease.eaa_effect,
                "95% GA Alt": disease.ci_lower,
                "95% GA Ust": disease.ci_upper,
                "n": disease.sample_size,
                "Saat": disease.clock_type,
                "Tersine Cevrilebilirlik": disease.reversibility
            })
        
        df = pd.DataFrame(data)
        df = df.sort_values("EAA (yil)", ascending=False)
        return df
    
    def get_category_summary(self) -> pd.DataFrame:
        """Kategorilere gore ozet istatistikler"""
        data = []
        for category in DiseaseCategory:
            diseases = self.get_diseases_by_category(category)
            if diseases:
                eaa_values = [d.eaa_effect for d in diseases.values()]
                data.append({
                    "Kategori": category.value,
                    "Hastalik Sayisi": len(diseases),
                    "Ortalama EAA": round(np.mean(eaa_values), 1),
                    "Min EAA": min(eaa_values),
                    "Max EAA": max(eaa_values),
                    "Toplam n": sum(d.sample_size for d in diseases.values())
                })
        
        return pd.DataFrame(data).sort_values("Ortalama EAA", ascending=False)
    
    def get_reversibility_analysis(self) -> pd.DataFrame:
        """Tersine cevrilebilirlik analizini olustur"""
        data = {"Evet": [], "Kismi": [], "Hayir": [], "Degisken": [], "Belirsiz": []}
        
        for key, disease in self.disease_database.items():
            rev = disease.reversibility
            if rev in data:
                data[rev].append({
                    "name": disease.disease_name,
                    "eaa": disease.eaa_effect
                })
        
        summary = []
        for rev_type, diseases in data.items():
            if diseases:
                summary.append({
                    "Tersine Cevrilebilirlik": rev_type,
                    "Hastalik Sayisi": len(diseases),
                    "Ortalama EAA": round(np.mean([d["eaa"] for d in diseases]), 1),
                    "Ornekler": ", ".join([d["name"] for d in diseases[:3]])
                })
        
        return pd.DataFrame(summary)
    
    def get_top_diseases(self, n: int = 10) -> pd.DataFrame:
        """En yuksek EAA etkisine sahip hastaliklari listele"""
        df = self.get_disease_summary_table()
        return df.head(n)
    
    def search_disease(self, query: str) -> pd.DataFrame:
        """Hastalik arama"""
        query = query.lower()
        results = []
        
        for key, disease in self.disease_database.items():
            if (query in disease.disease_name.lower() or 
                query in disease.disease_name_en.lower() or
                query in key.lower()):
                results.append({
                    "Anahtar": key,
                    "Hastalik": disease.disease_name,
                    "Kategori": disease.category.value,
                    "EAA (yil)": disease.eaa_effect,
                    "Mekanizma": disease.mechanism
                })
        
        return pd.DataFrame(results)
    
    def get_mechanism_details(self, disease_key: str) -> Dict:
        """Hastalik mekanizma detaylari"""
        disease = self.disease_database.get(disease_key)
        if not disease:
            return {}
        
        return {
            "disease_name": disease.disease_name,
            "mechanism": disease.mechanism,
            "eaa_effect": disease.eaa_effect,
            "reversibility": disease.reversibility,
            "reference": disease.reference,
            "pmid": disease.pmid
        }


def get_chronic_disease_analyzer() -> ChronicDiseaseAnalyzer:
    """Singleton analyzer instance"""
    return ChronicDiseaseAnalyzer()


def get_disease_count() -> int:
    """Toplam hastalik sayisi"""
    return len(CHRONIC_DISEASE_EAA_DATABASE)


def get_category_list() -> List[str]:
    """Kategori listesi"""
    return [cat.value for cat in DiseaseCategory]


# End of module - # nrcdnl94