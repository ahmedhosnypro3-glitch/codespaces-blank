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
//     3. "Gradient Descent Path to reach Minima" x 474..611, y 354..391
//     4. "Non-Convex Multiple Minima"            x 382..518, y 452..489
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
//   Thin RED RECTANGLE enclosing each plot (measured frame px, drawn as 2-D
//     figure-fraction artists inside each PNG):
//     TL x88..409 y114..291 | TR x619..876 y118..314
//     BL x80..472 y292..527 | BR x466..882 y342..532
//   CAPTION-TO-PLOT ASSIGNMENT is by measured X-OVERLAP with the plot: the top
//     row's LB1 (x270..406) overlaps TL (x86..409) = concave and LB2
//     (x475..611) overlaps TR (x472..876) = convex, so in the bottom row LB3
//     (x474..611) overlaps BR = the gradient-descent path and LB4 (x382..518)
//     overlaps BL = the multi-extremum surface. The analysis JSON's
//     "right of / left of" phrasings are unreliable (they describe LB1 as
//     "right of the top-left plot" when it actually sits ON TL), so the frame
//     geometry wins.
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
const LABEL_BLUE = "0000A0";
const CAPTION_YEL = "FFFF00"; // first word of the top caption boxes (measured)
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

// ── four 3-D surface plots (unscaled images at measured figure size) ─────────
// The original puts each plot in a SMALL white figure (measured from the
// frame's white-background blocks, snug around the cube + its axis labels) with
// a red border ~3px inside its own edge; the label boxes sit in the gutters
// BESIDE them, never over them. Measured figure boxes (frame px):
//   TL x85..265 y115..288 (180x173) | TR x616..879 y115..317 (263x202)
//   BL x83..376 y290..527 (293x237) | BR x615..880 y344..531 (265x187)
// Each PNG is 300dpi with figsize = box_px/72, so placing it at box_px/72 inches
// is exact — no rescale, no resampling ripple. Red reference lines and the BL
// annotations are drawn INSIDE these PNGs (2-D figure-fraction overlays), so
// their measured slide-space positions are preserved exactly.
slide.addImage({ path: path.join(assetsDir, "plot_025_tl.png"),
                 x: px(85),  y: px(115), w: 180 / 72, h: 173 / 72 });
slide.addImage({ path: path.join(assetsDir, "plot_025_tr.png"),
                 x: px(616), y: px(115), w: 263 / 72, h: 202 / 72 });
slide.addImage({ path: path.join(assetsDir, "plot_025_bl.png"),
                 x: px(83),  y: px(290), w: 293 / 72, h: 237 / 72 });
slide.addImage({ path: path.join(assetsDir, "plot_025_br.png"),
                 x: px(615), y: px(344), w: 265 / 72, h: 187 / 72 });

// ── thin red REFERENCE LINES (slide-level, exact measured frame px) ───────────
// The original's reference lines are pure HORIZONTAL 2-D strokes (uniform
// 1-2px runs at constant frame y) and they run PAST the figure image's own
// bounds (TL y186 reaches x281 while its image ends at x265; BL y418 reaches
// x382 while its image ends at x376). Drawn as figure-fraction artists inside
// a PNG they clip at the image edge, so they are drawn here as 2-frame-px tall
// strips at the measured coordinates instead (drawn after the images, so they
// sit on top exactly as in the original).
//   TL  y168 x119..267   y186 x109..281
//   TR  y226 x633..875   y234 x644..867
//   BL  y418 x124..382
//   BR  none
const REFLINES = [
  [168, 119, 267],   // TL maximum level, upper
  [186, 109, 281],   // TL maximum level, lower
  [200, 88, 274],    // TL third reference line (measured y200..201 x88..274)
  [226, 633, 875],   // TR minimum level, upper
  [234, 644, 867],   // TR minimum level, lower
  [417, 124, 382],   // BL single reference line
];
// TR slanted strokes (measured red-pixel map): A (860,189)->(655,209)
// descending-left, B (737,210)->(755,225) descending-right into the y226 line.
slide.addShape(pptx.ShapeType.line, {
  x: px(655), y: px(189), w: px(205), h: px(20), flipV: true,
  line: { color: RED, width: 1 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(737), y: px(210), w: px(18), h: px(15),
  line: { color: RED, width: 1 },
});
for (const [ry, rx0, rx1] of REFLINES) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(rx0), y: px(ry), w: (rx1 - rx0 + 1) / 72, h: 2 / 72,
    fill: { color: RED }, line: { type: "none" },
  });
}

// ── four blue label boxes with white bold text ───────────────────────────────
// The white text in EVERY box sits in TWO bands (measured: band pitch ~12px,
// e.g. box 1 bands y147..154 + y163..169; box 2 y195..201 + y210..216; box 3
// y362..369 + y377..384; box 4 y460..466 + y474..482) — all four labels wrap
// onto two lines, so each gets a two-line text box with lineSpacing pinned to
// reproduce the ~12px band pitch (~0.25in at 11pt).
const labels = [
  { runs: [
      { text: "Concave", options: { color: CAPTION_YEL } },
      { text: " Function", options: { color: WHITE, breakLine: true } },
      { text: "One Maxima", options: { color: WHITE } },
    ], x: 270, y: 137, w: 137, h: 42 },
  { runs: [
      { text: "Convex", options: { color: CAPTION_YEL } },
      { text: " Function", options: { color: WHITE, breakLine: true } },
      { text: "One Minima", options: { color: WHITE } },
    ], x: 475, y: 184, w: 137, h: 42 },
  { runs: [
      { text: "Gradient Descent", options: { color: WHITE, breakLine: true } },
      { text: "Path to reach Minima", options: { color: WHITE } },
    ], x: 474, y: 354, w: 138, h: 38 },
  { runs: [
      { text: "Non-Convex", options: { color: WHITE, breakLine: true } },
      { text: "Multiple Minima", options: { color: WHITE } },
    ], x: 382, y: 452, w: 137, h: 38 },
];
for (const L of labels) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
    fill: { color: LABEL_BLUE },
  });
  const opts = {
    x: px(L.x), y: px(L.y), w: px(L.w), h: px(L.h),
    align: "center", valign: "middle", fontSize: 11, bold: true,
    color: WHITE, fontFace: FONT, margin: 0, lineSpacing: 12,
  };
  if (L.runs) slide.addText(L.runs, opts);
  else slide.addText(L.text, opts);
}

const OUT = path.join(outDir, "slide_025_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
