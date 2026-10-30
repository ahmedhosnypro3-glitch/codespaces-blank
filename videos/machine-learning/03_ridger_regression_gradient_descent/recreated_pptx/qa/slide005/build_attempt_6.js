// Build slide 005 — "Minimization of Loss function to obtain BEST model parameters"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// GROUND TRUTH: unique_slides/slide_005.jpg (960x540, 1 frame px = 1 pt = 1/72 in).
//
// PIL-measured geometry (qa/slide005/measure_slide005.py + measure_slide005.json):
//   Title          ink x 162..808, y 68..92, single line
//                  red part x162..807, blue part "BEST" x565..619
//   cream_upper    fill FBFFE5 (measured 251,253,229), border BCBEB8
//                  x 72..892, y 102..277
//   blue_upper     fill DAEBFA (measured 218,236,250), border 9BAAB0
//                  x 676..882, y 134..238
//   pink           fill F8CFD3 (measured 248,208,211), border 7D1B28 (C00000 family)
//                  x 73..506, y 288..343
//   cream_lower    fill FBFFE5, border BCBEB8, x 72..892, y 358..522
//   blue_lower     fill DAEBFA, border 9BAAB0, x 656..872, y 372..422
//   green_outline  ring 2F8F3F (green), fill CEFFE3 (measured 206,255,226)
//                  x 688..879, y 464..498  → wraps the final W formula
//
// Text bands (frame px):
//   eq1 x 98..544 y 109..150   eq2 x 97..629 y 173..214   eq3 x 98..522 y 230..271
//   eq4 x 97..592 y 375..417   eq5 x 96..637 y 460..502 — eq5 is the ARROW CHAIN
//   Remember up x 681..754 y 138..149 ; Remember low x 661..733 y 376..387
//     — the ORIGINAL's lower-right box carries its content ~20 px LEFT of the
//     upper-right box's (x 661 vs 681); measured, not a typo.
//   "X is a matrix, W is a vector," x 681..869 y 158..171
//   "XW is a vector" x 680..787 y 178..191
//   "Get Best W that minimizes the loss" x 196..506 y 296..334
//
// HOUSE CHROME: deck 03 — white canvas FFFFFF, gray panel E9E9E7 x54..903
// y45..540, C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY
// (NO top stroke — a top stroke is a build defect). Badge circle d≈35px centered
// (876,73), fill FDFD96, purple ring 6A5ACD, bold Arial 18pt numeral 333333 = 5.
// NOTE the LO vertical offset seen on slide_003 (~22 render-px at 150dpi): the
// shared house_chrome.js draws the badge at cy=73; LO renders it ~22px LOW, so it
// lands at the measured y. Keep the module's own values (do not hand-correct).
//
// FONT: DejaVu Sans — verified 2026-10-24 by rendering probe strings through
// LibreOffice at 150dpi: title 18pt bold = 643.8 px vs original 647;
// "Remember" 12pt bold = 72.0 vs 74; body lines 14pt = 191.4 / 100.7 vs 184 / 108;
// "Get Best W that minimizes the loss" 18pt = 313.8 vs 311.
// Equations are matplotlib-mathtext 600dpi PNGs placed at px/600 (professional
// 2D format per founder directive 2026-10-09).

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_005_recreated.pptx";
const ASSETS = path.resolve(__dirname, "assets");

const px = (v) => v / 72; // frame px -> inches

// measured fills/borders
const CREAM = "FBFFE5"; // measured 251,253,229
const CBORD = "BCBEB8"; // measured 190,190,188 @1px
const BLUEF = "DAEBFA"; // measured 218,236,250
const BBORD = "9BAAB0"; // measured 156,174,184 @1px
const PINKF = "F8CFD3"; // measured 248,208,211
const PBORD = "7D1B28"; // measured 142,20,33 (C00000 family, JPEG-darkened)
const GRING = "2F8F3F"; // measured 66,146,59
const GFILL = "CEFFE3"; // measured 206,255,227
const RED = "FF0000";
const BLUE = "0000FF";
const BLACK = "000000";

const FONT = "DejaVu Sans"; // matches the original's glyph metrics

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 5 });

const rect = (x, y, w, h, fill, line = null) => {
  const opts = { x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill } };
  if (line) opts.line = { color: line.color, width: line.width };
  return slide.addShape(pptx.ShapeType.rect, opts);
};

const textbox = (x, y, w, h, runs, align, valign, ls) => {
  const opts = {
    x: px(x), y: px(y), w: px(w), h: px(h), align, valign, margin: 0,
    fontFace: FONT,
  };
  if (ls !== null && ls !== undefined) opts.lineSpacing = ls;
  slide.addText(runs, opts);
};

// equation image at exact px/600 size; fx/fy are the image's frame-px top-left
const eqImage = (file, fx, fy, wIn, hIn) => {
  slide.addImage({ path: path.join(ASSETS, file), x: px(fx), y: px(fy),
                   w: wIn, h: hIn });
};
// read the fit sidecar and place an equation so its INK box matches the measured
// original ink box (x0,x1,y0,y1 frame px).
// Horizontal: ink left == x0, ink right == x1. mathtext's rasterised ink is
// 1-2% narrower than the probe extent the fit used, so the image is stretched by
// (orig ink width / raster ink width), anchored on the ink's left edge.
// Vertical: with \dfrac the stack height comes within ~1px of the original, but
// it still varies per equation (the \dfrac stack is not a pure scale function of
// font size), so the image is scaled by (orig ink height / raster ink height) as
// well — a non-uniform stretch on a vector PNG, which is fine: only the ink bbox
// is being fitted, not glyph proportions inside it.
const eqFit = (file, x0, x1, y0, y1) => {
  const j = JSON.parse(fs.readFileSync(path.join(ASSETS, file.replace(".png", ".json")), "utf8"));
  const padPx = j.pad_px || 12;
  const dpi = j.dpi || 600;
  const padIn = padPx / dpi;                       // PAD px -> inches
  const rasterInkW = (j.w_px - 2 * padPx) / dpi * 72; // ink extents, frame px
  const rasterInkH = (j.h_px - 2 * padPx) / dpi * 72;
  const sx = (x1 - x0 + 1) / rasterInkW;
  const sy = (y1 - y0 + 1) / rasterInkH;
  const fx = x0 - padIn * 72 * sx;              // ink left edge -> x0
  const fy = (y0 + y1) / 2 - (j.h_in * 72 * sy) / 2;  // ink v-centre -> band centre
  eqImage(file, fx, fy, j.w_in * sx, j.h_in * sy);
  return j;
};

// ============================================================
// 1. TITLE — "Minimization of Loss function to obtain BEST model parameters"
//    ink x 162..808, y 68..88 (single line, 18pt bold)
//    Red: "Minimization of Loss function to obtain" + "model parameters"
//    Blue: "BEST" (ink x 565..619)
// ============================================================
textbox(162, 69, 700, 30, [
  { text: "Minimization of Loss function to obtain ", options: { color: RED, bold: true, fontSize: 18 } },
  { text: "BEST", options: { color: BLUE, bold: true, fontSize: 18 } },
  { text: " model parameters", options: { color: RED, bold: true, fontSize: 18 } },
], "left", "top", 18);

// ============================================================
// 2. CREAM UPPER BOX + three Loss equations
// ============================================================
rect(72, 102, 821, 176, CREAM, { color: CBORD, width: 1 });
eqFit("eq_005_loss1.png", 98, 544, 109, 150);
eqFit("eq_005_loss2.png", 97, 629, 173, 214);
eqFit("eq_005_loss3.png", 98, 522, 230, 271);

// ============================================================
// 3. BLUE UPPER BOX — Remember / X is a matrix... / X^T(XW) = (XW)^T X
// ============================================================
rect(676, 134, 207, 105, BLUEF, { color: BBORD, width: 1 });
// UNITS ARE FRAME PX. Every box must exceed the rendered ink (measured with the
// LibreOffice probe: "Remember" 12pt bold 72 px, body lines 14pt 191 / 101 px,
// "Get Best W..." 18pt 314 px, title 18pt bold 644 px) by >=20 px on BOTH sides
// — a snug box makes LO shrink/wrap the text and the render loses 25%+ of its ink.
textbox(681, 138, 130, 24, [
  { text: "Remember", options: { color: RED, bold: true, fontSize: 12 } },
], "left", "top", 12);
textbox(681, 158, 230, 26, [
  { text: "X is a matrix, W is a vector,", options: { color: BLACK, fontSize: 14 } },
], "left", "top", 14);
textbox(681, 179, 150, 26, [
  { text: "XW is a vector", options: { color: BLACK, fontSize: 14 } },
], "left", "top", 14);
eqFit("eq_005_remember1.png", 680, 864, 213, 235);

// ============================================================
// 4. PINK BAND — ∂Loss/∂W = 0 (left) | Get Best W that minimizes the loss (right)
// ============================================================
rect(73, 288, 434, 56, PINKF, { color: PBORD, width: 1 });
eqFit("eq_005_pinkfrac.png", 79, 164, 294, 338);
textbox(196, 303, 350, 28, [
  { text: "Get Best W that minimizes the loss", options: { color: BLACK, fontSize: 18 } },
], "left", "top", 18);

// ============================================================
// 5. CREAM LOWER BOX + two derivative equations
// ============================================================
rect(72, 358, 821, 165, CREAM, { color: CBORD, width: 1 });
eqFit("eq_005_deriv1.png", 97, 592, 375, 417);
eqFit("eq_005_deriv2.png", 96, 637, 460, 502);

// ============================================================
// 6. BLUE LOWER BOX — Remember / X^T(XW) = (XW)^T X
// ============================================================
rect(656, 372, 217, 51, BLUEF, { color: BBORD, width: 1 });
textbox(661, 376, 130, 24, [
  { text: "Remember", options: { color: RED, bold: true, fontSize: 12 } },
], "left", "top", 12);
eqFit("eq_005_remember2.png", 660, 867, 395, 420);

// ============================================================
// 7. GREEN OUTLINE around the final W formula
// ============================================================
rect(688, 464, 192, 35, GFILL, { color: GRING, width: 1 });
eqFit("eq_005_finalw.png", 690, 878, 465, 497);

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch((err) => {
  console.error("ERROR:", err);
  process.exit(1);
});
