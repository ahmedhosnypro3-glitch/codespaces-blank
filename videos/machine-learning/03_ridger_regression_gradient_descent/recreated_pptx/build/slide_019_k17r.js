// Build slide 019 — "Test Data" — Ridge Regression gradient descent
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// k17r independent second attempt (2026-10-31): w04 full leg FAIL had two
// PIL-confirmed MAJORs — (1) all 9 W-vector cells used heavy black round
// parens where the original uses thin RED square brackets spanning the 3
// stacked weights (orig x130 redpx=97 bow=1); (2) the ||W||² annotation ink
// crossed the W-box red bottom border y297 (render to y299.4, orig stops
// y296). Fix: square brackets drawn as C00000 1pt line shapes, ||W||² text
// shifted up 4px (gy+68 -> gy+64). Output goes to a QA pptx only.
// Attempt 4 — adds the table structure the original carries and that render_3
// was missing (adjudicated PIL-first, see qa/slide019/ worker_report.md):
//   * three full-width yellow row-highlight bands (frame y272..302, 379..409,
//     487..514; content columns x219..892, outlier column x78..118)
//   * bordered table: navy #201860 left border x65 + top rule y170 (the green
//     #008000 right border x894 and split-colour bottom rule y524 are measured
//     from the original frame), interior rules at x117.5 / x124 / x378
//   * row groups aligned across all three columns at y205 / 310 / 420 (the
//     bands prove the original's rows are aligned; attempt 3's per-column
//     y-positions were mis-measured)
//   * per-group geometry: W text left of a divider at x0+82, three test boxes
//     right of x0+95 (recreation_brief step 10: "at its left place red text
//     'W=...', then three equal-width small rectangles left-to-right")
//
// ═══════════════════════════════════════════════════════════════════════════════
// GROUND TRUTH: unique_slides/slide_019.jpg — 960x540, exactly 72 px/in
//                (verified: 960/13.3333 = 72.0001) => 1 frame px == 1 pt == 1/72 in.
// All geometry below is in FRAME PX == POINTS. Converted to inches by px().
// Measurement bank: recreated_pptx/qa/slide019/
// ═══════════════════════════════════════════════════════════════════════════════

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide019/slide_019_k17r.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top stroke on this deck), badge with numeral 19.
drawHouseChrome(pptx, slide, { numeral: 19 });

// ── COLOR PALETTE (spec hierarchy: headers/labels black, W+||W||² red, y green) ─
const BLUE   = "0000FF";  // column headers, title, test-vector labels
const RED    = "FF0000";  // W vectors, ||W||² (attempt_1 judge F1/F2 colour fix)
const GREEN  = "008000";  // predicted y values
const BLACK  = "000000";  // test headers, x values, labels, W label
const FONT   = "Arial";
// Measured from the original frame (qa/slide019/skeleton_census.py):
const NAVY   = "201860";  // table left/top border + interior rules
const GREENB = "008000";  // table right border + bottom-right rule
const YELLOW = "FFFF80";  // row-highlight bands (modal #F8F880)
const RULE   = "8B3A3A";  // W/test divider + inter-column rule (washed maroon)
const MAROON = "8B3A3A";  // test-grid interior rules (orig cell borders read washed maroon)
const REDB   = "8A2024";  // RIDGE-3 column rect edges (measured 138,32,36 / 135,34,38)

// ── HELPERS ────────────────────────────────────────────────────────────────────
function textBox(x, y, w, h, runs, opts = {}) {
  // pptxgenjs emits lineSpacing as POINTS (spcPts), not a multiplier: a bare
  // 1.2 becomes a 1.2pt line height and LibreOffice drops the text entirely.
  const first = Array.isArray(runs) ? runs[0] : runs;
  const size = (first && first.options && first.options.fontSize) || 12;
  const defaults = {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, lineSpacing: size * 1.2,
  };
  slide.addText(runs, { ...defaults, ...opts });
}

function band(x, y, w, h) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: YELLOW }, line: { type: "none" },
  });
}

function vline(x, y0, y1, color, width = 1) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x), y: px(y0), w: 0, h: px(y1 - y0),
    line: { color, width },
  });
}

function hline(y, x0, x1, color, width = 1) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x0), y: px(y), w: px(x1 - x0), h: 0,
    line: { color, width },
  });
}

// ── TITLE BAR ──────────────────────────────────────────────────────────────────
// Blue-bordered box at x68..434, y66..159 with "Test Data" in bold blue
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(66), w: px(434 - 68), h: px(159 - 66),
  line: { color: BLUE, width: 2 },
  fill: { color: "FFFFFF" }, // white interior
});
textBox(76, 74, 350, 90, [
  { text: "Test Data", options: { bold: true, italic: true, color: BLUE, fontSize: 15 } }
]);

// ── TEST POINT VECTORS (2-D stacked, INSIDE the box — orig ink rows y79..148) ──
// Orig: title left; three vector groups x~157-218 / 248-309 / 344-405:
// red underlined "zᵢ =" label, TALL parens spanning both rows (y82..124),
// top value y86-99 over bottom value y108-121 (black), blue "y=NN" y134-148.
// Title "Test Data" is uniformly blue in the orig (PIL census 0.88/0.90).
function vecGroup(label, labX, top, bot, parLX, valX, parRX, ytext, ytextX) {
  // orig: thin faded-red underbar under the whole "zᵢ" cluster (z+subscript),
  // y113-114, stopping before the "=" (crop_22 header_strip MAJOR) — drawn as
  // an explicit hline after the text (run-underline missed the subscript).
  textBox(labX, 98, 34, 22, [
    { text: label.split(" ")[0], options: { color: "C00000", fontSize: 12 } },
    { text: " =", options: { color: BLACK, fontSize: 12 } },
  ]);
  textBox(parLX, 78, 16, 50, [
    { text: "(", options: { color: BLACK, fontSize: 44 } }
  ]);
  textBox(valX, 82, 24, 22, [
    { text: top, options: { color: BLACK, fontSize: 16, align: "center" } }
  ]);
  textBox(valX, 105, 24, 22, [
    { text: bot, options: { color: BLACK, fontSize: 16, align: "center" } }
  ]);
  textBox(parRX, 78, 16, 50, [
    { text: ")", options: { color: BLACK, fontSize: 44 } }
  ]);
  textBox(ytextX, 130, 56, 18, [
    { text: ytext, options: { color: BLUE, fontSize: 12 } }
  ]);
}
vecGroup("z₁ =", 156, "30", "15", 190, 200, 216, "y=60", 168);
vecGroup("z₂ =", 246, "40", "20", 282, 292, 308, "y=80", 258);
vecGroup("z₃ =", 342, "50", "25", 378, 388, 404, "y=100", 352);
// z-cluster underbars (orig y113-114: x159-175 / 249-265 / 346-362; crop_22)
hline(113.5, 159, 175, "C00000", 0.75);
hline(113.5, 249, 265, "C00000", 0.75);
hline(113.5, 346, 362, "C00000", 0.75);

// ── TABLE BODY FILL + BOTTOM TINT STRIP (PIL adjudication of crop_18
// table_right D3-replacement finding: the original white-fills the whole table
// body y203..514 (incl. outlier column) where the render showed gray panel,
// and carries a tinted summary strip y515..523 — cream x130..377, peach
// x390..643, mint x644..894, same tints as the headers; no text in the strip,
// the interior rules cross it. Drawn here BEFORE the bands so the highlight
// bands and rules sit on top exactly as in the original.)
slide.addShape(pptx.ShapeType.rect, {
  x: px(66), y: px(203), w: px(828), h: px(311),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});
const TINTS = { "NO REG": "F7FBEC", "RIDGE 3": "FAE0C8", "RIDGE 10": "E8FFE8" };
const STRIP = [
  [130, 247, "NO REG"],
  [390, 253, "RIDGE 3"],
  [644, 250, "RIDGE 10"],
];
for (const [sx, sw, nm] of STRIP) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(sx), y: px(515), w: px(sw), h: px(8.5),
    fill: { color: TINTS[nm] }, line: { type: "none" },
  });
}

// ── WHITE SHEET (orig: table interior sits on white, not the gray panel) ──────
// Measured from the original frame (PIL): outlier column x68..117, every W box
// (x0+5..x0+82) and every test grid (x0+115..x0+249) is white in every row
// group; the gray panel shows only in the x0+83..x0+114 gaps. Bands, tints,
// rules and text draw on top of this sheet.
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(171), w: px(49), h: px(351),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});
const COLX = [124, 384, 644];   // column left edges (NO REG / RIDGE 3 / RIDGE 10)
const GROUPY = [205, 310, 420]; // row-group tops (rowGroupsY below)
for (const wx0 of COLX) {
  for (const gy of GROUPY) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(wx0 + 5), y: px(gy - 5), w: px(77), h: px(97),
      fill: { color: "FFFFFF" }, line: { type: "none" },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: px(wx0 + 115), y: px(gy + 2), w: px(134), h: px(92),
      fill: { color: "FFFFFF" }, line: { type: "none" },
    });
  }
}

// ── YELLOW ROW-HIGHLIGHT BANDS (drawn before all table text) ──────────────────
// Content columns: solid x219..892 broken only by the interior rules (rules are
// drawn on top). Outlier column: shorter measured boxes.
//           y-range        x-range
band(219, 272, 670, 31);  // band A content  (x219..889)
band(219, 379, 670, 31);  // band B content
band(219, 487, 670, 28);  // band C content
// outlier-column highlight boxes are drawn by outlierRow() below (measured
// y268..288 / 375..395 / 479..499 — pil_outlier_map_a21)

// ── TABLE RULES ────────────────────────────────────────────────────────────────
// Outer borders: navy left (x65) + top (y170), green right (x894), split bottom (y524).
vline(65, 168, 526, NAVY);
vline(894, 168, 526, GREENB);
hline(170, 64, 894, NAVY);
hline(170, 383.5, 640, REDB);   // top rule is colour-segmented (a29 rgb): red over RIDGE 3
hline(170, 644, 894, GREENB);   // green over RIDGE 10 (a29 rgb: 69,140,70 core)
hline(524, 64, 380, NAVY);      // bottom y524 segments (a29 rgb): navy over outlier+NO REG
hline(524, 383, 640, REDB);     // red over RIDGE 3
hline(524, 644, 894, GREENB);   // green over RIDGE 10
// Interior column-edge rules (continuous through the bands — measured 355/365 rows).
vline(117.5, 168, 526, NAVY);
vline(124, 168, 526, NAVY);
vline(378, 168, 526, NAVY);
// Divider + inter-column rules: drawn per row group, interrupted by the bands.
for (const [y0, y1] of [[203, 291], [310, 379], [416, 513]]) {
  vline(205.5, y0, y1, RULE);   // NO REG: W area | test boxes
  vline(466, y0, y1, RULE);     // RIDGE 3 divider column-internal
  vline(724, y0, y1, RULE);     // RIDGE 10 divider column-internal
}
// Anomalous-column rect edges are CONTINUOUS (a29 adjudication): λ3 rect edges
// dark-red at x383-384 / x637-639, λ10 left edge green at x643 — not per-band.
vline(383.5, 169, 525, REDB);
vline(638, 169, 525, REDB);
vline(643.5, 169, 525, GREENB);

// ── OUTLIER COLUMN ─────────────────────────────────────────────────────────────
// x=66..125 (rules at 64-66 navy and 117-118 navy); header on TWO lines
// (pil_probe_a25 + P1 orig read): "Outlier" y181-192 cap h11 -> fs15 bold
// italic; "Xₛ" y199-211 (X cap 11, lowered s h7) -> fs15 + fs10 subscript.
textBox(67, 178, 56, 18, [
  { text: "Outlier", options: { bold: true, italic: true, color: BLUE, fontSize: 15 } },
]);
textBox(84, 196, 18, 18, [
  { text: "X", options: { color: BLUE, fontSize: 15 } },
]);
// subscript run renders ~3px/clipped in LO — plain positioned box instead
// (orig s: x95-99, y205-211, cap h7 -> fs10)
textBox(95, 203, 8, 10, [
  { text: "s", options: { color: BLUE, fontSize: 10 } },
]);

// Yellow highlight box behind the outlier "22" (measured x76..116,
// y268..288 / 375..395 / 479..499 — pil_probe_a25 yellow census).
// Digit rows: orig glyph tops g1 219/244/269, g2 326/351/376, g3 429/455/480,
// cap h15 -> fs20 (box top = glyph top - 5); first/third bold, "3" regular
// (pil_probe_a25 stroke widths + P1 typography).
function outlierRow(y, x, first, firstColor, band_y, tops) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(76), y: px(band_y), w: px(40), h: px(20),
    fill: { color: YELLOW }, line: { type: "none" },
  });
  // three separate single-line boxes — LO misrenders stacked
  // lineSpacing runs (a20: second/third lines mostly missing)
  const rows = [
    { text: first, options: { color: firstColor, fontSize: 20, bold: true } },
    { text: "3", options: { color: BLUE, fontSize: 20 } },
    { text: "22", options: { color: GREEN, fontSize: 20, bold: true } },
  ];
  rows.forEach((r, i) => {
    textBox(x, tops[i], 30, 22, [r], { align: "center" });
  });
}
outlierRow(203, 84, "11", BLUE, 268, [214, 239, 264]);
outlierRow(325, 79, "30", RED, 375, [321, 346, 371]);
outlierRow(428, 79, "60", RED, 479, [424, 450, 475]);

// Thin blue delimiters around each outlier PAIR (first value + the "3" row;
// the highlighted "22" sits below, OUTSIDE the parens — orig ink y215..264 /
// 323..371 / 425..475). ~2px arcs, ink left [x, x+3], right [x+3.5, x+6.5]
// at bbox w6 — scratch/arc_test; P1 ink #2E3B96.
function outlierArcs(xL, xR, y0, h) {
  [[xL, [90, 270]], [xR, [270, 450]]].forEach(([x, a]) => {
    slide.addShape(pptx.ShapeType.arc, {
      x: px(x), y: px(y0), w: px(6), h: px(h),
      fill: { type: "none" },
      line: { color: "2E3B96", width: 1.5 },
      angleRange: a,
    });
  });
}
outlierArcs(83, 110, 215, 50);
outlierArcs(77.5, 106, 323, 49);
outlierArcs(77.5, 105.5, 425, 51);

// ── MAIN CONTENT COLUMNS ───────────────────────────────────────────────────────
// Column definitions: [name, x_start, x_end, header text split into blue + red runs]
// The original's headers are blue up to "with" and the "(as if λ=0)" / "λ=3" / "λ=10"
// tail in red (measured: red px in each header band, qa/slide019/ structure census).
const columns = [
  { name: "NO REG", x0: 124, x1: 380, headBlue: "NO Regularizer with ", headRed: "(as if λ=0)" },
  { name: "RIDGE 3", x0: 384, x1: 640, headBlue: "Ridge Regularizer with ", headRed: "λ=3" },
  { name: "RIDGE 10", x0: 644, x1: 900, headBlue: "Ridge Regularizer with ", headRed: "λ=10" },
];

// Data for each column: 3 row groups (one per outlier)
// Each row group: { w: "W=(...)", tests: [{x1,x2,y} x3] }
const columnData = {
  "NO REG": [
    {
      w: "W=(0, 2), ||W||²=4",
      w3: ['0', '2', '0'],
      norm: "||W||²=4",
      tests: [
        { x1: 30, x2: 15, y: 60 },
        { x1: 40, x2: 20, y: 80 },
        { x1: 50, x2: 25, y: 100 },
      ]
    },
    {
      w: "W=(2.7, 0.67), ||W||²=8.11",
      w3: ['2.7', '0.67', '0.64'],
      norm: "||W||²=8.11",
      tests: [
        { x1: 30, x2: 15, y: 32.4 },
        { x1: 40, x2: 20, y: 42.3 },
        { x1: 50, x2: 25, y: 52.3 },
      ]
    },
    {
      w: "W=(4, 0.29), ||W||²=16.7",
      w3: ['4', '0.29', '0.78'],
      norm: "||W||²=16.7",
      tests: [
        { x1: 30, x2: 15, y: 24.4 },
        { x1: 40, x2: 20, y: 31.2 },
        { x1: 50, x2: 25, y: 38 },
      ]
    },
  ],
  "RIDGE 3": [
    {
      w: "W=(0.1, 1.95), ||W||²=3.8",
      w3: ['0.1', '1.95', '0.03'],
      norm: "||W||²=3.8",
      tests: [
        { x1: 30, x2: 15, y: 59 },
        { x1: 40, x2: 20, y: 78.7 },
        { x1: 50, x2: 25, y: 98.4 },
      ]
    },
    {
      w: "W=(1.2, 0.72), ||W||²=2.45",
      w3: ['1.2', '0.72', '0.77'],
      norm: "||W||²=2.45",
      tests: [
        { x1: 30, x2: 15, y: 34.1 },
        { x1: 40, x2: 20, y: 45.1 },
        { x1: 50, x2: 25, y: 56.1 },
      ]
    },
    {
      w: "W=(1.77, 0.32), ||W||²=4.2",
      w3: ['1.77', '0.32', '0.99'],
      norm: "||W||²=4.2",
      tests: [
        { x1: 30, x2: 15, y: 26.2 },
        { x1: 40, x2: 20, y: 34.4 },
        { x1: 50, x2: 25, y: 42.5 },
      ]
    },
  ],
  "RIDGE 10": [
    {
      w: "W=(0.13, 1.87), ||W||²=3.5",
      w3: ['0.13', '1.87', '0.09'],
      norm: "||W||²=3.5",
      tests: [
        { x1: 30, x2: 15, y: 57.4 },
        { x1: 40, x2: 20, y: 76.5 },
        { x1: 50, x2: 25, y: 95.6 },
      ]
    },
    {
      w: "W=(0.54, 0.73), ||W||²=1.48",
      w3: ['0.54', '0.73', '0.81'],
      norm: "||W||²=1.48",
      tests: [
        { x1: 30, x2: 15, y: 34.6 },
        { x1: 40, x2: 20, y: 46 },
        { x1: 50, x2: 25, y: 57.4 },
      ]
    },
    {
      w: "W=(0.82, 0.33), ||W||²=1.92",
      w3: ['0.82', '0.33', '1.1'],
      norm: "||W||²=1.92",
      tests: [
        { x1: 30, x2: 15, y: 26.8 },
        { x1: 40, x2: 20, y: 35.4 },
        { x1: 50, x2: 25, y: 44.1 },
      ]
    },
  ],
};

// Row-group tops — ALIGNED across columns (the yellow bands span all three
// columns, proving the original's rows align; attempt 3 mis-measured per column).
const rowGroupsY = [205, 310, 420];

// Per-group geometry measured from the original frame:
//   W text area: x0 .. x0+82  (divider drawn at x0+82)
//   test boxes:  x0+82 .. x1  (three equal boxes right of the divider)
const W_W = 82;

for (const col of columns) {
  const x0 = col.x0;
  const w = col.x1 - col.x0;
  const data = columnData[col.name];

  // Tinted header boxes (measured from orig y172..203): pale yellow NO-REG,
  // pale peach RIDGE 3, mint RIDGE 10. TINTS is module-scope (shared with the
  // bottom summary strip).
  const tint = TINTS[col.name];
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x0), y: px(172), w: px(w), h: px(203 - 172),
    fill: { color: tint }, line: { type: "none" },
  });

  // Column header (blue bold, red λ tail): ink rows y181..196, caps ~12px ->
  // fs16, indented +16/+17/+18px from the column left (a29 head census)
  textBox(x0 + 16, 177, w, 30, [
    { text: col.headBlue, options: { bold: true, color: BLUE, fontSize: 16 } },
    { text: col.headRed, options: { bold: true, color: RED, fontSize: 16 } },
  ], {});

  for (let gi = 0; gi < 3; gi++) {
    const gy = rowGroupsY[gi];
    const group = data[gi];

    // W = 3-entry column vector. k17r (independent 2nd attempt, 2026-10-31):
    // w04 full leg FAILed with two PIL-confirmed MAJORs — heavy black round
    // parens where the orig uses thin RED SQUARE brackets spanning the 3
    // stacked weights (orig x130 redpx=97 bow=1, render redpx=0), and the
    // ||W||² ink crossing the W-box bottom border y297 (render to y299.4,
    // orig stops y296). Fix: square brackets drawn as C00000 1pt line shapes
    // (stem + top/bottom ticks) spanning gy..gy+62, and ||W||² shifted up 4px.
    // Third entries are the printed values per doc-parse 6x OCR — the
    // original's own ||W||² labels are inconsistent with them (lecturer
    // typos) and are reproduced as printed.
    const v3 = group.w3;
    // Enclosure rectangle around the W block (crop leg 16 #2 geometry
    // x129..206 / y200..297, 306..405, 415..514; orig border ink is dark).
    slide.addShape(pptx.ShapeType.rect, {
      x: px(x0 + 5), y: px(gy - 5), w: px(77), h: px(97),
      fill: { type: "none" }, line: { color: MAROON, width: 0.75 },
    });
    textBox(x0 + 16, gy + 22, 30, 16, [
      { text: "W", options: { color: RED, fontSize: 9, underline: true } },
      { text: " =", options: { color: BLACK, fontSize: 9 } },
    ], {});
    const BR = "C00000";
    vline(x0 + 38, gy, gy + 62, BR, 1);
    hline(gy, x0 + 38, x0 + 45, BR, 1);
    hline(gy + 62, x0 + 38, x0 + 45, BR, 1);
    vline(x0 + 66, gy, gy + 62, BR, 1);
    hline(gy, x0 + 59, x0 + 66, BR, 1);
    hline(gy + 62, x0 + 59, x0 + 66, BR, 1);
    textBox(x0 + 49, gy + 2, 16, 60, v3.map((v, i) => ({
      text: v, options: { color: RED, fontSize: 7, align: "center", breakLine: i < v3.length - 1 },
    })), { lineSpacing: 20 });
    textBox(x0 + 6, gy + 64, 76, 16, (() => {
      const m = group.norm.match(/^(\|\|)(W)(\|\|.*$)/);
      return m ? [
        { text: m[1], options: { color: RED, fontSize: 8 } },
        { text: m[2], options: { color: RED, fontSize: 8, underline: true } },
        { text: m[3], options: { color: RED, fontSize: 8 } },
      ] : [{ text: group.norm, options: { color: RED, fontSize: 8 } }];
    })(), {});

    // Blue flow arrow between the W box and the test grid (crop leg 13 #4/#5;
    // orig blue ink x204..230 y gy+37..+58 per row group)
    slide.addShape(pptx.ShapeType.rightArrow, {
      x: px(x0 + 85), y: px(gy + 40), w: px(25), h: px(19),
      fill: { type: "none" },
      line: { color: BLUE, width: 1 },
    });

    // Bordered test grid (crop leg 13 #7): header Test₁|Test₂|Test₃, rows
    // x₁ / x₂, green y row inside the highlight band. Label column INSIDE the
    // outer border (crop leg 17 #1: labels were dumped outside/clipped).
    const gx0 = x0 + 82;
    // λ=10 grid right border at 888 (orig): no border past the green column
    // rule at x894 or past the green y-text (a21 adjudication)
    const gx1 = col.name === "RIDGE 10" ? 888 : col.x1;
    const v0 = x0 + 142;
    const colW = (gx1 - v0) / 3;
    // outer box + rules
    slide.addShape(pptx.ShapeType.rect, {
      x: px(gx0), y: px(gy + 2), w: px(gx1 - gx0), h: px(92),
      fill: { type: "none" }, line: { color: MAROON, width: 0.75 },
    });
    for (const ry of [gy + 21, gy + 43]) {
      hline(ry, gx0, gx1, MAROON, 0.75);
    }
    for (const rx of [v0 + colW, v0 + 2 * colW]) {
      slide.addShape(pptx.ShapeType.line, {
        x: px(rx), y: px(gy + 2), w: 0, h: px(92),
        line: { color: MAROON, width: 0.75 },
      });
    }
    // header row
    for (let ti = 0; ti < 3; ti++) {
      textBox(v0 + ti * colW, gy + 5, colW, 15, [
        { text: `Test${"₁₂₃"[ti]}`, options: { color: BLACK, fontSize: 8, align: "center" } },
      ], {});
    }
    // x₁ / x₂ rows
    for (const [ri, key] of [[0, "x1"], [1, "x2"]]) {
      textBox(x0 + 96, gy + 23 + ri * 22, 48, 15, [
        { text: key === "x1" ? "x₁" : "x₂", options: { color: BLACK, fontSize: 8, align: "center" } },
      ], {});
      for (let ti = 0; ti < 3; ti++) {
        textBox(v0 + ti * colW, gy + 23 + ri * 22, colW, 15, [
          { text: String(group.tests[ti][key]), options: { color: BLACK, fontSize: 8, align: "center" } },
        ], {});
      }
    }
    // y row — green, inside the highlight band (orig green rows y276-294 etc.)
    textBox(x0 + 96, gy + 69, 48, 18, [
      { text: "y", options: { color: GREEN, fontSize: 8, align: "center" } },
    ], {});
    for (let ti = 0; ti < 3; ti++) {
      textBox(v0 + ti * colW, gy + 69, colW, 18, [
        { text: String(group.tests[ti].y), options: { color: GREEN, fontSize: 8, align: "center" } },
      ], {});
    }
  }
}

// ── INTER-COLUMN ARROWS ────────────────────────────────────────────────────────
// NONE — pixel census of the original (x375..405 / x630..672, y310..330) shows
// only the vertical divider rules in the gaps, no arrows (crop leg 17 #6).

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
