// Slide 036 — REBUILD WAVE 3, built ONLY from qa/reanalysis2/slide_036_analysis.txt.
// "How to Kernelize SVM" / Example: Quadratic Kernel: two blue-bordered white
// panels (primal dual top, kernelized dual bottom), center "Kernelize using" +
// red K(a,b)=(a^T b)^2 boxes with a red down arrow, two peach class-of-vector
// strips. Equations are segmented 600-dpi mathtext PNGs (eq_036/s36rb3_*).
// Build from project root: cd /home/codespace/ai_llm_slides && node <NS>/recreated_pptx/build/slide_036.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 36;
const W = 13.33, H = 7.5;
const EQ = path.join(__dirname, "eq_036");
const OUT = path.join(NS, "recreated_pptx", "slide_036_recreated.pptx");
const M = JSON.parse(fs.readFileSync(path.join(EQ, "eq_s36rb3_manifest.json"), "utf8"));
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
function label(b, text, color, italic) {
  const r = N(b);
  s.addText(text, Object.assign(r, {
    align: "center", valign: "middle", fontSize: 12, italic: !!italic,
    color, fontFace: FONT, margin: 0,
  }));
}

// ---- header label + panels + peach strips + kernel boxes (spec section 4) ----
box([0.06, 0.08, 0.32, 0.14], "FFFFFF", "3333CC", pres.shapes.ROUNDED_RECTANGLE);
box([0.05, 0.23, 0.96, 0.46], "FFFFFF", "3333CC");
box([0.05, 0.59, 0.96, 0.87], "FFFFFF", "3333CC");
box([0.12, 0.47, 0.88, 0.51], "FFDAB9", "800000");
box([0.12, 0.83, 0.88, 0.87], "FFDAB9", "800000");
box([0.28, 0.47, 0.42, 0.54], "FFFFFF", "800000");
box([0.59, 0.48, 0.71, 0.54], "FFFFFF", "800000");
// ---- text labels (spec verbatim) ----
label([0.06, 0.08, 0.32, 0.14], "Example: Quadratic Kernel", "0000FF", true);
label([0.28, 0.47, 0.42, 0.54], "Kernelize using", "FF0000", false);

// ---- red block down-arrow bridging kernel strip to bottom panel (spec x/y
//      [0.43,0.48,0.47,...]; extended down to visibly connect into the panel) ----
s.addShape(pres.shapes.DOWN_ARROW, {
  x: 0.43 * IN_X, y: 0.48 * IN_Y, w: 0.04 * IN_X, h: 0.12 * IN_Y,
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0.5 },
});

// ---- equations (spec section 8 boxes): left-aligned at box x, vertically
//      centered; green highlight rects over the marked terms, drawn first ----
function eq(name, boxOverride) {
  const m = M[name];
  const b = boxOverride || m.box;
  const x = b[0], y = b[1] + (b[3] - m.h_in) / 2;
  for (const lab of m.highlights) {
    const g = m.segments[lab];
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + g[0] / 600 - 0.03, y: y + g[2] / 600 - 0.02,
      w: (g[1] - g[0]) / 600 + 0.06, h: (g[3] - g[2]) / 600 + 0.04,
      fill: { color: "90EE90" }, line: { type: "none" },
    });
  }
  s.addImage({ path: path.join(EQ, m.image), x, y, w: m.w_in, h: m.h_in });
}
eq("s36rb3_lag_top");
eq("s36rb3_w");
eq("s36rb3_b_top");
eq("s36rb3_cls_top");
eq("s36rb3_kern");
eq("s36rb3_lag_bot");
eq("s36rb3_w", [1.0664, 5.325, 3.5991, 0.525]); // spec [0.08,0.71,0.35,0.78] -> inches; w repeats verbatim in bottom panel
eq("s36rb3_b_bot");
eq("s36rb3_cls_bot");

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
