# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
Reference Database Module
Simulated reference data based on 10,542 DNA methylation profiles
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import stats


@dataclass
# nrcdnl94
class ReferenceStatistics:
    # nrcdnl94
    """Statistics from reference population"""
    n_samples: int
    mean_eaa: float
    std_eaa: float
    percentiles: Dict[int, float]
    age_range: Tuple[float, float]
    substance_distribution: Dict[str, int]


@dataclass
# nrcdnl94
class ComparisonResult:
    # nrcdnl94
    """Result of comparing a sample to reference"""
    sample_eaa: float
    percentile: float
    z_score: float
    reference_mean: float
    reference_std: float
    interpretation: str
    similar_samples: int


class ReferenceDatabase:
    # nrcdnl94
    """
    Reference database based on 10,542 DNA methylation profiles.
    
    Dataset composition (from research paper):
    - Alcohol use disorder: n=2,183
    - Cocaine use: n=1,030
    - Opioid use: n=1,360
    - Methamphetamine use: n=48
    - Cannabis use: n=194
    - Polysubstance use: n=720
    - Healthy controls: n=5,007
    """
    
    DATASET_SIZES = {
        'control': 5007,
        'alcohol': 2183,
        'cocaine': 1030,
        'opioids': 1360,
        'methamphetamine': 48,
        'cannabis': 194,
        'polysubstance': 720
    }
    
    EAA_PARAMETERS = {
        'control': {'mean': 0.0, 'std': 2.5},
        'alcohol': {'mean': 3.6, 'std': 3.2},
        'cocaine': {'mean': 4.1, 'std': 3.5},
        'opioids': {'mean': 2.9, 'std': 2.8},
        'methamphetamine': {'mean': 6.2, 'std': 4.0},
        'cannabis': {'mean': 0.8, 'std': 2.2},
        'polysubstance': {'mean': 7.3, 'std': 4.5}
    }
    
    CONFIDENCE_INTERVALS = {
        'alcohol': (3.1, 4.2),
        'cocaine': (3.5, 4.7),
        'opioids': (2.5, 3.4),
        'methamphetamine': (4.5, 8.1),
        'cannabis': (0.3, 1.4),
        'polysubstance': (6.4, 8.3)
    }
    
    CLOCK_PERFORMANCE = {
        'horvath': {'mae': 3.6, 'r2': 0.96},
        'hannum': {'mae': 3.9, 'r2': 0.94},
        'phenoage': {'mae': 2.8, 'r2': 0.95},
        'grimage': {'mae': 2.4, 'r2': 0.94},
        'dunedinpace': {'mae': 0.15, 'r2': 0.89},
        'ensemble': {'mae': 2.1, 'r2': 0.96}
    }
    
    def __init__(self, random_state: int = 42):
        """Initialize the reference database"""
        self.random_state = random_state
        np.random.seed(random_state)
        self._generate_reference_data()
    
    def _generate_reference_data(self):
        """Generate simulated reference data based on research parameters"""
        
        self.reference_data = {}
        all_data = []
        
        for substance, n_samples in self.DATASET_SIZES.items():
            params = self.EAA_PARAMETERS[substance]
            
            ages = np.random.uniform(18, 75, n_samples)
            
            eaa_values = np.random.normal(params['mean'], params['std'], n_samples)
            
            age_effect = (ages - 45) * 0.02
            eaa_values += age_effect
            
            sex = np.random.choice(['M', 'F'], n_samples, p=[0.6, 0.4])
            sex_effect = np.where(sex == 'M', 0.5, -0.3)
            eaa_values += sex_effect
            
            grimage_eaa = eaa_values
            horvath_eaa = eaa_values * 0.8 + np.random.normal(0, 1, n_samples)
            hannum_eaa = eaa_values * 0.75 + np.random.normal(0, 1, n_samples)
            phenoage_eaa = eaa_values * 0.9 + np.random.normal(0, 0.8, n_samples)
            dunedinpace = 1.0 + eaa_values * 0.02 + np.random.normal(0, 0.05, n_samples)
            dunedinpace = np.clip(dunedinpace, 0.6, 1.8)
            
            for i in range(n_samples):
                all_data.append({
                    'sample_id': f"{substance}_{i:05d}",
                    'substance_type': substance,
                    'chronological_age': ages[i],
                    'sex': sex[i],
                    'grimage_eaa': grimage_eaa[i],
                    'horvath_eaa': horvath_eaa[i],
                    'hannum_eaa': hannum_eaa[i],
                    'phenoage_eaa': phenoage_eaa[i],
                    'dunedinpace': dunedinpace[i]
                })
            
            self.reference_data[substance] = pd.DataFrame({
                'chronological_age': ages,
                'sex': sex,
                'grimage_eaa': grimage_eaa,
                'horvath_eaa': horvath_eaa,
                'hannum_eaa': hannum_eaa,
                'phenoage_eaa': phenoage_eaa,
                'dunedinpace': dunedinpace
            })
        
        self.full_database = pd.DataFrame(all_data)
    
    def get_reference_statistics(self, 
                                  substance_type: str = None,
                                  clock_name: str = 'grimage') -> ReferenceStatistics:
        """
        Get reference statistics for a substance type or overall.
        
        Args:
            substance_type: Specific substance or None for all
            clock_name: Which clock's EAA to use
        
        Returns:
            ReferenceStatistics object
        """
        eaa_col = f"{clock_name}_eaa" if clock_name != 'dunedinpace' else 'dunedinpace'
        
        if substance_type:
            if substance_type not in self.reference_data:
                raise ValueError(f"Unknown substance type: {substance_type}")
            data = self.reference_data[substance_type]
            n_samples = len(data)
            substance_dist = {substance_type: n_samples}
        else:
            data = self.full_database
            n_samples = len(data)
            substance_dist = self.DATASET_SIZES.copy()
        
        eaa_values = data[eaa_col].values
        
        percentiles = {
            5: np.percentile(eaa_values, 5),
            25: np.percentile(eaa_values, 25),
            50: np.percentile(eaa_values, 50),
            75: np.percentile(eaa_values, 75),
            95: np.percentile(eaa_values, 95)
        }
        
        age_col = 'chronological_age'
        age_range = (data[age_col].min(), data[age_col].max())
        
        return ReferenceStatistics(
            n_samples=n_samples,
            mean_eaa=round(np.mean(eaa_values), 2),
            std_eaa=round(np.std(eaa_values), 2),
            percentiles={k: round(v, 2) for k, v in percentiles.items()},
            age_range=(round(age_range[0], 1), round(age_range[1], 1)),
            substance_distribution=substance_dist
        )
    
    def compare_to_reference(self,
                             sample_eaa: float,
                             substance_type: str = None,
                             clock_name: str = 'grimage',
                             age: float = None,
                             sex: str = None) -> ComparisonResult:
        """
        Compare a sample's EAA to the reference population.
        
        Args:
            sample_eaa: The sample's EAA value
            substance_type: Compare to specific substance group or None for control
            clock_name: Which clock was used
            age: Optional age for age-matched comparison
            sex: Optional sex for sex-matched comparison
        
        Returns:
            ComparisonResult with comparison statistics
        """
        eaa_col = f"{clock_name}_eaa" if clock_name != 'dunedinpace' else 'dunedinpace'
        
        if substance_type:
            data = self.reference_data.get(substance_type, self.reference_data['control'])
        else:
            data = self.reference_data['control']
        
        mask = np.ones(len(data), dtype=bool)
        
        if age is not None:
            age_diff = np.abs(data['chronological_age'] - age)
            mask &= age_diff <= 10
        
        if sex is not None:
            mask &= data['sex'] == sex
        
        if mask.sum() < 20:
            mask = np.ones(len(data), dtype=bool)
        
        filtered_data = data[mask]
        reference_values = filtered_data[eaa_col].values
        
        mean_ref = np.mean(reference_values)
        std_ref = np.std(reference_values)
        
        z_score = (sample_eaa - mean_ref) / (std_ref + 1e-10)
        percentile = stats.norm.cdf(z_score) * 100
        
        similar_mask = np.abs(reference_values - sample_eaa) <= std_ref * 0.5
        similar_samples = similar_mask.sum()
        
        if percentile < 10:
            interpretation = "Referans popülasyondan anlamlı şekilde düşük - koruyucu faktörler mevcut olabilir"
        elif percentile < 25:
            interpretation = "Referans popülasyonun alt çeyreğinde"
        elif percentile < 75:
            interpretation = "Referans popülasyonla uyumlu - tipik aralıkta"
        elif percentile < 90:
            interpretation = "Referans popülasyonun üst çeyreğinde - izlem önerilir"
        else:
            interpretation = "Referans popülasyondan anlamlı şekilde yüksek - müdahale düşünülmeli"
        
        return ComparisonResult(
            sample_eaa=round(sample_eaa, 2),
            percentile=round(percentile, 1),
            z_score=round(z_score, 2),
            reference_mean=round(mean_ref, 2),
            reference_std=round(std_ref, 2),
            interpretation=interpretation,
            similar_samples=int(similar_samples)
        )
    
    def get_substance_effect_summary(self) -> pd.DataFrame:
        """
        Get summary of substance effects on EAA from reference data.
        
        Returns:
            DataFrame with effect sizes and confidence intervals
        """
        control_mean = self.EAA_PARAMETERS['control']['mean']
        
        results = []
        for substance, params in self.EAA_PARAMETERS.items():
            if substance == 'control':
                continue
            
            effect_size = params['mean'] - control_mean
            
            ci = self.CONFIDENCE_INTERVALS.get(substance, (effect_size - 1, effect_size + 1))
            
            results.append({
                'substance': substance,
                'n_samples': self.DATASET_SIZES[substance],
                'mean_eaa': params['mean'],
                'std_eaa': params['std'],
                'effect_vs_control': round(effect_size, 2),
                'ci_lower': ci[0],
                'ci_upper': ci[1]
            })
        
        df = pd.DataFrame(results)
        df = df.sort_values('effect_vs_control', ascending=False)
        
        return df
    
    def get_clock_performance_summary(self) -> pd.DataFrame:
        """
        Get summary of clock performance metrics.
        
        Returns:
            DataFrame with MAE and R² for each clock
        """
        results = []
        for clock, metrics in self.CLOCK_PERFORMANCE.items():
            results.append({
                'clock': clock,
                'mae': metrics['mae'],
                'r_squared': metrics['r2'],
                'accuracy_category': 'Excellent' if metrics['mae'] < 3 else 'Good' if metrics['mae'] < 4 else 'Moderate'
            })
        
        return pd.DataFrame(results)
    
    def get_age_stratified_statistics(self,
                                       substance_type: str = None,
                                       age_bins: List[int] = None) -> pd.DataFrame:
        """
        Get EAA statistics stratified by age groups.
        
        Args:
            substance_type: Filter by substance type
            age_bins: Custom age bin edges
        
        Returns:
            DataFrame with age-stratified statistics
        """
        if age_bins is None:
            age_bins = [18, 30, 40, 50, 60, 75]
        
        if substance_type:
            data = self.full_database[self.full_database['substance_type'] == substance_type].copy()
        else:
            data = self.full_database.copy()
        
        data['age_group'] = pd.cut(
            data['chronological_age'],
            bins=age_bins,
            labels=[f"{age_bins[i]}-{age_bins[i+1]}" for i in range(len(age_bins)-1)]
        )
        
        results = data.groupby('age_group').agg({
            'grimage_eaa': ['count', 'mean', 'std'],
            'horvath_eaa': ['mean', 'std'],
            'phenoage_eaa': ['mean', 'std'],
            'dunedinpace': ['mean', 'std']
        }).round(2)
        
        results.columns = ['_'.join(col).strip() for col in results.columns.values]
        
        return results
    
    def generate_synthetic_cohort(self,
                                   n_samples: int,
                                   substance_distribution: Dict[str, float] = None,
                                   age_range: Tuple[float, float] = (25, 65)) -> pd.DataFrame:
        """
        Generate a synthetic cohort matching reference characteristics.
        
        Args:
            n_samples: Number of samples to generate
            substance_distribution: Dict of substance types to proportions
            age_range: Age range for synthetic samples
        
        Returns:
            DataFrame with synthetic cohort data
        """
        if substance_distribution is None:
            total = sum(self.DATASET_SIZES.values())
            substance_distribution = {
                k: v/total for k, v in self.DATASET_SIZES.items()
            }
        
        data = []
        
        for substance, proportion in substance_distribution.items():
            n_substance = int(n_samples * proportion)
            params = self.EAA_PARAMETERS[substance]
            
            ages = np.random.uniform(age_range[0], age_range[1], n_substance)
            sex = np.random.choice(['M', 'F'], n_substance, p=[0.55, 0.45])
            
            base_eaa = np.random.normal(params['mean'], params['std'], n_substance)
            age_effect = (ages - 45) * 0.02
            sex_effect = np.where(sex == 'M', 0.4, -0.2)
            grimage_eaa = base_eaa + age_effect + sex_effect
            
            for i in range(n_substance):
                data.append({
                    'sample_id': f"synth_{len(data):05d}",
                    'substance_type': substance,
                    'chronological_age': round(ages[i], 1),
                    'sex': sex[i],
                    'grimage_eaa': round(grimage_eaa[i], 2),
                    'horvath_eaa': round(grimage_eaa[i] * 0.8 + np.random.normal(0, 1), 2),
                    'hannum_eaa': round(grimage_eaa[i] * 0.75 + np.random.normal(0, 1), 2),
                    'phenoage_eaa': round(grimage_eaa[i] * 0.9 + np.random.normal(0, 0.8), 2),
                    'dunedinpace': round(np.clip(1.0 + grimage_eaa[i] * 0.02 + np.random.normal(0, 0.05), 0.6, 1.8), 3)
                })
        
        return pd.DataFrame(data)
    
    def get_database_summary(self) -> Dict:
        """
        Get comprehensive summary of the reference database.
        
        Returns:
            Dictionary with database summary statistics
        """
        return {
            'total_samples': sum(self.DATASET_SIZES.values()),
            'substance_distribution': self.DATASET_SIZES.copy(),
            'eaa_parameters': self.EAA_PARAMETERS.copy(),
            'confidence_intervals': self.CONFIDENCE_INTERVALS.copy(),
            'clock_performance': self.CLOCK_PERFORMANCE.copy(),
            'age_range': (18.0, 75.0),
            'sex_distribution': {'M': 0.55, 'F': 0.45}
        }


# End of module - # nrcdnl94