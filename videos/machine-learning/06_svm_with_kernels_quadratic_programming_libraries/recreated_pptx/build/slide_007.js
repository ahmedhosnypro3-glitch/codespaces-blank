const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 7;
const TITLE = "Equal Constraints";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. Badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Three sections stacked vertically
const boxW = 12.3;
const boxX = 0.5;
let y = 1.0;

// Section 1: One Constraint
s.addShape(pres.shapes.RECTANGLE, { x: boxX, y, w: boxW, h: 1.8, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 } });
s.addText("One Constraint:  \u2211 a_i x_i = a1 x1 + a2 x2 + a3 x3 = Z", { x: boxX+0.2, y: y+0.1, w: boxW-0.4, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("[ a1  a2  a3 ] [ x1 ] = ( Z ) 1x1", { x: boxX+0.2, y: y+0.4, w: boxW-0.4, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ x2 ]", { x: boxX+0.2, y: y+0.65, w: boxW-0.4, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ x3 ]", { x: boxX+0.2, y: y+0.9, w: boxW-0.4, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("Ax = b", { x: boxX+0.2, y: y+1.3, w: boxW-0.4, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Section 2: Three Constraints
y += 2.0;
s.addShape(pres.shapes.RECTANGLE, { x: boxX, y, w: boxW, h: 2.2, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 } });
s.addText("Three Constraints:", { x: boxX+0.2, y: y+0.1, w: boxW-0.4, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("\u2211 a_i x_i = Z1", { x: boxX+0.2, y: y+0.4, w: boxW-0.4, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("\u2211 b_i x_i = Z2", { x: boxX+0.2, y: y+0.65, w: boxW-0.4, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("\u2211 c_i x_i = Z3", { x: boxX+0.2, y: y+0.9, w: boxW-0.4, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("[ a1  a2  a3 ] [ x1 ] = [ Z1 ]", { x: boxX+0.2, y: y+1.2, w: boxW-0.4, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ b1  b2  b3 ] [ x2 ]   [ Z2 ] 3x1", { x: boxX+0.2, y: y+1.45, w: boxW-0.4, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ c1  c2  c3 ] [ x3 ]   [ Z3 ]", { x: boxX+0.2, y: y+1.7, w: boxW-0.4, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("Ax = b", { x: boxX+0.2, y: y+1.85, w: boxW-0.4, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Section 3: Four Constraints
y += 2.4;
s.addShape(pres.shapes.RECTANGLE, { x: boxX, y, w: boxW, h: 2.5, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 } });
s.addText("Four Constraints:", { x: boxX+0.2, y: y+0.1, w: boxW-0.4, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("x1 + 2x2 = 7", { x: boxX+0.2, y: y+0.4, w: boxW-0.4, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("3x1 + 4x2 = 12", { x: boxX+0.2, y: y+0.65, w: boxW-0.4, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("3x3 - 5x1 = 10", { x: boxX+0.2, y: y+0.9, w: boxW-0.4, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("x1 + x2 + x3 = 24", { x: boxX+0.2, y: y+1.15, w: boxW-0.4, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("[ 1  2  0 ] [ x1 ] = [ 7  ]", { x: boxX+0.2, y: y+1.45, w: boxW-0.4, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 3  4  0 ] [ x2 ]   [ 12 ]", { x: boxX+0.2, y: y+1.7, w: boxW-0.4, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[-5  0  3 ] [ x3 ]   [ 10 ]", { x: boxX+0.2, y: y+1.95, w: boxW-0.4, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 1  1  1 ]         [ 24 ] 4x3  4x1", { x: boxX+0.2, y: y+2.2, w: boxW-0.4, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("Ax = b", { x: boxX+0.2, y: y+2.3, w: boxW-0.4, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_007_recreated.pptx" })
  .then(() => console.log("wrote slide_007_recreated.pptx"))
  .catch(e => console.error(e));