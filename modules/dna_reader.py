# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
DNA Methylation Data Reader Module
Supports multiple formats: IDAT, CSV, TXT, Excel, GEO datasets

This module provides comprehensive support for reading DNA methylation data
from Illumina EPIC (850K) and 450K arrays.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import io
import re
import warnings


@dataclass
# nrcdnl94
class MethylationSample:
    # nrcdnl94
    """Represents a single DNA methylation sample"""
    sample_id: str
    beta_values: pd.Series
    chronological_age: Optional[float] = None
    sex: Optional[str] = None
    tissue_type: Optional[str] = None
    substance_type: Optional[str] = None
    metadata: Optional[Dict] = None
    array_type: Optional[str] = None
    cpg_count: int = 0
    quality_score: float = 0.0


@dataclass
# nrcdnl94
class MethylationDataset:
    # nrcdnl94
    """Represents a complete methylation dataset"""
    samples: List[MethylationSample]
    beta_matrix: pd.DataFrame
    sample_info: pd.DataFrame
    cpg_annotations: Optional[pd.DataFrame] = None
    array_type: str = "Unknown"
    source: str = "Unknown"
    quality_metrics: Optional[Dict] = None


class DNAMethylationReader:
    # nrcdnl94
    """
    Comprehensive DNA Methylation Data Reader
    
    Supported formats:
    - Illumina IDAT files (raw array data)
    - CSV/TXT beta value matrices
    - Excel files (.xlsx, .xls)
    - GEO Series Matrix files
    - Sesame/minfi output formats
    """
    
    SUPPORTED_ARRAYS = {
        'EPIC': {
            'cpg_count': 865918,
            'name': 'Illumina MethylationEPIC (850K)',
            'probes_prefix': ['cg', 'ch', 'rs']
        },
        'EPIC_V2': {
            'cpg_count': 937396,
            'name': 'Illumina MethylationEPIC v2.0',
            'probes_prefix': ['cg', 'ch', 'rs', 'nv']
        },
        '450K': {
            'cpg_count': 485512,
            'name': 'Illumina HumanMethylation450',
            'probes_prefix': ['cg', 'ch', 'rs']
        },
        '27K': {
            'cpg_count': 27578,
            'name': 'Illumina HumanMethylation27',
            'probes_prefix': ['cg']
        }
    }
    
    CLOCK_REQUIRED_CPGS = {
        'horvath': 353,
        'hannum': 71,
        'phenoage': 513,
        'grimage': 1030,
        'dunedinpace': 173
    }
    
    def __init__(self):
        self.last_error = None
        self.warnings = []
    
    def read_csv(self, file_path_or_buffer: Union[str, Path, io.BytesIO],
                 sample_column: str = None,
                 cpg_column: str = None,
                 transpose: bool = False,
                 sep: str = ',') -> MethylationDataset:
        """
        Read methylation data from CSV file
        
        Args:
            file_path_or_buffer: Path to CSV file or file buffer
            sample_column: Column name containing sample IDs (auto-detect if None)
            cpg_column: Column name for CpG identifiers (auto-detect if None)
            transpose: If True, samples are columns and CpGs are rows
            sep: Separator character
            
        Returns:
            MethylationDataset object
        """
        try:
            if isinstance(file_path_or_buffer, (str, Path)):
                df = pd.read_csv(file_path_or_buffer, sep=sep, index_col=0)
            else:
                df = pd.read_csv(file_path_or_buffer, sep=sep, index_col=0)
            
            if transpose:
                df = df.T
            
            df = self._detect_and_orient_data(df)
            
            beta_matrix = self._extract_beta_values(df)
            
            array_type = self._detect_array_type(beta_matrix)
            
            quality_metrics = self._calculate_quality_metrics(beta_matrix)
            
            samples = self._create_samples_from_matrix(beta_matrix, array_type)
            
            sample_info = pd.DataFrame({
                'sample_id': beta_matrix.columns.tolist(),
                'cpg_count': [len(beta_matrix)] * len(beta_matrix.columns),
                'array_type': [array_type] * len(beta_matrix.columns)
            })
            
            return MethylationDataset(
                samples=samples,
                beta_matrix=beta_matrix,
                sample_info=sample_info,
                array_type=array_type,
                source="CSV",
                quality_metrics=quality_metrics
            )
            
        except Exception as e:
            self.last_error = str(e)
            raise ValueError(f"Error reading CSV: {e}")
    
    def read_txt(self, file_path_or_buffer: Union[str, Path, io.BytesIO],
                 sep: str = '\t') -> MethylationDataset:
        """Read methylation data from tab-separated TXT file"""
        return self.read_csv(file_path_or_buffer, sep=sep)
    
    def read_excel(self, file_path_or_buffer: Union[str, Path, io.BytesIO],
                   sheet_name: Union[str, int] = 0) -> MethylationDataset:
        """
        Read methylation data from Excel file
        
        Args:
            file_path_or_buffer: Path to Excel file or buffer
            sheet_name: Sheet name or index to read
            
        Returns:
            MethylationDataset object
        """
        try:
            df = pd.read_excel(file_path_or_buffer, sheet_name=sheet_name, index_col=0)
            
            df = self._detect_and_orient_data(df)
            beta_matrix = self._extract_beta_values(df)
            array_type = self._detect_array_type(beta_matrix)
            quality_metrics = self._calculate_quality_metrics(beta_matrix)
            samples = self._create_samples_from_matrix(beta_matrix, array_type)
            
            sample_info = pd.DataFrame({
                'sample_id': beta_matrix.columns.tolist(),
                'cpg_count': [len(beta_matrix)] * len(beta_matrix.columns),
                'array_type': [array_type] * len(beta_matrix.columns)
            })
            
            return MethylationDataset(
                samples=samples,
                beta_matrix=beta_matrix,
                sample_info=sample_info,
                array_type=array_type,
                source="Excel",
                quality_metrics=quality_metrics
            )
            
        except Exception as e:
            self.last_error = str(e)
            raise ValueError(f"Error reading Excel: {e}")
    
    def read_geo_matrix(self, file_path_or_buffer: Union[str, Path, io.BytesIO]) -> MethylationDataset:
        """
        Read GEO Series Matrix file format
        
        GEO files typically have:
        - Header lines starting with !
        - Sample annotations
        - Expression/methylation matrix
        
        Args:
            file_path_or_buffer: Path to GEO matrix file
            
        Returns:
            MethylationDataset object
        """
        try:
            if isinstance(file_path_or_buffer, (str, Path)):
                with open(file_path_or_buffer, 'r') as f:
                    lines = f.readlines()
            else:
                lines = file_path_or_buffer.read().decode('utf-8').split('\n')
            
            metadata = {}
            data_start = 0
            
            for i, line in enumerate(lines):
                if line.startswith('!'):
                    key_match = re.match(r'!(\w+)\s*=\s*(.+)', line.strip())
                    if key_match:
                        metadata[key_match.group(1)] = key_match.group(2)
                elif line.startswith('"ID_REF"') or line.startswith('ID_REF'):
                    data_start = i
                    break
            
            data_lines = '\n'.join(lines[data_start:])
            df = pd.read_csv(io.StringIO(data_lines), sep='\t', index_col=0)
            
            df = self._extract_beta_values(df)
            array_type = self._detect_array_type(df)
            quality_metrics = self._calculate_quality_metrics(df)
            samples = self._create_samples_from_matrix(df, array_type)
            
            sample_info = pd.DataFrame({
                'sample_id': df.columns.tolist(),
                'cpg_count': [len(df)] * len(df.columns),
                'array_type': [array_type] * len(df.columns),
                'geo_accession': metadata.get('Series_geo_accession', 'Unknown')
            })
            
            return MethylationDataset(
                samples=samples,
                beta_matrix=df,
                sample_info=sample_info,
                array_type=array_type,
                source=f"GEO: {metadata.get('Series_geo_accession', 'Unknown')}",
                quality_metrics=quality_metrics
            )
            
        except Exception as e:
            self.last_error = str(e)
            raise ValueError(f"Error reading GEO matrix: {e}")
    
    def read_idat_summary(self, manifest_path: Union[str, Path, io.BytesIO]) -> MethylationDataset:
        """
        Read pre-processed IDAT summary (beta values exported from minfi/sesame)
        
        Note: Raw IDAT parsing requires specialized libraries (minfi in R).
        This function reads the exported beta value matrices.
        
        Args:
            manifest_path: Path to beta values file exported from IDAT processing
            
        Returns:
            MethylationDataset object
        """
        return self.read_csv(manifest_path, sep=',')
    
    def read_from_streamlit_upload(self, uploaded_file) -> MethylationDataset:
        """
        Read methylation data from Streamlit file uploader
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            MethylationDataset object
        """
        file_name = uploaded_file.name.lower()
        
        if file_name.endswith('.csv'):
            return self.read_csv(io.BytesIO(uploaded_file.read()))
        elif file_name.endswith('.txt') or file_name.endswith('.tsv'):
            return self.read_txt(io.BytesIO(uploaded_file.read()))
        elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            return self.read_excel(io.BytesIO(uploaded_file.read()))
        elif 'series_matrix' in file_name or file_name.endswith('.soft'):
            return self.read_geo_matrix(io.BytesIO(uploaded_file.read()))
        else:
            return self.read_csv(io.BytesIO(uploaded_file.read()))
    
    def _detect_and_orient_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect data orientation and standardize (CpGs as rows, samples as columns)
        """
        index_cpg_ratio = sum(str(idx).startswith('cg') for idx in df.index[:100]) / min(100, len(df.index))
        col_cpg_ratio = sum(str(col).startswith('cg') for col in df.columns[:100]) / min(100, len(df.columns))
        
        if col_cpg_ratio > index_cpg_ratio:
            df = df.T
            
        return df
    
    def _extract_beta_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract and validate beta values (0-1 range)
        """
        cpg_rows = [idx for idx in df.index if str(idx).startswith(('cg', 'ch', 'rs'))]
        
        if len(cpg_rows) > 0:
            df = df.loc[cpg_rows]
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df = df[numeric_cols]
        
        if df.max().max() > 1.5:
            self.warnings.append("M-values detected, converting to beta values")
            df = 2**df / (2**df + 1)
        
        df = df.clip(0, 1)
        
        return df
    
    def _detect_array_type(self, beta_matrix: pd.DataFrame) -> str:
        """Detect Illumina array type based on CpG count"""
        cpg_count = len(beta_matrix)
        
        if cpg_count > 800000:
            return 'EPIC_V2' if cpg_count > 900000 else 'EPIC'
        elif cpg_count > 400000:
            return '450K'
        elif cpg_count > 25000:
            return '27K'
        else:
            return 'Subset'
    
    def _calculate_quality_metrics(self, beta_matrix: pd.DataFrame) -> Dict:
        """Calculate quality control metrics"""
        metrics = {
            'total_cpgs': len(beta_matrix),
            'total_samples': len(beta_matrix.columns),
            'missing_rate': beta_matrix.isna().sum().sum() / (beta_matrix.shape[0] * beta_matrix.shape[1]),
            'mean_beta': beta_matrix.mean().mean(),
            'std_beta': beta_matrix.std().mean(),
            'clock_coverage': {}
        }
        
        for clock_name, required_cpgs in self.CLOCK_REQUIRED_CPGS.items():
            coverage = min(len(beta_matrix), required_cpgs) / required_cpgs * 100
            metrics['clock_coverage'][clock_name] = round(coverage, 2)
        
        return metrics
    
    def _create_samples_from_matrix(self, beta_matrix: pd.DataFrame, 
                                    array_type: str) -> List[MethylationSample]:
        """Create MethylationSample objects from beta matrix"""
        samples = []
        
        for col in beta_matrix.columns:
            sample = MethylationSample(
                sample_id=str(col),
                beta_values=beta_matrix[col],
                array_type=array_type,
                cpg_count=len(beta_matrix),
                quality_score=1.0 - beta_matrix[col].isna().mean()
            )
            samples.append(sample)
        
        return samples
    
    def validate_for_clocks(self, dataset: MethylationDataset, 
                           clocks: List[str] = None) -> Dict:
        """
        Validate dataset for epigenetic clock calculations
        
        Args:
            dataset: MethylationDataset to validate
            clocks: List of clock names to check (default: all)
            
        Returns:
            Validation report dictionary
        """
        if clocks is None:
            clocks = list(self.CLOCK_REQUIRED_CPGS.keys())
        
        from .published_coefficients import (
            HORVATH_353_COEFFICIENTS,
            HANNUM_71_COEFFICIENTS,
            PHENOAGE_513_TOP_COEFFICIENTS,
            DUNEDINPACE_173_COEFFICIENTS
        )
        
        clock_cpgs = {
            'horvath': set(HORVATH_353_COEFFICIENTS.keys()),
            'hannum': set(HANNUM_71_COEFFICIENTS.keys()),
            'phenoage': set(PHENOAGE_513_TOP_COEFFICIENTS.keys()),
            'dunedinpace': set(DUNEDINPACE_173_COEFFICIENTS.keys())
        }
        
        dataset_cpgs = set(dataset.beta_matrix.index)
        
        report = {
            'valid': True,
            'clocks': {},
            'recommendations': []
        }
        
        for clock in clocks:
            if clock in clock_cpgs:
                required = clock_cpgs[clock]
                available = required.intersection(dataset_cpgs)
                coverage = len(available) / len(required) * 100
                
                report['clocks'][clock] = {
                    'required_cpgs': len(required),
                    'available_cpgs': len(available),
                    'coverage_percent': round(coverage, 2),
                    'missing_cpgs': list(required - available)[:10],
                    'can_calculate': coverage >= 80
                }
                
                if coverage < 80:
                    report['valid'] = False
                    report['recommendations'].append(
                        f"{clock}: Only {coverage:.1f}% CpG coverage. Consider imputation."
                    )
        
        return report
    
    def impute_missing_cpgs(self, dataset: MethylationDataset,
                           method: str = 'mean') -> MethylationDataset:
        """
        Impute missing CpG values
        
        Args:
            dataset: MethylationDataset with missing values
            method: Imputation method ('mean', 'median', 'knn')
            
        Returns:
            MethylationDataset with imputed values
        """
        beta_matrix = dataset.beta_matrix.copy()
        
        if method == 'mean':
            beta_matrix = beta_matrix.fillna(beta_matrix.mean())
        elif method == 'median':
            beta_matrix = beta_matrix.fillna(beta_matrix.median())
        elif method == 'knn':
            from sklearn.impute import KNNImputer
            imputer = KNNImputer(n_neighbors=5)
            imputed = imputer.fit_transform(beta_matrix.T)
            beta_matrix = pd.DataFrame(
                imputed.T,
                index=beta_matrix.index,
                columns=beta_matrix.columns
            )
        
        beta_matrix = beta_matrix.fillna(0.5)
        
        dataset.beta_matrix = beta_matrix
        dataset.samples = self._create_samples_from_matrix(beta_matrix, dataset.array_type)
        
        return dataset


class SampleAnnotationParser:
    # nrcdnl94
    """Parse sample annotation files to extract metadata"""
    
    @staticmethod
    def parse_sample_sheet(file_path: Union[str, Path, io.BytesIO]) -> pd.DataFrame:
        """
        Parse Illumina Sample Sheet format
        
        Returns DataFrame with sample metadata
        """
        if isinstance(file_path, (str, Path)):
            with open(file_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = file_path.read().decode('utf-8').split('\n')
        
        data_start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('[Data]'):
                data_start = i + 1
                break
        
        data_lines = '\n'.join(lines[data_start:])
        df = pd.read_csv(io.StringIO(data_lines))
        
        return df
    
    @staticmethod
    def parse_phenotype_file(file_path: Union[str, Path, io.BytesIO],
                            sample_id_col: str = 'Sample_ID',
                            age_col: str = 'Age',
                            sex_col: str = 'Sex') -> pd.DataFrame:
        """
        Parse phenotype/clinical data file
        
        Returns DataFrame with parsed phenotype data
        """
        if isinstance(file_path, (str, Path)):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_csv(file_path)
        
        col_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'sample' in col_lower or 'id' in col_lower:
                col_mapping[col] = 'sample_id'
            elif 'age' in col_lower:
                col_mapping[col] = 'age'
            elif 'sex' in col_lower or 'gender' in col_lower:
                col_mapping[col] = 'sex'
            elif 'tissue' in col_lower:
                col_mapping[col] = 'tissue'
            elif 'substance' in col_lower or 'drug' in col_lower:
                col_mapping[col] = 'substance'
        
        df = df.rename(columns=col_mapping)
        
        return df


def calculate_epigenetic_age(dataset: MethylationDataset) -> pd.DataFrame:
    """
    Calculate epigenetic age using published clock coefficients
    
    Args:
        dataset: MethylationDataset with beta values
        
    Returns:
        DataFrame with calculated ages for each clock
    """
    from .published_coefficients import (
        HORVATH_353_COEFFICIENTS,
        HANNUM_71_COEFFICIENTS,
        PHENOAGE_513_TOP_COEFFICIENTS,
        DUNEDINPACE_173_COEFFICIENTS
    )
    
    beta_matrix = dataset.beta_matrix
    results = []
    
    for sample in dataset.samples:
        sample_id = sample.sample_id
        beta_values = beta_matrix[sample_id]
        
        # Horvath Clock
        horvath_age = _calculate_clock_age(
            beta_values, 
            HORVATH_353_COEFFICIENTS,
            intercept=0.696,
            transform='anti_trafo'
        )
        
        # Hannum Clock
        hannum_age = _calculate_clock_age(
            beta_values,
            HANNUM_71_COEFFICIENTS,
            intercept=0.0,
            transform='linear'
        )
        
        # PhenoAge Clock
        phenoage = _calculate_clock_age(
            beta_values,
            PHENOAGE_513_TOP_COEFFICIENTS,
            intercept=60.664,
            transform='linear'
        )
        
        # DunedinPACE (pace of aging)
        dunedin_pace = _calculate_clock_age(
            beta_values,
            DUNEDINPACE_173_COEFFICIENTS,
            intercept=1.0,
            transform='linear'
        )
        
        # Calculate coverage for each clock
        horvath_coverage = _calculate_coverage(beta_values, HORVATH_353_COEFFICIENTS)
        hannum_coverage = _calculate_coverage(beta_values, HANNUM_71_COEFFICIENTS)
        phenoage_coverage = _calculate_coverage(beta_values, PHENOAGE_513_TOP_COEFFICIENTS)
        dunedin_coverage = _calculate_coverage(beta_values, DUNEDINPACE_173_COEFFICIENTS)
        
        results.append({
            'sample_id': sample_id,
            'chronological_age': sample.chronological_age,
            'horvath_age': horvath_age,
            'hannum_age': hannum_age,
            'phenoage': phenoage,
            'dunedin_pace': dunedin_pace,
            'horvath_coverage': horvath_coverage,
            'hannum_coverage': hannum_coverage,
            'phenoage_coverage': phenoage_coverage,
            'dunedin_coverage': dunedin_coverage
        })
    
    return pd.DataFrame(results)


def _calculate_clock_age(beta_values: pd.Series, 
    # nrcdnl94
                         coefficients: Dict[str, float],
                         intercept: float = 0.0,
                         transform: str = 'linear') -> float:
    """
    Calculate clock age using weighted sum of CpG beta values
    
    Args:
        beta_values: Series with CpG beta values
        coefficients: Dictionary of CpG -> coefficient
        intercept: Clock intercept value
        transform: 'linear' or 'anti_trafo' (Horvath transformation)
        
    Returns:
        Calculated age
    """
    age = intercept
    matched_cpgs = 0
    
    for cpg, coef in coefficients.items():
        if cpg in beta_values.index:
            beta = beta_values[cpg]
            if not pd.isna(beta):
                age += beta * coef
                matched_cpgs += 1
    
    # Scale if not all CpGs matched
    if matched_cpgs < len(coefficients) and matched_cpgs > 0:
        scale_factor = len(coefficients) / matched_cpgs
        age = intercept + (age - intercept) * min(scale_factor, 1.5)
    
    # Apply Horvath anti-transformation if needed
    if transform == 'anti_trafo':
        # Horvath's anti-transformation: inverse of age transformation
        # Original: transformed_age = log(age+1) - log(21+1) if age <= 20
        #           transformed_age = (age - 20) / (21 + 1) if age > 20
        if age < 0:
            age = (21 + 1) * np.exp(age) - 1
        else:
            age = (21 + 1) * age + 20
    
    return round(max(0, age), 2)


def _calculate_coverage(beta_values: pd.Series, 
    # nrcdnl94
                        coefficients: Dict[str, float]) -> float:
    """Calculate percentage of clock CpGs available in sample"""
    available = sum(1 for cpg in coefficients.keys() if cpg in beta_values.index)
    return round(available / len(coefficients) * 100, 1)


def create_demo_methylation_data(n_samples: int = 10, 
    # nrcdnl94
                                 n_cpgs: int = 1000,
                                 include_clock_cpgs: bool = True) -> MethylationDataset:
    """
    Create demonstration methylation dataset
    
    Args:
        n_samples: Number of samples to generate
        n_cpgs: Number of CpG sites
        include_clock_cpgs: Include CpGs required for clock calculations
        
    Returns:
        MethylationDataset with simulated data
    """
    from .published_coefficients import (
        HORVATH_353_COEFFICIENTS,
        HANNUM_71_COEFFICIENTS,
        DUNEDINPACE_173_COEFFICIENTS
    )
    
    np.random.seed(42)
    
    cpg_names = []
    
    if include_clock_cpgs:
        cpg_names.extend(list(HORVATH_353_COEFFICIENTS.keys())[:100])
        cpg_names.extend(list(HANNUM_71_COEFFICIENTS.keys())[:50])
        cpg_names.extend(list(DUNEDINPACE_173_COEFFICIENTS.keys())[:50])
    
    remaining = n_cpgs - len(cpg_names)
    if remaining > 0:
        cpg_names.extend([f"cg{str(i).zfill(8)}" for i in range(remaining)])
    
    cpg_names = cpg_names[:n_cpgs]
    
    sample_names = [f"Sample_{i+1:03d}" for i in range(n_samples)]
    
    beta_values = np.random.beta(2, 5, size=(len(cpg_names), n_samples))
    
    beta_matrix = pd.DataFrame(
        beta_values,
        index=cpg_names,
        columns=sample_names
    )
    
    ages = np.random.uniform(20, 80, n_samples)
    sexes = np.random.choice(['M', 'F'], n_samples)
    substances = np.random.choice(
        ['control', 'alcohol', 'cocaine', 'opioids', 'cannabis'],
        n_samples,
        p=[0.5, 0.15, 0.1, 0.15, 0.1]
    )
    
    samples = []
    for i, col in enumerate(sample_names):
        sample = MethylationSample(
            sample_id=col,
            beta_values=beta_matrix[col],
            chronological_age=ages[i],
            sex=sexes[i],
            substance_type=substances[i],
            array_type='DEMO',
            cpg_count=len(cpg_names),
            quality_score=0.95 + np.random.uniform(0, 0.05)
        )
        samples.append(sample)
    
    sample_info = pd.DataFrame({
        'sample_id': sample_names,
        'age': ages,
        'sex': sexes,
        'substance': substances,
        'cpg_count': [len(cpg_names)] * n_samples,
        'array_type': ['DEMO'] * n_samples
    })
    
    reader = DNAMethylationReader()
    quality_metrics = reader._calculate_quality_metrics(beta_matrix)
    
    return MethylationDataset(
        samples=samples,
        beta_matrix=beta_matrix,
        sample_info=sample_info,
        array_type='DEMO',
        source='Simulated Demo Data',
        quality_metrics=quality_metrics
    )


# End of module - # nrcdnl94