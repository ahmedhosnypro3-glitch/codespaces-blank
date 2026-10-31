// slide_032.js — FRESH rebuild (wave 3) from qa/reanalysis2/slide_032_analysis.txt only.
// "New Kernel Functions can be derived From other Kernels": 4 blue-bordered panels,
// equations as 2-D mathtext PNGs. No plots (spec IMAGERY: none).
// Run from project root: node <NS>/recreated_pptx/build/slide_032.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_032/");
const manifest = JSON.parse(fs.readFileSync(EQ + "manifest.json", "utf8"));

const W = 13.33, H = 7.5, FONT = "Arial";
const box = (x0, y0, x1, y1) => ({ x: x0 * W, y: y0 * H, w: (x1 - x0) * W, h: (y1 - y0) * H });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome (overrides spec): red frame, badge, title box
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("32", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0 });
s.addText("New Kernel Functions can be derived\nFrom other Kernels", { x: 0.6, y: 0.28, w: 12.13, h: 1.1, align: "center", valign: "top", fontSize: 30, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Four panels: white fill, blue #0000FF border, spec section 4 coords
const panels = [
  [0.05, 0.22, 0.95, 0.43],
  [0.05, 0.45, 0.95, 0.60],
  [0.05, 0.62, 0.95, 0.77],
  [0.05, 0.79, 0.95, 0.94],
];
panels.forEach(p => {
  const b = box(...p);
  s.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 } });
});

// Panel headers: verbatim spec strings, bold black, left-aligned at panel top
const headers = [
  ["Sum of Kernels is a Kernel", 0.07, 0.228, 0.90, 0.282],
  ["Scalar Product of Kernel is a kernel", 0.07, 0.458, 0.90, 0.502],
  ["Product of Kernels is a Kernel", 0.07, 0.628, 0.90, 0.662],
  ["Combination of the above rules is a Kernel", 0.07, 0.802, 0.93, 0.836],
];
headers.forEach(([t, x0, y0, x1, y1]) => {
  const b = box(x0, y0, x1, y1);
  s.addText(t, { x: b.x, y: b.y, w: b.w, h: b.h, align: "left", valign: "middle", fontSize: 18, bold: true, color: "000000", fontFace: FONT, margin: 0 });
});

// Equations: 600-dpi mathtext PNGs at exact size (w_in = px/600), manifest-centered
["eq1", "eq2", "eq3", "eq4"].forEach(k => {
  const m = manifest[k];
  s.addImage({ path: EQ + m.file, x: m.x, y: m.y, w: m.w_in, h: m.h_in });
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_032_recreated.pptx") });
