# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
CpG Genome Search Module
Fast search and lookup for 29.4 million CpG sites
"""

import gzip
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
# nrcdnl94
class CpGSite:
    # nrcdnl94
    cpg_id: str
    chromosome: str
    position: int
    gene: str
    island_type: str
    functional: str
    strand: str

class CpGGenomeDatabase:
    # nrcdnl94
    """29.4 Million CpG Genome Database"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.index = self._load_index()
        self._cache = {}
    
    def _load_index(self) -> Dict:
        """Load the index file"""
        index_path = os.path.join(self.base_dir, 'index.json')
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        return {
            'total_cpg_sites': self.index.get('total_cpg_sites', 0),
            'genome_build': self.index.get('genome_build', 'hg38'),
            'chromosomes': len(self.index.get('chromosomes', {})),
            'sources': self.index.get('sources', []),
            'island_types': self.index.get('island_types', []),
            'functional_types': self.index.get('functional_types', [])
        }
    
    def get_chromosome_stats(self) -> Dict[str, Dict]:
        """Get per-chromosome statistics"""
        return self.index.get('chromosomes', {})
    
    def search_by_id(self, cpg_id: str) -> Optional[CpGSite]:
        """Search for a specific CpG by ID"""
        try:
            cpg_num = int(cpg_id.replace('cg', ''))
        except ValueError:
            return None
        
        for chrom, info in self.index.get('chromosomes', {}).items():
            if info['start_index'] <= cpg_num <= info['end_index']:
                return self._search_in_chromosome(chrom, cpg_id)
        
        return None
    
    def search_by_position(self, chromosome: str, start: int, end: int, limit: int = 1000) -> List[CpGSite]:
        """Search CpGs by genomic position range"""
        results = []
        
        chrom_key = chromosome if chromosome.startswith('chr') else f'chr{chromosome}'
        
        if chrom_key not in self.index.get('chromosomes', {}):
            return results
        
        file_path = os.path.join(self.base_dir, f"{chrom_key}_cpg.tsv.gz")
        
        if not os.path.exists(file_path):
            return results
        
        with gzip.open(file_path, 'rt') as f:
            next(f)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    pos = int(parts[2])
                    if start <= pos <= end:
                        results.append(CpGSite(
                            cpg_id=parts[0],
                            chromosome=parts[1],
                            position=pos,
                            gene=parts[3],
                            island_type=parts[4],
                            functional=parts[5],
                            strand=parts[6]
                        ))
                        if len(results) >= limit:
                            break
                    elif pos > end:
                        break
        
        return results
    
    def search_by_gene(self, gene_name: str, limit: int = 1000) -> List[CpGSite]:
        """Search CpGs by gene name"""
        results = []
        gene_upper = gene_name.upper()
        
        for chrom in self.index.get('chromosomes', {}).keys():
            file_path = os.path.join(self.base_dir, f"{chrom}_cpg.tsv.gz")
            
            if not os.path.exists(file_path):
                continue
            
            with gzip.open(file_path, 'rt') as f:
                next(f)
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 7 and parts[3].upper() == gene_upper:
                        results.append(CpGSite(
                            cpg_id=parts[0],
                            chromosome=parts[1],
                            position=int(parts[2]),
                            gene=parts[3],
                            island_type=parts[4],
                            functional=parts[5],
                            strand=parts[6]
                        ))
                        if len(results) >= limit:
                            return results
        
        return results
    
    def get_sample_cpgs(self, chromosome: str, count: int = 100) -> List[CpGSite]:
        """Get sample CpGs from a chromosome"""
        results = []
        
        chrom_key = chromosome if chromosome.startswith('chr') else f'chr{chromosome}'
        file_path = os.path.join(self.base_dir, f"{chrom_key}_cpg.tsv.gz")
        
        if not os.path.exists(file_path):
            return results
        
        with gzip.open(file_path, 'rt') as f:
            next(f)
            for i, line in enumerate(f):
                if i >= count:
                    break
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    results.append(CpGSite(
                        cpg_id=parts[0],
                        chromosome=parts[1],
                        position=int(parts[2]),
                        gene=parts[3],
                        island_type=parts[4],
                        functional=parts[5],
                        strand=parts[6]
                    ))
        
        return results
    
    def _search_in_chromosome(self, chromosome: str, cpg_id: str) -> Optional[CpGSite]:
        """Search for a CpG ID in a specific chromosome file"""
        file_path = os.path.join(self.base_dir, f"{chromosome}_cpg.tsv.gz")
        
        if not os.path.exists(file_path):
            return None
        
        with gzip.open(file_path, 'rt') as f:
            next(f)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 7 and parts[0] == cpg_id:
                    return CpGSite(
                        cpg_id=parts[0],
                        chromosome=parts[1],
                        position=int(parts[2]),
                        gene=parts[3],
                        island_type=parts[4],
                        functional=parts[5],
                        strand=parts[6]
                    )
        
        return None
    
    def get_island_type_distribution(self, chromosome: str = None) -> Dict[str, int]:
        """Get distribution of CpG island types"""
        distribution = {}
        
        chromosomes = [chromosome] if chromosome else list(self.index.get('chromosomes', {}).keys())
        
        for chrom in chromosomes[:3]:
            file_path = os.path.join(self.base_dir, f"{chrom}_cpg.tsv.gz")
            
            if not os.path.exists(file_path):
                continue
            
            with gzip.open(file_path, 'rt') as f:
                next(f)
                for i, line in enumerate(f):
                    if i >= 10000:
                        break
                    parts = line.strip().split('\t')
                    if len(parts) >= 5:
                        island_type = parts[4]
                        distribution[island_type] = distribution.get(island_type, 0) + 1
        
        return distribution
    
    def get_functional_distribution(self, chromosome: str = None) -> Dict[str, int]:
        """Get distribution of functional types"""
        distribution = {}
        
        chromosomes = [chromosome] if chromosome else list(self.index.get('chromosomes', {}).keys())
        
        for chrom in chromosomes[:3]:
            file_path = os.path.join(self.base_dir, f"{chrom}_cpg.tsv.gz")
            
            if not os.path.exists(file_path):
                continue
            
            with gzip.open(file_path, 'rt') as f:
                next(f)
                for i, line in enumerate(f):
                    if i >= 10000:
                        break
                    parts = line.strip().split('\t')
                    if len(parts) >= 6:
                        functional = parts[5]
                        distribution[functional] = distribution.get(functional, 0) + 1
        
        return distribution


_database_instance = None

def get_cpg_genome_database() -> CpGGenomeDatabase:
    """Get singleton instance of CpG Genome Database"""
    global _database_instance
    if _database_instance is None:
        _database_instance = CpGGenomeDatabase()
    return _database_instance

def get_total_cpg_count() -> int:
    """Get total CpG count"""
    db = get_cpg_genome_database()
    return db.get_statistics()['total_cpg_sites']

def search_cpg_by_id(cpg_id: str) -> Optional[Dict]:
    """Search CpG by ID and return as dict"""
    db = get_cpg_genome_database()
    result = db.search_by_id(cpg_id)
    if result:
        return {
            'cpg_id': result.cpg_id,
            'chromosome': result.chromosome,
            'position': result.position,
            'gene': result.gene,
            'island_type': result.island_type,
            'functional': result.functional,
            'strand': result.strand
        }
    return None

def search_cpg_by_region(chromosome: str, start: int, end: int, limit: int = 1000) -> List[Dict]:
    """Search CpGs by genomic region"""
    db = get_cpg_genome_database()
    results = db.search_by_position(chromosome, start, end, limit)
    return [{
        'cpg_id': r.cpg_id,
        'chromosome': r.chromosome,
        'position': r.position,
        'gene': r.gene,
        'island_type': r.island_type,
        'functional': r.functional,
        'strand': r.strand
    } for r in results]

def search_cpg_by_gene(gene_name: str, limit: int = 1000) -> List[Dict]:
    """Search CpGs by gene name"""
    db = get_cpg_genome_database()
    results = db.search_by_gene(gene_name, limit)
    return [{
        'cpg_id': r.cpg_id,
        'chromosome': r.chromosome,
        'position': r.position,
        'gene': r.gene,
        'island_type': r.island_type,
        'functional': r.functional,
        'strand': r.strand
    } for r in results]


if __name__ == "__main__":
    db = get_cpg_genome_database()
    
    print("=" * 60)
    print("CpG Genome Database Statistics")
    print("=" * 60)
    
    stats = db.get_statistics()
    print(f"Total CpG Sites: {stats['total_cpg_sites']:,}")
    print(f"Genome Build: {stats['genome_build']}")
    print(f"Chromosomes: {stats['chromosomes']}")
    print(f"Sources: {', '.join(stats['sources'])}")
    
    print("\nPer-chromosome CpG counts:")
    for chrom, info in db.get_chromosome_stats().items():
        print(f"  {chrom}: {info['cpg_count']:,}")
    
    print("\nSample search by ID:")
    result = db.search_by_id('cg00000100')
    if result:
        print(f"  {result.cpg_id}: {result.chromosome}:{result.position} - {result.gene}")
    
    print("\nSample CpGs from chr1:")
    samples = db.get_sample_cpgs('chr1', 5)
    for s in samples:
        print(f"  {s.cpg_id}: {s.chromosome}:{s.position} - {s.gene} ({s.functional})")


# End of module - # nrcdnl94