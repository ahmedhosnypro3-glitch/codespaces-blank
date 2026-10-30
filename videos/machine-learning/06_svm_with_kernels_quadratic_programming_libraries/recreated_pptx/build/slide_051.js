// slide_051.js — Blue upper-left / Red lower-right with blue grid shading
const { newPres, addHouseChrome, addPlotShell, addCluster, addLegend, W, H } = require("./shared.js");

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, 51, "SVM Classes with Decision Region Shading");

const m = addPlotShell(pres, s, 1.5, 1.0, 11.0, 6.0, -10, 50, -10, 40, "Feature 1", "Feature 2");

// Light blue grid shading in upper-left (0..50 x, 0..30 y approx)
// Add as a large semi-transparent rectangle
s.addShape(pres.shapes.RECTANGLE, {
  x: m.toX(0), y: m.toY(30),
  w: m.toX(50) - m.toX(0), h: m.toY(0) - m.toY(30),
  fill: { color: "ADD8E6", transparency: 70 }, line: { type: "none" },
});

// Blue scatter upper-left
addCluster(pres, s, m, 15, 20, 25, 80, "0000FF", 0.05);

// Red scatter lower-right
addCluster(pres, s, m, 30, 10, 20, 100, "FF0000", 0.05);

// Tiny glyph near origin (annotation)
s.addText("•", {
  x: m.toX(0) - 0.1, y: m.toY(0) - 0.1, w: 0.2, h: 0.2,
  fontSize: 12, color: "000000", fontFace: "Arial", margin: 0,
});

addLegend(pres, s, 1.7, 1.2, [
  { text: "■ Decision region (class 1)", color: "ADD8E6" },
  { text: "● Blue class (upper-left)", color: "0000FF" },
  { text: "● Red class (lower-right)", color: "FF0000" },
]);

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_051_recreated.pptx" })
  .then(() => console.log("wrote slide_051_recreated.pptx"))
  .catch(err => console.error(err));