"use strict";
// REV1 mechanical fixes (safe, content-preserving) + reflow helpers.
// Zero-hallucination: only spelling/terminology/format fixes the reviewer asked for.
// No sentence rewriting, no number/reference changes (thousands-separator commas
// are removed per reviewer: Turkish uses comma only as decimal separator).

// Phrase-level fixes (applied first; order matters). Each entry: [regexp, replacement]
const PHRASE_FIXES = [
  // -- terminology with Turkish + parenthetical explanation (reviewer p.2) --
  [/alternatif splicing ve transkripsiyonel elongasyonu/g,
    "alternatif uç birleştirme (splicing) ve transkripsiyonel uzamayı (elongasyon)"],
  [/hücresel diferansiyasyon/g, "hücresel farklılaşma süreci"],
  // -- "mediye" -> proper Turkish (reviewer p.4) --
  [/mediye edildiğini/g, "aracılığı ile gerçekleştiğini"],
  [/mediye etmiştir/g, "aracılık etmiştir"],
  // -- "modere" -> "düzenleme" forms (reviewer p.5; keep moderasyon/moderatör intact) --
  [/modere edebilir/g, "düzenleyebilir"],
  [/modere ettiği/g, "düzenlediği"],
  [/modere etmiş/g, "düzenlemiş"],
  [/modere etme\b/g, "düzenleme"],
  [/modere eder\b/g, "düzenler"],
  [/modere edip etmediğini/g, "düzenleyip düzenlemediğini"],
  [/modere edip etmediği/g, "düzenleyip düzenlemediği"],
  // -- academic Turkish names (reviewer p.6) --
  [/Nucleus Accumbens/g, "Nükleus Akkumbens"],
  [/Nucleus accumbens/g, "Nükleus akkumbens"],
  [/nucleus accumbens/g, "nükleus akkumbens"],
  [/Hippokampus/g, "Hipokampus"],
  [/hippokampus/g, "hipokampus"],
  // -- supplementary veriler (reviewer p.7) --
  [/supplementary veriler/g, "ek veriler (supplementary data)"],
  // -- veritabanı -> veri tabanı (reviewer p.8; büyük harfli biçim de, ör. Ek/tablo hücreleri) --
  [/Veritaban/g, "Veri taban"],
  [/veritaban/g, "veri taban"],
  // -- etyoloji -> etiyoloji (reviewer p.9) --
  [/etyoloji/g, "etiyoloji"],
  // -- invazif -> invaziv (reviewer p.10) --
  [/invazif/g, "invaziv"],
  // -- superior -> üstün (reviewer p.3) --
  [/Superior/g, "Üstün"],
  [/superior/g, "üstün"],
  // -- R2 -> R² (standalone token) --
  [/\bR2\b/g, "R²"],
  // -- acknowledgement: naturalize ornamental "moda-mod" phrasing (reviewer, Teşekkür) --
  [/paylaşma cömertliği sayesinde/g, "paylaşması sayesinde"],
  [/katkısını takdirle karşılıyoruz/g, "katkısını takdir ediyoruz"],
  // -- reviewer item 50: yazar adıyla kurulan cümlede atıf, yazarın hemen ardında değil
  //    cümle sonunda olmalı. Yalnızca metin-içi (prose) iki Horvath cümlesi; tablo
  //    hücreleri ("Rosen et al. (21)") kuraldışıdır, dokunulmaz. İçerik birebir korunur;
  //    sadece "(8)" işareti cümle sonuna taşınır. --
  [/Horvath \(8\) (tarafından tanımlanan[^.]*?koymuştur)\./g, "Horvath $1 (8)."],
  [/Horvath \(8\) (tarafından 2013 yılında yayımlanan[^.]*?kullanmıştır)\./g, "Horvath $1 (8)."],
  // -- reviewer (şekil reorganizasyonu): ek figürler EKLER altında "Ek 1–8" olarak
  //    yeniden numaralandı; metin-içi "(Ek Şekil S1)" atıfları "(Ek 1)" biçimine çevrilir
  //    (S1->Ek1 ... S8->Ek8). Bu fix "Şekil S" fix'inden ÖNCE çalışmalı ki "Ek Ek 1"
  //    oluşmasın. --
  [/Ek Şekil S(\d+)/g, "Ek $1"],
  // -- EPİCLOCK teknik mimari tablosu eski "Ek 4" iken yeni yapıda "Ek 11" oldu; tek
  //    metin-içi atıf ("...Ek 4'de sunulmuştur.") buna göre güncellenir. --
  [/Ek 4'de/g, "Ek 11'de"],
];

// Remove thousands-separator commas: 1,234 -> 1234 ; 10,542 -> 10542 ; 452,626 -> 452626
// GUARD: a comma directly inside a "letter(" group is NOT a thousands separator but a
// statistical degrees-of-freedom notation (e.g. F(4,142), t istatistiği) — leave it
// verbatim (zero-hallucination: F(4,142) must not collapse to F(4142)).
function stripThousands(s) {
  let prev;
  do {
    prev = s;
    s = s.replace(/(?<![A-Za-zχ²]\()(\d{1,3}),(\d{3})(?!\d)/g, "$1$2");
  } while (s !== prev);
  return s;
}

function applyFixes(text) {
  if (text == null) return text;
  let s = text;
  // MS365-unrenderable bullet glyph U+F0B7 (Word Symbol-font "•") leaks into the text as a
  // Times New Roman run -> renders as a tofu/□ box in MS365. It is pure list furniture (not
  // numbers/refs/legend prose), and panel labels (A./B.) + renderLinkList already provide the
  // list structure, so strip it and collapse the surrounding whitespace. Zero-hallucination-safe.
  s = s.replace(/\s*\uf0b7\s*/g, " ");
  for (const [re, rep] of PHRASE_FIXES) s = s.replace(re, rep);
  s = stripThousands(s);
  return s.trim();
}

// Reflow a slice of raw pdftotext lines into clean paragraphs.
// Blank line(s) separate paragraphs; wrapped lines join with a single space.
function reflowParagraphs(lines) {
  const paras = [];
  let cur = [];
  const flush = () => {
    if (cur.length) {
      let t = cur.join(" ").replace(/\s+/g, " ").trim();
      if (t) paras.push(applyFixes(t));
      cur = [];
    }
  };
  for (const raw of lines) {
    const line = raw.replace(/\s+$/g, "");
    if (line.trim() === "") {
      flush();
    } else {
      cur.push(line.trim());
    }
  }
  flush();
  return paras;
}

// Reflow references: each entry starts with /^\d+\.\s/. Continuation lines join.
// Lines matching separator markers are dropped. Returns array of {num, text}.
function reflowReferences(lines) {
  const refs = [];
  let cur = null;
  for (const raw of lines) {
    const line = raw.trim();
    if (line === "") continue;
    if (/^\d+\s*-\s*\d+\s*:/.test(line)) continue; // "1-22: (...)" / "23-75: (...)" separators
    const m = line.match(/^(\d+)\.\s+(.*)$/);
    const expected = cur ? cur.num + 1 : 1;
    // Only a strictly sequential number starts a new reference; "141-\n151." page-range
    // wraps (151.) must be treated as continuation, not a phantom reference.
    if (m && parseInt(m[1], 10) === expected) {
      if (cur) refs.push(cur);
      cur = { num: parseInt(m[1], 10), text: m[2] };
    } else if (cur) {
      cur.text += " " + line;
    }
  }
  if (cur) refs.push(cur);
  for (const r of refs) r.text = applyFixes(r.text.replace(/\s+/g, " ").trim());
  return refs;
}

// Reflow a key:value list (abbreviations, access links) -> array of strings, one per entry.
// An entry starts when a line begins (non-indented enough) and contains ':' ; continuation
// lines (heavily indented / URL wraps) join to previous.
function reflowList(lines, opts = {}) {
  const out = [];
  for (const raw of lines) {
    const line = raw.replace(/\s+$/g, "");
    if (line.trim() === "") continue;
    // continuation: starts with many spaces OR is a bare URL continuation
    const isCont =
      /^\s{6,}/.test(line) && out.length && !/:/.test(line.trim().split(/\s{2,}/)[0]);
    if (isCont) {
      out[out.length - 1] += " " + line.trim();
    } else {
      out.push(line.trim());
    }
  }
  return out.map((s) => applyFixes(s.replace(/\s+/g, " ").trim()));
}

module.exports = { applyFixes, stripThousands, reflowParagraphs, reflowReferences, reflowList };
