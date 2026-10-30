// slide_021_v3.js — "At Hidden Layer" (badge 21) — attempt 3
// Fixes vs v2 (judge FAIL 2026-10-27): capital O_j in equations (use eq*c
// color-coded assets), delta_j label at hidden node, j label on up-arrow,
// Where: baked into eq3c (no wrapping text box).
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const FONT = "Arial";
const NUM = 21;
const TITLE = "At Hidden Layer";

const EQ_DIR = path.join(__dirname, "eq_assets", "slide_021");
const eq = {};
for (const f of fs.readdirSync(EQ_DIR).filter(f => f.endsWith(".json"))) {
  eq[path.basename(f, ".json")] = JSON.parse(fs.readFileSync(path.join(EQ_DIR, f), "utf8"));
}
console.log("Loaded equations:", Object.keys(eq));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// HOUSE CHROME
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 26, bold: true, color: "C00000", fontFace: FONT, margin: 0,
  underline: { style: "sng", color: "C00000" },
});

const CX = 0.5, CY = 1.0, CW = 12.33, CH = 6.2;
const PANEL = { x: CX + 0.2, y: CY, w: 9.2, h: 4.0 };
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, { x: PANEL.x + PANEL.w*0.3 - 0.004, y: PANEL.y, w: 0.008, h: PANEL.h, fill: { color: "D9D9D9" }, line: { type: "none" } });
s.addShape(pres.shapes.RECTANGLE, { x: PANEL.x + PANEL.w*0.52 - 0.004, y: PANEL.y, w: 0.008, h: PANEL.h, fill: { color: "D9D9D9" }, line: { type: "none" } });
// diagram nodes + labels (v3: O_j above hidden node, delta_j below it, j on arrow)
const NODE_R = 0.28;
const NODE_CY = PANEL.y + PANEL.h * 0.42;
const INPUT_X = PANEL.x + PANEL.w * 0.25;
const INPUT_YS = [PANEL.y + PANEL.h * 0.12, PANEL.y + PANEL.h * 0.32, PANEL.y + PANEL.h * 0.52];
const HIDDEN_X = PANEL.x + PANEL.w * 0.50;
const HIDDEN_Y = NODE_CY;
const OUTPUT_X = PANEL.x + PANEL.w * 0.75;
const OUTPUT_YS = INPUT_YS.slice();

function addCircle(slide, x, y, r, fillColor, lineColor, lineWidth) {
  slide.addShape(pres.shapes.OVAL, { x: x - r, y: y - r, w: 2*r, h: 2*r,
    fill: { color: fillColor }, line: { color: lineColor, width: lineWidth } });
}
function addDot(slide, x, y, r, color) {
  slide.addShape(pres.shapes.OVAL, { x: x - r, y: y - r, w: 2*r, h: 2*r,
    fill: { color: color }, line: { type: "none" } });
}
function addArrow(slide, x1, y1, x2, y2, color, width) {
  slide.addShape(pres.shapes.LINE, { x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color: color, width: width, endArrowType: "triangle" } });
}
function lbl(slide, txt, x, y, color) {
  slide.addText(txt, { x, y, w: 0.5, h: 0.3, fontSize: 11, bold: true,
    italic: true, color, fontFace: FONT, margin: 0 });
}

INPUT_YS.forEach((y) => {
  addCircle(s, INPUT_X, y, NODE_R, "DCE6F1", "8DB4E2", 1);
  addDot(s, INPUT_X + NODE_R, y, 0.035, "C00000");
  lbl(s, "O\u1d62", INPUT_X + NODE_R + 0.05, y - 0.14, "C00000");
});

addCircle(s, HIDDEN_X, HIDDEN_Y, NODE_R, "C6E0B4", "8FBC8F", 1);
addDot(s, HIDDEN_X, HIDDEN_Y, 0.035, "C00000");
lbl(s, "O\u2c7c", HIDDEN_X - 0.08, HIDDEN_Y - 0.24, "C00000");          // above node
lbl(s, "\u03b4\u2c7c", HIDDEN_X + 0.06, HIDDEN_Y + 0.16, "C00000");       // below-right of node

OUTPUT_YS.forEach((y) => {
  addCircle(s, OUTPUT_X, y, NODE_R, "F8CBAD", "E0A87A", 1);
  addDot(s, OUTPUT_X - NODE_R, y, 0.035, "C00000");
  lbl(s, "\u03b4\u2096", OUTPUT_X + NODE_R + 0.02, y - 0.10, "C00000");
});

INPUT_YS.forEach((y) => {
  addArrow(s, INPUT_X + NODE_R, y, HIDDEN_X - NODE_R, HIDDEN_Y, "C00000", 1);
  const midX = (INPUT_X + NODE_R + HIDDEN_X - NODE_R) / 2;
  const midY = (y + HIDDEN_Y) / 2;
  s.addText("w\u2c7c\u1d62", { x: midX - 0.2, y: midY - 0.16, w: 0.4, h: 0.3,
    fontSize: 10, bold: true, italic: true, color: "0000FF", fontFace: FONT, margin: 0 });
});
OUTPUT_YS.forEach((y) => {
  addArrow(s, HIDDEN_X + NODE_R, HIDDEN_Y, OUTPUT_X - NODE_R, y, "C00000", 1);
  const midX = (HIDDEN_X + NODE_R + OUTPUT_X - NODE_R) / 2;
  const midY = (HIDDEN_Y + y) / 2;
  s.addText("w\u2096\u2c7c", { x: midX - 0.2, y: midY - 0.16, w: 0.4, h: 0.3,
    fontSize: 10, bold: true, italic: true, color: "0000FF", fontFace: FONT, margin: 0 });
});
// hollow up-arrow below hidden node, labeled j on its right
const ARROW_X = HIDDEN_X;
const ARROW_Y = HIDDEN_Y + NODE_R + 0.22;
const ARROW_W = 0.18;
const ARROW_H = 0.30;
s.addShape(pres.shapes.UP_ARROW, {
  x: ARROW_X - ARROW_W/2, y: ARROW_Y, w: ARROW_W, h: ARROW_H,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});
s.addText("j", { x: ARROW_X + 0.12, y: ARROW_Y + 0.02, w: 0.25, h: 0.26,
  fontSize: 11, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0 });

// equation strip (pale green, light blue border) with color-coded eq1c (capital O_j)
const STRIP_Y = PANEL.y + PANEL.h * 0.72;
const STRIP_H = 0.7;
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL.x + 0.4, y: STRIP_Y, w: PANEL.w - 0.8, h: STRIP_H,
  fill: { color: "E2EFDA" }, line: { color: "8EAADB", width: 1 },
});
if (eq.eq1c) {
  const targetBaseline = STRIP_Y + STRIP_H * 0.5;
  const y = targetBaseline - eq.eq1c.baseline_frac * eq.eq1c.h_in;
  s.addImage({ path: path.join(EQ_DIR, "eq1c.png"), x: PANEL.x + 0.55, y, w: eq.eq1c.w_in, h: eq.eq1c.h_in });
}

// bottom definition box: line1 eq2c, line2 eq3c (Where: baked in, no wrap)
const BOTTOM_BOX = { x: CX + 0.2, y: PANEL.y + PANEL.h + 0.3, w: 9.2, h: 1.15 };
s.addShape(pres.shapes.RECTANGLE, {
  x: BOTTOM_BOX.x, y: BOTTOM_BOX.y, w: BOTTOM_BOX.w, h: BOTTOM_BOX.h,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});
if (eq.eq2c) {
  const b1 = BOTTOM_BOX.y + 0.34;
  s.addImage({ path: path.join(EQ_DIR, "eq2c.png"), x: BOTTOM_BOX.x + 0.2,
    y: b1 - eq.eq2c.baseline_frac * eq.eq2c.h_in, w: eq.eq2c.w_in, h: eq.eq2c.h_in });
}
if (eq.eq3c) {
  const b2 = BOTTOM_BOX.y + 0.88;
  s.addImage({ path: path.join(EQ_DIR, "eq3c.png"), x: BOTTOM_BOX.x + 0.2,
    y: b2 - eq.eq3c.baseline_frac * eq.eq3c.h_in, w: eq.eq3c.w_in, h: eq.eq3c.h_in });
}

const OUT = path.join(__dirname, "slide_021_v3.pptx");
pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
