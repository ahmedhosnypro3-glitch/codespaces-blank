const pptxgenpkg = require("pptxgenjs");

// Slide 30 — "ROC Curve for Same Model -different thresholds" (fresh rebuild, agent-s30-fresh, v3).
// Original frame 960x540 px; 1px = 1pt = 1/72 in. All geometry PIL-measured from
// unique_slides/slide_030.jpg (panels are WHITE-filled with colored borders —
// the pink fills in the v1/v2 builds were a misread of JPEG-washed pixels):
//   outer RED rect x[59,900] y[48,516] fill white
//   blue lines: vert x=342 (y48..516); horiz y=162, y=288, y=401 (x59..635)
//   matrix panels: red border x[60,341] y[48,160] and y[167,284]
//   tan threshold header boxes x[71,170] y[55,75] / y[178,196] (fill F8DCC6)
//   matrix grids: x[116,225], vert x=166; m1 rows y92,112,136,157; m2 rows y212,234,256,279
//   "Predicted as" above each grid: m1 y[78,92], m2 y[198,212]; "Actual" rotated in gutter
//   metrics right of grids: TPR red #C00000, FPR blue #1F497D, bold, x[230,339]
//   ROC plot panel x[641,895] y[81,387] -> asset roc_030_v2.png (254x306 px)
//   title box x[353,622] y[426,474] white fill blue border, red bold text
//   bottom-right cell x[641,895] y[403,507] white fill blue border; formula box
//   x[649,752] y[415,500]; legend table x[784,880] y[440,500], TP/TN green #92D050,
//   FN/FP grey #F2F2F2
// Drift items (pool_run/spec_gaps.md slide_030): 2D stacked fractions
//   TPR = TP/(TP+FN), FPR = FP/(FP+TN) -> eq_030_v2_*.png (600dpi, TPR red, FPR #1F497D).
// House chrome (root AGENTS.md 2026-10-09): frame first (bg fill), badge+title LAST.

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";
const ASSETS = NS + "/recreated_pptx/build/assets";
const BG = "E8E8E8", RED = "C00000", DBLUE = "0000CC", INK = "000000";
const TAN = "F8DCC6", GREEN = "92D050", GREY = "F2F2F2", BADGE = "FFF9C4", NUM = "333333";
const FPRBLUE = "1F497D";
const FONT = "Arial";

const P = (px) => px / 72;
const rect = (x0, y0, x1, y1, fill, lineColor, lineW) => s.addShape(pptx.shapes.RECTANGLE, {
  x: P(x0), y: P(y0), w: P(x1 - x0), h: P(y1 - y0),
  fill: { color: fill }, line: { color: lineColor, width: lineW }
});
const hline = (x0, x1, y, color, w) => s.addShape(pptx.shapes.LINE, {
  x: P(x0), y: P(y), w: P(x1 - x0), h: 0, line: { color, width: w }
});
const vline = (x, y0, y1, color, w) => s.addShape(pptx.shapes.LINE, {
  x: P(x), y: P(y0), w: 0, h: P(y1 - y0), line: { color, width: w }
});
const txt = (x0, y0, x1, y1, text, size, color, bold, opts) => s.addText(text, Object.assign({
  x: P(x0), y: P(y0), w: P(x1 - x0), h: P(y1 - y0),
  align: "center", valign: "middle", fontSize: size, bold, color, fontFace: FONT, margin: 0
}, opts || {}));

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE red frame first (fill = bg gray) ---
rect(11, 11, 949, 529, BG, RED, 1.5); // 0.15in,13.03in,7.2in in frame px

// --- outer red content rect ---
rect(59, 48, 900, 516, "FFFFFF", RED, 1.5);

// --- blue structural lines ---
vline(342, 48, 516, DBLUE, 1.25);
hline(59, 635, 162, DBLUE, 1.25);
hline(59, 635, 288, DBLUE, 1.25);
hline(59, 635, 401, DBLUE, 1.25);

// --- confusion matrix panels ---
function matrixPanel(py, pend, header, ty, rows, cells) {
  // py..pend panel (red border, white fill); header tan box; grid at ty with 3 bands
  rect(60, py, 341, pend, "FFFFFF", RED, 1.25);
  rect(71, py + 7, 170, py + 27, TAN, RED, 1);
  txt(71, py + 7, 170, py + 27, header, 13, RED, true);
  // "Predicted as" above the grid
  txt(116, ty - 14, 225, ty, "Predicted as", 8, INK, true);
  // grid
  rect(116, ty, 225, rows[2], "FFFFFF", RED, 1);
  vline(166, ty, rows[2], RED, 1);
  hline(116, 225, rows[0], RED, 1);
  hline(116, 225, rows[1], RED, 1);
  // column headers P N
  txt(116, ty, 166, rows[0], "P", 10, INK, true);
  txt(166, ty, 225, rows[0], "N", 10, INK, true);
  // row labels via rotated "Actual" in the gutter + P/N row labels
  txt(63, ty + 6, 111, ty + 65, "Actual", 8, INK, true, { rotate: 270 });
  txt(60, rows[0], 116, rows[1], "P", 10, INK, true);
  txt(60, rows[1], 116, rows[2], "N", 10, INK, true);
  // cell values: [PP, PN, NP, NN] colors [cPP, cPN, cNP, cNN]
  const c = (cx0, cx1, cy0, cy1, t, col) => txt(cx0, cy0, cx1, cy1, t, 13, col, true);
  c(116, 166, rows[0], rows[1], cells[0][0], cells[0][1]);
  c(166, 225, rows[0], rows[1], cells[1][0], cells[1][1]);
  c(116, 166, rows[1], rows[2], cells[2][0], cells[2][1]);
  c(166, 225, rows[1], rows[2], cells[3][0], cells[3][1]);
  // worked metrics right of the grid: TPR red, FPR blue
  s.addText([
    { text: cells[4], options: { fontSize: 10.5, color: RED, bold: true, fontFace: FONT, breakLine: true } },
    { text: cells[5], options: { fontSize: 10.5, color: FPRBLUE, bold: true, fontFace: FONT, breakLine: true } },
  ], { x: P(230), y: P(ty + 16), w: P(339 - 230), h: P(44), margin: 0, lineSpacing: 15 });
}

matrixPanel(48, 160, "Threshold=0.0", 92, [112, 136, 157],
  [["5", RED], ["0", INK], ["6", RED], ["0", INK], "TPR=5/(5+0)=1", "FPR=6/(6+0)=1"]);
matrixPanel(167, 284, "Threshold=0.1", 212, [234, 256, 279],
  [["5", RED], ["0", INK], ["4", RED], ["2", INK], "TPR=5/(5+0)=1", "FPR=4/(4+2)=0.66"]);

// --- ROC plot panel (generated image, whole panel baked) ---
s.addImage({ path: ASSETS + "/roc_030_v2.png", x: P(641), y: P(81), w: P(254), h: P(306) });

// --- title box (white fill, blue border) ---
rect(353, 426, 622, 474, "FFFFFF", DBLUE, 1.25);
txt(358, 428, 612, 470, "ROC Curve for Same Model -different thresholds", 13, RED, true);

// --- bottom-right cell (white fill, blue border) ---
rect(641, 403, 895, 507, "FFFFFF", DBLUE, 1.25);
rect(649, 415, 752, 500, "FFFFFF", DBLUE, 1.25);
// drift equations as professional 2D fractions (600dpi PNG, exact size)
s.addImage({ path: ASSETS + "/eq_030_v2_tpr.png", x: P(656), y: P(424), w: 728 / 600, h: 230 / 600 });
s.addImage({ path: ASSETS + "/eq_030_v2_fpr.png", x: P(656), y: P(462), w: 725 / 600, h: 230 / 600 });

// --- legend 2x2 key: x[784,880] y[440,500]; cols 784-811-850-880; rows 440-460-480-500 ---
rect(784, 440, 880, 500, "FFFFFF", INK, 0.75);
rect(811, 460, 850, 480, GREEN, INK, 0.75);   // TP
rect(850, 480, 880, 500, GREEN, INK, 0.75);   // TN
rect(850, 460, 880, 480, GREY, INK, 0.75);    // FN
rect(811, 480, 850, 500, GREY, INK, 0.75);    // FP
vline(811, 440, 500, INK, 0.75);
vline(850, 440, 500, INK, 0.75);
hline(784, 880, 460, INK, 0.75);
hline(784, 880, 480, INK, 0.75);
txt(784, 425, 880, 440, "Predicted as", 7, INK, true);
txt(811, 440, 850, 460, "P", 7, INK, true);
txt(850, 440, 880, 460, "N", 7, INK, true);
txt(784, 460, 811, 500, "Actual", 7, INK, true, { rotate: 270 });
txt(784, 460, 811, 480, "P", 8, INK, true);
txt(784, 480, 811, 500, "N", 8, INK, true);
txt(811, 460, 850, 480, "TP", 8, INK, true);
txt(850, 460, 880, 480, "FN", 8, INK, true);
txt(811, 480, 850, 500, "FP", 8, INK, true);
txt(850, 480, 880, 500, "TN", 8, INK, true);

// --- HOUSE badge + title LAST ---
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("30", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.28, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: RED, fontFace: FONT, margin: 0
});

const outPath = NS + "/recreated_pptx/slide_030_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
