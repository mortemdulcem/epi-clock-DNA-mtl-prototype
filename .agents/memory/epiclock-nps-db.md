---
name: EpiClock NPS database — real chemistry, fabricated methylation
description: The author's EpiClock prototype ships a GENUINE, importable NPS database + Markush engine, but its per-substance methylation/CpG layer is fabricated and must be excluded.
---

# EpiClock prototype NPS database

The author (Dr. Nurcan) has a real prototype repo (github.com/mortemdulcem/epi-clock-DNA-mtl-prototype),
mirrored under `attached_assets/gdrive/epiclock/_code/EpiClockPrototype/modules/`. Three modules are
genuinely usable for the addiction-epigenetics article (scripts/revize):

- `nps_database_unodc.py` — 17 NPS across 7 UNODC categories; real molecular_formula / MW / CAS / IUPAC.
- `comprehensive_substance_database.py` — 27 reference substances via `get_all_substances()`, which returns
  a **dict of {class: {name: SubstanceProfile}}** (dict-of-dicts, NOT lists). Iterate `.values()` when scanning.
- `markush_rules.py` — `MARKUSH_RULES` = 10 rules with real `core_smarts` + `variable_positions`;
  `generate_all_possible_variants(rule_id, max_per_position)` enumerates **29,277** theoretical R-group variant
  combinations total. SMARTS validate 10/10 in RDKit. This 29,277 is the honest basis of the article's old
  "36,000+ substance database" claim.

**Real vs fabricated split (the trap):**
- REAL & reusable: the chemical identities + Markush scaffolds. Chemistry validates 15/17 under each test
  (internal formula→avg-MW and external PubChem). The 2 misses per test are: internal = Carfentanil
  (prototype DB formula C27H32N2O3 is genuinely WRONG; real/PubChem = C24H30N2O3) + Etizolam (stated mass is
  monoisotopic, not average — formula correct); external = Carfentanil + 2-FDCK (PubChem name resolves the HCl
  salt C13H17ClFNO, DB freebase correct). Report all four explicitly — do NOT collapse to one caveat.
- FABRICATED — must exclude: the per-substance `methylation_markers` / `detection_genes` / `methylation_cpgs`.
  Proof: AHRR smoking CpG `cg05575921` mis-assigned to 6 unrelated drugs; 11 CpGs reused across different drugs.

**Why:** A future agent asked to "use the EpiClock NPS data" would otherwise silently re-import the fabricated
methylation overlay, violating the Zero-Hallucination policy. The chemistry layer is trustworthy; the
epigenetic overlay is not.
**How to apply:** Pipeline = `scripts/revize/realdata/scripts/29_nps_database_markush.py` (imports the modules,
validates internally + via cached PubChem, RDKit-checks SMARTS, enumerates 29,277, quantifies+declares the
fabricated layer) → `out/dl/nps_database_markush.json` + `nps_unodc_validation.csv`. Surfaced in makale.txt
§2.3 + §2.4 module (4) and REPORT.md §4.11 row 4 / §5.
