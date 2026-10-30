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
//   * (2026-10-26 founder directive) ALL parentheses straightened: the paren_p047_*
//     PNG pairs and the row-vector font parens are replaced by straight 1px-rect
//     bars (dbar()) at measured bulge centers, per-region colors.
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
// straight delimiter bars (founder directive 2026-10-26: no curved parentheses);
// colors measured per region from the original frame
const PAREN_LT = "A6A6A6"; // triplet + stack columns (~(181,199,181) probes)
const PAREN_MD = "909090"; // matrix cell pairs (~(139,144,144) probes)
const PAREN_DK = "6E6E6E"; // Initial-W vector (~(109,112,112) probes)

const IN = (px) => px / 72; // frame px -> inches (1px = 1pt)

function rect(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pptx.ShapeType.rect, {
    x: IN(x), y: IN(y), w: IN(w), h: IN(h),
    fill: { color: fill },
    line: { color: lineColor, width: lineW === undefined ? 0.75 : lineW },
  });
}

// straight delimiter bar — the certified 1px-rect idiom (build/slide_045.js)
function dbar(x, y, h, color) {
  s.addShape(pptx.ShapeType.rect, {
    x: IN(x), y: IN(y), w: IN(1), h: IN(h),
    fill: { color: color }, line: { type: "none" },
  });
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
  // straight paren bars per column (measured bulge centers)
  const BAR_L = [89.81, 111.45, 133.54, 156.30, 178.75, 201.69];
  const BAR_R = [100.50, 122.84, 145.10, 168.06, 189.78, 212.36];
  const HDR = ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"];
  const data = [[1, 1], [2, 1], [1, 2], [5, 4], [6, 5], [6, 6]];
  const klass = [1, 1, 1, 2, 2, 2];
  for (let i = 0; i < 6; i++) {
    dbar(BAR_L[i], 77, 31, PAREN_MD);
    dbar(BAR_R[i], 77, 31, PAREN_MD);
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
// W vector: straight delimiter bars x330.5/352.0 spanning the THREE entries (y57..107)
dbar(330.5, 57, 50, PAREN_DK);
dbar(352.0, 57, 50, PAREN_DK);
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
  const BAR_L = [598.06, 621.45, 643.03];
  const BAR_R = [609.92, 632.78, 654.45];
  const data = [[0, 0], [7, 6], [3, 2]];
  for (let i = 0; i < 3; i++) {
    dbar(BAR_L[i], 80, 32, PAREN_MD);
    dbar(BAR_R[i], 80, 32, PAREN_MD);
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
  const BAR_L = [93.27, 114.66, 137.11, 159.49, 182.17, 204.63];
  const BAR_R = [105.67, 126.09, 149.00, 171.29, 193.88, 215.93];
  const HDR = ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"];
  const data = [[1, 1, 1], [1, 2, 1], [1, 1, 2], [1, 5, 4], [1, 6, 5], [1, 6, 6]];
  const klass = [1, 1, 1, 2, 2, 2];
  for (let i = 0; i < 6; i++) {
    dbar(BAR_L[i], 180, 46, PAREN_MD);
    dbar(BAR_R[i], 180, 46, PAREN_MD);
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
  // blue row-vector digits at measured centroids cx 336/353.5/369.5 (cy 153.5+dy),
  // flanked by straight paren bars x330/x378 (replaces the curved font parens)
  dbar(330.0, 147 + b.dy, 13, PAREN_LT);
  dbar(378.0, 148 + b.dy, 12, PAREN_LT);
  b.row.replace(/[()]/g, "").trim().split(/\s+/).forEach((d, k) =>
    cell(d, [336, 353.5, 369.5][k], 153.5 + b.dy, 13, BLUE, { w: 14 }));
  // green stacked column (14; -4; 0): straight delimiter bars x380.9/403.95, y145..(+dy)
  dbar(380.9, 145 + b.dy, b.dy === 135 ? 47 : 48, PAREN_LT);
  dbar(403.95, 145 + b.dy, b.dy === 135 ? 47 : 48, PAREN_LT);
  cell("14", 395, 153.5 + b.dy, 10.5, GREEN, { w: 16, h: 12 });
  cell("-4", 395, 167 + b.dy, 10.5, GREEN, { w: 16, h: 12 });
  cell("0",  395, 184 + b.dy, 10.5, GREEN, { w: 16, h: 12 });
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
