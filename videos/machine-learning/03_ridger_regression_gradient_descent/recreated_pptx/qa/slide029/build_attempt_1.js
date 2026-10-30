// Build slide 029 — "Example: Obtain Minimum Value of a function using Gradient Descent (GD)"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome = shared_patterns/house_chrome.js)
//
// RESUMED WORKER build (attempt 1): a previous worker died from a harness
// provider timeout ~27 min into its measurement phase; its banked measurements
// (qa/slide029/measure_original_output.txt, measure_rows_output.txt) are
// reused here. No build existed before this one.
//
// Ground truth: unique_slides/slide_029.jpg (960x540, 1px = 1pt = 1/72 in).
// Content = THREE centered lines of bold red title text in the middle band
// + house chrome only (PIL full-frame sensitive-ink scan: bands at the bottom
// stroke row 46, badge 55-93, and the three title lines — nothing else).
// The spec's #F2F2F2 background / #FFFF00 badge / gray border are pre-house
// values; this deck's measured house chrome (white canvas, E9E9E7 panel,
// C00000 L/R/bottom strokes — NO top stroke, FDFD96/6A5ACD badge) wins.
//
// MEASURED geometry (frame px; strict red mask core, JPEG halo +-1-2px noted):
//   L1 "Example: Obtain Minimum Value" ink x 137-824 (w 688, cx 480.5),
//        band y 191-236: cap top 192, baseline ~226 ('p' descender 227-236)
//   L2 "of a function using"            ink x 269-665 (w 397, cx 467.0),
//        band y 269-314: 'f' ascender 269, baseline ~304 ('g' descender 305-314)
//   L3 "Gradient Descent (GD)"          ink x 235-711 (w 477, cx 473.0),
//        band y 347-392: paren tops 347-348, baseline ~382 (paren tails 383-392)
//   Baseline pitch = 78px exactly. Ink core color (181,31,44) = JPEG-darkened
//   C00000 -> draw C00000 (family nominal, same law as the chrome strokes).
//   Font fit (qa/slide029/fit_fonts2_output.txt): Liberation Sans Bold
//   (Arial-metric) 44.65pt fits ALL THREE line widths within 0.3%
//   (687.0/395.8/476.0 vs 688/397/477) — residuals ~1px, no charSpacing.
//   Band heights measure 45-46px only because the ink mask catches the JPEG
//   halo; true glyph extent at 44.65pt is ~42px (fit script cross-check),
//   consistent with cap ~32px + descender ~9.5px + ascender overshoot.
//
// L2/L3 ink centers sit 13px / 7px LEFT of slide center (480): the original's
// centered paragraph evidently carried trailing spaces (space = 12.4px at
// 44.65pt; half-space shifts = 6.2px -> 2 spaces on L2, 1 on L3). We replicate
// the INK geometry by centering each line's box on its measured ink center —
// the drawn text stays verbatim (same approach as sibling slide 035).
//
// Title lines are THREE single-line boxes (fixed y per line = pixel-exact 78px
// pitch, no LO/PPT auto-pitch divergence — explicit-lineSpacing pattern).
// LO exact-lineSpacing model (peer slide 035, Liberation/Arial metrics):
//   baseline = box_top + halfLead + ascent
//   ascent+descent extent = 1.117*S, halfLead = (L - 1.117*S)/2, ascent = 0.905*S
//   with L = lineSpacing = 1.2*S (above natural extent so LO never clips
//   ascenders): at S=44.65, L=53.58 -> baseline = top + 42.28
// MEASURED LO CORRECTION (render_1 closed-loop, probe_baselines_1_output.txt):
//   LO places Liberation Sans Bold's single line ~1.9px BELOW the 0.905*S model
//   on all three lines (baseline deltas +1.72/+2.20/+1.72 vs the original's
//   measured baselines 226/304/382) -> fold +1.9 into the baseline offset.
//   The original's band-TOP (y191) carries ~1.5-2px of JPEG halo above the true
//   ascender tips; the baseline is the halo-robust anchor (selfcheck checks it).
// Box widths ~20% beyond longest ink (wrap-budget law: text wraps at BOX width).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_029_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes
// (NO top stroke — measured law for THIS deck), badge circle numeral 29
// (file number = printed number; no zero-padding).
drawHouseChrome(pptx, slide, { numeral: 29 });

// --- Title: three single-line boxes -----------------------------------------
const S = 44.65;            // Liberation Sans Bold width fit (see header)
const LS = 53.58;           // pinned lineSpacing = 1.2 * S
const LO_CORR = 1.9;        // measured LO baseline drop vs the hhea model
const BASE_OFF = (LS - 1.117 * S) / 2 + 0.905 * S + LO_CORR; // = 44.18

const LINES = [
  { t: "Example: Obtain Minimum Value", base: 226, cx: 480.5, boxW: 820 },
  { t: "of a function using",          base: 304, cx: 467.0, boxW: 500 },
  { t: "Gradient Descent (GD)",         base: 382, cx: 473.0, boxW: 580 },
];

for (const L of LINES) {
  slide.addText(L.t, {
    x: px(L.cx - L.boxW / 2),
    y: px(L.base - BASE_OFF),
    w: px(L.boxW),
    h: px(64),
    align: "center", valign: "top", margin: 0,
    fontFace: "Arial", fontSize: S, bold: true, color: "C00000",
    lineSpacing: LS,
  });
}

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
