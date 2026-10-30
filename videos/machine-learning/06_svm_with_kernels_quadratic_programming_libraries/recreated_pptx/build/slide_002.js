const pptxgen = require("pptxgenjs");

// Slide 002 rebuild from qa/reanalysis2/slide_002_analysis.txt (section divider)
const NUM = 2;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_002_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome: outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// House chrome: slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// House title box: "How to call" (red, ~26pt, centered)
s.addText("How to call", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 26, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Line 2: [20.63,48.15,79.38,55.56]% -> x=2.750 y=3.611 w=7.831 h=0.556
s.addText("Python Quadratic Programming Libraries", {
  x: 2.750, y: 3.611, w: 7.831, h: 0.556,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Line 3: [32.29,56.67,67.71,63.00]% -> x=4.304 y=4.250 w=4.722 h=0.475
s.addText("CVXOPT, QuadProg", {
  x: 4.304, y: 4.250, w: 4.722, h: 0.475,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: "3333CC", fontFace: FONT, margin: 0,
});

// Mouse-pointer arrow: [40.21,54.81,43.13,59.26]% -> x=5.360 y=4.111 w=0.389 h=0.334
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: 5.360, y: 4.111, w: 0.389, h: 0.334,
  fill: { color: "000000" }, line: { color: "000000", width: 0.75 },
  rotate: 315,
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
