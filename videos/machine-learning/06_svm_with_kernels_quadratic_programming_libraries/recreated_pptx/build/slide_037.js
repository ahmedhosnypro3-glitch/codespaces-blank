// slide_037.js — FRESH rebuild (wave 3) from qa/reanalysis2/slide_037_analysis.txt only.
// "How to Kernelize SVM" / Example: Polynomial Kernel. House chrome per NS AGENTS.md.
// Run: NODE_PATH=$(npm root -g) node slide_037.js
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const NUM = 37;
const TITLE = "How to Kernelize SVM";
const W = 13.33, H = 7.5;
const EQ = path.join(__dirname, "eq_037");
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_037_recreated.pptx";
const manifest = JSON.parse(fs.readFileSync(path.join(EQ, "eq_rb3_manifest.json"), "utf8"));
const SERIF = "Times New Roman";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// normalized [x0,y0,x1,y1] -> inches
const N = (x0, y0, x1, y1) => ({ x: x0 * 13.33, y: y0 * 7.5, w: (x1 - x0) * 13.33, h: (y1 - y0) * 7.5 });

function rbox(b, fill, lineColor) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(N.apply(null, b), {
    fill: { color: fill }, line: { color: lineColor, width: 1 },
  }));
}

// spec section 3/4: four rounded boxes + example label box
rbox([0.07, 0.07, 0.93, 0.16], "FFFFFF", "00008B");
rbox([0.07, 0.17, 0.93, 0.45], "F5F5F5", "00008B");
rbox([0.07, 0.49, 0.93, 0.61], "E0E0E0", "00008B");
rbox([0.07, 0.62, 0.93, 0.93], "F5F5F5", "00008B");
s.addShape(pres.shapes.RECTANGLE, Object.assign(N(0.08, 0.08, 0.35, 0.14), {
  fill: { type: "none" }, line: { color: "00008B", width: 1 },
}));

// green formula highlights
const HL = [
  [0.1, 0.2, 0.2, 0.25], [0.1, 0.3, 0.2, 0.35], [0.3, 0.3, 0.5, 0.35],
  [0.6, 0.3, 0.8, 0.35], [0.4, 0.4, 0.7, 0.45], [0.4, 0.5, 0.75, 0.55],
  [0.1, 0.64, 0.2, 0.69], [0.1, 0.73, 0.2, 0.78], [0.3, 0.73, 0.5, 0.78],
  [0.6, 0.73, 0.8, 0.78], [0.4, 0.83, 0.7, 0.88],
];
HL.forEach(b => s.addShape(pres.shapes.RECTANGLE, Object.assign(N.apply(null, b), {
  fill: { color: "90EE90" }, line: { type: "none" },
})));

// red arrow: top box -> middle box
s.addShape(pres.shapes.RIGHT_ARROW, Object.assign(N(0.45, 0.48, 0.55, 0.55), {
  fill: { color: "FF0000" }, line: { type: "none" },
}));

// spec text lines (wide boxes per slide-001 lesson; left lines x=0.10*13.33 w=9.5)
s.addText("Example: Polynomial Kernel", {
  x: 1.333, y: 0.6, w: 9.5, h: 0.45,
  align: "left", valign: "middle", fontSize: 12, color: "000000", fontFace: SERIF, margin: 0,
});
s.addText("Kernelize using", {
  x: 5.332, y: 3.75, w: 1.9, h: 0.375,
  align: "left", valign: "middle", fontSize: 12, color: "000000", fontFace: SERIF, margin: 0,
});
// spec section 8: equations as 600-dpi mathtext PNGs at exact size (w=px/600),
// centered in their spec boxes; the kernel equation sits right of "Kernelize using"
function eq(name, boxOverride, pinX) {
  const m = manifest[name];
  const b = boxOverride || m.box;
  const x = pinX !== undefined ? pinX : b[0] + (b[2] - m.w_in) / 2;
  const y = b[1] + (b[3] - m.h_in) / 2;
  s.addImage({ path: path.join(EQ, m.image), x, y, w: m.w_in, h: m.h_in });
}
eq("eq_rb3_lag_orig");
eq("eq_rb3_w");
eq("eq_rb3_b_orig");
eq("eq_rb3_class_orig");
eq("eq_rb3_kernel", null, 5.332 + 4.6655 - manifest.eq_rb3_kernel.w_in - 0.1);
eq("eq_rb3_lag_kern");
eq("eq_rb3_w", [1.333, 5.475, 2.666, 0.375]);
eq("eq_rb3_b_kern");
eq("eq_rb3_class_kern");

// house chrome (mandatory, drawn last so it stays on top)
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
  fontSize: 24, bold: true, color: "C00000", fontFace: "Arial", margin: 0,
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(err => { console.error(err); process.exit(1); });
