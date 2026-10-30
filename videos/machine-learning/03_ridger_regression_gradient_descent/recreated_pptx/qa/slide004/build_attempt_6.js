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
eqImage("eq_004_Yvec.png", 87, 131, 1.90373, 0.71400);

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
eqImage("eq_004_Yhatvec.png", 432, 130, 1.78800, 0.86600);

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

// "Remember" - bold black
textbox(787, 102, 92, 14, [
  { text: "Remember", options: { color: BLACK, bold: true, fontSize: 11 } },
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
  { text: "Ŷ≠Y", options: { color: INK, fontSize: 14, italic: true } },
  { text: " ⇒ There is an ", options: { color: INK, fontSize: 14 } },
  { text: "Error (Loss)", options: { color: REDTXT, bold: true, fontSize: 14 } },
], "left", "middle", 14);

// ============================================================
// 7. PREDICTED / WHERE BOX — red border, white fill
//    x 494..884, y 232..371 (measured: the block IS boxed, not free-floating)
// ============================================================
rect(494, 232, 390, 139, WHITE, { color: RED, width: 1 });

// "Ŷ = XW" + "Predicted" in red — first line. The original underlines Ŷ and W in
// this line (measured bars x506..519 y274 and x562..579 y274, i.e. under the Ŷ at
// x507..519 and the W at x563..579; the X at x541..556 is NOT underlined). The text
// is split into runs — never re-worded — only to place those two underlines.
textbox(500, 248, 378, 22, [
  { text: "Ŷ", options: { color: INK, fontSize: 16, italic: true, underline: true } },
  { text: " = X", options: { color: INK, fontSize: 16, italic: true } },
  { text: "W", options: { color: INK, fontSize: 16, italic: true, underline: true } },
  { text: "  Predicted", options: { color: REDTXT, bold: true, fontSize: 14 } },
], "left", "top", 16);

// "Where:" starts the first fact line INLINE in the original (measured: the
// y285..303 band runs "Where: X_{N×(d+1)} is a matrix ⇒ Given" as one line;
// band tops 285/314/345 -> pitch ~30).
// pptxgenjs v4 multi-line law (measured 2026-10-23 on slide_004): 'breakLine'
// emits NO <a:br/> so all runs collapse into ONE paragraph, and the nested-array
// (per-paragraph) form makes LibreOffice drop the whole shape. ONLY separate
// addText calls per line render every line — verified with pdftotext + a PIL
// ink-band check before banking. Each line is pinned to its own y so the pitch
// is explicit (LO-vs-PPT auto-pitch divergence law, founder directive (2026-10-10)).
const WHERE_LINES = [
  [
    { text: "Where: ", options: { color: INK, bold: true, fontSize: 13 } },
    { text: "X_{N×(d+1)} is a matrix ⇒ Given", options: { color: INK, fontSize: 13 } },
  ],
  [{ text: "Y_{N×1} is labels vector ⇒ Given", options: { color: INK, fontSize: 13 } }],
  [{ text: "W is Model Parameter ⇒ Required", options: { color: INK, fontSize: 13 } }],
];
const WHERE_Y = 285;      // first line top (measured: original 'Where:' band 285..303)
const WHERE_PITCH = 30;   // frame px between line tops (measured tops 285/314/345)
WHERE_LINES.forEach((runs, i) => {
  textbox(500, WHERE_Y + i * WHERE_PITCH, 378, 22, runs, "left", "top", 13);
});

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
eqImage("eq_004_formula.png", 171.54, 481.92, 3.68200, 0.33600);

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
