"""
MIQE (Minimum Information for Publication of Quantitative Real-Time PCR Experiments)
EpiClock v4.0 - Publication Ready

Implements:
- MIQE checklist (Bustin et al., Clinical Chemistry 2009)
- PCR validation documentation
- Primer design standards
- Amplification efficiency tracking
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import hashlib


@dataclass
class MIQEChecklist:
    """MIQE Checklist Implementation"""
    
    ESSENTIAL_ITEMS = {
        'experimental_design': [
            ('E1', 'Definition of experimental and control groups', True),
            ('E2', 'Number within each group', True),
            ('E3', 'Assay carried out by core lab or investigator', False),
            ('E4', 'Acknowledgement of authors contributions', False)
        ],
        'sample': [
            ('S1', 'Description', True),
            ('S2', 'Volume/mass of sample processed', False),
            ('S3', 'Microdissection or macrodissection', True),
            ('S4', 'Processing procedure', True),
            ('S5', 'If frozen - how and how quickly?', True),
            ('S6', 'If fixed - with what, how quickly?', True),
            ('S7', 'Sample storage conditions and duration', True)
        ],
        'nucleic_acid_extraction': [
            ('N1', 'Procedure and/or instrumentation', True),
            ('N2', 'Name of kit and details of modifications', True),
            ('N3', 'Source of additional reagents used', False),
            ('N4', 'Details of DNase or RNase treatment', True),
            ('N5', 'Contamination assessment (DNA or RNA)', True),
            ('N6', 'Nucleic acid quantification', True),
            ('N7', 'Instrument and method', True),
            ('N8', 'Purity (A260/A280)', True),
            ('N9', 'Yield', False)
        ],
        'reverse_transcription': [
            ('R1', 'Complete reaction conditions', True),
            ('R2', 'Amount of RNA and target', True),
            ('R3', 'Priming oligonucleotide and concentration', True),
            ('R4', 'Reverse transcriptase and concentration', True),
            ('R5', 'Temperature and time', True),
            ('R6', 'Manufacturer of reagents and catalogue numbers', False),
            ('R7', 'cDNA storage conditions', False)
        ],
        'qpcr_target': [
            ('T1', 'Gene symbol', True),
            ('T2', 'Sequence accession number', True),
            ('T3', 'Amplicon location', False),
            ('T4', 'Amplicon length', True),
            ('T5', 'In silico specificity screen', True),
            ('T6', 'Pseudogenes, retropseudogenes, splice variants', False),
            ('T7', 'Location of primers, exon-exon junction', False),
            ('T8', 'What splice variants are targeted?', False)
        ],
        'qpcr_oligonucleotides': [
            ('O1', 'Primer sequences', True),
            ('O2', 'RTPrimerDB Identification Number', False),
            ('O3', 'Probe sequences', False),
            ('O4', 'Location and identity of modifications', False),
            ('O5', 'Manufacturer of oligonucleotides', False)
        ],
        'qpcr_protocol': [
            ('P1', 'Complete reaction conditions', True),
            ('P2', 'Reaction volume and amount of cDNA/DNA', True),
            ('P3', 'Primer, (probe), Mg++ and dNTP concentrations', True),
            ('P4', 'Polymerase identity and concentration', True),
            ('P5', 'Buffer/kit identity and manufacturer', True),
            ('P6', 'Exact chemical composition of buffer', False),
            ('P7', 'Additives (SYBR Green I, DMSO, etc.)', True),
            ('P8', 'Manufacturer of plates/tubes and catalog number', False),
            ('P9', 'Complete thermocycling parameters', True),
            ('P10', 'Reaction setup (manual/robotic)', False),
            ('P11', 'Manufacturer of qPCR instrument', True)
        ],
        'qpcr_validation': [
            ('V1', 'Evidence of optimisation', False),
            ('V2', 'Specificity (gel, sequence, melt, digest)', True),
            ('V3', 'For SYBR Green I, Cq of NTC', True),
            ('V4', 'Standard curves with slope and y-intercept', True),
            ('V5', 'PCR efficiency calculated from slope', True),
            ('V6', 'Confidence interval for PCR efficiency', False),
            ('V7', 'r2 of standard curve', True),
            ('V8', 'Linear dynamic range', True),
            ('V9', 'Cq variation at lower limit', True),
            ('V10', 'Evidence for limit of detection', True),
            ('V11', 'If multiplex, efficiency and LOD of each assay', False)
        ],
        'data_analysis': [
            ('D1', 'qPCR analysis program (source, version)', True),
            ('D2', 'Cq method determination', True),
            ('D3', 'Outlier identification and disposition', True),
            ('D4', 'Results of NTCs', True),
            ('D5', 'Justification of number and choice of reference genes', True),
            ('D6', 'Description of normalisation method', True),
            ('D7', 'Number and concordance of biological replicates', False),
            ('D8', 'Number and stage of technical replicates', True),
            ('D9', 'Repeatability (intra-assay variation)', True),
            ('D10', 'Reproducibility (inter-assay variation)', False),
            ('D11', 'Power analysis', False),
            ('D12', 'Statistical methods for result significance', True),
            ('D13', 'Software (source, version)', True),
            ('D14', 'Cq or raw data submission to repository', False)
        ]
    }
    
    def __init__(self):
        self.completed = {}
        self.notes = {}
        for category in self.ESSENTIAL_ITEMS:
            for item_id, _, _ in self.ESSENTIAL_ITEMS[category]:
                self.completed[item_id] = False
                self.notes[item_id] = ""
    
    def mark_complete(self, item_id: str, notes: str = ""):
        """Mark checklist item as complete"""
        if item_id in self.completed:
            self.completed[item_id] = True
            self.notes[item_id] = notes
    
    def get_completion_status(self) -> Dict:
        """Get completion status"""
        total_essential = 0
        completed_essential = 0
        
        for category, items in self.ESSENTIAL_ITEMS.items():
            for item_id, _, is_essential in items:
                if is_essential:
                    total_essential += 1
                    if self.completed.get(item_id, False):
                        completed_essential += 1
        
        return {
            'essential_completed': completed_essential,
            'essential_total': total_essential,
            'essential_percentage': completed_essential / total_essential * 100 if total_essential > 0 else 0,
            'all_completed': sum(1 for v in self.completed.values() if v),
            'all_total': len(self.completed)
        }
    
    def generate_report(self) -> str:
        """Generate MIQE compliance report"""
        status = self.get_completion_status()
        
        report = []
        report.append("=" * 60)
        report.append("MIQE CHECKLIST COMPLIANCE REPORT")
        report.append("Reference: Bustin et al., Clinical Chemistry 2009")
        report.append("=" * 60)
        report.append(f"\nEssential Items: {status['essential_completed']}/{status['essential_total']} ({status['essential_percentage']:.1f}%)")
        report.append(f"All Items: {status['all_completed']}/{status['all_total']}")
        
        for category, items in self.ESSENTIAL_ITEMS.items():
            report.append(f"\n{category.upper().replace('_', ' ')}")
            report.append("-" * 40)
            for item_id, description, is_essential in items:
                check = "[X]" if self.completed.get(item_id, False) else "[ ]"
                essential_mark = "*" if is_essential else " "
                report.append(f"  {check}{essential_mark} {item_id}: {description[:50]}")
        
        report.append("\n* = Essential item")
        return "\n".join(report)


@dataclass
class PrimerDesignStandards:
    """Primer design documentation standards"""
    
    def __init__(self):
        self.primers = []
    
    def add_primer_pair(self, 
                        target_gene: str,
                        forward_seq: str,
                        reverse_seq: str,
                        amplicon_length: int,
                        tm_forward: float,
                        tm_reverse: float,
                        gc_forward: float,
                        gc_reverse: float,
                        accession: str = None,
                        exon_junction: bool = False) -> Dict:
        """Add primer pair with validation"""
        
        # Validate sequences
        valid_bases = set('ATCG')
        if not set(forward_seq.upper()).issubset(valid_bases):
            raise ValueError("Forward primer contains invalid bases")
        if not set(reverse_seq.upper()).issubset(valid_bases):
            raise ValueError("Reverse primer contains invalid bases")
        
        primer_record = {
            'target_gene': target_gene,
            'accession': accession,
            'forward_sequence': forward_seq.upper(),
            'reverse_sequence': reverse_seq.upper(),
            'forward_length': len(forward_seq),
            'reverse_length': len(reverse_seq),
            'amplicon_length': amplicon_length,
            'tm_forward': tm_forward,
            'tm_reverse': tm_reverse,
            'tm_difference': abs(tm_forward - tm_reverse),
            'gc_forward': gc_forward,
            'gc_reverse': gc_reverse,
            'spans_exon_junction': exon_junction,
            'validation_status': 'pending'
        }
        
        # Quality checks
        warnings = []
        if primer_record['tm_difference'] > 2:
            warnings.append("Tm difference > 2C")
        if len(forward_seq) < 18 or len(forward_seq) > 25:
            warnings.append("Forward primer length outside optimal range (18-25)")
        if len(reverse_seq) < 18 or len(reverse_seq) > 25:
            warnings.append("Reverse primer length outside optimal range (18-25)")
        if gc_forward < 40 or gc_forward > 60:
            warnings.append("Forward GC% outside optimal range (40-60%)")
        if gc_reverse < 40 or gc_reverse > 60:
            warnings.append("Reverse GC% outside optimal range (40-60%)")
        
        primer_record['warnings'] = warnings
        primer_record['quality_score'] = max(0, 100 - len(warnings) * 20)
        
        self.primers.append(primer_record)
        return primer_record
    
    def generate_primer_table(self) -> pd.DataFrame:
        """Generate primer table for publication"""
        if not self.primers:
            return pd.DataFrame()
        
        return pd.DataFrame([{
            'Target Gene': p['target_gene'],
            'Accession': p['accession'] or 'N/A',
            'Forward (5\'-3\')': p['forward_sequence'],
            'Reverse (5\'-3\')': p['reverse_sequence'],
            'Amplicon (bp)': p['amplicon_length'],
            'Tm F/R (C)': f"{p['tm_forward']:.1f}/{p['tm_reverse']:.1f}"
        } for p in self.primers])


@dataclass
class AmplificationEfficiency:
    """Track and validate PCR amplification efficiency"""
    
    def __init__(self):
        self.assays = {}
    
    def add_standard_curve(self,
                           assay_name: str,
                           concentrations: List[float],
                           cq_values: List[float],
                           replicates: int = 3) -> Dict:
        """Add standard curve data and calculate efficiency"""
        
        conc = np.array(concentrations)
        cq = np.array(cq_values)
        
        # Log transform concentrations
        log_conc = np.log10(conc)
        
        # Linear regression
        slope, intercept = np.polyfit(log_conc, cq, 1)
        
        # Calculate efficiency: E = 10^(-1/slope) - 1
        efficiency = (10 ** (-1/slope) - 1) * 100
        
        # Calculate R-squared
        predicted = slope * log_conc + intercept
        ss_res = np.sum((cq - predicted) ** 2)
        ss_tot = np.sum((cq - np.mean(cq)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Calculate dynamic range
        dynamic_range = np.log10(max(conc) / min(conc))
        
        result = {
            'assay_name': assay_name,
            'slope': slope,
            'intercept': intercept,
            'efficiency_percent': efficiency,
            'r_squared': r_squared,
            'dynamic_range_logs': dynamic_range,
            'n_points': len(concentrations),
            'replicates': replicates,
            'valid': 90 <= efficiency <= 110 and r_squared >= 0.98
        }
        
        self.assays[assay_name] = result
        return result
    
    def generate_validation_report(self) -> str:
        """Generate efficiency validation report"""
        report = []
        report.append("=" * 60)
        report.append("PCR AMPLIFICATION EFFICIENCY REPORT")
        report.append("=" * 60)
        
        for name, data in self.assays.items():
            report.append(f"\nAssay: {name}")
            report.append("-" * 40)
            report.append(f"  Slope: {data['slope']:.3f}")
            report.append(f"  Y-intercept: {data['intercept']:.3f}")
            report.append(f"  Efficiency: {data['efficiency_percent']:.1f}%")
            report.append(f"  R-squared: {data['r_squared']:.4f}")
            report.append(f"  Dynamic range: {data['dynamic_range_logs']:.1f} logs")
            status = "VALID" if data['valid'] else "NEEDS OPTIMIZATION"
            report.append(f"  Status: {status}")
        
        return "\n".join(report)


def test_miqe_standards():
    """Test MIQE module"""
    print("=" * 60)
    print("MIQE STANDARDS MODULE - TEST")
    print("=" * 60)
    
    # Test checklist
    print("\n[1] MIQE Checklist:")
    checklist = MIQEChecklist()
    checklist.mark_complete('E1', 'Case-control design')
    checklist.mark_complete('E2', 'n=50 per group')
    checklist.mark_complete('S1', 'Whole blood samples')
    status = checklist.get_completion_status()
    print(f"  Essential items: {status['essential_percentage']:.1f}%")
    
    # Test primer design
    print("\n[2] Primer Design:")
    primers = PrimerDesignStandards()
    primer = primers.add_primer_pair(
        target_gene='GAPDH',
        forward_seq='GTCTCCTCTGACTTCAACAGCG',
        reverse_seq='ACCACCCTGTTGCTGTAGCCAA',
        amplicon_length=131,
        tm_forward=60.5,
        tm_reverse=61.2,
        gc_forward=54.5,
        gc_reverse=50.0,
        accession='NM_002046.7'
    )
    print(f"  Quality score: {primer['quality_score']}")
    
    # Test efficiency
    print("\n[3] Amplification Efficiency:")
    efficiency = AmplificationEfficiency()
    result = efficiency.add_standard_curve(
        'GAPDH',
        [1e6, 1e5, 1e4, 1e3, 1e2],
        [15.2, 18.5, 21.8, 25.1, 28.4]
    )
    print(f"  Efficiency: {result['efficiency_percent']:.1f}%")
    print(f"  R-squared: {result['r_squared']:.4f}")
    print(f"  Valid: {result['valid']}")
    
    print("\n" + "=" * 60)
    print("MIQE Standards Test Complete")


if __name__ == "__main__":
    test_miqe_standards()
