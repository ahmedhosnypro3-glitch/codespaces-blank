// Slide 048 — machine-learning/03_ridger_regression_gradient_descent
// "Iteration 1: Weight Update using Step η = 1"
//
// Geometry is PIL-measured from unique_slides/slide_048.jpg (960x540, 1px = 1pt).
// Frame-px coordinates below are MEASURED absolute ink extents; `f*` helpers
// convert them directly to PPTX inches (px/72 — no origin offset).
//
// Frame-vs-spec deviations (frame wins, per references/building.md):
//   * Calc boxes are WHITE-filled with thin gray (~171,175,186) borders — the
//     spec's "light blue E9F2F9 / 8FB3CC" is not in the frame (interior census:
//     910 of 921 sampled px are (254,255,253)).
//   * Action phrases ("Update Weight" / "Keep same Weight") are BLACK, not the
//     spec's maroon 8B0000 (darkest core RGB (13,15,12)); only the ⇒ glyph is
//     red.
//   * "Check classes of" caption and the note "C1 positive, C2 negative, Zero is
//     unaccepted" are ABSENT from the frame — the check-classes box interior
//     (rows 58-70) is pure white and a whole-image red-ink inventory finds no
//     red text below row 75 outside the class row. Not drawn.
//   * The green ⇐ arrow is not measurable (green ink in row 1 is JPEG noise,
//     3-10 px/row) — not drawn.
//   * The input table's third feature row (1 2 2 4 5 6) is kept verbatim.
//   * The "Iteration 1" box is a RED-FILLED rect with WHITE text (box median
//     RGB (204,68,83); 231 near-white glyph px vs 687 red px), inverting the
//     spec's "white-filled with red border".

const pptxgenpkg = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const FONT = "Arial";
const BLACK = "000000";
const RED = "FF0000";

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

// ---------------------------------------------------------------- BOX A
// Input data table: box rows 55-129, cols 69-299; 5 rows x 6 cols of content.
// Header row 64-73, data rows 75-106, red class row 111-124.
{
  const bx = fx(69), by = fy(55), bw = fw(299 - 69 + 1), bh = fh(129 - 55 + 1);
  s.addShape(pptx.ShapeType.rect, {
    x: bx, y: by, w: bw, h: bh,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  // content table inside, measured cols 84-221 / rows 64-124
  const tx = fx(84), ty = fy(64), twid = fw(221 - 84 + 1);
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

// ---------------------------------------------------------------- BOX B
// Top-centre: box rows 55-129, cols 300-559.
// Stacked Initial-W vector cols 330-353 rows 61-101; label "Initial W ="
// cols 366-425 rows 61-73; red REPEAT cols 426-530 rows 61-74.
{
  const bx = fx(300), by = fy(55), bw = fw(559 - 300 + 1), bh = fh(129 - 55 + 1);
  s.addShape(pptx.ShapeType.rect, {
    x: bx, y: by, w: bw, h: bh,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });

  // stacked vector [4; -2; -2] at cols 330-353, vertically centred on the line
  const vm = sidecar("eq_initial_w_col");
  const vMidY = fy(81);                       // rows 61-101 centre
  s.addImage({
    path: path.join(ASSET_DIR, "eq_initial_w_col.png"),
    x: fx(330), y: vMidY - vm.h_in / 2, w: vm.w_in, h: vm.h_in,
  });

  // "Initial W =" label — baseline anchored. LO's valign:"baseline" puts the
  // first line's baseline AT the box top, so y = the measured baseline row.
  // Original cap band rows 61-73 -> baseline ~71.
  s.addText("Initial W =", {
    x: fx(366), y: fy(71), w: fw(70), h: fh(20),
    fontFace: FONT, fontSize: 13, color: BLACK, italic: true,
    align: "left", valign: "baseline", margin: 0, lineSpacing: 13,
  });

  // red REPEAT instruction (measured cols 426-530, cap band rows 60-74).
  // Baseline ~71 so the caps start at ~row 61.
  s.addText("REPEAT using Step \u03b7 = 1", {
    x: fx(426), y: fy(71), w: fw(104), h: fh(20),
    fontFace: FONT, fontSize: 13, color: RED, bold: true,
    align: "left", valign: "baseline", margin: 0, lineSpacing: 13,
  });
}

// ---------------------------------------------------------------- BOX C
// Check-classes table: box rows 56-118, cols 611-719.
// Measured column centres 648.5 / 671 / 693 (spacing 22.5) — header Z1 Z2 Z3
// rows 71-83, data rows (0 7 3) rows 88-100 and (0 6 2) rows 106-114.
{
  const bx = fx(611), by = fy(56), bw = fw(719 - 611 + 1), bh = fh(118 - 56 + 1);
  s.addShape(pptx.ShapeType.rect, {
    x: bx, y: by, w: bw, h: bh,
    fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
  });
  // columns centred on the measured centres: 637.2 .. 704.8
  const tx = fx(637), twid = fw(68);
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
// Matrix rows 163-241; a black box (borders at cols 69-70 and 245-246) encloses
// it from row ~145 to row ~306.
{
  s.addText("Ugmented Vectors (from Top)", {
    x: fx(90), y: fy(156), w: fw(138), h: fh(14),
    fontFace: FONT, fontSize: 12, color: BLACK,
    align: "left", valign: "baseline", margin: 0, lineSpacing: 12,
  });

  // Matrix columns centred on the measured centres 98/121/143/165.5/188/212.5
  // (spacing ~22.7): left edge 88, width 136. Box borders at cols 69-70 and
  // 245-246 enclose it.
  const mx = fx(88), mw = fw(136);
  const rows = [
    ["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"],
    ["1", "1", "1", "1", "1", "1"],
    ["1", "2", "1", "5", "6", "6"],
    ["1", "1", "2", "4", "5", "6"],
    ["C1", "C1", "C1", "C2", "C2", "C2"],
  ];
  const tbl = rows.map((r, ri) => r.map((cell) => ({
    text: cell,
    options: {
      fontFace: FONT, fontSize: 11, align: "center", valign: "middle",
      margin: 0, bold: ri === 0 || ri === 4,
      color: ri === 4 ? RED : BLACK,
    },
  })));
  s.addTable(tbl, {
    x: mx, y: fy(163), w: mw, h: fh(78),
    fontFace: FONT, colW: Array(6).fill(mw / 6),
    rowH: fw(15.6),
    border: { type: "none" },
    fill: { color: "FFFFFF" },
  });
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
      fill: { color: "FFFFFF" }, line: { color: "ABAFBA", width: 0.75 },
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
