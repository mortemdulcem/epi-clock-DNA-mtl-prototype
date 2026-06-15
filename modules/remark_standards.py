"""
REMARK (REporting recommendations for tumour MARKer prognostic studies)
EpiClock v4.0 - Publication Ready

Implements:
- REMARK checklist for biomarker studies
- Prognostic model validation standards
- Biomarker cutoff determination
- Survival analysis reporting
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from scipy import stats


@dataclass
class REMARKChecklist:
    """REMARK Checklist for Biomarker Studies"""
    
    CHECKLIST_ITEMS = {
        'introduction': [
            ('I1', 'State the marker examined, study objectives, and hypotheses', True)
        ],
        'materials_methods': [
            ('M1', 'Describe patient characteristics (inclusion/exclusion criteria)', True),
            ('M2', 'Describe type of biological material used', True),
            ('M3', 'Describe how biological material was obtained', True),
            ('M4', 'Describe assay method used and quality controls', True),
            ('M5', 'Describe handling of marker measurements in analyses', True),
            ('M6', 'Describe rationale for cutpoints (if used)', True),
            ('M7', 'Describe assay reproducibility assessments', True)
        ],
        'results_patients': [
            ('R1', 'Report patient characteristics', True),
            ('R2', 'Report number of patients available for each analysis', True),
            ('R3', 'Report distributions of basic characteristics', True),
            ('R4', 'Report length of follow-up', True),
            ('R5', 'Report number of events', True)
        ],
        'results_marker': [
            ('B1', 'Report distributions of marker values', True),
            ('B2', 'Report univariate analyses with confidence intervals', True),
            ('B3', 'Report multivariate analyses with confidence intervals', True),
            ('B4', 'Report interaction of marker with standard factors', False),
            ('B5', 'Report estimated effects with confidence intervals', True)
        ],
        'discussion': [
            ('D1', 'Interpret results in context of existing evidence', True),
            ('D2', 'Discuss implications for future research', True),
            ('D3', 'Discuss limitations of study', True)
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
        """Get REMARK compliance status"""
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
        """Generate REMARK compliance report"""
        status = self.get_compliance_status()
        
        report = []
        report.append("=" * 60)
        report.append("REMARK CHECKLIST COMPLIANCE REPORT")
        report.append("Reporting Recommendations for Tumor Marker Prognostic Studies")
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
class BiomarkerCutoffDetermination:
    """Methods for determining biomarker cutoffs"""
    
    METHODS = {
        'median': 'Median split',
        'tertile': 'Tertile split',
        'quartile': 'Quartile split',
        'optimal': 'Optimal cutpoint (maxstat)',
        'clinical': 'Clinical threshold',
        'roc': 'ROC-based optimal cutpoint'
    }
    
    def __init__(self):
        self.cutoffs = {}
    
    def determine_cutoff(self,
                         marker_values: np.ndarray,
                         method: str = 'median',
                         outcome: np.ndarray = None) -> Dict:
        """Determine biomarker cutoff using specified method"""
        
        if method == 'median':
            cutoff = np.median(marker_values)
            high_group = marker_values >= cutoff
            
        elif method == 'tertile':
            cutoffs = np.percentile(marker_values, [33.33, 66.67])
            cutoff = cutoffs  # Returns array
            high_group = marker_values >= cutoffs[1]
            
        elif method == 'quartile':
            cutoffs = np.percentile(marker_values, [25, 50, 75])
            cutoff = cutoffs
            high_group = marker_values >= cutoffs[2]
            
        elif method == 'optimal' and outcome is not None:
            # Simple optimal cutpoint search (maxstat-like)
            cutoff, _ = self._find_optimal_cutpoint(marker_values, outcome)
            high_group = marker_values >= cutoff
            
        elif method == 'roc' and outcome is not None:
            cutoff = self._find_roc_cutpoint(marker_values, outcome)
            high_group = marker_values >= cutoff
            
        else:
            cutoff = np.median(marker_values)
            high_group = marker_values >= cutoff
        
        result = {
            'method': self.METHODS.get(method, method),
            'cutoff': cutoff,
            'n_high': int(np.sum(high_group)),
            'n_low': int(np.sum(~high_group)),
            'percentage_high': float(np.mean(high_group) * 100)
        }
        
        return result
    
    def _find_optimal_cutpoint(self, marker: np.ndarray, outcome: np.ndarray) -> Tuple[float, float]:
        """Find optimal cutpoint using log-rank-like statistic"""
        sorted_markers = np.sort(np.unique(marker))
        best_stat = 0
        best_cutoff = np.median(marker)
        
        for cutoff in sorted_markers[1:-1]:
            high = marker >= cutoff
            low = ~high
            
            if np.sum(high) < 5 or np.sum(low) < 5:
                continue
            
            # Simple chi-square as proxy for log-rank
            observed_high = np.sum(outcome[high])
            expected_high = np.sum(outcome) * np.mean(high)
            
            if expected_high > 0:
                stat = (observed_high - expected_high) ** 2 / expected_high
                if stat > best_stat:
                    best_stat = stat
                    best_cutoff = cutoff
        
        return best_cutoff, best_stat
    
    def _find_roc_cutpoint(self, marker: np.ndarray, outcome: np.ndarray) -> float:
        """Find optimal cutpoint using Youden's J statistic"""
        sorted_markers = np.sort(np.unique(marker))
        best_j = 0
        best_cutoff = np.median(marker)
        
        for cutoff in sorted_markers:
            pred = marker >= cutoff
            tp = np.sum((pred == 1) & (outcome == 1))
            tn = np.sum((pred == 0) & (outcome == 0))
            fp = np.sum((pred == 1) & (outcome == 0))
            fn = np.sum((pred == 0) & (outcome == 1))
            
            sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            
            j = sensitivity + specificity - 1
            if j > best_j:
                best_j = j
                best_cutoff = cutoff
        
        return best_cutoff
    
    def generate_cutoff_report(self, result: Dict) -> str:
        """Generate cutoff determination report"""
        report = []
        report.append("BIOMARKER CUTOFF DETERMINATION")
        report.append("=" * 40)
        report.append(f"Method: {result['method']}")
        
        if isinstance(result['cutoff'], np.ndarray):
            report.append(f"Cutoffs: {', '.join([f'{c:.4f}' for c in result['cutoff']])}")
        else:
            report.append(f"Cutoff: {result['cutoff']:.4f}")
        
        report.append(f"High group: n={result['n_high']} ({result['percentage_high']:.1f}%)")
        report.append(f"Low group: n={result['n_low']} ({100 - result['percentage_high']:.1f}%)")
        
        return "\n".join(report)


@dataclass
class PrognosticModelValidation:
    """Prognostic model validation standards"""
    
    def __init__(self):
        self.validation_results = {}
    
    def calculate_c_index(self,
                          predicted_risk: np.ndarray,
                          survival_time: np.ndarray,
                          event: np.ndarray) -> Dict:
        """
        Calculate concordance index (C-index)
        Simplified version - in production use lifelines or similar
        """
        n = len(predicted_risk)
        concordant = 0
        discordant = 0
        tied = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if event[i] == 1 and event[j] == 1:
                    if survival_time[i] < survival_time[j]:
                        if predicted_risk[i] > predicted_risk[j]:
                            concordant += 1
                        elif predicted_risk[i] < predicted_risk[j]:
                            discordant += 1
                        else:
                            tied += 1
        
        total = concordant + discordant + tied
        c_index = (concordant + 0.5 * tied) / total if total > 0 else 0.5
        
        return {
            'c_index': c_index,
            'concordant': concordant,
            'discordant': discordant,
            'tied': tied,
            'interpretation': self._interpret_c_index(c_index)
        }
    
    def _interpret_c_index(self, c_index: float) -> str:
        """Interpret C-index value"""
        if c_index >= 0.9:
            return "Excellent discrimination"
        elif c_index >= 0.8:
            return "Good discrimination"
        elif c_index >= 0.7:
            return "Acceptable discrimination"
        elif c_index >= 0.6:
            return "Poor discrimination"
        else:
            return "No discrimination"
    
    def bootstrap_validation(self,
                             predicted: np.ndarray,
                             actual: np.ndarray,
                             n_bootstrap: int = 1000,
                             metric: str = 'c_index') -> Dict:
        """Bootstrap validation of model performance"""
        np.random.seed(42)
        n = len(predicted)
        bootstrap_metrics = []
        
        for _ in range(n_bootstrap):
            indices = np.random.choice(n, size=n, replace=True)
            boot_pred = predicted[indices]
            boot_actual = actual[indices]
            
            if metric == 'auc':
                # Simple AUC approximation
                from sklearn.metrics import roc_auc_score
                try:
                    auc = roc_auc_score(boot_actual, boot_pred)
                    bootstrap_metrics.append(auc)
                except:
                    pass
            else:
                # Correlation as proxy
                corr = np.corrcoef(boot_pred, boot_actual)[0, 1]
                bootstrap_metrics.append(corr)
        
        bootstrap_metrics = np.array(bootstrap_metrics)
        
        return {
            'original': float(np.corrcoef(predicted, actual)[0, 1]),
            'bootstrap_mean': float(np.mean(bootstrap_metrics)),
            'bootstrap_se': float(np.std(bootstrap_metrics)),
            'ci_lower': float(np.percentile(bootstrap_metrics, 2.5)),
            'ci_upper': float(np.percentile(bootstrap_metrics, 97.5)),
            'optimism': float(np.mean(bootstrap_metrics) - np.corrcoef(predicted, actual)[0, 1])
        }
    
    def calibration_analysis(self,
                              predicted_prob: np.ndarray,
                              actual_outcome: np.ndarray,
                              n_groups: int = 10) -> Dict:
        """Assess model calibration"""
        # Divide into deciles
        percentiles = np.percentile(predicted_prob, np.linspace(0, 100, n_groups + 1))
        
        observed = []
        expected = []
        
        for i in range(n_groups):
            mask = (predicted_prob >= percentiles[i]) & (predicted_prob < percentiles[i + 1])
            if i == n_groups - 1:
                mask = (predicted_prob >= percentiles[i]) & (predicted_prob <= percentiles[i + 1])
            
            if np.sum(mask) > 0:
                observed.append(np.mean(actual_outcome[mask]))
                expected.append(np.mean(predicted_prob[mask]))
        
        observed = np.array(observed)
        expected = np.array(expected)
        
        # Hosmer-Lemeshow-like statistic
        hl_stat = np.sum((observed - expected) ** 2 / (expected * (1 - expected) + 1e-10))
        
        # Calibration slope
        if len(expected) > 1:
            slope, intercept = np.polyfit(expected, observed, 1)
        else:
            slope, intercept = 1.0, 0.0
        
        return {
            'calibration_slope': float(slope),
            'calibration_intercept': float(intercept),
            'hosmer_lemeshow_stat': float(hl_stat),
            'observed_expected_ratio': float(np.sum(observed) / np.sum(expected)) if np.sum(expected) > 0 else 1.0,
            'well_calibrated': abs(slope - 1) < 0.2 and abs(intercept) < 0.1
        }
    
    def generate_validation_report(self) -> str:
        """Generate validation report"""
        report = []
        report.append("=" * 60)
        report.append("PROGNOSTIC MODEL VALIDATION REPORT")
        report.append("=" * 60)
        
        for name, results in self.validation_results.items():
            report.append(f"\n{name}")
            report.append("-" * 40)
            for key, value in results.items():
                if isinstance(value, float):
                    report.append(f"  {key}: {value:.4f}")
                else:
                    report.append(f"  {key}: {value}")
        
        return "\n".join(report)


def test_remark_standards():
    """Test REMARK standards module"""
    print("=" * 60)
    print("REMARK STANDARDS MODULE - TEST")
    print("=" * 60)
    
    # Test REMARK Checklist
    print("\n[1] REMARK Checklist:")
    checklist = REMARKChecklist()
    checklist.mark_complete('I1', 'DNA methylation as addiction biomarker')
    checklist.mark_complete('M1', 'SUD patients vs healthy controls')
    checklist.mark_complete('M2', 'Whole blood DNA')
    checklist.mark_complete('B1', 'Methylation beta values')
    status = checklist.get_compliance_status()
    print(f"  Compliance: {status['compliance_percentage']:.1f}%")
    
    # Test Cutoff Determination
    print("\n[2] Biomarker Cutoff Determination:")
    np.random.seed(42)
    marker_values = np.random.normal(0.5, 0.1, 100)
    outcome = (marker_values > 0.5).astype(int)
    
    cutoff_analyzer = BiomarkerCutoffDetermination()
    median_cutoff = cutoff_analyzer.determine_cutoff(marker_values, 'median')
    print(f"  Median cutoff: {median_cutoff['cutoff']:.4f}")
    
    optimal_cutoff = cutoff_analyzer.determine_cutoff(marker_values, 'optimal', outcome)
    print(f"  Optimal cutoff: {optimal_cutoff['cutoff']:.4f}")
    
    # Test Model Validation
    print("\n[3] Prognostic Model Validation:")
    predicted = np.random.uniform(0, 1, 100)
    actual = (predicted + np.random.normal(0, 0.2, 100) > 0.5).astype(int)
    
    validator = PrognosticModelValidation()
    
    # Bootstrap validation
    boot_results = validator.bootstrap_validation(predicted, actual.astype(float))
    print(f"  Bootstrap mean: {boot_results['bootstrap_mean']:.4f}")
    print(f"  95% CI: [{boot_results['ci_lower']:.4f}, {boot_results['ci_upper']:.4f}]")
    
    # Calibration
    calibration = validator.calibration_analysis(predicted, actual)
    print(f"  Calibration slope: {calibration['calibration_slope']:.4f}")
    print(f"  Well calibrated: {calibration['well_calibrated']}")
    
    print("\n" + "=" * 60)
    print("REMARK Standards Test Complete")


if __name__ == "__main__":
    test_remark_standards()
