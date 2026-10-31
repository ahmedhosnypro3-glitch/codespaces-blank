// slide_054.js — rebuilt from qa/reanalysis2/slide_054_analysis.txt (spec section 1+)
// and web_sources/slide_054/SOURCES.md. Data-only frame: no title, no legend, no
// axis titles. 4x4 checkerboard of 2x2 red/blue dot clusters on 0..25 axes inside a
// white plot box with light-red border, black left/bottom spines, tick labels
// 0,5,10,15,20,25. Plot art comes from slide_054_graph.png (pixel-extracted from the
// original frame, 64/64 dot color parity, no legend/axis titles added).
const path = require("path");
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "rb2-054";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome: outer red frame.
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
// House chrome: slide-number badge "54".
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("54", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
// House chrome: title box (spec SLIDE_TITLE is "none" — left empty, no invented text).
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: "Arial", margin: 0,
});

// Plot panel: original white plot box x 206..753, y 64..501 in the 960x540 frame.
const PX0 = 206 / 960, PY0 = 64 / 540, PX1 = 753 / 960, PY1 = 501 / 540;
s.addImage({
  path: path.join(__dirname, "slide_054_graph.png"),
  x: PX0 * W, y: PY0 * H,
  w: (PX1 - PX0) * W, h: (PY1 - PY0) * H,
});

pres.writeFile({ fileName: require("path").join(NS, "recreated_pptx/slide_054_recreated.pptx") })
  .then(() => console.log("wrote slide_054_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
