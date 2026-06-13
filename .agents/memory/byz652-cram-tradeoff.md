---
name: BYZ652 cram-sheet margin vs content tension
description: Why a hard-locked tiny page margin cannot coexist with "2 full pages" under zero-hallucination + no-repetition, and how the conflict was resolved.
---

# Cram-sheet: locked margin vs "fill exactly N full pages"

When a user demands BOTH (a) a hard-coded tiny page margin AND (b) "every column completely
full across exactly N pages" AND (c) zero-hallucination + absolute no-repetition, the three are
mutually impossible past the point where genuine, non-duplicated, source-verified content runs out
(~45-50k chars for this 4-col 4.5pt landscape sheet).

**Resolution / priority order (durable):** zero-hallucination and no-repetition WIN. The page
margin is the variable that yields — never pad with fabricated or repeated text to fill space.

**Why:** replit.md makes zero-hallucination + no-repetition non-negotiable for Dr. Nurcan; "fully
packed pages" is an aesthetic goal. Padding to fill would violate the hard rule to satisfy the soft one.

**How to apply:** parameterize the margin (env var), sweep it to find the largest value that still
yields the target page count (= maximally packed), and set that as default. Be transparent with the
user that the margin was relaxed to keep content genuine. Each round of dedup REDUCES content, so the
2-page tipping margin DRIFTS UP after every dedup pass — always re-sweep after editing content.

# Target renderer matters: Word 365 packs ~1.23x denser than LibreOffice

The deliverable is opened/printed in **Microsoft 365 Word**, but only LibreOffice (`soffice`) is
available to render here. Word fits ~1.23x MORE text per page than LibreOffice for the same docx.
So tuning the margin to give "exactly 2 LibreOffice pages" UNDERSHOOTS Word — Word then shows ~1.5
of 8 columns EMPTY on page 2. **To fill N full WORD pages, tune the margin so LibreOffice reaches
N×1.23 EFFECTIVE pages, not N.** Measure effective LO pages by char count, not page count:
effLO = (pageCount-1) + (chars_on_last_page / chars_on_page1); Word ≈ effLO / 1.23. For this sheet,
margin ~1130 twip → effLO≈2.46 → Word≈2.00 (page 2 full, no spill to a 3rd Word page) AFTER adding the patterns below; the tipping margin DROPS as genuine content grows.

**Content was NOT actually exhausted (lesson):** when the user opened the file and applied Word's own "Narrow" margin preset, page 2 left ~1.5 of 8 columns empty — the honest fix is MORE genuine content, not a wider margin or padding. Re-mining `ders_notu.txt` with `grep -iE "Pattern (for|–|-)"` surfaced 6 genuinely-missing real SAIP patterns (Service Mesh, Load Balancer, Throttling, Map-Reduce — performance; Intercepting Validator, IPS — security) NOT yet in the sheet (Circuit Breaker already was). Added them → content 46k→54k chars. ALWAYS systematically enumerate named patterns/tactics in the source before concluding "content exhausted." NOTE the explorer re-flagged the 7 ordering sequences that were ALREADY in the SIRALAMA section, and HALLUCINATED anti-patterns (God Object/Big Ball of Mud/Distributed Monolith/Golden Hammer) that grep found NOWHERE in doc51/ders_notu — never add an explorer's claim without grepping the source first.

**Why:** fixed genuine content + locked Cambria sz=9 + 6pt-exact line means the ONLY honest lever to
fill more page area is the margin (no fabricated padding). Bigger margin spreads fixed content over
more area → fills more Word columns. **How to apply:** aim Word≈1.97-2.00 (slightly under full) so it
fills without overflowing into a 3rd page; cannot verify Word directly — ask user to confirm in Word.

# Architect "repetition" reviews: verify before complying

The code-review architect repeatedly flagged "cross-section repetition" that was often just TOPICAL
grouping (e.g. three sections each covering DIFFERENT middleware techs / different patterns), not the
verbatim duplication the rule actually targets. Before acting on a repetition flag: grep the actual
strings and confirm literal/near-literal duplication. Real dups found were: a brief tech one-liner
duplicating a later detailed section, and a whole "EK DETAYLAR" section restating an earlier list.
Fix by folding net-new specifics into the single canonical section and deleting the duplicate.

Also: architect flagged source-verified numbers (~%80 maintenance cost, %99.999 five-nines) as
"unsourced" — they were in the vetted source files. BUT the reverse also happened: architect flagged
Avro "~3-10x smaller / ~20-100x faster" and those were genuinely NOT in ders_notu.txt (source had
only the slide titles "Data size Comparison" / "CPU Overhead", no values) — a real fabrication that
had to become qualitative. Lesson: grep the SPECIFIC number in the source every time; some flags are
false (keep) and some are real (must remove). Never trust your own prior "verified" note for a number
without re-grepping — that is how the Avro numbers slipped in.
