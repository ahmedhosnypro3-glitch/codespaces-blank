const pptxgen = require("pptxgenjs");

// Slide 24 — "Effect of Selecting Threshold Value on Model Performance"
// Frame 960x540 px, 72 px/in. Content measured from unique_slides/slide_024.jpg
// and pool_run/image_analysis/slide_024_analysis.txt (authoritative).
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "2E75B6";
const GREEN = "00B050";
const PINK = "FF99CC";
const WHITE = "FFFFFF";
const PANEL = "FBFEE3";
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
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- GENERIC CONFUSION MATRIX (top-left, TP/FN/TN/FP labels) ----------
// original region px x60-240, y48-168
const gX = 0.83, gY = 0.67;
const gLabelW = 0.42, gCellW = 0.75, gHeadH = 0.20, gColH = 0.25, gCellH = 0.50;
s.addText("Predicted as", {
  x: gX + gLabelW, y: gY, w: gCellW * 2, h: gHeadH,
  fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("P", { x: gX + gLabelW, y: gY + gHeadH, w: gCellW, h: gColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: gX + gLabelW + gCellW, y: gY + gHeadH, w: gCellW, h: gColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: gX, y: gY + gHeadH + gColH, w: gLabelW, h: gCellH * 2, fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: gX, y: gY + gHeadH + gColH, w: gLabelW, h: gCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: gX, y: gY + gHeadH + gColH + gCellH, w: gLabelW, h: gCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const gCells = [
  { lbl: "TP", fill: GREEN, txt: WHITE, cx: 0, cy: 0 },
  { lbl: "FN", fill: "F4CCCC", txt: BLACK, cx: 1, cy: 0 },
  { lbl: "TN", fill: GREEN, txt: WHITE, cx: 0, cy: 1 },
  { lbl: "FP", fill: "FFFF00", txt: BLACK, cx: 1, cy: 1 },
];
for (const c of gCells) {
  const cx = gX + gLabelW + c.cx * gCellW, cy = gY + gHeadH + gColH + c.cy * gCellH;
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: gCellW, h: gCellH, fill: { color: c.fill }, line: { color: BLACK, width: 0.5 } });
  s.addText(c.lbl, { x: cx, y: cy, w: gCellW, h: gCellH, fontSize: 10, bold: true, color: c.txt, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}

// ---------- NUMERIC CONFUSION MATRIX (below, 4/1/1/5, red grid) ----------
// original region px x66-229, y175-248
const nX = 0.92, nY = 2.40;
const nLabelW = 0.40, nCellW = 0.75, nHeadH = 0.18, nColH = 0.20, nCellH = 0.42;
s.addText("Predicted as", {
  x: nX + nLabelW, y: nY, w: nCellW * 2, h: nHeadH,
  fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0,
});
s.addText("P", { x: nX + nLabelW, y: nY + nHeadH, w: nCellW, h: nColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX + nLabelW + nCellW, y: nY + nHeadH, w: nCellW, h: nColH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: nX, y: nY + nHeadH + nColH, w: nLabelW, h: nCellH * 2, fontSize: 8, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: nX, y: nY + nHeadH + nColH, w: nLabelW, h: nCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX, y: nY + nHeadH + nColH + nCellH, w: nLabelW, h: nCellH, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const nVals = [["4", "1"], ["1", "5"]];
for (let r = 0; r < 2; r++) {
  for (let c = 0; c < 2; c++) {
    const cx = nX + nLabelW + c * nCellW, cy = nY + nHeadH + nColH + r * nCellH;
    s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: nCellW, h: nCellH, fill: { color: WHITE }, line: { color: RED, width: 1 } });
    s.addText(nVals[r][c], { x: cx, y: cy, w: nCellW, h: nCellH, fontSize: 13, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  }
}

// ---------- Threshold=0.5 label box ----------
const tX = 2.75, tY = 1.18, tW = 1.55, tH = 0.42;
s.addShape(pptx.shapes.RECTANGLE, { x: tX, y: tY, w: tW, h: tH, fill: { color: WHITE }, line: { color: RED, width: 1.25 } });
s.addText("Threshold=0.5", { x: tX, y: tY, w: tW, h: tH, fontSize: 13, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---------- PIPELINE PANEL (beige) ----------
// original px x328-868, y56-194
const pX = 4.56, pY = 0.78, pW = 7.70, pH = 1.95;
s.addShape(pptx.shapes.RECTANGLE, { x: pX, y: pY, w: pW, h: pH, fill: { color: PANEL }, line: { color: "C8C8A0", width: 1 } });

const fy = 1.62; // flow center line
const bh = 0.52;
const aw = 0.30;

function arrowRight(x0, y) {
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: y - 0.02, w: aw, h: 0.04, fill: { color: BLACK }, line: { type: "none" } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x0 + aw - 0.02, y: y - 0.06, w: 0.10, h: 0.12, fill: { color: BLACK }, line: { type: "none" }, rotate: 90 });
}

// Test Sample: label above box, airplane sketch inside
const tsX = 4.70, tsW = 1.25;
s.addText("Test Sample", { x: tsX, y: pY + 0.10, w: tsW, h: 0.22, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: fy - bh / 2, w: tsW, h: bh, fill: { color: WHITE }, line: { color: RED, width: 1 } });
drawPlane(tsX + tsW / 2 - 0.05, fy, 1.0, false);

arrowRight(tsX + tsW, fy);

// Model box with range note underneath
const mX = 6.28, mW = 1.00;
s.addShape(pptx.shapes.RECTANGLE, { x: mX, y: fy - bh / 2, w: mW, h: bh, fill: { color: "FFF2CC" }, line: { color: RED, width: 1.25 } });
s.addText("Model", { x: mX, y: fy - bh / 2, w: mW, h: bh, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("[Any value] \u2192 (0, +1)", { x: mX - 0.10, y: fy + bh / 2 + 0.02, w: mW + 0.20, h: 0.20, fontSize: 7, color: BLACK, fontFace: FONT, align: "center", margin: 0 });

arrowRight(mX + mW, fy);

// Predicted Value label + (0 — 1) box
const pvX = 7.60, pvW = 1.25;
s.addText("Predicted Value", { x: pvX, y: pY + 0.10, w: pvW, h: 0.22, fontSize: 9, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: pvX, y: fy - bh / 2, w: pvW, h: bh, fill: { color: "FFC7CE" }, line: { color: RED, width: 1.25 } });
s.addText("(0 \u2014 1)", { x: pvX, y: fy - bh / 2, w: pvW, h: bh, fontSize: 11, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Fork arrows to Class I / Class II with red threshold labels
const forkX = pvX + pvW;
const ciX = 11.05, ciW = 1.15;
s.addShape(pptx.shapes.LINE, { x: forkX + 0.03, y: fy - 0.10, w: ciX - forkX - 0.10, h: -(fy - 0.10 - (pY + 0.42)), line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: ciX - 0.10, y: pY + 0.36, w: 0.10, h: 0.12, fill: { color: RED }, line: { type: "none" }, rotate: 90 });
s.addShape(pptx.shapes.LINE, { x: forkX + 0.03, y: fy + 0.10, w: ciX - forkX - 0.10, h: (pY + 1.42) - (fy + 0.10), line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: ciX - 0.10, y: pY + 1.36, w: 0.10, h: 0.12, fill: { color: RED }, line: { type: "none" }, rotate: 90 });
s.addText("Threshold (e.g. 0.5)", { x: forkX + 0.10, y: fy - 0.34, w: 1.45, h: 0.18, fontSize: 8, bold: true, color: RED, fontFace: FONT, align: "left", margin: 0 });
s.addText("Threshold (e.g. 0.5)", { x: forkX + 0.10, y: fy + 0.16, w: 1.45, h: 0.18, fontSize: 8, bold: true, color: RED, fontFace: FONT, align: "left", margin: 0 });

// Class I (green oval, upper) / Class II (pink oval, lower)
s.addShape(pptx.shapes.OVAL, { x: ciX, y: pY + 0.22, w: ciW, h: 0.42, fill: { color: GREEN }, line: { color: GREEN, width: 1 } });
s.addText("Class I", { x: ciX, y: pY + 0.22, w: ciW, h: 0.42, fontSize: 10, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: ciX, y: pY + 1.22, w: ciW, h: 0.42, fill: { color: PINK }, line: { color: PINK, width: 1 } });
s.addText("Class II", { x: ciX, y: pY + 1.22, w: ciW, h: 0.42, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ---------- BOTTOM PLOT: 0.0–1.0 axis, dashed threshold, red dot, airplanes ----------
function drawPlane(cx, cy, scale, redDot) {
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 0.18 * scale, y: cy - 0.018 * scale,
    w: 0.36 * scale, h: 0.036 * scale,
    fill: { color: "9E9E9E" }, line: { color: "616161", width: 0.5 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.06 * scale, y: cy - 0.20 * scale,
    w: 0.20 * scale, h: 0.20 * scale,
    fill: { color: "BDBDBD" }, line: { color: "616161", width: 0.5 }, rotate: 180,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 0.17 * scale, y: cy - 0.09 * scale,
    w: 0.09 * scale, h: 0.09 * scale,
    fill: { color: "BDBDBD" }, line: { color: "616161", width: 0.5 }, rotate: 180,
  });
  s.addShape(pptx.shapes.OVAL, {
    x: cx + 0.14 * scale, y: cy - 0.03 * scale,
    w: 0.06 * scale, h: 0.06 * scale,
    fill: { color: redDot ? "FF0000" : "2E75B6" }, line: { type: "none" },
  });
}

const axL = 1.19, axR = 12.33, axY = 6.06;   // px 86..888 @ y436
const thrX = axL + (axR - axL) * 0.5;          // 0.5 tick = px 487

// airplanes: 5 left of threshold (plain), 6 right (red dot) — TP=4,FN=1,FP=1,TN=5
const planesLeft = [
  { x: 3.30, y: 3.85 }, { x: 2.95, y: 4.60 }, { x: 1.60, y: 4.95 },
  { x: 2.40, y: 5.20 }, { x: 4.30, y: 4.55 },
];
const planesRight = [
  { x: 5.28, y: 3.68 }, { x: 6.94, y: 4.24 }, { x: 7.85, y: 4.38 },
  { x: 9.03, y: 4.44 }, { x: 10.14, y: 4.44 }, { x: 11.50, y: 5.05 },
];
for (const p of planesLeft) drawPlane(p.x, p.y, 1.25, false);
for (const p of planesRight) drawPlane(p.x, p.y, 1.25, true);

// dashed blue vertical line at 0.5, from red dot down to axis
for (let i = 0; i < 36; i++) {
  const yy = 3.18 + i * 0.082;
  if (yy > axY - 0.05) break;
  s.addShape(pptx.shapes.LINE, { x: thrX, y: yy, w: 0, h: 0.045, line: { color: BLUE, width: 1.5, dashType: "dash" } });
}
// red threshold circle atop the dashed line (px ~(486,215), r~10)
s.addShape(pptx.shapes.OVAL, { x: thrX - 0.14, y: 2.85, w: 0.28, h: 0.28, fill: { color: "FF0000" }, line: { type: "none" } });

// red horizontal axis
s.addShape(pptx.shapes.LINE, { x: axL, y: axY, w: axR - axL, h: 0, line: { color: RED, width: 2 } });
// ticks + labels 0.0 / 0.5 / 1.0
const ticks = [{ label: "0.0", x: axL }, { label: "0.5", x: thrX }, { label: "1.0", x: axR }];
for (const t of ticks) {
  s.addShape(pptx.shapes.LINE, { x: t.x, y: axY - 0.08, w: 0, h: 0.16, line: { color: RED, width: 2 } });
  s.addText(t.label, { x: t.x - 0.25, y: axY + 0.10, w: 0.50, h: 0.26, fontSize: 10, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
}

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_024_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
