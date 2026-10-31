// slide_007.js — "Equal Constraints" (rebuild wave 3)
// Built ONLY from qa/reanalysis2/slide_007_analysis.txt (spec starts at "1. SLIDE_TITLE").
// House chrome per video AGENTS.md overrides spec frame/badge/title.
// Math assets: 600-dpi mathtext PNGs in build/eq_007/ (gen_eq_007.py + manifest.json).
// Run: NODE_PATH=$(npm root -g) node slide_007.js

const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { newPres, W, H, FONT } = require("./shared.js");

const NUM = 7;
const TITLE = "Equal Constraints";
const MATH = "Times New Roman";
const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = BASE + "/recreated_pptx/build/eq_007/";
const OUT = BASE + "/recreated_pptx/slide_007_recreated.pptx";
const M = JSON.parse(fs.readFileSync(EQ + "manifest.json", "utf8"));

const pres = newPres();
const s = pres.addSlide();

// House chrome
s.background = { color: "E8E8E8" };
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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Helpers
const N = (v) => v * 13.33;          // normalized x -> in
const NY = (v) => v * 7.5;           // normalized y -> in
const box = (b) => ({ x: N(b[0]), y: NY(b[1]), w: N(b[2] - b[0]), h: NY(b[3] - b[1]) });
function img(name, b) {               // centered in normalized box, native px/600 size
  const m = M[name], r = box(b);
  s.addImage({ path: EQ + m.image, x: r.x + (r.w - m.w_in) / 2, y: r.y + (r.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
}
function imgAt(name, x, y) {
  const m = M[name];
  s.addImage({ path: EQ + m.image, x, y, w: m.w_in, h: m.h_in });
}
function panel(b) {
  const r = box(b);
  s.addShape(pres.shapes.RECTANGLE, { x: r.x, y: r.y, w: r.w, h: r.h, fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 } });
}
function label(text, b) {             // blue bold underlined header, h>=0.35
  const r = box(b), cy = r.y + r.h / 2;
  s.addText(text, {
    x: r.x, y: cy - 0.175, w: r.w, h: 0.35,
    align: "left", valign: "middle", fontSize: 12, bold: true, underline: true,
    color: "0000FF", fontFace: FONT, margin: 0,
  });
}
function chip(b) {                    // pink rounded "A x = b" chip
  const r = box(b), cy = r.y + r.h / 2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: r.x, y: r.y, w: r.w, h: r.h, fill: { color: "FFC7CE" }, line: { color: "FFC7CE", width: 0.5 } });
  s.addText("A x = b", {
    x: r.x, y: cy - 0.175, w: r.w, h: 0.35,
    align: "center", valign: "middle", fontSize: 13, bold: true, italic: true,
    color: "FF0000", fontFace: MATH, margin: 0,
  });
}
function matrix(rows, x, y, gap) {    // stacked colored rows + thin black bracket bars
  const wMax = Math.max(...rows.map((r) => M[r].w_in));
  const hTot = rows.reduce((a, r) => a + M[r].h_in, 0) + gap * (rows.length - 1);
  let ry = y;
  rows.forEach((r) => { imgAt(r, x + 0.03, ry); ry += M[r].h_in + gap; });
  s.addShape(pres.shapes.RECTANGLE, { x, y: y - 0.02, w: 0.025, h: hTot + 0.04, fill: { color: "000000" }, line: { color: "000000", width: 0.25 } });
  s.addShape(pres.shapes.RECTANGLE, { x: x + 0.03 + wMax + 0.005, y: y - 0.02, w: 0.025, h: hTot + 0.04, fill: { color: "000000" }, line: { color: "000000", width: 0.25 } });
  return { w: wMax + 0.06, h: hTot };
}

// Panels (spec section 3/4: white fill, red stroke)
panel([0.094, 0.176, 0.823, 0.319]);
panel([0.094, 0.339, 0.823, 0.620]);
panel([0.094, 0.639, 0.823, 0.824]);

// Panel 1: summation, red arrow, 1x3 * 3x1 = (z)_{1*1}, label, chip
img("sum1", [0.101, 0.190, 0.368, 0.283]);
img("arrow", [0.405, 0.219, 0.424, 0.248]);
{
  const r = box([0.435, 0.181, 0.625, 0.294]), cy = r.y + r.h / 2, gap = 0.04;
  let x = r.x + (r.w - (M.p1_row.w_in + gap + M.vec_x.w_in + gap + M.p1_rhs.w_in)) / 2;
  const y1 = cy - M.p1_row.h_in / 2; imgAt("p1_row", x, y1); x += M.p1_row.w_in + gap;
  const y2 = cy - M.vec_x.h_in / 2; imgAt("vec_x", x, y2); x += M.vec_x.w_in + gap;
  const y3 = cy - M.p1_rhs.h_in / 2; imgAt("p1_rhs", x, y3);
  imgAt("ann_1x1", x + M.p1_rhs.w_in - M.ann_1x1.w_in + 0.03, y3 + M.p1_rhs.h_in - M.ann_1x1.h_in * 0.7);
}
label("One Constraint", [0.692, 0.183, 0.803, 0.209]);
chip([0.729, 0.222, 0.803, 0.263]);

// Panel 2: three summations, red arrow, 3x3 * 3x1 = Z^{3*1}, label, chip
img("sum_a", [0.101, 0.357, 0.172, 0.415]);
img("sum_b", [0.101, 0.439, 0.172, 0.502]);
img("sum_c", [0.101, 0.528, 0.172, 0.593]);
img("arrow", [0.234, 0.444, 0.253, 0.474]);
{
  const r = box([0.269, 0.398, 0.487, 0.528]), cy = r.y + r.h / 2, gap = 0.05;
  const mat = matrix(["r_a3", "r_b3", "r_c3"], 0, 0, 0.04);
  let x = r.x + (r.w - (mat.w + gap + M.vec_x.w_in + gap + M.eq_sign.w_in + gap + M.z_vec3.w_in)) / 2;
  const mat2 = matrix(["r_a3", "r_b3", "r_c3"], x, cy - mat.h / 2, 0.04);
  x += mat2.w + gap;
  imgAt("vec_x", x, cy - M.vec_x.h_in / 2); x += M.vec_x.w_in + gap;
  imgAt("eq_sign", x, cy - M.eq_sign.h_in / 2); x += M.eq_sign.w_in + gap;
  imgAt("z_vec3", x, cy - M.z_vec3.h_in / 2);
  imgAt("ann_3x1", x + M.z_vec3.w_in - M.ann_3x1.w_in + 0.04, cy - mat.h / 2 - 0.02);
}
label("Three Constraints", [0.678, 0.387, 0.810, 0.413]);
chip([0.729, 0.446, 0.803, 0.487]);

// Panel 3: four red equations, red arrow, 4x3 * 3x1 = 4x1, label, chip
img("e1", [0.116, 0.648, 0.207, 0.678]);
img("e2", [0.113, 0.687, 0.211, 0.717]);
img("e3", [0.113, 0.726, 0.211, 0.757]);
img("e4", [0.109, 0.767, 0.211, 0.809]);
img("arrow", [0.254, 0.702, 0.273, 0.732]);
{
  const r = box([0.296, 0.644, 0.512, 0.791]), cy = r.y + r.h / 2, gap = 0.05;
  const mat = matrix(["n1", "n2", "n3", "n4"], 0, 0, 0.02);
  let x = r.x + (r.w - (mat.w + gap + M.vec_x.w_in + gap + M.eq_sign.w_in + gap + M.rhs_vec4.w_in)) / 2;
  matrix(["n1", "n2", "n3", "n4"], x, cy - mat.h / 2, 0.02);
  imgAt("ann_4x3", x + mat.w - M.ann_4x3.w_in + 0.04, cy - mat.h / 2 - 0.02);
  x += mat.w + gap;
  imgAt("vec_x", x, cy - M.vec_x.h_in / 2); x += M.vec_x.w_in + gap;
  imgAt("eq_sign", x, cy - M.eq_sign.h_in / 2); x += M.eq_sign.w_in + gap;
  imgAt("rhs_vec4", x, cy - M.rhs_vec4.h_in / 2);
  imgAt("ann_4x1", x + M.rhs_vec4.w_in - M.ann_4x1.w_in + 0.04, cy - mat.h / 2 - 0.02);
}
label("Four Constraints", [0.685, 0.665, 0.813, 0.691]);
chip([0.729, 0.709, 0.803, 0.750]);

// Small grey pen/pointer graphic (spec: ISOSCELES_TRIANGLE, greys)
{
  const r = box([0.536, 0.637, 0.558, 0.678]);
  s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
    x: r.x, y: r.y, w: r.w, h: r.h, rotate: 40,
    fill: { color: "D9D9D9" }, line: { color: "808080", width: 1 },
  });
}

// Solid black rectangle, lower-right outside frame area
{
  const r = box([0.823, 0.861, 1.000, 1.000]);
  s.addShape(pres.shapes.RECTANGLE, { x: r.x, y: r.y, w: r.w, h: r.h, fill: { color: "000000" }, line: { color: "000000", width: 0.25 } });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
