const pptxgen = require("pptxgenjs");
const path = require("path");

// Slide 001 rebuild from qa/reanalysis2/slide_001_analysis.txt (title slide, no math/graphs)
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const NUM = 1;
const W = 13.33, H = 7.5;
const RED = "A61106";   // spec heading/label ink
const BLUE = "0000CC";  // spec body ink
const NAVY = "000080";  // second instructor name, darker shade per judge
const SANS = "Arial";
const SERIF = "Times New Roman";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome: outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// House chrome: slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: SANS, margin: 0,
});

// House chrome: title box starts at y=0.28; tall box + valign bottom + line
// spacing puts the two title lines at the original's vertical position
// (orig title ink at normalized y 0.335-0.53 = 2.51-3.98 in)
s.addText([
  { text: "SVM with Kernels &", options: { fontSize: 40, bold: true, color: "C00000", fontFace: SANS } },
  { text: "Quadratic Programming Libraries", options: { fontSize: 38, bold: true, color: "C00000", fontFace: SANS } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 3.75,
  align: "center", valign: "bottom", margin: 0, lineSpacing: 56,
});

// body text helper (inches)
function txt(str, x, y, w, h, size, color, align, font) {
  s.addText(str, {
    x, y, w, h, align, valign: "middle",
    fontSize: size, bold: true, color, fontFace: font || SANS, margin: 0,
  });
}

// Prepared By block (centered); y from original ink bands, x/w from spec
txt("Prepared By", 0.46 * 13.33, 4.68, 0.08 * 13.33, 0.30, 18, RED, "center", SERIF);
txt("Dr. Khaled Mostafa ElSayed", 0.43 * 13.33, 5.02, 0.14 * 13.33, 0.30, 16, BLUE, "center");
txt("kmelsayed@zewailcity.edu.eg", 0.41 * 13.33, 5.36, 0.18 * 13.33, 0.22, 13, BLUE, "center");

// Instructors block (left)
txt("Instructors:", 0.10 * 13.33, 5.62, 0.07 * 13.33, 0.24, 18, RED, "left", SERIF);
txt("Dr. Khaled Mostafa ElSayed", 0.13 * 13.33, 5.98, 0.17 * 13.33, 0.24, 16, BLUE, "left");
txt("kmelsayed@zewailcity.edu.eg", 0.13 * 13.33, 6.26, 0.16 * 13.33, 0.20, 13, BLUE, "left");
txt("Dr. Mohamed Maher Ata", 0.13 * 13.33, 6.52, 0.14 * 13.33, 0.24, 16, NAVY, "left");
txt("momaher@zewailcity.edu.eg", 0.13 * 13.33, 6.80, 0.17 * 13.33, 0.20, 13, BLUE, "left");

// Zewail City logo block: teal field, white mountain emblem, Arabic + ZEWAIL CITY + English lines
const lx = 0.61 * 13.33, ly = 6.05, lw = (0.83 - 0.61) * 13.33, lh = 0.95;
s.addShape(pres.shapes.RECTANGLE, {
  x: lx, y: ly, w: lw, h: lh,
  fill: { color: "007E7A" }, line: { color: "007E7A", width: 0.75 },
});
// white mountain emblem at the left of the logo
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: lx + 0.12, y: ly + 0.16, w: 0.46, h: 0.62,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0.5 },
});
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: lx + 0.44, y: ly + 0.38, w: 0.34, h: 0.42,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0.5 },
});
// logo text lines in white, right of the emblem
s.addText([
  { text: "جامعة العلوم والتكنولوجيا", options: { fontSize: 8, bold: false, color: "FFFFFF", fontFace: SANS } },
  { text: "ZEWAIL CITY", options: { fontSize: 11, bold: true, color: "FFFFFF", fontFace: SANS } },
  { text: "University of Science and Technology", options: { fontSize: 8, bold: false, color: "FFFFFF", fontFace: SANS } },
], {
  x: lx + 0.92, y: ly, w: lw - 1.0, h: lh,
  align: "center", valign: "middle", margin: 0, lineSpacing: 14,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_001_recreated.pptx") })
  .then(() => console.log("wrote slide_001_recreated.pptx"));
