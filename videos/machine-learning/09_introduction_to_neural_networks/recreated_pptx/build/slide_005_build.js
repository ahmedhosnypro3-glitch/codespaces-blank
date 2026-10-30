const pptxgen = require("pptxgenjs");

// Slide 005: Visualization of Single Perceptron
const NUM = 5;
const TITLE = "Visualization of Single Perceptron";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const GREEN = "00B050";
const BORDER_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const BADGE_OUTLINE = "4B0082";
const BADGE_NUM = "4B0082";
const YELLOW = "FFF9C4";
const BEIGE = "E8E0C8";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Bottom black bar - from validation analysis (video player overlay)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

// 3. Slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_NUM, fontFace: FONT, margin: 0,
});

// 4. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 5. Top-left box: Augmented Vector
// Position: upper left, roughly x=9% to x=45%, y=19% to y=37%
const tl_x = 1.2;
const tl_y = 1.43;
const tl_w = 4.8;
const tl_h = 1.35;

s.addShape(pres.shapes.RECTANGLE, {
  x: tl_x, y: tl_y, w: tl_w, h: tl_h,
  fill: { color: WHITE }, line: { color: RED, width: 1 },
});

// Label: "Augmented Vector" (blue italic)
s.addText("Augmented Vector", {
  x: tl_x + 0.15, y: tl_y + 0.05, w: tl_w - 0.3, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, color: BLUE, fontFace: FONT, italic: true, margin: 0,
});

// Input vector X
let y = tl_y + 0.35;
s.addText([
  { text: "X = [", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "₁", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "₂", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "; ...; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "ₙ", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "]", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
], {
  x: tl_x + 0.15, y: y, w: tl_w - 0.3, h: 0.35,
  align: "left", valign: "top", margin: 0,
});

y += 0.35;
// Arrow
s.addText("→", {
  x: tl_x + 0.15, y: y, w: tl_w - 0.3, h: 0.3,
  align: "left", valign: "top",
  fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

y += 0.3;
// Augmented vector X = [1; x₁; x₂; ...; xₙ]
s.addText([
  { text: "X = [", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "1", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "₁", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "₂", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "; ...; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "ₙ", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "]", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
], {
  x: tl_x + 0.15, y: y, w: tl_w - 0.3, h: 0.35,
  align: "left", valign: "top", margin: 0,
});

// 6. Top-right box: Model Weights
// Position: upper right, roughly x=55% to x=91%, y=19% to y=37%
const tr_x = 7.33;
const tr_y = 1.43;
const tr_w = 4.8;
const tr_h = 1.35;

s.addShape(pres.shapes.RECTANGLE, {
  x: tr_x, y: tr_y, w: tr_w, h: tr_h,
  fill: { color: WHITE }, line: { color: RED, width: 1 },
});

// Label: "Model Weights" (blue italic)
s.addText("Model Weights", {
  x: tr_x + 0.15, y: tr_y + 0.05, w: tr_w - 0.3, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, color: BLUE, fontFace: FONT, italic: true, margin: 0,
});

// Weight vector W = [b; w₁; w₂; ...; wₙ]
y = tr_y + 0.5;
s.addText([
  { text: "W = [", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "b", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "w", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "₁", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "w", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "₂", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "; ...; ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "w", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "ₙ", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "]", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
], {
  x: tr_x + 0.15, y: y, w: tr_w - 0.3, h: 0.35,
  align: "left", valign: "top", margin: 0,
});

// 7. Middle box: Decision function and classification
// Position: middle, roughly x=9% to x=80%, y=48% to y=62%
const mid_x = 1.2;
const mid_y = 3.6;
const mid_w = 9.47;
const mid_h = 1.05;

s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: mid_x, y: mid_y, w: mid_w, h: mid_h,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

y = mid_y + 0.1;
// Left side: equation d(X) = W^T X = ...
s.addText([
  { text: "d(X) = W", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT } },
  { text: "ᵀ", options: { color: BLACK, bold: true, fontSize: 12, fontFace: FONT } },
  { text: " X = ", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT } },
  { text: "w", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT, italic: true } },
  { text: "₁", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT, italic: true } },
  { text: "₁", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: " + ", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT } },
  { text: "w", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT, italic: true } },
  { text: "₂", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT, italic: true } },
  { text: "₂", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: " + ... + ", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT } },
  { text: "w", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT, italic: true } },
  { text: "ₙ", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: "x", options: { color: BLACK, bold: true, fontSize: 18, fontFace: FONT, italic: true } },
  { text: "ₙ", options: { color: BLACK, bold: true, fontSize: 10, fontFace: FONT } },
  { text: " + b", options: { color: RED, bold: true, fontSize: 18, fontFace: FONT } },
], {
  x: mid_x + 0.2, y: y, w: mid_w - 0.4, h: 0.4,
  align: "left", valign: "top", margin: 0,
});

// Right side: classification brace with three lines - INCREASE WIDTH to prevent clipping
const brace_x = mid_x + mid_w - 1.4;
s.addText(">0 ⇒ Class I", {
  x: brace_x, y: mid_y + 0.1, w: 1.3, h: 0.25,
  align: "left", valign: "top",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

s.addText("<0 ⇒ Class II", {
  x: brace_x, y: mid_y + 0.35, w: 1.3, h: 0.25,
  align: "left", valign: "top",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

s.addText("=0 ⇒ Undefined Class", {
  x: brace_x, y: mid_y + 0.6, w: 1.3, h: 0.25,
  align: "left", valign: "top",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Add a right brace character as text (approximation)
s.addText("}", {
  x: brace_x - 0.15, y: mid_y + 0.1, w: 0.2, h: 0.65,
  align: "center", valign: "middle",
  fontSize: 48, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 8. Bottom-left: Perceptron network diagram (embed generated PNG)
// Position: bottom left, roughly x=24% to x=64%, y=64% to y=94%
const diag_x = 3.2;
const diag_y = 4.8;
const diag_w = 4.5;
const diag_h = 2.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: diag_x, y: diag_y, w: diag_w, h: diag_h,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// Embed the generated perceptron diagram PNG
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_005_perceptron_diagram.png",
  x: diag_x + 0.05, y: diag_y + 0.05, w: diag_w - 0.1, h: diag_h - 0.1,
});

// 9. Bottom-right: Beige caption box "Binary Classification (2 Classes)"
// Position: bottom right, roughly x=66% to x=85%, y=74% to y=82%
const cap_x = 8.8;
const cap_y = 5.55;
const cap_w = 2.5;
const cap_h = 0.6;

s.addShape(pres.shapes.RECTANGLE, {
  x: cap_x, y: cap_y, w: cap_w, h: cap_h,
  fill: { color: BEIGE }, line: { color: "none" },
});
s.addText("Binary Classification (2 Classes)", {
  x: cap_x + 0.1, y: cap_y + 0.05, w: cap_w - 0.2, h: cap_h - 0.1,
  align: "center", valign: "middle",
  fontSize: 14, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_005_recreated.pptx" 
}).then(() => console.log("wrote slide_005_recreated.pptx"));