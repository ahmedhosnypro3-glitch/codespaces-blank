// Slide 049 — machine-learning/03_ridger_regression_gradient_descent
// "Iteration 2" — rebuild per qa/slide049/pil_adjudication_049h.txt REBUILD TARGETS
// + att12 fix cycle per qa/slide049/pil_adjudication_legA12.md FIX LIST
// (paren delimiters aug/Z/wcol/initial-W, C1/C2 + Z subscripts, triplet
// RED/INK coloring, black = between label and column, no label underline,
// italic aug title/headers/Stop).
// (+ s7_049 pixel maps: result digits, legend tokens, rule/background census).
// Frame unique_slides/slide_049.jpg (960x540, 1px = 1pt).
//
// Key rebuild deltas vs the prior build (all PIL-adjudicated):
//   * top box border is INK 211776 (frame cores 33,23,117), not violet
//   * tables are per-cell text boxes (LibreOffice expands addTable rows)
//   * top table: bracketed 2-value stacks (tall font parens y77..107) + third
//     value row below; "Initial W =" dark label LEFT of the stacked [4;-2;-2]
//     column (no underline — measured 1px); red REPEAT on one line
//   * aug box: gray frame rect, six 3-row bracketed columns, C1/C2 tags
//   * calc panel: white-filled region x274..853 y140..528 (frame census) with
//     ABAFBA rules — top y140, double separators 9px apart, bottom y528, left
//     vertical x274 y140..514, NO right vertical, NO y46 line (house law)
//   * d-rows per F2: bare digit triplet, high-bracket (5;-1;-1) column, "=",
//     results 3/2/2/-4/-6/-7 (pixel-decided, see adjudication addendum),
//     red =>, "Keep same Weight", "W =" + bracket column
//   * legend: no commas; "Zero" green (frame core RGB(91,156,78))

const pptxgenpkg = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");
const path = require("path");
const fs = require("fs");
const ASSET_DIR = path.join(__dirname, "assets");
const sidecar = (n) => JSON.parse(
  fs.readFileSync(path.join(ASSET_DIR, n + ".json"), "utf8"));

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const s = pptx.addSlide();
drawHouseChrome(pptx, s, { numeral: "49" });

const FONT = "Arial";
const BLACK = "000000";
const RED = "FF0000";
const CRED = "C00000";     // => glyph / house-stroke red family
const BOXRED = "C6020A";   // Iteration-box fill (048-certified measurement)
const INK = "211776";      // top-box border + C2 class tags
const NAVY = "1F1655";     // legend C2
const VIOLET = "6A5ACD";   // aug-box title
const GRAY = "ABAFBA";     // frame rects + calc rules
const DGRAY = "909090";    // aug-table delimiter strokes
const GREEN = "5B9C4E";    // legend "Zero" (frame core 91,156,78)
const WHITE = "FFFFFF";

const fx = (px) => px / 72;
const fy = (py) => py / 72;
const fw = (px) => px / 72;
const fh = (px) => px / 72;

function txt(str, o) {
  s.addText(str, Object.assign({
    fontFace: FONT, fontSize: 11, color: BLACK, align: "center",
    valign: "middle", margin: 0,
  }, o || {}));
}
// one row of six per-cell texts on given centres
function row(texts, centres, cellW, top, h, o) {
  for (let i = 0; i < 6; i++) {
    txt(texts[i], Object.assign({
      x: fx(centres[i] - cellW / 2), y: fy(top), w: fw(cellW), h: fh(h),
    }, o || {}));
  }
}

// ---------------------------------------------------------------- TOP-BAND BOX
// border bands measured: top y54-56, bottom y128-130, left x68-69, right x718-720
s.addShape(pptx.ShapeType.rect, {
  x: fx(69), y: fy(55), w: fw(719 - 69), h: fh(129 - 55),
  fill: { color: WHITE }, line: { color: INK, width: 1 },
});

// ------------------------------------------------------- TOP TABLE (x1..x6)
// header y64..73; bracketed 2-stacks y77..107 (digit rows y78..88 / y97..107);
// class tag row y113..124 (outside the brackets). Column centres 96.2..208.2.
{
  const centres = [96.2, 118.6, 141.0, 163.4, 185.8, 208.2];
  const cellW = 22.4;
  row(["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"],
    centres, cellW, 64, 10, { bold: true });
  row(["1", "2", "1", "5", "6", "6"], centres, cellW, 78, 10.5);
  row(["1", "1", "2", "4", "5", "6"], centres, cellW, 97, 10);
  // class tags C1..C6 -> C1 C1 C1 C2 C2 C2 at y113..124 (below the brackets)
  const cls = ["C\u2081", "C\u2081", "C\u2081", "C\u2082", "C\u2082", "C\u2082"];
  for (let i = 0; i < 6; i++) {
    txt(cls[i], {
      x: fx(centres[i] - cellW / 2), y: fy(113), w: fw(cellW), h: fh(12),
      bold: true, italic: true, color: i < 3 ? RED : INK,
    });
  }
  // tall parentheses around the 2-stack rows (ink y77..107): measured Bezier
  // PNGs (fix 15: font parens -> 909090 class, same as Z; bows = sub-pixel
  // centroids, qa/slide049/parenA_15c.out)
  const ptL = sidecar("parens049/paren_top2_lp");
  const ptR = sidecar("parens049/paren_top2_rp");
  const PPPT = 72 / 600;
  const topLP = [89.78, 111.18, 133.45, 155.89, 178.84, 201.21];
  const topRP = [102.42, 124.72, 147.12, 170.07, 192.45, 214.74];
  for (let i = 0; i < 6; i++) {
    s.addImage({
      path: path.join(ASSET_DIR, "parens049/paren_top2_lp.png"),
      x: fx(topLP[i] - (ptL.ink_left_px * PPPT + ptL.S_pt / 2)),
      y: fy(77 - ptL.ink_top_px * PPPT),
      w: ptL.px_w * PPPT / 72, h: ptL.px_h * PPPT / 72,
    });
    s.addImage({
      path: path.join(ASSET_DIR, "parens049/paren_top2_rp.png"),
      x: fx(topRP[i] + 0.5 - ((ptR.ink_right_px + 1) * PPPT - ptR.S_pt / 2)),
      y: fy(77 - ptR.ink_top_px * PPPT),
      w: ptR.px_w * PPPT / 72, h: ptR.px_h * PPPT / 72,
    });
  }
}
// --------------------------------------------- INITIAL-W VECTOR + REPEAT
// label LEFT of the vector with "=" (measured 1px: "Initial" x267..296,
// W x303..313, "=" x316..321 double bar, vector x330..353; the label's W
// is NOT underlined — the x366..421 band y71..72 belongs to the Step text).
// Step line mirrors the pixel-adjudicated orig (att18: "REPEAT" black
// italic underlined x366..421 + red bold italic "using Step η = 1" x425..530;
// see qa/slide050/adjud_step_line_20261026.md). Identical on slide 050.
{
  const vm = sidecar("eq_slide049_wcol_paren").iw;
  const PPP = 72 / 600; // pt per asset px
  s.addImage({
    path: path.join(ASSET_DIR, "eq_initial_w_col_paren.png"),
    x: fx(330.02), y: fy(58 - vm.ink_top_px * PPP),
    w: vm.w_in, h: vm.h_in,
  });
  s.addText("Initial W =", {
    x: fx(267), y: fy(72), w: fw(62), h: fh(14),
    fontFace: FONT, fontSize: 13, color: BLACK, italic: true,
    align: "left", valign: "middle", margin: 0,
  });
  s.addText("REPEAT", {
    x: fx(365), y: fy(56), w: fw(64), h: fw(18),
    fontFace: FONT, fontSize: 14, color: BLACK, italic: true, underline: true,
    align: "left", valign: "middle", margin: 0,
  });
  s.addText("using Step \u03B7 = 1", {
    x: fx(424.5), y: fy(57), w: fw(112), h: fw(17),
    fontFace: FONT, fontSize: 14, color: "92211B", bold: true, italic: true,
    align: "left", valign: "middle", margin: 0,
  });
}

// ------------------------------------------------------ CHECK-CLASSES + Z GRID
txt("Check classes of", {
  x: fx(548), y: fy(85), w: fw(92), h: fh(14),
  fontSize: 10, align: "left",
});
// header Z1 Z2 Z3 y71..84; rows (0,7,3) / (0,6,2); centres 648/670.5/693.5
{
  const centres = [648, 670.5, 693.5];
  const cellW = 22.4;
  const rows = [
    { top: 71, h: 13, texts: ["Z\u2081", "Z\u2082", "Z\u2083"], bold: false, italic: true },
    { top: 86, h: 14, texts: ["0", "7", "3"], bold: false, italic: false },
    { top: 106, h: 12, texts: ["0", "6", "2"], bold: false, italic: false },
  ];
  // measured paren pairs (bows, ink top y88): (0;0)(7;6)(3;2)
  // same bulge-centre placement as the aug pairs (lp bulge at bow, rp at bow+0.5)
  const pl = sidecar("parens049/paren_z49_lp");
  const pr = sidecar("parens049/paren_z49_rp");
  const PPPP = 72 / 600;
  const zp = [[641.5, 655.5], [664.5, 677.5], [686.5, 699.5]];
  for (const [lx, rx] of zp) {
    s.addImage({
      path: path.join(ASSET_DIR, "parens049/paren_z49_lp.png"),
      x: fx(lx - (pl.ink_left_px * PPPP + pl.S_pt / 2)),
      y: fy(88 - pl.ink_top_px * PPPP),
      w: pl.px_w * PPPP / 72, h: pl.px_h * PPPP / 72,
    });
    s.addImage({
      path: path.join(ASSET_DIR, "parens049/paren_z49_rp.png"),
      x: fx(rx + 0.5 - ((pr.ink_right_px + 1) * PPPP - pr.S_pt / 2)),
      y: fy(88 - pr.ink_top_px * PPPP),
      w: pr.px_w * PPPP / 72, h: pr.px_h * PPPP / 72,
    });
  }
  for (const b of rows) {
    for (let i = 0; i < 3; i++) {
      txt(b.texts[i], {
        x: fx(centres[i] - cellW / 2), y: fy(b.top), w: fw(cellW), h: fh(b.h),
        bold: b.bold, italic: b.italic, fontSize: 12,
      });
    }
  }
}

// ------------------------------------------------------------------- LEGEND
// x239..508 y110..124; NO commas (frame descender census); Zero is green (F6).
s.addText([
  { text: "C\u2081", options: { color: RED, bold: true } },
  { text: " positive " },
  { text: "C\u2082", options: { color: NAVY, bold: true } },
  { text: " negative " },
  { text: "Zero", options: { color: GREEN, bold: true } },
  { text: " is unaccepted" },
], {
  x: fx(239), y: fy(108), w: fw(300), h: fh(17),
  fontFace: FONT, fontSize: 13.5, color: BLACK,
  align: "left", valign: "middle", margin: 0, lineSpacing: 14,
});

// ------------------------------------------------------------- AUGMENTED BOX
// gray frame x69.5..245.5 / y139.5..255.5 (border strokes x70/x246, y140/y255)
s.addShape(pptx.ShapeType.rect, {
  x: fx(69.5), y: fy(139.5), w: fw(176), h: fh(116),
  fill: { color: WHITE }, line: { color: GRAY, width: 0.75 },
});
s.addText("Ugmented Vectors (from Top)", {
  x: fx(80), y: fy(146), w: fw(158), h: fh(15),
  fontFace: FONT, fontSize: 12, color: VIOLET, italic: true,
  align: "left", valign: "middle", margin: 0,
});
{
  const centres = [100, 122, 144.5, 167, 189.5, 212];
  const cellW = 22.4;
  row(["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"],
    centres, cellW, 166, 10, { bold: false, italic: true });
  // six 3-row columns, value bands y184..192 / 199..207 / 214..222
  const vals = [
    ["1", "1", "1"], ["1", "2", "1"], ["1", "1", "2"],
    ["1", "5", "4"], ["1", "6", "5"], ["1", "6", "6"],
  ];
  const bands = [183, 198, 213];
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 6; c++) {
      txt(vals[c][r], {
        x: fx(centres[c] - cellW / 2), y: fy(bands[r]), w: fw(cellW), h: fh(10),
      });
    }
  }
  // measured paren pairs (fix 2: bows lp x93.5/115.5/137.5/160.5/182.5/205.5,
  // rp x106.5/128.5/151.5/173.5/196.5/218.5, ink top y180; lp bulge = leftmost
  // ink at bow, rp bulge = rightmost ink at bow+0.5 = centre of the measured band)
  const paL = sidecar("parens049/paren_aug_lp");
  const paR = sidecar("parens049/paren_aug_rp");
  const PPP = 72 / 600;
  const augLP = [93.5, 115.5, 137.5, 160.5, 182.5, 205.5];
  const augRP = [106.5, 128.5, 151.5, 173.5, 196.5, 218.5];
  for (let i = 0; i < 6; i++) {
    s.addImage({
      path: path.join(ASSET_DIR, "parens049/paren_aug_lp.png"),
      x: fx(augLP[i] - (paL.ink_left_px * PPP + paL.S_pt / 2)),
      y: fy(180 - paL.ink_top_px * PPP),
      w: paL.px_w * PPP / 72, h: paL.px_h * PPP / 72,
    });
    s.addImage({
      path: path.join(ASSET_DIR, "parens049/paren_aug_rp.png"),
      x: fx(augRP[i] + 0.5 - ((paR.ink_right_px + 1) * PPP - paR.S_pt / 2)),
      y: fy(180 - paR.ink_top_px * PPP),
      w: paR.px_w * PPP / 72, h: paR.px_h * PPP / 72,
    });
  }
  // class tags C1..C6 -> C1 C1 C1 C2 C2 C2 (bold+italic, RED/INK, measured)
  for (let c = 0; c < 6; c++) {
    s.addText(c < 3 ? "C\u2081" : "C\u2082", {
      x: fx(centres[c] - cellW / 2), y: fy(230), w: fw(cellW), h: fh(14),
      fontFace: FONT, fontSize: 11, bold: true, italic: true,
      color: c < 3 ? RED : INK, align: "center", valign: "middle", margin: 0,
    });
  }
}

// ---------------------------------------------------------- ITERATION 2 BOX
// red fill x84..213 y278..304 (row census 278..304 solid; NOT taller — the
// r7 "y278..394" extent merged the box with the red Stop glyphs y376..393)
s.addShape(pptx.ShapeType.rect, {
  x: fx(84), y: fy(278), w: fw(129), h: fh(26),
  fill: { color: BOXRED }, line: { color: BOXRED, width: 1 },
});
s.addText("Iteration 2", {
  x: fx(84), y: fy(278), w: fw(129), h: fh(26),
  fontFace: FONT, fontSize: 21, color: WHITE, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ------------------------------- "No change in W" / "Stop Iterations"
s.addText("No change in ", {
  x: fx(78), y: fy(349), w: fw(120), h: fh(22),
  fontFace: FONT, fontSize: 20, color: BLACK, align: "left", valign: "middle", margin: 0,
});
s.addText("W", {
  x: fx(198), y: fy(349), w: fw(20), h: fh(22),
  fontFace: FONT, fontSize: 20, color: BLACK, underline: true,
  align: "left", valign: "middle", margin: 0,
});
s.addText("Stop", {
  x: fx(85), y: fy(374), w: fw(42), h: fh(22),
  fontFace: FONT, fontSize: 20, color: RED, italic: true,
  align: "left", valign: "middle", margin: 0,
});
s.addText("Iterations", {
  x: fx(127), y: fy(374), w: fw(90), h: fh(22),
  fontFace: FONT, fontSize: 20, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// ---------------------------------------------------------------- CALC PANEL
// white-filled region x274..853 y140..528 (frame census: interiors 254,255,253
// vs panel 231,233,230); ABAFBA rules; left vertical x274 y140..514; open right.
s.addShape(pptx.ShapeType.rect, {
  x: fx(274), y: fy(140), w: fw(853 - 274), h: fh(528 - 140),
  fill: { color: WHITE }, line: { type: "none" },
});
[140, 197, 206, 263, 272, 329, 338, 395, 404, 461, 470, 528].forEach((y) => {
  s.addShape(pptx.ShapeType.line, {
    x: fx(274), y: fy(y), w: fw(853 - 274), h: 0,
    line: { color: GRAY, width: 1 },
  });
});
s.addShape(pptx.ShapeType.line, {
  x: fx(274), y: fy(140), w: 0, h: fh(514 - 140),
  line: { color: GRAY, width: 1 },
});

// --------------------------------------------------- SIX CALCULATION ROWS
// band starts 140/206/272/338/404/470; ink offsets within a band:
//   bare digits +9..+20 at x-centres 335/353/371; label/+ others centred +30;
//   high-bracket column x379 (top +7); "=" x409 (rows 4-6 x411); result digit
//   x420 (rows 4-6 "−d" from x420); => x496 (rows 4-6 x508.5); verdict x516
//   (rows 4-6 x528); "W =" x695 (rows 4-6 x708); W column x721 (rows 4-6 x733).
{
  const B = [140, 206, 272, 338, 404, 470];
  const digits = [["1", "1", "1"], ["1", "2", "1"], ["1", "1", "2"],
    ["1", "5", "4"], ["1", "6", "5"], ["1", "6", "6"]];
  const results = ["3", "2", "2", "\u22124", "\u22126", "\u22127"];
  const centres = [335, 353, 371];
  for (let i = 0; i < 6; i++) {
    const b = B[i];
    const lower = i >= 3;
    // d(xi) = label with true subscript
    s.addText([
      { text: "d(x", options: {} },
      { text: String(i + 1), options: { subscript: true } },
      { text: ") =", options: {} },
    ], {
      x: fx(283), y: fy(b + 22), w: fw(46), h: fh(16),
      fontFace: FONT, fontSize: 12, color: BLACK, align: "left",
      valign: "middle", margin: 0,
    });
    // bare digit triplet (top-aligned); fix 8: rows 1-3 RED, rows 4-6 INK
    for (let c = 0; c < 3; c++) {
      txt(digits[i][c], {
        x: fx(centres[c] - 7), y: fy(b + 9), w: fw(14), h: fh(12),
        fontSize: 12, valign: "top", color: lower ? INK : RED,
      });
    }
    // high-bracket column (5;-1;-1) — paren asset, box pinned at certified x
    // (379.02 = 379.5 - 4*0.12; apex sits at asset px18 -> lands at 381.18)
    const wc = sidecar("eq_slide049_wcol_paren").wcol_1;
    s.addImage({
      path: path.join(ASSET_DIR, "slide_049_wcol_paren_1.png"),
      x: fx(379.02), y: fy(b + 7),
      w: wc.w_in, h: wc.h_in,
    });
    // "="
    txt("=", {
      x: fx(lower ? 411 : 409), y: fy(b + 22), w: fw(10), h: fh(16), fontSize: 12,
    });
    // result (rows 4-6 carry the minus in the same box)
    txt(results[i], {
      x: fx(lower ? 420 : 419), y: fy(b + 22), w: fw(lower ? 24 : 12), h: fh(16),
      fontSize: 12, align: "left",
    });
    // => (fix 10: BLACK, keep bold)
    txt("\u21d2", {
      x: fx(lower ? 508.5 : 496), y: fy(b + 22), w: fw(14), h: fh(16),
      fontSize: 15, bold: true, color: BLACK,
    });
    // verdict
    txt("Keep same Weight", {
      x: fx(lower ? 528 : 516), y: fy(b + 22), w: fw(110), h: fh(16),
      fontSize: 12, align: "left",
    });
    // W = (fix 9: W bold + underlined) + paren column (lp bow x722.5/x733.5, ink top b+8)
    s.addText([
      { text: "W", options: { bold: true, underline: true } },
      { text: " =", options: {} },
    ], {
      x: fx(lower ? 708 : 695), y: fy(b + 22), w: fw(26), h: fh(16),
      fontFace: FONT, fontSize: 12, color: BLACK, align: "left",
      valign: "middle", margin: 0,
    });
    const wcol = sidecar("eq_slide049_wcol_paren")["wcol_" + (i + 1)];
    s.addImage({
      path: path.join(ASSET_DIR, "slide_049_wcol_paren_" + (i + 1) + ".png"),
      x: fx(lower ? 733.02 : 722.02),
      y: fy(b + 8), w: wcol.w_in, h: wcol.h_in,
    });
  }
}

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_049_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
