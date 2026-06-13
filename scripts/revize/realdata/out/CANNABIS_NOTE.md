# Cannabis (GSE255929 / PMID 40205553) — honest status

Raw betas ARE public (peripheral blood, Illumina EPIC, n=93) but the cannabis status labels (never/former/current) are NOT deposited in GEO. The only grouping code (S1/S2, mislabeled under 'age') is two confounded sub-cohorts: S1 = 59 all-female, older (~59y); S2 = 34 mostly-male, younger (~47y). A self-computed cannabis EWAS is therefore NOT credible; the S2-vs-S1 contrast is a batch/sub-cohort artifact (364,347 'DMP', 42% of the array) and has been renamed `GSE255929_S1vsS2_subcohort_CONFOUNDED.csv` to prevent misuse.

USE the published, peer-reviewed results instead — PMID 40205553 (BMC Pulm Med 2025; DOI 10.1186/s12890-025-03634-9; CanCOLD cohort): n=93 peripheral blood, Illumina EPIC; 12,115 DMGs (current vs never), 10,806 DMGs (former vs never), 5,915 shared; 50 shared enriched pathways dominated by aging- and cancer-related pathways; all at FDR<0.05.
