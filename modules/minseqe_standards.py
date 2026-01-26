"""
MINSEQE (Minimum Information about a high-throughput SEQuencing Experiment)
EpiClock v4.0 - Publication Ready

Implements:
- MINSEQE checklist for sequencing experiments
- SRA/ENA submission preparation
- Sequencing metadata standards
- WGBS/RRBS methylation sequencing support
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MINSEQEChecklist:
    """MINSEQE Compliance Checklist"""
    
    REQUIREMENTS = {
        'general_information': [
            ('G1', 'Submitter information', True),
            ('G2', 'Experiment title and abstract', True),
            ('G3', 'Experiment type (WGBS, RRBS, etc.)', True),
            ('G4', 'Associated publications', False),
            ('G5', 'Release date', True)
        ],
        'raw_data': [
            ('R1', 'Raw sequence data files (FASTQ/BAM)', True),
            ('R2', 'File checksums (MD5)', True),
            ('R3', 'File format specification', True),
            ('R4', 'Quality scores encoding', True)
        ],
        'sample_information': [
            ('S1', 'Sample name and description', True),
            ('S2', 'Organism and strain', True),
            ('S3', 'Sample source (tissue, cell type)', True),
            ('S4', 'Sample treatment/condition', True),
            ('S5', 'Biological replicate information', True),
            ('S6', 'Technical replicate information', True)
        ],
        'library_information': [
            ('L1', 'Library construction protocol', True),
            ('L2', 'Library type (single/paired-end)', True),
            ('L3', 'Library selection method', True),
            ('L4', 'Library source (genomic DNA)', True),
            ('L5', 'Library layout', True),
            ('L6', 'Insert size (for paired-end)', True),
            ('L7', 'Strand-specific information', True)
        ],
        'sequencing_information': [
            ('Q1', 'Sequencing platform and model', True),
            ('Q2', 'Sequencing chemistry version', False),
            ('Q3', 'Read length', True),
            ('Q4', 'Sequencing depth/coverage', True),
            ('Q5', 'Flow cell ID', False),
            ('Q6', 'Lane number', False)
        ],
        'methylation_specific': [
            ('M1', 'Bisulfite conversion protocol', True),
            ('M2', 'Bisulfite conversion efficiency', True),
            ('M3', 'Lambda/pUC19 spike-in controls', True),
            ('M4', 'Reference genome and version', True),
            ('M5', 'Alignment algorithm and version', True),
            ('M6', 'Methylation calling method', True),
            ('M7', 'Coverage thresholds', True)
        ],
        'processed_data': [
            ('P1', 'Processed data files', False),
            ('P2', 'Processing pipeline description', True),
            ('P3', 'Genome coordinates (bed/bedGraph)', False),
            ('P4', 'Methylation level format (beta/M-value)', True)
        ]
    }
    
    def __init__(self):
        self.completed = {}
        self.values = {}
        for category in self.REQUIREMENTS:
            for item_id, _, _ in self.REQUIREMENTS[category]:
                self.completed[item_id] = False
                self.values[item_id] = None
    
    def set_item(self, item_id: str, value: Any):
        """Set checklist item"""
        if item_id in self.completed:
            self.completed[item_id] = True
            self.values[item_id] = value
    
    def get_compliance_status(self) -> Dict:
        """Get compliance status"""
        required = []
        for category, items in self.REQUIREMENTS.items():
            for item_id, _, is_required in items:
                if is_required:
                    required.append(item_id)
        
        completed_required = sum(1 for i in required if self.completed.get(i, False))
        
        return {
            'required_completed': completed_required,
            'required_total': len(required),
            'compliance_percentage': completed_required / len(required) * 100 if required else 0,
            'is_compliant': completed_required == len(required),
            'missing_required': [i for i in required if not self.completed.get(i, False)]
        }
    
    def generate_report(self) -> str:
        """Generate MINSEQE compliance report"""
        status = self.get_compliance_status()
        
        report = []
        report.append("=" * 60)
        report.append("MINSEQE COMPLIANCE REPORT")
        report.append("Minimum Information about a SEQuencing Experiment")
        report.append("=" * 60)
        
        compliance = "COMPLIANT" if status['is_compliant'] else "NOT COMPLIANT"
        report.append(f"\nStatus: {compliance}")
        report.append(f"Required Items: {status['required_completed']}/{status['required_total']}")
        report.append(f"Compliance: {status['compliance_percentage']:.1f}%")
        
        for category, items in self.REQUIREMENTS.items():
            report.append(f"\n{category.upper().replace('_', ' ')}")
            report.append("-" * 40)
            for item_id, description, is_required in items:
                check = "[X]" if self.completed.get(item_id, False) else "[ ]"
                req = "*" if is_required else " "
                report.append(f"  {check}{req} {item_id}: {description}")
        
        report.append("\n* = Required item")
        return "\n".join(report)


@dataclass
class SRASubmissionGenerator:
    """Generate SRA (Sequence Read Archive) submission files"""
    
    def __init__(self, bioproject_title: str):
        self.bioproject_title = bioproject_title
        self.biosamples = []
        self.experiments = []
        self.runs = []
    
    def add_biosample(self,
                      sample_name: str,
                      organism: str = 'Homo sapiens',
                      tissue: str = 'blood',
                      attributes: Dict = None) -> str:
        """Add BioSample"""
        biosample = {
            'sample_name': sample_name,
            'organism': organism,
            'tissue': tissue,
            'attributes': attributes or {},
            'biosample_id': f'SAMN{len(self.biosamples) + 1:08d}'  # Placeholder
        }
        self.biosamples.append(biosample)
        return biosample['biosample_id']
    
    def add_experiment(self,
                       biosample_name: str,
                       library_name: str,
                       library_strategy: str = 'Bisulfite-Seq',
                       library_source: str = 'GENOMIC',
                       library_selection: str = 'RANDOM',
                       library_layout: str = 'PAIRED',
                       platform: str = 'ILLUMINA',
                       instrument_model: str = 'Illumina NovaSeq 6000') -> str:
        """Add experiment"""
        experiment = {
            'biosample_name': biosample_name,
            'library_name': library_name,
            'library_strategy': library_strategy,
            'library_source': library_source,
            'library_selection': library_selection,
            'library_layout': library_layout,
            'platform': platform,
            'instrument_model': instrument_model,
            'experiment_id': f'SRX{len(self.experiments) + 1:08d}'  # Placeholder
        }
        self.experiments.append(experiment)
        return experiment['experiment_id']
    
    def add_run(self,
                experiment_id: str,
                file_name: str,
                file_type: str = 'fastq',
                md5: str = None) -> str:
        """Add run (raw data file)"""
        run = {
            'experiment_id': experiment_id,
            'file_name': file_name,
            'file_type': file_type,
            'md5': md5 or 'pending',
            'run_id': f'SRR{len(self.runs) + 1:08d}'  # Placeholder
        }
        self.runs.append(run)
        return run['run_id']
    
    def generate_biosample_tsv(self) -> str:
        """Generate BioSample submission TSV"""
        headers = ['sample_name', 'organism', 'tissue']
        
        # Get all unique attribute keys
        attr_keys = set()
        for bs in self.biosamples:
            attr_keys.update(bs['attributes'].keys())
        attr_keys = sorted(attr_keys)
        headers.extend(attr_keys)
        
        lines = ["\t".join(headers)]
        
        for bs in self.biosamples:
            row = [bs['sample_name'], bs['organism'], bs['tissue']]
            for key in attr_keys:
                row.append(bs['attributes'].get(key, ''))
            lines.append("\t".join(row))
        
        return "\n".join(lines)
    
    def generate_sra_metadata_tsv(self) -> str:
        """Generate SRA metadata submission TSV"""
        headers = [
            'biosample_accession', 'library_ID', 'title', 'library_strategy',
            'library_source', 'library_selection', 'library_layout',
            'platform', 'instrument_model', 'design_description', 'filetype', 'filename', 'filename2'
        ]
        
        lines = ["\t".join(headers)]
        
        for exp in self.experiments:
            # Find associated biosample
            biosample = next((bs for bs in self.biosamples if bs['sample_name'] == exp['biosample_name']), None)
            biosample_id = biosample['biosample_id'] if biosample else 'pending'
            
            # Find associated runs
            exp_runs = [r for r in self.runs if r['experiment_id'] == exp['experiment_id']]
            
            if exp['library_layout'] == 'PAIRED':
                files = [r['file_name'] for r in exp_runs]
                file1 = files[0] if len(files) > 0 else ''
                file2 = files[1] if len(files) > 1 else ''
                filetype = 'fastq'
            else:
                file1 = exp_runs[0]['file_name'] if exp_runs else ''
                file2 = ''
                filetype = exp_runs[0]['file_type'] if exp_runs else 'fastq'
            
            row = [
                biosample_id,
                exp['library_name'],
                f"{exp['library_strategy']} of {exp['biosample_name']}",
                exp['library_strategy'],
                exp['library_source'],
                exp['library_selection'],
                exp['library_layout'],
                exp['platform'],
                exp['instrument_model'],
                'Bisulfite converted genomic DNA library',
                filetype,
                file1,
                file2
            ]
            lines.append("\t".join(row))
        
        return "\n".join(lines)


@dataclass
class ENASubmissionGenerator:
    """Generate ENA (European Nucleotide Archive) submission files"""
    
    def __init__(self, study_title: str, study_abstract: str):
        self.study_title = study_title
        self.study_abstract = study_abstract
        self.samples = []
        self.experiments = []
        self.runs = []
    
    def add_sample(self,
                   sample_alias: str,
                   taxon_id: int = 9606,
                   scientific_name: str = 'Homo sapiens',
                   attributes: Dict = None) -> Dict:
        """Add sample"""
        sample = {
            'alias': sample_alias,
            'taxon_id': taxon_id,
            'scientific_name': scientific_name,
            'attributes': attributes or {}
        }
        self.samples.append(sample)
        return sample
    
    def generate_study_xml(self) -> str:
        """Generate study XML"""
        xml = []
        xml.append('<?xml version="1.0" encoding="UTF-8"?>')
        xml.append('<STUDY_SET>')
        xml.append('  <STUDY alias="epiclock_study">')
        xml.append('    <DESCRIPTOR>')
        xml.append(f'      <STUDY_TITLE>{self.study_title}</STUDY_TITLE>')
        xml.append('      <STUDY_TYPE existing_study_type="Other"/>')
        xml.append(f'      <STUDY_ABSTRACT>{self.study_abstract}</STUDY_ABSTRACT>')
        xml.append('    </DESCRIPTOR>')
        xml.append('  </STUDY>')
        xml.append('</STUDY_SET>')
        return "\n".join(xml)
    
    def generate_sample_xml(self) -> str:
        """Generate sample XML"""
        xml = []
        xml.append('<?xml version="1.0" encoding="UTF-8"?>')
        xml.append('<SAMPLE_SET>')
        
        for sample in self.samples:
            xml.append(f'  <SAMPLE alias="{sample["alias"]}">')
            xml.append(f'    <TITLE>{sample["alias"]}</TITLE>')
            xml.append('    <SAMPLE_NAME>')
            xml.append(f'      <TAXON_ID>{sample["taxon_id"]}</TAXON_ID>')
            xml.append(f'      <SCIENTIFIC_NAME>{sample["scientific_name"]}</SCIENTIFIC_NAME>')
            xml.append('    </SAMPLE_NAME>')
            if sample['attributes']:
                xml.append('    <SAMPLE_ATTRIBUTES>')
                for key, value in sample['attributes'].items():
                    xml.append('      <SAMPLE_ATTRIBUTE>')
                    xml.append(f'        <TAG>{key}</TAG>')
                    xml.append(f'        <VALUE>{value}</VALUE>')
                    xml.append('      </SAMPLE_ATTRIBUTE>')
                xml.append('    </SAMPLE_ATTRIBUTES>')
            xml.append('  </SAMPLE>')
        
        xml.append('</SAMPLE_SET>')
        return "\n".join(xml)


def test_minseqe_standards():
    """Test MINSEQE module"""
    print("=" * 60)
    print("MINSEQE STANDARDS MODULE - TEST")
    print("=" * 60)
    
    # Test MINSEQE Checklist
    print("\n[1] MINSEQE Checklist:")
    checklist = MINSEQEChecklist()
    checklist.set_item('G1', 'EpiClock Research Team')
    checklist.set_item('G2', 'Methylation sequencing of addiction')
    checklist.set_item('G3', 'WGBS')
    checklist.set_item('R1', 'FASTQ files submitted')
    checklist.set_item('S1', 'Case and control samples')
    status = checklist.get_compliance_status()
    print(f"  Compliance: {status['compliance_percentage']:.1f}%")
    print(f"  Missing required: {len(status['missing_required'])}")
    
    # Test SRA Submission
    print("\n[2] SRA Submission Generator:")
    sra = SRASubmissionGenerator('Epigenetic markers of addiction')
    biosample_id = sra.add_biosample(
        'Sample_001',
        tissue='whole blood',
        attributes={'age': '35', 'sex': 'male', 'disease': 'SUD'}
    )
    exp_id = sra.add_experiment(
        'Sample_001',
        'Library_001',
        library_strategy='Bisulfite-Seq'
    )
    sra.add_run(exp_id, 'Sample_001_R1.fastq.gz')
    sra.add_run(exp_id, 'Sample_001_R2.fastq.gz')
    
    biosample_tsv = sra.generate_biosample_tsv()
    sra_tsv = sra.generate_sra_metadata_tsv()
    print(f"  BioSample TSV lines: {len(biosample_tsv.split(chr(10)))}")
    print(f"  SRA metadata TSV lines: {len(sra_tsv.split(chr(10)))}")
    
    # Test ENA Submission
    print("\n[3] ENA Submission Generator:")
    ena = ENASubmissionGenerator(
        'Addiction Methylome Study',
        'WGBS analysis of substance use disorder'
    )
    ena.add_sample('ENA_Sample_001', attributes={'tissue': 'blood'})
    study_xml = ena.generate_study_xml()
    sample_xml = ena.generate_sample_xml()
    print(f"  Study XML lines: {len(study_xml.split(chr(10)))}")
    print(f"  Sample XML lines: {len(sample_xml.split(chr(10)))}")
    
    print("\n" + "=" * 60)
    print("MINSEQE Standards Test Complete")


if __name__ == "__main__":
    test_minseqe_standards()
