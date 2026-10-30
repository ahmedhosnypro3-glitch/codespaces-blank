// Build slide 009 — "Overfit vs. Generalized" (metadata-only title; NO title ink on the frame)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Attempt 1 — fresh build from WIP measurements (qa/slide009/measurements_summary.txt)
//
// ═══════════════════════════════════════════════════════════════════════════════
// GROUND TRUTH: unique_slides/slide_009.jpg — 960x540, exactly 72 px/in
//                (verified: 960/13.3333 = 72.0001) => 1 frame px == 1 pt == 1/72 in.
// All geometry below is in FRAME PX == POINTS. Converted to inches by px().
// Measurement bank: recreated_pptx/qa/slide009/ (probe1..probe59 + measurements_summary.txt)
// ═══════════════════════════════════════════════════════════════════════════════
//
// CONTENT (all PIL-verified, see qa/slide009/measurements_summary.txt):
//   * NO title/subtitle text anywhere on the frame (validation.uncertain_items[0]
//     confirms slide_title 'Overfit vs. Generalized' is metadata-only) -> nothing drawn.
//   * Two side-by-side scatter charts, each: white interior inside a 1pt NAVY border,
//     16x16 light-gray grid, RED x/y axes with triangular arrowheads, a BLUE fitted
//     line, 12 ORANGE data points, one pale-red diagonal annotation stroke, and small
//     solid red discs. The LEFT chart additionally carries a large solid red disc.
//   * A pale-cyan annotation box inside each chart holding one black equation.
//   * Four caption lines BELOW the charts (2 per chart), Times-like serif, 17pt:
//     a RED bold keyword + a near-black regular remainder on line 1, all near-black
//     on line 2, each caption centred on its chart (centres 264 / 671 frame px).
//
// ── SPEC-vs-FRAME DEVIATIONS (frame wins per the judge GROUND RULES) ───────────
//  1. typography_notes claims the captions are "bold red" THROUGHOUT. Measurement
//     (probe44 per-row runs, probe45 font fits) shows ONLY the leading keyword is red;
//     the remainder of line 1 and all of line 2 are near-black #333333.
//  2. brief/dispatch ask for vertical '50.85 mm' / '63.64 mm' arrows and labels.
//     NO 'mm' text and NO vertical double-arrow exist on the frame (probe28/29/30/44:
//     zero dark components in that region). NOT drawn.
//  3. Spec colours #F5F5F5 chart interior / #CCCCCC grid / #0000FF line / #FFA500
//     points / #E0F0FF box: measurement confirms the family; the grid renders
//     slightly lighter than #CCCCCC (cores 207..238 over a 250 interior) so D8D8D6
//     is used, and the annotation box fill measures pale CYAN (interior median
//     237,251,250 — b>g>r) not pale blue, so E0F0FF is used (frame's JPEG tolerance).
//  4. The RIGHT chart's navy border is genuinely ~12pt wider than the LEFT's
//     (independent cuts at y=300: LEFT x95..465, RIGHT x486.5..869.5) — reproduced
//     as measured rather than symmetrised.
//
// ── EQUATIONS (deck math law: professional 2D format) ─────────────────────────
//   Both are single-line with a raised superscript -> mathtext PNGs rendered by the
//   CERTIFIED scripts/render_eq.py loaded with matplotlib's default fontset
//   (the slide's typeface is serif/Times-like; DejaVu Sans matches measured ink
//   proportions — see probe56_eqstix.py rejection of STIX).
//   Size calibration (DejaVu Sans, fs=14.5) against the frame's measured ink:
//     ink box    render 856x131px / 860x131px   frame 82x13 / 81x13
//     digit hgt  render ~10pt                    frame 10pt (y155..166)
//     superscript render ~7pt                     frame 6pt  (y154..161)
//   Placement: w=w_in, h=h_in at exact px/600 size (never rescaled) + eq_*.json
//   sidecars for the orchestrator's OMML dual-representation wrap pass.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_009_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette ──────────────────────────────────────────────────────────
const NAVY      = "000080";   // chart-panel border  (frame core 0,0,108)
const INTERIOR  = "F5F5F5";   // chart interior      (frame ~248,248,248)
const GRID      = "D8D8D6";   // grid lines          (frame cores 207..238 over 250)
const RED       = "C00000";   // axes / red marks / caption keyword (house family)
const BLUE      = "0000FF";   // fitted lines        (frame core 0,0,132)
const ORANGE    = "FFA500";   // data points         (frame core 255,120,0)
const BIGRED    = "EE3145";   // the LEFT chart's large solid disc (frame core 238,49,69)
const BOXFILL   = "ECFDF9";   // annotation box fill (frame median 236,253,249 = pale cyan)
const BOXLINE   = "000080";   // annotation box border = navy (same as panel border)
const INK       = "333333";   // caption remainder ink (frame core 49,51,37)
const FONT      = "Times New Roman"; // serif, matches the frame (Liberation Serif metrics)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top
// stroke on this deck), badge with numeral 9. Drawn ONCE, first (under content).
drawHouseChrome(pptx, slide, { numeral: 9 });

// Helpers
const rect = (x, y, w, h, fill) =>
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill },
  });
const stroked = (x, y, w, h, color, width) =>
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    line: { color: color, width: width },
  });
const ellipse = (cx, cy, d, fill) =>
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill },
  });

// ═══════════════════════════════════════════════════════════════════════════════
// CHART PANELS
// ═══════════════════════════════════════════════════════════════════════════════
// border lines are centred on the rect edge (1pt == 1 frame px)
// Panel measurements from probe40/probe41:
const PANELS = [
  {
    name: "LEFT",
    // Navy border rect (outer)
    bx: 95,   by: 107, bw: 371, bh: 367,
    // White interior
    fx: 98,   fy: 111, fw: 365, fh: 359,
    // Grid box
    col0: 103.5, colPitch: 23, nCol: 16,
    row0: 120.5, rowPitch: 22.4, nRow: 16,
    // Axes (red)
    axisX: 126.5, axisX0: 152, axisX1: 437,
    axisY: 434,   axisY0: 124, axisY1: 428,
    // Arrowheads
    headUp:   { cx: 126.5, tipY: 143, baseY: 151, halfW: 4.0 },
    headRight:{ cy: 434,   tipX: 435, baseX: 428, halfH: 3.5 },
    // Blue fitted line (measured from probe41)
    line: { x0: 141, y0: 351, x1: 433, y1: 201 },
    // Pale-red diagonal annotation stroke
    diag: { x0: 199, y0: 198, x1: 232, y1: 241 },
    // Large red disc (left chart only)
    bigDisc: { cx: 232.5, cy: 241, d: 24.5 },
    // Genuine red residual marks (diamond + diagonal arrow)
    redMarks: [
      { type: "diamond", cx: 187,   cy: 155,   d: 9 },
      { type: "arrow",   x0: 204, y0: 199, x1: 218, y1: 233, headW: 34 },
    ],
    // Data points (12 orange, measured from probe41)
    points: [
      [197.5, 145.0], [188.5, 355.5], [176.5, 380.5], [242.5, 327.5], [260.5, 333.5],
      [294.0, 333.5], [324.0, 290.0], [328.5, 332.0], [381.5, 301.5], [397.5, 249.0],
      [421.5, 255.0], [233.5, 362.0],
    ],
    gOff: 0,
  },
  {
    name: "RIGHT",
    bx: 486.5, by: 107, bw: 385, bh: 367,
    fx: 489.5, fy: 111, fw: 378, fh: 359,
    col0: 517.5, colPitch: 23, nCol: 16,
    row0: 120.5, rowPitch: 22.4, nRow: 16,
    axisX: 540,   axisX0: 152, axisX1: 437,
    axisY: 434,   axisY0: 538, axisY1: 841,
    headUp:   { cx: 540,   tipY: 143, baseY: 151, halfW: 3.5 },
    headRight:{ cy: 434,   tipX: 848, baseX: 841, halfH: 3.5 },
    line: { x0: 555, y0: 387, x1: 849, y1: 247 },
    diag: { x0: 626, y0: 208, x1: 646, y1: 264 },
    bigDisc: null,
    redMarks: [
      { type: "diamond", cx: 602.5, cy: 149.5, d: 8 },
      { type: "arrow",   x0: 627, y0: 212, x1: 636, y1: 232, headW: 19 },
    ],
    points: [
      [611.0, 145.0], [601.5, 355.5], [589.5, 380.5], [656.0, 327.0], [674.0, 333.5],
      [707.5, 333.5], [737.5, 290.0], [741.5, 332.0], [794.0, 302.0], [810.0, 249.0],
      [834.5, 255.0], [647.0, 362.0],
    ],
    gOff: 413.5,
  },
];

for (const p of PANELS) {
  // 1. white interior (drawn first so the grid/axes sit on it)
  rect(p.fx, p.fy, p.fw, p.fh, INTERIOR);

  // 2. grid — 16 vertical + 16 horizontal 1pt lines inside the measured grid box.
  //    Grid box: x col0 .. col0+colPitch*(nCol-1); y row0 .. row0+rowPitch*(nRow-1)
  const gx0 = p.col0, gx1 = p.col0 + p.colPitch * (p.nCol - 1);
  const gy0 = p.row0, gy1 = p.row0 + p.rowPitch * (p.nRow - 1);
  for (let k = 0; k < p.nCol; k++) {
    const cx = p.col0 + p.colPitch * k;
    rect(cx - 0.5, gy0, 1, gy1 - gy0, GRID);
  }
  for (let k = 0; k < p.nRow; k++) {
    const cy = p.row0 + p.rowPitch * k;
    rect(gx0, cy - 0.5, gx1 - gx0, 1, GRID);
  }

  // 3. blue fitted line (2pt; frame per-column core span 2-3px)
  //    pptxgenjs line: x/y is top-left of bbox; w/h is bbox; use flipV for upward lines
  slide.addShape(pptx.ShapeType.line, {
    x: px(p.line.x0), y: px(p.line.y1), w: px(p.line.x1 - p.line.x0),
    h: px(p.line.y0 - p.line.y1), flipV: true,
    line: { color: BLUE, width: 2 },
  });

  // 4. 12 orange data points, d=7.5 (measured blob widths 6..8)
  for (const [cx, cy] of p.points) ellipse(cx, cy, 7.5, ORANGE);

  // 5. pale-red diagonal annotation stroke (2pt; measured core 2-3px, pale halo)
  slide.addShape(pptx.ShapeType.line, {
    x: px(p.diag.x0), y: px(p.diag.y0), w: px(p.diag.x1 - p.diag.x0),
    h: px(p.diag.y1 - p.diag.y0), line: { color: RED, width: 2 },
  });

  // 6. red axes (1pt shafts, centred on the measured axis)
  rect(p.axisX - 0.5, p.axisX0, 1, p.axisX1 - p.axisX0, RED); // vertical
  rect(p.axisY0, p.axisY - 0.5, p.axisY1 - p.axisY0, 1, RED); // horizontal

  // 7. triangular arrowheads (measured ~8x8 for the up-head, ~6x7 for the right-head)
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(p.headUp.cx - p.headUp.halfW), y: px(p.headUp.tipY),
    w: px(p.headUp.halfW * 2), h: px(p.headUp.baseY - p.headUp.tipY),
    fill: { color: RED },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(p.headRight.baseX), y: px(p.headRight.cy - p.headRight.halfH),
    w: px(p.headRight.halfH * 2), h: px(p.headRight.tipX - p.headRight.baseX),
    rotate: 90, fill: { color: RED },
  });

  // 8. red marks: small solid discs (+ the LEFT chart's large solid disc)
  //    Also draw the genuine red residual marks (diamond + arrow)
  for (const m of p.redMarks) {
    if (m.type === "diamond") {
      // Diamond = rotated square
      slide.addShape(pptx.ShapeType.rect, {
        x: px(m.cx - m.d / 2), y: px(m.cy - m.d / 2),
        w: px(m.d), h: px(m.d), rotate: 45, fill: { color: RED },
      });
    } else if (m.type === "arrow") {
      // Arrow shaft
      slide.addShape(pptx.ShapeType.line, {
        x: px(m.x0), y: px(m.y0), w: px(m.x1 - m.x0), h: px(m.y1 - m.y0),
        line: { color: RED, width: 3 },
      });
      // Arrowhead — triangle at the tip (pointing towards the data point)
      const dx = m.x1 - m.x0, dy = m.y1 - m.y0;
      const len = Math.hypot(dx, dy);
      const ux = dx / len, uy = dy / len;
      const hx = m.x1 - ux * 8, hy = m.y1 - uy * 8; // 8pt back from tip
      const perpX = -uy, perpY = ux;
      const hw = m.headW / 2;
      slide.addShape(pptx.ShapeType.triangle, {
        x: px(hx + perpX * hw), y: px(hy + perpY * hw),
        w: px(hw * 2), h: px(8), // approximate
        rotate: Math.atan2(dy, dx) * 180 / Math.PI - 90,
        fill: { color: RED },
      });
    }
  }
  if (p.bigDisc) ellipse(p.bigDisc.cx, p.bigDisc.cy, p.bigDisc.d, BIGRED);

  // 9. navy border on top
  stroked(p.bx, p.by, p.bw, p.bh, NAVY, 1);
}

// ═══════════════════════════════════════════════════════════════════════════════
// ANNOTATION BOXES + EQUATION IMAGES
// ═══════════════════════════════════════════════════════════════════════════════
// Box: navy 1pt border centred on the rect edge, pale-cyan fill.
// LEFT  box x216..317 y147..175 (w102 h29);  top y148 (probe26/27)
// RIGHT box x631..734 y147..175 (w104 h29);  top y148
// Equation PNG ink starts ~8px (0.96pt) inside the image box; placed so the ink's
// left edge lands on the measured ink x and its top on y155.
const ASSETS = path.resolve(__dirname, "assets");
const BOXES = [
  // LEFT: x216..317 (w102), y148..175 (h27)
  { x: 216, y: 148, w: 102, h: 27,
    img: path.join(ASSETS, "eq_009_left.png"),
    // PNG ink box: w_px=856, h_px=131, baseline=121 from top
    // Ink starts ~8px from image left/top. We want ink left at x226, top at y155.
    // Image left = 216 + 8 = 224 (frame px) -> 224/72 = 3.111in
    // Image top  = 148 + 8 = 156 -> 156/72 = 2.167in
    // But the PNG is 856px wide = 1.42667in. Ink box inside is 856-16 = 840px = 1.4in.
    // Measured ink width on frame: 82px = 1.139in. So scale factor = 1.139/1.4 = 0.814.
    // Better: place the PNG so its ink box lands on the frame's ink box.
    // PNG ink left = 8px, ink right = 856-8 = 848px. Frame ink left = 226, right = 307.
    // So PNG x = (226 - 8) / 72 = 218/72 = 3.0278in
    // PNG y = (155 - 8) / 72 = 147/72 = 2.0417in
    // PNG w = 856/600 = 1.42667in, h = 131/600 = 0.21833in
    ix: 3.0278, iy: 2.0417, iw: 1.42667, ih: 0.21833,
  },
  // RIGHT: x631..734 (w104), y148..175 (h27)
  // Frame ink left = 643, right = 723
  // PNG ink left = 8px -> PNG x = (643 - 8) / 72 = 635/72 = 8.8194in
  // PNG y = (155 - 8) / 72 = 147/72 = 2.0417in
  { x: 631, y: 148, w: 104, h: 27,
    img: path.join(ASSETS, "eq_009_right.png"),
    ix: 8.8194, iy: 2.0417, iw: 1.43333, ih: 0.21833,
  },
];

for (const b of BOXES) {
  // Box background + border
  slide.addShape(pptx.ShapeType.rect, {
    x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
    fill: { color: BOXFILL }, line: { color: BOXLINE, width: 1 },
  });
  // Equation image at exact px/600 size
  slide.addImage({ path: b.img, x: b.ix, y: b.iy, w: b.iw, h: b.ih });
}

// ═══════════════════════════════════════════════════════════════════════════════
// CAPTION-BAND ROSE ANNOTATION BOXES — PIL-measured on the frame 2026-10-24.
// Each caption sits inside a CREAM-FILLED, rose-outlined box that is open at the
// top: left + right verticals plus a bottom rule, no top stroke. Drawn BEFORE
// the captions so the ink sits on the fill, exactly as the hand annotation does.
//   LEFT  box x95..434 y479..529 ; RIGHT box x501..842 y479..529 (frame px)
// Fill medians 251,252,236 (cream) on both sides; stroke cores measured per side
// (the frame's JPEG halos widen each stroke ~1-2px around the cores below).
// ═══════════════════════════════════════════════════════════════════════════════
const CAPFILL = "FBFCEC"; // caption-box fill (frame median 251,252,236)
const BANDS = [
  { fill: { x: 97,    y: 480,  w: 335, h: 47, c: CAPFILL },
    strokes: [
      { x: 95.5,  y: 479,   w: 2, h: 49, c: "E2C6C3" }, // left vertical  (226,198,195)
      { x: 432.5, y: 479,   w: 2, h: 49, c: "F0E6E7" }, // right vertical (240,230,231)
      { x: 96,    y: 527.5, w: 337, h: 2, c: "DCBBBB" }, // bottom rule   (220,187,187)
    ] },
  { fill: { x: 504,   y: 480,  w: 335, h: 47, c: CAPFILL },
    strokes: [
      { x: 502,   y: 479,   w: 2, h: 49, c: "D3BCB9" }, // left vertical  (211,188,185)
      { x: 839.5, y: 479,   w: 2, h: 49, c: "CAA5A6" }, // right vertical (202,165,166)
      { x: 503,   y: 527.5, w: 337, h: 2, c: "D9BBBA" }, // bottom rule   (217,187,186)
    ] },
];
for (const band of BANDS) {
  rect(band.fill.x, band.fill.y, band.fill.w, band.fill.h, band.fill.c);
  for (const s of band.strokes) rect(s.x, s.y, s.w, s.h, s.c);
}

// ═══════════════════════════════════════════════════════════════════════════════
// CAPTIONS — 2 lines per chart, each line centred on its chart (264 / 671)
// ═══════════════════════════════════════════════════════════════════════════════
// Per-line boxes; y = baseline - fontSize (LO box-top -> baseline ~1.0 em)
const BASE_OFF = 1.0;
function captionLine(cx, baseline, w, runs, size) {
  slide.addText(runs, {
    x: px(cx - w / 2), y: px(baseline - size * BASE_OFF), w: px(w), h: px(34),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: size, lineSpacing: size * 1.2,
  });
}
const R = (text, o) => Object.assign({ text: text, options: o || {} });

// LEFT — line 1: red bold 'Overfit' + near-black regular remainder
captionLine(264, 500, 380, [
  R("Overfit", { bold: true, color: RED }),
  R(" (try to minimize the residuals ONLY)", { color: INK }),
], 17);
// LEFT — line 2: all near-black
captionLine(264, 519, 380, [
  R("Fails to detect the Pattern", { color: INK }),
], 17);
// RIGHT — line 1
captionLine(671, 500, 360, [
  R("Generalized", { bold: true, color: RED }),
  R(" (Residuals are not minimized)", { color: INK }),
], 17);
// RIGHT — line 2 ('Successes' sic — source grammar preserved)
captionLine(671, 519, 360, [
  R("Successes to detect the Pattern", { color: INK }),
], 17);

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
