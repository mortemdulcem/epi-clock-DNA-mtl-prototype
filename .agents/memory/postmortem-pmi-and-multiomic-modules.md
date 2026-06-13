---
name: Postmortem PMI (#7) + Multi-omic fusion (#6) real-data builds
description: Which public datasets and methods make the makale_revize "postmortem stability" and "multi-omics fusion" modules genuinely real, and the traps that force a data-blocked declaration instead.
---

# Postmortem stability (#7) — dataset + method

- **GSE98203 (opioid PFC neurons) REJECTED for PMI modeling.** It *has* a `pmi (hr)` field, but 80/88 samples are exactly 24h (rest: 4/4/6/12/21/24.5 + 2 censored "<6h"/"<12"). No usable gradient → any beta~PMI result would be over-claimed on ~6 informative samples. Having a PMI column is NOT enough — always check PMI **variance** in the series-matrix header before committing.
- **GSE41826 CHOSEN** (Illumina 450K, human frontal cortex, NeuN-sorted into NEURON vs GLIA, n=145). Real PMI variance (~9–22h, 24 distinct values; 9 samples pmi='--' missing). Covariates in header: diagnosis (Control 77/Depression 68), Sex, race, age (16–50+), suicide status. **Cell fraction is encoded in the sample title suffix** (`5175-N` neuron / `5175-G` glia) and the **title prefix is the donor ID** → N/G from same donor are non-independent.
- **Method (architect-approved):** primary = **stratified** within neuron and within glia separately (cell fraction dominates methylation variance), M-value `logit(beta) ~ PMI + age + sex + diagnosis`, OLS t-stat + BH-FDR; then meta/concordance across fractions. Secondary = pooled with cell-type + PMI×cell-type interaction. Add seed=42 **blocked** permutation of PMI (within cell type/diagnosis) for null calibration. Drop missing-PMI, report exact n.
- **Honesty rules:** observational **association, not causal degradation**. GSE41826 has **no tissue pH and no batch** variable → state as limitation; PMI may confound with pH/age/cause-of-death/handling. Label CpGs "PMI-labile / PMI-insensitive **in this dataset**" — never universal "stable CpGs" or half-lives.

# Multi-omic fusion (#6) — dataset + method

- No addiction cohort in this project has paired multi-omics (all 6 are methylation-only). Fusing unrelated cohorts = batch artefact, refused.
- **Real path:** use an external public **sample-matched methylation+expression** resource (small TCGA cohort via UCSC Xena gene-level matrices, or a compact GEO SuperSeries whose sample IDs truly match). **VERIFY the concrete dataset before coding** (matching sample IDs across both omics, phenotype with adequate class counts, feasible sizes).
- **Framing (required):** explicitly "fusion-engine **validation on a public reference, NOT addiction-specific** (addiction paired-omics is not public)". This is honest as a methods demonstration.
- **Leakage rules:** split samples first; inside each StratifiedKFold(5, seed=42) fold do imputation, scaling, variance filter, univariate feature selection, PCA/encoder, classifier on **train only**; predeclare simple settings or use inner CV; never feature-select/scale/balance on full data; preserve sample alignment, drop duplicate aliquots. Report fold metrics with SD/CI + intersection count + class distribution.

# Environment
- GSE41826 series matrix = **568 MB gz (~3.5 GB text)** — cannot decompress fully in one 120s call. Download once (curl -C - resumable), then process the local gz **chunked** (pandas chunksize) with a resumable/checkpointed per-CpG accumulator, or a seed=42 genome-wide random subset if full pass overruns.
