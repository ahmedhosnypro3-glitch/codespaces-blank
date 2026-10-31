// Pattern: house-chrome + slide 001 content (wave-3 rejudge: emblem added to logo tile, logo kept inside frame)
// Build: NODE_PATH=$(npm root -g) node slide_001_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 1;
const FONT = "Times New Roman";  // serif for lower half per judge
const TITLE_FONT = "Arial";      // title remains sans-serif
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };  // house template background

// 1. outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: TITLE_FONT, margin: 0,
});

// 3. title box - TWO LINES per original (line break after "Introduction to")
// Judge: title ~44pt, line spacing ~1.35x cap-to-cap
s.addText("Introduction to", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "top",
  fontSize: 44, bold: true, color: "C00000", fontFace: TITLE_FONT, margin: 0,
});
s.addText("Artificial Neural Networks (ANN)", {
  x: 0.6, y: 0.88, w: 12.13, h: 0.6,
  align: "center", valign: "top",
  fontSize: 44, bold: true, color: "C00000", fontFace: TITLE_FONT, margin: 0,
});

// 4. course code - Judge: ~24pt, extra spaces around hyphen
s.addText("CSAI 253  -  Spring 2024", {
  x: 0.6, y: 1.55, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "000080", fontFace: TITLE_FONT, margin: 0,
});

// 5. Prepared By block (centered) - Judge: ~26pt (was ~35% too large)
s.addText("Prepared By", {
  x: 0.6, y: 2.35, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 26, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 0.6, y: 2.85, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 22, bold: true, italic: true, color: "000080", fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 0.6, y: 3.35, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 18, italic: true, color: "000080", fontFace: FONT, margin: 0,
});

// 6. Instructors list (bottom-left)
// Measured from the original frame: "Instructors:" label ink starts x=87,
// names/emails indent to x=125; label->name gap 26px, name->email 22px,
// email->next-name 21px. At 960x540, 1px = 1pt.
const instLabelX = 1.21;  // label left edge
const instX = 1.74;       // names/emails indent
s.addText("Instructors:", {
  x: instLabelX, y: 4.0, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 22, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: instX, y: 4.40, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: "000080", fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: instX, y: 4.74, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 16, italic: true, color: "000080", fontFace: FONT, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: instX, y: 5.00, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: "000080", fontFace: FONT, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: instX, y: 5.33, w: 5.0, h: 0.45,
  align: "left", valign: "top",
  fontSize: 16, italic: true, color: "000080", fontFace: FONT, margin: 0,
});

// 7. University logo box (bottom-right) - two panels: left teal with emblem, right white with text
// Judge: original teal ~1.2in wide, white ~3.0in (1:2.6), bottom-aligned to frame
// Left panel (teal) with the white mountain+wave emblem above the wordmark
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.0, y: 6.0, w: 1.2, h: 1.2,
  fill: { color: "008080" },
  line: { color: "C00000", width: 1 },
});
s.addImage({ path: "assets/logo_emblem_001.png", x: 9.05, y: 6.05, w: 1.1, h: 0.4 });
s.addText("ZEWAIL CITY", {
  x: 9.0, y: 6.5, w: 1.2, h: 0.3,
  align: "center", valign: "top",
  fontSize: 12, bold: true, color: "FFFFFF", fontFace: TITLE_FONT, margin: 0,
});
s.addText("SCIENCE & TECHNOLOGY", {
  x: 9.0, y: 6.78, w: 1.2, h: 0.22,
  align: "center", valign: "top",
  fontSize: 6, color: "FFFFFF", fontFace: TITLE_FONT, margin: 0,
});

// Right panel (white) - NO border, Arabic dark red/maroon, English black
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.2, y: 6.0, w: 2.8, h: 1.2,
  fill: { color: "FFFFFF" },
  line: { type: "none" },
});
// Arabic in dark red/maroon (#8B0000 approx), bold
s.addText("جامعة العلوم والتكنولوجيا زويل", {
  x: 10.3, y: 6.1, w: 2.6, h: 0.5,
  align: "left", valign: "top",
  fontSize: 12, bold: true, color: "8B0000", fontFace: "Arial", margin: 0,
});
// English in black, single line, not wrapped
s.addText("University of Science and Technology", {
  x: 10.3, y: 6.6, w: 2.6, h: 0.35,
  align: "left", valign: "top",
  fontSize: 10, color: "000000", fontFace: TITLE_FONT, margin: 0,
});

// 8. Bottom black band (present in the original frame at rows 519-539), below the house frame rule
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.0, y: H - 0.15, w: W, h: 0.15,
  fill: { color: "000000" },
  line: { type: "none" },
});

pres.writeFile({ fileName: "slide_001_recreated.pptx" }).then(() => console.log("wrote slide_001_recreated.pptx"));