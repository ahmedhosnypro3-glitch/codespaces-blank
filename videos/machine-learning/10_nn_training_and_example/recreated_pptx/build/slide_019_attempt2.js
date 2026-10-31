// slide_019.js — Backprop training (slide 19)
const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "B03030";
const YELLOW_BADGE = "FFF9C4";
const BADGE_TEXT = "333333";
const TEXT = "000000";
const CYAN_BOX = "D9F2F2";
const CYAN_BORDER = "2E5C8A";
const TAN_BOX = "D8CEC0";
const MAGENTA = "CC00CC";
const RED_ARROW = "FF0000";
const GREEN = "008000";
const DARK_BLUE = "1F4E79";
const C00000 = "C00000";
const FONT = "Arial";
const EQBASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/eq_slide_019/";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE CHROME
s.addShape(pptx.ShapeType.rect, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2, line: { color: "C00000", width: 1.5 },
});
s.addShape(pptx.ShapeType.ellipse, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 1.5 },
});
s.addText("19", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Top-left: cyan box with four implication statements
s.addShape(pptx.ShapeType.rect, {
  x: 0.53, y: 0.75, w: 4.8, h: 2.1,
  fill: { color: CYAN_BOX }, line: { color: CYAN_BORDER, width: 1 },
});

const stmtFont = "Times New Roman";
const stmtJam = [
  { text: "W", options: { italic: true, bold: true, color: TEXT, fontFace: stmtFont } },
];

// Four lines of bold-italic statements with red arrow
s.addText(
  [
    { text: "W", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "ji", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " Affects ", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " ", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "⇒", options: { bold: true, fontSize: 16, color: RED_ARROW, fontFace: FONT } },
  ],
  { x: 0.63, y: 0.85, w: 4.6, h: 0.35, margin: 0, align: "left", valign: "top" }
);
s.addText(
  [
    { text: "Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " Affects ", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "O", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " ", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "⇒", options: { bold: true, fontSize: 16, color: RED_ARROW, fontFace: FONT } },
  ],
  { x: 0.63, y: 1.25, w: 4.6, h: 0.35, margin: 0, align: "left", valign: "top" }
);
s.addText(
  [
    { text: "O", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " Affects ", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "(Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=1", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=2", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", ..., Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=m", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ") ", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "⇒", options: { bold: true, fontSize: 16, color: RED_ARROW, fontFace: FONT } },
  ],
  { x: 0.63, y: 1.65, w: 4.6, h: 0.35, margin: 0, align: "left", valign: "top" }
);
s.addText(
  [
    { text: "(Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=1", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=2", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", ..., Net", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=m", options: { subscript: true, italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ") Affect Error", options: { italic: true, bold: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
  ],
  { x: 0.63, y: 2.05, w: 4.6, h: 0.35, margin: 0, align: "left", valign: "top" }
);

// ===== NEURAL NETWORK DIAGRAM (center-right) =====
// Tan container: upper-center to top-right, x≈41-89%, y≈13-40%
// In inches: x≈5.46, y≈0.975, w≈6.4, h≈2.0
const tanX = 5.46;
const tanY = 0.975;
const tanW = 6.4;
const tanH = 2.0;

s.addShape(pptx.ShapeType.rect, {
  x: tanX, y: tanY, w: tanW, h: tanH,
  fill: { color: TAN_BOX },
});

// Column positions inside tan container
// Col 0: input dots (magenta) at far left
// Col 1-2-3: Σ/f nodes (red, red, blue)
// Col 4: Σ nodes (green)
// Col 5: f nodes (yellow/orange)
// Col 6: Σ nodes (orange)
// Net_k rectangles (dark blue)
// Error bar (red)
// Class labels (green)

const numRows = 3;
const col0X = tanX + 0.15;  // input dots
const col1X = tanX + 0.7;   // red Σ
const col2X = tanX + 1.1;   // red f
const col3X = tanX + 1.7;   // blue f
const col4X = tanX + 2.4;   // green Σ
const col5X = tanX + 3.2;   // yellow f
const col6X = tanX + 3.9;   // orange Σ
const netX = tanX + 4.6;    // Net_k blue rects
const errorX = netX + 0.8;  // Error bar
const classX = errorX + 0.45;

const rowYs = [tanY + 0.3, tanY + 0.75, tanY + 1.2];

// Inter-node connections: forward black arrows + blue weight labels;
// dashed red arrows back from the Error bar (error backpropagation).
const FWD = { color: "333333", width: 0.75, endArrowType: "triangle" };
const BWD = { color: "C00000", width: 1, dashType: "dash", beginArrowType: "triangle" };
const edgeGaps = [
  [col0X + 0.15, 0.075, col1X - (col0X + 0.15)],
  [col1X + 0.25, 0.125, col2X - (col1X + 0.25)],
  [col2X + 0.2, 0.1, col3X - (col2X + 0.2)],
  [col3X + 0.2, 0.1, col4X - (col3X + 0.2)],
  [col4X + 0.25, 0.125, col5X - (col4X + 0.25)],
  [col5X + 0.25, 0.125, col6X - (col5X + 0.25)],
  [col6X + 0.25, 0.125, netX - (col6X + 0.25)],
];
for (const [ex, cyOff, gap] of edgeGaps) {
  for (let i = 0; i < numRows; i++) {
    s.addShape(pptx.ShapeType.line, {
      x: ex, y: rowYs[i] + cyOff, w: gap, h: 0.02, line: FWD,
    });
  }
}
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.line, {
    x: netX + 0.8, y: rowYs[i] + 0.075,
    w: errorX - (netX + 0.8), h: 0.02, line: FWD,
  });
}
// cross-layer edges so the net reads fully connected
for (let i = 0; i < numRows; i++) {
  for (let j = 0; j < numRows; j++) {
    if (i === j) continue;
    s.addShape(pptx.ShapeType.line, {
      x: col0X + 0.15, y: rowYs[i] + 0.075,
      w: col1X - (col0X + 0.15), h: rowYs[j] - rowYs[i], line: FWD,
    });
    s.addShape(pptx.ShapeType.line, {
      x: col4X + 0.25, y: rowYs[i] + 0.125,
      w: col5X - (col4X + 0.25), h: rowYs[j] - rowYs[i], line: FWD,
    });
  }
}
// weight labels (blue, italic) on two edges per row
function weightLabel(gx, cy) {
  s.addText("w", {
    x: gx - 0.15, y: cy - 0.19, w: 0.3, h: 0.16,
    align: "center", fontSize: 9, bold: true, italic: true,
    color: "1F4E79", fontFace: FONT, margin: 0,
  });
}
for (let i = 0; i < numRows; i++) {
  weightLabel((col1X + 0.25 + col2X) / 2, rowYs[i] + 0.125);
  weightLabel((col5X + 0.25 + col6X) / 2, rowYs[i] + 0.125);
}
// dashed backprop arrows: Error bar -> layer 3 nodes
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.line, {
    x: col3X + 0.2, y: rowYs[i] + 0.1,
    w: errorX - (col3X + 0.2),
    h: (rowYs[2] - rowYs[0]) * (i === 0 ? -0.35 : i === 2 ? 0.35 : 0.35),
    flipH: true, line: BWD,
  });
}

// Input dots (magenta)
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: col0X, y: rowYs[i], w: 0.15, h: 0.15,
    fill: { color: MAGENTA },
  });
}

// Red Σ column (col 1)
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: col1X, y: rowYs[i], w: 0.25, h: 0.25,
    line: { color: RED, width: 1.5 },
  });
  s.addText("Σ", {
    x: col1X, y: rowYs[i], w: 0.25, h: 0.25,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
  // Red f boxes to right
  s.addShape(pptx.ShapeType.rect, {
    x: col2X, y: rowYs[i], w: 0.2, h: 0.2,
    line: { color: RED, width: 1 },
  });
  s.addText("σ", {
    x: col2X, y: rowYs[i], w: 0.2, h: 0.2,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0, italic: true,
  });
}

// Blue f column (col 3)
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.rect, {
    x: col3X, y: rowYs[i], w: 0.2, h: 0.2,
    line: { color: "3498DB", width: 1 },
  });
  s.addText("σ", {
    x: col3X, y: rowYs[i], w: 0.2, h: 0.2,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: "3498DB", fontFace: FONT, margin: 0, italic: true,
  });
}

// Green Σ column (col 4)
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: col4X, y: rowYs[i], w: 0.25, h: 0.25,
    line: { color: GREEN, width: 1.5 },
  });
  s.addText("Σ", {
    x: col4X, y: rowYs[i], w: 0.25, h: 0.25,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: GREEN, fontFace: FONT, margin: 0,
  });
}

// Yellow f column (col 5)
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: col5X, y: rowYs[i], w: 0.25, h: 0.25,
    fill: { color: "FFC000" }, line: { color: "ED7D31", width: 1.5 },
  });
  s.addText("σ", {
    x: col5X, y: rowYs[i], w: 0.25, h: 0.25,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: "ED7D31", fontFace: FONT, margin: 0, italic: true,
  });
}

// Orange Σ column (col 6)
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: col6X, y: rowYs[i], w: 0.25, h: 0.25,
    fill: { color: "ED7D31" }, line: { color: "ED7D31", width: 1.5 },
  });
  s.addText("Σ", {
    x: col6X, y: rowYs[i], w: 0.25, h: 0.25,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}

// Net_k blue rectangles with white text
const netLabels = ["Net_k=1", "Net_k=2", "Net_k=3"];
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.rect, {
    x: netX, y: rowYs[i], w: 0.8, h: 0.25,
    fill: { color: DARK_BLUE },
  });
  s.addText(netLabels[i], {
    x: netX, y: rowYs[i], w: 0.8, h: 0.25,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}

// Error bar
s.addShape(pptx.ShapeType.rect, {
  x: errorX, y: tanY + 0.15, w: 0.35, h: tanH - 0.3,
  fill: { color: C00000 },
});
// "Error Error Error" stacked on the bar, as the frame shows
s.addText("Error\nError\nError", {
  x: errorX - 0.12, y: tanY + 0.15, w: 0.6, h: tanH - 0.3,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Class labels
const classLabels = ["Class 1", "Class 2", "Class m"];
for (let i = 0; i < numRows; i++) {
  s.addText(classLabels[i], {
    x: classX, y: rowYs[i] - 0.05, w: 1.0, h: 0.3,
    align: "left", valign: "middle",
    fontSize: 11, bold: true, color: GREEN, fontFace: FONT, margin: 0,
  });
}

// Bottom annotation row INSIDE the tan container (was clipped below it)
const bottomY = tanY + tanH - 0.28;

// "Sample Data" dot + text
s.addShape(pptx.ShapeType.ellipse, {
  x: col0X, y: bottomY, w: 0.15, h: 0.15,
  fill: { color: MAGENTA },
});
s.addText("Sample Data", {
  x: col0X + 0.2, y: bottomY - 0.05, w: 1.5, h: 0.2,
  fontSize: 10, color: MAGENTA, fontFace: FONT, margin: 0,
});

// Hollow light-blue upward arrow under blue f column
s.addShape(pptx.ShapeType.upArrow, {
  x: col3X + 0.05, y: bottomY - 0.1, w: 0.15, h: 0.2,
  fill: { color: "3498DB" }, line: { color: "3498DB", width: 1 },
});

// Magenta circle with white "1"
s.addShape(pptx.ShapeType.ellipse, {
  x: col4X + 0.05, y: bottomY - 0.1, w: 0.18, h: 0.18,
  fill: { color: MAGENTA },
});
s.addText("1", {
  x: col4X + 0.05, y: bottomY - 0.1, w: 0.18, h: 0.18,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Hollow green upward arrow under green Σ
s.addShape(pptx.ShapeType.upArrow, {
  x: col6X + 0.05, y: bottomY - 0.1, w: 0.15, h: 0.2,
  fill: { color: GREEN }, line: { color: GREEN, width: 1 },
});

// Second magenta circle with white "1"
s.addShape(pptx.ShapeType.ellipse, {
  x: col5X + 0.05, y: bottomY - 0.1, w: 0.18, h: 0.18,
  fill: { color: MAGENTA },
});
s.addText("1", {
  x: col5X + 0.05, y: bottomY - 0.1, w: 0.18, h: 0.18,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Orange X under orange Σ
s.addText("X", {
  x: col6X + 0.12, y: bottomY - 0.05, w: 0.2, h: 0.2,
  fontSize: 14, bold: true, color: "ED7D31", fontFace: FONT, margin: 0,
});

// ===== BOTTOM-LEFT: Chain-rule equation panel =====
// White box with blue border at bottom-left, x≈4-67%, y≈42-74%
// x≈0.53, y≈3.15, w≈8.3, h≈2.45
s.addShape(pptx.ShapeType.rect, {
  x: 0.53, y: 3.15, w: 8.3, h: 2.45,
  fill: { color: "FFFFFF" }, line: { color: CYAN_BORDER, width: 1 },
});
// Equation as image (natural size: w = px/600)
s.addImage({
  path: EQBASE + "eq1.png",
  x: 0.62, y: 3.42, w: 7.03667, h: 0.39167,
});

// ===== BOTTOM-RIGHT: Derivative reference panel =====
// White box with blue border at bottom-right, x≈67-95%, y≈42-83%
// x≈8.93, y≈3.15, w≈4.0, h≈2.85
s.addShape(pptx.ShapeType.rect, {
  x: 8.93, y: 3.15, w: 4.0, h: 2.85,
  fill: { color: "FFFFFF" }, line: { color: CYAN_BORDER, width: 1 },
});

// Four stacked equations as images
const eqYStart = 3.25;
const eqYStep = 0.6;
s.addImage({ path: EQBASE + "eq2.png", x: 9.0, y: eqYStart, w: 1.08667, h: 0.285 });
s.addImage({ path: EQBASE + "eq3.png", x: 9.0, y: eqYStart + eqYStep, w: 2.505, h: 0.41833 });
s.addImage({ path: EQBASE + "eq4.png", x: 9.0, y: eqYStart + 2*eqYStep, w: 2.825, h: 0.345 });
s.addImage({ path: EQBASE + "eq5.png", x: 9.0, y: eqYStart + 3*eqYStep, w: 2.30833, h: 0.455 });

// Output file
pptx.writeFile({
  fileName: "videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_019_attempt2.pptx"
}).then(() => console.log("done: slide_019_attempt2.pptx"));