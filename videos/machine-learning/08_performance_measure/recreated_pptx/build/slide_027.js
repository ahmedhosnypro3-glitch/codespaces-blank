const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const RED2 = "C00000";
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
// SLIDE 27 CONTENT — 7 lines, positions measured from the original
// frame in px at 960x540 (1px = 1pt = 1/72in)
// ============================================================
const px = (v) => v / 72;
const blockW = 12.2;

const lines = [
  { text: "Conclusion from Previous Experiments:", x: px(59),  y: px(140), color: RED2, bold: true,  fontSize: 20 },
  { text: "Same Model",                          x: px(83),  y: px(185), color: BLUE, bold: false, fontSize: 16 },
  { text: "Same Test Samples",                   x: px(84),  y: px(207), color: BLUE, bold: false, fontSize: 16 },
  { text: "Performance Measures (TP, TN, FP, FN) are affected by selected threshold", x: px(59), y: px(250), color: RED2, bold: true, fontSize: 20 },
  { text: "There is a Confusion Matrix for each threshold", x: px(267), y: px(297), color: BLUE, bold: false, fontSize: 16 },
  { text: "Can we combine All thresholds and corresponding Confusion Matrices in one Graph?", x: px(59), y: px(367), color: RED2, bold: true, fontSize: 20 },
  { text: "Solution: Use ROC Curve",             x: px(84),  y: px(412), color: BLUE, bold: false, fontSize: 16 },
];

for (const line of lines) {
  s.addText(line.text, {
    x: line.x, y: line.y, w: blockW, h: px(30),
    fontSize: line.fontSize, bold: line.bold, color: line.color,
    fontFace: FONT, align: "left", valign: "top", margin: 0,
  });
}

// ============================================================
// OUTPUT
// ============================================================
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_027_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
