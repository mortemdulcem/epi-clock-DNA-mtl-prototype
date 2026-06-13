---
name: BYZ652 doc51.txt question-bank parsing
description: Non-obvious structure traps when parsing scripts/arch/doc51.txt (232-block exam Q&A) for the BYZ652 cram DOCX
---

Parsing `scripts/arch/doc51.txt` (BYZ652 software-architecture exam bank) faithfully (zero-hallucination) has three traps learned the hard way:

- **Split blocks ONLY on line-start `\nSoru N`.** This yields exactly 232 blocks. Do NOT globally replace form-feed `\x0c` with `\n` before splitting: the file's Appendix B ("Ekler B — Taktik Temelli Anketler") has survey rows like "Taktik Soru 11" separated by page-break `\x0c`; a global replace promotes them to false question boundaries (232 → 247).
- **Cevap:/Açıklama: markers are sometimes prefixed by `\x0c`** (12 of them). Fix by normalizing `\x0c`→`\n` *inside each block* (after the Soru split) and using a leading-whitespace-tolerant regex `\n[ \t]*Cevap[ \t]*:`. Otherwise those 12 answers parse empty.
- **3 blocks (source-num 10, 25, 26) genuinely have NO `Cevap:`** — they are Appendix B tactics-checklist items, not answerable Q&A; block 10 also absorbs the whole inline Appendix B checklist (~21k chars). Per zero-hallucination, render them as plain text with NO fabricated answer. Integrity assert pins the answerless set to exactly {10,25,26}; counts: 232 blocks = 229 answered + 3 checklist, 123 with açıklama.

**Why:** faithful reproduction is mandatory (Dr. Nurcan zero-hallucination rules); silent mis-splits or invented answers violate it.
**How to apply:** when regenerating the cram DOCX via `scripts/arch/build_byz652_cram.py`, keep these invariants; the build's runtime asserts will fail loudly if boundaries drift.

**Coverage audit result (cram sheet vs all 232 blocks):** after a full audit the 2-page summary now carries the knowledge for ~all 232. The previously-missing named SAAP/Bass tactics were ADDED compactly and margin re-tuned 1240→1220 to still fit ~2 Word pages: Sanity Checking (availability detect-faults), Limit Nondeterminism + Executable Assertions + data source abstraction (testability), change default settings + message-delay & replay detection (security), peer-review vs outsider evaluation + tactic-survey columns "Supported E/H"+"Rationale" (evaluation). NOTE Locate & Orchestrate were ALREADY present (interoperability section) — explorers wrongly flagged them; always grep the file before trusting a coverage-gap claim.

**Numbering trap:** "Soru N" integers RESET across sections — splitting an audit by integer 1-232 is wrong. Two parts: blocks 1-155 (multiple-choice/matching/ordering, integers reset per sub-section, reach ~112) and blocks 156-232 = a second "Soru 1-37 — <topic>" detailed tactic-sequence essay set starting ~line 2613. Audit/partition by BLOCK ordinal (line-start `^Soru `), not by the printed integer.

**DOCX page-count tuning (no renderer available):** environment has no LibreOffice/Chromium/weasyprint, so exact Word pagination can't be measured. The spec locks 4.5pt Cambria / 6pt exact line / landscape A4 / 4 columns / no para spacing, so the ONLY legitimate lever to change page count is margins + column-gap. Geometry estimate at min margins (80 twip): ~193k visible chars ≈ ~7.5–8 pages (realistic ~66–70 chars/line for justified narrow Turkish columns).
