// Slide 7 build: Neural Network Model (attempt 4)
// House chrome + neural network diagram + 3 equations + 4 highlight boxes + inner beige panel
// Run: NODE_PATH=$(npm root -g) node slide_007.js  -> slide_007.pptx

const fs = require("fs");
const pptxgen = require("pptxgenjs");

const FONT = "Arial";
const NUM = 7;
const TITLE = "Neural Network Model";
const SUBTITLE = "(Weights of Output Layer AFFECTS Calculated Error)";

// Slide dimensions
const W = 13.33, H = 7.5;
const FRAME_X = 0.15, FRAME_Y = 0.15;
const FRAME_W = W - 0.3, FRAME_H = H - 0.3;

// Inner beige panel (from original) - inset from red frame
const PANEL_INSET = 0.15;  // inner panel inset from red frame
const PANEL_X = FRAME_X + PANEL_INSET;
const PANEL_Y = FRAME_Y + PANEL_INSET + 0.85;  // below title area
const PANEL_W = FRAME_W - 2 * PANEL_INSET;
const PANEL_H = FRAME_H - 2 * PANEL_INSET - 0.85 - 1.3;  // leave room for bottom boxes

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ==================== HOUSE CHROME (pattern: house-chrome) ====================

// 1. Outer red frame
s.addShape(pres.shapes.RECTANGLE, {
  x: FRAME_X, y: FRAME_Y, w: FRAME_W, h: FRAME_H,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Inner beige panel (content area background)
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL_X, y: PANEL_Y, w: PANEL_W, h: PANEL_H,
  fill: { color: "DCD6CC" },  // beige from original (DC D6 CC)
  line: { type: "none" },
});

// 3. Slide-number badge (yellow oval)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 4. Title box
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C0392B", fontFace: FONT, margin: 0,
});

// 5. Subtitle box - with AFFECTS in italic
s.addText([
  { text: "(Weights of Output Layer ", options: { italic: false } },
  { text: "AFFECTS", options: { italic: true } },
  { text: " Calculated Error)", options: { italic: false } }
], {
  x: 0.6, y: 0.72, w: 12.13, h: 0.4,
  align: "center", valign: "top",
  fontSize: 14, bold: false, color: "2980B9", fontFace: FONT, margin: 0,
});

// ==================== NEURAL NETWORK DIAGRAM ====================
// Layout strategy: Measure from original 960x540 image, scale to 13.33x7.5 in
// Key regions (inside panel PANEL_X..PANEL_X+PANEL_W, PANEL_Y..PANEL_Y+PANEL_H)

// Helper: convert image px to inches (960x540 -> 13.03x7.2 content area inside frame)
// frame content: 13.03 in wide x 7.2 in tall
// image: 960 px wide x 540 px tall
const PX_TO_IN_X = 13.03 / 960;
const PX_TO_IN_Y = 7.2 / 540;

// Panel origin (content area)
const CONTENT_X = PANEL_X;
const CONTENT_Y = PANEL_Y;

// ---- Diagram dimensions from image measurement ----
// Diagram starts ~y=1.3 from frame top = PANEL_Y - 0.45? 
// Let's use image-relative: title ends ~y=85px (1.13in), panel starts ~y=100px (1.33in)
// Diagram rows: Row 1 y=150px (2.0in), Row 2 y=270px (3.6in), Row 3 y=390px (5.2in)
// Bottom boxes start ~y=450px (6.0in)

const COL1_X = CONTENT_X + 150 * PX_TO_IN_X;  // ~2.18
const COL2_X = CONTENT_X + 380 * PX_TO_IN_X;  // ~5.16
const COL3_X = CONTENT_X + 620 * PX_TO_IN_X;  // ~8.41
const ERR_X  = CONTENT_X + 780 * PX_TO_IN_X;  // ~10.58
const CLASS_X = CONTENT_X + 830 * PX_TO_IN_X; // ~11.26

// Target Label box (top-right)
const TARGET_BOX_X = CONTENT_X + 760 * PX_TO_IN_X;  // ~10.3
const TARGET_BOX_Y = CONTENT_Y + 10 * PX_TO_IN_Y;   // ~0.13
const TARGET_BOX_W = 100 * PX_TO_IN_X;  // ~1.35
const TARGET_BOX_H = 40 * PX_TO_IN_Y;   // ~0.53

// Row Y positions relative to CONTENT_Y (which is ~PANEL_Y ~1.0in from frame top)
// In image: y=150,270,390 -> relative to panel top (y~100): 50, 170, 290 px
// 50*7.2/540=0.67in, 170*7.2/540=2.27in, 290*7.2/540=3.87in
const ROW1_Y = CONTENT_Y + 50 * PX_TO_IN_Y;   // ~0.67 from panel top
const ROW2_Y = CONTENT_Y + 170 * PX_TO_IN_Y;  // ~2.27
const ROW3_Y = CONTENT_Y + 290 * PX_TO_IN_Y;  // ~3.87
const COL1_ROWS = [ROW1_Y, ROW2_Y, ROW3_Y];
const COL2_ROWS = [ROW1_Y, ROW2_Y, ROW3_Y];
const COL3_ROWS = [ROW1_Y, ROW2_Y, ROW3_Y];

const NODE_R = 0.28;  // node radius in inches
const SIGMA_SIZE = 18; // pt

// ---- Input Sample box (purple rounded rect at top-left) ----
// Original: x~77-120, y~53-122 -> relative to panel: x~30-70px, y~0-30px from panel top
const INPUT_BOX_X = CONTENT_X + 30 * PX_TO_IN_X;  // ~0.4
const INPUT_BOX_Y = CONTENT_Y + 5 * PX_TO_IN_Y;   // ~0.07
const INPUT_BOX_W = 90 * PX_TO_IN_X;   // ~1.22
const INPUT_BOX_H = 40 * PX_TO_IN_Y;   // ~0.53

// Input Sample box (purple)
s.addShape(pres.shapes.RECTANGLE, {
  x: INPUT_BOX_X, y: INPUT_BOX_Y, w: INPUT_BOX_W, h: INPUT_BOX_H,
  fill: { color: "8E44AD" }, line: { color: "8E44AD", width: 0 },
});
s.addText("Input Sample", {
  x: INPUT_BOX_X, y: INPUT_BOX_Y, w: INPUT_BOX_W, h: INPUT_BOX_H,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Input dots (purple) - below the box: THREE dots (matching 3 rows), aligned with rows
const INPUT_DOTS_X = INPUT_BOX_X + INPUT_BOX_W/2 - 0.06;
const INPUT_DOTS_Y = INPUT_BOX_Y + INPUT_BOX_H + 0.1;
for (let i = 0; i < 3; i++) {  // THREE dots, one per row
  s.addShape(pres.shapes.OVAL, {
    x: INPUT_DOTS_X, y: INPUT_DOTS_Y + i * (ROW2_Y - ROW1_Y), w: 0.12, h: 0.12,
    fill: { color: "8E44AD" }, line: { color: "8E44AD", width: 0 },
  });
}

// Connector lines from each input dot to corresponding left column node (1-to-1)
for (let i = 0; i < 3; i++) {
  const dotY = INPUT_DOTS_Y + i * (ROW2_Y - ROW1_Y);
  const nodeY = COL1_ROWS[i];
  s.addShape(pres.shapes.LINE, {
    x: INPUT_DOTS_X + 0.06, y: dotY + 0.06,
    w: COL1_X - NODE_R - (INPUT_DOTS_X + 0.06), h: nodeY - dotY,
    line: { color: "8E44AD", width: 0.75, dashType: "sysDash" },
  });
}

// Arrow from input box to first column (purple arrow per original) - main trunk
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: INPUT_BOX_X + INPUT_BOX_W, y: INPUT_BOX_Y + INPUT_BOX_H/2 - 0.075, w: COL1_X - NODE_R - (INPUT_BOX_X + INPUT_BOX_W), h: 0.15,
  fill: { color: "8E44AD" }, line: { color: "8E44AD", width: 1 },
});

// Top horizontal purple dashed line (from Input Sample toward Target Label area)
const TOP_ARROW_Y = INPUT_BOX_Y + INPUT_BOX_H/2;
s.addShape(pres.shapes.LINE, {
  x: INPUT_BOX_X + INPUT_BOX_W, y: TOP_ARROW_Y,
  w: TARGET_BOX_X - (INPUT_BOX_X + INPUT_BOX_W), h: 0,
  line: { color: "8E44AD", width: 0.75, dashType: "sysDash" },
});

// ---- Column 1: White nodes with red Sigma (outlined, not filled) ----
for (let i = 0; i < COL1_ROWS.length; i++) {
  const y = COL1_ROWS[i];
  // White circle with red outline (matching original's outlined style)
  s.addShape(pres.shapes.OVAL, {
    x: COL1_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: "FFFFFF" }, line: { color: "C0392B", width: 2 },
  });
  // Red Sigma
  s.addText("Σ", {
    x: COL1_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle",
    fontSize: SIGMA_SIZE, bold: true, color: "C0392B", fontFace: "Symbol", margin: 0,
  });
  // f[] box to the right
  s.addShape(pres.shapes.RECTANGLE, {
    x: COL1_X + NODE_R + 0.05, y: y - 0.12, w: 0.3, h: 0.24,
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
  });
  s.addText("f", {
    x: COL1_X + NODE_R + 0.05, y: y - 0.12, w: 0.3, h: 0.24,
    align: "center", valign: "middle",
    fontSize: 10, bold: true, italic: true, color: "000000", fontFace: FONT, margin: 0,
  });
  // Three fan-out circles "o o o" after the f[] box
  for (let d = 0; d < 3; d++) {
    s.addShape(pres.shapes.OVAL, {
      x: COL1_X + NODE_R + 0.4 + d * 0.15, y: y - 0.06, w: 0.12, h: 0.12,
      fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.5 },
    });
  }
}
// Ellipsis after column 1
s.addText("...", {
  x: COL1_X + NODE_R + 0.4, y: ROW2_Y - 0.1, w: 0.2, h: 0.2,
  align: "center", fontSize: 14, color: "000000", fontFace: FONT, margin: 0,
});

// ---- Column 2: Blue nodes with Sigma (outlined style) ----
for (let i = 0; i < COL2_ROWS.length; i++) {
  const y = COL2_ROWS[i];
  // Blue circle with outline, transparent fill
  s.addShape(pres.shapes.OVAL, {
    x: COL2_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: "FFFFFF" }, line: { color: "2980B9", width: 2 },
  });
  // Sigma (blue)
  s.addText("Σ", {
    x: COL2_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle",
    fontSize: SIGMA_SIZE, bold: true, color: "2980B9", fontFace: "Symbol", margin: 0,
  });
  // Net_j (red) and O_j (black) labels to the right
  s.addText("Net_j", {
    x: COL2_X + NODE_R + 0.05, y: y - 0.25, w: 0.5, h: 0.2,
    align: "left", fontSize: 9, bold: true, color: "C0392B", fontFace: FONT, margin: 0,
  });
  s.addText("O_j", {
    x: COL2_X + NODE_R + 0.05, y: y - 0.05, w: 0.5, h: 0.2,
    align: "left", fontSize: 9, color: "000000", fontFace: FONT, margin: 0,
  });
  // f[] box (simple "f" text, no decoration)
  s.addShape(pres.shapes.RECTANGLE, {
    x: COL2_X + NODE_R + 0.55, y: y - 0.12, w: 0.3, h: 0.24,
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
  });
  s.addText("f", {
    x: COL2_X + NODE_R + 0.55, y: y - 0.12, w: 0.3, h: 0.24,
    align: "center", valign: "middle",
    fontSize: 10, bold: true, italic: true, color: "000000", fontFace: FONT, margin: 0,
  });
}

// ---- Column 3: Green nodes with Sigma (outlined style) ----
for (let i = 0; i < COL3_ROWS.length; i++) {
  const y = COL3_ROWS[i];
  // Green circle with outline, transparent fill
  s.addShape(pres.shapes.OVAL, {
    x: COL3_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: "FFFFFF" }, line: { color: "27AE60", width: 2 },
  });
  // Sigma (green)
  s.addText("Σ", {
    x: COL3_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle",
    fontSize: SIGMA_SIZE, bold: true, color: "27AE60", fontFace: "Symbol", margin: 0,
  });
  // f[] box immediately to the right of sigma node
  s.addShape(pres.shapes.RECTANGLE, {
    x: COL3_X + NODE_R + 0.05, y: y - 0.12, w: 0.3, h: 0.24,
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
  });
  s.addText("f", {
    x: COL3_X + NODE_R + 0.05, y: y - 0.12, w: 0.3, h: 0.24,
    align: "center", valign: "middle",
    fontSize: 10, bold: true, italic: true, color: "000000", fontFace: FONT, margin: 0,
  });
  // O_j label to the right of f[] box
  s.addText("O_j", {
    x: COL3_X + NODE_R + 0.4, y: y - 0.1, w: 0.5, h: 0.2,
    align: "left", fontSize: 9, color: "000000", fontFace: FONT, margin: 0,
  });
  // Arrow from O_j to Output label
  s.addShape(pres.shapes.RIGHT_ARROW, {
    x: COL3_X + NODE_R + 0.85, y: y + 0.02, w: 0.4, h: 0.15,
    fill: { color: "000000" }, line: { color: "000000", width: 1 },
  });
  // Output labels to the right
  const outLabels = ["Output 1", "Output 2", "Output m"];
  s.addText(outLabels[i], {
    x: COL3_X + NODE_R + 1.3, y: y - 0.1, w: 0.6, h: 0.2,
    align: "left", fontSize: 10, color: "000000", fontFace: FONT, margin: 0,
  });
}

// ---- Dense mesh of weight arrows between col2 and col3 (crossing curved) ----
// Original shows multiple crossing curved arrows with w_ji labels
// Draw curved lines from each col2 node to each col3 node
for (let i = 0; i < COL2_ROWS.length; i++) {
  for (let j = 0; j < COL3_ROWS.length; j++) {
    const y1 = COL2_ROWS[i];
    const y2 = COL3_ROWS[j];
    const startX = COL2_X + NODE_R + 0.85;
    const startY = y1;
    const endX = COL3_X - NODE_R;
    const endY = y2;
    // Use lines as approximation for curved arrows
    s.addShape(pres.shapes.LINE, {
      x: startX, y: startY, w: endX - startX, h: endY - startY,
      line: { color: "2980B9", width: 1, dashType: "sysDash", endArrowType: "triangle" },
    });
    // w_ji label at midpoint
    const mx = (startX + endX) / 2;
    const my = (startY + endY) / 2;
    s.addText("w_ji", {
      x: mx - 0.2, y: my - 0.15, w: 0.4, h: 0.2,
      align: "center", fontSize: 7, color: "2980B9", fontFace: FONT, margin: 0,
    });
  }
}

// ---- Target Label box at top-right (geometry defined above) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: TARGET_BOX_X, y: TARGET_BOX_Y, w: TARGET_BOX_W, h: TARGET_BOX_H,
  fill: { color: "8E44AD" }, line: { color: "8E44AD", width: 0 },
});
s.addText("Target Label", {
  x: TARGET_BOX_X, y: TARGET_BOX_Y, w: TARGET_BOX_W, h: TARGET_BOX_H,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Black curved dashed arrows from output region to Target Label
// Use curved approximation with multiple line segments
for (let i = 0; i < COL3_ROWS.length; i++) {
  const y = COL3_ROWS[i];
  const startX = COL3_X + NODE_R + 1.25;
  const startY = y;
  const endX = TARGET_BOX_X;
  const endY = TARGET_BOX_Y + TARGET_BOX_H/2;
  // Draw a curved path using two line segments (approximation)
  const midX = (startX + endX) / 2;
  const midY = startY - 0.3;  // curve upward
  s.addShape(pres.shapes.LINE, {
    x: startX, y: startY, w: midX - startX, h: midY - startY,
    line: { color: "000000", width: 1, dashType: "sysDash" },
  });
  s.addShape(pres.shapes.LINE, {
    x: midX, y: midY, w: endX - midX, h: endY - midY,
    line: { color: "000000", width: 1, dashType: "sysDash", endArrowType: "triangle" },
  });
}

// ---- Yellow w_ji circles above connections to col3 ----
for (let i = 0; i < COL3_ROWS.length; i++) {
  const y = COL3_ROWS[i];
  const wx = (COL2_X + NODE_R + 0.85 + COL3_X - NODE_R) / 2;
  s.addShape(pres.shapes.OVAL, {
    x: wx - 0.18, y: y - 0.5, w: 0.36, h: 0.36,
    fill: { color: "F1C40F" }, line: { color: "BF8F00", width: 1 },
  });
  s.addText("w_ji", {
    x: wx - 0.18, y: y - 0.5, w: 0.36, h: 0.36,
    align: "center", valign: "middle",
    fontSize: 8, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
}

// ---- Blue w_ji on diagonal connections from col1 to col2 ----
for (let i = 0; i < COL2_ROWS.length; i++) {
  const y = COL2_ROWS[i];
  const wx = (COL1_X + NODE_R + 0.35 + COL2_X - NODE_R) / 2;
  s.addText("w_ji", {
    x: wx - 0.2, y: y - 0.4, w: 0.4, h: 0.2,
    align: "center", fontSize: 8, color: "2980B9", fontFace: FONT, margin: 0,
  });
}

// ---- Purple circled "1" annotations (Node Bias badge) ----
// Position away from f[] boxes to avoid collision
const ann1_x = CONTENT_X + 130 * PX_TO_IN_X;  // measured from PIL
const ann1_y = CONTENT_Y + 320 * PX_TO_IN_Y;  // lower, away from f[]
const ann2_x = CONTENT_X + 450 * PX_TO_IN_X;
const ann2_y = CONTENT_Y + 320 * PX_TO_IN_Y;

for (const [ax, ay] of [[ann1_x, ann1_y], [ann2_x, ann2_y]]) {
  s.addShape(pres.shapes.OVAL, {
    x: ax - 0.12, y: ay - 0.12, w: 0.24, h: 0.24,
    fill: { color: "8E44AD" }, line: { color: "8E44AD", width: 0 },
  });
  s.addText("1", {
    x: ax - 0.12, y: ay - 0.12, w: 0.24, h: 0.24,
    align: "center", valign: "middle",
    fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}

// ---- "Node Bias" label near first circled 1 ----
s.addText("Node Bias", {
  x: ann1_x - 0.5, y: ann1_y + 0.15, w: 1.0, h: 0.2,
  align: "center", fontSize: 9, color: "000000", fontFace: FONT, margin: 0,
});

// ---- Up-arrow with i/j labels above middle bottom boxes (not circular badges) ----
// "Previous Layer" box center x, "Current Layer" box center x
const BADGE_I_X = CONTENT_X + 280 * PX_TO_IN_X;  // ~3.8
const BADGE_I_Y = CONTENT_Y + 340 * PX_TO_IN_Y;  // ~4.5
const BADGE_J_X = CONTENT_X + 500 * PX_TO_IN_X;  // ~6.8
const BADGE_J_Y = CONTENT_Y + 340 * PX_TO_IN_Y;

// Up arrow with "i" label - BLUE (matching "Previous Layer" box)
s.addShape(pres.shapes.UP_ARROW, {
  x: BADGE_I_X - 0.1, y: BADGE_I_Y - 0.25, w: 0.2, h: 0.25,
  fill: { color: "2980B9" }, line: { color: "2980B9", width: 1 },
});
s.addText("i", {
  x: BADGE_I_X - 0.15, y: BADGE_I_Y - 0.35, w: 0.3, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Up arrow with "j" label - GREEN (matching "Current Layer" box)
s.addShape(pres.shapes.UP_ARROW, {
  x: BADGE_J_X - 0.1, y: BADGE_J_Y - 0.25, w: 0.2, h: 0.25,
  fill: { color: "27AE60" }, line: { color: "27AE60", width: 1 },
});
s.addText("j", {
  x: BADGE_J_X - 0.15, y: BADGE_J_Y - 0.35, w: 0.3, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// ---- Error bar (vertical dark red) ----
// Bar width: 0.3in (original ~0.28in) to fit "Error" text at 6pt without wrap
s.addShape(pres.shapes.RECTANGLE, {
  x: ERR_X, y: ROW1_Y - 0.1, w: 0.3, h: ROW3_Y - ROW1_Y + 0.5,
  fill: { color: "C0392B" }, line: { color: "C0392B", width: 0 },
});
// "Error" repeated 3 times vertically - use 6pt font to fit in 0.3in box
const ERR_TEXT_W = 0.3;
const ERR_TEXT_H = 0.3;
s.addText("Error", {
  x: ERR_X, y: ROW1_Y + 0.15, w: ERR_TEXT_W, h: ERR_TEXT_H,
  align: "center", valign: "middle",
  fontSize: 6, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("Error", {
  x: ERR_X, y: ROW2_Y + 0.15, w: ERR_TEXT_W, h: ERR_TEXT_H,
  align: "center", valign: "middle",
  fontSize: 6, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("Error", {
  x: ERR_X, y: ROW3_Y + 0.15, w: ERR_TEXT_W, h: ERR_TEXT_H,
  align: "center", valign: "middle",
  fontSize: 6, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// ---- Class boxes (light green) ----
const CLASS_Y = [ROW1_Y - 0.1, ROW2_Y - 0.1, ROW3_Y - 0.1];
const CLASS_LABELS = ["Class 1", "Class 2", "Class m"];
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: CLASS_X, y: CLASS_Y[i], w: 0.8, h: 0.3,
    fill: { color: "D5F5E3" }, line: { color: "27AE60", width: 1 },
  });
  s.addText(CLASS_LABELS[i], {
    x: CLASS_X, y: CLASS_Y[i], w: 0.8, h: 0.3,
    align: "center", valign: "middle",
    fontSize: 10, color: "000000", fontFace: FONT, margin: 0,
  });
}

// ==================== BOTTOM ANNOTATION BOXES (pattern: highlight-box) ====================
// Four boxes at bottom: white/cream fills per original
const BOX_Y = CONTENT_Y + 350 * PX_TO_IN_Y;  // ~4.67 from panel top
const BOX_H = 1.2;
const BOX_GAP = 0.05;

const BOX_FILL_CREAM = "FDF2E9";
const BOX_FILL_GREEN = "D5F5E3";
const BOX_BORDER_CREAM = "BF8F00";
const BOX_BORDER_GREEN = "27AE60";

// Box 1: For Layer "j" (left) - cream bg, two equations
const BOX1_X = CONTENT_X + 0.2;
const BOX1_W = 3.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: BOX1_X, y: BOX_Y, w: BOX1_W, h: BOX_H,
  fill: { color: BOX_FILL_CREAM }, line: { color: BOX_BORDER_CREAM, width: 1 },
});
s.addText('For Layer "j"', {  // no trailing colon per original
  x: BOX1_X + 0.1, y: BOX_Y + 0.05, w: BOX1_W - 0.2, h: 0.25,
  align: "left", fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// Embed equation 1: Net_j = Σ (w_ji · O_i)
const eq1 = JSON.parse(fs.readFileSync("eq_net_j.json"));
const eq1_y = BOX_Y + 0.3 - eq1.baseline_frac * eq1.h_in;
s.addImage({ path: "eq_net_j.png", x: BOX1_X + 0.1, y: eq1_y, w: eq1.w_in, h: eq1.h_in });

// Embed equation 2: O_j = f(Net_j) = 1/(1+e^-Net_j)
const eq2 = JSON.parse(fs.readFileSync("eq_o_j.json"));
const eq2_y = BOX_Y + 0.75 - eq2.baseline_frac * eq2.h_in;
s.addImage({ path: "eq_o_j.png", x: BOX1_X + 0.1, y: eq2_y, w: eq2.w_in, h: eq2.h_in });

// Box 2: Previous Layer Layer (0) - cream bg, up arrow
const BOX2_X = BOX1_X + BOX1_W + BOX_GAP;
const BOX2_W = 2.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: BOX2_X, y: BOX_Y, w: BOX2_W, h: BOX_H,
  fill: { color: BOX_FILL_CREAM }, line: { color: BOX_BORDER_CREAM, width: 1 },
});
s.addText('Previous Layer Layer (0)', {
  x: BOX2_X + 0.1, y: BOX_Y + 0.5, w: BOX2_W - 0.2, h: 0.3,
  align: "center", fontSize: 11, color: "000000", fontFace: FONT, margin: 0,
});

// Box 3: Current Layer is Output Layer (You are here) - light green bg
const BOX3_X = BOX2_X + BOX2_W + BOX_GAP;
const BOX3_W = 3.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: BOX3_X, y: BOX_Y, w: BOX3_W, h: BOX_H,
  fill: { color: BOX_FILL_GREEN }, line: { color: BOX_BORDER_GREEN, width: 1 },
});
s.addText('Current Layer is Output Layer (You are here)', {
  x: BOX3_X + 0.1, y: BOX_Y + 0.5, w: BOX3_W - 0.2, h: 0.3,
  align: "center", fontSize: 11, color: "000000", fontFace: FONT, margin: 0,
});

// Box 4: If Layer "j" is Output Layer: - cream bg, one equation
const BOX4_X = BOX3_X + BOX3_W + BOX_GAP;
const BOX4_W = CONTENT_X + PANEL_W - BOX4_X - 0.1; // fill to panel right edge
s.addShape(pres.shapes.RECTANGLE, {
  x: BOX4_X, y: BOX_Y, w: BOX4_W, h: BOX_H,
  fill: { color: BOX_FILL_CREAM }, line: { color: BOX_BORDER_CREAM, width: 1 },
});
s.addText('If Layer "j" is Output Layer:', {
  x: BOX4_X + 0.1, y: BOX_Y + 0.05, w: BOX4_W - 0.2, h: 0.25,
  align: "left", fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
// Embed error equation
const eq3 = JSON.parse(fs.readFileSync("eq_error.json"));
const eq3_y = BOX_Y + 0.6 - eq3.baseline_frac * eq3.h_in;
s.addImage({ path: "eq_error.png", x: BOX4_X + 0.1, y: eq3_y, w: eq3.w_in, h: eq3.h_in });

// ==================== WRITE ====================
pres.writeFile({ fileName: "slide_007.pptx" })
  .then(() => console.log("wrote slide_007.pptx"))
  .catch(e => { console.error(e); process.exit(1); });