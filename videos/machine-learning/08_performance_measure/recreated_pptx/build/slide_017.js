const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E6E6E6", RED = "CC0000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const REDFRAME = "CC0000", MAGENTA = "CC00CC";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME (from root AGENTS.md)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: REDFRAME, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: MAGENTA, width: 1.5 } });
s.addText("17", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: TEXT, fontFace: FONT, margin: 0 });
s.addText("F-Score for different Precision and Recall values", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8, align: "center", valign: "middle",
  fontSize: 32, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// CHART: generated matplotlib image, red-outlined container
// ============================================================
// Chart container red rect: x=2.7, y=1.35, w=8.4, h=5.75
s.addShape(pptx.shapes.RECTANGLE, {
  x: 2.7, y: 1.35, w: 8.4, h: 5.75,
  fill: { color: BG }, line: { color: REDFRAME, width: 1.5 },
});

// Chart image inside the container (white plot figure)
// Image is 978x693 px -> embed at exact size: 978/150=6.52in, 693/150=4.62in
// Center it in the container
const chartW = 6.52, chartH = 4.62;
const chartX = 2.7 + (8.4 - chartW) / 2;
const chartY = 1.35 + (5.75 - chartH) / 2;
s.addImage({
  path: "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/slide017_f1chart.png",
  x: chartX, y: chartY, w: chartW, h: chartH,
});

// ============================================================
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_017_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));