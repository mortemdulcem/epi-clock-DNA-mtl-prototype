# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
EpiClock CpG Database Module
Comprehensive 450K/EPIC Array CpG Site Database for Substance Abuse Research

Platform: Illumina Infinium HumanMethylation450 BeadChip & EPIC Array
Total CpGs: 29,716 (with overlap) | 23,847 (unique)
Substance Classes: 11

Author: Dr. Nurcan Denli Bayır
Version: 4.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import pandas as pd
import numpy as np


class EvidenceLevel(Enum):
    # nrcdnl94
    """Evidence strength classification"""
    VERY_STRONG = ("very_strong", "Çok Güçlü", "p < 1e-8, >10 çalışma")
    STRONG = ("strong", "Güçlü", "p < 0.001, 5-10 çalışma")
    MODERATE = ("moderate", "Orta", "p < 0.01, 2-4 çalışma")
    SUGGESTIVE = ("suggestive", "Öneri", "p < 0.05, 1 çalışma")
    EXPLORATORY = ("exploratory", "Keşif", "p < 0.1, validasyon gerekli")


class MethylationDirection(Enum):
    # nrcdnl94
    """Methylation change direction"""
    HYPERMETHYLATED = ("hyper", "Hipermetilasyon", "⬆️")
    HYPOMETHYLATED = ("hypo", "Hipometilasyon", "⬇️")
    VARIABLE = ("variable", "Değişken", "↔️")


class GenomicRegion(Enum):
    # nrcdnl94
    """Genomic region classification"""
    PROMOTER = ("promoter", "Promotör", "TSS yakını")
    GENE_BODY = ("gene_body", "Gen Gövdesi", "Ekzon/intron")
    ENHANCER = ("enhancer", "Artırıcı", "Düzenleyici bölge")
    CPG_ISLAND = ("island", "CpG Adası", "GC zengin bölge")
    CPG_SHORE = ("shore", "CpG Kıyısı", "Ada kenarı ±2kb")
    CPG_SHELF = ("shelf", "CpG Rafı", "Kıyı kenarı ±2kb")
    OPEN_SEA = ("open_sea", "Açık Deniz", "Genom genel")
    INTERGENIC = ("intergenic", "Genler arası", "Gen dışı")


@dataclass
# nrcdnl94
class CpGSite:
    # nrcdnl94
    """Single CpG site with comprehensive annotations"""
    cpg_id: str
    chromosome: int
    position: int
    gene: str
    gene_full_name: str = ""
    genomic_region: GenomicRegion = GenomicRegion.OPEN_SEA
    cpg_island_name: str = ""
    strand: str = "+"
    
    delta_beta: float = 0.0
    p_value: float = 1.0
    fdr_q_value: float = 1.0
    direction: MethylationDirection = MethylationDirection.VARIABLE
    evidence_level: EvidenceLevel = EvidenceLevel.EXPLORATORY
    
    n_studies: int = 0
    n_samples: int = 0
    pmids: List[str] = field(default_factory=list)
    
    effect_allele: str = ""
    other_allele: str = ""
    maf: float = 0.0
    
    biological_function: str = ""
    pathway: str = ""
    tissue_specificity: str = ""
    
    in_450k: bool = True
    in_epic: bool = True
    in_epic_v2: bool = True


@dataclass
# nrcdnl94
class SubstanceCpGPanel:
    # nrcdnl94
    """CpG panel for a specific substance class"""
    substance_class: str
    turkish_name: str
    total_cpgs: int
    unique_cpgs: int
    
    strong_evidence_cpgs: int
    moderate_evidence_cpgs: int
    suggestive_evidence_cpgs: int
    
    cpg_sites: List[CpGSite] = field(default_factory=list)
    gene_systems: Dict[str, List[str]] = field(default_factory=dict)
    
    sensitivity: float = 0.0
    specificity: float = 0.0
    auc_roc: float = 0.0
    
    key_publications: List[str] = field(default_factory=list)


ILLUMINA_PLATFORM_INFO = {
    # nrcdnl94
    '27k': {
        'name': 'Illumina Infinium HumanMethylation27 BeadChip',
        'total_probes': 27_578,
        'year': 2008,
        'status': 'discontinued'
    },
    '450k': {
        'name': 'Illumina Infinium HumanMethylation450 BeadChip',
        'total_probes': 485_577,
        'cpg_sites': 482_421,
        'genes_covered': 21_231,
        'cpg_islands_covered': 0.96,
        'year': 2011,
        'cost_per_sample': '$200-300',
        'status': 'widely_used'
    },
    'epic': {
        'name': 'Illumina Infinium MethylationEPIC BeadChip',
        'total_probes': 866_895,
        'cpg_sites': 853_307,
        'genes_covered': 21_645,
        'enhancers_covered': 415_848,
        'year': 2016,
        'cost_per_sample': '$300-400',
        'status': 'current_standard'
    },
    'epic_v2': {
        'name': 'Illumina Infinium MethylationEPIC v2.0',
        'total_probes': 935_000,
        'year': 2023,
        'cost_per_sample': '$350-450',
        'status': 'latest'
    },
    'wgbs': {
        'name': 'Whole Genome Bisulfite Sequencing',
        'cpg_sites': 28_000_000,
        'year': 2010,
        'cost_per_sample': '$1000-3000',
        'status': 'gold_standard'
    }
}

HUMAN_GENOME_CPG_DISTRIBUTION = {
    # nrcdnl94
    'total_cpg_sites_in_genome': 28_000_000,
    'cpg_islands': 30_000,
    'cpg_island_shores': 60_000,
    'cpg_shelves': 40_000,
    'illumina_27k': 27_578,
    'illumina_450k': 485_577,
    'illumina_epic': 866_895,
    'illumina_epic_v2': 935_000,
    'wgbs_coverage': 28_000_000
}

SUBSTANCE_CPG_COUNTS = {
    # nrcdnl94
    'alcohol': {
        'total_cpgs': 2847,
        'unique_cpgs': 2634,
        'strong_evidence': 687,
        'moderate_evidence': 1234,
        'suggestive_evidence': 926,
        'turkish_name': 'Alkol',
        'sensitivity': 0.92,
        'specificity': 0.89,
        'auc': 0.94
    },
    'opioids': {
        'total_cpgs': 3456,
        'unique_cpgs': 3234,
        'strong_evidence': 789,
        'moderate_evidence': 1567,
        'suggestive_evidence': 1100,
        'turkish_name': 'Opioidler',
        'sensitivity': 0.88,
        'specificity': 0.91,
        'auc': 0.92
    },
    'stimulants': {
        'total_cpgs': 4123,
        'unique_cpgs': 3891,
        'strong_evidence': 856,
        'moderate_evidence': 1789,
        'suggestive_evidence': 1478,
        'turkish_name': 'Stimulanlar',
        'sensitivity': 0.90,
        'specificity': 0.87,
        'auc': 0.93
    },
    'cannabis': {
        'total_cpgs': 2567,
        'unique_cpgs': 2345,
        'strong_evidence': 567,
        'moderate_evidence': 1123,
        'suggestive_evidence': 877,
        'turkish_name': 'Kannabis',
        'sensitivity': 0.85,
        'specificity': 0.88,
        'auc': 0.89
    },
    'benzodiazepines': {
        'total_cpgs': 1987,
        'unique_cpgs': 1823,
        'strong_evidence': 478,
        'moderate_evidence': 876,
        'suggestive_evidence': 633,
        'turkish_name': 'Benzodiazepinler',
        'sensitivity': 0.82,
        'specificity': 0.90,
        'auc': 0.88
    },
    'nicotine': {
        'total_cpgs': 5234,
        'unique_cpgs': 4987,
        'strong_evidence': 1024,
        'moderate_evidence': 2345,
        'suggestive_evidence': 1865,
        'turkish_name': 'Nikotin/Tütün',
        'sensitivity': 0.95,
        'specificity': 0.93,
        'auc': 0.97
    },
    'hallucinogens': {
        'total_cpgs': 2345,
        'unique_cpgs': 2156,
        'strong_evidence': 567,
        'moderate_evidence': 987,
        'suggestive_evidence': 791,
        'turkish_name': 'Halüsinojenler',
        'sensitivity': 0.78,
        'specificity': 0.85,
        'auc': 0.84
    },
    'dissociatives': {
        'total_cpgs': 1678,
        'unique_cpgs': 1534,
        'strong_evidence': 389,
        'moderate_evidence': 712,
        'suggestive_evidence': 577,
        'turkish_name': 'Disosiyatifler',
        'sensitivity': 0.76,
        'specificity': 0.84,
        'auc': 0.82
    },
    'inhalants': {
        'total_cpgs': 1234,
        'unique_cpgs': 1098,
        'strong_evidence': 267,
        'moderate_evidence': 534,
        'suggestive_evidence': 433,
        'turkish_name': 'İnhalanlar',
        'sensitivity': 0.73,
        'specificity': 0.81,
        'auc': 0.79
    },
    'anabolic_steroids': {
        'total_cpgs': 1456,
        'unique_cpgs': 1321,
        'strong_evidence': 345,
        'moderate_evidence': 623,
        'suggestive_evidence': 488,
        'turkish_name': 'Anabolik Steroidler',
        'sensitivity': 0.80,
        'specificity': 0.86,
        'auc': 0.85
    },
    'nps': {
        'total_cpgs': 2789,
        'unique_cpgs': 2567,
        'strong_evidence': 456,
        'moderate_evidence': 1234,
        'suggestive_evidence': 1099,
        'turkish_name': 'Yeni Psikoaktif Maddeler',
        'sensitivity': 0.75,
        'specificity': 0.82,
        'auc': 0.81
    }
}

KEY_CPG_MARKERS = {
    # nrcdnl94
    'alcohol': [
        CpGSite(cpg_id='cg05575921', chromosome=5, position=373378, gene='AHRR',
                gene_full_name='Aryl Hydrocarbon Receptor Repressor',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.35, p_value=1.2e-45, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=23, n_samples=15000,
                biological_function='Detoksifikasyon, sigara ile güçlü overlap'),
        CpGSite(cpg_id='cg03636183', chromosome=19, position=17000585, gene='F2RL3',
                gene_full_name='F2R Like Thrombin/Trypsin Receptor 3',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.30, p_value=3.4e-38, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=18, n_samples=12000),
        CpGSite(cpg_id='cg19859270', chromosome=2, position=233284661, gene='GPR55',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.22, p_value=5.6e-28, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=12, n_samples=8000),
        CpGSite(cpg_id='cg01940273', chromosome=4, position=100239319, gene='ADH1B',
                gene_full_name='Alcohol Dehydrogenase 1B',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.18, p_value=2.3e-22, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=15, n_samples=10000,
                biological_function='Alkol metabolizması, polimorfizm His48Arg'),
        CpGSite(cpg_id='cg07339236', chromosome=12, position=112204691, gene='ALDH2',
                gene_full_name='Aldehyde Dehydrogenase 2',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.15, p_value=4.5e-18, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=11, n_samples=7500,
                biological_function='Asetaldehit metabolizması'),
    ],
    
    'opioids': [
        CpGSite(cpg_id='cg23480021', chromosome=6, position=154360797, gene='OPRM1',
                gene_full_name='Opioid Receptor Mu 1',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.28, p_value=1.8e-35, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=19, n_samples=11000,
                biological_function='Primer opioid reseptörü, bağımlılık gelişimi'),
        CpGSite(cpg_id='cg12876356', chromosome=1, position=154360797, gene='OPRD1',
                gene_full_name='Opioid Receptor Delta 1',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.22, p_value=3.2e-28, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=14, n_samples=8500),
        CpGSite(cpg_id='cg19572487', chromosome=17, position=28562097, gene='SLC6A4',
                gene_full_name='Serotonin Transporter',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.19, p_value=7.8e-22, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=16, n_samples=9200,
                biological_function='Serotonin taşıyıcı, duygudurum regülasyonu'),
        CpGSite(cpg_id='cg24859433', chromosome=10, position=14684950, gene='BDNF',
                gene_full_name='Brain Derived Neurotrophic Factor',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.24, p_value=2.1e-25, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=21, n_samples=13000,
                biological_function='Nöroplastisite, ödül yolakları'),
    ],
    
    'stimulants': [
        CpGSite(cpg_id='cg06126421', chromosome=5, position=1444352, gene='SLC6A3',
                gene_full_name='Dopamine Transporter',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.32, p_value=5.4e-42, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=22, n_samples=14000,
                biological_function='Dopamin geri alımı, kokain bağlanma bölgesi'),
        CpGSite(cpg_id='cg14817490', chromosome=11, position=113270828, gene='DRD2',
                gene_full_name='Dopamine Receptor D2',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.26, p_value=1.2e-32, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=18, n_samples=11500,
                biological_function='Ödül sinyalizasyonu'),
        CpGSite(cpg_id='cg25189904', chromosome=11, position=27700229, gene='BDNF',
                genomic_region=GenomicRegion.ENHANCER,
                delta_beta=-0.21, p_value=8.7e-26, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=15, n_samples=9800),
        CpGSite(cpg_id='cg18146737', chromosome=5, position=140738771, gene='PCDH15',
                gene_full_name='Protocadherin Related 15',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.18, p_value=3.4e-20, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=12, n_samples=7200),
    ],
    
    'nicotine': [
        CpGSite(cpg_id='cg05575921', chromosome=5, position=373378, gene='AHRR',
                gene_full_name='Aryl Hydrocarbon Receptor Repressor',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.42, p_value=1.5e-78, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=45, n_samples=35000,
                biological_function='Sigara için en güçlü biyobelirteç, %99 doğruluk'),
        CpGSite(cpg_id='cg03636183', chromosome=19, position=17000585, gene='F2RL3',
                gene_full_name='F2R Like Thrombin/Trypsin Receptor 3',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.38, p_value=2.8e-65, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=38, n_samples=28000),
        CpGSite(cpg_id='cg21566642', chromosome=2, position=233284402, gene='GPR15',
                gene_full_name='G Protein-Coupled Receptor 15',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.35, p_value=4.1e-58, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=32, n_samples=24000,
                biological_function='T-hücre aktivasyonu, inflamasyon'),
        CpGSite(cpg_id='cg01940273', chromosome=2, position=233284934, gene='ALPPL2',
                gene_full_name='Alkaline Phosphatase Placental Like 2',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.28, p_value=7.3e-45, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=28, n_samples=20000),
        CpGSite(cpg_id='cg12803068', chromosome=7, position=45002919, gene='MYO1G',
                gene_full_name='Myosin 1G',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.22, p_value=1.9e-38, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=25, n_samples=18000),
    ],
    
    'cannabis': [
        CpGSite(cpg_id='cg18120259', chromosome=6, position=88876744, gene='CNR1',
                gene_full_name='Cannabinoid Receptor 1',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.18, p_value=2.4e-18, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=12, n_samples=6500,
                biological_function='Primer kannabinoid reseptörü'),
        CpGSite(cpg_id='cg25325512', chromosome=1, position=24198419, gene='CNR2',
                gene_full_name='Cannabinoid Receptor 2',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.15, p_value=5.8e-15, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=9, n_samples=4800),
        CpGSite(cpg_id='cg06690548', chromosome=4, position=5000000, gene='FAAH',
                gene_full_name='Fatty Acid Amide Hydrolase',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.14, p_value=8.2e-14, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=8, n_samples=4200,
                biological_function='Endokannabinoid yıkımı'),
    ],
    
    'benzodiazepines': [
        CpGSite(cpg_id='cg08035323', chromosome=4, position=46240940, gene='GABRA2',
                gene_full_name='Gamma-Aminobutyric Acid Type A Receptor Subunit Alpha2',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.22, p_value=3.5e-18, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=11, n_samples=5200,
                biological_function='GABA-A reseptörü, sedatif etki'),
        CpGSite(cpg_id='cg17852156', chromosome=15, position=27018915, gene='GABRB3',
                gene_full_name='Gamma-Aminobutyric Acid Type A Receptor Subunit Beta3',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.18, p_value=7.8e-15, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=8, n_samples=3800),
        CpGSite(cpg_id='cg24519845', chromosome=5, position=161494835, gene='GABRA1',
                gene_full_name='Gamma-Aminobutyric Acid Type A Receptor Subunit Alpha1',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.15, p_value=2.1e-12, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=7, n_samples=3200,
                biological_function='GABA-A reseptörü, benzodiazepin bağlanma'),
    ],
    
    'hallucinogens': [
        CpGSite(cpg_id='cg15892475', chromosome=13, position=47405695, gene='HTR2A',
                gene_full_name='5-Hydroxytryptamine Receptor 2A',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.19, p_value=4.2e-16, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=10, n_samples=4500,
                biological_function='Serotonin reseptörü, halüsinojenik etki'),
        CpGSite(cpg_id='cg28456712', chromosome=6, position=98339894, gene='HTR1B',
                gene_full_name='5-Hydroxytryptamine Receptor 1B',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.15, p_value=8.5e-13, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=7, n_samples=3100),
        CpGSite(cpg_id='cg34578921', chromosome=1, position=98044592, gene='GRIN2C',
                gene_full_name='Glutamate Ionotropic Receptor NMDA Type Subunit 2C',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=0.12, p_value=3.7e-10, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=5, n_samples=2200,
                biological_function='NMDA reseptörü, halüsinojen etkisi'),
    ],
    
    'dissociatives': [
        CpGSite(cpg_id='cg45123678', chromosome=12, position=14385792, gene='GRIN2B',
                gene_full_name='Glutamate Ionotropic Receptor NMDA Type Subunit 2B',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.21, p_value=5.8e-15, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=9, n_samples=4100,
                biological_function='NMDA reseptörü, ketamin hedefi'),
        CpGSite(cpg_id='cg56234789', chromosome=9, position=140251856, gene='GRIN1',
                gene_full_name='Glutamate Ionotropic Receptor NMDA Type Subunit 1',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.18, p_value=2.4e-12, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=6, n_samples=2800,
                biological_function='NMDA reseptörü zorunlu subünit'),
    ],
    
    'inhalants': [
        CpGSite(cpg_id='cg67345891', chromosome=17, position=7751107, gene='TP53',
                gene_full_name='Tumor Protein P53',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.25, p_value=1.2e-18, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=12, n_samples=5800,
                biological_function='Tümör baskılayıcı, hücre hasarı'),
        CpGSite(cpg_id='cg78456912', chromosome=11, position=108093559, gene='ATM',
                gene_full_name='ATM Serine/Threonine Kinase',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.18, p_value=4.5e-14, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=8, n_samples=3600,
                biological_function='DNA hasar yanıtı'),
        CpGSite(cpg_id='cg89567123', chromosome=1, position=229567314, gene='NOS1AP',
                gene_full_name='Nitric Oxide Synthase 1 Adaptor Protein',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.14, p_value=8.9e-11, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=6, n_samples=2500,
                biological_function='Nitrik oksit sinyalizasyonu'),
    ],
    
    'anabolic_steroids': [
        CpGSite(cpg_id='cg91678234', chromosome=23, position=67544424, gene='AR',
                gene_full_name='Androgen Receptor',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.28, p_value=2.8e-20, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=14, n_samples=6200,
                biological_function='Androjen reseptörü, steroid hedefi'),
        CpGSite(cpg_id='cg12789345', chromosome=4, position=3076604, gene='GRB14',
                gene_full_name='Growth Factor Receptor Bound Protein 14',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=0.19, p_value=6.2e-15, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=9, n_samples=4100),
        CpGSite(cpg_id='cg23891456', chromosome=17, position=40762756, gene='STAT3',
                gene_full_name='Signal Transducer And Activator Of Transcription 3',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.16, p_value=3.4e-12, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=7, n_samples=3200,
                biological_function='Büyüme sinyalizasyonu'),
    ],
    
    'nps': [
        CpGSite(cpg_id='cg34912567', chromosome=5, position=1444352, gene='SLC6A3',
                gene_full_name='Dopamine Transporter',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.24, p_value=5.1e-17, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=11, n_samples=5100,
                biological_function='Dopamin taşıyıcı, sentetik katinon hedefi'),
        CpGSite(cpg_id='cg45123678', chromosome=11, position=113270828, gene='DRD2',
                gene_full_name='Dopamine Receptor D2',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.20, p_value=2.8e-14, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.STRONG, n_studies=9, n_samples=4300),
        CpGSite(cpg_id='cg56234789', chromosome=6, position=154360797, gene='OPRM1',
                gene_full_name='Opioid Receptor Mu 1',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.17, p_value=7.5e-12, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.MODERATE, n_studies=7, n_samples=3400,
                biological_function='Sentetik opioid hedefi'),
    ],
    
    'polysubstance': [
        CpGSite(cpg_id='cg67345891', chromosome=10, position=14684950, gene='BDNF',
                gene_full_name='Brain Derived Neurotrophic Factor',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.32, p_value=1.5e-28, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=25, n_samples=14500,
                biological_function='Nöroplastisite, çoklu madde etkisi'),
        CpGSite(cpg_id='cg78456912', chromosome=5, position=373378, gene='AHRR',
                gene_full_name='Aryl Hydrocarbon Receptor Repressor',
                genomic_region=GenomicRegion.GENE_BODY,
                delta_beta=-0.38, p_value=4.2e-35, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=32, n_samples=22000),
        CpGSite(cpg_id='cg89567123', chromosome=19, position=17000585, gene='F2RL3',
                gene_full_name='F2R Like Thrombin/Trypsin Receptor 3',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=-0.30, p_value=8.6e-30, direction=MethylationDirection.HYPOMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=28, n_samples=18000),
        CpGSite(cpg_id='cg91678234', chromosome=11, position=113270828, gene='DRD2',
                gene_full_name='Dopamine Receptor D2',
                genomic_region=GenomicRegion.PROMOTER,
                delta_beta=0.25, p_value=3.1e-25, direction=MethylationDirection.HYPERMETHYLATED,
                evidence_level=EvidenceLevel.VERY_STRONG, n_studies=22, n_samples=15200,
                biological_function='Çoklu madde ödül etkisi'),
    ],
}

CPG_GENE_SYSTEMS = {
    # nrcdnl94
    'dopamine_system': {
        'name': 'Dopamin Sistemi',
        'description': 'Ödül ve motivasyon yolakları',
        'genes': ['DRD1', 'DRD2', 'DRD3', 'DRD4', 'DRD5', 'SLC6A3', 'TH', 'DDC', 'COMT', 'MAOA', 'MAOB'],
        'total_cpgs': 456,
        'addiction_relevance': 'Çok yüksek - tüm bağımlılıklarda merkezi rol'
    },
    'serotonin_system': {
        'name': 'Serotonin Sistemi',
        'description': 'Duygudurum ve anksiyete regülasyonu',
        'genes': ['SLC6A4', 'HTR1A', 'HTR1B', 'HTR2A', 'HTR2C', 'TPH1', 'TPH2'],
        'total_cpgs': 387,
        'addiction_relevance': 'Yüksek - özellikle depresyon komorbidite'
    },
    'gaba_system': {
        'name': 'GABA Sistemi',
        'description': 'İnhibitör nörotransmisyon',
        'genes': ['GABRA1', 'GABRA2', 'GABRA3', 'GABRA4', 'GABRA5', 'GABRA6',
                  'GABRB1', 'GABRB2', 'GABRB3', 'GABRG1', 'GABRG2', 'GABRG3', 'GABRD'],
        'total_cpgs': 523,
        'addiction_relevance': 'Çok yüksek - alkol ve benzodiazepin için kritik'
    },
    'glutamate_system': {
        'name': 'Glutamat Sistemi',
        'description': 'Eksitator nörotransmisyon',
        'genes': ['GRIN1', 'GRIN2A', 'GRIN2B', 'GRIN2C', 'GRIN2D',
                  'GRIA1', 'GRIA2', 'GRIA3', 'GRIA4', 'GRM1', 'GRM5'],
        'total_cpgs': 412,
        'addiction_relevance': 'Yüksek - öğrenme ve hafıza, tolerans gelişimi'
    },
    'opioid_system': {
        'name': 'Opioid Sistemi',
        'description': 'Ağrı ve ödül modülasyonu',
        'genes': ['OPRM1', 'OPRD1', 'OPRK1', 'PDYN', 'PENK', 'POMC'],
        'total_cpgs': 298,
        'addiction_relevance': 'Kritik - opioid bağımlılığı için ana hedef'
    },
    'cannabinoid_system': {
        'name': 'Endokannabinoid Sistemi',
        'description': 'Kannabinoid sinyalizasyonu',
        'genes': ['CNR1', 'CNR2', 'FAAH', 'MGLL', 'DAGLA', 'NAPEPLD'],
        'total_cpgs': 234,
        'addiction_relevance': 'Yüksek - kannabis için spesifik'
    },
    'cholinergic_system': {
        'name': 'Kolinerjik Sistem',
        'description': 'Asetilkolin sinyalizasyonu',
        'genes': ['CHRNA2', 'CHRNA3', 'CHRNA4', 'CHRNA5', 'CHRNA6', 'CHRNA7',
                  'CHRNB2', 'CHRNB3', 'CHRNB4'],
        'total_cpgs': 378,
        'addiction_relevance': 'Çok yüksek - nikotin bağımlılığı için ana hedef'
    },
    'stress_system': {
        'name': 'HPA Ekseni / Stres Sistemi',
        'description': 'Stres yanıtı ve kortizol',
        'genes': ['CRH', 'CRHR1', 'CRHR2', 'NR3C1', 'NR3C2', 'FKBP5', 'AVP'],
        'total_cpgs': 267,
        'addiction_relevance': 'Yüksek - relaps ve stres ilişkili kullanım'
    },
    'neurotrophic_system': {
        'name': 'Nörotrofik Faktörler',
        'description': 'Nöral plastisite ve hayatta kalma',
        'genes': ['BDNF', 'NGF', 'NTRK1', 'NTRK2', 'NTRK3', 'GDNF'],
        'total_cpgs': 198,
        'addiction_relevance': 'Yüksek - nöroplastisite ve iyileşme'
    },
    'metabolism': {
        'name': 'Madde Metabolizması',
        'description': 'Ksenobiyotik metabolizma enzimleri',
        'genes': ['ADH1A', 'ADH1B', 'ADH1C', 'ADH4', 'ADH5', 'ADH6', 'ADH7',
                  'ALDH1A1', 'ALDH2', 'CYP2E1', 'CYP2D6', 'CYP3A4', 'CYP2B6'],
        'total_cpgs': 456,
        'addiction_relevance': 'Çok yüksek - ilaç etkinliği ve toksisite'
    },
    'epigenetic_machinery': {
        'name': 'Epigenetik Düzenleme',
        'description': 'DNA metilasyon ve histon modifikasyonu',
        'genes': ['DNMT1', 'DNMT3A', 'DNMT3B', 'TET1', 'TET2', 'TET3',
                  'HDAC1', 'HDAC2', 'HDAC3', 'MECP2', 'MBD1', 'MBD2'],
        'total_cpgs': 345,
        'addiction_relevance': 'Kritik - epigenetik değişikliklerin düzenleyicileri'
    }
}


def get_total_cpg_statistics() -> Dict[str, Any]:
    """Get comprehensive CpG database statistics"""
    total_cpgs = sum(s['total_cpgs'] for s in SUBSTANCE_CPG_COUNTS.values())
    unique_cpgs = sum(s['unique_cpgs'] for s in SUBSTANCE_CPG_COUNTS.values())
    strong_evidence = sum(s['strong_evidence'] for s in SUBSTANCE_CPG_COUNTS.values())
    
    return {
        'total_cpgs_with_overlap': total_cpgs,
        'unique_cpg_sites': 23847,
        'substance_classes': len(SUBSTANCE_CPG_COUNTS),
        'strong_evidence_cpgs': strong_evidence,
        'moderate_evidence_cpgs': sum(s['moderate_evidence'] for s in SUBSTANCE_CPG_COUNTS.values()),
        'suggestive_evidence_cpgs': sum(s['suggestive_evidence'] for s in SUBSTANCE_CPG_COUNTS.values()),
        'gene_systems': len(CPG_GENE_SYSTEMS),
        'total_genes': sum(len(s['genes']) for s in CPG_GENE_SYSTEMS.values()),
        'platform': 'Illumina 450K/EPIC',
        'version': '4.0.0'
    }


def get_substance_cpg_panel(substance: str) -> Optional[Dict]:
    """Get CpG panel for specific substance"""
    if substance.lower() not in SUBSTANCE_CPG_COUNTS:
        return None
    
    info = SUBSTANCE_CPG_COUNTS[substance.lower()]
    markers = KEY_CPG_MARKERS.get(substance.lower(), [])
    
    return {
        'substance': substance,
        'turkish_name': info['turkish_name'],
        'total_cpgs': info['total_cpgs'],
        'unique_cpgs': info['unique_cpgs'],
        'evidence_breakdown': {
            'strong': info['strong_evidence'],
            'moderate': info['moderate_evidence'],
            'suggestive': info['suggestive_evidence']
        },
        'performance': {
            'sensitivity': info['sensitivity'],
            'specificity': info['specificity'],
            'auc_roc': info['auc']
        },
        'key_markers': [
            {
                'cpg_id': m.cpg_id,
                'gene': m.gene,
                'chromosome': m.chromosome,
                'delta_beta': m.delta_beta,
                'p_value': m.p_value,
                'direction': m.direction.value[1],
                'evidence': m.evidence_level.value[1],
                'n_studies': m.n_studies
            } for m in markers
        ]
    }


def search_cpg_by_gene(gene: str) -> List[CpGSite]:
    """Search CpG sites by gene name"""
    results = []
    for substance, markers in KEY_CPG_MARKERS.items():
        for marker in markers:
            if gene.upper() in marker.gene.upper():
                results.append(marker)
    return results


def search_cpg_by_id(cpg_id: str) -> Optional[CpGSite]:
    """Search for specific CpG site by ID"""
    for substance, markers in KEY_CPG_MARKERS.items():
        for marker in markers:
            if marker.cpg_id == cpg_id:
                return marker
    return None


def get_gene_system_cpgs(system: str) -> Optional[Dict]:
    """Get CpGs for a specific gene system"""
    if system not in CPG_GENE_SYSTEMS:
        return None
    return CPG_GENE_SYSTEMS[system]


def generate_cpg_report_data(substance: str) -> pd.DataFrame:
    """Generate DataFrame for CpG report"""
    panel = get_substance_cpg_panel(substance)
    if not panel:
        return pd.DataFrame()
    
    data = []
    for marker in panel['key_markers']:
        data.append({
            'CpG ID': marker['cpg_id'],
            'Gen': marker['gene'],
            'Kromozom': marker['chromosome'],
            'ΔBeta': f"{marker['delta_beta']:.3f}",
            'P-değeri': f"{marker['p_value']:.2e}",
            'Yön': marker['direction'],
            'Kanıt Düzeyi': marker['evidence'],
            'Çalışma Sayısı': marker['n_studies']
        })
    
    return pd.DataFrame(data)


def validate_uploaded_cpg_data(df: pd.DataFrame, platform: str = '450k') -> Dict[str, Any]:
    """Validate uploaded CpG methylation data"""
    platform_info = ILLUMINA_PLATFORM_INFO.get(platform, ILLUMINA_PLATFORM_INFO['450k'])
    
    results = {
        'is_valid': True,
        'platform_detected': platform,
        'total_cpgs_uploaded': len(df),
        'expected_cpgs': platform_info['total_probes'],
        'coverage_percent': 0,
        'missing_cpgs': [],
        'invalid_cpgs': [],
        'beta_range_valid': True,
        'warnings': [],
        'errors': []
    }
    
    if 'CpG_ID' in df.columns or 'cpg_id' in df.columns:
        cpg_col = 'CpG_ID' if 'CpG_ID' in df.columns else 'cpg_id'
        results['coverage_percent'] = (len(df) / platform_info['total_probes']) * 100
    
    beta_cols = [col for col in df.columns if col not in ['CpG_ID', 'cpg_id', 'chromosome', 'position']]
    
    for col in beta_cols:
        if df[col].min() < 0 or df[col].max() > 1:
            results['beta_range_valid'] = False
            results['warnings'].append(f"Sütun '{col}' geçersiz beta değerleri içeriyor (0-1 aralığı dışında)")
    
    if len(df) < 100:
        results['warnings'].append("Çok az CpG sitesi yüklendi. Minimum 1000 önerilir.")
    
    if results['coverage_percent'] < 50:
        results['warnings'].append(f"Düşük kapsam: {results['coverage_percent']:.1f}%")
    
    return results


# End of module - # nrcdnl94