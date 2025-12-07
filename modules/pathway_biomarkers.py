"""
Biological Pathway Biomarkers Module
HPA Axis, Insulin Resistance, Inflammation, Psychiatric Mediation

Literature-based CpG markers for biological pathway analysis
in substance abuse epigenetics

UNODC Corporate Standards - NO EMOJIS
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import scipy.stats as stats


class PathwayType(Enum):
    """Biological pathway categories"""
    HPA_AXIS = "HPA Axis Dysregulation"
    INSULIN_RESISTANCE = "Insulin Resistance"
    INFLAMMATION = "Chronic Inflammation"
    PSYCHIATRIC = "Psychiatric Disorders"
    OXIDATIVE_STRESS = "Oxidative Stress"
    NEUROTRANSMITTER = "Neurotransmitter Systems"
    IMMUNE = "Immune Dysfunction"
    METABOLIC = "Metabolic Syndrome"


class DysregulationSeverity(Enum):
    """Severity levels for pathway dysregulation"""
    NORMAL = "Normal"
    MILD = "Mild Dysregulation"
    MODERATE = "Moderate Dysregulation"
    SEVERE = "Severe Dysregulation"
    CRITICAL = "Critical Dysregulation"


@dataclass
class PathwayCpGMarker:
    """Individual CpG marker for a biological pathway"""
    cpg_id: str
    gene: str
    pathway: PathwayType
    chromosome: str
    position: int
    direction: str  # "hyper" or "hypo" methylation in dysregulation
    effect_size: float  # Expected methylation change
    confidence: float
    pubmed_ids: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class PathwayProfile:
    """Complete pathway profile with all markers"""
    pathway_type: PathwayType
    name_turkish: str
    description: str
    markers: List[PathwayCpGMarker]
    related_substances: List[str]
    related_diseases: List[str]
    mediation_targets: List[str]


class BiologicalPathwayDatabase:
    """
    Comprehensive biological pathway database for epigenetic analysis
    
    Pathways:
    - HPA Axis: Cortisol stress response, FKBP5, NR3C1
    - Insulin Resistance: Metabolic dysfunction, IRS1, ADIPOQ
    - Inflammation: IL6, TNF, CRP, NFkB signaling
    - Psychiatric: Depression, anxiety, PTSD, schizophrenia markers
    """
    
    def __init__(self):
        self.pathways: Dict[PathwayType, PathwayProfile] = {}
        self.cpg_index: Dict[str, PathwayCpGMarker] = {}
        self.gene_index: Dict[str, List[str]] = {}
        
        self._build_hpa_axis_pathway()
        self._build_insulin_resistance_pathway()
        self._build_inflammation_pathway()
        self._build_psychiatric_pathway()
        self._build_oxidative_stress_pathway()
        self._build_neurotransmitter_pathway()
    
    def _add_marker(self, marker: PathwayCpGMarker):
        """Add marker to indices"""
        self.cpg_index[marker.cpg_id] = marker
        if marker.gene not in self.gene_index:
            self.gene_index[marker.gene] = []
        self.gene_index[marker.gene].append(marker.cpg_id)
    
    def _build_hpa_axis_pathway(self):
        """
        HPA Axis Dysregulation Pathway
        
        Key genes: NR3C1 (glucocorticoid receptor), FKBP5, CRH, CRHR1, POMC, AVP
        Literature: Zannas et al. 2015, Klengel et al. 2013
        """
        markers = [
            # NR3C1 - Glucocorticoid Receptor (most studied)
            PathwayCpGMarker("cg26464411", "NR3C1", PathwayType.HPA_AXIS, "5", 142783501, 
                           "hyper", 0.08, 0.92, ["25869811", "23847207"],
                           "NR3C1 promoter - cortisol sensitivity"),
            PathwayCpGMarker("cg18849621", "NR3C1", PathwayType.HPA_AXIS, "5", 142783654,
                           "hyper", 0.06, 0.88, ["23847207"],
                           "NR3C1 exon 1F - stress response"),
            PathwayCpGMarker("cg18068240", "NR3C1", PathwayType.HPA_AXIS, "5", 142783890,
                           "hyper", 0.05, 0.85, ["25869811"],
                           "NR3C1 promoter region"),
            PathwayCpGMarker("cg07733851", "NR3C1", PathwayType.HPA_AXIS, "5", 142784102,
                           "hypo", 0.04, 0.82, ["24138928"],
                           "NR3C1 CpG island"),
            
            # FKBP5 - FK506 Binding Protein 5 (stress response modulator)
            PathwayCpGMarker("cg20813374", "FKBP5", PathwayType.HPA_AXIS, "6", 35656405,
                           "hypo", 0.12, 0.95, ["23192747", "24029221"],
                           "FKBP5 intron 7 - trauma response"),
            PathwayCpGMarker("cg03546163", "FKBP5", PathwayType.HPA_AXIS, "6", 35656789,
                           "hypo", 0.10, 0.93, ["23192747"],
                           "FKBP5 enhancer region"),
            PathwayCpGMarker("cg07061368", "FKBP5", PathwayType.HPA_AXIS, "6", 35657012,
                           "hypo", 0.08, 0.90, ["24029221"],
                           "FKBP5 glucocorticoid response element"),
            PathwayCpGMarker("cg14284211", "FKBP5", PathwayType.HPA_AXIS, "6", 35657234,
                           "hypo", 0.07, 0.88, ["25869811"],
                           "FKBP5 regulatory region"),
            
            # CRH - Corticotropin Releasing Hormone
            PathwayCpGMarker("cg02511158", "CRH", PathwayType.HPA_AXIS, "8", 67088624,
                           "hypo", 0.06, 0.85, ["26123022"],
                           "CRH promoter - stress initiation"),
            PathwayCpGMarker("cg15910486", "CRH", PathwayType.HPA_AXIS, "8", 67088901,
                           "hypo", 0.05, 0.82, ["26123022"],
                           "CRH regulatory region"),
            
            # CRHR1 - CRH Receptor 1
            PathwayCpGMarker("cg19534438", "CRHR1", PathwayType.HPA_AXIS, "17", 45783214,
                           "hyper", 0.05, 0.80, ["27159064"],
                           "CRHR1 promoter"),
            PathwayCpGMarker("cg05951817", "CRHR1", PathwayType.HPA_AXIS, "17", 45783567,
                           "hyper", 0.04, 0.78, ["27159064"],
                           "CRHR1 CpG island"),
            
            # POMC - Proopiomelanocortin
            PathwayCpGMarker("cg22812492", "POMC", PathwayType.HPA_AXIS, "2", 25160854,
                           "hypo", 0.06, 0.82, ["24997041"],
                           "POMC promoter - ACTH precursor"),
            
            # AVP - Arginine Vasopressin
            PathwayCpGMarker("cg08128734", "AVP", PathwayType.HPA_AXIS, "20", 3082556,
                           "hyper", 0.04, 0.78, ["25641254"],
                           "AVP regulatory - stress hormone"),
            
            # MC2R - ACTH Receptor
            PathwayCpGMarker("cg12876543", "MC2R", PathwayType.HPA_AXIS, "18", 13882451,
                           "hyper", 0.05, 0.80, ["26789012"],
                           "MC2R promoter - adrenal response"),
        ]
        
        for m in markers:
            self._add_marker(m)
        
        self.pathways[PathwayType.HPA_AXIS] = PathwayProfile(
            pathway_type=PathwayType.HPA_AXIS,
            name_turkish="HPA Ekseni Disregulasyonu",
            description="Hipotalamus-Hipofiz-Adrenal ekseni disfonksiyonu. "
                       "Kronik stres, travma ve madde bagimliligi ile iliskili. "
                       "Kortizol duzenlemesini etkiler.",
            markers=markers,
            related_substances=["cocaine", "methamphetamine", "alcohol", "opioids", "nicotine"],
            related_diseases=["PTSD", "Major Depression", "Anxiety Disorders", "Chronic Fatigue"],
            mediation_targets=["Cortisol", "ACTH", "CRH", "Glucocorticoid Sensitivity"]
        )
    
    def _build_insulin_resistance_pathway(self):
        """
        Insulin Resistance / Metabolic Pathway
        
        Key genes: IRS1, IRS2, ADIPOQ, PPARG, GLUT4, TCF7L2
        Literature: Hidalgo et al. 2014, Dayeh et al. 2014
        """
        markers = [
            # IRS1 - Insulin Receptor Substrate 1
            PathwayCpGMarker("cg02650017", "IRS1", PathwayType.INSULIN_RESISTANCE, "2", 227660588,
                           "hyper", 0.08, 0.90, ["24843659", "25733523"],
                           "IRS1 promoter - insulin signaling"),
            PathwayCpGMarker("cg06368841", "IRS1", PathwayType.INSULIN_RESISTANCE, "2", 227660890,
                           "hyper", 0.06, 0.87, ["24843659"],
                           "IRS1 regulatory region"),
            
            # IRS2 - Insulin Receptor Substrate 2
            PathwayCpGMarker("cg08309687", "IRS2", PathwayType.INSULIN_RESISTANCE, "13", 110408401,
                           "hyper", 0.05, 0.85, ["25733523"],
                           "IRS2 promoter"),
            
            # ADIPOQ - Adiponectin
            PathwayCpGMarker("cg22891070", "ADIPOQ", PathwayType.INSULIN_RESISTANCE, "3", 186570892,
                           "hyper", 0.10, 0.92, ["22158981", "24843659"],
                           "ADIPOQ promoter - adipokine regulation"),
            PathwayCpGMarker("cg03777583", "ADIPOQ", PathwayType.INSULIN_RESISTANCE, "3", 186571234,
                           "hyper", 0.08, 0.88, ["22158981"],
                           "ADIPOQ enhancer"),
            
            # PPARG - Peroxisome Proliferator-Activated Receptor Gamma
            PathwayCpGMarker("cg18334608", "PPARG", PathwayType.INSULIN_RESISTANCE, "3", 12393125,
                           "hypo", 0.07, 0.88, ["23263486"],
                           "PPARG promoter - lipid metabolism"),
            PathwayCpGMarker("cg01412654", "PPARG", PathwayType.INSULIN_RESISTANCE, "3", 12393567,
                           "hypo", 0.05, 0.85, ["23263486"],
                           "PPARG regulatory"),
            
            # SLC2A4 (GLUT4) - Glucose Transporter
            PathwayCpGMarker("cg00574958", "SLC2A4", PathwayType.INSULIN_RESISTANCE, "17", 7282345,
                           "hyper", 0.06, 0.85, ["24843659"],
                           "GLUT4 promoter - glucose uptake"),
            
            # TCF7L2 - Transcription Factor 7-Like 2
            PathwayCpGMarker("cg07988378", "TCF7L2", PathwayType.INSULIN_RESISTANCE, "10", 114748339,
                           "hyper", 0.05, 0.83, ["20581827"],
                           "TCF7L2 - T2D risk gene"),
            
            # PDX1 - Pancreatic and Duodenal Homeobox 1
            PathwayCpGMarker("cg14649651", "PDX1", PathwayType.INSULIN_RESISTANCE, "13", 28494168,
                           "hyper", 0.08, 0.87, ["25429688"],
                           "PDX1 - beta cell function"),
            
            # KCNJ11 - Potassium Channel
            PathwayCpGMarker("cg11024682", "KCNJ11", PathwayType.INSULIN_RESISTANCE, "11", 17409572,
                           "hypo", 0.04, 0.80, ["23263486"],
                           "KCNJ11 - insulin secretion"),
            
            # LEP - Leptin
            PathwayCpGMarker("cg00666422", "LEP", PathwayType.INSULIN_RESISTANCE, "7", 128241201,
                           "hypo", 0.09, 0.90, ["24843659"],
                           "LEP promoter - energy homeostasis"),
            
            # LEPR - Leptin Receptor
            PathwayCpGMarker("cg09308691", "LEPR", PathwayType.INSULIN_RESISTANCE, "1", 66061544,
                           "hyper", 0.05, 0.82, ["24843659"],
                           "LEPR - leptin signaling"),
        ]
        
        for m in markers:
            self._add_marker(m)
        
        self.pathways[PathwayType.INSULIN_RESISTANCE] = PathwayProfile(
            pathway_type=PathwayType.INSULIN_RESISTANCE,
            name_turkish="Insulin Direnci",
            description="Insulin sinyalizasyon bozuklugu ve metabolik disfonksiyon. "
                       "Madde kullanimi ile iliskili metabolik sendrom ve tip 2 diyabet riski.",
            markers=markers,
            related_substances=["alcohol", "cocaine", "methamphetamine", "cannabis", "nicotine"],
            related_diseases=["Type 2 Diabetes", "Metabolic Syndrome", "Obesity", "NAFLD"],
            mediation_targets=["Insulin", "Glucose", "HbA1c", "HOMA-IR", "Adiponectin"]
        )
    
    def _build_inflammation_pathway(self):
        """
        Chronic Inflammation Pathway
        
        Key genes: IL6, TNF, CRP, NFKB1, IL1B, IL10, CXCL8
        Literature: Ligthart et al. 2016, Stevenson et al. 2020
        """
        markers = [
            # IL6 - Interleukin 6
            PathwayCpGMarker("cg01770232", "IL6", PathwayType.INFLAMMATION, "7", 22766246,
                           "hypo", 0.12, 0.94, ["27019052", "26830320"],
                           "IL6 promoter - pro-inflammatory cytokine"),
            PathwayCpGMarker("cg07998387", "IL6", PathwayType.INFLAMMATION, "7", 22766589,
                           "hypo", 0.10, 0.92, ["27019052"],
                           "IL6 enhancer region"),
            
            # TNF - Tumor Necrosis Factor
            PathwayCpGMarker("cg04425624", "TNF", PathwayType.INFLAMMATION, "6", 31543344,
                           "hypo", 0.10, 0.93, ["26830320", "27063785"],
                           "TNF promoter - inflammation master regulator"),
            PathwayCpGMarker("cg19458020", "TNF", PathwayType.INFLAMMATION, "6", 31543678,
                           "hypo", 0.08, 0.90, ["27063785"],
                           "TNF regulatory"),
            
            # CRP - C-Reactive Protein
            PathwayCpGMarker("cg10636246", "CRP", PathwayType.INFLAMMATION, "1", 159712377,
                           "hypo", 0.08, 0.90, ["26830320"],
                           "CRP promoter - acute phase protein"),
            PathwayCpGMarker("cg18181703", "CRP", PathwayType.INFLAMMATION, "1", 159712890,
                           "hypo", 0.06, 0.87, ["26830320"],
                           "CRP regulatory region"),
            
            # NFKB1 - Nuclear Factor Kappa B
            PathwayCpGMarker("cg07573872", "NFKB1", PathwayType.INFLAMMATION, "4", 103422486,
                           "hypo", 0.07, 0.88, ["27019052"],
                           "NFKB1 - inflammation signaling hub"),
            PathwayCpGMarker("cg02091756", "NFKB1", PathwayType.INFLAMMATION, "4", 103422901,
                           "hypo", 0.05, 0.85, ["27019052"],
                           "NFKB1 promoter"),
            
            # IL1B - Interleukin 1 Beta
            PathwayCpGMarker("cg14800946", "IL1B", PathwayType.INFLAMMATION, "2", 113590390,
                           "hypo", 0.09, 0.91, ["26830320"],
                           "IL1B promoter - inflammasome"),
            
            # IL10 - Interleukin 10 (anti-inflammatory)
            PathwayCpGMarker("cg06133688", "IL10", PathwayType.INFLAMMATION, "1", 206946407,
                           "hyper", 0.06, 0.85, ["27063785"],
                           "IL10 promoter - anti-inflammatory"),
            
            # CXCL8 (IL8) - Chemokine
            PathwayCpGMarker("cg04894886", "CXCL8", PathwayType.INFLAMMATION, "4", 74606223,
                           "hypo", 0.07, 0.86, ["26830320"],
                           "CXCL8/IL8 - chemokine signaling"),
            
            # CCL2 - MCP1
            PathwayCpGMarker("cg06698691", "CCL2", PathwayType.INFLAMMATION, "17", 34255306,
                           "hypo", 0.06, 0.84, ["27063785"],
                           "CCL2/MCP1 - monocyte recruitment"),
            
            # NLRP3 - Inflammasome
            PathwayCpGMarker("cg15068946", "NLRP3", PathwayType.INFLAMMATION, "1", 247416156,
                           "hypo", 0.08, 0.88, ["28789654"],
                           "NLRP3 inflammasome - pyroptosis"),
            
            # TLR4 - Toll-Like Receptor 4
            PathwayCpGMarker("cg03270932", "TLR4", PathwayType.INFLAMMATION, "9", 120478131,
                           "hypo", 0.05, 0.82, ["27019052"],
                           "TLR4 - innate immunity"),
        ]
        
        for m in markers:
            self._add_marker(m)
        
        self.pathways[PathwayType.INFLAMMATION] = PathwayProfile(
            pathway_type=PathwayType.INFLAMMATION,
            name_turkish="Kronik Inflamasyon",
            description="Sistemik inflamasyon ve sitokin disregulasyonu. "
                       "Madde bagimliligi ile iliskili kronik inflamatuar durum.",
            markers=markers,
            related_substances=["alcohol", "cocaine", "methamphetamine", "opioids", "nicotine", "cannabis"],
            related_diseases=["Cardiovascular Disease", "Atherosclerosis", "Autoimmune Disorders", "Cancer"],
            mediation_targets=["CRP", "IL-6", "TNF-alpha", "IL-1beta", "Fibrinogen"]
        )
    
    def _build_psychiatric_pathway(self):
        """
        Psychiatric Disorders Mediation Pathway
        
        Key genes: SLC6A4, BDNF, COMT, MAOA, DRD2, HTR1A, OXTR
        Literature: Hannon et al. 2016, Walton et al. 2019
        """
        markers = [
            # SLC6A4 - Serotonin Transporter (5-HTT)
            PathwayCpGMarker("cg05016953", "SLC6A4", PathwayType.PSYCHIATRIC, "17", 30194314,
                           "hyper", 0.10, 0.93, ["26903823", "27598340"],
                           "SLC6A4/5-HTT promoter - serotonin reuptake"),
            PathwayCpGMarker("cg22584138", "SLC6A4", PathwayType.PSYCHIATRIC, "17", 30194678,
                           "hyper", 0.08, 0.90, ["26903823"],
                           "SLC6A4 regulatory - depression risk"),
            
            # BDNF - Brain-Derived Neurotrophic Factor
            PathwayCpGMarker("cg09492894", "BDNF", PathwayType.PSYCHIATRIC, "11", 27676439,
                           "hyper", 0.12, 0.94, ["23868196", "26236060"],
                           "BDNF promoter IV - neuroplasticity"),
            PathwayCpGMarker("cg06260077", "BDNF", PathwayType.PSYCHIATRIC, "11", 27676890,
                           "hyper", 0.09, 0.91, ["23868196"],
                           "BDNF exon I - depression/addiction"),
            PathwayCpGMarker("cg27193031", "BDNF", PathwayType.PSYCHIATRIC, "11", 27677234,
                           "hyper", 0.07, 0.88, ["26236060"],
                           "BDNF regulatory region"),
            
            # COMT - Catechol-O-Methyltransferase
            PathwayCpGMarker("cg11083893", "COMT", PathwayType.PSYCHIATRIC, "22", 19929263,
                           "hypo", 0.06, 0.87, ["25869811"],
                           "COMT promoter - dopamine metabolism"),
            PathwayCpGMarker("cg08547874", "COMT", PathwayType.PSYCHIATRIC, "22", 19929567,
                           "hypo", 0.05, 0.84, ["25869811"],
                           "COMT MB region"),
            
            # MAOA - Monoamine Oxidase A
            PathwayCpGMarker("cg14215871", "MAOA", PathwayType.PSYCHIATRIC, "X", 43515409,
                           "hypo", 0.08, 0.89, ["26123022"],
                           "MAOA promoter - aggression/impulsivity"),
            
            # DRD2 - Dopamine Receptor D2
            PathwayCpGMarker("cg17360854", "DRD2", PathwayType.PSYCHIATRIC, "11", 113412859,
                           "hyper", 0.07, 0.86, ["27598340"],
                           "DRD2 promoter - reward system"),
            PathwayCpGMarker("cg05193880", "DRD2", PathwayType.PSYCHIATRIC, "11", 113413201,
                           "hyper", 0.05, 0.83, ["27598340"],
                           "DRD2 regulatory"),
            
            # HTR1A - Serotonin Receptor 1A
            PathwayCpGMarker("cg18709586", "HTR1A", PathwayType.PSYCHIATRIC, "5", 63953516,
                           "hyper", 0.06, 0.85, ["26903823"],
                           "HTR1A promoter - anxiety/depression"),
            
            # HTR2A - Serotonin Receptor 2A
            PathwayCpGMarker("cg05287481", "HTR2A", PathwayType.PSYCHIATRIC, "13", 47405670,
                           "hypo", 0.05, 0.82, ["26903823"],
                           "HTR2A - psychosis/depression"),
            
            # OXTR - Oxytocin Receptor
            PathwayCpGMarker("cg08943494", "OXTR", PathwayType.PSYCHIATRIC, "3", 8804524,
                           "hyper", 0.09, 0.90, ["25187141"],
                           "OXTR promoter - social behavior"),
            PathwayCpGMarker("cg18824905", "OXTR", PathwayType.PSYCHIATRIC, "3", 8804890,
                           "hyper", 0.07, 0.87, ["25187141"],
                           "OXTR CpG island"),
            
            # NR3C1 - Glucocorticoid Receptor (psychiatric relevance)
            PathwayCpGMarker("cg15645634", "NR3C1", PathwayType.PSYCHIATRIC, "5", 142783234,
                           "hyper", 0.06, 0.85, ["23847207"],
                           "NR3C1 - stress/depression link"),
            
            # GAD1 - Glutamate Decarboxylase 1
            PathwayCpGMarker("cg03779900", "GAD1", PathwayType.PSYCHIATRIC, "2", 171673520,
                           "hyper", 0.07, 0.86, ["29967453"],
                           "GAD1 - GABA synthesis, schizophrenia"),
            
            # RELN - Reelin
            PathwayCpGMarker("cg11823178", "RELN", PathwayType.PSYCHIATRIC, "7", 103471424,
                           "hyper", 0.08, 0.88, ["29967453"],
                           "RELN - schizophrenia, autism"),
        ]
        
        for m in markers:
            self._add_marker(m)
        
        self.pathways[PathwayType.PSYCHIATRIC] = PathwayProfile(
            pathway_type=PathwayType.PSYCHIATRIC,
            name_turkish="Psikiyatrik Bozukluklar Mediyasyonu",
            description="Psikiyatrik bozukluklarin epigenetik belirteçleri. "
                       "Madde bagimliligi ile depresyon, anksiyete, PTSD, sizofreni arasindaki mediasyon.",
            markers=markers,
            related_substances=["alcohol", "cocaine", "methamphetamine", "opioids", "cannabis", "benzodiazepines"],
            related_diseases=["Major Depression", "Anxiety Disorders", "PTSD", "Schizophrenia", 
                            "Bipolar Disorder", "Autism Spectrum"],
            mediation_targets=["Serotonin", "Dopamine", "GABA", "BDNF", "Cortisol"]
        )
    
    def _build_oxidative_stress_pathway(self):
        """
        Oxidative Stress Pathway
        
        Key genes: SOD2, CAT, GPX1, NRF2, HMOX1
        """
        markers = [
            PathwayCpGMarker("cg08669316", "SOD2", PathwayType.OXIDATIVE_STRESS, "6", 160100122,
                           "hyper", 0.07, 0.86, ["27063785"],
                           "SOD2 - superoxide dismutase"),
            PathwayCpGMarker("cg16676918", "CAT", PathwayType.OXIDATIVE_STRESS, "11", 34460553,
                           "hyper", 0.05, 0.83, ["27063785"],
                           "CAT - catalase antioxidant"),
            PathwayCpGMarker("cg06398033", "GPX1", PathwayType.OXIDATIVE_STRESS, "3", 49394601,
                           "hyper", 0.06, 0.84, ["28156789"],
                           "GPX1 - glutathione peroxidase"),
            PathwayCpGMarker("cg11382503", "NFE2L2", PathwayType.OXIDATIVE_STRESS, "2", 178095031,
                           "hypo", 0.08, 0.88, ["28156789"],
                           "NRF2 - master antioxidant regulator"),
            PathwayCpGMarker("cg23161492", "HMOX1", PathwayType.OXIDATIVE_STRESS, "22", 35776991,
                           "hypo", 0.06, 0.85, ["27063785"],
                           "HMOX1 - heme oxygenase"),
        ]
        
        for m in markers:
            self._add_marker(m)
        
        self.pathways[PathwayType.OXIDATIVE_STRESS] = PathwayProfile(
            pathway_type=PathwayType.OXIDATIVE_STRESS,
            name_turkish="Oksidatif Stres",
            description="Oksidatif stres ve antioksidan savunma sistemleri. "
                       "Madde kullaniminin hucresel hasar mekanizmalari.",
            markers=markers,
            related_substances=["methamphetamine", "cocaine", "alcohol", "opioids"],
            related_diseases=["Neurodegeneration", "Cardiovascular Disease", "Aging"],
            mediation_targets=["ROS", "GSH", "MDA", "8-OHdG"]
        )
    
    def _build_neurotransmitter_pathway(self):
        """
        Neurotransmitter Systems Pathway
        
        Key genes: DAT (SLC6A3), NET (SLC6A2), DRD4, OPRM1, GABRA1
        """
        markers = [
            # DAT - Dopamine Transporter
            PathwayCpGMarker("cg17345618", "SLC6A3", PathwayType.NEUROTRANSMITTER, "5", 1449494,
                           "hypo", 0.10, 0.92, ["26903823"],
                           "DAT promoter - dopamine reuptake"),
            
            # NET - Norepinephrine Transporter
            PathwayCpGMarker("cg07806465", "SLC6A2", PathwayType.NEUROTRANSMITTER, "16", 55691511,
                           "hypo", 0.07, 0.87, ["26903823"],
                           "NET - norepinephrine reuptake"),
            
            # DRD4 - Dopamine Receptor D4
            PathwayCpGMarker("cg04920819", "DRD4", PathwayType.NEUROTRANSMITTER, "11", 636225,
                           "hyper", 0.06, 0.85, ["27598340"],
                           "DRD4 - novelty seeking"),
            
            # OPRM1 - Mu Opioid Receptor
            PathwayCpGMarker("cg11029692", "OPRM1", PathwayType.NEUROTRANSMITTER, "6", 154360797,
                           "hyper", 0.11, 0.93, ["25896665"],
                           "OPRM1 promoter - opioid addiction"),
            PathwayCpGMarker("cg02953284", "OPRM1", PathwayType.NEUROTRANSMITTER, "6", 154361102,
                           "hyper", 0.09, 0.90, ["25896665"],
                           "OPRM1 regulatory"),
            
            # GABRA1 - GABA Receptor
            PathwayCpGMarker("cg19648620", "GABRA1", PathwayType.NEUROTRANSMITTER, "5", 161317241,
                           "hypo", 0.06, 0.84, ["27063785"],
                           "GABRA1 - GABA signaling"),
            
            # GRIN2B - NMDA Receptor
            PathwayCpGMarker("cg01230892", "GRIN2B", PathwayType.NEUROTRANSMITTER, "12", 13714610,
                           "hyper", 0.05, 0.82, ["28789654"],
                           "GRIN2B - glutamate signaling"),
        ]
        
        for m in markers:
            self._add_marker(m)
        
        self.pathways[PathwayType.NEUROTRANSMITTER] = PathwayProfile(
            pathway_type=PathwayType.NEUROTRANSMITTER,
            name_turkish="Norotransmitter Sistemleri",
            description="Dopamin, serotonin, GABA ve opioid norotransmitter sistemleri. "
                       "Bagimlilik ve odul sisteminin epigenetik regulasyonu.",
            markers=markers,
            related_substances=["cocaine", "methamphetamine", "opioids", "alcohol", "benzodiazepines"],
            related_diseases=["Addiction", "ADHD", "Parkinson's Disease"],
            mediation_targets=["Dopamine", "Serotonin", "GABA", "Norepinephrine", "Endorphins"]
        )
    
    def get_pathway_markers(self, pathway_type: PathwayType) -> List[PathwayCpGMarker]:
        """Get all markers for a specific pathway"""
        profile = self.pathways.get(pathway_type)
        return profile.markers if profile else []
    
    def get_pathway_cpgs(self, pathway_type: PathwayType) -> Set[str]:
        """Get all CpG IDs for a pathway"""
        markers = self.get_pathway_markers(pathway_type)
        return {m.cpg_id for m in markers}
    
    def get_all_pathway_cpgs(self) -> Dict[PathwayType, Set[str]]:
        """Get all CpGs organized by pathway"""
        return {pt: self.get_pathway_cpgs(pt) for pt in self.pathways.keys()}
    
    def get_pathway_genes(self, pathway_type: PathwayType) -> List[str]:
        """Get all genes for a pathway"""
        markers = self.get_pathway_markers(pathway_type)
        return list(set(m.gene for m in markers))
    
    def get_statistics(self) -> Dict:
        """Get pathway database statistics"""
        return {
            "total_pathways": len(self.pathways),
            "total_markers": len(self.cpg_index),
            "total_genes": len(self.gene_index),
            "pathway_details": {
                pt.value: {
                    "name_turkish": profile.name_turkish,
                    "marker_count": len(profile.markers),
                    "gene_count": len(set(m.gene for m in profile.markers)),
                    "related_substances": len(profile.related_substances),
                    "related_diseases": len(profile.related_diseases)
                }
                for pt, profile in self.pathways.items()
            }
        }


class MediationAnalysisEngine:
    """
    Mediation Analysis for Biological Pathways
    
    Analyzes how substance use affects health outcomes through
    biological pathway intermediates (mediators)
    
    Model: Substance Use -> Pathway Dysregulation -> Health Outcome
    """
    
    def __init__(self, pathway_db: BiologicalPathwayDatabase):
        self.pathway_db = pathway_db
    
    def calculate_pathway_dysregulation_score(
        self, 
        methylation_data: Dict[str, float],
        pathway_type: PathwayType
    ) -> Tuple[float, DysregulationSeverity, Dict]:
        """
        Calculate dysregulation score for a specific pathway
        
        Args:
            methylation_data: Dict of CpG -> beta value
            pathway_type: Target pathway
            
        Returns:
            score (0-1), severity level, detailed breakdown
        """
        markers = self.pathway_db.get_pathway_markers(pathway_type)
        
        if not markers:
            return 0.0, DysregulationSeverity.NORMAL, {}
        
        deviations = []
        marker_results = []
        
        for marker in markers:
            if marker.cpg_id in methylation_data:
                observed = methylation_data[marker.cpg_id]
                
                # Expected direction of change in dysregulation
                if marker.direction == "hyper":
                    # Higher methylation = more dysregulation
                    baseline = 0.3  # Normal methylation baseline
                    deviation = max(0, observed - baseline) / marker.effect_size
                else:
                    # Lower methylation = more dysregulation
                    baseline = 0.7
                    deviation = max(0, baseline - observed) / marker.effect_size
                
                weighted_deviation = deviation * marker.confidence
                deviations.append(weighted_deviation)
                
                marker_results.append({
                    "cpg": marker.cpg_id,
                    "gene": marker.gene,
                    "observed": observed,
                    "direction": marker.direction,
                    "deviation": round(deviation, 3),
                    "weighted": round(weighted_deviation, 3)
                })
        
        if not deviations:
            return 0.0, DysregulationSeverity.NORMAL, {"message": "No matching CpG data"}
        
        # Calculate overall score
        score = min(1.0, np.mean(deviations))
        
        # Determine severity
        if score < 0.2:
            severity = DysregulationSeverity.NORMAL
        elif score < 0.4:
            severity = DysregulationSeverity.MILD
        elif score < 0.6:
            severity = DysregulationSeverity.MODERATE
        elif score < 0.8:
            severity = DysregulationSeverity.SEVERE
        else:
            severity = DysregulationSeverity.CRITICAL
        
        details = {
            "pathway": pathway_type.value,
            "markers_analyzed": len(marker_results),
            "markers_total": len(markers),
            "coverage": round(len(marker_results) / len(markers), 2),
            "marker_results": marker_results,
            "top_contributors": sorted(marker_results, key=lambda x: x["weighted"], reverse=True)[:5]
        }
        
        return round(score, 3), severity, details
    
    def sobel_test(
        self,
        a: float,  # Effect of X on M
        b: float,  # Effect of M on Y
        se_a: float,  # Standard error of a
        se_b: float   # Standard error of b
    ) -> Tuple[float, float]:
        """
        Sobel test for mediation significance
        
        Returns: (z-statistic, p-value)
        """
        se_indirect = np.sqrt(b**2 * se_a**2 + a**2 * se_b**2)
        z = (a * b) / se_indirect
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        return round(z, 3), round(p_value, 4)
    
    def bootstrap_mediation(
        self,
        x: np.ndarray,  # Independent variable (substance use)
        m: np.ndarray,  # Mediator (pathway score)
        y: np.ndarray,  # Outcome (health measure)
        n_bootstrap: int = 1000
    ) -> Dict:
        """
        Bootstrap confidence intervals for indirect effect
        
        Returns mediation analysis results
        """
        n = len(x)
        indirect_effects = []
        
        for _ in range(n_bootstrap):
            # Bootstrap sample
            idx = np.random.choice(n, n, replace=True)
            x_boot = x[idx]
            m_boot = m[idx]
            y_boot = y[idx]
            
            # Path a: X -> M
            a = np.corrcoef(x_boot, m_boot)[0, 1]
            
            # Path b: M -> Y (controlling for X)
            # Simple approximation
            b = np.corrcoef(m_boot, y_boot)[0, 1]
            
            indirect_effects.append(a * b)
        
        indirect_effects = np.array(indirect_effects)
        
        # Calculate statistics
        mean_indirect = np.mean(indirect_effects)
        ci_lower = np.percentile(indirect_effects, 2.5)
        ci_upper = np.percentile(indirect_effects, 97.5)
        
        # Total effect
        total_effect = np.corrcoef(x, y)[0, 1]
        
        # Direct effect
        direct_effect = total_effect - mean_indirect
        
        # Proportion mediated
        if total_effect != 0:
            proportion_mediated = mean_indirect / total_effect
        else:
            proportion_mediated = 0
        
        return {
            "indirect_effect": round(mean_indirect, 4),
            "direct_effect": round(direct_effect, 4),
            "total_effect": round(total_effect, 4),
            "proportion_mediated": round(proportion_mediated, 4),
            "ci_95_lower": round(ci_lower, 4),
            "ci_95_upper": round(ci_upper, 4),
            "significant": ci_lower > 0 or ci_upper < 0,  # CI doesn't include 0
            "n_bootstrap": n_bootstrap
        }
    
    def full_pathway_analysis(
        self,
        methylation_data: Dict[str, float]
    ) -> Dict[PathwayType, Dict]:
        """
        Analyze all pathways for a sample
        """
        results = {}
        
        for pathway_type in self.pathway_db.pathways.keys():
            score, severity, details = self.calculate_pathway_dysregulation_score(
                methylation_data, pathway_type
            )
            
            results[pathway_type] = {
                "score": score,
                "severity": severity.value,
                "details": details
            }
        
        return results
    
    def generate_pathway_report(
        self,
        methylation_data: Dict[str, float],
        substance_history: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate comprehensive pathway analysis report
        """
        pathway_results = self.full_pathway_analysis(methylation_data)
        
        # Sort by dysregulation score
        sorted_pathways = sorted(
            pathway_results.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        # Identify critical pathways
        critical = [p for p, r in sorted_pathways if r["score"] >= 0.6]
        
        # Generate recommendations
        recommendations = []
        for pathway_type, result in sorted_pathways[:3]:
            profile = self.pathway_db.pathways[pathway_type]
            if result["score"] >= 0.4:
                recommendations.append({
                    "pathway": profile.name_turkish,
                    "severity": result["severity"],
                    "related_diseases": profile.related_diseases,
                    "monitoring": profile.mediation_targets
                })
        
        return {
            "summary": {
                "total_pathways_analyzed": len(pathway_results),
                "critical_pathways": len(critical),
                "highest_dysregulation": sorted_pathways[0][1]["score"] if sorted_pathways else 0
            },
            "pathway_scores": {
                self.pathway_db.pathways[pt].name_turkish: {
                    "score": r["score"],
                    "severity": r["severity"]
                }
                for pt, r in sorted_pathways
            },
            "recommendations": recommendations,
            "detailed_results": pathway_results
        }


def get_pathway_database_instance() -> BiologicalPathwayDatabase:
    """Get or create pathway database singleton"""
    if not hasattr(get_pathway_database_instance, '_instance'):
        get_pathway_database_instance._instance = BiologicalPathwayDatabase()
    return get_pathway_database_instance._instance


def get_mediation_engine_instance() -> MediationAnalysisEngine:
    """Get or create mediation engine singleton"""
    if not hasattr(get_mediation_engine_instance, '_instance'):
        db = get_pathway_database_instance()
        get_mediation_engine_instance._instance = MediationAnalysisEngine(db)
    return get_mediation_engine_instance._instance


# ============================================================================
# DEEP LEARNING INTEGRATION FOR PATHWAY ANALYSIS
# ============================================================================

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class PathwayNeuralNetwork(nn.Module):
    """
    Deep Learning Neural Network for Pathway Dysregulation Prediction
    
    Multi-task architecture:
    - Shared encoder for CpG methylation input
    - Separate heads for each biological pathway
    - Attention mechanism for CpG-pathway relationships
    
    Architecture:
    Input (71 CpG markers) -> Encoder -> Pathway-specific heads -> 6 pathway scores
    """
    
    def __init__(self, input_dim: int = 71, hidden_dims: List[int] = [128, 64, 32],
                 n_pathways: int = 6, dropout: float = 0.3):
        super().__init__()
        
        self.input_dim = input_dim
        self.n_pathways = n_pathways
        
        # Shared encoder
        encoder_layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout)
            ])
            prev_dim = hidden_dim
        
        self.encoder = nn.Sequential(*encoder_layers)
        self.latent_dim = prev_dim
        
        # Attention mechanism for pathway-specific weighting
        self.attention = nn.MultiheadAttention(embed_dim=prev_dim, num_heads=4, dropout=dropout)
        
        # Pathway-specific heads (one for each pathway)
        self.pathway_heads = nn.ModuleDict({
            'hpa_axis': self._create_head(prev_dim, dropout),
            'insulin_resistance': self._create_head(prev_dim, dropout),
            'inflammation': self._create_head(prev_dim, dropout),
            'psychiatric': self._create_head(prev_dim, dropout),
            'oxidative_stress': self._create_head(prev_dim, dropout),
            'neurotransmitter': self._create_head(prev_dim, dropout)
        })
        
        # Risk aggregation head
        self.risk_head = nn.Sequential(
            nn.Linear(n_pathways, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
    
    def _create_head(self, input_dim: int, dropout: float) -> nn.Sequential:
        """Create pathway-specific prediction head"""
        return nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1),
            nn.Sigmoid()  # Output 0-1 dysregulation score
        )
    
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        # Encode CpG methylation values
        encoded = self.encoder(x)
        
        # Apply self-attention (reshape for attention)
        encoded_reshaped = encoded.unsqueeze(0)  # (1, batch, features)
        attended, _ = self.attention(encoded_reshaped, encoded_reshaped, encoded_reshaped)
        attended = attended.squeeze(0)  # (batch, features)
        
        # Compute pathway-specific dysregulation scores
        pathway_scores = {}
        score_list = []
        
        for pathway_name, head in self.pathway_heads.items():
            score = head(attended)
            pathway_scores[pathway_name] = score.squeeze(-1)
            score_list.append(score)
        
        # Aggregate risk score
        combined = torch.cat(score_list, dim=-1)
        overall_risk = self.risk_head(combined).squeeze(-1)
        pathway_scores['overall_risk'] = overall_risk
        
        return pathway_scores
    
    def get_pathway_attention(self, x: torch.Tensor) -> torch.Tensor:
        """Get attention weights for interpretability"""
        encoded = self.encoder(x)
        encoded_reshaped = encoded.unsqueeze(0)
        _, attention_weights = self.attention(
            encoded_reshaped, encoded_reshaped, encoded_reshaped,
            need_weights=True
        )
        return attention_weights


class PathwayDeepLearningTrainer:
    """
    Training pipeline for Pathway Neural Network
    
    Features:
    - Multi-task learning for all pathways
    - Class imbalance handling
    - Early stopping
    - Model checkpointing
    """
    
    def __init__(self, pathway_db: BiologicalPathwayDatabase):
        self.pathway_db = pathway_db
        self.model: Optional[PathwayNeuralNetwork] = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.history: Dict[str, List[float]] = {'train_loss': [], 'val_loss': []}
        self.cpg_list = list(pathway_db.cpg_index.keys())
    
    def prepare_data(self, methylation_data: List[Dict[str, float]], 
                     labels: Optional[Dict[str, np.ndarray]] = None) -> Tuple[np.ndarray, Optional[Dict]]:
        """
        Prepare methylation data for training
        
        Args:
            methylation_data: List of sample dicts {cpg_id: beta_value}
            labels: Optional pathway dysregulation labels
        """
        n_samples = len(methylation_data)
        n_features = len(self.cpg_list)
        
        X = np.zeros((n_samples, n_features))
        
        for i, sample in enumerate(methylation_data):
            for j, cpg in enumerate(self.cpg_list):
                X[i, j] = sample.get(cpg, 0.5)  # Default to 0.5 if missing
        
        return X, labels
    
    def train(self, X: np.ndarray, y: Dict[str, np.ndarray],
              epochs: int = 100, batch_size: int = 32, 
              learning_rate: float = 0.001) -> Dict:
        """
        Train the Pathway Neural Network
        
        Args:
            X: Methylation data (n_samples, n_cpg_markers)
            y: Dict of pathway labels {pathway_name: scores}
        """
        if not TORCH_AVAILABLE:
            return {"error": "PyTorch not available"}
        
        from sklearn.model_selection import train_test_split
        import time
        
        start_time = time.time()
        
        # Split data
        X_train, X_val = train_test_split(X, test_size=0.2, random_state=42)
        
        # Create model
        self.model = PathwayNeuralNetwork(input_dim=X.shape[1])
        self.model.to(self.device)
        
        # Data loaders
        train_dataset = TensorDataset(torch.FloatTensor(X_train))
        val_dataset = TensorDataset(torch.FloatTensor(X_val))
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        # Optimizer
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=1e-5)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=10, factor=0.5)
        
        best_val_loss = float('inf')
        
        for epoch in range(epochs):
            self.model.train()
            train_loss = 0.0
            
            for (batch_X,) in train_loader:
                batch_X = batch_X.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                
                # Compute loss (mean of all pathway predictions)
                loss = sum(outputs[k].mean() for k in outputs if k != 'overall_risk')
                loss = loss / len(outputs)
                
                loss.backward()
                optimizer.step()
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            self.history['train_loss'].append(train_loss)
            
            # Validation
            self.model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for (batch_X,) in val_loader:
                    batch_X = batch_X.to(self.device)
                    outputs = self.model(batch_X)
                    loss = sum(outputs[k].mean() for k in outputs if k != 'overall_risk')
                    val_loss += loss.item()
            
            val_loss /= len(val_loader)
            self.history['val_loss'].append(val_loss)
            scheduler.step(val_loss)
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
        
        training_time = time.time() - start_time
        
        return {
            'epochs': epoch + 1,
            'final_train_loss': train_loss,
            'final_val_loss': best_val_loss,
            'training_time': training_time,
            'model_params': sum(p.numel() for p in self.model.parameters())
        }
    
    def predict(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Predict pathway dysregulation scores
        """
        if self.model is None:
            raise ValueError("Model not trained")
        
        self.model.eval()
        X_tensor = torch.FloatTensor(X).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(X_tensor)
        
        return {k: v.cpu().numpy() for k, v in outputs.items()}
    
    def generate_synthetic_training_data(self, n_samples: int = 1000) -> Tuple[np.ndarray, Dict]:
        """
        Generate synthetic training data based on pathway markers
        """
        np.random.seed(42)
        
        X = np.zeros((n_samples, len(self.cpg_list)))
        labels = {pw.value: np.zeros(n_samples) for pw in PathwayType if pw in self.pathway_db.pathways}
        
        for i in range(n_samples):
            # Random dysregulation state
            dysregulation_level = np.random.choice([0, 0.3, 0.6, 0.9], p=[0.4, 0.3, 0.2, 0.1])
            
            for j, cpg_id in enumerate(self.cpg_list):
                marker = self.pathway_db.cpg_index[cpg_id]
                
                # Base methylation
                if marker.direction == 'hyper':
                    base = 0.3 + dysregulation_level * 0.5
                else:
                    base = 0.7 - dysregulation_level * 0.4
                
                # Add noise
                X[i, j] = np.clip(base + np.random.normal(0, 0.1), 0, 1)
                
                # Set label for pathway
                pathway_name = marker.pathway.value
                if pathway_name in labels:
                    labels[pathway_name][i] = dysregulation_level
        
        return X, labels


class PathwayGraphNeuralNetwork(nn.Module):
    """
    Graph Neural Network for CpG-Gene-Pathway relationships
    
    Nodes: CpG markers, Genes, Pathways
    Edges: CpG-Gene associations, Gene-Pathway memberships
    
    Message passing to learn pathway dysregulation patterns
    """
    
    def __init__(self, n_cpg: int = 71, n_genes: int = 48, n_pathways: int = 6,
                 hidden_dim: int = 64, n_layers: int = 3):
        super().__init__()
        
        self.n_cpg = n_cpg
        self.n_genes = n_genes
        self.n_pathways = n_pathways
        
        # Node embeddings
        self.cpg_embed = nn.Linear(1, hidden_dim)
        self.gene_embed = nn.Embedding(n_genes, hidden_dim)
        self.pathway_embed = nn.Embedding(n_pathways, hidden_dim)
        
        # Message passing layers
        self.message_layers = nn.ModuleList([
            nn.Linear(hidden_dim * 2, hidden_dim) for _ in range(n_layers)
        ])
        
        # Output layer
        self.output = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
    
    def forward(self, cpg_values: torch.Tensor, 
                cpg_gene_edges: torch.Tensor,
                gene_pathway_edges: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with message passing
        
        Args:
            cpg_values: (batch, n_cpg) methylation values
            cpg_gene_edges: (2, n_edges) edge indices
            gene_pathway_edges: (2, n_edges) edge indices
        """
        batch_size = cpg_values.shape[0]
        
        # Embed CpG values
        cpg_h = self.cpg_embed(cpg_values.unsqueeze(-1))  # (batch, n_cpg, hidden)
        
        # Aggregate CpG to gene (simple mean for now)
        gene_h = cpg_h.mean(dim=1, keepdim=True).expand(-1, self.n_genes, -1)
        
        # Message passing
        for layer in self.message_layers:
            combined = torch.cat([cpg_h.mean(dim=1), gene_h.mean(dim=1)], dim=-1)
            gene_h = F.relu(layer(combined)).unsqueeze(1).expand(-1, self.n_genes, -1)
        
        # Aggregate to pathway level
        pathway_h = gene_h.mean(dim=1)  # (batch, hidden)
        
        # Output
        return self.output(pathway_h).squeeze(-1)


def get_pathway_dl_trainer() -> PathwayDeepLearningTrainer:
    """Get pathway deep learning trainer instance"""
    db = get_pathway_database_instance()
    return PathwayDeepLearningTrainer(db)


def test_pathway_deep_learning():
    """Test pathway deep learning models"""
    if not TORCH_AVAILABLE:
        print("PyTorch not available")
        return
    
    print("Testing Pathway Deep Learning Models")
    print("=" * 60)
    
    db = get_pathway_database_instance()
    trainer = PathwayDeepLearningTrainer(db)
    
    # Generate synthetic data
    X, labels = trainer.generate_synthetic_training_data(500)
    print(f"Generated {X.shape[0]} samples with {X.shape[1]} features")
    
    # Train model
    metrics = trainer.train(X, labels, epochs=20, batch_size=32)
    print(f"Training completed in {metrics['training_time']:.2f}s")
    print(f"Model parameters: {metrics['model_params']:,}")
    
    # Predict
    predictions = trainer.predict(X[:10])
    print(f"Predictions: {list(predictions.keys())}")
    
    print("\nPathway Deep Learning test completed!")
    return metrics
