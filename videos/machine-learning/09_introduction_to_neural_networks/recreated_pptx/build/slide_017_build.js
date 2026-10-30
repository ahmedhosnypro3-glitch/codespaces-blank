const pptxgen = require("pptxgenjs");

// Slide 017: Linear and Unit Step Activation Functions
const NUM = 17;
const TITLE = "Linear and Unit Step Activation Functions";
const FONT = "Arial";

const BG = "E8E8E8";
const BORDER_RED = "8B0000";
const BLACK = "000000";
const RED = "FF0000";
const DARK_RED = "8B0000";
const RED_BROWN = "A52A2A";
const GREEN = "008000";
const BLUE = "4169E1";
const LIGHT_GRAY = "F5F5F5";
const YELLOW = "FFF9C4";

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

// 2. Slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});

// ============================================================
// CONVERT PIXELS TO INCHES (1px = 1pt = 1/72 in at 960x540 original)
// ============================================================
function pxToIn(px) { return px / 72; }

// Top graph panel: x=309-595, y=120-268 (blue border)
const TG_X = pxToIn(309);
const TG_Y = pxToIn(120);
const TG_W = pxToIn(595 - 309);
const TG_H = pxToIn(268 - 120);

// Top label box: x=600-800, y=100-280 (light gray)
const TLB_X = pxToIn(600);
const TLB_Y = pxToIn(100);
const TLB_W = pxToIn(800 - 600);
const TLB_H = pxToIn(280 - 100);

// Bottom-left graph: x=137-422, y=289-437 (blue border)
const BLG_X = pxToIn(137);
const BLG_Y = pxToIn(289);
const BLG_W = pxToIn(422 - 137);
const BLG_H = pxToIn(437 - 289);

// Bottom-right graph: x=487-773, y=289-437 (blue border)
const BRG_X = pxToIn(487);
const BRG_Y = pxToIn(289);
const BRG_W = pxToIn(773 - 487);
const BRG_H = pxToIn(437 - 289);

// BL equation box: x=140-419, y=439-456 (light gray) - THIS IS TOO LOW, CLIPPING
// Move equation boxes UP to leave room for the equation PNG
// Original box y=439-456, h=17px -> move to y=410-445, h=35px
const BLE_X = pxToIn(140);
const BLE_Y = pxToIn(410);  // moved up from 439
const BLE_W = pxToIn(419 - 140);
const BLE_H = pxToIn(445 - 410);  // taller box

// BR equation box: x=490-769, y=438-456 (light gray) - MOVE UP
const BRE_X = pxToIn(490);
const BRE_Y = pxToIn(410);  // moved up from 438
const BRE_W = pxToIn(769 - 490);
const BRE_H = pxToIn(445 - 410);  // taller box

// Mouse cursor: ~row 317, x=445
const CURSOR_X = pxToIn(445);
const CURSOR_Y = pxToIn(317);

// Equation image paths (generated at 600dpi with render_eqs.py)
const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const EQ_LINEAR = BUILD_DIR + "/eq_linear.png";
const EQ_UNIPOLAR_FULL = BUILD_DIR + "/eq_unipolar_full.png";
const EQ_BIPOLAR_FULL = BUILD_DIR + "/eq_bipolar_full.png";

// ============================================================
// DRAW GRAPH PANELS
// ============================================================

// Helper: add a rectangular graph panel with blue border
function addGraphPanel(x, y, w, h) {
  // Blue border
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { type: "none" },
    line: { color: BLUE, width: 1.5 },
  });
}

// TOP GRAPH PANEL
addGraphPanel(TG_X, TG_Y, TG_W, TG_H);

// Axes for top graph (Cartesian with arrowheads)
const TG_MARGIN = pxToIn(40); // margin inside graph for axes
const TG_PLOT_X = TG_X + TG_MARGIN;
const TG_PLOT_Y = TG_Y + TG_MARGIN;
const TG_PLOT_W = TG_W - 2 * TG_MARGIN;
const TG_PLOT_H = TG_H - 2 * TG_MARGIN;

// X-axis (horizontal, with arrowhead)
s.addShape(pres.shapes.LINE, {
  x: TG_PLOT_X, y: TG_PLOT_Y + TG_PLOT_H / 2, w: TG_PLOT_W, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "med" },
});

// Y-axis (vertical, with arrowhead)
s.addShape(pres.shapes.LINE, {
  x: TG_PLOT_X + TG_PLOT_W / 2, y: TG_PLOT_Y + TG_PLOT_H, w: 0, h: -TG_PLOT_H,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "med" },
});

// Axis labels
// f(x) label - vertical axis, black
s.addText("f(x)", {
  x: TG_PLOT_X - pxToIn(30), y: TG_PLOT_Y - pxToIn(15), w: pxToIn(30), h: pxToIn(30),
  align: "center", valign: "middle",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});

// x label - horizontal axis, red
s.addText("x", {
  x: TG_PLOT_X + TG_PLOT_W + pxToIn(5), y: TG_PLOT_Y + TG_PLOT_H / 2 + pxToIn(5), w: pxToIn(20), h: pxToIn(20),
  align: "left", valign: "top",
  fontSize: 12, color: RED, fontFace: FONT, margin: 0,
});

// Diagonal red line (Linear function: y = x through origin)
// Origin is at center of plot area
const TG_ORIGIN_X = TG_PLOT_X + TG_PLOT_W / 2;
const TG_ORIGIN_Y = TG_PLOT_Y + TG_PLOT_H / 2;

// Line from bottom-left to top-right of plot area
s.addShape(pres.shapes.LINE, {
  x: TG_PLOT_X, y: TG_PLOT_Y + TG_PLOT_H, w: TG_PLOT_W, h: -TG_PLOT_H,
  line: { color: RED, width: 2 },
});

// TOP LABEL BOX (rounded rectangle, light gray fill)
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: TLB_X, y: TLB_Y, w: TLB_W, h: TLB_H,
  fill: { color: LIGHT_GRAY },
});
// Text inside: "F(x) = x" in black, "Linear (No Activation)" in red italic
s.addText("F(x) = x", {
  x: TLB_X + pxToIn(10), y: TLB_Y + pxToIn(10), w: TLB_W - pxToIn(20), h: pxToIn(30),
  align: "left", valign: "top",
  fontSize: 14, bold: false, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("Linear (No Activation)", {
  x: TLB_X + pxToIn(10), y: TLB_Y + pxToIn(40), w: TLB_W - pxToIn(20), h: pxToIn(30),
  align: "left", valign: "top",
  fontSize: 14, bold: false, color: RED_BROWN, fontFace: FONT, margin: 0, italic: true,
});

// BOTTOM-LEFT GRAPH PANEL
addGraphPanel(BLG_X, BLG_Y, BLG_W, BLG_H);

const BLG_MARGIN = pxToIn(35);
const BLG_PLOT_X = BLG_X + BLG_MARGIN;
const BLG_PLOT_Y = BLG_Y + BLG_MARGIN;
const BLG_PLOT_W = BLG_W - 2 * BLG_MARGIN;
const BLG_PLOT_H = BLG_H - 2 * BLG_MARGIN;

// X-axis
s.addShape(pres.shapes.LINE, {
  x: BLG_PLOT_X, y: BLG_PLOT_Y + BLG_PLOT_H / 2, w: BLG_PLOT_W, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "med" },
});

// Y-axis
s.addShape(pres.shapes.LINE, {
  x: BLG_PLOT_X + BLG_PLOT_W / 2, y: BLG_PLOT_Y + BLG_PLOT_H, w: 0, h: -BLG_PLOT_H,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "med" },
});

// Axis labels
s.addText("f(x)", {
  x: BLG_PLOT_X - pxToIn(30), y: BLG_PLOT_Y - pxToIn(15), w: pxToIn(30), h: pxToIn(30),
  align: "center", valign: "middle",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("x", {
  x: BLG_PLOT_X + BLG_PLOT_W + pxToIn(5), y: BLG_PLOT_Y + BLG_PLOT_H / 2 + pxToIn(5), w: pxToIn(20), h: pxToIn(20),
  align: "left", valign: "top",
  fontSize: 12, color: RED, fontFace: FONT, margin: 0,
});

// Uni-polar step function: y=0 for x<0, jump at x=0 to y=1, y=1 for x>0
const BLG_ORIGIN_X = BLG_PLOT_X + BLG_PLOT_W / 2;
const BLG_ORIGIN_Y = BLG_PLOT_Y + BLG_PLOT_H / 2;

const BLG_Y_ZERO = BLG_PLOT_Y + BLG_PLOT_H / 2;  // y=0 line (middle)
const BLG_Y_ONE = BLG_PLOT_Y;  // y=1 line (top)
const BLG_X_CENTER = BLG_ORIGIN_X;

// Segment 1: horizontal at y=0 (left half)
s.addShape(pres.shapes.LINE, {
  x: BLG_PLOT_X, y: BLG_Y_ZERO, w: BLG_PLOT_W / 2, h: 0,
  line: { color: RED, width: 2 },
});

// Segment 2: vertical jump at center
s.addShape(pres.shapes.LINE, {
  x: BLG_X_CENTER, y: BLG_Y_ZERO, w: 0, h: BLG_Y_ONE - BLG_Y_ZERO,
  line: { color: RED, width: 2 },
});

// Segment 3: horizontal at y=1 (right half)
s.addShape(pres.shapes.LINE, {
  x: BLG_X_CENTER, y: BLG_Y_ONE, w: BLG_PLOT_W / 2, h: 0,
  line: { color: RED, width: 2 },
});

// BOTTOM-LEFT EQUATION BOX - with 2D piecewise equation as single PNG
// Equation box background
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: BLE_X, y: BLE_Y, w: BLE_W, h: BLE_H,
  fill: { color: LIGHT_GRAY },
});
// Equation name text (left part of box)
s.addText("F(x) = Uni-polar Unit Step =", {
  x: BLE_X + pxToIn(8), y: BLE_Y + pxToIn(5), w: BLE_W - pxToIn(16), h: pxToIn(16),
  align: "left", valign: "top",
  fontSize: 10, bold: false, color: DARK_RED, fontFace: FONT, margin: 0,
});

// Embed the full piecewise equation PNG below the name
// PNG dims from render_eqs.py: 428x171 px at 600dpi = 0.713 x 0.285 inches
const EQ_W = pxToIn(428);
const EQ_H = pxToIn(171);
const EQ_X = BLE_X + pxToIn(70);
const EQ_Y = BLE_Y + pxToIn(20);  // moved up to fit in taller box

s.addImage({
  path: EQ_UNIPOLAR_FULL,
  x: EQ_X, y: EQ_Y, w: EQ_W, h: EQ_H
});

// BOTTOM-RIGHT GRAPH PANEL
addGraphPanel(BRG_X, BRG_Y, BRG_W, BRG_H);

const BRG_MARGIN = pxToIn(35);
const BRG_PLOT_X = BRG_X + BRG_MARGIN;
const BRG_PLOT_Y = BRG_Y + BRG_MARGIN;
const BRG_PLOT_W = BRG_W - 2 * BRG_MARGIN;
const BRG_PLOT_H = BRG_H - 2 * BRG_MARGIN;

// X-axis
s.addShape(pres.shapes.LINE, {
  x: BRG_PLOT_X, y: BRG_PLOT_Y + BRG_PLOT_H / 2, w: BRG_PLOT_W, h: 0,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "med" },
});

// Y-axis
s.addShape(pres.shapes.LINE, {
  x: BRG_PLOT_X + BRG_PLOT_W / 2, y: BRG_PLOT_Y + BRG_PLOT_H, w: 0, h: -BRG_PLOT_H,
  line: { color: BLACK, width: 1, endArrow: "triangle", endArrowSize: "med" },
});

// Axis labels
s.addText("f(x)", {
  x: BRG_PLOT_X - pxToIn(30), y: BRG_PLOT_Y - pxToIn(15), w: pxToIn(30), h: pxToIn(30),
  align: "center", valign: "middle",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("x", {
  x: BRG_PLOT_X + BRG_PLOT_W + pxToIn(5), y: BRG_PLOT_Y + BRG_PLOT_H / 2 + pxToIn(5), w: pxToIn(20), h: pxToIn(20),
  align: "left", valign: "top",
  fontSize: 12, color: RED, fontFace: FONT, margin: 0,
});

// Bi-polar step function: y=-1 for x<0, jump at x=0 to y=1, y=1 for x>0
const BRG_ORIGIN_X = BRG_PLOT_X + BRG_PLOT_W / 2;
const BRG_ORIGIN_Y = BRG_PLOT_Y + BRG_PLOT_H / 2;

const BRG_Y_MINUS_ONE = BRG_PLOT_Y + BRG_PLOT_H;  // y=-1 line (bottom)
const BRG_Y_ONE = BRG_PLOT_Y;  // y=1 line (top)
const BRG_X_CENTER = BRG_ORIGIN_X;

// Segment 1: horizontal at y=-1 (left half)
s.addShape(pres.shapes.LINE, {
  x: BRG_PLOT_X, y: BRG_Y_MINUS_ONE, w: BRG_PLOT_W / 2, h: 0,
  line: { color: RED, width: 2 },
});

// Segment 2: vertical jump at center
s.addShape(pres.shapes.LINE, {
  x: BRG_X_CENTER, y: BRG_Y_MINUS_ONE, w: 0, h: BRG_Y_ONE - BRG_Y_MINUS_ONE,
  line: { color: RED, width: 2 },
});

// Segment 3: horizontal at y=1 (right half)
s.addShape(pres.shapes.LINE, {
  x: BRG_X_CENTER, y: BRG_Y_ONE, w: BRG_PLOT_W / 2, h: 0,
  line: { color: RED, width: 2 },
});

// BOTTOM-RIGHT EQUATION BOX with 2D piecewise equation as single PNG
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: BRE_X, y: BRE_Y, w: BRE_W, h: BRE_H,
  fill: { color: LIGHT_GRAY },
});
// Equation name text
s.addText("F(x) = Bi-polar Unit Step =", {
  x: BRE_X + pxToIn(8), y: BRE_Y + pxToIn(5), w: BRE_W - pxToIn(16), h: pxToIn(16),
  align: "left", valign: "top",
  fontSize: 10, bold: false, color: DARK_RED, fontFace: FONT, margin: 0,
});

// Embed the full piecewise equation PNG
const EQ2_X = BRE_X + pxToIn(70);
const EQ2_Y = BRE_Y + pxToIn(24);

s.addImage({
  path: EQ_BIPOLAR_FULL,
  x: EQ2_X, y: EQ2_Y, w: EQ_W, h: EQ_H
});

// MOUSE CURSOR (small black arrow) - OMITTED per ground rule (c): capture artifacts correctly omitted
// s.addShape(pres.shapes.RIGHT_TRIANGLE, {
//   x: CURSOR_X, y: CURSOR_Y, w: pxToIn(8), h: pxToIn(10),
//   fill: { color: BLACK },
// });

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_017_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath));