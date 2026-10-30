// Build: slide 033 — "Non-Convex Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_033.jpg (960x540, 1px=1pt=1/72in)
//
// =====================================================================
// MEASURED GEOMETRY (frame px; PIL analysis of unique_slides/slide_033.jpg).
// The FRAME WINS over analysis/slide_033_final.json where they differ.
// =====================================================================
//
// HOUSE CHROME (shared_patterns/house_chrome.js): white canvas; gray E9E9E7
// panel x54..903 y45..540; C00000 1pt strokes LEFT x58.5 / RIGHT x901 /
// BOTTOM y538.5 only (NO top stroke); badge circle d~35 centered (876,73)
// fill FDFD96 ring 6A5ACD, bold Arial 18pt numeral 333333 = "33".
//
// TITLE  "Non-Convex Function" — red #FF0000 bold, ink rows 66-94,
//        cols ~190-440. Box x185 y58, 28pt.
// SUBTITLE L1 "May reach different minimum value based on:" — blue #0000FF
//        bold, ink rows 94-113, cols ~117-500. Box x115 y92, 16pt.
// SUBTITLE L2 "initial point and learning rate" — "initial point" red
//        #FF0000, "learning rate" blue #0000FF, ink rows 118-144, cols
//        ~300-459. Box x300 y114, 18pt bold.
//
// PARAMETER BOX x75-175 y245-309 (w100 h64): fill violet (167,160,227)
//        ~#A7A0E3, thin dark border, yellow #FFFF00 accent bar across the
//        top (rows 246-258). Three rows: step|0.1, initial x|-11, delta x|0.1
//        (~10pt dark, rows 257-270 / 274-291 / 292-307).
//
// CENTER CALLOUT x244-599 y252-301 (w355 h49): fill pale green (239,255,226)
//        ~#EFFFE2, thin dark border. Equation f(x) = (x^2 cos(x)-x)/10 as a
//        stacked fraction (mathtext PNG, ink rows 254-271), then two green
//        annotation lines (rows 281-292 and 287-299): "X is in between -9.7
//        and -9.6" (with -9.6 red bold) and "f(x) is in between -8.08 and
//        -8.011" (verbatim per spec).
//
// PLOT right, x600-930 rows 58-320: white; TWO x-axis rules at rows 312 and
//        320 (cols 606-901); TWO y-axis rules at cols 607 and 721 (rows
//        61/67-320); NO gridlines (D9D9D9 absent in this frame). Green
//        #00B050 non-convex curve traced from the frame's saturated ink
//        (cols 612-832, rows 110-264 — ONE smooth curve). Red dot at the
//        curve start (620,139); purple #7030A0 rounded callout "Reach Local
//        Minima" at x640-780 y258-278. Axis label "x" right of the axis,
//        "y" above it; x ticks -12/-10/-8/-6/-4/-2 at row ~288-301,
//        y ticks 1/0/-2/-4/-6/-8 left of the y-axis.
//
// TABLE x86-869 y320-519 — FRAME MEASURED (verified, see qa/slide033):
//   OUTER BORDER: top rule rows 320-322, bottom rule rows 516-519,
//                 left/right verticals at x86 and x869.
//   LABEL COLUMN  x86-121 (35px).
//   18 DATA COLUMNS, pitch 40px, gridlines at 121 + k*40 (k=0..18), the last
//                 column 841-869 is narrower (28px).
//   HORIZONTAL GRIDLINES (full-width dark rows): 320, 374, 410, 418, 454,
//                 460, 478, 484, 501, 517.
//   5 FILL BANDS (mode colour measured; draw as row bands):
//     y321-374  #D9E275  (217,226,119) yellow-green
//     y374-410  #D6B2F5  (214,178,248) violet
//     y418-454  #F7DDC2  (247,221,194) peach
//     y460-478  #DEAC95  (222,172,149) muted orange
//     y484-501  #F7BEC4  (247,190,196) pink
//   CYAN INSERT  x666-789 y332-368 inside band0 — fill #8BF8A9 (139,248,169)
//   8 TEXT ROWS (centres, matching the spec's 8 row labels):
//      341, 359, 383, 401, 427, 445, 469, 493
//     rows 469 & 493 carry RED BOLD text (the highlighted minimum cells).
//   DATA: the spec's 8 rows x 16 values (analysis/slide_033_final.json
//     recreation_brief), placed in grid columns 0..15 (x121..641). The frame
//     shows ~18 columns; the analysis transcribes 16 values per row
//     (documented deviation — the analysis contract supplies the values).
//
// Laws: hex without '#'; fontFace explicit on every text; margin 0; measured
// geometry throughout; equation via 600dpi mathtext PNG at exact px/600 size.

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

// ================= TITLE / SUBTITLE =================
slide.addText("Non-Convex Function", {
  x: px(185), y: px(58), w: px(270), h: px(36),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 28, bold: true, color: "FF0000",
});
slide.addText("May reach different minimum value based on:", {
  x: px(115), y: px(92), w: px(390), h: px(24),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 16, bold: true, color: "0000FF",
});
slide.addText([
  { text: "initial point", options: { fontFace: A, fontSize: 18, bold: true, color: "FF0000" } },
  { text: " and ", options: { fontFace: A, fontSize: 18, bold: true, color: "0000FF" } },
  { text: "learning rate", options: { fontFace: A, fontSize: 18, bold: true, color: "0000FF" } },
], {
  x: px(300), y: px(114), w: px(500), h: px(30),
  align: "left", valign: "top", margin: 0,
});

// ================= PARAMETER BOX =================
const PB = { x: 75, y: 245, w: 100, h: 64 };
slide.addShape(pptx.ShapeType.rect, {
  x: px(PB.x), y: px(PB.y), w: px(PB.w), h: px(PB.h),
  fill: { color: "A7A0E3" }, line: { color: "000000", width: 0.5 },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(PB.x), y: px(PB.y), w: px(PB.w), h: px(13),
  fill: { color: "FFFF00" }, line: { color: "FFFF00", width: 0 },
});
const param_rows = [
  { label: "step", value: "0.1", ry: PB.y + 12 },
  { label: "initial x", value: "-11", ry: PB.y + 30 },
  { label: "delta x", value: "0.1", ry: PB.y + 48 },
];
for (const row of param_rows) {
  slide.addText(row.label, {
    x: px(PB.x + 4), y: px(row.ry), w: px(48), h: px(14),
    align: "left", valign: "middle", margin: 0,
    fontFace: A, fontSize: 10, color: "000000",
  });
  slide.addText(row.value, {
    x: px(PB.x + 52), y: px(row.ry), w: px(44), h: px(14),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 10, color: "000000",
  });
}

// ================= CENTER CALLOUT (formula + annotations) =================
const CB = { x: 244, y: 252, w: 355, h: 49 };
slide.addShape(pptx.ShapeType.rect, {
  x: px(CB.x), y: px(CB.y), w: px(CB.w), h: px(CB.h),
  fill: { color: "EFFFE2" }, line: { color: "000000", width: 0.5 },
});
// stacked-fraction equation (600dpi mathtext PNG, exact px/600 size)
const eq_w = 1.35, eq_h = 0.21;
slide.addImage({
  path: ASSET_DIR + "/eq_033_main.png",
  x: px(CB.x + CB.w / 2) - eq_w / 2, y: px(CB.y + 1),
  w: eq_w, h: eq_h,
});
slide.addText([
  { text: "X is in between -9.7 and ", options: { fontFace: A, fontSize: 11, color: "006400" } },
  { text: "-9.6", options: { fontFace: A, fontSize: 11, bold: true, color: "FF0000" } },
], {
  x: px(CB.x + 2), y: px(CB.y + 29), w: px(CB.w - 4), h: px(13),
  align: "center", valign: "middle", margin: 0,
});
slide.addText("f(x) is in between -8.08 and -8.011", {
  x: px(CB.x + 2), y: px(CB.y + 38), w: px(CB.w - 4), h: px(12),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 11, color: "006400",
});

// ================= FUNCTION PLOT =================
const PL = { x0: 606, x1: 901, top: 60, ax1: 312, ax2: 320 };
slide.addShape(pptx.ShapeType.line, { // x-axis rule 1
  x: px(PL.x0), y: px(PL.ax1), w: px(PL.x1 - PL.x0), h: 0,
  line: { color: "000000", width: 1 },
});
slide.addShape(pptx.ShapeType.line, { // x-axis rule 2
  x: px(PL.x0), y: px(PL.ax2), w: px(PL.x1 - PL.x0), h: 0,
  line: { color: "000000", width: 0.75 },
});
slide.addShape(pptx.ShapeType.line, { // y-axis rule 1
  x: px(607), y: px(PL.top), w: 0, h: px(PL.ax2 - PL.top),
  line: { color: "000000", width: 1 },
});
slide.addShape(pptx.ShapeType.line, { // y-axis rule 2
  x: px(721), y: px(67), w: 0, h: px(PL.ax2 - 67),
  line: { color: "000000", width: 0.75 },
});
slide.addText("x", {
  x: px(PL.x1 - 24), y: px(PL.ax2 + 3), w: px(20), h: px(14),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "000000",
});
slide.addText("y", {
  x: px(583), y: px(PL.top - 4), w: px(20), h: px(14),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "000000",
});
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
const y_ticks = ["1", "0", "-2", "-4", "-6", "-8"];
for (let i = 0; i < y_ticks.length; i++) {
  slide.addText(y_ticks[i], {
    x: px(574), y: px(138 + i * 34), w: px(28), h: px(13),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 9, color: "000000",
  });
}

// ONE smooth non-convex curve, traced from the frame's saturated ink.
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
slide.addShape(pptx.ShapeType.ellipse, { // red initial point
  x: px(620), y: px(139), w: px(9), h: px(9),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
});
slide.addShape(pptx.ShapeType.roundRect, { // purple callout
  x: px(640), y: px(258), w: px(140), h: px(20),
  fill: { color: "7030A0" }, line: { color: "7030A0", width: 0 },
});
slide.addText("Reach Local Minima", {
  x: px(640), y: px(258), w: px(140), h: px(20),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 9, bold: true, color: "FFFFFF",
});

// ================= TABLE =================
const T = { x0: 86, x1: 869, y0: 320, y1: 519 };
// outer frame
slide.addShape(pptx.ShapeType.rect, {
  x: px(T.x0), y: px(T.y0), w: px(T.x1 - T.x0), h: px(T.y1 - T.y0),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0 },
});
for (const hy of [321, 517]) { // top + bottom border rules
  slide.addShape(pptx.ShapeType.line, {
    x: px(T.x0), y: px(hy), w: px(T.x1 - T.x0), h: 0,
    line: { color: "000000", width: 1 },
  });
}
for (const vx of [T.x0, T.x1]) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(vx), y: px(T.y0), w: 0, h: px(T.y1 - T.y0),
    line: { color: "000000", width: 0.75 },
  });
}
// fill bands
const bands = [
  { y0: 321, y1: 374, fill: "D9E275" },
  { y0: 374, y1: 410, fill: "D6B2F5" },
  { y0: 418, y1: 454, fill: "F7DDC2" },
  { y0: 460, y1: 478, fill: "DEAC95" },
  { y0: 484, y1: 501, fill: "F7BEC4" },
];
for (const bd of bands) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(121), y: px(bd.y0), w: px(869 - 121), h: px(bd.y1 - bd.y0),
    fill: { color: bd.fill }, line: { color: "000000", width: 0 },
  });
}
// cyan insert inside band0
slide.addShape(pptx.ShapeType.rect, {
  x: px(666), y: px(332), w: px(789 - 666), h: px(368 - 332),
  fill: { color: "8BF8A9" }, line: { color: "000000", width: 0 },
});
// gridlines: 20 verticals at 121 + k*40, horizontals at measured rows
for (let i = 0; i <= 18; i++) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(121 + i * 40), y: px(T.y0), w: 0, h: px(T.y1 - T.y0),
    line: { color: "000000", width: 0.25 },
  });
}
for (const hy of [320, 374, 410, 418, 454, 460, 478, 484, 501, 517]) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(121), y: px(hy), w: px(869 - 121), h: 0,
    line: { color: "000000", width: 0.25 },
  });
}

// ---- table content: 8 measured text rows x the analysis dataset ----
const rows = [
  { label: "x", vals: ["-11", "-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.5"] },
  { label: "f(x)", vals: ["1.15", "-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-8.11", "-8.05"] },
  { label: "x-delta", vals: ["-11.1", "-11", "-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6"] },
  { label: "f(x-delta)", vals: ["2.39", "1.15", "-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-8.11"] },
  { label: "x+delta", vals: ["-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.5", "-9.4"] },
  { label: "f(x+delta)", vals: ["-0.04", "-1.19", "-2.26", "-3.27", "-4.19", "-5.03", "-5.77", "-6.41", "-6.95", "-7.39", "-7.72", "-7.96", "-8.08", "-8.11", "-8.05", "-7.89"] },
  { label: "slope", vals: ["-24.3", "-23.4", "-22.2", "-20.8", "-19.3", "-17.6", "-15.8", "-13.8", "-11.8", "-9.8", "-7.7", "-5.7", "-3.6", "-1.5", "0.3", "2.2"] },
  { label: "next x", vals: ["-10.9", "-10.8", "-10.7", "-10.6", "-10.5", "-10.4", "-10.3", "-10.2", "-10.1", "-10", "-9.9", "-9.8", "-9.7", "-9.6", "-9.7", "-9.6"] },
];
const row_ys = [341, 359, 383, 401, 427, 445, 469, 493];
for (let ri = 0; ri < rows.length; ri++) {
  const ymid = row_ys[ri];
  const is_hl = (ri >= 6); // rows 7 & 8 carry the red-bold highlight
  slide.addText(rows[ri].label, {
    x: px(T.x0), y: px(ymid - 7), w: px(121 - T.x0), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: "000000",
  });
  for (let ci = 0; ci < 16; ci++) {
    slide.addText(rows[ri].vals[ci], {
      x: px(121 + ci * 40), y: px(ymid - 7), w: px(40), h: px(14),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 7,
      bold: is_hl, color: is_hl ? "FF0000" : "000000",
    });
  }
}

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});