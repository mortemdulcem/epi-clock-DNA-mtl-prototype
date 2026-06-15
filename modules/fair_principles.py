"""
FAIR Principles Implementation
EpiClock v4.0 - Publication Ready

Implements:
- Findable: Persistent identifiers, rich metadata
- Accessible: Open protocols, authentication where needed
- Interoperable: Standard vocabularies, qualified references
- Reusable: Clear licenses, provenance, domain standards
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
import uuid


@dataclass
class FAIRAssessment:
    """FAIR Principles Assessment Framework"""
    
    PRINCIPLES = {
        'findable': {
            'F1': ('Data assigned globally unique and persistent identifier', 3),
            'F2': ('Data described with rich metadata', 2),
            'F3': ('Metadata clearly includes identifier of data', 2),
            'F4': ('Data registered in searchable resource', 2)
        },
        'accessible': {
            'A1': ('Data retrievable by identifier using standard protocol', 3),
            'A1.1': ('Protocol is open, free, and universally implementable', 2),
            'A1.2': ('Protocol allows authentication where necessary', 1),
            'A2': ('Metadata accessible even when data no longer available', 2)
        },
        'interoperable': {
            'I1': ('Data uses formal, accessible, shared language', 2),
            'I2': ('Data uses vocabularies that follow FAIR principles', 2),
            'I3': ('Data includes qualified references to other data', 2)
        },
        'reusable': {
            'R1': ('Data richly described with plurality of attributes', 2),
            'R1.1': ('Data released with clear, accessible usage license', 3),
            'R1.2': ('Data associated with detailed provenance', 2),
            'R1.3': ('Data meets domain-relevant community standards', 2)
        }
    }
    
    def __init__(self):
        self.scores = {}
        self.notes = {}
        for category in self.PRINCIPLES:
            for principle_id in self.PRINCIPLES[category]:
                self.scores[principle_id] = 0
                self.notes[principle_id] = ""
    
    def score_principle(self, principle_id: str, score: int, notes: str = ""):
        """Score a FAIR principle (0-4 scale)"""
        if principle_id in self.scores:
            self.scores[principle_id] = min(4, max(0, score))
            self.notes[principle_id] = notes
    
    def get_fair_score(self) -> Dict:
        """Calculate overall FAIR score"""
        category_scores = {}
        total_weighted = 0
        total_weight = 0
        
        for category, principles in self.PRINCIPLES.items():
            cat_score = 0
            cat_max = 0
            for principle_id, (_, weight) in principles.items():
                cat_score += self.scores.get(principle_id, 0) * weight
                cat_max += 4 * weight
                total_weighted += self.scores.get(principle_id, 0) * weight
                total_weight += 4 * weight
            
            category_scores[category] = {
                'score': cat_score,
                'max': cat_max,
                'percentage': cat_score / cat_max * 100 if cat_max > 0 else 0
            }
        
        return {
            'overall_score': total_weighted,
            'overall_max': total_weight,
            'overall_percentage': total_weighted / total_weight * 100 if total_weight > 0 else 0,
            'category_scores': category_scores,
            'fair_level': self._get_fair_level(total_weighted / total_weight * 100 if total_weight > 0 else 0)
        }
    
    def _get_fair_level(self, percentage: float) -> str:
        """Determine FAIR compliance level"""
        if percentage >= 90:
            return "Excellent (Gold)"
        elif percentage >= 75:
            return "Good (Silver)"
        elif percentage >= 50:
            return "Acceptable (Bronze)"
        else:
            return "Needs Improvement"
    
    def generate_report(self) -> str:
        """Generate FAIR assessment report"""
        fair_score = self.get_fair_score()
        
        report = []
        report.append("=" * 60)
        report.append("FAIR PRINCIPLES ASSESSMENT REPORT")
        report.append("=" * 60)
        report.append(f"\nOverall Score: {fair_score['overall_score']:.0f}/{fair_score['overall_max']}")
        report.append(f"Percentage: {fair_score['overall_percentage']:.1f}%")
        report.append(f"FAIR Level: {fair_score['fair_level']}")
        
        for category, principles in self.PRINCIPLES.items():
            cat_score = fair_score['category_scores'][category]
            report.append(f"\n{category.upper()} ({cat_score['percentage']:.0f}%)")
            report.append("-" * 40)
            for principle_id, (description, weight) in principles.items():
                score = self.scores.get(principle_id, 0)
                report.append(f"  {principle_id}: {score}/4 - {description[:45]}...")
        
        return "\n".join(report)


@dataclass
class PersistentIdentifier:
    """Generate and manage persistent identifiers"""
    
    IDENTIFIER_TYPES = {
        'doi': 'Digital Object Identifier',
        'orcid': 'ORCID (researcher)',
        'ror': 'Research Organization Registry',
        'pmid': 'PubMed ID',
        'geo': 'GEO Accession',
        'arrayexpress': 'ArrayExpress Accession'
    }
    
    def __init__(self):
        self.identifiers = {}
    
    def generate_internal_id(self, resource_type: str = 'dataset') -> str:
        """Generate internal unique identifier"""
        return f"epiclock:{resource_type}:{uuid.uuid4().hex[:12]}"
    
    def add_identifier(self, id_type: str, value: str, resource_name: str):
        """Add persistent identifier"""
        self.identifiers[resource_name] = {
            'type': id_type,
            'value': value,
            'description': self.IDENTIFIER_TYPES.get(id_type, id_type),
            'added': datetime.now().isoformat()
        }
    
    def generate_citation(self, resource_name: str) -> str:
        """Generate citation with identifier"""
        if resource_name not in self.identifiers:
            return f"{resource_name} (no identifier assigned)"
        
        id_info = self.identifiers[resource_name]
        if id_info['type'] == 'doi':
            return f"{resource_name}. https://doi.org/{id_info['value']}"
        elif id_info['type'] == 'geo':
            return f"{resource_name}. GEO Accession: {id_info['value']} (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={id_info['value']})"
        else:
            return f"{resource_name}. {id_info['description']}: {id_info['value']}"


@dataclass
class MetadataSchema:
    """Rich metadata schema for FAIR compliance"""
    
    DUBLIN_CORE_FIELDS = [
        'title', 'creator', 'subject', 'description', 'publisher',
        'contributor', 'date', 'type', 'format', 'identifier',
        'source', 'language', 'relation', 'coverage', 'rights'
    ]
    
    DATACITE_FIELDS = [
        'identifier', 'creators', 'titles', 'publisher', 'publicationYear',
        'subjects', 'contributors', 'dates', 'resourceType', 'descriptions',
        'geoLocations', 'fundingReferences', 'relatedIdentifiers', 'version'
    ]
    
    def __init__(self):
        self.metadata = {}
    
    def set_field(self, field: str, value: Any):
        """Set metadata field"""
        self.metadata[field] = value
    
    def generate_dublin_core(self) -> Dict:
        """Generate Dublin Core metadata"""
        dc = {}
        for field in self.DUBLIN_CORE_FIELDS:
            if field in self.metadata:
                dc[f'dc:{field}'] = self.metadata[field]
        return dc
    
    def generate_datacite(self) -> Dict:
        """Generate DataCite metadata"""
        datacite = {}
        for field in self.DATACITE_FIELDS:
            if field in self.metadata:
                datacite[field] = self.metadata[field]
        return datacite
    
    def generate_schema_org(self) -> Dict:
        """Generate Schema.org JSON-LD metadata"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Dataset"
        }
        
        mappings = {
            'title': 'name',
            'description': 'description',
            'creator': 'creator',
            'date': 'datePublished',
            'rights': 'license',
            'identifier': 'identifier'
        }
        
        for local_field, schema_field in mappings.items():
            if local_field in self.metadata:
                schema[schema_field] = self.metadata[local_field]
        
        return schema


@dataclass
class DataLicense:
    """Data licensing for FAIR compliance"""
    
    COMMON_LICENSES = {
        'CC0': {
            'name': 'CC0 1.0 Universal (Public Domain)',
            'url': 'https://creativecommons.org/publicdomain/zero/1.0/',
            'allows_commercial': True,
            'allows_derivatives': True,
            'requires_attribution': False
        },
        'CC-BY-4.0': {
            'name': 'Creative Commons Attribution 4.0',
            'url': 'https://creativecommons.org/licenses/by/4.0/',
            'allows_commercial': True,
            'allows_derivatives': True,
            'requires_attribution': True
        },
        'CC-BY-NC-4.0': {
            'name': 'Creative Commons Attribution NonCommercial 4.0',
            'url': 'https://creativecommons.org/licenses/by-nc/4.0/',
            'allows_commercial': False,
            'allows_derivatives': True,
            'requires_attribution': True
        },
        'CC-BY-SA-4.0': {
            'name': 'Creative Commons Attribution ShareAlike 4.0',
            'url': 'https://creativecommons.org/licenses/by-sa/4.0/',
            'allows_commercial': True,
            'allows_derivatives': True,
            'requires_attribution': True
        }
    }
    
    def __init__(self, license_id: str = 'CC-BY-4.0'):
        self.license_id = license_id
        self.license_info = self.COMMON_LICENSES.get(license_id, {
            'name': license_id,
            'url': '',
            'allows_commercial': False,
            'allows_derivatives': False,
            'requires_attribution': True
        })
    
    def generate_license_text(self) -> str:
        """Generate license statement"""
        text = f"This dataset is released under {self.license_info['name']}.\n"
        text += f"License URL: {self.license_info['url']}\n\n"
        
        if self.license_info['requires_attribution']:
            text += "Attribution is required when using this data.\n"
        if not self.license_info['allows_commercial']:
            text += "Commercial use is not permitted.\n"
        if not self.license_info['allows_derivatives']:
            text += "Derivative works are not permitted.\n"
        
        return text
    
    def generate_data_availability_statement(self, 
                                              repository: str = "GEO",
                                              accession: str = None) -> str:
        """Generate data availability statement"""
        statement = "DATA AVAILABILITY STATEMENT\n"
        statement += "=" * 40 + "\n\n"
        
        if accession:
            statement += f"The data that support the findings of this study are openly available in {repository} "
            statement += f"with accession number {accession}.\n\n"
        else:
            statement += f"The data supporting the findings of this study will be deposited in {repository} "
            statement += "upon acceptance of this manuscript.\n\n"
        
        statement += f"License: {self.license_info['name']}\n"
        statement += f"URL: {self.license_info['url']}\n"
        
        return statement


@dataclass
class DataProvenance:
    """Track data provenance for FAIR compliance"""
    
    def __init__(self):
        self.provenance_records = []
    
    def record_activity(self,
                        activity_type: str,
                        description: str,
                        agent: str,
                        inputs: List[str] = None,
                        outputs: List[str] = None,
                        software: str = None,
                        version: str = None):
        """Record provenance activity"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'activity_type': activity_type,
            'description': description,
            'agent': agent,
            'inputs': inputs or [],
            'outputs': outputs or [],
            'software': software,
            'version': version
        }
        self.provenance_records.append(record)
    
    def generate_prov_document(self) -> str:
        """Generate W3C PROV-style provenance document"""
        prov = []
        prov.append("PROVENANCE DOCUMENT")
        prov.append("=" * 50)
        
        for i, record in enumerate(self.provenance_records, 1):
            prov.append(f"\nActivity {i}: {record['activity_type']}")
            prov.append(f"  Description: {record['description']}")
            prov.append(f"  Agent: {record['agent']}")
            prov.append(f"  Timestamp: {record['timestamp']}")
            if record['software']:
                prov.append(f"  Software: {record['software']} v{record['version']}")
            if record['inputs']:
                prov.append(f"  Inputs: {', '.join(record['inputs'])}")
            if record['outputs']:
                prov.append(f"  Outputs: {', '.join(record['outputs'])}")
        
        return "\n".join(prov)


def test_fair_principles():
    """Test FAIR principles module"""
    print("=" * 60)
    print("FAIR PRINCIPLES MODULE - TEST")
    print("=" * 60)
    
    # Test FAIR Assessment
    print("\n[1] FAIR Assessment:")
    assessment = FAIRAssessment()
    assessment.score_principle('F1', 4, 'DOI assigned')
    assessment.score_principle('F2', 3, 'Rich metadata provided')
    assessment.score_principle('A1', 4, 'HTTP/HTTPS access')
    assessment.score_principle('I1', 3, 'Standard formats used')
    assessment.score_principle('R1.1', 4, 'CC-BY license')
    
    fair_score = assessment.get_fair_score()
    print(f"  Overall: {fair_score['overall_percentage']:.1f}%")
    print(f"  Level: {fair_score['fair_level']}")
    
    # Test Identifiers
    print("\n[2] Persistent Identifiers:")
    pid = PersistentIdentifier()
    internal_id = pid.generate_internal_id('methylation_data')
    print(f"  Internal ID: {internal_id}")
    pid.add_identifier('geo', 'GSE123456', 'Methylation Dataset')
    citation = pid.generate_citation('Methylation Dataset')
    print(f"  Citation: {citation[:60]}...")
    
    # Test Metadata
    print("\n[3] Metadata Schema:")
    metadata = MetadataSchema()
    metadata.set_field('title', 'DNA Methylation EWAS Dataset')
    metadata.set_field('creator', 'EpiClock Team')
    metadata.set_field('date', '2026-01-26')
    dc = metadata.generate_dublin_core()
    print(f"  Dublin Core fields: {len(dc)}")
    
    # Test License
    print("\n[4] Data License:")
    license = DataLicense('CC-BY-4.0')
    statement = license.generate_data_availability_statement('GEO', 'GSE123456')
    print(f"  License: {license.license_info['name']}")
    
    # Test Provenance
    print("\n[5] Data Provenance:")
    prov = DataProvenance()
    prov.record_activity(
        'preprocessing',
        'Normalization of methylation data',
        'EpiClock Pipeline',
        inputs=['raw_idat_files'],
        outputs=['normalized_betas.csv'],
        software='minfi',
        version='1.40.0'
    )
    print(f"  Provenance records: {len(prov.provenance_records)}")
    
    print("\n" + "=" * 60)
    print("FAIR Principles Test Complete")


if __name__ == "__main__":
    test_fair_principles()
