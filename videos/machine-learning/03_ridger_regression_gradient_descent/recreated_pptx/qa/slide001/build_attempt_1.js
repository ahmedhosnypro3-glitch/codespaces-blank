// Build: slide 001 — "Ridge Regression, Gradient Descent, And Perceptron" (title slide)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GEOMETRY SOURCE: PIL measurement of unique_slides/slide_001.jpg (960x540, 1px=1pt=1/72in),
// banked in qa/slide001/selfcheck_measure_original.txt (measure_original*.py).
// Spec: analysis/slide_001_final.json. Where spec and frame disagree, THE FRAME WINS
// (documented deviations below).
//
// MEASURED LAYOUT (frame px):
//   Title (3 lines, Arial bold 44pt, C00000 — width fit: computed advances 389/379/328
//   vs measured ink 387/379/332 at 44pt):
//     L1 "Ridge Regression,"    ink x281..667 (ctr 474), cap-top y127
//     L2 "Gradient Descent,"    ink x278..656 (ctr 467), cap-top y178
//     L3 "And Perceptron"       ink x308..639 (ctr 473.5), cap-top y231
//   Subtitle "CSAI 253 - Spring 2024"  bold 23pt 0000FF, ink x348..601 (ctr 474.5), cap-top y313
//   "Prepared By"                     italic 18.5pt, ink x436..542 (ctr 489), cap-top y354
//   "Dr. Khaled Mostafa ElSayed"      bold 21pt 0000FF, ink x352..627 (ctr 489.5), cap-top y378
//   "kmelsayed@zewailcity.edu.eg"     regular 14.5pt 0000FF, ink x384..593 (ctr 488.5), top y404
//   "Instructors:"                    bold 21pt, ink x86..203, cap-top y422
//   name1 bold 19pt   ink x124..376, cap-top y449  (advance@19pt=252 vs measured 253)
//   email1 reg 13.75  ink x125..322, top y472       (advance=197 vs measured 197)
//   name2 bold 18.7  ink x124..340, cap-top y494   (advance=216 vs measured 216)
//   email2 reg 14     ink x124..314, top y516      (advance=190 vs measured 190)
//   Logo (IMAGE, embedded): crop x592..888, y456..532 (297x77 px) at exact size px/72.
//
// SPEC-VS-FRAME DEVIATIONS (frame wins, per building.md):
//   1. "Prepared By": spec says italic blue #0000FF — frame ink cores measure dark red
//      (107..124, 0..16, 14..23) = C00000 family (JPEG-shifted, same family as title).
//      Drawn italic C00000.
//   2. "Instructors:" header: spec says bold black — frame cores measure (130,0,10)
//      dark red. Drawn bold C00000.
//   3. Background/border/badge: spec's #F0F0F0 bg + #808080 slide border + yellow
//      badge with black outline are OVERRIDDEN by the deck house chrome law (white
//      canvas, gray E9E9E7 panel, red L/R/bottom strokes, FDFD96 badge + purple ring).
//      The measured frame HAS the house chrome (verified constant across 001/005/009/
//      018/040); the spec's gray border does not exist (residual-ink scan: clean).
//   4. Logo: spec's uncertain_items[0] says "the original image asset is needed for
//      pixel-perfect reproduction" — the original slide carries the logo as a bitmap
//      (teal panel content JPEG-destroyed beyond PIL recovery; Arabic + English text
//      bands at y483..497 / y507..514 in mixed mauve/dark ink). Recreation embeds an
//      exact crop of the logo from the original frame at its measured geometry
//      (asset: build/assets/logo_slide001.png, 297x77 at 72dpi, placed at x592 y456).
//      Verbatim logo text (ZEWAIL CITY / Arabic / University of Science and
//      Technology) is preserved inside the embedded image.
//   5. Title wrap point (spec uncertain): measured as 3 lines "Ridge Regression," /
//      "Gradient Descent," / "And Perceptron" (widths corroborate at 44pt).
//
// Laws honored: hex without '#'; fontFace explicit everywhere; margin 0; all boxes are
// SINGLE-LINE (no multi-line boxes -> no lineSpacing needed; one-band-per-element
// asserted in the closed loop); measured geometry over intuition; closed-loop render
// check before any judge call.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = __dirname + "/../slide_001_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome: white canvas, gray panel, red L/R/bottom strokes, badge "1" ----
drawHouseChrome(pptx, slide, { numeral: 1 });

const A = "Arial";

// ---- title: three single-line boxes at measured centers/cap-tops ----
// box top estimate: cap_top - 0.25*size (LO ascent offset); closed-loop corrected.
function centeredLine(text, size, ctr, capTop, color, opts = {}) {
  const wAdv = opts.w || 480;
  slide.addText(text, {
    x: px(ctr - wAdv / 2), y: px(capTop - 0.25 * size), w: px(wAdv), h: px(size * 1.7),
    align: "center", valign: "top", fontSize: size, bold: opts.bold !== false,
    color, fontFace: A, margin: 0, italic: !!opts.italic,
  });
}
centeredLine("Ridge Regression,", 44, 474, 127, "C00000");
centeredLine("Gradient Descent,", 44, 467, 178, "C00000");
centeredLine("And Perceptron", 44, 473.5, 231, "C00000");

// ---- subtitle ----
centeredLine("CSAI 253 - Spring 2024", 23, 474.5, 313, "0000FF", { w: 320 });

// ---- Prepared By block (centered ~489) ----
centeredLine("Prepared By", 18.5, 489, 354, "C00000", { w: 150, bold: false, italic: true });
centeredLine("Dr. Khaled Mostafa ElSayed", 21, 489.5, 378, "0000FF", { w: 350 });
centeredLine("kmelsayed@zewailcity.edu.eg", 14.5, 488.5, 404, "0000FF", { w: 265, bold: false });

// ---- Instructors block (left-aligned at measured left edges) ----
function leftLine(text, size, x, top, color, wBox, opts = {}) {
  slide.addText(text, {
    x: px(x), y: px(top - 0.25 * size), w: px(wBox), h: px(size * 1.7),
    align: "left", valign: "top", fontSize: size, bold: opts.bold !== false,
    color, fontFace: A, margin: 0,
  });
}
leftLine("Instructors:", 21, 84.5, 422, "C00000", 150);
leftLine("Dr. Khaled Mostafa ElSayed", 19, 124, 449, "0000FF", 330);
leftLine("kmelsayed@zewailcity.edu.eg", 13.75, 124.5, 472, "0000FF", 255, { bold: false });
leftLine("Dr. Mohamed Maher Ata", 18.7, 124, 494, "0000FF", 280);
leftLine("momaher@zewailcity.edu.eg", 14, 124.5, 516, "0000FF", 245, { bold: false });

// ---- institutional logo: exact crop from the original frame at native size ----
slide.addImage({
  path: ASSET_DIR + "/logo_slide001.png",
  x: px(592), y: px(456), w: px(297), h: px(77), // exact px/72 — never rescale
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
