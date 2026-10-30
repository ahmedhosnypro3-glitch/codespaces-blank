// slide_024.js — "Gradient Descent (GD)" / "and" / "How to apply to minimize Loss function"
// (ML lecture 03, Ridge Regression & Gradient Descent). Root slide: no parents,
// no children in the founder dependency graph (banked as a component anyway —
// playlist-scoped obligation).
//
// Ground truth: PIL-measured from unique_slides/slide_024.jpg (960x540, 1px=1pt),
// measurement scripts banked in qa/slide024/measure_frame.py (predecessor),
// measure_frame_2.py (census + icon + advance fit), measure_frame_3.py (font
// weight/size pinning by blurred-render row-profile simulation, calibrated
// against sibling 022's CERTIFIED render-vs-original halo ratios):
//   - Panel-interior ink census: EXACTLY 5 clusters — badge (y54..94),
//     title (y223..269), "and" (y294..322), subtitle line 2 (y349..381),
//     bottom pen icon (y506..521). No cursor artifact on this frame.
//   - Title "Gradient Descent (GD)": red ink x 242..718 (w 477, center x
//     480.0 = exactly slide-centered), band y 224..268. Cap top ~225.5,
//     baseline ~258.5 (cap height ~33px => Arial BOLD 45pt: 45x0.72=32.4px);
//     the rows 260..268 "tail" is the bottom curves of the (GD) PARENTHESES
//     (two strokes x 625..631 / x 710..717 descending 9.5px = 0.21em x 45pt
//     below baseline) — NOT an underline (no bar exists).
//   - "and": red ink x 451..508 (w 58), band y 294..321 (ascender-to-baseline
//     ~25.7px => BOLD ~34pt; Liberation Bold 34 advance w=57-58 exact).
//     Center x 479.5. NOTE: LARGER than line 3 — the frame shows two
//     different subtitle sizes (validator's "same smaller size" was a guess;
//     frame wins).
//   - "How to apply to minimize Loss function": red ink x 201..759 (w 559),
//     band y 350..380 (cap ~21.5px, descenders 'pp/y' of "apply" to 380)
//     => BOLD 30pt (Liberation Bold 30 advance 565 x render-ratio 0.987 =
//     558 = measured). Center x 480.0.
//   - Weight evidence: Bold sims need 1.20-1.27x halo inflation to match the
//     original's totals, Regular needs ~1.45x; sibling 022's certified Bold
//     build measured 1.33x on the same pipeline => Bold (family law anyway:
//     020/022 titles are Bold Arial).
//   - Bottom pen icon: tiny dark glyph x 464..479, y 506..522; nib triangle
//     x 464..470 y 506..513 (darkest px (468,511)=(15,15,15)) + diagonal
//     shaft (466.5,513)->(475,521.5). Shape ratio (4px nib + 13px shaft) =
//     PEN/PENCIL, not a mouse cursor; the spec INCLUDES it as a slide element
//     (visual_elements + imagery + recreation_brief step 7; validation kept
//     it) — recreated as a 600dpi transparent PNG (gen_icon.py) embedded at
//     EXACT px/600 size, color 404040 (spec; frame core corroborates).
//   - Text color: darkest-core px (151,15,27) = JPEG-darkened C00000 — the
//     founder-ratified family nominal (house_chrome.js header note).
//   - Badge numeral: 24 (file number; house chrome module).
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry,
// numeral 24; NO top stroke — correct for this deck).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

// ---- measured constants (frame px; 1px = 1pt = 1/72 in) --------------------
const RED = "C00000"; // family nominal (founder-ratified; see header note)
const FONT = "Arial";

const TITLE = "Gradient Descent (GD)";
const SUB1 = "and";
const SUB2 = "How to apply to minimize Loss function";

// Ink targets measured from the frame (inclusive halo bboxes; the self-check
// runs the SAME red mask on render and original so halo cancels both sides).
// valign-middle box-center law (sibling 022, certified): box center sits
// ~0.079em ABOVE the ink center (022 measured 3px at 38pt); initial estimate
// box_cy = ink_cy - 0.079*size, TUNE closed-loop after render pass 1.
const T_INK = { cx: 480.0, cy: 246.0, x0: 242, x1: 718, y0: 224, y1: 268 };
const S1_INK = { cx: 479.5, cy: 307.5, x0: 451, x1: 508, y0: 294, y1: 321 };
const S2_INK = { cx: 480.0, cy: 365.0, x0: 201, x1: 759, y0: 350, y1: 380 };

const TUNE = {
  t: { size: 45, charSpacing: null, dx: 0, dy: 0 },
  s1: { size: 34, charSpacing: null, dx: 0, dy: 0 },
  s2: { size: 30, charSpacing: null, dx: 0, dy: 0 },
};

const px = (v) => v / 72;

// Text boxes: width >= measured advance + ~20% wrap budget (boxes wrap at BOX
// width, not ink width — building.md wrap-budget law). Each line is its own
// SINGLE-LINE box (exact pitch control; single-line boxes need no lineSpacing
// pin — explicit-line-spacing law applies to multi-line boxes; the self-check
// asserts one-band-per-element).
const BOX_W = { t: 640, s1: 140, s2: 700 };
const BOX_H = { t: 64, s1: 56, s2: 52 };

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 24 });

// Title — ink target x 242..718, y 224..268
const tt = TUNE.t;
const topts = {
  x: px(T_INK.cx - BOX_W.t / 2 + tt.dx), y: px(T_INK.cy - 0.079 * tt.size - BOX_H.t / 2 + tt.dy),
  w: px(BOX_W.t), h: px(BOX_H.t),
  align: "center", valign: "middle", fontSize: tt.size, bold: true,
  color: RED, fontFace: FONT, margin: 0,
};
if (tt.charSpacing !== null) topts.charSpacing = tt.charSpacing;
slide.addText(TITLE, topts);

// Subtitle line 1 "and" — ink target x 451..508, y 294..321
const s1 = TUNE.s1;
const s1opts = {
  x: px(S1_INK.cx - BOX_W.s1 / 2 + s1.dx), y: px(S1_INK.cy - 0.079 * s1.size - BOX_H.s1 / 2 + s1.dy),
  w: px(BOX_W.s1), h: px(BOX_H.s1),
  align: "center", valign: "middle", fontSize: s1.size, bold: true,
  color: RED, fontFace: FONT, margin: 0,
};
if (s1.charSpacing !== null) s1opts.charSpacing = s1.charSpacing;
slide.addText(SUB1, s1opts);

// Subtitle line 2 — ink target x 201..759, y 350..380
const s2 = TUNE.s2;
const s2opts = {
  x: px(S2_INK.cx - BOX_W.s2 / 2 + s2.dx), y: px(S2_INK.cy - 0.079 * s2.size - BOX_H.s2 / 2 + s2.dy),
  w: px(BOX_W.s2), h: px(BOX_H.s2),
  align: "center", valign: "middle", fontSize: s2.size, bold: true,
  color: RED, fontFace: FONT, margin: 0,
};
if (s2.charSpacing !== null) s2opts.charSpacing = s2.charSpacing;
slide.addText(SUB2, s2opts);

// Bottom-center pen icon — 600dpi transparent PNG at EXACT px/600 size
// (asset law: addImage never rescaled). Canvas 146x163px @600dpi covers the
// measured loose ink window (slide-space x 462.5..480.0, y 504.5..524.1).
slide.addImage({
  path: path.resolve(__dirname, "assets/icon_024_pen.png"),
  x: px(462.5), y: px(504.5), w: 146 / 600, h: 163 / 600,
});

const OUT = path.resolve(__dirname, "../slide_024_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
