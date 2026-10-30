const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 6;
const TITLE = "Less Than Equal Constraints";
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

// Three boxes side by side
const boxW = 4.0, boxH = 5.5;
const boxX = [0.4, 4.7, 9.0];
const boxY = 1.0;

// Box 1: 3 constraints
let x = boxX[0], y = boxY;
s.addShape(pres.shapes.RECTANGLE, { x, y, w: boxW, h: boxH, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 } });
s.addText("3 constraints", { x: x+0.1, y: y+0.1, w: boxW-0.2, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("x1 \u2264 z1,  x2 \u2264 z2,  x3 \u2264 z3", { x: x+0.1, y: y+0.4, w: boxW-0.2, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("=>", { x: x+0.1, y: y+0.7, w: boxW-0.2, h: 0.3, fontSize: 16, bold: true, color: "008000", fontFace: FONT, margin: 0 });
s.addText("[1 0 0] [x1]   [z1]", { x: x+0.1, y: y+1.0, w: boxW-0.2, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[0 1 0] [x2] \u2264 [z2]", { x: x+0.1, y: y+1.3, w: boxW-0.2, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[0 0 1] [x3]   [z3]", { x: x+0.1, y: y+1.6, w: boxW-0.2, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: x+0.1, y: y+2.0, w: boxW-0.2, h: 0.5, fill: { color: "FFCCCC" }, line: { color: "C00000", width: 1 } });
s.addText("Gx \u2264 h", { x: x+0.1, y: y+2.1, w: boxW-0.2, h: 0.3, align: "center", fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Box 2: Greater-than converted
x = boxX[1];
s.addShape(pres.shapes.RECTANGLE, { x, y, w: boxW, h: boxH, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 } });
s.addText("Greater-than converted", { x: x+0.1, y: y+0.1, w: boxW-0.2, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("x1 \u2265 z1,  x2 \u2265 z2,  x3 \u2265 z3", { x: x+0.1, y: y+0.4, w: boxW-0.2, h: 0.3, fontSize: 14, color: "333333", fontFace: FONT, margin: 0 });
s.addText("=>", { x: x+0.1, y: y+0.7, w: boxW-0.2, h: 0.3, fontSize: 16, bold: true, color: "008000", fontFace: FONT, margin: 0 });
s.addText("[-1  0  0] [x1]   [-z1]", { x: x+0.1, y: y+1.0, w: boxW-0.2, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0 -1  0] [x2] \u2264 [-z2]", { x: x+0.1, y: y+1.3, w: boxW-0.2, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0  0 -1] [x3]   [-z3]", { x: x+0.1, y: y+1.6, w: boxW-0.2, h: 0.3, fontSize: 14, color: "000080", fontFace: "Courier New", margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: x+0.1, y: y+2.0, w: boxW-0.2, h: 1.2, fill: { color: "FFFFCC" }, line: { color: "C00000", width: 1 } });
s.addText("Convert", { x: x+0.1, y: y+2.1, w: boxW-0.2, h: 0.3, align: "center", fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("x1 \u2265 z1, x2 \u2265 z2, x3 \u2265 z3", { x: x+0.1, y: y+2.4, w: boxW-0.2, h: 0.3, fontSize: 12, color: "333333", fontFace: FONT, margin: 0 });
s.addText("TO", { x: x+0.1, y: y+2.7, w: boxW-0.2, h: 0.3, align: "center", fontSize: 12, bold: true, color: "333333", fontFace: FONT, margin: 0 });
s.addText("-x1 \u2264 -z1, -x2 \u2264 -z2, -x3 \u2264 -z3", { x: x+0.1, y: y+3.0, w: boxW-0.2, h: 0.3, fontSize: 12, color: "333333", fontFace: FONT, margin: 0 });

// Box 3: 6 constraints, 3 variables
x = boxX[2];
s.addShape(pres.shapes.RECTANGLE, { x, y, w: boxW, h: boxH, fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 } });
s.addText("6 constraints, 3 variables", { x: x+0.1, y: y+0.1, w: boxW-0.2, h: 0.3, fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("y1 \u2264 x1 \u2264 z1,  y2 \u2264 x2 \u2264 z2,  y3 \u2264 x3 \u2264 z3", { x: x+0.1, y: y+0.4, w: boxW-0.2, h: 0.3, fontSize: 13, color: "333333", fontFace: FONT, margin: 0 });
s.addText("=>", { x: x+0.1, y: y+0.7, w: boxW-0.2, h: 0.3, fontSize: 16, bold: true, color: "008000", fontFace: FONT, margin: 0 });
s.addText("[-1 0 0]  [-y1]", { x: x+0.1, y: y+1.0, w: boxW-0.2, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0 -1 0]  [-y2]", { x: x+0.1, y: y+1.25, w: boxW-0.2, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0 0 -1]  [-y3]", { x: x+0.1, y: y+1.5, w: boxW-0.2, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 1 0 0]   [ z1]", { x: x+0.1, y: y+1.75, w: boxW-0.2, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0 1 0] \u2264 [ z2]  (6x3)", { x: x+0.1, y: y+2.0, w: boxW-0.2, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addText("[ 0 0 1]   [ z3]", { x: x+0.1, y: y+2.25, w: boxW-0.2, h: 0.25, fontSize: 13, color: "000080", fontFace: "Courier New", margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: x+0.1, y: y+2.6, w: boxW-0.2, h: 0.5, fill: { color: "FFCCCC" }, line: { color: "C00000", width: 1 } });
s.addText("Gx \u2264 h", { x: x+0.1, y: y+2.7, w: boxW-0.2, h: 0.3, align: "center", fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// Write
pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_006_recreated.pptx" })
  .then(() => console.log("wrote slide_006_recreated.pptx"))
  .catch(e => console.error(e));