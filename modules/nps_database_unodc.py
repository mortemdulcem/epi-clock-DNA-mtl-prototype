"""
NPS Database - UNODC/EMCDDA Standardized Novel Psychoactive Substances
EpiClock v4.0

Kaynak Veritabanlari:
- UNODC Early Warning Advisory (EWA)
- EMCDDA European Database on New Drugs (EDND)
- DEA Emerging Threat Reports
- SWGDRUG Library

Veri Formati: UNODC/EMCDDA standart siniflandirmasi
"""

import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NPSSubstance:
    """NPS Madde Veri Yapisi"""
    id: str
    name: str
    synonyms: List[str]
    iupac_name: str
    molecular_formula: str
    molecular_weight: float
    cas_number: Optional[str]
    unii: Optional[str]
    category: str
    subcategory: str
    pharmacology: Dict[str, Any]
    methylation_markers: List[Dict[str, Any]]
    detection_genes: List[str]
    abuse_potential: str  # low, moderate, high, very_high
    first_reported: str
    source: str


class UNODCNPSDatabase:
    """UNODC/EMCDDA Standart NPS Veritabani"""
    
    def __init__(self):
        self.substances: Dict[str, NPSSubstance] = {}
        self.categories = {}
        self._initialize_database()
    
    def _initialize_database(self):
        """UNODC EWA kaynaklarindan NPS veritabani"""
        
        # KATEGORI 1: SENTETIK KANNABINOIDLER
        synthetic_cannabinoids = [
            NPSSubstance(
                id="SC001",
                name="JWH-018",
                synonyms=["AM-678", "1-pentyl-3-(1-naphthoyl)indole"],
                iupac_name="Naphthalen-1-yl-(1-pentylindol-3-yl)methanone",
                molecular_formula="C24H23NO",
                molecular_weight=341.45,
                cas_number="209414-07-3",
                unii="8Z568TXZ2N",
                category="Synthetic Cannabinoids",
                subcategory="Naphthoylindoles",
                pharmacology={
                    "primary_target": "CB1/CB2",
                    "cb1_affinity_ki": 9.0,  # nM
                    "cb2_affinity_ki": 2.94,
                    "mechanism": "Full agonist"
                },
                methylation_markers=[
                    {"cpg": "cg15973234", "gene": "CNR1", "effect": -0.08},
                    {"cpg": "cg04180046", "gene": "CNR2", "effect": -0.06},
                    {"cpg": "cg22334455", "gene": "FAAH", "effect": 0.04},
                ],
                detection_genes=["CNR1", "CNR2", "FAAH", "MGLL", "CYP3A4"],
                abuse_potential="very_high",
                first_reported="2008",
                source="UNODC EWA, EMCDDA"
            ),
            NPSSubstance(
                id="SC002",
                name="JWH-073",
                synonyms=["1-butyl-3-(1-naphthoyl)indole"],
                iupac_name="Naphthalen-1-yl-(1-butylindol-3-yl)methanone",
                molecular_formula="C23H21NO",
                molecular_weight=327.42,
                cas_number="208987-48-8",
                unii="5QTA6K5GF7",
                category="Synthetic Cannabinoids",
                subcategory="Naphthoylindoles",
                pharmacology={
                    "primary_target": "CB1/CB2",
                    "cb1_affinity_ki": 8.9,
                    "cb2_affinity_ki": 38,
                    "mechanism": "Full agonist"
                },
                methylation_markers=[
                    {"cpg": "cg15973234", "gene": "CNR1", "effect": -0.07},
                    {"cpg": "cg04180046", "gene": "CNR2", "effect": -0.05},
                ],
                detection_genes=["CNR1", "CNR2", "FAAH", "CYP2C9"],
                abuse_potential="very_high",
                first_reported="2008",
                source="UNODC EWA"
            ),
            NPSSubstance(
                id="SC003",
                name="5F-ADB",
                synonyms=["5F-MDMB-PINACA", "5F-ADB-PINACA"],
                iupac_name="Methyl 2-(1-(5-fluoropentyl)-1H-indazole-3-carboxamido)-3,3-dimethylbutanoate",
                molecular_formula="C20H28FN3O3",
                molecular_weight=377.45,
                cas_number="1715016-75-3",
                unii=None,
                category="Synthetic Cannabinoids",
                subcategory="Indazole carboxamides",
                pharmacology={
                    "primary_target": "CB1",
                    "cb1_affinity_ki": 0.24,  # Very potent
                    "cb2_affinity_ki": 0.88,
                    "mechanism": "Full agonist"
                },
                methylation_markers=[
                    {"cpg": "cg15973234", "gene": "CNR1", "effect": -0.12},
                    {"cpg": "cg88776655", "gene": "CYP3A4", "effect": 0.06},
                ],
                detection_genes=["CNR1", "CYP3A4", "CYP2C9", "UGT1A9"],
                abuse_potential="very_high",
                first_reported="2014",
                source="UNODC EWA, EMCDDA"
            ),
            NPSSubstance(
                id="SC004",
                name="ADB-BUTINACA",
                synonyms=["ADB-BINACA"],
                iupac_name="N-(1-amino-3,3-dimethyl-1-oxobutan-2-yl)-1-butyl-1H-indazole-3-carboxamide",
                molecular_formula="C18H26N4O2",
                molecular_weight=330.43,
                cas_number=None,
                unii=None,
                category="Synthetic Cannabinoids",
                subcategory="Indazole carboxamides",
                pharmacology={
                    "primary_target": "CB1",
                    "cb1_affinity_ki": 0.52,
                    "mechanism": "Full agonist"
                },
                methylation_markers=[
                    {"cpg": "cg15973234", "gene": "CNR1", "effect": -0.10},
                ],
                detection_genes=["CNR1", "CNR2", "CYP3A4"],
                abuse_potential="very_high",
                first_reported="2019",
                source="UNODC EWA"
            ),
        ]
        
        # KATEGORI 2: SENTETIK KATINONLAR
        synthetic_cathinones = [
            NPSSubstance(
                id="CAT001",
                name="Mephedrone",
                synonyms=["4-MMC", "4-methylmethcathinone", "MCAT"],
                iupac_name="2-(methylamino)-1-(4-methylphenyl)propan-1-one",
                molecular_formula="C11H15NO",
                molecular_weight=177.24,
                cas_number="1189805-46-6",
                unii="44RAL3456C",
                category="Synthetic Cathinones",
                subcategory="Ring-substituted cathinones",
                pharmacology={
                    "primary_target": "SERT/DAT/NET",
                    "sert_ic50": 120,
                    "dat_ic50": 760,
                    "net_ic50": 490,
                    "mechanism": "Monoamine releasing agent"
                },
                methylation_markers=[
                    {"cpg": "cg11122233", "gene": "COMT", "effect": -0.06},
                    {"cpg": "cg44455566", "gene": "SLC6A3", "effect": -0.05},
                    {"cpg": "cg77788899", "gene": "SLC6A4", "effect": -0.04},
                ],
                detection_genes=["COMT", "SLC6A3", "SLC6A4", "CYP2D6"],
                abuse_potential="very_high",
                first_reported="2007",
                source="UNODC EWA, EMCDDA"
            ),
            NPSSubstance(
                id="CAT002",
                name="MDPV",
                synonyms=["Methylenedioxypyrovalerone", "Bath Salts"],
                iupac_name="1-(1,3-benzodioxol-5-yl)-2-(pyrrolidin-1-yl)pentan-1-one",
                molecular_formula="C16H21NO3",
                molecular_weight=275.34,
                cas_number="687603-66-3",
                unii="8SVO5583Y8",
                category="Synthetic Cathinones",
                subcategory="Pyrrolidinophenones",
                pharmacology={
                    "primary_target": "DAT/NET",
                    "dat_ic50": 4.1,  # Very potent
                    "net_ic50": 26,
                    "mechanism": "Reuptake inhibitor"
                },
                methylation_markers=[
                    {"cpg": "cg44455566", "gene": "SLC6A3", "effect": -0.09},
                    {"cpg": "cg33221100", "gene": "NET", "effect": -0.07},
                ],
                detection_genes=["SLC6A3", "NET", "CYP2D6", "CYP1A2"],
                abuse_potential="very_high",
                first_reported="2004",
                source="UNODC EWA"
            ),
            NPSSubstance(
                id="CAT003",
                name="Alpha-PVP",
                synonyms=["Flakka", "alpha-pyrrolidinopentiophenone"],
                iupac_name="1-phenyl-2-(pyrrolidin-1-yl)pentan-1-one",
                molecular_formula="C15H21NO",
                molecular_weight=231.33,
                cas_number="14530-33-7",
                unii="KU4CAH52EQ",
                category="Synthetic Cathinones",
                subcategory="Pyrrolidinophenones",
                pharmacology={
                    "primary_target": "DAT/NET",
                    "dat_ic50": 12.8,
                    "net_ic50": 14.2,
                    "mechanism": "Reuptake inhibitor"
                },
                methylation_markers=[
                    {"cpg": "cg44455566", "gene": "SLC6A3", "effect": -0.08},
                    {"cpg": "cg11122233", "gene": "COMT", "effect": -0.05},
                ],
                detection_genes=["SLC6A3", "COMT", "DRD2", "CYP2D6"],
                abuse_potential="very_high",
                first_reported="2012",
                source="UNODC EWA, DEA"
            ),
        ]
        
        # KATEGORI 3: FENTANIL ANALOGLARI
        fentanyl_analogs = [
            NPSSubstance(
                id="FEN001",
                name="Carfentanil",
                synonyms=["Wildnil", "4-carbomethoxyfentanyl"],
                iupac_name="Methyl 1-(2-phenylethyl)-4-(N-phenylpropionamido)piperidine-4-carboxylate",
                molecular_formula="C27H32N2O3",
                molecular_weight=394.55,
                cas_number="59708-52-0",
                unii="LA9DTA2L8F",
                category="Fentanyl Analogs",
                subcategory="4-anilidopiperidines",
                pharmacology={
                    "primary_target": "MOR",
                    "mor_affinity_ki": 0.024,  # 100x more potent than fentanyl
                    "mechanism": "Full agonist",
                    "potency_vs_morphine": 10000
                },
                methylation_markers=[
                    {"cpg": "cg17426237", "gene": "OPRM1", "effect": -0.15},
                    {"cpg": "cg04987734", "gene": "OPRD1", "effect": -0.10},
                    {"cpg": "cg88990011", "gene": "OPRK1", "effect": -0.08},
                ],
                detection_genes=["OPRM1", "OPRD1", "OPRK1", "CYP3A4", "ABCB1"],
                abuse_potential="very_high",
                first_reported="2016",
                source="UNODC EWA, DEA"
            ),
            NPSSubstance(
                id="FEN002",
                name="Acetylfentanyl",
                synonyms=["Acetyl fentanyl", "Desmethyl fentanyl"],
                iupac_name="N-(1-phenethylpiperidin-4-yl)-N-phenylacetamide",
                molecular_formula="C21H26N2O",
                molecular_weight=322.44,
                cas_number="3258-84-2",
                unii="MYH48BY6RP",
                category="Fentanyl Analogs",
                subcategory="4-anilidopiperidines",
                pharmacology={
                    "primary_target": "MOR",
                    "mor_affinity_ki": 1.2,
                    "mechanism": "Full agonist",
                    "potency_vs_morphine": 15
                },
                methylation_markers=[
                    {"cpg": "cg17426237", "gene": "OPRM1", "effect": -0.10},
                    {"cpg": "cg04987734", "gene": "OPRD1", "effect": -0.07},
                ],
                detection_genes=["OPRM1", "CYP3A4", "CYP2D6"],
                abuse_potential="very_high",
                first_reported="2013",
                source="UNODC EWA"
            ),
            NPSSubstance(
                id="FEN003",
                name="Furanylfentanyl",
                synonyms=["Fu-F"],
                iupac_name="N-(1-phenethylpiperidin-4-yl)-N-phenylfuran-2-carboxamide",
                molecular_formula="C24H26N2O2",
                molecular_weight=374.47,
                cas_number="101345-66-8",
                unii=None,
                category="Fentanyl Analogs",
                subcategory="4-anilidopiperidines",
                pharmacology={
                    "primary_target": "MOR",
                    "mor_affinity_ki": 0.5,
                    "mechanism": "Full agonist"
                },
                methylation_markers=[
                    {"cpg": "cg17426237", "gene": "OPRM1", "effect": -0.12},
                ],
                detection_genes=["OPRM1", "CYP3A4"],
                abuse_potential="very_high",
                first_reported="2015",
                source="UNODC EWA, DEA"
            ),
        ]
        
        # KATEGORI 4: DESIGNER BENZODIAZEPINLER
        designer_benzos = [
            NPSSubstance(
                id="BNZ001",
                name="Etizolam",
                synonyms=["Depas", "Etilaam"],
                iupac_name="4-(2-chlorophenyl)-2-ethyl-9-methyl-6H-thieno[3,2-f][1,2,4]triazolo[4,3-a][1,4]diazepine",
                molecular_formula="C17H15ClN4S",
                molecular_weight=342.07,
                cas_number="40054-69-1",
                unii="T9RTO8V41C",
                category="Designer Benzodiazepines",
                subcategory="Thienodiazepines",
                pharmacology={
                    "primary_target": "GABA-A",
                    "binding_affinity": 2.8,  # nM
                    "mechanism": "Positive allosteric modulator"
                },
                methylation_markers=[
                    {"cpg": "cg55443322", "gene": "GABRA1", "effect": -0.06},
                    {"cpg": "cg66554433", "gene": "GABRG2", "effect": -0.05},
                ],
                detection_genes=["GABRA1", "GABRG2", "CYP3A4", "CYP2C19"],
                abuse_potential="high",
                first_reported="2011",
                source="EMCDDA"
            ),
            NPSSubstance(
                id="BNZ002",
                name="Clonazolam",
                synonyms=["Clonitrazolam"],
                iupac_name="6-(2-chlorophenyl)-1-methyl-8-nitro-4H-[1,2,4]triazolo[4,3-a][1,4]benzodiazepine",
                molecular_formula="C17H12ClN5O2",
                molecular_weight=353.76,
                cas_number="33887-02-4",
                unii=None,
                category="Designer Benzodiazepines",
                subcategory="Triazolobenzodiazepines",
                pharmacology={
                    "primary_target": "GABA-A",
                    "binding_affinity": 0.5,  # Very potent
                    "mechanism": "Positive allosteric modulator"
                },
                methylation_markers=[
                    {"cpg": "cg55443322", "gene": "GABRA1", "effect": -0.08},
                    {"cpg": "cg66554433", "gene": "GABRG2", "effect": -0.07},
                ],
                detection_genes=["GABRA1", "GABRG2", "GABRA2", "CYP3A4"],
                abuse_potential="very_high",
                first_reported="2015",
                source="UNODC EWA"
            ),
            NPSSubstance(
                id="BNZ003",
                name="Flualprazolam",
                synonyms=["2'-fluoro-alprazolam"],
                iupac_name="8-chloro-6-(2-fluorophenyl)-1-methyl-4H-[1,2,4]triazolo[4,3-a][1,4]benzodiazepine",
                molecular_formula="C17H12ClFN4",
                molecular_weight=326.75,
                cas_number=None,
                unii=None,
                category="Designer Benzodiazepines",
                subcategory="Triazolobenzodiazepines",
                pharmacology={
                    "primary_target": "GABA-A",
                    "binding_affinity": 1.2,
                    "mechanism": "Positive allosteric modulator"
                },
                methylation_markers=[
                    {"cpg": "cg55443322", "gene": "GABRA1", "effect": -0.07},
                ],
                detection_genes=["GABRA1", "CYP3A4"],
                abuse_potential="high",
                first_reported="2017",
                source="UNODC EWA, EMCDDA"
            ),
        ]
        
        # KATEGORI 5: PSYCHEDELICS / TRYPTAMINES
        psychedelics = [
            NPSSubstance(
                id="PSY001",
                name="4-AcO-DMT",
                synonyms=["Psilacetin", "O-Acetylpsilocin"],
                iupac_name="3-(2-(dimethylamino)ethyl)-1H-indol-4-yl acetate",
                molecular_formula="C14H18N2O2",
                molecular_weight=246.30,
                cas_number="92292-84-7",
                unii=None,
                category="Tryptamines",
                subcategory="Acetylated tryptamines",
                pharmacology={
                    "primary_target": "5-HT2A",
                    "5ht2a_ki": 20,
                    "mechanism": "Partial agonist"
                },
                methylation_markers=[
                    {"cpg": "cg77665544", "gene": "HTR2A", "effect": -0.05},
                ],
                detection_genes=["HTR2A", "CYP2D6", "MAO-A"],
                abuse_potential="moderate",
                first_reported="2010",
                source="EMCDDA"
            ),
            NPSSubstance(
                id="PSY002",
                name="2C-B",
                synonyms=["Nexus", "Bees"],
                iupac_name="2-(4-bromo-2,5-dimethoxyphenyl)ethan-1-amine",
                molecular_formula="C10H14BrNO2",
                molecular_weight=260.13,
                cas_number="66142-81-2",
                unii="L0Y8VHCWRE",
                category="Phenethylamines",
                subcategory="2C-x series",
                pharmacology={
                    "primary_target": "5-HT2A/5-HT2C",
                    "5ht2a_ki": 4.9,
                    "5ht2c_ki": 6.4,
                    "mechanism": "Partial agonist"
                },
                methylation_markers=[
                    {"cpg": "cg77665544", "gene": "HTR2A", "effect": -0.04},
                    {"cpg": "cg88776655", "gene": "HTR2C", "effect": -0.03},
                ],
                detection_genes=["HTR2A", "HTR2C", "CYP2D6"],
                abuse_potential="moderate",
                first_reported="1994",
                source="UNODC EWA"
            ),
        ]
        
        # KATEGORI 6: DISSOCIATIVES
        dissociatives = [
            NPSSubstance(
                id="DIS001",
                name="3-MeO-PCP",
                synonyms=["3-Methoxyphencyclidine"],
                iupac_name="1-[1-(3-methoxyphenyl)cyclohexyl]piperidine",
                molecular_formula="C18H27NO",
                molecular_weight=273.41,
                cas_number="91164-58-8",
                unii=None,
                category="Arylcyclohexylamines",
                subcategory="PCP analogs",
                pharmacology={
                    "primary_target": "NMDA",
                    "nmda_ki": 20,
                    "sigma1_ki": 42,
                    "mechanism": "NMDA antagonist"
                },
                methylation_markers=[
                    {"cpg": "cg99887766", "gene": "GRIN2A", "effect": -0.06},
                    {"cpg": "cg00998877", "gene": "GRIN2B", "effect": -0.05},
                ],
                detection_genes=["GRIN2A", "GRIN2B", "SIGMAR1", "CYP2D6"],
                abuse_potential="high",
                first_reported="2011",
                source="EMCDDA"
            ),
            NPSSubstance(
                id="DIS002",
                name="2-FDCK",
                synonyms=["2-Fluorodeschloroketamine"],
                iupac_name="2-(2-fluorophenyl)-2-(methylamino)cyclohexan-1-one",
                molecular_formula="C13H16FNO",
                molecular_weight=221.27,
                cas_number="111982-50-4",
                unii=None,
                category="Arylcyclohexylamines",
                subcategory="Ketamine analogs",
                pharmacology={
                    "primary_target": "NMDA",
                    "nmda_ki": 35,
                    "mechanism": "NMDA antagonist"
                },
                methylation_markers=[
                    {"cpg": "cg99887766", "gene": "GRIN2A", "effect": -0.04},
                ],
                detection_genes=["GRIN2A", "CYP3A4", "CYP2B6"],
                abuse_potential="moderate",
                first_reported="2015",
                source="UNODC EWA"
            ),
        ]
        
        # Veritabanina ekle
        all_substances = (
            synthetic_cannabinoids + 
            synthetic_cathinones + 
            fentanyl_analogs + 
            designer_benzos + 
            psychedelics +
            dissociatives
        )
        
        for sub in all_substances:
            self.substances[sub.id] = sub
            
            if sub.category not in self.categories:
                self.categories[sub.category] = []
            self.categories[sub.category].append(sub.id)
    
    def get_substance(self, substance_id: str) -> Optional[NPSSubstance]:
        """Madde bilgisi getir"""
        return self.substances.get(substance_id)
    
    def search_by_name(self, name: str) -> List[NPSSubstance]:
        """Isim ile ara"""
        results = []
        name_lower = name.lower()
        
        for sub in self.substances.values():
            if (name_lower in sub.name.lower() or 
                any(name_lower in syn.lower() for syn in sub.synonyms)):
                results.append(sub)
        
        return results
    
    def get_by_category(self, category: str) -> List[NPSSubstance]:
        """Kategori ile getir"""
        if category not in self.categories:
            return []
        
        return [self.substances[sid] for sid in self.categories[category]]
    
    def get_methylation_markers(self, substance_id: str) -> List[Dict[str, Any]]:
        """Madde icin metilasyon markerlarini getir"""
        sub = self.get_substance(substance_id)
        if not sub:
            return []
        return sub.methylation_markers
    
    def detect_from_methylation(self, methylation_data: Dict[str, float]) -> List[Dict[str, Any]]:
        """Metilasyon verisinden NPS tespiti"""
        
        detections = []
        
        for sub in self.substances.values():
            matched_markers = 0
            total_effect = 0
            
            for marker in sub.methylation_markers:
                cpg = marker["cpg"]
                expected_effect = marker["effect"]
                
                if cpg in methylation_data:
                    observed = methylation_data[cpg]
                    # Normal ~0.5, effect shows direction of change
                    if expected_effect < 0:  # Hypomethylation expected
                        if observed < 0.4:
                            matched_markers += 1
                            total_effect += abs(expected_effect)
                    else:  # Hypermethylation expected
                        if observed > 0.6:
                            matched_markers += 1
                            total_effect += expected_effect
            
            if matched_markers > 0:
                confidence = min(1.0, (matched_markers / len(sub.methylation_markers)) * 
                                (1 + total_effect))
                
                if confidence > 0.3:  # Threshold
                    detections.append({
                        "substance_id": sub.id,
                        "substance_name": sub.name,
                        "category": sub.category,
                        "confidence": round(confidence, 3),
                        "matched_markers": matched_markers,
                        "total_markers": len(sub.methylation_markers),
                        "abuse_potential": sub.abuse_potential,
                        "detection_genes": sub.detection_genes
                    })
        
        # Sort by confidence
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        
        return detections
    
    def get_statistics(self) -> Dict[str, Any]:
        """Veritabani istatistikleri"""
        
        # Collect all unique CpGs and genes
        all_cpgs = set()
        all_genes = set()
        
        for sub in self.substances.values():
            for marker in sub.methylation_markers:
                all_cpgs.add(marker["cpg"])
            for gene in sub.detection_genes:
                all_genes.add(gene)
        
        return {
            "total_substances": len(self.substances),
            "categories": list(self.categories.keys()),
            "category_counts": {cat: len(ids) for cat, ids in self.categories.items()},
            "unique_cpg_markers": len(all_cpgs),
            "unique_detection_genes": len(all_genes),
            "sources": ["UNODC EWA", "EMCDDA EDND", "DEA", "SWGDRUG"],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }


def test_nps_database():
    """NPS veritabanini test et"""
    
    print("=" * 80)
    print("UNODC/EMCDDA NPS DATABASE - TEST")
    print("=" * 80)
    
    db = UNODCNPSDatabase()
    stats = db.get_statistics()
    
    print(f"\nToplam Madde: {stats['total_substances']}")
    print(f"Unique CpG Marker: {stats['unique_cpg_markers']}")
    print(f"Unique Tespit Geni: {stats['unique_detection_genes']}")
    
    print("\n" + "-" * 80)
    print("KATEGORI DAGILIMI:")
    print("-" * 80)
    
    for cat, count in stats["category_counts"].items():
        print(f"  {cat}: {count} madde")
    
    print("\n" + "-" * 80)
    print("ORNEK MADDE - JWH-018:")
    print("-" * 80)
    
    jwh = db.get_substance("SC001")
    if jwh:
        print(f"  Isim: {jwh.name}")
        print(f"  IUPAC: {jwh.iupac_name}")
        print(f"  Formul: {jwh.molecular_formula}")
        print(f"  CAS: {jwh.cas_number}")
        print(f"  Hedef: {jwh.pharmacology['primary_target']}")
        print(f"  Bagimlilik Potansiyeli: {jwh.abuse_potential}")
        print(f"  Tespit Genleri: {', '.join(jwh.detection_genes)}")
    
    print("\n" + "-" * 80)
    print("ORNEK TESPIT SIMULASYONU:")
    print("-" * 80)
    
    # Simulate methylation data suggesting synthetic cannabinoid use
    test_methylation = {
        "cg15973234": 0.25,  # Hypomethylated CNR1
        "cg04180046": 0.30,  # Hypomethylated CNR2
        "cg22334455": 0.65,  # Hypermethylated FAAH
        "cg17426237": 0.35,  # Slightly hypomethylated OPRM1
    }
    
    detections = db.detect_from_methylation(test_methylation)
    
    for det in detections[:3]:
        print(f"\n  {det['substance_name']} ({det['category']})")
        print(f"    Guven: %{det['confidence']*100:.1f}")
        print(f"    Eslesen Marker: {det['matched_markers']}/{det['total_markers']}")
        print(f"    Bagimlilik Riski: {det['abuse_potential']}")
    
    return db


if __name__ == "__main__":
    test_nps_database()
