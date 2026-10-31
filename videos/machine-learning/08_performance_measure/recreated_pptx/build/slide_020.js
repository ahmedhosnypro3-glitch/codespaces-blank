const pptxgen = require("pptxgenjs");

// Slide 20 — Training Samples with Labels (Two Classes)
// Geometry measured from unique_slides/slide_020.jpg (960x540, 1px = 1pt @72dpi -> inches = px/72).
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const ASSET = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const FONT = "Arial";

const BLUE = "0000FF";
const BLUE_B = "0000CC";
const RED_T = "C00000";
const GREEN_T = "008000";
const DARKRED = "9C0006";
const PEACH = "FFC89A";
const CREAM = "F8F8E0";
const LEFTPANEL = "FFFFFF";
const PANELB = "B0C8E0";
const PINK = "F8D8D8";
const MINT = "E0F8E8";
const ORANGE_L = "FF8000";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome (root AGENTS.md 2026-10-09) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("20", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Training Samples with Labels (Two Classes)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: BLUE, fontFace: FONT, margin: 0,
  line: { color: BLUE, width: 1.25 },
});

// ---- left enclosing panel: x 63..555 px -> 0.88..7.71 in, y 92..507 -> 1.28..7.04 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.88, y: 1.28, w: 6.83, h: 5.76,
  fill: { color: LEFTPANEL }, line: { color: PANELB, width: 1 },
});

// ---- class headers ----
s.addText("Positive Class", {
  x: 1.55, y: 1.36, w: 1.5, h: 0.22, align: "left", valign: "top",
  fontSize: 14, bold: true, color: RED_T, fontFace: FONT, margin: 0,
});
s.addText('"Shoot the Enemy"', {
  x: 1.68, y: 1.62, w: 1.8, h: 0.2, align: "left", valign: "top",
  fontSize: 11, bold: true, color: RED_T, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 3.42, y: 1.62, w: 0.55, h: 0.2, align: "center", valign: "top",
  fontSize: 11, bold: true, color: RED_T, fontFace: FONT, margin: 0,
});
s.addText("Negative Class", {
  x: 4.92, y: 1.36, w: 1.6, h: 0.22, align: "left", valign: "top",
  fontSize: 14, bold: true, color: GREEN_T, fontFace: FONT, margin: 0,
});
s.addText('"Safe"', {
  x: 5.47, y: 1.62, w: 0.9, h: 0.2, align: "left", valign: "top",
  fontSize: 11, bold: true, color: GREEN_T, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 6.92, y: 1.62, w: 0.55, h: 0.2, align: "center", valign: "top",
  fontSize: 11, bold: true, color: GREEN_T, fontFace: FONT, margin: 0,
});

// ---- airplane boxes: red-bordered (both), x 82..236 / 332..481 px, y 138..503 px ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.14, y: 1.92, w: 2.14, h: 5.07,
  fill: { color: "FFFFFF" }, line: { color: "730000", width: 1.5 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.61, y: 1.92, w: 2.07, h: 5.07,
  fill: { color: "FFFFFF" }, line: { color: "730000", width: 1.5 },
});

// ---- five varied aircraft sketches per class (measured widths 1.28..1.88 in) ----
const ROW_Y = [2.70, 3.56, 4.42, 5.28, 6.14];       // row centres, 62px apart in the original
const POS_W = [1.30, 1.85, 1.35, 1.35, 1.35];
const NEG_W = [1.35, 1.10, 1.33, 1.83, 1.33];
const ENEMY = ["eq_020_plane_enemy_a.png", "eq_020_plane_enemy_b.png", "eq_020_plane_enemy_c.png"];
const SAFE = ["eq_020_plane_safe_a.png", "eq_020_plane_safe_b.png", "eq_020_plane_safe_c.png"];
const ASPECT = 2.6;
for (let i = 0; i < 5; i++) {
  const pw = POS_W[i], ph = pw / ASPECT;
  s.addImage({ path: ASSET + ENEMY[i % 3], x: 2.21 - pw / 2, y: ROW_Y[i] - ph / 2, w: pw, h: ph });
  const nw = NEG_W[i], nh = nw / ASPECT;
  s.addImage({ path: ASSET + SAFE[i % 3], x: 5.645 - nw / 2, y: ROW_Y[i] - nh / 2, w: nw, h: nh });
}

// ---- +1 strip: x 251..285 y 165..488 -> 3.49..3.96, 2.29..6.78 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 3.49, y: 2.29, w: 0.47, h: 4.49,
  fill: { color: PINK }, line: { color: RED_T, width: 1 },
});
for (let i = 0; i < 5; i++) {
  s.addText("+1", {
    x: 3.49, y: ROW_Y[i] - 0.15, w: 0.47, h: 0.3,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: RED_T, fontFace: FONT, margin: 0,
  });
}
// ---- 0 strip: x 498..536 y 162..497 -> 6.92..7.44, 2.25..6.90 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 6.92, y: 2.25, w: 0.52, h: 4.65,
  fill: { color: MINT }, line: { color: GREEN_T, width: 1 },
});
for (let i = 0; i < 5; i++) {
  s.addText("0", {
    x: 6.92, y: ROW_Y[i] - 0.15, w: 0.52, h: 0.3,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: GREEN_T, fontFace: FONT, margin: 0,
  });
}

// ---- Activation Function panel: x 574..882 y 92..165 -> 7.97..12.25, 1.28..2.29 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.97, y: 1.28, w: 4.28, h: 1.01,
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.25 },
});
s.addText("Activation Function", {
  x: 9.08, y: 1.34, w: 2.0, h: 0.2, align: "left", valign: "top",
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Sigmoid function (0, +1)", {
  x: 8.30, y: 1.60, w: 2.2, h: 0.2, align: "left", valign: "top",
  fontSize: 11, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText('Threshold at "0.5"', {
  x: 8.10, y: 1.88, w: 2.0, h: 0.2, align: "left", valign: "top",
  fontSize: 11, bold: true, color: RED_T, fontFace: FONT, margin: 0,
});
// pink circle with cross-axes + sigmoid curve: circle x 802..849 y 98..142 -> 11.14..11.79, 1.36..1.97
s.addImage({ path: ASSET + "eq_020_sigmoid_circle.png", x: 11.14, y: 1.36, w: 0.65, h: 0.65 });

// ---- Training panel: bordered cream box x 555..900 y 200..330 -> 7.71..12.50, 2.78..4.58 ----
s.addText("Training", {
  x: 7.71, y: 2.86, w: 4.79, h: 0.22, align: "center", valign: "top",
  fontSize: 13, bold: true, color: RED_T, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 7.71, y: 2.78, w: 4.79, h: 1.80,
  fill: { color: CREAM }, line: { color: "B9A06A", width: 0.75 }, adjustValue: 0.18,
});
s.addText("Input Sample", {
  x: 7.92, y: 3.21, w: 0.9, h: 0.18, align: "left", valign: "top",
  fontSize: 9, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Predicted Class", {
  x: 9.72, y: 3.21, w: 1.2, h: 0.18, align: "left", valign: "top",
  fontSize: 9, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// block arrow from the Input Sample label into the Model node (no placeholder box)
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 7.95, y: 3.62, w: 0.50, h: 0.26,
  fill: { color: "FFFFFF" }, line: { color: RED_T, width: 1.25 },
});
// Model box: x 612..738 y 243..307 -> 8.50..10.25, 3.38..4.26
s.addShape(pptx.shapes.RECTANGLE, {
  x: 8.50, y: 3.38, w: 1.75, h: 0.88,
  fill: { color: DARKRED }, line: { color: "600000", width: 1 },
});
s.addText("Model", {
  x: 8.56, y: 3.44, w: 1.06, h: 0.22, align: "center", valign: "top",
  fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addImage({ path: ASSET + "eq_020_sigmoid_circle_small.png", x: 9.70, y: 3.42, w: 0.44, h: 0.44 });
s.addText("(Any value \u2192 (0, +1))", {
  x: 8.52, y: 3.90, w: 1.71, h: 0.22, align: "center", valign: "top",
  fontSize: 8, bold: true, color: "FFFF00", fontFace: FONT, margin: 0,
});
// arrow model -> LOSS: x 741..769 -> 10.29..10.57
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 10.29, y: 3.78, w: 0.28, h: 0.20,
  fill: { color: "FFFFFF" }, line: { color: RED_T, width: 1 },
});
// LOSS ellipse: x 761..839 y 253..301 -> 10.57..11.65, 3.51..4.18
s.addShape(pptx.shapes.OVAL, {
  x: 10.57, y: 3.52, w: 1.08, h: 0.66,
  fill: { color: PEACH }, line: { color: ORANGE_L, width: 1.5 },
});
s.addText("LOSS", {
  x: 10.57, y: 3.52, w: 1.08, h: 0.66,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: RED_T, fontFace: FONT, margin: 0,
});
// left-pointing connector from "Label of Input Sample (+1, 0)" into LOSS
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 11.66, y: 3.78, w: 0.18, h: 0.20,
  fill: { color: "FFFFFF" }, line: { color: RED_T, width: 1 },
});
s.addText("Label of\nInput\nSample", {
  x: 11.88, y: 3.50, w: 0.58, h: 0.42, align: "left", valign: "top",
  fontSize: 7, bold: true, color: DARK, fontFace: FONT, margin: 0, lineSpacing: 8,
});
s.addText("(+1, 0)", {
  x: 11.88, y: 3.97, w: 0.6, h: 0.18, align: "left", valign: "top",
  fontSize: 9, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- Evaluation panel: bordered cream box x 555..900 y 375..500 -> 7.71..12.50, 5.21..6.94 ----
s.addText("Evaluation", {
  x: 7.71, y: 5.30, w: 4.79, h: 0.22, align: "center", valign: "top",
  fontSize: 13, bold: true, color: RED_T, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 7.71, y: 5.21, w: 4.79, h: 1.73,
  fill: { color: CREAM }, line: { color: "B9A06A", width: 0.75 }, adjustValue: 0.18,
});
s.addText("Test Sample", {
  x: 7.92, y: 5.65, w: 0.9, h: 0.18, align: "left", valign: "top",
  fontSize: 9, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Predicted Class", {
  x: 9.72, y: 5.65, w: 1.2, h: 0.18, align: "left", valign: "top",
  fontSize: 9, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 7.95, y: 6.06, w: 0.50, h: 0.26,
  fill: { color: "FFFFFF" }, line: { color: RED_T, width: 1.25 },
});
// Model box: x 612..738 y 418..483 -> 8.50..10.25, 5.81..6.71
s.addShape(pptx.shapes.RECTANGLE, {
  x: 8.50, y: 5.81, w: 1.75, h: 0.90,
  fill: { color: DARKRED }, line: { color: "600000", width: 1 },
});
s.addText("Model", {
  x: 8.56, y: 5.87, w: 1.06, h: 0.22, align: "center", valign: "top",
  fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addImage({ path: ASSET + "eq_020_sigmoid_circle_small.png", x: 9.70, y: 5.85, w: 0.44, h: 0.44 });
s.addText("(Any value \u2192 (0, +1))", {
  x: 8.52, y: 6.33, w: 1.71, h: 0.22, align: "center", valign: "top",
  fontSize: 8, bold: true, color: "FFFF00", fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: 10.29, y: 6.14, w: 0.70, h: 0.20,
  fill: { color: "FFFFFF" }, line: { color: RED_T, width: 1 },
});
s.addText("(+1, 0)", {
  x: 11.05, y: 6.12, w: 0.75, h: 0.24, align: "left", valign: "middle",
  fontSize: 11, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_020_recreated.pptx"
}).then(() => console.log("done"));
