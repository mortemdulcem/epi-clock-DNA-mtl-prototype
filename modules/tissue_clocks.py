"""
Tissue-Specific Epigenetic Clocks Module
=========================================

Advanced tissue-specific DNA methylation age estimation for:
- Brain (prefrontal cortex, hippocampus, cerebellum)
- Liver (hepatic tissue)
- Kidney (renal cortex)
- Heart (cardiac muscle)
- Lung (pulmonary tissue)
- Blood (peripheral blood mononuclear cells)
- Skin (dermal fibroblasts)

Based on research:
- Horvath pan-tissue clock adaptations
- Tissue-specific CpG coefficient sets
- Cross-tissue normalization algorithms

PROTOTYPE: Uses simulated coefficients for demonstration.
Real coefficients require licensing from original publications.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from scipy import stats
import hashlib


class TissueType(Enum):
    """Supported tissue types for epigenetic age estimation"""
    BLOOD = "blood"
    BRAIN_PFC = "brain_prefrontal_cortex"
    BRAIN_HIPPO = "brain_hippocampus"
    BRAIN_CEREBELLUM = "brain_cerebellum"
    LIVER = "liver"
    KIDNEY = "kidney"
    HEART = "heart"
    LUNG = "lung"
    SKIN = "skin"
    MUSCLE = "skeletal_muscle"
    ADIPOSE = "adipose_tissue"
    SALIVA = "saliva"


@dataclass
class TissueClockResult:
    """Result of tissue-specific epigenetic age calculation"""
    tissue_type: TissueType
    clock_name: str
    epigenetic_age: float
    chronological_age: float
    age_acceleration: float
    confidence_interval: Tuple[float, float]
    quality_score: float
    cpg_coverage: float
    tissue_correction_factor: float
    cross_tissue_normalized_age: float
    interpretation: str
    warning_flags: List[str] = field(default_factory=list)


@dataclass 
class TissueClockCoefficients:
    """Coefficients for a tissue-specific clock"""
    tissue_type: TissueType
    clock_name: str
    n_cpgs: int
    cpg_ids: List[str]
    coefficients: np.ndarray
    intercept: float
    transformation: str  # 'linear', 'log', 'anti-log'
    age_range: Tuple[float, float]
    validation_mae: float
    validation_r2: float
    tissue_correction: float
    cross_tissue_factor: float


class TissueSpecificClockRegistry:
    """
    Registry of tissue-specific epigenetic clocks with coefficients
    and cross-tissue normalization capabilities.
    """
    
    def __init__(self):
        self.clocks: Dict[str, TissueClockCoefficients] = {}
        self._initialize_tissue_clocks()
        
    def _initialize_tissue_clocks(self):
        """Initialize all tissue-specific clock coefficients (SIMULATED)"""
        
        tissue_configs = {
            TissueType.BLOOD: {
                'n_cpgs': 353,
                'mae': 3.6,
                'r2': 0.96,
                'correction': 0.0,
                'cross_factor': 1.0,
                'age_range': (0, 100)
            },
            TissueType.BRAIN_PFC: {
                'n_cpgs': 347,
                'mae': 4.2,
                'r2': 0.94,
                'correction': -2.3,
                'cross_factor': 1.08,
                'age_range': (20, 100)
            },
            TissueType.BRAIN_HIPPO: {
                'n_cpgs': 341,
                'mae': 4.5,
                'r2': 0.93,
                'correction': -1.8,
                'cross_factor': 1.12,
                'age_range': (20, 100)
            },
            TissueType.BRAIN_CEREBELLUM: {
                'n_cpgs': 338,
                'mae': 3.9,
                'r2': 0.95,
                'correction': -3.1,
                'cross_factor': 1.05,
                'age_range': (20, 100)
            },
            TissueType.LIVER: {
                'n_cpgs': 312,
                'mae': 4.8,
                'r2': 0.92,
                'correction': 1.7,
                'cross_factor': 0.95,
                'age_range': (18, 90)
            },
            TissueType.KIDNEY: {
                'n_cpgs': 298,
                'mae': 5.1,
                'r2': 0.91,
                'correction': 2.1,
                'cross_factor': 0.93,
                'age_range': (18, 85)
            },
            TissueType.HEART: {
                'n_cpgs': 287,
                'mae': 5.4,
                'r2': 0.89,
                'correction': 0.8,
                'cross_factor': 0.97,
                'age_range': (25, 85)
            },
            TissueType.LUNG: {
                'n_cpgs': 276,
                'mae': 5.2,
                'r2': 0.90,
                'correction': 1.2,
                'cross_factor': 0.96,
                'age_range': (20, 90)
            },
            TissueType.SKIN: {
                'n_cpgs': 391,
                'mae': 4.1,
                'r2': 0.94,
                'correction': -0.5,
                'cross_factor': 1.02,
                'age_range': (0, 100)
            },
            TissueType.MUSCLE: {
                'n_cpgs': 264,
                'mae': 5.6,
                'r2': 0.88,
                'correction': 1.5,
                'cross_factor': 0.94,
                'age_range': (20, 85)
            },
            TissueType.ADIPOSE: {
                'n_cpgs': 251,
                'mae': 5.8,
                'r2': 0.87,
                'correction': 2.4,
                'cross_factor': 0.91,
                'age_range': (18, 80)
            },
            TissueType.SALIVA: {
                'n_cpgs': 320,
                'mae': 4.0,
                'r2': 0.94,
                'correction': 0.3,
                'cross_factor': 1.01,
                'age_range': (0, 100)
            }
        }
        
        for tissue_type, config in tissue_configs.items():
            np.random.seed(hash(tissue_type.value) % 2**32)
            
            cpg_ids = [f"cg{10000000 + i:08d}" for i in range(config['n_cpgs'])]
            coefficients = np.random.normal(0, 0.1, config['n_cpgs'])
            coefficients = coefficients / np.sum(np.abs(coefficients)) * 50
            
            clock = TissueClockCoefficients(
                tissue_type=tissue_type,
                clock_name=f"Horvath_{tissue_type.value}",
                n_cpgs=config['n_cpgs'],
                cpg_ids=cpg_ids,
                coefficients=coefficients,
                intercept=21.0 + np.random.normal(0, 2),
                transformation='anti-log',
                age_range=config['age_range'],
                validation_mae=config['mae'],
                validation_r2=config['r2'],
                tissue_correction=config['correction'],
                cross_tissue_factor=config['cross_factor']
            )
            
            self.clocks[f"{tissue_type.value}_horvath"] = clock
            
            hannum_clock = TissueClockCoefficients(
                tissue_type=tissue_type,
                clock_name=f"Hannum_{tissue_type.value}",
                n_cpgs=min(71, config['n_cpgs']),
                cpg_ids=cpg_ids[:min(71, config['n_cpgs'])],
                coefficients=coefficients[:min(71, config['n_cpgs'])] * 1.2,
                intercept=19.0 + np.random.normal(0, 2),
                transformation='linear',
                age_range=config['age_range'],
                validation_mae=config['mae'] + 0.3,
                validation_r2=config['r2'] - 0.01,
                tissue_correction=config['correction'] * 0.8,
                cross_tissue_factor=config['cross_factor']
            )
            self.clocks[f"{tissue_type.value}_hannum"] = hannum_clock
    
    def get_clock(self, tissue_type: TissueType, clock_type: str = 'horvath') -> Optional[TissueClockCoefficients]:
        """Get specific tissue clock coefficients"""
        key = f"{tissue_type.value}_{clock_type}"
        return self.clocks.get(key)
    
    def list_available_clocks(self) -> List[Dict[str, Any]]:
        """List all available tissue-specific clocks"""
        return [
            {
                'tissue': clock.tissue_type.value,
                'clock_name': clock.clock_name,
                'n_cpgs': clock.n_cpgs,
                'mae': clock.validation_mae,
                'r2': clock.validation_r2,
                'age_range': clock.age_range
            }
            for clock in self.clocks.values()
        ]


class TissueSpecificClockCalculator:
    """
    Advanced tissue-specific epigenetic age calculator with:
    - Multi-tissue support
    - Cross-tissue normalization
    - Quality assessment
    - Confidence intervals
    """
    
    def __init__(self):
        self.registry = TissueSpecificClockRegistry()
        self.tissue_reference_data = self._load_tissue_reference_data()
        
    def _load_tissue_reference_data(self) -> Dict[TissueType, Dict]:
        """Load tissue-specific reference statistics"""
        reference_data = {}
        
        tissue_stats = {
            TissueType.BLOOD: {'mean_eaa': 0.0, 'std_eaa': 3.2, 'n_ref': 5007},
            TissueType.BRAIN_PFC: {'mean_eaa': 2.1, 'std_eaa': 4.1, 'n_ref': 847},
            TissueType.BRAIN_HIPPO: {'mean_eaa': 1.8, 'std_eaa': 4.3, 'n_ref': 623},
            TissueType.BRAIN_CEREBELLUM: {'mean_eaa': -0.5, 'std_eaa': 3.8, 'n_ref': 512},
            TissueType.LIVER: {'mean_eaa': 1.2, 'std_eaa': 4.5, 'n_ref': 389},
            TissueType.KIDNEY: {'mean_eaa': 0.8, 'std_eaa': 4.8, 'n_ref': 276},
            TissueType.HEART: {'mean_eaa': 0.5, 'std_eaa': 5.0, 'n_ref': 198},
            TissueType.LUNG: {'mean_eaa': 0.9, 'std_eaa': 4.7, 'n_ref': 234},
            TissueType.SKIN: {'mean_eaa': -0.3, 'std_eaa': 3.5, 'n_ref': 1203},
            TissueType.MUSCLE: {'mean_eaa': 0.6, 'std_eaa': 5.2, 'n_ref': 156},
            TissueType.ADIPOSE: {'mean_eaa': 1.5, 'std_eaa': 5.5, 'n_ref': 187},
            TissueType.SALIVA: {'mean_eaa': 0.2, 'std_eaa': 3.4, 'n_ref': 2341}
        }
        
        for tissue_type, stats in tissue_stats.items():
            reference_data[tissue_type] = stats
            
        return reference_data
    
    def calculate_tissue_age(
        self,
        methylation_data: np.ndarray,
        chronological_age: float,
        tissue_type: TissueType,
        clock_type: str = 'horvath'
    ) -> TissueClockResult:
        """
        Calculate tissue-specific epigenetic age
        
        Args:
            methylation_data: Beta values array
            chronological_age: Known chronological age
            tissue_type: Type of tissue
            clock_type: 'horvath' or 'hannum'
            
        Returns:
            TissueClockResult with all metrics
        """
        clock = self.registry.get_clock(tissue_type, clock_type)
        if clock is None:
            raise ValueError(f"Clock not found for {tissue_type.value}_{clock_type}")
        
        n_available = len(methylation_data)
        n_required = clock.n_cpgs
        cpg_coverage = min(n_available / n_required, 1.0)
        
        if n_available < n_required:
            extended_data = np.zeros(n_required)
            extended_data[:n_available] = methylation_data
            extended_data[n_available:] = 0.5
            methylation_data = extended_data
        else:
            methylation_data = methylation_data[:n_required]
        
        raw_age = np.dot(methylation_data, clock.coefficients) + clock.intercept
        
        if clock.transformation == 'anti-log':
            if raw_age < 0:
                epigenetic_age = 21 * np.exp(raw_age) - 1
            else:
                epigenetic_age = 21 * raw_age + 20
        else:
            epigenetic_age = raw_age
        
        tissue_corrected_age = epigenetic_age + clock.tissue_correction
        
        cross_tissue_age = tissue_corrected_age * clock.cross_tissue_factor
        
        age_acceleration = tissue_corrected_age - chronological_age
        
        ref_stats = self.tissue_reference_data.get(tissue_type, {'std_eaa': 4.0})
        se = ref_stats['std_eaa'] / np.sqrt(cpg_coverage * 100)
        ci_lower = age_acceleration - 1.96 * se
        ci_upper = age_acceleration + 1.96 * se
        
        quality_score = self._calculate_quality_score(
            cpg_coverage, 
            methylation_data, 
            clock.age_range,
            chronological_age
        )
        
        interpretation = self._generate_interpretation(
            age_acceleration, tissue_type, ref_stats
        )
        
        warning_flags = self._check_warnings(
            cpg_coverage, quality_score, chronological_age, clock.age_range
        )
        
        return TissueClockResult(
            tissue_type=tissue_type,
            clock_name=clock.clock_name,
            epigenetic_age=round(tissue_corrected_age, 2),
            chronological_age=chronological_age,
            age_acceleration=round(age_acceleration, 2),
            confidence_interval=(round(ci_lower, 2), round(ci_upper, 2)),
            quality_score=round(quality_score, 3),
            cpg_coverage=round(cpg_coverage, 3),
            tissue_correction_factor=clock.tissue_correction,
            cross_tissue_normalized_age=round(cross_tissue_age, 2),
            interpretation=interpretation,
            warning_flags=warning_flags
        )
    
    def _calculate_quality_score(
        self,
        cpg_coverage: float,
        methylation_data: np.ndarray,
        age_range: Tuple[float, float],
        chronological_age: float
    ) -> float:
        """Calculate overall quality score for the measurement"""
        coverage_score = cpg_coverage
        
        valid_range = (methylation_data >= 0) & (methylation_data <= 1)
        range_score = np.mean(valid_range)
        
        variance = np.var(methylation_data)
        variance_score = min(variance / 0.05, 1.0)
        
        if age_range[0] <= chronological_age <= age_range[1]:
            age_score = 1.0
        else:
            distance = min(
                abs(chronological_age - age_range[0]),
                abs(chronological_age - age_range[1])
            )
            age_score = max(0, 1 - distance / 20)
        
        quality = (
            0.4 * coverage_score +
            0.3 * range_score +
            0.2 * variance_score +
            0.1 * age_score
        )
        
        return quality
    
    def _generate_interpretation(
        self,
        age_acceleration: float,
        tissue_type: TissueType,
        ref_stats: Dict
    ) -> str:
        """Generate clinical interpretation of results"""
        z_score = age_acceleration / ref_stats.get('std_eaa', 4.0)
        
        tissue_name = tissue_type.value.replace('_', ' ').title()
        
        if abs(z_score) < 0.5:
            category = "normal aralıkta"
            severity = "Normal"
        elif abs(z_score) < 1.0:
            category = "hafif sapma" if z_score > 0 else "hafif genç"
            severity = "Hafif"
        elif abs(z_score) < 2.0:
            category = "orta derece ivmelenme" if z_score > 0 else "orta derece gençleşme"
            severity = "Orta"
        else:
            category = "belirgin ivmelenme" if z_score > 0 else "belirgin gençleşme"
            severity = "Yüksek"
        
        interpretation = (
            f"{tissue_name} dokusu için epigenetik yaş {category} göstermektedir "
            f"(EAA={age_acceleration:+.1f} yıl, z={z_score:.2f}). "
            f"Klinik önemi: {severity}."
        )
        
        return interpretation
    
    def _check_warnings(
        self,
        cpg_coverage: float,
        quality_score: float,
        chronological_age: float,
        age_range: Tuple[float, float]
    ) -> List[str]:
        """Check for potential issues and generate warnings"""
        warnings = []
        
        if cpg_coverage < 0.8:
            warnings.append(f"Düşük CpG kapsama oranı ({cpg_coverage:.1%})")
        
        if quality_score < 0.7:
            warnings.append(f"Düşük kalite skoru ({quality_score:.2f})")
        
        if chronological_age < age_range[0]:
            warnings.append(f"Kronolojik yaş validasyon aralığının altında (<{age_range[0]})")
        elif chronological_age > age_range[1]:
            warnings.append(f"Kronolojik yaş validasyon aralığının üstünde (>{age_range[1]})")
        
        return warnings
    
    def compare_tissues(
        self,
        methylation_data: Dict[TissueType, np.ndarray],
        chronological_age: float,
        clock_type: str = 'horvath'
    ) -> pd.DataFrame:
        """
        Compare epigenetic age across multiple tissues
        
        Args:
            methylation_data: Dict mapping tissue types to methylation arrays
            chronological_age: Known chronological age
            clock_type: Clock type to use
            
        Returns:
            DataFrame with cross-tissue comparison
        """
        results = []
        
        for tissue_type, data in methylation_data.items():
            try:
                result = self.calculate_tissue_age(
                    data, chronological_age, tissue_type, clock_type
                )
                results.append({
                    'Doku': tissue_type.value.replace('_', ' ').title(),
                    'Epigenetik Yaş': result.epigenetic_age,
                    'EAA': result.age_acceleration,
                    'CI Alt': result.confidence_interval[0],
                    'CI Üst': result.confidence_interval[1],
                    'Kalite': result.quality_score,
                    'Normalize Yaş': result.cross_tissue_normalized_age
                })
            except Exception as e:
                results.append({
                    'Doku': tissue_type.value.replace('_', ' ').title(),
                    'Epigenetik Yaş': np.nan,
                    'EAA': np.nan,
                    'CI Alt': np.nan,
                    'CI Üst': np.nan,
                    'Kalite': 0.0,
                    'Normalize Yaş': np.nan
                })
        
        return pd.DataFrame(results)
    
    def get_tissue_reference_percentile(
        self,
        age_acceleration: float,
        tissue_type: TissueType
    ) -> Dict[str, Any]:
        """Get percentile ranking for EAA within tissue-specific reference"""
        ref_stats = self.tissue_reference_data.get(tissue_type)
        if ref_stats is None:
            return {'percentile': 50, 'z_score': 0, 'category': 'Bilinmiyor'}
        
        z_score = (age_acceleration - ref_stats['mean_eaa']) / ref_stats['std_eaa']
        percentile = stats.norm.cdf(z_score) * 100
        
        if percentile < 10:
            category = "Çok Düşük (Biyolojik Olarak Genç)"
        elif percentile < 25:
            category = "Düşük"
        elif percentile < 75:
            category = "Normal"
        elif percentile < 90:
            category = "Yüksek"
        else:
            category = "Çok Yüksek (Hızlandırılmış Yaşlanma)"
        
        return {
            'percentile': round(percentile, 1),
            'z_score': round(z_score, 2),
            'category': category,
            'reference_n': ref_stats['n_ref'],
            'reference_mean': ref_stats['mean_eaa'],
            'reference_std': ref_stats['std_eaa']
        }


class CrossTissueNormalizer:
    """
    Cross-tissue normalization for comparing epigenetic ages
    across different tissue types
    """
    
    def __init__(self):
        self.tissue_factors = {
            TissueType.BLOOD: 1.0,
            TissueType.BRAIN_PFC: 1.08,
            TissueType.BRAIN_HIPPO: 1.12,
            TissueType.BRAIN_CEREBELLUM: 1.05,
            TissueType.LIVER: 0.95,
            TissueType.KIDNEY: 0.93,
            TissueType.HEART: 0.97,
            TissueType.LUNG: 0.96,
            TissueType.SKIN: 1.02,
            TissueType.MUSCLE: 0.94,
            TissueType.ADIPOSE: 0.91,
            TissueType.SALIVA: 1.01
        }
        
    def normalize_to_blood(
        self,
        epigenetic_age: float,
        source_tissue: TissueType
    ) -> float:
        """Normalize tissue-specific age to blood-equivalent"""
        factor = self.tissue_factors.get(source_tissue, 1.0)
        return epigenetic_age / factor
    
    def normalize_between_tissues(
        self,
        epigenetic_age: float,
        source_tissue: TissueType,
        target_tissue: TissueType
    ) -> float:
        """Convert epigenetic age between two tissue types"""
        source_factor = self.tissue_factors.get(source_tissue, 1.0)
        target_factor = self.tissue_factors.get(target_tissue, 1.0)
        
        blood_equivalent = epigenetic_age / source_factor
        target_age = blood_equivalent * target_factor
        
        return target_age
    
    def get_normalization_table(self) -> pd.DataFrame:
        """Get table of normalization factors"""
        data = []
        for tissue, factor in self.tissue_factors.items():
            data.append({
                'Doku': tissue.value.replace('_', ' ').title(),
                'Normalizasyon Faktörü': factor,
                'Kan Eşdeğeri Çarpanı': 1/factor if factor != 0 else np.nan
            })
        return pd.DataFrame(data)


class TissueAgeDiscordanceAnalyzer:
    """
    Analyze discordance between tissue-specific epigenetic ages
    to identify tissue-specific aging patterns
    """
    
    def __init__(self):
        self.calculator = TissueSpecificClockCalculator()
        self.normalizer = CrossTissueNormalizer()
        
    def analyze_discordance(
        self,
        tissue_ages: Dict[TissueType, float],
        chronological_age: float
    ) -> Dict[str, Any]:
        """
        Analyze discordance patterns across tissues
        
        Args:
            tissue_ages: Dict of tissue type to epigenetic age
            chronological_age: Known chronological age
            
        Returns:
            Discordance analysis results
        """
        normalized_ages = {}
        eaa_values = {}
        
        for tissue, age in tissue_ages.items():
            norm_age = self.normalizer.normalize_to_blood(age, tissue)
            normalized_ages[tissue] = norm_age
            eaa_values[tissue] = age - chronological_age
        
        ages_array = np.array(list(normalized_ages.values()))
        mean_age = np.mean(ages_array)
        std_age = np.std(ages_array)
        cv = (std_age / mean_age) * 100 if mean_age > 0 else 0
        
        max_tissue = max(eaa_values, key=eaa_values.get)
        min_tissue = min(eaa_values, key=eaa_values.get)
        max_discordance = eaa_values[max_tissue] - eaa_values[min_tissue]
        
        if cv < 5:
            pattern = "Homojen yaşlanma"
            interpretation = "Tüm dokular benzer hızda yaşlanmaktadır."
        elif cv < 10:
            pattern = "Hafif heterojen"
            interpretation = "Dokular arasında hafif yaşlanma farklılıkları mevcuttur."
        elif cv < 20:
            pattern = "Orta heterojen"
            interpretation = "Bazı dokular belirgin şekilde farklı yaşlanma göstermektedir."
        else:
            pattern = "Yüksek heterojen"
            interpretation = "Dokular arasında ciddi yaşlanma farklılıkları mevcuttur."
        
        return {
            'normalized_ages': {t.value: round(a, 2) for t, a in normalized_ages.items()},
            'eaa_values': {t.value: round(a, 2) for t, a in eaa_values.items()},
            'mean_normalized_age': round(mean_age, 2),
            'std_normalized_age': round(std_age, 2),
            'coefficient_of_variation': round(cv, 2),
            'max_discordance': round(max_discordance, 2),
            'fastest_aging_tissue': max_tissue.value,
            'slowest_aging_tissue': min_tissue.value,
            'pattern': pattern,
            'interpretation': interpretation
        }
    
    def identify_accelerated_tissues(
        self,
        tissue_ages: Dict[TissueType, float],
        chronological_age: float,
        threshold_years: float = 3.0
    ) -> List[Dict[str, Any]]:
        """Identify tissues with significant age acceleration"""
        accelerated = []
        
        for tissue, age in tissue_ages.items():
            eaa = age - chronological_age
            ref_info = self.calculator.get_tissue_reference_percentile(eaa, tissue)
            
            if eaa > threshold_years or ref_info['percentile'] > 90:
                accelerated.append({
                    'tissue': tissue.value,
                    'eaa': round(eaa, 2),
                    'percentile': ref_info['percentile'],
                    'z_score': ref_info['z_score'],
                    'severity': 'Yüksek' if eaa > threshold_years * 2 else 'Orta'
                })
        
        return sorted(accelerated, key=lambda x: x['eaa'], reverse=True)


def get_tissue_clock_summary() -> pd.DataFrame:
    """Get summary table of all available tissue-specific clocks"""
    registry = TissueSpecificClockRegistry()
    clocks = registry.list_available_clocks()
    
    df = pd.DataFrame(clocks)
    df.columns = ['Doku', 'Saat Adı', 'CpG Sayısı', 'MAE (yıl)', 'R²', 'Yaş Aralığı']
    df['Yaş Aralığı'] = df['Yaş Aralığı'].apply(lambda x: f"{x[0]}-{x[1]}")
    
    return df
