---
name: DNA-methylation factor coverage (beyond substances)
description: For Dr. Nurcan's "all factors that alter DNA methylation" system — which non-substance factors have REAL public per-sample data (built) vs mirages vs mechanism-only. Use when asked to add another factor/phenotype model.
---

# Factor → methylation model coverage (the 9-category expansion)

Scope: extend the genuine methylation→phenotype system (in `scripts/revize/realdata`) to cover
the factors in Dr. Nurcan's OneDrive 9-category review, under ABSOLUTE Zero-Hallucination
(only model factors with REAL public per-sample methylation data; else declare "veri yok").
The system loads models by glob: `substance_*` / `condition_*` / `exposure_*` joblib in
`out/dl/models/`; `predict.py` surfaces each with its own `oof_metrics.caveat` + cpg_coverage.

## Honest 3-way factor map (always present this, don't overclaim)
- **(a) MECHANISM — not a predictable phenotype:** DNMT1/3A/3B enzymes, genomic imprinting,
  X-inactivation, TET/active-demethylation, Rett (MECP2)/ICF syndromes, transposon silencing.
  These are HOW methylation changes, not labels to classify → no classifier, explain only.
- **(b) ALREADY in the system:** aging (Horvath/Hannum/PhenoAge clocks), smoking, alcohol,
  cocaine, methamphetamine, opioid, depression (see substance-methylation-data.md).
- **(c) NEW real data verified this round:** arsenic exposure ✅, schizophrenia/psychosis ✅.

## Built this round (REAL data, leakage-free OOF)
- **Arsenic EXPOSURE** — GSE109914, 450K whole blood, n=119 (84 exposed / 35 unexposed).
  Betas in the series matrix (slice first ~120k probes). `exposure_arsenic.joblib`, OOF AUC ≈ 0.86
  (sens high ~0.95 / spec low — imbalance). Strongest new signal.
- **Schizophrenia / first-episode psychosis** — GSE152026 (EU-GEI), EPIC whole blood, n=934
  (413 case / 521 control). Betas only in an 8 GB suppl signals CSV → stub-label + head-slice
  technique (see geo-large-matrix-env-limits.md). `condition_schizophrenia.joblib`, OOF AUC ≈ 0.66
  — weak/confounded (antipsychotics, smoking, cell mix); exploratory, NOT diagnostic.

## Mirages this round — verified NOT usable (do not re-chase as case/control classifiers)
- PTSD GSE72680 — series matrix is a 38 KB stub (and Grady cohort structure messy).
- Lupus/SLE GSE161476 — neutrophil-sorted, longitudinal, no clean controls.
- Rheumatoid arthritis GSE176168 — treatment wk0/wk12 design, no healthy controls.
- Autism GSE27044 — only 27K array + messy family/sib structure.
- (Keyword GEO scans are NOISY: e.g. "sleep" false-matched a Mammalian Methylation Consortium
  set. Always verify the series-matrix header before trusting an esearch hit.)

**Rule:** before adding any factor model, confirm a REAL per-sample beta source with genuine
case/control (or exposed/unexposed) labels and >0 of each class; declare "veri yok" otherwise.
