// components/slide_009.js — BANKED composition of slide 009
// ("Overfit vs. Generalized" — metadata-only title; NO title ink on the frame),
// ML lecture 03 (03_ridger_regression_gradient_descent).
//
// REFRESHED 2026-10-24 (worker w009): re-sourced from the CERTIFIED attempt-4/5
// build/slide_009.js after the full-slide + six-crop certification of render_5
// (cascade law: earlier bankings described the pre-attempt-4 build and are
// superseded by this file).
//
// CERTIFICATION (2026-10-24, w009):
//   Build: recreated_pptx/build/slide_009.js (md5 dbb694bc840268f9e8008cf1307aa0ab,
//     banked as qa/slide009/build_attempt_5.js) -> slide_009_recreated.pptx
//     (single plain-named version, md5 9b0efe4f1255774d7c2aac4c3e2e04dc).
//   Render: 150 dpi -> qa/slide009/render_5.png (2001x1125,
//     md5 84c8bf3179992d74717fa070f5f8c607). House-chrome check PASS
//     (qa/slide009/house_chrome_5.txt).
//   Visual gate, BOTH legs from render_5: full-slide judge_attempt_5.txt PASS +
//     six zoomed crop certificates crop_5_{eq_left,eq_right,cap_left,cap_right,
//     chart_left,chart_right}_judge.txt each PASS (cut_crops_5.txt VERDICT PASS,
//     matched effective scale). Pre-judge selfcheck: selfcheck_attempt_5.txt PASS
//     (0 FIX).
//   Attempt 4 (render_4) was a build round whose selfcheck caught the equation
//     containment/high-placement defect; it was superseded BEFORE judging and its
//     render is banked untouched. Attempts 1-3 and their (partly wrong) adjudication
//     records stay banked; the attempt-3 "mm labels are hallucinations" call was
//     disproved by direct de-rotated frame reads and is superseded by this build.
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide — house chrome
// (numeral 9) + the two scatter charts (each: white interior over a navy border,
// 16x16 grid, light-periwinkle dashed residual connectors from every point to its
// perpendicular foot on the fitted line, blue fitted line, 12 orange points, the
// measured annotation group — pale-rose dimension line from the top outlier to
// the fitted line with a solid red arrowhead, pale-rose callout leader + red head
// pointing at the outlier, and the rotated red '50.85 mm' / '63.64 mm' label — plus
// the LEFT chart's large solid red disc on the dimension line and red axes with
// triangular heads) + the two pale-cyan annotation boxes with their equation PNGs
// + the two caption-band boxes (cream fill, rose open-top outline) + the four
// caption lines. opts:
//   { numeral }       — override the badge numeral (a recap variant passes its own
//                       number; the badge numeral is ALWAYS the number printed on
//                       the VARIANT's own original frame)
//   { skip: {...} }   — omit any block: chrome, panels, fittedLines, points,
//                       marks, axes, eqBoxes, capBoxes, captions
//   { only: {...} }   — draw ONLY the listed blocks (a child composes its delta)
//
// Draw order inside BLOCKS is the certified z-order. Blocks are split per element
// rather than per panel: the two panels are disjoint rectangles (LEFT x95..466,
// RIGHT x486.5..871.5) and no element of either panel crosses the other's border,
// so cross-block z-order is geometrically irrelevant. NOTE the residual connectors
// are drawn inside the 'panels' block (before fittedLines/points) so the line and
// points cover their ends; the rotated labels are inside 'marks' (after eqBoxes?
// no — marks runs before eqBoxes; the labels sit outside the equation boxes and do
// not overlap them). capBoxes is ordered before captions so the cream fill sits
// under the caption ink.
//
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

// ── measured palette ──────────────────────────────────────────────────────────
const NAVY     = "000080";   // chart-panel border  (frame core 0,0,108)
const INTERIOR = "F5F5F5";   // chart interior      (frame ~248,248,248)
const GRID     = "D8D8D6";   // grid lines          (frame cores 207..238 over 250)
const RED      = "C00000";   // axes / red marks / caption keyword (house family)
const BLUE     = "0000FF";   // fitted lines        (frame core 0,0,132)
const ORANGE   = "FFA500";   // data points         (frame core 255,120,0)
const BIGRED   = "EE3145";   // the LEFT chart's large solid disc (frame core 238,49,69)
const BOXFILL  = "ECFDF9";   // annotation box fill (frame median 236,253,249)
const BOXLINE  = "000080";   // annotation box border = navy (same as panel border)
const INK      = "333333";   // caption remainder ink (frame core 49,51,37)
const DIMLINE  = "ECBAC4";   // pale-rose dimension line / callout leader (frame core 240,190,200)
const CONN     = "B4B2D2";   // light-periwinkle dashed residual connectors (frame core ~200,197,220)
const FONT     = "Times New Roman"; // serif, matches the frame (Liberation Serif metrics)

// caption-band box palette (PIL-measured 2026-10-24, frame cores)
const CAPFILL = "FBFCEC"; // caption-box fill (frame median 251,252,236)
const BAND_STROKES = [
  { x: 95.5,  y: 479, w: 2, h: 49, c: "E2C6C3" },   // LEFT left vertical  (226,198,195)
  { x: 432.5, y: 479, w: 2, h: 49, c: "F0E6E7" },   // LEFT right vertical (240,230,231)
  { x: 96,    y: 527.5, w: 337, h: 2, c: "DCBBBB" }, // LEFT bottom rule  (220,187,187)
  { x: 502,   y: 479, w: 2, h: 49, c: "D3BCB9" },   // RIGHT left vertical (211,188,185)
  { x: 839.5, y: 479, w: 2, h: 49, c: "CAA5A6" },   // RIGHT right vertical (202,165,166)
  { x: 503,   y: 527.5, w: 337, h: 2, c: "D9BBBA" }, // RIGHT bottom rule (217,187,186)
];
const BAND_FILLS = [
  { x: 97,  y: 480, w: 335, h: 47 },
  { x: 504, y: 480, w: 335, h: 47 },
];

// ── equation PNG assets (600-dpi matplotlib mathtext, deck math law) ──────────
// attempt-4 re-render: 12.1pt DejaVu Sans -> ink 702/704 px (81.9/82.1pt) wide,
// 96px (11.2pt) tall; placed so the INK box lands on the frame's measured
// x226..307 / x643..723, y155..167 (8px @600dpi pad = 0.8pt).
const ASSETS = path.resolve(__dirname, "..", "assets");

// ── chart panels ─────────────────────────────────────────────────────────────
const PANELS = [
  { name: "LEFT",
    bx: 95,   by: 107, bw: 371, bh: 367,   // navy border rect
    fx: 98,   fy: 111, fw: 365, fh: 359,   // white interior
    col0: 103.5, colPitch: 23, nCol: 16,   // vertical grid lines
    row0: 120.5, rowPitch: 22.4, nRow: 16, // horizontal grid lines
    axisX: 126.5, axisX0: 152, axisX1: 437, // y-axis (vertical)
    axisY: 434,   axisY0: 124, axisY1: 428, // x-axis (horizontal)
    headUp:   { cx: 126.5, tipY: 143, baseY: 151, halfW: 4.0 },
    headRight:{ cy: 434,   tipX: 435, baseX: 428, halfH: 3.5 },
    line: { x0: 141, y0: 351, x1: 433, y1: 201 }, // blue fitted line
    dim: { x0: 197, y0: 146, x1: 249, y1: 292 },  // pale-rose dimension line
    dimHead: { tipX: 249, tipY: 292, ux: 0.336, uy: 0.942, bw: 7, h: 7.5 },
    tail: { x0: 164, y0: 167, x1: 185, y1: 157 }, // callout leader
    tailHead: { tipX: 191, tipY: 150, ux: 0.707, uy: -0.707, bw: 6.5, h: 8 },
    label: { text: "50.85 mm", cx: 210, cy: 212, rot: -69 },
    bigDisc: { cx: 232.5, cy: 241, d: 24.5 },     // LEFT chart only
    points: [
      [197.5, 145.0], [188.5, 355.5], [176.5, 380.5], [242.5, 327.5], [260.5, 333.5],
      [294.0, 333.5], [324.0, 290.0], [328.5, 332.0], [381.5, 301.5], [397.5, 249.0],
      [421.5, 255.0], [233.5, 362.0],
    ] },
  { name: "RIGHT",
    bx: 486.5, by: 107, bw: 385, bh: 367,
    fx: 489.5, fy: 111, fw: 378, fh: 359,
    col0: 517.5, colPitch: 23, nCol: 16,
    row0: 120.5, rowPitch: 22.4, nRow: 16,
    axisX: 540,   axisX0: 152, axisX1: 437,
    axisY: 434,   axisY0: 538, axisY1: 841,
    headUp:   { cx: 540,   tipY: 143, baseY: 151, halfW: 3.5 },
    headRight:{ cy: 434,   tipX: 848, baseX: 841, halfH: 3.5 },
    line: { x0: 555, y0: 387, x1: 849, y1: 247 },
    dim: { x0: 611, y0: 147, x1: 682, y1: 324 },
    dimHead: { tipX: 682, tipY: 324, ux: 0.372, uy: 0.928, bw: 7, h: 8 },
    tail: { x0: 585, y0: 158, x1: 601, y1: 152 },
    tailHead: { tipX: 607, tipY: 144, ux: 0.707, uy: -0.707, bw: 6.5, h: 8 },
    label: { text: "63.64 mm", cx: 637, cy: 237, rot: -68 },
    bigDisc: null,
    points: [
      [611.0, 145.0], [601.5, 355.5], [589.5, 380.5], [656.0, 327.0], [674.0, 333.5],
      [707.5, 333.5], [737.5, 290.0], [741.5, 332.0], [794.0, 302.0], [810.0, 249.0],
      [834.5, 255.0], [647.0, 362.0],
    ] },
];

// ── annotation boxes + equation images ───────────────────────────────────────
const BOXES = [
  { x: 216, y: 148, w: 102, h: 27,
    img: path.join(ASSETS, "eq_009_left_attempt4.png"),
    ix: 3.127778, iy: 2.141667, iw: 1.195, ih: 0.185 },
  { x: 631, y: 148, w: 104, h: 27,
    img: path.join(ASSETS, "eq_009_right_attempt4.png"),
    ix: 8.919444, iy: 2.141667, iw: 1.198333, ih: 0.185 },
];

// ── captions: 2 lines per chart, each centred on its chart (264 / 671) ───────
const CAP_BASE_OFF = 1.0;
const CAPTIONS = [
  { cx: 264, base: 500, w: 380, size: 17,
    runs: [["Overfit", { bold: true, color: RED }],
           [" (try to minimize the residuals ONLY)", { color: INK }]] },
  { cx: 264, base: 519, w: 380, size: 17,
    runs: [["Fails to detect the Pattern", { color: INK }]] },
  { cx: 671, base: 500, w: 360, size: 17,
    runs: [["Generalized", { bold: true, color: RED }],
           [" (Residuals are not minimized)", { color: INK }]] },
  { cx: 671, base: 519, w: 360, size: 17,
    runs: [["Successes to detect the Pattern", { color: INK }]] },
];

function drawChrome(pptx, slide, opts) {
  const n = opts && opts.numeral !== undefined ? opts.numeral : 9;
  drawHouseChrome(pptx, slide, { numeral: n });
}

// plain segment (no heads): left-to-right, flipV when the left end is lower
function seg(pptx, slide, xa, ya, xb, yb, color, width, dashType) {
  const xl = Math.min(xa, xb), xr = Math.max(xa, xb);
  const yl = xa <= xb ? ya : yb, yr = xa <= xb ? yb : ya;
  const line = { color: color, width: width };
  if (dashType) line.dashType = dashType;
  slide.addShape(pptx.ShapeType.line, {
    x: px(xl), y: px(Math.min(yl, yr)), w: px(xr - xl), h: px(Math.abs(yr - yl)),
    flipV: yl > yr, line: line,
  });
}

// solid triangular head, tip at (tipX,tipY), pointing along (ux,uy)
function head(pptx, slide, tipX, tipY, ux, uy, bw, h) {
  const cx = tipX - ux * h / 2, cy = tipY - uy * h / 2;
  const rot = Math.atan2(ux, -uy) * 180 / Math.PI;
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(cx - bw / 2), y: px(cy - h / 2), w: px(bw), h: px(h),
    rotate: rot, fill: { color: RED },
  });
}

function drawPanels(pptx, slide) {
  const rect = (x, y, w, h, fill) =>
    slide.addShape(pptx.ShapeType.rect, {
      x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill },
    });
  const stroked = (x, y, w, h, color, width) =>
    slide.addShape(pptx.ShapeType.rect, {
      x: px(x), y: px(y), w: px(w), h: px(h), line: { color: color, width: width },
    });
  for (const p of PANELS) {
    // white interior (first, so the grid/axes sit on it)
    rect(p.fx, p.fy, p.fw, p.fh, INTERIOR);
    // 16 vertical + 16 horizontal 1pt grid lines inside the measured grid box
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
    // residual connectors: point -> perpendicular foot on the fitted line
    const { x0: lx0, y0: ly0, x1: lx1, y1: ly1 } = p.line;
    const ldx = lx1 - lx0, ldy = ly1 - ly0, l2 = ldx * ldx + ldy * ldy;
    for (const [cx, cy] of p.points) {
      const t = ((cx - lx0) * ldx + (cy - ly0) * ldy) / l2;
      const fx = lx0 + t * ldx, fy = ly0 + t * ldy;
      if (Math.hypot(fx - cx, fy - cy) < 9) continue;
      seg(pptx, slide, cx, cy, fx, fy, CONN, 0.75, "dash");
    }
    // navy border on top
    stroked(p.bx, p.by, p.bw, p.bh, NAVY, 1);
  }
}

function drawFittedLines(pptx, slide) {
  for (const p of PANELS) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(p.line.x0), y: px(p.line.y1), w: px(p.line.x1 - p.line.x0),
      h: px(p.line.y0 - p.line.y1), flipV: true,
      line: { color: BLUE, width: 2 },
    });
  }
}

function drawPoints(pptx, slide) {
  for (const p of PANELS) {
    for (const [cx, cy] of p.points) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(cx - 7.5 / 2), y: px(cy - 7.5 / 2), w: px(7.5), h: px(7.5),
        fill: { color: ORANGE },
      });
    }
  }
}

function drawMarks(pptx, slide) {
  // measured annotation group + the LEFT chart's large solid disc + rotated label.
  // Disc drawn after the dimension line so it covers it, as on the frame.
  for (const p of PANELS) {
    seg(pptx, slide, p.dim.x0, p.dim.y0, p.dim.x1, p.dim.y1, DIMLINE, 1.0);
    head(pptx, slide, p.dimHead.tipX, p.dimHead.tipY, p.dimHead.ux, p.dimHead.uy,
         p.dimHead.bw, p.dimHead.h);
    seg(pptx, slide, p.tail.x0, p.tail.y0, p.tail.x1, p.tail.y1, DIMLINE, 1.0);
    head(pptx, slide, p.tailHead.tipX, p.tailHead.tipY, p.tailHead.ux, p.tailHead.uy,
         p.tailHead.bw, p.tailHead.h);
    if (p.bigDisc) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(p.bigDisc.cx - p.bigDisc.d / 2), y: px(p.bigDisc.cy - p.bigDisc.d / 2),
        w: px(p.bigDisc.d), h: px(p.bigDisc.d), fill: { color: BIGRED },
      });
    }
    slide.addText(p.label.text, {
      x: px(p.label.cx - 45), y: px(p.label.cy - 7), w: px(90), h: px(14),
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 11, bold: true, color: RED,
      rotate: p.label.rot,
    });
  }
}

function drawAxes(pptx, slide) {
  for (const p of PANELS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(p.axisX - 0.5), y: px(p.axisX0), w: px(1), h: px(p.axisX1 - p.axisX0),
      fill: { color: RED },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: px(p.axisY0), y: px(p.axisY - 0.5), w: px(p.axisY1 - p.axisY0), h: px(1),
      fill: { color: RED },
    });
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
  }
}

function drawEqBoxes(pptx, slide) {
  for (const b of BOXES) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: BOXFILL }, line: { color: BOXLINE, width: 1 },
    });
    slide.addImage({ path: b.img, x: b.ix, y: b.iy, w: b.iw, h: b.ih });
  }
}

function drawCaptions(pptx, slide) {
  const R = (text, o) => Object.assign({ text: text, options: o || {} });
  for (const c of CAPTIONS) {
    const runs = c.runs.map(([t, o]) => R(t, o));
    slide.addText(runs, {
      x: px(c.cx - c.w / 2), y: px(c.base - c.size * CAP_BASE_OFF), w: px(c.w), h: px(34),
      align: "center", valign: "top", margin: 0,
      fontFace: FONT, fontSize: c.size, lineSpacing: c.size * 1.2,
    });
  }
}

function drawBandMarks(pptx, slide) { // block name: capBoxes
  for (const f of BAND_FILLS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(f.x), y: px(f.y), w: px(f.w), h: px(f.h), fill: { color: CAPFILL },
    });
  }
  for (const m of BAND_STROKES) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(m.x), y: px(m.y), w: px(m.w), h: px(m.h), fill: { color: m.c },
    });
  }
}

const BLOCKS = {
  chrome: drawChrome,
  panels: drawPanels,
  fittedLines: drawFittedLines,
  points: drawPoints,
  marks: drawMarks,
  axes: drawAxes,
  eqBoxes: drawEqBoxes,
  capBoxes: drawBandMarks,
  captions: drawCaptions,
};

function renderBase(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  const only = opts.only || null;
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (only && !only[name]) continue;
    if (!only && skip[name]) continue;
    fn(pptx, slide, opts);
  }
}

module.exports = {
  renderBase, BLOCKS,
  PANELS, BOXES, CAPTIONS, BAND_FILLS, BAND_STROKES,
  NAVY, INTERIOR, GRID, RED, BLUE, ORANGE, BIGRED, BOXFILL, BOXLINE, INK, FONT,
  DIMLINE, CONN, CAPFILL, ASSETS, CAP_BASE_OFF,
};
