"use strict";
// OOXML / DOCX low-level renderer (raw XML + JSZip). Times New Roman everywhere.
// Sizes are in half-points (sz). Spec: title 28, section heading 24, body 22,
// table/figure 18, references 17.

const fs = require("fs");
const path = require("path");

const FONT = "Times New Roman";
const EMU_PER_CM = 360000;

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// rPr builder
function rPr({ sz = 22, bold = false, italic = false, caps = false } = {}) {
  let x = `<w:rPr><w:rFonts w:ascii="${FONT}" w:hAnsi="${FONT}" w:cs="${FONT}"/>`;
  if (bold) x += "<w:b/>";
  if (italic) x += "<w:i/>";
  if (caps) x += "<w:caps/>";
  x += `<w:sz w:val="${sz}"/><w:szCs w:val="${sz}"/></w:rPr>`;
  return x;
}

// a run; text may contain segments. supports super/subscript via opts.script
function run(text, opts = {}) {
  if (text === "" || text == null) return "";
  return `<w:r>${rPr(opts)}<w:t xml:space="preserve">${esc(text)}</w:t></w:r>`;
}

// paragraph. runsXml is a string of <w:r> runs. opts: align, sz (for mark/pPr rPr),
// bold, spacingBefore/After (twips), line (default 276 = 1.15), indent (twips), hanging
function para(runsXml, opts = {}) {
  const {
    align = "both",
    line = 276,
    before = 0,
    after = 120,
    indentLeft = 0,
    hanging = 0,
    keepNext = false,
  } = opts;
  let pPr = "<w:pPr>";
  if (keepNext) pPr += "<w:keepNext/>";
  pPr += `<w:spacing w:before="${before}" w:after="${after}" w:line="${line}" w:lineRule="auto"/>`;
  if (indentLeft || hanging)
    pPr += `<w:ind w:left="${indentLeft}"${hanging ? ` w:hanging="${hanging}"` : ""}/>`;
  if (align) pPr += `<w:jc w:val="${align}"/>`;
  pPr += "</w:pPr>";
  return `<w:p>${pPr}${runsXml}</w:p>`;
}

// Convenience text-paragraph (single style across the whole paragraph)
function p(text, opts = {}) {
  return para(run(text, opts), opts);
}

// Heading helpers
function titleP(text) {
  return para(run(text, { sz: 28, bold: true }), { align: "center", after: 120 });
}
function subtitleP(text, o = {}) {
  return para(run(text, { sz: o.sz || 24, bold: o.bold !== false, italic: o.italic }), {
    align: o.align || "center",
    after: o.after != null ? o.after : 120,
  });
}
function h1(text) {
  // main section: 12pt, ALL CAPS, left, bold
  return para(run(text, { sz: 24, bold: true, caps: true }), {
    align: "left",
    before: 240,
    after: 120,
    keepNext: true,
  });
}
function h2(text) {
  // subsection: 12pt, first-letter caps, left, bold
  return para(run(text, { sz: 24, bold: true }), {
    align: "left",
    before: 160,
    after: 80,
    keepNext: true,
  });
}

// Table caption (9pt centered, bold label)
function tableCaption(label, title) {
  const runs = run(label + " ", { sz: 18, bold: true }) + run(title, { sz: 18, bold: true });
  return para(runs, { align: "center", before: 120, after: 40, keepNext: true });
}
function figureCaption(label, title) {
  const runs = run(label + " ", { sz: 18, bold: true }) + run(title || "", { sz: 18, bold: true });
  return para(runs, { align: "center", before: 80, after: 40 });
}

// Table. data = { headers:[...], rows:[[...]], widths:[...](optional pct ints summing ~5000) }
// cells sz=18, centered. Header row bold.
function table(data) {
  const { headers, sections } = data;
  const rows = data.rows || [];
  const ncol = headers ? headers.length : (rows[0] ? rows[0].length : (sections && sections[0] && sections[0].rows[0] ? sections[0].rows[0].length : 1));
  const widths = data.widths || null;

  const grid =
    "<w:tblGrid>" +
    Array.from({ length: ncol }, (_, i) => {
      const w = widths ? widths[i] : Math.round(5000 / ncol);
      return `<w:gridCol w:w="${Math.round((w / 5000) * 9000)}"/>`;
    }).join("") +
    "</w:tblGrid>";

  function cell(text, { bold = false, w } = {}) {
    const tcW = w
      ? `<w:tcW w:w="${w}" w:type="pct"/>`
      : `<w:tcW w:w="${Math.round(5000 / ncol)}" w:type="pct"/>`;
    const body = String(text == null ? "" : text);
    const runs = run(body, { sz: 18, bold });
    const cellP = para(runs || run("", { sz: 18 }), {
      align: "center",
      after: 0,
      line: 240,
    });
    return `<w:tc><w:tcPr>${tcW}<w:vAlign w:val="center"/></w:tcPr>${cellP}</w:tc>`;
  }

  function rowXml(cells, bold) {
    return (
      "<w:tr>" +
      cells
        .map((c, i) => cell(c, { bold, w: widths ? widths[i] : undefined }))
        .join("") +
      "</w:tr>"
    );
  }

  const borders =
    "<w:tblBorders>" +
    ["top", "left", "bottom", "right", "insideH", "insideV"]
      .map(
        (b) =>
          `<w:${b} w:val="single" w:sz="4" w:space="0" w:color="000000"/>`
      )
      .join("") +
    "</w:tblBorders>";

  // Full-width section-divider row (single cell spanning all columns), bold, shaded.
  function bandRow(title) {
    const cellP = para(run(String(title == null ? "" : title), { sz: 18, bold: true }), {
      align: "left", after: 0, line: 240,
    });
    return (
      "<w:tr>" +
      `<w:tc><w:tcPr><w:tcW w:w="5000" w:type="pct"/><w:gridSpan w:val="${ncol}"/>` +
      '<w:shd w:val="clear" w:color="auto" w:fill="DDEBF7"/><w:vAlign w:val="center"/></w:tcPr>' +
      cellP + "</w:tc></w:tr>"
    );
  }

  let xml =
    "<w:tbl><w:tblPr>" +
    '<w:tblW w:w="5000" w:type="pct"/>' +
    '<w:jc w:val="center"/>' +
    borders +
    '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>' +
    "</w:tblPr>" +
    grid;
  if (headers) xml += rowXml(headers, true);
  if (sections) {
    for (const s of sections) {
      if (s.title) xml += bandRow(s.title);
      for (const r of s.rows) xml += rowXml(r, false);
    }
  } else {
    for (const r of rows) xml += rowXml(r, false);
  }
  xml += "</w:tbl>";
  // Minimal required separator paragraph after the table. Word needs a paragraph after a
  // table, but we keep it tiny (3-4pt) so an attached table footnote/note sits snug against
  // the grid ("tabloya bitişik") instead of after a full blank line.
  return xml + `<w:p><w:pPr><w:spacing w:before="0" w:after="20" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="8"/><w:szCs w:val="8"/></w:rPr></w:pPr></w:p>`;
}

// Unified multi-panel table: renders ONE bordered <w:tbl> made of several "panels", each
// being a constituent table that keeps its OWN header row. panels = [{title, headers, rows}].
// The grid is sized to the widest panel; narrower panels distribute their cells across the
// grid via gridSpan (proportional), so each panel reads as an internally-even section. A
// full-width shaded title row labels each panel. Used to consolidate related tables into one
// professional composite (reviewer request) without forcing differing columns to misalign.
function unifiedTable(panels) {
  const ncol = Math.max(...panels.map((p) => p.headers.length));
  // Content-proportional column widths: each column's weight = its longest UNBREAKABLE token
  // (word) across the header + all data rows of every panel — wherever the long word sits
  // (a column header like "Metamfetamin" OR a row label). That column then gets enough width
  // to keep the word on one line, while numeric columns stay narrow. Long multi-word cells
  // still wrap across lines (intended). Data rows always have exactly ncol cells here, so
  // cell j maps to column j. Fixed layout makes these widths exact across Word/LibreOffice.
  const longestTok = (s) => String(s == null ? "" : s).trim().split(/\s+/).reduce((m, w) => Math.max(m, w.length), 0);
  const W = Array(ncol).fill(3);
  for (const p of panels) for (const r of [p.headers, ...p.rows]) {
    if (!Array.isArray(r) || r.length !== ncol) continue;
    for (let j = 0; j < ncol; j++) W[j] = Math.max(W[j], Math.min(longestTok(r[j]) + 1, 24));
  }
  const sumW = W.reduce((a, b) => a + b, 0);
  // Dense tables drop font so long single words fit without squeezing: 7pt at >=8 cols,
  // 8pt at 7 cols, 9pt otherwise.
  const CSZ = ncol >= 8 ? 14 : ncol === 7 ? 16 : 18;
  const grid =
    "<w:tblGrid>" +
    W.map((w) => `<w:gridCol w:w="${Math.round((9000 * w) / sumW)}"/>`).join("") +
    "</w:tblGrid>";

  // distribute ncol grid columns across k cells as evenly as possible (only the full-width
  // panel-title row spans >1 now; data rows always have exactly ncol cells -> span 1 -> the
  // grid lines stay perfectly aligned within a table, no raggedness).
  const colSpans = (k) => {
    const base = Math.floor(ncol / k), rem = ncol - base * k;
    return Array.from({ length: k }, (_, i) => base + (i < rem ? 1 : 0));
  };

  function uCell(text, { bold = false, start = 0, span = 1, align = "center", shade = null, sz = CSZ } = {}) {
    const wsum = W.slice(start, start + span).reduce((a, b) => a + b, 0);
    let tcPr = `<w:tcW w:w="${Math.round((5000 * wsum) / sumW)}" w:type="pct"/>`;
    if (span > 1) tcPr += `<w:gridSpan w:val="${span}"/>`;
    if (shade) tcPr += `<w:shd w:val="clear" w:color="auto" w:fill="${shade}"/>`;
    tcPr += '<w:vAlign w:val="center"/>';
    const runs = run(String(text == null ? "" : text), { sz, bold });
    const cellP = para(runs || run("", { sz }), { align, after: 0, line: 240 });
    return `<w:tc><w:tcPr>${tcPr}</w:tcPr>${cellP}</w:tc>`;
  }
  function uRow(cells, bold) {
    const sp = colSpans(cells.length);
    let start = 0, xml = "<w:tr>";
    for (let i = 0; i < cells.length; i++) { xml += uCell(cells[i], { bold, start, span: sp[i] }); start += sp[i]; }
    return xml + "</w:tr>";
  }
  function panelTitleRow(title) {
    return "<w:tr>" + uCell(title, { bold: true, start: 0, span: ncol, align: "left", shade: "D9E2F3", sz: 18 }) + "</w:tr>";
  }

  const borders =
    "<w:tblBorders>" +
    ["top", "left", "bottom", "right", "insideH", "insideV"]
      .map((b) => `<w:${b} w:val="single" w:sz="4" w:space="0" w:color="000000"/>`)
      .join("") +
    "</w:tblBorders>";

  let xml =
    "<w:tbl><w:tblPr>" +
    '<w:tblW w:w="5000" w:type="pct"/><w:jc w:val="center"/>' +
    borders +
    '<w:tblLayout w:type="fixed"/>' +
    // Tight cell padding: reclaims ~0.13cm of usable width per side in every column so a long
    // single word (e.g. the header "Metamfetamin") fits on one line in dense composites.
    '<w:tblCellMar><w:top w:w="20" w:type="dxa"/><w:left w:w="36" w:type="dxa"/><w:bottom w:w="20" w:type="dxa"/><w:right w:w="36" w:type="dxa"/></w:tblCellMar>' +
    '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>' +
    "</w:tblPr>" +
    grid;
  for (const p of panels) {
    if (p.title) xml += panelTitleRow(p.title);
    xml += uRow(p.headers, true);
    for (const r of p.rows) {
      let cells = r.slice(0, p.headers.length);
      while (cells.length < p.headers.length) cells.push("");
      xml += uRow(cells, false);
    }
  }
  xml += "</w:tbl>";
  return xml + `<w:p><w:pPr><w:spacing w:before="0" w:after="20" w:line="240" w:lineRule="auto"/><w:rPr><w:sz w:val="8"/><w:szCs w:val="8"/></w:rPr></w:pPr></w:p>`;
}

// --- Image (inline) ---
function getJpegSize(buf) {
  // returns {w,h}
  let i = 2;
  const len = buf.length;
  while (i < len) {
    if (buf[i] !== 0xff) {
      i++;
      continue;
    }
    const marker = buf[i + 1];
    if (
      (marker >= 0xc0 && marker <= 0xc3) ||
      (marker >= 0xc5 && marker <= 0xc7) ||
      (marker >= 0xc9 && marker <= 0xcb) ||
      (marker >= 0xcd && marker <= 0xcf)
    ) {
      const h = buf.readUInt16BE(i + 5);
      const w = buf.readUInt16BE(i + 7);
      return { w, h };
    }
    const segLen = buf.readUInt16BE(i + 2);
    i += 2 + segLen;
  }
  return { w: 1000, h: 750 };
}

// PNG IHDR: width/height are uint32 BE at byte offsets 16 and 20
function getPngSize(buf) {
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}
// dispatch on magic bytes (PNG signature 89 50 4E 47) else fall back to JPEG SOF parse
function getImageSize(buf) {
  if (buf.length > 24 && buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47)
    return getPngSize(buf);
  return getJpegSize(buf);
}

// image paragraph; rId is relationship id, dims in EMU, maxWcm content width
function imageP(rId, buf, maxWcm = 16.0, name = "image") {
  const { w, h } = getImageSize(buf);
  let cx = Math.round(maxWcm * EMU_PER_CM);
  let cy = Math.round((cx * h) / w);
  const maxHcm = 25.0; // cap height
  const maxCy = Math.round(maxHcm * EMU_PER_CM);
  if (cy > maxCy) {
    cy = maxCy;
    cx = Math.round((cy * w) / h);
  }
  const drawing =
    `<w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">` +
    `<wp:extent cx="${cx}" cy="${cy}"/>` +
    `<wp:effectExtent l="0" t="0" r="0" b="0"/>` +
    `<wp:docPr id="${rId}" name="${esc(name)}"/>` +
    `<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>` +
    `<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">` +
    `<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">` +
    `<pic:nvPicPr><pic:cNvPr id="${rId}" name="${esc(name)}"/><pic:cNvPicPr/></pic:nvPicPr>` +
    `<pic:blipFill><a:blip r:embed="rId${rId}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>` +
    `<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${cx}" cy="${cy}"/></a:xfrm>` +
    `<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>` +
    `</a:graphicData></a:graphic></wp:inline></w:drawing>`;
  return `<w:p><w:pPr><w:spacing w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:r>${drawing}</w:r></w:p>`;
}

// --- Document assembly ---
const NS =
  'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" ' +
  'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" ' +
  'xmlns:o="urn:schemas-microsoft-com:office:office" ' +
  'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ' +
  'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" ' +
  'xmlns:v="urn:schemas-microsoft-com:vml" ' +
  'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" ' +
  'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" ' +
  'xmlns:w10="urn:schemas-microsoft-com:office:word" ' +
  'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" ' +
  'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" ' +
  'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" ' +
  'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" ' +
  'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" ' +
  'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" ' +
  'mc:Ignorable="w14 wp14"';

function sectPr() {
  // A4 portrait, narrow margins 1.27cm = 720 twips
  return (
    "<w:sectPr>" +
    '<w:pgSz w:w="11906" w:h="16838"/>' +
    '<w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" w:header="708" w:footer="708" w:gutter="0"/>' +
    '<w:cols w:space="708"/>' +
    "<w:docGrid w:linePitch=\"360\"/>" +
    "</w:sectPr>"
  );
}

function documentXml(bodyXml) {
  return (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
    `<w:document ${NS}><w:body>${bodyXml}${sectPr()}</w:body></w:document>`
  );
}

function stylesXml() {
  return (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
    "<w:docDefaults><w:rPrDefault><w:rPr>" +
    `<w:rFonts w:ascii="${FONT}" w:hAnsi="${FONT}" w:cs="${FONT}"/>` +
    '<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="tr-TR"/>' +
    "</w:rPr></w:rPrDefault>" +
    '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>' +
    "</w:docDefaults>" +
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>' +
    "</w:styles>"
  );
}

const CONTENT_TYPES =
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
  '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
  '<Default Extension="xml" ContentType="application/xml"/>' +
  '<Default Extension="jpg" ContentType="image/jpeg"/>' +
  '<Default Extension="jpeg" ContentType="image/jpeg"/>' +
  '<Default Extension="png" ContentType="image/png"/>' +
  '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>' +
  '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>' +
  "</Types>";

const RELS =
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>' +
  "</Relationships>";

module.exports = {
  esc, run, para, p, titleP, subtitleP, h1, h2,
  tableCaption, figureCaption, table, unifiedTable, imageP, getJpegSize, getImageSize,
  documentXml, stylesXml, CONTENT_TYPES, RELS, FONT, EMU_PER_CM,
};
