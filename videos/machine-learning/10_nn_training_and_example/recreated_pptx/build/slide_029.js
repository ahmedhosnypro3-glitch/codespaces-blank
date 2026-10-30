// slide_029.js — After Updating O/p Layer weights (slide 29)
// Build: NODE_PATH=$(npm root -g) node slide_029.js
// Uses patterns: house-chrome, highlight-box
// Measurements: 960x540 source px -> 13.33x7.5in (72.02 px/in)

const pptxgen = require("pptxgenjs");

const ROOT = "/home/codespace/ai_llm_slides";
const VID = ROOT + "/videos/machine-learning/10_nn_training_and_example";

const FONT = "Arial";
const NUM = 29;
const TITLE = "After Updating O/p Layer weights";

const PX = 13.33 / 960;   // inches per source px
const px = v => +(v * PX).toFixed(4);

// House chrome colors
const BG = "E8E8E8";
const FRAME_COLOR = "C00000";
const BADGE_FILL = "FFF9C4";
const BADGE_LINE = "FFF9C4";
const BADGE_TEXT = "333333";
const TITLE_COLOR = "C00000";

// Slide colors (measured)
const RED = "C00000";
const BLUE_TEXT = "0000FF";
const BLACK = "000000";
const PALE_YELLOW = "FFF9C4";
const PURPLE_STROKE = "CC00CC";
const ORANGE_STROKE = "FF6600";
const CYAN = "33CCCC";
const GREEN_W = "00B000";
const MAGENTA_W = "CC33CC";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME_COLOR, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_FILL }, line: { color: BADGE_LINE, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: TITLE_COLOR, fontFace: FONT, margin: 0,
});

// ========== RED DIAGRAM BOX (x143-831, y202-397) ==========
const BX = px(143), BY = px(202), BW = px(831 - 143), BH = px(397 - 202);
s.addShape(pres.shapes.RECTANGLE, {
  x: BX, y: BY, w: BW, h: BH,
  fill: { type: "none" }, line: { color: "993333", width: 1.5 },
});

// ========== HELPERS ==========
function node(cxPx, cyPx, rPx, fill, stroke) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cxPx - rPx), y: px(cyPx - rPx), w: px(2 * rPx), h: px(2 * rPx),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
}
function circleText(cxPx, cyPx, rPx, txt, size) {
  s.addText(txt, {
    x: px(cxPx - rPx), y: px(cyPx - rPx), w: px(2 * rPx), h: px(2 * rPx),
    align: "center", valign: "middle",
    fontSize: size || 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}
function label(cxPx, cyPx, txt, color, size, wPx, italic) {
  s.addText(txt, {
    x: px(cxPx - (wPx || 40) / 2), y: px(cyPx - 8), w: px(wPx || 40), h: px(16),
    align: "center", valign: "middle",
    fontSize: size || 11, bold: true, italic: italic || false, color: color, fontFace: FONT, margin: 0,
  });
}
function conn(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color: color, width: 1 },
  });
}
function rotLabel(cxPx, cyPx, txt, color, size, wPx) {
  s.addText(txt, {
    x: px(cxPx - (wPx || 44) / 2), y: px(cyPx - 7), w: px(wPx || 44), h: px(14),
    align: "center", valign: "middle", rotate: -25,
    fontSize: size || 9, bold: true, color: color, fontFace: FONT, margin: 0,
  });
}

// ========== INPUT LAYER ==========
// Black input nodes x1, x2 + Bias (cyan, "1")
node(217, 240, 6, BLACK, BLACK);
node(217, 300, 6, BLACK, BLACK);
node(219, 340, 8, CYAN, BLUE_TEXT);
circleText(219, 340, 8, "1", 9);

// Input column vector [1;5] at x~170-204
s.addText("[", { x: px(168), y: px(240), w: px(10), h: px(90), fontSize: 13, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("1", { x: px(180), y: px(240), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("5", { x: px(180), y: px(289), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("]", { x: px(194), y: px(240), w: px(10), h: px(90), fontSize: 13, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// x1, x2 labels (right of input nodes)
label(224, 230, "x₁", BLACK, 11, 30);
label(224, 290, "x₂", BLACK, 11, 30);
label(224, 352, "Bias", BLACK, 10, 36);

// "Input" label (blue, top-left of box)
label(170, 214, "Input", BLUE_TEXT, 11, 46, false);

// ========== HIDDEN LAYER (yellow circles, purple stroke, "3","4","5") ==========
node(388, 237, 10, PALE_YELLOW, PURPLE_STROKE);
circleText(388, 237, 10, "3", 10);
node(388, 294, 10, PALE_YELLOW, PURPLE_STROKE);
circleText(388, 294, 10, "4", 10);
node(388, 350, 10, PALE_YELLOW, PURPLE_STROKE);
circleText(388, 350, 10, "5", 10);

// O3 O4 O5 labels above the hidden nodes
label(388, 219, "O₃", BLACK, 11, 30);
label(388, 276, "O₄", BLACK, 11, 30);
label(388, 332, "O₅", BLACK, 11, 30);

// Hidden Bias (cyan, "1") at (369,363)
node(369, 363, 7, CYAN, BLUE_TEXT);
circleText(369, 363, 7, "1", 8);
label(330, 363, "Bias", BLACK, 9, 36);

// ========== OUTPUT LAYER (orange circles "6","7") ==========
node(591, 269, 9, PALE_YELLOW, ORANGE_STROKE);
circleText(591, 269, 9, "6", 10);
node(591, 329, 9, PALE_YELLOW, ORANGE_STROKE);
circleText(591, 329, 9, "7", 10);

// O6 O7 labels to the right of output nodes
label(618, 266, "O₆", BLACK, 11, 30);
label(618, 326, "O₇", BLACK, 11, 30);

// "Output" label (blue, above output nodes)
label(600, 232, "Output", BLUE_TEXT, 11, 46, false);

// ========== TARGET (far right) ==========
label(752, 225, "Target", BLACK, 11, 46, true);
s.addText("[", { x: px(658), y: px(245), w: px(10), h: px(62), fontSize: 13, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("0", { x: px(669), y: px(245), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("1", { x: px(669), y: px(296), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("]", { x: px(681), y: px(245), w: px(10), h: px(62), fontSize: 13, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
label(641, 232, "t₆", BLACK, 10, 20);
label(641, 283, "t₇", BLACK, 10, 20);

// ========== CONNECTIONS ==========
// input -> hidden (green lines)
conn(223, 240, 378, 237, GREEN_W);
conn(223, 240, 378, 294, GREEN_W);
conn(223, 240, 378, 350, GREEN_W);
conn(223, 300, 378, 237, GREEN_W);
conn(223, 300, 378, 294, GREEN_W);
conn(223, 300, 378, 350, GREEN_W);
conn(226, 340, 378, 237, GREEN_W);
conn(226, 340, 378, 294, GREEN_W);
conn(226, 340, 378, 350, GREEN_W);

// hidden -> output (magenta lines)
conn(398, 237, 582, 269, MAGENTA_W);
conn(398, 237, 582, 329, MAGENTA_W);
conn(398, 294, 582, 269, MAGENTA_W);
conn(398, 294, 582, 329, MAGENTA_W);
conn(398, 350, 582, 269, MAGENTA_W);
conn(398, 350, 582, 329, MAGENTA_W);

// output -> target (red dashed)
conn(600, 269, 636, 252, RED);
conn(600, 269, 636, 305, RED);
conn(600, 329, 636, 252, RED);
conn(600, 329, 636, 305, RED);

// ========== GREEN WEIGHT LABELS ==========
label(241, 228, "0.1", GREEN_W, 9, 34);
label(236, 258, "0.3", GREEN_W, 9, 34);
label(265, 244, "0.2", GREEN_W, 9, 34);
label(306, 240, "0.4", GREEN_W, 9, 34);
label(312, 277, "0.5", GREEN_W, 9, 34);
label(239, 322, "0.1", GREEN_W, 9, 34);
label(263, 326, "0.1", GREEN_W, 9, 34);
label(263, 341, "0.1", GREEN_W, 9, 34);
label(312, 314, "0.6", GREEN_W, 9, 34);

// ========== MAGENTA WEIGHT LABELS (rotated ~-25deg) ==========
rotLabel(420, 220, "-0.29", MAGENTA_W, 8, 40);
rotLabel(410, 243, "0.458", MAGENTA_W, 8, 44);
rotLabel(437, 265, "-0.218", MAGENTA_W, 8, 44);
rotLabel(440, 280, "0.565", MAGENTA_W, 8, 44);
rotLabel(420, 305, "-0.134", MAGENTA_W, 8, 42);
rotLabel(412, 330, "0.669", MAGENTA_W, 8, 44);
rotLabel(462, 313, "-0.445", MAGENTA_W, 8, 42);
rotLabel(462, 343, "-0.375", MAGENTA_W, 8, 40);

// ========== LEARNING RATE (bottom-right of box) ==========
label(760, 380, "η= 5", RED, 12, 50, true);

// ========== WRITE FILE ==========
pres.writeFile({ fileName: VID + "/recreated_pptx/slide_029_recreated.pptx" })
  .then(() => console.log("wrote slide_029_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
