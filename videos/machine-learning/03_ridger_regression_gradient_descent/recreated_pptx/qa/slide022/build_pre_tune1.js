// slide_022.js — "[3] Inverse of High Dimension / (non-singular) Matrix"
// (ML lecture 03, Ridge Regression & Gradient Descent). Root slide: no parents,
// no children in the founder dependency graph.
//
// Ground truth: PIL-measured from unique_slides/slide_022.jpg (960x540, 1px=1pt),
// measurement scripts banked in qa/slide022/measure_frame_1.py, measure_frame_2.py,
// measure_cursor.py:
//   - Title line 1 "[3] Inverse of High Dimension": red ink x 189..726 (w 538),
//     glyph band y 235..274 (40 rows incl. JPEG halo; dense core 244..266,
//     cap/bracket tops 235-236, descender+bracket bottoms 273-274), ink center
//     (457.5, 254.5). NOTE: 22.5px LEFT of slide center 480 — the original's
//     title block is NOT centered on the slide (same family trait as slide 020:
//     its centers measured 458.5/463.5); frame wins (measured over intuition).
//   - Title line 2 "(non-singular) Matrix": red ink x 274..652 (w 379), glyph
//     band y 325..364, ink center (463.0, 344.5). Baseline pitch = 90px.
//   - Font size: Arial Bold 38pt — Liberation Sans Bold (Arial metric twin)
//     advance fit: L1 536px vs measured 538 (d=2), L2 378px vs 379 (d=1);
//     both lines agree at 38pt. (Spec pinned 48pt from a 44-54 estimate —
//     the frame measurement wins; sibling 020 measured 34pt the same way and
//     certified PASS.) Band-height ratio 40/38 = 1.05em matches 020's 35/34.
//   - NO underline (unlike sibling 020): longest solid red run in the title
//     zone is 39px (glyph strokes only) — no bar exists under either line.
//   - Title color: darkest-core px (121,1,13) = JPEG-darkened C00000 — the
//     founder-ratified family nominal (same law as slide 020's (134,10,22)
//     cores and the chrome strokes; house_chrome.js header note).
//   - Badge numeral: 22 (file number, printed on the original frame — verified
//     in the raw analysis verbatim_text.labels) — house chrome module.
//   - Mouse cursor: washed-out pointer sliver x 519..556, y 311..325 (the
//     analysis' claimed (44%,50%)=(422,270) position was wrong; measured
//     (519..556, 311..325), just above L2's right-center). Video-capture
//     artifact, OMITTED per judge GROUND RULES (c) + recreation_brief step 5.
//   - Full-frame panel-interior ink census: ONLY badge cluster (y54..94),
//     L1 (y234..274), L2 (y311..365 incl. cursor) — zero ink between badge and
//     L1, zero ink below L2. No other content on the slide.
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry, numeral 22).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

// ---- measured constants (frame px; 1px = 1pt = 1/72 in) --------------------
const RED = "C00000"; // family nominal (founder-ratified; see header note)
const FONT = "Arial";

const TITLE_L1 = "[3] Inverse of High Dimension";
const TITLE_L2 = "(non-singular) Matrix";

// Ink targets measured from the frame (inclusive-of-halo bboxes; the self-check
// runs the SAME red mask on render and original so halo cancels on both sides).
const L1_INK = { cx: 457.5, cy: 254.5 };  // ink bbox x 189..726, y 235..274
const L2_INK = { cx: 463.0, cy: 344.5 };  // ink bbox x 274..652, y 325..364

// closed-loop tuning knobs (frame-px deltas applied per element; tuned by
// qa/slide022/selfcheck_attempt_1.py against the 150dpi render, same law as
// slide_020's TUNE). Initial: valign-middle box center sits ~3px above the
// 38pt ink center (ink center = baseline - 0.259em vs linebox center =
// baseline - 0.3465em => 0.0875em x 38pt = 3.3px).
const TUNE = {
  l1: { size: 38, charSpacing: null, dx: 0, dy: 0 },
  l2: { size: 38, charSpacing: null, dx: 0, dy: 0 },
};

const px = (v) => v / 72;

// Text boxes: width = measured advance (538/379) + >=20% wrap budget = 660px
// (boxes wrap at BOX width, not ink width — building.md wrap-budget law).
// Each line is its own SINGLE-LINE box (independent placement = exact 90px
// pitch control; sibling 020 pattern, certified). Single-line boxes need no
// lineSpacing pin (explicit-line-spacing law applies to multi-line boxes);
// the self-check asserts one-band-per-element.
const BOX_W = 660;
const BOX_H = 60;

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 22 });

// Title line 1 — ink target x 189..726, y 235..274
const t1 = TUNE.l1;
const l1opts = {
  x: px(L1_INK.cx - BOX_W / 2 + t1.dx), y: px(L1_INK.cy - 3 - BOX_H / 2 + t1.dy),
  w: px(BOX_W), h: px(BOX_H),
  align: "center", valign: "middle", fontSize: t1.size, bold: true,
  color: RED, fontFace: FONT, margin: 0,
};
if (t1.charSpacing !== null) l1opts.charSpacing = t1.charSpacing;
slide.addText(TITLE_L1, l1opts);

// Title line 2 — ink target x 274..652, y 325..364
const t2 = TUNE.l2;
const l2opts = {
  x: px(L2_INK.cx - BOX_W / 2 + t2.dx), y: px(L2_INK.cy - 3 - BOX_H / 2 + t2.dy),
  w: px(BOX_W), h: px(BOX_H),
  align: "center", valign: "middle", fontSize: t2.size, bold: true,
  color: RED, fontFace: FONT, margin: 0,
};
if (t2.charSpacing !== null) l2opts.charSpacing = t2.charSpacing;
slide.addText(TITLE_L2, l2opts);

const OUT = path.resolve(__dirname, "../slide_022_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
