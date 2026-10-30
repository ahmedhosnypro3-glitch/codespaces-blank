const pptxgen = require("pptxgenjs");

// Slide 029: Neural Network Model
const NUM = 29;
const TITLE = "Neural Network Model";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const GREEN = "008000";
const BORDER_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const PEACH = "FDEBD0";
const TAN = "E6D5B8";
const TAN_TEXT = "5C4A2A";
const LIGHT_BLUE = "C0C0FF";
const PURPLE = "D0B0FF";
const GRAY = "808080";
const MAGENTA_FILL = "E6A0E6";
const MAGENTA_BORDER = "9932CC";
const DARK_GREEN = "00B050";
const LIGHT_GREEN_BG = "D9EAD3";
const LIGHT_BLUE_BG = "DDEBF7";
const LIGHT_GREEN_BG2 = "E2EFDA";
const PALE_YELLOW = "FFFDE7";
const BEIGE = "E8E0D0";
const LIGHT_BEIGE = "F2E4D0";
const PINK = "E8A0A0";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW (yellow circle at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Input Sample / Target Label boxes (magenta) with dashed arrow between
// Input Sample at top-left
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 1.0, w: 1.8, h: 0.6,
  fill: { color: MAGENTA_FILL }, line: { color: MAGENTA_BORDER, width: 1.5 },
});
s.addText([
  { text: "Input", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
  { text: "Sample", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
], {
  x: 0.6, y: 1.0, w: 1.8, h: 0.6,
  align: "center", valign: "middle",
  margin: 0,
});

// Target Label at top-right
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.8, y: 1.0, w: 1.8, h: 0.6,
  fill: { color: MAGENTA_FILL }, line: { color: MAGENTA_BORDER, width: 1.5 },
});
s.addText([
  { text: "Target", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
  { text: "Label", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
], {
  x: 10.8, y: 1.0, w: 1.8, h: 0.6,
  align: "center", valign: "middle",
  margin: 0,
});

// Dashed magenta arrow from Input Sample to Target Label
s.addShape(pres.shapes.LINE, {
  x: 2.4, y: 1.3, w: 8.4, h: 0,
  line: { color: MAGENTA_BORDER, width: 1.5, dashType: "dash" },
});
// Arrowhead
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 10.6, y: 1.25, w: 0.3, h: 0.15,
  fill: { color: MAGENTA_BORDER }, line: { color: MAGENTA_BORDER, width: 0.5 },
});

// 5. Neural network diagram (beige panel) - generated image
const diag_meta = require("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_diagram.json");
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_diagram.png",
  x: 0.6, y: 1.9, w: 6.8, h: 3.6,
});

// 6. Vertical dark-red "Error Error Error" bar (to right of diagram)
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.6, y: 2.0, w: 0.3, h: 3.3,
  fill: { color: RED }, line: { color: RED, width: 0 },
});
s.addText("Error Error Error", {
  x: 7.6, y: 2.0, w: 0.3, h: 3.3,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  // Note: pptxgenjs doesn't support rotation directly; use a workaround or pre-rotated image
});

// 7. Class labels (three pale-green boxes) to right of error bar
const class_labels = ["Class 1", "Class 2", "Class m"];
const class_y_positions = [2.3, 3.1, 3.9];
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.1, y: class_y_positions[i], w: 1.2, h: 0.4,
    fill: { color: LIGHT_GREEN_BG }, line: { color: DARK_GREEN, width: 1.5 },
  });
  s.addText(class_labels[i], {
    x: 8.1, y: class_y_positions[i], w: 1.2, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// 8. Legend box (upper right) - beige with red border
const legend_x = 9.5;
const legend_y = 1.9;
const legend_w = 3.5;
const legend_h = 1.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: legend_x, y: legend_y, w: legend_w, h: legend_h,
  fill: { color: LIGHT_BEIGE }, line: { color: RED, width: 1.5 },
});

const legend_items = [
  { symbol: "Net_j", meaning: "Summation at Node j" },
  { symbol: "O_j", meaning: "Output at Node j" },
  { symbol: "w_ji", meaning: "Weight from Node i to Node j" },
];

let legend_text_y = legend_y + 0.15;
for (const item of legend_items) {
  s.addText([
    { text: item.symbol + " ", options: { color: RED, bold: true, italic: true, fontSize: 12, fontFace: FONT } },
    { text: "\u21d2 ", options: { color: BLACK, fontSize: 12, fontFace: FONT } },
    { text: item.meaning, options: { color: BLACK, fontSize: 12, fontFace: FONT } },
  ], {
    x: legend_x + 0.15, y: legend_text_y, w: legend_w - 0.3, h: 0.35,
    align: "left", valign: "top",
    fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
  });
  legend_text_y += 0.35;
}

// 9. Node-count note box (white with red border) below legend
const note_x = 9.5;
const note_y = 3.5;
const note_w = 3.5;
const note_h = 0.8;

s.addShape(pres.shapes.RECTANGLE, {
  x: note_x, y: note_y, w: note_w, h: note_h,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

s.addText([
  { text: "Number of I/P Nodes = Input Vector Length", options: { breakLine: true } },
  { text: "Number of O/P Nodes = Number of classes" },
], {
  x: note_x + 0.15, y: note_y + 0.05, w: note_w - 0.3, h: note_h - 0.1,
  align: "left", valign: "top",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});

// 10. Layer callouts (below diagram panel)
// Previous Layer callout (blue arrow + light blue box)
s.addShape(pres.shapes.DOWN_ARROW, {
  x: 1.5, y: 5.4, w: 0.5, h: 0.4,
  fill: { color: BLUE }, line: { color: BLUE, width: 1.5 },
  flipV: true, // up arrow
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.2, y: 5.8, w: 1.1, h: 0.5,
  fill: { color: LIGHT_BLUE_BG }, line: { color: BLUE, width: 1.5 },
});
s.addText([
  { text: "Previous Layer", options: { fontSize: 11, color: BLACK, fontFace: FONT } },
  { text: "Layer (i)", options: { fontSize: 11, color: BLACK, fontFace: FONT } },
], {
  x: 1.2, y: 5.8, w: 1.1, h: 0.5,
  align: "center", valign: "middle",
  margin: 0,
});

// Current Layer callout (green arrow + light green box)
s.addShape(pres.shapes.DOWN_ARROW, {
  x: 3.5, y: 5.4, w: 0.5, h: 0.4,
  fill: { color: DARK_GREEN }, line: { color: DARK_GREEN, width: 1.5 },
  flipV: true, // up arrow
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.2, y: 5.8, w: 1.1, h: 0.5,
  fill: { color: LIGHT_GREEN_BG2 }, line: { color: DARK_GREEN, width: 1.5 },
});
s.addText([
  { text: "Current Layer", options: { fontSize: 11, color: BLACK, fontFace: FONT } },
  { text: "(You are here)", options: { fontSize: 11, color: BLACK, fontFace: FONT } },
], {
  x: 3.2, y: 5.8, w: 1.1, h: 0.5,
  align: "center", valign: "middle",
  margin: 0,
});

// 11. Bottom formula row (three columns)
// Left: "For Layer \u201cj\u201d" + Net_j summation formula
const left_x = 0.6;
const formula_y = 6.5;
const formula_w = 3.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: left_x, y: formula_y, w: formula_w, h: 0.4,
  fill: { color: WHITE }, line: { color: GRAY, width: 1 },
});
s.addText("For Layer \u201cj\u201d", {
  x: left_x, y: formula_y, w: formula_w, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 12, bold: false, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// Net_j equation image
const eq_net = require("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_equations.json");
const net_eq = eq_net["slide_029_eq_net"][0];
s.addImage({
  path: net_eq.path,
  x: left_x + 0.1, y: formula_y + 0.5, w: net_eq.w_in, h: net_eq.h_in,
});

// Center: Sigmoid formula
const center_x = 4.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: center_x, y: formula_y, w: 3.5, h: 1.1,
  fill: { color: PALE_YELLOW }, line: { color: GRAY, width: 1 },
});

const sigmoid_eq = eq_net["slide_029_eq_sigmoid"][0];
s.addImage({
  path: sigmoid_eq.path,
  x: center_x + 0.1, y: formula_y + 0.15, w: sigmoid_eq.w_in, h: sigmoid_eq.h_in,
});

// Right: "If Layer \u201cj\u201d is Output Layer:" + Error formula
const right_x = 9.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: right_x, y: formula_y, w: 3.8, h: 0.4,
  fill: { color: WHITE }, line: { color: GRAY, width: 1 },
});
s.addText("If Layer \u201cj\u201d is Output Layer:", {
  x: right_x, y: formula_y, w: 3.8, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 12, bold: false, italic: true, color: RED, fontFace: FONT, margin: 0,
});

const error_eq = eq_net["slide_029_eq_error"][0];
s.addImage({
  path: error_eq.path,
  x: right_x + 0.1, y: formula_y + 0.5, w: error_eq.w_in, h: error_eq.h_in,
});

// Write the PPTX
pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_recreated.pptx" 
}).then(() => console.log("wrote slide_029_recreated.pptx"));