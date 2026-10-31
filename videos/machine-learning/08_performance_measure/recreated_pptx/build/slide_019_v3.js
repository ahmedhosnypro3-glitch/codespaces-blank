// Slide 019 rebuild v3 — Training Samples with Labels (Two Classes)
// Base: build_attempt_7.js measured geometry (960x540 frame, 1px = 1pt = 1/72 in).
// Fixes vs attempt 7 judge FAIL:
//  - activation step badge fully contained inside the Activation panel (margin on all sides)
//  - exactly ONE pink step circle per Model box (overlapping its right edge, per reanalysis),
//    no stray circle on the Model->LOSS arrow
//  - Training loss-feed connector: LOSS <- LEFT_ARROW <- "Label of Input Sample (+1, -1)" text block
// Drift item from pool_run/spec_gaps.md baked in: "[Any value] → (-1 , +1)" caption in BOTH Model boxes.
const pptxgen = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const TXT_RED = "C02828";
const TXT_GREEN = "1E8A3C";
const BOX_RED = "9F0000";
const TAN = "F5C693";
const PINK = "F7A8C4";
const PINK_STRIP = "F8DBDD";
const GREEN_STRIP = "E4FFEE";
const MAROON = "A01818";
const TEAL = "12694E";
const PEACH = "F8E1C9";
const CREAM = "FBFEE3";
const ORANGE = "E8A33D";
const BLUE = "20409B";
const ACT_FILL = "D6EAF8";
const PURPLE = "6A3FB5";
const NAVY = "2E2A6E";
const BLUE_TXT = "0000CC";
const BLACK = "000000";
const WHITE = "FFFFFF";
const GRAY_LINE = "C8C8C8";
const PANEL_GRAY = "E0E0E0";
const FONT = "Arial";

const ASSETS = path.join(__dirname, "assets");
const PLANES_ENEMY = ["eq_019_plane_enemy_a.png", "eq_019_plane_enemy_b.png", "eq_019_plane_enemy_c.png"];
const PLANES_SAFE = ["eq_019_plane_safe_a.png", "eq_019_plane_safe_b.png", "eq_019_plane_safe_c.png"];
const STEP_PLOT_S = path.join(ASSETS, "eq_019_step_plot_small.png");
// v2 assets at 600dpi: planes 1092x732, step_plot_small 513x409
const PLANE_W = 1.30, PLANE_H = 1.30 * 732 / 1092; // ~0.871 in
const STEP_S_W = 513 / 600, STEP_S_H = 409 / 600;

const P = 1 / 72; // frame px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome (root AGENTS.md, overrides everything) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
// title: house text box x0.6 y0.28 w12.13 centered; original's white/blue-bordered
// banner drawn slightly narrower (ends x12.4) so it never reaches the badge at x12.48
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 11.8, h: 0.62,
  fill: { color: WHITE }, line: { color: BLUE, width: 1.5 },
});
s.addText("Training Samples with Labels (Two Classes)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 22, bold: true, color: NAVY, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("19", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// ---- samples panel x69..557 y92..509 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 69 * P, y: 92 * P, w: 488 * P, h: 417 * P,
  fill: { color: PANEL_GRAY }, line: { color: GRAY_LINE, width: 1 },
});

// Positive Class (red) — 5 enemy planes, 5x "+1"
s.addText("Positive Class", {
  x: 75 * P, y: 95 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("\u201CShoot the Enemy\u201D", {
  x: 75 * P, y: 114 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 247 * P, y: 138 * P, w: 42 * P, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 80 * P, y: 137 * P, w: 159 * P, h: 368 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});
for (let i = 0; i < 5; i++) {
  const cy = 137 + 368 * (i + 0.5) / 5;
  s.addImage({
    path: path.join(ASSETS, PLANES_ENEMY[i % 3]),
    x: 80 * P + (159 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H,
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 247 * P, y: 161 * P, w: 42 * P, h: 332 * P,
  fill: { color: PINK_STRIP }, line: { color: TXT_RED, width: 1 },
});
for (let i = 0; i < 5; i++) {
  const cy = 161 + 332 * (i + 0.5) / 5;
  s.addText("+1", {
    x: 247 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
}

// Negative Class (green) — 6 safe planes, 6x "-1"
s.addText("Negative Class", {
  x: 330 * P, y: 95 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201CSafe\u201D", {
  x: 330 * P, y: 114 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 498 * P, y: 138 * P, w: 42 * P, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 330 * P, y: 136 * P, w: 154 * P, h: 369 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});
for (let i = 0; i < 6; i++) {
  const cy = 136 + 369 * (i + 0.5) / 6;
  s.addImage({
    path: path.join(ASSETS, PLANES_SAFE[i % 3]),
    x: 330 * P + (154 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H,
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 498 * P, y: 161 * P, w: 42 * P, h: 338 * P,
  fill: { color: GREEN_STRIP }, line: { color: TXT_GREEN, width: 1 },
});
for (let i = 0; i < 6; i++) {
  const cy = 161 + 338 * (i + 0.5) / 6;
  s.addText("-1", {
    x: 498 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: TEAL, fontFace: FONT, margin: 0,
  });
}

// ---- Activation Function panel x660..944 y88..203 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 88 * P, w: 284 * P, h: 115 * P,
  fill: { color: ACT_FILL }, line: { color: BLUE, width: 1.5 },
});
const actCx = (665 + 878) / 2 * P, actW = (878 - 665) * P;
s.addText("Activation Function", {
  x: actCx - actW / 2, y: 96 * P, w: actW, h: 22 * P,
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Bi-polar step (-1 , +1)", {
  x: actCx - actW / 2, y: 122 * P, w: actW, h: 20 * P,
  align: "center", valign: "middle",
  fontSize: 11, color: PURPLE, fontFace: FONT, margin: 0,
});
s.addText("Threshold at \u201Czero\u201D", {
  x: actCx - actW / 2, y: 146 * P, w: actW, h: 20 * P,
  align: "center", valign: "middle",
  fontSize: 11, color: TXT_RED, fontFace: FONT, margin: 0,
});
// pink circular badge with step plot, fully inside panel (panel y88..203, x..944)
s.addShape(pptx.shapes.OVAL, {
  x: 888 * P, y: 124 * P, w: 40 * P, h: 40 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({
  path: STEP_PLOT_S,
  x: 894 * P, y: 130 * P, w: STEP_S_W * 0.5, h: STEP_S_H * 0.5,
});

// ---- Training panel x660..944 y240..322, heading above ----
s.addText("Training", {
  x: 700 * P, y: 224 * P, w: 2.0, h: 0.26,
  align: "center", fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 240 * P, w: 284 * P, h: 82 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ty = 252 * P; // flow row top
// Input Sample: solid red box, white 2-line text
s.addShape(pptx.shapes.RECTANGLE, {
  x: 664 * P, y: ty, w: 56 * P, h: 46 * P,
  fill: { color: BOX_RED },
});
s.addText("Input\nSample", {
  x: 664 * P, y: ty, w: 56 * P, h: 46 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 722 * P, y: ty + 15 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
// Model: tan box with verbatim drift caption; ONE pink step circle on its right edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 734 * P, y: ty - 4 * P, w: 92 * P, h: 54 * P,
  fill: { color: TAN }, line: { color: BOX_RED, width: 1 },
});
s.addText("Model", {
  x: 734 * P, y: ty + 2 * P, w: 92 * P, h: 18 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BOX_RED, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 734 * P, y: ty + 22 * P, w: 92 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 818 * P, y: ty + 16 * P, w: 18 * P, h: 18 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({ path: STEP_PLOT_S, x: 821 * P, y: ty + 19 * P, w: STEP_S_W * 0.38, h: STEP_S_H * 0.38 });
// arrow to Predicted Class (label above the arrow)
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 838 * P, y: ty + 15 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
s.addText("Predicted Class", {
  x: 830 * P, y: ty + 1 * P, w: 44 * P, h: 12 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
// LOSS circle (pale peach)
s.addShape(pptx.shapes.OVAL, {
  x: 852 * P, y: ty + 8 * P, w: 30 * P, h: 30 * P,
  fill: { color: PEACH }, line: { color: BOX_RED, width: 1 },
});
s.addText("LOSS", {
  x: 852 * P, y: ty + 8 * P, w: 30 * P, h: 30 * P,
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// loss-feed connector: label block at far right, LEFT_ARROW feeding into LOSS
s.addShape(pptx.shapes.LEFT_ARROW, { x: 886 * P, y: ty + 15 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
s.addText("Label of Input Sample", {
  x: 898 * P, y: ty + 2 * P, w: 44 * P, h: 20 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0, lineSpacing: 8,
});
s.addText("(+1, -1)", {
  x: 898 * P, y: ty + 24 * P, w: 44 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

// ---- Evaluation panel x660..944 y380..492, heading above ----
s.addText("Evaluation", {
  x: 700 * P, y: 368 * P, w: 2.0, h: 0.26,
  align: "center", fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 380 * P, w: 284 * P, h: 112 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ey = 420 * P;
s.addShape(pptx.shapes.RECTANGLE, {
  x: 664 * P, y: ey, w: 56 * P, h: 46 * P,
  fill: { color: BOX_RED },
});
s.addText("Test\nSample", {
  x: 664 * P, y: ey, w: 56 * P, h: 46 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 722 * P, y: ey + 15 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
s.addShape(pptx.shapes.RECTANGLE, {
  x: 734 * P, y: ey - 4 * P, w: 92 * P, h: 54 * P,
  fill: { color: TAN }, line: { color: BOX_RED, width: 1 },
});
s.addText("Model", {
  x: 734 * P, y: ey + 2 * P, w: 92 * P, h: 18 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BOX_RED, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 734 * P, y: ey + 22 * P, w: 92 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 818 * P, y: ey + 16 * P, w: 18 * P, h: 18 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({ path: STEP_PLOT_S, x: 821 * P, y: ey + 19 * P, w: STEP_S_W * 0.38, h: STEP_S_H * 0.38 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 838 * P, y: ey + 15 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
s.addText("Predicted Class", {
  x: 830 * P, y: ey + 1 * P, w: 44 * P, h: 12 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
// blue "(+1, -1)" at the right end (no LOSS in evaluation)
s.addText("(+1, -1)", {
  x: 856 * P, y: ey + 8 * P, w: 66 * P, h: 30 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_019_recreated.pptx"
}).then(() => console.log("done"));
