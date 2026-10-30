// slide_010.js — Build "Gradient Descent" slide for 10_nn_training_and_example
// Run: NODE_PATH=$(npm root -g) node slide_010.js

const pptxgen = require("pptxgenjs");

const W = 13.33, H = 7.5;
const FONT = "Arial";

// Equation metadata (from render_eq.py output)
const EQS = {
  eq1: {w_in: 2.07667, h_in: 0.35167, baseline_frac: 0.65403},
  eq2: {w_in: 1.89, h_in: 0.33833, baseline_frac: 0.6798},
  eq3: {w_in: 1.03833, h_in: 0.305, baseline_frac: 0.59563},
  eq4: {w_in: 1.45167, h_in: 0.44667, baseline_frac: 0.47388},
  eq5: {w_in: 1.92333, h_in: 0.29, baseline_frac: 0.62069},
  eq6: {w_in: 1.39333, h_in: 0.41833, baseline_frac: 0.50598},
  eq7: {w_in: 1.33667, h_in: 0.30667, baseline_frac: 0.59239},
  eq8: {w_in: 1.50667, h_in: 0.345, baseline_frac: 0.64251},
  eq9: {w_in: 0.80667, h_in: 0.34333, baseline_frac: 0.64078},
  eq10: {w_in: 1.76, h_in: 0.34667, baseline_frac: 0.63942},
  eq11: {w_in: 1.06, h_in: 0.34333, baseline_frac: 0.64078},
  eq12: {w_in: 3.345, h_in: 0.23167, baseline_frac: 0.69784},
  eq13: {w_in: 2.92, h_in: 0.305, baseline_frac: 0.59563},
  eq14: {w_in: 1.90333, h_in: 0.305, baseline_frac: 0.59563},
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };  // white background per analysis

// ============ HOUSE CHROME ============
// 1. Outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("10", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position)
s.addText("Gradient Descent", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ============ SLIDE CONTENT ============
const RED = "B22222";
const BLACK = "000000";
const LIGHT_BLUE = "B0E0E6";
const LIGHT_GREEN = "90EE90";
const YELLOW_BOX = "FFFFE0";
const PURPLE = "800080";
const RED_ACCENT = "FF0000";
const GREEN = "008000";
const GREY = "D3D3D3";

function addEq(name, x, y) {
  const eq = EQS[name];
  s.addImage({ path: `./eq_slide_010/${name}.png`, x, y, w: eq.w_in, h: eq.h_in });
}

// ---- 1. Top-left title box with equations ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.55, w: 5.5, h: 2.8,
  fill: { color: "FFFFFF" },
  line: { color: RED, width: 1.5 },
});

s.addText("Gradient Descent", {
  x: 0.5, y: 0.6, w: 5.3, h: 0.45,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
});

addEq("eq1", 0.5, 1.1);
addEq("eq2", 0.5, 1.55);
addEq("eq3", 0.5, 2.0);

// ---- 2. Neural Network Diagram (top-right) ----
const diagX = 6.5, diagY = 0.55, diagW = 6.3, diagH = 2.8;

// Input layer (purple dots)
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 0.3, y: diagY + 0.3 + i * 0.7, w: 0.15, h: 0.15,
    fill: { color: PURPLE }, line: { color: PURPLE, width: 1 },
  });
}
s.addText("Input\nBias", {
  x: diagX - 0.2, y: diagY + 0.3, w: 0.5, h: 1.0,
  align: "right", valign: "middle",
  fontSize: 9, color: PURPLE, fontFace: FONT, margin: 0,
});

// Hidden layer 1 (white circles with sigma)
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 1.5, y: diagY + 0.3 + i * 0.7, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  s.addText("Σ", {
    x: diagX + 1.5, y: diagY + 0.3 + i * 0.7, w: 0.4, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
  s.addText("f()", {
    x: diagX + 2.0, y: diagY + 0.3 + i * 0.7, w: 0.3, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Hidden layer 2 (blue)
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 3.0, y: diagY + 0.3 + i * 0.7, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 },
  });
  s.addText("Σ", {
    x: diagX + 3.0, y: diagY + 0.3 + i * 0.7, w: 0.4, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
  });
  s.addText("Netj\nOj", {
    x: diagX + 3.0, y: diagY + 0.3 + i * 0.7, w: 0.8, h: 0.5,
    align: "left", valign: "middle",
    fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Hidden layer 3 (green)
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 4.2, y: diagY + 0.3 + i * 0.7, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: GREEN, width: 1 },
  });
  s.addText("Σ", {
    x: diagX + 4.2, y: diagY + 0.3 + i * 0.7, w: 0.4, h: 0.4,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: GREEN, fontFace: FONT, margin: 0,
  });
  s.addText("Netj\nOj", {
    x: diagX + 4.2, y: diagY + 0.3 + i * 0.7, w: 0.8, h: 0.5,
    align: "left", valign: "middle",
    fontSize: 8, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Output layer
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.OVAL, {
    x: diagX + 5.2, y: diagY + 0.3 + i * 0.7, w: 0.4, h: 0.4,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  s.addText(`Output ${i+1}`, {
    x: diagX + 5.7, y: diagY + 0.3 + i * 0.7, w: 0.7, h: 0.4,
    align: "left", valign: "middle",
    fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Error classes on right
s.addShape(pres.shapes.RECTANGLE, {
  x: diagX + 5.9, y: diagY + 0.3, w: 0.8, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 },
});
s.addText("Error\nClass 1", {
  x: diagX + 5.9, y: diagY + 0.3, w: 0.8, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 9, color: RED, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: diagX + 5.9, y: diagY + 1.0, w: 0.8, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
});
s.addText("Error\nClass 2", {
  x: diagX + 5.9, y: diagY + 1.0, w: 0.8, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: diagX + 5.9, y: diagY + 1.7, w: 0.8, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 },
});
s.addText("Error\nClass m", {
  x: diagX + 5.9, y: diagY + 1.7, w: 0.8, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 9, color: RED, fontFace: FONT, margin: 0,
});

// ---- 3. Middle equation strip ----
const yMid = 3.6;

addEq("eq4", 0.5, yMid);
s.addText("For Sigmoid Activation", {
  x: 0.5, y: yMid + 0.5, w: 5, h: 0.3,
  align: "left", valign: "top",
  fontSize: 13, bold: true, color: RED, fontFace: FONT, margin: 0,
});
addEq("eq5", 0.5, yMid + 0.8);
addEq("eq6", 0.5, yMid + 1.2);

// ---- 4. Three partial derivative boxes ----
const yPartial = 4.5;
const boxW = 4.0, boxH = 1.2;
const boxX = [0.5, 4.8, 9.1];

for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: boxX[i], y: yPartial, w: boxW, h: boxH,
    fill: { color: i === 2 ? LIGHT_BLUE : "FFFFFF" },
    line: { color: BLACK, width: 1 },
  });
}

addEq("eq7", 0.6, yPartial + 0.2);
addEq("eq8", 4.9, yPartial + 0.2);
addEq("eq9", 9.2, yPartial + 0.2);

// ---- 5. Large chain-rule derivation box ----
const yDeriv = 5.8;
const boxDerivX = 0.5, boxDerivY = yDeriv, boxDerivW = 8.0, boxDerivH = 1.8;

s.addShape(pres.shapes.RECTANGLE, {
  x: boxDerivX, y: boxDerivY, w: boxDerivW, h: boxDerivH,
  fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1.5 },
});

// Highlight regions
s.addShape(pres.shapes.RECTANGLE, {
  x: boxDerivX + 0.1, y: boxDerivY + 0.1, w: 4.0, h: 0.4,
  fill: { color: LIGHT_BLUE }, line: { type: "none" },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: boxDerivX + 0.1, y: boxDerivY + 0.6, w: 4.0, h: 0.4,
  fill: { color: LIGHT_GREEN }, line: { type: "none" },
});

addEq("eq10", 0.6, boxDerivY + 0.1);
addEq("eq11", 0.6, boxDerivY + 0.45);
addEq("eq12", 0.6, boxDerivY + 0.8);
addEq("eq13", 0.6, boxDerivY + 1.2);

// ---- 6. Yellow summary box (right) ----
const yYellow = 5.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.0, y: yYellow, w: 3.8, h: 1.8,
  fill: { color: YELLOW_BOX }, line: { color: BLACK, width: 1 },
});

addEq("eq7", 9.1, yYellow + 0.2);
addEq("eq8", 9.1, yYellow + 0.6);
addEq("eq9", 9.1, yYellow + 1.0);

// ---- 7. Bottom strip with final delta rule ----
const yBottom = 6.9;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.3, y: yBottom, w: W - 0.6, h: 0.5,
  fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.3, y: yBottom + 0.1, w: 6.0, h: 0.3,
  fill: { color: LIGHT_GREEN }, line: { type: "none" },
});

addEq("eq14", 0.4, yBottom + 0.05);
s.addText("Where δj = (tj - Oj) * Oj(1-Oj) for output Layer", {
  x: 6.5, y: yBottom + 0.05, w: 6.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});

// Write file
pres.writeFile({ fileName: "slide_010_recreated.pptx" })
  .then(() => console.log("wrote slide_010_recreated.pptx"))
  .catch(e => console.error(e));