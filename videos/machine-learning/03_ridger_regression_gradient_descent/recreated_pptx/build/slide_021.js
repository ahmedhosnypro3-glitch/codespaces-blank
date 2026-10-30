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
// BLOCKS — closed rectangles, 2pt blue stroke. Rejudge r2 (2026-10-30) row census on
// the orig: stroke centers rows 128.96/256.00 (B1), 289.00/416.50 (B2), 438.00/528.00
// (B3); cols L 76.0, R 885.0 (B1) / 887.5 (B2/B3). Rect boundaries set ~0.3px below
// target so the centered stroke lands on the measured line (LO render offset):
//   B1 y129.2..256.2 x76.3..885.3 | B2 y289.3..416.8 x76.3..887.8 | B3 y438.3..528.3 x76.3..887.8
//
// EQUATIONS — matplotlib mathtext -> 600dpi PNG -> addImage at px/600.
// PLACEMENT LAW (the attempt-3 BLOCKER): a 600-dpi PNG's pixel counts are NOT frame px.
//   image height on slide = h_px/600 in = h_px*0.12 FRAME px
//   ink_left_in  = ink_left_frame/72 - 8/600   (render_eq.py pads 8 px @600dpi)
//   ink_top_in   = ink_top_frame/72  - 8/600
//   Place against the ORIGINAL's measured INK box, never by subtracting a 600-dpi
//   baseline_px from a frame-px target (that mixed the two scales and threw every
//   equation a block high).
//   original ink boxes / chosen font sizes (multi-colour composites, calibrated so the
//   TOTAL ink width matches the original within ~2%):
//     xtx     red  x97..141  y133..157  fs22       X^T X
//     det0    ink  x341..435 y187..212  fs22       |X^T X| = 0   (red X^TX 345..390)
//     d5685   ink  x338..464 y354..379  fs20.5     |X^T X| = 5685 (red X^TX 342..387)
//     regmat  ink  x89..206  y300..326  fs24       (X^T X + lambda I)
//     lam3    grn  x247..288 y305..320  fs18       lambda=3 (verbatim, no spaces; D2)
//     invexpr ink  x155..289 y466..492  fs24       (X^T X + lambda I)^-1 with \underline
//               underbars on both X glyphs (task 129; orig rows 487-488)
//   Equations are MULTI-COLOUR in the original (typography_notes): X^T X dark red,
//   "+ lambda I" blue, lambda=3 green, rest near-black - composed per-segment by
//   qa/slide021/compose_eq_021.py (probe: scratch/tmp/probe021_fontsets.py).
//
// TABLES (3x3, gridlines gray; rejudge r2 gridline census on orig: 68px cols):
//   P1 x98..302 y173..226 | P2 x90..294 y341..395 | P3 x422..626 y457..511
// TABLE ROW-HEIGHT LAW (measured 2026-10-24, the "rows drift down" defect):
//   LibreOffice treats a table row's declared height as a MINIMUM and expands it to
//   fit the glyph line-height PLUS the cell's default vertical insets. At fs14 that
//   made every row ~22.5px instead of the original's ~17.7px, pushing row-3 digits
//   ~12px below the original (and 4px past the gridline). Fix: margin:0 on the table
//   (kills the insets) + an explicit rowH array in the ORIGINAL's measured row
//   heights — then the declared height is not exceeded.
//   P1 rows [17,18,18] y173..226 | P2 rows [18,17,19] y341..395 | P3 rows [17,17,19] y458..511
// HIGHLIGHT: the middle table's diagonal cells (17/43/95) carry an OPAQUE FDFD96 band
//   around the digits only (r1c1 x107..143 y345..357, r2c2 x173..210 y363..374,
//   r3c3 x243..279 y380..392) — NOT a whole-cell saturated-yellow fill.
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
const YELLOW= "FFFF00"; // (unused now) saturated yellow — the original's is FDFD96
const HILITE= "FDFD96"; // original's diagonal-cell highlight band (measured, opaque)
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

// The original's chain arrows are DOUBLE-STROKE implication arrows "⇒" (measured
// ink ~17x10.5pt), not single-shaft "→" — glyph is a text run so both strokes render.
const arrowD = (x0, y, x1, color, pt = 23) =>
  slide.addText("\u21D2", {
    x: px(x0 - 3), y: px(y - 9), w: px(x1 - x0 + 20), h: px(18),
    align: "center", valign: "middle",
    fontSize: pt, color: color, fontFace: FONT_SERIF, margin: 0,
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
  { name: "P1", x: 76.3, y: 129.2, w: 809.0, h: 127.0 }, // top (stroke centers 128.96/256.0)
  { name: "P2", x: 76.3, y: 289.3, w: 811.5, h: 127.5 }, // middle (289.0/416.5)
  { name: "P3", x: 76.3, y: 438.3, w: 811.5, h: 90.0 },  // bottom (438.0/528.0)
];
for (const p of PANELS) {
  rect(p.x, p.y, p.w, p.h, WHITE);
  rect(p.x, p.y, p.w, p.h, null, { color: BLUE, width: 2 });
}

// ── 3. TOP PANEL (P1): singular X^T X, det 0 -> No Inverse ────────────────────
eq("eq_021_xtx.png", 97, 133, 375, 186);

const topTableData = [
  [{ text: "14" }, { text: "10" }, { text: "15" }],
  [{ text: "10" }, { text: "40" }, { text: "46" }],
  [{ text: "20" }, { text: "80" }, { text: "92" }],
];
slide.addTable(topTableData, {
  x: px(98), y: px(173), w: px(204), h: px(53),
  fontFace: FONT_SERIF, fontSize: 14, color: BLACK,
  align: "center", valign: "middle",
  border: { type: "solid", color: GRID, pt: 1 },
  margin: 0,
  rowH: [px(17), px(18), px(18)],
});

eq("eq_021_det0.png", 341, 187, 794, 230);
arrowD(460, 201, 476, BLUE);
textAt("Singular Matrix", 492, 192, 212, { boxW: 160, fontSize: 20, color: BLACK });
arrowD(660, 201, 677, BLUE);
textAt("No Inverse", 704, 193, 207, { boxW: 120, fontSize: 21, italic: true, color: RED });

// ── 4. MIDDLE PANEL (P2): (X^T X + lambda I) lambda=3, det 5685 -> Inverse Exists ──
eq("eq_021_regmat.png", 89, 300, 940, 227);
eq("eq_021_lambda3.png", 247, 305, 378, 131);

// Original highlight = an OPAQUE FDFD96 ELLIPSE behind each diagonal cell's digits
// (PIL-measured ovals, tapered not hard-edged: r1c1 x107..143 y340..363, r2c2
// x173..210 y356..378, r3c3 x243..279 y371..393). Drawn behind transparent table
// cells, so the digits sit on top.
const ellipse = (x, y, w, h, fill) =>
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill },
  });
for (const b of [
  { x: 107, y: 340, w: 37, h: 24 },
  { x: 173, y: 356, w: 38, h: 23 },
  { x: 243, y: 371, w: 37, h: 23 },
]) {
  ellipse(b.x, b.y, b.w, b.h, HILITE);
}

const midTableData = [
  ["17", "10", "15"],
  ["10", "43", "46"],
  ["20", "80", "95"],
];
slide.addTable(midTableData, {
  x: px(90), y: px(341), w: px(204), h: px(54),
  fontFace: FONT_SERIF, fontSize: 14, color: BLACK,
  align: "center", valign: "middle",
  border: { type: "solid", color: GRID, pt: 1 },
  margin: 0,
  rowH: [px(18), px(17), px(19)],
});

eq("eq_021_d5685.png", 338, 354, 1064, 215);
// P2 arrows: original ink a1 490..503, a2 729..744 (PIL, thin ~14px wide). The
// 23pt glyph measures 26px wide and jams into "Non-Singular"; 13pt lands ~15px.
arrowD(486, 368, 495, BLUE, 13);
textAt("Non-Singular Matrix", 515, 358, 378, { boxW: 210, fontSize: 23.5, color: BLACK });
arrowD(725, 368, 734, BLUE, 13);
textAt("Inverse Exists", 761, 359, 373, { boxW: 140, fontSize: 21, italic: true, color: RED });

// ── 5. BOTTOM PANEL (P3): (X^T X + lambda I)^-1 -> inverse matrix ─────────────
eq("eq_021_invexpr.png", 155, 466, 1140, 259);
arrowD(364, 480, 380, BLUE);

const botTableData = [
  [{ text: "0.07" }, { text: "0.04" }, { text: "-0.03" }],
  [{ text: "-0.01" }, { text: "0.23" }, { text: "-0.11" }],
  [{ text: "-0.01" }, { text: "-0.2" }, { text: "0.11" }],
];
slide.addTable(botTableData, {
  x: px(422), y: px(458), w: px(204), h: px(53),
  fontFace: FONT_SERIF, fontSize: 13, color: BLACK,
  align: "center", valign: "middle",
  border: { type: "solid", color: GRID, pt: 1 },
  margin: 0,
  rowH: [px(17), px(17), px(19)],
});

// ── Write ──────────────────────────────────────────────────────────────────────
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
