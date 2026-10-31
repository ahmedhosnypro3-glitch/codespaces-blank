const pptxgenpkg = require("pptxgenjs");

// Slide 29 — ROC Curve for Same Model -different thresholds (Threshold=0.0)
// Original frame 960x540 px; 1px = 1pt = 1/72 in. Geometry PIL-measured from
// unique_slides/slide_029.jpg (scratch/measure_029*.py).
// Drift items from pool_run/spec_gaps.md: 2D stacked fractions
// TPR = TP/(TP+FN) and FPR = FP/(FP+TN) as 600dpi mathtext PNGs (black ink,
// matching the original's measured formula ink).

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", HOUSE_RED = "C00000", BADGE = "FFF9C4", NUM = "333333";
const INK = "000000", RED2 = "C00000", BLUE = "000080", BLUE_INK = "0000FF";
const FONT = "Arial";
const P = (px) => px / 72; // px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE CHROME frame (root AGENTS.md 2026-10-09); badge+title drawn LAST ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 }
});

// --- outer content rectangle (red) x57..902 y42..518 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(57), y: P(42), w: P(902 - 57), h: P(518 - 42),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 2 }
});
// red vertical divider between left table and right panel (x=635)
s.addShape(pptx.shapes.LINE, {
  x: P(635), y: P(42), w: 0, h: P(518 - 42),
  line: { color: RED2, width: 2 }
});
// --- blue grid inside left table: vertical x=344, horizontals y=162,286,401 ---
s.addShape(pptx.shapes.LINE, {
  x: P(344), y: P(42), w: 0, h: P(518 - 42),
  line: { color: BLUE, width: 2 }
});
for (const gy of [162, 286, 401]) {
  s.addShape(pptx.shapes.LINE, {
    x: P(57), y: P(gy), w: P(635 - 57), h: 0,
    line: { color: BLUE, width: 2 }
  });
}

// --- top-left cell: threshold box (pink fill, red border) x68..173 y52..77 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(68), y: P(52), w: P(173 - 68), h: P(77 - 52),
  fill: { color: "F8DCC6" }, line: { color: RED2, width: 1.5 }
});
s.addText("Threshold=0.0", {
  x: P(68), y: P(52), w: P(173 - 68), h: P(77 - 52),
  align: "center", valign: "middle", fontSize: 13, color: RED2, fontFace: FONT, margin: 0
});

// --- top-left confusion matrix (red border) x80..218 y84..159 ---
const MX = P(80), MY = P(84), MW = P(218 - 80), MH = P(159 - 84);
s.addShape(pptx.shapes.RECTANGLE, {
  x: MX, y: MY, w: MW, h: MH,
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1.25 }
});
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
s.addText("Predicted as", {
  x: P(117), y: MY, w: P(218 - 117), h: P(92 - 84),
  align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0
});
s.addText("P", { x: P(117), y: P(92), w: P(166 - 117), h: P(112 - 92), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: P(166), y: P(92), w: P(218 - 166), h: P(112 - 92), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
// rotated "Actual" fully inside the label gutter x80..117 (center 98.5,134.5)
s.addText("Actual", {
  x: P(79.5), y: P(130.5), w: P(38), h: P(8),
  align: "center", valign: "middle", fontSize: 9, color: RED2, fontFace: FONT, margin: 0, rotate: 270
});
s.addText("P", { x: P(84), y: P(112), w: P(117 - 84), h: P(136 - 112), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: P(84), y: P(136), w: P(117 - 84), h: P(157 - 136), align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0 });
const cell = (cx0, cx1, cy0, cy1, txt, col) => s.addText(txt, {
  x: P(cx0), y: P(cy0), w: P(cx1 - cx0), h: P(cy1 - cy0),
  align: "center", valign: "middle", fontSize: 13, color: col, fontFace: FONT, margin: 0
});
cell(117, 166, 112, 136, "5", BLUE_INK);
cell(166, 218, 112, 136, "0", RED2);
cell(117, 166, 136, 157, "6", RED2);
cell(166, 218, 136, 157, "0", BLUE_INK);

// --- metrics box (pale yellow fill, red border) x224..341 y98..148 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(224), y: P(98), w: P(341 - 224), h: P(148 - 98),
  fill: { color: "F6F8DD" }, line: { color: RED2, width: 1.25 }
});
s.addText([
  { text: "TPR=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "5", options: { fontSize: 10, color: BLUE_INK, fontFace: FONT, breakLine: false } },
  { text: "/(5+0)=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "1", options: { fontSize: 10, color: BLUE_INK, fontFace: FONT, breakLine: true } },
  { text: "FPR=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "6", options: { fontSize: 10, color: RED2, fontFace: FONT, breakLine: false } },
  { text: "/(6+0)=", options: { fontSize: 10, color: INK, fontFace: FONT, breakLine: false } },
  { text: "1", options: { fontSize: 10, color: RED2, fontFace: FONT, breakLine: false } }
], {
  x: P(224), y: P(98), w: P(341 - 224), h: P(148 - 98),
  align: "center", valign: "middle", margin: 0, lineSpacing: 20
});

// --- bottom-center caption box (gray fill, blue border) x353..623 y425..477 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(353), y: P(425), w: P(623 - 353), h: P(477 - 425),
  fill: { color: "E7E6E4" }, line: { color: BLUE, width: 1.5 }
});
s.addText([
  { text: "ROC Curve for", options: { fontSize: 13, bold: true, color: RED2, fontFace: FONT, breakLine: true } },
  { text: "Same Model -different thresholds", options: { fontSize: 13, bold: true, color: RED2, fontFace: FONT, breakLine: false } }
], {
  x: P(353), y: P(425), w: P(623 - 353), h: P(477 - 425),
  align: "center", valign: "middle", margin: 0, lineSpacing: 24
});

// --- ROC chart: blue frame x641..895 y80..388, light fill ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(641), y: P(80), w: P(895 - 641), h: P(388 - 80),
  fill: { color: "ECFEFB" }, line: { color: BLUE, width: 2 }
});
// light gray grid: vlines x=702,745,788,831,873 ; hlines y=150,192,232,271,310
for (const gx of [702, 745, 788, 831, 873]) {
  s.addShape(pptx.shapes.LINE, { x: P(gx), y: P(80), w: 0, h: P(388 - 80), line: { color: "C3D6DA", width: 0.75 } });
}
for (const gy of [150, 192, 232, 271, 310]) {
  s.addShape(pptx.shapes.LINE, { x: P(641), y: P(gy), w: P(895 - 641), h: 0, line: { color: "C3D6DA", width: 0.75 } });
}
// red axes: y-axis x=661 y92..350 with up triangle head; x-axis y=350 x661..886 with right triangle head
s.addShape(pptx.shapes.LINE, {
  x: P(661), y: P(92), w: 0, h: P(350 - 92),
  line: { color: RED2, width: 1.5 }
});
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: P(656), y: P(84), w: P(10), h: P(8),
  fill: { color: RED2 }, line: { color: RED2, width: 0.5 }
});
s.addShape(pptx.shapes.LINE, {
  x: P(661), y: P(350), w: P(886 - 661), h: 0,
  line: { color: RED2, width: 1.5 }
});
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: P(886), y: P(345), w: P(8), h: P(10), rotate: 90,
  fill: { color: RED2 }, line: { color: RED2, width: 0.5 }
});
// axis labels: TPR rotated left of y-axis, FPR below x-axis
s.addText("TPR", {
  x: P(620), y: P(160), w: P(60), h: P(10),
  align: "center", valign: "middle", fontSize: 11, color: INK, fontFace: FONT, margin: 0, rotate: 270
});
s.addText("FPR", {
  x: P(750), y: P(358), w: P(90), h: P(12),
  align: "center", valign: "middle", fontSize: 11, color: INK, fontFace: FONT, margin: 0
});
// data point at threshold 0.0 -> (FPR=1, TPR=1): red open circle at (874,149), label "0.0" above
s.addShape(pptx.shapes.OVAL, {
  x: P(869), y: P(144), w: P(10), h: P(10),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1.5 }
});
s.addText("0.0", {
  x: P(862), y: P(119), w: P(20), h: P(12),
  align: "center", valign: "middle", fontSize: 10, color: INK, fontFace: FONT, margin: 0
});

// --- two stacked formula boxes (red borders) x650..750 y416..455 and y465..503 ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(650), y: P(416), w: P(750 - 650), h: P(455 - 416),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 }
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(650), y: P(465), w: P(750 - 650), h: P(503 - 465),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 }
});
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
// eq_029_*_black_attempt2.png: 712x240 / 699x240 px @600dpi -> 1.18667 x 0.4 / 1.165 x 0.4 in
s.addImage({ path: ASSETS + "/eq_029_tpr_black_attempt2.png", x: P(700) - 1.18667 / 2, y: P(421), w: 1.18667, h: 0.4 });
s.addImage({ path: ASSETS + "/eq_029_fpr_black_attempt2.png", x: P(700) - 1.165 / 2, y: P(470), w: 1.165, h: 0.4 });

// --- generic confusion matrix (red border) x762..887 y446..499 ---
const GX = P(762), GY = P(446), GW = P(887 - 762), GH = P(499 - 446);
// green fills first: TP (col1,row1) and TN (col2,row2)
s.addShape(pptx.shapes.RECTANGLE, { x: P(803), y: P(463), w: P(844 - 803), h: P(481 - 463), fill: { color: "8BFF10" }, line: { type: "none" } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(844), y: P(481), w: P(887 - 844), h: P(499 - 481), fill: { color: "8BFF10" }, line: { type: "none" } });
// frame + grid
s.addShape(pptx.shapes.RECTANGLE, { x: GX, y: GY, w: GW, h: GH, fill: { type: "none" }, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: P(803), y: GY, w: 0, h: GH, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: P(844), y: GY, w: 0, h: GH, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: P(803), y: P(455), w: P(887 - 803), h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: P(803), y: P(463), w: P(887 - 803), h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: GX, y: P(481), w: GW, h: 0, line: { color: RED2, width: 0.75 } });
// redraw green fills above grid lines
s.addShape(pptx.shapes.RECTANGLE, { x: P(803), y: P(463), w: P(844 - 803), h: P(481 - 463), fill: { color: "8BFF10" }, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.RECTANGLE, { x: P(844), y: P(481), w: P(887 - 844), h: P(499 - 481), fill: { color: "8BFF10" }, line: { color: RED2, width: 0.75 } });
// texts
s.addText("Predicted as", {
  x: P(803), y: GY, w: P(887 - 803), h: P(455 - 446),
  align: "center", valign: "middle", fontSize: 7, color: INK, fontFace: FONT, margin: 0
});
s.addText("P", { x: P(803), y: P(455), w: P(844 - 803), h: P(463 - 455), align: "center", valign: "middle", fontSize: 7, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: P(844), y: P(455), w: P(887 - 844), h: P(463 - 455), align: "center", valign: "middle", fontSize: 7, color: INK, fontFace: FONT, margin: 0 });
// rotated "Actual" fully inside gutter x762..803 (center 782.5,480)
s.addText("Actual", {
  x: P(763.5), y: P(476), w: P(38), h: P(8),
  align: "center", valign: "middle", fontSize: 7, color: RED2, fontFace: FONT, margin: 0, rotate: 270
});
s.addText("P", { x: GX, y: P(463), w: P(803 - 762), h: P(481 - 463), align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0 });
s.addText("N", { x: GX, y: P(481), w: P(803 - 762), h: P(499 - 481), align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0 });
const gcell = (x0, x1, y0, y1, txt) => s.addText(txt, {
  x: P(x0), y: P(y0), w: P(x1 - x0), h: P(y1 - y0),
  align: "center", valign: "middle", fontSize: 8, color: INK, fontFace: FONT, margin: 0
});
gcell(803, 844, 463, 481, "TP");
gcell(844, 887, 463, 481, "FN");
gcell(803, 844, 481, 499, "FP");
gcell(844, 887, 481, 499, "TN");

// --- HOUSE badge + title drawn LAST so no content shape can occlude them ---
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("29", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.28, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: HOUSE_RED, fontFace: FONT, margin: 0
});

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_029_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
