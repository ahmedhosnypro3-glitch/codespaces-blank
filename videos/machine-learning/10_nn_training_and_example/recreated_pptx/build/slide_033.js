// slide_033.js — "Initialized weights" vs "Updated weights (after iteration # 10)" (badge 33)
// Two stacked red-bordered panels, each with the same 2-3-2 network + target matrix.
// Build: NODE_PATH=$(npm root -g) node recreated_pptx/build/slide_033.js   (from video dir)
// Geometry measured from unique_slides/slide_033.jpg (960x540 px, PX=13.33/960 in/px).

const pptxgen = require("pptxgenjs");
const FONT = "Arial";
const NUM = 33;
const TITLE = "Initialized weights";
const PX = 13.33 / 960;
const px = v => +(v * PX).toFixed(4);

const BG = "E8E8E8", RED = "C00000", BLACK = "000000", BLUE = "0000FF";
const PALE_YELLOW = "FFF9C4", ORANGE = "FFA500";

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

// ========== HELPERS (all coords in source px, converted) ==========
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
function lab(cx, cy, txt, color, size, wPx) {
  s.addText(txt, {
    x: px(cx - (wPx || 40) / 2), y: px(cy - 8), w: px(wPx || 40), h: px(16),
    align: "center", valign: "middle", fontSize: size || 10, bold: true,
    color: color, fontFace: FONT, margin: 0,
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
// ========== PANEL DRAWING ==========
// Panel geometry (measured): top y=89-285, bottom y=330-525, x=101-823 px.
const PANELS = [
  { y0: 89, y1: 285, header: null },
  { y0: 330, y1: 525, header: "Updated weights (after iteration # 10)" },
];

// Per-panel network layout (px, relative to slide; measured from frame)
function drawNet(p, wIn, wHid, wOut, targetVals) {
  const X = { inL: 116, inV: 150, inN: 190, hid: 348, out: 600, tgtB: 643, tgt2: 747 };
  const yTop = p.y0 + 55, yMid = p.y0 + 112, yBot = p.y0 + 169;
  const yBias = p.y0 + 161;
  const oY1 = p.y0 + 55, oY2 = p.y0 + 117;

  // layer labels
  lab(142, p.y0 + 19, "Input", BLUE, 10, 46);
  lab(613, p.y0 + 21, "Output", BLUE, 10, 48);
  lab(796, p.y0 + 54, "Target", BLACK, 10, 46);

  // input column: x1/x2 labels, bracket vector [1;5], nodes
  lab(116, yTop + 10, "x₁", BLACK, 10, 20);
  lab(115, yMid + 46, "x₂", BLACK, 10, 20);
  bracket(138, yTop, yBot + 4);
  lab(150, yTop + 8, "1", BLACK, 11, 12);
  lab(150, yMid + 48, "5", BLACK, 11, 12);
  node(X.inN, yTop, 6, BLACK, BLACK);
  node(X.inN, yMid + 64, 6, BLACK, BLACK);
  lab(X.inN + 14, yBias, "Bias", BLUE, 9, 36);
  node(X.inN, yBias + 6, 6, BLACK, BLACK);

  // hidden nodes 3,4,5 (pale yellow)
  const hYs = [yTop, yMid, yBot];
  hYs.forEach((y, i) => {
    node(X.hid, y, 15, PALE_YELLOW, BLACK);
    ctext(X.hid, y, 15, String(i + 3), BLACK, 10);
    lab(X.hid + 2, y - 26, "O" + ["\u2083", "\u2084", "\u2085"][i], BLUE, 9, 24);
  });

  // output nodes 6,7 (orange)
  node(X.out, oY1, 13, ORANGE, BLACK);
  ctext(X.out, oY1, 13, "6", BLACK, 10);
  node(X.out, oY2, 13, ORANGE, BLACK);
  ctext(X.out, oY2, 13, "7", BLACK, 10);
  lab(X.out + 7, oY1 - 4, "O\u2086", BLUE, 9, 24);
  lab(X.out + 7, oY2 - 4, "O\u2087", BLUE, 9, 24);

  // target matrix: two bracketed columns (O-col values, target values) + t6/t7
  bracket(X.tgtB - 6, oY1 - 14, oY2 + 14);
  lab(672, oY1, targetVals[0], BLACK, 10, 30);
  lab(672, oY2, targetVals[1], BLACK, 10, 30);
  bracket(X.tgt2 - 6, oY1 - 14, oY2 + 14);
  lab(760, oY1, "0", BLACK, 10, 12);
  lab(760, oY2, "1", BLACK, 10, 12);
  lab(788, oY1 - 6, "t\u2086", BLACK, 9, 20);
  lab(790, oY2 - 6, "t\u2087", BLACK, 9, 20);

  // connections: input nodes -> hidden; hidden -> output; output -> target
  const inYs = [yTop, yMid + 64, yBias + 6];
  inYs.forEach(iy => hYs.forEach(hy => conn(X.inN + 6, iy, X.hid - 15, hy, "808080")));
  hYs.forEach(hy => [oY1, oY2].forEach(oy => conn(X.hid + 15, hy, X.out - 13, oy, "808080")));
  conn(X.out + 13, oY1, X.tgtB - 16, oY1, RED);
  conn(X.out + 13, oY2, X.tgtB - 16, oY2, RED);

  // weight labels on input->hidden edges (green) and hidden->output (purple)
  wIn.forEach((w, i) => {
    const col = Math.floor(i / 3), row = i % 3;
    lab(250 + col * 8, (inYs[col] + hYs[row]) / 2 - 4, w, "008000", 8, 34);
  });
  wHid.forEach((w, i) => {
    const row = Math.floor(i / 2), col = i % 2;
    lab(470, (hYs[row] + [oY1, oY2][col]) / 2 - 4, w, "800080", 8, 40);
  });
  wOut.forEach((w, i) => {
    lab(620 + i * 30, (i === 0 ? oY1 : oY2) + 14, w, "800080", 8, 40);
  });

  // eta footer
  lab(727, p.y1 - 28, "\u03b7 = 5", RED, 12, 50);
}

// ========== PANELS ==========
PANELS.forEach((p, pi) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(101), y: px(p.y0), w: px(823 - 101), h: px(p.y1 - p.y0),
    fill: { type: "none" }, line: { color: RED, width: 1.5 },
  });
  if (p.header) lab(192, p.y0 - 21, p.header, RED, 11, 170);
});
// ========== WEIGHTS + BUILD CALLS ==========
// Top panel (initialized) input->hidden weights, row-major by source (x1,x2,Bias) x target (3,4,5)
const wInTop = ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.1", "0.1", "0.1"];
const wHidTop = ["0.3", "0.3", "0.4", "0.4", "0.5", "0.5"]; // 3->6,3->7,4->6,4->7,5->6,5->7
const wOutTop = ["0.2", "0.2"]; // Bias->6, Bias->7
const tgtTop = ["0.791", "0.791"];

// Bottom panel (after iteration #10) — from isolated vision analysis
const wInBot = ["0.155", "0.215", "0.305", "0.675", "0.575", "0.625", "0.115", "0.115", "0.105"];
const wHidBot = ["-0.999", "-0.835", "-0.93", "-0.943", "-0.856", "-1.2"];
const wOutBot = ["1.05", "-0.77"];
const tgtBot = ["0.064", "0.939"];

let wIn = wInTop, wHid = wHidTop, wOut = wOutTop;
PANELS.forEach((p, pi) => {
  if (pi === 1) { wIn = wInBot; wHid = wHidBot; wOut = wOutBot; }
  drawNet(p, wIn, wHid, wOut, pi === 0 ? tgtTop : tgtBot);
});

const OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_033_recreated.pptx";
pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote", OUT))
  .catch(err => { console.error(err); process.exit(1); });
