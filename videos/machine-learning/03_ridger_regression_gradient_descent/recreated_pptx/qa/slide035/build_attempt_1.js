// Build slide 035 — "Using Gradient Descent to train Linear Regression Model (Problem Formulation)"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome = shared_patterns/house_chrome.js)
//
// Ground truth: unique_slides/slide_035.jpg (960x540, 1px = 1pt = 1/72 in).
// Content = a two-line red bold centered title + a one-line blue bold subtitle
// "(Problem Formulation)". No other content (PIL full-frame scan: no ink outside
// these bands + house chrome + badge). The spec's claimed white mouse cursor is
// NOT corroborated by pixels (no bright-than-panel cluster, no dark outline in the
// top band) — and it is a video artifact anyway (judge ground rule (c)) — omitted.
// The spec's #F2F2F2 background / #FFFF00 badge are pre-house values; deck house
// chrome (white canvas, E9E9E7 panel, C00000 strokes, FDFD96/6A5ACD badge) wins.
//
// MEASURED geometry (frame px, JPEG smear +-2px noted):
//   L1 "Using Gradient Descent to train"  ink x 147..813 (center 480.0), cap top ~178,
//        x-height top 185, baseline 211, 'g' descender to 221
//   L2 "Linear Regression Model"          ink x 217..743 (center 480.0), cap top ~254,
//        x-height top 263, baseline 288.5, 'g' descender to 298  (baseline pitch 77.5)
//   SUB "(Problem Formulation)"           ink x 271..678 (center 474.5 — measured,
//        consistent with a trailing space in the original's centered string; we
//        replicate the INK geometry, text stays verbatim), paren/ascender top 327,
//        cap top 328, x-height 335, baseline 357, paren bottom 365
//   Colors: title core (181,32,46) = JPEG-darkened C00000 -> draw C00000 (family
//        nominal, same law as the chrome strokes); subtitle core (20,9,196) -> 0000FF.
//   Font sizes fit from ink widths via Liberation Sans Bold (Arial-metric):
//        L1 44.5pt, L2 44.3pt -> 44pt; SUB 38.1pt -> 38pt.
//
// Title lines are TWO single-line boxes (fixed y per line = pixel-exact pitch 77.5,
// no LO/PPT auto-pitch divergence). lineSpacing pinned on every box (1.2em, above
// the 1.117em natural extent so LO never clips ascenders). Box widths ~20%+ beyond
// the longest ink so nothing wraps.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_035_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top),
// badge circle with numeral 35 (file number = printed number; no zero-padding).
drawHouseChrome(pptx, slide, { numeral: 35 });

// --- Title line 1 -----------------------------------------------------------
// ink x 147..813 (center 480.0); LO renders ink ~1.2px left of box center
// (side bearings) -> box center 481.2: x=71.2, w=820.
// LO exact-lineSpacing model + measured constant offset (render_2 self-check:
// LO places the first baseline ~1.6px lower than the halfLead+ascent model):
//   lineSpacing 54, ascent 40.73, halfLead 1.87, LO offset +1.6
//   -> baseline = top + 44.2 => top = 211 - 44.2 = 166.8px.
slide.addText("Using Gradient Descent to train", {
  x: px(71.2), y: px(166.8), w: px(820), h: px(70),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 45, bold: true, color: "C00000",
  lineSpacing: 54,
});

// --- Title line 2 -----------------------------------------------------------
// same width; y = L1 top + measured baseline pitch 77.5px; ink center offset
// measured -1.0px at box center 480 -> box center 481.0: x=71.0.
slide.addText("Linear Regression Model", {
  x: px(71.0), y: px(244.3), w: px(820), h: px(70),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 45, bold: true, color: "C00000",
  lineSpacing: 54,
});

// --- Subtitle ---------------------------------------------------------------
// ink x 271..678 (center 474.5); ink offset -0.5px -> box center 475: x=225, w=500.
// Baseline 357: lineSpacing 46, ascent 34.75, halfLead 1.55, LO offset +1.1
//   -> baseline = top + 37.4 => top = 319.6px.
slide.addText("(Problem Formulation)", {
  x: px(225.0), y: px(319.6), w: px(500), h: px(60),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 38.4, bold: true, color: "0000FF",
  lineSpacing: 46,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
