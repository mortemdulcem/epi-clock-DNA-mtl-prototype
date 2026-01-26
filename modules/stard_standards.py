"""
STARD (Standards for Reporting of Diagnostic Accuracy Studies)
EpiClock v4.0 - Publication Ready

Implements:
- STARD 2015 checklist
- Diagnostic accuracy metrics
- Sensitivity/Specificity analysis
- ROC curve analysis for diagnostics
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from scipy import stats


@dataclass
class STARDChecklist:
    """STARD 2015 Checklist for Diagnostic Accuracy Studies"""
    
    CHECKLIST_ITEMS = {
        'title_abstract': [
            ('TA1', 'Identify as diagnostic accuracy study in title/abstract', True),
            ('TA2', 'Provide structured summary including STARD items', True)
        ],
        'introduction': [
            ('IN1', 'Scientific and clinical background', True),
            ('IN2', 'Study objectives and hypotheses', True)
        ],
        'methods_participants': [
            ('MP1', 'Whether data collection was prospective or retrospective', True),
            ('MP2', 'Eligibility criteria', True),
            ('MP3', 'How and where participants were identified', True),
            ('MP4', 'Intended sample size and how it was determined', True)
        ],
        'methods_test': [
            ('MT1', 'Index test methods in detail to allow replication', True),
            ('MT2', 'Reference standard and rationale', True),
            ('MT3', 'Definition of positive/negative results', True),
            ('MT4', 'Number, training, expertise of test readers', False),
            ('MT5', 'Whether readers were blinded', True)
        ],
        'methods_analysis': [
            ('MA1', 'Methods for calculating diagnostic accuracy', True),
            ('MA2', 'How indeterminate results were handled', True),
            ('MA3', 'How missing data were handled', True),
            ('MA4', 'Any analyses of variability', False),
            ('MA5', 'Intended subgroup analyses', False)
        ],
        'results_participants': [
            ('RP1', 'Flow of participants with diagram', True),
            ('RP2', 'Baseline demographic characteristics', True),
            ('RP3', 'Time interval between index test and reference', True)
        ],
        'results_test': [
            ('RT1', 'Cross tabulation of index test vs reference', True),
            ('RT2', 'Estimates of diagnostic accuracy with CIs', True),
            ('RT3', 'Indeterminate results distribution', False),
            ('RT4', 'Adverse events from testing', False)
        ],
        'discussion': [
            ('DI1', 'Study limitations', True),
            ('DI2', 'Implications for practice', True),
            ('DI3', 'Generalizability of results', True)
        ]
    }
    
    def __init__(self):
        self.completed = {}
        self.notes = {}
        for category in self.CHECKLIST_ITEMS:
            for item_id, _, _ in self.CHECKLIST_ITEMS[category]:
                self.completed[item_id] = False
                self.notes[item_id] = ""
    
    def mark_complete(self, item_id: str, notes: str = ""):
        """Mark checklist item as complete"""
        if item_id in self.completed:
            self.completed[item_id] = True
            self.notes[item_id] = notes
    
    def get_compliance_status(self) -> Dict:
        """Get STARD compliance status"""
        required = []
        for category, items in self.CHECKLIST_ITEMS.items():
            for item_id, _, is_required in items:
                if is_required:
                    required.append(item_id)
        
        completed_required = sum(1 for i in required if self.completed.get(i, False))
        
        return {
            'required_completed': completed_required,
            'required_total': len(required),
            'compliance_percentage': completed_required / len(required) * 100 if required else 0,
            'is_compliant': completed_required == len(required)
        }
    
    def generate_report(self) -> str:
        """Generate STARD compliance report"""
        status = self.get_compliance_status()
        
        report = []
        report.append("=" * 60)
        report.append("STARD 2015 CHECKLIST COMPLIANCE REPORT")
        report.append("Standards for Reporting Diagnostic Accuracy Studies")
        report.append("=" * 60)
        
        compliance = "COMPLIANT" if status['is_compliant'] else "NOT COMPLIANT"
        report.append(f"\nStatus: {compliance}")
        report.append(f"Required Items: {status['required_completed']}/{status['required_total']}")
        report.append(f"Compliance: {status['compliance_percentage']:.1f}%")
        
        for category, items in self.CHECKLIST_ITEMS.items():
            report.append(f"\n{category.upper().replace('_', ' ')}")
            report.append("-" * 40)
            for item_id, description, is_required in items:
                check = "[X]" if self.completed.get(item_id, False) else "[ ]"
                req = "*" if is_required else " "
                report.append(f"  {check}{req} {item_id}: {description[:50]}")
        
        return "\n".join(report)


@dataclass
class DiagnosticAccuracyCalculator:
    """Calculate diagnostic accuracy metrics"""
    
    def __init__(self):
        self.results = {}
    
    def calculate_from_contingency(self,
                                    true_positive: int,
                                    false_positive: int,
                                    true_negative: int,
                                    false_negative: int) -> Dict:
        """Calculate all diagnostic metrics from 2x2 table"""
        tp, fp, tn, fn = true_positive, false_positive, true_negative, false_negative
        total = tp + fp + tn + fn
        
        # Basic metrics
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        ppv = tp / (tp + fp) if (tp + fp) > 0 else 0  # Positive predictive value
        npv = tn / (tn + fn) if (tn + fn) > 0 else 0  # Negative predictive value
        
        # Additional metrics
        accuracy = (tp + tn) / total if total > 0 else 0
        prevalence = (tp + fn) / total if total > 0 else 0
        
        # Likelihood ratios
        lr_positive = sensitivity / (1 - specificity) if (1 - specificity) > 0 else float('inf')
        lr_negative = (1 - sensitivity) / specificity if specificity > 0 else float('inf')
        
        # Diagnostic odds ratio
        dor = (tp * tn) / (fp * fn) if (fp * fn) > 0 else float('inf')
        
        # Youden's J statistic
        youden_j = sensitivity + specificity - 1
        
        # F1 score
        f1 = 2 * (ppv * sensitivity) / (ppv + sensitivity) if (ppv + sensitivity) > 0 else 0
        
        # Confidence intervals (Wilson score interval)
        def wilson_ci(p, n, z=1.96):
            if n == 0:
                return (0, 0)
            denominator = 1 + z**2 / n
            center = (p + z**2 / (2 * n)) / denominator
            margin = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denominator
            return (max(0, center - margin), min(1, center + margin))
        
        sens_ci = wilson_ci(sensitivity, tp + fn)
        spec_ci = wilson_ci(specificity, tn + fp)
        
        results = {
            'sensitivity': sensitivity,
            'sensitivity_ci': sens_ci,
            'specificity': specificity,
            'specificity_ci': spec_ci,
            'ppv': ppv,
            'npv': npv,
            'accuracy': accuracy,
            'prevalence': prevalence,
            'lr_positive': lr_positive,
            'lr_negative': lr_negative,
            'diagnostic_odds_ratio': dor,
            'youden_j': youden_j,
            'f1_score': f1,
            'contingency_table': {
                'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn
            }
        }
        
        self.results = results
        return results
    
    def calculate_from_arrays(self,
                               predicted: np.ndarray,
                               actual: np.ndarray,
                               threshold: float = 0.5) -> Dict:
        """Calculate metrics from prediction arrays"""
        pred_binary = (predicted >= threshold).astype(int)
        
        tp = np.sum((pred_binary == 1) & (actual == 1))
        fp = np.sum((pred_binary == 1) & (actual == 0))
        tn = np.sum((pred_binary == 0) & (actual == 0))
        fn = np.sum((pred_binary == 0) & (actual == 1))
        
        return self.calculate_from_contingency(tp, fp, tn, fn)
    
    def generate_report(self) -> str:
        """Generate diagnostic accuracy report"""
        if not self.results:
            return "No results calculated yet."
        
        r = self.results
        
        report = []
        report.append("=" * 60)
        report.append("DIAGNOSTIC ACCURACY REPORT")
        report.append("=" * 60)
        
        report.append("\n2x2 CONTINGENCY TABLE")
        report.append("-" * 40)
        ct = r['contingency_table']
        report.append(f"                    Disease+    Disease-")
        report.append(f"  Test+             {ct['tp']:>8}    {ct['fp']:>8}")
        report.append(f"  Test-             {ct['fn']:>8}    {ct['tn']:>8}")
        
        report.append("\nPRIMARY METRICS")
        report.append("-" * 40)
        report.append(f"  Sensitivity: {r['sensitivity']:.3f} (95% CI: {r['sensitivity_ci'][0]:.3f}-{r['sensitivity_ci'][1]:.3f})")
        report.append(f"  Specificity: {r['specificity']:.3f} (95% CI: {r['specificity_ci'][0]:.3f}-{r['specificity_ci'][1]:.3f})")
        report.append(f"  PPV: {r['ppv']:.3f}")
        report.append(f"  NPV: {r['npv']:.3f}")
        report.append(f"  Accuracy: {r['accuracy']:.3f}")
        
        report.append("\nADDITIONAL METRICS")
        report.append("-" * 40)
        report.append(f"  LR+: {r['lr_positive']:.2f}")
        report.append(f"  LR-: {r['lr_negative']:.3f}")
        report.append(f"  DOR: {r['diagnostic_odds_ratio']:.2f}")
        report.append(f"  Youden's J: {r['youden_j']:.3f}")
        report.append(f"  F1 Score: {r['f1_score']:.3f}")
        report.append(f"  Prevalence: {r['prevalence']:.3f}")
        
        return "\n".join(report)


@dataclass
class ROCAnalyzer:
    """ROC curve analysis for diagnostic tests"""
    
    def __init__(self):
        self.roc_data = None
        self.auc = None
    
    def calculate_roc(self,
                      scores: np.ndarray,
                      labels: np.ndarray) -> Dict:
        """Calculate ROC curve data"""
        # Sort by score descending
        sorted_indices = np.argsort(-scores)
        sorted_labels = labels[sorted_indices]
        sorted_scores = scores[sorted_indices]
        
        # Get unique thresholds
        thresholds = np.unique(sorted_scores)
        thresholds = np.concatenate([[thresholds[0] + 1], thresholds, [thresholds[-1] - 1]])
        
        tpr_list = []
        fpr_list = []
        
        total_positives = np.sum(labels == 1)
        total_negatives = np.sum(labels == 0)
        
        for thresh in thresholds:
            predictions = (scores >= thresh).astype(int)
            
            tp = np.sum((predictions == 1) & (labels == 1))
            fp = np.sum((predictions == 1) & (labels == 0))
            
            tpr = tp / total_positives if total_positives > 0 else 0
            fpr = fp / total_negatives if total_negatives > 0 else 0
            
            tpr_list.append(tpr)
            fpr_list.append(fpr)
        
        tpr_array = np.array(tpr_list)
        fpr_array = np.array(fpr_list)
        
        # Calculate AUC using trapezoidal rule
        sorted_idx = np.argsort(fpr_array)
        fpr_sorted = fpr_array[sorted_idx]
        tpr_sorted = tpr_array[sorted_idx]
        
        auc = np.trapz(tpr_sorted, fpr_sorted)
        
        self.roc_data = {
            'fpr': fpr_array,
            'tpr': tpr_array,
            'thresholds': thresholds
        }
        self.auc = auc
        
        # Find optimal threshold (Youden's J)
        youden_j = tpr_array - fpr_array
        optimal_idx = np.argmax(youden_j)
        optimal_threshold = thresholds[optimal_idx]
        
        return {
            'auc': auc,
            'auc_ci': self._bootstrap_auc_ci(scores, labels),
            'optimal_threshold': optimal_threshold,
            'optimal_sensitivity': tpr_array[optimal_idx],
            'optimal_specificity': 1 - fpr_array[optimal_idx],
            'n_thresholds': len(thresholds)
        }
    
    def _bootstrap_auc_ci(self, scores: np.ndarray, labels: np.ndarray, 
                          n_bootstrap: int = 1000, alpha: float = 0.05) -> Tuple[float, float]:
        """Calculate bootstrap confidence interval for AUC"""
        np.random.seed(42)
        n = len(scores)
        bootstrap_aucs = []
        
        for _ in range(n_bootstrap):
            indices = np.random.choice(n, size=n, replace=True)
            boot_scores = scores[indices]
            boot_labels = labels[indices]
            
            # Quick AUC calculation
            pos_scores = boot_scores[boot_labels == 1]
            neg_scores = boot_scores[boot_labels == 0]
            
            if len(pos_scores) == 0 or len(neg_scores) == 0:
                continue
            
            auc = np.mean([s1 > s2 for s1 in pos_scores for s2 in neg_scores])
            bootstrap_aucs.append(auc)
        
        if len(bootstrap_aucs) == 0:
            return (0.5, 0.5)
        
        ci_lower = np.percentile(bootstrap_aucs, alpha/2 * 100)
        ci_upper = np.percentile(bootstrap_aucs, (1 - alpha/2) * 100)
        
        return (ci_lower, ci_upper)
    
    def compare_auc_delong(self,
                           scores1: np.ndarray,
                           scores2: np.ndarray,
                           labels: np.ndarray) -> Dict:
        """Compare two AUCs using DeLong test (simplified)"""
        # Calculate AUCs
        auc1 = self._calculate_auc_simple(scores1, labels)
        auc2 = self._calculate_auc_simple(scores2, labels)
        
        # Simplified comparison (bootstrap-based)
        np.random.seed(42)
        n = len(labels)
        diff_bootstrap = []
        
        for _ in range(1000):
            indices = np.random.choice(n, size=n, replace=True)
            boot_auc1 = self._calculate_auc_simple(scores1[indices], labels[indices])
            boot_auc2 = self._calculate_auc_simple(scores2[indices], labels[indices])
            diff_bootstrap.append(boot_auc1 - boot_auc2)
        
        diff_bootstrap = np.array(diff_bootstrap)
        se = np.std(diff_bootstrap)
        z_stat = (auc1 - auc2) / se if se > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        return {
            'auc1': auc1,
            'auc2': auc2,
            'difference': auc1 - auc2,
            'z_statistic': z_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    def _calculate_auc_simple(self, scores: np.ndarray, labels: np.ndarray) -> float:
        """Simple AUC calculation"""
        pos_scores = scores[labels == 1]
        neg_scores = scores[labels == 0]
        
        if len(pos_scores) == 0 or len(neg_scores) == 0:
            return 0.5
        
        return np.mean([s1 > s2 for s1 in pos_scores for s2 in neg_scores])
    
    def generate_report(self) -> str:
        """Generate ROC analysis report"""
        if self.auc is None:
            return "No ROC analysis performed yet."
        
        report = []
        report.append("=" * 60)
        report.append("ROC CURVE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"\nAUC: {self.auc:.4f}")
        report.append(f"Number of thresholds evaluated: {len(self.roc_data['thresholds'])}")
        
        return "\n".join(report)


def test_stard_standards():
    """Test STARD standards module"""
    print("=" * 60)
    print("STARD STANDARDS MODULE - TEST")
    print("=" * 60)
    
    # Test STARD Checklist
    print("\n[1] STARD Checklist:")
    checklist = STARDChecklist()
    checklist.mark_complete('TA1', 'Diagnostic accuracy of methylation markers')
    checklist.mark_complete('IN1', 'Epigenetic markers for SUD detection')
    checklist.mark_complete('MP1', 'Retrospective cohort study')
    checklist.mark_complete('MT1', 'Illumina EPIC array')
    status = checklist.get_compliance_status()
    print(f"  Compliance: {status['compliance_percentage']:.1f}%")
    
    # Test Diagnostic Accuracy Calculator
    print("\n[2] Diagnostic Accuracy:")
    calculator = DiagnosticAccuracyCalculator()
    results = calculator.calculate_from_contingency(
        true_positive=85,
        false_positive=15,
        true_negative=90,
        false_negative=10
    )
    print(f"  Sensitivity: {results['sensitivity']:.3f}")
    print(f"  Specificity: {results['specificity']:.3f}")
    print(f"  AUC equivalent (Youden's J / 2 + 0.5): {results['youden_j']/2 + 0.5:.3f}")
    
    # Test from arrays
    print("\n[3] Metrics from Arrays:")
    np.random.seed(42)
    scores = np.random.uniform(0, 1, 200)
    labels = (scores + np.random.normal(0, 0.3, 200) > 0.5).astype(int)
    
    array_results = calculator.calculate_from_arrays(scores, labels, threshold=0.5)
    print(f"  Accuracy: {array_results['accuracy']:.3f}")
    print(f"  F1 Score: {array_results['f1_score']:.3f}")
    
    # Test ROC Analyzer
    print("\n[4] ROC Analysis:")
    roc_analyzer = ROCAnalyzer()
    roc_results = roc_analyzer.calculate_roc(scores, labels)
    print(f"  AUC: {roc_results['auc']:.4f}")
    print(f"  95% CI: [{roc_results['auc_ci'][0]:.4f}, {roc_results['auc_ci'][1]:.4f}]")
    print(f"  Optimal threshold: {roc_results['optimal_threshold']:.4f}")
    
    # Test AUC comparison
    print("\n[5] AUC Comparison (DeLong-like):")
    scores2 = np.random.uniform(0, 1, 200)
    comparison = roc_analyzer.compare_auc_delong(scores, scores2, labels)
    print(f"  AUC difference: {comparison['difference']:.4f}")
    print(f"  P-value: {comparison['p_value']:.4f}")
    print(f"  Significant: {comparison['significant']}")
    
    print("\n" + "=" * 60)
    print("STARD Standards Test Complete")


if __name__ == "__main__":
    test_stard_standards()
