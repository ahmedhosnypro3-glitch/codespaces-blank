// Build slide 013 — "Effect of Overfitting on model parameter "W""
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// CHILD of slide 012 (dependency edge 13 > 12). The composition lives in the
// shared component components/slide_013.js, which imports the certified parent
// component (table PATTERN) and redraws it at 013's own measured geometry.
// This script is only the writer.
//
// 2026-10-31 fix (rejudge r18 BLOCKER, PIL-confirmed): the original's three
// TEST tables carry a row-label column (empty header cell; X1/X2/y dark
// non-bold, left-aligned, white-filled, x669..719). The component ships a
// label-less variant; this writer skips its testTables block and redraws the
// tables at the original's measured x669 w204, cols [50,51,51,51].
//
// Run: cd <project root> && NODE_PATH=$(npm root -g) node <this file>
const path = require("path");
const pptxgen = require("pptxgenjs");
const C = require(path.resolve(__dirname, "./components/slide_013.js"));

const OUT = path.resolve(__dirname, "../slide_013_recreated.pptx");

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// Measured on unique_slides/slide_013.jpg: TEST table x669..873 (label col
// x669..719 + three 51px value columns); bands/rows unchanged from component.
const TEST_X = 669, TEST_W = 204;
const TEST_COLS = [50, 51, 51, 51];
const TEST_LABELS = ["X1", "X2", "y"];

function labelRuns(text, color, fontSize) {
  const m = /^(X)([1-8])$/.exec(String(text));
  if (!m) return String(text);
  return [
    { text: m[1], options: { fontFace: C.SERIF, fontSize, bold: false, color } },
    { text: m[2], options: { fontFace: C.SERIF, fontSize: C.SUBSCRIPT_SIZE, bold: false, color, charSpacing: -0.5 } },
  ];
}

function buildTestData(bi) {
  const head = ["", "Test1", "Test2", "Test3"].map((h, ci) => ({
    text: ci === 0 ? "" : C.runsFor(h, ci % 2 === 1 ? C.RED : C.BLUE, C.TEST_HEAD_FONT_SIZE),
    options: {
      fontFace: C.SERIF, fontSize: C.TEST_HEAD_FONT_SIZE, bold: true,
      color: ci % 2 === 1 ? C.RED : C.BLUE, align: "center", valign: "middle",
      fill: { color: C.WHITE }, margin: [0.03, 0.04, 0.03, 0.04],
    },
  }));
  const body = C.TEST_ROWS[bi].map((vals, ri) =>
    [TEST_LABELS[ri], ...vals].map((v, ci) => {
      const isLabel = ci === 0;
      const color = isLabel ? C.BLACK : (ci % 2 === 1 ? C.RED : C.BLUE);
      const fill = ri === 2 ? C.TEST_SHADE : C.WHITE; // y row = mint (all bands)
      return {
        text: isLabel ? labelRuns(v, color, C.TABLE_FONT_SIZE) : C.runsFor(v, color, C.TABLE_FONT_SIZE),
        options: {
          fontFace: C.SERIF, fontSize: isLabel ? C.TABLE_FONT_SIZE : C.TABLE_FONT_SIZE,
          bold: !isLabel, color, align: isLabel ? "left" : "center",
          valign: "middle", fill: { color: fill },
        },
      };
    })
  );
  return [head, ...body];
}

function drawTestTables(pptx, slide) {
  C.TEST_BANDS.forEach((band, bi) => {
    slide.addTable(buildTestData(bi), {
      x: px(TEST_X), y: px(band.y), w: px(TEST_W),
      h: px(band.rows.reduce((a, b) => a + b, 0)),
      colW: TEST_COLS.map(px), rowH: band.rows.map(px),
      fontFace: C.SERIF, fontSize: C.TABLE_FONT_SIZE,
      border: { pt: 1.25, color: C.TEST_BORDER },
      autoFit: false,
    });
  });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

C.renderBase(pres, slide, { numeral: 13, skip: { testTables: true } });
drawTestTables(pres, slide);

pres.writeFile({ fileName: OUT })
  .then((f) => console.log("wrote " + f))
  .catch((e) => { console.error(e); process.exit(1); });
