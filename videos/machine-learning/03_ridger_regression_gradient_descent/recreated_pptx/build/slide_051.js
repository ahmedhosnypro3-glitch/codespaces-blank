// Slide 051 — machine-learning/03_ridger_regression_gradient_descent
// "Check Classes" (Perceptron — final slide of the deck). ATTEMPT 4.
//
// Attempt-4 fixes (crop_3_dec judge + pixel adjudication):
//   row-3 label d(Z3)= -> d(Z2)=  (original prints Z2 on row 3 — source typo,
//               verbatim-ink law; dzlabel_3.png = dzlabel_2.png bytes, h 111->110)
//   ASCII hyphens -> U+2212 true minus in wcol_green/initw rows and "= −8" val
//               (regenerated via w051_wcol.py, W051_OVER_PT 1.5/2.2; ink boxes
//               unchanged: 223x360 + 223x378, ink 13/0)
//
// Attempt-2 judge findings addressed here (qa/slide051/judge_attempt_2.txt):
//   #1 BLOCKER  d(Zn) rows missing the blue test vector + "=" after d(Zi)
//               -> dzlabel/rowvec mathtext PNGs (600dpi, native scale)
//   #2 MAJOR    "Step n = 1" -> mathtext PNG with real eta (eq_051_step, #A1232A)
//   #3 MAJOR    vertical-bar delimiters -> bezier paren PNGs (parens051,
//               direction-verified: LP belly leftmost, RP belly rightmost)
//               on sample/Z/aug columns; initw column -> parenthesized PNG
//   #4 MAJOR    "Check classes of" wrap -> wider box (w105)
//   #5 MAJOR    row-3 condition wrap -> wider box (w130)
//   #6 MAJOR    missing => glyphs -> kept as the measured double-line arrows
//               (ground truth: 051 prints drawn arrows, see delta_vs_related.md D6)
//   #7 MINOR    d(Zi) subscript cramped -> mathtext PNG
//   #8 MINOR    "Augmented Vectors (from Top)" -> bold ITALIC
//
// MEASURED GEOMETRY (frame px; 1px = 1pt; qa/slide051/w051_assets2.json + HANDOFF.md):
//
//   chrome          : panel x54..903 y45..540 (E9E9E7), C00000 1pt strokes
//                     LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 (NO top stroke),
//                     badge d35 centred (876,73), numeral "51"
//   pale card       : x68..720 y54..130, border (32,24,109) 2pt, fill (254,255,232)
//   sample matrix   : 6 paren-pair columns; LP bows x89/111/133/156/179/201,
//                     RP bows x102/124/147/170/192/214, paren ink top y78;
//                     digit rows top y78/y94 (h12 fs11), column centres
//                     96/117.5/140.5/163/185.5/208; rows (1,1)(2,1)(1,2)(5,4)(6,5)(6,6);
//                     header x1..x6 centres 94/116.5/140.5/161/184/209 (y64..74);
//                     class row y110..125 — C1 red c93.5/116.5/140.5, C2 blue c163.5/185.5/208.5
//   centre block    : "Initial W =" x265..315 y75..85; parenthesized column vector
//                     [4;-2;-2] PNG ink-left 329.5 ink-top 59; red "Step eta = 1"
//                     mathtext PNG ink-left 365 ink-top 67 (#A1232A)
//   legend          : y110..124 — C1(red) x240..255, positive x262..312,
//                     C2(blue) x327..336, negative x344..396,
//                     Zero(green) x413..439, "is unaccepted" x447..520
//   label           : "Check classes of" x497 y76 w105 h16 fs12 bold (one line)
//   Z test matrix   : 3 paren-pair columns; LP bows x597/621/643, RP bows x612/634/656,
//                     paren ink top y81; digit rows top y81/y97, centres 605/627.5/649.5:
//                     Z1=(0,0) Z2=(7,6) Z3=(3,2) (arithmetic-forced reading).
//                     Header Z1 Z2 Z3 y64..76, centres 606.5/628/649.
//   augmented matrix: white card x69..246 y139..256 (hairline border), heading
//                     "Augmented Vectors (from Top)" NAVY bold ITALIC
//                     x74 y146 w182 fs11.5; 6 paren-pair columns; LP bows
//                     x93/114/137/159/182/204, RP bows x107/128/151/173/195/218,
//                     paren ink top y180; digit rows top y182/197/212, centres
//                     100.5/121.5/144/166.5/188.5/211.5;
//                     columns (1,1,1)(1,2,1)(1,1,2)(1,5,4)(1,6,5)(1,6,6);
//                     header x1..x6 y166..175; class row y231..243
//   red box         : x78..239 y277..305, fill (194,0,3), white bold "Check Classes"
//   decision rows   : three white cards x274..853, tops y140/206/272 h57 (2pt border).
//                     Row chain, all mathtext PNGs at native scale:
//                       dzlabel "d(Zn)=" ink-left 283, ink-top 160/230/296
//                       rowvec "(1 0 0)"-style, BLUE #0F0087, rp-apex x378.5,
//                         ink-top 149/218/284
//                       wcol "(5 -1 -1)" green PNG ink-left 381, ink-top 148/218/284
//                     then "=" x411, value x422 (5/-8/0), drawn double-line arrow
//                     x500/510/500, condition x522/531/512 (w100/100/130),
//                     class tag x655 RED / x668 BLUE / x652 BLUE; text baselines
//                     171/240/306 (TEXT_TOP = b-11).
//   bottom-right    : connected-component scan finds NO mouse-pointer cursor in the
//                     frame (only the bottom chrome stroke) — nothing drawn.

const pptxgenpkg = require("pptxgenjs");
const path = require("path");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in == 960x540 px at 1px=1pt
const s = pptx.addSlide();

drawHouseChrome(pptx, s, { numeral: "51" });

// ---------- helpers: frame px -> inches ----------
const fx = (px) => px / 72;

const FONT = "Arial";
const BLACK = "000000";
const WHITE = "FFFFFF";
const CREAM = "FEFFE8";        // measured pale-card fill (254,255,232)
const NAVY = "20186D";         // measured pale-card border (32,24,109)
const RED = "C00000";          // measured red text (~159,2,13)
const RED_BOX = "C90004";      // measured red-box fill (194,0,3)
const BLUE = "0000A8";         // measured blue text (~15,0,135)
const GREEN_DK = "27331A";     // measured legend "Zero" green (~59,71,45)
const CARD_BORDER = "9FA8B1";  // measured decision-card border (159,168,177)
const HAIRLINE = "A6A6A6";     // measured aug-card hairline (edge px ~196-210 gray)

const ASSET_DIR = path.join(__dirname, "assets");
const PPPT = 72 / 600; // pt per asset px (all assets are 600dpi: 1px = 0.12pt)

// Paren-pair PNG placement — 049 certified convention (bows = belly centroids):
//   LP: image x = bow - (ink_left_px*PPPT + S_pt/2)
//   RP: image x = bow + 0.5 - ((ink_right_px+1)*PPPT - S_pt/2)
//   Y : image y = inkTopTarget - ink_top_px*PPPT
// parens051 sidecars (w051_assets2.json): ink_left 4, ink_right 24, S 1.5,
// px_w 29; ink_top/px_h per group (sample 3/241, z 4/250, aug 4/375).
function parenPair(group, lpBow, rpBow, inkTop) {
  const inkTopPx = group === "sample51" ? 3 : 4;
  const pxH = group === "sample51" ? 241 : (group === "z51" ? 250 : 375);
  const wIn = 29 * PPPT / 72, hIn = pxH * PPPT / 72;
  s.addImage({
    path: path.join(ASSET_DIR, "parens051/paren_" + group + "_lp.png"),
    x: fx(lpBow - (4 * PPPT + 1.5 / 2)),
    y: fx(inkTop - inkTopPx * PPPT),
    w: wIn, h: hIn,
  });
  s.addImage({
    path: path.join(ASSET_DIR, "parens051/paren_" + group + "_rp.png"),
    x: fx(rpBow + 0.5 - ((24 + 1) * PPPT - 1.5 / 2)),
    y: fx(inkTop - inkTopPx * PPPT),
    w: wIn, h: hIn,
  });
}

// plain text digits for one column of a paren-pair matrix
function colDigits(centre, rowTops, vals) {
  vals.forEach(function (v, i) {
    s.addText(v, {
      x: fx(centre - 8), y: fx(rowTops[i]), w: fx(16), h: fx(12),
      fontFace: FONT, fontSize: 11, color: BLACK,
      align: "center", valign: "middle", margin: 0,
    });
  });
}

// mathtext/PIL asset PNG at native scale, anchored by its ink box
// target* = deck-px position of the asset's ink edge (sidecar ink_*_px)
function eqPng(file, inkLeftTarget, inkTopTarget, inkLeftPx, inkTopPx, wPx, hPx) {
  s.addImage({
    path: path.join(ASSET_DIR, file),
    x: fx(inkLeftTarget - inkLeftPx * PPPT),
    y: fx(inkTopTarget - inkTopPx * PPPT),
    w: wPx / 600, h: hPx / 600,
  });
}

// subscripted "C1"/"C2" class tag centred at cx
function classTag(cx, y, digit, color) {
  s.addText([
    { text: "C", options: { fontSize: 10, color: color, bold: true } },
    { text: digit, options: { fontSize: 8, color: color, bold: true, subscript: true } },
  ], {
    x: fx(cx - 11), y: fx(y), w: fx(22), h: fx(16),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
}

// ================= 1. PALE CARD (x68..720, y54..130) =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(68), y: fx(54), w: fx(720 - 68), h: fx(130 - 54),
  fill: { color: CREAM }, line: { color: NAVY, width: 2 },
});

// ================= 2. LEFT SAMPLE MATRIX (6 paren-pair columns) =================
const SAMPLE = [
  { hdr: 94,    lp: 89,  rp: 102, c: 96,    vals: ["1", "1"], cls: "1" },
  { hdr: 116.5, lp: 111, rp: 124, c: 117.5, vals: ["2", "1"], cls: "1" },
  { hdr: 140.5, lp: 133, rp: 147, c: 140.5, vals: ["1", "2"], cls: "1" },
  { hdr: 161,   lp: 156, rp: 170, c: 163,   vals: ["5", "4"], cls: "2" },
  { hdr: 184,   lp: 179, rp: 192, c: 185.5, vals: ["6", "5"], cls: "2" },
  { hdr: 209,   lp: 201, rp: 214, c: 208,   vals: ["6", "6"], cls: "2" },
];
const SAMPLE_ROWS = [78, 94];
SAMPLE.forEach(function (col, i) {
  s.addText([
    { text: "x", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(col.hdr - 9), y: fx(63), w: fx(18), h: fx(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
  parenPair("sample51", col.lp, col.rp, 78);
  colDigits(col.c, SAMPLE_ROWS, col.vals);
  classTag(col.c, 110, col.cls, col.cls === "1" ? RED : BLUE);
});

// ================= 3. CENTRE BLOCK =================
// "Initial W =" (black)
s.addText([
  { text: "Initial ", options: { fontSize: 12, color: BLACK } },
  { text: "W", options: { fontSize: 12, color: BLACK, bold: true, italic: true } },
  { text: " =", options: { fontSize: 12, color: BLACK } },
], {
  x: fx(263), y: fx(74), w: fx(58), h: fx(14),
  fontFace: FONT, align: "left", valign: "middle", margin: 0,
});

// parenthesized column vector [4; -2; -2] — full-column PIL PNG
// (eq_051_initw 223x378, ink_left 13, ink_top 0; ink-left 329.5, ink-top 59)
eqPng("eq_051_initw.png", 329.5, 59, 13, 0, 223, 378);

// red "Step eta = 1" — mathtext PNG (eq_051_step 583x121, #A1232A,
// ink_left 8, ink_top 8; ink-left 365, ink-top 67)
eqPng("eq_051_step.png", 365, 67, 8, 8, 583, 121);

// ================= 4. LEGEND (y110..124) =================
s.addText([
  { text: "C", options: { fontSize: 10, color: RED, bold: true } },
  { text: "1", options: { fontSize: 8, color: RED, bold: true, subscript: true } },
], {
  x: fx(240), y: fx(109), w: fx(18), h: fx(16),
  fontFace: FONT, align: "left", valign: "middle", margin: 0,
});
s.addText("positive", {
  x: fx(262), y: fx(109), w: fx(52), h: fx(16),
  fontFace: FONT, fontSize: 11, color: BLACK, italic: true, align: "left", valign: "middle", margin: 0,
});
s.addText([
  { text: "C", options: { fontSize: 10, color: BLUE, bold: true } },
  { text: "2", options: { fontSize: 8, color: BLUE, bold: true, subscript: true } },
], {
  x: fx(327), y: fx(109), w: fx(18), h: fx(16),
  fontFace: FONT, align: "left", valign: "middle", margin: 0,
});
s.addText("negative", {
  x: fx(344), y: fx(109), w: fx(54), h: fx(16),
  fontFace: FONT, fontSize: 11, color: BLACK, italic: true, align: "left", valign: "middle", margin: 0,
});
s.addText("Zero", {
  x: fx(413), y: fx(109), w: fx(28), h: fx(16),
  fontFace: FONT, fontSize: 11, color: "5B9C4E", bold: true, italic: true, align: "left", valign: "middle", margin: 0,
});
s.addText("is unaccepted", {
  x: fx(447), y: fx(109), w: fx(76), h: fx(16),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// "Check classes of" label — w105 keeps it on ONE line (att2 #4); regular weight
// per att4 full+mats judge consensus (orig is not bold)
s.addText("Check classes of", {
  x: fx(497), y: fx(76), w: fx(105), h: fx(16),
  fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// ================= 5. RIGHT Z TEST MATRIX (3 paren-pair columns) =================
const Z_COLS = [
  { hdr: 606.5, lp: 597, rp: 612, c: 605,    vals: ["0", "0"] },
  { hdr: 628,   lp: 621, rp: 634, c: 627.5,  vals: ["7", "6"] },
  { hdr: 649,   lp: 643, rp: 656, c: 649.5,  vals: ["3", "2"] },
];
const Z_ROWS = [81, 97];
Z_COLS.forEach(function (col, i) {
  s.addText([
    { text: "Z", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(col.hdr - 9), y: fx(63), w: fx(18), h: fx(14),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
  parenPair("z51", col.lp, col.rp, 81);
  colDigits(col.c, Z_ROWS, col.vals);
});

// ================= 6. AUGMENTED MATRIX (middle-left, 6 paren-pair columns) ========
// white card + hairline border around the block, measured on the original frame:
// edges x69-70 / x245-246, y139-140 / y255-256 (slide_045 card idiom)
s.addShape(pptx.ShapeType.rect, {
  x: fx(69), y: fx(139), w: fx(246 - 69), h: fx(256 - 139),
  fill: { color: WHITE }, line: { color: HAIRLINE, width: 1 },
});

// bold ITALIC per att2 #8; verbatim ink per orig: "Ugmented" (no A) + spaced parens
// (043 founder-delta class; pixel-confirmed 2026-10-26)
s.addText("Ugmented Vectors ( from Top )", {
  x: fx(74), y: fx(146), w: fx(182), h: fx(14),
  fontFace: FONT, fontSize: 11.5, color: NAVY, bold: true, italic: true,
  align: "left", valign: "middle", margin: 0,
});

const AUG = [
  { hdr: 100.5, lp: 93,  rp: 107, c: 100.5,  vals: ["1", "1", "1"], cls: "1" },
  { hdr: 121.5, lp: 114, rp: 128, c: 121.5,  vals: ["1", "2", "1"], cls: "1" },
  { hdr: 144,   lp: 137, rp: 151, c: 144,    vals: ["1", "1", "2"], cls: "1" },
  { hdr: 166.5, lp: 159, rp: 173, c: 166.5,  vals: ["1", "5", "4"], cls: "2" },
  { hdr: 188.5, lp: 182, rp: 195, c: 188.5,  vals: ["1", "6", "5"], cls: "2" },
  { hdr: 211.5, lp: 204, rp: 218, c: 211.5,  vals: ["1", "6", "6"], cls: "2" },
];
const AUG_ROWS = [182, 197, 212];
AUG.forEach(function (col, i) {
  s.addText([
    { text: "x", options: { fontSize: 10, color: BLACK, italic: true } },
    { text: String(i + 1), options: { fontSize: 8, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(col.hdr - 9), y: fx(165), w: fx(18), h: fx(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
  parenPair("aug51", col.lp, col.rp, 180);
  colDigits(col.c, AUG_ROWS, col.vals);
  classTag(col.c, 229, col.cls, col.cls === "1" ? RED : BLUE);
});

// ================= 7. RED "Check Classes" BOX =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(78), y: fx(277), w: fx(239 - 78), h: fx(305 - 277),
  fill: { color: RED_BOX }, line: { color: RED_BOX, width: 1 },
});
s.addText("Check Classes", {
  x: fx(78), y: fx(277), w: fx(239 - 78), h: fx(305 - 277),
  fontFace: FONT, fontSize: 13, color: WHITE, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ================= 8. THREE DECISION ROWS =================
// White cards, border cores measured at x274 / x853, top y140 / y206 / y272,
// bottom y197 / y263 / y329. Row chain: dzlabel PNG (d(Zn)=, with "="),
// rowvec PNG (blue parenthesized test vector), wcol PNG (green weight column),
// then "=", value, drawn double-line arrow, condition, class tag.
const DEC_ROWS = [
  {
    dzTop: 160, rvTop: 149, wcTop: 148,
    val: "5", arrow: [500, 165],
    cond: "Positive > 0", condX: 522, condW: 100, cls: "Class I", clsX: 655, clsColor: RED,
  },
  {
    dzTop: 230, rvTop: 218, wcTop: 218,
    val: "−8", arrow: [510, 234],
    cond: "Negative < 0", condX: 531, condW: 100, cls: "Class II", clsX: 668, clsColor: BLUE,
  },
  {
    dzTop: 296, rvTop: 284, wcTop: 284,
    val: "0", arrow: [500, 300],
    cond: "Not > 0 , Not < 0", condX: 512, condW: 130, cls: "Undefined Class", clsX: 652,
    clsColor: BLUE,
  },
];

// text box tops for a 12pt Arial baseline, h=14, valign middle
const TEXT_TOP = (baseline) => baseline - 11;
// row baselines 171 / 240 / 306
const BASES = [171, 240, 306];

// the small double-line right arrow measured at x500..509 / y165..170
function implyArrow(x, y) {
  s.addShape(pptx.ShapeType.line, {
    x: fx(x), y: fx(y + 1.5), w: fx(5), h: 0,
    line: { color: BLACK, width: 1 },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(x), y: fx(y + 3.5), w: fx(5), h: 0,
    line: { color: BLACK, width: 1 },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(x + 5), y: fx(y), w: fx(4), h: fx(2),
    line: { color: BLACK, width: 1 },
  });
  s.addShape(pptx.ShapeType.line, {
    x: fx(x + 5), y: fx(y + 2), w: fx(4), h: fx(2), flipV: true,
    line: { color: BLACK, width: 1 },
  });
}

DEC_ROWS.forEach(function (row, idx) {
  // white card
  s.addShape(pptx.ShapeType.rect, {
    x: fx(274), y: fx(140 + idx * 66), w: fx(853 - 274), h: fx(57),
    fill: { color: WHITE }, line: { color: CARD_BORDER, width: 2 },
  });

  // "d(Zn)=" black mathtext PNG (ink_left 8, ink_top 8; ink-left 283)
  eqPng("eq_051_dzlabel_" + (idx + 1) + ".png", 283, row.dzTop, 8, 8, 370, 110);

  // blue parenthesized test vector "(1 0 0)" — mathtext PNG anchored by the
  // right paren's apex: canvas apex x 423.5px -> target 378.5
  eqPng("eq_051_rowvec_" + (idx + 1) + ".png", 378.5 - (423.5 - 8) * PPPT, row.rvTop, 8, 8, 455, 132);

  // green weight column "(5 -1 -1)" — full-column PIL PNG
  // (eq_051_wcol_green 223x360, ink_left 13, ink_top 0; ink-left 381)
  eqPng("eq_051_wcol_green.png", 381, row.wcTop, 13, 0, 223, 360);

  // black "=" and the result value
  s.addText("=", {
    x: fx(411), y: fx(TEXT_TOP(BASES[idx])), w: fx(12), h: fx(14),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });
  s.addText(row.val, {
    x: fx(422), y: fx(TEXT_TOP(BASES[idx])), w: fx(34), h: fx(14),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });

  implyArrow(row.arrow[0], row.arrow[1]);

  // condition text and the class tag
  s.addText(row.cond, {
    x: fx(row.condX), y: fx(TEXT_TOP(BASES[idx])), w: fx(row.condW), h: fx(14),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });
  s.addText(row.cls, {
    x: fx(row.clsX), y: fx(TEXT_TOP(BASES[idx])), w: fx(100), h: fx(14),
    fontFace: FONT, fontSize: 12, color: row.clsColor, bold: true,
    align: "left", valign: "middle", margin: 0,
  });
});

// ================= OUTPUT =================
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_051_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
