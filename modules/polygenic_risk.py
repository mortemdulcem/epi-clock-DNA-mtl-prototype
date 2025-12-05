# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
Polygenic Risk Score (PRS) Module
Disease and trait risk prediction based on multiple genetic variants

Applications:
- Addiction susceptibility prediction
- Substance-specific risk assessment
- Treatment response prediction
- Mental health comorbidity risk

Uses publicly available GWAS summary statistics - FREE

Author: Dr. Nurcan Denli Bayır
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
# nrcdnl94
class PRSResult:
    # nrcdnl94
    """Polygenic risk score result"""
    trait: str
    score: float
    percentile: float
    risk_category: str
    n_variants: int
    interpretation: str


GWAS_SUMMARY_STATS = {
    # nrcdnl94
    'alcohol_dependence': {
        'source': 'MVP/GSCAN 2019',
        'n_samples': 274424,
        'n_variants': 99,
        'snps': {
            'rs1229984': {'beta': -0.82, 'p': 5e-100, 'gene': 'ADH1B'},
            'rs671': {'beta': -0.65, 'p': 1e-80, 'gene': 'ALDH2'},
            'rs1800497': {'beta': 0.12, 'p': 2e-8, 'gene': 'DRD2'},
            'rs1799971': {'beta': 0.08, 'p': 5e-6, 'gene': 'OPRM1'},
            'rs6265': {'beta': 0.06, 'p': 3e-5, 'gene': 'BDNF'},
            'rs4680': {'beta': 0.05, 'p': 8e-5, 'gene': 'COMT'},
        },
        'population_mean': 0.0,
        'population_sd': 1.0,
        'heritability': 0.49
    },
    'opioid_dependence': {
        'source': 'MVP 2020',
        'n_samples': 82707,
        'n_variants': 25,
        'snps': {
            'rs1799971': {'beta': 0.15, 'p': 2e-12, 'gene': 'OPRM1'},
            'rs2236861': {'beta': 0.09, 'p': 5e-8, 'gene': 'OPRD1'},
            'rs1800497': {'beta': 0.11, 'p': 1e-7, 'gene': 'DRD2'},
            'rs4680': {'beta': 0.07, 'p': 3e-6, 'gene': 'COMT'},
            'rs25531': {'beta': 0.06, 'p': 8e-5, 'gene': 'SLC6A4'},
        },
        'population_mean': 0.0,
        'population_sd': 1.0,
        'heritability': 0.43
    },
    'cocaine_dependence': {
        'source': 'PGC 2018',
        'n_samples': 15000,
        'n_variants': 15,
        'snps': {
            'rs1800497': {'beta': 0.18, 'p': 2e-9, 'gene': 'DRD2'},
            'rs27072': {'beta': 0.12, 'p': 5e-7, 'gene': 'DAT1'},
            'rs4680': {'beta': 0.09, 'p': 1e-5, 'gene': 'COMT'},
            'rs6265': {'beta': 0.07, 'p': 8e-5, 'gene': 'BDNF'},
        },
        'population_mean': 0.0,
        'population_sd': 1.0,
        'heritability': 0.65
    },
    'cannabis_use_disorder': {
        'source': 'iPSYCH/PGC 2020',
        'n_samples': 184765,
        'n_variants': 35,
        'snps': {
            'rs56372821': {'beta': 0.08, 'p': 2e-15, 'gene': 'CHRNA2'},
            'rs1800497': {'beta': 0.06, 'p': 3e-8, 'gene': 'DRD2'},
            'rs4680': {'beta': 0.05, 'p': 5e-6, 'gene': 'COMT'},
        },
        'population_mean': 0.0,
        'population_sd': 1.0,
        'heritability': 0.51
    },
    'nicotine_dependence': {
        'source': 'GSCAN 2019',
        'n_samples': 1232091,
        'n_variants': 378,
        'snps': {
            'rs16969968': {'beta': 0.25, 'p': 1e-200, 'gene': 'CHRNA5'},
            'rs1051730': {'beta': 0.22, 'p': 5e-180, 'gene': 'CHRNA3'},
            'rs4680': {'beta': 0.04, 'p': 2e-10, 'gene': 'COMT'},
            'rs1800497': {'beta': 0.03, 'p': 5e-8, 'gene': 'DRD2'},
        },
        'population_mean': 0.0,
        'population_sd': 1.0,
        'heritability': 0.50
    },
    'depression': {
        'source': 'PGC MDD 2019',
        'n_samples': 807553,
        'n_variants': 102,
        'snps': {
            'rs25531': {'beta': 0.05, 'p': 5e-30, 'gene': 'SLC6A4'},
            'rs6265': {'beta': 0.04, 'p': 2e-20, 'gene': 'BDNF'},
            'rs4680': {'beta': 0.03, 'p': 1e-12, 'gene': 'COMT'},
        },
        'population_mean': 0.0,
        'population_sd': 1.0,
        'heritability': 0.37
    },
    'anxiety': {
        'source': 'MVP 2020',
        'n_samples': 200000,
        'n_variants': 45,
        'snps': {
            'rs25531': {'beta': 0.06, 'p': 2e-15, 'gene': 'SLC6A4'},
            'rs4680': {'beta': 0.04, 'p': 5e-10, 'gene': 'COMT'},
            'rs6265': {'beta': 0.03, 'p': 1e-8, 'gene': 'BDNF'},
        },
        'population_mean': 0.0,
        'population_sd': 1.0,
        'heritability': 0.31
    }
}


class PolygenicRiskScoreCalculator:
    # nrcdnl94
    """
    Calculate Polygenic Risk Scores for addiction and related traits
    
    PRS = Σ(β × genotype dosage)
    
    Where:
    - β = effect size from GWAS
    - genotype dosage = 0, 1, or 2 (copies of risk allele)
    
    All GWAS summary statistics are publicly available - FREE
    """
    
    def __init__(self):
        self.gwas_data = GWAS_SUMMARY_STATS.copy()
        
    def calculate_prs(self, variants_df: pd.DataFrame, 
                      trait: str) -> PRSResult:
        """
        Calculate PRS for a specific trait
        
        Args:
            variants_df: Variant DataFrame with genotype information
            trait: Trait name (e.g., 'alcohol_dependence')
            
        Returns:
            PRSResult with score and interpretation
        """
        if trait not in self.gwas_data:
            return PRSResult(
                trait=trait,
                score=0.0,
                percentile=50.0,
                risk_category='Unknown',
                n_variants=0,
                interpretation=f'Trait {trait} not in database'
            )
        
        trait_data = self.gwas_data[trait]
        snps = trait_data['snps']
        
        prs = 0.0
        n_matched = 0
        
        for rsid, info in snps.items():
            if 'ID' in variants_df.columns:
                variant_row = variants_df[variants_df['ID'] == rsid]
                if len(variant_row) > 0:
                    dosage = self._estimate_dosage(variant_row.iloc[0])
                    prs += info['beta'] * dosage
                    n_matched += 1
            elif 'rsid' in variants_df.columns:
                variant_row = variants_df[variants_df['rsid'] == rsid]
                if len(variant_row) > 0:
                    dosage = self._estimate_dosage(variant_row.iloc[0])
                    prs += info['beta'] * dosage
                    n_matched += 1
        
        z_score = (prs - trait_data['population_mean']) / trait_data['population_sd']
        
        from scipy import stats
        percentile = stats.norm.cdf(z_score) * 100
        
        if percentile >= 90:
            risk_category = 'Very High'
        elif percentile >= 75:
            risk_category = 'High'
        elif percentile >= 50:
            risk_category = 'Average'
        elif percentile >= 25:
            risk_category = 'Low'
        else:
            risk_category = 'Very Low'
        
        interpretation = self._generate_interpretation(
            trait, risk_category, percentile, n_matched, len(snps)
        )
        
        return PRSResult(
            trait=trait,
            score=round(prs, 4),
            percentile=round(percentile, 1),
            risk_category=risk_category,
            n_variants=n_matched,
            interpretation=interpretation
        )
    
    def _estimate_dosage(self, variant_row) -> float:
        """Estimate allele dosage from genotype"""
        for col in variant_row.index:
            if '_GT' in col:
                gt = variant_row[col]
                if gt in ['0/1', '0|1', '1/0', '1|0']:
                    return 1.0
                elif gt in ['1/1', '1|1']:
                    return 2.0
                else:
                    return 0.0
        return 1.0
    
    def _generate_interpretation(self, trait: str, risk: str, 
                                  percentile: float, matched: int, 
                                  total: int) -> str:
        """Generate interpretation text"""
        trait_name = trait.replace('_', ' ').title()
        
        coverage = (matched / total * 100) if total > 0 else 0
        
        base = f"PRS for {trait_name}: {risk} risk (percentile: {percentile:.0f}%). "
        base += f"Based on {matched}/{total} variants ({coverage:.0f}% coverage). "
        
        if risk in ['Very High', 'High']:
            base += (
                "This suggests elevated genetic susceptibility. "
                "Environmental factors and interventions remain important."
            )
        elif risk in ['Very Low', 'Low']:
            base += (
                "This suggests lower genetic susceptibility. "
                "However, behavioral and environmental factors still matter."
            )
        else:
            base += "Genetic risk is within the typical range."
        
        return base
    
    def calculate_all_prs(self, variants_df: pd.DataFrame) -> Dict[str, PRSResult]:
        """Calculate PRS for all available traits"""
        results = {}
        for trait in self.gwas_data.keys():
            results[trait] = self.calculate_prs(variants_df, trait)
        return results
    
    def generate_prs_report(self, variants_df: pd.DataFrame,
                            patient_id: str = "Patient") -> Dict:
        """
        Generate comprehensive PRS report
        
        Args:
            variants_df: Variant DataFrame
            patient_id: Patient identifier
            
        Returns:
            Complete PRS report dictionary
        """
        all_prs = self.calculate_all_prs(variants_df)
        
        addiction_traits = ['alcohol_dependence', 'opioid_dependence', 
                           'cocaine_dependence', 'cannabis_use_disorder',
                           'nicotine_dependence']
        
        mental_health_traits = ['depression', 'anxiety']
        
        addiction_prs = {t: all_prs[t] for t in addiction_traits if t in all_prs}
        mental_prs = {t: all_prs[t] for t in mental_health_traits if t in all_prs}
        
        highest_risk_trait = max(
            addiction_prs.items(),
            key=lambda x: x[1].percentile,
            default=(None, None)
        )
        
        return {
            'patient_id': patient_id,
            'report_type': 'Polygenic Risk Score Report',
            'addiction_scores': {
                k: {
                    'score': v.score,
                    'percentile': v.percentile,
                    'risk_category': v.risk_category,
                    'variants_matched': v.n_variants
                }
                for k, v in addiction_prs.items()
            },
            'mental_health_scores': {
                k: {
                    'score': v.score,
                    'percentile': v.percentile,
                    'risk_category': v.risk_category,
                    'variants_matched': v.n_variants
                }
                for k, v in mental_prs.items()
            },
            'highest_risk': highest_risk_trait[0] if highest_risk_trait[0] else 'None',
            'summary': self._generate_summary(all_prs),
            'disclaimer': (
                'Polygenic risk scores provide probabilistic estimates based on '
                'current genetic knowledge. They should not be used as sole '
                'diagnostic criteria. Environmental, behavioral, and other '
                'genetic factors also contribute to disease risk.'
            )
        }
    
    def _generate_summary(self, all_prs: Dict[str, PRSResult]) -> str:
        """Generate summary text for PRS report"""
        high_risk = [t for t, r in all_prs.items() 
                     if r.risk_category in ['High', 'Very High']]
        low_risk = [t for t, r in all_prs.items() 
                    if r.risk_category in ['Low', 'Very Low']]
        
        if high_risk:
            traits = ', '.join([t.replace('_', ' ') for t in high_risk[:3]])
            return f"Elevated genetic risk identified for: {traits}. Consider enhanced monitoring."
        elif low_risk:
            return "No elevated genetic risk identified. Average to low genetic susceptibility."
        else:
            return "Genetic risk profile within normal range."


class IntegratedRiskModel:
    # nrcdnl94
    """
    Integrate PRS with epigenetic age acceleration for comprehensive risk
    
    Combined model:
    Risk = α × PRS + β × EAA + γ × (PRS × EAA)
    
    Where:
    - PRS = Polygenic Risk Score
    - EAA = Epigenetic Age Acceleration
    - α, β, γ = model weights
    """
    
    def __init__(self, alpha: float = 0.4, beta: float = 0.4, gamma: float = 0.2):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.prs_calculator = PolygenicRiskScoreCalculator()
        
    def calculate_integrated_risk(self, prs_percentile: float,
                                    eaa_years: float) -> Dict:
        """
        Calculate integrated risk score
        
        Args:
            prs_percentile: PRS percentile (0-100)
            eaa_years: Epigenetic age acceleration in years
            
        Returns:
            Integrated risk assessment
        """
        prs_normalized = (prs_percentile - 50) / 50
        
        eaa_normalized = eaa_years / 10
        eaa_normalized = np.clip(eaa_normalized, -1, 1)
        
        interaction = prs_normalized * eaa_normalized
        
        combined_risk = (
            self.alpha * prs_normalized +
            self.beta * eaa_normalized +
            self.gamma * interaction
        )
        
        risk_percentile = (combined_risk + 1) / 2 * 100
        risk_percentile = np.clip(risk_percentile, 0, 100)
        
        if risk_percentile >= 80:
            category = 'Very High'
            interpretation = (
                "Both genetic and epigenetic factors indicate elevated risk. "
                "Intensive monitoring and intervention recommended."
            )
        elif risk_percentile >= 60:
            category = 'High'
            interpretation = (
                "Elevated combined risk. Consider enhanced surveillance "
                "and preventive interventions."
            )
        elif risk_percentile >= 40:
            category = 'Moderate'
            interpretation = (
                "Moderate combined risk. Standard monitoring with "
                "attention to lifestyle factors."
            )
        elif risk_percentile >= 20:
            category = 'Low'
            interpretation = (
                "Lower combined risk. Continue healthy lifestyle "
                "and periodic monitoring."
            )
        else:
            category = 'Very Low'
            interpretation = (
                "Minimal combined genetic and epigenetic risk. "
                "Maintain healthy behaviors."
            )
        
        return {
            'prs_component': round(prs_normalized, 3),
            'eaa_component': round(eaa_normalized, 3),
            'interaction_component': round(interaction, 3),
            'combined_score': round(combined_risk, 3),
            'risk_percentile': round(risk_percentile, 1),
            'risk_category': category,
            'interpretation': interpretation
        }
    
    def generate_integrated_report(self, variants_df: pd.DataFrame,
                                    eaa_results: pd.DataFrame,
                                    patient_id: str = "Patient") -> Dict:
        """
        Generate integrated genetic + epigenetic risk report
        
        Args:
            variants_df: Variant DataFrame
            eaa_results: Epigenetic age acceleration results
            patient_id: Patient identifier
            
        Returns:
            Complete integrated risk report
        """
        all_prs = self.prs_calculator.calculate_all_prs(variants_df)
        
        avg_prs_percentile = np.mean([r.percentile for r in all_prs.values()])
        
        avg_eaa = 0.0
        if 'Horvath EAA' in eaa_results.columns:
            avg_eaa = eaa_results['Horvath EAA'].mean()
        elif 'horvath_age' in eaa_results.columns and 'chronological_age' in eaa_results.columns:
            avg_eaa = (eaa_results['horvath_age'] - eaa_results['chronological_age']).mean()
        
        integrated_risk = self.calculate_integrated_risk(avg_prs_percentile, avg_eaa)
        
        return {
            'patient_id': patient_id,
            'report_type': 'Integrated Genetic-Epigenetic Risk Report',
            'genetic_component': {
                'average_prs_percentile': round(avg_prs_percentile, 1),
                'individual_scores': {
                    t: {'percentile': r.percentile, 'category': r.risk_category}
                    for t, r in all_prs.items()
                }
            },
            'epigenetic_component': {
                'average_eaa': round(avg_eaa, 2),
                'interpretation': self._interpret_eaa(avg_eaa)
            },
            'integrated_assessment': integrated_risk,
            'recommendations': self._generate_recommendations(integrated_risk),
            'disclaimer': (
                'This integrated assessment combines genetic and epigenetic factors. '
                'Results are for research purposes and should not replace clinical judgment.'
            )
        }
    
    def _interpret_eaa(self, eaa: float) -> str:
        """Interpret epigenetic age acceleration"""
        if eaa > 5:
            return "Significant biological aging acceleration detected."
        elif eaa > 2:
            return "Moderate biological aging acceleration."
        elif eaa > -2:
            return "Biological age within normal range."
        else:
            return "Biological age younger than chronological age."
    
    def _generate_recommendations(self, risk_assessment: Dict) -> List[str]:
        """Generate recommendations based on risk level"""
        recommendations = []
        
        category = risk_assessment['risk_category']
        
        if category in ['Very High', 'High']:
            recommendations.append("Consider genetic counseling consultation")
            recommendations.append("Enhanced monitoring for substance use")
            recommendations.append("Proactive mental health support")
            recommendations.append("Lifestyle interventions for biological age")
        elif category == 'Moderate':
            recommendations.append("Standard health monitoring")
            recommendations.append("Lifestyle optimization recommended")
            recommendations.append("Periodic reassessment")
        else:
            recommendations.append("Maintain healthy lifestyle")
            recommendations.append("Continue regular check-ups")
        
        return recommendations


# End of module - # nrcdnl94