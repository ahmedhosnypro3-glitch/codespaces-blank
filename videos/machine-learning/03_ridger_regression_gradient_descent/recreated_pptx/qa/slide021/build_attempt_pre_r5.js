// slide_021.js — "Inverse Problem of Singular Matrix" (slide 21)
// ML lecture 03: Ridge Regression & Gradient Descent. Root slide (no deps).
// Ground truth: PIL-measured from unique_slides/slide_021.jpg (960x540, 1px=1pt).
//
// MEASUREMENT BANKS (all under recreated_pptx/qa/slide021/):
//   measure_strokes_out.txt      block stroke geometry (blueish mask b-r>25)
//   measure_mine.py / measure_tables.py
//   judge_attempt_3.txt          full-slide judge, attempt 3
//   judge_attempt_3_adjudication*.py (scratch/tmp/adjudicate_3.py + follow-ups)
//
// KEY MEASUREMENTS (frame px):
// Title: red ink x290..708 y77..101, center (499, 89), cap h=19px (~26pt serif bold)
// House chrome: house_chrome.js (panel E9E9E7 x54..903 y45..540, C00000 strokes L/R/B, badge "21")
//
// BLOCKS — closed rectangles, ~2px blue stroke (all three confirmed closed; x76 is a
// solid (46,36,123) column running the full block height):
//   B1 y129..257 x76..886 | B2 y288..418 x76..889 | B3 y437..530 x76..889
//
// EQUATIONS — matplotlib mathtext -> 600dpi PNG -> addImage at px/600.
// PLACEMENT LAW (the attempt-3 BLOCKER): a 600-dpi PNG's pixel counts are NOT frame px.
//   image height on slide = h_px/600 in = h_px*0.12 FRAME px
//   ink_left_in  = ink_left_frame/72 - 8/600   (render_eq.py pads 8 px @600dpi)
//   ink_top_in   = ink_top_frame/72  - 8/600
//   Place against the ORIGINAL's measured INK box, never by subtracting a 600-dpi
//   baseline_px from a frame-px target (that mixed the two scales and threw every
//   equation a block high).
//   original ink boxes / chosen font sizes (ink width matched within 2%):
//     xtx     red  x97..140  y133..156  fs22   |X^T X|
//     det0    red  x341..435 y187..212  fs22   |X^T X| = 0
//     d5685   red  x337..445 y354..378  fs18   |X^T X| = 5685
//     regmat  blue x89..255  y300..326  fs36   (X^T X + lambda I)
//     lam3    grn  x245..288 y304..321  fs18   lambda = 3
//     invexpr blue x154..288 y466..492  fs24   (X^T X + lambda I)^-1
//
// TABLES (3x3, gridlines gray): P1 x97..303 y173..227 | P2 x89..295 y340..395
//                               P3 x421..626 y457..511
// ARROWS — the original's chain arrows are BLUE (not black):
//   P1 a1 x460..476 @y201 | P1 a2 x660..677 @y201
//   P2 a1 x489..505 @y368 | P2 a2 x728..744 @y368 | P3 x364..380 @y480
// CHAIN TEXT: P1 "Singular Matrix" x492..626 y192..212, red italic "No Inverse" x704..794 y193..207
//             P2 "Non-Singular Matrix" x495..693 y358..378, red italic "Inverse Exists" x761..876 y359..373
// Colors: RED=C00000, BLUE=0000FF, GREEN=008000, YELLOW=FFFF00 (diag), GRID=909090

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_021_recreated.pptx");
const ASSETS = path.resolve(__dirname, "assets");

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt = 1/72 in)
const INK_PAD_IN = 8 / 600; // render_eq.py's transparent ink pad, in inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes, NO top stroke, badge "21"
drawHouseChrome(pptx, slide, { numeral: 21 });

// ── Palette ─────────────────────────────────────────────────────────────────────
const RED   = "C00000"; // title, conclusions
const BLUE  = "0000FF"; // panel borders, arrows, equation ink
const GREEN = "008000"; // lambda=3
const YELLOW= "FFFF00"; // diagonal highlights
const GRID  = "909090"; // table gridlines
const BLACK = "000000"; // table digits, chain text
const WHITE = "FFFFFF"; // panel fill
const FONT_SERIF = "Liberation Serif"; // Times-like serif (available)

// ── Helpers ────────────────────────────────────────────────────────────────────
// pptxgenjs has no {color:"none"}: a non-hex fill falls back to 000000. Omit the
// fill/line keys entirely for no-fill / no-line rects.
const rect = (x, y, w, h, fill, line) =>
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    ...(fill ? { fill: { color: fill } } : {}),
    ...(line ? { line: { color: line.color, width: line.width } } : {}),
  });

const arrow = (x0, y0, x1, y1, color, width) =>
  slide.addShape(pptx.ShapeType.line, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: color, width: width, endArrowType: "triangle" },
  });

// Equation image placed by the ORIGINAL's measured INK box (see placement law above).
const eq = (png, inkLeft, inkTop, wPx, hPx) =>
  slide.addImage({
    path: path.join(ASSETS, png),
    x: px(inkLeft) - INK_PAD_IN,
    y: px(inkTop) - INK_PAD_IN,
    w: wPx / 600,
    h: hPx / 600,
  });

// Text box whose ink band matches the original's measured band (vertically centered).
const textAt = (str, inkLeft, bandY0, bandY1, opts) =>
  slide.addText(str, {
    x: px(inkLeft), y: px(bandY0 - 2), w: px(opts.boxW), h: px(bandY1 - bandY0 + 4),
    align: "left", valign: "middle",
    fontSize: opts.fontSize, bold: !!opts.bold, italic: !!opts.italic,
    color: opts.color, fontFace: FONT_SERIF, margin: 0,
  });

// ── 1. TITLE ──────────────────────────────────────────────────────────────────
// Ink center (499, 89). Cap height 19px -> ~26pt.
slide.addText("Inverse Problem of Singular Matrix", {
  x: px(499 - 320), y: px(89 - 15), w: px(640), h: px(40),
  align: "center", valign: "middle",
  fontSize: 26, bold: true, color: RED, fontFace: FONT_SERIF, margin: 0,
});

// ── 2. THREE CONTENT PANELS ──────────────────────────────────────────────────
const PANELS = [
  { name: "P1", x: 76, y: 129, w: 810, h: 129 }, // top
  { name: "P2", x: 76, y: 288, w: 813, h: 130 }, // middle (rule lands y418)
  { name: "P3", x: 76, y: 437, w: 813, h: 93 },  // bottom
];
for (const p of PANELS) {
  rect(p.x, p.y, p.w, p.h, WHITE);
  rect(p.x, p.y, p.w, p.h, null, { color: BLUE, width: 1 });
}

// ── 3. TOP PANEL (P1): singular X^T X, det 0 -> No Inverse ────────────────────
eq("eq_021_xtx.png", 97, 133, 374, 185);

const topTableData = [
  [{ text: "14" }, { text: "10" }, { text: "15" }],
  [{ text: "10" }, { text: "40" }, { text: "46" }],
  [{ text: "20" }, { text: "80" }, { text: "92" }],
];
slide.addTable(topTableData, {
  x: px(97), y: px(173), w: px(206), h: px(54),
  fontFace: FONT_SERIF, fontSize: 14, color: BLACK,
  align: "center", valign: "middle",
  border: [{ type: "solid", color: GRID, pt: 1 }],
  row: { h: px(54 / 3) },
});

eq("eq_021_det0.png", 341, 187, 793, 229);
arrow(460, 201, 476, 201, BLUE, 2);
textAt("Singular Matrix", 492, 192, 212, { boxW: 160, fontSize: 20, color: BLACK });
arrow(660, 201, 677, 201, BLUE, 2);
textAt("No Inverse", 704, 193, 207, { boxW: 120, fontSize: 21, italic: true, color: RED });

// ── 4. MIDDLE PANEL (P2): (X^T X + lambda I) lambda=3, det 5685 -> Inverse Exists ──
eq("eq_021_regmat.png", 89, 300, 1401, 331);
eq("eq_021_lambda3.png", 245, 304, 378, 131);

const midTableData = [
  [
    { text: "17", options: { color: BLACK, fill: { color: YELLOW } } },
    { text: "10", options: { color: BLACK } },
    { text: "15", options: { color: BLACK } },
  ],
  [
    { text: "10", options: { color: BLACK } },
    { text: "43", options: { color: BLACK, fill: { color: YELLOW } } },
    { text: "46", options: { color: BLACK } },
  ],
  [
    { text: "20", options: { color: BLACK } },
    { text: "80", options: { color: BLACK } },
    { text: "95", options: { color: BLACK, fill: { color: YELLOW } } },
  ],
];
slide.addTable(midTableData, {
  x: px(89), y: px(340), w: px(206), h: px(55),
  fontFace: FONT_SERIF, fontSize: 14, color: BLACK,
  align: "center", valign: "middle",
  border: [{ type: "solid", color: GRID, pt: 1 }],
  row: { h: px(55 / 3) },
});

eq("eq_021_det5685.png", 337, 354, 935, 191);
arrow(489, 368, 505, 368, BLUE, 2);
textAt("Non-Singular Matrix", 495, 358, 378, { boxW: 210, fontSize: 18, color: BLACK });
arrow(728, 368, 744, 368, BLUE, 2);
textAt("Inverse Exists", 761, 359, 373, { boxW: 140, fontSize: 21, italic: true, color: RED });

// ── 5. BOTTOM PANEL (P3): (X^T X + lambda I)^-1 -> inverse matrix ─────────────
eq("eq_021_invexpr.png", 154, 466, 1152, 226);
arrow(364, 480, 380, 480, BLUE, 2);

const botTableData = [
  [{ text: "0.07" }, { text: "0.04" }, { text: "-0.03" }],
  [{ text: "-0.01" }, { text: "0.23" }, { text: "-0.11" }],
  [{ text: "-0.01" }, { text: "-0.2" }, { text: "0.11" }],
];
slide.addTable(botTableData, {
  x: px(421), y: px(457), w: px(205), h: px(54),
  fontFace: FONT_SERIF, fontSize: 13, color: BLACK,
  align: "center", valign: "middle",
  border: [{ type: "solid", color: GRID, pt: 1 }],
  row: { h: px(54 / 3) },
});

// ── Write ──────────────────────────────────────────────────────────────────────
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
