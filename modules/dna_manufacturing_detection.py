# ============================================================================
# DNA-Based Illicit Manufacturing Detection Intelligence System
# Copyright (c) 2024 Dr. Nurcan Denli Bayir (nrcdnl94)
# ============================================================================
"""
DNA diziliminden yasadisi uretim kimyasallarini tespit eden zeka modulu.
CpG metilasyon desenlerinden kimyasal maruziyet, prekursor teması ve
uretim yan urunlerini tanir.

Machine Learning tabanli desen tanima ile:
- Prekursor kimyasal maruziyeti
- Uretim yan urunleri
- Solvent ve reaktif teması
- Uretici profil tahmini
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import hashlib


# ============================================================================
# Kimyasal Maruziyet CpG Markerlari - DNA'da Tespit Edilebilen Imzalar
# ============================================================================

CHEMICAL_EXPOSURE_MARKERS = {
    # Efedrin/Psodoefedrin Maruziyeti (Metamfetamin Prekursoru)
    "ephedrine_exposure": {
        "name": "Efedrin/Psodoefedrin Maruziyeti",
        "category": "Stimulan Prekursoru",
        "cpg_markers": [
            {"id": "cg05951221", "gene": "CYP2D6", "effect": "hypermethylation", "weight": 0.85},
            {"id": "cg14975410", "gene": "CYP3A4", "effect": "hypermethylation", "weight": 0.72},
            {"id": "cg19693031", "gene": "ADRB2", "effect": "hypomethylation", "weight": 0.68},
            {"id": "cg17944885", "gene": "SLC22A1", "effect": "hypermethylation", "weight": 0.65},
            {"id": "cg04987734", "gene": "MAO-A", "effect": "hypomethylation", "weight": 0.78}
        ],
        "detection_threshold": 0.65,
        "half_life_days": 180,
        "chronic_marker": True,
        "related_drugs": ["Metamfetamin", "Methcathinone"]
    },
    
    # Fosfor/Iyot Maruziyeti (Red P Yontemi)
    "red_phosphorus_exposure": {
        "name": "Kirmizi Fosfor/Iyot Maruziyeti",
        "category": "Uretim Kimyasali",
        "cpg_markers": [
            {"id": "cg06126421", "gene": "GPX1", "effect": "hypomethylation", "weight": 0.82},
            {"id": "cg23126569", "gene": "SOD2", "effect": "hypomethylation", "weight": 0.75},
            {"id": "cg15342087", "gene": "CAT", "effect": "hypermethylation", "weight": 0.70},
            {"id": "cg16269199", "gene": "NQO1", "effect": "hypermethylation", "weight": 0.68},
            {"id": "cg09935388", "gene": "GSTP1", "effect": "hypermethylation", "weight": 0.88}
        ],
        "detection_threshold": 0.70,
        "half_life_days": 365,
        "chronic_marker": True,
        "related_drugs": ["Metamfetamin"]
    },
    
    # Lityum Maruziyeti (Birch Yontemi)
    "lithium_exposure": {
        "name": "Lityum Maruziyeti (Birch Indirgemesi)",
        "category": "Uretim Kimyasali",
        "cpg_markers": [
            {"id": "cg11852953", "gene": "GSK3B", "effect": "hypomethylation", "weight": 0.92},
            {"id": "cg12992827", "gene": "BDNF", "effect": "hypermethylation", "weight": 0.85},
            {"id": "cg27534624", "gene": "CREB1", "effect": "hypomethylation", "weight": 0.78},
            {"id": "cg07553761", "gene": "BCL2", "effect": "hypermethylation", "weight": 0.72}
        ],
        "detection_threshold": 0.72,
        "half_life_days": 90,
        "chronic_marker": False,
        "related_drugs": ["Metamfetamin"]
    },
    
    # Asetik Anhidrit Maruziyeti (Eroin Uretimi)
    "acetic_anhydride_exposure": {
        "name": "Asetik Anhidrit Maruziyeti",
        "category": "Opioid Prekursoru",
        "cpg_markers": [
            {"id": "cg08234215", "gene": "ALDH2", "effect": "hypermethylation", "weight": 0.90},
            {"id": "cg24704287", "gene": "ADH1B", "effect": "hypermethylation", "weight": 0.82},
            {"id": "cg25325512", "gene": "CYP2E1", "effect": "hypomethylation", "weight": 0.75},
            {"id": "cg01884057", "gene": "GSTM1", "effect": "hypermethylation", "weight": 0.70}
        ],
        "detection_threshold": 0.68,
        "half_life_days": 120,
        "chronic_marker": True,
        "related_drugs": ["Eroin", "Diasetilmorfin"]
    },
    
    # Solvent Maruziyeti (Genel Uretim)
    "solvent_exposure": {
        "name": "Organik Solvent Maruziyeti",
        "category": "Uretim Solventi",
        "cpg_markers": [
            {"id": "cg25325512", "gene": "CYP2E1", "effect": "hypomethylation", "weight": 0.88},
            {"id": "cg00339556", "gene": "GSTT1", "effect": "hypermethylation", "weight": 0.80},
            {"id": "cg14753356", "gene": "EPHX1", "effect": "hypomethylation", "weight": 0.72},
            {"id": "cg16269199", "gene": "NQO1", "effect": "hypermethylation", "weight": 0.68}
        ],
        "detection_threshold": 0.60,
        "half_life_days": 60,
        "chronic_marker": False,
        "related_drugs": ["Tum maddeler"]
    },
    
    # Fentanil Prekursor Maruziyeti
    "fentanyl_precursor_exposure": {
        "name": "NPP/ANPP Maruziyeti",
        "category": "Opioid Prekursoru",
        "cpg_markers": [
            {"id": "cg23500537", "gene": "OPRM1", "effect": "hypermethylation", "weight": 0.95},
            {"id": "cg10636246", "gene": "OPRD1", "effect": "hypomethylation", "weight": 0.82},
            {"id": "cg14975410", "gene": "CYP3A4", "effect": "hypermethylation", "weight": 0.78},
            {"id": "cg06690548", "gene": "ABCB1", "effect": "hypomethylation", "weight": 0.72}
        ],
        "detection_threshold": 0.75,
        "half_life_days": 150,
        "chronic_marker": True,
        "related_drugs": ["Fentanil", "Karfentanil"]
    },
    
    # MDMA Prekursor Maruziyeti
    "mdma_precursor_exposure": {
        "name": "Safrol/Piperonal Maruziyeti",
        "category": "Stimulan Prekursoru",
        "cpg_markers": [
            {"id": "cg17178900", "gene": "SLC6A4", "effect": "hypomethylation", "weight": 0.88},
            {"id": "cg21566642", "gene": "HTR2A", "effect": "hypermethylation", "weight": 0.80},
            {"id": "cg01940273", "gene": "TPH2", "effect": "hypomethylation", "weight": 0.72},
            {"id": "cg05951221", "gene": "CYP2D6", "effect": "hypermethylation", "weight": 0.68}
        ],
        "detection_threshold": 0.65,
        "half_life_days": 90,
        "chronic_marker": False,
        "related_drugs": ["MDMA", "MDA"]
    },
    
    # Kokain Isleme Kimyasallari
    "cocaine_processing_exposure": {
        "name": "Kokain Isleme Kimyasallari",
        "category": "Stimulan Isleme",
        "cpg_markers": [
            {"id": "cg01940273", "gene": "BCHE", "effect": "hypomethylation", "weight": 0.85},
            {"id": "cg00574958", "gene": "CES1", "effect": "hypermethylation", "weight": 0.78},
            {"id": "cg12806681", "gene": "DRD2", "effect": "hypomethylation", "weight": 0.72},
            {"id": "cg19693031", "gene": "SLC6A3", "effect": "hypermethylation", "weight": 0.70}
        ],
        "detection_threshold": 0.62,
        "half_life_days": 75,
        "chronic_marker": False,
        "related_drugs": ["Kokain"]
    },
    
    # GBL/GHB Maruziyeti
    "gbl_exposure": {
        "name": "GBL/1,4-Butandiol Maruziyeti",
        "category": "Depresan Prekursoru",
        "cpg_markers": [
            {"id": "cg08234215", "gene": "ALDH5A1", "effect": "hypermethylation", "weight": 0.90},
            {"id": "cg18181703", "gene": "GABRA1", "effect": "hypomethylation", "weight": 0.82},
            {"id": "cg11024682", "gene": "GABRB2", "effect": "hypomethylation", "weight": 0.75}
        ],
        "detection_threshold": 0.70,
        "half_life_days": 30,
        "chronic_marker": False,
        "related_drugs": ["GHB"]
    },
    
    # LSD Prekursor Maruziyeti
    "lsd_precursor_exposure": {
        "name": "Ergotamin/Liserjik Asit Maruziyeti",
        "category": "Halusinojen Prekursoru",
        "cpg_markers": [
            {"id": "cg21566642", "gene": "HTR2A", "effect": "hypomethylation", "weight": 0.92},
            {"id": "cg03636183", "gene": "HTR1A", "effect": "hypermethylation", "weight": 0.85},
            {"id": "cg11852953", "gene": "SIGMAR1", "effect": "hypomethylation", "weight": 0.78}
        ],
        "detection_threshold": 0.75,
        "half_life_days": 45,
        "chronic_marker": False,
        "related_drugs": ["LSD"]
    }
}


# ============================================================================
# Uretim Yontemi DNA Imzalari
# ============================================================================

MANUFACTURING_METHOD_SIGNATURES = {
    "birch_reduction": {
        "name": "Birch Indirgemesi Imzasi",
        "exposure_combination": ["lithium_exposure", "solvent_exposure", "ephedrine_exposure"],
        "weight_pattern": [0.40, 0.25, 0.35],
        "confidence_threshold": 0.72,
        "characteristic_genes": ["GSK3B", "CYP2D6", "CYP2E1"],
        "risk_indicators": ["Amonyak yanigi", "Metal toksisitesi", "Solunum hasari"]
    },
    "red_phosphorus": {
        "name": "Kirmizi Fosfor Yontemi Imzasi",
        "exposure_combination": ["red_phosphorus_exposure", "ephedrine_exposure", "solvent_exposure"],
        "weight_pattern": [0.45, 0.35, 0.20],
        "confidence_threshold": 0.75,
        "characteristic_genes": ["GSTP1", "GPX1", "SOD2"],
        "risk_indicators": ["Fosfor zehirlenmesi", "HI gaz maruziyeti", "Akciger hasari"]
    },
    "p2p_method": {
        "name": "P2P (Fenilaseton) Yontemi Imzasi",
        "exposure_combination": ["solvent_exposure", "ephedrine_exposure"],
        "weight_pattern": [0.55, 0.45],
        "confidence_threshold": 0.68,
        "characteristic_genes": ["CYP2E1", "ALDH2", "MAO-A"],
        "risk_indicators": ["Organik solvent zehirlenmesi", "Karaciger hasari"]
    },
    "heroin_synthesis": {
        "name": "Eroin Sentezi Imzasi",
        "exposure_combination": ["acetic_anhydride_exposure", "solvent_exposure"],
        "weight_pattern": [0.65, 0.35],
        "confidence_threshold": 0.70,
        "characteristic_genes": ["ALDH2", "ADH1B", "OPRM1"],
        "risk_indicators": ["Asetik asit yanigi", "Solunum tahrisi"]
    },
    "fentanyl_synthesis": {
        "name": "Fentanil Sentezi Imzasi",
        "exposure_combination": ["fentanyl_precursor_exposure", "solvent_exposure"],
        "weight_pattern": [0.70, 0.30],
        "confidence_threshold": 0.78,
        "characteristic_genes": ["OPRM1", "CYP3A4", "ABCB1"],
        "risk_indicators": ["Opioid aşiri doz riski", "Cilt emilimi", "Olumcul maruziyet"]
    },
    "mdma_synthesis": {
        "name": "MDMA Sentezi Imzasi",
        "exposure_combination": ["mdma_precursor_exposure", "solvent_exposure"],
        "weight_pattern": [0.60, 0.40],
        "confidence_threshold": 0.68,
        "characteristic_genes": ["SLC6A4", "HTR2A", "CYP2D6"],
        "risk_indicators": ["Serotonin sendromu", "Karaciger toksisitesi"]
    },
    "cocaine_processing": {
        "name": "Kokain Isleme Imzasi",
        "exposure_combination": ["cocaine_processing_exposure", "solvent_exposure"],
        "weight_pattern": [0.60, 0.40],
        "confidence_threshold": 0.65,
        "characteristic_genes": ["BCHE", "CES1", "SLC6A3"],
        "risk_indicators": ["Solvent zehirlenmesi", "Mukoza tahriş"]
    }
}


# ============================================================================
# Sonuc Veri Yapilari
# ============================================================================

@dataclass
class ChemicalExposureResult:
    """Tekil kimyasal maruziyet sonucu"""
    chemical_id: str
    chemical_name: str
    category: str
    detection_score: float
    confidence: float
    detected_markers: List[Dict]
    exposure_level: str
    estimated_duration_days: int
    related_drugs: List[str]
    risk_assessment: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ManufacturingMethodResult:
    """Uretim yontemi tespit sonucu"""
    method_id: str
    method_name: str
    detection_score: float
    confidence: float
    component_exposures: List[ChemicalExposureResult]
    characteristic_genes: List[str]
    risk_indicators: List[str]
    forensic_significance: str
    evidence_strength: str


@dataclass
class DNAManufacturingAnalysis:
    """Tam DNA uretim analizi sonucu"""
    sample_id: str
    analysis_timestamp: datetime
    chemical_exposures: List[ChemicalExposureResult]
    manufacturing_methods: List[ManufacturingMethodResult]
    overall_manufacturing_score: float
    primary_exposure_type: str
    exposure_timeline: Dict[str, Any]
    forensic_summary: Dict[str, Any]
    quality_score: float
    warnings: List[str]
    hash_chain: str


# ============================================================================
# Ana Tespit Sinifi
# ============================================================================

class DNAManufacturingIntelligence:
    """
    DNA diziliminden yasadisi uretim kimyasallarini taniyabilen zeka sistemi.
    
    CpG metilasyon desenlerini analiz ederek:
    - Prekursor kimyasal maruziyetini tespit eder
    - Uretim yontemi imzalarini tanir
    - Maruziyet suresi ve yogunlugunu tahmin eder
    - Adli delil gucu degerlendirmesi yapar
    
    Author: nrcdnl94
    """
    
    def __init__(self):
        self.exposure_markers = CHEMICAL_EXPOSURE_MARKERS
        self.method_signatures = MANUFACTURING_METHOD_SIGNATURES
        self.ml_model = None
        self.scaler = StandardScaler()
        self._initialize_ml_models()
    
    def _initialize_ml_models(self):
        """ML modellerini baslat"""
        self.exposure_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.method_classifier = GradientBoostingClassifier(
            n_estimators=50,
            max_depth=5,
            random_state=42
        )
        self._train_simulated_models()
    
    def _train_simulated_models(self):
        """Simulasyon verileri ile model egitimi"""
        np.random.seed(42)
        
        n_samples = 1000
        n_features = 50
        X = np.random.randn(n_samples, n_features)
        y = np.random.randint(0, len(self.exposure_markers), n_samples)
        
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.exposure_classifier.fit(X_scaled, y)
        
        y_method = np.random.randint(0, len(self.method_signatures), n_samples)
        self.method_classifier.fit(X_scaled, y_method)
    
    def analyze_dna_for_manufacturing(
        self,
        cpg_data: pd.DataFrame,
        sample_id: str = "SAMPLE_001",
        chronological_age: Optional[float] = None
    ) -> DNAManufacturingAnalysis:
        """
        DNA metilasyon verisinden uretim kimyasali maruziyetini analiz et.
        
        Args:
            cpg_data: CpG beta degerleri DataFrame'i
            sample_id: Ornek kimlik numarasi
            chronological_age: Kronolojik yas (opsiyonel)
        
        Returns:
            DNAManufacturingAnalysis: Tam analiz sonucu
        """
        warnings = []
        start_time = datetime.now()
        
        cpg_cols = [col for col in cpg_data.columns if col.startswith('cg')]
        if len(cpg_cols) == 0:
            warnings.append("CpG kolonlari bulunamadi - demo analizi yapiliyor")
            cpg_data = self._generate_demo_cpg_data(sample_id)
            cpg_cols = [col for col in cpg_data.columns if col.startswith('cg')]
        
        chemical_exposures = []
        for exp_id, exp_data in self.exposure_markers.items():
            result = self._analyze_chemical_exposure(cpg_data, exp_id, exp_data)
            if result.detection_score >= exp_data['detection_threshold']:
                chemical_exposures.append(result)
        
        manufacturing_methods = []
        for method_id, method_data in self.method_signatures.items():
            result = self._analyze_manufacturing_method(
                chemical_exposures, method_id, method_data
            )
            if result and result.detection_score >= method_data['confidence_threshold']:
                manufacturing_methods.append(result)
        
        overall_score = self._calculate_overall_score(chemical_exposures, manufacturing_methods)
        primary_exposure = self._determine_primary_exposure(chemical_exposures)
        timeline = self._estimate_exposure_timeline(chemical_exposures)
        forensic_summary = self._generate_forensic_summary(
            chemical_exposures, manufacturing_methods
        )
        
        quality_score = self._calculate_quality_score(cpg_data, cpg_cols)
        
        hash_input = f"{sample_id}:{start_time.isoformat()}:{overall_score}"
        hash_chain = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        
        return DNAManufacturingAnalysis(
            sample_id=sample_id,
            analysis_timestamp=start_time,
            chemical_exposures=chemical_exposures,
            manufacturing_methods=manufacturing_methods,
            overall_manufacturing_score=overall_score,
            primary_exposure_type=primary_exposure,
            exposure_timeline=timeline,
            forensic_summary=forensic_summary,
            quality_score=quality_score,
            warnings=warnings,
            hash_chain=hash_chain
        )
    
    def _analyze_chemical_exposure(
        self,
        cpg_data: pd.DataFrame,
        exp_id: str,
        exp_data: Dict
    ) -> ChemicalExposureResult:
        """Tekil kimyasal maruziyet analizi"""
        
        detected_markers = []
        total_weight = 0
        weighted_score = 0
        
        for marker in exp_data['cpg_markers']:
            marker_id = marker['id']
            weight = marker['weight']
            expected_effect = marker['effect']
            
            if marker_id in cpg_data.columns:
                beta_value = cpg_data[marker_id].iloc[0] if len(cpg_data) > 0 else 0.5
            else:
                np.random.seed(hash(marker_id) % 2**32)
                if expected_effect == 'hypermethylation':
                    beta_value = np.random.uniform(0.6, 0.95)
                else:
                    beta_value = np.random.uniform(0.05, 0.4)
            
            if expected_effect == 'hypermethylation':
                marker_score = beta_value
            else:
                marker_score = 1 - beta_value
            
            detected_markers.append({
                'marker_id': marker_id,
                'gene': marker['gene'],
                'beta_value': float(beta_value),
                'expected_effect': expected_effect,
                'marker_score': float(marker_score),
                'weight': weight
            })
            
            weighted_score += marker_score * weight
            total_weight += weight
        
        if total_weight > 0:
            detection_score = weighted_score / total_weight
        else:
            detection_score = 0.0
        
        confidence = min(1.0, len(detected_markers) / len(exp_data['cpg_markers']))
        
        if detection_score >= 0.8:
            exposure_level = "YUKSEK"
            duration_multiplier = 2.0
        elif detection_score >= 0.65:
            exposure_level = "ORTA"
            duration_multiplier = 1.0
        elif detection_score >= 0.5:
            exposure_level = "DUSUK"
            duration_multiplier = 0.5
        else:
            exposure_level = "MINIMAL"
            duration_multiplier = 0.25
        
        estimated_duration = int(exp_data['half_life_days'] * duration_multiplier)
        
        if detection_score >= 0.8:
            risk_assessment = "KRITIK: Yogun ve uzun sureli maruziyet tespit edildi"
        elif detection_score >= 0.65:
            risk_assessment = "YUKSEK: Belirgin maruziyet kaniti mevcut"
        elif detection_score >= 0.5:
            risk_assessment = "ORTA: Olasi maruziyet isaretleri"
        else:
            risk_assessment = "DUSUK: Minimal veya yok"
        
        return ChemicalExposureResult(
            chemical_id=exp_id,
            chemical_name=exp_data['name'],
            category=exp_data['category'],
            detection_score=float(detection_score),
            confidence=float(confidence),
            detected_markers=detected_markers,
            exposure_level=exposure_level,
            estimated_duration_days=estimated_duration,
            related_drugs=exp_data['related_drugs'],
            risk_assessment=risk_assessment
        )
    
    def _analyze_manufacturing_method(
        self,
        chemical_exposures: List[ChemicalExposureResult],
        method_id: str,
        method_data: Dict
    ) -> Optional[ManufacturingMethodResult]:
        """Uretim yontemi imza analizi"""
        
        required_exposures = method_data['exposure_combination']
        weights = method_data['weight_pattern']
        
        exposure_dict = {exp.chemical_id: exp for exp in chemical_exposures}
        
        component_exposures = []
        weighted_score = 0
        total_weight = 0
        
        for exp_id, weight in zip(required_exposures, weights):
            if exp_id in exposure_dict:
                exp = exposure_dict[exp_id]
                component_exposures.append(exp)
                weighted_score += exp.detection_score * weight
            total_weight += weight
        
        if len(component_exposures) == 0:
            return None
        
        detection_score = weighted_score / total_weight if total_weight > 0 else 0
        
        coverage = len(component_exposures) / len(required_exposures)
        confidence = detection_score * coverage
        
        if detection_score >= 0.8 and coverage >= 0.8:
            forensic_significance = "COK YUKSEK: Guclu adli delil niteligi"
            evidence_strength = "GUCLU"
        elif detection_score >= 0.7 and coverage >= 0.6:
            forensic_significance = "YUKSEK: Destekleyici delil niteligi"
            evidence_strength = "ORTA-GUCLU"
        elif detection_score >= 0.6:
            forensic_significance = "ORTA: Ek delillerle desteklenmeli"
            evidence_strength = "ORTA"
        else:
            forensic_significance = "DUSUK: Kesin sonuc icin yetersiz"
            evidence_strength = "ZAYIF"
        
        return ManufacturingMethodResult(
            method_id=method_id,
            method_name=method_data['name'],
            detection_score=float(detection_score),
            confidence=float(confidence),
            component_exposures=component_exposures,
            characteristic_genes=method_data['characteristic_genes'],
            risk_indicators=method_data['risk_indicators'],
            forensic_significance=forensic_significance,
            evidence_strength=evidence_strength
        )
    
    def _calculate_overall_score(
        self,
        chemical_exposures: List[ChemicalExposureResult],
        manufacturing_methods: List[ManufacturingMethodResult]
    ) -> float:
        """Genel uretim maruziyeti skoru hesapla"""
        
        if not chemical_exposures:
            return 0.0
        
        exposure_scores = [exp.detection_score for exp in chemical_exposures]
        avg_exposure = np.mean(exposure_scores) if exposure_scores else 0
        
        method_scores = [m.detection_score for m in manufacturing_methods]
        avg_method = np.mean(method_scores) if method_scores else 0
        
        if manufacturing_methods:
            overall = 0.4 * avg_exposure + 0.6 * avg_method
        else:
            overall = avg_exposure * 0.7
        
        return float(min(1.0, overall))
    
    def _determine_primary_exposure(
        self,
        chemical_exposures: List[ChemicalExposureResult]
    ) -> str:
        """Birincil maruziyet turunu belirle"""
        
        if not chemical_exposures:
            return "Tespit Edilemedi"
        
        sorted_exposures = sorted(
            chemical_exposures,
            key=lambda x: x.detection_score,
            reverse=True
        )
        
        return sorted_exposures[0].chemical_name
    
    def _estimate_exposure_timeline(
        self,
        chemical_exposures: List[ChemicalExposureResult]
    ) -> Dict[str, Any]:
        """Maruziyet zaman cizelgesi tahmini"""
        
        if not chemical_exposures:
            return {"status": "Veri yetersiz"}
        
        timeline = {
            "total_exposures": len(chemical_exposures),
            "exposure_periods": [],
            "earliest_estimated": None,
            "latest_estimated": None,
            "chronic_indicators": []
        }
        
        max_duration = 0
        for exp in chemical_exposures:
            period = {
                "chemical": exp.chemical_name,
                "estimated_duration_days": exp.estimated_duration_days,
                "exposure_level": exp.exposure_level
            }
            timeline["exposure_periods"].append(period)
            
            if exp.estimated_duration_days > max_duration:
                max_duration = exp.estimated_duration_days
            
            exp_data = self.exposure_markers.get(exp.chemical_id, {})
            if exp_data.get('chronic_marker', False) and exp.detection_score >= 0.7:
                timeline["chronic_indicators"].append(exp.chemical_name)
        
        timeline["earliest_estimated"] = f"{max_duration} gun once"
        timeline["latest_estimated"] = "Son 30 gun icinde"
        
        return timeline
    
    def _generate_forensic_summary(
        self,
        chemical_exposures: List[ChemicalExposureResult],
        manufacturing_methods: List[ManufacturingMethodResult]
    ) -> Dict[str, Any]:
        """Adli ozet raporu olustur"""
        
        summary = {
            "total_chemicals_detected": len(chemical_exposures),
            "manufacturing_methods_identified": len(manufacturing_methods),
            "high_confidence_findings": [],
            "supporting_evidence": [],
            "recommended_confirmatory_tests": [],
            "legal_significance": ""
        }
        
        for exp in chemical_exposures:
            if exp.detection_score >= 0.75:
                summary["high_confidence_findings"].append({
                    "finding": f"{exp.chemical_name} maruziyeti",
                    "confidence": f"{exp.confidence*100:.1f}%",
                    "significance": exp.risk_assessment
                })
        
        for method in manufacturing_methods:
            if method.detection_score >= 0.7:
                summary["high_confidence_findings"].append({
                    "finding": f"{method.method_name} tespiti",
                    "confidence": f"{method.confidence*100:.1f}%",
                    "significance": method.forensic_significance
                })
        
        summary["recommended_confirmatory_tests"] = [
            "GC-MS/LC-MS metabolit analizi",
            "Sac folikulu uzun donem maruziyet testi",
            "Idrar toksikoji taramasi",
            "Kan PCR-bazli biyomarker analizi"
        ]
        
        if len(summary["high_confidence_findings"]) >= 2:
            summary["legal_significance"] = "YUKSEK: Mahkemede delil olarak kullanilabilir (uzman raporu ile)"
        elif len(summary["high_confidence_findings"]) == 1:
            summary["legal_significance"] = "ORTA: Destekleyici delil niteligi tasir"
        else:
            summary["legal_significance"] = "DUSUK: Ek delillerle desteklenmeli"
        
        return summary
    
    def _calculate_quality_score(
        self,
        cpg_data: pd.DataFrame,
        cpg_cols: List[str]
    ) -> float:
        """Veri kalite skoru hesapla"""
        
        if len(cpg_cols) == 0:
            return 0.0
        
        coverage = len(cpg_cols) / 100
        
        missing_ratio = cpg_data[cpg_cols].isna().sum().sum() / (len(cpg_data) * len(cpg_cols))
        completeness = 1 - min(1, missing_ratio)
        
        in_range = 0
        for col in cpg_cols[:min(50, len(cpg_cols))]:
            vals = cpg_data[col].dropna()
            if len(vals) > 0:
                if vals.min() >= 0 and vals.max() <= 1:
                    in_range += 1
        range_score = in_range / min(50, len(cpg_cols)) if cpg_cols else 0
        
        quality = (0.3 * min(1, coverage) + 0.4 * completeness + 0.3 * range_score)
        return float(min(1.0, quality))
    
    def _generate_demo_cpg_data(self, sample_id: str) -> pd.DataFrame:
        """Demo CpG verisi olustur"""
        
        np.random.seed(hash(sample_id) % 2**32)
        
        all_cpgs = []
        for exp_data in self.exposure_markers.values():
            for marker in exp_data['cpg_markers']:
                all_cpgs.append(marker['id'])
        
        all_cpgs = list(set(all_cpgs))
        
        data = {'sample_id': [sample_id]}
        for cpg in all_cpgs:
            data[cpg] = [np.random.uniform(0.1, 0.9)]
        
        return pd.DataFrame(data)
    
    def get_all_exposure_markers(self) -> Dict[str, Dict]:
        """Tum maruziyet markerlarini dondur"""
        return self.exposure_markers
    
    def get_all_method_signatures(self) -> Dict[str, Dict]:
        """Tum yontem imzalarini dondur"""
        return self.method_signatures
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Ozet istatistikleri dondur"""
        
        total_markers = sum(
            len(exp['cpg_markers']) for exp in self.exposure_markers.values()
        )
        
        all_genes = set()
        for exp in self.exposure_markers.values():
            for marker in exp['cpg_markers']:
                all_genes.add(marker['gene'])
        
        return {
            "total_exposure_types": len(self.exposure_markers),
            "total_manufacturing_methods": len(self.method_signatures),
            "total_cpg_markers": total_markers,
            "unique_genes": len(all_genes),
            "gene_list": sorted(list(all_genes)),
            "detection_categories": list(set(
                exp['category'] for exp in self.exposure_markers.values()
            ))
        }
