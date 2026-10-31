const pptxgen = require("pptxgenjs");

// Slide 043 — FRESH build from qa/reanalysis2/slide_043_analysis.txt only.
// Spec: no title, no body text, no equations. One scatter plot with 7 colored
// clusters, gray axes, dotted #C0C0C0 grid, y labels 40..-10, x labels 0..40.
// Plot area [0.23,0.14,0.76,0.82]; labels span [0.20,0.12,0.76,0.87]; all
// rendered into one real matplotlib PNG (slide_043_graph.png).
const NUM = 43;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (mandatory, overrides spec) ----
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
// House title box (spec SLIDE_TITLE: none — box kept, no text added).
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- plot (spec sections 2-5): generated PNG covering labels + plot area ----
// Region [0.20, 0.12, 0.76, 0.87] normalized -> inches; PNG is 1492x1125 @200dpi.
const GX0 = 0.20, GY0 = 0.12, GX1 = 0.76, GY1 = 0.87;
s.addImage({
  path: __dirname + "/slide_043_graph.png",
  x: GX0 * W, y: GY0 * H,
  w: (GX1 - GX0) * W, h: (GY1 - GY0) * H,
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_043_recreated.pptx" })
  .then(() => console.log("wrote slide_043_recreated.pptx"))
  .catch(e => console.error(e));
