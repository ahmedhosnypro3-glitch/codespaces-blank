const pptxgen = require("pptxgenjs");
const fs = require("fs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

// ---- palette ----
const BG = "E8E8E8";
const HOUSE_RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const MAROON = "A50000";      // title / labels / equation ink (measured ~#A50000)
const NODE_RED = "B03030";    // filled circles on positive side
const NODE_GREEN = "008000";  // filled circles on negative side
const BLUE_FILL = "DCE9F7";   // precision/recall boxes (pale blue)
const BLUE_LINE = "2E75B6";
const GREEN_FILL = "CCFFCC";  // F1 box
const GREEN_LINE = "008000";
const ORANGE_FILL = "FFE0B2"; // explanation box
const ORANGE_LINE = "C55A11";
const GRAY_LINE = "BFBFBF";   // calc box borders
const WHITE = "FFFFFF";
const BLACK = "000000";
const BROWN = "8B4513";       // tree connectors
const GRAY = "808080";        // airplane strokes
const FONT = "Arial";

const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
const EQ = JSON.parse(fs.readFileSync(ASSETS + "/eq_016_manifest.json", "utf8"));

// original frame is 960x540 px, 1px = 1pt = 1/72 in
const px = (v) => v / 72;

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
  fontSize: 28, bold: true, color: MAROON, fontFace: FONT, margin: 0,
});

// ================= TREE DIAGRAMS =================
// measured circle centers (px): left top 30@(151,215) 70@(332,215);
// left bottom 20@(106,278) 10@(193,278) 59@(286,278) 11@(378,278)
// right top 30@(506,215) 70@(687,215);
// right bottom 30@(461,279) 0@(548,278) 0@(642,278) 70@(732,278)
const R = px(31) / 2; // circle radius ~15.5px

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

function connector(x1, y1, x2, y2) {
  const dx = px(x2) - px(x1), dy = px(y2) - px(y1);
  s.addShape(pptx.shapes.LINE, {
    x: px(x1), y: px(y1), w: Math.abs(dx), h: Math.abs(dy),
    line: { color: BROWN, width: 2 },
    flipH: dx < 0 ? true : false,
    flipV: dy < 0 ? true : false,
  });
}

// simple line-art airplane (side view, nose right), gray strokes, red nose
function drawPlane(cx, cy, w) {
  const h = w * 0.36;
  const X = px(cx) - px(w) / 2, Y = px(cy) - px(h) / 2;
  // fuselage
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: X, y: Y + px(h) * 0.28, w: px(w), h: px(h) * 0.44,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, adjustValue: 0.5,
  });
  // nose cone (red)
  s.addShape(pptx.shapes.OVAL, {
    x: X + px(w) - px(h) * 0.30, y: Y + px(h) * 0.28, w: px(h) * 0.30, h: px(h) * 0.44,
    fill: { color: MAROON }, line: { color: GRAY, width: 0.75 },
  });
  // main wing
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X + px(w) * 0.38, y: Y + px(h) * 0.55, w: px(w) * 0.22, h: px(h) * 0.55,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 180,
  });
  // tail wing
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X + px(w) * 0.02, y: Y + px(h) * 0.30, w: px(w) * 0.16, h: px(h) * 0.42,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 200,
  });
  // windows
  for (let i = 0; i < 3; i++) {
    s.addShape(pptx.shapes.OVAL, {
      x: X + px(w) * (0.22 + i * 0.13), y: Y + px(h) * 0.40, w: px(h) * 0.11, h: px(h) * 0.11,
      fill: { color: WHITE }, line: { color: GRAY, width: 0.75 },
    });
  }
}

function tree(x0, x1, topPos, topNeg, b1, b2, b3, b4, labels) {
  // enclosing red-bordered box
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(114), w: px(x1 - x0), h: px(324 - 114),
    fill: { color: BG }, line: { color: "8B2E2F", width: 1.5 },
  });
  // column labels
  s.addText("Positive", {
    x: px(topPos.cx) - px(45), y: px(96), w: px(90), h: px(20),
    align: "center", valign: "middle",
    fontSize: 15, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
  s.addText("Negative", {
    x: px(topNeg.cx) - px(45), y: px(96), w: px(90), h: px(20),
    align: "center", valign: "middle",
    fontSize: 15, bold: true, color: NODE_GREEN, fontFace: FONT, margin: 0,
  });
  // airplanes above top circles
  drawPlane(topPos.cx, 158, 70);
  drawPlane(topNeg.cx, 158, 70);
  connector(topPos.cx, 176, topPos.cx, topPos.cy - 16);
  connector(topNeg.cx, 176, topNeg.cy - 16);
  // top circles
  node(topPos.cx, topPos.cy, topPos.label, NODE_RED);
  node(topNeg.cx, topNeg.cy, topNeg.label, NODE_GREEN);
  // connectors to children + child circles
  const kids = [b1, b2, b3, b4];
  const from = [topPos, topPos, topNeg, topNeg];
  for (let i = 0; i < 4; i++) {
    connector(from[i].cx, from[i].cy + 16, kids[i].cx, kids[i].cy - 16);
    node(kids[i].cx, kids[i].cy, kids[i].label, kids[i].red ? NODE_RED : NODE_GREEN);
  }
  // TP/FN/TN/FP labels under children
  const labCols = [NODE_RED, NODE_GREEN, NODE_GREEN, NODE_RED];
  for (let i = 0; i < 4; i++) {
    s.addText(labels[i], {
      x: px(kids[i].cx) - px(20), y: px(329), w: px(40), h: px(17),
      align: "center", valign: "middle",
      fontSize: 12, bold: true, color: labCols[i], fontFace: FONT, margin: 0,
    });
  }
}

tree(68, 413,
  { cx: 151, cy: 215, label: "30" }, { cx: 332, cy: 215, label: "70" },
  { cx: 106, cy: 278, label: "20", red: true },
  { cx: 193, cy: 278, label: "10", red: false },
  { cx: 286, cy: 278, label: "59", red: false },
  { cx: 378, cy: 278, label: "11", red: true },
  ["TP", "FN", "TN", "FP"]);

tree(423, 768,
  { cx: 506, cy: 215, label: "30" }, { cx: 687, cy: 215, label: "70" },
  { cx: 461, cy: 279, label: "30", red: true },
  { cx: 548, cy: 278, label: "0", red: false },
  { cx: 642, cy: 278, label: "0", red: false },
  { cx: 732, cy: 278, label: "70", red: true },
  ["TP", "FN", "TN", "FP"]);

// ================= PRECISION / RECALL BOXES (right column) =================
function defBox(y0, y1, header, eqKey) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(749), y: px(y0), w: px(150), h: px(y1 - y0),
    fill: { color: BLUE_FILL }, line: { color: BLUE_LINE, width: 1.5 },
  });
  s.addText(header, {
    x: px(756), y: px(y0 + 4), w: px(136), h: px(18),
    align: "center", valign: "middle",
    fontSize: 13, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
  const m = EQ[eqKey];
  const wIn = m.w_in, hIn = m.h_in;
  // center the fraction ink in the lower part of the box
  const inkW = m.ink_w_frac * wIn, inkH = m.ink_h_frac * hIn;
  const cxBox = px(749) + px(150) / 2;
  const cyInk = px(y0 + 38) + px(y1 - y0 - 42) / 2; // ink center target
  s.addImage({
    path: ASSETS + "/eq_016_" + eqKey + ".png",
    x: cxBox - inkW / 2 - m.ink_left_frac * wIn + m.ink_left_frac * wIn - (wIn - inkW) / 2 + 0, // simplify below
    y: cyInk - inkH / 2 - m.ink_top_frac * hIn,
    w: wIn, h: hIn,
  });
}
// (placement simplified: center image box on target center)
function defBox2(y0, y1, header, eqKey) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(749), y: px(y0), w: px(150), h: px(y1 - y0),
    fill: { color: BLUE_FILL }, line: { color: BLUE_LINE, width: 1.5 },
  });
  s.addText(header, {
    x: px(756), y: px(y0 + 3), w: px(136), h: px(17),
    align: "center", valign: "middle",
    fontSize: 13, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
  const m = EQ[eqKey];
  const cxBox = px(749) + px(150) / 2;
  const cyTarget = px((y0 + y1) / 2) + px(10);
  s.addImage({
    path: ASSETS + "/eq_016_" + eqKey + ".png",
    x: cxBox - m.w_in / 2,
    y: cyTarget - m.h_in / 2,
    w: m.w_in, h: m.h_in,
  });
}
defBox2(111, 182, "Precision", "prec");
defBox2(183, 230, "Recall", "rec");

// ================= F1 EQUATION BOX (green) =================
s.addShape(pptx.shapes.RECTANGLE, {
  x: px(93), y: px(329), w: px(498 - 93), h: px(388 - 329),
  fill: { color: GREEN_FILL }, line: { color: GREEN_LINE, width: 1.5 },
});
{
  const m = EQ.f1;
  const cxBox = px(93) + px(405) / 2;
  const cyBox = px(329) + px(59) / 2;
  s.addImage({
    path: ASSETS + "/eq_016_f1.png",
    x: cxBox - m.w_in / 2,
    y: cyBox - m.h_in / 2,
    w: m.w_in, h: m.h_in,
  });
}

// ================= ORANGE EXPLANATION BOX =================
s.addShape(pptx.shapes.RECTANGLE, {
  x: px(514), y: px(330), w: px(880 - 514), h: px(387 - 330),
  fill: { color: ORANGE_FILL }, line: { color: ORANGE_LINE, width: 1.5 },
});
s.addText("Penalize Small Value (X) by Using 1/X", {
  x: px(525), y: px(343), w: px(340), h: px(16),
  align: "left", valign: "middle",
  fontSize: 14, color: MAROON, fontFace: FONT, margin: 0,
});
s.addText("Normalize (by * 0.5) to get F1 Score between 0,1", {
  x: px(525), y: px(361), w: px(345), h: px(16),
  align: "left", valign: "middle",
  fontSize: 14, color: MAROON, fontFace: FONT, margin: 0,
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
const rows = [[399, 426], [438, 465], [481, 509]];
function calcBox(x0, x1, y0, y1, line, f1) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: WHITE }, line: { color: GRAY_LINE, width: 1 },
  });
  if (f1) {
    // 'F1 Score' red, rest dark, final result blue (as in the original)
    const parts = line.split("=");
    s.addText([
      { text: parts[0] + "=", options: { color: "FF0000", bold: true } },
      { text: parts[1] + "=", options: { color: BLACK } },
      { text: parts[2], options: { color: "0000FF", bold: true } },
    ], {
      x: px(x0 + 9), y: px(y0), w: px(x1 - x0 - 18), h: px(y1 - y0),
      align: "left", valign: "middle",
      fontSize: 12, fontFace: FONT, margin: 0,
    });
  } else {
    s.addText(line, {
      x: px(x0 + 9), y: px(y0), w: px(x1 - x0 - 18), h: px(y1 - y0),
      align: "left", valign: "middle",
      fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
    });
  }
}
for (let i = 0; i < 3; i++) {
  calcBox(83, 371, rows[i][0], rows[i][1], calcL[i], i === 2);
  calcBox(439, 727, rows[i][0], rows[i][1], calcR[i], i === 2);
}

pptx.writeFile({
  fileName: "slide_016_recreated.pptx",
}).then(() => console.log("done"));
