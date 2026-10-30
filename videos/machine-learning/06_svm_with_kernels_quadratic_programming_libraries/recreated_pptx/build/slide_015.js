const pptxgen = require("pptxgenjs");

const NUM = 15;
const TITLE = "Non-Linearly Separable Data";
const INSTRUCTION = 'Each Sample is represented by one features "x"';
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
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

// Title: single centered line, "Separable" in blue + underlined
s.addText("Non-Linearly ", { x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", fontSize: 26, bold: true, color: "C0392B", fontFace: FONT, margin: 0 });
s.addText("Separable", { x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", fontSize: 26, bold: true, color: "2E6DA4", fontFace: FONT, margin: 0, underline: true, charSpacing: 0 });
s.addText("Data", { x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", fontSize: 26, bold: true, color: "C0392B", fontFace: FONT, margin: 0 });

// Chart pane with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.0, y: 1.3, w: 11.3, h: 5.4,
  fill: { color: "FFFFFF" }, line: { color: "C0392B", width: 2 },
});

// Instruction INSIDE white panel near top
s.addText(INSTRUCTION, {
  x: 1.3, y: 1.4, w: 10.7, h: 0.4,
  align: "left", fontSize: 15, italic: true, color: "C0392B", fontFace: FONT, margin: 0,
});

// X-axis (red horizontal line with arrowhead and "x" label)
s.addShape(pres.shapes.LINE, { x: 1.5, y: 4.8, w: 10.0, h: 0, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("x", { x: 11.4, y: 4.6, w: 0.4, h: 0.4, fontSize: 18, italic: true, color: "E74C3C", fontFace: FONT, margin: 0 });

// Cyan dots at both ends of x-axis
[1.8, 10.8].forEach(x => {
  s.addShape(pres.shapes.OVAL, { x: x-0.1, y: 4.7, w: 0.16, h: 0.16, fill: { color: "00CED1" }, line: { color: "00CED1" } });
});

// Orange upward-opening parabola (y = (x-6)^2 style) via polylines
// Left arm going up
s.addShape(pres.shapes.LINE, { x: 3.5, y: 4.6, w: 1.5, h: 0, line: { color: "F39C12", width: 3 } });
s.addShape(pres.shapes.LINE, { x: 5.0, y: 4.6, w: 1.0, h: 1.5, line: { color: "F39C12", width: 3, flipV: true } });
// Right arm going up
s.addShape(pres.shapes.LINE, { x: 6.0, y: 4.6, w: 1.0, h: 1.5, line: { color: "F39C12", width: 3, flipV: true } });
s.addShape(pres.shapes.LINE, { x: 6.0, y: 3.1, w: 1.5, h: 0, line: { color: "F39C12", width: 3 } });
s.addShape(pres.shapes.LINE, { x: 7.5, y: 3.1, w: 1.0, h: 1.5, line: { color: "F39C12", width: 3, flipV: true } });
s.addShape(pres.shapes.LINE, { x: 7.5, y: 1.6, w: 2.0, h: 0, line: { color: "F39C12", width: 3 } });

// Five red dots clustered in center on the axis
[5.5, 5.8, 6.0, 6.2, 6.5].forEach(x => {
  s.addShape(pres.shapes.OVAL, { x, y: 4.65, w: 0.14, h: 0.14, fill: { color: "E74C3C" }, line: { color: "E74C3C" } });
});

// Steep blue linear line crossing the axis
s.addShape(pres.shapes.LINE, { x: 5.7, y: 5.5, w: 0, h: -2.5, line: { color: "2E6DA4", width: 3, endArrow: "triangle" } });

// Callout boxes: BLUE border/text, diagonal leader lines to curves
// Non-Linear Decision Boundary (points to orange parabola)
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.5, y: 1.8, w: 2.6, h: 0.7,
  fill: { color: "FFFFFF" }, line: { color: "2E6DA4", width: 1.5 },
});
s.addText("Non-Linear Decision Boundary", { x: 1.55, y: 1.82, w: 2.5, h: 0.65, fontSize: 9, color: "2E6DA4", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
s.addShape(pres.shapes.LINE, { x: 3.8, y: 2.3, w: 2.4, h: 1.6, line: { color: "2E6DA4", width: 1, endArrow: "triangle" } });

// Linear Decision Boundary (points to blue line)
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.5, y: 1.8, w: 2.4, h: 0.7,
  fill: { color: "FFFFFF" }, line: { color: "2E6DA4", width: 1.5 },
});
s.addText("Linear Decision Boundary", { x: 9.55, y: 1.82, w: 2.3, h: 0.65, fontSize: 9, color: "2E6DA4", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
s.addShape(pres.shapes.LINE, { x: 9.4, y: 2.3, w: -1.5, h: 2.2, line: { color: "2E6DA4", width: 1, endArrow: "triangle" } });

// Black footer
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 7.0, w: 13.03, h: 0.5, fill: { color: "000000" }, line: { color: "000000" } });

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_015_recreated.pptx" })
  .then(() => console.log("wrote slide_015_recreated.pptx"))
  .catch(e => console.error(e));