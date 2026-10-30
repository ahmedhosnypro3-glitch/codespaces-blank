// Slide 048 — machine-learning/03_ridger_regression_gradient_descent
// "Iteration 1: Weight Update using Step η = 1"
//
// FRESH BUILD per CONTINUATION_PROMPT.md §5 (2026-10-26).
// Geometry is PIL-measured from unique_slides/slide_048.jpg (960x540, 1px = 1pt).
// Frame-px coordinates below are MEASURED absolute ink extents; `f*` helpers
// convert them directly to PPTX inches (px/72 — no origin offset).
//
// Color constants per §5:
const FONT = "Arial";
const BLACK = "000000";
const RED = "FF0000";
const CRED = "C00000";
const BOXRED = "C6020A";
const INK = "211776";
const NAVY = "1F1655";
const ATITLE = "2B207C";
const GRAY = "ABAFBA";
const DGRAY = "909090";
const IGRAY = "6E6E6E";
const DGREEN = "008000";
const GREEN = "5B9C4E";

const pptxgenpkg = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

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
  fs.readFileSync(path.join(ASSET_DIR, n + ".json"), "utf8")
);

// Place an equation PNG with its math baseline on a given text-line baseline.
function addEq(name, xIn, baselineIn) {
  const m = sidecar(name);
  const y = baselineIn - m.baseline_frac * m.h_in;
  s.addImage({ path: path.join(ASSET_DIR, name + ".png"), x: xIn, y, w: m.w_in, h: m.h_in });
  return m.w_in;
}

// 1px delimiter stroke helper — drawn as LINE to avoid LibreOffice fill→red artifact
function dbar(x, y, h, color) {
  s.addShape(pptx.ShapeType.line, {
    x: fx(x), y: fy(y), w: 0, h: fh(h),
    line: { color, width: 1 },
  });
}

// Centered 16x16 text box for digits
function txt(x, y, text, { fontSize = 12, color = BLACK, bold = false, italic = false } = {}) {
  s.addText(text, {
    x: fx(x - 8), y: fy(y - 8), w: fw(16), h: fh(16),
    fontFace: FONT, fontSize, color, bold, italic,
    align: "center", valign: "middle", margin: 0,
  });
}

// ---------------------------------------------------------------- TOP-BAND BOX
// One box, cols 69..719 / rows 55..129 (shape edges, so the centered strokes
// land on the measured border-band centres), indigo border.
{
  s.addShape(pptx.ShapeType.rect, {
    x: fx(69), y: fy(55), w: fw(719 - 69), h: fh(129 - 55),
    fill: { color: "FFFFFF" }, line: { color: INK, width: 1 },
  });
}

// ---------------------------------------------------------------- INPUT TABLE
// Header x₁..x₆ centres [96.2,118.6,141.0,163.4,185.8,208.2] cellW 22.4, y64 h10 bold
// Digits row1 (1,2,1,5,6,6) y78 h10.5
// Digits row2 (1,1,2,4,5,6) y97 h10 — NO third row
// Class C₁C₁C₁C₂C₂C₂ y113 h12 bold+italic RED(first3)/INK
// Bars topL=[89.81,111.95,133.86,156.28,179.34,202.25]
//      topR=[101.37,123.59,146.15,169.01,191.46,213.61] y77 h31 DGRAY
{
  const centres = [96.2, 118.6, 141.0, 163.4, 185.8, 208.2];
  const cellW = 22.4;

  // Header row
  for (let ci = 0; ci < 6; ci++) {
    s.addText(["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"][ci], {
      x: fx(centres[ci] - cellW / 2), y: fy(64), w: fw(cellW), h: fh(10),
      fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
      bold: true, color: BLACK,
    });
  }

  // Row 1 digits - original has (1) (2) (1) (5) (6) (6) - parentheses around all
  const row1 = ["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"];
  for (let ci = 0; ci < 6; ci++) {
    s.addText(row1[ci], {
      x: fx(centres[ci] - cellW / 2), y: fy(78), w: fw(cellW), h: fh(10.5),
      fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
      bold: false, color: BLACK,
    });
  }

  // Row 2 digits - original has (1) (1) (2) (4) (5) (6) - all black (PIL att18: orig red=0)
  const row2 = ["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"];
  for (let ci = 0; ci < 6; ci++) {
    const color = BLACK;
    s.addText(row2[ci], {
      x: fx(centres[ci] - cellW / 2), y: fy(97), w: fw(cellW), h: fh(10),
      fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
      bold: false, color: color,
    });
  }

  // Class row
  const classes = ["C1", "C1", "C1", "C2", "C2", "C2"];
  const classColors = [RED, RED, RED, NAVY, NAVY, NAVY];
  for (let ci = 0; ci < 6; ci++) {
    s.addText(classes[ci], {
      x: fx(centres[ci] - cellW / 2), y: fy(113), w: fw(cellW), h: fh(12),
      fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
      bold: true, italic: true, color: classColors[ci],
    });
  }

  // Tall delimiter bars (DGRAY) around the three data rows (y77 h31)
  const topL = [89.81, 111.95, 133.86, 156.28, 179.34, 202.25];
  const topR = [101.37, 123.59, 146.15, 169.01, 191.46, 213.61];
  for (let i = 0; i < 6; i++) {
    dbar(topL[i], 77, 31, DGRAY);
    dbar(topR[i], 77, 31, DGRAY);
  }
}

// ------------------------------------------------- INITIAL-W VECTOR + REPEAT
// dbar 330.28 / 351.72, y57 h49 IGRAY
// Digits "4"/"-2"/"-2" centred (341.5,66.5)/(344.5,82.5)/(344.5,97.5) fs13 BLACK
// Label runs [{text:"Initial", underline},{text:" W"}] x365 y61 w60 h13 fs13 italic left
// REPEAT "REPEAT using Step η = 1" x426 y60 w150 h16 fs12 RED bold (no italic/underline)
{
  // Delimiter brackets around Initial W column vector - use BLACK for visibility
  dbar(330.28, 57, 49, BLACK);
  dbar(351.72, 57, 49, BLACK);

// Initial W digits fs13 BLACK
  txt(341.5, 66.5, "4", { fontSize: 13, color: BLACK });
  txt(344.5, 82.5, "-2", { fontSize: 13, color: BLACK });
  txt(344.5, 97.5, "-2", { fontSize: 13, color: BLACK });

  // "Initial W =" label with underline on "Initial" + " ="
  s.addText([
    { text: "Initial", options: { underline: true } },
    { text: " W" },
    { text: " =" },
  ], {
    x: fx(365), y: fy(61), w: fw(70), h: fh(13),
    fontFace: FONT, fontSize: 13, color: BLACK, italic: true,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
  });

  // REPEAT instruction
  s.addText("REPEAT using Step \u03b7 = 1", {
    x: fx(426), y: fy(60), w: fw(150), h: fh(16),
    fontFace: FONT, fontSize: 12, color: RED, bold: true,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
  });
}

// ------------------------------------------------------------ "Check classes of"
s.addText("Check classes of", {
  x: fx(542), y: fy(85), w: fw(88), h: fh(14),
  fontFace: FONT, fontSize: 10, color: BLACK,
  align: "left", valign: "middle", margin: 0,
});

// ------------------------------------------------------------ Z-GRID
// Centres [648,670.5,693.5] cellW 22.4
// Z₁Z₂Z₃ y71 h13 italic fs12
// 0/7/3 y86 h14 fs12
// 0/6/2 y106 h12 fs12
// Bars zp=[[640.96,654.65],[664.10,676.56],[686.30,699.07]] y86 h33 DGRAY
{
  const zCentres = [648, 670.5, 693.5];
  const cellW = 22.4;

  // Header Z1 Z1 Z1 (PIL-adjudicated att18: orig subscripts mutually identical, best-match '1')
  for (let ci = 0; ci < 3; ci++) {
    s.addText(["Z\u2081", "Z\u2081", "Z\u2081"][ci], {
      x: fx(zCentres[ci] - cellW / 2), y: fy(71), w: fw(cellW), h: fh(13),
      fontFace: FONT, fontSize: 12, align: "center", valign: "middle", margin: 0,
      bold: false, italic: true, color: BLACK,
    });
  }

  // Row 1: 0 7 3
  for (let ci = 0; ci < 3; ci++) {
    s.addText(["0", "7", "3"][ci], {
      x: fx(zCentres[ci] - cellW / 2), y: fy(86), w: fw(cellW), h: fh(14),
      fontFace: FONT, fontSize: 12, align: "center", valign: "middle", margin: 0,
      color: BLACK,
    });
  }

  // Row 2: 0 6 2
  for (let ci = 0; ci < 3; ci++) {
    s.addText(["0", "6", "2"][ci], {
      x: fx(zCentres[ci] - cellW / 2), y: fy(106), w: fw(cellW), h: fh(12),
      fontFace: FONT, fontSize: 12, align: "center", valign: "middle", margin: 0,
      color: BLACK,
    });
  }

  // Delimiter bars
  const zp = [[640.96, 654.65], [664.10, 676.56], [686.30, 699.07]];
  for (let i = 0; i < 3; i++) {
    dbar(zp[i][0], 86, 33, DGRAY);
    dbar(zp[i][1], 86, 33, DGRAY);
  }
}

// ------------------------------------------------------------ LEGEND
// Runs C₁(RED bold)/" positive "/C₂(NAVY bold)/" negative "/Zero(GREEN bold)/" is unaccepted"
// x239 y108 w300 h17 fs13.5 left
{
  s.addText([
    { text: "C\u2081", options: { color: RED, bold: true } },
    { text: " positive " },
    { text: "C\u2082", options: { color: NAVY, bold: true } },
    { text: " negative " },
    { text: "Zero", options: { color: DGREEN, bold: true } },
    { text: " is unaccepted" },
  ], {
    x: fx(239), y: fy(108), w: fw(300), h: fh(17),
    fontFace: FONT, fontSize: 13.5, color: BLACK,
    align: "left", valign: "middle", margin: 0, lineSpacing: 13,
  });
}

// ------------------------------------------------- MID-LEFT: AUGMENTED MATRIX BOX
// Frame rect x69.5 y139.5 w176 h116 WHITE fill GRAY 0.75
// Title "Ugmented Vectors (from Top)" x82 y146 w160 h15 fs9.5 italic color 2B207C
// Centres [100,122,144.5,167,189.5,212]
// Header x₁..x₆ y166 h10 italic
// Vals - original has parentheses around cells:
// Row 1: (1) (1) (1) (1) (1) (1)
// Row 2: (1) (2) (1) (5) (6) (6) - some red
// Row 3: (1) (1) (2) (4) (5) (6)
// Bars augL=[93.59,115.28,137.43,160.65,182.66,205.64]
//      augR=[105.84,127.15,149.74,172.35,195.05,217.20] y180 h46 DGRAY
// Class C₁/C₂ y230 h14 fs11 bold+italic RED/INK
{
  s.addShape(pptx.ShapeType.rect, {
    x: fx(69.5), y: fy(139.5), w: fw(245.5 - 69.5), h: fh(255.5 - 139.5),
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 0.75 },
  });

  s.addText("Ugmented Vectors (from Top)", {
    x: fx(82), y: fy(146), w: fw(160), h: fh(15),
    fontFace: FONT, fontSize: 9.5, color: ATITLE, italic: true,
    align: "left", valign: "baseline", margin: 0, lineSpacing: 12,
  });

  const mx = fx(88), mw = fw(136);
  const centres = [100, 122, 144.5, 167, 189.5, 212];
  const cellW = 22.4;

  // Header x₁..x₆
  for (let ci = 0; ci < 6; ci++) {
    s.addText(["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"][ci], {
      x: fx(centres[ci] - cellW / 2), y: fy(166), w: fw(cellW), h: fh(10),
      fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
      bold: false, italic: true, color: BLACK,
    });
  }

  // Three data rows - with parentheses per original
  // Row 1: all (1)
  const row1 = ["(1)", "(1)", "(1)", "(1)", "(1)", "(1)"];
  // Row 2: (1) (2) (1) (5) (6) (6) - some red
  const row2 = ["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"];
  // Row 3: (1) (1) (2) (4) (5) (6)
  const row3 = ["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"];
  const rows = [row1, row2, row3];
  const rowTops = [183, 198, 213];
  for (let ri = 0; ri < 3; ri++) {
    for (let ci = 0; ci < 6; ci++) {
      const color = BLACK; // att18 PIL: orig aug row-2 digits all black (red=0)
      s.addText(rows[ri][ci], {
        x: fx(centres[ci] - cellW / 2), y: fy(rowTops[ri]), w: fw(cellW), h: fh(10),
        fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
        color: color,
      });
    }
  }

  // Delimiter bars augL/augR y180 h46
  const augL = [93.59, 115.28, 137.43, 160.65, 182.66, 205.64];
  const augR = [105.84, 127.15, 149.74, 172.35, 195.05, 217.20];
  for (let i = 0; i < 6; i++) {
    dbar(augL[i], 180, 46, DGRAY);
    dbar(augR[i], 180, 46, DGRAY);
  }

  // Class row
  s.addText("C\u2081", {
    x: fx(centres[0] - cellW / 2), y: fy(230), w: fw(cellW), h: fh(14),
    fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
    bold: true, italic: true, color: RED,
  });
  s.addText("C\u2081", {
    x: fx(centres[1] - cellW / 2), y: fy(230), w: fw(cellW), h: fh(14),
    fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
    bold: true, italic: true, color: RED,
  });
  s.addText("C\u2081", {
    x: fx(centres[2] - cellW / 2), y: fy(230), w: fw(cellW), h: fh(14),
    fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
    bold: true, italic: true, color: RED,
  });
  s.addText("C\u2082", {
    x: fx(centres[3] - cellW / 2), y: fy(230), w: fw(cellW), h: fh(14),
    fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
    bold: true, italic: true, color: INK,
  });
  s.addText("C\u2082", {
    x: fx(centres[4] - cellW / 2), y: fy(230), w: fw(cellW), h: fh(14),
    fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
    bold: true, italic: true, color: INK,
  });
  s.addText("C\u2082", {
    x: fx(centres[5] - cellW / 2), y: fy(230), w: fw(cellW), h: fh(14),
    fontFace: FONT, fontSize: 11, align: "center", valign: "middle", margin: 0,
    bold: true, italic: true, color: INK,
  });
}

// ------------------------------------------------------- ITERATION 1 (red box)
// Rect x83 y276 w132 h31 fill+border C6020A
// "Iteration 1" WHITE bold fs13 centred (measured fill x84..214 y277..305)
{
  const bx = fx(83), by = fy(276), bw = fw(214 - 83 + 1), bh = fh(306 - 276 + 1);
  s.addShape(pptx.ShapeType.rect, {
    x: bx, y: by, w: bw, h: bh,
    fill: { color: BOXRED }, line: { color: BOXRED, width: 1 },
  });
  s.addText("Iteration 1", {
    x: bx, y: by, w: bw, h: bh,
    fontFace: FONT, fontSize: 13, color: "FFFFFF", bold: true,
    align: "center", valign: "middle", margin: 0,
  });
}

// ------------------------------------------------------------- CALC PANEL
// Six SEPARATE white rects (fill WHITE, line none) x274 w(853-274)
// at bands [[140,197],[206,263],[272,330],[338,395],[404,461],[470,528]]
// Horizontal GRAY 1pt rules at [140,197,206,263,272,330,338,395,404,461,470,528] spanning x274..853
// Left vertical GRAY per band (segments y140..197, 206..263, 272..330, 338..395, 404..461, 470..528)
// NO right vertical
{
  const px = fx(274), pw = fw(853 - 274 + 1);
  const boxTop = [140, 206, 272, 338, 404, 470];
  const boxBot = [197, 263, 330, 395, 461, 528];
  const acts = ["Update Weight", "Keep same Weight", "Keep same Weight",
    "Keep same Weight", "Keep same Weight", "Keep same Weight"];
  const lefts = ["eq_r1_l", "eq_r2_l", "eq_r3_l", "eq_r4_l", "eq_r5_l", "eq_r6_l"];

  // Rule y-positions (including both top and bottom of each box + the gap)
  const ruleYs = [140, 197, 206, 263, 272, 330, 338, 395, 404, 461, 470, 528];

  // Draw horizontal rules
  for (const ry of ruleYs) {
    s.addShape(pptx.ShapeType.line, {
      x: px, y: fy(ry), w: pw, h: 0,
      line: { color: GRAY, width: 0.75 },
    });
  }

  // Draw left vertical segments (with gaps)
  const vSegments = [
    [140, 197], [206, 263], [272, 330], [338, 395], [404, 461], [470, 528],
  ];
  for (const [yt, yb] of vSegments) {
    s.addShape(pptx.ShapeType.line, {
      x: px, y: fy(yt), w: 0, h: fh(yb - yt),
      line: { color: GRAY, width: 0.75 },
    });
  }

  // Row content
  for (let i = 0; i < 6; i++) {
    const by = fy(boxTop[i]), bh = fh(boxBot[i] - boxTop[i]);

    // White rect (no border — rules/verticals drawn separately)
    s.addShape(pptx.ShapeType.rect, {
      x: px, y: by, w: pw, h: bh,
      fill: { color: "FFFFFF" }, line: { type: "none" },
    });

    // Text baseline = centre of the box's main ink band + 5/72
    const baseline = fy((boxTop[i] + boxBot[i]) / 2) + 5 / 72;

    // Left expression (d(xN) = ... = R)
    addEq(lefts[i], fx(301), baseline);

    // Red ⇒ glyph at x488
    s.addText("\u21d2", {
      x: fx(488), y: by, w: fw(12), h: bh,
      fontFace: FONT, fontSize: 15, color: CRED, bold: true,
      align: "center", valign: "middle", margin: 0,
    });

    // Action phrase (black) — w100 to keep "Update Weight" on ONE line
    // (measured x-extent in original: x489..582 = 94px wide)
    s.addText(acts[i], {
      x: fx(505), y: by, w: fw(115), h: bh,
      fontFace: FONT, fontSize: 13, color: BLACK,
      align: "left", valign: "middle", margin: 0, lineSpacing: 13,
    });
  }
}

// ------------------------------------------------- ROW-1 RIGHT SIDE — decoded update equation
// "W =" text box x615 y162 w26 h16 fs12, runs [{text:"W", bold+underline},{text:" ="}]
{
  s.addText([
    { text: "W", options: { bold: true, underline: true } },
    { text: " =" },
  ], {
    x: fx(615), y: fy(162), w: fw(26), h: fh(16),
    fontFace: FONT, fontSize: 12, color: BLACK,
    align: "left", valign: "middle", margin: 0, lineSpacing: 12,
  });
}

// dbar DGRAY: x643 y150 h45; x665.5 y150 h45; x707.5 y152 h41; x720.5 y152 h41
dbar(643, 150, 45, DGRAY);
dbar(665.5, 150, 45, DGRAY);
dbar(707.5, 152, 41, DGRAY);
dbar(720.5, 152, 41, DGRAY);

// vec1 digits fs12 BLACK centred: "4"(656,156), "-2"(654.5,172), "-2"(654.5,188)
txt(656, 156, "4", { fontSize: 12, color: BLACK });
txt(654.5, 172, "-2", { fontSize: 12, color: BLACK });
txt(654.5, 188, "-2", { fontSize: 12, color: BLACK });

// red C00000: "+" (677,170) fs12; "1" (688,170) fs12. BLACK "*" (699,168) fs12
s.addText("+", {
  x: fx(677 - 4), y: fy(170 - 8), w: fw(8), h: fh(16),
  fontFace: FONT, fontSize: 12, color: CRED, bold: true,
  align: "center", valign: "middle", margin: 0,
});
txt(688, 170, "1", { fontSize: 12, color: CRED });
s.addText("*", {
  x: fx(699 - 4), y: fy(168 - 8), w: fw(8), h: fh(16),
  fontFace: FONT, fontSize: 12, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});

// vec2 digits fs12 BLACK: "1"(714.5,156), "1"(714.5,172), "1"(714.5,188); "=" BLACK fs12 (731.5,169.5)
txt(714.5, 156, "1", { fontSize: 12, color: BLACK });
txt(714.5, 172, "1", { fontSize: 12, color: BLACK });
txt(714.5, 188, "1", { fontSize: 12, color: BLACK });
s.addText("=", {
  x: fx(731.5 - 4), y: fy(169.5 - 8), w: fw(8), h: fh(16),
  fontFace: FONT, fontSize: 12, color: BLACK,
  align: "center", valign: "middle", margin: 0,
});

// vec3 GREEN=DGREEN: dbar x740 y154 h38; dbar x763 y154 h38; digits fs12 DGREEN "5"(752,156), "-1"(753,172), "-1"(753,188)
dbar(740, 154, 38, DGREEN);
dbar(763, 154, 38, DGREEN);
txt(752, 156, "5", { fontSize: 12, color: DGREEN });
txt(753, 172, "-1", { fontSize: 12, color: DGREEN });
txt(753, 188, "-1", { fontSize: 12, color: DGREEN });

// "⇐" C00000 fs15 bold, box x784 y160 w17 h16 (centre 792,168)
s.addText("\u21d0", {
  x: fx(784), y: fy(160), w: fw(17), h: fh(16),
  fontFace: FONT, fontSize: 15, color: CRED, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ------------------------------------------------- ROWS 2-6 RIGHT SIDE — W column
// r: Wbox(x,y)   bars L/R (span)      "5"@  "-1"@  digit-cy
// 2: 695,229     723 / 744.5 (216..260)  733.5  734    222 / 238.5 / 253.5
// 3: 695,292     722.5 / 744.5 (280..322) 734.5  734    285 / 301.5 / 316.5
// 4: 708,361     735 / 757   (348..392)  746.5  746    354.5 / 370.5 / 386
// 5: 708,424     734 / 756   (410..455)  744.5  744.5  417.5 / 433 / 448.5
// 6: 708,490     734 / 756   (476..522)  744.5  744.5  483.5 / 500 / 515
const wRows = [
  { x: 695, y: 229, barL: 723, barR: 744.5, d5: 733.5, d1: 734, cy: [222, 238.5, 253.5] },
  { x: 695, y: 292, barL: 722.5, barR: 744.5, d5: 734.5, d1: 734, cy: [285, 301.5, 316.5] },
  { x: 708, y: 361, barL: 735, barR: 757, d5: 746.5, d1: 746, cy: [354.5, 370.5, 386] },
  { x: 708, y: 424, barL: 734, barR: 756, d5: 744.5, d1: 744.5, cy: [417.5, 433, 448.5] },
  { x: 708, y: 490, barL: 734, barR: 756, d5: 744.5, d1: 744.5, cy: [483.5, 500, 515] },
];

for (const r of wRows) {
  // "W =" box w26 h16 fs12 runs [{W bold+underline},{" ="}] left-aligned
  s.addText([
    { text: "W", options: { bold: true, underline: true } },
    { text: " =" },
  ], {
    x: fx(r.x), y: fy(r.y), w: fw(26), h: fh(16),
    fontFace: FONT, fontSize: 12, color: BLACK,
    align: "left", valign: "middle", margin: 0, lineSpacing: 12,
  });

  // Bars DGRAY full measured span
  dbar(r.barL, r.y, r.cy[2] - r.cy[0] + 16, DGRAY); // approx span
  dbar(r.barR, r.y, r.cy[2] - r.cy[0] + 16, DGRAY);

  // Digits fs12 BLACK centred 16x16: "5", "-1", "-1"
  txt(r.d5, r.cy[0], "5", { fontSize: 12, color: BLACK });
  txt(r.d1, r.cy[1], "-1", { fontSize: 12, color: BLACK });
  txt(r.d1, r.cy[2], "-1", { fontSize: 12, color: BLACK });
}

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_048_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(() => console.log("done: " + OUT));