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
//   P1  x 68..870   y 108..210  fill FFFFFF, border C00000, square corners
//   P2  x 66..891   y 229..341  fill FEFFE8, border C00000, rounded (~8px)
//   P3  x 66..891   y 348..531  fill EADBC8, border 865E3A, rounded (~8px)
//
// FRAME-MEASURED INK (2026-10-24 re-measure; the earlier build used generic
// colors that the frame contradicts — the FRAME WINS):
//   box1: "class I" RED bold italic, "Class II" BLUE bold italic (line 2 swapped:
//         class II blue / Class I red), "misclassified" BLACK bold italic
//         underlined, "<0"/">0" RED bold, "⇒" BLACK, "d" of d(X) GREEN,
//         "δ_i" GREEN with RED subscript i, "= -1"/"= +1" BLACK.
//   box2 heading "Redefine Error function as:" BLACK bold UNDERLINED.
//   box2 eq: "δ_i W^T X_i" GREEN with RED i, W/X underlined, T BLUE superscript;
//         "⇒" BLUE; "(W^T X_i)" black underlined W/X; the explanation is ITALIC
//         and on ONE line (x 394..869); "positive"/"negative" are black italic.
//   box2 sum line: "positive" RED bold italic underlined.
//   box3 heading: italic, "Gradient Descent" BLUE bold italic, eta RED bold.
//   box3 eq1: eta RED; TWO stacked fractions dError/dW (mathtext assets); the
//         Sigma carries a stacked limit line; "δ_i X_i" GREEN.
//   box3 eq2 (green rounded box x80..485 y462..520): same, limit
//         "misclassified vectors ONLY (i)".
// EQUATIONS: matplotlib mathtext -> 600dpi transparent PNG -> addImage at exact
// ink size (px/600 in), Sigma glyphs + stacked fractions. Limit lines are text
// runs centered under each Sigma (two-color limits: red keywords, black rest).
//
// SCRIPT SOURCE: analysis/slide_037_final.json (verbatim text); colors/styles
// re-read from the frame where the spec disagrees (frame wins, documented).

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
const RED = "C00000";          // title / dark-red headings + values (frame ~A2000E..C00000)
const BLACK = "000000";
const BLUE = "0000A8";         // class II / Gradient Descent / T / arrow (frame ~0E00A7)
const TAN = "EADBC8";
const CREAM = "FEFFE8";
const WHITE = "FFFFFF";
const BROWN = "865E3A";
const GREEN = "288428";        // delta_i / X_i term ink in the original (frame ~288428)
const GREEN_FILL = "DFFFEE";
const GREEN_EDGE = "7FBF7F";

const ASSET = __dirname + "/assets";
const px = (v) => v / 72; // frame px -> inches

const BODY = 21;   // box1 implication lines / equations
const HEAD = 20;   // "Define d_i as :"
const HEAD2 = 19;  // "Redefine Error function as:"
const SUM = 19;    // "Summation is always positive"
const EXPL = 18;   // box2 explanation line (italic; sized to stay inside the panel)
const SUP_BIG = 22; // "(updated)"/"old" superscript: LO renders 58% -> ~11.6pt visual
const SUP_T = 19;   // T exponent: LO renders 58% -> ~11pt visual
const SUB_I = 15;   // subscript i: LO renders 58% -> ~8.7pt visual

// helper: one text line pinned to a measured ink top (frame px) and left (frame px).
// LibreOffice renders the first line's ink ~0.25*size below the box top, so callers
// pass the measured ink top and the helper subtracts that offset.
function lineAt(runs, leftPx, inkTopPx, size, opts = {}) {
  const pad = opts.pad === undefined ? size * 0.25 : opts.pad;
  slide.addText(
    runs.map((r) => ({
      text: r.text,
      options: Object.assign({ color: BLACK, fontSize: size, fontFace: FONT }, r.o || {}),
    })),
    {
      x: px(leftPx), y: px(inkTopPx - pad),
      w: opts.w || px(940 - leftPx),
      h: opts.h || px(size * 1.5),
      margin: 0, valign: "top", align: opts.align || "left",
      lineSpacing: Math.round(size * 1.2 * 10) / 10,
    }
  );
}

// ============================================================
// TITLE — red ink rows 63..85, cols 353..629, centered on x479.5
// ============================================================
slide.addText("Problem Formulation", {
  x: px(11), y: px(60), w: 13.333, h: px(30), // frame title centre is x491 (not slide centre 480)
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
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(66), y: px(229), w: px(891 - 66), h: px(341 - 229),
  rectRadius: 0.1,
  fill: { color: CREAM }, line: { color: RED, width: 1.5 },
});
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(66), y: px(348), w: px(891 - 66), h: px(531 - 348),
  rectRadius: 0.1,
  fill: { color: TAN }, line: { color: BROWN, width: 1.5 },
});

// ============================================================
// GREEN HIGHLIGHT BOX around the second update equation
// measured fill box: cols 80..485, rows 462..520
// ============================================================
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(80), y: px(462), w: px(485 - 80), h: px(520 - 462),
  rectRadius: 0.09,
  fill: { color: GREEN_FILL }, line: { color: GREEN_EDGE, width: 1.5 },
});

// ============================================================
// PANEL 1 — "Define d_i as :" + two implication lines
// ============================================================
lineAt(
  [
    { text: "Define ", o: { bold: true, color: RED } },
    { text: "\u03b4", o: { bold: true, color: RED, italic: true } },
    { text: "_i", o: { bold: true, color: RED, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " as :", o: { bold: true, color: RED } },
  ],
  77, 116, HEAD
);

// line 1: class I = RED, Class II = BLUE, misclassified = BLACK bold italic underlined
lineAt(
  [
    { text: "If ", o: { italic: true } },
    { text: "X", o: { italic: true, underline: true } },
    { text: " \u2208 " },
    { text: "class I", o: { bold: true, italic: true, color: RED } },
    { text: "  and  " },
    { text: "misclassified", o: { bold: true, italic: true, underline: true } },
    { text: " as " },
    { text: "Class II", o: { bold: true, italic: true, color: BLUE } },
    { text: " then ", o: { italic: true } },
    { text: "d", o: { color: GREEN, italic: true } },
    { text: "(" },
    { text: "X", o: { italic: true, underline: true } },
    { text: ")" },
    { text: " will be ", o: { italic: true } },
    { text: "<0", o: { color: RED, bold: true, italic: true } },
    { text: " \u21d2 ", o: { bold: true } },
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " = -1", o: { bold: true, italic: true } },
    { text: " \u21d2 ", o: { bold: true } },
    { text: "d", o: { color: GREEN, italic: true } },
    { text: "(" },
    { text: "X", o: { italic: true, underline: true } },
    { text: ")" },
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " > 0", o: { bold: true, italic: true } },
  ],
  78, 142, BODY
);

// line 2: class II = BLUE, Class I = RED
lineAt(
  [
    { text: "If ", o: { italic: true } },
    { text: "X", o: { italic: true, underline: true } },
    { text: " \u2208 " },
    { text: "class II", o: { bold: true, italic: true, color: BLUE } },
    { text: "  and  " },
    { text: "misclassified", o: { bold: true, italic: true, underline: true } },
    { text: " as " },
    { text: "Class I", o: { bold: true, italic: true, color: RED } },
    { text: " then ", o: { italic: true } },
    { text: "d", o: { color: GREEN, italic: true } },
    { text: "(" },
    { text: "X", o: { italic: true, underline: true } },
    { text: ")" },
    { text: " will be ", o: { italic: true } },
    { text: ">0", o: { color: RED, bold: true, italic: true } },
    { text: " \u21d2 ", o: { bold: true } },
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " = +1", o: { bold: true, italic: true } },
    { text: " \u21d2 ", o: { bold: true } },
    { text: "d", o: { color: GREEN, italic: true } },
    { text: "(" },
    { text: "X", o: { italic: true, underline: true } },
    { text: ")" },
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " > 0", o: { bold: true, italic: true } },
  ],
  78, 170, BODY
);

// ============================================================
// PANEL 2 — redefined Error function
// ============================================================
// heading is BLACK bold underlined in the frame (NOT dark red)
lineAt([{ text: "Redefine Error function as:", o: { bold: true, underline: true } }], 77, 242, HEAD2);

// error equation: "Error =" + [Sigma glyph] + stacked limit + terms + arrow + explanation
lineAt([{ text: "Error =", o: { bold: true } }], 80, 268, BODY);

slide.addImage({
  path: ASSET + "/eq_037_sigma.png",
  x: px(201.30), y: px(261.36), w: 0.29605, h: 0.37788, // Sigma ink -> cols 202..221, rows 262..287
});

// stacked limit under the Sigma: "all misclassified vectors (i)"
lineAt(
  [
    { text: "all ", o: { italic: true } },
    { text: "misclassified", o: { color: RED, bold: true, italic: true, underline: true } },
    { text: " vectors ", o: { italic: true } },
    { text: "(i)", o: { italic: true } },
  ],
  121.5, 293, 10.75, { w: px(180), align: "center" }
);

// "d_i W^T X_i" — green terms, red i under delta, blue T, W and X underlined
lineAt(
  [
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " W", o: { color: GREEN, bold: true, italic: true, underline: true } },
    { text: "T", o: { color: BLUE, superscript: true, fontSize: SUP_T } },
    { text: " X", o: { color: GREEN, bold: true, italic: true, underline: true } },
    { text: "_i", o: { color: GREEN, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
  ],
  279, 268, BODY, { w: px(100) }
);

// blue implication arrow
lineAt([{ text: "\u21d2", o: { color: BLUE, bold: true } }], 360, 268, BODY, { w: px(30) });

// explanation — ITALIC in the frame, ONE line (fixes the attempt-4 wrap MAJOR)
lineAt(
  [
    { text: "(", o: { italic: true } },
    { text: "W", o: { italic: true, underline: true } },
    { text: "T", o: { color: BLUE, superscript: true, fontSize: SUP_T } },
    { text: " X", o: { italic: true, underline: true } },
    { text: "_i", o: { subscript: true, fontSize: SUB_I } },
    { text: ") takes positive and negative values and ", o: { italic: true } },
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " has the same sign", o: { italic: true } },
  ],
  393, 272, EXPL
);

lineAt(
  [
    { text: "Summation is always " },
    { text: "positive", o: { color: RED, bold: true, italic: true, underline: true } },
  ],
  76, 309, SUM
);

// ============================================================
// PANEL 3 — Gradient Descent update rules
// ============================================================
lineAt(
  [
    { text: "Minimize the Error using ", o: { italic: true } },
    { text: "Gradient Descent", o: { bold: true, italic: true, color: BLUE } },
    { text: " with step ", o: { italic: true } },
    { text: "\u03b7", o: { color: RED, bold: true, italic: true } },
  ],
  83, 362, BODY
);

// ---- update equation 1 -------------------------------------------------
// "W^(updated) = W^(old) - eta  [dError/dW]  where  [dError/dW] = Sigma_{...} d_i X_i"
lineAt(
  [
    { text: "W", o: { bold: true, italic: true, underline: true } },
    { text: "(updated)", o: { italic: true, superscript: true, fontSize: SUP_BIG } },
    { text: " = ", o: { bold: true, italic: true } },
    { text: "W", o: { bold: true, italic: true, underline: true } },
    { text: "old", o: { italic: true, superscript: true, fontSize: SUP_BIG } },
    { text: " - ", o: { bold: true } },
    { text: "\u03b7", o: { color: RED, bold: true, italic: true } },
  ],
  83, 415, BODY, { w: px(170) }
);

// stacked fraction dError/dW (mathtext, ink rows 403..448)
slide.addImage({
  path: ASSET + "/eq_037_frac.png",
  x: px(266.12), y: px(401.94), w: 0.99515, h: 0.66643,
});

lineAt([{ text: "where", o: { bold: true, italic: true } }], 409, 415, BODY, { w: px(80) });

slide.addImage({
  path: ASSET + "/eq_037_frac.png",
  x: px(510.12), y: px(401.94), w: 0.99515, h: 0.66643,
});

lineAt([{ text: "=", o: { bold: true } }], 589, 419, BODY, { w: px(25) });

slide.addImage({
  path: ASSET + "/eq_037_sigma.png",
  x: px(650.05), y: px(408.18), w: 0.39967, h: 0.47962, // Sigma ink cols 651..677 rows 409..441
});

// stacked limit under Sigma: "misclassified vectors"
lineAt(
  [
    { text: "misclassified", o: { color: RED, bold: true, italic: true } },
    { text: " vectors", o: { bold: true } },
  ],
  573, 445, 12.5, { w: px(180), align: "center" }
);

// "d_i X_i" — green terms, red i under delta
lineAt(
  [
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " X", o: { color: GREEN, bold: true, italic: true, underline: true } },
    { text: "_i", o: { color: GREEN, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
  ],
  722, 418, BODY, { w: px(90) }
);

// ---- update equation 2 (inside the green highlight box) -----------------
lineAt(
  [
    { text: "W", o: { bold: true, italic: true, underline: true } },
    { text: "(updated)", o: { italic: true, superscript: true, fontSize: SUP_BIG } },
    { text: " = ", o: { bold: true, italic: true } },
    { text: "W", o: { bold: true, italic: true, underline: true } },
    { text: "old", o: { italic: true, superscript: true, fontSize: SUP_BIG } },
    { text: " - ", o: { bold: true } },
    { text: "\u03b7", o: { color: RED, bold: true, italic: true } },
  ],
  83, 474, BODY, { w: px(170) }
);

slide.addImage({
  path: ASSET + "/eq_037_sigma.png",
  x: px(330.16), y: px(471.26), w: 0.35526, h: 0.43602, // Sigma ink cols 331..354 rows 472..501
});

// stacked limit under Sigma: "misclassified vectors ONLY (i)"
lineAt(
  [
    { text: "misclassified", o: { color: RED, bold: true, italic: true, underline: true } },
    { text: " vectors ", o: { bold: true } },
    { text: "ONLY", o: { color: RED, bold: true, italic: true, underline: true } },
    { text: " (i)" },
  ],
  243, 506, 11, { w: px(200), align: "center" }
);

lineAt(
  [
    { text: "\u03b4", o: { color: GREEN, bold: true, italic: true } },
    { text: "_i", o: { color: RED, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
    { text: " X", o: { color: GREEN, bold: true, italic: true, underline: true } },
    { text: "_i", o: { color: GREEN, bold: true, italic: true, subscript: true, fontSize: SUB_I } },
  ],
  422, 475, BODY, { w: px(90) }
);

// ============================================================
// OUTPUT
// ============================================================
const OUT = path.resolve(
  __dirname, "..", "..", "recreated_pptx", "slide_037_recreated.pptx"
);
pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
