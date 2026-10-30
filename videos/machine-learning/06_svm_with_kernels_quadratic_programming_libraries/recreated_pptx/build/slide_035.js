// slide_035.js — "How to Kernelize SVM" (v2: three bands, color-coded serif math, green ovals)
// Upper band: original SVM formulation. Middle band: Remember. Lower band: kernelized formulation.
// Run: NODE_PATH=$(npm root -g) node slide_035.js

const pptxgen = require("pptxgenjs");

const NUM = 35;
const TITLE = "How to Kernelize SVM";
const FONT = "Arial";
const MATH = "Times New Roman";
const W = 13.33, H = 7.5;
const EQ34 = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_034/";
const EQ35 = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_035/";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// 1. House red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position y=0.28)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Large blue-bordered container
const contX = 0.45, contY = 0.92, contW = 12.43, contH = 6.15;
s.addShape(pres.shapes.RECTANGLE, {
  x: contX, y: contY, w: contW, h: contH,
  fill: { type: "none" }, line: { color: "2980B9", width: 1.5 },
});

const bandW = contW - 0.4;
const bandX = contX + 0.2;
const upperY = contY + 0.08;
const midY = upperY + 1.9;
const lowY = midY + 1.95;

// --- UPPER BAND ---
// 5a. Lagrangian (no highlight)
s.addImage({ path: EQ34 + "eq1_lagrangian_multi.png", x: bandX + 0.6, y: upperY + 0.05, w: 5.40667, h: 0.995 });

// 5b. W and b boxes, sized to hug content
const uFormulaY = upperY + 1.12;
const wImgW = 2.01167, wImgH = 0.95;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX, y: uFormulaY, w: wImgW + 0.3, h: wImgH + 0.12,
  fill: { color: "FFFFFF" }, line: { color: "2980B9", width: 1 },
});
s.addImage({ path: EQ34 + "eq2_W_multi.png", x: bandX + 0.15, y: uFormulaY + 0.06, w: wImgW, h: wImgH });
const bImgW = 6.26, bImgH = 0.44667;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX + wImgW + 0.5, y: uFormulaY + 0.2, w: bImgW + 0.3, h: bImgH + 0.12,
  fill: { color: "FFFFFF" }, line: { color: "2980B9", width: 1 },
});
s.addImage({ path: EQ34 + "eq3_b_multi.png", x: bandX + wImgW + 0.65, y: uFormulaY + 0.23, w: bImgW, h: bImgH });

// 5c. Classification strip
const uClassY = uFormulaY + 1.08;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX, y: uClassY, w: 6.9, h: 0.4,
  fill: { color: "FDEBD0" }, line: { type: "none" },
});
s.addText([
  { text: "Class of vector ", options: { color: "2C3E50", fontFace: FONT } },
  { text: "Z", options: { color: "2C3E50", bold: true, fontFace: MATH } },
  { text: " \u21d2 sign(", options: { color: "2C3E50", fontFace: MATH } },
  { text: "W", options: { color: "2C3E50", fontFace: MATH } },
  { text: "T", options: { color: "2C3E50", fontFace: MATH, superscript: true } },
  { text: " Z + b)", options: { color: "2C3E50", fontFace: MATH } },
], {
  x: bandX, y: uClassY, w: 6.9, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 15, color: "2C3E50", fontFace: MATH, margin: 0,
});

// 6. Band separator
s.addShape(pres.shapes.LINE, {
  x: contX, y: midY - 0.12, w: contW, h: 0,
  line: { color: "2980B9", width: 1.5 },
});

// --- MIDDLE BAND: Remember ---
// 7a. Header
s.addText("Remember :", {
  x: bandX, y: midY, w: bandW, h: 0.3,
  align: "left", fontSize: 15, bold: true, italic: true, color: "2980B9", fontFace: FONT, margin: 0,
});

// 7b. Mapping row (inline typeset math)
const mapY = midY + 0.35;
s.addText([
  { text: "Mapping", options: { fontSize: 13, bold: true, italic: true, color: "C0392B", fontFace: FONT, margin: 0 } },
  { text: "  Instead of using ", options: { fontSize: 12, color: "2C3E50", fontFace: FONT, margin: 0 } },
  { text: "X", options: { fontSize: 12, bold: true, color: "2980B9", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, bold: true, color: "2980B9", fontFace: MATH, subscript: true, margin: 0 } },
  { text: " (of dimension ", options: { fontSize: 12, color: "2C3E50", fontFace: FONT, margin: 0 } },
  { text: "d", options: { fontSize: 12, italic: true, bold: true, color: "C0392B", fontFace: MATH, margin: 0 } },
  { text: ") use ", options: { fontSize: 12, color: "2C3E50", fontFace: FONT, margin: 0 } },
  { text: "\u03c6(X", options: { fontSize: 12, bold: true, color: "2980B9", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, bold: true, color: "2980B9", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ") (with higher dimension )", options: { fontSize: 12, italic: true, color: "C0392B", fontFace: FONT, margin: 0 } },
], { x: bandX, y: mapY, w: bandW, h: 0.28, align: "left", valign: "middle", margin: 0 });

// 7c. Mapping math line
s.addImage({ path: EQ34 + "eq4_mapping.png", x: bandX + 0.3, y: mapY + 0.3, w: 2.845, h: 0.45667 });

// 7d. Kernelization row
const kernY = mapY + 0.85;
s.addText([
  { text: "Kernelization", options: { fontSize: 13, bold: true, italic: true, color: "C0392B", fontFace: FONT, margin: 0 } },
  { text: "  Instead of using ", options: { fontSize: 12, color: "2C3E50", fontFace: FONT, margin: 0 } },
  { text: "\u03c6(X", options: { fontSize: 12, color: "2980B9", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, color: "2980B9", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ")", options: { fontSize: 12, color: "2980B9", fontFace: MATH, margin: 0 } },
  { text: "T", options: { fontSize: 12, color: "2980B9", fontFace: MATH, superscript: true, margin: 0 } },
  { text: " \u03c6(X", options: { fontSize: 12, color: "2980B9", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, color: "2980B9", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ")", options: { fontSize: 12, color: "2980B9", fontFace: MATH, margin: 0 } },
  { text: "T", options: { fontSize: 12, color: "2980B9", fontFace: MATH, superscript: true, margin: 0 } },
  { text: " use ", options: { fontSize: 12, color: "2C3E50", fontFace: FONT, margin: 0 } },
  { text: "K", options: { fontSize: 12, color: "C0392B", fontFace: MATH, margin: 0 } },
  { text: " (X", options: { fontSize: 12, color: "C0392B", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, color: "C0392B", fontFace: MATH, subscript: true, margin: 0 } },
  { text: "T", options: { fontSize: 12, color: "C0392B", fontFace: MATH, superscript: true, margin: 0 } },
  { text: " , X", options: { fontSize: 12, color: "C0392B", fontFace: MATH, margin: 0 } },
  { text: "j", options: { fontSize: 12, color: "C0392B", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ") (Where ", options: { fontSize: 12, italic: true, color: "C0392B", fontFace: FONT, margin: 0 } },
  { text: "K", options: { fontSize: 12, italic: true, color: "C0392B", fontFace: MATH, margin: 0 } },
  { text: " is one of kernel functions)", options: { fontSize: 12, italic: true, color: "C0392B", fontFace: FONT, margin: 0 } },
], { x: bandX, y: kernY, w: bandW, h: 0.28, align: "left", valign: "middle", margin: 0 });

// 8. Band separator
s.addShape(pres.shapes.LINE, {
  x: contX, y: lowY - 0.12, w: contW, h: 0,
  line: { color: "2980B9", width: 1.5 },
});

// --- LOWER BAND: kernelized formulation ---
// 9a. Kernelized Lagrangian
s.addImage({ path: EQ35 + "eq1_lagrangian_k_multi.png", x: bandX + 0.6, y: lowY + 0.05, w: 5.815, h: 0.995 });
// green oval around (X_i^T X_j)^2 at the tail of the equation
s.addShape(pres.shapes.OVAL, {
  x: bandX + 0.6 + 4.62, y: lowY + 0.24, w: 1.75, h: 0.6,
  fill: { type: "none" }, line: { color: "2ECC71", width: 1.75 },
});

// 9b. W box (unchanged) and kernelized b box (with green ovals)
const lFormulaY = lowY + 1.12;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX, y: lFormulaY, w: wImgW + 0.3, h: wImgH + 0.12,
  fill: { color: "FFFFFF" }, line: { color: "2980B9", width: 1 },
});
s.addImage({ path: EQ34 + "eq2_W_multi.png", x: bandX + 0.15, y: lFormulaY + 0.06, w: wImgW, h: wImgH });
const bkImgW = 6.99667, bkImgH = 0.44667;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX + wImgW + 0.5, y: lFormulaY + 0.2, w: bkImgW + 0.3, h: bkImgH + 0.12,
  fill: { color: "FFFFFF" }, line: { color: "2980B9", width: 1 },
});
s.addImage({ path: EQ35 + "eq2_b_k_multi.png", x: bandX + wImgW + 0.65, y: lFormulaY + 0.23, w: bkImgW, h: bkImgH });
// green ovals around the two [W^T X_i]^2 terms
s.addShape(pres.shapes.OVAL, {
  x: bandX + wImgW + 0.65 + 2.02, y: lFormulaY + 0.19, w: 1.55, h: 0.54,
  fill: { type: "none" }, line: { color: "2ECC71", width: 1.75 },
});
s.addShape(pres.shapes.OVAL, {
  x: bandX + wImgW + 0.65 + 4.86, y: lFormulaY + 0.19, w: 1.55, h: 0.54,
  fill: { type: "none" }, line: { color: "2ECC71", width: 1.75 },
});

// 9c. Kernelized classification strip with green oval on [W^T Z]^2
const lClassY = lFormulaY + 1.08;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX, y: lClassY, w: 7.6, h: 0.4,
  fill: { color: "FDEBD0" }, line: { type: "none" },
});
s.addText([
  { text: "Class of vector ", options: { color: "2C3E50", fontFace: FONT } },
  { text: "Z", options: { color: "2C3E50", bold: true, fontFace: MATH } },
  { text: " is sign([", options: { color: "2C3E50", fontFace: MATH } },
  { text: "W", options: { color: "2C3E50", fontFace: MATH } },
  { text: "T", options: { color: "2C3E50", fontFace: MATH, superscript: true } },
  { text: " Z]", options: { color: "2C3E50", fontFace: MATH } },
  { text: "2", options: { color: "2C3E50", fontFace: MATH, superscript: true } },
  { text: " + b)", options: { color: "2C3E50", fontFace: MATH } },
], {
  x: bandX, y: lClassY, w: 7.6, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 15, color: "2C3E50", fontFace: MATH, margin: 0,
});
s.addShape(pres.shapes.OVAL, {
  x: bandX + 2.35, y: lClassY + 0.04, w: 1.5, h: 0.32,
  fill: { type: "none" }, line: { color: "2ECC71", width: 1.5 },
});

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_035_recreated.pptx" })
  .then(() => console.log("wrote slide_035_recreated.pptx"))
  .catch(err => console.error(err));