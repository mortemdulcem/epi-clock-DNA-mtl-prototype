# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
Real Variant Data Sources Module
700,000+ variant integration from open-access genomic databases

Data Sources (ALL FREE):
- 1000 Genomes Project (84.7M variants, 2,504 individuals)
- gnomAD v4.0 (750M variants, 807K individuals)
- UK Biobank (96M variants, 500K individuals - academic access)
- TOPMed (400M variants, 150K individuals - dbGaP access)
- GWAS Catalog (ongoing additions)

Author: Dr. Nurcan Denli Bayır
Platform: EpiClock Prototype
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import hashlib


class DataSource(Enum):
    # nrcdnl94
    """Available genomic data sources"""
    THOUSAND_GENOMES = "1000 Genomes Project"
    GNOMAD = "gnomAD v4.0"
    UK_BIOBANK = "UK Biobank"
    TOPMED = "TOPMed"
    GWAS_CATALOG = "GWAS Catalog"


@dataclass
# nrcdnl94
class DataSourceInfo:
    # nrcdnl94
    """Information about a genomic data source"""
    name: str
    source: DataSource
    n_variants: int
    n_individuals: int
    access_type: str
    cost: str
    url: str
    file_size: str
    description: str
    populations: List[str]
    data_format: List[str]
    advantages: List[str]
    limitations: List[str]


DATA_SOURCES_DATABASE = {
    # nrcdnl94
    '1000_genomes': DataSourceInfo(
        name="1000 Genomes Project - Phase 3",
        source=DataSource.THOUSAND_GENOMES,
        n_variants=84_700_000,
        n_individuals=2504,
        access_type="Açık Erişim (Open Access)",
        cost="ÜCRETSİZ",
        url="https://www.internationalgenome.org/data",
        file_size="~40 GB (sıkıştırılmış), ~1.5 TB (açık)",
        description="Tüm genom sekanslama (WGS) ile 26 popülasyondan 2,504 bireyin genetik varyasyonları",
        populations=["AFR (Afrikalı)", "AMR (Amerikalı)", "EAS (Doğu Asyalı)", 
                    "EUR (Avrupalı)", "SAS (Güney Asyalı)"],
        data_format=["VCF", "CRAM", "FASTA"],
        advantages=[
            "84.7 milyon varyant (700K'dan çok fazla)",
            "Tam ücretsiz ve açık erişim",
            "Yüksek kalite (deep sequencing)",
            "Popülasyon frekansları mevcut",
            "Phased genotypes (haplotype bilgisi)",
            "Tüm dünyada kabul görmüş referans"
        ],
        limitations=[
            "Büyük dosya boyutu (~1.5 TB açık)",
            "İndirme süresi uzun",
            "Bazı nadir varyantlar eksik olabilir"
        ]
    ),
    
    'gnomad': DataSourceInfo(
        name="gnomAD v4.0 - Genome Aggregation Database",
        source=DataSource.GNOMAD,
        n_variants=750_000_000,
        n_individuals=807162,
        access_type="Açık Erişim (Open Access)",
        cost="ÜCRETSİZ",
        url="https://gnomad.broadinstitute.org/downloads",
        file_size="~200 GB (exomes), ~500 GB (genomes)",
        description="En güncel ve kapsamlı popülasyon varyant veritabanı",
        populations=["African/African American", "Admixed American", "Ashkenazi Jewish",
                    "East Asian", "Finnish", "Non-Finnish European", "Middle Eastern", "South Asian"],
        data_format=["VCF", "Hail Table"],
        advantages=[
            "750 milyon varyant (en kapsamlı)",
            "En güncel veri (2023)",
            "Yüksek kalite kontrol",
            "8 popülasyon frekansı",
            "Fonksiyonel anotasyonlar dahil",
            "ClinVar entegrasyonu"
        ],
        limitations=[
            "Çok büyük dosya boyutu (~700 GB)",
            "Google Cloud SDK gerekebilir",
            "İşlem gücü yoğun"
        ]
    ),
    
    'uk_biobank': DataSourceInfo(
        name="UK Biobank - World's Largest Health Database",
        source=DataSource.UK_BIOBANK,
        n_variants=96_000_000,
        n_individuals=500000,
        access_type="Başvuru Gerekli (Akademik)",
        cost="£0-2,500 (akademik), £20,000+ (ticari)",
        url="https://www.ukbiobank.ac.uk/enable-your-research/apply-for-access",
        file_size="~500 GB per chromosome",
        description="500,000 İngiliz bireyin genetik ve fenotip verileri",
        populations=["UK Population (predominantly European)"],
        data_format=["BGEN", "PLINK", "VCF (talep üzerine)"],
        advantages=[
            "96 milyon varyant (imputed)",
            "Zengin fenotip verileri (madde kullanımı dahil)",
            "Longitudinal takip",
            "Yüksek imputation kalitesi",
            "Biomarker verileri"
        ],
        limitations=[
            "Başvuru gerekli (4-8 hafta)",
            "Etik onayı şart",
            "Sadece UK popülasyonu"
        ]
    ),
    
    'topmed': DataSourceInfo(
        name="TOPMed - Trans-Omics for Precision Medicine",
        source=DataSource.TOPMED,
        n_variants=400_000_000,
        n_individuals=150000,
        access_type="dbGaP Başvurusu",
        cost="ÜCRETSİZ (akademik)",
        url="https://www.ncbi.nlm.nih.gov/gap/",
        file_size="Varies by study",
        description="Derin tüm genom sekanslama (30-40×) ile 150,000+ birey",
        populations=["Multi-ethnic US populations"],
        data_format=["VCF", "CRAM", "BAM"],
        advantages=[
            "400 milyon varyant",
            "Derin sekanslama (30-40×)",
            "Çeşitli fenotiplerle",
            "Yüksek kalite variant calling",
            "Nadir varyantlar dahil"
        ],
        limitations=[
            "dbGaP başvurusu gerekli",
            "IRB onayı şart",
            "Büyük dosya boyutu"
        ]
    ),
    
    'gwas_catalog': DataSourceInfo(
        name="GWAS Catalog - NHGRI-EBI",
        source=DataSource.GWAS_CATALOG,
        n_variants=500_000,
        n_individuals=0,
        access_type="Açık Erişim",
        cost="ÜCRETSİZ",
        url="https://www.ebi.ac.uk/gwas/",
        file_size="~5 GB",
        description="Tüm yayınlanmış GWAS çalışmalarından hastalık/özellik ilişkili varyantlar",
        populations=["All populations"],
        data_format=["TSV", "JSON", "API"],
        advantages=[
            "Hastalık ilişkileri doğrulanmış",
            "Sürekli güncelleniyor",
            "API erişimi mevcut",
            "Akademik referanslar dahil"
        ],
        limitations=[
            "Sadece GWAS-anlamlı varyantlar",
            "Bireysel genotip yok"
        ]
    )
}


ADDICTION_GENE_SYSTEMS = {
    # nrcdnl94
    'opioid_system': {
        'description': 'Opioid Reseptör Sistemi',
        'genes': ['OPRM1', 'OPRD1', 'OPRK1', 'OPRL1', 'PDYN', 'PENK', 'POMC',
                 'ARRB1', 'ARRB2', 'GRK2', 'GRK3', 'GRK5'],
        'relevance': 'Opioid bağımlılığı, ağrı duyarlılığı, ödül işleme'
    },
    'dopamine_system': {
        'description': 'Dopamin Nörotransmitter Sistemi',
        'genes': ['DRD1', 'DRD2', 'DRD3', 'DRD4', 'DRD5', 'SLC6A3', 'SLC18A2',
                 'TH', 'DDC', 'DBH', 'PNMT', 'COMT', 'MAOA', 'MAOB',
                 'PPP1R1B', 'GNAL', 'GNAO1', 'ANKK1'],
        'relevance': 'Ödül sistemi, motivasyon, bağımlılık genel riski'
    },
    'serotonin_system': {
        'description': 'Serotonin (5-HT) Sistemi',
        'genes': ['HTR1A', 'HTR1B', 'HTR1D', 'HTR2A', 'HTR2B', 'HTR2C',
                 'HTR3A', 'HTR3B', 'HTR4', 'HTR5A', 'HTR6', 'HTR7',
                 'SLC6A4', 'TPH1', 'TPH2'],
        'relevance': 'Duygudurum düzenleme, impulsivite, depresyon komorbidite'
    },
    'gaba_system': {
        'description': 'GABAerjik Sistem',
        'genes': ['GABRA1', 'GABRA2', 'GABRA3', 'GABRA4', 'GABRA5', 'GABRA6',
                 'GABRB1', 'GABRB2', 'GABRB3', 'GABRG1', 'GABRG2', 'GABRG3',
                 'GABRD', 'SLC6A1', 'GAD1', 'GAD2', 'ABAT'],
        'relevance': 'Anksiyete, alkol bağımlılığı, benzodiazepin duyarlılığı'
    },
    'glutamate_system': {
        'description': 'Glutamaterjik Sistem',
        'genes': ['GRIN1', 'GRIN2A', 'GRIN2B', 'GRIN2C', 'GRIN2D',
                 'GRIA1', 'GRIA2', 'GRIA3', 'GRIA4',
                 'GRIK1', 'GRIK2', 'GRIK3', 'GRIK4', 'GRIK5',
                 'GRM1', 'GRM2', 'GRM3', 'GRM4', 'GRM5', 'GRM6', 'GRM7', 'GRM8',
                 'SLC1A1', 'SLC1A2', 'SLC1A3'],
        'relevance': 'Nöroplastisite, öğrenme, nörotoksisite'
    },
    'cannabinoid_system': {
        'description': 'Endokannabinoid Sistemi',
        'genes': ['CNR1', 'CNR2', 'FAAH', 'MGLL', 'DAGLA', 'DAGLB',
                 'TRPV1', 'GPR55', 'GPR18', 'GPR119'],
        'relevance': 'Esrar bağımlılığı, ağrı, iştah düzenleme'
    },
    'nicotinic_system': {
        'description': 'Nikotinik Asetilkolin Sistemi',
        'genes': ['CHRNA3', 'CHRNA4', 'CHRNA5', 'CHRNA6', 'CHRNA7',
                 'CHRNB2', 'CHRNB3', 'CHRNB4', 'ACHE', 'BCHE', 'CHAT'],
        'relevance': 'Nikotin bağımlılığı, sigara kullanımı, bırakma zorluğu'
    },
    'alcohol_metabolism': {
        'description': 'Alkol Metabolizma Enzimleri',
        'genes': ['ADH1A', 'ADH1B', 'ADH1C', 'ADH4', 'ADH5', 'ADH6', 'ADH7',
                 'ALDH1A1', 'ALDH1B1', 'ALDH2', 'ALDH3A1', 'CYP2E1', 'PNPLA3'],
        'relevance': 'Alkol toleransı, "Asian flush", karaciğer hastalığı riski'
    },
    'drug_metabolism': {
        'description': 'Farmakogenomik (İlaç Metabolizması)',
        'genes': ['CYP1A1', 'CYP1A2', 'CYP2A6', 'CYP2B6', 'CYP2C8', 'CYP2C9',
                 'CYP2C19', 'CYP2D6', 'CYP2E1', 'CYP3A4', 'CYP3A5',
                 'UGT1A1', 'UGT2B7', 'UGT2B15',
                 'ABCB1', 'ABCG2', 'SLCO1B1', 'SLC22A1'],
        'relevance': 'İlaç yanıtı, doz ayarlaması, yan etki riski'
    },
    'neuroplasticity': {
        'description': 'Nöroplastisite ve Sinaptik Fonksiyon',
        'genes': ['BDNF', 'NGF', 'NTF3', 'NTF4', 'GDNF',
                 'NTRK1', 'NTRK2', 'NTRK3',
                 'CREB1', 'CREB3', 'FOS', 'FOSB', 'JUN',
                 'ARC', 'HOMER1', 'EGR1', 'EGR2'],
        'relevance': 'Öğrenme, hafıza, bağımlılık oluşumu ve düzelmesi'
    },
    'epigenetic_regulators': {
        'description': 'Epigenetik Düzenleyiciler',
        'genes': ['DNMT1', 'DNMT3A', 'DNMT3B', 'TET1', 'TET2', 'TET3',
                 'HDAC1', 'HDAC2', 'HDAC3', 'HDAC4', 'HDAC5',
                 'KAT2A', 'KAT2B', 'KDM1A', 'KDM4A', 'KDM5A'],
        'relevance': 'Epigenetik yaş ivmelenmesi, gen ekspresyon düzenleme'
    },
    'stress_hpa': {
        'description': 'Stres ve HPA Ekseni',
        'genes': ['NR3C1', 'NR3C2', 'FKBP5', 'FKBP4',
                 'CRH', 'CRHR1', 'CRHR2', 'POMC', 'MC2R',
                 'AVP', 'AVPR1A', 'AVPR1B', 'OXT', 'OXTR'],
        'relevance': 'Stres tepkisi, kortizol, travma ilişkili risk'
    }
}


class VariantDataSourceManager:
    # nrcdnl94
    """Manage variant data from multiple genomic sources"""
    
    def __init__(self):
        self.sources = DATA_SOURCES_DATABASE.copy()
        self.gene_systems = ADDICTION_GENE_SYSTEMS.copy()
        
    def get_source_comparison(self) -> pd.DataFrame:
        """Generate comparison table of all data sources"""
        comparison = []
        for key, info in self.sources.items():
            comparison.append({
                'Kaynak': info.name,
                'Varyant Sayısı': f"{info.n_variants:,}",
                'Birey Sayısı': f"{info.n_individuals:,}",
                'Erişim': info.access_type,
                'Maliyet': info.cost,
                'Dosya Boyutu': info.file_size
            })
        return pd.DataFrame(comparison)
    
    def get_addiction_genes_summary(self) -> pd.DataFrame:
        """Get summary of addiction-related gene systems"""
        summary = []
        for system, info in self.gene_systems.items():
            summary.append({
                'Sistem': info['description'],
                'Gen Sayısı': len(info['genes']),
                'Örnek Genler': ', '.join(info['genes'][:5]) + '...',
                'Klinik Önem': info['relevance']
            })
        return pd.DataFrame(summary)
    
    def get_all_addiction_genes(self) -> List[str]:
        """Get complete list of addiction-related genes"""
        all_genes = []
        for system, info in self.gene_systems.items():
            all_genes.extend(info['genes'])
        return list(set(all_genes))
    
    def calculate_cost_savings(self, n_samples: int = 100) -> Dict:
        """Calculate cost savings compared to traditional approach"""
        
        traditional = {
            'wgs_30x': n_samples * 15000,
            'bioinformatics': n_samples * 500,
            'software_licenses': 50000,
            'personnel': n_samples * 200,
            'storage': n_samples * 50,
        }
        traditional['total'] = sum(traditional.values())
        
        epiclock = {
            'wgs_1x': n_samples * 750,
            'imputation': 0,
            'cloud_compute': n_samples * 50,
            'personnel': n_samples * 100,
            'storage': n_samples * 20,
        }
        epiclock['total'] = sum(epiclock.values())
        
        savings = traditional['total'] - epiclock['total']
        savings_percent = (savings / traditional['total']) * 100
        
        imputed_variants = 40_000_000
        
        return {
            'traditional': traditional,
            'epiclock': epiclock,
            'savings': savings,
            'savings_percent': savings_percent,
            'imputed_variants': imputed_variants,
            'cost_per_variant_traditional': traditional['total'] / 700_000,
            'cost_per_variant_epiclock': epiclock['total'] / imputed_variants,
            'summary': f"""
MALIYET KARŞILAŞTIRMASI ({n_samples} örnek için)

Geleneksel Yaklaşım (30× WGS):
- Sekanslama: {traditional['wgs_30x']:,} TL
- Biyoinformatik: {traditional['bioinformatics']:,} TL
- Yazılım Lisansları: {traditional['software_licenses']:,} TL
- Personel: {traditional['personnel']:,} TL
- Depolama: {traditional['storage']:,} TL
- TOPLAM: {traditional['total']:,} TL

EpiClock Yaklaşımı (1× WGS + Imputation):
- Sekanslama: {epiclock['wgs_1x']:,} TL
- Imputation: ÜCRETSİZ (Michigan/TOPMed Server)
- Cloud: {epiclock['cloud_compute']:,} TL
- Personel: {epiclock['personnel']:,} TL
- Depolama: {epiclock['storage']:,} TL
- TOPLAM: {epiclock['total']:,} TL

TASARRUF: {savings:,} TL (%{savings_percent:.0f})
İmpute Edilen Varyant: ~{imputed_variants:,}
"""
        }
    
    def generate_download_guide(self, source: str) -> str:
        """Generate step-by-step download guide for a data source"""
        
        if source == '1000_genomes':
            return """
# 1000 GENOMES VERİ İNDİRME REHBERİ

## Adım 1: Gerekli Araçları Kurun
```bash
# bcftools ve tabix kurun
sudo apt-get install bcftools tabix wget

# Alternatif: conda ile
conda install -c bioconda bcftools tabix
```

## Adım 2: VCF Dosyalarını İndirin
```bash
# Tek kromozom için (örn: Chr1)
wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz

# Tüm kromozomlar için
for chr in {1..22} X Y; do
    wget -c ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz
    wget -c ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr${chr}.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz.tbi
done
```

## Adım 3: Bağımlılık Genlerini Filtreleyin
```bash
# Gen bölgelerini içeren BED dosyası oluşturun
# addiction_genes.bed dosyasını hazırlayın

# Filtreleme
bcftools view -R addiction_genes.bed ALL.chr1...vcf.gz -Oz -o addiction_chr1.vcf.gz
```

## Adım 4: Varyantları Sayın
```bash
bcftools stats addiction_chr1.vcf.gz | grep "number of SNPs"
```

## Tahmini Süre
- İndirme: 4-8 saat (100 Mbps bağlantı ile)
- Filtreleme: 1-2 saat
- Toplam: ~10 saat
"""
        
        elif source == 'gnomad':
            return """
# gnomAD VERİ İNDİRME REHBERİ

## Adım 1: Google Cloud SDK Kurun
```bash
# SDK indir
curl https://sdk.cloud.google.com | bash

# Yeniden başlat
exec -l $SHELL

# Yapılandır (ücretsiz hesap yeterli)
gcloud init
```

## Adım 2: gsutil ile İndirin
```bash
# Tek kromozom (exome)
gsutil -m cp \\
    gs://gcp-public-data--gnomad/release/4.0/vcf/exomes/gnomad.exomes.v4.0.sites.chr1.vcf.bgz \\
    gs://gcp-public-data--gnomad/release/4.0/vcf/exomes/gnomad.exomes.v4.0.sites.chr1.vcf.bgz.tbi \\
    ./gnomad_data/

# Tüm kromozomlar
for chr in {1..22} X Y; do
    gsutil -m cp \\
        gs://gcp-public-data--gnomad/release/4.0/vcf/exomes/gnomad.exomes.v4.0.sites.chr${chr}.vcf.bgz \\
        ./gnomad_data/
done
```

## Adım 3: Bağımlılık Varyantlarını Filtreleyin
```bash
# Yüksek kalite varyantları filtrele (PASS)
bcftools view -f PASS gnomad.exomes.v4.0.sites.chr1.vcf.bgz -Oz -o filtered_chr1.vcf.gz

# Spesifik genleri çıkar
bcftools view -R addiction_genes.bed filtered_chr1.vcf.gz -Oz -o addiction_variants.vcf.gz
```

## Tahmini Süre
- İndirme: 8-16 saat (fiber bağlantı önerilir)
- Filtreleme: 2-4 saat
"""
        
        elif source == 'gwas_catalog':
            return """
# GWAS CATALOG VERİ İNDİRME REHBERİ

## Adım 1: Python Ortamını Hazırlayın
```bash
pip install requests pandas
```

## Adım 2: API ile Bağımlılık Varyantlarını İndirin
```python
import requests
import pandas as pd

# GWAS Catalog API
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# Bağımlılık trait'leri
traits = [
    'alcohol dependence',
    'opioid dependence', 
    'cocaine dependence',
    'nicotine dependence',
    'cannabis use',
    'substance use disorder'
]

all_associations = []

for trait in traits:
    response = requests.get(
        f"{base_url}/efoTraits/search/findByName",
        params={'name': trait}
    )
    
    if response.ok:
        data = response.json()
        # Varyantları topla
        # ...

# CSV olarak kaydet
df = pd.DataFrame(all_associations)
df.to_csv('gwas_addiction_variants.csv', index=False)
```

## Adım 3: Alternatif - Toplu İndirme
```bash
# Tüm GWAS Catalog verisini indir
wget https://www.ebi.ac.uk/gwas/api/search/downloads/full

# Bağımlılık trait'lerini filtrele
grep -i "addiction\\|dependence\\|substance" gwas_catalog.tsv > addiction_gwas.tsv
```

## Tahmini Süre
- API ile: 30-60 dakika
- Toplu indirme: 5-10 dakika
"""
        
        return "Rehber bulunamadı"


def create_demo_variants_from_sources(n_variants: int = 1000) -> pd.DataFrame:
    """Create realistic demo variants based on real data source patterns"""
    np.random.seed(42)
    
    chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y']
    chrom_probs = [0.08]*5 + [0.06]*5 + [0.04]*10 + [0.03]*2 + [0.02, 0.01]
    chrom_probs = [p/sum(chrom_probs) for p in chrom_probs]
    
    bases = ['A', 'C', 'G', 'T']
    
    manager = VariantDataSourceManager()
    all_genes = manager.get_all_addiction_genes()
    
    variants = []
    for i in range(n_variants):
        chrom = np.random.choice(chromosomes, p=chrom_probs)
        pos = np.random.randint(1_000_000, 250_000_000)
        ref = np.random.choice(bases)
        alt = np.random.choice([b for b in bases if b != ref])
        
        qual = np.random.uniform(20, 100)
        
        rsid = f"rs{np.random.randint(1_000_000, 999_999_999)}" if np.random.random() > 0.2 else None
        
        af_eur = np.random.beta(0.5, 5)
        af_afr = np.random.beta(0.5, 4)
        af_eas = np.random.beta(0.5, 6)
        
        gene = np.random.choice(all_genes) if np.random.random() > 0.7 else None
        
        gt = np.random.choice(['0/0', '0/1', '1/1'], p=[0.5, 0.4, 0.1])
        
        variants.append({
            'CHROM': chrom,
            'POS': pos,
            'ID': rsid,
            'REF': ref,
            'ALT': alt,
            'QUAL': round(qual, 2),
            'FILTER': 'PASS' if qual > 30 else 'LowQual',
            'AF_EUR': round(af_eur, 4),
            'AF_AFR': round(af_afr, 4),
            'AF_EAS': round(af_eas, 4),
            'GENE': gene,
            'Sample_GT': gt,
            'Source': np.random.choice(['1000G', 'gnomAD', 'GWAS_Catalog'])
        })
    
    df = pd.DataFrame(variants)
    df = df.sort_values(['CHROM', 'POS'])
    
    return df


# End of module - # nrcdnl94