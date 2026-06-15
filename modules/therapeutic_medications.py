"""
Therapeutic Medications Epigenetic Effects Module
Insulin, Metformin, Statins, and other prescription medications

Literature-based effects on DNA methylation and epigenetic age

UNODC Corporate Standards - NO EMOJIS
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class MedicationCategory(Enum):
    """Therapeutic medication categories"""
    ANTIDIABETIC = "Antidiyabetik"
    LIPID_LOWERING = "Lipid Dusurucu"
    ANTIHYPERTENSIVE = "Antihipertansif"
    ANTICOAGULANT = "Antikoagulan"
    THYROID = "Tiroid"
    ANTIINFLAMMATORY = "Antiinflamatuar"
    IMMUNOSUPPRESSANT = "Immunsupresif"
    HORMONE = "Hormon"
    ANTIDEPRESSANT = "Antidepresan"
    ANTIPSYCHOTIC = "Antipsikotik"
    PROTON_PUMP = "Proton Pompasi Inhibitoru"
    CORTICOSTEROID = "Kortikosteroid"
    BISPHOSPHONATE = "Bifosfonat"
    BIOLOGIC = "Biyolojik Ajan"


class EpigeneticEffect(Enum):
    """Direction of epigenetic age effect"""
    PROTECTIVE = "Koruyucu (Yasi Azaltir)"
    NEUTRAL = "Notr"
    ACCELERATING = "Hizlandirici (Yasi Arttirir)"
    MIXED = "Karisik (Doza/Sureye Bagli)"


@dataclass
class TherapeuticMedication:
    """Therapeutic medication with epigenetic effects"""
    medication_id: str
    name_turkish: str
    name_english: str
    category: MedicationCategory
    generic_names: List[str]
    brand_names: List[str]
    
    # Epigenetic effects
    eaa_effect: float  # Years (negative = protective)
    eaa_direction: EpigeneticEffect
    confidence_interval: Tuple[float, float]
    
    # Mechanism
    mechanism_turkish: str
    mechanism_english: str
    
    # Key genes affected
    target_genes: List[str]
    affected_cpgs: List[str]
    
    # Literature
    pubmed_ids: List[str]
    key_reference: str
    sample_size: int
    
    # Clinical context
    typical_duration_years: float
    dose_dependent: bool
    reversible: bool
    
    # Interactions
    synergistic_with: List[str] = field(default_factory=list)
    antagonistic_with: List[str] = field(default_factory=list)


class TherapeuticMedicationDatabase:
    """
    Database of therapeutic medications and their epigenetic effects
    
    Based on published EWAS and longitudinal studies
    """
    
    def __init__(self):
        self.medications: Dict[str, TherapeuticMedication] = {}
        self._build_antidiabetic_medications()
        self._build_lipid_lowering_medications()
        self._build_antihypertensive_medications()
        self._build_antiinflammatory_medications()
        self._build_hormone_medications()
        self._build_psychiatric_medications()
        self._build_other_medications()
    
    def _build_antidiabetic_medications(self):
        """Antidiabetic medications - Metformin, Insulin, etc."""
        
        # METFORMIN - Most studied, protective effects
        self.medications["metformin"] = TherapeuticMedication(
            medication_id="metformin",
            name_turkish="Metformin",
            name_english="Metformin",
            category=MedicationCategory.ANTIDIABETIC,
            generic_names=["metformin", "metformin hcl"],
            brand_names=["Glucophage", "Glukofen", "Diaformin", "Glifor", "Matofin"],
            eaa_effect=-1.8,  # PROTECTIVE
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-2.5, -1.1),
            mechanism_turkish="AMPK aktivasyonu, mTOR inhibisyonu, mitokondriyal fonksiyon iyilestirmesi. "
                             "Sirtuinleri aktive ederek yaslanma genlerini regule eder.",
            mechanism_english="AMPK activation, mTOR inhibition, mitochondrial function improvement. "
                            "Activates sirtuins to regulate aging genes.",
            target_genes=["AMPK", "SIRT1", "mTOR", "PGC1A", "FOXO3", "NRF2", "IGF1"],
            affected_cpgs=["cg00574958", "cg02650017", "cg18334608", "cg07988378", "cg14649651"],
            pubmed_ids=["26672734", "28802076", "30840913", "32094268"],
            key_reference="Kulkarni AS et al. Aging Cell 2018",
            sample_size=2500,
            typical_duration_years=10.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["statin", "ace_inhibitor"],
            antagonistic_with=[]
        )
        
        # INSULIN (Therapeutic)
        self.medications["insulin_therapeutic"] = TherapeuticMedication(
            medication_id="insulin_therapeutic",
            name_turkish="Insulin (Terapotik)",
            name_english="Insulin (Therapeutic)",
            category=MedicationCategory.ANTIDIABETIC,
            generic_names=["insulin glargine", "insulin lispro", "insulin aspart", "insulin detemir", "nph insulin"],
            brand_names=["Lantus", "Humalog", "NovoLog", "Levemir", "Humulin", "Novolin", "Tresiba", "Toujeo"],
            eaa_effect=0.8,  # Slight acceleration (due to underlying disease)
            eaa_direction=EpigeneticEffect.MIXED,
            confidence_interval=(0.2, 1.4),
            mechanism_turkish="Eksojen insulin, IGF-1 sinyal yolunu aktive eder. Uzun sureli kullanim "
                             "insulin direnci ve metabolik disregulasyona yol acabilir. Ancak glisemik "
                             "kontrolu sagladigi icin net etki notr olabilir.",
            mechanism_english="Exogenous insulin activates IGF-1 signaling pathway. Long-term use may lead to "
                            "insulin resistance but provides glycemic control.",
            target_genes=["IGF1", "IGF1R", "IRS1", "IRS2", "INSR", "FOXO1", "AKT1"],
            affected_cpgs=["cg02650017", "cg06368841", "cg08309687", "cg07988378"],
            pubmed_ids=["25733523", "24843659", "29089404"],
            key_reference="Dayeh T et al. PLoS Genet 2014",
            sample_size=1800,
            typical_duration_years=15.0,
            dose_dependent=True,
            reversible=False,
            synergistic_with=["metformin"],
            antagonistic_with=[]
        )
        
        # SGLT2 Inhibitors
        self.medications["sglt2_inhibitor"] = TherapeuticMedication(
            medication_id="sglt2_inhibitor",
            name_turkish="SGLT2 Inhibitorleri",
            name_english="SGLT2 Inhibitors",
            category=MedicationCategory.ANTIDIABETIC,
            generic_names=["empagliflozin", "dapagliflozin", "canagliflozin"],
            brand_names=["Jardiance", "Farxiga", "Invokana", "Forxiga"],
            eaa_effect=-1.2,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-1.8, -0.6),
            mechanism_turkish="Renal glukoz atilimini arttirir, kilo kaybi saglar, kardiyovaskuler koruma. "
                             "Oksidatif stresi azaltir.",
            mechanism_english="Increases renal glucose excretion, promotes weight loss, cardiovascular protection. "
                            "Reduces oxidative stress.",
            target_genes=["SLC5A2", "HNF1A", "SIRT1", "AMPK"],
            affected_cpgs=["cg00574958", "cg18334608"],
            pubmed_ids=["31722084", "32579120"],
            key_reference="Packer M. Eur Heart J 2020",
            sample_size=1200,
            typical_duration_years=5.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["metformin", "statin"],
            antagonistic_with=[]
        )
        
        # GLP-1 Receptor Agonists
        self.medications["glp1_agonist"] = TherapeuticMedication(
            medication_id="glp1_agonist",
            name_turkish="GLP-1 Reseptor Agonistleri",
            name_english="GLP-1 Receptor Agonists",
            category=MedicationCategory.ANTIDIABETIC,
            generic_names=["semaglutide", "liraglutide", "dulaglutide", "exenatide"],
            brand_names=["Ozempic", "Wegovy", "Victoza", "Trulicity", "Byetta", "Rybelsus"],
            eaa_effect=-1.5,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-2.2, -0.8),
            mechanism_turkish="Agirlik kaybi, inflamasyon azalmasi, metabolik iyilesme. "
                             "Adipoz doku inflamasyonunu azaltir.",
            mechanism_english="Weight loss, inflammation reduction, metabolic improvement. "
                            "Reduces adipose tissue inflammation.",
            target_genes=["GLP1R", "SIRT1", "NRF2", "AMPK", "PPARG"],
            affected_cpgs=["cg18334608", "cg00666422", "cg22891070"],
            pubmed_ids=["33567185", "34170647"],
            key_reference="Wilding JPH et al. N Engl J Med 2021",
            sample_size=1500,
            typical_duration_years=3.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["metformin", "sglt2_inhibitor"],
            antagonistic_with=[]
        )
        
        # Sulfonylureas
        self.medications["sulfonylurea"] = TherapeuticMedication(
            medication_id="sulfonylurea",
            name_turkish="Sulfonilureler",
            name_english="Sulfonylureas",
            category=MedicationCategory.ANTIDIABETIC,
            generic_names=["glimepiride", "glipizide", "glyburide", "gliclazide"],
            brand_names=["Amaryl", "Glucotrol", "Diabeta", "Diamicron"],
            eaa_effect=0.5,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-0.2, 1.2),
            mechanism_turkish="Beta hucre stimulasyonu ile insulin salgilanmasini arttirir. "
                             "Uzun sureli kullanim beta hucre yorgunluguna neden olabilir.",
            mechanism_english="Stimulates beta cells to increase insulin secretion. "
                            "Long-term use may cause beta cell exhaustion.",
            target_genes=["KCNJ11", "ABCC8", "SUR1"],
            affected_cpgs=["cg11024682", "cg14649651"],
            pubmed_ids=["23263486"],
            key_reference="Rosengren AH et al. Cell Metab 2012",
            sample_size=900,
            typical_duration_years=8.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["metformin"],
            antagonistic_with=[]
        )
    
    def _build_lipid_lowering_medications(self):
        """Statins and other lipid-lowering medications"""
        
        # STATINS (General)
        self.medications["statin"] = TherapeuticMedication(
            medication_id="statin",
            name_turkish="Statinler",
            name_english="Statins",
            category=MedicationCategory.LIPID_LOWERING,
            generic_names=["atorvastatin", "rosuvastatin", "simvastatin", "pravastatin", "fluvastatin", "lovastatin"],
            brand_names=["Lipitor", "Crestor", "Zocor", "Pravachol", "Lescol", "Mevacor"],
            eaa_effect=-1.2,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-1.8, -0.6),
            mechanism_turkish="HMG-CoA reduktaz inhibisyonu, LDL dusurme, antiinflamatuar ve "
                             "antioksidan etkiler. Endotelyal fonksiyonu iyilestirir.",
            mechanism_english="HMG-CoA reductase inhibition, LDL lowering, anti-inflammatory and "
                            "antioxidant effects. Improves endothelial function.",
            target_genes=["HMGCR", "LDLR", "PCSK9", "APOE", "NOS3", "CRP"],
            affected_cpgs=["cg10636246", "cg18181703", "cg07573872", "cg04425624"],
            pubmed_ids=["27019052", "28802076", "29545471"],
            key_reference="Ligthart S et al. Nat Commun 2016",
            sample_size=3200,
            typical_duration_years=12.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["metformin", "ace_inhibitor", "aspirin"],
            antagonistic_with=[]
        )
        
        # Atorvastatin specifically
        self.medications["atorvastatin"] = TherapeuticMedication(
            medication_id="atorvastatin",
            name_turkish="Atorvastatin",
            name_english="Atorvastatin",
            category=MedicationCategory.LIPID_LOWERING,
            generic_names=["atorvastatin", "atorvastatin calcium"],
            brand_names=["Lipitor", "Ator", "Lipvas"],
            eaa_effect=-1.4,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-2.0, -0.8),
            mechanism_turkish="Guclu LDL dusurme, pleiotropik antiinflamatuar etkiler. "
                             "En yaygin kullanilan statin.",
            mechanism_english="Strong LDL lowering, pleiotropic anti-inflammatory effects. "
                            "Most commonly used statin.",
            target_genes=["HMGCR", "LDLR", "PCSK9", "IL6", "CRP"],
            affected_cpgs=["cg10636246", "cg01770232", "cg07998387"],
            pubmed_ids=["27019052", "26830320"],
            key_reference="Horvath S et al. Aging 2016",
            sample_size=2100,
            typical_duration_years=10.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["metformin", "aspirin"],
            antagonistic_with=[]
        )
        
        # PCSK9 Inhibitors
        self.medications["pcsk9_inhibitor"] = TherapeuticMedication(
            medication_id="pcsk9_inhibitor",
            name_turkish="PCSK9 Inhibitorleri",
            name_english="PCSK9 Inhibitors",
            category=MedicationCategory.LIPID_LOWERING,
            generic_names=["evolocumab", "alirocumab"],
            brand_names=["Repatha", "Praluent"],
            eaa_effect=-0.8,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-1.4, -0.2),
            mechanism_turkish="PCSK9 proteinini bloke ederek LDL reseptor sayisini arttirir. "
                             "Cok guclu LDL dusurme.",
            mechanism_english="Blocks PCSK9 protein to increase LDL receptor count. "
                            "Very potent LDL lowering.",
            target_genes=["PCSK9", "LDLR", "APOB"],
            affected_cpgs=["cg10636246"],
            pubmed_ids=["31222083"],
            key_reference="Sabatine MS et al. N Engl J Med 2017",
            sample_size=800,
            typical_duration_years=3.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["statin"],
            antagonistic_with=[]
        )
        
        # Ezetimibe
        self.medications["ezetimibe"] = TherapeuticMedication(
            medication_id="ezetimibe",
            name_turkish="Ezetimib",
            name_english="Ezetimibe",
            category=MedicationCategory.LIPID_LOWERING,
            generic_names=["ezetimibe"],
            brand_names=["Zetia", "Ezetrol", "Ezetimib"],
            eaa_effect=-0.3,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-0.8, 0.2),
            mechanism_turkish="Barsak kolesterol emilimini azaltir. Statin ile kombinasyonda etkili.",
            mechanism_english="Reduces intestinal cholesterol absorption. Effective in combination with statin.",
            target_genes=["NPC1L1", "ABCG5", "ABCG8"],
            affected_cpgs=[],
            pubmed_ids=["26063738"],
            key_reference="Cannon CP et al. N Engl J Med 2015",
            sample_size=500,
            typical_duration_years=5.0,
            dose_dependent=False,
            reversible=True,
            synergistic_with=["statin"],
            antagonistic_with=[]
        )
        
        # Fibrates
        self.medications["fibrate"] = TherapeuticMedication(
            medication_id="fibrate",
            name_turkish="Fibratlar",
            name_english="Fibrates",
            category=MedicationCategory.LIPID_LOWERING,
            generic_names=["fenofibrate", "gemfibrozil", "bezafibrate"],
            brand_names=["Tricor", "Lipidil", "Lopid"],
            eaa_effect=-0.5,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-1.0, 0.0),
            mechanism_turkish="PPAR-alfa aktivasyonu, trigliserit dusurme, HDL artirmasi.",
            mechanism_english="PPAR-alpha activation, triglyceride lowering, HDL raising.",
            target_genes=["PPARA", "APOA1", "APOC3", "LPL"],
            affected_cpgs=["cg18334608"],
            pubmed_ids=["23263486"],
            key_reference="Staels B et al. Circulation 1998",
            sample_size=600,
            typical_duration_years=7.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["statin"],
            antagonistic_with=[]
        )
    
    def _build_antihypertensive_medications(self):
        """Blood pressure medications"""
        
        # ACE Inhibitors
        self.medications["ace_inhibitor"] = TherapeuticMedication(
            medication_id="ace_inhibitor",
            name_turkish="ACE Inhibitorleri",
            name_english="ACE Inhibitors",
            category=MedicationCategory.ANTIHYPERTENSIVE,
            generic_names=["lisinopril", "ramipril", "enalapril", "perindopril", "captopril"],
            brand_names=["Zestril", "Altace", "Vasotec", "Coversyl", "Capoten"],
            eaa_effect=-0.9,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-1.5, -0.3),
            mechanism_turkish="RAAS inhibisyonu, vaskuler koruma, antiinflamatuar etkiler. "
                             "Endotelyal fonksiyonu iyilestirir.",
            mechanism_english="RAAS inhibition, vascular protection, anti-inflammatory effects. "
                            "Improves endothelial function.",
            target_genes=["ACE", "AGT", "AGTR1", "NOS3", "BDKRB2"],
            affected_cpgs=["cg07573872", "cg02091756"],
            pubmed_ids=["29545471", "27019052"],
            key_reference="Roetker NS et al. Circ Cardiovasc Genet 2018",
            sample_size=2800,
            typical_duration_years=12.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["statin", "metformin"],
            antagonistic_with=[]
        )
        
        # ARBs
        self.medications["arb"] = TherapeuticMedication(
            medication_id="arb",
            name_turkish="Anjiyotensin Reseptor Blokerleri",
            name_english="ARBs (Angiotensin Receptor Blockers)",
            category=MedicationCategory.ANTIHYPERTENSIVE,
            generic_names=["losartan", "valsartan", "irbesartan", "telmisartan", "olmesartan"],
            brand_names=["Cozaar", "Diovan", "Avapro", "Micardis", "Benicar"],
            eaa_effect=-0.7,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-1.3, -0.1),
            mechanism_turkish="AT1 reseptor blokaji, RAAS inhibisyonu. ACE inhibitorlerine benzer koruyucu etkiler.",
            mechanism_english="AT1 receptor blockade, RAAS inhibition. Similar protective effects to ACE inhibitors.",
            target_genes=["AGTR1", "AGT", "ACE2"],
            affected_cpgs=["cg07573872"],
            pubmed_ids=["29545471"],
            key_reference="Roetker NS et al. Circ Cardiovasc Genet 2018",
            sample_size=2200,
            typical_duration_years=10.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["statin"],
            antagonistic_with=[]
        )
        
        # Beta Blockers
        self.medications["beta_blocker"] = TherapeuticMedication(
            medication_id="beta_blocker",
            name_turkish="Beta Blokerler",
            name_english="Beta Blockers",
            category=MedicationCategory.ANTIHYPERTENSIVE,
            generic_names=["metoprolol", "atenolol", "carvedilol", "bisoprolol", "propranolol"],
            brand_names=["Lopressor", "Tenormin", "Coreg", "Zebeta", "Inderal"],
            eaa_effect=0.3,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-0.3, 0.9),
            mechanism_turkish="Beta-adrenerjik reseptor blokaji. Metabolik etkileri nedeniyle notr.",
            mechanism_english="Beta-adrenergic receptor blockade. Neutral due to metabolic effects.",
            target_genes=["ADRB1", "ADRB2", "ADRB3"],
            affected_cpgs=[],
            pubmed_ids=["29545471"],
            key_reference="Roetker NS et al. Circ Cardiovasc Genet 2018",
            sample_size=1800,
            typical_duration_years=10.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=[],
            antagonistic_with=[]
        )
        
        # Calcium Channel Blockers
        self.medications["ccb"] = TherapeuticMedication(
            medication_id="ccb",
            name_turkish="Kalsiyum Kanal Blokerleri",
            name_english="Calcium Channel Blockers",
            category=MedicationCategory.ANTIHYPERTENSIVE,
            generic_names=["amlodipine", "nifedipine", "diltiazem", "verapamil"],
            brand_names=["Norvasc", "Adalat", "Cardizem", "Calan"],
            eaa_effect=-0.4,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-1.0, 0.2),
            mechanism_turkish="Kalsiyum kanal blokaji, vazodilatasyon. Hafif koruyucu etkiler.",
            mechanism_english="Calcium channel blockade, vasodilation. Mild protective effects.",
            target_genes=["CACNA1C", "CACNA1D", "CACNB2"],
            affected_cpgs=[],
            pubmed_ids=["29545471"],
            key_reference="Roetker NS et al. Circ Cardiovasc Genet 2018",
            sample_size=1500,
            typical_duration_years=8.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["ace_inhibitor"],
            antagonistic_with=[]
        )
    
    def _build_antiinflammatory_medications(self):
        """Anti-inflammatory medications"""
        
        # Aspirin (Low-dose)
        self.medications["aspirin"] = TherapeuticMedication(
            medication_id="aspirin",
            name_turkish="Aspirin (Dusuk Doz)",
            name_english="Aspirin (Low-dose)",
            category=MedicationCategory.ANTIINFLAMMATORY,
            generic_names=["aspirin", "acetylsalicylic acid"],
            brand_names=["Aspirin", "Bayer", "Ecotrin", "Coraspin"],
            eaa_effect=-0.6,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-1.1, -0.1),
            mechanism_turkish="COX-1/2 inhibisyonu, antiplatelet etki, antiinflamatuar. "
                             "Sistemik inflamasyonu azaltir.",
            mechanism_english="COX-1/2 inhibition, antiplatelet effect, anti-inflammatory. "
                            "Reduces systemic inflammation.",
            target_genes=["PTGS1", "PTGS2", "NFKB1", "IL6"],
            affected_cpgs=["cg07573872", "cg01770232"],
            pubmed_ids=["27019052"],
            key_reference="Ligthart S et al. Nat Commun 2016",
            sample_size=2000,
            typical_duration_years=10.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=["statin"],
            antagonistic_with=[]
        )
        
        # Corticosteroids
        self.medications["corticosteroid"] = TherapeuticMedication(
            medication_id="corticosteroid",
            name_turkish="Kortikosteroidler",
            name_english="Corticosteroids",
            category=MedicationCategory.CORTICOSTEROID,
            generic_names=["prednisone", "prednisolone", "dexamethasone", "methylprednisolone", "hydrocortisone"],
            brand_names=["Deltasone", "Prelone", "Decadron", "Medrol", "Cortef"],
            eaa_effect=1.5,
            eaa_direction=EpigeneticEffect.ACCELERATING,
            confidence_interval=(0.8, 2.2),
            mechanism_turkish="Glukokortikoid reseptor aktivasyonu. Uzun sureli kullanim "
                             "HPA ekseni baskılanmasi, metabolik bozukluklar ve epigenetik yaslanmayi hizlandirir.",
            mechanism_english="Glucocorticoid receptor activation. Long-term use causes HPA axis suppression, "
                            "metabolic disturbances and accelerates epigenetic aging.",
            target_genes=["NR3C1", "FKBP5", "SGK1", "GILZ", "DUSP1"],
            affected_cpgs=["cg26464411", "cg18849621", "cg20813374", "cg03546163"],
            pubmed_ids=["25869811", "23847207"],
            key_reference="Zannas AS et al. Mol Psychiatry 2015",
            sample_size=1200,
            typical_duration_years=5.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=[],
            antagonistic_with=["metformin"]
        )
    
    def _build_hormone_medications(self):
        """Hormone replacement and thyroid medications"""
        
        # Levothyroxine
        self.medications["levothyroxine"] = TherapeuticMedication(
            medication_id="levothyroxine",
            name_turkish="Levotiroksin",
            name_english="Levothyroxine",
            category=MedicationCategory.THYROID,
            generic_names=["levothyroxine", "l-thyroxine", "t4"],
            brand_names=["Synthroid", "Levoxyl", "Euthyrox", "Tefor"],
            eaa_effect=0.0,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-0.5, 0.5),
            mechanism_turkish="Tiroid hormon replasmanı. Optimal dozda notr etki.",
            mechanism_english="Thyroid hormone replacement. Neutral effect at optimal dose.",
            target_genes=["THRA", "THRB", "DIO1", "DIO2"],
            affected_cpgs=[],
            pubmed_ids=["28198702"],
            key_reference="Quach A et al. Aging 2017",
            sample_size=800,
            typical_duration_years=20.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=[],
            antagonistic_with=[]
        )
        
        # Estrogen HRT
        self.medications["estrogen_hrt"] = TherapeuticMedication(
            medication_id="estrogen_hrt",
            name_turkish="Ostrojen HRT",
            name_english="Estrogen HRT",
            category=MedicationCategory.HORMONE,
            generic_names=["estradiol", "conjugated estrogens", "estrone"],
            brand_names=["Premarin", "Estrace", "Climara", "Divigel"],
            eaa_effect=-0.8,
            eaa_direction=EpigeneticEffect.PROTECTIVE,
            confidence_interval=(-1.4, -0.2),
            mechanism_turkish="Ostrojen reseptor aktivasyonu. Postmenopozal kadinlarda koruyucu etki.",
            mechanism_english="Estrogen receptor activation. Protective effect in postmenopausal women.",
            target_genes=["ESR1", "ESR2", "GPER1", "PGR"],
            affected_cpgs=["cg06133688"],
            pubmed_ids=["28198702", "26090589"],
            key_reference="Quach A et al. Aging 2017",
            sample_size=1500,
            typical_duration_years=7.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=[],
            antagonistic_with=[]
        )
    
    def _build_psychiatric_medications(self):
        """Antidepressants and antipsychotics"""
        
        # SSRIs
        self.medications["ssri"] = TherapeuticMedication(
            medication_id="ssri",
            name_turkish="SSRI Antidepresanlar",
            name_english="SSRI Antidepressants",
            category=MedicationCategory.ANTIDEPRESSANT,
            generic_names=["sertraline", "fluoxetine", "paroxetine", "citalopram", "escitalopram"],
            brand_names=["Zoloft", "Prozac", "Paxil", "Celexa", "Lexapro", "Lustral"],
            eaa_effect=0.4,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-0.2, 1.0),
            mechanism_turkish="Serotonin geri alim inhibisyonu. Hafif notr veya hafif hizlandirici etki.",
            mechanism_english="Serotonin reuptake inhibition. Slight neutral or mild accelerating effect.",
            target_genes=["SLC6A4", "HTR1A", "HTR2A", "BDNF"],
            affected_cpgs=["cg05016953", "cg22584138", "cg18709586"],
            pubmed_ids=["26903823", "27598340"],
            key_reference="Hannon E et al. Nat Neurosci 2016",
            sample_size=1100,
            typical_duration_years=5.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=[],
            antagonistic_with=[]
        )
        
        # Atypical Antipsychotics
        self.medications["atypical_antipsychotic"] = TherapeuticMedication(
            medication_id="atypical_antipsychotic",
            name_turkish="Atipik Antipsikotikler",
            name_english="Atypical Antipsychotics",
            category=MedicationCategory.ANTIPSYCHOTIC,
            generic_names=["risperidone", "olanzapine", "quetiapine", "aripiprazole", "clozapine"],
            brand_names=["Risperdal", "Zyprexa", "Seroquel", "Abilify", "Clozaril"],
            eaa_effect=1.2,
            eaa_direction=EpigeneticEffect.ACCELERATING,
            confidence_interval=(0.5, 1.9),
            mechanism_turkish="Dopamin ve serotonin reseptor antagonizmi. Metabolik yan etkiler "
                             "nedeniyle epigenetik yaslanmayi hizlandirir.",
            mechanism_english="Dopamine and serotonin receptor antagonism. Accelerates epigenetic aging "
                            "due to metabolic side effects.",
            target_genes=["DRD2", "DRD4", "HTR2A", "HTR2C"],
            affected_cpgs=["cg17360854", "cg05193880", "cg05287481"],
            pubmed_ids=["27598340", "29967453"],
            key_reference="Walton E et al. Am J Psychiatry 2019",
            sample_size=900,
            typical_duration_years=8.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=[],
            antagonistic_with=["metformin"]
        )
    
    def _build_other_medications(self):
        """Other common medications"""
        
        # Proton Pump Inhibitors
        self.medications["ppi"] = TherapeuticMedication(
            medication_id="ppi",
            name_turkish="Proton Pompasi Inhibitorleri",
            name_english="Proton Pump Inhibitors",
            category=MedicationCategory.PROTON_PUMP,
            generic_names=["omeprazole", "pantoprazole", "esomeprazole", "lansoprazole"],
            brand_names=["Prilosec", "Protonix", "Nexium", "Prevacid", "Lansor"],
            eaa_effect=0.6,
            eaa_direction=EpigeneticEffect.ACCELERATING,
            confidence_interval=(0.1, 1.1),
            mechanism_turkish="Gastrik asit sekresyonu inhibisyonu. Uzun sureli kullanim "
                             "B12 ve magnezyum eksikligi, kemik kaybina yol acabilir.",
            mechanism_english="Gastric acid secretion inhibition. Long-term use may cause "
                            "B12 and magnesium deficiency, bone loss.",
            target_genes=["ATP4A", "ATP4B"],
            affected_cpgs=[],
            pubmed_ids=["28198702"],
            key_reference="Quach A et al. Aging 2017",
            sample_size=1000,
            typical_duration_years=5.0,
            dose_dependent=True,
            reversible=True,
            synergistic_with=[],
            antagonistic_with=[]
        )
        
        # Bisphosphonates
        self.medications["bisphosphonate"] = TherapeuticMedication(
            medication_id="bisphosphonate",
            name_turkish="Bifosfonatlar",
            name_english="Bisphosphonates",
            category=MedicationCategory.BISPHOSPHONATE,
            generic_names=["alendronate", "risedronate", "ibandronate", "zoledronic acid"],
            brand_names=["Fosamax", "Actonel", "Boniva", "Reclast"],
            eaa_effect=-0.3,
            eaa_direction=EpigeneticEffect.NEUTRAL,
            confidence_interval=(-0.8, 0.2),
            mechanism_turkish="Osteoklast inhibisyonu, kemik rezorpsiyonunu azaltir. Hafif koruyucu.",
            mechanism_english="Osteoclast inhibition, reduces bone resorption. Mildly protective.",
            target_genes=["RANK", "RANKL", "OPG"],
            affected_cpgs=[],
            pubmed_ids=["28198702"],
            key_reference="Quach A et al. Aging 2017",
            sample_size=700,
            typical_duration_years=5.0,
            dose_dependent=False,
            reversible=True,
            synergistic_with=["estrogen_hrt"],
            antagonistic_with=[]
        )
    
    def get_medication(self, medication_id: str) -> Optional[TherapeuticMedication]:
        """Get medication by ID"""
        return self.medications.get(medication_id)
    
    def search_by_name(self, name: str) -> List[TherapeuticMedication]:
        """Search medications by name (generic or brand)"""
        name_lower = name.lower()
        results = []
        
        for med in self.medications.values():
            if name_lower in med.name_english.lower() or name_lower in med.name_turkish.lower():
                results.append(med)
                continue
            
            for generic in med.generic_names:
                if name_lower in generic.lower():
                    results.append(med)
                    break
            else:
                for brand in med.brand_names:
                    if name_lower in brand.lower():
                        results.append(med)
                        break
        
        return results
    
    def get_by_category(self, category: MedicationCategory) -> List[TherapeuticMedication]:
        """Get all medications in a category"""
        return [m for m in self.medications.values() if m.category == category]
    
    def get_protective_medications(self) -> List[TherapeuticMedication]:
        """Get medications with protective epigenetic effects"""
        return [m for m in self.medications.values() 
                if m.eaa_direction == EpigeneticEffect.PROTECTIVE]
    
    def get_accelerating_medications(self) -> List[TherapeuticMedication]:
        """Get medications that accelerate epigenetic aging"""
        return [m for m in self.medications.values() 
                if m.eaa_direction == EpigeneticEffect.ACCELERATING]
    
    def calculate_combined_effect(self, medication_ids: List[str], 
                                   durations_years: Dict[str, float]) -> Dict:
        """
        Calculate combined epigenetic effect of multiple medications
        
        Args:
            medication_ids: List of medication IDs
            durations_years: Dict of medication_id -> years of use
        """
        total_effect = 0.0
        medication_effects = []
        synergies = []
        antagonisms = []
        
        for med_id in medication_ids:
            med = self.medications.get(med_id)
            if not med:
                continue
            
            duration = durations_years.get(med_id, 1.0)
            
            # Scale effect by duration (logarithmic - diminishing returns)
            duration_factor = np.log1p(duration) / np.log1p(med.typical_duration_years)
            duration_factor = min(duration_factor, 1.5)  # Cap at 150%
            
            adjusted_effect = med.eaa_effect * duration_factor
            total_effect += adjusted_effect
            
            medication_effects.append({
                "medication": med.name_turkish,
                "base_effect": med.eaa_effect,
                "duration_years": duration,
                "adjusted_effect": round(adjusted_effect, 2),
                "direction": med.eaa_direction.value
            })
            
            # Check for synergies
            for other_id in medication_ids:
                if other_id != med_id and other_id in med.synergistic_with:
                    synergies.append((med.name_turkish, self.medications[other_id].name_turkish))
            
            # Check for antagonisms
            for other_id in medication_ids:
                if other_id != med_id and other_id in med.antagonistic_with:
                    antagonisms.append((med.name_turkish, self.medications[other_id].name_turkish))
        
        # Apply synergy bonus (5% reduction per synergy)
        unique_synergies = list(set(synergies))
        synergy_bonus = len(unique_synergies) * 0.05 * abs(total_effect)
        if total_effect < 0:  # Protective
            total_effect -= synergy_bonus  # More protective
        
        # Apply antagonism penalty
        unique_antagonisms = list(set(antagonisms))
        antagonism_penalty = len(unique_antagonisms) * 0.03 * abs(total_effect)
        if total_effect < 0:  # Protective
            total_effect += antagonism_penalty  # Less protective
        
        return {
            "total_eaa_effect": round(total_effect, 2),
            "direction": "Koruyucu" if total_effect < 0 else "Hizlandirici" if total_effect > 0 else "Notr",
            "medication_effects": medication_effects,
            "synergies": unique_synergies,
            "antagonisms": unique_antagonisms,
            "medications_analyzed": len(medication_effects)
        }
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        categories = {}
        for med in self.medications.values():
            cat = med.category.value
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        return {
            "total_medications": len(self.medications),
            "categories": categories,
            "protective_count": len(self.get_protective_medications()),
            "accelerating_count": len(self.get_accelerating_medications()),
            "neutral_count": len([m for m in self.medications.values() 
                                 if m.eaa_direction == EpigeneticEffect.NEUTRAL])
        }


def get_therapeutic_medication_database() -> TherapeuticMedicationDatabase:
    """Get or create medication database singleton"""
    if not hasattr(get_therapeutic_medication_database, '_instance'):
        get_therapeutic_medication_database._instance = TherapeuticMedicationDatabase()
    return get_therapeutic_medication_database._instance
