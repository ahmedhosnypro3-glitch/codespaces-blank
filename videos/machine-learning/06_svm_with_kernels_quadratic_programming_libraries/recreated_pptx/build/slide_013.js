const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 13;
const TITLE = "SVM Constraint Transformation to Standard QP Form (Gx \u2264 h, Ax = b)";
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

// 3. Title
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Left column: Primal block (red-bordered peach)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.9, w: 5.8, h: 2.5,
  fill: { color: "FADBD8" }, line: { color: "E74C3C", width: 1.5 },
});
s.addText([
  { text: "Minimize: \u00bd \u03b1\u207fP\u03b1 + q\u207f\u03b1", options: { fontSize: 14, bold: true, color: "E74C3C", fontFace: FONT, margin: 0 } },
  { text: "Subject to: \u03b1\u2081 + \u03b1\u2082 - \u03b1\u2083 - \u03b1\u2084 = 0", options: { fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0 } },
  { text: "0 \u2264 \u03b1\u2081, \u03b1\u2082, \u03b1\u2083, \u03b1\u2084 \u2264 1", options: { fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0 } },
], {
  x: 0.6, y: 1.0, w: 5.6, h: 2.0, fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 18,
});

// 5. Constraint transformation box (peach)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.5, w: 5.8, h: 1.0,
  fill: { color: "FADBD8" }, line: { color: "E74C3C", width: 1 },
});
s.addText("\u03b1\u2081\u22650, \u03b1\u2081\u22641 \u21d2 -\u03b1\u2081\u22640, \u03b1\u2081\u22641", {
  x: 0.6, y: 3.55, w: 5.6, h: 0.4, fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0,
});
s.addText("(\u2200i = 1..4)", {
  x: 0.6, y: 3.95, w: 5.6, h: 0.3, fontSize: 13, color: "2C3E50", fontFace: FONT, margin: 0,
});

// 6. Center: G matrix (dark navy)
const gMatrix = [
  "G = [ -1  0  0  0 ]",
  "    [  0 -1  0  0 ]",
  "    [  0  0 -1  0 ]",
  "    [  0  0  0 -1 ]",
  "    [  1  0  0  0 ]",
  "    [  0  1  0  0 ]",
  "    [  0  0  1  0 ]",
  "    [  0  0  0  1 ]"
];
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.7, y: 0.9, w: 3.5, h: 2.2,
  fill: { color: "FFFFFF" }, line: { color: "1A1A2E", width: 1.5 },
});
s.addText(gMatrix.join("\n"), {
  x: 6.8, y: 1.0, w: 3.3, h: 2.0,
  fontSize: 12, color: "1A1A2E", fontFace: "Courier New", margin: 0, lineSpacing: 15,
});

// 7. h vector (dark navy)
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.7, y: 3.2, w: 3.5, h: 1.0,
  fill: { color: "FFFFFF" }, line: { color: "1A1A2E", width: 1.5 },
});
s.addText("h = [ 0 0 0 0 1 1 1 1 ]\u207f", {
  x: 6.8, y: 3.35, w: 3.3, h: 0.7,
  fontSize: 14, color: "1A1A2E", fontFace: FONT, margin: 0,
});

// 8. A vector (peach box)
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.5, y: 0.9, w: 2.3, h: 0.8,
  fill: { color: "FADBD8" }, line: { color: "E74C3C", width: 1 },
});
s.addText("A = [ 1  1 -1 -1 ]", {
  x: 10.6, y: 1.0, w: 2.1, h: 0.6,
  fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0,
});

// 9. b scalar (peach box)
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.5, y: 1.8, w: 2.3, h: 0.5,
  fill: { color: "FADBD8" }, line: { color: "E74C3C", width: 1 },
});
s.addText("b = [ 0 ]", {
  x: 10.6, y: 1.85, w: 2.1, h: 0.4,
  fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0,
});

// 10. Solution box (peach, right)
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.5, y: 2.5, w: 2.3, h: 2.5,
  fill: { color: "FADBD8" }, line: { color: "E74C3C", width: 1.5 },
});
s.addText("Solution", {
  x: 10.6, y: 2.6, w: 2.1, h: 0.35,
  align: "center", fontSize: 15, bold: true, color: "E74C3C", fontFace: FONT, margin: 0,
});
s.addText("\u03b1\u2081 = 0.0690\n\u03b1\u2082 = 0.0690\n\u03b1\u2083 = 0.0690\n\u03b1\u2084 = 0.000008", {
  x: 10.6, y: 3.0, w: 2.1, h: 1.8,
  fontSize: 13, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 16,
});

// 11. Green arrow (Solution label)
s.addText("Solution", {
  x: 8.5, y: 4.0, w: 2.0, h: 0.4,
  align: "center", fontSize: 16, bold: true, color: "27AE60", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_013_recreated.pptx" })
  .then(() => console.log("wrote slide_013.js"))
  .catch(e => console.error(e));