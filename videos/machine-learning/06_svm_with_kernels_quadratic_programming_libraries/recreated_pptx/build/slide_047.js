// slide_047.js — REBUILD WAVE 3, built ONLY from qa/reanalysis2/slide_047_analysis.txt
// Spec: no printed title; badge "47"; full-slide scatter plot (x 0-35 step 5,
// y -10..40 step 10; gray dot lattice + blue/red/black spiral arms) rendered as
// a generated matplotlib PNG (gen_slide_047_graph_rb3.py -> slide_047_graph_rb3.png).
// Build from project root: node <NS>/recreated_pptx/build/slide_047.js
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 47;
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome: outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// House chrome: slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4" },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// House chrome: title box (spec has no printed title -> empty text, geometry kept)
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Full-slide generated plot (transparent PNG over the gray slide background)
s.addImage({
  path: path.join(NS, "recreated_pptx/build/slide_047_graph_rb4.png"),
  x: 0, y: 0, w: W, h: H,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_047_recreated.pptx") })
  .then(() => console.log("wrote slide_047_recreated.pptx"))
  .catch((err) => console.error(err));
