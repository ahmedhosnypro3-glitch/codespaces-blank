// slide_003.js — FRESH rebuild from qa/reanalysis2/slide_003_analysis.txt (rebuild wave 3).
// Slide: "Input to Quadratic Equation Solver" — three red-bordered white panels with
// colour-coded QP definitions; objective + constraint equations as mathtext PNGs.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_003.js

const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_003/";
const NUM = 3;
const TITLE = "Input to Quadratic Equation Solver";
const W = 13.33, H = 7.5;
const SANS = "Arial";
const SERIF = "Times New Roman";
const RED = "C00000", PANEL_RED = "CC0000", VAR_RED = "FF0000", BLUE = "0000FF",
      GREEN = "008000", BLACK = "000000";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome (mandatory, overrides spec geometry for frame/badge/title)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: SANS, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 14, bold: true, color: RED, fontFace: SANS, margin: 0,
});

// Panels (spec coords -> inches; white fill, thin red stroke)
function panel(y, h) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.91977, y, w: 10.14413, h,
    fill: { color: "FFFFFF" }, line: { color: PANEL_RED, width: 1.5 },
  });
}
panel(1.3875, 1.5675);  // panel 1
panel(3.15, 1.4775);    // panel 2
panel(4.8075, 1.635);   // panel 3

function txt(x, y, w, h, runs, extra) {
  s.addText(runs, Object.assign(
    { x, y, w, h, margin: 0, valign: "top" }, extra || {}));
}
const run = (text, o) => ({ text, options: Object.assign({ fontSize: 11, fontFace: SANS, color: BLACK }, o) });

// Panel headers
txt(1.17304, 1.47, 3.29251, 0.2475,
  [run("Put quadratic equation in the form:", { bold: true, italic: true, color: RED, fontSize: 12 })]);
txt(1.07973, 3.2475, 3.38582, 0.27,
  [run("Put all ≤ , ≥ constraints in the form:", { bold: true, color: RED, fontSize: 12 })]);
txt(1.07973, 4.905, 3.38582, 0.2775, [
  run("Put all ", { bold: true, color: RED, fontSize: 12 }),
  run('Equal "="', { bold: true, italic: true, color: BLUE, fontSize: 12 }),
  run(" constraints in the form:", { bold: true, color: RED, fontSize: 12 }),
]);
// Definition-line builder: var | black italic serif descriptor | red italic serif size | " ,"
function defLine(x, y, w, varRuns, descriptor, size) {
  txt(x, y, w, 0.26, [
    ...varRuns,
    run(" " + descriptor + " ", { italic: true, fontFace: SERIF }),
    run(size, { italic: true, fontFace: SERIF, color: PANEL_RED }),
    run(" ,", { fontFace: SERIF }),
  ]);
}
const vRun = (t, color) => run(t, { bold: true, color, fontSize: 11 });
function mLine(x, y, w) {
  txt(x, y, w, 0.24, [
    run("m", { bold: true, italic: true, color: GREEN, fontSize: 11 }),
    run(" is Number of constraints", { italic: true, fontFace: SERIF }),
    run(" ,", { fontFace: SERIF }),
  ]);
}

// Panel 1: objective equation PNG (exact size, never rescaled), centred in its spec box
s.addImage({ path: EQ + "eq_obj.png", x: 1.09306, y: 2.0979, w: 2.295, h: 0.41667 });
// Mouse-pointer arrow over the equation
s.addImage({ path: EQ + "cursor.png", x: 2.2661, y: 2.4, w: 0.24, h: 0.27833 });
// "where:" label
txt(4.65217, 2.1225, 0.61318, 0.27,
  [run("where:", { bold: true, fontSize: 11 })]);
// Panel-1 definition list (X / P / q^T)
defLine(5.51862, 1.905, 2.77264, [vRun("X", BLUE)], "is a Vector of size", "d+1");
defLine(5.51862, 2.1775, 2.77264, [vRun("P", VAR_RED)], "is a Matrix of size", "d×d");
defLine(5.51862, 2.45, 2.77264,
  [vRun("q", VAR_RED), run("T", { bold: true, color: VAR_RED, superScript: true, fontSize: 11 })],
  "is a Vector of size", "1×d");
// Large red question mark
txt(9.18437, 1.83, 0.54653, 0.6675,
  [run("?", { bold: true, color: RED, fontSize: 40 })],
  { align: "center", valign: "middle" });

// Panel 2: G x ≤ h equation PNG, where:, definition list (X / G / h)
s.addImage({ path: EQ + "eq_gxleh.png", x: 1.07973, y: 3.888, w: 0.81667, h: 0.26333 });
mLine(3.91902, 3.57, 2.71932);
txt(3.03924, 3.93, 0.62651, 0.2475, [run("where:", { bold: true, fontSize: 11 })]);
defLine(3.91902, 3.8175, 2.63934, [vRun("X", BLUE)], "is a Vector of size", "d+1");
defLine(3.91902, 4.06, 2.63934, [vRun("G", VAR_RED)], "is a Matrix of size", "m×d");
defLine(3.91902, 4.3025, 2.63934, [vRun("h", BLUE)], "is a Vector of size", "m×1");

// Panel 3: A x = b equation PNG, where:, definition list (X / A / b)
s.addImage({ path: EQ + "eq_axeqb.png", x: 1.07973, y: 5.5083, w: 0.80833, h: 0.26333 });
mLine(3.91902, 5.22, 2.71932);
txt(2.95926, 5.5425, 0.65317, 0.2475, [run("where:", { bold: true, fontSize: 11 })]);
defLine(3.91902, 5.445, 2.63934, [vRun("X", BLUE)], "is a Vector of size", "d+1");
defLine(3.91902, 5.69, 2.63934, [vRun("A", VAR_RED)], "is a Matrix of size", "m×d");
defLine(3.91902, 5.935, 2.63934, [vRun("b", BLUE)], "is a Vector of size", "m×1");

// Solid black band across the bottom of the capture
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5332, y: 6.8475, w: 12.2636, h: 0.6525,
  fill: { color: "000000" }, line: { type: "none" },
});

pres.writeFile({ fileName: NS + "/recreated_pptx/slide_003_recreated.pptx" });
console.log("wrote slide_003_recreated.pptx");
