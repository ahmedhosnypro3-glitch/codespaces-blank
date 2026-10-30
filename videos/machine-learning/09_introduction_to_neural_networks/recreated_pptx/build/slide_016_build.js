const pptxgen = require("pptxgenjs");

// Slide 016: Adding non-Linearity to Perceptrons (Activation Functions)
const NUM = 16;
const TITLE = "Adding non-Linearity to Perceptrons";
const FONT = "Times New Roman";  // Serif per spec (resembling Times New Roman)

const BG = "EAEAEA";
const RED = "C00000";
const BLUE = "0000FF";
const BLACK = "000000";
const YELLOW = "FFF200";
const BORDER_RED = "8B0000";

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

// 2. Bottom black bar - from validation analysis
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

// 3. Slide-number badge - yellow circle with black outline (HOUSE CHROME)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: BLACK, width: 1 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 4. Title - HOUSE CHROME LAW: text box starts y=0.28, x=0.6, w=12.13, centered
// Original cap height ~34px @540px → 71px @1125px. LO renders ~6.4px/pt.
// Need ~11pt. Use 12pt to match original visual size.
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 5. Subtitle - same visual size as title per original (roughly same cap height)
// Original subtitle ~27px @540px → 56px @1125px. My 30pt gave 42px (1.4px/pt).
// Use 12pt for parity with title.
s.addText([
  { text: "(", options: { color: RED, bold: true, fontSize: 12, fontFace: FONT } },
  { text: "Activation", options: { color: BLUE, bold: true, fontSize: 12, fontFace: FONT } },
  { text: " Functions)", options: { color: RED, bold: true, fontSize: 12, fontFace: FONT } },
], {
  x: 0.6, y: 0.9, w: 12.13, h: 0.5,
  align: "center", valign: "middle", margin: 0,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_016_recreated.pptx" 
}).then(() => console.log("wrote slide_016_recreated.pptx"));