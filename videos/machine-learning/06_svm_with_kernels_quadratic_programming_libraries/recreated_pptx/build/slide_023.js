// slide_023.js — FRESH rebuild (wave 3) from qa/reanalysis2/slide_023_analysis.txt ONLY.
// "Radial Basis Function (RBF) Kernel". House chrome per video AGENTS.md (overrides spec
// frame/badge/title). Normalized spec coords [x0,y0,x1,y1] -> inches x*13.33 / y*7.5.
// Math assets: eq_023/*.png (gen_eq_023_rb3.py, 600 dpi mathtext, exact-size addImage).
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_023.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const NUM = 23;
const TITLE = "Radial Basis Function (RBF) Kernel";
const W = 13.33, H = 7.5;
const SERIF = "Times New Roman";
const SANS = "Arial";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQDIR = path.join(NS, "recreated_pptx/build/eq_023");
const OUT = path.join(NS, "recreated_pptx/slide_023_recreated.pptx");
const manifest = JSON.parse(fs.readFileSync(path.join(EQDIR, "manifest.json"), "utf8"));

const X = v => v * 13.33, Y = v => v * 7.5;
const N = r => ({ x: X(r[0]), y: Y(r[1]), w: (r[2] - r[0]) * 13.33, h: (r[3] - r[1]) * 7.5 });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

function rect(r, fill, lineColor, lineW, round, dash) {
  const o = Object.assign(N(r), {
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: lineColor, width: lineW },
  });
  if (dash) o.line.dashType = dash;
  s.addShape(round ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, o);
}
// hollow right arrow: white shaft + open triangular head, red outline
function arrow(r, color) {
  const b = N(r);
  const headW = Math.min(0.22, b.w * 0.42);
  const shaftH = Math.max(0.03, b.h * 0.26);
  s.addShape(pres.shapes.RECTANGLE, {
    x: b.x, y: b.y + b.h / 2 - shaftH / 2, w: b.w - headW, h: shaftH,
    fill: { color: "FFFFFF" }, line: { color, width: 1.25 },
  });
  s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
    x: b.x + b.w - headW, y: b.y, w: headW, h: b.h, rotate: 90,
    fill: { color: "FFFFFF" }, line: { color, width: 1.25 },
  });
}
function txt(r, runs, o) {
  const b = N(r);
  s.addText(runs, Object.assign({}, b, {
    align: o.align || "center", valign: "middle",
    fontSize: o.size, bold: !!o.bold, italic: !!o.italic,
    color: o.color || "000000", fontFace: o.font || SERIF, margin: 0,
  }));
}
// math PNG at exact size (w_in = px/600), centered inside its spec box
function eq(name, r) {
  const b = N(r), m = manifest[name];
  s.addImage({
    path: m.path,
    x: b.x + (b.w - m.w_in) / 2, y: b.y + (b.h - m.h_in) / 2,
    w: m.w_in, h: m.h_in,
  });
}

// ---- house chrome (mandatory; overrides spec frame/badge/title) ----
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
  fontSize: 18, bold: true, color: "333333", fontFace: SANS, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 22, bold: true, color: "C00000", fontFace: SERIF, margin: 0,
});

// ---- top band (spec): Example-3 chip, bracketed RBF equation ----
rect([0.065, 0.081, 0.177, 0.150], "FFFFFF", "0000CC", 1.25, true, "dash");
txt([0.065, 0.092, 0.169, 0.137], "Example-3",
    { size: 12, bold: true, italic: true, color: "0000CC", font: SANS, align: "center" });
eq("top_rbf", [0.645, 0.078, 0.777, 0.135]);

// ---- upper-middle band (spec): input matrix, long arrow, Normal Model panel ----
rect([0.076, 0.226, 0.165, 0.335], "FFFFFF", "BFBFBF", 1);
eq("mat_ab", [0.080, 0.241, 0.155, 0.319]);
arrow([0.167, 0.254, 0.500, 0.298], "C00000");
rect([0.507, 0.154, 0.823, 0.407], "FFFFFF", "0000CC", 1.5);
txt([0.618, 0.196, 0.713, 0.228], "Normal Model",
    { size: 13, bold: true, italic: true, color: "C00000" });
eq("calc_atb", [0.619, 0.235, 0.708, 0.270]);
rect([0.620, 0.280, 0.688, 0.372], "E9F6FB", "6FA8C9", 1, true);
eq("mat_normal", [0.622, 0.291, 0.683, 0.361]);
arrow([0.822, 0.276, 0.854, 0.313], "C00000");

// ---- mid banner (spec): blue strip, "infinite" in red ----
rect([0.069, 0.393, 0.502, 0.448], "FFFFFF", "0000CC", 1);
txt([0.080, 0.404, 0.491, 0.437], [
  { text: "Map Input data from 2-D to ", options: { color: "0000CC", bold: true, italic: true, fontSize: 13, fontFace: SERIF } },
  { text: "infinite", options: { color: "C00000", bold: true, italic: true, fontSize: 13, fontFace: SERIF } },
  { text: " Dimension", options: { color: "0000CC", bold: true, italic: true, fontSize: 13, fontFace: SERIF } },
], { align: "left" });

// ---- lower half (spec): grey eq box, lower input matrix, mapping block ----
rect([0.214, 0.489, 0.345, 0.570], "F2F2F2", "808080", 1, true);
eq("eq_rbf", [0.235, 0.500, 0.340, 0.557]);
rect([0.076, 0.576, 0.165, 0.685], "FFFFFF", "BFBFBF", 1);
eq("mat_ab", [0.080, 0.590, 0.155, 0.668]);
rect([0.206, 0.580, 0.349, 0.680], "FDE7E7", "C00000", 1.5);
txt([0.224, 0.591, 0.322, 0.617], "Vectors Mapping",
    { size: 12, bold: true, color: "C00000", align: "center" });
eq("vec_map", [0.224, 0.617, 0.331, 0.657]);
// magenta complexity box (left)
rect([0.217, 0.691, 0.339, 0.780], "FF00FF", "FF00FF", 0);
txt([0.238, 0.694, 0.320, 0.770], "Higher\nComputational\nComplexity !!!",
    { size: 11, bold: true, italic: true, color: "0000FF" });
// pink two-column vector box
rect([0.385, 0.500, 0.471, 0.759], "FCE9F7", "E86FC6", 1);
eq("vec_pink", [0.395, 0.531, 0.450, 0.744]);
arrow([0.352, 0.607, 0.383, 0.652], "C00000");
arrow([0.474, 0.607, 0.510, 0.652], "C00000");
// tiny black diagonal arrow [?]
s.addShape(pres.shapes.RIGHT_ARROW, Object.assign(N([0.501, 0.583, 0.516, 0.613]), {
  fill: { color: "000000" }, line: { color: "000000", width: 0 }, rotate: -45,
}));

// ---- Kernelized Model panel (spec) ----
rect([0.507, 0.444, 0.797, 0.809], "FFFFFF", "70AD47", 1.5);
txt([0.583, 0.463, 0.721, 0.496], [
  { text: "Kernelized", options: { color: "C00000", bold: true, italic: true, fontSize: 13, fontFace: SERIF } },
  { text: " Model", options: { color: "000000", italic: true, fontSize: 13, fontFace: SERIF } },
], {});
eq("calc_utv", [0.629, 0.500, 0.719, 0.535]);
rect([0.555, 0.546, 0.764, 0.802], "EEF6EA", "70AD47", 1, true);
eq("mat_kernel", [0.570, 0.572, 0.755, 0.778]);
// magenta complexity box (right)
rect([0.568, 0.689, 0.691, 0.780], "FF00FF", "FF00FF", 0);
txt([0.600, 0.694, 0.683, 0.770], "Higher\nComputational\nComplexity !!!",
    { size: 11, bold: true, italic: true, color: "0000FF" });
arrow([0.822, 0.607, 0.854, 0.644], "C00000");

// ---- bottom black bar (spec visual element) ----
rect([0.036, 0.854, 0.932, 0.885], "000000", "000000", 0);

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(err => { console.error(err); process.exit(1); });
