// slide_014.js — Ridge Regression Gradient Descent slide 014
// Built per spec: slide_014_final.json + PIL-measured geometry from unique_slides/slide_014.jpg
// House chrome from shared_patterns/house_chrome.js

const pptxgenpkg = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.333, H = 7.5;

let s = pptx.addSlide();

// ---- HOUSE CHROME ----
drawHouseChrome(pptx, s, { numeral: 14 });

// ============ CONTENT POSITIONING (px -> in: divide by 72) ============
// Original frame: 960x540, 1px = 1pt = 1/72 in

// Panel inner content area (inside gray panel, away from red strokes)
// Panel: x 54..903, y 45..540 px → in: x 0.75..12.54, y 0.625..7.5
// Left stroke at x=58.5, right at x=901, bottom at y=538.5
// Inner safe area: x 58.5..901 (0.8125..12.51), y 46..538 (0.64..7.47)

// Content vertical bands (measured from frame):
// Title: y ~70px (0.97in)
// Badge: center (876,73) px
// Vector boxes: y 104..232 px (1.44..3.22in)
// Ridge band: y 250..278 px (3.47..3.86in)
// Objective band: y 310..334 px (4.31..4.64in)
// Define Loss band: y 398 px (5.53in)
// Loss/Reg boxes: y 468..520 px (6.50..7.22in)
// Final band: y 510..520 px (7.08..7.22in)

// Horizontal splits:
// Left column: x ~54..450 px (0.75..6.25in)
// Right column: x ~500..880 px (6.94..12.22in)
// Gap: ~450..500 px

// ============ STYLE CONSTANTS ============
const FONT = "Arial";
const BLACK = "000000";
const BLUE = "0000FF";
const RED = "FF0000";
const GREEN = "008000";

// Yellow band: #FFF9C4 (255,249,196)
const YEL_BAND = "FFF9C4";
// Pink band: #FFEBEE (255,235,238)
const PNK_BAND = "FFEBEE";
// Light blue band: #E1F5FE (225,245,254)
const LBLU_BAND = "E1F5FE";
// White box
const WHITE = "FFFFFF";

// ============ TITLE ============
// "LOSS Function that MINIMIZES Overfitting"
// LOSS, MINIMIZES, Overfitting in blue; "Function that" in black
// Top-left, y ~70px = 0.97in, left align
s.addText([
  { text: "LOSS ", options: { fontSize: 38, bold: true, color: BLUE, fontFace: FONT } },
  { text: "Function that ", options: { fontSize: 38, bold: true, color: BLACK, fontFace: FONT } },
  { text: "MINIMIZES ", options: { fontSize: 38, bold: true, color: BLUE, fontFace: FONT } },
  { text: "Overfitting", options: { fontSize: 38, bold: true, color: BLUE, fontFace: FONT } },
], {
  x: 0.85, y: 0.75, w: 11.5, h: 0.7, align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// ============ VECTOR BOXES ============
// Left: Original Labels box - white rect with black border
// Right: Predicted Labels box - white rect with black border
const boxY = 104 / 72;      // 1.444 in
const boxH = (232 - 104) / 72;  // 1.778 in
const leftX = 54 / 72;      // 0.75 in
const rightX = 500 / 72;    // 6.944 in
const boxW = (450 - 54) / 72;  // 5.5 in approx (gap at ~450..500)

// Left box - white with black border
s.addShape("rect", {
  x: leftX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});

// Right box
s.addShape("rect", {
  x: rightX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});

// LEFT BOX CONTENT
// "Let Y = [y1; y2; ...; yn] Nx1"
// "Original Labels"
// "from Training Samples"
const leftTextX = leftX + 0.15;  // padding
const leftTextW = boxW - 0.3;
s.addText([
  { text: "Let Y = [y1; y2; ...; yn] Nx1", options: { fontSize: 16, bold: true, color: BLACK, fontFace: FONT, italic: true } },
  { text: "Original Labels", options: { fontSize: 16, bold: true, color: BLACK, fontFace: FONT }, breakLine: true },
  { text: "from Training Samples", options: { fontSize: 16, color: BLACK, fontFace: FONT }, breakLine: true },
], {
  x: leftTextX, y: boxY + 0.1, w: leftTextW, h: boxH - 0.2, align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// RIGHT BOX CONTENT
// "Let Ŷ = [ŷ1; ŷ2; ...; ŷn] Nx1"
// "Predicted Labels"
// "from Model Ŷ = XW"
const rightTextX = rightX + 0.15;
s.addText([
  { text: "Let Ŷ = [ŷ1; ŷ2; ...; ŷn] Nx1", options: { fontSize: 16, bold: true, color: BLACK, fontFace: FONT, italic: true } },
  { text: "Predicted Labels", options: { fontSize: 16, bold: true, color: BLACK, fontFace: FONT }, breakLine: true },
  { text: "from Model Ŷ = XW", options: { fontSize: 16, color: BLACK, fontFace: FONT }, breakLine: true },
], {
  x: rightTextX, y: boxY + 0.1, w: leftTextW, h: boxH - 0.2, align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// ============ RIDGE REGULARIZATION BAND (Yellow) ============
// y 250..278 px → 3.47..3.86 in
const ridgeY = 250 / 72;  // 3.472
const ridgeH = 28 / 72;   // 0.389
s.addShape("rect", {
  x: CHROME.panel.x, y: ridgeY, w: CHROME.panel.w, h: ridgeH,
  fill: { color: YEL_BAND },
});
s.addText([
  { text: "Objective is ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "Ŷ=Y", options: { fontSize: 16, bold: true, color: BLUE, fontFace: FONT } },
  { text: " and ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "||W||", options: { fontSize: 16, bold: true, color: BLUE, fontFace: FONT } },
  { text: " is minimum", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
], {
  x: CHROME.panel.x + 0.2, y: ridgeY + 0.02, w: CHROME.panel.w - 0.4, h: ridgeH - 0.04,
  align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});
s.addText([
  { text: "This is called ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "Ridge Regularization", options: { fontSize: 16, bold: true, color: GREEN, fontFace: FONT } },
], {
  x: CHROME.panel.x + 0.2, y: ridgeY + ridgeH/2, w: CHROME.panel.w - 0.4, h: ridgeH/2,
  align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// ============ OBJECTIVE FUNCTION BAND (Yellow) ============
// y 310..334 px → 4.31..4.64 in
const objY = 310 / 72;  // 4.306
const objH = 24 / 72;   // 0.333
s.addShape("rect", {
  x: CHROME.panel.x, y: objY, w: CHROME.panel.w, h: objH,
  fill: { color: YEL_BAND },
});
s.addText([
  { text: "Objective function ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "J(W)", options: { fontSize: 16, bold: true, color: BLUE, fontFace: FONT } },
  { text: " = ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "Loss", options: { fontSize: 16, bold: true, color: RED, fontFace: FONT } },
  { text: "(X,Y,W) + ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "λ", options: { fontSize: 16, color: BLUE, fontFace: FONT } },
  { text: " ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "R(W)", options: { fontSize: 16, bold: true, color: BLUE, fontFace: FONT } },
  { text: "   (", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "λ", options: { fontSize: 16, color: BLUE, fontFace: FONT } },
  { text: " is a weighting factor)", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
], {
  x: CHROME.panel.x + 0.2, y: objY + 0.02, w: CHROME.panel.w - 0.4, h: objH - 0.04,
  align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// ============ DEFINE LOSS BAND (Pink) ============
// y 398 px → 5.53 in, roughly same height
const lossY = 398 / 72;  // 5.528
const lossH = 24 / 72;   // 0.333
s.addShape("rect", {
  x: CHROME.panel.x, y: lossY, w: CHROME.panel.w, h: lossH,
  fill: { color: PNK_BAND },
});
s.addText([
  { text: "Define ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "Loss", options: { fontSize: 16, bold: true, color: RED, fontFace: FONT } },
  { text: " function as ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "squared distance", options: { fontSize: 16, bold: true, color: GREEN, fontFace: FONT } },
  { text: " between ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "Ŷ", options: { fontSize: 16, bold: true, italic: true, color: BLACK, fontFace: FONT } },
  { text: " and ", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
  { text: "Y", options: { fontSize: 16, bold: true, italic: true, color: BLACK, fontFace: FONT } },
], {
  x: CHROME.panel.x + 0.2, y: lossY + 0.02, w: CHROME.panel.w - 0.4, h: lossH - 0.04,
  align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// ============ LOSS TERM / REGULARIZATION TERM BOXES (Light Blue) ============
// y 468..520 px → 6.50..7.22 in
const termY = 468 / 72;  // 6.50
const termH = (520 - 468) / 72;  // 0.722

// Left: Loss Term box
s.addShape("rect", {
  x: leftX, y: termY, w: boxW, h: termH,
  fill: { color: LBLU_BAND },
});
s.addText([
  { text: "Loss Term = ||Y-Ŷ||² = (Y-Ŷ)ᵀ(Y-Ŷ)", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
], {
  x: leftTextX, y: termY + 0.1, w: leftTextW, h: termH - 0.2, align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// Make "Loss Term" red
// We'll use rich text to color "Loss Term" red
s.addText([
  { text: "Loss Term", options: { fontSize: 16, bold: true, color: RED, fontFace: FONT } },
  { text: " = ||Y-Ŷ||² = (Y-Ŷ)ᵀ(Y-Ŷ)", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
], {
  x: leftTextX, y: termY + 0.1, w: leftTextW, h: termH - 0.2, align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// Right: Regularization Term box
s.addShape("rect", {
  x: rightX, y: termY, w: boxW, h: termH,
  fill: { color: LBLU_BAND },
});
s.addText([
  { text: "Regularization Term", options: { fontSize: 16, bold: true, color: BLUE, fontFace: FONT } },
  { text: " R = ||W||² = WᵀW", options: { fontSize: 16, color: BLACK, fontFace: FONT } },
], {
  x: rightTextX, y: termY + 0.1, w: leftTextW, h: termH - 0.2, align: "left", valign: "top", margin: 0, lineSpacing: 1.2,
});

// ============ FINAL OBJECTIVE BAND (Light Blue) ============
// y 510..520 px → 7.08..7.22 in
const finalY = 510 / 72;  // 7.083
const finalH = 10 / 72;   // 0.139 (thin band)
s.addShape("rect", {
  x: CHROME.panel.x, y: finalY, w: CHROME.panel.w, h: finalH,
  fill: { color: LBLU_BAND },
});
s.addText([
  { text: "Objective function ", options: { fontSize: 14, color: BLACK, fontFace: FONT } },
  { text: "J(W)", options: { fontSize: 14, bold: true, color: BLUE, fontFace: FONT } },
  { text: " = 1/2 [ (Y-Ŷ)ᵀ(Y-Ŷ) + ", options: { fontSize: 14, color: BLACK, fontFace: FONT } },
  { text: "λ", options: { fontSize: 14, color: BLUE, fontFace: FONT } },
  { text: " WᵀW ]", options: { fontSize: 14, color: BLACK, fontFace: FONT } },
], {
  x: CHROME.panel.x + 0.2, y: finalY + 0.01, w: CHROME.panel.w - 0.4, h: finalH - 0.02,
  align: "left", valign: "top", margin: 0, lineSpacing: 1.0,
});

// ============ WRITE OUTPUT ============
const outPath = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_014_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));