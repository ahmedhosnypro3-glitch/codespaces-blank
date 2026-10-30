const pptxgen = require("pptxgenjs");

// Slide 015: Using Two Perceptron Layers with non-Linearity
const NUM = 15;
const TITLE1 = "Using Two Perceptron Layers with";
const TITLE2 = "non-Linearity";
const FONT = "Arial";

const BG = "F2F2F2";  // slide 15 has #f2f2f2 background
const RED = "C00000";
const BLUE = "0000FF";
const GREEN = "008000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFD700";
const CYAN = "00FFFF";
const LIGHT_GREEN = "90EE90";
const PURPLE = "D2B48C";  // tan/brownish for step boxes
const LIGHT_YELLOW = "FFFFE0";

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
  fill: { color: YELLOW }, line: { color: BLACK, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (split red/blue)
// Title starts at y=0.28, x=0.6, w=12.13, centered
s.addText(TITLE1, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText(TITLE2, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ============================================================
// TOP-LEFT: Neural Network Diagram (blue-bordered box)
// Approx from visual_elements: upper-left/center, ~65% width, ~40% height
// Box: x=0.6, y=1.0, w=8.5, h=3.0
// ============================================================
const NN_X = 0.6, NN_Y = 1.0, NN_W = 8.5, NN_H = 3.0;

s.addShape(pres.shapes.RECTANGLE, {
  x: NN_X, y: NN_Y, w: NN_W, h: NN_H,
  fill: { color: WHITE }, line: { color: BLUE, width: 2 },
});

// Network layout
// Input layer: x1 (top), x2 (bottom) on left
const inX = NN_X + 0.5;
const inY1 = NN_Y + 0.5;   // x1
const inY2 = NN_Y + 2.0;   // x2

// Hidden layer: S1 (top), S2 (bottom) in middle
const s1X = NN_X + 2.8;
const s1Y = NN_Y + 0.5;
const s2X = NN_X + 2.8;
const s2Y = NN_Y + 2.0;

// Step boxes Z1, Z2
const z1X = NN_X + 4.8;
const z1Y = NN_Y + 0.3;
const z2X = NN_X + 4.8;
const z2Y = NN_Y + 1.8;

// Output neuron S3
const s3X = NN_X + 6.5;
const s3Y = NN_Y + 1.2;

// Step box Z3/O/P
const z3X = NN_X + 8.0;
const z3Y = NN_Y + 1.0;

// Neuron radius
const nr = 0.3;

// Input labels
s.addText("x\u2081", {
  x: inX, y: inY1, w: 0.4, h: 0.3,
  align: "right", valign: "middle",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("x\u2082", {
  x: inX, y: inY2, w: 0.4, h: 0.3,
  align: "right", valign: "middle",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Hidden neurons S1, S2
s.addShape(pres.shapes.OVAL, {
  x: s1X, y: s1Y, w: nr*2, h: nr*2,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: s1X, y: s1Y, w: nr*2, h: nr*2,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("S\u2081", {
  x: s1X - 0.3, y: s1Y - 0.25, w: 0.5, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

s.addShape(pres.shapes.OVAL, {
  x: s2X, y: s2Y, w: nr*2, h: nr*2,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: s2X, y: s2Y, w: nr*2, h: nr*2,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("S\u2082", {
  x: s2X - 0.3, y: s2Y - 0.25, w: 0.5, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Weights on arrows (with colors)
// x1->S1: -1 (red)
// x1->S2: 1 (blue)
// x2->S1: 1 (red)
// x2->S2: -1 (blue)

s.addText("\u22121", {
  x: inX + 0.6, y: inY1 - 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("1", {
  x: inX + 0.6, y: (inY1 + s2Y) / 2 - 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("1", {
  x: inX + 0.6, y: (s1Y + inY2) / 2 - 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("\u22121", {
  x: inX + 0.6, y: inY2 + 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// Arrows inputs to hidden
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY1 + 0.15, w: s1X - inX - 0.75, h: 0,
  line: { color: RED, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY2 + 0.15, w: s2X - inX - 0.75, h: 0,
  line: { color: BLUE, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY2 + 0.15, w: s1X - inX - 0.75, h: s1Y - inY2 - 0.15,
  line: { color: RED, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: inX + 0.4, y: inY1 + 0.15, w: s2X - inX - 0.75, h: s2Y - inY1 - 0.15,
  line: { color: BLUE, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});

// Step function boxes Z1, Z2 (purple outline)
const stepW = 1.0, stepH = 0.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: z1X, y: z1Y, w: stepW, h: stepH,
  fill: { color: WHITE }, line: { color: PURPLE, width: 1.5 },
});
s.addText([
  { text: ">0.5 \u21d2 1", options: { color: YELLOW, fontSize: 9, fontFace: FONT } },
  { text: "\n", options: { fontSize: 5 } },
  { text: "<0.5 \u21d2 0", options: { color: RED, fontSize: 9, fontFace: FONT } },
], {
  x: z1X, y: z1Y, w: stepW, h: stepH,
  align: "center", valign: "middle", margin: 0,
});
s.addText("Z\u2081", {
  x: z1X + stepW + 0.05, y: z1Y + 0.1, w: 0.4, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

s.addShape(pres.shapes.RECTANGLE, {
  x: z2X, y: z2Y, w: stepW, h: stepH,
  fill: { color: WHITE }, line: { color: PURPLE, width: 1.5 },
});
s.addText([
  { text: "\u2265\u22120.5 \u21d2 1", options: { color: GREEN, fontSize: 9, fontFace: FONT } },
  { text: "\n", options: { fontSize: 5 } },
  { text: "<\u22120.5 \u21d2 0", options: { color: RED, fontSize: 9, fontFace: FONT } },
], {
  x: z2X, y: z2Y, w: stepW, h: stepH,
  align: "center", valign: "middle", margin: 0,
});
s.addText("Z\u2082", {
  x: z2X + stepW + 0.05, y: z2Y + 0.1, w: 0.4, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Arrows S1->Z1, S2->Z2
s.addShape(pres.shapes.LINE, {
  x: s1X + nr, y: s1Y, w: z1X - s1X - nr, h: z1Y + stepH/2 - s1Y,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: s2X + nr, y: s2Y, w: z2X - s2X - nr, h: z2Y + stepH/2 - s2Y,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});

// Weights from Z1, Z2 to S3
s.addText("\u22121", {
  x: z1X + stepW + 0.2, y: z1Y - 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("1", {
  x: z2X + stepW + 0.2, y: z2Y - 0.1, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});

// Output neuron S3
s.addShape(pres.shapes.OVAL, {
  x: s3X, y: s3Y, w: nr*2, h: nr*2,
  fill: { color: WHITE }, line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: s3X, y: s3Y, w: nr*2, h: nr*2,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("S\u2083", {
  x: s3X - 0.3, y: s3Y - 0.25, w: 0.5, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Arrows Z1->S3, Z2->S3
s.addShape(pres.shapes.LINE, {
  x: z1X + stepW, y: z1Y + stepH/2, w: s3X - z1X - stepW, h: s3Y - (z1Y + stepH/2),
  line: { color: RED, width: 1.5, endArrow: "triangle", endArrowSize: "sm" },
});
s.addShape(pres.shapes.LINE, {
  x: z2X + stepW, y: z2Y + stepH/2, w: s3X - z2X - stepW, h: s3Y - (z2Y + stepH/2),
  line: { color: GREEN, width: 1.5, endArrow: "triangle", endArrowSize: "sm" },
});

// Step function box Z3/O/P
s.addShape(pres.shapes.RECTANGLE, {
  x: z3X, y: z3Y, w: stepW, h: stepH,
  fill: { color: WHITE }, line: { color: PURPLE, width: 1.5 },
});
s.addText([
  { text: ">0 \u21d2 1", options: { color: YELLOW, fontSize: 9, fontFace: FONT } },
  { text: "\n", options: { fontSize: 5 } },
  { text: "<0 \u21d2 0", options: { color: RED, fontSize: 9, fontFace: FONT } },
], {
  x: z3X, y: z3Y, w: stepW, h: stepH,
  align: "center", valign: "middle", margin: 0,
});
s.addText("Z\u2083", {
  x: z3X + stepW + 0.05, y: z3Y + 0.1, w: 0.4, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Output
s.addShape(pres.shapes.LINE, {
  x: z3X + stepW, y: z3Y + stepH/2, w: 0.5, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addText("O/P", {
  x: z3X + stepW + 0.6, y: z3Y + 0.1, w: 0.4, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// ============================================================
// TOP-RIGHT: XOR Truth Table (red-bordered box)
// Position: upper-right, x=9.8, y=1.0, w=3.0, h=2.5
// ============================================================
const TT_X = 9.8, TT_Y = 1.0, TT_W = 3.0, TT_H = 2.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: TT_X, y: TT_Y, w: TT_W, h: TT_H,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// Table: 3 cols X1, X2, O/P; 4 rows + header
const cellW = TT_W / 3;
const rowH = 0.35;
const startX = TT_X;
const startY = TT_Y + 0.15;

const headers = ["X\u2081", "X\u2082", "O/P"];
headers.forEach((h, i) => {
  s.addText(h, {
    x: startX + i * cellW, y: startY, w: cellW, h: rowH,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

const rows = [
  { vals: ["0", "0", "0"], fill: CYAN },
  { vals: ["0", "1", "1"], fill: LIGHT_GREEN },
  { vals: ["1", "0", "1"], fill: LIGHT_GREEN },
  { vals: ["1", "1", "0"], fill: CYAN },
];

rows.forEach((row, r) => {
  row.vals.forEach((v, c) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: startX + c * cellW, y: startY + (r + 1) * rowH, w: cellW, h: rowH,
      fill: { color: row.fill }, line: { color: RED, width: 0.75 },
    });
    s.addText(v, {
      x: startX + c * cellW, y: startY + (r + 1) * rowH, w: cellW, h: rowH,
      align: "center", valign: "middle",
      fontSize: 14, color: BLACK, fontFace: FONT, margin: 0,
    });
  });
});

// ============================================================
// BOTTOM: Data Table (red borders, merged header groups)
// Position: bottom-left to center, x=0.6, y=4.2, w=12.0, h=2.0
// Header: x2 | x1 || S1 | Z1 || S2 | Z2 || S3 | Z3
// ============================================================
const DT_X = 0.6, DT_Y = 4.2, DT_W = 12.0, DT_H = 2.0;

s.addShape(pres.shapes.RECTANGLE, {
  x: DT_X, y: DT_Y, w: DT_W, h: DT_H,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// 8 columns
const dtCellW = DT_W / 8;
const dtRowH = 0.35;
const dtStartY = DT_Y + 0.1;

const dtHeaders = ["x\u2082", "x\u2081", "S\u2081", "Z\u2081", "S\u2082", "Z\u2082", "S\u2083", "Z\u2083"];
dtHeaders.forEach((h, i) => {
  s.addText(h, {
    x: DT_X + i * dtCellW, y: dtStartY, w: dtCellW, h: dtRowH,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Add separator lines for merged header groups (visual)
const groupPositions = [2, 4, 6]; // after x1, Z1, Z2
groupPositions.forEach(pos => {
  s.addShape(pres.shapes.LINE, {
    x: DT_X + pos * dtCellW, y: DT_Y, w: 0, h: DT_H,
    line: { color: RED, width: 2 },
  });
});

const dtRows = [
  { vals: ["0", "0", "0", "0", "0", "1", "1", "1"], lastFill: CYAN },
  { vals: ["0", "1", "\u22121", "0", "\u22121", "0", "0", "0"], lastFill: LIGHT_GREEN },
  { vals: ["1", "0", "1", "1", "1", "1", "0", "0"], lastFill: LIGHT_GREEN },
  { vals: ["1", "1", "0", "0", "0", "1", "1", "1"], lastFill: CYAN },
];

dtRows.forEach((row, r) => {
  row.vals.forEach((v, c) => {
    const fill = (c === 7) ? row.lastFill : WHITE;
    s.addShape(pres.shapes.RECTANGLE, {
      x: DT_X + c * dtCellW, y: dtStartY + (r + 1) * dtRowH, w: dtCellW, h: dtRowH,
      fill: { color: fill }, line: { color: RED, width: 0.75 },
    });
    s.addText(v, {
      x: DT_X + c * dtCellW, y: dtStartY + (r + 1) * dtRowH, w: dtCellW, h: dtRowH,
      align: "center", valign: "middle",
      fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
    });
  });
});

// ============================================================
// BOTTOM-RIGHT: Callout Box "Adding Non-Linearity Solves the XOR Problem"
// Position: bottom-right, x=10.0, y=5.5, w=2.8, h=1.2
// ============================================================
const CB_X = 10.0, CB_Y = 5.5, CB_W = 2.8, CB_H = 1.2;

s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: CB_X, y: CB_Y, w: CB_W, h: CB_H,
  fill: { color: LIGHT_YELLOW }, line: { color: BLACK, width: 1 },
});

s.addText("Adding Non-Linearity", {
  x: CB_X + 0.1, y: CB_Y + 0.05, w: CB_W - 0.2, h: 0.35,
  align: "center", valign: "top",
  fontSize: 14, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Solves the", {
  x: CB_X + 0.1, y: CB_Y + 0.38, w: CB_W - 0.2, h: 0.35,
  align: "center", valign: "top",
  fontSize: 14, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "XOR Problem", options: { color: RED, fontSize: 14, bold: true, fontFace: FONT } },
], {
  x: CB_X + 0.1, y: CB_Y + 0.72, w: CB_W - 0.2, h: 0.35,
  align: "center", valign: "top",
  margin: 0,
});

// ============================================================
// 4. Black footer bar (bottom edge)
// ============================================================
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_015_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath));