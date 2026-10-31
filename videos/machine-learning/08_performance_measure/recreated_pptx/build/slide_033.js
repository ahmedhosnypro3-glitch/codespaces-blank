const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
const SHAPES = pptx.shapes;
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", BADGE = "FFF9C4", NUM = "333333";
const INK = "000000", BLUE = "000080", DRED = "C00000", PINK = "FFC7CE";
const GREEN = "C6EFCE", CREAM = "F9FBE5", PLOTBG = "FFFFFF", GRID = "C8C8C8";
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
function line(x0, y0, x1, y1, color, w, dash) {
  const o = {
    x: P(Math.min(x0, x1)), y: P(Math.min(y0, y1)),
    w: P(Math.abs(x1 - x0)), h: P(Math.abs(y1 - y0)),
    line: { color, width: w || 1 }
  };
  if (dash) o.line.dash = { type: dash };
  s.addShape(SHAPES.LINE, o);
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
// rotated label: box is given in UNROTATED orientation (w = text line length)
function vtext(x, y, w, h, str, size, color, bold) {
  // x,y = final top-left of the rotated box; w,h = pre-rotation box size
  s.addText(str, {
    x: P(x), y: P(y), w: P(w), h: P(h),
    fontSize: size, color, bold: !!bold, fontFace: FONT, margin: 0,
    align: "center", valign: "middle", rotate: 270
  });
}

// --- left grid: red outer border x58..636 y48..516, blue divider x343, blue rows y162/287/401 ---
const GX0 = 58, GX1 = 636, GY0 = 48, GY1 = 516, GMID = 343;
const ROWS = [162, 287, 401];
line(GX0, GY0, GX1, GY0, DRED, 1.25);
line(GX0, GY1, GX1, GY1, DRED, 1.25);
line(GX0, GY0, GX0, GY1, DRED, 1.25);
line(GX1, GY0, GX1, GY1, DRED, 1.25);
line(GMID, GY0, GMID, GY1, BLUE, 1);
for (const ry of ROWS) line(GX0, ry, GX1, ry, BLUE, 1);

// --- confusion matrix panel ---
// panel cell top-left (px,py); header pink box; matrix cols mx: [80,117,165,216]-style; formulas cream box right
function panel(px, py, label, cells, tpr, fpr) {
  // threshold header: pink box x px+10..px+112, y py+7..py+28, red text ~10pt
  rect(px + 10, py + 7, 102, 21, PINK, DRED, 1);
  text(px + 10, py + 7, 102, 21, label, 10, DRED, true, { align: "center", valign: "middle" });
  // "Predicted as" red, centered over matrix cols
  const mx0 = px + 20, mx1 = px + 156, my0 = py + 60, my1 = py + 111;
  const cols = [mx0, mx0 + 37, mx0 + 85, mx1];
  const rows = [my0, my0 + 17, my0 + 34, my1];
  text(cols[1], my0 - 18, cols[3] - cols[1], 14, "Predicted as", 10, DRED, false, { align: "center", valign: "middle" });
  // grid lines (black thin)
  line(mx0, my0, mx1, my0, INK, 0.75);
  line(mx0, rows[1], mx1, rows[1], INK, 0.75);
  line(mx0, rows[2], mx1, rows[2], INK, 0.75);
  line(mx0, my1, mx1, my1, INK, 0.75);
  line(cols[1], my0, cols[1], my1, INK, 0.75);
  line(cols[2], my0, cols[2], my1, INK, 0.75);
  // header cells P / N (pink)
  rect(cols[1], my0, cols[2] - cols[1], rows[1] - my0, PINK, INK, 0.75);
  rect(cols[2], my0, mx1 - cols[2], rows[1] - my0, PINK, INK, 0.75);
  text(cols[1], my0, cols[2] - cols[1], rows[1] - my0, "P", 12, INK, true, { align: "center", valign: "middle" });
  text(cols[2], my0, mx1 - cols[2], rows[1] - my0, "N", 12, INK, true, { align: "center", valign: "middle" });
  // row label cells P / N (pink)
  rect(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], PINK, INK, 0.75);
  rect(mx0, rows[2], cols[1] - mx0, my1 - rows[2], PINK, INK, 0.75);
  text(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], "P", 12, INK, true, { align: "center", valign: "middle" });
  text(mx0, rows[2], cols[1] - mx0, my1 - rows[2], "N", 12, INK, true, { align: "center", valign: "middle" });
  // "Actual" rotated red, left of matrix, box wide enough to avoid wrapping
  vtext(mx0 - 26, rows[1] + (rows[2] - rows[1]) / 2 - 6, my1 - rows[1], 12, "Actual", 10, DRED, false);
  // data cells: row P red, row N blue, bold
  text(cols[1], rows[1], cols[2] - cols[1], rows[2] - rows[1], cells[0], 13, DRED, true, { align: "center", valign: "middle" });
  text(cols[2], rows[1], mx1 - cols[2], rows[2] - rows[1], cells[1], 13, DRED, true, { align: "center", valign: "middle" });
  text(cols[1], rows[2], cols[2] - cols[1], my1 - rows[2], cells[2], 13, BLUE, true, { align: "center", valign: "middle" });
  text(cols[2], rows[2], mx1 - cols[2], my1 - rows[2], cells[3], 13, BLUE, true, { align: "center", valign: "middle" });
  // TPR/FPR in cream box with red border, right of matrix; red label + blue body runs
  const fx = mx1 + 11, fw = 112, fy = my0 + 2, fh = 44;
  rect(fx, fy, fw, fh, CREAM, DRED, 0.75);
  const runs = (pfx, body) => [
    { text: pfx, options: { fontSize: 11, color: DRED, bold: false, fontFace: FONT } },
    { text: body, options: { fontSize: 11, color: BLUE, bold: false, fontFace: FONT } }
  ];
  s.addText(runs("TPR=", tpr), { x: P(fx + 3), y: P(fy + 4), w: P(fw - 6), h: P(18), margin: 0, valign: "middle" });
  s.addText(runs("FPR=", fpr), { x: P(fx + 3), y: P(fy + 24), w: P(fw - 6), h: P(18), margin: 0, valign: "middle" });
}

// panel cell tops: left column rows start at y 48/162/287/401; top-right panel in cell (343,48)
panel(58, 48, "Threshold=0.0", ["5", "0", "6", "0"], "5/(5+0)=1", "6/(6+0)=1");
panel(58, 162, "Threshold=0.1", ["5", "0", "4", "2"], "5/(5+0)=1", "4/(4+2)=0.66");
panel(58, 287, "Threshold=0.3", ["5", "0", "2", "4"], "5/(5+0)=1", "2/(2+4)=0.33");
panel(58, 401, "Threshold=0.4", ["4", "1", "1", "5"], "4/(4+1)=4/5", "1/(1+5)=0.16");
panel(343, 48, "Threshold=0.6", ["3", "1", "1", "5"], "3/(3+1)=0.6", "1/(1+5)=0.16");

// --- ROC caption box: white fill, blue border, red bold text, original line break ---
rect(341, 408, 318, 48, "FFFFFF", BLUE, 1);
s.addText([
  { text: "ROC Curve for", options: { fontSize: 15, bold: true, color: DRED, fontFace: FONT, breakLine: true } },
  { text: "Same Model -different thresholds", options: { fontSize: 15, bold: true, color: DRED, fontFace: FONT } }
], { x: P(341), y: P(408), w: P(318), h: P(48), align: "center", valign: "middle", margin: 0 });

// --- ROC plot: blue border x641..894 y81..387; axes red with arrowheads; open red-ring markers ---
rect(641, 81, 253, 306, PLOTBG, BLUE, 1);
// grid: vertical x = 660 + k*43.3 (0.2 steps to 873), horizontal y = 82 + k*~40
const gx0 = 660, gx1 = 873;
for (let k = 1; k <= 4; k++) line(Math.round(gx0 + (gx1 - gx0) * k / 5), 82, Math.round(gx0 + (gx1 - gx0) * k / 5), 350, GRID, 0.75);
for (let k = 1; k <= 6; k++) line(660, Math.round(82 + (350 - 82) * k / 7), 893, Math.round(82 + (350 - 82) * k / 7), GRID, 0.75);
// axes: y-axis x=662 from y=350 up to y=88 (arrow at top); x-axis y=350 from x=662 to x=890 (arrow right)
s.addShape(SHAPES.LINE, {
  x: P(662), y: P(88), w: 0, h: P(350 - 88),
  line: { color: "FF0000", width: 1.5, startArrowType: "arrow", endArrowType: "none" }
});
s.addShape(SHAPES.LINE, {
  x: P(662), y: P(350), w: P(890 - 662), h: 0,
  line: { color: "FF0000", width: 1.5, endArrowType: "arrow" }
});
// axis labels: TPR rotated (wide box), FPR horizontal wide enough
vtext(607, 211, 90, 16, "TPR", 14, DRED, true);
text(745, 358, 44, 16, "FPR", 14, DRED, true, { align: "center", valign: "middle" });
// markers: open circles (white fill, red outline) at measured centers; labels above (top row) / right-below (0.4, 0.6)
const pts = [
  { l: "0.3", x: 726, y: 150, lx: 713, ly: 122 },
  { l: "0.1", x: 810, y: 150, lx: 797, ly: 122 },
  { l: "0.0", x: 874, y: 149, lx: 861, ly: 122 },
  { l: "0.4", x: 690, y: 194, lx: 706, ly: 204 },
  { l: "0.6", x: 690, y: 234, lx: 706, ly: 244 }
];
for (const p of pts) {
  rect(p.lx - 2, p.ly - 1, 30, 16, "FFF2CC", "C00000", 0.5);
  s.addShape(SHAPES.OVAL, {
    x: P(p.x - 5.5), y: P(p.y - 5.5), w: P(11), h: P(11),
    fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 }
  });
  text(p.lx, p.ly, 26, 14, p.l, 11, INK, true, { align: "center", valign: "middle" });
}

// --- bottom-right: stacked-fraction PNGs (left) + legend matrix (right) ---
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
// cream+red border boxes behind the two fractions
rect(648, 408, 100, 34, CREAM, DRED, 0.75);
rect(648, 452, 100, 34, CREAM, DRED, 0.75);
s.addImage({ path: ASSETS + "/eq_033_tpr.png", x: P(652), y: P(412), w: 884 / 600, h: 198 / 600 });
s.addImage({ path: ASSETS + "/eq_033_fpr.png", x: P(652), y: P(456), w: 881 / 600, h: 198 / 600 });

// legend matrix: x 771..901, y 426..500; cols [771,803,844,901], rows [426,447,470,500]
text(803, 416, 90, 10, "Predicted as", 9, DRED, false, { align: "center", valign: "middle" });
const lx0 = 771, lx1 = 901, ly0 = 426, ly1 = 500;
const lc = [771, 803, 844, 901], lr = [426, 447, 470, 500];
line(lx0, ly0, lx1, ly0, INK, 0.75);
for (let i = 1; i < 3; i++) { line(lx0, lr[i], lx1, lr[i], INK, 0.75); line(lc[i], ly0, lc[i], ly1, INK, 0.75); }
line(lx0, ly1, lx1, ly1, INK, 0.75);
rect(lc[1], lr[0], lc[2] - lc[1], lr[1] - lr[0], PINK, INK, 0.75);
rect(lc[2], lr[0], lx1 - lc[2], lr[1] - lr[0], PINK, INK, 0.75);
text(lc[1], lr[0], lc[2] - lc[1], lr[1] - lr[0], "P", 10, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[0], lx1 - lc[2], lr[1] - lr[0], "N", 10, INK, true, { align: "center", valign: "middle" });
rect(lc[0], lr[1], lc[1] - lc[0], lr[2] - lr[1], PINK, INK, 0.75);
rect(lc[0], lr[2], lc[1] - lc[0], ly1 - lr[2], PINK, INK, 0.75);
text(lc[0], lr[1], lc[1] - lc[0], lr[2] - lr[1], "P", 10, INK, true, { align: "center", valign: "middle" });
text(lc[0], lr[2], lc[1] - lc[0], ly1 - lr[2], "N", 10, INK, true, { align: "center", valign: "middle" });
vtext(752, lr[1] + (lr[2] - lr[1]) / 2 - 5, ly1 - lr[1], 10, "Actual", 9, DRED, false);
rect(lc[1], lr[1], lc[2] - lc[1], lr[2] - lr[1], GREEN, INK, 0.75);
rect(lc[2], lr[2], lx1 - lc[2], ly1 - lr[2], GREEN, INK, 0.75);
text(lc[1], lr[1], lc[2] - lc[1], lr[2] - lr[1], "TP", 10, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[1], lx1 - lc[2], lr[2] - lr[1], "FN", 10, INK, true, { align: "center", valign: "middle" });
text(lc[1], lr[2], lc[2] - lc[1], ly1 - lr[2], "FP", 10, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[2], lx1 - lc[2], ly1 - lr[2], "TN", 10, INK, true, { align: "center", valign: "middle" });

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_033_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
