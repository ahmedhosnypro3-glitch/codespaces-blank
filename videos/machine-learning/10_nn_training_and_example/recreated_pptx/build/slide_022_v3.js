// slide_022_v3.js — "Back Propagation Training Algorithm" (badge 22) — attempt 3
// v3 vs v2: full 3-3-3 network diagram (3 input / 3 hidden / 3 output nodes,
// 9+9 directed arrows, layer captions, weight labels, Net_j/O_j, Output/Target/
// Error labels, Neural Net caption). Step boxes + equations unchanged from v2
// (certified verbatim). House chrome per video AGENTS.md.
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
// original px -> house inches: x_in = px*0.013885 ; y_in = 1.0 + (py-108)*0.01471
const PURPLE = "800080", GREEN = "00FF00", RED = "FF0000", BLUE = "0000FF";
const BLACK = "000000", WHITE = "FFFFFF", DKGREEN = "006100";

// diagram panel
const PANEL = { x: 0.55, y: 1.00, w: 6.30, h: 2.10 };
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h,
  fill: { type: "none" }, line: { color: RED, width: 1 },
});

// 3 columns x 3 rows
const IN_X = 1.15, HID_X = 2.85, OUT_X = 4.55;
const ROW_YS = [1.30, 1.95, 2.60];
const IN_R = 0.055, NODE_R = 0.125;

function node(slide, x, y, r, fill, line, lineW) {
  slide.addShape(pres.shapes.OVAL, { x: x - r, y: y - r, w: 2*r, h: 2*r,
    fill: { color: fill }, line: { color: line, width: lineW } });
}
function arrow(slide, x1, y1, x2, y2) {
  slide.addShape(pres.shapes.LINE, { x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color: BLACK, width: 0.75, endArrowType: "triangle" } });
}
function cap(slide, txt, x, y, w, color, size) {
  slide.addText(txt, { x, y, w, h: 0.18, align: "center", valign: "middle",
    fontSize: size, bold: true, color, fontFace: FONT, margin: 0 });
}
// input nodes: small purple dots
ROW_YS.forEach(y => node(s, IN_X, y, IN_R, PURPLE, PURPLE, 0));
// hidden nodes: light blue circles containing Sigma
ROW_YS.forEach(y => {
  node(s, HID_X, y, NODE_R, "DDEBF7", BLUE, 1);
  cap(s, "\u03A3", HID_X - NODE_R, y - NODE_R, 2*NODE_R, BLACK, 11);
});
// output nodes: green circles containing Sigma
ROW_YS.forEach(y => {
  node(s, OUT_X, y, NODE_R, GREEN, DKGREEN, 1);
  cap(s, "\u03A3", OUT_X - NODE_R, y - NODE_R, 2*NODE_R, WHITE, 11);
});
// 9 input->hidden + 9 hidden->output directed arrows (all-to-all)
ROW_YS.forEach(y1 => ROW_YS.forEach(y2 => {
  arrow(s, IN_X + IN_R, y1, HID_X - NODE_R, y2);
}));
ROW_YS.forEach(y1 => ROW_YS.forEach(y2 => {
  arrow(s, HID_X + NODE_R, y1, OUT_X - NODE_R, y2);
}));

// layer captions (blue) under each column
cap(s, "Input Layer", IN_X - 0.45, PANEL.y + PANEL.h - 0.24, 0.9, BLUE, 8);
cap(s, "Hidden Layer", HID_X - 0.45, PANEL.y + PANEL.h - 0.24, 0.9, BLUE, 8);
cap(s, "Output Layer", OUT_X - 0.45, PANEL.y + PANEL.h - 0.24, 0.9, BLUE, 8);

// weight labels on arrows (blue italic): w_1j, w_2j, w_nj on input->hidden; w_ki on hidden->output
const SUB = { 1: "\u2081", 2: "\u2082", n: "\u2099", k: "\u2096", i: "\u1d62", j: "\u2c7c" };
function wlab(txt, x, y) {
  s.addText(txt, { x, y, w: 0.5, h: 0.2, fontSize: 8, bold: true, italic: true,
    color: BLUE, fontFace: FONT, margin: 0 });
}
wlab("w" + SUB[1] + SUB.j, 1.55, 1.38);
wlab("w" + SUB[2] + SUB.j, 1.75, 1.90);
wlab("w" + SUB.n + SUB.j, 1.55, 2.48);
wlab("w" + SUB.k + SUB.i, 3.55, 1.90);

// Net_j / O_j near top of network
wlab("Net" + SUB.j, HID_X - 0.25, PANEL.y + 0.02);
wlab("O" + SUB.j, OUT_X - 0.2, PANEL.y + 0.02);

// Output labels (green) right of output nodes
const OUT_L = ["Output 1", "Output 2", "Output m"];
ROW_YS.forEach((y, i) => s.addText(OUT_L[i], {
  x: OUT_X + NODE_R + 0.06, y: y - 0.09, w: 0.85, h: 0.18,
  align: "left", valign: "middle", fontSize: 8, bold: true, color: DKGREEN, fontFace: FONT, margin: 0 }));
// Target boxes (small green squares) + labels (red) and vertical Error panel
const TGT_X = 5.85, ERR_X = 6.55;
const TGT_L = ["Target 1", "Target 2", "Target m"];
ROW_YS.forEach((y, i) => {
  s.addShape(pres.shapes.RECTANGLE, { x: TGT_X, y: y - 0.08, w: 0.16, h: 0.16,
    fill: { color: GREEN }, line: { color: DKGREEN, width: 0.75 } });
  s.addText(TGT_L[i], { x: TGT_X + 0.20, y: y - 0.09, w: 0.7, h: 0.18,
    align: "left", valign: "middle", fontSize: 8, bold: true, color: RED, fontFace: FONT, margin: 0 });
});
s.addShape(pres.shapes.RECTANGLE, { x: ERR_X - 0.10, y: PANEL.y + 0.15, w: 0.20, h: PANEL.h - 0.55,
  fill: { color: RED }, line: { color: RED, width: 0 } });
s.addText("Error 1\nError 2\nError m", { x: ERR_X - 0.28, y: PANEL.y + 0.30, w: 0.56, h: PANEL.h - 0.85,
  align: "center", valign: "middle", fontSize: 7, bold: true, color: WHITE, fontFace: FONT, margin: 0 });

// "Neural Net" caption bottom-left of diagram
s.addText("Neural Net", { x: PANEL.x + 0.06, y: PANEL.y + 0.04, w: 0.8, h: 0.16,
  align: "left", valign: "middle", fontSize: 7, italic: true, color: "808080", fontFace: FONT, margin: 0 });

// ---- Blue box: steps [1]-[2] ----
const BLUE_BOX = { x: 0.55, y: 3.28, w: 12.40, h: 0.60 };
s.addShape(pres.shapes.RECTANGLE, {
  x: BLUE_BOX.x, y: BLUE_BOX.y, w: BLUE_BOX.w, h: BLUE_BOX.h,
  fill: { color: "E6F3FF" }, line: { color: BLUE, width: 2 },
});
s.addText([
  { text: "[1] ", options: { color: BLUE, bold: true } },
  { text: "Initialize all Weights with random values", options: { color: BLACK } },
], { x: BLUE_BOX.x + 0.12, y: BLUE_BOX.y + 0.05, w: BLUE_BOX.w - 0.24, h: 0.24,
  align: "left", valign: "middle", fontSize: 11, fontFace: FONT, margin: 0 });
s.addText([
  { text: "[2] ", options: { color: BLUE, bold: true } },
  { text: "Provide one training sample at a time (and its corresponding target label)", options: { color: BLACK } },
], { x: BLUE_BOX.x + 0.12, y: BLUE_BOX.y + 0.31, w: BLUE_BOX.w - 0.24, h: 0.24,
  align: "left", valign: "middle", fontSize: 11, fontFace: FONT, margin: 0 });
// ---- Red box: steps [3]-[6] + equation rows + Remember note ----
const RED_BOX = { x: 0.55, y: 4.07, w: 12.40, h: 3.08 };
s.addShape(pres.shapes.RECTANGLE, {
  x: RED_BOX.x, y: RED_BOX.y, w: RED_BOX.w, h: RED_BOX.h,
  fill: { color: "FFE6E6" }, line: { color: "C00000", width: 2 },
});
const STEP_FS = 11;
function stepLine(y, runs) {
  s.addText(runs, { x: RED_BOX.x + 0.12, y, w: RED_BOX.w - 0.24, h: 0.24,
    align: "left", valign: "middle", fontSize: STEP_FS, fontFace: FONT, margin: 0 });
}
const J = SUB.j, I = SUB.i, K = SUB.k, D = "\u0394", ETA = "\u03b7", DEL = "\u03b4", SIG = "\u03a3";

stepLine(4.20, [
  { text: "[3] ", options: { color: BLUE, bold: true } },
  { text: "Go Forward", options: { color: "C00000", bold: true } },
  { text: ` : Start from Input Layer, Calculate Net${J}, O${J} for each layer till reach output layer`, options: { color: BLACK } },
]);
stepLine(4.66, [
  { text: "[4] ", options: { color: BLUE, bold: true } },
  { text: "Go Backward", options: { color: "C00000", bold: true } },
  { text: ` : Start from Output Layer, Calculate ${D}w${J}${I}, W${J}${I} for each weights of Output layer`, options: { color: BLACK } },
]);

const EQ_A_BASE = 5.14;
s.addImage({ path: path.join(EQ_DIR, "eq_a1.png"), x: RED_BOX.x + 0.35,
  y: EQ_A_BASE - eq.a1.baseline_frac * eq.a1.h_in, w: eq.a1.w_in, h: eq.a1.h_in });
s.addText("Store:", { x: RED_BOX.x + 2.95, y: EQ_A_BASE - 0.18, w: 0.45, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0 });
s.addImage({ path: path.join(EQ_DIR, "eq_a2.png"), x: RED_BOX.x + 3.45,
  y: EQ_A_BASE - eq.a2.baseline_frac * eq.a2.h_in, w: eq.a2.w_in, h: eq.a2.h_in });
s.addText("(for each node at output Layer)", { x: RED_BOX.x + 5.45, y: EQ_A_BASE - 0.18, w: 2.6, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0 });
stepLine(5.46, [
  { text: "[5] ", options: { color: BLUE, bold: true } },
  { text: "Go Backward", options: { color: "C00000", bold: true } },
  { text: ` : go to previous Layer, Calculate ${D}w${J}${I}, W${J}${I} for each weights of Hidden layer`, options: { color: BLACK } },
]);

const EQ_B_BASE = 6.00;
s.addImage({ path: path.join(EQ_DIR, "eq_b1.png"), x: RED_BOX.x + 0.35,
  y: EQ_B_BASE - eq.b1.baseline_frac * eq.b1.h_in, w: eq.b1.w_in, h: eq.b1.h_in });
s.addText("Store:", { x: RED_BOX.x + 3.20, y: EQ_B_BASE - 0.18, w: 0.45, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0 });
s.addImage({ path: path.join(EQ_DIR, "eq_b2.png"), x: RED_BOX.x + 3.70,
  y: EQ_B_BASE - eq.b2.baseline_frac * eq.b2.h_in, w: eq.b2.w_in, h: eq.b2.h_in });
s.addText("(for each node at hidden Layer)", { x: RED_BOX.x + 5.95, y: EQ_B_BASE - 0.18, w: 2.6, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0 });

stepLine(6.48, [
  { text: "[6] ", options: { color: BLUE, bold: true } },
  { text: "Repeat [5]", options: { color: "C00000", bold: true } },
  { text: " till reach first hidden layer", options: { color: BLACK } },
]);

const REM_BASE = 6.88;
s.addText("Remember:", { x: RED_BOX.x + 0.55, y: REM_BASE - 0.18, w: 0.75, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: "C00000", bold: true, fontFace: FONT, margin: 0 });
s.addImage({ path: path.join(EQ_DIR, "eq_c1.png"), x: RED_BOX.x + 1.35,
  y: REM_BASE - eq.c1.baseline_frac * eq.c1.h_in, w: eq.c1.w_in, h: eq.c1.h_in });
s.addText(`of next layer   ( which is already calculated in previous step )`, {
  x: RED_BOX.x + 2.00, y: REM_BASE - 0.18, w: 4.6, h: 0.22,
  align: "left", valign: "bottom", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0 });

const OUT = path.join(__dirname, "slide_022_v3.pptx");
pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
