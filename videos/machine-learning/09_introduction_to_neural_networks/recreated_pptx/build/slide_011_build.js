const pptxgen = require("pptxgenjs");

// Slide 011: Classification of "AND" Truth Table (same content as 010 but different layout)
const NUM = 11;
const BG = "EAEAEA";  // From raw analysis
const RED = "C0392B";  // Dark red per analysis
const BLACK = "333333";
const CYAN = "D0F0F0";
const GREEN = "C0F0C0";
const YELLOW = "FFF9C4";
const BORDER_RED = "E74C3C";  // Red borders per analysis
const PEACH = "FDEBD0";
const BLUE = "3498DB";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. House frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. Badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title - HOUSE CHROME: y=0.28
s.addText("Classification of \"AND\" Truth Table", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Truth Table (top-left)
const tableData = [
  [{ text: "X1", options: { bold: true }}, { text: "X2", options: { bold: true }}, { text: "O/P", options: { bold: true }}],
  [{ text: "0" }, { text: "0" }, { text: "0" }],
  [{ text: "0" }, { text: "1" }, { text: "0" }],
  [{ text: "1" }, { text: "0" }, { text: "0" }],
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
    { fill: CYAN },
    { fill: CYAN },
    { fill: GREEN },
  ],
});

// 5. Decision Plot (middle-right) with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.0, y: 1.2, w: 5.5, h: 2.2,
  fill: { color: "FFFFFF" }, line: { color: BORDER_RED, width: 1.5 },
});
s.addText("Decision Boundary Plot\n(2D plot: x1 axis, x2 axis,\nblue line, cyan/green points)", {
  x: 7.2, y: 1.5, w: 5.1, h: 1.8,
  align: "center", valign: "middle",
  fontSize: 14, color: "666666", fontFace: FONT, margin: 0,
});

// 6. Perceptron Diagram (bottom-left) with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.8, y: 3.5, w: 5.5, h: 2.8,
  fill: { color: "FFFFFF" }, line: { color: BORDER_RED, width: 1.5 },
});
s.addText("x1 (-5)", { x: 1.0, y: 3.8, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: BLACK, fontFace: FONT });
s.addText("x2 (-3)", { x: 1.0, y: 4.4, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: BLACK, fontFace: FONT });
s.addText("1 (6)", { x: 1.0, y: 5.0, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: RED, fontFace: FONT });
s.addShape(pres.shapes.OVAL, { x: 3.0, y: 4.2, w: 0.6, h: 0.6, fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 } });
s.addText("Σ", { x: 3.0, y: 4.2, w: 0.6, h: 0.6, align: "center", valign: "middle", fontSize: 20, bold: true, color: BLACK, fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: 4.0, y: 4.3, w: 1.8, h: 0.8, fill: { color: "F0F0F0" }, line: { color: BLACK, width: 1 } });
s.addText(">0 => 1\n<0 => 0", { x: 4.0, y: 4.3, w: 1.8, h: 0.8, align: "center", valign: "middle", fontSize: 12, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("O/P", { x: 6.0, y: 4.5, w: 0.5, h: 0.3, fontSize: 14, bold: true, color: BLACK, fontFace: FONT });

// 7. Equation box (bottom-right) - peach rounded rect
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 7.0, y: 5.5, w: 5.5, h: 1.0,
  fill: { color: PEACH }, line: { color: BORDER_RED, width: 1.5 },
});

// Embed the equation PNG
// Equation: d(X) = -5 x1 - 3 x2 + 6
// From render: w_in=2.66333, h_in=0.25333, baseline_frac=0.79605
// Place it centered in the peach box
const eqImg = {
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/eq_s011_dX.png",
  w_in: 2.66333,
  h_in: 0.25333,
  baseline_frac: 0.79605,
};
const imgX = 7.0 + (5.5 - eqImg.w_in) / 2;
const imgY = 5.5 + (1.0 - eqImg.h_in) / 2;
s.addImage({
  path: eqImg.path,
  x: imgX, y: imgY, w: eqImg.w_in, h: eqImg.h_in,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_011_recreated.pptx" 
}).then(() => console.log("wrote slide_011_recreated.pptx"));
