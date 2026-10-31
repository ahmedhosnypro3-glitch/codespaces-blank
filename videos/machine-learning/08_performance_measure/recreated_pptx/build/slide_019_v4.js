// Slide 019 rebuild v4 — geometry re-measured from unique_slides/slide_019.jpg (960x540, 1px=1pt)
// vs v3: right-column panels are x660..902 (w242, not 944); activation y92..207; training y240..322;
// evaluation y382..497; samples panel x70..556 y91..509 fill #E7E9E6; pos box x84..238; +1 strip
// x250..288; neg box x335..482; -1 strip x501..539; +1 centers [195,257,319,380,441]; -1 centers
// [176,238,283,336,398,460]; activation pink circle x809 y100 d59 fill #F9E1F9; step circles paler.
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
const BOX_RED = "9F0000";    // solid red Input/Test Sample boxes (measured 159,0,0)
const TAN = "F5C692";        // Model boxes (measured 245,198,146)
const PINK = "F9E1F9";       // step circles (measured 249,225,249)
const PINK_STRIP = "F8DBDD"; // measured 248,219,221
const GREEN_STRIP = "E4FFEE";// measured 228,255,238
const MAROON = "A01818";
const TEAL = "12694E";
const PEACH = "F8E1C9";
const CREAM = "FBFEE3";      // measured 251,254,227
const ORANGE = "E8A33D";
const BLUE = "20409B";
const ACT_FILL = "F0FFFC";   // measured 240,255,252
const PURPLE = "6A3FB5";
const NAVY = "2E2A6E";
const BLUE_TXT = "0000CC";
const BLACK = "000000";
const WHITE = "FFFFFF";
const GRAY_LINE = "C8C8C8";
const PANEL_GRAY = "E7E9E6"; // measured 231,233,230
const FONT = "Arial";

const ASSETS = path.join(__dirname, "assets");
const PLANES_ENEMY = ["eq_019_plane_enemy_a.png", "eq_019_plane_enemy_b.png", "eq_019_plane_enemy_c.png"];
const PLANES_SAFE = ["eq_019_plane_safe_a.png", "eq_019_plane_safe_b.png", "eq_019_plane_safe_c.png"];
const STEP_PLOT_S = path.join(ASSETS, "eq_019_step_plot_small.png");
// v2 assets at 600dpi: planes 1092x732, step_plot_small 513x409
const PLANE_W = 1.30, PLANE_H = 1.30 * 732 / 1092;
const STEP_S_W = 513 / 600, STEP_S_H = 409 / 600;

const P = 1 / 72; // frame px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome (root AGENTS.md, overrides everything) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
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

// ---- samples panel x70..556 y91..509 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 70 * P, y: 91 * P, w: 486 * P, h: 418 * P,
  fill: { color: PANEL_GRAY }, line: { color: GRAY_LINE, width: 1 },
});

// Positive Class (red) — 5 enemy planes, 5x "+1"
s.addText("Positive Class", {
  x: 113 * P, y: 96 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("\u201CShoot the Enemy\u201D", {
  x: 113 * P, y: 116 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 250 * P, y: 140 * P, w: 38 * P, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 84 * P, y: 137 * P, w: 154 * P, h: 368 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});
for (let i = 0; i < 5; i++) {
  const cy = 137 + 368 * (i + 0.5) / 5;
  s.addImage({
    path: path.join(ASSETS, PLANES_ENEMY[i % 3]),
    x: 84 * P + (154 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H,
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 250 * P, y: 161 * P, w: 38 * P, h: 332 * P,
  fill: { color: PINK_STRIP }, line: { color: TXT_RED, width: 1 },
});
const POS_CY = [195, 257, 319, 380, 441]; // measured +1 text centers
for (const cy of POS_CY) {
  s.addText("+1", {
    x: 250 * P, y: (cy - 9) * P, w: 38 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
}

// Negative Class (green) — 6 safe planes, 6x "-1"
s.addText("Negative Class", {
  x: 353 * P, y: 96 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201CSafe\u201D", {
  x: 353 * P, y: 116 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 501 * P, y: 140 * P, w: 38 * P, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 335 * P, y: 136 * P, w: 147 * P, h: 369 * P,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});
for (let i = 0; i < 6; i++) {
  const cy = 136 + 369 * (i + 0.5) / 6;
  s.addImage({
    path: path.join(ASSETS, PLANES_SAFE[i % 3]),
    x: 335 * P + (147 * P - PLANE_W) / 2, y: cy * P - PLANE_H / 2,
    w: PLANE_W, h: PLANE_H,
  });
}
s.addShape(pptx.shapes.RECTANGLE, {
  x: 501 * P, y: 161 * P, w: 38 * P, h: 337 * P,
  fill: { color: GREEN_STRIP }, line: { color: TXT_GREEN, width: 1 },
});
const NEG_CY = [176, 238, 283, 336, 398, 460]; // measured -1 text centers
for (const cy of NEG_CY) {
  s.addText("-1", {
    x: 501 * P, y: (cy - 9) * P, w: 38 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: TEAL, fontFace: FONT, margin: 0,
  });
}

// ---- Activation Function panel x660..902 y92..207 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 92 * P, w: 242 * P, h: 115 * P,
  fill: { color: ACT_FILL }, line: { color: BLUE, width: 1.5 },
});
s.addText("Activation Function", {
  x: 666 * P, y: 98 * P, w: 140 * P, h: 18 * P,
  align: "left", valign: "middle",
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Bi-polar step (-1 , +1)", {
  x: 666 * P, y: 120 * P, w: 140 * P, h: 18 * P,
  align: "left", valign: "middle",
  fontSize: 11, color: PURPLE, fontFace: FONT, margin: 0,
});
s.addText("Threshold at \u201Czero\u201D", {
  x: 666 * P, y: 142 * P, w: 140 * P, h: 18 * P,
  align: "left", valign: "middle",
  fontSize: 11, color: TXT_RED, fontFace: FONT, margin: 0,
});
// pink circular badge with step plot at right, fully inside the panel
s.addShape(pptx.shapes.OVAL, {
  x: 809 * P, y: 100 * P, w: 59 * P, h: 59 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({
  path: STEP_PLOT_S,
  x: 817 * P, y: 110 * P, w: STEP_S_W * 0.7, h: STEP_S_H * 0.7,
});

// ---- Training: heading + panel x660..902 y240..322 ----
s.addText("Training", {
  x: 725 * P, y: 226 * P, w: 110 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 240 * P, w: 242 * P, h: 82 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ty = 248 * P;
// Input Sample: solid red box, white 2-line text
s.addShape(pptx.shapes.RECTANGLE, {
  x: 664 * P, y: ty, w: 68 * P, h: 56 * P,
  fill: { color: BOX_RED },
});
s.addText("Input\nSample", {
  x: 664 * P, y: ty, w: 68 * P, h: 56 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 734 * P, y: ty + 21 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
// Model: tan box + verbatim drift caption; ONE pale step circle on its right edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 746 * P, y: ty - 2 * P, w: 104 * P, h: 58 * P,
  fill: { color: TAN }, line: { color: BOX_RED, width: 1 },
});
s.addText("Model", {
  x: 746 * P, y: ty + 2 * P, w: 104 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BOX_RED, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 746 * P, y: ty + 20 * P, w: 104 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 842 * P, y: ty + 18 * P, w: 18 * P, h: 18 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({ path: STEP_PLOT_S, x: 844.5 * P, y: ty + 20.5 * P, w: STEP_S_W * 0.22, h: STEP_S_H * 0.22 });
// arrow to Predicted Class (label above the arrow)
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 854 * P, y: ty + 21 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
s.addText("Predicted Class", {
  x: 846 * P, y: ty - 2 * P, w: 44 * P, h: 10 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
// LOSS circle (pale peach)
s.addShape(pptx.shapes.OVAL, {
  x: 868 * P, y: ty + 8 * P, w: 28 * P, h: 28 * P,
  fill: { color: PEACH }, line: { color: BOX_RED, width: 1 },
});
s.addText("LOSS", {
  x: 868 * P, y: ty + 8 * P, w: 28 * P, h: 28 * P,
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// loss-feed connector: UP_ARROW from the label block into LOSS
s.addShape(pptx.shapes.UP_ARROW, { x: 879 * P, y: ty + 38 * P, w: 8 * P, h: 8 * P, fill: { color: BOX_RED } });
s.addText("Label of Input Sample", {
  x: 850 * P, y: ty + 46 * P, w: 52 * P, h: 10 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, -1)", {
  x: 850 * P, y: ty + 56 * P, w: 52 * P, h: 10 * P,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

// ---- Evaluation: heading + panel x660..902 y382..497 ----
s.addText("Evaluation", {
  x: 700 * P, y: 354 * P, w: 100 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 382 * P, w: 242 * P, h: 115 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ey = 424 * P;
s.addShape(pptx.shapes.RECTANGLE, {
  x: 664 * P, y: ey, w: 68 * P, h: 52 * P,
  fill: { color: BOX_RED },
});
s.addText("Test\nSample", {
  x: 664 * P, y: ey, w: 68 * P, h: 52 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 734 * P, y: ey + 19 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
s.addShape(pptx.shapes.RECTANGLE, {
  x: 746 * P, y: ey - 2 * P, w: 104 * P, h: 58 * P,
  fill: { color: TAN }, line: { color: BOX_RED, width: 1 },
});
s.addText("Model", {
  x: 746 * P, y: ey + 2 * P, w: 104 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BOX_RED, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 746 * P, y: ey + 20 * P, w: 104 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 842 * P, y: ey + 18 * P, w: 18 * P, h: 18 * P,
  fill: { color: PINK }, line: { color: PINK, width: 0.5 },
});
s.addImage({ path: STEP_PLOT_S, x: 844.5 * P, y: ey + 20.5 * P, w: STEP_S_W * 0.22, h: STEP_S_H * 0.22 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 854 * P, y: ey + 19 * P, w: 10 * P, h: 14 * P, fill: { color: BOX_RED } });
s.addText("Predicted Class", {
  x: 846 * P, y: ey - 2 * P, w: 44 * P, h: 10 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
// blue "(+1, -1)" at the right end (no LOSS in evaluation)
s.addText("(+1, -1)", {
  x: 870 * P, y: ey + 12 * P, w: 30 * P, h: 24 * P,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_019_recreated.pptx"
}).then(() => console.log("done"));
