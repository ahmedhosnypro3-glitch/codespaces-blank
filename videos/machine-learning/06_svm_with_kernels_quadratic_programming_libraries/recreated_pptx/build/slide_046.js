// slide_046.js — Three spiral arms (generated via graphgen)
// House frame + embedded matplotlib PNG for correct spiral topology
// Run: NODE_PATH=$(npm root -g) node slide_046.js

const pptxgen = require("pptxgenjs");

const NUM = 46;
const TITLE = "SVM Kernel Decision Boundary — Spiral Data";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// Badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Embed generated graph PNG (plot area: x 0-35, y -10 to 40)
const plotX = 1.5, plotY = 1.0, plotW = 11.0, plotH = 6.0;

s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/slide_046_graph.png",
  x: plotX, y: plotY, w: plotW, h: plotH,
});

// No legend per original (judge: original has no legend)
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_046_recreated.pptx" })
  .then(() => console.log("wrote slide_046_recreated.pptx"))
  .catch(err => console.error(err));