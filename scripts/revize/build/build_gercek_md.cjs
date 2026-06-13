"use strict";
// ============================================================================
// MAKALE_GERCEK.md -> DOCX  (gerçek, çok-maddeli, yeniden üretilebilir makale)
// ----------------------------------------------------------------------------
// Tek doğruluk kaynağı realdata/MAKALE_GERCEK.md'dir; bu betik onu BİREBİR
// DOCX'e çevirir (içerik elle yazılmaz -> drift olmaz). Biçim kuralları
// (dergi şablonu) lib.cjs üzerinden uygulanır:
//   başlık 14pt(sz28) · bölüm başlıkları 12pt(sz24) · gövde 11pt(sz22) ·
//   tablo/şekil 9pt(sz18) · KAYNAKLAR 8.5pt(sz17) · A4 dar kenar · 1.15 satır.
// Zero-Hallucination: hiçbir sayı eklenmez/değiştirilmez; yalnız markdown ->
// docx dönüşümü yapılır. Çıktı: build/MAKALE_GERCEK.docx
//
// Çalıştırma:  cd scripts/revize && node build/build_gercek_md.cjs
// ============================================================================

const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");
const L = require("./lib.cjs");

const MD_PATH = path.join(__dirname, "..", "realdata", "MAKALE_GERCEK.md");
const MD = fs.readFileSync(MD_PATH, "utf8");

const esc = (s) =>
  String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// ----------------------------------------------------------- inline & helpers
function monoRun(text, sz) {
  return (
    `<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>` +
    `<w:sz w:val="${sz}"/><w:szCs w:val="${sz}"/></w:rPr>` +
    `<w:t xml:space="preserve">${esc(text)}</w:t></w:r>`
  );
}

// markdown inline (**bold**, `code`) -> runs xml
function inlineRuns(text, sz) {
  let out = "";
  const re = /(\*\*([^*]+)\*\*|`([^`]+)`)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out += L.run(text.slice(last, m.index), { sz });
    if (m[2] != null) out += L.run(m[2], { sz, bold: true });
    else if (m[3] != null) out += monoRun(m[3], sz);
    last = re.lastIndex;
  }
  if (last < text.length) out += L.run(text.slice(last), { sz });
  return out || L.run("", { sz });
}

// strip inline markdown markers (for table cells, which are plain runs)
const stripInline = (s) => String(s).replace(/\*\*/g, "").replace(/`/g, "").trim();

// ------------------------------------------------------------------- builders
let body = "";
let inRefs = false;

function emitHeading(level, text) {
  if (level === 1) { // markdown "## " = makale bölüm başlığı (12pt)
    inRefs = /^kaynak/i.test(text.trim());
    body += L.para(L.run(text, { sz: 24, bold: true }),
      { align: "left", before: 220, after: 80, line: 276, keepNext: true });
  } else { // markdown "### " = alt başlık (11pt kalın)
    body += L.para(L.run(text, { sz: 22, bold: true }),
      { align: "left", before: 140, after: 60, line: 276, keepNext: true });
  }
}

function emitParagraph(text) {
  if (inRefs) {
    // KAYNAKLAR girişleri 8.5pt, asılı girinti
    body += L.para(inlineRuns(text, 17),
      { align: "both", before: 0, after: 60, line: 240, indentLeft: 360, hanging: 360 });
  } else {
    body += L.para(inlineRuns(text, 22), { align: "both", after: 120, line: 276 });
  }
}

function emitBullet(text) {
  body += L.para(inlineRuns("•  " + text, inRefs ? 17 : 22),
    { align: "both", after: 60, line: inRefs ? 240 : 276, indentLeft: 360, hanging: 200 });
}

function emitQuote(text) {
  body += L.para(L.run(text, { sz: 20, italic: true }),
    { align: "both", before: 40, after: 120, line: 264, indentLeft: 360 });
}

function emitMono(linesArr) {
  for (const ln of linesArr) {
    body += L.para(monoRun(ln.length ? ln : " ", 16),
      { align: "left", before: 0, after: 0, line: 240 });
  }
  body += L.para(L.run("", { sz: 10 }), { after: 60, line: 240 }); // küçük boşluk
}

function emitTable(tblLines) {
  const parse = (ln) => ln.replace(/^\|/, "").replace(/\|\s*$/, "").split("|").map((c) => c.trim());
  const headers = parse(tblLines[0]).map(stripInline);
  const rows = tblLines.slice(2).map((ln) => parse(ln).map(stripInline));
  body += L.table({ headers, rows });
}

// --------------------------------------------------------------- parse loop
const lines = MD.split(/\r?\n/);
let titleDone = false;
for (let i = 0; i < lines.length; ) {
  const line = lines[i];
  if (line.trim() === "") { i++; continue; }
  if (line.trim() === "---") { i++; continue; }

  if (/^#\s+/.test(line)) {
    const t = line.replace(/^#\s+/, "").trim();
    if (!titleDone) {
      body += L.para(L.run(t, { sz: 28, bold: true }), { align: "center", before: 0, after: 160, line: 276 });
      titleDone = true;
    } else {
      emitHeading(1, t);
    }
    i++; continue;
  }
  if (/^###\s+/.test(line)) { emitHeading(2, line.replace(/^###\s+/, "").trim()); i++; continue; }
  if (/^##\s+/.test(line)) { emitHeading(1, line.replace(/^##\s+/, "").trim()); i++; continue; }

  if (/^```/.test(line)) {
    i++;
    const buf = [];
    while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
    i++; // closing fence
    emitMono(buf);
    continue;
  }

  if (/^\|/.test(line)) {
    const buf = [];
    while (i < lines.length && /^\|/.test(lines[i])) { buf.push(lines[i]); i++; }
    if (buf.length >= 2) emitTable(buf);
    continue;
  }

  if (/^>\s?/.test(line)) {
    const buf = [];
    while (i < lines.length && /^>\s?/.test(lines[i])) { buf.push(lines[i].replace(/^>\s?/, "")); i++; }
    emitQuote(buf.join(" ").trim());
    continue;
  }

  if (/^[-*]\s+/.test(line)) {
    emitBullet(line.replace(/^[-*]\s+/, "").trim());
    i++; continue;
  }

  // normal paragraph: birleştir (markdown sert-sarma)
  const buf = [line];
  i++;
  while (
    i < lines.length &&
    lines[i].trim() !== "" &&
    lines[i].trim() !== "---" &&
    !/^#{1,3}\s+/.test(lines[i]) &&
    !/^```/.test(lines[i]) &&
    !/^\|/.test(lines[i]) &&
    !/^>\s?/.test(lines[i]) &&
    !/^[-*]\s+/.test(lines[i])
  ) { buf.push(lines[i]); i++; }
  emitParagraph(buf.join(" ").trim());
}

// ------------------------------------------------------------------- package
const docRels =
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' +
  "</Relationships>";

(async () => {
  const docXml = L.documentXml(body);
  const zip = new JSZip();
  zip.file("[Content_Types].xml", L.CONTENT_TYPES);
  zip.file("_rels/.rels", L.RELS);
  zip.file("word/document.xml", docXml);
  zip.file("word/styles.xml", L.stylesXml());
  zip.file("word/_rels/document.xml.rels", docRels);
  const out = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  const outPath = path.join(__dirname, "MAKALE_GERCEK.docx");
  fs.writeFileSync(outPath, out);
  fs.writeFileSync(path.join(__dirname, "_document_gercek_md.xml"), docXml);
  const nTbl = (docXml.match(/<w:tbl>/g) || []).length;
  console.log("WROTE", outPath, "(" + out.length + " bytes)");
  console.log("tables:", nTbl, "| docXml:", docXml.length, "chars");
})().catch((e) => { console.error("BUILD FAILED:", e); process.exit(1); });
