---
name: makale_revize journal/template + reviewer conformance
description: Authoritative external spec (2 Google Docs) the epigenetics article DOCX must match, and its point-size rules.
---
The `scripts/revize/build/makale_revize.docx` revision must conform to TWO authoritative external specs the user supplies as Google Docs (export via `curl -sL "https://docs.google.com/document/d/<ID>/export?format=txt"`):
1. **Reviewer correction list** — page-by-page terminology/structure fixes (Turkify English terms but keep "Türkçe (English)" parenthetical convention, e.g. "uç birleştirme (splicing)"; reference titles in KAYNAKÇA stay English; sequential table renumbering; citing paragraph before every table; "BULGULAR VE YORUMLAR" heading flow; real single-author CRediT; abbreviations under KISALTMALAR after abstract; appendix figures numbered Ek N with legend paragraph).
2. **Journal template** — point sizes (half-point sz in lib.cjs): title 14pt (28), section headings 12pt (24), body 11pt (22), tables+figure captions 9pt (18), **KAYNAKÇA 8.5pt (17)**.

**Why:** build.cjs once drifted references to 10pt (sz=20) even though lib.cjs header documents "references 17" — easy to miss because 67 refs all looked fine otherwise.
**How to apply:** after any rebuild, verify per-section sz with a zipfile/XML scan, not just the REPORT counts. REPORT should stay {abbr:40, refs:67, mainFigures:6, supplementary:8, tables:27}, 14 `<a:blip>`.

**Verified-OK deviations (do NOT "fix" — they are intentional, not bugs):**
- Wide composite tables auto-shrink to sz=16 (8pt) / sz=14 (7pt) to fit A4 width; the other ~1269 table cells stay sz=18 (9pt). Forcing all tables to 9pt overflows the page. Expect sz 14/16 ONLY inside `<w:tbl>`.
- Author affiliations, keywords, and KISALTMALAR abbreviation entries render at sz=20 (10pt) — template doesn't size these; fine.
- ~28 empty sz=8 (4pt) paragraphs are deliberate minimal separators preventing table/figure↔text overlap (replit.md anti-overlap rule beats the strip-empty-paragraph rule here).
- Body is sz=22 (11pt) per the JOURNAL TEMPLATE (spec doc 2), which overrides replit.md's generic 10pt rule for this article.
