// slide_032.js — FRESH rebuild (wave 3, final) from qa/reanalysis2/slide_032_analysis.txt,
// geometry pixel-verified on qa/rejudge2/orig_png/slide_032.png:
// panels x 0.135..0.695 (left two-thirds), y-runs 0.30-0.426 / 0.456-0.583 /
// 0.609-0.739 / 0.776-0.909; headers + equations left-aligned at x=0.059;
// eq colors: K blue, K_1/K_2/K_3 red, alpha green; eqs 24pt left-aligned.
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

// Four panels: white fill, blue #0000FF border, pixel-measured coords
const panels = [
  [0.135, 0.300, 0.695, 0.426],
  [0.135, 0.456, 0.695, 0.583],
  [0.135, 0.609, 0.695, 0.739],
  [0.135, 0.776, 0.695, 0.909],
];
panels.forEach(p => {
  const b = box(...p);
  s.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 } });
});

// Panel headers: verbatim spec strings, bold black, left-aligned at x=0.059, panel top
const headers = [
  ["Sum of Kernels is a Kernel", 0.235],
  ["Scalar Product of Kernel is a kernel", 0.466],
  ["Product of Kernels is a Kernel", 0.618],
  ["Combination of the above rules is a Kernel", 0.786],
];
headers.forEach(([t, yc]) => {
  const b = box(0.059, yc, 0.69, yc + 0.055);
  s.addText(t, { x: b.x, y: b.y, w: b.w, h: b.h, align: "left", valign: "middle", fontSize: 18, bold: true, color: "000000", fontFace: FONT, margin: 0 });
});

// Equations: 600-dpi mathtext PNGs at exact size (w_in = px/600), left-aligned
["eq1", "eq2", "eq3", "eq4"].forEach(k => {
  const m = manifest[k];
  s.addImage({ path: EQ + m.file, x: m.x, y: m.y, w: m.w_in, h: m.h_in });
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_032_recreated.pptx") });
