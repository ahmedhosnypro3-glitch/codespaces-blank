const pptxgen = require("pptxgenjs");
const { addEq } = require("./eqimg.js");

const NUM = 18;
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

// Title
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", fontSize: 26, bold: true, color: "C0392B", fontFace: FONT, margin: 0,
});

// Left mapping box: orange border, pale fill, tall 3-row column-vector delimiters
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 4.2, h: 3.0,
  fill: { color: "FFF8E1" }, line: { color: "F39C12", width: 1.5 },
});
s.addText("Mapping Z \u21d2 \u03c6(Z)", { x: 0.6, y: 1.1, w: 4.0, h: 0.4, fontSize: 16, bold: true, color: "2C3E50", fontFace: FONT, margin: 0 });
// Z = (x over y)  =>  (x^2 over y^2 over sqrt(2)xy), rendered as 2D math PNGs
addEq(s, "eq18_z", { x: 0.65, y: 1.55, w: 1.85, h: 1.35 });
// Double arrow
s.addText("\u21d2", { x: 2.45, y: 1.95, w: 0.9, h: 0.5, fontSize: 24, color: "2C3E50", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
// ( x² over y² over √2xy ) tall parens
addEq(s, "eq18_phi", { x: 3.15, y: 1.5, w: 1.45, h: 1.95 });

// Right 3D plot area
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.9, y: 1.0, w: 7.9, h: 5.9,
  fill: { color: "FFF8E1" }, line: { color: "F39C12", width: 1.5 },
});

// Tilted orange plane in perspective (parallelogram)
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.6, y: 3.3, w: 5.4, h: 2.6, rotate: -12,
  fill: { color: "F39C12", transparency: 25 }, line: { color: "F39C12", width: 1 },
});

// Red decision-boundary line drawn across the orange plane
s.addShape(pres.shapes.LINE, { x: 6.2, y: 4.3, w: 4.6, h: 0.5, rotate: -12, line: { color: "E74C3C", width: 3 } });

// Teal/cyan dots above the plane (upper cluster)
[[6.6,2.0],[7.4,2.2],[8.2,1.8],[7.0,1.6],[7.8,1.7],[8.6,1.5],[9.0,2.0],[6.4,1.8]].forEach(([x,y]) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.15, h: 0.15, fill: { color: "00CED1" }, line: { color: "00CED1" } });
});

// Darker/reddish dots near and below the plane
[[6.8,4.4],[7.6,4.6],[8.4,4.8],[7.2,5.2],[8.0,5.4],[8.8,5.5],[6.5,5.6],[9.4,4.9]].forEach(([x,y]) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.15, h: 0.15, fill: { color: "CD5C5C" }, line: { color: "CD5C5C" } });
});

// True 3D axes: z up, x right, y diagonally down-left
s.addShape(pres.shapes.LINE, { x: 5.6, y: 6.4, w: 3.0, h: 0, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("x", { x: 8.7, y: 6.2, w: 0.4, h: 0.4, fontSize: 14, color: "E74C3C", fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.LINE, { x: 5.6, y: 6.4, w: -1.4, h: 1.0, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("y", { x: 4.1, y: 7.0, w: 0.4, h: 0.4, fontSize: 14, color: "E74C3C", fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.LINE, { x: 5.6, y: 6.4, w: 0, h: -3.6, line: { color: "E74C3C", width: 2, endArrow: "triangle" } });
s.addText("z", { x: 5.2, y: 2.6, w: 0.4, h: 0.4, fontSize: 14, color: "E74C3C", fontFace: FONT, margin: 0 });

// Caption box (top-right, beige with blue/purple border)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 9.8, y: 1.2, w: 2.8, h: 0.8,
  fill: { color: "FADBD8" }, line: { color: "8E44AD", width: 1.5 },
});
s.addText("Data is linearly separable\nIn the new representation", { x: 9.85, y: 1.25, w: 2.7, h: 0.7, fontSize: 11, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 14, align: "center", valign: "middle" });

// Callout box: Linear Decision Boundary with blue/purple border, leader to the red line
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.8, y: 5.6, w: 2.8, h: 0.6,
  fill: { color: "FADBD8" }, line: { color: "8E44AD", width: 1.5 },
});
s.addText("Linear Decision Boundary", { x: 9.85, y: 5.62, w: 2.7, h: 0.55, fontSize: 11, color: "2C3E50", fontFace: FONT, margin: 0, align: "center", valign: "middle" });
s.addShape(pres.shapes.LINE, { x: 9.7, y: 5.9, w: -1.6, h: -1.2, line: { color: "E74C3C", width: 1, endArrow: "triangle" } });

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_018_recreated.pptx" })
  .then(() => console.log("wrote slide_018_recreated.pptx"))
  .catch(e => console.error(e));