// Pattern: house-chrome + slide 007 content (Multi-Class Classification using ONE VS ALL Binary Classifiers)
// Build: NODE_PATH=$(npm root -g) node slide_007_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 7;
const FONT = "Arial";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const TITLE_RED = "C00000";
const TITLE_BLUE = "0000FF";
const YELLOW = "FFF9C4";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: TITLE_RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box - TWO LINES per judge (original has break after "Classification")
// Line 1: "Multi-Class Classification" (red)
// Line 2: "using [ONE VS ALL] Binary Classifiers" (red, with [ONE VS ALL] in blue)
s.addText("Multi-Class Classification", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "using ", options: { color: TITLE_RED, fontSize: 28, bold: true, fontFace: FONT } },
  { text: "[ONE VS ALL] ", options: { color: TITLE_BLUE, fontSize: 28, bold: true, fontFace: FONT } },
  { text: "Binary Classifiers", options: { color: TITLE_RED, fontSize: 28, bold: true, fontFace: FONT } },
], {
  x: 0.6, y: 0.65, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

// 4. Plot frame position: x=2.4, y=1.65, w=8.66, h=5.25
const PLOT_X = 2.4;
const PLOT_Y = 1.65;
const PLOT_W = 8.66;
const PLOT_H = 5.25;

// White frame background with thin red border
s.addShape(pres.shapes.RECTANGLE, {
  x: PLOT_X, y: PLOT_Y, w: PLOT_W, h: PLOT_H,
  fill: { color: "FFFFFF" }, line: { color: TITLE_RED, width: 1 },
});

// Embed the generated PNG at exact size
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_007_decision_boundary.png",
  x: PLOT_X, y: PLOT_Y, w: PLOT_W, h: PLOT_H,
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_007_recreated.pptx"
}).then(() => console.log("wrote slide_007_recreated.pptx"));