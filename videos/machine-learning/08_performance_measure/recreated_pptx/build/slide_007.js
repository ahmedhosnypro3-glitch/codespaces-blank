// slide_007 — "Precision" (08_performance_measure). 1px of the 960x540 original = 1pt.
// Geometry measured from unique_slides/slide_007.jpg with PIL; text from the fresh
// image-analysis read (pool_run/image_analysis/slide_007_analysis.txt), cross-checked
// against analysis/reanalysis/slide_007_raw.json + sources/slide_007_research.md.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const DRED = "8F0000";
const GREEN = "00B050";
const GRN_FILL = "8CFF00";   // CM1 TP/TN cell fills (measured ~#87FF00)
const BLUE = "0070C0";
const ARROW_BLUE = "0000FF";
const BADGE = "FFF9C4";
const INK = "333333";
const BLACK = "000000";
const GRAY_BOX = "CBCDCA";   // definition band (measured ~#CBCDCA)
const PALE_Y = "F7FCD4";     // meaning band (measured ~#F7FCD4)
const PALE_C = "F0FFFD";     // worked-example box (measured ~#F0FFFD)
const CALLOUT = "FCFFE2";    // callout boxes (measured ~#FCFFE2)
const QBOX = "DDFFFF";       // question box (measured ~#DDFFFF)
const FONT = "Arial";

const px = (v) => v / 72;
const s = pptx.addSlide();
s.background = { color: BG };

// ---------- house chrome (root AGENTS.md 2026-10-09, overrides everything) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("7", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText("Precision", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62, align: "center", valign: "middle",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- helpers ----------
function rect(x0, y0, x1, y1, fill, lineColor, lineW) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: fill ? { color: fill } : { type: "none" },
    line: lineColor ? { color: lineColor, width: lineW || 1.25 } : { type: "none" },
  });
}
function hline(x0, x1, y, color, w) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y), w: px(x1 - x0), h: px(w || 2),
    fill: { color: color }, line: { color: color, width: 0.25 },
  });
}
function vline(x, y0, y1, color, w) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x), y: px(y0), w: px(w || 2), h: px(y1 - y0),
    fill: { color: color }, line: { color: color, width: 0.25 },
  });
}
function text(str, x0, y0, x1, y1, size, color, opts) {
  const o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "center", valign: "middle", fontSize: size, bold: true,
    color: color, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(str, o);
}
function rtext(parts, x0, y0, x1, y1, size, opts) {
  const o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "left", valign: "middle", fontSize: size, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(parts.map(([t, c, b, i]) => ({
    text: t, options: { color: c, bold: b !== false, italic: !!i, fontFace: FONT },
  })), o);
}

// ---------- gray definition band ----------
rect(72, 113, 823, 173, GRAY_BOX, null);
text("Correctly Classified (as Positive)", 70, 118, 640, 140, 16, BLACK);
hline(80, 641, 141, RED, 3);
text("Total Classified as Positive (either Correct and Erroneous)", 70, 150, 640, 171, 16, BLACK);

// ---------- Meaning band (pale yellow) ----------
rect(73, 199, 624, 253, PALE_Y, null);
text("Meaning", 78, 205, 178, 227, 16, RED, { align: "left" });
rtext([
  ["% of what you ", BLACK],
  ["Predicted", RED],
  [" as ", BLACK],
  ["POSITIVE", RED],
  [" is Actually Positive", BLACK],
], 79, 232, 620, 254, 16, { align: "left" });

// ---------- formula box (white, red border) ----------
rect(70, 262, 332, 336, "FFFFFF", RED, 2);
text("Precision =", 84, 283, 200, 308, 18, BLACK, { align: "left" });
// stacked fraction: numerator / bar / denominator (professional 2D)
text("TP", 246, 271, 288, 296, 18, BLACK);
hline(218, 322, 300, BLACK, 2.5);
text("TP + FP", 218, 303, 322, 327, 18, BLACK);

// ---------- worked example box (pale cyan) ----------
rect(336, 288, 508, 340, PALE_C, "9DC3E6", 1);
text("Precision= 18/(18+10)", 342, 293, 502, 313, 12, BLACK, { align: "left" });
text("=64.3%", 392, 316, 462, 336, 12, BLACK, { align: "left" });

// ---------- callout boxes ----------
rect(114, 358, 234, 388, CALLOUT, "BFBFBF", 0.75);
text("Positive Classified as +ive", 116, 360, 232, 386, 9, BLACK, { lineSpacing: 11 });
rect(242, 358, 362, 388, CALLOUT, "BFBFBF", 0.75);
text("Negative Classified as +ive", 244, 360, 360, 386, 9, BLACK, { lineSpacing: 11 });
// hand-drawn green underline under the callouts
hline(108, 333, 394, GREEN, 4);
// red italic annotation
rtext([
  ["All Samples ", RED],
  ["classified as Positive", BLACK],
], 74, 410, 310, 428, 12, { align: "left", italic: true });

// ---------- bottom question box (pale cyan, blue border) ----------
rect(80, 468, 495, 505, QBOX, "2E75B6", 1.25);
s.addText([
  { text: "If you said: the sample is positive, can I trust you ? ", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT, breakLine: true } },
  { text: "At what %?", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT, breakLine: false } },
], {
  x: px(88), y: px(472), w: px(399), h: px(29), align: "left", valign: "middle",
  margin: 0, lineSpacing: 20,
});

// ---------- confusion matrix helper ----------
function matrix(x0, y0, x1, y1, stubX1, cellX0, cellX1, hy0, hy1, ry0, ry1, cells) {
  rect(x0, y0, x1, y1, "FFFFFF", BLUE, 1.5);
  text("Predicted as", cellX0, y0 + 9, cellX1, hy0, 10, RED);
  text("P", cellX0, hy0, (cellX0 + cellX1) / 2, hy1, 10, BLACK);
  text("N", (cellX0 + cellX1) / 2, hy0, cellX1, hy1, 10, BLACK);
  const mid = (ry1 + ry0 + ry1) / 2; // unused
  cells.forEach(([cx0, cy0, cx1, cy1, fill]) => { if (fill) rect(cx0, cy0, cx1, cy1, fill, null); });
  hline(hy0, x0, x1, RED, 1.5);
  hline(hy1, x0, x1, RED, 1.5);
  hline(ry1, x0, x1, RED, 1.5);
  vline(stubX1, hy0, y1, RED, 1.5);
  vline(cellX0, hy0, y1, RED, 1.5);
  vline((cellX0 + cellX1) / 2, hy0, y1, RED, 1.5);
  vline(x1 - 2, hy0, y1, RED, 1.5);
  cells.forEach(([cx0, cy0, cx1, cy1, , label]) => { if (label) text(label, cx0, cy0, cx1, cy1, 12, BLACK); });
}
function actualLabel(cx, cy) {
  s.addText("Actual", {
    x: px(cx - 26), y: px(cy - 7), w: px(52), h: px(14), rotate: 270,
    align: "center", valign: "middle", fontSize: 10, bold: true, color: RED,
    fontFace: FONT, margin: 0,
  });
}

// matrix 1 (symbolic): panel x673-866 y43-168; stub 673-698; cells 738-791 / 791-866; rows 98-125 / 125-158
matrix(673, 43, 866, 168, 698, 738, 866, 73, 98, 98, 158, [
  [738, 98, 791, 125, GRN_FILL, "TP"],
  [791, 98, 866, 125, null, "FN"],
  [738, 125, 791, 158, null, "FP"],
  [791, 125, 866, 158, GRN_FILL, "TN"],
]);
text("P", 676, 104, 698, 122, 10, BLACK);
text("N", 676, 132, 698, 150, 10, BLACK);
actualLabel(685, 112);

// matrix 2 (numeric): panel x673-866 y168-291; stub 673-704; cells 746-800 / 800-856; rows 220-252 / 252-283
matrix(673, 168, 866, 291, 704, 746, 856, 191, 220, 220, 283, [
  [746, 220, 800, 252, null, "18"],
  [800, 220, 856, 252, null, "12"],
  [746, 252, 800, 283, null, "10"],
  [800, 252, 856, 283, null, "60"],
]);
text("P", 676, 234, 704, 250, 10, BLACK);
text("N", 676, 262, 704, 278, 10, BLACK);
actualLabel(688, 244);
// hand-drawn blue circles around 18 and 10 (the predicted-positive column)
s.addShape(pptx.shapes.OVAL, {
  x: px(742), y: px(216), w: px(62), h: px(40),
  fill: { type: "none" }, line: { color: BLUE, width: 2 },
});
s.addShape(pptx.shapes.OVAL, {
  x: px(742), y: px(248), w: px(62), h: px(40),
  fill: { type: "none" }, line: { color: BLUE, width: 2 },
});
// hand-drawn green rectangle around 60
s.addShape(pptx.shapes.RECTANGLE, {
  x: px(796), y: px(248), w: px(64), h: px(40),
  fill: { type: "none" }, line: { color: GREEN, width: 2 },
});

// ---------- Positive/Negative tree panel (red border) ----------
rect(536, 290, 880, 503, "FFFFFF", RED, 1.5);
text("Positive", 590, 296, 670, 316, 18, RED, { align: "left" });
text("Negative", 770, 296, 860, 316, 18, GREEN, { align: "left" });

// airplane line icons above the root nodes
function plane(cx, cy, bodyColor) {
  const w = 56, h = 30;
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - w / 2), y: px(cy - 4), w: px(w), h: px(9),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - 10), y: px(cy + 3), w: px(20), h: px(15),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - w / 2 + 2), y: px(cy - 11), w: px(12), h: px(10),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
}
plane(618, 352, "808080");
plane(799, 352, "A0A0A0");

// blue branch arrows with heads
function arrow(x0, y0, x1, y1) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: ARROW_BLUE, width: 1.5, endArrowType: "triangle" },
  });
}
arrow(612, 408, 579, 441);
arrow(624, 408, 657, 440);
arrow(793, 409, 761, 441);
arrow(805, 409, 841, 441);

// tree nodes
function node(cx, cy, d, fill, label) {
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill },
  });
  text(label, cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2, 12, "FFFFFF");
}
node(618, 393, 30, RED, "30");
node(799, 393, 33, GREEN, "70");
node(573, 456, 29, RED, "18");
node(661, 456, 32, GREEN, "12");
node(755, 457, 32, GREEN, "60");
node(845, 456, 29, RED, "10");
// leaf labels
text("TP", 578, 482, 604, 498, 10, RED);
text("FN", 658, 482, 684, 498, 10, RED);
text("TN", 748, 482, 774, 498, 10, RED);
text("FP", 838, 482, 864, 498, 10, RED);

// ---------- black footer bar (bottom edge, below house frame line) ----------
rect(38, 530, 921, 540, BLACK, null);

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_007_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
