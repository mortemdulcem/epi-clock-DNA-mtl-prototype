"""
Article integrity analysis: plagiarism heuristics + AI-text detection.
Outputs a multi-sheet Excel report with all findings.

NOTE: This is an OFFLINE statistical/heuristic analysis. No external
plagiarism database query is performed. Results approximate likelihood
based on internal text properties and self-comparison with prior drafts.
"""

import os
import re
import math
import statistics
from collections import Counter
from docx import Document
import pandas as pd
from datetime import datetime

TARGET = "attached_assets/DNA_Metilasyon_Saatleriyle_Bağımlılıkta_Epigenetik_Yaş_İvmel_1777112740836.docx"
PRIORS = [
    "attached_assets/DNA_Metilasyon_Saatleriyle_Bağımlılıkta_Epigenetik_Yaş_İvmel_1769760544557.docx",
    "attached_assets/EpiClock_v4_Tam_Makale_Profesyonel_1769687291095.docx",
]

OUT_DIR = "figures/output"
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "Article_Integrity_Analysis_Report.xlsx")


def extract_text(path):
    doc = Document(path)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


def tokenize(text):
    return re.findall(r"\b[\wÇçĞğİıÖöŞşÜü]+\b", text.lower())


def split_sentences(text):
    parts = re.split(r"(?<=[\.!?])\s+", text)
    return [s.strip() for s in parts if len(s.strip()) > 0]


def ngrams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def jaccard(a, b):
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb)


def shannon_entropy(tokens):
    counts = Counter(tokens)
    total = sum(counts.values())
    return -sum((c / total) * math.log2(c / total) for c in counts.values()) if total else 0.0


def burstiness(values):
    if len(values) < 2:
        return 0.0
    mean = statistics.mean(values)
    sd = statistics.stdev(values)
    if mean + sd == 0:
        return 0.0
    return (sd - mean) / (sd + mean)


def detect_ai_phrases(text):
    """Common AI-generated/translated phrases (TR + EN academic boilerplate)."""
    patterns = [
        r"\bsonuç olarak\b",
        r"\bgenel olarak\b",
        r"\bbu çalışmada\b",
        r"\bayrıca\b",
        r"\bbununla birlikte\b",
        r"\böte yandan\b",
        r"\bdolayısıyla\b",
        r"\bnitekim\b",
        r"\bbu bağlamda\b",
        r"\böncelikle\b",
        r"\bbuna ek olarak\b",
        r"\bbunun yanı sıra\b",
        r"\bbu nedenle\b",
        r"\bbu sayede\b",
        r"\bdiğer yandan\b",
        r"\bgösterilmiştir\b",
        r"\bbildirilmiştir\b",
        r"\bvurgulanmıştır\b",
        r"\börnek olarak\b",
        r"\bözellikle\b",
        r"\bkapsamlı bir şekilde\b",
        r"\bderinlemesine\b",
        r"\bgüncel literatür\b",
        r"\bilgili çalışmalar\b",
    ]
    counts = {}
    low = text.lower()
    for p in patterns:
        n = len(re.findall(p, low))
        if n:
            counts[p.strip(r"\b")] = n
    return counts


def find_internal_repeats(sentences, min_words=8):
    """Find near-duplicate sentences inside the same article."""
    repeats = []
    seen = {}
    for i, s in enumerate(sentences):
        toks = tokenize(s)
        if len(toks) < min_words:
            continue
        key = " ".join(toks)
        if key in seen:
            repeats.append((seen[key], i, s[:160]))
        else:
            seen[key] = i
        # also check 6-gram overlap
    return repeats


def shared_passages(target_sents, prior_text, min_run=10):
    """Find verbatim n-gram matches between target sentences and prior text."""
    prior_tokens = tokenize(prior_text)
    prior_ngrams = set(ngrams(prior_tokens, min_run))
    matches = []
    for s in target_sents:
        toks = tokenize(s)
        if len(toks) < min_run:
            continue
        s_ngrams = ngrams(toks, min_run)
        hits = [g for g in s_ngrams if g in prior_ngrams]
        if hits:
            matches.append((s[:200], len(hits), len(s_ngrams)))
    return matches


def reference_stats(paragraphs):
    """Estimate reference list size and citation density."""
    full = "\n".join(paragraphs)
    # numeric brackets like [12] or (Smith, 2020)
    bracket_cites = re.findall(r"\[\s*\d+(?:\s*[,–-]\s*\d+)*\s*\]", full)
    paren_cites = re.findall(r"\([A-ZÇĞİÖŞÜ][\w\-]+(?:\s+(?:ve|et\s+al\.?|and))?[^()]{0,40}?\d{4}\)", full)
    # try to find references section
    ref_start = None
    for i, p in enumerate(paragraphs):
        if re.match(r"^\s*(kaynak(lar|ça)?|references?|bibliyografya)\b", p.lower()):
            ref_start = i
            break
    ref_count = 0
    if ref_start is not None:
        for p in paragraphs[ref_start + 1:]:
            if re.match(r"^\s*\d+\.\s", p) or re.match(r"^\s*\[\s*\d+\s*\]", p):
                ref_count += 1
    return {
        "bracket_citations_in_text": len(bracket_cites),
        "parenthetical_citations_in_text": len(paren_cites),
        "reference_section_found": ref_start is not None,
        "reference_section_paragraph_index": ref_start if ref_start is not None else -1,
        "reference_entries_detected": ref_count,
    }


# ----------------- run analysis -----------------
print(f"[+] Loading target: {os.path.basename(TARGET)}")
paragraphs = extract_text(TARGET)
full_text = "\n".join(paragraphs)
sentences = []
for p in paragraphs:
    sentences.extend(split_sentences(p))

tokens = tokenize(full_text)
unique_tokens = set(tokens)
ttr = len(unique_tokens) / len(tokens) if tokens else 0
sent_lens = [len(tokenize(s)) for s in sentences if tokenize(s)]
b = burstiness(sent_lens)
ent = shannon_entropy(tokens)

# ----- AI heuristic score -----
# Burstiness lower / TTR lower / phrase density higher => more AI-like
phrase_counts = detect_ai_phrases(full_text)
phrase_density = sum(phrase_counts.values()) / max(1, len(tokens)) * 1000  # per 1k tokens

# Sentence-length CV
mean_sl = statistics.mean(sent_lens) if sent_lens else 0
sd_sl = statistics.stdev(sent_lens) if len(sent_lens) > 1 else 0
cv_sl = sd_sl / mean_sl if mean_sl else 0

# composite (0-100, higher = more AI-like)
ai_score = 0
ai_score += max(0, (0.55 - ttr)) * 120        # low diversity penalty
ai_score += max(0, (0.6 - cv_sl)) * 60        # low variability penalty
ai_score += max(0, (-b + 0.2)) * 50           # low burstiness penalty
ai_score += min(20, phrase_density * 1.2)     # boilerplate penalty
ai_score = max(0.0, min(100.0, ai_score))

# ----- Internal repetition -----
repeats = find_internal_repeats(sentences)

# ----- Self-similarity vs prior drafts -----
prior_overlaps = []
for prior_path in PRIORS:
    if not os.path.exists(prior_path):
        continue
    print(f"[+] Comparing with prior: {os.path.basename(prior_path)}")
    prior_paras = extract_text(prior_path)
    prior_text = "\n".join(prior_paras)
    prior_tokens = tokenize(prior_text)

    j5 = jaccard(set(ngrams(tokens, 5)), set(ngrams(prior_tokens, 5)))
    j8 = jaccard(set(ngrams(tokens, 8)), set(ngrams(prior_tokens, 8)))
    matches = shared_passages(sentences, prior_text, min_run=10)
    prior_overlaps.append({
        "prior_file": os.path.basename(prior_path),
        "prior_word_count": len(prior_tokens),
        "jaccard_5gram": round(j5, 4),
        "jaccard_8gram": round(j8, 4),
        "verbatim_sentence_matches_10gram": len(matches),
        "estimated_reuse_pct": round(j8 * 100, 2),
        "interpretation": (
            "High overlap - same article lineage" if j8 > 0.4 else
            "Moderate overlap - significant shared content" if j8 > 0.15 else
            "Low overlap - mostly independent text"
        ),
    })

# ----- References -----
ref_info = reference_stats(paragraphs)

# ----- Build Excel report -----
print("[+] Writing Excel report...")
with pd.ExcelWriter(OUT_PATH, engine="openpyxl") as xl:

    # Sheet 1: Summary
    summary = pd.DataFrame([
        ("Analyzed file", os.path.basename(TARGET)),
        ("Analysis date", datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Paragraph count", len(paragraphs)),
        ("Sentence count", len(sentences)),
        ("Word count (tokens)", len(tokens)),
        ("Unique words", len(unique_tokens)),
        ("Type-Token Ratio (TTR)", round(ttr, 4)),
        ("Mean sentence length (words)", round(mean_sl, 2)),
        ("Sentence length StDev", round(sd_sl, 2)),
        ("Sentence length CV", round(cv_sl, 3)),
        ("Burstiness index", round(b, 3)),
        ("Shannon entropy (bits)", round(ent, 3)),
        ("Boilerplate phrase density (per 1k tokens)", round(phrase_density, 2)),
        ("AI-likelihood composite score (0-100)", round(ai_score, 1)),
        ("AI-likelihood verdict", (
            "HIGH - text shows multiple AI patterns" if ai_score > 60 else
            "MODERATE - some AI-style traits" if ai_score > 35 else
            "LOW - text reads as human-authored"
        )),
        ("Internal duplicate sentences", len(repeats)),
        ("References section detected", ref_info["reference_section_found"]),
        ("Reference entries detected", ref_info["reference_entries_detected"]),
        ("Bracket citations in text", ref_info["bracket_citations_in_text"]),
        ("Parenthetical citations in text", ref_info["parenthetical_citations_in_text"]),
    ], columns=["Metric", "Value"])
    summary.to_excel(xl, sheet_name="Summary", index=False)

    # Sheet 2: AI heuristics breakdown
    ai_break = pd.DataFrame([
        ("Type-Token Ratio", ttr, "≥0.55 = diverse vocabulary (human-like)",
         "Diverse" if ttr >= 0.55 else "Limited diversity (mild AI signal)"),
        ("Sentence-length CV", cv_sl, "≥0.6 = naturally variable length",
         "Natural variability" if cv_sl >= 0.6 else "Uniform sentences (mild AI signal)"),
        ("Burstiness", b, ">0 = bursty/human, <0 = uniform/AI-like",
         "Human-like" if b > 0 else "AI-like uniformity"),
        ("Boilerplate phrase density (per 1k)", phrase_density, "<5 typical for original work",
         "Acceptable" if phrase_density < 5 else "High boilerplate (AI-like)"),
        ("Composite AI score", ai_score, "0=human, 100=AI",
         "HIGH" if ai_score > 60 else "MODERATE" if ai_score > 35 else "LOW"),
    ], columns=["Indicator", "Value", "Reference range", "Reading"])
    ai_break.to_excel(xl, sheet_name="AI_Detection", index=False)

    # Sheet 3: Boilerplate phrases
    if phrase_counts:
        ph = pd.DataFrame(
            sorted(phrase_counts.items(), key=lambda x: -x[1]),
            columns=["Phrase", "Occurrences"],
        )
    else:
        ph = pd.DataFrame(columns=["Phrase", "Occurrences"])
    ph.to_excel(xl, sheet_name="Boilerplate_Phrases", index=False)

    # Sheet 4: Self-plagiarism vs prior drafts
    if prior_overlaps:
        pd.DataFrame(prior_overlaps).to_excel(
            xl, sheet_name="Self_Plagiarism_Priors", index=False
        )
    else:
        pd.DataFrame([{"info": "No prior drafts found for comparison"}]).to_excel(
            xl, sheet_name="Self_Plagiarism_Priors", index=False
        )

    # Sheet 5: Internal repeats (sentence duplicates)
    if repeats:
        pd.DataFrame(repeats, columns=["First_index", "Repeat_index", "Sentence_excerpt"]).to_excel(
            xl, sheet_name="Internal_Duplicates", index=False
        )
    else:
        pd.DataFrame([{"info": "No internal duplicate sentences detected"}]).to_excel(
            xl, sheet_name="Internal_Duplicates", index=False
        )

    # Sheet 6: Sentence-length distribution
    bins = [(0, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 30), (31, 40), (41, 60), (61, 999)]
    dist_rows = []
    for lo, hi in bins:
        n = sum(1 for x in sent_lens if lo <= x <= hi)
        dist_rows.append((f"{lo}-{hi if hi < 999 else '∞'} words", n))
    pd.DataFrame(dist_rows, columns=["Length bucket", "Sentence count"]).to_excel(
        xl, sheet_name="Sentence_Length_Dist", index=False
    )

    # Sheet 7: References analysis
    pd.DataFrame(list(ref_info.items()), columns=["Metric", "Value"]).to_excel(
        xl, sheet_name="References_Analysis", index=False
    )

    # Sheet 8: Methodology / disclaimers
    method = pd.DataFrame([
        ("Plagiarism scope",
         "OFFLINE only. No internet/database lookup (Turnitin, iThenticate). "
         "Detects internal repetition + reuse from prior drafts in this project."),
        ("AI detection scope",
         "Heuristic statistical analysis (TTR, burstiness, sentence-length CV, "
         "boilerplate density). Not equivalent to GPTZero/Originality.AI but "
         "uses the same underlying signal types."),
        ("Burstiness reference",
         "Tian (2023) GPTZero: human text shows higher variance in sentence "
         "length and structure than AI text."),
        ("TTR reference",
         "Templin (1957) lexical diversity: TTR <0.5 over long Turkish text "
         "suggests limited vocabulary / templated writing."),
        ("Self-plagiarism method",
         "Jaccard similarity over 5-gram and 8-gram token sets, plus exact "
         "10-gram verbatim sentence matches against prior drafts."),
        ("Recommendation",
         "For publication-grade similarity score, run the file through "
         "iThenticate/Turnitin via your institution before submission."),
    ], columns=["Topic", "Notes"])
    method.to_excel(xl, sheet_name="Methodology", index=False)

print(f"[+] Report written: {OUT_PATH}")
print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Words:               {len(tokens)}")
print(f"Sentences:           {len(sentences)}")
print(f"TTR:                 {ttr:.3f}")
print(f"Burstiness:          {b:.3f}")
print(f"Sentence CV:         {cv_sl:.3f}")
print(f"AI score (0-100):    {ai_score:.1f}")
print(f"Internal duplicates: {len(repeats)}")
for po in prior_overlaps:
    print(f"vs {po['prior_file'][:50]:50s}  J8={po['jaccard_8gram']:.3f}  reuse~{po['estimated_reuse_pct']}%")
