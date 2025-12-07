"""
EpiClock v4.0 - Genomic Database API Clients
Real-time data fetching from public genomic databases

Supported APIs:
- gnomAD (Genome Aggregation Database)
- GWAS Catalog (Genetic Associations)
- PubChem (Chemical/Substance Data)
- UniProt (Protein Data)
- NCBI Entrez (Gene Data)

Author: nrcdnl94
"""

import requests
import json
import time
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from functools import lru_cache
import os
import pickle

GNOMAD_API_URL = "https://gnomad.broadinstitute.org/api"
GWAS_CATALOG_API = "https://www.ebi.ac.uk/gwas/rest/api"
PUBCHEM_API = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
UNIPROT_API = "https://rest.uniprot.org"
NCBI_ENTREZ_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

CACHE_DIR = ".cache/genomic_data"
os.makedirs(CACHE_DIR, exist_ok=True)


@dataclass
class APIResponse:
    """Standardized API response"""
    success: bool
    data: Any
    source: str
    timestamp: str
    cache_hit: bool = False
    error_message: str = ""


@dataclass
class VariantData:
    """Genomic variant information"""
    variant_id: str
    chromosome: str
    position: int
    ref_allele: str
    alt_allele: str
    allele_frequency: float
    population_frequencies: Dict[str, float] = field(default_factory=dict)
    gene_symbol: str = ""
    consequence: str = ""
    clinical_significance: str = ""


@dataclass
class GWASAssociation:
    """GWAS association data"""
    study_id: str
    trait: str
    gene: str
    snp_id: str
    p_value: float
    odds_ratio: Optional[float] = None
    beta: Optional[float] = None
    sample_size: int = 0
    ancestry: str = ""


@dataclass
class SubstanceData:
    """Chemical substance data from PubChem"""
    cid: int
    name: str
    smiles: str
    molecular_formula: str
    molecular_weight: float
    iupac_name: str = ""
    synonyms: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneData:
    """Gene information from NCBI"""
    gene_id: str
    symbol: str
    name: str
    chromosome: str
    start_position: int
    end_position: int
    description: str = ""
    aliases: List[str] = field(default_factory=list)


class CacheManager:
    """Manage data caching for API responses"""
    
    def __init__(self, cache_dir: str = CACHE_DIR, ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        """Generate cache file path from key"""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.pkl")
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve cached data if valid"""
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    cached = pickle.load(f)
                if datetime.now() - cached['timestamp'] < self.ttl:
                    return cached['data']
            except Exception:
                pass
        return None
    
    def set(self, key: str, data: Any) -> None:
        """Cache data with timestamp"""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump({
                    'data': data,
                    'timestamp': datetime.now()
                }, f)
        except Exception:
            pass
    
    def clear(self) -> int:
        """Clear expired cache entries"""
        cleared = 0
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            try:
                with open(filepath, 'rb') as f:
                    cached = pickle.load(f)
                if datetime.now() - cached['timestamp'] >= self.ttl:
                    os.remove(filepath)
                    cleared += 1
            except Exception:
                pass
        return cleared


class GnomADClient:
    """Client for gnomAD GraphQL API"""
    
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        self.api_url = GNOMAD_API_URL
        self.cache = cache_manager or CacheManager()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def query_variant(self, variant_id: str, dataset: str = "gnomad_r4") -> APIResponse:
        """
        Query variant information from gnomAD
        
        Args:
            variant_id: Variant ID in format chr-pos-ref-alt (e.g., "1-55516888-G-A")
            dataset: gnomAD dataset version
        
        Returns:
            APIResponse with variant data
        """
        cache_key = f"gnomad_variant_{variant_id}_{dataset}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="gnomAD",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        query = """
        query VariantQuery($variantId: String!, $datasetId: DatasetId!) {
            variant(variantId: $variantId, dataset: $datasetId) {
                variant_id
                chrom
                pos
                ref
                alt
                exome {
                    ac
                    an
                    af
                    populations {
                        id
                        ac
                        an
                        af
                    }
                }
                genome {
                    ac
                    an
                    af
                    populations {
                        id
                        ac
                        an
                        af
                    }
                }
                transcript_consequences {
                    gene_symbol
                    consequence_terms
                }
            }
        }
        """
        
        try:
            response = self.session.post(
                self.api_url,
                json={
                    'query': query,
                    'variables': {
                        'variantId': variant_id,
                        'datasetId': dataset
                    }
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                return APIResponse(
                    success=False,
                    data=None,
                    source="gnomAD",
                    timestamp=datetime.now().isoformat(),
                    error_message=str(data['errors'])
                )
            
            variant_data = data.get('data', {}).get('variant')
            if variant_data:
                self.cache.set(cache_key, variant_data)
            
            return APIResponse(
                success=True,
                data=variant_data,
                source="gnomAD",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="gnomAD",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_gene_variants(self, gene_symbol: str, dataset: str = "gnomad_r4") -> APIResponse:
        """Get all variants in a gene"""
        cache_key = f"gnomad_gene_{gene_symbol}_{dataset}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="gnomAD",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        query = """
        query GeneQuery($geneSymbol: String!, $datasetId: DatasetId!) {
            gene(gene_symbol: $geneSymbol, reference_genome: GRCh38) {
                gene_id
                symbol
                name
                chrom
                start
                stop
                variants(dataset: $datasetId) {
                    variant_id
                    pos
                    ref
                    alt
                    exome {
                        af
                    }
                    genome {
                        af
                    }
                }
            }
        }
        """
        
        try:
            response = self.session.post(
                self.api_url,
                json={
                    'query': query,
                    'variables': {
                        'geneSymbol': gene_symbol,
                        'datasetId': dataset
                    }
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            gene_data = data.get('data', {}).get('gene')
            if gene_data:
                self.cache.set(cache_key, gene_data)
            
            return APIResponse(
                success=True,
                data=gene_data,
                source="gnomAD",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="gnomAD",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )


class GWASCatalogClient:
    """Client for GWAS Catalog REST API"""
    
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        self.api_url = GWAS_CATALOG_API
        self.cache = cache_manager or CacheManager()
        self.session = requests.Session()
    
    def search_associations(self, trait: str, page_size: int = 100) -> APIResponse:
        """
        Search GWAS associations by trait
        
        Args:
            trait: Trait/phenotype to search (e.g., "alcohol dependence")
            page_size: Number of results per page
        
        Returns:
            APIResponse with association data
        """
        cache_key = f"gwas_trait_{trait}_{page_size}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="GWAS Catalog",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        try:
            response = self.session.get(
                f"{self.api_url}/associations/search/findByEfoTrait",
                params={
                    'efoTrait': trait,
                    'size': page_size
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            associations = []
            for assoc in data.get('_embedded', {}).get('associations', []):
                associations.append({
                    'study_id': assoc.get('study', {}).get('studyId', ''),
                    'trait': trait,
                    'p_value': assoc.get('pvalue', 1.0),
                    'snps': [snp.get('rsId', '') for snp in assoc.get('snps', [])],
                    'genes': [gene.get('geneName', '') for gene in assoc.get('genes', [])]
                })
            
            self.cache.set(cache_key, associations)
            
            return APIResponse(
                success=True,
                data=associations,
                source="GWAS Catalog",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="GWAS Catalog",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_study(self, study_id: str) -> APIResponse:
        """Get detailed study information"""
        cache_key = f"gwas_study_{study_id}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="GWAS Catalog",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        try:
            response = self.session.get(
                f"{self.api_url}/studies/{study_id}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            self.cache.set(cache_key, data)
            
            return APIResponse(
                success=True,
                data=data,
                source="GWAS Catalog",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="GWAS Catalog",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_addiction_gwas(self) -> APIResponse:
        """Get GWAS studies related to addiction phenotypes"""
        addiction_traits = [
            "alcohol dependence",
            "opioid dependence", 
            "cocaine dependence",
            "cannabis use disorder",
            "nicotine dependence",
            "substance use disorder",
            "drug addiction"
        ]
        
        all_associations = []
        for trait in addiction_traits:
            response = self.search_associations(trait)
            if response.success and response.data:
                for assoc in response.data:
                    assoc['addiction_trait'] = trait
                all_associations.extend(response.data)
            time.sleep(0.5)  # Rate limiting
        
        return APIResponse(
            success=True,
            data=all_associations,
            source="GWAS Catalog",
            timestamp=datetime.now().isoformat()
        )


class PubChemClient:
    """Client for PubChem PUG REST API"""
    
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        self.api_url = PUBCHEM_API
        self.cache = cache_manager or CacheManager()
        self.session = requests.Session()
    
    def get_compound_by_name(self, name: str) -> APIResponse:
        """
        Get compound information by name
        
        Args:
            name: Compound name (e.g., "morphine", "cocaine")
        
        Returns:
            APIResponse with compound data
        """
        cache_key = f"pubchem_name_{name}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="PubChem",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        try:
            response = self.session.get(
                f"{self.api_url}/compound/name/{name}/JSON",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            compounds = data.get('PC_Compounds', [])
            if compounds:
                compound = compounds[0]
                compound_data = self._parse_compound(compound)
                self.cache.set(cache_key, compound_data)
                
                return APIResponse(
                    success=True,
                    data=compound_data,
                    source="PubChem",
                    timestamp=datetime.now().isoformat()
                )
            
            return APIResponse(
                success=False,
                data=None,
                source="PubChem",
                timestamp=datetime.now().isoformat(),
                error_message="Compound not found"
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="PubChem",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_compound_properties(self, cid: int, properties: List[str] = None) -> APIResponse:
        """Get specific properties for a compound"""
        if properties is None:
            properties = [
                "MolecularFormula", "MolecularWeight", "CanonicalSMILES",
                "IUPACName", "XLogP", "TPSA", "Complexity", "HBondDonorCount",
                "HBondAcceptorCount", "RotatableBondCount"
            ]
        
        cache_key = f"pubchem_props_{cid}_{','.join(properties)}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="PubChem",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        try:
            props_str = ",".join(properties)
            response = self.session.get(
                f"{self.api_url}/compound/cid/{cid}/property/{props_str}/JSON",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            props = data.get('PropertyTable', {}).get('Properties', [{}])[0]
            self.cache.set(cache_key, props)
            
            return APIResponse(
                success=True,
                data=props,
                source="PubChem",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="PubChem",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def _parse_compound(self, compound: Dict) -> SubstanceData:
        """Parse PubChem compound JSON to SubstanceData"""
        cid = compound.get('id', {}).get('id', {}).get('cid', 0)
        
        props = compound.get('props', [])
        name = ""
        smiles = ""
        formula = ""
        weight = 0.0
        iupac = ""
        
        for prop in props:
            urn = prop.get('urn', {})
            label = urn.get('label', '')
            value = prop.get('value', {})
            
            if label == 'IUPAC Name' and urn.get('name') == 'Preferred':
                iupac = value.get('sval', '')
            elif label == 'SMILES' and urn.get('name') == 'Canonical':
                smiles = value.get('sval', '')
            elif label == 'Molecular Formula':
                formula = value.get('sval', '')
            elif label == 'Molecular Weight':
                weight = value.get('fval', 0.0)
        
        return SubstanceData(
            cid=cid,
            name=name or str(cid),
            smiles=smiles,
            molecular_formula=formula,
            molecular_weight=weight,
            iupac_name=iupac
        )
    
    def get_addiction_substances(self) -> APIResponse:
        """Get data for known addictive substances"""
        substances = [
            "morphine", "heroin", "fentanyl", "oxycodone", "hydrocodone",
            "cocaine", "methamphetamine", "amphetamine", "MDMA",
            "ethanol", "nicotine", "caffeine",
            "diazepam", "alprazolam", "clonazepam",
            "THC", "cannabidiol",
            "ketamine", "PCP", "LSD", "psilocybin"
        ]
        
        results = []
        for substance in substances:
            response = self.get_compound_by_name(substance)
            if response.success and response.data:
                results.append({
                    'name': substance,
                    'data': response.data
                })
            time.sleep(0.2)  # Rate limiting
        
        return APIResponse(
            success=True,
            data=results,
            source="PubChem",
            timestamp=datetime.now().isoformat()
        )


class NCBIEntrezClient:
    """Client for NCBI Entrez API"""
    
    def __init__(self, email: str = "research@epiclock.org", 
                 api_key: Optional[str] = None,
                 cache_manager: Optional[CacheManager] = None):
        self.api_url = NCBI_ENTREZ_API
        self.email = email
        self.api_key = api_key or os.environ.get('NCBI_API_KEY', '')
        self.cache = cache_manager or CacheManager()
        self.session = requests.Session()
    
    def search_gene(self, query: str, max_results: int = 20) -> APIResponse:
        """Search for genes"""
        cache_key = f"ncbi_gene_search_{query}_{max_results}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="NCBI Entrez",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        params = {
            'db': 'gene',
            'term': query,
            'retmax': max_results,
            'retmode': 'json',
            'email': self.email
        }
        if self.api_key:
            params['api_key'] = self.api_key
        
        try:
            response = self.session.get(
                f"{self.api_url}/esearch.fcgi",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            gene_ids = data.get('esearchresult', {}).get('idlist', [])
            self.cache.set(cache_key, gene_ids)
            
            return APIResponse(
                success=True,
                data=gene_ids,
                source="NCBI Entrez",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="NCBI Entrez",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_gene_info(self, gene_id: str) -> APIResponse:
        """Get detailed gene information"""
        cache_key = f"ncbi_gene_info_{gene_id}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="NCBI Entrez",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        params = {
            'db': 'gene',
            'id': gene_id,
            'retmode': 'json',
            'email': self.email
        }
        if self.api_key:
            params['api_key'] = self.api_key
        
        try:
            response = self.session.get(
                f"{self.api_url}/esummary.fcgi",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            gene_info = data.get('result', {}).get(gene_id, {})
            self.cache.set(cache_key, gene_info)
            
            return APIResponse(
                success=True,
                data=gene_info,
                source="NCBI Entrez",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="NCBI Entrez",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_addiction_genes(self) -> APIResponse:
        """Get information for addiction-related genes"""
        addiction_genes = [
            "OPRM1", "DRD2", "DRD4", "DAT1", "COMT", "BDNF",
            "GABRA2", "CHRNA5", "ADH1B", "ALDH2", "CNR1",
            "HTR2A", "MAOA", "SLC6A4", "FAAH", "ANKK1"
        ]
        
        results = []
        for gene in addiction_genes:
            search_response = self.search_gene(f"{gene}[gene] AND Homo sapiens[organism]", max_results=1)
            if search_response.success and search_response.data:
                gene_id = search_response.data[0]
                info_response = self.get_gene_info(gene_id)
                if info_response.success:
                    results.append({
                        'symbol': gene,
                        'gene_id': gene_id,
                        'info': info_response.data
                    })
            time.sleep(0.35)  # Rate limiting (3 requests/second without API key)
        
        return APIResponse(
            success=True,
            data=results,
            source="NCBI Entrez",
            timestamp=datetime.now().isoformat()
        )


class UniProtClient:
    """Client for UniProt REST API"""
    
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        self.api_url = UNIPROT_API
        self.cache = cache_manager or CacheManager()
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json'
        })
    
    def search_protein(self, query: str, organism: str = "human", 
                       max_results: int = 25) -> APIResponse:
        """Search for proteins"""
        cache_key = f"uniprot_search_{query}_{organism}_{max_results}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="UniProt",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        try:
            search_query = f"{query} AND organism_name:{organism}"
            response = self.session.get(
                f"{self.api_url}/uniprotkb/search",
                params={
                    'query': search_query,
                    'size': max_results,
                    'format': 'json'
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            results = data.get('results', [])
            self.cache.set(cache_key, results)
            
            return APIResponse(
                success=True,
                data=results,
                source="UniProt",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="UniProt",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_protein_entry(self, accession: str) -> APIResponse:
        """Get detailed protein entry"""
        cache_key = f"uniprot_entry_{accession}"
        cached = self.cache.get(cache_key)
        if cached:
            return APIResponse(
                success=True,
                data=cached,
                source="UniProt",
                timestamp=datetime.now().isoformat(),
                cache_hit=True
            )
        
        try:
            response = self.session.get(
                f"{self.api_url}/uniprotkb/{accession}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            self.cache.set(cache_key, data)
            
            return APIResponse(
                success=True,
                data=data,
                source="UniProt",
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                source="UniProt",
                timestamp=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_receptor_proteins(self) -> APIResponse:
        """Get receptor proteins relevant to addiction"""
        receptor_queries = [
            "opioid receptor",
            "dopamine receptor",
            "serotonin receptor",
            "GABA receptor",
            "glutamate receptor",
            "cannabinoid receptor"
        ]
        
        results = []
        for query in receptor_queries:
            response = self.search_protein(query, max_results=10)
            if response.success and response.data:
                for protein in response.data:
                    results.append({
                        'receptor_type': query,
                        'accession': protein.get('primaryAccession', ''),
                        'name': protein.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', ''),
                        'gene': protein.get('genes', [{}])[0].get('geneName', {}).get('value', '') if protein.get('genes') else ''
                    })
            time.sleep(0.5)
        
        return APIResponse(
            success=True,
            data=results,
            source="UniProt",
            timestamp=datetime.now().isoformat()
        )


class GenomicDataAggregator:
    """Aggregate data from all genomic APIs"""
    
    def __init__(self):
        self.cache = CacheManager(ttl_hours=48)
        self.gnomad = GnomADClient(self.cache)
        self.gwas = GWASCatalogClient(self.cache)
        self.pubchem = PubChemClient(self.cache)
        self.ncbi = NCBIEntrezClient(cache_manager=self.cache)
        self.uniprot = UniProtClient(self.cache)
    
    def fetch_addiction_research_data(self) -> Dict[str, APIResponse]:
        """Fetch comprehensive addiction research data from all sources"""
        results = {}
        
        print("Fetching GWAS addiction studies...")
        results['gwas'] = self.gwas.get_addiction_gwas()
        
        print("Fetching addiction-related substances from PubChem...")
        results['substances'] = self.pubchem.get_addiction_substances()
        
        print("Fetching addiction gene information from NCBI...")
        results['genes'] = self.ncbi.get_addiction_genes()
        
        print("Fetching receptor protein data from UniProt...")
        results['receptors'] = self.uniprot.get_receptor_proteins()
        
        return results
    
    def get_gene_variant_profile(self, gene_symbol: str) -> Dict:
        """Get comprehensive variant profile for a gene"""
        profile = {
            'gene_symbol': gene_symbol,
            'variants': None,
            'gene_info': None,
            'gwas_associations': None,
            'protein_info': None
        }
        
        gnomad_response = self.gnomad.get_gene_variants(gene_symbol)
        if gnomad_response.success:
            profile['variants'] = gnomad_response.data
        
        ncbi_search = self.ncbi.search_gene(f"{gene_symbol}[gene] AND Homo sapiens[organism]", max_results=1)
        if ncbi_search.success and ncbi_search.data:
            gene_info = self.ncbi.get_gene_info(ncbi_search.data[0])
            if gene_info.success:
                profile['gene_info'] = gene_info.data
        
        gwas_response = self.gwas.search_associations(gene_symbol)
        if gwas_response.success:
            profile['gwas_associations'] = gwas_response.data
        
        uniprot_response = self.uniprot.search_protein(gene_symbol, max_results=1)
        if uniprot_response.success and uniprot_response.data:
            profile['protein_info'] = uniprot_response.data[0]
        
        return profile
    
    def export_to_dataframe(self, data: Dict[str, APIResponse]) -> Dict[str, pd.DataFrame]:
        """Export aggregated data to DataFrames for ML training"""
        dfs = {}
        
        if 'gwas' in data and data['gwas'].success:
            gwas_records = []
            for assoc in data['gwas'].data:
                gwas_records.append({
                    'study_id': assoc.get('study_id', ''),
                    'trait': assoc.get('trait', ''),
                    'addiction_trait': assoc.get('addiction_trait', ''),
                    'p_value': assoc.get('p_value', 1.0),
                    'snps': ','.join(assoc.get('snps', [])),
                    'genes': ','.join(assoc.get('genes', []))
                })
            dfs['gwas'] = pd.DataFrame(gwas_records)
        
        if 'substances' in data and data['substances'].success:
            substance_records = []
            for item in data['substances'].data:
                sub_data = item.get('data')
                if sub_data:
                    substance_records.append({
                        'name': item.get('name', ''),
                        'cid': sub_data.cid if hasattr(sub_data, 'cid') else sub_data.get('cid', 0),
                        'smiles': sub_data.smiles if hasattr(sub_data, 'smiles') else sub_data.get('smiles', ''),
                        'molecular_formula': sub_data.molecular_formula if hasattr(sub_data, 'molecular_formula') else sub_data.get('molecular_formula', ''),
                        'molecular_weight': sub_data.molecular_weight if hasattr(sub_data, 'molecular_weight') else sub_data.get('molecular_weight', 0.0)
                    })
            dfs['substances'] = pd.DataFrame(substance_records)
        
        if 'genes' in data and data['genes'].success:
            gene_records = []
            for gene in data['genes'].data:
                info = gene.get('info', {})
                gene_records.append({
                    'symbol': gene.get('symbol', ''),
                    'gene_id': gene.get('gene_id', ''),
                    'name': info.get('name', ''),
                    'description': info.get('description', ''),
                    'chromosome': info.get('chromosome', '')
                })
            dfs['genes'] = pd.DataFrame(gene_records)
        
        if 'receptors' in data and data['receptors'].success:
            receptor_records = data['receptors'].data
            dfs['receptors'] = pd.DataFrame(receptor_records)
        
        return dfs


def test_api_clients():
    """Test all API clients"""
    print("=" * 60)
    print("EpiClock v4.0 - Genomic API Client Test")
    print("=" * 60)
    
    aggregator = GenomicDataAggregator()
    
    print("\n[1] Testing PubChem API...")
    pubchem_response = aggregator.pubchem.get_compound_by_name("morphine")
    print(f"    PubChem Success: {pubchem_response.success}")
    if pubchem_response.success and pubchem_response.data:
        print(f"    Morphine CID: {pubchem_response.data.cid if hasattr(pubchem_response.data, 'cid') else 'N/A'}")
    
    print("\n[2] Testing GWAS Catalog API...")
    gwas_response = aggregator.gwas.search_associations("alcohol dependence", page_size=5)
    print(f"    GWAS Success: {gwas_response.success}")
    if gwas_response.success and gwas_response.data:
        print(f"    Found {len(gwas_response.data)} associations")
    
    print("\n[3] Testing NCBI Entrez API...")
    ncbi_response = aggregator.ncbi.search_gene("OPRM1[gene] AND Homo sapiens[organism]", max_results=1)
    print(f"    NCBI Success: {ncbi_response.success}")
    if ncbi_response.success and ncbi_response.data:
        print(f"    OPRM1 Gene ID: {ncbi_response.data[0] if ncbi_response.data else 'N/A'}")
    
    print("\n[4] Testing UniProt API...")
    uniprot_response = aggregator.uniprot.search_protein("opioid receptor", max_results=3)
    print(f"    UniProt Success: {uniprot_response.success}")
    if uniprot_response.success and uniprot_response.data:
        print(f"    Found {len(uniprot_response.data)} proteins")
    
    print("\n" + "=" * 60)
    print("API Client Tests Complete")
    print("=" * 60)
    
    return aggregator


if __name__ == "__main__":
    test_api_clients()
