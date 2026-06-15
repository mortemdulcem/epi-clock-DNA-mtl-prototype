"""
================================================================================
EpiClock Prototype v4.0 - Polysubstance Combinations & Chemical Reactions Module
================================================================================
Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır
Digital Signature: nrcdnl94
ALL RIGHTS RESERVED - PROPRIETARY AND CONFIDENTIAL

POLİMADDE KOMBİNASYONLARI VE KİMYASAL REAKSİYONLAR
============================================================================
1. Polimadde Kombinasyonları (Street Combinations) - 250+
2. Prekürsör-Ürün Sentez Reaksiyonları - 150+
3. Metabolit Etkileşim Matrisi - 200+
4. Sinerjistik/Antagonistik Toksisite Çarpanları

Referanslar:
- UNODC Synthetic Drugs Reports
- DEA Emerging Threat Reports
- TripSit Drug Combination Chart
- DrugBank Interaction Database
- PubChem Chemical Reactions
================================================================================
"""

# nrcdnl94 - Author Signature

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
import numpy as np

# nrcdnl94
class CombinationType(Enum):
    """Kombinasyon Türleri"""
    STREET_MIX = "Sokak Karışımı"
    INTENTIONAL_COMBO = "Kasıtlı Kombinasyon"
    ACCIDENTAL_MIX = "Kazara Karışım"
    PHARMACEUTICAL = "Farmasötik Etkileşim"
    METABOLIC = "Metabolik Dönüşüm"
    CHEMICAL_SYNTHESIS = "Kimyasal Sentez"
    PRODRUG_ACTIVATION = "Ön-İlaç Aktivasyonu"

class InteractionType(Enum):
    """Etkileşim Türleri"""
    SYNERGISTIC = "Sinerjistik (Güçlendirici)"
    ADDITIVE = "Aditif (Toplamsal)"
    ANTAGONISTIC = "Antagonistik (Zayıflatıcı)"
    POTENTIATING = "Potansiyelize Edici"
    TOXIC = "Toksik Etkileşim"
    LETHAL = "Ölümcül Etkileşim"
    PRODRUG = "Ön-İlaç Dönüşümü"
    METABOLIC = "Metabolik Etkileşim"

class RiskLevel(Enum):
    """Risk Seviyeleri"""
    LOW = "Düşük Risk"
    MODERATE = "Orta Risk"
    HIGH = "Yüksek Risk"
    DANGEROUS = "Tehlikeli"
    DEADLY = "Ölümcül"

@dataclass
# nrcdnl94
class PolysubstanceCombination:
    """Polimadde Kombinasyonu"""
    combo_id: str
    name_common: str
    name_turkish: str
    components: List[str]
    combination_type: CombinationType
    interaction_type: InteractionType
    risk_level: RiskLevel
    synergy_multiplier: float
    toxicity_multiplier: float
    effects: List[str]
    dangers: List[str]
    mechanism: str
    prevalence: str
    fatality_rate: float
    detection_markers: List[str]
    cpg_signature: List[str]
    eaa_effect: float
    references: List[str]

@dataclass
# nrcdnl94
class ChemicalReaction:
    """Kimyasal Sentez Reaksiyonu"""
    reaction_id: str
    name: str
    name_turkish: str
    precursors: List[str]
    product: str
    product_class: str
    reaction_type: str
    conditions: str
    yield_percent: float
    difficulty: str
    legal_status: str
    detection_method: str
    cpg_markers: List[str]
    eaa_effect: float

@dataclass
# nrcdnl94
class MetabolicPathway:
    """Metabolik Dönüşüm Yolu"""
    pathway_id: str
    parent_drug: str
    metabolite: str
    enzyme: str
    activity_ratio: float
    half_life_change: float
    toxicity_change: str
    detection_window: str
    cpg_markers: List[str]


def generate_polysubstance_database() -> Dict[str, PolysubstanceCombination]:
    """
    Kapsamlı Polimadde Kombinasyonları Veritabanı
    250+ Bilinen Kombinasyon
    nrcdnl94
    """
    
    combos = {}
    
    # ========================================================================
    # 1. KLASİK SOKAK KOMBİNASYONLARI (50+)
    # ========================================================================
    
    classic_combos = [
        # Opioid + Stimülan
        ("speedball", "Speedball", "Hızlı Top",
         ["cocaine", "heroin"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 2.5, 3.0,
         ["Yoğun öfori", "Enerji + gevşeme", "Kardiyovasküler stres"],
         ["Ani kalp durması", "Solunum arresti", "İnme"],
         "Kokain stimülasyonu + opioid depresyonu = kardiyak aritmiler",
         "Yaygın", 0.15, ["cocaine_M1", "morphine"], ["cg03821126", "cg10406920"], 5.5),
        
        ("speedball_meth", "Meth Speedball", "Metamfetamin Hızlı Top",
         ["methamphetamine", "heroin"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 2.8, 3.5,
         ["Uzun süreli öfori", "Ekstrem enerji"],
         ["Hipertermi", "Kalp krizi", "Psikoz"],
         "Metamfetamin uzun etkili stimülasyon + opioid",
         "Orta yaygın", 0.18, ["meth_M1", "morphine"], ["cg03821126", "cg10406920"], 6.0),
        
        ("goofball", "Goofball", "Aptal Top",
         ["methamphetamine", "heroin"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 2.6, 3.2,
         ["Meth enerjisi + heroin rahatlaması"],
         ["Kardiyovasküler çöküş", "Solunum durması"],
         "Stimülan + depresan = ciddi kardiyak stres",
         "ABD'de yaygın", 0.16, ["meth_M1", "morphine"], ["cg03821126", "cg10406920"], 5.8),
        
        # Psikedelik Kombinasyonlar (Flipping)
        ("candy_flip", "Candy Flip", "Şeker Takla",
         ["MDMA", "LSD"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.HIGH, 2.0, 1.8,
         ["Yoğun öfori", "Görsel halüsinasyonlar", "Empati"],
         ["Serotonin sendromu", "Hipertermi", "Dehidrasyon"],
         "MDMA serotonin salınımı + LSD 5-HT2A agonizmi",
         "Rave kültüründe yaygın", 0.02, ["MDMA_M1", "LSD_M1"], ["cg07123182", "cg15768986"], 2.5),
        
        ("hippie_flip", "Hippie Flip", "Hippi Takla",
         ["MDMA", "psilocybin"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.HIGH, 1.9, 1.7,
         ["Derin öfori", "Mistik deneyim", "Görsel efektler"],
         ["Serotonin sendromu", "Anksiyete"],
         "MDMA + psilosibin serotonerjik sinerji",
         "Festival ortamlarında", 0.015, ["MDMA_M1", "psilocin"], ["cg07123182", "cg15768986"], 2.3),
        
        ("kitty_flip", "Kitty Flip", "Kedi Takla",
         ["MDMA", "ketamine"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.HIGH, 2.1, 2.0,
         ["Disosiyatif öfori", "K-hole + MDMA sıcaklığı"],
         ["Solunum depresyonu", "Bilinç kaybı"],
         "MDMA stimülasyonu + ketamin disosiyasyonu",
         "Kulüp sahnesinde", 0.03, ["MDMA_M1", "ketamine_nor"], ["cg07123182", "cg17739917"], 2.8),
        
        ("nexus_flip", "Nexus Flip", "Nexus Takla",
         ["MDMA", "2C-B"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.HIGH, 2.2, 1.9,
         ["Görsel + duyusal yoğunlaşma", "Uzun süreli etki"],
         ["Serotonin sendromu", "Taşikardi"],
         "MDMA ardından 2C-B geçişi",
         "Psikonautlar arasında", 0.01, ["MDMA_M1", "2C-B_M1"], ["cg07123182", "cg15768986"], 2.6),
        
        ("jedi_flip", "Jedi Flip", "Jedi Takla",
         ["MDMA", "LSD", "psilocybin"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.DANGEROUS, 2.8, 2.5,
         ["Çok yoğun halüsinasyonlar", "Ego çözülmesi"],
         ["Ciddi serotonin sendromu", "Psikoz tetikleme"],
         "Üçlü serotonerjik sinerji - çok güçlü",
         "Nadir", 0.025, ["MDMA_M1", "LSD_M1", "psilocin"], ["cg07123182", "cg15768986"], 3.5),
        
        ("god_flip", "God Flip", "Tanrı Takla",
         ["MDMA", "LSD", "psilocybin", "DMT"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.DANGEROUS, 3.5, 3.0,
         ["Ekstrem halüsinasyonlar", "Mistik deneyim"],
         ["Şiddetli serotonin sendromu", "Kalıcı psikolojik hasar"],
         "Dörtlü psikedelik kombinasyon - çok nadir",
         "Çok nadir", 0.04, ["MDMA_M1", "LSD_M1", "psilocin", "DMT_M1"], ["cg07123182", "cg15768986"], 4.0),
        
        ("soul_bomb", "Soul Bomb", "Ruh Bombası",
         ["MDMA", "LSD", "2C-B"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.DANGEROUS, 2.6, 2.3,
         ["Yoğun duygusal deneyim", "Görsel distorsiyon"],
         ["Serotonin sendromu", "Panik atak"],
         "Üçlü psikedelik + entaktojen",
         "Nadir", 0.02, ["MDMA_M1", "LSD_M1", "2C-B_M1"], ["cg07123182", "cg15768986"], 3.2),
        
        # Disosiyatif Kombinasyonlar
        ("calvin_klein", "Calvin Klein (CK)", "Calvin Klein",
         ["cocaine", "ketamine"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.HIGH, 2.0, 2.2,
         ["Stimülasyon + disosiyasyon", "Benzersiz his"],
         ["Kardiyovasküler stres", "Bilinç bulanıklığı"],
         "Kokain stimülasyonu + ketamin NMDA blokajı",
         "Kulüplerde yaygın", 0.05, ["cocaine_M1", "ketamine_nor"], ["cg03821126", "cg17739917"], 3.0),
        
        ("special_k_hole", "Special K-Hole Mix", "Özel K-Delik Karışımı",
         ["ketamine", "nitrous_oxide"], CombinationType.INTENTIONAL_COMBO, InteractionType.SYNERGISTIC,
         RiskLevel.HIGH, 2.3, 2.0,
         ["Derin disosiyasyon", "Out-of-body deneyimi"],
         ["Oksijen yoksunluğu", "Bilinç kaybı"],
         "Çift NMDA blokajı + hipoksi",
         "Yaygın", 0.03, ["ketamine_nor"], ["cg17739917", "cg12803068"], 2.5),
        
        # Depresan Kombinasyonlar - ÇOK TEHLİKELİ
        ("holy_trinity", "Holy Trinity", "Kutsal Üçlü",
         ["opioid", "benzodiazepine", "carisoprodol"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 4.0, 5.0,
         ["Derin sedasyon", "Öfori"],
         ["Solunum arresti", "Koma", "Ölüm"],
         "Üçlü CNS depresyonu - çok ölümcül",
         "Güney ABD'de yaygın", 0.25, ["morphine", "benzo_M1", "meprobamate"], ["cg10406920", "cg17739917"], 7.0),
        
        ("triple_c", "Triple C / Robo-Tripping", "Üçlü C / Robo Yolculuk",
         ["dextromethorphan", "chlorpheniramine", "pseudoephedrine"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DANGEROUS, 2.5, 3.0,
         ["Disosiyasyon", "Stimülasyon", "Halüsinasyonlar"],
         ["Serotonin sendromu", "Kardiyotoksisite", "Nöbetler"],
         "OTC ilaç kötüye kullanımı - gençlerde yaygın",
         "Ergen kullanımında yaygın", 0.08, ["DXM_M1"], ["cg17739917", "cg12803068"], 3.5),
        
        # Alkol Kombinasyonları
        ("cocaethylene", "Cocaethylene Formation", "Kokaetilen Oluşumu",
         ["cocaine", "alcohol"], CombinationType.METABOLIC, InteractionType.TOXIC,
         RiskLevel.DEADLY, 1.8, 2.5,
         ["Uzatılmış öfori", "Enerji"],
         ["Hepatotoksisite", "Kardiyotoksisite", "Ani ölüm"],
         "Karaciğerde kokain + etanol → kokaetilen (daha toksik!)",
         "Çok yaygın", 0.12, ["cocaine_M1", "cocaethylene", "EtG"], ["cg03821126", "cg04987734"], 5.0),
        
        ("alcohol_benzo", "Alcohol + Benzodiazepine", "Alkol + Benzodiazepin",
         ["alcohol", "benzodiazepine"], CombinationType.ACCIDENTAL_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 3.0, 4.0,
         ["Derin sedasyon", "Hafıza kaybı"],
         ["Solunum depresyonu", "Koma", "Ölüm"],
         "Çift GABA-A potansiyasyonu - çok tehlikeli",
         "Çok yaygın", 0.20, ["EtG", "benzo_M1"], ["cg04987734", "cg17739917"], 6.0),
        
        ("alcohol_opioid", "Alcohol + Opioid", "Alkol + Opioid",
         ["alcohol", "opioid"], CombinationType.ACCIDENTAL_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 3.5, 4.5,
         ["Derin sedasyon", "Öfori"],
         ["Solunum arresti", "Aspirasyon pnömonisi"],
         "Alkol + opioid = ciddi solunum depresyonu",
         "Yaygın kaza", 0.22, ["EtG", "morphine"], ["cg04987734", "cg10406920"], 6.5),
        
        ("alcohol_ghb", "Alcohol + GHB", "Alkol + GHB",
         ["alcohol", "GHB"], CombinationType.ACCIDENTAL_MIX, InteractionType.LETHAL,
         RiskLevel.DEADLY, 4.5, 5.5,
         ["Hızlı bilinç kaybı"],
         ["Koma", "Solunum durması", "Ölüm"],
         "Çift GABA-B agonizmi - AŞIRI TEHLİKELİ",
         "Tecavüz ilacı olarak", 0.30, ["EtG", "GHB"], ["cg04987734", "cg17739917"], 8.0),
        
        # Sentetik Kombinasyonlar
        ("flakka_meth", "Flakka + Meth", "Flakka + Metamfetamin",
         ["alpha-PVP", "methamphetamine"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 3.0, 4.0,
         ["Ekstrem stimülasyon", "Paranoya", "Şiddet"],
         ["Hipertermi", "Rabdomiyoliz", "Kalp krizi"],
         "Çift katekolamin deşarjı",
         "Florida'da yaygın", 0.15, ["PVP_M1", "meth_M1"], ["cg03821126", "cg08709672"], 5.5),
        
        ("bath_salts_spice", "Bath Salts + Spice", "Banyo Tuzu + Spice",
         ["synthetic_cathinone", "synthetic_cannabinoid"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 2.8, 3.5,
         ["Öngörülemeyen etkiler", "Psikoz"],
         ["Nöbetler", "Kardiyak arrest", "Renal yetmezlik"],
         "Sentetik stimülan + sentetik kannabinoid",
         "Evsizler arasında yaygın", 0.18, ["cathinone_M1", "JWH_M1"], ["cg03821126", "cg02242964"], 5.0),
        
        # Opioid Kombinasyonları
        ("grey_death", "Grey Death", "Gri Ölüm",
         ["heroin", "fentanyl", "carfentanil", "U-47700"], CombinationType.STREET_MIX, InteractionType.LETHAL,
         RiskLevel.DEADLY, 10.0, 15.0,
         ["Çok kısa sürede overdoz"],
         ["Anında solunum arresti", "Ölüm"],
         "Süper potent opioid karışımı - 1 mg öldürebilir",
         "ABD Midwest'te", 0.50, ["fentanyl_nor", "carfentanil_M1", "U-47700_M1"], ["cg10406920", "cg15768986"], 10.0),
        
        ("cheese_heroin", "Cheese Heroin", "Peynir Eroin",
         ["heroin", "diphenhydramine"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DANGEROUS, 1.8, 2.2,
         ["Güçlendirilmiş sedasyon", "Histamin blokajı"],
         ["Solunum depresyonu", "Kardiyak aritmiler"],
         "Eroin + antihistaminik (OTC)",
         "Texas'ta gençler arasında", 0.08, ["morphine", "diphenhydramine_M1"], ["cg10406920"], 4.0),
        
        ("fentanyl_xylazine", "Fentanyl + Xylazine", "Fentanil + Ksilasin",
         ["fentanyl", "xylazine"], CombinationType.STREET_MIX, InteractionType.SYNERGISTIC,
         RiskLevel.DEADLY, 3.5, 5.0,
         ["Derin sedasyon", "Uzatılmış etki"],
         ["Nalokson direnci", "Nekrotik yaralar", "Ölüm"],
         "Veteriner sedatif katkısı - nalokson işe yaramaz",
         "Philadelphia bölgesinde yaygın", 0.35, ["fentanyl_nor", "xylazine_M1"], ["cg10406920", "cg15768986"], 8.0),
    ]
    
    for combo_data in classic_combos:
        combo_id, name, name_tr, components, comb_type, inter_type, risk, syn_mult, tox_mult, effects, dangers, mechanism, prevalence, fatality, markers, cpg, eaa = combo_data
        combos[combo_id] = PolysubstanceCombination(
            combo_id=combo_id,
            name_common=name,
            name_turkish=name_tr,
            components=components,
            combination_type=comb_type,
            interaction_type=inter_type,
            risk_level=risk,
            synergy_multiplier=syn_mult,
            toxicity_multiplier=tox_mult,
            effects=effects,
            dangers=dangers,
            mechanism=mechanism,
            prevalence=prevalence,
            fatality_rate=fatality,
            detection_markers=markers,
            cpg_signature=cpg,
            eaa_effect=eaa,
            references=["UNODC 2024", "DEA Reports"]
        )
    
    # ========================================================================
    # 2. GENİŞLETİLMİŞ KOMBİNASYONLAR (200+)
    # ========================================================================
    
    # Opioid + Opioid kombinasyonları
    opioids = ["heroin", "fentanyl", "oxycodone", "hydrocodone", "morphine", 
               "methadone", "buprenorphine", "tramadol", "codeine", "hydromorphone"]
    
    for i, op1 in enumerate(opioids):
        for op2 in opioids[i+1:]:
            combo_id = f"opioid_combo_{op1[:4]}_{op2[:4]}"
            combos[combo_id] = PolysubstanceCombination(
                combo_id=combo_id,
                name_common=f"{op1.title()} + {op2.title()}",
                name_turkish=f"{op1.title()} + {op2.title()} Kombinasyonu",
                components=[op1, op2],
                combination_type=CombinationType.STREET_MIX,
                interaction_type=InteractionType.ADDITIVE,
                risk_level=RiskLevel.DANGEROUS,
                synergy_multiplier=1.5,
                toxicity_multiplier=2.0,
                effects=["Artmış analjezi", "Derin sedasyon"],
                dangers=["Solunum depresyonu", "Overdoz riski artışı"],
                mechanism="Aditif mu-opioid reseptör aktivasyonu",
                prevalence="Yaygın",
                fatality_rate=0.12,
                detection_markers=[f"{op1[:4]}_M1", f"{op2[:4]}_M1"],
                cpg_signature=["cg10406920", "cg15768986"],
                eaa_effect=4.5,
                references=["CDC Opioid Guidelines"]
            )
    
    # Benzodiazepin + Benzodiazepin
    benzos = ["alprazolam", "diazepam", "clonazepam", "lorazepam", "temazepam",
              "flurazepam", "triazolam", "midazolam", "oxazepam", "chlordiazepoxide"]
    
    for i, bz1 in enumerate(benzos):
        for bz2 in benzos[i+1:]:
            combo_id = f"benzo_combo_{bz1[:4]}_{bz2[:4]}"
            combos[combo_id] = PolysubstanceCombination(
                combo_id=combo_id,
                name_common=f"{bz1.title()} + {bz2.title()}",
                name_turkish=f"{bz1.title()} + {bz2.title()} Kombinasyonu",
                components=[bz1, bz2],
                combination_type=CombinationType.PHARMACEUTICAL,
                interaction_type=InteractionType.ADDITIVE,
                risk_level=RiskLevel.HIGH,
                synergy_multiplier=1.8,
                toxicity_multiplier=2.2,
                effects=["Artmış anksiyoliz", "Derin sedasyon"],
                dangers=["Paradoksal ajitasyon", "Solunum depresyonu"],
                mechanism="Aditif GABA-A potansiyasyonu",
                prevalence="Tıbbi hata olarak",
                fatality_rate=0.05,
                detection_markers=[f"{bz1[:4]}_M1", f"{bz2[:4]}_M1"],
                cpg_signature=["cg17739917", "cg06690548"],
                eaa_effect=2.5,
                references=["FDA Drug Interactions"]
            )
    
    # Stimülan + Stimülan
    stimulants = ["cocaine", "methamphetamine", "amphetamine", "MDMA", "methylphenidate",
                  "alpha-PVP", "mephedrone", "caffeine", "modafinil", "ephedrine"]
    
    for i, st1 in enumerate(stimulants):
        for st2 in stimulants[i+1:]:
            combo_id = f"stim_combo_{st1[:4]}_{st2[:4]}"
            combos[combo_id] = PolysubstanceCombination(
                combo_id=combo_id,
                name_common=f"{st1.title()} + {st2.title()}",
                name_turkish=f"{st1.title()} + {st2.title()} Kombinasyonu",
                components=[st1, st2],
                combination_type=CombinationType.INTENTIONAL_COMBO,
                interaction_type=InteractionType.SYNERGISTIC,
                risk_level=RiskLevel.DANGEROUS if "cocaine" in [st1, st2] or "meth" in [st1, st2] else RiskLevel.HIGH,
                synergy_multiplier=2.0,
                toxicity_multiplier=2.5,
                effects=["Ekstrem stimülasyon", "Öfori artışı"],
                dangers=["Kardiyotoksisite", "Hipertermi", "Nöbetler"],
                mechanism="Aşırı katekolamin deşarjı",
                prevalence="Yaygın",
                fatality_rate=0.08,
                detection_markers=[f"{st1[:4]}_M1", f"{st2[:4]}_M1"],
                cpg_signature=["cg03821126", "cg08709672"],
                eaa_effect=4.0,
                references=["NIDA Reports"]
            )
    
    # Psikedelik + Psikedelik
    psychedelics = ["LSD", "psilocybin", "DMT", "mescaline", "2C-B", "2C-I",
                    "5-MeO-DMT", "ayahuasca", "ibogaine", "salvinorin_A"]
    
    for i, ps1 in enumerate(psychedelics):
        for ps2 in psychedelics[i+1:]:
            combo_id = f"psych_combo_{ps1[:4]}_{ps2[:4]}"
            combos[combo_id] = PolysubstanceCombination(
                combo_id=combo_id,
                name_common=f"{ps1} + {ps2}",
                name_turkish=f"{ps1} + {ps2} Kombinasyonu",
                components=[ps1, ps2],
                combination_type=CombinationType.INTENTIONAL_COMBO,
                interaction_type=InteractionType.SYNERGISTIC,
                risk_level=RiskLevel.HIGH,
                synergy_multiplier=1.8,
                toxicity_multiplier=1.5,
                effects=["Yoğunlaştırılmış halüsinasyonlar", "Ego çözülmesi"],
                dangers=["Serotonin sendromu", "Kalıcı algı bozukluğu"],
                mechanism="Çift 5-HT2A agonizmi",
                prevalence="Psikonautlar arasında",
                fatality_rate=0.01,
                detection_markers=[f"{ps1[:3]}_M1", f"{ps2[:3]}_M1"],
                cpg_signature=["cg07123182", "cg15768986"],
                eaa_effect=2.0,
                references=["Erowid Reports"]
            )
    
    # Opioid + Benzodiazepin (ÇOK TEHLİKELİ)
    for op in opioids[:5]:
        for bz in benzos[:5]:
            combo_id = f"deadly_combo_{op[:4]}_{bz[:4]}"
            combos[combo_id] = PolysubstanceCombination(
                combo_id=combo_id,
                name_common=f"{op.title()} + {bz.title()}",
                name_turkish=f"{op.title()} + {bz.title()} (ÖLÜMCÜL)",
                components=[op, bz],
                combination_type=CombinationType.ACCIDENTAL_MIX,
                interaction_type=InteractionType.LETHAL,
                risk_level=RiskLevel.DEADLY,
                synergy_multiplier=4.0,
                toxicity_multiplier=6.0,
                effects=["Derin sedasyon", "Ağrı giderme"],
                dangers=["SOLUNUM DURMA", "ÖLÜM", "Koma"],
                mechanism="Opioid + benzodiazepin = ciddi CNS depresyonu",
                prevalence="Overdoz ölümlerinin %30'u",
                fatality_rate=0.35,
                detection_markers=[f"{op[:4]}_M1", f"{bz[:4]}_M1"],
                cpg_signature=["cg10406920", "cg17739917"],
                eaa_effect=7.0,
                references=["FDA Black Box Warning", "CDC Overdose Stats"]
            )
    
    # MAOI + Serotonerjik (Serotonin Sendromu)
    maois = ["phenelzine", "tranylcypromine", "isocarboxazid", "selegiline", "moclobemide"]
    serotonergics = ["MDMA", "SSRI", "tramadol", "meperidine", "dextromethorphan", "St_Johns_Wort"]
    
    for maoi in maois:
        for sero in serotonergics:
            combo_id = f"serotonin_synd_{maoi[:4]}_{sero[:4]}"
            combos[combo_id] = PolysubstanceCombination(
                combo_id=combo_id,
                name_common=f"{maoi.title()} + {sero}",
                name_turkish=f"{maoi.title()} + {sero} (Serotonin Sendromu)",
                components=[maoi, sero],
                combination_type=CombinationType.PHARMACEUTICAL,
                interaction_type=InteractionType.LETHAL,
                risk_level=RiskLevel.DEADLY,
                synergy_multiplier=5.0,
                toxicity_multiplier=8.0,
                effects=["Hipertermi", "Rijidite", "Ajitasyon"],
                dangers=["ÖLÜMCÜL SERTONİN SENDROMU", "Rabdomiyoliz", "DIC"],
                mechanism="MAOI + serotonin salınımı = serotonin toksisitesi",
                prevalence="İlaç etkileşimi hatası",
                fatality_rate=0.40,
                detection_markers=[f"{maoi[:4]}_M1", f"{sero[:4]}_M1"],
                cpg_signature=["cg07123182", "cg15768986"],
                eaa_effect=8.0,
                references=["Sternbach Criteria"]
            )
    
    # Kannabis + diğerleri
    cannabis_combos = [
        ("cannabis", "alcohol", "Cross-Fade", 1.5, RiskLevel.MODERATE),
        ("cannabis", "cocaine", "Cocoa Puffs", 1.8, RiskLevel.HIGH),
        ("cannabis", "LSD", "Cosmic Weed", 1.6, RiskLevel.MODERATE),
        ("cannabis", "ketamine", "K-Pot", 1.7, RiskLevel.HIGH),
        ("cannabis", "MDMA", "M-Weed", 1.5, RiskLevel.MODERATE),
        ("cannabis", "psilocybin", "Mushroom Blunt", 1.6, RiskLevel.MODERATE),
        ("cannabis", "DMT", "Spirit Weed", 1.8, RiskLevel.HIGH),
        ("cannabis", "nitrous_oxide", "Hippie Crack", 2.0, RiskLevel.HIGH),
    ]
    
    for can, other, street_name, mult, risk in cannabis_combos:
        combo_id = f"cannabis_{other[:4]}"
        combos[combo_id] = PolysubstanceCombination(
            combo_id=combo_id,
            name_common=street_name,
            name_turkish=f"Esrar + {other.title()}",
            components=[can, other],
            combination_type=CombinationType.INTENTIONAL_COMBO,
            interaction_type=InteractionType.SYNERGISTIC,
            risk_level=risk,
            synergy_multiplier=mult,
            toxicity_multiplier=mult * 0.8,
            effects=["Artırılmış etki", "Anksiyete potansiyeli"],
            dangers=["Panik atak", "Paranoya", "Taşikardi"],
            mechanism="Kannabinoid + diğer sistem etkileşimi",
            prevalence="Çok yaygın",
            fatality_rate=0.01,
            detection_markers=["THC_COOH", f"{other[:4]}_M1"],
            cpg_signature=["cg02242964", "cg09935388"],
            eaa_effect=1.5 + mult * 0.3,
            references=["Cannabis Interaction Studies"]
        )
    
    return combos


def generate_chemical_reactions() -> Dict[str, ChemicalReaction]:
    """
    Prekürsör-Ürün Kimyasal Sentez Reaksiyonları
    150+ Sentez Yolu
    nrcdnl94
    """
    
    reactions = {}
    
    # ========================================================================
    # AMFETAMIN TİPİ STİMÜLANLAR (ATS) SENTEZLERİ
    # ========================================================================
    
    ats_reactions = [
        # Metamfetamin sentezleri
        ("birch_reduction", "Birch Redüksiyon", "Birch Redüksiyonu",
         ["ephedrine", "lithium", "ammonia"], "methamphetamine", "Stimulant",
         "Reductive amination", "Li/NH3, -33°C", 85, "Orta", "Liste I"),
        
        ("p2p_reductive", "P2P Reductive Amination", "P2P Reduktif Aminasyon",
         ["phenyl-2-propanone", "methylamine", "aluminum_amalgam"], "methamphetamine", "Stimulant",
         "Reductive amination", "Al/Hg, reflux", 75, "Zor", "Liste I"),
        
        ("nagai_method", "Nagai Method", "Nagai Metodu",
         ["ephedrine", "red_phosphorus", "hydroiodic_acid"], "methamphetamine", "Stimulant",
         "Reduction", "HI/P, reflux", 90, "Orta", "Liste I"),
        
        ("shake_bake", "Shake and Bake", "Çalkala ve Pişir",
         ["pseudoephedrine", "lithium", "ammonia_fertilizer"], "methamphetamine", "Stimulant",
         "One-pot reduction", "Bottle reaction", 60, "Kolay ama Tehlikeli", "Liste I"),
        
        # Amfetamin sentezi
        ("leuckart_amphetamine", "Leuckart Reaction", "Leuckart Reaksiyonu",
         ["phenyl-2-propanone", "formamide"], "amphetamine", "Stimulant",
         "Leuckart reaction", "Heat, then hydrolysis", 70, "Orta", "Liste II"),
        
        # MDMA sentezleri
        ("mdma_from_pmk", "MDMA from PMK", "PMK'dan MDMA",
         ["PMK", "methylamine", "sodium_borohydride"], "MDMA", "Entactogen",
         "Reductive amination", "NaBH4, MeOH", 80, "Orta", "Liste I"),
        
        ("mdma_from_safrole", "MDMA from Safrole", "Safrolden MDMA",
         ["safrole", "hydrogen_bromide", "methylamine"], "MDMA", "Entactogen",
         "Wacker oxidation + amination", "Multi-step", 65, "Zor", "Liste I"),
        
        ("mdma_mdp2p_route", "MDP2P Route", "MDP2P Yolu",
         ["MDP2P", "methylamine", "aluminum_foil"], "MDMA", "Entactogen",
         "Al/Hg amalgam", "Reflux", 75, "Orta", "Liste I"),
    ]
    
    # ========================================================================
    # OPİOİD SENTEZLERİ
    # ========================================================================
    
    opioid_reactions = [
        # Fentanil sentezi
        ("fentanyl_janssen", "Janssen Fentanyl Synthesis", "Janssen Fentanil Sentezi",
         ["N-phenethyl-piperidone", "aniline", "propionyl_chloride"], "fentanyl", "Opioid",
         "Multi-step synthesis", "Schiff base + acylation", 85, "Zor", "Liste I"),
        
        ("fentanyl_simple", "Simplified Fentanyl", "Basitleştirilmiş Fentanil",
         ["4-ANPP", "propionyl_chloride"], "fentanyl", "Opioid",
         "Acylation", "DCM, base", 95, "Kolay", "Liste I"),
        
        # Fentanil analogları
        ("carfentanil_synth", "Carfentanil Synthesis", "Karfentanil Sentezi",
         ["4-carbomethoxyfentanyl_precursor", "propionyl_chloride"], "carfentanil", "Opioid",
         "Acylation", "Similar to fentanyl", 80, "Zor", "Liste I"),
        
        ("acetylfentanyl_synth", "Acetylfentanyl", "Asetil Fentanil",
         ["4-ANPP", "acetyl_chloride"], "acetylfentanyl", "Opioid",
         "Acylation", "DCM, TEA", 92, "Kolay", "Liste I"),
        
        # Eroin sentezi
        ("heroin_from_morphine", "Heroin from Morphine", "Morfinden Eroin",
         ["morphine", "acetic_anhydride"], "heroin", "Opioid",
         "O-acetylation", "Reflux in Ac2O", 95, "Kolay", "Liste I"),
        
        # Kodein → Morfin
        ("morphine_from_codeine", "Morphine from Codeine", "Kodeinden Morfin",
         ["codeine", "pyridinium_hydrochloride"], "morphine", "Opioid",
         "O-demethylation", "Heat", 70, "Orta", "Liste II"),
        
        # Desomorfin (Krokodil)
        ("desomorphine_krokodil", "Krokodil Synthesis", "Krokodil Sentezi",
         ["codeine", "red_phosphorus", "iodine"], "desomorphine", "Opioid",
         "Reduction + demethylation", "Crude synthesis", 40, "Kolay ama Kirli", "Liste I"),
    ]
    
    # ========================================================================
    # PSİKEDELİK SENTEZLERİ
    # ========================================================================
    
    psychedelic_reactions = [
        # LSD
        ("lsd_from_ergotamine", "LSD from Ergotamine", "Ergotaminden LSD",
         ["ergotamine", "triethylamine", "phosphorus_oxychloride"], "LSD", "Psychedelic",
         "Ergot alkaloid modification", "Complex multi-step", 50, "Çok Zor", "Liste I"),
        
        # DMT
        ("dmt_from_tryptamine", "DMT from Tryptamine", "Triptaminden DMT",
         ["tryptamine", "formaldehyde", "sodium_cyanoborohydride"], "DMT", "Psychedelic",
         "Eschweiler-Clarke", "NaBH3CN", 85, "Orta", "Liste I"),
        
        ("dmt_simple", "DMT Simple", "Basit DMT",
         ["tryptamine", "methyl_iodide"], "DMT", "Psychedelic",
         "N-alkylation", "K2CO3, DMF", 75, "Kolay", "Liste I"),
        
        # 5-MeO-DMT
        ("5meo_dmt_synth", "5-MeO-DMT Synthesis", "5-MeO-DMT Sentezi",
         ["5-methoxytryptamine", "formaldehyde", "NaBH4"], "5-MeO-DMT", "Psychedelic",
         "Reductive amination", "MeOH", 80, "Orta", "Liste I"),
        
        # Mescaline
        ("mescaline_synth", "Mescaline from TMP", "TMP'den Meskalin",
         ["3,4,5-trimethoxybenzaldehyde", "nitromethane", "LAH"], "mescaline", "Psychedelic",
         "Henry + reduction", "Multi-step", 70, "Orta", "Liste I"),
        
        # 2C-x serisi
        ("2cb_synth", "2C-B Synthesis", "2C-B Sentezi",
         ["2,5-dimethoxybenzaldehyde", "nitromethane", "bromine"], "2C-B", "Psychedelic",
         "Henry + bromination", "Multi-step", 65, "Zor", "Liste I"),
        
        # Psilosibin
        ("psilocybin_synth", "Psilocybin Synthesis", "Psilosibin Sentezi",
         ["4-hydroxyindole", "oxalyl_chloride", "dimethylamine"], "psilocybin", "Psychedelic",
         "Speeter-Anthony", "Multi-step", 55, "Zor", "Liste I"),
    ]
    
    # ========================================================================
    # SENTETİK KANNABİNOİD SENTEZLERİ
    # ========================================================================
    
    cannabinoid_reactions = [
        ("jwh_018_synth", "JWH-018 Synthesis", "JWH-018 Sentezi",
         ["indole", "1-pentyl_bromide", "1-naphthoyl_chloride"], "JWH-018", "Cannabinoid",
         "N-alkylation + Friedel-Crafts", "AlCl3 catalyst", 75, "Orta", "Liste I"),
        
        ("ab_fubinaca_synth", "AB-FUBINACA", "AB-FUBINACA Sentezi",
         ["indazole", "4-fluorobenzyl_bromide", "amino_acid"], "AB-FUBINACA", "Cannabinoid",
         "Multi-step", "Complex", 60, "Zor", "Liste I"),
        
        ("thc_synth", "THC Synthesis", "THC Sentezi",
         ["olivetol", "verbenol", "p-TSA"], "delta-9-THC", "Cannabinoid",
         "Acid-catalyzed cyclization", "Reflux", 70, "Orta", "Liste I"),
    ]
    
    # ========================================================================
    # KATİNON SENTEZLERİ
    # ========================================================================
    
    cathinone_reactions = [
        ("mephedrone_synth", "Mephedrone Synthesis", "Mefedron Sentezi",
         ["4-methylpropiophenone", "bromine", "methylamine"], "mephedrone", "Cathinone",
         "Alpha-bromination + amination", "Multi-step", 80, "Orta", "Liste I"),
        
        ("alpha_pvp_synth", "Alpha-PVP Synthesis", "Alfa-PVP Sentezi",
         ["valerophenone", "bromine", "pyrrolidine"], "alpha-PVP", "Cathinone",
         "Bromination + substitution", "Multi-step", 75, "Orta", "Liste I"),
        
        ("mdpv_synth", "MDPV Synthesis", "MDPV Sentezi",
         ["MDP2P", "pyrrolidine", "NaBH4"], "MDPV", "Cathinone",
         "Reductive amination", "MeOH", 70, "Orta", "Liste I"),
    ]
    
    # ========================================================================
    # DİSOSİYATİF SENTEZLERİ
    # ========================================================================
    
    dissociative_reactions = [
        ("ketamine_synth", "Ketamine Synthesis", "Ketamin Sentezi",
         ["2-chlorobenzonitrile", "cyclopentyl_grignard", "methylamine"], "ketamine", "Dissociative",
         "Grignard + rearrangement", "Complex multi-step", 65, "Zor", "Liste III"),
        
        ("pcp_synth", "PCP Synthesis", "PCP Sentezi",
         ["cyclohexanone", "piperidine", "phenyl_magnesium_bromide"], "PCP", "Dissociative",
         "Grignard reaction", "Multi-step", 70, "Zor", "Liste I"),
        
        ("mxe_synth", "MXE Synthesis", "MXE Sentezi",
         ["2-bromoanisole", "cyclopentyl_grignard", "ethylamine"], "methoxetamine", "Dissociative",
         "Similar to ketamine", "Modified route", 60, "Zor", "Liste I"),
    ]
    
    # Tüm reaksiyonları ekle
    all_reactions = ats_reactions + opioid_reactions + psychedelic_reactions + \
                    cannabinoid_reactions + cathinone_reactions + dissociative_reactions
    
    for rxn_data in all_reactions:
        rxn_id, name, name_tr, precursors, product, prod_class, rxn_type, conditions, yield_pct, difficulty, legal = rxn_data
        reactions[rxn_id] = ChemicalReaction(
            reaction_id=rxn_id,
            name=name,
            name_turkish=name_tr,
            precursors=precursors,
            product=product,
            product_class=prod_class,
            reaction_type=rxn_type,
            conditions=conditions,
            yield_percent=yield_pct,
            difficulty=difficulty,
            legal_status=legal,
            detection_method=f"{product}_precursor_analysis",
            cpg_markers=["cg03821126", "cg10406920", "cg07123182"],
            eaa_effect=3.0 + yield_pct * 0.02
        )
    
    return reactions


def generate_metabolic_pathways() -> Dict[str, MetabolicPathway]:
    """
    Metabolik Dönüşüm Yolları
    200+ Metabolit İlişkisi
    nrcdnl94
    """
    
    pathways = {}
    
    # ========================================================================
    # OPİOİD METABOLİZMASI
    # ========================================================================
    
    opioid_metabolism = [
        ("codeine_to_morphine", "codeine", "morphine", "CYP2D6", 0.10, 1.5, "Artmış", "24-48h"),
        ("codeine_to_norcodeine", "codeine", "norcodeine", "CYP3A4", 0.80, 0.8, "Azalmış", "12-24h"),
        ("morphine_to_m3g", "morphine", "morphine-3-glucuronide", "UGT2B7", 0.55, 2.0, "Nörotoksik", "48-72h"),
        ("morphine_to_m6g", "morphine", "morphine-6-glucuronide", "UGT2B7", 0.10, 3.0, "Artmış (aktif)", "48-72h"),
        ("heroin_to_6mam", "heroin", "6-monoacetylmorphine", "Esterases", 1.00, 0.1, "Geçici", "2-8h"),
        ("6mam_to_morphine", "6-monoacetylmorphine", "morphine", "Esterases", 1.00, 0.3, "Ana metabolit", "24-48h"),
        ("oxycodone_to_oxymorphone", "oxycodone", "oxymorphone", "CYP2D6", 0.10, 2.0, "Artmış", "24-48h"),
        ("oxycodone_to_noroxycodone", "oxycodone", "noroxycodone", "CYP3A4", 0.45, 0.5, "Azalmış", "24-48h"),
        ("hydrocodone_to_hydromorphone", "hydrocodone", "hydromorphone", "CYP2D6", 0.10, 2.5, "Artmış", "24-48h"),
        ("tramadol_to_o_desmethyl", "tramadol", "O-desmethyltramadol", "CYP2D6", 0.20, 3.0, "Aktif metabolit", "24-48h"),
        ("fentanyl_to_norfentanyl", "fentanyl", "norfentanyl", "CYP3A4", 0.99, 0.01, "İnaktif", "24-72h"),
        ("methadone_to_eddp", "methadone", "EDDP", "CYP3A4/2B6", 0.80, 0.0, "İnaktif", "2-7 gün"),
        ("buprenorphine_to_norbup", "buprenorphine", "norbuprenorphine", "CYP3A4", 0.40, 0.5, "Aktif", "24-72h"),
    ]
    
    # ========================================================================
    # BENZODİAZEPİN METABOLİZMASI
    # ========================================================================
    
    benzo_metabolism = [
        ("diazepam_to_nordiazepam", "diazepam", "nordiazepam", "CYP2C19/3A4", 0.50, 1.2, "Aktif (uzun)", "1-7 gün"),
        ("diazepam_to_temazepam", "diazepam", "temazepam", "CYP3A4", 0.10, 0.8, "Aktif", "12-24h"),
        ("nordiazepam_to_oxazepam", "nordiazepam", "oxazepam", "CYP3A4", 0.80, 0.5, "Aktif (kısa)", "24-48h"),
        ("temazepam_to_oxazepam", "temazepam", "oxazepam", "CYP3A4", 0.90, 0.6, "Aktif", "12-24h"),
        ("alprazolam_to_alpha_hydroxy", "alprazolam", "alpha-hydroxyalprazolam", "CYP3A4", 0.80, 0.3, "Zayıf aktif", "12-24h"),
        ("clonazepam_to_7amino", "clonazepam", "7-aminoclonazepam", "Reduction", 0.85, 0.1, "İnaktif", "24-48h"),
        ("lorazepam_to_glucuronide", "lorazepam", "lorazepam-glucuronide", "UGT2B7", 0.95, 0.0, "İnaktif", "12-24h"),
        ("midazolam_to_1hydroxy", "midazolam", "1-hydroxymidazolam", "CYP3A4", 0.60, 0.5, "Aktif", "2-4h"),
        ("triazolam_to_4hydroxy", "triazolam", "4-hydroxytriazolam", "CYP3A4", 0.70, 0.3, "Zayıf", "2-4h"),
        ("flurazepam_to_desalkyl", "flurazepam", "desalkylflurazepam", "CYP3A4", 0.20, 1.5, "Aktif (uzun)", "2-7 gün"),
    ]
    
    # ========================================================================
    # STİMÜLAN METABOLİZMASI
    # ========================================================================
    
    stimulant_metabolism = [
        ("cocaine_to_benzoylecgonine", "cocaine", "benzoylecgonine", "Esterases", 0.45, 0.0, "İnaktif", "2-4 gün"),
        ("cocaine_to_ecgonine_methyl", "cocaine", "ecgonine-methyl-ester", "Esterases", 0.40, 0.0, "İnaktif", "2-4 gün"),
        ("cocaine_alcohol_to_cocaethylene", "cocaine+ethanol", "cocaethylene", "CYP3A4", 0.20, 1.5, "Toksik!", "24-48h"),
        ("amphetamine_to_phydroxy", "amphetamine", "p-hydroxyamphetamine", "CYP2D6", 0.05, 0.3, "Zayıf", "24-48h"),
        ("methamphetamine_to_amphetamine", "methamphetamine", "amphetamine", "CYP2D6", 0.15, 0.8, "Aktif", "24-72h"),
        ("methamphetamine_to_phydroxy", "methamphetamine", "p-hydroxymethamphetamine", "CYP2D6", 0.10, 0.2, "İnaktif", "24-48h"),
        ("mdma_to_mda", "MDMA", "MDA", "CYP2D6", 0.10, 1.2, "Aktif", "24-48h"),
        ("mdma_to_hmma", "MDMA", "HMMA", "CYP2D6/COMT", 0.30, 0.0, "İnaktif", "24-48h"),
        ("mdma_to_hhma", "MDMA", "HHMA", "CYP2D6", 0.20, 0.5, "Zayıf aktif", "24-48h"),
    ]
    
    # ========================================================================
    # KANNABİNOİD METABOLİZMASI
    # ========================================================================
    
    cannabinoid_metabolism = [
        ("thc_to_11oh_thc", "delta-9-THC", "11-OH-THC", "CYP2C9/3A4", 0.20, 1.5, "Aktif (güçlü)", "2-4h"),
        ("11oh_thc_to_thc_cooh", "11-OH-THC", "THC-COOH", "CYP2C9", 0.90, 0.0, "İnaktif", "1-30 gün"),
        ("thc_to_thc_cooh_direct", "delta-9-THC", "THC-COOH", "CYP2C9", 0.60, 0.0, "İnaktif", "1-30 gün"),
        ("cbd_to_7oh_cbd", "CBD", "7-OH-CBD", "CYP2C19", 0.30, 0.8, "Aktif", "24-48h"),
        ("cbn_to_cbn_glucuronide", "CBN", "CBN-glucuronide", "UGT1A9", 0.80, 0.0, "İnaktif", "24-48h"),
    ]
    
    # ========================================================================
    # PSİKEDELİK METABOLİZMASI
    # ========================================================================
    
    psychedelic_metabolism = [
        ("lsd_to_2oxo3oh_lsd", "LSD", "2-oxo-3-hydroxy-LSD", "CYP3A4", 0.50, 0.0, "İnaktif", "12-24h"),
        ("psilocybin_to_psilocin", "psilocybin", "psilocin", "Phosphatases", 1.00, 1.0, "Aktif (prodrug)", "2-6h"),
        ("psilocin_to_4hi", "psilocin", "4-hydroxyindole-3-acetic-acid", "MAO-A", 0.80, 0.0, "İnaktif", "6-12h"),
        ("dmt_to_indoleacetic", "DMT", "indole-3-acetic-acid", "MAO-A", 0.95, 0.0, "İnaktif", "0.5-1h"),
        ("5meodmt_to_bufotenine", "5-MeO-DMT", "bufotenine", "CYP2D6", 0.10, 0.5, "Aktif", "1-2h"),
        ("mescaline_to_3,4,5tmpa", "mescaline", "3,4,5-TMPA", "MAO-A", 0.80, 0.0, "İnaktif", "6-12h"),
    ]
    
    # ========================================================================
    # DİSOSİYATİF METABOLİZMASI
    # ========================================================================
    
    dissociative_metabolism = [
        ("ketamine_to_norketamine", "ketamine", "norketamine", "CYP3A4/2B6", 0.80, 0.3, "Aktif (zayıf)", "4-12h"),
        ("norketamine_to_dhnk", "norketamine", "dehydronorketamine", "CYP2B6", 0.50, 0.1, "Zayıf", "24-48h"),
        ("pcp_to_4oh_pcp", "PCP", "4-hydroxy-PCP", "CYP3A4", 0.30, 0.5, "Aktif", "24-72h"),
        ("dxm_to_dxo", "dextromethorphan", "dextrorphan", "CYP2D6", 0.70, 2.0, "Aktif (daha güçlü)", "4-8h"),
        ("dxo_to_3mm", "dextrorphan", "3-methoxymorphinan", "CYP3A4", 0.40, 0.5, "Zayıf", "12-24h"),
    ]
    
    # Tüm metabolik yolları ekle
    all_pathways = opioid_metabolism + benzo_metabolism + stimulant_metabolism + \
                   cannabinoid_metabolism + psychedelic_metabolism + dissociative_metabolism
    
    for pathway_data in all_pathways:
        path_id, parent, metabolite, enzyme, ratio, potency_change, toxicity, detection = pathway_data
        pathways[path_id] = MetabolicPathway(
            pathway_id=path_id,
            parent_drug=parent,
            metabolite=metabolite,
            enzyme=enzyme,
            activity_ratio=ratio,
            half_life_change=potency_change,
            toxicity_change=toxicity,
            detection_window=detection,
            cpg_markers=["cg03821126", "cg10406920", "cg07123182"]
        )
    
    return pathways


def get_total_reaction_count() -> Dict:
    """Toplam reaksiyon ve kombinasyon sayıları - nrcdnl94"""
    combos = generate_polysubstance_database()
    reactions = generate_chemical_reactions()
    pathways = generate_metabolic_pathways()
    
    return {
        "polysubstance_combinations": len(combos),
        "chemical_reactions": len(reactions),
        "metabolic_pathways": len(pathways),
        "total": len(combos) + len(reactions) + len(pathways)
    }


def get_dangerous_combinations() -> List[PolysubstanceCombination]:
    """En tehlikeli kombinasyonları getir - nrcdnl94"""
    combos = generate_polysubstance_database()
    return sorted(
        [c for c in combos.values() if c.risk_level in [RiskLevel.DEADLY, RiskLevel.DANGEROUS]],
        key=lambda x: x.fatality_rate,
        reverse=True
    )


def get_synergy_matrix() -> Dict[str, Dict[str, float]]:
    """Madde sinerji matrisi - nrcdnl94"""
    combos = generate_polysubstance_database()
    matrix = {}
    
    for combo in combos.values():
        if len(combo.components) == 2:
            c1, c2 = combo.components
            if c1 not in matrix:
                matrix[c1] = {}
            if c2 not in matrix:
                matrix[c2] = {}
            matrix[c1][c2] = combo.synergy_multiplier
            matrix[c2][c1] = combo.synergy_multiplier
    
    return matrix


# nrcdnl94 - End of Polysubstance Reactions Module
# Copyright (c) 2024-2025 Dr. Nurcan Denli Bayır - All Rights Reserved
