// slide_020.js — FRESH rebuild of "Model Kernelization" from qa/reanalysis2/slide_020_analysis.txt ONLY.
// Build from project root: node videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/slide_020.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const M = require(path.join(NS, "recreated_pptx/build/eq_020/manifest.json"));
const X = 13.33, Y = 7.5;
const R = (x0, y0, x1, y1) => ({ x: x0 * X, y: y0 * Y, w: (x1 - x0) * X, h: (y1 - y0) * Y });
const SERIF = "Times New Roman", SANS = "Arial";
const RED = "C00000", BLUE = "0000CC", GREEN = "00B050";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// black band across bottom edge (spec visual element, drawn under the house frame)
let band = R(0.042, 0.941, 0.958, 1.0);
s.addShape(pres.shapes.RECTANGLE, { x: band.x, y: band.y, w: band.w, h: band.h, fill: { color: "000000" }, line: { color: "000000", width: 0.25 } });

// house chrome (overrides spec frame/badge/title)
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { type: "none" }, line: { color: RED, width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("20", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: SANS, margin: 0 });
s.addText("Model Kernelization", { x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top", fontSize: 26, bold: true, italic: true, color: RED, fontFace: SERIF, margin: 0 });

function txt(str, box, o) {
  s.addText(str, Object.assign({ x: box.x, y: box.y, w: box.w, h: box.h, align: "center", valign: "middle", margin: 0 }, o));
}
function runs(arr, box, o) {
  s.addText(arr, Object.assign({ x: box.x, y: box.y, w: box.w, h: box.h, align: "center", valign: "middle", margin: 0 }, o));
}
function rect(box, fill, line, wpt, rounded) {
  s.addShape(rounded ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE,
    { x: box.x, y: box.y, w: box.w, h: box.h, fill: { color: fill }, line: { color: line, width: wpt || 1.5 } });
}
function arrow(box) {
  s.addShape(pres.shapes.RIGHT_ARROW, { x: box.x, y: box.y, w: box.w, h: box.h, fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 } });
}
function eq(key, box) {
  const m = M[key];
  let w = m.w_in, h = m.h_in;
  if (w > box.w) { h *= box.w / w; w = box.w; }
  if (h > box.h) { w *= box.h / h; h = box.h; }
  s.addImage({ path: m.path, x: box.x + (box.w - w) / 2, y: box.y + (box.h - h) / 2, w, h });
}
function complexity(box) {
  rect(box, "E8DCF5", "B4A7D6", 1);
  const o = { fontSize: 11, bold: true, italic: true, color: BLUE, fontFace: SERIF };
  const h3 = box.h / 3;
  txt("Higher", { x: box.x, y: box.y, w: box.w, h: h3 }, o);
  txt("Computational", { x: box.x, y: box.y + h3, w: box.w, h: h3 }, o);
  txt("Complexity !!!", { x: box.x, y: box.y + 2 * h3, w: box.w, h: h3 }, o);
}

// upper-left input vector box + content
rect(R(0.081, 0.254, 0.167, 0.365), "FFFFFF", BLUE, 1.5);
eq("eq20_vec", R(0.083, 0.256, 0.165, 0.363));
// long arrow into Normal Model panel
arrow(R(0.173, 0.293, 0.513, 0.326));
// Normal Model panel
rect(R(0.518, 0.189, 0.846, 0.435), "FFFFFF", BLUE, 1.5);
runs([{ text: "Normal ", options: { fontSize: 14, bold: true, italic: true, color: RED, fontFace: SERIF } },
      { text: "Model", options: { fontSize: 14, bold: true, italic: true, color: BLUE, fontFace: SERIF } }], R(0.640, 0.226, 0.731, 0.259));
eq("eq20_calc_a", R(0.643, 0.267, 0.720, 0.298));
rect(R(0.637, 0.319, 0.710, 0.417), "DEEAF6", "9DC3E6", 1, true);
eq("eq20_norm_mtx", R(0.639, 0.321, 0.708, 0.415));
// O/P + small arrow at right of Normal panel
txt("O/P", R(0.871, 0.265, 0.906, 0.293), { fontSize: 13, bold: true, italic: true, color: BLUE, fontFace: SANS });
arrow(R(0.865, 0.302, 0.898, 0.330));
// instruction box (two centred blue bold-italic lines)
rect(R(0.108, 0.417, 0.461, 0.524), "FFFFFF", BLUE, 1.5);
const io = { fontSize: 16, bold: true, italic: true, color: BLUE, fontFace: SANS };
txt("Map Input data to higher dimensions", R(0.108, 0.417, 0.461, 0.470), io);
txt("Before Apply to the model", R(0.108, 0.470, 0.461, 0.524), io);
// lower flow row, left to right
rect(R(0.081, 0.639, 0.167, 0.763), "FFFFFF", BLUE, 1.5);
eq("eq20_vec", R(0.083, 0.641, 0.165, 0.761));
arrow(R(0.172, 0.683, 0.206, 0.711));
// Vectors Mapping box
rect(R(0.211, 0.652, 0.357, 0.752), "FFFFFF", RED, 1.5);
txt("Vectors Mapping", R(0.211, 0.654, 0.357, 0.698), { fontSize: 14, bold: true, color: RED, fontFace: SERIF });
eq("eq20_map", R(0.221, 0.700, 0.350, 0.745));
complexity(R(0.222, 0.763, 0.347, 0.870));
arrow(R(0.364, 0.683, 0.394, 0.711));
// tall purple u/v matrix box
rect(R(0.398, 0.565, 0.481, 0.861), "F1E8F8", "B4A7D6", 1.5);
eq("eq20_uv_mtx", R(0.400, 0.567, 0.479, 0.859));
arrow(R(0.495, 0.683, 0.526, 0.711));
// Kernelized Model panel
rect(R(0.523, 0.504, 0.833, 0.902), "FFFFFF", GREEN, 1.5);
runs([{ text: "Kernelized ", options: { fontSize: 14, bold: true, italic: true, color: RED, fontFace: SERIF } },
      { text: "Model", options: { fontSize: 14, bold: true, italic: true, color: BLUE, fontFace: SERIF } }], R(0.604, 0.530, 0.729, 0.561));
eq("eq20_calc_u", R(0.651, 0.565, 0.719, 0.594));
rect(R(0.573, 0.611, 0.792, 0.902), "E2EFDA", "A9D08E", 1, true);
eq("eq20_kern_uv", R(0.594, 0.618, 0.782, 0.768));
complexity(R(0.594, 0.772, 0.693, 0.870));
// O/P + small arrow at right of Kernelized panel
txt("O/P", R(0.881, 0.641, 0.917, 0.667), { fontSize: 13, bold: true, italic: true, color: BLUE, fontFace: SANS });
arrow(R(0.870, 0.680, 0.902, 0.709));

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_020_recreated.pptx") });
