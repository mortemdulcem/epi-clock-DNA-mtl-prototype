---
name: Fixed-width text table -> DOCX parsing
description: How to faithfully parse plain-text fixed-width tables (e.g. an "Ek/Appendix" code-architecture table) into clean DOCX cells without chopping words.
---

# Parsing fixed-width plain-text tables into clean table cells

Source tables pasted from a tool/PDF are laid out by spaces, NOT tabs, and the
column positions are NOT stable across the whole table — different section bands
shift a column a few chars left/right (e.g. the "software" column at char ~75 in
some bands, ~77 in others). A single global set of char-position column
boundaries WILL misbucket the minority bands (a value lands one column early and
its real column goes empty).

**Rule that works (use this ordering):**
1. Detect section-band title lines first (a single all-caps token near the left
   margin). A band title can itself wrap, and a trailing single-letter piece is a
   wrapped suffix — join it to the previous word WITHOUT a space
   (`STANDARTLAR` + `I` -> `STANDARTLARI`), not with one.
2. A *full* data row is exactly N single-token cells (cells keep their internal
   single spaces because you tokenize on runs of >=2 spaces). So when a line has
   exactly N tokens and starts at the left margin, assign tokens **positionally**
   (token i -> column i) and ignore char positions entirely. This is immune to the
   per-band alignment drift.
3. Only *partial* lines (an empty cell, or a wrapped continuation) fall back to
   char-position bucketing to decide which columns they touch. A line that is
   indented OR fills <= 3 columns is a continuation of the previous row.

**Joining wrapped continuations — space vs no-space (the subtle part):**
- A column of snake_case identifiers wraps mid-token
  (`deep_learning_methyla` + `tion`) -> rejoin with NO space.
- A 1-2 char lowercase fragment is a mid-word completion
  (`PubChe` + `m` -> `PubChem`; `Anonimleştirilmi` + `ş veri` ->
  `Anonimleştirilmiş veri`) -> attach with NO space (then any remaining words in
  that fragment keep their spaces).
- Everything else (a full lowercase/Capitalized word continuation: `boyut` +
  `indirgeme`, `CpG` + `markers`, `Ensemble` + `Ağırlıkları`) wraps at a word
  boundary -> join WITH a space.
- Positional char-offset heuristics for "did the fragment reach the column edge"
  are NOT reliable here (forced-break vs word-wrap end-distances overlap, and the
  last column has no right edge). The token-length/case rule above is what works.

**Why:** the user reported "tüm tablolar bozuk" because an earlier version sliced
data rows at HEADER-derived char positions, chopping words mid-cell across the
band-alignment shifts. Positional assignment for full rows + the join rules above
produced intact, correctly-aligned cells across all 14 bands.

**How to apply:** any time you reconstruct a space-delimited fixed-width table
into real table cells (DOCX/HTML), prefer positional token mapping for full rows
and reserve char-position bucketing for partial/continuation lines only.
