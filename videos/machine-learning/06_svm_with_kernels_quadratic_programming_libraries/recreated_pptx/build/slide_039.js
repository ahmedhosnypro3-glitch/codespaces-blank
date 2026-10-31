const pptxgen = require("pptxgenjs");
const path = require("path");
// Slide 039 — rebuild round 1 from qa/reanalysis2/slide_039_analysis.txt (spec starts
// at "1. SLIDE_TITLE"), with geometry re-measured from qa/rejudge2/orig_png/slide_039.png
// (960x540): blue frame [87,103]-[864,500], 9 text lines at measured y, main text x~116,
// sub text x~152. Mouse cursor is a capture artifact -> omitted (judge ground rule).
// Run from project root: node $NS/recreated_pptx/build/slide_039.js
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const W = 13.33, H = 7.5, FONT = "Arial";
const ix = v => v * W, iy = v => v * H;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome: outer red frame, badge + numeral 39, title box
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("39", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Bonus Assignment (SVM with Kernels)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Measured blue content frame [0.0906,0.1907,0.900,0.9259], white fill, blue stroke
s.addShape(pres.shapes.RECTANGLE, {
  x: ix(0.0906), y: iy(0.1907), w: ix(0.900 - 0.0906), h: iy(0.9259 - 0.1907),
  fill: { color: "FFFFFF" }, line: { color: "0000CC", width: 1.5 },
});

// One single-line text frame per measured line. Bullet lines carry the bullet option;
// continuation lines are plain so no second glyph appears.
function line(yNorm, xNorm, text, bulleted) {
  const opts = {
    x: ix(xNorm), y: iy(yNorm - 0.012), w: ix(0.895 - xNorm), h: iy(0.062),
    align: "left", valign: "top", fontSize: 17, color: "0000CC",
    fontFace: FONT, margin: 0,
  };
  if (bulleted) opts.bullet = { characterCode: "2022", indent: 14 };
  s.addText(text, opts);
}

line(0.246, 0.108, "Develop your own SVM library (from Scratch)", true);
line(0.326, 0.108, "You may use any Quadratic Programming solver (e.g. quadprog, CVXOPT, ..) to solve", true);
line(0.406, 0.121, "the Lagrangian Equation.", false);
line(0.485, 0.108, "Make use of Kernel functions (e.g. Quadratic , Polynomial, or RBF)", true);
line(0.565, 0.108, "For each of the given dataset (2-D):", true);
line(0.644, 0.145, "Draw the dataset points using color coding (assign same color to points belong to", true);
line(0.726, 0.158, "same class)", false);
line(0.802, 0.145, "Divide the background into grid, classify each point in the grid, give each point", true);
line(0.881, 0.158, "same color code of the class it belongs to.", false);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_039_recreated.pptx") })
  .then(() => console.log("wrote slide_039_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });
