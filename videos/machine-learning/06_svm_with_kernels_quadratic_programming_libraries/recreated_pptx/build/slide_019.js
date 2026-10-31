// slide_019.js — FRESH rebuild (wave 3) from qa/reanalysis2/slide_019_analysis.txt ONLY.
// Spec coords [x0,y0,x1,y1] normalized -> inches: x*13.33, y*7.5.
// Build from project root: node <NS>/recreated_pptx/build/slide_019.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const BUILD = NS + "/recreated_pptx/build";
const eq = JSON.parse(fs.readFileSync(BUILD + "/eq_019/eq19_kernel_rb2.png.json", "utf8"));
const W = 13.33, H = 7.5;
const ARIAL = "Arial", SERIF = "Times New Roman";
const X = v => v * 13.33, Y = v => v * 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec geometry): red frame, badge, title box
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("19", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: ARIAL, margin: 0,
});
s.addText("Kernels", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: ARIAL, margin: 0,
});

// Spec: faint top rule (placed just above the house title box)
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.059), y: 0.24, w: X(0.905 - 0.059), h: 0.02,
  fill: { color: "E6E6E6" }, line: { type: "none" },
});

// Spec: inner blue rectangle around the bullets [0.068,0.172,0.852,0.837]
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.068), y: Y(0.172), w: X(0.852 - 0.068), h: Y(0.837 - 0.172),
  fill: { type: "none" }, line: { color: "0000CC", width: 1.5 },
});

// Six small round navy bullet markers at x ~ 0.087 (judge: original has round bullets)
[0.216, 0.317, 0.443, 0.631, 0.690, 0.786].forEach(y =>
  s.addShape(pres.shapes.OVAL, {
    x: X(0.087), y: Y(y), w: 0.09, h: 0.09,
    fill: { color: "000080" }, line: { type: "none" },
  })
);

// Body text: spec boxes -> inches, Times 15pt black unless run overrides
function body(x0, y0, x1, y1, runs) {
  s.addText(runs, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fontSize: 15, fontFace: SERIF, color: "000000",
    margin: 0, valign: "top", lineSpacingMultiple: 1.0,
  });
}
const blk = t => ({ text: t, options: { color: "000000" } });
const red = t => ({ text: t, options: { color: "CC0000" } });
const redBold = t => ({ text: t, options: { bold: true, color: "CC0000" } });
const redU = t => ({ text: t, options: { color: "CC0000", underline: { style: "sng" } } });
const blueIt = t => ({ text: t, options: { italic: true, color: "0000CC" } });
const brk = r => Object.assign({}, r, { options: Object.assign({}, r.options, { breakLine: true }) });

// Bullet 1 [0.082,0.196,0.731,0.238]: bold red "dot product of two vectors"
body(0.082, 0.196, 0.731, 0.238, [
  blk("Kernels Represent a "),
  redBold("dot product of two vectors"),
  blk(" in a higher dimensional feature space"),
]);

// Bullet 2 [0.082,0.298,0.758,0.337]
body(0.082, 0.298, 0.758, 0.337, [
  blk("Any Machine Learning Model that contains dot product of input samples can be kernelized"),
]);

// Bullet 3 [0.082,0.402,0.851,0.494]: two lines, red underlined clause
body(0.082, 0.402, 0.851, 0.494, [
  blk("Instead of calculating dot product between input vectors, "),
  brk(redU("calculate dot product between input")),
  redU("vectors after mapping them to higher dimensional space"),
]);
// Equation image [0.122,0.530,0.762,0.587]: certified 600dpi mathtext PNG at exact size
const eqBoxW = X(0.762 - 0.122), eqBoxH = Y(0.587 - 0.530);
s.addImage({
  path: eq.path,
  x: X(0.122) + (eqBoxW - eq.w_in) / 2,
  y: Y(0.530) + (eqBoxH - eq.h_in) / 2,
  w: eq.w_in,
});

// Bullet 4 [0.082,0.613,0.613,0.652]
body(0.082, 0.613, 0.613, 0.652, [
  blk("Different Kernel functions are based on different mapping functions"),
]);

// Bullet 5 [0.082,0.667,0.845,0.752]: two lines, blue italic
body(0.082, 0.667, 0.845, 0.752, [
  brk(blueIt("Calculations of mapping and calculations of dot product in higher dimensional space are very")),
  blueIt("expensive."),
]);

// Bullet 6 [0.082,0.770,0.610,0.811]: bold red "Kernel Trick"
body(0.082, 0.770, 0.610, 0.811, [
  blk("Use "), redBold("Kernel Trick"),
  blk(" to minimize both calculations (at no extra cost)"),
]);

// Spec pointer arrow [0.267,0.226,0.283,0.261] is a mouse-cursor artifact [?] — omitted

// Spec: solid black band across the bottom [0.039,0.867,0.904,1.000] (drawn last)
s.addShape(pres.shapes.RECTANGLE, {
  x: X(0.039), y: Y(0.867), w: X(0.904 - 0.039), h: Y(1.0 - 0.867),
  fill: { color: "000000" }, line: { type: "none" },
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_019_recreated.pptx") })
  .then(() => console.log("wrote slide_019_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
