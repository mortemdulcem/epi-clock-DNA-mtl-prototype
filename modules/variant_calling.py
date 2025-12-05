# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
Variant Calling Module
Integrates GATK best practices with EpiClock pipeline

Supports:
- Illumina short reads (FASTQ)
- BAM/CRAM alignment files
- VCF input/output
- Low-pass WGS with imputation

Cost-effective approach for 700K variant analysis
Target: Reduce costs from 1.5M TL to ~75K TL

Author: Dr. Nurcan Denli Bayır
"""

import subprocess
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import io
import gzip


@dataclass
# nrcdnl94
class VariantCallResult:
    # nrcdnl94
    """Results from variant calling pipeline"""
    sample_id: str
    total_variants: int
    snps: int
    indels: int
    filtered_variants: int
    quality_metrics: Dict
    vcf_path: str


@dataclass
# nrcdnl94
class Variant:
    # nrcdnl94
    """Single variant representation"""
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float
    filter_status: str
    info: Dict
    genotype: str
    rsid: Optional[str] = None


class VCFReader:
    # nrcdnl94
    """
    VCF File Reader for variant analysis
    
    Supports:
    - VCF 4.1/4.2/4.3 format
    - Gzipped VCF (.vcf.gz)
    - Multi-sample VCF
    """
    
    def __init__(self):
        self.header = []
        self.samples = []
        self.variants = []
        self.metadata = {}
        
    def read_vcf(self, file_path_or_buffer) -> pd.DataFrame:
        """
        Read VCF file into DataFrame
        
        Args:
            file_path_or_buffer: Path to VCF or file buffer
            
        Returns:
            DataFrame with variant information
        """
        if isinstance(file_path_or_buffer, (str, Path)):
            if str(file_path_or_buffer).endswith('.gz'):
                with gzip.open(file_path_or_buffer, 'rt') as f:
                    return self._parse_vcf(f)
            else:
                with open(file_path_or_buffer, 'r') as f:
                    return self._parse_vcf(f)
        else:
            content = file_path_or_buffer.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return self._parse_vcf(io.StringIO(content))
    
    def _parse_vcf(self, file_handle) -> pd.DataFrame:
        """Parse VCF file content"""
        variants = []
        
        for line in file_handle:
            line = line.strip()
            
            if line.startswith('##'):
                self._parse_metadata(line)
            elif line.startswith('#CHROM'):
                fields = line[1:].split('\t')
                self.header = fields[:9]
                self.samples = fields[9:] if len(fields) > 9 else ['SAMPLE']
            elif line and not line.startswith('#'):
                variant = self._parse_variant_line(line)
                if variant:
                    variants.append(variant)
        
        self.variants = variants
        return self._to_dataframe(variants)
    
    def _parse_metadata(self, line: str):
        """Parse VCF metadata lines"""
        if '=' in line:
            key = line[2:].split('=')[0]
            value = '='.join(line[2:].split('=')[1:])
            self.metadata[key] = value
    
    def _parse_variant_line(self, line: str) -> Optional[Dict]:
        """Parse single variant line"""
        fields = line.split('\t')
        
        if len(fields) < 8:
            return None
        
        chrom = fields[0]
        pos = int(fields[1])
        rsid = fields[2] if fields[2] != '.' else None
        ref = fields[3]
        alt = fields[4]
        qual = float(fields[5]) if fields[5] != '.' else 0.0
        filter_status = fields[6]
        info = self._parse_info(fields[7])
        
        genotypes = {}
        if len(fields) > 9:
            format_fields = fields[8].split(':')
            for i, sample in enumerate(self.samples):
                if i + 9 < len(fields):
                    sample_data = fields[i + 9].split(':')
                    genotypes[sample] = dict(zip(format_fields, sample_data))
        
        return {
            'CHROM': chrom,
            'POS': pos,
            'ID': rsid,
            'REF': ref,
            'ALT': alt,
            'QUAL': qual,
            'FILTER': filter_status,
            'INFO': info,
            'GENOTYPES': genotypes
        }
    
    def _parse_info(self, info_str: str) -> Dict:
        """Parse INFO field"""
        info = {}
        for item in info_str.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                info[key] = value
            else:
                info[item] = True
        return info
    
    def _to_dataframe(self, variants: List[Dict]) -> pd.DataFrame:
        """Convert variants to DataFrame"""
        rows = []
        for v in variants:
            row = {
                'CHROM': v['CHROM'],
                'POS': v['POS'],
                'ID': v['ID'],
                'REF': v['REF'],
                'ALT': v['ALT'],
                'QUAL': v['QUAL'],
                'FILTER': v['FILTER']
            }
            
            for key, value in v['INFO'].items():
                if key in ['AF', 'DP', 'MQ', 'QD', 'FS']:
                    row[key] = value
            
            for sample, gt in v['GENOTYPES'].items():
                row[f'{sample}_GT'] = gt.get('GT', './.')
                row[f'{sample}_DP'] = gt.get('DP', '0')
                row[f'{sample}_GQ'] = gt.get('GQ', '0')
            
            rows.append(row)
        
        return pd.DataFrame(rows)


class VariantCaller:
    # nrcdnl94
    """
    Automated variant calling from sequencing data.
    
    Supports:
    - Illumina short reads (FASTQ)
    - BAM/CRAM alignment files
    - VCF output
    
    Pipeline:
    1. Quality control (FastQC)
    2. Alignment (BWA-MEM)
    3. Variant calling (GATK HaplotypeCaller)
    4. Filtering (GATK VQSR)
    
    Cost-effective options:
    - Low-pass WGS (0.5-1× coverage) + Imputation
    - Targeted sequencing (custom panel)
    - Array genotyping + Imputation
    """
    
    REFERENCE_GENOMES = {
        'hg38': 'GRCh38',
        'hg19': 'GRCh37',
        'GRCh38': 'GRCh38',
        'GRCh37': 'GRCh37'
    }
    
    ADDICTION_GENES = {
        'opioid': ['OPRM1', 'OPRK1', 'OPRD1', 'PDYN', 'PENK'],
        'dopamine': ['DRD1', 'DRD2', 'DRD3', 'DRD4', 'DAT1', 'COMT'],
        'serotonin': ['SLC6A4', 'HTR1A', 'HTR2A', 'TPH2'],
        'gaba': ['GABRA2', 'GABRG1', 'GABRB2'],
        'alcohol': ['ADH1B', 'ADH1C', 'ALDH2', 'ADH4', 'ADH7'],
        'metabolism': ['CYP2D6', 'CYP2C19', 'CYP3A4', 'CYP2B6', 'UGT2B7']
    }
    
    def __init__(self, reference_genome: str = "hg38", threads: int = 8):
        self.reference = self.REFERENCE_GENOMES.get(reference_genome, reference_genome)
        self.threads = threads
        self.gatk_available = self._check_gatk()
        
    def _check_gatk(self) -> bool:
        """Check if GATK is available"""
        try:
            result = subprocess.run(['which', 'gatk'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def call_variants_from_vcf(self, vcf_file) -> Tuple[pd.DataFrame, Dict]:
        """
        Analyze pre-called variants from VCF file
        
        This is the most common use case - analyzing existing VCF data
        from sequencing facilities or public databases.
        
        Args:
            vcf_file: VCF file path or buffer
            
        Returns:
            Tuple of (variants DataFrame, quality metrics)
        """
        reader = VCFReader()
        variants_df = reader.read_vcf(vcf_file)
        
        metrics = self._calculate_vcf_metrics(variants_df, reader.metadata)
        
        return variants_df, metrics
    
    def _calculate_vcf_metrics(self, df: pd.DataFrame, metadata: Dict) -> Dict:
        """Calculate quality metrics from VCF"""
        metrics = {
            'total_variants': len(df),
            'snps': len(df[df['REF'].str.len() == df['ALT'].str.len()]),
            'indels': len(df[df['REF'].str.len() != df['ALT'].str.len()]),
            'pass_variants': len(df[df['FILTER'] == 'PASS']),
            'chromosomes': df['CHROM'].nunique(),
            'mean_quality': df['QUAL'].mean() if 'QUAL' in df.columns else 0,
            'samples': [c.replace('_GT', '') for c in df.columns if c.endswith('_GT')]
        }
        
        if 'AF' in df.columns:
            try:
                af_values = pd.to_numeric(df['AF'], errors='coerce')
                metrics['common_variants'] = len(af_values[af_values >= 0.05])
                metrics['rare_variants'] = len(af_values[af_values < 0.01])
            except:
                pass
        
        return metrics
    
    def filter_addiction_variants(self, variants_df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter variants to addiction-related genes
        
        Args:
            variants_df: DataFrame with variant data
            
        Returns:
            Filtered DataFrame
        """
        all_genes = []
        for category, genes in self.ADDICTION_GENES.items():
            all_genes.extend(genes)
        
        if 'GENE' in variants_df.columns:
            return variants_df[variants_df['GENE'].isin(all_genes)]
        
        return variants_df
    
    def calculate_coverage_stats(self, variants_df: pd.DataFrame) -> Dict:
        """Calculate coverage statistics per chromosome"""
        if 'DP' not in variants_df.columns:
            return {}
        
        dp_values = pd.to_numeric(variants_df['DP'], errors='coerce')
        
        return {
            'mean_depth': dp_values.mean(),
            'median_depth': dp_values.median(),
            'min_depth': dp_values.min(),
            'max_depth': dp_values.max(),
            'coverage_uniformity': 1 - (dp_values.std() / dp_values.mean()) if dp_values.mean() > 0 else 0
        }
    
    def generate_variant_report(self, variants_df: pd.DataFrame, 
                                sample_id: str = "Sample") -> Dict:
        """
        Generate comprehensive variant report
        
        Args:
            variants_df: Variant DataFrame
            sample_id: Sample identifier
            
        Returns:
            Report dictionary
        """
        metrics = self._calculate_vcf_metrics(variants_df, {})
        coverage = self.calculate_coverage_stats(variants_df)
        
        variant_types = {
            'transitions': 0,
            'transversions': 0,
            'insertions': 0,
            'deletions': 0
        }
        
        for _, row in variants_df.iterrows():
            ref, alt = row['REF'], row['ALT']
            if len(ref) == 1 and len(alt) == 1:
                if (ref in 'AG' and alt in 'AG') or (ref in 'CT' and alt in 'CT'):
                    variant_types['transitions'] += 1
                else:
                    variant_types['transversions'] += 1
            elif len(ref) < len(alt):
                variant_types['insertions'] += 1
            else:
                variant_types['deletions'] += 1
        
        ti_tv_ratio = (variant_types['transitions'] / variant_types['transversions'] 
                       if variant_types['transversions'] > 0 else 0)
        
        return {
            'sample_id': sample_id,
            'summary': metrics,
            'coverage': coverage,
            'variant_types': variant_types,
            'ti_tv_ratio': round(ti_tv_ratio, 2),
            'quality_pass': ti_tv_ratio >= 2.0
        }


class LowPassWGSAnalyzer:
    # nrcdnl94
    """
    Low-Pass WGS Analysis with Imputation
    
    Cost-effective approach:
    - 0.5-1× coverage WGS: ~300 TL/sample
    - Imputation with TOPMED/1000G: Free
    - Result: ~10M imputed variants
    
    Total cost: 30,000 TL for 100 samples (vs 800,000 TL for 30× WGS)
    """
    
    REFERENCE_PANELS = {
        'TOPMED': {
            'name': 'Trans-Omics for Precision Medicine',
            'variants': 308_000_000,
            'samples': 97_256,
            'populations': 'Multi-ethnic'
        },
        '1000G': {
            'name': '1000 Genomes Project Phase 3',
            'variants': 88_000_000,
            'samples': 2_504,
            'populations': 'Global'
        },
        'HRC': {
            'name': 'Haplotype Reference Consortium',
            'variants': 40_000_000,
            'samples': 32_470,
            'populations': 'European'
        }
    }
    
    def __init__(self, reference_panel: str = 'TOPMED'):
        self.reference_panel = reference_panel
        
    def estimate_imputation_quality(self, coverage: float, maf: float) -> float:
        """
        Estimate imputation accuracy based on coverage and MAF
        
        Args:
            coverage: Sequencing coverage (0.5-30×)
            maf: Minor allele frequency (0-0.5)
            
        Returns:
            Expected R² (imputation accuracy)
        """
        base_r2 = 0.95
        
        coverage_factor = 1 - np.exp(-coverage / 5)
        
        maf_factor = np.sqrt(maf / 0.5) if maf > 0 else 0
        
        r2 = base_r2 * coverage_factor * maf_factor
        
        return min(0.99, max(0.0, r2))
    
    def calculate_cost_savings(self, n_samples: int, 
                               target_variants: int = 700000) -> Dict:
        """
        Calculate cost savings with low-pass approach
        
        Args:
            n_samples: Number of samples
            target_variants: Target variant count
            
        Returns:
            Cost comparison dictionary
        """
        traditional = {
            'wgs_30x': n_samples * 8000,
            'bioinformatics': 400000,
            'software': 200000,
            'personnel': 100000
        }
        traditional['total'] = sum(traditional.values())
        
        lowpass = {
            'wgs_1x': n_samples * 300,
            'imputation': 0,
            'cloud_compute': 10000,
            'personnel': 15000
        }
        lowpass['total'] = sum(lowpass.values())
        
        savings = traditional['total'] - lowpass['total']
        savings_percent = (savings / traditional['total']) * 100
        
        return {
            'traditional': traditional,
            'low_pass': lowpass,
            'savings': savings,
            'savings_percent': round(savings_percent, 1),
            'imputed_variants': 10_000_000
        }


class TargetedSequencingPanel:
    # nrcdnl94
    """
    Custom Targeted Sequencing Panel Designer
    
    Focus on addiction-related genes for cost-effective analysis.
    
    Cost:
    - Panel design: 20,000 TL (one-time)
    - Sequencing: 500 TL/sample
    - Total for 100 samples: 70,000 TL
    """
    
    ADDICTION_PANEL_GENES = {
        'opioid_system': {
            'OPRM1': {'chr': '6', 'size_kb': 80, 'key_variants': ['rs1799971', 'rs1799972']},
            'OPRK1': {'chr': '8', 'size_kb': 25, 'key_variants': ['rs6473797']},
            'OPRD1': {'chr': '1', 'size_kb': 50, 'key_variants': ['rs2234918']},
        },
        'dopamine_system': {
            'DRD2': {'chr': '11', 'size_kb': 65, 'key_variants': ['rs1800497', 'rs6277']},
            'DRD4': {'chr': '11', 'size_kb': 4, 'key_variants': ['rs1800955']},
            'DAT1': {'chr': '5', 'size_kb': 65, 'key_variants': ['rs27072']},
            'COMT': {'chr': '22', 'size_kb': 28, 'key_variants': ['rs4680', 'rs6269']},
        },
        'serotonin_system': {
            'SLC6A4': {'chr': '17', 'size_kb': 35, 'key_variants': ['5-HTTLPR', 'rs25531']},
            'HTR2A': {'chr': '13', 'size_kb': 65, 'key_variants': ['rs6313', 'rs6311']},
            'TPH2': {'chr': '12', 'size_kb': 95, 'key_variants': ['rs4570625']},
        },
        'alcohol_metabolism': {
            'ADH1B': {'chr': '4', 'size_kb': 16, 'key_variants': ['rs1229984', 'rs2066702']},
            'ADH1C': {'chr': '4', 'size_kb': 16, 'key_variants': ['rs698']},
            'ALDH2': {'chr': '12', 'size_kb': 45, 'key_variants': ['rs671']},
        },
        'pharmacogenomics': {
            'CYP2D6': {'chr': '22', 'size_kb': 5, 'key_variants': ['*1', '*2', '*3', '*4', '*10']},
            'CYP2C19': {'chr': '10', 'size_kb': 90, 'key_variants': ['*2', '*3', '*17']},
            'CYP3A4': {'chr': '7', 'size_kb': 27, 'key_variants': ['*1B', '*22']},
            'CYP2B6': {'chr': '19', 'size_kb': 30, 'key_variants': ['*6', '*18']},
        }
    }
    
    def __init__(self):
        self.panel_size_kb = 0
        self.gene_count = 0
        self.variant_count = 0
        
    def design_panel(self, categories: List[str] = None) -> Dict:
        """
        Design custom sequencing panel
        
        Args:
            categories: Gene categories to include (default: all)
            
        Returns:
            Panel design specification
        """
        if categories is None:
            categories = list(self.ADDICTION_PANEL_GENES.keys())
        
        genes = []
        total_size = 0
        total_variants = 0
        
        for category in categories:
            if category in self.ADDICTION_PANEL_GENES:
                for gene, info in self.ADDICTION_PANEL_GENES[category].items():
                    genes.append({
                        'gene': gene,
                        'category': category,
                        'chromosome': info['chr'],
                        'size_kb': info['size_kb'],
                        'key_variants': info['key_variants']
                    })
                    total_size += info['size_kb']
                    total_variants += len(info['key_variants'])
        
        self.panel_size_kb = total_size
        self.gene_count = len(genes)
        self.variant_count = total_variants
        
        return {
            'genes': genes,
            'total_genes': len(genes),
            'total_size_kb': total_size,
            'total_size_mb': round(total_size / 1000, 2),
            'key_variants': total_variants,
            'estimated_coverage': '100-500×',
            'cost_per_sample': 500,
            'panel_design_cost': 20000
        }
    
    def calculate_panel_cost(self, n_samples: int) -> Dict:
        """Calculate total cost for panel sequencing"""
        design_cost = 20000
        per_sample = 500
        
        return {
            'design_cost': design_cost,
            'sequencing_cost': n_samples * per_sample,
            'total_cost': design_cost + (n_samples * per_sample),
            'cost_per_sample': per_sample + (design_cost / n_samples)
        }


def read_vcf_from_streamlit(uploaded_file) -> Tuple[pd.DataFrame, Dict]:
    """
    Read VCF file from Streamlit uploader
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Tuple of (variants DataFrame, metrics)
    """
    reader = VCFReader()
    
    content = uploaded_file.read()
    if uploaded_file.name.endswith('.gz'):
        content = gzip.decompress(content).decode('utf-8')
    elif isinstance(content, bytes):
        content = content.decode('utf-8')
    
    variants_df = reader._parse_vcf(io.StringIO(content))
    
    caller = VariantCaller()
    metrics = caller._calculate_vcf_metrics(variants_df, reader.metadata)
    
    return variants_df, metrics


def create_demo_vcf_data(n_variants: int = 1000) -> pd.DataFrame:
    """
    Create demonstration VCF data for testing
    
    Args:
        n_variants: Number of variants to generate
        
    Returns:
        DataFrame with simulated variant data
    """
    np.random.seed(42)
    
    chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y']
    bases = ['A', 'C', 'G', 'T']
    
    chrom_probs = [1.0/24]*24
    
    variants = []
    for i in range(n_variants):
        chrom = np.random.choice(chromosomes, p=chrom_probs)
        pos = np.random.randint(1000000, 250000000)
        ref = np.random.choice(bases)
        alt = np.random.choice([b for b in bases if b != ref])
        qual = np.random.uniform(20, 100)
        
        rsid = f"rs{np.random.randint(1000000, 999999999)}" if np.random.random() > 0.3 else None
        
        af = np.random.beta(0.5, 5)
        dp = np.random.randint(10, 100)
        
        gt = np.random.choice(['0/0', '0/1', '1/1'], p=[0.5, 0.4, 0.1])
        
        variants.append({
            'CHROM': chrom,
            'POS': pos,
            'ID': rsid,
            'REF': ref,
            'ALT': alt,
            'QUAL': round(qual, 2),
            'FILTER': 'PASS' if qual > 30 else 'LowQual',
            'AF': round(af, 4),
            'DP': dp,
            'Sample_GT': gt
        })
    
    return pd.DataFrame(variants).sort_values(['CHROM', 'POS'])


# End of module - # nrcdnl94