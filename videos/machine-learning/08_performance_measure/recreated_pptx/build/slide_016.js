const pptxgen = require("pptxgenjs");
const fs = require("fs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

// ---- palette (measured on unique_slides/slide_016.jpg) ----
const BG = "E8E8E8";
const HOUSE_RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const MAROON = "A50000";      // title / labels / equation ink
const NODE_RED = "B03030";
const NODE_GREEN = "2E8B3C";
const PREC_FILL = "FFF9C4";   // pale yellow (Precision box)
const PREC_LINE = "BF8F00";   // amber border
const REC_FILL = "CCECFF";    // pale blue (Recall box)
const REC_LINE = "1F5FA8";    // blue border
const GREEN_FILL = "EAFBE6";  // F1 box, very pale green
const GREEN_LINE = "008000";
const ORANGE_FILL = "FFE0B2";
const ORANGE_LINE = "C55A11";
const GRAY_LINE = "BFBFBF";
const ROW1_FILL = "FFF6CC";   // Precision calc rows (pale yellow)
const ROW2_FILL = "DFF3FB";   // Recall calc rows (pale blue)
const ROW3_FILL = "E8FBF3";   // F1 calc rows (very pale green)
const WHITE = "FFFFFF";
const BLACK = "000000";
const CONN_BLUE = "1F4E79";   // tree connector blue
const GRAY = "808080";
const FONT = "Arial";

const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
const EQ = JSON.parse(fs.readFileSync(ASSETS + "/eq_016_manifest.json", "utf8"));

const px = (v) => v / 72;   // original frame 960x540 px, 1px = 1pt

let s = pptx.addSlide();
s.background = { color: BG };

// ================= HOUSE CHROME =================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("16", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Combine Precision and Recall in one number", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.7,
  align: "center", valign: "middle",
  fontSize: 38, bold: true, color: MAROON, fontFace: FONT, margin: 0,
});

// ================= TREE DIAGRAMS =================
const R = px(20);   // node circle radius, ~40px diameter like the original

function node(cx, cy, label, fill) {
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx) - R, y: px(cy) - R, w: R * 2, h: R * 2,
    fill: { color: fill }, line: { color: fill, width: 0.75 },
  });
  s.addText(label, {
    x: px(cx) - R, y: px(cy) - R, w: R * 2, h: R * 2,
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
}

// blue connector with a small arrowhead at the child end
function connector(x1, y1, x2, y2) {
  const dx = px(x2) - px(x1), dy = px(y2) - px(y1);
  s.addShape(pptx.shapes.LINE, {
    x: Math.min(px(x1), px(x2)), y: Math.min(px(y1), px(y2)),
    w: Math.abs(dx), h: Math.abs(dy),
    line: { color: CONN_BLUE, width: 1.5 },
    flipH: dx < 0, flipV: dy < 0,
  });
  const len = Math.hypot(dx, dy);
  const ux = dx / len, uy = dy / len;           // unit, slide coords y-down
  const hw = px(5), hh = px(7);                  // half-width, half-height (unrotated)
  const ang = Math.atan2(ux, -uy) * 180 / Math.PI; // clockwise deg from "up"
  const cxm = px(x2) - ux * hh, cym = px(y2) - uy * hh; // shape center
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cxm - hw, y: cym - hh, w: hw * 2, h: hh * 2,
    fill: { color: CONN_BLUE }, line: { color: CONN_BLUE, width: 0.5 },
    rotate: ang,
  });
}

// side-view line-art propeller plane, nose right, red nose cone
function drawPlane(cx, cy, w) {
  const h = w * 0.62;
  const X = px(cx) - px(w) / 2, Y = px(cy) - px(h) / 2;
  const P = (v) => px(v);
  // fuselage (pill)
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: X, y: Y + P(h) * 0.32, w: P(w), h: P(h) * 0.38,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, adjustValue: 0.5,
  });
  // red nose cone
  s.addShape(pptx.shapes.OVAL, {
    x: X + P(w) - P(h) * 0.22, y: Y + P(h) * 0.32, w: P(h) * 0.26, h: P(h) * 0.38,
    fill: { color: MAROON }, line: { color: GRAY, width: 0.75 },
  });
  // propeller
  s.addShape(pptx.shapes.LINE, {
    x: X + P(w) + P(1), y: Y + P(h) * 0.10, w: 0, h: P(h) * 0.82,
    line: { color: GRAY, width: 1.5 },
  });
  // main wing (down)
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X + P(w) * 0.38, y: Y + P(h) * 0.66, w: P(w) * 0.24, h: P(h) * 0.34,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 180,
  });
  // top wing (up)
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X + P(w) * 0.38, y: Y + P(h) * 0.02, w: P(w) * 0.24, h: P(h) * 0.32,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 },
  });
  // tail fin
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X + P(w) * 0.02, y: Y + P(h) * 0.04, w: P(w) * 0.16, h: P(h) * 0.34,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 },
  });
  // cockpit window
  s.addShape(pptx.shapes.OVAL, {
    x: X + P(w) * 0.70, y: Y + P(h) * 0.36, w: P(h) * 0.12, h: P(h) * 0.16,
    fill: { color: "9DC3E6" }, line: { color: GRAY, width: 0.75 },
  });
  // windows
  for (let i = 0; i < 3; i++) {
    s.addShape(pptx.shapes.OVAL, {
      x: X + P(w) * (0.28 + i * 0.13), y: Y + P(h) * 0.44, w: P(h) * 0.11, h: P(h) * 0.11,
      fill: { color: WHITE }, line: { color: GRAY, width: 0.75 },
    });
  }
}

function tree(x0, x1, topPos, topNeg, kids, labels) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(100), w: px(x1 - x0), h: px(345 - 100),
    fill: { color: BG }, line: { color: "8B2E2F", width: 1.5 },
  });
  s.addText("Positive", {
    x: px(topPos.cx) - px(45), y: px(104), w: px(90), h: px(20),
    align: "center", valign: "middle",
    fontSize: 17, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
  s.addText("Negative", {
    x: px(topNeg.cx) - px(45), y: px(104), w: px(90), h: px(20),
    align: "center", valign: "middle",
    fontSize: 17, bold: true, color: NODE_GREEN, fontFace: FONT, margin: 0,
  });
  drawPlane(topPos.cx, 148, 62);
  drawPlane(topNeg.cx, 148, 62);
  node(topPos.cx, topPos.cy, topPos.label, NODE_RED);
  node(topNeg.cx, topNeg.cy, topNeg.label, NODE_GREEN);
  const from = [topPos, topPos, topNeg, topNeg];
  for (let i = 0; i < 4; i++) {
    connector(from[i].cx, from[i].cy + 20, kids[i].cx, kids[i].cy - 21);
    node(kids[i].cx, kids[i].cy, kids[i].label, kids[i].red ? NODE_RED : NODE_GREEN);
  }
  const labCols = [NODE_RED, NODE_GREEN, NODE_GREEN, NODE_RED];
  for (let i = 0; i < 4; i++) {
    s.addText(labels[i], {
      x: px(kids[i].cx) - px(20), y: px(318), w: px(40), h: px(16),
      align: "center", valign: "middle",
      fontSize: 12, bold: true, color: labCols[i], fontFace: FONT, margin: 0,
    });
  }
}

tree(75, 415,
  { cx: 140, cy: 195, label: "30" }, { cx: 330, cy: 195, label: "70" },
  [
    { cx: 95, cy: 290, label: "20", red: true },
    { cx: 185, cy: 290, label: "10", red: false },
    { cx: 285, cy: 290, label: "59", red: false },
    { cx: 380, cy: 290, label: "11", red: true },
  ],
  ["TP", "FN", "TN", "FP"]);

tree(435, 760,
  { cx: 505, cy: 195, label: "30" }, { cx: 680, cy: 195, label: "70" },
  [
    { cx: 455, cy: 290, label: "30", red: true },
    { cx: 545, cy: 290, label: "0", red: false },
    { cx: 610, cy: 290, label: "0", red: false },
    { cx: 700, cy: 290, label: "70", red: true },
  ],
  ["TP", "FN", "TN", "FP"]);

// ================= PRECISION / RECALL BOXES (right column) =================
function defBox(y0, y1, header, eqKey, fill, line) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(775), y: px(y0), w: px(165), h: px(y1 - y0),
    fill: { color: fill }, line: { color: line, width: 1.5 }, adjustValue: 0.12,
  });
  s.addText(header + " =", {
    x: px(781), y: px(y0), w: px(78), h: px(y1 - y0),
    align: "left", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
  const m = EQ[eqKey];
  const cxBox = px(775) + px(165) - px(48);
  const cyTarget = px((y0 + y1) / 2);
  s.addImage({
    path: ASSETS + "/eq_016_" + eqKey + ".png",
    x: cxBox - m.w_in / 2,
    y: cyTarget - m.h_in / 2,
    w: m.w_in, h: m.h_in,
  });
}
defBox(110, 175, "Precision", "prec", PREC_FILL, PREC_LINE);
defBox(185, 250, "Recall", "rec", REC_FILL, REC_LINE);

// ================= F1 EQUATION BOX (green) =================
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: px(75), y: px(382), w: px(435 - 75), h: px(472 - 382),
  fill: { color: GREEN_FILL }, line: { color: GREEN_LINE, width: 1.25 }, adjustValue: 0.08,
});
{
  const m = EQ.f1;
  const cxBox = px(75) + px(360) / 2;
  const cyBox = px(382) + px(90) / 2;
  s.addImage({
    path: ASSETS + "/eq_016_f1.png",
    x: cxBox - m.w_in / 2,
    y: cyBox - m.h_in / 2,
    w: m.w_in, h: m.h_in,
  });
}

// ================= ORANGE EXPLANATION BOX =================
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: px(450), y: px(382), w: px(925 - 450), h: px(472 - 382),
  fill: { color: ORANGE_FILL }, line: { color: ORANGE_LINE, width: 1.5 }, adjustValue: 0.08,
});
s.addText("Penalize Small Value (X) by Using 1/X", {
  x: px(462), y: px(396), w: px(450), h: px(18),
  align: "left", valign: "middle",
  fontSize: 14, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Normalize (by * 0.5) to get ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "F1 Score between 0,1", options: { color: BLACK, bold: true, underline: true, fontSize: 14, fontFace: FONT } },
], {
  x: px(462), y: px(426), w: px(450), h: px(18),
  align: "left", valign: "middle", margin: 0,
});

// ================= BOTTOM CALC BOXES (2 cols x 3 rows) =================
const calcL = [
  "Precision= 20/(20+11) =64.5%",
  "Recall= 20/(20+10) =66.6%",
  "F1 Score= 68.7%+60% =65.55%",
];
const calcR = [
  "Precision= 30/(30+70) =30.3%",
  "Recall= 30/(30+0) =100%",
  "F1 Score= 30.3%+100% =46%",
];
const rowFills = [ROW1_FILL, ROW2_FILL, ROW3_FILL];
const rows = [[470, 486], [490, 506], [510, 526]];
function calcBox(x0, x1, y0, y1, line, f1, fill) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: fill }, line: { color: GRAY_LINE, width: 1 },
  });
  const parts = line.split("=");
  const labelCol = f1 ? "FF0000" : BLACK;
  s.addText([
    { text: parts[0] + "=", options: { color: labelCol, bold: true, fontSize: 12, fontFace: FONT } },
    { text: parts[1] + "=", options: { color: BLACK, fontSize: 12, fontFace: FONT } },
    { text: parts[2], options: { color: "0000FF", bold: true, fontSize: 12, fontFace: FONT } },
  ], {
    x: px(x0 + 9), y: px(y0), w: px(x1 - x0 - 18), h: px(y1 - y0),
    align: "left", valign: "middle", margin: 0,
  });
}
for (let i = 0; i < 3; i++) {
  calcBox(75, 465, rows[i][0], rows[i][1], calcL[i], i === 2, rowFills[i]);
  calcBox(470, 860, rows[i][0], rows[i][1], calcR[i], i === 2, rowFills[i]);
}

pptx.writeFile({ fileName: "slide_016_recreated.pptx" }).then(() => console.log("done"));
