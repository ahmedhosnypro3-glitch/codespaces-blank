// slide_033.js — FRESH rebuild (wave 3) from qa/reanalysis2/slide_033_analysis.txt only.
// Spec: title-only slide "How to Kernelize SVM" + black bottom band + pointer stroke.
// House chrome (frame/badge/title box/background) overrides the spec per house rule.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_033.js

const pptxgen = require("pptxgenjs");

const NUM = 33;
const TITLE = "How to Kernelize SVM";
const FONT = "Arial";
const W = 13.33, H = 7.5;
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_033_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// 1. House outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. House slide-number badge (numeral = printed number, no padding)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title (house box position; spec text/size/color: bold red ~32pt, centred)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.65,
  align: "center", valign: "top",
  fontSize: 32, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Spec black band across the bottom of the frame
//    box [0.040, 0.848, 0.917, 1.000] -> inches
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.040 * 13.33, y: 0.848 * 7.5,
  w: (0.917 - 0.040) * 13.33, h: (1.000 - 0.848) * 7.5,
  fill: { color: "000000" }, line: { type: "none" },
});

// 5. Spec pointer stroke, lower-left quadrant
//    box [0.163, 0.706, 0.183, 0.744] -> diagonal line, dark grey
s.addShape(pres.shapes.LINE, {
  x: 0.163 * 13.33, y: 0.706 * 7.5,
  w: (0.183 - 0.163) * 13.33, h: (0.744 - 0.706) * 7.5,
  line: { color: "555555", width: 1.75 },
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(err => { console.error(err); process.exit(1); });
