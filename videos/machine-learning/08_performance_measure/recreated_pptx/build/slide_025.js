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
const PANEL = "FBFEE3";
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
s.addText("25", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED2, fontFace: FONT, margin: 0,
});

// ============================================================
// SLIDE 25 CONTENT (measured from original frame)
// Original 960x540 px @ 72.02 px/in
// ============================================================

// ---- SMALL CONFUSION MATRIX (top-left): x 1.08..2.31in, y 1.39..2.69in ----
// Cells: P/N top row, FP/TN bottom (green/red fills per judge)
const smX = 1.08, smY = 1.39;
const smCellW = 0.615, smCellH = 0.65;   // total 1.23 x 1.30
const smHeadH = 0.25;
const smLabelW = 0.30;

s.addText("Predicted as", {
  x: smX + smLabelW, y: smY, w: smCellW * 2, h: smHeadH,
  fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0,
});
s.addText("P", { x: smX + smLabelW, y: smY + smHeadH, w: smCellW, h: smCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: smX + smLabelW + smCellW, y: smY + smHeadH, w: smCellW, h: smCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: smX, y: smY + smHeadH, w: smLabelW, h: smCellH * 2, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: smX, y: smY + smHeadH, w: smLabelW, h: smCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: smX, y: smY + smHeadH + smCellH, w: smLabelW, h: smCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// Red-bordered frame (judge: red borders)
s.addShape(pptx.shapes.RECTANGLE, { x: smX + smLabelW, y: smY + smHeadH, w: smCellW * 2, h: smCellH * 2, fill: { type: "none" }, line: { color: RED2, width: 1.25 } });
// Cells P, N (top); FN, TN (bottom) — green fill for FN, TN red text on white
s.addShape(pptx.shapes.RECTANGLE, { x: smX + smLabelW, y: smY + smHeadH, w: smCellW, h: smCellH, fill: { color: WHITE }, line: { color: RED2, width: 0.5 } });
s.addText("P", { x: smX + smLabelW, y: smY + smHeadH, w: smCellW, h: smCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: smX + smLabelW + smCellW, y: smY + smHeadH, w: smCellW, h: smCellH, fill: { color: WHITE }, line: { color: RED2, width: 0.5 } });
s.addText("N", { x: smX + smLabelW + smCellW, y: smY + smHeadH, w: smCellW, h: smCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: smX + smLabelW, y: smY + smHeadH + smCellH, w: smCellW, h: smCellH, fill: { color: GREEN }, line: { color: RED2, width: 0.5 } });
s.addText("FN", { x: smX + smLabelW, y: smY + smHeadH + smCellH, w: smCellW, h: smCellH, fontSize: 10, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: smX + smLabelW + smCellW, y: smY + smHeadH + smCellH, w: smCellW, h: smCellH, fill: { color: WHITE }, line: { color: RED2, width: 0.5 } });
s.addText("TN", { x: smX + smLabelW + smCellW, y: smY + smHeadH + smCellH, w: smCellW, h: smCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---- THRESHOLD BOX: to the RIGHT of small matrix, same band (x 2.44..4.71in, y 1.54..2.06in) ----
const tbX = 2.44, tbY = 1.54, tbW = 2.27, tbH = 0.52;
s.addShape(pptx.shapes.RECTANGLE, { x: tbX, y: tbY, w: tbW, h: tbH, fill: { color: WHITE }, line: { color: RED2, width: 1.25 } });
s.addText("Threshold=0.6", { x: tbX, y: tbY, w: tbW, h: tbH, fontSize: 13, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---- BIG CONFUSION MATRIX: below small one (x 1.08..2.31in, y 2.71..4.12in) ----
const bmX = 1.08, bmY = 2.71;
const bmCellW = 0.615, bmCellH = 0.71;
s.addText("Predicted as", { x: bmX + 0.30, y: bmY, w: bmCellW * 2, h: 0.25, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0 });
s.addText("P", { x: bmX + 0.30, y: bmY + 0.25, w: bmCellW, h: bmCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: bmX + 0.30 + bmCellW, y: bmY + 0.25, w: bmCellW, h: bmCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: bmX, y: bmY + 0.25, w: 0.30, h: bmCellH * 2, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: bmX, y: bmY + 0.25, w: 0.30, h: bmCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: bmX, y: bmY + 0.25 + bmCellH, w: 0.30, h: bmCellH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: bmX + 0.30, y: bmY + 0.25, w: bmCellW * 2, h: bmCellH * 2, fill: { type: "none" }, line: { color: RED2, width: 1.25 } });
// Values 3(blue), 2(red) / 1(red), 5(blue)
s.addShape(pptx.shapes.RECTANGLE, { x: bmX + 0.30, y: bmY + 0.25, w: bmCellW, h: bmCellH, fill: { color: WHITE }, line: { color: RED2, width: 0.5 } });
s.addText("3", { x: bmX + 0.30, y: bmY + 0.25, w: bmCellW, h: bmCellH, fontSize: 12, bold: true, color: BLUE_DARK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: bmX + 0.30 + bmCellW, y: bmY + 0.25, w: bmCellW, h: bmCellH, fill: { color: WHITE }, line: { color: RED2, width: 0.5 } });
s.addText("2", { x: bmX + 0.30 + bmCellW, y: bmY + 0.25, w: bmCellW, h: bmCellH, fontSize: 12, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: bmX + 0.30, y: bmY + 0.25 + bmCellH, w: bmCellW, h: bmCellH, fill: { color: WHITE }, line: { color: RED2, width: 0.5 } });
s.addText("1", { x: bmX + 0.30, y: bmY + 0.25 + bmCellH, w: bmCellW, h: bmCellH, fontSize: 12, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: bmX + 0.30 + bmCellW, y: bmY + 0.25 + bmCellH, w: bmCellW, h: bmCellH, fill: { color: WHITE }, line: { color: RED2, width: 0.5 } });
s.addText("5", { x: bmX + 0.30 + bmCellW, y: bmY + 0.25 + bmCellH, w: bmCellW, h: bmCellH, fontSize: 12, bold: true, color: BLUE_DARK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---- PIPELINE PANEL: measured x 4.56..11.66in, y 1.42..2.68in (color #FBFEE3) ----
const pnX = 4.56, pnY = 1.42, pnW = 7.10, pnH = 1.26;
s.addShape(pptx.shapes.RECTANGLE, { x: pnX, y: pnY, w: pnW, h: pnH, fill: { color: PANEL }, line: { color: "C8C8A0", width: 1 } });

// --- Flowchart inside panel ---
const fy = 1.85;             // box vertical center line
const bh = 0.50;             // box height
const aw = 0.32;             // arrow width

// Test Sample box (x 4.70..5.80) with airplane sketch
const tsX = 4.70, tsW = 1.10;
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: fy - bh/2, w: tsW, h: bh, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
s.addText("Test Sample", { x: tsX + 0.05, y: fy - bh/2, w: tsW - 0.30, h: bh, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// Hand-drawn airplane sketch inside box (fuselage + wings + tail)
const apx = tsX + tsW - 0.24, apy = fy;
s.addShape(pptx.shapes.LINE, { x: apx - 0.07, y: apy, w: 0.14, h: 0, line: { color: "808080", width: 1.25 } });
s.addShape(pptx.shapes.LINE, { x: apx, y: apy - 0.03, w: 0, h: 0.06, line: { color: "808080", width: 1.25 } });
s.addShape(pptx.shapes.LINE, { x: apx - 0.07, y: apy - 0.015, w: 0.04, h: 0.03, line: { color: "808080", width: 1 } });
s.addShape(pptx.shapes.OVAL, { x: apx - 0.05, y: apy - 0.04, w: 0.04, h: 0.04, fill: { type: "none" }, line: { color: "808080", width: 1 } });

// Arrow (hollow red outlined, white filled) Test Sample -> Model
s.addShape(pptx.shapes.RECTANGLE, { x: tsX + tsW, y: fy - 0.02, w: aw, h: 0.04, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: tsX + tsW + aw - 0.08, y: fy - 0.06, w: 0.08, h: 0.12, fill: { color: WHITE }, line: { color: RED2, width: 1 }, rotate: 90 });

// Model box (x 6.12..7.05, dark red, white text)
const mdX = 6.12, mdW = 0.93;
s.addShape(pptx.shapes.RECTANGLE, { x: mdX, y: fy - 0.35, w: mdW, h: 0.70, fill: { color: RED2 }, line: { type: "none" } });
s.addText("Model", { x: mdX, y: fy - 0.34, w: mdW, h: 0.32, fontSize: 10, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("[Any value] ~ (0, +∞)", { x: mdX, y: fy - 0.02, w: mdW, h: 0.34, fontSize: 7, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Magenta circle with white pie/clock face (x 7.20..7.60, y 1.60..2.15)
const ccX = 7.20, ccY = 1.60, ccD = 0.50;
s.addShape(pptx.shapes.OVAL, { x: ccX, y: ccY, w: ccD, h: ccD, fill: { color: PURPLE }, line: { type: "none" } });
s.addShape(pptx.shapes.OVAL, { x: ccX + 0.10, y: ccY + 0.10, w: 0.30, h: 0.30, fill: { color: WHITE }, line: { type: "none" } });
s.addShape(pptx.shapes.PIE, { x: ccX + 0.10, y: ccY + 0.10, w: 0.30, h: 0.30, fill: { color: PURPLE }, line: { type: "none" }, angleRange: [180, 270] });

// Arrow Model -> Predicted Value
s.addShape(pptx.shapes.RECTANGLE, { x: ccX + ccD, y: fy - 0.02, w: aw, h: 0.04, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: ccX + ccD + aw - 0.08, y: fy - 0.06, w: 0.08, h: 0.12, fill: { color: WHITE }, line: { color: RED2, width: 1 }, rotate: 90 });

// Predicted Value label + (0 --- 1) box (x 8.02..8.92)
const pvX = 8.02, pvW = 0.90;
s.addText("Predicted Value", { x: pvX, y: fy - 0.45, w: pvW, h: 0.22, fontSize: 8, bold: true, color: BLUE, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: pvX, y: fy - bh/2, w: pvW, h: bh, fill: { color: WHITE }, line: { color: BLUE, width: 1.25 } });
s.addText("(0 --- 1)", { x: pvX, y: fy - bh/2, w: pvW, h: bh, fontSize: 9, bold: true, color: BLUE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Arrow -> Threshold
s.addShape(pptx.shapes.RECTANGLE, { x: pvX + pvW, y: fy - 0.02, w: aw, h: 0.04, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: pvX + pvW + aw - 0.08, y: fy - 0.06, w: 0.08, h: 0.12, fill: { color: WHITE }, line: { color: RED2, width: 1 }, rotate: 90 });

// Threshold box (red) (x 9.24..10.24)
const thX = 9.24, thW = 1.00;
s.addShape(pptx.shapes.RECTANGLE, { x: thX, y: fy - bh/2, w: thW, h: bh, fill: { color: WHITE }, line: { color: RED2, width: 1.25 } });
s.addText("Threshold", { x: thX, y: fy - bh/2, w: thW, h: bh, fontSize: 9, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Two RED diagonal arrows (X-fork) to Class I (up) and Class II (down)
const forkX = thX + thW;
const clsIX = 10.60, clsIIX = 10.60;
s.addShape(pptx.shapes.LINE, { x: forkX + 0.05, y: fy - 0.12, w: 0.32, h: -0.22, line: { color: RED2, width: 1.5, endArrowType: "triangle" } });
s.addShape(pptx.shapes.LINE, { x: forkX + 0.05, y: fy + 0.12, w: 0.32, h: 0.22, line: { color: RED2, width: 1.5, endArrowType: "triangle" } });

// Class I oval (green) — inside panel, upper
s.addShape(pptx.shapes.OVAL, { x: clsIX, y: fy - 0.55, w: 0.95, h: 0.44, fill: { color: GREEN }, line: { color: GREEN, width: 1 } });
s.addText("Class I", { x: clsIX, y: fy - 0.55, w: 0.95, h: 0.44, fontSize: 9, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// Class II oval (purple) — inside panel, lower
s.addShape(pptx.shapes.OVAL, { x: clsIIX, y: fy + 0.11, w: 0.95, h: 0.44, fill: { color: PURPLE }, line: { color: PURPLE, width: 1 } });
s.addText("Class II", { x: clsIIX, y: fy + 0.11, w: 0.95, h: 0.44, fontSize: 9, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// BOTTOM: airplane illustrations scatter + axis (measured)
// airplanes in original x range 1.33..12.08, y 3.14..5.60, each ~1.0..1.4in wide
// ============================================================
const planePositions = [
  { x: 1.60, y: 3.50 },
  { x: 3.10, y: 3.95 },
  { x: 4.40, y: 3.60 },
  { x: 5.60, y: 4.35 },
  { x: 6.95, y: 3.90 },
  { x: 7.90, y: 4.85 },
  { x: 8.95, y: 4.45 },
  { x: 9.95, y: 5.20 },
  { x: 10.90, y: 4.85 },
  { x: 12.00, y: 5.25 },
  { x: 2.75, y: 4.55 },
  { x: 5.90, y: 5.35 },
];

function drawPlane(cx, cy, scale) {
  // Simple gray airplane silhouette (top view), left-facing like originals
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 0.18 * scale, y: cy - 0.018 * scale,
    w: 0.36 * scale, h: 0.036 * scale,
    fill: { color: "9E9E9E" }, line: { color: "616161", width: 0.5 },
  });
  // wings (swept)
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.06 * scale, y: cy - 0.20 * scale,
    w: 0.20 * scale, h: 0.20 * scale,
    fill: { color: "BDBDBD" }, line: { color: "616161", width: 0.5 }, rotate: 180,
  });
  // tail
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.17 * scale, y: cy - 0.09 * scale,
    w: 0.09 * scale, h: 0.09 * scale,
    fill: { color: "BDBDBD" }, line: { color: "616161", width: 0.5 }, rotate: 180,
  });
  // nose dot (red or blue)
  s.addShape(pptx.shapes.OVAL, {
    x: cx + 0.15 * scale, y: cy - 0.03 * scale,
    w: 0.06 * scale, h: 0.06 * scale,
    fill: { color: (cx % 2 < 1 ? RED2 : BLUE_DARK) }, line: { type: "none" },
  });
}

for (const p of planePositions) drawPlane(p.x, p.y, 1.35);

// Vertical dashed line at x=0.58 of axis + faint magenta offset
const axL = 1.21, axR = 12.32, axY = 6.06;
const thrIn = axL + (axR - axL) * 0.58;
for (let i = 0; i < 40; i++) {
  const yy = 3.05 + i * 0.075;
  if (yy > 6.05) break;
  s.addShape(pptx.shapes.LINE, { x: thrIn, y: yy, w: 0, h: 0.04, line: { color: BLUE, width: 1, dashType: "dash" } });
}
s.addShape(pptx.shapes.LINE, { x: thrIn + 0.06, y: 3.05, w: 0, h: 3.0, line: { color: PURPLE, width: 0.5, dashType: "dash" } });

// Horizontal red axis, full content width, arrowheads at BOTH ends
s.addShape(pptx.shapes.LINE, { x: axL + 0.12, y: axY, w: axR - axL - 0.24, h: 0, line: { color: RED2, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: axL, y: axY - 0.06, w: 0.12, h: 0.12, fill: { color: RED2 }, line: { type: "none" }, rotate: 270 });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: axR - 0.12, y: axY - 0.06, w: 0.12, h: 0.12, fill: { color: RED2 }, line: { type: "none" }, rotate: 90 });

// Ticks: 0.0/0.5/1.0 labeled + intermediate short ticks
const mainT = [
  { label: "0.0", x: axL },
  { label: "0.5", x: axL + (axR - axL) * 0.5 },
  { label: "1.0", x: axR },
];
for (const t of mainT) {
  s.addShape(pptx.shapes.LINE, { x: t.x, y: axY, w: 0, h: 0.16, line: { color: RED2, width: 2 } });
  s.addText(t.label, { x: t.x - 0.22, y: axY + 0.18, w: 0.44, h: 0.28, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
}
for (const pos of [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]) {
  const x = axL + (axR - axL) * pos;
  s.addShape(pptx.shapes.LINE, { x: x, y: axY, w: 0, h: 0.09, line: { color: RED2, width: 1.25 } });
}

// ---- OUTPUT ----
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_025_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
