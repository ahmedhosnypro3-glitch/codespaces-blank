// Slide 036 — REBUILD fix pass, built ONLY from qa/reanalysis2/slide_036_analysis.txt.
// "How to Kernelize SVM" / Example: Quadratic Kernel. Equations are width-targeted
// 600-dpi mathtext PNGs (eq_036/eq_s36rb5_manifest.json; s36rb5_cls_bot carries the
// segmented [W^T Z]^2 green highlight). Side-limit sums per house rule.
// Build from project root: cd /home/codespace/ai_llm_slides && node <NS>/recreated_pptx/build/slide_036.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 36;
const W = 13.33, H = 7.5;
const EQ = path.join(__dirname, "eq_036");
const OUT = path.join(NS, "recreated_pptx", "slide_036_recreated.pptx");
const M = JSON.parse(fs.readFileSync(path.join(EQ, "eq_s36rb5_manifest.json"), "utf8"));
const FONT = "Arial";
const IN_X = 13.33, IN_Y = 7.5;
const N = b => ({ x: b[0] * IN_X, y: b[1] * IN_Y, w: (b[2] - b[0]) * IN_X, h: (b[3] - b[1]) * IN_Y });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (mandatory, overrides spec geometry) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("How to Kernelize SVM", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- helpers ----
function box(b, fill, line, shape) {
  s.addShape(shape || pres.shapes.RECTANGLE,
    Object.assign(N(b), { fill: { color: fill }, line: { color: line, width: 1.25 } }));
}
function richLabel(b, runs) {
  const r = N(b);
  s.addText(runs.map(t => ({ text: t[0], options: Object.assign({
    align: "center", fontSize: 12, fontFace: FONT,
  }, t[1]) })), Object.assign(r, { align: "center", valign: "middle", margin: 0 }));
}

// ---- panels, peach class strips INSIDE the panels, w/b row boxes (judge MAJORs/MINORs) ----
box([0.06, 0.08, 0.32, 0.14], "FFFFFF", "3333CC", pres.shapes.ROUNDED_RECTANGLE);
box([0.05, 0.23, 0.96, 0.46], "FFFFFF", "3333CC");
box([0.05, 0.59, 0.96, 0.87], "FFFFFF", "3333CC");
box([0.12, 0.405, 0.88, 0.45], "FFDAB9", "800000");
box([0.12, 0.81, 0.88, 0.865], "FFDAB9", "800000");
box([0.07, 0.345, 0.36, 0.425], "FFFFFF", "3333CC");
box([0.37, 0.345, 0.93, 0.425], "FFFFFF", "3333CC");
box([0.07, 0.71, 0.36, 0.79], "FFFFFF", "3333CC");
box([0.37, 0.71, 0.93, 0.79], "FFFFFF", "3333CC");
// center kernel row
box([0.28, 0.47, 0.42, 0.54], "FFFFFF", "800000");
box([0.59, 0.48, 0.71, 0.54], "FFFFFF", "800000");
// labels: "Example:" black italic + "Quadratic Kernel" bold blue; "Kernelize using" black italic
richLabel([0.06, 0.08, 0.32, 0.14], [
  ["Example: ", { italic: true, color: "000000" }],
  ["Quadratic Kernel", { italic: true, bold: true, color: "0000FF" }],
]);
richLabel([0.28, 0.47, 0.42, 0.54], [
  ["Kernelize using", { italic: true, color: "000000" }],
]);

// ---- red HOLLOW down-arrow between the panels, tip above the bottom panel (judge MINOR) ----
s.addShape(pres.shapes.DOWN_ARROW, {
  x: 0.43 * IN_X, y: 0.545 * IN_Y, w: 0.04 * IN_X, h: 0.04 * IN_Y,
  fill: { type: "none" }, line: { color: "FF0000", width: 2 },
});

// ---- equations: green highlight rects behind marked terms first, then the PNG ----
function eq(name, cyOverride) {
  const m = M[name];
  const cy = cyOverride || m.cy_in;
  const y = cy - m.h_in / 2;
  for (const lab of m.highlights) {
    const g = m.segments[lab];
    if (!g) continue;
    s.addShape(pres.shapes.RECTANGLE, {
      x: m.x_in + g[0] / 600 - 0.03, y: y + g[2] / 600 - 0.02,
      w: (g[1] - g[0]) / 600 + 0.06, h: (g[3] - g[2]) / 600 + 0.04,
      fill: { color: "90EE90" }, line: { type: "none" },
    });
  }
  s.addImage({ path: path.join(EQ, m.image), x: m.x_in, y, w: m.w_in, h: m.h_in });
}
eq("s36rb4_lag_top");
eq("s36rb4_w_top");
eq("s36rb4_b_top");
eq("s36rb4_cls_top", 3.24);
eq("s36rb4_kern");
eq("s36rb4_lag_bot");
eq("s36rb4_w_bot");
eq("s36rb4_b_bot");
eq("s36rb5_cls_bot");

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
