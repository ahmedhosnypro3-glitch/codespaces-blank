// Slide 048 — machine-learning/03_ridger_regression_gradient_descent
// "Iteration 1: Weight Update using Step η = 1"
//
// Geometry is PIL-measured from unique_slides/slide_048.jpg (960x540, 1px = 1pt).
// Frame-px coordinates below are MEASURED absolute ink extents; `f*` helpers
// convert them directly to PPTX inches (px/72 — no origin offset).
//
// Frame-vs-spec deviations (frame wins, per references/building.md):
//   * The top band is ONE indigo box, cols 68..720 / rows 54..130 — not the
//     spec's three clusters in separate frames. Border cores measure
//     (33,23,118) top and (35,23,109) right; there is NO internal divider
//     (cols 285..315 over rows 52..132: longest continuous run 12 px vs 77 for
//     the real left border and 71 for the real right).
//   * The Augmented-matrix block has its own light-gray frame box, cols
//     69..247 / rows 139..257 (left stroke col 70 and right stroke col 246 are
//     each a continuous 118-px run rows 139..256; top/bottom horizontal
//     strokes across cols 69..246 at rows 139-140 and 255-256; cores
//     (161,171,180)..(196,204,207), the calc-panel gray family). Fill is white
//     like the interior's (253,254,253) median.
//   * Calc boxes are WHITE-filled with thin gray (171,175,186) borders — the
//     spec's "light blue E9F2F9 / 8FB3CC" is not in the frame (interior census:
//     910 of 921 sampled px are (254,255,253)).
//   * Action phrases ("Update Weight" / "Keep same Weight") are BLACK, not the
//     spec's maroon 8B0000 (darkest core RGB (13,15,12)); only the ⇒ glyph is
//     red.
//   * "Check classes of" is absent from the check-classes box (interior rows
//     58-70 is pure white) and the analysis spec's position for the
//     "C1 positive, C2 negative, Zero is unaccepted" note is wrong — it is
//     measured in the top band at rows 110..124 / cols 239..508, and its
//     "Zero" is GREEN (core 69,138,56), not the spec's red. See the note block.
//   * The green ⇐ arrow is not measurable: a strict green census finds 583 px
//     spread over rows 153..518 / cols 379..764 (~0.2 px per column), i.e.
//     chroma noise, not a glyph. Not drawn.
//   * The input table's third feature row (1 2 2 4 5 6) is kept verbatim.
//   * The "Iteration 1" box is a RED-FILLED rect with WHITE text (box median
//     RGB (204,68,83); 231 near-white glyph px vs 687 red px), inverting the
//     spec's "white-filled with red border".
//   * ~66 px of unidentified sparse ink at cols 305..323 / rows 75..85 (between
//     the input table and the Initial-W vector) is in the frame but not in the
//     spec and is not legibly transcribable — omitted rather than invented.
//   * ~105 px of light-gray micro-ink at cols 283..310 / rows 293..305 (right
//     of the Iteration box) is likewise frame-only and illegible — omitted.

const pptxgenpkg = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const FONT = "Arial";
const BLACK = "000000";
const RED = "FF0000";
// Indigo of the top-band box border (frame cores (33,23,118) / (35,23,109)).
const INK = "211776";
// Light gray of the calc-panel and augmented-frame borders.
const GRAY = "ABAFBA";
// Delimiter strokes around the augmented-matrix column vectors (frame cores
// mean 144, range 127..159, neutral => mid gray).
const DGRAY = "909090";

let s = pptx.addSlide();
drawHouseChrome(pptx, s, { numeral: "48" });

// frame px -> PPTX inches. Frame px are ABSOLUTE slide coords (1px = 1pt), so
// no origin offset: fx(69) is the absolute frame column 69.
const fx = (px) => px / 72;
const fy = (py) => py / 72;
const fw = (px) => px / 72;
const fh = (px) => px / 72;

const path = require("path");
const fs = require("fs");
const ASSET_DIR = path.join(__dirname, "assets");
const sidecar = (n) => JSON.parse(
  fs.readFileSync(path.join(ASSET_DIR, n + ".json"), "utf8"));

// Place an equation PNG with its math baseline on a given text-line baseline.
function addEq(name, xIn, baselineIn) {
  const m = sidecar(name);
  const y = baselineIn - m.baseline_frac * m.h_in;
  s.addImage({ path: path.join(ASSET_DIR, name + ".png"), x: xIn, y, w: m.w_in, h: m.h_in });
  return m.w_in;
}

// ---------------------------------------------------------------- TOP-BAND BOX
// One box, cols 69..719 / rows 55..129 (shape edges, so the centered strokes
// land on the measured border-band centres), indigo border. It holds all three
// clusters (input table, Initial-W vector + red REPEAT, check-classes table).
// Measured border bands: top rows 54-56 cols 68..719; bottom rows 128-130 cols
// 68..719; left col 68-69 rows 54..130; right col 718-720 rows 54..130.
{
  s.addShape(pptx.ShapeType.rect, {
    x: fx(69), y: fy(55), w: fw(719 - 69), h: fh(129 - 55),
    fill: { color: "FFFFFF" }, line: { color: INK, width: 1 },
  });
}

// ---------------------------------------------------------------- INPUT TABLE
// Input data table inside the top-band box: 5 rows x 6 cols, cols 85..219,
// rows 64..124. Column centres measured at 96.0/118.0/140.5/163.0/185.5/208.0
// (spacing 22.4); header row 64-73, data rows 75-106, red class row 111-124.
{
  // colW must be equal: centres 96.2/118.6/141.0/163.4/185.8/208.2
  const tx = fx(85), ty = fy(64), twid = fw(134);
  const rows = [
    ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"],
    ["1", "2", "1", "5", "6", "6"],
    ["1", "1", "2", "4", "5", "6"],
    ["1", "2", "2", "4", "5", "6"],
    ["C1", "C1", "C1", "C2", "C2", "C2"],
  ];
  const tbl = rows.map((r, ri) => r.map((cell) => ({
    text: cell,
    options: {
      fontFace: FONT, fontSize: 12, align: "center", valign: "middle",
      margin: 0,
      bold: ri === 0 || ri === 4,
      color: ri === 4 ? RED : BLACK,
    },
  })));
  s.addTable(tbl, {
    x: tx, y: ty, w: twid, h: fh(124 - 64 + 1),
    fontFace: FONT, colW: [twid / 6, twid / 6, twid / 6, twid / 6, twid / 6, twid / 6],
    rowH: fh(60 / 5),
    border: { type: "none" },
    fill: { color: "FFFFFF" },
  });
}

// ------------------------------------------------- INITIAL-W VECTOR + REPEAT
// Top-centre contents of the top-band box (no separate box).
// Measured bracket strokes: left col 330 rows 64..100 / col 331 rows 59..104,
// right col 353 rows 63..101 — so the composite spans cols 330..353 and its
// centre is col 341.5.
// Label "Initial W =" cols 366..421 / rows 61..72; red REPEAT cols 426..530,
// caps rows 62..73.
{
  // stacked vector [4; -2; -2], vertically centred on the line
  const vm = sidecar("eq_initial_w_col");
  const vMidY = fy(81);                       // rows 61-101 centre
  s.addImage({
    path: path.join(ASSET_DIR, "eq_initial_w_col.png"),
    x: fx(330), y: vMidY - vm.h_in / 2, w: vm.w_in, h: vm.h_in,
  });

  // "Initial W =" label. Measured band cols 366..421 (w=56 == render w=57),
  // rows 61..72. Rendered tall because valign:"baseline" parks the first
  // line's baseline at the box top and this is single-line, so use "middle"
  // and put the box on the measured band.
  s.addText("Initial W =", {
    x: fx(366), y: fy(61), w: fw(70), h: fh(13),
    fontFace: FONT, fontSize: 13, color: BLACK, italic: true,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
  });

  // red REPEAT instruction. Measured band cols 426..530 (w=105), caps rows
  // 62..73. At fontSize 13 the string is ~13% wider than the frame's and
  // wrapped to two lines even in a 115px box; 12pt keeps it on one line in a
  // box that cannot wrap.
  s.addText("REPEAT using Step \u03b7 = 1", {
    x: fx(426), y: fy(60), w: fw(150), h: fh(16),
    fontFace: FONT, fontSize: 12, color: RED, bold: true,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
  });
}

// ------------------------------------------------------------ CLASSES-OF NOTE
// The frame carries a caption line under the Initial-W/REPEAT cluster, rows
// 110..124, cols 239..508 — omitted by earlier builds. Measured char pitch is
// uniform across the whole line (5.38 px/char for cols 239..378, 5.80 for the
// green word at 395..423, 5.57 for cols 430..508), which pins the reading:
// 26 chars = "C1 positive, C2 negative,", 5 chars green = "Zero", 14 chars =
// "is unaccepted". Colour census: 35 red px (the two "C1" tokens) and 238
// green px, mean RGB (153,205,138) core (69,138,56) — so "Zero" is GREEN in
// the frame, not red as the analysis spec says.
{
  s.addText([
    { text: "C1", options: { color: RED, bold: true } },
    { text: " positive, " },
    { text: "C2", options: { color: RED, bold: true } },
    { text: " negative, " },
    { text: "Zero", options: { color: "458A38", bold: true } },
    { text: " is unaccepted" },
  ], {
    x: fx(239), y: fy(108), w: fw(275), h: fh(18),
    fontFace: FONT, fontSize: 13.5, color: BLACK,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
  });
}

// ------------------------------------------------------------ CHECK-CLASSES
// Check-classes table inside the top-band box (no separate box).
// Measured column centres 648.5 / 671.0 / 693.0 (spacing 22.25) — header Z1 Z2 Z3
// rows 71-83, data rows (0 7 3) rows ~88-100 and (0 6 2) rows ~106-114.
{
  // columns centred on the measured centres: 637.4 .. 704.2
  const tx = fx(637), twid = fw(67);
  const rows = [
    ["Z1", "Z2", "Z3"],
    ["0", "7", "3"],
    ["0", "6", "2"],
  ];
  const tbl = rows.map((r, ri) => r.map((cell) => ({
    text: cell,
    options: {
      fontFace: FONT, fontSize: 12, align: "center", valign: "middle",
      margin: 0, bold: ri === 0, color: BLACK,
    },
  })));
  s.addTable(tbl, {
    x: tx, y: fy(71), w: twid, h: fh(45),
    fontFace: FONT, colW: [twid / 3, twid / 3, twid / 3],
    rowH: fw(15),
    border: { type: "none" },
    fill: { color: "FFFFFF" },
  });
}

// ------------------------------------------------- MID-LEFT: augmented matrix
// Header "Ugmented Vectors (from Top)" rows 149-156, cols 90-228 (the header
// ink runs 90-131/138-178/185-206/214-228 measure the full line's extent).
// A light-gray frame box encloses the matrix: cols 69..247 / rows 139..257.
{
  s.addShape(pptx.ShapeType.rect, {
    x: fx(69.5), y: fy(139.5), w: fw(245.5 - 69.5), h: fh(255.5 - 139.5),
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 0.75 },
  });

  s.addText("Ugmented Vectors (from Top)", {
    x: fx(90), y: fy(156), w: fw(138), h: fh(14),
    fontFace: FONT, fontSize: 12, color: BLACK,
    align: "left", valign: "baseline", margin: 0, lineSpacing: 12,
  });

  // Matrix columns centred on the measured centres 98/121/143/165.5/188/212.5
  // (spacing ~22.7): left edge 88, width 136. Frame borders at cols 69-70 and
  // 245-246 enclose it.
  const mx = fx(88), mw = fw(136);
  const rows = [
    ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"],
    ["1", "1", "1", "1", "1", "1"],
    ["1", "2", "1", "5", "6", "6"],
    ["1", "1", "2", "4", "5", "6"],
    ["C1", "C1", "C1", "C2", "C2", "C2"],
  ];
  const tbl = rows.map((r, ri) => r.map((cell, ci) => ({
    text: cell,
    options: {
      fontFace: FONT, fontSize: 11, align: "center", valign: "middle",
      margin: 0, bold: ri === 0 || ri === 4,
      color: ri === 4 ? (ci < 3 ? RED : INK) : BLACK,
    },
  })));
  s.addTable(tbl, {
    x: mx, y: fy(163), w: mw, h: fh(78),
    fontFace: FONT, colW: Array(6).fill(mw / 6),
    rowH: fw(15.6),
    border: { type: "none" },
    fill: { color: "FFFFFF" },
  });

  // Tall delimiter strokes pair each column: the frame shows xâ..xâ as six
  // COLUMN VECTORS, each of the three entries enclosed in parentheses spanning
  // all three rows. PIL-measured on the frame (matched crop, 2.0737 crop-px per
  // frame-px): 12 continuous vertical runs over rows 180..225.2, i.e. exactly
  // the three numeric rows (the header and class rows are outside). Stroke
  // cores are neutral gray, mean value 144 (range 127..159) => DGRAY. Centroids
  // per column pairs: 93.8/106.5, 114.6/127.9, 136.9/150.5, 159.4/173.2,
  // 182.2/195.8, 204.7/218.2 — each pair centred on its column centre.
  for (const cx of [93.8, 106.5, 114.6, 127.9, 136.9, 150.5,
    159.4, 173.2, 182.2, 195.8, 204.7, 218.2]) {
    s.addShape(pptx.ShapeType.rect, {
      x: fx(cx - 0.5), y: fy(180), w: fw(1), h: fh(225.2 - 180),
      fill: { color: DGRAY }, line: { type: "none" },
    });
  }
}

// ------------------------------------------------------- ITERATION 1 (red box)
// Red-filled rect rows 276-306, cols 83-214, white text rows 289-298.
{
  const bx = fx(83), by = fy(276), bw = fw(214 - 83 + 1), bh = fh(306 - 276 + 1);
  s.addShape(pptx.ShapeType.rect, {
    x: bx, y: by, w: bw, h: bh,
    fill: { color: "C6020A" }, line: { color: "C6020A", width: 1 },
  });
  s.addText("Iteration 1", {
    x: bx, y: by, w: bw, h: bh,
    fontFace: FONT, fontSize: 13, color: "FFFFFF", bold: true,
    align: "center", valign: "middle", margin: 0,
  });
}

// ------------------------------------------------------------- CALC PANEL
// Six white boxes with thin gray (171,175,186) borders, rows 139..528, cols
// 275..853. Measured tops/bottoms: (139,197)(197,272)(272,330)(330,395)
// (404,461)(461,528) — a 9-frame-px gap separates box 4 from box 5.
// Box 1 line: left expr cols 301-429, red ⇒ cols 490-498, action cols 509-582,
// right expr cols 617-799. All text is BLACK (darkest core RGB ~(13,15,12));
// only the ⇒ is red (JPEG-darkened C00000 family).
{
  const px = fx(275), pw = fw(853 - 275 + 1);
  const boxTop = [139, 197, 272, 330, 404, 461];
  const boxBot = [197, 272, 330, 395, 461, 528];
  const acts = ["Update Weight", "Keep same Weight", "Keep same Weight",
    "Keep same Weight", "Keep same Weight", "Keep same Weight"];
  const lefts = ["eq_r1_l", "eq_r2_l", "eq_r3_l", "eq_r4_l", "eq_r5_l", "eq_r6_l"];

  for (let i = 0; i < 6; i++) {
    const by = fy(boxTop[i]), bh = fh(boxBot[i] - boxTop[i]);
    s.addShape(pptx.ShapeType.rect, {
      x: px, y: by, w: pw, h: bh,
      fill: { color: "FFFFFF" }, line: { color: GRAY, width: 0.75 },
    });

    // text baseline = centre of the box's main ink band
    const baseline = fy((boxTop[i] + boxBot[i]) / 2) + 5 / 72;

    // left expression (d(xN) = ... = R)
    addEq(lefts[i], fx(301), baseline);

    // red ⇒ glyph at cols 490-498
    s.addText("\u21d2", {
      x: fx(488), y: by, w: fw(12), h: bh,
      fontFace: FONT, fontSize: 15, color: "C00000", bold: true,
      align: "center", valign: "middle", margin: 0,
    });

    // action phrase (black)
    s.addText(acts[i], {
      x: fx(509), y: by, w: fw(80), h: bh,
      fontFace: FONT, fontSize: 13, color: BLACK,
      align: "left", valign: "middle", margin: 0, lineSpacing: 13,
    });

    // right expression (W = ...)
    addEq(i === 0 ? "eq_r1_w" : "eq_r_kw", fx(617), baseline);
  }
}

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_048_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(() => console.log("done: " + OUT));
