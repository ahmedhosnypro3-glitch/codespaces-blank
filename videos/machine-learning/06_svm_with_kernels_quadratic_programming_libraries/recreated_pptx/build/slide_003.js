const pptxgen = require("pptxgenjs");
const fs = require("fs");

// Slide 003 — FRESH rebuild from qa/reanalysis2/slide_003_analysis.txt ONLY.
// "Input to Quadratic Equation Solver" — 3 red-bordered panels. House chrome mandatory.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_003.js

const NUM = 3;
const FONT = "Arial";
const SERIF = "Times New Roman";
const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = BASE + "/recreated_pptx/build/eq_003/";
const OUT = BASE + "/recreated_pptx/slide_003_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (overrides spec) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
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
s.addText("Input to Quadratic Equation Solver", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

const X = n => n * 13.33, Y = n => n * 7.5;
function panel(x0, y0, x1, y1) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: { color: "FFFFFF" }, line: { color: "CC0000", width: 1.25 },
  });
}
function txt(str, x0, y0, x1, y1, o) {
  s.addText(str, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    align: o.align || "left", valign: "middle",
    fontSize: o.fs || 12, bold: !!o.bold, italic: !!o.italic,
    color: o.color || "000000", fontFace: o.font || FONT, margin: 0,
  });
}
function runs(arr, x0, y0, x1, y1) {
  s.addText(arr, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    align: "left", valign: "middle", margin: 0,
  });
}
function img(name, x0n, y0n, y1n) {
  const m = JSON.parse(fs.readFileSync(EQ + name + ".json"));
  s.addImage({ path: EQ + name + ".png", x: X(x0n),
    y: Y(y0n) + (Y(y1n - y0n) - m.h_in) / 2, w: m.w_in, h: m.h_in });
}
const vr = (t, c, o) => ({ text: t, options: Object.assign(
  { fontFace: FONT, fontSize: 11, bold: true, color: c }, o || {}) });
const serif = (t, o) => ({ text: t, options: Object.assign(
  { fontFace: SERIF, fontSize: 11, italic: true, color: "000000" }, o || {}) });
function defline(vruns, desc, size, x0, y0, x1, y1) {
  const tail = [serif(" " + desc + " ")];
  if (size) tail.push(serif(size, { color: "CC0000" }));
  tail.push(serif(" ,"));
  runs(vruns.concat(tail), x0, y0, x1, y1);
}
// ---- panel 1: objective ----
panel(0.069, 0.185, 0.830, 0.394);
txt("Put quadratic equation in the form:", 0.088, 0.196, 0.335, 0.229,
    { fs: 12, bold: true, italic: true, color: "C00000" });
img("eq_obj", 0.082, 0.259, 0.356);
txt("where:", 0.349, 0.283, 0.395, 0.319, { fs: 11, bold: true });
defline([vr("X", "0000FF")], "is a Vector of size", "d*1", 0.414, 0.2540, 0.622, 0.2904);
defline([vr("P", "FF0000")], "is a Matrix of size", "d*d", 0.414, 0.2904, 0.622, 0.3267);
defline([vr("q", "FF0000"), vr("T", "FF0000", { superscript: true })],
        "is a Vector of size", "1*d", 0.414, 0.3267, 0.622, 0.3630);
txt("?", 0.689, 0.244, 0.730, 0.333, { fs: 40, bold: true, color: "C00000", align: "center" });

// ---- panel 2: inequality constraints ----
panel(0.069, 0.420, 0.830, 0.617);
txt("Put all ≤ , ≥ constraints in the form:", 0.081, 0.433, 0.335, 0.469,
    { fs: 12, bold: true, color: "C00000" });
defline([vr("m", "008000")], "is Number of constraints", "", 0.294, 0.476, 0.620, 0.505);
img("eq_gxleh", 0.081, 0.515, 0.557);
txt("where:", 0.228, 0.524, 0.275, 0.557, { fs: 11, bold: true });
defline([vr("X", "0000FF")], "is a Vector of size", "d*1", 0.294, 0.5090, 0.492, 0.5413);
defline([vr("G", "FF0000")], "is a Matrix of size", "m*d", 0.294, 0.5413, 0.492, 0.5737);
defline([vr("h", "0000FF")], "is a Vector of size", "m*1", 0.294, 0.5737, 0.492, 0.6060);

// ---- panel 3: equality constraints ----
panel(0.069, 0.641, 0.830, 0.859);
runs([
  { text: "Put all ", options: { fontFace: FONT, fontSize: 12, bold: true, color: "C00000" } },
  { text: 'Equal "="', options: { fontFace: FONT, fontSize: 12, bold: true, italic: true, color: "0000FF" } },
  { text: " constraints in the form:", options: { fontFace: FONT, fontSize: 12, bold: true, color: "C00000" } },
], 0.081, 0.654, 0.335, 0.691);
defline([vr("m", "008000")], "is Number of constraints", "", 0.294, 0.696, 0.620, 0.726);
img("eq_axeqb", 0.081, 0.730, 0.774);
txt("where:", 0.222, 0.739, 0.271, 0.772, { fs: 11, bold: true });
defline([vr("X", "0000FF")], "is a Vector of size", "d*1", 0.294, 0.7260, 0.492, 0.7587);
defline([vr("A", "FF0000")], "is a Matrix of size", "m*d", 0.294, 0.7587, 0.492, 0.7913);
defline([vr("b", "0000FF", { italic: true })], "is a Vector of size", "m*1", 0.294, 0.7913, 0.492, 0.8240);

// ---- solid black capture band across the bottom ----
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.040), y: Y(0.913), w: X(0.920), h: Y(0.087),
  fill: { color: "000000" }, line: { type: "none" },
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
