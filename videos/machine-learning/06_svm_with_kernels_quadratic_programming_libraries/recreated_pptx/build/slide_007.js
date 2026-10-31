// slide_007.js — wave-3 rebuild round 2 from qa/reanalysis2/slide_007_analysis.txt ONLY.
// rb4 math assets: true stacked 2-D vectors/matrices (row PNGs + drawn brackets),
// panel-3 block sized to fit its panel, en-dash in equation 3.
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx", "build", "eq_007");
const MAN = require(path.join(EQ, "rb4_manifest.json"));

const W = 13.33, H = 7.5;
const X = (v) => v * W, Y = (v) => v * H;
const box = (b) => ({ x: X(b[0]), y: Y(b[1]), w: X(b[2] - b[0]), h: Y(b[3] - b[1]) });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
slide.background = { color: "E8E8E8" };

// Solid black rectangle, lower-right corner (spec; under house frame)
let b = box([0.823, 0.861, 1.0, 1.0]);
slide.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "000000" }, line: { type: "none" } });

// House chrome (mandatory, overrides spec)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
slide.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
slide.addText("7", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
slide.addText("Equal Constraints", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: "Arial", margin: 0,
});

// Three red-outlined white panels
for (const p of [
  [0.094, 0.176, 0.823, 0.319],
  [0.094, 0.339, 0.823, 0.620],
  [0.094, 0.639, 0.823, 0.824],
]) {
  b = box(p);
  slide.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 } });
}

// Math helpers
function img(name, x, y) {
  const m = MAN[name];
  slide.addImage({ path: path.join(EQ, m.image), x, y, w: m.w_in, h: m.h_in });
  return m;
}
function eqC(name, bb) {
  const m = MAN[name];
  img(name, bb.x + (bb.w - m.w_in) / 2, bb.y + (bb.h - m.h_in) / 2);
}
function plain(name, x, cy) {
  const m = MAN[name];
  img(name, x, cy - m.h_in / 2);
  return m.w_in;
}
function brackets(x0, x1, y0, y1) {
  slide.addShape(pres.shapes.RECTANGLE, { x: x0, y: y0, w: 0.022, h: y1 - y0, fill: { color: "000000" }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: x1 - 0.022, y: y0, w: 0.022, h: y1 - y0, fill: { color: "000000" }, line: { type: "none" } });
}
// Stack row PNGs as a true 2-D block centered in [x, x+w] around cy; draw brackets.
function stack(names, x, w, cy, gap) {
  const hs = names.map((n) => MAN[n].h_in);
  const total = hs.reduce((a, c) => a + c, 0) + gap * (names.length - 1);
  const wMax = Math.max(...names.map((n) => MAN[n].w_in));
  const x0 = x + (w - wMax) / 2;
  let y = cy - total / 2;
  const y0 = y;
  for (const n of names) { img(n, x0, y); y += MAN[n].h_in + gap; }
  brackets(x0 - 0.045, x0 + wMax + 0.045, y0 - 0.015, y - gap + 0.015);
  return { x0, w: wMax, y0, y1: y - gap };
}
// Section labels (blue, bold, underlined) and pink "A x = b" chips
for (const [w1, w2, bb0] of [
  ["One", "Constraint", [0.692, 0.183, 0.803, 0.209]],
  ["Three", "Constraints", [0.678, 0.387, 0.810, 0.413]],
  ["Four", "Constraints", [0.685, 0.665, 0.813, 0.691]],
]) {
  b = box(bb0);
  slide.addText([
    { text: w1 + " ", options: { fontSize: 12, bold: true, underline: true, color: "0000FF", fontFace: "Arial" } },
    { text: w2, options: { fontSize: 12, bold: true, underline: true, color: "FF0000", fontFace: "Arial" } },
  ], {
    x: b.x, y: b.y, w: b.w, h: b.h,
    align: "left", valign: "middle", margin: 0,
  });
}
for (const c of [
  [0.729, 0.222, 0.803, 0.263],
  [0.729, 0.446, 0.803, 0.487],
  [0.729, 0.709, 0.803, 0.750],
]) {
  b = box(c);
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFC7CE" }, line: { type: "none" } });
  slide.addText("A x = b", {
    x: b.x, y: b.y, w: b.w, h: b.h,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, italic: true, color: "FF0000", fontFace: "Times New Roman", margin: 0,
  });
}

// Panel 1: summation, red arrow, [a1 a2 a3][x1;x2;x3] = (z)_{1*1}
eqC("rb4_sum1", box([0.101, 0.190, 0.368, 0.283]));
eqC("rb4_arrow", box([0.405, 0.219, 0.424, 0.248]));
b = box([0.435, 0.181, 0.625, 0.294]);
let cy = b.y + b.h / 2;
let cx = b.x + 0.03;
cx += plain("rb4_p1_rowA", cx, cy) + 0.07;
let v = stack(["rb4_x1", "rb4_x2", "rb4_x3"], cx, 0.34, cy, 0.03);
cx = v.x0 + v.w + 0.10;
plain("rb4_p1_rhs", cx, cy);

// Panel 2: three summations, arrow, 3x3 matrix * x-vector = Z-vector with 3*1
eqC("rb4_sum_a", box([0.101, 0.357, 0.172, 0.415]));
eqC("rb4_sum_b", box([0.101, 0.439, 0.172, 0.502]));
eqC("rb4_sum_c", box([0.101, 0.528, 0.172, 0.593]));
eqC("rb4_arrow", box([0.234, 0.444, 0.253, 0.474]));
b = box([0.269, 0.398, 0.487, 0.528]);
cy = b.y + b.h / 2;
cx = b.x + 0.02;
let m = stack(["rb4_r_a", "rb4_r_b", "rb4_r_c"], cx, 0.95, cy, 0.05);
cx = m.x0 + m.w + 0.10;
v = stack(["rb4_x1", "rb4_x2", "rb4_x3"], cx, 0.34, cy, 0.03);
cx = v.x0 + v.w + 0.08;
cx += plain("rb4_eq", cx, cy) + 0.06;
let r = stack(["rb4_Z1", "rb4_Z2", "rb4_Z3"], cx, 0.34, cy, 0.03);
img("rb4_ann31", r.x0 + r.w + 0.02, r.y0 - 0.02);

// Panel 3: four red equations, arrow, 4x3 matrix (4*3) * x-vector = (7;12;10;24) (4*1)
eqC("rb4_p3_left", box([0.109, 0.648, 0.210, 0.809]));
eqC("rb4_arrow", box([0.254, 0.702, 0.273, 0.732]));
b = box([0.296, 0.644, 0.512, 0.791]);
cy = b.y + b.h / 2;
cx = b.x + 0.02;
m = stack(["rb4_n1", "rb4_n2", "rb4_n3", "rb4_n4"], cx, 0.95, cy, 0.035);
img("rb4_ann43", m.x0 + m.w + 0.03, m.y0 - 0.02);
cx = m.x0 + m.w + 0.16;
v = stack(["rb4_x1", "rb4_x2", "rb4_x3"], cx, 0.34, cy, 0.03);
cx = v.x0 + v.w + 0.08;
cx += plain("rb4_eq", cx, cy) + 0.06;
r = stack(["rb4_v7", "rb4_v12", "rb4_v10", "rb4_v24"], cx, 0.34, cy, 0.03);
img("rb4_ann41", r.x0 + r.w + 0.02, r.y0 - 0.02);

// Small grey pen/pointer graphic (tilted pen)
b = box([0.536, 0.637, 0.558, 0.678]);
slide.addShape(pres.shapes.RECTANGLE, {
  x: b.x + b.w * 0.3, y: b.y, w: b.w * 0.24, h: b.h * 0.7,
  fill: { color: "808080" }, line: { color: "000000", width: 0.5 }, rotate: 38,
});
slide.addShape(pres.shapes.RIGHT_TRIANGLE, {
  x: b.x + b.w * 0.58, y: b.y + b.h * 0.58, w: b.w * 0.34, h: b.h * 0.42,
  fill: { color: "D9D9D9" }, line: { color: "000000", width: 0.5 }, rotate: 38,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_007_recreated.pptx") });
