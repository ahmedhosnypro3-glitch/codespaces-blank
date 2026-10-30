// Build slide 019 — "Test Data" — Ridge Regression gradient descent
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
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

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_019_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top stroke on this deck), badge with numeral 19.
drawHouseChrome(pptx, slide, { numeral: 19 });

// ── COLOR PALETTE ──────────────────────────────────────────────────────────────
const BLUE   = "0000FF";  // headers, title
const RED    = "FF0000";  // W vectors, ||W||²
const GREEN  = "008000";  // predicted y values
const BLACK  = "000000";  // x values, labels, arrows
const FONT   = "Arial";
// Measured from the original frame (qa/slide019/skeleton_census.py):
const NAVY   = "201860";  // table left/top border + interior rules
const GREENB = "008000";  // table right border + bottom-right rule
const YELLOW = "FFFF80";  // row-highlight bands (modal #F8F880)
const RULE   = "8B3A3A";  // W/test divider + inter-column rule (washed maroon)

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
textBox(76, 72, 350, 90, [
  { text: "Test Data", options: { bold: true, color: BLUE, fontSize: 24 } }
]);

// ── TEST POINT REFERENCE LINE ──────────────────────────────────────────────────
// y=80..99, x=433..895 — black text
textBox(433, 80, 462, 20, [
  { text: "z₁=(30, 15), y=60;  z₂=(40, 20), y=80;  z₃=(50, 25), y=100", options: { color: BLACK, fontSize: 12 } }
]);

// ── YELLOW ROW-HIGHLIGHT BANDS (drawn before all table text) ──────────────────
// Content columns: solid x219..892 broken only by the interior rules (rules are
// drawn on top). Outlier column: shorter measured boxes.
//           y-range        x-range
band(206, 272, 674, 31);  // band A content  (x206..880)
band(206, 379, 674, 31);  // band B content
band(206, 487, 674, 28);  // band C content
band(78, 272, 40, 17);    // band A outlier column
band(78, 379, 40, 17);    // band B outlier column
band(78, 487, 40, 14);    // band C outlier column (y486..499)

// ── TABLE RULES ────────────────────────────────────────────────────────────────
// Outer borders: navy left (x65) + top (y170), green right (x894), split bottom (y524).
vline(65, 168, 526, NAVY);
vline(894, 168, 526, GREENB);
hline(170, 64, 894, NAVY);
hline(524, 64, 641, NAVY);
hline(524, 641, 894, GREENB);
// Interior column-edge rules (continuous through the bands — measured 355/365 rows).
vline(117.5, 168, 526, NAVY);
vline(124, 168, 526, NAVY);
vline(130, 168, 526, NAVY);
vline(378, 168, 526, NAVY);
// Divider + inter-column rules: drawn per row group, interrupted by the bands.
for (const [y0, y1] of [[203, 291], [310, 379], [416, 513]]) {
  vline(205.5, y0, y1, RULE);   // NO REG: W area | test boxes
  vline(466, y0, y1, RULE);     // RIDGE 3 divider column-internal
  vline(724, y0, y1, RULE);     // RIDGE 10 divider column-internal
}
for (const [y0, y1] of [[168, 271], [303, 378], [410, 486]]) {
  vline(383.5, y0, y1, RULE);   // between NO REG and RIDGE 3
  vline(390, y0, y1, RULE);     // second inter-column rule
  vline(643.5, y0, y1, GREENB); // between RIDGE 3 and RIDGE 10
}

// ── OUTLIER COLUMN ─────────────────────────────────────────────────────────────
// x=66..125 (rules at 64-66 navy and 117-118 navy); header measured y181..192
textBox(68, 181, 56, 30, [
  { text: "Outlier Xₛ", options: { bold: true, color: BLUE, fontSize: 9 } }
]);

// Three outlier rows — black, aligned to the row-group tops (measured y200..210 / 327..341 / 430..443)
textBox(68, 203, 56, 30, [
  { text: "11, 3, 22", options: { color: BLACK, fontSize: 10 } }
]);
textBox(68, 325, 56, 30, [
  { text: "30, 3, 22", options: { color: BLACK, fontSize: 10 } }
]);
textBox(68, 428, 56, 30, [
  { text: "60, 3, 22", options: { color: BLACK, fontSize: 10 } }
]);

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
      w: "W=(2, 0), ||W||²=4",
      tests: [
        { x1: 30, x2: 15, y: 60 },
        { x1: 40, x2: 20, y: 80 },
        { x1: 50, x2: 25, y: 100 },
      ]
    },
    {
      w: "W=(2.7, 0.67), ||W||²=8.11",
      tests: [
        { x1: 30, x2: 15, y: 32.4 },
        { x1: 40, x2: 20, y: 42.3 },
        { x1: 50, x2: 25, y: 52.3 },
      ]
    },
    {
      w: "W=(4, 0.29), ||W||²=16.7",
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
      tests: [
        { x1: 30, x2: 15, y: 59 },
        { x1: 40, x2: 20, y: 78.7 },
        { x1: 50, x2: 25, y: 98.4 },
      ]
    },
    {
      w: "W=(1.2, 0.72), ||W||²=2.45",
      tests: [
        { x1: 30, x2: 15, y: 34.1 },
        { x1: 40, x2: 20, y: 45.1 },
        { x1: 50, x2: 25, y: 56.1 },
      ]
    },
    {
      w: "W=(1.77, 0.32), ||W||²=4.2",
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
      tests: [
        { x1: 30, x2: 15, y: 57.4 },
        { x1: 40, x2: 20, y: 76.5 },
        { x1: 50, x2: 25, y: 95.6 },
      ]
    },
    {
      w: "W=(0.54, 0.73), ||W||²=1.48",
      tests: [
        { x1: 30, x2: 15, y: 34.6 },
        { x1: 40, x2: 20, y: 46 },
        { x1: 50, x2: 25, y: 57.4 },
      ]
    },
    {
      w: "W=(0.82, 0.33), ||W||²=1.92",
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

  // Column header (blue bold, red λ tail) at y=181..198 (measured band)
  textBox(x0, 181, w, 30, [
    { text: col.headBlue, options: { bold: true, color: BLUE, fontSize: 12 } },
    { text: col.headRed, options: { bold: true, color: RED, fontSize: 12 } },
  ], {});

  for (let gi = 0; gi < 3; gi++) {
    const gy = rowGroupsY[gi];
    const group = data[gi];

    // W vector + ||W||² (red) — left of the divider; explicit break at the
    // vector's closing comma so the wrap never lands inside "||W||²".
    const cut = group.w.indexOf("), ") + 1;
    textBox(x0, gy, W_W, 40, [
      { text: group.w.slice(0, cut), options: { color: RED, fontSize: 9, breakLine: true } },
      { text: group.w.slice(cut + 1), options: { color: RED, fontSize: 9 } },
    ], {});

    // Three test boxes right of the divider: "TestN:" / "x₁=..,x₂=..," / "y=.."
    // (three lines — matches the original's ~36px test block; x black, y green)
    const testW = (w - W_W) / 3;
    for (let ti = 0; ti < 3; ti++) {
      const test = group.tests[ti];
      const tx = x0 + W_W + ti * testW;
      const ty = gy + 25; // test block sits in the group's lower half
      const runs = [
        { text: `Test${ti + 1}:`, options: { color: BLACK, fontSize: 8, breakLine: true } },
        { text: `x₁=${test.x1},x₂=${test.x2},`, options: { color: BLACK, fontSize: 8, breakLine: true } },
        { text: `y=${test.y}`, options: { color: GREEN, fontSize: 8 } },
      ];
      textBox(tx, ty, testW, 40, runs, {});
    }
  }
}

// ── INTER-COLUMN ARROWS ────────────────────────────────────────────────────────
// Two right-pointing arrows between columns at mid-height (y=320)
const arrowY = 320;
const arrowLen = 20;

slide.addShape(pptx.ShapeType.line, {
  x: px(380), y: px(arrowY), w: px(arrowLen), h: 0,
  line: { color: BLACK, width: 1.5, endArrowType: "triangle" },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(640), y: px(arrowY), w: px(arrowLen), h: 0,
  line: { color: BLACK, width: 1.5, endArrowType: "triangle" },
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
