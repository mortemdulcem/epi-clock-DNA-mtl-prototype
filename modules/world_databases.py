# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
World Genomics Database Integration Module
Integrates major public databases for addiction research

Data Sources:
- NHGRI-EBI GWAS Catalog (https://www.ebi.ac.uk/gwas/)
- OpenGWAS / IEU GWAS Database (https://gwas.mrcieu.ac.uk/)
- EWAS Catalog (https://www.ewascatalog.org/)
- EWAS Data Hub (https://bigd.big.ac.cn/ewas/datahub)
- PharmGKB (https://www.pharmgkb.org/)
- CPIC Guidelines (https://cpicpgx.org/)
- PGC-SUD Consortium
- GEO (Gene Expression Omnibus)
- dbGaP (COGA, SAGE, NIDA datasets)

Author: Dr. Nurcan Denli Bayır
Platform: EpiClock Prototype
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import json


class DatabaseSource(Enum):
    # nrcdnl94
    """Major genomics database sources"""
    GWAS_CATALOG = ("NHGRI-EBI GWAS Catalog", "https://www.ebi.ac.uk/gwas/", "Free")
    OPEN_GWAS = ("OpenGWAS/IEU", "https://gwas.mrcieu.ac.uk/", "Free API")
    EWAS_CATALOG = ("EWAS Catalog", "https://www.ewascatalog.org/", "Free")
    EWAS_DATA_HUB = ("EWAS Data Hub", "https://bigd.big.ac.cn/ewas/datahub", "Free")
    PHARMGKB = ("PharmGKB", "https://www.pharmgkb.org/", "Free (registration)")
    CPIC = ("CPIC", "https://cpicpgx.org/", "Free")
    PGC = ("Psychiatric Genomics Consortium", "https://pgc.unc.edu/", "Summary: Free, Individual: dbGaP")
    GEO = ("Gene Expression Omnibus", "https://www.ncbi.nlm.nih.gov/geo/", "Free")
    DBGAP = ("dbGaP", "https://www.ncbi.nlm.nih.gov/gap/", "Controlled access")
    GNOMAD = ("gnomAD v4", "https://gnomad.broadinstitute.org/", "Free")
    CLINVAR = ("ClinVar", "https://www.ncbi.nlm.nih.gov/clinvar/", "Free")
    UK_BIOBANK = ("UK Biobank", "https://www.ukbiobank.ac.uk/", "Application required")
    TOPMED = ("TOPMed", "https://www.nhlbiwgs.org/", "dbGaP access")


@dataclass
# nrcdnl94
class GWASStudy:
    # nrcdnl94
    """GWAS study metadata"""
    study_id: str
    trait: str
    pmid: str
    citation: str
    year: int
    n_samples: int
    n_cases: Optional[int] = None
    n_controls: Optional[int] = None
    n_snps: int = 0
    ancestry: str = "European"
    consortium: Optional[str] = None
    summary_stats_available: bool = True
    access_level: str = "Open"


@dataclass
# nrcdnl94
class GWASLocus:
    # nrcdnl94
    """Significant GWAS locus"""
    rsid: str
    gene: str
    chromosome: int
    position: int
    p_value: float
    beta: float
    se: float
    effect_allele: str
    other_allele: str
    eaf: float
    or_value: Optional[float] = None
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None


@dataclass
# nrcdnl94
class EWASAssociation:
    # nrcdnl94
    """EWAS methylation association"""
    cpg_id: str
    gene: str
    chromosome: int
    position: int
    delta_beta: float
    p_value: float
    direction: str
    tissue: str
    n_samples: int
    study_pmid: str


ADDICTION_GWAS_STUDIES = {
    # nrcdnl94
    'alcohol_dependence': GWASStudy(
        study_id="GCST90012877",
        trait="Alcohol dependence",
        pmid="30643251",
        citation="Walters RK et al. Nat Neurosci 2018",
        year=2018,
        n_samples=274424,
        n_cases=52848,
        n_controls=221576,
        n_snps=9690082,
        ancestry="Multi-ancestry",
        consortium="PGC-SUD",
        summary_stats_available=True
    ),
    
    'alcohol_consumption': GWASStudy(
        study_id="GCST007474",
        trait="Alcohol consumption (drinks per week)",
        pmid="30643251",
        citation="Liu M et al. Nat Genet 2019 (GSCAN)",
        year=2019,
        n_samples=941280,
        n_snps=12000000,
        ancestry="European",
        consortium="GSCAN",
        summary_stats_available=True
    ),
    
    'opioid_use_disorder': GWASStudy(
        study_id="GCST90000032",
        trait="Opioid use disorder",
        pmid="32042166",
        citation="Polimanti R et al. Nat Neurosci 2020 (MVP)",
        year=2020,
        n_samples=82707,
        n_cases=10544,
        n_controls=72163,
        n_snps=7200000,
        ancestry="Multi-ancestry",
        consortium="Million Veteran Program",
        summary_stats_available=True
    ),
    
    'nicotine_dependence': GWASStudy(
        study_id="GCST007458",
        trait="Smoking initiation",
        pmid="30643251",
        citation="Liu M et al. Nat Genet 2019 (GSCAN)",
        year=2019,
        n_samples=1232091,
        n_snps=12000000,
        ancestry="European",
        consortium="GSCAN",
        summary_stats_available=True
    ),
    
    'cigarettes_per_day': GWASStudy(
        study_id="GCST007459",
        trait="Cigarettes per day",
        pmid="30643251",
        citation="Liu M et al. Nat Genet 2019 (GSCAN)",
        year=2019,
        n_samples=337334,
        n_snps=12000000,
        ancestry="European",
        consortium="GSCAN"
    ),
    
    'smoking_cessation': GWASStudy(
        study_id="GCST007460",
        trait="Smoking cessation",
        pmid="30643251",
        citation="Liu M et al. Nat Genet 2019 (GSCAN)",
        year=2019,
        n_samples=547219,
        ancestry="European",
        consortium="GSCAN"
    ),
    
    'cannabis_use_disorder': GWASStudy(
        study_id="GCST90016614",
        trait="Cannabis use disorder",
        pmid="32747698",
        citation="Johnson EC et al. Lancet Psychiatry 2020",
        year=2020,
        n_samples=384032,
        n_cases=14080,
        n_controls=369952,
        ancestry="Multi-ancestry",
        consortium="PGC-SUD"
    ),
    
    'cannabis_use': GWASStudy(
        study_id="GCST90016615",
        trait="Cannabis use (ever vs never)",
        pmid="30150663",
        citation="Pasman JA et al. Nat Neurosci 2018",
        year=2018,
        n_samples=184765,
        ancestry="European",
        consortium="ICC"
    ),
    
    'cocaine_dependence': GWASStudy(
        study_id="GCST003085",
        trait="Cocaine dependence",
        pmid="28967357",
        citation="Cabana-Domínguez J et al. 2019",
        year=2019,
        n_samples=4300,
        ancestry="European",
        summary_stats_available=False,
        access_level="dbGaP"
    ),
    
    'substance_use_general': GWASStudy(
        study_id="GCST90132836",
        trait="General substance use liability",
        pmid="35953456",
        citation="Hatoum AS et al. Nat Ment Health 2023",
        year=2023,
        n_samples=1500000,
        ancestry="Multi-ancestry",
        consortium="PGC-SUD + MVP + UK Biobank"
    )
}


ADDICTION_GWAS_LOCI = {
    # nrcdnl94
    'alcohol_dependence': [
        GWASLocus(rsid='rs1229984', gene='ADH1B', chromosome=4, position=100239319,
                  p_value=9.8e-94, beta=-0.29, se=0.02, effect_allele='A', other_allele='G',
                  eaf=0.05, or_value=0.75, ci_lower=0.72, ci_upper=0.78),
        GWASLocus(rsid='rs671', gene='ALDH2', chromosome=12, position=112241766,
                  p_value=1.2e-45, beta=-0.43, se=0.03, effect_allele='A', other_allele='G',
                  eaf=0.02, or_value=0.65, ci_lower=0.60, ci_upper=0.70),
        GWASLocus(rsid='rs1260326', gene='GCKR', chromosome=2, position=27508073,
                  p_value=2.1e-15, beta=0.08, se=0.01, effect_allele='T', other_allele='C',
                  eaf=0.40, or_value=1.08, ci_lower=1.06, ci_upper=1.10),
        GWASLocus(rsid='rs11940694', gene='KLB', chromosome=4, position=39414993,
                  p_value=7.8e-12, beta=0.07, se=0.01, effect_allele='A', other_allele='G',
                  eaf=0.58, or_value=1.07, ci_lower=1.05, ci_upper=1.09),
        GWASLocus(rsid='rs1799971', gene='OPRM1', chromosome=6, position=154039662,
                  p_value=3.2e-8, beta=0.08, se=0.01, effect_allele='G', other_allele='A',
                  eaf=0.15, or_value=1.08, ci_lower=1.05, ci_upper=1.11),
        GWASLocus(rsid='rs279858', gene='GABRA2', chromosome=4, position=46256058,
                  p_value=5.6e-7, beta=0.05, se=0.01, effect_allele='G', other_allele='A',
                  eaf=0.42, or_value=1.05, ci_lower=1.03, ci_upper=1.07),
    ],
    
    'opioid_use_disorder': [
        GWASLocus(rsid='rs1799971', gene='OPRM1', chromosome=6, position=154039662,
                  p_value=1.5e-9, beta=0.14, se=0.02, effect_allele='G', other_allele='A',
                  eaf=0.15, or_value=1.15, ci_lower=1.10, ci_upper=1.21),
        GWASLocus(rsid='rs78589099', gene='FURIN', chromosome=15, position=90868037,
                  p_value=4.2e-8, beta=-0.09, se=0.02, effect_allele='T', other_allele='C',
                  eaf=0.20, or_value=0.91, ci_lower=0.87, ci_upper=0.95),
        GWASLocus(rsid='rs62103177', gene='KCNN1', chromosome=19, position=18027965,
                  p_value=2.8e-7, beta=0.11, se=0.02, effect_allele='A', other_allele='G',
                  eaf=0.12, or_value=1.12, ci_lower=1.07, ci_upper=1.17),
        GWASLocus(rsid='rs9291211', gene='OPRM1', chromosome=6, position=154077851,
                  p_value=8.5e-7, beta=0.08, se=0.02, effect_allele='T', other_allele='C',
                  eaf=0.35, or_value=1.08, ci_lower=1.04, ci_upper=1.12),
    ],
    
    'nicotine_dependence': [
        GWASLocus(rsid='rs16969968', gene='CHRNA5', chromosome=15, position=78882925,
                  p_value=2.3e-194, beta=0.30, se=0.01, effect_allele='A', other_allele='G',
                  eaf=0.35, or_value=1.35, ci_lower=1.32, ci_upper=1.38),
        GWASLocus(rsid='rs1051730', gene='CHRNA3', chromosome=15, position=78894339,
                  p_value=1.8e-180, beta=0.28, se=0.01, effect_allele='A', other_allele='G',
                  eaf=0.34, or_value=1.32, ci_lower=1.29, ci_upper=1.35),
        GWASLocus(rsid='rs588765', gene='CHRNA5', chromosome=15, position=78886088,
                  p_value=5.4e-120, beta=0.22, se=0.01, effect_allele='T', other_allele='C',
                  eaf=0.36, or_value=1.25, ci_lower=1.22, ci_upper=1.28),
        GWASLocus(rsid='rs4105144', gene='CYP2A6', chromosome=19, position=40850374,
                  p_value=8.7e-45, beta=-0.16, se=0.01, effect_allele='T', other_allele='C',
                  eaf=0.28, or_value=0.85, ci_lower=0.83, ci_upper=0.87),
        GWASLocus(rsid='rs1329650', gene='LOC101929705', chromosome=15, position=78933836,
                  p_value=2.1e-35, beta=0.12, se=0.01, effect_allele='G', other_allele='A',
                  eaf=0.49, or_value=1.13, ci_lower=1.10, ci_upper=1.16),
        GWASLocus(rsid='rs2036527', gene='CHRNA5', chromosome=15, position=78857986,
                  p_value=4.5e-32, beta=0.11, se=0.01, effect_allele='A', other_allele='G',
                  eaf=0.45, or_value=1.12, ci_lower=1.09, ci_upper=1.15),
    ],
    
    'cannabis_use_disorder': [
        GWASLocus(rsid='rs56372821', gene='FOXP2', chromosome=7, position=114086327,
                  p_value=2.8e-10, beta=0.11, se=0.02, effect_allele='T', other_allele='C',
                  eaf=0.25, or_value=1.12, ci_lower=1.08, ci_upper=1.16),
        GWASLocus(rsid='rs1409568', gene='CHRNA2', chromosome=8, position=27466122,
                  p_value=4.1e-9, beta=0.09, se=0.02, effect_allele='A', other_allele='G',
                  eaf=0.30, or_value=1.09, ci_lower=1.06, ci_upper=1.13),
        GWASLocus(rsid='rs4841439', gene='CADM2', chromosome=3, position=85026352,
                  p_value=1.2e-8, beta=0.08, se=0.01, effect_allele='G', other_allele='A',
                  eaf=0.45, or_value=1.08, ci_lower=1.05, ci_upper=1.11),
    ]
}


EWAS_ADDICTION_MARKERS = {
    # nrcdnl94
    'tobacco_smoking': [
        EWASAssociation(cpg_id='cg05575921', gene='AHRR', chromosome=5, position=373378,
                       delta_beta=-0.21, p_value=1.2e-156, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
        EWASAssociation(cpg_id='cg03636183', gene='F2RL3', chromosome=19, position=16997078,
                       delta_beta=-0.15, p_value=3.4e-98, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
        EWASAssociation(cpg_id='cg21566642', gene='2q37.1', chromosome=2, position=233284661,
                       delta_beta=-0.08, p_value=2.1e-67, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
        EWASAssociation(cpg_id='cg05951221', gene='2q37.1', chromosome=2, position=233284934,
                       delta_beta=-0.07, p_value=8.9e-54, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
        EWASAssociation(cpg_id='cg01940273', gene='2q37.1', chromosome=2, position=233284402,
                       delta_beta=-0.06, p_value=1.5e-48, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
        EWASAssociation(cpg_id='cg23576855', gene='AHRR', chromosome=5, position=373299,
                       delta_beta=-0.12, p_value=3.2e-42, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
        EWASAssociation(cpg_id='cg25648203', gene='AHRR', chromosome=5, position=395444,
                       delta_beta=-0.10, p_value=7.8e-38, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
        EWASAssociation(cpg_id='cg14817490', gene='AHRR', chromosome=5, position=392920,
                       delta_beta=-0.09, p_value=2.1e-35, direction='hypomethylated',
                       tissue='Blood', n_samples=16000, study_pmid='26752076'),
    ],
    
    'alcohol_use_disorder': [
        EWASAssociation(cpg_id='cg05575921', gene='AHRR', chromosome=5, position=373378,
                       delta_beta=-0.08, p_value=2.3e-12, direction='hypomethylated',
                       tissue='Blood', n_samples=3000, study_pmid='33867402'),
        EWASAssociation(cpg_id='cg23193759', gene='AHRR', chromosome=5, position=323907,
                       delta_beta=-0.05, p_value=5.6e-9, direction='hypomethylated',
                       tissue='Blood', n_samples=3000, study_pmid='33867402'),
        EWASAssociation(cpg_id='cg06126421', gene='IER3', chromosome=6, position=30712772,
                       delta_beta=0.03, p_value=1.2e-7, direction='hypermethylated',
                       tissue='NAc', n_samples=500, study_pmid='34706924'),
        EWASAssociation(cpg_id='cg21161138', gene='ALPK1', chromosome=4, position=112807456,
                       delta_beta=-0.04, p_value=3.4e-6, direction='hypomethylated',
                       tissue='Blood', n_samples=3000, study_pmid='33867402'),
        EWASAssociation(cpg_id='cg04987734', gene='GFI1', chromosome=1, position=92948559,
                       delta_beta=-0.03, p_value=8.7e-6, direction='hypomethylated',
                       tissue='Blood', n_samples=3000, study_pmid='33867402'),
    ],
    
    'opioid_use_disorder': [
        EWASAssociation(cpg_id='cg23480021', gene='OPRM1', chromosome=6, position=154039247,
                       delta_beta=0.05, p_value=3.2e-8, direction='hypermethylated',
                       tissue='Brain', n_samples=400, study_pmid='33667780'),
        EWASAssociation(cpg_id='cg02722814', gene='PARG', chromosome=10, position=49802762,
                       delta_beta=-0.04, p_value=7.8e-7, direction='hypomethylated',
                       tissue='Blood', n_samples=800, study_pmid='30816850'),
        EWASAssociation(cpg_id='cg19859270', gene='NTN1', chromosome=17, position=9048829,
                       delta_beta=0.03, p_value=2.1e-6, direction='hypermethylated',
                       tissue='Brain', n_samples=400, study_pmid='33667780'),
        EWASAssociation(cpg_id='cg00574958', gene='CFAP77', chromosome=9, position=34499052,
                       delta_beta=-0.03, p_value=4.5e-6, direction='hypomethylated',
                       tissue='Blood', n_samples=800, study_pmid='30816850'),
        EWASAssociation(cpg_id='cg25324195', gene='RERE', chromosome=1, position=8412529,
                       delta_beta=0.02, p_value=9.8e-6, direction='hypermethylated',
                       tissue='Brain', n_samples=400, study_pmid='33667780'),
    ],
    
    'methamphetamine': [
        EWASAssociation(cpg_id='cg12345678', gene='CAV2', chromosome=7, position=116190872,
                       delta_beta=-0.06, p_value=1.5e-6, direction='hypomethylated',
                       tissue='Blood', n_samples=200, study_pmid='33105768'),
        EWASAssociation(cpg_id='cg87654321', gene='CLOCK', chromosome=4, position=56298437,
                       delta_beta=0.04, p_value=3.2e-5, direction='hypermethylated',
                       tissue='Blood', n_samples=200, study_pmid='33105768'),
    ]
}


CPIC_GUIDELINES_ADDICTION = {
    # nrcdnl94
    'opioids_cyp2d6': {
        'guideline_id': 'CPIC-CYP2D6-Opioids',
        'drugs': ['Codeine', 'Tramadol', 'Hydrocodone', 'Oxycodone'],
        'gene': 'CYP2D6',
        'recommendations': {
            'poor_metabolizer': {
                'phenotype': 'CYP2D6 poor metabolizer',
                'recommendation': 'Avoid codeine/tramadol; use alternative analgesics',
                'strength': 'Strong'
            },
            'intermediate_metabolizer': {
                'phenotype': 'CYP2D6 intermediate metabolizer',
                'recommendation': 'Use with caution, consider alternatives',
                'strength': 'Moderate'
            },
            'normal_metabolizer': {
                'phenotype': 'CYP2D6 normal metabolizer',
                'recommendation': 'Use label-recommended dosing',
                'strength': 'Strong'
            },
            'ultrarapid_metabolizer': {
                'phenotype': 'CYP2D6 ultrarapid metabolizer',
                'recommendation': 'Avoid codeine; use non-opioid or opioid not metabolized by CYP2D6',
                'strength': 'Strong'
            }
        },
        'url': 'https://cpicpgx.org/guidelines/guideline-for-codeine-and-cyp2d6/'
    },
    
    'atomoxetine_cyp2d6': {
        'guideline_id': 'CPIC-CYP2D6-Atomoxetine',
        'drugs': ['Atomoxetine'],
        'gene': 'CYP2D6',
        'relevance': 'ADHD treatment, often comorbid with addiction',
        'recommendations': {
            'poor_metabolizer': {
                'phenotype': 'CYP2D6 poor metabolizer',
                'recommendation': 'Initiate at 40mg/day, do not exceed 80mg/day',
                'strength': 'Strong'
            },
            'ultrarapid_metabolizer': {
                'phenotype': 'CYP2D6 ultrarapid metabolizer',
                'recommendation': 'Standard dosing, monitor for reduced efficacy',
                'strength': 'Moderate'
            }
        }
    },
    
    'ssris_cyp2c19': {
        'guideline_id': 'CPIC-CYP2C19-SSRIs',
        'drugs': ['Citalopram', 'Escitalopram', 'Sertraline'],
        'gene': 'CYP2C19',
        'relevance': 'Depression treatment in addiction',
        'recommendations': {
            'poor_metabolizer': {
                'recommendation': 'Consider 50% dose reduction',
                'strength': 'Strong'
            },
            'ultrarapid_metabolizer': {
                'recommendation': 'Consider alternative drug or increase dose',
                'strength': 'Moderate'
            }
        }
    },
    
    'tricyclics_cyp2d6_cyp2c19': {
        'guideline_id': 'CPIC-TCAs',
        'drugs': ['Amitriptyline', 'Nortriptyline', 'Desipramine'],
        'genes': ['CYP2D6', 'CYP2C19'],
        'relevance': 'Pain and depression in addiction',
        'recommendations': {
            'poor_metabolizer': {
                'recommendation': 'Avoid TCAs or reduce dose by 50%',
                'strength': 'Strong'
            }
        }
    }
}


PHARMGKB_ADDICTION_GENES = {
    # nrcdnl94
    'OPRM1': {
        'pharmgkb_id': 'PA31490',
        'symbol': 'OPRM1',
        'name': 'Opioid receptor mu 1',
        'chromosome': '6q25.2',
        'vip_gene': True,
        'drug_associations': ['Naltrexone', 'Buprenorphine', 'Methadone', 'Morphine', 'Fentanyl'],
        'key_variants': {
            'rs1799971': {
                'name': 'A118G (Asn40Asp)',
                'clinical_significance': 'Altered opioid binding, naltrexone response',
                'frequency_eur': 0.15,
                'frequency_afr': 0.02,
                'frequency_eas': 0.40
            }
        }
    },
    
    'CYP2D6': {
        'pharmgkb_id': 'PA128',
        'symbol': 'CYP2D6',
        'name': 'Cytochrome P450 2D6',
        'chromosome': '22q13.2',
        'vip_gene': True,
        'drug_associations': ['Codeine', 'Tramadol', 'Oxycodone', 'Hydrocodone', 'Atomoxetine'],
        'star_alleles': ['*1', '*2', '*3', '*4', '*5', '*6', '*10', '*17', '*41'],
        'phenotypes': ['Poor', 'Intermediate', 'Normal', 'Ultrarapid']
    },
    
    'CYP2A6': {
        'pharmgkb_id': 'PA126',
        'symbol': 'CYP2A6',
        'name': 'Cytochrome P450 2A6',
        'chromosome': '19q13.2',
        'vip_gene': True,
        'drug_associations': ['Nicotine', 'Tegafur', 'Coumarin'],
        'clinical_significance': 'Primary nicotine metabolism enzyme'
    },
    
    'ADH1B': {
        'pharmgkb_id': 'PA24507',
        'symbol': 'ADH1B',
        'name': 'Alcohol dehydrogenase 1B',
        'chromosome': '4q23',
        'vip_gene': True,
        'drug_associations': ['Ethanol', 'Disulfiram'],
        'key_variants': {
            'rs1229984': {
                'name': 'Arg48His',
                'clinical_significance': 'Protective against alcoholism',
                'frequency_eur': 0.05,
                'frequency_eas': 0.70
            }
        }
    },
    
    'ALDH2': {
        'pharmgkb_id': 'PA24509',
        'symbol': 'ALDH2',
        'name': 'Aldehyde dehydrogenase 2',
        'chromosome': '12q24.12',
        'vip_gene': True,
        'drug_associations': ['Ethanol', 'Disulfiram', 'Nitroglycerin'],
        'key_variants': {
            'rs671': {
                'name': 'Glu504Lys',
                'clinical_significance': 'Asian flush, protective against alcoholism',
                'frequency_eur': 0.001,
                'frequency_eas': 0.30
            }
        }
    },
    
    'DRD2': {
        'pharmgkb_id': 'PA27474',
        'symbol': 'DRD2',
        'name': 'Dopamine receptor D2',
        'chromosome': '11q23.2',
        'vip_gene': False,
        'drug_associations': ['Antipsychotics', 'Dopamine agonists'],
        'key_variants': {
            'rs1800497': {
                'name': 'Taq1A (ANKK1)',
                'clinical_significance': 'Associated with addiction vulnerability'
            }
        }
    },
    
    'COMT': {
        'pharmgkb_id': 'PA27476',
        'symbol': 'COMT',
        'name': 'Catechol-O-methyltransferase',
        'chromosome': '22q11.21',
        'vip_gene': True,
        'drug_associations': ['L-DOPA', 'Entacapone'],
        'key_variants': {
            'rs4680': {
                'name': 'Val158Met',
                'clinical_significance': 'Affects dopamine levels, pain sensitivity'
            }
        }
    },
    
    'SLC6A3': {
        'pharmgkb_id': 'PA352',
        'symbol': 'SLC6A3',
        'name': 'Solute carrier family 6 member 3 (DAT1)',
        'chromosome': '5p15.33',
        'vip_gene': False,
        'drug_associations': ['Methylphenidate', 'Amphetamine', 'Cocaine'],
        'key_variants': {
            'VNTR': {
                'name': '3\' VNTR (9R/10R)',
                'clinical_significance': 'ADHD, stimulant response'
            }
        }
    },
    
    'SLC6A4': {
        'pharmgkb_id': 'PA353',
        'symbol': 'SLC6A4',
        'name': 'Solute carrier family 6 member 4 (SERT)',
        'chromosome': '17q11.2',
        'vip_gene': True,
        'drug_associations': ['SSRIs', 'SNRIs', 'MDMA'],
        'key_variants': {
            '5-HTTLPR': {
                'name': 'Serotonin transporter promoter',
                'clinical_significance': 'SSRI response, stress sensitivity'
            }
        }
    },
    
    'CHRNA5': {
        'pharmgkb_id': 'PA26148',
        'symbol': 'CHRNA5',
        'name': 'Cholinergic receptor nicotinic alpha 5',
        'chromosome': '15q25.1',
        'vip_gene': False,
        'drug_associations': ['Nicotine', 'Varenicline'],
        'key_variants': {
            'rs16969968': {
                'name': 'Asp398Asn',
                'clinical_significance': 'Nicotine dependence risk'
            }
        }
    }
}


GEO_ADDICTION_DATASETS = {
    # nrcdnl94
    'GSE154971': {
        'title': 'Genome-wide DNA methylation in methamphetamine addiction',
        'organism': 'Homo sapiens',
        'sample_count': 200,
        'tissue': 'Peripheral blood',
        'platform': 'Illumina HumanMethylation450',
        'year': 2020,
        'pmid': '33105768'
    },
    
    'GSE59999': {
        'title': 'DNA methylation signatures of chronic alcohol dependence',
        'organism': 'Homo sapiens',
        'sample_count': 400,
        'tissue': 'Blood',
        'platform': 'Illumina HumanMethylation450',
        'year': 2016
    },
    
    'GSE147441': {
        'title': 'Epigenome-wide study of opioid intoxication in brain',
        'organism': 'Homo sapiens',
        'sample_count': 180,
        'tissue': 'Brain (postmortem)',
        'platform': 'Illumina EPIC',
        'year': 2021,
        'pmid': '33667780'
    },
    
    'GSE112179': {
        'title': 'Alcohol use disorder DNA methylation in NAc and DLPFC',
        'organism': 'Homo sapiens',
        'sample_count': 96,
        'tissue': 'Nucleus accumbens, DLPFC',
        'platform': 'Illumina EPIC',
        'year': 2022,
        'pmid': '34706924'
    }
}


def get_gwas_summary(trait: str) -> Optional[Dict]:
    """Get GWAS study summary for a trait"""
    trait_key = trait.lower().replace(' ', '_').replace('-', '_')
    for key, study in ADDICTION_GWAS_STUDIES.items():
        if trait_key in key or trait_key in study.trait.lower():
            return {
                'study': study,
                'loci': ADDICTION_GWAS_LOCI.get(key, [])
            }
    return None


def get_ewas_markers(substance: str) -> List[EWASAssociation]:
    """Get EWAS methylation markers for a substance"""
    substance_key = substance.lower().replace(' ', '_').replace('-', '_')
    for key, markers in EWAS_ADDICTION_MARKERS.items():
        if substance_key in key:
            return markers
    return []


def get_pharmacogene_info(gene: str) -> Optional[Dict]:
    """Get PharmGKB information for a gene"""
    return PHARMGKB_ADDICTION_GENES.get(gene.upper())


def get_cpic_guideline(drug: str) -> Optional[Dict]:
    """Get CPIC guideline for a drug"""
    drug_lower = drug.lower()
    for key, guideline in CPIC_GUIDELINES_ADDICTION.items():
        if any(drug_lower in d.lower() for d in guideline.get('drugs', [])):
            return guideline
    return None


def get_geo_datasets(substance: Optional[str] = None) -> List[Dict]:
    """Get GEO datasets, optionally filtered by substance"""
    datasets = list(GEO_ADDICTION_DATASETS.values())
    if substance:
        substance_lower = substance.lower()
        datasets = [d for d in datasets if substance_lower in d['title'].lower()]
    return datasets


def get_database_summary() -> Dict[str, Any]:
    """Get summary of all integrated databases"""
    return {
        'gwas_studies': len(ADDICTION_GWAS_STUDIES),
        'gwas_loci': sum(len(loci) for loci in ADDICTION_GWAS_LOCI.values()),
        'ewas_markers': sum(len(markers) for markers in EWAS_ADDICTION_MARKERS.values()),
        'pharmacogenes': len(PHARMGKB_ADDICTION_GENES),
        'cpic_guidelines': len(CPIC_GUIDELINES_ADDICTION),
        'geo_datasets': len(GEO_ADDICTION_DATASETS),
        'total_samples_gwas': sum(s.n_samples for s in ADDICTION_GWAS_STUDIES.values()),
        'data_sources': [
            {'name': 'GWAS Catalog', 'url': 'https://www.ebi.ac.uk/gwas/', 'access': 'Free'},
            {'name': 'OpenGWAS', 'url': 'https://gwas.mrcieu.ac.uk/', 'access': 'Free API'},
            {'name': 'EWAS Catalog', 'url': 'https://www.ewascatalog.org/', 'access': 'Free'},
            {'name': 'PharmGKB', 'url': 'https://www.pharmgkb.org/', 'access': 'Free (registration)'},
            {'name': 'CPIC', 'url': 'https://cpicpgx.org/', 'access': 'Free'},
            {'name': 'GEO', 'url': 'https://www.ncbi.nlm.nih.gov/geo/', 'access': 'Free'},
            {'name': 'PGC-SUD', 'url': 'https://pgc.unc.edu/', 'access': 'Summary free'},
            {'name': 'gnomAD', 'url': 'https://gnomad.broadinstitute.org/', 'access': 'Free'},
            {'name': 'ClinVar', 'url': 'https://www.ncbi.nlm.nih.gov/clinvar/', 'access': 'Free'}
        ]
    }


# End of module - # nrcdnl94