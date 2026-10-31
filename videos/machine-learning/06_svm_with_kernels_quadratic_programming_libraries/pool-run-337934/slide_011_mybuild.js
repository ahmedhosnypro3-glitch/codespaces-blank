// slide_011.js — REBUILD WAVE 3, built only from qa/reanalysis2 + judge findings + doc-parse
// of unique_slides/slide_011.jpg. Run: NODE_PATH=$(npm root -g) node slide_011.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_011") + "/";
const NUM = 11;
const TITLE = "Training Vectors: SVM QP Formulation";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Top-left: Training Vectors box with all four vectors + labels
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.35, y: 0.95, w: 4.35, h: 1.9,
  fill: { color: "FBF7C8" }, line: { color: "BFBFBF", width: 1 },
});
s.addText("Training Vectors", {
  x: 0.5, y: 1.02, w: 4.0, h: 0.28,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addImage({ path: EQ + "eq_vecs.png", x: 0.5, y: 1.32, w: 2.81167, h: 1.495 });

// Top-middle: Test Vectors box
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.85, y: 0.95, w: 2.7, h: 1.9,
  fill: { color: "FBF7C8" }, line: { color: "BFBFBF", width: 1 },
});
s.addText("Test Vectors", {
  x: 5.0, y: 1.02, w: 2.4, h: 0.28,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addImage({ path: EQ + "eq_test.png", x: 5.15, y: 1.45, w: 1.76167, h: 0.94667 });
// Top-right: "Use C=1" inside a red rectangular callout box
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.7, y: 0.95, w: 2.3, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 2 },
});
s.addText("Use C=1", {
  x: 7.7, y: 0.95, w: 2.3, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Top-right: constraint box — equality + four separate 0<=alpha_i<=C rows
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.7, y: 1.55, w: 5.28, h: 1.3,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});
s.addImage({ path: EQ + "eq_cons.png", x: 7.85, y: 1.68, w: 2.45333, h: 0.84833 });

// Middle band: Maximize => Minimize dual (blue outline)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.35, y: 3.0, w: 12.63, h: 0.72,
  fill: { color: "FFFFFF" }, line: { color: "1F4E79", width: 1.5 },
});
s.addImage({ path: EQ + "eq_dual.png", x: 0.55, y: 3.06, w: 8.08333, h: 0.59667 });

// Diagonal watermark (large grey, as in original)
s.addText("From Previous Lecture", {
  x: 3.2, y: 3.72, w: 6.6, h: 0.5, rotate: -18,
  fontSize: 20, bold: true, italic: true, color: "808080", fontFace: FONT, margin: 0,
});
// Matrices row: X, G = X^T X, Y = (y_i y_j), Y∘G
s.addImage({ path: EQ + "eq_X.png", x: 0.5, y: 4.25, w: 1.86333, h: 1.245 });
s.addImage({ path: EQ + "eq_G.png", x: 3.0, y: 4.2, w: 2.33167, h: 1.32167 });
s.addImage({ path: EQ + "eq_Y.png", x: 6.2, y: 4.22, w: 2.43833, h: 1.295 });
s.addImage({ path: EQ + "eq_YG.png", x: 9.2, y: 4.2, w: 1.81167, h: 1.325 });

// Lower red panel: quadratic objective + constraints
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.35, y: 5.6, w: 12.63, h: 1.75,
  fill: { color: "FFF7F7" }, line: { color: "C00000", width: 1.5 },
});
s.addText("Minimize:", {
  x: 0.5, y: 5.68, w: 1.3, h: 0.3,
  fontSize: 13, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
// objective across three aligned lines, leading "[ +1a1^2+2a1a2-5.5a1a3-6a1a4..."
s.addImage({ path: EQ + "eq_obj.png", x: 1.85, y: 5.64, w: 7.385, h: 1.02 });
// four separate 0 <= alpha_i <= C rows, right side of panel
s.addImage({ path: EQ + "eq_bounds.png", x: 9.6, y: 5.64, w: 1.055, h: 0.645 });

// "Subject to:" on its own line
s.addText("Subject to:", {
  x: 0.5, y: 6.78, w: 1.3, h: 0.3,
  fontSize: 12, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addImage({ path: EQ + "eq_subj.png", x: 1.85, y: 6.72, w: 7.39333, h: 0.565 });

// "Quadratic Equation in α with constraints" bottom-RIGHT of the panel
s.addText("Quadratic Equation in \u03b1 with constraints", {
  x: 8.3, y: 6.95, w: 4.6, h: 0.35,
  align: "right", valign: "middle",
  fontSize: 12, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_011_recreated.pptx") })
  .then(() => console.log("wrote slide_011_recreated.pptx"))
  .catch(e => console.error(e));
