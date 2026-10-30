const pptxgen = require("pptxgenjs");

// Slide 012: Classification of "OR" Truth Table
// Colors and geometry follow analysis/slide_012_final.json (validated, score 9).
const NUM = 12;
const TITLE = 'Classification of \u201cOR\u201d Truth Table';
const FONT = "Arial";
const SERIF = "Times New Roman";

const BG = "E6E6E6";
const BORDER_RED = "C00000";
const BLACK = "000000";
const LIGHT_GREEN = "90EE90";
const LIGHT_CYAN = "C0FFFF";
const PEACH = "FFE4C4";
const YELLOW = "FFF9C4";
const WHITE = "FFFFFF";

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
  x: 0, y: H - 0.33, w: W, h: 0.33,
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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: BORDER_RED, fontFace: SERIF, margin: 0,
});

// ============================================================
// TRUTH TABLE (top-left: x 10-33%, y 25-58%)
// ============================================================
const TABLE_X = 0.95;
const TABLE_Y = 1.35;
const TABLE_W = 3.55;
const TABLE_H = 2.35;

const rows = [
  ["X\u2081", "X\u2082", "O/P"],
  ["0", "0", "0"],
  ["0", "1", "1"],
  ["1", "0", "1"],
  ["1", "1", "1"],
];
const rowH = TABLE_H / 5;
const colW = TABLE_W / 3;

rows.forEach((row, ri) => {
  row.forEach((cell, ci) => {
    const x = TABLE_X + ci * colW;
    const y = TABLE_Y + ri * rowH;
    // Cell fill first (white, or the O/P highlight)
    let fill = WHITE;
    if (ri > 0 && ci === 2) {
      fill = (ri === 1) ? LIGHT_CYAN : LIGHT_GREEN;
    }
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: colW, h: rowH,
      fill: { color: fill },
      line: { color: BORDER_RED, width: 1 },
    });
    s.addText(cell, {
      x, y, w: colW, h: rowH,
      align: "center", valign: "middle",
      fontSize: 15, bold: (ri === 0), color: BLACK, fontFace: FONT, margin: 0,
    });
  });
});

// ============================================================
// DECISION BOUNDARY PLOT (top-right: x 55-88%, y 20-65%)
// ============================================================
const PLOT_X = 6.60;
const PLOT_Y = 1.10;
const PLOT_W = 4.55;
const PLOT_H = 3.15;

s.addShape(pres.shapes.RECTANGLE, {
  x: PLOT_X, y: PLOT_Y, w: PLOT_W, h: PLOT_H,
  fill: { color: WHITE },
  line: { color: BORDER_RED, width: 1 },
});
s.addImage({
  path: "slide_012_decision_boundary.png",
  x: PLOT_X + 0.12, y: PLOT_Y + 0.08, w: PLOT_W - 0.24, h: PLOT_H - 0.16,
});

// ============================================================
// NEURAL NETWORK DIAGRAM (bottom-left: x 15-53%, y 65-92%)
// Thin red rectangle border enclosing the area.
// ============================================================
const PERC_X = 1.55;
const PERC_Y = 4.75;
const PERC_W = 4.95;
const PERC_H = 2.05;

s.addShape(pres.shapes.RECTANGLE, {
  x: PERC_X, y: PERC_Y, w: PERC_W, h: PERC_H,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1 },
});
s.addImage({
  path: "slide_012_perceptron.png",
  x: PERC_X + 0.08, y: PERC_Y + 0.06, w: PERC_W - 0.16, h: PERC_H - 0.12,
});

// ============================================================
// EQUATION BOX (bottom-right: x 60-85%, y 78-88%)
// ============================================================
const EQ_X = 7.55;
const EQ_Y = 5.85;
const EQ_W = 3.35;
const EQ_H = 0.80;

s.addShape(pres.shapes.RECTANGLE, {
  x: EQ_X, y: EQ_Y, w: EQ_W, h: EQ_H,
  fill: { color: PEACH },
  line: { color: BORDER_RED, width: 1.25 },
});
// Equation image - d(X) = -7x1 - 5x2 + 2 (mathtext, 600dpi, professional format)
s.addImage({
  path: "eq_s012_dX.png",
  x: EQ_X + 0.18, y: EQ_Y + 0.14, w: 2.07, h: 0.205,
});

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_012_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath));