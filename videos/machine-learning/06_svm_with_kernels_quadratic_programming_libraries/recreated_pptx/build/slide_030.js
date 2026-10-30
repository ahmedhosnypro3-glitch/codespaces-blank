// slide_030.js — RBF Kernel derivation with Taylor series (FIXED)
// Vision: Maroon title "RBF Kernel", badge 30, left derivation panel (identity, horizontal Taylor series box, φ(a)ᵀ/φ(b) pills, vertical Taylor column, e^(-b²/2) factor), right result panel with blue-boxed e^(-γ||a-b||²)
// Doc-parse: "e^(-1/2(a-b)²) = e^(-a²/2) e^(-b²/2) e^(ab)" + horizontal Taylor: "1, a/√1!, a²/√2!, a³/√3!, a⁴/√4!, ..." + vertical Taylor: "1/b, b/√1!, b²/√2!, b³/√3!, b⁴/√4!, ..., ∞"
// Run: NODE_PATH=$(npm root -g) node slide_030.js

const pptxgen = require("pptxgenjs");

const NUM = 30;
const TITLE = "Radial Basis Function (RBF) Kernel";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House red frame (0.15in inset)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (maroon per vision)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "800000", fontFace: FONT, margin: 0,
});

// 4. Left derivation panel - LARGE to accommodate all content
const leftX = 1.0, leftY = 1.0, leftW = 9.5, leftH = 5.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: leftX, y: leftY, w: leftW, h: leftH,
  fill: { color: "F8F8F8" }, line: { color: "0066CC", width: 1 },
});

// Top: kernel identity with colored terms
s.addText("e⁻¹ᐟ²||a−b||² = e⁻¹ᐟ²(aᵀa + bᵀb − 2aᵀb) = e⁻ᵃ²ᐟ² · e⁻ᵇ²ᐟ² · eᵃᵀᵇ", {
  x: leftX + 0.2, y: leftY + 0.2, w: leftW - 0.4, h: 0.5,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});

// Horizontal Taylor series box (1, a/√1!, a²/√2!, a³/√3!, a⁴/√4!, ...)
const taylorX = leftX + 0.3, taylorY = leftY + 0.8, taylorW = leftW - 0.6, taylorH = 0.7;
s.addShape(pres.shapes.RECTANGLE, {
  x: taylorX, y: taylorY, w: taylorW, h: taylorH,
  fill: { color: "FFFDD0" }, line: { color: "C00000", width: 1 },
});
s.addText("Taylor expansion of eᵃᵀᵇ:", {
  x: taylorX + 0.1, y: taylorY + 0.05, w: taylorW - 0.2, h: 0.25,
  fontSize: 12, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("1  +  aᵀᵇ/√1!  +  (aᵀᵇ)²/√2!  +  (aᵀᵇ)³/√3!  +  (aᵀᵇ)⁴/√4!  +  ...  ∞", {
  x: taylorX + 0.1, y: taylorY + 0.35, w: taylorW - 0.2, h: 0.3,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});

// φ(a)ᵀ and φ(b) pills (rounded)
const pillY = taylorY + taylorH + 0.2;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: leftX + leftW - 3.5, y: pillY, w: 1.6, h: 0.35,
  fill: { color: "E0F0E0" }, line: { color: "008000", width: 1 },
});
s.addText("φ(a)ᵀ = e⁻ᵃ²ᐟ² [1, a₁/√1!, ...]", {
  x: leftX + leftW - 3.5, y: pillY, w: 1.6, h: 0.35,
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "008000", fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: leftX + leftW - 1.8, y: pillY, w: 1.6, h: 0.35,
  fill: { color: "E0E0F0" }, line: { color: "000080", width: 1 },
});
s.addText("φ(b) = e⁻ᵇ²ᐟ² [1, b₁/√1!, ...]ᵀ", {
  x: leftX + leftW - 1.8, y: pillY, w: 1.6, h: 0.35,
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "000080", fontFace: FONT, margin: 0,
});

// Product line
s.addText("φ(a)ᵀφ(b) = e⁻ᵃ²ᐟ² e⁻ᵇ²ᐟ² [1 + aᵀᵇ/√1! + (aᵀᵇ)²/√2! + ...] = e⁻ᵃ²ᐟ² e⁻ᵇ²ᐟ² eᵃᵀᵇ", {
  x: leftX + 0.2, y: pillY + 0.5, w: leftW - 0.4, h: 0.4,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("= e⁻||a−b||²ᐟ²", {
  x: leftX + 0.2, y: pillY + 0.9, w: leftW - 0.4, h: 0.4,
  fontSize: 13, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Vertical Taylor column (1/b, b/√1!, b²/√2!, b³/√3!, b⁴/√4!, ..., ∞)
const vertX = leftX + 0.3, vertY = pillY + 1.4, vertW = 2.0, vertH = 3.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: vertX, y: vertY, w: vertW, h: vertH,
  fill: { color: "FFFFE0" }, line: { color: "999999", width: 0.5 },
});
s.addText("b series:", {
  x: vertX, y: vertY + 0.05, w: vertW, h: 0.25,
  fontSize: 11, bold: true, color: "666666", fontFace: FONT, margin: 0,
});
const bTerms = [
  "1",
  "b/√1!",
  "b²/√2!",
  "b³/√3!",
  "b⁴/√4!",
  "...",
  "∞"
];
bTerms.forEach((term, i) => {
  s.addText(term, {
    x: vertX + 0.1, y: vertY + 0.35 + i * 0.35, w: vertW - 0.2, h: 0.3,
    fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
  });
});

// e^(-b²/2) factor below vertical column
s.addText("e⁻ᵇ²ᐟ²", {
  x: vertX, y: vertY + vertH + 0.1, w: vertW, h: 0.3,
  align: "center", fontSize: 13, color: "000080", fontFace: FONT, margin: 0,
});

// 5. Right result panel - blue boxed final formula (matching original)
const rightX = leftX + leftW + 0.3, rightY = 1.0, rightW = 3.0, rightH = 2.0;
s.addText("RBF Kernel", {
  x: rightX, y: rightY, w: rightW, h: 0.4,
  align: "center", fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: rightX + 0.3, y: rightY + 0.5, w: rightW - 0.6, h: 1.0,
  fill: { color: "E8F4FF" }, line: { color: "0066CC", width: 2 },
});
s.addText("e⁻ᵞ||a−b||²", {
  x: rightX + 0.3, y: rightY + 0.5, w: rightW - 0.6, h: 1.0,
  align: "center", valign: "middle", fontSize: 18, bold: true, color: "0066CC", fontFace: FONT, margin: 0,
});

// Note: Bottom black letterbox bar from original treated as capture chrome, omitted

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_030_recreated.pptx" })
  .then(() => console.log("wrote slide_030_recreated.pptx"))
  .catch(err => console.error(err));