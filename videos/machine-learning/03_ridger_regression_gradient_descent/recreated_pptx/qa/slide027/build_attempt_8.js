// Build slide 027 — "Follow Negative Direction of Gradient with Selected Learning Rate"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome =
// shared_patterns/house_chrome.js — white canvas, E9E9E7 panel, C00000 L/R/bottom
// strokes with NO top stroke, FDFD96 badge + 6A5ACD ring, numeral 27).
//
// RESUMED WORKER build (attempt 2 — offline refinements only, no judge evidence existed
// on the inherited attempt-1 render). A previous worker died in an upstream provider
// storm mid-task; its banked measured-geometry dossier
// (qa/slide027/measured_geometry.md) is the AUTHORITY for every element below.
// Supplemental probes (qa/slide027/prep_geometry.py + output, fit_fonts.py + output):
//   - Font fit: title = Calibri Bold 31.5pt (width fit 553/300px, cap 19.75 vs measured
//     21px band incl JPEG halo; dossier glyph reading 'l'-tail/'f'-curl = Calibri;
//     spec estimate 32-36pt consistent). Labels = Arial (Liberation-Sans metrics)
//     per-label width-fit sizes 16.88-18.88pt (tightest single-family consistency;
//     caps 11.75-13 vs measured 13-14 bands incl halo). theta glyphs ~22pt (height fit).
//   - Parabola: NOT a polynomial (best deg-5 LSQ residual 8.9px > 5px tolerance) ->
//     the banked 54-point trace itself is the geometry; drawn as ONE custGeom
//     Catmull-Rom cubic-bezier chain (B1=P1+(P2-P0)/6, B2=P2-(P3-P1)/6 per
//     building.md), full-slide bbox with absolute inch points (curved-arrows-custgeom
//     pattern), stroke black 2pt, no fill.
//   - Dot discs: pure-blue mask shows 12-13px discs (dossier bboxes were halo-inclusive);
//     d=13 drawn. Yellow min dot d=12.5.
//   - theta-hat: caret drawn as an open custGeom 2-stroke path at the measured ink
//     bbox (x440..448, rows 480..484) over the theta body.
//
// FRAME-vs-SPEC deviations (banked dossier + PIL refutations, frame wins):
//   1. NINE blue descent dots (spec said ~8)          4. dashed leader BELOW the yellow
//   2. NO '+' on the x-axis (spec claimed one;          min dot (spec missed it) -> drawn
//      PIL refuted)                                  5. graph box x193.5..716 / y167..507
//   3. NO small arrow at 'Learning step'                 (spec estimated %s)
//      (spec claimed one; PIL refuted)               6. title = TWO measured lines
//
// All frame px are 960x540 with 1px = 1pt = 1/72in. Hex colors never carry '#'.
// Text boxes: single-line, valign top, explicit lineSpacing (LO/PowerPoint auto-pitch
// divergence law); DY[] per-element closed-loop corrections (0 on attempt 1, tuned
// from the 150dpi render against the dossier bands).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const px = (v) => v / 72; // frame px -> inches
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_027_recreated.pptx";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- house chrome (panel, strokes L/R/bottom — NO top stroke, badge "27") ----
drawHouseChrome(pptx, slide, { numeral: 27 });

// ---- TITLE: Calibri Bold 31.5pt, 8B0000, two measured single-line boxes --------
// LO baseline model (hhea metrics via PIL, Calibri Bold: extent 0.996em, ascent
// 0.747em): with lineSpacing L = 1.2*S, baseline = boxTop + (L - 0.996*S)/2 + 0.747*S
//                                             = boxTop + 0.849*S (+ DY correction).
const T_S = 31.5;
const T_LS = 1.2 * T_S;            // pinned lineSpacing (pt)
const T_BASE_FRAC = 0.849;         // boxTop -> baseline, fraction of S
// Closed-loop (w4 worker, 2026-10-20): PIL of render_1 showed L1 ink rows 75.9..102.8
// and L2 111.3..137.7 vs frame bands 73..100 / 108..134 -> whole title block sat
// ~2.9-3.4 frame px LOW. dy corrections pull it back onto the measured bands
// (independently re-measured on the JPEG: L1 73..100 cols 192..742, L2 108..134
// cols 322..620 — dossier numbers confirmed).
const TITLE = [
  // measured: L1 cap band rows 73..93, ink x 191..744 (advance 553, cx 467.5)
  { t: "Follow Negative Direction of Gradient with", base: 92.75, cx: 467.5, boxW: 660, dy: -2.9 },
  // measured: L2 cap rows 108..~128, 'g' descender 134..135, ink x 321..621 (advance 300, cx 471)
  { t: "Selected Learning Rate", base: 127.75, cx: 471.0, boxW: 400, dy: -3.4 },
];
for (const L of TITLE) {
  slide.addText(L.t, {
    x: px(L.cx - L.boxW / 2),
    y: px(L.base - T_BASE_FRAC * T_S + (L.dy || 0)),
    w: px(L.boxW), h: px(52),
    align: "center", valign: "top", margin: 0,
    fontFace: "Calibri", fontSize: T_S, bold: true, color: "8B0000",
    lineSpacing: T_LS,
  });
}

// ---- graph box: FF0000 2pt border, WHITE interior ------------------------------
// measured edges: left x193..194, right x716, top y167, bottom y507.
// Attempt-4 fix (w8 resumption, 2026-10-20/21): the box interior is NOT the panel
// gray. Scanline probe of the original frame (y=250/300/470, plus five clean
// interior patches): panel left/right of the box reads (231,233,230) = E9E9E7, but
// the box interior reads (254,255,253) — byte-identical to the canvas white outside
// the panel. The original PowerPoint draws a white-filled rect on the gray panel
// (spec brief calls it a "no-fill rectangle"; pixels show canvas-white fill).
// Attempt-3 build filled it E9E9E7 (measured delta 254 vs 232 = 8.6% luminance) ->
// changed to FFFFFF, matching the spec's no-fill intent AND the frame.
slide.addShape(pptx.ShapeType.rect, {
  x: px(193.5), y: px(167), w: px(522.5), h: px(340),
  fill: { color: "FFFFFF" },
  line: { color: "FF0000", width: 2 },
});

// ---- axes (black 2pt) + arrowheads (filled custGeom triangles at measured bboxes)
// y-axis: line x222..223 rows 206..436; head apex (223,206), base row 222 x218..228
slide.addShape(pptx.ShapeType.line, {
  x: px(222.5), y: px(222), w: 0, h: px(214),
  line: { color: "000000", width: 2 },
});
// x-axis: line y435..437 cols 222..685; head apex (686,436), base col 670 rows 431..442
slide.addShape(pptx.ShapeType.line, {
  x: px(222), y: px(436), w: px(448), h: 0,
  line: { color: "000000", width: 2 },
});
// filled arrowhead helper: closed custGeom triangle in frame px
function triShape(pts) {
  const path = pts.map((p, i) =>
    i === 0 ? { x: px(p[0]), y: px(p[1]), moveTo: true } : { x: px(p[0]), y: px(p[1]) });
  path.push({ close: true });
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,           // full-slide bbox; absolute inch points
    fill: { color: "000000" }, line: { color: "000000", width: 0 },
    points: path,
  });
}
triShape([[223, 206], [218, 222], [228, 222]]);   // y-axis up-arrow
triShape([[686, 436], [670, 431], [670, 442]]);   // x-axis right-arrow

// ---- dashed leader lines (measured dash rows; 2pt black, drawn dash-by-dash) ----
const DASHES = [
  { x: 262.5, rows: [[272, 278], [286, 292], [300, 306], [314, 320], [328, 335],
                     [343, 348], [357, 363], [371, 377], [385, 391], [400, 406],
                     [414, 420], [428, 434]] },
  { x: 444.5, rows: [[415, 422], [430, 436]] },
];
for (const d of DASHES) {
  for (const [y0, y1] of d.rows) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(d.x), y: px(y0), w: 0, h: px(y1 - y0 + 1),
      line: { color: "000000", width: 2 },
    });
  }
}

// ---- parabola: banked 54-point trace -> Catmull-Rom cubic-bezier custGeom -------
const TRACE = [
  [253, 230], [254, 236], [255, 242], [256, 246], [259, 252], [262, 272], [268, 280],
  [270, 286], [272, 292], [274, 296], [276, 300], [278, 302], [288, 318], [290, 322],
  [291, 324], [293, 326], [294, 328], [296, 330], [297, 332], [299, 334], [313, 350],
  [316, 352], [318, 354], [320, 356], [322, 358], [324, 360], [363, 386], [365, 388],
  [383, 395], [400, 400], [420, 404], [436, 406], [445, 408],
  [463, 406], [479, 404], [497, 400], [525, 390], [543, 380], [561, 368], [571, 360],
  [584, 348], [595, 336], [604, 324], [612, 312], [619, 300], [624, 288], [628, 280],
  [632, 268], [635, 260], [637, 252], [638, 248], [639, 244], [640, 240], [641, 236],
];
function catmullRomPoints(P) {
  const phantom0 = { x: 2 * P[0][0] - P[1][0], y: 2 * P[0][1] - P[1][1] };
  const phantomN = { x: 2 * P[P.length - 1][0] - P[P.length - 2][0],
                     y: 2 * P[P.length - 1][1] - P[P.length - 2][1] };
  const Q = [phantom0, ...P.map((p) => ({ x: p[0], y: p[1] })), phantomN];
  const out = [{ x: px(Q[1].x), y: px(Q[1].y), moveTo: true }];
  for (let i = 1; i < Q.length - 2; i++) {
    const P0 = Q[i - 1], P1 = Q[i], P2 = Q[i + 1], P3 = Q[i + 2];
    out.push({
      x: px(P2.x), y: px(P2.y),
      curve: { type: "cubic",
               x1: px(P1.x + (P2.x - P0.x) / 6), y1: px(P1.y + (P2.y - P0.y) / 6),
               x2: px(P2.x - (P3.x - P1.x) / 6), y2: px(P2.y - (P3.y - P1.y) / 6) },
    });
  }
  return out;
}
slide.addShape(pptx.ShapeType.custGeom, {
  x: 0, y: 0, w: 13.333, h: 7.5,           // full-slide bbox; absolute inch points
  line: { color: "000000", width: 2 },     // NO fill option -> <a:noFill/> (open stroke)
  points: catmullRomPoints(TRACE),
});

// ---- LEARNING-STEP CHAIN: 9 measured GRAY ARCS above the descent iterates -----
// ATTEMPT-8 FIX (worker w10-s027-a7-20261021T1945, 2026-10-21).
// Attempt 7 (build_attempt_7.js, render_7.png, judge_attempt_7.txt) PASSED the
// full-slide leg and the min_cluster / axis_top crop legs, but the dot_sequence
// crop judge FAILed it (crop_7_dot_sequence_judge.txt, item 1 MAJOR): the
// original's step connectors read as CURVED per-interval arrows while the render
// drew straight head-less rays. PIL-first adjudication CONFIRMED the shape claim
// and REFUTED the two other sub-claims:
//   REFUTED "absent over dot6->dot7 / dot7->dot8": probe_adj7_dotseq_output.txt
//     TEST 3 — the render carries MORE chain ink than the original in all nine
//     interval windows (dot6->dot7: 68 px vs 32; dot7->dot8: 63 vs 25;
//     dot8->dot9: 31 vs 22; dot9->yellow: 55 vs 34) and a real gray component
//     (area 12, frame (378,380)-(380,381)) sits inside the judge's cited band.
//   REFUTED "head-tipped": TEST 4 — zero solid head candidates (fill>=0.75 AND
//     area>=40) among the original's chain-window components; the 4x10 fill~0.9
//     blobs at x261 are the dashed LEADER's dashes, not arrowheads.
//   CONFIRMED "curved": a clean component census with the curve halo excluded
//     (>=6 fpx from the parabola) found NINE marks, and every one is an ARC:
//     a quadratic explains its centre-line 3-7x better than a straight line
//     (lineRMS 0.80-1.49 fpx vs quadRMS 0.08-0.43, R2 0.91-0.98), while the
//     render's own known-straight chords read lineRMS ~0.1-0.3 through the
//     identical code path. Sagitta 0.98-5.16 fpx, always bowing AWAY from the
//     parabola. Mean thickness 1.99-2.28 fpx (~2pt), NOT 1pt.
//
// MEASURED GEOMETRY (scratch/probe_adj7_*.py; reproduced below, frame px,
// 1px = 1pt): nine links, each 9-24 fpx long, that chain from (272.5,262.8)
// just outside dot 1 to (444.0,395.9) just outside the yellow minimum. Every
// link's ends sit 8-12 fpx from the ADJACENT iterate centres (disc radius 6.5),
// i.e. the trajectory grazes each disc's rim on its upper-right side and is
// separated from the next link by 1.6-10.8 fpx. That supersedes attempt-7's
// inferred "re-aim each stroke's end 2.5 fpx INTO the rim" rule (adjudication
// attempt_6's fix spec) — the banked pixel census is the authority and it says
// the links stop just OUTSIDE the discs.
//
// Attempt-7's separate "main + 0.75pt companions" inventory came from component
// censuses that split each arc with a 4-fpx exclusion around the dots/curve; the
// clean census (curve halo excluded, no dilation) shows ONE arc per inter-dot
// interval. All nine are drawn at the same measured 2pt weight.
const CHAIN_GRAY = "ACACAD";
// each link = 9 measured centre-line points (quadratic fit of the ink, sampled
// evenly along the fitted axis); drawn as a custGeom polyline, NO fill.
const CHAIN_LINKS = [
  [[272.5, 262.8], [276.3, 267.2], [279.5, 271.7], [282.2, 276.5], [284.4, 281.5],
   [286.0, 286.7], [287.2, 292.1], [287.8, 297.7], [287.8, 303.5]],   // dot1->2
  [[292.9, 310.1], [296.7, 311.6], [300.0, 313.5], [302.9, 315.8], [305.3, 318.4],
   [307.3, 321.4], [308.9, 324.7], [310.0, 328.4], [310.7, 332.4]],   // dot2->3
  [[315.5, 341.7], [318.8, 342.4], [321.8, 343.4], [324.7, 344.7], [327.2, 346.4],
   [329.6, 348.3], [331.7, 350.6], [333.5, 353.2], [335.1, 356.1]],   // dot3->4
  [[335.4, 358.2], [338.9, 357.9], [342.0, 358.0], [344.7, 358.7], [347.1, 359.8],
   [349.0, 361.5], [350.7, 363.8], [351.9, 366.5], [352.8, 369.8]],   // dot4->5
  [[354.3, 370.5], [357.4, 369.7], [360.3, 369.3], [362.9, 369.5], [365.3, 370.2],
   [367.4, 371.4], [369.3, 373.2], [371.0, 375.5], [372.4, 378.3]],   // dot5->6
  [[374.9, 381.3], [377.4, 380.7], [379.8, 380.4], [382.1, 380.5], [384.3, 380.9],
   [386.4, 381.6], [388.5, 382.7], [390.4, 384.1], [392.3, 385.9]],   // dot6->7
  [[398.0, 388.6], [399.1, 388.1], [400.2, 387.8], [401.3, 387.5], [402.4, 387.4],
   [403.6, 387.4], [404.7, 387.6], [405.9, 387.8], [407.0, 388.2]],   // dot7->8
  [[416.0, 394.1], [417.5, 393.5], [419.0, 393.0], [420.5, 392.8], [422.0, 392.7],
   [423.5, 392.8], [425.0, 393.1], [426.5, 393.5], [428.0, 394.2]],   // dot8->9
  [[429.0, 395.8], [430.9, 395.2], [432.8, 394.8], [434.7, 394.5], [436.5, 394.4],
   [438.4, 394.5], [440.3, 394.8], [442.2, 395.3], [444.0, 395.9]],   // dot9->min
];
for (const link of CHAIN_LINKS) {
  const pts = link.map((p, i) => ({ x: px(p[0]), y: px(p[1]), moveTo: i === 0 }));
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,           // full-slide bbox; absolute inch points
    line: { color: CHAIN_GRAY, width: 2 },   // measured mean thickness ~2.0 fpx
    points: pts,                             // NO fill -> <a:noFill/> (open stroke)
  });
}

// ---- descent dots: NINE blue discs d=13 at banked centers ---------------------
// w8 resumption adjudication 2026-10-20: spec pinned #0000CD but the VALIDATION
// block itself flagged the hue ("source says purple/blue, only #0000CD existed in
// the palette; #0000CD was used"). PIL ink cores of the ORIGINAL frame
// (qa/slide027/adjudication_attempt_3.md): darkest-10% core (56,31,147) #381F93,
// halo-excluded interior median (95,65,196) #5F41C4 — violet-blue, NOT medium
// blue. Two independent judges (full-slide attempt 2 + crop dot_sequence) read the
// original dots as deeper indigo/purple-blue-violet vs the render's brighter blue.
// Frame wins -> fill #5F41C4 (interior median, halo-excluded).
const BLUE = "5F41C4";
const BLUE_DOTS = [
  [262.0, 263.5], [283.0, 310.5], [306.5, 342.0], [332.0, 366.5], [354.5, 380.5],
  [374.5, 390.0], [392.0, 396.5], [411.0, 403.5], [426.5, 403.5],
];
for (const [cx, cy] of BLUE_DOTS) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - 6.5), y: px(cy - 6.5), w: px(13), h: px(13),
    fill: { color: BLUE }, line: { color: BLUE, width: 0 },
  });
}
// ---- yellow minimum dot: d=12.5 at (444.5, 407) ---------------------------------
slide.addShape(pptx.ShapeType.ellipse, {
  x: px(444.5 - 6.25), y: px(407 - 6.25), w: px(12.5), h: px(12.5),
  fill: { color: "FFFF00" }, line: { color: "FFFF00", width: 0 },
});

// ---- text labels (Arial regular, black; per-label width-fit sizes) --------------
// LO baseline model (Liberation Sans hhea via PIL: extent 1.138em, ascent 0.913em):
// baseline = boxTop + (L - 1.138*S)/2 + 0.913*S, L = 1.2*S  (+ DY correction).
const L_ASC = 0.913, L_EXT = 1.138;
function addLabel(t, S, base, cx, inkW, dy) {
  const L = 1.2 * S;
  slide.addText(t, {
    x: px(cx - inkW * 1.25 / 2),
    y: px(base - ((L - L_EXT * S) / 2 + L_ASC * S) + (dy || 0)),
    w: px(inkW * 1.25), h: px(34),
    align: "center", valign: "top", margin: 0,
    fontFace: "Arial", fontSize: S, color: "000000",
    lineSpacing: L,
  });
}
// (text, size pt, baseline px, ink-center-x px, ink advance px, dy correction)
addLabel("Cost",           18.88, 189.0, 219.0, 39, 0);  // rows 176..189, x 200..238
addLabel("Learning step",  17.62, 284.1, 350.5, 107, 0); // rows 272..289, x 297..404
addLabel("Minimum",        16.88, 375.6, 462.5, 69, 0);  // rows 364..376, x 428..497
addLabel("Random",         17.12, 455.8, 262.5, 65, 0);  // rows 444..457, x 230..295
addLabel("initial value",  17.62, 478.0, 262.5, 87, 0);  // rows 466..479, x 219..306

// ---- theta glyphs (Arial ~22pt, height-fit) --------------------------------------
addLabel("\u03b8", 22.0, 443.4, 703.0, 12.3, 0);   // axis label rows 427..444, x 697..709
addLabel("\u03b8", 22.0, 504.0, 444.0, 12.3, 0);   // theta-hat body rows 488..504, x 439..449

// ---- faint gray '+' (w4 closed-loop discovery, 2026-10-20) -----------------------
// The dossier REFUTED the spec's '+' with a BLACK-ink scan — but a full-frame
// faint-gray scan (neutral, lum 110..215) finds exactly ONE clean glyph that is not
// a JPEG halo of dark ink: a 11x10 plus at rows 446..455, cols 406..416, directly
// below dot 8 (x=411) and 13px below the x-axis, core RGB(140,140,140) = 8C8C8C
// (its darkest pixel is lum 140 — the black labels' cores are lum 0..16, so this is a
// genuinely LIGHT-GRAY mark, not a halo). Frame wins -> draw it, gray, at the measured
// ink bbox. Drawn as two exact rects (vertical bar cols 410..411 rows 446..455,
// horizontal bar cols 406..416 rows 450..451) so the geometry is measured, not guessed.
const PLUS = "8C8C8C";
slide.addShape(pptx.ShapeType.rect, {
  x: px(410), y: px(446), w: px(2), h: px(10),
  fill: { color: PLUS }, line: { color: PLUS, width: 0 },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(406), y: px(450), w: px(11), h: px(2),
  fill: { color: PLUS }, line: { color: PLUS, width: 0 },
});

// theta-hat caret: open 2-stroke custGeom at measured ink bbox x440..448, rows 480..484
slide.addShape(pptx.ShapeType.custGeom, {
  x: 0, y: 0, w: 13.333, h: 7.5,
  line: { color: "000000", width: 1.5 },   // NO fill -> open stroke
  points: [
    { x: px(440), y: px(484.5), moveTo: true },
    { x: px(444), y: px(480) },
    { x: px(448), y: px(484.5) },
  ],
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
