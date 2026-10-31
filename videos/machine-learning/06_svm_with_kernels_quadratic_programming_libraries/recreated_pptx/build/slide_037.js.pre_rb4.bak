// Slide 037 — REBUILD WAVE 3, built ONLY from qa/reanalysis2/slide_037_analysis.txt.
// "How to Kernelize SVM" — Example: Polynomial Kernel. White header band with
// example label, top/middle/bottom blue-bordered boxes, green formula highlights,
// red down-arrow, 2-D mathtext equation PNGs (eq_037/s37w3_*).
// Build from project root: cd /home/codespace/ai_llm_slides && node <NS>/recreated_pptx/build/slide_037.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 37;
const W = 13.33, H = 7.5;
const EQ = path.join(__dirname, "eq_037");
const OUT = path.join(NS, "recreated_pptx", "slide_037_recreated.pptx");
const M = JSON.parse(fs.readFileSync(path.join(EQ, "s37w3_manifest.json"), "utf8"));
const FONT = "Times New Roman";
const N = b => ({ x: b[0] * W, y: b[1] * H, w: (b[2] - b[0]) * W, h: (b[3] - b[1]) * H });

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
  const o = N(b);
  const opt = { fill: { color: fill }, line: { color: line, width: 1.25 } };
  if (shape) opt.shape = shape;
  s.addShape(shape || pres.shapes.RECTANGLE, opt);
}
function hl(b) {
  s.addShape(pres.shapes.RECTANGLE,
    Object.assign(N(b), { fill: { color: "90EE90" }, line: { type: "none" } }));
}

// ---- spec section 4 boxes (rounded header + 3 panels, plain example box) ----
box([0.07, 0.07, 0.93, 0.16], "FFFFFF", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.07, 0.17, 0.93, 0.45], "F5F5F5", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.07, 0.49, 0.93, 0.61], "E0E0E0", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.07, 0.62, 0.93, 0.93], "F5F5F5", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.08, 0.08, 0.35, 0.14], "FFFFFF", "00008B");

// ---- green highlights, measured from the original frame (kernel terms only) ----
hl([0.412, 0.190, 0.480, 0.278]);  // top L_D: X_i^T X_j
hl([0.378, 0.293, 0.630, 0.360]);  // top b: max arg
hl([0.645, 0.287, 0.775, 0.367]);  // top b: min arg
hl([0.285, 0.380, 0.482, 0.447]);  // top class line: w^T Z
hl([0.424, 0.630, 0.558, 0.707]);  // bottom L_D: [X_i^T X_j + 1]^d
hl([0.355, 0.723, 0.898, 0.815]);  // bottom b: max/min args
hl([0.285, 0.830, 0.555, 0.889]);  // bottom class line: [w^T Z + 1]^d

// ---- red down-arrow between top and middle boxes ----
s.addShape(pres.shapes.DOWN_ARROW, Object.assign(N([0.45, 0.48, 0.55, 0.55]), {
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0.5 },
}));

// ---- example label (verbatim, spec brief item 2) ----
s.addText("Example: Polynomial Kernel", Object.assign(N([0.08, 0.08, 0.35, 0.14]), {
  align: "left", valign: "middle", fontSize: 12, color: "000000",
  fontFace: FONT, margin: 0.02,
}));
// ---- equations (spec section 8 boxes): left edge at box x, vertically centered ----
function eq(name, boxOverride) {
  const m = M[name];
  const b = boxOverride || m.box;
  const x = b[0];
  const y = b[1] + (b[3] - m.h_in) / 2;
  s.addImage({ path: path.join(EQ, m.image), x, y, w: m.w_in, h: m.h_in });
}
eq("s37w3_lag_orig");   // top box  [0.1,0.2,0.9,0.28]
eq("s37w3_w");          // top box  [0.1,0.3,0.3,0.35]
eq("s37w3_b_orig");     // top box  [0.35,0.3,0.9,0.35]
eq("s37w3_cls_orig");   // top box  [0.2,0.4,0.8,0.45]
eq("s37w3_kernelize");  // middle   [0.4,0.5,0.75,0.55] "Kernelize using K(a,b)=[a^T b+1]^d"
eq("s37w3_lag_kern");   // bottom   [0.1,0.64,0.9,0.72]
eq("s37w3_w", [1.333, 5.475, 3.999, 0.375]); // bottom [0.1,0.73,0.3,0.78], w repeats verbatim
eq("s37w3_b_kern");     // bottom   [0.35,0.73,0.9,0.78]
eq("s37w3_cls_kern");   // bottom   [0.2,0.83,0.8,0.88]

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
