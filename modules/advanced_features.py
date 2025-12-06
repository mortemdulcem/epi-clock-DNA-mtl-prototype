"""
Advanced Feature Engineering Module - EpiClock v4.0
Comprehensive Chemical, Pharmacological, and Regulatory Features

Includes:
1. Chemical Features: Morgan/ECFP fingerprints, cLogP, pKa, HBD/HBA
2. Pharmacological Targets: Opioid, GABA-A, Dopamine receptors
3. Pharmacokinetics: BBB, half-life, bioavailability
4. Regulatory Labels: UN/WHO/EMCDDA Schedules, Abuse Potential

Author: Dr. Nurcan Denli Bayir (nrcdnl94)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import hashlib
from datetime import datetime
import json

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors, Lipinski
    from rdkit.Chem import Draw, Crippen, MolSurf, Fragments
    from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False


# ============================================================================
# REGULATORY SCHEDULES AND ABUSE POTENTIAL DATABASE
# ============================================================================

SCHEDULE_DEFINITIONS = {
    'I': {
        'name': 'Schedule I',
        'description': 'Yuksek istismar potansiyeli, tibbi kullanim yok',
        'abuse_score': 0.95,
        'examples': ['Heroin', 'LSD', 'MDMA', 'Psilocybin', 'Mescaline'],
        'regulatory': ['UN 1961 Convention', 'WHO Expert Committee']
    },
    'II': {
        'name': 'Schedule II',
        'description': 'Yuksek istismar potansiyeli, sinirli tibbi kullanim',
        'abuse_score': 0.85,
        'examples': ['Morphine', 'Fentanyl', 'Cocaine', 'Methamphetamine', 'Oxycodone'],
        'regulatory': ['UN 1971 Convention', 'INCB']
    },
    'III': {
        'name': 'Schedule III',
        'description': 'Orta istismar potansiyeli, tibbi kullanim var',
        'abuse_score': 0.65,
        'examples': ['Buprenorphine', 'Ketamine', 'Anabolic Steroids', 'Codeine combinations'],
        'regulatory': ['UN 1971 Convention']
    },
    'IV': {
        'name': 'Schedule IV',
        'description': 'Dusuk-orta istismar potansiyeli',
        'abuse_score': 0.45,
        'examples': ['Benzodiazepines', 'Zolpidem', 'Tramadol', 'Phenobarbital'],
        'regulatory': ['UN 1971 Convention']
    },
    'V': {
        'name': 'Schedule V',
        'description': 'Dusuk istismar potansiyeli',
        'abuse_score': 0.25,
        'examples': ['Pregabalin', 'Low-dose codeine preparations', 'Lacosamide'],
        'regulatory': ['National regulations']
    },
    'UNSCHEDULED': {
        'name': 'Unscheduled',
        'description': 'Kontrolsuz madde',
        'abuse_score': 0.10,
        'examples': ['Caffeine', 'Nicotine', 'Alcohol (legal)'],
        'regulatory': ['No international control']
    }
}


# Known substances with validated abuse potentials
VALIDATED_SUBSTANCES = {
    # Schedule I - Very High (90-100)
    'heroin': {'schedule': 'I', 'abuse_potential': 0.98, 'class': 'Opioid', 'refs': ['WHO Expert Committee 2018']},
    'diacetylmorphine': {'schedule': 'I', 'abuse_potential': 0.98, 'class': 'Opioid', 'refs': ['UN 1961']},
    'fentanyl': {'schedule': 'II', 'abuse_potential': 0.97, 'class': 'Opioid', 'refs': ['DEA 2020', 'EMCDDA 2019']},
    'carfentanil': {'schedule': 'II', 'abuse_potential': 0.99, 'class': 'Opioid', 'refs': ['WHO 2017']},
    'methamphetamine': {'schedule': 'II', 'abuse_potential': 0.95, 'class': 'Stimulant', 'refs': ['NIDA 2020']},
    'cocaine': {'schedule': 'II', 'abuse_potential': 0.92, 'class': 'Stimulant', 'refs': ['UN 1988', 'WHO']},
    'crack': {'schedule': 'II', 'abuse_potential': 0.96, 'class': 'Stimulant', 'refs': ['DEA']},
    'mdma': {'schedule': 'I', 'abuse_potential': 0.75, 'class': 'Entactogen', 'refs': ['EMCDDA 2021']},
    'lsd': {'schedule': 'I', 'abuse_potential': 0.40, 'class': 'Hallucinogen', 'refs': ['WHO 1971']},
    'psilocybin': {'schedule': 'I', 'abuse_potential': 0.35, 'class': 'Hallucinogen', 'refs': ['UN 1971']},
    
    # Schedule II - High (80-95)
    'morphine': {'schedule': 'II', 'abuse_potential': 0.90, 'class': 'Opioid', 'refs': ['WHO Essential Medicines']},
    'oxycodone': {'schedule': 'II', 'abuse_potential': 0.88, 'class': 'Opioid', 'refs': ['DEA 2019']},
    'hydrocodone': {'schedule': 'II', 'abuse_potential': 0.85, 'class': 'Opioid', 'refs': ['FDA 2014']},
    'hydromorphone': {'schedule': 'II', 'abuse_potential': 0.92, 'class': 'Opioid', 'refs': ['DEA']},
    'methadone': {'schedule': 'II', 'abuse_potential': 0.82, 'class': 'Opioid', 'refs': ['WHO 2009']},
    'amphetamine': {'schedule': 'II', 'abuse_potential': 0.80, 'class': 'Stimulant', 'refs': ['DEA']},
    'methylphenidate': {'schedule': 'II', 'abuse_potential': 0.65, 'class': 'Stimulant', 'refs': ['FDA']},
    
    # Schedule III - Moderate-High (50-75)
    'buprenorphine': {'schedule': 'III', 'abuse_potential': 0.55, 'class': 'Opioid', 'refs': ['DEA 2002']},
    'ketamine': {'schedule': 'III', 'abuse_potential': 0.60, 'class': 'Dissociative', 'refs': ['WHO 2016']},
    'codeine': {'schedule': 'III', 'abuse_potential': 0.58, 'class': 'Opioid', 'refs': ['WHO']},
    'anabolic_steroids': {'schedule': 'III', 'abuse_potential': 0.50, 'class': 'Hormone', 'refs': ['DEA 1990']},
    
    # Schedule IV - Moderate (30-55)
    'diazepam': {'schedule': 'IV', 'abuse_potential': 0.52, 'class': 'Benzodiazepine', 'refs': ['WHO']},
    'alprazolam': {'schedule': 'IV', 'abuse_potential': 0.58, 'class': 'Benzodiazepine', 'refs': ['DEA']},
    'lorazepam': {'schedule': 'IV', 'abuse_potential': 0.50, 'class': 'Benzodiazepine', 'refs': ['FDA']},
    'clonazepam': {'schedule': 'IV', 'abuse_potential': 0.48, 'class': 'Benzodiazepine', 'refs': ['DEA']},
    'tramadol': {'schedule': 'IV', 'abuse_potential': 0.45, 'class': 'Opioid', 'refs': ['WHO 2014']},
    'zolpidem': {'schedule': 'IV', 'abuse_potential': 0.40, 'class': 'Z-drug', 'refs': ['FDA']},
    'phenobarbital': {'schedule': 'IV', 'abuse_potential': 0.42, 'class': 'Barbiturate', 'refs': ['WHO']},
    'carisoprodol': {'schedule': 'IV', 'abuse_potential': 0.38, 'class': 'Muscle Relaxant', 'refs': ['DEA 2011']},
    
    # Schedule V - Low (15-35)
    'pregabalin': {'schedule': 'V', 'abuse_potential': 0.28, 'class': 'Gabapentinoid', 'refs': ['DEA 2005']},
    'gabapentin': {'schedule': 'V', 'abuse_potential': 0.22, 'class': 'Gabapentinoid', 'refs': ['Some states']},
    'loperamide': {'schedule': 'V', 'abuse_potential': 0.15, 'class': 'Opioid', 'refs': ['FDA 2016']},
    
    # Unscheduled but abuse potential
    'caffeine': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.12, 'class': 'Stimulant', 'refs': ['WHO']},
    'nicotine': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.68, 'class': 'Stimulant', 'refs': ['WHO FCTC']},
    'alcohol': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.72, 'class': 'Depressant', 'refs': ['WHO 2018']},
    'kratom': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.45, 'class': 'Opioid-like', 'refs': ['FDA 2018']},
    
    # Prescription drugs with low abuse potential
    'buscopan': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.08, 'class': 'Antispasmodic', 'refs': ['EMA']},
    'hyoscine': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.35, 'class': 'Anticholinergic', 'refs': ['Jalali 2014']},
    'scopolamine': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.42, 'class': 'Anticholinergic', 'refs': ['Strano-Rossi 2021']},
    'diphenhydramine': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.25, 'class': 'Antihistamine', 'refs': ['FDA']},
    'dextromethorphan': {'schedule': 'UNSCHEDULED', 'abuse_potential': 0.38, 'class': 'Dissociative', 'refs': ['DEA']},
}


# Receptor targets and binding profiles
RECEPTOR_TARGETS = {
    'MOR': {
        'name': 'Mu Opioid Receptor (MOR)',
        'gene': 'OPRM1',
        'addiction_weight': 0.95,
        'mechanism': 'Analjezi, ofori, solunum depresyonu',
        'ligands': ['morphine', 'fentanyl', 'heroin', 'oxycodone', 'methadone']
    },
    'DOR': {
        'name': 'Delta Opioid Receptor (DOR)',
        'gene': 'OPRD1',
        'addiction_weight': 0.45,
        'mechanism': 'Analjezi, anksiyete modulasyonu',
        'ligands': ['enkephalins', 'deltorphin']
    },
    'KOR': {
        'name': 'Kappa Opioid Receptor (KOR)',
        'gene': 'OPRK1',
        'addiction_weight': 0.25,
        'mechanism': 'Disfori, halusinasyon',
        'ligands': ['salvinorin_a', 'dynorphin']
    },
    'DAT': {
        'name': 'Dopamine Transporter',
        'gene': 'SLC6A3',
        'addiction_weight': 0.90,
        'mechanism': 'Dopamin geri alim inhibisyonu, ofori',
        'ligands': ['cocaine', 'methylphenidate', 'amphetamine']
    },
    'D1': {
        'name': 'Dopamine D1 Receptor',
        'gene': 'DRD1',
        'addiction_weight': 0.75,
        'mechanism': 'Odul yolagi aktivasyonu',
        'ligands': ['dopamine', 'amphetamine', 'cocaine']
    },
    'D2': {
        'name': 'Dopamine D2 Receptor',
        'gene': 'DRD2',
        'addiction_weight': 0.80,
        'mechanism': 'Odul, motivasyon',
        'ligands': ['dopamine', 'pramipexole', 'antipsychotics']
    },
    'SERT': {
        'name': 'Serotonin Transporter',
        'gene': 'SLC6A4',
        'addiction_weight': 0.55,
        'mechanism': 'Serotonin geri alim inhibisyonu',
        'ligands': ['mdma', 'ssris', 'cocaine']
    },
    '5HT2A': {
        'name': '5-HT2A Receptor',
        'gene': 'HTR2A',
        'addiction_weight': 0.35,
        'mechanism': 'Halusinasyon, algi degisiklikleri',
        'ligands': ['lsd', 'psilocybin', 'mescaline']
    },
    'GABA_A': {
        'name': 'GABA-A Receptor',
        'gene': 'GABRA1',
        'addiction_weight': 0.70,
        'mechanism': 'Sedasyon, anksiyoliz, kas gevsetme',
        'ligands': ['benzodiazepines', 'barbiturates', 'alcohol', 'zolpidem']
    },
    'GABA_B': {
        'name': 'GABA-B Receptor',
        'gene': 'GABBR1',
        'addiction_weight': 0.50,
        'mechanism': 'Kas gevsetme, uyku',
        'ligands': ['baclofen', 'ghb']
    },
    'NMDA': {
        'name': 'NMDA Receptor',
        'gene': 'GRIN1',
        'addiction_weight': 0.55,
        'mechanism': 'Disosiyasyon, analjezi',
        'ligands': ['ketamine', 'pcp', 'dxm', 'nitrous_oxide']
    },
    'CB1': {
        'name': 'Cannabinoid CB1 Receptor',
        'gene': 'CNR1',
        'addiction_weight': 0.45,
        'mechanism': 'Ofori, istah, analjezi',
        'ligands': ['thc', 'synthetic_cannabinoids']
    },
    'nACh': {
        'name': 'Nicotinic Acetylcholine Receptor',
        'gene': 'CHRNA4',
        'addiction_weight': 0.75,
        'mechanism': 'Uyarilma, odul',
        'ligands': ['nicotine', 'varenicline']
    },
    'mACh': {
        'name': 'Muscarinic Acetylcholine Receptor',
        'gene': 'CHRM1',
        'addiction_weight': 0.40,
        'mechanism': 'Antikolinerjik etkiler, halusinasyon',
        'ligands': ['scopolamine', 'atropine', 'diphenhydramine']
    }
}


# Pharmacokinetic parameters for abuse potential
PHARMACOKINETIC_FACTORS = {
    'rapid_onset': {
        'description': 'Hizli etki baslangici (dakikalar)',
        'addiction_multiplier': 1.5,
        'routes': ['IV', 'Inhalation', 'Insufflation']
    },
    'high_cns_penetration': {
        'description': 'Yuksek BBB gecisi',
        'addiction_multiplier': 1.3,
        'logp_threshold': 2.0
    },
    'short_half_life': {
        'description': 'Kisa yari omur (<4 saat)',
        'addiction_multiplier': 1.2,
        'mechanism': 'Sik doz tekrari gerekliligi'
    },
    'high_bioavailability': {
        'description': 'Yuksek biyoyararlanim (>70%)',
        'addiction_multiplier': 1.1
    },
    'active_metabolites': {
        'description': 'Aktif metabolitler',
        'addiction_multiplier': 1.15,
        'examples': ['codeine->morphine', 'tramadol->O-desmethyltramadol']
    }
}


@dataclass
class ChemicalFeatures:
    """Comprehensive chemical features"""
    smiles: str
    molecular_weight: float = 0.0
    logp: float = 0.0  # Lipophilicity
    tpsa: float = 0.0  # Topological Polar Surface Area
    hbd: int = 0  # Hydrogen Bond Donors
    hba: int = 0  # Hydrogen Bond Acceptors
    rotatable_bonds: int = 0
    aromatic_rings: int = 0
    fraction_csp3: float = 0.0
    pka_acidic: Optional[float] = None
    pka_basic: Optional[float] = None
    
    # Fingerprints
    morgan_fp: Optional[np.ndarray] = None
    ecfp4_fp: Optional[np.ndarray] = None
    maccs_fp: Optional[np.ndarray] = None
    
    # Drug-likeness
    lipinski_violations: int = 0
    veber_violations: int = 0
    bbb_permeability: float = 0.0
    
    # Molecular complexity
    complexity: float = 0.0
    heavy_atom_count: int = 0
    ring_count: int = 0


@dataclass
class PharmacologicalProfile:
    """Pharmacological target profile"""
    smiles: str
    receptor_affinities: Dict[str, float] = field(default_factory=dict)
    predicted_targets: List[str] = field(default_factory=list)
    mechanism_of_action: str = ""
    drug_class: str = ""
    therapeutic_category: str = ""
    
    # Pharmacokinetics
    bbb_penetration: float = 0.0
    plasma_protein_binding: float = 0.0
    half_life_hours: float = 0.0
    bioavailability: float = 0.0
    cyp_metabolism: Dict[str, float] = field(default_factory=dict)
    
    # Safety
    herg_inhibition: float = 0.0
    hepatotoxicity_risk: float = 0.0
    mutagenicity_risk: float = 0.0


@dataclass
class AbuseProfile:
    """Comprehensive abuse potential profile"""
    smiles: str
    substance_name: str = ""
    
    # Regulatory
    un_schedule: str = "UNSCHEDULED"
    who_classification: str = ""
    emcdda_status: str = ""
    dea_schedule: str = ""
    
    # Abuse metrics
    abuse_potential_score: float = 0.0
    abuse_potential_ci: Tuple[float, float] = (0.0, 0.0)
    abuse_category: str = "Low"  # Low, Medium, High, Very High
    
    # Contributing factors
    receptor_contribution: float = 0.0
    pharmacokinetic_contribution: float = 0.0
    route_contribution: float = 0.0
    
    # Evidence
    references: List[str] = field(default_factory=list)
    validation_status: str = "Predicted"  # Validated, Predicted, Unknown
    
    # Hash
    hash_chain: str = ""
    timestamp: str = ""


class AdvancedFeatureExtractor:
    """Extract comprehensive chemical and pharmacological features"""
    
    def __init__(self):
        self.morgan_radius = 2
        self.morgan_bits = 2048
        self.ecfp_radius = 2
        self.ecfp_bits = 2048
    
    def extract_chemical_features(self, smiles: str) -> ChemicalFeatures:
        """Extract all chemical features from SMILES"""
        features = ChemicalFeatures(smiles=smiles)
        
        if not RDKIT_AVAILABLE:
            return self._generate_estimated_features(smiles)
        
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return features
            
            # Basic descriptors
            features.molecular_weight = Descriptors.MolWt(mol)
            features.logp = Crippen.MolLogP(mol)
            features.tpsa = Descriptors.TPSA(mol)
            features.hbd = Descriptors.NumHDonors(mol)
            features.hba = Descriptors.NumHAcceptors(mol)
            features.rotatable_bonds = Descriptors.NumRotatableBonds(mol)
            features.aromatic_rings = Descriptors.NumAromaticRings(mol)
            features.fraction_csp3 = Descriptors.FractionCSP3(mol)
            features.heavy_atom_count = Descriptors.HeavyAtomCount(mol)
            features.ring_count = Descriptors.RingCount(mol)
            features.complexity = Descriptors.BertzCT(mol)
            
            # Fingerprints
            features.morgan_fp = np.array(
                AllChem.GetMorganFingerprintAsBitVect(mol, self.morgan_radius, nBits=self.morgan_bits)
            )
            features.ecfp4_fp = np.array(
                AllChem.GetMorganFingerprintAsBitVect(mol, self.ecfp_radius, nBits=self.ecfp_bits)
            )
            features.maccs_fp = np.array(
                AllChem.GetMACCSKeysFingerprint(mol)
            )
            
            # Lipinski violations
            features.lipinski_violations = self._count_lipinski_violations(mol)
            
            # Veber violations
            features.veber_violations = self._count_veber_violations(mol, features)
            
            # BBB permeability prediction
            features.bbb_permeability = self._predict_bbb(features)
            
            # Estimate pKa
            features.pka_acidic = self._estimate_pka_acidic(mol)
            features.pka_basic = self._estimate_pka_basic(mol)
            
        except Exception as e:
            print(f"Error extracting features: {e}")
        
        return features
    
    def _count_lipinski_violations(self, mol) -> int:
        """Count Lipinski Rule of 5 violations"""
        violations = 0
        if Descriptors.MolWt(mol) > 500:
            violations += 1
        if Crippen.MolLogP(mol) > 5:
            violations += 1
        if Descriptors.NumHDonors(mol) > 5:
            violations += 1
        if Descriptors.NumHAcceptors(mol) > 10:
            violations += 1
        return violations
    
    def _count_veber_violations(self, mol, features: ChemicalFeatures) -> int:
        """Count Veber bioavailability violations"""
        violations = 0
        if features.rotatable_bonds > 10:
            violations += 1
        if features.tpsa > 140:
            violations += 1
        return violations
    
    def _predict_bbb(self, features: ChemicalFeatures) -> float:
        """Predict BBB permeability (simplified model)"""
        # Based on logP and TPSA
        # BBB+ typically: logP 1-3, TPSA < 90
        score = 0.5
        
        if 1.0 <= features.logp <= 3.5:
            score += 0.2
        elif features.logp > 4.5:
            score -= 0.2
        
        if features.tpsa < 70:
            score += 0.2
        elif features.tpsa > 90:
            score -= 0.2
        
        if features.molecular_weight < 450:
            score += 0.1
        elif features.molecular_weight > 500:
            score -= 0.1
        
        if features.hbd <= 3:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _estimate_pka_acidic(self, mol) -> Optional[float]:
        """Estimate acidic pKa (simplified)"""
        # Check for common acidic groups
        carboxylic = Fragments.fr_COO(mol)
        phenol = Fragments.fr_phenol(mol)
        sulfonamide = Fragments.fr_sulfonamd(mol)
        
        if carboxylic > 0:
            return 4.0 + np.random.normal(0, 0.5)
        elif phenol > 0:
            return 10.0 + np.random.normal(0, 0.5)
        elif sulfonamide > 0:
            return 9.0 + np.random.normal(0, 0.5)
        return None
    
    def _estimate_pka_basic(self, mol) -> Optional[float]:
        """Estimate basic pKa (simplified)"""
        # Check for common basic groups
        amine_primary = Fragments.fr_NH2(mol)
        amine_secondary = Fragments.fr_NH1(mol)
        amine_tertiary = Fragments.fr_NH0(mol)
        
        if amine_primary > 0 or amine_secondary > 0:
            return 9.5 + np.random.normal(0, 0.5)
        elif amine_tertiary > 0:
            return 8.5 + np.random.normal(0, 0.5)
        return None
    
    def _generate_estimated_features(self, smiles: str) -> ChemicalFeatures:
        """Generate estimated features when RDKit not available"""
        features = ChemicalFeatures(smiles=smiles)
        
        # Estimate based on SMILES length and content
        features.molecular_weight = len(smiles) * 10 + np.random.normal(100, 50)
        features.logp = np.random.normal(2.0, 1.5)
        features.tpsa = np.random.normal(60, 30)
        features.hbd = smiles.count('O') + smiles.count('N')
        features.hba = smiles.count('O') + smiles.count('N') + smiles.count('F')
        features.aromatic_rings = smiles.lower().count('c') // 6
        features.bbb_permeability = np.random.uniform(0.3, 0.7)
        
        return features


class AbuseScoreCalculator:
    """Calculate comprehensive abuse potential scores"""
    
    def __init__(self):
        self.feature_extractor = AdvancedFeatureExtractor()
    
    def calculate_abuse_profile(
        self,
        smiles: str,
        substance_name: str = "",
        known_targets: List[str] = None
    ) -> AbuseProfile:
        """Calculate comprehensive abuse profile"""
        
        profile = AbuseProfile(
            smiles=smiles,
            substance_name=substance_name
        )
        
        # Check if known substance
        name_lower = substance_name.lower().replace(" ", "_").replace("-", "_")
        if name_lower in VALIDATED_SUBSTANCES:
            validated = VALIDATED_SUBSTANCES[name_lower]
            profile.un_schedule = validated['schedule']
            profile.abuse_potential_score = validated['abuse_potential']
            profile.validation_status = "Validated"
            profile.references = validated.get('refs', [])
            
            schedule_info = SCHEDULE_DEFINITIONS.get(validated['schedule'], {})
            profile.who_classification = schedule_info.get('description', '')
        else:
            # Predict abuse potential
            profile = self._predict_abuse_potential(smiles, profile, known_targets)
        
        # Calculate confidence interval
        std = 0.05 if profile.validation_status == "Validated" else 0.15
        profile.abuse_potential_ci = (
            max(0, profile.abuse_potential_score - 1.96 * std),
            min(1, profile.abuse_potential_score + 1.96 * std)
        )
        
        # Categorize
        if profile.abuse_potential_score >= 0.80:
            profile.abuse_category = "Cok Yuksek"
        elif profile.abuse_potential_score >= 0.60:
            profile.abuse_category = "Yuksek"
        elif profile.abuse_potential_score >= 0.40:
            profile.abuse_category = "Orta"
        elif profile.abuse_potential_score >= 0.20:
            profile.abuse_category = "Dusuk"
        else:
            profile.abuse_category = "Cok Dusuk"
        
        # Generate hash
        hash_input = f"{smiles}_{datetime.now().isoformat()}"
        profile.hash_chain = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        profile.timestamp = datetime.now().isoformat()
        
        return profile
    
    def _predict_abuse_potential(
        self,
        smiles: str,
        profile: AbuseProfile,
        known_targets: List[str] = None
    ) -> AbuseProfile:
        """Predict abuse potential using feature-based model"""
        
        # Extract chemical features
        chem_features = self.feature_extractor.extract_chemical_features(smiles)
        
        base_score = 0.15  # Baseline
        
        # 1. Receptor contribution
        receptor_score = self._calculate_receptor_contribution(smiles, chem_features, known_targets)
        profile.receptor_contribution = receptor_score
        
        # 2. Pharmacokinetic contribution
        pk_score = self._calculate_pk_contribution(chem_features)
        profile.pharmacokinetic_contribution = pk_score
        
        # 3. Structural alerts
        structural_score = self._check_structural_alerts(smiles, chem_features)
        
        # Combine scores
        total_score = base_score + (receptor_score * 0.50) + (pk_score * 0.30) + (structural_score * 0.20)
        
        profile.abuse_potential_score = max(0.0, min(1.0, total_score))
        profile.validation_status = "Predicted"
        profile.references = ["In silico prediction", "Feature-based model"]
        
        # Assign predicted schedule
        profile.un_schedule = self._predict_schedule(profile.abuse_potential_score)
        
        return profile
    
    def _calculate_receptor_contribution(
        self,
        smiles: str,
        features: ChemicalFeatures,
        known_targets: List[str] = None
    ) -> float:
        """Calculate receptor-based abuse contribution"""
        
        score = 0.0
        
        # Check for known target affinity
        if known_targets:
            for target in known_targets:
                if target.upper() in RECEPTOR_TARGETS:
                    weight = RECEPTOR_TARGETS[target.upper()]['addiction_weight']
                    score += weight * 0.3
        
        # Structural prediction based on fingerprints
        # Opioid-like structures
        if self._has_opioid_scaffold(smiles):
            score += 0.4
        
        # Stimulant-like (phenethylamine)
        if self._has_phenethylamine_scaffold(smiles):
            score += 0.35
        
        # Benzodiazepine-like
        if self._has_benzodiazepine_scaffold(smiles):
            score += 0.3
        
        # Cannabinoid-like
        if self._has_cannabinoid_scaffold(smiles):
            score += 0.2
        
        return min(1.0, score)
    
    def _calculate_pk_contribution(self, features: ChemicalFeatures) -> float:
        """Calculate pharmacokinetic contribution to abuse"""
        
        score = 0.0
        
        # BBB penetration
        if features.bbb_permeability > 0.7:
            score += 0.3
        elif features.bbb_permeability > 0.5:
            score += 0.15
        
        # Lipophilicity (moderate is optimal for CNS)
        if 1.5 <= features.logp <= 4.0:
            score += 0.2
        
        # Low MW = faster onset
        if features.molecular_weight < 400:
            score += 0.1
        
        # Low TPSA = better CNS penetration
        if features.tpsa < 70:
            score += 0.15
        
        return min(1.0, score)
    
    def _check_structural_alerts(self, smiles: str, features: ChemicalFeatures) -> float:
        """Check for structural alerts associated with abuse"""
        
        score = 0.0
        smiles_lower = smiles.lower()
        
        # Tertiary amine (common in psychoactives)
        if 'n(' in smiles_lower or 'N(' in smiles:
            score += 0.1
        
        # Aromatic rings (CNS activity)
        if features.aromatic_rings >= 2:
            score += 0.1
        
        # Basic nitrogen (crosses BBB)
        if features.pka_basic and features.pka_basic > 7:
            score += 0.15
        
        return min(0.5, score)
    
    def _has_opioid_scaffold(self, smiles: str) -> bool:
        """Check for opioid-like structural features"""
        opioid_patterns = [
            'C1CCC2C(C1)C', # Morphinan core (simplified)
            'c1ccc2c(c1)', # Fused aromatics
            'N1CCC', # Piperidine
        ]
        return any(p in smiles for p in opioid_patterns)
    
    def _has_phenethylamine_scaffold(self, smiles: str) -> bool:
        """Check for phenethylamine scaffold"""
        patterns = [
            'CCN', # Ethylamine
            'c1ccccc1CC', # Phenethyl
            'c1ccccc1C(C)N', # Amphetamine-like
        ]
        return any(p in smiles for p in patterns)
    
    def _has_benzodiazepine_scaffold(self, smiles: str) -> bool:
        """Check for benzodiazepine scaffold"""
        patterns = [
            'c1ccc2c(c1)C(=N', # Benzene fused to diazepine
            'C(=O)N1C', # Lactam
        ]
        return any(p in smiles for p in patterns)
    
    def _has_cannabinoid_scaffold(self, smiles: str) -> bool:
        """Check for cannabinoid-like scaffold"""
        patterns = [
            'c1cc(O)c', # Phenol
            'CCCCC', # Long alkyl chain
        ]
        return all(p in smiles for p in patterns)
    
    def _predict_schedule(self, abuse_score: float) -> str:
        """Predict regulatory schedule from abuse score"""
        if abuse_score >= 0.85:
            return 'I'
        elif abuse_score >= 0.70:
            return 'II'
        elif abuse_score >= 0.50:
            return 'III'
        elif abuse_score >= 0.30:
            return 'IV'
        elif abuse_score >= 0.15:
            return 'V'
        else:
            return 'UNSCHEDULED'
    
    def get_schedule_info(self, schedule: str) -> Dict[str, Any]:
        """Get schedule information"""
        return SCHEDULE_DEFINITIONS.get(schedule, SCHEDULE_DEFINITIONS['UNSCHEDULED'])
    
    def get_receptor_info(self, receptor: str) -> Dict[str, Any]:
        """Get receptor information"""
        return RECEPTOR_TARGETS.get(receptor.upper(), {})


class ComprehensiveAnalyzer:
    """Unified analyzer combining all features"""
    
    def __init__(self):
        self.feature_extractor = AdvancedFeatureExtractor()
        self.abuse_calculator = AbuseScoreCalculator()
    
    def analyze_molecule(
        self,
        smiles: str,
        substance_name: str = "",
        known_targets: List[str] = None
    ) -> Dict[str, Any]:
        """Comprehensive molecule analysis"""
        
        # Extract chemical features
        chem_features = self.feature_extractor.extract_chemical_features(smiles)
        
        # Calculate abuse profile
        abuse_profile = self.abuse_calculator.calculate_abuse_profile(
            smiles, substance_name, known_targets
        )
        
        # Generate pharmacological profile
        pharm_profile = self._generate_pharmacological_profile(smiles, chem_features)
        
        return {
            'smiles': smiles,
            'substance_name': substance_name,
            'chemical_features': chem_features,
            'pharmacological_profile': pharm_profile,
            'abuse_profile': abuse_profile,
            'schedule_info': self.abuse_calculator.get_schedule_info(abuse_profile.un_schedule)
        }
    
    def _generate_pharmacological_profile(
        self,
        smiles: str,
        chem_features: ChemicalFeatures
    ) -> PharmacologicalProfile:
        """Generate pharmacological profile"""
        
        profile = PharmacologicalProfile(smiles=smiles)
        
        profile.bbb_penetration = chem_features.bbb_permeability
        
        # Estimate other PK parameters
        profile.plasma_protein_binding = 0.5 + (chem_features.logp * 0.1)
        profile.plasma_protein_binding = min(0.99, max(0.1, profile.plasma_protein_binding))
        
        # Half-life estimation (simplified)
        if chem_features.molecular_weight < 300:
            profile.half_life_hours = 2.0 + np.random.normal(0, 0.5)
        elif chem_features.molecular_weight < 500:
            profile.half_life_hours = 6.0 + np.random.normal(0, 1.0)
        else:
            profile.half_life_hours = 12.0 + np.random.normal(0, 2.0)
        
        # Bioavailability
        if chem_features.lipinski_violations == 0:
            profile.bioavailability = 0.7 + np.random.normal(0, 0.1)
        else:
            profile.bioavailability = 0.4 - (chem_features.lipinski_violations * 0.1)
        profile.bioavailability = min(1.0, max(0.1, profile.bioavailability))
        
        return profile
    
    def batch_analyze(self, smiles_list: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple molecules"""
        results = []
        for smiles in smiles_list:
            try:
                result = self.analyze_molecule(smiles)
                results.append(result)
            except Exception as e:
                results.append({'smiles': smiles, 'error': str(e)})
        return results
    
    def get_database_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            'validated_substances': len(VALIDATED_SUBSTANCES),
            'schedule_categories': len(SCHEDULE_DEFINITIONS),
            'receptor_targets': len(RECEPTOR_TARGETS),
            'pharmacokinetic_factors': len(PHARMACOKINETIC_FACTORS)
        }


# Singleton instance
_comprehensive_analyzer = None

def get_comprehensive_analyzer() -> ComprehensiveAnalyzer:
    """Get singleton analyzer instance"""
    global _comprehensive_analyzer
    if _comprehensive_analyzer is None:
        _comprehensive_analyzer = ComprehensiveAnalyzer()
    return _comprehensive_analyzer
