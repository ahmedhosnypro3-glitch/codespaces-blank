// slide_016.js — REBUILD WAVE 3. MAJOR fixes per qa/rejudge2/slide_016_judge.txt;
// geometry measured from qa/rejudge2/orig_png/slide_016.png (norm -> in: x*13.33, y*7.5).
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_016");
const man = JSON.parse(fs.readFileSync(path.join(EQ, "manifest.json"), "utf8"));
const W = 13.33, H = 7.5, FONT = "Arial";
const X = n => n * W, Y = n => n * H;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
// House chrome (mandatory, overrides spec)
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3, fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("16", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0 });
s.addText([
  { text: "Non-Linearly ", options: { fontSize: 26, bold: true, color: "C00000", fontFace: FONT } },
  { text: "Separable", options: { fontSize: 26, bold: true, color: "1F49C7", fontFace: FONT, underline: { style: "sng" } } },
  { text: " Data", options: { fontSize: 26, bold: true, color: "C00000", fontFace: FONT } },
], { x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top", margin: 0 });
// Mapping box [0.060,0.205,0.275,0.315]: pale cream fill, tan border, blue italic serif header
const mb = { x: X(0.060), y: Y(0.205), w: X(0.275) - X(0.060), h: Y(0.315) - Y(0.205) };
s.addShape(pres.shapes.RECTANGLE, { x: mb.x, y: mb.y, w: mb.w, h: mb.h, fill: { color: "F9EFE6" }, line: { color: "A88663", width: 1.25 } });
s.addText("Mapping  x ⇒ φ(x)", { x: mb.x, y: mb.y + 0.02, w: mb.w, h: 0.22, align: "center", valign: "middle", fontSize: 12, italic: true, color: "1F49C7", fontFace: "Georgia", margin: 0 });
const em = man.eq_map;
s.addImage({ path: path.join(EQ, em.file), w: em.w_in, x: mb.x + (mb.w - em.w_in) / 2, y: mb.y + mb.h - em.h_in - 0.05 });
// Right note: red italic with bold emphasis, then black line
s.addText([
  { text: "Data is ", options: { fontSize: 14, italic: true, color: "C00000", fontFace: FONT } },
  { text: "linearly separable", options: { fontSize: 14, bold: true, italic: true, color: "C00000", fontFace: FONT } },
], { x: X(0.69), y: Y(0.295), w: X(0.90) - X(0.69), h: Y(0.335) - Y(0.295), align: "left", valign: "middle", margin: 0 });
s.addText("In the new representation", { x: X(0.69), y: Y(0.345), w: X(0.90) - X(0.69), h: 0.4, align: "left", valign: "middle", fontSize: 14, italic: true, color: "000000", fontFace: FONT, margin: 0 });
// "Linear Decision Boundary" callout: 3-line bold-italic blue, centre-right above boundary end
s.addText("Linear\nDecision\nBoundary", { x: X(0.70), y: Y(0.45), w: X(0.90) - X(0.70), h: Y(0.58) - Y(0.45), align: "center", valign: "middle", fontSize: 12, bold: true, italic: true, color: "1F49C7", fontFace: FONT, margin: 0, lineSpacing: 14 });
const ax = X(0.79), ay = Y(0.575), bx = X(0.752), by = Y(0.602);
s.addShape(pres.shapes.LINE, { x: ax, y: ay, w: Math.hypot(bx - ax, by - ay), h: 0.01, rotate: Math.atan2(by - ay, bx - ax) * 180 / Math.PI, line: { color: "1F49C7", width: 1.5 } });
// Axes: vertical x^2 at panel centre x=0.471 (arrowhead top), horizontal x at y=0.827 (arrowhead right)
s.addShape(pres.shapes.LINE, { x: X(0.471), y: Y(0.174), w: 0.01, h: Y(0.827) - Y(0.174), line: { color: "C00000", width: 2 } });
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: X(0.471) - 0.08, y: Y(0.152), w: 0.16, h: 0.16, fill: { color: "C00000" }, line: { type: "none" } });
s.addShape(pres.shapes.LINE, { x: X(0.091), y: Y(0.827), w: X(0.898) - X(0.091), h: 0.01, line: { color: "C00000", width: 2, endArrowType: "triangle" } });
const e2 = man.eq_x2, e1 = man.eq_x;
s.addImage({ path: path.join(EQ, e2.file), x: X(0.422), y: Y(0.119), w: e2.w_in });
s.addImage({ path: path.join(EQ, e1.file), x: X(0.855), y: Y(0.815), w: e1.w_in });
// Blue linear decision boundary: y=0.603, x 0.217 -> 0.756 (stops short of the callout)
s.addShape(pres.shapes.LINE, { x: X(0.217), y: Y(0.603), w: X(0.756) - X(0.217), h: 0.01, line: { color: "1F49C7", width: 2.25 } });
// Cyan parabola: 3 left / 3 right of the axis, height increasing outward
const cyan = [[0.296, 0.239], [0.658, 0.239], [0.328, 0.418], [0.623, 0.418], [0.363, 0.558], [0.586, 0.558]];
// Red tight symmetric cluster just above the x-axis
const red = [[0.386, 0.647], [0.554, 0.647], [0.416, 0.736], [0.523, 0.736], [0.452, 0.733], [0.490, 0.733]];
function dots(list, color, r) {
  list.forEach(p => s.addShape(pres.shapes.OVAL, { x: X(p[0]) - r, y: Y(p[1]) - r, w: 2 * r, h: 2 * r, fill: { color }, line: { color, width: 0 } }));
}
dots(cyan, "00B0F0", 0.083);
dots(red, "DD2C2C", 0.083);
// 12 open circles on the x-axis, 6 left / 6 right of the axis, alternating blue/red
const circ = [0.300, 0.330, 0.360, 0.390, 0.420, 0.450, 0.492, 0.522, 0.552, 0.585, 0.620, 0.655];
circ.forEach((cx, i) => s.addShape(pres.shapes.OVAL, {
  x: X(cx) - 0.075, y: Y(0.827) - 0.075, w: 0.15, h: 0.15,
  fill: { type: "none" }, line: { color: i % 2 ? "C00000" : "1F49C7", width: 1.5 },
}));
pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_016_recreated.pptx") })
  .then(() => console.log("wrote slide_016_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
