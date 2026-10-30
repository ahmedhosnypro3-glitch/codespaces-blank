// Build slide 044 — Perceptron iteration 3 ("No title")
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// 12-item prephase rebuild (qa/slide044/prephase/build_readiness.md +
// adjudication_attempt3.md, PIL-arbitrated in delta_vs_related.md).
// GROUND TRUTH: unique_slides/slide_044.jpg — 960x540, 1 frame px == 1 pt.
//
// House chrome (shared_patterns/house_chrome.js — deck-frozen):
//   canvas FFFFFF | panel E9E9E7 x54..903 y45..540 | C00000 1pt strokes
//   LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY (NO top stroke) |
//   badge d~35 centered (876,73) fill FDFD96 ring 6A5ACD, bold Arial 18pt "44".
//
// Rebuild deltas vs attempt 1 (all frame/PIL-arbitrated):
//   1. eq PNG assets regenerated in dot-product form (gen_eq_044.py) with a
//      bare "image" field; eqImg uses ASSETS + m.image.
//   2. dx rows: d(x_i) = [raised class-colored row vector] [GREEN 3-row W col]
//      = value — RED row/val digits boxes 1-3, BLUE boxes 4-6; box 6 prints
//      -112 verbatim (the original's own arithmetic typo — never correct).
//   3. W update rows 1-3: black W-underbar = black old-W col + RED "+ 2 *" +
//      black x col + "=" + GREEN result; keep rows 4-6 short black W = (14,-4,0).
//   4. red ⇐ added at far right of update rows 1-3 only.
//   5. decision moved off the dx cluster: ⇒ at x~502..523, text at x~519..542.
//   6. box-3 bottom rule y329.5 added (frame has 12 border rows).
//   7. legend split into per-fragment boxes; Zero GREEN bold; C1 RED / C2 BLUE.
//   8. TL + Z columns get tall bowed paren PNGs (parens044, 041-cert P3) around
//      bare digits; Initial-W underline bar added at y~92.
//   9. LM caption verbatim sic: "Ugmented Vectors ( from Top )" (frame drops the m).

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = __dirname + "/../slide_044_recreated.pptx";
const ASSETS = __dirname + "/assets/";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const A = "Arial";
const RED = "C00000";
const BLUE = "0000C8";
const GREEN = "009A4A";
const NAVY = "221777";
const GRAYBLUE = "A3A9B7";
const CREAM = "FFFEE8";
const BLACK = "000000";
const WHITE = "FFFFFF";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 44 });

// ---- helpers ----
function eqImg(name, leftPx, baselinePx) {
  const m = JSON.parse(fs.readFileSync(ASSETS + name + ".json", "utf8"));
  slide.addImage({
    path: ASSETS + m.image, x: px(leftPx),
    y: px(baselinePx) - m.baseline_frac * m.h_in,
    w: m.w_in, h: m.h_in,
  });
  return m;
}
function parenImg(file, leftPx, topPx) {
  const m = JSON.parse(fs.readFileSync(ASSETS + "parens044/" + file + ".json", "utf8"));
  slide.addImage({
    path: ASSETS + "parens044/" + file + ".png",
    x: px(leftPx), y: px(topPx),
    w: m.px_w * m.pt_per_px / 72, h: m.px_h * m.pt_per_px / 72,
  });
}
function line(text, size, xPx, capTopPx, color, opts = {}) {
  slide.addText(text, {
    x: px(xPx), y: px(capTopPx - 0.25 * size),
    w: px(opts.w || (text.length * size * 0.62 + 24)),
    h: px(size * 1.7),
    align: opts.align || "left", valign: "top",
    fontSize: size, bold: !!opts.bold, italic: !!opts.italic,
    color, fontFace: A, margin: 0, charSpacing: opts.charSpacing,
  });
}
function ctrLine(text, size, ctrPx, capTopPx, color, opts = {}) {
  const w = opts.w || (text.length * size * 0.62 + 24);
  slide.addText(text, {
    x: px(ctrPx - w / 2), y: px(capTopPx - 0.25 * size),
    w: px(w), h: px(size * 1.7),
    align: "center", valign: "top",
    fontSize: size, bold: !!opts.bold, italic: !!opts.italic,
    color, fontFace: A, margin: 0,
  });
}
function vline(xPx, y0, y1, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(xPx), y: px(y0), w: 0, h: px(y1 - y0),
    line: { color: color, width: width },
  });
}
function hline(yPx, x0, x1, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x0), y: px(yPx), w: px(x1 - x0), h: 0,
    line: { color: color, width: width },
  });
}

// ================= TOP BAND: cream fill + navy outline box (x68..720 y54..130) =====
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(56), w: px(718 - 70), h: px(128 - 56),
  fill: { color: CREAM }, line: { type: "none" },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(720 - 68), h: px(130 - 54),
  fill: { type: "none" }, line: { color: NAVY, width: 1 },
});

// ---- top-left table: header + 2 data rows + class row, tall parens per column ---
const tlCols = [96, 119, 142, 164, 186, 209]; // PIL column centres
["x₁", "x₂", "x₃", "x₄", "x₅", "x₆"].forEach((t, i) =>
  ctrLine(t, 13, tlCols[i], 64, BLACK, { w: 34 }));
["1", "2", "1", "5", "6", "6"].forEach((t, i) =>
  ctrLine(t, 13, tlCols[i], 80, BLACK, { w: 30 }));
["1", "1", "2", "4", "5", "6"].forEach((t, i) =>
  ctrLine(t, 13, tlCols[i], 96, BLACK, { w: 30 }));
[["C₁", RED], ["C₁", RED], ["C₁", RED], ["C₂", BLUE], ["C₂", BLUE], ["C₂", BLUE]]
  .forEach(([t, c], i) => ctrLine(t, 13, tlCols[i], 114, c, { w: 30 }));
tlCols.forEach((cx) => {           // tall bowed parens, ink y77..107
  parenImg("paren_tl2_lp", cx - 7.98, 76.5);
  parenImg("paren_tl2_rp", cx + 4.62, 76.5);
});

// ---- top-centre: "Initial W =" + 3-stack bracket + underline bar on W ----
line("Initial  W =", 14, 266, 75, BLACK, { w: 90 });
hline(92, 319.5, 330, BLACK, 1.5); // W underline bar (frame y91.5..93)
vline(331, 55, 103, BLACK, 1);
vline(353, 55, 103, BLACK, 1);
ctrLine("4", 13, 342, 62, BLACK, { w: 22 });
ctrLine("-2", 13, 343, 78, BLACK, { w: 24 });
ctrLine("-2", 13, 343, 93, BLACK, { w: 24 });

// ---- "Step η = 2" (RED bold, measured x365..435 y66..77) ----
line("Step η = 2", 17, 365, 66, RED, { bold: true, italic: true, w: 110 });

// ---- "Check classes of" + Z-matrix (3 cols x 2 rows, tall parens per column) ----
line("Check classes of", 13, 499, 82, BLACK, { w: 130 });
const zCols = [605, 627.5, 649];   // PIL column centres
["Z₁", "Z₁", "Z₁"].forEach((t, i) => ctrLine(t, 12, zCols[i], 64, BLACK, { w: 26 }));
["0", "7", "3"].forEach((t, i) => ctrLine(t, 12, zCols[i], 83, BLACK, { w: 26 }));
["0", "6", "2"].forEach((t, i) => ctrLine(t, 12, zCols[i], 99, BLACK, { w: 26 }));
zCols.forEach((cx) => {            // tall bowed parens, ink y81..111
  parenImg("paren_z2_lp", cx - 7.98, 80.5);
  parenImg("paren_z2_rp", cx + 4.62, 80.5);
});

// ---- class rule legend: per-fragment boxes (Zero GREEN bold) ----
line("C₁", 13, 239, 110, RED, { bold: true, w: 30 });
line("positive,", 13, 250, 110, BLACK, { italic: true, w: 70 });
line("C₂", 13, 315, 110, BLUE, { bold: true, w: 30 });
line("negative,", 13, 325, 110, BLACK, { italic: true, w: 70 });
line("Zero", 13, 398, 110, GREEN, { bold: true, w: 45 });
line("is unaccepted", 13, 435, 110, BLACK, { w: 110 });

// ================= LEFT-MIDDLE BOX (x70..246 y140..255) ===========================
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(140), w: px(246 - 70), h: px(255 - 140),
  fill: { type: "none" }, line: { color: GRAYBLUE, width: 1 },
});
// verbatim sic — the frame prints the caption without the "m"
line("Ugmented Vectors ( from Top )", 11, 86, 148, "0000FF", { bold: true, w: 175 });
const aCols = [100, 121, 144, 167, 189, 212];
["x₁", "x₂", "x₃", "x₄", "x₅", "x₆"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 166, BLACK, { w: 26 }));
["(1)", "(1)", "(1)", "(1)", "(1)", "(1)"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 184, BLACK, { w: 24 }));
["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 199, BLACK, { w: 24 }));
["(1)", "(2)", "(4)", "(5)", "(6)", "(6)"].forEach((t, i) =>
  ctrLine(t, 12, aCols[i], 214, BLACK, { w: 24 }));
[["C₁", RED], ["C₁", RED], ["C₁", RED], ["C₂", "0000FF"], ["C₂", "0000FF"], ["C₂", "0000FF"]]
  .forEach(([t, c], i) => ctrLine(t, 12, aCols[i], 232, c, { w: 24 }));

// ================= CALCULATION AREA (x274..852, 6 bands) ==========================
slide.addShape(pptx.ShapeType.rect, {
  x: px(275), y: px(141), w: px(852 - 275), h: px(527 - 141),
  fill: { color: WHITE }, line: { type: "none" },
});
vline(273.5, 141, 527, GRAYBLUE, 0.75);
vline(852.5, 141, 527, GRAYBLUE, 0.75);
// 12 border rows measured on the frame (box-3 bottom rule y329.5 included)
[140, 197, 206, 263, 272, 329.5, 338, 395, 404, 461, 470, 528].forEach((y) =>
  hline(y, 274, 852, GRAYBLUE, 0.75));

// per-band measured anchors (frame px): row baseline, dx left, arrow x, W-group left, ⇐ x
const BL   = [178, 245, 305, 374, 437, 503];
const DX0  = [287, 287, 287, 284, 284, 284];
const ARX  = [513, 513, 502, 511, 516, 523];
const WX   = [640, 641, 629, 710, 715, 722];
const LX   = [821, 817, 799];           // ⇐ on update rows 1-3 only
const DEC  = ["Update Weight", "Update Weight", "Update Weight",
              "Keep same Weight", "Keep same Weight", "Keep same Weight"];

for (let i = 0; i < 6; i++) {
  const bl = BL[i];
  // dx cluster: d(x_i) = [raised row vector] [green W col] = val (cumulative)
  let x = DX0[i];
  let m = eqImg(`eq_044_dx${i + 1}_a`, x, bl); x += m.w_in * 72 + 3;
  m = eqImg(`eq_044_dx${i + 1}_b`, x, bl - 13); x += m.w_in * 72 + 3; // raised, class-colored
  m = eqImg(`eq_044_dx${i + 1}_c`, x, bl); x += m.w_in * 72 + 3;       // green tall W column
  eqImg(`eq_044_dx${i + 1}_d`, x, bl);                                  // = value
  // decision: ⇒ + text (arrow red on update rows, black on keep rows)
  m = eqImg(i < 3 ? "eq_044_arrD" : "eq_044_arrDk", ARX[i], bl);
  line(DEC[i], 14, ARX[i] + m.w_in * 72 + 5, bl - 10, BLACK, { w: 120 });
  // W group
  if (i < 3) {
    let wx = WX[i];
    for (const p of ["a", "b", "c", "d", "e", "f"]) {
      m = eqImg(`eq_044_w${i + 1}_${p}`, wx, bl);
      wx += m.w_in * 72 + 3;
    }
    eqImg("eq_044_arrL", LX[i], bl);   // red ⇐ on update rows
  } else {
    eqImg(`eq_044_w${i + 1}_a`, WX[i], bl);
  }
}

// ================= RED "Iteration 3" BADGE =========================================
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(84), y: px(277), w: px(214 - 84), h: px(305 - 277),
  fill: { color: "FF0000" }, line: { type: "none" }, rectRadius: 0.05,
});
slide.addText("Iteration 3", {
  x: px(84), y: px(283), w: px(214 - 84), h: px(20),
  align: "center", valign: "middle",
  fontSize: 15, bold: true, color: "FFFFFF", fontFace: A, margin: 0,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
