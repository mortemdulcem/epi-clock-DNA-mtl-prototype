---
name: Enrichr CSV parsing + Turkish comma-decimal DOCX numbers
description: Two gotchas when turning Enrichr GO/KEGG output and seeded stats into a Turkish reproducible DOCX.
---

## Enrichr GO/KEGG CSV: term names contain UNQUOTED commas
gseapy/Enrichr `*_KEGG_2021_Human.csv` / `*_GO_Biological_Process_2021.csv` write the
`Term` column with literal commas (e.g. "Glycine, serine and threonine metabolism") and
do NOT quote it. So `awk -F,` / naive split-by-comma shifts every later column and gives
garbage (once produced a fake "min adjP=0,03, 1 significant" KEGG result that was pure
parsing artifact). **Always parse these CSVs with python `csv.DictReader`**, never awk.
Verified-correct KEGG for the smoking rebuild: 98 terms, 0 at FDR<0.05, min adjusted
p=0.167995 ("Pathways in cancer").

**Why:** comma-in-field + unquoted = column drift; the artifact looked like a real
positive and nearly got reported, violating zero-hallucination.

## Never run fixes.cjs `stripThousands` on comma-decimal content
`scripts/revize/build/fixes.cjs` `stripThousands` removes thousands commas
(`1,234`→`1234`) for the OLD fabricated text. Turkish decimals use a comma
(`0,245`, `3,51`, `0,016`) and match the SAME pattern → it would corrupt them
(`0,245`→`0245`). The genuine-article builder `build_gercek.cjs` deliberately does NOT
require fixes.cjs; it writes correct Turkish prose from scratch and formats numbers with
its own `dec()`/`sci()` helpers (period = thousands, comma = decimal, U+2212 minus,
superscript sci-notation). Verify output with a python `<w:t>` text grep for
`0245`/`undefined`/`NaN`/mojibake = 0.

**Why:** a single regex pass silently turned real decimals into wrong integers.

## Genuine smoking-axis rebuild location
`scripts/revize/build/build_gercek.cjs` (run: `cd scripts/revize && node build/build_gercek.cjs`)
reads numbers straight from `realdata/out/*.json` + `realdata/data/manifest.json`,
embeds the 4 Turkish figures, outputs `build/makale_gercek.docx`. It replaces the
fabricated epigenetics article; every number is real-sourced or seeded computation, and
unreproducible original claims are declared in appendix "Ek 3".
