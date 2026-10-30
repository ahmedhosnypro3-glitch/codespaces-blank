// slide_022_v2.js — "Back Propagation Training Algorithm" (badge 22)
// v2: correct layout from measured original geometry (boxys: diagram panel
// y108..243px, blue box y256..297px, red box y310..520px of 960x540) +
// 2D equation law: matplotlib mathtext -> 600dpi PNG -> addImage at exact size.
// House chrome (machine-learning family, ref slide 3) OVERRIDES per-slide spec:
//  - bg E8E8E8; outer red frame x=0.15 y=0.15 w=13.03 h=7.2, C00000 1.5pt
//  - yellow badge x=12.48 y=0.30 w=0.5 h=0.5, fill FFF9C4, line FFF9C4 0.5, bold 18pt 333333
//  - title box y=0.28 x=0.6 w=12.13 centered (26pt bold C00000, per certified slide_021)

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const FONT = "Arial";
const NUM = 22;
const TITLE = "Back Propagation Training Algorithm";

const EQ_DIR = path.join(__dirname, "eq_assets", "slide_022");
const eq = {};
for (const f of fs.readdirSync(EQ_DIR).filter(f => f.endsWith(".json"))) {
  const meta = JSON.parse(fs.readFileSync(path.join(EQ_DIR, f), "utf8"));
  eq[path.basename(f, ".json")] = meta;
  eq[path.basename(f, ".json").replace(/^eq_/, "")] = meta;
}
console.log("Loaded equations:", Object.keys(eq));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- HOUSE CHROME ----
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
});

// ---- CONTENT GEOMETRY (measured from unique_slides/slide_022.jpg, 960x540) ----
// original px -> house inches:  x_in = px * 0.013885 ; y_in = 1.0 + (py-108)*0.01471
const NODE_R = 0.13;
const PANEL = { x: 0.95, y: 1.00, w: 5.60, h: 2.00 };
const IN_X = 1.39, HID_X = 3.89, OUT_X = 4.65, TGT_X = 6.11, ERR_X = 7.08;
const NODE_YS = [1.29, 1.90, 2.69];

const PURPLE = "800080";
const GREEN = "00FF00";
const RED = "FF0000";
const BLUE = "0000FF";
const BLACK = "000000";
const WHITE = "FFFFFF";

// ---- Neural network diagram ----
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h,
  fill: { type: "none" }, line: { color: "FF0000", width: 1 },
});

// Input layer: small purple dots
NODE_YS.forEach(y => {
  s.addShape(pres.shapes.OVAL, {
    x: IN_X - NODE_R * 0.6, y: y - NODE_R * 0.6, w: NODE_R * 1.2, h: NODE_R * 1.2,
    fill: { color: PURPLE }, line: { color: PURPLE, width: 0 },
  });
});

// Hidden layer: white circles with Sigma
NODE_YS.forEach(y => {
  s.addShape(pres.shapes.OVAL, {
    x: HID_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText("\u03A3", {
    x: HID_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle", fontSize: 11, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Output layer: green circles with Sigma
const OUT_LABELS = ["Output 1", "Output 2", "Output m"];
NODE_YS.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: OUT_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    fill: { color: GREEN }, line: { color: GREEN, width: 1 },
  });
  s.addText("\u03A3", {
    x: OUT_X - NODE_R, y: y - NODE_R, w: NODE_R * 2, h: NODE_R * 2,
    align: "center", valign: "middle", fontSize: 11, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
  s.addText(OUT_LABELS[i], {
    x: TGT_X - 1.05, y: y - 0.10, w: 1.0, h: 0.20,
    align: "left", valign: "middle", fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Connections input -> hidden -> output
NODE_YS.forEach(y => {
  s.addShape(pres.shapes.LINE, {
    x: IN_X + NODE_R * 0.6, y: y, w: HID_X - IN_X - NODE_R * 1.6, h: 0,
    line: { color: BLACK, width: 1 },
  });
  s.addShape(pres.shapes.LINE, {
    x: HID_X + NODE_R, y: y, w: OUT_X - HID_X - NODE_R * 2, h: 0,
    line: { color: BLACK, width: 1 },
  });
});

// Target boxes (green) and Error panel (tall red) to the right of the output layer
const TGT_LABELS = ["Target 1", "Target 2", "Target m"];
NODE_YS.forEach((y, i) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: TGT_X - 0.22, y: y - 0.10, w: 0.44, h: 0.20,
    fill: { color: GREEN }, line: { color: GREEN, width: 1 },
  });
  s.addText(TGT_LABELS[i], {
    x: TGT_X - 0.42, y: y - 0.10, w: 0.20, h: 0.20,
    align: "center", valign: "middle", fontSize: 6, color: WHITE, fontFace: FONT, margin: 0,
  });
});
s.addShape(pres.shapes.RECTANGLE, {
  x: ERR_X - 0.14, y: 1.05, w: 0.28, h: 1.95,
  fill: { color: RED }, line: { color: RED, width: 0 },
});
s.addText("Error 1\nError 2\nError m", {
  x: ERR_X - 0.40, y: 1.20, w: 0.80, h: 1.65,
  align: "center", valign: "middle", fontSize: 9, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Diagram caption (bottom-left of diagram, per analysis label "Neural Net")
s.addText("Neural Net", {
  x: PANEL.x + 0.10, y: PANEL.y + PANEL.h - 0.22, w: 1.0, h: 0.18,
  align: "left", valign: "middle", fontSize: 8, color: "808080", fontFace: FONT, margin: 0,
});

// ---- Blue box: steps [1]-[2] (original x40..840, y256..297) ----
const BLUE_BOX = { x: 0.55, y: 3.28, w: 12.40, h: 0.60 };
s.addShape(pres.shapes.RECTANGLE, {
  x: BLUE_BOX.x, y: BLUE_BOX.y, w: BLUE_BOX.w, h: BLUE_BOX.h,
  fill: { color: "E6F3FF" }, line: { color: BLUE, width: 2 },
});
s.addText([
  { text: "[1] ", options: { color: BLUE, bold: true } },
  { text: "Initialize all Weights with random values", options: { color: BLACK } },
], {
  x: BLUE_BOX.x + 0.12, y: BLUE_BOX.y + 0.05, w: BLUE_BOX.w - 0.24, h: 0.24,
  align: "left", valign: "middle", fontSize: 11, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "[2] ", options: { color: BLUE, bold: true } },
  { text: "Provide one training sample at a time (and its corresponding target label)", options: { color: BLACK } },
], {
  x: BLUE_BOX.x + 0.12, y: BLUE_BOX.y + 0.31, w: BLUE_BOX.w - 0.24, h: 0.24,
  align: "left", valign: "middle", fontSize: 11, fontFace: FONT, margin: 0,
});

// ---- Red box: steps [3]-[6] + equation rows (original x40..840, y310..520) ----
const RED_BOX = { x: 0.55, y: 4.07, w: 12.40, h: 3.08 };
s.addShape(pres.shapes.RECTANGLE, {
  x: RED_BOX.x, y: RED_BOX.y, w: RED_BOX.w, h: RED_BOX.h,
  fill: { color: "FFE6E6" }, line: { color: "C00000", width: 2 },
});

const STEP_FS = 11;
const SUB = { j: "\u2c7c", i: "\u1d62", k: "\u2096" }; // Unicode subscripts (Arial-safe, matches certified slide_021)

function stepLine(y, runs) {
  s.addText(runs, {
    x: RED_BOX.x + 0.12, y, w: RED_BOX.w - 0.24, h: 0.24,
    align: "left", valign: "middle", fontSize: STEP_FS, fontFace: FONT, margin: 0,
  });
}

// [3] Go Forward : Start from Input Layer, Calculate Net_j, O_j for each layer till reach output layer
stepLine(4.20, [
  { text: "[3] ", options: { color: BLUE, bold: true } },
  { text: "Go Forward", options: { color: "C00000", bold: true } },
  { text: ` : Start from Input Layer, Calculate Net${SUB.j}, O${SUB.j} for each layer till reach output layer`, options: { color: BLACK } },
]);

// [4] Go Backward : Start from Output Layer, Calculate Δw_ji, W_ji ... Output layer
stepLine(4.66, [
  { text: "[4] ", options: { color: BLUE, bold: true } },
  { text: "Go Backward", options: { color: "C00000", bold: true } },
  { text: ` : Start from Output Layer, Calculate \u0394w${SUB.j}${SUB.i}, W${SUB.j}${SUB.i} for each weights of Output layer`, options: { color: BLACK } },
]);

// Equation row A (output layer): Δw_ji = η O_i O_j(1-O_j) (t_j-O_j)  Store: δ_j = O_j(1-O_j) (t_j-O_j)
const EQ_A_BASE = 5.14;                  // baseline (inches)
s.addImage({
  path: path.join(EQ_DIR, "eq_a1.png"), x: RED_BOX.x + 0.35, w: eq.a1.w_in, h: eq.a1.h_in,
  y: EQ_A_BASE - eq.a1.baseline_frac * eq.a1.h_in,
});
s.addText("Store:", {
  x: RED_BOX.x + 2.95, y: EQ_A_BASE - 0.18, w: 0.45, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addImage({
  path: path.join(EQ_DIR, "eq_a2.png"), x: RED_BOX.x + 3.45, w: eq.a2.w_in, h: eq.a2.h_in,
  y: EQ_A_BASE - eq.a2.baseline_frac * eq.a2.h_in,
});
s.addText("(for each node at output Layer)", {
  x: RED_BOX.x + 5.45, y: EQ_A_BASE - 0.18, w: 2.6, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// [5] Go Backward : go to previous Layer, Calculate Δw_ji, W_ji ... Hidden layer
stepLine(5.46, [
  { text: "[5] ", options: { color: BLUE, bold: true } },
  { text: "Go Backward", options: { color: "C00000", bold: true } },
  { text: ` : go to previous Layer, Calculate \u0394w${SUB.j}${SUB.i}, W${SUB.j}${SUB.i} for each weights of Hidden layer`, options: { color: BLACK } },
]);

// Equation row B (hidden layer): Δw_ji = η O_i O_j(1-O_j) [Σ_k (δ_k w_kj)]  Store: δ_j = O_j(1-O_j) [Σ_k (δ_k w_kj)]
const EQ_B_BASE = 6.00;
s.addImage({
  path: path.join(EQ_DIR, "eq_b1.png"), x: RED_BOX.x + 0.35, w: eq.b1.w_in, h: eq.b1.h_in,
  y: EQ_B_BASE - eq.b1.baseline_frac * eq.b1.h_in,
});
s.addText("Store:", {
  x: RED_BOX.x + 3.20, y: EQ_B_BASE - 0.18, w: 0.45, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});
s.addImage({
  path: path.join(EQ_DIR, "eq_b2.png"), x: RED_BOX.x + 3.70, w: eq.b2.w_in, h: eq.b2.h_in,
  y: EQ_B_BASE - eq.b2.baseline_frac * eq.b2.h_in,
});
s.addText("(for each node at hidden Layer)", {
  x: RED_BOX.x + 5.95, y: EQ_B_BASE - 0.18, w: 2.6, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// [6] Repeat [5] till reach first hidden layer
stepLine(6.48, [
  { text: "[6] ", options: { color: BLUE, bold: true } },
  { text: "Repeat [5]", options: { color: "C00000", bold: true } },
  { text: " till reach first hidden layer", options: { color: BLACK } },
]);

// Remember: δ_k = δ_j of next layer ( which is already calculated in previous step )
const REM_BASE = 6.88;
s.addText("Remember:", {
  x: RED_BOX.x + 0.55, y: REM_BASE - 0.18, w: 0.75, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: "C00000", bold: true, fontFace: FONT, margin: 0,
});
s.addImage({
  path: path.join(EQ_DIR, "eq_c1.png"), x: RED_BOX.x + 1.35, w: eq.c1.w_in, h: eq.c1.h_in,
  y: REM_BASE - eq.c1.baseline_frac * eq.c1.h_in,
});
s.addText("of next layer   ( which is already calculated in previous step )", {
  x: RED_BOX.x + 2.00, y: REM_BASE - 0.18, w: 4.6, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// ---- Write deliverable (single version: slide_022_recreated.pptx) ----
const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_022_recreated.pptx";
pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
