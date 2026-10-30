// components/slide_017.js — BANKED composition of slide 017
// ("Adding Ridge Regularizer to the model λ=3"), ML lecture 03
// (03_ridger_regression_gradient_descent).
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide — house chrome
// (numeral 17) + the two-tone title + the one Train/Test label pair + three
// Train tables + three Test tables + two hollow blue arrows per band + three
// red-bordered W boxes (white rect + 600-dpi math image: W with red underline,
// "=", parenthesised 3-value vector, and the BLUE ||W||^2 line — 017 has NO
// pale-yellow ellipse, unlike the parent). opts:
//   { numeral }     — override the badge numeral (variant passes its own number)
//   { skip: {...} } — omit any block: chrome, title, labels, trainTables,
//                     testTables, arrows, wBoxes
//   { only: {...} } — draw ONLY the listed blocks
//
// CHILD of slide 013 (dependency edge 17 > 13) — the chain 12→13→17 composes
// transitively. The table PATTERN is IMPORTED from the certified parent
// component: makeTrainTable / makeTestTable (012's builders, re-exported by
// 013), the alternating blue/red ink rule, runsFor's real subscripts, and the
// already-measured arrow and label blocks (017's frame measures them in the
// SAME slot: arrows x464..503 / x627..666 in all three bands; label boxes
// x96..161 / x802..867 at y96..126). Nothing is copy-pasted, nothing re-derived.
//
// 017 redraws the tables at its OWN PIL-measured geometry with its OWN values:
//   - train tables: x92..459, gridlines 92 133 174 214 255 296 337 377 418 459
//     (identical slot to the parent), cell ink ci0 BLACK / odd ci BLUE / even RED
//   - test tables: x668..872 — 017 ADDS a BLACK label column (X1/X2/y) and a
//     BLANK header cell that the parent's 3-column test table does not have;
//     ink phase INVERTED vs the train table (odd ci RED / even BLUE); the y row
//     (ri 3) carries the measured mint CCFFE1 fill, the other rows stay white
//   - W boxes: x505..623, y126..251 / 264..390 / 402..527 — measured, red 2pt
// Geometry: recreated_pptx/qa/slide017/MEASUREMENTS.md (PIL, 960x540, 1px=1pt).
//
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));
// CERTIFIED PARENT COMPONENT (import, never copy).
const C = require(path.resolve(__dirname, "./slide_013.js"));

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette (qa/slide017/MEASUREMENTS.md) ───────────────────────────
const RED = C.RED;             // title ink, red table ink, W glyph, W-box border
const BLUE = C.BLUE;           // blue table ink, label fill, W norm line, arrows
const BLACK = C.BLACK;
const WHITE = C.WHITE;
const YELLOW = C.YELLOW;       // X8 outlier-cell highlight (measured 250,255,13)
const TRAIN_BORDER = C.TRAIN_BORDER; // measured gray gridlines (206,208,205)
const TEST_BORDER = C.TEST_BORDER;   // measured rose gridlines (212,188,192)
const TEST_SHADE = C.TEST_SHADE;     // measured y-row mint fill (202,255,222)
const SERIF = C.SERIF;
const SANS = C.SANS;

// Title: two ink colours, measured per word (see MEASUREMENTS.md).
// "Adding" RED, "Ridge" BLUE, "Regularizer to the model" RED, "λ=3" all BLUE
// (PIL: original's tail is one blue run; a red "=" was a defect, fixed 2026-10-24).
const TITLE_RUNS = [
  { text: "Adding ", options: { color: RED } },
  { text: "Ridge ", options: { color: BLUE } },
  { text: "Regularizer to the model  ", options: { color: RED } },
  { text: "λ=3", options: { color: BLUE } },
];
const TITLE_BOX = { x: 176, y: 62, w: 650, h: 42, fontSize: 30, lineSpacing: 34 };

// ── measured geometry (frame px) ─────────────────────────────────────────────
const TRAIN_X = 92, TRAIN_W = 367;
const TRAIN_COLS = [41, 41, 40, 41, 41, 41, 40, 41, 40]; // 92,133,174,214,255,296,337,377,418,459
const TRAIN_BANDS = [
  { y: 126, rows: [31, 31, 31, 30] },
  { y: 265, rows: [31, 31, 31, 31] },
  { y: 402, rows: [32, 31, 31, 31] },
];

// 017's test table carries a label column the parent's does not: 4 columns.
const TEST_X = 668, TEST_W = 204;
const TEST_COLS = [51, 51, 51, 51]; // 668,719,770,821,872
const TEST_BANDS = [
  { y: 128, rows: [32, 30, 31, 31] },
  { y: 266, rows: [32, 30, 31, 31] },
  { y: 403, rows: [32, 30, 31, 31] },
];

// W boxes: red 2pt border rect + math image (115x123 px at 600 dpi).
const WBOX_W = 118, WBOX_H = 125;
const WBOX_RECT = [
  { x: 505, y: 127 },
  { x: 505, y: 265 },
  { x: 505, y: 403 },
];
const WBOX_IMG = [
  { image: path.resolve(__dirname, "../assets/wbox017_band1.png"), x: 507, y: 127 },
  { image: path.resolve(__dirname, "../assets/wbox017_band2.png"), x: 507, y: 265 },
  { image: path.resolve(__dirname, "../assets/wbox017_band3.png"), x: 507, y: 403 },
];

// ── measured table content (verbatim per analysis/slide_017_final.json) ──────
const TRAIN_HEADER = ["", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"];
// 017's test table has a label column; its header cell is BLANK (measured).
const TEST_HEADER = ["", "Test1", "Test2", "Test3"];

const ROW_X2 = ["X2", 1, 3, 5, 6, 16, 7, 5, 3];
const ROW_Y = ["y", 2, 4, 6, 8, 16, 18, 20, 22];
const TRAIN_ROWS = [
  [["X1", 1, 2, 3, 4, 8, 9, 10, 11], ROW_X2, ROW_Y], // band 1: no highlight
  [["X1", 1, 2, 3, 4, 8, 9, 10, 30], ROW_X2, ROW_Y], // band 2: X8 = 30, yellow
  [["X1", 1, 2, 3, 4, 8, 9, 10, 60], ROW_X2, ROW_Y], // band 3: X8 = 60, yellow
];
const TEST_ROWS = [
  [["X1", 30, 40, 50], ["X2", 15, 20, 25], ["y", 59, 78.7, 98.4]],
  [["X1", 30, 40, 50], ["X2", 15, 20, 25], ["y", 34.1, 45.1, 56.1]],
  [["X1", 30, 40, 50], ["X2", 15, 20, 25], ["y", 26.2, 34.4, 42.5]],
];

const TABLE_FONT_SIZE = C.TABLE_FONT_SIZE;     // 20pt — measured 13-15px cap
const TEST_HEAD_FONT_SIZE = C.TEST_HEAD_FONT_SIZE;
const SUBSCRIPT_SIZE = C.SUBSCRIPT_SIZE;

// ── helpers ──────────────────────────────────────────────────────────────────
function cellStyle(color, fill, align, fontSize) {
  return {
    fontFace: SERIF, fontSize, bold: true, color, align,
    valign: "middle", fill: { color: fill },
  };
}

function buildTrainData(bi) {
  const hl = bi === 0 ? -1 : 0; // X1 row of bands 2/3 carries the yellow X8 cell
  const base = C.makeTrainTable(TRAIN_HEADER, TRAIN_ROWS[bi], hl, 8);
  return base.map((row, ri) =>
    row.map((cell, ci) => {
      const isHead = ri === 0;
      const color = ci === 0 ? BLACK : (ci % 2 === 1 ? BLUE : RED);
      const fill = cell.options.fill && cell.options.fill.color === "FFFF00" ? YELLOW : WHITE;
      const align = ci === 0 || isHead ? "left" : "center";
      return {
        text: C.runsFor(cell.text, color, TABLE_FONT_SIZE),
        options: cellStyle(color, fill, align, TABLE_FONT_SIZE),
      };
    })
  );
}

function buildTestData(bi) {
  // 017's test table has a label column, so it goes through the train-table
  // builder (the only 012 builder that models a label column).
  const base = C.makeTrainTable(TEST_HEADER, TEST_ROWS[bi], -1, -1);
  return base.map((row, ri) =>
    row.map((cell, ci) => {
      const isHead = ri === 0;
      if (ci === 0) {
        return {
          text: C.runsFor(cell.text, BLACK, TABLE_FONT_SIZE),
          options: cellStyle(BLACK, WHITE, "left", TABLE_FONT_SIZE),
        };
      }
      // measured phase: odd ci RED / even ci BLUE — the INVERSE of the train table
      const color = ci % 2 === 1 ? RED : BLUE;
      const fill = ri === 3 ? TEST_SHADE : WHITE; // y row = mint (measured)
      const fontSize = isHead ? TEST_HEAD_FONT_SIZE : TABLE_FONT_SIZE;
      const opt = cellStyle(color, fill, "center", fontSize);
      if (isHead) opt.margin = [0.03, 0.04, 0.03, 0.04];
      return { text: C.runsFor(cell.text, color, fontSize), options: opt };
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
  const n = opts && opts.numeral !== undefined ? opts.numeral : 17;
  drawHouseChrome(pptx, slide, { numeral: n });
}

function drawTitle(pptx, slide) {
  const T = TITLE_BOX;
  const runs = TITLE_RUNS.map((r) => ({
    text: r.text,
    options: Object.assign({ fontFace: SANS, fontSize: T.fontSize, bold: true }, r.options),
  }));
  slide.addText(runs, {
    x: px(T.x), y: px(T.y), w: px(T.w), h: px(T.h),
    align: "left", valign: "top", margin: 0,
    lineSpacing: T.lineSpacing,
  });
}

// Label boxes and arrows measure in the SAME slot as the parent's certified
// blocks — inherited, not redrawn (verified: MEASUREMENTS.md).
function drawLabels(pptx, slide) { C.drawLabels(pptx, slide); }
function drawArrows(pptx, slide) { C.drawArrows(pptx, slide); }

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
  // shared-pattern re-exports (718 would compose its delta from these)
  makeTrainTable: C.makeTrainTable, makeTestTable: C.makeTestTable,
  TRAIN_X, TRAIN_W, TRAIN_COLS, TRAIN_BANDS,
  TEST_X, TEST_W, TEST_COLS, TEST_BANDS,
  WBOX_RECT, WBOX_IMG, WBOX_W, WBOX_H,
  TRAIN_HEADER, TEST_HEADER, TRAIN_ROWS, TEST_ROWS,
  TABLE_FONT_SIZE, TEST_HEAD_FONT_SIZE, SUBSCRIPT_SIZE,
  RED, BLUE, BLACK, WHITE, YELLOW, TRAIN_BORDER, TEST_BORDER, TEST_SHADE,
  SERIF, SANS, TITLE_RUNS, TITLE_BOX, runsFor: C.runsFor,
};
