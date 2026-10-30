const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 11;
const TITLE = "Training Vectors: SVM QP Formulation";
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

// Training data
s.addText("Training Vectors:", { x: 0.5, y: 0.9, w: 6.0, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("x1 = (1, 1), y1 = 1", { x: 0.5, y: 1.2, w: 6.0, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("x2 = (2, 2), y2 = 1", { x: 0.5, y: 1.45, w: 6.0, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("x3 = (7, 4), y3 = 1", { x: 0.5, y: 1.7, w: 6.0, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("x4 = (4, 8), y4 = -1", { x: 0.5, y: 1.95, w: 6.0, h: 0.25, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });

s.addText("Use C = 1", { x: 6.5, y: 0.9, w: 6.3, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Objective
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.3, w: 12.3, h: 1.5, fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1.5 } });
s.addText("Maximize L = \u2211 \u03b1_i - \u00bd \u2211 \u2211 \u03b1_i \u03b1_j y_i y_j x_i^T x_j", { x: 0.7, y: 2.4, w: 11.8, h: 0.3, fontSize: 15, color: "333333", fontFace: FONT, margin: 0 });
s.addText("=> Minimize L_D(\u03b1) = \u00bd \u2211 \u2211 \u03b1_i \u03b1_j y_i y_j x_i^T x_j - \u2211 \u03b1_i", { x: 0.7, y: 2.75, w: 11.8, h: 0.3, fontSize: 15, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("\u03b1_1 y_1 + \u03b1_2 y_2 + \u03b1_3 y_3 + \u03b1_4 y_4 = 0", { x: 0.7, y: 3.1, w: 11.8, h: 0.3, fontSize: 15, color: "333333", fontFace: FONT, margin: 0 });

// Quadratic equation
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.95, w: 12.3, h: 2.5, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 } });
s.addText("Minimize: [ +\u03b1_1^2 + 2\u03b1_1\u03b1_2 - 5.5\u03b1_1\u03b1_3 - 6\u03b1_1\u03b1_4 + 2\u03b1_2\u03b1_1 + 4\u03b1_2^2 - 11\u03b1_2\u03b1_3 - 12\u03b1_2\u03b1_4", { x: 0.7, y: 4.05, w: 11.8, h: 0.3, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("          - 5.5\u03b1_3\u03b1_1 - 11\u03b1_3\u03b1_2 + 32.5\u03b1_3^2 + 36\u03b1_3\u03b1_4 - 6\u03b1_4\u03b1_1 - 12\u03b1_4\u03b1_2 + 36\u03b1_4\u03b1_3 + 40\u03b1_4^2 ]", { x: 0.7, y: 4.35, w: 11.8, h: 0.3, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("          - [ \u03b1_1 + \u03b1_2 + \u03b1_3 + \u03b1_4 ]", { x: 0.7, y: 4.65, w: 11.8, h: 0.3, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("Subject to: \u03b1_1 + \u03b1_2 - \u03b1_3 - \u03b1_4 = 0", { x: 0.7, y: 5.0, w: 11.8, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("\u03b1_1, \u03b1_2, \u03b1_3, \u03b1_4 \u2264 1 (C)", { x: 0.7, y: 5.35, w: 11.8, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("\u03b1_1, \u03b1_2, \u03b1_3, \u03b1_4 \u2265 0", { x: 0.7, y: 5.7, w: 11.8, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("Quadratic Equation in \u03b1 with constraints", { x: 0.7, y: 6.05, w: 11.8, h: 0.3, fontSize: 14, bold: true, color: "E74C3C", fontFace: FONT, margin: 0 });

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_011_recreated.pptx" })
  .then(() => console.log("wrote slide_011_recreated.pptx"))
  .catch(e => console.error(e));