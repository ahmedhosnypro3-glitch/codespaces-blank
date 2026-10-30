// Build script for slide 037 of
// videos/machine-learning/03_ridger_regression_gradient_descent
// "Problem Formulation"
//
// Frame geometric measurements (unique_slides/slide_037.jpg, 960x540 px = slide pts,
// PIL-based measurement 2026-10-23):
//   Title: "Problem Formulation" - dark red (C00000), centered, rows 65-83, cols 354-627
//   Badge: "37" at (877, 73.5), d~28px
//   Gray panel (house chrome): x 54..903, y 45..540, fill E9E9E7
//   Red strokes: left x58, right x901, bottom y538.5 (NO top stroke)
//   Pale yellow panel (FFF9C4): rows ~110-200, cols ~70-890, red border
//   Tan panel 1 (F5E6CA): rows ~228-379, cols ~70-890, red border
//   Tan panel 2 (F5E6CA): rows ~380-519, cols ~70-890, red border
//   Text bands (ink tops, approx pt heights):
//     Define δ_i heading:    y111-134, ~23px, dark red C00000
//     Implication 1:         y146-162, ~16px, black + red highlights + blue italic class labels
//     Implication 2:         y172-189, ~17px, black + red highlights + blue italic class labels
//     Redefine Error heading: y243-256, ~13px, dark red C00000
//     Error equation:        y264-287, ~23px, black + red subscript/arrow
//     Summation positive:    y310-322, ~12px, black + red "positive"
//     Minimize heading:      y363-381, ~18px, black italic + blue "Gradient Descent"
//     First update eq:       y404-449, ~45px (two visual lines), black + red subscript
//     Second update eq:      y473-513, ~40px, black + red subscript + red "ONLY"
//   Green highlights:
//     Highlight 1: around "W^(updated) = W^(old)" on first eq, border rows 417-430, cols 724-752
//     Highlight 2: around full second eq, fill rows 465-514, cols 78-486, border rows 480-493, cols 432-460
//   Green arrow: between highlights, ~rows 450-470
//
// Spec: analysis/slide_037_final.json - verbatim text, colors, layout per recreation_brief
// Spec-vs-frame: frame geometry wins; spec provides verbatim text and color roles

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(
  __dirname, "..", "..", "shared_patterns", "house_chrome.js"
));

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const slide = pptx.addSlide();

// ---- House chrome: white canvas + E9E9E7 panel + C00000 L/R/bottom strokes + badge "37" ----
drawHouseChrome(pptx, slide, { numeral: 37 });

const FONT = "Arial";
const RED = "C00000";
const BLACK = "000000";
const BLUE = "0000FF";
const GREEN_FILL = "E8F5E9";
const GREEN_BORDER = "2E7D32";
const PALE_YELLOW = "FFF9C4";
const TAN = "F5E6CA";
const PANEL_RED = "C00000"; // panel border color

// Conversion: frame px (960x540) -> inches (1px = 1pt = 1/72 in)
const px = (v) => v / 72;

// ============================================================
// PANEL DEFINITIONS (measured frame coordinates)
// ============================================================
// Pale yellow panel (upper): ~rows 110-200
const PY_Y0 = px(110);
const PY_Y1 = px(200);
const PY_H = PY_Y1 - PY_Y0;
const PY_X = px(70);
const PY_W = px(890 - 70);

// Tan panel 1 (middle): ~rows 228-379
const T1_Y0 = px(228);
const T1_Y1 = px(379);
const T1_H = T1_Y1 - T1_Y0;
const T1_X = px(70);
const T1_W = px(890 - 70);

// Tan panel 2 (bottom): ~rows 380-519
const T2_Y0 = px(380);
const T2_Y1 = px(519);
const T2_H = T2_Y1 - T2_Y0;
const T2_X = px(70);
const T2_W = px(890 - 70);

// Panel border width (red stroke)
const PANEL_BORDER_W = 1.5; // pt

// Internal padding for text inside panels (frame px)
const PAD = px(12);

// ============================================================
// TITLE - add early to ensure it's above gray panel
// ============================================================
// Frame: centered at x~479.5, cap-top y~74 (rows 65-83)
slide.addText("Problem Formulation", {
  x: 0, y: px(68), w: 13.333, h: px(34),
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT,
  margin: 0,
});

// ============================================================
// PALE YELLOW PANEL (upper): Define δ_i as : + two implications
// ============================================================
// Panel background
slide.addShape(pptx.ShapeType.rect, {
  x: PY_X, y: PY_Y0, w: PY_W, h: PY_H,
  fill: { color: PALE_YELLOW }, line: { color: PANEL_RED, width: PANEL_BORDER_W },
});

// Heading: "Define δ_i as :"
slide.addText("Define \u03b4_i as :", {
  x: PY_X + PAD, y: PY_Y0 + PAD, w: PY_W - 2*PAD, h: px(28),
  fontSize: 18, bold: true, color: RED, fontFace: FONT,
  margin: 0, valign: "top",
});

// Implication 1: "If X ∈ class I and misclassified as Class II then d(X) will be <0 ⇒ δ_i = -1 ⇒ d(X)δ_i > 0"
// Row ~146-162. Black text, with:
// - "class I" and "Class II" italic blue
// - "misclassified" red
// - "⇒" (⇒) red
// - "δ_i" red
// - "-1" red
// - "> 0" red
// - "d(X)" underlined
const imp1_y = PY_Y0 + px(44);
slide.addText([
  { text: "If X \u2208 ", options: { color: BLACK, fontSize: 16 } },
  { text: "class I", options: { color: BLUE, fontSize: 16, italic: true } },
  { text: " and ", options: { color: BLACK, fontSize: 16 } },
  { text: "misclassified", options: { color: RED, fontSize: 16 } },
  { text: " as ", options: { color: BLACK, fontSize: 16 } },
  { text: "Class II", options: { color: BLUE, fontSize: 16, italic: true } },
  { text: " then ", options: { color: BLACK, fontSize: 16 } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, underline: true } },
  { text: " will be ", options: { color: BLACK, fontSize: 16 } },
  { text: "<0", options: { color: RED, fontSize: 16 } },
  { text: " \u21d2 ", options: { color: RED, fontSize: 16 } },
  { text: "\u03b4_i", options: { color: RED, fontSize: 16 } },
  { text: " = ", options: { color: RED, fontSize: 16 } },
  { text: "-1", options: { color: RED, fontSize: 16 } },
  { text: " \u21d2 ", options: { color: RED, fontSize: 16 } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, underline: true } },
  { text: "\u03b4_i", options: { color: RED, fontSize: 16 } },
  { text: " > 0", options: { color: RED, fontSize: 16 } },
], {
  x: PY_X + PAD, y: imp1_y, w: PY_W - 2*PAD, h: px(28),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// Implication 2: "If X ∈ class II and misclassified as Class I then d(X) will be >0 ⇒ δ_i = +1 ⇒ d(X)δ_i > 0"
// Row ~172-189
const imp2_y = imp1_y + px(30);
slide.addText([
  { text: "If X \u2208 ", options: { color: BLACK, fontSize: 16 } },
  { text: "class II", options: { color: BLUE, fontSize: 16, italic: true } },
  { text: " and ", options: { color: BLACK, fontSize: 16 } },
  { text: "misclassified", options: { color: RED, fontSize: 16 } },
  { text: " as ", options: { color: BLACK, fontSize: 16 } },
  { text: "Class I", options: { color: BLUE, fontSize: 16, italic: true } },
  { text: " then ", options: { color: BLACK, fontSize: 16 } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, underline: true } },
  { text: " will be ", options: { color: BLACK, fontSize: 16 } },
  { text: ">0", options: { color: RED, fontSize: 16 } },
  { text: " \u21d2 ", options: { color: RED, fontSize: 16 } },
  { text: "\u03b4_i", options: { color: RED, fontSize: 16 } },
  { text: " = ", options: { color: RED, fontSize: 16 } },
  { text: "+1", options: { color: RED, fontSize: 16 } },
  { text: " \u21d2 ", options: { color: RED, fontSize: 16 } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, underline: true } },
  { text: "\u03b4_i", options: { color: RED, fontSize: 16 } },
  { text: " > 0", options: { color: RED, fontSize: 16 } },
], {
  x: PY_X + PAD, y: imp2_y, w: PY_W - 2*PAD, h: px(28),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// ============================================================
// TAN PANEL 1 (middle): Redefine Error function
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: T1_X, y: T1_Y0, w: T1_W, h: T1_H,
  fill: { color: TAN }, line: { color: PANEL_RED, width: PANEL_BORDER_W },
});

// Heading: "Redefine Error function as:"
slide.addText("Redefine Error function as:", {
  x: T1_X + PAD, y: T1_Y0 + PAD, w: T1_W - 2*PAD, h: px(28),
  fontSize: 18, bold: true, color: RED, fontFace: FONT,
  margin: 0, valign: "top",
});

// Error equation: "Error = Σ_{all misclassified vectors (i)} δ_i W^T X_i ⇒ (W^T X_i) takes positive and negative values and δ_i has the same sign"
// Row ~264-287. Black text with:
// - Σ subscript "all misclassified vectors (i)" red
// - ⇒ red
// - δ_i red (both occurrences)
// - "positive" in red italic per spec
const eq1_y = T1_Y0 + px(40);
slide.addText([
  { text: "Error = ", options: { color: BLACK, fontSize: 16 } },
  { text: "\u03a3", options: { color: RED, fontSize: 20 } },
  { text: " all misclassified vectors (i) ", options: { color: RED, fontSize: 13 } },
  { text: "\u03b4_i W^T X_i ", options: { color: BLACK, fontSize: 16 } },
  { text: "\u21d2 ", options: { color: RED, fontSize: 16 } },
  { text: "(W^T X_i) takes ", options: { color: BLACK, fontSize: 16 } },
  { text: "positive", options: { color: RED, fontSize: 16, italic: true } },
  { text: " and negative values and ", options: { color: BLACK, fontSize: 16 } },
  { text: "\u03b4_i", options: { color: RED, fontSize: 16 } },
  { text: " has the same sign", options: { color: BLACK, fontSize: 16 } },
], {
  x: T1_X + PAD, y: eq1_y, w: T1_W - 2*PAD, h: px(36),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// "Summation is always positive" - row ~310-322
const sum_pos_y = eq1_y + px(38);
slide.addText([
  { text: "Summation is always ", options: { color: BLACK, fontSize: 16 } },
  { text: "positive", options: { color: RED, fontSize: 16, italic: true } },
], {
  x: T1_X + PAD, y: sum_pos_y, w: T1_W - 2*PAD, h: px(24),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// ============================================================
// TAN PANEL 2 (bottom): Minimize Error using Gradient Descent
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: T2_X, y: T2_Y0, w: T2_W, h: T2_H,
  fill: { color: TAN }, line: { color: PANEL_RED, width: PANEL_BORDER_W },
});

// Heading: "Minimize the Error using Gradient Descent with step η"
// Row ~363-381. Black italic, "Gradient Descent" blue bold
const head2_y = T2_Y0 + PAD;
slide.addText([
  { text: "Minimize the Error using ", options: { color: BLACK, fontSize: 16, italic: true } },
  { text: "Gradient Descent", options: { color: BLUE, fontSize: 16, bold: true, italic: true } },
  { text: " with step \u03b7", options: { color: BLACK, fontSize: 16, italic: true } },
], {
  x: T2_X + PAD, y: head2_y, w: T2_W - 2*PAD, h: px(28),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// ============================================================
// GREEN HIGHLIGHTS - add BEFORE text so text renders on top
// ============================================================

// Green highlight 1: around "W^(updated) = W^(old)" on first eq
// Frame: border rows 417-430, cols 724-752
// In inches: x=724/72..752/72 = 10.05..10.44, y=417/72..430/72 = 5.79..5.97
// Width ~0.4in, height ~0.18in
// Add padding: ~10px = 0.14in
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(714), y: px(407), w: px(50), h: px(33),
  fill: { color: GREEN_FILL }, line: { color: GREEN_BORDER, width: 1.5 },
});

// Green highlight 2: larger rounded rectangle around full second equation
// Frame: fill rows 465-514, cols 78-486 -> x=78..486, y=465..514
// Inches: x=1.08..6.75, y=6.46..7.14
// Width ~5.67in, height ~0.68in
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(68), y: px(455), w: px(428), h: px(64),
  fill: { color: GREEN_FILL }, line: { color: GREEN_BORDER, width: 1.5 },
});

// ============================================================
// FIRST UPDATE EQUATION
// "W^(updated) = W^(old) - η ∂Error/∂W where ∂Error/∂W = Σ_{misclassified vectors} δ_i X_i"
// Row ~404-449. Black text with:
// - "where" italic
// - Σ subscript "misclassified vectors" red
// Green highlight 1 around "W^(updated) = W^(old)" 
// ============================================================
const eq2_y = head2_y + px(34);
const eq2_x = T2_X + PAD;
const eq2_w = T2_W - 2*PAD;

// Part 1 - highlighted portion: "W^(updated) = W^(old)"
slide.addText("W^(updated) = W^(old)", {
  x: eq2_x, y: eq2_y, w: eq2_w, h: px(28),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// Part 2 - rest of first equation
slide.addText([
  { text: " - \u03b7 ", options: { color: BLACK, fontSize: 16 } },
  { text: "\u2202Error/\u2202W", options: { color: BLACK, fontSize: 16 } },
  { text: " where ", options: { color: BLACK, fontSize: 16, italic: true } },
  { text: "\u2202Error/\u2202W", options: { color: BLACK, fontSize: 16 } },
  { text: " = ", options: { color: BLACK, fontSize: 16 } },
  { text: "\u03a3", options: { color: RED, fontSize: 20 } },
  { text: " misclassified vectors ", options: { color: RED, fontSize: 13 } },
  { text: "\u03b4_i X_i", options: { color: BLACK, fontSize: 16 } },
], {
  x: eq2_x + px(110), y: eq2_y, w: eq2_w - px(110), h: px(28),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// ============================================================
// SECOND UPDATE EQUATION
// "W^(updated) = W^(old) - η Σ_{misclassified vectors ONLY (i)} δ_i X_i"
// Row ~473-513. Black text with:
// - Σ subscript "misclassified vectors ONLY (i)" red
// - "ONLY" red
// Green highlight 2 around entire expression
// ============================================================
const eq3_y = eq2_y + px(52);

slide.addText([
  { text: "W^(updated) = W^(old) - \u03b7 ", options: { color: BLACK, fontSize: 16 } },
  { text: "\u03a3", options: { color: RED, fontSize: 20 } },
  { text: " misclassified vectors ONLY (i) ", options: { color: RED, fontSize: 13 } },
  { text: "\u03b4_i X_i", options: { color: BLACK, fontSize: 16 } },
], {
  x: eq2_x, y: eq3_y, w: eq2_w, h: px(36),
  fontSize: 16, color: BLACK, fontFace: FONT,
  margin: 0, valign: "top",
});

// ============================================================
// GREEN ARROW: small curved arrow from highlight 1 down to highlight 2
// Frame: between highlights ~rows 450-470
// Approx: from bottom of first highlight (y~430) to top of second (y~465)
// Arrow at x ~ right side of first highlight (col ~752) pointing down-left to second
// ============================================================
slide.addShape(pptx.ShapeType.curvedDownArrow, {
  x: px(750), y: px(430), w: px(30), h: px(40),
  fill: { color: GREEN_BORDER }, line: { color: GREEN_BORDER, width: 2 },
});

// ============================================================
// OUTPUT
// ============================================================
const OUT = path.resolve(
  __dirname, "..", "..", "recreated_pptx", "slide_037_recreated.pptx"
);
pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));