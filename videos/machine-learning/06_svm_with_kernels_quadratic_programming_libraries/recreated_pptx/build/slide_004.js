const pptxgen = require("pptxgenjs");
const fs = require("fs");

// Slide 004 — FRESH rebuild from qa/reanalysis2/slide_004_analysis.txt ONLY.
// "Quadratic Coefficients" — 3 red-bordered panels: derivation eqs, coefficient
// readings, operator diagram. House chrome mandatory.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_004.js

const NUM = 4;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = BASE + "/recreated_pptx/build/eq_004/";
const OUT = BASE + "/recreated_pptx/slide_004_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome ----
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
s.addText("Quadratic Coefficients", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

const X = n => n * 13.33, Y = n => n * 7.5;
function panel(x0, y0, x1, y1) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: { type: "none" }, line: { color: "C00000", width: 1.25 },
  });
}
function img(name, x0n, y0n, maxwN, maxhN) {
  const m = JSON.parse(fs.readFileSync(EQ + name + ".png.json"));
  let w = m.w_in, h = m.h_in;
  if (w > X(maxwN)) { const k = X(maxwN) / w; w *= k; h *= k; }
  if (h > Y(maxhN)) { const k = Y(maxhN) / h; w *= k; h *= k; }
  s.addImage({ path: EQ + name + ".png", x: X(x0n), y: Y(y0n), w, h });
  return m;
}
function txt(str, x0, y0, x1, y1, o) {
  s.addText(str, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    align: o.align || "left", valign: "middle",
    fontSize: o.fs || 14, bold: !!o.bold, italic: !!o.italic,
    underline: !!o.under, color: o.color || "000000",
    fontFace: FONT, margin: 0,
  });
}

// sub-heading
txt("Two Variables Example", 0.078, 0.247, 0.246, 0.293,
    { fs: 15, italic: true, under: true, color: "8B0000" });

// panel 1: derivation
panel(0.045, 0.325, 0.955, 0.550);
img("eq1", 0.075, 0.332, 0.875, 0.070);
img("eq2", 0.085, 0.406, 0.865, 0.046);
img("eq3", 0.085, 0.458, 0.605, 0.054);

// panel 2: coefficient readings
panel(0.060, 0.618, 0.960, 0.795);
img("c1", 0.075, 0.628, 0.525, 0.048);
img("c2a", 0.075, 0.688, 0.855, 0.052);
img("c2b", 0.560, 0.688, 0.370, 0.052);
img("c3", 0.075, 0.748, 0.525, 0.046);

// panel 3: operator diagram
panel(0.060, 0.826, 0.960, 0.925);
img("dmat", 0.108, 0.845, 0.140, 0.073);
txt("x_1   x_2", 0.115, 0.828, 0.240, 0.845, { fs: 11, color: "0000CC" });
img("r1", 0.080, 0.852, 0.025, 0.030);
img("r2", 0.080, 0.885, 0.027, 0.030);
img("darrow", 0.262, 0.868, 0.053, 0.020);
function pink(name, x0, y0, x1, y1) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: { color: "FFE6E6" }, line: { color: "C00000", width: 0.75 },
  });
  img(name, x0 + 0.005, y0 + 0.004, x1 - x0 - 0.01, y1 - y0 - 0.008);
}
pink("bx1", 0.330, 0.838, 0.560, 0.870);
pink("bx2", 0.570, 0.838, 0.800, 0.870);
pink("bx3", 0.330, 0.883, 0.560, 0.915);
pink("bx4", 0.570, 0.883, 0.800, 0.915);

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
