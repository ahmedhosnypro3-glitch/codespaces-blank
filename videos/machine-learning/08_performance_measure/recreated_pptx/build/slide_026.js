const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const RED2 = "D32F2F";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "1565C0";
const BLUE_DARK = "0000FF";
const GREEN = "4CAF50";
const PURPLE = "9C27B0";
const WHITE = "FFFFFF";
const LIGHT_KHAKI = "F0E68C";
const DARK_RED = "8B0000";
const LIGHT_GREEN = "90EE90";
const BLACK = "212121";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("26", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});

// ============================================================
// SLIDE 26 CONTENT
// ============================================================

// LEFT SIDE: Legend matrix, threshold box, numeric matrix
const leftX = 0.6;
const leftW = 3.5;
const cellW = 0.7, cellH = 0.45;
const headerH = 0.35;
const labelW = 0.6;

let yPos = 1.3;

// 1. Confusion matrix legend (TP/FN/FP/TN)
s.addText("Predicted as", {
  x: leftX + labelW, y: yPos, w: cellW * 2, h: headerH,
  fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0,
});
s.addText("P", { x: leftX + labelW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: leftX + labelW + cellW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: leftX, y: yPos + headerH, w: labelW, h: cellH * 2, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: leftX, y: yPos + headerH, w: labelW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: leftX, y: yPos + headerH + cellH, w: labelW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW, y: yPos + headerH, w: cellW * 2, h: cellH * 2, fill: { color: WHITE }, line: { color: BLUE, width: 1.5 } });
// Cells: TP, FN / FP, TN (note: different arrangement from slide 25)
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW, y: yPos + headerH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("TP", { x: leftX + labelW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW + cellW, y: yPos + headerH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("FN", { x: leftX + labelW + cellW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW, y: yPos + headerH + cellH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("FP", { x: leftX + labelW, y: yPos + headerH + cellH, w: cellW, h: cellH, fontSize: 11, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW + cellW, y: yPos + headerH + cellH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("TN", { x: leftX + labelW + cellW, y: yPos + headerH + cellH, w: cellW, h: cellH, fontSize: 11, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// 2. Threshold box
yPos += headerH + cellH * 2 + 0.15;
s.addShape(pptx.shapes.RECTANGLE, { x: leftX, y: yPos, w: leftW, h: 0.5, fill: { color: WHITE }, line: { color: DARK_RED, width: 1.5 } });
s.addText("Threshold=0.7", { x: leftX, y: yPos, w: leftW, h: 0.5, fontSize: 14, bold: true, color: DARK_RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// 3. Numeric confusion matrix (3, 2, 0, 6)
yPos += 0.65;
s.addText("Predicted as", { x: leftX + labelW, y: yPos, w: cellW * 2, h: headerH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0 });
s.addText("P", { x: leftX + labelW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: leftX + labelW + cellW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: leftX, y: yPos + headerH, w: labelW, h: cellH * 2, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: leftX, y: yPos + headerH, w: labelW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: leftX, y: yPos + headerH + cellH, w: labelW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW, y: yPos + headerH, w: cellW * 2, h: cellH * 2, fill: { color: WHITE }, line: { color: BLUE, width: 1.5 } });
// Cells with colored numbers: 3(blue), 2(red) / 0(black), 6(red)
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW, y: yPos + headerH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("3", { x: leftX + labelW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, bold: true, color: BLUE_DARK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW + cellW, y: yPos + headerH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("2", { x: leftX + labelW + cellW, y: yPos + headerH, w: cellW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW, y: yPos + headerH + cellH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("0", { x: leftX + labelW, y: yPos + headerH + cellH, w: cellW, h: cellH, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + labelW + cellW, y: yPos + headerH + cellH, w: cellW, h: cellH, fill: { color: WHITE }, line: { color: BLACK, width: 0.5 } });
s.addText("6", { x: leftX + labelW + cellW, y: yPos + headerH + cellH, w: cellW, h: cellH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// RIGHT SIDE: Flowchart
// ============================================================
const flowX = 4.5;
const flowY = 1.5;
const boxW = 1.4, boxH = 0.5;
const arrowW = 0.4;

// Test Sample
s.addShape(pptx.shapes.RECTANGLE, { x: flowX, y: flowY, w: boxW, h: boxH, fill: { color: WHITE }, line: { color: BLACK, width: 1 } });
s.addText("Test Sample", { x: flowX, y: flowY, w: boxW, h: boxH, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: flowX + boxW - 0.2, y: flowY + 0.1, w: 0.18, h: 0.3, fill: { color: BLACK } });

// Arrow
s.addShape(pptx.shapes.RIGHT_ARROW, { x: flowX + boxW, y: flowY + 0.1, w: arrowW, h: 0.3, fill: { color: BLACK } });

// Model box (dark red)
const modelX = flowX + boxW + arrowW;
s.addShape(pptx.shapes.RECTANGLE, { x: modelX, y: flowY - 0.1, w: 1.8, h: 0.7, fill: { color: DARK_RED } });
s.addText("Model [Any value] - (0, +∞)", { x: modelX, y: flowY + 0.05, w: 1.8, h: 0.6, fontSize: 11, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Bell curve circle
s.addShape(pptx.shapes.OVAL, { x: modelX + 1.8 + 0.15, y: flowY + 0.05, w: 0.5, h: 0.5, fill: { color: PURPLE }, line: { color: PURPLE, width: 1 } });
s.addText("∿", { x: modelX + 1.8 + 0.15, y: flowY + 0.05, w: 0.5, h: 0.5, fontSize: 18, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Arrow
s.addShape(pptx.shapes.RIGHT_ARROW, { x: modelX + 1.8 + 0.7, y: flowY + 0.2, w: arrowW, h: 0.3, fill: { color: BLACK } });

// Predicted Value box (blue border)
const predX = modelX + 1.8 + 0.7 + arrowW;
s.addShape(pptx.shapes.RECTANGLE, { x: predX, y: flowY, w: 1.6, h: boxH, fill: { color: WHITE }, line: { color: BLUE, width: 1.5 } });
s.addText("Predicted Value (0 --- 1)", { x: predX, y: flowY, w: 1.6, h: boxH, fontSize: 11, bold: true, color: BLUE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Arrow
s.addShape(pptx.shapes.RIGHT_ARROW, { x: predX + 1.6, y: flowY + 0.1, w: arrowW, h: 0.3, fill: { color: BLACK } });

// Threshold box (red border)
const threshX = predX + 1.6 + arrowW;
s.addShape(pptx.shapes.RECTANGLE, { x: threshX, y: flowY, w: 1.6, h: boxH, fill: { color: WHITE }, line: { color: RED2, width: 1.5 } });
s.addText("Threshold (e.g. 0.5)", { x: threshX, y: flowY, w: 1.6, h: boxH, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Arrow split
const splitX = threshX + 1.6;
s.addShape(pptx.shapes.RIGHT_ARROW, { x: splitX, y: flowY + 0.1, w: arrowW, h: 0.3, fill: { color: BLACK } });

// Class I (light green oval) - upper
s.addShape(pptx.shapes.OVAL, { x: splitX + arrowW, y: flowY - 0.2, w: 1.0, h: 0.5, fill: { color: LIGHT_GREEN }, line: { color: GREEN, width: 1 } });
s.addText("Class I", { x: splitX + arrowW, y: flowY - 0.2, w: 1.0, h: 0.5, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Class II (light green oval) - lower
s.addShape(pptx.shapes.OVAL, { x: splitX + arrowW, y: flowY + 0.4, w: 1.0, h: 0.5, fill: { color: LIGHT_GREEN }, line: { color: GREEN, width: 1 } });
s.addText("Class II", { x: splitX + arrowW, y: flowY + 0.4, w: 1.0, h: 0.5, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// BOTTOM: Airplane scatter + horizontal axis
// ============================================================
const scatterY = 3.5;
const scatterH = 2.5;

function drawAirplane(cx, cy, dotColor) {
  s.addShape(pptx.shapes.LINE, { x: cx - 0.12, y: cy, w: 0.24, h: 0, line: { color: BLACK, width: 1.5 } });
  s.addShape(pptx.shapes.LINE, { x: cx, y: cy - 0.04, w: 0, h: 0.08, line: { color: BLACK, width: 1.5 } });
  s.addShape(pptx.shapes.LINE, { x: cx - 0.12, y: cy - 0.02, w: 0.06, h: 0.04, line: { color: BLACK, width: 1 } });
  if (dotColor) {
    s.addShape(pptx.shapes.OVAL, { x: cx + 0.06, y: cy - 0.03, w: 0.06, h: 0.06, fill: { color: dotColor }, line: { color: dotColor, width: 0 } });
  }
}

const planePositions = [
  { x: 5.0, y: scatterY + 0.3, dot: RED2 },
  { x: 6.2, y: scatterY + 0.8, dot: BLUE_DARK },
  { x: 7.5, y: scatterY + 0.2, dot: RED2 },
  { x: 8.8, y: scatterY + 1.1, dot: BLUE_DARK },
  { x: 10.0, y: scatterY + 0.5, dot: RED2 },
  { x: 11.2, y: scatterY + 1.3, dot: BLUE_DARK },
  { x: 5.5, y: scatterY + 1.5, dot: RED2 },
  { x: 6.8, y: scatterY + 1.8, dot: BLUE_DARK },
  { x: 8.0, y: scatterY + 1.6, dot: RED2 },
  { x: 9.3, y: scatterY + 1.9, dot: BLUE_DARK },
  { x: 10.5, y: scatterY + 1.7, dot: RED2 },
  { x: 11.5, y: scatterY + 2.0, dot: BLUE_DARK },
];

for (const pos of planePositions) {
  drawAirplane(pos.x, pos.y, pos.dot);
}

// Vertical dashed line at x ≈ 0.7 position
const axisLeftX = 4.5;
const axisRightX = 12.5;
const thresholdX = axisLeftX + (axisRightX - axisLeftX) * 0.7;

for (let i = 0; i < 20; i++) {
  const y = scatterY + i * 0.12;
  if (y < scatterY + scatterH) {
    s.addShape(pptx.shapes.LINE, { x: thresholdX, y: y, w: 0, h: 0.06, line: { color: PURPLE, width: 1, dashType: "dash" } });
  }
}

// Bottom horizontal red axis with arrow
const axisY = scatterY + scatterH + 0.1;
s.addShape(pptx.shapes.LINE, { x: axisLeftX, y: axisY, w: axisRightX - axisLeftX, h: 0, line: { color: RED2, width: 2 } });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: axisRightX, y: axisY - 0.05, w: 0.15, h: 0.1, fill: { color: RED2 } });

// Tick marks and labels
const ticks = [
  { label: "0.0", x: axisLeftX },
  { label: "0.5", x: axisLeftX + (axisRightX - axisLeftX) * 0.5 },
  { label: "1.0", x: axisRightX },
];

for (const tick of ticks) {
  s.addShape(pptx.shapes.LINE, { x: tick.x, y: axisY, w: 0, h: 0.1, line: { color: RED2, width: 1.5 } });
  s.addText(tick.label, { x: tick.x - 0.2, y: axisY + 0.12, w: 0.4, h: 0.3, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
}

// ============================================================
// OUTPUT
// ============================================================
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_026_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));