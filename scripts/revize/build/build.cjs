"use strict";
// Master build: assembles the revised DOCX (rev1 content/language fixes + rev2 format).
// Zero-hallucination: content read verbatim from makale.txt; only the reviewer-requested
// mechanical fixes (fixes.cjs) + structural re-org (heading renumber, table renumber,
// KISALTMALAR move, appendix renumber, reference-marker removal) are applied.
// Numeric table grids come from tables.cjs (hand-verified against source). Output:
//   scripts/revize/build/makale_revize.docx   (rev1.docx / rev2.docx templates untouched)

const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");
const L = require("./lib.cjs");
const F = require("./fixes.cjs");
const T = require("./tables.cjs");

const ROOT = path.join(__dirname, "..");
const SRC = fs.readFileSync(path.join(ROOT, "makale.txt"), "utf8").split("\n");

const deFF = (s) => String(s == null ? "" : s).replace(/\f/g, "");
const ln = (n) => deFF(SRC[n - 1]);
const slice = (a, b) => SRC.slice(a - 1, b).map(deFF);
const clean = (arr) => F.applyFixes(arr.join(" ").replace(/\s+/g, " ").trim());

// Verbatim source caption titles by OLD table number (used as panel section titles in the
// consolidated composite tables). A caption may wrap one line (a single left-margin word,
// e.g. old27 "...Epigenetik Yaş" + "İvmelenmesi") -> that continuation is re-attached.
const CAP_TITLE = {};
for (let i = 0; i < SRC.length; i++) {
  const t = deFF(SRC[i]).trim();
  const m = t.match(/^Tablo\s+(\d+)\.\s*(.*)$/);
  if (!m) continue;
  let title = m[2].trim();
  for (let j = i + 1; j < SRC.length; j++) {
    const r2 = deFF(SRC[j]); const t2 = r2.trim();
    if (t2 === "") continue;
    const gaps = (t2.match(/ {2,}/g) || []).length;
    const gridLike = gaps >= 2 || / {4,}/.test(t2);
    const oneWord = !/\s/.test(t2);
    const indent = r2.length - r2.replace(/^ +/, "").length;
    if (!gridLike && oneWord && indent < 6 && !/^Tablo\s+\d+\./.test(t2)) title += " " + t2;
    break;
  }
  CAP_TITLE[parseInt(m[1], 10)] = title;
}

// ---------- shared image packaging (PNG figures from figgen/out) ----------
// rId1 is reserved for styles.xml; image relationships start at rId2 and are
// allocated sequentially as figures are emitted (inline body figures first, then
// EKLER supplementary figures). All regenerated figures are PNG.
const FIG_DIR = path.join(ROOT, "figgen", "out");
let MEDIA_RID = 2;
const MEDIA_RELS = [];
const MEDIA_FILES = [];
function addImageP(png, widthCm) {
  const buf = fs.readFileSync(path.join(FIG_DIR, png));
  const rId = MEDIA_RID++;
  const xml = L.imageP(rId, buf, widthCm, png);
  MEDIA_RELS.push(`<Relationship Id="rId${rId}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image${rId}.png"/>`);
  MEDIA_FILES.push({ name: `word/media/image${rId}.png`, buf });
  return xml;
}

// Main figure (Şekil 1–6) rendered inline at its relevant body section: image +
// bold centered caption + verbatim legend description. Legend title line starts
// "Şekil N:" -> stripped to the title text; remaining lines become the description.
// Split a single dense legend string into readable lines: each panel label (A. B. C. ...)
// and each "- " bullet starts its own paragraph. Only inserts line breaks (no word is
// added/removed/reordered) so content stays verbatim. Panel match is a SINGLE A–F letter
// immediately followed by "." or ")" then a space — specific enough not to fire on
// sentence boundaries ("...edildi. Bonferroni" has a multi-letter word, no match).
function splitLegend(text) {
  // text, kaynaktaki boş satırlardan gelen "\n" paragraf sınırlarını içerebilir; bunları
  // koru, sonra her parça içinde panel etiketleri (A./B.)) ve "- " madde işaretlerini ayır.
  const pieces = [];
  for (const part of text.split("\n")) {
    let s = " " + part;
    s = s.replace(/\s+([A-F])([.)])\s+/g, "\n$1$2 ");
    // Bullet dash: only when followed by a LETTER (real list item, e.g. "- Prefrontal").
    // A " - " followed by a digit is a math minus (e.g. "ln(x) - 3.53") — leave it inline
    // so the equation stays verbatim (zero-hallucination).
    s = s.replace(/\s+[-–—]\s+(?=[A-Za-zÇĞİÖŞÜçğıöşü])/g, "\n- ");
    for (const p of s.split("\n")) { const t = p.trim(); if (t) pieces.push(t); }
  }
  return pieces;
}

function figBlock(num, png, lf, lt) {
  let x = addImageP(png, 17.0);
  const raw = slice(lf, lt).map((s) => s.trim());
  let i = 0;
  while (i < raw.length && raw[i] === "") i++; // baştaki boş satırları atla
  const titleLine = raw[i] || ""; i++;          // başlık = ilk boş olmayan satır
  const sm = titleLine.match(/^Şekil\s*(\d+)/);
  const srcNum = sm ? sm[1] : null; // kaynaktaki orijinal şekil numarası (self-referans remap için)
  const title = titleLine.replace(/^Şekil\s*\d+\s*[:.]\s*/, "").trim();
  // Açıklamayı boş-satır paragraf sınırlarını ("\n") KORUYARAK kur; bir paragraf içinde
  // sarmalanmış satırlar boşlukla birleşir. Böylece panel etiketleri, "- " maddeleri ve
  // sondaki cümleler ayrı paragraflarda kalır (reviewer: legend sıkışıklığı sorunu).
  let descRaw = "", prevBlank = true;
  for (; i < raw.length; i++) {
    if (raw[i] === "") { prevBlank = true; continue; }
    descRaw += (descRaw === "" ? "" : (prevBlank ? "\n" : " ")) + raw[i];
    prevBlank = false;
  }
  // Yalnızca gereksiz "Şekil N:" / "Şekil N." ETİKETİ baştan atılır ([:.] zorunlu) —
  // "Şekil N'te sunulan..." gibi cümle-içi atıf KORUNUR. Sonra kaynaktaki self-referans
  // numarası yeni görüntü numarasına (num) eşlenir.
  descRaw = descRaw.replace(/^Şekil\s*\d+\s*[:.]\s*/, "");
  if (srcNum) descRaw = descRaw.replace(new RegExp("Şekil\\s*" + srcNum + "\\b", "g"), "Şekil " + num);
  x += L.figureCaption("Şekil " + num + ".", F.applyFixes(title));
  if (descRaw.trim()) {
    const segs = splitLegend(descRaw);
    if (segs.length > 1) for (const seg of segs) x += L.p(F.applyFixes(seg), { align: "both", sz: 18, before: 0, after: 40, line: 240 });
    else x += L.p(F.applyFixes(descRaw), { align: "both", sz: 18, before: 0, after: 40, line: 240 });
  }
  return x;
}

// line (HM heading) -> main figure injected right after that heading
const INLINE_FIG = {
  // Şekiller GÖRÜNME SIRASINA göre numaralandırılır (kaynak numarası değil): ilk görünen = Şekil 1.
  347: { num: 1, png: "fig4.png", from: 1693, to: 1704 }, // 3.1 Veri Seti Karakteristikleri -> Çalışma Kohortu Özellikleri (ilk görünen)
  363: { num: 2, png: "fig1.png", from: 1669, to: 1677 }, // 3.2 Epigenetik Saat Performans -> Saat Performans Karşılaştırması
  398: { num: 3, png: "fig2.png", from: 1678, to: 1685 }, // 3.3 Maddeye Özgü EAA -> Maddeye Özgü EAA
  510: { num: 4, png: "fig3.png", from: 1686, to: 1692 }, // 3.6 Mediyasyon Analizleri -> Mediyasyon
  826: { num: 6, png: "fig6.png", from: 1728, to: 1758 }, // 3.13 Tersine Çevrilebilirlik -> Müdahale & EAA Geri Dönüşü (Şekil 5 fig5.png 3.10'da inline)
};

// ---------- table order mapping (old source no -> sequential 1..27 + t-object) ----------
const OLD = [1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31];
const TOBJ = [T.t1, T.t2, T.t3, T.t4, T.t5, T.t6, T.t7, T.t8, T.t9, T.t10, T.t11, T.t12, T.t13, T.t14, T.t15, T.t16, T.t17, T.t18, T.t19, T.t20, T.t21, T.t22, T.t23, T.t24, T.t25, T.t26, T.t27];
const tableByOld = (old) => {
  const i = OLD.indexOf(old);
  return i < 0 ? null : { t: TOBJ[i], num: i + 1 };
};

// ---------- table consolidation layout (reviewer: 27 tables -> 10 composites) ----------
// Display order 1..10. Each entry is either a single table (old source no) or a GROUP of
// related tables merged into one professional composite (unifiedTable). Umbrella titles for
// multi-member groups are authored section labels; the single-member group (disp 5) reuses
// its own verbatim caption (CAP_TITLE[11]). Per-table captions survive as panel titles.
const TABLE_LAYOUT = [
  { disp: 1, single: 1 },
  { disp: 2, single: 6 },
  { disp: 3, group: [7, 8, 9], umbrella: "Madde Türüne Göre Epigenetik Yaş İvmelenmesi ve Fonksiyonel Zenginleştirme Analizleri" },
  { disp: 4, single: 10 },
  { disp: 5, group: [11], umbrella: CAP_TITLE[11] },
  { disp: 6, single: 12 },
  { disp: 7, group: [13, 14], umbrella: "Postmortem Validasyon: PMI Düzeltmesi ve Doku pH Performans Değerlendirmesi" },
  { disp: 8, group: [15, 16, 17, 18, 19, 20, 21], umbrella: "Klinik ve Demografik Kovaryatların Epigenetik Yaş İvmelenmesi Üzerindeki Etkileri" },
  { disp: 9, group: [22, 23, 24, 25, 26], umbrella: "Epigenetik Yaş İvmelenmesinin Tersine Çevrilebilirliği: Müdahale Etkileri ve Literatür Sentezi" },
  { disp: 10, group: [27, 28, 29, 30, 31], umbrella: "Mevcut Literatürle Karşılaştırma, Çalışmanın Özgünlüğü ve Tanısal Doğruluk" },
];
// old source table no -> { disp, single } | { disp, isFirst, olds, umbrella }
const groupInfo = {};
for (const e of TABLE_LAYOUT) {
  if (e.single != null) { groupInfo[e.single] = { disp: e.disp, single: true }; continue; }
  e.group.forEach((old, idx) => {
    groupInfo[old] = { disp: e.disp, single: false, isFirst: idx === 0, olds: e.group, umbrella: e.umbrella };
  });
}

function fixCells(arr) { return arr.map((r) => r.map((c) => F.applyFixes(String(c == null ? "" : c)))); }
function fixTable(tobj) {
  if (tobj.segments) {
    return { segments: tobj.segments.map((s) => ({ subtitle: s.subtitle, headers: s.headers.map(F.applyFixes), rows: fixCells(s.rows) })) };
  }
  return { headers: tobj.headers.map(F.applyFixes), rows: fixCells(tobj.rows) };
}

// --- in-text table reference sentence (reviewer: her tablodan önce ona atıf yapan cümle) ---
const LOC_TE = new Set([3, 4, 5, 13, 14, 15, 23, 24, 25]);
const LOC_DA = new Set([6, 9, 10, 16, 19, 26]);
const locSuffix = (n) => (LOC_TE.has(n) ? "'te" : LOC_DA.has(n) ? "'da" : "'de");
const REF_VERBS = ["sunulmuştur", "verilmiştir", "özetlenmiştir", "gösterilmektedir", "yer almaktadır"];
function tableRefSentence(num, title) {
  const t = String(title == null ? "" : title).replace(/\s+/g, " ").trim().replace(/[.:]+$/, "").trim();
  const verb = REF_VERBS[num % REF_VERBS.length];
  return (t ? t : "İlgili bulgular") + ", Tablo " + num + locSuffix(num) + " " + verb + ".";
}

let TABLE_COUNT = 0;
function renderTable(num, titleText, tobj) {
  TABLE_COUNT++;
  const cleanTitle = F.applyFixes(titleText);
  let x = L.p(tableRefSentence(num, cleanTitle), { align: "both", keepNext: true });
  x += L.tableCaption("Tablo " + num + ".", cleanTitle);
  const ft = fixTable(tobj);
  if (ft.segments) {
    // Reviewer: consolidate stacked tables. If every segment shares the SAME header row,
    // render ONE table with full-width band rows (the subtitles) instead of N separate
    // tables. Segments with differing columns stay as labelled sub-tables.
    const h0 = JSON.stringify(ft.segments[0].headers);
    const sameHeaders = ft.segments.every((s) => JSON.stringify(s.headers) === h0);
    if (sameHeaders) {
      x += L.table({ headers: ft.segments[0].headers, sections: ft.segments.map((s) => ({ title: s.subtitle, rows: s.rows })) });
    } else {
      for (const seg of ft.segments) {
        if (seg.subtitle) x += L.para(L.run(seg.subtitle, { sz: 18, bold: true }), { align: "left", before: 80, after: 20, keepNext: true });
        x += L.table({ headers: seg.headers, rows: seg.rows });
      }
    }
  } else {
    x += L.table({ headers: ft.headers, rows: ft.rows });
  }
  return x;
}

// Render ONE grouped member as a clean, self-contained bordered sub-table (reviewer: 27 -> 10
// consolidated under 10 numbers, but each part stays a tidy table). Because each member is its
// OWN table (its own grid), columns size to ITS content — no cross-table raggedness and no
// forced equal-width wrapping. A shaded title bar (the per-table verbatim caption CAP_TITLE[old])
// labels the part. A segmented source table whose segments all share a column count becomes one
// internally-aligned multi-panel table; otherwise each segment is its own sub-table. The member's
// footnote is NOT emitted here — it flows verbatim right below via the caller's emitTail, so each
// note sits under its own part and nothing is rewritten or lost.
function renderMemberSection(old) {
  const info = tableByOld(old);
  if (!info) return "";
  const ft = fixTable(info.t);
  if (ft.segments) {
    const counts = ft.segments.map((s) => s.headers.length);
    const panels = ft.segments.map((s) => ({ title: F.applyFixes(s.subtitle || ""), headers: s.headers, rows: s.rows }));
    if (counts.every((c) => c === counts[0])) return L.unifiedTable(panels); // uniform -> one aligned table
    let x = ""; for (const p of panels) x += L.unifiedTable([p]); return x;   // mixed -> stacked sub-tables
  }
  return L.unifiedTable([{ title: F.applyFixes(CAP_TITLE[old] || ""), headers: ft.headers, rows: ft.rows }]);
}

// ---------- heading map (line -> directive) ----------
const HM = {
  48: { level: 1 }, 49: { level: 2 }, 73: { level: 2 }, 102: { level: 2 }, 126: { level: 2 }, 148: { level: 2 }, 158: { level: 2 },
  176: { level: 1 }, 177: { level: 2 }, 213: { level: 2 }, 251: { level: 2 }, 293: { level: 2 },
  346: { level: 1, label: "3. BULGULAR VE YORUMLAR" },
  347: { level: 2 }, 363: { level: 2 }, 398: { level: 2 }, 404: { level: 2 }, 490: { level: 2 }, 510: { level: 2 },
  // --- reviewer items 35/49: eski Tartışma yorumları (4.x) ilgili bulgu/tablo bölümlerinin
  //     hemen ardına taşındı (birebir, yeni cümle yok). Numaralar yeni akışa göre. ---
  1082: { level: 2, num: "3.7" },   // eski 4.3 Mekanistik İçgörüler -> 3.6 Mediyasyon'dan sonra
  595: { level: 2, num: "3.8" },    // Moderasyon Analizleri
  1114: { level: 2, num: "3.9" },   // eski 4.4 Psikolojik Dayanıklılık -> Moderasyon'dan sonra
  631: { level: 2, num: "3.10" },   // Postmortem Validasyon
  1136: { level: 2, num: "3.11" },  // eski 4.5 Adli Uygulamalar -> Postmortem'den sonra
  691: { level: 2, num: "3.12" },   // Klinik ve Demografik Kovaryatlar
  826: { level: 2, num: "3.13" },   // Tersine Çevrilebilirlik
  1157: { level: 2, num: "3.14" },  // eski 4.6 Klinik Uygulamalar -> Tersine Çevrilebilirlik'ten sonra
  930: { level: 2, num: "3.15" },   // eski 4.1 Ana Bulguların Özeti ve Yorumu (sentez)
  952: { level: 2, num: "3.16" },   // eski 4.2 Mevcut Literatürle Karşılaştırma (Tablo 23-27)
  929: { skip: true },
  1173: { level: 2, num: "4.1", prepend: "4. TARTIŞMA" },
  1184: { level: 2, num: "4.2" },
  1210: { level: 1, label: "5. SONUÇ" },
};

const titleOf = (raw) => { const m = raw.trim().match(/^[\d.]+\.\s*(.*)$/); return m ? m[1] : raw.trim(); };

function renderStream(from, to) {
  let out = "", buf = [], tailBuf = [];
  const flush = () => { if (buf.length) { for (const p of F.reflowParagraphs(buf)) out += L.p(p, { align: "both" }); buf = []; } };
  // Post-table TAIL handling. tailBuf collects lines AFTER a grid row; it is CLEARED on
  // every new grid row, so wrapped cells that are interspersed between grid rows
  // (e.g. "Eğimi Kesişimi", "(Ağırlıklı)") never survive — only text after the LAST grid
  // row of a block reaches emitTail. There, a line with no letters or an ALLCAPS single
  // token is grid residue ("(3.2-5.1)", "<0.001", "TOPLAMI") -> dropped before reflow;
  // after reflow, a paragraph starting lowercase is a dangling half-sentence (its head is
  // a mis-extracted cell) -> dropped; a <5-word paragraph with no .!? and no ':' is a stray
  // cell fragment ("Eğimi Kesişimi (Ağırlıklı)") -> dropped. Real footnotes/legends survive.
  const isJunkLine = (s) => !/[A-Za-zÇĞİÖŞÜçğıöşü]/.test(s) || /^[A-ZÇĞİÖŞÜ]+$/.test(s);
  const emitTail = () => {
    const kept = tailBuf.filter((s) => !isJunkLine(s));
    tailBuf = [];
    if (!kept.length) return;
    for (const para of F.reflowParagraphs(kept)) {
      if (/^[a-zçğıöşü]/.test(para)) continue;
      const words = para.split(/\s+/).filter(Boolean).length;
      if (words < 5 && !/[.!?]/.test(para) && !para.includes(":")) continue;
      out += L.p(para, { align: "both", sz: 18, before: 0, after: 60, line: 240 });
    }
  };
  // A table block runs from a "Tablo N." caption to the next structural boundary
  // (next caption / heading / Şekil). Internal blank lines do NOT end it, because
  // pdftotext sprinkles blanks inside grids. Grid rows (gaps>=2) are skipped (real
  // tables come from tables.cjs); low-gap lines before the first grid row are caption
  // continuation, low-gap lines after it are footnotes/body prose (kept). OUTSIDE any
  // table block, every line is kept verbatim — so justified prose with stretch-spacing
  // (e.g. intro lines) is never mistaken for a grid row.
  let inGrid = false, seenGrid = false, pendingCap = null;
  const renderCap = () => {
    if (!pendingCap) return;
    const cap = pendingCap; pendingCap = null;
    const info = groupInfo[cap.num];
    if (!info) return;                       // table not in any layout -> drop (shouldn't happen)
    if (info.single) {
      const tb = tableByOld(cap.num);
      if (tb) out += renderTable(info.disp, cap.text.trim(), tb.t);
      return;
    }
    // Grouped member: one umbrella caption ("Tablo N.") is emitted ONCE at the first member,
    // then EACH member renders as its own clean sub-table at its own caption — so the caller's
    // emitTail drops that member's footnote right below it (reviewer: notes under each part).
    if (info.isFirst) {
      TABLE_COUNT++;
      const title = F.applyFixes(info.umbrella || "");
      out += L.p(tableRefSentence(info.disp, title), { align: "both", keepNext: true });
      out += L.tableCaption("Tablo " + info.disp + ".", title);
    }
    out += renderMemberSection(cap.num);
  };
  for (let i = from; i <= to; i++) {
    const raw = deFF(SRC[i - 1]);
    const hm = HM[i];
    if (hm) {
      renderCap(); emitTail(); flush(); inGrid = false; seenGrid = false;
      if (hm.skip) continue;
      if (hm.prepend) out += L.h1(hm.prepend);
      let lbl;
      if (hm.label) lbl = hm.label;
      else if (hm.num) lbl = hm.num + ". " + titleOf(raw);
      else lbl = raw.trim();
      out += hm.level === 1 ? L.h1(F.applyFixes(lbl)) : L.h2(F.applyFixes(lbl));
      const fig = INLINE_FIG[i];
      if (fig) out += figBlock(fig.num, fig.png, fig.from, fig.to); // reviewer: ana şekil ilgili bölüm başlığının hemen ardına
      continue;
    }
    const t = raw.trim();
    if (t === "") { flush(); continue; } // blank flushes a paragraph but never ends a table block (grids contain internal blanks)
    const mC = t.match(/^Tablo\s+(\d+)\.\s*(.*)$/);
    if (mC) {
      renderCap(); emitTail(); flush();
      pendingCap = { num: parseInt(mC[1], 10), text: mC[2] };
      inGrid = true; seenGrid = false;
      continue;
    }
    if (/^Şekil\s/.test(t)) {
      renderCap(); emitTail(); flush(); inGrid = false; seenGrid = false;
      if (i === 673) {
        // Body "Şekil 1. Beyin Bölgelerinde..." kaynakta ŞEKİLLER'deki Şekil 5 (bölgesel EAA)
        // ile aynı figürün görselsiz mükerreridir. Reviewer: ana şekil ilgili bölüme taşınacak —
        // bu konumda (3.10 Postmortem Validasyon) gerçek Şekil 5 figürünü inline basıyoruz.
        out += figBlock(5, "fig5.png", 1705, 1727);
        continue;
      }
      out += L.para(L.run(F.applyFixes(t), { sz: 18, bold: true }), { align: "center", before: 80, after: 80 });
      continue;
    }
    if (t.startsWith("*")) { renderCap(); emitTail(); flush(); out += L.para(L.run(F.applyFixes(t.replace(/\s+/g, " ")), { sz: 18 }), { align: "left", after: 40 }); continue; }
    const gaps = (t.match(/ {2,}/g) || []).length;
    // gaps>=2: two column separators. / {4,}/: a single wide gap = a 2-column block
    // (GO/KEGG explanatory grids that pdftotext renders as one big-gap pair per line).
    const gridLike = gaps >= 2 || / {4,}/.test(t) || /^\d+\.\s+[A-ZÇĞİÖŞÜ]{2,}/.test(t);
    if (inGrid) {
      if (gridLike) { renderCap(); seenGrid = true; tailBuf = []; continue; } // grid row -> drop + reset tail (interspersed wrapped cells die here)
      if (!seenGrid && pendingCap) {
        // A genuine wrapped-caption overflow is a single word still at the left margin
        // (e.g. "...Epigenetik Yaş" + "İvmelenmesi"). A multi-word line or an indented
        // line is a mis-extracted table header/cell (e.g. "Bağışıklık yanıtı", indented
        // "Önceki") whose real text already lives in tables.cjs -> drop it, don't pollute
        // the caption (and, via the ref sentence, the body).
        const oneWord = !/\s/.test(t);
        const indent = raw.length - raw.replace(/^ +/, "").length;
        if (oneWord && indent < 6) { pendingCap.text += " " + t; continue; } // wrapped caption continuation
        continue; // pre-grid table fragment -> drop
      }
      tailBuf.push(t); // candidate footnote/prose AFTER a grid row -> survives only if no later grid row clears it
      continue;
    }
    buf.push(t); // outside any table block -> always keep verbatim
  }
  renderCap();
  emitTail();
  flush();
  return out;
}

function renderAbstract(from, to) {
  let ab = F.applyFixes(slice(from, to).join(" ").replace(/\s+/g, " ").trim());
  ab = ab.replace(/(Background:|Objective:|Methods:|Results:|Conclusions:)/g, "\u0001$1");
  let out = "";
  for (const seg of ab.split("\u0001")) {
    if (!seg.trim()) continue;
    const m = seg.match(/^(Background:|Objective:|Methods:|Results:|Conclusions:)\s*([\s\S]*)$/);
    if (m) out += L.para(L.run(m[1] + " ", { sz: 22, bold: true }) + L.run(m[2].trim(), { sz: 22 }), { align: "both" });
    else out += L.p(seg.trim(), { align: "both" });
  }
  return out;
}

function renderEk4() {
  const headers = ["Özellik", "Modül", "Hesaplama Yöntemi", "Yazılım Teknolojisi", "Veri Kaynağı", "Çıktı"];
  // The source is fixed-width but NOT uniformly aligned: section bands shift the
  // columns a few chars and some first-column values wrap. So we tokenize each row
  // on runs of >=2 spaces (multi-word cells stay intact) and bucket every token into
  // a column by its start position (column starts derived from blank-column gaps).
  const dataLines = [];
  for (let i = 1481; i <= 1665; i++) {
    const raw = deFF(SRC[i - 1]).replace(/\s+$/, "");
    if (raw.trim() !== "") dataLines.push(raw);
  }
  if (!dataLines.length) return L.p("(Ek 4 teknik tablo ayrıştırılamadı.)", { sz: 20 });
  const maxLen = Math.max(...dataLines.map((l) => l.length));

  // A column gap is a run (>= 2 wide) of positions blank in >= 80% of the rows.
  const blankFrac = [];
  for (let p = 0; p < maxLen; p++) {
    let b = 0; for (const l of dataLines) if ((l[p] || " ") === " ") b++;
    blankFrac[p] = b / dataLines.length;
  }
  const colStarts = [0];
  let gs = -1;
  for (let p = 0; p <= maxLen; p++) {
    const hi = p < maxLen && blankFrac[p] >= 0.80;
    if (hi && gs < 0) gs = p;
    else if (!hi && gs >= 0) { if (p - gs >= 2 && p < maxLen) colStarts.push(p); gs = -1; }
  }
  if (colStarts.length !== 6) return L.p(`(Ek 4 teknik tablo ayrıştırılamadı: ${colStarts.length} sütun.)`, { sz: 20 });
  const bucket = (pos) => { let c = 0; for (let k = 0; k < colStarts.length; k++) if (pos >= colStarts[k]) c = k; return c; };

  // Split a line into {start,text} tokens separated by runs of >= 2 spaces.
  const tokenize = (raw) => {
    const out = []; const re = /\s{2,}/g; let last = 0, m; const parts = [];
    while ((m = re.exec(raw))) { parts.push([last, m.index]); last = re.lastIndex; }
    parts.push([last, raw.length]);
    for (const [a, b] of parts) {
      const seg = raw.slice(a, b); const t = seg.trim();
      if (t) out.push({ start: a + (seg.length - seg.trimStart().length), text: t });
    }
    return out;
  };
  const isBandText = (t) => !/[a-zçğıöşü]/.test(t) && /[A-ZÇĞİÖŞÜ]/.test(t) && /^[A-ZÇĞİÖŞÜ0-9&/.\- ]+$/.test(t);

  // Join band-title words with spaces, except a wrapped single-letter suffix
  // (STANDARTLAR + I -> STANDARTLARI) which attaches to the previous word.
  const joinBand = (ws) => ws.reduce((s, w) => (s && w.length === 1 ? s + w : s ? s + " " + w : w), "");
  const groups = [];
  let bandWords = [], rows = [], cur = null;
  const pushGroup = () => { if (rows.length || bandWords.length) groups.push({ title: joinBand(bandWords), rows }); bandWords = []; rows = []; cur = null; };
  for (let i = 1481; i <= 1665; i++) {
    const raw = deFF(SRC[i - 1]).replace(/\s+$/, "");
    if (raw.trim() === "") continue;
    const toks = tokenize(raw);
    const lead = /^\s/.test(raw);
    // band title: a single all-caps token near the left margin
    if (toks.length === 1 && toks[0].start < 21 && isBandText(toks[0].text)) {
      if (rows.length) pushGroup();
      bandWords.push(toks[0].text); cur = null; continue;
    }
    // A full data row is exactly 6 single-token cells, so assign tokens positionally
    // (token i -> column i). This is robust to the source's per-section alignment shifts
    // (some bands place a column a few chars left/right of others). Partial lines
    // (empty cells or wrapped continuations) fall back to position-based bucketing.
    let c;
    if (!lead && toks.length === 6 && toks[0].start < 21) {
      c = toks.map((t) => t.text);
    } else {
      c = ["", "", "", "", "", ""];
      for (const t of toks) { const k = bucket(t.start); c[k] += (c[k] ? " " : "") + t.text; }
    }
    const nonEmpty = c.filter((x) => x).length;
    // Continuation of the previous row: every genuine row fills all 6 columns, so a
    // line that is indented or fills <= 3 columns is a wrapped continuation. The Modül
    // column (k=1) holds snake_case identifiers that wrap mid-token (deep_learning_methyla
    // + tion) and must be re-joined WITHOUT a space; all other columns wrap at word breaks.
    if (cur && (lead || nonEmpty <= 3)) {
      for (let k = 0; k < 6; k++) {
        if (!c[k]) continue;
        if (!cur[k]) { cur[k] = c[k]; continue; }
        // Modül (k=1) holds snake_case identifiers that wrap mid-token -> join without space.
        if (k === 1) { cur[k] += c[k]; continue; }
        // A 1-2 char lowercase fragment is a mid-word completion (PubChe+m, Anonimleştirilmi+ş)
        // -> attach with no space; genuine word-wrap continuations are full words -> add a space.
        const fw = c[k].split(/\s+/)[0];
        if (fw.length <= 2 && /^[a-zçğıöşü]/.test(fw) && /[A-Za-z0-9çğıöşüÇĞİÖŞÜ\/]$/.test(cur[k])) {
          cur[k] += c[k];
        } else {
          cur[k] += " " + c[k];
        }
      }
      continue;
    }
    // normal data row
    cur = c; rows.push(cur);
  }
  pushGroup();

  // Reviewer: consolidate the ~14 per-band tables into ONE table whose band titles become
  // full-width section rows (shared 6-column header printed once).
  const sections = groups
    .filter((g) => g.rows.length || g.title)
    .map((g) => ({ title: g.title ? F.applyFixes(g.title) : "", rows: fixCells(g.rows) }));
  if (!sections.length) return "";
  return L.table({ headers, sections });
}

// Robust link-list renderer for Ek 9 / Ek 10. Each source line is one entry, EXCEPT a
// bare-URL line (the wrapped tail "(https://...)" of the previous entry) which is joined
// back. Section labels (a line ending ":" with no URL, e.g. "GEO Veri Setleri:") render
// bold; every link gets its OWN left-aligned paragraph (justified would stretch long
// unbreakable URLs into the "bozuk" look the reviewer flagged). Verbatim: no link dropped
// or merged across entries (fixes the GEO/ArrayExpress cramming and the missing Hannum row).
function renderLinkList(from, to) {
  let out = "";
  const ent = [];
  for (let i = from; i <= to; i++) {
    const t = deFF(SRC[i - 1]).replace(/\s+/g, " ").trim();
    if (!t) continue;
    if (/^\(?https?:\/\//.test(t) && ent.length) { ent[ent.length - 1].text += " " + t; continue; }
    ent.push({ text: t, label: /:$/.test(t) && !/https?:/.test(t) });
  }
  for (const e of ent) {
    const fixed = F.applyFixes(e.text);
    if (e.label) out += L.para(L.run(fixed, { sz: 20, bold: true }), { align: "left", before: 80, after: 20, keepNext: true });
    else out += L.para(L.run(fixed, { sz: 20 }), { align: "left", after: 20, indentLeft: 360 });
  }
  return out;
}

// =================== ASSEMBLE ===================
(async () => {
  let body = "";
  const report = {};

  // --- Front matter ---
  body += L.titleP(clean(slice(1, 3)));
  body += L.subtitleP(clean(slice(5, 6)), { italic: true, bold: false, sz: 22, after: 80 });
  body += L.p(ln(7).trim(), { align: "center", after: 20, bold: true });
  body += L.p(ln(8).trim(), { align: "center", after: 20, sz: 20 });
  body += L.p(ln(9).trim(), { align: "center", after: 160, sz: 20 });

  // --- Abstract + keywords ---
  body += L.h1("ABSTRACT");
  body += renderAbstract(15, 41);
  body += L.para(L.run("Keywords: ", { sz: 20, bold: true }) + L.run(clean(slice(42, 43)).replace(/^Keywords:\s*/, ""), { sz: 20 }), { align: "both", after: 120 });

  // --- KISALTMALAR (moved from Ek 1) ---
  body += L.h1("KISALTMALAR");
  const abbr = F.reflowList(slice(1405, 1444));
  for (const e of abbr) body += L.p(e, { align: "both", sz: 20, after: 20 });
  report.abbr = abbr.length;

  // --- Intro / Method / Results+Yorumlar (her analiz tablosunun hemen ardına ilgili
  //     mevcut literatür-destekli yorum gelecek şekilde yeniden sıralandı; birebir
  //     taşıma, yeni cümle yok — reviewer items 35/49) / Tartışma / Sonuç ---
  body += renderStream(48, 594);     // GİRİŞ, YÖNTEM, "3. BULGULAR VE YORUMLAR", 3.1-3.6 (Mediyasyon'a kadar)
  body += renderStream(1082, 1111);  // 3.7  (eski 4.3) Mekanistik İçgörüler — Mediyasyon yorumu
  body += renderStream(595, 630);    // 3.8  Moderasyon Analizleri
  body += renderStream(1114, 1133);  // 3.9  (eski 4.4) Psikolojik Dayanıklılık — Moderasyon yorumu
  body += renderStream(631, 690);    // 3.10 Postmortem Validasyon
  body += renderStream(1136, 1156);  // 3.11 (eski 4.5) Adli Uygulamalar — sınıflandırma + postmortem yorumu
  body += renderStream(691, 825);    // 3.12 Klinik ve Demografik Kovaryatlar
  body += renderStream(826, 928);    // 3.13 Tersine Çevrilebilirlik
  body += renderStream(1157, 1172);  // 3.14 (eski 4.6) Klinik Uygulamalar — yorum
  body += renderStream(930, 951);    // 3.15 (eski 4.1) Ana Bulguların Özeti ve Yorumu — sentez
  body += renderStream(952, 1080);   // 3.16 (eski 4.2) Mevcut Literatürle Karşılaştırma (Tablo 23-27)
  body += renderStream(1173, 1220);  // 4. TARTIŞMA (Güçlü Yönler, Limitasyonlar) + 5. SONUÇ

  // --- Teşekkür + beyanlar (naturalized via fixes) ---
  body += L.h1("TEŞEKKÜR");
  body += L.p(clean(slice(1224, 1226)), { align: "both" });
  for (const no of [1227, 1228, 1229, 1230]) {
    const txt = F.applyFixes(ln(no).trim());
    const m = txt.match(/^([^:]+:)\s*([\s\S]*)$/);
    if (m) body += L.para(L.run(m[1] + " ", { sz: 22, bold: true }) + L.run(m[2], { sz: 22 }), { align: "both", after: 40 });
    else body += L.p(txt, { align: "both", after: 40 });
  }
  // Yazar Katkıları: source placeholder (1398-1401, fake X.Y./Z.A.) dropped; replaced with a
  // standard single-author (Dr. Nurcan Denli Bayır = N.D.B.) CRediT statement per user instruction.
  body += L.para(L.run("Yazar Katkıları: ", { sz: 22, bold: true }) + L.run("Çalışmanın tüm aşamaları — kavramsallaştırma, yöntem tasarımı, veri toplama ve analizi, özgün taslağın yazımı ile eleştirel gözden geçirme ve düzenleme — tek yazar (N.D.B.) tarafından yürütülmüştür. Yazar, makalenin yayımlanacak son hâlini okumuş ve onaylamıştır.", { sz: 22 }), { align: "both", after: 40 });

  // --- Kaynakça ---
  body += L.h1("KAYNAKÇA");
  const refs = F.reflowReferences(slice(1232, 1394));
  let rn = 1;
  for (const r of refs) { body += L.para(L.run(rn + ". ", { sz: 17 }) + L.run(r.text, { sz: 17 }), { align: "both", indentLeft: 360, hanging: 360, after: 40 }); rn++; }
  report.refs = refs.length;

  // --- Ekler ---
  // Reviewer (şekil reorganizasyonu): kaynaktaki "Ek Şekil S1–S8" ek figürleri EKLER altında
  // "Ek 1–8" olarak yeniden numaralandırıldı (S1->Ek1 ... S8->Ek8, birebir). Her birine kaynak
  // figür açıklaması (legend) metin-içi yorum olarak eklendi; legend'in kendi "Şekil SN" etiketi
  // "Ek N"e çevrildi. Metin-tabanlı eski ekler (eski Ek2/3/4) sona kaydı: Ek 9 (saat katsayıları),
  // Ek 10 (veri linkleri), Ek 11 (EPİCLOCK teknik mimari). Metin-içi "(Ek Şekil SN)" atıfları
  // fixes.cjs ile "(Ek N)"e, EPİCLOCK atfı "Ek 4'de"->"Ek 11'de" olarak güncellendi.
  body += L.h1("EKLER");
  const SUPP = [
    { num: 1, png: "s1.png", label: "DNA Metilasyon Verisi İşleme ve Analiz İş Akışı", from: null, to: null },
    { num: 2, png: "s2.png", label: "Batch Etkisi Düzeltmesi (ComBat)", from: 1759, to: 1775 },
    { num: 3, png: "s3.png", label: "Epigenetik Saat Kalibrasyonu", from: 1776, to: 1793 },
    { num: 4, png: "s4.png", label: "Diferansiyel Metilasyon Volkan Grafikleri", from: 1794, to: 1816 },
    { num: 5, png: "s5.png", label: "Aracılık Yol Diyagramları", from: 1817, to: 1838 },
    { num: 6, png: "s6.png", label: "Moderasyon Etkileşim Etkileri", from: 1839, to: 1852 },
    { num: 7, png: "s7.png", label: "Postmortem Aralık (PMI) Düzeltme Etkisi", from: 1853, to: 1866 },
    { num: 8, png: "s8.png", label: "Beyin Bölgesine Özgü Epigenetik Yaş Hızlanması", from: 1867, to: 1885 },
  ];
  for (const s of SUPP) {
    body += L.h2("Ek " + s.num + ". " + s.label);
    body += addImageP(s.png, 17.0);
    if (s.from) {
      let dtext = F.applyFixes(slice(s.from, s.to).map((x) => x.trim()).join(" ").replace(/\s+/g, " ").trim());
      dtext = dtext.replace(new RegExp("Şekil\\s*S" + s.num + "\\b", "g"), "Ek " + s.num); // legend self-label S_n -> Ek n
      if (dtext) body += L.p(dtext, { align: "both", sz: 18, before: 0, after: 40, line: 240 });
    }
  }
  body += L.h2("Ek 9. Epigenetik Saat Katsayıları Erişim Bilgileri");
  body += renderLinkList(1447, 1452);
  body += L.h2("Ek 10. Veri Erişim Linkleri");
  body += renderLinkList(1454, 1470);
  body += L.h2("Ek 11. EPİCLOCK v4.0 — Kapsamlı Teknik Mimari Tablosu");
  body += renderEk4();

  report.mainFigures = 6;            // Şekil 1–6 inline (ilgili bölümlerde)
  report.supplementary = SUPP.length; // Ek 1–8 (eski S1–S8)
  report.tables = TABLE_COUNT;

  // --- package ---
  const docRels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' +
    MEDIA_RELS.join("") + "</Relationships>";

  const docXml = L.documentXml(body);
  const zip = new JSZip();
  zip.file("[Content_Types].xml", L.CONTENT_TYPES);
  zip.file("_rels/.rels", L.RELS);
  zip.file("word/document.xml", docXml);
  zip.file("word/styles.xml", L.stylesXml());
  zip.file("word/_rels/document.xml.rels", docRels);
  for (const m of MEDIA_FILES) zip.file(m.name, m.buf);
  const out = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  const outPath = path.join(__dirname, "makale_revize.docx");
  fs.writeFileSync(outPath, out);

  // verification dump
  fs.writeFileSync(path.join(__dirname, "_document.xml"), docXml);
  console.log("WROTE", outPath, "(" + out.length + " bytes)");
  console.log("REPORT", JSON.stringify(report));
  console.log("docXml length", docXml.length, "tables", TABLE_COUNT);
})().catch((e) => { console.error("BUILD FAILED:", e); process.exit(1); });
