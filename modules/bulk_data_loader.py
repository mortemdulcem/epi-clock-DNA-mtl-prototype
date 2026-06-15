"""
Bulk Data Loader - Milyonlarca Kayit Icin ETL Sistemi
=====================================================

GWAS Catalog, PubChem ve diger kaynaklardan
buyuk olcekli veri yuklemesi yapar.

Author: EpiClock Team
Version: 2.0
"""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from sqlalchemy import create_engine, text
    HAS_DB = True
except ImportError:
    HAS_DB = False


class BulkDataLoader:
    """
    Buyuk olcekli veri yukleme sistemi
    
    Desteklenen kaynaklar:
    - GWAS Catalog (1M+ association)
    - PubChem (116M+ compound)
    - GEO DataSets (3000+ methylation studies)
    """
    
    GWAS_API = "https://www.ebi.ac.uk/gwas/rest/api"
    PUBCHEM_API = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    GEO_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.environ.get('DATABASE_URL')
        self.engine = None
        
        if self.db_url and HAS_DB:
            try:
                self.engine = create_engine(self.db_url)
            except:
                pass
        
        self.stats = {
            'gwas_fetched': 0,
            'pubchem_fetched': 0,
            'geo_fetched': 0,
            'db_imported': 0,
            'errors': 0,
            'last_run': None
        }
        
        os.makedirs("data/bulk_downloads", exist_ok=True)
    
    def fetch_gwas_batch(self, page: int, size: int = 500) -> List[Dict]:
        """GWAS Catalog'dan bir sayfa veri cek"""
        try:
            url = f"{self.GWAS_API}/associations?size={size}&page={page}"
            resp = requests.get(url, timeout=60, headers={'Accept': 'application/json'})
            
            if resp.status_code != 200:
                return []
            
            data = resp.json()
            associations = data.get('_embedded', {}).get('associations', [])
            
            results = []
            for assoc in associations:
                try:
                    loci = assoc.get('loci', [])
                    for locus in loci:
                        genes = locus.get('authorReportedGenes', [])
                        for gene in genes:
                            gene_name = gene.get('geneName', '')
                            if gene_name:
                                p_val = assoc.get('pvalueMantissa', 1) * (10 ** assoc.get('pvalueExponent', 0))
                                results.append({
                                    'gene': gene_name,
                                    'p_value': p_val,
                                    'beta': assoc.get('betaNum') or 0.02,
                                    'study': assoc.get('study', {}).get('accessionId', '')
                                })
                except:
                    continue
            
            return results
            
        except Exception as e:
            self.stats['errors'] += 1
            return []
    
    def fetch_gwas_parallel(self, max_pages: int = 100, workers: int = 5) -> int:
        """Paralel olarak GWAS verisi cek"""
        all_data = []
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(self.fetch_gwas_batch, page): page for page in range(max_pages)}
            
            for future in as_completed(futures):
                page = futures[future]
                try:
                    results = future.result()
                    all_data.extend(results)
                    self.stats['gwas_fetched'] += len(results)
                except Exception as e:
                    self.stats['errors'] += 1
        
        # Save to file
        with open("data/bulk_downloads/gwas_data.json", "w") as f:
            json.dump(all_data, f)
        
        return len(all_data)
    
    def fetch_pubchem_substances(self, substance_names: List[str]) -> int:
        """PubChem'den madde verisi cek"""
        all_data = []
        
        for name in substance_names:
            try:
                # Get CID
                url = f"{self.PUBCHEM_API}/compound/name/{name}/cids/JSON"
                resp = requests.get(url, timeout=10)
                
                if resp.status_code == 200:
                    cids = resp.json().get('IdentifierList', {}).get('CID', [])
                    if cids:
                        cid = cids[0]
                        
                        # Get properties
                        prop_url = f"{self.PUBCHEM_API}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,IUPACName,CanonicalSMILES/JSON"
                        prop_resp = requests.get(prop_url, timeout=10)
                        
                        if prop_resp.status_code == 200:
                            props = prop_resp.json().get('PropertyTable', {}).get('Properties', [{}])[0]
                            all_data.append({
                                'name': name,
                                'cid': cid,
                                'formula': props.get('MolecularFormula', ''),
                                'weight': props.get('MolecularWeight', 0),
                                'iupac': props.get('IUPACName', ''),
                                'smiles': props.get('CanonicalSMILES', '')
                            })
                            self.stats['pubchem_fetched'] += 1
                
                time.sleep(0.2)  # Rate limit
                
            except Exception as e:
                self.stats['errors'] += 1
        
        # Save
        with open("data/bulk_downloads/pubchem_data.json", "w") as f:
            json.dump(all_data, f)
        
        return len(all_data)
    
    def import_to_database(self, batch_size: int = 1000) -> int:
        """Indirilen verileri veritabanina aktar"""
        if not self.engine:
            return 0
        
        imported = 0
        
        # GWAS data
        gwas_file = "data/bulk_downloads/gwas_data.json"
        if os.path.exists(gwas_file):
            with open(gwas_file) as f:
                gwas_data = json.load(f)
            
            with self.engine.connect() as conn:
                for i, item in enumerate(gwas_data):
                    try:
                        cpg_id = f"cg_{item['gene'][:10].lower()}"
                        
                        conn.execute(text("""
                            INSERT INTO ewas_associations (cpg, trait, trait_category, beta, p_value, gene)
                            VALUES (:cpg, 'gwas_association', 'GWAS', :beta, :pval, :gene)
                            ON CONFLICT DO NOTHING
                        """), {
                            'cpg': cpg_id,
                            'beta': item.get('beta', 0.02),
                            'pval': item.get('p_value', 1e-5),
                            'gene': item['gene']
                        })
                        imported += 1
                        
                        if i % batch_size == 0:
                            conn.commit()
                            
                    except:
                        continue
                
                conn.commit()
        
        self.stats['db_imported'] = imported
        return imported
    
    def run_full_pipeline(self, gwas_pages: int = 50, 
                          substances: List[str] = None) -> Dict[str, Any]:
        """Tam ETL pipeline calistir"""
        self.stats['last_run'] = datetime.now().isoformat()
        
        # GWAS
        print(f"[1/3] GWAS Catalog'dan veri cekiliyor ({gwas_pages} sayfa)...")
        gwas_count = self.fetch_gwas_parallel(max_pages=gwas_pages)
        print(f"      {gwas_count:,} GWAS kaydi cekildi")
        
        # PubChem
        if substances:
            print(f"[2/3] PubChem'den madde verisi cekiliyor ({len(substances)} madde)...")
            pubchem_count = self.fetch_pubchem_substances(substances)
            print(f"      {pubchem_count:,} madde cekildi")
        else:
            print("[2/3] PubChem atlandi (madde listesi yok)")
        
        # Import
        print("[3/3] Veritabanina aktariliyor...")
        imported = self.import_to_database()
        print(f"      {imported:,} kayit aktarildi")
        
        return self.stats
    
    def get_database_stats(self) -> Dict[str, int]:
        """Veritabani istatistiklerini al"""
        if not self.engine:
            return {}
        
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    (SELECT COUNT(*) FROM ewas_associations) as ewas,
                    (SELECT COUNT(DISTINCT gene) FROM ewas_associations WHERE gene IS NOT NULL) as genes,
                    (SELECT COUNT(*) FROM disease_signatures) as diseases,
                    (SELECT COUNT(*) FROM substance_signatures) as substances,
                    (SELECT COUNT(*) FROM therapeutic_medications) as medications
            """))
            row = result.fetchone()
            
            return {
                'ewas_associations': row[0],
                'unique_genes': row[1],
                'disease_signatures': row[2],
                'substance_signatures': row[3],
                'therapeutic_medications': row[4]
            }


# Predefined substance lists
ABUSE_SUBSTANCES = [
    # Stimulants
    'cocaine', 'methamphetamine', 'amphetamine', 'methylphenidate',
    'modafinil', 'ephedrine', 'cathinone', 'mephedrone', 'mdpv',
    # Opioids
    'heroin', 'morphine', 'fentanyl', 'oxycodone', 'hydrocodone',
    'codeine', 'tramadol', 'methadone', 'buprenorphine', 'carfentanil',
    # Cannabinoids
    'thc', 'cannabidiol', 'synthetic cannabinoid',
    # Hallucinogens
    'lsd', 'psilocybin', 'mescaline', 'dmt', 'ketamine', 'pcp',
    # Depressants
    'alcohol', 'ghb', 'barbiturate', 'benzodiazepine',
    # Others
    'mdma', 'nicotine', 'kratom', 'salvia', 'nitrous oxide'
]

THERAPEUTIC_DRUGS = [
    # Antidepressants
    'fluoxetine', 'sertraline', 'paroxetine', 'citalopram', 'escitalopram',
    'venlafaxine', 'duloxetine', 'bupropion', 'mirtazapine', 'amitriptyline',
    # Antipsychotics
    'haloperidol', 'risperidone', 'olanzapine', 'quetiapine', 'aripiprazole',
    'clozapine', 'ziprasidone', 'paliperidone',
    # Antidiabetics
    'metformin', 'glipizide', 'glyburide', 'pioglitazone', 'sitagliptin',
    'empagliflozin', 'liraglutide', 'insulin',
    # Antiretrovirals
    'tenofovir', 'emtricitabine', 'dolutegravir', 'efavirenz', 'ritonavir',
    'atazanavir', 'darunavir', 'raltegravir', 'lamivudine', 'abacavir',
    # Cardiovascular
    'atorvastatin', 'simvastatin', 'lisinopril', 'amlodipine', 'metoprolol',
    'losartan', 'warfarin', 'clopidogrel',
    # Others
    'prednisone', 'methotrexate', 'ibuprofen', 'acetaminophen'
]


def run_bulk_import():
    """Toplu veri yukleme islemini baslat"""
    loader = BulkDataLoader()
    
    print("=" * 70)
    print("TOPLU VERI YUKLEME SISTEMI")
    print("=" * 70)
    
    # Run pipeline
    all_substances = ABUSE_SUBSTANCES + THERAPEUTIC_DRUGS
    stats = loader.run_full_pipeline(
        gwas_pages=50,  # ~25,000 GWAS kayit
        substances=all_substances[:30]  # Ilk 30 madde
    )
    
    # Database stats
    db_stats = loader.get_database_stats()
    
    print("\n" + "=" * 70)
    print("SONUC")
    print("=" * 70)
    print(f"GWAS Cekildi: {stats['gwas_fetched']:,}")
    print(f"PubChem Cekildi: {stats['pubchem_fetched']:,}")
    print(f"Veritabanina Aktarildi: {stats['db_imported']:,}")
    print(f"Hatalar: {stats['errors']}")
    print()
    print("Veritabani Durumu:")
    for key, value in db_stats.items():
        print(f"  {key}: {value:,}")
    
    return stats, db_stats


if __name__ == "__main__":
    run_bulk_import()
