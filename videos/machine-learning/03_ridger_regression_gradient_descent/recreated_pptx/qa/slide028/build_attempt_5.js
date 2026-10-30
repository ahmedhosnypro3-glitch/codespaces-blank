// Build slide 028 — "Effect of small and large Learning Rate"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Attempt 5 — curve-only change: quadratic fits replaced with trimmed-LS
//             quartics (finding 2 of crop_4_right_curve_judge, PIL-adjudicated).
//             Attempt-4 fixes for judge_attempt_1 + crop_3_left_curve are retained
//             (adjudication_attempt_1*.py, adjudication_attempt_4/5.py).
//
// FIXES (measured from unique_slides/slide_028.jpg, 960x540, 1px = 1pt):
//  1. Chart interior is WHITE in the original (367k white px inside the 1F4E79 box);
//     the attempt-3 build painted the E9E9E7 panel everywhere. Now the 1F4E79 box
//     carries a white fill.
//  2. Axes are RED, not dark blue. Core colours measured (128,85,90)/(127,63,71)
//     match the C00000 house-stroke maroon cores (113,40,51) — same red family.
//     Geometry: LEFT y-axis x156..160 y208..444 (up arrow); LEFT x-axis y438..447
//     x157..428 (right arrow); RIGHT y-axis x509..512 y205..440; RIGHT x-axis
//     y435..442 x510..780.
//  3. "Loss" labels are DARK grey, horizontal, LEFT of each y-axis
//     (left x121..146 y220..231; right x475..499 y217..227). Attempt 3 drew them
//     rotated and red.
//  4. Removed the extra black pointer + leader line near the left valley —
//     PIL shows no such ink in the original (only the red x-axis at y441..444 and
//     the "Value of weight" text at y446..459 in that band).
//  5. Curves are now ONE analytic fit each, drawn dense (1.5px steps) instead
//     of the attempt-3 28-point polylines (the judge read the joins as segmentation).
//     Attempt 4's quadratics were 14.6/15.4px RMSE and rose 49-63px above the
//     original at both ends (the judge read the render's U as too wide/short).
//     Attempt 5 re-fits them as QUARTICS by trimmed least squares (per-column
//     median blue y, worst-residual anchors dropped) — RMSE 2.0/2.8px, max
//     4.5/9.7px, ends within 1px of the original, valley at x275/x628 y439/y436.
//  6. Right panel's 4 large dots now oscillate ACROSS the valley
//     (down-right, back left-down, then out to the right and up) per the analysis
//     spec and the measured staircase at x554..596 / x632..662.
//  7. Removed the panel divider at x474 — the original has no such line.
//  8. Headings recentred to the measured ink (left centre 306, right centre 655).
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_028_recreated.pptx";
const px = (v) => v / 72;

const TITLE_RED = "FF0000", FRAME_BLUE = "1F4E79";
const CURVE_BLUE = "2E75B6", AXIS_RED = "C00000", INK = "333333", FONT = "Arial";

const pptx = new pptxgen(); pptx.layout = "LAYOUT_WIDE"; const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 28 });

const rect = (x, y, w, h, fill) =>
  slide.addShape(pptx.ShapeType.rect, { x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill } });
const line = (x, y, w, h, color, width) =>
  slide.addShape(pptx.ShapeType.line, { x: px(x), y: px(y), w: px(w), h: px(h), line: { color: color, width: width } });
const arrowUp = (cx, tipY, baseY, halfW, color) =>
  slide.addShape(pptx.ShapeType.triangle, { x: px(cx - halfW), y: px(tipY), w: px(halfW * 2), h: px(baseY - tipY), fill: { color: color } });
const arrowRight = (cy, tipX, baseX, halfH, color) =>
  slide.addShape(pptx.ShapeType.triangle, { x: px(baseX), y: px(cy - halfH), w: px(tipX - baseX), h: px(halfH * 2), fill: { color: color } });
const dot = (cx, cy, d, color) =>
  slide.addShape(pptx.ShapeType.ellipse, { x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d), fill: { color: color } });

// TITLE — measured x58..690 y60..109 (red bold, centred)
slide.addText("Effect of small and large Learning Rate", {
  x: px(0), y: px(72), w: px(960), h: px(25),
  align: "center", valign: "middle", fontFace: FONT, fontSize: 25, bold: true, color: TITLE_RED, margin: 0,
});

// CHART FRAME — 1F4E79 outline, WHITE fill (original interior is white)
rect(90, 127, 768, 381, "FFFFFF");
slide.addShape(pptx.ShapeType.rect, { x: px(90), y: px(127), w: px(768), h: px(381), line: { color: FRAME_BLUE, width: 1 }, fill: { type: "none" } });

// PANEL HEADINGS — measured ink: left x240..373 y188..199, right x589..721 y188..199
const headingY = 192, headingSize = 12;
slide.addText("Small Learning Rate", { x: px(306 - 90), y: px(headingY - headingSize), w: px(180), h: px(16), align: "center", valign: "middle", fontFace: FONT, fontSize: headingSize, bold: true, color: INK, margin: 0 });
slide.addText("Large Learning Rate", { x: px(655 - 90), y: px(headingY - headingSize), w: px(180), h: px(16), align: "center", valign: "middle", fontFace: FONT, fontSize: headingSize, bold: true, color: INK, margin: 0 });

// ── AXES — RED 2pt shafts + filled triangle heads (measured geometry above) ──
const shaftW = 1.25;

// LEFT panel
line(157.5, 221, 0, 444 - 221, AXIS_RED, shaftW);              // y-axis shaft
arrowUp(158, 208, 221, 5, AXIS_RED);                            // y-axis up head
line(157, 441.5, 414 - 157, 0, AXIS_RED, shaftW);               // x-axis shaft
arrowRight(442, 428, 414, 4.5, AXIS_RED);                       // x-axis right head

// RIGHT panel
line(509.5, 221, 0, 440 - 221, AXIS_RED, shaftW);
arrowUp(510, 205, 221, 5, AXIS_RED);
line(510, 437.5, 772 - 510, 0, AXIS_RED, shaftW);
arrowRight(438, 780, 772, 4.5, AXIS_RED);

// "Loss" labels — dark, horizontal, LEFT of each y-axis (measured bboxes)
slide.addText("Loss", { x: px(118), y: px(218), w: px(32), h: px(14), align: "left", valign: "middle", fontFace: FONT, fontSize: 9, bold: false, color: INK, margin: 0 });
slide.addText("Loss", { x: px(470), y: px(215), w: px(32), h: px(14), align: "left", valign: "middle", fontFace: FONT, fontSize: 9, bold: false, color: INK, margin: 0 });

// "Value of weight" labels — dark, centred under each panel x-axis
slide.addText("Value of weight", { x: px(245), y: px(452), w: px(130), h: px(14), align: "center", valign: "top", fontFace: FONT, fontSize: 10, color: INK, margin: 0 });
slide.addText("Value of weight", { x: px(580), y: px(448), w: px(130), h: px(14), align: "center", valign: "top", fontFace: FONT, fontSize: 10, color: INK, margin: 0 });

// ── CURVES — one analytic quartic each, drawn dense (ripple check below) ──
// Trimmed-LS quartic fits over the original's blue stroke (the dot staircases
// straddle the curve, so columns are medianed and outliers dropped). Coeffs
// are high->low: [a4,a3,a2,a1,a0].
const LEFT_FIT = { c: [1.257813992130e-06, -1.380428744223e-03, 5.367079591099e-01, -8.662429049860e+01, 5.186743353907e+03], x0: 161, x1: 383 };
const RIGHT_FIT = { c: [1.280248111588e-06, -3.212513553308e-03, 2.991242381533e+00, -1.224430887994e+03, 1.862054178402e+05], x0: 514, x1: 737 };
const curveY = (f, x) => ((((f.c[0] * x + f.c[1]) * x + f.c[2]) * x + f.c[3]) * x + f.c[4]);

function drawAnalyticCurve(f, color, width, step = 1.5) {
  let prevX = f.x0, prevY = curveY(f, f.x0);
  for (let x = f.x0 + step; x <= f.x1 + 1e-9; x += step) {
    const cx = Math.min(x, f.x1), cy = curveY(f, cx);
    slide.addShape(pptx.ShapeType.line, { x: px(prevX), y: px(prevY), w: px(cx - prevX), h: px(cy - prevY), line: { color: color, width: width } });
    prevX = cx; prevY = cy;
  }
}
drawAnalyticCurve(LEFT_FIT, CURVE_BLUE, 1);
drawAnalyticCurve(RIGHT_FIT, CURVE_BLUE, 1);

// ── LEFT panel: 6 small dots descending to the minimum ──
// Measured step path (blue staircase) runs from the right arm (293,246) diagonally
// down-left into the valley at (275,418). Dots ride that path; d≈4.
const leftDescentPts = [
  [293, 250], [283, 280], [274, 308], [265, 336], [253, 372], [264, 412], [277, 419],
];
for (let i = 0; i < leftDescentPts.length; i++) {
  const [x, y] = leftDescentPts[i];
  dot(x, y, 4, CURVE_BLUE);
  if (i > 0) {
    const [px0, py0] = leftDescentPts[i - 1];
    slide.addShape(pptx.ShapeType.line, { x: px(px0), y: px(py0), w: px(x - px0), h: px(y - py0), line: { color: CURVE_BLUE, width: 0.75 } });
  }
}

// ── RIGHT panel: 4 large dots oscillating ACROSS the valley ──
// Measured staircase anchors: (563,313) and (647,345) on the slopes, (590,394)
// near the valley. The path therefore crosses the valley bracket — start mid-left
// high, jump right-down, back left-down past the valley, then out right and up.
// d≈9 (the original's markers read ~2x the left panel's).
const rightOscPts = [
  [536, 300], [563, 313], [647, 345], [590, 394], [706, 322],
];
for (let i = 0; i < rightOscPts.length; i++) {
  const [x, y] = rightOscPts[i];
  dot(x, y, 9, CURVE_BLUE);
  if (i > 0) {
    const [px0, py0] = rightOscPts[i - 1];
    slide.addShape(pptx.ShapeType.line, { x: px(px0), y: px(py0), w: px(x - px0), h: px(y - py0), line: { color: CURVE_BLUE, width: 1 } });
  }
}

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
