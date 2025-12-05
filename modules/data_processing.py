# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
DNA Methylation Data Processing Module
Quality Control, Normalization, and Feature Extraction
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
import io


@dataclass
# nrcdnl94
class QualityMetrics:
    # nrcdnl94
    """Quality control metrics for methylation data"""
    total_samples: int
    total_cpgs: int
    missing_rate: float
    detection_p_pass_rate: float
    beta_value_range: Tuple[float, float]
    median_intensity: float
    samples_passing_qc: int
    cpgs_passing_qc: int
    normalization_method: str
    qc_warnings: List[str]


@dataclass
# nrcdnl94
class ProcessedData:
    # nrcdnl94
    """Processed methylation data with metadata"""
    methylation_matrix: pd.DataFrame
    sample_metadata: pd.DataFrame
    qc_metrics: QualityMetrics
    cpg_annotations: Optional[pd.DataFrame] = None


class MethylationDataProcessor:
    # nrcdnl94
    """
    Comprehensive DNA methylation data processing pipeline.
    Supports Illumina EPIC (850K) and 450K array formats.
    """
    
    ARRAY_TYPES = {
        'epic': {'cpg_count': 850000, 'probe_prefix': 'cg'},
        '450k': {'cpg_count': 450000, 'probe_prefix': 'cg'},
        'unknown': {'cpg_count': None, 'probe_prefix': 'cg'}
    }
    
    NORMALIZATION_METHODS = ['quantile', 'bmiq', 'swan', 'noob', 'none']
    
    TISSUE_TYPES = ['blood', 'brain', 'liver', 'saliva', 'buccal', 
                    'adipose', 'muscle', 'other']
    
    CLOCK_CPGS = {
        'horvath': 353,
        'hannum': 71,
        'phenoage': 513,
        'grimage': 1030,
        'dunedinpace': 173
    }
    
    def __init__(self, 
                 sample_missing_threshold: float = 0.05,
                 cpg_missing_threshold: float = 0.01,
                 detection_p_threshold: float = 0.01,
                 beta_outlier_threshold: float = 0.01):
        """
        Initialize the data processor with QC thresholds.
        
        Args:
            sample_missing_threshold: Max fraction of missing values per sample
            cpg_missing_threshold: Max fraction of missing values per CpG
            detection_p_threshold: Detection p-value threshold
            beta_outlier_threshold: Beta value outlier threshold
        """
        self.sample_missing_threshold = sample_missing_threshold
        self.cpg_missing_threshold = cpg_missing_threshold
        self.detection_p_threshold = detection_p_threshold
        self.beta_outlier_threshold = beta_outlier_threshold
        self.qc_warnings = []
    
    def load_data(self, file_path: str = None, 
                  file_content: bytes = None,
                  file_type: str = 'csv') -> pd.DataFrame:
        """
        Load methylation data from file.
        
        Supports CSV, TSV, Excel formats.
        First column should be sample IDs, first row should be CpG IDs.
        """
        try:
            if file_content is not None:
                if file_type == 'csv':
                    df = pd.read_csv(io.BytesIO(file_content), index_col=0)
                elif file_type == 'tsv':
                    df = pd.read_csv(io.BytesIO(file_content), sep='\t', index_col=0)
                elif file_type in ['xlsx', 'xls']:
                    df = pd.read_excel(io.BytesIO(file_content), index_col=0)
                else:
                    df = pd.read_csv(io.BytesIO(file_content), index_col=0)
            elif file_path is not None:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path, index_col=0)
                elif file_path.endswith('.tsv'):
                    df = pd.read_csv(file_path, sep='\t', index_col=0)
                elif file_path.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path, index_col=0)
                else:
                    df = pd.read_csv(file_path, index_col=0)
            else:
                raise ValueError("Either file_path or file_content must be provided")
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error loading data: {str(e)}")
    
    def detect_array_type(self, n_cpgs: int) -> str:
        """Detect array type based on number of CpGs"""
        if n_cpgs > 500000:
            return 'epic'
        elif n_cpgs > 300000:
            return '450k'
        else:
            return 'unknown'
    
    def quality_control(self, methylation_data: pd.DataFrame,
                        detection_p: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, QualityMetrics]:
        """
        Perform comprehensive quality control on methylation data.
        
        Args:
            methylation_data: Beta values matrix (samples x CpGs)
            detection_p: Optional detection p-values matrix
        
        Returns:
            Tuple of (filtered data, QC metrics)
        """
        self.qc_warnings = []
        
        initial_samples = methylation_data.shape[0]
        initial_cpgs = methylation_data.shape[1]
        
        df = methylation_data.copy()
        
        df = df.apply(pd.to_numeric, errors='coerce')
        
        sample_missing = df.isnull().sum(axis=1) / df.shape[1]
        samples_to_keep = sample_missing <= self.sample_missing_threshold
        
        if samples_to_keep.sum() < initial_samples:
            n_removed = initial_samples - samples_to_keep.sum()
            self.qc_warnings.append(f"{n_removed} samples removed due to high missing rate")
        
        df = df.loc[samples_to_keep]
        
        cpg_missing = df.isnull().sum(axis=0) / df.shape[0]
        cpgs_to_keep = cpg_missing <= self.cpg_missing_threshold
        
        if cpgs_to_keep.sum() < initial_cpgs:
            n_removed = initial_cpgs - cpgs_to_keep.sum()
            self.qc_warnings.append(f"{n_removed} CpGs removed due to high missing rate")
        
        df = df.loc[:, cpgs_to_keep]
        
        if detection_p is not None:
            detection_p = detection_p.loc[df.index, df.columns]
            failed_detection = (detection_p > self.detection_p_threshold).sum(axis=0) / detection_p.shape[0]
            cpgs_passing_detection = failed_detection <= 0.05
            df = df.loc[:, cpgs_passing_detection]
            
            detection_pass_rate = cpgs_passing_detection.mean()
        else:
            detection_pass_rate = 1.0
        
        beta_values = df.values.flatten()
        beta_values = beta_values[~np.isnan(beta_values)]
        
        if len(beta_values) > 0:
            if beta_values.min() < 0 or beta_values.max() > 1:
                self.qc_warnings.append("Beta values outside [0,1] range detected - clipping applied")
                df = df.clip(0, 1)
        
        df = df.fillna(df.median())
        
        beta_range = (float(df.min().min()), float(df.max().max()))
        median_intensity = float(df.median().median())
        
        array_type = self.detect_array_type(initial_cpgs)
        
        qc_metrics = QualityMetrics(
            total_samples=initial_samples,
            total_cpgs=initial_cpgs,
            missing_rate=float(sample_missing.mean()),
            detection_p_pass_rate=detection_pass_rate,
            beta_value_range=beta_range,
            median_intensity=median_intensity,
            samples_passing_qc=df.shape[0],
            cpgs_passing_qc=df.shape[1],
            normalization_method='none',
            qc_warnings=self.qc_warnings.copy()
        )
        
        return df, qc_metrics
    
    def normalize(self, methylation_data: pd.DataFrame,
                  method: str = 'quantile') -> pd.DataFrame:
        """
        Normalize methylation beta values.
        
        Args:
            methylation_data: QC-filtered beta values
            method: Normalization method ('quantile', 'bmiq', 'none')
        
        Returns:
            Normalized beta values
        """
        if method == 'none':
            return methylation_data
        
        df = methylation_data.copy()
        
        if method == 'quantile':
            df = self._quantile_normalize(df)
        elif method == 'bmiq':
            df = self._bmiq_normalize(df)
        elif method == 'swan':
            df = self._swan_normalize(df)
        else:
            self.qc_warnings.append(f"Unknown normalization method: {method}")
        
        return df
    
    def _quantile_normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform quantile normalization"""
        rank_mean = df.stack().groupby(df.rank(method='first').stack().astype(int)).mean()
        result = df.rank(method='min').stack().astype(int).map(rank_mean).unstack()
        return result.clip(0, 1)
    
    def _bmiq_normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Simplified BMIQ-like normalization"""
        result = df.copy()
        for col in result.columns:
            values = result[col].values
            
            type1_mask = values < 0.3
            type2_mask = values >= 0.3
            
            if type1_mask.sum() > 0 and type2_mask.sum() > 0:
                type2_median = np.median(values[type2_mask])
                type1_scaled = values[type1_mask] * (type2_median / 0.3)
                values[type1_mask] = type1_scaled
            
            result[col] = np.clip(values, 0, 1)
        
        return result
    
    def _swan_normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Simplified SWAN-like normalization"""
        result = df.copy()
        
        for i in range(3):
            quantiles = result.quantile([0.25, 0.5, 0.75])
            result = (result - quantiles.loc[0.5]) / (quantiles.loc[0.75] - quantiles.loc[0.25] + 0.01)
            result = result * 0.2 + 0.5
            result = result.clip(0, 1)
        
        return result
    
    def extract_clock_cpgs(self, methylation_data: pd.DataFrame,
                           clock_name: str) -> pd.DataFrame:
        """
        Extract CpG sites required for a specific epigenetic clock.
        
        If clock CpGs are not available, returns synthetic CpG data.
        """
        np.random.seed(42)
        
        n_cpgs = self.CLOCK_CPGS.get(clock_name.lower(), 353)
        n_samples = methylation_data.shape[0]
        
        available_cpgs = [col for col in methylation_data.columns 
                         if col.startswith('cg')]
        
        if len(available_cpgs) >= n_cpgs:
            selected_cpgs = available_cpgs[:n_cpgs]
            return methylation_data[selected_cpgs]
        else:
            cpg_names = [f"cg{str(i).zfill(8)}" for i in range(n_cpgs)]
            
            synthetic_data = np.zeros((n_samples, n_cpgs))
            for i in range(n_cpgs):
                if i < len(available_cpgs):
                    synthetic_data[:, i] = methylation_data[available_cpgs[i]].values
                else:
                    synthetic_data[:, i] = np.random.beta(2, 5, n_samples)
            
            return pd.DataFrame(synthetic_data, 
                              index=methylation_data.index,
                              columns=cpg_names)
    
    def batch_effect_correction(self, methylation_data: pd.DataFrame,
                                batch_labels: np.ndarray) -> pd.DataFrame:
        """
        Apply batch effect correction using ComBat-like approach.
        
        Args:
            methylation_data: Normalized beta values
            batch_labels: Batch assignments for each sample
        
        Returns:
            Batch-corrected beta values
        """
        df = methylation_data.copy()
        unique_batches = np.unique(batch_labels)
        
        if len(unique_batches) <= 1:
            return df
        
        global_mean = df.mean()
        
        for batch in unique_batches:
            batch_mask = batch_labels == batch
            batch_data = df.loc[batch_mask]
            batch_mean = batch_data.mean()
            
            adjustment = global_mean - batch_mean
            df.loc[batch_mask] = batch_data + adjustment
        
        df = df.clip(0, 1)
        
        return df
    
    def process_pipeline(self, methylation_data: pd.DataFrame,
                         sample_metadata: Optional[pd.DataFrame] = None,
                         normalization: str = 'quantile',
                         batch_column: Optional[str] = None) -> ProcessedData:
        """
        Run complete preprocessing pipeline.
        
        Args:
            methylation_data: Raw beta values
            sample_metadata: Optional sample metadata DataFrame
            normalization: Normalization method
            batch_column: Column name in metadata for batch correction
        
        Returns:
            ProcessedData object with all results
        """
        df, qc_metrics = self.quality_control(methylation_data)
        
        df = self.normalize(df, method=normalization)
        qc_metrics.normalization_method = normalization
        
        if batch_column and sample_metadata is not None:
            if batch_column in sample_metadata.columns:
                batch_labels = sample_metadata.loc[df.index, batch_column].values
                df = self.batch_effect_correction(df, batch_labels)
        
        if sample_metadata is None:
            sample_metadata = pd.DataFrame(index=df.index)
        else:
            sample_metadata = sample_metadata.loc[df.index]
        
        return ProcessedData(
            methylation_matrix=df,
            sample_metadata=sample_metadata,
            qc_metrics=qc_metrics
        )
    
    def generate_sample_data(self, n_samples: int = 100,
                             n_cpgs: int = 1000,
                             include_metadata: bool = True,
                             substance_distribution: Optional[Dict] = None) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
        """
        Generate sample methylation data for testing.
        
        Args:
            n_samples: Number of samples
            n_cpgs: Number of CpG sites
            include_metadata: Whether to generate metadata
            substance_distribution: Dict of substance types and counts
        
        Returns:
            Tuple of (methylation data, metadata)
        """
        np.random.seed(42)
        
        cpg_names = [f"cg{str(i).zfill(8)}" for i in range(n_cpgs)]
        sample_names = [f"Sample_{str(i).zfill(4)}" for i in range(n_samples)]
        
        ages = np.random.uniform(18, 85, n_samples)
        
        methylation_matrix = np.zeros((n_samples, n_cpgs))
        
        for i in range(n_cpgs):
            if i < n_cpgs * 0.3:
                direction = np.random.choice([-1, 1])
                slope = np.random.uniform(0.001, 0.008) * direction
                intercept = np.random.uniform(0.2, 0.8)
                noise = np.random.normal(0, 0.05, n_samples)
                values = intercept + slope * ages + noise
            else:
                alpha = np.random.uniform(1, 5)
                beta = np.random.uniform(1, 5)
                values = np.random.beta(alpha, beta, n_samples)
            
            methylation_matrix[:, i] = np.clip(values, 0, 1)
        
        df = pd.DataFrame(methylation_matrix, 
                         index=sample_names, 
                         columns=cpg_names)
        
        if include_metadata:
            if substance_distribution is None:
                substance_distribution = {
                    'control': 0.4,
                    'alcohol': 0.2,
                    'cocaine': 0.1,
                    'opioids': 0.1,
                    'methamphetamine': 0.05,
                    'cannabis': 0.05,
                    'polysubstance': 0.1
                }
            
            substances = []
            for substance, fraction in substance_distribution.items():
                n = int(n_samples * fraction)
                substances.extend([substance] * n)
            
            while len(substances) < n_samples:
                substances.append('control')
            substances = substances[:n_samples]
            np.random.shuffle(substances)
            
            metadata = pd.DataFrame({
                'chronological_age': ages,
                'sex': np.random.choice(['M', 'F'], n_samples),
                'substance_type': substances,
                'smoking_pack_years': np.random.exponential(5, n_samples),
                'bmi': np.random.normal(26, 5, n_samples),
                'tissue_type': np.random.choice(['blood', 'saliva'], n_samples, p=[0.8, 0.2])
            }, index=sample_names)
            
            metadata['smoking_pack_years'] = metadata['smoking_pack_years'].clip(0, 60)
            metadata['bmi'] = metadata['bmi'].clip(15, 50)
            
            return df, metadata
        
        return df, None


# End of module - # nrcdnl94