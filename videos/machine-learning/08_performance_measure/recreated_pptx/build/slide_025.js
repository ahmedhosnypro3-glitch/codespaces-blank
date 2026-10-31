const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const RED2 = "B03A2E";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE_D = "1A237E";
const LIME = "86FF0D";
const GREEN_T = "2E7D32";
const WHITE = "FFFFFF";
const PANEL = "FBFEE3";
const PEACH = "FAE4CD";
const DASH = "7B7FD0";
const PURPLE = "9C27B0";
const FONT = "Arial";

// px->in: original frame 960x540, 1px = 1/72 in
const IN = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME (root AGENTS.md) + inner red content frame (original x62..900, y82..436)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: IN(62), y: IN(82), w: IN(838), h: IN(354),
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("25", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED2, fontFace: FONT, margin: 0,
});

// ============================================================
// LEFT BLOCK — mini confusion matrix (labels)
// both matrices share outer left x84 and grid left x130 (measured);
// top band y81-108 holds "Predicted as" (y85-96) above P|N (y97-108)
// ============================================================
const mX = IN(84), mY = IN(81), mBot = IN(136);
const mLabW = IN(46);                 // label col x84-130
const mGridX = IN(130), mGridW = IN(36), mColW = IN(18);
const mHeadH = IN(27);                // y81-108
const mRowH = IN(14);                 // y108-122, y122-136

s.addText("Predicted as", {
  x: mGridX, y: mY + IN(4), w: mGridW, h: IN(11),
  fontSize: 6, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0,
});
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mY, w: mGridW, h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mY + IN(16), w: mGridW, h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mBot, w: mGridW, h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mY, w: 0, h: mHeadH + mRowH * 2, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX + mGridW, y: mY, w: 0, h: mHeadH + mRowH * 2, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX + mColW, y: mY + IN(16), w: 0, h: mHeadH - IN(16) + mRowH * 2, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mY + mHeadH, w: mGridW, h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mY + mHeadH + mRowH, w: mGridW, h: 0, line: { color: RED2, width: 0.75 } });

s.addText("Actual", {
  x: IN(58), y: mY + IN(20), w: IN(36), h: IN(14),
  fontSize: 7, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle",
  margin: 0, rotate: 270,
});
// header P | N (bottom of top band, y97-108)
const mPnY = mY + IN(16), mPnH = mHeadH - IN(16);
s.addText("P", { x: mGridX, y: mPnY, w: mColW, h: mPnH, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: mGridX + mColW, y: mPnY, w: mColW, h: mPnH, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// row labels P / N
s.addText("P", { x: mX, y: mY + mHeadH, w: mLabW, h: mRowH, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: mX, y: mY + mHeadH + mRowH, w: mLabW, h: mRowH, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// content cells: TP lime, FN red text, FP blue text, TN green text (per original ink colors)
const miniCells = [
  { t: "TP", fill: LIME, tc: DARK },
  { t: "FN", fill: WHITE, tc: RED2 },
  { t: "FP", fill: WHITE, tc: BLUE_D },
  { t: "TN", fill: WHITE, tc: GREEN_T },
];
miniCells.forEach((c, i) => {
  const cx = mGridX + (i % 2) * mColW;
  const cy = mY + mHeadH + Math.floor(i / 2) * mRowH;
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: mColW, h: mRowH, fill: { color: c.fill }, line: { type: "none" } });
  s.addText(c.t, { x: cx, y: cy, w: mColW, h: mRowH, fontSize: 7, bold: true, color: c.tc, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
});

// Threshold=0.6 pill right of mini matrix, same band
const pX = IN(180), pY = IN(108), pW = IN(129), pH = IN(28);
s.addShape(pptx.shapes.RECTANGLE, { x: pX, y: pY, w: pW, h: pH, fill: { color: PEACH }, line: { color: RED2, width: 1.25 } });
s.addText("Threshold=0.6", { x: pX, y: pY, w: pW, h: pH, fontSize: 12, bold: true, color: "8A2020", fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// LEFT BLOCK — numeric confusion matrix; outer left x84, grid x130-230, y146-222
// caption "Predicted as" inside top band y146-156; header P|N y156-176; rows y176-199, y199-222
// ============================================================
const nX = IN(84), nY = IN(146), nGridX = IN(130), nGridW = IN(100);
const nLabW = IN(46), nColW = nGridW / 2;
const nHeadH = IN(20), nRowH = IN(23);

s.addText("Predicted as", {
  x: nGridX, y: nY, w: nGridW, h: IN(10),
  fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0,
});
s.addShape(pptx.shapes.LINE, { x: nGridX, y: nY + IN(10), w: nGridW, h: 0, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: nGridX, y: nY + IN(10) + nHeadH, w: nGridW, h: 0, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: nGridX, y: nY + IN(10) + nHeadH + nRowH, w: nGridW, h: 0, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: nGridX, y: nY + IN(76), w: nGridW, h: 0, line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: nGridX, y: nY + IN(10), w: 0, h: IN(66), line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: nGridX + nGridW, y: nY + IN(10), w: 0, h: IN(66), line: { color: RED2, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: nGridX + nColW, y: nY + IN(10), w: 0, h: IN(66), line: { color: RED2, width: 1 } });

s.addText("Actual", {
  x: IN(58), y: nY + IN(31), w: IN(36), h: IN(14),
  fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle",
  margin: 0, rotate: 270,
});
s.addText("P", { x: nGridX, y: nY + IN(10), w: nColW, h: nHeadH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nGridX + nColW, y: nY + IN(10), w: nColW, h: nHeadH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("P", { x: nX, y: nY + IN(10) + nHeadH, w: nLabW, h: nRowH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX, y: nY + IN(10) + nHeadH + nRowH, w: nLabW, h: nRowH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const numCells = [
  { t: "3", tc: "C00000" },
  { t: "2", tc: "7A1024" },
  { t: "1", tc: "1A1A1A" },
  { t: "5", tc: BLUE_D },
];
numCells.forEach((c, i) => {
  const cx = nGridX + (i % 2) * nColW;
  const cy = nY + IN(10) + nHeadH + Math.floor(i / 2) * nRowH;
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: nColW, h: nRowH, fill: { color: WHITE }, line: { type: "none" } });
  s.addText(c.t, { x: cx, y: cy, w: nColW, h: nRowH, fontSize: 14, bold: true, color: c.tc, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
});

// ============================================================
// PIPELINE PANEL — cream x328-840 y102-194
// ============================================================
const pnX = IN(328), pnY = IN(102), pnW = IN(512), pnH = IN(92);
s.addShape(pptx.shapes.RECTANGLE, { x: pnX, y: pnY, w: pnW, h: pnH, fill: { color: PANEL }, line: { color: "CEB396", width: 1 } });

const fy = IN(150);

function arrow(x0, x1, y) {
  s.addShape(pptx.shapes.RIGHT_ARROW, { x: x0, y: y - IN(5), w: x1 - x0, h: IN(10), fill: { color: WHITE }, line: { color: RED2, width: 1.5 } });
}

// Test Sample box x355-440 y130-170 with verbatim plane sketch crop (74x32px)
const tsX = IN(355), tsY = IN(130), tsW = IN(85), tsH = IN(40);
s.addText("Test\nSample", { x: tsX, y: pnY, w: tsW, h: IN(24), fontSize: 9, bold: true, color: DARK, fontFace: FONT, align: "center", margin: 0, lineSpacing: 10 });
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: tsY, w: tsW, h: tsH, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
s.addImage({ path: __dirname + "/assets/slide025/ts_icon.png", x: tsX + IN(6), y: tsY + IN(4), w: IN(74), h: IN(32) });

arrow(tsX + tsW, IN(448), fy);

// Model box x445-571 y121-180, original fill #9F0000
const mdX = IN(445), mdY = IN(121), mdW = IN(126), mdH = IN(59);
s.addShape(pptx.shapes.RECTANGLE, { x: mdX, y: mdY, w: mdW, h: mdH, fill: { color: "9F0000" }, line: { type: "none" } });
s.addText("Model", { x: mdX, y: mdY + IN(2), w: IN(42), h: IN(20), fontSize: 12, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// caption kept left of the icon so it never collides (orig caption x455-525 y170-179)
s.addText("[Any value] → (0, +1)", { x: mdX, y: mdY + IN(46), w: IN(78), h: IN(13), fontSize: 8, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0, wordWrap: true });
// verbatim crop of the original's light-purple sigmoid circle (orig x526-571 y124-168)
s.addImage({ path: __dirname + "/assets/slide025/model_icon.png", x: IN(526), y: IN(124), w: IN(45), h: IN(44) });

arrow(IN(571), IN(585), fy);

// "Predicted Value" stacked on two lines above the (0 --- 1) box; box x585-640
const pvX = IN(585), pvW = IN(55);
s.addText("Predicted\nValue", { x: pvX, y: pnY + IN(1), w: pvW, h: IN(22), fontSize: 7, bold: true, color: BLUE_D, fontFace: FONT, align: "center", valign: "top", margin: 0, lineSpacing: 9 });
s.addShape(pptx.shapes.RECTANGLE, { x: pvX, y: fy - IN(11), w: pvW, h: IN(22), fill: { color: WHITE }, line: { color: BLUE_D, width: 1 } });
s.addText("(0 --- 1)", { x: pvX, y: fy - IN(11), w: pvW, h: IN(22), fontSize: 8, bold: true, color: BLUE_D, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

arrow(pvX + pvW, IN(668), fy);

// Threshold module: pale-pink square-cornered vertical pill x673-738 y109-188, rotated red text
const thX = IN(673), thY = IN(109), thW = IN(65), thH = IN(79);
s.addShape(pptx.shapes.RECTANGLE, { x: thX, y: thY, w: thW, h: thH, fill: { color: "F8CECC" }, line: { color: RED2, width: 1.25 } });
s.addText("Threshold (e.g. 0.5)", { x: thX, y: thY, w: thW, h: thH, fontSize: 7, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });

// Red fork arrows with triangular heads to the two class ovals
const fkX = thX + thW;
s.addShape(pptx.shapes.RIGHT_ARROW, { x: fkX + IN(2) - IN(11), y: fy - IN(17) - IN(5), w: IN(24), h: IN(10), fill: { color: RED2 }, line: { color: RED2, width: 1 }, rotate: -42 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: fkX + IN(2) - IN(11), y: fy + IN(7) - IN(5), w: IN(24), h: IN(10), fill: { color: RED2 }, line: { color: RED2, width: 1 }, rotate: 42 });

// Class I (pastel green, dark text) / Class II (light orchid, dark text) ovals x760-833
const clX = IN(760), clW = IN(73);
s.addShape(pptx.shapes.OVAL, { x: clX, y: IN(112), w: clW, h: IN(34), fill: { color: "D3FFE4" }, line: { color: "D3FFE4", width: 1 } });
s.addText("Class I", { x: clX, y: IN(112), w: clW, h: IN(34), fontSize: 10, bold: true, color: DARK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: clX, y: IN(158), w: clW, h: IN(34), fill: { color: "F8C8FA" }, line: { color: "F8C8FA", width: 1 } });
s.addText("Class II", { x: clX, y: IN(158), w: clW, h: IN(34), fontSize: 10, bold: true, color: DARK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// BOTTOM PLOT — verbatim airplane crops + red axis + dashed threshold
// ============================================================
const axL = IN(86), axR = IN(889), axY = IN(436);
const thrX = IN(557);

s.addShape(pptx.shapes.LINE, { x: thrX, y: IN(210), w: 0, h: IN(248), line: { color: DASH, width: 1.5, dashType: "dash" } });
s.addShape(pptx.shapes.LINE, { x: thrX + IN(3), y: IN(210), w: 0, h: IN(248), line: { color: PURPLE, width: 0.75, dashType: "dash" } });

const planeCrops = [
  [630, 293, 777, 358], [90, 327, 217, 387], [768, 340, 877, 404], [759, 224, 865, 306],
  [349, 288, 454, 372], [109, 231, 217, 291], [193, 282, 301, 334], [325, 224, 430, 287],
  [205, 358, 294, 409], [482, 285, 556, 345], [499, 367, 556, 411], [560, 365, 609, 403],
  [560, 289, 590, 329],
];
planeCrops.forEach((b, i) => {
  s.addImage({
    path: __dirname + "/assets/slide025/plane_" + String(i).padStart(2, "0") + ".png",
    x: IN(b[0]), y: IN(b[1]), w: IN(b[2] - b[0]), h: IN(b[3] - b[1]),
  });
});

// horizontal red axis, right arrowhead only
s.addShape(pptx.shapes.LINE, { x: axL, y: axY, w: axR - axL - IN(8), h: 0, line: { color: RED2, width: 2 } });
s.addShape(pptx.shapes.LINE, { x: axL, y: axY - IN(5), w: 0, h: IN(10), line: { color: RED2, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: axR - IN(10), y: axY - IN(5), w: IN(12), h: IN(10), fill: { color: RED2 }, line: { type: "none" }, rotate: 90 });

for (let i = 0; i <= 10; i++) {
  const f = i / 10;
  const x = axL + (axR - axL) * f;
  const major = i === 0 || i === 5 || i === 10;
  s.addShape(pptx.shapes.LINE, { x: x, y: axY, w: 0, h: major ? IN(10) : IN(6), line: { color: RED2, width: major ? 2 : 1 } });
  if (major) {
    s.addText(f === 0 ? "0.0" : f === 0.5 ? "0.5" : "1.0", {
      x: x - IN(12), y: axY + IN(12), w: IN(24), h: IN(12),
      fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0,
    });
  }
}

// ---- OUTPUT ----
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_025_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
