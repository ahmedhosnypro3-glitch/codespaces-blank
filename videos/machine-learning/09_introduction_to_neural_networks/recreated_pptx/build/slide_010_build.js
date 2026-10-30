const pptxgen = require("pptxgenjs");

// Slide 010: Classification of "AND" Truth Table
const NUM = 10;
const TITLE = 'Classification of \u201cAND\u201d Truth Table';
const FONT = "Arial";

const BG = "E8E8E8";
const BORDER_RED = "8B0000";
const BLACK = "000000";
const RED = "FF0000";
const DARK_RED = "C00000";
const GREEN = "00B050";
const BLUE = "0000FF";
const CYAN = "00FFFF";
const PEACH = "FFE4C4";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: DARK_RED, width: 1.5 },
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
  fontSize: 28, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});

// ============================================================
// TOP-LEFT: Truth Table with red border
// Approx position from visual_elements: x:10-35%, y:25-55%
// Frame: x=0.15, y=0.15, w=13.03, h=7.2
// So table: x=0.15+1.3=1.45, y=0.15+1.8=1.95, w=3.25, h=2.16
// Using box at x=0.6, y=1.0, w=4.5, h=2.5 with red border
// ============================================================
const TT_X = 0.6, TT_Y = 1.0, TT_W = 5.0, TT_H = 2.0;

// White box with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: TT_X, y: TT_Y, w: TT_W, h: TT_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Truth table headers and rows
// 3 columns: X1, X2, O/P
// 4 data rows - ORIGINAL ONLY COLORS THE O/P COLUMN (3rd column)
const cellW = TT_W / 3;
const rowH = 0.35;
const startX = TT_X;
const startY = TT_Y + 0.1;

// Headers
const headers = ["X\u2081", "X\u2082", "O/P"];
headers.forEach((h, i) => {
  s.addText(h, {
    x: startX + i * cellW, y: startY, w: cellW, h: rowH,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Data rows - only O/P column colored
const rows = [
  { vals: ["0", "0", "0"], opFill: "#B0E0E6" },  // cyan O/P
  { vals: ["0", "1", "0"], opFill: "#B0E0E6" },  // cyan O/P
  { vals: ["1", "0", "0"], opFill: "#B0E0E6" },  // cyan O/P
  { vals: ["1", "1", "1"], opFill: "#90EE90" },  // green O/P
];

rows.forEach((row, r) => {
  row.vals.forEach((v, c) => {
    // Only fill O/P column (c=2)
    const fillColor = (c === 2) ? row.opFill : WHITE;
    s.addShape(pres.shapes.RECTANGLE, {
      x: startX + c * cellW, y: startY + (r + 1) * rowH, w: cellW, h: rowH,
      fill: { color: fillColor },
      line: { color: DARK_RED, width: 0.5 },
    });
    s.addText(v, {
      x: startX + c * cellW, y: startY + (r + 1) * rowH, w: cellW, h: rowH,
      align: "center", valign: "middle",
      fontSize: 14, color: BLACK, fontFace: FONT, margin: 0,
    });
  });
});

// ============================================================
// TOP-RIGHT: 2D Decision Boundary Plot
// Approx: x:55-88%, y:20-65% of frame
// Plot area: x=7.2, y=1.0, w=4.5, h=3.5
// ============================================================
const PL_X = 6.5, PL_Y = 1.0, PL_W = 5.8, PL_H = 3.5;

// White box with red border for plot area
s.addShape(pres.shapes.RECTANGLE, {
  x: PL_X, y: PL_Y, w: PL_W, h: PL_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Axes - draw using lines with LARGE arrowheads
// Y-axis: left edge + 0.5in, from bottom to top
const axisX = PL_X + 0.6;
const axisY0 = PL_Y + PL_H - 0.4;  // bottom
const axisY1 = PL_Y + 0.3;         // top
const axisX1 = PL_X + PL_W - 0.3;  // right

// Y-axis line with LARGE arrow
s.addShape(pres.shapes.LINE, {
  x: axisX, y: axisY1, w: 0, h: axisY0 - axisY1,
  line: { color: BLACK, width: 2, endArrow: "triangle", endArrowSize: "lg" },
});
// Y-axis label "2" near top - RED per original
s.addText("2", {
  x: axisX - 0.35, y: axisY1 + 0.05, w: 0.3, h: 0.25,
  align: "right", valign: "middle",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// X-axis line with LARGE arrow
s.addShape(pres.shapes.LINE, {
  x: axisX, y: axisY0, w: axisX1 - axisX, h: 0,
  line: { color: BLACK, width: 2, endArrow: "triangle", endArrowSize: "lg" },
});
// X-axis label "x1" as axis title at far right
s.addText("x\u2081", {
  x: axisX1 - 0.3, y: axisY0 + 0.15, w: 0.4, h: 0.25,
  align: "center", valign: "top",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});

// Decision boundary line (dark blue, descending)
// Equation: d(X) = -5x1 - 3x2 + 6 = 0 => x2 = (-5/3)x1 + 2
// At x1=0: x2=2; At x2=0: x1=1.2
// Line from y-axis (x=0, y=2) to x-axis (x=1.2, y=0)
const pw = PL_W - 0.9;
const ph = PL_H - 0.7;
const p0x = axisX;
const p0y = axisY0;

// Line from (x1=0, x2=2) to (x1=1.2, x2=0)
// Start at y-axis intercept, not at a data point
const lx1 = p0x;  // x=0 at y-axis
const ly1 = p0y - (2.0/2.0) * ph;  // x2=2 -> top (y-axis intercept)
const lx2 = p0x + (1.2/1.2) * pw;  // x=1.2 -> right (x-axis intercept)
const ly2 = p0y;  // x2=0 -> bottom

s.addShape(pres.shapes.LINE, {
  x: lx1, y: ly1, w: lx2 - lx1, h: ly2 - ly1,
  line: { color: BLUE, width: 2 },
});

// Cyan points (class 0): (0,0), (1,0) - NO point at (0,2) per original
// Green point (class 1): (1,1)
const pts = [
  { x: 0, y: 0, color: CYAN },   // origin
  { x: 1, y: 0, color: CYAN },   // x-axis right
  { x: 1, y: 1, color: GREEN },  // above line
];

pts.forEach(pt => {
  const px = p0x + (pt.x / 1.2) * pw;
  const py = p0y - (pt.y / 2.0) * ph;
  s.addShape(pres.shapes.OVAL, {
    x: px - 0.08, y: py - 0.08, w: 0.16, h: 0.16,
    fill: { color: pt.color },
    line: { color: BLACK, width: 0.5 },
  });
});

// Red label "1.2" near x-axis at x=1.2 intercept
s.addText("1.2", {
  x: lx2 - 0.2, y: axisY0 + 0.05, w: 0.4, h: 0.2,
  align: "center", valign: "top",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// BOTTOM-LEFT: Perceptron/Neural Network Diagram
// Approx: x:15-52%, y:65-90%
// Box: x=1.0, y=4.6, w=6.0, h=2.5
// ============================================================
const NN_X = 1.0, NN_Y = 4.6, NN_W = 6.5, NN_H = 2.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: NN_X, y: NN_Y, w: NN_W, h: NN_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Perceptron diagram elements
// Inputs on left: x1 (-5), x2 (-3), bias 1 (6 in red)
// Summation circle in middle
// Step function box
// Output on right

const inY = [NN_Y + 0.3, NN_Y + 1.0, NN_Y + 1.7];  // three inputs
const inX = NN_X + 0.3;
const sumX = NN_X + 2.5;
const sumY = NN_Y + 1.25;
const stepX = NN_X + 4.0;
const stepY = NN_Y + 1.0;
const outX = NN_X + 5.5;
const outY = NN_Y + 1.1;

// Input labels and weights
const inputs = [
  { label: "x\u2081", weight: "-5", y: inY[0] },
  { label: "x\u2082", weight: "-3", y: inY[1] },
  { label: "1", weight: "6", y: inY[2], weightColor: BLUE },  // Blue per original
];

inputs.forEach(inp => {
  // Input label
  s.addText(inp.label, {
    x: inX, y: inp.y, w: 0.4, h: 0.25,
    align: "right", valign: "middle",
    fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
  });
  // Weight
  s.addText(inp.weight, {
    x: inX + 0.5, y: inp.y, w: 0.5, h: 0.25,
    align: "left", valign: "middle",
    fontSize: 12, bold: true, color: inp.weightColor || BLACK, fontFace: FONT, margin: 0,
  });
  // Arrow to summation
  s.addShape(pres.shapes.LINE, {
    x: inX + 0.9, y: inp.y + 0.12, w: sumX - inX - 1.0, h: sumY - inp.y - 0.12,
    line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
  });
});

// Summation circle (Σ)
s.addShape(pres.shapes.OVAL, {
  x: sumX, y: sumY, w: 0.5, h: 0.5,
  fill: { color: WHITE },
  line: { color: BLACK, width: 1.5 },
});
s.addText("\u03a3", {
  x: sumX, y: sumY, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Arrow from sum to step function
s.addShape(pres.shapes.LINE, {
  x: sumX + 0.5, y: sumY + 0.25, w: stepX - sumX - 0.5, h: stepY + 0.3 - sumY - 0.25,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});

// Step function box - piecewise/bracket style per original
// Draw a left bracket/brace shape
s.addShape(pres.shapes.RECTANGLE, {
  x: stepX, y: stepY, w: 1.2, h: 0.6,
  fill: { color: WHITE },
  line: { color: BLACK, width: 1 },
});
// Left bracket using lines
s.addShape(pres.shapes.LINE, {
  x: stepX, y: stepY, w: 0, h: 0.6,
  line: { color: BLACK, width: 2 },
});
s.addShape(pres.shapes.LINE, {
  x: stepX, y: stepY, w: 0.1, h: 0,
  line: { color: BLACK, width: 2 },
});
s.addShape(pres.shapes.LINE, {
  x: stepX, y: stepY + 0.6, w: 0.1, h: 0,
  line: { color: BLACK, width: 2 },
});
// Text inside bracket
s.addText([
  { text: ">0 \u21d2 1", options: { color: BLACK, fontSize: 9, fontFace: FONT } },
  { text: "\n", options: { fontSize: 6 } },
  { text: "<0 \u21d2 0", options: { color: BLACK, fontSize: 9, fontFace: FONT } },
], {
  x: stepX + 0.15, y: stepY, w: 1.0, h: 0.6,
  align: "left", valign: "middle", margin: 0,
});

// Output label
s.addShape(pres.shapes.LINE, {
  x: stepX + 1.2, y: stepY + 0.3, w: outX - stepX - 1.2, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "sm" },
});
s.addText("O/P", {
  x: outX, y: outY, w: 0.4, h: 0.25,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// ============================================================
// BOTTOM-RIGHT: Equation Box (peach with red border)
// Approx: x:59-84%, y:78-88%
// Box: x=7.7, y=5.6, w=3.5, h=0.7
// ============================================================
const EQ_X = 7.5, EQ_Y = 5.6, EQ_W = 3.8, EQ_H = 0.7;

s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: EQ_X, y: EQ_Y, w: EQ_W, h: EQ_H,
  fill: { color: PEACH },
  line: { color: DARK_RED, width: 1.5 },
});

// Embed the equation PNG
// Equation: d(X) = -5 x1 - 3 x2 + 6
// From render: w_in=2.66333, h_in=0.25333, baseline_frac=0.79605
// Place it centered in the peach box
const eqImg = {
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_010_eq.png",
  w_in: 2.66333,
  h_in: 0.25333,
  baseline_frac: 0.79605,
};
const imgX = EQ_X + (EQ_W - eqImg.w_in) / 2;
const imgY = EQ_Y + (EQ_H - eqImg.h_in) / 2;
s.addImage({
  path: eqImg.path,
  x: imgX, y: imgY, w: eqImg.w_in, h: eqImg.h_in,
});

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_010_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath));