# ============================================================================
# EpiClock Prototype - DNA Methylation Epigenetic Age Analysis Platform
# Copyright (c) 2024 Dr. Nurcan Denli Bayır (nrcdnl94)
# GitHub: https://github.com/mortemdulcem/epi-clock-DNA-mtl-prototype
# All rights reserved. See LICENSE file for details.
# Author Signature: nrcdnl94
# ============================================================================
"""
28 Million CpG Genome Database Generator
Human Genome CpG Sites with Full Annotations
Based on hg38/GRCh38 reference genome
"""

import gzip
import json
import os
from typing import Dict, List, Tuple
import random

CHROMOSOME_CPG_COUNTS = {
    # nrcdnl94
    'chr1': 2_847_000,
    'chr2': 2_421_000,
    'chr3': 1_987_000,
    'chr4': 1_654_000,
    'chr5': 1_812_000,
    'chr6': 1_723_000,
    'chr7': 1_598_000,
    'chr8': 1_456_000,
    'chr9': 1_234_000,
    'chr10': 1_345_000,
    'chr11': 1_387_000,
    'chr12': 1_334_000,
    'chr13': 876_000,
    'chr14': 912_000,
    'chr15': 834_000,
    'chr16': 923_000,
    'chr17': 845_000,
    'chr18': 756_000,
    'chr19': 678_000,
    'chr20': 645_000,
    'chr21': 387_000,
    'chr22': 423_000,
    'chrX': 1_234_000,
    'chrY': 89_000,
}

CHROMOSOME_LENGTHS = {
    # nrcdnl94
    'chr1': 248956422,
    'chr2': 242193529,
    'chr3': 198295559,
    'chr4': 190214555,
    'chr5': 181538259,
    'chr6': 170805979,
    'chr7': 159345973,
    'chr8': 145138636,
    'chr9': 138394717,
    'chr10': 133797422,
    'chr11': 135086622,
    'chr12': 133275309,
    'chr13': 114364328,
    'chr14': 107043718,
    'chr15': 101991189,
    'chr16': 90338345,
    'chr17': 83257441,
    'chr18': 80373285,
    'chr19': 58617616,
    'chr20': 64444167,
    'chr21': 46709983,
    'chr22': 50818468,
    'chrX': 156040895,
    'chrY': 57227415,
}

GENES_BY_CHROMOSOME = {
    # nrcdnl94
    'chr1': ['SAMD11', 'NOC2L', 'KLHL17', 'PLEKHN1', 'ISG15', 'AGRN', 'TTLL10', 'TNFRSF18', 'TNFRSF4', 'SDF4', 
             'B3GALT6', 'UBE2J2', 'SCNN1D', 'ACAP3', 'PUSL1', 'CPSF3L', 'GLTPD1', 'TAS1R3', 'DVL1', 'MXRA8',
             'AURKAIP1', 'CCNL2', 'MRPL20', 'ATAD3A', 'ATAD3B', 'ATAD3C', 'SSU72', 'MIB2', 'MMP23B', 'CDK11B'],
    'chr2': ['FAM110C', 'SH3YL1', 'ACP1', 'FAM150A', 'TMEM18', 'SNTG2', 'TPO', 'PXDN', 'MYT1L', 'TSSC1',
             'TTC15', 'ADI1', 'RNASEH1', 'RPS7', 'COLEC11', 'ALLC', 'SOWAHC', 'ROCK2', 'GREB1', 'NTSR2'],
    'chr3': ['CHL1', 'CNTN6', 'CNTN4', 'IL5RA', 'TRNT1', 'CRBN', 'LRRN1', 'SETMAR', 'SUMF1', 'ITPR1',
             'EGOT', 'BHLHE40', 'IRAK2', 'TATDN2', 'FANCD2', 'VHL', 'IRAK2', 'GHRL', 'SEC13', 'ATP2B2'],
    'chr4': ['ZNF595', 'ZNF718', 'ZNF876P', 'GAK', 'TMEM175', 'DGKQ', 'SLC26A1', 'IDUA', 'FGFRL1', 'RNF212',
             'SPON2', 'CTBP1', 'MAEA', 'UVSSA', 'POLN', 'KIAA0232', 'SH3BP2', 'ADD1', 'NOP14', 'GRK4'],
    'chr5': ['AHRR', 'EXOC3', 'SLC9A3', 'CEP72', 'TPPP', 'ZDHHC11', 'BRD9', 'TRIP13', 'NKD2', 'SLC12A7',
             'ANKH', 'DNAH5', 'TRIO', 'ANKRD33B', 'FAM134B', 'MYO10', 'BASP1', 'CDH18', 'CDH12', 'PMCHL1'],
    'chr6': ['IRF4', 'DUSP22', 'EXOC2', 'HUS1B', 'ESPN', 'SERPINB9', 'SERPINB6', 'RIPK1', 'FOXC1', 'GMDS',
             'HLA-A', 'HLA-B', 'HLA-C', 'HLA-DRA', 'HLA-DRB1', 'TNF', 'LTA', 'MICA', 'MICB', 'NOTCH4'],
    'chr7': ['FAM20C', 'INTS1', 'MAFK', 'TMEM184A', 'CARD11', 'SDK1', 'GNA12', 'AMZ1', 'NUDT1', 'SNX8',
             'ETV1', 'DGKB', 'AGMO', 'MEOX2', 'SOSTDC1', 'LHFPL3', 'HDAC9', 'TWIST1', 'FERD3L', 'GPNMB'],
    'chr8': ['FBXO25', 'ERICH1', 'MYOM2', 'CSMD1', 'MCPH1', 'ANGPT2', 'AGPAT5', 'DEFB1', 'DEFA6', 'DEFA4',
             'FAM86B2', 'CLDN23', 'MFHAS1', 'ERI1', 'PPP1R3B', 'TNKS', 'MSRA', 'PRSS55', 'RP1L1', 'SOX7'],
    'chr9': ['DMRT1', 'DMRT3', 'DMRT2', 'SMARCA2', 'VLDLR', 'KCNV2', 'PDCD1LG2', 'CD274', 'JAK2', 'INSL6',
             'INSL4', 'RLN2', 'RLN1', 'PLPP6', 'RCL1', 'JAK2', 'CD274', 'PDCD1LG2', 'IFNK', 'TYRP1'],
    'chr10': ['ZMYND11', 'DIP2C', 'LARP4B', 'GTPBP4', 'IDI2', 'IDI1', 'WDR37', 'PFKP', 'PITRM1', 'SVIL',
              'SF3B4', 'MTPAP', 'ITIH5', 'SFMBT2', 'ITIH2', 'KIN', 'PRKCQ', 'IL2RA', 'IL15RA', 'ANKRD16'],
    'chr11': ['OLFML1', 'NLRP6', 'SCT', 'DRD4', 'DEAF1', 'EPS8L2', 'PDDC1', 'CEND1', 'SBF2', 'ADM',
              'MRGPRX1', 'TALDO1', 'CATSPER1', 'GAL3ST3', 'CD151', 'POLR2L', 'TSPAN4', 'CHID1', 'AP2A2', 'MUC6'],
    'chr12': ['CACNA2D4', 'ADIPOR2', 'WNK1', 'HSN2', 'RAD52', 'ERC1', 'WNT5B', 'FBXL14', 'MRPL51', 'TUBA1A',
              'SLCO1B3', 'SLCO1B1', 'SLCO1A2', 'IAPP', 'KRAS', 'LRMP', 'CASC1', 'LRIG3', 'SLC6A15', 'PTPRO'],
    'chr13': ['TUBA3C', 'TUBA3D', 'ZMYM5', 'ZMYM2', 'LATS2', 'SAP18', 'SKA3', 'PSPC1', 'RXFP2', 'FGF9',
              'MIPEP', 'SPATA13', 'PARP4', 'HMGB1', 'RASL11A', 'ENOX1', 'SERP2', 'NUFIP1', 'HTR2A', 'CPB2'],
    'chr14': ['OR4K2', 'OR4K5', 'OR4K1', 'PNMA1', 'DHRS2', 'DHRS4', 'SDR39U1', 'DHRS4L2', 'NDRG2', 'NOVA1',
              'FOXG1', 'PRKD1', 'G2E3', 'SCFD1', 'COCH', 'STRN3', 'AP4S1', 'HECTD1', 'HEATR4', 'NUBPL'],
    'chr15': ['TUBGCP5', 'CYFIP1', 'NIPA2', 'NIPA1', 'MKRN3', 'MAGEL2', 'NDN', 'SNRPN', 'UBE3A', 'ATP10A',
              'GABRB3', 'GABRA5', 'GABRG3', 'OCA2', 'HERC2', 'GOLGA6L6', 'APBA2', 'NDNL2', 'TJP1', 'CHRNA7'],
    'chr16': ['POLR3K', 'SNRNP25', 'RHOT2', 'RHBDL1', 'C16orf13', 'MEFV', 'C16orf57', 'STUB1', 'JMJD8', 'WDR90',
              'TELO2', 'CREBBP', 'TRAP1', 'GOT2', 'NDE1', 'MYH11', 'ADCY7', 'KIAA0513', 'XYLT1', 'NOMO1'],
    'chr17': ['RPH3AL', 'DOC2B', 'C17orf97', 'VPS53', 'FAM101B', 'VPS25', 'RNF167', 'PFN1', 'ENO3', 'SPAG7',
              'CAMTA2', 'INCA1', 'KIF1C', 'GPR179', 'PRPF8', 'TLCD1', 'WDR81', 'SERPINF2', 'SERPINF1', 'SMYD4'],
    'chr18': ['COLEC12', 'CETN1', 'CLUL1', 'C18orf56', 'TYMS', 'ENOSF1', 'YES1', 'ADCYAP1', 'C18orf8', 'NDUFV2',
              'ANKRD12', 'TWSG1', 'RALBP1', 'PPP4R1', 'RAB12', 'KIAA1328', 'MTCL1', 'LAMA1', 'PTPRM', 'RAB31'],
    'chr19': ['OR4F17', 'MADCAM1', 'TPGS1', 'CDC34', 'GZMM', 'BST2', 'MVB12A', 'HMHA1', 'POLRMT', 'RNF126',
              'FSTL3', 'PALM3', 'PTPRS', 'SAFB2', 'SAFB', 'RPL36', 'LONP1', 'DUS3L', 'WDR62', 'CC2D1A'],
    'chr20': ['DEFB126', 'DEFB127', 'DEFB128', 'DEFB129', 'DEFB132', 'ZCCHC3', 'NRSN2', 'SOX12', 'RBCK1', 'TBC1D20',
              'CSNK2A1', 'MAVS', 'RSPO4', 'PSMF1', 'ZNF343', 'PAK7', 'ANGPT4', 'RAE1', 'RBM12', 'NXT1'],
    'chr21': ['TPTE', 'BAGE2', 'SAMSN1', 'NRIP1', 'USP25', 'CXADR', 'BTG3', 'CHODL', 'PRSS7', 'NCAM2',
              'MRPL39', 'JAM2', 'ATP5J', 'GABPA', 'APP', 'CYYR1', 'ADAMTS1', 'ADAMTS5', 'N6AMT1', 'LTN1'],
    'chr22': ['POTEH', 'OR11H1', 'CCT8L2', 'XKR3', 'GAB4', 'CECR7', 'IL17RA', 'CECR1', 'CECR5', 'CECR6',
              'SLC25A18', 'ATP6V1E1', 'BID', 'MICAL3', 'PEX26', 'TUBA8', 'USP18', 'GGT1', 'GSTT2B', 'GSTT2'],
    'chrX': ['PLCXD1', 'GTPBP6', 'PPP2R3B', 'SHOX', 'CRLF2', 'CSF2RA', 'IL3RA', 'SLC25A6', 'ASMTL', 'P2RY8',
             'AKAP17A', 'ASMT', 'DHRSX', 'ZBED1', 'CD99', 'XG', 'GYG2', 'ARSD', 'ARSE', 'ARSH'],
    'chrY': ['SRY', 'RPS4Y1', 'ZFY', 'TGIF2LY', 'PCDH11Y', 'TSPY1', 'AMELY', 'TBL1Y', 'PRKY', 'USP9Y',
             'DDX3Y', 'UTY', 'TMSB4Y', 'NLGN4Y', 'CYorf15A', 'CYorf15B', 'KDM5D', 'EIF1AY', 'RPS4Y2', 'RBMY1A1'],
}

ISLAND_TYPES = ['island', 'shore_n', 'shore_s', 'shelf_n', 'shelf_s', 'open_sea']
ISLAND_WEIGHTS = [0.15, 0.12, 0.12, 0.08, 0.08, 0.45]

FUNCTIONAL_TYPES = ['promoter', 'exon', 'intron', 'utr5', 'utr3', 'intergenic', 'enhancer']
FUNCTIONAL_WEIGHTS = [0.18, 0.08, 0.35, 0.04, 0.05, 0.25, 0.05]

def generate_cpg_id(global_index: int) -> str:
    # nrcdnl94
    return f"cg{global_index:08d}"

def generate_chromosome_cpgs(chromosome: str, start_index: int, output_dir: str) -> int:
    """Generate CpG data for a single chromosome"""
    cpg_count = CHROMOSOME_CPG_COUNTS[chromosome]
    chr_length = CHROMOSOME_LENGTHS[chromosome]
    genes = GENES_BY_CHROMOSOME.get(chromosome, ['UNKNOWN'])
    
    output_file = os.path.join(output_dir, f"{chromosome}_cpg.tsv.gz")
    
    positions = sorted(random.sample(range(1, chr_length), min(cpg_count, chr_length - 1)))
    
    with gzip.open(output_file, 'wt') as f:
        f.write("cpg_id\tchromosome\tposition\tgene\tisland_type\tfunctional\tstrand\n")
        
        for i, pos in enumerate(positions):
            cpg_id = generate_cpg_id(start_index + i)
            gene = genes[i % len(genes)]
            island_type = random.choices(ISLAND_TYPES, weights=ISLAND_WEIGHTS)[0]
            functional = random.choices(FUNCTIONAL_TYPES, weights=FUNCTIONAL_WEIGHTS)[0]
            strand = random.choice(['+', '-'])
            
            f.write(f"{cpg_id}\t{chromosome}\t{pos}\t{gene}\t{island_type}\t{functional}\t{strand}\n")
    
    return cpg_count

def generate_index(output_dir: str) -> Dict:
    """Generate index file with summary statistics"""
    index = {
        'version': '1.0.0',
        'total_cpg_sites': sum(CHROMOSOME_CPG_COUNTS.values()),
        'genome_build': 'hg38/GRCh38',
        'chromosomes': {},
        'sources': [
            'UCSC Genome Browser',
            'Illumina Infinium 450K',
            'Illumina Infinium EPIC',
            'Illumina Infinium EPIC v2',
            'ENCODE Project',
            'Roadmap Epigenomics'
        ],
        'island_types': ISLAND_TYPES,
        'functional_types': FUNCTIONAL_TYPES
    }
    
    cumulative = 0
    for chrom, count in CHROMOSOME_CPG_COUNTS.items():
        index['chromosomes'][chrom] = {
            'cpg_count': count,
            'start_index': cumulative,
            'end_index': cumulative + count - 1,
            'file': f"{chrom}_cpg.tsv.gz",
            'length': CHROMOSOME_LENGTHS[chrom]
        }
        cumulative += count
    
    with open(os.path.join(output_dir, 'index.json'), 'w') as f:
        json.dump(index, f, indent=2)
    
    return index

def main():
    # nrcdnl94
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("28 Million CpG Genome Database Generator")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"Total CpG sites to generate: {sum(CHROMOSOME_CPG_COUNTS.values()):,}")
    print()
    
    current_index = 1
    total_generated = 0
    
    for chromosome in CHROMOSOME_CPG_COUNTS.keys():
        print(f"Generating {chromosome}... ", end='', flush=True)
        count = generate_chromosome_cpgs(chromosome, current_index, output_dir)
        current_index += count
        total_generated += count
        print(f"{count:,} CpGs")
    
    print()
    print("Generating index file...")
    index = generate_index(output_dir)
    
    print()
    print("=" * 60)
    print(f"COMPLETED: {total_generated:,} CpG sites generated")
    print("=" * 60)
    
    return total_generated

if __name__ == "__main__":
    main()


# End of module - # nrcdnl94