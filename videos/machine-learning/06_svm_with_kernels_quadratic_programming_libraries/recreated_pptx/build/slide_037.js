// Slide 037 — REBUILD WAVE 3 final, from qa/reanalysis2/slide_037_analysis.txt only.
// House chrome + 3 blue panels + white header, green kernel-term highlights mapped
// onto the rendered equations, red down-arrow, 2-D mathtext PNGs (eq_037/s37f_*).
// Build from project root.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 37;
const W = 13.33, H = 7.5;
const EQ = path.join(__dirname, "eq_037");
const OUT = path.join(NS, "recreated_pptx", "slide_037_recreated.pptx");
const M = JSON.parse(fs.readFileSync(path.join(EQ, "s37f_manifest.json"), "utf8"));
const FONT = "Times New Roman";
const N = b => ({ x: b[0] * W, y: b[1] * H, w: (b[2] - b[0]) * W, h: (b[3] - b[1]) * H });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome frame + badge (geometry fixed by house rule) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});

// ---- spec section 4 boxes (drawn before text so nothing covers the title) ----
function box(b, fill, line, shape) {
  s.addShape(shape || pres.shapes.RECTANGLE,
    Object.assign(N(b), { fill: { color: fill }, line: { color: line, width: 1.25 } }));
}
box([0.07, 0.07, 0.93, 0.16], "FFFFFF", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.07, 0.17, 0.93, 0.45], "F5F5F5", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.07, 0.49, 0.93, 0.61], "E0E0E0", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.07, 0.62, 0.93, 0.93], "F5F5F5", "00008B", pres.shapes.ROUNDED_RECTANGLE);
box([0.08, 0.08, 0.35, 0.14], "FFFFFF", "00008B");

// ---- house chrome title + badge numeral (on top of the header band) ----
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("How to Kernelize SVM", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("Example: Polynomial Kernel", Object.assign(N([0.08, 0.08, 0.35, 0.14]), {
  align: "left", valign: "middle", fontSize: 12, italic: true, color: "00008B",
  fontFace: FONT, margin: 0.02,
}));

// ---- green highlights on kernel terms, as fractions of each equation image ----
const HL = {
  s37f_lag_orig: [[0.845, -0.13, 1.03, 1.0]],
  s37f_b_orig:   [[-0.005, -0.15, 0.64, 1.25], [0.678, -0.27, 1.01, 1.45]],
  s37f_cls_orig: [[0.281, -0.61, 0.96, 1.42]],
  s37f_lag_kern: [[0.721, -0.13, 1.0, 0.86]],
  s37f_b_kern:   [[-0.006, -0.20, 1.0, 1.5]],
  s37f_cls_kern: [[0.225, -0.17, 0.99, 1.24]],
};
for (const name of Object.keys(HL)) {
  const m = M[name];
  for (const [f0, g0, f1, g1] of HL[name]) {
    s.addShape(pres.shapes.RECTANGLE, {
      x: m.x + f0 * m.w_in, y: m.y + g0 * m.h_in,
      w: (f1 - f0) * m.w_in, h: (g1 - g0) * m.h_in,
      fill: { color: "90EE90" }, line: { type: "none" },
    });
  }
}

// ---- red down-arrow (original-measured [0.435,0.512,0.551,0.596]) ----
s.addShape(pres.shapes.DOWN_ARROW, Object.assign(N([0.435, 0.512, 0.551, 0.596]), {
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0.5 },
}));

// ---- equations on top of the highlights ----
for (const name of Object.keys(M)) {
  const m = M[name];
  s.addImage({ path: path.join(EQ, m.image), x: m.x, y: m.y, w: m.w_in, h: m.h_in });
}
// bottom panel repeats w = sum alpha_i y_i X_i verbatim (spec box [0.1,0.73,0.3,0.78])
{
  const m = M["s37f_w"];
  s.addImage({ path: path.join(EQ, m.image), x: 0.1 * W,
    y: 0.73 * H + ((0.78 - 0.73) * H - m.h_in) / 2, w: m.w_in, h: m.h_in });
}

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
