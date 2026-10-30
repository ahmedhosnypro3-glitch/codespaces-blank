// Build slide 036 — "Problem Formulation"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// House chrome: shared_patterns/house_chrome.js (white canvas, E9E9E7 panel x54..903
// y45..540, C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5, NO top stroke,
// badge circle d35 center (876,73) fill FDFD96 ring 6A5ACD, bold Arial 18pt numeral 36).
//
// Ground truth: unique_slides/slide_036.jpg (960x540, 1px = 1pt = 1/72in).
// PIL-measured geometry (frame px -> inches via /72), all values measured on the JPEG:
//
// TITLE "Problem Formulation": ink x=354..628 (center 491), cap top y=64, baseline y=83
//   (no descenders -> ink bottom = baseline). Color core (142,0,16) -> C00000.
//   Bold 26pt fits ink width 275px (Liberation Sans Bold @26pt = 275px); cap height
//   20px = 0.716*26=18.6 + AA -> consistent.
//
// 4 content boxes (border A60000 1pt, fill F7F7F7), left border x=68 (stroke core),
//   right border x=870, interior x=69..869 (800px):   [drawBoxX = 68, drawBoxW = 802.5]
//   box1 y=94..212 | box2 y=226..314 | box3 y=328..421 | box4 y=437..539
//   Text ink always starts x=79 (=> 10.5px inside the left border).
//
// BODY TEXT 20pt Arial, left-aligned, black. MEASURED line baselines / cap tops:
//   box1: 116/101 (L1), 146/127 (L2), 172/158 (L3), 202/187 (L4)   [pitch ~29px]
//   box2: 248/231 (L1), 278/259 (L2), 306/288 (L3)
//   box3: 353/338 (L1 heading "Define Error function as:"), equation row y=369..396
//   box4: 455/442 (L1), 486/468 (L2), 512/494 (L3)
//   => first baseline = boxTop + 22; successive baselines pitch 29px.
//   LO line model (validated on sibling build 035): with exact lineSpacing L and font F,
//   first baseline = top + (L - 1.117F)/2 + 0.905F + 1.6  [Arial asc 0.905, desc 0.212]
//
// COLOR CODING (measured from the frame; the analysis JSON's color claims are
// uncorroborated by pixels and are superseded by the frame):
//   lowercase "class" + "I"      -> C00000 red
//   uppercase "Class" + "II"     -> 0000FF blue
//   "d(X)", "delta_i", "X_i"     -> 008000 green (math symbols, italic)
//   inequality results           -> line's class color (red on class-I lines, blue on
//                                   Class-II lines); box 4's trailing "d(X) delta_i >0"
//                                   is BLACK (measured (29,29,29))
//   title                        -> C00000
//   body                         -> 000000
//
// EQUATION (box 3, left-aligned at x=84, ink y=369..396):
//   "Error = Sum_{all misclassified vectors(i)} (W^T X_i) => (W^T X_i) take positive
//    and negative values"  -- main row ~21pt, Sigma 219..239 (tall, display style with
//   the subscript BELOW, centered under the Sigma), subscript at y=401..411 x=162..297
//   (partially red, partially black in the frame). Rendered as ONE mathtext PNG at
//   600dpi (professional 2D format) + eq_036_error.json sidecar; placed at its measured
//   left edge; the trailing explanatory phrase is set BLACK (measured core (13,15,12)) --
//   the JSON brief's "red phrase" claim is not corroborated by the frame.
//   NOTE: the trailing phrase is rendered SEPARATELY in Liberation Sans Narrow 18.7pt,
//   ink-positioned at frame x=507 (scratch/tmp/eq036_v2.py). Attempt 1 glued it onto the
//   "_i) (W" run at 21pt, ran ~85 frame-px past the canvas edge and CLIPPED the last
//   glyph; the original measures that phrase's ink as x=507..733 (226px).
//
// RED X MARK: standalone, ink x=766..786 y=367..390 (core (168,0,5) -> FF0000),
//   ~32pt bold Arial, at the far right of box 3, right edge 86px inside the right border.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_036_recreated.pptx";
const EQ = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_036_error.png";
// equation image metrics from the composite renderer (600dpi, tight crop, 3px pad)
const EQ_W = 8.99667, EQ_H = 0.615, EQ_X = 83.6, EQ_Y = 368.6;

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 36 });

// ---------------------------------------------------------------------------
// Layout constants (frame px)
// ---------------------------------------------------------------------------
const BODY = 20;          // body font pt
const LS = 28;            // exact line spacing (pt) -> measured render pitch ~29px
const BOX_TOP1 = 94, BOX_BOT1 = 212;
const BOX_TOP2 = 226, BOX_BOT2 = 314;
const BOX_TOP3 = 328, BOX_BOT3 = 421;
const BOX_TOP4 = 437, BOX_BOT4 = 539;
const BOX_X = 68;          // left border core
const BOX_W = 802.5;       // to the right border core x=870 (68+802.5=870.5)
const TXT_X = 79;          // text ink left edge in every line of the original
const TXT_W = 790;         // 20% beyond the longest ink (846) but well inside the box

// First text baseline = boxTop + 22; successive pitch 29.
// Box y of an addText block whose FIRST baseline must land at BASE1:
const firstTop = (base1) => base1 - ((LS - 1.117 * BODY) / 2 + 0.905 * BODY + 1.6);

// ---------------------------------------------------------------------------
// Content boxes (drawn first so text sits on top)
// ---------------------------------------------------------------------------
function drawBox(yTop, yBottom) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(BOX_X), y: px(yTop), w: px(BOX_W), h: px(yBottom - yTop),
    fill: { color: "F7F7F7" }, line: { color: "A60000", width: 1 },
  });
}
drawBox(BOX_TOP1, BOX_BOT1);
drawBox(BOX_TOP2, BOX_BOT2);
drawBox(BOX_TOP3, BOX_BOT3);
drawBox(BOX_TOP4, BOX_BOT4);

// ---------------------------------------------------------------------------
// Text helper: one left-aligned line, verbatim runs with measured colors
// ---------------------------------------------------------------------------
function line(base1, runs) {
  slide.addText(runs.map((r, i) => ({
    text: r[0],
    options: {
      color: r[1] || "000000", italic: !!r[2], underline: !!r[3],
      superscript: !!r[4], subscript: !!r[5],
    },
  })), {
    x: px(TXT_X), y: px(firstTop(base1)), w: px(TXT_W), h: px(60),
    align: "left", valign: "top", margin: 0,
    fontFace: "Arial", fontSize: BODY, lineSpacing: LS, paraSpaceAfter: 0,
  });
}
const R = "C00000", B = "0000FF", G = "008000", K = "000000";

// --- Box 1 (measured colors: "class I" red, "Class II" blue, d(X) green) ---
line(116, [["Define two classes: " + ""], ["class", R], [" "], ["I", R], [" and "], ["Class", B], [" "], ["II", B]]);
line(144, [["let "], ["d(X)", G, true], [" be a discriminant function = "], ["W", K, true], ["T", K, false, false, true], [" "], ["X", G, true]]);
line(172, [["if "], ["X", K, true], [" \u2208 "], ["class", R], [" I", R], [" then "], ["d(X)", G, true], [" > 0", R]]);
line(201, [["if "], ["X", K, true], [" \u2208 "], ["Class", B], [" II", B], [" then "], ["d(X)", G, true], [" < 0", B]]);

// --- Box 2 ---
line(247, [["For "], ["misclassified"], [" "], ["X", G, true], [" :"]]);
line(274, [["If "], ["X", K, true], [" \u2208 "], ["class", R], [" I", R], [" and "], ["misclassified"], [" as "], ["Class", B], [" II", B], [" then "], ["d(X)", G, true], [" will be "], ["<0", R]]);
line(302, [["If "], ["X", K, true], [" \u2208 "], ["Class", B], [" II", B], [" and "], ["misclassified"], [" as "], ["class", R], [" I", R], [" then "], ["d(X)", G, true], [" will be "], [">0", B]]);

// --- Box 3 heading (black; the frame shows NO underline under "Error") ---
line(353, [["Define "], ["Error"], [" function as:"]]);
// Equation: single mathtext PNG, left edge at the measured ink x=84
slide.addImage({ path: EQ, x: px(84), y: px(EQ_Y), w: EQ_W, h: EQ_H });

// --- Box 4 ---
line(459, [["Define "], ["\u03b4_i", G, true], [" as :"]]);
line(482, [
  ["If "], ["X", K, true], [" \u2208 "], ["class", R], [" I", R], [" and "], ["misclassified"], [" as "],
  ["Class", B], [" II", B], [" then "], ["d(X)", G, true], [" will be "], ["<0", R], [" \u21d2 "],
  ["\u03b4_i", G, true], [" = -1"], [" \u21d2 "], ["d(X) ", K, true], ["\u03b4_i >0", K],
]);
line(509, [
  ["If "], ["X", K, true], [" \u2208 "], ["Class", B], [" II", B], [" and "], ["misclassified"], [" as "],
  ["class", R], [" I", R], [" then "], ["d(X)", G, true], [" will be "], [">0", B], [" \u21d2 "],
  ["\u03b4_i", G, true], [" = +1"], [" \u21d2 "], ["d(X) ", K, true], ["\u03b4_i >0", K],
]);

// ---------------------------------------------------------------------------
// Title: bold, red, centered (measured ink center x=491 -> box center 492),
// cap top 64 / baseline 83.
// ---------------------------------------------------------------------------
const T_SIZE = 26, T_LS = 34;
const titleTop = 83 - ((T_LS - 1.117 * T_SIZE) / 2 + 0.905 * T_SIZE + 1.6);
slide.addText("Problem Formulation", {
  x: px(72), y: px(titleTop), w: px(840), h: px(60),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: T_SIZE, bold: true, color: "C00000",
  lineSpacing: T_LS,
});

// ---------------------------------------------------------------------------
// Red X mark at the far right of box 3
// ---------------------------------------------------------------------------
const X_SIZE = 32, X_LS = 34;
const xTop = 390 - ((X_LS - 1.117 * X_SIZE) / 2 + 0.905 * X_SIZE + 1.6);
slide.addText("X", {
  x: px(752), y: px(xTop), w: px(50), h: px(50),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: X_SIZE, bold: true, color: "FF0000",
  lineSpacing: X_LS,
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
