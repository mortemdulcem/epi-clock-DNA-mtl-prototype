# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Clinical Decision Support System for EpiClock Prototype
Risk stratification and treatment recommendations based on EAA scores
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@dataclass
# nrcdnl94
class RiskAssessment:
    # nrcdnl94
    """Comprehensive risk assessment result"""
    patient_id: str
    assessment_date: datetime
    risk_category: str
    risk_score: float
    risk_percentile: float
    
    eaa_contribution: float
    substance_contribution: float
    clinical_contribution: float
    lifestyle_contribution: float
    
    primary_concerns: List[str]
    protective_factors: List[str]
    
    interpretation: str


@dataclass
# nrcdnl94
class TreatmentRecommendation:
    # nrcdnl94
    """Treatment recommendation with evidence"""
    recommendation_id: str
    priority: str
    category: str
    title: str
    description: str
    expected_eaa_reduction: float
    evidence_level: str
    time_to_effect: str
    target_pathways: List[str]
    monitoring_metrics: List[str]


@dataclass 
# nrcdnl94
class InterventionPlan:
    # nrcdnl94
    """Comprehensive intervention plan"""
    patient_id: str
    creation_date: datetime
    risk_assessment: RiskAssessment
    recommendations: List[TreatmentRecommendation]
    timeline: Dict[str, List[str]]
    monitoring_schedule: List[Dict]
    expected_outcomes: Dict[str, float]


class ClinicalDecisionSupport:
    # nrcdnl94
    """
    Clinical decision support system for epigenetic age management.
    Provides risk stratification, treatment recommendations, and monitoring guidance.
    """
    
    RISK_THRESHOLDS = {
        'low': {'min': -10, 'max': 2},
        'moderate': {'min': 2, 'max': 5},
        'high': {'min': 5, 'max': 8},
        'very_high': {'min': 8, 'max': 20}
    }
    
    SUBSTANCE_RISK_MULTIPLIERS = {
        'control': 1.0,
        'cannabis': 1.1,
        'alcohol': 1.4,
        'opioids': 1.5,
        'cocaine': 1.6,
        'methamphetamine': 1.8,
        'polysubstance': 2.0
    }
    
    CLINICAL_RISK_FACTORS = {
        'high_crp': {'threshold': 3.0, 'weight': 0.15, 'name': 'Yüksek CRP (Sistemik İnflamasyon)'},
        'high_homa_ir': {'threshold': 2.5, 'weight': 0.12, 'name': 'İnsülin Direnci'},
        'low_albumin': {'threshold': 3.5, 'weight': 0.10, 'name': 'Düşük Albümin'},
        'high_creatinine': {'threshold': 1.3, 'weight': 0.08, 'name': 'Yüksek Kreatinin'},
        'high_glucose': {'threshold': 126, 'weight': 0.10, 'name': 'Yüksek Açlık Glukozu'},
        'smoking': {'threshold': 10, 'weight': 0.15, 'name': 'Sigara Kullanımı (>10 paket-yıl)'}
    }
    
    TREATMENT_DATABASE = {
        'lifestyle_exercise': TreatmentRecommendation(
            recommendation_id='REC001',
            priority='high',
            category='lifestyle',
            title='Düzenli Aerobik Egzersiz Programı',
            description='Haftada en az 150 dakika orta yoğunlukta veya 75 dakika yüksek yoğunlukta aerobik egzersiz. '
                       'Yürüyüş, koşu, yüzme veya bisiklet önerilir.',
            expected_eaa_reduction=1.5,
            evidence_level='A',
            time_to_effect='3-6 ay',
            target_pathways=['SIRT1', 'AMPK', 'PGC1A', 'Telomer stabilizasyonu'],
            monitoring_metrics=['VO2max', 'Kalp hızı değişkenliği', 'BMI']
        ),
        'lifestyle_nutrition': TreatmentRecommendation(
            recommendation_id='REC002',
            priority='high',
            category='lifestyle',
            title='Anti-İnflamatuar Beslenme Planı',
            description='Akdeniz diyeti veya DASH diyeti prensiplerine uygun beslenme. '
                       'Omega-3 açısından zengin gıdalar, antioksidanlar ve lifli gıdalar.',
            expected_eaa_reduction=1.0,
            evidence_level='A',
            time_to_effect='3-6 ay',
            target_pathways=['NRF2', 'NFkB inhibisyonu', 'İnsülin duyarlılığı'],
            monitoring_metrics=['CRP', 'HbA1c', 'Lipid profili']
        ),
        'lifestyle_sleep': TreatmentRecommendation(
            recommendation_id='REC003',
            priority='moderate',
            category='lifestyle',
            title='Uyku Kalitesi Optimizasyonu',
            description='7-9 saat kaliteli uyku hedeflenmeli. Uyku hijyeni prensipleri, '
                       'düzenli uyku saatleri ve karanlık oda ortamı önerilir.',
            expected_eaa_reduction=0.8,
            evidence_level='B',
            time_to_effect='1-3 ay',
            target_pathways=['Kortizol regülasyonu', 'GH sekresyonu', 'Hücre onarımı'],
            monitoring_metrics=['Uyku süresi', 'Uyku kalitesi skoru', 'Kortizol düzeyi']
        ),
        'lifestyle_stress': TreatmentRecommendation(
            recommendation_id='REC004',
            priority='moderate',
            category='lifestyle',
            title='Stres Yönetimi ve Mindfulness',
            description='Günlük meditasyon veya mindfulness pratiği (15-30 dakika). '
                       'Derin nefes egzersizleri ve progresif kas gevşetme teknikleri.',
            expected_eaa_reduction=0.6,
            evidence_level='B',
            time_to_effect='2-4 ay',
            target_pathways=['HPA eksen regulasyonu', 'Telomeraz aktivitesi', 'İnflamasyon azaltma'],
            monitoring_metrics=['Kortizol/DHEA oranı', 'Kalp hızı değişkenliği', 'Subjektif stres skoru']
        ),
        'substance_treatment': TreatmentRecommendation(
            recommendation_id='REC005',
            priority='very_high',
            category='substance_treatment',
            title='Madde Bağımlılığı Tedavi Programı',
            description='Kanıta dayalı bağımlılık tedavisi: Bilişsel davranışçı terapi, '
                       'motivasyonel görüşme, gerekirse farmakoterapi (naltrexone, buprenorfin vb).',
            expected_eaa_reduction=2.5,
            evidence_level='A',
            time_to_effect='6-12 ay',
            target_pathways=['Dopamin sistemi', 'Stres yanıtı', 'Nöroinflamasyon'],
            monitoring_metrics=['Madde kullanım günleri', 'Aşerme skoru', 'EAA takibi']
        ),
        'medical_metformin': TreatmentRecommendation(
            recommendation_id='REC006',
            priority='moderate',
            category='pharmacological',
            title='Metformin Tedavisi (Endike İse)',
            description='Prediabet veya metabolik sendrom varlığında metformin başlanması düşünülebilir. '
                       'AMPK aktivasyonu ve yaşlanma karşıtı etkileri bildirilmiştir.',
            expected_eaa_reduction=1.2,
            evidence_level='B',
            time_to_effect='6-12 ay',
            target_pathways=['AMPK aktivasyonu', 'mTOR inhibisyonu', 'İnsülin duyarlılığı'],
            monitoring_metrics=['HbA1c', 'HOMA-IR', 'Vitamin B12']
        ),
        'supplement_omega3': TreatmentRecommendation(
            recommendation_id='REC007',
            priority='low',
            category='supplement',
            title='Omega-3 Yağ Asidi Takviyesi',
            description='Günlük 2-4 gram EPA/DHA kombinasyonu. '
                       'Anti-inflamatuar etki ve telomer koruması için önerilir.',
            expected_eaa_reduction=0.5,
            evidence_level='B',
            time_to_effect='3-6 ay',
            target_pathways=['İnflamasyon', 'Membran akışkanlığı', 'Telomer stabilizasyonu'],
            monitoring_metrics=['Omega-3 indeksi', 'CRP', 'Trigliseritler']
        ),
        'supplement_nad': TreatmentRecommendation(
            recommendation_id='REC008',
            priority='low',
            category='supplement',
            title='NAD+ Prekürsör Takviyesi (NMN/NR)',
            description='Nikotinamid mononükleotid (NMN) veya nikotinamid ribozit (NR) takviyesi. '
                       'Hücresel enerji metabolizması ve sirtuinlerin aktivasyonu için.',
            expected_eaa_reduction=0.4,
            evidence_level='C',
            time_to_effect='3-6 ay',
            target_pathways=['Sirtuin aktivasyonu', 'NAD+ havuzu', 'Mitokondri fonksiyonu'],
            monitoring_metrics=['Enerji düzeyi', 'Kognitif fonksiyon', 'Fiziksel performans']
        ),
        'medical_inflammation': TreatmentRecommendation(
            recommendation_id='REC009',
            priority='high',
            category='medical',
            title='Kronik İnflamasyon Tedavisi',
            description='Altta yatan kronik inflamatuar durumların tedavisi. '
                       'Otoimmün hastalıklar, kronik enfeksiyonlar veya diğer inflamatuar durumlar.',
            expected_eaa_reduction=1.8,
            evidence_level='A',
            time_to_effect='3-6 ay',
            target_pathways=['NFkB', 'İnflamazom', 'Sitokin üretimi'],
            monitoring_metrics=['CRP', 'IL-6', 'TNF-alpha', 'ESR']
        ),
        'psychological_support': TreatmentRecommendation(
            recommendation_id='REC010',
            priority='moderate',
            category='psychological',
            title='Psikolojik Destek ve Terapi',
            description='Düzenli psikoterapi seansları: CBT, ACT veya diğer kanıta dayalı yaklaşımlar. '
                       'Duygu düzenleme ve öz-bakım becerilerinin geliştirilmesi.',
            expected_eaa_reduction=0.7,
            evidence_level='B',
            time_to_effect='3-6 ay',
            target_pathways=['Stres yanıtı', 'Duygu düzenleme', 'Sosyal destek'],
            monitoring_metrics=['DERS skoru', 'Depresyon/anksiyete skorları', 'Yaşam kalitesi']
        )
    }
    
    def __init__(self):
        pass
    
    def calculate_risk_score(self,
                              eaa_values: Dict[str, float],
                              substance_type: str = 'control',
                              clinical_data: Dict = None,
                              lifestyle_data: Dict = None) -> RiskAssessment:
        """
        Calculate comprehensive risk score based on multiple factors.
        
        Args:
            eaa_values: Dictionary of EAA values from different clocks
            substance_type: Type of substance use
            clinical_data: Clinical biomarker data
            lifestyle_data: Lifestyle factors
        
        Returns:
            RiskAssessment with detailed risk analysis
        """
        grimage_eaa = eaa_values.get('grimage_eaa', 0)
        phenoage_eaa = eaa_values.get('phenoage_eaa', 0)
        horvath_eaa = eaa_values.get('horvath_eaa', 0)
        
        eaa_score = (grimage_eaa * 0.4 + phenoage_eaa * 0.35 + horvath_eaa * 0.25)
        
        substance_multiplier = self.SUBSTANCE_RISK_MULTIPLIERS.get(substance_type, 1.0)
        
        clinical_score = 0.0
        clinical_concerns = []
        clinical_protective = []
        
        if clinical_data:
            if clinical_data.get('crp', 0) > self.CLINICAL_RISK_FACTORS['high_crp']['threshold']:
                clinical_score += self.CLINICAL_RISK_FACTORS['high_crp']['weight'] * 10
                clinical_concerns.append(self.CLINICAL_RISK_FACTORS['high_crp']['name'])
            else:
                clinical_protective.append('Normal CRP düzeyi')
            
            if clinical_data.get('homa_ir', 0) > self.CLINICAL_RISK_FACTORS['high_homa_ir']['threshold']:
                clinical_score += self.CLINICAL_RISK_FACTORS['high_homa_ir']['weight'] * 10
                clinical_concerns.append(self.CLINICAL_RISK_FACTORS['high_homa_ir']['name'])
            
            if clinical_data.get('albumin', 5) < self.CLINICAL_RISK_FACTORS['low_albumin']['threshold']:
                clinical_score += self.CLINICAL_RISK_FACTORS['low_albumin']['weight'] * 10
                clinical_concerns.append(self.CLINICAL_RISK_FACTORS['low_albumin']['name'])
            
            if clinical_data.get('glucose', 0) > self.CLINICAL_RISK_FACTORS['high_glucose']['threshold']:
                clinical_score += self.CLINICAL_RISK_FACTORS['high_glucose']['weight'] * 10
                clinical_concerns.append(self.CLINICAL_RISK_FACTORS['high_glucose']['name'])
        
        lifestyle_score = 0.0
        
        if lifestyle_data:
            if lifestyle_data.get('smoking_pack_years', 0) > 10:
                lifestyle_score += 1.5
                clinical_concerns.append('Sigara kullanımı')
            
            if lifestyle_data.get('bmi', 25) > 30:
                lifestyle_score += 1.0
                clinical_concerns.append('Obezite (BMI > 30)')
            elif lifestyle_data.get('bmi', 25) < 18.5:
                lifestyle_score += 0.5
                clinical_concerns.append('Düşük BMI')
            
            if lifestyle_data.get('exercise_minutes_week', 0) >= 150:
                lifestyle_score -= 0.5
                clinical_protective.append('Düzenli egzersiz')
            
            if lifestyle_data.get('sleep_hours', 7) >= 7:
                clinical_protective.append('Yeterli uyku')
        
        total_risk = (eaa_score + clinical_score + lifestyle_score) * substance_multiplier
        
        if total_risk < 2:
            risk_category = 'low'
        elif total_risk < 5:
            risk_category = 'moderate'
        elif total_risk < 8:
            risk_category = 'high'
        else:
            risk_category = 'very_high'
        
        from scipy import stats
        risk_percentile = stats.norm.cdf(total_risk, loc=3, scale=2.5) * 100
        
        interpretation = self._generate_risk_interpretation(
            risk_category, total_risk, substance_type, clinical_concerns
        )
        
        return RiskAssessment(
            patient_id='',
            assessment_date=datetime.now(),
            risk_category=risk_category,
            risk_score=round(total_risk, 2),
            risk_percentile=round(risk_percentile, 1),
            eaa_contribution=round(eaa_score, 2),
            substance_contribution=round((substance_multiplier - 1) * eaa_score, 2),
            clinical_contribution=round(clinical_score, 2),
            lifestyle_contribution=round(lifestyle_score, 2),
            primary_concerns=clinical_concerns,
            protective_factors=clinical_protective,
            interpretation=interpretation
        )
    
    def _generate_risk_interpretation(self, 
                                       risk_category: str,
                                       risk_score: float,
                                       substance_type: str,
                                       concerns: List[str]) -> str:
        """Generate clinical interpretation of risk assessment"""
        
        category_texts = {
            'low': 'Düşük risk kategorisinde yer almaktadır. Koruyucu faktörler etkin görünmektedir.',
            'moderate': 'Orta risk kategorisinde yer almaktadır. Yaşam tarzı müdahaleleri önerilir.',
            'high': 'Yüksek risk kategorisinde yer almaktadır. Kapsamlı müdahale planı gereklidir.',
            'very_high': 'Çok yüksek risk kategorisinde yer almaktadır. Acil ve yoğun müdahale gereklidir.'
        }
        
        interpretation = f"Hasta, epigenetik yaş ivmelenmesi açısından {category_texts.get(risk_category, '')} "
        interpretation += f"(Risk skoru: {risk_score:.1f}). "
        
        if substance_type != 'control':
            substance_names = {
                'alcohol': 'Alkol kullanım bozukluğu',
                'cocaine': 'Kokain kullanımı',
                'opioids': 'Opioid kullanımı',
                'methamphetamine': 'Metamfetamin kullanımı',
                'cannabis': 'Kannabis kullanımı',
                'polysubstance': 'Çoklu madde kullanımı'
            }
            interpretation += f"{substance_names.get(substance_type, substance_type)} nedeniyle risk artmaktadır. "
        
        if concerns:
            interpretation += f"Ek risk faktörleri: {', '.join(concerns[:3])}. "
        
        return interpretation
    
    def generate_recommendations(self,
                                  risk_assessment: RiskAssessment,
                                  substance_type: str = 'control') -> List[TreatmentRecommendation]:
        """
        Generate personalized treatment recommendations based on risk assessment.
        
        Args:
            risk_assessment: Risk assessment result
            substance_type: Type of substance use
        
        Returns:
            List of prioritized treatment recommendations
        """
        recommendations = []
        
        if substance_type != 'control':
            recommendations.append(self.TREATMENT_DATABASE['substance_treatment'])
        
        if risk_assessment.risk_category in ['high', 'very_high']:
            recommendations.append(self.TREATMENT_DATABASE['lifestyle_exercise'])
            recommendations.append(self.TREATMENT_DATABASE['lifestyle_nutrition'])
            
            if 'Yüksek CRP' in ' '.join(risk_assessment.primary_concerns) or \
               'İnflamasyon' in ' '.join(risk_assessment.primary_concerns):
                recommendations.append(self.TREATMENT_DATABASE['medical_inflammation'])
        
        if risk_assessment.risk_category in ['moderate', 'high', 'very_high']:
            recommendations.append(self.TREATMENT_DATABASE['lifestyle_stress'])
            recommendations.append(self.TREATMENT_DATABASE['lifestyle_sleep'])
        
        if 'İnsülin Direnci' in ' '.join(risk_assessment.primary_concerns):
            recommendations.append(self.TREATMENT_DATABASE['medical_metformin'])
        
        if risk_assessment.risk_category != 'low':
            recommendations.append(self.TREATMENT_DATABASE['psychological_support'])
        
        if len(recommendations) < 5 and risk_assessment.risk_category != 'very_high':
            if self.TREATMENT_DATABASE['supplement_omega3'] not in recommendations:
                recommendations.append(self.TREATMENT_DATABASE['supplement_omega3'])
        
        priority_order = {'very_high': 0, 'high': 1, 'moderate': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x.priority, 4))
        
        return recommendations[:8]
    
    def create_intervention_plan(self,
                                  patient_id: str,
                                  risk_assessment: RiskAssessment,
                                  recommendations: List[TreatmentRecommendation]) -> InterventionPlan:
        """
        Create comprehensive intervention plan with timeline.
        
        Args:
            patient_id: Patient identifier
            risk_assessment: Risk assessment result
            recommendations: List of treatment recommendations
        
        Returns:
            InterventionPlan with timeline and monitoring schedule
        """
        timeline = {
            'immediate': [],
            'short_term': [],
            'medium_term': [],
            'long_term': []
        }
        
        for rec in recommendations:
            if rec.priority in ['very_high', 'high']:
                timeline['immediate'].append(rec.title)
            elif rec.priority == 'moderate':
                timeline['short_term'].append(rec.title)
            else:
                timeline['medium_term'].append(rec.title)
        
        timeline['long_term'].append('Düzenli EAA takibi (6-12 ayda bir)')
        timeline['long_term'].append('Yaşam tarzı değişikliklerinin sürdürülmesi')
        
        monitoring_schedule = [
            {'timepoint': '1 ay', 'assessments': ['Tedaviye uyum değerlendirmesi', 'Yan etki taraması']},
            {'timepoint': '3 ay', 'assessments': ['Klinik biyobelirteçler', 'Yaşam kalitesi ölçümü']},
            {'timepoint': '6 ay', 'assessments': ['Epigenetik yaş kontrolü', 'Kapsamlı değerlendirme']},
            {'timepoint': '12 ay', 'assessments': ['Yıllık epigenetik yaş analizi', 'Tedavi planı revizyonu']}
        ]
        
        total_expected_reduction = sum(rec.expected_eaa_reduction for rec in recommendations[:5])
        
        expected_outcomes = {
            'expected_eaa_reduction': round(total_expected_reduction * 0.7, 1),
            'minimum_eaa_reduction': round(total_expected_reduction * 0.3, 1),
            'maximum_eaa_reduction': round(total_expected_reduction, 1),
            'expected_risk_category_change': 'moderate' if risk_assessment.risk_category in ['high', 'very_high'] else 'low'
        }
        
        return InterventionPlan(
            patient_id=patient_id,
            creation_date=datetime.now(),
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            timeline=timeline,
            monitoring_schedule=monitoring_schedule,
            expected_outcomes=expected_outcomes
        )
    
    def plot_risk_dashboard(self, risk_assessment: RiskAssessment) -> go.Figure:
        """Create risk assessment dashboard visualization"""
        
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "indicator"}, {"type": "pie"}],
                   [{"type": "bar", "colspan": 2}, None]],
            subplot_titles=('Risk Skoru', 'Risk Bileşenleri', 'Risk Faktörleri'),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        risk_colors = {
            'low': 'green',
            'moderate': 'yellow',
            'high': 'orange',
            'very_high': 'red'
        }
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=risk_assessment.risk_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 15]},
                    'bar': {'color': risk_colors.get(risk_assessment.risk_category, 'gray')},
                    'steps': [
                        {'range': [0, 2], 'color': "lightgreen"},
                        {'range': [2, 5], 'color': "lightyellow"},
                        {'range': [5, 8], 'color': "lightsalmon"},
                        {'range': [8, 15], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': risk_assessment.risk_score
                    }
                },
                title={'text': f"<b>{risk_assessment.risk_category.upper()}</b>"}
            ),
            row=1, col=1
        )
        
        components = ['EAA', 'Madde', 'Klinik', 'Yaşam Tarzı']
        values = [
            max(0, risk_assessment.eaa_contribution),
            max(0, risk_assessment.substance_contribution),
            max(0, risk_assessment.clinical_contribution),
            max(0, abs(risk_assessment.lifestyle_contribution))
        ]
        
        fig.add_trace(
            go.Pie(
                labels=components,
                values=values,
                hole=0.4,
                marker_colors=['#1f77b4', '#ff7f0e', '#d62728', '#2ca02c']
            ),
            row=1, col=2
        )
        
        factors = risk_assessment.primary_concerns + ['Koruyucu: ' + p for p in risk_assessment.protective_factors]
        factor_values = [1] * len(risk_assessment.primary_concerns) + [-0.5] * len(risk_assessment.protective_factors)
        colors = ['red'] * len(risk_assessment.primary_concerns) + ['green'] * len(risk_assessment.protective_factors)
        
        if factors:
            fig.add_trace(
                go.Bar(
                    x=factor_values,
                    y=factors,
                    orientation='h',
                    marker_color=colors
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title=dict(text='Klinik Risk Değerlendirmesi Dashboard', x=0.5),
            template='plotly_white',
            height=700,
            showlegend=False
        )
        
        return fig
    
    def plot_recommendation_timeline(self, intervention_plan: InterventionPlan) -> go.Figure:
        """Create timeline visualization for intervention plan"""
        
        fig = go.Figure()
        
        phases = [
            ('Hemen', intervention_plan.timeline['immediate'], 0),
            ('1-3 Ay', intervention_plan.timeline['short_term'], 1),
            ('3-6 Ay', intervention_plan.timeline['medium_term'], 2),
            ('6+ Ay', intervention_plan.timeline['long_term'], 3)
        ]
        
        colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
        
        for phase_name, items, phase_idx in phases:
            for i, item in enumerate(items):
                fig.add_trace(go.Scatter(
                    x=[phase_idx],
                    y=[i],
                    mode='markers+text',
                    marker=dict(size=15, color=colors[phase_idx]),
                    text=[item[:30] + '...' if len(item) > 30 else item],
                    textposition='middle right',
                    name=phase_name,
                    showlegend=i == 0,
                    hovertemplate=f"<b>{phase_name}</b><br>{item}<extra></extra>"
                ))
        
        fig.update_layout(
            title=dict(text='Müdahale Planı Zaman Çizelgesi', x=0.5),
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3],
                ticktext=['Hemen', '1-3 Ay', '3-6 Ay', '6+ Ay'],
                title='Zaman Dilimi'
            ),
            yaxis=dict(visible=False),
            template='plotly_white',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def generate_clinical_report(self,
                                  patient_id: str,
                                  risk_assessment: RiskAssessment,
                                  intervention_plan: InterventionPlan) -> Dict:
        """Generate comprehensive clinical decision support report"""
        
        return {
            'patient_id': patient_id,
            'report_date': datetime.now().isoformat(),
            'risk_assessment': {
                'category': risk_assessment.risk_category,
                'score': risk_assessment.risk_score,
                'percentile': risk_assessment.risk_percentile,
                'interpretation': risk_assessment.interpretation
            },
            'risk_components': {
                'eaa_contribution': risk_assessment.eaa_contribution,
                'substance_contribution': risk_assessment.substance_contribution,
                'clinical_contribution': risk_assessment.clinical_contribution,
                'lifestyle_contribution': risk_assessment.lifestyle_contribution
            },
            'concerns': risk_assessment.primary_concerns,
            'protective_factors': risk_assessment.protective_factors,
            'recommendations': [
                {
                    'id': rec.recommendation_id,
                    'priority': rec.priority,
                    'title': rec.title,
                    'description': rec.description,
                    'expected_benefit': f"{rec.expected_eaa_reduction} yıl EAA azalması",
                    'evidence': rec.evidence_level,
                    'timeframe': rec.time_to_effect
                }
                for rec in intervention_plan.recommendations
            ],
            'timeline': intervention_plan.timeline,
            'monitoring': intervention_plan.monitoring_schedule,
            'expected_outcomes': intervention_plan.expected_outcomes,
            'disclaimer': "Bu rapor klinik karar destek aracı olarak hazırlanmıştır. "
                         "Tüm tedavi kararları yetkili sağlık profesyonelleri tarafından verilmelidir."
        }


# End of module - # nrcdnl94