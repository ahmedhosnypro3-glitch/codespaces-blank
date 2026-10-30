// slide_025.js — Quadratic Kernel Mapping and Kernel Trick
// Vision: Title "Quadratic Kernel Mapping and Kernel Trick", gold badge 25, beige panel with blue border, vector defs, feature map φ(x), "2D ⇒ 3D"
// Run: NODE_PATH=$(npm root -g) node slide_025.js

const pptxgen = require("pptxgenjs");

const NUM = 25;
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

// 2. Slide-number badge (gold circle per vision)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFD700" }, line: { color: "FFD700", width: 0.5 },
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

// 4. Main content panel (light beige fill, dark red/purple border)
const panelX = 1.0, panelY = 1.2, panelW = 11.33, panelH = 5.5;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: panelX, y: panelY, w: panelW, h: panelH,
  fill: { color: "FFF8E0" }, line: { color: "8B0040", width: 2 },
});

// 5. Left equation block - vector definitions and dot-product expansion
// Vision: "vector definitions (a, b) and dot-product expansion at top-left inside the panel"
const leftX = panelX + 0.3, leftY = panelY + 0.3, leftW = 5.5, leftH = 4.5;
s.addText("Vectors:", {
  x: leftX, y: leftY, w: leftW, h: 0.3,
  fontSize: 14, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a = [a₁, a₂]ᵀ", {
  x: leftX, y: leftY + 0.35, w: leftW, h: 0.3,
  fontSize: 14, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("b = [b₁, b₂]ᵀ", {
  x: leftX, y: leftY + 0.65, w: leftW, h: 0.3,
  fontSize: 14, color: "0000FF", fontFace: FONT, margin: 0,
});
s.addText("(aᵀb)² = a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂²", {
  x: leftX, y: leftY + 1.1, w: leftW, h: 0.4,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("= (a₁b₁)² + 2(a₁b₁)(a₂b₂) + (a₂b₂)²", {
  x: leftX, y: leftY + 1.5, w: leftW, h: 0.4,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});

// 6. Right definition block - feature map φ(x)
const rightX = panelX + 6.5, rightY = panelY + 0.5, rightW = 4.5, rightH = 4.0;
s.addText("Where: φ(x) ↦", {
  x: rightX, y: rightY, w: rightW, h: 0.3,
  fontSize: 14, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("φ(x) = [x₁², √2 x₁x₂, x₂²]ᵀ", {
  x: rightX, y: rightY + 0.4, w: rightW, h: 0.4,
  fontSize: 14, color: "006600", fontFace: FONT, margin: 0,
});
s.addText("φ(a)ᵀφ(b) = a₁²b₁² + 2a₁a₂b₁b₂ + a₂²b₂²", {
  x: rightX, y: rightY + 1.0, w: rightW, h: 0.4,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("= (aᵀb)²", {
  x: rightX, y: rightY + 1.5, w: rightW, h: 0.4,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 7. "2D ⇒ 3D" red annotation at bottom-right inside panel
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: panelX + panelW - 2.0, y: panelY + panelH - 0.8, w: 1.8, h: 0.5,
  fill: { color: "FFF0F0" }, line: { color: "C00000", width: 1 },
});
s.addText("2D ⇒ 3D", {
  x: panelX + panelW - 2.0, y: panelY + panelH - 0.8, w: 1.8, h: 0.5,
  align: "center", valign: "middle", fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Note: Bottom black strip from original is treated as capture chrome and omitted

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_025_recreated.pptx" })
  .then(() => console.log("wrote slide_025_recreated.pptx"))
  .catch(err => console.error(err));