// slide_032.js — "New Kernel Functions can be derived From other Kernels"
// FRESH rebuild from qa/reanalysis2/slide_032_analysis.txt only (wave 3).
// House chrome per namespace AGENTS.md overrides spec. No plots (IMAGERY: none).
// Equations: matplotlib mathtext 600dpi PNGs in eq_032/ (render_math.py).
// Run: NODE_PATH=$(npm root -g) node slide_032.js

const pptxgen = require("pptxgenjs");

const NUM = 32;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const EQ = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_032/";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House red outer frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// House badge (numeral 32)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// House title box, two verbatim lines, red bold centered
s.addText("New Kernel Functions can be derived\nFrom other Kernels", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.1,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Four blue-bordered white panels, spec section 4 coords (normalized -> inches)
const panels = [
  [0.05, 0.22, 0.95, 0.43],
  [0.05, 0.45, 0.95, 0.60],
  [0.05, 0.62, 0.95, 0.77],
  [0.05, 0.79, 0.95, 0.94],
];
panels.forEach(([x0, y0, x1, y1]) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: x0 * W, y: y0 * H, w: (x1 - x0) * W, h: (y1 - y0) * H,
    fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 },
  });
});

// Panel headers: verbatim spec strings, bold black left-aligned, wide boxes
const headers = [
  { t: "Sum of Kernels is a Kernel", y: 0.25 * H },
  { t: "Scalar Product of  Kernel is a kernel", y: 3.525 },
  { t: "Product of Kernels is a Kernel", y: 4.80 },
  { t: "Combination of the above rules is a Kernel", y: 6.075 },
];
headers.forEach(h => {
  s.addText(h.t, {
    x: 1.33, y: h.y, w: 9.5, h: 0.4,
    align: "left", valign: "top",
    fontSize: 20, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
});
// Equations: spec section 8 boxes, images centered inside, exact size w=px/600
const eqs = [
  // [specBox, image, w_in, h_in]
  [[0.10, 0.29, 0.90, 0.41], "eq1.png", 3.81667, 0.34667],
  [[0.10, 0.51, 0.75, 0.58], "eq2.png", 2.74, 0.35],
  [[0.10, 0.67, 0.85, 0.75], "eq3.png", 3.73167, 0.34667],
  [[0.10, 0.84, 0.92, 0.92], "eq4.png", 5.32833, 0.34667],
];
eqs.forEach(([box, img, wIn, hIn]) => {
  const bx = box[0] * W, by = box[1] * H, bw = (box[2] - box[0]) * W, bh = (box[3] - box[1]) * H;
  s.addImage({
    path: EQ + img,
    x: bx + (bw - wIn) / 2, y: by + (bh - hIn) / 2,
    w: wIn, h: hIn,
  });
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_032_recreated.pptx",
});
