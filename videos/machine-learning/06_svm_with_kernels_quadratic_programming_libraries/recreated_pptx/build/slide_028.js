// slide_028.js — Polynomial Kernel proof (two-panel: theory + numeric)
// Vision: Top panel cream with blue border - general identity [aᵀb+1]² = φ(a)ᵀφ(b) + Where: φ(x)
// Bottom panel white with blue border - numeric proof a=[1,2], b=[3,4], result 144
// Run: NODE_PATH=$(npm root -g) node slide_028.js

const pptxgen = require("pptxgenjs");

const NUM = 28;
const TITLE = "Polynomial Kernel Proof";
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

// 3. Title box
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Top panel - cream with blue border (general identity)
const topX = 1.0, topY = 1.0, topW = 11.33, topH = 2.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: topX, y: topY, w: topW, h: topH,
  fill: { color: "FFFDD0" }, line: { color: "0066CC", width: 1.5 },
});
s.addText("[aᵀb + 1]² = aᵀa bᵀb + 2aᵀb + 1 = φ(a)ᵀφ(b)", {
  x: topX + 0.3, y: topY + 0.2, w: topW - 0.6, h: 0.5,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Where: φ(x) = [x₁², √2 x₁x₂, x₂², √2 x₁, √2 x₂, 1]ᵀ", {
  x: topX + 0.3, y: topY + 0.8, w: topW - 0.6, h: 0.5,
  fontSize: 16, color: "006600", fontFace: FONT, margin: 0,
});
s.addText("φ(x) ∈ ℝ⁶ — 2D input mapped to 6D feature space", {
  x: topX + 0.3, y: topY + 1.4, w: topW - 0.6, h: 0.5,
  fontSize: 14, color: "666666", fontFace: FONT, margin: 0,
});
s.addText("φ(a)ᵀφ(b) = a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂² + 2a₁b₁ + 2a₂b₂ + 1", {
  x: topX + 0.3, y: topY + 2.0, w: topW - 0.6, h: 0.5,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});

// 5. Bottom panel - white with blue border (numeric proof)
const botX = 1.0, botY = topY + topH + 0.3, botW = 11.33, botH = 3.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: botX, y: botY, w: botW, h: botH,
  fill: { color: "FFFFFF" }, line: { color: "0066CC", width: 1.5 },
});
s.addText("Numeric Example: a = [1, 2]ᵀ, b = [3, 4]ᵀ", {
  x: botX + 0.3, y: botY + 0.2, w: botW - 0.6, h: 0.4,
  fontSize: 16, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("aᵀb = 1·3 + 2·4 = 3 + 8 = 11", {
  x: botX + 0.3, y: botY + 0.7, w: botW - 0.6, h: 0.4,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("[aᵀb + 1]² = (11 + 1)² = 12² = 144", {
  x: botX + 0.3, y: botY + 1.1, w: botW - 0.6, h: 0.4,
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("φ(a) = [1, √2·2, 4, √2·1, √2·2, 1]ᵀ = [1, 2√2, 4, √2, 2√2, 1]ᵀ", {
  x: botX + 0.3, y: botY + 1.6, w: botW - 0.6, h: 0.4,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("φ(b) = [9, √2·12, 16, √2·3, √2·4, 1]ᵀ = [9, 12√2, 16, 3√2, 4√2, 1]ᵀ", {
  x: botX + 0.3, y: botY + 2.0, w: botW - 0.6, h: 0.4,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("φ(a)ᵀφ(b) = 1·9 + (2√2)(12√2) + 4·16 + √2·3√2 + (2√2)(4√2) + 1·1 = 9 + 48 + 64 + 6 + 16 + 1 = 144", {
  x: botX + 0.3, y: botY + 2.4, w: botW - 0.6, h: 0.6,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("✓ [aᵀb + 1]² = 144 = φ(a)ᵀφ(b) — Kernel trick verified", {
  x: botX + 0.3, y: botY + botH - 0.5, w: botW - 0.6, h: 0.4,
  fontSize: 16, bold: true, color: "008000", fontFace: FONT, margin: 0,
});

// Note: Bottom black strip from original is treated as capture chrome and omitted

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_028_recreated.pptx" })
  .then(() => console.log("wrote slide_028_recreated.pptx"))
  .catch(err => console.error(err));