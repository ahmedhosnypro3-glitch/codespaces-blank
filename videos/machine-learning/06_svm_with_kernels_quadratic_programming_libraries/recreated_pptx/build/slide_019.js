// slide_019.js — FRESH rebuild from qa/reanalysis2/slide_019_analysis.txt (rebuild wave 3)
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_019.js
const pptxgen = require("pptxgenjs");

const NUM = 19;
const TITLE = "Kernels";
const W = 13.33, H = 7.5;
const ARIAL = "Arial";
const SERIF = "Times New Roman";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_019/eq19_kernel.png";
const EQ_W = 8.13667, EQ_H = 0.38667; // px/600 from render_math.py, never rescaled

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec): red frame, badge, title box
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
  fontSize: 18, bold: true, color: "333333", fontFace: ARIAL, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: ARIAL, margin: 0,
});

// Faint top rule [0.059,0.065,0.905,0.070]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.78647, y: 0.4875, w: 11.27318, h: 0.0375,
  fill: { color: "E6E6E6" }, line: { color: "E6E6E6", width: 0 },
});

// Black bottom band [0.039,0.867,0.904,1.000]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.52087, y: 6.5025, w: 11.51645, h: 0.9975,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

// Inner blue rectangle around bullets [0.068,0.172,0.852,0.837]
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.90644, y: 1.29, w: 10.44672, h: 4.9875,
  fill: { type: "none" }, line: { color: "0000CC", width: 1 },
});

// Six square bullet markers at x≈0.087
[1.62, 2.3775, 3.3225, 4.7325, 5.175, 5.895].forEach(cy => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 1.15971, y: cy - 0.035, w: 0.07, h: 0.07,
    fill: { color: "000080" }, line: { color: "000080", width: 0 },
  });
});

// Small diagonal pointer arrow [0.267,0.226,0.283,0.261], head at upper-left tip
s.addShape(pres.shapes.LINE, {
  x: 3.77239, y: 1.9575, w: -0.21328, h: -0.2625,
  line: { color: "4A6FB0", width: 1, endArrow: "triangle" },
});
// Bullet 1 [0.082,0.196,0.731,0.238] — "dot product of two vectors" bold red
s.addText([
  { text: "Kernels Represent  a " },
  { text: "dot product of two vectors", options: { bold: true, color: "CC0000" } },
  { text: " in a higher dimensional feature space" },
], {
  x: 1.09306, y: 1.47, w: 8.65787, h: 0.315,
  align: "left", valign: "middle",
  fontSize: 16, color: "000000", fontFace: SERIF, margin: 0,
});

// Bullet 2 [0.082,0.298,0.758,0.337]
s.addText("Any Machine Learning Model that contains dot product of input samples can be kernelized", {
  x: 1.09306, y: 2.235, w: 9.01694, h: 0.2925,
  align: "left", valign: "middle",
  fontSize: 16, color: "000000", fontFace: SERIF, margin: 0,
});

// Bullet 3 [0.082,0.402,0.851,0.494] — two lines, red underlined clause
s.addText([
  { text: "Instead of calculating dot product between input vectors, " },
  { text: "calculate dot product between input\nvectors after mapping them to higher dimensional space",
    options: { color: "CC0000", underline: true } },
], {
  x: 1.09306, y: 3.015, w: 10.26443, h: 0.69,
  align: "left", valign: "middle", lineSpacing: 20,
  fontSize: 16, color: "000000", fontFace: SERIF, margin: 0,
});

// Equation image centered in [0.122,0.530,0.762,0.587]
s.addImage({ path: EQ, x: 1.82453, y: 3.99542, w: EQ_W, h: EQ_H });

// Bullet 4 [0.082,0.613,0.613,0.652]
s.addText("Different Kernel functions are based on different mapping functions", {
  x: 1.09306, y: 4.5975, w: 7.07411, h: 0.2925,
  align: "left", valign: "middle",
  fontSize: 16, color: "000000", fontFace: SERIF, margin: 0,
});

// Bullet 5 [0.082,0.667,0.845,0.752] — two lines, blue italic
s.addText("Calculations of mapping  and  calculations of dot product in higher dimensional space are very\nexpensive.", {
  x: 1.09306, y: 5.0025, w: 10.17285, h: 0.6375,
  align: "left", valign: "middle", lineSpacing: 20,
  fontSize: 16, italic: true, color: "0000CC", fontFace: SERIF, margin: 0,
});

// Bullet 6 [0.082,0.770,0.610,0.811] — "Kernel Trick" bold red
s.addText([
  { text: "Use " },
  { text: "Kernel Trick", options: { bold: true, color: "CC0000" } },
  { text: " to minimize  both calculations (at no extra cost)" },
], {
  x: 1.09306, y: 5.775, w: 6.93337, h: 0.3075,
  align: "left", valign: "middle",
  fontSize: 16, color: "000000", fontFace: SERIF, margin: 0,
});

pres.writeFile({ fileName: NS + "/recreated_pptx/slide_019_recreated.pptx" })
  .then(() => console.log("wrote slide_019_recreated.pptx"))
  .catch(e => console.error(e));
