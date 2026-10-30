// Build slide 045 — "Iteration 4" (perceptron weight-update iteration, ROOT build, no dependencies)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_045.jpg (960x540, 1px=1pt=1/72in)
// Spec: analysis/slide_045_final.json  (PASS_WITH_FIXES, recreatability 9)
//
// MEASURED GEOMETRY (frame px — from qa/slide045/measurements_045.txt, bands_final.out,
// metrics_1.out; every value below was scanned from the frame, not guessed):
//   Canvas: white FFFFFF
//   Panel: gray E9E9E7 rect x54..903 y45..540 (house_chrome.js: C00000 L/R/bottom, NO top)
//   Badge: numeral "45" at (876,73) d~35, fill FDFD96, ring 6A5ACD, 333333 bold Arial 18pt
//   Top example panel: x68..719, y54..129 — BLUE #0000FF 1pt outline (frame x68 y60 =
//     155,146,203 — blue-dominant, R~G~B would be black), WHITE interior (frame x200 y90 =
//     240,242,220). The recreation_brief calls the border black; the frame measurement wins.
//     - left data table: header x1..x6 y64..73 (cy 68.5); 3 data rows in band y77..107
//       (cy 82 / 92.5 / 103); class row y113..125 (cy 119)
//       cols centred: 96, 118, 140.5, 163, 186, 209 (6 cols, pitch ~22.5)
//       class row measured C1 RED (x94..105) + C2 BLACK (x116..127) — cols 1,3 red; 2,4,5,6 black
//     - "Initial W =": text x266..324 y75..85, W underlined; bracket vector [4;-2;-2] with
//       verticals x330.5 / x351.5 spanning y59..105, rows at cy 66.5 / 83 / 97.5
//     - "Step η = 2": RED D8262C, x365..435 y66..80 (cy 73)
//     - "Check classes of": x499..583 y79..88 (cy 83.5)
//     - Z table: header Z1 Z1 Z1 y64..76 (cy 70) BLUE; data band y80..110, rows cy 87.5 / 102.5
//       cols centred: 605, 627.5, 650
//     - pointer arrow: small dark arrow x638..655 y115..127 (shaft + head), down-right
//   Legend line: y109..124 (cy 116.5) x240..509 — C1 RED x239..253, C2 BLUE x310..319, rest black
//   Augmented vectors table: white box x70..246 y140..255, 1pt BLACK border
//     title "Ugmented Vectors (from Top)" BLUE y147..159 x81..236 (sic: frame omits the "A")
//     row1 cy 170.5; rows2-4 cy 187.5 / 203 / 218; class row cy 237.5
//     class row measured C1 RED (x94..105) + C2 BLUE (x116..127)
//     cols centred: 99.5, 122, 144.5, 167, 189.5, 212.5
//   Iteration badge: RED D8262C fill x84..214 y277..305, WHITE bold text (cy 291)
//   Stop box: WHITE x64..246 y330..415, 1pt RED border
//     "No change in W" (W underlined) x77..130 y350..366
//     "Stop Iterations" RED FF0000 italic x85..160 y374..392
//   Calculation panel: WHITE x274..853 y139..528; light-grey D9D9D9 1pt rules at
//     y140 | 197 | 206 | 263 | 272 | 329 | 338 | 395 | 404 | 461 | 470 | 528
//     (6 rows of 57-58px, separated by ~9px double-rule gaps)
//     ONE text line per row, cy = row_top + 27.5 -> 167 / 233.5 / 299.5 / 368.5 / 431.5 / 497.5
//     TWO 3-row bracket column vectors per row, centred on that text line
//       (vector y-extent = row_top+6 .. row_top+51; row cy = vecTop + 7.5 + 15.5*k)
//     d(xᵢ) vector bracket verticals x379.5 / x403.5 (all rows)
//     W vector bracket verticals: x729.5/753.5 | 724.5/748.5 | 730/754 | 735.5/759.5 | 740.5/764.5 | 746/770
//     text run x anchors: label x283 | scalar x411 | ⇒ x505/500/505/510/516/522 |
//       "Keep same Weight" x525/519/525/530/535/541 | "W =" x704/698/704/710/715/721
//
// FRAME-VS-SPEC DEVIATIONS (frame wins — recorded, not silently "fixed"):
//   1. brief says top table header at "y 7-10%", rows y11-31% -> measured header y64..73,
//      class row y113..125.
//   2. brief says class row is "C₁ C₁ C₁ C₂ C₂ C₂" with C₁ red and C₂ BLUE everywhere.
//      MEASURED: top-left table has C₂ in BLACK (0 blue px in y113..125 x116..127);
//      the augmented table has C₂ in BLUE. Top-left table therefore keeps C₂ black.
//   3. brief says the top panel border is "black" -> measured blue-dominant (#0000FF).
//   4. Frame's own arithmetic is preserved verbatim: d(x₂) = -4 and d(x₆) = -112 do not
//      equal the dot product with W = [14;-4;0]. No [?] marker in the source; kept as written.
//   5. Spec percentages for the calc panel (x35-99%, y41-97%) match the measured box.
//   6. Text metrics: the frame's glyphs are ~15-25% LARGER than a 12pt Arial render
//      (measured: legend ink w 270px vs 233.8px; calc 'K' cap-height 10px vs 6.7px when
//      clipped). Sizes are set at 13-14pt and lineSpacing ≈ size+2 so text is not clipped.
//
// Laws honored: hex without '#'; explicit fontFace on every run; margin 0; measured geometry;
// real (not Unicode look-alike) subscripts per the deck's equation-format rule; bracket
// strokes drawn as 1px rects with line:{type:"none"} (proven idiom in build/slide_046.js).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_045_recreated.pptx";

const px = (v) => v / 72;   // frame px -> inches
const A = "Arial";
const BLUE = "0000FF";
const RED = "FF0000";
const RED2 = "D8262C";      // dark red used in accents
const BLACK = "000000";
const WHITE = "FFFFFF";
// calc panel rules: brief says #D9D9D9; measured lum 165-193 (blue-tinted from JPEG
// chroma subsampling on a 1px line).
const RULE = "D9D9D9";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- HOUSE CHROME: white canvas, gray panel, C00000 L/R/bottom strokes (NO top), badge "45" ----
drawHouseChrome(pptx, slide, { numeral: 45 });

// ---- helpers ---------------------------------------------------------------
// base letter + true subscript digit (deck idiom; never Unicode look-alikes)
function SUB(base, sub, x, y, w, h, size, subSize, color, extra) {
  slide.addText(
    [
      { text: base, options: { fontFace: A, fontSize: size, color: color } },
      { text: sub, options: { fontFace: A, fontSize: subSize, color: color, subscript: true } },
    ],
    Object.assign({
      x: px(x), y: px(y), w: px(w), h: px(h),
      align: "center", valign: "middle", margin: 0, lineSpacing: size + 2,
    }, extra || {}))
  ;
}
function CELL(cx, y0, y1, w, text, size, color, extra) {
  slide.addText(text, Object.assign({
    x: px(cx - w / 2), y: px(y0), w: px(w), h: px(y1 - y0 + 1),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: size, color: color, lineSpacing: size + 2,
  }, extra || {}));
}

// ============================================================
// 1. TOP EXAMPLE PANEL — blue 1pt outline, white interior
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(719 - 68), h: px(129 - 54),
  fill: { color: WHITE }, line: { color: BLUE, width: 1 },
});

// ---- 1a. LEFT DATA TABLE (x1..x6 header + 3 rows + class row) ----
const TOP_COLS = [96, 118, 140.5, 163, 186, 209];
TOP_COLS.forEach((cx, i) =>
  SUB("x", String(i + 1), cx - 9, 63, 18, 12, 13, 9.5, BLUE));

const TOP_ROWS_CY = [82, 92.5, 103];               // measured band y77..107
const topData = [
  ["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"],
  ["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"],
  ["(1)", "(1)", "(1)", "(4)", "(5)", "(6)"],
];
topData.forEach((row, r) =>
  TOP_COLS.forEach((cx, c) =>
    CELL(cx, TOP_ROWS_CY[r] - 6, TOP_ROWS_CY[r] + 6, 26, row[c], 13, BLACK)));

// Class row C1 C1 C1 C2 C2 C2 — measured: C1 red, C2 BLACK in this table
const TOP_CLASS = ["1", "2", "1", "2", "2", "2"];
TOP_COLS.forEach((cx, i) =>
  SUB("C", TOP_CLASS[i], cx - 9, 112, 18, 14, 13, 9.5,
      i === 0 || i === 2 ? RED2 : BLACK, { bold: true }));

// ---- 1b. "Initial W = [4; -2; -2]" ----
// Text part x266..324 y75..85; W underlined
slide.addText([
  { text: "Initial ", options: { fontFace: A, fontSize: 14, color: BLACK } },
  { text: "W", options: { fontFace: A, fontSize: 14, color: BLACK, underline: true } },
  { text: " = ", options: { fontFace: A, fontSize: 14, color: BLACK } },
], {
  x: px(266), y: px(74), w: px(80), h: px(14),
  align: "left", valign: "middle", margin: 0, lineSpacing: 16,
});
// bracket column vector [4; -2; -2]: verticals x330.5 / x351.5 spanning y59..105
[[330.5, 59, 105], [351.5, 59, 105]].forEach(([x, y0, y1]) =>
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y0), w: px(1), h: px(y1 - y0 + 1),
    fill: { color: BLACK }, line: { type: "none" },
  }));
[["4", 66.5], ["-2", 83], ["-2", 97.5]].forEach(([t, cy]) =>
  slide.addText(t, {
    x: px(333), y: px(cy - 8), w: px(20), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 13, color: BLACK, lineSpacing: 15,
  }));

// ---- 1c. "Step η = 2" in red ----
slide.addText([
  { text: "Step ", options: { fontFace: A, fontSize: 14, color: RED2 } },
  { text: "\u03b7", options: { fontFace: A, fontSize: 14, color: RED2 } },
  { text: " = 2", options: { fontFace: A, fontSize: 14, color: RED2 } },
], {
  x: px(365), y: px(65), w: px(84), h: px(16),
  align: "left", valign: "middle", margin: 0, lineSpacing: 16,
});

// ---- 1d. "Check classes of" label ----
slide.addText("Check classes of", {
  x: px(499), y: px(78), w: px(95), h: px(12),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 13, color: BLACK, lineSpacing: 15,
});

// ---- 1e. Z table (2 rows x 3 cols) ----
const Z_COLS = [605, 627.5, 650];
Z_COLS.forEach((cx) =>
  SUB("Z", "1", cx - 9, 63, 18, 14, 13, 9.5, BLUE));
const Z_DATA = [["(0)", "(7)", "(3)"], ["(0)", "(6)", "(2)"]];
const Z_ROWS_CY = [87.5, 102.5];                   // measured band y80..110
Z_DATA.forEach((row, r) =>
  Z_COLS.forEach((cx, c) =>
    CELL(cx, Z_ROWS_CY[r] - 8, Z_ROWS_CY[r] + 8, 26, row[c], 13, BLACK)));

// ---- 1f. pointer arrow from the Z matrix down-right toward the legend ----
slide.addShape(pptx.ShapeType.rect, {
  x: px(640), y: px(116), w: px(14), h: px(1),
  fill: { color: BLACK }, line: { type: "none" },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(652), y: px(119), w: px(1), h: px(7),
  fill: { color: BLACK }, line: { type: "none" },
});

// ============================================================
// 2. LEGEND LINE
// ============================================================
slide.addText([
  { text: "C", options: { fontFace: A, fontSize: 13, color: RED2, bold: true } },
  { text: "1", options: { fontFace: A, fontSize: 9.5, color: RED2, bold: true, subscript: true } },
  { text: " positive, ", options: { fontFace: A, fontSize: 13, color: BLACK } },
  { text: "C", options: { fontFace: A, fontSize: 13, color: BLUE, bold: true } },
  { text: "2", options: { fontFace: A, fontSize: 9.5, color: BLUE, bold: true, subscript: true } },
  { text: " negative, ", options: { fontFace: A, fontSize: 13, color: BLACK } },
  { text: "Zero is unaccepted", options: { fontFace: A, fontSize: 13, color: BLACK } },
], {
  x: px(240), y: px(109), w: px(272), h: px(16),
  align: "left", valign: "middle", margin: 0, lineSpacing: 15,
});

// ============================================================
// 3. AUGMENTED VECTORS TABLE
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(140), w: px(246 - 70), h: px(255 - 140),
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
// title (blue, "Ugmented Vectors (from Top)" — sic: the frame omits the leading "A")
slide.addText("Ugmented Vectors (from Top)", {
  x: px(81), y: px(147), w: px(158), h: px(13),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, color: BLUE, italic: true, lineSpacing: 14,
});
const AUG_COLS = [99.5, 122, 144.5, 167, 189.5, 212.5];
// row 1 (1)(1)(1)(1)(1)(1), cy 170.5
AUG_COLS.forEach((cx) => CELL(cx, 164, 177, 26, "(1)", 12, BLACK));
// rows 2-4, cy 187.5 / 203 / 218 (measured band y179..226)
const AUG_ROWS_CY = [187.5, 203, 218];
const AUG_DATA = [
  ["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"],
  ["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"],
  ["(1)", "(1)", "(1)", "(4)", "(5)", "(6)"],
];
AUG_DATA.forEach((row, r) =>
  AUG_COLS.forEach((cx, c) =>
    CELL(cx, AUG_ROWS_CY[r] - 8, AUG_ROWS_CY[r] + 8, 26, row[c], 12, BLACK)));
// class row C1 C1 C1 C2 C2 C2 — measured C1 red, C2 BLUE here
const AUG_CLASS = ["1", "2", "1", "2", "2", "2"];
AUG_COLS.forEach((cx, i) =>
  SUB("C", AUG_CLASS[i], cx - 9, 230, 18, 15, 12, 9,
      i === 0 || i === 2 ? RED2 : BLUE, { bold: true }));

// ============================================================
// 4. ITERATION BADGE
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(277), w: px(214 - 84), h: px(305 - 277),
  fill: { color: RED2 }, line: { type: "none" },
});
slide.addText("Iteration 4", {
  x: px(84), y: px(277), w: px(214 - 84), h: px(305 - 277),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 17, bold: true, color: WHITE, lineSpacing: 19,
});

// ============================================================
// 5. STOP BOX
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(64), y: px(330), w: px(246 - 64), h: px(415 - 330),
  fill: { color: WHITE }, line: { color: RED2, width: 1 },
});
slide.addText("No change in ", {
  x: px(77), y: px(349), w: px(60), h: px(18),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 13, color: BLACK, lineSpacing: 15,
});
slide.addText("W", {
  x: px(133), y: px(349), w: px(14), h: px(18),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 13, color: BLACK, underline: true, lineSpacing: 15,
});
slide.addText("Stop Iterations", {
  x: px(85), y: px(374), w: px(120), h: px(20),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 14, italic: true, color: RED, lineSpacing: 16,
});

// ============================================================
// 6. CALCULATION PANEL — six ruled rows, each one text line + two bracket vectors
// ============================================================
const CALC = [
  { band: [140, 197], cy: 167,   vec: [146, 191], dx: [379.5, 403.5], wv: [729.5, 753.5], scalarX: 411, arrowX: 505, keepX: 525, weqX: 704 },
  { band: [207, 263], cy: 233.5, vec: [213, 258], dx: [379.5, 403.5], wv: [724.5, 748.5], scalarX: 411, arrowX: 500, keepX: 519, weqX: 698 },
  { band: [272, 329], cy: 299.5, vec: [278, 324], dx: [379.5, 403.5], wv: [730.0, 754.0], scalarX: 411, arrowX: 505, keepX: 525, weqX: 704 },
  { band: [338, 395], cy: 368.5, vec: [344, 389], dx: [379.5, 403.5], wv: [735.5, 759.5], scalarX: 412, arrowX: 510, keepX: 530, weqX: 710 },
  { band: [404, 461], cy: 431.5, vec: [410, 455], dx: [379.5, 403.5], wv: [740.5, 764.5], scalarX: 412, arrowX: 516, keepX: 535, weqX: 715 },
  { band: [470, 528], cy: 497.5, vec: [476, 521], dx: [379.5, 403.5], wv: [746.0, 770.0], scalarX: 411, arrowX: 522, keepX: 541, weqX: 721 },
];
// The frame keeps its own arithmetic errors verbatim (no [?] marker) — never "fixed"
const CALC_ROWS = [
  { sub: "1", dvec: ["1 1 1", "-4", "0"], scalar: "= 10" },
  { sub: "2", dvec: ["1 1 2", "-4", "0"], scalar: "= -4" },
  { sub: "3", dvec: ["1 1 2", "-4", "0"], scalar: "= 10" },
  { sub: "4", dvec: ["1 5 4", "-4", "0"], scalar: "= -6" },
  { sub: "5", dvec: ["1 6 5", "-4", "0"], scalar: "= -10" },
  { sub: "6", dvec: ["1 6 6", "-4", "0"], scalar: "= -112" },
];
const W_VEC = ["14", "-4", "0"];   // identical in every row

slide.addShape(pptx.ShapeType.rect, {
  x: px(274), y: px(139), w: px(853 - 274), h: px(528 - 139),
  fill: { color: WHITE }, line: { color: RULE, width: 1 },
});
CALC.forEach((r) => [r.band[0], r.band[1]].forEach((y) =>
  slide.addShape(pptx.ShapeType.line, {
    x: px(277), y: px(y), w: px(848 - 277), h: 0,
    line: { color: RULE, width: 1 },
  })));

// bracket column vector: two 1px vertical strokes + centred value rows
function bracketVector(vecYR, rowCy, rows, leftX, rightX) {
  const span = rightX - leftX;
  [leftX, rightX].forEach((x) =>
    slide.addShape(pptx.ShapeType.rect, {
      x: px(x), y: px(vecYR[0]), w: px(1), h: px(vecYR[1] - vecYR[0] + 1),
      fill: { color: BLACK }, line: { type: "none" },
    }));
  rows.forEach((t, k) =>
    slide.addText(t, {
      x: px(leftX + 1), y: px(rowCy[k] - 8), w: px(span - 2), h: px(16),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 13, color: BLACK, lineSpacing: 15,
    }));
}

CALC.forEach((r, i) => {
  const row = CALC_ROWS[i];
  const TY = r.cy - 9, TH = 18;                    // one text line, vertically centred on cy

  // "d(xᵢ) ="  with a real subscript, left-aligned at measured x283
  slide.addText([
    { text: "d(", options: { fontFace: A, fontSize: 13, color: BLACK } },
    { text: "x", options: { fontFace: A, fontSize: 13, color: BLACK } },
    { text: row.sub, options: { fontFace: A, fontSize: 9.5, color: BLACK, subscript: true } },
    { text: ")", options: { fontFace: A, fontSize: 13, color: BLACK } },
    { text: " = ", options: { fontFace: A, fontSize: 13, color: BLACK } },
  ], {
    x: px(283), y: px(TY), w: px(92), h: px(TH),
    align: "left", valign: "middle", margin: 0, lineSpacing: 15,
  });

  bracketVector(r.vec, [r.vec[0] + 7.5, r.vec[0] + 23, r.vec[0] + 38.5], row.dvec, r.dx[0], r.dx[1]);

  // "= <scalar>"
  slide.addText(row.scalar, {
    x: px(r.scalarX), y: px(TY), w: px(58), h: px(TH),
    align: "left", valign: "middle", margin: 0,
    fontFace: A, fontSize: 13, color: BLACK, lineSpacing: 15,
  });

  // "⇒" (measured gap between the arrow and the words)
  slide.addText("\u21d2", {
    x: px(r.arrowX), y: px(TY), w: px(16), h: px(TH),
    align: "left", valign: "middle", margin: 0,
    fontFace: A, fontSize: 13, color: BLACK, lineSpacing: 15,
  });

  // "Keep same Weight" (Weight's W underlined)
  slide.addText([
    { text: "Keep same ", options: { fontFace: A, fontSize: 13, color: BLACK } },
    { text: "W", options: { fontFace: A, fontSize: 13, color: BLACK, underline: true } },
    { text: "eight", options: { fontFace: A, fontSize: 13, color: BLACK } },
  ], {
    x: px(r.keepX), y: px(TY), w: px(r.weqX - r.keepX - 6), h: px(TH),
    align: "left", valign: "middle", margin: 0, lineSpacing: 15,
  });

  // "W =" (W underlined)
  slide.addText([
    { text: "W", options: { fontFace: A, fontSize: 13, color: BLACK, underline: true } },
    { text: " = ", options: { fontFace: A, fontSize: 13, color: BLACK } },
  ], {
    x: px(r.weqX), y: px(TY), w: px(27), h: px(TH),
    align: "left", valign: "middle", margin: 0, lineSpacing: 15,
  });

  bracketVector(r.vec, [r.vec[0] + 7.5, r.vec[0] + 23, r.vec[0] + 38.5], W_VEC, r.wv[0], r.wv[1]);
});

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});
