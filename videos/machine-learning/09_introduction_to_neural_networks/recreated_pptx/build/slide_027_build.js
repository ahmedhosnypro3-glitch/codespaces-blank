// Build slide 027: Multi-Layer Neural Network (badge 27)
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";

// ---- HOUSE CHROME ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFD966" }, line: { color: "800080", width: 1.5 },
});
s.addText("27", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Title
s.addText("Multi-Layer Neural Network", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Subtitle
s.addText("The complete Picture", {
  x: 0.6, y: 1.0, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Bottom bar
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.4, w: W, h: 0.4,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

const outPath = "slide_027_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));