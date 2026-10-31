const path = require("path");
const pptxgen = require("pptxgenjs");

// Slide 048 — fresh rebuild from qa/reanalysis2/slide_048_analysis.txt only.
// Spec: no title, no body text, no equations. One scatter plot on a white
// panel with red border: red outer ring, blue left-inner cluster, black
// right-inner cluster; x ticks 0..40, y ticks 0..35; black bottom app bar.
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 48;
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (mandatory, overrides spec) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
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
// Spec SLIDE_TITLE is none: title box kept at house position, no text added.
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13,
  align: "center", bold: true, color: "C00000", fontFace: "Arial", fontSize: 18,
});

// ---- plot panel (spec [0.227,0.122,0.974,0.967]) — generated PNG ----
const P = [0.227, 0.122, 0.974, 0.967];
s.addImage({
  path: __dirname + "/slide_048_graph_rb3.png",
  x: P[0] * W, y: P[1] * H,
  w: (P[2] - P[0]) * W, h: (P[3] - P[1]) * H,
});

// ---- bottom black app bar (spec [0.000,0.935,1.000,1.000]) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.935 * H, w: W, h: (1 - 0.935) * H,
  fill: { color: "000000" }, line: { type: "none" },
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_048_recreated.pptx") })
  .then(() => console.log("wrote slide_048_recreated.pptx"))
  .catch((e) => console.error(e));
