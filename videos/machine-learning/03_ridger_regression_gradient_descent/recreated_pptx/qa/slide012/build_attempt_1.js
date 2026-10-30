// Build slide 012 — "Effect of Overfitting on model parameter "W""
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// House chrome: shared_patterns/house_chrome.js
//
// GROUND TRUTH: unique_slides/slide_012.jpg (960x540, 1px = 1pt = 1/72 in).
// All measurements from frame via PIL analysis (scratch/tmp/measure_012.py).
// Frame measurements used directly — spec percent positions were approximate.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_012_recreated.pptx");

const px = (v) => v / 72; // frame px -> inches (1px = 1pt)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome (panel + L/R/bottom strokes, NO top stroke, badge numeral 12).
drawHouseChrome(pptx, slide, { numeral: 12 });

// ── COLOR PALETTE ──────────────────────────────────────────────────────────────
const RED     = "FF0000";  // title, red labels, Again callout, arrow
const BLUE    = "0000FF";  // blue labels, table headers, y-row values, question box
const BLACK   = "000000";  // table X1/X2 row values
const WHITE   = "FFFFFF";  // label text, question box fill
const YELLOW  = "FFFF00";  // outlier cell highlight
const FONT    = "Arial";

// ── HELPERS ────────────────────────────────────────────────────────────────────
function labelBox(x, y, w, h, fill, text, fontSize = 14) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill },
  });
  slide.addText(text, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: fontSize, bold: true, color: WHITE,
    lineSpacing: fontSize * 1.2,
  });
}

function calloutBox(x, y, w, h, fill, textLines, fontSize = 13) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill },
  });
  const totalH = textLines.length * fontSize * 1.2;
  const y0 = y + (h - totalH) / 2;
  textLines.forEach((line, i) => {
    slide.addText(line, {
      x: px(x), y: px(y0 + i * fontSize * 1.2), w: px(w), h: px(fontSize * 1.2),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: fontSize, bold: true, color: WHITE,
      lineSpacing: fontSize * 1.2,
    });
  });
}

// ── TITLE ──────────────────────────────────────────────────────────────────────
// Measured ink: x154..788 (center 471), y67..98 (h=32). Cap top row 67, baseline ~90.
slide.addText('Effect of Overfitting on model parameter \u201cW\u201d', {
  x: px(160), y: px(70), w: px(640), h: px(40),
  align: "left", valign: "top", margin: 0,
  fontFace: FONT, fontSize: 28, bold: true, color: RED,
  lineSpacing: 34,
});

// ── LEFT LABEL COLUMN ──────────────────────────────────────────────────────────
// x 60..200 (w=140), aligned with table left edge (x203).
// 1. Training Data (blue): measured blue band rows 104..133
labelBox(60, 110, 140, 30, BLUE, "Training Data", 14);

// 2. Perfect Data / Y follows x1 (red): measured red band rows 173..222
labelBox(60, 175, 140, 50, RED, "Perfect Data\nY follows x1", 14);

// 3. x8 is Outlier (red): measured red band rows 321..350
labelBox(60, 325, 140, 30, RED, "x8 is Outlier", 14);

// 4. x8 is Outlier (red): measured red band rows 444..473
labelBox(60, 450, 140, 30, RED, "x8 is Outlier", 14);

// ── TABLES ─────────────────────────────────────────────────────────────────────
// Table styling: header + row labels bold BLUE; X1/X2 values BLACK; y-row values BLUE
// Outlier highlight: yellow fill on X8 column of X1 row.

// Perfect training table: x203..571 (w=368), y127..265 (h=138)
// 9 columns (row-label + X1..X8), 4 rows (header, X1, X2, y)
// Measured vertical grid: 203, 244, 285, 326, 367, 407, 448, 489, 530, 571
// Col widths: [41, 41, 41, 41, 40, 41, 41, 41, 41]
// Measured horizontal grid: 127, 158, 189, 219, 249, 265
// Row gaps: 31, 31, 30, 30, 16(border). Interior row heights: [31, 31, 30, 30]

const trainCols = [41, 41, 41, 41, 40, 41, 41, 41, 41];
const trainRows = [31, 31, 30, 30];

// First outlier table: y265..404. Measured horizontal: 265, 296, 327, 358, 388, 404
// Row gaps: 31, 31, 31, 30, 16(border). Interior: [31, 31, 30, 30]
const outlier1Rows = [31, 31, 30, 30];

// Second outlier table: y404..496. Measured horizontal: 404, 435, 465, 496
// Row gaps: 31, 30, 31 (only 3 intervals visible for 4 rows). Use equal 23px each for 4 rows = 92px
const outlier2Rows = [23, 23, 23, 23];

// Test table: y130..252 (h=122). Measured horizontal: 130, 160, 221, 252
// Row gaps: 30, 61, 31 (irregular). Use equal 30.5 -> [30, 30, 31, 31] = 122
const testRows = [30, 30, 31, 31];

function makeTrainTable(header, rows, highlightCol = -1, highlightRow = -1) {
  // highlightRow: 0=X1 data row, 1=X2 data row, 2=y data row (header is separate)
  const result = [];
  result.push(header.map((h, ci) => ({
    text: h, options: { bold: true, color: BLUE, fontFace: FONT, fontSize: 11, margin: 2 }
  })));
  rows.forEach((row, ri) => {
    // ri: 0=X1, 1=X2, 2=y
    result.push(row.map((cell, ci) => {
      const isHeader = ci === 0;
      // Highlight applies to DATA rows only (ri 0,1,2 map to result rows 1,2,3)
      const isHighlight = (ci === highlightCol && ri === highlightRow);
      let color = BLACK;
      if (isHeader) color = BLUE;
      else if (ri === 2) color = BLUE; // y row (index 2)
      const opts = { bold: isHeader, color: color, fontFace: FONT, fontSize: 11, margin: 2 };
      if (isHighlight) opts.fill = { color: YELLOW };
      return { text: String(cell), options: opts };
    }));
  });
  return result;
}

function makeTestTable(header, rows) {
  const result = [];
  result.push(header.map((h, ci) => ({
    text: h, options: { bold: true, color: BLUE, fontFace: FONT, fontSize: 11, margin: 2 }
  })));
  rows.forEach((row, ri) => {
    result.push(row.map((cell, ci) => {
      const isHeader = ci === 0;
      const isYRow = ri === 2;
      let color = isYRow ? BLUE : BLACK;
      if (isHeader) color = BLUE;
      return { text: String(cell), options: { bold: isHeader, color: color, fontFace: FONT, fontSize: 11, margin: 2 } };
    }));
  });
  return result;
}

const perfectTrainHeader = ["", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"];
const perfectTrainRows = [
  ["X1", 1, 2, 3, 4, 8, 9, 10, 11],
  ["X2", 1, 3, 5, 6, 16, 7, 5, 3],
  ["y",  2, 4, 6, 8, 16, 18, 20, 22],
];
const outlier1TrainRows = [
  ["X1", 1, 2, 3, 4, 8, 9, 10, 30],
  ["X2", 1, 3, 5, 6, 16, 7, 5, 3],
  ["y",  2, 4, 6, 8, 16, 18, 20, 22],
];
const outlier2TrainRows = [
  ["X1", 1, 2, 3, 4, 8, 9, 10, 60],
  ["X2", 1, 3, 5, 6, 16, 7, 5, 3],
  ["y",  2, 4, 6, 8, 16, 18, 20, 22],
];

// Perfect table
const trainTableData = makeTrainTable(perfectTrainHeader, perfectTrainRows);
slide.addTable(trainTableData, {
  x: px(203), y: px(127), w: px(368), h: px(138),
  colW: trainCols.map(px), rowH: trainRows.map(px),
  fontFace: FONT, fontSize: 11, border: { pt: 1, color: "000000" },
  autoFit: false,
});

// ── Test Data ──
// Blue label box: measured x767..866 (w=100), y100..152 (h=52) -> use x=780, y=115, w=100, h=30
labelBox(780, 115, 100, 30, BLUE, "Test Data", 14);

// Test Data table: measured x720..872 (w=152), rows ~130..252 (h=122)
// Vertical grid: 719/720, 770, 821, 872. Spec data has Test1, Test2, Test3 headers.
// The frame shows only 3 interior lines -> 4 columns implied. Use equal 38px cols,
// interior row heights [30, 30, 31, 31] (sum 122) to land the internal grid on rows 160/190/221/251.

const testHeader = ["", "Test1", "Test2", "Test3"];
const testRowsData = [
  ["X1", 30, 40, 50],
  ["X2", 15, 20, 25],
  ["y",  60, 80, 100],
];
const testTableData = makeTestTable(testHeader, testRowsData);
slide.addTable(testTableData, {
  x: px(720), y: px(130), w: px(152), h: px(122),
  colW: Array(4).fill(px(38)),
  rowH: testRows.map(px),
  fontFace: FONT, fontSize: 11, border: { pt: 1, color: "000000" },
  autoFit: false,
});

// ── First Outlier Table ──
// Measured: x203..571, y265..404 (h=139)
// Horizontal: 265, 296, 327, 358, 388, 404 -> row gaps: 31, 31, 31, 30, 16(border)
// Interior row heights: [31, 31, 30, 30] (sum=122) + borders = 139
const outlier1TableData = makeTrainTable(perfectTrainHeader, outlier1TrainRows, 8, 0); // X8 col (index 8), X1 data row (ri=0)
slide.addTable(outlier1TableData, {
  x: px(203), y: px(265), w: px(368), h: px(139),
  colW: trainCols.map(px), rowH: outlier1Rows.map(px),
  fontFace: FONT, fontSize: 11, border: { pt: 1, color: "000000" },
  autoFit: false,
});

// ── Again Callout ──
// Measured red band: x706..837 (w=132), y269..318 (h=50), centered at y~293
calloutBox(706, 275, 132, 45, RED, ["Again", "Y follows x1"], 13);

// ── Arrow ──
// Red curved arrow from Again callout (left edge ~706) pointing left to middle table (right edge ~571)
// At y ~293 (center of Again callout). Draw as line with arrowhead.
const arrowY = 293;
slide.addShape(pptx.ShapeType.line, {
  x: px(571), y: px(arrowY), w: px(706 - 571), h: 0,
  line: { color: RED, width: 2, endArrowType: "triangle" },
});

// ── Second Outlier Table ──
// Measured: x203..571, y404..496 (h=92) — compressed vertically in original
// Frame horizontal lines: 404, 435, 465, 496 (3 gaps of 31/30/31 for 4 rows).
const outlier2Rows4 = [23, 23, 23, 23]; // 92/4

const outlier2TableData = makeTrainTable(perfectTrainHeader, outlier2TrainRows, 8, 0); // X8 col, X1 data row
slide.addTable(outlier2TableData, {
  x: px(203), y: px(404), w: px(368), h: px(92),
  colW: trainCols.map(px), rowH: outlier2Rows4.map(px),
  fontFace: FONT, fontSize: 11, border: { pt: 1, color: "000000" },
  autoFit: false,
});

// ── Question Callout ──
// Measured box borders: horizontal gray/blue lines at rows 366-367 and 414-415,
// spanning x603..869 (w=267). Box = x603..869, y366..415 (h=50). White fill, blue border.
// Text (blue, 2 lines): line 1 rows 374..387, line 2 rows 394..406.
const qBoxX = 603, qBoxY = 366, qBoxW = 267, qBoxH = 50;
slide.addShape(pptx.ShapeType.rect, {
  x: px(qBoxX), y: px(qBoxY), w: px(qBoxW), h: px(qBoxH),
  fill: { color: WHITE }, line: { color: BLUE, width: 2 },
});
slide.addText("What will be the effect of X8 Outlier values on the trained model ???", {
  x: px(qBoxX + 8), y: px(qBoxY + 6), w: px(qBoxW - 16), h: px(qBoxH - 12),
  align: "left", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 11, color: BLUE, bold: false,
  lineSpacing: 14,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));