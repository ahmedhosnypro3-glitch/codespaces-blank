// Build slide 025: Linear and Unit Step Activation Functions (badge 17)
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E6E6E6" };
const FONT = "Arial";

// ---- HOUSE CHROME (laws from pattern) ----
// 1. Outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("17", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box
s.addText("Linear and Unit Step Activation Functions", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- SLIDE CONTENT ----

// Top-center graph: Linear (F(x) = x)
s.addImage({
  path: "slide_025_linear.png",
  x: 1.2, y: 1.0, w: 3.5, h: 2.5,
});

// Top-right: Red X and Linear equation box
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.5, y: 1.0, w: 4.0, h: 2.5,
  fill: { color: "FFE6CC" },
  line: { color: "C00000", width: 1 },
});
s.addText("F(x) = x", {
  x: 5.5, y: 1.1, w: 4.0, h: 0.5,
  align: "center", fontSize: 16, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
s.addText("Linear (No Activation)", {
  x: 5.5, y: 1.7, w: 4.0, h: 0.5,
  align: "center", fontSize: 14, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
});
// Red X mark
s.addText("✕", {
  x: 7.0, y: 0.5, w: 1.0, h: 0.5,
  align: "center", fontSize: 48, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
});

// Bottom-left graph: Unipolar Unit Step
s.addImage({
  path: "slide_025_unipolar_step.png",
  x: 1.2, y: 4.0, w: 3.5, h: 2.5,
});

// Bottom-left equation box
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.2, y: 6.6, w: 3.5, h: 0.6,
  fill: { color: "FFE6CC" },
  line: { color: "C00000", width: 1 },
});
s.addText("F(x) = Uni-polar Unit Step = { 0 for x<0 ; 1 for x ≥ 0 }", {
  x: 1.2, y: 6.6, w: 3.5, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 12, color: "008000", fontFace: FONT, margin: 0,
});

// Bottom-right graph: Bipolar Unit Step
s.addImage({
  path: "slide_025_bipolar_step.png",
  x: 5.5, y: 4.0, w: 3.5, h: 2.5,
});

// Bottom-right equation box
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.5, y: 6.6, w: 3.5, h: 0.6,
  fill: { color: "FFE6CC" },
  line: { color: "C00000", width: 1 },
});
s.addText("F(x) = Bi-polar Unit Step = { -1 for x<0 ; 1 for x ≥ 0 }", {
  x: 5.5, y: 6.6, w: 3.5, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 12, color: "008000", fontFace: FONT, margin: 0,
});

const outPath = "slide_025_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));