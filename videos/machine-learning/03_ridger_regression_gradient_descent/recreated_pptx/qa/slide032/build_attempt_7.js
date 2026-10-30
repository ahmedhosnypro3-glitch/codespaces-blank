// Build: slide 032 — "Convex Function, Learning Rate =0.4, Start at X=3"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GEOMETRY SOURCE: fresh PIL re-measurement of unique_slides/slide_032.jpg
// (960x540, 1px=1pt) banked in qa/slide032/measure_v2_032.txt (2026-10-24,
// worker w032). Where the spec and the frame disagree, THE FRAME WINS.
//
// KEY FRAME FACTS (re-measured; supersedes measure_probe*):
//   * TYPEFACE IS SERIF (Times family) on every text element — the title runs,
//     param table, callouts and iteration table are serif; the earlier Arial
//     assumption came from the analysis record's typography note, not the frame.
//   * TITLE is ONE line: red "Convex Function," x82..239, green
//     "Learning Rate =0.4," x258..435, blue "Start at X=3" x446..557, ink y66..88.
//     Liberation/Times Serif Bold 21pt reproduces the three run widths to <1px.
//   * PARAM TABLE x81..206 y179..250 with an internal vertical divider at
//     x153.5; three rows y179..202.5 / 202.5..226 / 226..250.
//   * GRAPH (x573..810, y66..309): white interior to y307; gray axes (not
//     black) at x631 / y266; gridlines every 1 unit both ways; labels that the
//     earlier probe MISSED: y ticks 5/10/15, x ticks -5/0/5/10/15, point labels
//     "(2, 10)" "(7, 7)" "(5, 1)", two segment "3" labels, three black dots on
//     the chord, a DASHED red x=5 line (not solid), and a chord that spans
//     x652..727 (NOT the full plot width).
//   * CALLOUTS: one GREEN box x333..538 y234..280 holds BOTH "X = 5" (red,
//     16pt) and "f(x) Minimum value is 1.0" (18.5pt; "f(x)" blue italic,
//     "1.0" blue bold). The pink band is x335..570 y292..320 with 16pt bold
//     italic 800080 text. The arrow is a white-filled crimson-outlined
//     down-arrow at x349..377 y317..354, drawn OVER the table.
//   * ITERATION TABLE x298..600 y330..527: labels are RIGHT-aligned in the
//     label column (x299..355); serif bold labels ~10.5pt, serif numbers ~9.5pt.
//
// House chrome (deck standard shared_patterns/house_chrome.js):
//   canvas FFFFFF; gray panel E9E9E7 x54..903 y45..540 (no border);
//   C00000 1pt strokes LEFT x58.5 (rows46..539), RIGHT x901, BOTTOM y538.5;
//   NO TOP STROKE; badge circle d~35 centred (876,73), fill FDFD96,
//   ring 6A5ACD 2pt, bold "32" Arial 18pt #333333.
//
// Laws honored: hex without '#'; fontFace explicit everywhere; margin 0;
// measured geometry over intuition; explicit lineSpacing on every multi-line box;
// single plain-named deliverable.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = __dirname + "/../slide_032_recreated.pptx";
const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();
const ST = pptx.ShapeType;
const A = "Times New Roman"; // frame typeface is a serif (Times family)

drawHouseChrome(pptx, slide, { numeral: 32 });

// ------------------------------------------------------------------ TITLE
// ONE line, ink x81..557, y66..88. Run widths measured 158 / 177 / 111 px;
// Times/Liberation Serif Bold 21pt gives 158.7 / 178.8 / 111.1.
slide.addText(
  [
    { text: "Convex Function,  ", options: { fontSize: 21, bold: true, color: "C00000", fontFace: A } },
    { text: "Learning Rate =0.4, ", options: { fontSize: 21, bold: true, color: "008000", fontFace: A } },
    { text: "Start at X=3", options: { fontSize: 21, bold: true, color: "0000FF", fontFace: A } },
  ],
  { x: px(80), y: px(62), w: px(520), h: px(30), margin: 0, align: "left", valign: "top" }
);

// ------------------------------------------------------- PARAMETER TABLE
// x81..206, y179..250, vertical divider x153.5, three rows.
const paramRows = [
  { label: "step", value: "0.4", fill: "E9FFD5" },
  { label: "initial X", value: "3", fill: "F3BEC2" },
  { label: "delta", value: "0.1", fill: "FAFF0D" },
];
const PT = { x0: 81, x1: 206, div: 153.5, y0: 179, y1: 250, rows: [179, 202.5, 226, 250] };
paramRows.forEach((row, i) => {
  const y = px(PT.rows[i]);
  const h = px(PT.rows[i + 1] - PT.rows[i]);
  slide.addShape(ST.rect, {
    x: px(PT.x0), y, w: px(PT.x1 - PT.x0), h,
    fill: { color: row.fill }, line: { color: "595959", width: 1 },
  });
  slide.addText(row.label, {
    x: px(PT.x0 + 1), y, w: px(PT.div - PT.x0 - 1), h,
    align: "center", valign: "middle", fontSize: 14, bold: true,
    color: "000000", fontFace: A, margin: 0,
  });
  slide.addText(row.value, {
    x: px(PT.div), y, w: px(PT.x1 - PT.div), h,
    align: "center", valign: "middle", fontSize: 14,
    color: "000000", fontFace: A, margin: 0,
  });
});
// internal vertical divider through all three rows
slide.addShape(ST.line, {
  x: px(PT.div), y: px(PT.y0), w: 0, h: px(PT.y1 - PT.y0),
  line: { color: "595959", width: 1 },
});

// ----------------------------------------------------------------- GRAPH
// White interior x574..809, y67..307; red frame x573 / x810 / y66 / y309;
// gray axes x631 (y67..309) and y266; calibration x=630.5+11.5*data,
// y=266-12*data (measured gridline census).
const GP = { x0: 574, x1: 809, y0: 67, y1: 307 };
const XC = 630.5, SX = 11.5;
const YC = 266, SY = 12;
const mx = (v) => XC + SX * v;
const my = (v) => YC - SY * v;
const GRAY_AXIS = "969696";
const LABEL_GRAY = "666666";

// white plot background
slide.addShape(ST.rect, {
  x: px(GP.x0), y: px(GP.y0), w: px(GP.x1 - GP.x0), h: px(GP.y1 - GP.y0),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});

// gridlines every 1 data unit, vertical and horizontal (measured x585..803,
// y75..302); 0.5pt light gray
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

// red frame: left x573, right x810, top y66, bottom red band y309
slide.addShape(ST.line, { x: px(573), y: px(66), w: 0, h: px(309 - 66), line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(810), y: px(66), w: 0, h: px(309 - 66), line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(573), y: px(66), w: px(810 - 573), h: 0, line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(573), y: px(309), w: px(810 - 573), h: 0, line: { color: "C00000", width: 1 } });

// gray axes (measured cores ~#969696, NOT black): y-axis x631, x-axis y266
slide.addShape(ST.line, { x: px(631), y: px(GP.y0), w: 0, h: px(309 - GP.y0), line: { color: GRAY_AXIS, width: 1 } });
slide.addShape(ST.line, { x: px(GP.x0), y: px(266), w: px(GP.x1 - GP.x0), h: 0, line: { color: GRAY_AXIS, width: 1 } });

// DASHED dark-red vertical at data x=5 (measured dash pattern; the earlier
// build drew it solid)
slide.addShape(ST.line, {
  x: px(mx(5)), y: px(GP.y0), w: 0, h: px(309 - GP.y0),
  line: { color: "C00000", width: 1, dashType: "dash" },
});

// black 2pt chord at data y=10 spanning x652..727 (between the two end dots)
slide.addShape(ST.line, { x: px(652), y: px(146), w: px(727 - 652), h: 0, line: { color: "000000", width: 2 } });

// black dots on the chord ends and at the red-line crossing (measured centres)
[[653.5, 146], [687.5, 146], [722.5, 146]].forEach(([cx, cy]) => {
  slide.addShape(ST.ellipse, {
    x: px(cx - 3.5), y: px(cy - 3.5), w: px(7), h: px(7),
    fill: { color: "000000" }, line: { color: "000000", width: 0.5 },
  });
});

// ------------------------------------------------------------ THE LOSS CURVE
// f(x) = (x-5)^2 + 1 — one smooth analytic quadratic rasterized at 600 dpi by
// build/render_curve_032.py; steel-blue (measured frame core family ~#7D9AAA,
// NOT the vivid #0000FF of the analysis note). Visible span inside the plot.
const cv = require("./assets/curve_032.json");
const cvPadFramePx = (2 * 2) / (cv.dpi / 72);
slide.addImage({
  path: ASSET_DIR + "/curve_032.png",
  x: px(cv.frame_x0 - cvPadFramePx),
  y: px(cv.frame_y0 - cvPadFramePx),
  w: cv.x_in,
  h: cv.y_in,
});

// markers — GREEN dot centre (687.5,255) 9x9 ; RED dot centre (660.5,182.5) 7x7
slide.addShape(ST.ellipse, { x: px(683), y: px(250.5), w: px(9), h: px(9), fill: { color: "008000" }, line: { color: "008000", width: 1 } });
slide.addShape(ST.ellipse, { x: px(657), y: px(179), w: px(7), h: px(7), fill: { color: "FF0000" }, line: { color: "FF0000", width: 1 } });

// graph labels (measured bboxes; medium gray, 9-10pt serif)
const gLabel = (text, x, y, w, h, align) =>
  slide.addText(text, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align, valign: "middle", fontSize: text.length > 2 ? 10 : 9,
    color: LABEL_GRAY, fontFace: A, margin: 0,
  });
// y-axis ticks (right-aligned, ending 2px left of the axis at x630)
gLabel("15", 606, 79, 22, 14, "right");
gLabel("10", 606, 139, 22, 14, "right");
gLabel("5", 606, 199, 22, 14, "right");
// x-axis ticks (centres measured on the frame; label colour gray)
gLabel("-5", 568, 266, 24, 13, "center");
gLabel("0", 618, 266, 24, 13, "center");
gLabel("5", 676, 266, 24, 13, "center");
gLabel("10", 733.5, 266, 24, 13, "center");
gLabel("15", 790.5, 266, 24, 13, "center");
// point labels
gLabel("(2, 10)", 619, 149, 40, 14, "left");
gLabel("(7, 7)", 724, 140, 30, 13, "left");
gLabel("(5, 1)", 694, 246, 36, 14, "left");
// segment length labels above the chord (measured gray-blue family)
slide.addText("3", { x: px(664), y: px(124), w: px(15), h: px(13), align: "center", valign: "middle", fontSize: 9, color: "99AABA", fontFace: A, margin: 0 });
slide.addText("3", { x: px(697), y: px(124), w: px(15), h: px(13), align: "center", valign: "middle", fontSize: 9, color: "99AABA", fontFace: A, margin: 0 });

// --------------------------------------------------- EQUATION CALLOUTS
// box 1: equation, red border, white fill (measured x398..530 y184..212)
slide.addShape(ST.rect, { x: px(398), y: px(184), w: px(132), h: px(28), fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 } });
const eq = require("./assets/eq_032_main.json");
const eqX = px(398 + (132 - eq.w_in * 72) / 2);
const eqY = px(184 + (28 - eq.h_in * 72) / 2);
slide.addImage({ path: ASSET_DIR + "/eq_032_main.png", x: eqX, y: eqY, w: eq.w_in, h: eq.h_in });

// box 2: GREEN box x333..538 y234..280 holding BOTH callout lines (measured)
slide.addShape(ST.rect, {
  x: px(333), y: px(234), w: px(538 - 333), h: px(280 - 234),
  fill: { color: "EFFFE2" }, line: { color: "438A3C", width: 1 },
});
// line 1: "X = 5" — X bold italic, "= 5" bold upright, red (16pt)
slide.addText(
  [
    { text: "X", options: { fontSize: 16, bold: true, italic: true, color: "C00000", fontFace: A } },
    { text: " = 5", options: { fontSize: 16, bold: true, color: "C00000", fontFace: A } },
  ],
  { x: px(339), y: px(236), w: px(120), h: px(16), align: "left", valign: "middle", margin: 0 }
);
// line 2: "f(x) Minimum value is 1.0" (18.5pt; blue italic f(x), blue bold 1.0)
slide.addText(
  [
    { text: "f(x)", options: { fontSize: 18.5, italic: true, color: "0000FF", fontFace: A } },
    { text: " Minimum value is ", options: { fontSize: 18.5, color: "000000", fontFace: A } },
    { text: "1.0", options: { fontSize: 18.5, bold: true, color: "0000FF", fontFace: A } },
  ],
  { x: px(337), y: px(253), w: px(200), h: px(18), align: "left", valign: "middle", margin: 0 }
);

// box 3: pink LOW BAND x335..570 y292..320 (measured; extends under the plot)
slide.addShape(ST.rect, {
  x: px(335), y: px(292), w: px(570 - 335), h: px(320 - 292),
  fill: { color: "F7C9FB" }, line: { color: "CBA6D1", width: 0.75 },
});
slide.addText("Reach Minimum after 6  Steps", {
  x: px(342), y: px(295), w: px(230), h: px(22),
  align: "left", valign: "middle", fontSize: 16, bold: true, italic: true,
  color: "800080", fontFace: A, margin: 0,
});

// --------------------------------------------------- ITERATION TABLE
// One outer frame (x298..600, y330..527, border 564BA7 1pt) holding FIVE
// full-width colour bands separated by white gaps; 2+2+2+1+1 = 8 data rows.
// Labels are RIGHT-aligned in the x299..355 label column (measured).
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
const BANDS = [
  { y0: 344, y1: 383, fill: "D8E175", border: "9B9B7F", text: "767300", splitY: 363.5, rows: 2 },
  { y0: 387, y1: 424, fill: "D4B2F5", border: "A78CC2", text: "4B0082", splitY: 406, rows: 2 },
  { y0: 431, y1: 468, fill: "F6DDC1", border: "C9B197", text: "8B5A2B", splitY: 450, rows: 2 },
  { y0: 472, y1: 494, fill: "E7FFD2", border: "40842F", text: "1E3010", splitY: null, rows: 1 },
  { y0: 497, y1: 517, fill: "F4BEC2", border: "AA000B", text: "7A1414", splitY: null, rows: 1 },
];
const TBX = [298.5, 355, 395.5, 436.5, 477.5, 518, 559, 599.5];
const TBORDER = "564BA7";
const TF = 9.5;   // data numbers
const TL = 10.5;  // row labels (bold)

const rowBoxes = [];
BANDS.forEach((bd) => {
  if (bd.splitY === null) {
    rowBoxes.push({ y0: bd.y0, y1: bd.y1, fill: bd.fill, border: bd.border, text: bd.text });
  } else {
    rowBoxes.push({ y0: bd.y0, y1: bd.splitY, fill: bd.fill, border: bd.border, text: bd.text });
    rowBoxes.push({ y0: bd.splitY, y1: bd.y1, fill: bd.fill, border: bd.border, text: bd.text });
  }
});

// outer table frame — four sides only, no fill
[330, 527].forEach((y) => {
  slide.addShape(ST.line, { x: px(298), y: px(y), w: px(600 - 298), h: 0, line: { color: TBORDER, width: 1 } });
});
[298.5, 599.5].forEach((x) => {
  slide.addShape(ST.line, { x: px(x), y: px(330), w: 0, h: px(527 - 330), line: { color: TBORDER, width: 1 } });
});

// band fills + borders + internal row rules + column rules
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
  for (let c = 1; c <= 6; c++) {
    slide.addShape(ST.line, { x: px(TBX[c]), y: px(bd.y0), w: 0, h: px(bd.y1 - bd.y0), line: { color: bd.border, width: 0.5 } });
  }
});

// cell text — labels RIGHT-aligned in the label column, numbers centred
rowBoxes.forEach((rb, r) => {
  for (let c = 0; c < 7; c++) {
    const x0 = TBX[c], x1 = TBX[c + 1];
    const isLabel = c === 0;
    const txt = isLabel ? rowLabels[r] : rowData[r][c - 1];
    slide.addText(txt, {
      x: px(x0), y: px(rb.y0), w: px(x1 - x0), h: px(rb.y1 - rb.y0),
      align: isLabel ? "right" : "center", valign: "middle",
      fontSize: isLabel ? TL : TF, bold: isLabel, color: rb.text,
      fontFace: A, margin: isLabel ? 1 : 0, lineSpacing: 12,
    });
  }
});

// ------------------------------------------------------------------ ARROW
// White-filled crimson-outlined down-arrow x349..377 y317..354, rotated
// ~25 degrees, drawn AFTER the table so it overlays the top band like the
// frame's hand-drawn arrow does.
slide.addShape(ST.downArrow, {
  x: px(350), y: px(317), w: px(16), h: px(37),
  fill: { color: "FFFFFF" }, line: { color: "8B1A2B", width: 1.5 },
  rotate: 25,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
