// Slide 002 — Training Samples with Labels [0,1] (Two Classes)
// Rebuilt from PIL measurements of unique_slides/slide_002.jpg (960x540 px, 1px = 1pt = 1/72 in)
// plus pool_run/image_analysis/slide_002_analysis.txt (fresh read) and spec_gaps.md slide_002:
// the mapping line "(Any value) → (-1 , +1)" appears inside BOTH Model boxes, verbatim with
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
// Plane panes copied pixel-for-pixel from the original frame (defect Pattern A fix).
const PANE_POS = path.join(ASSETS, "pane_pos_002.png"); // 146x357 px
const PANE_NEG = path.join(ASSETS, "pane_neg_002.png"); // 142x359 px
const SIGMOID = path.join(ASSETS, "sigmoid_002.png");   // 801x291 px @300dpi
const SIG_W = 801 / 300, SIG_H = 291 / 300;

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
  { text: "Training Samples with Labels ", options: { fontSize: 30, bold: true, color: NAVY, fontFace: FONT } },
  { text: "[0,1]", options: { fontSize: 30, bold: true, color: RED_BRIGHT, fontFace: FONT } },
  { text: " (Two Classes)", options: { fontSize: 30, bold: true, color: NAVY, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62, align: "center", valign: "middle", margin: 0,
});

// ---- left container -------------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 57 / 72, y: 91 / 72, w: 499 / 72, h: 425 / 72,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});

// class headers + subtitles
s.addText("Positive Class", {
  x: 103 / 72, y: 100 / 72, w: 1.9, h: 0.45, align: "left", valign: "top",
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Negative Class", {
  x: 356 / 72, y: 100 / 72, w: 1.9, h: 0.42, align: "left", valign: "top",
  fontSize: 16, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201cShoot the Enemy\u201d", {
  x: 103 / 72, y: 135 / 72, w: 1.9, h: 0.34, align: "left", valign: "top",
  fontSize: 13, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("\u201cSafe\u201d", {
  x: 356 / 72, y: 138 / 72, w: 1.9, h: 0.3, align: "left", valign: "top",
  fontSize: 13, bold: true, italic: true, color: GREEN, fontFace: FONT, margin: 0,
});
// "Label" captions above each value strip
s.addText("Label", {
  x: 255 / 72, y: 117 / 72, w: 0.56, h: 0.2, align: "center", valign: "top",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 502 / 72, y: 117 / 72, w: 0.56, h: 0.2, align: "center", valign: "top",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// positive pane (red border) + artwork copied from the original frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 81 / 72, y: 137 / 72, w: 156 / 72, h: 367 / 72,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});
s.addImage({ path: PANE_POS, x: 86 / 72, y: 142 / 72, w: 146 / 72, h: 357 / 72 });

// pink +1 strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 238 / 72, y: 158 / 72, w: 60 / 72, h: 353 / 72,
  fill: { color: PINK_STRIP }, line: { color: RED, width: 1 },
});
const plusY = [184, 247, 309, 371, 432]; // px, box tops for glyph centers 194..442
for (const py of plusY) {
  s.addText("+1", {
    x: 238 / 72, y: py / 72, w: 60 / 72, h: 20 / 72, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// negative pane (green border) + artwork copied from the original frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 330 / 72, y: 138 / 72, w: 154 / 72, h: 371 / 72,
  fill: { color: WHITE }, line: { color: GREEN, width: 2 },
});
s.addImage({ path: PANE_NEG, x: 336 / 72, y: 144 / 72, w: 142 / 72, h: 359 / 72 });

// green 0 strip — the original prints six "0" digits (measured glyph rows)
s.addShape(pres.shapes.RECTANGLE, {
  x: 494 / 72, y: 160 / 72, w: 49 / 72, h: 339 / 72,
  fill: { color: GREEN_STRIP }, line: { color: GREEN, width: 1 },
});
const zeroY = [166, 228, 274, 326, 386, 448]; // px, box tops for glyph centers 176..458
for (const zy of zeroY) {
  s.addText("0", {
    x: 494 / 72, y: zy / 72, w: 49 / 72, h: 20 / 72, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ---- right: Activation Function panel --------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 574 / 72, y: 91 / 72, w: 308 / 72, h: 74 / 72,
  fill: { color: ACT_BG }, line: { color: BLUE_BORDER, width: 1.5 },
});
s.addText("Activation Function", {
  x: 584 / 72, y: 96 / 72, w: 3.0, h: 0.4, align: "left", valign: "top",
  fontSize: 15, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Sigmoid function (0 , +1)", {
  x: 584 / 72, y: 134 / 72, w: 3.2, h: 0.32, align: "left", valign: "top",
  fontSize: 12, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Threshold at \u201c0.5\u201d", {
  x: 584 / 72, y: 158 / 72, w: 3.2, h: 0.3, align: "left", valign: "top",
  fontSize: 12, color: RED, fontFace: FONT, margin: 0,
});
// sigmoid curve with axes, drawn in the panel's right area (original: curve x693-853 y108-141)
s.addImage({ path: SIGMOID, x: 690 / 72, y: 96 / 72, w: 193 / 72, h: 69 / 72 });

// ---- right: Training panel --------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 574 / 72, y: 205 / 72, w: 328 / 72, h: 177 / 72,
  fill: { color: TRAIN_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Training", {
  x: 584 / 72, y: 226 / 72, w: 1.6, h: 0.3, align: "left", valign: "top",
  fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// Input Sample ellipse
s.addShape(pres.shapes.OVAL, {
  x: 556 / 72, y: 236 / 72, w: 58 / 72, h: 44 / 72,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Input Sample", {
  x: 556 / 72, y: 236 / 72, w: 58 / 72, h: 44 / 72, align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 8.52, y: 3.50, w: 0.12, h: 0.16, fill: { color: "7B241C" }, line: { type: "none" },
});
// Model box (training) — mapping line INSIDE the box, verbatim
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 613 / 72, y: 245 / 72, w: 123 / 72, h: 60 / 72,
  fill: { color: MODEL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Model", {
  x: 620 / 72, y: 246 / 72, w: 0.8, h: 0.3, align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 648 / 72, y: 250 / 72, w: 80 / 72, h: 29 / 72 });
s.addText("(Any value) \u2192 (-1 , +1)", {
  x: 613 / 72, y: 272 / 72, w: 123 / 72, h: 0.25, align: "center", valign: "top",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow Model -> LOSS
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 10.30, y: 3.55, w: 0.30, h: 0.16, fill: { color: "7B241C" }, line: { type: "none" },
});
// LOSS amber circle
s.addShape(pres.shapes.OVAL, {
  x: 774 / 72, y: 245 / 72, w: 55 / 72, h: 56 / 72,
  fill: { color: AMBER }, line: { color: "843C0C", width: 1 },
});
s.addText("LOSS", {
  x: 774 / 72, y: 245 / 72, w: 55 / 72, h: 56 / 72, align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// Predicted Class ellipse (upper right)
s.addShape(pres.shapes.OVAL, {
  x: 793 / 72, y: 232 / 72, w: 108 / 72, h: 41 / 72,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted Class", {
  x: 793 / 72, y: 232 / 72, w: 108 / 72, h: 41 / 72, align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow Predicted Class -> LOSS (down)
s.addShape(pres.shapes.DOWN_ARROW, {
  x: 11.45, y: 3.90, w: 0.16, h: 0.28, fill: { color: "7B241C" }, line: { type: "none" },
});
// Label of Input Sample ellipse (below) + (+1, 0)
s.addShape(pres.shapes.OVAL, {
  x: 697 / 72, y: 344 / 72, w: 93 / 72, h: 34 / 72,
  fill: { color: LBLUE }, line: { color: BLUE_BORDER, width: 1 },
});
s.addText("Label of Input Sample", {
  x: 697 / 72, y: 344 / 72, w: 93 / 72, h: 34 / 72, align: "center", valign: "middle",
  fontSize: 7.5, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 795 / 72, y: 358 / 72, w: 90 / 72, h: 0.28, align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow Label -> LOSS (up)
s.addShape(pres.shapes.UP_ARROW, {
  x: 10.55, y: 4.22, w: 0.16, h: 0.42, fill: { color: BLACK }, line: { type: "none" },
});

// ---- right: Evaluation panel ------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 574 / 72, y: 384 / 72, w: 328 / 72, h: 132 / 72,
  fill: { color: EVAL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Evaluation", {
  x: 584 / 72, y: 390 / 72, w: 1.6, h: 0.3, align: "left", valign: "top",
  fontSize: 15, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// Test Sample ellipse
s.addShape(pres.shapes.OVAL, {
  x: 561 / 72, y: 410 / 72, w: 58 / 72, h: 41 / 72,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Test Sample", {
  x: 561 / 72, y: 410 / 72, w: 58 / 72, h: 41 / 72, align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 8.55, y: 5.85, w: 0.12, h: 0.16, fill: { color: "7B241C" }, line: { type: "none" },
});
// Model box (evaluation) — mapping line INSIDE the box, verbatim (second occurrence)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 613 / 72, y: 420 / 72, w: 123 / 72, h: 60 / 72,
  fill: { color: MODEL_BG }, line: { color: RED, width: 1.5 },
});
s.addText("Model", {
  x: 620 / 72, y: 421 / 72, w: 0.8, h: 0.3, align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 648 / 72, y: 425 / 72, w: 80 / 72, h: 29 / 72 });
s.addText("(Any value) \u2192 (-1 , +1)", {
  x: 613 / 72, y: 447 / 72, w: 123 / 72, h: 0.25, align: "center", valign: "top",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 10.30, y: 5.90, w: 0.30, h: 0.16, fill: { color: "7B241C" }, line: { type: "none" },
});
// Predicted Class ellipse (evaluation)
s.addShape(pres.shapes.OVAL, {
  x: 790 / 72, y: 408 / 72, w: 111 / 72, h: 41 / 72,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted Class", {
  x: 790 / 72, y: 408 / 72, w: 111 / 72, h: 41 / 72, align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 790 / 72, y: 452 / 72, w: 90 / 72, h: 0.28, align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_002_recreated.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out)).catch((e) => { console.error(e); process.exit(1); });
