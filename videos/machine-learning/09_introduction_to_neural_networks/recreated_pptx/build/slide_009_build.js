const pptxgen = require("pptxgenjs");

// Slide 009: Test Single Perceptron with [AND – OR – XOR] Logic (Binary Classification)
const NUM = 9;
const TITLE_LINE1 = "Test Single Perceptron with";
const TITLE_LINE2 = "[AND \u2013 OR \u2013 XOR] Logic";
const TITLE_LINE3 = "(Binary Classification)";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const BORDER_RED = "8B0000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const BADGE_OUTLINE = "4B0082";
const BADGE_NUM = "4B0082";
const YELLOW = "FFF9C4";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_NUM, fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
// Three lines with specific colors per validation
// Line 1: 'Test' and 'with' in RED (#c00000), 'Single Perceptron' in BLUE (#0000ff)
// Line 2: all RED
// Line 3: all RED
// Need to use multiple addText calls for different colors per line

// Since pptxgenjs doesn't support mixed colors in a single text box easily,
// we'll use separate text boxes or use a single box with formatted runs if supported.
// Actually, pptxgenjs supports array of runs with different colors.

s.addText([
  { text: "Test ", options: { color: RED, bold: true, fontSize: 36, fontFace: FONT } },
  { text: "Single Perceptron", options: { color: BLUE, bold: true, fontSize: 36, fontFace: FONT } },
  { text: " with", options: { color: RED, bold: true, fontSize: 36, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

s.addText(TITLE_LINE2, {
  x: 0.6, y: 0.75, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

s.addText(TITLE_LINE3, {
  x: 0.6, y: 1.22, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_009_recreated.pptx" 
}).then(() => console.log("wrote slide_009_recreated.pptx"));