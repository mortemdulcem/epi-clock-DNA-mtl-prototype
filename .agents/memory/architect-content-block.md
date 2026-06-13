---
name: Architect blocked on forensic/medical content
description: The code_review/architect subagent refuses this repo's Turkish forensic/medical text; self-verify instead.
---

# Architect / code_review is content-policy-blocked on this repo's academic content

When working on the Turkish forensic-medicine / clinical academic documents in this
repo (e.g. `scripts/revize/` DOCX pipelines, TOMEC, thesis material), the
`code_review` skill's `architect()` subagent returns *"Agent declined to respond …
content policy"* — even when the task is framed as a pure code-logic review and only
the build scripts (`.cjs`) are passed as `relevantFiles`. The mere presence of the
Turkish medical/forensic text in the diff or referenced files trips the filter.

**Why:** repeated across sessions; the block is about the *content domain*, not a code
defect. Do not interpret the refusal as a problem with the code.

**How to apply:** skip architect for these tasks and self-verify rigorously instead.
For DOCX builds, validate the output with `python3` + `zipfile`: parse
`word/document.xml` (XML validity), reconcile image `r:embed` ids ↔ relationships ↔
`word/media/*` files (counts must match, no missing/dangling), check section/heading
ordering by text position, and assert expected substring counts (e.g. citation
conversions applied, no leftover tokens). This catches the same class of bugs the
architect would.
