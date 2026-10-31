const pptxgen = require("pptxgenjs");

// Slide 048 — fresh build from qa/reanalysis2/slide_048_analysis.txt only.
// Spec: no title, no body text, no equations; one scatter plot (red ring,
// blue left cluster, black right cluster) on a white panel with a red border.
// Plot region measured from the original frame: panel x 207..757, y 64..501
// of a 960x540 capture -> normalized [0.2156, 0.1185, 0.7885, 0.9278].
const NUM = 48;
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

// ---- plot (spec sections 4-5): generated PNG at measured panel region ----
const PX0 = 207 / 960, PY0 = 64 / 540, PX1 = 757 / 960, PY1 = 501 / 540;
s.addImage({
  path: __dirname + "/slide_048_graph.png",
  x: PX0 * W, y: PY0 * H,
  w: (PX1 - PX0) * W, h: (PY1 - PY0) * H,
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_048_recreated.pptx" })
  .then(() => console.log("wrote slide_048_recreated.pptx"))
  .catch(e => console.error(e));
