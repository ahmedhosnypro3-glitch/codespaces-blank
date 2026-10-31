const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
const SHAPES = pptx.shapes;
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", BADGE = "FFF9C4", NUM = "333333";
const DRED = "8B0000";   // original slide's dark red text/frame
const INK = "000000", PINK = "FFC7CE", GREEN = "92D050", REDFILL = "FFC7CE";
const CREAM = "FFF2CC";
const FONT = "Arial";
const P = (px) => px / 72; // original frame 960x540, 1px = 1pt = 1/72 in
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE CHROME (root AGENTS.md 2026-10-09) ---
s.addShape(SHAPES.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 }
});
s.addShape(SHAPES.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("36", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
// top title band stays empty: the original frame has no text there
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle", margin: 0
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
  o.fill = fill ? { color: fill } : { type: "none" };
  if (lineColor) o.line = { color: lineColor, width: lineW || 1 };
  s.addShape(SHAPES.RECTANGLE, o);
}
function text(x, y, w, h, str, size, color, bold, opts) {
  s.addText(str, Object.assign({
    x: P(x), y: P(y), w: P(w), h: P(h),
    fontSize: size, color, bold: !!bold, fontFace: FONT, margin: 0
  }, opts || {}));
}

// --- original content frame: dark red border x[58,901] y[43,517] ---
rect(58, 43, 901 - 58, 517 - 43, null, DRED, 1.5);
// vertical divider between middle column and plot region at x=635
line(635, 43, 635, 517, DRED, 1);

// --- confusion matrix panel (geometry measured from the original) ---
// panel(dx, dy, label, cells, tpr, fpr); header box, "Predicted as", 2x2 grid, formulas
function panel(dx, dy, label, cells, tpr, fpr) {
  rect(68 + dx, dy + 10, 104, 23, "FFFFFF", DRED, 1);
  text(68 + dx, dy + 10, 104, 23, label, 12, DRED, true, { align: "center", valign: "middle" });
  text(117 + dx, dy + 37, 99, 12, "Predicted as", 12, DRED, false, { align: "center", valign: "middle" });
  const mx0 = 80 + dx, mx1 = 216 + dx, my0 = dy + 49, my1 = dy + 114;
  const cols = [mx0, mx0 + 37, mx0 + 85, mx1];
  const rows = [my0, my0 + 21, my0 + 44, my1];
  line(mx0, my0, mx1, my0, DRED, 1);
  line(mx0, rows[1], mx1, rows[1], DRED, 1);
  line(mx0, rows[2], mx1, rows[2], DRED, 1);
  line(mx0, my1, mx1, my1, DRED, 1);
  line(cols[1], my0, cols[1], my1, DRED, 1);
  line(cols[2], my0, cols[2], my1, DRED, 1);
  // header cells P / N
  rect(cols[1], my0, cols[2] - cols[1], rows[1] - my0, PINK, INK, 1);
  rect(cols[2], my0, mx1 - cols[2], rows[1] - my0, PINK, INK, 1);
  text(cols[1], my0, cols[2] - cols[1], rows[1] - my0, "P", 13, INK, true, { align: "center", valign: "middle" });
  text(cols[2], my0, mx1 - cols[2], rows[1] - my0, "N", 13, INK, true, { align: "center", valign: "middle" });
  // row label cells P / N
  rect(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], PINK, INK, 1);
  rect(mx0, rows[2], cols[1] - mx0, my1 - rows[2], PINK, INK, 1);
  text(mx0, rows[1], cols[1] - mx0, rows[2] - rows[1], "P", 13, INK, true, { align: "center", valign: "middle" });
  text(mx0, rows[2], cols[1] - mx0, my1 - rows[2], "N", 13, INK, true, { align: "center", valign: "middle" });
  // "Actual" rotated left of the grid (wide enough to stay on one line)
  const acx = mx0 - 17, acy = (rows[1] + my1) / 2;
  text(acx - 35, acy - 9, 70, 18, "Actual", 11, DRED, false,
    { align: "center", valign: "middle", rotate: 270 });
  // data cells (black numbers in the original)
  const cw1 = cols[2] - cols[1], cw2 = mx1 - cols[2];
  text(cols[1], rows[1], cw1, rows[2] - rows[1], cells[0], 14, INK, true, { align: "center", valign: "middle" });
  text(cols[2], rows[1], cw2, rows[2] - rows[1], cells[1], 14, INK, true, { align: "center", valign: "middle" });
  text(cols[1], rows[2], cw1, my1 - rows[2], cells[2], 14, INK, true, { align: "center", valign: "middle" });
  text(cols[2], rows[2], cw2, my1 - rows[2], cells[3], 14, INK, true, { align: "center", valign: "middle" });
  // TPR / FPR formulas right of the grid, dark red
  text(224 + dx, dy + 55, 116, 18, tpr, 13, DRED, false, { align: "left", valign: "middle" });
  text(224 + dx, dy + 88, 116, 18, fpr, 13, DRED, false, { align: "left", valign: "middle" });
}

// left column: thresholds 0.0, 0.1, 0.3, 0.4
panel(0, 43, "Threshold=0.0", ["5", "0", "6", "0"], "TPR=5/(5+0)=1", "FPR=6/(6+0)=1");
panel(0, 163, "Threshold=0.1", ["5", "0", "4", "2"], "TPR=5/(5+0)=1", "FPR=4/(4+2)=0.66");
panel(0, 287, "Threshold=0.3", ["5", "0", "2", "4"], "TPR=5/(5+0)=1", "FPR=2/(2+4)=0.33");
panel(0, 401, "Threshold=0.4", ["4", "1", "1", "5"], "TPR=4/(4+1)=4/5", "FPR=1/(1+5)=0.16");
// right column: thresholds 0.6, 0.7, 1
panel(345, 43, "Threshold=0.6", ["3", "1", "1", "5"], "TPR=3/(3+1)=0.6", "FPR=1/(1+5)=0.16");
panel(345, 163, "Threshold=0.7", ["3", "2", "0", "6"], "TPR=3/(3+2)=0.6", "FPR=0/(0+6)=0");
panel(345, 287, "Threshold=1", ["0", "5", "0", "6"], "TPR=0/(0+5)=0", "FPR=0/(0+6)=0");

// --- center-bottom title (original: two lines at x[340,570] y[420,480]) ---
s.addText([
  { text: "ROC Curve for", options: { fontSize: 15, bold: true, color: DRED, fontFace: FONT, breakLine: true } },
  { text: "Same Model -different thresholds", options: { fontSize: 15, bold: true, color: DRED, fontFace: FONT } }
], { x: P(330), y: P(420), w: P(290), h: P(60), align: "center", valign: "middle", margin: 0 });

// --- ROC plot: generated matplotlib PNG at measured box x[636,901] y[43,405] ---
s.addImage({
  path: ASSETS + "/roc_036.png",
  x: P(636), y: P(43), w: 2208 / 600, h: 3016 / 600,
});
// threshold label '1.0' for the origin point sits below the plot box in the original (frame glyphs x[655,672] y[431,439])
text(648, 428, 30, 14, "1.0", 10, INK, false, { align: "center", valign: "middle" });

// --- bottom strip: stacked-fraction definition boxes ---
// eq PNGs: 594x136 and 592x136 px at 600 dpi
rect(583, 398, 126, 36, "FFFFCC", DRED, 1);
s.addImage({ path: ASSETS + "/eq_036_tpr.png", x: P(586), y: P(404), w: 594 / 600, h: 136 / 600 });
rect(583, 458, 126, 36, "FFFFCC", DRED, 1);
s.addImage({ path: ASSETS + "/eq_036_fpr.png", x: P(586), y: P(464), w: 592 / 600, h: 136 / 600 });

// --- legend matrix bottom-right: x[710,850] y[395,495] ---
text(760, 390, 100, 10, "Predicted as", 10, DRED, false, { align: "center", valign: "middle" });
const lx0 = 710, lx1 = 850, ly0 = 408, ly1 = 495;
const lc = [lx0, lx0 + 42, lx0 + 92, lx1], lr = [ly0, ly0 + 26, ly0 + 55, ly1];
line(lx0, ly0, lx1, ly0, DRED, 1);
for (let i = 1; i < 3; i++) { line(lx0, lr[i], lx1, lr[i], DRED, 1); line(lc[i], ly0, lc[i], ly1, DRED, 1); }
line(lx0, ly1, lx1, ly1, DRED, 1);
// header P/N
rect(lc[1], lr[0], lc[2] - lc[1], lr[1] - lr[0], PINK, INK, 1);
rect(lc[2], lr[0], lx1 - lc[2], lr[1] - lr[0], PINK, INK, 1);
text(lc[1], lr[0], lc[2] - lc[1], lr[1] - lr[0], "P", 11, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[0], lx1 - lc[2], lr[1] - lr[0], "N", 11, INK, true, { align: "center", valign: "middle" });
// row labels P/N
rect(lc[0], lr[1], lc[1] - lc[0], lr[2] - lr[1], PINK, INK, 1);
rect(lc[0], lr[2], lc[1] - lc[0], ly1 - lr[2], PINK, INK, 1);
text(lc[0], lr[1], lc[1] - lc[0], lr[2] - lr[1], "P", 11, INK, true, { align: "center", valign: "middle" });
text(lc[0], lr[2], lc[1] - lc[0], ly1 - lr[2], "N", 11, INK, true, { align: "center", valign: "middle" });
// "Actual" rotated left of legend
const lacx = 692 + 11, lacy = (lr[1] + ly1) / 2;
text(lacx - 30, lacy - 8, 60, 16, "Actual", 10, DRED, false, { align: "center", valign: "middle", rotate: 270 });
// cells: TP green, TN green, FN red, FP red (per original highlights)
rect(lc[1], lr[1], lc[2] - lc[1], lr[2] - lr[1], GREEN, INK, 1);
rect(lc[2], lr[2], lx1 - lc[2], ly1 - lr[2], GREEN, INK, 1);
rect(lc[2], lr[1], lx1 - lc[2], lr[2] - lr[1], REDFILL, INK, 1);
rect(lc[1], lr[2], lc[2] - lc[1], ly1 - lr[2], REDFILL, INK, 1);
text(lc[1], lr[1], lc[2] - lc[1], lr[2] - lr[1], "TP", 11, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[1], lx1 - lc[2], lr[2] - lr[1], "FN", 11, INK, true, { align: "center", valign: "middle" });
text(lc[1], lr[2], lc[2] - lc[1], ly1 - lr[2], "FP", 11, INK, true, { align: "center", valign: "middle" });
text(lc[2], lr[2], lx1 - lc[2], ly1 - lr[2], "TN", 11, INK, true, { align: "center", valign: "middle" });

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_036_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
