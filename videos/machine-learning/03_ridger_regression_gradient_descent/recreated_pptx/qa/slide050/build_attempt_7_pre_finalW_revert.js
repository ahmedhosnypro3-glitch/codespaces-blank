// Slide 050 — machine-learning/03_ridger_regression_gradient_descent
// "Iteration 2" (Perceptron) — built from PIL measurement of
// unique_slides/slide_050.jpg (960x540 frame, 1px = 1pt).
//
// MEASURED GEOMETRY (frame px; all banked in scratch/slide050_measurements.json,
// produced by scratch/measure_050_chart_full.py + scratch/verify_050_*.py):
//
//   chrome          : panel x54..903 y45..540 (E9E9E7), C00000 1pt strokes
//                     LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 (NO top stroke),
//                     badge d35 centred (876,73), numeral "50"
//   top navy box    : x68..719 y54..130, navy 2pt border (30,26,118), CREAM fill
//                     (254,255,232) — the box encloses BOTH the data table
//                     (x68..245) and the math zone (x246..719)
//   data table      : col centres 94/117/139/162/185/208 (pitch 22.6),
//                     header x1..x6 y63..74, rows [1,2,1,5,6,6] y80..89 and
//                     [1,1,2,4,5,6] y96..105 (each cell a bracketed 1x1 digit),
//                     class row C1 C1 C1 C2 C2 C2 y112..125 (red / blue)
//   caption box     : x66..240 y134..248, WHITE fill, 1pt grey border
//                     (161,171,183), "Augmented Vectors (from Top)" navy y147..160
//   vectors table   : same 6 columns; THREE rows (augmented, leading 1s):
//                     [1,1,1,1,1,1] y183..192, [1,2,1,5,6,6] y198..207,
//                     [1,1,2,4,5,6] y214..222, class row y231..244
//   math zone       : x246..717 inside the navy box; 3 lines
//                       L1 y59..83 : "Initial W = (4/-2)" stacked (black) + "REPEAT using Step"
//                                    (red ink x415..537 — the zone right of it is BLANK cream:
//                                    the original shows no "eta = 1" text)
//                       L3 y86..120: "Check classes of" (x542..626) + Z1 Z2 Z3 labels/vectors
//                                    (x640..702; labels y74..85, vectors y86..120)
//                       L4 y110..124: key caption "C1 positive  C2 negative  Zero is unaccepted"
//                                    (x240..510; C1 red / C2 blue / Zero green / rest black)
//   pink box        : x743..830 y58..171, fill (249,232,250), underlined W = (5/-1/-1)
//   red box         : x84..213 y278..305, fill (201,0,4), white bold "Iteration 2"
//   stop text       : "No change in W" y350..371 (W underlined), "Stop Iterations"
//                     y375..394 with "Stop" in red
//   chart           : x312..824 y173..481, red border (146,22,33) 3px, white fill.
//                     axis map x_px=362.7+52.725*x, y_px=428.7-30.671*y.
//                     gridlines at data y = 7,6,5,3,2,1,0 (NO gridline at y=4 —
//                     measured; the magenta diamond (5,4) sits on that row).
//                     vertical spines x362 (left) and x784 (right).
//                     x ticks 0..8 at px 362,415,468,521,574,627,680,732,784;
//                     y ticks 7..0 at px 215,245,276,306,337,368,399,430.
//                     decision line: least-squares on 1935 red px ->
//                     y_data = -1.00417*x + 4.90556, ink from (-0.51,5.42) to
//                     (6.19,-1.31); both ends taper to a point.
//                     markers: blue squares (1,1),(2,1),(2,2); magenta diamonds
//                     (5,4),(6,5),(6,6); red triangle (7,6); red origin blob (0,0).
//                     "+ve" red text at data (0.56,3.84) with two small red arrows.

const pptxgenpkg = require("pptxgenjs");
const path = require("path");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in == 960x540 px at 1px=1pt
const s = pptx.addSlide();

drawHouseChrome(pptx, s, { numeral: "50" });

// ---------- helpers: frame px -> inches (absolute frame coordinates) ----------
const fx = (px) => px / 72;
const fw = (px) => px / 72;

const FONT = "Arial";
const BLACK = "000000";
const WHITE = "FFFFFF";
const NAVY = "1E1A76";        // measured navy ink
const RED = "FF0000";
const BLUE = "0000FF";
const RED_DARK = "C90004";    // measured red-box fill (201,0,4)
const CHART_RED = "92211B";   // measured chart border/line red (~146,22,33 / 200,48,60)
const GRID = "CFD1CE";        // measured gridline grey
const CREAM = "FFFFE8";       // measured table fill
const PINK = "F9E8FA";        // measured pink box fill
const MARK_BLUE = "1C3D5E";   // measured blue marker (28,61,94)
const MARK_MAG = "FF94FF";    // measured magenta marker (255,148,255)
const MARK_RED = "D2000F";    // measured red triangle / blob (210,0,15)
const GREEN = "008000";       // measured "Zero" green in the L4 key caption

// chart axis mapping (measured least squares over the 7 marker centres)
const X2PX = (x) => 362.7 + 52.725 * x;
const Y2PY = (y) => 428.7 - 30.671 * y;

const EQ = (name) => path.join(__dirname, "assets", name);
// sidecars are "<basename>.png" + "<basename>.json" written by render_eq.py
function eqInfo(name) { return require(EQ(name.replace(/\.png$/, "") + ".json")); }

// ================= 1. TOP NAVY BOX (encloses table + math zone) =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(68), y: fx(54), w: fw(719 - 68), h: fw(130 - 54),
  fill: { color: CREAM }, line: { color: NAVY, width: 2 },
});

// NOTE: the frame shows NO divider between the data table (x68..245) and the
// math zone (x246..717) — the only vertical strokes in the navy box are its
// own border columns x68..70 and x718..720 (measured). Nothing is drawn here.

// ================= 2. TOP-LEFT DATA TABLE =================
// header row x1..x6
[["x1", 88], ["x2", 110], ["x3", 132], ["x4", 155], ["x5", 178], ["x6", 203]].forEach(function (c) {
  s.addText([
    { text: "x", options: { fontSize: 12, color: BLACK, italic: true } },
    { text: c[0][1], options: { fontSize: 8, color: BLACK, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(62), w: fw(22), h: fw(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

const TBL_COLS = [88, 110, 132, 155, 178, 203]; // left edge of each bracketed cell
const TBL_ROWS = [
  { y: 80, vals: ["1", "2", "1", "5", "6", "6"] },
  { y: 96, vals: ["1", "1", "2", "4", "5", "6"] },
];
TBL_ROWS.forEach(function (r) {
  r.vals.forEach(function (v, i) {
    s.addText("(" + v + ")", {
      x: fx(TBL_COLS[i]), y: fx(r.y), w: fw(22), h: fw(10),
      fontFace: FONT, fontSize: 10, color: BLACK,
      align: "center", valign: "middle", margin: 0,
    });
  });
});

// class row C1 C1 C1 C2 C2 C2 (red / blue)
const CLS = [["C1", 88, RED], ["C1", 110, RED], ["C1", 132, RED],
             ["C2", 155, BLUE], ["C2", 178, BLUE], ["C2", 203, BLUE]];
CLS.forEach(function (c) {
  s.addText([
    { text: "C", options: { fontSize: 10, color: c[2], bold: true } },
    { text: c[0][1], options: { fontSize: 8, color: c[2], bold: true, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(112), w: fw(22), h: fw(13),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

// ================= 3. MATH ZONE (right half of the navy box) =================
// L1: "Initial W = (4/-2)" as a professional 2D column vector (mathtext PNG)
(function () {
  const m = eqInfo("eq_050_initialW.png");
  s.addImage({ path: EQ("eq_050_initialW.png"), x: fx(266), y: fx(63), w: m.w_in, h: m.h_in });
})();

// L1 red text: "REPEAT using Step"  (measured red ink x415..537, y59..77 — no "eta = 1"
// follows it in the original: the zone right of it is blank cream, PIL-verified;
// the prior lane's "eta" glyphs were a misread of the Initial-W "-2" denominator.)
s.addText("REPEAT using Step", {
  x: fx(425), y: fx(59), w: fw(108), h: fw(15),
  fontFace: FONT, fontSize: 11, color: CHART_RED, bold: true,
  align: "left", valign: "middle", margin: 0,
});

// L3: "Check classes of" caption (measured ink x542..626, y86..96)
s.addText("Check classes of", {
  x: fx(542), y: fx(84), w: fw(110), h: fw(15),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// L3/L4: the three Z column vectors with subscript labels (measured Z labels + parens).
// Measured: label x641..656 / x664..678 / x684..702 y74..85; vector x640..658 /
// x663..680 / x684..702 y86..120 (pitch 23).
const ZVEC = [
  { label: "Z", sub: "1", img: "eq_050_Z1.png", x: 641 },
  { label: "Z", sub: "2", img: "eq_050_Z2.png", x: 664 },
  { label: "Z", sub: "3", img: "eq_050_Z3.png", x: 686 },
];
ZVEC.forEach(function (z) {
  s.addText([
    { text: "Z", options: { fontSize: 12, color: BLACK, italic: true } },
    { text: z.sub, options: { fontSize: 9, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(z.x), y: fx(74), w: fw(16), h: fw(12),
    fontFace: FONT, align: "left", valign: "middle", margin: 0,
  });
  const m = eqInfo(z.img);
  s.addImage({ path: EQ(z.img), x: fx(z.x), y: fx(86), w: m.w_in, h: m.h_in });
});

// L4: the key caption under the math lines — measured x240..510 y110..124:
// "C1 positive  C2 negative  Zero is unaccepted" with C1 red (x240..253),
// C2 blue, Zero green (x394..423), remainder black.
s.addText([
  { text: "C", options: { color: RED, bold: true } },
  { text: "1", options: { color: RED, bold: true, subscript: true } },
  { text: " positive   ", options: { color: BLACK } },
  { text: "C", options: { color: BLUE, bold: true } },
  { text: "2", options: { color: BLUE, bold: true, subscript: true } },
  { text: " negative   ", options: { color: BLACK } },
  { text: "Zero", options: { color: GREEN } },
  { text: " is unaccepted", options: { color: BLACK } },
], {
  x: fx(240), y: fx(106), w: fw(280), h: fw(20),
  fontFace: FONT, fontSize: 13, align: "left", valign: "middle", margin: 0,
});

// ================= 4. PINK WEIGHT BOX (top-right) =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(743), y: fx(58), w: fw(830 - 743), h: fw(171 - 58),
  fill: { color: PINK }, line: { color: PINK, width: 1 },
});
(function () {
  const m = eqInfo("eq_050_finalW.png");   // underlined W = (5/-1/-1) column vector
  s.addImage({ path: EQ("eq_050_finalW.png"), x: fx(744), y: fx(69), w: m.w_in, h: m.h_in });
})();

// ================= 5. RED "Iteration 2" BOX =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(84), y: fx(278), w: fw(213 - 84), h: fw(305 - 278),
  fill: { color: RED_DARK }, line: { color: RED_DARK, width: 1 },
});
s.addText("Iteration 2", {
  x: fx(84), y: fx(278), w: fw(213 - 84), h: fw(305 - 278),
  fontFace: FONT, fontSize: 13, color: WHITE, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ================= 6. STOP TEXT =================
// "No change in W" — W underlined (measured underline y365..370)
s.addText([
  { text: "No change in ", options: { color: BLACK } },
  { text: "W", options: { color: BLACK, italic: true, underline: true } },
], {
  x: fx(78), y: fx(350), w: fw(140), h: fw(21),
  fontFace: FONT, fontSize: 11, align: "left", valign: "middle", margin: 0,
});
// "Stop Iterations" — "Stop" red, "Iterations" black (measured Stop ink x83..121)
s.addText([
  { text: "Stop", options: { color: CHART_RED, bold: true } },
  { text: " Iterations", options: { color: BLACK } },
], {
  x: fx(83), y: fx(375), w: fw(140), h: fw(19),
  fontFace: FONT, fontSize: 11, align: "left", valign: "middle", margin: 0,
});

// ================= 7. CHART =================
// 7a. white plot panel with the measured 3px red border
s.addShape(pptx.ShapeType.rect, {
  x: fx(312), y: fx(173), w: fw(824 - 312), h: fw(481 - 173),
  fill: { color: WHITE }, line: { color: CHART_RED, width: 3 },
});

// 7b. horizontal gridlines (data y = 7,6,5,3,2,1,0 — measured; no line at y=4)
[7, 6, 5, 3, 2, 1, 0].forEach(function (gy) {
  s.addShape(pptx.ShapeType.line, {
    x: fx(363), y: fx(Y2PY(gy)), w: fw(784 - 363), h: 0,
    line: { color: GRID, width: 1 },
  });
});

// 7c. vertical spines: left axis (x=0) and right (x=8)
[0, 8].forEach(function (sx) {
  s.addShape(pptx.ShapeType.line, {
    x: fx(X2PX(sx)), y: fx(Y2PY(7)), w: 0, h: fw(Y2PY(0) - Y2PY(7)),
    line: { color: GRID, width: 1 },
  });
});

// 7d. x tick labels 0..8
[0, 1, 2, 3, 4, 5, 6, 7, 8].forEach(function (tx) {
  s.addText(String(tx), {
    x: fx(X2PX(tx) - 10), y: fx(438), w: fw(20), h: fw(8),
    fontFace: FONT, fontSize: 8, color: BLACK, align: "center", valign: "middle", margin: 0,
  });
});
// 7e. y tick labels 7..0
[7, 6, 5, 4, 3, 2, 1, 0].forEach(function (ty) {
  s.addText(String(ty), {
    x: fx(348), y: fx(Y2PY(ty) - 5), w: fw(12), h: fw(10),
    fontFace: FONT, fontSize: 8, color: BLACK, align: "center", valign: "middle", margin: 0,
  });
});

// 7f. decision line y = -1.00417x + 4.90556 from (-0.51,5.42) to (6.19,-1.31).
//     Both measured ends taper to a point, so the line is drawn as a filled
//     triangle-free tapered shape: a thick line with a triangular arrowhead at
//     the lower-right end (the frame's taper reads as a point there).
(function () {
  const x0d = -0.51, y0d = -1.00417 * x0d + 4.90556;
  const x1d = 6.19, y1d = -1.00417 * x1d + 4.90556;
  const ax = X2PX(x0d), ay = Y2PY(y0d);
  const bx = X2PX(x1d), by = Y2PY(y1d);
  // flipY: pptxgenjs lines measure from (x,y) by w/h, and negative h is invalid,
  // so express the line top-left to bottom-right.
  const lx = ax, ly = ay, lw = bx - ax, lh = by - ay;
  s.addShape(pptx.ShapeType.line, {
    x: fx(lx), y: fx(ly), w: fw(lw), h: fw(lh),
    line: { color: CHART_RED, width: 3.5, endArrowType: "triangle" },
  });
})();

// 7g. blue squares (class C1)
[[1, 1], [2, 1], [2, 2]].forEach(function (p) {
  const cx = X2PX(p[0]), cy = Y2PY(p[1]);
  s.addShape(pptx.ShapeType.rect, {
    x: fx(cx - 4), y: fx(cy - 4), w: fw(8), h: fw(8),
    fill: { color: MARK_BLUE }, line: { color: MARK_BLUE, width: 1 },
  });
});
// 7h. magenta diamonds (class C2)
[[5, 4], [6, 5], [6, 6]].forEach(function (p) {
  const cx = X2PX(p[0]), cy = Y2PY(p[1]);
  s.addShape(pptx.ShapeType.diamond, {
    x: fx(cx - 5.5), y: fx(cy - 5.5), w: fw(11), h: fw(11),
    fill: { color: MARK_MAG }, line: { color: MARK_MAG, width: 1 },
  });
});
// 7i. red triangle at (7,6) — measured as an upward triangle 9x9 px
(function () {
  const cx = X2PX(7), cy = Y2PY(6);
  s.addShape(pptx.ShapeType.triangle, {
    x: fx(cx - 4.5), y: fx(cy - 4.5), w: fw(9), h: fw(9),
    fill: { color: MARK_RED }, line: { color: MARK_RED, width: 1 },
    rotate: 0,
  });
})();
// 7j. red origin blob at (0,0) — measured 9x9 px filled circle
(function () {
  const cx = X2PX(0), cy = Y2PY(0);
  s.addShape(pptx.ShapeType.ellipse, {
    x: fx(cx - 4.5), y: fx(cy - 4.5), w: fw(9), h: fw(9),
    fill: { color: MARK_RED }, line: { color: MARK_RED, width: 1 },
  });
})();

// 7k. "+ve" red annotation at data (0.56,3.84) with its two small red arrows.
//     Arrow 1 runs from data (0.21,4.59) down-right to (0.80,4.03);
//     arrow 2 is a short V (head at (0.65,3.58), tail at (0.36,3.30)).
s.addText("+ve", {
  x: fx(X2PX(0.56) - 21), y: fx(Y2PY(3.84) - 6), w: fw(42), h: fw(12),
  fontFace: FONT, fontSize: 11, color: CHART_RED, bold: true,
  align: "center", valign: "middle", margin: 0,
});
s.addShape(pptx.ShapeType.line, {
  x: fx(X2PX(0.21)), y: fx(Y2PY(4.59)), w: fw(X2PX(0.80) - X2PX(0.21)),
  h: fw(Y2PY(4.03) - Y2PY(4.59)),
  line: { color: CHART_RED, width: 3, endArrowType: "triangle" },
});
s.addShape(pptx.ShapeType.line, {
  x: fx(X2PX(0.36)), y: fx(Y2PY(3.58)), w: fw(X2PX(0.65) - X2PX(0.36)),
  h: fw(Y2PY(3.30) - Y2PY(3.58)),
  line: { color: CHART_RED, width: 3, beginArrowType: "triangle" },
});

// ================= 9. CAPTION BOX + AUGMENTED-VECTORS TABLE =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(66), y: fx(134), w: fw(240 - 66), h: fw(248 - 134),
  fill: { color: WHITE }, line: { color: "A1ABB5", width: 1 },
});
s.addText("Augmented Vectors (from Top)", {
  x: fx(82), y: fx(145), w: fw(155), h: fw(15),
  fontFace: FONT, fontSize: 10, color: NAVY, bold: true,
  align: "left", valign: "middle", margin: 0,
});

// header x1..x6 (same 6 columns as the top table)
const V_HDR = [["x1", 93], ["x2", 114], ["x3", 137], ["x4", 159], ["x5", 182], ["x6", 204]];
V_HDR.forEach(function (c) {
  s.addText([
    { text: "x", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: c[0][1], options: { fontSize: 8, color: BLACK, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(164), w: fw(20), h: fw(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

// three augmented rows (each cell a paren-wrapped digit, per the frame)
const V_ROWS = [
  { y: 181, vals: ["1", "1", "1", "1", "1", "1"] },
  { y: 196, vals: ["1", "2", "1", "5", "6", "6"] },
  { y: 212, vals: ["1", "1", "2", "4", "5", "6"] },
];
V_ROWS.forEach(function (r) {
  r.vals.forEach(function (v, i) {
    s.addText("(" + v + ")", {
      x: fx(V_HDR[i][1]), y: fx(r.y), w: fw(20), h: fw(10),
      fontFace: FONT, fontSize: 10, color: BLACK,
      align: "center", valign: "middle", margin: 0,
    });
  });
});

// class row beneath the augmented table
const V_CLS = [["C1", 93, RED], ["C1", 114, RED], ["C1", 137, RED],
               ["C2", 159, BLUE], ["C2", 182, BLUE], ["C2", 204, BLUE]];
V_CLS.forEach(function (c) {
  s.addText([
    { text: "C", options: { fontSize: 10, color: c[2], bold: true } },
    { text: c[0][1], options: { fontSize: 8, color: c[2], bold: true, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(231), w: fw(20), h: fw(13),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

// ================= OUTPUT =================
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_050_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
