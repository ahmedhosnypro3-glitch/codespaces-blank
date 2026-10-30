const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 4;
const TITLE = "Quadratic Coefficients";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. Badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Subtitle
s.addText("Two Variables Example", {
  x: 0.6, y: 0.9, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 5. Matrix expansion box
let y = 1.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: y, w: 12.3, h: 2.5,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});

s.addText("( x1  x2 ) [ a11  a12 ] [ x1 ]   = ( a11 x1 + a21 x2  a12 x1 + a22 x2 ) [ x1 ]", {
  x: 0.6, y: y + 0.1, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("                [ a21  a22 ] [ x2 ]       ( a11 x1 + a21 x2 )x1 + (a12 x1 + a22 x2)x2", {
  x: 0.6, y: y + 0.35, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("                = a11 x1^2 + a21 x1 x2 + a12 x1 x2 + a22 x2^2", {
  x: 0.6, y: y + 0.6, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("                = a11 x1^2 + (a21 + a12) x1 x2 + a22 x2^2 => Quadratic form", {
  x: 0.6, y: y + 0.85, w: 12.0, h: 0.3,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 6. Coefficient definitions box
y += 2.7;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: y, w: 12.3, h: 1.5,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});
s.addText("a11 => Coefficient of x1^2", {
  x: 0.6, y: y + 0.1, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a21 + a12 => Coefficient of x1 x2 => a12 = a21 = 1/2 Coefficient of x1 x2", {
  x: 0.6, y: y + 0.35, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a22 => Coefficient of x2^2", {
  x: 0.6, y: y + 0.6, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});

// 7. Numerical mapping box
y += 1.7;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: y, w: 12.3, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});
s.addText("( x1  x2 ) [ a11  a12 ]   =>   [ coef of x1^2     0.5 coef of x1 x2 ]", {
  x: 0.6, y: y + 0.1, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("                [ a21  a22 ]           [ 0.5 coef of x1 x2   coef of x2^2 ]", {
  x: 0.6, y: y + 0.35, w: 12.0, h: 0.3,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("(Note: symmetric matrix - off-diagonal elements are half the cross-term coefficient)", {
  x: 0.6, y: y + 0.6, w: 12.0, h: 0.3,
  fontSize: 12, color: "666666", fontFace: FONT, margin: 0,
});

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_004_recreated.pptx" })
  .then(() => console.log("wrote slide_004_recreated.pptx"))
  .catch(e => console.error(e));