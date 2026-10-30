// Build slide 046 — "Perceptron Algorithm: Iteration 4 — Stop Iterations"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Spec: analysis/slide_046_final.json + slide_046_raw.json
// Frame: unique_slides/slide_046.jpg (960x540, 1px = 1pt = 1/72 in) — PIL measured.
//
// MEASURED GEOMETRY (frame px, from unique_slides/slide_046.jpg):
//   Rules (black 3px bars): y 54..56 and y 128..130, both spanning x 68..719
//   Top-left block, 6 columns at measured centres:
//     subscript header  y 64..73  x [94.5 116.5 138.5 160.5 183.5 206.5]  "x1 x2 x3 x4 x5 x6"
//     data row 1        y 80..89  x [96.5 118.5 140.5 163.5 186 208.5]     "1 2 1 5 6 4"
//     data row 2        y 96..105 x [97 118 140.5 163 186.5 208.5]         "1 1 2 4 5 6"
//     class labels      y 111..124 x [94 116.5 138.5 161 183.5 206.5]      "C1 C1 C1 C2 C2 C2"
//     caption           x 253..449 (coloured C1 / C2 / Zero + black words)
//   Upper-mid block: "Initial" + W vector (x 336..470, y 62..74),
//     red "Step η = 2" (x 336..~400, y 77..90), "Check Classes of Z" (y 110..124)
//   Z matrix: Z1 Z1 Z1 header x [384 398 412] y 169..180,
//     rows "0 0 7" y 175..183 and "0 6 2" y 187..195
//   Yellow final-weight box: x 744..828, y 58..107 (fill FFFF99, 1pt black border),
//     holds eq_046_final_w.png = W = (14,-4,0)^T
//   Lower data matrix (x 68..236):
//     dashed separator y 140 (x 70..246) | small subscript line y 148..159
//     subscript header y 166..175 x [97.5 119.5 142.5 164.5 187.5 210.5]
//     data rows y 184..192 / 199..207 / 214..222 at x [100 121.5 144 166.5 189.5 212]
//       = "1 2 1 5 6 4" / "1 1 2 4 5 6" / "1 1 1 4 5 6"
//     class labels y 232..240 x [97.5 120 142 165 187.5 210]
//   "Iteration 4" red-outlined box: x 83..217, y 278..305
//   "Stop Iterations" pink box: x 63..244, y 330..416 (fill FFC0CB)
//   Scatter plot: plot_046_scatter.png at x=312, y=173, w=514, h=310 (native px/72)
//
// HEX never carries '#'; fontFace explicit; margin 0; single-line boxes with a
// pinned lineSpacing (LO/PowerPoint auto-pitch divergence law); images at native
// px/600 so eq glyphs are exactly fontsize pt on the slide.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");
const fs = require("fs");

const px = (v) => v / 72; // frame px -> inches
const A = "Arial";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_046_recreated.pptx";
const EQ = (n) => JSON.parse(fs.readFileSync(__dirname + "/assets/" + n + ".json", "utf8"));

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes, badge "46" ----
drawHouseChrome(pptx, slide, { numeral: 46 });

// ---- helpers ---------------------------------------------------------------
function AB(base, x, y, size, subSize) {          // italic base + subscript digit
  slide.addText(
    [
      { text: base, options: { fontFace: A, fontSize: size, italic: true, color: "000000" } },
      { text: "1", options: { fontFace: A, fontSize: subSize, color: "0000FF", subscript: true } },
    ],
    { x: px(x), y: px(y), w: px(18), h: px(11),
      align: "left", valign: "middle", margin: 0, lineSpacing: 11 }
  );
}
function NUM(v, x, y, size) {                      // black digit, centred on x
  slide.addText(String(v), {
    x: px(x - 6), y: px(y), w: px(12), h: px(11),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: size, color: "000000",
  });
}
function CL(sub, x, y) {                           // class label C1/C2, coloured
  const col = sub === "1" ? "0000FF" : "FF0000";
  slide.addText(
    [
      { text: "C", options: { fontFace: A, fontSize: 10, bold: true, color: col } },
      { text: sub, options: { fontFace: A, fontSize: 7.5, bold: true, color: col, subscript: true } },
    ],
    { x: px(x - 9), y: px(y), w: px(18), h: px(11),
      align: "center", valign: "middle", margin: 0, lineSpacing: 11 }
  );
}

// ===========================================================================
// TOP-LEFT BLOCK (x 68..719, y 54..130)
// ===========================================================================
for (const ry of [54, 128]) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(68), y: px(ry), w: px(719 - 68), h: px(3),
    fill: { color: "000000" }, line: { type: "none" },
  });
}
const TOP_H = [94.5, 116.5, 138.5, 160.5, 183.5, 206.5];
TOP_H.forEach((x) => AB("x", x - 6, 64, 8, 6));
[96.5, 118.5, 140.5, 163.5, 186, 208.5].forEach((x, i) => NUM([1, 2, 1, 5, 6, 4][i], x, 80, 13));
[97, 118, 140.5, 163, 186.5, 208.5].forEach((x, i) => NUM([1, 1, 2, 4, 5, 6][i], x, 96, 13));
[94, 116.5, 138.5, 161, 183.5, 206.5].forEach((x, i) => CL(["1", "1", "1", "2", "2", "2"][i], x, 111));

// caption: "C1 positive   C2 negative   Zero is unaccepted" (x 253..449)
const CAP = [
  { t: "C1", c: "0000FF", b: true }, { t: " positive   ", c: "000000", b: false },
  { t: "C2", c: "FF0000", b: true }, { t: " negative   ", c: "000000", b: false },
  { t: "Zero", c: "008000", b: true }, { t: " is unaccepted", c: "000000", b: false },
];
slide.addText(
  CAP.map((w) => ({ text: w.t, options: { fontFace: A, fontSize: 9, color: w.c, bold: w.b } })),
  { x: px(253), y: px(111), w: px(200), h: px(14),
    align: "left", valign: "middle", margin: 0, lineSpacing: 12 }
);

// ===========================================================================
// UPPER-MID BLOCK (x 330..545): Initial W, Step eta = 2, Check Classes of Z
// ===========================================================================
slide.addText("Initial", {
  x: px(336), y: px(62), w: px(46), h: px(12),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 10, color: "000000", lineSpacing: 12,
});
const eInit = EQ("eq_046_initial_w");
slide.addImage({ path: __dirname + "/assets/eq_046_initial_w.png", x: px(340), y: px(61), w: eInit.w_in, h: eInit.h_in });

slide.addText("Step", {
  x: px(336), y: px(77), w: px(28), h: px(12),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 10, bold: true, color: "FF0000", lineSpacing: 12,
});
slide.addImage({ path: __dirname + "/assets/eq_046_step_eta.png", x: px(364), y: px(75), w: 0.352, h: 0.16 });

slide.addText("Check Classes of Z", {
  x: px(336), y: px(110), w: px(115), h: px(13),
  align: "left", valign: "middle", margin: 0,
  fontFace: A, fontSize: 10, color: "000000", lineSpacing: 12,
});
// Z matrix (x 384..412): Z1 Z1 Z1 header, rows "0 0 7" and "0 6 2"
const ZX = [384, 398, 412];
ZX.forEach((x, i) => {
  slide.addText(
    [
      { text: "Z", options: { fontFace: A, fontSize: 10, italic: true, color: "FF0000" } },
      { text: String(i + 1), options: { fontFace: A, fontSize: 7.5, color: "FF0000", subscript: true } },
    ],
    { x: px(x - 6), y: px(169), w: px(16), h: px(11),
      align: "left", valign: "middle", margin: 0, lineSpacing: 11 }
  );
});
["0", "0", "7"].forEach((v, i) => NUM(v, ZX[i], 175, 10));
["0", "6", "2"].forEach((v, i) => NUM(v, ZX[i], 187, 10));

// ===========================================================================
// YELLOW FINAL-WEIGHT BOX (x 744..828, y 58..107)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(744), y: px(58), w: px(84), h: px(49),
  fill: { color: "FFFF99" }, line: { color: "000000", width: 1 },
});
const eFin = EQ("eq_046_final_w");
slide.addImage({
  path: __dirname + "/assets/eq_046_final_w.png",
  x: px(786) - eFin.w_in / 2, y: px(82.5) - eFin.h_in / 2,
  w: eFin.w_in, h: eFin.h_in,
});

// ===========================================================================
// LOWER DATA MATRIX (x 68..236, y 140..243)
// ===========================================================================
slide.addShape(pptx.ShapeType.line, {
  x: px(70), y: px(140), w: px(176), h: 0,
  line: { color: "000000", width: 0.75, dashType: "dash" },
});
// small subscript line y 148..159 (x 84..236) — the x1..x6 header, small
[84, 99, 114, 130, 145, 161].forEach((x, i) => {
  slide.addText(
    [
      { text: "x", options: { fontFace: A, fontSize: 7.5, italic: true, color: "000000" } },
      { text: String(i + 1), options: { fontFace: A, fontSize: 6, color: "000000", subscript: true } },
    ],
    { x: px(x), y: px(149), w: px(16), h: px(11),
      align: "left", valign: "middle", margin: 0, lineSpacing: 10 }
  );
});
// subscript header y 166..175
const LO_H = [97.5, 119.5, 142.5, 164.5, 187.5, 210.5];
LO_H.forEach((x) => AB("x", x - 6, 166, 8, 6));
// three data rows
const LO_R = [100, 121.5, 144, 166.5, 189.5, 212];
const LO_V = [[1, 2, 1, 5, 6, 4], [1, 1, 2, 4, 5, 6], [1, 1, 1, 4, 5, 6]];
LO_V.forEach((vals, r) => {
  vals.forEach((v, i) => NUM(v, LO_R[i], 184 + r * 15, 11));
});
// class labels y 232..240
[97.5, 120, 142, 165, 187.5, 210].forEach((x, i) =>
  CL(["1", "1", "1", "2", "2", "2"][i], x, 232)
);

// ===========================================================================
// "ITERATION 4" red-outlined box (x 83..217, y 278..305)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(83), y: px(278), w: px(134), h: px(27),
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1 },
});
slide.addText("Iteration 4", {
  x: px(83), y: px(278), w: px(134), h: px(27),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 16, bold: true, color: "FF0000", lineSpacing: 18,
});

// ===========================================================================
// "STOP ITERATIONS" pink box (x 63..244, y 330..416)
// ===========================================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(63), y: px(330), w: px(181), h: px(86),
  fill: { color: "FFC0CB" }, line: { color: "000000", width: 1 },
});
slide.addText(
  [
    { text: "No change in ", options: { fontFace: A, fontSize: 15, color: "000000" } },
    { text: "W", options: { fontFace: A, fontSize: 15, color: "000000", underline: true } },
  ],
  { x: px(63), y: px(350), w: px(181), h: px(20),
    align: "center", valign: "middle", margin: 0, lineSpacing: 18 }
);
slide.addText("Stop Iterations", {
  x: px(63), y: px(375), w: px(181), h: px(20),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "FF0000", lineSpacing: 20,
});

// ===========================================================================
// SCATTER PLOT — plot_046_scatter.png at native px/72 (NO rescale)
// ===========================================================================
slide.addImage({
  path: __dirname + "/assets/plot_046_scatter.png",
  x: px(312), y: px(173), w: px(514), h: px(310),
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
