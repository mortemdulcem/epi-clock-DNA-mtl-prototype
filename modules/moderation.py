"""
Moderasyon Analizi Modülü
DERS (Duygu Düzenleme) ve SCS-B (Öz-Kontrol) moderasyon etkileri
PDF Referans: Tablo 14-21, Bölüm 3.7
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from scipy import stats


@dataclass
class ModerationResult:
    """Moderasyon analizi sonucu"""
    moderator: str
    interaction_beta: float
    interaction_se: float
    interaction_ci: Tuple[float, float]
    interaction_p: float
    model_r2: float
    delta_r2: float
    f_statistic: float


class EmotionRegulationModerator:
    """
    Duygu Düzenleme (DERS) Moderasyon Analizi
    PDF Tablo 14-16'ya dayanmaktadır
    """
    
    def __init__(self):
        self.model_results = {
            'substance_duration': {'beta': 0.42, 'se': 0.06, 'ci': (0.30, 0.54), 'p': '<0.001'},
            'ders_score': {'beta': 0.28, 'se': 0.05, 'ci': (0.18, 0.38), 'p': '<0.001'},
            'interaction': {'beta': 0.38, 'se': 0.07, 'ci': (0.24, 0.52), 'p': '<0.001'},
            'model_r2': 0.67,
            'interaction_delta_r2': 0.09,
            'f_statistic': 42.3
        }
        
        self.simple_slopes = {
            'low_ders': {
                'level': 'Düşük DERS (-1 SD)',
                'beta': 0.18,
                'se': 0.05,
                'ci': (0.08, 0.28),
                'p': 0.001,
                'interpretation': 'İyi duygu düzenleme'
            },
            'mean_ders': {
                'level': 'Ortalama DERS',
                'beta': 0.42,
                'se': 0.06,
                'ci': (0.30, 0.54),
                'p': '<0.001',
                'interpretation': 'Orta düzenleme'
            },
            'high_ders': {
                'level': 'Yüksek DERS (+1 SD)',
                'beta': 0.66,
                'se': 0.07,
                'ci': (0.52, 0.80),
                'p': '<0.001',
                'interpretation': 'Zayıf duygu düzenleme'
            }
        }
        
        self.categorical_analysis = [
            {
                'category': 'İyi Düzenleme (DERS<60)',
                'n': 387,
                'substance_eaa': 1.8,
                'eaa_ci': (1.1, 2.6),
                'control_eaa': 0.2,
                'difference': 1.6,
                't_stat': 2.1,
                'p': 0.042
            },
            {
                'category': 'Orta Düzenleme (DERS 60-90)',
                'n': 624,
                'substance_eaa': 3.9,
                'eaa_ci': (3.3, 4.6),
                'control_eaa': 0.1,
                'difference': 3.8,
                't_stat': 8.7,
                'p': '<0.001'
            },
            {
                'category': 'Zayıf Düzenleme (DERS>90)',
                'n': 512,
                'substance_eaa': 6.2,
                'eaa_ci': (5.3, 7.2),
                'control_eaa': 0.3,
                'difference': 5.9,
                't_stat': 12.4,
                'p': '<0.001'
            }
        ]
        
        self.johnson_neyman = {
            'threshold': 68,
            'percent_above': 42,
            'interpretation': 'DERS skoru >68 eşiğinde madde kullanımının EAA üzerindeki etkisi istatistiksel olarak anlamlı'
        }
    
    def get_model_summary(self) -> pd.DataFrame:
        """Model özet tablosu"""
        data = [
            {
                'Model Terimi': 'Madde Kullanım Süresi',
                'β': self.model_results['substance_duration']['beta'],
                'SE': self.model_results['substance_duration']['se'],
                '95% GA': f"{self.model_results['substance_duration']['ci']}",
                'p-değeri': self.model_results['substance_duration']['p']
            },
            {
                'Model Terimi': 'DERS Skoru',
                'β': self.model_results['ders_score']['beta'],
                'SE': self.model_results['ders_score']['se'],
                '95% GA': f"{self.model_results['ders_score']['ci']}",
                'p-değeri': self.model_results['ders_score']['p']
            },
            {
                'Model Terimi': 'Madde × DERS Etkileşimi',
                'β': self.model_results['interaction']['beta'],
                'SE': self.model_results['interaction']['se'],
                '95% GA': f"{self.model_results['interaction']['ci']}",
                'p-değeri': self.model_results['interaction']['p']
            },
            {
                'Model Terimi': 'Model R²',
                'β': self.model_results['model_r2'],
                'SE': '-',
                '95% GA': '-',
                'p-değeri': '-'
            },
            {
                'Model Terimi': 'Etkileşim Terimi ΔR²',
                'β': self.model_results['interaction_delta_r2'],
                'SE': '-',
                '95% GA': '-',
                'p-değeri': '-'
            }
        ]
        return pd.DataFrame(data)
    
    def get_simple_slopes_table(self) -> pd.DataFrame:
        """Simple slopes analizi tablosu"""
        data = []
        for level, info in self.simple_slopes.items():
            data.append({
                'DERS Seviyesi': info['level'],
                'β': info['beta'],
                'SE': info['se'],
                '95% GA': f"{info['ci']}",
                'p-değeri': info['p'],
                'Yorum': info['interpretation']
            })
        return pd.DataFrame(data)
    
    def get_categorical_table(self) -> pd.DataFrame:
        """Kategorik DERS analizi tablosu"""
        data = []
        for cat in self.categorical_analysis:
            data.append({
                'DERS Kategorisi': cat['category'],
                'n': cat['n'],
                'Madde Kullanıcı EAA (yıl)': cat['substance_eaa'],
                '95% GA': f"{cat['eaa_ci']}",
                'Kontrol EAA (yıl)': cat['control_eaa'],
                'Fark (yıl)': cat['difference'],
                't-istatistiği': cat['t_stat'],
                'p-değeri': cat['p']
            })
        return pd.DataFrame(data)
    
    def calculate_moderation_effect(self, ders_score: float) -> float:
        """DERS skoruna göre moderasyon etkisini hesapla"""
        mean_ders = 75
        sd_ders = 20
        z_score = (ders_score - mean_ders) / sd_ders
        
        base_effect = self.model_results['substance_duration']['beta']
        moderation = self.model_results['interaction']['beta'] * z_score
        
        return base_effect + moderation


class SelfControlModerator:
    """
    Öz-Kontrol (SCS-B) Moderasyon Analizi
    PDF Tablo 17-21'e dayanmaktadır
    """
    
    def __init__(self):
        self.model_results = {
            'substance_duration': {'beta': 0.48, 'se': 0.07, 'ci': (0.34, 0.62), 'p': '<0.001'},
            'scsb_score': {'beta': -0.22, 'se': 0.06, 'ci': (-0.34, -0.10), 'p': '<0.001'},
            'interaction': {'beta': -0.26, 'se': 0.08, 'ci': (-0.42, -0.10), 'p': 0.002},
            'model_r2': 0.61,
            'interaction_delta_r2': 0.05,
            'f_statistic': 18.7
        }
        
        self.simple_slopes = {
            'low_scsb': {
                'level': 'Düşük Öz-Kontrol (-1 SD)',
                'beta': 0.74,
                'se': 0.08,
                'ci': (0.58, 0.90),
                'p': '<0.001',
                'interpretation': 'Zayıf öz-kontrol'
            },
            'mean_scsb': {
                'level': 'Ortalama Öz-Kontrol',
                'beta': 0.48,
                'se': 0.07,
                'ci': (0.34, 0.62),
                'p': '<0.001',
                'interpretation': 'Orta öz-kontrol'
            },
            'high_scsb': {
                'level': 'Yüksek Öz-Kontrol (+1 SD)',
                'beta': 0.22,
                'se': 0.07,
                'ci': (0.08, 0.36),
                'p': 0.003,
                'interpretation': 'İyi öz-kontrol'
            }
        }
        
        self.categorical_analysis = [
            {
                'category': 'Düşük (SCS-B<30)',
                'n': 342,
                'eaa': 5.7,
                'eaa_ci': (4.9, 6.6),
                'reference': True,
                'difference': None,
                't_stat': None,
                'p': None
            },
            {
                'category': 'Orta (SCS-B 30-40)',
                'n': 518,
                'eaa': 3.4,
                'eaa_ci': (2.8, 4.1),
                'reference': False,
                'difference': -2.3,
                't_stat': 4.2,
                'p': '<0.001'
            },
            {
                'category': 'Yüksek (SCS-B>40)',
                'n': 429,
                'eaa': 1.9,
                'eaa_ci': (1.3, 2.6),
                'reference': False,
                'difference': -3.8,
                't_stat': 7.8,
                'p': '<0.001'
            }
        ]
        
        self.moderated_mediation = {
            'low_scsb': {'n': 987, 'indirect_effect': 0.34, 'ci': (0.26, 0.43), 'p': '<0.001'},
            'mean_scsb': {'n': 987, 'indirect_effect': 0.21, 'ci': (0.16, 0.27), 'p': '<0.001'},
            'high_scsb': {'n': 987, 'indirect_effect': 0.09, 'ci': (0.03, 0.16), 'p': 0.008}
        }
        
        self.path_a_moderation = {
            'low_control': {'beta': 0.68, 'p': '<0.001'},
            'high_control': {'beta': 0.28, 'p': 0.004},
            'interaction': {'beta': -0.29, 'p': 0.002}
        }
    
    def get_model_summary(self) -> pd.DataFrame:
        """Model özet tablosu"""
        data = [
            {
                'Model Terimi': 'Madde Kullanım Süresi',
                'β': self.model_results['substance_duration']['beta'],
                'SE': self.model_results['substance_duration']['se'],
                '95% GA': f"{self.model_results['substance_duration']['ci']}",
                'p-değeri': self.model_results['substance_duration']['p']
            },
            {
                'Model Terimi': 'SCS-B Skoru',
                'β': self.model_results['scsb_score']['beta'],
                'SE': self.model_results['scsb_score']['se'],
                '95% GA': f"{self.model_results['scsb_score']['ci']}",
                'p-değeri': self.model_results['scsb_score']['p']
            },
            {
                'Model Terimi': 'Madde × SCS-B Etkileşimi',
                'β': self.model_results['interaction']['beta'],
                'SE': self.model_results['interaction']['se'],
                '95% GA': f"{self.model_results['interaction']['ci']}",
                'p-değeri': self.model_results['interaction']['p']
            },
            {
                'Model Terimi': 'Model R²',
                'β': self.model_results['model_r2'],
                'SE': '-',
                '95% GA': '-',
                'p-değeri': '-'
            }
        ]
        return pd.DataFrame(data)
    
    def get_simple_slopes_table(self) -> pd.DataFrame:
        """Simple slopes analizi tablosu"""
        data = []
        for level, info in self.simple_slopes.items():
            data.append({
                'SCS-B Seviyesi': info['level'],
                'β': info['beta'],
                'SE': info['se'],
                '95% GA': f"{info['ci']}",
                'p-değeri': info['p'],
                'Yorum': info['interpretation']
            })
        return pd.DataFrame(data)
    
    def get_categorical_table(self) -> pd.DataFrame:
        """Kategorik SCS-B analizi tablosu"""
        data = []
        for cat in self.categorical_analysis:
            data.append({
                'SCS-B Kategorisi': cat['category'],
                'n': cat['n'],
                'EAA (yıl)': cat['eaa'],
                '95% GA': f"{cat['eaa_ci']}",
                'Düşük Öz-Kontrole Göre Fark (yıl)': cat['difference'] if cat['difference'] else 'Referans',
                't-istatistiği': cat['t_stat'] if cat['t_stat'] else '-',
                'p-değeri': cat['p'] if cat['p'] else '-'
            })
        return pd.DataFrame(data)
    
    def get_moderated_mediation_table(self) -> pd.DataFrame:
        """Moderated mediation analizi tablosu"""
        data = []
        level_names = {
            'low_scsb': 'Düşük (-1 SD)',
            'mean_scsb': 'Ortalama',
            'high_scsb': 'Yüksek (+1 SD)'
        }
        for level, info in self.moderated_mediation.items():
            data.append({
                'Öz-Kontrol Seviyesi': level_names[level],
                'n': info['n'],
                'İndirekt Etki β': info['indirect_effect'],
                '95% GA': f"{info['ci']}",
                'p-değeri': info['p']
            })
        return pd.DataFrame(data)
    
    def calculate_protective_effect(self) -> Dict:
        """Öz-kontrolün koruyucu etkisini hesapla"""
        low_eaa = 5.7
        high_eaa = 1.9
        reduction = low_eaa - high_eaa
        percent_reduction = (reduction / low_eaa) * 100
        
        return {
            'low_control_eaa': low_eaa,
            'high_control_eaa': high_eaa,
            'absolute_reduction': reduction,
            'percent_reduction': round(percent_reduction, 1),
            'interpretation': f'Yüksek öz-kontrol, EAA\'yı %{round(percent_reduction)}  azaltmaktadır'
        }


class ReversibilityAnalysis:
    """
    Epigenetik Yaş İvmelenmesinin Tersine Çevrilebilirliği
    PDF Bölüm 3.10 ve 4.6'ya dayanmaktadır
    """
    
    def __init__(self):
        self.intervention_studies = [
            {
                'intervention': 'Metilasyon-destekleyici diyet',
                'authors': 'Fitzgerald ve ark. (2021)',
                'n': 43,
                'duration': '8 hafta',
                'eaa_change': -3.23,
                'ci': (-4.1, -2.4),
                'p': '<0.001'
            },
            {
                'intervention': 'Yoğun egzersiz programı',
                'authors': 'Quach ve ark. (2017)',
                'n': 78,
                'duration': '12 hafta',
                'eaa_change': -2.87,
                'ci': (-3.6, -2.1),
                'p': '<0.001'
            },
            {
                'intervention': 'Mindfulness ve yoga',
                'authors': 'Epel ve ark. (2016)',
                'n': 96,
                'duration': '12 hafta',
                'eaa_change': -1.96,
                'ci': (-2.7, -1.2),
                'p': '<0.001'
            },
            {
                'intervention': 'Kombine müdahale (diyet + egzersiz + stress)',
                'authors': 'Fitzgerald ve ark. (2021)',
                'n': 43,
                'duration': '8 hafta',
                'eaa_change': -4.60,
                'ci': (-5.8, -3.4),
                'p': '<0.001'
            }
        ]
        
        self.cessation_effects = [
            {
                'timepoint': '1 yıl sonra',
                'n': 124,
                'eaa_change': -1.52,
                'ci': (-2.3, -0.7),
                'p': 0.002,
                'source': 'Ambatipudi ve ark. (2016)'
            },
            {
                'timepoint': '5 yıl sonra',
                'n': 89,
                'eaa_change': -3.18,
                'ci': (-4.2, -2.1),
                'p': '<0.001',
                'source': 'Ambatipudi ve ark. (2016)'
            }
        ]
        
        self.meta_analysis = {
            'n_studies': 6,
            'total_n': 473,
            'mean_change': -2.73,
            'ci': (-3.4, -2.1),
            'p': '<0.001',
            'heterogeneity_i2': 68,
            'heterogeneity_p': 0.008,
            'heterogeneity_level': 'Orta düzey'
        }
    
    def get_intervention_table(self) -> pd.DataFrame:
        """Müdahale çalışmaları tablosu"""
        data = []
        for study in self.intervention_studies:
            data.append({
                'Müdahale': study['intervention'],
                'Kaynak': study['authors'],
                'n': study['n'],
                'Süre': study['duration'],
                'EAA Değişimi (yıl)': study['eaa_change'],
                '95% GA': f"{study['ci']}",
                'p-değeri': study['p']
            })
        return pd.DataFrame(data)
    
    def get_cessation_table(self) -> pd.DataFrame:
        """Madde bırakma etkileri tablosu"""
        data = []
        for effect in self.cessation_effects:
            data.append({
                'Zaman Noktası': effect['timepoint'],
                'n': effect['n'],
                'EAA Değişimi (yıl)': effect['eaa_change'],
                '95% GA': f"{effect['ci']}",
                'p-değeri': effect['p'],
                'Kaynak': effect['source']
            })
        return pd.DataFrame(data)
    
    def get_meta_analysis_summary(self) -> Dict:
        """Meta-analiz özeti"""
        return self.meta_analysis
    
    def calculate_recovery_trajectory(
        self, 
        initial_eaa: float, 
        months_abstinent: int
    ) -> float:
        """
        Tahmini EAA iyileşme eğrisi
        """
        annual_recovery = 1.5
        monthly_recovery = annual_recovery / 12
        
        max_recovery = initial_eaa * 0.7
        
        recovery = min(monthly_recovery * months_abstinent, max_recovery)
        
        return initial_eaa - recovery
    
    def get_clinical_recommendations(self) -> List[Dict]:
        """Klinik öneriler"""
        return [
            {
                'recommendation': 'Metilasyon-destekleyici diyet',
                'components': 'Folat, B12, betain, kolin zengin gıdalar',
                'expected_effect': '-3.2 yıl (8 hafta)',
                'evidence_level': 'RCT'
            },
            {
                'recommendation': 'Düzenli egzersiz',
                'components': 'Haftada ≥3 kez, orta-yoğun aerobik',
                'expected_effect': '-2.9 yıl (12 hafta)',
                'evidence_level': 'RCT'
            },
            {
                'recommendation': 'Stress yönetimi',
                'components': 'Mindfulness, yoga, meditasyon',
                'expected_effect': '-2.0 yıl (12 hafta)',
                'evidence_level': 'RCT'
            },
            {
                'recommendation': 'Madde kullanımını bırakma',
                'components': 'Tam cessation',
                'expected_effect': '-1.5 yıl (1 yıl), -3.2 yıl (5 yıl)',
                'evidence_level': 'Kohort'
            }
        ]


class ClinicalCovariates:
    """
    Klinik ve Demografik Kovaryatlar
    PDF Tablo 26-32'ye dayanmaktadır
    """
    
    def __init__(self):
        self.onset_age_analysis = [
            {'category': '<30 yaş', 'n': 1247, 'eaa': 4.8, 'ci': (4.1, 5.6)},
            {'category': '30-50 yaş', 'n': 2834, 'eaa': 3.2, 'ci': (2.8, 3.7)},
            {'category': '>50 yaş', 'n': 1454, 'eaa': 2.1, 'ci': (1.6, 2.7)}
        ]
        
        self.sex_effects = {
            'alcohol': {'male': 2.6, 'male_ci': (2.1, 3.2), 'female': 3.2, 'female_ci': (2.6, 3.9), 'diff': 0.6, 't': 2.1, 'p': 0.042},
            'cocaine': {'male': 3.4, 'male_ci': (2.8, 4.1), 'female': 2.8, 'female_ci': (2.1, 3.6), 'diff': -0.6, 't': 1.3, 'p': 0.18},
            'opioid': {'male': 2.3, 'male_ci': (1.8, 2.9), 'female': 2.6, 'female_ci': (2.0, 3.3), 'diff': 0.3, 't': 0.7, 'p': 0.51},
            'methamphetamine': {'male': 5.1, 'male_ci': (3.4, 7.0), 'female': 3.8, 'female_ci': (1.9, 6.1), 'diff': -1.3, 't': 1.0, 'p': 0.31}
        }
        
        self.education_effects = [
            {'level': '<Lise', 'n': 1876, 'eaa': 4.7, 'ci': (4.1, 5.4)},
            {'level': 'Lise', 'n': 2143, 'eaa': 3.4, 'ci': (2.9, 4.0)},
            {'level': 'Üniversite', 'n': 1516, 'eaa': 2.1, 'ci': (1.6, 2.7)}
        ]
        
        self.bmi_effects = [
            {'category': 'Normal', 'range': '18.5-25', 'n': 2347, 'eaa': 2.8, 'ci': (2.3, 3.4)},
            {'category': 'Fazla Kilolu', 'range': '25-30', 'n': 1892, 'eaa': 3.6, 'ci': (3.1, 4.2)},
            {'category': 'Obez', 'range': '>30', 'n': 1296, 'eaa': 5.1, 'ci': (4.4, 5.9)}
        ]
        
        self.exercise_effects = [
            {'frequency': 'Düzenli (≥3×/hafta)', 'n': 1124, 'eaa': 2.1, 'ci': (1.6, 2.7)},
            {'frequency': 'Ara Sıra (1-2×/hafta)', 'n': 1687, 'eaa': 3.4, 'ci': (2.9, 4.0)},
            {'frequency': 'Hiç Yok', 'n': 2724, 'eaa': 4.9, 'ci': (4.3, 5.6)}
        ]
        
        self.hierarchical_regression = {
            'model1': {'variables': 'Yaş + Cinsiyet', 'r2': 0.12, 'delta_r2': None, 'f': None, 'p': None},
            'model2': {'variables': '+ Madde kullanım süresi', 'r2': 0.30, 'delta_r2': 0.18, 'f': 287.4, 'p': '<0.001'},
            'model3': {'variables': '+ Fizyolojik mediyatörler', 'r2': 0.37, 'delta_r2': 0.07, 'f': 94.3, 'p': '<0.001'},
            'model4': {'variables': '+ Psikolojik moderatörler', 'r2': 0.42, 'delta_r2': 0.05, 'f': 67.8, 'p': '<0.001'}
        }
        
        self.final_model_contributions = [
            {'variable': 'Madde Kullanım Süresi', 'beta': 0.42, 'se': 0.03, 'ci': (0.36, 0.48), 'p': '<0.001', 'ind_r2': 0.18},
            {'variable': 'BMI', 'beta': 0.21, 'se': 0.03, 'ci': (0.15, 0.27), 'p': '<0.001', 'ind_r2': 0.04},
            {'variable': 'Eğitim Seviyesi', 'beta': -0.18, 'se': 0.03, 'ci': (-0.24, -0.12), 'p': '<0.001', 'ind_r2': 0.03},
            {'variable': 'Egzersiz Sıklığı', 'beta': -0.15, 'se': 0.03, 'ci': (-0.21, -0.09), 'p': '<0.001', 'ind_r2': 0.02},
            {'variable': 'DERS Skoru', 'beta': 0.24, 'se': 0.03, 'ci': (0.18, 0.30), 'p': '<0.001', 'ind_r2': 0.06},
            {'variable': 'İnsülin Direnci (HOMA-IR)', 'beta': 0.19, 'se': 0.03, 'ci': (0.13, 0.25), 'p': '<0.001', 'ind_r2': 0.04},
            {'variable': 'İnflamasyon Skoru', 'beta': 0.22, 'se': 0.03, 'ci': (0.16, 0.28), 'p': '<0.001', 'ind_r2': 0.05}
        ]
    
    def get_onset_age_table(self) -> pd.DataFrame:
        """Başlangıç yaşı analizi tablosu"""
        data = []
        for cat in self.onset_age_analysis:
            data.append({
                'Başlangıç Yaş Kategorisi': cat['category'],
                'n': cat['n'],
                'EAA (yıl)': cat['eaa'],
                '95% GA': f"{cat['ci']}"
            })
        return pd.DataFrame(data)
    
    def get_sex_effects_table(self) -> pd.DataFrame:
        """Cinsiyet etkileri tablosu"""
        data = []
        for substance, effects in self.sex_effects.items():
            data.append({
                'Madde Türü': substance.title(),
                'Erkek EAA (yıl)': effects['male'],
                'Erkek 95% GA': f"{effects['male_ci']}",
                'Kadın EAA (yıl)': effects['female'],
                'Kadın 95% GA': f"{effects['female_ci']}",
                'Fark (yıl)': effects['diff'],
                't-istatistiği': effects['t'],
                'p-değeri': effects['p']
            })
        return pd.DataFrame(data)
    
    def get_education_table(self) -> pd.DataFrame:
        """Eğitim seviyesi analizi tablosu"""
        data = []
        for edu in self.education_effects:
            data.append({
                'Eğitim Seviyesi': edu['level'],
                'n': edu['n'],
                'EAA (yıl)': edu['eaa'],
                '95% GA': f"{edu['ci']}"
            })
        return pd.DataFrame(data)
    
    def get_bmi_table(self) -> pd.DataFrame:
        """BMI analizi tablosu"""
        data = []
        for bmi in self.bmi_effects:
            data.append({
                'BMI Kategorisi': bmi['category'],
                'BMI Aralığı': bmi['range'],
                'n': bmi['n'],
                'EAA (yıl)': bmi['eaa'],
                '95% GA': f"{bmi['ci']}"
            })
        return pd.DataFrame(data)
    
    def get_exercise_table(self) -> pd.DataFrame:
        """Egzersiz sıklığı analizi tablosu"""
        data = []
        for ex in self.exercise_effects:
            data.append({
                'Egzersiz Sıklığı': ex['frequency'],
                'n': ex['n'],
                'EAA (yıl)': ex['eaa'],
                '95% GA': f"{ex['ci']}"
            })
        return pd.DataFrame(data)
    
    def get_hierarchical_regression_table(self) -> pd.DataFrame:
        """Hiyerarşik regresyon tablosu"""
        data = []
        for model, info in self.hierarchical_regression.items():
            data.append({
                'Model': model.upper(),
                'Eklenen Değişkenler': info['variables'],
                'R²': info['r2'],
                'ΔR²': info['delta_r2'] if info['delta_r2'] else '-',
                'F-istatistiği': info['f'] if info['f'] else '-',
                'p-değeri': info['p'] if info['p'] else '-'
            })
        return pd.DataFrame(data)
    
    def get_final_model_table(self) -> pd.DataFrame:
        """Final model değişken katkıları tablosu"""
        data = []
        for var in self.final_model_contributions:
            data.append({
                'Değişken': var['variable'],
                'β (standardize)': var['beta'],
                'SE': var['se'],
                '95% GA': f"{var['ci']}",
                'p-değeri': var['p'],
                'Bağımsız R²': var['ind_r2']
            })
        return pd.DataFrame(data)
