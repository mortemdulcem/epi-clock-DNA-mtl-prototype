#!/usr/bin/env python3
"""
EpiClock v4.0 - Module-Specific Excel Export
Creates comprehensive Excel files for each implemented module
Format: Multi-sheet workbooks with data + summary sheets
"""

import pandas as pd
import os
from datetime import datetime

output_dir = "figures/output"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("EpiClock v4.0 - Module Excel Export")
print("=" * 60)

# ============================================================================
# 1. EPIGENETIC CLOCKS DATABASE
# ============================================================================
print("\n[1/6] Creating EpiClock_Epigenetic_Clocks_v4.0.xlsx...")

try:
    from modules.real_epigenetic_clocks import RealEpigeneticClockDatabase
    clocks_db = RealEpigeneticClockDatabase()
    
    clock_data = []
    clock_summary = []
    
    for clock_name, clock_obj in clocks_db.clocks.items():
        coeffs = clock_obj.coefficients
        clock_info = {
            "Clock_Name": clock_name.upper(),
            "Full_Name": clock_obj.name if hasattr(clock_obj, 'name') else clock_name,
            "Reference": clock_obj.reference if hasattr(clock_obj, 'reference') else "",
            "PMID": clock_obj.pmid if hasattr(clock_obj, 'pmid') else "",
            "Year": clock_obj.year if hasattr(clock_obj, 'year') else "",
            "License": clock_obj.license if hasattr(clock_obj, 'license') else "",
            "CpG_Count": len(coeffs),
            "Validated_CpGs": sum(1 for c in coeffs if hasattr(c, 'validated') and c.validated),
            "Status": "Open Source" if "open" in str(clock_obj.license).lower() else "Licensed"
        }
        clock_summary.append(clock_info)
        
        for coef in coeffs:
            clock_data.append({
                "Clock": clock_name.upper(),
                "CpG_ID": coef.cpg_id if hasattr(coef, 'cpg_id') else "",
                "Coefficient": coef.coefficient if hasattr(coef, 'coefficient') else 0,
                "Gene": coef.gene if hasattr(coef, 'gene') else "",
                "Chromosome": coef.chromosome if hasattr(coef, 'chromosome') else "",
                "Position": coef.position if hasattr(coef, 'position') else "",
                "Validated": coef.validated if hasattr(coef, 'validated') else False,
                "Reference": clock_obj.reference if hasattr(clock_obj, 'reference') else "",
                "PMID": clock_obj.pmid if hasattr(clock_obj, 'pmid') else ""
            })
    
    with pd.ExcelWriter(f"{output_dir}/EpiClock_Epigenetic_Clocks_v4.0.xlsx", engine='openpyxl') as writer:
        pd.DataFrame(clock_data).to_excel(writer, sheet_name='Clock_Coefficients', index=False)
        pd.DataFrame(clock_summary).to_excel(writer, sheet_name='Clock_Summary', index=False)
    
    print(f"   -> {len(clock_data)} coefficients, {len(clock_summary)} clocks")
except Exception as e:
    print(f"   -> Error: {e}")

# ============================================================================
# 2. SUBSTANCE ABUSE DATABASE
# ============================================================================
print("\n[2/6] Creating EpiClock_Substance_Abuse_Database_v4.0.xlsx...")

try:
    from modules.pharmacological_abuse_intelligence import PharmacologicalAbuseIntelligence
    pharma_db = PharmacologicalAbuseIntelligence()
    
    substance_data = []
    category_summary = {}
    
    if hasattr(pharma_db, 'substance_profiles'):
        for sub_id, sub_info in pharma_db.substance_profiles.items():
            category = sub_info.get("pharmacological_class", "Unknown")
            category_summary[category] = category_summary.get(category, 0) + 1
            
            cpg_markers = sub_info.get("cpg_markers", [])
            cpg_ids = [m.get("id", "") for m in cpg_markers[:5]]
            
            substance_data.append({
                "Substance_ID": sub_id,
                "Name": sub_info.get("name", ""),
                "Pharmacological_Class": category,
                "CAS_Number": sub_info.get("cas_number", ""),
                "Addiction_Potential": sub_info.get("addiction_potential", ""),
                "Addiction_CI_Lower": sub_info.get("addiction_ci", (0, 0))[0] if sub_info.get("addiction_ci") else "",
                "Addiction_CI_Upper": sub_info.get("addiction_ci", (0, 0))[1] if sub_info.get("addiction_ci") else "",
                "Mechanism": sub_info.get("mechanism", ""),
                "Withdrawal_Severity": sub_info.get("withdrawal_severity", ""),
                "Key_Genes": "; ".join(sub_info.get("key_genes", [])),
                "CpG_Markers": "; ".join(cpg_ids),
                "References": "; ".join(sub_info.get("references", [])[:2])
            })
    
    summary_data = [{"Category": k, "Substance_Count": v} for k, v in sorted(category_summary.items(), key=lambda x: -x[1])]
    
    with pd.ExcelWriter(f"{output_dir}/EpiClock_Substance_Abuse_Database_v4.0.xlsx", engine='openpyxl') as writer:
        pd.DataFrame(substance_data).to_excel(writer, sheet_name='Substance_Database', index=False)
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Category_Summary', index=False)
    
    print(f"   -> {len(substance_data)} substances, {len(category_summary)} categories")
except Exception as e:
    print(f"   -> Error: {e}")

# ============================================================================
# 3. ABUSE METHOD DETECTION
# ============================================================================
print("\n[3/6] Creating EpiClock_Abuse_Method_Detection_v4.0.xlsx...")

try:
    from modules.abuse_method_detection import AbuseMethodDetectionIntelligence
    abuse_db = AbuseMethodDetectionIntelligence()
    
    method_data = []
    marker_data = []
    method_summary = {}
    
    if hasattr(abuse_db, 'abuse_methods'):
        for method_id, method_info in abuse_db.abuse_methods.items():
            cpg_sig = method_info.get("cpg_signature", [])
            
            method_summary[method_id] = {
                "Method_ID": method_id,
                "Method_Name": method_info.get("name", ""),
                "Description": method_info.get("description", ""),
                "Chemical_Process": method_info.get("chemical_process", ""),
                "Absorption_Rate": method_info.get("absorption_rate", ""),
                "Bioavailability": method_info.get("bioavailability", ""),
                "Overdose_Risk": method_info.get("overdose_risk", ""),
                "Examples": "; ".join(method_info.get("examples", [])),
                "CpG_Marker_Count": len(cpg_sig)
            }
            
            for cpg_info in cpg_sig:
                marker_data.append({
                    "Method_ID": method_id,
                    "Method_Name": method_info.get("name", ""),
                    "CpG_ID": cpg_info.get("id", "") if isinstance(cpg_info, dict) else "",
                    "Gene": cpg_info.get("gene", "") if isinstance(cpg_info, dict) else "",
                    "Effect": cpg_info.get("effect", "") if isinstance(cpg_info, dict) else "",
                    "Weight": cpg_info.get("weight", "") if isinstance(cpg_info, dict) else "",
                    "PMID": cpg_info.get("pmid", "") if isinstance(cpg_info, dict) else ""
                })
    
    with pd.ExcelWriter(f"{output_dir}/EpiClock_Abuse_Method_Detection_v4.0.xlsx", engine='openpyxl') as writer:
        pd.DataFrame(marker_data).to_excel(writer, sheet_name='CpG_Markers', index=False)
        pd.DataFrame(list(method_summary.values())).to_excel(writer, sheet_name='Method_Summary', index=False)
    
    print(f"   -> {len(marker_data)} markers, {len(method_summary)} methods")
except Exception as e:
    print(f"   -> Error: {e}")

# ============================================================================
# 4. DNA MANUFACTURING DETECTION
# ============================================================================
print("\n[4/6] Creating EpiClock_DNA_Manufacturing_Detection_v4.0.xlsx...")

try:
    from modules.dna_manufacturing_detection import DNAManufacturingIntelligence
    mfg_db = DNAManufacturingIntelligence()
    
    exposure_data = []
    method_data = []
    
    if hasattr(mfg_db, 'exposure_markers'):
        for exp_id, exp_info in mfg_db.exposure_markers.items():
            for marker in exp_info.get("cpg_markers", []):
                exposure_data.append({
                    "Exposure_ID": exp_id,
                    "Chemical_Name": exp_info.get("name", ""),
                    "CAS_Number": exp_info.get("cas_number", ""),
                    "Category": exp_info.get("category", ""),
                    "CpG_ID": marker.get("cpg_id", ""),
                    "Gene": marker.get("gene", ""),
                    "Effect": marker.get("effect", ""),
                    "PMID": marker.get("pmid", "")
                })
    
    if hasattr(mfg_db, 'method_signatures'):
        for method_id, method_info in mfg_db.method_signatures.items():
            for marker in method_info.get("cpg_markers", []):
                method_data.append({
                    "Method_ID": method_id,
                    "Method_Name": method_info.get("name", ""),
                    "Description": method_info.get("description", ""),
                    "CpG_ID": marker.get("cpg_id", ""),
                    "Gene": marker.get("gene", ""),
                    "Effect": marker.get("effect", ""),
                    "PMID": marker.get("pmid", "")
                })
    
    with pd.ExcelWriter(f"{output_dir}/EpiClock_DNA_Manufacturing_Detection_v4.0.xlsx", engine='openpyxl') as writer:
        pd.DataFrame(exposure_data).to_excel(writer, sheet_name='Chemical_Exposures', index=False)
        pd.DataFrame(method_data).to_excel(writer, sheet_name='Manufacturing_Methods', index=False)
        
        summary = pd.DataFrame([
            {"Category": "Chemical Exposures", "Record_Count": len(exposure_data)},
            {"Category": "Manufacturing Methods", "Record_Count": len(method_data)}
        ])
        summary.to_excel(writer, sheet_name='Summary', index=False)
    
    print(f"   -> {len(exposure_data)} exposures, {len(method_data)} methods")
except Exception as e:
    print(f"   -> Error: {e}")

# ============================================================================
# 5. GSEA PATHWAY DATABASE
# ============================================================================
print("\n[5/6] Creating EpiClock_GSEA_Pathway_Database_v4.0.xlsx...")

try:
    from modules.gsea import GSEAnalyzer
    gsea = GSEAnalyzer()
    
    pathway_data = []
    gene_data = []
    
    if hasattr(gsea, 'PATHWAY_DATABASE'):
        for pathway_id, pathway_info in gsea.PATHWAY_DATABASE.items():
            genes = pathway_info.get("genes", [])
            cpgs = pathway_info.get("cpg_markers", [])
            
            pathway_data.append({
                "Pathway_ID": pathway_id,
                "Pathway_Name": pathway_info.get("name", ""),
                "Category": pathway_info.get("category", ""),
                "Source": pathway_info.get("source", ""),
                "Gene_Count": len(genes),
                "CpG_Count": len(cpgs),
                "Genes": "; ".join(genes[:30]),
                "CpG_Markers": "; ".join(cpgs[:20])
            })
            
            for gene in genes:
                gene_data.append({
                    "Pathway_ID": pathway_id,
                    "Pathway_Name": pathway_info.get("name", ""),
                    "Gene": gene
                })
    
    with pd.ExcelWriter(f"{output_dir}/EpiClock_GSEA_Pathway_Database_v4.0.xlsx", engine='openpyxl') as writer:
        pd.DataFrame(pathway_data).to_excel(writer, sheet_name='Pathways', index=False)
        pd.DataFrame(gene_data).to_excel(writer, sheet_name='Pathway_Genes', index=False)
    
    print(f"   -> {len(pathway_data)} pathways, {len(gene_data)} gene associations")
except Exception as e:
    print(f"   -> Error: {e}")

# ============================================================================
# 6. REFERENCE METHYLATION DATABASE
# ============================================================================
print("\n[6/6] Creating EpiClock_Reference_Database_v4.0.xlsx...")

try:
    from modules.reference_database_expanded import ExpandedReferenceDatabase
    ref_db = ExpandedReferenceDatabase(quick_mode=True)
    
    profile_data = []
    condition_summary = {}
    
    for profile in ref_db.profiles[:2000]:
        condition = profile.condition if hasattr(profile, 'condition') else "Unknown"
        condition_summary[condition] = condition_summary.get(condition, 0) + 1
        
        profile_data.append({
            "Profile_ID": profile.profile_id if hasattr(profile, 'profile_id') else "",
            "Age": profile.age if hasattr(profile, 'age') else "",
            "Sex": profile.sex if hasattr(profile, 'sex') else "",
            "Condition": condition,
            "Condition_Category": profile.condition_category if hasattr(profile, 'condition_category') else "",
            "Condition_Duration_Years": profile.condition_duration_years if hasattr(profile, 'condition_duration_years') else "",
            "Epigenetic_Age": round(profile.epigenetic_age, 2) if hasattr(profile, 'epigenetic_age') else "",
            "EAA_Years": round(profile.eaa, 2) if hasattr(profile, 'eaa') else "",
            "Ethnicity": profile.ethnicity if hasattr(profile, 'ethnicity') else "",
            "Source_Study": profile.source_study if hasattr(profile, 'source_study') else ""
        })
    
    summary_data = [{"Condition": k, "Profile_Count": v} for k, v in sorted(condition_summary.items(), key=lambda x: -x[1])]
    
    with pd.ExcelWriter(f"{output_dir}/EpiClock_Reference_Database_v4.0.xlsx", engine='openpyxl') as writer:
        pd.DataFrame(profile_data).to_excel(writer, sheet_name='Reference_Profiles', index=False)
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Condition_Summary', index=False)
        
        stats = ref_db.get_statistics()
        stats_df = pd.DataFrame([
            {"Metric": "Total Profiles", "Value": stats.get("total_profiles", 0)},
            {"Metric": "Total CpG Sites", "Value": stats.get("total_cpg_sites", 0)},
            {"Metric": "Conditions", "Value": stats.get("conditions", 0)},
            {"Metric": "Age Range", "Value": f"{stats.get('age_range', {}).get('min', 0)}-{stats.get('age_range', {}).get('max', 0)}"},
            {"Metric": "Male Count", "Value": stats.get("sex_distribution", {}).get("M", 0)},
            {"Metric": "Female Count", "Value": stats.get("sex_distribution", {}).get("F", 0)}
        ])
        stats_df.to_excel(writer, sheet_name='Database_Statistics', index=False)
    
    print(f"   -> {len(profile_data)} profiles, {len(condition_summary)} conditions")
except Exception as e:
    print(f"   -> Error: {e}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 60)
print("EXPORT COMPLETE!")
print("=" * 60)

print(f"\nAll files saved to: {output_dir}/")
print("\nGenerated Excel Files:")
files = [
    "EpiClock_Disease_Methylation_Database_v4.0.xlsx",
    "EpiClock_Epigenetic_Clocks_v4.0.xlsx",
    "EpiClock_Substance_Abuse_Database_v4.0.xlsx",
    "EpiClock_Abuse_Method_Detection_v4.0.xlsx",
    "EpiClock_DNA_Manufacturing_Detection_v4.0.xlsx",
    "EpiClock_GSEA_Pathway_Database_v4.0.xlsx",
    "EpiClock_Reference_Database_v4.0.xlsx"
]
for f in files:
    if os.path.exists(f"{output_dir}/{f}"):
        size = os.path.getsize(f"{output_dir}/{f}") / 1024
        print(f"  - {f} ({size:.1f} KB)")
