const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Slide 010 — FRESH wave-3 rebuild from qa/reanalysis2/slide_010_analysis.txt ONLY.
// Spec: title-only slide, two red centred title lines + a small mouse-pointer arrow
// in the empty field. No equations, no graphs, no body text.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_010.js

const NUM = 10;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_010");
const OUT = path.join(NS, "recreated_pptx/slide_010_recreated.pptx");

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

// ---- title (house title box; two verbatim lines via \n -> real <a:br/> breaks) ----
s.addText("Solving Lagrangian Dual Equation of SVM\nUsing Quadratic Programming", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.6,
  align: "center", valign: "top", lineSpacingMultiple: 1.4, margin: 0,
  fontSize: 34, bold: true, color: "C00000", fontFace: FONT,
});

// ---- mouse-pointer arrow, spec region [0.171,0.609,0.206,0.680] ----
const X = n => n * 13.33, Y = n => n * 7.5;
const cur = JSON.parse(fs.readFileSync(path.join(EQ, "cursor.png.json")));
s.addImage({
  path: path.join(EQ, "cursor.png"),
  x: X(0.171), y: Y(0.609),
  w: cur.w_in, h: cur.h_in,
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
