// slide_018.js — Neural Network Model (slide 18)
// Patterns: house-chrome, equations-mathtext-png
// Equation pre-rendered by render_eq.py (eq_s18)

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 18;
const TITLE = "";  // No title on this slide
const SUBTITLE = null;

const BG = "F0F0F0";
const TITLE_COLOR = "000000";
const FRAME_COLOR = "C00000";

const EQ = JSON.parse(fs.readFileSync("eq_s18.json"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// HOUSE CHROME
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME_COLOR, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title box (empty - no title on this slide, but keep position per house chrome)
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: TITLE_COLOR, fontFace: FONT, margin: 0,
});

// Thin black bar at very bottom edge (from original)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 7.35, w: W - 0.3, h: 0.02,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

// NEURAL NETWORK DIAGRAM - simplified reconstruction (measured from original)
const L1_X = 2.5;
const L2_X = 4.5;
const L3_X = 6.5;
const L4_X = 8.5;
const NODE_Y_BASE = 1.5;
const NODE_SPACING = 0.55;

// Layer 1: Input nodes (purple dots)
s.addText("Input Data", {
  x: 0.8, y: NODE_Y_BASE + 1.7, w: 1.2, h: 0.3,
  align: "center", valign: "middle", fontSize: 12, color: "000000", fontFace: FONT, margin: 0,
});
for (let i = 0; i < 4; i++) {
  const y = NODE_Y_BASE + i * NODE_SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: L1_X - 0.15, y: y - 0.15, w: 0.3, h: 0.3,
    fill: { color: "9370DB" }, line: { color: "9370DB", width: 1 },
  });
}

// Layer 2: Hidden layer (green nodes)
for (let i = 0; i < 4; i++) {
  const y = NODE_Y_BASE + i * NODE_SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: L2_X - 0.15, y: y - 0.15, w: 0.3, h: 0.3,
    fill: { color: "90EE90" }, line: { color: "000000", width: 1 },
  });
}

// Layer 3: Hidden layer (yellow/orange nodes)
for (let i = 0; i < 4; i++) {
  const y = NODE_Y_BASE + i * NODE_SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: L3_X - 0.15, y: y - 0.15, w: 0.3, h: 0.3,
    fill: { color: "FFD700" }, line: { color: "000000", width: 1 },
  });
}

// Layer 4: Output nodes
for (let i = 0; i < 3; i++) {
  const y = NODE_Y_BASE + 0.5 + i * NODE_SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: L4_X - 0.15, y: y - 0.15, w: 0.3, h: 0.3,
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
  });
}

// Output labels
s.addText("Output1", { x: L4_X + 0.3, y: NODE_Y_BASE + 0.35, w: 1.0, h: 0.3, align: "left", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Output2", { x: L4_X + 0.3, y: NODE_Y_BASE + 0.9, w: 1.0, h: 0.3, align: "left", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Output3", { x: L4_X + 0.3, y: NODE_Y_BASE + 1.45, w: 1.0, h: 0.3, align: "left", valign: "middle", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });

// ERROR BAR (vertical red, right of diagram)
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.7, y: NODE_Y_BASE - 0.2, w: 0.35, h: 2.4,
  fill: { color: "C00000" }, line: { color: "C00000", width: 1 },
});
s.addText("Error", {
  x: 9.65, y: NODE_Y_BASE - 0.2, w: 0.45, h: 2.4,
  align: "center", valign: "middle", rot: 270,
  fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// CLASS LABELS (to the right of error bar)
s.addText("Class 1", { x: 10.3, y: NODE_Y_BASE - 0.1, w: 1.2, h: 0.5, align: "left", valign: "middle", fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Class 2", { x: 10.3, y: NODE_Y_BASE + 0.6, w: 1.2, h: 0.5, align: "left", valign: "middle", fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Class m", { x: 10.3, y: NODE_Y_BASE + 1.3, w: 1.2, h: 0.5, align: "left", valign: "middle", fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0 });

// EQUATION: ∂E/∂w_ij ? (with red question mark)
const eq_baseline_y = 2.5 + (1 - EQ.baseline_frac) * EQ.h_in;
s.addImage({ path: "eq_s18.png", x: 11.5, y: eq_baseline_y - EQ.baseline_frac * EQ.h_in, w: EQ.w_in, h: EQ.h_in });
s.addText("?", {
  x: 11.5 + EQ.w_in + 0.05, y: 2.45, w: 0.2, h: 0.4,
  align: "left", valign: "middle", fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// NOTE: Mouse cursor in original is a screen-capture artifact — omit per house rule

// ========== WRITE FILE ==========
pres.writeFile({ fileName: "slide_018_recreated.pptx" })
  .then(() => console.log("wrote slide_018_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });