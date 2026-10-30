// slide_023.js — RBF Kernel derivation (Example-3)
// Vision: Example-3, RBF Kernel title, Normal Model vs Kernelized Model panes, 2D->infinite mapping
// Run: NODE_PATH=$(npm root -g) node slide_023.js

const pptxgen = require("pptxgenjs");

const NUM = 23;
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

// 3. Title box
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Top-left source card - vector definitions
// Vision: "Top-left source card — small rounded box at upper-left showing column vectors [a₁ b₁; a₂ b₂]"
const srcX = 0.6, srcY = 1.0, srcW = 3.0, srcH = 1.2;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: srcX, y: srcY, w: srcW, h: srcH,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});
s.addText("Input Vectors", {
  x: srcX + 0.1, y: srcY + 0.05, w: srcW - 0.2, h: 0.3,
  align: "center", fontSize: 12, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a = [a₁, a₂]ᵀ    b = [b₁, b₂]ᵀ", {
  x: srcX + 0.1, y: srcY + 0.4, w: srcW - 0.2, h: 0.6,
  align: "center", fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});

// 5. Top-right "Normal Model" pane
// Vision: "Normal Model / Calculate aᵀb", inner vector pair, red exit arrow
const normX = 9.0, normY = 1.0, normW = 3.8, normH = 1.2;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: normX, y: normY, w: normW, h: normH,
  fill: { color: "E0F0FF" }, line: { color: "0066CC", width: 1.5 },
});
s.addText("Normal Model", {
  x: normX + 0.1, y: normY + 0.05, w: normW - 0.2, h: 0.3,
  align: "center", fontSize: 12, bold: true, color: "0066CC", fontFace: FONT, margin: 0,
});
s.addText("Calculate aᵀb", {
  x: normX + 0.1, y: normY + 0.35, w: normW - 0.2, h: 0.25,
  align: "center", fontSize: 11, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("a = [a₁, a₂]ᵀ\nb = [b₁, b₂]ᵀ", {
  x: normX + 0.2, y: normY + 0.6, w: normW - 0.4, h: 0.5,
  align: "center", fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});

// Red exit arrow from Normal Model
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: normX + normW, y: normY + normH/2 - 0.15, w: 0.3, h: 0.3,
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});

// 6. Middle header band: "Map Input data from 2D to infinite Dimension"
s.addText("Map Input data from 2D to infinite Dimension", {
  x: 0.6, y: 2.4, w: 12.13, h: 0.4,
  align: "center", fontSize: 16, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 7. Bottom-left flow cluster - vector box, mapping pill, matrix column
const flowX = 0.6, flowY = 3.0;
const boxW = 3.0, boxH = 0.6;
const pillW = 4.0, pillH = 0.6;
const matW = 3.0, matH = 2.5;

// Left vector box
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: flowX, y: flowY, w: boxW, h: boxH,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});
s.addText("Input: a,b", {
  x: flowX + 0.1, y: flowY + 0.1, w: boxW - 0.2, h: boxH - 0.2,
  align: "center", fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});

// Red hatch arrow 1
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: flowX + boxW, y: flowY + boxH/2 - 0.15, w: 0.4, h: 0.3,
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});

// Vectors Mapping pill (red border)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: flowX + boxW + 0.5, y: flowY, w: pillW, h: pillH,
  fill: { color: "FFF0F0" }, line: { color: "C00000", width: 1.5 },
});
s.addText("Vectors Mapping e⁻ᵞ||a-b||² a,b → u,v", {
  x: flowX + boxW + 0.5 + 0.1, y: flowY + 0.05, w: pillW - 0.2, h: pillH - 0.1,
  align: "center", fontSize: 11, color: "C00000", fontFace: FONT, margin: 0,
});

// Red hatch arrow 2
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: flowX + boxW + 0.5 + pillW, y: flowY + pillH/2 - 0.15, w: 0.4, h: 0.3,
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});

// Tall matrix column [u₁ v₁ … u∞ v∞]
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: flowX + boxW + 0.5 + pillW + 0.5, y: flowY - 1.0, w: matW, h: matH,
  fill: { color: "FFFFFF" }, line: { color: "999999", width: 1 },
});
s.addText("Mapped Vectors", {
  x: flowX + boxW + 0.5 + pillW + 0.5 + 0.1, y: flowY - 1.0 + 0.05, w: matW - 0.2, h: 0.25,
  align: "center", fontSize: 11, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("u₁, v₁\nu₂, v₂\n⋮\nu∞, v∞", {
  x: flowX + boxW + 0.5 + pillW + 0.5 + 0.1, y: flowY - 0.7, w: matW - 0.2, h: matH - 0.3,
  align: "center", fontSize: 12, color: "333333", fontFace: FONT, margin: 0,
});

// Purple "Higher Computational Complexity !!!" chip (bottom-left of flow cluster)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: flowX, y: flowY + boxH + 0.2, w: 4.5, h: 0.4,
  fill: { color: "E0D0FF" }, line: { color: "8000FF", width: 1 },
});
s.addText("Higher Computational Complexity !!!", {
  x: flowX + 0.1, y: flowY + boxH + 0.2, w: 4.5, h: 0.4,
  align: "center", valign: "middle", fontSize: 10, bold: true, color: "8000FF", fontFace: FONT, margin: 0,
});

// 8. Bottom-right "Kernelized Model" pane
const kernX = 9.0, kernY = 3.0, kernW = 3.8, kernH = 3.0;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: kernX, y: kernY, w: kernW, h: kernH,
  fill: { color: "E0FFE0" }, line: { color: "008000", width: 1.5 },
});
s.addText("Kernelized Model", {
  x: kernX + 0.1, y: kernY + 0.05, w: kernW - 0.2, h: 0.3,
  align: "center", fontSize: 12, bold: true, color: "008000", fontFace: FONT, margin: 0,
});
s.addText("Calculate uᵀv", {
  x: kernX + 0.1, y: kernY + 0.35, w: kernW - 0.2, h: 0.25,
  align: "center", fontSize: 11, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("U = [u₁ u₂ u₃ … u∞\n      v₁ v₂ v₃ … v∞]", {
  x: kernX + 0.2, y: kernY + 0.65, w: kernW - 0.4, h: 1.5,
  align: "center", fontSize: 11, color: "333333", fontFace: FONT, margin: 0,
});

// Purple complexity chip inside Kernelized Model (bottom-left)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: kernX + 0.1, y: kernY + kernH - 0.5, w: 3.6, h: 0.4,
  fill: { color: "E0D0FF" }, line: { color: "8000FF", width: 1 },
});
s.addText("Higher Computational Complexity !!!", {
  x: kernX + 0.1, y: kernY + kernH - 0.5, w: 3.6, h: 0.4,
  align: "center", valign: "middle", fontSize: 9, bold: true, color: "8000FF", fontFace: FONT, margin: 0,
});

// Red exit arrow from Kernelized Model
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: kernX + kernW, y: kernY + kernH/2 - 0.15, w: 0.3, h: 0.3,
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});

// 9. RBF formula at top-right (from vision: "right math formula [e⁻ᵞ||a-b||²]")
s.addText("e⁻ᵞ||a−b||²", {
  x: 10.5, y: 0.3, w: 2.0, h: 0.5,
  align: "center", fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// "Example-3" chip at top-left
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 0.3, w: 1.2, h: 0.4,
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});
s.addText("Example-3", {
  x: 0.6, y: 0.3, w: 1.2, h: 0.4,
  align: "center", valign: "middle", fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_023_recreated.pptx" })
  .then(() => console.log("wrote slide_023_recreated.pptx"))
  .catch(err => console.error(err));