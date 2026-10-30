// Slide 002 — Training Samples with Labels [0,1] (Two Classes)
// Rebuilt from PIL measurements of unique_slides/slide_002.jpg (960x540 px, 1px = 1pt = 1/72 in)
// plus pool_run/image_analysis/slide_002_analysis.txt (fresh read) and spec_gaps.md slide_002:
// the mapping line "(Any value) → (-1 , +1)" appears under BOTH Model boxes, verbatim with
// arrow glyph and printed spacing.
const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const FONT = "Arial";
const BG = "E8E8E8";
const FRAME = "C00000";
const BADGE = "FFF9C4";
const INK = "333333";
const NAVY = "1F3864";
const RED = "C00000";
const RED_BRIGHT = "FF0000";
const GREEN = "2E7D32";
const BLUE = "0070C0";
const BLUE_BORDER = "2E75B6";
const PURPLE = "8E44AD";
const PINK_STRIP = "F8DBDD";
const GREEN_STRIP = "E4FFEE";
const ACT_BG = "F1FAFF";
const TRAIN_BG = "F6D7FF";
const EVAL_BG = "FFE0F8";
const MODEL_BG = "FCE4EC";
const AMBER = "FFAF95";
const LBLUE = "DDEBF7";
const WHITE = "FFFFFF";
const BLACK = "000000";

const ASSETS = path.join(__dirname, "assets");
const AIR_ENEMY = path.join(ASSETS, "eq_019_airplane_enemy.png"); // 745x672 px @600dpi
const AIR_SAFE = path.join(ASSETS, "eq_019_airplane_safe.png");
const SIGMOID = path.join(ASSETS, "sigmoid_002.png");            // 801x291 px @300dpi
const AIR_W = 0.83, AIR_H = 0.75;        // drawn size in inches
const SIG_W = 801 / 300, SIG_H = 291 / 300; // 2.67 x 0.97 in

const s = pres.addSlide();
s.background = { color: BG };

// ---- house chrome ---------------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("2", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- title (house rule: y=0.28, x=0.6, w=12.13, centered; navy box echoes original) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  fill: { color: WHITE }, line: { color: NAVY, width: 1.5 },
});
s.addText([
  { text: "Training Samples with Labels ", options: { fontSize: 24, bold: true, color: NAVY, fontFace: FONT } },
  { text: "[0,1]", options: { fontSize: 24, bold: true, color: RED_BRIGHT, fontFace: FONT } },
  { text: " (Two Classes)", options: { fontSize: 24, bold: true, color: NAVY, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62, align: "center", valign: "middle", margin: 0,
});

// ---- left: Positive Class -------------------------------------------------
s.addText("Positive Class", {
  x: 1.33, y: 1.32, w: 2.9, h: 0.44, align: "left", valign: "top",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("\u201cShoot the Enemy\u201d", {
  x: 1.33, y: 1.86, w: 2.9, h: 0.35, align: "left", valign: "top",
  fontSize: 15, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
// rotated "Label" caption left of the positive plane pane
s.addText("Label", {
  x: 1.05, y: 3.55, w: 1.9, h: 0.3, align: "center", valign: "middle",
  fontSize: 12, color: RED, fontFace: FONT, margin: 0, rotate: 270,
});
// positive plane pane (red border)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.82, y: 1.81, w: 2.47, h: 5.29,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});
const posPlaneY = [2.60, 3.32, 4.33, 5.07, 6.00];
for (const py of posPlaneY) {
  s.addImage({ path: AIR_ENEMY, x: 1.10, y: py, w: AIR_W, h: AIR_H });
}
// pink +1 strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.36, y: 2.24, w: 0.79, h: 4.86,
  fill: { color: PINK_STRIP }, line: { color: RED, width: 1 },
});
const plusY = [2.50, 3.57, 4.43, 5.29, 6.14];
for (const py of plusY) {
  s.addText("+1", {
    x: 3.36, y: py, w: 0.79, h: 0.28, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ---- left: Negative Class -------------------------------------------------
s.addText("Negative Class", {
  x: 4.93, y: 1.32, w: 2.9, h: 0.44, align: "left", valign: "top",
  fontSize: 20, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201cSafe\u201d", {
  x: 4.93, y: 1.86, w: 2.9, h: 0.35, align: "left", valign: "top",
  fontSize: 15, bold: true, italic: true, color: GREEN, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 6.55, y: 3.55, w: 1.9, h: 0.3, align: "center", valign: "middle",
  fontSize: 12, color: GREEN, fontFace: FONT, margin: 0, rotate: 270,
});
// negative plane pane (green border)
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.58, y: 1.92, w: 2.14, h: 5.15,
  fill: { color: WHITE }, line: { color: GREEN, width: 2 },
});
const negPlaneY = [2.30, 3.20, 4.10, 4.95, 5.90];
for (const py of negPlaneY) {
  s.addImage({ path: AIR_SAFE, x: 4.80, y: py, w: AIR_W, h: AIR_H });
}
// green 0 strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.89, y: 2.22, w: 0.65, h: 4.60,
  fill: { color: GREEN_STRIP }, line: { color: GREEN, width: 1 },
});
const zeroY = [2.44, 3.31, 3.94, 4.67, 6.36];
for (const py of zeroY) {
  s.addText("0", {
    x: 6.89, y: py, w: 0.65, h: 0.28, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ---- right: Activation Function panel --------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.97, y: 1.18, w: 4.39, h: 1.13,
  fill: { color: ACT_BG }, line: { color: BLUE_BORDER, width: 1.5 },
});
s.addText("Activation Function", {
  x: 8.11, y: 1.30, w: 3.0, h: 0.30, align: "left", valign: "top",
  fontSize: 15, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Sigmoid function (0 , +1)", {
  x: 8.11, y: 1.62, w: 3.2, h: 0.26, align: "left", valign: "top",
  fontSize: 12, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Threshold at \u201c0.5\u201d", {
  x: 8.11, y: 1.90, w: 3.2, h: 0.26, align: "left", valign: "top",
  fontSize: 12, color: RED, fontFace: FONT, margin: 0,
});
// sigmoid plot
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.58, y: 1.32, w: 2.67, h: 0.97,
  fill: { color: WHITE }, line: { color: "9A9A9A", width: 0.75 },
});
s.addImage({ path: SIGMOID, x: 9.58, y: 1.32, w: SIG_W, h: SIG_H });

// ---- right: Training panel --------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.99, y: 2.92, w: 4.54, h: 2.51,
  fill: { color: TRAIN_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Training", {
  x: 8.11, y: 2.98, w: 1.6, h: 0.30, align: "left", valign: "top",
  fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// Input Sample ellipse (amber)
s.addShape(pres.shapes.OVAL, {
  x: 7.93, y: 3.40, w: 1.29, h: 0.42,
  fill: { color: AMBER }, line: { color: "843C0C", width: 1 },
});
s.addText("Input Sample", {
  x: 7.93, y: 3.40, w: 1.29, h: 0.42, align: "center", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow Input Sample -> Model
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 9.24, y: 3.52, w: 0.14, h: 0.18,
  fill: { color: "7B241C" }, line: { type: "none" },
});
// Model box (training)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 8.33, y: 3.33, w: 2.07, h: 0.91,
  fill: { color: MODEL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Model", {
  x: 8.42, y: 3.42, w: 0.9, h: 0.30, align: "left", valign: "middle",
  fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// mini sigmoid icon inside Model box
s.addImage({ path: SIGMOID, x: 9.15, y: 3.42, w: 1.15, h: 0.42 });
// MISSING mapping line from spec_gaps.md slide_002 — verbatim, arrow + spacing as printed
s.addText("(Any value) \u2192 (-1 , +1)", {
  x: 8.27, y: 3.72, w: 2.22, h: 0.25, align: "center", valign: "top",
  fontSize: 10.5, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow Model -> LOSS
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 10.42, y: 3.62, w: 0.30, h: 0.18,
  fill: { color: "7B241C" }, line: { type: "none" },
});
// LOSS circle (amber in original)
s.addShape(pres.shapes.OVAL, {
  x: 10.75, y: 3.42, w: 0.76, h: 0.76,
  fill: { color: AMBER }, line: { color: "843C0C", width: 1 },
});
s.addText("LOSS", {
  x: 10.75, y: 3.42, w: 0.76, h: 0.76, align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// Predicted Class label above the Model->LOSS arrow region
s.addShape(pres.shapes.OVAL, {
  x: 11.08, y: 3.33, w: 1.38, h: 0.42,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted Class", {
  x: 11.08, y: 3.33, w: 1.38, h: 0.42, align: "center", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
// Label of Input Sample ellipse (pale blue) below, arrow up into LOSS
s.addShape(pres.shapes.OVAL, {
  x: 9.69, y: 4.88, w: 1.29, h: 0.50,
  fill: { color: LBLUE }, line: { color: BLUE_BORDER, width: 1 },
});
s.addText("Label of Input Sample", {
  x: 9.69, y: 4.88, w: 1.29, h: 0.50, align: "center", valign: "middle",
  fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 11.10, y: 4.95, w: 1.27, h: 0.28, align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow Label -> LOSS (up-right)
s.addShape(pres.shapes.UP_ARROW, {
  x: 10.62, y: 4.30, w: 0.18, h: 0.55,
  fill: { color: BLACK }, line: { type: "none" }, rotate: 35,
});

// ---- right: Evaluation panel ------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.99, y: 5.44, w: 4.54, h: 1.67,
  fill: { color: EVAL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Evaluation", {
  x: 8.11, y: 5.50, w: 1.6, h: 0.30, align: "left", valign: "top",
  fontSize: 15, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// Test Sample ellipse (amber)
s.addShape(pres.shapes.OVAL, {
  x: 7.93, y: 5.90, w: 1.29, h: 0.42,
  fill: { color: AMBER }, line: { color: "843C0C", width: 1 },
});
s.addText("Test Sample", {
  x: 7.93, y: 5.90, w: 1.29, h: 0.42, align: "center", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 9.24, y: 6.02, w: 0.14, h: 0.18,
  fill: { color: "7B241C" }, line: { type: "none" },
});
// Model box (evaluation)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 8.33, y: 5.83, w: 2.07, h: 0.91,
  fill: { color: MODEL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Model", {
  x: 8.42, y: 5.92, w: 0.9, h: 0.30, align: "left", valign: "middle",
  fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 9.15, y: 5.92, w: 1.15, h: 0.42 });
// MISSING mapping line (verbatim, second occurrence)
s.addText("(Any value) \u2192 (-1 , +1)", {
  x: 8.27, y: 6.22, w: 2.22, h: 0.25, align: "center", valign: "top",
  fontSize: 10.5, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 10.42, y: 6.12, w: 0.30, h: 0.18,
  fill: { color: "7B241C" }, line: { type: "none" },
});
// Predicted Class ellipse (evaluation)
s.addShape(pres.shapes.OVAL, {
  x: 11.08, y: 5.83, w: 1.38, h: 0.42,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted Class", {
  x: 11.08, y: 5.83, w: 1.38, h: 0.42, align: "center", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 11.10, y: 6.30, w: 1.27, h: 0.28, align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_002_recreated.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out)).catch((e) => { console.error(e); process.exit(1); });
