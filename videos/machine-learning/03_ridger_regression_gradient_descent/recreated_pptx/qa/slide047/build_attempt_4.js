const pptxgenpkg = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";  // 13.333 x 7.5 in
const W = 13.333, H = 7.5;

let s = pptx.addSlide();

// ---- HOUSE CHROME (frozen: canvas FFFFFF, panel E9E9E7 x54..903 y45..540,
//      C00000 1pt LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY — NO top stroke) ----
drawHouseChrome(pptx, s, { numeral: "47" });

// ---- CONSTANTS ----
const FONT = "Arial";
const BLACK = "000000";
const RED   = "FF0000";
const BLUE  = "0000FF";
const GREEN = "008000";

// ---- frame px -> pptx inches. Origin = PANEL corner (x=54, y=45),
//      so feed PANEL-RELATIVE frame px (= absolute - 54 / - 45). ----
function fx(px) { return 54 / 72 + px / 72; }
function fy(px) { return 45 / 72 + px / 72; }
function fw(px) { return px / 72; }
function fh(px) { return px / 72; }
// ABSOLUTE frame px -> pptx inches (panel origin already subtracted): 1 frame px = 1pt.
function ax(px) { return px / 72; }
function ay(py) { return py / 72; }

const ASSET = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/";
function placeEq(img, baselineYIn, xIn) {
  const yTop = baselineYIn - img.baseline_frac * img.h_in;
  s.addImage({ path: ASSET + img.file, x: xIn, y: yTop, w: img.w_in, h: img.h_in });
}

// ============================================================
// SPANNING-PAREN COLUMN VECTORS (measured on the 960x540 original)
// Every column of the three matrices is enclosed in ONE paren pair spanning all
// its component lines; the header row sits ABOVE the parens. Placements were
// computed by make_parens047.py from the measured stroke centres/extents.
// entry = [x, y, w, h] in ABSOLUTE frame px.
// ============================================================
const PAREN2 = [
  [88.65, 74.04, 14.72, 36.35], [110.65, 74.04, 14.72, 36.35],
  [132.62, 74.04, 15.29, 36.35], [155.09, 74.04, 15.85, 36.35],
  [177.59, 74.04, 15.85, 36.35], [200.65, 74.04, 14.72, 36.35],
];
const PAREN3 = [
  [92.65, 171.94, 14.72, 61.70], [113.65, 171.94, 14.72, 61.70],
  [136.11, 171.94, 15.29, 61.70], [158.58, 171.94, 15.85, 61.70],
  [181.11, 171.94, 15.29, 61.70], [203.61, 171.94, 15.29, 61.70],
];
const PARENZ = [
  [597.05, 76.94, 16.42, 37.56], [620.12, 76.94, 15.29, 37.56],
  [642.12, 76.94, 15.29, 37.56],
];
function placeParen(px, py, pw, ph, file) {
  s.addImage({ path: ASSET + file, x: ax(px), y: ay(py), w: fw(pw), h: fh(ph) });
}
// One digit inside a paren pair, optically centred on the column's paren centre.
function placeDigit(txt, colCentre, bandCentre, fs, color) {
  s.addText(txt, {
    x: ax(colCentre - 8), y: ay(bandCentre - 10), w: fw(16), h: fh(20),
    fontFace: FONT, fontSize: fs, color: color, margin: 0,
    align: "center", valign: "middle",
  });
}
// Header / class glyph, centred on the column's paren centre.
function placeCell(txt, colCentre, bandCentre, fs, color, bold) {
  s.addText(txt, {
    x: ax(colCentre - 12), y: ay(bandCentre - 9), w: fw(24), h: fh(18),
    fontFace: FONT, fontSize: fs, color: color, bold: !!bold, margin: 0,
    align: "center", valign: "middle",
  });
}
const SUB1 = "\u2081", SUB2 = "\u2082";
const HDR = ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"];
const CLASS = (n) => n === 1 ? "C" + SUB1 : "C" + SUB2;

// ============================================================
// 1. TOP BAND: bordered box (abs x68..720, y55..130)
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: fx(14), y: fy(10), w: fw(652), h: fh(75),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.75 },
});

// ---- 1a. TOP-LEFT data matrix ----
// header x1..x6 (abs y63..74, centre 68.5); each column is a 2-component
// column vector in spanning parens (abs y77..107) with digit bands centred
// y84 / y101; class row (abs y113..125, centre 119).
{
  const centres = [96, 118, 140.25, 163, 185.5, 208];
  const bands = [84, 101];
  const data = [[1, 1], [2, 1], [1, 2], [5, 4], [6, 5], [6, 6]];
  const klass = [1, 1, 1, 2, 2, 2];
  for (let i = 0; i < 6; i++) {
    placeParen(...PAREN2[i], "eq_047_span2.png");
    placeCell(HDR[i], centres[i], 68.5, 14, BLACK, true);
    for (let b = 0; b < 2; b++) placeDigit(String(data[i][b]), centres[i], bands[b], 14, BLACK);
    placeCell(CLASS(klass[i]), centres[i], 119, 14, klass[i] === 1 ? RED : BLUE, true);
  }
}

// ---- 1b. TOP-CENTER params ----
// "Initial W =" black (abs x266..354 y75..84)
s.addText("Initial W =", {
  x: fx(212), y: fy(30), w: fw(68), h: fh(12),
  fontFace: FONT, fontSize: 14, color: BLACK, margin: 0,
  align: "left", valign: "middle",
});
// W column vector (4;-2;-2) with ROUND parentheses per measured frame:
// paren strokes abs x327..330 and x350..353, y58..106
{
  const bx = fx(273), by = fy(13), bw = fw(26), bh = fh(48);
  const paren = { file: "eq_047_parens.png", w_in: 0.49833, h_in: 0.47, baseline_frac: 0.97163 };
  s.addImage({ path: ASSET + paren.file, x: fx(272), y: fy(10), w: fw(30), h: fh(33) });
  for (const r of [ { t: "4",  y: fy(16) }, { t: "-2", y: fy(32) }, { t: "-2", y: fy(48) } ]) {
    s.addText(r.t, {
      x: bx + fw(8), y: r.y, w: fw(13), h: fh(11),
      fontFace: FONT, fontSize: 14, color: BLACK, margin: 0,
      align: "center", valign: "middle",
    });
  }
}
// "Step η = 2" RED (abs x366..435 y66..80) — measured red, right of the W bracket
s.addText([
  { text: "Step \u03b7 = 2", options: { fontFace: FONT, fontSize: 13, color: RED, bold: true } },
], {
  x: fx(312), y: fy(21), w: fw(72), h: fh(15),
  fontFace: FONT, margin: 0, align: "left", valign: "middle",
});
// "Check classes of" BLACK (abs x499..583 y78..89) — left of the Z matrix
s.addText("Check classes of", {
  x: fx(445), y: fy(31), w: fw(105), h: fh(13),
  fontFace: FONT, fontSize: 13, color: BLACK, margin: 0,
  align: "left", valign: "middle",
});

// ---- 1c. legend line (abs x239..509, y110..124) ----
s.addText([
  { text: "C\u2081", options: { fontFace: FONT, fontSize: 13, color: RED } },
  { text: " positive ", options: { fontFace: FONT, fontSize: 13, color: BLACK } },
  { text: "C\u2082", options: { fontFace: FONT, fontSize: 13, color: BLUE } },
  { text: "negative", options: { fontFace: FONT, fontSize: 13, color: BLACK } },
  { text: "Zero", options: { fontFace: FONT, fontSize: 13, color: GREEN } },
  { text: " is unaccepted", options: { fontFace: FONT, fontSize: 13, color: BLACK } },
], {
  x: fx(182), y: fy(64), w: fw(272), h: fh(16),
  fontFace: FONT, margin: 0, align: "left", valign: "middle",
});

// ---- 1d. TOP-RIGHT: Z matrix ----
// header Z1 Z1 Z1 (abs y64..77, centre 70.5); each column is a 2-component
// column vector in spanning parens (abs y80..111) with digit bands centred
// y87 / y103.
{
  const centres = [605.25, 627.75, 649.75];
  const bands = [87, 103];
  const data = [[0, 0], [7, 6], [3, 2]];
  for (let i = 0; i < 3; i++) {
    placeParen(...PARENZ[i], "eq_047_span2.png");
    placeCell("Z" + SUB1, centres[i], 70.5, 13, BLACK, true);
    for (let b = 0; b < 2; b++) placeDigit(String(data[i][b]), centres[i], bands[b], 13, BLACK);
  }
}

// ============================================================
// 2. MID-LEFT: "Ugmented Vectors ( from Top )" inside a bordered box
//    box abs x69..247, y139..256 (measured 2px strokes); interior white
//    title abs x81..236, y147..160 — BLUE (measured ink core B-G=+78)
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: fx(15), y: fy(94), w: fw(178), h: fh(117),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.75 },
});
s.addText("Ugmented Vectors ( from Top )", {
  x: fx(22), y: fy(101), w: fw(172), h: fh(16),
  fontFace: FONT, fontSize: 13, color: BLUE, margin: 0,
  align: "left", valign: "middle",
});
// matrix: header x1..x6 (abs y165..176, centre 170.5); each column is a
// 3-component column vector in spanning parens (abs y179..226) with digit
// bands centred y187.5 / 202.5 / 218.5; class row (abs y231..243, centre 237).
{
  const centres = [100, 121, 143.75, 166.5, 188.75, 211.25];
  const bands = [187.5, 202.5, 218.5];
  const data = [[1, 1, 1], [1, 2, 1], [1, 1, 2], [1, 5, 4], [1, 6, 5], [1, 6, 6]];
  const klass = [1, 1, 1, 2, 2, 2];
  for (let i = 0; i < 6; i++) {
    placeParen(...PAREN3[i], "eq_047_span3.png");
    placeCell(HDR[i], centres[i], 170.5, 13, BLACK, true);
    for (let b = 0; b < 3; b++) placeDigit(String(data[i][b]), centres[i], bands[b], 13, BLACK);
    placeCell(CLASS(klass[i]), centres[i], 237, 13, klass[i] === 1 ? RED : BLUE, true);
  }
}

// ============================================================
// 3. MID-RIGHT: three bordered calculation boxes (abs x273..855)
//    box1 y139..198 | box2 y206..264 | box3 y271..330
// ============================================================
const calcBoxes = [
  { top: 139, bot: 198,
    eq: { file: "eq_047_dz_1.png", w_in: 2.43833, h_in: 0.56667, baseline_frac: 0.92353 },
    val: { file: "eq_047_v_1.png", w_in: 0.47167, h_in: 0.17833, baseline_frac: 0.92523 },
    arrow: "Positive > 0", arrowColor: RED, klass: "Class I", klassColor: RED },
  { top: 206, bot: 264,
    eq: { file: "eq_047_dz_2.png", w_in: 2.43833, h_in: 0.56667, baseline_frac: 0.92353 },
    val: { file: "eq_047_v_2.png", w_in: 0.64833, h_in: 0.17833, baseline_frac: 0.92523 },
    arrow: "Negative < 0", arrowColor: BLUE, klass: "Class II", klassColor: BLUE },
  { top: 271, bot: 330,
    eq: { file: "eq_047_dz_3.png", w_in: 2.43833, h_in: 0.56667, baseline_frac: 0.92353 },
    val: { file: "eq_047_v_3.png", w_in: 0.50667, h_in: 0.18167, baseline_frac: 0.92661 },
    arrow: "Negative < 0", arrowColor: BLUE, klass: "Class II", klassColor: BLUE },
];

for (const box of calcBoxes) {
  s.addShape(pptx.ShapeType.rect, {
    x: fx(219), y: fy(box.top - 45), w: fw(582), h: fh(box.bot - box.top),
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.75 },
  });
  const baselineIn = fy((box.top + box.bot) / 2 - 45 + 4);
  placeEq(box.eq, baselineIn, fx(230));
  placeEq(box.val, baselineIn, fx(371));
  s.addText("\u21d2 " + box.arrow, {
    x: fx(455), y: fy(box.top - 45), w: fw(90), h: fh(box.bot - box.top),
    fontFace: FONT, fontSize: 14, color: box.arrowColor, bold: true,
    align: "left", valign: "middle", margin: 0,
  });
  s.addText(box.klass, {
    x: fx(605), y: fy(box.top - 45), w: fw(75), h: fh(box.bot - box.top),
    fontFace: FONT, fontSize: 14, color: box.klassColor, bold: true,
    align: "left", valign: "middle", margin: 0,
  });
}

// ============================================================
// 4. BOTTOM-LEFT red button "Check Classes" (abs x79..238, y278..304)
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: fx(25), y: fy(233), w: fw(160), h: fh(27),
  fill: { color: RED }, line: { color: RED, width: 0.75 },
});
s.addText("Check Classes", {
  x: fx(25), y: fy(233), w: fw(160), h: fh(27),
  fontFace: FONT, fontSize: 14, color: "FFFFFF", bold: true,
  align: "center", valign: "middle",
});

pptx.writeFile({ fileName: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_047_recreated.pptx" })
  .then((f) => console.log("WROTE " + f));
