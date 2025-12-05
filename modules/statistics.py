# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Statistical Analysis Module for Epigenetic Age Acceleration
Includes EAA calculation, mediation analysis, moderation analysis, and DMA
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
import warnings
warnings.filterwarnings('ignore')


@dataclass
# nrcdnl94
class EAAResults:
    # nrcdnl94
    """Epigenetic Age Acceleration results"""
    sample_id: str
    chronological_age: float
    epigenetic_age: float
    eaa: float
    eaa_residual: float
    percentile: float
    z_score: float
    interpretation: str


@dataclass
# nrcdnl94
class DifferentialMethylationResult:
    # nrcdnl94
    """Result for a single CpG in differential methylation analysis"""
    cpg_id: str
    mean_diff: float
    log2_fold_change: float
    p_value: float
    adjusted_p_value: float
    is_significant: bool
    direction: str


@dataclass
# nrcdnl94
class MediationResult:
    # nrcdnl94
    """Mediation analysis result"""
    mediator: str
    total_effect: float
    direct_effect: float
    indirect_effect: float
    proportion_mediated: float
    sobel_z: float
    sobel_p: float
    is_significant: bool


@dataclass
# nrcdnl94
class ModerationResult:
    # nrcdnl94
    """Moderation analysis result"""
    moderator: str
    main_effect: float
    interaction_effect: float
    interaction_p: float
    simple_slopes: Dict[str, float]
    is_significant: bool


class StatisticalAnalyzer:
    # nrcdnl94
    """
    Comprehensive statistical analysis for epigenetic age acceleration studies.
    """
    
    SUBSTANCE_TYPES = ['control', 'alcohol', 'cocaine', 'opioids', 
                       'methamphetamine', 'cannabis', 'polysubstance']
    
    PHYSIOLOGICAL_MEDIATORS = ['homa_ir', 'cortisol_acth_ratio', 'crp', 
                               'il6', 'tnf_alpha', 'telomere_length']
    
    PSYCHOLOGICAL_MODERATORS = ['ders_score', 'self_control', 'social_support',
                                'resilience', 'coping_style']
    
    def __init__(self, alpha: float = 0.05):
        """
        Initialize the statistical analyzer.
        
        Args:
            alpha: Significance level for statistical tests
        """
        self.alpha = alpha
    
    def calculate_eaa(self, chronological_ages: np.ndarray,
                      epigenetic_ages: np.ndarray,
                      method: str = 'residual') -> List[EAAResults]:
        """
        Calculate Epigenetic Age Acceleration (EAA).
        
        Args:
            chronological_ages: Array of chronological ages
            epigenetic_ages: Array of predicted epigenetic ages
            method: 'residual' (age-adjusted) or 'difference'
        
        Returns:
            List of EAAResults for each sample
        """
        n_samples = len(chronological_ages)
        
        simple_eaa = epigenetic_ages - chronological_ages
        
        if method == 'residual':
            X = sm.add_constant(chronological_ages)
            model = sm.OLS(epigenetic_ages, X).fit()
            eaa_residual = model.resid
        else:
            eaa_residual = simple_eaa
        
        eaa_mean = np.mean(eaa_residual)
        eaa_std = np.std(eaa_residual)
        
        results = []
        for i in range(n_samples):
            z_score = (eaa_residual[i] - eaa_mean) / (eaa_std + 1e-10)
            percentile = stats.norm.cdf(z_score) * 100
            
            if eaa_residual[i] < -5:
                interpretation = "Significant biological youth"
            elif eaa_residual[i] < -2:
                interpretation = "Moderate biological youth"
            elif eaa_residual[i] < 2:
                interpretation = "Age-appropriate"
            elif eaa_residual[i] < 5:
                interpretation = "Moderate age acceleration"
            else:
                interpretation = "Significant age acceleration"
            
            results.append(EAAResults(
                sample_id=f"Sample_{i}",
                chronological_age=round(chronological_ages[i], 1),
                epigenetic_age=round(epigenetic_ages[i], 1),
                eaa=round(simple_eaa[i], 2),
                eaa_residual=round(eaa_residual[i], 2),
                percentile=round(percentile, 1),
                z_score=round(z_score, 2),
                interpretation=interpretation
            ))
        
        return results
    
    def compare_groups(self, eaa_values: np.ndarray,
                       group_labels: np.ndarray,
                       reference_group: str = 'control') -> pd.DataFrame:
        """
        Compare EAA between substance groups vs control.
        
        Args:
            eaa_values: Array of EAA values
            group_labels: Array of group assignments
            reference_group: Reference group for comparisons
        
        Returns:
            DataFrame with group comparison statistics
        """
        unique_groups = np.unique(group_labels)
        reference_data = eaa_values[group_labels == reference_group]
        
        results = []
        for group in unique_groups:
            group_data = eaa_values[group_labels == group]
            
            mean_eaa = np.mean(group_data)
            std_eaa = np.std(group_data)
            n = len(group_data)
            
            se = std_eaa / np.sqrt(n)
            ci_lower = mean_eaa - 1.96 * se
            ci_upper = mean_eaa + 1.96 * se
            
            if group != reference_group and len(reference_data) > 0:
                t_stat, p_value = stats.ttest_ind(group_data, reference_data)
                
                pooled_std = np.sqrt((np.var(group_data) + np.var(reference_data)) / 2)
                cohens_d = (mean_eaa - np.mean(reference_data)) / (pooled_std + 1e-10)
            else:
                t_stat, p_value, cohens_d = 0, 1, 0
            
            results.append({
                'group': group,
                'n': n,
                'mean_eaa': round(mean_eaa, 2),
                'std_eaa': round(std_eaa, 2),
                'ci_lower': round(ci_lower, 2),
                'ci_upper': round(ci_upper, 2),
                't_statistic': round(t_stat, 3),
                'p_value': round(p_value, 4),
                'cohens_d': round(cohens_d, 3),
                'significant': p_value < self.alpha
            })
        
        df = pd.DataFrame(results)
        
        _, adjusted_p, _, _ = multipletests(
            df['p_value'].values, 
            method='fdr_bh'
        )
        df['adjusted_p_value'] = np.round(adjusted_p, 4)
        df['significant_adjusted'] = adjusted_p < self.alpha
        
        return df
    
    def anova_analysis(self, eaa_values: np.ndarray,
                       group_labels: np.ndarray) -> Dict:
        """
        Perform one-way ANOVA and post-hoc tests.
        
        Returns:
            Dictionary with ANOVA results
        """
        unique_groups = np.unique(group_labels)
        groups = [eaa_values[group_labels == g] for g in unique_groups]
        
        f_stat, p_value = stats.f_oneway(*groups)
        
        total_n = len(eaa_values)
        k = len(unique_groups)
        ss_between = sum(len(g) * (np.mean(g) - np.mean(eaa_values))**2 for g in groups)
        ss_total = np.sum((eaa_values - np.mean(eaa_values))**2)
        eta_squared = ss_between / (ss_total + 1e-10)
        
        posthoc_results = []
        for i, g1 in enumerate(unique_groups):
            for j, g2 in enumerate(unique_groups):
                if i < j:
                    data1 = eaa_values[group_labels == g1]
                    data2 = eaa_values[group_labels == g2]
                    t_stat, p = stats.ttest_ind(data1, data2)
                    posthoc_results.append({
                        'group1': g1,
                        'group2': g2,
                        'mean_diff': round(np.mean(data1) - np.mean(data2), 2),
                        't_statistic': round(t_stat, 3),
                        'p_value': round(p, 4)
                    })
        
        if posthoc_results:
            p_values = [r['p_value'] for r in posthoc_results]
            _, adjusted_p, _, _ = multipletests(p_values, method='bonferroni')
            for i, r in enumerate(posthoc_results):
                r['adjusted_p'] = round(adjusted_p[i], 4)
                r['significant'] = adjusted_p[i] < self.alpha
        
        return {
            'f_statistic': round(f_stat, 3),
            'p_value': round(p_value, 6),
            'eta_squared': round(eta_squared, 4),
            'significant': p_value < self.alpha,
            'n_groups': k,
            'total_n': total_n,
            'posthoc': pd.DataFrame(posthoc_results)
        }
    
    def differential_methylation_analysis(self, 
                                          methylation_data: pd.DataFrame,
                                          group_labels: np.ndarray,
                                          case_group: str,
                                          control_group: str = 'control',
                                          min_delta_beta: float = 0.05) -> pd.DataFrame:
        """
        Perform differential methylation analysis (DMA) between groups.
        
        Args:
            methylation_data: Beta values matrix (samples x CpGs)
            group_labels: Group assignments
            case_group: Case group name
            control_group: Control group name
            min_delta_beta: Minimum beta difference for significance
        
        Returns:
            DataFrame with DMA results
        """
        case_mask = group_labels == case_group
        control_mask = group_labels == control_group
        
        case_data = methylation_data.loc[case_mask]
        control_data = methylation_data.loc[control_mask]
        
        results = []
        
        for cpg in methylation_data.columns:
            case_values = case_data[cpg].values
            control_values = control_data[cpg].values
            
            mean_case = np.mean(case_values)
            mean_control = np.mean(control_values)
            mean_diff = mean_case - mean_control
            
            epsilon = 0.01
            log2_fc = np.log2((mean_case + epsilon) / (mean_control + epsilon))
            
            t_stat, p_value = stats.ttest_ind(case_values, control_values)
            
            results.append({
                'cpg_id': cpg,
                'mean_case': round(mean_case, 4),
                'mean_control': round(mean_control, 4),
                'mean_diff': round(mean_diff, 4),
                'log2_fold_change': round(log2_fc, 4),
                't_statistic': round(t_stat, 3),
                'p_value': p_value
            })
        
        df = pd.DataFrame(results)
        
        _, adjusted_p, _, _ = multipletests(df['p_value'].values, method='fdr_bh')
        df['adjusted_p_value'] = adjusted_p
        
        df['is_significant'] = (df['adjusted_p_value'] < self.alpha) & \
                               (np.abs(df['mean_diff']) >= min_delta_beta)
        
        df['direction'] = np.where(df['mean_diff'] > 0, 'hypermethylated', 'hypomethylated')
        
        df = df.sort_values('p_value')
        
        return df
    
    def mediation_analysis(self, 
                           eaa_values: np.ndarray,
                           substance_exposure: np.ndarray,
                           mediator_values: np.ndarray,
                           mediator_name: str = 'mediator') -> MediationResult:
        """
        Perform mediation analysis (Sobel test).
        
        Tests whether a mediator (e.g., inflammation) mediates the 
        relationship between substance use and EAA.
        
        Args:
            eaa_values: Epigenetic age acceleration values
            substance_exposure: Binary or continuous exposure variable
            mediator_values: Proposed mediator values
            mediator_name: Name of the mediator
        
        Returns:
            MediationResult with effect decomposition
        """
        X = sm.add_constant(substance_exposure)
        model_total = sm.OLS(eaa_values, X).fit()
        total_effect = model_total.params[1]
        
        model_a = sm.OLS(mediator_values, X).fit()
        a = model_a.params[1]
        se_a = model_a.bse[1]
        
        X_mediated = sm.add_constant(np.column_stack([substance_exposure, mediator_values]))
        model_b = sm.OLS(eaa_values, X_mediated).fit()
        b = model_b.params[2]
        se_b = model_b.bse[2]
        direct_effect = model_b.params[1]
        
        indirect_effect = a * b
        
        sobel_se = np.sqrt(b**2 * se_a**2 + a**2 * se_b**2)
        sobel_z = indirect_effect / (sobel_se + 1e-10)
        sobel_p = 2 * (1 - stats.norm.cdf(abs(sobel_z)))
        
        proportion_mediated = indirect_effect / (total_effect + 1e-10)
        proportion_mediated = np.clip(proportion_mediated, 0, 1)
        
        return MediationResult(
            mediator=mediator_name,
            total_effect=round(total_effect, 4),
            direct_effect=round(direct_effect, 4),
            indirect_effect=round(indirect_effect, 4),
            proportion_mediated=round(proportion_mediated, 4),
            sobel_z=round(sobel_z, 3),
            sobel_p=round(sobel_p, 4),
            is_significant=sobel_p < self.alpha
        )
    
    def moderation_analysis(self,
                            eaa_values: np.ndarray,
                            substance_exposure: np.ndarray,
                            moderator_values: np.ndarray,
                            moderator_name: str = 'moderator') -> ModerationResult:
        """
        Perform moderation analysis.
        
        Tests whether a moderator (e.g., resilience) moderates the 
        relationship between substance use and EAA.
        
        Args:
            eaa_values: Epigenetic age acceleration values
            substance_exposure: Predictor variable
            moderator_values: Proposed moderator values
            moderator_name: Name of the moderator
        
        Returns:
            ModerationResult with interaction effects
        """
        exposure_centered = substance_exposure - np.mean(substance_exposure)
        moderator_centered = moderator_values - np.mean(moderator_values)
        interaction = exposure_centered * moderator_centered
        
        X = sm.add_constant(np.column_stack([
            exposure_centered, 
            moderator_centered, 
            interaction
        ]))
        
        model = sm.OLS(eaa_values, X).fit()
        
        main_effect = model.params[1]
        interaction_effect = model.params[3]
        interaction_p = model.pvalues[3]
        
        mod_low = np.mean(moderator_values) - np.std(moderator_values)
        mod_high = np.mean(moderator_values) + np.std(moderator_values)
        
        simple_slopes = {
            'low_moderator': round(main_effect + interaction_effect * (mod_low - np.mean(moderator_values)), 4),
            'mean_moderator': round(main_effect, 4),
            'high_moderator': round(main_effect + interaction_effect * (mod_high - np.mean(moderator_values)), 4)
        }
        
        return ModerationResult(
            moderator=moderator_name,
            main_effect=round(main_effect, 4),
            interaction_effect=round(interaction_effect, 4),
            interaction_p=round(interaction_p, 4),
            simple_slopes=simple_slopes,
            is_significant=interaction_p < self.alpha
        )
    
    def correlation_matrix(self, 
                          variables: pd.DataFrame,
                          method: str = 'pearson') -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculate correlation matrix with p-values.
        
        Args:
            variables: DataFrame with variables to correlate
            method: 'pearson' or 'spearman'
        
        Returns:
            Tuple of (correlation matrix, p-value matrix)
        """
        n = variables.shape[1]
        corr_matrix = np.zeros((n, n))
        p_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    corr_matrix[i, j] = 1.0
                    p_matrix[i, j] = 0.0
                else:
                    x = variables.iloc[:, i].values
                    y = variables.iloc[:, j].values
                    
                    mask = ~(np.isnan(x) | np.isnan(y))
                    x, y = x[mask], y[mask]
                    
                    if method == 'pearson':
                        r, p = stats.pearsonr(x, y)
                    else:
                        r, p = stats.spearmanr(x, y)
                    
                    corr_matrix[i, j] = r
                    p_matrix[i, j] = p
        
        columns = variables.columns
        corr_df = pd.DataFrame(corr_matrix, index=columns, columns=columns)
        p_df = pd.DataFrame(p_matrix, index=columns, columns=columns)
        
        return corr_df.round(3), p_df.round(4)
    
    def generate_summary_statistics(self, 
                                    data: pd.DataFrame,
                                    group_column: Optional[str] = None) -> pd.DataFrame:
        """
        Generate comprehensive summary statistics.
        
        Args:
            data: DataFrame with numerical variables
            group_column: Optional column for grouped statistics
        
        Returns:
            Summary statistics DataFrame
        """
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if group_column and group_column in data.columns:
            summary = data.groupby(group_column)[numeric_cols].agg([
                'count', 'mean', 'std', 'min', 
                lambda x: x.quantile(0.25),
                'median',
                lambda x: x.quantile(0.75),
                'max'
            ])
            summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        else:
            summary = data[numeric_cols].describe().T
            summary['cv'] = summary['std'] / (summary['mean'] + 1e-10)
            summary['skewness'] = data[numeric_cols].skew()
            summary['kurtosis'] = data[numeric_cols].kurtosis()
        
        return summary.round(3)


# End of module - # nrcdnl94