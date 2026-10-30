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
// filled arrowhead helper: closed custGeom triangle in frame px.
// col defaults to black (the two axis heads below); attempt 9 passes CHAIN_GRAY for
// the learning-step arrowheads (founder finding C). Optional arg -- the existing two
// axis calls keep their exact attempt-8 behaviour.
function triShape(pts, col) {
  const C = col || "000000";
  const path = pts.map((p, i) =>
    i === 0 ? { x: px(p[0]), y: px(p[1]), moveTo: true } : { x: px(p[0]), y: px(p[1]) });
  path.push({ close: true });
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,           // full-slide bbox; absolute inch points
    fill: { color: C }, line: { color: C, width: 0 },
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

// ---- parabola: ONE SMOOTH analytic quadratic, densely sampled (founder finding A) -
// ATTEMPT-9 FIX (worker w11-s027-a9-20261021, 2026-10-21).
// Founder finding A (BINDING, overrides every judge PASS and every prior PIL
// refutation on this slide): the black cost curve read as "noticeably
// jagged/rippled rather than a smooth mathematical curve"; the founder asks that it
// be identified as a quadratic curve and redrawn as ONE SMOOTH mathematical curve --
// a quadratic cost function of the iterate position, with dense sampling so the
// rendered stroke carries no visible ripple or facet.
//
// ROOT CAUSE of attempt 8's ripple: the 54-point hand-trace (TRACE, now removed) was
// interpolated with a Catmull-Rom cubic chain. The trace's own measurement noise
// (+/-2-3 fpx per column-centroid) became local overshoot in the stroke -- the
// banked render_8 ripple measurement was a second-difference max of 27.5 fpx, i.e. a
// visible sawtooth on the arms. Interpolating noisy samples CANNOT be smooth; only a
// fitted analytic function can.
//
// MEASURED (scratch/probe_adj9_geometry.py; banked output
// recreated_pptx/qa/slide027/probe_adj9_geometry_output.txt). Orthogonal-distance
// (total least squares) fit of the original's black-ink pixels -- lum<200, the
// violet/yellow discs dilated 5 px and the label boxes excluded, window
// x246..700 / y200..428, 1748 ink px, weights 1/lum^2 (the unbiased estimator for a
// steep stroke, where per-column centroid tracing biases):
//     free quadratic      a=-0.00421895 vertex (450.414,414.429) RMS 6.641
//     vertex-y locked     a=-0.00395282 vertex (450.410,407.250) RMS 6.924
// SELECTED the vertex-y-locked fit: it costs only 0.28 fpx of RMS and puts the
// curve's bottom exactly on the yellow MINIMUM dot (444.49,407.25) -- i.e. the curve
// is a quadratic cost function whose minimum IS the yellow iterate, which is the
// identification the founder asked for.
//   y = -0.00395282 * (x - 450.41)^2 + 407.25
//
// HONESTY OF THE fit (recorded, not hidden): the original's two arms are steeper than
// any single full-extent quadratic -- a quartic fits the same ink at RMS 3.76 vs the
// quadratic's 6.92 -- so the drawn quadratic deviates from the original's traced
// centre-line by max 13.6 fpx (3.4% of the 400 fpx span), concentrated in the arms,
// while the vertex region matches to 0.2 fpx. Drawing the quadratic anyway is the
// founder's explicit model choice (finding A names a quadratic); the price is that
// residual, and it is measured and banked above.
//
// EXTENT: x=241..660 is exactly where the quadratic sweeps y=233.6..407.25 -- the
// same vertical envelope as the original's ink (caps ~y230.3 / y243.5). Drawing only
// the ink's x-span (253..643) would clip both arms ~20 fpx short of the original.
//
// SMOOTHNESS (the founder's actual complaint): 420 samples at 1 fpx. A quadratic's
// second difference is the constant 2*a = -0.0079 fpx -- mathematically ZERO ripple,
// no sawtooth, no facet (the 1-fpx chord facets are 0.002 fpx deep). The render's
// centre-line is re-traced and its second difference measured after the build to
// confirm (see qa/slide027/ selfcheck + adjudication_attempt_9.md).
const CURVE = { a: -0.00395282, h: 450.41, k: 407.25, x0: 241, x1: 660 };
{
  const pts = [];
  for (let x = CURVE.x0; x <= CURVE.x1; x++) {
    pts.push({ x: px(x), y: px(CURVE.a * (x - CURVE.h) ** 2 + CURVE.k),
               moveTo: x === CURVE.x0 });
  }
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,           // full-slide bbox; absolute inch points
    line: { color: "000000", width: 2 },     // NO fill option -> <a:noFill/> (open stroke)
    points: pts,
  });
}

// ============================================================================
// ATTEMPT 9 (worker w11-s027-a9-20261021T2100, 2026-10-21) — FOUNDER FINDINGS B
// & C, BINDING. They override every judge PASS and every PIL census banked for
// attempt 8 (adjudications 3/6/8, probe_adj7_*), all of which stay banked.
//
//   FINDING B — "the grey dashed step connectors [are] misaligned arc
//   connectors: some overlap awkwardly or float slightly off from the centers
//   of the purple data points." Fix spec: EACH connector runs between
//   CONSECUTIVE PURPLE DOT CENTRES — measure the 9 dot centres in the original
//   frame, put the render's dots AT those centres, and start/end every
//   connector ON a dot centre. No floating, no overlap.
//
//   FINDING C — those connectors are NOT "headless plain arrows"; they are
//   "ARROWS WITH ARROWHEADS (arc arrows pointing along the descent direction
//   between the iterates)". Fix spec: draw REAL arrowheads at the terminating
//   end of each connector, with the head geometry measured from the original
//   frame (size, angle, colour) — not guessed.
//
// The ATTEMPT-8 FIX comment block immediately below is KEPT VERBATIM as
// superseded lineage (it is the banked record of what attempt 8 drew and why);
// its geometry — polyline links that stop 8-12 fpx OUTSIDE the disc rims, with
// no arrowheads — is exactly the float/overlap the founder saw. Full provenance
// is preserved at qa/slide027/build_attempt_8.js, adjudication_attempt_8.md and
// probe_adj7_*_output.txt; the PIL "no arrowheads" census and founder finding C
// are reconciled in qa/slide027/adjudication_attempt_9.md.
// ============================================================================
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
// ---- ATTEMPT-9 CHAIN GEOMETRY (founder findings B & C) ----------------------
// MEASURED INPUT: scratch/probe_adj9_geometry.py, banked at
// qa/slide027/probe_adj9_geometry_output.txt (+ machine-readable
// scratch/adj9_geometry.json). All numbers are ORIGINAL frame px (960x540,
// 1px = 1pt = 1/72in).
//   (1) The nine violet dot CENTRES, halo-excluded disc centroids of the original
//       (the JPEG ring around each violet disc is removed by dilating the disc
//       masks 5-7 fpx before taking the centroid — without that the ring drags
//       the estimate ~1 fpx up-left). They are repinned in BLUE_DOTS below.
//   (2) Nine cubic-Bezier arcs P0 -> C -> P2 fitted to the original's visible
//       arc-ink, with the control offset solved by w = 2s(1-s) weighted
//       projection of the ink offset onto the dot-centre chord. The ink always
//       bows AWAY from the black parabola (offset -1.66..-13.35 fpx at s=0.5),
//       so C sits on the away side. VIS-ink RMS 0.92-4.98 fpx; the arcs never
//       cross the parabola (0/60 crossing tests).
//   (3) Arrowheads (finding C): length 5.4 fpx, half-width 2.7 fpx, filled grey,
//       the OPENING tip of the triangle pointing along the arc's terminal
//       direction at the receiving disc. The tip sits 6.31-6.58 fpx from the
//       target dot centre, i.e. essentially ON the disc rim (radius 6.5) — drawn
//       as an explicit closed custGeom (see triShape), never as a line
//       endArrowType, per the house arrowhead law.
// DRAWN ORDER: shaft arcs first, then the head triangles, then the discs — so
// each shaft's overrun past its head (into the receiving dot centre) is covered
// by its own head and then by that dot. Nothing floats, nothing overlaps.
const CHAIN_GRAY = "ACACAD";   // measured chain core-35% (162,162,161) #A1A2A0,
                               // darkest-10% (155,155,154); attempt-8 value
                               // stays inside the measured band.
// [P0 = source dot centre, C = quadratic control point (already the offset
//  control, converted to cubic in the loop), P2 = target dot centre]
const CHAIN_ARCS = [
  [[263.12, 263.41], [298.32, 275.63], [283.64, 309.88]],   // dot1->2
  [[283.64, 309.88], [316.79, 310.17], [306.85, 341.79]],   // dot2->3
  [[306.85, 341.79], [336.00, 337.17], [331.65, 366.36]],   // dot3->4
  [[331.65, 366.36], [358.14, 350.23], [354.26, 381.00]],   // dot4->5
  [[354.26, 381.00], [372.23, 368.79], [373.91, 390.45]],   // dot5->6
  [[373.91, 390.45], [391.42, 369.30], [392.40, 396.74]],   // dot6->7
  [[392.40, 396.74], [408.35, 374.43], [410.77, 401.75]],   // dot7->8
  [[410.77, 401.75], [425.41, 378.93], [428.21, 405.90]],   // dot8->9
  [[428.21, 405.90], [438.78, 377.28], [444.49, 407.25]],   // dot9->minimum
];
// [tip, base corner, base corner] — length 5.4 fpx, half-width 2.7 fpx each.
const CHAIN_HEADS = [
  [[285.92, 303.76], [284.96, 297.80], [290.11, 299.42]],
  [[308.47, 335.44], [306.83, 329.63], [312.13, 330.64]],
  [[332.21, 359.84], [329.58, 354.41], [334.98, 354.48]],
  [[354.75, 374.49], [352.13, 369.05], [357.53, 369.13]],
  [[372.85, 384.00], [368.78, 379.54], [373.98, 378.07]],
  [[391.84, 390.26], [388.36, 385.33], [393.69, 384.51]],
  [[409.86, 395.24], [406.12, 390.50], [411.41, 389.40]],
  [[427.21, 399.40], [423.41, 394.71], [428.69, 393.55]],
  [[443.10, 401.09], [439.08, 396.58], [444.29, 395.17]],
];
for (const [P0, C, P2] of CHAIN_ARCS) {
  // quadratic control C -> the two cubic control points (standard q->cubic
  // conversion, exact: (1-t)PO + 2t(1-t)C + t^2 P2)
  const x1 = P0[0] + (2 / 3) * (C[0] - P0[0]), y1 = P0[1] + (2 / 3) * (C[1] - P0[1]);
  const x2 = P2[0] + (2 / 3) * (C[0] - P2[0]), y2 = P2[1] + (2 / 3) * (C[1] - P2[1]);
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,           // full-slide bbox; absolute inch points
    line: { color: CHAIN_GRAY, width: 2 },   // measured mean thickness ~2.0 fpx
    points: [                                 // NO fill -> open stroked arc
      { x: px(P0[0]), y: px(P0[1]), moveTo: true },
      { x: px(P2[0]), y: px(P2[1]),
        curve: { type: "cubic", x1: px(x1), y1: px(y1), x2: px(x2), y2: px(y2) } },
    ],
  });
}
for (const h of CHAIN_HEADS) triShape(h, CHAIN_GRAY);   // founder finding C


// ---- descent dots: NINE violet discs d=13 at the ORIGINAL's measured centres --
// w8 resumption adjudication 2026-10-20: spec pinned #0000CD but the VALIDATION
// block itself flagged the hue ("source says purple/blue, only #0000CD existed in
// the palette; #0000CD was used"). PIL ink cores of the ORIGINAL frame
// (qa/slide027/adjudication_attempt_3.md): darkest-10% core (56,31,147) #381F93,
// halo-excluded interior median (95,65,196) #5F41C4 — violet-blue, NOT medium
// blue. Two independent judges (full-slide attempt 2 + crop dot_sequence) read the
// original dots as deeper indigo/purple-blue-violet vs the render's brighter blue.
// Frame wins -> fill #5F41C4 (interior median, halo-excluded).
//
// ATTEMPT-9 REPIN (founder finding B): the CENTRES below are no longer the
// attempt-8 rounded guesses (262.0,263.5) ... (426.5,403.5), which sit up to 2.9
// fpx from the original's disc centroids. They are the halo-excluded centroids
// measured in probe_adj9_geometry (disc masks dilated 5-7 fpx against the JPEG
// ring), and the CHAIN_ARCS / CHAIN_HEADS above are anchored on exactly these
// numbers — so every connector starts and ends ON a dot centre. Attempt 8's dots
// cannot be reached from its link endpoints, which is the "float / overlap" the
// founder reported.
const BLUE = "5F41C4";
const BLUE_DOTS = [
  [263.12, 263.41], [283.64, 309.88], [306.85, 341.79], [331.65, 366.36],
  [354.26, 381.00], [373.91, 390.45], [392.40, 396.74], [410.77, 401.75],
  [428.21, 405.90],
];
for (const [cx, cy] of BLUE_DOTS) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - 6.5), y: px(cy - 6.5), w: px(13), h: px(13),
    fill: { color: BLUE }, line: { color: BLUE, width: 0 },
  });
}
// ---- yellow minimum dot: d=12.5 at the measured centre (444.49, 407.25) --------
// founder finding B also pins this one: CHAIN_ARCS[8] terminates exactly here
// (attempt 8 used the rounded (444.5, 407) while its last link ended at
// (444.0, 395.9) — 11 fpx short of the dot centre).
slide.addShape(pptx.ShapeType.ellipse, {
  x: px(444.49 - 6.25), y: px(407.25 - 6.25), w: px(12.5), h: px(12.5),
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
