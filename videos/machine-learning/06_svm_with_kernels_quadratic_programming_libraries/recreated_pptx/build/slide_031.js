// slide_031.js — REBUILD WAVE 3, built ONLY from qa/reanalysis2/slide_031_analysis.txt
// "Most Common Kernel Functions": 4 blue-outlined kernel panels (Linear, Quadratic,
// Polynomial, RBF), 2D mathtext equation PNGs, red/black ink split per spec.
// Run from project root: node <NS>/recreated_pptx/build/slide_031.js
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_031/");
const manifest = require(path.join(EQ, "manifest.json"));

const NUM = 31;
const TITLE = "Most Common Kernel Functions";
const FONT = "Arial";
const MATH = "Times New Roman";
const W = 13.33, H = 7.5;

// normalized spec coords [x0,y0,x1,y1] -> inches
const IN = (b) => ({ x: b[0] * W, y: b[1] * H, w: (b[2] - b[0]) * W, h: (b[3] - b[1]) * H });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome: outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// House chrome: slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// House chrome: title
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 21, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Faint pale top rule was marked [?] in the spec and crosses the title text
// (judged as a strikethrough artifact) — omitted.

// Four kernel panels: white fill, blue-violet outline, bold black heading
const PANELS = [
  { box: [0.082, 0.193, 0.667, 0.313], head: "Linear Kernel", hb: [0.086, 0.206, 0.210, 0.237] },
  { box: [0.082, 0.333, 0.667, 0.454], head: "Quadratic Kernel", hb: [0.086, 0.341, 0.238, 0.372] },
  { box: [0.082, 0.474, 0.667, 0.594], head: "Polynomial Kernel (of degree \u201cd\u201d)", hb: [0.086, 0.481, 0.327, 0.515] },
  { box: [0.082, 0.641, 0.667, 0.793], head: "Radial Basis Function (RBF) Kernel", hb: [0.086, 0.648, 0.352, 0.683] },
];
for (const p of PANELS) {
  const pb = IN(p.box);
  s.addShape(pres.shapes.RECTANGLE, {
    x: pb.x, y: pb.y, w: pb.w, h: pb.h,
    fill: { color: "FFFFFF" }, line: { color: "3333B3", width: 1 },
  });
  const hb = IN(p.hb);
  s.addText(p.head, {
    x: hb.x, y: hb.y, w: hb.w, h: hb.h,
    align: "left", valign: "middle",
    fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
}
// "or" separators between the two equations of panels 2 and 3
for (const ob of [[0.330, 0.400, 0.348, 0.430], [0.330, 0.544, 0.348, 0.576]]) {
  const b = IN(ob);
  s.addText("or", {
    x: b.x, y: b.y, w: b.w, h: b.h,
    align: "center", valign: "middle",
    fontSize: 11, color: "000000", fontFace: FONT, margin: 0,
  });
}

// 2D math equations: place each PNG centered in its spec box at natural size
// (w = px/600 in), scaled down only if wider than the box.
const EQS = [
  ["eq1", [0.121, 0.246, 0.217, 0.289]],
  ["eq_phi", [0.344, 0.250, 0.517, 0.291]],
  ["eq2", [0.125, 0.387, 0.235, 0.431]],
  ["eq3", [0.408, 0.387, 0.535, 0.431]],
  ["eq4", [0.121, 0.533, 0.238, 0.580]],
  ["eq5", [0.408, 0.533, 0.560, 0.580]],
  ["eq6", [0.129, 0.717, 0.333, 0.770]],
];
for (const [name, specBox] of EQS) {
  const m = manifest[name];
  const b = IN(specBox);
  const w = m.w_in, h = m.h_in;
  s.addImage({
    path: path.join(EQ, m.file),
    x: b.x, y: b.y + (b.h - h) / 2, w, h,
  });
}

// RBF bandwidth note: red bold-italic gamma + black remainder
const nb = IN([0.410, 0.733, 0.634, 0.770]);
s.addText([
  { text: "\u03b3", options: { color: "CC0000", bold: true, italic: true, fontFace: MATH, fontSize: 12 } },
  { text: " is called RBF Kernel bandwidth", options: { color: "000000", fontFace: FONT, fontSize: 11 } },
], { x: nb.x, y: nb.y, w: nb.w, h: nb.h, align: "left", valign: "middle", margin: 0 });

// Tiny grey pointer glyph [?] in the original is a capture/cursor artifact — omitted.

// Bottom black strip of the original frame is a video-capture artifact
// (ground rule: capture artifacts are correctly omitted) — not recreated.

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_031_recreated.pptx") })
  .then(() => console.log("wrote slide_031_recreated.pptx"))
  .catch((err) => console.error(err));
