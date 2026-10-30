// Build slide 045 — "Iteration 4" (perceptron iteration, ROOT build, no dependencies)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_045.jpg (960x540, 1px=1pt=1/72in)
// Spec: analysis/slide_045_final.json
//
// MEASURED GEOMETRY (frame px, from qa/slide045/measurements_045.txt + PIL scans):
//   Canvas: white FFFFFF
//   Panel: gray E9E9E7 rect x54..903 y45..540 (house_chrome.js: no top stroke, C00000 L/R/bottom)
//   Badge: numeral "45" at (876,73) d~35, fill FDFD96, ring 6A5ACD 2pt, numeral 333333 bold Arial 18pt
// MEASURED: Top example panel has a WHITE interior (x200 y90 = 240,242,220); blue 1pt outline.
//   Calc panel: white x274..853 y139..528, thin grey D9D9D9 1pt rules at
//     - left data table: header x1..x6 at y64..73 (cy 68.5), 3 data rows y77..107, class row y113..125 (cy 119)
//       cols centered: 96, 118, 140.5, 163, 186, 209 (6 cols, pitch ~22.6)
//     - "Initial W = [4; -2; -2]": text x266..327 y77..84, bracket column vector x330..353 y58..105
//       rows at cy 66.5 / 83 / 97.5
//     - "Step eta = 2": RED x365..435 y66..80 (cy 73)
//     - "Check classes of" label: x499..583 y79..88 (cy 83.5)
//     - Z table: header Z1 Z1 Z1 y64..76 (cy 70), rows y80..110 (cy 84.5 / 99)
//       cols centered: 605, 627.5, 650
//   Legend line: x240..509 y109..124 (cy 116.5) — "C1 positive, C2 negative, Zero is unaccepted"
//     C1 in red x239..253, C2 in blue x310..319, rest black
//   Augmented vectors table: white box x70..246 y140..255, 1pt black border
//     title "Ugmented Vectors (from Top)" BLUE y147..159 x81..236
//     row1 y166..175 (cy 170.5), rows2-4 y179..226, class row y231..243 (cy 237)
//     cols centered: 99.5, 122, 144.5, 167, 189.5, 212.5
//   Iteration badge: red fill x84..214 y277..305, white bold text (cy 291)
//   Stop box: white x64..246 y330..415, 1pt red border; "No change in W" y350..366, "Stop Iterations" italic red y374..392
//   Calculation panel: white x274..853 y139..528; gray rule pairs at
//     y139/140 | y197 | y206/207 | y263 | y272 | y329 | y337/338 | y395 | y404 | y461/462 | y470 | y528
//     rows: (143..196) (209..262) (275..328) (341..394) (407..460) (473..527)
//     ONE text line per row (cy ≈ row_top+28.5) beside two 3-row bracket column vectors
//     centred on that line (pitch ~15.5px): d(xᵢ) vector at x379..405, W vector at x739..757.
//
// FRAME-VS-SPEC DEVIATIONS (frame wins):
//   1. analysis says top table header at "y 7-10%" and rows at y11-31% -> measured header y64..73 class row y113..125.
//   2. analysis says class row "C₁ C₁ C₁ C₂ C₂ C₂" — measured RED~74 (C1 red, C2 black) in top-left table;
//      augmented table class row measured RED~97 + BLUE~22 (C1 red, C2 blue) per typography notes.
//   3. Pointer from "Check classes of" matrix to "Zero is unaccepted": a black/gray right-arrow at y115..127 x638..655.
//   4. "W" underlined in "Initial W" and "No change in W" (measured underline runs at y85 x304..337 in top panel).
//   5. Spec percentages for calc panel (x35-99%, y41-97%) match measured box x274..853 y139..528.
//
// Laws honored: hex without '#'; explicit fontFace; margin 0; measured geometry; eq PNGs at exact px/600 size.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");
const fs = require("fs");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_045_recreated.pptx";
const ASSET_DIR = __dirname + "/assets";

const px = (v) => v / 72;   // frame px -> inches
const A = "Arial";
const BLUE = "0000FF";
const RED = "FF0000";
const RED2 = "D8262C";      // dark red used in some accents
const BLACK = "000000";
const WHITE = "FFFFFF";
// calc panel's light-grey rules: measured lum 165-193 (bluish from JPEG chroma
// subsampling on a thin line); analysis brief specifies #D9D9D9.
const RULE = "D9D9D9";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- HOUSE CHROME: white canvas, gray panel, C00000 L/R/bottom strokes (NO top), badge "45" ----
drawHouseChrome(pptx, slide, { numeral: 45 });

// ============================================================
// 1. TOP EXAMPLE PANEL (blue outline box, no fill)
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(719 - 68 + 1), h: px(129 - 54 + 1),
  line: { color: BLUE, width: 1 },
  // no fill: omit entirely so <a:noFill/> is emitted
});

// ---- 1a. LEFT DATA TABLE (x1..x6 header + 3 rows + class row) ----
// Column centres (measured): 96, 118, 140.5, 163, 186, 209
const TOP_COLS = [96, 118, 140.5, 163, 186, 209];
const TOP_HDR_Y = 64, TOP_HDR_BOT = 73;   // header band
const TOP_ROWS_Y = [78, 89, 100];         // data row bands (y77..107 merged: 3 rows of ~10px + gaps)
const TOP_CLASS_Y = 113, TOP_CLASS_BOT = 125;

function tableCell(cx, y0, y1, text, opts) {
  slide.addText(text, Object.assign({
    x: px(cx - 16), y: px(y0), w: px(32), h: px(y1 - y0 + 1),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 12,
  }, opts || {}));
}

// Header row x1..x6 (blue)
const topHdr = ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"];
TOP_COLS.forEach((cx, i) => tableCell(cx, TOP_HDR_Y, TOP_HDR_BOT, topHdr[i],
  { color: BLUE, fontSize: 12 }));

// Data rows — parenthesised single digits
const topData = [
  ["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"],
  ["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"],
  ["(1)", "(1)", "(1)", "(4)", "(5)", "(6)"],
];
topData.forEach((row, r) => {
  const y0 = TOP_ROWS_Y[r], y1 = y0 + 9;
  TOP_COLS.forEach((cx, c) => tableCell(cx, y0, y1, row[c], { color: BLACK }));
});

// Class row C1 C1 C1 C2 C2 C2 (measured: C1 red, C2 black in this table)
const topClass = [
  { t: "C\u2081", o: { color: RED2, bold: true } },
  { t: "C\u2082", o: { color: BLACK, bold: true } },
  { t: "C\u2081", o: { color: RED2, bold: true } },
  { t: "C\u2082", o: { color: BLACK, bold: true } },
  { t: "C\u2082", o: { color: BLACK, bold: true } },
  { t: "C\u2082", o: { color: BLACK, bold: true } },
];
// measured class row: cols (90,102) C1-red | (113,124) C2-black | (134,146) C1-red | (157,169) C2 | (180,192) C2 | (203,214) C2
TOP_COLS.forEach((cx, i) =>
  tableCell(cx, TOP_CLASS_Y, TOP_CLASS_BOT, topClass[i].t, topClass[i].o));

// ---- 1b. "Initial W = [4; -2; -2]" ----
// Text part: "Initial W =" x266..327 y77..84, W underlined
slide.addText([
  { text: "Initial ", options: { fontFace: A, fontSize: 13, color: BLACK } },
  { text: "W", options: { fontFace: A, fontSize: 13, color: BLACK, underline: true } },
  { text: " = ", options: { fontFace: A, fontSize: 13, color: BLACK } },
], {
  x: px(266), y: px(75), w: px(64), h: px(12),
  align: "left", valign: "middle", margin: 0, lineSpacing: 13,
});

// Bracket column vector [4; -2; -2]: verticals x330-331 & x351-352 spanning y59..105
// 3 stacked rows at cy 66.5 / 83 / 97.5 (pitch ~15.5)
slide.addText("[", {
  x: px(330), y: px(59), w: px(6), h: px(105 - 59 + 1),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 42, color: BLACK,
});
slide.addText("]", {
  x: px(347), y: px(59), w: px(7), h: px(105 - 59 + 1),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 42, color: BLACK,
});
// rows: 4 / -2 / -2
[["4", 63, 70], ["-2", 79, 87], ["-2", 94, 101]].forEach(([t, y0, y1]) => {
  slide.addText(t, {
    x: px(334), y: px(y0), w: px(20), h: px(y1 - y0 + 1),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: BLACK,
  });
});

// ---- 1c. "Step eta = 2" in red ----
slide.addText([
  { text: "Step ", options: { fontFace: A, fontSize: 13, color: RED2 } },
  { text: "\u03b7", options: { fontFace: A, fontSize: 13, color: RED2 } },
  { text: " = 2", options: { fontFace: A, fontSize: 13, color: RED2 } },
], {
  x: px(365), y: px(66), w: px(72), h: px(14),
  align: "left", valign: "middle", margin: 0, lineSpacing: 14,
});

// ---- 1d. "Check classes of" label ----
slide.addText("Check classes of", {
  x: px(499), y: px(79), w: px(85), h: px(10),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, color: BLACK,
});

// ---- 1e. Z table (2 rows x 3 cols) ----
const Z_COLS = [605, 627.5, 650];
const Z_HDR_Y = 64, Z_HDR_BOT = 76;
const Z_ROWS_Y = [[83, 90], [96, 104]];
["Z\u2081", "Z\u2081", "Z\u2081"].forEach((t, i) =>
  slide.addText(t, {
    x: px(Z_COLS[i] - 10), y: px(Z_HDR_Y), w: px(20), h: px(Z_HDR_BOT - Z_HDR_Y + 1),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 12, color: BLUE,
  }));
const Z_DATA = [
  ["(0)", "(7)", "(3)"],
  ["(0)", "(6)", "(2)"],
];
Z_DATA.forEach((row, r) => {
  const [y0, y1] = Z_ROWS_Y[r];
  Z_COLS.forEach((cx, c) => slide.addText(row[c], {
    x: px(cx - 10), y: px(y0), w: px(20), h: px(y1 - y0 + 1),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 12, color: BLACK,
  }));
});

// ---- 1f. pointer arrow from Z matrix toward "Zero is unaccepted" ----
// measured: black arrow x638..655 y115..127 (a small right/down arrow)
slide.addShape(pptx.ShapeType.line, {
  x: px(640), y: px(115), w: px(16), h: px(12),
  line: { color: BLACK, width: 1 },
});
slide.addShape(pptx.ShapeType.triangle, {
  x: px(652), y: px(117), w: px(6), h: px(8),
  rotate: 90, fill: { color: BLACK },
});

// ============================================================
// 2. LEGEND LINE
// ============================================================
slide.addText([
  { text: "C\u2081", options: { fontFace: A, fontSize: 12, color: RED2, bold: true } },
  { text: " positive, ", options: { fontFace: A, fontSize: 12, color: BLACK } },
  { text: "C\u2082", options: { fontFace: A, fontSize: 12, color: BLUE, bold: true } },
  { text: " negative, ", options: { fontFace: A, fontSize: 12, color: BLACK } },
  { text: "Zero is unaccepted", options: { fontFace: A, fontSize: 12, color: BLACK } },
], {
  x: px(240), y: px(109), w: px(270), h: px(16),
  align: "left", valign: "middle", margin: 0, lineSpacing: 14,
});

// ============================================================
// 3. AUGMENTED VECTORS TABLE
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(140), w: px(246 - 70 + 1), h: px(255 - 140 + 1),
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
// title (blue, "Ugmented Vectors (from Top)" — sic: the A is missing in the frame)
slide.addText("Ugmented Vectors (from Top)", {
  x: px(81), y: px(147), w: px(156), h: px(13),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 11, color: BLUE, italic: true,
});
const AUG_COLS = [99.5, 122, 144.5, 167, 189.5, 212.5];
// row 1: (1)(1)(1)(1)(1)(1)  y166..175
["(1)", "(1)", "(1)", "(1)", "(1)", "(1)"].forEach((t, i) =>
  slide.addText(t, {
    x: px(AUG_COLS[i] - 11), y: px(166), w: px(22), h: px(10),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: BLACK,
  }));
// rows 2-4 (band y179..226, 3 rows): (1)(2)(1)(5)(6)(6) / (1)(1)(2)(4)(5)(6) / (1)(1)(1)(4)(5)(6)
const AUG_ROWS_Y = [[180, 190], [196, 206], [212, 224]];
const AUG_DATA = [
  ["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"],
  ["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"],
  ["(1)", "(1)", "(1)", "(4)", "(5)", "(6)"],
];
AUG_DATA.forEach((row, r) => {
  const [y0, y1] = AUG_ROWS_Y[r];
  AUG_COLS.forEach((cx, c) => slide.addText(row[c], {
    x: px(cx - 11), y: px(y0), w: px(22), h: px(y1 - y0 + 1),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: BLACK,
  }));
});
// class row C1 C1 C1 C2 C2 C2 (C1 red, C2 blue)
const AUG_CLASS = [
  { t: "C\u2081", o: { color: RED2, bold: true } },
  { t: "C\u2082", o: { color: BLUE, bold: true } },
  { t: "C\u2081", o: { color: RED2, bold: true } },
  { t: "C\u2082", o: { color: BLUE, bold: true } },
  { t: "C\u2082", o: { color: BLUE, bold: true } },
  { t: "C\u2082", o: { color: BLUE, bold: true } },
];
AUG_COLS.forEach((cx, i) =>
  slide.addText(AUG_CLASS[i].t, {
    x: px(cx - 11), y: px(231), w: px(22), h: px(13),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, ...AUG_CLASS[i].o,
  }));

// ============================================================
// 4. ITERATION BADGE
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(277), w: px(214 - 84 + 1), h: px(305 - 277 + 1),
  fill: { color: RED2 },
});
slide.addText("Iteration 4", {
  x: px(84), y: px(277), w: px(131), h: px(29),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 15, bold: true, color: WHITE,
});

// ============================================================
// 5. STOP BOX
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(64), y: px(330), w: px(246 - 64 + 1), h: px(415 - 330 + 1),
  fill: { color: WHITE },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(64), y: px(330), w: px(246 - 64 + 1), h: px(415 - 330 + 1),
  line: { color: RED2, width: 1 },
});
slide.addText([
  { text: "No change in ", options: { fontFace: A, fontSize: 12, color: BLACK } },
  { text: "W", options: { fontFace: A, fontSize: 12, color: BLACK, underline: true } },
], {
  x: px(68), y: px(350), w: px(120), h: px(14),
  align: "left", valign: "middle", margin: 0, lineSpacing: 14,
});
slide.addText("Stop Iterations", {
  x: px(68), y: px(374), w: px(120), h: px(18),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 13, italic: true, color: RED,
});

// ============================================================
// 6. CALCULATION PANEL — six rows, each one text line + two bracket vectors
// ============================================================
// MEASURED per row (frame y): band, text-line band, vector-row centres, vector y-extent
const CALC = [
  // bandTop bandBot  txtTop txtBot  vecRowCy [r1,r2,r3]   vecTop vecBot   dvecL dvecR  wvecL wvecR   scalarX arrowX  keepX   weqX  wvecX
  { band: [140, 197], txt: [158, 180], cy: [153, 169, 184.5], vec: [146, 191], dx: [379.5, 403.5], wv: [729.5, 753.5], scalarX: 411, arrowX: 505, keepX: 525, weqX: 704, wvx: 733 },
  { band: [207, 263], txt: [224, 244], cy: [219, 235, 251],   vec: [213, 258], dx: [379.5, 403.5], wv: [724.5, 748.5], scalarX: 411, arrowX: 500, keepX: 519, weqX: 698, wvx: 728 },
  { band: [272, 329], txt: [290, 309], cy: [286, 301, 316],   vec: [279, 322], dx: [379.5, 403.5], wv: [730.0, 754.0], scalarX: 411, arrowX: 505, keepX: 525, weqX: 704, wvx: 734 },
  { band: [338, 395], txt: [359, 379], cy: [354, 370, 386],   vec: [350, 391], dx: [380.0, 405.0], wv: [735.5, 759.5], scalarX: 412, arrowX: 510, keepX: 530, weqX: 710, wvx: 739 },
  { band: [404, 461], txt: [421, 440], cy: [417.5, 433, 448.5], vec: [409, 456], dx: [379.5, 403.5], wv: [740.5, 764.5], scalarX: 412, arrowX: 516, keepX: 535, weqX: 715, wvx: 744 },
  { band: [470, 528], txt: [487, 507], cy: [484, 499.5, 515], vec: [476, 522], dx: [380.0, 405.0], wv: [746.0, 770.0], scalarX: 411, arrowX: 522, keepX: 541, weqX: 721, wvx: 750 },
];
// frame keeps its own arithmetic errors verbatim — no [?] marker in the source, never "fix"
const CALC_ROWS = [
  { sub: "x\u2081", dvec: ["1 1 1", "-4", "0"], scalar: "= 10" },
  { sub: "x\u2082", dvec: ["1 1 2", "-4", "0"], scalar: "= -4" },
  { sub: "x\u2083", dvec: ["1 1 2", "-4", "0"], scalar: "= 10" },
  { sub: "x\u2084", dvec: ["1 5 4", "-4", "0"], scalar: "= -6" },
  { sub: "x\u2085", dvec: ["1 6 5", "-4", "0"], scalar: "= -10" },
  { sub: "x\u2086", dvec: ["1 6 6", "-4", "0"], scalar: "= -112" },
];
const W_VEC = ["14", "-4", "0"];   // identical in every row

// white panel + thin grey L/R borders (measured at x274 and x852-853) + grey rules
slide.addShape(pptx.ShapeType.rect, {
  x: px(274), y: px(139), w: px(853 - 274 + 1), h: px(528 - 139 + 1),
  fill: { color: WHITE }, line: { color: RULE, width: 1 },
});
CALC.forEach((r) => {
  slide.addShape(pptx.ShapeType.line, {
    x: px(277), y: px(r.band[0]), w: px(848 - 277), h: 0,
    line: { color: RULE, width: 1 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(277), y: px(r.band[1]), w: px(848 - 277), h: 0,
    line: { color: RULE, width: 1 },
  });
});

CALC.forEach((r, i) => {
  const row = CALC_ROWS[i];
  const [txtTop, txtBot] = r.txt;
  const txtH = txtBot - txtTop + 1;

  // -- "d(xᵢ) =" with x subscript, left-aligned at measured x283 --
  slide.addText([
    { text: "d(", options: { fontFace: A, fontSize: 12, color: BLACK } },
    { text: "x", options: { fontFace: A, fontSize: 12, color: BLACK, subscript: true } },
    { text: row.sub.slice(1), options: { fontFace: A, fontSize: 12, color: BLACK } },
    { text: ")", options: { fontFace: A, fontSize: 12, color: BLACK } },
    { text: " = ", options: { fontFace: A, fontSize: 12, color: BLACK } },
  ], {
    x: px(283), y: px(txtTop), w: px(90), h: px(txtH),
    align: "left", valign: "middle", margin: 0, lineSpacing: txtH,
  });

  // -- d(xᵢ) bracket column vector: 3 stacked rows, bracket verticals as shapes --
  bracketVector(r.cy, r.vec, row.dvec, r.dx[0], r.dx[1], r.dx[1] - r.dx[0]);

  // -- "= <scalar>" --
  slide.addText(row.scalar, {
    x: px(r.scalarX), y: px(txtTop), w: px(46), h: px(txtH),
    align: "left", valign: "middle", margin: 0, lineSpacing: txtH,
    fontFace: A, fontSize: 12, color: BLACK,
  });

  // -- "⇒ Keep same Weight" (W underlined) --
  slide.addText([
    { text: "\u21d2", options: { fontFace: A, fontSize: 12, color: BLACK } },
    { text: " ", options: { fontFace: A, fontSize: 12, color: BLACK } },
    { text: "Keep same ", options: { fontFace: A, fontSize: 12, color: BLACK } },
    { text: "Weight", options: { fontFace: A, fontSize: 12, color: BLACK, underline: true } },
  ], {
    x: px(r.arrowX), y: px(txtTop), w: px(r.weqX - r.arrowX - 4), h: px(txtH),
    align: "left", valign: "middle", margin: 0, lineSpacing: txtH,
    fontFace: A, fontSize: 12, color: BLACK,
  });

  // -- "W =" --
  slide.addText([
    { text: "W", options: { fontFace: A, fontSize: 12, color: BLACK, underline: true } },
    { text: " = ", options: { fontFace: A, fontSize: 12, color: BLACK } },
  ], {
    x: px(r.weqX), y: px(txtTop), w: px(30), h: px(txtH),
    align: "left", valign: "middle", margin: 0, lineSpacing: txtH,
    fontFace: A, fontSize: 12, color: BLACK,
  });

  // -- W bracket column vector [14; -4; 0] --
  bracketVector(r.cy, r.vec, W_VEC, r.wv[0], r.wv[1], r.wv[1] - r.wv[0]);
});

// Draws a bracket column vector: two 1px vertical strokes plus centred value rows.
// Bracket verticals are thin rects (not the ARC/line presets) so caps stay square in LO.
function bracketVector(cy, vecYR, rows, leftX, rightX, spanX) {
  const innerW = Math.max(spanX - 6, 14);
  slide.addShape(pptx.ShapeType.rect, {
    x: px(leftX), y: px(vecYR[0]), w: px(1), h: px(vecYR[1] - vecYR[0] + 1),
    fill: { color: BLACK }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(rightX), y: px(vecYR[0]), w: px(1), h: px(vecYR[1] - vecYR[0] + 1),
    fill: { color: BLACK }, line: { type: "none" },
  });
  rows.forEach((t, k) => {
    slide.addText(t, {
      x: px(leftX + 2), y: px(cy[k] - 7), w: px(innerW), h: px(14),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 12, color: BLACK,
    });
  });
}

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});
