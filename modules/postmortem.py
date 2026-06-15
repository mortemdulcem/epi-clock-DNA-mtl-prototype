# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Postmortem Validasyon Modülü
PMI (Postmortem Interval) düzeltme algoritması ve beyin dokusu analizi
PDF Referans: Tablo 22-25
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from scipy import stats


@dataclass
# nrcdnl94
class PMICorrectionResult:
    # nrcdnl94
    """PMI düzeltme sonucu"""
    original_age: float
    corrected_age: float
    pmi_hours: float
    tissue_ph: float
    correction_factor: float
    quality_category: str
    reliability_score: float


class PostmortemValidator:
    # nrcdnl94
    """
    Postmortem beyin dokusu örneklerinde epigenetik yaş validasyonu
    PDF'deki Tablo 22-25 verilerine dayanmaktadır
    """
    
    def __init__(self):
        self.pmi_coefficient = 0.08
        self.pmi_intercept = 0.12
        
        self.ph_thresholds = {
            'excellent': (6.5, 10.0),
            'good': (6.0, 6.5),
            'moderate': (5.5, 6.0),
            'poor': (0.0, 5.5)
        }
        
        self.ph_quality_metrics = {
            'excellent': {'mae': 2.8, 'mae_ci': (2.1, 3.6), 'r2': 0.93, 'usability': 'Optimal'},
            'good': {'mae': 3.6, 'mae_ci': (3.0, 4.3), 'r2': 0.89, 'usability': 'İyi'},
            'moderate': {'mae': 5.1, 'mae_ci': (4.2, 6.1), 'r2': 0.78, 'usability': 'Dikkatli Kullanım'},
            'poor': {'mae': 8.4, 'mae_ci': (6.7, 10.3), 'r2': 0.52, 'usability': 'Önerilmez'}
        }
        
        self.brain_regions = {
            'prefrontal_cortex': {
                'name': 'Prefrontal Korteks',
                'abbreviation': 'PFC',
                'n': 48,
                'horvath_eaa': 5.3,
                'eaa_ci': (4.2, 6.5),
                'functional_significance': 'Karar verme, dürtü kontrolü'
            },
            'nucleus_accumbens': {
                'name': 'Nucleus Accumbens',
                'abbreviation': 'NAc',
                'n': 36,
                'horvath_eaa': 4.1,
                'eaa_ci': (3.2, 5.1),
                'functional_significance': 'Ödül sistemi, bağımlılık merkezi'
            },
            'hippocampus': {
                'name': 'Hippokampus',
                'abbreviation': 'HPC',
                'n': 24,
                'horvath_eaa': 3.2,
                'eaa_ci': (2.3, 4.2),
                'functional_significance': 'Bellek, öğrenme'
            }
        }
        
        self.validation_metrics = {
            'before_correction': {
                'mae': 7.2, 'mae_ci': (6.4, 8.1),
                'rmse': 9.1, 'rmse_ci': (8.1, 10.2),
                'r2': 0.72, 'r2_ci': (0.67, 0.77),
                'calibration_slope': 0.81, 'slope_ci': (0.76, 0.86)
            },
            'after_correction': {
                'mae': 3.8, 'mae_ci': (3.2, 4.5),
                'rmse': 4.9, 'rmse_ci': (4.2, 5.7),
                'r2': 0.87, 'r2_ci': (0.83, 0.91),
                'calibration_slope': 0.94, 'slope_ci': (0.90, 0.98)
            },
            'improvement': {
                'mae_reduction': 47,
                'rmse_reduction': 46,
                'r2_increase': 21,
                'slope_improvement': 16
            }
        }
    
    def calculate_pmi_error(self, pmi_hours: float) -> float:
        """
        PMI'ya bağlı tahmin hatasını hesapla
        Lineer model: Hata = 0.08 × PMI + 0.12
        """
        return self.pmi_coefficient * pmi_hours + self.pmi_intercept
    
    def get_ph_quality_category(self, ph: float) -> str:
        """Doku pH'sına göre kalite kategorisini belirle"""
        for category, (low, high) in self.ph_thresholds.items():
            if low <= ph < high:
                return category
        return 'poor'
    
    def apply_pmi_correction(
        self, 
        epigenetic_age: float, 
        pmi_hours: float, 
        tissue_ph: float
    ) -> PMICorrectionResult:
        """
        PMI düzeltme algoritmasını uygula
        
        Args:
            epigenetic_age: Ham epigenetik yaş tahmini
            pmi_hours: Postmortem interval (saat)
            tissue_ph: Doku pH değeri
            
        Returns:
            PMICorrectionResult: Düzeltilmiş yaş ve kalite metrikleri
        """
        pmi_error = self.calculate_pmi_error(pmi_hours)
        
        quality_category = self.get_ph_quality_category(tissue_ph)
        ph_metrics = self.ph_quality_metrics[quality_category]
        
        ph_adjustment = 1.0
        if quality_category == 'moderate':
            ph_adjustment = 0.85
        elif quality_category == 'poor':
            ph_adjustment = 0.6
        
        correction_factor = pmi_error * ph_adjustment
        corrected_age = epigenetic_age - correction_factor
        
        reliability_score = ph_metrics['r2'] * (1 - pmi_hours / 100)
        reliability_score = max(0.3, min(1.0, reliability_score))
        
        return PMICorrectionResult(
            original_age=epigenetic_age,
            corrected_age=corrected_age,
            pmi_hours=pmi_hours,
            tissue_ph=tissue_ph,
            correction_factor=correction_factor,
            quality_category=quality_category,
            reliability_score=reliability_score
        )
    
    def get_brain_region_eaa(self, region: str) -> Dict:
        """Belirli beyin bölgesi için EAA verilerini getir"""
        if region in self.brain_regions:
            return self.brain_regions[region]
        return None
    
    def compare_brain_regions(self) -> pd.DataFrame:
        """Beyin bölgeleri arası EAA karşılaştırması"""
        data = []
        for region_id, region_data in self.brain_regions.items():
            data.append({
                'Beyin Bölgesi': region_data['name'],
                'n': region_data['n'],
                'Horvath EAA (yıl)': region_data['horvath_eaa'],
                '95% CI': f"({region_data['eaa_ci'][0]}-{region_data['eaa_ci'][1]})",
                'Fonksiyonel Önemi': region_data['functional_significance']
            })
        return pd.DataFrame(data)
    
    def get_posthoc_comparisons(self) -> pd.DataFrame:
        """Tukey HSD post-hoc karşılaştırmaları"""
        comparisons = [
            {
                'Karşılaştırma': 'Prefrontal Korteks vs Nucleus Accumbens',
                'Ortalama Fark (yıl)': 1.2,
                'p-değeri': 0.024,
                'Anlamlılık': '*'
            },
            {
                'Karşılaştırma': 'Prefrontal Korteks vs Hippokampus',
                'Ortalama Fark (yıl)': 2.1,
                'p-değeri': '<0.001',
                'Anlamlılık': '***'
            },
            {
                'Karşılaştırma': 'Nucleus Accumbens vs Hippokampus',
                'Ortalama Fark (yıl)': 0.9,
                'p-değeri': 0.18,
                'Anlamlılık': 'NS'
            }
        ]
        return pd.DataFrame(comparisons)
    
    def get_validation_summary(self) -> Dict:
        """Validasyon özet istatistiklerini getir"""
        return {
            'total_samples': 108,
            'pmi_range': '6-48 saat',
            'ph_range': '5.2-7.1',
            'before_correction': self.validation_metrics['before_correction'],
            'after_correction': self.validation_metrics['after_correction'],
            'improvement': self.validation_metrics['improvement']
        }
    
    def simulate_postmortem_analysis(
        self, 
        n_samples: int = 108,
        substance_type: str = 'mixed'
    ) -> pd.DataFrame:
        """
        Postmortem analiz simülasyonu
        """
        np.random.seed(42)
        
        chronological_ages = np.random.normal(52, 14, n_samples)
        chronological_ages = np.clip(chronological_ages, 25, 85)
        
        pmis = np.random.uniform(6, 48, n_samples)
        
        phs = np.random.normal(6.2, 0.5, n_samples)
        phs = np.clip(phs, 5.0, 7.2)
        
        regions = np.random.choice(
            ['Prefrontal Korteks', 'Nucleus Accumbens', 'Hippokampus'],
            n_samples,
            p=[0.44, 0.33, 0.22]
        )
        
        region_eaa_map = {
            'Prefrontal Korteks': 5.3,
            'Nucleus Accumbens': 4.1,
            'Hippokampus': 3.2
        }
        
        data = []
        for i in range(n_samples):
            chron_age = chronological_ages[i]
            pmi = pmis[i]
            ph = phs[i]
            region = regions[i]
            
            base_eaa = region_eaa_map[region]
            eaa_noise = np.random.normal(0, 1.5)
            eaa = base_eaa + eaa_noise
            
            raw_epigenetic_age = chron_age + eaa + self.calculate_pmi_error(pmi)
            
            result = self.apply_pmi_correction(raw_epigenetic_age, pmi, ph)
            
            data.append({
                'Sample_ID': f'PM{str(i+1).zfill(3)}',
                'Kronolojik Yaş': round(chron_age, 1),
                'PMI (saat)': round(pmi, 1),
                'Doku pH': round(ph, 2),
                'Beyin Bölgesi': region,
                'Ham Epigenetik Yaş': round(raw_epigenetic_age, 1),
                'Düzeltilmiş Epigenetik Yaş': round(result.corrected_age, 1),
                'EAA (yıl)': round(result.corrected_age - chron_age, 1),
                'Kalite Kategorisi': result.quality_category,
                'Güvenilirlik Skoru': round(result.reliability_score, 2)
            })
        
        return pd.DataFrame(data)
    
    def get_pmi_effect_model(self) -> Dict:
        """PMI etki modeli parametreleri"""
        return {
            'equation': 'Epigenetik yaş tahmini hatası = 0.08 × PMI (saat) + 0.12',
            'coefficient': self.pmi_coefficient,
            'intercept': self.pmi_intercept,
            'r2': 0.43,
            'p_value': '<0.001',
            'interpretation': 'Her 10 saat PMI artışı için yaklaşık 0.8 yıl ek hata'
        }
    
    def get_ph_quality_table(self) -> pd.DataFrame:
        """pH kalite değerlendirme tablosu"""
        data = []
        ph_ranges = {
            'excellent': '>6.5',
            'good': '6.0-6.5',
            'moderate': '5.5-6.0',
            'poor': '<5.5'
        }
        n_values = {'excellent': 28, 'good': 42, 'moderate': 26, 'poor': 12}
        
        for category, metrics in self.ph_quality_metrics.items():
            data.append({
                'pH Kategorisi': category.replace('excellent', 'Mükemmel Kalite')
                                        .replace('good', 'İyi Kalite')
                                        .replace('moderate', 'Orta Kalite')
                                        .replace('poor', 'Zayıf Kalite'),
                'pH Aralığı': ph_ranges[category],
                'n': n_values[category],
                'MAE (yıl)': metrics['mae'],
                '95% CI': f"({metrics['mae_ci'][0]}-{metrics['mae_ci'][1]})",
                'R²': metrics['r2'],
                'Kullanılabilirlik': metrics['usability']
            })
        return pd.DataFrame(data)


class ForensicApplications:
    # nrcdnl94
    """
    Adli uygulamalar için epigenetik analiz
    PDF Bölüm 4.5'e dayanmaktadır
    """
    
    def __init__(self):
        self.classification_accuracy = 87.3
        self.cpg_signature_count = 1847
        
        self.daubert_criteria = {
            'testability': {
                'status': 'Karşılanıyor',
                'evidence': '100\'den fazla peer-reviewed yayın'
            },
            'peer_review': {
                'status': 'Karşılanıyor',
                'evidence': 'Epigenetik saatler yaygın olarak yayınlanmış'
            },
            'error_rate': {
                'status': 'İyi karakterize edilmiş',
                'evidence': 'MAE=2-3 yıl (antemortem), 3.8 yıl (postmortem)'
            },
            'standards': {
                'status': 'Mevcut',
                'evidence': 'Illumina platformları, yaygın kabul'
            },
            'general_acceptance': {
                'status': 'Gelişmekte',
                'evidence': 'Henüz tam oluşmamış, destekleyici kanıt olarak kullanılmalı'
            }
        }
    
    def assess_chronic_exposure(
        self, 
        eaa: float, 
        cpg_signature_match: float
    ) -> Dict:
        """
        Kronik madde maruziyeti değerlendirmesi
        """
        if eaa > 5.0 and cpg_signature_match > 0.7:
            exposure_level = 'Yüksek'
            confidence = 'Güçlü kanıt'
        elif eaa > 3.0 and cpg_signature_match > 0.5:
            exposure_level = 'Orta'
            confidence = 'Orta düzey kanıt'
        elif eaa > 1.5:
            exposure_level = 'Düşük-Orta'
            confidence = 'Zayıf kanıt'
        else:
            exposure_level = 'Minimal/Yok'
            confidence = 'Yetersiz kanıt'
        
        return {
            'eaa': eaa,
            'cpg_match': cpg_signature_match,
            'exposure_level': exposure_level,
            'confidence': confidence,
            'note': 'Destekleyici kanıt olarak değerlendirilmeli, tek başına yeterli değil'
        }
    
    def get_daubert_summary(self) -> pd.DataFrame:
        """Daubert kriterleri özeti"""
        data = []
        for criterion, info in self.daubert_criteria.items():
            data.append({
                'Kriter': criterion.replace('_', ' ').title(),
                'Durum': info['status'],
                'Kanıt': info['evidence']
            })
        return pd.DataFrame(data)
    
    def get_forensic_applications(self) -> List[Dict]:
        """Adli uygulama alanları"""
        return [
            {
                'application': 'Kronik Maruziyet Tespiti',
                'description': 'Akut tespit penceresinin ötesinde madde kullanım geçmişi',
                'advantage': 'Aylar-yıllar sonra bile değerlendirme imkanı',
                'limitation': 'Tek başına yeterli değil, destekleyici kanıt'
            },
            {
                'application': 'Madde Türü Sınıflandırması',
                'description': '1,847 CpG imzası ile %87.3 doğruluk',
                'advantage': 'Birincil madde maruziyetini belirleme',
                'limitation': 'Çoklu madde kullanımında zorlaşır'
            },
            {
                'application': 'Postmortem Değerlendirme',
                'description': 'PMI düzeltme ile MAE=3.8 yıl',
                'advantage': 'Antemortem geçmişi bilinmeyen vakalarda',
                'limitation': 'pH<6.0 örneklerde düşük güvenilirlik'
            }
        ]


# End of module - # nrcdnl94