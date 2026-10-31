// slide_026.js — FRESH rebuild from qa/reanalysis2/slide_026_analysis.txt (REBUILD WAVE 3).
// Spec coords [x0,y0,x1,y1] normalized -> inches: x*13.33, y*7.5, w=(x1-x0)*13.33, h=(y1-y0)*7.5.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_026.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_026") + "/";
const man = JSON.parse(fs.readFileSync(EQ + "manifest.json", "utf8"));
const W = 13.33, H = 7.5;
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome (mandatory, overrides spec): red frame, badge, title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
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
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Content panels (spec LAYOUT): rounded rects with blue border
function panel(x, y, w, h, fill) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: fill }, line: { color: "3A4FC0", width: 1.5 }, adj: 0.05,
  });
}
panel(0.866, 1.058, 10.771, 3.263, "FDF6E3"); // upper cream panel  [0.065,0.141,0.873,0.576]
panel(0.866, 4.350, 10.771, 1.973, "FFFFFF"); // lower white panel  [0.065,0.580,0.873,0.843]

// Peach highlights behind the squared inner-product terms
function hl(x, y, w, h) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: "FBE2D3" }, line: { color: "E8A87C", width: 0.75 }, adj: 0.25,
  });
}
hl(0.946, 2.018, 0.667, 0.510); // behind (a^T b)^2, upper line 2  [0.071,0.269,0.121,0.337]
hl(0.946, 3.165, 0.627, 0.503); // behind [a^T b]^2, upper line 3  [0.071,0.422,0.118,0.489]
hl(7.706, 5.580, 0.627, 0.293); // behind [a^T b]^2, lower line 2  [0.578,0.744,0.625,0.783]
// Equation PNGs (600 dpi mathtext): exact size w = px/600 in, vertically centered in spec box
function eq(name, x, y, w, h) {
  const m = man[name];
  s.addImage({ path: EQ + m.file, x, y: y + Math.max(0, (h - m.h_in) / 2), w: m.w_in, h: m.h_in });
}
eq("eq1_a",     1.000, 1.223, 0.693, 0.525); // a = (a1,a2)^T red            [0.075,0.163,0.127,0.233]
eq("eq2_b",     1.906, 1.223, 0.693, 0.525); // b = (b1,b2)^T blue           [0.143,0.163,0.195,0.233]
eq("eq3_chain", 0.946, 1.988, 6.758, 0.585); // (a^Tb)^2 = ... chain         [0.071,0.265,0.578,0.343]
eq("eq4_phi",   0.946, 2.850, 4.773, 1.148); // [a^Tb]^2 = (phi|phi) = phi(a)^Tphi(b)  [0.071,0.380,0.429,0.533]
eq("eq5_where", 7.079, 2.850, 3.679, 1.178); // Where: phi(x) = ... => ...   [0.531,0.380,0.807,0.537]
eq("eq6_cap",   8.958, 3.945, 1.173, 0.248); // 2D => 3D red caption         [0.672,0.526,0.760,0.559]
eq("eq7_a",     0.946, 4.418, 0.746, 0.608); // a = (1,2)^T red              [0.071,0.589,0.127,0.670]
eq("eq8_b",     1.906, 4.418, 0.733, 0.608); // b = (3,4) blue               [0.143,0.589,0.198,0.670]
eq("eq9_num",   2.986, 4.418, 6.212, 0.833); // phi(a)^Tphi(b) = ... = 9+64+48=121  [0.224,0.589,0.690,0.700]
eq("eq10_sq",   7.706, 5.528, 3.199, 0.390); // [a^Tb]^2 = (1*3+2*4)^2 = 11^2 = 121  [0.578,0.737,0.818,0.789]

// Hollow red left-pointing annotation arrows (spec color #D84343)
s.addShape(pres.shapes.LEFT_ARROW, {
  x: 10.946, y: 4.725, w: 0.587, h: 0.165,
  fill: { type: "none" }, line: { color: "D84343", width: 1.5 },
});
s.addShape(pres.shapes.LEFT_ARROW, {
  x: 10.946, y: 5.670, w: 0.587, h: 0.165,
  fill: { type: "none" }, line: { color: "D84343", width: 1.5 },
});

// Small grey diagonal pen/pointer stroke above-left of lower-right equation [0.783,0.726,0.808,0.778]
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.520, y: 5.795, w: 0.30, h: 0.018,
  fill: { color: "8A8A8A" }, line: { type: "none" }, rotate: -38,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_026_recreated.pptx") })
  .then(() => console.log("wrote slide_026_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
