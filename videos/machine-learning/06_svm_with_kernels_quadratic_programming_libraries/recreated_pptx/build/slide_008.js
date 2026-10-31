// slide_008.js — "Example" QP slide (rebuild wave 3)
// Built ONLY from qa/reanalysis2/slide_008_analysis.txt (spec starts at "1. SLIDE_TITLE").
// House chrome per video AGENTS.md overrides spec frame/badge/title.
// Math assets: 600-dpi mathtext PNGs in build/eq_008/ (gen_eq_008.py + manifest.json).
// Run: NODE_PATH=$(npm root -g) node slide_008.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const { newPres, W, H, FONT } = require("./shared.js");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_008/");
const OUT = path.join(NS, "recreated_pptx/slide_008_recreated.pptx");
const M = JSON.parse(fs.readFileSync(EQ + "manifest.json", "utf8"));
const MATH = "Times New Roman";

const pres = newPres();
const s = pres.addSlide();

// House chrome (mandatory, overrides spec frame/badge/title)
s.background = { color: "E8E8E8" };
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("8", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Example", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

const N = (v) => v * 13.33;
const NY = (v) => v * 7.5;
const box = (b) => ({ x: N(b[0]), y: NY(b[1]), w: N(b[2] - b[0]), h: NY(b[3] - b[1]) });
function img(name, b, align) {  // native px/600 size, vertically centered in box
  const m = M[name], r = box(b);
  const x = align === "left" ? r.x : r.x + (r.w - m.w_in) / 2;
  s.addImage({ path: EQ + m.image, x, y: r.y + (r.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
}
function panel(b) {
  const r = box(b);
  s.addShape(pres.shapes.RECTANGLE, { x: r.x, y: r.y, w: r.w, h: r.h, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 } });
}
function callout(b) {
  const r = box(b);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: r.x, y: r.y, w: r.w, h: r.h, fill: { color: "FCE4D6" }, line: { color: "E8B79B", width: 1 } });
}

// Objective panel: "Minimize 0.5x^2+3x+4y" + quadratic-form callout
panel([0.076, 0.196, 0.931, 0.500]);
{
  const r = box([0.085, 0.208, 0.188, 0.248]);
  s.addText("Minimize", { x: r.x, y: r.y, w: r.w, h: r.h, align: "left", valign: "middle", fontSize: 20, bold: true, italic: true, color: "1A1A1A", fontFace: MATH, margin: 0 });
}
img("obj", [0.188, 0.203, 0.325, 0.248], "left");
callout([0.763, 0.293, 0.917, 0.372]);
img("qform", [0.765, 0.293, 0.917, 0.372]);

// Constraint panel: "Subject to" + Gx<=h callout + 5-line stack
panel([0.076, 0.519, 0.931, 0.867]);
{
  const r = box([0.086, 0.535, 0.168, 0.566]);
  s.addText("Subject to", { x: r.x, y: r.y, w: r.w, h: r.h, align: "left", valign: "middle", fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
}
callout([0.404, 0.534, 0.508, 0.602]);
img("gxh", [0.413, 0.545, 0.500, 0.590]);
img("c1", [0.085, 0.611, 0.126, 0.648], "left");
img("c2", [0.085, 0.653, 0.126, 0.689], "left");
img("c3", [0.085, 0.694, 0.185, 0.731], "left");
img("c4", [0.085, 0.735, 0.201, 0.772], "left");
img("c5", [0.085, 0.777, 0.194, 0.813], "left");

pres.writeFile({ fileName: require("path").join(NS, "recreated_pptx/slide_008_recreated.pptx") })
  .then(() => console.log("wrote", OUT));
