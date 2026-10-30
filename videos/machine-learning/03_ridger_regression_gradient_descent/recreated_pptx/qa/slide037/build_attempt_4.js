// Build script for slide 037 of
// videos/machine-learning/03_ridger_regression_gradient_descent
// "Problem Formulation"
//
// ALL geometry below is PIL-measured from unique_slides/slide_037.jpg
// (960x540 frame px, 1px = 1pt = 1/72in). The frame is ground truth.
//
// HOUSE CHROME (deck law, measured 2026-10-19): canvas FFFFFF; gray E9E9E7 panel
// x54..903 y45..540; C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5
// ONLY (no top stroke); badge circle d~35 centered (876,73), fill FDFD96,
// ring 6A5ACD, bold 18pt Arial numeral 333333 (file number 37).
//
// CONTENT PANELS (measured fills + borders + extents):
//   P1  x 68..870   y 108..210  fill (254,255,253) -> FFFFFF, border C00000
//   P2  x 66..891   y 229..341  fill (254,255,232) -> FEFFE8, border C00000
//   P3  x 66..891   y 348..531  fill (234,219,200) -> EADBC8, border brown
//                                    (134,94,58) -> 865E3A (measured; the bottom
//                                    panel's border is brown, not red)
//
// TEXT LINES (measured ink rows; left edge measured):
//   title                       rows  64.. 84, cols 354..628 (center x 479.5)
//   "Define d_i as :"           rows 111..134, left col 77
//   implication 1               rows 144..171, left col 78
//   implication 2               rows 172..189, left col 78
//   "Redefine Error function as:" rows 243..256, left col 77
//   error equation line         rows 264..286, left col 80
//   "Summation is always positive" rows 310..326, left col 76
//   "Minimize the Error using Gradient Descent with step eta" rows 363..381, left 83
//   update equation 1           rows 404..438, left col 83
//   update equation 2           rows 472..500, left col 82
//
// SIGMA OPERATORS (measured glyph ink boxes; all three are Sigma — the two
// bottom ones simply carry a heavier stroke weight):
//   error eq      cols 202..220, rows 263..287
//   update eq 1   cols 652..673, rows 409..438
//   update eq 2   cols 332..353, rows 472..500
//   each carries a RED stacked subscript below it:
//     error eq subscript    cols 151..272, rows 292..303
//     update eq 1 subscript cols 611..679, rows 442..452
//     update eq 2 subscript cols 262..426, rows 506..514
//   -> rendered as professional 2D format (matplotlib mathtext, 600dpi transparent
//      PNG, addImage at exact px/600 + eq_*.json sidecar), Sigma aligned to the
//      measured Sigma ink box, subscript stacked below the Sigma.
//
// GREEN HIGHLIGHT BOX (second update equation): x 80..485, y 462..520,
//   fill (223,255,238) -> DFFFEE, soft green edge (~99CC99).
//
// SCRIPT SOURCE: analysis/slide_037_final.json (verbatim text, per-run colours).

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(
  __dirname, "..", "..", "shared_patterns", "house_chrome.js"
));

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const slide = pptx.addSlide();

// ---- house chrome (deck 03 measured template) ----
drawHouseChrome(pptx, slide, { numeral: 37 });

const FONT = "Liberation Serif"; // Times-like serif, calibrated against the original ink
const RED = "C00000";
const BLACK = "000000";
const BLUE = "0000FF";
const TAN = "EADBC8";
const CREAM = "FEFFE8";
const WHITE = "FFFFFF";
const BROWN = "865E3A";
const BRIGHT_RED = "FF0000";
const GREEN_FILL = "DFFFEE";
const GREEN_EDGE = "99CC99";

const ASSET = __dirname + "/assets";
const px = (v) => v / 72; // frame px -> inches

const BODY = 21; // Liberation Serif, calibrated: "Summation is always positive" ink = 220px wide
const HEAD = 20; // panel headings ("Define d_i as :", "Redefine Error function as:")

// helper: one text line pinned to a measured ink top (frame px) and left (frame px)
function lineAt(runs, leftPx, topPx, size, opts = {}) {
  slide.addText(
    runs.map((r) => ({
      text: r.text,
      options: Object.assign({ color: BLACK, fontSize: size, fontFace: FONT }, r.o || {}),
    })),
    {
      x: px(leftPx), y: px(topPx), w: opts.w || px(890 - leftPx),
      h: px(size * 1.35),
      margin: 0, valign: "top", align: "left",
    }
  );
}

// ============================================================
// TITLE — red ink rows 64..84, cols 354..628, centered on x479.5
// ============================================================
slide.addText("Problem Formulation", {
  x: 0, y: px(62), w: 13.333, h: px(28),
  align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// CONTENT PANELS (measured extents, fills, border colours)
// ============================================================
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(108), w: px(870 - 68), h: px(210 - 108),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(66), y: px(229), w: px(891 - 66), h: px(341 - 229),
  fill: { color: CREAM }, line: { color: RED, width: 1.5 },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(66), y: px(348), w: px(891 - 66), h: px(531 - 348),
  fill: { color: TAN }, line: { color: BROWN, width: 1.5 },
});

// ============================================================
// GREEN HIGHLIGHT BOX around the second update equation
// measured fill box: cols 80..485, rows 462..520 (before the text)
// ============================================================
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(80), y: px(462), w: px(485 - 80), h: px(520 - 462),
  fill: { color: GREEN_FILL }, line: { color: GREEN_EDGE, width: 1 },
});

// ============================================================
// PANEL 1 — "Define d_i as :" + two implication lines
// ============================================================
lineAt(
  [
    { text: "Define ", o: { bold: true, color: RED } },
    { text: "\u03b4", o: { bold: true, color: RED, italic: true } },
    { text: "_i", o: { bold: true, color: RED, italic: true, subscript: true } },
    { text: " as :", o: { bold: true, color: RED } },
  ],
  77, 112, HEAD
);

lineAt(
  [
    { text: "If X \u2208 " },
    { text: "class I", o: { italic: true, color: BLUE } },
    { text: " and " },
    { text: "misclassified", o: { color: BRIGHT_RED } },
    { text: " as " },
    { text: "Class II", o: { italic: true, color: BLUE } },
    { text: " then " },
    { text: "d(X)", o: { underline: true } },
    { text: " will be " },
    { text: "<0", o: { color: BRIGHT_RED } },
    { text: " \u21d2 ", o: { color: BRIGHT_RED } },
    { text: "\u03b4", o: { color: BRIGHT_RED, italic: true } },
    { text: "_i", o: { color: BRIGHT_RED, italic: true, subscript: true } },
    { text: " = ", o: { color: BRIGHT_RED } },
    { text: "-1", o: { color: BRIGHT_RED } },
    { text: " \u21d2 ", o: { color: BRIGHT_RED } },
    { text: "d(X)", o: { underline: true } },
    { text: "\u03b4", o: { color: BRIGHT_RED, italic: true } },
    { text: "_i", o: { color: BRIGHT_RED, italic: true, subscript: true } },
    { text: " > 0", o: { color: BRIGHT_RED } },
  ],
  78, 144, BODY
);

lineAt(
  [
    { text: "If X \u2208 " },
    { text: "class II", o: { italic: true, color: BLUE } },
    { text: " and " },
    { text: "misclassified", o: { color: BRIGHT_RED } },
    { text: " as " },
    { text: "Class I", o: { italic: true, color: BLUE } },
    { text: " then " },
    { text: "d(X)", o: { underline: true } },
    { text: " will be " },
    { text: ">0", o: { color: BRIGHT_RED } },
    { text: " \u21d2 ", o: { color: BRIGHT_RED } },
    { text: "\u03b4", o: { color: BRIGHT_RED, italic: true } },
    { text: "_i", o: { color: BRIGHT_RED, italic: true, subscript: true } },
    { text: " = ", o: { color: BRIGHT_RED } },
    { text: "+1", o: { color: BRIGHT_RED } },
    { text: " \u21d2 ", o: { color: BRIGHT_RED } },
    { text: "d(X)", o: { underline: true } },
    { text: "\u03b4", o: { color: BRIGHT_RED, italic: true } },
    { text: "_i", o: { color: BRIGHT_RED, italic: true, subscript: true } },
    { text: " > 0", o: { color: BRIGHT_RED } },
  ],
  78, 172, BODY
);

// ============================================================
// PANEL 2 — redefined Error function
// ============================================================
lineAt([{ text: "Redefine Error function as:", o: { bold: true, color: RED } }], 77, 243, HEAD);

// error equation: "Error = " + [Sigma + red stacked subscript] + explanation
lineAt([{ text: "Error = " }], 80, 263, BODY);

slide.addImage({
  path: ASSET + "/eq_037_sum_error.png",
  x: px(126.76), y: px(262.04), w: 2.30333, h: 0.545, // Sigma ink -> cols 202..218, rows 263..286
});

lineAt(
  [
    { text: " " },
    { text: "\u03b4", o: { italic: true } },
    { text: "_i", o: { italic: true, subscript: true } },
    { text: " W" },
    { text: "T", o: { superscript: true } },
    { text: " X" },
    { text: "_i", o: { subscript: true } },
    { text: " " },
    { text: "\u21d2", o: { color: BRIGHT_RED } },
    { text: " (W" },
    { text: "T", o: { superscript: true } },
    { text: " X" },
    { text: "_i", o: { subscript: true } },
    { text: ") takes " },
    { text: "positive", o: { color: BRIGHT_RED, italic: true } },
    { text: " and negative values and " },
    { text: "\u03b4", o: { color: BRIGHT_RED, italic: true } },
    { text: "_i", o: { color: BRIGHT_RED, italic: true, subscript: true } },
    { text: " has the same sign" },
  ],
  295, 263, BODY
);

lineAt(
  [
    { text: "Summation is always " },
    { text: "positive", o: { color: BRIGHT_RED, italic: true } },
  ],
  76, 310, BODY
);

// ============================================================
// PANEL 3 — Gradient Descent update rules
// ============================================================
lineAt(
  [
    { text: "Minimize the Error using ", o: { italic: true } },
    { text: "Gradient Descent", o: { bold: true, italic: true, color: BLUE } },
    { text: " with step ", o: { italic: true } },
    { text: "\u03b7", o: { italic: true } },
  ],
  83, 358, BODY + 2
);

// ---- update equation 1 -------------------------------------------------
// "W^(updated) = W^(old) - eta dError/dW where dError/dW = " + [Sigma+sub] + " d_i X_i"
lineAt(
  [
    { text: "W" },
    { text: "(updated)", o: { superscript: true } },
    { text: " = W" },
    { text: "(old)", o: { superscript: true } },
    { text: " - " },
    { text: "\u03b7" },
    { text: " " },
    { text: "\u2202Error/\u2202W" },
    { text: " " },
    { text: "where", o: { italic: true } },
    { text: " " },
    { text: "\u2202Error/\u2202W" },
    { text: " = " },
  ],
  83, 404, BODY
);

slide.addImage({
  path: ASSET + "/eq_037_sum_misclass.png",
  x: px(580.12), y: px(408.04), w: 2.27833, h: 0.65833, // Sigma ink -> cols 652..672, rows 409..438
});

lineAt(
  [
    { text: " " },
    { text: "\u03b4", o: { italic: true } },
    { text: "_i", o: { italic: true, subscript: true } },
    { text: " X" },
    { text: "_i", o: { subscript: true } },
  ],
  747, 404, BODY
);

// ---- update equation 2 (inside the green highlight box) -----------------
// "W^(updated) = W^(old) - eta " + [Sigma + red stacked subscript ONLY] + " d_i X_i"
lineAt(
  [
    { text: "W" },
    { text: "(updated)", o: { superscript: true } },
    { text: " = W" },
    { text: "(old)", o: { superscript: true } },
    { text: " - " },
    { text: "\u03b7" },
    { text: " " },
  ],
  82, 472, BODY
);

slide.addImage({
  path: ASSET + "/eq_037_sum_only.png",
  x: px(242.72), y: px(471.04), w: 2.71167, h: 0.58, // Sigma ink -> cols 332..349, rows 472..496
});

lineAt(
  [
    { text: " " },
    { text: "\u03b4", o: { italic: true } },
    { text: "_i", o: { italic: true, subscript: true } },
    { text: " X" },
    { text: "_i", o: { subscript: true } },
  ],
  460, 472, BODY
);

// ============================================================
// OUTPUT
// ============================================================
const OUT = path.resolve(
  __dirname, "..", "..", "recreated_pptx", "slide_037_recreated.pptx"
);
pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));