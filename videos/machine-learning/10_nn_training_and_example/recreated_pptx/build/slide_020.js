// slide_020.js — Hidden layer backprop (slide 20)
const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW_BADGE = "FFD700";
const BADGE_OUTLINE = "000000";
const TEXT = "000000";
const LIGHT_BLUE = "E1F5FE";
const LIGHT_RED = "FFCDD2";
const LIGHT_YELLOW = "FFF9C4";
const GRAY_BG = "D3D3D3";
const PURPLE = "9C27B0";
const GREEN = "4CAF50";
const ORANGE = "FF9800";
const BLUE = "0000FF";
const FONT = "Arial";
const EQBASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/eq_slide_020/";

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
s.addText("20", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Top-left: light blue box with four chain-of-affect lines
s.addShape(pptx.ShapeType.rect, {
  x: 0.53, y: 0.75, w: 5.0, h: 2.0,
  fill: { color: LIGHT_BLUE }, line: { color: BLUE, width: 1 },
});

const stmtFont = "Times New Roman";

// Four lines with red right-arrow
s.addText(
  [
    { text: "W", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " Affects ", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " ", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "→", options: { fontSize: 16, color: RED, fontFace: FONT } },
  ],
  { x: 0.63, y: 0.85, w: 4.8, h: 0.35, margin: 0, align: "left", valign: "top" }
);
s.addText(
  [
    { text: "Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " Affects ", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "O", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " ", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "→", options: { fontSize: 16, color: RED, fontFace: FONT } },
  ],
  { x: 0.63, y: 1.25, w: 4.8, h: 0.35, margin: 0, align: "left", valign: "top" }
);
s.addText(
  [
    { text: "O", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: " Affects ", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "(Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=1", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=2", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", ..., Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=m", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ") ", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "→", options: { fontSize: 16, color: RED, fontFace: FONT } },
  ],
  { x: 0.63, y: 1.65, w: 4.8, h: 0.35, margin: 0, align: "left", valign: "top" }
);
s.addText(
  [
    { text: "(Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=1", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=2", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ", ..., Net", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: "k=m", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
    { text: ") Affect Error", options: { italic: true, fontSize: 16, color: TEXT, fontFace: stmtFont } },
  ],
  { x: 0.63, y: 2.05, w: 4.8, h: 0.35, margin: 0, align: "left", valign: "top" }
);

// ===== NEURAL NETWORK DIAGRAM (top-right) =====
// Gray background: top-right quadrant
const diagramX = 6.0;
const diagramY = 0.75;
const diagramW = 6.8;
const diagramH = 2.3;

s.addShape(pptx.ShapeType.rect, {
  x: diagramX, y: diagramY, w: diagramW, h: diagramH,
  fill: { color: GRAY_BG },
});

// Input layer: purple Sigma circles (3 nodes)
const numRows = 3;
const rowYs = [diagramY + 0.3, diagramY + 0.8, diagramY + 1.3];
const inputX = diagramX + 0.5;
const hiddenX = diagramX + 2.2;
const outputX = diagramX + 4.0;
const errorX = outputX + 1.2;
const classX = errorX + 0.45;

// Input nodes: purple circles with Σ
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: inputX, y: rowYs[i], w: 0.3, h: 0.3,
    fill: { color: PURPLE },
  });
  s.addText("Σ", {
    x: inputX, y: rowYs[i], w: 0.3, h: 0.3,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}

// Arrows from input to hidden
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.rightArrow, {
    x: inputX + 0.3, y: rowYs[i] + 0.05, w: hiddenX - (inputX + 0.3), h: 0.2,
    fill: { color: TEXT },
  });
}

// Hidden nodes: green circles
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: hiddenX, y: rowYs[i], w: 0.35, h: 0.35,
    fill: { color: GREEN },
  });
}

// "Hidden Node" label pointing to one
s.addText("Hidden Node", {
  x: hiddenX - 1.0, y: rowYs[1] + 0.2, w: 1.0, h: 0.3,
  fontSize: 10, color: TEXT, fontFace: FONT, margin: 0,
});

// "Net" labels near connections
for (let i = 0; i < numRows; i++) {
  s.addText("Net", {
    x: hiddenX + 0.4, y: rowYs[i] - 0.1, w: 0.4, h: 0.2,
    fontSize: 10, color: TEXT, fontFace: FONT, margin: 0,
  });
}

// Arrows from hidden to output
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.rightArrow, {
    x: hiddenX + 0.35, y: rowYs[i] + 0.05, w: outputX - (hiddenX + 0.35), h: 0.2,
    fill: { color: TEXT },
  });
}

// Output nodes: orange/yellow circles
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: outputX, y: rowYs[i], w: 0.35, h: 0.35,
    fill: { color: ORANGE },
  });
  s.addText("Output", {
    x: outputX + 0.5, y: rowYs[i], w: 1.0, h: 0.35,
    align: "left", valign: "middle",
    fontSize: 10, color: TEXT, fontFace: FONT, margin: 0,
  });
}

// Blue dashed arrows - approximated with regular arrows
// Vertical red "Error" bar
s.addShape(pptx.ShapeType.rect, {
  x: errorX, y: diagramY + 0.15, w: 0.35, h: diagramH - 0.3,
  fill: { color: RED },
});
s.addText("Error", {
  x: errorX, y: diagramY + 0.15, w: 0.35, h: diagramH - 0.3,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Class labels
const classLabels = ["Class 1", "Class 2", "Class m"];
for (let i = 0; i < numRows; i++) {
  s.addText(classLabels[i], {
    x: classX, y: rowYs[i] - 0.05, w: 1.0, h: 0.35,
    align: "left", valign: "middle",
    fontSize: 11, color: TEXT, fontFace: FONT, margin: 0,
  });
}

// Small numbered circles (1, 2, 3) near some nodes
for (let i = 0; i < numRows; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: hiddenX - 0.2, y: rowYs[i] - 0.15, w: 0.15, h: 0.15,
    fill: { color: TEXT }, line: { color: TEXT, width: 1 },
  });
  s.addText(String(i + 1), {
    x: hiddenX - 0.2, y: rowYs[i] - 0.15, w: 0.15, h: 0.15,
    align: "center", valign: "middle",
    fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}

// ===== BOTTOM-LEFT: Two partial derivative equation lines =====
// White background area
// First equation line
s.addText(
  [
    { text: "∂E/∂w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "∂E/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k=1", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " ∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k=1", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " + ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "∂E/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k=2", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " ∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k=2", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " + ... + ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "∂E/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k=m", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " ∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k=m", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " ⋅ ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " ⋅ ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
  ],
  { x: 0.53, y: 3.2, w: 11.0, h: 0.5, margin: 0, align: "left", valign: "top" }
);

// Second equation line (simplified with summation)
s.addText(
  [
    { text: "∂E/∂w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "Σ", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "k=1..m", options: { subscript: true, fontSize: 10, color: TEXT, fontFace: FONT } },
    { text: " ∂E/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " ∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " + ∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " + ∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "Σ", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "k=1..m", options: { subscript: true, fontSize: 10, color: TEXT, fontFace: FONT } },
    { text: " -δ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "kj", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " + O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "(1-O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: ") ⋅ O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "i", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
  ],
  { x: 0.53, y: 3.8, w: 11.0, h: 0.5, margin: 0, align: "left", valign: "top" }
);

// ===== BOTTOM-RIGHT: Light yellow box with four simplified derivative equations =====
s.addShape(pptx.ShapeType.rect, {
  x: 8.0, y: 4.5, w: 5.0, h: 2.5,
  fill: { color: LIGHT_YELLOW }, line: { color: "F1C40F", width: 1 },
});

const eqYStart = 4.6;
const eqYStep = 0.55;

s.addText(
  [
    { text: "∂E/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " → ", options: { fontSize: 14, color: RED, fontFace: FONT } },
    { text: "-δ", options: { fontSize: 14, color: GREEN, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: GREEN, fontFace: FONT } },
  ],
  { x: 8.1, y: eqYStart, w: 4.8, h: 0.4, margin: 0, align: "left", valign: "top" }
);

s.addText(
  [
    { text: "Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = Σ", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "kj", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " → ", options: { fontSize: 14, color: RED, fontFace: FONT } },
    { text: "∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "kj", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
  ],
  { x: 8.1, y: eqYStart + eqYStep, w: 4.8, h: 0.4, margin: 0, align: "left", valign: "top" }
);

s.addText(
  [
    { text: "O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = 1/(1+e", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "-Net", options: { superscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, superscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: ") → ", options: { fontSize: 14, color: RED, fontFace: FONT } },
    { text: "∂O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "(1-O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: ")", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
  ],
  { x: 8.1, y: eqYStart + 2*eqYStep, w: 4.8, h: 0.4, margin: 0, align: "left", valign: "top" }
);

s.addText(
  [
    { text: "Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = Σ", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "i", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " → ", options: { fontSize: 14, color: RED, fontFace: FONT } },
    { text: "∂Net", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "/∂w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "i", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
  ],
  { x: 8.1, y: eqYStart + 3*eqYStep, w: 4.8, h: 0.4, margin: 0, align: "left", valign: "top" }
);

// ===== BOTTOM STRIP: Red box with weight update rule =====
s.addShape(pptx.ShapeType.rect, {
  x: 0.53, y: 6.3, w: 12.0, h: 0.7,
  fill: { color: LIGHT_RED }, line: { color: RED, width: 1 },
});

s.addText(
  [
    { text: "Δ", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: " = -η ", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "∂E/∂W", options: { italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "ji", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: " = Σ", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "k=1..m", options: { subscript: true, fontSize: 12, color: TEXT, fontFace: FONT } },
    { text: " δ", options: { italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: " w", options: { italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "kj", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: " ↷ O", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "(1-O", options: { italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: ") ⋅ O", options: { italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "i", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: " = η δ", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: " ⋅ O", options: { italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "i", options: { subscript: true, italic: true, fontSize: 16, color: TEXT, fontFace: FONT } },
  ],
  { x: 0.63, y: 6.35, w: 10.0, h: 0.3, margin: 0, align: "left", valign: "top" }
);

s.addText(
  [
    { text: "Where: δ", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " = Σ", options: { fontSize: 16, color: TEXT, fontFace: FONT } },
    { text: "k=1..m", options: { subscript: true, fontSize: 12, color: TEXT, fontFace: FONT } },
    { text: " δ", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "k", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " w", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "kj", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: " ⋅ O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "(1-O", options: { italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: "j", options: { subscript: true, italic: true, fontSize: 14, color: TEXT, fontFace: FONT } },
    { text: ") (for each Node j at hidden layer)", options: { fontSize: 14, color: TEXT, fontFace: FONT } },
  ],
  { x: 0.63, y: 6.65, w: 10.0, h: 0.3, margin: 0, align: "left", valign: "top" }
);

// Output file
pptx.writeFile({
  fileName: "videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_020_recreated.pptx"
}).then(() => console.log("done: slide_020_recreated.pptx"));