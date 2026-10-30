const pptxgen = require("pptxgenjs");

// Slide 001 (title slide) — fresh build from qa/reanalysis2/slide_001_analysis.txt only.
const NUM = 1;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const RED = "A61106";   // headings/labels per spec colors
const BLUE = "0000CC";  // names/emails per spec colors

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (mandatory, overrides spec) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
// two-line title in the house title box (wide box, explicit newline)
s.addText("SVM with Kernels &\nQuadratic Programming Libraries", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.3,
  align: "center", valign: "top", margin: 0,
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT,
});

// ---- spec content at measured y; wide boxes so text never wraps/overlaps ----
// normalized y -> inches: y*7.5. Centered lines span the title width; left lines start at 0.10*13.33.
function cline(ynorm, text, size, color) {
  s.addText(text, {
    x: 0.6, y: ynorm * 7.5, w: 12.13, h: 0.42,
    align: "center", valign: "top", fontSize: size, bold: true,
    color, fontFace: FONT, margin: 0,
  });
}
function lline(ynorm, text, size, color) {
  s.addText(text, {
    x: 0.10 * 13.33, y: ynorm * 7.5, w: 9.5, h: 0.42,
    align: "left", valign: "top", fontSize: size, bold: true,
    color, fontFace: FONT, margin: 0,
  });
}
// Prepared By block (centered, red label / blue name+email)
cline(0.53, "Prepared By", 18, RED);
cline(0.57, "Dr. Khaled Mostafa ElSayed", 16, BLUE);
cline(0.62, "kmelsayed@zewailcity.edu.eg", 13, BLUE);

// Instructors block (left, red label / blue name+email pairs)
lline(0.70, "Instructors:", 18, RED);
lline(0.75, "Dr. Khaled Mostafa ElSayed", 16, BLUE);
lline(0.80, "kmelsayed@zewailcity.edu.eg", 13, BLUE);
lline(0.84, "Dr. Mohamed Maher Ata", 16, BLUE);
lline(0.89, "momaher@zewailcity.edu.eg", 13, BLUE);

// ---- Zewail City logo block, bottom right: [0.61,0.80,0.83,0.88] ----
const lg = { x: 0.61 * 13.33, y: 0.80 * 7.5, w: (0.83 - 0.61) * 13.33, h: (0.88 - 0.80) * 7.5 };
s.addShape(pres.shapes.RECTANGLE, {
  x: lg.x, y: lg.y, w: lg.w, h: lg.h,
  fill: { color: "007E7A" }, line: { color: "007E7A", width: 0 },
});
// white emblem mark at left of the teal box
s.addShape(pres.shapes.OVAL, {
  x: lg.x + 0.12, y: lg.y + 0.10, w: 0.40, h: 0.40,
  fill: { type: "none" }, line: { color: "FFFFFF", width: 2 },
});
// white Arabic line over English line (web-verified: جامعة العلوم والتكنولوجيا)
s.addText("جامعة العلوم والتكنولوجيا", {
  x: lg.x + 0.60, y: lg.y + 0.05, w: lg.w - 0.68, h: 0.27,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("University of Science and Technology", {
  x: lg.x + 0.60, y: lg.y + 0.32, w: lg.w - 0.68, h: 0.24,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_001_recreated.pptx" })
  .then(() => console.log("wrote slide_001_recreated.pptx"))
  .catch(e => console.error(e));
