const pptxgen = require("pptxgenjs");

// Slide 018 — Precision and Recall of Multi-class classification
// v2 rebuild (2026-10-30 re-judge wave). Geometry PIL-measured from
// unique_slides/slide_018.jpg (960x540, 1px = 1pt = 1/72in).
// Frame-vs-spec deviations vs the old consumed spec: caption line1 is RED
// ("Predicted as") and line2 black ("(Positive Class)"); table grid rules are
// dark red; Dog-row data cells carry a tan fill (#F0D8B0) and a translucent
// yellow strip runs down the Dog column (x202-221, y203-292); bottom bands are
// pink header #F9EDF7 / pale-yellow precision #FCFED2 / tan recall #F9E4CD with
// a thin pink box border; formulas are dark red (#8B0000) inline text.

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

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

const PANEL_FILL = "EEFFF4";   // 238,255,244 measured panel/cell fill
const PANEL_LINE = "469546";   // measured green border
const ROW_TAN = "F0D8B0";      // 240,216,172 measured Dog-row cell fill
const HDR_BAND = "F9EDF7";     // measured header band
const PREC_BAND = "FCFED2";    // measured precision band
const REC_BAND = "F9E4CD";     // measured recall band
const BOX_LINE = "DCC8D0";     // measured pink box border

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
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: RED, fontFace: NARROW, margin: 0,
});

// ---------------- CONFUSION MATRIX PANEL (green border, pale green) ----
// measured border x89-435, y114-310
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.2361, y: 1.5694, w: 4.8056, h: 2.7361,
  fill: { color: PANEL_FILL }, line: { color: PANEL_LINE, width: 3 },
});

// two-line caption, centered at x287px: line1 black, line2 red; pitch 18px
s.addText([
  { text: "Predicted as", options: { breakLine: true, fontSize: 17, color: BLACK } },
  { text: "(Positive Class)", options: { fontSize: 17, color: RED } },
], {
  x: 2.7361, y: 1.6806, w: 2.5, h: 0.55,
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", lineSpacing: 18,
});

// rotated row label "Actual" (visual ink x96-108, y217-264)
s.addText("Actual", {
  x: 1.0832, y: 3.2203, w: 0.667, h: 0.24,
  rotate: 270, align: "center", valign: "middle", margin: 0,
  fontSize: 19, bold: true, color: BLACK, fontFace: NARROW,
});

// blue caption right of the table (ink x449-603, y212-226)
s.addText("Confusion Matrix", {
  x: 6.2083, y: 2.9028, w: 2.36, h: 0.3056,
  align: "left", valign: "middle", margin: 0,
  fontSize: 21, color: BLUE, fontFace: "Arial",
});

// ---------------- TABLE GRID (dark-red rules; x114-420, y157-299) --------
function tc(t, fill) {
  return {
    text: t, options: {
      fontSize: 19, fontFace: NARROW, color: BLACK,
      align: "center", valign: "middle",
      fill: { color: fill || PANEL_FILL }, margin: 0,
    },
  };
}
let tableData = [
  [tc(""), tc("Dog"), tc("Cat"), tc("Fish"), tc("Total")],
  [tc("Dog"), tc("5", ROW_TAN), tc("2", ROW_TAN), tc("1", ROW_TAN), tc("8")],
  [tc("Cat"), tc("4"), tc("6"), tc("1"), tc("11")],
  [tc("Fish"), tc("7"), tc("0"), tc("0"), tc("7")],
];
s.addTable(tableData, {
  x: 1.5833, y: 2.1806,
  colW: [0.8889, 0.9167, 0.875, 0.7917, 0.7778],
  rowH: [0.5, 0.5, 0.4722, 0.5],
  fontSize: 19, fontFace: NARROW, color: BLACK,
  border: [{ type: "solid", color: GRID, width: 2 }],
});
// LO drops some table rules in render — draw all 11 grid rules explicitly
// measured rules: x=114,178,244,307,364,420 (y157-299); y=157,193,229,263,299 (x114-420)
[114, 178, 244, 307, 364, 420].forEach((gx) => {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: gx / 72 - 1 / 72, y: 157 / 72, w: 2 / 72, h: 142 / 72,
    fill: { color: GRID }, line: { type: "none" },
  });
});
[157, 193, 229, 263, 299].forEach((gy) => {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 114 / 72, y: gy / 72 - 1 / 72, w: 306 / 72, h: 2 / 72,
    fill: { color: GRID }, line: { type: "none" },
  });
});

// ---------------- YELLOW STRIP down the Dog column (x202-221, y203-292) --
s.addShape(pptx.shapes.RECTANGLE, {
  x: 2.8056, y: 2.8194, w: 0.2639, h: 1.2361,
  fill: { color: "FFFF00", transparency: 73 }, line: { type: "none" },
});

// ---------------- BOTTOM COLUMNS (DOG / CAT / FISH) ---------------------
// measured boxes x81-325, 361-606, 630-874; bands y321-374 header,
// y387-429 precision, y442-472 recall; thin pink border around each box.
const BOX_X = [1.125, 5.0139, 8.75];
const BOX_W = [3.3889, 3.4028, 3.3889];
const BOX_Y = 4.4306, BOX_H = 2.125;
// dark-red 17pt mathtext PNGs (600dpi, placed by measured ink bbox; pad 8px)
const EQ = {
  p1: { f: "eq_018_p1_dr.png", w: 3.23,    h: 0.23833 },
  r1: { f: "eq_018_r1_dr.png", w: 2.72833, h: 0.23833 },
  p2: { f: "eq_018_p2_dr.png", w: 3.07833, h: 0.23833 },
  r2: { f: "eq_018_r2_dr.png", w: 2.87333, h: 0.23833 },
  p3: { f: "eq_018_p3_dr.png", w: 2.84833, h: 0.23833 },
  r3: { f: "eq_018_r3_dr.png", w: 2.5,     h: 0.23833 },
};
const PAD = 8 / 600;
const INK_LEFT = [87 / 72, 367 / 72, 636 / 72];  // measured formula ink lefts
const PREC_TOP = 396 / 72, REC_TOP = 450 / 72;    // measured ink tops
const cols = [
  { cls: "DOG",  p: "p1", r: "r1" },
  { cls: "CAT",  p: "p2", r: "r2" },
  { cls: "FISH", p: "p3", r: "r3" },
];

cols.forEach((c, i) => {
  const x = BOX_X[i], w = BOX_W[i];
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: 4.4583, w: w, h: 0.7361, fill: { color: HDR_BAND }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: 5.375, w: w, h: 0.5833, fill: { color: PREC_BAND }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: 6.1389, w: w, h: 0.4167, fill: { color: REC_BAND }, line: { type: "none" },
  });
  s.addText([
    { text: "Precision and Recall", options: { breakLine: true, bold: false } },
    { text: "of " + c.cls + " Class", options: { bold: true } },
  ], {
    x: x, y: 330 / 72, w: w, h: 0.7361,
    align: "center", valign: "top", margin: 0,
    fontSize: 24, color: MAROON, fontFace: NARROW, lineSpacing: 20,
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: BOX_Y, w: w, h: BOX_H,
    fill: { type: "none" }, line: { color: BOX_LINE, width: 1 },
  });
  const pe = EQ[c.p], re = EQ[c.r];
  s.addImage({ path: A + pe.f, x: INK_LEFT[i] - PAD, y: PREC_TOP - PAD, w: pe.w, h: pe.h });
  s.addImage({ path: A + re.f, x: INK_LEFT[i] - PAD, y: REC_TOP - PAD, w: re.w, h: re.h });
});

pptx.writeFile({ fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_018_recreated.pptx" })
  .then((f) => console.log("wrote " + f));
