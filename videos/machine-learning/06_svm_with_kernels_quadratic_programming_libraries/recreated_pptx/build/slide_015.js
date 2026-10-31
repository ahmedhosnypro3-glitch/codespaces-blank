const pptxgen = require("pptxgenjs");
const path = require("path");
// Slide 015 rebuilt FRESH from qa/reanalysis2/slide_015_analysis.txt only.
// Spec coords are normalized [x0,y0,x1,y1]; X/Y map them to inches.
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const W = 13.33, H = 7.5, FONT = "Arial";
const X = v => v * W, Y = v => v * H;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (house rule overrides spec geometry)
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3, fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("15", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0 });

// Title: "Separable" blue + underlined per spec; house box geometry
s.addText([
  { text: "Non-Linearly ", options: { fontSize: 22, bold: true, color: "C00000", fontFace: FONT } },
  { text: "Separable", options: { fontSize: 22, bold: true, color: "0000FF", underline: true, fontFace: FONT } },
  { text: " Data", options: { fontSize: 22, bold: true, color: "C00000", fontFace: FONT } },
], { x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top", margin: 0 });

// Inner red content frame, white fill: spec [0.090,0.175,0.912,0.935]
s.addShape(pres.shapes.RECTANGLE, { x: X(0.090), y: Y(0.175), w: X(0.912 - 0.090), h: Y(0.935 - 0.175), fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 } });

// Italic red instruction line, verbatim with straight quotes around x
// (y placed at the original's measured 0.267-0.281, not the spec's 0.246)
s.addText('Each Sample is represented by one features "x"', { x: X(0.139), y: Y(0.260), w: X(0.547 - 0.139), h: Y(0.288 - 0.260), align: "left", valign: "top", fontSize: 14, italic: true, color: "CC0000", fontFace: FONT, margin: 0 });

// Plot region: matplotlib-generated PNG (parabola, blue line, x-axis, markers, "x")
s.addImage({ path: path.join(NS, "recreated_pptx/build/eq_015/plot_015.png"), x: X(0.111), y: Y(0.497), w: 1988 / 200, h: 627 / 200 });

// Annotation box 1 "Non-Linear Decision Boundary" (blue), spec [0.296,0.387,0.394,0.478]
s.addShape(pres.shapes.RECTANGLE, { x: X(0.296), y: Y(0.387), w: X(0.394 - 0.296), h: Y(0.478 - 0.387), fill: { color: "FFFFFF" }, line: { color: "9999CC", width: 1 } });
s.addText("Non-Linear\nDecision\nBoundary", { x: X(0.296), y: Y(0.387), w: X(0.394 - 0.296), h: Y(0.478 - 0.387), align: "center", valign: "middle", fontSize: 12, bold: true, italic: true, color: "3333CC", fontFace: "Times New Roman", lineSpacing: 14, margin: 0 });

// Annotation box 2 "Linear Decision Boundary" (purple), spec [0.438,0.417,0.534,0.513]
s.addShape(pres.shapes.RECTANGLE, { x: X(0.438), y: Y(0.417), w: X(0.534 - 0.438), h: Y(0.513 - 0.417), fill: { color: "FFFFFF" }, line: { color: "B07FD0", width: 1 } });
s.addText("Linear\nDecision\nBoundary", { x: X(0.438), y: Y(0.417), w: X(0.534 - 0.438), h: Y(0.513 - 0.417), align: "center", valign: "middle", fontSize: 12, bold: true, italic: true, color: "6633CC", fontFace: "Times New Roman", lineSpacing: 14, margin: 0 });

// Lavender leader lines (rotated thin rects)
function leader(x0, y0, x1, y1, color) {
  const x0i = X(x0), y0i = Y(y0), x1i = X(x1), y1i = Y(y1);
  const dx = x1i - x0i, dy = y1i - y0i, len = Math.hypot(dx, dy);
  const ang = Math.atan2(dy, dx) * 180 / Math.PI;
  s.addShape(pres.shapes.RECTANGLE, { x: (x0i + x1i) / 2 - len / 2, y: (y0i + y1i) / 2 - 0.01, w: len, h: 0.02, rotate: ang, fill: { color }, line: { type: "none" } });
}
leader(0.288, 0.404, 0.265, 0.528, "B19CD9");
leader(0.436, 0.428, 0.397, 0.520, "B19CD9");

// Small black NW cursor-like arrow, spec [0.405,0.659,0.423,0.696]
s.addShape(pres.shapes.RIGHT_ARROW, { x: X(0.405), y: Y(0.659), w: X(0.423 - 0.405), h: Y(0.696 - 0.659), rotate: 225, fill: { color: "000000" }, line: { color: "808080", width: 0.5 } });

// Bottom black overlay bar, spec [0.042,0.950,0.978,1.000]
s.addShape(pres.shapes.RECTANGLE, { x: X(0.042), y: Y(0.950), w: X(0.978 - 0.042), h: Y(1.000 - 0.950), fill: { color: "000000" }, line: { type: "none" } });

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_015_recreated.pptx") })
  .then(() => console.log("wrote slide_015_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
