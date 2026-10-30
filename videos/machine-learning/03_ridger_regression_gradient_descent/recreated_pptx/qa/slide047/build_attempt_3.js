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

const ASSET = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/";
function placeEq(img, baselineYIn, xIn) {
  const yTop = baselineYIn - img.baseline_frac * img.h_in;
  s.addImage({ path: ASSET + img.file, x: xIn, y: yTop, w: img.w_in, h: img.h_in });
}

// ============================================================
// 1. TOP BAND: bordered box (abs x68..720, y55..130)
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: fx(14), y: fy(10), w: fw(652), h: fh(75),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.75 },
});

// ---- 1a. TOP-LEFT data matrix (abs x88..217; rows y63-74/77-89/93-107/110-125) ----
const SUB1 = "\u2081";
const CLASS_ROW = ["C\u2081","C\u2081","C\u2081","C\u2082","C\u2082","C\u2082"];
const TLX = fx(34), TLY = fy(18), TLW = fw(129);
s.addTable([
  ["x\u2081","x\u2082","x\u2083","x\u2084","x\u2085","x\u2086"],
  ["(1)","(2)","(1)","(5)","(6)","(6)"],
  ["(1)","(1)","(2)","(4)","(5)","(6)"],
  CLASS_ROW,
].map((row, ri) => row.map((txt) => {
  const o = { fontFace: FONT, fontSize: 14, align: "center", valign: "middle", margin: 0 };
  if (ri === 0) { o.bold = true; o.color = BLACK; }
  else if (ri === 3) { o.bold = true; o.color = txt.indexOf(SUB1) !== -1 ? RED : BLUE; }
  else { o.color = BLACK; }
  return { text: txt, options: o };
})), {
  x: TLX, y: TLY, w: TLW, h: fh(63),
  fontFace: FONT, border: { pt: 0, color: "FFFFFF" }, fill: { color: "FFFFFF" },
  colW: [TLW / 6, TLW / 6, TLW / 6, TLW / 6, TLW / 6, TLW / 6],
  rowH: [fh(14), fh(14), fh(16), fh(17)],
});

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
// "Check classes of" BLACK (abs x499..582 y78..89) — left of the Z matrix
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

// ---- 1d. TOP-RIGHT: Z matrix (abs x597..657; hdr y64..77, r1 y79..92, r2 y98..111) ----
{
  const ZX = fx(543), ZY = fy(19), ZW = fw(62);
  s.addTable([
    ["Z\u2081", "Z\u2081", "Z\u2081"],
    ["(0)", "(7)", "(3)"],
    ["(0)", "(6)", "(2)"],
  ].map((row, ri) => row.map((txt) => ({
    text: txt,
    options: {
      fontFace: FONT, fontSize: 13, bold: (ri === 0), color: BLACK,
      align: "center", valign: "middle", margin: 0,
    },
  }))), {
    x: ZX, y: ZY, w: ZW, h: fh(48),
    fontFace: FONT, border: { pt: 0, color: "FFFFFF" }, fill: { color: "FFFFFF" },
    colW: [ZW / 3, ZW / 3, ZW / 3],
    rowH: [fh(16), fh(16), fh(16)],
  });
}

// ============================================================
// 2. MID-LEFT: "Augmented Vectors (from Top)" inside a bordered box
//    box abs x69..247, y139..256 (measured 2px strokes); interior white
// ============================================================
s.addShape(pptx.ShapeType.rect, {
  x: fx(15), y: fy(94), w: fw(178), h: fh(117),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.75 },
});
// title abs x81..237, y147..160, ONE line (build must not wrap)
s.addText("Augmented Vectors (from Top)", {
  x: fx(14), y: fy(101), w: fw(178), h: fh(15),
  fontFace: FONT, fontSize: 12, color: BLACK, margin: 0,
  align: "left", valign: "middle",
});
{
  const AX = fx(41), AY = fy(120), AW = fw(125);
  s.addTable([
    ["x\u2081","x\u2082","x\u2083","x\u2084","x\u2085","x\u2086"],
    ["(1)","(1)","(1)","(1)","(1)","(1)"],
    ["(1)","(2)","(1)","(5)","(6)","(6)"],
    ["(1)","(1)","(2)","(4)","(5)","(6)"],
    CLASS_ROW,
  ].map((row, ri) => row.map((txt) => {
    const o = { fontFace: FONT, fontSize: 13, align: "center", valign: "middle", margin: 0 };
    if (ri === 0) { o.bold = true; o.color = BLACK; }
    else if (ri === 4) { o.bold = true; o.color = txt.indexOf(SUB1) !== -1 ? RED : BLUE; }
    else { o.color = BLACK; }
    return { text: txt, options: o };
  })), {
    x: AX, y: AY, w: AW, h: fh(80),
    fontFace: FONT, border: { pt: 0, color: "FFFFFF" }, fill: { color: "FFFFFF" },
    colW: [AW / 6, AW / 6, AW / 6, AW / 6, AW / 6, AW / 6],
    rowH: [fh(11), fh(11), fh(15), fh(15), fh(13)],
  });
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
  align: "center", valign: "middle", margin: 0,
});

pptx.writeFile({ fileName: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_047_recreated.pptx" })
  .then((f) => console.log("WROTE " + f));
