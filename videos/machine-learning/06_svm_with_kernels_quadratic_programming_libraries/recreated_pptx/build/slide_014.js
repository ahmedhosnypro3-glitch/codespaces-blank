const pptxgen = require("pptxgenjs");

// Slide 014 — built FRESH from qa/reanalysis2/slide_014_analysis.txt only.
// Spec: title-only slide; no equations, no plots, no other body text.
const NUM = 14;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House outer red frame (house rule overrides spec geometry)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. House badge: yellow circle + numeral
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title (spec VERBATIM_TEXT / SLIDE_TITLE, two lines, red bold centered)
//    Spec: "Mapping non-linearly Separable Data to Higher Dimensions",
//    bold, #C00000, sans-serif, centered, ~30pt.
s.addText("Mapping non-linearly Separable Data\nto Higher Dimensions", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.3,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: "C00000", fontFace: FONT, margin: 0,
  lineSpacing: 38,
});

// 4. Lower two-thirds intentionally blank (spec RECREATION_BRIEF item 6).

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_014_recreated.pptx" })
  .then(() => console.log("wrote slide_014_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
