---
name: Substance methylation data reality (public GEO/ArrayExpress)
description: What substance-use DNA-methylation data actually exists publicly, what was pulled, and the smoking-confound in alcohol EWAS. Use when deciding what real data can back the makale_revize article.
---

# Public substance-use DNA-methylation data — the real landscape

Exhaustive live search of NCBI GEO (E-utilities, db=gds) + EBI ArrayExpress/BioStudies
(script: `scripts/revize/realdata/scripts/07_inventory.py`; outputs in `out/inventory_*`).

- Raw "substance + methylation + Homo sapiens" hits: **573 datasets / 53,481 samples**, but
  most are INCIDENTAL mentions (reference epigenomes, cancer, HIV, schizophrenia, RA where the
  substance is just a covariate). Pooling those would be scientifically wrong.
- Genuinely substance-FOCUSED cohorts (substance in the title), deduplicated:
  **82 datasets / 8,985 unique samples**. Breakdown (overlaps counted per substance):
  smoking 5,714 · IDU/SUD 1,758 · alcohol 1,659 · opioid 279 · cocaine 211 · cannabis 129 · meth 32.
- **The article's "10,542 samples / 7 balanced classes / 87.3%" does NOT exist publicly** and is
  not reproducible. cocaine/meth/cannabis cohorts are tiny (n≈8–58). Real version is
  smoking-dominated, with usable alcohol + (supplementary-only) IDU.
- Curated list saved: `out/curated_substance_cohorts.csv`.

## Datasets actually downloaded + verified (SHA in data/manifest.json)
- GSE50660 (smoking, 450K whole blood) — real betas; current-vs-never EWAS already done.
- GSE110043 (alcohol, 450K whole blood) — 94 samples, 47 drinkers / 47 non; real betas.
- GSE57853 (alcohol, 450K lymphocyte) — 92 samples but PAIRED (T1/T2 per individual) → needs
  longitudinal handling, not a plain case/control.
- GSE100264 (IDU) — series matrix is metadata-only (platform GPL16304, sequencing); **no beta
  values in the matrix**. Real IDU betas need supplementary files or GSE107082 (EPIC).
- GSE77056 (cocaine/crack, 450K **whole blood**) — REAL betas, 23 dependents vs 24 healthy
  controls. EWAS (06_dmp_substance.py) → 11,987 CpG FDR<0.05. Heavy POLY-drug confound: pheno
  itself records smoke/cannabis/solvents/heroin co-use; AHRR rank ~2490 (smoking present, not
  dominant). Small n → exploratory.
- GSE154971 (methamphetamine, 450K **peripheral blood lymphocytes**) — REAL betas, 16 users
  vs 8 controls. EWAS → 398 CpG FDR<0.05; AHRR rank ~203 (more smoking-tinged). Tiny n.
- Real BLOOD 450K case/control cohorts in hand for 4 substances: smoking (GSE50660), alcohol
  (GSE110043), cocaine (GSE77056), meth (GSE154971) — all GPL13534.
- OPIOID/heroin: GSE98203 = REAL 450K processed betas BUT BRAIN (orbitofrontal cortex neuronal
  nuclei, postmortem), 37 heroin / 29 control. My EWAS (07_dmp_opioid_brain.py) heroin-vs-control
  + age+sex → only 12 CpG FDR<0.05 (top cg27504782 p=7.7e-8); AHRR not sig (not tobacco). Heroin
  group younger (mean 25.7 vs 37.2, ranges overlap → age-adjusted, defensible exploratory). Brain
  only → cannot merge with blood classifier.
- CANNABIS: published blood EWAS EXISTS = PMID 40205553 / GSE255929 (BMC Pulm Med 2025, CanCOLD,
  n=93 blood EPIC). CITE its real numbers: 12,115 DMGs current-vs-never, 10,806 former-vs-never,
  5,915 shared, 50 shared aging/cancer pathways, FDR<0.05. BUT raw SELF-reproduction is BLOCKED:
  GEO deposits only Sex+age+a 2-code 'S1/S2' (mislabeled under 'age'). S1=59 ALL-female age~59,
  S2=34 mostly-male age~47 → confounded sub-cohorts, NOT cannabis labels. My S2-vs-S1 EWAS gave a
  bogus 364k DMP (42% of array) batch artifact → DISCARDED/renamed *_CONFOUNDED.csv. Lesson: always
  crosstab a deposited grouping vs age/sex before trusting it.
- Synthetic cannabinoids / MDMA / ecstasy / ketamine: ZERO human methylation data (GEO esearch=0).
  Only PubChem chemistry is real (cheminformatics angle, not methylation).
- Fabricated unified 7-class / 10,542 / 87.3% classifier remains impossible (mixed platforms 450K
  vs EPIC, blood vs brain, tiny n). Honest design = per-substance EWAS with declared (small) n +
  cross-substance marker comparison + CITE published cannabis/opioid numbers where raw self-repro
  is confounded/brain-only.

## Enrichment + epigenetic-clock outcomes per substance (scripts 09/10, generic)
- Horvath 2013 pan-tissue clock behaves very differently by cohort: **brain opioid GSE98203
  r=0.91 (excellent), blood cocaine GSE77056 r=0.44 (poor — ages only 23–29, range too narrow)**.
  Lesson: clock validity needs a wide chronological-age spread; narrow-age cohorts give weak r
  even when the clock is implemented correctly. Brain MAE is inflated (~11y offset, known).
- **GSE154971 (meth) has NO chronological age in the GEO deposit** → epigenetic clock impossible;
  do not fabricate, declare it.
- Enrichment reality: cocaine (11,987 CpG → genes capped at 1500) gives 14 KEGG terms FDR<0.05
  (cancer/cellular-senescence/Wnt/Hippo); meth (398 CpG) gives 0 sig GO/KEGG; opioid brain
  (only 12 CpG) gives 25 sig GO terms but **every term is a single-gene overlap (1/5–1/8) →
  biologically coherent (synaptic) but statistically fragile**, must be flagged as suggestive.
- No age-acceleration difference reached significance for any substance (all honest nulls).

## Extra public-coefficient clocks added (Hannum + PhenoAge) — biolearn source + Framingham reality
- **Public clock-coefficient source = biolearn GitHub** (`bio-learn/biolearn`, branch master):
  `https://raw.githubusercontent.com/bio-learn/biolearn/master/biolearn/data/<Clock>.csv`. Clean
  CSVs `CpGmarker,CoefficientTraining` (+ optional `intercept` row). Available: Hannum (71, no
  intercept→0, linear), PhenoAge (513, intercept 60.664, linear), Horvath1/2, DunedinPACE (173,
  intercept −1.9498, needs gold-means quantile-norm), GrimAgeV1/V2 (protein sub-models + age/sex),
  Smoking, Alcohol, Zhang2019. `13_multiclock.py` computes Hannum+PhenoAge (simple linear) on any
  cohort with age; DunedinPACE/GrimAge declared, NOT hand-approximated (would need full biolearn).
- **Blood vs brain clock behavior is REAL, not a bug:** Hannum/PhenoAge are blood-trained → validate
  well in blood (Hannum r 0.57–0.80, PhenoAge 0.63–0.75) but weak/variable in postmortem brain
  (alcohol GSE49393 r 0.38–0.46); pan-tissue Horvath stays strong in brain (r 0.80–0.91). PhenoAge
  MAE is large (47–66y in brain) because it returns PHENOTYPIC (mortality-calibrated) age, not
  chronological — judge by r + age-accel, not MAE.
- **Two genuine positive age-accel signals** (rest null): cocaine GSE77056 Hannum age-accel Welch
  **p=0.021** (cases higher); smoking GSE50660 PhenoAge age-accel **p=0.051** (borderline).
- **Framingham Heart Study (GrimAge's "10,000+") is NOT usable:** raw methylation is dbGaP
  controlled-access (phs000724) — needs application+IRB+DUA, not downloadable. GEO "Framingham"
  hits (~608) are incidental/citational; the actual matrix is not public. Adding clocks raises the
  count of real CpGs *computed* (+71, +513 per clock) but does NOT enlarge the substance-specific
  DMP signature, which is bounded by the cohorts we can actually access.

## Key confound lesson — alcohol EWAS (GSE110043)
`beta ~ drinker + sex` (no age/smoking covariate available in this series). Top hits are
**SMOKING CpGs**, not alcohol: cg05575921/AHRR rank 1, cg21566642 rank 3, cg03636183/F2RL3
rank 4, cg09935388/GFI1 rank 9. Drinkers in this cohort smoke more → alcohol signal is
**confounded by smoking** and cannot be deconfounded without a smoking variable.
Genuine alcohol markers ARE present though: cg04987734/CDC42BPB rank 15 (p=5e-11),
cg06690548/SLC7A11 rank 520 (p=6e-6, FDR-sig). 4,387 CpGs FDR<0.05 total.

**Why this matters:** it proves the pipeline recovers real biology AND that real substance
methylation is messy/confounded — the opposite of the fabricated article's clean 87.3%
7-way separation. Any honest alcohol claim must flag the smoking confound (or find a cohort
with a smoking covariate).

## All 14 CITED sources verified LIVE — every one fabricated/mislabeled (do not re-chase)
Script `11_verify_cited_sources.py` queried each Table-1 accession live (NCBI E-utils + EBI
BioStudies + PMC); raw in `out/cited_raw/`, summary `out/cited_sources_verification.json`.
**None match the article's claimed substance/n.** Highlights: GSE181817=solid-tumor atlas n=6
(not "cocaine 1030"); GSE149229=MOUSE liver phenobarbital n=28 (not "meth 48"); GSE105018=E-Risk
twins; GSE125105=depression blood; GSE154566=victimization twins; GSE87571=aging n=732 (its N
was falsely pasted onto GSE110043's "732"); E-MTAB-5738=SCC, 7309=SATSA aging, 10888=yolk sac.
Lesson: the citations are noise — never treat a makale accession as ground truth, always verify.

## TWO genuine substance sources were HIDDEN inside the fake citations (recovered + analyzed)
- **GSE49393** = REAL adult alcohol-use-disorder postmortem **prefrontal cortex** 450K, **n=48**
  (23 AUD vs 25 control) — article lied "n=24". Our EWAS (`12_dmp_alcohol_brain.py`, age+sex):
  **8 CpG FDR<0.05**, top cg00393248 p=9.3e-8; **smoking-clean** (AHRR rank ≈169k). Enrichment
  (09): 3 genes → GO 2 / KEGG 9, all single-gene → fragile. Clock (10, now has GSE49393 in
  CONFIG): Horvath **r=0.796 p=1.4e-11 MAE 6.5y**; age-accel ns (Welch p=0.29). 2nd genuine
  alcohol cohort + first smoking-clean alcohol signal (complements smoking-confounded GSE110043).
- **PMC9979153** = REAL opioid blood EWAS **meta-analysis** (Epigenomics 2022;14(23):1479-1492,
  PMID 36700736): **282 users / 10,560 controls**, 6 CpG FDR<0.05 (KIAA0226/RUBCNL, CPLX2, TDRP,
  RNF38, TTC23, GPR179). CITE these (meta-analysis, no single raw matrix to recompute). Gives
  opioid a BLOOD complement to our BRAIN GSE98203.
- FASD GSE112987 (n=103) & GSE80261 (n=216) = real alcohol but PRENATAL exposure (different
  phenotype, not adult addiction) → declared, not analyzed as addiction. EWAS Data Hub Hub-1/2/3
  "substance subsets" at the claimed Ns don't exist → unverifiable, not used.

## GitHub repo (EpiClockPrototype) — fully investigated, nothing real there
Private repo `mortemdulcem/epi-clock-DNA-mtl-prototype` pulled LIVE with the owner's token.
- Live `main` froze at **2 Feb 2026**; it is OLDER than the **25 Apr 2026** zip snapshot we
  already had. GitHub has **nothing extra** — the local zip is the superset. Other branches
  are only dependabot dependency bumps. Do NOT re-chase the GitHub repo for "real data."
- The Feb 2026 commits titled "Replace placeholder data with real EWAS-validated markers" /
  "Update CpG markers to use real, validated data" are **cosmetic fabrication**: obvious dummy
  IDs (`cg12121212`, `cg13131313`, …) were swapped for real-looking CpG IDs that are
  **misassigned to the wrong genes** — e.g. `cg05575921` (the canonical AHRR *smoking* marker)
  pasted onto CHRM1; `cg03636183` (F2RL3 smoking) onto CHRM2; the same id `cg10636246` reused
  for two different genes. Weights (0.88, 0.82, …) unchanged. No real measurements added; this
  is disguised fabrication, more deceptive than the plain placeholders.
- The repo's own README (6 Dec 2025) states it is "a demonstration platform using simulated
  data." Conclusion stands: the article's 10,542 samples / 7 substances / 87.3% exist nowhere.

## External "methodology guide" GEO IDs are mostly mislabeled (verify every one)
A Monica/Claude-Sonnet technical guide the user supplied listed substance GEO datasets;
NCBI esummary (db=gds) check (out/cited_raw/*_esummary.json):
- GSE149229 claimed "Metamfetamin" = REALLY mouse-liver phenobarbital CAR/PXR study (GPL10787, n=28) → WRONG, not human, not meth.
- GSE125105 claimed "Opioid/brain" = REALLY depression cohort n=489+210=699, whole blood, 450K → WRONG (same lie as the fabricated article).
- GSE80261 claimed "Alkol/BA9 brain" = REALLY fetal alcohol spectrum disorder (FASD, prenatal), 450K, n=216 → wrong phenotype+tissue.
- GSE154566 claimed "Genel" = REALLY adolescent-victimization MZ-twin study (EPIC, n=1177) → not substance use.
- GSE87571 claimed "aging control n=700+" = CORRECT (human lifespan methylome aging, 450K, n=732).
**Lesson:** even a polished guide that itself preaches anti-hallucination confidently mislabels GEO accessions. ALWAYS resolve every accession against esummary before citing/using. Real adult-substance methylation stays smoking-dominated (see top of file).
