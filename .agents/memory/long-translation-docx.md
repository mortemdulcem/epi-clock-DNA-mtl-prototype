---
name: Long LLM book translation -> DOCX pitfalls
description: Recurring failure modes when translating a large book chunk-by-chunk via LLM and assembling raw-XML DOCX
---

# Chunked LLM translation -> raw-XML DOCX: recurring failures

**Sentinel/marker corruption (most common).** When the source uses sentinel markers (e.g. figure markers `⟦FIG:x⟧…⟦/FIG⟧`), the model sporadically wraps *unrelated* spans in the same bracket characters — in-text citations (`⟦131⟧`), figure call-outs (`⟦Şekiller 9.11⟧`), or headings (`⟦ANALYSIS REPORT…⟧`), often leaving an orphan close tag.
**How to apply:** never trust only open==close==complete counts. Strip all *complete* marker blocks first, then assert ZERO remaining bracket chars anywhere. Re-translate offending chunks from clean source, then re-scan until zero.

**Markdown leakage.** Even with a "no markdown" prompt, the model injects `###`/`####` headings, `**bold**`, `---` rules, and exotic unicode spaces (`\u2003` em-space). These are NOT in the source — convert (# -> heading by level, ** -> bold run) or drop (---), don't render literally.

**Invalid XML 1.0 control chars.** Translations can contain control chars like `\x07`. An XML escaper that only handles `& < > "` will produce a non-well-formed document.xml. Always also strip `[\x00-\x08\x0B\x0C\x0E-\x1F]` (keep \t \n \r).
**Why:** Word/ET both reject these as "invalid token"; failure surfaces only at final validation.

**Validation must be end-to-end.** Parse all 4 key parts (`[Content_Types].xml`, `_rels/.rels`, `word/document.xml`, `word/_rels/document.xml.rels`) with a real XML parser; assert every `r:embed` id resolves to a relId whose Target exists in `word/media/`.

**Page-furniture removal is safe & expected.** Dropping standalone `^\d{1,3}$` lines is page numbers, not content — verify by confirming all dropped values fall within the book's page count and none are large outliers.

**Editing pdftotext-derived verbatim source (sentence boundaries split across physical lines).** In a `pdftotext`-extracted source, a sentence-ending token frequently sits at end-of-line while the next sentence's first word starts the next physical line (e.g. `…göstermektedir.` then newline then `Ancak, …`). An exact-match edit whose `old_string` spans that boundary fails. **How to apply:** keep `old_string` within a single physical line; anchor on a unique substring before the period, not across it. The build's reflow joins lines with single spaces, so inline parentheticals you insert (e.g. `(Ek Şekil S3)`) survive reflow unchanged.

**On-image text vs. caption (figure-overlay pipeline).** To remove text baked into a figure image, set the overlay op's `text:""` (renderer fills the box with detected bg → original cleared, nothing drawn) rather than deleting the op (which would leave the original English showing). Figure number+name belong in the DOCX caption only; supplementary captions get their name from the build's `label` field (which does NOT pass through applyFixes — write final Turkish directly).

## Verbatim DOCX reorg via renderStream sub-ranges (revize pipeline)
To reorganize sections of a verbatim-source DOCX (reviewer asks "move interpretation next to its results table") **without rewriting any sentence**: replace the single full-range render call with an ordered list of `renderStream(from,to)` sub-range calls in the desired reading order, and override each moved heading's section number in the heading-map (HM). Content stays byte-identical (relocation only) — fully zero-hallucination.
**Why table numbering stays correct:** table numbers come from a *fixed source-order OLD→index map*, independent of render order. Reordering is safe for ascending table order **only if** the moved blocks are prose-only and the one table-bearing block moves as a whole unit (then tables still appear 1..N ascending).
**Verify empirically** (architect/code_review is persistently content-policy-blocked on this repo's Turkish forensic-medical text): read `word/document.xml` with python zipfile, regex-extract paragraphs, assert heading flow + `Tablo N` captions == range(1,N+1) ascending + each moved subsection's signature sentence count.
**Gotcha:** identical sentences can legitimately appear twice in the source (e.g. same opening line in Özet *and* Sonuç) — preserve both, do NOT dedupe.

## Figure readability in DOCX ≠ DPI metadata
When a reviewer says embedded figures are "low resolution / text unreadable", check the
*source* image native size and the *display* size, not just the embedded dpi tag. Symptom seen:
embedded JPGs were 300 dpi / ~3198px, but the English source charts were only ~1600px (2× LANCZOS
upscale), and they were placed at a small content width — so dense 4–6 panel composites had
physically tiny (~3–4pt) sub-labels. Levers that actually help, in order: (1) enlarge the on-page
display size (full content width, raise height cap); (2) landscape full-page for wide dense
composites; (3) split composites into per-panel figures. Re-rendering at higher --scale only
sharpens edges (already >300ppi at display size) and bloats the file — it does NOT make small text
bigger. **Why:** readability is governed by physical text size on the page, not pixel count.
**How to apply:** for this repo, figure overlay pipeline is `scripts/revize/figtrans/` (media_en →
Turkish overlay → media); display size set in `build/build.cjs` imageP call + `build/lib.cjs` imageP maxHcm cap.
