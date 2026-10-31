// slide_031.js — "Example": worked backpropagation (slide 31)
// Build: NODE_PATH=$(npm root -g) node slide_031.js
// Patterns: house-chrome, equations-mathtext-png (assets/s31), explicit-line-spacing
// Measurements: 960x540 source px -> 13.33x7.5in (PX = 13.33/960)
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example";
const ASSETS = VID + "/recreated_pptx/build/assets/s31";
const MAN = JSON.parse(fs.readFileSync(ASSETS + "/manifest.json"));
const PX = 13.33 / 960;
const px = v => +(v * PX).toFixed(4);

const FONT = "Arial";
const NUM = 31;
const TITLE = "Example";
const RED = "FF0000", BLUE = "0000FF", BLACK = "000000";
const GREEN_W = "00B000", MAGENTA_W = "CC33CC", CYAN = "33CCCC";
const PALE_YELLOW = "FFF9C4", PURPLE_STROKE = "CC00CC", ORANGE_STROKE = "FF6600";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ========== HOUSE CHROME ==========
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
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ========== HELPERS ==========
// equation image placed so its math baseline lands on yBase (inches)
function eq(key, xIn, yBase, fsOverride) {
  const m = MAN[key];
  const y = yBase - m.baseline_frac * m.h_in;
  s.addImage({ path: m.png, x: xIn, y, w: m.w_in, h: m.h_in });
  return m.w_in; // advance width for chained segments
}
function txt(str, x, y, w, h, size, color, bold, align, italic) {
  s.addText(str, {
    x, y, w, h, align: align || "left", valign: "middle",
    fontSize: size, bold: !!bold, italic: !!italic, color, fontFace: FONT, margin: 0,
  });
}
function node(cxPx, cyPx, rPx, fill, stroke) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cxPx - rPx), y: px(cyPx - rPx), w: px(2 * rPx), h: px(2 * rPx),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
}
function circleText(cxPx, cyPx, rPx, t, size) {
  txt(t, px(cxPx - rPx), px(cyPx - rPx), px(2 * rPx), px(2 * rPx),
      size, BLACK, true, "center");
}
function label(cxPx, cyPx, t, color, size, wPx, italic) {
  txt(t, px(cxPx - (wPx || 40) / 2), px(cyPx - 8), px(wPx || 40), px(16),
      size, color, true, "center", italic);
}
function conn(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color, width: 1 },
  });
}

// ========== A) TOP-LEFT FORMULA BOX (red ruled) ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: px(45), y: px(89), w: px(407 - 45), h: px(171 - 89),
  fill: { type: "none" }, line: { color: RED, width: 1 },
});
eq("t1", px(52), px(115));
eq("t2", px(52), px(146));
eq("t3", px(52), px(157));
eq("t4", px(52), px(169));

// ========== B) HEADER "Backward (Update hidden Layer Weights)" ==========
s.addText([
  { text: "Backward", options: { color: RED, bold: true } },
  { text: " (Update hidden Layer Weights)", options: { color: BLUE, bold: true } },
], {
  x: px(54), y: px(182), w: px(400), h: px(18),
  align: "left", valign: "middle", fontSize: 14, fontFace: FONT, margin: 0,
});

// ========== C) DELTA LINES (left column) ==========
eq("d1", px(57), px(219));
eq("d2", px(57), px(241));
eq("d3", px(57), px(266));
eq("d4", px(57), px(289));

// ========== D) SIGMOID LINES (middle-right) ==========
eq("s1", px(468), px(238));
eq("s2", px(468), px(260));
eq("s3", px(468), px(284));
eq("s4", px(468), px(308));
eq("s5", px(468), px(340));

// ========== E) BOTTOM ΔW / W COLUMNS (9 rows) + blue arrows ==========
const ROW_Y = [338, 362, 386, 410, 436, 460, 484, 508, 532]; // px baselines
for (let i = 0; i < 9; i++) {
  const yb = px(ROW_Y[i]);
  const wL = eq("dw" + i + "_p", px(59), px(ROW_Y[i]));
  eq("dw" + i + "_r", px(59) + wL + 0.04, px(ROW_Y[i]));
  const wR = eq("w" + i + "_p", px(422), px(ROW_Y[i]));
  eq("w" + i + "_r", px(422) + wR + 0.04, px(ROW_Y[i]));
}
// three large blue right-pointing arrows between the columns
for (const ay of [386, 460, 508]) {
  s.addShape(pres.shapes.RIGHT_ARROW, {
    x: px(300), y: px(ay - 12), w: px(110), h: px(24),
    fill: { color: "0000FF" }, line: { color: "0000FF", width: 0.5 },
  });
}

// ========== F) NETWORK DIAGRAM (top-right) ==========
// Input (black disks) + input vector [1;5]; hidden 3/4/5; output 6/7; target [0;1]
node(484, 85, 7, BLACK, BLACK);
node(484, 125, 7, BLACK, BLACK);
node(490, 168, 8, CYAN, BLUE);
circleText(490, 168, 8, "1", 9);
label(510, 78, "x1(1)", BLACK, 10, 44);
label(510, 118, "x2(5)", BLACK, 10, 44);
label(468, 168, "Bias", BLUE, 9, 34);
label(452, 70, "Input", BLUE, 12, 50);

// input column vector [1;5] left of the input disks
s.addText("[", { x: px(453), y: px(72), w: px(10), h: px(80), fontSize: 16, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("1", { x: px(462), y: px(76), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("5", { x: px(462), y: px(116), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("]", { x: px(462), y: px(72), w: px(10), h: px(80), fontSize: 16, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// hidden layer 3/4/5 (pale yellow, purple stroke)
node(565, 64, 10, PALE_YELLOW, PURPLE_STROKE);
circleText(565, 64, 10, "3", 10);
node(565, 108, 10, PALE_YELLOW, PURPLE_STROKE);
circleText(565, 108, 10, "4", 10);
node(565, 144, 10, PALE_YELLOW, PURPLE_STROKE);
circleText(565, 144, 10, "5", 10);
label(565, 46, "O3", BLACK, 10, 30);
label(565, 90, "O4", BLACK, 10, 30);
label(565, 126, "O5", BLACK, 10, 30);

// output layer 6/7 (tan)
node(712, 93, 9, PALE_YELLOW, ORANGE_STROKE);
circleText(712, 93, 9, "6", 10);
node(712, 132, 9, PALE_YELLOW, ORANGE_STROKE);
circleText(712, 132, 9, "7", 10);
label(744, 90, "O6", BLACK, 10, 30);
label(744, 129, "O7", BLACK, 10, 30);
label(712, 72, "Output", BLUE, 11, 50);

// target vector [0;1]
label(770, 100, "t6", BLACK, 9, 20);
label(770, 128, "t7", BLACK, 9, 20);
s.addText("[", { x: px(779), y: px(90), w: px(10), h: px(50), fontSize: 16, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("0", { x: px(789), y: px(94), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("1", { x: px(789), y: px(120), w: px(13), h: px(18), fontSize: 12, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("]", { x: px(800), y: px(90), w: px(10), h: px(50), fontSize: 16, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
label(770, 74, "Target", BLACK, 11, 50, true);
label(880, 200, "η= 5", RED, 12, 50, true);

// edges input -> hidden (green)
conn(492, 85, 555, 64, GREEN_W); conn(492, 85, 555, 108, GREEN_W); conn(492, 85, 555, 144, GREEN_W);
conn(492, 125, 555, 64, GREEN_W); conn(492, 125, 555, 108, GREEN_W); conn(492, 125, 555, 144, GREEN_W);
conn(498, 168, 555, 64, GREEN_W); conn(498, 168, 555, 108, GREEN_W); conn(498, 168, 555, 144, GREEN_W);
// edges hidden -> output (magenta)
conn(575, 64, 703, 93, MAGENTA_W); conn(575, 64, 703, 132, MAGENTA_W);
conn(575, 108, 703, 93, MAGENTA_W); conn(575, 108, 703, 132, MAGENTA_W);
conn(575, 144, 703, 93, MAGENTA_W); conn(575, 144, 703, 132, MAGENTA_W);
// edges output -> target (red)
conn(721, 93, 779, 100, RED); conn(721, 93, 779, 128, RED);
conn(721, 132, 779, 100, RED); conn(721, 132, 779, 128, RED);

// input->hidden weight labels (green)
label(512, 72, "0.1", GREEN_W, 8, 30);
label(512, 108, "0.2", GREEN_W, 8, 30);
label(512, 140, "0.3", GREEN_W, 8, 30);
label(540, 96, "0.4", GREEN_W, 8, 30);
label(540, 148, "0.5", GREEN_W, 8, 30);
label(528, 168, "0.6", GREEN_W, 8, 30);
// hidden->output weight labels (magenta, rotated)
function rot(cx, cy, t, col) {
  txt(t, px(cx - 22), px(cy - 7), px(44), px(14), 8, col, true, "center");
}
rot(640, 60, "-0.29", MAGENTA_W); rot(650, 82, "0.458", MAGENTA_W);
rot(632, 100, "-0.218", MAGENTA_W); rot(645, 122, "0.565", MAGENTA_W);
rot(628, 140, "-0.134", MAGENTA_W); rot(648, 155, "0.669", MAGENTA_W);
rot(668, 112, "-0.445", MAGENTA_W); rot(668, 145, "-0.375", MAGENTA_W);

pres.writeFile({ fileName: VID + "/recreated_pptx/slide_031_recreated.pptx" })
  .then(() => console.log("wrote slide_031_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
