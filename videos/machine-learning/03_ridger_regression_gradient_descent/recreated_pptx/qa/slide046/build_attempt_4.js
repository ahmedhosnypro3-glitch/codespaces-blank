// Build slide 046 — "Perceptron Algorithm: Iteration 4 — Stop Iterations"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// ATTEMPT 4 — frame-true rebuild. The attempt-2/3 build transcribed the top
// matrix as horizontal ROWS and the Z matrix with wrong values; the frame
// (unique_slides/slide_046.jpg, 960x540, 1px = 1pt) actually shows
// PARENTHESISED COLUMN VECTORS. Every coordinate below is PIL-measured on the
// frame (measurements banked in qa/slide046/selfcheck_attempt_4.py).
//
// MEASURED FRAME FACTS (attempt 4)
//  - Top-left box: cream fill #FEFFE8, thin NAVY #221775 border, x68..720 y54..130.
//  - Top matrix = 6 parenthesised 2-value COLUMNS (x1..x6 = (1,1)(2,1)(1,2)(5,4)
//    (6,5)(6,6)); header x1..x6 y64..73; values y80..88 / y97..104; parens
//    y78..107; class row y114..124 = C1 C1 C1 in RED, C2 C2 C2 in BLUE
//    (the analysis JSON has the C1/C2 colours SWAPPED — the frame wins).
//  - Caption y110..123, x245..508: "C1 positive  C2negative   Zero  is
//    unaccepted" — C1 red, C2 blue, Zero green.
//  - "Initial" x267..305 y75..84; "W =" x305..325; vector 4 / -2 / -2 in tall
//    parens x330..371 y58..108; "Step η = 2" red bold italic x374..455 y67..80.
//  - "Check classes of" x499..581 y80..88.
//  - Z matrix: header Z1 Z1 Z1 y64..72 at x [604,627,650]; 3 parenthesised
//    COLUMNS (0,0) (7,6) (3,2) — frame values, NOT the spec's 0 0 7 / 0 6 2.
//  - Final-weight box x738..829 y58..143, fill #F9E8FA, border #D4BED5;
//    underlined W + "=" + 14 / -4 / 0 between tall parens x786..822.
//  - Augmented box x69..246 y140..255, white fill, #C0C3C8 border; title
//    "Ugmented Vectors ( from Top )" blue-violet #453CA5 x82..236 y146..159;
//    header x1..x6 y166..175; 6 columns of 3 values (1,1,1)(1,2,1)(1,1,2)
//    (1,5,4)(1,6,5)(1,6,6) y180..226; class row y232..240 C1 red / C2 blue.
//  - "Iteration 4" solid #C00000 box x84..213 y278..304, white bold text.
//  - Stop box x64..245 y331..415, fill #F9D7D8, thin red border; "No change in
//    W" (W bold italic underlined) y350..370; "Stop" RED bold italic +
//    "Iterations" BLACK italic y376..394.
//  - Scatter plot x312..825 y173..482 (generated PNG, assets/m046_plot.png):
//    white field, red border, gray grid, decision line data x=3.478,
//    blue squares (1,2)(1,1)(2,1), magenta diamonds (5,4)(6,5)(6,6),
//    red down triangles (3,2)(7,6)(0,0), red "+ve" with a LEFT arrow.
//
// House chrome: shared_patterns/house_chrome.js (deck geometry, numeral 46).
// Hex never carries '#'; fontFace explicit; margin 0; explicit lineSpacing.

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const px = (v) => v / 72;                      // frame px -> inches (1px = 1pt)
const A = "Arial";
const OUT = path.resolve(__dirname, "../slide_046_recreated.pptx");
const ASSETS = path.join(__dirname, "assets");

const RED = "C00000";
const BLUE = "0000CC";
const GREEN = "008000";
const NAVY = "221775";
const CREAM = "FEFFE8";
const LAV_FILL = "F9E8FA";
const LAV_LINE = "D4BED5";
const GRAYBLUE = "C0C3C8";
const STOP_FILL = "F9D7D8";
const AUG_TITLE = "453CA5";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 46 });

// ---------------------------------------------------------------- helpers
function txt(runs, x, y, w, h, opts = {}) {
  slide.addText(runs, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: opts.align || "left", valign: opts.valign || "middle",
    margin: 0, fontFace: A, lineSpacing: opts.lineSpacing || (opts.size || 12) * 1.2,
    charSpacing: opts.charSpacing || 0, wrap: opts.wrap === undefined ? true : opts.wrap,
  });
}
function word(text, x, y, w, h, size, color, opts = {}) {
  txt([{ text, options: { fontSize: size, color, bold: !!opts.bold, italic: !!opts.italic } }],
    x, y, w, h, { align: opts.align || "center", size, wrap: opts.wrap });
}
function subLabel(base, sub, cx, y, h, size, subSize, color, opts = {}) {
  const w = opts.w || 26;
  txt([
    { text: base, options: { fontSize: size, color, italic: opts.italic !== false, bold: !!opts.bold } },
    { text: sub, options: { fontSize: subSize, color, subscript: true, bold: !!opts.bold } },
  ], cx - w / 2, y, w, h, { align: "center", size });
}
function img(name, x, y) {
  const m = require(ASSETS + "/" + name.replace(/\.png$/, ".json"));
  slide.addImage({ path: ASSETS + "/" + name, x: px(x), y: px(y), w: m.w_in, h: m.h_in });
}

// ============================================================ TOP-LEFT BOX
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(720 - 68), h: px(130 - 54),
  fill: { color: CREAM }, line: { color: NAVY, width: 0.75 },
});

// --- matrix header x1..x6 (y64..73) ---
const TOPC = [96, 118, 140, 162, 185, 207];
TOPC.forEach((cx, i) => subLabel("x", String(i + 1), cx, 60, 16, 10, 7.5, "000000"));

// --- 6 parenthesised 2-value column vectors (y77..109) ---
const TOPV = [["1", "1"], ["2", "1"], ["1", "2"], ["5", "4"], ["6", "5"], ["6", "6"]];
TOPV.forEach((v, i) => {
  img("m046_topcol" + (i + 1) + ".png", TOPC[i] - 7.5, 77);
});

// --- class row y114..124: C1 x3 RED, C2 x3 BLUE (frame; spec has this swapped) ---
["1", "1", "1", "2", "2", "2"].forEach((s, i) =>
  subLabel("C", s, TOPC[i], 111, 16, 11.5, 8.5, s === "1" ? RED : BLUE, { bold: true, italic: false }));

// --- caption y110..123 (C1 red, C2 blue, Zero green; words italic) ---
txt([
  { text: "C", options: { fontSize: 13, bold: true, italic: true, color: RED } },
  { text: "1", options: { fontSize: 9.5, bold: true, italic: true, color: RED, subscript: true } },
  { text: " positive   ", options: { fontSize: 13, italic: true, color: "000000" } },
  { text: "C", options: { fontSize: 13, bold: true, italic: true, color: BLUE } },
  { text: "2", options: { fontSize: 9.5, bold: true, italic: true, color: BLUE, subscript: true } },
  { text: "negative    ", options: { fontSize: 13, italic: true, color: "000000" } },
  { text: "Zero", options: { fontSize: 13, bold: true, italic: true, color: GREEN } },
  { text: "  is unaccepted", options: { fontSize: 13, italic: true, color: "000000" } },
], 245, 107, 280, 20, { align: "left", size: 13 });

// ---------------------------------------------------- Initial W + Step eta
word("Initial", 266, 67, 44, 22, 11.5, "000000", { align: "left" });
txt([
  { text: "W", options: { fontSize: 12, bold: true, italic: true, underline: true, color: "000000" } },
  { text: " =", options: { fontSize: 12, bold: true, italic: true, color: "000000" } },
], 305, 66, 26, 24, { align: "left", size: 12 });
img("m046_vec_initial.png", 330, 56);              // 4 / -2 / -2 in tall parens
word("Step η = 2", 371, 63, 88, 20, 14, RED, { align: "left", bold: true, italic: true });

// ---------------------------------------------------- Check classes of + Z
word("Check classes of", 499, 75, 90, 18, 11, "000000", { align: "left" });
const ZC = [604, 627, 650];
ZC.forEach((cx, i) => subLabel("Z", "1", cx, 60, 16, 11.5, 8.5, "000000"));
["m046_zcol1.png", "m046_zcol2.png", "m046_zcol3.png"].forEach((n, i) =>
  img(n, ZC[i] - 7.5, 80));

// ================================================== FINAL-WEIGHT (lavender)
slide.addShape(pptx.ShapeType.rect, {
  x: px(738), y: px(58), w: px(829 - 738), h: px(143 - 58),
  fill: { color: LAV_FILL }, line: { color: LAV_LINE, width: 0.75 },
});
txt([
  { text: "W", options: { fontSize: 17, bold: true, italic: true, underline: true, color: "000000" } },
], 741, 82, 24, 30, { align: "center", size: 17 });
word("=", 762, 86, 16, 22, 17, "000000");
img("m046_vec_final.png", 783, 66);                // 14 / -4 / 0 in tall parens

// =================================================== AUGMENTED-VECTORS BOX
slide.addShape(pptx.ShapeType.rect, {
  x: px(69), y: px(140), w: px(246 - 69), h: px(255 - 140),
  fill: { color: "FFFFFF" }, line: { color: GRAYBLUE, width: 0.75 },
});
word("Ugmented Vectors ( from Top )", 66, 142, 187, 20, 10.7, AUG_TITLE,
  { align: "center", bold: true, italic: true, wrap: false });
const AUGC = [98, 120, 142, 165, 188, 210];
AUGC.forEach((cx, i) => subLabel("x", String(i + 1), cx, 161.5, 13, 7.8, 5.8, "000000", { w: 20 }));
["m046_augcol1.png", "m046_augcol2.png", "m046_augcol3.png",
 "m046_augcol4.png", "m046_augcol5.png", "m046_augcol6.png"].forEach((n, i) =>
  img(n, AUGC[i] - 7.5, 178));
["1", "1", "1", "2", "2", "2"].forEach((s, i) =>
  subLabel("C", s, AUGC[i], 229, 16, 11.5, 8.5, s === "1" ? RED : BLUE, { bold: true, italic: false }));

// =========================================================== ITERATION 4
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(278), w: px(213 - 84), h: px(304 - 278),
  fill: { color: RED }, line: { type: "none" },
});
word("Iteration 4", 84, 277, 129, 28, 19, "FFFFFF", { align: "center", bold: true });

// ========================================================== STOP BOX
slide.addShape(pptx.ShapeType.rect, {
  x: px(64), y: px(331), w: px(245 - 64), h: px(415 - 331),
  fill: { color: STOP_FILL }, line: { color: RED, width: 0.75 },
});
txt([
  { text: "No change in ", options: { fontSize: 19.5, color: "000000" } },
  { text: "W", options: { fontSize: 19.5, color: "000000", bold: true, italic: true, underline: true } },
], 59, 343, 176, 30, { align: "center", size: 19.5 });
txt([
  { text: "Stop", options: { fontSize: 19, color: RED, bold: true, italic: true } },
  { text: " Iterations", options: { fontSize: 19, color: "000000", italic: true } },
], 59, 371, 176, 26, { align: "center", size: 19 });

// ============================================================ SCATTER PLOT
slide.addImage({
  path: ASSETS + "/m046_plot.png",
  x: px(312), y: px(173), w: 513 / 72, h: 309 / 72,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
