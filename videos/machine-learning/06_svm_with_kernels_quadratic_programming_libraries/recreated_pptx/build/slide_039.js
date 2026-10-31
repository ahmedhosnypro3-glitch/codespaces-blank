const pptxgen = require("pptxgenjs");

// Slide 039 — FRESH rebuild (wave 3) from qa/reanalysis2/slide_039_analysis.txt ONLY.
// Spec: title "Bonus Assignment (SVM with Kernels)" + 6 bullets (4 top-level, 2 nested).
// No equations, no plots. House chrome overrides spec geometry per house rule.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_039.js

const NUM = 39;
const TITLE = "Bonus Assignment (SVM with Kernels)";
const FONT = "Arial";
const W = 13.33, H = 7.5;
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_039_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. House badge: yellow circle + numeral "39"
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title in the house title box (spec: bold ~24pt red, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Spec bullets — verbatim strings, black ~14pt, left-aligned.
//    Wide boxes (lesson from slide 001 judge FAIL) so LO never wraps/overlaps.
function bullet(yIn, text, indentIn) {
  s.addText(text, {
    x: 0.10 * W + indentIn, y: yIn, w: 9.5, h: 0.55,
    align: "left", valign: "top",
    fontSize: 14, color: "000000", fontFace: FONT, margin: 0,
    bullet: { code: "2022" }, indent: indentIn > 0 ? 1 : 0,
  });
}

// Body block placed to match the original's measured text extent
// (first body line ynorm ~0.246 -> 1.85 in, pitch ~0.85 in, last line ~ynorm 0.85)
bullet(1.85, "Develop your own SVM library (from Scratch)", 0);
bullet(2.70, "You may use any Quadratic Programming solver (e.g. quadprog, CVXOPT, ..) to solve the Lagrangian Equation.", 0);
bullet(3.55, "Make use of Kernel functions (e.g. Quadratic , Polynomial, or RBF)", 0);
bullet(4.40, "For each of the given dataset (2-D):", 0);
bullet(5.25, "Draw the dataset points using color coding (assign same color to points belong to same class)", 0.5);
bullet(6.10, "Divide the background into grid, classify each point in the grid, give each point same color code of the class it belongs to.", 0.5);

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
