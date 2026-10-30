// Slide 001 attempt 2: fixes vs slide_001.js (attempt 1)
//  - add missing SERIF binding (attempt 1 crashes: ReferenceError: SERIF is not defined)
//  - logo: embed exact crop of the original lockup at measured position
//    original frame 960x540, crop (588,436)-(840,513) -> 252x77 px
//    inches: x=588/960*13.33, y=436/540*7.5, w=252/960*13.33, h=77/540*7.5
const pptxgen = require("pptxgenjs");

const FONT = "Arial";
const SERIF = "Times New Roman";
const NUM = 1;
const TITLE = "Neural Network";
const SUBTITLE = "Back Propagation Training Algorithm";

const BG = "E8E8E8";
const TITLE_COLOR = "D32F2F";
const SUBTITLE_COLOR = "D32F2F";
const COURSE_COLOR = "1565C0";
const BODY_COLOR = "1565C0";
const LABEL_COLOR = "D32F2F";
const FRAME_COLOR = "C00000";
const BADGE_FILL = "FFF9C4";
const BADGE_LINE = "FFF9C4";
const BADGE_TEXT = "333333";

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example";
const OUT = process.argv[2] || (NS + "/qa/slide001/rejudge/r2/slide_001_attempt2.pptx");

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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 44, bold: true, color: TITLE_COLOR, fontFace: SERIF, margin: 0,
});
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
s.addText("Prepared By", {
  x: 0.6, y: 2.50, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 22, italic: true, color: LABEL_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 0.6, y: 2.95, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 22, bold: true, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 0.6, y: 3.35, w: 12.13, h: 0.35,
  align: "center", valign: "top",
  fontSize: 16, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});

// ========== INSTRUCTORS BLOCK (bottom left) ==========
const INS_X_LABEL = 1.2;
const INS_X_NAME = 1.8;
const INS_X_EMAIL = 1.8;
const INS_Y_START = 5.10;
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
  x: INS_X_EMAIL, y: INS_Y_START + 2 * INS_LINE_H, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 14, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: INS_X_NAME, y: INS_Y_START + 3 * INS_LINE_H, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 20, bold: true, italic: true, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: INS_X_EMAIL, y: INS_Y_START + 4 * INS_LINE_H, w: 5.0, h: INS_LINE_H,
  align: "left", valign: "top",
  fontSize: 14, color: BODY_COLOR, fontFace: SERIF, margin: 0,
});

// ========== UNIVERSITY LOGO (bottom right) ==========
// Exact crop of the original lockup: frame px (588,436)-(840,513) on 960x540,
// mapped to inches at 13.33x7.5 (aspect preserved: 252/77 = 3.5/1.0694).
s.addImage({
  path: NS + "/recreated_pptx/build/assets/logo_slide001_crop.png",
  x: 588 / 960 * 13.33, y: 436 / 540 * 7.5,
  w: 252 / 960 * 13.33, h: 77 / 540 * 7.5,
});

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(err => { console.error(err); process.exit(1); });
