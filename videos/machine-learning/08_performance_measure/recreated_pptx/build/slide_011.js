// slide_011.js — attempt 11: geometry rebuilt from PIL measurements of slide_011.jpg (1px=1pt)
// Fixes vs attempt 10: fraction INSIDE the red "Recall =" box, calc inline right of box,
// matrices as slide_009-certified text+shape pattern, tree panel contained, ovals on 28 (blue) and 2 (red).
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const BLUE = "2E5C8A", LBLUE = "0070C0", GREEN = "00B050", LGREEN = "90EE90";
const FONT = "Arial";
const A = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides everything)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 } });
s.addText("11", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0 });
s.addText("Recall", { x: 0.6, y: 0.28, w: 12.13, h: 0.7, align: "center", valign: "middle", fontSize: 44, bold: true, color: RED, fontFace: FONT, margin: 0 });

// ===== LEFT COLUMN =====
// 1. Gray definition strip (px 61,95..660,200) with red divider (px 80,147..646,151)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.85, y: 1.32, w: 8.45, h: 1.46, fill: { color: "D9D9D9" }, line: { type: "none" } });
s.addText("Correctly Classified (as Positive)", { x: 0.85, y: 1.70, w: 8.45, h: 0.34, align: "center", valign: "middle", fontSize: 17, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
s.addShape(pptx.shapes.LINE, { x: 1.11, y: 2.06, w: 7.86, h: 0, line: { color: RED, width: 2.25 } });
s.addText("Total objects that should be retrieved (Actually Positive)", { x: 0.85, y: 2.14, w: 8.45, h: 0.34, align: "center", valign: "middle", fontSize: 17, bold: true, color: TEXT, fontFace: FONT, margin: 0 });

// 2. Meaning box (pale yellow, px 67,201..615,264)
s.addShape(pptx.shapes.RECTANGLE, { x: 0.93, y: 2.79, w: 7.61, h: 0.85, fill: { color: "FFFFCC" }, line: { color: "CCC000", width: 0.75 } });
s.addText("Meaning", { x: 1.12, y: 2.84, w: 2.0, h: 0.34, fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0, valign: "middle" });
s.addText([
  { text: "Does the classifier " },
  { text: "miss", options: { color: "FF0000", italic: true, underline: true } },
  { text: " any of " },
  { text: "Positive", options: { color: "0000CC", bold: true } },
  { text: " Objects ?" },
], { x: 1.12, y: 3.20, w: 8.15, h: 0.34, fontSize: 19, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });

// 3. Formula box: ONE red rounded rect enclosing "Recall =" + the 2D fraction (px 70,262..317,322)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.97, y: 3.64, w: 3.44, h: 0.83, fill: { color: "FFFFFF" }, line: { color: RED, width: 2 } });
s.addText("Recall =", { x: 1.10, y: 3.80, w: 1.90, h: 0.50, fontSize: 20, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
s.addImage({ path: A + "/eq_011_v3_tpfn.png", x: 3.02, y: 3.71, w: 1.3017, h: 0.6133 });

// 4. Worked example inline right of the formula box: "Recall=" + 28/(28+2) fraction + "=93.3%" (px 344..667, 292..354)
s.addText("Recall=", { x: 4.62, y: 4.10, w: 0.80, h: 0.32, fontSize: 15, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
s.addImage({ path: A + "/eq_011_v3_frac28.png", x: 5.46, y: 4.02, w: 0.715, h: 0.42 });
s.addText("=93.3%", { x: 6.26, y: 4.10, w: 1.05, h: 0.32, fontSize: 15, bold: true, color: "FF0000", fontFace: FONT, margin: 0, valign: "middle" });

// 5. Two beige callouts with upward pointers (px L 112,330..227,374  R 225,333..319,374)
function callout(x, y, w, h, line2) {
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x + w / 2 - 0.07, y: y - 0.11, w: 0.14, h: 0.11, fill: { color: "F2E6D9" }, line: { color: "C8A878", width: 1 }, rotate: 180 });
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: x, y: y, w: w, h: h, fill: { color: "F2E6D9" }, line: { color: "C8A878", width: 1 } });
  s.addText("Positive", { x: x, y: y + 0.05, w: w, h: 0.24, align: "center", valign: "middle", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addText(line2, { x: x, y: y + 0.30, w: w, h: 0.24, align: "center", valign: "middle", fontSize: 10, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
}
callout(1.56, 4.58, 1.59, 0.61, "Classified as +ive");
callout(3.12, 4.62, 1.31, 0.57, "Classified as -ive");

// 6. Green underbrace (px 107,385..334,402) as line + end ticks + center tick
s.addShape(pptx.shapes.LINE, { x: 1.49, y: 5.50, w: 3.15, h: 0, line: { color: GREEN, width: 2.5 } });
s.addShape(pptx.shapes.LINE, { x: 1.49, y: 5.38, w: 0, h: 0.12, line: { color: GREEN, width: 2.5 } });
s.addShape(pptx.shapes.LINE, { x: 4.64, y: 5.38, w: 0, h: 0.12, line: { color: GREEN, width: 2.5 } });
s.addShape(pptx.shapes.LINE, { x: 3.065, y: 5.50, w: 0, h: 0.10, line: { color: GREEN, width: 2.5 } });

// 7. Red italic caption (px 96,408..329,419)
s.addText("All Positive Samples in the Dataset", { x: 1.30, y: 5.66, w: 3.34, h: 0.26, align: "center", valign: "middle", fontSize: 12, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0 });

// 8. Blue takeaway box (px 70,437..499,504)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: 0.97, y: 6.07, w: 5.96, h: 0.93, fill: { color: "ADD8E6" }, line: { color: LBLUE, width: 1 } });
s.addText([
  { text: "Higher Recall means ", options: { color: "0000EE" } },
  { text: "I HIGHLY trust you if you said I picked ALL Positive Objects.", options: { bold: true, color: TEXT } },
], { x: 1.12, y: 6.15, w: 5.66, h: 0.30, fontSize: 12, fontFace: FONT, margin: 0, valign: "middle" });
s.addText([
  { text: "It Does ", options: { color: "0000EE" } },
  { text: "NOT", options: { bold: true, color: "0000EE" } },
  { text: " mean ", options: { color: "0000EE" } },
  { text: "All you said Positive are Actually Positive", options: { bold: true, color: TEXT } },
], { x: 1.12, y: 6.51, w: 5.66, h: 0.30, fontSize: 12, fontFace: FONT, margin: 0, valign: "middle" });

// ===== RIGHT: confusion matrices (slide_009-certified text+shape pattern) =====
function matrix(x, y, w, h) {
  const lw = 1.0;
  const lx = x, gx = x + lw, gw = w - lw;
  const hh = 0.30, chh = 0.28;
  const rh = (h - hh - chh) / 2;
  s.addShape(pptx.shapes.RECTANGLE, { x: x, y: y, w: w, h: h, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 } });
  s.addText("Predicted as", { x: gx, y: y + 0.02, w: gw, h: hh, align: "center", valign: "middle", fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0 });
  s.addText("P", { x: gx, y: y + hh, w: gw / 2, h: chh, align: "center", valign: "middle", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addText("N", { x: gx + gw / 2, y: y + hh, w: gw / 2, h: chh, align: "center", valign: "middle", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addText("Actual", { x: x + 0.02, y: y + hh + 0.05, w: 0.22, h: rh * 2, align: "center", valign: "middle", fontSize: 9, bold: true, color: RED, fontFace: FONT, margin: 0, rotate: 270 });
  s.addText("P", { x: x, y: y + hh + chh, w: lw, h: rh, align: "center", valign: "middle", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addText("N", { x: x, y: y + hh + chh + rh, w: lw, h: rh, align: "center", valign: "middle", fontSize: 11, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
  s.addShape(pptx.shapes.LINE, { x: gx, y: y + hh, w: gw, h: 0, line: { color: RED, width: 0.75 } });
  s.addShape(pptx.shapes.LINE, { x: gx, y: y + hh + chh, w: gw, h: 0, line: { color: RED, width: 0.75 } });
  s.addShape(pptx.shapes.LINE, { x: gx, y: y + hh + chh + rh, w: gw, h: 0, line: { color: RED, width: 0.75 } });
  s.addShape(pptx.shapes.LINE, { x: gx + gw / 2, y: y + hh, w: 0, h: h - hh, line: { color: RED, width: 0.75 } });
  return { gx: gx, gw: gw, gy: y + hh + chh, rh: rh, cw: gw / 2 };
}
function cell(g, cx, cy, fill, label, txtColor) {
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: g.cw, h: g.rh, fill: { color: fill }, line: { color: RED, width: 0.75 } });
  s.addText(label, { x: cx, y: cy, w: g.cw, h: g.rh, align: "center", valign: "middle", fontSize: 14, bold: true, color: txtColor, fontFace: FONT, margin: 0 });
}
// Matrix 1 — symbolic (px 672,52..869,159)
const m1 = matrix(9.33, 0.72, 2.74, 1.49);
cell(m1, m1.gx, m1.gy, LGREEN, "TP", TEXT);
cell(m1, m1.gx + m1.cw, m1.gy, "FFFFFF", "FN", TEXT);
cell(m1, m1.gx, m1.gy + m1.rh, "FFFFFF", "FP", TEXT);
cell(m1, m1.gx + m1.cw, m1.gy + m1.rh, LGREEN, "TN", TEXT);

// Matrix 2 — numeric (px 672,167..867,288); 28 has blue oval, 2 has red oval
const m2 = matrix(9.33, 2.32, 2.71, 1.68);
cell(m2, m2.gx, m2.gy, "FFFFFF", "28", TEXT);
cell(m2, m2.gx + m2.cw, m2.gy, "FFFFFF", "2", TEXT);
cell(m2, m2.gx, m2.gy + m2.rh, "FFFFFF", "30", TEXT);
cell(m2, m2.gx + m2.cw, m2.gy + m2.rh, LGREEN, "40", TEXT);
s.addShape(pptx.shapes.OVAL, { x: m2.gx + m2.cw / 2 - 0.21, y: m2.gy + m2.rh / 2 - 0.21, w: 0.42, h: 0.42, fill: { type: "none" }, line: { color: LBLUE, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: m2.gx + m2.cw + m2.cw / 2 - 0.21, y: m2.gy + m2.rh / 2 - 0.21, w: 0.42, h: 0.42, fill: { type: "none" }, line: { color: RED, width: 1.5 } });

// ===== TREE PANEL (red frame, px 535,290..882,503) =====
s.addShape(pptx.shapes.RECTANGLE, { x: 7.43, y: 4.03, w: 4.82, h: 2.96, fill: { color: "FFFFFF" }, line: { color: RED, width: 2 } });
s.addImage({ path: A + "/plane_011_v3_pos.png", x: 8.17, y: 4.76, w: 1.1806, h: 0.4167 });
s.addImage({ path: A + "/plane_011_v3_neg.png", x: 10.61, y: 4.76, w: 1.2222, h: 0.3333 });
s.addText("Positive", { x: 8.09, y: 5.20, w: 1.0, h: 0.24, align: "center", valign: "middle", fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0 });
s.addText("Negative", { x: 10.61, y: 5.20, w: 1.0, h: 0.24, align: "center", valign: "middle", fontSize: 15, bold: true, color: GREEN, fontFace: FONT, margin: 0 });

function node(cx, cy, num, fill) {
  s.addShape(pptx.shapes.OVAL, { x: cx - 0.21, y: cy - 0.21, w: 0.42, h: 0.42, fill: { color: fill }, line: { color: fill, width: 1 } });
  s.addText(num, { x: cx - 0.21, y: cy - 0.21, w: 0.42, h: 0.42, align: "center", valign: "middle", fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });
}
function branch(x0, y0, x1, y1) {
  s.addShape(pptx.shapes.LINE, { x: Math.min(x0, x1), y: Math.min(y0, y1), w: Math.abs(x1 - x0), h: Math.abs(y1 - y0), line: { color: LBLUE, width: 1.5 } });
  const ang = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI;
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x1 - 0.07, y: y1 - 0.07, w: 0.14, h: 0.14, fill: { color: LBLUE }, line: { type: "none" }, rotate: ang + 90 });
}
function leaf(cx, label, color) {
  s.addText(label, { x: cx - 0.25, y: 6.62, w: 0.5, h: 0.26, align: "center", valign: "middle", fontSize: 11, bold: true, color: color, fontFace: FONT, margin: 0 });
}
// left (Positive) tree: 30 -> 28 (TP), 2 (FN)
node(8.61, 5.56, "30", RED);
node(7.98, 6.34, "28", RED);
node(9.18, 6.35, "2", GREEN);
branch(8.61, 5.77, 7.98, 6.13);
branch(8.61, 5.77, 9.18, 6.14);
leaf(7.98, "TP", RED);
leaf(9.18, "FN", GREEN);
// right (Negative) tree: 70 -> 40 (TN), 30 (FP)
node(11.11, 5.56, "70", GREEN);
node(10.47, 6.34, "40", GREEN);
node(11.75, 6.34, "30", RED);
branch(11.11, 5.77, 10.47, 6.13);
branch(11.11, 5.77, 11.75, 6.13);
leaf(10.47, "TN", GREEN);
leaf(11.75, "FP", RED);

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_011_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done", outPath));
