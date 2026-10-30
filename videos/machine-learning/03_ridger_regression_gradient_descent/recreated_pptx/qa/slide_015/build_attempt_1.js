const pptxgen = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";   // 13.333 x 7.5 in
const W = 13.333, H = 7.5;

let s = pptx.addSlide();

// --- House chrome (panel, strokes, badge) ---
drawHouseChrome(pptx, s, { numeral: "15" });

// ============================================================
// MEASURED GEOMETRY (frame px -> inches via /72, 1px = 1pt)
// ============================================================
// Title: y=68..84 (17px tall), words x=129..826 (697px wide, 64 chars).
//   Arial Bold char advance ~0.62em -> orig font ~19-20pt (measured).
//   Words alternate RED/BLUE: "Minimization of" (R) "Objective" (B)
//   "function to obtain" (R) "BEST" (B) "model parameters" (R)
//   Box must be wide enough to avoid wrap: use x=1.7, w=10.1 in.
const TITLE_X = 1.7, TITLE_Y = 0.92, TITLE_W = 10.1, TITLE_H = 0.32;
const TITLE_SIZE = 20;

// Eq block 1: y=105..155 (three lines), center x~499 (frame)
//   Frame y=105..155 → in: 105/72=1.46 .. 155/72=2.15
//   Use y=1.5 in, h=0.8 in
const EQ1_Y = 1.5, EQ1_H = 0.8;

// Red box (callout): border y=276..333, x=80..700 (frame)
//   Frame y=276..333 → in: 3.83 .. 4.63
//   Use y=3.8 in, h=0.85 in, x=1.1 in, w=8.6 in
const RED_BOX_X = 1.1, RED_BOX_Y = 3.8, RED_BOX_W = 8.6, RED_BOX_H = 0.85;
const RED_BORDER = "C00000"; // red border

// Peach box (Remember): fill x=788..903, y=275..334 (frame)
//   Frame x=788..903 → in: 10.94 .. 12.54
//   y same as red box
//   Use x=10.9 in, w=1.6 in, same y/h as red box
const PEACH_BOX_X = 10.9, PEACH_BOX_W = 1.6, PEACH_FILL = "FCE4D6";

// Derivative steps: y=345..410 (two lines), center x~490
//   Frame y=345..410 → in: 4.79 .. 5.69
//   Use y=4.85 in, h=0.9 in
const DERIV_Y = 4.85, DERIV_H = 0.9;

// Normal equation line: y=412..470, center x~490
//   Frame y=412..470 → in: 5.72 .. 6.53
//   Use y=5.8 in, h=0.7 in
const NORMALEQ_Y = 5.8, NORMALEQ_H = 0.7;

// Green box: border y=473..516, x=314..884 (frame)
//   Frame y=473..516 → in: 6.57 .. 7.17
//   x=314..884 → in: 4.36 .. 12.28
//   Use x=4.4 in, w=7.9 in, y=6.6 in, h=0.55 in
const GREEN_BOX_X = 4.4, GREEN_BOX_Y = 6.6, GREEN_BOX_W = 7.9, GREEN_BOX_H = 0.55;
const GREEN_BORDER = "00B050";
const GREEN_FILL = "E2EFDA";

// Colors
const DARK_BLUE = "00008B";   // body text
const RED_TEXT  = "FF0000";   // red accents
const BLUE_TEXT = "0000FF";   // blue accents
const FONT = "Arial";
const MATH_FONT = "Times New Roman";  // serif/math style for equations

// ============================================================
// TITLE — word-by-word alternating red/blue
// ============================================================
// Use a single text box with rich-text runs to get exact coloring
s.addText([
  { text: "Minimization of ", options: { fontSize: TITLE_SIZE, bold: true, color: RED_TEXT, fontFace: FONT } },
  { text: "Objective ",       options: { fontSize: TITLE_SIZE, bold: true, color: BLUE_TEXT, fontFace: FONT } },
  { text: "function to obtain ", options: { fontSize: TITLE_SIZE, bold: true, color: RED_TEXT, fontFace: FONT } },
  { text: "BEST ",            options: { fontSize: TITLE_SIZE, bold: true, color: BLUE_TEXT, fontFace: FONT } },
  { text: "model parameters", options: { fontSize: TITLE_SIZE, bold: true, color: RED_TEXT, fontFace: FONT } },
], {
  x: TITLE_X, y: TITLE_Y, w: TITLE_W, h: TITLE_H,
  align: "left", valign: "middle", margin: 0,
});

// ============================================================
// EQUATION BLOCK 1 — three lines, centered, dark blue serif
// ============================================================
const eq1Lines = [
  "J(W)=½(Y−Ŷ)^T(Y−Ŷ)+½ λ W^T W = ½(Y−XW)^T(Y−XW)+½ λ W^T W",
  "J(W)=½[Y^T Y + (XW)^T(XW) − Y^T(XW) − (XW)^T Y]+½ λ W^T W",
  "J(W)=½[Y^T Y + (XW)^T(XW) − 2(XW)^T Y]+½ λ W^T W",
];

s.addText(eq1Lines.map((t, i) => ({
  text: t,
  options: { fontSize: 16, color: DARK_BLUE, fontFace: MATH_FONT, bold: false, breakLine: i < eq1Lines.length - 1 },
})), {
  x: 1.1, y: EQ1_Y, w: W - 2.2, h: EQ1_H,
  align: "center", valign: "middle", margin: 0, lineSpacing: 19.2,
});

// ============================================================
// RED CALLOUT BOX — middle-left
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: RED_BOX_X, y: RED_BOX_Y, w: RED_BOX_W, h: RED_BOX_H,
  fill: { color: "FFFFFF" },
  line: { color: RED_BORDER, width: 1.5 },
});

// Text boxes: explicit point lineSpacing (fleet convention — pptxgenjs turns a
// bare fraction into spcPts = value*100, which LibreOffice renders as nothing).
s.addText([
  { text: "∂J(W)/∂W = 0", options: { fontSize: 16, color: DARK_BLUE, fontFace: MATH_FONT, bold: true, breakLine: true } },
  { text: "Get Best W that minimizes the ", options: { fontSize: 14, color: DARK_BLUE, fontFace: FONT } },
  { text: "Objective Function J(W)", options: { fontSize: 14, color: BLUE_TEXT, fontFace: FONT, underline: true } },
], {
  x: RED_BOX_X + 0.15, y: RED_BOX_Y + 0.05, w: RED_BOX_W - 0.3, h: RED_BOX_H - 0.1,
  align: "left", valign: "middle", margin: 0, lineSpacing: 16.8,
});

// ============================================================
// PEACH "REMEMBER" BOX — middle-right
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: PEACH_BOX_X, y: RED_BOX_Y, w: PEACH_BOX_W, h: RED_BOX_H,
  fill: { color: PEACH_FILL },
  // no border line
});

s.addText([
  { text: "Remember", options: { fontSize: 14, bold: true, color: RED_TEXT, fontFace: FONT, caps: true, breakLine: true } },
  { text: "∂W^T W/∂W = 2W", options: { fontSize: 16, color: DARK_BLUE, fontFace: MATH_FONT } },
], {
  x: PEACH_BOX_X + 0.1, y: RED_BOX_Y + 0.08, w: PEACH_BOX_W - 0.2, h: RED_BOX_H - 0.16,
  align: "center", valign: "middle", margin: 0, lineSpacing: 16.8,
});

// ============================================================
// DERIVATIVE STEPS — two lines, centered
// ============================================================
const derivLines = [
  "∂J(W)/∂W = 0 = ½[(XW)^T(X) + (X)^T(XW) − 2(X)^T Y]+λ W",
  "∂J(W)/∂W = 0 = ½[2X^T X W − 2 X^T Y]+λ I W",
];

s.addText(derivLines.map((t, i) => ({
  text: t,
  options: { fontSize: 15, color: DARK_BLUE, fontFace: MATH_FONT, breakLine: i < derivLines.length - 1 },
})), {
  x: 1.1, y: DERIV_Y, w: W - 2.2, h: DERIV_H,
  align: "center", valign: "middle", margin: 0, lineSpacing: 18,
});

// ============================================================
// NORMAL EQUATION LINE + ARROW
// ============================================================
s.addText([
  { text: "(X^T X + λ I)W = X^T Y", options: { fontSize: 18, color: DARK_BLUE, fontFace: MATH_FONT, bold: true } },
], {
  x: 2.5, y: NORMALEQ_Y, w: W - 5.0, h: 0.5,
  align: "center", valign: "middle", margin: 0,
});

// Right-pointing arrow (dark blue) pointing to green box
// Arrow from x≈9.0 to x≈10.5 at same vertical center
s.addShape(pptx.ShapeType.rightArrow, {
  x: 9.0, y: NORMALEQ_Y + 0.05, w: 1.5, h: 0.4,
  fill: { color: DARK_BLUE },
  line: { color: DARK_BLUE, width: 1 },
});

// ============================================================
// GREEN SOLUTION BOX — bottom-center
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: GREEN_BOX_X, y: GREEN_BOX_Y, w: GREEN_BOX_W, h: GREEN_BOX_H,
  fill: { color: GREEN_FILL },
  line: { color: GREEN_BORDER, width: 1.5 },
});

s.addText([
  { text: "W = (X^T X + λ I)^(-1) X^T Y", options: { fontSize: 18, color: DARK_BLUE, fontFace: MATH_FONT, underline: true } },
], {
  x: GREEN_BOX_X + 0.2, y: GREEN_BOX_Y + 0.02, w: GREEN_BOX_W - 0.4, h: GREEN_BOX_H - 0.04,
  align: "center", valign: "middle", margin: 0,
});

// ============================================================
// WRITE
// ============================================================
const outPath = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_015_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done:", outPath));