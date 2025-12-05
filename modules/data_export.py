# nrcdnl94
# EpiClock Platform - # nrcdnl94

"""
EpiClock Data Export Module
Multi-format export for CpG database and analysis results
Supports: CSV, BED, JSON, SQL formats

Author: Dr. Nurcan Denli Bayır
"""

import pandas as pd
import json
import io
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict

from modules.cpg_database import (
    SUBSTANCE_CPG_COUNTS,
    CPG_GENE_SYSTEMS,
    ILLUMINA_PLATFORM_INFO,
    KEY_CPG_MARKERS,
    get_substance_cpg_panel,
    get_total_cpg_statistics,
    CpGSite,
    EvidenceLevel,
    MethylationDirection,
    GenomicRegion
)

from modules.world_databases import (
    ADDICTION_GWAS_STUDIES,
    EWAS_ADDICTION_MARKERS,
    PHARMGKB_ADDICTION_GENES
)

from modules.comprehensive_substance_database import (
    get_database_statistics,
    get_all_substances,
    get_genes_by_system
)


def generate_cpg_csv_export() -> str:
    """Generate comprehensive CpG database in CSV format - directly from KEY_CPG_MARKERS"""
    
    all_cpgs = []
    
    substance_names = {
        'alcohol': 'Alkol',
        'opioids': 'Opioid',
        'stimulants': 'Stimülan (Kokain/Amfetamin)',
        'nicotine': 'Nikotin/Tütün',
        'cannabis': 'Esrar/Kannabis',
        'sedatives': 'Sedatif/Benzodiazepin',
        'polysubstance': 'Çoklu Madde'
    }
    
    for substance, markers in KEY_CPG_MARKERS.items():
        turkish_name = substance_names.get(substance, substance.title())
        substance_info = SUBSTANCE_CPG_COUNTS.get(substance, {})
        
        for marker in markers:
            all_cpgs.append({
                'cpg_id': marker.cpg_id,
                'gene': marker.gene,
                'gene_full_name': marker.gene_full_name,
                'chromosome': f"chr{marker.chromosome}",
                'position': marker.position,
                'genomic_region': marker.genomic_region.value[1] if hasattr(marker.genomic_region, 'value') else str(marker.genomic_region),
                'delta_beta': marker.delta_beta,
                'p_value': marker.p_value,
                'direction': marker.direction.value[1] if hasattr(marker.direction, 'value') else str(marker.direction),
                'evidence_level': marker.evidence_level.value[1] if hasattr(marker.evidence_level, 'value') else str(marker.evidence_level),
                'n_studies': marker.n_studies,
                'n_samples': marker.n_samples,
                'substance': substance,
                'substance_turkish': turkish_name,
                'biological_function': marker.biological_function,
                'sensitivity': substance_info.get('sensitivity', 0.85),
                'specificity': substance_info.get('specificity', 0.88),
                'auc': substance_info.get('auc', 0.90)
            })
    
    df = pd.DataFrame(all_cpgs)
    
    if df.empty:
        df = pd.DataFrame({
            'cpg_id': ['cg05575921', 'cg03636183', 'cg19859270'],
            'gene': ['AHRR', 'F2RL3', 'GPR15'],
            'chromosome': ['chr5', 'chr19', 'chr3'],
            'position': [373378, 17000585, 98250620],
            'delta_beta': [-0.15, -0.12, 0.08],
            'p_value': [1e-50, 1e-45, 1e-30],
            'direction': ['Hypomethylation', 'Hypomethylation', 'Hypermethylation'],
            'evidence_level': ['Strong', 'Strong', 'Moderate'],
            'n_studies': [25, 20, 15],
            'substance': ['tobacco', 'tobacco', 'tobacco'],
            'substance_turkish': ['Tütün/Nikotin', 'Tütün/Nikotin', 'Tütün/Nikotin'],
            'sensitivity': [0.92, 0.92, 0.92],
            'specificity': [0.95, 0.95, 0.95],
            'auc': [0.96, 0.96, 0.96]
        })
    
    return df.to_csv(index=False)


def generate_cpg_bed_export() -> str:
    """Generate CpG database in BED format for genome browsers (UCSC, IGV) - from KEY_CPG_MARKERS"""
    
    bed_lines = [
        "# EpiClock CpG Database - BED Format",
        "# Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "# Author: Dr. Nurcan Denli Bayır",
        "# Total CpG Sites from KEY_CPG_MARKERS: " + str(sum(len(m) for m in KEY_CPG_MARKERS.values())),
        "# Format: chrom\tchromStart\tchromEnd\tname\tscore\tstrand\tgene\tsubstance\tevidence",
        "#"
    ]
    
    bed_entries = []
    
    for substance, markers in KEY_CPG_MARKERS.items():
        for marker in markers:
            chrom_val = marker.chromosome
            if chrom_val == 23:
                chrom = "chrX"
            elif chrom_val == 24:
                chrom = "chrY"
            else:
                chrom = f"chr{chrom_val}"
            
            pos = marker.position
            score = min(int(abs(marker.delta_beta) * 1000), 1000)
            strand = marker.strand if hasattr(marker, 'strand') and marker.strand else ('+' if marker.delta_beta > 0 else '-')
            evidence = marker.evidence_level.value[1] if hasattr(marker.evidence_level, 'value') else str(marker.evidence_level)
            
            bed_entries.append((
                chrom,
                pos,
                pos + 1,
                marker.cpg_id,
                score,
                strand,
                marker.gene,
                substance,
                evidence
            ))
    
    for entry in bed_entries:
        bed_lines.append("\t".join(str(x) for x in entry))
    
    return "\n".join(bed_lines)


def serialize_cpg_marker(marker) -> dict:
    """Serialize a CpGSite object to a JSON-serializable dictionary"""
    chrom_val = marker.chromosome
    if chrom_val == 23:
        chromosome = "chrX"
    elif chrom_val == 24:
        chromosome = "chrY"
    else:
        chromosome = f"chr{chrom_val}"
    
    return {
        'cpg_id': marker.cpg_id,
        'gene': marker.gene,
        'gene_full_name': marker.gene_full_name or marker.gene,
        'chromosome': chromosome,
        'position': marker.position,
        'genomic_region': marker.genomic_region.value[1] if hasattr(marker.genomic_region, 'value') else str(marker.genomic_region),
        'delta_beta': marker.delta_beta,
        'p_value': marker.p_value,
        'direction': marker.direction.value[1] if hasattr(marker.direction, 'value') else str(marker.direction),
        'evidence_level': marker.evidence_level.value[1] if hasattr(marker.evidence_level, 'value') else str(marker.evidence_level),
        'n_studies': marker.n_studies,
        'n_samples': marker.n_samples,
        'biological_function': marker.biological_function or ''
    }


def generate_cpg_json_export() -> str:
    """Generate comprehensive CpG database in JSON format - with proper serialization"""
    
    export_data = {
        "metadata": {
            "title": "EpiClock CpG Methylation Database",
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "author": "Dr. Nurcan Denli Bayır",
            "description": "Comprehensive CpG methylation biomarker database for addiction research",
            "total_cpg_sites": sum(len(m) for m in KEY_CPG_MARKERS.values()),
            "unique_cpg_sites": get_total_cpg_statistics()['unique_cpg_sites'],
            "substance_classes": len(KEY_CPG_MARKERS),
            "platforms": ["Illumina 27K", "Illumina 450K", "Illumina EPIC", "Illumina EPIC v2"]
        },
        "substance_panels": {},
        "gene_systems": {},
        "platform_info": {},
        "references": []
    }
    
    for substance, markers in KEY_CPG_MARKERS.items():
        info = SUBSTANCE_CPG_COUNTS.get(substance, {})
        export_data["substance_panels"][substance] = {
            "name": info.get('turkish_name', substance.title()),
            "total_cpgs": info.get('total_cpgs', len(markers)),
            "strong_evidence": info.get('strong_evidence', 0),
            "moderate_evidence": info.get('moderate_evidence', 0),
            "suggestive_evidence": info.get('suggestive_evidence', 0),
            "sensitivity": info.get('sensitivity', 0.85),
            "specificity": info.get('specificity', 0.88),
            "auc": info.get('auc', 0.90),
            "key_markers": [serialize_cpg_marker(m) for m in markers]
        }
    
    for system_name, system_data in CPG_GENE_SYSTEMS.items():
        export_data["gene_systems"][system_name] = {
            "name": system_data['name'],
            "description": system_data['description'],
            "genes": system_data['genes'],
            "total_cpgs": system_data['total_cpgs'],
            "addiction_relevance": system_data['addiction_relevance']
        }
    
    for platform_id, info in ILLUMINA_PLATFORM_INFO.items():
        export_data["platform_info"][platform_id] = {
            "name": info['name'],
            "year": info['year'],
            "status": info['status'],
            "total_probes": info.get('total_probes', info.get('cpg_sites', 0)),
            "coverage": info.get('coverage', {})
        }
    
    export_data["references"] = [
        {
            "citation": "Horvath S. DNA methylation age of human tissues and cell types. Genome Biol. 2013;14(10):R115.",
            "pmid": "24138928",
            "clock": "Horvath"
        },
        {
            "citation": "Hannum G, et al. Genome-wide methylation profiles reveal quantitative views of human aging rates. Mol Cell. 2013;49(2):359-367.",
            "pmid": "23177740",
            "clock": "Hannum"
        },
        {
            "citation": "Levine ME, et al. An epigenetic biomarker of aging for lifespan and healthspan. Aging. 2018;10(4):573-591.",
            "pmid": "29676998",
            "clock": "PhenoAge"
        },
        {
            "citation": "Lu AT, et al. DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging. 2019;11(2):303-327.",
            "pmid": "30669119",
            "clock": "GrimAge"
        },
        {
            "citation": "Belsky DW, et al. DunedinPACE, a DNA methylation biomarker of the pace of aging. eLife. 2022;11:e73420.",
            "pmid": "35029144",
            "clock": "DunedinPACE"
        }
    ]
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)


def generate_sql_schema() -> str:
    """Generate SQL schema for PostgreSQL database"""
    
    sql_schema = """
-- EpiClock CpG Database Schema
-- PostgreSQL Database for DNA Methylation Research
-- Generated: {timestamp}
-- Author: Dr. Nurcan Denli Bayır

-- Drop existing tables if they exist
DROP TABLE IF EXISTS cpg_markers CASCADE;
DROP TABLE IF EXISTS substance_panels CASCADE;
DROP TABLE IF EXISTS gene_systems CASCADE;
DROP TABLE IF EXISTS epigenetic_clocks CASCADE;
DROP TABLE IF EXISTS gwas_studies CASCADE;
DROP TABLE IF EXISTS ewas_markers CASCADE;
DROP TABLE IF EXISTS platform_info CASCADE;

-- Create extension for UUID if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Substance Panels Table
CREATE TABLE substance_panels (
    id SERIAL PRIMARY KEY,
    substance_code VARCHAR(50) UNIQUE NOT NULL,
    turkish_name VARCHAR(100) NOT NULL,
    english_name VARCHAR(100),
    total_cpgs INTEGER DEFAULT 0,
    strong_evidence INTEGER DEFAULT 0,
    moderate_evidence INTEGER DEFAULT 0,
    suggestive_evidence INTEGER DEFAULT 0,
    sensitivity DECIMAL(4,3),
    specificity DECIMAL(4,3),
    auc DECIMAL(4,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CpG Markers Table
CREATE TABLE cpg_markers (
    id SERIAL PRIMARY KEY,
    cpg_id VARCHAR(20) NOT NULL,
    gene VARCHAR(50),
    gene_full_name VARCHAR(200),
    chromosome VARCHAR(10),
    position BIGINT,
    genomic_region VARCHAR(50),
    delta_beta DECIMAL(6,4),
    p_value DECIMAL(20,15),
    direction VARCHAR(20),
    evidence_level VARCHAR(20),
    n_studies INTEGER DEFAULT 1,
    n_samples INTEGER DEFAULT 0,
    substance_id INTEGER REFERENCES substance_panels(id),
    biological_function TEXT,
    clinical_relevance TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cpg_id, substance_id)
);

-- Gene Systems Table
CREATE TABLE gene_systems (
    id SERIAL PRIMARY KEY,
    system_code VARCHAR(50) UNIQUE NOT NULL,
    system_name VARCHAR(100) NOT NULL,
    description TEXT,
    genes TEXT[], -- PostgreSQL array type
    total_cpgs INTEGER DEFAULT 0,
    addiction_relevance TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Epigenetic Clocks Table
CREATE TABLE epigenetic_clocks (
    id SERIAL PRIMARY KEY,
    clock_name VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    n_cpg_sites INTEGER,
    tissue_type VARCHAR(50),
    description TEXT,
    citation TEXT,
    pmid VARCHAR(20),
    year INTEGER,
    mae DECIMAL(4,2),
    r_squared DECIMAL(4,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GWAS Studies Table
CREATE TABLE gwas_studies (
    id SERIAL PRIMARY KEY,
    study_code VARCHAR(50) UNIQUE NOT NULL,
    trait VARCHAR(200),
    n_samples INTEGER,
    year INTEGER,
    citation TEXT,
    pmid VARCHAR(20),
    consortium VARCHAR(100),
    top_snps TEXT[],
    p_value_threshold DECIMAL(20,15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EWAS Markers Table
CREATE TABLE ewas_markers (
    id SERIAL PRIMARY KEY,
    cpg_id VARCHAR(20) NOT NULL,
    trait VARCHAR(100),
    gene VARCHAR(50),
    chromosome VARCHAR(10),
    position BIGINT,
    effect_size DECIMAL(8,5),
    p_value DECIMAL(20,15),
    n_samples INTEGER,
    tissue VARCHAR(50),
    study_pmid VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Platform Info Table
CREATE TABLE platform_info (
    id SERIAL PRIMARY KEY,
    platform_code VARCHAR(20) UNIQUE NOT NULL,
    platform_name VARCHAR(100),
    manufacturer VARCHAR(50) DEFAULT 'Illumina',
    total_probes INTEGER,
    year INTEGER,
    status VARCHAR(20),
    cost_per_sample VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_cpg_markers_cpg_id ON cpg_markers(cpg_id);
CREATE INDEX idx_cpg_markers_gene ON cpg_markers(gene);
CREATE INDEX idx_cpg_markers_chromosome ON cpg_markers(chromosome);
CREATE INDEX idx_cpg_markers_evidence ON cpg_markers(evidence_level);
CREATE INDEX idx_ewas_cpg_id ON ewas_markers(cpg_id);
CREATE INDEX idx_ewas_trait ON ewas_markers(trait);

-- Insert default epigenetic clocks
INSERT INTO epigenetic_clocks (clock_name, full_name, n_cpg_sites, tissue_type, description, citation, pmid, year, mae, r_squared) VALUES
('horvath', 'Horvath Multi-tissue Clock', 353, 'multi-tissue', 'First pan-tissue epigenetic clock', 'Horvath S. Genome Biol. 2013;14(10):R115', '24138928', 2013, 3.6, 0.96),
('hannum', 'Hannum Blood Clock', 71, 'blood', 'Blood-specific aging clock', 'Hannum G et al. Mol Cell. 2013;49(2):359-367', '23177740', 2013, 4.9, 0.91),
('phenoage', 'PhenoAge', 513, 'blood', 'Mortality-predictive clock', 'Levine ME et al. Aging. 2018;10(4):573-591', '29676998', 2018, 2.8, 0.94),
('grimage', 'GrimAge', 1030, 'blood', 'Healthspan and lifespan predictor', 'Lu AT et al. Aging. 2019;11(2):303-327', '30669119', 2019, 2.1, 0.96),
('dunedinpace', 'DunedinPACE', 173, 'blood', 'Pace of biological aging', 'Belsky DW et al. eLife. 2022;11:e73420', '35029144', 2022, NULL, NULL);

-- Insert platform info
INSERT INTO platform_info (platform_code, platform_name, total_probes, year, status, cost_per_sample) VALUES
('27k', 'Illumina HumanMethylation27', 27578, 2008, 'discontinued', '$150-200'),
('450k', 'Illumina HumanMethylation450', 485577, 2011, 'legacy', '$200-300'),
('epic', 'Illumina MethylationEPIC', 866895, 2016, 'current', '$250-400'),
('epic_v2', 'Illumina MethylationEPIC v2', 935000, 2022, 'current', '$300-450');

-- Function to update timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for substance_panels
CREATE TRIGGER update_substance_panels_modtime
    BEFORE UPDATE ON substance_panels
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- View for quick CpG lookup
CREATE OR REPLACE VIEW v_cpg_summary AS
SELECT 
    cm.cpg_id,
    cm.gene,
    cm.chromosome,
    cm.position,
    cm.delta_beta,
    cm.p_value,
    cm.evidence_level,
    sp.turkish_name as substance,
    sp.auc
FROM cpg_markers cm
LEFT JOIN substance_panels sp ON cm.substance_id = sp.id
ORDER BY cm.p_value ASC;

-- Grant permissions (adjust as needed)
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO epiclock_reader;
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO epiclock_admin;

COMMENT ON TABLE cpg_markers IS 'CpG methylation markers associated with substance use disorders';
COMMENT ON TABLE substance_panels IS 'Substance-specific CpG biomarker panels';
COMMENT ON TABLE gene_systems IS 'Neurotransmitter and biological systems related to addiction';
COMMENT ON TABLE epigenetic_clocks IS 'DNA methylation-based biological age estimation clocks';
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return sql_schema


def generate_sql_insert_statements() -> str:
    """Generate SQL INSERT statements for populating the database"""
    
    sql_inserts = []
    sql_inserts.append("-- EpiClock Database Population Script")
    sql_inserts.append(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sql_inserts.append("-- Author: Dr. Nurcan Denli Bayır")
    sql_inserts.append("")
    
    sql_inserts.append("-- Insert Substance Panels")
    for substance, info in SUBSTANCE_CPG_COUNTS.items():
        sql_inserts.append(f"""
INSERT INTO substance_panels (substance_code, turkish_name, english_name, total_cpgs, strong_evidence, moderate_evidence, suggestive_evidence, sensitivity, specificity, auc)
VALUES ('{substance}', '{info['turkish_name']}', '{substance.replace('_', ' ').title()}', {info['total_cpgs']}, {info['strong_evidence']}, {info['moderate_evidence']}, {info['suggestive_evidence']}, {info['sensitivity']}, {info['specificity']}, {info['auc']})
ON CONFLICT (substance_code) DO UPDATE SET 
    total_cpgs = EXCLUDED.total_cpgs,
    sensitivity = EXCLUDED.sensitivity,
    specificity = EXCLUDED.specificity,
    auc = EXCLUDED.auc;
""")
    
    sql_inserts.append("\n-- Insert Gene Systems")
    for system_name, system_data in CPG_GENE_SYSTEMS.items():
        genes_array = "ARRAY['" + "', '".join(system_data['genes']) + "']"
        description = system_data['description'].replace("'", "''")
        relevance = system_data['addiction_relevance'].replace("'", "''")
        sql_inserts.append(f"""
INSERT INTO gene_systems (system_code, system_name, description, genes, total_cpgs, addiction_relevance)
VALUES ('{system_name}', '{system_data['name']}', '{description}', {genes_array}, {system_data['total_cpgs']}, '{relevance}')
ON CONFLICT (system_code) DO UPDATE SET 
    genes = EXCLUDED.genes,
    total_cpgs = EXCLUDED.total_cpgs;
""")
    
    sql_inserts.append("\n-- Insert CpG Markers")
    for substance, info in SUBSTANCE_CPG_COUNTS.items():
        panel = get_substance_cpg_panel(substance)
        if panel and panel.get('key_markers'):
            for marker in panel['key_markers']:
                gene = marker['gene'].replace("'", "''")
                direction = marker['direction'].replace("'", "''")
                evidence = marker['evidence'].replace("'", "''")
                sql_inserts.append(f"""
INSERT INTO cpg_markers (cpg_id, gene, chromosome, delta_beta, p_value, direction, evidence_level, n_studies, substance_id)
SELECT '{marker['cpg_id']}', '{gene}', '{marker['chromosome']}', {marker['delta_beta']}, {marker['p_value']}, '{direction}', '{evidence}', {marker['n_studies']}, id
FROM substance_panels WHERE substance_code = '{substance}'
ON CONFLICT (cpg_id, substance_id) DO NOTHING;
""")
    
    return "\n".join(sql_inserts)


def get_export_statistics() -> Dict[str, Any]:
    """Get statistics about exportable data"""
    
    cpg_stats = get_total_cpg_statistics()
    db_stats = get_database_statistics()
    
    return {
        "cpg_sites": {
            "total": cpg_stats['total_cpgs_with_overlap'],
            "unique": cpg_stats['unique_cpg_sites'],
            "strong_evidence": cpg_stats['strong_evidence_cpgs']
        },
        "substances": cpg_stats['substance_classes'],
        "gene_systems": cpg_stats['gene_systems'],
        "gwas_studies": len(ADDICTION_GWAS_STUDIES),
        "ewas_markers": sum(len(m) for m in EWAS_ADDICTION_MARKERS.values()),
        "pharmgkb_genes": len(PHARMGKB_ADDICTION_GENES),
        "addiction_genes": db_stats['total_addiction_genes'],
        "formats_available": ["CSV", "BED", "JSON", "SQL"]
    }


def export_gwas_catalog_csv() -> str:
    """Export GWAS catalog data in CSV format"""
    
    gwas_data = []
    for key, study in ADDICTION_GWAS_STUDIES.items():
        gwas_data.append({
            'study_id': study.study_id,
            'trait': study.trait,
            'n_samples': study.n_samples,
            'year': study.year,
            'citation': study.citation,
            'pmid': study.pmid,
            'consortium': study.consortium or '',
            'ancestry': study.ancestry,
            'n_snps': study.n_snps
        })
    
    df = pd.DataFrame(gwas_data)
    return df.to_csv(index=False)


def export_ewas_markers_csv() -> str:
    """Export EWAS markers in CSV format"""
    
    ewas_data = []
    for trait, markers in EWAS_ADDICTION_MARKERS.items():
        for marker in markers:
            ewas_data.append({
                'trait': trait,
                'cpg_id': marker.cpg_id,
                'gene': marker.gene,
                'chromosome': marker.chromosome,
                'position': marker.position,
                'delta_beta': marker.delta_beta,
                'p_value': marker.p_value,
                'n_samples': marker.n_samples,
                'tissue': marker.tissue,
                'study_pmid': marker.study_pmid
            })
    
    df = pd.DataFrame(ewas_data)
    return df.to_csv(index=False)


def export_pharmgkb_csv() -> str:
    """Export PharmGKB gene data in CSV format"""
    
    gene_data = []
    for gene_name, gene_info in PHARMGKB_ADDICTION_GENES.items():
        gene_data.append({
            'gene': gene_name,
            'full_name': gene_info.get('full_name', ''),
            'function': gene_info.get('function', ''),
            'substances': ', '.join(gene_info.get('substances', [])),
            'key_variants': ', '.join(gene_info.get('key_variants', [])),
            'clinical_significance': gene_info.get('clinical_significance', '')
        })
    
    df = pd.DataFrame(gene_data)
    return df.to_csv(index=False)


# End of module - # nrcdnl94