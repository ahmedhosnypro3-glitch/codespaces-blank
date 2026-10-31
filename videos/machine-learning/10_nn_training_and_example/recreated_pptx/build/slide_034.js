// slide_034.js — "Forward Calculations" (badge 34): network diagram top-right + red-bordered
// 4x9 table (O6 | O7 | Squared Error) bottom + large red down arrow at table's right edge.
// Build: NODE_PATH=$(npm root -g) node recreated_pptx/build/slide_034.js
// Geometry measured from unique_slides/slide_034.jpg (960x540 px, PX=13.33/960).

const pptxgen = require("pptxgenjs");
const FONT = "Arial";
const NUM = 34;
const TITLE = "Forward Calculations";
const PX = 13.33 / 960;
const px = v => +(v * PX).toFixed(4);

const BG = "E8E8E8", RED = "C00000", BLACK = "000000", BLUE = "0000FF",
      GREEN = "008000", DARKGREEN = "006400", PALE_YELLOW = "FFF9C4", ORANGE = "FFA500";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ========== HELPERS ==========
function lab(cx, cy, txt, color, size, wPx, bold) {
  s.addText(txt, {
    x: px(cx - (wPx || 40) / 2), y: px(cy - 8), w: px(wPx || 40), h: px(16),
    align: "center", valign: "middle", fontSize: size || 10,
    bold: bold === undefined ? true : bold, color: color, fontFace: FONT, margin: 0,
  });
}
function node(cx, cy, r, fill, stroke) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
}
function ctext(cx, cy, r, txt, color, size) {
  s.addText(txt, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    align: "center", valign: "middle", fontSize: size || 10, bold: true,
    color: color || BLACK, fontFace: FONT, margin: 0,
  });
}
function conn(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color: color, width: 1 },
  });
}
function bracket(x, yTop, yBot) {
  s.addText("[", { x: px(x), y: px(yTop), w: px(10), h: px(yBot - yTop),
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText("]", { x: px(x + 16), y: px(yTop), w: px(10), h: px(yBot - yTop),
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
}
// ========== NETWORK BOX (top-right): red border x=365-861, y=53-193 ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: px(365), y: px(53), w: px(861 - 365), h: px(193 - 53),
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
// layer labels (blue)
lab(400, 66, "Input", BLUE, 10, 46);
lab(728, 66, "Output", BLUE, 10, 50);
lab(804, 70, "Target", BLUE, 10, 46);
// input vector [1;5] with x1/x2 labels
lab(375, 99, "x\u2081", BLACK, 10, 18);
lab(378, 134, "x\u2082", BLACK, 10, 18);
bracket(391, 89, 143);
lab(402, 97, "1", BLACK, 11, 12);
lab(402, 134, "5", BLACK, 11, 12);
// hidden nodes 3,4,5 (pale yellow) at x~542
node(542, 78, 11, PALE_YELLOW, BLACK);
ctext(542, 78, 11, "3", BLACK, 9);
node(544, 118, 11, PALE_YELLOW, BLACK);
ctext(544, 118, 11, "4", BLACK, 9);
node(542, 158, 11, PALE_YELLOW, BLACK);
ctext(542, 158, 11, "5", BLACK, 9);
lab(543, 119, "O\u2084", BLUE, 8, 20);
lab(546, 187, "Bias", BLUE, 8, 30);
lab(524, 187, "O\u2085", BLUE, 8, 20);
// output nodes 6,7 at x~688
node(688, 100, 12, ORANGE, BLACK);
ctext(688, 100, 12, "6", BLACK, 9);
node(688, 144, 12, ORANGE, BLACK);
ctext(688, 144, 12, "7", BLACK, 9);
lab(728, 92, "O\u2086", BLUE, 8, 20);
lab(728, 136, "O\u2087", BLUE, 8, 20);
// target vector [0;1] with t6/t7
bracket(762, 94, 148);
lab(772, 102, "0", BLACK, 11, 12);
lab(773, 140, "1", BLACK, 11, 12);
lab(792, 101, "t\u2086", BLACK, 8, 16);
lab(793, 140, "t\u2087", BLACK, 8, 16);
// connections (thin gray) input->hidden, hidden->output
[99, 134].forEach(iy => [78, 118, 158].forEach(hy => conn(412, iy, 531, hy, "808080")));
[78, 118, 158].forEach(hy => [100, 144].forEach(oy => conn(555, hy, 676, oy, "808080")));
conn(700, 100, 762, 102, RED);
conn(700, 144, 762, 140, RED);
// eta footer
lab(826, 182, "\u03b7=5", RED, 11, 40);
// ========== TABLE (bottom): red border x=45-648, y=201-532; 4 cols x 9 rows ==========
const TX = 45, TY = 201, TW = 648 - 45, TH = 532 - 201;
// column x-boundaries (px): label col 45-205, O6 205-330, O7 330-452, SqErr 452-648
const COLS = [45, 205, 330, 452, 648];
const ROWS = 9;
const RH = TH / ROWS;
s.addShape(pres.shapes.RECTANGLE, {
  x: px(TX), y: px(TY), w: px(TW), h: px(TH),
  fill: { type: "none" }, line: { color: "FF0000", width: 2.25 },
});
// green header boxes for the 3 data columns (header row)
[[227, 294], [350, 417], [453, 597]].forEach(([a, b]) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(a), y: px(TY + 14), w: px(b - a), h: px(31),
    fill: { color: "FFFFFF" }, line: { color: GREEN, width: 1.5 },
  });
});
lab(260, TY + 30, "O\u2086", BLACK, 10, 30);
lab(384, TY + 30, "O\u2087", BLACK, 10, 30);
lab(525, TY + 30, "Squared Error", BLACK, 9, 90);
// table data
const rowLabels = ["", "Initial Weights", "Iteration 1", "Iteration 2", "Iteration 3",
  "Iteration 4", "Iteration 5", "", "Target"];
const data = [
  ["0.791", "0.791", "0.669362"],
  ["0.352", "0.835", "0.151129"],
  ["0.152", "0.875", "0.038729"],
  ["0.119", "0.895", "0.025186"],
  ["0.102", "0.908", "0.018868"],
  ["0.091", "0.917", "0.01517"],
  ["...", "...", "..."],
  ["0", "1", ""],
];
for (let r = 0; r < ROWS; r++) {
  const cy = TY + RH * (r + 0.5) + 8;
  const isTarget = r === 8, isEllipsis = r === 7, isHeader = r === 0;
  if (!isHeader) {
    lab((COLS[0] + COLS[1]) / 2, cy, rowLabels[r],
        isTarget ? "FF0000" : BLACK, 10, 110, !isEllipsis);
  }
  for (let c = 0; c < 3; c++) {
    if (isHeader) continue;
    const v = data[r - 1][c];
    if (!v) continue;
    lab((COLS[c + 1] + COLS[c + 2]) / 2, cy, v,
        isEllipsis ? "0000FF" : BLACK, 10, 80, false);
  }
}
// ========== RED DOWN ARROW at table right edge (x=583-623, y=274-443) ==========
s.addShape(pres.shapes.DOWN_ARROW, {
  x: px(583), y: px(274), w: px(623 - 583), h: px(443 - 274),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0.5 },
});

const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_034_recreated.pptx";
pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote", OUT))
  .catch(err => { console.error(err); process.exit(1); });
