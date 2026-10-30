// slide_025.js — "Types of Loss function shapes" (ML lecture 03, Ridge
// Regression & Gradient Descent). Root slide: no parents, no children.
//
// Ground truth: PIL-measured from unique_slides/slide_025.jpg (960x540,
// 1px = 1pt = 1/72 in). This is a diagram-only slide (verbatim_text.bullets
// empty, no subtitle): the whole body is a 2x2 grid of 3-D surface plots with
// four blue label boxes between the columns.
//
// Measured ink (frame px, inclusive):
//   Title "Types of Loss function shapes" — red ink x 266..585 (w 319), y 63..88,
//     center x 425.5, ascender-to-descender 26px => Arial Bold ~22pt.
//   Badge numeral 25 — house chrome (drawHouseChrome).
//   Four blue label boxes, fill 0000FF-family, white bold text, ~h 42/38px:
//     1. "Concave Function One Maxima"          x 270..406, y 137..178
//     2. "Convex Function One Minima"           x 475..611, y 184..225
//     3. "Non-Convex Multiple Minima"           x 474..611, y 354..391
//     4. "Gradient Descent Path to reach Minima" x 382..518, y 452..489
//     Every box's white text sits in TWO bands (band pitch ~12px) — all four
//     labels wrap to two lines.
//   Four 3-D surface plots (jet/rainbow), white-background figure rects
//     measured from the frame (non-panel, non-gray bboxes per column):
//     TL concave dome  x 60..470  y 116..289  (411 x 174)
//     TR convex bowl   x 470..901 y 116..316  (431 x 200)
//     BL non-convex    x 60..470  y 296..527  (411 x 231)
//     BR GD path       x 470..901 y 346..530  (431 x 184)
//   Red reference lines are HORIZONTAL 2-D strokes in the original (uniform
//     1-2px runs at constant frame y), measured inside the plot rects:
//     TL  y168 x121..267  and  y186 x110..279   (maximum level, upper)
//     TR  y222 x619..873  and  y234 x619..866   (minimum level, lower)
//     BL  y418 x124..381                          (single reference line)
//     BR  none — the ink at y371..396 x698..875 in that region is jet
//         colormap, NOT a line (analysis agrees: no red line on this plot).
//   BL black annotations measured at (slide px): "Global Maxima"
//     ~x242..268 y304..319, "Local Maxima" ~x286..315 y337..352,
//     "Local Minima" ~x286..311 y390..399, "Global Minima" ~x145..201 y439..465.
//
// Assets: plot_025_tl/tr/bl/br.png generated at 300dpi at the EXACT measured
//   region size (figsize = region_px / 72), so addImage() places them
//   unscaled at region_px/72 inches — no resampling, no ripple. Surface is a
//   single dense analytic array per plot (90..120 grid), shade=True gives the
//   smooth MATLAB-style shading. Banked in build/assets/ via
//   build/generate_plots_025.py.
//
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry,
// numeral 25; NO top stroke — correct for this deck).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const outDir = path.resolve(__dirname, "..");
const assetsDir = path.resolve(__dirname, "assets");
const px = (v) => v / 72;

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 25 });

const RED = "C00000";      // family nominal (founder-ratified; see sibling 024 header)
const LABEL_BLUE = "0000FF";
const WHITE = "FFFFFF";
const FONT = "Arial";

// ── title ────────────────────────────────────────────────────────────────────
// Ink x 266..585 (w 319), y 63..88 — center x 425.5; ascender-to-descender
// 26px => Arial Bold ~22pt. The box must be wide enough that the string never
// wraps (a wrapped title pushes ink above frame y52 and trips the chrome
// checker's top-stroke law).
{
  const size = 22;
  const boxW = 420, boxH = 40;
  slide.addText("Types of Loss function shapes", {
    x: px(425.5 - boxW / 2), y: px(75.5 - 0.079 * size - boxH / 2),
    w: px(boxW), h: px(boxH),
    align: "center", valign: "middle", fontSize: size, bold: true,
    color: RED, fontFace: FONT, margin: 0,
  });
}

// ── four 3-D surface plots (unscaled images at measured region size) ─────────
// TL 400x174, TR 418x200, BL 400x231, BR 418x184 frame px. Each PNG is 300dpi
// with figsize = region_px/72, so placing it at region_px/72 inches is exact —
// no rescale, no resampling ripple. Red reference lines and the BL annotations
// are drawn INSIDE these PNGs (2-D figure-fraction overlays), so their measured
// slide-space positions are preserved exactly.
slide.addImage({ path: path.join(assetsDir, "plot_025_tl.png"),
                 x: px(60),  y: px(116), w: 400 / 72, h: 174 / 72 });
slide.addImage({ path: path.join(assetsDir, "plot_025_tr.png"),
                 x: px(480), y: px(116), w: 418 / 72, h: 200 / 72 });
slide.addImage({ path: path.join(assetsDir, "plot_025_bl.png"),
                 x: px(60),  y: px(296), w: 400 / 72, h: 231 / 72 });
slide.addImage({ path: path.join(assetsDir, "plot_025_br.png"),
                 x: px(480), y: px(346), w: 418 / 72, h: 184 / 72 });

// ── four blue label boxes with white bold text ───────────────────────────────
// The white text in EVERY box sits in TWO bands (measured: band pitch ~12px,
// e.g. box 1 bands y147..154 + y163..169; box 2 y195..201 + y210..216; box 3
// y362..369 + y377..384; box 4 y460..466 + y474..482) — all four labels wrap
// onto two lines, so each gets a two-line text box with lineSpacing pinned to
// reproduce the ~12px band pitch (~0.25in at 11pt).
const labels = [
  { text: "Concave Function One Maxima",           x: 270, y: 137, w: 137, h: 42 },
  { text: "Convex Function One Minima",            x: 475, y: 184, w: 137, h: 42 },
  { text: "Non-Convex Multiple Minima",            x: 474, y: 354, w: 138, h: 38 },
  { text: "Gradient Descent Path to reach Minima", x: 382, y: 452, w: 137, h: 38 },
];
for (const L of labels) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
    fill: { color: LABEL_BLUE },
  });
  slide.addText(L.text, {
    x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
    align: "center", valign: "middle", fontSize: 11, bold: true,
    color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
  });
}

const OUT = path.join(outDir, "slide_025_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
