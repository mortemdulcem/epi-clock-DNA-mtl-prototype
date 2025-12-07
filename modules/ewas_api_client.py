"""
EWAS Catalog API Client
=======================

Otomatik olarak EWAS Catalog'dan hastalik-CpG iliskilerini ceker.

EWAS Catalog: https://ewascatalog.org/
- 500,000+ CpG-hastalik iliskileri
- Peer-reviewed EWAS calismalari
- Ucretsiz akademik erisim

Author: EpiClock Team
Version: 1.0
"""

import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import time
import hashlib
import os

# Database imports
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False


@dataclass
class EWASStudy:
    """EWAS calismasi"""
    study_id: str
    trait: str
    trait_category: str
    pmid: str
    author: str
    year: int
    sample_size: int
    tissue: str
    array_type: str
    ancestry: str


@dataclass  
class EWASAssociation:
    """CpG-Trait iliskisi"""
    cpg: str
    trait: str
    trait_category: str
    beta: float
    se: float
    p_value: float
    n: int
    study_id: str
    pmid: str
    gene: Optional[str] = None
    chr: Optional[str] = None
    pos: Optional[int] = None


class EWASCatalogAPI:
    """
    EWAS Catalog API Client
    
    EWAS Catalog veritabanindan otomatik veri ceker.
    Rate limiting ve caching destekler.
    """
    
    BASE_URL = "https://ewascatalog.org/api"
    
    # Oncelikli hastalik kategorileri
    PRIORITY_TRAITS = [
        # Bagimlilik
        "smoking", "alcohol", "cannabis", "cocaine", "opioid", "substance",
        # Psikiyatrik
        "depression", "anxiety", "ptsd", "schizophrenia", "bipolar",
        # Metabolik
        "diabetes", "obesity", "bmi", "metabolic",
        # Kanser
        "cancer", "leukemia", "lymphoma", "carcinoma",
        # Norolojik
        "alzheimer", "parkinson", "dementia",
        # Kardiyovaskuler
        "cardiovascular", "hypertension", "atherosclerosis",
        # Solunum
        "asthma", "copd", "lung",
        # Yeme bozukluklari
        "anorexia", "bulimia", "eating",
        # Otoimmun
        "rheumatoid", "lupus", "autoimmune",
        # Diger
        "aging", "mortality", "inflammation"
    ]
    
    def __init__(self, cache_dir: str = "data/ewas_cache"):
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EpiClock/1.0 (Academic Research)',
            'Accept': 'application/json'
        })
        
        # Cache dizini olustur
        os.makedirs(cache_dir, exist_ok=True)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms
        
        # Istatistikler
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'api_calls': 0,
            'errors': 0
        }
    
    def _rate_limit(self):
        """Rate limiting uygula"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _get_cache_path(self, key: str) -> str:
        """Cache dosya yolu olustur"""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.json")
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Cache'den veri oku"""
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    # 7 gunluk cache
                    if time.time() - data.get('timestamp', 0) < 7 * 24 * 3600:
                        self.stats['cache_hits'] += 1
                        return data.get('content')
            except:
                pass
        return None
    
    def _set_cache(self, key: str, content: Any):
        """Cache'e veri yaz"""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'content': content
                }, f)
        except:
            pass
    
    def _api_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """API istegi yap"""
        self.stats['total_requests'] += 1
        
        # Cache kontrol
        cache_key = f"{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        # Rate limit
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self._set_cache(cache_key, data)
            self.stats['api_calls'] += 1
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.stats['errors'] += 1
            print(f"API Error: {e}")
            return None
    
    def get_traits(self) -> List[str]:
        """Tum trait'leri listele"""
        # EWAS Catalog'un trait listesi endpoint'i
        # Not: Gercek API yapisina gore ayarlanmali
        
        # Simdilik bilinen trait kategorilerini dondur
        return self.PRIORITY_TRAITS
    
    def search_trait(self, trait: str, limit: int = 1000) -> List[EWASAssociation]:
        """
        Belirli bir trait icin CpG iliskilerini ara
        
        Args:
            trait: Aranacak trait (ornek: "smoking", "diabetes")
            limit: Maksimum sonuc sayisi
        
        Returns:
            EWASAssociation listesi
        """
        
        # EWAS Catalog API sorgusu
        # Not: Gercek API yapisina gore ayarlanmali
        params = {
            'trait': trait,
            'limit': limit
        }
        
        data = self._api_request('associations', params)
        
        if not data:
            return []
        
        associations = []
        
        # API yanitini parse et
        results = data if isinstance(data, list) else data.get('results', [])
        
        for item in results:
            try:
                assoc = EWASAssociation(
                    cpg=item.get('cpg', item.get('probe', '')),
                    trait=item.get('trait', trait),
                    trait_category=item.get('category', ''),
                    beta=float(item.get('beta', item.get('effect', 0))),
                    se=float(item.get('se', item.get('standard_error', 0))),
                    p_value=float(item.get('p', item.get('pvalue', 1))),
                    n=int(item.get('n', item.get('sample_size', 0))),
                    study_id=item.get('study_id', ''),
                    pmid=str(item.get('pmid', '')),
                    gene=item.get('gene', None),
                    chr=item.get('chr', None),
                    pos=item.get('pos', None)
                )
                associations.append(assoc)
            except (ValueError, KeyError) as e:
                continue
        
        return associations
    
    def get_cpg_associations(self, cpg: str) -> List[EWASAssociation]:
        """
        Belirli bir CpG icin tum trait iliskilerini getir
        
        Args:
            cpg: CpG ID (ornek: "cg00000029")
        
        Returns:
            EWASAssociation listesi
        """
        
        params = {'cpg': cpg}
        data = self._api_request('cpg', params)
        
        if not data:
            return []
        
        associations = []
        results = data if isinstance(data, list) else data.get('results', [])
        
        for item in results:
            try:
                assoc = EWASAssociation(
                    cpg=cpg,
                    trait=item.get('trait', ''),
                    trait_category=item.get('category', ''),
                    beta=float(item.get('beta', 0)),
                    se=float(item.get('se', 0)),
                    p_value=float(item.get('p', 1)),
                    n=int(item.get('n', 0)),
                    study_id=item.get('study_id', ''),
                    pmid=str(item.get('pmid', '')),
                    gene=item.get('gene', None),
                    chr=item.get('chr', None),
                    pos=item.get('pos', None)
                )
                associations.append(assoc)
            except:
                continue
        
        return associations
    
    def bulk_download_traits(self, traits: List[str] = None, 
                             progress_callback=None) -> Dict[str, List[EWASAssociation]]:
        """
        Birden fazla trait icin toplu indirme
        
        Args:
            traits: Trait listesi (None ise oncelikli traitler)
            progress_callback: Ilerleme callback fonksiyonu
        
        Returns:
            {trait: [associations]} dictionary
        """
        
        if traits is None:
            traits = self.PRIORITY_TRAITS
        
        all_data = {}
        
        for i, trait in enumerate(traits):
            if progress_callback:
                progress_callback(i + 1, len(traits), trait)
            
            associations = self.search_trait(trait)
            if associations:
                all_data[trait] = associations
            
            # Progress log
            print(f"[{i+1}/{len(traits)}] {trait}: {len(associations)} association")
        
        return all_data
    
    def build_disease_signatures(self, min_associations: int = 5,
                                  max_pvalue: float = 1e-5) -> Dict[str, Dict]:
        """
        Indirilen verilerden hastalik imzalari olustur
        
        Args:
            min_associations: Minimum CpG sayisi
            max_pvalue: Maksimum p-value esigi
        
        Returns:
            {trait: {cpg_markers, metadata}} dictionary
        """
        
        print("Trait verileri indiriliyor...")
        all_data = self.bulk_download_traits()
        
        signatures = {}
        
        for trait, associations in all_data.items():
            # P-value filtreleme
            significant = [a for a in associations if a.p_value <= max_pvalue]
            
            if len(significant) < min_associations:
                continue
            
            # En anlamli CpG'leri sec (p-value'a gore sirala)
            significant.sort(key=lambda x: x.p_value)
            top_cpgs = significant[:50]  # En fazla 50 CpG
            
            # CpG -> coefficient mapping
            cpg_markers = {}
            for assoc in top_cpgs:
                if assoc.cpg and assoc.beta != 0:
                    cpg_markers[assoc.cpg] = assoc.beta
            
            if len(cpg_markers) >= min_associations:
                # Ortalama sample size
                avg_n = np.mean([a.n for a in top_cpgs if a.n > 0])
                
                # PubMed ID'leri
                pmids = list(set(a.pmid for a in top_cpgs if a.pmid))[:5]
                
                # Etkilenen genler
                genes = list(set(a.gene for a in top_cpgs if a.gene))[:10]
                
                signatures[trait] = {
                    'trait': trait,
                    'cpg_markers': cpg_markers,
                    'n_cpgs': len(cpg_markers),
                    'avg_sample_size': int(avg_n) if not np.isnan(avg_n) else 0,
                    'pubmed_ids': pmids,
                    'affected_genes': genes,
                    'category': self._categorize_trait(trait)
                }
        
        print(f"\n{len(signatures)} hastalik imzasi olusturuldu")
        return signatures
    
    def _categorize_trait(self, trait: str) -> str:
        """Trait kategorisini belirle"""
        trait_lower = trait.lower()
        
        if any(x in trait_lower for x in ['smoking', 'alcohol', 'cannabis', 'cocaine', 'opioid', 'substance', 'drug']):
            return 'Bagimlilik'
        elif any(x in trait_lower for x in ['depression', 'anxiety', 'ptsd', 'schizophrenia', 'bipolar', 'psychiatric']):
            return 'Psikiyatrik'
        elif any(x in trait_lower for x in ['diabetes', 'obesity', 'bmi', 'metabolic', 'insulin']):
            return 'Metabolik'
        elif any(x in trait_lower for x in ['cancer', 'leukemia', 'lymphoma', 'carcinoma', 'tumor']):
            return 'Kanser'
        elif any(x in trait_lower for x in ['alzheimer', 'parkinson', 'dementia', 'neurological']):
            return 'Norolojik'
        elif any(x in trait_lower for x in ['cardiovascular', 'hypertension', 'atherosclerosis', 'heart']):
            return 'Kardiyovaskuler'
        elif any(x in trait_lower for x in ['asthma', 'copd', 'lung', 'respiratory']):
            return 'Solunum'
        elif any(x in trait_lower for x in ['anorexia', 'bulimia', 'eating']):
            return 'Yeme Bozuklugu'
        elif any(x in trait_lower for x in ['rheumatoid', 'lupus', 'autoimmune']):
            return 'Otoimmun'
        elif any(x in trait_lower for x in ['aging', 'age', 'mortality']):
            return 'Yaslanma'
        else:
            return 'Diger'
    
    def get_statistics(self) -> Dict[str, Any]:
        """API istatistiklerini dondur"""
        return {
            **self.stats,
            'cache_dir': self.cache_dir,
            'priority_traits': len(self.PRIORITY_TRAITS)
        }


class PharmGKBAPI:
    """
    PharmGKB API Client
    
    Ilac-Gen iliskilerini ceker.
    https://www.pharmgkb.org/
    """
    
    BASE_URL = "https://api.pharmgkb.org/v1/data"
    
    def __init__(self, cache_dir: str = "data/pharmgkb_cache"):
        self.cache_dir = cache_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EpiClock/1.0 (Academic Research)',
            'Accept': 'application/json'
        })
        os.makedirs(cache_dir, exist_ok=True)
        
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 saniye
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def search_drug(self, drug_name: str) -> Optional[Dict]:
        """Ilac ara"""
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/drug"
            params = {'name': drug_name}
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    def get_drug_genes(self, drug_id: str) -> List[Dict]:
        """Ilacin etkiledigi genleri getir"""
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/drug/{drug_id}/relationships"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return [r for r in data.get('data', []) if r.get('type') == 'gene']
            return []
        except:
            return []
    
    def get_clinical_annotations(self, gene: str) -> List[Dict]:
        """Gen icin klinik anotasyonlari getir"""
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/clinicalAnnotation"
            params = {'gene': gene}
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('data', [])
            return []
        except:
            return []


class DrugBankAPI:
    """
    DrugBank API Client (Limited - Academic)
    
    Ilac veritabani.
    https://go.drugbank.com/
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.drugbank.com/v1"
    
    def search_drug(self, name: str) -> Optional[Dict]:
        """Ilac ara (API key gerektirir)"""
        if not self.api_key:
            return None
        
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(
                f"{self.base_url}/drugs",
                params={'q': name},
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None


class GenomicDataPipeline:
    """
    Birlesik Genomik Veri Pipeline
    
    Tum veri kaynaklarini birlestirir ve veritabanina yazar.
    """
    
    def __init__(self, db_url: str = None):
        self.ewas_client = EWASCatalogAPI()
        self.pharmgkb_client = PharmGKBAPI()
        
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.engine = None
        
        if self.db_url and HAS_SQLALCHEMY:
            try:
                self.engine = create_engine(self.db_url)
            except:
                pass
    
    def create_tables(self):
        """Veritabani tablolarini olustur"""
        if not self.engine:
            print("Veritabani baglantisi yok")
            return False
        
        create_sql = """
        -- EWAS Associations tablosu
        CREATE TABLE IF NOT EXISTS ewas_associations (
            id SERIAL PRIMARY KEY,
            cpg VARCHAR(20) NOT NULL,
            trait VARCHAR(255) NOT NULL,
            trait_category VARCHAR(100),
            beta FLOAT,
            se FLOAT,
            p_value FLOAT,
            sample_size INTEGER,
            study_id VARCHAR(100),
            pmid VARCHAR(20),
            gene VARCHAR(50),
            chromosome VARCHAR(10),
            position INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(cpg, trait, study_id)
        );
        
        -- Disease Signatures tablosu
        CREATE TABLE IF NOT EXISTS disease_signatures (
            id SERIAL PRIMARY KEY,
            disease_id VARCHAR(100) NOT NULL UNIQUE,
            disease_name_tr VARCHAR(255),
            disease_name_en VARCHAR(255),
            category VARCHAR(100),
            cpg_markers JSONB,
            pubmed_ids TEXT[],
            affected_genes TEXT[],
            sample_size INTEGER,
            sensitivity FLOAT,
            specificity FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Substance Signatures tablosu
        CREATE TABLE IF NOT EXISTS substance_signatures (
            id SERIAL PRIMARY KEY,
            substance_id VARCHAR(100) NOT NULL UNIQUE,
            substance_name_tr VARCHAR(255),
            substance_name_en VARCHAR(255),
            substance_class VARCHAR(100),
            cpg_markers JSONB,
            dose_response_cpgs JSONB,
            pubmed_ids TEXT[],
            affected_receptors TEXT[],
            affected_genes TEXT[],
            min_detectable_months INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Therapeutic Medications tablosu
        CREATE TABLE IF NOT EXISTS therapeutic_medications (
            id SERIAL PRIMARY KEY,
            medication_id VARCHAR(100) NOT NULL UNIQUE,
            name_tr VARCHAR(255),
            name_en VARCHAR(255),
            category VARCHAR(100),
            eaa_effect FLOAT,
            eaa_direction VARCHAR(20),
            mechanism_tr TEXT,
            mechanism_en TEXT,
            target_genes TEXT[],
            affected_cpgs JSONB,
            pubmed_ids TEXT[],
            drugbank_id VARCHAR(20),
            pharmgkb_id VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Indexler
        CREATE INDEX IF NOT EXISTS idx_ewas_cpg ON ewas_associations(cpg);
        CREATE INDEX IF NOT EXISTS idx_ewas_trait ON ewas_associations(trait);
        CREATE INDEX IF NOT EXISTS idx_ewas_pvalue ON ewas_associations(p_value);
        CREATE INDEX IF NOT EXISTS idx_disease_category ON disease_signatures(category);
        CREATE INDEX IF NOT EXISTS idx_substance_class ON substance_signatures(substance_class);
        """
        
        try:
            with self.engine.connect() as conn:
                for statement in create_sql.split(';'):
                    if statement.strip():
                        conn.execute(text(statement))
                conn.commit()
            print("Veritabani tablolari olusturuldu")
            return True
        except Exception as e:
            print(f"Tablo olusturma hatasi: {e}")
            return False
    
    def import_ewas_data(self, traits: List[str] = None):
        """EWAS verilerini veritabanina aktar"""
        if not self.engine:
            print("Veritabani baglantisi yok")
            return
        
        print("EWAS verileri indiriliyor...")
        all_data = self.ewas_client.bulk_download_traits(traits)
        
        imported = 0
        
        with self.engine.connect() as conn:
            for trait, associations in all_data.items():
                for assoc in associations:
                    try:
                        conn.execute(text("""
                            INSERT INTO ewas_associations 
                            (cpg, trait, trait_category, beta, se, p_value, sample_size, study_id, pmid, gene, chromosome, position)
                            VALUES (:cpg, :trait, :category, :beta, :se, :pval, :n, :study, :pmid, :gene, :chr, :pos)
                            ON CONFLICT (cpg, trait, study_id) DO UPDATE SET
                                beta = EXCLUDED.beta,
                                p_value = EXCLUDED.p_value
                        """), {
                            'cpg': assoc.cpg,
                            'trait': assoc.trait,
                            'category': assoc.trait_category,
                            'beta': assoc.beta,
                            'se': assoc.se,
                            'pval': assoc.p_value,
                            'n': assoc.n,
                            'study': assoc.study_id,
                            'pmid': assoc.pmid,
                            'gene': assoc.gene,
                            'chr': assoc.chr,
                            'pos': assoc.pos
                        })
                        imported += 1
                    except Exception as e:
                        continue
            
            conn.commit()
        
        print(f"{imported} EWAS association veritabanina aktarildi")
    
    def generate_signatures_from_db(self, min_cpgs: int = 5, max_pvalue: float = 1e-5):
        """Veritabanindan hastalik imzalari olustur"""
        if not self.engine:
            return {}
        
        query = text("""
            SELECT trait, trait_category,
                   array_agg(cpg) as cpgs,
                   array_agg(beta) as betas,
                   array_agg(gene) as genes,
                   array_agg(pmid) as pmids,
                   avg(sample_size) as avg_n,
                   count(*) as n_associations
            FROM ewas_associations
            WHERE p_value <= :pval
            GROUP BY trait, trait_category
            HAVING count(*) >= :min_cpgs
            ORDER BY count(*) DESC
        """)
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {'pval': max_pvalue, 'min_cpgs': min_cpgs})
            rows = result.fetchall()
        
        signatures = {}
        for row in rows:
            trait = row[0]
            cpg_markers = dict(zip(row[2][:50], row[3][:50]))  # Max 50 CpG
            
            signatures[trait] = {
                'trait': trait,
                'category': row[1],
                'cpg_markers': cpg_markers,
                'affected_genes': list(set(g for g in row[4] if g))[:10],
                'pubmed_ids': list(set(p for p in row[5] if p))[:5],
                'sample_size': int(row[6]) if row[6] else 0,
                'n_associations': row[7]
            }
        
        return signatures
    
    def run_full_pipeline(self):
        """Tam pipeline calistir"""
        print("="*60)
        print("GENOMIK VERI PIPELINE BASLATILIYOR")
        print("="*60)
        
        # 1. Tablolari olustur
        print("\n[1/3] Veritabani tablolari olusturuluyor...")
        self.create_tables()
        
        # 2. EWAS verilerini indir ve aktar
        print("\n[2/3] EWAS verileri indiriliyor...")
        self.import_ewas_data()
        
        # 3. Imzalari olustur
        print("\n[3/3] Hastalik imzalari olusturuluyor...")
        signatures = self.generate_signatures_from_db()
        
        print("\n" + "="*60)
        print(f"PIPELINE TAMAMLANDI: {len(signatures)} imza olusturuldu")
        print("="*60)
        
        return signatures


# Simulated EWAS data for demo (when API is not available)
SIMULATED_EWAS_DATA = {
    'smoking': [
        {'cpg': 'cg05575921', 'beta': -0.085, 'p': 1e-50, 'gene': 'AHRR', 'n': 15000},
        {'cpg': 'cg21566642', 'beta': 0.065, 'p': 1e-45, 'gene': 'ALPPL2', 'n': 15000},
        {'cpg': 'cg01940273', 'beta': -0.048, 'p': 1e-40, 'gene': 'GPR15', 'n': 15000},
        {'cpg': 'cg03636183', 'beta': 0.038, 'p': 1e-35, 'gene': 'F2RL3', 'n': 15000},
        {'cpg': 'cg06126421', 'beta': -0.032, 'p': 1e-30, 'gene': 'LRRN3', 'n': 15000},
    ],
    'alcohol': [
        {'cpg': 'cg06500161', 'beta': -0.028, 'p': 1e-25, 'gene': 'ADH1B', 'n': 10000},
        {'cpg': 'cg14983602', 'beta': 0.024, 'p': 1e-22, 'gene': 'ALDH2', 'n': 10000},
        {'cpg': 'cg18849583', 'beta': -0.021, 'p': 1e-20, 'gene': 'GABRB3', 'n': 10000},
    ],
    'diabetes': [
        {'cpg': 'cg19693031', 'beta': 0.045, 'p': 1e-60, 'gene': 'TXNIP', 'n': 25000},
        {'cpg': 'cg00574958', 'beta': -0.032, 'p': 1e-45, 'gene': 'ABCG1', 'n': 25000},
        {'cpg': 'cg06500161', 'beta': 0.028, 'p': 1e-40, 'gene': 'CPT1A', 'n': 25000},
    ],
    'obesity': [
        {'cpg': 'cg00574958', 'beta': -0.038, 'p': 1e-35, 'gene': 'HIF3A', 'n': 18000},
        {'cpg': 'cg22891070', 'beta': 0.032, 'p': 1e-30, 'gene': 'CPT1A', 'n': 18000},
    ],
    'depression': [
        {'cpg': 'cg05575921', 'beta': -0.028, 'p': 1e-20, 'gene': 'SLC6A4', 'n': 12000},
        {'cpg': 'cg18849583', 'beta': -0.032, 'p': 1e-25, 'gene': 'NR3C1', 'n': 12000},
        {'cpg': 'cg20067310', 'beta': 0.027, 'p': 1e-22, 'gene': 'FKBP5', 'n': 12000},
    ],
    'alzheimer': [
        {'cpg': 'cg11823178', 'beta': 0.042, 'p': 1e-40, 'gene': 'ANK1', 'n': 8000},
        {'cpg': 'cg03169557', 'beta': -0.035, 'p': 1e-35, 'gene': 'RHBDF2', 'n': 8000},
    ],
    'asthma': [
        {'cpg': 'cg10142874', 'beta': -0.023, 'p': 1e-25, 'gene': 'ADRB2', 'n': 10000},
        {'cpg': 'cg27469152', 'beta': 0.018, 'p': 1e-20, 'gene': 'GSDMB', 'n': 10000},
    ],
    'leukemia': [
        {'cpg': 'cg21943212', 'beta': -0.065, 'p': 1e-50, 'gene': 'CEBPA', 'n': 5000},
        {'cpg': 'cg00936728', 'beta': 0.055, 'p': 1e-45, 'gene': 'DNMT3A', 'n': 5000},
    ]
}


def get_simulated_ewas_associations(trait: str) -> List[Dict]:
    """Simule edilmis EWAS verisi dondur"""
    return SIMULATED_EWAS_DATA.get(trait, [])


# Global instance
_pipeline = None

def get_genomic_pipeline() -> GenomicDataPipeline:
    """Global pipeline instance"""
    global _pipeline
    if _pipeline is None:
        _pipeline = GenomicDataPipeline()
    return _pipeline
