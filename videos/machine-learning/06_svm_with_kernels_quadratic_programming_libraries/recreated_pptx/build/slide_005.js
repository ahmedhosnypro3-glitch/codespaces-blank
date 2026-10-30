const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 5;
const TITLE = "Quadratic Coefficients (Three Variables)";
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

// 4. Matrix expansion box
let y = 0.9;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: y, w: 12.3, h: 3.5,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});

s.addText("( x1  x2  x3 ) [ a11  a12  a13 ] [ x1 ]   =   [ a11 x1 + a21 x2 + a31 x3   a12 x1 + a22 x2 + a32 x3   a13 x1 + a23 x2 + a33 x3 ] [ x1 ]", {
  x: 0.6, y: y + 0.1, w: 12.0, h: 0.3,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("                [ a21  a22  a23 ] [ x2 ]       ( a11 x1 + a21 x2 + a31 x3 ) x1 + ( a12 x1 + a22 x2 + a32 x3 ) x2 + ( a13 x1 + a23 x2 + a33 x3 ) x3", {
  x: 0.6, y: y + 0.35, w: 12.0, h: 0.3,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("                [ a31  a32  a33 ] [ x3 ]", {
  x: 0.6, y: y + 0.6, w: 12.0, h: 0.3,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("= a11 x1^2 + a22 x2^2 + a33 x3^2 + (a21+a12) x1 x2 + (a31+a13) x1 x3 + (a32+a23) x2 x3 => Quadratic form", {
  x: 0.6, y: y + 0.85, w: 12.0, h: 0.3,
  fontSize: 13, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("a11 => Coefficient of X1^2", {
  x: 0.6, y: y + 1.2, w: 12.0, h: 0.25,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a22 => Coefficient of X2^2", {
  x: 0.6, y: y + 1.4, w: 12.0, h: 0.25,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a33 => Coefficient of X3^2", {
  x: 0.6, y: y + 1.6, w: 12.0, h: 0.25,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a21+a12 => Coefficient of x1 x2 => a12=a21=1/2 coeff of x1 x2", {
  x: 0.6, y: y + 1.85, w: 12.0, h: 0.25,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a13+a31 => Coefficient of x1 x3 => a13=a31=1/2 coeff of x1 x3", {
  x: 0.6, y: y + 2.1, w: 12.0, h: 0.25,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a32+a23 => Coefficient of x2 x3 => a32=a23=1/2 coeff of x2 x3", {
  x: 0.6, y: y + 2.35, w: 12.0, h: 0.25,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});

// 5. Mapping box (bottom)
y += 4.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: y, w: 12.3, h: 2.5,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});
s.addText("[ x1  x2  x3 ] [ a11  a12  a13 ]   =>   [ a11   a12=a21   a13=a31 ]   [ coef x1^2   0.5 coef x1x2   0.5 coef x1x3 ]", {
  x: 0.6, y: y + 0.1, w: 12.0, h: 0.3,
  fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("             [ a21  a22  a23 ]               [ a12   a22   a23=a32 ]   [ 0.5 coef x1x2   coef x2^2   0.5 coef x2x3 ]", {
  x: 0.6, y: y + 0.35, w: 12.0, h: 0.3,
  fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("             [ a31  a32  a33 ]               [ a13   a23   a33 ]   [ 0.5 coef x1x3   0.5 coef x2x3   coef x3^2 ]", {
  x: 0.6, y: y + 0.6, w: 12.0, h: 0.3,
  fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("(Symmetric matrix - off-diagonal elements are half the corresponding cross-term coefficient)", {
  x: 0.6, y: y + 1.8, w: 12.0, h: 0.3,
  fontSize: 12, color: "666666", fontFace: FONT, margin: 0,
});

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_005_recreated.pptx" })
  .then(() => console.log("wrote slide_005_recreated.pptx"))
  .catch(e => console.error(e));