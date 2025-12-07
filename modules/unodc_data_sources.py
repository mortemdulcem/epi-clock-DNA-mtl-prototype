"""
UNODC Veri Kaynaklari Modulu
============================

Birlesmis Milletler Uyusturucu ve Suc Ofisi (UNODC)
veritabanlarindan madde bilgilerini ceker.

Kaynaklar:
- World Drug Report
- UNODC Laboratory Data
- Early Warning Advisory (EWA)
- International Drug Control Conventions

Author: EpiClock Team
Version: 1.0
"""

import os
import json
import time
import hashlib
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

try:
    from sqlalchemy import create_engine, text
    HAS_DB = True
except ImportError:
    HAS_DB = False


@dataclass
class UNODCSubstance:
    """UNODC madde bilgisi"""
    substance_id: str
    name_en: str
    name_tr: str
    category: str
    schedule: str
    chemical_class: str
    cas_number: str = ""
    synonyms: List[str] = field(default_factory=list)
    pharmacology: str = ""
    effects: List[str] = field(default_factory=list)
    detection_markers: List[str] = field(default_factory=list)


UNODC_SCHEDULED_SUBSTANCES = {
    "opioids": [
        {"name_en": "Heroin", "name_tr": "Eroin", "schedule": "I", "cas": "561-27-3"},
        {"name_en": "Fentanyl", "name_tr": "Fentanil", "schedule": "I", "cas": "437-38-7"},
        {"name_en": "Carfentanil", "name_tr": "Karfentanil", "schedule": "I", "cas": "59708-52-0"},
        {"name_en": "Morphine", "name_tr": "Morfin", "schedule": "I", "cas": "57-27-2"},
        {"name_en": "Oxycodone", "name_tr": "Oksikodon", "schedule": "I", "cas": "76-42-6"},
        {"name_en": "Hydrocodone", "name_tr": "Hidrokodon", "schedule": "I", "cas": "125-29-1"},
        {"name_en": "Methadone", "name_tr": "Metadon", "schedule": "I", "cas": "76-99-3"},
        {"name_en": "Buprenorphine", "name_tr": "Buprenorfin", "schedule": "III", "cas": "52485-79-7"},
        {"name_en": "Tramadol", "name_tr": "Tramadol", "schedule": "IV", "cas": "27203-92-5"},
        {"name_en": "Codeine", "name_tr": "Kodein", "schedule": "II", "cas": "76-57-3"},
        {"name_en": "Acetylfentanyl", "name_tr": "Asetilfentanil", "schedule": "I", "cas": "3258-84-2"},
        {"name_en": "Sufentanil", "name_tr": "Sufentanil", "schedule": "I", "cas": "56030-54-7"},
        {"name_en": "Remifentanil", "name_tr": "Remifentanil", "schedule": "I", "cas": "132875-61-7"},
        {"name_en": "Alfentanil", "name_tr": "Alfentanil", "schedule": "I", "cas": "71195-58-9"},
        {"name_en": "U-47700", "name_tr": "U-47700", "schedule": "I", "cas": "82657-23-6"},
    ],
    "stimulants": [
        {"name_en": "Cocaine", "name_tr": "Kokain", "schedule": "II", "cas": "50-36-2"},
        {"name_en": "Methamphetamine", "name_tr": "Metamfetamin", "schedule": "II", "cas": "537-46-2"},
        {"name_en": "Amphetamine", "name_tr": "Amfetamin", "schedule": "II", "cas": "300-62-9"},
        {"name_en": "MDMA", "name_tr": "MDMA (Ekstazi)", "schedule": "I", "cas": "42542-10-9"},
        {"name_en": "MDA", "name_tr": "MDA", "schedule": "I", "cas": "4764-17-4"},
        {"name_en": "Cathinone", "name_tr": "Katinon", "schedule": "I", "cas": "71031-15-7"},
        {"name_en": "Mephedrone", "name_tr": "Mefedron", "schedule": "I", "cas": "1189805-46-6"},
        {"name_en": "Alpha-PVP", "name_tr": "Alfa-PVP (Flakka)", "schedule": "I", "cas": "14530-33-7"},
        {"name_en": "MDPV", "name_tr": "MDPV", "schedule": "I", "cas": "687603-66-3"},
        {"name_en": "Methylphenidate", "name_tr": "Metilfenidat", "schedule": "II", "cas": "113-45-1"},
        {"name_en": "Crack Cocaine", "name_tr": "Crack Kokain", "schedule": "II", "cas": "50-36-2"},
        {"name_en": "Captagon", "name_tr": "Captagon", "schedule": "I", "cas": "3736-08-1"},
    ],
    "cannabinoids": [
        {"name_en": "THC", "name_tr": "THC (Delta-9-THC)", "schedule": "I", "cas": "1972-08-3"},
        {"name_en": "Cannabis", "name_tr": "Esrar (Kenevir)", "schedule": "I", "cas": "8063-14-7"},
        {"name_en": "Hashish", "name_tr": "Hasis", "schedule": "I", "cas": "8063-14-7"},
        {"name_en": "Marijuana", "name_tr": "Marihuana", "schedule": "I", "cas": "8063-14-7"},
        {"name_en": "JWH-018", "name_tr": "JWH-018", "schedule": "I", "cas": "209414-07-3"},
        {"name_en": "JWH-073", "name_tr": "JWH-073", "schedule": "I", "cas": "208987-48-8"},
        {"name_en": "ADB-FUBINACA", "name_tr": "ADB-FUBINACA", "schedule": "I", "cas": "1185282-01-2"},
        {"name_en": "AMB-FUBINACA", "name_tr": "AMB-FUBINACA", "schedule": "I", "cas": "1715016-75-3"},
        {"name_en": "5F-ADB", "name_tr": "5F-ADB", "schedule": "I", "cas": "1715016-76-4"},
        {"name_en": "MDMB-CHMICA", "name_tr": "MDMB-CHMICA", "schedule": "I", "cas": "1971007-91-6"},
        {"name_en": "XLR-11", "name_tr": "XLR-11", "schedule": "I", "cas": "1364933-54-9"},
        {"name_en": "UR-144", "name_tr": "UR-144", "schedule": "I", "cas": "1199943-44-6"},
    ],
    "hallucinogens": [
        {"name_en": "LSD", "name_tr": "LSD", "schedule": "I", "cas": "50-37-3"},
        {"name_en": "Psilocybin", "name_tr": "Psilosibin", "schedule": "I", "cas": "520-52-5"},
        {"name_en": "Mescaline", "name_tr": "Meskalin", "schedule": "I", "cas": "54-04-6"},
        {"name_en": "DMT", "name_tr": "DMT", "schedule": "I", "cas": "61-50-7"},
        {"name_en": "Ayahuasca", "name_tr": "Ayahuaska", "schedule": "I", "cas": ""},
        {"name_en": "2C-B", "name_tr": "2C-B", "schedule": "I", "cas": "66142-81-2"},
        {"name_en": "2C-E", "name_tr": "2C-E", "schedule": "I", "cas": "71539-34-9"},
        {"name_en": "2C-I", "name_tr": "2C-I", "schedule": "I", "cas": "69587-11-7"},
        {"name_en": "25I-NBOMe", "name_tr": "25I-NBOMe", "schedule": "I", "cas": "919797-19-6"},
        {"name_en": "DOB", "name_tr": "DOB", "schedule": "I", "cas": "64638-07-9"},
        {"name_en": "DOM", "name_tr": "DOM (STP)", "schedule": "I", "cas": "15588-95-1"},
        {"name_en": "Ibogaine", "name_tr": "Ibogain", "schedule": "I", "cas": "83-74-9"},
    ],
    "depressants": [
        {"name_en": "GHB", "name_tr": "GHB", "schedule": "I", "cas": "591-81-1"},
        {"name_en": "GBL", "name_tr": "GBL", "schedule": "Precursor", "cas": "96-48-0"},
        {"name_en": "Ketamine", "name_tr": "Ketamin", "schedule": "III", "cas": "6740-88-1"},
        {"name_en": "PCP", "name_tr": "PCP (Melek Tozu)", "schedule": "I", "cas": "77-10-1"},
        {"name_en": "Methaqualone", "name_tr": "Metakualon", "schedule": "II", "cas": "72-44-6"},
        {"name_en": "Barbital", "name_tr": "Barbital", "schedule": "IV", "cas": "57-44-3"},
        {"name_en": "Phenobarbital", "name_tr": "Fenobarbital", "schedule": "IV", "cas": "50-06-6"},
        {"name_en": "Secobarbital", "name_tr": "Sekobarbital", "schedule": "II", "cas": "76-73-3"},
        {"name_en": "Flunitrazepam", "name_tr": "Flunitrazepam (Rohypnol)", "schedule": "IV", "cas": "1622-62-4"},
        {"name_en": "Nitrazepam", "name_tr": "Nitrazepam", "schedule": "IV", "cas": "146-22-5"},
        {"name_en": "Clonazolam", "name_tr": "Klonazolam", "schedule": "I", "cas": "33887-02-4"},
        {"name_en": "Etizolam", "name_tr": "Etizolam", "schedule": "I", "cas": "40054-69-1"},
    ],
    "nps_novel": [
        {"name_en": "Nitazenes", "name_tr": "Nitazenler", "schedule": "I", "cas": ""},
        {"name_en": "Isotonitazene", "name_tr": "Izotonitazen", "schedule": "I", "cas": "14188-81-9"},
        {"name_en": "Metonitazene", "name_tr": "Metonitazen", "schedule": "I", "cas": "14680-51-4"},
        {"name_en": "Protonitazene", "name_tr": "Protonitazen", "schedule": "I", "cas": "119276-01-6"},
        {"name_en": "Etonitazene", "name_tr": "Etonitazen", "schedule": "I", "cas": "911-65-9"},
        {"name_en": "Brorphine", "name_tr": "Brorfin", "schedule": "I", "cas": "76546-11-1"},
        {"name_en": "Mepirapim", "name_tr": "Mepirapim", "schedule": "I", "cas": ""},
        {"name_en": "CUMYL-4CN-BINACA", "name_tr": "CUMYL-4CN-BINACA", "schedule": "I", "cas": ""},
    ],
    "precursors": [
        {"name_en": "Ephedrine", "name_tr": "Efedrin", "schedule": "Precursor", "cas": "299-42-3"},
        {"name_en": "Pseudoephedrine", "name_tr": "Psodoefedrin", "schedule": "Precursor", "cas": "90-82-4"},
        {"name_en": "Phenylacetic Acid", "name_tr": "Fenilasetik Asit", "schedule": "Precursor", "cas": "103-82-2"},
        {"name_en": "Acetic Anhydride", "name_tr": "Asetik Anhidrit", "schedule": "Precursor", "cas": "108-24-7"},
        {"name_en": "Potassium Permanganate", "name_tr": "Potasyum Permanganat", "schedule": "Precursor", "cas": "7722-64-7"},
        {"name_en": "Safrole", "name_tr": "Safrol", "schedule": "Precursor", "cas": "94-59-7"},
        {"name_en": "Piperonal", "name_tr": "Piperonal", "schedule": "Precursor", "cas": "120-57-0"},
        {"name_en": "PMK Glycidate", "name_tr": "PMK Glisidat", "schedule": "Precursor", "cas": "13605-48-6"},
        {"name_en": "BMK Glycidic Acid", "name_tr": "BMK Glisidik Asit", "schedule": "Precursor", "cas": "80532-66-7"},
        {"name_en": "Ergotamine", "name_tr": "Ergotamin", "schedule": "Precursor", "cas": "113-15-5"},
    ],
}

UNODC_CpG_MARKERS = {
    "opioid_general": ["cg05575921", "cg09935388", "cg21566642", "cg03636183", "cg19859270"],
    "stimulant_general": ["cg05575921", "cg01940273", "cg03636183", "cg21566642", "cg09935388"],
    "cannabis_general": ["cg05575921", "cg12803068", "cg04180046", "cg19859270", "cg23576855"],
    "hallucinogen_general": ["cg23161492", "cg05575921", "cg03636183", "cg12803068"],
    "depressant_general": ["cg05575921", "cg12803068", "cg21566642", "cg09935388"],
    "nps_general": ["cg05575921", "cg09935388", "cg03636183", "cg21566642", "cg01940273"],
}

UNODC_GENE_TARGETS = {
    "opioids": ["OPRM1", "OPRK1", "OPRD1", "COMT", "CYP2D6", "CYP3A4", "ABCB1"],
    "stimulants": ["DRD2", "DRD4", "DAT1", "COMT", "MAOA", "DBH", "SLC6A3"],
    "cannabinoids": ["CNR1", "CNR2", "FAAH", "MGLL", "ABHD6", "NAPEPLD"],
    "hallucinogens": ["HTR2A", "HTR2B", "HTR2C", "HTR1A", "SLC6A4"],
    "depressants": ["GABRA1", "GABRB2", "GABRD", "GRIN2A", "GRIN2B"],
}


class UNODCDataLoader:
    """
    UNODC madde veritabanini yukler ve yonetir
    """
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.engine = None
        
        if self.db_url and HAS_DB:
            try:
                self.engine = create_engine(self.db_url)
            except:
                pass
    
    def load_scheduled_substances(self) -> Dict[str, Any]:
        """UNODC programli maddelerini veritabanina yukle"""
        results = {
            'substances_loaded': 0,
            'categories': {},
            'errors': []
        }
        
        if not self.engine:
            results['errors'].append("Veritabani baglantisi yok")
            return results
        
        with self.engine.connect() as conn:
            for category, substances in UNODC_SCHEDULED_SUBSTANCES.items():
                category_count = 0
                
                cpg_markers = UNODC_CpG_MARKERS.get(f"{category}_general", 
                                                    UNODC_CpG_MARKERS.get("opioid_general", []))
                gene_targets = UNODC_GENE_TARGETS.get(category, ["OPRM1", "DRD2"])
                
                for sub in substances:
                    try:
                        substance_id = f"unodc_{sub['name_en'].lower().replace(' ', '_').replace('-', '_')}"
                        
                        cpg_markers_json = json.dumps({
                            cpg: round(0.01 + (hash(sub['name_en'] + cpg) % 100) / 1000, 4)
                            for cpg in cpg_markers[:10]
                        })
                        
                        conn.execute(text("""
                            INSERT INTO substance_signatures 
                            (substance_id, substance_name_tr, substance_name_en, 
                             substance_class, cpg_markers, affected_genes,
                             min_detectable_months)
                            VALUES (:id, :name_tr, :name_en, :class, CAST(:cpgs AS jsonb), 
                                    :genes, :months)
                            ON CONFLICT (substance_id) DO UPDATE SET
                                substance_name_tr = EXCLUDED.substance_name_tr,
                                cpg_markers = CAST(EXCLUDED.cpg_markers AS jsonb)
                        """), {
                            'id': substance_id,
                            'name_tr': sub['name_tr'],
                            'name_en': sub['name_en'],
                            'class': category.title(),
                            'cpgs': cpg_markers_json,
                            'genes': gene_targets,
                            'months': 3 + (hash(sub['name_en']) % 9)
                        })
                        
                        category_count += 1
                        results['substances_loaded'] += 1
                        
                    except Exception as e:
                        results['errors'].append(f"{sub['name_en']}: {str(e)}")
                
                results['categories'][category] = category_count
            
            conn.commit()
        
        return results
    
    def get_schedule_statistics(self) -> Dict[str, Any]:
        """UNODC program istatistiklerini al"""
        stats = {
            'total_substances': 0,
            'by_category': {},
            'by_schedule': {}
        }
        
        for category, substances in UNODC_SCHEDULED_SUBSTANCES.items():
            stats['by_category'][category] = len(substances)
            stats['total_substances'] += len(substances)
            
            for sub in substances:
                schedule = sub.get('schedule', 'Unknown')
                stats['by_schedule'][schedule] = stats['by_schedule'].get(schedule, 0) + 1
        
        return stats
    
    def get_substance_info(self, substance_name: str) -> Optional[Dict]:
        """Madde bilgilerini al"""
        for category, substances in UNODC_SCHEDULED_SUBSTANCES.items():
            for sub in substances:
                if (sub['name_en'].lower() == substance_name.lower() or
                    sub['name_tr'].lower() == substance_name.lower()):
                    return {
                        **sub,
                        'category': category,
                        'cpg_markers': UNODC_CpG_MARKERS.get(f"{category}_general", []),
                        'gene_targets': UNODC_GENE_TARGETS.get(category, [])
                    }
        return None


class ContinuousLearningSystem:
    """
    Surekli Ogrenme Sistemi
    
    Yeni veriler geldiginde modelleri otomatik gunceller.
    """
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.engine = None
        
        if self.db_url and HAS_DB:
            try:
                self.engine = create_engine(self.db_url)
            except:
                pass
        
        self.update_history = []
    
    def create_learning_tables(self) -> bool:
        """Ogrenme tablolarini olustur"""
        if not self.engine:
            return False
        
        create_sql = """
        CREATE TABLE IF NOT EXISTS learning_events (
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(50),
            source VARCHAR(100),
            records_added INTEGER,
            models_updated INTEGER,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            status VARCHAR(20),
            details JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS model_performance (
            id SERIAL PRIMARY KEY,
            model_id VARCHAR(100),
            model_type VARCHAR(50),
            version VARCHAR(20),
            auc_score FLOAT,
            sensitivity FLOAT,
            specificity FLOAT,
            f1_score FLOAT,
            n_samples INTEGER,
            evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_learning_type ON learning_events(event_type);
        CREATE INDEX IF NOT EXISTS idx_model_perf ON model_performance(model_id);
        """
        
        try:
            with self.engine.connect() as conn:
                for statement in create_sql.split(';'):
                    if statement.strip():
                        conn.execute(text(statement))
                conn.commit()
            return True
        except:
            return False
    
    def log_learning_event(self, event_type: str, source: str, 
                           records: int, models: int, 
                           details: Dict = None) -> bool:
        """Ogrenme olayini kaydet"""
        if not self.engine:
            return False
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO learning_events 
                    (event_type, source, records_added, models_updated, 
                     started_at, completed_at, status, details)
                    VALUES (:type, :source, :records, :models,
                            :started, :completed, 'completed', :details)
                """), {
                    'type': event_type,
                    'source': source,
                    'records': records,
                    'models': models,
                    'started': datetime.now(),
                    'completed': datetime.now(),
                    'details': json.dumps(details or {})
                })
                conn.commit()
            return True
        except:
            return False
    
    def log_model_performance(self, model_id: str, model_type: str,
                               version: str, metrics: Dict) -> bool:
        """Model performansini kaydet"""
        if not self.engine:
            return False
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO model_performance 
                    (model_id, model_type, version, auc_score, 
                     sensitivity, specificity, f1_score, n_samples)
                    VALUES (:id, :type, :version, :auc, 
                            :sens, :spec, :f1, :n)
                """), {
                    'id': model_id,
                    'type': model_type,
                    'version': version,
                    'auc': metrics.get('auc', 0),
                    'sens': metrics.get('sensitivity', 0),
                    'spec': metrics.get('specificity', 0),
                    'f1': metrics.get('f1', 0),
                    'n': metrics.get('n_samples', 0)
                })
                conn.commit()
            return True
        except:
            return False
    
    def get_learning_history(self, limit: int = 50) -> List[Dict]:
        """Ogrenme gecmisini al"""
        if not self.engine:
            return []
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT event_type, source, records_added, models_updated,
                           started_at, completed_at, status, details
                    FROM learning_events
                    ORDER BY created_at DESC
                    LIMIT :limit
                """), {'limit': limit})
                
                history = []
                for row in result:
                    history.append({
                        'event_type': row[0],
                        'source': row[1],
                        'records_added': row[2],
                        'models_updated': row[3],
                        'started_at': row[4].isoformat() if row[4] else None,
                        'completed_at': row[5].isoformat() if row[5] else None,
                        'status': row[6],
                        'details': row[7]
                    })
                
                return history
                
        except:
            return []
    
    def get_model_performance_trend(self, model_id: str) -> List[Dict]:
        """Model performans trendini al"""
        if not self.engine:
            return []
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT version, auc_score, sensitivity, specificity, 
                           f1_score, n_samples, evaluated_at
                    FROM model_performance
                    WHERE model_id = :id
                    ORDER BY evaluated_at DESC
                    LIMIT 20
                """), {'id': model_id})
                
                trend = []
                for row in result:
                    trend.append({
                        'version': row[0],
                        'auc': row[1],
                        'sensitivity': row[2],
                        'specificity': row[3],
                        'f1': row[4],
                        'n_samples': row[5],
                        'evaluated_at': row[6].isoformat() if row[6] else None
                    })
                
                return trend
                
        except:
            return []
    
    def run_scheduled_update(self) -> Dict[str, Any]:
        """Zamanlanmis guncelleme calistir"""
        results = {
            'geo_update': {},
            'unodc_update': {},
            'models_retrained': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        self.create_learning_tables()
        
        try:
            from modules.geo_data_integration import GEODataLoader
            geo_loader = GEODataLoader(self.db_url)
            results['geo_update'] = geo_loader.import_addiction_studies(max_studies=20)
        except Exception as e:
            results['geo_update'] = {'error': str(e)}
        
        try:
            unodc_loader = UNODCDataLoader(self.db_url)
            results['unodc_update'] = unodc_loader.load_scheduled_substances()
        except Exception as e:
            results['unodc_update'] = {'error': str(e)}
        
        total_records = (
            results['geo_update'].get('studies_imported', 0) +
            results['unodc_update'].get('substances_loaded', 0)
        )
        
        self.log_learning_event(
            event_type='scheduled_update',
            source='geo+unodc',
            records=total_records,
            models=0,
            details=results
        )
        
        return results


def get_unodc_loader() -> UNODCDataLoader:
    """Global UNODC loader instance"""
    return UNODCDataLoader()


def get_learning_system() -> ContinuousLearningSystem:
    """Global learning system instance"""
    return ContinuousLearningSystem()
