const pptxgen = require("pptxgenjs");

// Slide 015: Using Two Perceptron Layers with non-Linearity
const NUM = 15;
const TITLE = "Using Two Perceptron Layers with non-Linearity";
const FONT = "Arial";

const BG = "E8E8E8";
const BORDER_RED = "8B0000";
const BLACK = "000000";
const RED = "FF0000";
const DARK_RED = "C00000";
const GREEN = "00B050";
const BLUE = "0000FF";
const PURPLE = "D2B48C";
const YELLOW = "FFF9C4";
const WHITE = "FFFFFF";
const CYAN = "00FFFF";
const LIGHT_GREEN = "90EE90";
const LIGHT_YELLOW = "FFFFE0";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Bottom black bar - video player overlay
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

// 3. Slide-number badge - HOUSE CHROME LAW
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 4. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
// Title has mixed colors: "Using Two Perceptron Layers with" in red, "non-Linearity" in blue
s.addText([
  { text: "Using Two Perceptron Layers with ", options: { color: RED, bold: true, fontSize: 28, fontFace: FONT } },
  { text: "non-Linearity", options: { color: BLUE, bold: true, fontSize: 28, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

// ============================================================
// MAIN DIAGRAM: Two-layer perceptron with non-linearity (upper-left/center, blue-bordered)
// ============================================================
const MD_X = 0.6, MD_Y = 1.0, MD_W = 8.5, MD_H = 3.5;

// White background box with blue border
s.addShape(pres.shapes.RECTANGLE, {
  x: MD_X, y: MD_Y, w: MD_W, h: MD_H,
  fill: { color: WHITE },
  line: { color: BLUE, width: 2 },
});

// Embed the generated diagram
s.addImage({
  path: "slide_015_main_diagram.png",
  x: MD_X + 0.1, y: MD_Y + 0.1, w: MD_W - 0.2, h: MD_H - 0.2,
});

// ============================================================
// TRUTH TABLE: XOR (upper-right, red-bordered)
// ============================================================
const TT_X = 9.5, TT_Y = 1.0, TT_W = 3.5, TT_H = 2.0;

s.addShape(pres.shapes.RECTANGLE, {
  x: TT_X, y: TT_Y, w: TT_W, h: TT_H,
  fill: { color: WHITE },
  line: { color: RED, width: 2 },
});

// Table headers
s.addText("X1", { x: TT_X + 0.2, y: TT_Y + 0.1, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("X2", { x: TT_X + 1.0, y: TT_Y + 0.1, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("O/P", { x: TT_X + 1.8, y: TT_Y + 0.1, w: 1.0, h: 0.35, align: "center", valign: "middle", fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0 });

// Table rows - XOR truth table
// Row 1: 0, 0, 0 (cyan O/P)
s.addText("0", { x: TT_X + 0.2, y: TT_Y + 0.45, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("0", { x: TT_X + 1.0, y: TT_Y + 0.45, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("0", { x: TT_X + 1.8, y: TT_Y + 0.45, w: 1.0, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: CYAN, fontFace: FONT, margin: 0 });

// Row 2: 0, 1, 1 (green O/P)
s.addText("0", { x: TT_X + 0.2, y: TT_Y + 0.8, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("1", { x: TT_X + 1.0, y: TT_Y + 0.8, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("1", { x: TT_X + 1.8, y: TT_Y + 0.8, w: 1.0, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: LIGHT_GREEN, fontFace: FONT, margin: 0 });

// Row 3: 1, 0, 1 (green O/P)
s.addText("1", { x: TT_X + 0.2, y: TT_Y + 1.15, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("0", { x: TT_X + 1.0, y: TT_Y + 1.15, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("1", { x: TT_X + 1.8, y: TT_Y + 1.15, w: 1.0, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: LIGHT_GREEN, fontFace: FONT, margin: 0 });

// Row 4: 1, 1, 0 (cyan O/P)
s.addText("1", { x: TT_X + 0.2, y: TT_Y + 1.5, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("1", { x: TT_X + 1.0, y: TT_Y + 1.5, w: 0.8, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: BLACK, fontFace: FONT, margin: 0 });
s.addText("0", { x: TT_X + 1.8, y: TT_Y + 1.5, w: 1.0, h: 0.35, align: "center", valign: "middle", fontSize: 14, color: CYAN, fontFace: FONT, margin: 0 });

// ============================================================
// DATA TABLE: Bottom-left to center, red-bordered
// ============================================================
const DT_X = 0.6, DT_Y = 4.7, DT_W = 12.13, DT_H = 2.0;

s.addShape(pres.shapes.RECTANGLE, {
  x: DT_X, y: DT_Y, w: DT_W, h: DT_H,
  fill: { color: WHITE },
  line: { color: RED, width: 1.5 },
});

// Header row
const headers = ["x2", "x1", "S1", "Z1", "S2", "Z2", "S3", "Z3"];
const colWidth = DT_W / 8;
for (let i = 0; i < 8; i++) {
  s.addText(headers[i], {
    x: DT_X + i * colWidth, y: DT_Y + 0.05, w: colWidth, h: 0.35,
    align: "center", valign: "middle", fontSize: 11, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Data rows from analysis
const dataRows = [
  [0, 0, 0, 0, 0, 1, 1, 1],  // last Z3 cyan
  [0, 1, -1, 0, -1, 0, 0, 0], // last Z3 green
  [1, 0, 1, 1, 1, 1, 0, 0],   // last Z3 green
  [1, 1, 0, 0, 0, 1, 1, 1],   // last Z3 cyan
];

const rowColors = [
  [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, CYAN],
  [BLACK, BLACK, RED, BLACK, RED, BLACK, BLACK, LIGHT_GREEN],
  [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, LIGHT_GREEN],
  [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, CYAN],
];

for (let r = 0; r < 4; r++) {
  const rowY = DT_Y + 0.4 + r * 0.35;
  for (let c = 0; c < 8; c++) {
    s.addText(String(dataRows[r][c]), {
      x: DT_X + c * colWidth, y: rowY, w: colWidth, h: 0.35,
      align: "center", valign: "middle", fontSize: 11, color: rowColors[r][c], fontFace: FONT, margin: 0,
    });
  }
}

// ============================================================
// CALLOUT BOX: Bottom-right, rounded light-yellow
// ============================================================
const CB_X = 9.5, CB_Y = 3.3, CB_W = 3.5, CB_H = 1.3;

s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: CB_X, y: CB_Y, w: CB_W, h: CB_H,
  fill: { color: LIGHT_YELLOW },
  line: { color: "AAAAAA", width: 0.5 },
});

// Add the three lines as text
s.addText("Adding Non-Linearity", {
  x: CB_X + 0.2, y: CB_Y + 0.1, w: CB_W - 0.4, h: 0.4,
  align: "left", valign: "top", fontSize: 14, bold: false, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Solves the", {
  x: CB_X + 0.2, y: CB_Y + 0.45, w: CB_W - 0.4, h: 0.4,
  align: "left", valign: "top", fontSize: 14, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "XOR", options: { color: RED, fontSize: 14, fontFace: FONT } },
  { text: " Problem", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
], {
  x: CB_X + 0.2, y: CB_Y + 0.8, w: CB_W - 0.4, h: 0.4,
  align: "left", valign: "top", margin: 0,
});

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_015_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath));