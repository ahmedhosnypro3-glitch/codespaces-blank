// Build slide 002 — "Revision of Standard Linear Regression Model"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome = shared_patterns/house_chrome.js)
// Resumed worker (w002-resume-20261019a) — rebuilt fresh from the frame after a dead
// worker banked only measurement scripts (qa/slide002/measure_original.py, glyph_forensics.py).
//
// Ground truth: unique_slides/slide_002.jpg (960x540, 1px = 1pt = 1/72 in).
// Content = a two-line red bold centered title + a small gray plus-sign annotation
// artifact near the top-center-right + house chrome. PIL full-frame census found NO
// other content (only strokes + badge + title + plus).
//
// MEASURED geometry (frame px; JPEG smear +-2px noted):
//   L1 "Revision of Standard Linear"  ink x 197..756 (center 476.5), ink rows 199..230
//        -> cap top 199, baseline ~230.3, cap height ~30 -> fs 42 (Liberation Sans Bold
//           = Arial metrics: fs42 -> advance 558 vs 560 measured; capH 29+AA=31)
//   L2 "Regression Model"            ink x 298..655 (center 476.5), ink rows 274..314
//        -> cap top 274, baseline ~305, 'g' descender to 314; baseline pitch 75.0
//   Title color: frame ink core (172,34,48) = JPEG-darkened C00000 — statistically
//        identical to certified siblings 035/029 (cores (173,35,49), drawn C00000,
//        judge-PASSED). The spec's "#FF0000" is a vision misread of this frame;
//        family nominal C00000 wins (same law as the chrome strokes).
//   Plus sign (annotation/cursor artifact, spec step 6 mandatory): hbar x 763..772
//        y 74..76 (10x3), vbar x 766..768 y 71..81 (3x11); ink core (140,142,139)
//        -> draw spec color 808080.
//
// FRAME-VS-SPEC DEVIATIONS (frame + deck law win; documented):
//   - Spec's #F2F2F2 background / #FFFF00 badge / [?] border frame are pre-house
//     analysis values; deck house chrome (white canvas, E9E9E7 panel x54..903 y45..540,
//     C00000 L/R/bottom strokes, NO top stroke, FDFD96 badge + 6A5ACD ring, numeral
//     2) overrides them (deck AGENTS.md law).
//   - Spec's "approximately 66 pt" title size is an admitted guess; measured fit = 42pt.
//   - The 1px tan halo row at y46 across the panel (present on ALL deck frames incl.
//     reference slide_003: 846/850 px, mean (183,166,170)) is the panel-top JPEG/video
//     edge artifact, NOT chrome law ("NO TOP STROKE", "rect carries NO border line")
//     -> not drawn; adjudication record banked in worker_report.md.
//
// Title lines are TWO single-line boxes (fixed y per line = pixel-exact 75px pitch,
// no LO/PPT auto-pitch divergence). lineSpacing pinned (50pt, above the 46.9pt
// natural extent so LO never clips ascenders). Boxes ~43% wider than the longest
// ink (no wrap). LO placement model + constants from certified sibling slide_035:
//   baseline = top + halfLead + ascent + LO_offset  (halfLead=(LS-natural)/2=1.52,
//   ascent 38.05, LO offset ~+1.5 at 42pt) -> top1 = 230.3 - 41.06 = 189.2;
//   box center = ink center + 1.1 (LO side-bearing) -> x = 477.6 - 400 = 77.6.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_002_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top),
// badge circle with numeral 2 (file number = printed number; no zero-padding).
drawHouseChrome(pptx, slide, { numeral: 2 });

// --- Title line 1 -----------------------------------------------------------
// ink x 197..756 (center 476.5); render_pre1 calibration: LO ink offset +1.0px
// right of box center and ~1% narrower than the Liberation advance estimate
// (554 vs 560) -> fs 42.5 (L1 560.6), box center 475.5 -> x=75.5, w=800.
slide.addText("Revision of Standard Linear", {
  x: px(75.5), y: px(189.0), w: px(800), h: px(70),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 42.5, bold: true, color: "C00000",
  lineSpacing: 50,
});

// --- Title line 2 -----------------------------------------------------------
// ink x 298..655 (same ink center 476.5); ink offset -0.2px -> box center 476.7
// -> x=76.7; y = L1 top + measured baseline pitch 75.
slide.addText("Regression Model", {
  x: px(76.7), y: px(264.0), w: px(800), h: px(70),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 42.5, bold: true, color: "C00000",
  lineSpacing: 50,
});

// --- Plus-sign annotation artifact (gray, measured 10x11 px) ----------------
// vbar x766..768 y71..81; hbar x763..772 y74..76; fill 808080 (spec color,
// measured core (140,142,139)); no border.
slide.addShape(pptx.ShapeType.rect, {
  x: px(766), y: px(71), w: px(3), h: px(11),
  fill: { color: "808080" },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(763), y: px(74), w: px(10), h: px(3),
  fill: { color: "808080" },
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
