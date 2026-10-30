// Build: slide 043 — "Perceptron Iteration 2" (S6 fresh carrier, 042-cert engine)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GROUND TRUTH: unique_slides/slide_043.jpg (960x540, 1px = 1pt).
// Band engine + LM/TL mechanisms ported from CERTIFIED build/slide_042.js
// (attempt 25) — same teacher template. Content per the crop-4 founder deltas:
//   - every band's LHS weight vector carries its leading component
//     (4;-10;-8) (6;-8;-6) (8;-4;-4) (10;-2;0) (8;-12;-8) (8;-12;-8)
//   - band 2 prints -14 as the frame shows (frame value wins over arithmetic)
//   - Initial W: THREE digit rows 4/-2/-2 (frame y63..69/78..86/94..101),
//     bowed paren tips 330.5/353.5 (three-frame identity with 042/044;
//     the old x430.5 stroke was 100px off); "=" ends ~4px clear of the
//     paren tip as in the frame
//   - LM header "Ugmented Vectors ( from Top )" char-exact; LM columns get
//     tall bowed paren pairs (crop-4 midleft BLOCKER)
//   - blue arrows DELETED (S20d-PIL: those zones hold the dx |digits| ink)
// Geometry: S20d stack/topband descs + PIL re-measurement (scratch/tmp/
// s6_043_measure.py): blue box 68..719 y55..129, Z cols 604/626/649,
// Step eta red ink x367..434 y68..78, calc boxes b1..b6 + sliver per S20d,
// box borders BEBEBE (row-scan min ~(187,187,187)), inter-box gaps panel grey
// (231,232,233) so NO calc-area white fill; no right-edge red bar exists.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_043_recreated.pptx");
const ASSETS = path.resolve(__dirname, "assets");

const px = (v) => v / 72; // frame px -> inches

const RED = "C00000";
const BLUE = "0000FF";
const BLACK = "000000";
const GREEN = "008000";
const GREENV = "00A050";
const WHITE = "FFFFFF";
const CREAM = "FFF8E0";     // measured top-band tint
const NAVY = "201070";      // measured top-band outline
const GRAYBLUE = "C0C3CA";  // measured LM card outline
const FONT = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

function txt(text, x, y, w, h, opts = {}) {
  slide.addText(text, Object.assign({
    x: px(x), y: px(y), w: px(w), h: px(h),
    fontFace: FONT, margin: 0, isTextBox: true,
  }, opts));
}

function txtsub(base, sub, x, y, w, h, opts = {}) {
  const subSize = Math.round(((opts.fontSize || 10) * 0.7) * 10) / 10;
  slide.addText([
    { text: base },
    { text: sub, options: { subscript: true, fontSize: subSize } },
  ], Object.assign({
    x: px(x), y: px(y), w: px(w), h: px(h),
    fontFace: FONT, margin: 0, isTextBox: true,
  }, opts));
}

function eqImage(tag, x, centerPx) {
  const m = JSON.parse(fs.readFileSync(path.join(ASSETS, tag + ".json"), "utf8"));
  slide.addImage({
    path: path.join(ASSETS, m.image),
    x: px(x), y: px(centerPx - m.h_in * 36), w: m.w_in, h: m.h_in,
  });
}

// bowed paren pair (041/042-cert pattern): side-aware ink placement, tips xl/xr
function parenPair(xl, xr, inkTopPx, inkH, stem) {
  const P = path.join(ASSETS, "parens042");
  const sc = inkH / 39.96;
  [[`${P}/${stem}lp.png`, `${P}/${stem}lp.json`, xl, "lp"],
   [`${P}/${stem}rp.png`, `${P}/${stem}rp.json`, xr, "rp"]]
    .forEach(([img, meta, tipX, side]) => {
      const j = JSON.parse(fs.readFileSync(meta, "utf8"));
      const ink = side === "lp" ? j.ink_right_px : j.ink_left_px;
      slide.addImage({
        path: img,
        x: px(tipX - ink * j.pt_per_px * sc),
        y: px(inkTopPx - j.ink_top_px * j.pt_per_px * sc),
        w: (j.px_w * j.pt_per_px * sc) / 72,
        h: (j.px_h * j.pt_per_px * sc) / 72,
      });
    });
}

// tall 3-row column vector: bowed parens + centred digits
function tallVec(xl, xr, y0, y1, rows, vals, color) {
  const P = path.join(ASSETS, "parens042");
  const stem = color === GREENV ? "paren_tall_green_" : "paren_tall_";
  const sc = (y1 - y0) / 39.96;
  [[`${P}/${stem}lp.png`, `${P}/${stem}lp.json`, xl, "lp"],
   [`${P}/${stem}rp.png`, `${P}/${stem}rp.json`, xr, "rp"]]
    .forEach(([img, meta, tipX, side]) => {
      const j = JSON.parse(fs.readFileSync(meta, "utf8"));
      const ink = side === "lp" ? j.ink_right_px : j.ink_left_px;
      slide.addImage({
        path: img,
        x: px(tipX - ink * j.pt_per_px * sc),
        y: px(y0 - j.ink_top_px * j.pt_per_px * sc),
        w: (j.px_w * j.pt_per_px * sc) / 72,
        h: (j.px_h * j.pt_per_px * sc) / 72,
      });
    });
  vals.forEach((d, ri) => {
    txt(String(d), xl + 2, rows[ri] - 2, xr - xl - 4, 12, {
      fontSize: 10, color, align: "center", valign: "middle", wrap: false,
    });
  });
}

// ---- house chrome -----------------------------------------------------------
drawHouseChrome(pptx, slide, { numeral: 43 });

// ---- top band: cream fill + navy outline (043 frame-measured tones) ---------
slide.addShape(pptx.ShapeType.rect, {
  x: px(73), y: px(59), w: px(715 - 73), h: px(125 - 59),
  fill: { color: CREAM }, line: { type: "none" },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(719 - 68), h: px(130 - 54),
  fill: { type: "none" }, line: { color: NAVY, width: 1 },
});

// ---- top-left data table: txtsub headers, per-cell paren rows, class row ----
const tblCols = [96, 118, 140, 162, 184, 206];
tblCols.forEach((cx, i) => {
  txtsub("x", String(i + 1), cx - 8, 62, 16, 12, {
    fontSize: 10, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});
["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"].forEach((t, i) =>
  txt(t, tblCols[i] - 22, 80, 44, 14, { fontSize: 11, color: BLACK, align: "center", valign: "middle" }));
["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"].forEach((t, i) =>
  txt(t, tblCols[i] - 22, 96, 44, 14, { fontSize: 11, color: BLACK, align: "center", valign: "middle" }));
[["C1", 0], ["C1", 1], ["C1", 2], ["C2", 3], ["C2", 4], ["C2", 5]].forEach(([lab, i]) => {
  txtsub(lab[0], lab[1], tblCols[i] - 8, 111, 16, 15, {
    fontSize: 10, color: lab === "C1" ? RED : BLUE, bold: true,
    align: "center", valign: "middle",
  });
});

// ---- Initial W = (4;-2;-2): runs + bowed parens tips 330.5/353.5 ------------
slide.addText([
  { text: "Initial " },
  { text: "W", options: { italic: true, underline: true } },
  { text: "=" },
], { x: px(281), y: px(74), w: px(72), h: px(18), fontSize: 11, color: BLACK,
  valign: "middle", fontFace: FONT, margin: 0, wrap: false });
parenPair(330.5, 353.5, 62, 40, "paren_tall_");
txt("4", 334.5, 63, 14, 14, { fontSize: 11, color: BLACK, align: "center", valign: "middle" });
txt("-2", 337.5, 78, 18, 14, { fontSize: 11, color: BLACK, align: "center", valign: "middle" });
txt("-2", 337.5, 94, 18, 14, { fontSize: 11, color: BLACK, align: "center", valign: "middle" });

// Step η = 2 — red ink measured x367..434 y68..78 (15pt)
txt("Step \u03B7 = 2", 367, 64, 78, 19, {
  fontSize: 15, color: RED, bold: true, italic: true, valign: "middle",
});

// ---- top-right: Check classes of + Z1 txtsub + mx matrix images -------------
txt("Check classes of", 499, 80, 90, 14, { fontSize: 11, color: BLACK, valign: "middle" });
const mCols = [605, 628, 651];
mCols.forEach((cx, i) => {
  txtsub("Z", "1", cx - 4, 62, 16, 13, {
    fontSize: 10, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});
mCols.forEach((cx, i) => {
  eqImage("eq043_mx" + (i + 1), cx, 95);
});

// ---- legend: 041/042-cert per-fragment pattern, frame x's, no commas --------
txtsub("C", "1", 238, 108, 15, 17, { fontSize: 12, color: RED, valign: "middle", wrap: false });
txt("positive", 256, 108, 48, 16, { fontSize: 12, color: BLACK, valign: "middle", wrap: false });
txtsub("C", "2", 311, 108, 15, 17, { fontSize: 12, color: BLUE, valign: "middle", wrap: false });
txt("negative", 327, 108, 52, 16, { fontSize: 12, color: BLACK, valign: "middle", wrap: false });
txt("Zero", 394, 108, 30, 16, { fontSize: 12, color: GREEN, valign: "middle", wrap: false });
txt("is unaccepted", 429, 108, 84, 16, { fontSize: 12, color: BLACK, valign: "middle", wrap: false });

// ---- left-middle: white card + Ugmented header + digit rows + tall parens ---
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(140), w: px(246 - 70), h: px(255 - 140),
  fill: { color: WHITE }, line: { color: GRAYBLUE, width: 1 },
});
txt("Ugmented Vectors ( from Top )", 79, 146, 168, 13, {
  fontSize: 11, color: "3B3F8C", bold: true, valign: "middle",
});
tblCols.forEach((cx, i) => {
  txtsub("x", String(i + 1), cx - 8, 164, 16, 12, {
    fontSize: 10, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});
const LM_BANDS = [
  { y: 183, vals: [1, 1, 1, 1, 1, 1] },
  { y: 198, vals: [1, 2, 1, 5, 6, 6] },
  { y: 214, vals: [1, 1, 2, 4, 5, 6] },
];
LM_BANDS.forEach((band) => {
  tblCols.forEach((cx, ci) => {
    txt(String(band.vals[ci]), cx - 5, band.y, 11, 11, {
      fontSize: 10, color: BLACK, align: "center", valign: "middle",
    });
  });
});
[[90, 103], [112, 125], [134, 147], [156, 169], [178, 191], [200, 213]].forEach(([xl, xr]) => {
  parenPair(xl, xr, 179, 46, "paren_tall_");
});
[["C1", 0], ["C1", 1], ["C1", 2], ["C2", 3], ["C2", 4], ["C2", 5]].forEach(([lab, i]) => {
  txtsub(lab[0], lab[1], tblCols[i] - 9, 230, 18, 14, {
    fontSize: 10, color: lab === "C1" ? RED : BLUE, bold: true,
    align: "center", valign: "middle",
  });
});

// ---- red Iteration 2 badge ---------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(277), w: px(214 - 84), h: px(305 - 277),
  fill: { color: RED }, line: { type: "none" },
});
txt("Iteration 2", 84, 285, 214 - 84, 20, {
  fontSize: 15, color: WHITE, bold: true, align: "center", valign: "middle",
});

// ---- right computation stack: 6 boxes (frame 66px pitch; gray gap below box 6) --
const STACK_BOXES = [
  [145, 203], [209, 267], [273, 330], [336, 396], [404, 463], [469, 528],
];
STACK_BOXES.forEach(([y0, y1]) => {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(277), y: px(y0), w: px(854 - 277), h: px(y1 - y0 + 1),
    fill: { color: WHITE }, line: { color: "BEBEBE", width: 1 },
  });
});

// band content (founder deltas + S20d stack desc; ⇒ black on this frame)
const ROWS = [
  { sub: "1", mat: ["1", "1", "1"], matColor: RED, gVals: [4, -10, -8], dEq: "-14",
    action: "Update Weight", arrowX: 505, actX: 525, eqX: 414, wX: 632,
    updateEq: { op: "+ 2 *", opColor: RED, opX: 690, incVals: [1, 1, 1], incX: [717, 733],
      eqX: 737, resVals: [6, -8, -6], resX: [746, 772], resColor: GREENV, backX: 795 } },
  { sub: "2", mat: ["1", "2", "1"], matColor: RED, gVals: [6, -8, -6], dEq: "-14",
    action: "Update Weight", arrowX: 505, actX: 525, eqX: 414, wX: 632,
    updateEq: { op: "+ 2 *", opColor: RED, opX: 690, incVals: [1, 2, 1], incX: [717, 733],
      eqX: 737, resVals: [8, -4, -4], resX: [746, 772], resColor: GREENV, backX: 795 } },
  { sub: "3", mat: ["1", "1", "2"], matColor: RED, gVals: [8, -4, -4], dEq: "-4",
    action: "Update Weight", arrowX: 505, actX: 525, eqX: 414, wX: 632,
    updateEq: { op: "+ 2 *", opColor: RED, opX: 690, incVals: [1, 1, 2], incX: [717, 733],
      eqX: 737, resVals: [10, -2, 0], resX: [746, 772], resColor: GREENV, backX: 795 } },
  { sub: "4", mat: ["1", "5", "4"], matColor: BLUE, gVals: [10, -2, 0], dEq: "0",
    action: "Update Weight", arrowX: 493, actX: 509, eqX: 415, wX: 618,
    updateEq: { op: "- 2 *", opColor: BLUE, opX: 673, incVals: [1, 5, 4], incX: [702, 719],
      eqX: 723, resVals: [8, -12, -8], resX: [731, 757], resColor: GREENV, backX: 787 } },
  { sub: "5", mat: ["1", "6", "5"], matColor: BLUE, gVals: [8, -12, -8], dEq: "-104",
    action: "Keep same Weight", arrowX: 527, actX: 546, eqX: 416, wX: 724 },
  { sub: "6", mat: ["1", "6", "6"], matColor: BLUE, gVals: [8, -12, -8], dEq: "-112",
    action: "Keep same Weight", arrowX: 527, actX: 546, eqX: 416, wX: 724 },
];

const LBL_X = 283;
const BAR1_X = 327;
const BAR2_X = 379;
const MAT_CX = [337, 354.5, 372];
const DVEC_XS = [[381, 401], [383, 401], [383, 401], [379, 398], [378, 397], [378, 397]];
const BAND_A = [166, 231, 293, 357, 425, 490];
const VSPAN = [
  { y0: 154, y1: 201, rows: [155, 172, 189] },
  { y0: 218, y1: 265, rows: [219, 237, 254] },
  { y0: 279, y1: 326, rows: [280, 298, 316] },
  { y0: 343, y1: 392, rows: [344, 362, 379] },
  { y0: 409, y1: 457, rows: [410, 427, 444] },
  { y0: 474, y1: 522, rows: [475, 492, 509] },
];
const WVEC_XS = [[659, 685], [659, 685], [659, 685], [644, 670], [745, 773], [745, 773]];

ROWS.forEach((r, i) => {
  const a = BAND_A[i];
  const v = VSPAN[i];

  // d(x_i) = label
  slide.addText(
    [
      { text: "d(x", options: {} },
      { text: r.sub, options: { subscript: true, fontSize: 9 } },
      { text: ") =", options: {} },
    ],
    { x: px(LBL_X), y: px(a - 3), w: px(34), h: px(14), fontSize: 13,
      color: BLACK, valign: "middle", wrap: false, fontFace: FONT, margin: 0 }
  );

  // | 1 xi1 xi2 | bars hugging the digit band
  [BAR1_X, BAR2_X].forEach((x) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(a - 17), w: 0, h: px(15),
      line: { color: r.matColor, width: 1 },
    });
  });
  r.mat.forEach((d, ci) => {
    txt(d, MAT_CX[ci] - 7, a - 15, 14, 11, {
      fontSize: 10, color: r.matColor, align: "center", valign: "middle",
    });
  });

  // green W vector (tall) + = value
  tallVec(DVEC_XS[i][0], DVEC_XS[i][1], v.y0, v.y1, v.rows, r.gVals, GREENV);
  txt("= " + r.dEq, r.eqX, a - 3, 56, 14, { fontSize: 12, color: BLACK, valign: "middle" });

  // ⇒ action (black on this frame)
  txt("\u21D2", r.arrowX, a - 3, 16, 14, {
    fontSize: 12, color: BLACK, align: "center", valign: "middle",
  });
  txt(r.action, r.actX, a - 3, 140, 14, {
    fontSize: 13, color: BLACK, valign: "middle", wrap: false,
  });

  // W̲ = (black W vector, tall)
  slide.addText([
    { text: "W", options: { bold: true, underline: true } },
    { text: " =" },
  ], { x: px(r.wX), y: px(a - 3), w: px(30), h: px(14), fontSize: 11,
    color: BLACK, valign: "middle", wrap: false, fontFace: FONT, margin: 0 });
  tallVec(WVEC_XS[i][0], WVEC_XS[i][1], v.y0, v.y1, v.rows, r.gVals, BLACK);

  // update rows: ± 2 * (inc) = (result green), red ⇐ far right
  if (r.updateEq) {
    const u = r.updateEq;
    txt(u.op, u.opX, a - 3, 24, 14, { fontSize: 10, color: u.opColor, valign: "middle", wrap: false });
    tallVec(u.incX[0], u.incX[1], v.y0, v.y1, v.rows, u.incVals, BLACK);
    txt("=", u.eqX, a - 3, 12, 14, { fontSize: 11, color: BLACK, valign: "middle" });
    tallVec(u.resX[0], u.resX[1], v.y0, v.y1, v.rows, u.resVals, u.resColor);
    txt("\u21D0", u.backX, a - 3, 20, 15, {
      fontSize: 12, color: RED, align: "center", valign: "middle",
    });
  }
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
