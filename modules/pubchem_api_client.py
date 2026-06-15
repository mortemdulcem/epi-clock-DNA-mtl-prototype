"""
PubChem API Client
==================

Otomatik olarak PubChem'den kimyasal yapilar ve ilac bilgileri ceker.

PubChem: https://pubchem.ncbi.nlm.nih.gov/
- 100+ milyon bilesik
- Kimyasal yapilar, ozellikler
- Biyoaktivite verileri
- Ucretsiz erisim

Author: EpiClock Team
Version: 1.0
"""

import requests
import time
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import hashlib


@dataclass
class PubChemCompound:
    """PubChem bilesik bilgileri"""
    cid: int
    name: str
    iupac_name: Optional[str]
    molecular_formula: Optional[str]
    molecular_weight: Optional[float]
    canonical_smiles: Optional[str]
    inchi: Optional[str]
    inchikey: Optional[str]
    xlogp: Optional[float]
    complexity: Optional[float]
    h_bond_donor_count: Optional[int]
    h_bond_acceptor_count: Optional[int]
    rotatable_bond_count: Optional[int]
    is_drug: bool = False
    drug_class: Optional[str] = None


@dataclass
class DrugInfo:
    """Ilac bilgileri"""
    cid: int
    name: str
    drug_class: str
    mechanism: Optional[str]
    indications: List[str]
    side_effects: List[str]
    target_genes: List[str]
    pharmacokinetics: Optional[Dict]


class PubChemAPI:
    """
    PubChem PUG REST API Client
    
    https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
    """
    
    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    
    # Bilinen ilac siniflari
    DRUG_CLASSES = {
        'antipsychotic': ['haloperidol', 'risperidone', 'olanzapine', 'quetiapine', 'aripiprazole'],
        'antidepressant': ['fluoxetine', 'sertraline', 'citalopram', 'escitalopram', 'venlafaxine', 'duloxetine'],
        'anxiolytic': ['diazepam', 'lorazepam', 'alprazolam', 'clonazepam'],
        'opioid_analgesic': ['morphine', 'fentanyl', 'oxycodone', 'hydrocodone', 'tramadol', 'codeine'],
        'stimulant': ['methylphenidate', 'amphetamine', 'lisdexamfetamine'],
        'anticonvulsant': ['valproate', 'carbamazepine', 'lamotrigine', 'topiramate', 'gabapentin', 'pregabalin'],
        'retinoid': ['isotretinoin', 'tretinoin', 'acitretin', 'adapalene'],
        'immunosuppressant': ['methotrexate', 'cyclosporine', 'tacrolimus', 'mycophenolate'],
        'chemotherapy': ['cisplatin', 'doxorubicin', 'cyclophosphamide', 'methotrexate', 'fluorouracil'],
        'corticosteroid': ['prednisone', 'prednisolone', 'dexamethasone', 'hydrocortisone'],
        'statin': ['atorvastatin', 'simvastatin', 'rosuvastatin', 'pravastatin'],
        'antidiabetic': ['metformin', 'glipizide', 'glyburide', 'sitagliptin', 'pioglitazone'],
        'antihypertensive': ['lisinopril', 'amlodipine', 'losartan', 'metoprolol', 'atenolol'],
        'anticoagulant': ['warfarin', 'heparin', 'rivaroxaban', 'apixaban', 'dabigatran'],
        'antibiotic': ['amoxicillin', 'azithromycin', 'ciprofloxacin', 'doxycycline'],
        'nsaid': ['ibuprofen', 'naproxen', 'diclofenac', 'celecoxib'],
        'ppi': ['omeprazole', 'pantoprazole', 'esomeprazole', 'lansoprazole'],
    }
    
    # Bilinen bagimliliK yapici maddeler
    ADDICTIVE_SUBSTANCES = {
        'stimulant_abuse': ['cocaine', 'methamphetamine', 'amphetamine', 'mdma', 'cathinone', 'mephedrone'],
        'opioid_abuse': ['heroin', 'fentanyl', 'oxycodone', 'morphine', 'carfentanil'],
        'cannabinoid': ['thc', 'cannabis', 'synthetic cannabinoid', 'jwh-018', 'jwh-073'],
        'hallucinogen': ['lsd', 'psilocybin', 'dmt', 'mescaline', 'ketamine', 'pcp'],
        'depressant': ['ghb', 'barbiturate', 'benzodiazepine'],
        'inhalant': ['toluene', 'butane', 'nitrous oxide'],
    }
    
    def __init__(self, cache_dir: str = "data/pubchem_cache"):
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EpiClock/1.0 (Academic Research)',
            'Accept': 'application/json'
        })
        os.makedirs(cache_dir, exist_ok=True)
        
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms - PubChem allows 5 req/sec
        
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'api_calls': 0,
            'errors': 0
        }
    
    def _rate_limit(self):
        """Rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _get_cache_path(self, key: str) -> str:
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.json")
    
    def _get_cached(self, key: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    if time.time() - data.get('timestamp', 0) < 30 * 24 * 3600:  # 30 gun
                        self.stats['cache_hits'] += 1
                        return data.get('content')
            except:
                pass
        return None
    
    def _set_cache(self, key: str, content: Any):
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump({'timestamp': time.time(), 'content': content}, f)
        except:
            pass
    
    def _api_request(self, endpoint: str) -> Optional[Dict]:
        """API istegi"""
        self.stats['total_requests'] += 1
        
        cached = self._get_cached(endpoint)
        if cached is not None:
            return cached
        
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self._set_cache(endpoint, data)
            self.stats['api_calls'] += 1
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.stats['errors'] += 1
            return None
    
    def search_compound(self, name: str) -> Optional[int]:
        """
        Bilesik adi ile CID ara
        
        Args:
            name: Bilesik adi
        
        Returns:
            CID (Compound ID) veya None
        """
        endpoint = f"compound/name/{name}/cids/JSON"
        data = self._api_request(endpoint)
        
        if data and 'IdentifierList' in data:
            cids = data['IdentifierList'].get('CID', [])
            return cids[0] if cids else None
        return None
    
    def get_compound_properties(self, cid: int) -> Optional[PubChemCompound]:
        """
        Bilesik ozelliklerini getir
        
        Args:
            cid: PubChem Compound ID
        
        Returns:
            PubChemCompound objesi
        """
        properties = [
            'MolecularFormula', 'MolecularWeight', 'CanonicalSMILES',
            'InChI', 'InChIKey', 'XLogP', 'Complexity',
            'HBondDonorCount', 'HBondAcceptorCount', 'RotatableBondCount',
            'IUPACName'
        ]
        
        props_str = ','.join(properties)
        endpoint = f"compound/cid/{cid}/property/{props_str}/JSON"
        
        data = self._api_request(endpoint)
        
        if data and 'PropertyTable' in data:
            props = data['PropertyTable'].get('Properties', [{}])[0]
            
            # Ilac sinifini belirle
            name = self._get_compound_name(cid)
            drug_class = self._classify_compound(name.lower() if name else '')
            
            return PubChemCompound(
                cid=cid,
                name=name or f"CID{cid}",
                iupac_name=props.get('IUPACName'),
                molecular_formula=props.get('MolecularFormula'),
                molecular_weight=props.get('MolecularWeight'),
                canonical_smiles=props.get('CanonicalSMILES'),
                inchi=props.get('InChI'),
                inchikey=props.get('InChIKey'),
                xlogp=props.get('XLogP'),
                complexity=props.get('Complexity'),
                h_bond_donor_count=props.get('HBondDonorCount'),
                h_bond_acceptor_count=props.get('HBondAcceptorCount'),
                rotatable_bond_count=props.get('RotatableBondCount'),
                is_drug=drug_class is not None,
                drug_class=drug_class
            )
        
        return None
    
    def _get_compound_name(self, cid: int) -> Optional[str]:
        """Bilesik adini getir"""
        endpoint = f"compound/cid/{cid}/synonyms/JSON"
        data = self._api_request(endpoint)
        
        if data and 'InformationList' in data:
            info = data['InformationList'].get('Information', [{}])[0]
            synonyms = info.get('Synonym', [])
            return synonyms[0] if synonyms else None
        return None
    
    def _classify_compound(self, name: str) -> Optional[str]:
        """Bilesigi siniflandir"""
        name_lower = name.lower()
        
        # Ilac siniflari
        for drug_class, drugs in self.DRUG_CLASSES.items():
            for drug in drugs:
                if drug in name_lower:
                    return drug_class
        
        # Bagimlilik yapici maddeler
        for sub_class, substances in self.ADDICTIVE_SUBSTANCES.items():
            for sub in substances:
                if sub in name_lower:
                    return f"abuse:{sub_class}"
        
        return None
    
    def get_bioactivity_data(self, cid: int) -> List[Dict]:
        """
        Bilesik biyoaktivite verilerini getir
        
        Args:
            cid: PubChem Compound ID
        
        Returns:
            Biyoaktivite listesi
        """
        endpoint = f"compound/cid/{cid}/assaysummary/JSON"
        data = self._api_request(endpoint)
        
        activities = []
        
        if data and 'Table' in data:
            columns = data['Table'].get('Columns', {}).get('Column', [])
            rows = data['Table'].get('Row', [])
            
            for row in rows[:50]:  # Max 50 aktivite
                cells = row.get('Cell', [])
                if len(cells) >= len(columns):
                    activity = dict(zip(columns, cells))
                    activities.append(activity)
        
        return activities
    
    def get_drug_target_genes(self, cid: int) -> List[str]:
        """
        Ilacin hedef genlerini getir
        
        Args:
            cid: PubChem Compound ID
        
        Returns:
            Gen listesi
        """
        endpoint = f"compound/cid/{cid}/targets/ProteinGI,GeneSymbol/JSON"
        data = self._api_request(endpoint)
        
        genes = []
        
        if data and 'InformationList' in data:
            for info in data['InformationList'].get('Information', []):
                gene_symbols = info.get('GeneSymbol', [])
                genes.extend(gene_symbols)
        
        return list(set(genes))
    
    def search_drugs_by_class(self, drug_class: str) -> List[PubChemCompound]:
        """
        Ilac sinifina gore ilaclari ara
        
        Args:
            drug_class: Ilac sinifi
        
        Returns:
            Bilesik listesi
        """
        if drug_class not in self.DRUG_CLASSES:
            return []
        
        compounds = []
        
        for drug_name in self.DRUG_CLASSES[drug_class]:
            cid = self.search_compound(drug_name)
            if cid:
                compound = self.get_compound_properties(cid)
                if compound:
                    compound.drug_class = drug_class
                    compound.is_drug = True
                    compounds.append(compound)
        
        return compounds
    
    def build_therapeutic_database(self) -> Dict[str, List[PubChemCompound]]:
        """
        Tum terapotik ilac veritabanini olustur
        
        Returns:
            {drug_class: [compounds]} dictionary
        """
        print("Terapotik ilac veritabani olusturuluyor...")
        
        database = {}
        total_drugs = sum(len(drugs) for drugs in self.DRUG_CLASSES.values())
        processed = 0
        
        for drug_class, drug_names in self.DRUG_CLASSES.items():
            compounds = []
            
            for drug_name in drug_names:
                processed += 1
                print(f"[{processed}/{total_drugs}] {drug_name}...")
                
                cid = self.search_compound(drug_name)
                if cid:
                    compound = self.get_compound_properties(cid)
                    if compound:
                        compound.drug_class = drug_class
                        compound.is_drug = True
                        compounds.append(compound)
            
            if compounds:
                database[drug_class] = compounds
        
        print(f"\n{sum(len(c) for c in database.values())} ilac yuklendi")
        return database
    
    def build_substance_database(self) -> Dict[str, List[PubChemCompound]]:
        """
        Bagimlilik yapici madde veritabanini olustur
        
        Returns:
            {substance_class: [compounds]} dictionary
        """
        print("Madde veritabani olusturuluyor...")
        
        database = {}
        total_subs = sum(len(subs) for subs in self.ADDICTIVE_SUBSTANCES.values())
        processed = 0
        
        for sub_class, sub_names in self.ADDICTIVE_SUBSTANCES.items():
            compounds = []
            
            for sub_name in sub_names:
                processed += 1
                print(f"[{processed}/{total_subs}] {sub_name}...")
                
                cid = self.search_compound(sub_name)
                if cid:
                    compound = self.get_compound_properties(cid)
                    if compound:
                        compound.drug_class = f"abuse:{sub_class}"
                        compounds.append(compound)
            
            if compounds:
                database[sub_class] = compounds
        
        print(f"\n{sum(len(c) for c in database.values())} madde yuklendi")
        return database
    
    def get_statistics(self) -> Dict[str, Any]:
        """API istatistiklerini dondur"""
        return {
            **self.stats,
            'drug_classes': len(self.DRUG_CLASSES),
            'total_known_drugs': sum(len(d) for d in self.DRUG_CLASSES.values()),
            'substance_classes': len(self.ADDICTIVE_SUBSTANCES),
            'total_known_substances': sum(len(s) for s in self.ADDICTIVE_SUBSTANCES.values())
        }


class DrugBankLite:
    """
    DrugBank benzeri veriler (PubChem uzerinden)
    
    Ilac-gen-hastalık iliskilerini icerir
    """
    
    # Ilac-Gen-CpG iliskileri (literaturden)
    DRUG_GENE_CPG_MAP = {
        'isotretinoin': {
            'genes': ['RARA', 'RARB', 'RARG', 'RXR', 'CYP26A1'],
            'cpg_effects': {
                'cg12803068': 0.08,   # RARA
                'cg04983687': 0.06,   # RXR
                'cg23130731': 0.05,   # CYP26A1
            },
            'eaa_effect': 0.4,  # yillik EAA artisi
            'mechanism': 'Retinoid reseptor aktivasyonu'
        },
        'metformin': {
            'genes': ['AMPK', 'PRKAA1', 'PRKAA2', 'SLC22A1'],
            'cpg_effects': {
                'cg19693031': -0.03,  # TXNIP - azaltir
                'cg06500161': -0.02,  # CPT1A
            },
            'eaa_effect': -0.3,  # EAA azaltir
            'mechanism': 'AMPK aktivasyonu, mitokondri fonksiyonu'
        },
        'methotrexate': {
            'genes': ['DHFR', 'TYMS', 'MTHFR', 'FPGS'],
            'cpg_effects': {
                'cg00574958': 0.04,
                'cg22891070': 0.05,
            },
            'eaa_effect': 0.6,
            'mechanism': 'Folat antagonisti, DNA sentez inhibisyonu'
        },
        'fluoxetine': {
            'genes': ['SLC6A4', 'HTR1A', 'HTR2A', 'BDNF'],
            'cpg_effects': {
                'cg05575921': -0.02,  # SLC6A4
                'cg18800161': -0.03,  # HTR2A
            },
            'eaa_effect': -0.1,
            'mechanism': 'SSRI - serotonin geri alim inhibisyonu'
        },
        'haloperidol': {
            'genes': ['DRD2', 'DRD3', 'HTR2A', 'COMT'],
            'cpg_effects': {
                'cg14983602': 0.03,   # DRD2
                'cg03636183': 0.02,   # DRD4
            },
            'eaa_effect': 0.3,
            'mechanism': 'Dopamin D2 antagonisti'
        },
        'prednisone': {
            'genes': ['NR3C1', 'FKBP5', 'GILZ', 'IL6'],
            'cpg_effects': {
                'cg18849583': 0.05,   # NR3C1
                'cg20067310': 0.06,   # FKBP5
            },
            'eaa_effect': 0.8,
            'mechanism': 'Glukokortikoid reseptor aktivasyonu'
        },
        'atorvastatin': {
            'genes': ['HMGCR', 'LDLR', 'APOE', 'PCSK9'],
            'cpg_effects': {
                'cg06500161': -0.02,
                'cg00574958': -0.01,
            },
            'eaa_effect': -0.2,
            'mechanism': 'HMG-CoA reduktaz inhibisyonu'
        },
        'valproate': {
            'genes': ['HDAC1', 'HDAC2', 'GABA', 'SCN1A'],
            'cpg_effects': {
                'cg05575921': 0.04,
                'cg18849583': 0.03,
            },
            'eaa_effect': 0.4,
            'mechanism': 'HDAC inhibisyonu, GABA artisi'
        }
    }
    
    @classmethod
    def get_drug_info(cls, drug_name: str) -> Optional[Dict]:
        """Ilac bilgilerini getir"""
        drug_lower = drug_name.lower()
        return cls.DRUG_GENE_CPG_MAP.get(drug_lower)
    
    @classmethod
    def get_all_therapeutic_cpg_effects(cls) -> Dict[str, Dict]:
        """Tum terapotik ilac CpG etkilerini getir"""
        return cls.DRUG_GENE_CPG_MAP
    
    @classmethod
    def calculate_medication_eaa_effect(cls, medications: List[Dict]) -> float:
        """
        Toplam ilac EAA etkisini hesapla
        
        Args:
            medications: [{'name': 'drug', 'duration_years': 2}, ...]
        
        Returns:
            Toplam EAA degisimi
        """
        total_eaa = 0.0
        
        for med in medications:
            drug_info = cls.get_drug_info(med.get('name', ''))
            if drug_info:
                duration = med.get('duration_years', 1)
                eaa_effect = drug_info.get('eaa_effect', 0) * duration
                total_eaa += eaa_effect
        
        return total_eaa


# Global instance
_pubchem_api = None

def get_pubchem_api() -> PubChemAPI:
    """Global PubChem API instance"""
    global _pubchem_api
    if _pubchem_api is None:
        _pubchem_api = PubChemAPI()
    return _pubchem_api
