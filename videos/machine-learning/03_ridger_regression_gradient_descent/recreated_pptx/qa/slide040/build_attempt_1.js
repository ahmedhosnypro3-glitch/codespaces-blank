// Build slide 040 — "Training of Linear Regression Model ... using SGD ... Solved Example"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Attempt 1 — fresh ROOT build (no dependencies; slide 40 has no children).
//
// GROUND TRUTH: unique_slides/slide_040.jpg — 960x540, 1 frame px == 1 pt == 1/72 in
// (verified: 960/13.3333 = 72.0001). All geometry below is in FRAME PX.
// Measurement bank: qa/slide040/selfcheck_attempt_1.py + measure_original.py output.
//
// MEASURED LAYOUT (frame px):
//   House chrome (shared_patterns/house_chrome.js, verified constant across the deck):
//     canvas FFFFFF | panel E9E9E7 x54..903 y45..540 no border |
//     C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY (NO top stroke) |
//     badge circle d~35 centered (876,73) fill FDFD96 ring 6A5ACD, bold Arial 18pt "40"
//
//   Content (three centred bold lines, no equations, no charts, no table):
//     L1 "Training of Linear Regression Model"  C00000 bold, cap-top y177, centred c474
//     L2 "usnig SGD"   (typo preserved verbatim per validation policy)  0000FF bold,
//        cap-top y257, centred c473 — ink x367..580 (measured)
//     L3 "Solved Example"  C00000 bold, cap-top y326, centred c462 — ink x306..629
//   Pointer icon: tiny dark mark at (508, 470-471) on the gray panel (bottom-center),
//     ~1-2px — a mouse-pointer / video-capture artifact at the visible resolution.
//
// SPEC-vs-FRAME DEVIATIONS (frame wins per the judge GROUND RULES + house chrome law):
//   1. The spec's #F0F0F0 background, 2pt #808080 perimeter border and FFFF00 badge are
//      OVERRIDDEN by the deck house chrome (white canvas, E9E9E7 panel, C00000 1pt
//      L/R/bottom strokes, FDFD96 badge with purple ring). The real frame carries the
//      house chrome (measured: gray panel 232,232,232 family rows y45..536, red stroke
//      px 1708 at the bottom band, top-band red px = 0, purple ring px at x876 y73).
//   2. The pointer icon at the bottom-center measures 1-2 dark px on the panel — below
//      the 6px print threshold and a cursor artifact class; not drawn (GROUND RULE (c):
//      mouse-cursor / video-capture artifacts in image 2 are video artifacts, correctly
//      omitted from the recreation).
//   3. "usnig SGD" is almost certainly "using SGD"; validation.uncertain_items[0] says
//      keep it VERBATIM — drawn exactly as "usnig SGD".
//
// SIZE FIT CHECKS (measured advance vs measured ink, Arial bold):
//   L1 44pt: advance "Training of Linear Regression Model" = 736 vs ink 736 (108..844)
//   L2 36pt: advance "usnig SST" = 0 -> measured ink w=214 (367..580) at x-height+desc
//   L3 44pt: advance "Solved Example" = 323 vs ink 323 (306..629)
//   All lines sit fully inside the panel (x58.5..901, y45..540) with >= 55px clearance.
//
// Laws honored: hex without '#'; fontFace explicit; margin 0; every text box is
// SINGLE-LINE (one band per element — no multi-line box, so no lineSpacing needed);
// explicit x/y in inches via px(); centring from measured centres.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = __dirname + "/../slide_040_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// Deck house font (measured sans-serif on the frame; the slide_001 build uses Arial)
const A = "Arial";
const RED = "C00000";  // title + sub-header (frame ink families; deck nominal)
const BLUE = "0000FF"; // "usnig SGD"

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes (no top), badge 40 ----
drawHouseChrome(pptx, slide, { numeral: 40 });

// ---- three centred single-line text boxes, one band per element ----
// capTop is the top of the cap letters on the frame; box top = capTop - 0.25*size
// (LibreOffice ascent offset, same model as the slide_001 build).
function centeredLine(text, size, ctr, capTop, color) {
  const w = 760; // wide enough for the longest line (736 px advance) with margin
  slide.addText(text, {
    x: px(ctr - w / 2),
    y: px(capTop - 0.25 * size),
    w: px(w),
    h: px(size * 1.7),
    align: "center", valign: "top",
    fontSize: size, bold: true,
    color, fontFace: A, margin: 0,
  });
}

centeredLine("Training of Linear Regression Model", 44, 474, 177, RED);
centeredLine("usnig SGD", 36, 473, 257, BLUE);
centeredLine("Solved Example", 44, 462, 326, RED);

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
