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
const GREEN = "66BB6A";
const LIME = "86FF0D";
const PURPLE = "9C27B0";
const MAGENTA = "C2185B";
const WHITE = "FFFFFF";
const PANEL = "FBFEE3";
const PEACH = "FAE4CD";
const GRAY = "9E9E9E";
const GRAY_D = "616161";
const DASH = "7B7FD0";
const FONT = "Arial";

// px->in: original frame 960x540, 1px = 1/72 in
const IN = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides everything)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
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
// LEFT BLOCK — mini confusion matrix (labels) + Threshold=0.6 pill
// measured: grid x 59-166px, hlines y 81/108/136; pill x 180-309, y 108-136
// ============================================================
const mX = IN(59), mY = IN(81), mW = IN(166 - 59), mBot = IN(136);
const mLabW = IN(16);                 // left "Actual" label column
const mGridX = mX + mLabW;            // 75px
const mGridW = IN(166 - 75);          // 91px
const mColW = mGridW / 2;
const mHeadH = IN(27);                // top band y81-108: "Predicted as" y81-97, P|N y97-108
const mRowH = IN(14);                 // content rows y108-122, y122-136

// "Predicted as" sits INSIDE the matrix top band (original y90-95 over the grid)
s.addText("Predicted as", {
  x: mGridX, y: mY + IN(4), w: mGridW, h: IN(11),
  fontSize: 7, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0,
});
// matrix top border + divider between caption band and P|N band
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mY, w: mGridW, h: 0, line: { color: RED2, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: mGridX, y: mY + IN(16), w: mGridW, h: 0, line: { color: RED2, width: 0.75 } });
// rotated label: pre-rotation w becomes the vertical extent
s.addText("Actual", {
  x: IN(67) - IN(18), y: mY + IN(20), w: IN(36), h: IN(14),
  fontSize: 7, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle",
  margin: 0, rotate: 270,
});
// header row P | N (bottom of the top band)
const mPnY = mY + IN(16), mPnH = mHeadH - IN(16);
s.addShape(pptx.shapes.RECTANGLE, { x: mGridX, y: mPnY, w: mColW, h: mPnH, fill: { color: WHITE }, line: { color: RED2, width: 0.75 } });
s.addText("P", { x: mGridX, y: mPnY, w: mColW, h: mPnH, fontSize: 9, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: mGridX + mColW, y: mPnY, w: mColW, h: mPnH, fill: { color: WHITE }, line: { color: RED2, width: 0.75 } });
s.addText("N", { x: mGridX + mColW, y: mPnY, w: mColW, h: mPnH, fontSize: 9, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// row labels P / N
s.addText("P", { x: mX, y: mY + mHeadH, w: mLabW, h: mRowH, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: mX, y: mY + mHeadH + mRowH, w: mLabW, h: mRowH, fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// content cells TP | FN (green fill on TP), FP | TN
const miniCells = [
  { t: "TP", fill: LIME, tc: DARK },
  { t: "FN", fill: WHITE, tc: RED2 },
  { t: "FP", fill: WHITE, tc: RED2 },
  { t: "TN", fill: WHITE, tc: RED2 },
];
miniCells.forEach((c, i) => {
  const cx = mGridX + (i % 2) * mColW;
  const cy = mY + mHeadH + Math.floor(i / 2) * mRowH;
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: mColW, h: mRowH, fill: { color: c.fill }, line: { color: RED2, width: 0.75 } });
  s.addText(c.t, { x: cx, y: cy, w: mColW, h: mRowH, fontSize: 8, bold: true, color: c.tc, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
});

// Threshold=0.6 pill: peach fill, red border, dark-red bold text; right of mini matrix, same band
const pX = IN(180), pY = IN(108), pW = IN(129), pH = IN(28);
s.addShape(pptx.shapes.RECTANGLE, { x: pX, y: pY, w: pW, h: pH, fill: { color: PEACH }, line: { color: RED2, width: 1.25 } });
s.addText("Threshold=0.6", { x: pX, y: pY, w: pW, h: pH, fontSize: 12, bold: true, color: "8A2020", fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// LEFT BLOCK — numeric confusion matrix
// measured: x 94-230px, y 146-222px; vlines 94/130/179/230, hlines 156/176/199/222
// ============================================================
const nX = IN(94), nY = IN(146), nGridX = IN(130), nGridW = IN(230 - 130);
const nLabW = IN(130 - 94);
const nColW = nGridW / 2;            // 49px each
const nHeadH = IN(20);                // y156-176
const nRowH = IN(23);                 // y176-199, y199-222

s.addText("Predicted as", {
  x: nGridX, y: nY, w: nGridW, h: IN(10),
  fontSize: 9, bold: true, color: RED2, fontFace: FONT, align: "center", margin: 0,
});
s.addText("Actual", {
  x: IN(112) - IN(24), y: nY + IN(10) + nHeadH + nRowH - IN(7), w: IN(48), h: IN(14),
  fontSize: 8, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270,
});
s.addShape(pptx.shapes.RECTANGLE, { x: nGridX, y: nY + IN(10), w: nColW, h: nHeadH, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
s.addText("P", { x: nGridX, y: nY + IN(10), w: nColW, h: nHeadH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: nGridX + nColW, y: nY + IN(10), w: nColW, h: nHeadH, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
s.addText("N", { x: nGridX + nColW, y: nY + IN(10), w: nColW, h: nHeadH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("P", { x: nX, y: nY + IN(10) + nHeadH, w: nLabW, h: nRowH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("N", { x: nX, y: nY + IN(10) + nHeadH + nRowH, w: nLabW, h: nRowH, fontSize: 10, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// values: 3 blue, 2 red / 1 red, 5 blue
const numCells = [
  { t: "3", tc: BLUE_D },
  { t: "2", tc: "9C1B33" },
  { t: "1", tc: "9C1B33" },
  { t: "5", tc: BLUE_D },
];
numCells.forEach((c, i) => {
  const cx = nGridX + (i % 2) * nColW;
  const cy = nY + IN(10) + nHeadH + Math.floor(i / 2) * nRowH;
  s.addShape(pptx.shapes.RECTANGLE, { x: cx, y: cy, w: nColW, h: nRowH, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
  s.addText(c.t, { x: cx, y: cy, w: nColW, h: nRowH, fontSize: 14, bold: true, color: c.tc, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
});

// ============================================================
// PIPELINE PANEL — beige pill x 328-840px, y 102-194px
// ============================================================
const pnX = IN(328), pnY = IN(102), pnW = IN(512), pnH = IN(92);
s.addShape(pptx.shapes.RECTANGLE, { x: pnX, y: pnY, w: pnW, h: pnH, fill: { color: PANEL }, line: { color: "CEB396", width: 1 } });

const fy = IN(150); // flow center line ~150px

// helper: hollow red-outline white-filled arrow
function arrow(x0, x1, y) {
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: y - 0.025, w: x1 - x0 - 0.10, h: 0.05, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x1 - 0.10, y: y - 0.065, w: 0.10, h: 0.13, fill: { color: WHITE }, line: { color: RED2, width: 1 }, rotate: 90 });
}

// Test Sample box x 355-440px, y 130-170px, with airplane sketch
const tsX = IN(355), tsY = IN(130), tsW = IN(85), tsH = IN(40);
s.addText("Test\nSample", { x: tsX, y: pnY + IN(0), w: tsW, h: IN(24), fontSize: 9, bold: true, color: DARK, fontFace: FONT, align: "center", margin: 0, lineSpacing: 10 });
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: tsY, w: tsW, h: tsH, fill: { color: WHITE }, line: { color: RED2, width: 1 } });
// original airplane sketch cropped from the frame, embedded at measured size (74x32px)
s.addImage({ path: __dirname + "/assets/slide025/ts_icon.png", x: tsX + IN(6), y: tsY + IN(4), w: IN(74), h: IN(32) });

arrow(tsX + tsW, IN(448), fy);

// Model box: dark red fill x 445-571px, y 121-180px (original #9F0000)
const mdX = IN(445), mdY = IN(121), mdW = IN(126), mdH = IN(59);
s.addShape(pptx.shapes.RECTANGLE, { x: mdX, y: mdY, w: mdW, h: mdH, fill: { color: "9F0000" }, line: { type: "none" } });
s.addText("Model", { x: mdX, y: mdY + IN(2), w: IN(42), h: IN(20), fontSize: 12, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("[Any value] ~ (0, +\u221E)", { x: mdX, y: mdY + IN(38), w: mdW, h: IN(18), fontSize: 8, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Model icon: verbatim crop of the original's light-purple sigmoid circle (orig x526-571, y124-168)
s.addImage({ path: __dirname + "/assets/slide025/model_icon.png", x: IN(526), y: IN(124), w: IN(45), h: IN(44) });

arrow(IN(571), IN(585) - 0.0, fy);

// Predicted Value caption centered directly above the (0 --- 1) box; box x 585-640px
const pvX = IN(585), pvW = IN(55);
s.addText("Predicted Value", { x: pvX, y: pnY + IN(2), w: pvW, h: IN(11), fontSize: 7, bold: true, color: BLUE_D, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: pvX, y: fy - IN(11), w: pvW, h: IN(22), fill: { color: WHITE }, line: { color: BLUE_D, width: 1 } });
s.addText("(0 --- 1)", { x: pvX, y: fy - IN(11), w: pvW, h: IN(22), fontSize: 8, bold: true, color: BLUE_D, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

arrow(pvX + pvW, IN(668), fy);

// Threshold module: pale-pink rounded vertical pill x 673-738px, y 109-188px, rotated red text
const thX = IN(673), thY = IN(109), thW = IN(65), thH = IN(79);
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: thX, y: thY, w: thW, h: thH, fill: { color: "F8CECC" }, line: { color: RED2, width: 1.25 } });
s.addText("Threshold (e.g. 0.5)", { x: thX, y: thY, w: thW, h: thH, fontSize: 7, bold: true, color: RED2, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });

// Red X-fork: two diagonal arrows from threshold box right edge to the ovals
const fkX = thX + thW;
s.addShape(pptx.shapes.LINE, { x: fkX + IN(2), y: fy - IN(6), w: IN(24), h: -IN(22), line: { color: RED2, width: 1.5, endArrowType: "triangle" } });
s.addShape(pptx.shapes.LINE, { x: fkX + IN(2), y: fy + IN(6), w: IN(24), h: IN(22), line: { color: RED2, width: 1.5, endArrowType: "triangle" } });

// Class I (green) / Class II (purple) ovals INSIDE panel right: x 760-833px
const clX = IN(760), clW = IN(73);
s.addShape(pptx.shapes.OVAL, { x: clX, y: IN(112), w: clW, h: IN(34), fill: { color: "D3FFE4" }, line: { color: "D3FFE4", width: 1 } });
s.addText("Class I", { x: clX, y: IN(112), w: clW, h: IN(34), fontSize: 10, bold: true, color: DARK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addShape(pptx.shapes.OVAL, { x: clX, y: IN(158), w: clW, h: IN(34), fill: { color: "F8C8FA" }, line: { color: "F8C8FA", width: 1 } });
s.addText("Class II", { x: clX, y: IN(158), w: clW, h: IN(34), fontSize: 10, bold: true, color: DARK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// BOTTOM PLOT — airplane scatter + full-width red axis + dashed threshold
// axis: y 436px, x 86-889px, arrowheads both ends; dashed line x 557px
// ============================================================
const axL = IN(86), axR = IN(889), axY = IN(436);
const thrX = IN(557);

// dashed threshold line: from above the plot down past the axis (blue-gray + faint purple offset)
s.addShape(pptx.shapes.LINE, { x: thrX, y: IN(210), w: 0, h: IN(460 - 210), line: { color: DASH, width: 1.5, dashType: "dash" } });
s.addShape(pptx.shapes.LINE, { x: thrX + IN(3), y: IN(210), w: 0, h: IN(460 - 210), line: { color: PURPLE, width: 0.75, dashType: "dash" } });

// airplanes: real doodles cropped from the original frame, embedded at measured bbox (1px = 1/72in)
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

// horizontal red axis: plain left terminus (tick), arrowhead at right end only
s.addShape(pptx.shapes.LINE, { x: axL, y: axY, w: axR - axL - IN(8), h: 0, line: { color: RED2, width: 2 } });
s.addShape(pptx.shapes.LINE, { x: axL, y: axY - IN(5), w: 0, h: IN(10), line: { color: RED2, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: axR - IN(10), y: axY - IN(5), w: IN(12), h: IN(10), fill: { color: RED2 }, line: { type: "none" }, rotate: 90 });

// ticks: labeled 0.0/0.5/1.0 + minor every 0.1
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
