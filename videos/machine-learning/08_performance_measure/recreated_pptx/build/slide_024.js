const pptxgen = require("pptxgenjs");

// Slide 24 — "Effect of Selecting Threshold Value on Model Performance"
// Built from analysis/reanalysis/slide_024_raw.json + sources/slide_024_research.md
// + pool_run/image_analysis/slide_024_analysis.txt (frame px @960x540, 1px = 1/72 in).
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const DARKRED = "8B0000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "0000FF";
const GREEN = "90EE90";
const PINK = "FFB6C1";
const WHITE = "FFFFFF";
const PANEL = "FFFACD";
const BLACK = "212121";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---------- HOUSE CHROME ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("24", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- CONFUSION MATRIX (top-left, colored cells with TP/FN/FP/TN + counts) ----------
// original region px x60-240, y48-168
const gX = 0.83, gY = 0.67;
const gLabelW = 0.42, gCellW = 0.75, gHeadH = 0.20, gColH = 0.25, gCellH = 0.55;
const cellTop = (r) => gY + gHeadH + gColH + r * gCellH;
const colLeft = (c) => gX + gLabelW + c * gCellW;

s.addText("Predicted as", {
  x: gX + gLabelW, y: gY, w: gCellW * 2, h: gHeadH,
  fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("P", { x: colLeft(0), y: gY + gHeadH, w: gCellW, h: gColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: colLeft(1), y: gY + gHeadH, w: gCellW, h: gColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: gX, y: gY + gHeadH + gColH, w: gLabelW, h: gCellH * 2, fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("P", { x: gX, y: cellTop(0), w: gLabelW, h: gCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: gX, y: cellTop(1), w: gLabelW, h: gCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Standard orientation: rows = Actual P/N, cols = Predicted P/N
const gCells = [
  { lbl: "TP", val: "4", fill: GREEN, row: 0, col: 0 },
  { lbl: "FN", val: "1", fill: PINK, row: 0, col: 1 },
  { lbl: "FP", val: "1", fill: PINK, row: 1, col: 0 },
  { lbl: "TN", val: "5", fill: GREEN, row: 1, col: 1 },
];
for (const c of gCells) {
  const cx = colLeft(c.col), cy = cellTop(c.row);
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: gCellW, h: gCellH, fill: { color: c.fill }, line: { color: BLACK, width: 0.75 } });
  s.addText(c.lbl + "\n" + c.val, {
    x: cx, y: cy, w: gCellW, h: gCellH,
    fontSize: 10, bold: true, color: BLACK, fontFace: FONT,
    align: "center", valign: "middle", margin: 0,
  });
}

// ---------- NUMERIC CONFUSION MATRIX directly beneath (top-left stack) ----------
// original region px x66-229, y175-248
const nX = 0.92, nY = 2.22;
const nLabelW = 0.40, nCellW = 0.75, nHeadH = 0.18, nColH = 0.20, nCellH = 0.40;
const nTop = (r) => nY + nHeadH + nColH + r * nCellH;
s.addText("Predicted as", {
  x: nX + nLabelW, y: nY, w: nCellW * 2, h: nHeadH,
  fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("P", { x: nX + nLabelW, y: nY + nHeadH, w: nCellW, h: nColH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX + nLabelW + nCellW, y: nY + nHeadH, w: nCellW, h: nColH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: nX, y: nY + nHeadH + nColH, w: nLabelW, h: nCellH * 2, fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("P", { x: nX, y: nTop(0), w: nLabelW, h: nCellH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX, y: nTop(1), w: nLabelW, h: nCellH, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const nVals = [["4", "1"], ["1", "5"]];
for (let r = 0; r < 2; r++) {
  for (let c = 0; c < 2; c++) {
    const cx = nX + nLabelW + c * nCellW, cy = nTop(r);
    s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: nCellW, h: nCellH, fill: { color: WHITE }, line: { color: RED, width: 1 } });
    s.addText(nVals[r][c], { x: cx, y: cy, w: nCellW, h: nCellH, fontSize: 12, bold: true, color: DARKRED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  }
}

// ---------- Threshold=0.5 plain label right of the matrices ----------
s.addText("Threshold=0.5", {
  x: 2.85, y: 1.15, w: 1.60, h: 0.35,
  fontSize: 14, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});

// ---------- PIPELINE PANEL (cream) ----------
// original px x328-868, y56-194
const pX = 4.56, pY = 0.78, pW = 7.70, pH = 1.95;
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: pX, y: pY, w: pW, h: pH, fill: { color: PANEL }, line: { color: "C8C8A0", width: 1 } });

const fy = 1.66; // flow center line
const bh = 0.52;
const aw = 0.30;

function arrowRight(x0, y) {
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: y - 0.02, w: aw, h: 0.04, fill: { color: BLACK }, line: { type: "none" } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x0 + aw - 0.02, y: y - 0.06, w: 0.10, h: 0.12, fill: { color: BLACK }, line: { type: "none" }, rotate: 90 });
}

// airplane side-profile sketch: fuselage, tail fin up, swept wing down, center dot
function drawPlane(cx, cy, sc, dotColor) {
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 0.34 * sc, y: cy - 0.035 * sc, w: 0.68 * sc, h: 0.07 * sc,
    fill: { color: "BDBDBD" }, line: { color: "616161", width: 0.75 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.37 * sc, y: cy - 0.16 * sc, w: 0.12 * sc, h: 0.13 * sc,
    fill: { color: "CFCFCF" }, line: { color: "616161", width: 0.5 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.06 * sc, y: cy + 0.02 * sc, w: 0.24 * sc, h: 0.13 * sc,
    fill: { color: "CFCFCF" }, line: { color: "616161", width: 0.5 }, rotate: 180,
  });
  s.addShape(pptx.shapes.OVAL, {
    x: cx + 0.10 * sc, y: cy - 0.045 * sc, w: 0.09 * sc, h: 0.09 * sc,
    fill: { color: "E8E8E8" }, line: { color: "616161", width: 0.5 },
  });
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 0.035 * sc, y: cy - 0.035 * sc, w: 0.07 * sc, h: 0.07 * sc,
    fill: { color: dotColor }, line: { type: "none" },
  });
}

// Test Sample: label above box, airplane sketch inside
const tsX = 4.70, tsW = 1.25;
s.addText("Test Sample", { x: tsX, y: pY + 0.08, w: tsW, h: 0.22, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: fy - bh / 2, w: tsW, h: bh, fill: { color: WHITE }, line: { color: RED, width: 1 } });
drawPlane(tsX + tsW / 2, fy, 0.85, BLUE);

arrowRight(tsX + tsW, fy);

// Model box: dark red fill, white bold text, small white ROC-style curve icon, sub-caption underneath
const mX = 6.28, mW = 1.00;
s.addShape(pptx.shapes.RECTANGLE, { x: mX, y: fy - bh / 2, w: mW, h: bh, fill: { color: DARKRED }, line: { color: DARKRED, width: 1 } });
s.addText("Model", { x: mX, y: fy - bh / 2, w: mW, h: 0.24, fontSize: 11, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// curve icon: rising polyline with marker dots in the lower half of the box
const curve = [[6.36, 1.84], [6.55, 1.79], [6.74, 1.75], [6.94, 1.68], [7.18, 1.61]];
for (let i = 0; i < curve.length - 1; i++) {
  s.addShape(pptx.shapes.LINE, { x: curve[i][0], y: curve[i][1], w: curve[i + 1][0] - curve[i][0], h: curve[i + 1][1] - curve[i][1], line: { color: WHITE, width: 1.5 } });
}
for (const p of curve.slice(1, -1)) {
  s.addShape(pptx.shapes.OVAL, { x: p[0] - 0.025, y: p[1] - 0.025, w: 0.05, h: 0.05, fill: { color: WHITE }, line: { type: "none" } });
}
s.addText("[Any value] \u2014 (0, +1)", { x: mX - 0.15, y: fy + bh / 2 + 0.03, w: mW + 0.30, h: 0.20, fontSize: 7, color: BLACK, fontFace: FONT, align: "center", margin: 0 });

arrowRight(mX + mW, fy);
s.addText("(0 \u2014 1)", { x: mX + mW + 0.02, y: fy - 0.30, w: aw + 0.35, h: 0.18, fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });

// Threshold (e.g. 0.5) box
const thX = 7.72, thW = 1.45;
s.addShape(pptx.shapes.RECTANGLE, { x: thX, y: fy - bh / 2, w: thW, h: bh, fill: { color: WHITE }, line: { color: RED, width: 1.25 } });
s.addText("Threshold (e.g. 0.5)", { x: thX, y: fy - bh / 2, w: thW, h: bh, fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// branch arrows to Class I / Class II
const forkX = thX + thW;
const ciX = 11.10, ciW = 1.05;
s.addShape(pptx.shapes.LINE, { x: forkX + 0.03, y: fy - 0.08, w: ciX - forkX - 0.12, h: -(fy - 0.08 - (pY + 0.45)), line: { color: BLACK, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: ciX - 0.11, y: pY + 0.39, w: 0.10, h: 0.12, fill: { color: BLACK }, line: { type: "none" }, rotate: 90 });
s.addShape(pptx.shapes.LINE, { x: forkX + 0.03, y: fy + 0.08, w: ciX - forkX - 0.12, h: (pY + 1.48) - (fy + 0.08), line: { color: BLACK, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: ciX - 0.11, y: pY + 1.42, w: 0.10, h: 0.12, fill: { color: BLACK }, line: { type: "none" }, rotate: 90 });

// Class I (light green oval, upper) / Class II (light pink oval, lower)
s.addShape(pptx.shapes.OVAL, { x: ciX, y: pY + 0.24, w: ciW, h: 0.42, fill: { color: "98FB98" }, line: { color: "548235", width: 1 } });
s.addText("Class I", { x: ciX, y: pY + 0.24, w: ciW, h: 0.42, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: ciX, y: pY + 1.24, w: ciW, h: 0.42, fill: { color: PINK }, line: { color: "C55A11", width: 1 } });
s.addText("Class II", { x: ciX, y: pY + 1.24, w: ciW, h: 0.42, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---------- BOTTOM PLOT: Predicted axis 0.0–1.0, dashed threshold line, red dot, planes ----------
const axL = 1.19, axR = 12.33, axY = 6.06;   // px 86..888 @ y436
const thrX = axL + (axR - axL) * 0.5;          // 0.5 tick = px 487

s.addText("Predicted", { x: axL, y: axY - 0.32, w: 1.0, h: 0.22, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "left", margin: 0 });

// airplanes: 6 left of threshold (blue dot), 5 right (red dot) — predicted N=6, P=5
const planesLeft = [
  { x: 1.70, y: 4.10 }, { x: 2.60, y: 3.75 }, { x: 3.50, y: 4.30 },
  { x: 4.40, y: 3.80 }, { x: 5.30, y: 4.45 }, { x: 6.20, y: 3.90 },
];
const planesRight = [
  { x: 7.40, y: 4.00 }, { x: 8.30, y: 4.55 }, { x: 9.40, y: 3.95 },
  { x: 10.50, y: 4.50 }, { x: 11.60, y: 4.10 },
];
for (const p of planesLeft) drawPlane(p.x, p.y, 1.15, BLUE);
for (const p of planesRight) drawPlane(p.x, p.y, 1.15, "FF0000");

// dashed blue vertical line at 0.5, from red dot down to the axis
for (let i = 0; i < 40; i++) {
  const yy = 3.30 + i * 0.068;
  if (yy > axY - 0.06) break;
  s.addShape(pptx.shapes.LINE, { x: thrX, y: yy, w: 0, h: 0.038, line: { color: BLUE, width: 1.5, dashType: "dash" } });
}
// red threshold circle atop the dashed line (px ~(486,215), r~10)
s.addShape(pptx.shapes.OVAL, { x: thrX - 0.14, y: 2.85, w: 0.28, h: 0.28, fill: { color: "FF0000" }, line: { type: "none" } });

// dark-red horizontal axis with ticks + labels 0.0 / 0.5 / 1.0
s.addShape(pptx.shapes.LINE, { x: axL, y: axY, w: axR - axL, h: 0, line: { color: DARKRED, width: 2 } });
const ticks = [{ label: "0.0", x: axL }, { label: "0.5", x: thrX }, { label: "1.0", x: axR }];
for (const t of ticks) {
  s.addShape(pptx.shapes.LINE, { x: t.x, y: axY - 0.08, w: 0, h: 0.16, line: { color: DARKRED, width: 2 } });
  s.addText(t.label, { x: t.x - 0.25, y: axY + 0.10, w: 0.50, h: 0.26, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
}

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_024_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
