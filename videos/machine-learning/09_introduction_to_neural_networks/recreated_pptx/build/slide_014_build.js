const pptxgen = require("pptxgenjs");

// Slide 014: Using Two Perceptron Layers
const NUM = 14;
const TITLE = "Using Two Perceptron Layers";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const GREEN = "008000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const PURPLE = "D0B0D0";
const GRAY_BORDER = "808080";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW
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
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// TOP-LEFT: Two-Layer Perceptron Diagram (white box with red border)
// Approx from visual_elements: top-left, ~45% width x 40% height of frame
// Frame: x=0.15, y=0.15, w=13.03, h=7.2
// Box: x=0.6, y=1.0, w=5.8, h=3.0
// ============================================================
const MD_X = 0.6, MD_Y = 1.0, MD_W = 5.8, MD_H = 3.0;

s.addShape(pres.shapes.RECTANGLE, {
  x: MD_X, y: MD_Y, w: MD_W, h: MD_H,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// Diagram layout within the box
// Inputs on left: x1 (top), x2 (bottom)
const inX = MD_X + 0.3;
const inY1 = MD_Y + 0.6;   // x1
const inY2 = MD_Y + 1.8;   // x2

// Three neurons in middle
const n1X = MD_X + 2.0;
const n1Y = MD_Y + 0.5;
const n2X = MD_X + 2.0;
const n2Y = MD_Y + 1.5;
const n3X = MD_X + 3.8;
const n3Y = MD_Y + 1.0;

// Neuron radius
const nr = 0.35;

// Step function box
const stepX = MD_X + 5.0;
const stepY = MD_Y + 0.85;

// Output
const outX = MD_X + 5.5;
const outY = MD_Y + 1.0;

// Input labels
s.addText("x\u2081", {
  x: inX, y: inY1, w: 0.4, h: 0.3,
  align: "right", valign: "middle",
  fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("x\u2082", {
  x: inX, y: inY2, w: 0.4, h: 0.3,
  align: "right", valign: "middle",
  fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Neuron 1 (top)
s.addShape(pres.shapes.OVAL, {
  x: n1X, y: n1Y, w: nr*2, h: nr*2,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: n1X, y: n1Y, w: nr*2, h: nr*2,
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("1", {
  x: n1X - 0.25, y: n1Y - 0.25, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
// Red circle with number 1
s.addShape(pres.shapes.OVAL, {
  x: n1X - 0.25, y: n1Y - 0.25, w: 0.5, h: 0.5,
  fill: { color: RED },
});
s.addText("1", {
  x: n1X - 0.25, y: n1Y - 0.25, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Neuron 2 (bottom)
s.addShape(pres.shapes.OVAL, {
  x: n2X, y: n2Y, w: nr*2, h: nr*2,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: n2X, y: n2Y, w: nr*2, h: nr*2,
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.OVAL, {
  x: n2X - 0.25, y: n2Y - 0.25, w: 0.5, h: 0.5,
  fill: { color: RED },
});
s.addText("2", {
  x: n2X - 0.25, y: n2Y - 0.25, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Neuron 3 (right)
s.addShape(pres.shapes.OVAL, {
  x: n3X, y: n3Y, w: nr*2, h: nr*2,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: n3X, y: n3Y, w: nr*2, h: nr*2,
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.OVAL, {
  x: n3X - 0.25, y: n3Y - 0.25, w: 0.5, h: 0.5,
  fill: { color: RED },
});
s.addText("3", {
  x: n3X - 0.25, y: n3Y - 0.25, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Weight labels on arrows
// x1 -> n1: w11
s.addText("w\u2081\u2081", {
  x: inX + 0.5, y: inY1 - 0.15, w: 0.5, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// x2 -> n1: w12
s.addText("w\u2081\u2082", {
  x: inX + 0.5, y: (inY1 + n1Y) / 2 - 0.1, w: 0.5, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// x1 -> n2: w21
s.addText("w\u2082\u2081", {
  x: inX + 0.5, y: (n1Y + inY2) / 2 - 0.1, w: 0.5, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// x2 -> n2: w22
s.addText("w\u2082\u2082", {
  x: inX + 0.5, y: inY2 + 0.1, w: 0.5, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// n1 -> n3: w31 (green)
s.addText("w\u2083\u2081", {
  x: n1X + 0.6, y: n1Y - 0.1, w: 0.5, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});
// n2 -> n3: w32 (green)
s.addText("w\u2083\u2082", {
  x: n2X + 0.6, y: n2Y - 0.1, w: 0.5, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});

// Arrows from inputs to neurons
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY1 + 0.15, w: n1X - inX - 0.75, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY2 + 0.15, w: n2X - inX - 0.75, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
// Diagonal arrows x2->n1, x1->n2
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY2 + 0.15, w: n1X - inX - 0.75, h: n1Y - inY2 - 0.15,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY1 + 0.15, w: n2X - inX - 0.75, h: n2Y - inY1 - 0.15,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});

// Arrows from neurons 1,2 to neuron 3
s.addShape(pres.shapes.LINE, {
  x: n1X + nr, y: n1Y, w: n3X - n1X - nr, h: n3Y - n1Y,
  line: { color: GREEN, width: 1.5, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: n2X + nr, y: n2Y, w: n3X - n2X - nr, h: n3Y - n2Y,
  line: { color: GREEN, width: 1.5, endArrow: "triangle", endArrowSize: "sm" },
});

// Step function box (purple)
s.addShape(pres.shapes.RECTANGLE, {
  x: stepX, y: stepY, w: 1.0, h: 0.5,
  fill: { color: PURPLE }, line: { color: BLACK, width: 1 },
});
s.addText([
  { text: ">0 \u21d2 1", options: { color: BLACK, fontSize: 10, fontFace: FONT } },
  { text: "\n", options: { fontSize: 6 } },
  { text: "\u22640 \u21d2 0", options: { color: BLACK, fontSize: 10, fontFace: FONT } },
], {
  x: stepX, y: stepY, w: 1.0, h: 0.5,
  align: "center", valign: "middle", margin: 0,
});

// Arrow from neuron 3 to step box
s.addShape(pres.shapes.LINE, {
  x: n3X + nr, y: n3Y, w: stepX - n3X - nr, h: stepY + 0.25 - n3Y,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});

// Output label
s.addShape(pres.shapes.LINE, {
  x: stepX + 1.0, y: stepY + 0.25, w: outX - stepX - 1.0, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addText("O/P", {
  x: outX, y: outY, w: 0.5, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// ============================================================
// BOTTOM-LEFT: Equation Panel (white box with dark gray/blue border)
// Below main diagram: x=0.6, y=4.2, w=5.8, h=1.5
// ============================================================
const EQ_X = 0.6, EQ_Y = 4.2, EQ_W = 5.8, EQ_H = 1.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: EQ_X, y: EQ_Y, w: EQ_W, h: EQ_H,
  fill: { color: WHITE }, line: { color: GRAY_BORDER, width: 1.5 },
});

const eqLines = [
  { text: "Sum 1 = W\u2081\u2081 x\u2081 + W\u2081\u2082 x\u2082", color: RED, bold: true },
  { text: "Sum 2 = W\u2082\u2081 x\u2081 + W\u2082\u2082 x\u2082", color: RED, bold: true },
  { text: "Sum 3 = (W\u2081\u2081 x\u2081 + W\u2081\u2082 x\u2082) w\u2083\u2081 + (W\u2082\u2081 x\u2081 + W\u2082\u2082 x\u2082) w\u2083\u2082", color: BLACK, bold: true },
  { text: "= (W\u2081\u2081 w\u2083\u2081 + W\u2082\u2081 w\u2083\u2082)x\u2081 + (W\u2081\u2082 w\u2083\u2081 + W\u2082\u2082 w\u2083\u2082)x\u2082", color: BLACK, bold: true },
  { text: "= W'\u2081 x\u2081 + W'\u2082 x\u2082 \u21d2 Still Linear Equation", color: BLUE, bold: true, italic: true, underline: true },
];

eqLines.forEach((line, i) => {
  s.addText(line.text, {
    x: EQ_X + 0.15, y: EQ_Y + 0.1 + i * 0.28, w: EQ_W - 0.3, h: 0.28,
    align: "left", valign: "top",
    fontSize: 13, bold: line.bold || false, color: line.color, fontFace: FONT,
    italic: line.italic || false, underline: line.underline || false, margin: 0,
  });
});

// ============================================================
// BOTTOM-RIGHT: Single Perceptron Diagram (yellow box)
// Position: bottom-right, roughly x=7.0 to x=12.0, y=4.5 to y=6.5
// ============================================================
const SD_X = 7.0, SD_Y = 4.5, SD_W = 5.0, SD_H = 2.0;

s.addShape(pres.shapes.RECTANGLE, {
  x: SD_X, y: SD_Y, w: SD_W, h: SD_H,
  fill: { color: WHITE }, line: { color: YELLOW, width: 2 },
});

// Single perceptron inside yellow box
const sinX = SD_X + 0.3;
const sinY1 = SD_Y + 0.4;
const sinY2 = SD_Y + 1.2;
const sigmaX = SD_X + 2.0;
const sigmaY = SD_Y + 0.8;
const stepX2 = SD_X + 3.5;
const stepY2 = SD_Y + 0.65;
const outX2 = SD_X + 4.5;
const outY2 = SD_Y + 0.75;

// Inputs x1, x2
s.addText("x\u2081", {
  x: sinX, y: sinY1, w: 0.4, h: 0.3,
  align: "right", valign: "middle",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("x\u2082", {
  x: sinX, y: sinY2, w: 0.4, h: 0.3,
  align: "right", valign: "middle",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Weights
s.addText("w\u2081", {
  x: sinX + 0.5, y: sinY1 - 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("w\u2082", {
  x: sinX + 0.5, y: sinY2 - 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Arrows to sigma
s.addShape(pres.shapes.LINE, {
  x: sinX + 0.4, y: sinY1 + 0.15, w: sigmaX - sinX - 0.75, h: sigmaY - sinY1 - 0.15,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: sinX + 0.4, y: sinY2 + 0.15, w: sigmaX - sinX - 0.75, h: sigmaY - sinY2 - 0.15,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});

// Sigma circle
s.addShape(pres.shapes.OVAL, {
  x: sigmaX, y: sigmaY, w: 0.5, h: 0.5,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: sigmaX, y: sigmaY, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Step function box
s.addShape(pres.shapes.RECTANGLE, {
  x: stepX2, y: stepY2, w: 0.8, h: 0.5,
  fill: { color: PURPLE }, line: { color: BLACK, width: 1 },
});
s.addText([
  { text: ">0 \u21d2 1", options: { color: BLACK, fontSize: 9, fontFace: FONT } },
  { text: "\n", options: { fontSize: 6 } },
  { text: "\u22640 \u21d2 0", options: { color: BLACK, fontSize: 9, fontFace: FONT } },
], {
  x: stepX2, y: stepY2, w: 0.8, h: 0.5,
  align: "center", valign: "middle", margin: 0,
});

// Arrow sigma to step
s.addShape(pres.shapes.LINE, {
  x: sigmaX + 0.25, y: sigmaY + 0.25, w: stepX2 - sigmaX - 0.25, h: stepY2 + 0.25 - sigmaY - 0.25,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});

// Output
s.addShape(pres.shapes.LINE, {
  x: stepX2 + 0.8, y: stepY2 + 0.25, w: outX2 - stepX2 - 0.8, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addText("O/P", {
  x: outX2, y: outY2, w: 0.4, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// ============================================================
// 4. Black footer bar (bottom edge)
// ============================================================
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK },
});

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_014_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath));