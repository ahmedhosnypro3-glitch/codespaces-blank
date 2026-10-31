// Slide 002 — Training Samples with Labels [0,1] (Two Classes)
// Rebuild v2 (agent-s02-fresh): geometry re-measured from unique_slides/slide_002.jpg
// (960x540 px, 1px = 1pt). Fixes vs render_3: quotes no longer hidden under pane
// images, strips/panels match measured boxes, six->five label cells, activation
// text inside panel, training flow laid out horizontally per original.
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
const PANEL_BLUE_LINE = "2E5AAC";
const PINK_STRIP = "FFDADE";
const GREEN_STRIP = "E4FFEE";
const ACT_BG = "F0FAFF";
const TRAIN_BG = "F0E0D0";
const TRAIN_LINE = "806050";
const EVAL_BG = "FFFFFF";
const EVAL_LINE = "806050";
const MODEL_BG = "FCE4EC";
const AMBER = "F8CBAD";
const LBLUE = "DDEBF7";
const WHITE = "FFFFFF";
const BLACK = "000000";
const ARROW = "7B241C";

const ASSETS = path.join(__dirname, "assets");
const PANE_POS = path.join(ASSETS, "pane_pos_002.png"); // 151x362 px
const PANE_NEG = path.join(ASSETS, "pane_neg_002.png"); // 144x362 px
const SIGMOID = path.join(ASSETS, "sigmoid_002.png");   // 140x60 px

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

// ---- title (house rule: y=0.28, x=0.6, w=12.13, centered) -------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  fill: { color: WHITE }, line: { color: NAVY, width: 1.5 },
});
s.addText([
  { text: "Training Samples with Labels ", options: { fontSize: 22, bold: true, color: NAVY, fontFace: FONT } },
  { text: "[0,1]", options: { fontSize: 22, bold: true, color: RED_BRIGHT, fontFace: FONT } },
  { text: " (Two Classes)", options: { fontSize: 22, bold: true, color: NAVY, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62, align: "center", valign: "middle", margin: 0,
});

// ---- left: class headers + quotes (above the panes, never covered) ---------
s.addText("Positive Class", {
  x: 103 / 72, y: 99 / 72, w: 2.2, h: 0.24, align: "left", valign: "top",
  fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("\u201cShoot the Enemy\u201d", {
  x: 103 / 72, y: 117 / 72, w: 2.4, h: 0.24, align: "left", valign: "top",
  fontSize: 13, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Negative Class", {
  x: 374 / 72, y: 99 / 72, w: 2.2, h: 0.24, align: "left", valign: "top",
  fontSize: 15, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201cSafe\u201d", {
  x: 396 / 72, y: 117 / 72, w: 1.4, h: 0.24, align: "left", valign: "top",
  fontSize: 13, bold: true, italic: true, color: GREEN, fontFace: FONT, margin: 0,
});

// ---- positive pane (red border) + artwork cropped from the original ---------
s.addShape(pres.shapes.RECTANGLE, {
  x: 82 / 72, y: 138 / 72, w: 154 / 72, h: 365 / 72,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});
s.addImage({ path: PANE_POS, x: 84 / 72, y: 140 / 72, w: 151 / 72, h: 362 / 72 });

// ---- pink +1 strip: vertical "Label" left, five "+1" right -----------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 237 / 72, y: 138 / 72, w: 96 / 72, h: 365 / 72,
  fill: { color: PINK_STRIP }, line: { color: RED, width: 1.25 },
});
s.addText("Label", {
  x: 240 / 72, y: 230 / 72, w: 0.3, h: 2.4, rotate: 270,
  align: "center", valign: "middle",
  fontSize: 11, color: RED, fontFace: FONT, margin: 0,
});
const plusY = [185, 247, 309, 370, 432]; // px box tops, glyph centers 195..442
for (const py of plusY) {
  s.addText("+1", {
    x: 262 / 72, y: py / 72, w: 44 / 72, h: 20 / 72, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ---- negative pane (green border) + artwork cropped from the original -------
s.addShape(pres.shapes.RECTANGLE, {
  x: 334 / 72, y: 138 / 72, w: 147 / 72, h: 365 / 72,
  fill: { color: WHITE }, line: { color: GREEN, width: 2 },
});
s.addImage({ path: PANE_NEG, x: 336 / 72, y: 140 / 72, w: 144 / 72, h: 362 / 72 });

// ---- green 0 strip: vertical "Label" left, five "0" right -------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 482 / 72, y: 138 / 72, w: 73 / 72, h: 365 / 72,
  fill: { color: GREEN_STRIP }, line: { color: GREEN, width: 1.25 },
});
s.addText("Label", {
  x: 500 / 72, y: 230 / 72, w: 0.3, h: 2.4, rotate: 270,
  align: "center", valign: "middle",
  fontSize: 11, color: GREEN, fontFace: FONT, margin: 0,
});
const zeroY = [185, 247, 309, 370, 432];
for (const zy of zeroY) {
  s.addText("0", {
    x: 520 / 72, y: zy / 72, w: 30 / 72, h: 20 / 72, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ---- right: Activation Function panel (y 92..165) ---------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 577 / 72, y: 92 / 72, w: 322 / 72, h: 73 / 72,
  fill: { color: ACT_BG }, line: { color: PANEL_BLUE_LINE, width: 1.5 },
});
s.addText("Activation Function", {
  x: 585 / 72, y: 100 / 72, w: 3.4, h: 0.24, align: "left", valign: "top",
  fontSize: 14, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Sigmoid function (0 , +1)", {
  x: 585 / 72, y: 116 / 72, w: 3.6, h: 0.24, align: "left", valign: "top",
  fontSize: 12, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Threshold at \u201c0.5\u201d", {
  x: 585 / 72, y: 136 / 72, w: 3.6, h: 0.24, align: "left", valign: "top",
  fontSize: 12, color: RED, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 740 / 72, y: 100 / 72, w: 140 / 72, h: 60 / 72 });

// ---- right: Training panel (y 206..320) --------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 577 / 72, y: 206 / 72, w: 322 / 72, h: 114 / 72,
  fill: { color: TRAIN_BG }, line: { color: TRAIN_LINE, width: 2 },
});
s.addText("Training", {
  x: 585 / 72, y: 227 / 72, w: 1.6, h: 0.24, align: "left", valign: "top",
  fontSize: 14, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// Input Sample (amber ellipse)
s.addShape(pres.shapes.OVAL, {
  x: 580 / 72, y: 250 / 72, w: 58 / 72, h: 44 / 72,
  fill: { color: AMBER }, line: { color: BLACK, width: 1 },
});
s.addText("Input Sample", {
  x: 580 / 72, y: 250 / 72, w: 58 / 72, h: 44 / 72, align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 640 / 72, y: 268 / 72, w: 18 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Model box with mini sigmoid + verbatim mapping line (drift item)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 660 / 72, y: 246 / 72, w: 76 / 72, h: 44 / 72,
  fill: { color: MODEL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Model", {
  x: 664 / 72, y: 250 / 72, w: 0.7, h: 0.24, align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 694 / 72, y: 252 / 72, w: 38 / 72, h: 16 / 72 });
s.addText("(Any value) \u2192 (-1 , +1)", {
  x: 655 / 72, y: 292 / 72, w: 120 / 72, h: 0.22, align: "center", valign: "top",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 738 / 72, y: 268 / 72, w: 18 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Predicted Class (plain label above LOSS per original) + LOSS circle
s.addText("Predicted Class", {
  x: 758 / 72, y: 248 / 72, w: 76 / 72, h: 0.2, align: "center", valign: "top",
  fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.OVAL, {
  x: 762 / 72, y: 266 / 72, w: 48 / 72, h: 40 / 72,
  fill: { color: AMBER }, line: { color: "843C0C", width: 1 },
});
s.addText("LOSS", {
  x: 762 / 72, y: 266 / 72, w: 48 / 72, h: 40 / 72, align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 812 / 72, y: 280 / 72, w: 16 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Label of Input Sample (light blue ellipse) + (+1, 0)
s.addShape(pres.shapes.OVAL, {
  x: 830 / 72, y: 266 / 72, w: 66 / 72, h: 40 / 72,
  fill: { color: LBLUE }, line: { color: PANEL_BLUE_LINE, width: 1 },
});
s.addText("Label of Input Sample", {
  x: 830 / 72, y: 266 / 72, w: 66 / 72, h: 40 / 72, align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 830 / 72, y: 308 / 72, w: 66 / 72, h: 0.2, align: "center", valign: "top",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// ---- right: Evaluation panel (y 321..496) ------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 577 / 72, y: 321 / 72, w: 322 / 72, h: 175 / 72,
  fill: { color: EVAL_BG }, line: { color: EVAL_LINE, width: 2 },
});
s.addText("Evaluation", {
  x: 577 / 72, y: 350 / 72, w: 322 / 72, h: 0.24, align: "center", valign: "top",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// Test Sample (amber ellipse)
s.addShape(pres.shapes.OVAL, {
  x: 580 / 72, y: 424 / 72, w: 58 / 72, h: 44 / 72,
  fill: { color: AMBER }, line: { color: BLACK, width: 1 },
});
s.addText("Test Sample", {
  x: 580 / 72, y: 424 / 72, w: 58 / 72, h: 44 / 72, align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 640 / 72, y: 442 / 72, w: 18 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Model box (evaluation) — second verbatim mapping line (drift item)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 660 / 72, y: 424 / 72, w: 76 / 72, h: 44 / 72,
  fill: { color: MODEL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Model", {
  x: 664 / 72, y: 428 / 72, w: 0.7, h: 0.24, align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 694 / 72, y: 430 / 72, w: 38 / 72, h: 16 / 72 });
s.addText("(Any value) \u2192 (-1 , +1)", {
  x: 655 / 72, y: 470 / 72, w: 120 / 72, h: 0.22, align: "center", valign: "top",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 738 / 72, y: 442 / 72, w: 18 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Predicted Class ellipse + (+1, 0)
s.addShape(pres.shapes.OVAL, {
  x: 758 / 72, y: 424 / 72, w: 80 / 72, h: 40 / 72,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted Class", {
  x: 758 / 72, y: 424 / 72, w: 80 / 72, h: 40 / 72, align: "center", valign: "middle",
  fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 758 / 72, y: 466 / 72, w: 80 / 72, h: 0.22, align: "center", valign: "top",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_002_recreated.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out)).catch((e) => { console.error(e); process.exit(1); });
