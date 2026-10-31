// slide_027.js — "Polynomial Kernel" (REBUILD WAVE 3, from qa/reanalysis2/slide_027_analysis.txt only)
// Build from project root: cd /home/codespace/ai_llm_slides && NODE_PATH=$(npm root -g) node <NS>/recreated_pptx/build/slide_027.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_027") + "/";
const W = 13.33, H = 7.5;
const MATH = "Times New Roman";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome (mandatory, overrides spec)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("27", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
s.addText("Polynomial Kernel", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: MATH, margin: 0,
});

// normalized spec box -> inches
const bx = (x0, y0, x1, y1) => ({ x: x0 * W, y: y0 * H, w: (x1 - x0) * W, h: (y1 - y0) * H });
const meta = (n) => require(EQ + n + ".png.json");
// image at exact native size (px/600), centered in spec box
const imgC = (n, x0, y0, x1, y1) => {
  const m = meta(n), b = bx(x0, y0, x1, y1);
  s.addImage({ path: EQ + n + ".png", x: b.x + (b.w - m.w_in) / 2, y: b.y + (b.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
};
// image at exact native size, left-aligned in spec box
const imgL = (n, x0, y0, x1, y1) => {
  const m = meta(n), b = bx(x0, y0, x1, y1);
  s.addImage({ path: EQ + n + ".png", x: b.x, y: b.y + (b.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
};

// inner light-blue content frame (sharp corners), capped inside the house red frame
const f = bx(0.028, 0.185, 0.992, 0.988);
s.addShape(pres.shapes.RECTANGLE, {
  x: f.x, y: f.y, w: Math.min(f.w, 13.18 - f.x), h: Math.min(f.h, 7.35 - f.y),
  fill: { type: "none" }, line: { color: "7BA7D9", width: 1 },
});

// vector boxes a and b with stacked components
for (const [lbl, x0, x1, imgn] of [["a", 0.060, 0.130, "eq_veca"], ["b", 0.138, 0.208, "eq_vecb"]]) {
  const b = bx(x0, 0.203, x1, 0.272);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "DAE3F3" }, line: { color: "1F4E79", width: 1 },
  });
  s.addText(lbl, {
    x: b.x, y: b.y, w: 0.34, h: b.h, align: "center", valign: "middle",
    fontSize: 20, italic: true, color: "C00000", fontFace: MATH, margin: 0,
  });
  const m = meta(imgn);
  s.addImage({ path: EQ + imgn + ".png", x: b.x + 0.36, y: b.y + (b.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
}

// gray highlight panel behind the Remember line
const rp = bx(0.295, 0.207, 0.810, 0.257);
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: rp.x, y: rp.y, w: rp.w, h: rp.h,
  fill: { color: "E7E6E6" }, line: { type: "none" },
});
imgL("eq_remember", 0.300, 0.212, 0.805, 0.252);
imgL("eq_label", 0.095, 0.338, 0.335, 0.368);

// tan kernel boxes
for (const [x0, y0, x1, y1, imgn] of [[0.063, 0.372, 0.185, 0.430, "eq_tan1"], [0.063, 0.528, 0.183, 0.585, "eq_tan2"]]) {
  const b = bx(x0, y0, x1, y1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: b.x, y: b.y, w: b.w, h: b.h, fill: { color: "FBE4D5" }, line: { color: "C55A11", width: 1.25 },
  });
  imgC(imgn, x0, y0, x1, y1);
}

imgL("eq_exp1", 0.185, 0.378, 0.995, 0.425);
imgL("eq_exp2", 0.188, 0.428, 0.995, 0.470);
// phi(a)^T row sits in the bottom block, between the tan box and the phi(b) column
imgL("eq_strip", 0.195, 0.540, 0.395, 0.600);
imgC("eq_phib", 0.398, 0.495, 0.472, 0.672);
imgL("eq_phimap", 0.480, 0.505, 0.695, 0.560);
imgL("eq_where", 0.500, 0.575, 0.680, 0.615);
imgC("eq_phix", 0.698, 0.495, 0.800, 0.672);
imgL("eq_2d6d", 0.835, 0.618, 0.940, 0.652);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_027_recreated.pptx") })
  .then(() => console.log("wrote slide_027_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });
