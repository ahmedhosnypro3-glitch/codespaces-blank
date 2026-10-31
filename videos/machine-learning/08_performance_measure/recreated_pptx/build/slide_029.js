const pptxgenpkg = require("pptxgenjs");

// Slide 29 — ROC Curve for Same Model -different thresholds (Threshold=0.0)
// Original frame 960x540 px; 1px = 1pt = 1/72 in. All geometry measured from
// unique_slides/slide_029.jpg with PIL (see qa/slide029/selfcheck_1.py).
// Drift items from pool_run/spec_gaps.md: 2D stacked fractions
// TPR = TP/(TP+FN) and FPR = FP/(FP+TN) (rendered as 600dpi mathtext PNGs).

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", HOUSE_RED = "C00000", BADGE = "FFF9C4", NUM = "333333";
// Pixel forensics on the original: reds are dark C00000, blues are navy 000080.
const INK = "000000", RED2 = "C00000", BLUE = "000080";
const FONT = "Arial";
const P = (px) => px / 72; // px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE CHROME (root AGENTS.md 2026-10-09) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 }
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("29", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8, align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0
});

// --- outer content rectangle (red) x57..902 y42..517 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(57), y: P(42), w: P(902 - 57), h: P(517 - 42),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 2 }
});
// red vertical divider between left table and right panel (x=636)
s.addShape(pptx.shapes.LINE, {
  x: P(636), y: P(42), w: 0, h: P(517 - 42),
  line: { color: RED2, width: 2 }
});
// --- blue grid inside left table: vertical x=344, horizontals y=162,286,401 ---
s.addShape(pptx.shapes.LINE, {
  x: P(344), y: P(42), w: 0, h: P(517 - 42),
  line: { color: BLUE, width: 2 }
});
for (const gy of [162, 286, 401]) {
  s.addShape(pptx.shapes.LINE, {
    x: P(57), y: P(gy), w: P(636 - 57), h: 0,
    line: { color: BLUE, width: 2 }
  });
}

// --- top-left cell: threshold box (pink fill, red border) x68..174 y52..78 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(68), y: P(52), w: P(174 - 68), h: P(78 - 52),
  fill: { color: "F8DCC6" }, line: { color: RED2, width: 1.5 }
});
s.addText("Threshold=0.0", {
  x: P(68), y: P(52), w: P(174 - 68), h: P(78 - 52),
  align: "center", valign: "middle", fontSize: 13, color: RED2, fontFace: FONT, margin: 0
});

// --- top-left confusion matrix (red border) x80..218 y84..159 ---
const MX = P(80), MY = P(84), MW = P(218 - 80), MH = P(159 - 84);
s.addShape(pptx.shapes.RECTANGLE, {
  x: MX, y: MY, w: MW, h: MH,
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1.25 }
});
// internal grid: vlines x=117,166 from y=92 down; hlines y=92 (right part),112,136,157
for (const vx of [117, 166]) {
  s.addShape(pptx.shapes.LINE, {
    x: P(vx), y: P(92), w: 0, h: P(159 - 92),
    line: { color: RED2, width: 1 }
  });
}
s.addShape(pptx.shapes.LINE, { x: P(117), y: P(92), w: P(218 - 117), h: 0, line: { color: RED2, width: 1 } });
for (const hy of [112, 136, 157]) {
  s.addShape(pptx.shapes.LINE, { x: MX, y: P(hy), w: MW, h: 0, line: { color: RED2, width: 1 } });
}
// header "Predicted as" spanning value columns (row y84..92)
s.addText("Predicted as", {
  x: P(117), y: MY, w: P(218 - 117), h: P(92 - 84),
  align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0
});
// column headers P / N (row y92..112)
s.addText("P", { x: P(117), y: P(92), w: P(166 - 117), h: P(112 - 92), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: P(166), y: P(92), w: P(218 - 166), h: P(112 - 92), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
// rotated "Actual" in label column
s.addText("Actual", {
  x: P(80) - P(38) / 2 + P(2), y: P(137) - P(4) / 2, w: P(38), h: P(4),
  align: "center", valign: "middle", fontSize: 9, color: INK, fontFace: FONT, margin: 0, rotate: 270
});
// row labels P / N
s.addText("P", { x: P(84), y: P(112), w: P(117 - 84), h: P(136 - 112), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: P(84), y: P(136), w: P(117 - 84), h: P(157 - 136), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
// cell values: TP=5 blue, FN=0, FP=6 red, TN=0 (13pt)
const cell = (cx0, cx1, cy0, cy1, txt, col) => s.addText(txt, {
  x: P(cx0), y: P(cy0), w: P(cx1 - cx0), h: P(cy1 - cy0),
  align: "center", valign: "middle", fontSize: 13, color: col, fontFace: FONT, margin: 0
});
cell(117, 166, 112, 136, "5", BLUE);
cell(166, 218, 112, 136, "0", RED2);
cell(117, 166, 136, 157, "6", RED2);
cell(166, 218, 136, 157, "0", BLUE);

// --- metrics box (pale yellow fill, red border) x224..341 y98..148 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(224), y: P(98), w: P(341 - 224), h: P(148 - 98),
  fill: { color: "F9FBDF" }, line: { color: RED2, width: 1.25 }
});
s.addText([
  { text: "TPR=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "5", options: { fontSize: 10, color: BLUE, fontFace: FONT, breakLine: false } },
  { text: "/(5+0)=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "1", options: { fontSize: 10, color: BLUE, fontFace: FONT, breakLine: true } },
  { text: "FPR=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "6", options: { fontSize: 10, color: RED2, fontFace: FONT, breakLine: false } },
  { text: "/(6+0)=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "1", options: { fontSize: 10, color: RED2, fontFace: FONT, breakLine: false } }
], {
  x: P(224), y: P(98), w: P(341 - 224), h: P(148 - 98),
  align: "center", valign: "middle", margin: 0, lineSpacing: 20
});

// --- bottom-center title box (gray fill, blue border) x354..624 y425..477 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(354), y: P(425), w: P(624 - 354), h: P(477 - 425),
  fill: { color: "E7E6E4" }, line: { color: BLUE, width: 1.5 }
});
s.addText([
  { text: "ROC Curve for", options: { fontSize: 17, bold: true, color: RED2, fontFace: FONT, breakLine: true } },
  { text: "Same Model -different thresholds", options: { fontSize: 17, bold: true, color: RED2, fontFace: FONT, breakLine: false } }
], {
  x: P(354), y: P(425), w: P(624 - 354), h: P(477 - 425),
  align: "center", valign: "middle", margin: 0, lineSpacing: 20
});

// --- ROC chart: blue frame x641..896 y79..387, light fill ---
const CX = P(641), CY = P(79), CW = P(896 - 641), CH = P(387 - 79);
s.addShape(pptx.shapes.RECTANGLE, {
  x: CX, y: CY, w: CW, h: CH,
  fill: { color: "EFF9FB" }, line: { color: BLUE, width: 2 }
});
// light gray grid: vlines x=702,745,788,831,873 ; hlines y=150,192,232,271,310
for (const gx of [702, 745, 788, 831, 873]) {
  s.addShape(pptx.shapes.LINE, { x: P(gx), y: P(80), w: 0, h: P(384 - 80), line: { color: "C9D4D8", width: 0.75 } });
}
for (const gy of [150, 192, 232, 271, 310]) {
  s.addShape(pptx.shapes.LINE, { x: P(661), y: P(gy), w: P(891 - 661), h: 0, line: { color: "C9D4D8", width: 0.75 } });
}
// red axes with arrowheads: y-axis x=661 (top arrow), x-axis y=350 (right arrow)
s.addShape(pptx.shapes.LINE, {
  x: P(661), y: P(90), w: 0, h: P(350 - 90),
  line: { color: RED2, width: 1.5, startArrowType: "triangle" }
});
s.addShape(pptx.shapes.LINE, {
  x: P(661), y: P(350), w: P(891 - 661), h: 0,
  line: { color: RED2, width: 1.5, endArrowType: "triangle" }
});
// axis labels: TPR rotated left of y-axis, FPR below x-axis
s.addText("TPR", {
  x: P(648) - P(60) / 2, y: P(220) - P(10) / 2, w: P(60), h: P(10),
  align: "center", valign: "middle", fontSize: 11, color: INK, fontFace: FONT, margin: 0, rotate: 270
});
s.addText("FPR", {
  x: P(756), y: P(360), w: P(784 - 756), h: P(368 - 360),
  align: "center", valign: "middle", fontSize: 11, color: INK, fontFace: FONT, margin: 0
});
// data point at threshold 0.0 -> (FPR=1, TPR=1) top-right: red circle at (874,149)
s.addShape(pptx.shapes.OVAL, {
  x: P(874) - P(10) / 2, y: P(149) - P(10) / 2, w: P(10), h: P(10),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1.5 }
});
s.addText("0.0", {
  x: P(862), y: P(119), w: P(882 - 862), h: P(131 - 119),
  align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0
});

// --- two stacked formula boxes (red borders), original outlines at y416..454 and y466..502 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(650), y: P(416), w: P(750 - 650), h: P(454 - 416),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 }
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(650), y: P(466), w: P(750 - 650), h: P(502 - 466),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 }
});
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
// eq_029_tpr.png: 712x240 px @600dpi -> 1.18667 x 0.4 in ; eq_029_fpr.png: 699x240 -> 1.165 x 0.4 in
const fcx = P(650) + P(100) / 2;
s.addImage({ path: ASSETS + "/eq_029_tpr.png", x: fcx - 1.18667 / 2, y: P(420), w: 1.18667, h: 0.4 });
s.addImage({ path: ASSETS + "/eq_029_fpr.png", x: fcx - 1.165 / 2, y: P(470), w: 1.165, h: 0.4 });

// --- generic confusion matrix (red border) x784..880 y446..499 ---
const GX = P(784), GY = P(446), GW = P(880 - 784), GH = P(499 - 446);
// cell fills first: TP (col1,row1) and TN (col2,row2) green; FN/FP white
s.addShape(pptx.shapes.RECTANGLE, { x: P(811), y: P(459), w: P(845 - 811), h: P(479 - 459), fill: { color: "7CFC00" }, line: { color: "none" } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(845), y: P(479), w: P(880 - 845), h: P(499 - 479), fill: { color: "7CFC00" }, line: { color: "none" } });
// border + grid
s.addShape(pptx.shapes.RECTANGLE, { x: GX, y: GY, w: GW, h: GH, fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 } });
// redraw green fills on top of white fill (fill covers nothing yet since border drawn after)
s.addShape(pptx.shapes.RECTANGLE, { x: P(811), y: P(459), w: P(845 - 811), h: P(479 - 459), fill: { color: "7CFC00" }, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(845), y: P(479), w: P(880 - 845), h: P(499 - 479), fill: { color: "7CFC00" }, line: { color: RED2, width: 0.75 } });
// grid lines
s.addShape(pptx.shapes.LINE, { x: P(811), y: P(452), w: 0, h: P(499 - 452), line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: P(845), y: P(452), w: 0, h: P(499 - 452), line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: P(811), y: P(452), w: P(880 - 811), h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: GX, y: P(459), w: GW, h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: GX, y: P(479), w: GW, h: 0, line: { color: RED2, width: 0.75 } });
// texts
s.addText("Predicted as", {
  x: P(811), y: GY, w: P(880 - 811), h: P(452 - 446),
  align: "center", valign: "middle", fontSize: 7, color: INK, fontFace: FONT, margin: 0
});
s.addText("P", { x: P(811), y: P(452), w: P(845 - 811), h: P(459 - 452), align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: P(845), y: P(452), w: P(880 - 845), h: P(459 - 452), align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0 });
s.addText("Actual", {
  x: P(784) + P(27) / 2 - P(40) / 2, y: P(479) - P(8) / 2, w: P(40), h: P(8),
  align: "center", valign: "middle", fontSize: 7, color: INK, fontFace: FONT, margin: 0, rotate: 270
});
s.addText("P", { x: GX, y: P(459), w: P(811 - 784), h: P(479 - 459), align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: GX, y: P(479), w: P(811 - 784), h: P(499 - 479), align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0 });
const gcell = (x0, x1, y0, y1, txt) => s.addText(txt, {
  x: P(x0), y: P(y0), w: P(x1 - x0), h: P(y1 - y0),
  align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0
});
gcell(811, 845, 459, 479, "TP");
gcell(845, 880, 459, 479, "FN");
gcell(811, 845, 479, 499, "FP");
gcell(845, 880, 479, 499, "TN");

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_029_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
