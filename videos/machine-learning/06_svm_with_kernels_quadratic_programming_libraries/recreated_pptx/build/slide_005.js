const pptxgen = require("pptxgenjs");
const fs = require("fs");

// Slide 005 — FRESH rebuild from qa/reanalysis2/slide_005_analysis.txt ONLY.
// No printed title; "Three Variables Example" label right side; top eq block,
// six coefficient definitions, bottom matrix->coef-boxes diagram.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_005.js

const NUM = 5;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = BASE + "/recreated_pptx/build/eq_005/";
const OUT = BASE + "/recreated_pptx/slide_005_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
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

const X = n => n * 13.33, Y = n => n * 7.5;
function img(name, x0n, y0n, maxwN, maxhN) {
  const m = JSON.parse(fs.readFileSync(EQ + name + ".png.json"));
  let w = m.w_in, h = m.h_in;
  if (w > X(maxwN)) { const k = X(maxwN) / w; w *= k; h *= k; }
  if (h > Y(maxhN)) { const k = Y(maxhN) / h; w *= k; h *= k; }
  s.addImage({ path: EQ + name + ".png", x: X(x0n), y: Y(y0n), w, h });
}
function txt(str, x0, y0, x1, y1, o) {
  s.addText(str, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    align: o.align || "left", valign: "middle",
    fontSize: o.fs || 14, bold: !!o.bold, italic: !!o.italic,
    color: o.color || "000000", fontFace: FONT, margin: 0,
  });
}
function box(x0, y0, x1, y1, fill, line, lw) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: { color: fill }, line: { color: line, width: lw || 1 },
  });
}

// top equation block
img("e1", 0.030, 0.080, 0.942, 0.135);
img("e2", 0.030, 0.225, 0.942, 0.060);
img("e3", 0.030, 0.295, 0.942, 0.055);
img("e4", 0.030, 0.360, 0.942, 0.050);

// six coefficient definitions (left column)
const dy = 0.385, step = 0.052;
["d1", "d2", "d3", "d4", "d5", "d6"].forEach((n, i) =>
  img(n, 0.035, dy + i * step, 0.570, 0.050));

// right annotation
txt("Three Variables Example", 0.742, 0.405, 0.980, 0.555,
    { fs: 16, italic: true, color: "000000", align: "right" });

// bottom diagram
img("hdr", 0.100, 0.700, 0.150, 0.030);
img("mat", 0.080, 0.745, 0.150, 0.170);
// blue highlight around top row cells, red around a22/a32 area
box(0.115, 0.755, 0.230, 0.795, "FFFFFF", "4472C4", 1.5);
box(0.125, 0.815, 0.185, 0.850, "FFFFFF", "C00000", 1.5);
box(0.125, 0.875, 0.185, 0.910, "FFFFFF", "C00000", 1.5);
// connector marks
s.addShape(pres.shapes.LINE, { x: X(0.250), y: Y(0.805), w: X(0.080), h: Y(0.035), line: { color: "000000", width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: X(0.315), y: Y(0.765), w: X(0.105), h: Y(0.040), line: { color: "000000", width: 1.5 } });
// right 3x3 coefficient grid
const bx = [[0.500, 0.640, 0.800], [0.640, 0.800, 0.965]];
const by = [0.745, 0.805, 0.865];
const names = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9"];
let k = 0;
for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
  const x0 = bx[0][c], x1 = bx[1][c], y0 = by[r], y1 = by[r] + 0.030;
  box(x0, y0, x1, y1, "FFFFFF", "C00000", 1);
  img(names[k], x0 + 0.004, y0 + 0.003, x1 - x0 - 0.008, y1 - y0 - 0.006);
  k++;
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
