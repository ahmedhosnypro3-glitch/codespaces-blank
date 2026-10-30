// Build script for slide 038 — "Gradient Descent (GD) vs Stochastic Gradient Descent (SGD)"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (lecture 03)
//
// GEOMETRY LAW: measured from unique_slides/slide_038.jpg with PIL (2026-10-19,
// measurement scripts banked in scratch/tmp/slide038/ + self-check banked in qa/slide038/).
// Frame 960x540, 1px = 1pt = 1/72in. Every value below is a measured frame pixel.
//
// MEASURED TARGETS (frame px):
//   L1 "Gradient Descent (GD)": red ink 230..597, blue ink 625..717 (ink center 473.5),
//        red cap band y177..210 -> cap top 178, baseline ~210 (34px band incl. ~1.5px JPEG
//        spread; true cap 31.9px at 44.5pt). Descent->" (GD)" gap ~27px = TWO spaces
//        (one space renders ~16.3px ink-gap at 44.5pt).
//   L2 "vs": ink 444..490, center 467 (6.5px LEFT of the other lines' 473.5 — consistent
//        with a trailing space in the original's centered block; reproduced as a centered
//        box at 467). x-band y264..288 -> baseline ~288.
//   L3 "Stochastic Gradient Descent (SGD)": red ink 96..713, blue 730..851 (center 473.5),
//        cap band y333..366 -> baseline ~366. Stochastic->"Gradient" gap ~27px = TWO spaces;
//        other gaps single spaces (~15.5-16px measured).
//   Baseline pitch: 78px exactly (210 -> 288 -> 366).
//   Font fit (empirical, PIL + real Arial TTF): Arial BOLD 44.5pt — word ink widths all
//        within 2px of measured (Gradient 180.2/181, Descent 169.3/171, (GD) 92/93,
//        vs 47.0/47, (SGD) 121.6/122, Stochastic 221.6/222). Cap 31.9 vs ~32.5 true.
//        Spec's "'vs' slightly smaller" is REFUTED by measurement: same 44.5pt.
//   Colors: red text core measured (174,20,36) = JPEG-darkened C00000 family nominal;
//        blue core (6,0,192) = JPEG-darkened 0000FF. Draw nominal C00000 / 0000FF.
//
// DEVIATIONS FROM SPEC (law hierarchy: deck AGENTS.md + judge_protocol_03.md + runbook
// OVERRIDE the analysis spec; frame measurement overrides intuition):
//   1. House chrome (this deck: white canvas, E9E9E7 panel x54..903 y45..540, red C00000
//      1pt strokes LEFT/RIGHT/BOTTOM only — NO TOP STROKE — badge FDFD96/6A5ACD ring,
//      numeral 38) is drawn by shared_patterns/house_chrome.js per deck AGENTS.md. The
//      spec's "#F5F5F5 background", "#808080 thin border frame", "#FFFF00 badge with black
//      outline" are the vision model's misread of this chrome at 960px — house law wins.
//   2. The mouse-cursor smudge at (~684..697, ~373..387) px (9 dark px total — a video
//      screen-capture artifact) is OMITTED per 17_worker_instructions.md ("Mouse cursors
//      or video-capture artifacts in the original must NOT be recreated") and frozen judge
//      ground rule (c) ("CORRECTLY omitted"). The spec's recreation_brief step 7 ("overlay
//      the cursor") is overridden by the higher law.
//   3. Spec's ~54pt/~44pt title estimates replaced by the measured 44.5pt for ALL three
//      lines (empirical font fit above).
//
// Single version deliverable: recreated_pptx/slide_038_recreated.pptx (no suffixes).

const pptxgenpkg = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const PX = 1 / 72; // frame px -> inches
const RED = "C00000";   // no '#' in pptxgenjs hex
const BLUE = "0000FF";
const FONT = "Arial";
const SIZE = 44.5;      // measured fit

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

const slide = pptx.addSlide();

// House chrome: white canvas, gray panel, red L/R/bottom strokes (NO top), badge "38"
drawHouseChrome(pptx, slide, { numeral: 38 });

// --- three-line centered title block -------------------------------------------------
// valign top; baseline_offset = distance from box top to the text baseline.
// 41.0 was the metric estimate (ascent 0.905em + lineGap/2 ~0.016em = 0.921em =>
// 41.0px at 44.5pt); the 150dpi render measured the true LO offset ~3.4px larger
// (selfcheck_attempt_1: every line's ink y0 +4.8..+5.0 / y1 +1.8..+2.4 low, i.e.
// centroid +3.4px low), so the closed-loop-corrected value is 44.4.
//
// ATTEMPT-2 DELTAS (selfcheck_attempt_1.out, frame px, render - orig):
//   L1 x0 +0.3 x1 -3.2 y0 +5.0 y1 +1.8 | L2 x0 -1.7 x1 -2.6 y0 +4.8 y1 +2.4
//   L3 x0 +0.4 x1 -2.8 y0 +5.0 y1 +1.8
// Fix = pure translation per line (font size/widths already fit; the residual
// x/y asymmetry ~1.5-1.75px/side is the original's JPEG ink spread, expected):
//   y: shift ALL lines UP 3.4px  (BASELINE_OFFSET 41.0 -> 44.4; pitch 78 kept)
//   x: shift RIGHT by each line's ink-center delta: L1 +1.45 (center 473.5 ->
//      474.95), L2 +2.15 (467 -> 469.15), L3 +1.2 (473.5 -> 474.7).
// Predicted post-fix residuals (all < 2.0 frame-px tol): L1 x +/-1.75 y +/-1.6;
// L2 x +/-0.45 y +1.4/-1.0; L3 x +/-1.6 y +/-1.6.
const BASELINE_OFFSET = 44.4; // frame px, box-top -> baseline (LO-measured)
function titleLine(yBaselinePx, centerPx, runs) {
  const w = 800 * PX; // 800px box, no wrap risk (longest advance 774px)
  return {
    x: (centerPx - 400) * PX, y: (yBaselinePx - BASELINE_OFFSET) * PX,
    w, h: 70 * PX,
    align: "center", valign: "top", margin: 0,
    bold: true, fontSize: SIZE, fontFace: FONT,
    runs,
  };
}

// L1: "Gradient Descent" red + "  (GD)" blue (two spaces = measured 27px gap)
slide.addText(
  [
    { text: "Gradient Descent", options: { color: RED } },
    { text: "  (GD)", options: { color: BLUE } },
  ],
  titleLine(210, 474.95)
);

// L2: "vs" red — same 44.5pt (spec's "slightly smaller" refuted by measurement);
// ink center 467 per the original's centered-block-with-trailing-space rendering.
slide.addText(
  [{ text: "vs", options: { color: RED } }],
  titleLine(288, 469.15)
);

// L3: "Stochastic  Gradient Descent" red (two spaces after Stochastic = measured 27px gap)
// + " (SGD)" blue (single space = measured 15.5px gap)
slide.addText(
  [
    { text: "Stochastic  Gradient Descent", options: { color: RED } },
    { text: " (SGD)", options: { color: BLUE } },
  ],
  titleLine(366, 474.7)
);

pptx
  .writeFile({
    fileName:
      "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_038_recreated.pptx",
  })
  .then(() => console.log("slide_038_recreated.pptx written"));
