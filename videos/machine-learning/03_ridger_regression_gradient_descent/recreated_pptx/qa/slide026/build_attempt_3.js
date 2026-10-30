// Build script for slide 026 — "Gradient Descent Solution"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (lecture 03)
//
// GEOMETRY LAW: every value below is a MEASURED frame pixel from the banked 8-pass
// measurement bank (qa/slide026/measure_frame*.py + _out.txt, 2026-10-19/20) — frame
// 960x540, 1px = 1pt = 1/72in. Font fit calibrated against the banked ink widths
// (scratch/tmp/calib2_026.py): Arial/Liberation 17.5pt fits ALL measured text lines
// within +/-2.1% (rowA -0.5%, rowB +2.0%, rowC ~-2.6%, rowD -2.0%, N1 -1.6%,
// N2 +0.8%, N3 +2.1%, N4 +0.9%); title bold 27.5pt (adv 345.3 vs ink 346);
// section headers bold 17.5pt (GD hdr 280.5 vs 283; Notes hdr 51.6 vs 51).
//
// MEASURED TARGETS (frame px, from the bank):
//   Blue content box: border cols 82-83 (L) / 862-864 (R), rows 90-92 (T) / 498-500 (B)
//     => box x82..864, y90..500, white interior (255,255,255), border nominal 0000FF
//     (core (0,0,97)), thin. Title red ink y60..82 x294..639 (center 466.5), no descenders.
//   Algorithm steps start x146; section headers + notes text start x109; bullet discs
//     d=7 at x91..97 (N1 y346..352, N3 y446..451), black.
//   Line bands (ink tops): GD hdr 110 | rowA 143 | rowB 177 | rowC 210 | rowD 243
//     (pitch 33-34) | Notes hdr 310 | N1 342 | N2 376 | N3 441 | N4 475;
//     N2->N3 gap = 65px (an extra blank line between the two Notes bullets).
//   UNDERLINE BARS (measured, solid runs): rowB y192..194 x349..716
//     ("moving along the direction of negative gradient"); rowD y258..260 x287..473
//     ("gradient is almost zero"); N3 y458 x177..277 ("approximately") and
//     x538..728 ("variable number of steps"). Rendered as run-level underline: true
//     (PPT underline sits ~2-3px below the baseline = exactly where the bars are).
//   RED-ON-BLUE: the tail of row C, "AKA Learning Rate)" x518..689, is RED
//     (C00000 family) in the original (measure_frame2 run classification + the
//     2026-10-20 tiebreak probe) — the analysis brief says blue; THE FRAME WINS.
//   Bold spans — validated against the banked ink widths (bank run width vs this build's
//   measured advance, calibrated on the regular controls; halo bound +0..+4, kern/gap
//   bound -7..+2 for multi-word runs). Kept bold where the frame agrees with the brief:
//     rowA "Random Weights (W)"; rowB "negative gradient" (underlined);
//     rowC "moving step is a hyper parameter" + "AKA Learning Rate" (red);
//     rowD "almost zero" (underlined); N1 "is a convex function"; N2 "ONE Minimum";
//     N4 "Learning Rate".
//   REGULAR (brief over-claimed bold — the frame wins, measured):
//     rowB "Loss function" (bank ink 5-6px narrower than this build's bold advances);
//     N3 "variable number of steps" (bank w191 = regular sim 191; bold would be 207);
//     rowC "w.r.t. W" (bank w43/w23 = regular; bold would be +3).
//
// DEVIATIONS FROM SPEC (law hierarchy: deck AGENTS.md + judge_protocol_03.md +
// runbook OVERRIDE the analysis spec; frame measurement overrides intuition):
//   1. House chrome (white canvas FFFFFF; gray E9E9E7 panel x54..903 y45..540; thin
//      C00000 1pt strokes LEFT/RIGHT/BOTTOM only — NO TOP STROKE; badge FDFD96 with
//      6A5ACD ring, numeral 26) via shared_patterns/house_chrome.js per deck AGENTS.md.
//      The spec's "#F0F0F0 background / #FFFF00 badge" are vision misreads; house law wins.
//   2. Spec's vague percentage positions replaced by the measured pixel geometry above.
//   3. Spec says step [2] is entirely blue; measured row C tail "AKA Learning Rate)"
//      is red — drawn red (frame wins).
//
// Single version deliverable: recreated_pptx/slide_026_recreated.pptx (no suffixes).

const pptxgenpkg = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const PX = 1 / 72; // frame px -> inches
const RED = "C00000";   // no '#' in pptxgenjs hex
const BLUE = "0000FF";
const BLACK = "000000";
const FONT = "Arial";
const BODY = 17.5;   // measured global fit for all body lines
const TITLE = 27.5;  // measured fit (bold)
const HDR = 17.5;    // section headers: bold + red, measured same pt as body

// ---- measured geometry (frame px) ---------------------------------------------------
const BOX = { x: 82, y: 90, w: 783, h: 411 };            // blue content box x82..864 y90..500
const LINES = {
  gdhdr:   { base: 123, x: 109 },   // "Gradient Descent (GD) Algorithm:" (cap top 110)
  rowA:    { base: 156, x: 146 },   // cap top 143
  rowB:    { base: 190, x: 146 },   // cap top 177
  rowC:    { base: 223, x: 146 },   // cap top 210
  rowD:    { base: 256, x: 146 },   // cap top 243
  noteshdr:{ base: 323, x: 109 },   // "Notes:" (cap top 310)
  N1:      { base: 355, x: 109 },   // cap top 342
  N2:      { base: 385, x: 109 },   // x-height top 376
  N3:      { base: 454, x: 109 },   // cap top 441
  N4:      { base: 488, x: 109 },   // ascender top 475
};
// title: ink x294..639, no descenders => baseline = ink bottom = 82
const TITLE_BASE = 82, TITLE_X = 294;

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

const slide = pptx.addSlide();

// House chrome: white canvas, gray panel, red L/R/Bottom strokes (NO top), badge "26"
drawHouseChrome(pptx, slide, { numeral: 26 });

// --- blue-bordered white content box -------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: BOX.x * PX, y: BOX.y * PX, w: BOX.w * PX, h: BOX.h * PX,
  fill: { color: "FFFFFF" },
  line: { color: BLUE, width: 1.25 },  // measured border 2-3px @150dpi => ~1.25pt
});

// ---- text helper ---------------------------------------------------------------------
// One text box PER LINE at its measured baseline (immune to PowerPoint-vs-LO auto
// pitch divergence; per-line boxes have no pitch to diverge on). BASELINE_OFFSET is
// the measured box-top -> baseline distance in em (LO natural pitch, valign top,
// margin 0); calibrated closed-loop against the 150dpi render in the selfcheck.
const BASELINE_OFFSET_EM = 1.0;
function line(key, runs, sizePx, widthPx) {
  const g = LINES[key];
  const topPx = g.base - sizePx * BASELINE_OFFSET_EM;
  slide.addText(runs, {
    x: g.x * PX, y: topPx * PX, w: widthPx * PX, h: 30 * PX,
    valign: "top", align: "left", margin: 0, fontFace: FONT,
  });
}
const r = (text, opts) => ({ text: text, options: opts });

// ---- title (red bold 27.5pt, ink x294..639) ------------------------------------------
slide.addText([r("Gradient Descent Solution", { bold: true })], {
  x: TITLE_X * PX, y: (TITLE_BASE - TITLE * BASELINE_OFFSET_EM) * PX,
  w: 380 * PX, h: 34 * PX,
  fontSize: TITLE, bold: true, color: RED, fontFace: FONT,
  valign: "top", align: "left", margin: 0,
});

// ---- section header: "Gradient Descent (GD) Algorithm:" (red bold) --------------------
line("gdhdr", [r("Gradient Descent (GD) Algorithm:", { bold: true, color: RED, fontSize: HDR })], HDR, 300);

// ---- algorithm steps (blue 17.5pt) -----------------------------------------------------
// [1] — bold "Random Weights (W)"
line("rowA", [
  r("[1] Start with initial ", { color: BLUE, fontSize: BODY }),
  r("Random Weights (W)", { color: BLUE, fontSize: BODY, bold: true }),
], BODY, 350);

// [2] line 1 — underline "moving along the direction of negative gradient" (measured bar),
// bold "negative gradient" ONLY. "Loss function" is REGULAR in the frame: the banked ink
// runs "Loss" (x742..777, w35) and "function" (x783..846, w63) are 5-6px NARROWER than
// this build's bold advances (41 / 68), while the single-word controls ("Start" w36,
// "weights" w59, "(w.r.t." w70) sit within -1..+4 of their advances — the same test that
// proves the brief's "w.r.t. W" (also claimed bold) is actually regular. Vision over-
// detected bold here; the frame wins.
line("rowB", [
  r("[2] Update the weights by ", { color: BLUE, fontSize: BODY }),
  r("moving along the direction of ", { color: BLUE, fontSize: BODY, underline: true }),
  r("negative gradient", { color: BLUE, fontSize: BODY, bold: true, underline: true }),
  r(" of Loss function", { color: BLUE, fontSize: BODY }),
], BODY, 730);

// [2] line 2 — blue until "parameter,", then RED bold "AKA Learning Rate" (measured red)
line("rowC", [
  r("(w.r.t. W) (", { color: BLUE, fontSize: BODY }),
  r("moving step is a hyper parameter,", { color: BLUE, fontSize: BODY, bold: true }),
  r(" ", { color: BLUE, fontSize: BODY }),
  r("AKA Learning Rate", { color: RED, fontSize: BODY, bold: true }),
  r(")", { color: RED, fontSize: BODY }),
], BODY, 560);

// [3] — underline "gradient is almost zero" (measured bar x287..473 is CONTINUOUS:
// the space between the runs must be underlined too or the bar splits in two)
line("rowD", [
  r("[3] Stop when the ", { color: BLUE, fontSize: BODY }),
  r("gradient is ", { color: BLUE, fontSize: BODY, underline: true }),
  r("almost zero", { color: BLUE, fontSize: BODY, bold: true, underline: true }),
  r(" (this is at the minimum value of the function)", { color: BLUE, fontSize: BODY }),
], BODY, 700);

// ---- section header: "Notes:" (red bold) ----------------------------------------------
line("noteshdr", [r("Notes:", { bold: true, color: RED, fontSize: HDR })], HDR, 90);

// ---- notes bullets (black 17.5pt, round disc markers d=7px at x91) ---------------------
const bullet = (topPx) => slide.addShape(pptx.ShapeType.ellipse, {
  x: 91 * PX, y: topPx * PX, w: 7 * PX, h: 7 * PX,
  fill: { color: BLACK },
});
bullet(346); // N1 disc y346..352 (measured)
bullet(446); // N3 disc y446..451 (measured)

// Note 1 line 1 — bold "is a convex function"
line("N1", [
  r("Least Squares Linear regression objective function ", { color: BLACK, fontSize: BODY }),
  r("is a convex function", { color: BLACK, fontSize: BODY, bold: true }),
  r(" (even with", { color: BLACK, fontSize: BODY }),
], BODY, 680);

// Note 1 line 2 — bold "ONE Minimum"
line("N2", [
  r("regularizer). This means it has ", { color: BLACK, fontSize: BODY }),
  r("ONE Minimum", { color: BLACK, fontSize: BODY, bold: true }),
  r(" (good news ).", { color: BLACK, fontSize: BODY }),
], BODY, 500);

// Note 2 line 1 — VERBATIM wrap recovered from the bank: the original's N3 line
// has an ink run at x818..836 AFTER "depending" (measure_frame2 N3 runs), and N4's
// measured width (x109..295 = 186px) fits only "the used Learning Rate" — so line 1
// ends "...depending on" and line 2 is "the used Learning Rate" (the "on" belongs to
// line 1, it is NOT optional: dropping it breaks the verbatim contract).
// underline "approximately", underline "variable number of steps" (REGULAR, not bold:
// banked ink run x538..728 (w191) matches this build's REGULAR simulation exactly (191)
// while a bold simulation is 207 — 16px wider, far beyond the +0..+4 halo bound the
// multi-word controls allow; the brief's bold claim for this span is a vision over-read)
line("N3", [
  r("GD will ", { color: BLACK, fontSize: BODY }),
  r("approximately", { color: BLACK, fontSize: BODY, underline: true }),
  r(" find this minimum value but at a ", { color: BLACK, fontSize: BODY }),
  r("variable number of steps", { color: BLACK, fontSize: BODY, underline: true }),
  r(" depending on", { color: BLACK, fontSize: BODY }),
], BODY, 765);

// Note 2 line 2 — bold "Learning Rate"
line("N4", [
  r("the used ", { color: BLACK, fontSize: BODY }),
  r("Learning Rate", { color: BLACK, fontSize: BODY, bold: true }),
], BODY, 210);

pptx.writeFile({ fileName: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_026_recreated.pptx" })
  .then(() => console.log("wrote slide_026_recreated.pptx"));
