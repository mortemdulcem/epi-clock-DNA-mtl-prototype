"""
MIAME (Minimum Information About a Microarray Experiment)
EpiClock v4.0 - Publication Ready

Implements:
- MIAME 2.0 checklist (Brazma et al., Nature Genetics 2001)
- GEO/ArrayExpress submission preparation
- Microarray data standards
- Experimental annotation requirements
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MIAMEChecklist:
    """MIAME Compliance Checklist"""
    
    REQUIREMENTS = {
        'experimental_design': [
            ('ED1', 'The set of hybridisation experiments as a whole', True),
            ('ED2', 'Type of experiment (e.g., normal vs. disease)', True),
            ('ED3', 'Experimental factors studied', True),
            ('ED4', 'Number of hybridisations in the experiment', True),
            ('ED5', 'Reference used for hybridisations', True),
            ('ED6', 'Hybridisation design (dye-swap, reference design)', True),
            ('ED7', 'Quality control steps (replicates, spike-ins)', True)
        ],
        'array_design': [
            ('AD1', 'Platform name and accession (GPL)', True),
            ('AD2', 'Provider of arrays (commercial or custom)', True),
            ('AD3', 'Surface type and coating', False),
            ('AD4', 'Probe type (oligo, cDNA, beads)', True),
            ('AD5', 'Annotation reference (build version)', True),
            ('AD6', 'Quality control information', True)
        ],
        'samples': [
            ('SA1', 'Origin of biological sample (species, tissue)', True),
            ('SA2', 'Manipulation of biological samples', True),
            ('SA3', 'External control (spike-in) information', False),
            ('SA4', 'Extract preparation protocol', True),
            ('SA5', 'Labeling protocol', True),
            ('SA6', 'Hybridisation protocol', True),
            ('SA7', 'Scanning hardware and software', True)
        ],
        'measurements': [
            ('ME1', 'Raw data files', True),
            ('ME2', 'Processed data files (normalized)', True),
            ('ME3', 'Image quantification specifications', True),
            ('ME4', 'Data processing specifications', True)
        ],
        'normalization': [
            ('NO1', 'Normalization algorithm name', True),
            ('NO2', 'Parameters and thresholds used', True),
            ('NO3', 'Background correction method', True),
            ('NO4', 'Software and version', True),
            ('NO5', 'Filtering criteria', True)
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
        """Set checklist item value"""
        if item_id in self.completed:
            self.completed[item_id] = True
            self.values[item_id] = value
    
    def get_compliance_status(self) -> Dict:
        """Get MIAME compliance status"""
        required_items = []
        for category, items in self.REQUIREMENTS.items():
            for item_id, _, is_required in items:
                if is_required:
                    required_items.append(item_id)
        
        completed_required = sum(1 for i in required_items if self.completed.get(i, False))
        
        return {
            'required_completed': completed_required,
            'required_total': len(required_items),
            'compliance_percentage': completed_required / len(required_items) * 100 if required_items else 0,
            'is_compliant': completed_required == len(required_items),
            'missing_required': [i for i in required_items if not self.completed.get(i, False)]
        }
    
    def generate_report(self) -> str:
        """Generate MIAME compliance report"""
        status = self.get_compliance_status()
        
        report = []
        report.append("=" * 60)
        report.append("MIAME COMPLIANCE REPORT")
        report.append("Reference: Brazma et al., Nature Genetics 2001")
        report.append("=" * 60)
        
        compliance_status = "COMPLIANT" if status['is_compliant'] else "NOT COMPLIANT"
        report.append(f"\nStatus: {compliance_status}")
        report.append(f"Required Items: {status['required_completed']}/{status['required_total']}")
        report.append(f"Compliance: {status['compliance_percentage']:.1f}%")
        
        if status['missing_required']:
            report.append(f"\nMissing Required Items:")
            for item_id in status['missing_required']:
                for category, items in self.REQUIREMENTS.items():
                    for i, desc, _ in items:
                        if i == item_id:
                            report.append(f"  - {item_id}: {desc}")
        
        return "\n".join(report)


@dataclass 
class GEOSubmissionGenerator:
    """Generate GEO submission files"""
    
    def __init__(self, series_title: str, series_summary: str):
        self.series_title = series_title
        self.series_summary = series_summary
        self.samples = []
        self.platform = None
        self.contributors = []
    
    def set_platform(self, platform_id: str, platform_name: str):
        """Set array platform"""
        self.platform = {
            'id': platform_id,
            'name': platform_name
        }
    
    def add_contributor(self, name: str, email: str = None, affiliation: str = None):
        """Add contributor"""
        self.contributors.append({
            'name': name,
            'email': email,
            'affiliation': affiliation
        })
    
    def add_sample(self, 
                   sample_id: str,
                   title: str,
                   source_name: str,
                   organism: str = 'Homo sapiens',
                   characteristics: Dict = None,
                   molecule: str = 'genomic DNA',
                   label: str = 'Cy3',
                   description: str = None) -> Dict:
        """Add sample metadata"""
        sample = {
            'sample_id': sample_id,
            'title': title,
            'source_name': source_name,
            'organism': organism,
            'characteristics': characteristics or {},
            'molecule': molecule,
            'label': label,
            'description': description
        }
        self.samples.append(sample)
        return sample
    
    def generate_soft_file(self) -> str:
        """Generate SOFT format file for GEO submission"""
        soft = []
        
        # Series section
        soft.append("^SERIES")
        soft.append(f"!Series_title = {self.series_title}")
        soft.append(f"!Series_summary = {self.series_summary}")
        soft.append(f"!Series_type = Methylation profiling by array")
        
        for contrib in self.contributors:
            soft.append(f"!Series_contributor = {contrib['name']}")
        
        soft.append("")
        
        # Platform section
        if self.platform:
            soft.append("^PLATFORM")
            soft.append(f"!Platform_geo_accession = {self.platform['id']}")
            soft.append(f"!Platform_title = {self.platform['name']}")
            soft.append("")
        
        # Sample sections
        for sample in self.samples:
            soft.append(f"^SAMPLE = {sample['sample_id']}")
            soft.append(f"!Sample_title = {sample['title']}")
            soft.append(f"!Sample_source_name = {sample['source_name']}")
            soft.append(f"!Sample_organism = {sample['organism']}")
            soft.append(f"!Sample_molecule = {sample['molecule']}")
            soft.append(f"!Sample_label = {sample['label']}")
            
            for key, value in sample['characteristics'].items():
                soft.append(f"!Sample_characteristics_ch1 = {key}: {value}")
            
            if sample['description']:
                soft.append(f"!Sample_description = {sample['description']}")
            
            soft.append("")
        
        return "\n".join(soft)
    
    def generate_metadata_spreadsheet(self) -> pd.DataFrame:
        """Generate metadata spreadsheet for submission"""
        rows = []
        for sample in self.samples:
            row = {
                'Sample_ID': sample['sample_id'],
                'Sample_Title': sample['title'],
                'Source_Name': sample['source_name'],
                'Organism': sample['organism'],
                'Molecule': sample['molecule'],
                'Label': sample['label']
            }
            for key, value in sample['characteristics'].items():
                row[f'Characteristic_{key}'] = value
            rows.append(row)
        
        return pd.DataFrame(rows)


@dataclass
class ArrayExpressSubmissionGenerator:
    """Generate ArrayExpress (EBI) submission files"""
    
    def __init__(self, experiment_title: str, experiment_description: str):
        self.experiment_title = experiment_title
        self.experiment_description = experiment_description
        self.experiment_type = "methylation profiling by array"
        self.samples = []
        self.protocols = []
        self.array_design = None
    
    def set_array_design(self, accession: str, name: str):
        """Set array design reference"""
        self.array_design = {
            'accession': accession,
            'name': name
        }
    
    def add_protocol(self, 
                     protocol_type: str,
                     name: str,
                     description: str,
                     hardware: str = None,
                     software: str = None) -> Dict:
        """Add experimental protocol"""
        protocol = {
            'type': protocol_type,
            'name': name,
            'description': description,
            'hardware': hardware,
            'software': software
        }
        self.protocols.append(protocol)
        return protocol
    
    def add_sample(self,
                   sample_name: str,
                   material_type: str = 'whole blood',
                   characteristics: Dict = None) -> Dict:
        """Add sample"""
        sample = {
            'name': sample_name,
            'material_type': material_type,
            'characteristics': characteristics or {}
        }
        self.samples.append(sample)
        return sample
    
    def generate_idf_file(self) -> str:
        """Generate Investigation Description Format (IDF) file"""
        idf = []
        
        idf.append(f"Investigation Title\t{self.experiment_title}")
        idf.append(f"Experiment Description\t{self.experiment_description}")
        idf.append(f"Experimental Design\tcase control design")
        idf.append(f"Experimental Factor Name\tDisease")
        idf.append(f"Experimental Factor Type\tdisease")
        
        if self.array_design:
            idf.append(f"Array Design REF\t{self.array_design['accession']}")
        
        idf.append("")
        idf.append("Protocol Name\tProtocol Type\tProtocol Description")
        for protocol in self.protocols:
            idf.append(f"{protocol['name']}\t{protocol['type']}\t{protocol['description']}")
        
        return "\n".join(idf)
    
    def generate_sdrf_file(self) -> str:
        """Generate Sample and Data Relationship Format (SDRF) file"""
        headers = [
            "Source Name",
            "Material Type", 
            "Characteristics[organism]",
            "Characteristics[disease]",
            "Protocol REF",
            "Extract Name",
            "Labeled Extract Name",
            "Array Design REF",
            "Assay Name",
            "Array Data File"
        ]
        
        sdrf = ["\t".join(headers)]
        
        for sample in self.samples:
            row = [
                sample['name'],
                sample['material_type'],
                sample['characteristics'].get('organism', 'Homo sapiens'),
                sample['characteristics'].get('disease', 'normal'),
                self.protocols[0]['name'] if self.protocols else '',
                f"{sample['name']}_extract",
                f"{sample['name']}_labeled",
                self.array_design['accession'] if self.array_design else '',
                f"{sample['name']}_assay",
                f"{sample['name']}.idat"
            ]
            sdrf.append("\t".join(row))
        
        return "\n".join(sdrf)


def test_miame_standards():
    """Test MIAME module"""
    print("=" * 60)
    print("MIAME STANDARDS MODULE - TEST")
    print("=" * 60)
    
    # Test MIAME checklist
    print("\n[1] MIAME Checklist:")
    checklist = MIAMEChecklist()
    checklist.set_item('ED1', 'Case-control methylation study')
    checklist.set_item('ED2', 'Addiction vs healthy controls')
    checklist.set_item('ED3', 'Substance use disorder')
    checklist.set_item('ED4', '100 hybridizations')
    status = checklist.get_compliance_status()
    print(f"  Compliance: {status['compliance_percentage']:.1f}%")
    print(f"  Missing: {len(status['missing_required'])} items")
    
    # Test GEO submission
    print("\n[2] GEO Submission Generator:")
    geo = GEOSubmissionGenerator(
        series_title="DNA Methylation in Substance Use Disorder",
        series_summary="Epigenome-wide association study of addiction"
    )
    geo.set_platform('GPL21145', 'Illumina MethylationEPIC BeadChip')
    geo.add_contributor('EpiClock Team', 'epiclock@example.org')
    geo.add_sample(
        'GSM001',
        'Control_01',
        'Peripheral blood',
        characteristics={'tissue': 'whole blood', 'age': '35', 'sex': 'male'}
    )
    soft = geo.generate_soft_file()
    print(f"  SOFT file lines: {len(soft.split(chr(10)))}")
    
    # Test ArrayExpress
    print("\n[3] ArrayExpress Submission:")
    ae = ArrayExpressSubmissionGenerator(
        experiment_title="Methylation profiling of SUD",
        experiment_description="EWAS study"
    )
    ae.set_array_design('A-GEOD-21145', 'MethylationEPIC')
    ae.add_protocol('nucleic acid extraction', 'DNA extraction', 'Qiagen DNeasy Blood kit')
    ae.add_sample('Sample_001', characteristics={'organism': 'Homo sapiens', 'disease': 'SUD'})
    idf = ae.generate_idf_file()
    sdrf = ae.generate_sdrf_file()
    print(f"  IDF lines: {len(idf.split(chr(10)))}")
    print(f"  SDRF lines: {len(sdrf.split(chr(10)))}")
    
    print("\n" + "=" * 60)
    print("MIAME Standards Test Complete")


if __name__ == "__main__":
    test_miame_standards()
