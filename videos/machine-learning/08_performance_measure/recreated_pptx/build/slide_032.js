const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";      // house frame
const RED2 = "FF0000";     // original slide's red accents
const BLUE = "0000FF";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLACK = "000000";
const GREEN = "90EE90";
const FONT = "Arial";

const P = (px) => px / 72; // 960x540 frame, 1px = 1pt = 1/72 in

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides everything)
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
s.addText("32", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// ORIGINAL CONTENT (measured from unique_slides/slide_032.jpg, 960x540)
// ============================================================

// Left column: red-bordered box x[60,340] y[48,516], white fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(60), y: P(48), w: P(340 - 60), h: P(516 - 48),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1.5 },
});
// internal vertical divider of left column at x=224
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(224), y: P(48), w: P(2), h: P(516 - 48),
  fill: { color: RED2 }, line: { type: "none" },
});

// Four threshold panels, stacked: tops at y = 48, 165, 282, 399 (height 117 each)
const panels = [
  { th: "Threshold=0.0", cells: [["5", "0"], ["6", "0"]], tpr: "TPR=5/(5+0)=1", fpr: "FPR=6/(6+0)=1" },
  { th: "Threshold=0.1", cells: [["5", "0"], ["4", "2"]], tpr: "TPR=5/(5+0)=1", fpr: "FPR=4/(4+2)=.66" },
  { th: "Threshold=0.3", cells: [["5", "0"], ["2", "4"]], tpr: "TPR=5/(5+0)=1", fpr: "FPR=2/(2+4)=.33" },
  { th: "Threshold=0.4", cells: [["4", "1"], ["1", "5"]], tpr: "TPR=4/(4+1)=4/5", fpr: "FPR=1/(1+5)=.16" },
];
const panelTop = [48, 165, 282, 399];
const panelH = 117;

panels.forEach((p, i) => {
  const y0 = P(panelTop[i]);
  // threshold label, red bold, top-left of panel
  s.addText(p.th, {
    x: P(66), y: y0 + P(6), w: P(150), h: P(14),
    align: "left", valign: "middle",
    fontSize: 10, bold: true, color: RED2, fontFace: FONT, margin: 0,
  });
  // confusion matrix: 3 cols x 3 rows; cols at x 80..215, rows y0+30 .. y0+105
  const tx = P(80), ty = y0 + P(30), tw = P(135), th = P(75);
  const rows = [
    ["Predicted as", "P", "N"],
    ["Actual P", p.cells[0][0], p.cells[0][1]],
    ["Actual N", p.cells[1][0], p.cells[1][1]],
  ];
  s.addTable(rows, {
    x: tx, y: ty, w: tw, h: th,
    colW: [P(55), P(40), P(40)],
    border: { type: "solid", color: RED2, pt: 1 },
    fill: { color: "FFFFFF" },
    fontSize: 9, color: BLACK, fontFace: FONT, bold: false,
    align: "center", valign: "middle", margin: 0,
  });
  // TPR / FPR calc text right of the matrix (x 225..335)
  s.addText([
    { text: p.tpr, options: { fontSize: 9, color: BLACK, fontFace: FONT, breakLine: true } },
    { text: p.fpr, options: { fontSize: 9, color: BLACK, fontFace: FONT, breakLine: true } },
  ], {
    x: P(228), y: ty, w: P(108), h: th,
    align: "left", valign: "top", margin: 0, lineSpacing: 14,
  });
});

// Blue vertical divider at x=342, spanning content height y[43,516]
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(342), y: P(43), w: P(2), h: P(516 - 43),
  fill: { color: BLUE }, line: { type: "none" },
});

// ROC plot: generated matplotlib PNG at measured box x[634,902] y[43,344]
// PNG is 2233x2508 px at 600dpi -> w = px/600 in
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/roc_032.png",
  x: P(634), y: P(43), w: 2233 / 600, h: 2508 / 600,
});

// Center-bottom red-bordered title box: x[345,634] y[435,475]
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(345), y: P(435), w: P(634 - 345), h: P(475 - 435),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1.5 },
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: P(345), y: P(435), w: P(634 - 345), h: P(475 - 435),
  align: "center", valign: "middle",
  fontSize: 12, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});

// Bottom-right: TPR / FPR fraction definitions (2D professional format PNGs)
// eq PNGs are 881x294 / 878x294 px at 600dpi
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_032_tpr.png",
  x: P(640), y: P(415), w: 881 / 600, h: 294 / 600,
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_032_fpr.png",
  x: P(640), y: P(468), w: 878 / 600, h: 294 / 600,
});

// Bottom-right legend confusion matrix x[800,902] y[428,499], TP/TN green cells
const lx = P(800), ly = P(428), lw = P(102), lh = P(71);
s.addTable(
  [
    ["Predicted as", "P", "N"],
    ["Actual P", "TP", "FN"],
    ["Actual N", "FP", "TN"],
  ],
  {
    x: lx, y: ly, w: lw, h: lh,
    colW: [P(42), P(30), P(30)],
    border: { type: "solid", color: BLACK, pt: 1 },
    fill: { color: "FFFFFF" },
    fontSize: 9, color: BLACK, fontFace: FONT,
    align: "center", valign: "middle", margin: 0,
  }
);
// green fills for TP (row1,col1) and TN (row2,col2) — overlay green cells
s.addShape(pptx.shapes.RECTANGLE, {
  x: lx + P(42), y: ly + P(71 / 3), w: P(30), h: P(71 / 3),
  fill: { color: GREEN }, line: { color: BLACK, width: 1 },
});
s.addText("TP", {
  x: lx + P(42), y: ly + P(71 / 3), w: P(30), h: P(71 / 3),
  align: "center", valign: "middle", fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: lx + P(72), y: ly + P(142 / 3), w: P(30), h: P(71 / 3),
  fill: { color: GREEN }, line: { color: BLACK, width: 1 },
});
s.addText("TN", {
  x: lx + P(72), y: ly + P(142 / 3), w: P(30), h: P(71 / 3),
  align: "center", valign: "middle", fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_032_recreated.pptx",
});
console.log("written slide_032_recreated.pptx");
