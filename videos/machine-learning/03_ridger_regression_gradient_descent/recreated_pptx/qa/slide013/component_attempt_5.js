// components/slide_013.js — BANKED composition of slide 013
// ("Effect of Overfitting on model parameter "W""), ML lecture 03
// (03_ridger_regression_gradient_descent).
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide — house chrome
// (numeral 13) + title + the one Train/Test label pair + three training tables +
// three test tables + two hollow arrows per band + three W boxes (red-bordered
// white rect with a 600-dpi math image: W = [v1;v2;v3] inside thin parens and
// the pale-yellow ||W||^2 ellipse). opts:
//   { numeral }     — override the badge numeral (variant passes its own number)
//   { skip: {...} } — omit any block: chrome, title, labels, trainTables,
//                     testTables, arrows, wBoxes
//   { only: {...} } — draw ONLY the listed blocks
//
// CHILD of slide 012 (dependency edge 13 > 12): the table PATTERN is imported
// from the certified parent component (makeTrainTable / makeTestTable and the
// alternating blue/red ink rule), never copy-pasted. 013 redraws it at 013's own
// PIL-measured geometry (train x92..459 vs 012's x203..571) with 013's own
// values, and restyles the cells to 013's measured typography (Times New Roman
// bold 20pt, real subscripts on X1..X8 / Test1..Test3 — the frame shows them).
//
// Geometry is PIL-measured from unique_slides/slide_013.jpg (960x540, 1px=1pt);
// see qa/slide013/MEASUREMENTS.md + measure_013_final*.txt. The W-box math
// (W, =, parens, digits, ellipse) is a matplotlib STIX PNG rendered at 600 dpi
// (build/assets/make_013_wbox.py) and placed at exact px/600 size — the deck's
// certified professional-2D math mechanism.
//
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));
// CERTIFIED PARENT COMPONENT (import, never copy).
const P = require(path.resolve(__dirname, "./slide_012.js"));

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette (qa/slide013/measure_013_final*.txt) ────────────────────
const RED = "C00000";        // title, red table ink, W glyph, W-box border
const BLUE = "0000A7";       // blue table ink, Train/Test label fill, arrows
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFFF00";     // outlier-cell highlight (measured 250,255,14)
const TRAIN_BORDER = "CED0CD"; // measured gray gridlines (206,208,205)
const TEST_BORDER = "D7BEC2";  // measured rose gridlines (213,188,192)
const TEST_SHADE = "CCFFE1";   // measured y-row mint fill (203,255,224)
const SERIF = "Times New Roman";
const SANS = "Arial";

const TITLE_TEXT = "Effect of Overfitting on model parameter \u201cW\u201d";

// ── measured geometry (frame px) ─────────────────────────────────────────────
const TITLE_BOX = { x: 154, y: 62, w: 660, h: 40, fontSize: 30, lineSpacing: 34 };

const LABELS = [
  { x: 96, y: 97, w: 64, h: 28, text: "Train" },
  { x: 802, y: 97, w: 64, h: 28, text: "Test" },
];
const LABEL_FONT_SIZE = 17;

const TRAIN_X = 92, TRAIN_W = 367;
const TRAIN_COLS = [41, 41, 40, 41, 41, 41, 40, 42, 40]; // 92,133,174,214,255,296,337,377,419,459
const TRAIN_BANDS = [
  { y: 126, rows: [31, 31, 31, 30] },
  { y: 265, rows: [31, 31, 31, 31] },
  { y: 402, rows: [32, 31, 31, 31] },
];

const TEST_X = 719, TEST_W = 153;
const TEST_COLS = [51, 51, 51];
const TEST_BANDS = [
  { y: 128, rows: [32, 30, 31, 31] },
  { y: 266, rows: [32, 30, 31, 31] },
  { y: 403, rows: [32, 30, 31, 31] },
];

// W boxes: red 2pt border rect + math image (origin 507 / band y, 115x123 px).
const WBOX_W = 116, WBOX_H = 124;
const WBOX_RECT = [
  { x: 506.5, y: 127.5 },
  { x: 506.5, y: 265.5 },
  { x: 506.5, y: 403.5 },
];
const WBOX_IMG = [
  { image: path.resolve(__dirname, "../assets/wbox_band1.png"), x: 507, y: 128 },
  { image: path.resolve(__dirname, "../assets/wbox_band2.png"), x: 507, y: 266 },
  { image: path.resolve(__dirname, "../assets/wbox_band3.png"), x: 507, y: 404 },
];

// Hollow blue arrows, one pair per band. Measured: total 25px tall, shaft rows
// y+6..y+19, tail bar at the left end, 30px shaft, 9px solid head tip.
const ARROWS = [
  { y: 186, L: 464, R: 627 },
  { y: 319, L: 464, R: 628 },
  { y: 452, L: 464, R: 627 },
];
const ARROW = { h: 25, shaftTop: 6, shaftBot: 19, shaft: 30, head: 9 };

// ── measured table content (verbatim per analysis/slide_013_final.json) ──────
const TRAIN_HEADER = ["", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"];
const TEST_HEADER = ["Test1", "Test2", "Test3"];

const ROW_X2 = ["X2", 1, 3, 5, 6, 16, 7, 5, 3];
const ROW_Y = ["y", 2, 4, 6, 8, 16, 18, 20, 22];
const TRAIN_ROWS = [
  [["X1", 1, 2, 3, 4, 8, 9, 10, 11], ROW_X2, ROW_Y],  // band 1: no highlight
  [["X1", 1, 2, 3, 4, 8, 9, 10, 30], ROW_X2, ROW_Y],  // band 2: X8 30, yellow
  [["X1", 1, 2, 3, 4, 8, 9, 10, 60], ROW_X2, ROW_Y],  // band 3: X8 60, yellow
];
const TEST_ROWS = [
  [[30, 40, 50], [15, 20, 25], [60, 80, 100]],
  [[30, 40, 50], [15, 20, 25], [32.4, 42.3, 52.3]],
  [[30, 40, 50], [15, 20, 25], [24.4, 31.2, 38]],
];

const TABLE_FONT_SIZE = 20;
const TEST_HEAD_FONT_SIZE = 18; // measured Test1 cap 12px vs body digit 13px
const SUBSCRIPT_SIZE = 11;

// ── helpers ──────────────────────────────────────────────────────────────────
// Subscript-style runs: "X1" -> X + a smaller 1 SET ON THE SAME BASELINE.
// Measured from the frame: the index digit is ~7px tall (11pt) and its bottom
// sits on the X baseline (1px lower at most) — a full pptx baseline shift
// (-25% = 2.75px at 11pt) renders visibly too low, so the run stays on the
// baseline and only its size shrinks.
function runsFor(value, color, fontSize) {
  const m = /^(X|Test)([1-8])$/.exec(String(value));
  if (!m) return String(value);
  return [
    { text: m[1], options: { fontFace: SERIF, fontSize, bold: true, color } },
    { text: m[2], options: { fontFace: SERIF, fontSize: SUBSCRIPT_SIZE, bold: true,
                             color, charSpacing: -0.5 } },
  ];
}

function cellStyle(ci, ri, color, fill, align, fontSize) {
  return {
    fontFace: SERIF, fontSize, bold: true, color, align,
    valign: "middle", fill: { color: fill },
  };
}

function buildTrainData(bi) {
  const hl = bi === 0 ? -1 : 0; // X1 row of bands 2/3 carries the yellow X8 cell
  const base = P.makeTrainTable(TRAIN_HEADER, TRAIN_ROWS[bi], hl, 8);
  return base.map((row, ri) =>
    row.map((cell, ci) => {
      const isHead = ri === 0;
      // Measured: headers alternate BLUE(odd)/RED(even); the row-label column
      // (X1/X2/y) is BLACK (frame median 79,81,78), not blue.
      const color = ci === 0 ? BLACK : (ci % 2 === 1 ? BLUE : RED);
      const fill = cell.options.fill && cell.options.fill.color === "FFFF00" ? YELLOW : WHITE;
      // Measured: train headers are LEFT-aligned (X1 ink starts 9px into the
      // cell, not centered); row labels left; data cells centered.
      const align = ci === 0 || isHead ? "left" : "center";
      const fontSize = TABLE_FONT_SIZE; // header X1 measured cap 14px == 20pt serif
      return {
        text: runsFor(cell.text, color, fontSize),
        options: cellStyle(ci, ri, color, fill, align, fontSize),
      };
    })
  );
}

function buildTestData(bi) {
  const base = P.makeTestTable(TEST_HEADER, TEST_ROWS[bi]);
  return base.map((row, ri) =>
    row.map((cell, ci) => {
      const isHead = ri === 0;
      const color = ci % 2 === 0 ? RED : BLUE; // measured RED/BLUE/RED phase
      const fill = ri === 3 ? TEST_SHADE : WHITE; // y row = mint (all bands)
      const fontSize = isHead ? TEST_HEAD_FONT_SIZE : TABLE_FONT_SIZE;
      return {
        text: runsFor(cell.text, color, fontSize),
        options: cellStyle(ci, ri, color, fill, "center", fontSize),
      };
    })
  );
}

function addTable(slide, data, x, y, w, colW, rowH, border) {
  slide.addTable(data, {
    x: px(x), y: px(y), w: px(w), h: px(rowH.reduce((a, b) => a + b, 0)),
    colW: colW.map(px), rowH: rowH.map(px),
    fontFace: SERIF, fontSize: TABLE_FONT_SIZE,
    border: { pt: 1.25, color: border },
    autoFit: false,
  });
}

// ── BLOCK draw functions (draw order = certified z-order) ────────────────────
function drawChrome(pptx, slide, opts) {
  const n = opts && opts.numeral !== undefined ? opts.numeral : 13;
  drawHouseChrome(pptx, slide, { numeral: n });
}

function drawTitle(pptx, slide) {
  const T = TITLE_BOX;
  slide.addText(TITLE_TEXT, {
    x: px(T.x), y: px(T.y), w: px(T.w), h: px(T.h),
    align: "left", valign: "top", margin: 0,
    fontFace: SANS, fontSize: T.fontSize, bold: true, color: RED,
    lineSpacing: T.lineSpacing,
  });
}

function drawLabels(pptx, slide) {
  for (const L of LABELS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
      fill: { color: BLUE }, line: { type: "none" },
    });
    slide.addText(L.text, {
      x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
      align: "center", valign: "middle", margin: 0,
      fontFace: SERIF, fontSize: LABEL_FONT_SIZE, bold: true, italic: true,
      color: WHITE, lineSpacing: LABEL_FONT_SIZE + 3,
    });
  }
}

function drawTrainTables(pptx, slide) {
  TRAIN_BANDS.forEach((band, bi) => {
    addTable(slide, buildTrainData(bi), TRAIN_X, band.y, TRAIN_W,
      TRAIN_COLS, band.rows, TRAIN_BORDER);
  });
}

function drawTestTables(pptx, slide) {
  TEST_BANDS.forEach((band, bi) => {
    addTable(slide, buildTestData(bi), TEST_X, band.y, TEST_W,
      TEST_COLS, band.rows, TEST_BORDER);
  });
}

// Hollow right-pointing arrow: tail bar + two shaft strokes + solid head.
// The head is HOLLOW in the frame: a ~1.5px blue outline around a white core
// (PIL: head interior at mid-height is white left of the tip strokes).
function arrowHead(pptx, slide, x, y, w, h) {
  slide.addShape(pptx.ShapeType.custGeom, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    points: [
      { x: 0, y: 0 },
      { x: px(w), y: px(h) / 2 },
      { x: 0, y: px(h) },
      { close: true },
    ],
    fill: { color: WHITE }, line: { color: BLUE, width: 1.5 },
  });
}

function arrow(pptx, slide, x, y) {
  const A = ARROW;
  const ln = { color: BLUE, width: 1.25 };
  slide.addShape(pptx.ShapeType.line, { x: px(x), y: px(y + A.shaftTop),
    w: px(A.shaft), h: 0, line: ln });
  slide.addShape(pptx.ShapeType.line, { x: px(x), y: px(y + A.shaftBot),
    w: px(A.shaft), h: 0, line: ln });
  slide.addShape(pptx.ShapeType.line, { x: px(x), y: px(y + A.shaftTop),
    w: 0, h: px(A.shaftBot - A.shaftTop), line: ln });
  arrowHead(pptx, slide, x + A.shaft, y, A.head, A.h);
}

function drawArrows(pptx, slide) {
  for (const band of ARROWS) {
    arrow(pptx, slide, band.L, band.y);
    arrow(pptx, slide, band.R, band.y);
  }
}

function drawWBoxes(pptx, slide) {
  WBOX_RECT.forEach((b, i) => {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(WBOX_W), h: px(WBOX_H),
      fill: { color: WHITE }, line: { color: RED, width: 2 },
    });
    const im = WBOX_IMG[i];
    slide.addImage({ path: im.image, x: px(im.x), y: px(im.y),
      w: px(115), h: px(123) }); // 600-dpi PNG placed at exact px/600 inches
  });
}

const BLOCKS = {
  chrome: drawChrome,
  title: drawTitle,
  labels: drawLabels,
  trainTables: drawTrainTables,
  testTables: drawTestTables,
  arrows: drawArrows,
  wBoxes: drawWBoxes,
};

function renderBase(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  const only = opts.only || null;
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (only && !only[name]) continue;
    if (!only && skip[name]) continue;
    fn(pptx, slide, opts);
  }
}

module.exports = {
  renderBase, BLOCKS,
  drawChrome, drawTitle, drawLabels, drawTrainTables, drawTestTables,
  drawArrows, drawWBoxes,
  // shared-pattern re-exports (slide 017 composes its delta from these)
  makeTrainTable: P.makeTrainTable, makeTestTable: P.makeTestTable,
  TITLE_TEXT, TITLE_BOX, LABELS, LABEL_FONT_SIZE,
  TRAIN_X, TRAIN_W, TRAIN_COLS, TRAIN_BANDS,
  TEST_X, TEST_W, TEST_COLS, TEST_BANDS,
  WBOX_RECT, WBOX_IMG, WBOX_W, WBOX_H, ARROWS, ARROW,
  TRAIN_HEADER, TEST_HEADER, TRAIN_ROWS, TEST_ROWS,
  TABLE_FONT_SIZE, TEST_HEAD_FONT_SIZE, SUBSCRIPT_SIZE,
  RED, BLUE, BLACK, WHITE, YELLOW, TRAIN_BORDER, TEST_BORDER, TEST_SHADE,
  SERIF, SANS, runsFor,
};
