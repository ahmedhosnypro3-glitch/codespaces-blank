// Pattern: house-chrome + slide 008 content (from slide_008_final.json)
// Build: NODE_PATH=$(npm root -g) node slide_008_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 8;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E6E6E6" };

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

// 3. title (single line: red + blue + red)
s.addText([
  { text: "Multi-Class Classification using ", options: { color: "C0392B", fontSize: 28, bold: true, fontFace: FONT } },
  { text: "[ONE VS ALL]", options: { color: "21618C", fontSize: 28, bold: true, fontFace: FONT } },
  { text: " Binary Classifiers", options: { color: "C0392B", fontSize: 28, bold: true, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

// 4. PLOT FRAME with embedded graph
s.addImage({
  path: "slide_008_graph.png",
  x: 1.5, y: 1.2, w: 9.0, h: 5.3,
});

// 5. Plot frame border (red)
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.5, y: 1.2, w: 9.0, h: 5.3,
  fill: { type: "none" },
  line: { color: "C0392B", width: 1 },
});

// 6. "Undefined" box (top-left, outside plot) with leader lines
// Drawn in the graph but also added as native shapes for editability
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.25, y: 1.3, w: 1.0, h: 0.4,
  fill: { color: "D5F5E3" },
  line: { color: "000000", width: 1 },
});
s.addText("Undefined", {
  x: 0.25, y: 1.3, w: 1.0, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 11, color: "000000", fontFace: FONT, margin: 0,
});
// Leader lines from Undefined box to plot
s.addShape(pres.shapes.LINE, {
  x: 1.25, y: 1.5, w: 0.25, h: 0.5,
  line: { color: "C0392B", width: 0.75 },
});
s.addShape(pres.shapes.LINE, {
  x: 1.25, y: 1.6, w: 0.35, h: 0.8,
  line: { color: "C0392B", width: 0.75 },
});

// 7. "New Class" box (middle-right, outside plot)
s.addShape(pres.shapes.RECTANGLE, {
  x: 11.0, y: 3.5, w: 1.2, h: 0.4,
  fill: { color: "D7BDE2" },
  line: { color: "8E44AD", width: 1.2 },
});
s.addText("New Class", {
  x: 11.0, y: 3.5, w: 1.2, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 11, color: "000000", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "slide_008_recreated.pptx" }).then(() => console.log("wrote slide_008_recreated.pptx"));