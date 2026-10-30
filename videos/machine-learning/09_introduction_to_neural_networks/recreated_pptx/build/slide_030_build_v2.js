// Build slide 030: Example - Bad Weights (badge 30) - FIXED version
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";

// ---- HOUSE CHROME ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 1.5 },
});
s.addText("30", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Title "Example" in red serif
s.addText("Example", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "left", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: "Times New Roman", margin: 0,
});

// "Bad Weights" in pink box below title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.6, y: 0.85, w: 2.5, h: 0.35,
  fill: { color: "F8CBAD" }, line: { color: "F8CBAD", width: 0 },
});
s.addText("Bad Weights", {
  x: 0.6, y: 0.85, w: 2.5, h: 0.35,
  align: "center", valign: "middle",
  fontSize: 12, color: "000000", fontFace: FONT, margin: 0,
});

// ============================================================
// NEURAL NETWORK DIAGRAM with RED BORDER
// Diagram frame: x=2.0 to 11.0, y=0.7 to 3.5 (approx)
// ============================================================
const diagram = {
  x: 2.0, y: 0.7, w: 9.0, h: 2.8,
  inputX: 2.3,
  hiddenX: 5.5,
  outputX: 8.5,
  // Node Y positions - 3 hidden, 2 output
  hiddenYs: [1.1, 1.8, 2.5],
  outputYs: [1.45, 2.15],
};

s.addShape(pres.shapes.RECTANGLE, {
  x: diagram.x, y: diagram.y, w: diagram.w, h: diagram.h,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 2 },
});

// ---- Input labels x1, x2 ----
s.addText("x1", { x: diagram.inputX - 0.5, y: diagram.hiddenYs[0] - 0.15, w: 0.5, h: 0.3, align: "right", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("x2", { x: diagram.inputX - 0.5, y: diagram.hiddenYs[2] - 0.15, w: 0.5, h: 0.3, align: "right", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });

// ---- Input values [7], [4] in vertical bracket ----
// Draw bracket using lines
s.addShape(pres.shapes.LINE, {
  x: diagram.inputX + 0.1, y: diagram.hiddenYs[0] - 0.25, w: 0, h: diagram.hiddenYs[2] - diagram.hiddenYs[0] + 0.5,
  line: { color: "000000", width: 1.5 }
});
s.addShape(pres.shapes.LINE, {
  x: diagram.inputX + 0.1, y: diagram.hiddenYs[0] - 0.25, w: 0.2, h: 0,
  line: { color: "000000", width: 1.5 }
});
s.addShape(pres.shapes.LINE, {
  x: diagram.inputX + 0.1, y: diagram.hiddenYs[2] + 0.25, w: 0.2, h: 0,
  line: { color: "000000", width: 1.5 }
});
s.addText("[7]", { x: diagram.inputX + 0.35, y: diagram.hiddenYs[0] - 0.15, w: 0.4, h: 0.3, align: "center", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0 });
s.addText("[4]", { x: diagram.inputX + 0.35, y: diagram.hiddenYs[2] - 0.15, w: 0.4, h: 0.3, align: "center", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0 });

// ---- Input-to-hidden weights (from x1: 0.1, 0.2, 0.3; from x2: 0.4, 0.5, 0.6) ----
// We'll place weight labels near the connection lines
const weightLabels_x1 = ["0.1", "0.2", "0.3"];
const weightLabels_x2 = ["0.4", "0.5", "0.6"];

// ---- Hidden layer nodes (3 yellow circles) ----
for (let i = 0; i < 3; i++) {
  const y = diagram.hiddenYs[i];
  // Yellow circle
  s.addShape(pres.shapes.OVAL, {
    x: diagram.hiddenX - 0.25, y: y - 0.25, w: 0.5, h: 0.5,
    fill: { color: "FFE699" }, line: { color: "000000", width: 1 },
  });
  // Node number
  s.addText([3, 4, 5][i].toString(), {
    x: diagram.hiddenX - 0.25, y: y - 0.25, w: 0.5, h: 0.5,
    align: "center", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  // O labels above (blue)
  s.addText(["O3", "O4", "O5"][i], {
    x: diagram.hiddenX - 0.25, y: y - 0.5, w: 0.5, h: 0.3,
    align: "center", fontSize: 10, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
  });
}

// ---- Output layer nodes (2 orange circles) ----
for (let i = 0; i < 2; i++) {
  const y = diagram.outputYs[i];
  s.addShape(pres.shapes.OVAL, {
    x: diagram.outputX - 0.25, y: y - 0.25, w: 0.5, h: 0.5,
    fill: { color: "F4B183" }, line: { color: "000000", width: 1 },
  });
  s.addText([6, 7][i].toString(), {
    x: diagram.outputX - 0.25, y: y - 0.25, w: 0.5, h: 0.5,
    align: "center", valign: "middle", fontSize: 14, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  // O labels
  s.addText(["O6", "O7"][i], {
    x: diagram.outputX + 0.3, y: y - 0.15, w: 0.5, h: 0.3,
    align: "left", fontSize: 10, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
  });
}

// ============================================================
// CONNECTION LINES WITH PER-EDGE WEIGHT LABELS
// ============================================================

// Input-to-hidden connections (6 lines)
// x1 (top) to hidden 3,4,5; x2 (bottom) to hidden 3,4,5
const inputYs = [diagram.hiddenYs[0], diagram.hiddenYs[2]]; // x1 top, x2 bottom
const weight_x1 = [0.1, 0.2, 0.3];
const weight_x2 = [0.4, 0.5, 0.6];

for (let hi = 0; hi < 3; hi++) {
  const hy = diagram.hiddenYs[hi];
  
  // From x1 (top input)
  s.addShape(pres.shapes.LINE, {
    x: diagram.inputX + 0.3, y: inputYs[0], w: diagram.hiddenX - diagram.inputX - 0.55, h: hy - inputYs[0],
    line: { color: "000000", width: 1 }
  });
  // Weight label on x1->hidden connection
  const midX1 = diagram.inputX + 0.3 + (diagram.hiddenX - diagram.inputX - 0.55) * 0.3;
  const midY1 = inputYs[0] + (hy - inputYs[0]) * 0.3;
  s.addText(weight_x1[hi].toString(), {
    x: midX1 - 0.2, y: midY1 - 0.1, w: 0.4, h: 0.2,
    align: "center", fontSize: 9, color: "000000", fontFace: FONT, margin: 0,
  });
  
  // From x2 (bottom input)
  s.addShape(pres.shapes.LINE, {
    x: diagram.inputX + 0.3, y: inputYs[1], w: diagram.hiddenX - diagram.inputX - 0.55, h: hy - inputYs[1],
    line: { color: "000000", width: 1 }
  });
  const midX2 = diagram.inputX + 0.3 + (diagram.hiddenX - diagram.inputX - 0.55) * 0.3;
  const midY2 = inputYs[1] + (hy - inputYs[1]) * 0.3;
  s.addText(weight_x2[hi].toString(), {
    x: midX2 - 0.2, y: midY2 - 0.1, w: 0.4, h: 0.2,
    align: "center", fontSize: 9, color: "000000", fontFace: FONT, margin: 0,
  });
}

// Hidden-to-output connections (6 lines: 3 hidden × 2 output)
// Weights: 0.3 from node 3, 0.4 from node 4, 0.5 from node 5 (red)
const hiddenToOutputWeights = [0.3, 0.4, 0.5];
for (let hi = 0; hi < 3; hi++) {
  const hy = diagram.hiddenYs[hi];
  for (let oi = 0; oi < 2; oi++) {
    const oy = diagram.outputYs[oi];
    s.addShape(pres.shapes.LINE, {
      x: diagram.hiddenX + 0.25, y: hy, w: diagram.outputX - diagram.hiddenX - 0.5, h: oy - hy,
      line: { color: "000000", width: 1 }
    });
    // Weight label (red) - place midway
    const midX = diagram.hiddenX + 0.25 + (diagram.outputX - diagram.hiddenX - 0.5) * 0.5;
    const midY = hy + (oy - hy) * 0.5;
    s.addText(hiddenToOutputWeights[hi].toString(), {
      x: midX - 0.15, y: midY - 0.1, w: 0.3, h: 0.2,
      align: "center", fontSize: 9, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
    });
  }
}

// ============================================================
// OUTPUT / TARGET COLUMNS WITH SPANNING BRACKET
// ============================================================
const targetX = diagram.outputX + 1.2;
s.addText("Output", { x: targetX - 0.1, y: diagram.y + 0.1, w: 1.0, h: 0.3, align: "center", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0 });
s.addText("Target", { x: targetX + 0.8, y: diagram.y + 0.1, w: 1.0, h: 0.3, align: "center", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0 });

// Target column with spanning left bracket [ 0 ; 1 ]
const t6y = diagram.outputYs[0];
const t7y = diagram.outputYs[1];
const targetTop = t6y - 0.2;
const targetBot = t7y + 0.2;

// Spanning left bracket for target column
s.addShape(pres.shapes.LINE, {
  x: targetX + 0.6, y: targetTop, w: 0, h: targetBot - targetTop,
  line: { color: "000000", width: 1.5 }
});
s.addShape(pres.shapes.LINE, {
  x: targetX + 0.6, y: targetTop, w: 0.15, h: 0,
  line: { color: "000000", width: 1.5 }
});
s.addShape(pres.shapes.LINE, {
  x: targetX + 0.6, y: targetBot, w: 0.15, h: 0,
  line: { color: "000000", width: 1.5 }
});

// Target values and t-labels
s.addText("[0]", { x: targetX + 0.8, y: t6y - 0.12, w: 0.4, h: 0.25, align: "center", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("t6", { x: targetX + 1.2, y: t6y - 0.12, w: 0.4, h: 0.25, align: "left", fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
s.addText("[1]", { x: targetX + 0.8, y: t7y - 0.12, w: 0.4, h: 0.25, align: "center", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("t7", { x: targetX + 1.2, y: t7y - 0.12, w: 0.4, h: 0.25, align: "left", fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });

// Dashed lines from output nodes to target bracket
for (let i = 0; i < 2; i++) {
  const oy = diagram.outputYs[i];
  const tx = targetX + 0.6;
  s.addShape(pres.shapes.LINE, {
    x: diagram.outputX + 0.25, y: oy, w: tx - (diagram.outputX + 0.25), h: 0,
    line: { color: "000000", width: 1, dashType: "dash", endArrow: "triangle" }
  });
}

// ============================================================
// "FORWARD" HEADER
// ============================================================
s.addText("Forward", { x: 0.6, y: 3.7, w: 1.5, h: 0.3, align: "left", fontSize: 14, bold: true, italic: true, color: "0000FF", fontFace: "Times New Roman", margin: 0 });

// ============================================================
// EQUATION BOXES - USE PROFESSIONAL 2D MATH (PNGs)
// ============================================================
const eqDir = "."; // equations generated in same dir

// Helper to add equation PNG if exists
function addEqPNG(name, x, y, maxW, maxH) {
  const path = `${eqDir}/${name}`;
  if (fs.existsSync(path)) {
    // Calculate size from image
    // We know the PNG is 600dpi, so size in inches = px/600
    // But pptxgenjs expects inches
    const img = fs.readFileSync(path);
    // For now use fixed reasonable sizes based on generation output
    s.addImage({ path, x, y, w: maxW, h: maxH });
    return true;
  }
  return false;
}

// ---- Blue equation box 1: Net3, Net4, Net5 ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.1, w: 4.0, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 },
});

// Use Net equation PNGs (professional 2D with proper subscripts)
const net3W = 1704/600; const net3H = 133/600;
const net4W = 1704/600; const net4H = 133/600;
const net5W = 1704/600; const net5H = 133/600;

if (!addEqPNG("eq_Net3.png", 0.6, 4.12, net3W, net3H)) {
  s.addText("Net₃ = 7 × 0.1 + 4 × 0.4 = 2.3", { x: 0.6, y: 4.12, w: 3.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}
if (!addEqPNG("eq_Net4.png", 0.6, 4.45, net4W, net4H)) {
  s.addText("Net₄ = 7 × 0.2 + 4 × 0.5 = 3.4", { x: 0.6, y: 4.45, w: 3.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}
if (!addEqPNG("eq_Net5.png", 0.6, 4.78, net5W, net5H)) {
  s.addText("Net₅ = 7 × 0.3 + 4 × 0.6 = 4.5", { x: 0.6, y: 4.78, w: 3.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}

// ---- Blue equation box 2: Net6, Net7 ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.4, w: 6.5, h: 0.8,
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 },
});

const net6W = 3161/600; const net6H = 133/600;
const net7W = 3161/600; const net7H = 133/600;

if (!addEqPNG("eq_Net6.png", 0.6, 5.42, net6W, net6H)) {
  s.addText("Net₆ = 0.909 × 0.3 + 0.968 × 0.4 + 0.989 × 0.5 = 1.1544", { x: 0.6, y: 5.42, w: 6.3, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}
if (!addEqPNG("eq_Net7.png", 0.6, 5.75, net7W, net7H)) {
  s.addText("Net₇ = 0.909 × 0.3 + 0.968 × 0.4 + 0.989 × 0.5 = 1.1544", { x: 0.6, y: 5.75, w: 6.3, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}

// ---- Green equation box 1: O3, O4, O5 (sigmoid) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.5, y: 4.1, w: 5.0, h: 1.2,
  fill: { color: "FFFFFF" }, line: { color: "00B050", width: 1.5 },
});

const o3W = 1140/600; const o3H = 180/600;
const o4W = 1140/600; const o4H = 180/600;
const o5W = 1140/600; const o5H = 180/600;

if (!addEqPNG("eq_O3.png", 7.6, 4.12, o3W, o3H)) {
  s.addText("O₃ = 1 / (1 + e⁻²·³) = 0.909", { x: 7.6, y: 4.12, w: 4.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}
if (!addEqPNG("eq_O4.png", 7.6, 4.45, o4W, o4H)) {
  s.addText("O₄ = 1 / (1 + e⁻³·⁴) = 0.968", { x: 7.6, y: 4.45, w: 4.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}
if (!addEqPNG("eq_O5.png", 7.6, 4.78, o5W, o5H)) {
  s.addText("O₅ = 1 / (1 + e⁻⁴·⁵) = 0.989", { x: 7.6, y: 4.78, w: 4.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}

// ---- Green equation box 2: O6, O7 (sigmoid) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.5, y: 5.4, w: 5.0, h: 0.8,
  fill: { color: "FFFFFF" }, line: { color: "00B050", width: 1.5 },
});

const o6W = 1176/600; const o6H = 180/600;
const o7W = 1176/600; const o7H = 180/600;

if (!addEqPNG("eq_O6.png", 7.6, 5.42, o6W, o6H)) {
  s.addText("O₆ = 1 / (1 + e⁻¹·¹⁵⁴⁴) = 0.76", { x: 7.6, y: 5.42, w: 4.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}
if (!addEqPNG("eq_O7.png", 7.6, 5.75, o7W, o7H)) {
  s.addText("O₇ = 1 / (1 + e⁻¹·¹⁵⁴⁴) = 0.76", { x: 7.6, y: 5.75, w: 4.8, h: 0.35, fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
}

// ============================================================
// SAVE
// ============================================================
const outPath = "slide_030_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));