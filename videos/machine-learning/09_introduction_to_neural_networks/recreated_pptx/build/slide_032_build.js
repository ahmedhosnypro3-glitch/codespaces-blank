// Build slide 032: How to Update Weights in order to minimize Error ? (badge 32)
// Rejudge iteration 1 — geometry from PIL measurement of unique_slides/slide_032.jpg (960x540, 1px=1pt):
//   title 2 lines, Arial Bold 34pt C00000, ink w 554/265px, pitch 38pt
//   body 2 lines, Arial Bold 30pt 000000, ink w 658/227px, band y 218-244 / 251-271
//   blue line, Arial Bold 34pt 0000FF, ink w 478px, band y 312-345
//   badge: yellow fill FFF9C4 + purple ring 4B0082 (measured on frame + family reference slide 3)
// house chrome: E8E8E8 bg, red frame 0.15in inset C00000 1.5pt, title box y=0.28 x=0.6 w=12.13
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";
const RED = "C00000", BLACK = "000000", BLUE = "0000FF";
const YELLOW = "FFF9C4", BADGE_RING = "4B0082", BADGE_NUM = "333333";

// ---- HOUSE CHROME ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: BADGE_RING, width: 1.5 },
});
s.addText("32", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_NUM, fontFace: FONT, margin: 0,
});

// Title - house box y=0.28, two lines matching the original's line break
s.addText("How to Update Weights in order to\nminimize Error ?", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.2,
  align: "center", valign: "top",
  fontSize: 34, bold: true, color: RED, fontFace: FONT, margin: 0,
  lineSpacing: 38,
});

// Main body text - two single-line boxes at the original's measured bands
s.addText("Move in the opposite direction of the gradients", {
  x: 0.6, y: 2.917, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("Of the whole NN", {
  x: 0.6, y: 3.381, w: 12.13, h: 0.45,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Blue section header: "(Back Propagation Algorithm)"
s.addText("(Back Propagation Algorithm)", {
  x: 0.6, y: 4.217, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 34, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// Solid black horizontal bar at bottom edge (video player overlay, as in the original;
// same convention as certified siblings 005/009)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { type: "none" },
});

const outPath = "slide_032_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));
