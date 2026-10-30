// Build slide 043 — "Perceptron Iteration 2"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// GROUND TRUTH: unique_slides/slide_043.jpg — 960x540, 1 frame px == 1 pt.
// All geometry below is FRAME PX; px() converts to inches.
//
// Every coordinate was PIL-measured from the original frame (scratch/043/:
// show.py, bandrows.py, lineink2.py, disputes.py, pngink.py + MEASUREMENTS.md)
// and cross-checked against analysis/slide_043_final.json. Where the analysis
// narrative and the frame disagree, the frame wins:
//   - "Iteration 2" is a SOLID RED FILLED block with WHITE text (measured
//     192,0,0) fill, white glyph ink) — not the analysis's "red border/black text".
//   - The legend line is BLACK with only "Zero" green; C1/C2 in it are not
//     coloured on the frame (measured red px = 1-2, blue = 2-3 per row).
//   - The class row of BOTH tables is drawn black on this frame.
//   - The middle-left box holds 6 parenthesised STACKED COLUMN VECTORS, not a
//     plain 4-row table.
//
// House chrome (shared_patterns/house_chrome.js — deck-frozen, overrides spec):
//   canvas FFFFFF | panel E9E9E7 x54..903 y45..540 no border |
//   C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY (no top stroke) |
//   badge d~35 centered (876,73) fill FDFD96, ring 6A5ACD, bold Arial 18pt "43".

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = __dirname + "/../slide_043_recreated.pptx";
const ASSETS = __dirname + "/assets/";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const A = "Arial";
const RED = "C00000";      // measured deck red (Step eta, C1, arrows accents)
const BLUE = "0000FF";
const GREEN = "008000";
const NAVY = "201070";     // measured top-band outline (32,16,112)
const CREAM = "FFF8E0";    // measured top-band tint (248,248,224)
const GRAYBLUE = "C0C3CA"; // measured faint box/rule outlines

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 43 });

// equation image: 600dpi transparent PNG, width stretched to the measured
// frame-px ink extent of its line, natural height, left edge on measured ink.
function eqImg(name, leftPx, rightPx, centerPx) {
  const m = JSON.parse(fs.readFileSync(ASSETS + "eq_043_" + name + ".json", "utf8"));
  const w = px(rightPx - leftPx);
  slide.addImage({
    path: ASSETS + m.image, x: px(leftPx),
    y: px(centerPx) - m.h_in / 2,
    w: w, h: 0.20,
  });
  return m;
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
    color, fontFace: A, margin: 0, charSpacing: opts.charSpacing,
  });
}

// ================= TOP BAND =================
slide.addShape(pptx.ShapeType.rect, {
  x: px(73), y: px(59), w: px(715 - 73), h: px(125 - 59),
  fill: { color: CREAM }, line: { type: "none" },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(719 - 68), h: px(130 - 54),
  fill: { type: "none" }, line: { color: NAVY, width: 1 },
});

// ---- top-left data table: header + 2 data rows + class row ----
const tblCols = [96, 118, 140, 162, 184, 206];
["x1", "x2", "x3", "x4", "x5", "x6"].forEach((t, i) => ctrLine(t, 11, tblCols[i], 64, "000000", { w: 40 }));
["(1)", "(2)", "(1)", "(5)", "(6)", "(6)"].forEach((t, i) => ctrLine(t, 11, tblCols[i], 80, "000000", { w: 44 }));
["(1)", "(1)", "(2)", "(4)", "(5)", "(6)"].forEach((t, i) => ctrLine(t, 11, tblCols[i], 96, "000000", { w: 44 }));
// class row measured BLACK on this frame (red 1-2px, blue 2-3px = JPEG noise)
["C1", "C1", "C1", "C2", "C2", "C2"].forEach((t, i) => ctrLine(t, 11, tblCols[i], 113, "000000", { w: 40 }));

// ---- top-center ----
line("Step η = 2", 17, 331, 63, RED, { bold: true, italic: true, w: 120 });
line("Initial  W =", 12, 266, 76, "000000", { w: 76 });
line("4", 14, 344, 82, "000000", { w: 30 });
line("-2", 14, 344, 98, "000000", { w: 30 });
slide.addShape(pptx.ShapeType.line, { x: px(330.5), y: px(62), w: 0, h: px(105 - 62), line: { color: "000000", width: 1 } });
slide.addShape(pptx.ShapeType.line, { x: px(430.5), y: px(62), w: 0, h: px(105 - 62), line: { color: "000000", width: 1 } });

// ---- top-right: "Check classes of" label + class-check matrix ----
line("Check classes of", 11, 499, 80, "000000", { w: 90 });
const mCols = [605, 628, 651];
["Z1", "Z1", "Z1"].forEach((t, i) => ctrLine(t, 11, mCols[i], 64, "000000", { w: 30 }));
[["(0)", "(7)", "(3)"], ["(0)", "(6)", "(2)"]].forEach((row, ri) => {
  row.forEach((t, i) => ctrLine(t, 11, mCols[i], 83 + ri * 27, "000000", { w: 24 }));
});

// ---- legend line: black, "Zero" green only (measured) ----
line("C1 positive, C2 negative, ", 12, 240, 110, "000000", { w: 155 });
line("Zero", 12, 396, 110, GREEN, { w: 30 });
line(" is unaccepted", 12, 431, 110, "000000", { w: 110 });

// ================= MIDDLE-LEFT BOX =================
slide.addShape(pptx.ShapeType.rect, {
  x: px(70), y: px(140), w: px(246 - 70), h: px(255 - 140),
  fill: { type: "none" }, line: { color: GRAYBLUE, width: 1 },
});
line("Augmented Vectors (from Top)", 11, 88, 146, "3B3F8C", { bold: true, w: 170 });
// header row (text) + 6 stacked column vectors + class row (PIL image)
["x1", "x2", "x3", "x4", "x5", "x6"].forEach((t, i) => ctrLine(t, 11, tblCols[i], 166, "000000", { w: 30 }));
slide.addImage({
  path: ASSETS + "aug_043.png", x: px(86), y: px(182),
  w: px(232 - 86), h: px(242 - 182),
});

// ================= CALCULATION ROWS =================
[140, 197, 206, 272, 328, 337, 404, 461, 470, 528].forEach((y) => slide.addShape(pptx.ShapeType.line, {
  x: px(275), y: px(y), w: px(852 - 275), h: 0,
  line: { color: GRAYBLUE, width: 0.75 },
}));
slide.addShape(pptx.ShapeType.line, { x: px(831), y: px(140), w: 0, h: px(528 - 140), line: { color: GRAYBLUE, width: 0.75 } });
slide.addShape(pptx.ShapeType.line, { x: px(851), y: px(140), w: 0, h: px(528 - 140), line: { color: GRAYBLUE, width: 0.75 } });

// measured per-band ink extents (frame px): dx line, decision line, w line
const bands = [
  { dx: "dx1", w: "w1", dec: "Update Weight", decTop: 173, dxL: 287, dxR: 829, dxC: 166, wL: 382, wR: 788, wC: 189 },
  { dx: "dx2", w: "w2", dec: "Update Weight", decTop: 242, dxL: 287, dxR: 818, dxC: 235, wL: 382, wR: 781, wC: 258 },
  { dx: "dx3", w: "w3", dec: "Update Weight", decTop: 302, dxL: 287, dxR: 812, dxC: 295, wL: 383, wR: 776, wC: 318 },
  { dx: "dx4", w: "w4", dec: "Keep same Weight", decTop: 368, dxL: 287, dxR: 803, dxC: 361, wL: 384, wR: 766, wC: 384 },
  { dx: "dx5", w: "w5", dec: "Keep same Weight", decTop: 434, dxL: 283, dxR: 782, dxC: 427, wL: 380, wR: 782, wC: 450 },
  { dx: "dx6", w: "w6", dec: "Keep same Weight", decTop: 499, dxL: 284, dxR: 781, dxC: 492, wL: 380, wR: 781, wC: 515 },
];
bands.forEach((b) => {
  eqImg(b.dx, b.dxL, b.dxR, b.dxC);
  line(b.dec, 11, b.dxL, b.decTop, b.dec.startsWith("Update") ? RED : "000000", { bold: true, w: 130 });
  eqImg(b.w, b.wL, b.wR, b.wC);
});

// blue left-pointing arrows (measured bands 4-6 x335..377, plus one x673..686 y360)
[[347, 333], [413, 333], [479, 333]].forEach(([y, x]) => {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x + 45), y: px(y + 5), w: px(-45), h: 0,
    line: { color: BLUE, width: 1, endArrowType: "triangle" },
  });
});
slide.addShape(pptx.ShapeType.line, {
  x: px(673 + 13), y: px(360 + 5), w: px(-13), h: 0,
  line: { color: BLUE, width: 1, endArrowType: "triangle" },
});

// ================= RED "Iteration 2" CALLOUT =================
// SOLID RED fill (measured C00000), WHITE bold text
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(277), w: px(214 - 84), h: px(305 - 277),
  fill: { color: "C00000" }, line: { type: "none" },
});
slide.addText("Iteration 2", {
  x: px(84), y: px(285), w: px(214 - 84), h: px(20),
  align: "center", valign: "middle",
  fontSize: 15, bold: true, color: "FFFFFF", fontFace: A, margin: 0,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
