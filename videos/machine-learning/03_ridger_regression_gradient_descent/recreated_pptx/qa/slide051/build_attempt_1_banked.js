// Slide 051 — machine-learning/03_ridger_regression_gradient_descent
// "Check Classes" (Perceptron — final slide of the deck).
// Built from PIL measurement of unique_slides/slide_051.jpg (960x540 frame, 1px = 1pt).
//
// MEASURED GEOMETRY (frame px; banked in qa/slide051/measurements_051.json):
//
//   chrome          : panel x54..903 y45..540 (E9E9E7), C00000 1pt strokes
//                     LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 (NO top stroke),
//                     badge d35 centred (876,73), numeral "51"
//   pale card       : x68..720 y54..130, border (32,24,109) 2pt, fill (254,255,232)
//   sample matrix   : header x1..x6 y64..74 (cols x91-97/114-119/135-146/158-164/
//                     181-187/204-214); rows (1)(2)(1)(5)(6)(6) y77..91 and
//                     (1)(1)(2)(4)(5)(6) y94..108; class row C1 C1 C1 C2 C2 C2
//                     y113..125 (red / blue)
//   centre block    : "Initial W =" x265..315 y75..85; bracketed column vector
//                     [4; -2; -2] bars x329..333 & x351..354 y59..106 with entries
//                     4 y61..71, -2 y77..87, -2 y93..102; red "Step η = 1"
//                     x365..435 y67..81
//   legend          : y110..124 — C1(red) x240..255, positive x262..312,
//                     C2(blue) x327..336, negative x344..396,
//                     Zero(green) x413..439, "is unaccepted" x447..520
//   label           : "Check classes of" x498..583 y78..89 (black)
//   Z test matrix   : x597..658, header Z1 Z2 Z3 y64..76 (cols x600..613/621..635/
//                     643..655), 2 data rows y80..110 read as 3 COLUMNS x 2 ROWS:
//                     cols = (0,7,3) and (0,6,2) -> Z1=(0,0), Z2=(7,6), Z3=(3,2)
//   augmented matrix: heading "Augmented Vectors (from Top)" navy x81..236 y147..159;
//                     header x1..x6 y166..175; rows y180..199 / y197..225 / y231..243
//                     (3 rows x 6 cols: bias 1s, then (1,2,1,5,6,6), (1,1,2,4,5,6));
//                     class row y231..243 (red x93..145 / blue x184..218)
//   red box         : x78..239 y277..305, fill (194,0,3), white bold "Check Classes"
//   decision rows   : three white cards x276..853, tops y141 / y207 / y273
//                     (2pt grey border (159,168,177)); each holds a blue d(Zn) label,
//                     a green bracketed weight vector [5; -1; -1] (bars x381..382 and
//                     x404..405, interior 3 lines), then the chain
//                     "= <val>" / "<condition>" / "<class tag>".
//                     Arithmetic check: W=(5,-1,-1) gives (1,0,0)FW=5,
//                     (1,7,6)FW=-8, (1,3,2)FW=0 — exactly the printed results, so the
//                     DEC bracket interior is the weight vector, not the Z vectors.
//   bottom-right    : connected-component scan finds NO mouse-pointer cursor in the
//                     frame (only the bottom chrome stroke) — nothing drawn.

const pptxgenpkg = require("pptxgenjs");
const path = require("path");
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

// ================= 1. PALE CARD (x68..720, y54..130) =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(68), y: fx(54), w: fx(720 - 68), h: fx(130 - 54),
  fill: { color: CREAM }, line: { color: NAVY, width: 2 },
});

// ================= 2. LEFT SAMPLE MATRIX =================
const HDR_X = [91, 114, 135, 158, 181, 204];
HDR_X.forEach(function (x, i) {
  s.addText([
    { text: "x", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(x), y: fx(63), w: fx(18), h: fx(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

const COLS = [91, 114, 135, 158, 181, 204]; // glyph centres, pitch ~23
const ROWS = [
  { y: 76, vals: ["1", "2", "1", "5", "6", "6"] },
  { y: 93, vals: ["1", "1", "2", "4", "5", "6"] },
];
ROWS.forEach(function (r) {
  r.vals.forEach(function (v, i) {
    s.addText("(" + v + ")", {
      x: fx(COLS[i] - 6), y: fx(r.y), w: fx(20), h: fx(14),
      fontFace: FONT, fontSize: 10, color: BLACK,
      align: "center", valign: "middle", margin: 0,
    });
  });
});

const CLS = [
  ["C1", 90, RED], ["C1", 112, RED], ["C1", 134, RED],
  ["C2", 157, BLUE], ["C2", 179, BLUE], ["C2", 203, BLUE],
];
CLS.forEach(function (c) {
  s.addText([
    { text: "C", options: { fontSize: 10, color: c[2], bold: true } },
    { text: c[0][1], options: { fontSize: 8, color: c[2], bold: true, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(110), w: fx(20), h: fx(16),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
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

// red "Step η = 1" — Step x365..391, η x401..409, = x414..422, 1 x429..435
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

// ================= 5. RIGHT Z TEST MATRIX =================
// header Z1 Z2 Z3 (3 columns)
const Z_HDR = [600, 621, 643];
Z_HDR.forEach(function (x, i) {
  s.addText([
    { text: "Z", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(x), y: fx(63), w: fx(20), h: fx(14),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});
// 2 data rows, each 3 paren-wrapped digits: (0)(7)(3) then (0)(6)(2)
const Z_ROWS = [
  { y: 80, vals: ["0", "7", "3"] },
  { y: 95, vals: ["0", "6", "2"] },
];
Z_ROWS.forEach(function (r) {
  r.vals.forEach(function (v, i) {
    s.addText("(" + v + ")", {
      x: fx(Z_HDR[i] - 5), y: fx(r.y), w: fx(22), h: fx(14),
      fontFace: FONT, fontSize: 10, color: BLACK,
      align: "center", valign: "middle", margin: 0,
    });
  });
});

// ================= 6. AUGMENTED MATRIX (middle-left) =================
s.addText("Augmented Vectors (from Top)", {
  x: fx(81), y: fx(146), w: fx(158), h: fx(14),
  fontFace: FONT, fontSize: 11, color: NAVY, bold: true, align: "left", valign: "middle", margin: 0,
});

const AUG_HDR = [93, 116, 139, 162, 185, 208];
AUG_HDR.forEach(function (x, i) {
  s.addText([
    { text: "x", options: { fontSize: 10, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(x), y: fx(165), w: fx(18), h: fx(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

const AUG_ROWS = [
  { y: 179, vals: ["1", "1", "1", "1", "1", "1"] },
  { y: 197, vals: ["1", "2", "1", "5", "6", "6"] },
  { y: 215, vals: ["1", "1", "2", "4", "5", "6"] },
];
AUG_ROWS.forEach(function (r) {
  r.vals.forEach(function (v, i) {
    s.addText("(" + v + ")", {
      x: fx(AUG_HDR[i] - 6), y: fx(r.y), w: fx(20), h: fx(12),
      fontFace: FONT, fontSize: 10, color: BLACK,
      align: "center", valign: "middle", margin: 0,
    });
  });
});

const AUG_CLS = [
  ["C1", 93, RED], ["C1", 116, RED], ["C1", 139, RED],
  ["C2", 184, BLUE], ["C2", 206, BLUE], ["C2", 210, BLUE],
];
AUG_CLS.forEach(function (c) {
  s.addText([
    { text: "C", options: { fontSize: 10, color: c[2], bold: true } },
    { text: c[0][1], options: { fontSize: 8, color: c[2], bold: true, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(229), w: fx(20), h: fx(16),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
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
// white cards x276..853 at y141 / y207 / y273, 2pt grey border
[141, 207, 273].forEach(function (y) {
  s.addShape(pptx.ShapeType.rect, {
    x: fx(276), y: fx(y), w: fx(853 - 276), h: fx(56),
    fill: { color: WHITE }, line: { color: CARD_BORDER, width: 2 },
  });
});

// d(Zn) blue labels + green weight-vector brackets (constant across the 3 rows)
const DEC_BASE = [141, 207, 273];
DEC_BASE.forEach(function (base, idx) {
  const sub = String(idx + 1);
  // blue d(Zn)
  s.addText([
    { text: "d", options: { fontSize: 12, color: BLUE, italic: true } },
    { text: "(Z", options: { fontSize: 12, color: BLUE, italic: true } },
    { text: sub, options: { fontSize: 8, color: BLUE, italic: true, subscript: true } },
    { text: ")", options: { fontSize: 12, color: BLUE, italic: true } },
  ], {
    x: fx(333), y: fx(base + 8), w: fx(44), h: fx(14),
    fontFace: FONT, align: "left", valign: "middle", margin: 0,
  });
  // green bracket bars spanning the 3 interior lines
  s.addShape(pptx.ShapeType.line, {
    x: fx(381.5), y: fx(base + 4), w: 0, h: fx(46),
    line: { color: GREEN, width: 2 },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(404.5), y: fx(base + 4), w: 0, h: fx(46),
    line: { color: GREEN, width: 2 },
  });
  // interior: the weight vector [5; -1; -1] in green
  ["5", "-1", "-1"].forEach(function (v, i) {
    s.addText(v, {
      x: fx(386), y: fx(base + 6 + i * 15), w: fx(16), h: fx(13),
      fontFace: FONT, fontSize: 10, color: GREEN,
      align: "center", valign: "middle", margin: 0,
    });
  });
});

// chain texts, per row: "= <val>", "<condition>", "<class tag>"
const CHAINS = [
  {
    val: "= 5", valX: 421, valColor: BLACK, cond: "Positive > 0",
    condX: 522, condColor: BLACK, cls: "Class I", clsX: 655, clsColor: RED,
  },
  {
    val: "= -8", valX: 421, valColor: BLACK, cond: "Negative < 0",
    condX: 532, condColor: BLACK, cls: "Class II", clsX: 669, clsColor: BLUE,
  },
  {
    val: "= 0", valX: 420, valColor: BLACK, cond: "Not > 0 , Not < 0",
    condX: 512, condColor: BLACK, cls: "Undefined Class", clsX: 653, clsColor: BLUE,
  },
];
DEC_BASE.forEach(function (base, i) {
  const c = CHAINS[i];
  s.addText(c.val, {
    x: fx(c.valX), y: fx(base + 20), w: fx(34), h: fx(14),
    fontFace: FONT, fontSize: 11, color: c.valColor, align: "left", valign: "middle", margin: 0,
  });
  s.addText(c.cond, {
    x: fx(c.condX), y: fx(base + 20), w: fx(80), h: fx(14),
    fontFace: FONT, fontSize: 11, color: c.condColor, align: "left", valign: "middle", margin: 0,
  });
  s.addText(c.cls, {
    x: fx(c.clsX), y: fx(base + 20), w: fx(70), h: fx(14),
    fontFace: FONT, fontSize: 11, color: c.clsColor, bold: true, align: "left", valign: "middle", margin: 0,
  });
});

// ================= OUTPUT =================
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_051_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
