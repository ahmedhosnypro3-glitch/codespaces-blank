// slide_006.js — fix pass for qa/rejudge2/slide_006_judge_a1_1.txt MAJORs:
// crisp Unicode text for inline inequalities / chips / convert box, arc-paren
// matrix images (fx_*), panel-2 chip moved inside the panel border.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx", "build", "eq_006") + "/";
const W = 13.33, H = 7.5, SANS = "Arial";
const RED = "C00000", LRED = "FF0000";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

const R = (text, o) => ({ text, options: Object.assign({ fontSize: 16, color: "000000", fontFace: SANS }, o) });
function T(x, y, w, h, runs, o) {
  s.addText(runs, Object.assign({ x, y, w, h, margin: 0, valign: "middle", fontFace: SANS }, o));
}
function imgC(name, cx, cy) {
  const j = JSON.parse(fs.readFileSync(EQ + "fx_" + name + ".json"));
  s.addImage({ path: EQ + "fx_" + name + ".png", x: cx - j.w_in / 2, y: cy - j.h_in / 2, w: j.w_in });
}
function panel(y0, y1) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.03 * W, y: y0 * H, w: 0.94 * W, h: (y1 - y0) * H,
    fill: { color: "FFFFFF" }, line: { color: "808080", width: 0.75 },
  });
}
function chip(x, y, w, h) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, fill: { color: "FFFDD0" }, line: { color: LRED, width: 1.25 },
  });
  T(x, y, w, h, [R("G x ≤ h", { bold: true, color: LRED, fontSize: 16 })], { align: "center" });
}
const sub = (i) => ["₁", "₂", "₃"][i - 1];
function ineq3(a, op, b, col, cc) {
  const r = [];
  [1, 2, 3].forEach((i) => {
    if (i > 1) r.push(R(" , ", { color: cc }));
    r.push(R(a + sub(i), { color: col }), R(op, { color: cc }), R(b + sub(i), { color: col }));
  });
  return r;
}
function chain3() {
  const r = [];
  [1, 2, 3].forEach((i) => {
    if (i > 1) r.push(R(" , ", { color: "000000" }));
    r.push(R("y" + sub(i), { color: "0000FF" }), R("≤", { color: "000000" }),
      R("x" + sub(i), { color: "0000FF" }), R("≤", { color: "000000" }),
      R("z" + sub(i), { color: "0000FF" }));
  });
  return r;
}
function conv() {
  const r = [];
  [1, 2, 3].forEach((i) => {
    if (i > 1) r.push(R(" , ", { color: "008000" }));
    r.push(R("-x" + sub(i), { color: "008000" }), R("≤", { color: "008000" }),
      R("-z" + sub(i), { color: "008000" }));
  });
  return r;
}
function arrow(cx, cy) { T(cx - 0.3, cy - 0.22, 0.6, 0.44, [R("⇒", { color: LRED, fontSize: 24 })], { align: "center" }); }
function leqMark(cx, cy) { T(cx - 0.2, cy - 0.2, 0.4, 0.4, [R("≤", { fontSize: 18 })], { align: "center" }); }

// House chrome (mandatory)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
T(12.48, 0.30, 0.5, 0.5, [R("6", { fontSize: 18, bold: true, color: "333333" })], { align: "center" });
T(0.6, 0.28, 12.13, 0.55, [R("Less Than Equal Constraints", { fontSize: 28, bold: true, color: RED })], { align: "center", valign: "top" });

panel(0.160, 0.340); panel(0.345, 0.575); panel(0.585, 0.875);
chip(0.672 * W, 0.246 * H, (0.790 - 0.672) * W, (0.285 - 0.246) * H);
chip(0.672 * W, 4.06, (0.790 - 0.672) * W, 0.24); // inside panel 2 (bottom edge 4.3125)
chip(0.675 * W, 0.700 * H, (0.790 - 0.675) * W, (0.740 - 0.700) * H);

T(0.063 * W, 1.30, 2.2, 0.28, [R("3 constraints", { bold: true, italic: true, color: LRED, fontSize: 14 })], { align: "left" });
T(0.063 * W, 4.46, 3.4, 0.28, [R("6 constraints , 3 variables", { bold: true, italic: true, color: LRED, fontSize: 14 })], { align: "left" });

// Panel 1: x_i <= z_i  =>  I [x] <= [z]
T(0.065 * W, 0.237 * H, (0.335 - 0.065) * W, (0.275 - 0.237) * H, ineq3("x", "≤", "z", "0000FF", "000000"), { align: "left" });
arrow(4.55, 1.875);
imgC("m3id", 5.30, 1.875);
imgC("vx3", 6.45, 1.875);
leqMark(7.05, 1.875);
imgC("vz3", 7.75, 1.875);

// Panel 2: x_i >= z_i  =>  -I [x] <= [-z]  + Convert box + chip
T(0.065 * W, 0.385 * H, (0.335 - 0.065) * W, (0.425 - 0.385) * H, ineq3("x", "≥", "z", "0000FF", "000000"), { align: "left" });
arrow(4.55, 3.45);
imgC("m3neg", 5.30, 3.45);
imgC("vx3", 6.45, 3.45);
leqMark(7.05, 3.45);
imgC("vnegz3", 7.80, 3.45);
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.674 * W, y: 0.375 * H, w: (0.902 - 0.674) * W, h: (0.535 - 0.375) * H,
  fill: { color: "FFFF99" }, line: { color: "808080", width: 0.75 },
});
T(0.674 * W, 2.86, (0.902 - 0.674) * W, 0.22, [R("Convert", { bold: true, italic: true, color: "FF8C00", fontSize: 11 })], { align: "center" });
T(0.674 * W, 3.12, (0.902 - 0.674) * W, 0.26, ineq3("x", "≥", "z", "008000", "008000"), { align: "center" });
T(0.674 * W, 3.42, (0.902 - 0.674) * W, 0.20, [R("to", { color: "008000", fontSize: 10 })], { align: "center" });
T(0.674 * W, 3.64, (0.902 - 0.674) * W, 0.30, conv(), { align: "center" });

// Panel 3: y_i <= x_i <= z_i  =>  6x3 [x] <= [-y; z]
T(0.065 * W, 0.665 * H, (0.335 - 0.065) * W, (0.705 - 0.665) * H, chain3(), { align: "left" });
arrow(4.55, 5.475);
imgC("m6", 5.30, 5.475);
T(4.90, 6.02, 0.80, 0.22, [R("6 x 3", { color: LRED, fontSize: 10 })], { align: "center" });
imgC("vx3", 6.45, 5.475);
leqMark(7.05, 5.475);
imgC("vyz6", 7.80, 5.475);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx", "slide_006_recreated.pptx") });
console.log("wrote slide_006_recreated.pptx");
