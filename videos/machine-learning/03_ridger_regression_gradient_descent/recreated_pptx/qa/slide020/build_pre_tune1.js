// slide_020.js — "[2] Ridge Regularization to overcome / Inverse Problem of Singular Matrix"
// (ML lecture 03, Ridge Regression & Gradient Descent). Root slide: no parents, no children.
//
// Ground truth: PIL-measured from unique_slides/slide_020.jpg (960x540, 1px=1pt),
// measurement scripts banked in qa/slide020/measure_frame*.py:
//   - Title line 1 "[2] Ridge Regularization to overcome": red ink x 159..758 (w 600),
//     glyph band y 230..264 (ascender->descender, 35 rows) => Arial BOLD 34pt
//     (advance fit: 17.670em x 34pt = 600.8px vs measured 600), ink center (458.5, 247).
//     NOTE: measured center is 21px LEFT of slide center 480 — the original's title
//     block is NOT centered on the slide; frame wins (measured over intuition).
//   - Title line 2 "Inverse Problem of Singular Matrix": red ink x 183..744 (w 562),
//     glyph band y 310..344, ink center (463.5, 327). Baseline-to-baseline pitch = 80px.
//   - UNDERLINE under line 2 (spec: "second line underlined"): solid red bar rows
//     338/339/340 (562 px wide = full glyph ink width), AA rows 337/341. Drawn as an
//     explicit filled rect at the measured band (renderer-native underlines drift
//     between LO and PowerPoint; measured geometry is the law).
//   - Badge numeral: 20 (file number, printed on original) — house chrome module.
//   - Mouse cursor at x 454..470 y 397..414: video-capture artifact, OMITTED per
//     judge GROUND RULES (c) and recreation_brief step 5.
//   - Title color: darkest-core px ~ (134,10,22) = JPEG-darkened C00000 — the
//     founder-ratified family nominal (spec: #C00000; same law as chrome strokes,
//     house_chrome.js note: 02's certified C00000 builds PASS against these frames).
//   - NO other content on the slide (full-frame ink cluster census: only title words,
//     badge cluster, cursor cluster — measure_frame2.py).
// House chrome: shared_patterns/house_chrome.js (THIS deck's geometry, numeral 20).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

// ---- measured constants (frame px; 1px = 1pt = 1/72 in) --------------------
const RED = "C00000"; // family nominal (founder-ratified; see header note)
const FONT = "Arial";

const TITLE_L1 = "[2] Ridge Regularization to overcome";
const TITLE_L2 = "Inverse Problem of Singular Matrix";

// closed-loop tuning knobs (frame px deltas applied per element)
const TUNE = {
  l1: { size: 34, charSpacing: null, dx: 0, dy: 0 },
  l2: { size: 34, charSpacing: null, dx: 0, dy: 0 },
  underline: { dx: 0, dy: 0 },
};

const px = (v) => v / 72;

// Text boxes: width = measured advance (601/559) + ~20% wrap budget = 720px.
// valign middle centers the LINE BOX, whose ink sits ~3px below its center for
// 34pt Arial (ink center = baseline - 0.259em vs linebox center = baseline - 0.3465em),
// so box centers start 3px above the ink-center targets (247 / 327) and the
// render loop tunes dy.
const BOX_W = 720;
const BOX_H = 60;

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 20 });

// Title line 1 — ink target x 159..758, y 230..264
const t1 = TUNE.l1;
const l1opts = {
  x: px(458.5 - BOX_W / 2 + t1.dx), y: px(247 - 3 - BOX_H / 2 + t1.dy),
  w: px(BOX_W), h: px(BOX_H),
  align: "center", valign: "middle", fontSize: t1.size, bold: true,
  color: RED, fontFace: FONT, margin: 0,
};
if (t1.charSpacing !== null) l1opts.charSpacing = t1.charSpacing;
slide.addText(TITLE_L1, l1opts);

// Title line 2 — ink target x 183..744, glyph y 310..344
const t2 = TUNE.l2;
const l2opts = {
  x: px(463.5 - BOX_W / 2 + t2.dx), y: px(327 - 3 - BOX_H / 2 + t2.dy),
  w: px(BOX_W), h: px(BOX_H),
  align: "center", valign: "middle", fontSize: t2.size, bold: true,
  color: RED, fontFace: FONT, margin: 0,
};
if (t2.charSpacing !== null) l2opts.charSpacing = t2.charSpacing;
slide.addText(TITLE_L2, l2opts);

// Underline under line 2 — measured bar: x 183..744 (w 562), rows 338..340 core
slide.addShape(pptx.ShapeType.rect, {
  x: px(183 + TUNE.underline.dx), y: px(338 + TUNE.underline.dy),
  w: px(562), h: px(3),
  fill: { color: RED },
  // no line option => no outline (house_chrome.js panel pattern)
});

const OUT = path.resolve(__dirname, "../slide_020_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
