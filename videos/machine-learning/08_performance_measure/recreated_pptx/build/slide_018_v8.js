const pptxgen = require("pptxgenjs");

// Slide 018 — Precision and Recall of Multi-class classification
// v8 rebuild (2026-10-31). v7 judge attempt 4 PASSed; corroboration FAILed with
// pixel-verifiable findings, all fixed here (PIL-measured from the original):
//  - open top-left grid corner: top rule y158 spans x178-420 only, left rule
//    x115 spans y194-302 only (corner cell has fill but no rules)
//  - matrix text is dark red (#8B0000) and bold, not black regular
//  - bottom boxes: white fill behind bands; header band is narrower and
//    offset vs formula bands (hdr x88-309/368-593/640-860, prec x79-327/
//    360-607/628-876, rec x81-322/363-606/631-873); band rows hdr y321-376,
//    prec y389-426, rec y444-471; border #E0C0CB
//  - class header line1 regular weight, only the class name bold on line2
// House chrome per root AGENTS.md (frame/badge/title override everything).

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
const BOX_LINE = "E0C0CB";

const P = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// ---------------- HOUSE CHROME ----------------
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

// ---------------- CONFUSION MATRIX PANEL ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(89), y: P(114), w: P(346), h: P(196),
  fill: { color: PANEL_FILL }, line: { color: PANEL_LINE, width: 3 },
});

// two-line caption: line1 dark, line2 dark red
s.addText([
  { text: "Predicted as", options: { breakLine: true, fontSize: 17, color: BLACK } },
  { text: "(Positive Class)", options: { fontSize: 17, color: MAROON } },
], {
  x: P(200), y: P(119), w: P(174), h: P(38),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", lineSpacing: 18,
});

// rotated "Actual" (ink x97-107, y218-263)
s.addText("Actual", {
  x: P(78), y: P(232), w: P(48), h: P(17),
  rotate: 270, align: "center", valign: "middle", margin: 0,
  fontSize: 19, bold: true, color: BLACK, fontFace: NARROW,
});

// blue caption (ink x451-602, y213-225)
s.addText("Confusion Matrix", {
  x: P(449), y: P(209), w: P(158), h: P(22),
  align: "left", valign: "middle", margin: 0,
  fontSize: 21, color: BLUE, fontFace: "Arial",
});

// ---------------- TABLE GRID (explicit shapes, OPEN top-left corner) -----
const VX = [115, 178, 244, 308, 365, 420];
const HY = [158, 194, 230, 266, 302];

// cell fills: pale green everywhere; Dog-row data cells (cols 1..3) tan
for (let r = 0; r < HY.length - 1; r++) {
  for (let c = 0; c < VX.length - 1; c++) {
    const fill = (r === 1 && c >= 1 && c <= 3) ? ROW_TAN : PANEL_FILL;
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

// rules: top border starts at x178 (open corner); left border starts at y194
VX.forEach((vx) => {
  const y0 = vx === 115 ? 194 : 158;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(vx - 1), y: P(y0), w: P(2), h: P(302 - y0),
    fill: { color: GRID }, line: { type: "none" },
  });
});
HY.forEach((hy) => {
  const x0 = hy === 158 ? 178 : 115;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(x0), y: P(hy - 1), w: P(420 - x0), h: P(2),
    fill: { color: GRID }, line: { type: "none" },
  });
});

// cell text: dark red, bold
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
      fontSize: 19, bold: true, color: GRID, fontFace: NARROW,
    });
  }
}

// ---------------- BOTTOM COLUMNS (DOG / CAT / FISH) ---------------------
// white box fill + pink border; header band narrower/offset vs formula bands
const BOX_X = [81, 361, 630].map(P);
const BOX_W = [244, 245, 244].map(P);
const BOX_Y = P(319), BOX_H = P(153);
const HDR_X = [88, 368, 640].map(P);
const HDR_W = [221, 225, 220].map(P);
const PREC_X = [79, 360, 628].map(P);
const PREC_W = [248, 247, 248].map(P);
const REC_X = [81, 363, 631].map(P);
const REC_W = [241, 243, 242].map(P);
const EQ = {
  p1: { f: "eq_018_p1_dr.png", w: 1938 / 600, h: 143 / 600 },
  r1: { f: "eq_018_r1_dr.png", w: 1637 / 600, h: 143 / 600 },
  p2: { f: "eq_018_p2_dr.png", w: 1847 / 600, h: 143 / 600 },
  r2: { f: "eq_018_r2_dr.png", w: 1724 / 600, h: 143 / 600 },
  p3: { f: "eq_018_p3_dr.png", w: 1709 / 600, h: 143 / 600 },
  r3: { f: "eq_018_r3_dr.png", w: 1500 / 600, h: 143 / 600 },
};
const PAD = 8 / 600;
const INK_LEFT = [87, 367, 636].map(P);
const PREC_TOP = P(396), REC_TOP = P(450);
const cols = [
  { cls: "DOG", p: "p1", r: "r1" },
  { cls: "CAT", p: "p2", r: "r2" },
  { cls: "FISH", p: "p3", r: "r3" },
];

cols.forEach((c, i) => {
  const x = BOX_X[i], w = BOX_W[i];
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x, y: BOX_Y, w: w, h: BOX_H,
    fill: { color: "FFFFFF" }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: HDR_X[i], y: P(321), w: HDR_W[i], h: P(55), fill: { color: HDR_BAND }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: PREC_X[i], y: P(389), w: PREC_W[i], h: P(37), fill: { color: PREC_BAND }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: REC_X[i], y: P(444), w: REC_W[i], h: P(27), fill: { color: REC_BAND }, line: { type: "none" },
  });
  // two-line header: line1 regular, only the class name bold
  s.addText([
    { text: "Precision and Recall", options: { breakLine: true, bold: false } },
    { text: "of ", options: { bold: false } },
    { text: c.cls, options: { bold: true } },
    { text: " Class", options: { bold: false } },
  ], {
    x: x, y: P(326), w: w, h: P(44),
    align: "center", valign: "top", margin: 0,
    fontSize: 20, color: MAROON, fontFace: NARROW, lineSpacing: 31,
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
