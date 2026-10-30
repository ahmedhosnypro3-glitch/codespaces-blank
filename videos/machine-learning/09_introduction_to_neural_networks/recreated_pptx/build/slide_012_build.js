const pptxgen = require("pptxgenjs");

// Slide 012: Classification of "OR" Truth Table
const NUM = 12;
const BG = "E6E6E6";
const RED = "C0392B";
const BLACK = "333333";
const CYAN = "00BFFF";
const GREEN = "2ECC71";
const YELLOW = "FFF9C4";
const BORDER_RED = "E74C3C";
const PEACH = "FDEBD0";
const BLUE = "2980B9";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// House frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// Badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title
s.addText("Classification of \"OR\" Truth Table", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Truth Table (top-left)
const tableData = [
  [{ text: "X₁", options: { bold: true }}, { text: "X₂", options: { bold: true }}, { text: "O/P", options: { bold: true }}],
  [{ text: "0" }, { text: "0" }, { text: "0" }],
  [{ text: "0" }, { text: "1" }, { text: "1" }],
  [{ text: "1" }, { text: "0" }, { text: "1" }],
  [{ text: "1" }, { text: "1" }, { text: "1" }],
];
s.addTable(tableData, {
  x: 0.8, y: 1.2, w: 5.0, h: 2.0,
  fontSize: 16, fontFace: FONT, color: BLACK,
  border: { type: "solid", color: BORDER_RED, pt: 1 },
  cellMargins: 2,
  rowColors: [
    { fill: "FFFFFF" },
    { fill: CYAN },
    { fill: GREEN },
    { fill: GREEN },
    { fill: GREEN },
  ],
});

// Decision Plot (top-right)
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.0, y: 1.2, w: 5.5, h: 2.2,
  fill: { color: "FFFFFF" }, line: { color: BORDER_RED, width: 1.5 },
});
s.addText("Decision Boundary Plot\n(OR gate: separates (0,0)\nfrom other points)", {
  x: 7.2, y: 1.5, w: 5.1, h: 1.8,
  align: "center", valign: "middle",
  fontSize: 14, color: "666666", fontFace: FONT, margin: 0,
});

// Perceptron Diagram (bottom-left)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 3.5, w: 5.5, h: 2.8,
  fill: { color: "FFFFFF" }, line: { color: BORDER_RED, width: 1.5 },
});
s.addText("x₁ (-7)", { x: 1.0, y: 3.8, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: BLACK, fontFace: FONT });
s.addText("x₂ (-5)", { x: 1.0, y: 4.4, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: BLACK, fontFace: FONT });
s.addText("1 (2)", { x: 1.0, y: 5.0, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: BLUE, fontFace: FONT });
s.addShape(pres.shapes.OVAL, { x: 3.0, y: 4.2, w: 0.6, h: 0.6, fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 } });
s.addText("Σ", { x: 3.0, y: 4.2, w: 0.6, h: 0.6, align: "center", valign: "middle", fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: 4.0, y: 4.3, w: 1.8, h: 0.8, fill: { color: "F0F0F0" }, line: { color: "8E44AD", width: 1 } });
s.addText(">0 => 1\n<0 => 0", { x: 4.0, y: 4.3, w: 1.8, h: 0.8, align: "center", valign: "middle", fontSize: 12, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("O/P", { x: 6.0, y: 4.5, w: 0.5, h: 0.3, fontSize: 14, bold: true, color: BLACK, fontFace: FONT });

// Equation box
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.0, y: 5.5, w: 5.5, h: 1.0,
  fill: { color: PEACH }, line: { color: BORDER_RED, width: 1.5 },
});
s.addText("d(X) = -7 x₁ - 5 x₂ + 2", {
  x: 7.0, y: 5.6, w: 5.5, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_012_recreated.pptx" 
}).then(() => console.log("wrote slide_012_recreated.pptx"));
