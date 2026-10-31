const pptxgen = require("pptxgenjs");
const path = require("path");
// Slide 039 — FRESH wave-3 rebuild from qa/reanalysis2/slide_039_analysis.txt ONLY
// (spec starts at its "1. SLIDE_TITLE" line). House chrome overrides spec geometry.
// Run from project root: node <NS>/recreated_pptx/build/slide_039.js
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = path.join(NS, "recreated_pptx", "slide_039_recreated.pptx");
const W = 13.33, H = 7.5, FONT = "Arial";
const NUM = 39;
const TITLE = "Bonus Assignment (SVM with Kernels)";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome: outer red frame, badge, title box
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

// Spec visual element: inner blue-bordered white content box [0.086,0.170,0.942,0.902]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.086 * W, y: 0.170 * H,
  w: (0.942 - 0.086) * W, h: (0.902 - 0.170) * H,
  fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1.5 },
});

// Spec bullets: verbatim strings with the spec's line breaks (breakLine runs keep
// wrapped lines in the same paragraph, so no second bullet glyph).
function bullet(x0, y0, x1, y1, lines) {
  const runs = lines.map((t, i) => ({ text: t, options: i ? { breakLine: true } : {} }));
  s.addText(runs, {
    x: x0 * W, y: y0 * H, w: (x1 - x0) * W + 0.4, h: (y1 - y0) * H,
    align: "left", valign: "top",
    fontSize: 17, color: "0000CC", fontFace: FONT, margin: 0,
    bullet: { characterCode: "2022", indent: 20 },
  });
}

bullet(0.108, 0.226, 0.565, 0.266, [
  "Develop your own SVM library (from Scratch)",
]);
bullet(0.108, 0.287, 0.854, 0.377, [
  "You may use any Quadratic Programming solver (e.g. quadprog, CVXOPT, ..) to solve",
  "the Lagrangian Equation.",
]);
bullet(0.108, 0.408, 0.630, 0.449, [
  "Make use of Kernel functions (e.g. Quadratic , Polynomial, or RBF)",
]);
bullet(0.108, 0.474, 0.422, 0.514, [
  "For each of the given dataset (2-D):",
]);
bullet(0.152, 0.544, 0.856, 0.631, [
  "Draw the dataset points using color coding (assign same color to points belong to",
  "same class)",
]);
bullet(0.152, 0.672, 0.873, 0.759, [
  "Divide the background into grid, classify each point in the grid, give each point",
  "same color code of the class it belongs to.",
]);

// Spec visual element: mouse pointer overlay near bullet 3 [0.350,0.441,0.376,0.505]
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: 0.350 * W, y: 0.441 * H,
  w: (0.376 - 0.350) * W, h: (0.505 - 0.441) * H,
  fill: { color: "000000" }, line: { color: "FFFFFF", width: 0.75 },
  rotation: 315,
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch((e) => { console.error(e); process.exit(1); });
