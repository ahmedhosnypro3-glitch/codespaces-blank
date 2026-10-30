// Slide 051 — machine-learning/03_ridger_regression_gradient_descent
// "Check Classes" (Perceptron — final slide of the deck).
// Built from PIL measurement of unique_slides/slide_051.jpg (960x540 frame, 1px = 1pt).
//
// MEASURED GEOMETRY (frame px; banked in qa/slide051/measurements_051.json plus
// qa/slide051/fix_measurements_051.txt):
//
//   chrome          : panel x54..903 y45..540 (E9E9E7), C00000 1pt strokes
//                     LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 (NO top stroke),
//                     badge d35 centred (876,73), numeral "51"
//   pale card       : x68..720 y54..130, border (32,24,109) 2pt, fill (254,255,232)
//   sample matrix   : 6 TALL-BRACKET COLUMN VECTORS, each one column of the
//                     2-row x 6-column sample matrix. Brackets are straight
//                     single-px strokes spanning BOTH data rows (y78..106);
//                     digit lines centred y84 (row 1) and y100 (row 2).
//                     bracket x pairs (L,R) and interior centre:
//                       90/102  c96     111/124  c117.5  134/147  c140.5
//                       156/170 c163    179/192  c185.5  202/214  c208
//                     header x1..x6 centres 94/116.5/140.5/161/184/209 (y64..74);
//                     class row y110..125 — C1 red c93.5/116.5/140.5,
//                     C2 blue c163.5/185.5/208.5.
//                     rows: (1)(2)(1)(5)(6)(6) / (1)(1)(2)(4)(5)(6)
//   centre block    : "Initial W =" x265..315 y75..85; bracketted column vector
//                     [4; -2; -2] bars x329..333 & x351..354 y59..106 with entries
//                     4 y61..71, -2 y77..87, -2 y93..102; red "Step η = 1"
//                     x365..435 y67..81
//   legend          : y110..124 — C1(red) x240..255, positive x262..312,
//                     C2(blue) x327..336, negative x344..396,
//                     Zero(green) x413..439, "is unaccepted" x447..520
//   label           : "Check classes of" x498..583 y78..89 (black)
//   Z test matrix   : 3 TALL-BRACKET COLUMN VECTORS (Z1 Z2 Z3) x597..658,
//                     brackets y80..108, digit lines y87 / y103:
//                     Z1 598/612 c605 = (0,0); Z2 621/634 c627.5 = (7,6);
//                     Z3 643/656 c649.5 = (3,2). Header Z1 Z2 Z3 y64..76,
//                     centres 606.5 / 628 / 649.
//                     Cross-checked against the decision rows: Z1=(0,0), Z2=(7,6),
//                     Z3=(3,2) is the reading the printed d(Zn) arithmetic forces
//                     (the analysis JSON's 3x3 grid reading contradicts it).
//   augmented matrix: heading "Augmented Vectors (from Top)" navy x81..236 y147..159;
//                     6 TALL-BRACKET COLUMN VECTORS, brackets y181..224,
//                     digit lines y188 / y203 / y218, bracket x pairs and
//                     interior centres:
//                       94/107  c100.5   115/128  c121.5   137/151  c144
//                       160/173 c166.5   182/195  c188.5   205/218  c211.5
//                     header x1..x6 y166..175; class row y231..243 —
//                     C1 red c97.5/120/142.5, C2 blue c164.5/189.5/209.5.
//                     columns: (1,1,1) (1,2,1) (1,1,2) (1,5,4) (1,6,5) (1,6,6)
//   red box         : x78..239 y277..305, fill (194,0,3), white bold "Check Classes"
//   decision rows   : three white cards x276..853, tops y141 / y207 / y273
//                     (2pt grey border (159,168,177)); each holds a blue d(Zn) label,
//                     a GREEN tall-bracket vector [5; -1; -1] (bars x383..386 and
//                     x402..406 spanning y145..191, three interior lines), then the
//                     chain "= <val>" / "<condition>" / "<class tag>" at y161..173.
//   bottom-right    : connected-component scan finds NO mouse-pointer cursor in the
//                     frame (only the bottom chrome stroke) — nothing drawn.

const pptxgenpkg = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in == 960x540 px at 1px=1pt
const s = pptx.addSlide();

drawHouseChrome(pptx, s, { numeral: "51" });

// ---------- helpers: frame px -> inches ----------
const fx = (px) => px / 72;

const FONT = "Arial";
const BLACK = "000000";
const WHITE = "FFFFFF";
const CREAM = "FEFFE8";        // measured pale-card fill (254,255,232)
const NAVY = "20186D";         // measured pale-card border (32,24,109)
const RED = "C00000";          // measured red text (~159,2,13)
const RED_BOX = "C90004";      // measured red-box fill (194,0,3)
const BLUE = "0000A8";         // measured blue text (~15,0,135)
const GREEN = "5C9A5C";        // measured DEC interior green (~101,153,105)
const GREEN_DK = "27331A";     // measured legend "Zero" green (~59,71,45)
const CARD_BORDER = "9FA8B1";  // measured decision-card border (159,168,177)

// A tall bracket column: two straight vertical strokes spanning all enclosed
// lines, with each entry centred in the interior.
function bracketColumn(L, R, yTop, yBot, vals, digitCentres, opts) {
  opts = opts || {};
  const color = opts.color || BLACK;
  const fontSize = opts.fontSize || 10;
  const strokeW = opts.strokeW == null ? 1 : opts.strokeW;
  s.addShape(pptx.ShapeType.line, {
    x: fx(L), y: fx(yTop), w: 0, h: fx(yBot - yTop),
    line: { color: color, width: strokeW },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(R), y: fx(yTop), w: 0, h: fx(yBot - yTop),
    line: { color: color, width: strokeW },
  });
  vals.forEach(function (v, i) {
    s.addText(v, {
      x: fx(L), y: fx(digitCentres[i] - 7), w: fx(R - L), h: fx(14),
      fontFace: FONT, fontSize: fontSize, color: color,
      align: "center", valign: "middle", margin: 0,
    });
  });
}

// subscripted "C1"/"C2" class tag centred at cx
function classTag(cx, y, digit, color) {
  s.addText([
    { text: "C", options: { fontSize: 10, color: color, bold: true } },
    { text: digit, options: { fontSize: 8, color: color, bold: true, subscript: true } },
  ], {
    x: fx(cx - 11), y: fx(y), w: fx(22), h: fx(16),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
}

// ================= 1. PALE CARD (x68..720, y54..130) =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(68), y: fx(54), w: fx(720 - 68), h: fx(130 - 54),
  fill: { color: CREAM }, line: { color: NAVY, width: 2 },
});

// ================= 2. LEFT SAMPLE MATRIX (6 tall bracket columns) =================
const SAMPLE = [
  { hdr: 94, L: 90, R: 102, c: 96, vals: ["1", "1"], cls: "1" },
  { hdr: 116.5, L: 111, R: 124, c: 117.5, vals: ["2", "1"], cls: "1" },
  { hdr: 140.5, L: 134, R: 147, c: 140.5, vals: ["1", "2"], cls: "1" },
  { hdr: 161, L: 156, R: 170, c: 163, vals: ["5", "4"], cls: "2" },
  { hdr: 184, L: 179, R: 192, c: 185.5, vals: ["6", "5"], cls: "2" },
  { hdr: 209, L: 202, R: 214, c: 208, vals: ["6", "6"], cls: "2" },
];
SAMPLE.forEach(function (col, i) {
  s.addText([
    { text: "x", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(col.hdr - 9), y: fx(63), w: fx(18), h: fx(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
  bracketColumn(col.L, col.R, 78, 106, col.vals, [84, 100]);
  classTag(col.c, 110, col.cls, col.cls === "1" ? RED : BLUE);
});

// ================= 3. CENTRE BLOCK =================
// "Initial W =" (black)
s.addText([
  { text: "Initial ", options: { fontSize: 12, color: BLACK } },
  { text: "W", options: { fontSize: 12, color: BLACK, italic: true } },
  { text: " =", options: { fontSize: 12, color: BLACK } },
], {
  x: fx(263), y: fx(74), w: fx(58), h: fx(14),
  fontFace: FONT, align: "left", valign: "middle", margin: 0,
});

// bracketed column vector [4; -2; -2]
s.addShape(pptx.ShapeType.line, {
  x: fx(331), y: fx(59), w: 0, h: fx(47),
  line: { color: BLACK, width: 1.5 },
});
s.addShape(pptx.ShapeType.line, {
  x: fx(352), y: fx(59), w: 0, h: fx(47),
  line: { color: BLACK, width: 1.5 },
});
["4", "-2", "-2"].forEach(function (v, i) {
  s.addText(v, {
    x: fx(333), y: fx(60 + i * 16), w: fx(17), h: fx(14),
    fontFace: FONT, fontSize: 11, color: BLACK,
    align: "center", valign: "middle", margin: 0,
  });
});

// red "Step η = 1"
s.addText([
  { text: "Step ", options: { fontSize: 12, color: RED, italic: true } },
  { text: "\u03b7", options: { fontSize: 12, color: RED, italic: true } },
  { text: " = 1", options: { fontSize: 12, color: RED } },
], {
  x: fx(363), y: fx(66), w: fx(75), h: fx(16),
  fontFace: FONT, align: "left", valign: "middle", margin: 0,
});

// ================= 4. LEGEND (y110..124) =================
s.addText([
  { text: "C", options: { fontSize: 10, color: RED, bold: true } },
  { text: "1", options: { fontSize: 8, color: RED, bold: true, subscript: true } },
], {
  x: fx(240), y: fx(109), w: fx(18), h: fx(16),
  fontFace: FONT, align: "left", valign: "middle", margin: 0,
});
s.addText("positive", {
  x: fx(262), y: fx(109), w: fx(52), h: fx(16),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});
s.addText([
  { text: "C", options: { fontSize: 10, color: BLUE, bold: true } },
  { text: "2", options: { fontSize: 8, color: BLUE, bold: true, subscript: true } },
], {
  x: fx(327), y: fx(109), w: fx(18), h: fx(16),
  fontFace: FONT, align: "left", valign: "middle", margin: 0,
});
s.addText("negative", {
  x: fx(344), y: fx(109), w: fx(54), h: fx(16),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});
s.addText("Zero", {
  x: fx(413), y: fx(109), w: fx(28), h: fx(16),
  fontFace: FONT, fontSize: 11, color: GREEN_DK, italic: true, align: "left", valign: "middle", margin: 0,
});
s.addText("is unaccepted", {
  x: fx(447), y: fx(109), w: fx(76), h: fx(16),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// "Check classes of" label
s.addText("Check classes of", {
  x: fx(496), y: fx(77), w: fx(92), h: fx(14),
  fontFace: FONT, fontSize: 12, color: BLACK, bold: true, align: "left", valign: "middle", margin: 0,
});

// ================= 5. RIGHT Z TEST MATRIX (3 tall bracket columns) =================
const Z_COLS = [
  { hdr: 606.5, L: 598, R: 612, c: 605, vals: ["0", "0"] },
  { hdr: 628, L: 621, R: 634, c: 627.5, vals: ["7", "6"] },
  { hdr: 649, L: 643, R: 656, c: 649.5, vals: ["3", "2"] },
];
Z_COLS.forEach(function (col, i) {
  s.addText([
    { text: "Z", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(col.hdr - 9), y: fx(63), w: fx(18), h: fx(14),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
  bracketColumn(col.L, col.R, 80, 108, col.vals, [87, 103]);
});

// ================= 6. AUGMENTED MATRIX (middle-left, 6 tall bracket columns) =================
s.addText("Augmented Vectors (from Top)", {
  x: fx(81), y: fx(146), w: fx(158), h: fx(14),
  fontFace: FONT, fontSize: 11, color: NAVY, bold: true, align: "left", valign: "middle", margin: 0,
});

const AUG = [
  { hdr: 100.5, L: 94, R: 107, c: 100.5, vals: ["1", "1", "1"], cls: "1" },
  { hdr: 121.5, L: 115, R: 128, c: 121.5, vals: ["1", "2", "1"], cls: "1" },
  { hdr: 144, L: 137, R: 151, c: 144, vals: ["1", "1", "2"], cls: "1" },
  { hdr: 166.5, L: 160, R: 173, c: 166.5, vals: ["1", "5", "4"], cls: "2" },
  { hdr: 188.5, L: 182, R: 195, c: 188.5, vals: ["1", "6", "5"], cls: "2" },
  { hdr: 211.5, L: 205, R: 218, c: 211.5, vals: ["1", "6", "6"], cls: "2" },
];
AUG.forEach(function (col, i) {
  s.addText([
    { text: "x", options: { fontSize: 10, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(col.hdr - 9), y: fx(165), w: fx(18), h: fx(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
  bracketColumn(col.L, col.R, 181, 224, col.vals, [188, 203, 218]);
  classTag(col.c, 229, col.cls, col.cls === "1" ? RED : BLUE);
});

// ================= 7. RED "Check Classes" BOX =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(78), y: fx(277), w: fx(239 - 78), h: fx(305 - 277),
  fill: { color: RED_BOX }, line: { color: RED_BOX, width: 1 },
});
s.addText("Check Classes", {
  x: fx(78), y: fx(277), w: fx(239 - 78), h: fx(305 - 277),
  fontFace: FONT, fontSize: 13, color: WHITE, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ================= 8. THREE DECISION ROWS =================
// White cards, border cores measured at x274 / x853, top y140 / y206 / y272,
// bottom y197 / y263 / y329.
//
// Row content, measured from unique_slides/slide_051.jpg (PIL, ink < 200):
//   black italic "d(Zn)"   x283..312        (the n is a subscript)
//   black "="              x319..324
//   BLUE augmented test vector, three glyphs at x335 / x351 / x369
//                          row1 "1 0 0", row2 "1 7 6", row3 "1 3 2"
//                          (5*1-1*7-1*6 = -8 and 5*1-1*3-1*2 = 0 fix the reading)
//   GREEN weight vector [5; -1; -1] in tall brackets, bars x381..382 / x404..405
//   black "="              x412..417, then the value at x423
//   black "=>" arrow       x500..509 (x510..519 on row 2)
//   condition text, then the colour-coded class tag
const DEC_ROWS = [
  {
    z: ["1", "0", "0"], zX: [334, 350, 369], zBase: 157,
    mainBase: 171, vecBase: [157, 173, 189],
    val: "5", arrow: [500, 165],
    cond: "Positive > 0", condX: 522, cls: "Class I", clsX: 655, clsColor: RED,
  },
  {
    z: ["1", "7", "6"], zX: [334, 351, 369], zBase: 227,
    mainBase: 240, vecBase: [227, 242, 258],
    val: "-8", arrow: [510, 234],
    cond: "Negative < 0", condX: 531, cls: "Class II", clsX: 668, clsColor: BLUE,
  },
  {
    z: ["1", "3", "2"], zX: [334, 351, 369], zBase: 293,
    mainBase: 306, vecBase: [292, 308, 324],
    val: "0", arrow: [500, 300],
    cond: "Not > 0 , Not < 0", condX: 512, cls: "Undefined Class", clsX: 652,
    clsColor: BLUE,
  },
];

// text box tops for a 12pt Arial baseline, h=14, valign middle
const TEXT_TOP = (baseline) => baseline - 11;
// text box top for the 13pt italic label, h=16
const LABEL_TOP = (baseline) => baseline - 12.5;

// the small double-line right arrow measured at x500..509 / y165..170
function implyArrow(x, y) {
  s.addShape(pptx.ShapeType.line, {
    x: fx(x), y: fx(y + 1.5), w: fx(5), h: 0,
    line: { color: BLACK, width: 1 },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(x), y: fx(y + 3.5), w: fx(5), h: 0,
    line: { color: BLACK, width: 1 },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(x + 5), y: fx(y), w: fx(4), h: fx(2),
    line: { color: BLACK, width: 1 },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(x + 5), y: fx(y + 2), w: fx(4), h: fx(2), flipV: true,
    line: { color: BLACK, width: 1 },
  });
}

DEC_ROWS.forEach(function (row, idx) {
  const sub = String(idx + 1);

  // white card
  s.addShape(pptx.ShapeType.rect, {
    x: fx(274), y: fx(140 + idx * 66), w: fx(853 - 274), h: fx(57),
    fill: { color: WHITE }, line: { color: CARD_BORDER, width: 2 },
  });

  // black italic d(Zn) label
  s.addText([
    { text: "d", options: { fontSize: 13, color: BLACK, italic: true } },
    { text: "(Z", options: { fontSize: 13, color: BLACK, italic: true } },
    { text: sub, options: { fontSize: 9, color: BLACK, italic: true, subscript: true } },
    { text: ")", options: { fontSize: 13, color: BLACK, italic: true } },
  ], {
    x: fx(282), y: fx(LABEL_TOP(row.mainBase)), w: fx(36), h: fx(16),
    fontFace: FONT, align: "left", valign: "middle", margin: 0,
  });

  // black "=" between the label and the test vector
  s.addText("=", {
    x: fx(318), y: fx(TEXT_TOP(row.mainBase)), w: fx(12), h: fx(14),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });

  // blue augmented test vector, three separately spaced glyphs
  row.z.forEach(function (d, i) {
    s.addText(d, {
      x: fx(row.zX[i]), y: fx(TEXT_TOP(row.zBase)), w: fx(10), h: fx(14),
      fontFace: FONT, fontSize: 12, color: BLUE, align: "left", valign: "middle", margin: 0,
    });
  });

  // green weight-vector bracket [5; -1; -1]
  bracketColumn(382, 405, row.vecBase[0] - 8, row.vecBase[2] + 8, ["5", "-1", "-1"],
    row.vecBase.map(function (b) { return b - 4; }), { color: GREEN, strokeW: 2, fontSize: 12 });

  // black "=" and the result value
  s.addText("=", {
    x: fx(411), y: fx(TEXT_TOP(row.mainBase)), w: fx(12), h: fx(14),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });
  s.addText(row.val, {
    x: fx(422), y: fx(TEXT_TOP(row.mainBase)), w: fx(34), h: fx(14),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });

  implyArrow(row.arrow[0], row.arrow[1]);

  // condition text and the class tag
  s.addText(row.cond, {
    x: fx(row.condX), y: fx(TEXT_TOP(row.mainBase)), w: fx(100), h: fx(14),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });
  s.addText(row.cls, {
    x: fx(row.clsX), y: fx(TEXT_TOP(row.mainBase)), w: fx(100), h: fx(14),
    fontFace: FONT, fontSize: 12, color: row.clsColor, bold: true,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= OUTPUT =================
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_051_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
