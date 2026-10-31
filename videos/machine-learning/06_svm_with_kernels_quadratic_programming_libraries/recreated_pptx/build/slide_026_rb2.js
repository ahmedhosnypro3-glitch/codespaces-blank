// slide_026.js — REBUILD from qa/reanalysis2/slide_026_analysis.txt (wave 3).
// Spec geometry normalized [x0,y0,x1,y1] -> inches x*13.33, y*7.5.
// Run: NODE_PATH=$(npm root -g) node slide_026.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_026/";
const man = JSON.parse(fs.readFileSync(EQ + "manifest.json", "utf8"));
const W = 13.33, H = 7.5;
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome (overrides spec): red frame, badge, title box
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("26", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Quadratic Kernel Mapping and Kernel Trick", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Content panels (spec section 3/4): rounded rects, blue border
function panel(x, y, w, h, fill) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: fill }, line: { color: "3A4FC0", width: 1.5 }, adj: 0.05,
  });
}
panel(0.866, 1.058, 10.772, 3.263, "FDF6E3"); // upper cream panel
panel(0.866, 4.350, 10.772, 1.973, "FFFFFF"); // lower white panel

// Peach highlights behind the squared inner-product terms
function hl(x, y, w, h) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: "FBE2D3" }, line: { color: "E8A87C", width: 0.75 }, adj: 0.25,
  });
}
hl(0.946, 2.018, 0.667, 0.510); // behind (a^T b)^2, upper line 2
hl(0.946, 3.165, 0.627, 0.503); // behind [a^T b]^2, upper line 3
hl(7.706, 5.580, 0.627, 0.293); // behind [a^T b]^2, lower line 2

// Equation images: exact size w = px/600 in, vertically centered in spec box
function eq(name, x, y, w, h) {
  const m = man[name];
  s.addImage({ path: EQ + m.file, x, y: y + Math.max(0, (h - m.h_in) / 2), w: m.w_in });
}
eq("eq1_a", 1.000, 1.223, 0.693, 0.525);   // a = (a1,a2)^T  red
eq("eq2_b", 1.906, 1.223, 0.693, 0.525);   // b = (b1,b2)^T  blue
eq("eq3_chain", 0.946, 1.988, 6.761, 0.585); // (a^Tb)^2 = ... chain
eq("eq4_phi", 0.946, 2.850, 4.773, 1.148);   // [a^Tb]^2 = (phi(a)|phi(b)) = phi(a)^T phi(b)
eq("eq5_where", 7.079, 2.850, 3.680, 1.178); // Where: phi(x) = ... => ...
eq("eq6_cap", 8.958, 3.945, 1.174, 0.248);   // 2D => 3D  red caption
eq("eq7_a", 0.946, 4.418, 0.747, 0.608);     // a = (1,2)^T  red
eq("eq8_b", 1.906, 4.418, 0.734, 0.608);     // b = (3,4)  blue
eq("eq9_num", 2.986, 4.418, 6.208, 0.833);   // phi(a)^T phi(b) = ... = 9+64+48=121
eq("eq10_sq", 7.706, 5.528, 3.199, 0.390);   // [a^Tb]^2 = (1*3+2*4)^2 = 11^2 = 121
// Hollow red left-pointing annotation arrows (spec: color #D84343)
s.addShape(pres.shapes.LEFT_ARROW, {
  x: 10.946, y: 4.725, w: 0.587, h: 0.165,
  fill: { type: "none" }, line: { color: "D84343", width: 1.5 },
});
s.addShape(pres.shapes.LEFT_ARROW, {
  x: 10.946, y: 5.670, w: 0.587, h: 0.165,
  fill: { type: "none" }, line: { color: "D84343", width: 1.5 },
});

// Small grey diagonal pen/pointer stroke above-left of lower-right equation
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.520, y: 5.560, w: 0.30, h: 0.018,
  fill: { color: "8A8A8A" }, line: { type: "none" }, rotate: -38,
});

pres.writeFile({ fileName: NS + "/recreated_pptx/slide_026_recreated.pptx" })
  .then(() => console.log("wrote slide_026_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
