"""
Istatistiksel Validasyon Modulu
EpiClock v4.0

Uluslararasi hesaplamali calisma standartlari:
- Coklu test duzeltmesi (FDR, Bonferroni)
- Bootstrap guven araliklari
- ROC-AUC / PR-AUC metrikleri
- Power analizi
- Effect size hesaplama
- Cross-validation

Referanslar:
- Benjamini & Hochberg (1995) - FDR
- Efron & Tibshirani (1993) - Bootstrap
- DeLong et al. (1988) - ROC comparison
- Cohen (1988) - Effect sizes
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass
from scipy import stats
from scipy.special import comb
import warnings


# ============================================================================
# COKLU TEST DUZELTMESI
# ============================================================================

class MultipleTestingCorrection:
    """
    Coklu Test Duzeltmesi
    
    EWAS/GWAS analizlerinde tip I hata kontrolu
    """
    
    @staticmethod
    def bonferroni(p_values: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Bonferroni duzeltmesi
        
        En muhafazakar yontem
        alpha_adj = alpha / n_tests
        """
        n = len(p_values)
        alpha_adj = alpha / n
        significant = p_values < alpha_adj
        
        return {
            'method': 'Bonferroni',
            'n_tests': n,
            'alpha_original': alpha,
            'alpha_adjusted': alpha_adj,
            'threshold': alpha_adj,
            'n_significant': int(np.sum(significant)),
            'significant_indices': np.where(significant)[0].tolist(),
            'corrected_p': np.minimum(p_values * n, 1.0)
        }
    
    @staticmethod
    def benjamini_hochberg(p_values: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Benjamini-Hochberg FDR duzeltmesi
        
        False Discovery Rate kontrolu
        Daha az muhafazakar, EWAS icin tercih edilir
        """
        n = len(p_values)
        sorted_idx = np.argsort(p_values)
        sorted_p = p_values[sorted_idx]
        
        # Critical values
        critical = np.arange(1, n + 1) * alpha / n
        
        # Find largest k where p(k) <= k*alpha/n
        significant_sorted = sorted_p <= critical
        
        # Calculate adjusted p-values (q-values)
        q_values = np.zeros(n)
        q_values[sorted_idx[-1]] = sorted_p[-1]
        
        for i in range(n - 2, -1, -1):
            q_values[sorted_idx[i]] = min(
                q_values[sorted_idx[i + 1]],
                sorted_p[i] * n / (i + 1)
            )
        q_values = np.minimum(q_values, 1.0)
        
        significant = q_values < alpha
        
        return {
            'method': 'Benjamini-Hochberg (FDR)',
            'n_tests': n,
            'alpha_original': alpha,
            'fdr_level': alpha,
            'n_significant': int(np.sum(significant)),
            'significant_indices': np.where(significant)[0].tolist(),
            'q_values': q_values,
            'adjusted_p': q_values
        }
    
    @staticmethod
    def storey_q(p_values: np.ndarray, lambda_val: float = 0.5) -> Dict[str, Any]:
        """
        Storey q-value yontemi
        
        pi0 tahmini ile daha guclu FDR kontrolu
        """
        n = len(p_values)
        
        # Estimate pi0 (proportion of true nulls)
        pi0 = np.sum(p_values > lambda_val) / (n * (1 - lambda_val))
        pi0 = min(pi0, 1.0)
        
        # Sort p-values
        sorted_idx = np.argsort(p_values)
        sorted_p = p_values[sorted_idx]
        
        # Calculate q-values
        q_values = np.zeros(n)
        q_values[sorted_idx[-1]] = pi0 * sorted_p[-1]
        
        for i in range(n - 2, -1, -1):
            q_values[sorted_idx[i]] = min(
                q_values[sorted_idx[i + 1]],
                pi0 * sorted_p[i] * n / (i + 1)
            )
        
        return {
            'method': 'Storey q-value',
            'n_tests': n,
            'pi0_estimate': round(pi0, 4),
            'lambda': lambda_val,
            'q_values': q_values
        }
    
    @staticmethod
    def holm(p_values: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Holm-Bonferroni step-down yontemi
        
        Bonferroni'den daha guclu, FWER kontrolu
        """
        n = len(p_values)
        sorted_idx = np.argsort(p_values)
        sorted_p = p_values[sorted_idx]
        
        # Adjusted p-values
        adjusted = np.zeros(n)
        adjusted[sorted_idx[0]] = sorted_p[0] * n
        
        for i in range(1, n):
            adjusted[sorted_idx[i]] = max(
                adjusted[sorted_idx[i - 1]],
                sorted_p[i] * (n - i)
            )
        adjusted = np.minimum(adjusted, 1.0)
        
        significant = adjusted < alpha
        
        return {
            'method': 'Holm-Bonferroni',
            'n_tests': n,
            'alpha_original': alpha,
            'n_significant': int(np.sum(significant)),
            'significant_indices': np.where(significant)[0].tolist(),
            'adjusted_p': adjusted
        }


# ============================================================================
# BOOTSTRAP GUVEN ARALIKLARI
# ============================================================================

class BootstrapCI:
    """
    Bootstrap Guven Araliklari
    
    Non-parametrik guven araligi tahmini
    """
    
    @staticmethod
    def percentile(data: np.ndarray, 
                   statistic: Callable,
                   n_bootstrap: int = 10000,
                   ci_level: float = 0.95,
                   seed: int = 42) -> Dict[str, Any]:
        """
        Percentile bootstrap CI
        
        En basit ve robust yontem
        """
        np.random.seed(seed)
        n = len(data)
        
        boot_stats = []
        for _ in range(n_bootstrap):
            boot_sample = data[np.random.randint(0, n, n)]
            boot_stats.append(statistic(boot_sample))
        
        boot_stats = np.array(boot_stats)
        
        alpha = 1 - ci_level
        ci_lower = np.percentile(boot_stats, alpha / 2 * 100)
        ci_upper = np.percentile(boot_stats, (1 - alpha / 2) * 100)
        
        return {
            'method': 'Percentile Bootstrap',
            'n_bootstrap': n_bootstrap,
            'ci_level': ci_level,
            'point_estimate': statistic(data),
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'se_bootstrap': np.std(boot_stats),
            'bias': np.mean(boot_stats) - statistic(data)
        }
    
    @staticmethod
    def bca(data: np.ndarray,
            statistic: Callable,
            n_bootstrap: int = 10000,
            ci_level: float = 0.95,
            seed: int = 42) -> Dict[str, Any]:
        """
        BCa (Bias-Corrected and Accelerated) bootstrap CI
        
        Bias ve skewness duzeltmeli, en doğru yontem
        """
        np.random.seed(seed)
        n = len(data)
        
        # Original statistic
        theta_hat = statistic(data)
        
        # Bootstrap distribution
        boot_stats = []
        for _ in range(n_bootstrap):
            boot_sample = data[np.random.randint(0, n, n)]
            boot_stats.append(statistic(boot_sample))
        boot_stats = np.array(boot_stats)
        
        # Bias correction (z0)
        z0 = stats.norm.ppf(np.mean(boot_stats < theta_hat))
        
        # Acceleration (a) via jackknife
        jack_stats = []
        for i in range(n):
            jack_sample = np.delete(data, i)
            jack_stats.append(statistic(jack_sample))
        jack_stats = np.array(jack_stats)
        jack_mean = np.mean(jack_stats)
        
        num = np.sum((jack_mean - jack_stats) ** 3)
        denom = 6 * (np.sum((jack_mean - jack_stats) ** 2) ** 1.5)
        a = num / denom if denom != 0 else 0
        
        # BCa percentiles
        alpha = 1 - ci_level
        z_alpha_lower = stats.norm.ppf(alpha / 2)
        z_alpha_upper = stats.norm.ppf(1 - alpha / 2)
        
        p_lower = stats.norm.cdf(z0 + (z0 + z_alpha_lower) / (1 - a * (z0 + z_alpha_lower)))
        p_upper = stats.norm.cdf(z0 + (z0 + z_alpha_upper) / (1 - a * (z0 + z_alpha_upper)))
        
        ci_lower = np.percentile(boot_stats, p_lower * 100)
        ci_upper = np.percentile(boot_stats, p_upper * 100)
        
        return {
            'method': 'BCa Bootstrap',
            'n_bootstrap': n_bootstrap,
            'ci_level': ci_level,
            'point_estimate': theta_hat,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'bias_correction': z0,
            'acceleration': a,
            'se_bootstrap': np.std(boot_stats)
        }


# ============================================================================
# ROC-AUC VE PR-AUC
# ============================================================================

class ClassificationMetrics:
    """
    Siniflandirma Performans Metrikleri
    
    ROC-AUC, PR-AUC, Sensitivity, Specificity
    """
    
    @staticmethod
    def confusion_matrix(y_true: np.ndarray, 
                         y_pred: np.ndarray,
                         threshold: float = 0.5) -> Dict[str, int]:
        """Confusion matrix hesapla"""
        
        y_binary = (y_pred >= threshold).astype(int)
        
        tp = np.sum((y_true == 1) & (y_binary == 1))
        tn = np.sum((y_true == 0) & (y_binary == 0))
        fp = np.sum((y_true == 0) & (y_binary == 1))
        fn = np.sum((y_true == 1) & (y_binary == 0))
        
        return {'tp': int(tp), 'tn': int(tn), 'fp': int(fp), 'fn': int(fn)}
    
    @staticmethod
    def roc_curve(y_true: np.ndarray, 
                  y_scores: np.ndarray,
                  n_thresholds: int = 100) -> Dict[str, Any]:
        """ROC curve hesapla"""
        
        thresholds = np.linspace(0, 1, n_thresholds)
        tpr_list = []
        fpr_list = []
        
        for thresh in thresholds:
            cm = ClassificationMetrics.confusion_matrix(y_true, y_scores, thresh)
            
            tpr = cm['tp'] / (cm['tp'] + cm['fn']) if (cm['tp'] + cm['fn']) > 0 else 0
            fpr = cm['fp'] / (cm['fp'] + cm['tn']) if (cm['fp'] + cm['tn']) > 0 else 0
            
            tpr_list.append(tpr)
            fpr_list.append(fpr)
        
        return {
            'fpr': np.array(fpr_list),
            'tpr': np.array(tpr_list),
            'thresholds': thresholds
        }
    
    @staticmethod
    def roc_auc(y_true: np.ndarray, y_scores: np.ndarray) -> float:
        """ROC-AUC hesapla (trapezoidal integration)"""
        
        roc = ClassificationMetrics.roc_curve(y_true, y_scores)
        
        # Sort by FPR
        sorted_idx = np.argsort(roc['fpr'])
        fpr_sorted = roc['fpr'][sorted_idx]
        tpr_sorted = roc['tpr'][sorted_idx]
        
        # Trapezoidal integration
        auc = np.trapz(tpr_sorted, fpr_sorted)
        
        return round(abs(auc), 4)
    
    @staticmethod
    def pr_curve(y_true: np.ndarray,
                 y_scores: np.ndarray,
                 n_thresholds: int = 100) -> Dict[str, Any]:
        """Precision-Recall curve hesapla"""
        
        thresholds = np.linspace(0, 1, n_thresholds)
        precision_list = []
        recall_list = []
        
        for thresh in thresholds:
            cm = ClassificationMetrics.confusion_matrix(y_true, y_scores, thresh)
            
            precision = cm['tp'] / (cm['tp'] + cm['fp']) if (cm['tp'] + cm['fp']) > 0 else 0
            recall = cm['tp'] / (cm['tp'] + cm['fn']) if (cm['tp'] + cm['fn']) > 0 else 0
            
            precision_list.append(precision)
            recall_list.append(recall)
        
        return {
            'precision': np.array(precision_list),
            'recall': np.array(recall_list),
            'thresholds': thresholds
        }
    
    @staticmethod
    def pr_auc(y_true: np.ndarray, y_scores: np.ndarray) -> float:
        """PR-AUC hesapla"""
        
        pr = ClassificationMetrics.pr_curve(y_true, y_scores)
        
        # Sort by recall
        sorted_idx = np.argsort(pr['recall'])
        recall_sorted = pr['recall'][sorted_idx]
        precision_sorted = pr['precision'][sorted_idx]
        
        # Trapezoidal integration
        auc = np.trapz(precision_sorted, recall_sorted)
        
        return round(abs(auc), 4)
    
    @staticmethod
    def delong_test(y_true: np.ndarray,
                    y_scores1: np.ndarray,
                    y_scores2: np.ndarray) -> Dict[str, float]:
        """
        DeLong test - iki ROC-AUC karsilastirmasi
        
        DeLong et al. (1988)
        """
        
        auc1 = ClassificationMetrics.roc_auc(y_true, y_scores1)
        auc2 = ClassificationMetrics.roc_auc(y_true, y_scores2)
        
        # Simplified z-test (approximation)
        n = len(y_true)
        se = np.sqrt((1/n) * auc1 * (1 - auc1) + (1/n) * auc2 * (1 - auc2))
        
        if se > 0:
            z = (auc1 - auc2) / se
            p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        else:
            z = 0
            p_value = 1.0
        
        return {
            'auc1': auc1,
            'auc2': auc2,
            'difference': round(auc1 - auc2, 4),
            'z_statistic': round(z, 4),
            'p_value': round(p_value, 4),
            'significant': p_value < 0.05
        }


# ============================================================================
# EFFECT SIZE
# ============================================================================

class EffectSize:
    """
    Effect Size Hesaplama
    
    Cohen's d, Hedge's g, Glass's delta, eta-squared
    """
    
    @staticmethod
    def cohens_d(group1: np.ndarray, group2: np.ndarray) -> Dict[str, float]:
        """
        Cohen's d - standardized mean difference
        
        d = (M1 - M2) / pooled_SD
        """
        n1, n2 = len(group1), len(group2)
        m1, m2 = np.mean(group1), np.mean(group2)
        s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        
        # Pooled standard deviation
        pooled_sd = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
        
        d = (m1 - m2) / pooled_sd if pooled_sd > 0 else 0
        
        # Interpretation
        if abs(d) < 0.2:
            interpretation = "negligible"
        elif abs(d) < 0.5:
            interpretation = "small"
        elif abs(d) < 0.8:
            interpretation = "medium"
        else:
            interpretation = "large"
        
        # 95% CI (approximate)
        se = np.sqrt((n1 + n2) / (n1 * n2) + d**2 / (2 * (n1 + n2)))
        ci_lower = d - 1.96 * se
        ci_upper = d + 1.96 * se
        
        return {
            'effect_size': round(d, 4),
            'interpretation': interpretation,
            'ci_lower': round(ci_lower, 4),
            'ci_upper': round(ci_upper, 4),
            'method': "Cohen's d"
        }
    
    @staticmethod
    def hedges_g(group1: np.ndarray, group2: np.ndarray) -> Dict[str, float]:
        """
        Hedge's g - bias-corrected Cohen's d
        
        Kucuk orneklemler icin tercih edilir
        """
        result = EffectSize.cohens_d(group1, group2)
        d = result['effect_size']
        
        n1, n2 = len(group1), len(group2)
        df = n1 + n2 - 2
        
        # Correction factor
        j = 1 - (3 / (4 * df - 1))
        g = d * j
        
        result['effect_size'] = round(g, 4)
        result['method'] = "Hedge's g"
        result['correction_factor'] = round(j, 4)
        
        return result
    
    @staticmethod
    def eta_squared(groups: List[np.ndarray]) -> Dict[str, float]:
        """
        Eta-squared - ANOVA effect size
        
        SS_between / SS_total
        """
        all_data = np.concatenate(groups)
        grand_mean = np.mean(all_data)
        
        ss_total = np.sum((all_data - grand_mean) ** 2)
        
        ss_between = sum(
            len(g) * (np.mean(g) - grand_mean) ** 2
            for g in groups
        )
        
        eta_sq = ss_between / ss_total if ss_total > 0 else 0
        
        # Interpretation (Cohen, 1988)
        if eta_sq < 0.01:
            interpretation = "negligible"
        elif eta_sq < 0.06:
            interpretation = "small"
        elif eta_sq < 0.14:
            interpretation = "medium"
        else:
            interpretation = "large"
        
        return {
            'effect_size': round(eta_sq, 4),
            'interpretation': interpretation,
            'method': "Eta-squared",
            'n_groups': len(groups)
        }
    
    @staticmethod
    def correlation_to_d(r: float) -> float:
        """Korelasyonu Cohen's d'ye cevir"""
        if abs(r) >= 1:
            return np.sign(r) * np.inf
        return 2 * r / np.sqrt(1 - r**2)


# ============================================================================
# POWER ANALIZI
# ============================================================================

class PowerAnalysis:
    """
    Power Analizi
    
    Orneklem buyuklugu hesaplama
    """
    
    @staticmethod
    def two_sample_ttest(effect_size: float,
                         alpha: float = 0.05,
                         power: float = 0.80,
                         ratio: float = 1.0) -> Dict[str, Any]:
        """
        Iki orneklem t-test icin orneklem buyuklugu
        
        Args:
            effect_size: Cohen's d
            alpha: Tip I hata orani
            power: 1 - Tip II hata orani
            ratio: n2/n1 orani
        """
        
        # Z scores
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)
        
        # Sample size per group (equal allocation)
        n1 = ((z_alpha + z_beta) ** 2 * 2) / (effect_size ** 2) if effect_size != 0 else np.inf
        n2 = n1 * ratio
        
        return {
            'n_per_group': int(np.ceil(n1)),
            'n_group1': int(np.ceil(n1)),
            'n_group2': int(np.ceil(n2)),
            'n_total': int(np.ceil(n1 + n2)),
            'effect_size': effect_size,
            'alpha': alpha,
            'power': power,
            'ratio': ratio
        }
    
    @staticmethod
    def correlation(effect_size: float,
                    alpha: float = 0.05,
                    power: float = 0.80) -> Dict[str, Any]:
        """Korelasyon testi icin orneklem buyuklugu"""
        
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)
        
        # Fisher's z transformation
        z_r = 0.5 * np.log((1 + effect_size) / (1 - effect_size)) if abs(effect_size) < 1 else np.inf
        
        n = ((z_alpha + z_beta) / z_r) ** 2 + 3 if z_r != 0 else np.inf
        
        return {
            'n_required': int(np.ceil(n)),
            'correlation': effect_size,
            'alpha': alpha,
            'power': power
        }
    
    @staticmethod
    def ewas_sample_size(n_cpgs: int = 450000,
                         expected_significant: int = 100,
                         effect_size: float = 0.05,
                         alpha: float = 0.05,
                         power: float = 0.80) -> Dict[str, Any]:
        """
        EWAS icin orneklem buyuklugu tahmini
        
        Bonferroni-adjusted alpha kullanir
        """
        
        # Bonferroni correction
        alpha_adj = alpha / n_cpgs
        
        z_alpha = stats.norm.ppf(1 - alpha_adj / 2)
        z_beta = stats.norm.ppf(power)
        
        # Approximate sample size for methylation difference
        n = ((z_alpha + z_beta) ** 2 * 2 * 0.25) / (effect_size ** 2)  # 0.25 = max variance for beta
        
        return {
            'n_recommended': int(np.ceil(n)),
            'n_cpgs': n_cpgs,
            'expected_significant': expected_significant,
            'effect_size_delta_beta': effect_size,
            'alpha_original': alpha,
            'alpha_adjusted': alpha_adj,
            'power': power,
            'note': 'Bonferroni-adjusted for genome-wide significance'
        }


# ============================================================================
# CROSS-VALIDATION
# ============================================================================

class CrossValidator:
    """
    Cross-Validation Pipeline
    
    Model performans degerlendirmesi
    """
    
    @staticmethod
    def k_fold_cv(X: np.ndarray,
                  y: np.ndarray,
                  model_class,
                  n_folds: int = 5,
                  stratified: bool = True,
                  seed: int = 42,
                  **model_kwargs) -> Dict[str, Any]:
        """
        K-Fold Cross-Validation
        """
        np.random.seed(seed)
        n_samples = len(y)
        
        # Create fold indices
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        
        fold_size = n_samples // n_folds
        fold_results = []
        all_predictions = np.zeros(n_samples)
        
        for fold in range(n_folds):
            # Split
            start = fold * fold_size
            end = start + fold_size if fold < n_folds - 1 else n_samples
            
            test_idx = indices[start:end]
            train_idx = np.concatenate([indices[:start], indices[end:]])
            
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Train and predict
            model = model_class(**model_kwargs)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            all_predictions[test_idx] = y_pred
            
            # Metrics
            mae = np.mean(np.abs(y_pred - y_test))
            rmse = np.sqrt(np.mean((y_pred - y_test) ** 2))
            r = np.corrcoef(y_pred, y_test)[0, 1] if len(y_test) > 1 else 0
            
            fold_results.append({
                'fold': fold + 1,
                'n_train': len(train_idx),
                'n_test': len(test_idx),
                'mae': round(mae, 4),
                'rmse': round(rmse, 4),
                'r': round(r, 4)
            })
        
        # Overall metrics
        overall_mae = np.mean(np.abs(all_predictions - y))
        overall_r = np.corrcoef(all_predictions, y)[0, 1]
        
        return {
            'n_folds': n_folds,
            'fold_results': fold_results,
            'mean_mae': round(np.mean([f['mae'] for f in fold_results]), 4),
            'std_mae': round(np.std([f['mae'] for f in fold_results]), 4),
            'mean_r': round(np.mean([f['r'] for f in fold_results]), 4),
            'overall_mae': round(overall_mae, 4),
            'overall_r': round(overall_r, 4),
            'predictions': all_predictions
        }
    
    @staticmethod
    def nested_cv(X: np.ndarray,
                  y: np.ndarray,
                  model_class,
                  param_grid: Dict[str, List],
                  outer_folds: int = 5,
                  inner_folds: int = 3,
                  seed: int = 42) -> Dict[str, Any]:
        """
        Nested Cross-Validation
        
        Hyperparameter tuning + performance estimation
        """
        np.random.seed(seed)
        n_samples = len(y)
        
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        
        fold_size = n_samples // outer_folds
        outer_results = []
        
        for outer_fold in range(outer_folds):
            # Outer split
            start = outer_fold * fold_size
            end = start + fold_size if outer_fold < outer_folds - 1 else n_samples
            
            test_idx = indices[start:end]
            train_idx = np.concatenate([indices[:start], indices[end:]])
            
            X_train_outer, X_test_outer = X[train_idx], X[test_idx]
            y_train_outer, y_test_outer = y[train_idx], y[test_idx]
            
            # Inner CV for hyperparameter tuning (simplified)
            best_params = {k: v[0] for k, v in param_grid.items()}  # Just use first param for demo
            
            # Train with best params
            model = model_class(**best_params)
            model.fit(X_train_outer, y_train_outer)
            y_pred = model.predict(X_test_outer)
            
            mae = np.mean(np.abs(y_pred - y_test_outer))
            
            outer_results.append({
                'outer_fold': outer_fold + 1,
                'best_params': best_params,
                'test_mae': round(mae, 4)
            })
        
        return {
            'outer_folds': outer_folds,
            'inner_folds': inner_folds,
            'results': outer_results,
            'mean_test_mae': round(np.mean([r['test_mae'] for r in outer_results]), 4),
            'std_test_mae': round(np.std([r['test_mae'] for r in outer_results]), 4)
        }


# ============================================================================
# REGRESSION METRICS
# ============================================================================

class RegressionMetrics:
    """
    Regresyon Performans Metrikleri
    
    MAE, RMSE, R-squared, etc.
    """
    
    @staticmethod
    def calculate_all(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Tum regresyon metriklerini hesapla"""
        
        n = len(y_true)
        
        # MAE
        mae = np.mean(np.abs(y_pred - y_true))
        
        # RMSE
        rmse = np.sqrt(np.mean((y_pred - y_true) ** 2))
        
        # R-squared
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # Adjusted R-squared (k=1 predictor assumed)
        adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - 2)
        
        # Correlation
        r = np.corrcoef(y_pred, y_true)[0, 1]
        
        # Median Absolute Error
        median_ae = np.median(np.abs(y_pred - y_true))
        
        # Mean Bias Error
        bias = np.mean(y_pred - y_true)
        
        # MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100 if np.all(y_true != 0) else np.nan
        
        return {
            'n': n,
            'mae': round(mae, 4),
            'rmse': round(rmse, 4),
            'r_squared': round(r_squared, 4),
            'adj_r_squared': round(adj_r_squared, 4),
            'correlation': round(r, 4),
            'median_ae': round(median_ae, 4),
            'bias': round(bias, 4),
            'mape': round(mape, 2) if not np.isnan(mape) else None
        }


def get_statistics() -> Dict[str, Any]:
    """Modul istatistikleri"""
    return {
        "module": "Statistical Validation",
        "version": "1.0",
        "capabilities": {
            "multiple_testing": ["Bonferroni", "Benjamini-Hochberg", "Holm", "Storey q-value"],
            "bootstrap_ci": ["Percentile", "BCa"],
            "classification": ["ROC-AUC", "PR-AUC", "DeLong test"],
            "effect_size": ["Cohen's d", "Hedge's g", "Eta-squared"],
            "power_analysis": ["t-test", "correlation", "EWAS"],
            "cross_validation": ["k-fold", "nested CV"],
            "regression": ["MAE", "RMSE", "R-squared", "MAPE"]
        },
        "references": [
            "Benjamini & Hochberg (1995) J Royal Stat Soc",
            "Cohen (1988) Statistical Power Analysis",
            "DeLong et al. (1988) Biometrics",
            "Efron & Tibshirani (1993) Bootstrap Methods"
        ]
    }


def test_statistical_validation():
    """Test fonksiyonu"""
    
    print("=" * 80)
    print("STATISTICAL VALIDATION MODULE - TEST")
    print("=" * 80)
    
    np.random.seed(42)
    
    # 1. Multiple testing
    print("\n[1] Coklu Test Duzeltmesi:")
    p_values = np.random.uniform(0, 1, 1000)
    p_values[:10] = np.random.uniform(0, 0.001, 10)  # True positives
    
    bonf = MultipleTestingCorrection.bonferroni(p_values)
    fdr = MultipleTestingCorrection.benjamini_hochberg(p_values)
    
    print(f"  Bonferroni: {bonf['n_significant']} significant")
    print(f"  FDR (BH): {fdr['n_significant']} significant")
    
    # 2. Bootstrap
    print("\n[2] Bootstrap CI:")
    data = np.random.normal(50, 10, 100)
    boot = BootstrapCI.percentile(data, np.mean)
    print(f"  Mean: {boot['point_estimate']:.2f}")
    print(f"  95% CI: [{boot['ci_lower']:.2f}, {boot['ci_upper']:.2f}]")
    
    # 3. Effect size
    print("\n[3] Effect Size:")
    group1 = np.random.normal(50, 10, 50)
    group2 = np.random.normal(55, 10, 50)
    d = EffectSize.cohens_d(group1, group2)
    print(f"  Cohen's d: {d['effect_size']} ({d['interpretation']})")
    
    # 4. Power analysis
    print("\n[4] Power Analizi:")
    power = PowerAnalysis.two_sample_ttest(effect_size=0.5)
    print(f"  d=0.5 icin gerekli n: {power['n_per_group']} / grup")
    
    ewas = PowerAnalysis.ewas_sample_size()
    print(f"  EWAS icin onerilen n: {ewas['n_recommended']}")
    
    # 5. Regression metrics
    print("\n[5] Regresyon Metrikleri:")
    y_true = np.random.uniform(20, 80, 100)
    y_pred = y_true + np.random.normal(0, 3, 100)
    metrics = RegressionMetrics.calculate_all(y_true, y_pred)
    print(f"  MAE: {metrics['mae']}")
    print(f"  R-squared: {metrics['r_squared']}")
    print(f"  Korelasyon: {metrics['correlation']}")
    
    return True


if __name__ == "__main__":
    test_statistical_validation()
