"""
Multi-omics Integration Module for EpiClock Prototype
Integration of transcriptomic and proteomic data with DNA methylation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
from scipy.cluster import hierarchy
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@dataclass
class OmicsLayer:
    """Single omics data layer"""
    name: str
    data_type: str
    n_features: int
    n_samples: int
    feature_names: List[str]
    sample_names: List[str]


@dataclass
class IntegrationResult:
    """Result of multi-omics integration"""
    method: str
    n_layers: int
    n_samples: int
    variance_explained: List[float]
    top_features: Dict[str, List[str]]
    cross_layer_correlations: pd.DataFrame
    integrated_scores: pd.DataFrame


@dataclass
class MultiOmicsProfile:
    """Complete multi-omics profile for a sample"""
    sample_id: str
    methylation_age: float
    transcriptomic_age: float
    proteomic_age: float
    integrated_age: float
    age_concordance: float
    discordant_features: Dict[str, List[str]]


class MultiOmicsIntegrator:
    """
    Multi-omics integration for comprehensive biological age assessment.
    Combines DNA methylation, transcriptomics, and proteomics data.
    """
    
    AGING_GENES = {
        'senescence': ['CDKN2A', 'CDKN1A', 'TP53', 'RB1', 'E2F1'],
        'telomere': ['TERT', 'TERC', 'POT1', 'TRF1', 'TRF2'],
        'mitochondria': ['MT-ND1', 'MT-CO1', 'MT-ATP6', 'PGC1A', 'NRF1'],
        'inflammation': ['IL6', 'TNF', 'IL1B', 'NFKB1', 'CRP', 'IL8'],
        'autophagy': ['ATG5', 'BECN1', 'LC3', 'SQSTM1', 'ULK1'],
        'proteostasis': ['HSP70', 'HSP90', 'HSPA1A', 'DNAJB1', 'BAG3'],
        'stem_cell': ['OCT4', 'SOX2', 'NANOG', 'KLF4', 'MYC'],
        'epigenetic': ['DNMT1', 'DNMT3A', 'TET1', 'TET2', 'HDAC1', 'SIRT1']
    }
    
    AGING_PROTEINS = {
        'inflammatory': ['CRP', 'IL6', 'TNF', 'SAA', 'Fibrinogen'],
        'metabolic': ['Insulin', 'IGF1', 'Adiponectin', 'Leptin', 'HOMA-IR'],
        'hormonal': ['Cortisol', 'DHEAS', 'GH', 'TSH', 'Testosterone'],
        'oxidative_stress': ['MDA', 'SOD', 'GPx', 'CAT', 'GSH'],
        'kidney': ['Creatinine', 'Cystatin_C', 'BUN', 'eGFR'],
        'liver': ['Albumin', 'ALT', 'AST', 'GGT', 'ALP']
    }
    
    SUBSTANCE_SIGNATURES = {
        'alcohol': {
            'methylation': ['cg00000001', 'cg00000010', 'cg00000020'],
            'transcriptomic': ['ADH1B', 'ALDH2', 'CYP2E1', 'IL6', 'TNF'],
            'proteomic': ['GGT', 'MCV', 'CDT', 'AST', 'ALT']
        },
        'cocaine': {
            'methylation': ['cg00000002', 'cg00000011', 'cg00000021'],
            'transcriptomic': ['DRD2', 'SLC6A3', 'BDNF', 'COMT'],
            'proteomic': ['Dopamine', 'Prolactin', 'Cortisol']
        },
        'opioids': {
            'methylation': ['cg00000003', 'cg00000012', 'cg00000022'],
            'transcriptomic': ['OPRM1', 'OPRD1', 'POMC', 'PENK'],
            'proteomic': ['Beta_endorphin', 'Enkephalin', 'Cortisol']
        },
        'methamphetamine': {
            'methylation': ['cg00000004', 'cg00000013', 'cg00000023'],
            'transcriptomic': ['SLC6A3', 'TH', 'MAOA', 'DRD2'],
            'proteomic': ['Dopamine', 'Norepinephrine', 'Serotonin']
        }
    }
    
    def __init__(self):
        self.scaler = StandardScaler()
        np.random.seed(42)
    
    def simulate_transcriptomic_data(self, 
                                      n_samples: int,
                                      chronological_ages: np.ndarray,
                                      substance_types: np.ndarray = None) -> pd.DataFrame:
        """
        Simulate transcriptomic (RNA-seq) data for demonstration.
        
        Args:
            n_samples: Number of samples
            chronological_ages: Array of chronological ages
            substance_types: Optional substance type labels
        
        Returns:
            DataFrame with simulated gene expression values
        """
        all_genes = []
        for category in self.AGING_GENES.values():
            all_genes.extend(category)
        all_genes = list(set(all_genes))
        
        n_genes = len(all_genes) + 50
        gene_names = all_genes + [f'Gene_{i}' for i in range(50)]
        
        expression_data = np.zeros((n_samples, n_genes))
        
        for i, gene in enumerate(gene_names):
            base_expression = np.random.normal(8, 2)
            
            if gene in ['CDKN2A', 'CDKN1A', 'TP53', 'IL6', 'TNF', 'IL1B']:
                age_effect = 0.02 * chronological_ages
            elif gene in ['TERT', 'TERC', 'OCT4', 'SOX2', 'NANOG']:
                age_effect = -0.015 * chronological_ages
            else:
                age_effect = np.random.uniform(-0.005, 0.005) * chronological_ages
            
            noise = np.random.normal(0, 0.5, n_samples)
            
            expression_data[:, i] = base_expression + age_effect + noise
        
        if substance_types is not None:
            for j, substance in enumerate(substance_types):
                if substance in self.SUBSTANCE_SIGNATURES:
                    sig_genes = self.SUBSTANCE_SIGNATURES[substance].get('transcriptomic', [])
                    for gene in sig_genes:
                        if gene in gene_names:
                            idx = gene_names.index(gene)
                            expression_data[j, idx] += np.random.uniform(0.5, 1.5)
        
        sample_names = [f'Sample_{i}' for i in range(n_samples)]
        
        return pd.DataFrame(expression_data, index=sample_names, columns=gene_names)
    
    def simulate_proteomic_data(self,
                                 n_samples: int,
                                 chronological_ages: np.ndarray,
                                 substance_types: np.ndarray = None) -> pd.DataFrame:
        """
        Simulate proteomic data for demonstration.
        
        Args:
            n_samples: Number of samples
            chronological_ages: Array of chronological ages
            substance_types: Optional substance type labels
        
        Returns:
            DataFrame with simulated protein levels
        """
        all_proteins = []
        for category in self.AGING_PROTEINS.values():
            all_proteins.extend(category)
        all_proteins = list(set(all_proteins))
        
        n_proteins = len(all_proteins)
        
        protein_data = np.zeros((n_samples, n_proteins))
        
        for i, protein in enumerate(all_proteins):
            base_level = np.random.uniform(10, 100)
            
            if protein in ['CRP', 'IL6', 'TNF', 'Fibrinogen', 'MDA']:
                age_effect = 0.5 * chronological_ages
            elif protein in ['IGF1', 'DHEAS', 'Testosterone', 'GH', 'Albumin']:
                age_effect = -0.3 * chronological_ages
            else:
                age_effect = np.random.uniform(-0.1, 0.1) * chronological_ages
            
            noise = np.random.normal(0, base_level * 0.1, n_samples)
            
            protein_data[:, i] = base_level + age_effect + noise
            protein_data[:, i] = np.clip(protein_data[:, i], 0, None)
        
        sample_names = [f'Sample_{i}' for i in range(n_samples)]
        
        return pd.DataFrame(protein_data, index=sample_names, columns=all_proteins)
    
    def calculate_transcriptomic_age(self,
                                      expression_data: pd.DataFrame,
                                      chronological_ages: np.ndarray) -> np.ndarray:
        """
        Calculate transcriptomic age based on gene expression patterns.
        
        Args:
            expression_data: Gene expression matrix
            chronological_ages: Array of chronological ages
        
        Returns:
            Array of predicted transcriptomic ages
        """
        aging_genes = [g for g in expression_data.columns 
                      if g in sum(self.AGING_GENES.values(), [])]
        
        if len(aging_genes) < 5:
            aging_genes = expression_data.columns[:20].tolist()
        
        X = expression_data[aging_genes].values
        X_scaled = self.scaler.fit_transform(X)
        
        pca = PCA(n_components=min(5, len(aging_genes)))
        pc_scores = pca.fit_transform(X_scaled)
        
        slope, intercept, _, _, _ = stats.linregress(pc_scores[:, 0], chronological_ages)
        
        transcriptomic_ages = pc_scores[:, 0] * slope + intercept
        
        noise = np.random.normal(0, 2, len(transcriptomic_ages))
        transcriptomic_ages += noise
        
        return np.clip(transcriptomic_ages, 18, 100)
    
    def calculate_proteomic_age(self,
                                 protein_data: pd.DataFrame,
                                 chronological_ages: np.ndarray) -> np.ndarray:
        """
        Calculate proteomic age based on protein levels.
        
        Args:
            protein_data: Protein level matrix
            chronological_ages: Array of chronological ages
        
        Returns:
            Array of predicted proteomic ages
        """
        aging_proteins = [p for p in protein_data.columns
                         if p in sum(self.AGING_PROTEINS.values(), [])]
        
        if len(aging_proteins) < 5:
            aging_proteins = protein_data.columns[:15].tolist()
        
        X = protein_data[aging_proteins].values
        X_scaled = self.scaler.fit_transform(X)
        
        pca = PCA(n_components=min(5, len(aging_proteins)))
        pc_scores = pca.fit_transform(X_scaled)
        
        slope, intercept, _, _, _ = stats.linregress(pc_scores[:, 0], chronological_ages)
        
        proteomic_ages = pc_scores[:, 0] * slope + intercept
        
        noise = np.random.normal(0, 2.5, len(proteomic_ages))
        proteomic_ages += noise
        
        return np.clip(proteomic_ages, 18, 100)
    
    def integrate_multi_omics(self,
                               methylation_data: pd.DataFrame,
                               expression_data: pd.DataFrame,
                               protein_data: pd.DataFrame,
                               chronological_ages: np.ndarray) -> IntegrationResult:
        """
        Integrate multiple omics layers using data fusion.
        
        Args:
            methylation_data: DNA methylation beta values
            expression_data: Gene expression data
            protein_data: Protein level data
            chronological_ages: Array of chronological ages
        
        Returns:
            IntegrationResult with integrated analysis
        """
        common_samples = list(set(methylation_data.index) & 
                             set(expression_data.index) & 
                             set(protein_data.index))
        
        n_samples = len(common_samples)
        
        meth_scaled = self.scaler.fit_transform(methylation_data.loc[common_samples].values[:, :100])
        expr_scaled = self.scaler.fit_transform(expression_data.loc[common_samples].values[:, :50])
        prot_scaled = self.scaler.fit_transform(protein_data.loc[common_samples].values[:, :30])
        
        combined = np.hstack([meth_scaled, expr_scaled, prot_scaled])
        
        pca = PCA(n_components=10)
        integrated_scores = pca.fit_transform(combined)
        
        variance_explained = pca.explained_variance_ratio_.tolist()
        
        feature_importance = np.abs(pca.components_[0])
        
        n_meth = meth_scaled.shape[1]
        n_expr = expr_scaled.shape[1]
        
        meth_importance = feature_importance[:n_meth]
        expr_importance = feature_importance[n_meth:n_meth+n_expr]
        prot_importance = feature_importance[n_meth+n_expr:]
        
        top_features = {
            'methylation': [f'CpG_{i}' for i in np.argsort(meth_importance)[-10:][::-1]],
            'transcriptomic': [expression_data.columns[i] for i in np.argsort(expr_importance)[-10:][::-1]],
            'proteomic': [protein_data.columns[i] for i in np.argsort(prot_importance)[-10:][::-1]]
        }
        
        layer_scores = {
            'methylation': meth_scaled.mean(axis=1),
            'transcriptomic': expr_scaled.mean(axis=1),
            'proteomic': prot_scaled.mean(axis=1)
        }
        
        corr_matrix = np.corrcoef(np.vstack(list(layer_scores.values())))
        cross_layer_correlations = pd.DataFrame(
            corr_matrix,
            index=['methylation', 'transcriptomic', 'proteomic'],
            columns=['methylation', 'transcriptomic', 'proteomic']
        )
        
        integrated_df = pd.DataFrame(
            integrated_scores,
            index=common_samples,
            columns=[f'PC{i+1}' for i in range(10)]
        )
        
        return IntegrationResult(
            method='PCA_fusion',
            n_layers=3,
            n_samples=n_samples,
            variance_explained=variance_explained,
            top_features=top_features,
            cross_layer_correlations=cross_layer_correlations,
            integrated_scores=integrated_df
        )
    
    def calculate_integrated_age(self,
                                  methylation_age: float,
                                  transcriptomic_age: float,
                                  proteomic_age: float,
                                  weights: Dict[str, float] = None) -> float:
        """
        Calculate integrated biological age from multiple omics layers.
        
        Args:
            methylation_age: Epigenetic age from DNA methylation
            transcriptomic_age: Age from transcriptomic data
            proteomic_age: Age from proteomic data
            weights: Optional custom weights for each layer
        
        Returns:
            Integrated biological age
        """
        if weights is None:
            weights = {
                'methylation': 0.50,
                'transcriptomic': 0.30,
                'proteomic': 0.20
            }
        
        integrated_age = (
            methylation_age * weights['methylation'] +
            transcriptomic_age * weights['transcriptomic'] +
            proteomic_age * weights['proteomic']
        )
        
        return round(integrated_age, 2)
    
    def calculate_age_concordance(self,
                                   methylation_age: float,
                                   transcriptomic_age: float,
                                   proteomic_age: float) -> float:
        """
        Calculate concordance between different omics-based age estimates.
        
        Args:
            methylation_age: Epigenetic age
            transcriptomic_age: Transcriptomic age
            proteomic_age: Proteomic age
        
        Returns:
            Concordance score (0-1, higher = more concordant)
        """
        ages = [methylation_age, transcriptomic_age, proteomic_age]
        std_dev = np.std(ages)
        mean_age = np.mean(ages)
        
        cv = std_dev / mean_age if mean_age > 0 else 0
        concordance = 1 - min(cv, 1)
        
        return round(concordance, 3)
    
    def identify_discordant_features(self,
                                      methylation_data: pd.DataFrame,
                                      expression_data: pd.DataFrame,
                                      sample_idx: int,
                                      threshold: float = 2.0) -> Dict[str, List[str]]:
        """
        Identify features with discordant patterns between omics layers.
        
        Args:
            methylation_data: DNA methylation data
            expression_data: Gene expression data
            sample_idx: Sample index to analyze
            threshold: Z-score threshold for discordance
        
        Returns:
            Dictionary of discordant features by category
        """
        discordant = {
            'hyper_meth_low_expr': [],
            'hypo_meth_high_expr': [],
            'other_discordant': []
        }
        
        sample_meth = methylation_data.iloc[sample_idx].values
        sample_expr = expression_data.iloc[sample_idx].values
        
        meth_z = (sample_meth - np.mean(sample_meth)) / (np.std(sample_meth) + 1e-10)
        expr_z = (sample_expr - np.mean(sample_expr)) / (np.std(sample_expr) + 1e-10)
        
        n_common = min(len(meth_z), len(expr_z), 50)
        
        for i in range(n_common):
            if meth_z[i] > threshold and expr_z[i] < -threshold:
                discordant['hyper_meth_low_expr'].append(f'Feature_{i}')
            elif meth_z[i] < -threshold and expr_z[i] > threshold:
                discordant['hypo_meth_high_expr'].append(f'Feature_{i}')
            elif abs(meth_z[i] - expr_z[i]) > 2 * threshold:
                discordant['other_discordant'].append(f'Feature_{i}')
        
        return discordant
    
    def plot_multi_omics_overview(self,
                                   integration_result: IntegrationResult) -> go.Figure:
        """Create overview visualization of multi-omics integration"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Variance Explained by PCs',
                'Cross-Layer Correlations',
                'Sample Distribution (PC1 vs PC2)',
                'Top Features by Layer'
            ),
            specs=[[{"type": "bar"}, {"type": "heatmap"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        fig.add_trace(
            go.Bar(
                x=[f'PC{i+1}' for i in range(len(integration_result.variance_explained))],
                y=[v * 100 for v in integration_result.variance_explained],
                marker_color='steelblue'
            ),
            row=1, col=1
        )
        
        corr = integration_result.cross_layer_correlations
        fig.add_trace(
            go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                colorscale='RdBu',
                zmid=0,
                text=np.round(corr.values, 2),
                texttemplate='%{text}',
                showscale=True
            ),
            row=1, col=2
        )
        
        scores = integration_result.integrated_scores
        fig.add_trace(
            go.Scatter(
                x=scores['PC1'],
                y=scores['PC2'],
                mode='markers',
                marker=dict(size=8, color='steelblue', opacity=0.6),
                hovertemplate="PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>"
            ),
            row=2, col=1
        )
        
        layer_counts = []
        layer_names = []
        for layer, features in integration_result.top_features.items():
            layer_counts.append(len(features))
            layer_names.append(layer)
        
        fig.add_trace(
            go.Bar(
                x=layer_names,
                y=layer_counts,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title=dict(text='Multi-Omics Integration Overview', x=0.5),
            template='plotly_white',
            height=700,
            showlegend=False
        )
        
        fig.update_yaxes(title_text='Variance (%)', row=1, col=1)
        fig.update_xaxes(title_text='PC1', row=2, col=1)
        fig.update_yaxes(title_text='PC2', row=2, col=1)
        
        return fig
    
    def plot_age_comparison(self,
                            chronological_ages: np.ndarray,
                            methylation_ages: np.ndarray,
                            transcriptomic_ages: np.ndarray,
                            proteomic_ages: np.ndarray,
                            integrated_ages: np.ndarray) -> go.Figure:
        """Create comparison plot of different age estimates"""
        
        fig = make_subplots(rows=2, cols=2,
                           subplot_titles=(
                               'Methylation Age',
                               'Transcriptomic Age',
                               'Proteomic Age',
                               'Integrated Age'
                           ))
        
        ages_list = [
            (methylation_ages, 'Methylation'),
            (transcriptomic_ages, 'Transcriptomic'),
            (proteomic_ages, 'Proteomic'),
            (integrated_ages, 'Integrated')
        ]
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        colors = ['#d62728', '#2ca02c', '#1f77b4', '#9467bd']
        
        for (ages, name), (row, col), color in zip(ages_list, positions, colors):
            r, _ = stats.pearsonr(chronological_ages, ages)
            mae = np.mean(np.abs(ages - chronological_ages))
            
            fig.add_trace(
                go.Scatter(
                    x=chronological_ages,
                    y=ages,
                    mode='markers',
                    marker=dict(color=color, size=8, opacity=0.6),
                    name=name,
                    hovertemplate=f"Chrono: %{{x:.1f}}<br>{name}: %{{y:.1f}}<extra></extra>"
                ),
                row=row, col=col
            )
            
            min_age = min(chronological_ages.min(), ages.min())
            max_age = max(chronological_ages.max(), ages.max())
            fig.add_trace(
                go.Scatter(
                    x=[min_age, max_age],
                    y=[min_age, max_age],
                    mode='lines',
                    line=dict(dash='dash', color='gray'),
                    showlegend=False
                ),
                row=row, col=col
            )
            
            fig.add_annotation(
                x=0.02, y=0.98,
                xref='paper', yref='paper',
                text=f"R={r:.3f}, MAE={mae:.1f}",
                showarrow=False,
                font=dict(size=10),
                row=row, col=col
            )
        
        fig.update_layout(
            title=dict(text='Multi-Omics Age Comparison', x=0.5),
            template='plotly_white',
            height=700,
            showlegend=False
        )
        
        for row in [1, 2]:
            for col in [1, 2]:
                fig.update_xaxes(title_text='Chronological Age', row=row, col=col)
                fig.update_yaxes(title_text='Predicted Age', row=row, col=col)
        
        return fig
    
    def generate_multiomics_report(self,
                                    sample_id: str,
                                    chronological_age: float,
                                    methylation_age: float,
                                    transcriptomic_age: float,
                                    proteomic_age: float,
                                    integration_result: IntegrationResult = None) -> Dict:
        """Generate comprehensive multi-omics analysis report"""
        
        integrated_age = self.calculate_integrated_age(
            methylation_age, transcriptomic_age, proteomic_age
        )
        concordance = self.calculate_age_concordance(
            methylation_age, transcriptomic_age, proteomic_age
        )
        
        ages = {
            'methylation': methylation_age,
            'transcriptomic': transcriptomic_age,
            'proteomic': proteomic_age,
            'integrated': integrated_age
        }
        
        accelerations = {
            name: age - chronological_age
            for name, age in ages.items()
        }
        
        if concordance < 0.7:
            concordance_interpretation = "Düşük uyum - farklı biyolojik süreçler farklı hızlarda yaşlanıyor olabilir"
        elif concordance < 0.85:
            concordance_interpretation = "Orta uyum - genel yaşlanma paterni tutarlı"
        else:
            concordance_interpretation = "Yüksek uyum - tüm biyolojik sistemler benzer hızda yaşlanıyor"
        
        return {
            'sample_id': sample_id,
            'chronological_age': chronological_age,
            'ages': ages,
            'accelerations': {k: round(v, 2) for k, v in accelerations.items()},
            'concordance': concordance,
            'concordance_interpretation': concordance_interpretation,
            'top_features': integration_result.top_features if integration_result else {},
            'cross_layer_correlations': integration_result.cross_layer_correlations.to_dict() if integration_result else {},
            'interpretation': self._generate_interpretation(
                accelerations, concordance, chronological_age
            )
        }
    
    def _generate_interpretation(self,
                                  accelerations: Dict[str, float],
                                  concordance: float,
                                  chronological_age: float) -> str:
        """Generate text interpretation of multi-omics results"""
        
        integrated_acc = accelerations.get('integrated', 0)
        
        if integrated_acc > 5:
            severity = "belirgin biyolojik yaşlanma hızlanması"
        elif integrated_acc > 2:
            severity = "hafif biyolojik yaşlanma hızlanması"
        elif integrated_acc < -2:
            severity = "biyolojik olarak genç görünüm"
        else:
            severity = "yaşa uygun biyolojik profil"
        
        interpretation = f"Multi-omik entegrasyon analizi sonucunda {severity} tespit edilmiştir "
        interpretation += f"(Entegre biyolojik yaş: {chronological_age + integrated_acc:.1f} yıl). "
        
        max_layer = max(accelerations.items(), key=lambda x: abs(x[1]) if x[0] != 'integrated' else 0)
        if max_layer[0] != 'integrated':
            if max_layer[1] > 3:
                interpretation += f"{max_layer[0].title()} katmanında belirgin yaşlanma gözlenmektedir. "
            elif max_layer[1] < -3:
                interpretation += f"{max_layer[0].title()} katmanında koruyucu faktörler tespit edilmiştir. "
        
        if concordance < 0.7:
            interpretation += "Farklı omik katmanlar arasında tutarsızlık, hedefe yönelik müdahalelerin gerekli olabileceğini göstermektedir."
        
        return interpretation
