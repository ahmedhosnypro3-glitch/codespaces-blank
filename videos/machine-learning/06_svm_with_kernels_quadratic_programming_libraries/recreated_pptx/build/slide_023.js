// slide_023.js — FRESH rebuild from qa/reanalysis2/slide_023_analysis.txt (rebuild wave 3)
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_023.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NUM = 23;
const TITLE = "Radial Basis Function (RBF) Kernel";
const W = 13.33, H = 7.5;
const SERIF = "Times New Roman";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQDIR = path.join(NS, "recreated_pptx/build/eq_023_rb5");
const manifest = require(path.join(EQDIR, "manifest.json"));

// normalized spec coords [x0,y0,x1,y1] -> inches
const X = v => v * 13.33, Y = v => v * 7.5;
const box = r => ({ x: X(r[0]), y: Y(r[1]), w: (r[2] - r[0]) * 13.33, h: (r[3] - r[1]) * 7.5 });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec frame/badge/title)
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
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 22, bold: true, color: "C00000", fontFace: SERIF, margin: 0,
});

// helpers
function ctext(strOrRuns, r, opt) {
  const b = box(r);
  s.addText(strOrRuns, Object.assign({
    x: b.x, y: b.y, w: b.w, h: b.h,
    align: "center", valign: "middle",
    fontFace: SERIF, margin: 0,
  }, opt));
}
function rect(r, fill, lineColor, lineW, rounded, dash) {
  const b = box(r);
  const opt = {
    x: b.x, y: b.y, w: b.w, h: b.h,
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: lineColor, width: lineW },
  };
  if (dash) opt.line.dashType = dash;
  s.addShape(rounded ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, opt);
}
function arrow(r, color, fillWhite, rotate) {
  const b = box(r);
  const opt = {
    x: b.x, y: b.y, w: b.w, h: b.h,
    fill: fillWhite ? { color: "FFFFFF" } : { type: "none" },
    line: { color: color, width: 1.5 },
  };
  if (rotate) opt.rotate = rotate;
  s.addShape(pres.shapes.RIGHT_ARROW, opt);
}
// math PNG at natural size (w = px/600); valign "top"/"bottom"/"center" in its spec box
function eq(name, r, valign) {
  const b = box(r), m = manifest[name];
  let y = b.y + (b.h - m.h_in) / 2;
  if (valign === "top") y = b.y;
  if (valign === "bottom") y = b.y + b.h - m.h_in;
  s.addImage({
    path: m.path,
    x: b.x + (b.w - m.w_in) / 2, y,
    w: m.w_in, h: m.h_in,
  });
}

// --- top band ---
rect([0.065, 0.081, 0.177, 0.150], "FFFFFF", "0000CC", 1, true, "dash");
ctext("Example-3", [0.065, 0.081, 0.177, 0.150], {
  align: "left", fontFace: "Arial", fontSize: 12, bold: true, italic: true, color: "0000CC",
});
eq("top_rbf", [0.645, 0.078, 0.777, 0.135], "bottom");

// --- upper-middle band: input matrix, long arrow, Normal Model panel ---
rect([0.076, 0.226, 0.165, 0.335], "FFFFFF", "BFBFBF", 1);
eq("mat_ab", [0.080, 0.241, 0.155, 0.319]);
arrow([0.167, 0.254, 0.500, 0.298], "C00000", true);
rect([0.507, 0.154, 0.823, 0.407], "FFFFFF", "0000CC", 1.5);
ctext("Normal Model", [0.618, 0.196, 0.713, 0.228], {
  fontSize: 13, bold: true, italic: true, color: "C00000",
});
eq("calc_atb", [0.619, 0.228, 0.708, 0.266], "top");
rect([0.620, 0.280, 0.688, 0.372], "E9F6FB", "6FA8C9", 1, true);
eq("mat_normal", [0.622, 0.291, 0.683, 0.361]);
arrow([0.822, 0.276, 0.854, 0.313], "C00000", true);

// --- mid banner ---
rect([0.069, 0.393, 0.502, 0.448], "FFFFFF", "0000CC", 1);
ctext([
  { text: "Map Input data from 2-D to ", options: { fontSize: 13, bold: true, italic: true, color: "0000CC", fontFace: SERIF } },
  { text: "infinite Dimension", options: { fontSize: 13, bold: true, italic: true, color: "C00000", fontFace: SERIF } },
], [0.080, 0.404, 0.491, 0.437], { align: "left" });

// --- lower half: grey eq box, lower input matrix, Vectors Mapping ---
rect([0.214, 0.489, 0.345, 0.570], "F2F2F2", "808080", 1, true);
eq("eq_rbf", [0.235, 0.500, 0.340, 0.557]);
rect([0.076, 0.576, 0.165, 0.685], "FFFFFF", "BFBFBF", 1);
eq("mat_ab", [0.080, 0.590, 0.155, 0.668]);
rect([0.206, 0.580, 0.349, 0.680], "FDE7E7", "C00000", 1.5);
ctext("Vectors Mapping", [0.224, 0.591, 0.322, 0.617], {
  fontSize: 12, bold: true, color: "C00000",
});
eq("vec_map", [0.224, 0.612, 0.331, 0.654], "top");
rect([0.217, 0.691, 0.339, 0.780], "FF00FF", "FF00FF", 0);
ctext("Higher\nComputational\nComplexity !!!", [0.217, 0.691, 0.339, 0.780], {
  fontSize: 11, bold: true, italic: true, color: "0000FF",
});
rect([0.385, 0.500, 0.471, 0.759], "FCE9F7", "E86FC6", 1);
eq("vec_pink", [0.395, 0.531, 0.450, 0.744]);
arrow([0.352, 0.607, 0.383, 0.652], "C00000", true);
arrow([0.474, 0.607, 0.510, 0.652], "C00000", true);
arrow([0.501, 0.583, 0.516, 0.613], "70AD47", false, -45);

// --- Kernelized Model panel ---
rect([0.507, 0.444, 0.797, 0.809], "FFFFFF", "70AD47", 1.5);
ctext([
  { text: "Kernelized ", options: { fontSize: 13, bold: true, italic: true, color: "C00000", fontFace: SERIF } },
  { text: "Model", options: { fontSize: 13, italic: true, color: "000000", fontFace: SERIF } },
], [0.583, 0.463, 0.721, 0.496]);
eq("calc_utv", [0.629, 0.496, 0.719, 0.532], "top");
rect([0.555, 0.546, 0.764, 0.802], "EEF6EA", "70AD47", 1, true);
eq("mat_kernel", [0.570, 0.572, 0.755, 0.778]);
rect([0.568, 0.689, 0.691, 0.780], "FF00FF", "FF00FF", 0);
ctext("Higher\nComputational\nComplexity !!!", [0.568, 0.689, 0.691, 0.780], {
  fontSize: 11, bold: true, italic: true, color: "0000FF",
});
arrow([0.822, 0.607, 0.854, 0.644], "C00000", true);

// --- bottom black bar ---
rect([0.036, 0.854, 0.932, 0.885], "000000", "000000", 0);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_023_recreated.pptx") })
  .then(() => console.log("wrote slide_023_recreated.pptx"))
  .catch(e => console.error(e));
