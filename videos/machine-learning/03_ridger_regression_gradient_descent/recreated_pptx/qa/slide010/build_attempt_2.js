// slide_010.js — worker w010, 2026-10-24 (deck 03 completion pool, run 859463)
// Slide 010 "Overfit vs. Generalized" (no on-frame title; catalog title only).
//
// DEPENDENCY: 010 <- 009 (certified: gen_status=passed, visual_check=PASS,
// judge_attempt_5 + six crop certificates on render_5). This build IMPORTS the
// certified component `components/slide_009.js` — it does NOT re-derive the
// parent's geometry. Full-grid diff slide_009.jpg vs slide_010.jpg = 91.3%
// pixels identical (tol<=8) → inheritance, not a re-style
// (banked in qa/slide010/inheritance_diff.txt).
//
// COMPOSITION = parent base MINUS its 'marks' (dimension line / callout /
// rotated mm-labels / big red disc) and 'eqBoxes' (50.85²/63.64² boxes) —
// none of those exist on slide 010 — PLUS slide 010's measured delta:
//   * one green dashed cross per panel (horizontal from the y-axis to the
//     fitted line + vertical from the line down to the x-axis) ending in a
//     solid bright-green dot on the x-axis;
//   * two pale-rose projection pairs per panel (horizontal dashed line from
//     the y-axis to a highlighted point with a small dark-red left arrowhead
//     at the axis, a dark-red up-pointing triangle under the point, and a
//     vertical dashed line down to the x-axis).
// The white mouse cursor in the left panel is a video-capture artifact and is
// deliberately NOT drawn (deck judge ground rule (c)).
//
// Z-ORDER: parent underlay (chrome, panels incl. grid + periwinkle residual
// connectors + navy borders, axes, caption boxes) → delta → fitted lines +
// points + captions. This matches the frame: the blue line is drawn OVER the
// pale-rose projection dashes, and the orange dots cover the delta line ends.
//
// All delta coordinates are PIL-measured on unique_slides/slide_010.jpg
// (960x540 frame px; 1 px = 1 pt). Measured 2026-10-24:
//   GREEN dash colour  ~ (84,156,82) JPEG core of a 1px dash → 008000 family
//   BRIGHT green dot   (19,255,134) JPEG core           → 00FF00
//   PALE-ROSE dashes   (204..232, 179..216, 181..219)   → ECBAC4 (slide-009
//                      certified dimension-line family, visually identical)
//   red arrowheads / triangles core (127..153, 0..23, 12..35) → C00000 family

const path = require("path");
const pptxgen = require("pptxgenjs");
const base = require("./components/slide_009.js");

const OUT = path.resolve(__dirname, "..", "slide_010_recreated.pptx");
const px = (v) => v / 72; // frame px -> inches (1 px == 1 pt)

const GREEN = "008000";
const BRIGHTGREEN = "00FF00";
const PALE = "ECBAC4";
const RED = "C00000";

// ── measured delta geometry (frame px) ───────────────────────────────────────
const DELTA = [
  { name: "LEFT",
    // green cross: horizontal y 238.5 from the y-axis out to the fitted line,
    // vertical x 353 down to the x-axis, bright-green dot on the axis.
    green: {
      y: 238.5, x0: 136, x1: 353,
      head: { tipX: 127.5, baseX: 136, halfH: 3 },
      vx: 353, vy0: 240, vy1: 431,
      dot: { cx: 353, cy: 433, d: 8 },
    },
    // pale-rose projection pairs: two highlighted points per panel
    axisHead: { tipX: 127.5, baseX: 136, halfH: 3.5 },
    pairs: [
      { cx: 324, cy: 289.5, hy: 289.5, vx: 324, vy0: 301 },
      { cx: 381, cy: 301,   hy: 300.5, vx: 382, vy0: 312 },
    ] },
  { name: "RIGHT",
    green: {
      y: 287, x0: 550, x1: 766,
      head: { tipX: 541, baseX: 549, halfH: 3 },
      vx: 766.5, vy0: 288.5, vy1: 431,
      dot: { cx: 766.5, cy: 433, d: 8 },
    },
    axisHead: { tipX: 541, baseX: 549, halfH: 3.5 },
    pairs: [
      { cx: 737, cy: 290,   hy: 291.5, vx: 737, vy0: 302 },
      { cx: 794, cy: 301.5, hy: 301.5, vx: 795, vy0: 313 },
    ] },
];

// ── helpers (local; the parent's helpers are not exported) ──────────────────
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

// solid left-pointing triangle, tip at (tipX, cy), base at baseX.
// Rotated presets are declared in their UNROTATED frame (building.md law):
// w = visual vertical extent, h = visual horizontal extent, box centred on the
// visual centre; rotate 270 turns the up-pointing preset to point left.
function headLeft(pptx, slide, tipX, baseX, cy, halfH, color) {
  const wV = baseX - tipX;   // visual horizontal extent
  const hV = halfH * 2;      // visual vertical extent
  const cx = (tipX + baseX) / 2;
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(cx - hV / 2), y: px(cy - wV / 2), w: px(hV), h: px(wV),
    rotate: 270, fill: { color: color },
  });
}

// solid up-pointing triangle, tip at (cx, tipY), base at baseY
function headUp(pptx, slide, cx, tipY, baseY, halfW, color) {
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(cx - halfW), y: px(tipY), w: px(halfW * 2), h: px(baseY - tipY),
    fill: { color: color },
  });
}

function drawDelta(pptx, slide) {
  for (const d of DELTA) {
    // pale-rose projection pairs (drawn first; the green vertical crosses them)
    for (const p of d.pairs) {
      // horizontal dashed line from the y-axis out past the point (the dot --
      // drawn later by the parent's points block -- covers the middle exactly
      // as on the frame, whose last dash emerges ~2px right of the dot)
      seg(pptx, slide, d.axisHead.baseX, p.hy, p.cx + 5, p.hy, PALE, 1, "dash");
      // dark-red left arrowhead at the y-axis
      headLeft(pptx, slide, d.axisHead.tipX, d.axisHead.baseX, p.hy,
               d.axisHead.halfH, RED);
      // dark-red up triangle under the highlighted point (tip on the dot edge)
      headUp(pptx, slide, p.cx, p.cy + 4, p.cy + 10, 4, RED);
      // vertical dashed line from below the triangle down to the x-axis
      seg(pptx, slide, p.vx, p.vy0, p.vx, 434, PALE, 1, "dash");
    }
    // green dashed cross + bright-green axis dot
    const g = d.green;
    seg(pptx, slide, g.x0, g.y, g.x1, g.y, GREEN, 1, "dash");
    headLeft(pptx, slide, g.head.tipX, g.head.baseX, g.y, g.head.halfH, GREEN);
    seg(pptx, slide, g.vx, g.vy0, g.vx, g.vy1, GREEN, 1, "dash");
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(g.dot.cx - g.dot.d / 2), y: px(g.dot.cy - g.dot.d / 2),
      w: px(g.dot.d), h: px(g.dot.d), fill: { color: BRIGHTGREEN },
    });
  }
}

// ── compose ─────────────────────────────────────────────────────────────────
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// stage 1 — parent underlay (chrome, panels incl. grid + residual connectors,
// axes, caption boxes; the parent's 'marks' and 'eqBoxes' do not exist on
// slide 010 and are skipped)
base.renderBase(pptx, slide, {
  numeral: 10,
  only: { chrome: true, panels: true, axes: true, capBoxes: true },
});

// stage 2 — slide 010's own measured delta (under the fitted line: on the
// frame the blue line is drawn OVER the pale-rose projection dashes)
drawDelta(pptx, slide);

// stage 3 — parent fitted lines, points + captions on top
base.renderBase(pptx, slide, {
  numeral: 10,
  only: { fittedLines: true, points: true, captions: true },
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
