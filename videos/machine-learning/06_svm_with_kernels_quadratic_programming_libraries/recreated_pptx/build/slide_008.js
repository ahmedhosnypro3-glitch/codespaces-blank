const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 8;
const TITLE = "Example: QP Formulation";
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

// Objective function
let y = 0.9;
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 12.3, h: 1.2, fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1.5 } });
s.addText("Objective Function:", { x: 0.7, y: y+0.1, w: 11.8, h: 0.3, fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("Minimize 0.5 x^2 + 3x + 4y", { x: 0.7, y: y+0.4, w: 11.8, h: 0.3, fontSize: 16, color: "333333", fontFace: FONT, margin: 0 });
s.addText("Standard QP form: \u00bd [x^T P x] + q^T x", { x: 0.7, y: y+0.7, w: 11.8, h: 0.3, fontSize: 14, color: "3498DB", fontFace: FONT, margin: 0 });

// Subject to
y += 1.4;
s.addText("Subject to: Gx \u2264 h", { x: 0.7, y, w: 11.8, h: 0.3, fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Constraints
y += 0.4;
const constraints = [
  "x \u2265 0  =>  -x \u2264 0",
  "y \u2265 0  =>  -y \u2264 0",
  "x + 3y \u2265 15  =>  -x - 3y \u2264 -15",
  "2x + 5y \u2264 100",
  "3x + 4y \u2264 80",
];
constraints.forEach((c, i) => {
  s.addText(c, { x: 0.7, y: y + i*0.35, w: 11.8, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
});

// G matrix and h vector
y += constraints.length * 0.35 + 0.2;
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 6.0, h: 2.0, fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1.5 } });
s.addText("G =", { x: 0.7, y: y+0.1, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: "3498DB", fontFace: FONT, margin: 0 });
s.addText("[-1  0 ]", { x: 0.7, y: y+0.4, w: 5.6, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0 -1 ]", { x: 0.7, y: y+0.65, w: 5.6, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[-1 -3 ]", { x: 0.7, y: y+0.9, w: 5.6, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 2  5 ]", { x: 0.7, y: y+1.15, w: 5.6, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 3  4 ]", { x: 0.7, y: y+1.4, w: 5.6, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });

s.addShape(pres.shapes.RECTANGLE, { x: 7.0, y, w: 5.8, h: 2.0, fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1.5 } });
s.addText("h =", { x: 7.2, y: y+0.1, w: 5.4, h: 0.3, fontSize: 14, bold: true, color: "3498DB", fontFace: FONT, margin: 0 });
s.addText("[  0 ]", { x: 7.2, y: y+0.4, w: 5.4, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[  0 ]", { x: 7.2, y: y+0.65, w: 5.4, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[-15 ]", { x: 7.2, y: y+0.9, w: 5.4, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[100 ]", { x: 7.2, y: y+1.15, w: 5.4, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 80 ]", { x: 7.2, y: y+1.4, w: 5.4, h: 0.25, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_008_recreated.pptx" })
  .then(() => console.log("wrote slide_008_recreated.pptx"))
  .catch(e => console.error(e));