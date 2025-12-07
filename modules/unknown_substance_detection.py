# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Bilinmeyen Madde Tespit Modulu - Anomali Tabanli ML Yaklasimi

Bu modul, veritabaninda kayitli olmayan maddeleri tespit etmek icin
makine ogrenmesi tabanli anomali tespiti kullanir.

Yontemler:
1. Isolation Forest - Anomali skoru hesaplama
2. Local Outlier Factor (LOF) - Yerel yogunluk anomalisi
3. Autoencoder - Rekonstrüksiyon hatasi
4. Z-score tabanli sapma analizi
5. Mahalanobis mesafesi

UNODC Standartlari:
- Renk: #0050A0 (UNODC Blue), #003366 (Dark Navy), #00A7D8 (Turquoise)
- Emoji kullanimi YASAKTIR
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class AnomalyType(Enum):
    NORMAL = "Normal Profil"
    MILD_ANOMALY = "Hafif Anomali"
    MODERATE_ANOMALY = "Orta Anomali"
    SEVERE_ANOMALY = "Ciddi Anomali"
    UNKNOWN_SUBSTANCE = "Bilinmeyen Madde Izi"


class AnomalySource(Enum):
    UNKNOWN_SUBSTANCE = "Bilinmeyen Madde"
    NOVEL_NPS = "Yeni Sentetik Madde (NPS)"
    METABOLITE = "Tanimlanamayan Metabolit"
    CONTAMINATION = "Cevresel Kontaminasyon"
    GENETIC_VARIANT = "Genetik Varyant Etkisi"
    DISEASE_MARKER = "Hastalik Markeri"
    MIXED_EXPOSURE = "Karisik Maruziyet"


@dataclass
class AnomalyDetectionResult:
    """Anomali tespit sonucu"""
    sample_id: str
    is_anomaly: bool
    anomaly_type: AnomalyType
    anomaly_score: float
    confidence: float
    likely_sources: List[Dict[str, Any]]
    affected_cpgs: List[str]
    deviation_magnitude: float
    isolation_score: float
    lof_score: float
    reconstruction_error: float
    z_scores: Dict[str, float]
    interpretation: str
    recommendations: List[str]


@dataclass
class UnknownSubstanceProfile:
    """Bilinmeyen madde profili"""
    profile_id: str
    detection_timestamp: str
    anomaly_pattern: Dict[str, float]
    affected_pathways: List[str]
    similar_known_substances: List[Dict[str, float]]
    estimated_potency: str
    risk_assessment: str
    cpg_signature: List[str]


class ReferenceProfileBuilder:
    """Normal metilasyon profili referans veritabani"""
    
    def __init__(self):
        self.reference_profiles = self._build_reference_database()
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)
        self._fitted = False
    
    def _build_reference_database(self) -> Dict[str, np.ndarray]:
        """Referans profilleri olustur - nrcdnl94"""
        np.random.seed(42)
        
        reference_cpgs = [
            "cg05575921", "cg03636183", "cg21566642", "cg01940273", "cg05951221",
            "cg06126421", "cg23576855", "cg19859270", "cg14753356", "cg09935388",
            "cg04987734", "cg02583484", "cg00252813", "cg08697849", "cg00574958",
            "cg17739917", "cg06690548", "cg12803068", "cg02242964", "cg04180046",
            "cg07123182", "cg15768986", "cg22132788", "cg14179389", "cg25949550",
            "cg10406920", "cg03821126", "cg08709672", "cg11314684", "cg16867657",
            "cg18120259", "cg06500161", "cg21161138", "cg19693031", "cg01656216",
            "cg27243685", "cg23771366", "cg11330918", "cg19418362", "cg00500440"
        ]
        
        n_healthy = 500
        healthy_profiles = np.random.beta(8, 2, size=(n_healthy, len(reference_cpgs)))
        healthy_profiles = healthy_profiles * 0.4 + 0.3
        
        return {
            'cpg_ids': reference_cpgs,
            'healthy_mean': np.mean(healthy_profiles, axis=0),
            'healthy_std': np.std(healthy_profiles, axis=0),
            'healthy_cov': np.cov(healthy_profiles.T),
            'profiles': healthy_profiles
        }
    
    def fit(self):
        """Referans profillere modeli fit et"""
        if not self._fitted:
            profiles = self.reference_profiles['profiles']
            self.scaler.fit(profiles)
            scaled = self.scaler.transform(profiles)
            self.pca.fit(scaled)
            self._fitted = True
    
    def get_reference_cpgs(self) -> List[str]:
        """Referans CpG listesi"""
        return self.reference_profiles['cpg_ids']
    
    def get_healthy_statistics(self) -> Tuple[np.ndarray, np.ndarray]:
        """Saglikli referans istatistikleri"""
        return (
            self.reference_profiles['healthy_mean'],
            self.reference_profiles['healthy_std']
        )


class IsolationForestDetector:
    """Isolation Forest tabanli anomali tespiti - nrcdnl94"""
    
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
            max_samples='auto'
        )
        self.scaler = StandardScaler()
        self._fitted = False
    
    def fit(self, reference_data: np.ndarray):
        """Referans veri ile modeli egit"""
        scaled = self.scaler.fit_transform(reference_data)
        self.model.fit(scaled)
        self._fitted = True
    
    def predict(self, sample: np.ndarray) -> Tuple[bool, float]:
        """Ornekte anomali tespit et"""
        if not self._fitted:
            return False, 0.0
        
        if len(sample.shape) == 1:
            sample = sample.reshape(1, -1)
        
        scaled = self.scaler.transform(sample)
        prediction = self.model.predict(scaled)
        score = self.model.decision_function(scaled)
        
        is_anomaly = prediction[0] == -1
        anomaly_score = -score[0]
        
        normalized_score = (anomaly_score + 0.5) / 1.0
        normalized_score = max(0, min(1, normalized_score))
        
        return is_anomaly, normalized_score


class LOFDetector:
    """Local Outlier Factor tabanli anomali tespiti - nrcdnl94"""
    
    def __init__(self, n_neighbors: int = 20):
        self.n_neighbors = n_neighbors
        self.reference_data = None
        self.scaler = StandardScaler()
    
    def fit(self, reference_data: np.ndarray):
        """Referans veri kaydet"""
        self.reference_data = self.scaler.fit_transform(reference_data)
    
    def predict(self, sample: np.ndarray) -> Tuple[bool, float]:
        """LOF skoru hesapla"""
        if self.reference_data is None:
            return False, 0.0
        
        if len(sample.shape) == 1:
            sample = sample.reshape(1, -1)
        
        scaled_sample = self.scaler.transform(sample)
        
        combined = np.vstack([self.reference_data, scaled_sample])
        
        lof = LocalOutlierFactor(n_neighbors=min(self.n_neighbors, len(combined)-1))
        predictions = lof.fit_predict(combined)
        scores = lof.negative_outlier_factor_
        
        sample_prediction = predictions[-1]
        sample_score = -scores[-1]
        
        is_anomaly = sample_prediction == -1
        normalized_score = min(1, max(0, (sample_score - 1) / 2))
        
        return is_anomaly, normalized_score


class AutoencoderAnomalyDetector:
    """Basit Autoencoder tabanli anomali tespiti (NumPy) - nrcdnl94"""
    
    def __init__(self, encoding_dim: int = 10):
        self.encoding_dim = encoding_dim
        self.mean = None
        self.std = None
        self.pca = None
        self._fitted = False
    
    def fit(self, reference_data: np.ndarray):
        """PCA tabanli basit autoencoder simulasyonu"""
        self.mean = np.mean(reference_data, axis=0)
        self.std = np.std(reference_data, axis=0) + 1e-8
        
        normalized = (reference_data - self.mean) / self.std
        
        self.pca = PCA(n_components=min(self.encoding_dim, reference_data.shape[1]))
        self.pca.fit(normalized)
        self._fitted = True
    
    def predict(self, sample: np.ndarray) -> Tuple[bool, float]:
        """Rekonstruksiyon hatasi hesapla"""
        if not self._fitted:
            return False, 0.0
        
        if len(sample.shape) == 1:
            sample = sample.reshape(1, -1)
        
        normalized = (sample - self.mean) / self.std
        
        encoded = self.pca.transform(normalized)
        reconstructed = self.pca.inverse_transform(encoded)
        
        mse = np.mean((normalized - reconstructed) ** 2)
        
        threshold = 0.5
        is_anomaly = mse > threshold
        
        normalized_score = min(1, mse / 2)
        
        return is_anomaly, normalized_score


class ZScoreDetector:
    """Z-score tabanli sapma analizi - nrcdnl94"""
    
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.mean = None
        self.std = None
    
    def fit(self, reference_data: np.ndarray):
        """Referans istatistikleri hesapla"""
        self.mean = np.mean(reference_data, axis=0)
        self.std = np.std(reference_data, axis=0) + 1e-8
    
    def predict(self, sample: np.ndarray) -> Tuple[bool, float, Dict[str, float]]:
        """Z-score hesapla"""
        if self.mean is None:
            return False, 0.0, {}
        
        if len(sample.shape) == 1:
            sample_flat = sample
        else:
            sample_flat = sample.flatten()
        
        z_scores = (sample_flat - self.mean) / self.std
        
        extreme_count = np.sum(np.abs(z_scores) > self.threshold)
        extreme_ratio = extreme_count / len(z_scores)
        
        is_anomaly = extreme_ratio > 0.1
        anomaly_score = min(1, extreme_ratio * 5)
        
        z_dict = {f"cpg_{i}": float(z) for i, z in enumerate(z_scores) if abs(z) > 2}
        
        return is_anomaly, anomaly_score, z_dict


class MahalanobisDetector:
    """Mahalanobis mesafesi tabanli anomali tespiti - nrcdnl94"""
    
    def __init__(self, threshold_percentile: float = 95):
        self.threshold_percentile = threshold_percentile
        self.mean = None
        self.cov_inv = None
        self.threshold = None
    
    def fit(self, reference_data: np.ndarray):
        """Referans istatistikleri hesapla"""
        self.mean = np.mean(reference_data, axis=0)
        cov = np.cov(reference_data.T)
        
        try:
            self.cov_inv = np.linalg.inv(cov + np.eye(cov.shape[0]) * 1e-6)
        except np.linalg.LinAlgError:
            self.cov_inv = np.eye(cov.shape[0])
        
        distances = []
        for sample in reference_data:
            d = self._calculate_distance(sample)
            distances.append(d)
        
        self.threshold = np.percentile(distances, self.threshold_percentile)
    
    def _calculate_distance(self, sample: np.ndarray) -> float:
        """Mahalanobis mesafesi hesapla"""
        diff = sample - self.mean
        distance = np.sqrt(np.dot(np.dot(diff, self.cov_inv), diff))
        return distance
    
    def predict(self, sample: np.ndarray) -> Tuple[bool, float]:
        """Anomali tespit et"""
        if self.mean is None:
            return False, 0.0
        
        if len(sample.shape) > 1:
            sample = sample.flatten()
        
        distance = self._calculate_distance(sample)
        
        is_anomaly = distance > self.threshold if self.threshold else False
        
        normalized_score = min(1, distance / (self.threshold * 2)) if self.threshold else 0
        
        return is_anomaly, normalized_score


class UnknownSubstanceDetector:
    """
    Ana bilinmeyen madde tespit sinifi
    Tum anomali tespit yontemlerini birlestirir
    Author: nrcdnl94
    """
    
    def __init__(self):
        self.reference_builder = ReferenceProfileBuilder()
        self.isolation_detector = IsolationForestDetector()
        self.lof_detector = LOFDetector()
        self.autoencoder_detector = AutoencoderAnomalyDetector()
        self.zscore_detector = ZScoreDetector()
        self.mahalanobis_detector = MahalanobisDetector()
        self._fitted = False
        
        self._fit_all_models()
    
    def _fit_all_models(self):
        """Tum modelleri referans veriye fit et"""
        self.reference_builder.fit()
        reference_data = self.reference_builder.reference_profiles['profiles']
        
        self.isolation_detector.fit(reference_data)
        self.lof_detector.fit(reference_data)
        self.autoencoder_detector.fit(reference_data)
        self.zscore_detector.fit(reference_data)
        self.mahalanobis_detector.fit(reference_data)
        
        self._fitted = True
    
    def get_reference_cpgs(self) -> List[str]:
        """Referans CpG listesi"""
        return self.reference_builder.get_reference_cpgs()
    
    def analyze_sample(self, methylation_data: pd.DataFrame, sample_id: str = "SAMPLE_001") -> AnomalyDetectionResult:
        """
        Ornegi analiz et ve anomali tespit et
        
        Args:
            methylation_data: CpG ve Beta sutunlari iceren DataFrame
            sample_id: Ornek kimlik numarasi
            
        Returns:
            AnomalyDetectionResult: Detayli anomali analiz sonucu
        """
        reference_cpgs = self.get_reference_cpgs()
        
        if 'CpG' in methylation_data.columns and 'Beta' in methylation_data.columns:
            beta_dict = dict(zip(methylation_data['CpG'], methylation_data['Beta']))
        else:
            beta_dict = {}
            for col in methylation_data.columns:
                if str(col).startswith('cg'):
                    beta_dict[col] = methylation_data[col].mean()
        
        sample_vector = []
        matched_cpgs = []
        for cpg in reference_cpgs:
            if cpg in beta_dict:
                sample_vector.append(beta_dict[cpg])
                matched_cpgs.append(cpg)
            else:
                mean_val = self.reference_builder.reference_profiles['healthy_mean'][
                    reference_cpgs.index(cpg)
                ]
                sample_vector.append(mean_val)
        
        sample_array = np.array(sample_vector)
        
        iso_anomaly, iso_score = self.isolation_detector.predict(sample_array)
        lof_anomaly, lof_score = self.lof_detector.predict(sample_array)
        ae_anomaly, ae_score = self.autoencoder_detector.predict(sample_array)
        z_anomaly, z_score, z_dict = self.zscore_detector.predict(sample_array)
        mah_anomaly, mah_score = self.mahalanobis_detector.predict(sample_array)
        
        anomaly_votes = sum([iso_anomaly, lof_anomaly, ae_anomaly, z_anomaly, mah_anomaly])
        is_anomaly = anomaly_votes >= 3
        
        combined_score = (
            iso_score * 0.25 +
            lof_score * 0.25 +
            ae_score * 0.20 +
            z_score * 0.15 +
            mah_score * 0.15
        )
        
        if combined_score < 0.2:
            anomaly_type = AnomalyType.NORMAL
        elif combined_score < 0.4:
            anomaly_type = AnomalyType.MILD_ANOMALY
        elif combined_score < 0.6:
            anomaly_type = AnomalyType.MODERATE_ANOMALY
        elif combined_score < 0.8:
            anomaly_type = AnomalyType.SEVERE_ANOMALY
        else:
            anomaly_type = AnomalyType.UNKNOWN_SUBSTANCE
        
        healthy_mean, healthy_std = self.reference_builder.get_healthy_statistics()
        deviations = np.abs(sample_array - healthy_mean) / (healthy_std + 1e-8)
        affected_indices = np.where(deviations > 2)[0]
        affected_cpgs = [reference_cpgs[i] for i in affected_indices[:10]]
        
        likely_sources = self._infer_likely_sources(
            combined_score, affected_cpgs, anomaly_type
        )
        
        confidence = min(0.95, 0.5 + anomaly_votes * 0.1)
        
        interpretation = self._generate_interpretation(
            anomaly_type, combined_score, affected_cpgs, likely_sources
        )
        
        recommendations = self._generate_recommendations(
            anomaly_type, combined_score, likely_sources
        )
        
        return AnomalyDetectionResult(
            sample_id=sample_id,
            is_anomaly=is_anomaly,
            anomaly_type=anomaly_type,
            anomaly_score=round(combined_score, 3),
            confidence=round(confidence, 2),
            likely_sources=likely_sources,
            affected_cpgs=affected_cpgs,
            deviation_magnitude=round(float(np.mean(deviations)), 3),
            isolation_score=round(iso_score, 3),
            lof_score=round(lof_score, 3),
            reconstruction_error=round(ae_score, 3),
            z_scores=z_dict,
            interpretation=interpretation,
            recommendations=recommendations
        )
    
    def _infer_likely_sources(
        self, 
        score: float, 
        affected_cpgs: List[str],
        anomaly_type: AnomalyType
    ) -> List[Dict[str, Any]]:
        """Muhtemel anomali kaynaklarini cikar"""
        sources = []
        
        if anomaly_type == AnomalyType.UNKNOWN_SUBSTANCE:
            sources.append({
                'source': AnomalySource.UNKNOWN_SUBSTANCE.value,
                'probability': min(0.9, score + 0.2),
                'evidence': 'Coklu anomali dedektorleri tarafindan tespit edildi',
                'affected_regions': affected_cpgs[:5]
            })
            sources.append({
                'source': AnomalySource.NOVEL_NPS.value,
                'probability': min(0.7, score),
                'evidence': 'Bilinen madde imzalariyla eslesmiyor',
                'affected_regions': affected_cpgs[:3]
            })
        
        elif anomaly_type == AnomalyType.SEVERE_ANOMALY:
            sources.append({
                'source': AnomalySource.MIXED_EXPOSURE.value,
                'probability': min(0.75, score + 0.1),
                'evidence': 'Birden fazla yolak etkilenmis',
                'affected_regions': affected_cpgs[:4]
            })
            sources.append({
                'source': AnomalySource.METABOLITE.value,
                'probability': min(0.6, score - 0.1),
                'evidence': 'Ara metabolit imzasi olabilir',
                'affected_regions': affected_cpgs[:2]
            })
        
        elif anomaly_type == AnomalyType.MODERATE_ANOMALY:
            sources.append({
                'source': AnomalySource.CONTAMINATION.value,
                'probability': min(0.5, score),
                'evidence': 'Cevresel maruziyetle tutarli',
                'affected_regions': affected_cpgs[:3]
            })
        
        elif anomaly_type == AnomalyType.MILD_ANOMALY:
            sources.append({
                'source': AnomalySource.GENETIC_VARIANT.value,
                'probability': 0.4,
                'evidence': 'Dogal varyasyon sinirlarinda',
                'affected_regions': affected_cpgs[:2]
            })
        
        return sources
    
    def _generate_interpretation(
        self,
        anomaly_type: AnomalyType,
        score: float,
        affected_cpgs: List[str],
        likely_sources: List[Dict]
    ) -> str:
        """Klinik yorum olustur"""
        
        if anomaly_type == AnomalyType.NORMAL:
            return "Metilasyon profili normal sinirlar icinde. Bilinen veya bilinmeyen madde izi tespit edilmedi."
        
        elif anomaly_type == AnomalyType.MILD_ANOMALY:
            return f"Hafif metilasyon sapmasi tespit edildi (skor: {score:.2f}). Bu, dogal varyasyon veya dusuk duzeyde cevresel maruziyet ile aciklanabilir. {len(affected_cpgs)} CpG bolgesi etkilenmis."
        
        elif anomaly_type == AnomalyType.MODERATE_ANOMALY:
            return f"Orta duzeyde anomali tespit edildi (skor: {score:.2f}). {len(affected_cpgs)} CpG bolgesinde normal disinda degerler goruldu. Cevresel maruziyet veya dusuk dozda madde kullanimi mumkun."
        
        elif anomaly_type == AnomalyType.SEVERE_ANOMALY:
            sources_str = ", ".join([s['source'] for s in likely_sources[:2]])
            return f"Ciddi metilasyon anomalisi tespit edildi (skor: {score:.2f}). Muhtemel kaynaklar: {sources_str}. {len(affected_cpgs)} CpG bolgesi belirgin sekilde etkilenmis. Ileri analiz onerilir."
        
        else:
            return f"BILINMEYEN MADDE IZI TESPIT EDILDI (skor: {score:.2f}). Veritabanindaki hicbir bilinen madde imzasiyla eslesmeyen anormal metilasyon oruntuleri goruldu. {len(affected_cpgs)} CpG bolgesinde ciddi sapmalar mevcut. Bu, yeni bir sentetik madde (NPS) veya tanimlanmamis bir metabolit isareti olabilir."
    
    def _generate_recommendations(
        self,
        anomaly_type: AnomalyType,
        score: float,
        likely_sources: List[Dict]
    ) -> List[str]:
        """Klinik oneriler olustur"""
        recommendations = []
        
        if anomaly_type == AnomalyType.NORMAL:
            recommendations.append("Rutin takip yeterlidir")
        
        elif anomaly_type == AnomalyType.MILD_ANOMALY:
            recommendations.append("3-6 ay icinde kontrol ornekleme onerilir")
            recommendations.append("Cevresel maruziyet sorgulanmali")
        
        elif anomaly_type == AnomalyType.MODERATE_ANOMALY:
            recommendations.append("Detayli madde tarama paneli uygulanmali")
            recommendations.append("Klinik degerlendirme onerilir")
            recommendations.append("Ek biyolojik ornek alinmasi dusunulmeli")
        
        elif anomaly_type == AnomalyType.SEVERE_ANOMALY:
            recommendations.append("Acil klinik degerlendirme gerekli")
            recommendations.append("Kapsamli toksikoloji paneli uygulanmali")
            recommendations.append("Ileri molekuler analiz (LC-MS/MS) onerilir")
            recommendations.append("Hasta gecmisi ve cevresel maruziyetler detayli incelenmeli")
        
        else:
            recommendations.append("ACIL: Bilinmeyen madde protokolu baslatilmali")
            recommendations.append("Kapsamli toksikoloji paneli (GC-MS, LC-MS/MS)")
            recommendations.append("Ornek ileri analiz icin saklanmali")
            recommendations.append("Adli makamlar bilgilendirilmeli (gerekirse)")
            recommendations.append("Benzerligi yuksek bilinen maddeler icin hedefe yonelik testler")
            recommendations.append("Karsilastirmali NPS veritabani taramasi")
        
        return recommendations
    
    def generate_demo_unknown_substance(
        self, 
        base_substances: List[str] = None,
        anomaly_level: str = "moderate"
    ) -> pd.DataFrame:
        """
        Demo amacli bilinmeyen madde metilasyon verisi olustur
        
        Args:
            base_substances: Temel alinan maddeler (bilinen imzalari karistirmak icin)
            anomaly_level: Anomali seviyesi (mild, moderate, severe, unknown)
            
        Returns:
            DataFrame: Anomali iceren metilasyon verisi
        """
        reference_cpgs = self.get_reference_cpgs()
        healthy_mean, healthy_std = self.reference_builder.get_healthy_statistics()
        
        beta_values = {}
        for i, cpg in enumerate(reference_cpgs):
            beta_values[cpg] = np.random.normal(healthy_mean[i], healthy_std[i] * 0.5)
            beta_values[cpg] = np.clip(beta_values[cpg], 0.05, 0.95)
        
        if anomaly_level == "mild":
            n_affected = 3
            deviation = 0.08
        elif anomaly_level == "moderate":
            n_affected = 6
            deviation = 0.12
        elif anomaly_level == "severe":
            n_affected = 10
            deviation = 0.18
        else:
            n_affected = 15
            deviation = 0.25
        
        affected_indices = np.random.choice(len(reference_cpgs), n_affected, replace=False)
        for idx in affected_indices:
            cpg = reference_cpgs[idx]
            direction = np.random.choice([-1, 1])
            beta_values[cpg] += direction * deviation * np.random.uniform(0.8, 1.2)
            beta_values[cpg] = np.clip(beta_values[cpg], 0.02, 0.98)
        
        df = pd.DataFrame({
            'CpG': list(beta_values.keys()),
            'Beta': list(beta_values.values())
        })
        
        return df


def get_unknown_detector() -> UnknownSubstanceDetector:
    """Singleton detector instance"""
    global _unknown_detector
    try:
        return _unknown_detector
    except NameError:
        _unknown_detector = UnknownSubstanceDetector()
        return _unknown_detector


_unknown_detector = None


if __name__ == "__main__":
    detector = UnknownSubstanceDetector()
    
    demo_data = detector.generate_demo_unknown_substance(anomaly_level="unknown")
    result = detector.analyze_sample(demo_data, "DEMO_UNKNOWN_001")
    
    print(f"Anomali Tespit Edildi: {result.is_anomaly}")
    print(f"Anomali Tipi: {result.anomaly_type.value}")
    print(f"Anomali Skoru: {result.anomaly_score}")
    print(f"Guven: {result.confidence}")
    print(f"Yorum: {result.interpretation}")
    print(f"Oneriler: {result.recommendations}")
