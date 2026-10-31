const pptxgen = require("pptxgenjs");

// Slide 012: Classification of "OR" Truth Table
// Geometry is measured from unique_slides/slide_012.jpg (960x540 px, 1px=1pt),
// so every content coordinate below is frame_px / 72 inches.
const NUM = 12;
const TITLE = 'Classification of “OR” Truth Table';
const FONT = "Arial";
const SERIF = "Times New Roman";

const BG = "E8E8E8";
const BORDER_RED = "C00000";
const BLACK = "000000";
const DARK = "333333";
const LIGHT_GREEN = "90EE90";
const LIGHT_CYAN = "C0FFFF";
const PEACH = "FFE4C4";
const YELLOW = "FFF9C4";
const WHITE = "FFFFFF";
const GRID_GRAY = "BFBFBF";

const PX = 1 / 72; // one original-frame pixel in inches

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
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// 4. Title box - HOUSE CHROME LAW (y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: BORDER_RED, fontFace: SERIF, margin: 0,
});

// ============================================================
// TRUTH TABLE - measured frame px: x 96..313, y 138..305
// column boundaries 96 | 166 | 236 | 313, rows 138/176/212/244/278/305
// ============================================================
const COL_X = [96, 166, 236, 313];
const ROW_Y = [138, 176, 212, 244, 278, 305];

const rows = [
  ["X₁", "X₂", "O/P"],
  ["0", "0", "0"],
  ["0", "1", "1"],
  ["1", "0", "1"],
  ["1", "1", "1"],
];

// cell fills
rows.forEach((row, ri) => {
  row.forEach((cell, ci) => {
    const x = COL_X[ci] * PX;
    const y = ROW_Y[ri] * PX;
    const w = (COL_X[ci + 1] - COL_X[ci]) * PX;
    const h = (ROW_Y[ri + 1] - ROW_Y[ri]) * PX;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h, fill: { color: WHITE },
    });
  });
});

// interior gridlines (thin gray) then the red outer border
for (let i = 1; i < COL_X.length - 1; i++) {
  s.addShape(pres.shapes.LINE, {
    x: COL_X[i] * PX, y: ROW_Y[0] * PX,
    w: 0, h: (ROW_Y[ROW_Y.length - 1] - ROW_Y[0]) * PX,
    line: { color: GRID_GRAY, width: 0.75 },
  });
}
for (let i = 1; i < ROW_Y.length - 1; i++) {
  s.addShape(pres.shapes.LINE, {
    x: COL_X[0] * PX, y: ROW_Y[i] * PX,
    w: (COL_X[COL_X.length - 1] - COL_X[0]) * PX, h: 0,
    line: { color: GRID_GRAY, width: 0.75 },
  });
}
s.addShape(pres.shapes.RECTANGLE, {
  x: COL_X[0] * PX, y: ROW_Y[0] * PX,
  w: (COL_X[COL_X.length - 1] - COL_X[0]) * PX,
  h: (ROW_Y[ROW_Y.length - 1] - ROW_Y[0]) * PX,
  fill: { type: "none" }, line: { color: BORDER_RED, width: 1 },
});

// O/P highlights sit OVER the gridlines so the bands stay continuous:
// cyan chip on the row-1 "0": x 263..285, y 178..201
s.addShape(pres.shapes.RECTANGLE, {
  x: 263 * PX, y: 178 * PX, w: 23 * PX, h: 24 * PX,
  fill: { color: LIGHT_CYAN },
});
// continuous green band over the three "1" rows: x 262..286, y 214..302
s.addShape(pres.shapes.RECTANGLE, {
  x: 262 * PX, y: 214 * PX, w: 25 * PX, h: 89 * PX,
  fill: { color: LIGHT_GREEN },
});

// values
rows.forEach((row, ri) => {
  row.forEach((cell, ci) => {
    const x = COL_X[ci] * PX;
    const y = ROW_Y[ri] * PX;
    const w = (COL_X[ci + 1] - COL_X[ci]) * PX;
    const h = (ROW_Y[ri + 1] - ROW_Y[ri]) * PX;
    s.addText(cell, {
      x, y, w, h, align: "center", valign: "middle",
      fontSize: 16, bold: (ri === 0), color: BLACK, fontFace: FONT, margin: 0,
    });
  });
});

// ============================================================
// DECISION BOUNDARY PLOT - measured panel: x 537..843, y 109..370
// The PNG carries the white panel, pink border, red axes, navy boundary
// (558,235)->(683,364), the three green + one cyan points and the labels.
// ============================================================
s.addImage({
  path: "slide_012_decision_boundary.png",
  x: 537 * PX, y: 109 * PX, w: 307 * PX, h: 262 * PX,
});

// ============================================================
// NEURAL NETWORK DIAGRAM - measured panel: x 141..515, y 352..492
// The PNG carries the inputs/weights, Sigma node, red input triangle,
// red arrows, the activation box holding ONLY the step pictogram, and the
// rule legend on its pale strip ABOVE the activation box.
// ============================================================
s.addShape(pres.shapes.RECTANGLE, {
  x: 141 * PX, y: 352 * PX, w: 375 * PX, h: 141 * PX,
  fill: { type: "none" }, line: { color: BORDER_RED, width: 1 },
});
s.addImage({
  path: "slide_012_perceptron.png",
  x: 141 * PX, y: 352 * PX, w: 375 * PX, h: 141 * PX,
});

// ============================================================
// EQUATION BOX - measured: x 579..810, y 417..463
// ============================================================
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 579 * PX, y: 417 * PX, w: 232 * PX, h: 47 * PX,
  fill: { color: PEACH }, line: { color: BORDER_RED, width: 1.25 },
});
// Equation image - mathtext, 600dpi, professional 2D format (1593x152 px)
// placed at exactly px/600 inches: 2.655 x 0.25333 in
s.addImage({
  path: "eq_s012_dX.png",
  x: 594.04 * PX, y: 428.04 * PX, w: 2.655, h: 0.25333,
});

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_012_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath));
