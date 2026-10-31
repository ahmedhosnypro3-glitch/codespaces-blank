// Slide 019 rebuild attempt 7 — Training Samples with Labels (Two Classes)
// Frame-vs-spec deviations (measured from unique_slides/slide_019.jpg, 960x540, 1px=1pt):
//  - 5 positive planes / 5x "+1" (pink strip), 6 negative planes / 6x "-1" (green strip)
//    [6 "-1" glyph groups proven by 1px ASCII of strip x498-542]
//  - Planes are SIDE-VIEW PROPELLER aircraft with varied pitch (v2 assets); enemy ones carry a target ring
//  - Input/Test Sample nodes are SOLID RED boxes with white 2-line text (measured 159,0,0)
//  - Model boxes are TAN/gold (measured 245,198,146) with pink step circle at right edge;
//    caption verbatim drift item: [Any value] → (-1 , +1)
//  - "Predicted Class" is an ARROW LABEL (no box); LOSS is a pale circle; red feedback arrow
//    from "Label of Input Sample (+1, -1)" into LOSS; Evaluation ends with blue "(+1, -1)"
//  - Activation panel: light-blue fill, blue border, CENTERED text, pink circular badge with
//    step plot at right-middle
//  - house chrome per root AGENTS.md; title rect drawn BEFORE badge so it cannot cover the numeral
const pptxgen = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";        // house frame
const YELLOW = "FFF9C4";     // badge
const DARK = "333333";
const TXT_RED = "C02828";
const TXT_GREEN = "1E8A3C";
const BOX_RED = "9F0000";    // solid red Input/Test Sample boxes (measured 159,0,0)
const TAN = "F5C693";        // Model boxes (measured 245,198,146)
const PINK = "F7A8C4";       // activation circles
const PINK_STRIP = "F8DBDD";
const GREEN_STRIP = "E4FFEE";
const MAROON = "A01818";
const TEAL = "12694E";
const PEACH = "F8E1C9";      // LOSS circle
const CREAM = "FBFEE3";      // training/eval panels
const ORANGE = "E8A33D";     // panel borders
const BLUE = "20409B";       // activation border/heading
const ACT_FILL = "D6EAF8";   // activation panel fill
const PURPLE = "6A3FB5";
const NAVY = "2E2A6E";
const BLUE_TXT = "0000CC";
const BLACK = "000000";
const WHITE = "FFFFFF";
const GRAY_LINE = "C8C8C8";
const FONT = "Arial";

const ASSETS = path.join(__dirname, "assets");
const PLANES_ENEMY = ["eq_019_plane_enemy_a.png", "eq_019_plane_enemy_b.png", "eq_019_plane_enemy_c.png"];
const PLANES_SAFE = ["eq_019_plane_safe_a.png", "eq_019_plane_safe_b.png", "eq_019_plane_safe_c.png"];
const STEP_PLOT = path.join(ASSETS, "eq_019_step_plot.png");
const STEP_PLOT_S = path.join(ASSETS, "eq_019_step_plot_small.png");
// v2 asset pixel sizes at 600dpi: planes 1092x732, step_plot 696x480, step_plot_small 513x409
const PLANE_W = 1.30, PLANE_H = 1.30 * 732 / 1092;      // ~0.871 in
const STEP_W = 696 / 600, STEP_H = 480 / 600;
const STEP_S_W = 513 / 600, STEP_S_H = 409 / 600;

const P = 1 / 72; // frame px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
// title box (house geometry) drawn BEFORE the badge so its fill cannot cover the numeral
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 11.8, h: 0.62,
  fill: { color: WHITE }, line: { color: BLUE, width: 1.5 },
});
s.addText("Training Samples with Labels (Two Classes)", {
  x: 0.6, y: 0.28, w: 11.8, h: 0.62,
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
  fill: { color: WHITE }, line: { color: GRAY_LINE, width: 1 },
});

// Positive Class (red)
s.addText("Positive Class", {
  x: 75 * P, y: 95 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("\u201CShoot the Enemy\u201D", {
  x: 75 * P, y: 114 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 247 * P, y: 138 * P, w: 0.6, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 80 * P, y: 137 * P, w: 159 * P, h: 368 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});
const ROT_E = [0, 9, -7, 14, -12];
for (let i = 0; i < 5; i++) {
  const cy = 137 + 368 * (i + 0.5) / 5; // 173.8, 247.4, 321, 394.6, 468.2
  s.addImage({
    path: path.join(ASSETS, PLANES_ENEMY[i % 3]),
    x: 80 * P + (159 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H, rotate: ROT_E[i],
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 247 * P, y: 137 * P, w: 42 * P, h: 368 * P,
  fill: { color: PINK_STRIP }, line: { color: TXT_RED, width: 1 },
});
for (let i = 0; i < 5; i++) {
  const cy = 137 + 368 * (i + 0.5) / 5; // same row centers as the planes
  s.addText("+1", {
    x: 247 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
}

// Negative Class (green)
s.addText("Negative Class", {
  x: 330 * P, y: 95 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201CSafe\u201D", {
  x: 330 * P, y: 114 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 498 * P, y: 138 * P, w: 0.6, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 330 * P, y: 136 * P, w: 154 * P, h: 369 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});
const ROT_S = [-6, 0, 11, -14, 7, -3];
for (let i = 0; i < 6; i++) {
  const cy = 136 + 369 * (i + 0.5) / 6; // 166.75 ... 474.25
  s.addImage({
    path: path.join(ASSETS, PLANES_SAFE[i % 3]),
    x: 330 * P + (154 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H, rotate: ROT_S[i],
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 498 * P, y: 136 * P, w: 42 * P, h: 369 * P,
  fill: { color: GREEN_STRIP }, line: { color: TXT_GREEN, width: 1 },
});
for (let i = 0; i < 6; i++) {
  const cy = 136 + 369 * (i + 0.5) / 6; // same row centers as the planes
  s.addText("-1", {
    x: 498 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: TEAL, fontFace: FONT, margin: 0,
  });
}

// ---- Activation Function panel x660..944 y88..203: light blue, centered text, pink badge ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 88 * P, w: 284 * P, h: 115 * P,
  fill: { color: ACT_FILL }, line: { color: BLUE, width: 1.5 },
});
const actCx = (665 + 880) / 2 * P, actW = (880 - 665) * P;
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
// pink circular badge with step plot, fully inside panel (panel x660..944 y88..203)
s.addShape(pptx.shapes.OVAL, {
  x: 882 * P, y: 110 * P, w: 56 * P, h: 56 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({
  path: STEP_PLOT_S,
  x: 892 * P, y: 122 * P, w: STEP_S_W * 0.62, h: STEP_S_H * 0.62,
});

// ---- Training panel x660..944 y240..322 ----
s.addText("Training", {
  x: 700 * P, y: 219 * P, w: 2.0, h: 0.28,
  align: "center", fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 660 * P, y: 240 * P, w: 284 * P, h: 82 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ty = 252 * P; // flow row top
// Input Sample: solid red box, white 2-line text
s.addShape(pptx.shapes.RECTANGLE, {
  x: 666 * P, y: ty, w: 60 * P, h: 50 * P,
  fill: { color: BOX_RED },
});
s.addText("Input\nSample", {
  x: 666 * P, y: ty, w: 60 * P, h: 50 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 728 * P, y: ty + 17 * P, w: 12 * P, h: 16 * P, fill: { color: BOX_RED } });
// Model: tan box, dark text + verbatim caption, pink step circle at right edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 742 * P, y: ty - 4 * P, w: 98 * P, h: 58 * P,
  fill: { color: TAN }, line: { color: BOX_RED, width: 1 },
});
s.addText("Model", {
  x: 742 * P, y: ty + 2 * P, w: 98 * P, h: 18 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BOX_RED, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 742 * P, y: ty + 22 * P, w: 98 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 832 * P, y: ty + 12 * P, w: 20 * P, h: 20 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({ path: STEP_PLOT_S, x: 835 * P, y: ty + 15 * P, w: STEP_S_W * 0.42, h: STEP_S_H * 0.42 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 854 * P, y: ty + 17 * P, w: 10 * P, h: 16 * P, fill: { color: BOX_RED } });
// "Predicted Class" as an arrow label above arrow2
s.addText("Predicted Class", {
  x: 842 * P, y: ty - 2 * P, w: 46 * P, h: 12 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
// LOSS circle (pale peach)
s.addShape(pptx.shapes.OVAL, {
  x: 868 * P, y: ty + 10 * P, w: 30 * P, h: 30 * P,
  fill: { color: PEACH }, line: { color: BOX_RED, width: 1 },
});
s.addText("LOSS", {
  x: 868 * P, y: ty + 10 * P, w: 30 * P, h: 30 * P,
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// red feedback arrow into LOSS from the right
s.addShape(pptx.shapes.LEFT_ARROW, { x: 900 * P, y: ty + 15 * P, w: 14 * P, h: 20 * P, fill: { color: BOX_RED } });
// "Label of Input Sample" + "(+1, -1)" at the right, below the feedback arrow
s.addText("Label of Input Sample", {
  x: 898 * P, y: ty + 38 * P, w: 46 * P, h: 12 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, -1)", {
  x: 898 * P, y: ty + 50 * P, w: 46 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});
// upward connector from the label block into the LOSS circle
s.addShape(pptx.shapes.UP_ARROW, { x: 878 * P, y: ty + 41 * P, w: 12 * P, h: 12 * P, fill: { color: BOX_RED } });

// ---- Evaluation panel x660..944 y380..495 ----
s.addText("Evaluation", {
  x: 700 * P, y: 360 * P, w: 2.0, h: 0.28,
  align: "center", fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 660 * P, y: 380 * P, w: 284 * P, h: 112 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ey = 420 * P;
s.addShape(pptx.shapes.RECTANGLE, {
  x: 666 * P, y: ey, w: 60 * P, h: 50 * P,
  fill: { color: BOX_RED },
});
s.addText("Test\nSample", {
  x: 666 * P, y: ey, w: 60 * P, h: 50 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 728 * P, y: ey + 17 * P, w: 12 * P, h: 16 * P, fill: { color: BOX_RED } });
s.addShape(pptx.shapes.RECTANGLE, {
  x: 742 * P, y: ey - 4 * P, w: 98 * P, h: 58 * P,
  fill: { color: TAN }, line: { color: BOX_RED, width: 1 },
});
s.addText("Model", {
  x: 742 * P, y: ey + 2 * P, w: 98 * P, h: 18 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BOX_RED, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 742 * P, y: ey + 22 * P, w: 98 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 832 * P, y: ey + 12 * P, w: 20 * P, h: 20 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({ path: STEP_PLOT_S, x: 835 * P, y: ey + 15 * P, w: STEP_S_W * 0.42, h: STEP_S_H * 0.42 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 854 * P, y: ey + 17 * P, w: 10 * P, h: 16 * P, fill: { color: BOX_RED } });
s.addText("Predicted Class", {
  x: 842 * P, y: ey - 2 * P, w: 46 * P, h: 12 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
// blue "(+1, -1)" at the right end (no LOSS in evaluation)
s.addText("(+1, -1)", {
  x: 872 * P, y: ey + 8 * P, w: 66 * P, h: 34 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_019_recreated.pptx"
}).then(() => console.log("done"));
