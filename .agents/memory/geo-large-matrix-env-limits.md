---
name: GEO large supplementary matrix — Replit env limits
description: Why huge GEO beta matrices (multi-GB gz) can't be processed in this env, plus the download/decompress gotchas hit while trying.
---

# Processing huge GEO methylation matrices in the Replit env

Context: GSE125105 normalized beta matrix (`GSE125105_matrix_normalized.txt.gz`, 3.5 GB
gzip, 699 samples × ~485k CpG). Goal was to extract ~887 epigenetic-clock CpG rows.

## Hard wall: single-pass decompression > 120s/call
- The matrix decompresses to ~12–17 GB plain text; measured decompression throughput
  <122 MB/s (CPU-bound, even with `libdeflate-gzip`, not disk — disk read was 187 MB/s).
- A full `zcat|grep` / `libdeflate-gzip -dc` pass needs ~130–200s — exceeds this env's
  **~120s per bash-call execution limit**. gzip is a single stream → cannot be split,
  paused, or resumed mid-decompress. Building a gzip random-access index also needs one
  full pass. So a big single-member gz simply cannot be fully scanned here.
- **Why:** every clock CpG row requires scanning all 485k probe rows = full decompress.
  Subsetting sample columns does NOT reduce the decompress cost (cost is per-row read).
- **How to apply:** for any GEO supplementary matrix more than ~1.5 GB gzip, don't try to
  decompress it whole in one call. Prefer the small `*_series_matrix.txt.gz` (metadata,
  KB-sized) for phenotype/labels, and declare the per-CpG computation "not reproducible in
  this env" per Zero-Hallucination. The committed engine (e.g. `14_depression.py`) stays
  reproducible on a bigger machine / Colab with the recorded data SHA.

## Background jobs are unreliable across call boundaries
- `nohup setsid bash -c '...' & disown` survives WITHIN a call and sometimes ONE boundary,
  but then stalls (output frozen while process still listed) and dies at a later boundary.
  Do NOT rely on background jobs spanning multiple tool calls here. Anything that must
  finish has to fit inside one ≤120s foreground call.

## Download gotchas (cost real time — avoid repeating)
- `curl --max-time 115` silently TRUNCATES a large download at the time limit → produces a
  partial gz that fails late with `gzip: unexpected end of file` and only partial matches.
  **Always** verify size vs server `Content-Length`, and resume with `curl -C - -o file`
  (NCBI HTTPS honors `Accept-Ranges: bytes`). Re-run resume until bytes == Content-Length.
- `tail -c4 file.gz | od -An -tu4` = gzip ISIZE = decompressed size **mod 2^32** (ambiguous
  if >4 GB; only the low bits).
- `zcat file | head -1` can hang: some zcat ignore SIGPIPE and decompress the whole file
  before exiting. Get a gz header line via Python `gzip.open().readline()` instead.

## pkill self-kill
- `pkill -f '<pattern>'` matches your OWN current shell's command line if the pattern text
  appears in the command you're running → kills your shell (exit 143, no output). Never
  `pkill -f` on a string that is present in the very command issuing it; use a PID/PGID or
  a `ps | grep '[x]...'` bracket trick instead.

## NCBI esummary paging pitfall (silent screening loss)
When paging db=gds esummary in chunks (id lists >~60), each call's JSON `result["uids"]`
lists ONLY that chunk. If you merge chunks with `dict.update(result)`, the later "uids"
CLOBBERS the earlier one, so you iterate only the LAST chunk and silently drop the most
relevant (top-ranked) records. Fix: accumulate uids into your own ordered list across chunks.
Symptom seen: cocaine/opioid/cannabis screened to 0 hits (wrong) until fixed.

## Workaround that DID beat the decompress wall (for a CLASSIFIER candidate pool)
A classifier needs a *label-blind probe pool*, not clock-specific rows. `timeout ~105 bash -c
"zcat matrix | head -80001 > prefix.tsv"` grabs header + first 80k probe rows in ONE foreground
call (~30s; head stops early, timeout reaps the lingering zcat). Probe FILE POSITION is independent
of the sample outcome -> the prefix is a leakage-free (partial-genome) pool. Then awk-slice
beta-only columns (drop *_DetectionPval: header even fields, data odd fields >=3; data row cg=$2)
before pandas. This is how the GSE125105 depression classifier got built without the full 3.3GB pass.
**Why:** full-matrix passes AND background jobs both fail here; a position-based prefix is the only
label-blind pool that fits one call. **Perf trap:** pandas `df.T.fillna(series).T` on an 80k x 699
frame blows the 120s wall — impute with numpy (`np.nanmean(A,1)` + boolean-index fill) instead.

## GSE125105 depression — real findings (durable)
- Cell-adjusted epigenetic AGE-ACCELERATION: depressed > control, PhenoAge Welch p=0.0015 / MWU
  0.0019 (Horvath & Hannum NS). This is the strong, defensible depression-methylation signal.
- Direct MDD case/control CLASSIFIER (partial-genome 80k pool, leakage-free 5-fold) OOF AUC ~= 0.61
  only -> MDD blood methylation is a weak, cell-confounded signal. Report exploratory, never Dx.

## Substance series-matrix tractability (this env decompress/mem wall)
Tractable (downloaded, parse OK): GSE154971 meth 450K 61MB; GSE49393 alcohol-PFC 450K 20MB;
GSE66348 rat-NAc-cocaine 35MB; GSE110043 alcohol-blood 347MB (already in data/).
WALLED / no single series_matrix: GSE147040 smk-NAc 1.5GB (too big); GSE235818/GSE164822
(opioid) + GSE293262 (meth EPIC) + GSE87571 (aging ctrl) give NO single series_matrix.txt.gz
(supplementary/raw only -> need IDAT/minfi we don't have). Declare these as env-blocked.

## "Stub series-matrix + betas in supplementary" — check before declaring a set unusable
- A tiny series_matrix.txt.gz (~22-40 KB) is a METADATA-ONLY STUB: betas are NOT inside it,
  they live in `suppl/`. Confirm via `curl -sI .../matrix/...txt.gz` Content-Length. Do NOT
  conclude "veri yok" from a stub — list `suppl/` next.
- Many EPIC suppl matrices are a "processed_signals" CSV where each sample has TWO interleaved
  columns: a direct BETA value column + a `*_Detection_Pval` column (header width = 1+N*2).
  This IS usable — the beta cols are the odd data fields (2,4,6,...).
- Even an 8 GB suppl gz is sliceable in one call without full decompress (the head trick stops
  the stream early): `curl -s --max-time 110 URL | zcat | head -40001 | cut -d',' -f1,$(seq -s, 2 2 N) | tr -d '"' > slice.csv`
  -> first ~40k array-order probes, beta cols only, ~60-100s. Labels come from the stub
  (`!Sample_title` first token = sentrix id == suppl column name; map to phenotype). This is how
  the schizophrenia GSE152026 (8 GB) classifier got built. See `scripts/revize/realdata/SLICE_PROVENANCE.md`.
- Trainer guard against silent slice corruption: assert no surviving `*_Detection_Pval` column
  and assert exact expected label counts (fail loudly on GEO format / label drift).

## Per-fold impute memory trap (big partial-genome matrix)
For publishable leakage-free OOF, impute/feature-select/scale_pos_weight must be TRAIN-only per
fold. On a ~934 x 40k matrix, `np.where(np.isnan(M[tr]), mu, M[tr])` per fold (2 full-matrix
copies x5) blows RAM/time and gets the process killed. Fix: fill IN-PLACE on the fancy-index
copy -> `Xtr=M[tr]; b=np.isnan(Xtr); Xtr[b]=mu[np.where(b)[1]]` + `del Xtr,Xte,b` each fold.
Drops peak memory enough to finish in ~80s. (Small matrices like 119 x 120k don't hit this.)
