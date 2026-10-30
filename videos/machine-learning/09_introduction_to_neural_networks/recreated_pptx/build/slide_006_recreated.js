// Pattern: house-chrome + slide 006 content (from slide_006_final.json)
// Build: NODE_PATH=$(npm root -g) node slide_006_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 6;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "F2F2F2" };

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

// 3. title (colored words: red + blue + red)
s.addText([
  { text: "Visualization of ", options: { color: "C00000", fontSize: 26, bold: true, fontFace: FONT } },
  { text: "Single Layer", options: { color: "0000FF", fontSize: 26, bold: true, fontFace: FONT } },
  { text: " Perceptron", options: { color: "C00000", fontSize: 26, bold: true, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "left", valign: "top", margin: 0,
});

// 4. EQUATION BOX (peach, left column upper) - 3 equations
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.8, y: 1.0, w: 5.2, h: 1.8,
  fill: { color: "FDEBD0" },
  line: { type: "none" },
  roundedCorner: true,
});
s.addText("d\u2081(X) = W\u2081\u1D40 X = w\u2081\u2081x\u2081 + w\u2081\u2082x\u2082 + ... + w\u2081\u2099x\u2099 + b\u2081 * 1", {
  x: 1.0, y: 1.15, w: 4.8, h: 0.35,
  align: "left", valign: "top",
  fontSize: 12, color: "000000", fontFace: FONT, margin: 0,
});
s.addText("d\u2082(X) = W\u2082\u1D40 X = w\u2082\u2081x\u2081 + w\u2082\u2082x\u2082 + ... + w\u2082\u2099x\u2099 + b\u2082 * 1", {
  x: 1.0, y: 1.55, w: 4.8, h: 0.35,
  align: "left", valign: "top",
  fontSize: 12, color: "000000", fontFace: FONT, margin: 0,
});
s.addText("d\u2098(X) = W\u2098\u1D40 X = w\u2098\u2081x\u2081 + w\u2098\u2082x\u2082 + ... + w\u2098\u2099x\u2099 + b\u2098 * 1", {
  x: 1.0, y: 1.95, w: 4.8, h: 0.35,
  align: "left", valign: "top",
  fontSize: 12, color: "000000", fontFace: FONT, margin: 0,
});

// 5. CLASSIFICATION LABEL (tan, left column middle-lower)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 3.0, w: 5.2, h: 0.55,
  fill: { color: "E6D5B8" },
  line: { type: "none" },
});
s.addText("Multi-Class Classification", {
  x: 0.8, y: 3.0, w: 5.2, h: 0.55,
  align: "center", valign: "middle",
  fontSize: 14, color: "5C4A2A", fontFace: FONT, margin: 0,
});

// 6. DIAGRAM (right side) with embedded graph
s.addImage({
  path: "slide_006_graph.png",
  x: 6.3, y: 1.0, w: 6.5, h: 5.2,
});

pres.writeFile({ fileName: "slide_006_recreated.pptx" }).then(() => console.log("wrote slide_006_recreated.pptx"));