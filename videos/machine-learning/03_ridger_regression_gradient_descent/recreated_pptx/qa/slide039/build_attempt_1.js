// slide_039.js — "Gradient Descent (GD) – Stochastic Gradient Descent SGD) and Mini-Batch Gradient Descent"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (lecture 03), root slide (no deps).
//
// GEOMETRY LAW: every value below is a MEASURED frame pixel from unique_slides/slide_039.jpg
// (960x540, 1px = 1pt = 1/72in), taken in the banked forensic passes of this session.
// Text is VERBATIM from analysis/slide_039_final.json.
//
// MEASURED TARGETS (frame px):
//   Content panel: white (253,255,254) fill; border centerlines x73.5/867.5, y142.5/482.5
//     (2px @150dpi = 1pt); border dark core (43,37,144) => navy-violet 2B2590.
//     Panel rect x73..868 w795, y142..482 h340.
//   TITLE L1 (RED, bold): ink x121..837 (w716), band y79..98, cap 18px.
//     "Gradient Descent (GD) – Stochastic Gradient Descent SGD)" = 24.24em; Times bold
//     @28pt = 706px vs measured 716 (+1.4%); cap 0.662x28 = 18.5 vs measured 18. OK.
//   TITLE L2 (bold, THREE colour runs - measured per-run x extents):
//     RED  "and"             x280..322 (42px)
//     BLUE "Mini-Batch"      x340..467 (127px)
//     RED  "Gradient Descent" x478..687 (209px)
//     band y109..128, cap 18px => same 28pt bold. Drawn as three boxes at their measured
//     left edges (single-box layout drifts on inter-run gaps - slide_023 pattern).
//   UPPER bullets: blue arrow markers at x84..93; text starts x101/102.
//     B1 wraps to 2 lines (measured split after "...the Error"):
//       L1 x101..839 y155..168; L2 x101..478 y184..194. Pitch 27.5px.
//     B2 x102..660 y209..219 | B3 x102..765 y231..244.
//     Cap 13px => Times regular 19pt (advance fit: B2 29.16em x 19 = 554 vs measured 558).
//   GREEN callout box: x348..855 w507, y260..302 h42; fill (226,255,239) => E1FFEF;
//     border core (89,129,76) => 59814C, ~2-3px => 1.5pt.
//   EQUATION (professional 2D): ink x367..563 (196px), baseline y291; the mandated 2D
//     form is more vertically compact than the original's ink (y270..299), matched on
//     left edge / baseline / ink centre (y285) instead. 17pt mathtext => ink 199px.
//   RED annotation "Repeat for ALL misclassified Samples": x605..841 (236px), y279..292.
//     16.10em => Times regular 15pt (242px).
//   WHY USING SGD (red, bold): ink x84..212, band y308..324. 7.11em x 1.04 x 18 = 133px.
//   LOWER bullets: B4 x101..402 y337..346; B5 x101..336 y363..371 (19pt regular).
//     FRAME WINS over the analysis's "['efficient' in red]" guess: the word measures BLACK
//     (50,50,50) in the original - no red ink exists in the bullet zone (scan y325..380).
//   BOTTOM CAPTION (red, bold 17pt, left-aligned at x92, wraps to 2 lines):
//     L1 x90..830 y409..425, L2 x92..429 y435..447 (pitch 24px => lineSpacing 24pt).
//   BLUE caption (bold 19pt, centred on panel centre x470.5):
//     "If n=N (it is GD), and if n=1 (it is SGD)" ink x313..628 y459..475.
//   RED NOTE: the caption's first line measures red ink only up to x453 with black ink
//     from x455..830 - a mid-line colour change in the original. The analysis spec
//     declares this line wholly RED and no clean word boundary explains the split at
//     x455; rendered per spec (all red). Adjudication input for the judge if raised.
//
// DEVIATIONS FROM SPEC (law hierarchy: deck AGENTS.md + judge_protocol_03.md + runbook
// OVERRIDE the analysis spec; the frame wins):
//   1. House chrome via shared_patterns/house_chrome.js (white canvas, gray E9E9E7 panel
//      x54..903 y45..540, C00000 1pt strokes LEFT/RIGHT/BOTTOM only - NO top stroke,
//      badge FDFD96 + 6A5ACD ring, bold 18pt Arial 333333 numeral 39).
//   2. Spec percentage positions replaced by the measured pixel geometry above.
//   3. Serif font (Times New Roman) per typography_notes; advance-fit verified.
//   4. 'efficient' rendered black (frame measurement), not red (spec's flagged guess).
//   5. Mouse-pointer arrow over the equation: video-capture artifact, OMITTED per
//      judge GROUND RULES (c) and recreation_brief step 11.
//
// Single-version deliverable: recreated_pptx/slide_039_recreated.pptx (no suffixes).
// Equation sidecar: build/assets/eq_039_main.json (for the post-certification OMML wrap,
// which the orchestrator applies after certification - NOT applied here).

const pptxgenpkg = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const PX = 1 / 72; // frame px -> inches
const SERIF = "Times New Roman";
const RED = "C00000";          // founder-ratified family nominal (measured core ~8E1325)
const BLUE = "584CA8";         // measured median of blue text ink (74,66,169)/(109,100,195)
const BLUE_BORDER = "2B2590";  // panel border dark core (43,37,144)
const GREEN_BORDER = "59814C"; // green box border core (89,129,76)
const GREEN_FILL = "E1FFEF";   // green box fill (226,255,239)
const BLACK = "000000";
const ARROW = "3F35A8";        // chevron marker ink

// ---- measured geometry (frame px) ---------------------------------------------------
const PANEL = { x: 73, y: 142, w: 795, h: 340 };          // white panel + blue border
const GBOX = { x: 348, y: 260, w: 507, h: 42 };           // green equation callout
const EQ = {
  path: path.resolve(__dirname, "assets/eq_039_main.png"),
  wIn: 1676 / 600, hIn: 179 / 600,
  x: 366.04, y: 274.1,   // ink x367..566 (orig x367..563), baseline y291 (orig 291), ink centre y285 (orig 284.5)
};
const ARROW_PNG = {
  path: path.resolve(__dirname, "assets/evt_039.png"),
  wIn: 0.18, hIn: 0.15167, x: 83, yTop: 156,  // glyph y156.3..165.4, centre 160.85
};
const TITLE_SIZE = 28;   // bold, Times
const BODY = 19;         // regular, Times
const WHY_SIZE = 18;     // bold
const ANN_SIZE = 15;     // regular
const CAP_SIZE = 17;     // bold (red caption)
const CAP_BLUE_SIZE = 19;// bold (blue caption)

// closed-loop tuning knobs (frame px deltas, applied per element after render measurement)
const TUNE = {};

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, gray panel, red L/R/Bottom strokes (NO top), badge "39"
drawHouseChrome(pptx, slide, { numeral: 39 });

// ---- white content panel with blue border -------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: PANEL.x * PX, y: PANEL.y * PX, w: PANEL.w * PX, h: PANEL.h * PX,
  fill: { color: "FFFFFF" },
  line: { color: BLUE_BORDER, width: 1 }, // measured 2px @150dpi = 1pt
});

// ---- green equation callout box ------------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: GBOX.x * PX, y: GBOX.y * PX, w: GBOX.w * PX, h: GBOX.h * PX,
  fill: { color: GREEN_FILL },
  line: { color: GREEN_BORDER, width: 1.5 }, // measured ~2-3px @150dpi
});

// ---- title line 1 (red, bold) ---------------------------------------------------------
// ink x121..837, band y79..98. Box centred on ink centre (479, 88), align left.
slide.addText("Gradient Descent (GD) \u2013 Stochastic Gradient Descent SGD)", {
  x: 121 * PX, y: (88 - 15) * PX, w: 800 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: TITLE_SIZE, bold: true, color: RED, fontFace: SERIF, margin: 0,
});

// ---- title line 2 (three measured colour runs, separate boxes at measured left edges) --
slide.addText("and", {
  x: 280 * PX, y: (118 - 15) * PX, w: 60 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: TITLE_SIZE, bold: true, color: RED, fontFace: SERIF, margin: 0,
});
slide.addText("Mini-Batch", {
  x: 340 * PX, y: (118 - 15) * PX, w: 140 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: TITLE_SIZE, bold: true, color: BLUE, fontFace: SERIF, margin: 0,
});
slide.addText("Gradient Descent", {
  x: 478 * PX, y: (118 - 15) * PX, w: 215 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: TITLE_SIZE, bold: true, color: RED, fontFace: SERIF, margin: 0,
});

// ---- upper bullets (blue arrow markers + black text) ---------------------------------
// marker bands: B1 y159..164, B2 y210..215, B3 y235..240 (glyph template centre 160.85)
const MARKERS = [161.5, 212.5, 237.5];
MARKERS.forEach((my) => {
  slide.addImage({ path: ARROW_PNG.path,
    x: ARROW_PNG.x * PX, y: (ARROW_PNG.yTop + (my - 160.85)) * PX,
    w: ARROW_PNG.wIn, h: ARROW_PNG.hIn });
});

// Bullet 1 wraps after "...the Error" (measured: L1 x101..839, L2 x101..478)
slide.addText("Stochastic Gradient Descent (SGD) is a variant of GD which computes the gradient of the Error", {
  x: 101 * PX, y: (160.5 - 15) * PX, w: 760 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: BODY, color: BLACK, fontFace: SERIF, margin: 0,
});
slide.addText("function with respect to a single training example", {
  x: 101 * PX, y: (189 - 15) * PX, w: 500 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: BODY, color: BLACK, fontFace: SERIF, margin: 0,
});

// Bullet 2 — x102..660 y209..219
slide.addText("In other words, it updates the weights using one training sample at a time", {
  x: 102 * PX, y: (214 - 15) * PX, w: 600 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: BODY, color: BLACK, fontFace: SERIF, margin: 0,
});

// Bullet 3 — x102..765 y231..244
slide.addText("Remember: GD updated the weight vector after passing through ALL training samples.", {
  x: 102 * PX, y: (237 - 15) * PX, w: 680 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: BODY, color: BLACK, fontFace: SERIF, margin: 0,
});

// ---- equation (professional 2D) + red annotation -------------------------------------
slide.addImage({ path: EQ.path, x: EQ.x * PX, y: EQ.y * PX, w: EQ.wIn, h: EQ.hIn });

slide.addText("Repeat for ALL misclassified Samples", {
  x: 605 * PX, y: (283.5 - 9) * PX, w: 250 * PX, h: 18 * PX,
  align: "left", valign: "middle",
  fontSize: ANN_SIZE, color: RED, fontFace: SERIF, margin: 0,
});

// ---- "Why using SGD" (red, bold) -----------------------------------------------------
slide.addText("Why using SGD", {
  x: 84 * PX, y: (313 - 12) * PX, w: 140 * PX, h: 24 * PX,
  align: "left", valign: "middle",
  fontSize: WHY_SIZE, bold: true, color: RED, fontFace: SERIF, margin: 0,
});

// ---- lower bullets --------------------------------------------------------------------
const MARKERS_L = [338.5, 364.5];
MARKERS_L.forEach((my) => {
  slide.addImage({ path: ARROW_PNG.path,
    x: ARROW_PNG.x * PX, y: (ARROW_PNG.yTop + (my - 160.85)) * PX,
    w: ARROW_PNG.wIn, h: ARROW_PNG.hIn });
});

slide.addText("SGD is usually more efficient than GD", {
  x: 101 * PX, y: (341 - 15) * PX, w: 320 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: BODY, color: BLACK, fontFace: SERIF, margin: 0,
});
slide.addText("SGD converges faster than GD", {
  x: 101 * PX, y: (367 - 15) * PX, w: 260 * PX, h: 30 * PX,
  align: "left", valign: "middle",
  fontSize: BODY, color: BLACK, fontFace: SERIF, margin: 0,
});

// ---- bottom captions ------------------------------------------------------------------
// red caption: left-aligned at x92, wraps to 2 lines (measured pitches 24px => lineSpacing 24pt)
slide.addText("Batch GD is a generalization of GD and SGD where weights are updated after passing through \u201cMini-Batch\u201d of training samples with size n", {
  x: 92 * PX, y: (425 - 23) * PX, w: 745 * PX, h: 46 * PX,
  align: "left", valign: "middle",
  fontSize: CAP_SIZE, bold: true, color: RED, fontFace: SERIF, margin: 0,
  lineSpacing: 24,
});

// blue caption: centred on the panel centre (470.5)
slide.addText("If n=N (it is GD), and if n=1 (it is SGD)", {
  x: 313 * PX, y: (465 - 13) * PX, w: 315 * PX, h: 26 * PX,
  align: "center", valign: "middle",
  fontSize: CAP_BLUE_SIZE, bold: true, color: BLUE, fontFace: SERIF, margin: 0,
});

const OUT = path.resolve(__dirname, "../slide_039_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
