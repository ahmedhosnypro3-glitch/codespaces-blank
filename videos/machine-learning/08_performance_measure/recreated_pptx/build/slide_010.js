const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", RED2 = "D32F2F", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const GREEN = "4CAF50", BLUE = "2196F3", PURPLE = "9C27B0", ORANGE = "FF9800";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { color: BG }, line: { color: RED, width: 1.5 } });
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 } });
s.addText("10", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0 });
s.addText("Recall", { x: 0.6, y: 0.28, w: 12.13, h: 0.8, align: "center", valign: "middle", fontSize: 40, bold: true, color: RED2, fontFace: FONT, margin: 0 });

// ============================================================
// LEFT COLUMN
// ============================================================
const leftX = 0.6, leftW = 5.5;

// 1. DEFINITION BAND: gray, bold centered, red rule INSIDE
s.addShape(pptx.shapes.RECTANGLE, { x: leftX, y: 1.2, w: leftW, h: 0.85, fill: { color: "E0E0E0" }, line: { type: "none" } });
s.addText("Correctly Classified (as Positive)", { x: leftX + 0.1, y: 1.22, w: leftW - 0.2, h: 0.35, fontSize: 14, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center" });
s.addShape(pptx.shapes.RECTANGLE, { x: leftX + 1.0, y: 1.57, w: 3.5, h: 0.02, fill: { color: RED2 }, line: { type: "none" } });
s.addText("Total objects that should be retrieved (Actually Positive)", { x: leftX + 0.1, y: 1.6, w: leftW - 0.2, h: 0.4, fontSize: 14, bold: true, color: TEXT, fontFace: FONT, margin: 0, align: "center" });

// 2. MEANING PANEL: pale yellow, thin border, narrow enough to avoid matrix area
s.addShape(pptx.shapes.RECTANGLE, { x: leftX, y: 2.15, w: leftW, h: 0.75, fill: { color: "FFF9C4" }, line: { color: "CCCC00", width: 0.75 } });
s.addText("Meaning", { x: leftX + 0.15, y: 2.2, w: 1.6, h: 0.35, fontSize: 18, bold: true, color: RED2, fontFace: FONT, margin: 0 });
s.addText([{ text: "Does the classifier " }, { text: "miss", options: { color: RED2 } }, { text: " any of " }, { text: "Positive", options: { color: BLUE, underline: true } }, { text: " Objects ?" }], { x: leftX + 0.15, y: 2.52, w: leftW - 0.3, h: 0.35, fontSize: 13, color: TEXT, fontFace: FONT, margin: 0 });

// 3. RECALL FORMULA BOX: compact white, red outline, "Recall =" in BLACK
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: leftX, y: 3.05, w: 3.4, h: 1.1, fill: { color: "FFFFFF" }, line: { color: RED2, width: 2 } });
s.addText("Recall =", { x: leftX + 0.1, y: 3.45, w: 1.1, h: 0.4, fontSize: 16, bold: true, color: TEXT, fontFace: FONT, margin: 0, valign: "middle" });
const eqW = 1.07, eqH = 0.64667;
s.addImage({ path: "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/eq_010_recall.png", x: 1.9, y: 3.25, w: eqW, h: eqH });

// Speech bubbles with connectors UP
s.addShape(pptx.shapes.LINE, { x: 1.1, y: 4.15, w: 0, h: -0.35, line: { color: TEXT, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: 3.3, y: 4.15, w: 0, h: -0.35, line: { color: TEXT, width: 1 } });

function drawStickyNote(x, y, text, tailX) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: x, y: y, w: 1.6, h: 0.5, fill: { color: "FFFDE7" }, line: { color: "E0C000", width: 0.75 } });
  s.addText(text, { x: x + 0.05, y: y + 0.02, w: 1.5, h: 0.45, fontSize: 10, color: TEXT, fontFace: FONT, margin: 0, align: "center", valign: "middle" });
  // Triangle tail pointing UP toward formula
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: tailX, y: y - 0.12, w: 0.15, h: 0.12, fill: { color: "FFFDE7" }, line: { color: "E0C000", width: 0.75 }, rotate: 180 });
}
drawStickyNote(0.65, 4.5, "Positive Classified as +ive", 1.1);
drawStickyNote(3.15, 4.5, "Positive Classified as -ive", 3.6);

// Green curly brace spanning under bubbles + caption
s.addShape(pptx.shapes.LINE, { x: 0.65, y: 5.1, w: 4.1, h: 0, line: { color: GREEN, width: 2 } });
s.addShape(pptx.shapes.LINE, { x: 0.65, y: 5.05, w: 0, h: 0.1, line: { color: GREEN, width: 2 } });
s.addShape(pptx.shapes.LINE, { x: 4.75, y: 5.05, w: 0, h: 0.1, line: { color: GREEN, width: 2 } });
s.addText("All Positive Samples in the Dataset", { x: leftX, y: 5.15, w: leftW, h: 0.3, fontSize: 12, italic: true, color: RED2, fontFace: FONT, margin: 0, align: "center" });

// 6. BOTTOM QUESTION BOX: pale blue, blue border, italic
s.addShape(pptx.shapes.RECTANGLE, { x: leftX, y: 5.85, w: leftW, h: 0.9, fill: { color: "E3F2FD" }, line: { color: BLUE, width: 2 } });
s.addText([{ text: "If you said: I picked " }, { text: "ALL", options: { bold: true, color: RED2 } }, { text: " Positive objects,", options: { breakLine: true } }, { text: "can I trust you ? At what %?" }], { x: leftX + 0.15, y: 5.9, w: leftW - 0.3, h: 0.8, fontSize: 13, color: TEXT, fontFace: FONT, margin: 0, lineSpacing: 18, italic: true });

// ============================================================
// RIGHT SIDE
// ============================================================
const rightX = 5.8;
const rightW = 6.6;
const cw = 1.0, ch = 0.5;

// ---- BLUE CONTAINER for BOTH matrices ----
const contX = rightX, contY = 1.4, contW = rightW - 0.5, contH = 3.4;
s.addShape(pptx.shapes.RECTANGLE, { x: contX, y: contY, w: contW, h: contH, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 } });

// TOP MATRIX inside container
const cmX = contX + 0.3, cmY = contY + 0.15;
s.addText("Predicted as", { x: cmX, y: cmY - 0.3, w: cw * 2 + 0.6, h: 0.25, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0 });
s.addText("P", { x: cmX + 0.6, y: cmY, w: cw, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: cmX + 0.6 + cw, y: cmY, w: cw, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: cmX + 0.63, y: cmY + ch + 0.1, w: 0.3, h: ch * 1.8, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: cmX, y: cmY + ch, w: 0.6, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: cmX, y: cmY + ch * 2, w: 0.6, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: cmX + 0.6, y: cmY + ch, w: cw * 2, h: ch * 2, fill: { color: "FFFFFF" }, line: { color: TEXT, width: 0.5 } });
s.addShape(pptx.shapes.RECTANGLE, { x: cmX + 0.6, y: cmY + ch, w: cw, h: ch, fill: { color: GREEN }, line: { color: TEXT, width: 0.5 } });
s.addText("TP", { x: cmX + 0.6, y: cmY + ch, w: cw, h: ch, fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: cmX + 0.6 + cw, y: cmY + ch, w: cw, h: ch, fill: { color: "FFFFFF" }, line: { color: TEXT, width: 0.5 } });
s.addText("FN", { x: cmX + 0.6 + cw, y: cmY + ch, w: cw, h: ch, fontSize: 11, color: TEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: cmX + 0.6, y: cmY + ch * 2, w: cw, h: ch, fill: { color: "FFFFFF" }, line: { color: TEXT, width: 0.5 } });
s.addText("FP", { x: cmX + 0.6, y: cmY + ch * 2, w: cw, h: ch, fontSize: 11, color: TEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: cmX + 0.6 + cw, y: cmY + ch * 2, w: cw, h: ch, fill: { color: GREEN }, line: { color: TEXT, width: 0.5 } });
s.addText("TN", { x: cmX + 0.6 + cw, y: cmY + ch * 2, w: cw, h: ch, fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// NUMERIC MATRIX inside same container, BELOW
const nmX = contX + 0.3, nmY = cmY + ch * 2 + 0.7;
s.addText("Predicted as", { x: nmX, y: nmY - 0.3, w: cw * 2 + 0.6, h: 0.25, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0 });
s.addText("P", { x: nmX + 0.6, y: nmY, w: cw, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nmX + 0.6 + cw, y: nmY, w: cw, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("Actual", { x: nmX + 0.63, y: nmY + ch + 0.1, w: 0.3, h: ch * 1.8, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
s.addText("P", { x: nmX, y: nmY + ch, w: 0.6, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nmX, y: nmY + ch * 2, w: 0.6, h: ch, fontSize: 11, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: nmX + 0.6, y: nmY + ch, w: cw * 2, h: ch * 2, fill: { color: "FFFFFF" }, line: { color: TEXT, width: 0.5 } });
s.addShape(pptx.shapes.OVAL, { x: nmX + 0.75, y: nmY + ch + 0.08, w: 0.7, h: 0.35, fill: { color: PURPLE }, line: { color: PURPLE, width: 1 } });
s.addText("18", { x: nmX + 0.75, y: nmY + ch + 0.08, w: 0.7, h: 0.35, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: nmX + 0.75 + cw, y: nmY + ch + 0.08, w: 0.7, h: 0.35, fill: { color: ORANGE }, line: { color: ORANGE, width: 1 } });
s.addText("12", { x: nmX + 0.75 + cw, y: nmY + ch + 0.08, w: 0.7, h: 0.35, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: nmX + 0.6, y: nmY + ch * 2, w: cw, h: ch, fill: { color: "FFFFFF" }, line: { color: TEXT, width: 0.5 } });
s.addText("10", { x: nmX + 0.6, y: nmY + ch * 2, w: cw, h: ch, fontSize: 11, color: TEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: nmX + 0.75 + cw, y: nmY + ch * 2 + 0.08, w: 0.7, h: 0.35, fill: { color: GREEN }, line: { color: GREEN, width: 1 } });
s.addText("60", { x: nmX + 0.75 + cw, y: nmY + ch * 2 + 0.08, w: 0.7, h: 0.35, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// PRECISION BOX inside blue container, to the right
const pxX = contX + 3.4, pxY = contY + 0.3;
s.addShape(pptx.shapes.RECTANGLE, { x: pxX, y: pxY, w: 2.6, h: 2.5, fill: { color: "FFFFFF" }, line: { type: "none" } });
s.addText("Precision= 18/(18+12)", { x: pxX + 0.1, y: pxY + 0.3, w: 2.4, h: 0.3, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, align: "center", margin: 0 });
s.addText("=60%", { x: pxX + 0.1, y: pxY + 0.65, w: 2.4, h: 0.3, fontSize: 13, bold: true, color: TEXT, fontFace: FONT, align: "center", margin: 0 });

// ---- RED PANEL for decision trees ----
const panelX = rightX, panelY = contY + contH + 0.1, panelW = contW, panelH = 5.9 - (contY + contH + 0.1) - 0.15;
s.addShape(pptx.shapes.RECTANGLE, { x: panelX, y: panelY, w: panelW, h: panelH, fill: { color: BG }, line: { color: RED, width: 1.5 } });

// Headers INSIDE red panel as column headers
const treeY = panelY + 0.8;
const tX1 = panelX + 0.5, tX2 = panelX + 3.5;

s.addText("Positive", { x: tX1, y: panelY + 0.1, w: 2.2, h: 0.3, fontSize: 14, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0 });
s.addText("Negative", { x: tX2, y: panelY + 0.1, w: 2.2, h: 0.3, fontSize: 14, bold: true, color: GREEN, fontFace: FONT, align: "center", margin: 0 });

function drawAirplane(cx, cy) {
  s.addShape(pptx.shapes.LINE, { x: cx - 0.12, y: cy, w: 0.24, h: 0, line: { color: TEXT, width: 1.5 } });
  s.addShape(pptx.shapes.LINE, { x: cx, y: cy - 0.04, w: 0, h: 0.08, line: { color: TEXT, width: 1.5 } });
  s.addShape(pptx.shapes.LINE, { x: cx - 0.04, y: cy - 0.04, w: 0.08, h: 0.04, line: { color: TEXT, width: 1 } });
}
drawAirplane(tX1 + 1.1, treeY - 0.15);
drawAirplane(tX2 + 1.1, treeY - 0.15);

const darkBlue = "1565C0";
function drawTree(tx, rootColor, rootNum, leftColor, leftNum, leftLabel, rightColor, rightNum, rightLabel) {
  s.addShape(pptx.shapes.OVAL, { x: tx + 0.7, y: treeY, w: 0.6, h: 0.4, fill: { color: rootColor }, line: { color: rootColor, width: 1 } });
  s.addText(rootNum, { x: tx + 0.7, y: treeY, w: 0.6, h: 0.4, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addShape(pptx.shapes.LINE, { x: tx + 0.7, y: treeY + 0.4, w: -0.3, h: 0.2, line: { color: darkBlue, width: 1.5 } });
  s.addShape(pptx.shapes.LINE, { x: tx + 1.3, y: treeY + 0.4, w: 0.3, h: 0.2, line: { color: darkBlue, width: 1.5 } });
  s.addShape(pptx.shapes.OVAL, { x: tx + 0.1, y: treeY + 0.6, w: 0.6, h: 0.4, fill: { color: leftColor }, line: { color: leftColor, width: 1 } });
  s.addText(leftNum, { x: tx + 0.1, y: treeY + 0.6, w: 0.6, h: 0.4, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText(leftLabel, { x: tx + 0.1, y: treeY + 1.0, w: 0.6, h: 0.25, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0 });
  s.addShape(pptx.shapes.OVAL, { x: tx + 1.6, y: treeY + 0.6, w: 0.6, h: 0.4, fill: { color: rightColor }, line: { color: rightColor, width: 1 } });
  s.addText(rightNum, { x: tx + 1.6, y: treeY + 0.6, w: 0.6, h: 0.4, fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText(rightLabel, { x: tx + 1.6, y: treeY + 1.0, w: 0.6, h: 0.25, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0 });
}
drawTree(tX1, RED2, "30", RED2, "18", "TP", GREEN, "12", "FN");
drawTree(tX2, GREEN, "70", GREEN, "60", "TN", RED2, "10", "FP");

// ============================================================
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_010_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));