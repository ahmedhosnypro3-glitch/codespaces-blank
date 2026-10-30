// slide_038.js — "Training Vectors / Test Vectors (QP Formulation)"
// Upper: red-framed blocks of 2-D column vectors (training x1..x4 with y labels,
// test T1..T3). Lower: cyan band with the Minimize box (Lagrangian + 4x4 Q matrix)
// and the Subject-to box. Equations are 2D matplotlib-mathtext PNGs in build/eq_038/.
// Run: node slide_038.js

const pptxgen = require("pptxgenjs");
const { newPres, W, H, FONT } = require("./shared.js");

const NUM = 38;
const TITLE = "Training Vectors / Test Vectors (QP Formulation)";
const MATH = "Times New Roman";
const EQ = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_038/";
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_038_recreated.pptx";

const pres = newPres();
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule
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
  fontSize: 24, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
});

// 1. "Use C=1" pill (top-right, left of the badge): red border, pale-gray fill, blue C
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.35, y: 0.30, w: 1.95, h: 0.5,
  fill: { color: "F2F2F2" }, line: { color: "C00000", width: 1 },
});
s.addText([
  { text: "Use ", options: { color: "000000" } },
  { text: "C", options: { color: "0000CC", bold: true } },
  { text: "=1", options: { color: "000000" } },
], {
  x: 10.35, y: 0.30, w: 1.95, h: 0.5,
  align: "center", valign: "middle", fontSize: 15, fontFace: MATH, margin: 0,
});

// 2. Vector blocks: red-framed, red column headers, stacked 2-D vectors, y labels
function vecBlock(bx, bw, title, headers, vecs, yLabels) {
  s.addText(title, {
    x: bx, y: 0.92, w: bw, h: 0.32,
    align: "left", valign: "middle", fontSize: 17, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: bx, y: 1.28, w: bw, h: 1.95,
    fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
  });
  const colW = bw / vecs.length;
  headers.forEach((h, i) => {
    s.addText([
      { text: h, options: { color: "CC0000", italic: true } },
      { text: String(i + 1), options: { color: "CC0000", italic: true, subscript: true } },
    ], {
      x: bx + i * colW, y: 1.34, w: colW, h: 0.30,
      align: "center", valign: "middle", fontSize: 13, fontFace: MATH, margin: 0,
    });
  });
  vecs.forEach((v, i) => {
    s.addImage({ path: EQ + v.name, x: bx + i * colW + (colW - v.w) / 2, y: 1.70, w: v.w, h: v.h });
  });
  yLabels.forEach((t, i) => {
    s.addText([
      { text: "\u03b1", options: { color: "CC0000", italic: true } },
      { text: String(i + 1), options: { color: "CC0000", italic: true, subscript: true } },
      { text: " = " + t, options: { color: "CC0000" } },
    ], {
      x: bx + i * colW, y: 2.72, w: colW, h: 0.30,
      align: "center", valign: "middle", fontSize: 13, fontFace: MATH, margin: 0,
    });
  });
}

const TRAIN = [
  { name: "vec_x1.png", w: 0.685, h: 0.25333 },
  { name: "vec_x2.png", w: 0.69, h: 0.26 },
  { name: "vec_x3.png", w: 0.705, h: 0.28333 },
  { name: "vec_x4.png", w: 0.705, h: 0.28333 },
];
const TEST = [
  { name: "vec_T1.png", w: 0.71667, h: 0.26 },
  { name: "vec_T2.png", w: 0.73333, h: 0.285 },
  { name: "vec_T3.png", w: 0.71667, h: 0.26 },
];
vecBlock(0.6, 6.6, "Training Vectors", ["x", "x", "x", "x"], TRAIN, ["1", "1", "-1", "-1"]);
vecBlock(7.6, 4.8, "Test Vectors", ["T", "T", "T"], TEST, []);

// 3. Lower band (pale cyan) with two blue-bordered boxes
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 3.30, w: 12.13, h: 3.95,
  fill: { color: "E0F7F7" }, line: { type: "none" },
});

const MB = { x: 0.72, y: 3.40, w: 7.4, h: 3.80 };
s.addShape(pres.shapes.RECTANGLE, {
  x: MB.x, y: MB.y, w: MB.w, h: MB.h,
  fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
});
s.addText("Minimize:", {
  x: MB.x + 0.10, y: MB.y + 0.04, w: 2.2, h: 0.30,
  align: "left", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
s.addImage({ path: EQ + "eq_minimize.png", x: MB.x + 0.10, y: MB.y + 0.38, w: 6.57167, h: 0.83667 });
s.addText("= \u00bd [\u03b11 \u03b12 \u03b13 \u03b14] \u00b7 Q \u00b7 [\u03b11; \u03b12; \u03b13; \u03b14] \u2212 [\u03b11 + \u03b12 + \u03b13 + \u03b14]", {
  x: MB.x + 0.10, y: MB.y + 1.26, w: MB.w - 0.20, h: 0.30,
  align: "left", valign: "middle", fontSize: 12, color: "000000", fontFace: MATH, margin: 0,
});
s.addImage({ path: EQ + "q_matrix.png", x: MB.x + 0.35, y: MB.y + 1.62, w: 6.23833, h: 2.21 });

// 4. Subject-to box: 5 constraint lines (native subscripts, serif italic)
const SB = { x: 8.22, y: 3.40, w: 4.4, h: 3.80 };
s.addShape(pres.shapes.RECTANGLE, {
  x: SB.x, y: SB.y, w: SB.w, h: SB.h,
  fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1 },
});
s.addText("Subject to:", {
  x: SB.x + 0.10, y: SB.y + 0.04, w: 2.2, h: 0.30,
  align: "left", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

const M = { fontFace: MATH, color: "000000", italic: true, fontSize: 13 };
const a = () => ({ text: "\u03b1", options: M });
const sub = (n) => ({ text: String(n), options: { ...M, subscript: true } });
const sp = () => ({ text: " ", options: M });

s.addText([
  { text: "\u2212 [", options: M }, a(), sub(1), { text: " + ", options: M }, a(), sub(2),
  { text: " + ", options: M }, a(), sub(3), { text: " + ", options: M }, a(), sub(4),
  { text: "]", options: M },
], { x: SB.x + 0.10, y: SB.y + 0.42, w: SB.w - 0.20, h: 0.32, align: "left", valign: "middle", margin: 0 });

s.addImage({ path: EQ + "eq_constraint_sum.png", x: SB.x + 0.10, y: SB.y + 0.78, w: 1.38333, h: 0.42667 });

s.addText([
  a(), sub(1), { text: " + ", options: M }, a(), sub(2), { text: " \u2212 ", options: M },
  a(), sub(3), { text: " \u2212 ", options: M }, a(), sub(4), { text: " = 0", options: M },
], { x: SB.x + 0.10, y: SB.y + 1.26, w: SB.w - 0.20, h: 0.32, align: "left", valign: "middle", margin: 0 });

s.addText([
  { text: "\u03b1", options: M }, { text: "1", options: { ...M, subscript: true } },
  { text: " \u2264 1, ", options: M },
  { text: "\u03b1", options: M }, { text: "2", options: { ...M, subscript: true } },
  { text: " \u2264 1, ", options: M },
  { text: "\u03b1", options: M }, { text: "3", options: { ...M, subscript: true } },
  { text: " \u2264 1, ", options: M },
  { text: "\u03b1", options: M }, { text: "4", options: { ...M, subscript: true } },
  { text: " \u2264 1", options: M },
], { x: SB.x + 0.10, y: SB.y + 1.74, w: SB.w - 0.20, h: 0.32, align: "left", valign: "middle", margin: 0 });

s.addText([
  { text: "\u03b1", options: M }, { text: "i", options: { ...M, subscript: true } },
  { text: " \u2265 0", options: M },
  { text: "   (i = 1, 2, 3, 4)", options: M },
], { x: SB.x + 0.10, y: SB.y + 2.22, w: SB.w - 0.20, h: 0.32, align: "left", valign: "middle", margin: 0 });

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(err => console.error(err));
