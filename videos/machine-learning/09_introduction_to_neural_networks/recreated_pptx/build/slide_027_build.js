// Build slide 027 (badge 27): "Multi-Layer Neural Network / The complete Picture"
// Geometry from PIL on unique_slides/slide_027.jpg (960x540 => 1px = 1pt):
//   title ink y 214..251, baseline 243; subtitle ink y 279..319, baseline 308
//   both lines Liberation Sans Bold @38pt (per-glyph N/u/l/t/i positions matched)
//   black band x 38..921 (0.53..12.80 in), y 518..539 (7.19..7.5 in)
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";
const RED = "C00000";

// Bottom black band — original: x 0.53..12.80 in, y 7.19..7.5 in (drawn first, under the frame)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.53, y: 7.19, w: 12.27, h: 0.31,
  fill: { color: "000000" }, line: { width: 0 },
});

// ---- HOUSE CHROME (on top of the band) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("27", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title — ink center 3.229 in, box centered on it
s.addText("Multi-Layer Neural Network", {
  x: 0.6, y: 2.779, w: 12.13, h: 0.9,
  align: "center", valign: "middle",
  fontSize: 38, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Second line — ink center 4.153 in (same size and color as line 1)
s.addText("The complete Picture", {
  x: 0.6, y: 3.703, w: 12.13, h: 0.9,
  align: "center", valign: "middle",
  fontSize: 38, bold: true, color: RED, fontFace: FONT, margin: 0,
});

const outPath = "slide_027_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));
