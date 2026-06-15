"""
ETL Pipeline Yonetim Modulu
===========================

EWAS, PharmGKB, PubChem verilerinin otomatik
cekilmesi, islenmesi ve model egitimini yonetir.

Author: EpiClock Team
Version: 1.0
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import hashlib

# Database
try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    HAS_DB = True
except ImportError:
    HAS_DB = False

# Local imports
try:
    from modules.ewas_api_client import EWASCatalogAPI, PharmGKBAPI, GenomicDataPipeline
    from modules.pubchem_api_client import PubChemAPI, DrugBankLite
    from modules.auto_model_trainer import AutoModelTrainer, DurationEstimator
except ImportError:
    pass

# GEO and UNODC imports
try:
    from modules.geo_data_integration import GEODataLoader, GEODataClient
    from modules.unodc_data_sources import UNODCDataLoader, ContinuousLearningSystem
    HAS_GEO_UNODC = True
except ImportError:
    HAS_GEO_UNODC = False


class PipelineStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    SCHEDULED = "scheduled"


@dataclass
class PipelineJob:
    """Pipeline is"""
    job_id: str
    job_type: str
    status: PipelineStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    message: str = ""
    error: Optional[str] = None
    results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataSource:
    """Veri kaynagi"""
    source_id: str
    name: str
    description: str
    api_url: str
    last_sync: Optional[datetime] = None
    record_count: int = 0
    status: str = "idle"
    requires_api_key: bool = False


class ETLPipelineManager:
    """
    ETL Pipeline Yoneticisi
    
    Tum veri kaynaklarini yonetir ve senkronize eder.
    """
    
    # Veri kaynaklari
    DATA_SOURCES = {
        'ewas_catalog': DataSource(
            source_id='ewas_catalog',
            name='EWAS Catalog',
            description='Epigenome-Wide Association Studies - 500,000+ CpG-hastalik iliskileri',
            api_url='https://ewascatalog.org/api',
            requires_api_key=False
        ),
        'pharmgkb': DataSource(
            source_id='pharmgkb',
            name='PharmGKB',
            description='Pharmacogenomics - Ilac-Gen iliskileri',
            api_url='https://api.pharmgkb.org/v1',
            requires_api_key=False
        ),
        'pubchem': DataSource(
            source_id='pubchem',
            name='PubChem',
            description='Kimyasal yapilar ve biyoaktivite - 100M+ bilesik',
            api_url='https://pubchem.ncbi.nlm.nih.gov/rest/pug',
            requires_api_key=False
        ),
        'drugbank': DataSource(
            source_id='drugbank',
            name='DrugBank',
            description='Kapsamli ilac veritabani',
            api_url='https://api.drugbank.com/v1',
            requires_api_key=True
        ),
        'geo_datasets': DataSource(
            source_id='geo_datasets',
            name='GEO DataSets',
            description='NCBI Gene Expression Omnibus - DNA metilasyon verileri',
            api_url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils',
            requires_api_key=False
        ),
        'clinvar': DataSource(
            source_id='clinvar',
            name='ClinVar',
            description='Genetik varyant-hastalik iliskileri',
            api_url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils',
            requires_api_key=False
        )
    }
    
    # Oncelikli trait listesi (EWAS icin)
    PRIORITY_TRAITS = [
        # Bagimlilik
        'smoking', 'alcohol consumption', 'cannabis', 'cocaine', 'opioid',
        'methamphetamine', 'substance use', 'drug abuse',
        # Psikiyatrik
        'depression', 'major depressive disorder', 'anxiety', 'ptsd',
        'schizophrenia', 'bipolar disorder', 'autism',
        # Metabolik
        'type 2 diabetes', 'obesity', 'bmi', 'metabolic syndrome',
        'insulin resistance', 'fatty liver',
        # Kanser
        'breast cancer', 'lung cancer', 'colorectal cancer', 'prostate cancer',
        'leukemia', 'lymphoma', 'melanoma',
        # Norolojik
        'alzheimer', 'parkinson', 'dementia', 'multiple sclerosis',
        # Kardiyovaskuler
        'cardiovascular disease', 'hypertension', 'atherosclerosis',
        'heart failure', 'stroke',
        # Solunum
        'asthma', 'copd', 'lung function',
        # Yeme bozukluklari
        'anorexia nervosa', 'bulimia', 'eating disorder',
        # Otoimmun
        'rheumatoid arthritis', 'lupus', 'crohn disease', 'ulcerative colitis',
        # Diger
        'aging', 'mortality', 'inflammation', 'infection', 'hiv'
    ]
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.engine = None
        
        if self.db_url and HAS_DB:
            try:
                self.engine = create_engine(self.db_url)
            except:
                pass
        
        # Pipeline durumu
        self.jobs: Dict[str, PipelineJob] = {}
        self.current_job: Optional[PipelineJob] = None
        
        # Istatistikler
        self.stats = {
            'total_diseases': 0,
            'total_substances': 0,
            'total_medications': 0,
            'total_cpg_markers': 0,
            'last_sync': None
        }
        
        self._load_stats()
    
    def _load_stats(self):
        """Veritabanindan istatistikleri yukle"""
        if not self.engine:
            return
        
        try:
            with self.engine.connect() as conn:
                # Hastalik sayisi
                result = conn.execute(text("SELECT COUNT(DISTINCT trait) FROM ewas_associations"))
                self.stats['total_diseases'] = result.scalar() or 0
                
                # CpG sayisi
                result = conn.execute(text("SELECT COUNT(DISTINCT cpg) FROM ewas_associations"))
                self.stats['total_cpg_markers'] = result.scalar() or 0
                
        except Exception as e:
            pass
    
    def create_tables(self) -> bool:
        """Veritabani tablolarini olustur"""
        if not self.engine:
            return False
        
        create_sql = """
        -- EWAS Associations
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
        
        -- Disease Signatures
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
            model_version VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Substance Signatures
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
        
        -- Therapeutic Medications
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
        
        -- ETL Job History
        CREATE TABLE IF NOT EXISTS etl_job_history (
            id SERIAL PRIMARY KEY,
            job_id VARCHAR(100) NOT NULL,
            job_type VARCHAR(50),
            status VARCHAR(20),
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            records_processed INTEGER,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Model Registry
        CREATE TABLE IF NOT EXISTS model_registry (
            id SERIAL PRIMARY KEY,
            model_id VARCHAR(100) NOT NULL UNIQUE,
            model_type VARCHAR(50),
            target_name VARCHAR(255),
            target_category VARCHAR(100),
            n_features INTEGER,
            auc_score FLOAT,
            sensitivity FLOAT,
            specificity FLOAT,
            model_path VARCHAR(500),
            version VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Indexes
        CREATE INDEX IF NOT EXISTS idx_ewas_cpg ON ewas_associations(cpg);
        CREATE INDEX IF NOT EXISTS idx_ewas_trait ON ewas_associations(trait);
        CREATE INDEX IF NOT EXISTS idx_ewas_pvalue ON ewas_associations(p_value);
        CREATE INDEX IF NOT EXISTS idx_disease_cat ON disease_signatures(category);
        CREATE INDEX IF NOT EXISTS idx_substance_class ON substance_signatures(substance_class);
        CREATE INDEX IF NOT EXISTS idx_med_cat ON therapeutic_medications(category);
        """
        
        try:
            with self.engine.connect() as conn:
                for statement in create_sql.split(';'):
                    if statement.strip():
                        conn.execute(text(statement))
                conn.commit()
            return True
        except Exception as e:
            print(f"Tablo olusturma hatasi: {e}")
            return False
    
    def sync_ewas_catalog(self, traits: List[str] = None, 
                          progress_callback: Callable = None) -> Dict[str, Any]:
        """
        EWAS Catalog'u senkronize et
        
        Args:
            traits: Trait listesi (None ise oncelikliler)
            progress_callback: Ilerleme callback
        
        Returns:
            Senkronizasyon sonuclari
        """
        if traits is None:
            traits = self.PRIORITY_TRAITS
        
        job_id = f"ewas_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        job = PipelineJob(
            job_id=job_id,
            job_type='ewas_sync',
            status=PipelineStatus.RUNNING,
            started_at=datetime.now()
        )
        self.current_job = job
        self.jobs[job_id] = job
        
        results = {
            'traits_processed': 0,
            'associations_imported': 0,
            'errors': []
        }
        
        try:
            ewas_api = EWASCatalogAPI()
            
            for i, trait in enumerate(traits):
                job.progress = (i + 1) / len(traits)
                job.message = f"Isleniyor: {trait}"
                
                if progress_callback:
                    progress_callback(i + 1, len(traits), trait)
                
                # Bu trait icin iliskileri cek
                associations = ewas_api.search_trait(trait)
                
                if associations and self.engine:
                    # Veritabanina yaz
                    imported = self._import_ewas_associations(trait, associations)
                    results['associations_imported'] += imported
                
                results['traits_processed'] += 1
            
            job.status = PipelineStatus.COMPLETED
            job.completed_at = datetime.now()
            job.results = results
            
        except Exception as e:
            job.status = PipelineStatus.ERROR
            job.error = str(e)
            results['errors'].append(str(e))
        
        self.current_job = None
        self._update_stats()
        
        return results
    
    def _import_ewas_associations(self, trait: str, associations: List) -> int:
        """EWAS iliskilerini veritabanina aktar"""
        if not self.engine:
            return 0
        
        imported = 0
        
        with self.engine.connect() as conn:
            for assoc in associations:
                try:
                    conn.execute(text("""
                        INSERT INTO ewas_associations 
                        (cpg, trait, trait_category, beta, se, p_value, 
                         sample_size, study_id, pmid, gene, chromosome, position)
                        VALUES (:cpg, :trait, :category, :beta, :se, :pval,
                                :n, :study, :pmid, :gene, :chr, :pos)
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
                except:
                    continue
            
            conn.commit()
        
        return imported
    
    def sync_therapeutic_medications(self) -> Dict[str, Any]:
        """Terapotik ilaclari senkronize et"""
        results = {'medications_imported': 0, 'errors': []}
        
        if not self.engine:
            return results
        
        # DrugBankLite'dan verileri al
        drug_data = DrugBankLite.get_all_therapeutic_cpg_effects()
        
        with self.engine.connect() as conn:
            for drug_name, info in drug_data.items():
                try:
                    conn.execute(text("""
                        INSERT INTO therapeutic_medications
                        (medication_id, name_en, eaa_effect, mechanism_en, 
                         target_genes, affected_cpgs)
                        VALUES (:med_id, :name, :eaa, :mechanism, :genes, :cpgs)
                        ON CONFLICT (medication_id) DO UPDATE SET
                            eaa_effect = EXCLUDED.eaa_effect,
                            affected_cpgs = EXCLUDED.affected_cpgs
                    """), {
                        'med_id': drug_name.lower().replace(' ', '_'),
                        'name': drug_name.title(),
                        'eaa': info.get('eaa_effect', 0),
                        'mechanism': info.get('mechanism', ''),
                        'genes': info.get('genes', []),
                        'cpgs': json.dumps(info.get('cpg_effects', {}))
                    })
                    results['medications_imported'] += 1
                except Exception as e:
                    results['errors'].append(f"{drug_name}: {e}")
            
            conn.commit()
        
        return results
    
    def train_all_models(self, min_cpgs: int = 5, max_pvalue: float = 1e-5) -> Dict[str, Any]:
        """Tum modelleri egit"""
        results = {'models_trained': 0, 'errors': []}
        
        trainer = AutoModelTrainer(self.db_url)
        
        try:
            trainer.train_from_database(min_cpgs=min_cpgs, max_pvalue=max_pvalue)
            
            # Model sayisini al
            summary = trainer.get_model_summary()
            results['models_trained'] = summary.get('total_models', 0)
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def sync_geo_datasets(self, max_studies: int = 50) -> Dict[str, Any]:
        """
        GEO DataSets'ten metilasyon calismalarini senkronize et
        
        Faz 3 - GEO veri entegrasyonu
        """
        results = {
            'addiction_studies': {},
            'disease_studies': {},
            'errors': []
        }
        
        if not HAS_GEO_UNODC:
            results['errors'].append("GEO modulu yuklenemedi")
            return results
        
        try:
            geo_loader = GEODataLoader(self.db_url)
            
            # Bagimlilik calismalari
            results['addiction_studies'] = geo_loader.import_addiction_studies(
                max_studies=max_studies // 2
            )
            
            # Hastalik calismalari
            results['disease_studies'] = geo_loader.import_disease_studies(
                max_studies=max_studies // 2
            )
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def sync_unodc_substances(self) -> Dict[str, Any]:
        """
        UNODC programli maddelerini senkronize et
        
        Faz 2 - UNODC madde genisletme
        """
        results = {
            'substances_loaded': 0,
            'categories': {},
            'errors': []
        }
        
        if not HAS_GEO_UNODC:
            results['errors'].append("UNODC modulu yuklenemedi")
            return results
        
        try:
            unodc_loader = UNODCDataLoader(self.db_url)
            results = unodc_loader.load_scheduled_substances()
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def run_continuous_learning(self) -> Dict[str, Any]:
        """
        Surekli ogrenme sistemini calistir
        
        Faz 4 - Surekli ogrenme, model guncelleme
        """
        results = {
            'update_results': {},
            'models_retrained': 0,
            'errors': []
        }
        
        if not HAS_GEO_UNODC:
            results['errors'].append("Continuous learning modulu yuklenemedi")
            return results
        
        try:
            learning_system = ContinuousLearningSystem(self.db_url)
            results['update_results'] = learning_system.run_scheduled_update()
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def run_full_pipeline(self, progress_callback: Callable = None) -> Dict[str, Any]:
        """
        Tam ETL pipeline calistir
        
        Adimlar (Faz 0-4):
        1. Tablolari olustur (Faz 0)
        2. EWAS verilerini senkronize et (Faz 1)
        3. PharmGKB/Terapotik ilaclari yukle (Faz 1)
        4. UNODC madde genisletme (Faz 2)
        5. GEO veri entegrasyonu (Faz 3)
        6. Modelleri egit (Faz 4)
        7. Surekli ogrenme baslat (Faz 4)
        """
        results = {
            'tables_created': False,
            'ewas_sync': {},
            'medications_sync': {},
            'unodc_sync': {},
            'geo_sync': {},
            'models_trained': {},
            'continuous_learning': {},
            'started_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        total_steps = 7
        
        # Faz 0: Tablolar
        if progress_callback:
            progress_callback(1, total_steps, "Faz 0: Veritabani tablolari olusturuluyor...")
        results['tables_created'] = self.create_tables()
        
        # Faz 1: EWAS Sync
        if progress_callback:
            progress_callback(2, total_steps, "Faz 1: EWAS verileri senkronize ediliyor...")
        results['ewas_sync'] = self.sync_ewas_catalog()
        
        # Faz 1: Medications (PharmGKB)
        if progress_callback:
            progress_callback(3, total_steps, "Faz 1: PharmGKB/Terapotik ilaclar yukleniyor...")
        results['medications_sync'] = self.sync_therapeutic_medications()
        
        # Faz 2: UNODC Madde Genisletme
        if progress_callback:
            progress_callback(4, total_steps, "Faz 2: UNODC maddeleri senkronize ediliyor...")
        results['unodc_sync'] = self.sync_unodc_substances()
        
        # Faz 3: GEO Veri Entegrasyonu
        if progress_callback:
            progress_callback(5, total_steps, "Faz 3: GEO metilasyon calismalari yukleniyor...")
        results['geo_sync'] = self.sync_geo_datasets()
        
        # Faz 4: Train Models
        if progress_callback:
            progress_callback(6, total_steps, "Faz 4: Modeller egitiliyor...")
        results['models_trained'] = self.train_all_models()
        
        # Faz 4: Continuous Learning
        if progress_callback:
            progress_callback(7, total_steps, "Faz 4: Surekli ogrenme sistemi baslatiliyor...")
        results['continuous_learning'] = self.run_continuous_learning()
        
        results['completed_at'] = datetime.now().isoformat()
        
        self._update_stats()
        
        return results
    
    def _update_stats(self):
        """Istatistikleri guncelle"""
        if not self.engine:
            return
        
        try:
            with self.engine.connect() as conn:
                # Hastalik sayisi
                result = conn.execute(text(
                    "SELECT COUNT(DISTINCT trait) FROM ewas_associations"
                ))
                self.stats['total_diseases'] = result.scalar() or 0
                
                # CpG sayisi
                result = conn.execute(text(
                    "SELECT COUNT(DISTINCT cpg) FROM ewas_associations"
                ))
                self.stats['total_cpg_markers'] = result.scalar() or 0
                
                # Ilac sayisi
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM therapeutic_medications"
                ))
                self.stats['total_medications'] = result.scalar() or 0
                
                self.stats['last_sync'] = datetime.now().isoformat()
                
        except:
            pass
    
    def get_data_sources(self) -> List[Dict]:
        """Veri kaynaklarini listele"""
        sources = []
        
        for source_id, source in self.DATA_SOURCES.items():
            sources.append({
                'id': source.source_id,
                'name': source.name,
                'description': source.description,
                'api_url': source.api_url,
                'last_sync': source.last_sync.isoformat() if source.last_sync else None,
                'record_count': source.record_count,
                'status': source.status,
                'requires_api_key': source.requires_api_key
            })
        
        return sources
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Pipeline durumunu dondur"""
        return {
            'current_job': {
                'job_id': self.current_job.job_id if self.current_job else None,
                'status': self.current_job.status.value if self.current_job else 'idle',
                'progress': self.current_job.progress if self.current_job else 0,
                'message': self.current_job.message if self.current_job else ''
            },
            'stats': self.stats,
            'recent_jobs': [
                {
                    'job_id': job.job_id,
                    'type': job.job_type,
                    'status': job.status.value,
                    'started': job.started_at.isoformat() if job.started_at else None
                }
                for job in list(self.jobs.values())[-5:]
            ]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Detayli istatistikler"""
        self._update_stats()
        
        category_stats = {}
        
        if self.engine:
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT trait_category, COUNT(DISTINCT trait), COUNT(*)
                        FROM ewas_associations
                        WHERE trait_category IS NOT NULL
                        GROUP BY trait_category
                    """))
                    
                    for row in result:
                        category_stats[row[0] or 'other'] = {
                            'traits': row[1],
                            'associations': row[2]
                        }
            except:
                pass
        
        return {
            **self.stats,
            'categories': category_stats,
            'data_sources': len(self.DATA_SOURCES)
        }


# Singleton instance
_pipeline_manager = None

def get_pipeline_manager() -> ETLPipelineManager:
    """Global pipeline manager instance"""
    global _pipeline_manager
    if _pipeline_manager is None:
        _pipeline_manager = ETLPipelineManager()
    return _pipeline_manager
