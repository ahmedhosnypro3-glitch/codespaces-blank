const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const RED2 = "D32F2F";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "0000FF";
const BLACK = "000000";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("27", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Receiver Operating Characteristic (ROC) Curve", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED2, fontFace: FONT, margin: 0,
});

// ============================================================
// SLIDE 27 CONTENT — text block with red/blue alternating lines
// ============================================================
const blockX = 0.8;
const blockY = 1.4;
const blockW = 11.5;

const lines = [
  { text: "Conclusion from Previous Experiments:", color: RED2, bold: true, fontSize: 18, indent: false },
  { text: "Same Model", color: BLUE, bold: false, fontSize: 16, indent: true },
  { text: "Same Test Samples", color: BLUE, bold: false, fontSize: 16, indent: true },
  { text: "Performance Measures (TP, TN, FP, FN) are affected by selected threshold", color: RED2, bold: true, fontSize: 18, indent: false },
  { text: "There is a Confusion Matrix for each threshold", color: BLUE, bold: false, fontSize: 16, indent: false },
  { text: "Can we combine All thresholds and corresponding Confusion Matrices in one Graph?", color: RED2, bold: true, fontSize: 18, indent: false },
  { text: "Solution: Use ROC Curve", color: BLUE, bold: false, fontSize: 16, indent: false },
];

// Render lines with explicit line spacing (mandatory per pattern law)
const lineH = 0.55;
let curY = blockY;
for (const line of lines) {
  const x = line.indent ? blockX + 0.4 : blockX;
  s.addText(line.text, {
    x: x, y: curY, w: blockW, h: lineH,
    fontSize: line.fontSize, bold: line.bold, color: line.color,
    fontFace: FONT, align: "left", valign: "middle", margin: 0,
  });
  curY += lineH;
}

// ============================================================
// FOOTER: solid black bar spanning full width at bottom
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: H - 0.35, w: W - 0.3, h: 0.2,
  fill: { color: BLACK }, line: { type: "none" },
});

// ============================================================
// OUTPUT
// ============================================================
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_027_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
