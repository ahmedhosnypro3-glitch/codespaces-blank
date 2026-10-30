// slide_047.js — "Check Classes of Z Vectors" (deck 03, 960x540 frame, 1px = 1pt)
//
// FRAME-VS-SPEC DEVIATIONS (frame is authority; all re-derived by direct frame reads
// + PIL measurement on 2026-10-24, worker w047 — see analysis/slide_047_final.json
// validation block):
//   * Initial W has THREE entries 4 / -2 / -2 (spec said two).
//   * BOTH matrices' class rows print C1 C1 C1 C2 C2 C2 (three of each; spec said 2+4).
//   * Augmented matrix = header + THREE data rows (spec's 4th row was a read error).
//   * Top-right Z headers are Z1 Z1 Z1 verbatim (resolved; not Z2/Z3).
//   * Calc boxes: d(Z1), d(Z2), d(Z2) (spec said all d(Z1)).
//   * Sign statements are BLACK bold (spec claimed red/blue); row vectors BLUE,
//     (14;-4;0) stacks GREEN, block title BLUE italic.
//   * Serif typeface throughout (frame is Times-like; spec said sans-serif).
//   * Measured fills: top band cream FFFFE8; content boxes white with A6ACB8 hairline;
//     red = C00000 (flat button interior median 198,0,16); blue ~1A1A99; green 008000.
//
// Geometry notes: all coordinates below are ABSOLUTE frame px (960x540) measured from
// unique_slides/slide_047.jpg with PIL. 1 frame px = 1 pt = 1/72 in.

const pptxgenpkg = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const s = pptx.addSlide();

drawHouseChrome(pptx, s, { numeral: "47" });

const FONT = "Times New Roman";
const BLACK = "000000";
const RED = "C00000";
const BLUE = "1A1A99";
const GREEN = "008000";
const CREAM = "FFFFE8";
const BOXLINE = "A6ACB8";
const ASSET = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/";

const IN = (px) => px / 72; // frame px -> inches (1px = 1pt)

function rect(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pptx.ShapeType.rect, {
    x: IN(x), y: IN(y), w: IN(w), h: IN(h),
    fill: { color: fill },
    line: { color: lineColor, width: lineW === undefined ? 0.75 : lineW },
  });
}

function img(file, x, y, w, h) {
  s.addImage({ path: ASSET + file, x: IN(x), y: IN(y), w: IN(w), h: IN(h) });
}

// centred ink-cell text (matrix digits / headers / class labels)
function cell(text, cx, cy, size, color, opts = {}) {
  const w = opts.w || 22, h = opts.h || 16;
  s.addText(text, {
    x: IN(cx - w / 2), y: IN(cy - h / 2), w: IN(w), h: IN(h),
    fontFace: FONT, fontSize: size, color: color,
    bold: !!opts.bold, italic: !!opts.italic, margin: 0,
    align: "center", valign: "middle",
  });
}

// left-aligned text whose INK box target is (x, cy)
function left(text, x, cy, w, h, size, color, opts = {}) {
  s.addText(text, {
    x: IN(x), y: IN(cy - h / 2), w: IN(w), h: IN(h),
    fontFace: FONT, fontSize: size, color: color,
    bold: !!opts.bold, italic: !!opts.italic, margin: 0,
    align: "left", valign: "middle",
  });
}

// ============================================================
// 1. TOP BAND — cream box x68..720, y55..130, dark-blue hairline
// ============================================================
rect(68, 55, 652, 75, CREAM, BLUE, 1);

// 1a. top-left data matrix: header y69, digit bands y84 / 100.5, class y118.5
{
  const CX = [96.5, 118.5, 140.5, 163, 185.5, 208];
  const PAR_X = [88.65, 110.65, 132.62, 155.09, 177.59, 200.65];
  const PAR_W = [14.72, 14.72, 15.29, 15.85, 15.85, 14.72];
  const HDR = ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"];
  const data = [[1, 1], [2, 1], [1, 2], [5, 4], [6, 5], [6, 6]];
  const klass = [1, 1, 1, 2, 2, 2];
  for (let i = 0; i < 6; i++) {
    img("paren_p047_tl2.png", PAR_X[i], 76.5, 15.24, 31.44);
    cell(HDR[i], CX[i], 65.6, 12.5, BLACK, { italic: true, w: 24 });
    cell(String(data[i][0]), CX[i], 83.6, 13.5, BLACK, { w: 18 });
    cell(String(data[i][1]), CX[i], 100.1, 13.5, BLACK, { w: 18 });
    cell(klass[i] === 1 ? "C\u2081" : "C\u2082", CX[i], 116.5, 13,
      klass[i] === 1 ? RED : BLUE, { italic: true, w: 22 });
  }
}

// 1b. top-centre: Initial W = (W bold underlined) + 3-entry vector + Step eta
s.addText([
  { text: "Initial ", options: { fontFace: FONT, fontSize: 13, color: BLACK } },
  { text: "W", options: { fontFace: FONT, fontSize: 13, color: BLACK, bold: true, underline: { style: "sng" } } },
  { text: " =", options: { fontFace: FONT, fontSize: 13, color: BLACK } },
], {
  x: IN(266), y: IN(78.5 - 8), w: IN(68), h: IN(16),
  fontFace: FONT, margin: 0, align: "left", valign: "middle",
});
// W vector: paren pair x327..353 spanning the THREE entries (y58..105)
img("paren_p047_w.png", 326, 58, 31, 47.4);
for (const r of [{ t: "4", cy: 66 }, { t: "-2", cy: 82 }, { t: "-2", cy: 97.5 }]) {
  cell(r.t, 340, r.cy, 14, BLACK, { w: 18, h: 13 });
}
// Step eta = 2 (red, measured x365..435 y67..80)
left("Step \u03b7 = 2", 365, 72, 82, 18, 17.5, RED, { bold: true, italic: true });
// Check classes of (x499..582, y79..88)
left("Check classes of", 499, 83, 94, 16, 12.5, BLACK);

// 1c. legend (x239..508, y110..123)
s.addText([
  { text: "C\u2081", options: { fontFace: FONT, fontSize: 15, color: RED } },
  { text: "  positive  ", options: { fontFace: FONT, fontSize: 15, color: BLACK } },
  { text: "C\u2082", options: { fontFace: FONT, fontSize: 15, color: BLUE } },
  { text: "negative   ", options: { fontFace: FONT, fontSize: 15, color: BLACK } },
  { text: "Zero", options: { fontFace: FONT, fontSize: 15, color: GREEN } },
  { text: " is unaccepted", options: { fontFace: FONT, fontSize: 15, color: BLACK } },
], {
  x: IN(239), y: IN(115 - 8), w: IN(280), h: IN(16),
  fontFace: FONT, margin: 0, align: "left", valign: "middle",
});

// 1d. top-right Z matrix: header y70.5, digit bands y87 / 104.5
{
  const CX = [606.5, 628, 650.5];
  const PAR_X = [597.05, 620.12, 642.12];
  const PAR_W = [16.42, 15.29, 15.29];
  const data = [[0, 0], [7, 6], [3, 2]];
  for (let i = 0; i < 3; i++) {
    img("paren_p047_z.png", PAR_X[i], 79, 16.2, 32.4);
    cell("Z\u2081", CX[i], 68.2, 12.5, BLACK, { italic: true, w: 24 });
    cell(String(data[i][0]), CX[i], 86.2, 13.5, BLACK, { w: 18 });
    cell(String(data[i][1]), CX[i], 103.5, 13.5, BLACK, { w: 18 });
  }
}

// ============================================================
// 2. MID-LEFT augmented-vectors box x69..247 y139..256
// ============================================================
rect(69, 139, 178, 117, "FFFFFF", BOXLINE, 0.75);
left("Ugmented Vectors ( from Top )", 82, 152.5, 178, 16, 13, BLUE, { italic: true });
{
  const CX = [100.5, 121.5, 144.5, 167, 189.5, 211.5];
  const PAR_X = [92.65, 113.65, 136.11, 158.58, 181.11, 203.61];
  const PAR_W = [14.72, 14.72, 15.29, 15.85, 15.29, 15.29];
  const HDR = ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"];
  const data = [[1, 1, 1], [1, 2, 1], [1, 1, 2], [1, 5, 4], [1, 6, 5], [1, 6, 6]];
  const klass = [1, 1, 1, 2, 2, 2];
  for (let i = 0; i < 6; i++) {
    img("paren_p047_aug3.png", PAR_X[i], 181, 15.24, 45.48);
    cell(HDR[i], CX[i], 167.8, 12.5, BLACK, { italic: true, w: 24 });
    cell(String(data[i][0]), CX[i], 187.7, 13.5, BLACK, { w: 18 });
    cell(String(data[i][1]), CX[i], 202.7, 13.5, BLACK, { w: 18 });
    cell(String(data[i][2]), CX[i], 217.7, 13.5, BLACK, { w: 18 });
    cell(klass[i] === 1 ? "C\u2081" : "C\u2082", CX[i], 236.7, 13,
      klass[i] === 1 ? RED : BLUE, { italic: true, w: 22 });
  }
}

// ============================================================
// 3. MID-RIGHT calculation boxes (x273..855)
//    box1 y139..198 | box2 y206..264 | box3 y271..330
//    per-box offsets measured: box2 = box1 + 69, box3 = box1 + 135
// ============================================================
const boxes = [
  { top: 139, h: 59, dy: 0,   label: "d(Z\u2081) =", row: "(1  0  0)", result: "= 14",  sign: "\u21d2 Positive > 0", cls: "Class I",  clsColor: RED,  clsX: 663 },
  { top: 206, h: 58, dy: 69,  label: "d(Z\u2082) =", row: "(1  7  6)", result: "= -14", sign: "\u21d2 Negative < 0", cls: "Class II", clsColor: BLUE, clsX: 677 },
  { top: 271, h: 59, dy: 135, label: "d(Z\u2082) =", row: "(1  3  2)", result: "= -2",  sign: "\u21d2 Negative < 0", cls: "Class II", clsColor: BLUE, clsX: 670 },
];
for (const b of boxes) {
  rect(273, b.top, 582, b.h, "FFFFFF", BOXLINE, 0.75);
  // d(Z) = label: ink x283..323, band centre 168 (+dy)
  left(b.label, 283, 166.4 + b.dy, 52, 18, 14, BLACK, { italic: true });
  // blue row vector: ink x335..375, band centre 153 (+dy)
  left(b.row, 335, 152 + b.dy, 50, 16, 13, BLUE);
  // green stacked column (14; -4; 0): parens x388..405 y150..188 (+dy)
  img("paren_p047_stack.png", 388, 150 + b.dy, 18.24, 39.48);
  cell("14", 397, 153.5 + b.dy, 10.5, GREEN, { w: 16, h: 12 });
  cell("-4", 397, 167 + b.dy, 10.5, GREEN, { w: 16, h: 12 });
  cell("0",  397, 184 + b.dy, 10.5, GREEN, { w: 16, h: 12 });
  // result: ink x414..435, band centre 166.5 (+dy)
  left(b.result, 414, 166.2 + b.dy, 40, 16, 13.5, BLACK);
  // sign statement: black bold, ONE line, ink starts x508 (arrow glyph)
  left(b.sign, 507, 166.5 + b.dy, 100, 16, 14, BLACK, { bold: true });
  // class outcome
  left(b.cls, b.clsX, 166 + b.dy, 50, 16, 13, b.clsColor, { bold: true });
}

// ============================================================
// 4. BOTTOM-LEFT red button x79..238 y278..304
// ============================================================
rect(79, 278, 160, 27, RED, RED, 0.5);
s.addText("Check Classes", {
  x: IN(79), y: IN(278), w: IN(160), h: IN(27),
  fontFace: FONT, fontSize: 23, color: "FFFFFF", bold: true,
  align: "center", valign: "middle", margin: 0,
});

pptx.writeFile({ fileName: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_047_recreated.pptx" })
  .then((f) => console.log("WROTE " + f));
