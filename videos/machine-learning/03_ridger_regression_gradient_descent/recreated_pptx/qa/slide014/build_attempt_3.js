// slide_014.js — Ridge Regression Gradient Descent slide 014
// Built per spec: slide_014_final.json + PIL-measured geometry from unique_slides/slide_014.jpg
// House chrome from shared_patterns/house_chrome.js
// 2026-10-25 rebuild (w-s2): band/box geometry re-measured from the frame —
// vector boxes x80..433 / x457..810 with maroon borders; bands y243..285 (x58..901),
// y303..341, define-loss x90..665 y347..392, term boxes y399..448 (left x89..471,
// right x533..880), final box x87..880 y469..528.

const pptxgenpkg = require("pptxgenjs");
const pptxgen = new pptxgenpkg();
pptxgen.layout = "LAYOUT_WIDE";
const pptx = pptxgen;

const s = pptx.addSlide();

// ---- HOUSE CHROME ----
require("../../shared_patterns/house_chrome.js").drawHouseChrome(pptx, s, { numeral: 14 });

// ============ STYLE CONSTANTS ============
const FONT = "Arial";
const BLUE = "0000FF";
const GREEN = "008000";
const RED = "FF0000";
const BLACK = "000000";
const MAROON = "8F1220";      // vector-box borders + "Function that" title run
const TITLE_MAROON = "800020";
const NAVY = "1E0060";        // band rules
const YEL = "F9FBDC";         // ridge/objective band interiors
const PEACH = "F9DEC1";       // define-loss band
const PEACH2 = "F9DFC8";      // left term box
const PALE_YEL = "F9FEDE";    // right term box
const PALE_CYAN = "ECFFFD";   // final objective band
const WHITE = "FFFFFF";

const ASSETS = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/";

// ============ TITLE (measured: blue / maroon / blue, y70..92, centered x190..744) ============
s.addText([
  { text: "LOSS ", options: { fontSize: 28, bold: true, color: BLUE, fontFace: FONT } },
  { text: "Function that ", options: { fontSize: 28, bold: true, color: TITLE_MAROON, fontFace: FONT } },
  { text: "MINIMIZES Overfitting", options: { fontSize: 28, bold: true, color: BLUE, fontFace: FONT } },
], {
  x: 0.6, y: 0.85, w: 12.13, h: 0.55, align: "center", valign: "top", margin: 0,
  lineSpacing: 33.6,
});

// ============ VECTOR BOXES (y99..238; left x80..433, right x457..810) ============
const vboxY = 99 / 72;
const vboxH = 140 / 72;
const leftX = 80 / 72, leftW = 354 / 72;
const rightX = 457 / 72, rightW = 353 / 72;

s.addShape(pptx.ShapeType.rect, { x: leftX, y: vboxY, w: leftW, h: vboxH, fill: { color: WHITE }, line: { color: MAROON, width: 2 } });
s.addShape(pptx.ShapeType.rect, { x: rightX, y: vboxY, w: rightW, h: vboxH, fill: { color: WHITE }, line: { color: MAROON, width: 2 } });

// Left box: red column-vector equation PNG + two text lines
s.addImage({ path: ASSETS + "eq_014_Yvec.png", x: leftX + 0.3, y: vboxY + 0.12, w: 1.88, h: 0.80167 });
s.addText([
  { text: "Original Labels", options: { fontSize: 18, bold: true, color: BLACK, fontFace: FONT } },
], { x: leftX + 0.25, y: vboxY + 1.0, w: leftW - 0.5, h: 0.32, align: "left", valign: "top", margin: 0, lineSpacing: 21.6 });
s.addText([
  { text: "from Training Samples", options: { fontSize: 18, color: BLACK, fontFace: FONT } },
], { x: leftX + 0.25, y: vboxY + 1.34, w: leftW - 0.5, h: 0.32, align: "left", valign: "top", margin: 0, lineSpacing: 21.6 });

// Right box: blue column-vector equation PNG + two text lines
s.addImage({ path: ASSETS + "eq_014_Yhatvec.png", x: rightX + 0.3, y: vboxY + 0.12, w: 2.02333, h: 1.06667 });
s.addText([
  { text: "Predicted Labels", options: { fontSize: 18, bold: true, color: BLACK, fontFace: FONT } },
], { x: rightX + 0.25, y: vboxY + 1.26, w: rightW - 0.5, h: 0.32, align: "left", valign: "top", margin: 0, lineSpacing: 21.6 });
s.addText([
  { text: "from Model \u0176 = XW", options: { fontSize: 18, color: BLACK, fontFace: FONT } },
], { x: rightX + 0.25, y: vboxY + 1.6, w: rightW - 0.5, h: 0.32, align: "left", valign: "top", margin: 0, lineSpacing: 21.6 });

// ============ BAND 1 — Ridge Regularization (y243..285, x58..901, yellow, navy rules) ============
const bandX = 58 / 72, bandW = (901 - 58) / 72;
const ruleH = 3 / 72;
function band(yTop, hPx, fill, ruleColor) {
  const y = yTop / 72, h = hPx / 72;
  s.addShape(pptx.ShapeType.rect, { x: bandX, y, w: bandW, h, fill: { color: fill } });
  s.addShape(pptx.ShapeType.rect, { x: bandX, y, w: bandW, h: ruleH, fill: { color: ruleColor } });
  s.addShape(pptx.ShapeType.rect, { x: bandX, y: y + h - ruleH, w: bandW, h: ruleH, fill: { color: ruleColor } });
  return { y, h };
}
const b1 = band(243, 43, YEL, NAVY);
const b1t = { x: bandX + 0.25, y: b1.y + ruleH, w: bandW - 0.5, h: b1.h - 2 * ruleH };
s.addText([
  { text: "Objective is ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "\u0176=Y", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT } },
  { text: " and ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "||W||", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT } },
  { text: " is minimum", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
], { x: b1t.x, y: b1t.y, w: b1t.w, h: b1t.h, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });
s.addText([
  { text: "This is called ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "Ridge Regularization", options: { fontSize: 17, bold: true, color: GREEN, fontFace: FONT } },
], { x: b1t.x, y: b1t.y + 0.20, w: b1t.w, h: b1t.h - 0.20, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });

// ============ BAND 2 — Objective function (y303..341, x58..901, yellow, navy rules) ============
const b2 = band(303, 39, YEL, NAVY);
const b2t = { x: bandX + 0.25, y: b2.y + ruleH, w: bandW - 0.5, h: b2.h - 2 * ruleH };
s.addText([
  { text: "Objective function ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "J(W)", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT } },
  { text: " = ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "Loss", options: { fontSize: 17, bold: true, color: RED, fontFace: FONT } },
  { text: "(X,Y,W) + ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "\u03bb", options: { fontSize: 17, color: BLUE, fontFace: FONT } },
  { text: " ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "R(W)", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT } },
], { x: b2t.x, y: b2t.y, w: b2t.w, h: b2t.h, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });
s.addText([
  { text: "(", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  { text: "\u03bb", options: { fontSize: 17, color: BLUE, fontFace: FONT } },
  { text: " is a weighting factor)", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
], { x: b2t.x, y: b2t.y + 0.19, w: b2t.w, h: b2t.h - 0.19, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });

// ============ DEFINE LOSS band (x90..665, y347..392, peach, maroon rules) ============
{
  const x = 90 / 72, y = 347 / 72, w = (665 - 90) / 72, h = 45 / 72;
  s.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: PEACH } });
  s.addShape(pptx.ShapeType.rect, { x, y, w, h: ruleH, fill: { color: MAROON } });
  s.addShape(pptx.ShapeType.rect, { x, y: y + h - ruleH, w, h: ruleH, fill: { color: MAROON } });
  s.addText([
    { text: "Define ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "Loss", options: { fontSize: 17, bold: true, color: RED, fontFace: FONT } },
    { text: " function as ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "squared distance", options: { fontSize: 17, bold: true, color: GREEN, fontFace: FONT } },
    { text: " between ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "\u0176", options: { fontSize: 17, bold: true, italic: true, color: BLACK, fontFace: FONT } },
    { text: " and ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "Y", options: { fontSize: 17, bold: true, italic: true, color: BLACK, fontFace: FONT } },
  ], { x: x + 0.25, y: y + ruleH, w: w - 0.5, h: h - 2 * ruleH, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });
}

// ============ TERM BOXES (y399..448: left x89..471 peach, right x533..880 pale yellow) ============
{
  const y = 399 / 72, h = 49 / 72;
  const lx = 89 / 72, lw = (471 - 89) / 72;
  const rx = 533 / 72, rw = (880 - 533) / 72;
  s.addShape(pptx.ShapeType.rect, { x: lx, y, w: lw, h, fill: { color: PEACH2 } });
  s.addShape(pptx.ShapeType.rect, { x: rx, y, w: rw, h, fill: { color: PALE_YEL } });
  s.addText([
    { text: "Loss Term", options: { fontSize: 17, bold: true, color: RED, fontFace: FONT } },
    { text: " = ||Y-\u0176||", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "2", options: { fontSize: 17, color: BLACK, fontFace: FONT, superscript: true } },
    { text: " = (Y-\u0176)", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "T", options: { fontSize: 17, color: BLACK, fontFace: FONT, superscript: true } },
    { text: "(Y-\u0176)", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  ], { x: lx + 0.15, y: y + 0.08, w: lw - 0.3, h: h - 0.16, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });
  s.addText([
    { text: "Regularization Term", options: { fontSize: 17, bold: true, color: BLUE, fontFace: FONT } },
    { text: " R = ||W||", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "2", options: { fontSize: 17, color: BLACK, fontFace: FONT, superscript: true } },
    { text: " = W", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
    { text: "T", options: { fontSize: 17, color: BLACK, fontFace: FONT, superscript: true } },
    { text: "W", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  ], { x: rx + 0.15, y: y + 0.08, w: rw - 0.3, h: h - 0.16, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });
}

// ============ FINAL OBJECTIVE BAND (x87..880, y469..528, pale cyan, navy rules) ============
{
  const x = 87 / 72, y = 469 / 72, w = (880 - 87) / 72, h = 59 / 72;
  s.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: PALE_CYAN } });
  s.addShape(pptx.ShapeType.rect, { x, y, w, h: ruleH, fill: { color: NAVY } });
  s.addShape(pptx.ShapeType.rect, { x, y: y + h - ruleH, w, h: ruleH, fill: { color: NAVY } });
  s.addText([
    { text: "Objective function ", options: { fontSize: 17, color: BLACK, fontFace: FONT } },
  ], { x: x + 0.2, y: y + ruleH, w: 2.2, h: h - 2 * ruleH, align: "left", valign: "middle", margin: 0, lineSpacing: 20 });
  // 2D professional-format objective formula (stacked 1/2 fraction), baseline-aligned to the text line
  s.addImage({ path: ASSETS + "eq_014_final.png", x: x + 2.1, y: y + 0.10, w: 4.21667, h: 0.39 });
}

// ============ WRITE OUTPUT ============
const outPath = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_014_recreated.pptx";
pptx.write({ fileName: outPath }).then(() => console.log("done: " + outPath));
