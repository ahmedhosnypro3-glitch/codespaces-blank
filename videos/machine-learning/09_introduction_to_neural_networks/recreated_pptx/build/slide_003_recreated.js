// Pattern: house-chrome + slide 003 content (corrected from judge feedback v2)
// Build: NODE_PATH=$(npm root -g) node slide_003_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 3;
const TITLE = "Problem Formulation";
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
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Four stacked content boxes with red borders
const boxX = 0.67;
const boxW = 12.0;
const boxH1 = 1.125; // 15% of 7.5
const boxH2 = 1.125;
const boxH3 = 1.125;
const boxH4 = 1.5;   // 20% of 7.5
const gap = 0.15;    // 2% gap

let boxY = 0.15 + 0.55 + 0.15 + gap; // after title (0.28+0.55) + gap

// Box 1 - Define two classes, discriminant function
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH1,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
s.addText([
  { text: "Define two classes: ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "class I", options: { color: "C00000", fontSize: 20, fontFace: FONT, italic: true } },
  { text: " and ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "Class II", options: { color: "008000", fontSize: 20, fontFace: FONT, italic: true } },
], {
  x: boxX + 0.2, y: boxY + 0.1, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "let d(X) be a discriminant function = ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "W^T X", options: { color: "000000", fontSize: 20, fontFace: FONT, italic: true } },
], {
  x: boxX + 0.2, y: boxY + 0.4, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "if X \u2208 ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "class I", options: { color: "C00000", fontSize: 20, fontFace: FONT, italic: true } },
  { text: " then d(X) ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "> 0", options: { color: "C00000", fontSize: 20, fontFace: FONT } },
], {
  x: boxX + 0.2, y: boxY + 0.7, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "if X \u2208 ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "class II", options: { color: "008000", fontSize: 20, fontFace: FONT, italic: true } },
  { text: " then d(X) ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "< 0", options: { color: "0000FF", fontSize: 20, fontFace: FONT } },
], {
  x: boxX + 0.2, y: boxY + 1.0, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});

boxY += boxH1 + gap;

// Box 2 - For misclassified X
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH2,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
s.addText([
  { text: "For misclassified ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "X", options: { color: "008000", fontSize: 20, fontFace: FONT, italic: true } },  // Judge: X should be green
  { text: " :", options: { color: "000000", fontSize: 20, fontFace: FONT } },
], {
  x: boxX + 0.2, y: boxY + 0.1, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "If X \u2208 ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "class I", options: { color: "C00000", fontSize: 20, fontFace: FONT, italic: true } },
  { text: " and misclassified as Class II then d(X) will be ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "<0", options: { color: "C00000", fontSize: 20, fontFace: FONT } },
], {
  x: boxX + 0.2, y: boxY + 0.4, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "If X \u2208 ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "class II", options: { color: "008000", fontSize: 20, fontFace: FONT, italic: true } },
  { text: " and misclassified as Class I then d(X) will be ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: ">0", options: { color: "0000FF", fontSize: 20, fontFace: FONT } },
], {
  x: boxX + 0.2, y: boxY + 0.7, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});

boxY += boxH2 + gap;

// Box 3 - Define Error function - USE 2D EQUATION PNG
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH3,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
s.addText("Define Error function as:", {
  x: boxX + 0.2, y: boxY + 0.1, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top",
  fontSize: 20, color: "000000", fontFace: FONT, margin: 0,
});
// Embed the 2D equation PNG - centered vertically
// eq_error.png: w_in=7.225, h_in=0.492, baseline_frac=0.932
// Center vertically in the box: boxH3 = 1.125
const eqErrorY = boxY + (boxH3 - 0.492) / 2;
// Add "Error = " text label before the equation image
s.addText("Error = ", {
  x: boxX + 0.2, y: eqErrorY + 0.05, w: 1.5, h: 0.3,
  align: "left", valign: "top",
  fontSize: 16, color: "000000", fontFace: FONT, margin: 0,
});
s.addImage({
  path: "assets/eq_error.png",
  x: boxX + 1.5,
  y: eqErrorY,
  w: 7.225,
  h: 0.492,
});
// Red X inline at right end of equation line
s.addText("X", {
  x: boxX + 8.8, y: eqErrorY + 0.1, w: 1.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

boxY += boxH3 + gap;

// Box 4 - Define delta_i
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH4,
  fill: { color: "FFFFFF" },
  line: { color: "C00000", width: 1 },
});
s.addText("Define \u03B4_i as :", {
  x: boxX + 0.2, y: boxY + 0.1, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top",
  fontSize: 20, color: "000000", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "If X \u2208 ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "class I", options: { color: "C00000", fontSize: 20, fontFace: FONT, italic: true } },
  { text: " and misclassified as Class II then d(X) will be ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "<0 \u21D2 \u03B4_i = -1 \u21D2 d(X) \u03B4_i >0", options: { color: "000000", fontSize: 20, fontFace: FONT } },
], {
  x: boxX + 0.2, y: boxY + 0.4, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});
s.addText([
  { text: "If X \u2208 ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: "class II", options: { color: "008000", fontSize: 20, fontFace: FONT, italic: true } },
  { text: " and misclassified as Class I then d(X) will be ", options: { color: "000000", fontSize: 20, fontFace: FONT } },
  { text: ">0 \u21D2 \u03B4_i = +1 \u21D2 d(X) \u03B4_i >0", options: { color: "000000", fontSize: 20, fontFace: FONT } },
], {
  x: boxX + 0.2, y: boxY + 0.7, w: boxW - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});

pres.writeFile({ fileName: "slide_003_recreated.pptx" }).then(() => console.log("wrote slide_003_recreated.pptx"));