// slide_027.js — Polynomial Kernel (with dark app frame)
// Vision: Dark app frame, light gray header "Polynomial Kernel" + badge 27, white body with blue border
// Math: vectors a,b with red/blue components, "Remember: (aᵀb)² = ...", expansion (aᵀb + 1)², feature mapping φ(a)ᵀφ(b) with 6D column vector, "2D ⇒ 6D"
// Run: NODE_PATH=$(npm root -g) node slide_027.js

const pptxgen = require("pptxgenjs");

const NUM = 27;
const TITLE = "Polynomial Kernel";
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

// 4. Light gray header bar (from vision)
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.0, y: 1.0, w: 11.33, h: 0.5,
  fill: { color: "D0D0D0" }, line: { color: "999999", width: 0.5 },
});
s.addText("Polynomial Kernel", {
  x: 1.0, y: 1.0, w: 11.33, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 5. Main white body with blue border
const bodyX = 1.0, bodyY = 1.7, bodyW = 11.33, bodyH = 5.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: bodyX, y: bodyY, w: bodyW, h: bodyH,
  fill: { color: "FFFFFF" }, line: { color: "0066CC", width: 2 },
});

// 6. Top-left math block - vectors a (red) and b (blue)
s.addText("Vectors:", {
  x: bodyX + 0.3, y: bodyY + 0.2, w: bodyW, h: 0.3,
  fontSize: 14, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a = [a₁, a₂]ᵀ", {
  x: bodyX + 0.3, y: bodyY + 0.5, w: 3.0, h: 0.3,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("b = [b₁, b₂]ᵀ", {
  x: bodyX + 3.5, y: bodyY + 0.5, w: 3.0, h: 0.3,
  fontSize: 14, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// 7. Top-right "Remember:" callout
const rememberX = bodyX + bodyW - 4.5, rememberY = bodyY + 0.2, rememberW = 4.0, rememberH = 0.8;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: rememberX, y: rememberY, w: rememberW, h: rememberH,
  fill: { color: "F0F0F0" }, line: { color: "999999", width: 1 },
});
s.addText("Remember:", {
  x: rememberX + 0.1, y: rememberY + 0.05, w: rememberW - 0.2, h: 0.3,
  fontSize: 12, bold: true, color: "666666", fontFace: FONT, margin: 0,
});
s.addText("(aᵀb)² = a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂²", {
  x: rememberX + 0.1, y: rememberY + 0.35, w: rememberW - 0.2, h: 0.3,
  fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});

// 8. Middle expansion block - (aᵀb + 1)² spanning full width
s.addText("(aᵀb + 1)² = (aᵀb)² + 2(aᵀb) + 1", {
  x: bodyX + 0.3, y: bodyY + 1.2, w: bodyW - 0.6, h: 0.4,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("= a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂² + 2(a₁b₁ + a₂b₂) + 1", {
  x: bodyX + 0.3, y: bodyY + 1.6, w: bodyW - 0.6, h: 0.4,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});

// 9. Bottom feature-mapping block
s.addText("φ(a)ᵀφ(b) = [a₁², √2 a₁a₂, a₂², √2 a₁, √2 a₂, 1] · [b₁², √2 b₁b₂, b₂², √2 b₁, √2 b₂, 1]", {
  x: bodyX + 0.3, y: bodyY + 2.3, w: bodyW - 0.6, h: 0.4,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Where: φ(x) = [x₁², √2 x₁x₂, x₂², √2 x₁, √2 x₂, 1]ᵀ", {
  x: bodyX + 0.3, y: bodyY + 2.8, w: bodyW - 0.6, h: 0.4,
  fontSize: 14, color: "006600", fontFace: FONT, margin: 0,
});

// 10. Right column vector (6D) - tall column
const vecX = bodyX + bodyW - 3.0, vecY = bodyY + 3.3, vecW = 2.5, vecH = 3.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: vecX, y: vecY, w: vecW, h: vecH,
  fill: { color: "F8F8F8" }, line: { color: "999999", width: 1 },
});
s.addText("φ(x) =", {
  x: vecX, y: vecY + 0.1, w: vecW, h: 0.3,
  align: "center", fontSize: 12, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("x₁²\n√2 x₁x₂\nx₂²\n√2 x₁\n√2 x₂\n1", {
  x: vecX, y: vecY + 0.4, w: vecW, h: vecH - 0.5,
  align: "center", fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});

// 11. "2D ⇒ 6D" red at bottom-right corner
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: bodyX + bodyW - 2.0, y: bodyY + bodyH - 0.6, w: 1.8, h: 0.4,
  fill: { color: "FFF0F0" }, line: { color: "C00000", width: 1 },
});
s.addText("2D ⇒ 6D", {
  x: bodyX + bodyW - 2.0, y: bodyY + bodyH - 0.6, w: 1.8, h: 0.4,
  align: "center", valign: "middle", fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Note: Dark app frame and bottom black strip from original treated as capture chrome, omitted per house rule

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_027_recreated.pptx" })
  .then(() => console.log("wrote slide_027_recreated.pptx"))
  .catch(err => console.error(err));