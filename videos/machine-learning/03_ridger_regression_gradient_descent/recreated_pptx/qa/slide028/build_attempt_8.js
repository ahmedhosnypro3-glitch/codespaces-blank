// Build slide 028 — "Effect of small and large Learning Rate"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// ATTEMPT 8 (w028, 2026-10-24). Attempt 7 (render_7) was re-judged by direct
// image reads and measured with PIL; five real deviations were found and are
// fixed here. Every number below is measured from
// unique_slides/slide_028.jpg (960x540, 1px = 1pt) — see
// qa/slide028/measure_attempt_8*.out.txt for the measurement records.
//
//  D1 LEFT-panel descent path [MAJOR, confirmed]:
//     original = SEVEN hollow circles (white core, cyan ring, d~8.5) descending
//     the LEFT arm at (179,251) (195,288) (220,349) (239,394) (247,413)
//     (262,436) (283,440), joined by six outward-bulging grey step arcs
//     (apex 7-13px off the chord). Attempt 7 drew SEVEN FILLED discs, five of
//     them on the right ascending arm where the original has NO marker ink
//     (strict hollow-ring detector: 0 hit on x276..440 except the valley ring;
//     saturated-disc detector: 0 cores in the whole left panel of the original).
//  D2 RIGHT-panel connector topology [MAJOR, confirmed]:
//     chord ink coverage on the original -> A-C 1.00, A-D 1.00, B-C 1.00;
//     A-B / C-D are only the curve (mean colour = curve cyan, no connector);
//     B-D 0.05. The original's drawn path is therefore D -> A -> C -> B.
//     Attempt 7 drew A->B->C->D (A-C and A-D absent, 0.00 coverage).
//  D3 RIGHT-panel marker fill [MINOR->fixed]: saturated-cyan core #32B6DD
//     (measured (50,182,221)), bbox 9-10 x 10-11 px -> filled disc d=10.
//     Attempt 7 used the light curve cyan 8FC3D1 at d=9.
//  D4 Title [MAJOR, confirmed]: original is a bold SERIF, core colour
//     (160,0,16)=#A00010, ink bbox x189..690 y72..101 (w=501 h=29, centre 439.5).
//     Attempt 7 was Arial bold #FF0000, ink x251..709 y76..99 (w=459 h=23,
//     centre 480). Now Times New Roman bold #A00010, box centred on 440.
//  D5 "Value of weight" [MAJOR, confirmed]: the original sets both labels BOLD,
//     right-aligned under the x-axis ARROW END (left ink x367..453 y448..460,
//     right ink x707..797 y450..462) — not centred under the axis as attempt 7
//     drew them (ink x276..343 / x611..678, regular weight).
//  D6 Subplot headings [MINOR->fixed]: original core near-black (41,43,40),
//     ink x239..374 y187..200 (w=135 h=13); attempt 7 was #62625F grey and
//     smaller (w=114 h=11, y184..195). Now #2B2D2A, size 14, +4px down.
//
// RETAINED (verified correct by measurement):
//  * white chart interior (367k white px inside the 1F4E79 box);
//  * RED axes (C00000 family) at the measured geometry, filled triangle heads;
//  * "Loss" labels dark, horizontal, left of each y-axis (ink x122..154 /
//    x475..498 y215..230);
//  * one analytic quartic per curve (ripple-checked, valley x275/x628);
//  * curve colour 8FC3D1 (measured means (155,199,209)/(140,196,210));
//  * 4 right-panel markers at the measured centroids (562,315) (593,395)
//    (683,351) (710,284);
//  * no panel divider, no extra black pointer (the black mark near the valley
//    in the original is the mouse cursor — ground rule (c)).
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_028_recreated.pptx";
const px = (v) => v / 72;

const TITLE_RED = "A00010", FRAME_BLUE = "1F4E79";
const CURVE_BLUE = "8FC3D1",   // measured original curve ink
      DISC_CYAN = "32B6DD",    // measured saturated marker fill (right panel)
      CONNECTOR = "A6BCBE",    // measured step-connector grey-cyan
      AXIS_RED = "C00000", INK = "333333", FONT = "Arial",
      HEADING_INK = "2B2D2A";

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
const ring = (cx, cy, d, color, width) =>
  slide.addShape(pptx.ShapeType.ellipse, { x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: "FFFFFF" }, line: { color: color, width: width } });
// quadratic Bezier P0 -> C -> P1 as a dense polyline (frame px)
function bezier(p0, c, p1, color, width, steps = 16) {
  let prev = p0;
  for (let i = 1; i <= steps; i++) {
    const t = i / steps, u = 1 - t;
    const x = u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0];
    const y = u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1];
    line(prev[0], prev[1], x - prev[0], y - prev[1], color, width);
    prev = [x, y];
  }
}

// TITLE — measured ink x189..690 y72..101 (bold serif #A00010, w=501 h=29, centre 439.5)
slide.addText("Effect of small and large Learning Rate", {
  x: px(140), y: px(63), w: px(600), h: px(40),
  align: "center", valign: "middle", fontFace: "Times New Roman", fontSize: 30,
  bold: true, color: TITLE_RED, margin: 0,
});

// CHART FRAME — 1F4E79 outline, WHITE fill (original interior is white)
rect(90, 127, 768, 381, "FFFFFF");
slide.addShape(pptx.ShapeType.rect, { x: px(90), y: px(127), w: px(768), h: px(381), line: { color: FRAME_BLUE, width: 1 }, fill: { type: "none" } });

// PANEL HEADINGS — measured ink left x239..374 y187..200, right x589..722 y187..200
const headingY = 192, headingSize = 14;
slide.addText("Small Learning Rate", { x: px(306 - 90), y: px(headingY - 9), w: px(180), h: px(18), align: "center", valign: "middle", fontFace: FONT, fontSize: headingSize, bold: true, color: HEADING_INK, margin: 0 });
slide.addText("Large Learning Rate", { x: px(655 - 90), y: px(headingY - 9), w: px(180), h: px(18), align: "center", valign: "middle", fontFace: FONT, fontSize: headingSize, bold: true, color: HEADING_INK, margin: 0 });

// ── AXES — RED 2pt shafts + filled triangle heads (measured geometry) ──
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

// "Value of weight" — BOLD, right-aligned under the x-axis arrow end
// (measured left ink x367..453 y448..460, right ink x707..797 y450..462)
slide.addText("Value of weight", { x: px(335), y: px(445), w: px(120), h: px(16), align: "right", valign: "top", fontFace: FONT, fontSize: 12, bold: true, color: INK, margin: 0 });
slide.addText("Value of weight", { x: px(679), y: px(447), w: px(120), h: px(16), align: "right", valign: "top", fontFace: FONT, fontSize: 12, bold: true, color: INK, margin: 0 });

// ── CURVES — one analytic quartic each, drawn dense (ripple check below) ──
const LEFT_FIT = { c: [1.257813992130e-06, -1.380428744223e-03, 5.367079591099e-01, -8.662429049860e+01, 5.186743353907e+03], x0: 161, x1: 383 };
const RIGHT_FIT = { c: [1.280248111588e-06, -3.212513553308e-03, 2.991242381533e+00, -1.224430887994e+03, 1.862054178402e+05], x0: 514, x1: 737 };
const curveY = (f, x) => ((((f.c[0] * x + f.c[1]) * x + f.c[2]) * x + f.c[3]) * x + f.c[4]);

function drawAnalyticCurve(f, color, width, step = 1.5) {
  let prevX = f.x0, prevY = curveY(f, f.x0);
  for (let x = f.x0 + step; x <= f.x1 + 1e-9; x += step) {
    const cx = Math.min(x, f.x1), cy = curveY(f, cx);
    line(prevX, prevY, cx - prevX, cy - prevY, color, width);
    prevX = cx; prevY = cy;
  }
}

// ── RIGHT panel: step connectors D -> A -> C -> B (measured chord topology) ──
// Drawn UNDER the curve and the markers, in the measured connector grey.
const RP = { A: [562, 315], B: [593, 395], C: [683, 351], D: [710, 284] };
for (const [p, q] of [[RP.D, RP.A], [RP.A, RP.C], [RP.C, RP.B]]) {
  line(p[0], p[1], q[0] - p[0], q[1] - p[1], CONNECTOR, 1);
}

// stroke weight 2.5pt: the original's curve core measures 3-5 frame px across
// (measure_attempt_8_stroke.out.txt); attempt 7's 1pt hairline measured ~1 px.
drawAnalyticCurve(LEFT_FIT, CURVE_BLUE, 2.5);
drawAnalyticCurve(RIGHT_FIT, CURVE_BLUE, 2.5);

// ── LEFT panel: small-learning-rate descent = 7 hollow circles + 6 step arcs ──
// Measured circle centres (white core, cyan ring) and per-hop arc apexes
// (quadratic control = 2*apex - (P0+P1)/2, see measure_attempt_8g).
const leftCircles = [[179, 251], [195, 288], [220, 349], [239, 394], [247, 413], [262, 436], [283, 440]];
const hopControls = [
  [209.0, 254.5],   // hop 1 apex (198,262)
  [226.5, 305.5],   // hop 2 apex (217,312)
  [246.5, 364.5],   // hop 3 apex (238,368)
  [255.0, 398.5],   // hop 4 apex (249,401)
  [271.5, 413.5],   // hop 5 apex (263,419)
  [273.5, 420.0],   // hop 6 apex (273,429)
];
for (let i = 0; i < hopControls.length; i++) {
  bezier(leftCircles[i], hopControls[i], leftCircles[i + 1], CONNECTOR, 1, 14);
}
for (const [x, y] of leftCircles) {
  ring(x, y, 7.5, CURVE_BLUE, 1);
}

// ── RIGHT panel: 4 filled markers at the measured centroids, saturated cyan ──
for (const [x, y] of [RP.A, RP.B, RP.C, RP.D]) {
  dot(x, y, 10, DISC_CYAN);
}

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
