// Slide 26 attempt 1: fix vs certified build — title RED (spec #c00000, measured
// #B41929), BOTH subtitle lines BLUE (spec #0000cc, measured ~#3232BE), positions
// matched to original frame (sub1 y4.00-4.42, sub2 y4.72-5.14). House title at y=0.28.
const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const NUM = 26;
const FONT = "Times New Roman";

let s = pres.addSlide();
s.background = { color: "E8E8E8" };

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
s.addText("Solved Example", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("[ Update Weights of Output Layer and Hidden Layer ]", {
  x: 0.6, y: 4.00, w: 12.13, h: 0.42,
  align: "center", valign: "middle",
  fontSize: 28, color: "3232BE", fontFace: FONT, margin: 0,
});
s.addText("Using one training sample", {
  x: 0.6, y: 4.72, w: 12.13, h: 0.42,
  align: "center", valign: "middle",
  fontSize: 28, color: "3232BE", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "slide_026_attempt1.pptx" })
  .then(() => console.log("wrote slide_026_attempt1.pptx"));
