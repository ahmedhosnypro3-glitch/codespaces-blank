// Slide 002 — Training Samples with Labels [0,1] (Two Classes)
// Rebuild v4: fixes judge_attempt_8 D1-D9 adjudicated against PIL measurements of
// unique_slides/slide_002.jpg (960x540, 1px = 1pt):
//  D1 left arrow Label-of-Input -> LOSS added; D2 activation text overlap removed;
//  D3/D4 Input/Test Sample capsules fully left of Model boxes; D5 Training/Evaluation
//  headings above panels, centered; D6 separate rounded panels w/ white gap;
//  D7 Predicted Class clear of panel top; D9 model sigmoid icon sized; caption verbatim
//  "(Any value) → (-1, +1)" per spec_gaps.
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
const RED_DARK = "A00000";
const RED_BRIGHT = "FF0000";
const GREEN = "2E7D32";
const GREEN_DARK = "1E7A34";
const BLUE = "0070C0";
const PANEL_BLUE_LINE = "2E5AAC";
const PINK_STRIP = "FFDADE";
const GREEN_STRIP = "E4FFEE";
const PANEL_TAN_LINE = "B7A28F";
const PANEL_TAN_FILL = "FEFEF4";
const MODEL_RED = "9D0000";
const AMBER = "F4C692";
const CAPSULE_PINK = "FBD3D3";
const WHITE = "FFFFFF";
const BLACK = "000000";
const ARROW = "333333";

const ASSETS = path.join(__dirname, "assets");
const PANE_POS = path.join(ASSETS, "pane_pos_002.png"); // 151x362
const PANE_NEG = path.join(ASSETS, "pane_neg_002.png"); // 144x362
const SIGMOID = path.join(ASSETS, "sigmoid_002.png");   // 140x60

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

// ---- left: class headers + quotes -------------------------------------------
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

// ---- positive pane + pink +1 strip ------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 82 / 72, y: 138 / 72, w: 154 / 72, h: 365 / 72,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});
s.addImage({ path: PANE_POS, x: 84 / 72, y: 140 / 72, w: 151 / 72, h: 362 / 72 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 237 / 72, y: 138 / 72, w: 96 / 72, h: 365 / 72,
  fill: { color: PINK_STRIP }, line: { color: RED, width: 1.25 },
});
s.addText("Label", {
  x: 237 / 72, y: 156 / 72, w: 96 / 72, h: 0.24, align: "center", valign: "top",
  fontSize: 10, color: RED_DARK, fontFace: FONT, margin: 0,
});
const plusY = [185, 247, 309, 370, 432];
for (const py of plusY) {
  s.addText("+1", {
    x: 244 / 72, y: py / 72, w: 60 / 72, h: 20 / 72, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: RED_DARK, fontFace: FONT, margin: 0,
  });
}

// ---- negative pane + green 0 strip -------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 334 / 72, y: 138 / 72, w: 147 / 72, h: 365 / 72,
  fill: { color: WHITE }, line: { color: RED_DARK, width: 2 },
});
s.addImage({ path: PANE_NEG, x: 336 / 72, y: 140 / 72, w: 144 / 72, h: 362 / 72 });

s.addShape(pres.shapes.RECTANGLE, {
  x: 482 / 72, y: 138 / 72, w: 73 / 72, h: 365 / 72,
  fill: { color: GREEN_STRIP }, line: { color: GREEN, width: 1.25 },
});
s.addText("Label", {
  x: 482 / 72, y: 156 / 72, w: 73 / 72, h: 0.24, align: "center", valign: "top",
  fontSize: 10, color: GREEN_DARK, fontFace: FONT, margin: 0,
});
const zeroY = [185, 247, 309, 370, 432];
for (const zy of zeroY) {
  s.addText("0", {
    x: 490 / 72, y: zy / 72, w: 55 / 72, h: 20 / 72, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: GREEN_DARK, fontFace: FONT, margin: 0,
  });
}

// ---- right: Activation Function panel (orig x575-881 y90-166) ----------------
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 575 / 72, y: 90 / 72, w: 306 / 72, h: 76 / 72,
  fill: { color: WHITE }, line: { color: PANEL_BLUE_LINE, width: 1.5 },
});
s.addText("Activation Function", {
  x: 584 / 72, y: 99 / 72, w: 120 / 72, h: 0.2, align: "left", valign: "top",
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Sigmoid function (0 , +1)", {
  x: 584 / 72, y: 118 / 72, w: 115 / 72, h: 0.18, align: "left", valign: "top",
  fontSize: 10, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Threshold at \u201c0.5\u201d", {
  x: 584 / 72, y: 137 / 72, w: 115 / 72, h: 0.18, align: "left", valign: "top",
  fontSize: 10, color: RED, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 706 / 72, y: 96 / 72, w: 170 / 72, h: 64 / 72 });

// ---- "Training" heading above its panel (orig y~180-190, centered) -----------
s.addText("Training", {
  x: 575 / 72, y: 178 / 72, w: 306 / 72, h: 0.26, align: "center", valign: "top",
  fontSize: 14, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- right: Training panel (orig x575-881 y205-320, tan) ----------------------
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 575 / 72, y: 205 / 72, w: 306 / 72, h: 115 / 72,
  fill: { color: PANEL_TAN_FILL }, line: { color: PANEL_TAN_LINE, width: 1.5 },
});
// Input Sample capsule (fully left of Model box)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 578 / 72, y: 262 / 72, w: 32 / 72, h: 28 / 72,
  fill: { color: CAPSULE_PINK }, line: { color: BLACK, width: 0.75 },
});
s.addText("Input Sample", {
  x: 578 / 72, y: 262 / 72, w: 32 / 72, h: 28 / 72, align: "center", valign: "middle",
  fontSize: 6.5, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 611 / 72, y: 271 / 72, w: 10 / 72, h: 10 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Model box (orig x613-736 y245-305, solid dark red)
s.addShape(pres.shapes.RECTANGLE, {
  x: 613 / 72, y: 245 / 72, w: 123 / 72, h: 60 / 72,
  fill: { color: MODEL_RED }, line: { color: MODEL_RED, width: 1 },
});
s.addText("Model", {
  x: 618 / 72, y: 250 / 72, w: 60 / 72, h: 0.24, align: "left", valign: "middle",
  fontSize: 12, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 688 / 72, y: 252 / 72, w: 44 / 72, h: 18 / 72 });
s.addText("(Any value) \u2192 (-1, +1)", {
  x: 616 / 72, y: 284 / 72, w: 117 / 72, h: 0.18, align: "center", valign: "middle",
  fontSize: 8, color: WHITE, fontFace: FONT, margin: 0,
});
// arrow Model -> LOSS
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 738 / 72, y: 268 / 72, w: 36 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Predicted Class label above LOSS circle, clear of panel top (D7)
s.addText("Predicted Class", {
  x: 740 / 72, y: 236 / 72, w: 88 / 72, h: 0.15, align: "left", valign: "top",
  fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
});
// LOSS amber circle (orig x775-829 y246-301)
s.addShape(pres.shapes.OVAL, {
  x: 775 / 72, y: 246 / 72, w: 54 / 72, h: 55 / 72,
  fill: { color: AMBER }, line: { color: "843C0C", width: 1 },
});
s.addText("LOSS", {
  x: 775 / 72, y: 246 / 72, w: 54 / 72, h: 55 / 72, align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// D1: left-pointing arrow from Label of Input Sample into LOSS
s.addShape(pres.shapes.LEFT_ARROW, {
  x: 831 / 72, y: 268 / 72, w: 14 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Label of Input Sample (orig x833-876 y243-261) + (+1, 0) below (orig y287-299)
s.addText("Label of Input Sample", {
  x: 846 / 72, y: 242 / 72, w: 34 / 72, h: 0.32, align: "left", valign: "top",
  fontSize: 6, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 840 / 72, y: 286 / 72, w: 40 / 72, h: 0.18, align: "left", valign: "top",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});

// ---- "Evaluation" heading above its panel (orig y~350-360, centered) ---------
s.addText("Evaluation", {
  x: 575 / 72, y: 350 / 72, w: 306 / 72, h: 0.26, align: "center", valign: "top",
  fontSize: 14, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- right: Evaluation panel (orig x575-881 y382-497) ------------------------
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 575 / 72, y: 382 / 72, w: 306 / 72, h: 115 / 72,
  fill: { color: PANEL_TAN_FILL }, line: { color: PANEL_TAN_LINE, width: 1.5 },
});
// Test Sample capsule (fully left of Model box)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 578 / 72, y: 438 / 72, w: 32 / 72, h: 28 / 72,
  fill: { color: CAPSULE_PINK }, line: { color: BLACK, width: 0.75 },
});
s.addText("Test Sample", {
  x: 578 / 72, y: 438 / 72, w: 32 / 72, h: 28 / 72, align: "center", valign: "middle",
  fontSize: 6.5, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 611 / 72, y: 447 / 72, w: 10 / 72, h: 10 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Model box (eval, orig x613-736 y422-463)
s.addShape(pres.shapes.RECTANGLE, {
  x: 613 / 72, y: 422 / 72, w: 123 / 72, h: 41 / 72,
  fill: { color: MODEL_RED }, line: { color: MODEL_RED, width: 1 },
});
s.addText("Model", {
  x: 618 / 72, y: 426 / 72, w: 60 / 72, h: 0.24, align: "left", valign: "middle",
  fontSize: 12, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addImage({ path: SIGMOID, x: 688 / 72, y: 428 / 72, w: 44 / 72, h: 18 / 72 });
s.addText("(Any value) \u2192 (-1, +1)", {
  x: 616 / 72, y: 447 / 72, w: 117 / 72, h: 0.14, align: "center", valign: "middle",
  fontSize: 7, color: WHITE, fontFace: FONT, margin: 0,
});
// arrow Model -> Predicted Class
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 738 / 72, y: 446 / 72, w: 36 / 72, h: 12 / 72,
  fill: { color: ARROW }, line: { type: "none" },
});
// Predicted Class label (orig y420-427 x736-776) + final (+1, 0) (orig y444-456 x770-829)
s.addText("Predicted Class", {
  x: 736 / 72, y: 420 / 72, w: 90 / 72, h: 0.15, align: "left", valign: "top",
  fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, 0)", {
  x: 776 / 72, y: 444 / 72, w: 54 / 72, h: 0.18, align: "center", valign: "top",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_002_recreated.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out)).catch((e) => { console.error(e); process.exit(1); });
