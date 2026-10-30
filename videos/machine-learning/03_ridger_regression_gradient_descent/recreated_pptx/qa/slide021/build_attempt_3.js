// slide_021.js — "Inverse Problem of Singular Matrix" (slide 21)
// ML lecture 03: Ridge Regression & Gradient Descent. Root slide (no deps).
// Ground truth: PIL-measured from unique_slides/slide_021.jpg (960x540, 1px=1pt).
// Measurement bank: recreated_pptx/qa/slide021/measure_mine.py + measure_tables.py
//
// KEY MEASUREMENTS (frame px):
// Title: red ink x290..708 y77..101, center (499, 89), cap h=19px (~26pt Liberation Serif Bold)
// House chrome: house_chrome.js (panel E9E9E7 x54..903 y45..540, C00000 strokes L/R/B, badge "21")
// Three content panels (blue #0000FF ~1pt stroke, white fill on gray house panel).
// Measured 2026-10-23 (scratch/tmp/measure_strokes.py → qa/slide021/measure_strokes_out.txt)
// from the original frame with a blueish mask (b-r>25) that catches the anti-aliased
// 2px strokes:
//   LEFT vertical cols 75-77 (core 76 — a solid (46,36,123) column, full block height);
//   RIGHT vertical: B1 x884-886, B2/B3 x886-889;
//   TOP/BOTTOM rules 2-3px rows: B1 128-130 / 255-257, B2 288-290 / 415-418,
//   B3 437-439 / 527-529. All three blocks are CLOSED rectangles.
// Tables (3x3 each, gridlines gray ~#6D6F6C):
//   TOP:    x98..302, y174..226. Cols [98,166,234,302], Rows [174,191,209,226]
//   MID:    x90..294, y342..395. Cols [90,158,226,294], Rows [342,360,377,395]
//   BOT:    x422..625, y458..511. Cols [422,490,558,625], Rows [458,475,493,511]
// Chain text (right side of P1/P2):
//   P1: "|X^T X| = 0" → arrow → "Singular Matrix" → arrow → "No Inverse" (red italic)
//   P2: "|X^T X| = 5685" → arrow → "Non-Singular Matrix" → arrow → "Inverse Exists" (red italic)
// Bottom: "(X^T X + λI)^-1" → long arrow → inverse matrix table
// Colors: RED=C00000, BLUE=0000FF, GREEN=008000, YELLOW=FFFF00 (diag), GRID=909090

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_021_recreated.pptx");
const ASSETS = path.resolve(__dirname, "assets");

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt = 1/72 in)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes, NO top stroke, badge "21"
drawHouseChrome(pptx, slide, { numeral: 21 });

// ── Palette ─────────────────────────────────────────────────────────────────────
const RED   = "C00000"; // title, labels, conclusions
const BLUE  = "0000FF"; // panel borders, arrows, λI parts
const GREEN = "008000"; // λ=3
const YELLOW= "FFFF00"; // diagonal highlights
const GRID  = "909090"; // table gridlines (frame cores ~109-144)
const BLACK = "000000"; // table digits, chain text
const WHITE = "FFFFFF"; // panel fill
const FONT_SERIF = "Liberation Serif"; // Times-like serif (available)
const FONT_SANS  = "Liberation Sans";  // Arial metric twin

// ── Helpers ────────────────────────────────────────────────────────────────────
// pptxgenjs has no {color:"none"}: a non-hex fill falls back to 000000. Omit the
// fill/line keys entirely for no-fill / no-line rects.
const rect = (x, y, w, h, fill, line) =>
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    ...(fill ? { fill: { color: fill } } : {}),
    ...(line ? { line: { color: line.color, width: line.width } } : {}),
  });

// Arrow with a triangular head at the END point (pptxgenjs line.endArrowType).
const arrow = (x0, y0, x1, y1, color, width) =>
  slide.addShape(pptx.ShapeType.line, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: color, width: width, endArrowType: "triangle" },
  });

// ── 1. TITLE ──────────────────────────────────────────────────────────────────
// Ink center (499, 89). Cap height 19px → ~26pt. Text: "Inverse Problem of Singular Matrix"
slide.addText("Inverse Problem of Singular Matrix", {
  x: px(499 - 320), y: px(89 - 15), w: px(640), h: px(40),
  align: "center", valign: "middle",
  fontSize: 26, bold: true, color: RED, fontFace: FONT_SERIF, margin: 0,
});

// ── 2. THREE CONTENT PANELS ──────────────────────────────────────────────────
// Measured geometry (see header): B1 y129..257 x76..886, B2 y288..418 x76..889,
// B3 y437..530 x76..889. Stroke width 1pt ≈ the original's 2px blue rules.
const PANELS = [
  { name: "P1", x: 76, y: 129, w: 810, h: 129 }, // top
  { name: "P2", x: 76, y: 288, w: 813, h: 130 }, // middle (rule lands y418)
  { name: "P3", x: 76, y: 437, w: 813, h: 93 },  // bottom
];

for (const p of PANELS) {
  // White fill on top of house gray panel, then a blue 1pt border rect on top
  rect(p.x, p.y, p.w, p.h, WHITE);
  rect(p.x, p.y, p.w, p.h, null, { color: BLUE, width: 1 });
}

// ── 3. TOP PANEL (P1) ─────────────────────────────────────────────────────────
const P1 = PANELS[0];

// 3a. Left label: "X^T X" (red) above matrix — use equation PNG
// Label bbox measured: x98..120, y134..153. Place PNG so its ink aligns.
// PNG eq_021_xtx: w_px=374, h_px=185, baseline=177 from top.
// We want ink baseline at y~150 (label vertical center), left at x~100.
{
  const png = "eq_021_xtx.png";
  const w_in = 374/600, h_in = 185/600;
  const baseline_frac = 177/185;
  // Target: ink left ~100, baseline ~150
  const x = px(100 - 8); // 8px padding from render_eq.py
  const y = px(150 - 177); // baseline - baseline_px
  slide.addImage({ path: path.join(ASSETS, png), x, y, w: w_in, h: h_in });
}

// 3b. Top matrix table (3x3)
// Cell boundaries: cols [98,166,234,302], rows [174,191,209,226]
// Table top-left: (98, 174), cell widths: 68, 68, 68, cell heights: 17, 18, 17
const topTableData = [
  [{ text: "14", options: { color: BLACK } }, { text: "10", options: { color: BLACK } }, { text: "15", options: { color: BLACK } }],
  [{ text: "10", options: { color: BLACK } }, { text: "40", options: { color: BLACK } }, { text: "46", options: { color: BLACK } }],
  [{ text: "20", options: { color: BLACK } }, { text: "80", options: { color: BLACK } }, { text: "92", options: { color: BLACK } }],
];
slide.addTable(topTableData, {
  x: px(98), y: px(174), w: px(204), h: px(52),
  fontFace: FONT_SERIF, fontSize: 14, color: BLACK,
  align: "center", valign: "middle",
  border: [{ type: "solid", color: GRID, pt: 1 }],
  row: { h: px(52/3) },
});

// 3c. Right chain: "|X^T X| = 0" → arrow → "Singular Matrix" → arrow → "No Inverse"
// Chain vertical center ~y192..211. Baseline ~200.
// |X^T X| = 0 PNG: w=581px, h=171px, baseline=131. Place at x~330 (left of Singular Matrix)
{
  const png = "eq_021_det0.png";
  const w_in = 581/600, h_in = 171/600;
  const baseline_px = 131;
  // Target baseline y=200, left x=330
  const x = px(330 - 8);
  const y = px(200 - baseline_px);
  slide.addImage({ path: path.join(ASSETS, png), x, y, w: w_in, h: h_in });
}
// Arrow 1: from eq0 right edge (~x330+0.97in=330+70=400) to Singular Matrix left (~x462)
// Measured arrow1 bbox x430..462
arrow(430, 200, 462, 200, BLACK, 1.5);
// "Singular Matrix" text: measured bbox x462..600, y192..211. Center ~531, baseline ~200
slide.addText("Singular Matrix", {
  x: px(462), y: px(200 - 10), w: px(140), h: px(20),
  align: "left", valign: "middle",
  fontSize: 16, color: BLACK, fontFace: FONT_SERIF, margin: 0,
});
// Arrow 2: from Singular Matrix right (~x600) to No Inverse left (~x705)
// Measured arrow2 bbox x612..623
arrow(612, 200, 650, 200, BLACK, 1.5);
// "No Inverse" red italic: measured bbox x705..794, y193..207. Center ~750, baseline ~200
slide.addText("No Inverse", {
  x: px(705), y: px(200 - 10), w: px(90), h: px(20),
  align: "left", valign: "middle",
  fontSize: 16, bold: false, italic: true, color: RED, fontFace: FONT_SERIF, margin: 0,
});

// ── 4. MIDDLE PANEL (P2) ──────────────────────────────────────────────────────
const P2 = PANELS[1];

// 4a. Left label: "(X^T X + λI)" with λ=3
// "(X^T X + λI)" PNG (blue): w=862px, h=209px, baseline=177
// Measured paren+red bbox x100..120 y301..322, lambda blue x175..220 y290..320
// Target: baseline ~310 (middle of label), left x~95
{
  const png = "eq_021_regmat.png";
  const w_in = 862/600, h_in = 209/600;
  const baseline_px = 177;
  const x = px(95 - 8);
  const y = px(310 - baseline_px);
  slide.addImage({ path: path.join(ASSETS, png), x, y, w: w_in, h: h_in });
}
// "λ=3" PNG (green): w=298px, h=107px, baseline=97
// Measured green bbox x247..305 y287..319. Place to the right of regmat
{
  const png = "eq_021_lambda3.png";
  const w_in = 298/600, h_in = 107/600;
  const baseline_px = 97;
  // Place at x~240 (right of regmat), baseline ~310
  const x = px(240 - 8);
  const y = px(310 - baseline_px);
  slide.addImage({ path: path.join(ASSETS, png), x, y, w: w_in, h: h_in });
}

// 4b. Middle matrix table (3x3) with yellow diagonal
// Cell boundaries: cols [90,158,226,294], rows [342,360,377,395]
// Cell widths: 68, 68, 68. Heights: 18, 17, 18
const midTableData = [
  [
    { text: "17", options: { color: BLACK, fill: { color: YELLOW } } },
    { text: "10", options: { color: BLACK } },
    { text: "15", options: { color: BLACK } },
  ],
  [
    { text: "10", options: { color: BLACK } },
    { text: "43", options: { color: BLACK, fill: { color: YELLOW } } },
    { text: "46", options: { color: BLACK } },
  ],
  [
    { text: "20", options: { color: BLACK } },
    { text: "80", options: { color: BLACK } },
    { text: "95", options: { color: BLACK, fill: { color: YELLOW } } },
  ],
];
slide.addTable(midTableData, {
  x: px(90), y: px(342), w: px(204), h: px(53),
  fontFace: FONT_SERIF, fontSize: 14, color: BLACK,
  align: "center", valign: "middle",
  border: [{ type: "solid", color: GRID, pt: 1 }],
  row: { h: px(53/3) },
});

// 4c. Right chain: "|X^T X| = 5685" → arrow → "Non-Singular Matrix" → arrow → "Inverse Exists"
// |X^T X| = 5685 PNG (red): w=833px, h=171px, baseline=131
// Measured eq5685 red bbox x344..350, dark x389..430 y358..377. Baseline ~367
{
  const png = "eq_021_det5685.png";
  const w_in = 833/600, h_in = 171/600;
  const baseline_px = 131;
  const x = px(330 - 8);
  const y = px(367 - baseline_px);
  slide.addImage({ path: path.join(ASSETS, png), x, y, w: w_in, h: h_in });
}
// Arrow 1: measured x450..463 at y~367
arrow(450, 367, 480, 367, BLACK, 1.5);
// "Non-Singular Matrix": measured x517..680 y359..377. Center ~598, baseline ~367
slide.addText("Non-Singular Matrix", {
  x: px(517), y: px(367 - 10), w: px(165), h: px(20),
  align: "left", valign: "middle",
  fontSize: 16, color: BLACK, fontFace: FONT_SERIF, margin: 0,
});
// Arrow 2: measured x680..691 at y~367
arrow(680, 367, 715, 367, BLACK, 1.5);
// "Inverse Exists" red italic: measured x761..876 y359..373. Center ~818, baseline ~367
slide.addText("Inverse Exists", {
  x: px(761), y: px(367 - 10), w: px(115), h: px(20),
  align: "left", valign: "middle",
  fontSize: 16, italic: true, color: RED, fontFace: FONT_SERIF, margin: 0,
});

// ── 5. BOTTOM PANEL (P3) ──────────────────────────────────────────────────────
const P3 = PANELS[2];

// 5a. Left expression: "(X^T X + λI)^-1" PNG (blue): w=1057px, h=209px, baseline=177
// Measured paren+red x165..205 y466..488, plus x218..226, lambda x238..262, sup x~270
// Target baseline ~475 (vertical center of panel), left x~150
{
  const png = "eq_021_invexpr.png";
  const w_in = 1057/600, h_in = 209/600;
  const baseline_px = 177;
  const x = px(150 - 8);
  const y = px(475 - baseline_px);
  slide.addImage({ path: path.join(ASSETS, png), x, y, w: w_in, h: h_in });
}

// 5b. Long arrow from expression right edge to table left edge
// Expression right edge ~ x150 + 1.76in = x150 + 127 = x277
// Table left edge x422
// Arrow spans ~x277 to x422 at vertical center y~475
arrow(277, 475, 422, 475, BLACK, 2);

// 5c. Inverse matrix table (3x3)
// Cell boundaries: cols [422,490,558,625], rows [458,475,493,511]
// Widths: 68, 68, 67. Heights: 17, 18, 18
const botTableData = [
  [{ text: "0.07", options: { color: BLACK } }, { text: "0.04", options: { color: BLACK } }, { text: "-0.03", options: { color: BLACK } }],
  [{ text: "-0.01", options: { color: BLACK } }, { text: "0.23", options: { color: BLACK } }, { text: "-0.11", options: { color: BLACK } }],
  [{ text: "-0.01", options: { color: BLACK } }, { text: "-0.2", options: { color: BLACK } }, { text: "0.11", options: { color: BLACK } }],
];
slide.addTable(botTableData, {
  x: px(422), y: px(458), w: px(203), h: px(53),
  fontFace: FONT_SERIF, fontSize: 13, color: BLACK,
  align: "center", valign: "middle",
  border: [{ type: "solid", color: GRID, pt: 1 }],
  row: { h: px(53/3) },
});

// ── Write ──────────────────────────────────────────────────────────────────────
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));