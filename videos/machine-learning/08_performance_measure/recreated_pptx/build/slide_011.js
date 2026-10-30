const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// House frame: outer red frame x=0.15 y=0.15 w=13.03 h=7.2, border RED 1.5pt, no fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// Slide-number badge: yellow circle x=12.48 y=0.30 w=0.5 h=0.5 fill YELLOW outline YELLOW, numeral 18pt INK
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("11", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Slide title: text box at y=0.28, x=0.6 w=12.13 centered
s.addText("Recall", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Definition strip: gray box at upper left with red horizontal divider
// Position: upper left area, approx x=0.4, y=1.0, w=5.5, h=0.8
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.4, y: 1.0, w: 6.0, h: 0.8,
  fill: { color: "E0E0E0" }, line: { color: "E0E0E0", width: 0 },
});
// Red horizontal divider at middle (bottom of first line)
s.addShape(pptx.shapes.LINE, {
  x: 0.4, y: 1.4, w: 6.0, h: 0,
  line: { color: "D00000", width: 2 },
});
// Two centered bold lines
s.addText("Correctly Classified (as Positive)", {
  x: 0.5, y: 1.05, w: 5.8, h: 0.35, fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center",
});
s.addText("Total objects that should be retrieved (Actually Positive)", {
  x: 0.5, y: 1.45, w: 5.8, h: 0.35, fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center",
});

// Meaning box: cream box below definition strip
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.4, y: 1.6, w: 5.5, h: 1.2,
  fill: { color: "F5F5DC" }, line: { color: "D0D0D0", width: 0.5 },
});
s.addText("Meaning", {
  x: 0.5, y: 1.65, w: 5.3, h: 0.3, fontSize: 18, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// "Does the classifier miss any of Positive Objects ?" with "miss" in red italic, "Positive" underlined blue
// Split into parts for styling
const meaningY = 2.0;
s.addText("Does the classifier ", {
  x: 0.5, y: meaningY, w: 5.3, h: 0.35, fontSize: 15, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("miss", {
  x: 2.4, y: meaningY, w: 0.8, h: 0.35, fontSize: 15, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText(" any of ", {
  x: 3.1, y: meaningY, w: 1.5, h: 0.35, fontSize: 15, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Positive", {
  x: 3.8, y: meaningY, w: 1.2, h: 0.35, fontSize: 15, underline: true, color: "0000FF", fontFace: FONT, margin: 0,
});
s.addText(" Objects ?", {
  x: 4.5, y: meaningY, w: 1.3, h: 0.35, fontSize: 15, color: TEXT, fontFace: FONT, margin: 0,
});

// Formula box: RED rounded rectangle with stacked fraction
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.4, y: 3.0, w: 3.5, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 },
  round: 0.2,
});
s.addText("Recall =", {
  x: 0.5, y: 3.1, w: 3.3, h: 0.4, fontSize: 18, color: TEXT, fontFace: FONT, margin: 0,
});
// Add equation image: TP over TP+FN
s.addImage({ path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_011_1.png", x: 0.9, y: 3.55, w: 0.68333, h: 0.33 });

// Calculation box: light blue box to the right of formula box
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.1, y: 3.0, w: 3.0, h: 1.2,
  fill: { color: "E3F2FD" }, line: { color: "D0D0D0", width: 0.5 },
});
// "Recall =" text prefix
s.addText("Recall =", {
  x: 4.2, y: 3.3, w: 1.0, h: 0.35, fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});
// Equation image: 28/(28+2) = 93.3%
s.addImage({ path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_011_2.png", x: 5.2, y: 3.25, w: 1.49333, h: 0.30167 });

// Speech bubbles: two beige WEDGE callouts with UPWARD-pointing tails
// Left callout - using custom shape approximation
const calloutY = 4.4;
const calloutW = 2.8, calloutH = 0.8;

// Left callout body
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.4, y: calloutY, w: calloutW, h: calloutH,
  fill: { color: "F5E6D3" }, line: { color: "D0B080", width: 1 },
  round: 0.1,
});
// Upward tail for left (triangle pointing up)
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: 1.5, y: calloutY + calloutH, w: 0.3, h: 0.2,
  fill: { color: "F5E6D3" }, line: { color: "D0B080", width: 1 },
  rotate: 270,
});
// Two-line text: "Positive" / "Classified as +ive"
s.addText("Positive", {
  x: 0.5, y: calloutY + 0.05, w: calloutW - 0.2, h: 0.35, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center",
});
s.addText("Classified as +ive", {
  x: 0.5, y: calloutY + 0.4, w: calloutW - 0.2, h: 0.35, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center",
});

// Right callout
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 3.5, y: calloutY, w: calloutW, h: calloutH,
  fill: { color: "F5E6D3" }, line: { color: "D0B080", width: 1 },
  round: 0.1,
});
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: 4.6, y: calloutY + calloutH, w: 0.3, h: 0.2,
  fill: { color: "F5E6D3" }, line: { color: "D0B080", width: 1 },
  rotate: 270,
});
s.addText("Positive", {
  x: 3.6, y: calloutY + 0.05, w: calloutW - 0.2, h: 0.35, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center",
});
s.addText("Classified as -ive", {
  x: 3.6, y: calloutY + 0.4, w: calloutW - 0.2, h: 0.35, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center",
});

// Green curly brace under callouts (PNG, exact size 3.0 x 0.45 in)
s.addImage({ path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/brace_011.png", x: 0.55, y: calloutY + calloutH + 0.05, w: 3.0, h: 0.45 });

// Dataset line: red italic text centered under brace
s.addText("All Positive Samples in the Dataset", {
  x: 1.5, y: calloutY + calloutH + 0.55, w: 3.3, h: 0.3, fontSize: 14, italic: true, color: RED, fontFace: FONT, margin: 0, align: "center",
});

// Blue note box at bottom left
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.4, y: 5.7, w: 5.8, h: 1.4,
  fill: { color: "E3F2FD" }, line: { color: "0000FF", width: 1.5 },
});
s.addText("Higher Recall means I HIGHLY trust you if you said I picked ALL Positive Objects.", {
  x: 0.5, y: 5.75, w: 5.6, h: 0.5, fontSize: 13, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("It Does NOT mean All you said Positive are Actually Positive", {
  x: 0.5, y: 6.3, w: 5.6, h: 0.5, fontSize: 13, color: TEXT, fontFace: FONT, margin: 0,
});

// Top-right: Two confusion matrices stacked with proper structure
// Blue enclosing rectangle around first matrix (added FIRST so it's behind the table)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.45, y: 0.95, w: 5.1, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 2 },
});

// First confusion matrix with "Predicted as" header spanning P/N, vertical "Actual" label, left row headers P/N
let tableData1 = [
  [{ text: "", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" } } },
   { text: "Predicted as", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "P", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "N", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } }],
  [{ text: "Actual", options: { fontSize: 12, bold: true, color: RED, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center", rotation: 90 } },
   { text: "P", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "TP", options: { fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, fill: { color: "00AA00" }, align: "center" } },
   { text: "FN", options: { fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, fill: { color: "FF0000" }, align: "center" } }],
  [{ text: "", options: { fontSize: 12, color: TEXT, fontFace: FONT } },
   { text: "N", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "FP", options: { fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, fill: { color: "FF0000" }, align: "center" } },
   { text: "TN", options: { fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, fill: { color: "00AA00" }, align: "center" } }],
];

s.addTable(tableData1, {
  x: 7.5, y: 1.0, w: 5.0,
  rowH: [0.3, 0.4, 0.4],
  fontSize: 12,
  fontFace: FONT,
  color: TEXT,
  border: [{ type: "solid", color: "000000", width: 1 }],
});

// Blue enclosing rectangle around second matrix (added FIRST)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.45, y: 2.25, w: 5.1, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 2 },
});

// Second confusion matrix
let tableData2 = [
  [{ text: "", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" } } },
   { text: "Predicted as", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "P", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "N", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } }],
  [{ text: "Actual", options: { fontSize: 12, bold: true, color: RED, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center", rotation: 90 } },
   { text: "P", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "28", options: { fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, fill: { color: "800080" }, align: "center" } },
   { text: "2", options: { fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, fill: { color: "FF0000" }, align: "center" } }],
  [{ text: "", options: { fontSize: 12, color: TEXT, fontFace: FONT } },
   { text: "N", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "F0F0F0" }, align: "center" } },
   { text: "30", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "00AA00" }, align: "center" } },
   { text: "40", options: { fontSize: 12, bold: true, color: TEXT, fontFace: FONT, fill: { color: "00AA00" }, align: "center" } }],
];

s.addTable(tableData2, {
  x: 7.5, y: 2.3, w: 5.0,
  rowH: [0.3, 0.4, 0.4],
  fontSize: 12,
  fontFace: FONT,
  color: TEXT,
  border: [{ type: "solid", color: "000000", width: 1 }],
});

// Bottom-right: Red enclosing frame around both tree diagrams
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.45, y: 3.7, w: 5.1, h: 3.3,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 },
});

// Positive tree (left) inside red frame
const treeY = 3.9;
const treeX = 7.7;

// Positive label
s.addText("Positive", {
  x: treeX, y: treeY, w: 2.3, h: 0.3, fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0, align: "center",
});

// Airplane icon (PNG line drawing, 0.21333 x 0.24 in)
s.addImage({ path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/airplane_011.png", x: treeX + 0.89, y: treeY - 0.42, w: 0.21333, h: 0.24 });

// Root node 30 (red circle)
s.addShape(pptx.shapes.OVAL, {
  x: treeX + 0.7, y: treeY + 0.3, w: 0.6, h: 0.6,
  fill: { color: RED }, line: { color: RED, width: 1 },
});
s.addText("30", {
  x: treeX + 0.7, y: treeY + 0.3, w: 0.6, h: 0.6, align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Left child 28 (red circle, TP)
s.addShape(pptx.shapes.OVAL, {
  x: treeX + 0.2, y: treeY + 1.2, w: 0.6, h: 0.6,
  fill: { color: RED }, line: { color: RED, width: 1 },
});
s.addText("28", {
  x: treeX + 0.2, y: treeY + 1.2, w: 0.6, h: 0.6, align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("TP", {
  x: treeX + 0.2, y: treeY + 1.85, w: 0.6, h: 0.25, align: "center",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Right child 2 (green circle, FN)
s.addShape(pptx.shapes.OVAL, {
  x: treeX + 1.5, y: treeY + 1.2, w: 0.6, h: 0.6,
  fill: { color: "00AA00" }, line: { color: "00AA00", width: 1 },
});
s.addText("2", {
  x: treeX + 1.5, y: treeY + 1.2, w: 0.6, h: 0.6, align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("FN", {
  x: treeX + 1.5, y: treeY + 1.85, w: 0.6, h: 0.25, align: "center",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Connector lines (root to children) - thin blue
s.addShape(pptx.shapes.LINE, {
  x: treeX + 1.0, y: treeY + 0.9, w: -0.5, h: 0.3,
  line: { color: "0000FF", width: 1 },
});
s.addShape(pptx.shapes.LINE, {
  x: treeX + 1.0, y: treeY + 0.9, w: 0.5, h: 0.3,
  line: { color: "0000FF", width: 1 },
});

// Negative tree (right)
const negTreeX = 10.3;
s.addText("Negative", {
  x: negTreeX, y: treeY, w: 2.3, h: 0.3, fontSize: 16, bold: true, color: "00AA00", fontFace: FONT, margin: 0, align: "center",
});

s.addImage({ path: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/airplane_011.png", x: negTreeX + 0.89, y: treeY - 0.42, w: 0.21333, h: 0.24 });

// Root node 70 (green circle)
s.addShape(pptx.shapes.OVAL, {
  x: negTreeX + 0.7, y: treeY + 0.3, w: 0.6, h: 0.6,
  fill: { color: "00AA00" }, line: { color: "00AA00", width: 1 },
});
s.addText("70", {
  x: negTreeX + 0.7, y: treeY + 0.3, w: 0.6, h: 0.6, align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Left child 40 (green circle, TN)
s.addShape(pptx.shapes.OVAL, {
  x: negTreeX + 0.2, y: treeY + 1.2, w: 0.6, h: 0.6,
  fill: { color: "00AA00" }, line: { color: "00AA00", width: 1 },
});
s.addText("40", {
  x: negTreeX + 0.2, y: treeY + 1.2, w: 0.6, h: 0.6, align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("TN", {
  x: negTreeX + 0.2, y: treeY + 1.85, w: 0.6, h: 0.25, align: "center",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Right child 30 (red circle, FP)
s.addShape(pptx.shapes.OVAL, {
  x: negTreeX + 1.5, y: treeY + 1.2, w: 0.6, h: 0.6,
  fill: { color: RED }, line: { color: RED, width: 1 },
});
s.addText("30", {
  x: negTreeX + 1.5, y: treeY + 1.2, w: 0.6, h: 0.6, align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("FP", {
  x: negTreeX + 1.5, y: treeY + 1.85, w: 0.6, h: 0.25, align: "center",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Connector lines - thin blue
s.addShape(pptx.shapes.LINE, {
  x: negTreeX + 1.0, y: treeY + 0.9, w: -0.5, h: 0.3,
  line: { color: "0000FF", width: 1 },
});
s.addShape(pptx.shapes.LINE, {
  x: negTreeX + 1.0, y: treeY + 0.9, w: 0.5, h: 0.3,
  line: { color: "0000FF", width: 1 },
});

// Write output
const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_011_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done"));