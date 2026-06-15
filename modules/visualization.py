# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Advanced Visualization Module for Epigenetic Age Analysis
Interactive Plotly charts, scientific visualizations, and publication-ready figures
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64


class EpigeneticVisualizer:
    # nrcdnl94
    """
    Comprehensive visualization toolkit for epigenetic age analysis.
    Includes interactive Plotly charts and publication-ready matplotlib figures.
    """
    
    SUBSTANCE_COLORS = {
        'control': '#2E86AB',
        'alcohol': '#A23B72',
        'cocaine': '#F18F01',
        'opioids': '#C73E1D',
        'methamphetamine': '#3B1F2B',
        'cannabis': '#44AF69',
        'polysubstance': '#6B2D5C'
    }
    
    CLOCK_COLORS = {
        'Horvath': '#1f77b4',
        'Hannum': '#ff7f0e',
        'PhenoAge': '#2ca02c',
        'GrimAge': '#d62728',
        'DunedinPACE': '#9467bd'
    }
    
    def __init__(self, theme: str = 'plotly_white'):
        """Initialize visualizer with theme settings"""
        self.theme = theme
        plt.style.use('seaborn-v0_8-whitegrid')
    
    def plot_age_correlation(self, 
                             chronological_ages: np.ndarray,
                             epigenetic_ages: np.ndarray,
                             clock_name: str = 'Epigenetic',
                             groups: Optional[np.ndarray] = None,
                             title: Optional[str] = None) -> go.Figure:
        """
        Create scatter plot of chronological vs epigenetic age.
        
        Args:
            chronological_ages: Array of chronological ages
            epigenetic_ages: Array of epigenetic ages
            clock_name: Name of the epigenetic clock
            groups: Optional group labels for coloring
            title: Optional custom title
        
        Returns:
            Plotly Figure object
        """
        df = pd.DataFrame({
            'Kronolojik Yaş': chronological_ages,
            'Epigenetik Yaş': epigenetic_ages,
            'Grup': groups if groups is not None else ['Tüm Örnekler'] * len(chronological_ages)
        })
        
        if groups is not None:
            fig = px.scatter(
                df, 
                x='Kronolojik Yaş', 
                y='Epigenetik Yaş',
                color='Grup',
                color_discrete_map=self.SUBSTANCE_COLORS,
                opacity=0.7,
                hover_data={'Kronolojik Yaş': ':.1f', 'Epigenetik Yaş': ':.1f'}
            )
        else:
            fig = px.scatter(
                df,
                x='Kronolojik Yaş',
                y='Epigenetik Yaş',
                opacity=0.7,
                hover_data={'Kronolojik Yaş': ':.1f', 'Epigenetik Yaş': ':.1f'}
            )
        
        min_age = min(chronological_ages.min(), epigenetic_ages.min()) - 5
        max_age = max(chronological_ages.max(), epigenetic_ages.max()) + 5
        
        fig.add_trace(go.Scatter(
            x=[min_age, max_age],
            y=[min_age, max_age],
            mode='lines',
            name='Mükemmel Korelasyon',
            line=dict(dash='dash', color='gray', width=2)
        ))
        
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            chronological_ages, epigenetic_ages
        )
        regression_y = slope * np.array([min_age, max_age]) + intercept
        
        fig.add_trace(go.Scatter(
            x=[min_age, max_age],
            y=regression_y,
            mode='lines',
            name=f'Regresyon (R²={r_value**2:.3f})',
            line=dict(color='red', width=2)
        ))
        
        if title is None:
            title = f'{clock_name} Saati: Kronolojik vs Epigenetik Yaş'
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            xaxis_title='Kronolojik Yaş (yıl)',
            yaxis_title=f'{clock_name} Epigenetik Yaş (yıl)',
            template=self.theme,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            height=500
        )
        
        mae = np.mean(np.abs(epigenetic_ages - chronological_ages))
        fig.add_annotation(
            x=0.98, y=0.02,
            xref='paper', yref='paper',
            text=f'MAE = {mae:.2f} yıl<br>R² = {r_value**2:.3f}',
            showarrow=False,
            font=dict(size=12),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray',
            borderwidth=1
        )
        
        return fig
    
    def plot_eaa_violin(self,
                        eaa_values: np.ndarray,
                        group_labels: np.ndarray,
                        title: str = 'Madde Tipine Göre Epigenetik Yaş İvmelenmesi') -> go.Figure:
        """
        Create violin plot of EAA distribution by substance group.
        """
        df = pd.DataFrame({
            'EAA (yıl)': eaa_values,
            'Madde Tipi': group_labels
        })
        
        group_order = ['control', 'alcohol', 'cocaine', 'opioids', 
                      'methamphetamine', 'cannabis', 'polysubstance']
        group_order = [g for g in group_order if g in df['Madde Tipi'].unique()]
        
        group_labels_tr = {
            'control': 'Kontrol',
            'alcohol': 'Alkol',
            'cocaine': 'Kokain',
            'opioids': 'Opioid',
            'methamphetamine': 'Metamfetamin',
            'cannabis': 'Kannabis',
            'polysubstance': 'Çoklu Madde'
        }
        df['Madde Tipi (TR)'] = df['Madde Tipi'].map(group_labels_tr)
        
        fig = go.Figure()
        
        for group in group_order:
            group_data = df[df['Madde Tipi'] == group]['EAA (yıl)']
            color = self.SUBSTANCE_COLORS.get(group, '#888888')
            
            fig.add_trace(go.Violin(
                y=group_data,
                name=group_labels_tr.get(group, group),
                box_visible=True,
                meanline_visible=True,
                fillcolor=color,
                line_color=color,
                opacity=0.7
            ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                     annotation_text="Referans (EAA=0)")
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            yaxis_title='Epigenetik Yaş İvmelenmesi (yıl)',
            xaxis_title='Madde Tipi',
            template=self.theme,
            showlegend=False,
            height=500
        )
        
        return fig
    
    def plot_eaa_boxplot_comparison(self,
                                     eaa_values: np.ndarray,
                                     group_labels: np.ndarray,
                                     clock_results: Dict = None) -> go.Figure:
        """
        Create grouped boxplot comparing EAA across multiple clocks.
        """
        if clock_results is None:
            df = pd.DataFrame({
                'EAA': eaa_values,
                'Grup': group_labels,
                'Saat': ['GrimAge'] * len(eaa_values)
            })
        else:
            data = []
            for clock_name, results in clock_results.items():
                for i, (eaa, group) in enumerate(zip(results, group_labels)):
                    data.append({
                        'EAA': eaa,
                        'Grup': group,
                        'Saat': clock_name
                    })
            df = pd.DataFrame(data)
        
        fig = px.box(
            df,
            x='Grup',
            y='EAA',
            color='Saat',
            color_discrete_map=self.CLOCK_COLORS,
            title='Epigenetik Saatlere Göre Yaş İvmelenmesi Karşılaştırması'
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        fig.update_layout(
            template=self.theme,
            xaxis_title='Madde Tipi',
            yaxis_title='Epigenetik Yaş İvmelenmesi (yıl)',
            height=500
        )
        
        return fig
    
    def plot_volcano(self,
                     dma_results: pd.DataFrame,
                     p_value_threshold: float = 0.05,
                     fc_threshold: float = 0.1,
                     title: str = 'Diferansiyel Metilasyon Volcano Plot') -> go.Figure:
        """
        Create volcano plot for differential methylation analysis.
        """
        df = dma_results.copy()
        df['-log10(p)'] = -np.log10(df['p_value'] + 1e-300)
        
        conditions = [
            (df['adjusted_p_value'] < p_value_threshold) & (df['mean_diff'] > fc_threshold),
            (df['adjusted_p_value'] < p_value_threshold) & (df['mean_diff'] < -fc_threshold),
            True
        ]
        choices = ['Hipermetilasyon', 'Hipometilasyon', 'Anlamsız']
        df['Durum'] = np.select(conditions, choices)
        
        color_map = {
            'Hipermetilasyon': '#d62728',
            'Hipometilasyon': '#2ca02c',
            'Anlamsız': '#7f7f7f'
        }
        
        fig = px.scatter(
            df,
            x='mean_diff',
            y='-log10(p)',
            color='Durum',
            color_discrete_map=color_map,
            hover_data=['cpg_id', 'mean_diff', 'adjusted_p_value'],
            opacity=0.6
        )
        
        fig.add_hline(y=-np.log10(p_value_threshold), line_dash="dash", 
                     line_color="gray", annotation_text=f"p={p_value_threshold}")
        fig.add_vline(x=fc_threshold, line_dash="dash", line_color="gray")
        fig.add_vline(x=-fc_threshold, line_dash="dash", line_color="gray")
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            xaxis_title='Ortalama Metilasyon Farkı (Δβ)',
            yaxis_title='-log₁₀(p-değeri)',
            template=self.theme,
            height=500
        )
        
        n_hyper = (df['Durum'] == 'Hipermetilasyon').sum()
        n_hypo = (df['Durum'] == 'Hipometilasyon').sum()
        fig.add_annotation(
            x=0.02, y=0.98,
            xref='paper', yref='paper',
            text=f'Hipermetilasyon: {n_hyper}<br>Hipometilasyon: {n_hypo}',
            showarrow=False,
            font=dict(size=11),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray'
        )
        
        return fig
    
    def plot_heatmap(self,
                     correlation_matrix: pd.DataFrame,
                     title: str = 'Korelasyon Matrisi') -> go.Figure:
        """
        Create interactive heatmap for correlation matrix.
        """
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu_r',
            zmid=0,
            text=np.round(correlation_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            template=self.theme,
            height=600,
            width=700
        )
        
        return fig
    
    def plot_roc_curves(self,
                        fpr_dict: Dict[str, np.ndarray],
                        tpr_dict: Dict[str, np.ndarray],
                        auc_dict: Dict[str, float],
                        title: str = 'ROC Eğrileri - Model Performansı') -> go.Figure:
        """
        Plot ROC curves for multiple models.
        """
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1
        
        for i, (model_name, fpr) in enumerate(fpr_dict.items()):
            tpr = tpr_dict[model_name]
            auc = auc_dict[model_name]
            
            fig.add_trace(go.Scatter(
                x=fpr,
                y=tpr,
                mode='lines',
                name=f'{model_name} (AUC = {auc:.3f})',
                line=dict(color=colors[i % len(colors)], width=2)
            ))
        
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Rastgele Sınıflandırıcı',
            line=dict(dash='dash', color='gray', width=1)
        ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            xaxis_title='Yanlış Pozitif Oranı (1-Özgüllük)',
            yaxis_title='Doğru Pozitif Oranı (Duyarlılık)',
            template=self.theme,
            height=500,
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1])
        )
        
        return fig
    
    def plot_clock_comparison_radar(self,
                                     clock_results: Dict,
                                     sample_id: str = 'Örnek') -> go.Figure:
        """
        Create radar chart comparing all epigenetic clock results.
        """
        categories = list(clock_results.keys())
        
        eaa_values = []
        for clock_name in categories:
            result = clock_results[clock_name]
            if hasattr(result, 'age_acceleration'):
                eaa_values.append(result.age_acceleration)
            else:
                eaa_values.append(result)
        
        eaa_values.append(eaa_values[0])
        categories_closed = categories + [categories[0]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=eaa_values,
            theta=categories_closed,
            fill='toself',
            name=sample_id,
            line_color='#1f77b4'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[min(eaa_values) - 2, max(eaa_values) + 2]
                )
            ),
            showlegend=True,
            title=dict(text=f'{sample_id} - Epigenetik Saat Karşılaştırması', x=0.5),
            height=500
        )
        
        return fig
    
    def plot_mediation_diagram(self,
                                mediation_result) -> go.Figure:
        """
        Create mediation path diagram.
        """
        fig = go.Figure()
        
        positions = {
            'exposure': (0.1, 0.5),
            'mediator': (0.5, 0.8),
            'outcome': (0.9, 0.5)
        }
        
        labels = {
            'exposure': 'Madde<br>Maruziyeti',
            'mediator': f'{mediation_result.mediator}<br>(Aracı)',
            'outcome': 'Epigenetik<br>Yaş İvmelenmesi'
        }
        
        for key, (x, y) in positions.items():
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(size=60, color='lightblue', line=dict(color='darkblue', width=2)),
                text=[labels[key]],
                textposition='middle center',
                textfont=dict(size=10),
                showlegend=False
            ))
        
        fig.add_annotation(
            x=positions['mediator'][0], y=positions['mediator'][1] - 0.1,
            ax=positions['exposure'][0] + 0.05, ay=positions['exposure'][1] + 0.1,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='green'
        )
        
        indirect_text = f"a×b = {mediation_result.indirect_effect:.3f}"
        if mediation_result.is_significant:
            indirect_text += " *"
        
        fig.add_annotation(
            x=0.3, y=0.7,
            text=indirect_text,
            showarrow=False,
            font=dict(size=11, color='green')
        )
        
        fig.add_annotation(
            x=positions['outcome'][0] - 0.05, y=positions['outcome'][1] + 0.1,
            ax=positions['mediator'][0] + 0.05, ay=positions['mediator'][1] - 0.1,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='green'
        )
        
        fig.add_annotation(
            x=positions['outcome'][0] - 0.05, y=positions['outcome'][1] - 0.1,
            ax=positions['exposure'][0] + 0.05, ay=positions['exposure'][1] - 0.1,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='blue'
        )
        
        direct_text = f"c' = {mediation_result.direct_effect:.3f}"
        fig.add_annotation(
            x=0.5, y=0.35,
            text=direct_text,
            showarrow=False,
            font=dict(size=11, color='blue')
        )
        
        total_text = f"Toplam Etki: {mediation_result.total_effect:.3f}"
        prop_text = f"Mediated: {mediation_result.proportion_mediated*100:.1f}%"
        
        fig.add_annotation(
            x=0.5, y=0.15,
            text=f"{total_text}<br>{prop_text}",
            showarrow=False,
            font=dict(size=12),
            bgcolor='rgba(255,255,255,0.8)'
        )
        
        fig.update_layout(
            title=dict(text='Mediyasyon Analizi Diyagramı', x=0.5),
            xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, showticklabels=False),
            height=400,
            template=self.theme
        )
        
        return fig
    
    def plot_feature_importance(self,
                                 importance_df: pd.DataFrame,
                                 top_n: int = 20,
                                 title: str = 'CpG Özellik Önem Sıralaması') -> go.Figure:
        """
        Create horizontal bar chart of feature importance.
        """
        df = importance_df.head(top_n).sort_values('importance')
        
        fig = go.Figure(go.Bar(
            x=df['importance'],
            y=df['feature'],
            orientation='h',
            marker_color='steelblue'
        ))
        
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=16)),
            xaxis_title='Önem Skoru',
            yaxis_title='CpG Bölgesi',
            template=self.theme,
            height=max(400, top_n * 25)
        )
        
        return fig
    
    def plot_model_performance_comparison(self,
                                           metrics: Dict) -> go.Figure:
        """
        Create bar chart comparing model performance metrics.
        """
        models = list(metrics.keys())
        mae_values = [m.mae for m in metrics.values()]
        r2_values = [m.r_squared for m in metrics.values()]
        
        fig = make_subplots(rows=1, cols=2, 
                           subplot_titles=('MAE (yıl)', 'R² Skoru'))
        
        fig.add_trace(
            go.Bar(x=models, y=mae_values, name='MAE', marker_color='coral'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=models, y=r2_values, name='R²', marker_color='steelblue'),
            row=1, col=2
        )
        
        fig.update_layout(
            title=dict(text='Model Performans Karşılaştırması', x=0.5),
            showlegend=False,
            template=self.theme,
            height=400
        )
        
        return fig
    
    def create_dashboard_summary(self,
                                  sample_results: Dict,
                                  reference_stats: Dict = None) -> go.Figure:
        """
        Create a summary dashboard figure with key metrics.
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Epigenetik Saat Sonuçları',
                'Referans Karşılaştırması',
                'Yaş İvmelenmesi Dağılımı',
                'Risk Değerlendirmesi'
            ),
            specs=[[{"type": "bar"}, {"type": "indicator"}],
                   [{"type": "histogram"}, {"type": "pie"}]]
        )
        
        clock_names = list(sample_results.keys())
        eaa_values = [r.age_acceleration if hasattr(r, 'age_acceleration') else r 
                     for r in sample_results.values()]
        
        fig.add_trace(
            go.Bar(x=clock_names, y=eaa_values, marker_color='steelblue'),
            row=1, col=1
        )
        
        mean_eaa = np.mean(eaa_values)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=mean_eaa,
                delta={'reference': 0, 'relative': False},
                gauge={
                    'axis': {'range': [-10, 15]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [-10, -2], 'color': "lightgreen"},
                        {'range': [-2, 2], 'color': "lightyellow"},
                        {'range': [2, 5], 'color': "orange"},
                        {'range': [5, 15], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': mean_eaa
                    }
                },
                title={'text': "Ortalama EAA"}
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Histogram(x=eaa_values, nbinsx=10, marker_color='steelblue'),
            row=2, col=1
        )
        
        risk_levels = ['Düşük', 'Orta', 'Yüksek']
        risk_counts = [
            sum(1 for e in eaa_values if e < 2),
            sum(1 for e in eaa_values if 2 <= e < 5),
            sum(1 for e in eaa_values if e >= 5)
        ]
        
        fig.add_trace(
            go.Pie(labels=risk_levels, values=risk_counts,
                  marker_colors=['green', 'orange', 'red']),
            row=2, col=2
        )
        
        fig.update_layout(
            height=700,
            showlegend=False,
            title=dict(text='Epigenetik Yaş Analizi Özeti', x=0.5, font=dict(size=18)),
            template=self.theme
        )
        
        return fig


# End of module - # nrcdnl94