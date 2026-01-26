"""
GATHER (Gene List Reporting) Standards Module
EpiClock v4.0 - Publication Ready

Implements:
- Gene list reporting guidelines
- Pathway analysis standards
- Gene ontology enrichment reporting
- Functional annotation requirements
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class GATHERChecklist:
    """GATHER Guidelines for Reporting Gene Lists"""
    
    GUIDELINES = {
        'gene_list_generation': [
            ('G1', 'Describe algorithm/method used to generate gene list', True),
            ('G2', 'Report statistical threshold and multiple testing correction', True),
            ('G3', 'Report number of genes before and after filtering', True),
            ('G4', 'Provide complete gene list in supplementary materials', True),
            ('G5', 'Use standard gene nomenclature (HGNC symbols)', True)
        ],
        'annotation_database': [
            ('A1', 'Report annotation database used (GO, KEGG, Reactome)', True),
            ('A2', 'Report version/date of annotation database', True),
            ('A3', 'Report background gene set used', True),
            ('A4', 'Describe any custom annotations', False)
        ],
        'enrichment_analysis': [
            ('E1', 'Report enrichment method (hypergeometric, GSEA)', True),
            ('E2', 'Report multiple testing correction for enrichment', True),
            ('E3', 'Report significance threshold for enrichment', True),
            ('E4', 'Report number of categories tested', True),
            ('E5', 'Report overlap genes for significant terms', True)
        ],
        'results_reporting': [
            ('R1', 'Report p-values and adjusted p-values', True),
            ('R2', 'Report fold enrichment or enrichment ratio', True),
            ('R3', 'Report number of genes in each category', True),
            ('R4', 'Visualize results (bar plot, bubble plot)', False),
            ('R5', 'Discuss biological relevance of top terms', True)
        ]
    }
    
    def __init__(self):
        self.completed = {}
        self.notes = {}
        for category in self.GUIDELINES:
            for item_id, _, _ in self.GUIDELINES[category]:
                self.completed[item_id] = False
                self.notes[item_id] = ""
    
    def mark_complete(self, item_id: str, notes: str = ""):
        """Mark guideline item as complete"""
        if item_id in self.completed:
            self.completed[item_id] = True
            self.notes[item_id] = notes
    
    def get_compliance_status(self) -> Dict:
        """Get compliance status"""
        required = []
        for category, items in self.GUIDELINES.items():
            for item_id, _, is_required in items:
                if is_required:
                    required.append(item_id)
        
        completed_required = sum(1 for i in required if self.completed.get(i, False))
        
        return {
            'required_completed': completed_required,
            'required_total': len(required),
            'compliance_percentage': completed_required / len(required) * 100 if required else 0,
            'is_compliant': completed_required == len(required)
        }
    
    def generate_report(self) -> str:
        """Generate GATHER compliance report"""
        status = self.get_compliance_status()
        
        report = []
        report.append("=" * 60)
        report.append("GATHER GUIDELINES COMPLIANCE REPORT")
        report.append("Gene List Reporting Standards")
        report.append("=" * 60)
        
        compliance = "COMPLIANT" if status['is_compliant'] else "NOT COMPLIANT"
        report.append(f"\nStatus: {compliance}")
        report.append(f"Required Items: {status['required_completed']}/{status['required_total']}")
        report.append(f"Compliance: {status['compliance_percentage']:.1f}%")
        
        for category, items in self.GUIDELINES.items():
            report.append(f"\n{category.upper().replace('_', ' ')}")
            report.append("-" * 40)
            for item_id, description, is_required in items:
                check = "[X]" if self.completed.get(item_id, False) else "[ ]"
                req = "*" if is_required else " "
                report.append(f"  {check}{req} {item_id}: {description}")
        
        return "\n".join(report)


@dataclass
class GeneListReporter:
    """Standardized gene list reporting"""
    
    def __init__(self):
        self.gene_lists = {}
        self.enrichment_results = {}
    
    def add_gene_list(self,
                      list_name: str,
                      genes: List[str],
                      source: str,
                      method: str,
                      threshold: str,
                      background_size: int = None) -> Dict:
        """Add a gene list with metadata"""
        gene_list = {
            'name': list_name,
            'genes': genes,
            'n_genes': len(genes),
            'source': source,
            'method': method,
            'threshold': threshold,
            'background_size': background_size,
            'created': datetime.now().isoformat()
        }
        self.gene_lists[list_name] = gene_list
        return gene_list
    
    def convert_to_standard_symbols(self, genes: List[str]) -> Tuple[List[str], List[str]]:
        """
        Convert gene identifiers to HGNC symbols
        Returns (converted_genes, unmapped_genes)
        
        Note: In production, this would use a proper gene ID mapping service
        """
        # Simulated conversion - in real use, would call HGNC/Ensembl API
        converted = []
        unmapped = []
        
        for gene in genes:
            if gene.startswith('ENSG'):
                # Simulated Ensembl to HGNC conversion
                converted.append(f"GENE_{gene[-4:]}")
            else:
                converted.append(gene.upper())
        
        return converted, unmapped
    
    def generate_supplementary_table(self, list_name: str) -> pd.DataFrame:
        """Generate supplementary gene list table"""
        if list_name not in self.gene_lists:
            return pd.DataFrame()
        
        gene_list = self.gene_lists[list_name]
        
        return pd.DataFrame({
            'Gene_Symbol': gene_list['genes'],
            'Source': [gene_list['source']] * len(gene_list['genes']),
            'Selection_Method': [gene_list['method']] * len(gene_list['genes']),
            'Threshold': [gene_list['threshold']] * len(gene_list['genes'])
        })


@dataclass
class PathwayAnalysisReporter:
    """Standardized pathway analysis reporting"""
    
    DATABASES = {
        'GO_BP': 'Gene Ontology Biological Process',
        'GO_MF': 'Gene Ontology Molecular Function',
        'GO_CC': 'Gene Ontology Cellular Component',
        'KEGG': 'KEGG Pathways',
        'Reactome': 'Reactome Pathways',
        'WikiPathways': 'WikiPathways',
        'MSigDB_H': 'MSigDB Hallmark Gene Sets',
        'MSigDB_C2': 'MSigDB Curated Gene Sets'
    }
    
    def __init__(self):
        self.analyses = []
    
    def add_enrichment_analysis(self,
                                 gene_list: List[str],
                                 database: str,
                                 database_version: str,
                                 method: str = 'hypergeometric',
                                 background_genes: int = 20000,
                                 p_threshold: float = 0.05,
                                 correction_method: str = 'BH') -> Dict:
        """Add enrichment analysis parameters"""
        analysis = {
            'n_input_genes': len(gene_list),
            'database': database,
            'database_name': self.DATABASES.get(database, database),
            'database_version': database_version,
            'method': method,
            'background_genes': background_genes,
            'p_threshold': p_threshold,
            'correction_method': correction_method,
            'timestamp': datetime.now().isoformat()
        }
        self.analyses.append(analysis)
        return analysis
    
    def simulate_enrichment_results(self, n_terms: int = 20) -> pd.DataFrame:
        """Simulate enrichment results for demonstration"""
        np.random.seed(42)
        
        terms = [f"GO:00{i:05d}" for i in range(n_terms)]
        names = [
            'response to drug', 'regulation of neurotransmitter', 
            'synaptic transmission', 'dopamine metabolic process',
            'reward response', 'addiction behavior', 'learning and memory',
            'stress response', 'immune response', 'cell death',
            'oxidative stress', 'inflammation', 'metabolism',
            'signal transduction', 'gene expression', 'protein binding',
            'transcription regulation', 'cell cycle', 'apoptosis', 'autophagy'
        ][:n_terms]
        
        p_values = 10 ** np.random.uniform(-10, -1, n_terms)
        p_adjusted = np.minimum(p_values * n_terms, 1.0)  # Simple Bonferroni
        
        return pd.DataFrame({
            'Term_ID': terms,
            'Term_Name': names,
            'P_Value': p_values,
            'P_Adjusted': p_adjusted,
            'Fold_Enrichment': np.random.uniform(1.5, 10, n_terms),
            'Overlap_Genes': np.random.randint(3, 50, n_terms),
            'Term_Size': np.random.randint(10, 500, n_terms),
            'Background_Size': [20000] * n_terms
        }).sort_values('P_Value')
    
    def generate_methods_text(self) -> str:
        """Generate methods section text for pathway analysis"""
        if not self.analyses:
            return "No pathway analysis performed."
        
        texts = []
        for analysis in self.analyses:
            text = f"Gene ontology and pathway enrichment analysis was performed using "
            text += f"the {analysis['method']} test against the {analysis['database_name']} "
            text += f"(version {analysis['database_version']}). "
            text += f"A total of {analysis['n_input_genes']} genes were analyzed against "
            text += f"a background of {analysis['background_genes']} genes. "
            text += f"Multiple testing was corrected using the {analysis['correction_method']} method, "
            text += f"and terms with adjusted p-value < {analysis['p_threshold']} were considered significant."
            texts.append(text)
        
        return " ".join(texts)
    
    def generate_results_table(self, results: pd.DataFrame, top_n: int = 10) -> str:
        """Generate formatted results table"""
        top_results = results.head(top_n)
        
        table = []
        table.append("TOP ENRICHED TERMS")
        table.append("=" * 80)
        table.append(f"{'Term ID':<12} {'Term Name':<30} {'P-adj':<12} {'Fold':<8} {'Genes':<8}")
        table.append("-" * 80)
        
        for _, row in top_results.iterrows():
            table.append(
                f"{row['Term_ID']:<12} {row['Term_Name'][:28]:<30} "
                f"{row['P_Adjusted']:.2e}  {row['Fold_Enrichment']:.2f}    {row['Overlap_Genes']}"
            )
        
        return "\n".join(table)


@dataclass
class GeneOntologyReporter:
    """Gene Ontology specific reporting"""
    
    GO_EVIDENCE_CODES = {
        'EXP': 'Inferred from Experiment',
        'IDA': 'Inferred from Direct Assay',
        'IPI': 'Inferred from Physical Interaction',
        'IMP': 'Inferred from Mutant Phenotype',
        'IGI': 'Inferred from Genetic Interaction',
        'IEP': 'Inferred from Expression Pattern',
        'HTP': 'Inferred from High Throughput Experiment',
        'HDA': 'Inferred from High Throughput Direct Assay',
        'HMP': 'Inferred from High Throughput Mutant Phenotype',
        'HGI': 'Inferred from High Throughput Genetic Interaction',
        'HEP': 'Inferred from High Throughput Expression Pattern',
        'IBA': 'Inferred from Biological aspect of Ancestor',
        'IBD': 'Inferred from Biological aspect of Descendant',
        'IKR': 'Inferred from Key Residues',
        'IRD': 'Inferred from Rapid Divergence',
        'ISS': 'Inferred from Sequence or structural Similarity',
        'ISO': 'Inferred from Sequence Orthology',
        'ISA': 'Inferred from Sequence Alignment',
        'ISM': 'Inferred from Sequence Model',
        'IGC': 'Inferred from Genomic Context',
        'RCA': 'Inferred from Reviewed Computational Analysis',
        'TAS': 'Traceable Author Statement',
        'NAS': 'Non-traceable Author Statement',
        'IC': 'Inferred by Curator',
        'ND': 'No biological Data available',
        'IEA': 'Inferred from Electronic Annotation'
    }
    
    def __init__(self):
        self.go_version = None
        self.evidence_filter = []
    
    def set_go_version(self, version: str, date: str):
        """Set GO version used"""
        self.go_version = {
            'version': version,
            'date': date
        }
    
    def set_evidence_filter(self, evidence_codes: List[str]):
        """Set evidence codes to include"""
        self.evidence_filter = evidence_codes
    
    def generate_go_methods(self) -> str:
        """Generate GO-specific methods text"""
        text = "Gene Ontology analysis was performed using "
        
        if self.go_version:
            text += f"GO version {self.go_version['version']} (released {self.go_version['date']}). "
        else:
            text += "the Gene Ontology database. "
        
        if self.evidence_filter:
            codes = ', '.join(self.evidence_filter)
            text += f"Only annotations with the following evidence codes were considered: {codes}. "
        
        return text
    
    def describe_evidence_code(self, code: str) -> str:
        """Get description of evidence code"""
        return self.GO_EVIDENCE_CODES.get(code, 'Unknown evidence code')


def test_gather_standards():
    """Test GATHER standards module"""
    print("=" * 60)
    print("GATHER STANDARDS MODULE - TEST")
    print("=" * 60)
    
    # Test GATHER Checklist
    print("\n[1] GATHER Checklist:")
    checklist = GATHERChecklist()
    checklist.mark_complete('G1', 'Differential methylation analysis')
    checklist.mark_complete('G2', 'FDR < 0.05')
    checklist.mark_complete('G5', 'HGNC symbols used')
    checklist.mark_complete('A1', 'GO and KEGG')
    status = checklist.get_compliance_status()
    print(f"  Compliance: {status['compliance_percentage']:.1f}%")
    
    # Test Gene List Reporter
    print("\n[2] Gene List Reporter:")
    reporter = GeneListReporter()
    genes = ['OPRM1', 'DRD2', 'COMT', 'SLC6A4', 'BDNF', 'GABRA2']
    gene_list = reporter.add_gene_list(
        'Addiction_Genes',
        genes,
        source='EWAS analysis',
        method='Linear regression with FDR correction',
        threshold='FDR < 0.05, |delta beta| > 0.1',
        background_size=485512
    )
    print(f"  Gene list size: {gene_list['n_genes']}")
    
    # Test Pathway Analysis Reporter
    print("\n[3] Pathway Analysis Reporter:")
    pathway_reporter = PathwayAnalysisReporter()
    pathway_reporter.add_enrichment_analysis(
        genes,
        database='GO_BP',
        database_version='2024-01-01',
        method='hypergeometric',
        correction_method='BH'
    )
    results = pathway_reporter.simulate_enrichment_results()
    print(f"  Enriched terms: {len(results)}")
    print(f"  Top term: {results.iloc[0]['Term_Name']}")
    
    # Test GO Reporter
    print("\n[4] GO Reporter:")
    go_reporter = GeneOntologyReporter()
    go_reporter.set_go_version('2024-01-01', 'January 1, 2024')
    go_reporter.set_evidence_filter(['EXP', 'IDA', 'IMP', 'TAS'])
    methods = go_reporter.generate_go_methods()
    print(f"  Methods text length: {len(methods)} chars")
    
    print("\n" + "=" * 60)
    print("GATHER Standards Test Complete")


if __name__ == "__main__":
    test_gather_standards()
