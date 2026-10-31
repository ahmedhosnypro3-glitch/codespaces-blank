// slide_052.js — FRESH rebuild from qa/reanalysis2/slide_052_analysis.txt (Wave 3).
// Scatter plot: blue U-shape + red cluster, axis labels, vline x=0 (in plot PNG),
// black down-right arrow. House chrome mandatory; spec SLIDE_TITLE: none -> no title text.
// Run: NODE_PATH=$(npm root -g) node slide_052.js
const pptxgen = require("pptxgenjs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 52;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome: outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
// House chrome: badge oval + numeral
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Plot area per spec LAYOUT [0.22, 0.12, 0.79, 0.84] -> inches
const PX = 0.22 * W, PY = 0.12 * H, PW = (0.79 - 0.22) * W, PH = (0.84 - 0.12) * H;
s.addImage({
  path: NS + "/recreated_pptx/build/slide_052_plot_rb4.png",
  x: PX, y: PY, w: PW, h: PH,
});

// Y-axis labels per spec: 35..-5 along region [0.20, 0.10, 0.23, 0.84], right-aligned
const yLabels = ["35", "30", "25", "20", "15", "10", "5", "0", "-5"];
yLabels.forEach((t, i) => {
  const tickN = 0.11 + i * 0.0925; // label band top 0.10, 9 labels to 0.84
  s.addText(t, {
    x: 0.20 * W, y: tickN * H - 0.175, w: (0.23 - 0.20) * W, h: 0.35,
    align: "right", valign: "middle",
    fontSize: 10, color: "000000", fontFace: FONT, margin: 0,
  });
});

// X-axis labels per spec: 0,5,10,15,20 along [0.22, 0.86, 0.79, 0.90], centered on ticks
// Plot maps data x to norm: nx = 0.22 + (xd + 3) / 24 * 0.57 (xlim -3..21)
const xLabels = ["0", "5", "10", "15", "20"];
xLabels.forEach(t => {
  const xd = Number(t);
  const nx = 0.22 + ((xd + 3) / 24) * 0.57;
  s.addText(t, {
    x: nx * W - 0.5, y: 0.86 * H, w: 1.0, h: 0.35,
    align: "center", valign: "top",
    fontSize: 10, color: "000000", fontFace: FONT, margin: 0,
  });
});

// Black arrow pointing down-right per spec [0.32, 0.68, 0.34, 0.71]
const ax0 = 0.32 * W, ay0 = 0.68 * H, ax1 = 0.34 * W, ay1 = 0.71 * H;
s.addShape(pres.shapes.LINE, {
  x: ax0, y: ay0, w: ax1 - ax0, h: ay1 - ay0,
  line: { color: "000000", width: 2 },
});
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: ax1 - 0.09, y: ay1 - 0.08, w: 0.18, h: 0.16,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
  rotate: 135,
});

pres.writeFile({ fileName: NS + "/recreated_pptx/slide_052_recreated.pptx" })
  .then(() => console.log("wrote slide_052_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
