# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
Longitudinal Analysis Module for EpiClock Prototype
Track epigenetic age changes over time for individual patients
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@dataclass
# nrcdnl94
class LongitudinalTrend:
    # nrcdnl94
    """Result of longitudinal trend analysis"""
    patient_id: str
    n_timepoints: int
    time_span_years: float
    
    eaa_slope: float
    eaa_intercept: float
    eaa_r_squared: float
    eaa_p_value: float
    
    annual_change: float
    trend_direction: str
    is_significant: bool
    
    first_eaa: float
    last_eaa: float
    total_change: float
    
    interpretation: str


@dataclass
# nrcdnl94
class InterventionEffect:
    # nrcdnl94
    """Analysis of intervention effect on EAA"""
    intervention_date: datetime
    pre_intervention_eaa: float
    post_intervention_eaa: float
    eaa_change: float
    percent_change: float
    is_improvement: bool
    effect_size: float
    interpretation: str


class LongitudinalAnalyzer:
    # nrcdnl94
    """
    Longitudinal analysis of epigenetic age changes over time.
    Tracks EAA progression, intervention effects, and recovery patterns.
    """
    
    TREND_THRESHOLDS = {
        'accelerating': 0.5,
        'stable': 0.2,
        'improving': -0.2
    }
    
    CLOCK_WEIGHTS = {
        'grimage_eaa': 0.35,
        'phenoage_eaa': 0.25,
        'horvath_eaa': 0.20,
        'hannum_eaa': 0.10,
        'dunedinpace': 0.10
    }
    
    def __init__(self):
        pass
    
    def calculate_composite_eaa(self, row: pd.Series) -> float:
        """Calculate weighted composite EAA from multiple clocks"""
        composite = 0.0
        total_weight = 0.0
        
        for clock, weight in self.CLOCK_WEIGHTS.items():
            if clock in row and pd.notna(row[clock]):
                if clock == 'dunedinpace':
                    composite += (row[clock] - 1.0) * 10 * weight
                else:
                    composite += row[clock] * weight
                total_weight += weight
        
        if total_weight > 0:
            return composite / total_weight
        return 0.0
    
    def analyze_trend(self, longitudinal_data: pd.DataFrame, 
                      patient_id: str,
                      eaa_column: str = 'grimage_eaa') -> LongitudinalTrend:
        """
        Analyze longitudinal trend in EAA for a patient.
        
        Args:
            longitudinal_data: DataFrame with analysis dates and EAA values
            patient_id: Patient identifier
            eaa_column: Column name for EAA values
        
        Returns:
            LongitudinalTrend with trend statistics
        """
        if len(longitudinal_data) < 2:
            return LongitudinalTrend(
                patient_id=patient_id,
                n_timepoints=len(longitudinal_data),
                time_span_years=0.0,
                eaa_slope=0.0,
                eaa_intercept=longitudinal_data[eaa_column].iloc[0] if len(longitudinal_data) > 0 else 0.0,
                eaa_r_squared=0.0,
                eaa_p_value=1.0,
                annual_change=0.0,
                trend_direction='insufficient_data',
                is_significant=False,
                first_eaa=longitudinal_data[eaa_column].iloc[0] if len(longitudinal_data) > 0 else 0.0,
                last_eaa=longitudinal_data[eaa_column].iloc[-1] if len(longitudinal_data) > 0 else 0.0,
                total_change=0.0,
                interpretation="Trend analizi için en az 2 zaman noktası gereklidir."
            )
        
        df = longitudinal_data.sort_values('analysis_date').copy()
        
        df['days_from_start'] = (df['analysis_date'] - df['analysis_date'].iloc[0]).dt.days
        df['years_from_start'] = df['days_from_start'] / 365.25
        
        time_span = df['years_from_start'].max()
        
        x = df['years_from_start'].values
        y = df[eaa_column].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        if slope > self.TREND_THRESHOLDS['accelerating']:
            trend_direction = 'accelerating'
            interpretation = f"Epigenetik yaş ivmelenmesi artış eğiliminde (yıllık +{slope:.2f} yıl). " \
                           "Bu, biyolojik yaşlanmanın hızlandığını göstermektedir."
        elif slope < self.TREND_THRESHOLDS['improving']:
            trend_direction = 'improving'
            interpretation = f"Epigenetik yaş ivmelenmesi azalış eğiliminde (yıllık {slope:.2f} yıl). " \
                           "Bu, biyolojik yaşlanmanın yavaşladığını göstermektedir."
        else:
            trend_direction = 'stable'
            interpretation = f"Epigenetik yaş ivmelenmesi stabil seyretmektedir (yıllık {slope:+.2f} yıl)."
        
        is_significant = p_value < 0.05
        
        if is_significant:
            interpretation += f" Bu değişim istatistiksel olarak anlamlıdır (p={p_value:.4f})."
        else:
            interpretation += f" Ancak bu değişim istatistiksel olarak anlamlı değildir (p={p_value:.4f})."
        
        return LongitudinalTrend(
            patient_id=patient_id,
            n_timepoints=len(df),
            time_span_years=round(time_span, 2),
            eaa_slope=round(slope, 4),
            eaa_intercept=round(intercept, 4),
            eaa_r_squared=round(r_value**2, 4),
            eaa_p_value=round(p_value, 6),
            annual_change=round(slope, 2),
            trend_direction=trend_direction,
            is_significant=is_significant,
            first_eaa=round(y[0], 2),
            last_eaa=round(y[-1], 2),
            total_change=round(y[-1] - y[0], 2),
            interpretation=interpretation
        )
    
    def analyze_intervention_effect(self, 
                                     longitudinal_data: pd.DataFrame,
                                     intervention_date: datetime,
                                     eaa_column: str = 'grimage_eaa',
                                     min_pre_points: int = 1,
                                     min_post_points: int = 1) -> Optional[InterventionEffect]:
        """
        Analyze the effect of an intervention on EAA.
        
        Args:
            longitudinal_data: DataFrame with analysis dates and EAA values
            intervention_date: Date of intervention
            eaa_column: Column name for EAA values
            min_pre_points: Minimum pre-intervention data points required
            min_post_points: Minimum post-intervention data points required
        
        Returns:
            InterventionEffect or None if insufficient data
        """
        df = longitudinal_data.sort_values('analysis_date').copy()
        
        pre_intervention = df[df['analysis_date'] < intervention_date]
        post_intervention = df[df['analysis_date'] >= intervention_date]
        
        if len(pre_intervention) < min_pre_points or len(post_intervention) < min_post_points:
            return None
        
        pre_eaa = pre_intervention[eaa_column].mean()
        post_eaa = post_intervention[eaa_column].mean()
        
        eaa_change = post_eaa - pre_eaa
        percent_change = (eaa_change / abs(pre_eaa)) * 100 if pre_eaa != 0 else 0
        
        is_improvement = eaa_change < 0
        
        pre_std = pre_intervention[eaa_column].std()
        if pre_std > 0:
            effect_size = abs(eaa_change) / pre_std
        else:
            effect_size = 0.0
        
        if is_improvement:
            if abs(eaa_change) > 2:
                interpretation = f"Müdahale sonrası belirgin iyileşme gözlendi (EAA: {eaa_change:.1f} yıl). " \
                               "Bu, tedavinin epigenetik yaşlanma üzerinde olumlu etkisi olduğunu göstermektedir."
            elif abs(eaa_change) > 0.5:
                interpretation = f"Müdahale sonrası hafif iyileşme gözlendi (EAA: {eaa_change:.1f} yıl)."
            else:
                interpretation = "Müdahale sonrası anlamlı bir değişiklik gözlenmedi."
        else:
            if eaa_change > 2:
                interpretation = f"Müdahale sonrası EAA'da artış gözlendi ({eaa_change:.1f} yıl). " \
                               "Bu, müdahalenin beklenen etkiyi sağlayamadığını göstermektedir."
            else:
                interpretation = f"Müdahale sonrası EAA stabil kalmıştır ({eaa_change:+.1f} yıl)."
        
        return InterventionEffect(
            intervention_date=intervention_date,
            pre_intervention_eaa=round(pre_eaa, 2),
            post_intervention_eaa=round(post_eaa, 2),
            eaa_change=round(eaa_change, 2),
            percent_change=round(percent_change, 1),
            is_improvement=is_improvement,
            effect_size=round(effect_size, 2),
            interpretation=interpretation
        )
    
    def predict_future_eaa(self, 
                           longitudinal_data: pd.DataFrame,
                           prediction_years: float = 5.0,
                           eaa_column: str = 'grimage_eaa') -> Dict:
        """
        Predict future EAA based on current trend.
        
        Args:
            longitudinal_data: Historical EAA data
            prediction_years: Years into future to predict
            eaa_column: Column name for EAA values
        
        Returns:
            Dictionary with predictions and confidence intervals
        """
        if len(longitudinal_data) < 2:
            return {
                'error': 'Yetersiz veri noktası',
                'predicted_eaa': None,
                'confidence_interval': None
            }
        
        df = longitudinal_data.sort_values('analysis_date').copy()
        df['years_from_start'] = (df['analysis_date'] - df['analysis_date'].iloc[0]).dt.days / 365.25
        
        x = df['years_from_start'].values
        y = df[eaa_column].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        current_time = x.max()
        future_time = current_time + prediction_years
        
        predicted_eaa = slope * future_time + intercept
        
        n = len(x)
        x_mean = np.mean(x)
        se_pred = std_err * np.sqrt(1 + 1/n + (future_time - x_mean)**2 / np.sum((x - x_mean)**2))
        
        t_value = stats.t.ppf(0.975, n - 2)
        ci_lower = predicted_eaa - t_value * se_pred
        ci_upper = predicted_eaa + t_value * se_pred
        
        return {
            'predicted_eaa': round(predicted_eaa, 2),
            'confidence_interval': (round(ci_lower, 2), round(ci_upper, 2)),
            'prediction_years': prediction_years,
            'current_eaa': round(y[-1], 2),
            'expected_change': round(predicted_eaa - y[-1], 2),
            'trend_slope': round(slope, 4),
            'r_squared': round(r_value**2, 4)
        }
    
    def calculate_recovery_rate(self,
                                 longitudinal_data: pd.DataFrame,
                                 baseline_date: datetime,
                                 target_eaa: float = 0.0,
                                 eaa_column: str = 'grimage_eaa') -> Dict:
        """
        Calculate recovery rate toward target EAA (e.g., normal aging).
        
        Args:
            longitudinal_data: Historical EAA data
            baseline_date: Treatment/intervention start date
            target_eaa: Target EAA value (default 0 = normal aging)
            eaa_column: Column name for EAA values
        
        Returns:
            Dictionary with recovery metrics
        """
        df = longitudinal_data[longitudinal_data['analysis_date'] >= baseline_date].copy()
        
        if len(df) < 2:
            return {
                'error': 'Yetersiz post-baseline veri',
                'recovery_rate': None
            }
        
        df = df.sort_values('analysis_date')
        df['days_from_baseline'] = (df['analysis_date'] - baseline_date).dt.days
        df['years_from_baseline'] = df['days_from_baseline'] / 365.25
        
        baseline_eaa = df[eaa_column].iloc[0]
        current_eaa = df[eaa_column].iloc[-1]
        time_elapsed = df['years_from_baseline'].iloc[-1]
        
        initial_gap = abs(baseline_eaa - target_eaa)
        current_gap = abs(current_eaa - target_eaa)
        
        if initial_gap > 0:
            recovery_percent = ((initial_gap - current_gap) / initial_gap) * 100
        else:
            recovery_percent = 100.0 if current_gap == 0 else 0.0
        
        if time_elapsed > 0:
            annual_recovery = (baseline_eaa - current_eaa) / time_elapsed
        else:
            annual_recovery = 0.0
        
        if annual_recovery > 0 and current_gap > 0:
            estimated_years_to_target = current_gap / annual_recovery
        else:
            estimated_years_to_target = None
        
        return {
            'baseline_eaa': round(baseline_eaa, 2),
            'current_eaa': round(current_eaa, 2),
            'target_eaa': target_eaa,
            'initial_gap': round(initial_gap, 2),
            'current_gap': round(current_gap, 2),
            'recovery_percent': round(recovery_percent, 1),
            'annual_recovery_rate': round(annual_recovery, 2),
            'time_elapsed_years': round(time_elapsed, 2),
            'estimated_years_to_target': round(estimated_years_to_target, 1) if estimated_years_to_target else None
        }
    
    def plot_longitudinal_trajectory(self,
                                      longitudinal_data: pd.DataFrame,
                                      patient_id: str,
                                      eaa_columns: List[str] = None,
                                      show_trend: bool = True,
                                      show_prediction: bool = True,
                                      prediction_years: float = 2.0) -> go.Figure:
        """
        Create interactive plot of longitudinal EAA trajectory.
        
        Args:
            longitudinal_data: Historical EAA data
            patient_id: Patient identifier
            eaa_columns: List of EAA columns to plot
            show_trend: Whether to show trend line
            show_prediction: Whether to show future predictions
            prediction_years: Years to predict into future
        
        Returns:
            Plotly Figure object
        """
        if eaa_columns is None:
            eaa_columns = ['grimage_eaa', 'phenoage_eaa', 'horvath_eaa', 'hannum_eaa']
        
        df = longitudinal_data.sort_values('analysis_date').copy()
        
        clock_colors = {
            'grimage_eaa': '#d62728',
            'phenoage_eaa': '#2ca02c',
            'horvath_eaa': '#1f77b4',
            'hannum_eaa': '#ff7f0e',
            'dunedinpace': '#9467bd'
        }
        
        clock_names = {
            'grimage_eaa': 'GrimAge EAA',
            'phenoage_eaa': 'PhenoAge EAA',
            'horvath_eaa': 'Horvath EAA',
            'hannum_eaa': 'Hannum EAA',
            'dunedinpace': 'DunedinPACE'
        }
        
        fig = go.Figure()
        
        for column in eaa_columns:
            if column in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['analysis_date'],
                    y=df[column],
                    mode='lines+markers',
                    name=clock_names.get(column, column),
                    line=dict(color=clock_colors.get(column, '#888888'), width=2),
                    marker=dict(size=10),
                    hovertemplate=f"<b>{clock_names.get(column, column)}</b><br>" +
                                 "Tarih: %{x|%d.%m.%Y}<br>" +
                                 "EAA: %{y:.2f} yıl<extra></extra>"
                ))
                
                if show_trend and len(df) >= 2:
                    x_numeric = (df['analysis_date'] - df['analysis_date'].iloc[0]).dt.days / 365.25
                    slope, intercept, _, _, _ = stats.linregress(x_numeric, df[column])
                    
                    trend_y = slope * x_numeric + intercept
                    
                    fig.add_trace(go.Scatter(
                        x=df['analysis_date'],
                        y=trend_y,
                        mode='lines',
                        name=f'{clock_names.get(column, column)} Trend',
                        line=dict(color=clock_colors.get(column, '#888888'), width=1, dash='dash'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                     annotation_text="Normal Yaşlanma (EAA=0)")
        
        fig.update_layout(
            title=dict(
                text=f'Hasta {patient_id} - Longitudinal Epigenetik Yaş Takibi',
                x=0.5,
                font=dict(size=16)
            ),
            xaxis_title='Tarih',
            yaxis_title='Epigenetik Yaş İvmelenmesi (yıl)',
            template='plotly_white',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def plot_intervention_timeline(self,
                                    longitudinal_data: pd.DataFrame,
                                    interventions: List[Dict],
                                    eaa_column: str = 'grimage_eaa') -> go.Figure:
        """
        Create timeline plot with intervention markers.
        
        Args:
            longitudinal_data: Historical EAA data
            interventions: List of intervention dicts with 'date', 'name', 'type'
            eaa_column: Column name for EAA values
        
        Returns:
            Plotly Figure object
        """
        df = longitudinal_data.sort_values('analysis_date').copy()
        
        fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3],
                           subplot_titles=('Epigenetik Yaş İvmelenmesi', 'Müdahaleler'),
                           vertical_spacing=0.15)
        
        fig.add_trace(
            go.Scatter(
                x=df['analysis_date'],
                y=df[eaa_column],
                mode='lines+markers',
                name='GrimAge EAA',
                line=dict(color='#d62728', width=2),
                marker=dict(size=10)
            ),
            row=1, col=1
        )
        
        colors = {'treatment': 'green', 'medication': 'blue', 'lifestyle': 'orange', 'other': 'gray'}
        symbols = {'treatment': 'triangle-up', 'medication': 'circle', 'lifestyle': 'square', 'other': 'diamond'}
        
        for intervention in interventions:
            int_date = intervention.get('date')
            int_name = intervention.get('name', 'Müdahale')
            int_type = intervention.get('type', 'other')
            
            fig.add_vline(
                x=int_date,
                line=dict(color=colors.get(int_type, 'gray'), width=2, dash='dot'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=[int_date],
                    y=[0.5],
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        symbol=symbols.get(int_type, 'circle'),
                        color=colors.get(int_type, 'gray')
                    ),
                    text=[int_name],
                    textposition='top center',
                    name=int_name,
                    showlegend=True
                ),
                row=2, col=1
            )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
        
        fig.update_layout(
            title=dict(text='Müdahale Zaman Çizelgesi ve EAA Değişimi', x=0.5),
            template='plotly_white',
            height=600,
            showlegend=True
        )
        
        fig.update_yaxes(title_text='EAA (yıl)', row=1, col=1)
        fig.update_yaxes(visible=False, row=2, col=1)
        fig.update_xaxes(title_text='Tarih', row=2, col=1)
        
        return fig
    
    def generate_longitudinal_report(self,
                                      longitudinal_data: pd.DataFrame,
                                      patient_id: str,
                                      interventions: List[Dict] = None) -> Dict:
        """
        Generate comprehensive longitudinal analysis report.
        
        Args:
            longitudinal_data: Historical EAA data
            patient_id: Patient identifier
            interventions: List of intervention dicts
        
        Returns:
            Dictionary with complete longitudinal analysis
        """
        report = {
            'patient_id': patient_id,
            'analysis_date': datetime.now().isoformat(),
            'n_timepoints': len(longitudinal_data),
            'clock_trends': {},
            'interventions': [],
            'predictions': {},
            'summary': {}
        }
        
        eaa_columns = ['grimage_eaa', 'phenoage_eaa', 'horvath_eaa', 'hannum_eaa']
        
        for column in eaa_columns:
            if column in longitudinal_data.columns:
                trend = self.analyze_trend(longitudinal_data, patient_id, column)
                report['clock_trends'][column] = {
                    'slope': trend.eaa_slope,
                    'r_squared': trend.eaa_r_squared,
                    'p_value': trend.eaa_p_value,
                    'direction': trend.trend_direction,
                    'is_significant': trend.is_significant,
                    'interpretation': trend.interpretation
                }
        
        if interventions:
            for intervention in interventions:
                effect = self.analyze_intervention_effect(
                    longitudinal_data,
                    intervention['date'],
                    'grimage_eaa'
                )
                if effect:
                    report['interventions'].append({
                        'name': intervention.get('name'),
                        'date': intervention['date'].isoformat(),
                        'pre_eaa': effect.pre_intervention_eaa,
                        'post_eaa': effect.post_intervention_eaa,
                        'change': effect.eaa_change,
                        'effect_size': effect.effect_size,
                        'interpretation': effect.interpretation
                    })
        
        prediction = self.predict_future_eaa(longitudinal_data, prediction_years=5.0)
        if 'error' not in prediction:
            report['predictions'] = prediction
        
        if report['clock_trends']:
            grimage_trend = report['clock_trends'].get('grimage_eaa', {})
            
            if grimage_trend.get('direction') == 'improving':
                overall_status = 'İyileşme Eğiliminde'
            elif grimage_trend.get('direction') == 'accelerating':
                overall_status = 'Kötüleşme Eğiliminde'
            else:
                overall_status = 'Stabil'
            
            report['summary'] = {
                'overall_status': overall_status,
                'primary_trend': grimage_trend.get('direction', 'unknown'),
                'annual_change': grimage_trend.get('slope', 0),
                'recommendation': self._get_recommendation(grimage_trend)
            }
        
        return report
    
    def _get_recommendation(self, trend: Dict) -> str:
        """Generate recommendation based on trend"""
        direction = trend.get('direction', 'stable')
        slope = trend.get('slope', 0)
        
        if direction == 'accelerating' and slope > 1.0:
            return "Acil müdahale önerilir. Madde kullanım tedavisinin yoğunlaştırılması ve " \
                   "yaşam tarzı değişiklikleri (egzersiz, beslenme) düşünülmelidir."
        elif direction == 'accelerating':
            return "Tedavi planının gözden geçirilmesi ve ek destek müdahaleleri önerilir."
        elif direction == 'improving':
            return "Mevcut tedavi planı etkin görünmektedir. Devam edilmesi önerilir."
        else:
            return "Stabil seyir. Rutin takip önerilir."


# End of module - # nrcdnl94