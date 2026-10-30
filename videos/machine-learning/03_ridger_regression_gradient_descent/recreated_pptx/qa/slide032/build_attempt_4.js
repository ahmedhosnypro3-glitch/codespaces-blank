// Build: slide 032 — "Convex Function, Learning Rate =0.4, Start at X=3"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GEOMETRY SOURCE: PIL measurement of unique_slides/slide_032.jpg (960x540, 1px=1pt).
// Spec: analysis/slide_032_final.json + sibling pattern from slide_030.js / slide_031.js.
// Where spec and frame disagree, THE FRAME WINS. All frame px below are measured ink boxes.
//
// MEASURED LAYOUT (frame px, 960x540):
//   House chrome (deck standard shared_patterns/house_chrome.js):
//     canvas FFFFFF; gray panel E9E9E7 x54..903 y45..540 (no border);
//     C00000 1pt strokes LEFT x58.5 (rows46..539), RIGHT x901, BOTTOM y538.5; NO TOP STROKE;
//     badge circle d~35 centred (876,73), fill FDFD96, ring 6A5ACD 2pt, bold "32" Arial 18pt #333333.
//
//   Title (ONE line, on the PANEL GRAY — not white): bold Arial ~26pt in three runs
//     "Convex Function,  " C00000 | "Learning Rate =0.4,  " 008000 | "Start at X=3" 0000FF
//     measured ink x 80..557, y 63..88 (red 82..240 / green 260..432 / blue 446..557).
//     LibreOffice renders Arial ~0.84x the original's advance, so 22pt reproduces 477pt.
//
//   Parameter table (3 rows x 2 cols): x 76..208, y 178..251
//     Each ROW carries ONE fill across BOTH columns (no vertical split drawn):
//       row1 y178..202 = E8FFD5 | row2 y204..227 = F7BFC2 | row3 y229..251 = FBFF0B
//     thin dark outer border; black text; label col x76..142, value col x142..208.
//
//   Graph (top-right): WHITE plot interior x 576..806, y 69..305 (measured gridlines at
//     y277-278 / y288-290 / y301-302 continue below the x-axis on a white field;
//     the build's rect is
//     1px wider each side and is absorbed by the 1pt red stroke).
//     RE-MEASURED 2026-10-24 (worker-fresh-032c, MEASUREMENTS_STEP1.md items 6/7/11):
//     red 1pt frame LEFT x573 / RIGHT x810 / TOP y66, and the frame runs DOWN TO y309;
//     a red 1pt horizontal at y=309 spans x573..810. The gray 1pt line at y266 is the
//     x-axis; the white interior stops at y265 but the STROKES continue to y309 and the
//     black y-axis + red x=5 line both run y67..310 (measured: dark columns x631..632 and
//     red x687..689 persist down to y307, terminated by the y308..310 red band).
//     gridlines 0.5pt: vertical at data x=-4..15 (x=585,596,607,619,631[,642,653,664,676,
//       687.5,699,710,722,733,745,756,768,780,791,802]); horizontal at data y=1..16
//       (y=254,242,230,218,206,194,182,170,158,146,134,122,110,98,86,74)
//     axis: black 1pt y-axis at x=630 (data x=0), black 1pt x-axis at y=266
//     red 1pt vertical line at x=687.5 (data x=5) — same span as the axes
//     black 2pt horizontal CHORD at y=146 (data y=10) spanning the FULL interior
//       x576..806 (measured: y146 cluster x576..805 core 0A0000 — the inherited stub
//       x651..725 under-drew it by 149px)
//     GREEN solid dot 9x9 centre (687.5,254.5) = data (5,1)
//     RED solid dot 7x7 centre (661.5,182.5) -> data(2.7,6.96)
//     NO point labels, NO axis titles, and NO x-axis tick labels/marks below the plot —
//       the frame has no glyph ink there (census over y266..299 x548..835 in section U
//       of measure_probe3 shows only the axis/vertical-line/edge clusters).
//
//   Equation callout column (centre-left, x ~370..600):
//     box1 x 398..530, y 184..212 : RED border 1.5pt (measured y185..187 and y210..212),
//           WHITE fill — mathtext equation PNG
//     "X = 5" bold C00000, y 215..230
//     box2 x 370..540, y 232..281 : EFFFE2 fill, GREEN 1pt border TOP y234 / BOTTOM y279
//           (measured green runs x370..540 on both rows — the inherited "no border" is WRONG)
//           — "f(x) Minimum value is 1.0"
//     box3 x ~330..600, y ~291..320 : F7C9FA fill LOW BAND (measured F7C9FA-family ink
//           x331..599 on every row y291..320), no border — "Reach Minimum after 6 Steps"
//           800080 (the 800080 text glyphs themselves run y296..315)
//
//   CRIMSON down-arrow, x 349..372, y 317..355: a 3px wedge cap at y318..320 that splits
//     into two ~3px crimson strokes angling right-down (measured component n=263, cores
//     852735/842634). NOT C000C0 magenta and NOT at x540..568 — the inherited values are
//     both wrong; a whole-frame C000C0 census found no dense magenta object at all.
//
//   Iteration table (outer frame x 298..600, y 330..527):
//     outer border 564BA7 1pt on all four sides; NO internal vertical rules
//     FIVE colour bands, each a full-width cell with a white gap between bands:
//       band  olive    #D9E277 border #9B9B7F  y 344..383  holds rows 'x' + 'f(x)'
//       band lavender  #D6B3F7 border #A78CC2  y 387..424  holds rows 'x-delta' + 'f(x-delta)'
//       band  peach    #F7DEC0 border #C9B197  y 431..468  holds rows 'x+delta' + 'f(x+delta)'
//       band  green    #E8FFD5 border #40842F  y 472..494  holds row  'slope'
//       band  salmon   #F9BEC0 border #AA000B  y 497..517  holds row  'next x'
//     internal horizontal rule inside each band at its row split:
//       y 363.5 (olive), 406 (lavender), 450 (peach); green/salmon are single-row bands
//     text colours follow the band accent (measured ink cores):
//       olive band #767300 | lavender band #4B0082 | peach band #8B5A2B
//       green band #1E3010 | salmon band #7A1414
//
// Laws honored: hex without '#'; fontFace explicit everywhere; margin 0; measured geometry
// over intuition; explicit lineSpacing on multi-line text; single plain-named deliverable.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = __dirname + "/../slide_032_recreated.pptx";
const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();
const ST = pptx.ShapeType;
const A = "Arial";

drawHouseChrome(pptx, slide, { numeral: 32 });

// ------------------------------------------------------------------ TITLE
// Measured: ONE line, ink x 80..557 (red 82..240 / green 260..432 / blue 446..557).
// LibreOffice renders Arial ~0.84x wider than the original's renderer, so 22pt here
// reproduces the measured 477pt advance and keeps the blue run clear of the plot.
slide.addText(
  [
    { text: "Convex Function,  ", options: { fontSize: 22, bold: true, color: "C00000", fontFace: A } },
    { text: "Learning Rate =0.4,  ", options: { fontSize: 22, bold: true, color: "008000", fontFace: A } },
    { text: "Start at X=3", options: { fontSize: 22, bold: true, color: "0000FF", fontFace: A } },
  ],
  { x: px(80), y: px(64), w: px(500), h: px(28), margin: 0, align: "left", valign: "top" }
);

// ------------------------------------------------------- PARAMETER TABLE
// Measured: x 76..208, y 178..251. Each ROW carries one fill across BOTH columns
// (measured row1 ~E8FFD5, row2 ~F7BFC2, row3 ~FBFF0B at x 90..195).
const paramRows = [
  { label: "step", value: "0.4", fill: "E8FFD5" },
  { label: "initial X", value: "3", fill: "F7BFC2" },
  { label: "delta", value: "0.1", fill: "FBFF0B" },
];
const pTBL = 76, pTBV = 142, pTBR = 208;
const pRowY = [178, 204, 229];
const pRowH = [25, 24, 23];
paramRows.forEach((row, i) => {
  const y = px(pRowY[i]), h = px(pRowH[i]);
  // full-width row fill with a thin dark outer border
  slide.addShape(ST.rect, {
    x: px(pTBL), y, w: px(pTBR - pTBL), h,
    fill: { color: row.fill }, line: { color: "000000", width: 0.5 },
  });
  slide.addText(row.label, { x: px(pTBL), y, w: px(pTBV - pTBL), h, align: "center", valign: "middle", fontSize: 12, color: "000000", fontFace: A, margin: 0 });
  slide.addText(row.value, { x: px(pTBV), y, w: px(pTBR - pTBV), h, align: "center", valign: "middle", fontSize: 12, color: "000000", fontFace: A, margin: 0 });
});

// ----------------------------------------------------------------- GRAPH
// The white interior runs to y306, not y265: measured gridline rows at y277-278,
// y288-290 and y301-302 (= my(-1)=278, my(-2)=290, my(-3)=302 with YC=266/SY=12) sit on
// a white field down to y305, and the red frame band is at y308..310.
const GP = { x0: 574, x1: 809, y0: 67, y1: 306 };
const XC = 630, SX = 11.5;   // data x -> px
const YC = 266, SY = 12;     // data y -> px (inverted)
const mx = (v) => XC + SX * v;
const my = (v) => YC - SY * v;

// white plot background
slide.addShape(ST.rect, { x: px(GP.x0), y: px(GP.y0), w: px(GP.x1 - GP.x0), h: px(GP.y1 - GP.y0), fill: { color: "FFFFFF" }, line: { type: "none" } });

// gridlines — vertical every 1 data unit, horizontal every 1 data unit INCLUDING the three
// rows below data y=0 (measured y277-278, y288-290, y301-302)
for (let k = -4; k <= 15; k++) {
  const x = mx(k);
  if (x < GP.x0 || x > GP.x1) continue;
  slide.addShape(ST.line, { x: px(x), y: px(GP.y0), w: 0, h: px(GP.y1 - GP.y0), line: { color: "D9D9D9", width: 0.5 } });
}
for (let k = -3; k <= 16; k++) {
  const y = my(k);
  if (y < GP.y0 || y > GP.y1) continue;
  slide.addShape(ST.line, { x: px(GP.x0), y: px(y), w: px(GP.x1 - GP.x0), h: 0, line: { color: "D9D9D9", width: 0.5 } });
}

// plot frame: red LEFT x573 / RIGHT x810 / TOP y66, and the frame runs DOWN TO y309
// (measured: red clusters y309..310 span x573..810 solid). The white interior stops at
// y265; only the STROKES continue below, and the axes run with them down to y310.
slide.addShape(ST.line, { x: px(573), y: px(66), w: 0, h: px(309 - 66), line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(810), y: px(66), w: 0, h: px(309 - 66), line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(GP.x0), y: px(66), w: px(GP.x1 - GP.x0), h: 0, line: { color: "C00000", width: 1 } });
// red horizontal band at y=309 across the full frame width (measured y308..310)
slide.addShape(ST.line, { x: px(573), y: px(309), w: px(810 - 573), h: 0, line: { color: "C00000", width: 1 } });
// gray 1pt x-axis at y=266 (measured AEB0AD/9A9C99 family across the interior)
slide.addShape(ST.line, { x: px(GP.x0), y: px(266), w: px(GP.x1 - GP.x0), h: 0, line: { color: "808080", width: 1 } });

// black axes — the y-axis at data x=0 and the gray x-axis at data y=0 both run the FULL
// frame span y67..310 (measured: dark cols x631..632 persist y267..307, red x687..689 too)
slide.addShape(ST.line, { x: px(630), y: px(67), w: 0, h: px(310 - 67), line: { color: "000000", width: 1 } });

// NO tick marks and NO x-axis tick labels below the plot: a census of every non-panel,
// non-white pixel in y266..299 x548..835 (measure_probe3 section U) found only the
// y-axis / red-x=5 / plot-edge clusters — no glyph ink exists there in the frame.

// red vertical line at data x=5 — same span as the axes, y67..310
slide.addShape(ST.line, { x: px(687.5), y: px(67), w: 0, h: px(310 - 67), line: { color: "FF0000", width: 1 } });

// black 2pt horizontal CHORD at data y=10 (frame y=146) spanning the FULL plot interior
// x576..806 — measured: y146 cluster x576..805, core 0A0000. The inherited stub
// (x651..725) under-drew it by 149px.
slide.addShape(ST.line, { x: px(576), y: px(146), w: px(806 - 576), h: 0, line: { color: "000000", width: 2 } });

// markers — GREEN dot (5,1) centre (688,255) 9x9 ; RED dot centre (660.5,182.5) 7x7
slide.addShape(ST.ellipse, { x: px(683.5), y: px(250.5), w: px(9), h: px(9), fill: { color: "008000" }, line: { color: "008000", width: 1 } });
slide.addShape(ST.ellipse, { x: px(657), y: px(179), w: px(7), h: px(7), fill: { color: "FF0000" }, line: { color: "FF0000", width: 1 } });

// --------------------------------------------------- EQUATION CALLOUTS
// box 1: equation, red border, white fill
slide.addShape(ST.rect, { x: px(398), y: px(184), w: px(132), h: px(28), fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 } });
const eq = require("./assets/eq_032_main.json");
const eqX = px(398 + (132 - eq.w_in * 72) / 2);
const eqY = px(184 + (28 - eq.h_in * 72) / 2);
slide.addImage({ path: ASSET_DIR + "/eq_032_main.png", x: eqX, y: eqY, w: eq.w_in, h: eq.h_in });

// "X = 5" bold red
slide.addText("X = 5", { x: px(398), y: px(217), w: px(120), h: px(24), align: "left", valign: "middle", fontSize: 20, bold: true, color: "C00000", fontFace: A, margin: 0, lineSpacing: 22 });

// box 2: EFFFE2 fill with a GREEN 1pt border TOP (y234) and BOTTOM (y279)
// (measured green runs x370..540 on both rows; the inherited "no border" was wrong)
slide.addShape(ST.rect, {
  x: px(370), y: px(232), w: px(540 - 370), h: px(281 - 232),
  fill: { color: "EFFFE2" }, line: { color: "40842F", width: 1 },
});
slide.addText([
  { text: "f(x) ", options: { fontSize: 13, color: "000000", fontFace: A } },
  { text: "Minimum value is ", options: { fontSize: 13, color: "800080", fontFace: A } },
  { text: "1.0", options: { fontSize: 13, bold: true, color: "0000FF", fontFace: A } },
], { x: px(374), y: px(248), w: px(160), h: px(22), align: "left", valign: "middle", margin: 0, lineSpacing: 15 });

// box 3: F7C9FA LOW BAND across the corridor, x ~330..600, y ~291..320 (measured
// F7C9FA-family ink x331..599 on every row y291..320 — not a small furnished box)
slide.addShape(ST.rect, { x: px(330), y: px(291), w: px(600 - 330), h: px(320 - 291), fill: { color: "F7C9FA" }, line: { type: "none" } });
slide.addText("Reach Minimum after 6 Steps", { x: px(344), y: px(296), w: px(230), h: px(18), align: "left", valign: "middle", fontSize: 13, bold: true, color: "800080", fontFace: A, margin: 0, lineSpacing: 15 });

// ------------------------------------------------------------- LOSS CURVE
// f(x) = (x-5)^2 + 1 — ONE smooth analytic quadratic, blue 0000FF, 2pt (deck convention,
// siblings 030/031). Rasterized at 600 dpi by build/render_curve_032.py so the PNG's own
// pixels carry the analytic shape; the sampler's second-difference ripple is ~1.4e-05
// frame px. Visible span = the part inside the plot box. The image's origin maps to
// frame (cv.frame_x0, cv.frame_y0) offset by the rasterizer's 2*PXW pad.
const cv = require("./assets/curve_032.json");
const cvPadFramePx = (2 * 2) / (cv.dpi / 72); // rasterizer PXW=2, in frame px
slide.addImage({
  path: ASSET_DIR + "/curve_032.png",
  x: px(cv.frame_x0 - cvPadFramePx),
  y: px(cv.frame_y0 - cvPadFramePx),
  w: cv.x_in,
  h: cv.y_in,
});

// ------------------------------------------------------------ ARROW
// CRIMSON 2-stroke arrow at x349..372, y317..355 (measured component n=263, cores
// 852735 / 842634). Solid ~3px wedge cap at y318..320 splitting into two ~3px strokes
// that angle right-down. A whole-frame C000C0 census found no dense magenta object.
const AC = "852735";
slide.addShape(ST.line, { x: px(352), y: px(319), w: px(360 - 352), h: 0, line: { color: AC, width: 3 } });
slide.addShape(ST.line, { x: px(352), y: px(320), w: px(359 - 352), h: px(352 - 320), line: { color: AC, width: 3 } });
slide.addShape(ST.line, { x: px(360), y: px(320), w: px(371 - 360), h: px(352 - 320), line: { color: AC, width: 3 } });

// --------------------------------------------------- ITERATION TABLE
// Measured structure: ONE outer frame (x 298..600, y 330..527, border 564BA7 1pt) holding
// FIVE full-width colour bands separated by white gaps.  Bands, in order, hold
// 2 + 2 + 2 + 1 + 1 = 8 data rows.  Each band carries its own internal row rule.
const rowLabels = ["x", "f(x)", "x-delta", "f(x-delta)", "x+delta", "f(x+delta)", "slope", "next x"];
const rowData = [
  ["3", "3.4", "3.8", "4.2", "4.6", "5"],
  ["5", "3.56", "2.44", "1.64", "1.16", "1"],
  ["2.9", "3.3", "3.7", "4.1", "4.5", "4.9"],
  ["5.41", "3.89", "2.69", "1.81", "1.25", "1.01"],
  ["3.1", "3.5", "3.9", "4.3", "4.7", "5.1"],
  ["4.61", "3.25", "2.21", "1.49", "1.09", "1.01"],
  ["-8", "-6.4", "-4.8", "-3.2", "-1.6", "0"],
  ["3.4", "3.8", "4.2", "4.6", "5", "stop"],
];

// band: { y0, y1 (frame px), fill, border, textColour, splitY (null = single row) }
const BANDS = [
  { y0: 344, y1: 383, fill: "D9E277", border: "9B9B7F", text: "767300", splitY: 363.5, rows: 2 },
  { y0: 387, y1: 424, fill: "D6B3F7", border: "A78CC2", text: "4B0082", splitY: 406,   rows: 2 },
  { y0: 431, y1: 468, fill: "F7DEC0", border: "C9B197", text: "8B5A2B", splitY: 450,   rows: 2 },
  { y0: 472, y1: 494, fill: "E8FFD5", border: "40842F", text: "1E3010", splitY: null,  rows: 1 },
  { y0: 497, y1: 517, fill: "F9BEC0", border: "AA000B", text: "7A1414", splitY: null,  rows: 1 },
];
const TBX = [298.5, 354.5, 395.5, 436.5, 477.5, 518, 558.5, 599.5];
const TBORDER = "564BA7";
const TF = 9;            // data text pt
const TL = 9;            // label text pt

// build the 8 row boxes from the bands
const rowBoxes = [];
BANDS.forEach((bd) => {
  if (bd.splitY === null) {
    rowBoxes.push({ y0: bd.y0, y1: bd.y1, fill: bd.fill, border: bd.border, text: bd.text, bold: false });
  } else {
    rowBoxes.push({ y0: bd.y0, y1: bd.splitY, fill: bd.fill, border: bd.border, text: bd.text, bold: false });
    rowBoxes.push({ y0: bd.splitY, y1: bd.y1, fill: bd.fill, border: bd.border, text: bd.text, bold: false });
  }
});

// outer table frame — four sides only, no fill
[330, 527].forEach((y) => {
  slide.addShape(ST.line, { x: px(298), y: px(y), w: px(600 - 298), h: 0, line: { color: TBORDER, width: 1 } });
});
[298.5, 599.5].forEach((x) => {
  slide.addShape(ST.line, { x: px(x), y: px(330), w: 0, h: px(527 - 330), line: { color: TBORDER, width: 1 } });
});

// band fills + borders + internal row rules + vertical column rules
BANDS.forEach((bd) => {
  slide.addShape(ST.rect, { x: px(298.5), y: px(bd.y0), w: px(599.5 - 298.5), h: px(bd.y1 - bd.y0), fill: { color: bd.fill }, line: { type: "none" } });
  const bw = { color: bd.border, width: 1 };
  slide.addShape(ST.line, { x: px(298.5), y: px(bd.y0), w: px(599.5 - 298.5), h: 0, line: bw });
  slide.addShape(ST.line, { x: px(298.5), y: px(bd.y1), w: px(599.5 - 298.5), h: 0, line: bw });
  [298.5, 599.5].forEach((x) => {
    slide.addShape(ST.line, { x: px(x), y: px(bd.y0), w: 0, h: px(bd.y1 - bd.y0), line: bw });
  });
  if (bd.splitY !== null) {
    slide.addShape(ST.line, { x: px(298.5), y: px(bd.splitY), w: px(599.5 - 298.5), h: 0, line: bw });
  }
  // vertical column rules INSIDE the band only (the frame's white gaps stay white)
  for (let c = 1; c <= 6; c++) {
    slide.addShape(ST.line, { x: px(TBX[c]), y: px(bd.y0), w: 0, h: px(bd.y1 - bd.y0), line: { color: bd.border, width: 0.5 } });
  }
});

// cell text — measured row box centres: 354 / 373.5 / 396.5 / 415 / 440.5 / 459 / 483 / 507
rowBoxes.forEach((rb, r) => {
  for (let c = 0; c < 7; c++) {
    const x0 = TBX[c], x1 = TBX[c + 1];
    const isLabel = c === 0;
    const txt = isLabel ? rowLabels[r] : rowData[r][c - 1];
    slide.addText(txt, {
      x: px(x0), y: px(rb.y0), w: px(x1 - x0), h: px(rb.y1 - rb.y0),
      align: isLabel ? "left" : "center", valign: "middle",
      fontSize: isLabel ? TL : TF, bold: isLabel, color: rb.text,
      fontFace: A, margin: 0, lineSpacing: 11,
    });
  }
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
