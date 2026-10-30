// slide_011.js — Build "Updated Weights of Output Layer" slide for 10_nn_training_and_example (FIXED v2)
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

// Yellow highlighter block behind the word "Output" in the title.
// Measured on the original frame: highlight band x 7.28-8.41in, median RGB (251,255,26).
// The word "Output" in the 24pt Arial Bold title starts at 4.015 + 9.67em*0.3333 = 7.24in.
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.24, y: 0.33, w: 1.09, h: 0.36,
  fill: { color: "FFFF00" }, line: { type: "none" },
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
const YELLOW = "FFFF00";

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

// Arrow from Target Label to outputs - use LINE shape with arrow
s.addShape(pres.shapes.LINE, {
  x: 11.5, y: 1.85, w: 1.5, h: 1.5,
  line: { color: BLUE, width: 1.5, headEndType: "triangle" },
});

// ---- 3. Neural Network Diagram (center) ----
const diagX = 2.0, diagY = 2.5, diagW = 9.5, diagH = 3.5;

// ---- Connections between layers (drawn first so nodes and labels sit on top) ----
const nodeY = (i) => diagY + 0.75 + i * 0.8;      // center y of the 3-node layers
const dotY = (i) => diagY + 0.4 + i * 0.65;       // center y of the 4 input dots

function connect(ax, ay, bx, by, color) {
  s.addShape(pres.shapes.LINE, {
    x: ax, y: Math.min(ay, by), w: bx - ax, h: Math.abs(by - ay),
    line: { color, width: 0.75 },
    flipV: ay > by,
  });
}

// input dots -> first Sigma layer
for (let i = 0; i < 4; i++) {
  for (let j = 0; j < 3; j++) connect(diagX + 0.7, dotY(i), diagX + 1.8, nodeY(j), BLACK);
}
// first layer (Oi box) -> second Sigma layer
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    connect(diagX + 3.0, diagY + 0.675 + i * 0.8, diagX + 3.8, nodeY(j), BLACK);
  }
}
// second Sigma layer -> third Sigma layer
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) connect(diagX + 4.3, nodeY(i), diagX + 5.5, nodeY(j), BLACK);
}
// third Sigma layer -> output nodes
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) connect(diagX + 6.0, nodeY(i), diagX + 7.2, nodeY(j), BLACK);
}

// Layer 1: Input nodes (white dots)
for (let i = 0; i < 4; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 0.5, y: diagY + 0.3 + i * 0.65, w: 0.2, h: 0.2,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
}

// Layer 2: First Sigma layer (white circles with sigma) + f() boxes
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
  // f() activation boxes
  s.addShape(pres.shapes.RECTANGLE, {
    x: diagX + 2.3, y: diagY + 0.5 + i * 0.8, w: 0.3, h: 0.35,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  s.addText("f()", {
    x: diagX + 2.3, y: diagY + 0.5 + i * 0.8, w: 0.3, h: 0.35,
    align: "center", valign: "middle",
    fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
  });
  // Oi value boxes
  s.addShape(pres.shapes.RECTANGLE, {
    x: diagX + 2.7, y: diagY + 0.5 + i * 0.8, w: 0.3, h: 0.35,
    fill: { color: LIGHT_GREEN }, line: { color: BLACK, width: 1 },
  });
  s.addText(`Oi`, {
    x: diagX + 2.7, y: diagY + 0.5 + i * 0.8, w: 0.3, h: 0.35,
    align: "center", valign: "middle",
    fontSize: 9, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Layer 3: Second Sigma layer (blue) with Netj/Oj labels
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 3.8, y: diagY + 0.5 + i * 0.8, w: 0.5, h: 0.5,
    fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 },
  });
  s.addText("Σ", {
    x: diagX + 3.8, y: diagY + 0.5 + i * 0.8, w: 0.5, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 20, bold: true, color: BLUE, fontFace: FONT, margin: 0,
  });
  s.addText("Netj\nOj", {
    x: diagX + 3.8, y: diagY + 0.5 + i * 0.8, w: 1.0, h: 0.5,
    align: "left", valign: "middle",
    fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Layer 4: Third Sigma layer (green) with Netj/Oj labels
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 5.5, y: diagY + 0.5 + i * 0.8, w: 0.5, h: 0.5,
    fill: { color: "FFFFFF" }, line: { color: GREEN, width: 1.5 },
  });
  s.addText("Σ", {
    x: diagX + 5.5, y: diagY + 0.5 + i * 0.8, w: 0.5, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 20, bold: true, color: GREEN, fontFace: FONT, margin: 0,
  });
  s.addText("Netj\nOj", {
    x: diagX + 5.5, y: diagY + 0.5 + i * 0.8, w: 1.0, h: 0.5,
    align: "left", valign: "middle",
    fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Output layer
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 7.2, y: diagY + 0.5 + i * 0.8, w: 0.5, h: 0.5,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  s.addText(`Output ${i===2 ? 'm' : i+1}`, {
    x: diagX + 7.8, y: diagY + 0.5 + i * 0.8, w: 0.7, h: 0.4,
    align: "left", valign: "middle",
    fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Weight labels on arrows
s.addText("wji", {
  x: diagX + 1.2, y: diagY + 0.3, w: 0.5, h: 0.2,
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("wjj", {
  x: diagX + 3.1, y: diagY + 0.3, w: 0.5, h: 0.2,
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

// Red highlighted output node (top one)
s.addShape(pres.shapes.OVAL, {
  x: diagX + 7.2, y: diagY + 0.5, w: 0.5, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 3 },
});

// Circled "1" icon near Node Bias (certified spec: circled 1 in purple near Node Bias)
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

// Circled "1" icon near bottom center of diagram
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

// Class boxes - use "Class m" for the last one
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 12.7, y: diagY + 0.3 + i * 0.65, w: 0.6, h: 0.5,
    fill: { color: LIGHT_GREEN }, line: { color: BLACK, width: 1 },
  });
  s.addText(i === 2 ? "Class m" : `Class ${i+1}`, {
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

// The word "Sigmoid" is part of the eq3 image itself (mathtext:
// "\text{For Output Layer, Sigmoid Activation } ..."), so no separate red text
// overlay is drawn — an overlay there covers the "⇒ Δji =" term of the equation.

// Write file
pres.writeFile({ fileName: "slide_011_recreated_attempt2.pptx" })
  .then(() => console.log("wrote slide_011_recreated_attempt2.pptx"))
  .catch(e => console.error(e));