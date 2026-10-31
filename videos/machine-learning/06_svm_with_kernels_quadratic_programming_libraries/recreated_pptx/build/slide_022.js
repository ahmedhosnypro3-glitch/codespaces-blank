// slide_022.js — FRESH rebuild from qa/reanalysis2/slide_022_analysis.txt (rebuild wave 3)
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_022.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NUM = 22;
const TITLE = "Polynomial Kernel (of order 2)";
const W = 13.33, H = 7.5;
const SERIF = "Times New Roman";
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQDIR = path.join(NS, "recreated_pptx/build/eq_022");
const manifest = require(path.join(EQDIR, "manifest.json"));

// normalized spec coords [x0,y0,x1,y1] -> inches
const X = v => v * 13.33, Y = v => v * 7.5;
const box = r => ({ x: X(r[0]), y: Y(r[1]), w: (r[2] - r[0]) * 13.33, h: (r[3] - r[1]) * 7.5 });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec frame/badge/title)
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
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: SERIF, margin: 0,
});

// centered wide text line over a target center (lesson: WIDE box, h>=0.35)
function ctext(str, cxNorm, yNorm, hNorm, opt) {
  const cx = X(cxNorm), y = Y(yNorm), h = Math.max(Y(hNorm), 0.35);
  const w = Math.min(12.13, 2 * (cx - 0.05));
  s.addText(str, Object.assign({
    x: cx - w / 2, y, w, h,
    align: "center", valign: "middle",
    fontFace: SERIF, margin: 0,
  }, opt));
}
// left-aligned wide text line (lesson: left x=1.33 w=9.5, h>=0.35)
function ltext(str, lxNorm, yNorm, hNorm, opt) {
  const y = Y(yNorm), h = Math.max(Y(hNorm), 0.35);
  s.addText(str, Object.assign({
    x: Math.max(0.2, X(lxNorm) - 0.14), y, w: 9.5, h,
    align: "left", valign: "middle",
    fontFace: SERIF, margin: 0,
  }, opt));
}
// math PNG at natural size (w = px/600), centered in its spec box
function eq(name, r) {
  const b = box(r), m = manifest[name];
  s.addImage({
    path: m.path,
    x: b.x + (b.w - m.w_in) / 2, y: b.y + (b.h - m.h_in) / 2,
    w: m.w_in, h: m.h_in,
  });
}
// right-pointing arrow: red shaft + ISOSCELES_TRIANGLE head (rotated 90)
function arrow(r) {
  const b = box(r);
  const headW = Math.min(0.22, b.w * 0.45);
  const shaftH = Math.min(0.045, b.h * 0.3);
  s.addShape(pres.shapes.RECTANGLE, {
    x: b.x, y: b.y + b.h / 2 - shaftH / 2, w: b.w - headW, h: shaftH,
    fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
  });
  s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
    x: b.x + b.w - headW, y: b.y, w: headW, h: b.h, rotate: 90,
    fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
  });
}
function rect(r, fill, lineColor, lineW, rounded, dash) {
  const b = box(r);
  const opt = {
    x: b.x, y: b.y, w: b.w, h: b.h,
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: lineColor, width: lineW },
  };
  if (dash) opt.line.dashType = dash;
  s.addShape(rounded ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, opt);
}
