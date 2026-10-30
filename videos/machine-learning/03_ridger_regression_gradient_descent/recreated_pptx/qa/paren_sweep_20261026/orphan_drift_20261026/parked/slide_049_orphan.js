// Slide 049 — machine-learning/03_ridger_regression_gradient_descent
// "Iteration 2" — rebuild per qa/slide049/pil_adjudication_049h.txt REBUILD TARGETS
// + att12 fix cycle per qa/slide049/pil_adjudication_legA12.md FIX LIST
// (paren delimiters aug/Z/wcol/initial-W, C1/C2 + Z subscripts, triplet
// RED/INK coloring, W bold+underline, black =>, Initial-only underline,
// italic aug title/headers/Stop).
// (+ s7_049 pixel maps: result digits, legend tokens, rule/background census).
// Frame unique_slides/slide_049.jpg (960x540, 1px = 1pt).
//
// (2026-10-26 founder directive: NO curved parentheses — every paren asset
// (top2 / Z / aug / initial-W / wcol dx+W) and the triplet font-paren plan are
// replaced by straight 1px-rect delimiter bars at measured bulge centers, with
// re-laid digit cells at measured centroids; triplet parens ADDED.)
//
// Key rebuild deltas vs the prior build (all PIL-adjudicated):
//   * top box border is INK 211776 (frame cores 33,23,117), not violet
//   * tables are per-cell text boxes (LibreOffice expands addTable rows)
//   * top table: bracketed 2-value stacks (tall font parens y77..107) + third
//     value row below; "Initial W" dark label (no "=", underlined) with the
//     stacked [4;-2;-2] column LEFT of it; red REPEAT on one line
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
const DGRAY = "909090";    // aug/top2/Z/W-column delimiter bars (measured neutral)
const PGRAY = "A6A6A6";    // calc triplet + dx delimiter bars (measured green-gray)
const IGRAY = "6E6E6E";    // initial-W delimiter bars (measured dark)
const DGREEN = "008000";   // dx column digits (measured green family)
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

// straight delimiter bar — the certified 1px-rect idiom (build/slide_045.js);
// founder directive 2026-10-26: NO curved parentheses anywhere on the slide
function dbar(x, y, h, color) {
  s.addShape(pptx.ShapeType.rect, {
    x: fx(x), y: fy(y), w: fw(1), h: fh(h),
    fill: { color: color }, line: { type: "none" },
  });
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
  // straight paren bars around the 2-stack rows (y77..107): measured bulge
  // centers (founder directive 2026-10-26: no curved parentheses)
  const topL = [89.81, 111.95, 133.86, 156.28, 179.34, 202.25];
  const topR = [101.37, 123.59, 146.15, 169.01, 191.46, 213.61];
  for (let i = 0; i < 6; i++) {
    dbar(topL[i], 77, 31, DGRAY);
    dbar(topR[i], 77, 31, DGRAY);
  }
}
// --------------------------------------------- INITIAL-W VECTOR + REPEAT
// stacked column [4;-2;-2] LEFT of its label (F1); dark underlined "Initial W"
// (no "="; underline band y72..73 x364..423); red REPEAT single line (F5).
{
  // straight delimiter bars + digit cells at measured centroids (founder
  // directive 2026-10-26; replaces the curved paren asset; content [4;-2;-2])
  dbar(330.28, 57, 49, IGRAY);
  dbar(351.72, 57, 49, IGRAY);
  [["4", 341.5, 66.5], ["\u22122", 344.5, 82.5], ["\u22122", 344.5, 97.5]].forEach(([t, cx, cy]) =>
    txt(t, {
      x: fx(cx - 9), y: fy(cy - 8), w: fw(18), h: fh(16),
      fontSize: 13, align: "center",
    }));
  // underline band y72..73 x365..422 = "Initial" only; W has no underline
  s.addText([
    { text: "Initial", options: { underline: true } },
    { text: " W", options: {} },
  ], {
    x: fx(365), y: fy(61), w: fw(60), h: fh(13),
    fontFace: FONT, fontSize: 13, color: BLACK, italic: true,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
  });
  s.addText("REPEAT using Step \u03b7 = 1", {
    x: fx(426), y: fy(60), w: fw(150), h: fh(16),
    fontFace: FONT, fontSize: 12, color: RED, bold: true,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
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
  // straight paren bars per column, measured bulge centers (founder directive
  // 2026-10-26: no curved parentheses)
  const zp = [[640.96, 654.65], [664.10, 676.56], [686.30, 699.07]];
  for (const [lx, rx] of zp) {
    dbar(lx, 86, 33, DGRAY);
    dbar(rx, 86, 33, DGRAY);
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
  // straight paren bars per column, measured bulge centers (founder directive
  // 2026-10-26: no curved parentheses)
  const augL = [93.59, 115.28, 137.43, 160.65, 182.66, 205.64];
  const augR = [105.84, 127.15, 149.74, 172.35, 195.05, 217.20];
  for (let i = 0; i < 6; i++) {
    dbar(augL[i], 180, 46, DGRAY);
    dbar(augR[i], 180, 46, DGRAY);
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
  // measured dx/W column bar y-spans per row (top..bottom inclusive, both bars)
  const DY = [[145, 192], [214, 260], [277, 324], [347, 392], [410, 456], [475, 522]];
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
    // straight delimiter bars around the column + GREEN digit cells (founder
    // directive 2026-10-26; digits at measured centroids, content [5;-1;-1])
    dbar(378.5, DY[i][0], DY[i][1] - DY[i][0] + 1, PGRAY);
    dbar(401.0, DY[i][0], DY[i][1] - DY[i][0] + 1, PGRAY);
    [["5", 392, b + 12], ["\u22121", 393.5, b + 29], ["\u22121", 393.5, b + 45.5]].forEach(([t, cx, cy]) =>
      txt(t, {
        x: fx(cx - 9), y: fy(cy - 7), w: fw(18), h: fh(14),
        fontSize: 12, color: DGREEN,
      }));
    // straight paren bars hugging the bare triplet (49's measured bulges)
    dbar(329.0, b + 7, 13, PGRAY);
    dbar(375.0, b + 8, 12, PGRAY);
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
    // W = (fix 9: W bold + underlined) + straight delimiter bars around [5;-1;-1]
    s.addText([
      { text: "W", options: { bold: true, underline: true } },
      { text: " =", options: {} },
    ], {
      x: fx(lower ? 708 : 695), y: fy(b + 22), w: fw(26), h: fh(16),
      fontFace: FONT, fontSize: 12, color: BLACK, align: "left",
      valign: "middle", margin: 0,
    });
    // straight delimiter bars + BLACK digit cells for the W column
    // ([5;-1;-1], same per-row spans as the dx column; measured centroids)
    const wL = lower ? 733.8 : 722.3, wR = lower ? 755.4 : 744.0;
    dbar(wL, DY[i][0], DY[i][1] - DY[i][0] + 1, DGRAY);
    dbar(wR, DY[i][0], DY[i][1] - DY[i][0] + 1, DGRAY);
    const w5 = lower ? 745.5 : 733.5, wm1 = lower ? 748 : 736;
    [["5", w5, b + 12], ["\u22121", wm1, b + 29], ["\u22121", wm1, b + 45.5]].forEach(([t, cx, cy]) =>
      txt(t, {
        x: fx(cx - 9), y: fy(cy - 7), w: fw(18), h: fh(14),
        fontSize: 12, color: BLACK,
      }));
  }
}

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_049_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
