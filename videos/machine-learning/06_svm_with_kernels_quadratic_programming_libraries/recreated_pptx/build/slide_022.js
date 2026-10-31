// slide_022.js — FRESH rebuild from qa/reanalysis2/slide_022_analysis.txt (REBUILD WAVE 3).
// Spec coords [x0,y0,x1,y1] normalized -> inches: x*13.33, y*7.5, w=(x1-x0)*13.33, h=(y1-y0)*7.5.
// Build from PROJECT ROOT: cd /home/codespace/ai_llm_slides && node <NS>/recreated_pptx/build/slide_022.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQDIR = path.join(NS, "recreated_pptx/build/eq_022");
const manifest = require(path.join(EQDIR, "manifest.json"));
const W = 13.33, H = 7.5, SERIF = "Times New Roman";
const X = v => v * W, Y = v => v * H;
const box = r => ({ x: X(r[0]), y: Y(r[1]), w: (r[2] - r[0]) * W, h: (r[3] - r[1]) * H });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// Bottom black bar first so the house frame line stays on top of it (spec [0.04,0.96,0.97,1.00])
let b = box([0.04, 0.96, 0.97, 1.00]);
s.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "000000" }, line: { type: "none" } });

// House chrome (mandatory, overrides spec frame/badge/title)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("22", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
s.addText("Polynomial Kernel (of order 2)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: SERIF, margin: 0,
});

// helpers
function shape(r, type, opt) {
  const bb = box(r);
  s.addShape(type, Object.assign({ x: bb.x, y: bb.y, w: bb.w, h: bb.h }, opt));
}
function rect(r, fill, lineColor, lineW, rounded, dash) {
  const opt = {
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: lineColor, width: lineW },
  };
  if (dash) opt.line.dashType = dash;
  shape(r, rounded ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, opt);
}
function text(r, str, opt) {
  const bb = box(r);
  s.addText(str, Object.assign({
    x: bb.x, y: bb.y, w: bb.w, h: bb.h,
    align: "center", valign: "middle",
    fontFace: SERIF, margin: 0,
  }, opt));
}
// math PNG at natural size (w = px/600 in), centered in spec box, scaled down if too wide
function eq(name, r) {
  const bb = box(r), m = manifest[name];
  let w = m.w_in, h = m.h_in;
  if (w > bb.w) { h *= bb.w / w; w = bb.w; }
  s.addImage({ path: m.path, x: bb.x + (bb.w - w) / 2, y: bb.y + (bb.h - h) / 2, w, h });
}
// red right-pointing arrow: shaft + rotated triangle head
function arrow(r) {
  const bb = box(r);
  const headW = Math.min(0.22, bb.w * 0.45), shaftH = Math.min(0.045, bb.h * 0.3);
  s.addShape(pres.shapes.RECTANGLE, {
    x: bb.x, y: bb.y + bb.h / 2 - shaftH / 2, w: bb.w - headW, h: shaftH,
    fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
  });
  s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
    x: bb.x + bb.w - headW, y: bb.y, w: headW, h: bb.h, rotate: 90,
    fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
  });
}

// "Example-2" dashed blue rounded label (spec top-left)
rect([0.07, 0.09, 0.19, 0.16], null, "0000FF", 1.25, true, "dash");
text([0.07, 0.09, 0.19, 0.16], "Example-2", { fontSize: 14, bold: true, italic: true, color: "0000FF" });
// top equation [a^T b + 1]^2
eq("eq_top", [0.66, 0.10, 0.77, 0.16]);
// top input vector box (light yellow, blue border) + 2x2 vector matrix
rect([0.08, 0.25, 0.17, 0.37], "FFFFCC", "0000FF", 1.25, true);
eq("eq_vec", [0.08, 0.25, 0.17, 0.37]);
// long red arrow to Normal Model
arrow([0.18, 0.29, 0.53, 0.32]);
// Normal Model box (blue border)
rect([0.53, 0.17, 0.88, 0.44], null, "0000FF", 1.25);
text([0.65, 0.23, 0.75, 0.26], "Normal Model", { fontSize: 14, bold: true, italic: true, color: "FF0000" });
eq("eq_calc_ab", [0.65, 0.27, 0.74, 0.31]); // "Calculate a^T b" (red transpose)
// light blue inner rounded box + small a/b matrix
rect([0.65, 0.33, 0.72, 0.42], "CCFFFF", "0000FF", 1.0, true);
eq("eq_mat", [0.65, 0.33, 0.72, 0.42]);
// outgoing arrow
arrow([0.89, 0.30, 0.92, 0.33]);
// center caption box (white fill per judge MINOR) + text
rect([0.11, 0.42, 0.48, 0.48], "FFFFFF", "0000FF", 1.25);
text([0.11, 0.42, 0.48, 0.48], "Map Input data from 2-D to 6-D", { fontSize: 16, bold: true, italic: true, color: "0000FF" });
// bottom input vector box + matrix
rect([0.08, 0.65, 0.17, 0.77], "FFFFCC", "0000FF", 1.25, true);
eq("eq_vec", [0.08, 0.65, 0.17, 0.77]);
arrow([0.18, 0.69, 0.22, 0.72]);
// gray rounded box with [a^T b + 1]^2 above the mapping box
rect([0.24, 0.58, 0.35, 0.66], "D3D3D3", "000000", 1.0, true);
eq("eq_top", [0.24, 0.58, 0.35, 0.66]);
// Vectors Mapping box (red border) + label + a,b => u,v
rect([0.22, 0.66, 0.36, 0.76], null, "FF0000", 1.25);
text([0.22, 0.68, 0.36, 0.71], "Vectors Mapping", { fontSize: 12, bold: true, color: "FF0000" });
eq("eq_map", [0.23, 0.71, 0.35, 0.74]);
arrow([0.37, 0.69, 0.40, 0.72]);
// pink mapped-vectors box (purple border) + 6x2 feature matrix
rect([0.40, 0.57, 0.55, 0.85], "FFF0FF", "AA00AA", 1.25);
eq("eq_6x2", [0.40, 0.57, 0.55, 0.85]);
arrow([0.55, 0.69, 0.58, 0.72]);
// Kernelized Model box (green border)
rect([0.57, 0.51, 0.88, 0.91], null, "33AA33", 1.25);
text([0.66, 0.53, 0.79, 0.56], "Kernelized Model", { fontSize: 14, bold: true, italic: true, color: "FF0000" });
eq("eq_calc_uv", [0.68, 0.57, 0.75, 0.61]);
// light green inner rounded box + row/column feature vectors
rect([0.58, 0.62, 0.87, 0.91], "EFFFEF", "33AA33", 1.0, true);
eq("eq_rowcol", [0.58, 0.62, 0.87, 0.91]);
// purple "Higher Computational Complexity!!!" box
rect([0.60, 0.78, 0.73, 0.88], "CC99FF", "AA00AA", 1.0);
text([0.60, 0.78, 0.73, 0.88], [
  { text: "Higher", options: { fontSize: 12, italic: true, color: "000000", fontFace: SERIF, breakLine: true } },
  { text: "Computational", options: { fontSize: 12, italic: true, color: "000000", fontFace: SERIF, breakLine: true } },
  { text: "Complexity!!!", options: { fontSize: 12, italic: true, color: "000000", fontFace: SERIF } },
], { align: "center", valign: "middle" });
// final outgoing arrow
arrow([0.89, 0.69, 0.92, 0.72]);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_022_recreated.pptx") })
  .then(() => console.log("wrote slide_022_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
