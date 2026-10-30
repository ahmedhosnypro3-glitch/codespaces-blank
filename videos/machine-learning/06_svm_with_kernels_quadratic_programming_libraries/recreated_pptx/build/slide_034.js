// slide_034.js — "How to Kernelize SVM" (v2: judge-fix round)
// Judge FAIL findings addressed: color-coded serif equations, typeset inline math
// (true sub/superscript runs), panel border, box-fit, inline (not display) kernel term.
// Adjudicated & DISMISSED (house rule / measurement): 4:3 vs 16:9 aspect claim
// (original frame is 960x540 = 16:9, same as recreation), badge numeral color #333333
// (house rule mandates), yellow-badge shape (house rule overrides per-slide).
// Run: NODE_PATH=$(npm root -g) node slide_034.js

const pptxgen = require("pptxgenjs");

const NUM = 34;
const TITLE = "How to Kernelize SVM";
const FONT = "Arial";
const MATH = "Times New Roman";
const W = 13.33, H = 7.5;
const EQ = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_034/";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// 1. House red frame (0.15in inset)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position at y=0.28)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Cream content panel with thin red/maroon border (judge fix #6)
const creamY = 0.95;
const creamH = 3.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.6, y: creamY, w: 10.13, h: creamH,
  fill: { color: "FFFFE0" }, line: { color: "C00000", width: 1 },
});

// 5. Color-coded Lagrangian (blue vars, red alphas/operators)
s.addImage({
  path: EQ + "eq1_lagrangian_multi.png",
  x: 2.0, y: creamY + 0.2, w: 5.40667, h: 0.995,
});

// 6. W and b boxes sized to hug their content (judge fix #7)
const formulaY = creamY + 1.3;
// W box — hugs the W equation
const wImgW = 2.01167, wImgH = 0.95;
const wBoxW = wImgW + 0.3;
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.8, y: formulaY, w: wBoxW, h: wImgH + 0.16,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 },
});
s.addImage({ path: EQ + "eq2_W_multi.png", x: 1.95, y: formulaY + 0.06, w: wImgW, h: wImgH });
// b box — hugs the b equation
const bImgW = 6.26, bImgH = 0.44667;
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.8 + wBoxW + 0.2, y: formulaY + 0.18, w: bImgW + 0.3, h: bImgH + 0.16,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 },
});
s.addImage({ path: EQ + "eq3_b_multi.png", x: 1.95 + wBoxW + 0.2, y: formulaY + 0.22, w: bImgW, h: bImgH });

// 7. Classification strip, narrower bordered box (judge fix #16)
const classY = formulaY + 1.25;
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.2, y: classY, w: 6.9, h: 0.42,
  fill: { color: "FFCC99" }, line: { color: "C00000", width: 1 },
});
s.addText([
  { text: "Class of vector ", options: { color: "C00000", fontFace: FONT } },
  { text: "Z", options: { color: "C00000", bold: true, fontFace: MATH } },
  { text: " \u21d2 sign(", options: { color: "C00000", fontFace: MATH } },
  { text: "W", options: { color: "C00000", fontFace: MATH } },
  { text: "T", options: { color: "C00000", fontFace: MATH, superscript: true } },
  { text: " Z + b)", options: { color: "C00000", fontFace: MATH } },
], {
  x: 3.2, y: classY, w: 6.9, h: 0.42,
  align: "center", valign: "middle",
  fontSize: 16, color: "C00000", fontFace: MATH, margin: 0,
});

// 8. Remember section — full-width blue-bordered frame below cream panel
const rememberY = creamY + creamH + 0.2;
const rememberH = 2.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: rememberY, w: 12.3, h: rememberH,
  fill: { type: "none" }, line: { color: "0000FF", width: 1.5 },
});
// Remember header — bold italic (judge fix #14)
s.addText("Remember :", {
  x: 0.7, y: rememberY + 0.05, w: 11.8, h: 0.32,
  align: "left", fontSize: 15, bold: true, italic: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// 9. Mapping row — inline true sub/superscript runs (judge fix #3)
const mapY = rememberY + 0.42;
s.addText([
  { text: "Mapping", options: { fontSize: 14, bold: true, italic: true, color: "FF0000", fontFace: FONT, margin: 0 } },
  { text: "  Instead of using ", options: { fontSize: 13, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "X", options: { fontSize: 13, bold: true, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 13, bold: true, color: "0000FF", fontFace: MATH, subscript: true, margin: 0 } },
  { text: " (of dimension ", options: { fontSize: 13, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "d", options: { fontSize: 13, italic: true, bold: true, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: ") use ", options: { fontSize: 13, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "\u03c6(X", options: { fontSize: 13, bold: true, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 13, bold: true, color: "0000FF", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ") (with higher dimension )", options: { fontSize: 13, italic: true, color: "FF0000", fontFace: FONT, underline: true, margin: 0 } },
], {
  x: 0.7, y: mapY, w: 11.9, h: 0.3,
  align: "left", valign: "middle", margin: 0,
});

// 10. Mapping math line — red arrow (judge fix #13)
s.addImage({ path: EQ + "eq4_mapping.png", x: 3.2, y: mapY + 0.32, w: 2.845, h: 0.45667 });

// 11. Kernelization row — inline kernel term (judge fix #11), full parenthetical (fix #1)
const kernY = mapY + 0.9;
s.addText([
  { text: "Kernelization", options: { fontSize: 14, bold: true, italic: true, color: "FF0000", fontFace: FONT, margin: 0 } },
  { text: "  Instead of using ", options: { fontSize: 13, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "\u03c6(X", options: { fontSize: 13, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 13, color: "0000FF", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ")", options: { fontSize: 13, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: "T", options: { fontSize: 13, color: "0000FF", fontFace: MATH, superscript: true, margin: 0 } },
  { text: " \u03c6(X", options: { fontSize: 13, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 13, color: "0000FF", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ")", options: { fontSize: 13, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: "T", options: { fontSize: 13, color: "0000FF", fontFace: MATH, superscript: true, margin: 0 } },
  { text: " use ", options: { fontSize: 13, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "K", options: { fontSize: 13, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: " (X", options: { fontSize: 13, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 13, color: "FF0000", fontFace: MATH, subscript: true, margin: 0 } },
  { text: "T", options: { fontSize: 13, color: "FF0000", fontFace: MATH, superscript: true, margin: 0 } },
  { text: " , X", options: { fontSize: 13, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: "j", options: { fontSize: 13, color: "FF0000", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ") (Where ", options: { fontSize: 13, italic: true, color: "FF0000", fontFace: FONT, margin: 0 } },
  { text: "K", options: { fontSize: 13, italic: true, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: " is one of kernel functions)", options: { fontSize: 13, italic: true, color: "FF0000", fontFace: FONT, margin: 0 } },
], {
  x: 0.7, y: kernY, w: 11.9, h: 0.3,
  align: "left", valign: "middle", margin: 0,
});

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_034_recreated.pptx" })
  .then(() => console.log("wrote slide_034_recreated.pptx"))
  .catch(err => console.error(err));