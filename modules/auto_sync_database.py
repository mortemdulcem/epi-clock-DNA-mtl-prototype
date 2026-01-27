# -*- coding: utf-8 -*-
"""
EpiClock v4.0 - Auto-Sync Database Module
Automatic synchronization with external genomic and substance databases

Supported Databases:
- NHGRI-EBI GWAS Catalog (https://www.ebi.ac.uk/gwas/)
- EWAS Catalog (https://www.ewascatalog.org/)
- PubChem (https://pubchem.ncbi.nlm.nih.gov/)
- DrugBank (reference data)
- PharmGKB (https://www.pharmgkb.org/)

Author: nrcdnl94
"""

import os
import json
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
import threading
import time

import pandas as pd
import numpy as np

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float, JSON
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base() if SQLALCHEMY_AVAILABLE else None


# =============================================================================
# DATABASE MODELS
# =============================================================================

if SQLALCHEMY_AVAILABLE:
    class SyncedSubstance(Base):
        __tablename__ = 'synced_substances'
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        external_id = Column(String(100), unique=True, nullable=False)
        name = Column(String(500), nullable=False)
        source = Column(String(50), nullable=False)
        category = Column(String(100))
        chemical_formula = Column(String(200))
        smiles = Column(Text)
        inchi_key = Column(String(50))
        cas_number = Column(String(50))
        addiction_potential = Column(Float)
        cpg_markers = Column(JSON)
        extra_data = Column(JSON)
        data_hash = Column(String(64))
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        is_active = Column(Boolean, default=True)

    class SyncedGWASStudy(Base):
        __tablename__ = 'synced_gwas_studies'
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        study_accession = Column(String(50), unique=True, nullable=False)
        pmid = Column(String(20))
        title = Column(Text)
        trait = Column(String(500))
        mapped_trait = Column(String(500))
        p_value = Column(Float)
        risk_allele = Column(String(100))
        risk_allele_frequency = Column(Float)
        snp_id = Column(String(50))
        gene_name = Column(String(100))
        chromosome = Column(String(10))
        position = Column(Integer)
        sample_size = Column(Integer)
        ancestry = Column(String(200))
        source = Column(String(50), default='GWAS_Catalog')
        extra_data = Column(JSON)
        data_hash = Column(String(64))
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class SyncedEWASMarker(Base):
        __tablename__ = 'synced_ewas_markers'
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        cpg_id = Column(String(20), nullable=False)
        gene = Column(String(100))
        chromosome = Column(String(10))
        position = Column(Integer)
        trait = Column(String(500))
        exposure = Column(String(500))
        p_value = Column(Float)
        effect_size = Column(Float)
        direction = Column(String(20))
        pmid = Column(String(20))
        sample_size = Column(Integer)
        tissue = Column(String(100))
        array_type = Column(String(50))
        source = Column(String(50), default='EWAS_Catalog')
        extra_data = Column(JSON)
        data_hash = Column(String(64))
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class SyncLog(Base):
        __tablename__ = 'sync_logs'
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        source = Column(String(50), nullable=False)
        sync_type = Column(String(50))
        status = Column(String(20))
        records_fetched = Column(Integer, default=0)
        records_added = Column(Integer, default=0)
        records_updated = Column(Integer, default=0)
        records_skipped = Column(Integer, default=0)
        error_message = Column(Text)
        started_at = Column(DateTime, default=datetime.utcnow)
        completed_at = Column(DateTime)
        duration_seconds = Column(Float)


# =============================================================================
# API CLIENTS
# =============================================================================

@dataclass
class APIConfig:
    """Configuration for API endpoints"""
    name: str
    base_url: str
    rate_limit: int = 10
    timeout: int = 30
    requires_auth: bool = False
    auth_header: Optional[str] = None


class GWASCatalogClient:
    """Client for NHGRI-EBI GWAS Catalog REST API"""
    
    CONFIG = APIConfig(
        name="GWAS Catalog",
        base_url="https://www.ebi.ac.uk/gwas/rest/api",
        rate_limit=10,
        timeout=60
    )
    
    ADDICTION_TRAITS = [
        "alcohol dependence",
        "alcohol consumption",
        "smoking behavior",
        "nicotine dependence",
        "cannabis use",
        "opioid dependence",
        "cocaine dependence",
        "substance use disorder",
        "drug addiction",
        "gambling disorder"
    ]
    
    def __init__(self):
        self.session = requests.Session() if REQUESTS_AVAILABLE else None
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Enforce rate limiting"""
        elapsed = time.time() - self.last_request_time
        min_interval = 1.0 / self.CONFIG.rate_limit
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_request_time = time.time()
    
    def fetch_addiction_studies(self, limit: int = 1000) -> List[Dict]:
        """Fetch addiction-related GWAS studies"""
        if not REQUESTS_AVAILABLE:
            logger.warning("requests library not available, using simulated data")
            return self._get_simulated_data()
        
        all_studies = []
        
        for trait in self.ADDICTION_TRAITS:
            try:
                self._rate_limit()
                
                url = f"{self.CONFIG.base_url}/efoTraits/search/findByEfoTrait"
                params = {"trait": trait, "size": limit}
                
                response = self.session.get(url, params=params, timeout=self.CONFIG.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    studies = data.get("_embedded", {}).get("efoTraits", [])
                    
                    for study in studies:
                        all_studies.append({
                            "trait": trait,
                            "study_data": study,
                            "source": "GWAS_Catalog",
                            "fetched_at": datetime.utcnow().isoformat()
                        })
                        
                    logger.info(f"Fetched {len(studies)} studies for trait: {trait}")
                else:
                    logger.warning(f"API error for {trait}: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error fetching {trait}: {str(e)}")
                
        return all_studies
    
    def fetch_associations(self, trait: str, limit: int = 500) -> List[Dict]:
        """Fetch SNP associations for a specific trait"""
        if not REQUESTS_AVAILABLE:
            return self._get_simulated_associations(trait)
        
        try:
            self._rate_limit()
            
            url = f"{self.CONFIG.base_url}/associations/search/findByEfoTrait"
            params = {"efoTrait": trait, "size": limit}
            
            response = self.session.get(url, params=params, timeout=self.CONFIG.timeout)
            
            if response.status_code == 200:
                data = response.json()
                associations = data.get("_embedded", {}).get("associations", [])
                return associations
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error fetching associations for {trait}: {str(e)}")
            return []
    
    def _get_simulated_data(self) -> List[Dict]:
        """Return simulated data when API is unavailable"""
        return [
            {
                "study_accession": f"GCST{90000000 + i}",
                "pmid": f"3{7000000 + i}",
                "trait": trait,
                "snp_id": f"rs{1000000 + i * 100 + j}",
                "gene_name": f"GENE{j}",
                "p_value": 10 ** (-np.random.uniform(7, 15)),
                "source": "GWAS_Catalog_Simulated",
                "fetched_at": datetime.utcnow().isoformat()
            }
            for i, trait in enumerate(self.ADDICTION_TRAITS)
            for j in range(5)
        ]
    
    def _get_simulated_associations(self, trait: str) -> List[Dict]:
        """Return simulated associations"""
        np.random.seed(hash(trait) % 2**32)
        return [
            {
                "snp_id": f"rs{np.random.randint(1000000, 9999999)}",
                "gene": np.random.choice(["DRD2", "OPRM1", "COMT", "ADH1B", "CHRNA5"]),
                "p_value": 10 ** (-np.random.uniform(7, 12)),
                "effect_size": np.random.uniform(-0.5, 0.5),
                "risk_allele_frequency": np.random.uniform(0.1, 0.5)
            }
            for _ in range(10)
        ]


class EWASCatalogClient:
    """Client for EWAS Catalog API"""
    
    CONFIG = APIConfig(
        name="EWAS Catalog",
        base_url="https://www.ewascatalog.org/api",
        rate_limit=5,
        timeout=60
    )
    
    ADDICTION_EXPOSURES = [
        "smoking",
        "alcohol",
        "cannabis",
        "cocaine",
        "opioid",
        "substance abuse",
        "nicotine"
    ]
    
    def __init__(self):
        self.session = requests.Session() if REQUESTS_AVAILABLE else None
        self.last_request_time = 0
        
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        min_interval = 1.0 / self.CONFIG.rate_limit
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_request_time = time.time()
    
    def fetch_addiction_markers(self, limit: int = 1000) -> List[Dict]:
        """Fetch addiction-related CpG markers"""
        if not REQUESTS_AVAILABLE:
            return self._get_simulated_markers()
        
        all_markers = []
        
        for exposure in self.ADDICTION_EXPOSURES:
            try:
                self._rate_limit()
                
                url = f"{self.CONFIG.base_url}/search"
                params = {"exposure": exposure, "limit": limit}
                
                response = self.session.get(url, params=params, timeout=self.CONFIG.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    markers = data.get("results", [])
                    
                    for marker in markers:
                        marker["exposure_category"] = exposure
                        marker["source"] = "EWAS_Catalog"
                        marker["fetched_at"] = datetime.utcnow().isoformat()
                        all_markers.append(marker)
                        
                    logger.info(f"Fetched {len(markers)} markers for: {exposure}")
                    
            except Exception as e:
                logger.error(f"Error fetching {exposure}: {str(e)}")
        
        return all_markers
    
    def _get_simulated_markers(self) -> List[Dict]:
        """Return simulated EWAS markers"""
        cpg_examples = [
            ("cg05575921", "AHRR", "5", 373378, "smoking"),
            ("cg03636183", "F2RL3", "19", 17000585, "smoking"),
            ("cg21566642", "ALPPL2", "2", 233284661, "alcohol"),
            ("cg06126421", "ALDH1A2", "15", 58680954, "alcohol"),
            ("cg04987734", "OPRM1", "6", 154360797, "opioid"),
            ("cg19859270", "GPR15", "3", 98251294, "cannabis"),
            ("cg14391737", "PRSS23", "11", 86510915, "cocaine"),
        ]
        
        markers = []
        for cpg, gene, chrom, pos, exposure in cpg_examples:
            for i in range(3):
                markers.append({
                    "cpg_id": cpg if i == 0 else f"cg{np.random.randint(10000000, 99999999)}",
                    "gene": gene,
                    "chromosome": chrom,
                    "position": pos + i * 1000,
                    "exposure": exposure,
                    "p_value": 10 ** (-np.random.uniform(7, 20)),
                    "effect_size": np.random.uniform(-0.3, 0.3),
                    "direction": np.random.choice(["hyper", "hypo"]),
                    "pmid": f"3{np.random.randint(1000000, 9999999)}",
                    "sample_size": np.random.randint(500, 10000),
                    "tissue": np.random.choice(["blood", "saliva", "brain"]),
                    "source": "EWAS_Catalog_Simulated",
                    "fetched_at": datetime.utcnow().isoformat()
                })
        
        return markers


class PubChemClient:
    """Client for PubChem REST API"""
    
    CONFIG = APIConfig(
        name="PubChem",
        base_url="https://pubchem.ncbi.nlm.nih.gov/rest/pug",
        rate_limit=5,
        timeout=30
    )
    
    def __init__(self):
        self.session = requests.Session() if REQUESTS_AVAILABLE else None
        self.last_request_time = 0
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        min_interval = 1.0 / self.CONFIG.rate_limit
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_request_time = time.time()
    
    def fetch_substance_info(self, name: str) -> Optional[Dict]:
        """Fetch substance information from PubChem"""
        if not REQUESTS_AVAILABLE:
            return self._get_simulated_substance(name)
        
        try:
            self._rate_limit()
            
            url = f"{self.CONFIG.base_url}/compound/name/{name}/JSON"
            response = self.session.get(url, timeout=self.CONFIG.timeout)
            
            if response.status_code == 200:
                data = response.json()
                compounds = data.get("PC_Compounds", [])
                
                if compounds:
                    compound = compounds[0]
                    return self._parse_compound(compound, name)
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching {name} from PubChem: {str(e)}")
            return None
    
    def fetch_substances_by_category(self, category: str) -> List[Dict]:
        """Fetch substances by pharmacological category"""
        substances = []
        
        category_substances = {
            "opioid": ["morphine", "fentanyl", "oxycodone", "hydrocodone", "heroin"],
            "stimulant": ["cocaine", "amphetamine", "methamphetamine", "MDMA"],
            "depressant": ["ethanol", "diazepam", "alprazolam", "phenobarbital"],
            "cannabinoid": ["THC", "CBD", "cannabinol"],
            "hallucinogen": ["LSD", "psilocybin", "mescaline", "DMT"]
        }
        
        names = category_substances.get(category.lower(), [])
        
        for name in names:
            info = self.fetch_substance_info(name)
            if info:
                info["category"] = category
                substances.append(info)
        
        return substances
    
    def _parse_compound(self, compound: Dict, name: str) -> Dict:
        """Parse PubChem compound data"""
        props = compound.get("props", [])
        
        result = {
            "name": name,
            "cid": compound.get("id", {}).get("id", {}).get("cid"),
            "source": "PubChem",
            "fetched_at": datetime.utcnow().isoformat()
        }
        
        for prop in props:
            urn = prop.get("urn", {})
            label = urn.get("label", "")
            value = prop.get("value", {})
            
            if label == "SMILES" and "sval" in value:
                result["smiles"] = value["sval"]
            elif label == "InChIKey" and "sval" in value:
                result["inchi_key"] = value["sval"]
            elif label == "Molecular Formula" and "sval" in value:
                result["molecular_formula"] = value["sval"]
            elif label == "Molecular Weight" and "fval" in value:
                result["molecular_weight"] = value["fval"]
        
        return result
    
    def _get_simulated_substance(self, name: str) -> Dict:
        """Return simulated substance data"""
        return {
            "name": name,
            "cid": np.random.randint(1000, 100000),
            "smiles": f"C{'C' * np.random.randint(3, 10)}O",
            "inchi_key": f"{''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 14))}-{''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 10))}-N",
            "molecular_formula": f"C{np.random.randint(5, 20)}H{np.random.randint(10, 30)}O{np.random.randint(1, 5)}",
            "molecular_weight": np.random.uniform(100, 500),
            "source": "PubChem_Simulated",
            "fetched_at": datetime.utcnow().isoformat()
        }


# =============================================================================
# SYNC MANAGER
# =============================================================================

@dataclass
class SyncResult:
    """Result of a sync operation"""
    source: str
    status: str
    records_fetched: int = 0
    records_added: int = 0
    records_updated: int = 0
    records_skipped: int = 0
    errors: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    @property
    def duration(self) -> float:
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0


class DatabaseSyncManager:
    """Manager for automatic database synchronization"""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.environ.get("DATABASE_URL")
        self.engine = None
        self.Session = None
        
        self.gwas_client = GWASCatalogClient()
        self.ewas_client = EWASCatalogClient()
        self.pubchem_client = PubChemClient()
        
        self._scheduler_thread = None
        self._running = False
        
        if SQLALCHEMY_AVAILABLE and self.database_url:
            self._init_database()
    
    def _init_database(self):
        """Initialize database connection and create tables"""
        try:
            self.engine = create_engine(self.database_url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
    
    def _calculate_hash(self, data: Dict) -> str:
        """Calculate hash of data for change detection"""
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def sync_gwas_catalog(self) -> SyncResult:
        """Synchronize with GWAS Catalog"""
        result = SyncResult(source="GWAS_Catalog", status="running")
        
        try:
            logger.info("Starting GWAS Catalog sync...")
            
            studies = self.gwas_client.fetch_addiction_studies()
            result.records_fetched = len(studies)
            
            if self.Session:
                session = self.Session()
                
                for study_data in studies:
                    try:
                        data_hash = self._calculate_hash(study_data)
                        
                        accession = study_data.get("study_accession", 
                                                   study_data.get("study_data", {}).get("shortForm", f"UNKNOWN_{result.records_added}"))
                        
                        existing = session.query(SyncedGWASStudy).filter_by(
                            study_accession=accession
                        ).first()
                        
                        if existing:
                            if existing.data_hash != data_hash:
                                existing.extra_data = study_data
                                existing.data_hash = data_hash
                                existing.updated_at = datetime.utcnow()
                                result.records_updated += 1
                            else:
                                result.records_skipped += 1
                        else:
                            new_study = SyncedGWASStudy(
                                study_accession=accession,
                                pmid=study_data.get("pmid"),
                                trait=study_data.get("trait"),
                                snp_id=study_data.get("snp_id"),
                                gene_name=study_data.get("gene_name"),
                                p_value=study_data.get("p_value"),
                                source="GWAS_Catalog",
                                extra_data=study_data,
                                data_hash=data_hash
                            )
                            session.add(new_study)
                            result.records_added += 1
                            
                    except Exception as e:
                        result.errors.append(f"Error processing study: {str(e)}")
                
                session.commit()
                
                log_entry = SyncLog(
                    source="GWAS_Catalog",
                    sync_type="full",
                    status="success",
                    records_fetched=result.records_fetched,
                    records_added=result.records_added,
                    records_updated=result.records_updated,
                    records_skipped=result.records_skipped,
                    started_at=result.started_at,
                    completed_at=datetime.utcnow(),
                    duration_seconds=result.duration
                )
                session.add(log_entry)
                session.commit()
                session.close()
            
            result.status = "success"
            result.completed_at = datetime.utcnow()
            
            logger.info(f"GWAS sync completed: {result.records_added} added, {result.records_updated} updated")
            
        except Exception as e:
            result.status = "error"
            result.errors.append(str(e))
            logger.error(f"GWAS sync failed: {str(e)}")
        
        return result
    
    def sync_ewas_catalog(self) -> SyncResult:
        """Synchronize with EWAS Catalog"""
        result = SyncResult(source="EWAS_Catalog", status="running")
        
        try:
            logger.info("Starting EWAS Catalog sync...")
            
            markers = self.ewas_client.fetch_addiction_markers()
            result.records_fetched = len(markers)
            
            if self.Session:
                session = self.Session()
                
                for marker_data in markers:
                    try:
                        data_hash = self._calculate_hash(marker_data)
                        cpg_id = marker_data.get("cpg_id")
                        exposure = marker_data.get("exposure")
                        
                        existing = session.query(SyncedEWASMarker).filter_by(
                            cpg_id=cpg_id,
                            exposure=exposure
                        ).first()
                        
                        if existing:
                            if existing.data_hash != data_hash:
                                existing.gene = marker_data.get("gene")
                                existing.p_value = marker_data.get("p_value")
                                existing.effect_size = marker_data.get("effect_size")
                                existing.extra_data = marker_data
                                existing.data_hash = data_hash
                                result.records_updated += 1
                            else:
                                result.records_skipped += 1
                        else:
                            new_marker = SyncedEWASMarker(
                                cpg_id=cpg_id,
                                gene=marker_data.get("gene"),
                                chromosome=marker_data.get("chromosome"),
                                position=marker_data.get("position"),
                                exposure=exposure,
                                trait=marker_data.get("trait"),
                                p_value=marker_data.get("p_value"),
                                effect_size=marker_data.get("effect_size"),
                                direction=marker_data.get("direction"),
                                pmid=marker_data.get("pmid"),
                                sample_size=marker_data.get("sample_size"),
                                tissue=marker_data.get("tissue"),
                                source="EWAS_Catalog",
                                extra_data=marker_data,
                                data_hash=data_hash
                            )
                            session.add(new_marker)
                            result.records_added += 1
                            
                    except Exception as e:
                        result.errors.append(f"Error processing marker: {str(e)}")
                
                session.commit()
                
                log_entry = SyncLog(
                    source="EWAS_Catalog",
                    sync_type="full",
                    status="success",
                    records_fetched=result.records_fetched,
                    records_added=result.records_added,
                    records_updated=result.records_updated,
                    records_skipped=result.records_skipped,
                    started_at=result.started_at,
                    completed_at=datetime.utcnow(),
                    duration_seconds=result.duration
                )
                session.add(log_entry)
                session.commit()
                session.close()
            
            result.status = "success"
            result.completed_at = datetime.utcnow()
            
            logger.info(f"EWAS sync completed: {result.records_added} added, {result.records_updated} updated")
            
        except Exception as e:
            result.status = "error"
            result.errors.append(str(e))
            logger.error(f"EWAS sync failed: {str(e)}")
        
        return result
    
    def sync_pubchem_substances(self, categories: List[str] = None) -> SyncResult:
        """Synchronize substance data from PubChem"""
        result = SyncResult(source="PubChem", status="running")
        
        if categories is None:
            categories = ["opioid", "stimulant", "depressant", "cannabinoid", "hallucinogen"]
        
        try:
            logger.info("Starting PubChem sync...")
            
            all_substances = []
            for category in categories:
                substances = self.pubchem_client.fetch_substances_by_category(category)
                all_substances.extend(substances)
            
            result.records_fetched = len(all_substances)
            
            if self.Session:
                session = self.Session()
                
                for substance_data in all_substances:
                    try:
                        data_hash = self._calculate_hash(substance_data)
                        external_id = f"PubChem_{substance_data.get('cid', substance_data.get('name'))}"
                        
                        existing = session.query(SyncedSubstance).filter_by(
                            external_id=external_id
                        ).first()
                        
                        if existing:
                            if existing.data_hash != data_hash:
                                existing.smiles = substance_data.get("smiles")
                                existing.inchi_key = substance_data.get("inchi_key")
                                existing.chemical_formula = substance_data.get("molecular_formula")
                                existing.extra_data = substance_data
                                existing.data_hash = data_hash
                                result.records_updated += 1
                            else:
                                result.records_skipped += 1
                        else:
                            new_substance = SyncedSubstance(
                                external_id=external_id,
                                name=substance_data.get("name"),
                                source="PubChem",
                                category=substance_data.get("category"),
                                smiles=substance_data.get("smiles"),
                                inchi_key=substance_data.get("inchi_key"),
                                chemical_formula=substance_data.get("molecular_formula"),
                                extra_data=substance_data,
                                data_hash=data_hash
                            )
                            session.add(new_substance)
                            result.records_added += 1
                            
                    except Exception as e:
                        result.errors.append(f"Error processing substance: {str(e)}")
                
                session.commit()
                
                log_entry = SyncLog(
                    source="PubChem",
                    sync_type="full",
                    status="success",
                    records_fetched=result.records_fetched,
                    records_added=result.records_added,
                    records_updated=result.records_updated,
                    records_skipped=result.records_skipped,
                    started_at=result.started_at,
                    completed_at=datetime.utcnow(),
                    duration_seconds=result.duration
                )
                session.add(log_entry)
                session.commit()
                session.close()
            
            result.status = "success"
            result.completed_at = datetime.utcnow()
            
            logger.info(f"PubChem sync completed: {result.records_added} added, {result.records_updated} updated")
            
        except Exception as e:
            result.status = "error"
            result.errors.append(str(e))
            logger.error(f"PubChem sync failed: {str(e)}")
        
        return result
    
    def sync_all(self) -> Dict[str, SyncResult]:
        """Run full synchronization across all sources"""
        results = {}
        
        logger.info("Starting full database synchronization...")
        
        results["GWAS_Catalog"] = self.sync_gwas_catalog()
        results["EWAS_Catalog"] = self.sync_ewas_catalog()
        results["PubChem"] = self.sync_pubchem_substances()
        
        logger.info("Full synchronization completed")
        
        return results
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status and statistics"""
        if not self.Session:
            return {"status": "database_not_connected"}
        
        session = self.Session()
        
        try:
            substances_count = session.query(SyncedSubstance).count()
            gwas_count = session.query(SyncedGWASStudy).count()
            ewas_count = session.query(SyncedEWASMarker).count()
            
            recent_logs = session.query(SyncLog).order_by(
                SyncLog.completed_at.desc()
            ).limit(10).all()
            
            return {
                "status": "connected",
                "counts": {
                    "substances": substances_count,
                    "gwas_studies": gwas_count,
                    "ewas_markers": ewas_count
                },
                "recent_syncs": [
                    {
                        "source": log.source,
                        "status": log.status,
                        "records_added": log.records_added,
                        "completed_at": log.completed_at.isoformat() if log.completed_at else None
                    }
                    for log in recent_logs
                ],
                "scheduler_running": self._running
            }
            
        finally:
            session.close()
    
    def start_scheduler(self, interval_hours: int = 24):
        """Start background scheduler for automatic sync"""
        if self._running:
            logger.warning("Scheduler already running")
            return
        
        self._running = True
        
        def scheduler_loop():
            while self._running:
                try:
                    logger.info("Scheduled sync starting...")
                    self.sync_all()
                    logger.info(f"Scheduled sync completed. Next sync in {interval_hours} hours")
                except Exception as e:
                    logger.error(f"Scheduled sync error: {str(e)}")
                
                for _ in range(interval_hours * 3600):
                    if not self._running:
                        break
                    time.sleep(1)
        
        self._scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self._scheduler_thread.start()
        
        logger.info(f"Scheduler started with {interval_hours}h interval")
    
    def stop_scheduler(self):
        """Stop the background scheduler"""
        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        logger.info("Scheduler stopped")
    
    def get_new_substances(self, since: datetime = None) -> List[Dict]:
        """Get newly added substances since a specific date"""
        if not self.Session:
            return []
        
        session = self.Session()
        
        try:
            if since is None:
                since = datetime.utcnow() - timedelta(days=7)
            
            substances = session.query(SyncedSubstance).filter(
                SyncedSubstance.created_at >= since
            ).all()
            
            return [
                {
                    "name": s.name,
                    "source": s.source,
                    "category": s.category,
                    "smiles": s.smiles,
                    "created_at": s.created_at.isoformat()
                }
                for s in substances
            ]
            
        finally:
            session.close()
    
    def get_new_markers(self, since: datetime = None) -> List[Dict]:
        """Get newly added EWAS markers since a specific date"""
        if not self.Session:
            return []
        
        session = self.Session()
        
        try:
            if since is None:
                since = datetime.utcnow() - timedelta(days=7)
            
            markers = session.query(SyncedEWASMarker).filter(
                SyncedEWASMarker.created_at >= since
            ).all()
            
            return [
                {
                    "cpg_id": m.cpg_id,
                    "gene": m.gene,
                    "exposure": m.exposure,
                    "p_value": m.p_value,
                    "created_at": m.created_at.isoformat()
                }
                for m in markers
            ]
            
        finally:
            session.close()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_sync_manager() -> DatabaseSyncManager:
    """Create and return a configured sync manager"""
    return DatabaseSyncManager()


def run_full_sync() -> Dict[str, SyncResult]:
    """Run a full synchronization"""
    manager = create_sync_manager()
    return manager.sync_all()


def get_database_statistics() -> Dict[str, Any]:
    """Get current database statistics"""
    manager = create_sync_manager()
    return manager.get_sync_status()


# =============================================================================
# STREAMLIT UI COMPONENT
# =============================================================================

def render_sync_dashboard():
    """Render Streamlit dashboard for database synchronization"""
    import streamlit as st
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0050A0, #003366); color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
        <h2>Database Auto-Sync Manager</h2>
        <p>Automatic synchronization with external genomic databases</p>
    </div>
    """, unsafe_allow_html=True)
    
    manager = create_sync_manager()
    status = manager.get_sync_status()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Substances", status.get("counts", {}).get("substances", 0))
    with col2:
        st.metric("GWAS Studies", status.get("counts", {}).get("gwas_studies", 0))
    with col3:
        st.metric("EWAS Markers", status.get("counts", {}).get("ewas_markers", 0))
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Manual Sync")
        
        sync_source = st.selectbox(
            "Select Source",
            ["All Sources", "GWAS Catalog", "EWAS Catalog", "PubChem"]
        )
        
        if st.button("Run Sync Now"):
            with st.spinner(f"Syncing {sync_source}..."):
                if sync_source == "All Sources":
                    results = manager.sync_all()
                    for source, result in results.items():
                        st.success(f"{source}: {result.records_added} added, {result.records_updated} updated")
                elif sync_source == "GWAS Catalog":
                    result = manager.sync_gwas_catalog()
                    st.success(f"GWAS: {result.records_added} added, {result.records_updated} updated")
                elif sync_source == "EWAS Catalog":
                    result = manager.sync_ewas_catalog()
                    st.success(f"EWAS: {result.records_added} added, {result.records_updated} updated")
                elif sync_source == "PubChem":
                    result = manager.sync_pubchem_substances()
                    st.success(f"PubChem: {result.records_added} added, {result.records_updated} updated")
    
    with col2:
        st.subheader("Scheduler")
        
        interval = st.selectbox(
            "Sync Interval",
            [6, 12, 24, 48, 168],
            index=2,
            format_func=lambda x: f"{x} hours" if x < 168 else "Weekly"
        )
        
        if status.get("scheduler_running"):
            st.success("Scheduler is running")
            if st.button("Stop Scheduler"):
                manager.stop_scheduler()
                st.rerun()
        else:
            if st.button("Start Scheduler"):
                manager.start_scheduler(interval)
                st.success(f"Scheduler started with {interval}h interval")
    
    st.markdown("---")
    st.subheader("Recent Sync History")
    
    recent_syncs = status.get("recent_syncs", [])
    if recent_syncs:
        df = pd.DataFrame(recent_syncs)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No sync history available")


if __name__ == "__main__":
    manager = create_sync_manager()
    
    print("Running test sync...")
    results = manager.sync_all()
    
    for source, result in results.items():
        print(f"\n{source}:")
        print(f"  Status: {result.status}")
        print(f"  Fetched: {result.records_fetched}")
        print(f"  Added: {result.records_added}")
        print(f"  Updated: {result.records_updated}")
        print(f"  Duration: {result.duration:.2f}s")
