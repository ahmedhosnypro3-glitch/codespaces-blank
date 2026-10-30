// Pattern: house-chrome + slide 005 content (from slide_005_final.json)
// Build: NODE_PATH=$(npm root -g) node slide_005_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 5;
const TITLE = "Visualization of Single Perceptron";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "F0F0F0" };

// 1. outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. title box
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. TOP-LEFT VECTOR BOX (x=9%-42%, y=13%-45%)
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.2, y: 0.98, w: 4.39, h: 2.4,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
// column vector X = [x1; x2; ...; xn]
s.addText([
  { text: "X = ", options: { color: "000000", fontSize: 16, fontFace: FONT, italic: true } },
  { text: "[", options: { color: "000000", fontSize: 22, fontFace: FONT, bold: true } },
], {
  x: 1.35, y: 1.15, w: 4.0, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "x\u2081;\n x\u2082;\n ...\n x\u2099", options: { color: "000000", fontSize: 14, fontFace: FONT, italic: true } },
], {
  x: 1.95, y: 1.35, w: 1.0, h: 0.9,
  align: "left", valign: "top", margin: 0, lineSpacing: 13,
});
s.addText("]", {
  x: 2.95, y: 1.15, w: 0.3, h: 0.3,
  align: "left", valign: "top",
  fontSize: 22, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
// arrow
s.addText("\u2192", {
  x: 3.35, y: 1.6, w: 0.5, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
// augmented vector X = [1; x1; x2; ...; xn]
s.addText([
  { text: "X = ", options: { color: "000000", fontSize: 16, fontFace: FONT, italic: true } },
  { text: "[", options: { color: "000000", fontSize: 22, fontFace: FONT, bold: true } },
], {
  x: 3.9, y: 1.15, w: 1.6, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "1;\n x\u2081;\n x\u2082;\n ...\n x\u2099", options: { color: "000000", fontSize: 14, fontFace: FONT, italic: true } },
], {
  x: 4.45, y: 1.35, w: 1.0, h: 1.1,
  align: "left", valign: "top", margin: 0, lineSpacing: 13,
});
s.addText("]", {
  x: 5.45, y: 1.15, w: 0.3, h: 0.3,
  align: "left", valign: "top",
  fontSize: 22, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
// Augmented Vector label
s.addText("Augmented Vector", {
  x: 1.35, y: 2.95, w: 4.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, color: "0000FF", fontFace: FONT, italic: true, margin: 0,
});

// 5. TOP-RIGHT VECTOR BOX (x=46%-80%, y=13%-45%)
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.13, y: 0.98, w: 4.53, h: 2.4,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
s.addText([
  { text: "W = ", options: { color: "000000", fontSize: 16, fontFace: FONT, italic: true } },
  { text: "[", options: { color: "000000", fontSize: 22, fontFace: FONT, bold: true } },
], {
  x: 6.3, y: 1.15, w: 0.6, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "b;\n w\u2081;\n w\u2082;\n ...\n w\u2099", options: { color: "000000", fontSize: 14, fontFace: FONT, italic: true } },
], {
  x: 6.9, y: 1.35, w: 1.0, h: 1.1,
  align: "left", valign: "top", margin: 0, lineSpacing: 13,
});
s.addText("]", {
  x: 7.9, y: 1.15, w: 0.3, h: 0.3,
  align: "left", valign: "top",
  fontSize: 22, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
// Model Weights label
s.addText("Model Weights", {
  x: 8.3, y: 1.6, w: 2.2, h: 0.4,
  align: "left", valign: "middle",
  fontSize: 14, color: "0000FF", fontFace: FONT, italic: true, margin: 0,
});

// 6. MIDDLE EQUATION BOX (x=9%-80%, y=48%-62%)
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.2, y: 3.6, w: 9.46, h: 1.05,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
// equation: d(X) = WᵀX = w₁x₁ + w₂x₂ + ... + wₙxₙ + b*1
s.addText("d(X) = W\u1D40 X = w\u2081x\u2081 + w\u2082x\u2082 + ...... + w\u2099x\u2099 + b*1", {
  x: 1.35, y: 3.75, w: 6.5, h: 0.4,
  align: "left", valign: "top",
  fontSize: 16, color: "000000", fontFace: FONT, margin: 0,
});
// classification cases with right brace
s.addText("}", {
  x: 8.6, y: 3.7, w: 0.4, h: 0.9,
  align: "center", valign: "middle",
  fontSize: 40, color: "000000", fontFace: FONT, margin: 0,
});
s.addText(">0 \u21D2 Class I\n<0 \u21D2 Class II\n=0 \u21D2 Undefined Class", {
  x: 9.0, y: 3.7, w: 1.6, h: 0.9,
  align: "left", valign: "top",
  fontSize: 11, color: "000000", fontFace: FONT, margin: 0, lineSpacing: 13,
});

// 7. BOTTOM-LEFT DIAGRAM BOX (x=24%-64%, y=64%-94%) with embedded graph
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.2, y: 4.8, w: 5.33, h: 2.25,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
s.addImage({
  path: "slide_005_graph.png",
  x: 3.25, y: 4.85, w: 5.23, h: 2.15,
});

// 8. BOTTOM-RIGHT CAPTION (x=66%-85%, y=74%-82%)
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.8, y: 5.55, w: 2.53, h: 0.6,
  fill: { color: "E8E0C8" },
  line: { type: "none" },
});
s.addText("Binary Classification (2 Classes)", {
  x: 8.85, y: 5.55, w: 2.43, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "slide_005_recreated.pptx" }).then(() => console.log("wrote slide_005_recreated.pptx"));