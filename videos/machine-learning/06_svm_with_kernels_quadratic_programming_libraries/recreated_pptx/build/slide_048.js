const path = require("path");
const pptxgen = require("pptxgenjs");

// Slide 048 — rebuild fixing judge MAJORs (axes/ticks/labels absent).
// Pixel-measured original: gray panel w/ maroon border at capture
// [56,42,904,516]; white axes face [207,63,756,501]; x ticks 0..40 step 5,
// y ticks 0..35 step 5 (labels inside); black app bar y 519..540.
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
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13,
  align: "center", bold: true, color: "C00000", fontFace: "Arial", fontSize: 18,
});

// ---- plot panel — generated PNG in capture px of the original ----
s.addImage({
  path: __dirname + "/slide_048_graph_rb5.png",
  x: 58 / 960 * W, y: 42 / 540 * H,
  w: 844 / 960 * W, h: 476 / 540 * H,
});

// ---- bottom black app bar — capture y 519..540 ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 519 / 540 * H, w: W, h: (540 - 519) / 540 * H,
  fill: { color: "000000" }, line: { type: "none" },
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_048_recreated.pptx") })
  .then(() => console.log("wrote slide_048_recreated.pptx"))
  .catch((e) => console.error(e));
