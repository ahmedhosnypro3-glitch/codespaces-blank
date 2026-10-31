// slide_006.js — FRESH rebuild from qa/reanalysis2/slide_006_analysis.txt (rebuild wave 3).
// Slide: "Less Than Equal Constraints" — three bordered panels: leq / geq / chained
// constraint strings with stacked matrix-vector inequalities, G x <= h chips, Convert chip.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_006.js

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_006/";
const NUM = 6;
const TITLE = "Less Than Equal Constraints";
const W = 13.33, H = 7.5;
const SANS = "Arial";
const RED = "C00000", LABEL_RED = "FF0000", BLUE = "0000FF", GREEN = "008000",
      BLACK = "000000", ORANGE = "FF8C00";

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
  fontSize: 28, bold: true, color: RED, fontFace: SANS, margin: 0,
});

// Spec normalized coords -> inches: x*13.33, y*7.5. Content containers (white, gray border)
function container(y, h) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.3999, y, w: 12.5302, h,
    fill: { color: "FFFFFF" }, line: { color: "808080", width: 0.75 },
  });
}
container(1.2, 1.35);     // panel 1 [0.030,0.160,0.970,0.340]
container(2.5875, 1.725); // panel 2 [0.030,0.345,0.970,0.575]
container(4.3875, 2.175); // panel 3 [0.030,0.585,0.970,0.875]

// G x <= h chips (red outline, pale fill) + their mathtext PNG centered inside
function gxChip(cx, cy, w) {
  const h = 0.35;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: cx - w / 2, y: cy - h / 2, w, h,
    fill: { color: "FFFDD0" }, line: { color: LABEL_RED, width: 1.25 },
  });
  const j = JSON.parse(fs.readFileSync(EQ + "gxleh.json"));
  s.addImage({ path: EQ + "gxleh.png", x: cx - j.w_in / 2, y: cy - j.h_in / 2, w: j.w_in });
}
gxChip(9.74455, 1.99125, 1.5731); // [0.672,0.246,0.790,0.285]
gxChip(9.74455, 4.21875, 1.5731); // [0.672,0.545,0.790,0.580]
gxChip(9.7644, 5.4, 1.5332);      // [0.675,0.700,0.790,0.740]

// Convert chip (yellow fill, gray outline) [0.674,0.375,0.902,0.535]
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 8.9856, y: 2.8125, w: 3.0392, h: 1.2,
  fill: { color: "FFFF99" }, line: { color: "808080", width: 0.75 },
});

function txt(x, y, w, runs, extra) {
  s.addText(runs, Object.assign(
    { x, y, w, h: 0.35, margin: 0, valign: "middle" }, extra || {}));
}
const run = (text, o) => ({ text, options: Object.assign(
  { fontSize: 11, fontFace: SANS, color: BLACK }, o) });
const img = (name, x, y) => {
  const j = JSON.parse(fs.readFileSync(EQ + name + ".json"));
  s.addImage({ path: EQ + name + ".png", x, y, w: j.w_in });
  return j;
};
// Panel headers (red bold italic, spec y; wide left boxes per lesson)
txt(1.33, 1.425, 9.5, [run("3 constraints", { bold: true, italic: true, color: LABEL_RED, fontSize: 14 })],
  { align: "left" });
txt(1.33, 4.6125, 9.5, [run("6 constraints , 3 variables", { bold: true, italic: true, color: LABEL_RED, fontSize: 14 })],
  { align: "left" });

// Convert chip contents: heading + two green conversion lines + "to"
txt(8.9856, 2.8425, 3.0392, [run("Convert", { bold: true, italic: true, color: ORANGE, fontSize: 11 })],
  { align: "center" });
// place conv lines centered in chip (chip cx=10.5052)
{
  const j1 = JSON.parse(fs.readFileSync(EQ + "conv1.json"));
  s.addImage({ path: EQ + "conv1.png", x: 10.5052 - j1.w_in / 2, y: 3.2625 + (0.225 - j1.h_in) / 2, w: j1.w_in });
  const j2 = JSON.parse(fs.readFileSync(EQ + "conv2.json"));
  s.addImage({ path: EQ + "conv2.png", x: 10.5052 - j2.w_in / 2, y: 3.6375 + (0.225 - j2.h_in) / 2, w: j2.w_in });
}
txt(8.9856, 3.39, 3.0392, [run("to", { color: GREEN, fontSize: 11 })], { align: "center" });

// Row 1 (panel 1): x1<=z1, x2<=z2, x3<=z3  =>  I [x] <= [z]
img("le_str", 0.8665, 1.7775 + (0.285 - 0.27667) / 2);
img("arrow", 4.55, 2.04375 - 0.245 / 2);
img("m3_id", 4.8655, 2.04375 - 0.43333 / 2);
img("vx3", 6.4972, 2.04375 - 0.45 / 2);
img("leq", 7.3989, 2.04375 - 0.115 / 2);
img("vz3", 7.6389, 2.04375 - 0.45 / 2);

// Row 2 (panel 2): x1>=z1, x2>=z2, x3>=z3  =>  -I [x] <= [-z]
img("ge_str", 0.8665, 2.8875 + (0.3 - 0.27667) / 2);
img("arrow", 4.55, 3.20625 - 0.245 / 2);
img("m3_neg", 4.8655, 3.20625 - 0.43333 / 2);
img("vx3", 6.4972, 3.20625 - 0.45 / 2);
img("leq", 7.3989, 3.20625 - 0.115 / 2);
img("vnegz3", 7.6389, 3.20625 - 0.45 / 2);

// Row 3 (panel 3): y<=x<=z chained  =>  6x3 matrix [x] <= [-y; z]
img("chain_str", 0.8665, 4.9875 + (0.3 - 0.20833) / 2);
img("arrow", 4.55, 5.45625 - 0.245 / 2);
img("m6", 4.8655, 5.45625 - 0.93333 / 2);
img("vx3", 6.4972, 4.98958); // top-aligned with the 6-row matrix
img("leq", 7.3989, 5.45625 - 0.115 / 2);
img("vyz6", 7.6389, 4.98958);
txt(4.8655, 5.9625, 2.0, [run("6 x 3", { color: LABEL_RED, fontSize: 10 })], { align: "center" });

pres.writeFile({ fileName: NS + "/recreated_pptx/slide_006_recreated.pptx" });
console.log("wrote slide_006_recreated.pptx");
