// Build slide 004 — "Concept of LOSS Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Rebuild attempt 2 — 2026-10-23
//
// GROUND TRUTH: unique_slides/slide_004.jpg — 960x540, 1 frame px == 1 pt == 1/72 in.
// PIL-measured structure (qa/slide004/measure_boxes + measure_out_4.txt):
//   Title                     y 70..91, x ~280..660 (red/red/blue runs)
//   Box1 Original Labels      x 80..395  y  99..222  RED border, white fill
//   Box2 Predicted Labels     x 427..745 y  99..222  RED border, white fill
//   Remember box              x 784..880 y 100..152  pale-blue fill, NO border
//   Objective box             x  78..302 y 242..301  BLUE border, pale-yellow fill
//   Error box                 x  78..486 y 306..365  BLUE border, pale-yellow fill
//   Predicted/Where box       x 494..884 y 232..371  RED border, white fill
//   Define box                x  78..655 y 388..447  RED border, salmon fill
//   Formula box               x  78..486 y 464..522  BLUE border, pale-yellow fill
//
// MEASURED FILL COLORS (PIL medians, text-free interior bands):
//   pale yellow  (249,253,218) -> FFFDDA
//   salmon       (247,223,193) -> FAEBD7 family (kept per founder spec)
//   remember box (219,233,252) -> DBE9FC
//
// ATTEMPT-1 DEFECTS FIXED (all found by PIL-first adjudication of a blank render):
//   1. lineSpacing: 1.15 (an RATIO) -> pptxgenjs writes spcPts=115 HUNDREDTHS-OF-A-
//      POINT = 1.15pt line spacing, which makes LibreOffice drop EVERY text run.
//      pptxgenjs lineSpacing is POINTS. All boxes now pass explicit point values.
//      (Render attempt 1 had ALL text missing except the badge numeral.)
//   2. Predicted/Where block was unboxed on the gray panel -> now a RED-bordered
//      white box at the measured x494..884 y232..371.
//   3. Objective / Error / Formula boxes were white-filled -> now pale yellow
//      FFFDDA as measured.
//   4. Formula box sat at y455..515 with cream fill and no border -> now
//      x78..486 y464..522 with a BLUE border and pale-yellow fill.
//   5. Remember box was 150x132 white with a 6A5ACD ring -> now a 97x53
//      pale-blue-filled rect with NO border (measured).
//   6. The two vector equations were LINEAR single-line PNGs -> now rendered in
//      PROFESSIONAL 2D FORMAT (stacked column vectors) per founder directive.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_004_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const NAVY   = "000080";   // blue borders (objective, error, formula, remember)
const RED    = "C00000";   // red borders (label boxes, where, define)
const REDTXT = "FF0000";   // red text
const BLUE   = "0000FF";   // blue text
const SALMON = "FAEBD7";   // define box fill
const PALE   = "FFFDDA";   // pale yellow fill (measured 249,253,218)
const PALEBL = "DBE9FC";   // remember box fill (measured 219,233,252)
const WHITE  = "FFFFFF";
const BLACK  = "000000";
const INK    = "333333";
const WHEREBLUE = "1F1FC8"; // where-block math letters (measured)
const FONT   = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 4 });

// Helper: rectangle with fill (+ optional line)
const rect = (x, y, w, h, fill, line = null) => {
  const opts = { x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill } };
  if (line) opts.line = { color: line.color, width: line.width };
  return slide.addShape(pptx.ShapeType.rect, opts);
};

// Helper: text block. `ls` is in POINTS (pptxgenjs lineSpacing is points;
// passing a ratio produces sub-point spacing that LibreOffice silently drops).
const textbox = (x, y, w, h, runs, align = "left", valign = "top", ls = null) => {
  const opts = {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align, valign, margin: 0, fontFace: FONT,
  };
  if (ls !== null) opts.lineSpacing = ls;
  slide.addText(runs, opts);
};

// Helper: equation image at exact px/600 size (frame coords -> inches)
const ASSETS = path.resolve(__dirname, "assets");
const eqImage = (file, fx, fy, wIn, hIn) => {
  slide.addImage({ path: path.join(ASSETS, file), x: px(fx), y: px(fy), w: wIn, h: hIn });
};

// ============================================================
// 1. TITLE — "Concept of LOSS Function" y 70..91, x ~280..660
// ============================================================
// Title box is wide enough for the single line (~470 frame px of ink at 32pt
// bold Arial); a narrower box wraps "Function" onto a second line.
textbox(240, 68, 440, 26, [
  { text: "Concept of ", options: { color: REDTXT, bold: true, fontSize: 32 } },
  { text: "LOSS", options: { color: BLUE, bold: true, fontSize: 32 } },
  { text: " Function", options: { color: REDTXT, bold: true, fontSize: 32 } },
], "center", "middle", 32);

// ============================================================
// 2. BOX 1 — Original Labels (red border, white fill)
//    x 80..395, y 99..222
// ============================================================
rect(80, 99, 315, 123, WHITE, { color: RED, width: 1 });

// Original arrangement, PIL-measured on unique_slides/slide_004.jpg
// (qa/slide004/adjud5_defects.py, 1px == 1pt):
//   "Let Y ="      x 87..148, y145..157        black, box-left
//   matrix         x165..209, y115..203        left / centre band
//   "Original Labels"  x246..371, y136..153    red, RIGHT of the matrix
//   "from Training Samples" x215..388, y159..177 black, UNDER the caption
// => the caption block sits beside the matrix, not stacked under it.
eqImage("eq_004_Yvec.png", 84, 102, 2.47222, 1.50000);

// "Original Labels" - bold red, to the RIGHT of the matrix (same vertical band)
textbox(245, 136, 145, 18, [
  { text: "Original Labels", options: { color: REDTXT, bold: true, fontSize: 15 } },
], "left", "top", 15);

// "from Training Samples" - black, underneath the caption
textbox(214, 158, 165, 20, [
  { text: "from Training Samples", options: { color: BLACK, fontSize: 13 } },
], "left", "top", 13);

// ============================================================
// 3. BOX 2 — Predicted Labels (red border, white fill)
//    x 427..745, y 99..222
// ============================================================
rect(427, 99, 318, 123, WHITE, { color: RED, width: 1 });

// Measured arrangement (same adjudication script): "Let Yh=" x432..494 y145..163,
// matrix x511..547 y114..208, "Predicted Labels" x587..722 y137..150 RIGHT of the
// matrix, "from Model Yh=XW" x565..735 y163..183 UNDER the caption.
eqImage("eq_004_Yhatvec.png", 428, 104, 1.91667, 1.59722);

// "Predicted Labels" - bold blue, to the RIGHT of the matrix (same vertical band)
textbox(587, 137, 145, 18, [
  { text: "Predicted Labels", options: { color: BLUE, bold: true, fontSize: 15 } },
], "left", "top", 15);

// "from Model Yh=XW" - black, underneath the caption; the original underlines W
// (measured bar x720..734 y184, under the W glyph at x720..735).
textbox(565, 163, 170, 20, [
  { text: "from Model ", options: { color: BLACK, fontSize: 13 } },
  { text: "Ŷ=X", options: { color: BLACK, fontSize: 13 } },
  { text: "W", options: { color: BLACK, fontSize: 13, underline: true } },
], "left", "top", 13);

// ============================================================
// 4. REMEMBER BOX — pale-blue fill, NO border
//    x 784..880 (97px), y 100..152 (53px)
// ============================================================
rect(784, 100, 97, 53, PALEBL);

// "Remember" - bold dark-red (PIL-measured original ink RGB(169,51,74) = the
// same dark-red as the slide's other red text runs, JPEG-softened; REDTXT FF0000
// is the build's red-text constant, matching "Original Labels"/"Error (Loss)").
// Underlined: the original carries a full-width bar under the header
// (measured y118, x795..864, clear gap below the text baseline).
textbox(787, 102, 92, 14, [
  { text: "Remember", options: { color: REDTXT, bold: true, fontSize: 11, underline: true } },
], "left", "top", 11);

// "||a||2 = a^T a"
eqImage("eq_004_norm.png", 797.92, 126.78, 1.13600, 0.27400);

// ============================================================
// 5. OBJECTIVE BOX — blue border, pale-yellow fill
//    x 78..302, y 242..301
// ============================================================
rect(78, 242, 224, 59, PALE, { color: NAVY, width: 1 });

textbox(84, 242, 212, 59, [
  { text: "Objective is ", options: { color: INK, fontSize: 14 } },
  { text: "Ŷ=Y", options: { color: INK, fontSize: 14, italic: true } },
], "left", "middle", 14);

// The original shows NO underline under "Ŷ=Y" — PIL-measured: the Objective box's
// ink ends at y286 (descenders) and the bottom border starts y299; no isolated
// >=8px-wide bar exists under the phrase, so the blank stays blank (a free "—" in
// the original's own spacing is not a line).

// ============================================================
// 6. ERROR BOX — blue border, pale-yellow fill
//    x 78..486, y 306..365
// ============================================================
rect(78, 306, 408, 59, PALE, { color: NAVY, width: 1 });

textbox(84, 306, 396, 59, [
  { text: "If ", options: { color: INK, fontSize: 14 } },
  // PIL-measured in unique_slides/slide_004.jpg: "Ŷ≠Y" run is BLUE at slide x136..181,
  // 336 blueish px, core [0,0,139] -> 00008B (rejudge adjudication 2026-10-27, confirmed)
  { text: "Ŷ≠Y", options: { color: "00008B", fontSize: 14, italic: true } },
  { text: " ⇒ There is an ", options: { color: INK, fontSize: 14 } },
  { text: "Error (Loss)", options: { color: REDTXT, bold: true, fontSize: 14 } },
], "left", "middle", 14);

// ============================================================
// 7. PREDICTED / WHERE BOX — red border, white fill
//    x 494..884, y 232..371 (measured: the block IS boxed, not free-floating)
// ============================================================
rect(494, 234, 388, 137, WHITE, { color: RED, width: 1 });

// Line 1 "Ŷ = XW": Ŷ black bold, X/W blue bold-italic (measured 1F1FC8);
// the X–W gap is real in the original. Underlines are separate line shapes,
// not run underlines (measured bars: Ŷ x508..526 y278 black, W x566..584 y278
// red; the X at x541..556 is NOT underlined). "Predicted" is its own red
// box well to the right (measured x672..760 y256..278), not inline.
textbox(505, 252, 120, 22, [
  { text: "Ŷ", options: { color: INK, bold: true, fontSize: 16 } },
  { text: " = ", options: { color: INK, fontSize: 16 } },
  { text: "X", options: { color: WHEREBLUE, bold: true, italic: true, fontSize: 16 } },
  { text: " W", options: { color: REDTXT, bold: true, italic: true, fontSize: 16 } },
], "left", "top", 16);
slide.addShape(pptx.ShapeType.line, {
  x: px(508), y: px(266), w: px(18), h: 0,
  line: { color: BLACK, width: 1.5 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(551), y: px(266), w: px(15), h: 0,
  line: { color: REDTXT, width: 1.5 },
});
textbox(672.5, 256, 88, 22, [
  { text: "Predicted", options: { color: REDTXT, bold: true, italic: true, fontSize: 14 } },
], "left", "top", 14);

// Three fact lines with the original's staircase indentation (measured line
// x-origins 506 / 572.5 / 564, tops 284/309/336), clean typographic
// subscripts (subscript: true — same idiom as slide_003.js), bold emphasis
// on matrix/vector/Given/Required, and right-aligned ⇒-tag column at x770.
// pptxgenjs v4 multi-line law: ONLY separate addText calls per line render
// every line (see the retired WHERE_LINES block history below).
const whereLine = (x, y, runs) => textbox(x, y, 220, 22, runs, "left", "top", 13);
const whereArrow = (y, tag, tagY) => {
  textbox(770, y, 22, 16, [
    { text: "⇒", options: { color: INK, bold: true, fontSize: 13 } },
  ], "center", "middle", 13);
  textbox(799, tagY, 80, 22, [
    { text: tag, options: { color: INK, bold: true, fontSize: 13 } },
  ], "left", "top", 13);
};

// L2: Where : X_{N x d+1} is a matrix ⇒ Given
whereLine(506, 284, [
  { text: "Where", options: { color: INK, italic: true, fontSize: 13 } },
  { text: " : ", options: { color: INK, fontSize: 13 } },
  { text: "X", options: { color: WHEREBLUE, bold: true, italic: true, fontSize: 13 } },
  { text: "N x d+1", options: { color: WHEREBLUE, italic: true, fontSize: 9.5, subscript: true } },
  { text: " is a ", options: { color: INK, fontSize: 13 } },
  { text: "matrix", options: { color: INK, bold: true, fontSize: 13 } },
]);
whereArrow(286, "Given", 284);

// L3: Y_{N x 1} is labels vector ⇒ Given  (Y red with red underline)
whereLine(572.5, 309, [
  { text: "Y", options: { color: REDTXT, bold: true, italic: true, fontSize: 13 } },
  { text: "N x 1", options: { color: REDTXT, italic: true, fontSize: 9.5, subscript: true } },
  { text: " is labels ", options: { color: INK, fontSize: 13 } },
  { text: "vector", options: { color: INK, bold: true, fontSize: 13 } },
]);
slide.addShape(pptx.ShapeType.line, {
  x: px(574), y: px(322.5), w: px(17), h: 0,
  line: { color: REDTXT, width: 1.5 },
});
whereArrow(311, "Given", 309);

// L4: W is Model Parameter ⇒ Required  (W red with red underline)
whereLine(564, 336, [
  { text: "W", options: { color: REDTXT, bold: true, italic: true, fontSize: 13 } },
  { text: " is Model Parameter ", options: { color: INK, fontSize: 13 } },
]);
slide.addShape(pptx.ShapeType.line, {
  x: px(565), y: px(348), w: px(19), h: 0,
  line: { color: REDTXT, width: 1.5 },
});
whereArrow(338, "Required", 336);

// ============================================================
// 8. DEFINE BOX — red border, salmon fill
//    x 75..660, y 387..448
// ============================================================
rect(75, 387, 585, 61, SALMON, { color: RED, width: 1 });

textbox(82, 387, 571, 61, [
  { text: "Define ", options: { color: INK, fontSize: 15 } },
  { text: "Loss", options: { color: REDTXT, bold: true, fontSize: 15 } },
  { text: " function as ", options: { color: INK, fontSize: 15 } },
  { text: "squared distance", options: { color: BLUE, bold: true, fontSize: 15 } },
  { text: " between ", options: { color: INK, fontSize: 15 } },
  { text: "Ŷ", options: { color: INK, fontSize: 15, italic: true } },
  { text: " and ", options: { color: INK, fontSize: 15 } },
  { text: "Y", options: { color: INK, fontSize: 15, italic: true } },
], "left", "middle", 15);

// ============================================================
// 9. FORMULA BOX — blue border, pale-yellow fill
//    x 78..486, y 464..522
// ============================================================
rect(78, 464, 408, 58, PALE, { color: NAVY, width: 1 });

// "Loss = ||Y - Ŷ||2 = (Y - Ŷ)^T (Y - Ŷ)"
// Placement maps the asset's ink onto the original's measured ink span
// x93..392 (299 frame px) with y-top 472.8 — NOT the sidecar's ×1.2 native
// size (that put the equation at x171..437, right-shifted 78px and 15% short).
// Asset ink is two-tone: "Loss =" recolored red, body black (recolor_vectors.py).
eqImage("eq_004_formula.png", 93, 472.8, 4.1528, 0.3789);

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
