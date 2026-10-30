const pptxgen = require("pptxgenjs");

// Slide 010: Classification of "AND" Truth Table
const NUM = 10;
const TITLE = 'Classification of \u201cAND\u201d Truth Table';
const FONT = "Arial";

const BG = "E8E8E8";
const DARK_RED = "C00000";
const BLACK = "000000";
const RED = "FF0000";
const BLUE = "0000FF";
const DARK_BLUE = "000080";  // dark navy for decision line
const GREEN = "00B050";
const CYAN = "00FFFF";
const LIGHT_CYAN = "B0E0E6";
const LIGHT_GREEN = "90EE90";
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
// Original: table box at x:96-336, y:135-297 (960x540)
// In inches (13.33x7.5): x=1.33, y=1.88, w=3.33, h=2.25
// But using house frame coords: x=0.15, y=0.15
// Table: x=0.15+1.33=1.48, y=0.15+1.88=2.03
// Let's use TT_X = 0.8, TT_Y = 1.2, TT_W = 4.5, TT_H = 1.8 (tighter)
// ============================================================
const TT_X = 0.8, TT_Y = 1.2, TT_W = 4.8, TT_H = 1.8;

// White box with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: TT_X, y: TT_Y, w: TT_W, h: TT_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Truth table headers and rows - 3 columns, 4 data rows + header
const cellW = TT_W / 3;
const rowH = 0.32;
const startX = TT_X + 0.1;
const startY = TT_Y + 0.05;

// Headers
const headers = ["X\u2081", "X\u2082", "O/P"];
headers.forEach((h, i) => {
  s.addText(h, {
    x: startX + i * cellW, y: startY, w: cellW, h: rowH,
    align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Data rows - only O/P column highlighted as narrow rounded chips
const rows = [
  { vals: ["0", "0", "0"], opColor: LIGHT_CYAN },
  { vals: ["0", "1", "0"], opColor: LIGHT_CYAN },
  { vals: ["1", "0", "0"], opColor: LIGHT_CYAN },
  { vals: ["1", "1", "1"], opColor: LIGHT_GREEN },
];

rows.forEach((row, r) => {
  row.vals.forEach((v, c) => {
    // Cell border
    s.addShape(pres.shapes.RECTANGLE, {
      x: startX + c * cellW, y: startY + (r + 1) * rowH, w: cellW, h: rowH,
      fill: { color: WHITE },
      line: { color: DARK_RED, width: 0.5 },
    });
    // O/P column gets a rounded highlight chip centered in cell
    if (c === 2) {
      const chipW = cellW * 0.6;
      const chipH = rowH * 0.7;
      const chipX = startX + c * cellW + (cellW - chipW) / 2;
      const chipY = startY + (r + 1) * rowH + (rowH - chipH) / 2;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: chipX, y: chipY, w: chipW, h: chipH,
        fill: { color: row.opColor },
      });
    }
    s.addText(v, {
      x: startX + c * cellW, y: startY + (r + 1) * rowH, w: cellW, h: rowH,
      align: "center", valign: "middle",
      fontSize: 13, color: BLACK, fontFace: FONT, margin: 0,
    });
  });
});

// ============================================================
// TOP-RIGHT: 2D Decision Boundary Plot
// Original: plot at x:528-844, y:108-351 (960x540)
// In inches: x=7.33, y=1.5, w=4.4, h=3.38
// Plot panel with dark red border and axes
// ============================================================
const PL_X = 6.2, PL_Y = 1.0, PL_W = 5.2, PL_H = 3.2;

// White box with DARK RED border for plot area
s.addShape(pres.shapes.RECTANGLE, {
  x: PL_X, y: PL_Y, w: PL_W, h: PL_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Axes - DARK RED with LARGE arrowheads
// Plot inner margins
const marginL = 0.7;
const marginB = 0.5;
const marginT = 0.4;
const marginR = 0.4;

const axisX = PL_X + marginL;
const axisY0 = PL_Y + PL_H - marginB;  // bottom
const axisY1 = PL_Y + 0.15;            // top - extend to near panel top
const axisX1 = PL_X + PL_W - marginR;  // right - extend to near panel right

// Y-axis line with LARGE arrow - DARK RED, extends to panel top
s.addShape(pres.shapes.LINE, {
  x: axisX, y: axisY1, w: 0, h: axisY0 - axisY1,
  line: { color: DARK_RED, width: 2, endArrow: "triangle", endArrowSize: "lg" },
});

// X-axis line with LARGE arrow - DARK RED, extends past x-intercept
s.addShape(pres.shapes.LINE, {
  x: axisX, y: axisY0, w: axisX1 - axisX, h: 0,
  line: { color: DARK_RED, width: 2, endArrow: "triangle", endArrowSize: "lg" },
});

// Axis labels
// "2" at mid-height of y-axis, LEFT of axis, RED
s.addText("2", {
  x: axisX - 0.4, y: axisY0 - (axisY0 - axisY1) / 2 - 0.05, w: 0.35, h: 0.25,
  align: "right", valign: "middle",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// "x1" at far right past the axis arrow, RED per original
s.addText("x\u2081", {
  x: axisX1 + 0.05, y: axisY0 - 0.35, w: 0.4, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Decision boundary line (DARK NAVY, thick)
// Equation: d(X) = -5x1 - 3x2 + 6 = 0 => x2 = (-5/3)x1 + 2
// Line starts AT the y-axis intercept (0, 2) and runs to x-intercept (1.2, 0)
const pw = axisX1 - axisX;
const ph = axisY0 - axisY1;

// Start: exactly at y-axis (x=0), y=2 (the intercept marked by red "2")
// End: x=1.2, y=0 (x-intercept) - but line runs PAST the x-intercept
const lineStartX = 0;
const lineStartY = 2.0;
const lineEndX = 1.35;  // past the x-intercept at 1.2
const lineEndY = -0.05; // slightly below axis

const lx1 = axisX + (lineStartX / 1.2) * pw;
const ly1 = axisY0 - (lineStartY / 2.0) * ph;
const lx2 = axisX + (lineEndX / 1.2) * pw;
const ly2 = axisY0 - (lineEndY / 2.0) * ph;

s.addShape(pres.shapes.LINE, {
  x: lx1, y: ly1, w: lx2 - lx1, h: ly2 - ly1,
  line: { color: DARK_BLUE, width: 3 },
});

// Sample points (cyan for class 0, green for class 1)
// Original: cyan at origin, cyan at mid-y-axis, cyan at x-intercept, green above line
const pts = [
  { x: 0, y: 0, color: CYAN },       // origin
  { x: 0.05, y: 1.0, color: CYAN },  // mid-y-axis (near axis)
  { x: 1.2, y: 0, color: CYAN },     // x-intercept
  { x: 0.9, y: 0.7, color: GREEN },  // above line (class 1)
];

pts.forEach(pt => {
  const px = axisX + (pt.x / 1.2) * pw;
  const py = axisY0 - (pt.y / 2.0) * ph;
  s.addShape(pres.shapes.OVAL, {
    x: px - 0.07, y: py - 0.07, w: 0.14, h: 0.14,
    fill: { color: pt.color },
    line: { color: BLACK, width: 0.5 },
  });
});

// Red label "1.2" just BELOW x-intercept
s.addText("1.2", {
  x: lx2 - 0.15, y: axisY0 + 0.05, w: 0.3, h: 0.2,
  align: "center", valign: "top",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// BOTTOM-LEFT: Perceptron/Neural Network Diagram
// Original: x:144-499, y:351-486 (960x540)
// In inches: x=2.0, y=4.88, w=4.9, h=1.88
// ============================================================
const NN_X = 1.0, NN_Y = 4.6, NN_W = 6.5, NN_H = 2.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: NN_X, y: NN_Y, w: NN_W, h: NN_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Perceptron diagram - inline label/weight arrangement
// Inputs: x1 (-5 blue), x2 (-3 blue), 1 (bias: 1 red, weight 6 blue)
// All on same horizontal line: label then weight right next to it
// Converging to Σ circle
// Then step function box with ⇒ arrows
// Then O/P

const inY = [NN_Y + 0.35, NN_Y + 1.1, NN_Y + 1.85];
const inX = NN_X + 0.3;
const sumX = NN_X + 3.0;
const sumY = NN_Y + 1.25;
const stepX = NN_X + 4.5;
const stepY = NN_Y + 1.0;
const outX = NN_X + 5.8;
const outY = NN_Y + 1.1;

const inputs = [
  { label: "x\u2081", weight: "-5", y: inY[0], labelColor: BLACK, weightColor: BLUE },
  { label: "x\u2082", weight: "-3", y: inY[1], labelColor: BLACK, weightColor: BLUE },
  { label: "1", weight: "6", y: inY[2], labelColor: RED, weightColor: BLUE },  // bias: label red, weight blue
];

inputs.forEach(inp => {
  // Input label and weight INLINE (label then weight immediately to the right)
  s.addText(inp.label, {
    x: inX, y: inp.y, w: 0.35, h: 0.25,
    align: "right", valign: "middle",
    fontSize: 12, bold: true, color: inp.labelColor, fontFace: FONT, margin: 0,
  });
  s.addText(inp.weight, {
    x: inX + 0.4, y: inp.y, w: 0.4, h: 0.25,
    align: "left", valign: "middle",
    fontSize: 12, bold: true, color: inp.weightColor, fontFace: FONT, margin: 0,
  });
  // Arrow from weight to summation (diagonal converging)
  s.addShape(pres.shapes.LINE, {
    x: inX + 0.85, y: inp.y + 0.12, w: sumX - inX - 1.0, h: sumY - inp.y - 0.12,
    line: { color: DARK_RED, width: 1.5, endArrow: "triangle", endArrowSize: "med" },
  });
});

// Summation circle (Σ) - LIGHT CYAN fill, BLACK outline
s.addShape(pres.shapes.OVAL, {
  x: sumX, y: sumY, w: 0.5, h: 0.5,
  fill: { color: LIGHT_CYAN },
  line: { color: BLACK, width: 2 },
});
s.addText("\u03a3", {
  x: sumX, y: sumY, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 22, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Arrow from Σ to step function - RED
s.addShape(pres.shapes.LINE, {
  x: sumX + 0.5, y: sumY + 0.2, w: stepX - sumX - 0.5, h: stepY + 0.2 - sumY - 0.2,
  line: { color: DARK_RED, width: 1.5, endArrow: "triangle", endArrowSize: "med" },
});

// Step function box - SMALL square, pale outlined (no fill)
const stepBoxW = 0.4;
const stepBoxH = 0.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: stepX, y: stepY, w: stepBoxW, h: stepBoxH,
  fill: { color: WHITE },
  line: { color: BLACK, width: 1.5 },
});
// Internal step glyph - outlined staircase shape (pale, no fill)
// Step: horizontal line then vertical line (staircase)
s.addShape(pres.shapes.LINE, {
  x: stepX + 0.08, y: stepY + 0.22, w: 0.12, h: 0,
  line: { color: BLACK, width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: stepX + 0.2, y: stepY + 0.1, w: 0, h: 0.12,
  line: { color: BLACK, width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: stepX + 0.2, y: stepY + 0.1, w: 0.12, h: 0,
  line: { color: BLACK, width: 1.5 },
});

// Text OUTSIDE to the right: >0 ⇒ 1 / <0 ⇒ 0
s.addText(">0 \u21d2 1", {
  x: stepX + stepBoxW + 0.05, y: stepY - 0.05, w: 0.8, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("<0 \u21d2 0", {
  x: stepX + stepBoxW + 0.05, y: stepY + 0.2, w: 0.8, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// Arrow from step box to O/P - RED, with a visible ⇒ arrow glyph
s.addShape(pres.shapes.LINE, {
  x: stepX + stepBoxW + 0.85, y: stepY + 0.2, w: outX - stepX - stepBoxW - 0.85, h: 0,
  line: { color: DARK_RED, width: 1.5, endArrow: "triangle", endArrowSize: "med" },
});
// Explicit ⇒ arrow glyph in the connector
s.addText("\u21d2", {
  x: stepX + stepBoxW + 0.85, y: stepY + 0.02, w: 0.3, h: 0.25,
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});
s.addText("O/P", {
  x: outX, y: outY, w: 0.4, h: 0.25,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// ============================================================
// BOTTOM-RIGHT: Equation Box (peach with red border)
// Original: x:566-806, y:421-475 (960x540)
// In inches: x=7.86, y=5.88, w=3.33, h=0.75
// ============================================================
const EQ_X = 7.5, EQ_Y = 5.6, EQ_W = 3.8, EQ_H = 0.7;

s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: EQ_X, y: EQ_Y, w: EQ_W, h: EQ_H,
  fill: { color: PEACH },
  line: { color: DARK_RED, width: 1.5 },
});

// Embed the equation PNG
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