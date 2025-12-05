# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
Pharmacogenomics Module
Drug response prediction based on genetic variants

Focus areas for addiction medicine:
- Opioid metabolism (CYP2D6, OPRM1)
- Alcohol metabolism (ADH1B, ALDH2)
- Stimulant response (DAT1, DRD2)
- Treatment response (COMT, 5-HTTLPR)

Based on CPIC Guidelines (Clinical Pharmacogenetics Implementation Consortium)
All guidelines are FREE and publicly available.

Author: Dr. Nurcan Denli Bayır
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
# nrcdnl94
class DrugRecommendation:
    # nrcdnl94
    """Drug recommendation based on pharmacogenomics"""
    drug: str
    gene: str
    phenotype: str
    recommendation: str
    strength: str
    alternative: Optional[str] = None
    dose_adjustment: Optional[str] = None


CYP2D6_ALLELES = {
    # nrcdnl94
    '*1': {'function': 'Normal', 'activity': 1.0},
    '*2': {'function': 'Normal', 'activity': 1.0},
    '*3': {'function': 'No function', 'activity': 0.0},
    '*4': {'function': 'No function', 'activity': 0.0},
    '*5': {'function': 'No function', 'activity': 0.0},
    '*6': {'function': 'No function', 'activity': 0.0},
    '*9': {'function': 'Decreased', 'activity': 0.5},
    '*10': {'function': 'Decreased', 'activity': 0.5},
    '*17': {'function': 'Decreased', 'activity': 0.5},
    '*29': {'function': 'Decreased', 'activity': 0.5},
    '*41': {'function': 'Decreased', 'activity': 0.5},
    '*1xN': {'function': 'Increased', 'activity': 2.0},
    '*2xN': {'function': 'Increased', 'activity': 2.0},
}

CYP2D6_PHENOTYPES = {
    # nrcdnl94
    (0.0, 0.0): 'Poor Metabolizer (PM)',
    (0.0, 0.5): 'Intermediate Metabolizer (IM)',
    (0.5, 0.5): 'Intermediate Metabolizer (IM)',
    (0.5, 1.0): 'Normal Metabolizer (NM)',
    (1.0, 1.0): 'Normal Metabolizer (NM)',
    (1.0, 2.0): 'Ultrarapid Metabolizer (UM)',
    (2.0, 2.0): 'Ultrarapid Metabolizer (UM)',
}

CYP2C19_ALLELES = {
    # nrcdnl94
    '*1': {'function': 'Normal', 'activity': 1.0},
    '*2': {'function': 'No function', 'activity': 0.0},
    '*3': {'function': 'No function', 'activity': 0.0},
    '*17': {'function': 'Increased', 'activity': 1.5},
}

OPRM1_VARIANTS = {
    # nrcdnl94
    'rs1799971': {
        'A/A': {'phenotype': 'Normal opioid sensitivity', 'effect': 'Standard response'},
        'A/G': {'phenotype': 'Reduced opioid sensitivity', 'effect': 'May need higher doses'},
        'G/G': {'phenotype': 'Low opioid sensitivity', 'effect': 'Significantly higher doses needed'}
    }
}


class PharmacogenomicsAnalyzer:
    # nrcdnl94
    """
    Predict drug response based on pharmacogenomic variants.
    
    Focus areas:
    - Opioid metabolism (CYP2D6, OPRM1)
    - Alcohol metabolism (ADH1B, ALDH2)
    - Stimulant response (DAT1, DRD2)
    - Treatment response (COMT, 5-HTTLPR)
    
    Based on CPIC Guidelines - FREE and publicly available.
    """
    
    CPIC_DRUGS = {
        'codeine': {
            'gene': 'CYP2D6',
            'recommendations': {
                'Poor Metabolizer (PM)': {
                    'recommendation': 'Avoid codeine - use alternative analgesic',
                    'strength': 'Strong',
                    'reason': 'No analgesic effect, risk of adverse events',
                    'alternative': 'Morphine, acetaminophen, NSAIDs'
                },
                'Intermediate Metabolizer (IM)': {
                    'recommendation': 'Use with caution, consider dose reduction or alternative',
                    'strength': 'Moderate',
                    'reason': 'Reduced analgesic effect',
                    'alternative': 'Consider morphine at reduced dose'
                },
                'Normal Metabolizer (NM)': {
                    'recommendation': 'Standard dosing',
                    'strength': 'Strong',
                    'reason': 'Normal metabolism expected',
                    'alternative': None
                },
                'Ultrarapid Metabolizer (UM)': {
                    'recommendation': 'Avoid codeine - risk of toxicity',
                    'strength': 'Strong',
                    'reason': 'Rapid conversion to morphine, risk of respiratory depression',
                    'alternative': 'Morphine at reduced dose, acetaminophen'
                }
            }
        },
        'tramadol': {
            'gene': 'CYP2D6',
            'recommendations': {
                'Poor Metabolizer (PM)': {
                    'recommendation': 'Avoid tramadol - reduced efficacy',
                    'strength': 'Strong',
                    'reason': 'Reduced conversion to active metabolite',
                    'alternative': 'Morphine, tapentadol'
                },
                'Ultrarapid Metabolizer (UM)': {
                    'recommendation': 'Avoid tramadol - risk of toxicity',
                    'strength': 'Strong',
                    'reason': 'Rapid conversion to O-desmethyltramadol',
                    'alternative': 'Morphine at reduced dose'
                }
            }
        },
        'oxycodone': {
            'gene': 'CYP2D6',
            'recommendations': {
                'Ultrarapid Metabolizer (UM)': {
                    'recommendation': 'Use with caution, monitor closely',
                    'strength': 'Moderate',
                    'reason': 'Increased formation of active metabolite',
                    'alternative': 'Consider dose reduction'
                }
            }
        },
        'methadone': {
            'gene': 'CYP2B6',
            'recommendations': {
                'Poor Metabolizer': {
                    'recommendation': 'Start with lower dose, monitor for toxicity',
                    'strength': 'Strong',
                    'reason': 'Reduced clearance, higher plasma levels',
                    'alternative': 'Start at 50% standard dose'
                }
            }
        },
        'buprenorphine': {
            'gene': 'OPRM1',
            'recommendations': {
                'G/G': {
                    'recommendation': 'May need higher induction dose',
                    'strength': 'Moderate',
                    'reason': 'Reduced receptor binding affinity',
                    'alternative': None
                }
            }
        },
        'naltrexone': {
            'gene': 'OPRM1',
            'recommendations': {
                'A/A': {
                    'recommendation': 'Good response expected',
                    'strength': 'Moderate',
                    'reason': 'Normal receptor function',
                    'alternative': None
                },
                'G/G': {
                    'recommendation': 'May have better response for alcohol use disorder',
                    'strength': 'Moderate',
                    'reason': 'Enhanced endorphin response',
                    'alternative': None
                }
            }
        },
        'disulfiram': {
            'gene': 'ALDH2',
            'recommendations': {
                '*2/*2': {
                    'recommendation': 'Use with extreme caution',
                    'strength': 'Strong',
                    'reason': 'Already has severe alcohol reaction',
                    'alternative': 'Naltrexone, acamprosate'
                }
            }
        }
    }
    
    def __init__(self):
        self.cpic_drugs = self.CPIC_DRUGS.copy()
        
    def analyze(self, variants_df: pd.DataFrame) -> Dict:
        """
        Full pharmacogenomic analysis
        
        Args:
            variants_df: Annotated variants DataFrame
            
        Returns:
            Dictionary with drug recommendations
        """
        results = {
            'opioid': self._analyze_opioid_metabolism(variants_df),
            'alcohol': self._analyze_alcohol_metabolism(variants_df),
            'stimulant': self._analyze_stimulant_response(variants_df),
            'treatment': self._analyze_treatment_response(variants_df),
            'all_recommendations': []
        }
        
        for category in ['opioid', 'alcohol', 'stimulant', 'treatment']:
            if 'recommendations' in results[category]:
                results['all_recommendations'].extend(results[category]['recommendations'])
        
        return results
    
    def _analyze_opioid_metabolism(self, df: pd.DataFrame) -> Dict:
        """
        Analyze CYP2D6 and OPRM1 variants for opioid response
        
        CYP2D6 phenotypes affect:
        - Codeine → Morphine conversion
        - Tramadol → O-desmethyltramadol conversion
        - Oxycodone metabolism
        
        OPRM1 affects:
        - Opioid receptor binding
        - Pain sensitivity
        - Addiction susceptibility
        """
        result = {
            'cyp2d6_phenotype': 'Normal Metabolizer (NM)',
            'oprm1_genotype': 'A/A',
            'recommendations': []
        }
        
        cyp2d6_genotype = self._detect_cyp2d6_phenotype(df)
        if cyp2d6_genotype:
            result['cyp2d6_phenotype'] = cyp2d6_genotype
        
        oprm1_genotype = self._detect_oprm1_genotype(df)
        if oprm1_genotype:
            result['oprm1_genotype'] = oprm1_genotype
        
        for drug in ['codeine', 'tramadol', 'oxycodone']:
            rec = self._get_drug_recommendation(drug, result['cyp2d6_phenotype'])
            if rec:
                result['recommendations'].append(rec)
        
        return result
    
    def _analyze_alcohol_metabolism(self, df: pd.DataFrame) -> Dict:
        """
        Analyze ADH1B and ALDH2 for alcohol metabolism
        
        ADH1B*2 (rs1229984):
        - Faster alcohol → acetaldehyde conversion
        - Protective against alcohol dependence
        
        ALDH2*2 (rs671):
        - Impaired acetaldehyde → acetate conversion
        - Causes flushing reaction
        - Common in East Asian populations
        """
        result = {
            'adh1b_status': 'Normal',
            'aldh2_status': 'Normal',
            'alcohol_sensitivity': 'Normal',
            'addiction_risk': 'Average',
            'recommendations': []
        }
        
        if 'ID' in df.columns:
            if 'rs1229984' in df['ID'].values:
                result['adh1b_status'] = 'Fast metabolizer'
                result['addiction_risk'] = 'Reduced'
            
            if 'rs671' in df['ID'].values:
                result['aldh2_status'] = 'Deficient'
                result['alcohol_sensitivity'] = 'High (flushing syndrome)'
                result['addiction_risk'] = 'Reduced'
                result['recommendations'].append({
                    'drug': 'Alcohol',
                    'recommendation': 'Likely to experience flushing reaction',
                    'clinical_note': 'Natural aversion to alcohol, protective against AUD'
                })
        
        return result
    
    def _analyze_stimulant_response(self, df: pd.DataFrame) -> Dict:
        """
        Analyze DAT1, DRD2, DRD4 for stimulant response
        
        These genes affect:
        - Dopamine signaling
        - Stimulant addiction risk
        - Treatment response (e.g., methylphenidate for ADHD)
        """
        result = {
            'dopamine_function': 'Normal',
            'addiction_susceptibility': 'Average',
            'recommendations': []
        }
        
        if 'clinvar_gene' in df.columns:
            drd2_variants = df[df['clinvar_gene'] == 'DRD2']
            if len(drd2_variants) > 0:
                result['dopamine_function'] = 'Altered DRD2 signaling'
                result['recommendations'].append({
                    'drug': 'Antipsychotics',
                    'recommendation': 'May have altered response to D2 antagonists'
                })
        
        return result
    
    def _analyze_treatment_response(self, df: pd.DataFrame) -> Dict:
        """
        Analyze COMT, SLC6A4 for addiction treatment response
        
        COMT Val158Met (rs4680):
        - Affects dopamine/norepinephrine breakdown
        - Pain sensitivity
        - Stress response
        
        SLC6A4 (5-HTTLPR):
        - Serotonin transporter
        - Antidepressant response
        - Anxiety/depression susceptibility
        """
        result = {
            'comt_status': 'Normal',
            'serotonin_function': 'Normal',
            'recommendations': []
        }
        
        if 'ID' in df.columns:
            if 'rs4680' in df['ID'].values:
                result['comt_status'] = 'Val/Met or Met/Met - Higher dopamine levels'
                result['recommendations'].append({
                    'drug': 'Opioids',
                    'recommendation': 'May have increased pain sensitivity'
                })
        
        return result
    
    def _detect_cyp2d6_phenotype(self, df: pd.DataFrame) -> Optional[str]:
        """Detect CYP2D6 metabolizer status from variants"""
        if 'clinvar_gene' in df.columns:
            cyp2d6_variants = df[df['clinvar_gene'] == 'CYP2D6']
            if len(cyp2d6_variants) > 0:
                return 'Normal Metabolizer (NM)'
        return None
    
    def _detect_oprm1_genotype(self, df: pd.DataFrame) -> Optional[str]:
        """Detect OPRM1 genotype from variants"""
        if 'ID' in df.columns:
            if 'rs1799971' in df['ID'].values:
                return 'A/G'
        return None
    
    def _get_drug_recommendation(self, drug: str, phenotype: str) -> Optional[Dict]:
        """Get drug recommendation based on phenotype"""
        if drug in self.cpic_drugs:
            drug_info = self.cpic_drugs[drug]
            if phenotype in drug_info['recommendations']:
                rec = drug_info['recommendations'][phenotype]
                return {
                    'drug': drug.title(),
                    'gene': drug_info['gene'],
                    'phenotype': phenotype,
                    'recommendation': rec['recommendation'],
                    'strength': rec['strength'],
                    'reason': rec['reason'],
                    'alternative': rec.get('alternative')
                }
        return None
    
    def generate_pgx_report(self, variants_df: pd.DataFrame, 
                            patient_id: str = "Patient") -> Dict:
        """
        Generate comprehensive pharmacogenomics report
        
        Args:
            variants_df: Annotated variant DataFrame
            patient_id: Patient identifier
            
        Returns:
            Complete PGx report dictionary
        """
        analysis = self.analyze(variants_df)
        
        report = {
            'patient_id': patient_id,
            'report_type': 'Pharmacogenomics Report',
            'genes_analyzed': ['CYP2D6', 'CYP2C19', 'OPRM1', 'ADH1B', 'ALDH2', 'COMT'],
            'opioid_summary': analysis['opioid'],
            'alcohol_summary': analysis['alcohol'],
            'stimulant_summary': analysis['stimulant'],
            'treatment_summary': analysis['treatment'],
            'all_recommendations': analysis['all_recommendations'],
            'actionable_findings': len(analysis['all_recommendations']),
            'disclaimer': (
                'This report is for research purposes only. '
                'Clinical decisions should be made in consultation with '
                'a healthcare provider and clinical pharmacologist.'
            )
        }
        
        return report


class DrugDoseCalculator:
    # nrcdnl94
    """
    Calculate personalized drug doses based on pharmacogenomics
    """
    
    STANDARD_DOSES = {
        'codeine': {'dose': 30, 'unit': 'mg', 'frequency': 'q4-6h'},
        'tramadol': {'dose': 50, 'unit': 'mg', 'frequency': 'q4-6h'},
        'oxycodone': {'dose': 5, 'unit': 'mg', 'frequency': 'q4-6h'},
        'methadone': {'dose': 10, 'unit': 'mg', 'frequency': 'daily'},
        'buprenorphine': {'dose': 8, 'unit': 'mg', 'frequency': 'daily'},
        'naltrexone': {'dose': 50, 'unit': 'mg', 'frequency': 'daily'},
    }
    
    DOSE_ADJUSTMENTS = {
        'Poor Metabolizer (PM)': 0.0,
        'Intermediate Metabolizer (IM)': 0.75,
        'Normal Metabolizer (NM)': 1.0,
        'Ultrarapid Metabolizer (UM)': 0.5,
    }
    
    def calculate_adjusted_dose(self, drug: str, phenotype: str) -> Dict:
        """
        Calculate adjusted dose based on metabolizer status
        
        Args:
            drug: Drug name
            phenotype: Metabolizer phenotype
            
        Returns:
            Adjusted dose information
        """
        if drug not in self.STANDARD_DOSES:
            return {'error': f'Drug {drug} not in database'}
        
        standard = self.STANDARD_DOSES[drug]
        adjustment = self.DOSE_ADJUSTMENTS.get(phenotype, 1.0)
        
        if adjustment == 0.0:
            return {
                'drug': drug,
                'recommendation': 'AVOID - Use alternative',
                'reason': f'{phenotype} - drug not recommended'
            }
        
        adjusted_dose = standard['dose'] * adjustment
        
        return {
            'drug': drug,
            'standard_dose': f"{standard['dose']} {standard['unit']}",
            'adjusted_dose': f"{adjusted_dose:.1f} {standard['unit']}",
            'frequency': standard['frequency'],
            'adjustment_factor': adjustment,
            'phenotype': phenotype
        }


class AddictionRiskCalculator:
    # nrcdnl94
    """
    Calculate genetic addiction risk based on multiple variants
    """
    
    RISK_VARIANTS = {
        'rs1799971': {'gene': 'OPRM1', 'risk_allele': 'G', 'odds_ratio': 1.25, 'addiction': 'Opioid'},
        'rs1800497': {'gene': 'DRD2', 'risk_allele': 'A', 'odds_ratio': 1.31, 'addiction': 'General'},
        'rs4680': {'gene': 'COMT', 'risk_allele': 'A', 'odds_ratio': 1.15, 'addiction': 'General'},
        'rs1229984': {'gene': 'ADH1B', 'risk_allele': 'A', 'odds_ratio': 0.5, 'addiction': 'Alcohol'},
        'rs671': {'gene': 'ALDH2', 'risk_allele': 'A', 'odds_ratio': 0.4, 'addiction': 'Alcohol'},
        'rs25531': {'gene': 'SLC6A4', 'risk_allele': 'G', 'odds_ratio': 1.18, 'addiction': 'General'},
    }
    
    def calculate_risk(self, variants_df: pd.DataFrame) -> Dict:
        """
        Calculate combined addiction risk score
        
        Args:
            variants_df: Variant DataFrame with genotype information
            
        Returns:
            Risk assessment dictionary
        """
        risk_score = 1.0
        found_variants = []
        
        for rsid, info in self.RISK_VARIANTS.items():
            if 'ID' in variants_df.columns and rsid in variants_df['ID'].values:
                risk_score *= info['odds_ratio']
                found_variants.append({
                    'rsid': rsid,
                    'gene': info['gene'],
                    'odds_ratio': info['odds_ratio'],
                    'addiction_type': info['addiction']
                })
        
        if risk_score > 1.5:
            risk_category = 'High'
        elif risk_score > 1.0:
            risk_category = 'Moderate'
        elif risk_score < 0.7:
            risk_category = 'Low (Protective)'
        else:
            risk_category = 'Average'
        
        return {
            'combined_risk_score': round(risk_score, 2),
            'risk_category': risk_category,
            'variants_found': found_variants,
            'total_risk_variants': len(found_variants),
            'interpretation': self._interpret_risk(risk_score, found_variants)
        }
    
    def _interpret_risk(self, score: float, variants: List[Dict]) -> str:
        """Generate interpretation text for risk score"""
        if score > 1.5:
            return (
                "Elevated genetic risk for substance dependence. "
                "Consider enhanced monitoring and preventive interventions. "
                "Note: Genetic risk is only one factor among many."
            )
        elif score < 0.7:
            return (
                "Genetic factors suggest reduced addiction susceptibility, "
                "particularly for alcohol. However, environmental factors "
                "remain important considerations."
            )
        else:
            return (
                "Genetic risk is within the average range. "
                "Environmental and behavioral factors play a significant role "
                "in addiction susceptibility."
            )


# End of module - # nrcdnl94