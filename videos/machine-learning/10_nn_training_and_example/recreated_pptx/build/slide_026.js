// Pattern: house-chrome (machine-learning family, measured from slide 3 reference)
// LAWS: Slide LAYOUT_WIDE 13.33x7.5in, background E8E8E8; red frame 0.15in inset; yellow badge; title at y=0.28
// Slide 26 specific: Content positioned to match original layout (title at 1.5in, subtitles at 3.3in and 4.5in)

const pptxgen = require("pptxgenjs");

const NUM = 26;
const TITLE = "Solved Example";
const SUBTITLE1 = "[ Update Weights of Output Layer and Hidden Layer ]";
const SUBTITLE2 = "Using one training sample";
const FONT = "Times New Roman";  // Serif font per analysis

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E7E9E6" };  // Match original background

// 1. Outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral) - HOUSE CHROME
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title at original position (y≈1.5in), centered, dark gray serif
s.addText(TITLE, {
  x: 0.6, y: 1.5, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: "4A4A4A", fontFace: FONT, margin: 0,
});

// 4. Subtitle 1 (centered, red/pink serif) - at y≈3.3in
// Original color: R=185, G=60, B=70 -> B93C46
s.addText(SUBTITLE1, {
  x: 0.6, y: 3.3, w: 12.13, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 28, color: "B93C46", fontFace: FONT, margin: 0,
});

// 5. Subtitle 2 (centered, blue/purple serif) - at y≈4.5in
// Original color: R=67, G=59, B=193 -> 433BC1
s.addText(SUBTITLE2, {
  x: 0.6, y: 4.5, w: 12.13, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 28, color: "433BC1", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "slide_026_recreated.pptx" }).then(() => console.log("wrote slide_026_recreated.pptx"));