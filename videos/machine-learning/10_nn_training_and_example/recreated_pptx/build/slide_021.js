// slide_021.js — "At Hidden Layer" (badge 21) — HOUSE CHROME version
// House chrome (machine-learning family, ref slide 3) — OVERRIDES per-slide spec:
//  - background E8E8E8, outer red frame 0.15in inset (x=0.15 y=0.15 w=13.03 h=7.2), C00000 1.5pt
//  - yellow badge oval x=12.48 y=0.30 w=0.5 h=0.5, fill FFF9C4, line FFF9C4 0.5, bold 18pt 333333
//  - title box y=0.28 x=0.6 w=12.13 centered
// Equations: matplotlib mathtext -> 600dpi PNG -> addImage at EXACT size (w=px/600)
// Baseline law: y_image = target_baseline - baseline_frac * h_image
// FIXES for attempt 2:
//  - UP_ARROW shape for hollow upward arrow below center neuron (not rect+triangle)
//  - Equations use lowercase o_j and inter-term spacing \;
//  - Color-coded equations (separate PNGs per colored segment)

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const FONT = "Arial";
const NUM = 21;
const TITLE = "At Hidden Layer";

// ---- Equation sidecars ----
const EQ_DIR = path.join(__dirname, "eq_assets", "slide_021");
const eq = {};
const files = fs.readdirSync(EQ_DIR).filter(f => f.endsWith(".json"));
for (const f of files) {
  eq[path.basename(f, ".json")] = JSON.parse(fs.readFileSync(path.join(EQ_DIR, f), "utf8"));
}
console.log("Loaded equations:", Object.keys(eq));

// ---- Build ----------------------------------------------------------------------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. HOUSE CHROME: outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. HOUSE CHROME: yellow badge (numeral = printed number on original = 21)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. HOUSE CHROME: title box (centered per house rule) + red underline per original
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 26, bold: true, color: "C00000", fontFace: FONT, margin: 0,
  underline: { style: "sng", color: "C00000" },
});

// 4. Content area (inside house frame)
const CX = 0.5, CY = 1.0, CW = 12.33, CH = 6.2;

// 5. Main panel: red-outlined rectangle (content, not house chrome)
const PANEL = { x: CX + 0.2, y: CY, w: 9.2, h: 4.0 };
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 6. Vertical guide lines (faint light-gray, content) - use thin rectangles
s.addShape(pres.shapes.RECTANGLE, { x: PANEL.x + PANEL.w*0.3 - 0.004, y: PANEL.y, w: 0.008, h: PANEL.h, fill: { color: "D9D9D9" }, line: { type: "none" } });
s.addShape(pres.shapes.RECTANGLE, { x: PANEL.x + PANEL.w*0.52 - 0.004, y: PANEL.y, w: 0.008, h: PANEL.h, fill: { color: "D9D9D9" }, line: { type: "none" } });

// 7. Neural Network Diagram
const NODE_R = 0.28;
const NODE_CY = PANEL.y + PANEL.h * 0.42;

const INPUT_X = PANEL.x + PANEL.w * 0.25;
const INPUT_YS = [
  PANEL.y + PANEL.h * 0.12,
  PANEL.y + PANEL.h * 0.32,
  PANEL.y + PANEL.h * 0.52
];

const HIDDEN_X = PANEL.x + PANEL.w * 0.50;
const HIDDEN_Y = NODE_CY;

const OUTPUT_X = PANEL.x + PANEL.w * 0.75;
const OUTPUT_YS = INPUT_YS.slice();

function addCircle(slide, x, y, r, fillColor, lineColor, lineWidth) {
  slide.addShape(pres.shapes.OVAL, {
    x: x - r, y: y - r, w: 2*r, h: 2*r,
    fill: { color: fillColor }, line: { color: lineColor, width: lineWidth },
  });
}
function addDot(slide, x, y, r, color) {
  slide.addShape(pres.shapes.OVAL, {
    x: x - r, y: y - r, w: 2*r, h: 2*r,
    fill: { color: color }, line: { type: "none" },
  });
}
function addArrow(slide, x1, y1, x2, y2, color, width) {
  slide.addShape(pres.shapes.LINE, {
    x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color: color, width: width, endArrowType: "triangle" },
  });
}

// Input nodes (3 light blue)
INPUT_YS.forEach((y) => {
  addCircle(s, INPUT_X, y, NODE_R, "DCE6F1", "8DB4E2", 1);
  addDot(s, INPUT_X + NODE_R, y, 0.035, "C00000");
  s.addText("O\u1d62", {
    x: INPUT_X + NODE_R + 0.05, y: y - 0.14, w: 0.4, h: 0.3,
    fontSize: 11, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
  });
});

// Hidden node (light green)
addCircle(s, HIDDEN_X, HIDDEN_Y, NODE_R, "C6E0B4", "8FBC8F", 1);
addDot(s, HIDDEN_X, HIDDEN_Y, 0.035, "C00000");
s.addText("O\u2c7c", {
  x: HIDDEN_X - 0.08, y: HIDDEN_Y - 0.22, w: 0.4, h: 0.3,
  fontSize: 11, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Output nodes (tan/orange)
OUTPUT_YS.forEach((y) => {
  addCircle(s, OUTPUT_X, y, NODE_R, "F8CBAD", "E0A87A", 1);
  addDot(s, OUTPUT_X - NODE_R, y, 0.035, "C00000");
  s.addText("\u03b4\u2096", {
    x: OUTPUT_X + NODE_R + 0.02, y: y - 0.1, w: 0.4, h: 0.3,
    fontSize: 11, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
  });
});

// Arrows input->hidden with w_ji labels
INPUT_YS.forEach((y) => {
  addArrow(s, INPUT_X + NODE_R, y, HIDDEN_X - NODE_R, HIDDEN_Y, "C00000", 1);
  const midX = (INPUT_X + NODE_R + HIDDEN_X - NODE_R) / 2;
  const midY = (y + HIDDEN_Y) / 2;
  s.addText("w\u2c7c\u1d62", {
    x: midX - 0.2, y: midY - 0.16, w: 0.4, h: 0.3,
    fontSize: 10, bold: true, italic: true, color: "0000FF", fontFace: FONT, margin: 0,
  });
});

// Arrows hidden->output with w_kj labels
OUTPUT_YS.forEach((y) => {
  addArrow(s, HIDDEN_X + NODE_R, HIDDEN_Y, OUTPUT_X - NODE_R, y, "C00000", 1);
  const midX = (HIDDEN_X + NODE_R + OUTPUT_X - NODE_R) / 2;
  const midY = (HIDDEN_Y + y) / 2;
  s.addText("w\u2096\u2c7c", {
    x: midX - 0.2, y: midY - 0.16, w: 0.4, h: 0.3,
    fontSize: 10, bold: true, italic: true, color: "0000FF", fontFace: FONT, margin: 0,
  });
});

// FIX: Hollow upward block arrow below hidden node using UP_ARROW shape
// UP_ARROW is a block arrow pointing up; we want it hollow (white fill, red outline)
const ARROW_X = HIDDEN_X;
const ARROW_Y = HIDDEN_Y + NODE_R + 0.1;
const ARROW_W = 0.18;
const ARROW_H = 0.35;
s.addShape(pres.shapes.UP_ARROW, {
  x: ARROW_X - ARROW_W/2, y: ARROW_Y, w: ARROW_W, h: ARROW_H,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});

// 8. Equation strip (pale green, light blue border)
const STRIP_Y = PANEL.y + PANEL.h * 0.72;
const STRIP_H = 0.7;
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL.x + 0.4, y: STRIP_Y, w: PANEL.w - 0.8, h: STRIP_H,
  fill: { color: "E2EFDA" }, line: { color: "8EAADB", width: 1 },
});

// Equation 1 inside strip (target baseline centers it)
// The new eq1.png has lowercase o_j and \;; spacing
if (eq.eq1) {
  const targetBaseline = STRIP_Y + STRIP_H * 0.5;
  const y = targetBaseline - eq.eq1.baseline_frac * eq.eq1.h_in;
  s.addImage({ path: path.join(EQ_DIR, "eq1.png"), x: PANEL.x + 0.6, y, w: eq.eq1.w_in, h: eq.eq1.h_in });
}

// 9. Bottom definition box
const BOTTOM_BOX = { x: CX + 0.2, y: PANEL.y + PANEL.h + 0.3, w: 7.8, h: 1.1 };
s.addShape(pres.shapes.RECTANGLE, {
  x: BOTTOM_BOX.x, y: BOTTOM_BOX.y, w: BOTTOM_BOX.w, h: BOTTOM_BOX.h,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});

// Equation 2 (simplified) - new eq2.png has \;; spacing
if (eq.eq2) {
  const targetBaseline = BOTTOM_BOX.y + 0.28;
  const y = targetBaseline - eq.eq2.baseline_frac * eq.eq2.h_in;
  s.addImage({ path: path.join(EQ_DIR, "eq2.png"), x: BOTTOM_BOX.x + 0.2, y, w: eq.eq2.w_in, h: eq.eq2.h_in });
}

// "Where:" label (regular black serif, per analysis ~18px) then Equation 3
if (eq.eq3) {
  const whereX = BOTTOM_BOX.x + 0.2;
  const eq3X = BOTTOM_BOX.x + 0.75;
  const targetBaseline = BOTTOM_BOX.y + 0.72;
  const y = targetBaseline - eq.eq3.baseline_frac * eq.eq3.h_in;
  s.addText("Where:", {
    x: whereX, y: targetBaseline - 0.14, w: 0.5, h: 0.24,
    align: "left", valign: "bottom",
    fontSize: 14, bold: false, italic: false, color: "000000", fontFace: FONT, margin: 0,
  });
  s.addImage({ path: path.join(EQ_DIR, "eq3.png"), x: eq3X, y, w: eq.eq3.w_in, h: eq.eq3.h_in });
}

pres.writeFile({ fileName: path.join(__dirname, "slide_021_recreated.pptx") })
  .then(() => console.log("wrote slide_021_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });