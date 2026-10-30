const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 9;
const TITLE = "Example: Complete QP Solution";
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

// Left side: formulation
let y = 0.9;
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 6.0, h: 6.0, fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1.5 } });
s.addText("Original Function:", { x: 0.7, y: y+0.1, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("Minimize 0.5 x^2 + 3x + 4y", { x: 0.7, y: y+0.4, w: 5.6, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });

s.addText("Matrix Form: Minimize \u00bd [x^T P x] + q^T x", { x: 0.7, y: y+0.8, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "3498DB", fontFace: FONT, margin: 0 });
s.addText("P = [ 1  0 ]", { x: 0.7, y: y+1.2, w: 5.6, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("      [ 0  0 ]", { x: 0.7, y: y+1.5, w: 5.6, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("q = [ 3 ]", { x: 0.7, y: y+1.9, w: 5.6, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("      [ 4 ]", { x: 0.7, y: y+2.2, w: 5.6, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });

s.addText("Constraints Gx \u2264 h:", { x: 0.7, y: y+2.6, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
const constraints = [
  "x \u2265 0   =>  -x \u2264 0",
  "y \u2265 0   =>  -y \u2264 0",
  "x + 3y \u2265 15  =>  -x - 3y \u2264 -15",
  "2x + 5y \u2264 100",
  "3x + 4y \u2264 80",
];
constraints.forEach((c, i) => {
  s.addText(c, { x: 0.7, y: y+2.9+i*0.3, w: 5.6, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
});

s.addText("G =", { x: 0.7, y: y+4.4, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "3498DB", fontFace: FONT, margin: 0 });
s.addText("[-1  0 ]", { x: 0.7, y: y+4.7, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0 -1 ]", { x: 0.7, y: y+4.95, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[-1 -3 ]", { x: 0.7, y: y+5.2, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 2  5 ]", { x: 0.7, y: y+5.45, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 3  4 ]", { x: 0.7, y: y+5.7, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });

// Right side: solution
y = 0.9;
s.addShape(pres.shapes.RECTANGLE, { x: 6.8, y, w: 6.0, h: 6.0, fill: { color: "FFF9C4" }, line: { color: "E74C3C", width: 1.5 } });
s.addText("SOLUTION", { x: 7.0, y: y+0.1, w: 5.6, h: 0.4, align: "center", fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("Optimal Point: x = 0, y = 5", { x: 7.0, y: y+0.6, w: 5.6, h: 0.3, align: "center", fontSize: 16, color: "333333", fontFace: FONT, margin: 0 });
s.addText("Constraint Check:", { x: 7.0, y: y+1.0, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("x + 3y = 15 \u2265 15 \u2713", { x: 7.0, y: y+1.4, w: 5.6, h: 0.3, fontSize: 14, color: "008000", fontFace: FONT, margin: 0 });
s.addText("2x + 5y = 25 \u2264 100 \u2713", { x: 7.0, y: y+1.75, w: 5.6, h: 0.3, fontSize: 14, color: "008000", fontFace: FONT, margin: 0 });
s.addText("3x + 4y = 20 \u2264 80 \u2713", { x: 7.0, y: y+2.1, w: 5.6, h: 0.3, fontSize: 14, color: "008000", fontFace: FONT, margin: 0 });
s.addText("Minimum Value:", { x: 7.0, y: y+2.6, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("0.5 x^2 + 3x + 4y = 20", { x: 7.0, y: y+3.0, w: 5.6, h: 0.3, align: "center", fontSize: 16, bold: true, color: "E74C3C", fontFace: FONT, margin: 0 });
s.addText("h =", { x: 7.0, y: y+3.6, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "3498DB", fontFace: FONT, margin: 0 });
s.addText("[  0 ]", { x: 7.0, y: y+3.9, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[  0 ]", { x: 7.0, y: y+4.15, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[-15 ]", { x: 7.0, y: y+4.4, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[100 ]", { x: 7.0, y: y+4.65, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 80 ]", { x: 7.0, y: y+4.9, w: 5.6, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_009_recreated.pptx" })
  .then(() => console.log("wrote slide_009_recreated.pptx"))
  .catch(e => console.error(e));