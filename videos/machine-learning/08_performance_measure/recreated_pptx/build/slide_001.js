// Slide 001 — Classifications Performance Measures (cover slide)
// Rebuild from PIL measurements of unique_slides/slide_001.jpg (960x540 px, 1px = 1pt = 1/72 in).
//
// FRAME-vs-SPEC DEVIATIONS (frame is ground truth):
//  - Title: spec/final JSON already corrected to "Classifications Performance Measures"
//    (the raw JSON's "ZEWIAL CITY OF SCIENCE AND TECHNOLOGY" logo text is NOT the title).
//  - Logo wordmark spelling: raw JSON "ZEWIAL CITY" -> final JSON "ZEWAIL CITY" (validation fix);
//    the teal emblem carries this wordmark, so the recreation draws "ZEWAIL CITY".
//  - Logo Arabic label: spec_drift/spec_gaps slide_001 REQUIRED verbatim label is
//    "جامعة العلوم والتكنولوجيا" (confirmed by doc-parse crop + pixel width: ink w=186px at
//    960x540; the longer "جامعة زويل للعلوم والتكنولوجيا" renders 219px+ and does not fit).
//    Rendered with rtlMode:true, centered in the white panel as in the original.
//  - Teal emblem measured #0FADAE (spec said #1abc9c); its artwork is a lighter teal #58C6C5,
//    not white (local-contrast analysis of the 80x69px emblem).
//  - Logo English line reads as thin light strokes; Arabic line is the dark one in the original.
//  - Text colors re-measured from frame core ink: red ~#C00000, blue ~#0000CC (was C0392B/2980B9).
//  - Background measured #E7E9E6; house rule #E8E8E8 wins.
//  - Original's own red frame is a U-shape inset 59px/44px; house chrome (0.15in full rect) wins.
//  - Original badge: yellow #EFED9F circle at 12.16in/0.68in; house badge geometry/color win.
//  - Cover title is body content at y=2.36in in the original (not a y=0.28 header title),
//    so it is reproduced at its measured position; the house title box rule targets header titles.
//  - Black bar below y=518px is a video-capture artifact and is omitted.
//
// Font sizes below are closed-loop derived: attempt 1 measured each rendered band's ink width
// against the original's; sizes were set = attempt1_size * target_width / measured_width.
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const FONT = "Arial";
const AR_FONT = "Noto Kufi Arabic";
const BG = "E8E8E8";
const FRAME = "C00000";
const RED = "C00000";
const BLUE = "0000CC";
const TEAL = "0FADAE";
const TEAL_LT = "58C6C5";
const LOGO_DARK = "3A1028";
const LOGO_GRAY = "5A5A5A";
const BADGE = "FFF9C4";
const INK = "333333";
const WHITE = "FFFFFF";

const s = pres.addSlide();
s.background = { color: BG };

// ---- house chrome ---------------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("1", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- title (original: line1 glyph top 170px, line2 224px, pitch 54px) -----
s.addText("Classifications\nPerformance Measures", {
  x: 0.6, y: 2.22, w: 12.13, h: 1.55, align: "center", valign: "top",
  fontSize: 48, bold: true, color: RED, fontFace: FONT, margin: 0,
  lineSpacing: 54, charSpacing: -0.31,
});

// ---- course code (original glyph top 284px) ------------------------------
s.addText("CSAI 253 - Spring 2024", {
  x: 0.6, y: 3.86, w: 12.13, h: 0.5, align: "center", valign: "top",
  fontSize: 28, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- "Prepared By" block (original: 339/362/387px glyph tops, centered x=489) --
s.addText("Prepared By", {
  x: 0.725, y: 4.63, w: 12.13, h: 0.4, align: "center", valign: "top",
  fontSize: 19, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 0.725, y: 4.95, w: 12.13, h: 0.45, align: "center", valign: "top",
  fontSize: 22.3, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 0.725, y: 5.30, w: 12.13, h: 0.4, align: "center", valign: "top",
  fontSize: 16, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- "Instructors:" block (original: label x=87px, entries x=125px) --------
s.addText("Instructors:", {
  x: 1.208, y: 5.56, w: 3.0, h: 0.4, align: "left", valign: "top",
  fontSize: 21.5, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("Dr. Khaled Mostafa ElSayed", {
  x: 1.736, y: 5.94, w: 4.5, h: 0.4, align: "left", valign: "top",
  fontSize: 20.5, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("kmelsayed@zewailcity.edu.eg", {
  x: 1.736, y: 6.25, w: 4.5, h: 0.35, align: "left", valign: "top",
  fontSize: 15, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Dr. Mohamed Maher Ata", {
  x: 1.736, y: 6.53, w: 4.5, h: 0.4, align: "left", valign: "top",
  fontSize: 20.2, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("momaher@zewailcity.edu.eg", {
  x: 1.736, y: 6.84, w: 4.5, h: 0.35, align: "left", valign: "top",
  fontSize: 15, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- university logo (original: teal 594..674 / white panel 677..884, y441..508) ----
// emblem artwork is a LIGHTER TEAL in the original, not white
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.25, y: 6.125, w: 1.125, h: 0.958, fill: { color: TEAL }, line: { type: "none" },
});
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: 8.55, y: 6.17, w: 0.55, h: 0.40, fill: { color: TEAL_LT }, line: { type: "none" },
});
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: 8.70, y: 6.28, w: 0.32, h: 0.29, fill: { color: TEAL }, line: { type: "none" },
});
s.addText("ZEWAIL CITY", {
  x: 8.19, y: 6.62, w: 1.25, h: 0.12, align: "center", valign: "top",
  fontSize: 5.5, bold: true, color: TEAL_LT, fontFace: FONT, margin: 0,
});
s.addText("OF SCIENCE AND TECHNOLOGY", {
  x: 8.19, y: 6.76, w: 1.25, h: 0.12, align: "center", valign: "top",
  fontSize: 5.5, bold: true, color: TEAL_LT, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.403, y: 6.125, w: 2.875, h: 0.93, fill: { color: WHITE }, line: { type: "none" },
});
s.addText("جامعة العلوم والتكنولوجيا", {
  x: 9.403, y: 6.40, w: 2.875, h: 0.32, align: "center", valign: "top",
  fontSize: 16.5, bold: false, color: LOGO_DARK, fontFace: AR_FONT, margin: 0,
  rtlMode: true,
});
s.addText("University of Science and Technology", {
  x: 9.403, y: 6.74, w: 2.875, h: 0.28, align: "center", valign: "top",
  fontSize: 10.5, bold: false, color: LOGO_GRAY, fontFace: FONT, margin: 0,
});

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_001_recreated.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out)).catch((e) => { console.error(e); process.exit(1); });
