# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
PostgreSQL Database Module for EpiClock Prototype
Patient data, analysis history, and longitudinal tracking persistence
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import pandas as pd
import numpy as np

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True
    )
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
else:
    engine = None
    SessionLocal = None

Base = declarative_base()


class Patient(Base):
    # nrcdnl94
    """Patient model for storing patient information"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), unique=True, index=True, nullable=False)
    external_id = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    sex = Column(String(10), nullable=False)
    substance_type = Column(String(50), nullable=True)
    smoking_pack_years = Column(Float, default=0)
    bmi = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    analyses = relationship("Analysis", back_populates="patient", cascade="all, delete-orphan")
    clinical_data = relationship("ClinicalData", back_populates="patient", cascade="all, delete-orphan")


class Analysis(Base):
    # nrcdnl94
    """Analysis model for storing epigenetic age analysis results"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    analysis_date = Column(DateTime, default=datetime.utcnow, index=True)
    sample_id = Column(String(100), nullable=True)
    tissue_type = Column(String(50), default="blood")
    chronological_age = Column(Float, nullable=False)
    
    horvath_age = Column(Float, nullable=True)
    horvath_eaa = Column(Float, nullable=True)
    hannum_age = Column(Float, nullable=True)
    hannum_eaa = Column(Float, nullable=True)
    phenoage_age = Column(Float, nullable=True)
    phenoage_eaa = Column(Float, nullable=True)
    grimage_age = Column(Float, nullable=True)
    grimage_eaa = Column(Float, nullable=True)
    dunedinpace = Column(Float, nullable=True)
    dunedinpace_deviation = Column(Float, nullable=True)
    
    ensemble_age = Column(Float, nullable=True)
    ensemble_eaa = Column(Float, nullable=True)
    
    reference_percentile = Column(Float, nullable=True)
    reference_z_score = Column(Float, nullable=True)
    
    risk_category = Column(String(50), nullable=True)
    risk_score = Column(Float, nullable=True)
    
    clock_results_json = Column(JSON, nullable=True)
    biomarkers_json = Column(JSON, nullable=True)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="analyses")


class ClinicalData(Base):
    # nrcdnl94
    """Clinical biomarker data for patients"""
    __tablename__ = "clinical_data"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    measurement_date = Column(DateTime, default=datetime.utcnow)
    
    albumin = Column(Float, nullable=True)
    creatinine = Column(Float, nullable=True)
    glucose = Column(Float, nullable=True)
    crp = Column(Float, nullable=True)
    lymphocyte_percent = Column(Float, nullable=True)
    mcv = Column(Float, nullable=True)
    rdw = Column(Float, nullable=True)
    white_blood_cell = Column(Float, nullable=True)
    alkaline_phosphatase = Column(Float, nullable=True)
    
    homa_ir = Column(Float, nullable=True)
    cortisol = Column(Float, nullable=True)
    acth = Column(Float, nullable=True)
    il6 = Column(Float, nullable=True)
    tnf_alpha = Column(Float, nullable=True)
    telomere_length = Column(Float, nullable=True)
    
    ders_score = Column(Float, nullable=True)
    self_control_score = Column(Float, nullable=True)
    social_support_score = Column(Float, nullable=True)
    resilience_score = Column(Float, nullable=True)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="clinical_data")


class GSEAResult(Base):
    # nrcdnl94
    """Gene Set Enrichment Analysis results"""
    __tablename__ = "gsea_results"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_name = Column(String(200), nullable=False)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    substance_type = Column(String(50), nullable=True)
    
    pathway_id = Column(String(100), nullable=False)
    pathway_name = Column(String(500), nullable=False)
    pathway_source = Column(String(50), nullable=False)
    
    enrichment_score = Column(Float, nullable=True)
    normalized_es = Column(Float, nullable=True)
    p_value = Column(Float, nullable=True)
    fdr_q_value = Column(Float, nullable=True)
    
    leading_edge_genes = Column(JSON, nullable=True)
    gene_count = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class TreatmentRecommendation(Base):
    # nrcdnl94
    """Clinical decision support recommendations"""
    __tablename__ = "treatment_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    
    recommendation_type = Column(String(100), nullable=False)
    priority = Column(String(20), nullable=False)
    recommendation_text = Column(Text, nullable=False)
    evidence_level = Column(String(20), nullable=True)
    
    target_pathway = Column(String(200), nullable=True)
    expected_eaa_reduction = Column(Float, nullable=True)
    
    is_accepted = Column(Boolean, default=False)
    accepted_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    if engine:
        try:
            Base.metadata.create_all(bind=engine)
            return True
        except Exception:
            return False
    return False


@contextmanager
def get_db_session():
    """Context manager for database sessions with proper cleanup"""
    if not SessionLocal:
        yield None
        return
    
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()
        SessionLocal.remove()


def get_db():
    """Get database session (legacy - prefer get_db_session context manager)"""
    if SessionLocal:
        db = None
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            return db
        except Exception:
            if db:
                db.close()
                SessionLocal.remove()
            return None
    return None


class DatabaseManager:
    # nrcdnl94
    """Manager class for database operations"""
    
    def __init__(self):
        self.initialized = init_db()
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        if not self.initialized or engine is None:
            return False
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
    
    def _get_fresh_session(self):
        """Get a fresh database session"""
        if not SessionLocal:
            return None
        try:
            session = SessionLocal()
            session.execute(text("SELECT 1"))
            return session
        except Exception:
            return None
    
    def create_patient(self, patient_data: Dict) -> Optional[Patient]:
        """Create a new patient record"""
        db = get_db()
        if not db:
            return None
        
        try:
            patient = Patient(**patient_data)
            db.add(patient)
            db.commit()
            db.refresh(patient)
            return patient
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Get patient by patient_id"""
        db = get_db()
        if not db:
            return None
        
        try:
            return db.query(Patient).filter(Patient.patient_id == patient_id).first()
        finally:
            db.close()
    
    def get_patient_by_id(self, id: int) -> Optional[Patient]:
        """Get patient by database ID"""
        db = get_db()
        if not db:
            return None
        
        try:
            return db.query(Patient).filter(Patient.id == id).first()
        finally:
            db.close()
    
    def get_all_patients(self) -> List[Patient]:
        """Get all patients"""
        db = get_db()
        if not db:
            return []
        
        try:
            return db.query(Patient).order_by(Patient.created_at.desc()).all()
        finally:
            db.close()
    
    def update_patient(self, patient_id: str, update_data: Dict) -> Optional[Patient]:
        """Update patient record"""
        db = get_db()
        if not db:
            return None
        
        try:
            patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
            if patient:
                for key, value in update_data.items():
                    if hasattr(patient, key):
                        setattr(patient, key, value)
                db.commit()
                db.refresh(patient)
            return patient
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def delete_patient(self, patient_id: str) -> bool:
        """Delete patient record"""
        db = get_db()
        if not db:
            return False
        
        try:
            patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
            if patient:
                db.delete(patient)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def save_analysis(self, patient_id: str, analysis_data: Dict) -> Optional[Analysis]:
        """Save analysis results"""
        db = get_db()
        if not db:
            return None
        
        try:
            patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
            if not patient:
                return None
            
            analysis_data['patient_id'] = patient.id
            analysis = Analysis(**analysis_data)
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            return analysis
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_patient_analyses(self, patient_id: str) -> List[Analysis]:
        """Get all analyses for a patient"""
        db = get_db()
        if not db:
            return []
        
        try:
            patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
            if not patient:
                return []
            return db.query(Analysis).filter(Analysis.patient_id == patient.id).order_by(Analysis.analysis_date.desc()).all()
        finally:
            db.close()
    
    def get_longitudinal_data(self, patient_id: str) -> pd.DataFrame:
        """Get longitudinal analysis data for a patient"""
        analyses = self.get_patient_analyses(patient_id)
        
        if not analyses:
            return pd.DataFrame()
        
        data = []
        for analysis in analyses:
            data.append({
                'analysis_date': analysis.analysis_date,
                'chronological_age': analysis.chronological_age,
                'horvath_age': analysis.horvath_age,
                'horvath_eaa': analysis.horvath_eaa,
                'hannum_age': analysis.hannum_age,
                'hannum_eaa': analysis.hannum_eaa,
                'phenoage_age': analysis.phenoage_age,
                'phenoage_eaa': analysis.phenoage_eaa,
                'grimage_age': analysis.grimage_age,
                'grimage_eaa': analysis.grimage_eaa,
                'dunedinpace': analysis.dunedinpace,
                'ensemble_age': analysis.ensemble_age,
                'ensemble_eaa': analysis.ensemble_eaa,
                'risk_category': analysis.risk_category,
                'risk_score': analysis.risk_score
            })
        
        return pd.DataFrame(data)
    
    def save_clinical_data(self, patient_id: str, clinical_data: Dict) -> Optional[ClinicalData]:
        """Save clinical biomarker data"""
        db = get_db()
        if not db:
            return None
        
        try:
            patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
            if not patient:
                return None
            
            clinical_data['patient_id'] = patient.id
            clinical = ClinicalData(**clinical_data)
            db.add(clinical)
            db.commit()
            db.refresh(clinical)
            return clinical
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def save_gsea_result(self, gsea_data: Dict) -> Optional[GSEAResult]:
        """Save GSEA result"""
        db = get_db()
        if not db:
            return None
        
        try:
            gsea = GSEAResult(**gsea_data)
            db.add(gsea)
            db.commit()
            db.refresh(gsea)
            return gsea
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_gsea_results(self, substance_type: Optional[str] = None) -> List[GSEAResult]:
        """Get GSEA results, optionally filtered by substance type"""
        db = get_db()
        if not db:
            return []
        
        try:
            query = db.query(GSEAResult)
            if substance_type:
                query = query.filter(GSEAResult.substance_type == substance_type)
            return query.order_by(GSEAResult.p_value).all()
        finally:
            db.close()
    
    def save_treatment_recommendation(self, analysis_id: int, recommendation_data: Dict) -> Optional[TreatmentRecommendation]:
        """Save treatment recommendation"""
        db = get_db()
        if not db:
            return None
        
        try:
            recommendation_data['analysis_id'] = analysis_id
            recommendation = TreatmentRecommendation(**recommendation_data)
            db.add(recommendation)
            db.commit()
            db.refresh(recommendation)
            return recommendation
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_analysis_recommendations(self, analysis_id: int) -> List[TreatmentRecommendation]:
        """Get recommendations for an analysis"""
        db = get_db()
        if not db:
            return []
        
        try:
            return db.query(TreatmentRecommendation).filter(
                TreatmentRecommendation.analysis_id == analysis_id
            ).order_by(TreatmentRecommendation.priority).all()
        finally:
            db.close()
    
    def get_database_stats(self) -> Dict:
        """Get database statistics with robust error handling"""
        if not self.is_connected():
            return {'connected': False, 'error': 'Database not connected'}
        
        try:
            from sqlalchemy import func, text
            
            with get_db_session() as db:
                if db is None:
                    return {'connected': False, 'error': 'Could not create session'}
                
                try:
                    patient_count = db.query(Patient).count()
                    analysis_count = db.query(Analysis).count()
                    clinical_count = db.query(ClinicalData).count()
                    gsea_count = db.query(GSEAResult).count()
                    
                    substance_counts = {}
                    substance_query = db.query(
                        Patient.substance_type, 
                        func.count(Patient.id)
                    ).group_by(Patient.substance_type).all()
                    
                    for substance, count in substance_query:
                        if substance:
                            substance_counts[substance] = count
                    
                    return {
                        'connected': True,
                        'patient_count': patient_count,
                        'analysis_count': analysis_count,
                        'clinical_data_count': clinical_count,
                        'gsea_result_count': gsea_count,
                        'substance_counts': substance_counts
                    }
                except OperationalError as e:
                    return {
                        'connected': False, 
                        'error': 'Database connection lost',
                        'patient_count': 0,
                        'analysis_count': 0,
                        'clinical_data_count': 0,
                        'gsea_result_count': 0
                    }
        except Exception as e:
            return {
                'connected': False, 
                'error': str(e),
                'patient_count': 0,
                'analysis_count': 0,
                'clinical_data_count': 0,
                'gsea_result_count': 0
            }


# End of module - # nrcdnl94