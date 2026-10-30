// Pattern: house-chrome + slide 002 content (from slide_002_final.json)
// Build: NODE_PATH=$(npm root -g) node slide_002_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 2;
const TITLE_LINE1 = "Revision of";
const TITLE_LINE2 = "Perceptron Algorithm";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };  // house template background

// 1. outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
// Judge: original title ~38% and ~52% vertical, two lines
s.addText(TITLE_LINE1, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText(TITLE_LINE2, {
  x: 0.6, y: 0.85, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. BOTTOM BLACK BAR - video player strip (from original frame capture)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.0, y: H - 0.2, w: W, h: 0.2,
  fill: { color: "000000" },
  line: { type: "none" },
});

pres.writeFile({ fileName: "slide_002_recreated.pptx" }).then(() => console.log("wrote slide_002_recreated.pptx"));