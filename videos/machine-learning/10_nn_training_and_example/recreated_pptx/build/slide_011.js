// slide_011.js — Build "Updated Weights of Output Layer" slide for 10_nn_training_and_example
// Run: NODE_PATH=$(npm root -g) node slide_011.js

const pptxgen = require("pptxgenjs");

const W = 13.33, H = 7.5;
const FONT = "Arial";

// Equation metadata (from render_eq.py output)
const EQS = {
  eq1: {w_in: 3.01, h_in: 0.34333, baseline_frac: 0.64078},
  eq2: {w_in: 3.23333, h_in: 0.305, baseline_frac: 0.59563},
  eq3: {w_in: 7.84167, h_in: 0.23333, baseline_frac: 0.7},
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "FDF5E6" };  // cream background per analysis

// ============ HOUSE CHROME ============
// 1. Outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge (yellow/gold oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFD700" }, line: { color: "FFD700", width: 0.5 },
});
s.addText("11", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// 3. Title box (house position)
s.addText("Updated Weights of Output Layer", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Subtitle
s.addText("( Calculated Error is affected by Netj,)", {
  x: 0.6, y: 0.75, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 16, color: "0000FF", fontFace: FONT, margin: 0,
});

// ============ SLIDE CONTENT ============
const RED = "C00000";
const BLACK = "000000";
const BLUE = "0000FF";
const LIGHT_GREEN = "90EE90";
const PURPLE = "DDA0DD";
const DARK_RED = "8B0000";
const GREEN = "00FF00";
const GOLD = "FFD700";

function addEq(name, x, y) {
  const eq = EQS[name];
  s.addImage({ path: `./eq_slide_011/${name}.png`, x, y, w: eq.w_in, h: eq.h_in });
}

// ---- 1. Input Sample box (top-left) ----
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.5, w: 2.5, h: 0.7,
  fill: { color: PURPLE }, line: { color: PURPLE, width: 1 },
});
s.addText("Input Sample", {
  x: 0.5, y: 1.5, w: 2.5, h: 0.7,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// ---- 2. Target Label box (top-right) ----
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 10.3, y: 1.5, w: 2.5, h: 0.7,
  fill: { color: PURPLE }, line: { color: PURPLE, width: 1 },
});
s.addText("Target Label", {
  x: 10.3, y: 1.5, w: 2.5, h: 0.7,
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// ---- 3. Neural Network Diagram (center) ----
// This is the most complex part - building a layered neural network diagram
const diagX = 2.0, diagY = 2.5, diagW = 9.5, diagH = 3.5;

// Layer 1: Input nodes (white dots)
for (let i = 0; i < 4; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 0.5, y: diagY + 0.3 + i * 0.65, w: 0.2, h: 0.2,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
}

// Layer 2: First Sigma layer (white circles with sigma)
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 1.8, y: diagY + 0.5 + i * 0.8, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  s.addText("Σ", {
    x: diagX + 1.8, y: diagY + 0.5 + i * 0.8, w: 0.4, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
  s.addText("f()", {
    x: diagX + 2.3, y: diagY + 0.5 + i * 0.8, w: 0.3, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Layer 3: Second Sigma layer (blue)
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 3.5, y: diagY + 0.5 + i * 0.8, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 },
  });
  s.addText("Σ", {
    x: diagX + 3.5, y: diagY + 0.5 + i * 0.8, w: 0.4, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: BLUE, fontFace: FONT, margin: 0,
  });
  s.addText("Netj\nOj", {
    x: diagX + 3.5, y: diagY + 0.5 + i * 0.8, w: 0.8, h: 0.5,
    align: "left", valign: "middle",
    fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Layer 4: Third Sigma layer (green)
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 5.2, y: diagY + 0.5 + i * 0.8, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: GREEN, width: 1.5 },
  });
  s.addText("Σ", {
    x: diagX + 5.2, y: diagY + 0.5 + i * 0.8, w: 0.4, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: GREEN, fontFace: FONT, margin: 0,
  });
  s.addText("Netj\nOj", {
    x: diagX + 5.2, y: diagY + 0.5 + i * 0.8, w: 0.8, h: 0.5,
    align: "left", valign: "middle",
    fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Output layer
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 7.0, y: diagY + 0.5 + i * 0.8, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  s.addText(`Output ${i+1}`, {
    x: diagX + 7.5, y: diagY + 0.5 + i * 0.8, w: 0.7, h: 0.4,
    align: "left", valign: "middle",
    fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Weight labels on arrows (simplified)
s.addText("wji", {
  x: diagX + 1.2, y: diagY + 0.3, w: 0.5, h: 0.2,
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("wjj", {
  x: diagX + 2.9, y: diagY + 0.3, w: 0.5, h: 0.2,
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// Partial derivative labels (red)
s.addText("∂E/∂wji", {
  x: diagX + 4.2, y: diagY + 0.1, w: 0.6, h: 0.2,
  fontSize: 9, color: RED, fontFace: FONT, margin: 0,
});
s.addText("∂E/∂Netj = -δj", {
  x: diagX + 4.2, y: diagY + 2.5, w: 0.8, h: 0.3,
  fontSize: 9, color: RED, fontFace: FONT, margin: 0,
});

// Red highlighted output node
s.addShape(pres.shapes.OVAL, {
  x: diagX + 7.0, y: diagY + 0.5, w: 0.4, h: 0.4,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 3 },
});

// Circled "1" icons
s.addShape(pres.shapes.OVAL, {
  x: diagX + 0.3, y: diagY + 2.5, w: 0.2, h: 0.2,
  fill: { color: PURPLE }, line: { color: PURPLE, width: 1 },
});
s.addText("1", {
  x: diagX + 0.3, y: diagY + 2.5, w: 0.2, h: 0.2,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("Node Bias", {
  x: diagX - 0.5, y: diagY + 2.5, w: 0.6, h: 0.2,
  align: "right", valign: "middle",
  fontSize: 8, color: PURPLE, fontFace: FONT, margin: 0,
});

s.addShape(pres.shapes.OVAL, {
  x: diagX + 3.0, y: diagY + 2.9, w: 0.2, h: 0.2,
  fill: { color: PURPLE }, line: { color: PURPLE, width: 1 },
});
s.addText("1", {
  x: diagX + 3.0, y: diagY + 2.9, w: 0.2, h: 0.2,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Green upward arrows with circled numbers
for (let i = 0; i < 2; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 5.5, y: diagY + 1.0 + i * 1.0, w: 0.2, h: 0.2,
    fill: { color: "FFFFFF" }, line: { color: GREEN, width: 1 },
  });
  s.addText("1", {
    x: diagX + 5.5, y: diagY + 1.0 + i * 1.0, w: 0.2, h: 0.2,
    align: "center", valign: "middle",
    fontSize: 9, bold: true, color: GREEN, fontFace: FONT, margin: 0,
  });
}

// ---- 4. Error Error bar (far right) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 12.0, y: diagY + 0.3, w: 0.6, h: 2.0,
  fill: { color: DARK_RED }, line: { color: DARK_RED, width: 1 },
});
s.addText("Error\nError", {
  x: 12.0, y: diagY + 0.3, w: 0.6, h: 2.0,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Class boxes
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 12.7, y: diagY + 0.3 + i * 0.65, w: 0.6, h: 0.5,
    fill: { color: LIGHT_GREEN }, line: { color: BLACK, width: 1 },
  });
  s.addText(`Class ${i+1}`, {
    x: 12.7, y: diagY + 0.3 + i * 0.65, w: 0.6, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ---- 5. Equation row at bottom of diagram ----
const yEqRow = diagY + diagH + 0.2;

addEq("eq1", 1.0, yEqRow);

s.addText("Where δj = -∂E/∂Netj (one δ for each Node j)", {
  x: 4.5, y: yEqRow, w: 4.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});

// ---- 6. Bottom strip with sigmoid activation ----
const yBottom = 6.5;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.3, y: yBottom, w: W - 0.6, h: 0.6,
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 2 },
});

addEq("eq3", 0.5, yBottom + 0.15);

// "Sigmoid" in red - we'll add it as text overlay
s.addText("Sigmoid", {
  x: 5.5, y: yBottom + 0.15, w: 1.0, h: 0.2,
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Write file
pres.writeFile({ fileName: "slide_011_recreated.pptx" })
  .then(() => console.log("wrote slide_011_recreated.pptx"))
  .catch(e => console.error(e));