const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

const FONT = "Arial";
const RED = "C00000";
const BLUE = "0000FF";
const DARK_RED = "8B0000";
const BLACK = "000000";
const YELLOW = "FFF9C4";

// 1. House outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("6", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position) - positioned per original's measured layout
s.addText("Update Weights of", {
  x: 0.6, y: 1.0, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Output Layer", {
  x: 0.6, y: 1.27, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Subtitle (from original: centered, blue, with 'previous' and 'output layer' underlined)
// Use rich text: separate runs for underlined words
s.addText([
  { text: "( Weights from ", options: { breakLine: false } },
  { text: "previous", options: { breakLine: false, underline: true } },
  { text: " layer to ", options: { breakLine: false } },
  { text: "output layer", options: { breakLine: false, underline: true } },
  { text: " )", options: { breakLine: false } },
], {
  x: 0.6, y: 2.1, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 20, color: BLUE, fontFace: FONT, margin: 0,
});

// 6. Thick black strip at bottom edge (inside house frame)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: H - 0.38, w: W - 0.3, h: 0.08,
  fill: { color: BLACK }, line: { type: "none" },
});

pres.writeFile({ fileName: path.join(__dirname, "slide_006_recreated.pptx") })
  .then(() => console.log("wrote slide_006_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });