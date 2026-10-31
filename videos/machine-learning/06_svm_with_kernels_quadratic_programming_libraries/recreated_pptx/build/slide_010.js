const pptxgen = require("pptxgenjs");

// Slide 010 — FRESH wave-3 rebuild from qa/reanalysis2/slide_010_analysis.txt ONLY.
// Spec: section-header slide. Verbatim content is exactly the two-line title
// "Solving Lagrangian Dual Equation of SVM" / "Using Quadratic Programming"
// plus the badge numeral 10. The spec's grey panel / black bottom band / mouse
// pointer are video-player chrome, not slide content; house chrome (grey E8E8E8
// background, red frame, yellow badge, title at y=0.28) overrides the spec.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_010.js

const NUM = 10;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = BASE + "/recreated_pptx/slide_010_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (mandatory, overrides spec geometry) ----
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
s.addText("Solving Lagrangian Dual Equation of SVM\nUsing Quadratic Programming", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.2,
  align: "center", valign: "top",
  fontSize: 22, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
