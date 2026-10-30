// slide_014.js — Neural Network Model (slide 14) — "Current Layer is Hidden Layer"
// Build: NODE_PATH=$(npm root -g) node slide_014.js
// Judge attempt 7 fixes: bordered panel, visible dashed arrows, thick layer arrows,
// intermediate square nodes, white eq boxes, "Error Error" text, remove Node Bias label

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 14;
const TITLE = "Neural Network Model";
const SUBTITLE = "(Current Layer is Hidden Layer)";

const FRAME_COLOR = "C00000";
const BADGE_FILL = "FFF9C4";
const BADGE_LINE = "FFF9C4";
const BADGE_TEXT = "333333";
const TITLE_COLOR = "1A1A2E";
const SUBTITLE_COLOR = "0000FF";

const EQ1 = JSON.parse(fs.readFileSync("eq1_014.json"));
const EQ2 = JSON.parse(fs.readFileSync("eq2_014.json"));
const EQ3 = JSON.parse(fs.readFileSync("eq3_014.json"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME_COLOR, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_FILL }, line: { color: BADGE_LINE, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: TITLE_COLOR, fontFace: FONT, margin: 0,
});
s.addText(SUBTITLE, {
  x: 0.6, y: 0.75, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 16, bold: true, color: SUBTITLE_COLOR, fontFace: FONT, margin: 0,
});

// ========== NETWORK PANEL (light grey rounded rect WITH thin border) ==========
const PANEL_X = 1.5;
const PANEL_Y = 1.7;
const PANEL_W = 7.2;
const PANEL_H = 3.0;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_X, y: PANEL_Y, w: PANEL_W, h: PANEL_H,
  fill: { color: "F0F0F0" }, line: { color: "AAAAAA", width: 1 },
  rectRadius: 0.05,
});

// ========== INPUT SAMPLE (purple box TOP-LEFT) ==========
const INPUT_BOX_X = 0.25;
const INPUT_BOX_Y = 1.1;
const INPUT_BOX_W = 1.1;
const INPUT_BOX_H = 0.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: INPUT_BOX_X, y: INPUT_BOX_Y, w: INPUT_BOX_W, h: INPUT_BOX_H,
  fill: { color: "D8B4E0" }, line: { color: "D8B4E0", width: 1 },
});
s.addText("Input Sample", {
  x: INPUT_BOX_X, y: INPUT_BOX_Y, w: INPUT_BOX_W, h: INPUT_BOX_H,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
// DASHED PURPLE ARROW (drawn thick and dark for visibility) from Input Sample to panel
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: INPUT_BOX_X + INPUT_BOX_W + 0.05, y: INPUT_BOX_Y + INPUT_BOX_H / 2 - 0.1,
  w: PANEL_X - (INPUT_BOX_X + INPUT_BOX_W) - 0.15, h: 0.2,
  fill: { color: "9B59B6" }, line: { color: "9B59B6", width: 1 },
  dashType: "dash",
});

// ========== TARGET LABEL (purple box TOP-RIGHT) ==========
const TARGET_BOX_X = PANEL_X + PANEL_W + 0.1;
const TARGET_BOX_Y = 1.1;
const TARGET_BOX_W = 1.1;
const TARGET_BOX_H = 0.4;
s.addShape(pres.shapes.RECTANGLE, {
  x: TARGET_BOX_X, y: TARGET_BOX_Y, w: TARGET_BOX_W, h: TARGET_BOX_H,
  fill: { color: "D8B4E0" }, line: { color: "D8B4E0", width: 1 },
});
s.addText("Target Label", {
  x: TARGET_BOX_X, y: TARGET_BOX_Y, w: TARGET_BOX_W, h: TARGET_BOX_H,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
// DASHED PURPLE ARROW from panel to Target Label
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: PANEL_X + PANEL_W + 0.1, y: TARGET_BOX_Y + TARGET_BOX_H / 2 - 0.1,
  w: TARGET_BOX_X - (PANEL_X + PANEL_W + 0.15), h: 0.2,
  fill: { color: "9B59B6" }, line: { color: "9B59B6", width: 1 },
  dashType: "dash",
});

// ========== NEURAL NETWORK LAYOUT ==========
const COL0_X = PANEL_X + 0.4;
const COL1_X = PANEL_X + 1.5;
const COL2_X = PANEL_X + 2.9;
const COL3_X = PANEL_X + 4.5;
const COL4_X = PANEL_X + 6.1;
const OUT_X   = PANEL_X + 6.9;
const COL_Y = PANEL_Y + 0.45;
const SPACING = 0.8;
const NODE_R = 0.25;
const NODES = 3;

const PURPLE = "8E44AD";
const WHITE = "FFFFFF";
const RED = "FF0000";
const BLUE = "0000FF";
const GREEN = "90EE90";
const ORANGE = "FFCC99";
const BLACK = "000000";
const RED_WEIGHT = "C0392B";
const PINK = "FF6B6B";

// Helper: full mesh
function drawMesh(colX1, colX2, nodeY, nodeR, weightColor, labelTop, labelBottom) {
  for (let i = 0; i < NODES; i++) {
    for (let j = 0; j < NODES; j++) {
      s.addShape(pres.shapes.LINE, {
        x: colX1 + nodeR, y: nodeY + i * SPACING,
        w: colX2 - (colX1 + nodeR) - nodeR, h: (j - i) * SPACING,
        line: { color: weightColor, width: 0.75, dashType: "solid" },
      });
    }
  }
  for (let i = 0; i < NODES; i++) {
    s.addText(labelTop, {
      x: (colX1 + colX2) / 2 - 0.18, y: nodeY + i * SPACING - 0.2, w: 0.4, h: 0.2,
      align: "center", valign: "middle", fontSize: 7, bold: true, color: weightColor, fontFace: FONT, margin: 0,
    });
    s.addText(labelBottom, {
      x: (colX1 + colX2) / 2 - 0.18, y: nodeY + i * SPACING + 0.02, w: 0.4, h: 0.2,
      align: "center", valign: "middle", fontSize: 7, bold: true, color: weightColor, fontFace: FONT, margin: 0,
    });
  }
}

// Helper: intermediate square node between circle and f box
function drawSquare(x, y, size, fill, border) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: x - size/2, y: y - size/2, w: size, h: size,
    fill: { color: fill }, line: { color: border, width: 1 },
  });
}

// ========== COL 0: 3 PURPLE DOTS ==========
for (let i = 0; i < NODES; i++) {
  const y = COL_Y + i * SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: COL0_X - NODE_R/2, y: y - NODE_R/2, w: NODE_R, h: NODE_R,
    fill: { color: PURPLE }, line: { color: PURPLE, width: 1 },
  });
}
drawMesh(COL0_X, COL1_X, COL_Y, NODE_R, RED_WEIGHT, "O_j w_ji", "w_ji");
s.addText("\u22EE", {
  x: COL0_X - 0.1, y: COL_Y + NODES * SPACING, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 18, color: PURPLE, fontFace: FONT, margin: 0,
});

// ========== COL 1: WHITE CIRCLES RED Σ + INTERMEDIATE SQUARES + f BOXES ==========
for (let i = 0; i < NODES; i++) {
  const y = COL_Y + i * SPACING;
  // Σ circle
  s.addShape(pres.shapes.OVAL, {
    x: COL1_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText("\u03A3", {
    x: COL1_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
  // INTERMEDIATE SQUARE NODE between circle and f box
  drawSquare(COL1_X + NODE_R + 0.12, y, 0.12, WHITE, BLACK);
  // f box
  s.addShape(pres.shapes.RECTANGLE, {
    x: COL1_X + NODE_R + 0.2, y: y - 0.12, w: 0.3, h: 0.25,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText("f", {
    x: COL1_X + NODE_R + 0.2, y: y - 0.12, w: 0.3, h: 0.25,
    align: "center", valign: "middle", fontSize: 9, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}
s.addText("\u22EE", {
  x: COL1_X - 0.05, y: COL_Y + NODES * SPACING, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 20, color: BLACK, fontFace: FONT, margin: 0,
});

// ========== COL 2: WHITE CIRCLES BLUE Σ OUTLINES + SQUARES + f BOXES ==========
for (let i = 0; i < NODES; i++) {
  const y = COL_Y + i * SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: COL2_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: WHITE }, line: { color: BLUE, width: 2 },
  });
  s.addText("\u03A3", {
    x: COL2_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: BLUE, fontFace: FONT, margin: 0,
  });
  // Net_j / O_j labels right of circle
  s.addText("Net_j", {
    x: COL2_X + NODE_R + 0.02, y: y - 0.18, w: 0.45, h: 0.18,
    align: "left", valign: "bottom", fontSize: 7, bold: true, color: RED_WEIGHT, fontFace: FONT, margin: 0,
  });
  s.addText("O_j", {
    x: COL2_X + NODE_R + 0.02, y: y + 0.0, w: 0.45, h: 0.18,
    align: "left", valign: "top", fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
  });
  // INTERMEDIATE SQUARE + f box
  drawSquare(COL2_X + NODE_R + 0.52, y, 0.12, WHITE, BLACK);
  s.addShape(pres.shapes.RECTANGLE, {
    x: COL2_X + NODE_R + 0.6, y: y - 0.12, w: 0.3, h: 0.25,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText("f", {
    x: COL2_X + NODE_R + 0.6, y: y - 0.12, w: 0.3, h: 0.25,
    align: "center", valign: "middle", fontSize: 9, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}
s.addText("\u22EE", {
  x: COL2_X - 0.05, y: COL_Y + NODES * SPACING, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 20, color: BLACK, fontFace: FONT, margin: 0,
});

// ========== MESH Col 2→3 ==========
drawMesh(COL2_X, COL3_X, COL_Y, NODE_R, RED_WEIGHT, "O_j w_kj", "w_kj");

// ========== COL 3: GREEN CIRCLES Σ + SQUARES + f BOXES ==========
for (let i = 0; i < NODES; i++) {
  const y = COL_Y + i * SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: COL3_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: GREEN }, line: { color: BLACK, width: 1 },
  });
  s.addText("\u03A3", {
    x: COL3_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
  s.addText("Net_j", {
    x: COL3_X + NODE_R + 0.02, y: y - 0.18, w: 0.45, h: 0.18,
    align: "left", valign: "bottom", fontSize: 7, bold: true, color: RED_WEIGHT, fontFace: FONT, margin: 0,
  });
  s.addText("O_j", {
    x: COL3_X + NODE_R + 0.02, y: y + 0.0, w: 0.45, h: 0.18,
    align: "left", valign: "top", fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
  });
  drawSquare(COL3_X + NODE_R + 0.12, y, 0.12, WHITE, BLACK);
  s.addShape(pres.shapes.RECTANGLE, {
    x: COL3_X + NODE_R + 0.2, y: y - 0.12, w: 0.3, h: 0.25,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText("f", {
    x: COL3_X + NODE_R + 0.2, y: y - 0.12, w: 0.3, h: 0.25,
    align: "center", valign: "middle", fontSize: 9, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}
s.addText("\u22EE", {
  x: COL3_X - 0.05, y: COL_Y + NODES * SPACING, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 20, color: BLACK, fontFace: FONT, margin: 0,
});

// ========== MESH Col 3→4 ==========
drawMesh(COL3_X, COL4_X, COL_Y, NODE_R, RED_WEIGHT, "O_k w_kl", "w_kl");

// ========== COL 4: ORANGE CIRCLES Σ + SQUARES + f BOXES ==========
for (let i = 0; i < NODES; i++) {
  const y = COL_Y + i * SPACING;
  s.addShape(pres.shapes.OVAL, {
    x: COL4_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: ORANGE }, line: { color: BLACK, width: 1 },
  });
  s.addText("\u03A3", {
    x: COL4_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
  s.addText("Net_k", {
    x: COL4_X + NODE_R + 0.02, y: y - 0.18, w: 0.45, h: 0.18,
    align: "left", valign: "bottom", fontSize: 7, bold: true, color: RED_WEIGHT, fontFace: FONT, margin: 0,
  });
  s.addText("O_k", {
    x: COL4_X + NODE_R + 0.02, y: y + 0.0, w: 0.45, h: 0.18,
    align: "left", valign: "top", fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
  });
  drawSquare(COL4_X + NODE_R + 0.12, y, 0.12, WHITE, BLACK);
  s.addShape(pres.shapes.RECTANGLE, {
    x: COL4_X + NODE_R + 0.2, y: y - 0.12, w: 0.3, h: 0.25,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText("f", {
    x: COL4_X + NODE_R + 0.2, y: y - 0.12, w: 0.3, h: 0.25,
    align: "center", valign: "middle", fontSize: 9, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}
s.addText("\u22EE", {
  x: COL4_X - 0.05, y: COL_Y + NODES * SPACING, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 20, color: BLACK, fontFace: FONT, margin: 0,
});

// ========== OUTPUT LABELS ==========
for (let i = 0; i < NODES; i++) {
  const y = COL_Y + i * SPACING;
  s.addShape(pres.shapes.LINE, {
    x: COL4_X + NODE_R + 0.35, y: y,
    w: OUT_X - (COL4_X + NODE_R + 0.35), h: 0,
    line: { color: PINK, width: 1, dashType: "dash" },
  });
  s.addText(i === 2 ? "Output m" : `Output ${i + 1}`, {
    x: OUT_X, y: y - 0.1, w: 1.0, h: 0.3,
    align: "left", valign: "middle", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ========== ERROR BAR ("Error Error" stacked, clean) ==========
const ERR_X = OUT_X + 1.35;
s.addShape(pres.shapes.RECTANGLE, {
  x: ERR_X, y: PANEL_Y + 0.15, w: 0.18, h: PANEL_H - 0.3,
  fill: { color: "8B0000" }, line: { color: "8B0000", width: 1 },
});
s.addText([
  { text: "Error", options: { breakLine: true } },
  { text: "Error", options: {} },
], {
  x: ERR_X - 0.12, y: PANEL_Y + 0.15, w: 0.42, h: PANEL_H - 0.3,
  align: "center", valign: "middle", rot: 270,
  fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// ========== CLASS LABELS ==========
const CLASS_X = ERR_X + 0.3;
for (let i = 0; i < NODES; i++) {
  const y = PANEL_Y + 0.35 + i * 0.75;
  s.addShape(pres.shapes.RECTANGLE, {
    x: CLASS_X, y: y, w: 1.2, h: 0.5,
    fill: { color: "C8E6C9" }, line: { color: BLACK, width: 1 },
  });
  s.addText(i === 2 ? "Class m" : `Class ${i + 1}`, {
    x: CLASS_X, y: y, w: 1.2, h: 0.5,
    align: "center", valign: "middle", fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// ========== CIRCLED "1" (bias markers, NO "Node Bias" label) ==========
const BIAS_Y = COL_Y + (NODES - 1) * SPACING + 0.35;
s.addShape(pres.shapes.OVAL, {
  x: COL1_X - 0.35, y: BIAS_Y - 0.12, w: 0.25, h: 0.25,
  fill: { type: "none" }, line: { color: PURPLE, width: 2 },
});
s.addText("1", {
  x: COL1_X - 0.35, y: BIAS_Y - 0.12, w: 0.25, h: 0.25,
  align: "center", valign: "middle", fontSize: 9, bold: true, color: PURPLE, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.OVAL, {
  x: COL2_X - 0.35, y: BIAS_Y - 0.12, w: 0.25, h: 0.25,
  fill: { type: "none" }, line: { color: PURPLE, width: 2 },
});
s.addText("1", {
  x: COL2_X - 0.35, y: BIAS_Y - 0.12, w: 0.25, h: 0.25,
  align: "center", valign: "middle", fontSize: 9, bold: true, color: PURPLE, fontFace: FONT, margin: 0,
});

// ========== BOTTOM ANNOTATION STRIP ==========
const BOX_Y = PANEL_Y + PANEL_H + 0.3;
const BOX_H = 1.1;
const SMALL_BOX_H = 0.6;

// Box 1: For Layer "j" (WHITE fill per judge)
const B1_X = 0.6;
const B1_W = 2.5;
s.addShape(pres.shapes.RECTANGLE, {
  x: B1_X, y: BOX_Y, w: B1_W, h: BOX_H,
  fill: { color: "FFFFFF" }, line: { color: PINK, width: 1 },
});
s.addText('For Layer "j"', {
  x: B1_X, y: BOX_Y, w: B1_W, h: 0.25,
  align: "left", valign: "top", fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0.05,
});
const eq1_y = BOX_Y + 0.35 - EQ1.baseline_frac * EQ1.h_in;
s.addImage({ path: "eq1_014.png", x: B1_X + 0.1, y: eq1_y, w: EQ1.w_in, h: EQ1.h_in });
const eq2_y = BOX_Y + 0.7 - EQ2.baseline_frac * EQ2.h_in;
s.addImage({ path: "eq2_014.png", x: B1_X + 0.1, y: eq2_y, w: EQ2.w_in, h: EQ2.h_in });

// Box 2: Previous Layer — BLUE DOWN-ARROW above (thick colored)
const B2_X = B1_X + B1_W + 0.15;
const B2_W = 1.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: B2_X, y: BOX_Y, w: B2_W, h: SMALL_BOX_H,
  fill: { color: "FFFFFF" }, line: { color: PINK, width: 1 },
});
s.addShape(pres.shapes.DOWN_ARROW, {  // BLUE DOWN-ARROW
  x: B2_X + B2_W / 2 - 0.15, y: BOX_Y - 0.55, w: 0.3, h: 0.5,
  fill: { color: "2980B9" }, line: { color: "2980B9", width: 1 },
});
s.addText("Previous Layer\n(l)", {
  x: B2_X, y: BOX_Y, w: B2_W, h: SMALL_BOX_H,
  align: "center", valign: "middle", fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0.05,
});

// Box 3: Current Layer — GREEN UP-ARROW above
const B3_X = B2_X + B2_W + 0.15;
const B3_W = 2.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: B3_X, y: BOX_Y, w: B3_W, h: SMALL_BOX_H,
  fill: { color: "FFFFFF" }, line: { color: PINK, width: 1 },
});
s.addShape(pres.shapes.UP_ARROW, {  // GREEN UP-ARROW
  x: B3_X + B3_W / 2 - 0.15, y: BOX_Y - 0.55, w: 0.3, h: 0.5,
  fill: { color: "27AE60" }, line: { color: "27AE60", width: 1 },
});
s.addText("Current Layer\n(You are here)", {
  x: B3_X, y: BOX_Y, w: B3_W, h: SMALL_BOX_H,
  align: "center", valign: "middle", fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0.05,
});

// Box 4: Next Layer — ORANGE UP-ARROW above
const B4_X = B3_X + B3_W + 0.15;
const B4_W = 1.5;
s.addShape(pres.shapes.RECTANGLE, {
  x: B4_X, y: BOX_Y, w: B4_W, h: SMALL_BOX_H,
  fill: { color: "FFFFFF" }, line: { color: PINK, width: 1 },
});
s.addShape(pres.shapes.UP_ARROW, {  // ORANGE UP-ARROW
  x: B4_X + B4_W / 2 - 0.15, y: BOX_Y - 0.55, w: 0.3, h: 0.5,
  fill: { color: "E67E22" }, line: { color: "E67E22", width: 1 },
});
s.addText("Next Layer\n(K)", {
  x: B4_X, y: BOX_Y, w: B4_W, h: SMALL_BOX_H,
  align: "center", valign: "middle", fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0.05,
});

// Box 5: Note — white with pink border
const B5_X = B4_X + B4_W + 0.15;
const B5_W = 2.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: B5_X, y: BOX_Y, w: B5_W, h: SMALL_BOX_H,
  fill: { color: "FFFFFF" }, line: { color: PINK, width: 1 },
});
s.addText([
  { text: "Note: Layer \"j\" is ", options: { bold: false, fontFace: "Georgia" } },
  { text: "NOT", options: { bold: true, fontFace: "Georgia" } },
  { text: " Output Layer", options: { bold: false, fontFace: "Georgia" } },
], {
  x: B5_X, y: BOX_Y, w: B5_W, h: SMALL_BOX_H,
  align: "center", valign: "middle", fontSize: 10, color: PINK, fontFace: "Georgia", margin: 0.05,
});

// Box 6: Error equation — white, X's right
const B6_X = ERR_X - 0.1;
const B6_Y = BOX_Y + SMALL_BOX_H + 0.15;
const B6_W = 2.3;
const B6_H = 0.6;
s.addShape(pres.shapes.RECTANGLE, {
  x: B6_X, y: B6_Y, w: B6_W, h: B6_H,
  fill: { color: "FFFFFF" }, line: { color: PINK, width: 1 },
});
const eq3_y = B6_Y + 0.2 - EQ3.baseline_frac * EQ3.h_in;
s.addImage({ path: "eq3_014.png", x: B6_X + 0.1, y: eq3_y, w: EQ3.w_in, h: EQ3.h_in });
s.addText("X X X", {
  x: B6_X + EQ3.w_in + 0.15, y: B6_Y + 0.1, w: 1.0, h: 0.4,
  align: "left", valign: "middle", fontSize: 18, bold: true, color: "FF0000", fontFace: FONT, margin: 0,
});

// ========== WRITE FILE ==========
pres.writeFile({ fileName: "slide_014_recreated.pptx" })
  .then(() => console.log("wrote slide_014_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });