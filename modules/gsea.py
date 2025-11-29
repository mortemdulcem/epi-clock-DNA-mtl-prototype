"""
Gene Set Enrichment Analysis (GSEA) Module for EpiClock Prototype
Biological pathway analysis of differentially methylated CpGs
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@dataclass
class PathwayResult:
    """Result for a single pathway in enrichment analysis"""
    pathway_id: str
    pathway_name: str
    source: str
    n_genes: int
    n_significant_genes: int
    enrichment_score: float
    normalized_es: float
    p_value: float
    fdr_q_value: float
    leading_edge_genes: List[str]
    is_significant: bool


@dataclass
class GSEAResult:
    """Complete GSEA analysis result"""
    analysis_name: str
    substance_type: str
    n_cpgs_analyzed: int
    n_significant_cpgs: int
    n_pathways_tested: int
    n_significant_pathways: int
    top_pathways: List[PathwayResult]
    enriched_categories: Dict[str, int]


class GSEAnalyzer:
    """
    Gene Set Enrichment Analysis for DNA methylation data.
    Maps CpGs to genes and performs pathway enrichment analysis.
    """
    
    CPG_GENE_MAPPING = {
        'cg00000001': 'DNMT3A',
        'cg00000002': 'TET1',
        'cg00000003': 'TET2',
        'cg00000004': 'HDAC1',
        'cg00000005': 'HDAC2',
        'cg00000006': 'SIRT1',
        'cg00000007': 'SIRT3',
        'cg00000008': 'TP53',
        'cg00000009': 'CDKN2A',
        'cg00000010': 'FOXO3',
        'cg00000011': 'TERT',
        'cg00000012': 'TERC',
        'cg00000013': 'IGF1',
        'cg00000014': 'MTOR',
        'cg00000015': 'AMPK',
        'cg00000016': 'NRF2',
        'cg00000017': 'NFE2L2',
        'cg00000018': 'SOD2',
        'cg00000019': 'CAT',
        'cg00000020': 'GPX1',
        'cg00000021': 'IL6',
        'cg00000022': 'TNF',
        'cg00000023': 'IL1B',
        'cg00000024': 'NFKB1',
        'cg00000025': 'CRP',
        'cg00000026': 'GR',
        'cg00000027': 'NR3C1',
        'cg00000028': 'FKBP5',
        'cg00000029': 'CRH',
        'cg00000030': 'POMC',
        'cg00000031': 'DRD2',
        'cg00000032': 'DRD4',
        'cg00000033': 'SLC6A3',
        'cg00000034': 'SLC6A4',
        'cg00000035': 'OPRM1',
        'cg00000036': 'OPRD1',
        'cg00000037': 'COMT',
        'cg00000038': 'MAOA',
        'cg00000039': 'BDNF',
        'cg00000040': 'NGF'
    }
    
    PATHWAY_DATABASE = {
        'GO:0007568': {
            'name': 'Aging',
            'source': 'GO_BP',
            'genes': ['SIRT1', 'SIRT3', 'FOXO3', 'TERT', 'TERC', 'TP53', 'CDKN2A', 'IGF1', 'MTOR']
        },
        'GO:0006281': {
            'name': 'DNA Repair',
            'source': 'GO_BP',
            'genes': ['TP53', 'CDKN2A', 'TERT', 'DNMT3A', 'TET1', 'TET2']
        },
        'GO:0006954': {
            'name': 'Inflammatory Response',
            'source': 'GO_BP',
            'genes': ['IL6', 'TNF', 'IL1B', 'NFKB1', 'CRP', 'NFE2L2']
        },
        'GO:0006979': {
            'name': 'Response to Oxidative Stress',
            'source': 'GO_BP',
            'genes': ['NRF2', 'NFE2L2', 'SOD2', 'CAT', 'GPX1', 'SIRT3']
        },
        'GO:0042493': {
            'name': 'Response to Drug',
            'source': 'GO_BP',
            'genes': ['DRD2', 'DRD4', 'SLC6A3', 'SLC6A4', 'OPRM1', 'OPRD1', 'COMT', 'MAOA']
        },
        'GO:0007631': {
            'name': 'Feeding Behavior',
            'source': 'GO_BP',
            'genes': ['DRD2', 'OPRM1', 'BDNF', 'NGF', 'POMC']
        },
        'KEGG:hsa04010': {
            'name': 'MAPK signaling pathway',
            'source': 'KEGG',
            'genes': ['TP53', 'NFE2L2', 'NFKB1', 'BDNF', 'NGF']
        },
        'KEGG:hsa04068': {
            'name': 'FoxO signaling pathway',
            'source': 'KEGG',
            'genes': ['FOXO3', 'IGF1', 'SIRT1', 'AMPK', 'MTOR']
        },
        'KEGG:hsa04211': {
            'name': 'Longevity regulating pathway',
            'source': 'KEGG',
            'genes': ['SIRT1', 'SIRT3', 'FOXO3', 'IGF1', 'MTOR', 'AMPK']
        },
        'KEGG:hsa04728': {
            'name': 'Dopaminergic synapse',
            'source': 'KEGG',
            'genes': ['DRD2', 'DRD4', 'SLC6A3', 'COMT', 'MAOA']
        },
        'KEGG:hsa04080': {
            'name': 'Neuroactive ligand-receptor interaction',
            'source': 'KEGG',
            'genes': ['DRD2', 'DRD4', 'OPRM1', 'OPRD1', 'SLC6A4', 'NR3C1']
        },
        'KEGG:hsa05030': {
            'name': 'Cocaine addiction',
            'source': 'KEGG',
            'genes': ['DRD2', 'SLC6A3', 'BDNF', 'FOSB', 'CREB1']
        },
        'KEGG:hsa05031': {
            'name': 'Amphetamine addiction',
            'source': 'KEGG',
            'genes': ['DRD2', 'SLC6A3', 'TH', 'MAOA', 'COMT']
        },
        'KEGG:hsa05032': {
            'name': 'Morphine addiction',
            'source': 'KEGG',
            'genes': ['OPRM1', 'OPRD1', 'DRD2', 'GABA', 'CREB1']
        },
        'KEGG:hsa05034': {
            'name': 'Alcoholism',
            'source': 'KEGG',
            'genes': ['DRD2', 'OPRM1', 'GABA', 'NMDA', 'BDNF', 'CREB1']
        },
        'REACTOME:R-HSA-2262752': {
            'name': 'Cellular response to stress',
            'source': 'REACTOME',
            'genes': ['TP53', 'NFE2L2', 'NRF2', 'FOXO3', 'SIRT1', 'AMPK']
        },
        'REACTOME:R-HSA-212436': {
            'name': 'Generic transcription pathway',
            'source': 'REACTOME',
            'genes': ['DNMT3A', 'TET1', 'TET2', 'HDAC1', 'HDAC2', 'SIRT1']
        },
        'REACTOME:R-HSA-112316': {
            'name': 'Neuronal system',
            'source': 'REACTOME',
            'genes': ['DRD2', 'DRD4', 'SLC6A3', 'SLC6A4', 'BDNF', 'NGF']
        }
    }
    
    SUBSTANCE_PATHWAYS = {
        'alcohol': ['KEGG:hsa05034', 'GO:0006954', 'GO:0006979', 'KEGG:hsa04010'],
        'cocaine': ['KEGG:hsa05030', 'KEGG:hsa04728', 'GO:0042493', 'GO:0006954'],
        'opioids': ['KEGG:hsa05032', 'KEGG:hsa04080', 'GO:0042493', 'GO:0006979'],
        'methamphetamine': ['KEGG:hsa05031', 'KEGG:hsa04728', 'GO:0006979', 'GO:0006954'],
        'cannabis': ['KEGG:hsa04080', 'REACTOME:R-HSA-112316', 'GO:0007631'],
        'polysubstance': ['GO:0042493', 'GO:0006954', 'GO:0006979', 'KEGG:hsa04211', 'GO:0007568']
    }
    
    def __init__(self):
        np.random.seed(42)
        self._extend_cpg_gene_mapping()
    
    def _extend_cpg_gene_mapping(self):
        """Extend CpG to gene mapping with simulated data"""
        all_genes = set()
        for pathway in self.PATHWAY_DATABASE.values():
            all_genes.update(pathway['genes'])
        
        gene_list = list(all_genes)
        
        for i in range(40, 500):
            cpg_id = f"cg{str(i).zfill(8)}"
            gene = np.random.choice(gene_list)
            self.CPG_GENE_MAPPING[cpg_id] = gene
    
    def map_cpgs_to_genes(self, cpg_list: List[str]) -> Dict[str, str]:
        """Map CpG IDs to gene symbols"""
        mapping = {}
        for cpg in cpg_list:
            if cpg in self.CPG_GENE_MAPPING:
                mapping[cpg] = self.CPG_GENE_MAPPING[cpg]
            else:
                idx = hash(cpg) % len(list(self.CPG_GENE_MAPPING.values()))
                genes = list(set(self.CPG_GENE_MAPPING.values()))
                mapping[cpg] = genes[idx % len(genes)]
        return mapping
    
    def perform_enrichment(self,
                           significant_cpgs: List[str],
                           background_cpgs: List[str],
                           substance_type: str = None,
                           fdr_threshold: float = 0.05) -> GSEAResult:
        """
        Perform gene set enrichment analysis.
        
        Args:
            significant_cpgs: List of significantly differentially methylated CpGs
            background_cpgs: List of all tested CpGs (background)
            substance_type: Optional substance type for pathway prioritization
            fdr_threshold: FDR threshold for significance
        
        Returns:
            GSEAResult with enrichment results
        """
        sig_genes = set(self.map_cpgs_to_genes(significant_cpgs).values())
        bg_genes = set(self.map_cpgs_to_genes(background_cpgs).values())
        
        pathway_results = []
        
        for pathway_id, pathway_info in self.PATHWAY_DATABASE.items():
            pathway_genes = set(pathway_info['genes'])
            
            sig_in_pathway = len(sig_genes & pathway_genes)
            sig_not_in_pathway = len(sig_genes) - sig_in_pathway
            bg_in_pathway = len(bg_genes & pathway_genes)
            bg_not_in_pathway = len(bg_genes) - bg_in_pathway
            
            if sig_in_pathway > 0 and bg_in_pathway > 0:
                oddsratio, p_value = stats.fisher_exact([
                    [sig_in_pathway, sig_not_in_pathway],
                    [bg_in_pathway - sig_in_pathway, bg_not_in_pathway - sig_not_in_pathway]
                ], alternative='greater')
            else:
                oddsratio, p_value = 1.0, 1.0
            
            enrichment_score = np.log2(oddsratio + 0.001) if oddsratio > 0 else 0
            
            expected = len(sig_genes) * (len(pathway_genes) / len(bg_genes)) if len(bg_genes) > 0 else 0
            if expected > 0:
                normalized_es = (sig_in_pathway - expected) / np.sqrt(expected)
            else:
                normalized_es = 0
            
            leading_edge = list(sig_genes & pathway_genes)
            
            pathway_results.append(PathwayResult(
                pathway_id=pathway_id,
                pathway_name=pathway_info['name'],
                source=pathway_info['source'],
                n_genes=len(pathway_genes),
                n_significant_genes=sig_in_pathway,
                enrichment_score=round(enrichment_score, 4),
                normalized_es=round(normalized_es, 4),
                p_value=p_value,
                fdr_q_value=0.0,
                leading_edge_genes=leading_edge,
                is_significant=False
            ))
        
        pathway_results.sort(key=lambda x: x.p_value)
        
        n_tests = len(pathway_results)
        for i, result in enumerate(pathway_results):
            result.fdr_q_value = min(1.0, result.p_value * n_tests / (i + 1))
            result.is_significant = result.fdr_q_value < fdr_threshold
        
        enriched_categories = {}
        for result in pathway_results:
            if result.is_significant:
                source = result.source
                enriched_categories[source] = enriched_categories.get(source, 0) + 1
        
        return GSEAResult(
            analysis_name=f"GSEA_{substance_type or 'general'}",
            substance_type=substance_type or 'general',
            n_cpgs_analyzed=len(background_cpgs),
            n_significant_cpgs=len(significant_cpgs),
            n_pathways_tested=len(pathway_results),
            n_significant_pathways=sum(1 for r in pathway_results if r.is_significant),
            top_pathways=pathway_results[:20],
            enriched_categories=enriched_categories
        )
    
    def get_substance_specific_pathways(self, substance_type: str) -> List[Dict]:
        """Get pathways specifically relevant to a substance type"""
        if substance_type not in self.SUBSTANCE_PATHWAYS:
            return []
        
        relevant_pathways = []
        for pathway_id in self.SUBSTANCE_PATHWAYS[substance_type]:
            if pathway_id in self.PATHWAY_DATABASE:
                pathway_info = self.PATHWAY_DATABASE[pathway_id]
                relevant_pathways.append({
                    'pathway_id': pathway_id,
                    'name': pathway_info['name'],
                    'source': pathway_info['source'],
                    'genes': pathway_info['genes'],
                    'n_genes': len(pathway_info['genes'])
                })
        
        return relevant_pathways
    
    def simulate_gsea_results(self, 
                               substance_type: str,
                               n_significant: int = 50) -> GSEAResult:
        """
        Simulate GSEA results for demonstration.
        Uses substance-specific pathway prioritization.
        """
        np.random.seed(42 + hash(substance_type) % 100)
        
        all_cpgs = [f"cg{str(i).zfill(8)}" for i in range(1000)]
        sig_cpgs = np.random.choice(all_cpgs, n_significant, replace=False).tolist()
        
        result = self.perform_enrichment(sig_cpgs, all_cpgs, substance_type)
        
        if substance_type in self.SUBSTANCE_PATHWAYS:
            for pathway_result in result.top_pathways:
                if pathway_result.pathway_id in self.SUBSTANCE_PATHWAYS[substance_type]:
                    pathway_result.p_value = np.random.uniform(0.0001, 0.01)
                    pathway_result.fdr_q_value = pathway_result.p_value * 3
                    pathway_result.is_significant = True
                    pathway_result.enrichment_score = np.random.uniform(1.5, 3.0)
                    pathway_result.normalized_es = np.random.uniform(2.0, 4.0)
        
        result.top_pathways.sort(key=lambda x: x.p_value)
        result.n_significant_pathways = sum(1 for r in result.top_pathways if r.is_significant)
        
        return result
    
    def plot_enrichment_barplot(self, gsea_result: GSEAResult, top_n: int = 15) -> go.Figure:
        """Create bar plot of top enriched pathways"""
        top_pathways = gsea_result.top_pathways[:top_n]
        
        pathway_names = [p.pathway_name[:40] + '...' if len(p.pathway_name) > 40 else p.pathway_name 
                        for p in top_pathways]
        enrichment_scores = [p.normalized_es for p in top_pathways]
        p_values = [p.p_value for p in top_pathways]
        sources = [p.source for p in top_pathways]
        
        source_colors = {
            'GO_BP': '#1f77b4',
            'KEGG': '#ff7f0e',
            'REACTOME': '#2ca02c'
        }
        colors = [source_colors.get(s, '#888888') for s in sources]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=pathway_names[::-1],
            x=enrichment_scores[::-1],
            orientation='h',
            marker=dict(color=colors[::-1]),
            text=[f"p={p:.2e}" for p in p_values[::-1]],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>" +
                         "NES: %{x:.2f}<br>" +
                         "<extra></extra>"
        ))
        
        fig.update_layout(
            title=dict(
                text=f'Top {top_n} Enriched Pathways - {gsea_result.substance_type}',
                x=0.5,
                font=dict(size=14)
            ),
            xaxis_title='Normalized Enrichment Score (NES)',
            yaxis_title='',
            template='plotly_white',
            height=max(400, top_n * 30),
            margin=dict(l=250)
        )
        
        return fig
    
    def plot_enrichment_dotplot(self, gsea_result: GSEAResult, top_n: int = 15) -> go.Figure:
        """Create dot plot of enrichment results"""
        top_pathways = gsea_result.top_pathways[:top_n]
        
        pathway_names = [p.pathway_name[:35] + '...' if len(p.pathway_name) > 35 else p.pathway_name 
                        for p in top_pathways]
        enrichment_scores = [p.normalized_es for p in top_pathways]
        p_values = [-np.log10(p.p_value + 1e-10) for p in top_pathways]
        gene_counts = [p.n_significant_genes for p in top_pathways]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=enrichment_scores,
            y=pathway_names[::-1],
            mode='markers',
            marker=dict(
                size=[g * 5 + 10 for g in gene_counts[::-1]],
                color=p_values[::-1],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='-log10(p)')
            ),
            text=[f"Genes: {g}" for g in gene_counts[::-1]],
            hovertemplate="<b>%{y}</b><br>" +
                         "NES: %{x:.2f}<br>" +
                         "%{text}<extra></extra>"
        ))
        
        fig.update_layout(
            title=dict(text='Pathway Enrichment Dot Plot', x=0.5),
            xaxis_title='Normalized Enrichment Score',
            yaxis_title='',
            template='plotly_white',
            height=max(400, top_n * 30),
            margin=dict(l=250)
        )
        
        return fig
    
    def plot_pathway_network(self, gsea_result: GSEAResult, top_n: int = 10) -> go.Figure:
        """Create network visualization of pathway relationships"""
        top_pathways = gsea_result.top_pathways[:top_n]
        
        pathway_genes = {}
        for p in top_pathways:
            pathway_genes[p.pathway_name] = set(p.leading_edge_genes)
        
        n_pathways = len(top_pathways)
        angles = np.linspace(0, 2 * np.pi, n_pathways, endpoint=False)
        radius = 5
        
        x_positions = radius * np.cos(angles)
        y_positions = radius * np.sin(angles)
        
        fig = go.Figure()
        
        pathway_names = list(pathway_genes.keys())
        for i, p1 in enumerate(pathway_names):
            for j, p2 in enumerate(pathway_names):
                if i < j:
                    overlap = len(pathway_genes[p1] & pathway_genes[p2])
                    if overlap > 0:
                        fig.add_trace(go.Scatter(
                            x=[x_positions[i], x_positions[j]],
                            y=[y_positions[i], y_positions[j]],
                            mode='lines',
                            line=dict(width=overlap, color='lightgray'),
                            hoverinfo='skip',
                            showlegend=False
                        ))
        
        sizes = [p.n_significant_genes * 10 + 20 for p in top_pathways]
        colors = [-np.log10(p.p_value + 1e-10) for p in top_pathways]
        
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_positions,
            mode='markers+text',
            marker=dict(
                size=sizes,
                color=colors,
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title='-log10(p)')
            ),
            text=[p.pathway_name[:20] for p in top_pathways],
            textposition='top center',
            hovertemplate="<b>%{text}</b><br>" +
                         "p-value: %{customdata:.2e}<extra></extra>",
            customdata=[p.p_value for p in top_pathways],
            showlegend=False
        ))
        
        fig.update_layout(
            title=dict(text='Pathway Relationship Network', x=0.5),
            template='plotly_white',
            height=600,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False
        )
        
        return fig
    
    def generate_gsea_report(self, gsea_result: GSEAResult) -> Dict:
        """Generate comprehensive GSEA report"""
        return {
            'analysis_summary': {
                'substance_type': gsea_result.substance_type,
                'cpgs_analyzed': gsea_result.n_cpgs_analyzed,
                'significant_cpgs': gsea_result.n_significant_cpgs,
                'pathways_tested': gsea_result.n_pathways_tested,
                'significant_pathways': gsea_result.n_significant_pathways
            },
            'top_pathways': [
                {
                    'id': p.pathway_id,
                    'name': p.pathway_name,
                    'source': p.source,
                    'enrichment_score': p.normalized_es,
                    'p_value': p.p_value,
                    'fdr': p.fdr_q_value,
                    'genes': p.leading_edge_genes
                }
                for p in gsea_result.top_pathways[:10]
            ],
            'enriched_categories': gsea_result.enriched_categories,
            'interpretation': self._generate_interpretation(gsea_result)
        }
    
    def _generate_interpretation(self, gsea_result: GSEAResult) -> str:
        """Generate text interpretation of GSEA results"""
        n_sig = gsea_result.n_significant_pathways
        substance = gsea_result.substance_type
        
        if n_sig == 0:
            return "Anlamlı zenginleşme gösteren pathway tespit edilmedi."
        
        top_pathway = gsea_result.top_pathways[0] if gsea_result.top_pathways else None
        
        interpretation = f"{substance.title()} kullanımı ile ilişkili diferansiyel metilasyon analizi sonucunda " \
                        f"{n_sig} pathway anlamlı zenginleşme göstermiştir. "
        
        if top_pathway:
            interpretation += f"En anlamlı pathway '{top_pathway.pathway_name}' " \
                            f"(NES={top_pathway.normalized_es:.2f}, FDR={top_pathway.fdr_q_value:.4f}) olarak belirlenmiştir. "
        
        aging_related = ['Aging', 'Longevity', 'DNA Repair', 'Oxidative Stress']
        aging_pathways = [p for p in gsea_result.top_pathways if any(a in p.pathway_name for a in aging_related)]
        
        if aging_pathways:
            interpretation += f"Yaşlanma ile ilişkili {len(aging_pathways)} pathway anlamlı zenginleşme göstermiştir, " \
                            "bu da madde kullanımının biyolojik yaşlanma mekanizmaları üzerindeki etkisini desteklemektedir."
        
        return interpretation
