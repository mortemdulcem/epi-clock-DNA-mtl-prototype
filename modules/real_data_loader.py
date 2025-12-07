# ============================================================================
# EpiClock v4.0 - Real DNA Methylation Data Loader
# CSV, Excel, Parquet Support with Validation
# Author: nrcdnl94
# ============================================================================
"""
Real DNA Methylation Data Loader

Supports:
1. CSV/TSV files (GEO datasets, custom data)
2. Excel files (.xlsx, .xls)
3. Parquet files (large datasets)
4. Automatic CpG site detection and validation

Expected data format:
- Rows: Samples (or CpG sites)
- Columns: CpG sites (or Samples)
- Values: Beta values (0-1) or M-values
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from io import BytesIO, StringIO
import re
import warnings


@dataclass
class LoadedMethylationData:
    """Container for loaded methylation data"""
    data: pd.DataFrame
    n_samples: int
    n_cpgs: int
    sample_ids: List[str]
    cpg_ids: List[str]
    data_type: str
    value_range: Tuple[float, float]
    missing_rate: float
    is_valid: bool
    validation_messages: List[str]
    metadata: Dict[str, Any]


class RealDataLoader:
    """
    Load real DNA methylation data from various file formats
    
    Supports:
    - GEO datasets (GSE format)
    - Custom CSV/Excel files
    - Parquet for large datasets
    
    Automatically detects:
    - Data orientation (samples x CpGs or CpGs x samples)
    - Value type (beta or M-values)
    - CpG naming convention
    """
    
    CG_PATTERN = re.compile(r'^cg\d{7,8}$', re.IGNORECASE)
    CH_PATTERN = re.compile(r'^ch\.\d+\.\d+', re.IGNORECASE)
    
    REQUIRED_OPEN_SOURCE_CPGS = {
        'hannum': [
            'cg00059225', 'cg00075967', 'cg00374717', 'cg00747726', 'cg00945507',
            'cg01019327', 'cg01062963', 'cg01131483', 'cg01234531', 'cg01560885',
            'cg01644124', 'cg01656216', 'cg01873645', 'cg01968178', 'cg02217159',
            'cg02228185', 'cg02332238', 'cg02331561', 'cg02364642', 'cg02388150'
        ],
        'dunedinpace': [
            'cg00006289', 'cg00009053', 'cg00009946', 'cg00011943', 'cg00013374',
            'cg00014837', 'cg00016831', 'cg00017461', 'cg00021109', 'cg00023568',
            'cg00027290', 'cg00028519', 'cg00029685', 'cg00030746', 'cg00031162'
        ]
    }
    
    def __init__(self):
        self.loaded_data = None
        self.original_orientation = None
    
    def load_file(self, file_input: Union[str, BytesIO, Any],
                  file_type: Optional[str] = None,
                  sample_column: Optional[str] = None,
                  transpose: Optional[bool] = None) -> LoadedMethylationData:
        """
        Load methylation data from file
        
        Args:
            file_input: File path, BytesIO object, or Streamlit UploadedFile
            file_type: 'csv', 'tsv', 'excel', 'parquet' (auto-detected if None)
            sample_column: Column name containing sample IDs (auto-detected if None)
            transpose: Whether to transpose data (auto-detected if None)
        
        Returns:
            LoadedMethylationData with validated methylation matrix
        """
        if file_type is None:
            file_type = self._detect_file_type(file_input)
        
        if file_type == 'csv':
            df = self._load_csv(file_input, delimiter=',')
        elif file_type == 'tsv':
            df = self._load_csv(file_input, delimiter='\t')
        elif file_type == 'excel':
            df = self._load_excel(file_input)
        elif file_type == 'parquet':
            df = self._load_parquet(file_input)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        df, sample_ids = self._extract_sample_ids(df, sample_column)
        
        needs_transpose = self._detect_orientation(df) if transpose is None else transpose
        if needs_transpose:
            df = df.T
            self.original_orientation = 'cpgs_as_rows'
        else:
            self.original_orientation = 'samples_as_rows'
        
        df = self._clean_data(df)
        
        validation_result = self._validate_data(df)
        
        cpg_ids = list(df.columns)
        if sample_ids is None:
            sample_ids = list(df.index)
        
        value_range = (df.values.min(), df.values.max())
        missing_rate = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        
        clock_coverage = self._check_clock_coverage(cpg_ids)
        
        self.loaded_data = LoadedMethylationData(
            data=df,
            n_samples=df.shape[0],
            n_cpgs=df.shape[1],
            sample_ids=sample_ids if isinstance(sample_ids, list) else list(sample_ids),
            cpg_ids=cpg_ids,
            data_type='beta' if value_range[1] <= 1.1 else 'm_value',
            value_range=value_range,
            missing_rate=missing_rate,
            is_valid=validation_result['is_valid'],
            validation_messages=validation_result['messages'],
            metadata={
                'file_type': file_type,
                'original_orientation': self.original_orientation,
                'clock_coverage': clock_coverage
            }
        )
        
        return self.loaded_data
    
    def _detect_file_type(self, file_input) -> str:
        """Detect file type from input"""
        if isinstance(file_input, str):
            if file_input.endswith('.csv'):
                return 'csv'
            elif file_input.endswith('.tsv') or file_input.endswith('.txt'):
                return 'tsv'
            elif file_input.endswith('.xlsx') or file_input.endswith('.xls'):
                return 'excel'
            elif file_input.endswith('.parquet'):
                return 'parquet'
        
        if hasattr(file_input, 'name'):
            name = file_input.name.lower()
            if name.endswith('.csv'):
                return 'csv'
            elif name.endswith('.tsv') or name.endswith('.txt'):
                return 'tsv'
            elif name.endswith('.xlsx') or name.endswith('.xls'):
                return 'excel'
            elif name.endswith('.parquet'):
                return 'parquet'
        
        return 'csv'
    
    def _load_csv(self, file_input, delimiter: str = ',') -> pd.DataFrame:
        """Load CSV/TSV file"""
        try:
            if isinstance(file_input, str):
                df = pd.read_csv(file_input, delimiter=delimiter, index_col=0)
            elif hasattr(file_input, 'read'):
                content = file_input.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
                file_input.seek(0)
                df = pd.read_csv(StringIO(content), delimiter=delimiter, index_col=0)
            else:
                df = pd.read_csv(file_input, delimiter=delimiter, index_col=0)
            
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
    
    def _load_excel(self, file_input) -> pd.DataFrame:
        """Load Excel file"""
        try:
            if isinstance(file_input, str):
                df = pd.read_excel(file_input, index_col=0, engine='openpyxl')
            elif hasattr(file_input, 'read'):
                content = file_input.read()
                file_input.seek(0)
                df = pd.read_excel(BytesIO(content), index_col=0, engine='openpyxl')
            else:
                df = pd.read_excel(file_input, index_col=0, engine='openpyxl')
            
            return df
        except Exception as e:
            raise ValueError(f"Error loading Excel file: {str(e)}")
    
    def _load_parquet(self, file_input) -> pd.DataFrame:
        """Load Parquet file"""
        try:
            if isinstance(file_input, str):
                df = pd.read_parquet(file_input)
            elif hasattr(file_input, 'read'):
                content = file_input.read()
                file_input.seek(0)
                df = pd.read_parquet(BytesIO(content))
            else:
                df = pd.read_parquet(file_input)
            
            if df.columns[0] not in ['cg', 'sample', 'id']:
                first_col = df.columns[0]
                if df[first_col].dtype == 'object':
                    df = df.set_index(first_col)
            
            return df
        except Exception as e:
            raise ValueError(f"Error loading Parquet file: {str(e)}")
    
    def _extract_sample_ids(self, df: pd.DataFrame,
                            sample_column: Optional[str]) -> Tuple[pd.DataFrame, Optional[List[str]]]:
        """Extract sample IDs from data"""
        if sample_column and sample_column in df.columns:
            sample_ids = df[sample_column].tolist()
            df = df.drop(columns=[sample_column])
            df.index = sample_ids
            return df, sample_ids
        
        return df, None
    
    def _detect_orientation(self, df: pd.DataFrame) -> bool:
        """
        Detect if data needs transposition
        
        Returns True if CpGs are in rows (needs transpose to samples x CpGs)
        """
        col_cpg_count = sum(1 for col in df.columns if self.CG_PATTERN.match(str(col)))
        row_cpg_count = sum(1 for idx in df.index if self.CG_PATTERN.match(str(idx)))
        
        col_ratio = col_cpg_count / len(df.columns) if len(df.columns) > 0 else 0
        row_ratio = row_cpg_count / len(df.index) if len(df.index) > 0 else 0
        
        if col_ratio > 0.5:
            return False
        elif row_ratio > 0.5:
            return True
        
        if len(df.columns) > len(df.index) * 10:
            return False
        elif len(df.index) > len(df.columns) * 10:
            return True
        
        return False
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate data values"""
        numeric_cols = []
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().any():
                    numeric_cols.append(col)
            except:
                pass
        
        df = df[numeric_cols]
        
        cpg_cols = [col for col in df.columns if self.CG_PATTERN.match(str(col)) or self.CH_PATTERN.match(str(col))]
        
        if len(cpg_cols) > 0:
            df = df[cpg_cols]
        
        return df
    
    def _validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate methylation data"""
        messages = []
        is_valid = True
        
        if df.shape[0] < 1:
            messages.append("ERROR: No samples found in data")
            is_valid = False
        
        if df.shape[1] < 10:
            messages.append("ERROR: Too few CpG sites found (<10)")
            is_valid = False
        
        cpg_count = sum(1 for col in df.columns if self.CG_PATTERN.match(str(col)))
        if cpg_count < df.shape[1] * 0.5:
            messages.append(f"WARNING: Only {cpg_count}/{df.shape[1]} columns match CpG naming pattern")
        
        value_range = (df.values.min(), df.values.max())
        if value_range[0] < -20 or value_range[1] > 20:
            messages.append("WARNING: Values outside expected M-value range (-20 to 20)")
        
        if value_range[1] <= 1.1 and value_range[0] >= -0.1:
            messages.append("INFO: Data appears to be beta values (0-1)")
        else:
            messages.append("INFO: Data appears to be M-values")
        
        missing_rate = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        if missing_rate > 0.1:
            messages.append(f"WARNING: High missing rate ({missing_rate:.1%})")
        
        if is_valid:
            messages.append(f"SUCCESS: Loaded {df.shape[0]} samples x {df.shape[1]} CpG sites")
        
        return {
            'is_valid': is_valid,
            'messages': messages
        }
    
    def _check_clock_coverage(self, cpg_ids: List[str]) -> Dict[str, float]:
        """Check coverage of required CpG sites for each clock"""
        cpg_set = set(c.lower() for c in cpg_ids)
        
        coverage = {}
        for clock_name, required_cpgs in self.REQUIRED_OPEN_SOURCE_CPGS.items():
            matched = sum(1 for cpg in required_cpgs if cpg.lower() in cpg_set)
            coverage[clock_name] = matched / len(required_cpgs) if required_cpgs else 0
        
        return coverage
    
    def get_methylation_matrix(self) -> pd.DataFrame:
        """Get the loaded methylation matrix"""
        if self.loaded_data is None:
            raise ValueError("No data loaded. Call load_file() first.")
        return self.loaded_data.data
    
    def get_sample_ids(self) -> List[str]:
        """Get sample IDs"""
        if self.loaded_data is None:
            raise ValueError("No data loaded. Call load_file() first.")
        return self.loaded_data.sample_ids
    
    def get_cpg_ids(self) -> List[str]:
        """Get CpG site IDs"""
        if self.loaded_data is None:
            raise ValueError("No data loaded. Call load_file() first.")
        return self.loaded_data.cpg_ids


class GEODataLoader(RealDataLoader):
    """
    Specialized loader for GEO (Gene Expression Omnibus) datasets
    
    Handles:
    - GSE matrix files
    - Soft format files
    - Series matrix format
    """
    
    def load_geo_matrix(self, file_input, 
                        skip_metadata: bool = True) -> LoadedMethylationData:
        """
        Load GEO series matrix file
        
        Args:
            file_input: Path or file object for GEO matrix file
            skip_metadata: Whether to skip GEO metadata rows
        
        Returns:
            LoadedMethylationData with methylation matrix
        """
        if isinstance(file_input, str):
            with open(file_input, 'r') as f:
                lines = f.readlines()
        else:
            content = file_input.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            file_input.seek(0)
            lines = content.split('\n')
        
        data_start = 0
        if skip_metadata:
            for i, line in enumerate(lines):
                if line.startswith('!series_matrix_table_begin'):
                    data_start = i + 1
                    break
                if line.startswith('"ID_REF"') or line.startswith('ID_REF'):
                    data_start = i
                    break
        
        data_lines = []
        for line in lines[data_start:]:
            if line.startswith('!series_matrix_table_end'):
                break
            if line.strip():
                data_lines.append(line)
        
        df = pd.read_csv(StringIO('\n'.join(data_lines)), sep='\t', index_col=0)
        
        df = self._clean_data(df.T)
        
        validation_result = self._validate_data(df)
        
        cpg_ids = list(df.columns)
        sample_ids = list(df.index)
        
        value_range = (df.values.min(), df.values.max())
        missing_rate = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        
        clock_coverage = self._check_clock_coverage(cpg_ids)
        
        self.loaded_data = LoadedMethylationData(
            data=df,
            n_samples=df.shape[0],
            n_cpgs=df.shape[1],
            sample_ids=sample_ids,
            cpg_ids=cpg_ids,
            data_type='beta' if value_range[1] <= 1.1 else 'm_value',
            value_range=value_range,
            missing_rate=missing_rate,
            is_valid=validation_result['is_valid'],
            validation_messages=validation_result['messages'],
            metadata={
                'file_type': 'geo_matrix',
                'original_orientation': 'cpgs_as_rows',
                'clock_coverage': clock_coverage
            }
        )
        
        return self.loaded_data


def test_real_data_loader():
    """Test the RealDataLoader"""
    print("Testing RealDataLoader")
    print("=" * 60)
    
    n_samples = 20
    n_cpgs = 100
    
    cpg_names = [f"cg{i:08d}" for i in range(n_cpgs)]
    sample_names = [f"Sample_{i}" for i in range(n_samples)]
    
    np.random.seed(42)
    beta_values = np.random.beta(2.5, 4, (n_samples, n_cpgs))
    
    df = pd.DataFrame(beta_values, index=sample_names, columns=cpg_names)
    
    csv_path = "/tmp/test_methylation.csv"
    df.to_csv(csv_path)
    
    print("\n1. Testing CSV loading...")
    loader = RealDataLoader()
    result = loader.load_file(csv_path)
    
    print(f"   Samples: {result.n_samples}")
    print(f"   CpG sites: {result.n_cpgs}")
    print(f"   Data type: {result.data_type}")
    print(f"   Value range: {result.value_range}")
    print(f"   Valid: {result.is_valid}")
    print(f"   Messages: {result.validation_messages}")
    
    print("\n2. Testing transposed data...")
    df_transposed = df.T
    csv_path_t = "/tmp/test_methylation_transposed.csv"
    df_transposed.to_csv(csv_path_t)
    
    result_t = loader.load_file(csv_path_t)
    print(f"   Original orientation: {result_t.metadata['original_orientation']}")
    print(f"   After auto-transpose: {result_t.n_samples} samples x {result_t.n_cpgs} CpGs")
    
    print("\n3. Testing clock coverage...")
    print(f"   Hannum coverage: {result.metadata['clock_coverage'].get('hannum', 0):.1%}")
    print(f"   DunedinPACE coverage: {result.metadata['clock_coverage'].get('dunedinpace', 0):.1%}")
    
    print("\n" + "=" * 60)
    print("RealDataLoader tested successfully!")
    
    return result


if __name__ == "__main__":
    test_real_data_loader()
