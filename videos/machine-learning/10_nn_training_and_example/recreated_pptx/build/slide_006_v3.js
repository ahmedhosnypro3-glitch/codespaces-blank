const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

const FONT = "Arial";
const BG = "E8E8E8";
const FRAME_RED = "C00000";   // house frame
const TITLE_RED = "B00000";   // audit-measured title ink
const SUB_BLUE = "0000CC";   // audit-measured subtitle ink
const YELLOW = "FFF9C4";
const BLACK = "000000";

// 1. House outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: FRAME_RED, width: 1.5 },
});

// 2. Slide-number badge (house: yellow circle, 12.48/0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("6", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title, two lines, house title box (y=0.28, x=0.6, w=12.13, centered);
//    original line gap 21px @72px/in = 0.29in, ink height 35px = 0.49in.
s.addText("Update Weights of", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 32, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});
s.addText("Output Layer", {
  x: 0.6, y: 0.85, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 32, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// 4. Subtitle: bold italic blue, "( Weights ...)" (space after "(" only),
//    underline ONLY "previous" and "output". Original gap 17px = 0.24in.
s.addText([
  { text: "( Weights from ", options: { breakLine: false } },
  { text: "previous", options: { breakLine: false, underline: true } },
  { text: " layer to ", options: { breakLine: false } },
  { text: "output", options: { breakLine: false, underline: true } },
  { text: " layer)", options: { breakLine: false } },
], {
  x: 0.6, y: 1.64, w: 12.13, h: 0.45,
  align: "center", valign: "top",
  fontSize: 20, bold: true, italic: true, color: SUB_BLUE,
  fontFace: FONT, margin: 0,
});

// Black bottom bar of the original is a video-capture artifact (audit2 S6 §7) —
// ground rule (c): omitted by design.

pres.writeFile({ fileName: path.join(__dirname, "slide_006_v3.pptx") })
  .then(() => console.log("wrote slide_006_v3.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
