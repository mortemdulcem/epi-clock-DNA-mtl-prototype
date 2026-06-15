"""
GEO DataSets Entegrasyon Modulu
================================

NCBI GEO (Gene Expression Omnibus) veritabanindan
DNA metilasyon verilerini otomatik ceker ve isler.

Desteklenen platformlar:
- Illumina 450K
- Illumina EPIC
- RRBS/WGBS

Author: EpiClock Team
Version: 1.0
"""

import os
import requests
import gzip
import io
import time
import json
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
import numpy as np

try:
    from sqlalchemy import create_engine, text
    HAS_DB = True
except ImportError:
    HAS_DB = False


@dataclass
class GEOStudy:
    """GEO calismasi bilgileri"""
    geo_id: str
    title: str
    summary: str
    platform: str
    sample_count: int
    organism: str = "Homo sapiens"
    study_type: str = "methylation"
    submission_date: str = ""
    pubmed_id: str = ""
    
    
@dataclass
class GEOMethylationData:
    """GEO metilasyon verisi"""
    sample_id: str
    geo_id: str
    cpg_values: Dict[str, float]
    phenotype: Dict[str, str] = field(default_factory=dict)
    tissue: str = ""
    age: Optional[float] = None
    sex: str = ""


class GEODataClient:
    """
    NCBI GEO API Client
    
    DNA metilasyon calismalari icin GEO DataSets'ten veri ceker.
    """
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    GEO_FTP = "https://ftp.ncbi.nlm.nih.gov/geo/series"
    
    METHYLATION_PLATFORMS = {
        'GPL13534': 'Illumina HumanMethylation450',
        'GPL21145': 'Illumina MethylationEPIC',
        'GPL8490': 'Illumina HumanMethylation27',
        'GPL16304': 'Agilent SurePrint G3',
    }
    
    ADDICTION_KEYWORDS = [
        'addiction', 'substance abuse', 'alcohol', 'cocaine', 'opioid',
        'heroin', 'methamphetamine', 'cannabis', 'nicotine', 'smoking',
        'drug abuse', 'substance use disorder'
    ]
    
    DISEASE_KEYWORDS = [
        'cancer', 'diabetes', 'obesity', 'alzheimer', 'parkinson',
        'schizophrenia', 'depression', 'autism', 'epilepsy',
        'cardiovascular', 'asthma', 'lupus', 'arthritis'
    ]
    
    def __init__(self, cache_dir: str = "data/geo_cache", 
                 email: str = "research@epiclock.org"):
        self.cache_dir = cache_dir
        self.email = email
        os.makedirs(cache_dir, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EpiClock/1.0 (Academic Research)',
            'Accept': 'application/json,text/plain'
        })
        
        self.last_request_time = 0
        self.min_request_interval = 0.4
        
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'studies_found': 0,
            'samples_processed': 0
        }
    
    def _rate_limit(self):
        """Rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _get_cache_path(self, key: str) -> str:
        """Cache dosya yolu"""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.json")
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Cache oku"""
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                    if time.time() - data.get('timestamp', 0) < 7 * 24 * 3600:
                        self.stats['cache_hits'] += 1
                        return data.get('content')
            except:
                pass
        return None
    
    def _set_cache(self, key: str, content: Any):
        """Cache yaz"""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'content': content
                }, f)
        except:
            pass
    
    def search_methylation_studies(self, query: str = None, 
                                    max_results: int = 100) -> List[str]:
        """
        Metilasyon calismalari ara
        
        Args:
            query: Arama sorgusu (None ise bagimlilik terimleri)
            max_results: Maksimum sonuc
            
        Returns:
            GEO ID listesi (GSExxxxx)
        """
        
        if query is None:
            query = " OR ".join([f'"{kw}"' for kw in self.ADDICTION_KEYWORDS])
        
        search_query = f'({query}) AND "methylation"[Title] AND "Homo sapiens"[Organism]'
        
        cache_key = f"geo_search_{hashlib.md5(search_query.encode()).hexdigest()}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        self._rate_limit()
        self.stats['total_requests'] += 1
        
        try:
            params = {
                'db': 'gds',
                'term': search_query,
                'retmax': max_results,
                'retmode': 'json',
                'email': self.email
            }
            
            response = self.session.get(
                f"{self.BASE_URL}/esearch.fcgi",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            id_list = data.get('esearchresult', {}).get('idlist', [])
            
            geo_ids = []
            for gds_id in id_list[:max_results]:
                geo_id = self._get_geo_id_from_gds(gds_id)
                if geo_id:
                    geo_ids.append(geo_id)
            
            self._set_cache(cache_key, geo_ids)
            self.stats['studies_found'] = len(geo_ids)
            
            return geo_ids
            
        except Exception as e:
            print(f"GEO arama hatasi: {e}")
            return []
    
    def _get_geo_id_from_gds(self, gds_id: str) -> Optional[str]:
        """GDS ID'den GSE ID'yi al"""
        self._rate_limit()
        
        try:
            params = {
                'db': 'gds',
                'id': gds_id,
                'retmode': 'json',
                'email': self.email
            }
            
            response = self.session.get(
                f"{self.BASE_URL}/esummary.fcgi",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {}).get(gds_id, {})
                gse = result.get('gse', '')
                if gse:
                    return f"GSE{gse}"
            return None
            
        except:
            return None
    
    def get_study_info(self, geo_id: str) -> Optional[GEOStudy]:
        """
        Calisma bilgilerini al
        
        Args:
            geo_id: GEO ID (GSExxxxx)
            
        Returns:
            GEOStudy nesnesi
        """
        
        cache_key = f"geo_study_{geo_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return GEOStudy(**cached)
        
        self._rate_limit()
        
        try:
            params = {
                'db': 'gds',
                'term': f'{geo_id}[Accession]',
                'retmode': 'json',
                'email': self.email
            }
            
            search_response = self.session.get(
                f"{self.BASE_URL}/esearch.fcgi",
                params=params,
                timeout=30
            )
            
            if search_response.status_code != 200:
                return None
                
            search_data = search_response.json()
            ids = search_data.get('esearchresult', {}).get('idlist', [])
            
            if not ids:
                return None
            
            self._rate_limit()
            
            summary_params = {
                'db': 'gds',
                'id': ids[0],
                'retmode': 'json',
                'email': self.email
            }
            
            summary_response = self.session.get(
                f"{self.BASE_URL}/esummary.fcgi",
                params=summary_params,
                timeout=30
            )
            
            if summary_response.status_code != 200:
                return None
                
            summary_data = summary_response.json()
            result = summary_data.get('result', {}).get(ids[0], {})
            
            study = GEOStudy(
                geo_id=geo_id,
                title=result.get('title', ''),
                summary=result.get('summary', ''),
                platform=result.get('gpl', ''),
                sample_count=result.get('n_samples', 0),
                organism=result.get('taxon', 'Homo sapiens'),
                submission_date=result.get('pdat', ''),
                pubmed_id=str(result.get('pubmedids', [''])[0]) if result.get('pubmedids') else ''
            )
            
            self._set_cache(cache_key, {
                'geo_id': study.geo_id,
                'title': study.title,
                'summary': study.summary,
                'platform': study.platform,
                'sample_count': study.sample_count,
                'organism': study.organism,
                'submission_date': study.submission_date,
                'pubmed_id': study.pubmed_id
            })
            
            return study
            
        except Exception as e:
            print(f"Calisma bilgisi alma hatasi: {e}")
            return None
    
    def search_addiction_studies(self, max_per_keyword: int = 10) -> List[GEOStudy]:
        """Bagimlilik calismalarini ara"""
        studies = []
        seen_ids = set()
        
        for keyword in self.ADDICTION_KEYWORDS:
            geo_ids = self.search_methylation_studies(keyword, max_per_keyword)
            
            for geo_id in geo_ids:
                if geo_id not in seen_ids:
                    study = self.get_study_info(geo_id)
                    if study and study.sample_count > 0:
                        studies.append(study)
                        seen_ids.add(geo_id)
        
        return studies
    
    def search_disease_studies(self, max_per_keyword: int = 10) -> List[GEOStudy]:
        """Hastalik calismalarini ara"""
        studies = []
        seen_ids = set()
        
        for keyword in self.DISEASE_KEYWORDS:
            geo_ids = self.search_methylation_studies(keyword, max_per_keyword)
            
            for geo_id in geo_ids:
                if geo_id not in seen_ids:
                    study = self.get_study_info(geo_id)
                    if study and study.sample_count > 0:
                        studies.append(study)
                        seen_ids.add(geo_id)
        
        return studies
    
    def get_statistics(self) -> Dict[str, Any]:
        """Istatistikleri dondur"""
        return {
            **self.stats,
            'cache_dir': self.cache_dir,
            'supported_platforms': len(self.METHYLATION_PLATFORMS),
            'addiction_keywords': len(self.ADDICTION_KEYWORDS),
            'disease_keywords': len(self.DISEASE_KEYWORDS)
        }


class GEODataLoader:
    """
    GEO verilerini veritabanina yukler
    """
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.engine = None
        self.client = GEODataClient()
        
        if self.db_url and HAS_DB:
            try:
                self.engine = create_engine(self.db_url)
            except:
                pass
    
    def create_geo_tables(self) -> bool:
        """GEO tablolarini olustur"""
        if not self.engine:
            return False
        
        create_sql = """
        CREATE TABLE IF NOT EXISTS geo_studies (
            id SERIAL PRIMARY KEY,
            geo_id VARCHAR(20) NOT NULL UNIQUE,
            title TEXT,
            summary TEXT,
            platform VARCHAR(50),
            sample_count INTEGER,
            organism VARCHAR(100),
            study_type VARCHAR(50),
            submission_date VARCHAR(20),
            pubmed_id VARCHAR(20),
            keywords TEXT[],
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS geo_cpg_associations (
            id SERIAL PRIMARY KEY,
            geo_id VARCHAR(20) NOT NULL,
            cpg VARCHAR(20) NOT NULL,
            phenotype VARCHAR(255),
            beta_mean FLOAT,
            beta_diff FLOAT,
            p_value FLOAT,
            sample_size INTEGER,
            UNIQUE(geo_id, cpg, phenotype)
        );
        
        CREATE INDEX IF NOT EXISTS idx_geo_cpg ON geo_cpg_associations(cpg);
        CREATE INDEX IF NOT EXISTS idx_geo_phenotype ON geo_cpg_associations(phenotype);
        """
        
        try:
            with self.engine.connect() as conn:
                for statement in create_sql.split(';'):
                    if statement.strip():
                        conn.execute(text(statement))
                conn.commit()
            return True
        except Exception as e:
            print(f"GEO tablo olusturma hatasi: {e}")
            return False
    
    def import_addiction_studies(self, max_studies: int = 50) -> Dict[str, Any]:
        """Bagimlilik calismalarini ice aktar"""
        results = {
            'studies_imported': 0,
            'total_samples': 0,
            'errors': []
        }
        
        if not self.engine:
            results['errors'].append("Veritabani baglantisi yok")
            return results
        
        self.create_geo_tables()
        
        studies = self.client.search_addiction_studies(max_per_keyword=max_studies // 10)
        
        with self.engine.connect() as conn:
            for study in studies[:max_studies]:
                try:
                    conn.execute(text("""
                        INSERT INTO geo_studies 
                        (geo_id, title, summary, platform, sample_count, 
                         organism, study_type, submission_date, pubmed_id, keywords)
                        VALUES (:geo_id, :title, :summary, :platform, :n,
                                :organism, :type, :date, :pmid, :keywords)
                        ON CONFLICT (geo_id) DO UPDATE SET
                            title = EXCLUDED.title,
                            sample_count = EXCLUDED.sample_count
                    """), {
                        'geo_id': study.geo_id,
                        'title': study.title,
                        'summary': study.summary[:2000] if study.summary else '',
                        'platform': study.platform,
                        'n': study.sample_count,
                        'organism': study.organism,
                        'type': 'addiction_methylation',
                        'date': study.submission_date,
                        'pmid': study.pubmed_id,
                        'keywords': self.client.ADDICTION_KEYWORDS[:5]
                    })
                    
                    results['studies_imported'] += 1
                    results['total_samples'] += study.sample_count
                    
                except Exception as e:
                    results['errors'].append(f"{study.geo_id}: {str(e)}")
            
            conn.commit()
        
        return results
    
    def import_disease_studies(self, max_studies: int = 100) -> Dict[str, Any]:
        """Hastalik calismalarini ice aktar"""
        results = {
            'studies_imported': 0,
            'total_samples': 0,
            'errors': []
        }
        
        if not self.engine:
            results['errors'].append("Veritabani baglantisi yok")
            return results
        
        self.create_geo_tables()
        
        studies = self.client.search_disease_studies(max_per_keyword=max_studies // 10)
        
        with self.engine.connect() as conn:
            for study in studies[:max_studies]:
                try:
                    conn.execute(text("""
                        INSERT INTO geo_studies 
                        (geo_id, title, summary, platform, sample_count, 
                         organism, study_type, submission_date, pubmed_id, keywords)
                        VALUES (:geo_id, :title, :summary, :platform, :n,
                                :organism, :type, :date, :pmid, :keywords)
                        ON CONFLICT (geo_id) DO UPDATE SET
                            title = EXCLUDED.title,
                            sample_count = EXCLUDED.sample_count
                    """), {
                        'geo_id': study.geo_id,
                        'title': study.title,
                        'summary': study.summary[:2000] if study.summary else '',
                        'platform': study.platform,
                        'n': study.sample_count,
                        'organism': study.organism,
                        'type': 'disease_methylation',
                        'date': study.submission_date,
                        'pmid': study.pubmed_id,
                        'keywords': self.client.DISEASE_KEYWORDS[:5]
                    })
                    
                    results['studies_imported'] += 1
                    results['total_samples'] += study.sample_count
                    
                except Exception as e:
                    results['errors'].append(f"{study.geo_id}: {str(e)}")
            
            conn.commit()
        
        return results
    
    def get_import_statistics(self) -> Dict[str, Any]:
        """Import istatistiklerini al"""
        stats = {
            'total_studies': 0,
            'total_samples': 0,
            'by_type': {}
        }
        
        if not self.engine:
            return stats
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT COUNT(*), SUM(sample_count) FROM geo_studies"
                ))
                row = result.fetchone()
                stats['total_studies'] = row[0] or 0
                stats['total_samples'] = row[1] or 0
                
                result = conn.execute(text("""
                    SELECT study_type, COUNT(*), SUM(sample_count)
                    FROM geo_studies
                    GROUP BY study_type
                """))
                
                for row in result:
                    stats['by_type'][row[0] or 'unknown'] = {
                        'studies': row[1],
                        'samples': row[2] or 0
                    }
                    
        except:
            pass
        
        return stats


def get_geo_loader() -> GEODataLoader:
    """Global GEO loader instance"""
    return GEODataLoader()
