---
name: makale_revize correction approach (Dr. Nurcan)
description: How to handle the fabricated multi-substance epigenetics article — correct in place, never replace with a short rebuild.
---

The fabricated multi-substance addiction-epigenetics article (`scripts/revize/makale.txt`
+ `tables.cjs` → `build/makale_revize.docx`, ~36 pages, 7 substances: alcohol/cocaine/
opioid/meth/cannabis/polysubstance) must be **corrected IN PLACE** — keep its length,
structure, and subject. Do NOT replace it with a shorter from-scratch "genuine" article
and do NOT silently change its subject (a 10-page smoking-only rebuild via
`build_gercek.cjs` was rejected hard: "36 sayfa nasıl 10 sayfa oldu").

**Process the user wants:** before changing any fabricated number, show her the
fabrication evidence **line-by-line** and let her decide each item; she supplies the real
data (Excel/CSV/SPSS/PDF) per substance. Don't act unilaterally.

**Why:** smoking (GSE50660) is not even one of the article's 7 substances; substituting it
changed the paper's topic AND shrank it. Both were wrong.

**Fabrication tells (detail in `scripts/revize/realdata/REPORT.md`):** cited GEO accessions
point to unrelated studies (GSE181817 = solid-tumor atlas, GSE149229 = mouse-liver
phenobarbital, GSE110043 = real alcohol but ~94 not 732, GSE154566 = twin victimization);
PMC9979153 is an article id, not a dataset; postmortem n contradiction (108 vs 1,119);
substance EAA values swapped across sections (meth/polysubstance +6.2↔+7.3); cg05575921/
AHRR (the canonical SMOKING CpG) mislabeled as the top ALCOHOL CpG; repo has no methylation
data and no analysis scripts, so all p/FDR/accuracy numbers were never computed.

**Source code obtained (EpiClockPrototype, via the user's Drive zip) CONFIRMS simulation:**
the article's exact published numbers are hardcoded Python lists in the figure scripts —
e.g. `figures/figure_2_substance_eaa.py` has `# Data from Table 7` then
`n_samples=[2183,1030,1360,48,194,720]`, `grimace_eaa=[3.6,4.1,2.9,6.2,1.6,7.3]`,
`cohens_d=[...]`. The "methylation data" is `np.random.beta` (`modules/data_processing.py`
synthetic_data + generate_sample_data); the clocks add `np.random.normal` noise and even
build GrimAge coefficients randomly (`modules/epigenetic_clocks.py`). A `real_data_loader.py`
exists but the published numbers do NOT come from it. So: simulated data presented as real
GEO analysis = fabrication, confirmed independently in two sessions.

**real_data_loader.py audited:** it is genuine file-parsing code (CSV/Excel/Parquet/GEO
series-matrix) but does NOT download anything (no GEOparse/urllib/requests/FTP) — it only
reads a file a human manually uploads; its own test fn fills `np.random.beta` data. It is
wired only into the Streamlit upload screens (dna_upload_analysis.py, analysis_pipeline.py),
so its mere existence does NOT make the article's numbers real.


## realdata pipeline: single source of truth + post-compression check
The genuine replacement lives in scripts/revize/realdata. After a context compression, the
out/ directory was FAR more complete than the recovery summary implied: canonical DMP
(06/07/08/12), clocks (05/10/13 Horvath+Hannum+PhenoAge), PRISMA (15), classifier (04) were
already done for 6 human substance cohorts (smoking GSE50660, alcohol-blood GSE110043,
alcohol-brain GSE49393, cocaine GSE77056, opioid-brain GSE98203, meth GSE154971; cannabis
GSE255929 dropped as confounded). LESSON: before re-deriving anything post-compression, list
out/ and read REPORT.md headings to see what already exists.

**Consistency trap (Zero-Hallucination):** the canonical DMP scripts use EQUAL-VARIANCE OLS
(limma-equivalent). Re-running EWAS with Welch (unequal var) gives a DIFFERENT sig count for
the SAME dataset (meth: 398 canonical vs 67 Welch) even though delta-beta is identical — this
is exactly the forbidden "same number differs across sections" error. Keep ONE method/source
of truth (the committed DMP csvs in out/), do not introduce a parallel EWAS script.

**Status: P1-P8 all COMPLETE.** P6 expanded ML done (18_ml.py: RF/ElasticNet/XGBoost +
SHAP, leakage-free; SHAP independently re-found cg05575921/AHRR = strong validation). P7 power
done (19_power.py). P8 deliverable = scripts/revize/realdata/MAKALE_GERCEK.md (genuine Turkish
IMRaD). The fabricated scripts/revize/makale.txt was LEFT INTACT on purpose as the audit trail
(REPORT.md maps fabrication->real); do NOT overwrite it. DunedinPACE/GrimAge declared
not-reproducible (gated/needs R). Before finishing, FDR<0.05 counts in the manuscript were
re-verified against out/*_dmp.csv (all 6 match) — keep doing this consistency check.

## Genuine DOCX builder (render from markdown, single source of truth)
The accepted deliverable's DOCX is rendered FROM MAKALE_GERCEK.md by build/build_gercek_md.cjs
→ build/MAKALE_GERCEK.docx (content never hand-typed, so text↔docx can't drift). It legitimately
has ~7 tables (NOT the fabricated 27) and NO figures — the original 14 figures + brain image
visualize fabricated data, so putting them in a "genuine" doc would itself be fabrication
(Zero-Hallucination); PRISMA is kept as a text/code block. Journal format via lib.cjs: title
14pt/sz28, headings 12pt/sz24, body 11pt/sz22, tables 9pt/sz18, refs 8.5pt/sz17, A4 narrow
(720twip), kerning(`<w:spacing w:val>`)=0, gray-shd D9D9D9=0. The OLD build_gercek.cjs →
makale_gercek.docx is the REJECTED smoking-only short version — superseded, do not use it.
Self-verify the docx with python zipfile/XML (well-formed, table count, sz set, kerning/shd=0,
key numbers present) since architect content-blocks this repo.

## GitHub push (T4) is blocked beyond just the token
`git push` to a clean GitHub repo is NOT currently possible: the repo already TRACKS ~1617 large
binaries under attached_assets incl. a 1.6GB zip (gdrive/epiclock/EpiClockPrototype.zip) and many
>100MB files (research_corpus/*.pdf, scripts/sinerji_dump/*.json). GitHub rejects >100MB blobs and
.gitignore does NOT untrack already-committed files, so a naive push fails. realdata/data (5.3GB)
is already gitignored (`data/` rule); attached_assets is not. A clean push needs a scope decision —
(a) push only scripts/revize as a fresh repo, (b) Git LFS, or (c) history rewrite (destructive) —
PLUS GITHUB_TOKEN. This is a genuine user decision/access; do NOT autonomously rewrite history.

## Gerçek-veri verdict (in-place revize, doğrulanmış)
- Derin analiz = 6 madde GEO kohortu, n=742 (sigara GSE50660 n=464, alkol-kan GSE110043 n=94, alkol-beyin GSE49393 n=48, kokain GSE77056 n=47, meth GSE154971 n=24, opioid-beyin GSE98203 n=65). Makalenin n=10542 entegre kohortu UYDURMA.
- **En kritik bulgu:** gerçek Horvath EAA (vaka−kontrol) KÜÇÜK ve NEGATİF (alkol-beyin −0.82y, kokain −0.66y, opioid-beyin −1.48y) → makalenin "+2.8…+7.3y hızlanmış yaşlanma" iddiasının TERSİ. Gerçek veri hızlanmayı desteklemiyor.
- Zenginleştirme ZAYIF: sigara GO yalnız 2 terim FDR<0.05 (her ikisi 0.023); KEGG hiçbir yolak FDR<0.05 (en iyi 0.168).
- Saatler (GSE50660): Horvath MAE 3.51/R²0.586, Hannum 7.82/0.641, PhenoAge 6.77/0.565. GrimAge 450K beta'dan hesaplanamaz.
- Sınıflandırıcı AUC (sızıntısız CV): sigara 0.928, alkol 0.926, kokain 1.0, meth 0.922.
- **Asla doldurulamaz (veri yok):** t7 mediasyon(HOMA-IR/kortizol/CRP-IL6), t8 moderasyon(DERS/SCS-B), t9 PMI, t10 doku-pH, t16/t17(bireysel fenotip), t24/t26 kısmen — bireysel fenotip kamuya açık metilasyon setinde yok.
- İlerleme izleyici: scripts/revize/TABLO_DURUM.md (tablo-tablo durum). Dönüştü: t1,t2,t4,t5,t6 (gerçek); t7-t10 (veri yok). Bekliyor: t3 (veri hazır, hassas p sonraki tur), t11-t27 (literatür/web-doğrulama + prose senkronu).

## Figure fabrication map (figs_main.py / figs_supp.py — matplotlib, data-driven)
- figs_main.py HARDCODES fabricated numbers: clock MAE/RMSE (L20/40), per-substance EAA eaa=[0,3.2,4.8,5.1,6.2,2.1,7.3] (L97), Cohen's d incl meth 1.03 (L118-123), EAA summary table +6.2/+7.3 (L171-172), footer "ANOVA F(6,10535) n=10.542" (L176), regional brain PFC+5.3/NAc+4.1/VTA+2.8 n=48/36/18 (L387-431), demographic table n=2183 etc (L319-372).
- REAL values: clock Horvath MAE3.51 R2.586 / Hannum7.82 .641 / PhenoAge6.77 .565; EAA small NEGATIVE alcohol-brain-0.82 cocaine-0.66 opioid-brain-1.48 (meth EAA NA no chrono age); DMP FDR<0.05 smoking89 cocaine11987 meth398 opioid12 alcohol-brain8 alcohol-blood4387; classify AUC cocaine1.0 smoking.928 alcohol.926 meth.922.
- UNREPRODUCIBLE figures (no real data): fig3 mediation, fig5 regional-brain subdivisions (only whole-tissue EAA for 2 brain cohorts), fig6 reversibility, Cohen's d. -> repurpose to real (DMP/GO-KEGG/AUC) or honest veri-yok; keep anatomical brain image, drop fake regional markers.

## Figures + Discussion tables: DONE this session (verified)
- ALL 6 main figures regenerated DATA-DRIVEN (figs_main.py loads realdata/out JSON at runtime, zero hardcoded fab) + ALL 6 legends rewritten LINE-LOCKED in makale.txt (spans 1669-1758, total stays 1886): fig1=3-clock perf, fig2=negative-NS EAA, fig3 REPURPOSED→DMP counts/smoking SHAP/GO, fig4=cohort n=742, fig5=brain whole-tissue (anatomical image INTACT, 2 cohorts neg-NS, no regional/PMI), fig6 REPURPOSED→per-substance classification AUC.
- Discussion tables (tables.cjs) corrected to real: t23 (own EAA→negative-NS), t24 (ensemble/`%61`/n=108-PMI/3-brain-region claims→honest), t25 (brain→whole-tissue 2 cohorts neg-NS), t27 (aggregate AUC 0.867→per-substance AUC). t7-t10 already veri-yok. Build edits to tables.cjs do NOT change makale.txt line count.
- Legend line-lock helper: build/relegend.cjs splices 6 blocks by line index with length asserts.

## DECIMAL RULE for real content (fixes.cjs comma-thousands stripper)
- fixes.cjs strips comma+exactly-3-digits as a thousands sep -> CORRUPTS Turkish 3-digit decimals: "0,922"->"0922", "1,000"->"1000", "0,928"->"0928". Comma+2-digit ("-0,82","FDR<0,05") is SAFE; period-thousands ("11.987","4.387") and period-decimals ("0.922","p=0.003") are SAFE.
- RULE: in all REAL content I author (prose, tables.cjs, legends) write decimals with PERIOD (0.922, p=0.003, MAE 3.51) and thousands with period (11.987). Never a comma before 3 digits.
- Verify after build: extract paras and check AUC/p render as "0.922" not "0922"; mangle-scan regex \b0\d{3,}\b has FALSE POSITIVES (matches fraction of legit 0.0046) so confirm by reading context.

## DELIVERABLE COMPLETE — where the two-revision-doc conformance actually lives
The rendered build/makale_revize.docx is essentially clean and conformed; do NOT re-hunt
makale.txt prose for fabrication — most legacy fixed-width fabricated tables in makale.txt
are DROPPED at build (renderStream gridLike-detection) and replaced by tables.cjs t1–t27.
- **All tables real:** tables.cjs t1–t27 carry real values or honest "veri yok"; the DOCX
  scan confirms n=742, 6 GEO accessions, Horvath 3.51, EAA −0.82/−0.66/−1.48, DMP
  89/4387/11987/398/12/8, per-substance AUC 0.928/0.926/1.000/0.922, "veri yok" ~188×.
- **Reviewer Doc 1 (terminology) is ALL in fixes.cjs PHRASE_FIXES** (verified rendered):
  splicing/elongasyon→Türkçe+parenthetical, diferansiyasyon→farklılaşma, mediye→aracılığı,
  modere→düzenle* (incl. "edip etmediği"), Nükleus Akkumbens, hipokampus, veri tabanı,
  etiyoloji, invaziv, superior→üstün, R², supplementary veriler→ek veriler, Ek Şekil S→Ek,
  citation-to-sentence-end (2 Horvath), thousands-comma stripper. etyoloji/invazif fixes are
  no-ops (words absent in source) — harmless.
- **Reviewer Doc 1 (structure) is ALL in build.cjs** (verified rendered): "3. BULGULAR VE
  YORUMLAR" merged heading + 4.x interpretations moved inline (HM map + renderStream order),
  27 tables consolidated→10 sequential composites with a citing sentence before each
  (tableRefSentence), KISALTMALAR moved after abstract (was Ek1), KAYNAKÇA sequential w/ the
  "23-75:" splitter dropped (reflowReferences), single-author Yazar Katkıları, Ek figures
  numbered, main Şekil 1–6 inline at their section, fig5 brain whole-tissue (no fake regional).
- **Reviewer Doc 2 (point sizes) via lib.cjs:** title 14pt/sz28, section 12pt/sz24, body
  11pt/sz22, abstract+KISALTMALAR 10pt/sz20, tables+captions+legends 9pt/sz18, KAYNAKÇA
  8.5pt/sz17. NOTE: very wide composite tables (≥8 cols, e.g. t3 group) AUTO-SHRINK to 7–8pt
  (sz14/sz16) in lib.cjs to fit A4 — accepted exception, not a bug; no super/subscript used.
- **Only "fabrication" left in the DOCX is deliberate honest disclosure** (KEEP, do not fix):
  "10.542 referans profillik … veri tabanı kurulmamıştır", "makalenin uydurma %87,3 … iddiasının
  gerçek karşılığı", and "'+5.3/+4.1/+3.2 yıl bölgesel hızlanma' iddiasını desteklememektedir".
  The +3.2 in t23 is Monick et al.'s REAL cited literature value, not own data.
- **Abstract is English-only by source design** (makale.txt 14–23 ABSTRACT + 42–43 Keywords);
  there is NO Turkish Öz/Anahtar Kelimeler and NEITHER revision doc asked for one — do not add
  (Zero-Hallucination + scope). Reviewer's Turkish-text rule (line 50) is about figures/appendices.
- Verify after any rebuild via python zipfile/XML (architect content-blocks this repo): XML
  well-formed, 14 <a:blip>, fab tells only in the 3 honest-callout contexts, real tells present,
  sz set matches above. Build: `cd scripts/revize && node build/build.cjs`.
- Still open & user-gated (unchanged): GitHub push (needs GITHUB_TOKEN + scope/history decision).
