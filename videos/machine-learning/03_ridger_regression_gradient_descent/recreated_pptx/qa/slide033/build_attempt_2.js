// Build: slide 033 — "Non-Convex Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_033.jpg (960x540, 1px=1pt=1/72in)
//
// =====================================================================
// MEASURED GEOMETRY (frame px; PIL analysis of unique_slides/slide_033.jpg)
// The FRAME WINS over analysis/slide_033_final.json wherever they differ.
// =====================================================================
//
// HOUSE CHROME (from shared_patterns/house_chrome.js):
//   canvas FFFFFF | panel E9E9E7 x54..903 y45..540 | C00000 1pt strokes
//   LEFT x58.5, RIGHT x901, BOTTOM y538.5 (NO top stroke) |
//   badge circle d~35 center (876,73) fill FDFD96 ring 6A5ACD,
//   bold Arial 18pt numeral 333333 = "33".
//
// TITLE  "Non-Convex Function"
//   ink rows 66-94; glyph groups span cols ~190-440 => text box x190 y58.
//   red #FF0000, bold, ~28pt Arial.
//
// SUBTITLE L1  "May reach different minimum value based on:"
//   ink rows 94-113, cols ~117-500. blue #0000FF bold ~16pt. box x115 y92.
//
// SUBTITLE L2  "initial point and learning rate"
//   ink rows 118-144, cols ~300-790 ("initial point" red ~305-417,
//   "learning rate" blue ~426-459 + orange marks ~620-790 which are the
//   plot's red initial-point marker bleeding right). box x300 y114, 18pt bold.
//
// PARAMETER BOX  x 75-175, y 245-309 (w100 h64)
//   fill violet (167,160,227) ~ #A7A0E3; thin dark border.
//   yellow #FFFF00 accent bar across the TOP of the box (rows ~246-258).
//   3 label/value rows, ~10pt dark text, rows:
//     A y257-270 "step  0.1"
//     B y274-291 "initial x  -11"     (yellow bar sits behind this row)
//     C y292-307 "delta x   0.1"
//
// CENTER CALLOUT  x 244-599, y 252-301 (w355 h49)
//   fill pale green (239,255,226) ~ #EFFFE2, thin dark border.
//   - EQUATION  f(x) = (x^2 cos(x) - x)/10 as a stacked fraction,
//     ink rows 254-271, cols 246-596 => mathtext PNG (eq_033_main.png).
//   - ANNOTATION 1 "X is in between -9.7 and -9.6" ink rows 281-292
//   - ANNOTATION 2 "f(x) is in between -8.08 and -8.011" ink rows 287-299
//     ("-9.6" red bold; both lines ~11pt green #008000 dark).
//
// PLOT  white region right of the callout, x 600-930, rows 58-320.
//   - x-axis: horizontal dark band rows 312-313 and 320-321 (two 2px rules)
//     spanning cols 606-901 -> draw as 1pt lines at rows 312 and 320.
//   - y-axis: vertical dark cols 607 (rows 61-317) and 721 (rows 67-317)
//   - no gridlines (grey D9D9D9 was NOT detected in this frame)
//   - CURVE: non-convex oscillating f(x), traced from saturated ink:
//       (624,143)->(644,116)->(668,130)->(692,178)->FLAT y~171 x696-748
//       ->(780,139)->(772,151) hump ->(808,262) -> decays.
//     colour green #00B050.
//   - red/orange markers in rows 110-295 cols 616-840 (initial point,
//     "Reach Local Minima" callout, tick labels) — drawn as: red dot at the
//     curve start (624,143), purple callout near (640,265),
//     and the tick labels along the axis.
//
// TABLE  x 86-870, y 320-519.
//   top border rule rows 320-322 (cols 90-868); bottom border rows 517-519.
//   LABEL COLUMN: x 86-121 (35px wide), no fill (panel).
//   16 DATA COLUMNS: pitch 40px, boundaries at
//     121,161,201,241,281,321,361,401,441,481,521,561,601,641,681,721,761,801,841,861
//     (the fitted 121+k*40 grid matches every text row's token centroids).
//   5 ROW BANDS (fills measured):
//     band0 y332-368  fill #D9E275 (217,226,119)  — green-yellow
//     band1 y376-410  fill #D6B2F5 (214,178,248)  — violet
//     band2 y420-455  fill #F7DDC2 (247,221,194)  — peach
//     band3 y458-479  fill #DEAC95 (222,172,149)  — muted orange
//     band4 y482-504  fill #F7BEC4 (247,190,196)  — pink
//   SPECIAL CELLS:
//     - cyan #8BF8A9 insert spanning band0 cols 666-789 (139,248,169)
//     - yellow highlight cols ~715-820 within band3
//     - RED BOLD TEXT rows 467-505 (cols 149-864) = the min-column highlight
//   TEXT: 8pt dark numerals in bands 0-2; rows 467-505 carry red bold text.
//
// Laws: hex without '#'; fontFace explicit; margin:0; all geometry measured.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_033_recreated.pptx";

const px = (v) => v / 72;
const A = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: "33" });

// ---- TITLE (red, rows 66-94) ----
slide.addText("Non-Convex Function", {
  x: px(185), y: px(58), w: px(270), h: px(36),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 28, bold: true, color: "FF0000",
});

// ---- SUBTITLE L1 (blue, rows 94-113) ----
slide.addText("May reach different minimum value based on:", {
  x: px(115), y: px(92), w: px(390), h: px(24),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 16, bold: true, color: "0000FF",
});

// ---- SUBTITLE L2 (red + blue, rows 118-144) ----
slide.addText([
  { text: "initial point", options: { fontFace: A, fontSize: 18, bold: true, color: "FF0000" } },
  { text: " and ", options: { fontFace: A, fontSize: 18, bold: true, color: "0000FF" } },
  { text: "learning rate", options: { fontFace: A, fontSize: 18, bold: true, color: "0000FF" } },
], {
  x: px(300), y: px(114), w: px(500), h: px(30),
  align: "left", valign: "top", margin: 0,
});

// ---- PARAMETER BOX (x75-175, y245-309) ----
const pb_x = 75, pb_y = 245, pb_w = 100, pb_h = 64;
slide.addShape(pptx.ShapeType.rect, {
  x: px(pb_x), y: px(pb_y), w: px(pb_w), h: px(pb_h),
  fill: { color: "A7A0E3" }, line: { color: "000000", width: 0.5 },
});
// yellow accent bar across the top of the box
slide.addShape(pptx.ShapeType.rect, {
  x: px(pb_x), y: px(pb_y), w: px(pb_w), h: px(13),
  fill: { color: "FFFF00" }, line: { color: "FFFF00", width: 0 },
});
const param_rows = [
  { label: "step", value: "0.1", ry: pb_y + 12 },
  { label: "initial x", value: "-11", ry: pb_y + 30 },
  { label: "delta x", value: "0.1", ry: pb_y + 48 },
];
for (const row of param_rows) {
  slide.addText(row.label, {
    x: px(pb_x + 4), y: px(row.ry), w: px(48), h: px(14),
    align: "left", valign: "middle", margin: 0,
    fontFace: A, fontSize: 10, color: "000000",
  });
  slide.addText(row.value, {
    x: px(pb_x + 52), y: px(row.ry), w: px(44), h: px(14),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 10, color: "000000",
  });
}

// ---- CENTER CALLOUT (x244-599, y252-301, pale green) ----
const cb_x = 244, cb_y = 252, cb_w = 355, cb_h = 49;
slide.addShape(pptx.ShapeType.rect, {
  x: px(cb_x), y: px(cb_y), w: px(cb_w), h: px(cb_h),
  fill: { color: "EFFFE2" }, line: { color: "000000", width: 0.5 },
});
// equation (stacked fraction), ink rows 254-271 -> 18px tall
const eq_w = 1.35, eq_h = 0.21;
slide.addImage({
  path: ASSET_DIR + "/eq_033_main.png",
  x: px(cb_x + cb_w / 2) - eq_w / 2, y: px(cb_y + 1),
  w: eq_w, h: eq_h,
});
slide.addText([
  { text: "X is in between -9.7 and ", options: { fontFace: A, fontSize: 11, color: "006400" } },
  { text: "-9.6", options: { fontFace: A, fontSize: 11, bold: true, color: "FF0000" } },
], {
  x: px(cb_x + 2), y: px(cb_y + 29), w: px(cb_w - 4), h: px(13),
  align: "center", valign: "middle", margin: 0,
});
slide.addText("f(x) is in between -8.08 and -8.011", {
  x: px(cb_x + 2), y: px(cb_y + 38), w: px(cb_w - 4), h: px(12),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 11, color: "006400",
});

// ---- PLOT (right, x600-930, rows 58-320) ----
const PL_X0 = 606, PL_X1 = 901, PL_TOP = 60, PL_AX1 = 312, PL_AX2 = 320;
// two x-axis rules (rows 312 and 320)
slide.addShape(pptx.ShapeType.line, {
  x: px(PL_X0), y: px(PL_AX1), w: px(PL_X1 - PL_X0), h: 0,
  line: { color: "000000", width: 1 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(PL_X0), y: px(PL_AX2), w: px(PL_X1 - PL_X0), h: 0,
  line: { color: "000000", width: 0.75 },
});
// y-axis rules (cols 607 and 721)
slide.addShape(pptx.ShapeType.line, {
  x: px(607), y: px(PL_TOP), w: 0, h: px(PL_AX2 - PL_TOP),
  line: { color: "000000", width: 1 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(721), y: px(67), w: 0, h: px(PL_AX2 - 67),
  line: { color: "000000", width: 0.75 },
});
// axis labels "x" / "y"
slide.addText("x", {
  x: px(PL_X1 - 24), y: px(PL_AX2 + 3), w: px(20), h: px(14),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "000000",
});
slide.addText("y", {
  x: px(583), y: px(PL_TOP - 4), w: px(20), h: px(14),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "000000",
});

// x tick labels (dark, along row ~296-300 under the axis)
const x_ticks = [
  { v: "-12", c: 610 }, { v: "-10", c: 648 }, { v: "-8", c: 687 },
  { v: "-6", c: 726 }, { v: "-4", c: 765 }, { v: "-2", c: 804 },
];
for (const t of x_ticks) {
  slide.addText(t.v, {
    x: px(t.c - 14), y: px(288), w: px(28), h: px(13),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 9, color: "000000",
  });
}
// y tick labels (left of the y-axis)
const y_ticks = ["1", "0", "-2", "-4", "-6", "-8"];
for (let i = 0; i < y_ticks.length; i++) {
  const ty = 138 + i * 34;
  slide.addText(y_ticks[i], {
    x: px(574), y: px(ty), w: px(28), h: px(13),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 9, color: "000000",
  });
}

// CURVE — ONE smooth non-convex curve, traced from the frame's saturated ink.
const curve = [
  [624, 143], [628, 196], [632, 130], [636, 125], [640, 120], [644, 116],
  [648, 183], [652, 155], [656, 137], [660, 128], [664, 127], [668, 130],
  [672, 141], [676, 153], [680, 163], [684, 170], [688, 174], [692, 176],
  [696, 173], [700, 172], [704, 172], [708, 171], [712, 171], [716, 171],
  [720, 171], [724, 171], [728, 171], [732, 171], [736, 172], [740, 174],
  [744, 176], [748, 180], [752, 183], [756, 186], [760, 182], [764, 174],
  [768, 160], [772, 151], [776, 142], [780, 139], [784, 142], [788, 151],
  [792, 171], [796, 198], [800, 227], [804, 252], [808, 262], [812, 248],
  [816, 209], [820, 167], [824, 112],
];
for (let i = 0; i < curve.length - 1; i++) {
  const p1 = curve[i], p2 = curve[i + 1];
  slide.addShape(pptx.ShapeType.line, {
    x: px(p1[0]), y: px(p1[1]), w: px(p2[0] - p1[0]), h: px(p2[1] - p1[1]),
    line: { color: "00B050", width: 1 },
  });
}
// red initial-point dot at the curve start
slide.addShape(pptx.ShapeType.ellipse, {
  x: px(620), y: px(139), w: px(9), h: px(9),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
});
// purple "Reach Local Minima" callout near the curve's minimum region
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(640), y: px(258), w: px(140), h: px(20),
  fill: { color: "7030A0" }, line: { color: "7030A0", width: 0 },
});
slide.addText("Reach Local Minima", {
  x: px(640), y: px(258), w: px(140), h: px(20),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 9, bold: true, color: "FFFFFF",
});

// ---- TABLE (x86-870, y320-519) ----
const tbl_x0 = 86, tbl_x1 = 870, tbl_y0 = 320, tbl_y1 = 519;
// outer frame: top rule rows 320-322, bottom rule rows 517-519
slide.addShape(pptx.ShapeType.rect, {
  x: px(tbl_x0), y: px(tbl_y0), w: px(tbl_x1 - tbl_x0), h: px(tbl_y1 - tbl_y0),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(tbl_x0), y: px(321), w: px(tbl_x1 - tbl_x0), h: 0,
  line: { color: "000000", width: 1 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(tbl_x0), y: px(518), w: px(tbl_x1 - tbl_x0), h: 0,
  line: { color: "000000", width: 1 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(tbl_x0), y: px(tbl_y0), w: 0, h: px(tbl_y1 - tbl_y0),
  line: { color: "000000", width: 0.75 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(tbl_x1), y: px(tbl_y0), w: 0, h: px(tbl_y1 - tbl_y0),
  line: { color: "000000", width: 0.75 },
});

const bands = [
  { y0: 332, y1: 368, fill: "D9E275" },
  { y0: 376, y1: 410, fill: "D6B2F5" },
  { y0: 420, y1: 455, fill: "F7DDC2" },
  { y0: 458, y1: 479, fill: "DEAC95" },
  { y0: 482, y1: 504, fill: "F7BEC4" },
];
for (const bd of bands) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(121), y: px(bd.y0), w: px(870 - 121), h: px(bd.y1 - bd.y0),
    fill: { color: bd.fill }, line: { color: "000000", width: 0 },
  });
}
// cyan insert inside band0, cols 666-789
slide.addShape(pptx.ShapeType.rect, {
  x: px(666), y: px(332), w: px(789 - 666), h: px(368 - 332),
  fill: { color: "8BF8A9" }, line: { color: "000000", width: 0 },
});

// vertical gridlines every 40px from 121 to 861
for (let i = 0; i <= 19; i++) {
  const cx = 121 + i * 40;
  slide.addShape(pptx.ShapeType.line, {
    x: px(cx), y: px(tbl_y0), w: 0, h: px(tbl_y1 - tbl_y0),
    line: { color: "000000", width: 0.25 },
  });
}
// horizontal gridlines between the bands
const hlines = [332, 368, 376, 410, 420, 455, 458, 479, 482, 504];
for (const hy of hlines) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(121), y: px(hy), w: px(870 - 121), h: 0,
    line: { color: "000000", width: 0.25 },
  });
}

// ---- TABLE TEXT ----
// Label column (x86-121) and the first 5 rows' data, from the spec's dataset.
// Row labels measured in the frame's label column at rows 382-386, 398-406,
// 424-430, 442-450, 462-476 => the frame's table has 5 visible label rows.
// The spec lists 8 row labels (x, f(x), x-delta, f(x-delta), x+delta, f(x+delta,
// slope, next x) but the FRAME shows only 5 data bands -> the frame wins:
// 5 bands, 16 data columns each.
const row_data = [
  { label: "x", vals: ["-11", "-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.5"] },
  { label: "f(x)", vals: ["1.15", "-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-8.11", "-8.05"] },
  { label: "x-delta", vals: ["-11.1", "-11", "-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6"] },
  { label: "f(x-delta)", vals: ["2.39", "1.15", "-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-8.11"] },
  { label: "x+delta", vals: ["-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.5", "-9.4"] },
];

for (let ri = 0; ri < bands.length; ri++) {
  const bd = bands[ri];
  const ytop = bd.y0, ybot = bd.y1;
  const ymid = (ytop + ybot) / 2;
  const row = row_data[ri];
  // label
  slide.addText(row.label, {
    x: px(tbl_x0), y: px(ymid - 7), w: px(121 - tbl_x0), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: "000000",
  });
  // data cells
  for (let ci = 0; ci < 16; ci++) {
    const cx = 121 + ci * 40;
    const is_red = (ri === 4 && ci === 14); // red-bold highlight (measured rows 467-505)
    slide.addText(row.vals[ci], {
      x: px(cx), y: px(ymid - 7), w: px(40), h: px(14),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 7,
      bold: is_red, color: is_red ? "FF0000" : "000000",
    });
  }
}

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});