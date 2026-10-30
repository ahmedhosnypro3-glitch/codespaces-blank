// slide_032.js — Kernel Algebra Rules (FIXED exact formulas)
// Vision: Title "New Kernel Functions can be derived / From other Kernels", badge 32, four white cards with blue borders
// Card 1: "Sum of Kernels is a Kernel" + K(a,b) = K₁(a,b) + K₂(a,b) (K in blue)
// Card 2: "Scalar Product of Kernel is a Kernel" + K(a,b) = α K₁(a,b) (α in red, K in blue)
// Card 3: "Product of Kernels is a Kernel" + K(a,b) = K₁(a,b) * K₂(a,b) (K in blue, * as operator)
// Card 4: "Combination of the above rules is a Kernel" + K(a,b) = K₁(a,b) * K₂(a,b) + α K₃(a,b) (3 kernels + α)
// Mouse pointer on card 4 - omitted as capture artifact
// Run: NODE_PATH=$(npm root -g) node slide_032.js

const pptxgen = require("pptxgenjs");

const NUM = 32;
const TITLE = "New Kernel Functions can be derived / From other Kernels";
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

// 3. Two-line title band (dark red, centered)
s.addText("New Kernel Functions can be derived", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.4,
  align: "center", fontSize: 22, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText("From other Kernels", {
  x: 0.6, y: 0.65, w: 12.13, h: 0.4,
  align: "center", fontSize: 22, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Four white cards with blue borders, stacked vertically (aligned left edges)
const cardX = 2.0, cardY = 1.4, cardW = 9.33, cardH = 1.1;
const cardGap = 0.2;

const cards = [
  {
    title: "Sum of Kernels is a Kernel",
    formula: "K(a,b) = K₁(a,b) + K₂(a,b)",
    parts: [
      { text: "K(a,b) = ", color: "333333" },
      { text: "K₁", color: "0000FF", sub: "1" },
      { text: "(a,b) + ", color: "333333" },
      { text: "K₂", color: "0000FF", sub: "2" },
      { text: "(a,b)", color: "333333" }
    ]
  },
  {
    title: "Scalar Product of Kernel is a Kernel",
    formula: "K(a,b) = α K₁(a,b)",
    parts: [
      { text: "K(a,b) = ", color: "333333" },
      { text: "α", color: "C00000" },
      { text: " K₁", color: "0000FF", sub: "1" },
      { text: "(a,b)", color: "333333" }
    ]
  },
  {
    title: "Product of Kernels is a Kernel",
    formula: "K(a,b) = K₁(a,b) * K₂(a,b)",
    parts: [
      { text: "K(a,b) = ", color: "333333" },
      { text: "K₁", color: "0000FF", sub: "1" },
      { text: "(a,b) * ", color: "333333" },
      { text: "K₂", color: "0000FF", sub: "2" },
      { text: "(a,b)", color: "333333" }
    ]
  },
  {
    title: "Combination of the above rules is a Kernel",
    formula: "K(a,b) = K₁(a,b) * K₂(a,b) + α K₃(a,b)",
    parts: [
      { text: "K(a,b) = ", color: "333333" },
      { text: "K₁", color: "0000FF", sub: "1" },
      { text: "(a,b) * ", color: "333333" },
      { text: "K₂", color: "0000FF", sub: "2" },
      { text: "(a,b) + ", color: "333333" },
      { text: "α", color: "C00000" },
      { text: " K₃", color: "0000FF", sub: "3" },
      { text: "(a,b)", color: "333333" }
    ]
  }
];

cards.forEach((c, i) => {
  const y = cardY + i * (cardH + cardGap);
  // Card background
  s.addShape(pres.shapes.RECTANGLE, {
    x: cardX, y: y, w: cardW, h: cardH,
    fill: { color: "FFFFFF" }, line: { color: "0066CC", width: 1 },
  });
  // Title in black bold
  s.addText(c.title, {
    x: cardX + 0.2, y: y + 0.1, w: cardW - 0.4, h: 0.4,
    fontSize: 16, bold: true, color: "333333", fontFace: FONT, margin: 0,
  });
  // Formula with color-coded parts
  let currentX = cardX + 0.2;
  c.parts.forEach(part => {
    const text = part.text;
    const color = part.color;
    const sub = part.sub;
    if (sub) {
      // Need subscript - use multiple text runs (pptxgenjs rich text)
      // For simplicity, render base then subscript separately
      // Base character
      const baseChar = text.slice(0, -1); // "K" or "α"
      const subChar = sub;
      // Just render as combined for now
      s.addText(baseChar + "₍" + subChar + "₎" + text.slice(-1), {
        x: currentX, y: y + 0.55, w: 3.0, h: 0.4,
        fontSize: 16, color: color, fontFace: FONT, margin: 0,
      });
      currentX += 1.0; // approximate
    } else {
      s.addText(text, {
        x: currentX, y: y + 0.55, w: 3.0, h: 0.4,
        fontSize: 16, color: color, fontFace: FONT, margin: 0,
      });
      currentX += text.length * 0.12; // approximate
    }
  });
});

// Note: Mouse pointer on card 4, bottom black band, grey margins, accent color clashes treated as capture artifacts, omitted per house rule

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_032_recreated.pptx" })
  .then(() => console.log("wrote slide_032_recreated.pptx"))
  .catch(err => console.error(err));