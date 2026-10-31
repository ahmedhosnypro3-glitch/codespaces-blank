// slide_031.js — FRESH rebuild (wave 3) from qa/reanalysis2/slide_031_analysis.txt only.
// "Most Common Kernel Functions": 4 panels (Linear/Quadratic/Polynomial/RBF), equations as 2-D mathtext PNGs.
// Run: NODE_PATH=$(npm root -g) node slide_031.js
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_031/";
const manifest = JSON.parse(fs.readFileSync(EQ + "manifest.json", "utf8"));

const W = 13.33, H = 7.5, FONT = "Arial";
const box = (x0, y0, x1, y1) => ({ x: x0 * W, y: y0 * H, w: (x1 - x0) * W, h: (y1 - y0) * H });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// Spec: solid black bottom strip, drawn before the frame so the frame line stays visible
let b = box(0.042, 0.850, 0.922, 1.000);
s.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "000000" }, line: { type: "none" } });
// Spec: faint pale top rule
b = box(0.042, 0.067, 0.922, 0.072);
s.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "D5DBE8" }, line: { type: "none" } });
// House chrome: outer red frame, badge, title
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3, fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("31", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0 });
s.addText("Most Common Kernel Functions", { x: 0.6, y: 0.28, w: 12.13, h: 0.42, align: "center", valign: "middle", fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Panels (spec: white fill, #3333B3 outline)
const panels = [
  [0.082, 0.193, 0.667, 0.313],
  [0.082, 0.333, 0.667, 0.454],
  [0.082, 0.474, 0.667, 0.594],
  [0.082, 0.641, 0.667, 0.793],
];
panels.forEach(p => {
  b = box(...p);
  s.addShape(pres.shapes.RECTANGLE, { x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FFFFFF" }, line: { color: "3333B3", width: 1 } });
});

// Panel headings (bold black, spec boxes)
const headings = [
  ["Linear Kernel", 0.086, 0.206, 0.210, 0.237],
  ["Quadratic Kernel", 0.086, 0.341, 0.238, 0.372],
  ["Polynomial Kernel (of degree \u201cd\u201d)", 0.086, 0.481, 0.327, 0.515],
  ["Radial Basis Function (RBF) Kernel", 0.086, 0.648, 0.352, 0.683],
];
headings.forEach(([t, ...bb]) => {
  b = box(...bb);
  s.addText(t, { x: b.x, y: b.y, w: b.w, h: b.h, align: "left", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0 });
});
// Equations as 2-D mathtext PNGs at exact size (w_in = px/600, never rescaled)
["eq1", "eq2", "eq3", "eq4", "eq5", "eq6"].forEach(k => {
  const m = manifest[k];
  s.addImage({ path: EQ + m.file, x: m.x, y: m.y, w: m.w_in, h: m.h_in });
});

// "or" labels (black, centered between the two equations of panels 2 and 3)
[[0.330, 0.400, 0.348, 0.430], [0.330, 0.544, 0.348, 0.576]].forEach(bb => {
  b = box(...bb);
  s.addText("or", { x: b.x, y: b.y, w: b.w, h: b.h, align: "center", valign: "middle", fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
});

// Panel 1 note: "No Mapping , φ(x)= x" — all red, φ and x italic
b = box(0.344, 0.250, 0.517, 0.291);
s.addText([
  { text: "No Mapping , ", options: { color: "CC0000", fontSize: 11, fontFace: FONT } },
  { text: "φ", options: { color: "CC0000", fontSize: 11, italic: true, fontFace: FONT } },
  { text: "(", options: { color: "CC0000", fontSize: 11, fontFace: FONT } },
  { text: "x", options: { color: "CC0000", fontSize: 11, italic: true, fontFace: FONT } },
  { text: ")= ", options: { color: "CC0000", fontSize: 11, fontFace: FONT } },
  { text: "x", options: { color: "CC0000", fontSize: 11, italic: true, fontFace: FONT } },
], { x: b.x, y: b.y, w: b.w, h: b.h, align: "left", valign: "middle", margin: 0 });

// Panel 4 bandwidth note: leading γ bold italic red, remainder black
b = box(0.410, 0.733, 0.634, 0.770);
s.addText([
  { text: "γ", options: { color: "CC0000", fontSize: 11, bold: true, italic: true, fontFace: FONT } },
  { text: " is called RBF Kernel bandwidth", options: { color: "000000", fontSize: 11, fontFace: FONT } },
], { x: b.x, y: b.y, w: b.w, h: b.h, align: "left", valign: "middle", margin: 0 });

// Small grey pointer glyph between RBF equation and bandwidth note
b = box(0.358, 0.717, 0.375, 0.743);
s.addShape(pres.shapes.LINE, { x: b.x, y: b.y, w: b.w, h: b.h, line: { color: "6E6E6E", width: 2 } });

pres.writeFile({ fileName: NS + "/recreated_pptx/slide_031_recreated.pptx" });
