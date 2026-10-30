// Build script for slide 023 — "Inverse of High Dimension Matrix"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (lecture 03)
//
// GEOMETRY LAW: every value below is a MEASURED frame pixel taken from the original
// frame unique_slides/slide_023.jpg (960x540, 1px = 1pt = 1/72 in) in the banked
// forensic passes of this session (qa/slide023/forensics_*.py, 2026-10-20/21).
// Text content is VERBATIM from analysis/slide_023_final.json.
//
// MEASURED TARGETS (frame px, ink extents / border centerlines / baselines):
//   Title: RED ink x219..654 y78..104 (cap 19-20, 'g' descender to 104) => Arial bold
//     27.5pt (advance 436.5 == measured ink 436), baseline = 78 + 19.9 = 98.
//   GREEN recall box: strokes center L x97.5 (cols 97-98) R x754.5, T y110.5 (rows
//     110-111) B y218.5 (rows 218-219); fill median (206,255,226) => CEFFE2; border
//     cores avg (84,155,86) => 549B56; sharp corners (verified by hue dump).
//   "Recall" (NO trailing colon - see the adjudication note at the text box) black ITALIC
//     28pt, underlined (bar rows 141-142 x107..178), ink x103..177, cap 21-22 => Arial
//     Italic 28pt. Italic verified on the frame three ways: the 'R' stem leans (top x107
//     vs bottom x103 = 12-17 deg), the column-profile cos is 0.889 (Italic) vs 0.798
//     (Regular), and the analysis typography_notes say so.
//   EQUATION ink x104..429 y150..186 (325x37): multi-colour composite
//     assets/eq_023_main.png (2712x334 @600dpi, PAD 8px = 0.96 frame px) placed so the
//     ink lands exactly at (104,150): image origin (103.04, 149.04), w 4.52 h 0.55667.
//     Colours per frame: body black, lambda+I 008000, superscript -1 C00000; BOTH the
//     W and the Y carry an underline bar (mathtext \underline).
//   DIM NOTE (one line, two runs separated by a wide gap): baseline 211 (ink bottom).
//     part1 "if Feature vectors are of dimension d" x104..409, Arial 19pt (advance 307.8
//     vs 306); the trailing "d" x400..409 is RED.
//     ARROW (judge Template A attempt 1, MAJOR): red "⇒" ink x437..455 y200..209 in the
//     gap - double-shaft shape (two bars y202-203/y206-207 + solid right head x448..455)
//     = DejaVu Sans U+21D2 @25pt, ink exactly 19w x 10h. Arial has no U+21D2. box x436
//     base 224. (Arial has no U+21D2 at all, so the fontFace must be explicit.)
//     part2 "(X^T X) is of size d+1 x d+1" x505..746, Arial 20pt; measured run starts
//     662 / 'x' 701..708 / 714 with wider-than-Arial internal spacing => the four runs
//     are laid out as SEPARATE boxes at their measured left edges (single-box layout
//     drifts 10px on the second half because the original's inter-word gaps are wider
//     than Arial's space advance).
//   BLUE complexity box: strokes center L x87.75 (87-88) R x868.5, T y228.5 B y425.5;
//     fill (248,248,255) => F8F8FF; border cores avg (175,172,206) => B9B6D8.
//     3 navy lines at 33px pitch, baselines 260 / 294 / 327 (caps 243/276/309):
//       L1 "The standard matrix inversion algorithm has a time complexity of O(n^3),"
//          ink x96..835; Arial 23.5pt (advance 749 vs 740); RED "O(n^3)" x774..830 and
//          a RED COMMA at x831..835 y257..264 (hanging 4px below the baseline 260,
//          directly after the ')'). L2 starts "which means" - no leading comma.
//          (judge Template A attempt 1, MINOR: the comma was missing - now added and
//          made RED to match the frame.)
//          (prefix advance 677.9 -> red starts 773.9 == measured 775).
//       L2 "which means that the computation time increases rapidly with the size of"
//          ink x98..835; Arial 23.5pt (752 vs 744).
//       L3 "the matrix (increasing cubically with the number of components)."
//          ink x97..760; Arial 23.5pt (670 vs 664).
//     Colour measured SATURATED NAVY (core (2,0,111)..(14,0,123)) => 000080 (NOT the
//     spec's 1F3864: the frame's badge fill measures faithful (246,255,150) vs
//     FDFD96 (253,253,150) so there is no colour cast, and neutral black text in the
//     same frame measures (0,1,0) with no blue bleed).
//   EX lines INSIDE the blue box, BLACK (core (0,1,0)) + RED numbers:
//     EX1 "For Example: if Features vector is of size 1000 then Inverse calculation is"
//          ink x95..854, baseline 382 ('p' descender to 387); Arial 23.5pt (761 vs 760);
//          RED "1000" x529..577 (prefix 432.3 -> 528.3).
//     EX2 "or order 1,000,000,000 which is impractical"
//          ink x96..541, baseline 416; Arial 23.5pt (448 vs 447); RED
//          "1,000,000,000" x189..327 (prefix 88.8 -> 184.8, 4px early - accepted).
//   YELLOW solution box: strokes center L x87.5 R x874.75, T y435.5 B y530;
//     fill median (250,253,226) => FAFDE2; border cores avg (107,86,46) => 6B562E.
//     "Solution:" navy 000080 bold, ink x96..176, cap 13-15, baseline 464 => Arial bold
//       21pt (advance 82.3 vs 80; cap 15.2 vs 15).
//     SOL1 "Instead of using Least Squares with Matrix inversion," ink x245..710
//       (center 477.5) core y478..496 (h19) => Arial 20pt (468 vs 463), baseline 492.
//     SOL2 "use Gradient Descent iterative solution" ink x313..648 (center 480.5)
//       core y506..521 => Arial 20pt (335 vs 334), baseline 519.
//     Both solution lines are CENTRED (box centre x481 == measured centres 477.5/480.5).
//
// DEVIATIONS FROM SPEC (law hierarchy: deck AGENTS.md + judge_protocol_03.md + runbook
// OVERRIDE the analysis spec; frame measurement overrides intuition):
//   1. House chrome (white canvas, gray E9E9E7 panel x54..903 y45..540, C00000 1pt
//      strokes LEFT/RIGHT/BOTTOM only - NO TOP STROKE, badge FDFD96 + 6A5ACD ring,
//      numeral 23) via shared_patterns/house_chrome.js per deck AGENTS.md.
//   2. Spec's percentage positions replaced by the measured pixel geometry above.
//   3. Spec's 1F3864 navy replaced by the measured saturated navy 000080.
//   4. Spec's table/section framing is a set of three coloured boxes per the frame.
//
// Single version deliverable: recreated_pptx/slide_023_recreated.pptx (no suffixes).
// Equation sidecar: build/assets/eq_023_main.json (for the post-certification OMML wrap,
// which the orchestrator applies after certification - NOT applied here).

const pptxgenpkg = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const PX = 1 / 72; // frame px -> inches
const RED = "C00000";
const BLACK = "000000";
const NAVY = "000080"; // measured saturated navy (frame core (2,0,111))
const FONT = "Arial";

// ---- measured geometry (frame px) ---------------------------------------------------
const BOXES = [
  // green "Recall:" box, strokes x97..754 / y110..219
  { x: 97.5, y: 110.5, w: 657, h: 108, fill: "CEFFE2", line: "549B56" },
  // blue complexity box, strokes x87..868 / y228..425
  { x: 87.75, y: 228.5, w: 781, h: 197, fill: "F8F8FF", line: "B9B6D8" },
  // yellow solution box, strokes x87..874 / y435..529
  { x: 87.5, y: 435.5, w: 787.25, h: 94.5, fill: "FAFDE2", line: "6B562E" },
];

// equation composite (600dpi PNG, PAD 8px = 0.96 frame px)
const EQ = {
  path: path.resolve(__dirname, "assets/eq_023_main.png"),
  wIn: 4.52, hIn: 0.55667,
  x: 103.04, y: 149.04, // image origin so the ink starts at frame (104,150)
};

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, gray panel, red L/R/Bottom strokes (NO top), badge "23"
drawHouseChrome(pptx, slide, { numeral: 23 });

// ---- the three coloured content boxes -----------------------------------------------
for (const b of BOXES) {
  slide.addShape(pptx.ShapeType.rect, {
    x: b.x * PX, y: b.y * PX, w: b.w * PX, h: b.h * PX,
    fill: { color: b.fill },
    line: { color: b.line, width: 1 }, // measured 2px strokes @150dpi ~= 0.96pt
  });
}

// ---- text helper ---------------------------------------------------------------------
// One text box per line at its measured baseline (LO box-top -> baseline distance
// calibrated at 1.0 em in the closed-loop selfcheck; per-line boxes have no line
// pitch to diverge on).
const BASE_OFF = 1.0;
function textBox(x, base, w, runs, size, extra) {
  slide.addText(runs, Object.assign({
    x: x * PX, y: (base - size * BASE_OFF) * PX, w: w * PX, h: 30 * PX,
    valign: "top", align: "left", margin: 0, fontFace: FONT, fontSize: size,
  }, extra || {}));
}
const r = (text, opts) => ({ text: text, options: opts || {} });
const center = (cx, w) => cx - w / 2;

// ---- title (red bold 27.5pt, ink x219..654) ------------------------------------------
textBox(219, 98, 460,
  [r("Inverse of High Dimension Matrix", { bold: true })], 27.5, { color: RED, bold: true });

// ---- "Recall" (black ITALIC 28pt, underlined, ink x103..177) --------------------------
// PIL-ADJUDICATED DEVIATION FROM THE ANALYSIS SPEC (2026-10-21): the analysis's
// `labels` list renders this as "Recall:" WITH a trailing colon, but the ORIGINAL FRAME
// HAS NO COLON. Measured on unique_slides/slide_023.jpg: the label's glyph groups are
// exactly 5 (R x103..120, e x122..133, c+a x135..160, l x164..169, l x172..177) and a
// permissive scan (lum<225) of x176..216 y118..144 finds only the 'l' tail, the underline
// bar at y141..142 and isolated JPEG noise - a 28pt colon would be ~20-30 dark pixels and
// there are none. The colon is a script-12/13 transcription artefact.
// Verbatim law hierarchy (build header): judge_protocol_03.md OVERRIDES the analysis spec,
// and its Template B demands glyph-level exactness ("any wrong/missing/garbled characters
// ... is a MAJOR-to-BLOCKER defect"), so the frame wins. Removing the colon also drops
// this label's advance deviation from +13px to +3px.
// Italic verified three ways: the 'R' stem leans (top x107 vs bottom x103 = ~16 deg over
// the 21px cap), the column-profile cos is 0.889 (Italic) vs 0.798 (Regular), and the
// analysis typography_notes say "'Recall:' is italic and underlined". Arial Italic's
// advance is then 77 vs the original's 74 (+3px) - inside tolerance.
// LEFT-EDGE SHIFT + SIZE FIT (2026-10-21, measured on render_2/render_3): with the box at
// x106 the italic ink landed at x107.2..184.0 while the frame's label is x103..177, and
// the underline bar at x106.2..183.5 vs the frame's x103..178. Both were 3.2px right of
// the mark, so the box is pulled to x102.0: that puts the ink at x103.5..178.9 (+0.5/+1.9)
// and the underline at x102.1..179.3 (-1.9/+1.3), and it aligns the label with the green
// box's CONTENT margin - dim part1 starts at x104 and the equation image ink at x104, so
// every green-box element begins at x~104.
// SIZE 27.5pt (not 28pt): at 28pt the Arial-Italic advance is 76.8 against the frame's
// 74 (+4.1 right edge, the largest single advance deviation on the slide). Dropping half
// a point brings the advance to 75.4 while costing only 0.4px of cap height (20.1 ->
// 19.7 vs the frame's 21), so the worst-case metric falls from 4.1 to 1.9 px (2.6% of the
// label's 74px width). Font forensics: at cap 21 Arial Italic advance/cap = 3.71 vs the
// frame's 3.52; Arial Regular 3.75 (+6.6% wide), NimbusNarrow-Oblique 3.44 (-10% narrow).
// Arial Italic stays the closest single choice - switching to a narrow face would buy 5%
// of width but make this one label a different family from every other run on the slide.
// Note the UNDERLINE's y already matches the frame's y141..142 exactly (0.0px), even
// though the line-box offset for the label is +0.4px: the label has no descenders, so its
// ink bottom IS the baseline and LO's underline hangs at the same offset as the original's.
textBox(102.0, 138, 95,
  [r("Recall", { underline: true, italic: true })], 27.5,
  { color: BLACK, italic: true });

// ---- equation ink x104..429 y150..186 -------------------------------------------------
slide.addImage({
  path: EQ.path,
  x: EQ.x * PX, y: EQ.y * PX, w: EQ.wIn, h: EQ.hIn,
});

// ---- dim note (baseline 211): part 1 + the green-box implication arrow + part 2 -------
textBox(103, 211, 320,
  [r("if Feature vectors are of dimension "), r("d", { color: RED })], 19, { color: BLACK });

// green-box implication arrow: RED ink x437..455 y200..209 in the gap between part 1
// (ends x409) and part 2 (starts x505). The R-G map shows TWO horizontal bars
// (y202-203, y206-207, x439..453) plus a solid right head (x448..455, y200..209) =
// the double-shaft U+21D2 "⇒". DejaVu Sans U+21D2 @25pt reproduces that ink EXACTLY
// (19w x 10h with the same two-bar + head structure); Arial (the deck font) has no
// U+21D2 at all, so the fontFace is explicit (otherwise LO silently substitutes).
// Arrow core RGB ~(145,10,25) = the deck red C00000 under JPEG.
// LO line-box offset measured on render_2: ink top = box_top + 11.8 (DejaVu's line
// height is 1.43em, not the PIL ascent), so base 213 puts the ink at y200..209.
// (base 224 landed it 11px low at y211..220.)
textBox(436, 213, 40, [r("⇒", { color: RED })], 25,
  { color: RED, fontFace: "DejaVu Sans" });

textBox(505, 211, 170, [r("(X^T X) is of size ")], 20, { color: BLACK });
textBox(662, 211, 42, [r("d+1")], 20, { color: RED });
textBox(695.4, 211, 20, [r(" x ")], 20, { color: BLACK });
textBox(714, 211, 42, [r("d+1")], 20, { color: RED });

// ---- blue box: 3 navy lines (baselines 260/294/327) ----------------------------------
// L1's verbatim text ends "O(n^3)," WITH the comma (analysis/slide_023_final.json
// bullets[0]) and the frame has it: a RED comma at x831..835 y257..264 hanging 4px
// below the baseline 260, directly after the ')' (x826..830). L2 starts "which means"
// with no leading comma. The comma therefore belongs to the RED run, not the navy one.
textBox(96, 260, 760, [
  r("The standard matrix inversion algorithm has a time complexity of "),
  r("O(n^3),", { color: RED }),
], 23.5, { color: NAVY });

textBox(96, 294, 760, [
  r("which means that the computation time increases rapidly with the size of"),
], 23.5, { color: NAVY });

textBox(96, 327, 690, [
  r("the matrix (increasing cubically with the number of components)."),
], 23.5, { color: NAVY });

// ---- blue box: the two example lines (black + red numbers) ---------------------------
textBox(96, 382, 770, [
  r("For Example: if Features vector is of size "),
  r("1000", { color: RED }),
  r(" then Inverse calculation is"),
], 23.5, { color: BLACK });

textBox(96, 416, 460, [
  r("or order "),
  r("1,000,000,000", { color: RED }),
  r(" which is impractical"),
], 23.5, { color: BLACK });

// ---- yellow box: "Solution:" (navy bold 21pt) + two centred lines --------------------
textBox(96, 464, 100,
  [r("Solution:", { bold: true })], 21, { color: NAVY, bold: true });

// PIL-verdict (2026-10-24): the frame's solution lines set in an oblique/italic
// face. Verified on unique_slides/slide_023.jpg by stem-slant and glyph-form
// forensics (SOL1 12 stems -0.129 px/row = -7.3 deg vs the render's 0.0; the
// 'e' counter at y512 x493..495 spans 3 columns where roman 'e' spans 5, and the
// SOL2 'G' top terminal leans left-of-centre) - oblique terminals, not serifs.
// The same family is already used for the "Recall" label and the blue/EX body
// lines, so italics + `r(..., {italic:true})` is the deck-consistent choice.
textBox(center(477.5, 480), 492, 480, [
  r("Instead of using Least Squares with Matrix inversion,", { italic: true }),
], 20, { color: NAVY, align: "center", italic: true });

textBox(center(480.5, 360), 519, 360, [
  r("use Gradient Descent iterative solution", { italic: true }),
], 20, { color: NAVY, align: "center", italic: true });

pptx.writeFile({ fileName: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_023_recreated.pptx" })
  .then(() => console.log("wrote slide_023_recreated.pptx"));
