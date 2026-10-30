const pptxgen = require("pptxgenjs");
const { addEq } = require("./eqimg.js");

const NUM = 22;
const TITLE = "Polynomial Kernel (of order 2)";
const FORMULA = "[a\u1d40b + 1]\u00b2";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "000000" }; // Black canvas

// White page on black
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});

// Badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Example-2 label (red)
s.addText("Example-2", { x: 0.5, y: 0.3, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: "E74C3C", fontFace: FONT, margin: 0 });

// Title + formula (red)
s.addText(TITLE, { x: 3.0, y: 0.28, w: 7.0, h: 0.55, align: "center", fontSize: 24, bold: true, color: "E74C3C", fontFace: FONT, margin: 0 });
addEq(s, "eq22_title", { x: 3.0, y: 0.8, w: 7.0, h: 0.5 });

// LEFT COLUMN: two stacked rows of vectors with red double-arrows
// Top row
addEq(s, "eq22_lab1", { x: 0.5, y: 1.45, w: 1.5, h: 0.45 });
addEq(s, "eq22_lab2", { x: 0.5, y: 1.95, w: 1.5, h: 0.45 });
// Red double-arrows top
s.addShape(pres.shapes.LINE, { x: 2.2, y: 1.6, w: 1.5, h: 0, line: { color: "E74C3C", width: 3 } });
s.addShape(pres.shapes.LINE, { x: 2.2, y: 2.1, w: 1.5, h: 0, line: { color: "E74C3C", width: 3 } });

// Bottom row (same vectors)
addEq(s, "eq22_lab1", { x: 0.5, y: 3.45, w: 1.5, h: 0.45 });
addEq(s, "eq22_lab2", { x: 0.5, y: 3.95, w: 1.5, h: 0.45 });
// Red double-arrows around Vectors Mapping box
s.addShape(pres.shapes.LINE, { x: 2.2, y: 3.6, w: 1.0, h: 0, line: { color: "E74C3C", width: 3 } });
s.addShape(pres.shapes.LINE, { x: 2.2, y: 4.1, w: 1.0, h: 0, line: { color: "E74C3C", width: 3 } });

// CENTER BAND: Map Input data from 2-D to 6-D (gray band)
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 1.2, w: 5.5, h: 0.6,
  fill: { color: "95A5A6" }, line: { color: "95A5A6" },
});
s.addText("Map Input data from 2-D to 6-D", { x: 3.6, y: 1.22, w: 5.3, h: 0.55, align: "center", fontSize: 13, color: "FFFFFF", fontFace: FONT, margin: 0 });

// MIDDLE-LEFT: Normal Model (red border)
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 2.0, w: 2.8, h: 2.5,
  fill: { color: "FADBD8" }, line: { color: "E74C3C", width: 2 },
});
addEq(s, "eq22_norm_a", { x: 3.6, y: 2.05, w: 2.6, h: 0.45 });
// 2x2 matrix
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.0, y: 2.7, w: 1.8, h: 1.5,
  fill: { color: "FFFFFF" }, line: { color: "E74C3C", width: 1 },
});
addEq(s, "eq22_mtx", { x: 4.05, y: 2.75, w: 1.7, h: 1.4 });

// LOWER-MIDDLE: Vectors Mapping (purple border)
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 4.8, w: 2.8, h: 2.0,
  fill: { color: "F5EEF8" }, line: { color: "8E44AD", width: 2 },
});
s.addText("Vectors Mapping", { x: 3.6, y: 4.9, w: 2.6, h: 0.4, fontSize: 12, bold: true, color: "8E44AD", fontFace: FONT, margin: 0, align: "center" });
// Column vectors
addEq(s, "eq22_col_a", { x: 3.65, y: 5.35, w: 1.3, h: 1.3 });
addEq(s, "eq22_col_b", { x: 4.95, y: 5.35, w: 1.3, h: 1.3 });
// Purple complexity pill (with warning emojis)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.5, y: 6.9, w: 2.8, h: 0.4,
  fill: { color: "8E44AD" }, line: { color: "8E44AD" },
});
s.addText("Higher Computational Complexity \u26A0\u26A0", { x: 3.6, y: 6.9, w: 2.6, h: 0.35, align: "center", fontSize: 9, color: "FFFFFF", fontFace: FONT, margin: 0 });

// RIGHT: Kernelized Model (green border)
s.addShape(pres.shapes.RECTANGLE, {
  x: 6.8, y: 2.0, w: 6.0, h: 4.8,
  fill: { color: "D5F5E3" }, line: { color: "E74C3C", width: 2 },
});
addEq(s, "eq22_kern_u", { x: 6.9, y: 2.05, w: 5.8, h: 0.45 });
// 6-D vector
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.2, y: 2.7, w: 5.2, h: 1.5,
  fill: { color: "FFFFFF" }, line: { color: "27AE60", width: 1 },
});
addEq(s, "eq22_6d", { x: 7.3, y: 2.85, w: 5.0, h: 1.2 });
// Green complexity pill
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 6.8, y: 4.4, w: 2.5, h: 0.4,
  fill: { color: "27AE60" }, line: { color: "27AE60" },
});
s.addText("Higher Computational Complexity!!!", { x: 6.9, y: 4.4, w: 2.3, h: 0.35, align: "center", fontSize: 9, color: "FFFFFF", fontFace: FONT, margin: 0 });
// Expanded b-vector column (right of kernelized)
s.addShape(pres.shapes.RECTANGLE, {
  x: 12.0, y: 2.7, w: 1.2, h: 3.5,
  fill: { color: "FFFFFF" }, line: { color: "27AE60", width: 1 },
});
addEq(s, "eq22_b6", { x: 12.05, y: 2.85, w: 1.1, h: 3.2 });

// Red double-arrows connecting left to center to right
// Top flow
s.addShape(pres.shapes.LINE, { x: 3.7, y: 1.9, w: 3.0, h: 0, line: { color: "E74C3C", width: 3 } });
s.addShape(pres.shapes.LINE, { x: 6.5, y: 1.9, w: 0.5, h: 0, line: { color: "E74C3C", width: 3 } });

// Bottom flow
s.addShape(pres.shapes.LINE, { x: 3.7, y: 5.2, w: 3.0, h: 0, line: { color: "E74C3C", width: 3 } });
s.addShape(pres.shapes.LINE, { x: 6.5, y: 5.2, w: 0.5, h: 0, line: { color: "E74C3C", width: 3 } });

// Black band bottom
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 7.0, w: 13.03, h: 0.5, fill: { color: "000000" }, line: { color: "000000" } });

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_022_recreated.pptx" })
  .then(() => console.log("wrote slide_022_recreated.pptx"))
  .catch(e => console.error(e));