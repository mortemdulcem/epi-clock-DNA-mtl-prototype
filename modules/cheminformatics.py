# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Chemoinformatics Module for EpiClock Platform
Molecular structure analysis, similarity search, and variant detection

Features:
- PubChem integration (111M+ compounds)
- SMILES/InChI molecular structures
- Molecular fingerprints (Morgan/ECFP)
- Tanimoto similarity analysis
- Structural analog/variant detection
- Metabolite prediction
"""

import pubchempy as pcp
import requests
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from functools import lru_cache
import hashlib

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
# nrcdnl94
class MolecularData:
    # nrcdnl94
    """Molecular structure data for a substance"""
    substance_key: str
    name_tr: str
    name_en: str
    pubchem_cid: Optional[int] = None
    smiles: Optional[str] = None
    smiles_isomeric: Optional[str] = None
    inchi: Optional[str] = None
    inchi_key: Optional[str] = None
    molecular_formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    xlogp: Optional[float] = None
    hbond_donor: Optional[int] = None
    hbond_acceptor: Optional[int] = None
    rotatable_bonds: Optional[int] = None
    tpsa: Optional[float] = None  # Topological Polar Surface Area
    complexity: Optional[float] = None
    charge: Optional[int] = None
    synonyms: List[str] = field(default_factory=list)
    pharmacological_class: Optional[str] = None
    dea_schedule: Optional[str] = None

@dataclass 
# nrcdnl94
class SimilarityResult:
    # nrcdnl94
    """Result of molecular similarity search"""
    query_substance: str
    similar_cid: int
    similar_name: str
    similar_smiles: str
    tanimoto_score: float
    molecular_weight: Optional[float] = None

@dataclass
# nrcdnl94
class MetaboliteResult:
    # nrcdnl94
    """Predicted metabolite information"""
    parent_substance: str
    metabolite_name: str
    reaction_type: str  # oxidation, reduction, hydrolysis, conjugation
    metabolite_smiles: Optional[str] = None
    metabolite_cid: Optional[int] = None
    enzyme: Optional[str] = None  # CYP3A4, CYP2D6, etc.
    probability: float = 0.5

# ============================================================================
# KNOWN SUBSTANCE SMILES DATABASE (Pre-cached for speed)
# ============================================================================

KNOWN_SUBSTANCE_SMILES = {
    # nrcdnl94
    # Opioids
    'heroin': ('CC(=O)Oc1ccc2CC3C(C=Cc12)C(OC(C)=O)C4N(C)CCC34', 5462328, 'Diacetylmorphine'),
    'morphine': ('CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O', 5288826, 'Morphine'),
    'codeine': ('CN1CCC23C4C1CC5=C2C(=C(C=C5)OC)OC3C(C=C4)O', 2833, 'Codeine'),
    'fentanyl': ('CCC(=O)N(C1CCN(CC1)CCC2=CC=CC=C2)C3=CC=CC=C3', 3345, 'Fentanyl'),
    'oxycodone': ('CN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)OC)O4)O', 5284603, 'Oxycodone'),
    'methadone': ('CCC(=O)C(CC(C)N(C)C)(C1=CC=CC=C1)C2=CC=CC=C2', 4095, 'Methadone'),
    'hydrocodone': ('CN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)OC)O4)O', 5284569, 'Hydrocodone'),
    'tramadol': ('CN(C)CC1CCCCC1(C2=CC(=CC=C2)OC)O', 33741, 'Tramadol'),
    'buprenorphine': ('CC(C)(C)C(=O)OC1C2CCC3(C4C1(CCN2CC5CC5)C=CC6=C3C(=C(C=C6)O)O4)OC', 644073, 'Buprenorphine'),
    
    # Stimulants
    'cocaine': ('CN1C2CCC1C(C(C2)OC(=O)C3=CC=CC=C3)C(=O)OC', 446220, 'Cocaine'),
    'methamphetamine': ('CC(CC1=CC=CC=C1)NC', 1206, 'Methamphetamine'),
    'amphetamine': ('CC(CC1=CC=CC=C1)N', 3007, 'Amphetamine'),
    'mdma': ('CC(CC1=CC2=C(C=C1)OCO2)NC', 1615, 'MDMA'),
    'methylphenidate': ('COC(=O)C(C1CCCCN1)C2=CC=CC=C2', 4158, 'Methylphenidate'),
    
    # Depressants
    'alcohol': ('CCO', 702, 'Ethanol'),
    'ethanol': ('CCO', 702, 'Ethanol'),
    'ghb': ('OCCCC(=O)O', 10413, 'Gamma-Hydroxybutyric acid'),
    'diazepam': ('CN1C(=O)CN=C(C2=C1C=CC(=C2)Cl)C3=CC=CC=C3', 3016, 'Diazepam'),
    'alprazolam': ('CC1=NN=C2N1C3=C(C=C(C=C3)Cl)C(=NC2)C4=CC=CC=C4', 2118, 'Alprazolam'),
    'clonazepam': ('C1C(=O)NC2=C(C=C(C=C2)[N+](=O)[O-])C(=N1)C3=CC=CC=C3Cl', 2802, 'Clonazepam'),
    'lorazepam': ('C1=CC=C(C=C1)C2=NC(C(=O)NC3=C2C=C(C=C3)Cl)O)Cl', 3958, 'Lorazepam'),
    'phenobarbital': ('CCC1(C(=O)NC(=O)NC1=O)C2=CC=CC=C2', 4763, 'Phenobarbital'),
    
    # Cannabinoids
    'thc': ('CCCCCC1=CC(=C2C3C=C(CCC3C(OC2=C1)(C)C)C)O', 16078, 'Delta-9-THC'),
    'cannabis': ('CCCCCC1=CC(=C2C3C=C(CCC3C(OC2=C1)(C)C)C)O', 16078, 'Delta-9-THC'),
    'cbd': ('CCCCCC1=CC(=C(C(=C1)O)C2C=C(CCC2C(=C)C)C)O', 644019, 'Cannabidiol'),
    'synthetic_cannabinoid': ('CCCCCF.Cc1cc(C)c2c(c1)c1ccccc1n2CC(=O)N', 44148157, 'JWH-018'),
    
    # Hallucinogens
    'lsd': ('CCN(CC)C(=O)C1CN(C2CC3=CNC4=CC=CC(=C34)C2=C1)C', 5761, 'LSD'),
    'psilocybin': ('CN(C)CCC1=CNC2=C1C=C(C=C2)OP(=O)(O)O', 10624, 'Psilocybin'),
    'psilocin': ('CN(C)CCC1=CNC2=C1C=C(C=C2)O', 4980, 'Psilocin'),
    'dmt': ('CN(C)CCC1=CNC2=CC=CC=C21', 6089, 'DMT'),
    'mescaline': ('COC1=CC(=CC(=C1OC)OC)CCN', 4076, 'Mescaline'),
    'ketamine': ('CNC1(CCCCC1=O)C2=CC=CC=C2Cl', 3821, 'Ketamine'),
    'pcp': ('C1CCC(CC1)(C2=CC=CC=C2)N3CCCCC3', 6468, 'PCP'),
    
    # Tobacco/Nicotine
    'tobacco': ('CN1CCCC1C2=CN=CC=C2', 89594, 'Nicotine'),
    'nicotine': ('CN1CCCC1C2=CN=CC=C2', 89594, 'Nicotine'),
    
    # Inhalants
    'toluene': ('CC1=CC=CC=C1', 1140, 'Toluene'),
    'butane': ('CCCC', 7843, 'Butane'),
    'nitrous_oxide': ('N=N=O', 948, 'Nitrous oxide'),
    
    # Designer Drugs / NPS
    'bath_salts': ('CCCC(C(=O)C1=CC=C(C=C1)OC)NC', 11148955, 'Mephedrone'),
    'mephedrone': ('CCCC(C(=O)C1=CC=C(C=C1)OC)NC', 11148955, 'Mephedrone'),
    'flakka': ('CCCC(C(=O)C1=CC=C(C=C1)F)NC2CCCCC2', 71741891, 'Alpha-PVP'),
    'spice': ('CCCCCF.Cc1cc(C)c2c(c1)c1ccccc1n2CC(=O)N', 44148157, 'JWH-018'),
    
    # Anabolic Steroids
    'testosterone': ('CC12CCC3C(C1CCC2O)CCC4=CC(=O)CCC34C', 6013, 'Testosterone'),
    'nandrolone': ('CC12CCC3C(C1CCC2O)CCC4=CC(=O)CCC34', 9904, 'Nandrolone'),
    'stanozolol': ('CC12C(CC3C1(CCC4C3CCC5=CC(=O)CCC45C)C)N=C(N2)C', 25249, 'Stanozolol'),
    
    # Prescription Drugs (commonly abused)
    'oxycontin': ('CN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)OC)O4)O', 5284603, 'Oxycodone'),
    'adderall': ('CC(CC1=CC=CC=C1)N', 3007, 'Amphetamine'),
    'xanax': ('CC1=NN=C2N1C3=C(C=C(C=C3)Cl)C(=NC2)C4=CC=CC=C4', 2118, 'Alprazolam'),
    'valium': ('CN1C(=O)CN=C(C2=C1C=CC(=C2)Cl)C3=CC=CC=C3', 3016, 'Diazepam'),
    'vicodin': ('CN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)OC)O4)O', 5284569, 'Hydrocodone'),
    'percocet': ('CN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)OC)O4)O', 5284603, 'Oxycodone'),
    
    # Caffeine
    'caffeine': ('CN1C=NC2=C1C(=O)N(C(=O)N2C)C', 2519, 'Caffeine'),
}

# ============================================================================
# METABOLITE PATHWAYS DATABASE
# ============================================================================

METABOLITE_PATHWAYS = {
    # nrcdnl94
    'heroin': [
        {'name': '6-Monoacetylmorphine', 'reaction': 'hydrolysis', 'enzyme': 'Esterases', 'cid': 5462501},
        {'name': 'Morphine', 'reaction': 'hydrolysis', 'enzyme': 'Esterases', 'cid': 5288826},
        {'name': 'Morphine-3-glucuronide', 'reaction': 'conjugation', 'enzyme': 'UGT2B7', 'cid': 5487896},
        {'name': 'Morphine-6-glucuronide', 'reaction': 'conjugation', 'enzyme': 'UGT2B7', 'cid': 5360621},
    ],
    'cocaine': [
        {'name': 'Benzoylecgonine', 'reaction': 'hydrolysis', 'enzyme': 'Carboxylesterases', 'cid': 2349},
        {'name': 'Ecgonine methyl ester', 'reaction': 'hydrolysis', 'enzyme': 'Carboxylesterases', 'cid': 247919},
        {'name': 'Norcocaine', 'reaction': 'N-demethylation', 'enzyme': 'CYP3A4', 'cid': 65056},
    ],
    'methamphetamine': [
        {'name': 'Amphetamine', 'reaction': 'N-demethylation', 'enzyme': 'CYP2D6', 'cid': 3007},
        {'name': '4-Hydroxymethamphetamine', 'reaction': 'hydroxylation', 'enzyme': 'CYP2D6', 'cid': 36604},
        {'name': 'Norephedrine', 'reaction': 'beta-hydroxylation', 'enzyme': 'Dopamine beta-hydroxylase', 'cid': 26934},
    ],
    'thc': [
        {'name': '11-Hydroxy-THC', 'reaction': 'hydroxylation', 'enzyme': 'CYP2C9/CYP3A4', 'cid': 37482},
        {'name': '11-nor-9-carboxy-THC', 'reaction': 'oxidation', 'enzyme': 'ADH/ALDH', 'cid': 107885},
        {'name': 'THC-glucuronide', 'reaction': 'conjugation', 'enzyme': 'UGT1A9', 'cid': None},
    ],
    'fentanyl': [
        {'name': 'Norfentanyl', 'reaction': 'N-dealkylation', 'enzyme': 'CYP3A4', 'cid': 62276},
        {'name': 'Hydroxyfentanyl', 'reaction': 'hydroxylation', 'enzyme': 'CYP3A4', 'cid': None},
        {'name': 'Despropionylfentanyl', 'reaction': 'amide hydrolysis', 'enzyme': 'Amidases', 'cid': None},
    ],
    'alcohol': [
        {'name': 'Acetaldehyde', 'reaction': 'oxidation', 'enzyme': 'ADH', 'cid': 177},
        {'name': 'Acetic acid', 'reaction': 'oxidation', 'enzyme': 'ALDH', 'cid': 176},
        {'name': 'Ethyl glucuronide', 'reaction': 'conjugation', 'enzyme': 'UGT', 'cid': 441403},
        {'name': 'Ethyl sulfate', 'reaction': 'conjugation', 'enzyme': 'SULT', 'cid': 6992086},
    ],
    'nicotine': [
        {'name': 'Cotinine', 'reaction': 'oxidation', 'enzyme': 'CYP2A6', 'cid': 854019},
        {'name': 'Trans-3-hydroxycotinine', 'reaction': 'hydroxylation', 'enzyme': 'CYP2A6', 'cid': 5311381},
        {'name': 'Nicotine-N-oxide', 'reaction': 'N-oxidation', 'enzyme': 'FMO3', 'cid': 72307},
        {'name': 'Nornicotine', 'reaction': 'N-demethylation', 'enzyme': 'CYP2B6', 'cid': 412},
    ],
    'mdma': [
        {'name': 'MDA', 'reaction': 'N-demethylation', 'enzyme': 'CYP2D6', 'cid': 1614},
        {'name': 'HMMA', 'reaction': 'O-demethylation', 'enzyme': 'CYP2D6', 'cid': 126851},
        {'name': 'HMA', 'reaction': 'O-demethylation', 'enzyme': 'CYP2D6', 'cid': 160552},
    ],
    'diazepam': [
        {'name': 'Nordiazepam', 'reaction': 'N-demethylation', 'enzyme': 'CYP3A4/CYP2C19', 'cid': 2997},
        {'name': 'Temazepam', 'reaction': 'hydroxylation', 'enzyme': 'CYP3A4', 'cid': 5391},
        {'name': 'Oxazepam', 'reaction': 'hydroxylation', 'enzyme': 'CYP3A4', 'cid': 4616},
    ],
}

# ============================================================================
# CHEMOINFORMATICS ENGINE
# ============================================================================

class ChemoinformaticsEngine:
    # nrcdnl94
    """
    Chemoinformatics analysis engine for substance molecular data
    """
    
    def __init__(self):
        self.known_smiles = KNOWN_SUBSTANCE_SMILES
        self.metabolite_db = METABOLITE_PATHWAYS
        self.cache: Dict[str, MolecularData] = {}
        self._api_delay = 0.3  # PubChem rate limit
    
    def _rate_limit(self):
        """Respect PubChem API rate limits"""
        time.sleep(self._api_delay)
    
    @lru_cache(maxsize=500)
    def get_pubchem_data(self, substance_name: str) -> Optional[Dict]:
        """Fetch molecular data from PubChem"""
        try:
            # First check known database
            key = substance_name.lower().replace(' ', '_').replace('-', '_')
            if key in self.known_smiles:
                smiles, cid, name = self.known_smiles[key]
                return {
                    'cid': cid,
                    'smiles': smiles,
                    'name': name,
                    'source': 'local_cache'
                }
            
            # Query PubChem
            self._rate_limit()
            compounds = pcp.get_compounds(substance_name, 'name')
            
            if compounds:
                comp = compounds[0]
                return {
                    'cid': comp.cid,
                    'smiles': comp.canonical_smiles,
                    'smiles_isomeric': comp.isomeric_smiles,
                    'inchi': comp.inchi,
                    'inchi_key': comp.inchikey,
                    'molecular_formula': comp.molecular_formula,
                    'molecular_weight': comp.molecular_weight,
                    'xlogp': comp.xlogp,
                    'hbond_donor': comp.h_bond_donor_count,
                    'hbond_acceptor': comp.h_bond_acceptor_count,
                    'rotatable_bonds': comp.rotatable_bond_count,
                    'tpsa': comp.tpsa,
                    'complexity': comp.complexity,
                    'charge': comp.charge,
                    'synonyms': comp.synonyms[:10] if comp.synonyms else [],
                    'source': 'pubchem_api'
                }
        except Exception as e:
            print(f"PubChem query error for {substance_name}: {e}")
        
        return None
    
    def get_molecular_data(self, substance_key: str, name_tr: str, name_en: str) -> MolecularData:
        """Get complete molecular data for a substance"""
        
        # Check cache first
        if substance_key in self.cache:
            return self.cache[substance_key]
        
        # Check known database
        key = substance_key.lower().replace(' ', '_').replace('-', '_')
        
        if key in self.known_smiles:
            smiles, cid, name = self.known_smiles[key]
            
            mol_data = MolecularData(
                substance_key=substance_key,
                name_tr=name_tr,
                name_en=name_en,
                pubchem_cid=cid,
                smiles=smiles
            )
            
            # Try to get additional data from PubChem
            try:
                pubchem_data = self.get_pubchem_data(name_en)
                if pubchem_data:
                    mol_data.molecular_formula = pubchem_data.get('molecular_formula')
                    mol_data.molecular_weight = pubchem_data.get('molecular_weight')
                    mol_data.xlogp = pubchem_data.get('xlogp')
                    mol_data.inchi = pubchem_data.get('inchi')
                    mol_data.inchi_key = pubchem_data.get('inchi_key')
                    mol_data.tpsa = pubchem_data.get('tpsa')
                    mol_data.complexity = pubchem_data.get('complexity')
            except:
                pass
            
            self.cache[substance_key] = mol_data
            return mol_data
        
        # Query PubChem for unknown substances
        pubchem_data = self.get_pubchem_data(name_en)
        
        if pubchem_data:
            mol_data = MolecularData(
                substance_key=substance_key,
                name_tr=name_tr,
                name_en=name_en,
                pubchem_cid=pubchem_data.get('cid'),
                smiles=pubchem_data.get('smiles'),
                smiles_isomeric=pubchem_data.get('smiles_isomeric'),
                inchi=pubchem_data.get('inchi'),
                inchi_key=pubchem_data.get('inchi_key'),
                molecular_formula=pubchem_data.get('molecular_formula'),
                molecular_weight=pubchem_data.get('molecular_weight'),
                xlogp=pubchem_data.get('xlogp'),
                hbond_donor=pubchem_data.get('hbond_donor'),
                hbond_acceptor=pubchem_data.get('hbond_acceptor'),
                rotatable_bonds=pubchem_data.get('rotatable_bonds'),
                tpsa=pubchem_data.get('tpsa'),
                complexity=pubchem_data.get('complexity'),
                charge=pubchem_data.get('charge'),
                synonyms=pubchem_data.get('synonyms', [])
            )
            self.cache[substance_key] = mol_data
            return mol_data
        
        # Return minimal data if nothing found
        return MolecularData(
            substance_key=substance_key,
            name_tr=name_tr,
            name_en=name_en
        )
    
    def calculate_tanimoto_similarity(self, smiles1: str, smiles2: str) -> float:
        """
        Calculate Tanimoto similarity between two SMILES strings
        Uses character-based fingerprint as fallback (no RDKit dependency)
        """
        if not smiles1 or not smiles2:
            return 0.0
        
        # Character n-gram based fingerprint
        def get_ngram_fingerprint(smiles: str, n: int = 3) -> set:
            """Generate character n-grams as fingerprint"""
            ngrams = set()
            for i in range(len(smiles) - n + 1):
                ngrams.add(smiles[i:i+n])
            return ngrams
        
        fp1 = get_ngram_fingerprint(smiles1)
        fp2 = get_ngram_fingerprint(smiles2)
        
        # Tanimoto = intersection / union
        intersection = len(fp1 & fp2)
        union = len(fp1 | fp2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def find_similar_compounds(self, query_smiles: str, threshold: float = 0.6, max_results: int = 20) -> List[SimilarityResult]:
        """Find similar compounds in the known database"""
        results = []
        
        for key, (smiles, cid, name) in self.known_smiles.items():
            similarity = self.calculate_tanimoto_similarity(query_smiles, smiles)
            
            if similarity >= threshold:
                results.append(SimilarityResult(
                    query_substance=key,
                    similar_cid=cid,
                    similar_name=name,
                    similar_smiles=smiles,
                    tanimoto_score=similarity
                ))
        
        # Sort by similarity score
        results.sort(key=lambda x: x.tanimoto_score, reverse=True)
        return results[:max_results]
    
    def get_metabolites(self, substance_key: str) -> List[MetaboliteResult]:
        """Get known metabolites for a substance"""
        key = substance_key.lower().replace(' ', '_').replace('-', '_')
        
        metabolites = []
        
        if key in self.metabolite_db:
            for met in self.metabolite_db[key]:
                metabolites.append(MetaboliteResult(
                    parent_substance=substance_key,
                    metabolite_name=met['name'],
                    metabolite_cid=met.get('cid'),
                    reaction_type=met['reaction'],
                    enzyme=met.get('enzyme'),
                    probability=0.9 if met.get('cid') else 0.7
                ))
        
        return metabolites
    
    def search_pubchem_similar(self, cid: int, threshold: int = 90, max_results: int = 50) -> List[Dict]:
        """Search PubChem for similar compounds by 2D similarity"""
        try:
            self._rate_limit()
            
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/{cid}/cids/JSON?Threshold={threshold}&MaxRecords={max_results}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                similar_cids = data.get('IdentifierList', {}).get('CID', [])
                
                # Get basic info for similar compounds
                results = []
                for sim_cid in similar_cids[:max_results]:
                    try:
                        self._rate_limit()
                        comp = pcp.Compound.from_cid(sim_cid)
                        results.append({
                            'cid': sim_cid,
                            'name': comp.iupac_name or f"CID {sim_cid}",
                            'smiles': comp.canonical_smiles,
                            'molecular_weight': comp.molecular_weight
                        })
                    except:
                        continue
                
                return results
        except Exception as e:
            print(f"PubChem similarity search error: {e}")
        
        return []
    
    def get_structural_variants(self, substance_key: str, include_pubchem: bool = False) -> Dict[str, Any]:
        """
        Get structural variants, analogs, and related compounds
        """
        key = substance_key.lower().replace(' ', '_').replace('-', '_')
        
        result = {
            'substance': substance_key,
            'smiles': None,
            'cid': None,
            'local_variants': [],
            'metabolites': [],
            'pubchem_similar': []
        }
        
        # Get base compound data
        if key in self.known_smiles:
            smiles, cid, name = self.known_smiles[key]
            result['smiles'] = smiles
            result['cid'] = cid
            
            # Find local similar compounds
            similar = self.find_similar_compounds(smiles, threshold=0.4)
            result['local_variants'] = [
                {
                    'name': s.similar_name,
                    'cid': s.similar_cid,
                    'smiles': s.similar_smiles,
                    'similarity': round(s.tanimoto_score, 3)
                }
                for s in similar if s.similar_name != name
            ]
            
            # Get metabolites
            metabolites = self.get_metabolites(substance_key)
            result['metabolites'] = [
                {
                    'name': m.metabolite_name,
                    'cid': m.metabolite_cid,
                    'reaction': m.reaction_type,
                    'enzyme': m.enzyme
                }
                for m in metabolites
            ]
            
            # Search PubChem for more variants
            if include_pubchem and cid:
                result['pubchem_similar'] = self.search_pubchem_similar(cid, threshold=85, max_results=20)
        
        return result
    
    def generate_molecular_report(self, substance_key: str, name_tr: str, name_en: str) -> Dict[str, Any]:
        """Generate comprehensive molecular report"""
        
        mol_data = self.get_molecular_data(substance_key, name_tr, name_en)
        variants = self.get_structural_variants(substance_key, include_pubchem=False)
        metabolites = self.get_metabolites(substance_key)
        
        return {
            'substance': {
                'key': substance_key,
                'name_tr': name_tr,
                'name_en': name_en
            },
            'molecular_data': {
                'pubchem_cid': mol_data.pubchem_cid,
                'smiles': mol_data.smiles,
                'inchi': mol_data.inchi,
                'inchi_key': mol_data.inchi_key,
                'molecular_formula': mol_data.molecular_formula,
                'molecular_weight': mol_data.molecular_weight,
                'xlogp': mol_data.xlogp,
                'tpsa': mol_data.tpsa,
                'complexity': mol_data.complexity,
                'hbond_donor': mol_data.hbond_donor,
                'hbond_acceptor': mol_data.hbond_acceptor
            },
            'variants': variants['local_variants'],
            'metabolites': [
                {
                    'name': m.metabolite_name,
                    'reaction': m.reaction_type,
                    'enzyme': m.enzyme,
                    'cid': m.metabolite_cid
                }
                for m in metabolites
            ],
            'variant_count': len(variants['local_variants']),
            'metabolite_count': len(metabolites)
        }

# ============================================================================
# BATCH PROCESSING
# ============================================================================

def process_substance_batch(substances: List[Dict], engine: ChemoinformaticsEngine = None) -> List[Dict]:
    """Process multiple substances for molecular data"""
    if engine is None:
        engine = ChemoinformaticsEngine()
    
    results = []
    for sub in substances:
        key = sub.get('key', sub.get('substance_key', ''))
        name_tr = sub.get('name_tr', sub.get('substance_name_tr', ''))
        name_en = sub.get('name_en', sub.get('substance_name_en', ''))
        
        report = engine.generate_molecular_report(key, name_tr, name_en)
        results.append(report)
    
    return results

# ============================================================================
# STATISTICS
# ============================================================================

def get_cheminformatics_stats() -> Dict[str, Any]:
    """Get chemoinformatics database statistics"""
    return {
        'known_substances_with_smiles': len(KNOWN_SUBSTANCE_SMILES),
        'substances_with_metabolites': len(METABOLITE_PATHWAYS),
        'total_known_metabolites': sum(len(m) for m in METABOLITE_PATHWAYS.values()),
        'pubchem_integration': True,
        'similarity_algorithm': 'Tanimoto (n-gram fingerprint)',
        'categories': {
            'opioids': len([k for k in KNOWN_SUBSTANCE_SMILES if 'morphine' in k or 'codeine' in k or 'fentanyl' in k or 'heroin' in k or 'oxycodone' in k or 'methadone' in k]),
            'stimulants': len([k for k in KNOWN_SUBSTANCE_SMILES if 'cocaine' in k or 'amphetamine' in k or 'methamphetamine' in k or 'mdma' in k]),
            'depressants': len([k for k in KNOWN_SUBSTANCE_SMILES if 'diazepam' in k or 'alprazolam' in k or 'alcohol' in k or 'ghb' in k]),
            'cannabinoids': len([k for k in KNOWN_SUBSTANCE_SMILES if 'thc' in k or 'cannabis' in k or 'cbd' in k]),
            'hallucinogens': len([k for k in KNOWN_SUBSTANCE_SMILES if 'lsd' in k or 'psilocybin' in k or 'dmt' in k or 'ketamine' in k]),
        }
    }

# ============================================================================
# QUICK ACCESS FUNCTIONS
# ============================================================================

def get_smiles(substance_name: str) -> Optional[str]:
    """Quick function to get SMILES for a substance"""
    engine = ChemoinformaticsEngine()
    data = engine.get_pubchem_data(substance_name)
    return data.get('smiles') if data else None

def get_similar_substances(substance_name: str, threshold: float = 0.5) -> List[Dict]:
    """Quick function to find similar substances"""
    engine = ChemoinformaticsEngine()
    key = substance_name.lower().replace(' ', '_').replace('-', '_')
    
    if key in engine.known_smiles:
        smiles = engine.known_smiles[key][0]
        similar = engine.find_similar_compounds(smiles, threshold)
        return [
            {'name': s.similar_name, 'cid': s.similar_cid, 'similarity': round(s.tanimoto_score, 3)}
            for s in similar
        ]
    return []

def get_metabolites_quick(substance_name: str) -> List[Dict]:
    """Quick function to get metabolites"""
    engine = ChemoinformaticsEngine()
    metabolites = engine.get_metabolites(substance_name)
    return [
        {'name': m.metabolite_name, 'reaction': m.reaction_type, 'enzyme': m.enzyme}
        for m in metabolites
    ]


# End of module - # nrcdnl94