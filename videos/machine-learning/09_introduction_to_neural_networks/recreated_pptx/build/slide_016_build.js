const pptxgen = require("pptxgenjs");

// Slide 016: Adding non-Linearity to Perceptrons (Activation Functions)
const NUM = 16;
const TITLE = "Adding non-Linearity to Perceptrons";
const FONT = "Arial";  // measured: no serifs, x-height/cap 0.73, 5px stems -> Arial-class bold sans

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const BLACK = "000000";
const YELLOW = "FFF9C4";
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
  line: { color: RED, width: 1.5 },
});

// 2. Original's own content-area border, measured in the 960x540 frame:
//    verticals at x=58 and x=901, top edge at y=43, running down behind the black bar.
//    Only the two verticals are drawn: at the house-mandated title band (y=0.28in) the
//    original's top edge would strike through the title, so that edge is left off.
const BW = 1.5 / 72;
s.addShape(pres.shapes.RECTANGLE, {
  x: (58 - BW / 2) / 72, y: 43 / 72, w: BW, h: (540 - 43) / 72,
  fill: { color: BORDER_RED }, line: { color: BORDER_RED, width: 0.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: (901 - BW / 2) / 72, y: 43 / 72, w: BW, h: (540 - 43) / 72,
  fill: { color: BORDER_RED }, line: { color: BORDER_RED, width: 0.5 },
});

// 3. Bottom black bar - measured original: y518..540, i.e. 0.306in flush with the bottom.
//    Drawn after the border so it covers the border's bottom edge.
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.306, w: W, h: 0.306,
  fill: { color: BLACK }, line: { color: BLACK, width: 1 },
});

// 4. Slide-number badge - yellow circle (HOUSE CHROME)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 1 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 5. Title - HOUSE CHROME LAW: text box starts y=0.28, x=0.6, w=12.13, centered.
// Measured original: ink width 674px, cap height 30px, x-height 22px, descender 8px
// (1px = 1pt at 960x540 -> 13.33x7.5in). Liberation Sans Bold @40pt gives
// width 693, cap 28, x-height 22, descender 8.
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 1.0,
  align: "center", valign: "top",
  fontSize: 40, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 6. Subtitle - measured original: ink width 401px, cap height 29px.
// Baseline 65px below the title baseline (title baseline 243, subtitle baseline 308).
s.addText([
  { text: "(", options: { color: RED, bold: true, fontSize: 39, fontFace: FONT } },
  { text: "Activation", options: { color: BLUE, bold: true, fontSize: 39, fontFace: FONT } },
  { text: " Functions)", options: { color: RED, bold: true, fontSize: 39, fontFace: FONT } },
], {
  x: 0.6, y: 1.196, w: 12.13, h: 1.0,
  align: "center", valign: "top", margin: 0,
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_016_recreated.pptx"
}).then(() => console.log("wrote slide_016_recreated.pptx"));
