// slide_026.js — Quadratic Kernel Mapping with numeric example
// Vision: Purple header "Quadratic Kernel Mapping and Kernel Trick" + badge 26, three formula bands
// Top: vector defs + (aᵀb)² expansion; Middle: feature-map derivation φ(a)ᵀφ(b), "2D → 3D"; Bottom: numeric example a=[1,2], b=[3,4]
// Run: NODE_PATH=$(npm root -g) node slide_026.js

const pptxgen = require("pptxgenjs");

const NUM = 26;
const TITLE = "Quadratic Kernel Mapping and Kernel Trick";
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

// 2. Slide-number badge (yellow circle per vision)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Purple header strip (per vision)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: 0.6,
  fill: { color: "6A00A0" }, line: { color: "6A00A0", width: 0 },
});
s.addText(TITLE, {
  x: 0.6, y: 0.18, w: 11.0, h: 0.55,
  align: "left", valign: "middle",
  fontSize: 24, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// 4. Top formula band - light cream panel with vector definitions
const bandY1 = 0.9, bandH1 = 1.5, bandX = 1.0, bandW = 11.33;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX, y: bandY1, w: bandW, h: bandH1,
  fill: { color: "FFFDD0" }, line: { color: "333333", width: 0.5 },
});
s.addText("a = [a₁, a₂]ᵀ     b = [b₁, b₂]ᵀ", {
  x: bandX + 0.2, y: bandY1 + 0.1, w: bandW, h: 0.3,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("(aᵀb)² = (a₁b₁ + a₂b₂)² = a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂²", {
  x: bandX + 0.2, y: bandY1 + 0.5, w: bandW, h: 0.3,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("□ (aᵀb)² = a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂²  (boxed per vision)", {
  x: bandX + 0.2, y: bandY1 + 0.9, w: bandW, h: 0.3,
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 5. Middle formula band - feature-map derivation
const bandY2 = bandY1 + bandH1 + 0.3, bandH2 = 2.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX, y: bandY2, w: bandW, h: bandH2,
  fill: { color: "FFFDD0" }, line: { color: "333333", width: 0.5 },
});
s.addText("φ(a)ᵀφ(b) = [a₁², √2 a₁a₂, a₂²] · [b₁², √2 b₁b₂, b₂²]", {
  x: bandX + 0.2, y: bandY2 + 0.1, w: bandW, h: 0.3,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("= a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂²", {
  x: bandX + 0.2, y: bandY2 + 0.5, w: bandW, h: 0.3,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("φ(x) = [x₁², √2 x₁x₂, x₂²]ᵀ", {
  x: bandX + 0.2, y: bandY2 + 1.0, w: bandW, h: 0.3,
  fontSize: 16, color: "006600", fontFace: FONT, margin: 0,
});

// Red "2D → 3D" annotation
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: bandX + bandW - 2.0, y: bandY2 + bandH2 - 0.6, w: 1.8, h: 0.5,
  fill: { color: "FFF0F0" }, line: { color: "C00000", width: 1 },
});
s.addText("2D → 3D", {
  x: bandX + bandW - 2.0, y: bandY2 + bandH2 - 0.6, w: 1.8, h: 0.5,
  align: "center", valign: "middle", fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Right annotation edge - red callout arrows (simplified as text markers)
s.addText("→ φ(a)ᵀφ(b)", {
  x: bandX + bandW + 0.2, y: bandY2 + 0.1, w: 2.0, h: 0.3,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("→ φ(x) definition", {
  x: bandX + bandW + 0.2, y: bandY2 + 1.0, w: 2.0, h: 0.3,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 6. Bottom formula band - numeric instantiation
const bandY3 = bandY2 + bandH2 + 0.3, bandH3 = 2.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: bandX, y: bandY3, w: bandW, h: bandH3,
  fill: { color: "FFFDD0" }, line: { color: "333333", width: 0.5 },
});
s.addText("a = [1, 2]ᵀ     b = [3, 4]ᵀ", {
  x: bandX + 0.2, y: bandY3 + 0.1, w: bandW, h: 0.3,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("(aᵀb)² = (1·3 + 2·4)² = (3 + 8)² = 11² = 121", {
  x: bandX + 0.2, y: bandY3 + 0.5, w: bandW, h: 0.3,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("φ(a)ᵀφ(b) = 1²·3² + 2·1·2·3·4 + 2²·4² = 9 + 48 + 64 = 121", {
  x: bandX + 0.2, y: bandY3 + 0.9, w: bandW, h: 0.3,
  fontSize: 16, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("9 + 64 + 48 = 121", {
  x: bandX + 0.2, y: bandY3 + 1.3, w: bandW, h: 0.3,
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("[aᵀb]² = (1·3 + 2·4)² = 11² = 121", {
  x: bandX + 0.2, y: bandY3 + 1.7, w: bandW, h: 0.3,
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Red arrow and return glyph note (omitted return glyph per defect)

// Note: Bottom black strip from original is treated as capture chrome and omitted

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_026_recreated.pptx" })
  .then(() => console.log("wrote slide_026_recreated.pptx"))
  .catch(err => console.error(err));