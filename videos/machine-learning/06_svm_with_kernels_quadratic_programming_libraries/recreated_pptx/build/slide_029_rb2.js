// slide_029.js — RBF Kernel Taylor series derivation (FIXED with numerical data)
// Vision: Dark app frame, light slide card, title "Radial Basis Function (RBF) Kernel", badge 29
// Left: three blue-bordered equation boxes (derivation)
// Right: red-bordered Taylor series expansion panel with numerical approximation list
// Doc-parse numerical data: e³ approximations: 13, 16.375, 18.4, 19.413, 19.84, 19.8420.01, Actual 20.086
// Run: NODE_PATH=$(npm root -g) node slide_029.js

const pptxgen = require("pptxgenjs");

const NUM = 29;
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

// 4. Main content card (light rounded rect)
const cardX = 1.0, cardY = 1.0, cardW = 11.33, cardH = 5.8;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: cardX, y: cardY, w: cardW, h: cardH,
  fill: { color: "FFFFFF" }, line: { color: "CCCCCC", width: 1 },
});

// 5. Title inside card (top-left per vision)
s.addText(TITLE, {
  x: cardX + 0.3, y: cardY + 0.2, w: 6.0, h: 0.4,
  fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 6. Left derivation pane - three stacked blue-bordered boxes
const leftX = cardX + 0.3, leftY = cardY + 0.8, leftW = 5.5, leftH = 4.5;
const boxH = 1.2;
const boxGap = 0.2;

for (let i = 0; i < 3; i++) {
  const boxY = leftY + i * (boxH + boxGap);
  s.addShape(pres.shapes.RECTANGLE, {
    x: leftX, y: boxY, w: leftW, h: boxH,
    fill: { color: "F8F8FF" }, line: { color: "0066CC", width: 1.5 },
  });
}

s.addText("e⁻¹ᐟ²||a−b||² = e⁻¹ᐟ²(aᵀa + bᵀb − 2aᵀb) = e⁻ᵃ²ᐟ² e⁻ᵇ²ᐟ² eᵃᵀᵇ", {
  x: leftX + 0.2, y: leftY + 0.1, w: leftW - 0.4, h: boxH - 0.2,
  fontSize: 14, color: "333333", fontFace: FONT, margin: 0,
});

s.addText("eᵃᵀᵇ = 1 + aᵀᵇ/1! + (aᵀᵇ)²/2! + (aᵀᵇ)³/3! + (aᵀᵇ)⁴/4! + ...", {
  x: leftX + 0.2, y: leftY + boxH + boxGap + 0.1, w: leftW - 0.4, h: boxH - 0.2,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});

s.addText("φ(a)ᵀ = e⁻ᵃ²ᐟ² [1, a₁/√1!, a₂/√1!, a₁²/√2!, a₁a₂/√2!, a₂²/√2!, ...]", {
  x: leftX + 0.2, y: leftY + 2*(boxH + boxGap) + 0.1, w: leftW - 0.4, h: boxH - 0.2,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("φ(b)  = e⁻ᵇ²ᐟ² [1, b₁/√1!, b₂/√1!, b₁²/√2!, b₁b₂/√2!, b₂²/√2!, ...]ᵀ", {
  x: leftX + 0.2, y: leftY + 2*(boxH + boxGap) + 0.5, w: leftW - 0.4, h: boxH - 0.2,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});

// 7. Right expansion pane - red-bordered Taylor series WITH NUMERICAL DATA
const rightX = cardX + cardW - 5.8, rightY = cardY + 0.8, rightW = 5.3, rightH = 4.5;
s.addShape(pres.shapes.RECTANGLE, {
  x: rightX, y: rightY, w: rightW, h: rightH,
  fill: { color: "FFF8F8" }, line: { color: "C00000", width: 1.5 },
});
s.addText("Taylor series expansion of eˣ", {
  x: rightX + 0.2, y: rightY + 0.1, w: rightW - 0.4, h: 0.4,
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("eˣ = 1 + x/1! + x²/2! + x³/3! + x⁴/4! + x⁵/5! + ...", {
  x: rightX + 0.2, y: rightY + 0.5, w: rightW - 0.4, h: 0.3,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("e³ = 1 + 3/1! + 3²/2! + 3³/3! + 3⁴/4! + 3⁵/5! + ...", {
  x: rightX + 0.2, y: rightY + 0.85, w: rightW - 0.4, h: 0.3,
  fontSize: 13, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Approximations:", {
  x: rightX + 0.2, y: rightY + 1.3, w: rightW - 0.4, h: 0.3,
  fontSize: 13, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Numerical approximations from doc-parse (matching original exactly)
const approximations = [
  "Approx. to 4 terms ⇒ 13",
  "Approx. to 5 terms ⇒ 16.375",
  "Approx. to 6 terms ⇒ 18.4",
  "Approx. to 7 terms ⇒ 19.413",
  "Approx. to 8 terms ⇒ 19.84",
  "Approx. to 9 terms ⇒ 19.8420...",
  "Actual Value ⇒ 20.086"
];

approximations.forEach((approx, i) => {
  const y = rightY + 1.65 + i * 0.32;
  const isActual = i === approximations.length - 1;
  s.addText(approx, {
    x: rightX + 0.2, y: y, w: rightW - 0.4, h: 0.28,
    fontSize: 12, bold: isActual, color: isActual ? "008000" : "333333", fontFace: FONT, margin: 0,
  });
});

// Note: Hand-drawn annotations (pink pills, squiggle) and bottom black strip treated as capture artifacts, omitted per house rule

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_029_recreated.pptx" })
  .then(() => console.log("wrote slide_029_recreated.pptx"))
  .catch(err => console.error(err));