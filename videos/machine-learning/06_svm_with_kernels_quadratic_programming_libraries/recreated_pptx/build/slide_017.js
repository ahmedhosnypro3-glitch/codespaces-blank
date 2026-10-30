const pptxgen = require("pptxgenjs");

const NUM = 17;
const TITLE = "Non-Linearly Separable Data";
const INSTRUCTION = 'Each Sample is represented by two features "x" and "y"';
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

// Dark gray header band with white title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 1.2,
  fill: { color: "2C3E50" }, line: { color: "2C3E50" },
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", fontSize: 26, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Instruction below header
s.addText(INSTRUCTION, {
  x: 0.6, y: 1.35, w: 12.13, h: 0.4,
  align: "center", fontSize: 14, italic: true, color: "C0392B", fontFace: FONT, margin: 0,
});

// Chart pane with dark-red border
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.0, y: 1.8, w: 11.3, h: 4.9,
  fill: { color: "FFFFFF" }, line: { color: "C0392B", width: 1.5 },
});

// Red x-axis (horizontal, with arrowhead + "x" label)
s.addShape(pres.shapes.LINE, { x: 1.0, y: 4.25, w: 11.3, h: 0, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("x", { x: 12.1, y: 4.05, w: 0.3, h: 0.4, fontSize: 16, italic: true, color: "E74C3C", fontFace: FONT, margin: 0 });

// Red y-axis (vertical, with arrowhead + "y" label)
s.addShape(pres.shapes.LINE, { x: 6.65, y: 1.8, w: 0, h: 4.9, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("y", { x: 6.35, y: 1.55, w: 0.4, h: 0.4, fontSize: 16, italic: true, color: "E74C3C", fontFace: FONT, margin: 0 });

// Orange decision circle centered at origin (axis intersection)
s.addShape(pres.shapes.OVAL, {
  x: 4.15, y: 2.4, w: 2.5, h: 1.8,
  fill: { type: "none" }, line: { color: "F39C12", width: 2 },
});

// Blue straight line with positive slope (~1) passing near origin
s.addShape(pres.shapes.LINE, { x: 3.5, y: 4.5, w: 5.0, h: -2.5, line: { color: "2E6DA4", width: 3 } });

// Ring of cyan dots surrounding the orange circle just outside it
[[4.0,2.5],[4.6,2.3],[5.4,2.25],[6.3,2.35],[7.0,2.6],[7.4,3.1],[7.5,3.7],[7.3,4.2],[6.7,4.6],[6.0,4.55],[5.2,4.5],[4.5,4.35],[3.9,4.0],[3.75,3.4],[3.8,2.95]].forEach(([x,y]) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.13, h: 0.13, fill: { color: "00CED1" }, line: { color: "00CED1" } });
});

// Red dots clustered inside the centered circle
[[5.3,3.3],[5.8,3.15],[6.2,3.3],[5.5,3.5],[6.0,3.55],[5.9,2.95]].forEach(([x,y]) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.13, h: 0.13, fill: { color: "E74C3C" }, line: { color: "E74C3C" } });
});

// Callout boxes: white fill, thin borders, leaders terminating on the right targets
// Linear Decision Boundary -> blue line (white box, blue text/border)
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.5, y: 2.0, w: 1.9, h: 0.7,
  fill: { color: "FFFFFF" }, line: { color: "3498DB", width: 1 },
});
s.addText("Linear\nDecision Boundary", { x: 10.55, y: 2.02, w: 1.8, h: 0.65, fontSize: 10, color: "3498DB", fontFace: FONT, margin: 0, lineSpacing: 12, align: "center", valign: "middle" });
s.addShape(pres.shapes.LINE, { x: 10.4, y: 2.6, w: -1.2, h: 1.3, line: { color: "3498DB", width: 1, endArrow: "triangle" } });

// Non-Linear Decision Boundary -> orange circle (white box, orange text/border)
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.5, y: 3.2, w: 1.9, h: 0.7,
  fill: { color: "FFFFFF" }, line: { color: "F39C12", width: 1 },
});
s.addText("Non-Linear\nDecision Boundary", { x: 10.55, y: 3.22, w: 1.8, h: 0.65, fontSize: 10, color: "F39C12", fontFace: FONT, margin: 0, lineSpacing: 12, align: "center", valign: "middle" });
s.addShape(pres.shapes.LINE, { x: 10.4, y: 3.8, w: -2.0, h: 0.8, line: { color: "F39C12", width: 1, endArrow: "triangle" } });

// Black footer
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 7.0, w: 13.03, h: 0.5, fill: { color: "000000" }, line: { color: "000000" } });

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_017_recreated.pptx" })
  .then(() => console.log("wrote slide_017_recreated.pptx"))
  .catch(e => console.error(e));