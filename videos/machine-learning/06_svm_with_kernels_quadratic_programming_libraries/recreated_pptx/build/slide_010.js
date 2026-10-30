const pptxgen = require("pptxgenjs");

// Slide 010 — rebuilt from qa/reanalysis2/slide_010_analysis.txt only.
const NUM = 10;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House frame
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

// Two-line red centered title (spec section 2/5, house title box position)
s.addText([
  { text: "Solving Lagrangian Dual Equation of SVM", options: { fontSize: 24, bold: true, color: "C00000", fontFace: FONT } },
  { text: "Using Quadratic Programming", options: { fontSize: 24, bold: true, color: "C00000", fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 1.1,
  align: "center", valign: "top", lineSpacingMultiple: 1.4, margin: 0,
});

// Mouse-pointer arrow, spec region [0.171,0.609,0.206,0.680] -> inches
const ax = 0.171 * W, ay = 0.609 * H;
const aw = (0.206 - 0.171) * W, ah = (0.680 - 0.609) * H;
s.addShape(pres.shapes.LEFT_UP_ARROW, {
  x: ax, y: ay, w: aw, h: ah,
  fill: { color: "000000" }, line: { color: "000000", width: 0.5 },
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_010_recreated.pptx" })
  .then(() => console.log("wrote slide_010_recreated.pptx"))
  .catch(e => console.error(e));
