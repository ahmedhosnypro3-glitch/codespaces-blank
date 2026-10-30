// Build slide 044 — Perceptron iteration 3 ("No title")
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Attempt 1. GROUND TRUTH: unique_slides/slide_044.jpg — 960x540, 1 frame px == 1 pt.
// All geometry below is in FRAME PX (px() converts to inches).
//
// MEASURED LAYOUT (frame px) — 50+ PIL measurement passes over the original frame;
// scripts banked at recreated_pptx/qa/slide044/measure_1..28.py, m*.py in scratch/tmp.
//
// House chrome (shared_patterns/house_chrome.js — deck-frozen, overrides spec):
//   canvas FFFFFF | panel E9E9E7 x54..903 y45..540 no border |
//   C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY (NO top stroke —
//   measured top-band red px = 0) | badge d~35 centered (876,73) fill FDFD96 ring
//   6A5ACD, bold Arial 18pt numeral "44" (= the file number, checked at build time).
//
// SPEC-vs-FRAME DEVIATIONS (the frame wins; judge GROUND RULES + house chrome law):
//   1. NO title, NO subtitle — the title area is intentionally empty.
//   2. NO scatter plot / decision line anywhere — this is a tables+text+equation slide
//      (the parent's reminders about a scatter/decision line do not apply to this frame).
//   3. Top band = ONE cream-filled navy-outlined box x68..720 y54..130 holding BOTH the
//      top-left table (x88..216) and ALL of the centre text (x266..657).
//   4. The top-left table is header "x1..x6" + TWO data rows (each cell a parenthesized
//      digit, measured glyph rows y80..89 and y96..105) + class row. The spec's
//      "3 data rows / (1)(1)(1)(2)(4)(5)" row is a transcription artifact — pixel
//      sampling finds exactly two digit bands (verified at y90/92/94 across all 6 cols).
//   5. "Initial W" bracket measures THREE glyph stacks (4 / -2 / -2 at y62..102 between
//      strokes x331 and x353) — the spec's "[4; -2]" drops the third entry. Frame wins.
//   6. T2 (left-middle box x70..246 y140..255): BLUE caption "Upgraded Vectors (from
//      Top)" at y148..159, header x1..x6 at y166..175, then exactly THREE data rows
//      (y184..192, y199..207, y214..222) matching the spec's rows, class row y232..243.
//   7. "Step n = 2" is RED italic at x365..435 y66..77; "Initial W =" is black at
//      x266..320 y75..84 (vertically centred on the bracket).
//   8. Red "Iteration 3" badge: SOLID RED rounded block x84..214 y277..305, white text
//      (white glyph ink measured inside the block, x86..151 / x151..213 at y289).
//   9. Calculation area is bounded by grey verticals at x273.5 / x852.5 (y141..527) with
//      horizontal rules at y140/197/206/263/272/338/395/404/461/470/528. Bands 1-3 carry
//      a RED "=> Update Weight" decision + RED W line (red ink measured x337..830);
//      bands 4-6 carry a BLACK decision and a plain W line (zero red measured).
//  10. The class rows split 3+3 for BOTH tables (cells 1-3 red, 4-6 blue) — measured.
//  11. The mouse-pointer icon beside d(x4) is a video-capture artifact — omitted.

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = __dirname + "/../slide_044_recreated.pptx";
const ASSETS = __dirname + "/assets/";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const A = "Arial";
const RED = "C00000";      // deck nominal accent red
const BLUE = "0000FF";
const NAVY = "221777";     // measured top-band outline core (34,23,117)
const GRAYBLUE = "A3A9B7"; // measured faint box/rule outlines
const CREAM = "FFFEE8";    // measured (254,255,234) top-band tint
const BLACK = "000000";
const WHITE = "FFFFFF";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome ----
drawHouseChrome(pptx, slide, { numeral: 44 });

// ---- helpers ----
function eqImg(name, leftPx, baselinePx) {
  const m = JSON.parse(fs.readFileSync(ASSETS + "eq_044_" + name + ".json", "utf8"));
  slide.addImage({
    path: m.path, x: px(leftPx),
    y: px(baselinePx) - m.baseline_frac * m.h_in,
    w: m.w_in, h: m.h_in,
  });
  return m;
}

// single-line text box anchored on the cap-top row of the measured ink
function line(text, size, xPx, capTopPx, color, opts = {}) {
  slide.addText(text, {
    x: px(xPx), y: px(capTopPx - 0.25 * size),
    w: px(opts.w || (text.length * size * 0.62 + 24)),
    h: px(size * 1.7),
    align: opts.align || "left", valign: "top",
    fontSize: size, bold: !!opts.bold, italic: !!opts.italic,
    color, fontFace: A, margin: 0, charSpacing: opts.charSpacing,
  });
}

// centered single-line box on a measured centre
function ctrLine(text, size, ctrPx, capTopPx, color, opts = {}) {
  const w = opts.w || (text.length * size * 0.62 + 24);
  slide.addText(text, {
    x: px(ctrPx - w / 2), y: px(capTopPx - 0.25 * size),
    w: px(w), h: px(size * 1.7),
    align: "center", valign: "top",
    fontSize: size, bold: !!opts.bold, italic: !!opts.italic,
    color, fontFace: A, margin: 0, charSpacing: opts.charSpacing,
  });
}

function vline(xPx, y0, y1, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(xPx), y: px(y0), w: 0, h: px(y1 - y0),
    line: { color: color, width: width },
  });
}
function hline(yPx, x0, x1, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x0), y: px(yPx), w: px(x1 - x0), h: 0,
    line: { color: color, width: width },
  });
}

// ================= TOP BAND: cream fill + navy outline box (x68..720 y54..130) =====
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(56), w: px(718 - 70), h: px(128 - 56),
  fill: { color: CREAM }, line: { type: "none" },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(720 - 68), h: px(130 - 54),
  fill: { type: "none" }, line: { color: NAVY, width: 1 },
});

// ---- top-left table: header + 2 data rows + class row (measured glyph rows) ----
const tblCols = [101, 123, 145, 167, 189, 212]; // measured column centres
["x₁", "x₂", "x₃", "x₄", "x₅", "x₆"].forEach((t, i) =>
  ctrLine(t, 13, tblCols[i], 64, BLACK, { w: 34 }));
["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"].forEach((t, i) =>
  ctrLine(t, 13, tblCols[i], 80, BLACK, { w: 30 }));
["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"].forEach((t, i) =>
  ctrLine(t, 13, tblCols[i], 96, BLACK, { w: 30 }));
[["C₁", RED], ["C₁", RED], ["C₁", RED], ["C₂", BLUE], ["C₂", BLUE], ["C₂", BLUE]]
  .forEach(([t, c], i) => ctrLine(t, 13, tblCols[i], 113, c, { w: 30 }));

// ---- top-centre: "Initial W = [4; -2; -2]" (3 glyph stacks measured) ----
line("Initial  W =", 14, 266, 75, BLACK, { w: 90 });
vline(331, 55, 103, BLACK, 1);
vline(353, 55, 103, BLACK, 1);
ctrLine("4", 13, 342, 62, BLACK, { w: 22 });
ctrLine("-2", 13, 343, 78, BLACK, { w: 24 });
ctrLine("-2", 13, 343, 93, BLACK, { w: 24 });

// ---- "Step η = 2" (RED, measured x365..435 y66..77) ----
line("Step η = 2", 17, 365, 66, RED, { bold: true, italic: true, w: 110 });

// ---- "Check classes of" + Z-matrix (3 cols x 2 rows, parenthesized digits) ----
line("Check classes of", 13, 499, 82, BLACK, { w: 130 });
const mCols = [605, 627, 649];
["Z₁", "Z₁", "Z₁"].forEach((t, i) => ctrLine(t, 12, mCols[i], 64, BLACK, { w: 26 }));
["(0)", "(7)", "(3)"].forEach((t, i) => ctrLine(t, 12, mCols[i], 83, BLACK, { w: 26 }));
["(0)", "(6)", "(2)"].forEach((t, i) => ctrLine(t, 12, mCols[i], 99, BLACK, { w: 26 }));

// ---- class rule line: C₁ positive, C₂ negative, Zero is unaccepted ----
slide.addText([
  { text: "C₁", options: { color: RED, bold: true } },
  { text: " positive, ", options: { color: BLACK } },
  { text: "C₂", options: { color: BLUE, bold: true } },
  { text: " negative, Zero is unaccepted", options: { color: BLACK } },
], {
  x: px(239), y: px(110 - 0.25 * 13), w: px(290), h: px(22),
  align: "left", valign: "top", fontSize: 13, fontFace: A, margin: 0,
});

// ================= LEFT-MIDDLE BOX (x70..246 y140..255) ===========================
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(140), w: px(246 - 70), h: px(255 - 140),
  fill: { type: "none" }, line: { color: GRAYBLUE, width: 1 },
});
line("Upgraded Vectors (from Top)", 11, 86, 148, BLUE, { bold: true, w: 160 });
const aCols = [100, 121, 144, 167, 189, 212];
["x₁", "x₂", "x₃", "x₄", "x₅", "x₆"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 166, BLACK, { w: 26 }));
["(1)", "(1)", "(1)", "(1)", "(1)", "(1)"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 184, BLACK, { w: 24 }));
["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 199, BLACK, { w: 24 }));
["(1)", "(2)", "(4)", "(5)", "(6)", "(6)"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 214, BLACK, { w: 24 }));
[["C₁", RED], ["C₁", RED], ["C₁", RED], ["C₂", BLUE], ["C₂", BLUE], ["C₂", BLUE]]
  .forEach(([t, c], i) => ctrLine(t, 12, aCols[i], 232, c, { w: 24 }));

// ================= CALCULATION AREA (x274..852, 6 bands) ==========================
// white background measured inside the calc area (box x276..851 y141..527; grey
// border lines at x274 and x852..853); the panel grey must NOT show through here.
slide.addShape(pptx.ShapeType.rect, {
  x: px(275), y: px(141), w: px(852 - 275), h: px(527 - 141),
  fill: { color: WHITE }, line: { type: "none" },
});
// grey bounding verticals (measured x273.5 / x852.5, y141..527)
vline(273.5, 141, 527, GRAYBLUE, 0.75);
vline(852.5, 141, 527, GRAYBLUE, 0.75);
// horizontal rules (measured)
[140, 197, 206, 263, 272, 338, 395, 404, 461, 470, 528].forEach((y) =>
  hline(y, 274, 852, GRAYBLUE, 0.75));

const bands = [
  { dx: "dx1", dec: "⇒ Update Weight", decRed: true,  w: "w1", y1: 153, y2: 168, y3: 184 },
  { dx: "dx2", dec: "⇒ Update Weight", decRed: true,  w: "w2", y1: 221, y2: 235, y3: 253 },
  { dx: "dx3", dec: "⇒ Update Weight", decRed: true,  w: "w3", y1: 281, y2: 295, y3: 312 },
  { dx: "dx4", dec: "⇒ Keep same Weight", decRed: false, w: "w4", y1: 347, y2: 360, y3: 378 },
  { dx: "dx5", dec: "⇒ Keep same Weight", decRed: false, w: "w5", y1: 414, y2: 427, y3: 444 },
  { dx: "dx6", dec: "⇒ Keep same Weight", decRed: false, w: "w6", y1: 479, y2: 492, y3: 511 },
];
// left edges of the three lines per band (measured merged ink starts x283..294)
const leftEdges = {
  dx: [287, 287, 287, 287, 283, 283],
  dec: [337, 337, 337, 338, 333, 333],
  w:  [391, 387, 388, 394, 389, 388],
};
bands.forEach((b, bi) => {
  eqImg(b.dx, leftEdges.dx[bi], b.y1 + 8);
  line(b.dec, 15, leftEdges.dec[bi], b.y2, b.decRed ? RED : BLACK, { bold: true, w: 210 });
  eqImg(b.w, leftEdges.w[bi], b.y3 + 8);
});

// ================= RED "Iteration 3" BADGE =========================================
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(84), y: px(277), w: px(214 - 84), h: px(305 - 277),
  fill: { color: "FF0000" }, line: { type: "none" }, rectRadius: 0.05,
});
slide.addText("Iteration 3", {
  x: px(84), y: px(283), w: px(214 - 84), h: px(20),
  align: "center", valign: "middle",
  fontSize: 15, bold: true, color: "FFFFFF", fontFace: A, margin: 0,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
