const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
const SHAPES = pptx.shapes;
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", BADGE = "FFF9C4", NUM = "333333";
const INK = "000000", BLUE = "000080", PINK = "FFC7CE", GREEN = "92D050";
const CREAM = "FFF2CC", GRAYBOX = "E7E9E6", PLOTBG = "EEFEFB", GRID = "C8C8C8";
const FONT = "Arial";
const P = (px) => px / 72; // original frame: 960x540 px == 13.333x7.5 in, 1px = 1pt

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE CHROME (root AGENTS.md) ---
s.addShape(SHAPES.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 }
});
s.addShape(SHAPES.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("33", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});

// --- helpers ---
function line(x0, y0, x1, y1, color, w) {
  s.addShape(SHAPES.LINE, {
    x: P(Math.min(x0, x1)), y: P(Math.min(y0, y1)),
    w: P(Math.abs(x1 - x0)), h: P(Math.abs(y1 - y0)),
    line: { color, width: w || 1 }
  });
}
function rect(x, y, w, h, fill, lineColor, lineW) {
  const o = { x: P(x), y: P(y), w: P(w), h: P(h) };
  if (fill) o.fill = { color: fill }; else o.fill = { type: "none" };
  if (lineColor) o.line = { color: lineColor, width: lineW || 1 };
  s.addShape(SHAPES.RECTANGLE, o);
}
function text(x, y, w, h, str, size, color, bold, opts) {
  s.addText(str, Object.assign({
    x: P(x), y: P(y), w: P(w), h: P(h),
    fontSize: size, color, bold: !!bold, fontFace: FONT, margin: 0
  }, opts || {}));
}

// --- left grid: x 58..635, rows y 43/163/287/401/518, divider x 343 ---
const GX0 = 58, GX1 = 635, GY0 = 43, GY1 = 518, GMID = 343;
const ROWS = [43, 163, 287, 401, 518];
line(GX0, GY0, GX1, GY0, BLUE, 1);
line(GX0, GY1, GX1, GY1, BLUE, 1);
line(GX0, GY0, GX0, GY1, BLUE, 1);
line(GX1, GY0, GX1, GY1, BLUE, 1);
line(GMID, GY0, GMID, GY1, BLUE, 1);
for (let i = 1; i < ROWS.length - 1; i++) line(GX0, ROWS[i], GX1, ROWS[i], BLUE, 1);
// right column divider + its bottom edge
line(901, GY0, 901, 517, BLUE, 1);
line(635, 517, 901, 517, BLUE, 1);

// --- confusion matrix panel ---
// panel: matrix grid x 80..216 (cols 80/117/165/216), rows y 92/113/136/157 (panel1 coords)
// per-panel vertical offset dy: panel row top ROWS[k]; header box y = top+10..top+33
function panel(dy, label, cells, tpr, fpr) {
  // threshold header: cream box x 68..172, y dy+10..dy+33, red bold text
  rect(68, dy + 10, 104, 23, CREAM, RED, 1);
  text(68, dy + 10, 104, 23, label, 15, RED, true, { align: "center", valign: "middle" });
  // "Predicted as" above matrix, centered over cols 117..216
  text(117, dy + 37, 99, 12, "Predicted as", 12, INK, false, { align: "center", valign: "middle" });
  // matrix grid
  const mx0 = 80, mx1 = 216, my0 = dy + 49, my1 = dy + 114;
  const cols = [80, 117, 165, 216], rows = [my0, my0 + 21, my0 + 44, my1];
  line(mx0, my0, mx1, my0, INK, 1);
  line(mx0, rows[1], mx1, rows[1], INK, 1);
  line(mx0, rows[2], mx1, rows[2], INK, 1);
  line(mx0, my1, mx1, my1, INK, 1);
  line(cols[1], my0, cols[1], my1, INK, 1);
  line(cols[2], my0, cols[2], my1, INK, 1);
  line(mx0, rows[1], cols[1], rows[1], INK, 1); // col0 starts at row1
  // header cells P / N (pink)
  rect(cols[1], my0, cols[2] - cols[1], rows[1] - my0, PINK, INK, 1);
  rect(cols[2], my0, mx1 - cols[2], rows[1] - my0, PINK, INK, 1);
  text(cols[1], my0, cols[2] - cols[1], rows[1] - my0, "P", 13, INK, true, { align: "center", valign: "middle" });
  text(cols[2], my0, mx1 - cols[2], rows[1] - my0, "N", 13, INK, true, { align: "center", valign: "middle" });
  // row label cells P / N (pink)
  rect(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], PINK, INK, 1);
  rect(mx0, rows[2], cols[1] - mx0, my1 - rows[2], PINK, INK, 1);
  text(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], "P", 13, INK, true, { align: "center", valign: "middle" });
  text(mx0, rows[2], cols[1] - mx0, my1 - rows[2], "N", 13, INK, true, { align: "center", valign: "middle" });
  // "Actual" rotated, left of table
  text(mx0 - 22, rows[1], 14, my1 - rows[1], "Actual", 12, INK, false,
    { align: "center", valign: "middle", rotate: 270 });
  // data cells: cells = [pp, pn, np, nn]; row P numbers red, row N numbers blue
  const cw1 = cols[2] - cols[1], cw2 = mx1 - cols[2];
  const rh1 = rows[2] - rows[1], rh2 = my1 - rows[2];
  text(cols[1], rows[1], cw1, rh1, cells[0], 14, RED, true, { align: "center", valign: "middle" });
  text(cols[2], rows[1], cw2, rh1, cells[1], 14, RED, true, { align: "center", valign: "middle" });
  text(cols[1], rows[2], cw1, rh2, cells[2], 14, BLUE, true, { align: "center", valign: "middle" });
  text(cols[2], rows[2], cw2, rh2, cells[3], 14, BLUE, true, { align: "center", valign: "middle" });
  // TPR/FPR lines right of matrix
  text(224, dy + 55, 116, 18, tpr, 13, INK, false, { align: "left", valign: "middle" });
  text(224, dy + 88, 116, 18, fpr, 13, INK, false, { align: "left", valign: "middle" });
}

panel(ROWS[0], "Threshold=0.0", ["5", "0", "6", "0"], "TPR=5/(5+0)=1", "FPR=6/(6+0)=1");
panel(ROWS[1], "Threshold=0.1", ["5", "0", "4", "2"], "TPR=5/(5+0)=1", "FPR=4/(4+2)=0.66");
panel(ROWS[2], "Threshold=0.3", ["5", "0", "2", "4"], "TPR=5/(5+0)=1", "FPR=2/(2+4)=0.33");
panel(ROWS[3], "Threshold=0.4", ["4", "1", "1", "5"], "TPR=4/(4+1)=4/5", "FPR=1/(1+5)=0.16");
// top-center panel: Threshold=0.6, matrix shifted +285 x, header x 350..466
function panel06() {
  const dx = 285, dy = ROWS[0];
  rect(350, dy + 12, 116, 23, CREAM, RED, 1);
  text(350, dy + 12, 116, 23, "Threshold=0.6", 15, RED, true, { align: "center", valign: "middle" });
  text(402, dy + 37, 99, 12, "Predicted as", 12, INK, false, { align: "center", valign: "middle" });
  const mx0 = 365, mx1 = 501, my0 = dy + 49, my1 = dy + 114;
  const cols = [365, 402, 450, 501], rows = [my0, my0 + 21, my0 + 44, my1];
  line(mx0, my0, mx1, my0, INK, 1);
  line(mx0, rows[1], mx1, rows[1], INK, 1);
  line(mx0, rows[2], mx1, rows[2], INK, 1);
  line(mx0, my1, mx1, my1, INK, 1);
  line(cols[1], my0, cols[1], my1, INK, 1);
  line(cols[2], my0, cols[2], my1, INK, 1);
  rect(cols[1], my0, cols[2] - cols[1], rows[1] - my0, PINK, INK, 1);
  rect(cols[2], my0, mx1 - cols[2], rows[1] - my0, PINK, INK, 1);
  text(cols[1], my0, cols[2] - cols[1], rows[1] - my0, "P", 13, INK, true, { align: "center", valign: "middle" });
  text(cols[2], my0, mx1 - cols[2], rows[1] - my0, "N", 13, INK, true, { align: "center", valign: "middle" });
  rect(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], PINK, INK, 1);
  rect(mx0, rows[2], cols[1] - mx0, my1 - rows[2], PINK, INK, 1);
  text(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], "P", 13, INK, true, { align: "center", valign: "middle" });
  text(mx0, rows[2], cols[1] - mx0, my1 - rows[2], "N", 13, INK, true, { align: "center", valign: "middle" });
  text(mx0 - 22, rows[1], 14, my1 - rows[1], "Actual", 12, INK, false,
    { align: "center", valign: "middle", rotate: 270 });
  const cells = ["3", "1", "1", "5"];
  text(cols[1], rows[1], cols[2] - cols[1], rows[2] - rows[1], cells[0], 14, RED, true, { align: "center", valign: "middle" });
  text(cols[2], rows[1], mx1 - cols[2], rows[2] - rows[1], cells[1], 14, RED, true, { align: "center", valign: "middle" });
  text(cols[1], rows[2], cols[2] - cols[1], my1 - rows[2], cells[2], 14, BLUE, true, { align: "center", valign: "middle" });
  text(cols[2], rows[2], mx1 - cols[2], my1 - rows[2], cells[3], 14, BLUE, true, { align: "center", valign: "middle" });
  text(509, dy + 55, 120, 18, "TPR=3/(3+1)=0.6", 13, INK, false, { align: "left", valign: "middle" });
  text(509, dy + 88, 120, 18, "FPR=1/(1+5)=0.16", 13, INK, false, { align: "left", valign: "middle" });
}
panel06();

// --- ROC title box (center-bottom): x 353..622, y 426..476 ---
rect(353, 426, 269, 50, GRAYBOX, "5B5BD6", 1);
text(353, 426, 269, 50,
  [{ text: "ROC Curve for Same Model", options: { fontSize: 16, bold: true, color: RED, fontFace: FONT, breakLine: true } },
   { text: "-different thresholds", options: { fontSize: 16, bold: true, color: RED, fontFace: FONT } }],
  { x: P(353), y: P(426), w: P(269), h: P(50), align: "center", valign: "middle", margin: 0 });

// --- ROC plot: box x 642..894 y 81..387, light cyan fill ---
rect(642, 81, 252, 306, PLOTBG, "5A5DA8", 1);
// grid: 0.2 steps; FPR: x = 661 + 214*k ; TPR: y = 351 - 204*k
for (let k = 1; k <= 4; k++) {
  line(Math.round(661 + 214 * k / 5), 84, Math.round(661 + 214 * k / 5), 351, GRID, 0.75);
  line(661, Math.round(351 - 204 * k / 5), 890, Math.round(351 - 204 * k / 5), GRID, 0.75);
}
// axes (red, arrowheads via line endArrowType): y-axis x=661 y 351->84 ; x-axis y=351 x 661->890
s.addShape(SHAPES.LINE, {
  x: P(661), y: P(84), w: 0, h: P(351 - 84),
  line: { color: "FF0000", width: 1.75, endArrowType: "arrow" }
});
s.addShape(SHAPES.LINE, {
  x: P(661), y: P(351), w: P(890 - 661), h: 0,
  line: { color: "FF0000", width: 1.75, endArrowType: "arrow" }
});
// axis labels
text(646, 180, 14, 90, "TPR", 16, INK, true, { align: "center", valign: "middle", rotate: 270 });
text(756, 357, 28, 14, "FPR", 16, INK, true, { align: "center", valign: "middle" });
// data points (FPR,TPR): 0.0->(1,1) 0.1->(0.667,1) 0.3->(0.333,1) 0.4->(0.167,0.8) 0.6->(0.167,0.6)
const fx = (f) => 661 + 214 * f, fy = (t) => 351 - 204 * t;
const pts = [
  { l: "0.6", f: 1 / 6, t: 0.6 }, { l: "0.4", f: 1 / 6, t: 0.8 },
  { l: "0.3", f: 1 / 3, t: 1 }, { l: "0.1", f: 2 / 3, t: 1 }, { l: "0.0", f: 1, t: 1 }
];
// dashed red polyline through points in threshold order
for (let i = 0; i < pts.length - 1; i++) {
  const a = pts[i], b = pts[i + 1];
  s.addShape(SHAPES.LINE, {
    x: P(Math.min(fx(a.f), fx(b.f))), y: P(Math.min(fy(a.t), fy(b.t))),
    w: P(Math.abs(fx(b.f) - fx(a.f))), h: P(Math.abs(fy(b.t) - fy(a.t))),
    line: { color: "FF0000", width: 1.25, dash: { type: "dash" } }
  });
}
for (const p of pts) {
  s.addShape(SHAPES.OVAL, {
    x: P(fx(p.f) - 5), y: P(fy(p.t) - 5), w: P(10), h: P(10),
    fill: { color: "FF0000" }, line: { color: "FF0000", width: 1 }
  });
}
// point labels (threshold values), placed left/above the points
text(713, 122, 22, 14, "0.3", 12, INK, true, { align: "center", valign: "middle" });
text(776, 140, 22, 14, "0.1", 12, INK, true, { align: "center", valign: "middle" });
text(848, 140, 22, 14, "0.0", 12, INK, true, { align: "center", valign: "middle" });
text(664, 180, 22, 14, "0.4", 12, INK, true, { align: "center", valign: "middle" });
text(664, 222, 22, 14, "0.6", 12, INK, true, { align: "center", valign: "middle" });

// --- bottom-right stacked-fraction equations (600dpi PNG, exact size) ---
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
s.addImage({ path: ASSETS + "/eq_033_tpr.png", x: P(650), y: P(416), w: 2.59833, h: 0.56333 });
s.addImage({ path: ASSETS + "/eq_033_fpr.png", x: P(651), y: P(465), w: 2.59167, h: 0.56333 });

// --- legend matrix: x 771..886, y 438..499 (cols 771/803/844/886, rows 438/457/478/499) ---
text(803, 428, 83, 10, "Predicted as", 10, INK, false, { align: "center", valign: "middle" });
const lx0 = 771, lx1 = 886, ly0 = 438, ly1 = 499;
const lc = [771, 803, 844, 886], lr = [438, 457, 478, 499];
line(lx0, ly0, lx1, ly0, INK, 1);
for (let i = 1; i < 3; i++) { line(lx0, lr[i], lx1, lr[i], INK, 1); line(lc[i], ly0, lc[i], ly1, INK, 1); }
line(lx0, ly1, lx1, ly1, INK, 1);
// header P/N pink
rect(lc[1], lr[0], lc[2] - lc[1], lr[1] - lr[0], PINK, INK, 1);
rect(lc[2], lr[0], lx1 - lc[2], lr[1] - lr[0], PINK, INK, 1);
text(lc[1], lr[0], lc[2] - lc[1], lr[1] - lr[0], "P", 11, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[0], lx1 - lc[2], lr[1] - lr[0], "N", 11, INK, true, { align: "center", valign: "middle" });
// row labels P/N pink
rect(lc[0], lr[1], lc[1] - lc[0], lr[2] - lr[1], PINK, INK, 1);
rect(lc[0], lr[2], lc[1] - lc[0], ly1 - lr[2], PINK, INK, 1);
text(lc[0], lr[1], lc[1] - lc[0], lr[2] - lr[1], "P", 11, INK, true, { align: "center", valign: "middle" });
text(lc[0], lr[2], lc[1] - lc[0], ly1 - lr[2], "N", 11, INK, true, { align: "center", valign: "middle" });
// Actual rotated left of legend
text(757, lr[1], 12, ly1 - lr[1], "Actual", 10, INK, false, { align: "center", valign: "middle", rotate: 270 });
// cells: TP green, TN green, FN/FP plain
rect(lc[1], lr[1], lc[2] - lc[1], lr[2] - lr[1], GREEN, INK, 1);
rect(lc[2], lr[2], lx1 - lc[2], ly1 - lr[2], GREEN, INK, 1);
text(lc[1], lr[1], lc[2] - lc[1], lr[2] - lr[1], "TP", 11, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[1], lx1 - lc[2], lr[2] - lr[1], "FN", 11, INK, true, { align: "center", valign: "middle" });
text(lc[1], lr[2], lc[2] - lc[1], ly1 - lr[2], "FP", 11, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[2], lx1 - lc[2], ly1 - lr[2], "TN", 11, INK, true, { align: "center", valign: "middle" });

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_033_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
