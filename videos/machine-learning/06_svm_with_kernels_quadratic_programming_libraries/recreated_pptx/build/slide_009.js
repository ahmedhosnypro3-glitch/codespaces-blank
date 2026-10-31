const pptxgen = require("pptxgenjs");
const fs = require("fs");

// Slide 009 — FRESH wave-3 rebuild from qa/reanalysis2/slide_009_analysis.txt ONLY.
// Spec: "Example" QP slide — three Minimize lines (green 0y^2 / red 0xy), boxed
// [x^T P x]+q^T x, P/q matrices, Subject-to constraints => Gx<=h form, and the
// right evaluation box (x=0, y=5, minimum value 20).
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_009.js

const NUM = 9;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = BASE + "/recreated_pptx/build/eq_009/";
const OUT = BASE + "/recreated_pptx/slide_009_recreated.pptx";

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
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Example", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- helpers: normalized spec coords [0..1] -> inches ----
const X = n => n * 13.33, Y = n => n * 7.5;
function img(name, x, y) {
  const m = JSON.parse(fs.readFileSync(EQ + name + ".png.json"));
  s.addImage({ path: EQ + name + ".png", x, y, w: m.w_in, h: m.h_in });
  return m;
}
function rect(x0, y0, x1, y1, fill, line, lw) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: line, width: lw || 1.25 },
  });
}

// ---- upper equation stack ----
img("m1", X(0.070), Y(0.128));
img("m2", X(0.286), Y(0.181));
img("m3", X(0.299), Y(0.246));
// pale-yellow boxed quadratic form [x^T P x] + q^T x
rect(0.692, 0.222, 0.935, 0.286, "FFFFE0", "000000", 0.75);
const bx = JSON.parse(fs.readFileSync(EQ + "boxed.png.json"));
img("boxed", X(0.692) + (X(0.935 - 0.692) - bx.w_in) / 2,
    Y(0.222) + (Y(0.286 - 0.222) - bx.h_in) / 2);

// ---- P and q matrices ----
img("P", X(0.381), Y(0.419));
img("q", X(0.449), Y(0.419));

// ---- red horizontal divider under the top block ----
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.043), y: Y(0.553), w: X(0.964 - 0.043), h: 0.012,
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});
// ---- "Subject to" header box + left constraint list ----
rect(0.060, 0.589, 0.161, 0.635, null, "C00000", 1.25);
s.addText("Subject to", {
  x: X(0.060), y: Y(0.589), w: X(0.35), h: Y(0.046),
  align: "left", valign: "middle",
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
const rowYs = [0.638, 0.668, 0.698, 0.728, 0.758];
["t1", "t2", "ge15", "t4", "t5"].forEach((n, i) => img(n, X(0.060), Y(rowYs[i])));

// ---- arrow + transformed constraint list ----
img("arrow", X(0.171), Y(0.704));
["t6", "t7", "t3", "t4", "t5"].forEach((n, i) => img(n, X(0.218), Y(rowYs[i])));

// ---- standard form: Gx <= h header + G / h matrices ----
img("gh", X(0.392), Y(0.589));
const g = img("G_rb3", X(0.358), Y(0.646));
img("h_rb3", X(0.358) + g.w_in + 0.12, Y(0.646));

// ---- vertical divider + red-bordered right evaluation box ----
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.557), y: Y(0.571), w: 0.012, h: Y(0.920 - 0.571),
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});
rect(0.567, 0.571, 0.981, 0.920, null, "C00000", 1.25);
s.addText("x=0, y=5", {
  x: X(0.578), y: Y(0.601), w: X(0.93 - 0.578), h: Y(0.041),
  align: "left", valign: "middle",
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
const chkYs = [0.664, 0.691, 0.718, 0.745, 0.772];
["c1", "c2", "c3", "c4", "c5"].forEach((n, i) => img(n, X(0.578), Y(chkYs[i])));
s.addText("Minimum value:", {
  x: X(0.578), y: Y(0.838), w: X(0.93 - 0.578), h: Y(0.034),
  align: "left", valign: "middle",
  fontSize: 12, italic: true, color: "0000CC", fontFace: FONT, margin: 0,
});
img("minv", X(0.578), Y(0.876));

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
