const pptxgen = require("pptxgenjs");

const NUM = 16;
const TITLE = "Non-Linearly Separable Data";
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

// Title: single centered line, "Separable" blue underlined, rest dark red
s.addText([
  { text: "Non-Linearly ", options: { fontSize: 26, bold: true, color: "C0392B", fontFace: FONT } },
  { text: "Separable", options: { fontSize: 26, bold: true, color: "2E6DA4", fontFace: FONT, underline: true } },
  { text: " Data", options: { fontSize: 26, bold: true, color: "C0392B", fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

// Plot card with red border
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1.0, y: 1.1, w: 11.3, h: 5.6,
  fill: { color: "FFFFFF" }, line: { color: "E74C3C", width: 1.5 },
});

// Horizontal red x-axis with arrowhead + "x" label
s.addShape(pres.shapes.LINE, { x: 1.5, y: 5.5, w: 9.0, h: 0, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("x", { x: 10.6, y: 5.3, w: 0.4, h: 0.4, fontSize: 16, italic: true, color: "E74C3C", fontFace: FONT, margin: 0 });

// Full vertical red axis with arrowhead at top labeled "x²"
s.addShape(pres.shapes.LINE, { x: 2.0, y: 1.5, w: 0, h: 4.0, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("x\u00b2", { x: 2.1, y: 1.3, w: 0.6, h: 0.4, fontSize: 16, color: "E74C3C", fontFace: FONT, margin: 0 });

// Row of open blue circles at y = 0 (on the x-axis)
[2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5].forEach(x => {
  s.addShape(pres.shapes.OVAL, { x: x-0.1, y: 5.4, w: 0.2, h: 0.2, fill: { color: "FFFFFF" }, line: { color: "2E6DA4", width: 1.5 } });
});

// Blue horizontal decision boundary line (above axis)
s.addShape(pres.shapes.LINE, { x: 1.5, y: 3.8, w: 9.0, h: 0, line: { color: "3498DB", width: 3 } });

// Cyan dots (upper region)
[[3.0,2.6],[4.0,2.4],[5.0,2.7],[4.5,2.9],[3.5,2.8],[6.0,2.5],[7.0,2.8],[8.0,2.6],[9.0,2.7],[10.0,2.9]].forEach(([x,y]) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.14, h: 0.14, fill: { color: "00CED1" }, line: { color: "00CED1" } });
});

// Red dots (lower region)
[[3.0,4.6],[4.5,4.3],[5.5,4.7],[7.0,4.4],[8.5,4.6],[9.5,4.3],[10.0,4.8],[3.5,5.0],[5.0,5.2]].forEach(([x,y]) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.14, h: 0.14, fill: { color: "E74C3C" }, line: { color: "E74C3C" } });
});

// Legend box (blue border, compact)
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.2, y: 2.0, w: 2.8, h: 0.45,
  fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1.5 },
});
s.addText("Linear Decision Boundary", { x: 9.25, y: 2.02, w: 2.7, h: 0.4, fontSize: 10, color: "3498DB", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
// Leader line to blue boundary
s.addShape(pres.shapes.LINE, { x: 10.6, y: 2.45, w: 0, h: 1.35, line: { color: "3498DB", width: 1, endArrow: "triangle" } });

// Callout box (beige, right)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 9.2, y: 4.2, w: 2.8, h: 1.0,
  fill: { color: "FADBD8" }, line: { color: "E74C3C", width: 1 },
});
s.addText("Data is linearly separable\nIn the new representation", { x: 9.25, y: 4.25, w: 2.7, h: 0.9, fontSize: 11, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 14, align: "center", valign: "middle" });

// Mapping box (beige/orange border, pale fill) with TALL delimiters spanning 2 lines
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.2, y: 2.0, w: 3.6, h: 1.3,
  fill: { color: "FFF8E1" }, line: { color: "F39C12", width: 1.5 },
});
s.addText("Mapping x \u2192 \u03c6(x)", { x: 1.3, y: 2.05, w: 3.4, h: 0.3, fontSize: 13, bold: true, color: "2C3E50", fontFace: FONT, margin: 0 });
// Stacked column with tall parens: x => ( x ) over ( x² )
s.addText("(", { x: 2.6, y: 2.4, w: 0.25, h: 0.85, fontSize: 28, color: "2C3E50", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
s.addText("x\nx\u00b2", { x: 2.85, y: 2.4, w: 0.6, h: 0.85, fontSize: 14, color: "1A1A2E", fontFace: FONT, margin: 0, lineSpacing: 16, align: "center", valign: "middle" });
s.addText(")", { x: 3.45, y: 2.4, w: 0.25, h: 0.85, fontSize: 28, color: "2C3E50", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
// Double arrow
s.addText("\u21d2", { x: 1.9, y: 2.6, w: 0.7, h: 0.5, fontSize: 20, color: "2C3E50", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
s.addText("x", { x: 1.35, y: 2.6, w: 0.5, h: 0.5, fontSize: 16, italic: true, color: "1A1A2E", fontFace: FONT, margin: 0, align: "center", valign: "middle" });

// Black footer
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 7.0, w: 13.03, h: 0.5, fill: { color: "000000" }, line: { color: "000000" } });

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_016_recreated.pptx" })
  .then(() => console.log("wrote slide_016_recreated.pptx"))
  .catch(e => console.error(e));