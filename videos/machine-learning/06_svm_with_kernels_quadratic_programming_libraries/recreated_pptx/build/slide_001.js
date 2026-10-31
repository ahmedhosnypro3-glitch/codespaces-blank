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
const CX = 13.33 / 2;

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

// House chrome: title box at y=0.28. Two separate single-line boxes place the
// title ink at the original's measured position (norm y 0.335-0.393 / 0.465-0.53)
s.addText("SVM with Kernels &", {
  x: 0.6, y: 2.42, w: 12.13, h: 0.62, align: "center", valign: "middle",
  fontSize: 40, bold: true, color: "C00000", fontFace: SANS, margin: 0, wrap: false,
});
s.addText("Quadratic Programming Libraries", {
  x: 0.6, y: 3.44, w: 12.13, h: 0.58, align: "center", valign: "middle",
  fontSize: 38, bold: true, color: "C00000", fontFace: SANS, margin: 0, wrap: false,
});

// body text helper (inches); boxes wider than the ink so nothing wraps
function txt(str, x, y, w, h, size, color, align, font) {
  s.addText(str, {
    x, y, w, h, align, valign: "middle", wrap: false,
    fontSize: size, bold: true, color, fontFace: font || SANS, margin: 0,
  });
}

// Prepared By block (centered); y from original ink bands
txt("Prepared By", CX - 0.9, 4.68, 1.8, 0.32, 18, RED, "center", SERIF);
txt("Dr. Khaled Mostafa ElSayed", CX - 1.7, 5.02, 3.4, 0.32, 16, BLUE, "center");
txt("kmelsayed@zewailcity.edu.eg", CX - 1.5, 5.36, 3.0, 0.24, 13, BLUE, "center");

// Instructors block (left)
txt("Instructors:", 1.333, 5.62, 1.6, 0.26, 18, RED, "left", SERIF);
txt("Dr. Khaled Mostafa ElSayed", 1.333, 5.98, 3.2, 0.26, 16, BLUE, "left");
txt("kmelsayed@zewailcity.edu.eg", 1.333, 6.26, 2.8, 0.22, 13, BLUE, "left");
txt("Dr. Mohamed Maher Ata", 1.333, 6.52, 2.8, 0.26, 16, NAVY, "left");
txt("momaher@zewailcity.edu.eg", 1.333, 6.80, 2.8, 0.22, 13, BLUE, "left");

// Zewail City logo block: teal field, white mountain emblem, Arabic + ZEWAIL CITY + English lines
const lx = 0.61 * 13.33, ly = 6.05, lw = (0.83 - 0.61) * 13.33, lh = 0.95;
s.addShape(pres.shapes.RECTANGLE, {
  x: lx, y: ly, w: lw, h: lh,
  fill: { color: "007E7A" }, line: { color: "007E7A", width: 0.75 },
});
// white mountain emblem at the left of the logo
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: lx + 0.10, y: ly + 0.14, w: 0.48, h: 0.66,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0.5 },
});
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: lx + 0.42, y: ly + 0.38, w: 0.36, h: 0.44,
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0.5 },
});
// logo text: three separate single-line boxes, right of the emblem
const tx = lx + 0.88, tw = lw - 0.94;
s.addText("جامعة العلوم والتكنولوجيا", {
  x: tx, y: ly + 0.05, w: tw, h: 0.24, align: "center", valign: "middle",
  fontSize: 8, bold: false, color: "FFFFFF", fontFace: SANS, margin: 0, wrap: false,
});
s.addText("ZEWAIL CITY", {
  x: tx, y: ly + 0.32, w: tw, h: 0.28, align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: SANS, margin: 0, wrap: false,
});
s.addText("University of Science and Technology", {
  x: tx, y: ly + 0.62, w: tw, h: 0.28, align: "center", valign: "middle",
  fontSize: 7, bold: false, color: "FFFFFF", fontFace: SANS, margin: 0, wrap: false,
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_001_recreated.pptx") })
  .then(() => console.log("wrote slide_001_recreated.pptx"));
