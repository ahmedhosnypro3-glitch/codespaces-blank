const pptxgen = require("pptxgenjs");

// slide_040.js — FRESH build from qa/reanalysis2/slide_040_analysis.txt only
// (spec starts at "1. SLIDE_TITLE"): "Check class of each background point in the
// following datasets" — six SIPU/UEF benchmark scatter panels + label boxes.
// Build from project root:
//   cd /home/codespace/ai_llm_slides && node <NS>/recreated_pptx/build/slide_040.js

const path = require("path");
const NUM = 40;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const BUILD = __dirname;

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
s.addText("Check class of each background point in the following datasets", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- helpers: normalized [x0,y0,x1,y1] -> inches ----
const box = r => ({ x: r[0] * 13.33, y: r[1] * 7.5, w: (r[2] - r[0]) * 13.33, h: (r[3] - r[1]) * 7.5 });

// blue-bordered white label box, italic 12pt centered black text (spec sec 4/7)
function label(r, text) {
  const b = box(r);
  s.addShape(pres.shapes.RECTANGLE, {
    x: b.x, y: b.y, w: b.w, h: b.h,
    fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 },
  });
  s.addText(text, {
    x: b.x, y: b.y, w: b.w, h: b.h,
    align: "center", valign: "middle", margin: 0,
    fontSize: 12, italic: true, color: "000000", fontFace: FONT,
  });
}

pres.writeFile({ fileName: require("path").join("/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries", "recreated_pptx/slide_040_recreated.pptx") });

// scatter panel: 600-dpi PNG placed at exact pixel size w=px/600, h=py/600 (never rescaled)
function plot(r, png, pw, ph) {
  const b = box(r);
  s.addImage({ path: path.join(BUILD, png), x: b.x, y: b.y, w: pw / 600, h: ph / 600 });
}

// ---- label boxes (spec section 4; brief items 4-9) ----
label([0.15, 0.21, 0.27, 0.25], "Aggregation.txt");
label([0.42, 0.21, 0.55, 0.25], "Compound.txt");
label([0.70, 0.21, 0.83, 0.25], "Spiral.txt");
label([0.15, 0.57, 0.27, 0.61], "Pathbased.txt");
label([0.42, 0.57, 0.55, 0.61], "Flame.txt");
label([0.70, 0.57, 0.83, 0.61], "Jain.txt");

// ---- scatter plots (spec section 4 plot regions; brief items 10-15) ----
plot([0.11, 0.26, 0.31, 0.52], "slide_040_graph_Aggregation.png", 1599, 1170);
plot([0.39, 0.26, 0.58, 0.52], "slide_040_graph_Compound.png", 1519, 1170);
plot([0.67, 0.26, 0.86, 0.52], "slide_040_graph_Spiral.png", 1519, 1170);
plot([0.11, 0.62, 0.31, 0.88], "slide_040_graph_Pathbased.png", 1599, 1170);
plot([0.39, 0.62, 0.58, 0.88], "slide_040_graph_Flame.png", 1519, 1170);
plot([0.67, 0.62, 0.86, 0.88], "slide_040_graph_Jain.png", 1519, 1170);

// ---- cursor arrow at [0.56,0.56,0.58,0.58], black (spec section 4; brief item 16) ----
const a = box([0.56, 0.56, 0.58, 0.58]);
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: a.x, y: a.y, w: a.w, h: a.h,
  fill: { color: "000000" }, line: { color: "000000", width: 0.5 },
  rotate: -45,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_040_recreated.pptx") })
  .then(() => console.log("wrote slide_040_recreated.pptx"))
  .catch(e => console.error(e));
