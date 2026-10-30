const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 1;
const TITLE = "Neural Network";
const SUBTITLE = "Back Propagation Training Algorithm";

const BG = "E8E8E8";              // House background
const TITLE_COLOR = "D32F2F";     // Red from spec
const SUBTITLE_COLOR = "D32F2F";  // Red from spec
const COURSE_COLOR = "1565C0";    // Blue from spec
const BODY_COLOR = "1565C0";      // Blue from spec
const LABEL_COLOR = "D32F2F";     // Red for labels
const FRAME_COLOR = "C00000";     // House red frame
const BADGE_FILL = "FFF9C4";      // House badge
const BADGE_LINE = "FFF9C4";      // House badge line
const BADGE_TEXT = "333333";      // House badge text

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME_COLOR, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_FILL }, line: { color: BADGE_LINE, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});
// Title box at house position
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 44, bold: true, color: TITLE_COLOR, fontFace: SERIF, margin: 0,
});
// Subtitle below title
s.addText(SUBTITLE, {
  x: 0.6, y: 0.85, w: 12.13, h: 0.65,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: SUBTITLE_COLOR, fontFace: SERIF, margin: 0,
});

// ========== COURSE INFO (centered) ==========
s.addText("CSAI 253 - Spring 2024", {
  x: 0.6, y: 1.80, w: 12.13, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: COURSE_COLOR, fontFace: SERIF, margin: 0,
});

// ========== PREPARED BY BLOCK (centered, 3 lines) ==========
// "Prepared By" - red italic serif
s.addText("Prepared By", {
  x: 0.6, y: 2.50, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 22, italic: true, color: LABEL_COLOR, fontFace: SERIF, margin: 0,
});
// Author name - blue bold serif
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 0.6, y: 2.95, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 22, bold: true, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});
// Email - blue regular serif (smaller)
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 0.6, y: 3.35, w: 12.13, h: 0.35,
  align: "center", valign: "top",
  fontSize: 16, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});

// ========== INSTRUCTORS BLOCK (bottom left, 5 lines with indentation) ==========
// Move lower to match original (y ~5.1 start)
const INS_X_LABEL = 1.2;    // Label position
const INS_X_NAME = 1.8;     // Name indented
const INS_X_EMAIL = 1.8;    // Email same as name
const INS_Y_START = 5.10;   // Moved lower to match original
const INS_LINE_H = 0.38;

s.addText("Instructors:", {
  x: INS_X_LABEL, y: INS_Y_START, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: LABEL_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: INS_X_NAME, y: INS_Y_START + INS_LINE_H, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: INS_X_EMAIL, y: INS_Y_START + 2*INS_LINE_H, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 14, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: INS_X_NAME, y: INS_Y_START + 3*INS_LINE_H, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: INS_X_EMAIL, y: INS_Y_START + 4*INS_LINE_H, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 14, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});

// ========== UNIVERSITY LOGO (bottom right) ==========
// Embed the extracted logo image
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets/logo_slide001.png",
  x: 10.5, y: 6.10, w: 2.6, h: 1.2,
});

const BASEDIR = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example";

pres.writeFile({ fileName: BASEDIR + "/_pool/probe_slide_001_build.pptx" })
  .then(() => console.log("wrote slide_001_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });