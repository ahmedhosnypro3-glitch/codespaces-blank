// Build: slide 031 — "Convex Function, Learning Rate =0.3, Start at X=3"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GEOMETRY SOURCE: PIL measurement of unique_slides/slide_031.jpg (960x540, 1px=1pt=1/72in).
// Spec: analysis/slide_031_final.json. Where spec and frame disagree, THE FRAME WINS.
//
// MEASURED LAYOUT (frame px, 960x540):
//   House chrome (deck standard): white FFFFFF canvas; gray E9E9E7 panel x54..903, y45..540;
//   red C00000 1pt strokes LEFT x58.5 (rows 46..539), RIGHT x901 (rows 46..539),
//   BOTTOM y538.5 (cols 58..902); NO TOP STROKE. Badge circle d~35px centered (876,73),
//   fill FDFD96, ring 6A5ACD 2pt, bold numeral 333333 Arial 18pt -> "31".
//
//   Title (top-left, multicolor, Arial bold ~26pt):
//     "Convex Function,"   red C00000
//     "Learning Rate =0.3,"  green 008000
//     "Start at X=3"      blue 0000FF
//     measured y ~ 65-85, x ~ 40-350
//
//   Parameter table (3 rows x 2 cols, below title, x ~ 80-250, y ~ 175-215):
//     Row 1: "step" | "0.3"
//     Row 2: "initial X" | "3"
//     Row 3: "delta" | "0.1"
//     Label cells: yellow FFFFF99 fill, black text
//     Value cells: white FFFFFF fill, black text
//     Grid lines: thin black
//
//   Formula box (top-center, x ~ 330-640, y ~ 185-200):
//     Red FF0000 border, white FFFFFF fill, black text
//     Equation: f(x)=(x-5)^2+1 (rendered as eq asset, 24pt)
//
//   Graph (top-right, x ~ 600-920, y ~ 50-250):
//     Cartesian plot of f(x)=(x-5)^2+1
//     Grid: light gray CCCCCC
//     Axes: black 000000 with tick labels -5, 0, 5, 10, 15 on both x and y
//     Blue parabola 0000FF
//     Green point 008000 at (5,1) labeled "(5,1)"
//     Red point FF0000 at (3,9)
//     Black horizontal segment from (3,9) to (7,9) labeled "(7,9)"
//     Red dashed lines FF0000 at x=5 and y=1
//
//   Annotation box (center below formula, x ~ 180-800, y ~ 245-310):
//     Red FF0000 border, white FFFFFF fill
//     Line 1: "X is in between 4.8 and 5.1" (5.1 in red bold C00000)
//     Line 2: "f(x) is in between 1.04 and 1.01"
//
//   "Bouncing" label + purple arrow (center-right above table, x ~ 340-560, y ~ 310-330):
//     Purple 7030A0 text "Bouncing" with purple arrow pointing down/right
//
//   Red arrow (left side above table, x ~ 160-170, y ~ 324-348):
//     Red FF0000 arrow pointing down/right
//
//   Main table (bottom full width, 8 rows x 17 cols, x ~ 63-893, y ~ 350-530):
//     Row labels (col 0): x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
//     16 data columns per row with exact values from analysis
//     Row background colors: FFFFF99, D9EAD3, CFE2F3, D9D9D9, FCE5CD, 000000 (text)
//     (6 colors for 8 rows - pattern: first 6 rows colored, last 2 dark text)
//
// SPEC-VS-FRAME DEVIATIONS (frame wins, per building.md):
//   1. Spec says 17 columns for main table; frame shows 16 data columns + 1 label col = 17 total.
//      Verified: 1 label col + 16 data cols.
//   2. Spec main_table row count says 8 rows; visual_elements confirms 8 rows.
//      Spec recreation_brief had 9 rows originally - fixed by validation fixes_applied[2].
//   3. "color red bold" in verbatim_text.bullets is a formatting marker, not literal text.
//      The "5.1" in annotation line 1 is rendered red bold.
//   4. Table row-to-color mapping: spec lists 6 colors for 8 rows.
//      Frame evidence: alternating row colors visible. Mapping inferred from frame scan.
//
// Laws honored: hex without '#'; fontFace explicit everywhere; margin 0;
// measured geometry over intuition; closed-loop render check before any judge call.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = __dirname + "/../slide_031_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes, badge "31" ----
drawHouseChrome(pptx, slide, { numeral: 31 });

const A = "Arial";

// ============================================================
// TITLE: ONE line, three coloured segments (frame law)
// MEASURED in unique_slides/slide_031.jpg: the whole title is ONE row at frame
// y 66..83 — red "Convex Function," starts x 81, green "Learning Rate =0.3,"
// starts x 260, blue "Start at X=3" starts x 446 and runs to x ~530. Stacking
// the three segments on separate lines was a MAJOR line-break deviation.
// ============================================================
const titleY = px(66);
const titleX = px(81);
const titleSize = 22;

slide.addText([
  { text: "Convex Function,", options: { color: "C00000" } },
  { text: "  Learning Rate =0.3,", options: { color: "008000" } },
  { text: "  Start at X=3", options: { color: "0000FF" } },
], {
  x: titleX, y: titleY, w: px(560), h: px(24),
  fontSize: titleSize, bold: true, fontFace: A, margin: 0,
  valign: "middle",
});

// ============================================================
// PARAMETER TABLE (3 rows x 2 cols)
// Position: x ~ 80-250, y ~ 175-215
// Cell sizes: label col ~ 80px, value col ~ 80px, row height ~ 12px
// ============================================================
const pTableX = px(80);
const pTableY = px(175);
const pLabelW = px(80);
const pValueW = px(80);
const pRowH = px(13);

const pRows = [
  { label: "step", value: "0.3" },
  { label: "initial X", value: "3" },
  { label: "delta", value: "0.1" },
];

pRows.forEach((row, i) => {
  const y = pTableY + i * pRowH;
  // Label cell (yellow)
  slide.addShape(pptx.ShapeType.rect, {
    x: pTableX, y: y, w: pLabelW, h: pRowH,
    fill: { color: "FFFF99" }, line: { color: "000000", width: 0.5 },
  });
  slide.addText(row.label, {
    x: pTableX, y: y, w: pLabelW, h: pRowH,
    align: "center", valign: "middle", fontSize: 12, bold: false,
    color: "000000", fontFace: A, margin: 0,
  });
  // Value cell (white)
  slide.addShape(pptx.ShapeType.rect, {
    x: pTableX + pLabelW, y: y, w: pValueW, h: pRowH,
    fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.5 },
  });
  slide.addText(row.value, {
    x: pTableX + pLabelW, y: y, w: pValueW, h: pRowH,
    align: "center", valign: "middle", fontSize: 12, bold: false,
    color: "000000", fontFace: A, margin: 0,
  });
});

// ============================================================
// FORMULA BOX (red border, white fill, centered equation)
// Position: x ~ 330-640, y ~ 185-200
// Box: w ~ 310px, h ~ 50px
// ============================================================
const fBoxX = px(330);
const fBoxY = px(185);
const fBoxW = px(310);
const fBoxH = px(50);

slide.addShape(pptx.ShapeType.rect, {
  x: fBoxX, y: fBoxY, w: fBoxW, h: fBoxH,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});

// Equation rendered at 24pt, placed centered in box
// Asset: eq_031_main.png (w=1690px @600dpi = 2.81667in, h=0.38167in)
const eqInfo = require("./assets/eq_031_main.json"); // will read from generated file
// Actually we inline the JSON for now
const eqW = 2.81667;
const eqH = 0.38167;
const eqX = fBoxX + (fBoxW - eqW) / 2;
const eqY = fBoxY + (fBoxH - eqH) / 2;

slide.addImage({
  path: ASSET_DIR + "/eq_031_main.png",
  x: eqX, y: eqY, w: eqW, h: eqH,
});

// ============================================================
// GRAPH (parabola with axes, grid, points, dashed lines)
// MEASURED from unique_slides/slide_031.jpg (007 re-measure, 2026-10-23):
//   plot box x 573..809, y 66..267 (236x201 px) — RED C00000 border, white fill.
//   The plot box's LEFT edge is x573; it never reaches the badge zone
//   (x 858..894, y 56..90), so the badge stays fully visible.
//   Grid lines measured at x 572/630/689/748/807 and y 87/146/206/265
//   (tick labels -5,0,5,10,15 on both axes).
//   OLD geometry (x 640..900, y 70..240) put the white plot rect ON TOP of
//   the badge — the house chrome check caught it (badge center 21 render-px
//   high, lower half covered). See worker_report.md.
// ============================================================
const gX = px(573);
const gY = px(66);
const gW = px(809 - 573); // 236px
const gH = px(267 - 66);  // 201px

// Graph background (white), RED border per the frame
slide.addShape(pptx.ShapeType.rect, {
  x: gX, y: gY, w: gW, h: gH,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
});

// Grid lines (light gray CCCCCC) - both horizontal and vertical
// MEASURED grid (007 re-measure, 2026-10-23, PIL scans of slide_031.jpg):
//   vertical  at frame x 573/630/687/745/801 = data x -5/0/5/10/15 (11.4 px/unit)
//   horizontal at frame y 87/146/206/265     = data y 15/10/5/0    (11.87 px/unit)
// So the y axis runs 0..15 with y=0 ON the box bottom (frame 265) — the old
// yMax=15-with-y0-inside mapping squashed the grid to 10 px/unit, disproved.
const xMin = -5, xMax = 15;
const xTickVals = [-5, 0, 5, 10, 15];
const yTickVals = [0, 5, 10, 15];
const yMin = 0, yMax = 15;
// MEASURED y-origin and scale from the frame's grid lines: y=0 sits at frame y 265
// (box bottom), grid spacing 11.8667 px/unit, so y=15 lands at frame y 87 — INSIDE
// the box, which extends up to frame y 66. The box top is data y ~16.8, not 15,
// so mapping yMax onto the box edge squashed the grid 13% low.
const yZeroY = 265, yPPU = 11.8667;

function mapX(x) { return gX + ((x - xMin) / (xMax - xMin)) * gW; }
function mapY(y) { return (yZeroY - y * yPPU) / 72; }

// Vertical grid lines
xTickVals.forEach(xv => {
  const xPx = mapX(xv);
  slide.addShape(pptx.ShapeType.line, {
    x: xPx, y: gY, w: 0, h: gH,
    line: { color: "CCCCCC", width: 0.5 },
  });
});

// Horizontal grid lines
yTickVals.forEach(yv => {
  const yPx = mapY(yv);
  slide.addShape(pptx.ShapeType.line, {
    x: gX, y: yPx, w: gW, h: 0,
    line: { color: "CCCCCC", width: 0.5 },
  });
});

// Axes (black, slightly thicker)
slide.addShape(pptx.ShapeType.line, { // x-axis (y=0)
  x: gX, y: mapY(0), w: gW, h: 0,
  line: { color: "000000", width: 1.5 },
});
slide.addShape(pptx.ShapeType.line, { // y-axis (x=0)
  x: mapX(0), y: gY, w: 0, h: gH,
  line: { color: "000000", width: 1.5 },
});

// Tick labels (Arial 9pt)
// The x-axis labels sit at frame y 269..283 — INSIDE the annotation box's white
// fill (y 244..289), so they must be emitted AFTER that box or LibreOffice
// paints over them. xTickVals is consumed again below.
yTickVals.forEach(yv => {
  if (yv === 0) return; // skip 0 on y-axis (already at origin)
  slide.addText(String(yv), {
    x: mapX(0) - px(30), y: mapY(yv) - px(9), w: px(28), h: px(12),
    align: "right", valign: "top", fontSize: 9, color: "000000", fontFace: A, margin: 0,
  });
});

// Axis labels "x" and "y"
slide.addText("x", { x: gX + gW - px(15), y: mapY(0) + px(4), w: px(15), h: px(14), fontSize: 10, bold: true, color: "000000", fontFace: A, margin: 0 });
slide.addText("y", { x: mapX(0) - px(15), y: gY - px(12), w: px(15), h: px(14), fontSize: 10, bold: true, color: "000000", fontFace: A, margin: 0 });

// Parabola f(x) = (x-5)^2 + 1 — ONE smooth analytic quadratic, blue 0000FF, 2pt.
// CLIPPED to the plot box: the un-clipped old build drew 5952 blue px OUTSIDE
// the plot (arms ran off to frame y 0 at x 659..832), i.e. ink outside its
// enclosing frame — a MAJOR containment defect.
// Visible span: (x-5)^2+1 <= yMax(15) -> |x-5| <= sqrt(14) -> data x 1.025..8.975.
// Ripple (2nd difference): N=200 -> 3.16e-03 = 0.0375 frame-px (see
// qa/slide031/measurement_notes.md).
const N = 200;
const xVisLo = 5 - Math.sqrt(yMax - 1);
const xVisHi = 5 + Math.sqrt(yMax - 1);
let prevX = null, prevY = null;
for (let i = 0; i <= N; i++) {
  const x = xVisLo + (xVisHi - xVisLo) * i / N;
  const y = Math.pow(x - 5, 2) + 1;
  const px1 = mapX(x);
  const py1 = mapY(y);
  if (prevX !== null) {
    slide.addShape(pptx.ShapeType.line, {
      x: prevX, y: prevY, w: px1 - prevX, h: py1 - prevY,
      line: { color: "0000FF", width: 2 },
    });
  }
  prevX = px1; prevY = py1;
}

// Green point at (5,1) - minimum
const gx5 = mapX(5);
const gy1 = mapY(1);
slide.addShape(pptx.ShapeType.ellipse, {
  x: gx5 - px(4), y: gy1 - px(4), w: px(8), h: px(8),
  fill: { color: "008000" }, line: { color: "008000", width: 1 },
});
// The "(5,1)" LABEL is added AFTER the annotation box (see below) — the box's
// white fill spans x 243..809 y 244..289 and would paint over any label drawn
// before it.

// Black horizontal chord — MEASURED: frame y 143..150, x 650..725.
// That is data y ~10 (frame 146) spanning data x ~1.75..8.33 — NOT (3,9)-(7,9)
// as the spec said (frame wins). The spec's (3,9)/(7,9) endpoints land on
// frame x 664/710 at frame y 158 — neither matches, so the frame reading stands.
// It carries THREE short vertical ticks below it at frame x 653 / 691 / 733
// (data x ~2 / ~5.4 / ~9 — the ends and near the middle).
const gChordY = mapY(10);
const gChordX0 = mapX(1.75);
const gChordX1 = mapX(8.33);
slide.addShape(pptx.ShapeType.line, {
  x: gChordX0, y: gChordY, w: gChordX1 - gChordX0, h: 0,
  line: { color: "000000", width: 1.5 },
});
[653, 691, 733].forEach(tx => {
  slide.addShape(pptx.ShapeType.line, {
    x: tx / 72, y: gChordY, w: 0, h: (150 - 143) / 72,
    line: { color: "000000", width: 1.5 },
  });
});

// Red dot — MEASURED: frame x 657..665, y 179..186 -> data ~(2.7, 6.9).
const gRdX = 661 / 72;
const gRdY = 183 / 72;
slide.addShape(pptx.ShapeType.ellipse, {
  x: gRdX - px(4), y: gRdY - px(4), w: px(8), h: px(8),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 1 },
});

// Red dashed lines at x=5 (vertical) and y=1 (horizontal)
// pptxgenjs doesn't support dashed lines well, use short segments
// Vertical dashed at x=5
for (let yv = yMin; yv <= yMax; yv += 0.5) {
  const y1 = mapY(yv);
  const y2 = mapY(yv + 0.25);
  slide.addShape(pptx.ShapeType.line, {
    x: gx5, y: y1, w: 0, h: y2 - y1,
    line: { color: "FF0000", width: 1 },
  });
}
// Horizontal dashed at y=1
for (let xv = xMin; xv <= xMax; xv += 0.5) {
  const x1 = mapX(xv);
  const x2 = mapX(xv + 0.25);
  slide.addShape(pptx.ShapeType.line, {
    x: x1, y: gy1, w: x2 - x1, h: 0,
    line: { color: "FF0000", width: 1 },
  });
}

// ============================================================
// ANNOTATION BOX (red border, white fill, 2 lines)
// MEASURED from the frame: box spans frame y 244..289 (borders at 244 and 289),
// line 1 text y 249..261, line 2 text y 266..283, x 243..809. The box MUST stop
// above the plot's x-tick labels (frame y 271..285) — the old h=px(65) ran the
// white rect down to y 310 and painted over them.
// ============================================================
const aBoxX = px(243);
const aBoxY = px(244);
const aBoxW = px(809 - 243);
const aBoxH = px(289 - 244);

slide.addShape(pptx.ShapeType.rect, {
  x: aBoxX, y: aBoxY, w: aBoxW, h: aBoxH,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});

// Line 1: "X is in between 4.8 and 5.1" (5.1 in red bold) — MEASURED y 249..261
slide.addText([
  { text: "X is in between 4.8 and ", options: { fontSize: 13, color: "000000", fontFace: A, bold: false } },
  { text: "5.1", options: { fontSize: 13, color: "C00000", fontFace: A, bold: true } },
], {
  x: aBoxX + px(10), y: px(247), w: aBoxW - px(20), h: px(16),
  align: "left", valign: "middle", margin: 0,
});

// Line 2: "f(x) is in between 1.04 and 1.01" — MEASURED y 266..283
slide.addText("f(x) is in between 1.04 and 1.01", {
  x: aBoxX + px(10), y: px(264), w: aBoxW - px(20), h: px(16),
  align: "left", valign: "middle", fontSize: 13, color: "000000", fontFace: A, margin: 0,
});

// "(5,1)" label — MEASURED in the frame at x 497..535, y 249..261: left of the
// plot box, vertically centered on the vertex (frame y 253). MUST be drawn after
// the annotation box (its white fill covers this footprint) and after the plot.
slide.addText("(5,1)", {
  x: px(497), y: px(249), w: px(38), h: px(14),
  align: "left", valign: "top", fontSize: 9, color: "008000", fontFace: A, margin: 0,
});

// x-axis tick labels — MEASURED band frame y 269..283 under the plot box, which
// the annotation box's white fill would otherwise cover, so drawn here.
xTickVals.forEach(xv => {
  slide.addText(String(xv), {
    x: mapX(xv) - px(12), y: mapY(0) + px(4), w: px(24), h: px(14),
    align: "center", valign: "top", fontSize: 9, color: "000000", fontFace: A, margin: 0,
  });
});

// ============================================================
// BOUNCING LABEL + PURPLE ARROW
// "Bouncing" in purple 7030A0 at x ~ 340-560, y ~ 310-330
// Arrow pointing down/right toward oscillating columns
// ============================================================
const bounceX = px(380);
const bounceY = px(310);
slide.addText("Bouncing", {
  x: bounceX, y: bounceY, w: px(120), h: px(20),
  fontSize: 14, bold: true, color: "7030A0", fontFace: A, margin: 0,
});

// Purple arrow: from near "Bouncing" pointing down/right
// Draw as triangle (arrowhead) + line
const arrowStartX = px(460);
const arrowStartY = px(320);
const arrowEndX = px(520);
const arrowEndY = px(350);
slide.addShape(pptx.ShapeType.line, {
  x: arrowStartX, y: arrowStartY, w: arrowEndX - arrowStartX, h: arrowEndY - arrowStartY,
  line: { color: "7030A0", width: 2 },
});
// Arrowhead (triangle)
slide.addShape(pptx.ShapeType.triangle, {
  x: arrowEndX - px(5), y: arrowEndY - px(5), w: px(10), h: px(10),
  fill: { color: "7030A0" }, line: { color: "7030A0", width: 0 },
  flipV: true, // point down/right
});

// ============================================================
// RED ARROW (left side above main table)
// x ~ 160-170, y ~ 324-348, pointing down/right
// ============================================================
const rArrowStartX = px(165);
const rArrowStartY = px(330);
const rArrowEndX = px(220);
const rArrowEndY = px(370);
slide.addShape(pptx.ShapeType.line, {
  x: rArrowStartX, y: rArrowStartY, w: rArrowEndX - rArrowStartX, h: rArrowEndY - rArrowStartY,
  line: { color: "FF0000", width: 2 },
});
// Arrowhead
slide.addShape(pptx.ShapeType.triangle, {
  x: rArrowEndX - px(5), y: rArrowEndY - px(5), w: px(10), h: px(10),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
  flipV: true,
});

// ============================================================
// MAIN TABLE (8 rows x 17 cols = 1 label + 16 data)
// Position: x ~ 63-893, y ~ 350-530
// Row labels: x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
// ============================================================
const mTableX = px(63);
const mTableY = px(350);
const mLabelW = px(80);
const mColW = px(50); // 830px / 16 = ~52px per col
const mRowH = px(22); // ~180px / 8 = 22.5px

const rowLabels = [
  "x", "f(x)", "x-delta", "f(x-delta)", "x+delta", "f(x+delta)", "slope", "next x"
];

const rowData = [
  // row 0: x
  [3, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1],
  // row 1: f(x)
  [9, 3.89, 2.96, 2.21, 1.64, 1.25, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01],
  // row 2: x-delta
  [2.9, 3.2, 3.5, 3.8, 4.1, 4.4, 4.7, 5, 4.7, 5, 4.7, 5, 4.7, 5, 4.7, 5],
  // row 3: f(x-delta)
  [5.41, 4.24, 3.25, 2.44, 1.81, 1.36, 1.09, 1, 1.09, 1, 1.09, 1, 1.09, 1, 1.09, 1],
  // row 4: x+delta
  [3.1, 3.4, 3.7, 4, 4.3, 4.6, 4.9, 5.2, 4.9, 5.2, 4.9, 5.2, 4.9, 5.2, 4.9, 5.2],
  // row 5: f(x+delta)
  [4.61, 3.56, 2.69, 2, 1.49, 1.16, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04, 1.01, 1.04],
  // row 6: slope
  [-8, -6.8, -5.6, -4.4, -3.2, -2, -0.8, 0.4, -0.8, 0.4, -0.8, 0.4, -0.8, 0.4, -0.8, 0.4],
  // row 7: next x
  [3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8, 5.1, 4.8],
];

// Row background colors MEASURED from the frame at x=850, row centre. The frame
// is an 8-colour rainbow — not the spec's 6-colour list, which is why the old
// build painted rows 6/7 white.
const rowBgColors = [
  "D0D97C",  // row 0: x — frame (208,217,124) yellow-green
  "FCFBF6",  // row 1: f(x) — frame (252,251,246) near-white
  "BF9DDA",  // row 2: x-delta — frame (191,157,218) purple
  "FFFFFD",  // row 3: f(x-delta) — frame (255,255,253) white
  "F8DDC8",  // row 4: x+delta — frame (248,221,200) orange
  "EFEDF0",  // row 5: f(x+delta) — frame (239,237,240) light gray
  "93D186",  // row 6: slope — frame (147,209,134) green
  "FCBCBD",  // row 7: next x — frame (252,188,189) pink
];
const rowTextColors = [
  "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000"
];

// Draw table
for (let r = 0; r < 8; r++) {
  const y = mTableY + r * mRowH;
  const bgColor = rowBgColors[r];
  const textColor = rowTextColors[r];
  
  // Label cell
  slide.addShape(pptx.ShapeType.rect, {
    x: mTableX, y: y, w: mLabelW, h: mRowH,
    fill: { color: bgColor }, line: { color: "000000", width: 0.5 },
  });
  slide.addText(rowLabels[r], {
    x: mTableX, y: y, w: mLabelW, h: mRowH,
    align: "center", valign: "middle", fontSize: 10, bold: true,
    color: textColor, fontFace: A, margin: 0,
  });
  
  // Data cells (16 columns)
  for (let c = 0; c < 16; c++) {
    const x = mTableX + mLabelW + c * mColW;
    const val = rowData[r][c];
    // MEASURED: the frame shows minimal significant digits ("3.3", "5", "1.01")
    // — never a padded "3.30" or "5.0". Strip trailing zeros only.
    let valStr = String(val);
    if (valStr.indexOf(".") >= 0) valStr = valStr.replace(/0+$/, "").replace(/\.$/, "");
    
    slide.addShape(pptx.ShapeType.rect, {
      x: x, y: y, w: mColW, h: mRowH,
      fill: { color: bgColor }, line: { color: "000000", width: 0.5 },
    });
    slide.addText(valStr, {
      x: x, y: y, w: mColW, h: mRowH,
      align: "center", valign: "middle", fontSize: 9,
      color: textColor, fontFace: A, margin: 0,
    });
  }
}

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));