const pptxgen = require("pptxgenjs");

// Slide 018 — Precision and Recall of Multi-class classification
// v7 rebuild (2026-10-31 re-judge wave). Geometry PIL-measured from
// unique_slides/slide_018.jpg (960x540, 1px = 1pt = 1/72in).
// v7 change vs v6: the confusion matrix is drawn entirely from explicit
// shapes (cell fill rects + 2px red rule rects) — no addTable, so no
// double-drawn/stray grid rules under LibreOffice.
// Measured frame facts: green panel border x89-435 y114-310, fill #EEFFF4;
// red grid verticals x=115,178,244,308,365,420, horizontals y=158,194,230,266,302
// (2px, #8B0000); Dog-row data cells (5,2,1) tan #EAD8AC; translucent yellow
// strip x202-221 y203-292 in the predicted-Dog column; caption line1
// "Predicted as" dark y121-133, line2 "(Positive Class)" dark red y139-150;
// blue "Confusion Matrix" ink x451-602 y213-225; "Actual" vertical bold ink
// x97-107 y218-263; bottom boxes x81-325 / 361-606 / 630-874, y319-472 with
// pink header band y321-374 (#F9EFFA, two maroon lines y328-341/359-366),
// pale-yellow precision band y387-429 (#FCFFD2), tan recall band y442-472
// (#F9E5CD), thin pink box border #DCC8D0; six formulas are dark-red 600dpi
// mathtext PNGs placed by measured ink bbox.

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const GRID = "8B0000";
const BADGE_Y = "FFF9C4";
const DARK = "333333";
const BLACK = "000000";
const BLUE = "0000FF";
const MAROON = "8B0000";
const NARROW = "Arial Narrow";
const A = "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/";

const PANEL_FILL = "EEFFF4";
const PANEL_LINE = "469546";
const ROW_TAN = "EAD8AC";
const HDR_BAND = "F9EFFA";
const PREC_BAND = "FCFFD2";
const REC_BAND = "F9E5CD";
const BOX_LINE = "DCC8D0";

const P = (px) => px / 72; // px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// ---------------- HOUSE CHROME (overrides spec + judge) ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_Y }, line: { color: BADGE_Y, width: 0.5 },
});
s.addText("18", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: "Arial", margin: 0,
});
s.addText("Precision and Recall of Multi-class classification", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: RED, fontFace: "Arial", margin: 0,
});

// ---------------- CONFUSION MATRIX PANEL (green border, pale green) ----
// measured border x89-435, y114-310
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(89), y: P(114), w: P(346), h: P(196),
  fill: { color: PANEL_FILL }, line: { color: PANEL_LINE, width: 3 },
});

// two-line caption centered near x287: line1 dark, line2 dark red
s.addText([
  { text: "Predicted as", options: { breakLine: true, fontSize: 17, color: BLACK } },
  { text: "(Positive Class)", options: { fontSize: 17, color: MAROON } },
], {
  x: P(200), y: P(119), w: P(174), h: P(38),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", lineSpacing: 18,
});

// rotated row label "Actual" (visual ink x97-107, y218-263)
s.addText("Actual", {
  x: P(78), y: P(232), w: P(48), h: P(17),
  rotate: 270, align: "center", valign: "middle", margin: 0,
  fontSize: 19, bold: true, color: BLACK, fontFace: NARROW,
});

// blue caption right of the table (ink x451-602, y213-225)
s.addText("Confusion Matrix", {
  x: P(449), y: P(209), w: P(158), h: P(22),
  align: "left", valign: "middle", margin: 0,
  fontSize: 21, color: BLUE, fontFace: "Arial",
});

// ---------------- TABLE GRID (all explicit shapes) ---------------------
// verticals x=115,178,244,308,365,420 ; horizontals y=158,194,230,266,302
const VX = [115, 178, 244, 308, 365, 420];
const HY = [158, 194, 230, 266, 302];
const GX0 = VX[0], GX1 = VX[VX.length - 1];
const GY0 = HY[0], GY1 = HY[HY.length - 1];

// cell fills: pale green everywhere; Dog-row data cells (cols 1..3) tan
const TAN_COLS = [1, 2, 3];
const DOG_ROW = 1;
for (let r = 0; r < HY.length - 1; r++) {
  for (let c = 0; c < VX.length - 1; c++) {
    const fill = (r === DOG_ROW && TAN_COLS.includes(c)) ? ROW_TAN : PANEL_FILL;
    s.addShape(pptx.shapes.RECTANGLE, {
      x: P(VX[c]), y: P(HY[r]), w: P(VX[c + 1] - VX[c]), h: P(HY[r + 1] - HY[r]),
      fill: { color: fill }, line: { type: "none" },
    });
  }
}

// translucent yellow strip down the predicted-Dog column (x202-221, y203-292)
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(202), y: P(203), w: P(19), h: P(89),
  fill: { color: "FFFF00", transparency: 70 }, line: { type: "none" },
});

// 2px dark-red rules
VX.forEach((vx) => {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(vx - 1), y: P(GY0), w: P(2), h: P(GY1 - GY0),
    fill: { color: GRID }, line: { type: "none" },
  });
});
HY.forEach((hy) => {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(GX0), y: P(hy - 1), w: P(GX1 - GX0), h: P(2),
    fill: { color: GRID }, line: { type: "none" },
  });
});

// cell text
const CELLS = [
  ["", "Dog", "Cat", "Fish", "Total"],
  ["Dog", "5", "2", "1", "8"],
  ["Cat", "4", "6", "1", "11"],
  ["Fish", "7", "0", "0", "7"],
];
for (let r = 0; r < CELLS.length; r++) {
  for (let c = 0; c < CELLS[r].length; c++) {
    const t = CELLS[r][c];
    if (t === "") continue;
    s.addText(t, {
      x: P(VX[c]), y: P(HY[r]), w: P(VX[c + 1] - VX[c]), h: P(HY[r + 1] - HY[r]),
      align: "center", valign: "middle", margin: 0,
      fontSize: 19, color: BLACK, fontFace: NARROW,
    });
  }
}

// ---------------- BOTTOM COLUMNS (DOG / CAT / FISH) ---------------------
// measured boxes x81-325, 361-606, 630-874; y319-472; bands header y321-374,
// precision y387-429, recall y442-472; thin pink border around each box.
const BOX_X = [81, 361, 630].map(P);
const BOX_W = [244, 245, 244].map(P);
const BOX_Y = P(319), BOX_H = P(153);
const EQ = {
  p1: { f: "eq_018_p1_dr.png", w: 1938 / 600, h: 143 / 600 },
  r1: { f: "eq_018_r1_dr.png", w: 1637 / 600, h: 143 / 600 },
  p2: { f: "eq_018_p2_dr.png", w: 1847 / 600, h: 143 / 600 },
  r2: { f: "eq_018_r2_dr.png", w: 1724 / 600, h: 143 / 600 },
  p3: { f: "eq_018_p3_dr.png", w: 1709 / 600, h: 143 / 600 },
  r3: { f: "eq_018_r3_dr.png", w: 1500 / 600, h: 143 / 600 },
};
const PAD = 8 / 600;
const INK_LEFT = [87, 367, 636].map(P);   // measured formula ink lefts
const PREC_TOP = P(396), REC_TOP = P(450); // measured ink tops
const cols = [
  { cls: "DOG", p: "p1", r: "r1" },
  { cls: "CAT", p: "p2", r: "r2" },
  { cls: "FISH", p: "p3", r: "r3" },
];

cols.forEach((c, i) => {
  const x = BOX_X[i], w = BOX_W[i];
  // bands
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: P(321), w: w, h: P(53), fill: { color: HDR_BAND }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: P(387), w: w, h: P(42), fill: { color: PREC_BAND }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: P(442), w: w, h: P(30), fill: { color: REC_BAND }, line: { type: "none" },
  });
  // two-line maroon header (ink lines y328-341 and y359-366, pitch 31px)
  s.addText([
    { text: "Precision and Recall", options: { breakLine: true, bold: true } },
    { text: "of " + c.cls + " Class", options: { bold: true } },
  ], {
    x: x, y: P(326), w: w, h: P(44),
    align: "center", valign: "top", margin: 0,
    fontSize: 20, color: MAROON, fontFace: NARROW, lineSpacing: 31,
  });
  // box border
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: BOX_Y, w: w, h: BOX_H,
    fill: { type: "none" }, line: { color: BOX_LINE, width: 1 },
  });
  // formulas (600dpi PNGs at exact size, placed by measured ink bbox)
  const pe = EQ[c.p], re = EQ[c.r];
  s.addImage({ path: A + pe.f, x: INK_LEFT[i] - PAD, y: PREC_TOP - PAD, w: pe.w, h: pe.h });
  s.addImage({ path: A + re.f, x: INK_LEFT[i] - PAD, y: REC_TOP - PAD, w: re.w, h: re.h });
});

pptx.writeFile({ fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_018_recreated.pptx" })
  .then((f) => console.log("wrote " + f));
