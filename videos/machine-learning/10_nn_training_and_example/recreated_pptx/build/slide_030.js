// slide_030.js — "Backward ( Update hidden Layer Weights)" (badge 30)
// Build: NODE_PATH=$(npm root -g) node slide_030.js
// Uses patterns: house-chrome, equations-mathtext-png
// Measurements: 960x540 source px -> 13.33x7.5in (72.02 px/in)

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const ROOT = "/home/codespace/ai_llm_slides";
const VID = ROOT + "/videos/machine-learning/10_nn_training_and_example";

const FONT = "Arial";
const NUM = 30;
const TITLE = "Example";

const PX = 13.33 / 960;   // inches per source px
const px = v => +(v * PX).toFixed(4);

const BG = "E8E8E8";
const FRAME_COLOR = "C00000";
const BADGE_FILL = "FFF9C4";
const BADGE_LINE = "FFF9C4";
const BADGE_TEXT = "333333";
const TITLE_COLOR = "C00000";
const BLACK = "000000";
const BLUE = "0000FF";
const RED = "C00000";
const GREEN_W = "00B000";
const MAGENTA_W = "CC33CC";

const EQ_DIR = path.join(__dirname, "eq_assets", "slide_030");
const eq = {};
for (const f of fs.readdirSync(EQ_DIR).filter(f => f.endsWith(".json"))) {
  eq[path.basename(f, ".json")] = JSON.parse(fs.readFileSync(path.join(EQ_DIR, f), "utf8"));
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

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
  fontSize: 36, bold: true, color: TITLE_COLOR, fontFace: FONT, margin: 0,
});

// ========== HELPERS ==========
function txt(xPx, yPx, wPx, hPx, str, size, color, bold, italic, align) {
  s.addText(str, {
    x: px(xPx), y: px(yPx), w: px(wPx), h: px(hPx),
    align: align || "left", valign: "top",
    fontSize: size, bold: !!bold, italic: !!italic, color: color, fontFace: FONT, margin: 0,
  });
}
function rule(yPx, x0, x1, color, wpt) {
  s.addShape(pres.shapes.LINE, {
    x: px(x0), y: px(yPx), w: px(x1 - x0), h: 0,
    line: { color: color, width: wpt || 1 },
  });
}
function node(cx, cy, r, fill, stroke) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
}
function circleText(cx, cy, r, str, size, color) {
  s.addText(str, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    align: "center", valign: "middle",
    fontSize: size, bold: true, color: color || BLACK, fontFace: FONT, margin: 0,
  });
}
function conn(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color: color, width: 0.75 },
  });
}
function eqImg(name, xPx, baselinePx) {
  const e = eq[name];
  const y = px(baselinePx) - e.baseline_frac * e.h_in;
  s.addImage({ path: path.join(EQ_DIR, name + ".png"), x: px(xPx), y, w: e.w_in, h: e.h_in });
}

// ========== RED SECTION RULES (measured y=89, 170, 198) ==========
rule(89, 38, 920, RED, 1);
rule(170, 38, 920, RED, 1);
rule(198, 45, 683, RED, 0.75);

// ========== LEFT COLUMN: DELTA / ETA RULES (2D equations) ==========
eqImg("eq1", 50, 117);   // blue:  d_j = O_j(1-O_j)[SUM_k (d_k w_kj)]
eqImg("eq2", 50, 157);   // purple: Dw_ji = eta O_i O_j(1-O_j)[SUM...] = eta O_i d_j

// ========== DELTA 6 / DELTA 7 LINE (y184-196) ==========
txt(50, 183, 640, 18,
  "δ₆ = 0.791(1−0.791)(0−0.791) = −0.131        δ₇ = 0.791(1−0.791)(1−0.791) = 0.035",
  13, BLACK, false, false);

// ========== HEADING (y208-221) ==========
s.addText([
  { text: "Backward ( ", options: { color: BLACK } },
  { text: "Update", options: { color: RED } },
  { text: " hidden ", options: { color: RED } },
  { text: "Layer Weights)", options: { color: BLACK } },
], {
  x: px(50), y: px(205), w: px(400), h: px(20),
  align: "left", valign: "top",
  fontSize: 14, bold: true, fontFace: FONT, margin: 0,
});

// ========== DELTA 3..5 LINES ==========
txt(58, 228, 300, 18, "δ₃ = O₃(1−O₃)[δ₆*W₆₃ + δ₇*W₇₃]", 13, BLUE, false, false);
txt(58, 252, 440, 18, "δ₃ = 0.9(1−0.9)[−0.131*−0.29 + 0.035*0.458] = 0.005", 13, BLACK, false, false);
txt(58, 276, 500, 18, "δ₄ = 0.943(1−0.943)[−0.131*−0.218 + 0.035*0.565] = 0.003", 13, BLACK, false, false);
txt(58, 299, 520, 18, "δ₅ = 0.968(1−0.968)[−0.131*−0.134 + 0.035*0.669] = 0.001", 13, BLACK, false, false);

// ========== WEIGHT UPDATE GRID (two columns, rows y333..517) ==========
const DW = ["ΔW₃₁ = 5*0.005*1 = 0.025", "ΔW₃₂ = 5*0.005*5 = 0.125", "ΔW₃b = 5*0.005*1 = 0.025",
            "ΔW₄₁ = 5*0.003*1 = 0.015", "ΔW₄₂ = 5*0.003*5 = 0.075", "ΔW₄b = 5*0.003*1 = 0.015",
            "ΔW₅₁ = 5*0.001*1 = 0.005", "ΔW₅₂ = 5*0.001*5 = 0.025", "ΔW₅b = 5*0.001*1 = 0.005"];
const WV = ["W₃₁ = 0.1 + 0.025 = 0.125", "W₃₂ = 0.4 + 0.125 = 0.525", "W₃b = 0.1 + 0.025 = 0.125",
            "W₄₁ = 0.2 + 0.015 = 0.215", "W₄₂ = 0.5 + 0.075 = 0.575", "W₄b = 0.1 + 0.015 = 0.115",
            "W₅₁ = 0.3 + 0.005 = 0.305", "W₅₂ = 0.6 + 0.025 = 0.625", "W₅b = 0.1 + 0.005 = 0.105"];
for (let i = 0; i < 9; i++) {
  const y = 333 + i * 23;
  txt(59, y, 210, 17, DW[i], 12, BLACK, false, false);
  txt(326, y, 280, 17, WV[i], 12, BLUE, false, false);
}

// ========== OUTPUT SIGMOID COLUMN (x612, baselines 268/295/321/351/381) ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: px(604), y: px(252), w: px(326), h: px(28),
  fill: { color: "DDEBF7" }, line: { type: "none" },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: px(604), y: px(279), w: px(326), h: px(28),
  fill: { color: "DDEBF7" }, line: { type: "none" },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: px(604), y: px(305), w: px(326), h: px(28),
  fill: { color: "DDEBF7" }, line: { type: "none" },
});
eqImg("o3", 612, 268);
eqImg("o4", 612, 295);
eqImg("o5", 612, 321);
eqImg("o6", 612, 351);
eqImg("o7", 612, 381);

// ========== NETWORK DIAGRAM (x430-920, y42-247) ==========
txt(440, 44, 60, 16, "Input", 11, BLUE, true, false);
txt(690, 44, 60, 16, "Output", 11, BLUE, true, false);
txt(788, 44, 60, 16, "Target", 11, BLUE, true, false);

// input nodes
txt(432, 70, 26, 16, "x₁", 11, BLACK, false, false);
node(470, 78, 10, "FFFFFF", BLACK);
circleText(470, 78, 10, "1", 9);
txt(432, 133, 26, 16, "x₂", 11, BLACK, false, false);
node(470, 143, 10, "FFFFFF", BLACK);
circleText(470, 143, 10, "5", 9);
txt(432, 158, 50, 16, "Bias", 10, BLUE, false, false);

// hidden nodes
node(545, 72, 10, "C6EFCE", "00B050");
circleText(545, 72, 10, "3", 9);
node(545, 108, 10, "C6EFCE", "00B050");
circleText(545, 108, 10, "4", 9);
node(545, 144, 10, "C6EFCE", "00B050");
circleText(545, 144, 10, "5", 9);
txt(558, 64, 26, 16, "O₃", 10, BLACK, false, false);
txt(558, 100, 26, 16, "O₄", 10, BLACK, false, false);
txt(558, 136, 26, 16, "O₅", 10, BLACK, false, false);

// output nodes
node(735, 105, 11, "FFC7CE", "FF0000");
circleText(735, 105, 11, "6", 9);
node(735, 148, 11, "FFC7CE", "FF0000");
circleText(735, 148, 11, "7", 9);
txt(750, 97, 26, 16, "O₆", 10, BLACK, false, false);
txt(750, 140, 26, 16, "O₇", 10, BLACK, false, false);

// targets
txt(795, 92, 40, 16, "t₆", 11, BLACK, false, false);
txt(820, 92, 40, 16, "0", 11, BLACK, false, false);
txt(795, 135, 40, 16, "t₇", 11, BLACK, false, false);
txt(820, 135, 40, 16, "1", 11, BLACK, false, false);

// learning rate
txt(575, 200, 60, 18, "η = 5", 12, BLUE, false, false);

// connections
conn(480, 78, 535, 72, GREEN_W);
conn(480, 78, 535, 108, GREEN_W);
conn(480, 78, 535, 144, GREEN_W);
conn(480, 143, 535, 72, GREEN_W);
conn(480, 143, 535, 108, GREEN_W);
conn(480, 143, 535, 144, GREEN_W);
conn(555, 72, 724, 105, MAGENTA_W);
conn(555, 72, 724, 148, MAGENTA_W);
conn(555, 108, 724, 105, MAGENTA_W);
conn(555, 108, 724, 148, MAGENTA_W);
conn(555, 144, 724, 105, MAGENTA_W);
conn(555, 144, 724, 148, MAGENTA_W);

// edge weight labels
txt(492, 62, 26, 12, "0.1", 7, GREEN_W, false, false);
txt(492, 106, 26, 12, "0.3", 7, GREEN_W, false, false);
txt(500, 130, 26, 12, "0.5", 7, GREEN_W, false, false);
txt(575, 62, 30, 12, "−0.29", 7, MAGENTA_W, false, false);
txt(600, 86, 32, 12, "0.458", 7, MAGENTA_W, false, false);
txt(575, 110, 32, 12, "−0.218", 7, MAGENTA_W, false, false);
txt(610, 128, 32, 12, "0.565", 7, MAGENTA_W, false, false);
txt(575, 146, 32, 12, "−0.134", 7, MAGENTA_W, false, false);
txt(640, 158, 32, 12, "0.669", 7, MAGENTA_W, false, false);

// ========== WRITE FILE ==========
pres.writeFile({ fileName: VID + "/recreated_pptx/slide_030_recreated.pptx" })
  .then(() => console.log("wrote slide_030_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
