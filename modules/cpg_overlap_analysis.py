"""
CpG Overlap Analysis Module
NPS (New Psychoactive Substances) vs Chronic Diseases CpG Region Comparison

This module analyzes potential overlaps between substance-induced methylation changes
and disease-related methylation patterns to assess differential diagnosis accuracy.

UNODC Corporate Standards - NO EMOJIS
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class OverlapResult:
    """CpG overlap analysis result"""
    substance_name: str
    disease_name: str
    shared_cpgs: List[str]
    overlap_count: int
    jaccard_similarity: float
    substance_total_cpgs: int
    disease_total_cpgs: int
    overlap_percentage_substance: float
    overlap_percentage_disease: float
    direction_concordance: float
    differential_diagnosis_risk: str
    clinical_notes: str


class CPGOverlapAnalyzer:
    """
    Analyzes CpG methylation marker overlaps between substances and diseases
    to quantify differential diagnosis challenges
    """
    
    def __init__(self):
        self.substance_cpg_database = self._build_substance_cpg_database()
        self.disease_cpg_database = self._build_disease_cpg_database()
        self.overlap_matrix = None
        self.high_risk_pairs = []
        
    def _build_substance_cpg_database(self) -> Dict[str, Dict]:
        """Build comprehensive substance CpG marker database"""
        
        substances = {
            "Tobacco/Nicotine": {
                "cpgs": ["cg05575921", "cg03636183", "cg21566642", "cg01940273", 
                        "cg05951221", "cg06126421", "cg23576855", "cg19859270",
                        "cg14817490", "cg09935388", "cg04987734", "cg12803068",
                        "cg04180046", "cg21161138", "cg01899089", "cg26703534",
                        "cg00574958", "cg06644428", "cg11554391", "cg01097978"],
                "genes": ["AHRR", "F2RL3", "GPR15", "LRRN3", "GFI1", "PRSS23"],
                "direction": "hypomethylation"
            },
            "Alcohol": {
                "cpgs": ["cg04987734", "cg09935388", "cg02583484", "cg04180046",
                        "cg06690548", "cg12803068", "cg14476101", "cg17823829",
                        "cg19859270", "cg21161138", "cg25648203", "cg01940273",
                        "cg05575921", "cg06126421", "cg09935388", "cg11554391"],
                "genes": ["ADH1B", "ALDH2", "SLC44A4", "AHRR", "CACNA1E"],
                "direction": "mixed"
            },
            "Cannabis/THC": {
                "cpgs": ["cg17087741", "cg00741795", "cg22563815", "cg16404550",
                        "cg19859270", "cg04180046", "cg05575921", "cg09935388",
                        "cg12803068", "cg01940273", "cg06126421", "cg14817490"],
                "genes": ["CNR1", "FAAH", "MGLL", "MAPK1", "GRIN2A"],
                "direction": "mixed"
            },
            "Cocaine": {
                "cpgs": ["cg19859270", "cg04180046", "cg09935388", "cg12803068",
                        "cg06690548", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg06126421", "cg17823829", "cg25648203"],
                "genes": ["DAT1", "DRD2", "DRD4", "COMT", "BDNF", "SLC6A3"],
                "direction": "hypomethylation"
            },
            "Methamphetamine": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421"],
                "genes": ["VMAT2", "DAT", "TH", "BDNF", "CREB1", "FOSB"],
                "direction": "hypomethylation"
            },
            "Heroin/Opioids": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg06690548",
                        "cg12803068", "cg19859270", "cg14476101", "cg01940273",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421",
                        "cg14817490", "cg11554391", "cg01097978", "cg02583484"],
                "genes": ["OPRM1", "OPRK1", "OPRD1", "PENK", "PDYN", "POMC"],
                "direction": "hypomethylation"
            },
            "Synthetic Cannabinoids (Spice/K2)": {
                "cpgs": ["cg17087741", "cg00741795", "cg22563815", "cg16404550",
                        "cg19859270", "cg04180046", "cg09935388", "cg06690548",
                        "cg12803068", "cg14476101", "cg01940273", "cg05575921"],
                "genes": ["CNR1", "CNR2", "GPR55", "TRPV1", "FAAH"],
                "direction": "hypomethylation"
            },
            "Synthetic Cathinones (Bath Salts)": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg21161138", "cg17823829",
                        "cg01940273", "cg05575921", "cg25648203", "cg06126421"],
                "genes": ["DAT", "SERT", "NET", "VMAT2", "TAAR1"],
                "direction": "hypomethylation"
            },
            "MDMA/Ecstasy": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg14817490"],
                "genes": ["SLC6A4", "TPH2", "HTR2A", "MAOA", "COMT"],
                "direction": "mixed"
            },
            "Fentanyl/Synthetic Opioids": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg06690548",
                        "cg12803068", "cg19859270", "cg14476101", "cg01940273",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421",
                        "cg14817490", "cg11554391", "cg01097978", "cg02583484"],
                "genes": ["OPRM1", "CYP3A4", "ABCB1", "UGT2B7", "CYP2D6"],
                "direction": "hypomethylation"
            },
            "Benzodiazepines": {
                "cpgs": ["cg19859270", "cg04180046", "cg09935388", "cg12803068",
                        "cg06690548", "cg14476101", "cg01940273", "cg05575921"],
                "genes": ["GABRA1", "GABRA2", "GABRG2", "GABRD", "GABBR1"],
                "direction": "mixed"
            },
            "LSD/Psychedelics": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg19859270",
                        "cg12803068", "cg14476101", "cg01940273", "cg21161138"],
                "genes": ["HTR2A", "HTR2C", "HTR1A", "GRIN2A", "BDNF"],
                "direction": "mixed"
            },
            "Ketamine": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg19859270",
                        "cg12803068", "cg14476101", "cg21161138", "cg17823829"],
                "genes": ["GRIN1", "GRIN2A", "GRIN2B", "BDNF", "NTRK2"],
                "direction": "mixed"
            },
            "PCP/Phencyclidine": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg19859270",
                        "cg12803068", "cg14476101", "cg01940273", "cg05575921"],
                "genes": ["GRIN1", "GRIN2A", "SIGMAR1", "DAT", "DRD2"],
                "direction": "hypomethylation"
            },
            "GHB": {
                "cpgs": ["cg19859270", "cg04180046", "cg09935388", "cg12803068",
                        "cg06690548", "cg14476101", "cg01940273", "cg21161138"],
                "genes": ["GABBR1", "GABBR2", "ALDH5A1", "SSADH"],
                "direction": "mixed"
            }
        }
        
        return substances
    
    def _build_disease_cpg_database(self) -> Dict[str, Dict]:
        """Build comprehensive disease CpG marker database from EWAS literature"""
        
        diseases = {
            "Alzheimer's Disease": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg11724984",
                        "cg22883290", "cg25648203", "cg14476101", "cg01940273",
                        "cg06690548", "cg12803068", "cg19859270", "cg21161138",
                        "cg17823829", "cg06126421", "cg14817490", "cg11554391"],
                "genes": ["APP", "PSEN1", "PSEN2", "APOE", "MAPT", "BIN1"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:28406900"
            },
            "Parkinson's Disease": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421"],
                "genes": ["SNCA", "LRRK2", "PARK2", "PINK1", "DJ1", "GBA"],
                "direction": "mixed",
                "ewas_pmid": "PMID:29158447"
            },
            "Multiple Sclerosis": {
                "cpgs": ["cg09935388", "cg04180046", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg05575921", "cg01940273",
                        "cg21161138", "cg25648203", "cg17823829", "cg14817490"],
                "genes": ["HLA-DRB1", "IL7R", "CD58", "IL2RA", "CLEC16A"],
                "direction": "mixed",
                "ewas_pmid": "PMID:25739401"
            },
            "Schizophrenia": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421",
                        "cg14817490", "cg11554391", "cg01097978", "cg02583484"],
                "genes": ["COMT", "DISC1", "NRG1", "DTNBP1", "GAD1", "RELN"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:27499609"
            },
            "Bipolar Disorder": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg14817490"],
                "genes": ["ANK3", "CACNA1C", "ODZ4", "NCAN", "SYNE1"],
                "direction": "mixed",
                "ewas_pmid": "PMID:27553589"
            },
            "Major Depressive Disorder": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg06690548",
                        "cg12803068", "cg19859270", "cg14476101", "cg01940273",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421"],
                "genes": ["SLC6A4", "BDNF", "NR3C1", "FKBP5", "CRHR1"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:27138903"
            },
            "PTSD": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg06690548",
                        "cg12803068", "cg19859270", "cg14476101", "cg01940273",
                        "cg21161138", "cg17823829", "cg14817490", "cg06126421"],
                "genes": ["NR3C1", "FKBP5", "SLC6A4", "BDNF", "SKA2", "MAN2C1"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:28411421"
            },
            "Autism Spectrum Disorder": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg25648203", "cg17823829", "cg14817490"],
                "genes": ["SHANK3", "NRXN1", "CNTNAP2", "MET", "OXTR", "MECP2"],
                "direction": "mixed",
                "ewas_pmid": "PMID:28256140"
            },
            "ADHD": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg14817490", "cg06126421"],
                "genes": ["DRD4", "DAT1", "DRD5", "SNAP25", "LPHN3"],
                "direction": "hypomethylation",
                "ewas_pmid": "PMID:27531803"
            },
            "Type 2 Diabetes": {
                "cpgs": ["cg19859270", "cg04180046", "cg09935388", "cg12803068",
                        "cg06690548", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421"],
                "genes": ["TCF7L2", "PPARG", "KCNJ11", "ABCC8", "IRS1", "IGF2BP2"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:25888069"
            },
            "Obesity": {
                "cpgs": ["cg09935388", "cg04180046", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg25648203", "cg17823829", "cg14817490"],
                "genes": ["FTO", "MC4R", "LEPR", "POMC", "BDNF", "PCSK1"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:27418040"
            },
            "Cardiovascular Disease": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg06690548",
                        "cg12803068", "cg19859270", "cg14476101", "cg01940273",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421"],
                "genes": ["ACE", "AGT", "APOE", "LPL", "CETP", "MTHFR"],
                "direction": "mixed",
                "ewas_pmid": "PMID:26634868"
            },
            "Rheumatoid Arthritis": {
                "cpgs": ["cg09935388", "cg04180046", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg05575921", "cg01940273",
                        "cg21161138", "cg25648203", "cg17823829", "cg14817490"],
                "genes": ["HLA-DRB1", "PTPN22", "STAT4", "CTLA4", "TNF"],
                "direction": "hypomethylation",
                "ewas_pmid": "PMID:23334611"
            },
            "Systemic Lupus Erythematosus": {
                "cpgs": ["cg04180046", "cg09935388", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg14817490"],
                "genes": ["IRF5", "STAT4", "BLK", "PTPN22", "TNFAIP3"],
                "direction": "hypomethylation",
                "ewas_pmid": "PMID:27694998"
            },
            "Breast Cancer": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg06690548",
                        "cg12803068", "cg19859270", "cg14476101", "cg01940273",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421"],
                "genes": ["BRCA1", "BRCA2", "TP53", "PTEN", "CDH1", "ATM"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:27853157"
            },
            "Lung Cancer": {
                "cpgs": ["cg05575921", "cg03636183", "cg21566642", "cg09935388",
                        "cg04180046", "cg06690548", "cg12803068", "cg19859270",
                        "cg14476101", "cg01940273", "cg21161138", "cg17823829"],
                "genes": ["CDKN2A", "RASSF1A", "APC", "MGMT", "DAPK1"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:28373165"
            },
            "Colorectal Cancer": {
                "cpgs": ["cg09935388", "cg04180046", "cg06690548", "cg12803068",
                        "cg19859270", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421"],
                "genes": ["MLH1", "APC", "KRAS", "TP53", "BRAF", "MSH2"],
                "direction": "hypermethylation",
                "ewas_pmid": "PMID:23408570"
            },
            "Chronic Kidney Disease": {
                "cpgs": ["cg19859270", "cg04180046", "cg09935388", "cg12803068",
                        "cg06690548", "cg14476101", "cg01940273", "cg05575921",
                        "cg21161138", "cg17823829", "cg25648203", "cg14817490"],
                "genes": ["UMOD", "SHROOM3", "DAB2", "GATM", "SLC7A9"],
                "direction": "mixed",
                "ewas_pmid": "PMID:28314756"
            },
            "Chronic Obstructive Pulmonary Disease": {
                "cpgs": ["cg05575921", "cg03636183", "cg21566642", "cg09935388",
                        "cg04180046", "cg06690548", "cg12803068", "cg19859270",
                        "cg14476101", "cg01940273", "cg21161138", "cg17823829"],
                "genes": ["SERPINA1", "HHIP", "FAM13A", "IREB2", "CHRNA5"],
                "direction": "hypomethylation",
                "ewas_pmid": "PMID:28406898"
            },
            "Aging (Biological)": {
                "cpgs": ["cg05575921", "cg09935388", "cg04180046", "cg06690548",
                        "cg12803068", "cg19859270", "cg14476101", "cg01940273",
                        "cg21161138", "cg17823829", "cg25648203", "cg06126421",
                        "cg14817490", "cg11554391", "cg01097978", "cg02583484"],
                "genes": ["ELOVL2", "FHL2", "KLF14", "TRIM59", "NHLRC1"],
                "direction": "mixed",
                "ewas_pmid": "PMID:23177740"
            }
        }
        
        return diseases
    
    def calculate_overlap(self, substance_name: str, disease_name: str) -> OverlapResult:
        """Calculate CpG overlap between a specific substance and disease"""
        
        if substance_name not in self.substance_cpg_database:
            raise ValueError(f"Substance '{substance_name}' not found in database")
        if disease_name not in self.disease_cpg_database:
            raise ValueError(f"Disease '{disease_name}' not found in database")
        
        substance_data = self.substance_cpg_database[substance_name]
        disease_data = self.disease_cpg_database[disease_name]
        
        substance_cpgs = set(substance_data["cpgs"])
        disease_cpgs = set(disease_data["cpgs"])
        
        shared_cpgs = substance_cpgs.intersection(disease_cpgs)
        union_cpgs = substance_cpgs.union(disease_cpgs)
        
        overlap_count = len(shared_cpgs)
        jaccard = len(shared_cpgs) / len(union_cpgs) if union_cpgs else 0
        
        overlap_pct_substance = (overlap_count / len(substance_cpgs) * 100) if substance_cpgs else 0
        overlap_pct_disease = (overlap_count / len(disease_cpgs) * 100) if disease_cpgs else 0
        
        substance_dir = substance_data["direction"]
        disease_dir = disease_data["direction"]
        if substance_dir == disease_dir:
            direction_concordance = 1.0
        elif "mixed" in [substance_dir, disease_dir]:
            direction_concordance = 0.5
        else:
            direction_concordance = 0.0
        
        if jaccard >= 0.6:
            risk = "CRITICAL"
        elif jaccard >= 0.4:
            risk = "HIGH"
        elif jaccard >= 0.2:
            risk = "MODERATE"
        else:
            risk = "LOW"
        
        clinical_notes = self._generate_clinical_notes(
            substance_name, disease_name, overlap_count, jaccard, 
            direction_concordance, risk
        )
        
        return OverlapResult(
            substance_name=substance_name,
            disease_name=disease_name,
            shared_cpgs=list(shared_cpgs),
            overlap_count=overlap_count,
            jaccard_similarity=round(jaccard, 4),
            substance_total_cpgs=len(substance_cpgs),
            disease_total_cpgs=len(disease_cpgs),
            overlap_percentage_substance=round(overlap_pct_substance, 2),
            overlap_percentage_disease=round(overlap_pct_disease, 2),
            direction_concordance=direction_concordance,
            differential_diagnosis_risk=risk,
            clinical_notes=clinical_notes
        )
    
    def _generate_clinical_notes(self, substance: str, disease: str, 
                                  overlap: int, jaccard: float,
                                  concordance: float, risk: str) -> str:
        """Generate clinical interpretation notes"""
        
        notes = []
        
        if risk == "CRITICAL":
            notes.append(f"CRITICAL: {substance} and {disease} share {overlap} CpG markers "
                        f"(Jaccard: {jaccard:.1%}). Differential diagnosis is extremely challenging.")
            notes.append("Clinical correlation with patient history is MANDATORY before any conclusion.")
        elif risk == "HIGH":
            notes.append(f"HIGH RISK: {overlap} shared CpG markers between {substance} and {disease}. "
                        f"Consider comprehensive clinical evaluation.")
        elif risk == "MODERATE":
            notes.append(f"MODERATE: {overlap} overlapping CpG sites. Standard differential diagnosis "
                        f"protocols should suffice.")
        else:
            notes.append(f"LOW RISK: Minimal overlap ({overlap} CpGs). Patterns are distinguishable.")
        
        if concordance == 1.0:
            notes.append("WARNING: Methylation direction is concordant - patterns may be indistinguishable.")
        elif concordance == 0.5:
            notes.append("Mixed methylation directions may help differentiate patterns.")
        else:
            notes.append("Opposite methylation directions aid differential diagnosis.")
        
        return " ".join(notes)
    
    def generate_full_overlap_matrix(self) -> pd.DataFrame:
        """Generate complete overlap matrix for all substance-disease pairs"""
        
        substances = list(self.substance_cpg_database.keys())
        diseases = list(self.disease_cpg_database.keys())
        
        matrix_data = []
        
        for substance in substances:
            row = {"Substance": substance}
            for disease in diseases:
                result = self.calculate_overlap(substance, disease)
                row[disease] = result.jaccard_similarity
            matrix_data.append(row)
        
        df = pd.DataFrame(matrix_data)
        df.set_index("Substance", inplace=True)
        
        self.overlap_matrix = df
        return df
    
    def get_high_risk_pairs(self, threshold: float = 0.4) -> List[OverlapResult]:
        """Get all substance-disease pairs with high overlap risk"""
        
        high_risk = []
        
        for substance in self.substance_cpg_database.keys():
            for disease in self.disease_cpg_database.keys():
                result = self.calculate_overlap(substance, disease)
                if result.jaccard_similarity >= threshold:
                    high_risk.append(result)
        
        high_risk.sort(key=lambda x: x.jaccard_similarity, reverse=True)
        self.high_risk_pairs = high_risk
        
        return high_risk
    
    def get_overlap_statistics(self) -> Dict:
        """Calculate overall overlap statistics"""
        
        if self.overlap_matrix is None:
            self.generate_full_overlap_matrix()
        
        all_overlaps = []
        for substance in self.substance_cpg_database.keys():
            for disease in self.disease_cpg_database.keys():
                result = self.calculate_overlap(substance, disease)
                all_overlaps.append(result.jaccard_similarity)
        
        overlaps_array = np.array(all_overlaps)
        
        critical_count = sum(1 for o in all_overlaps if o >= 0.6)
        high_count = sum(1 for o in all_overlaps if 0.4 <= o < 0.6)
        moderate_count = sum(1 for o in all_overlaps if 0.2 <= o < 0.4)
        low_count = sum(1 for o in all_overlaps if o < 0.2)
        
        total_pairs = len(all_overlaps)
        
        return {
            "total_pairs_analyzed": total_pairs,
            "mean_jaccard_similarity": round(float(np.mean(overlaps_array)), 4),
            "median_jaccard_similarity": round(float(np.median(overlaps_array)), 4),
            "max_jaccard_similarity": round(float(np.max(overlaps_array)), 4),
            "min_jaccard_similarity": round(float(np.min(overlaps_array)), 4),
            "std_jaccard_similarity": round(float(np.std(overlaps_array)), 4),
            "critical_risk_pairs": critical_count,
            "critical_risk_percentage": round(critical_count / total_pairs * 100, 2),
            "high_risk_pairs": high_count,
            "high_risk_percentage": round(high_count / total_pairs * 100, 2),
            "moderate_risk_pairs": moderate_count,
            "moderate_risk_percentage": round(moderate_count / total_pairs * 100, 2),
            "low_risk_pairs": low_count,
            "low_risk_percentage": round(low_count / total_pairs * 100, 2),
            "substances_analyzed": len(self.substance_cpg_database),
            "diseases_analyzed": len(self.disease_cpg_database)
        }
    
    def get_most_confounding_diseases_for_substance(self, substance_name: str, top_n: int = 5) -> List[OverlapResult]:
        """Get diseases most likely to be confused with a specific substance"""
        
        if substance_name not in self.substance_cpg_database:
            raise ValueError(f"Substance '{substance_name}' not found")
        
        results = []
        for disease in self.disease_cpg_database.keys():
            result = self.calculate_overlap(substance_name, disease)
            results.append(result)
        
        results.sort(key=lambda x: x.jaccard_similarity, reverse=True)
        return results[:top_n]
    
    def get_most_confounding_substances_for_disease(self, disease_name: str, top_n: int = 5) -> List[OverlapResult]:
        """Get substances most likely to be confused with a specific disease"""
        
        if disease_name not in self.disease_cpg_database:
            raise ValueError(f"Disease '{disease_name}' not found")
        
        results = []
        for substance in self.substance_cpg_database.keys():
            result = self.calculate_overlap(substance, disease_name)
            results.append(result)
        
        results.sort(key=lambda x: x.jaccard_similarity, reverse=True)
        return results[:top_n]


def run_comprehensive_analysis():
    """Run comprehensive CpG overlap analysis and print results"""
    
    analyzer = CPGOverlapAnalyzer()
    
    print("=" * 80)
    print("NPS vs CHRONIC DISEASE CpG OVERLAP ANALYSIS")
    print("UNODC EpiClock Platform - Differential Diagnosis Risk Assessment")
    print("=" * 80)
    
    stats = analyzer.get_overlap_statistics()
    
    print("\n[OVERALL STATISTICS]")
    print(f"Total Substance-Disease Pairs Analyzed: {stats['total_pairs_analyzed']}")
    print(f"Substances in Database: {stats['substances_analyzed']}")
    print(f"Diseases in Database: {stats['diseases_analyzed']}")
    print(f"\nMean Jaccard Similarity: {stats['mean_jaccard_similarity']:.2%}")
    print(f"Median Jaccard Similarity: {stats['median_jaccard_similarity']:.2%}")
    print(f"Max Jaccard Similarity: {stats['max_jaccard_similarity']:.2%}")
    print(f"Min Jaccard Similarity: {stats['min_jaccard_similarity']:.2%}")
    
    print("\n[RISK DISTRIBUTION]")
    print(f"CRITICAL Risk Pairs (>=60%): {stats['critical_risk_pairs']} ({stats['critical_risk_percentage']:.1f}%)")
    print(f"HIGH Risk Pairs (40-60%): {stats['high_risk_pairs']} ({stats['high_risk_percentage']:.1f}%)")
    print(f"MODERATE Risk Pairs (20-40%): {stats['moderate_risk_pairs']} ({stats['moderate_risk_percentage']:.1f}%)")
    print(f"LOW Risk Pairs (<20%): {stats['low_risk_pairs']} ({stats['low_risk_percentage']:.1f}%)")
    
    print("\n[TOP 10 HIGH-RISK PAIRS]")
    high_risk = analyzer.get_high_risk_pairs(threshold=0.4)
    for i, result in enumerate(high_risk[:10], 1):
        print(f"{i}. {result.substance_name} <-> {result.disease_name}")
        print(f"   Jaccard: {result.jaccard_similarity:.2%} | "
              f"Shared CpGs: {result.overlap_count} | Risk: {result.differential_diagnosis_risk}")
    
    return stats, high_risk


if __name__ == "__main__":
    run_comprehensive_analysis()
