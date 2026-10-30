// Build: slide 042 — "Iteration 1" (Perceptron gradient-descent worked example)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GROUND TRUTH: unique_slides/slide_042.jpg (960x540, 1px = 1pt = 1/72in).
// Content spec: analysis/slide_042_final.json (verbatim_text.equations —
// ten equations: five d(x_i)=… and five distinct W=… result equations).
//
// ATTEMPT 24 — over attempt 23 (adjudication_attempt23.md + read-legs
// read_{dx1,initialw,lmbox}_judge.txt; geometry PIL-arbitrated in
// scratch/tmp/s6_042_pil24.py):
//   1. d(x1) box added (STACK_BOXES/BAND_A/VSPAN/wGeo prepend): white box
//      y142..195, mat (1,1,1) RED with red curved parens at superscript height
//      (tinted P3 PNGs), green d-vec (4,-2,-2), dEq 0, red => Update Weight,
//      update eq W = (4,-2,-2) + 2 * (1,1,1) = (6,0,0) green + red <= (anchors
//      from frame ink clusters x614..790)
//   2. Initial W -> 3 components 4/-2/-2 (rows y63/79/95); right paren pair
//      moved x349->x353; W bold-italic-underlined in "Initial W ="
//   3. matrix bars hug digits in ALL boxes: bars a-17..a-2 (was a+1..a+15)
//   4. LM caption -> "Ugmented Vectors ( from Top )" (read_lmbox, char-exact)
//   5. LM grid -> 3 digit rows y166/184/199 (values 111111/121566/112456);
//      the frame's 4th ink band y215..222 is the PAREN BOTTOM HOOKS, not a
//      4th digit row (PIL: hook clusters land exactly on paren x pairs) —
//      6 paren pairs (93,107)..(203,216) span y166..222
//   6. legend left section: C1 RED at x239 (PIL red ink; the old no-red
//      reading scanned x257+ and missed the glyph), positive ends x302,
//      C2 x312..319, negative from x322
//   7. W̲ bold+underline on the two update rows' "W =" labels
//
// ATTEMPT 18 — over attempt 17 (adjudication_17.md):
//   1. LM_BANDS[3] [1,2,1,5,6,6] -> [1,1,2,5,6,6] (frame band4 cols 2/3 read 1,2)
//   2. txtsub() subscript runs on 17 tokens (041-certified pattern): TL headers
//      x1..x6, TL class row, legend C1/C2, LM class row, Z1 Z1 Z1
// ATTEMPT 17 — colour corrections over attempt 16 (channel-order measured):
//   the frame's table headers are BLACK where the build drew them blue. The test
//   distinguishes them unambiguously: on a JPEG where blue ink IS detectable
//   (the LM caption's darkest px carry b-r = +45..+77), the TL x1..x6 header's
//   12 darkest px all carry b-r = -19..-20 and 0 px pass b>r+25 & b>120.
//   Same signature as the check-classes header (b-r = -19..-20), already fixed.
//   1. BAND_A/BAND_B re-derived from the frame's own ink bands. Attempt 11's bands
//      were calibrated for TEXT boxes (LibreOffice centres a h=14 text box's ink
//      ~6px ABOVE the box top) but applied the same +8 shift to the IMAGES, which
//      place their ink at the image top. Two hard defects followed:
//        - box1's W equation image sat at y258..272, crossing box1's bottom border
//          (y263) and spilling into the y264..272 inter-box gap that the frame keeps
//          INK-FREE (0 ink px there on the frame)
//        - box4's W equation image sat at y420..434, ABOVE box4's d(x4) line
//          (BAND_B[3]=420 < BAND_A[3]=434) — inverted order and overlapping "= 6"
//   2. matrix row pitch 11px -> 7px: the frame's per-box 2-row d(x_i) matrix fits in a
//      12-13px line, so its rows sit ~6.5px apart, not 11px
//
// Frame-measured line bands (frame px), ink spans:
//   box1 142..195  lineA 164..176 (full update line present)
//   box2 214..262  lineA 231..242  (no other box draws a W-update
//   box3 273..328  lineA 294..306   equation line; box4 additionally
//   box4 340..394  lineA 360..372   carries the full update equation)
//   box5 406..459  lineA 426..437
//   box6 472..527  lineA 492..503
//
// Equation PNGs: build/render_stackeq_042.py (extends the certified
// build/render_stackeq.py with a 2-D matrix segment), 600dpi transparent PNG,
// embedded at exact px/600 size per the deck's equation law.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_042_recreated.pptx");
const ASSETS = path.resolve(__dirname, "assets");
const EQ = require(path.resolve(ASSETS, "eq_index_042.json"));

const px = (v) => v / 72; // frame px -> inches

const RED = "FF0000";
const BLUE = "0000FF";
const BLACK = "000000";
const GREEN = "008000";
const WHITE = "FFFFFF";
const CREAM = "FEFFE8";     // frame-measured interior of the top-left box
const PANEL = "E9E9E7";
const FONT = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

function txt(text, x, y, w, h, opts = {}) {
  slide.addText(text, Object.assign({
    x: px(x), y: px(y), w: px(w), h: px(h),
    fontFace: FONT, margin: 0, isTextBox: true,
  }, opts));
}

// base+subscript run (041-certified pattern) for C1/C2/Z1/x1..x6 tokens
function txtsub(base, sub, x, y, w, h, opts = {}) {
  const subSize = Math.round(((opts.fontSize || 10) * 0.7) * 10) / 10;
  slide.addText([
    { text: base },
    { text: sub, options: { subscript: true, fontSize: subSize } },
  ], Object.assign({
    x: px(x), y: px(y), w: px(w), h: px(h),
    fontFace: FONT, margin: 0, isTextBox: true,
  }, opts));
}

function vecCol(digits, cx, yTop, size, color, bold) {
  const h = size * 1.18;
  digits.forEach((d, i) => {
    txt(String(d), cx - size, yTop + i * h, size * 2, h, {
      fontSize: size, color, bold, align: "center", valign: "middle",
    });
  });
}

// embed an equation PNG with its top edge at frame y (baseline lands at
// y + baseline_frac*h, matching the frame's line band)
function eqImage(tag, x, topY) {
  const e = EQ.find((q) => q.tag === tag);
  if (!e) throw new Error("no equation sidecar for " + tag);
  const hPx = e.h_in * 72;
  slide.addImage({
    path: path.join(ASSETS, e.image),
    x: px(x), y: px(topY), w: e.w_in, h: e.h_in,
  });
  return topY + hPx;
}

// ---- house chrome (deck 03 values) -----------------------------------------
drawHouseChrome(pptx, slide, { numeral: 42 });

// ---------------------------------------------------------------------------
// white content areas (frame shows white boxes on the gray panel)
// ---------------------------------------------------------------------------
// top-left grouping box: CREAM interior with the frame's blue border
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(653), h: px(77),
  fill: { color: CREAM }, line: { color: BLUE, width: 1 },
});

// right computation stack: five white boxes with a thin gray border
// (frame-measured: border x273..853 verticals at x274 / x852-853,
//  colour ~(190,196,196), 1px; box tops y217/273/340/406/472)
const STACK_BOXES = [
  [142, 195], [214, 262], [273, 328], [340, 394], [406, 459], [472, 527],
];
STACK_BOXES.forEach(([y0, y1]) => {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(273), y: px(y0), w: px(581), h: px(y1 - y0 + 1),
    fill: { color: WHITE }, line: { color: "BEBEBE", width: 1 },
  });
});

// ---------------------------------------------------------------------------
// 1. TOP-LEFT vector table  (inside the cream box, x68..720 y54..130)
// ---------------------------------------------------------------------------
[95, 117, 139, 161, 184, 206].forEach((cx, i) => {
  // the frame's x1..x6 header ink is BLACK, not blue: the 12 darkest px in
  // y64..73 x86..216 all have b-r = -19..-20 (blue is the LOWEST channel),
  // and 0 px pass a blue test (b>r+25 & b>120). The same test on the LM caption
  // gives b-r = +45..+77, so blue ink IS detectable in this JPEG — the TL header
  // simply is not blue.
  txtsub("x", String(i + 1), cx - 8, 62, 16, 12, {
    fontSize: 10, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});

const TL_COLS = [[1, 1], [2, 1], [1, 2], [5, 4], [6, 5], [6, 6]];
TL_COLS.forEach((v, i) => {
  const cx = [95, 117, 139, 161, 184, 206][i];
  vecCol(v, cx, 78, 11, BLACK, true);
});

[["C1", 95], ["C1", 117], ["C1", 139], ["C2", 161], ["C2", 184], ["C2", 206]]
  .forEach(([lab, cx]) => {
    txtsub(lab[0], lab[1], cx - 8, 109, 16, 15, {
      fontSize: 10, color: lab === "C1" ? RED : BLUE, bold: true,
      align: "center", valign: "middle",
    });
  });

// red ⇒ at the right end of the class row (x239..253)
txt("\u21D2", 239, 109, 15, 15, {
  fontSize: 12, color: RED, align: "center", valign: "middle",
});

// ---------------------------------------------------------------------------
// 2. TOP-CENTRE: Initial W = (4/-2) matrix, then red italic Step η = 2
// ---------------------------------------------------------------------------
// "Initial W =": the frame's W is bold-italic-underlined (read_initialw)
slide.addText([
  { text: "Initial " },
  { text: "W", options: { bold: true, italic: true, underline: true } },
  { text: " =" },
], { x: px(262), y: px(71), w: px(70), h: px(18), fontSize: 14, color: BLACK,
  valign: "middle", fontFace: FONT, margin: 0 });
// the 3x1 matrix parens: a 34pt glyph paren renders far too tall in pptxgenjs
// (measured y202..289 vs the frame's y63..102), so draw them as thin line shapes
// with top/bottom hooks, exactly like the LM table's parens.
[[330, 337], [353, 360]].forEach(([xl, xr]) => {
  [xl, xr].forEach((x) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(63), w: 0, h: px(39),
      line: { color: BLACK, width: 1 },
    });
  });
  [[63, xl + 1], [102, xr - 7]].forEach(([y, hx]) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(hx), y: px(y), w: px(6), h: 0,
      line: { color: BLACK, width: 1 },
    });
  });
});
txt("4", 341, 63, 14, 14, { fontSize: 13, color: BLACK, align: "center", valign: "middle" });
txt("-2", 339, 79, 18, 14, { fontSize: 13, color: BLACK, align: "center", valign: "middle" });
txt("-2", 339, 91, 18, 14, { fontSize: 13, color: BLACK, align: "center", valign: "middle" });

txt("Step \u03B7 = 2", 364, 63, 74, 19, {
  fontSize: 15, color: RED, italic: true, valign: "middle",
});

// ---------------------------------------------------------------------------
// 3. TOP-RIGHT check-classes table + the colour legend sentence
// ---------------------------------------------------------------------------
txt("Check classes of", 496, 74, 100, 20, {
  fontSize: 12, color: BLACK, valign: "middle",
});
[601, 625, 645].forEach((cx, i) => {
  // the frame prints "Z1" THREE times over this block (glyphs identical, measured
  // x-masks dot-for-dot) and the ink is DARK (darkest px rgb 31,33,11 — b is the
  // lowest channel, so not blue; analysis colors for this block list only #FFFFFF
  // and #000000), so the headers are black, not the TL table's blue.
  txtsub("Z", "1", cx - 4, 62, 16, 13, {
    fontSize: 10, color: BLACK, bold: true, align: "center", valign: "middle",
  });
});
[[0, 0], [7, 6], [3, 2]].forEach((v, i) => {
  vecCol(v, [601, 625, 645][i], 82, 11, BLACK, true);
  // bowed paren PNGs (041-cert P3 pattern, 30pt ink) spanning both digits —
  // thin line pairs read as square brackets in the zoomed crop judge
  const cx = [601, 625, 645][i];
  const P = path.join(ASSETS, "parens042");
  [[`${P}/paren_z_lp.png`, `${P}/paren_z_lp.json`, cx - 9], [`${P}/paren_z_rp.png`, `${P}/paren_z_rp.json`, cx + 9]]
    .forEach(([img, meta, tipX]) => {
      const j = JSON.parse(fs.readFileSync(meta, "utf8"));
      const ptPerPx = j.pt_per_px;
      slide.addImage({
        path: img,
        x: px(tipX - j.ink_right_px * ptPerPx),
        y: px(80 - j.ink_top_px * ptPerPx),
        w: j.px_w / 600,
        h: j.px_h / 600,
      });
    });
});

// legend sentence — ORIG ink clusters (PIL): C1(red) 239..253, "positive," ends
// 302, C2(blue) 312..319, "negative," 322..378, Zero 396..422, is-unaccepted 431..508
const LEGEND = [
  { sub: ["C", "1"], c: RED, x: 236 },
  { t: " positive, ", c: BLACK, x: 252 },
  { sub: ["C", "2"], c: BLUE, x: 309 },
  { t: " negative, ", c: BLACK, x: 317 },
  { t: "Zero", c: GREEN, x: 394 },
  { t: " is unaccepted", c: BLACK, x: 428 },
];
LEGEND.forEach((s) => {
  if (s.sub) {
    txtsub(s.sub[0], s.sub[1], s.x, 107, 15, 17, {
      fontSize: 13, color: s.c, valign: "middle", wrap: false,
    });
  } else {
    txt(s.t, s.x, 108, 90, 16, { fontSize: 13, color: s.c, valign: "middle", wrap: false });
  }
});

// ---------------------------------------------------------------------------
// 4. LEFT-MIDDLE "Upgraded Vectors (From Top)"
// ---------------------------------------------------------------------------
txt("Ugmented Vectors ( from Top )", 79, 150, 168, 13, {
  fontSize: 11, color: BLUE, bold: true, valign: "middle",
});

const LM_CENTRES = [99, 121, 143, 166, 188, 211];
const LM_BANDS = [
  { y: 164, vals: [1, 1, 1, 1, 1, 1] },
  { y: 182, vals: [1, 2, 1, 5, 6, 6] },
  { y: 197, vals: [1, 1, 2, 4, 5, 6] },
];
LM_BANDS.forEach((band) => {
  LM_CENTRES.forEach((cx, ci) => {
    txt(String(band.vals[ci]), cx - 5, band.y, 11, 11, {
      fontSize: 10, color: BLACK, align: "center", valign: "middle",
    });
  });
});
// the frame shows THIN 1px strokes, not glyph parens; 6 pairs spanning the
// 3 digit rows, bottom hooks at y222 (the frame's 4th ink band y215..222 IS
// these hooks — PIL hook clusters land on the pair x positions)
const LM_PAREN_PAIRS = [[93, 107], [115, 128], [137, 150], [159, 173], [182, 196], [205, 218]];
LM_PAREN_PAIRS.forEach(([xl, xr]) => {
  [xl, xr].forEach((x) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(166), w: 0, h: px(56),
      line: { color: BLACK, width: 0.75 },
    });
  });
  [[166, xl + 1], [222, xr - 7]].forEach(([y, hx]) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(hx), y: px(y), w: px(6), h: 0,
      line: { color: BLACK, width: 0.75 },
    });
  });
});

[["C1", 95], ["C1", 117], ["C1", 139], ["C2", 161], ["C2", 184], ["C2", 206]]
  .forEach(([lab, cx]) => {
    txtsub(lab[0], lab[1], cx - 9, 230, 18, 14, {
      fontSize: 10, color: lab === "C1" ? RED : BLUE, bold: true,
      align: "center", valign: "middle",
    });
  });

// ---------------------------------------------------------------------------
// 5. ITERATION BADGE (red rect x84..214 y277..305, white bold text)
// ---------------------------------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: px(84), y: px(277), w: px(131), h: px(29),
  fill: { color: RED },
});
txt("Iteration 1", 98, 283, 104, 17, {
  fontSize: 15, color: WHITE, bold: true, align: "center", valign: "middle",
});

// ---------------------------------------------------------------------------
// 6. RIGHT COMPUTATION STACK — 5 white boxes, two lines each
// ---------------------------------------------------------------------------
// 6. RIGHT COMPUTATION STACK — 5 white boxes (frame-verified structure,
// S20d ground-truth read + PIL arbitration, adjudication of the crop-18 FAIL)
//
// Each box, one line vertically centred (tall elements span the box):
//   d(x_i) = | 1 xi1 xi2 | (green 3-row d-result vector) = <value>  ⇒ <action>
//            W = (black 3-row W vector)
// box3 additionally continues:  - 2 * (1,5,4) = (4,-10,-8)  with a red ⇐ far right
// Matrices are SINGLE-ROW [1, xi1, xi2]: box i's digits = 1 + TL column (i+1);
// red digits for x2/x3, blue for x4/x5/x6 (PIL chroma: box1 r=3/9/10, boxes 3-5 blue).
// Subscripts run x2..x6 (041 covered x1; sequence arithmetic matches TL_COLS).
// The analysis JSON's five wide W-update equations are a model extrapolation the
// frame does not draw (only box3 carries one) — recorded in worker_report.md.

const GREENV = "00A050";  // frame-measured green vector colour

const ROWS = [
  { sub: "1", mat: ["1", "1", "1"], matColor: RED, matParens: true,
    gVals: [4, -2, -2], dEq: "0", action: "Update Weight",
    arrowColor: RED, arrowX: 486, actX: 506, eqX: 411, wX: 614, wUnderline: true,
    updateEq: { op: "+ 2 *", opColor: RED, opX: 676,
      incVals: [1, 1, 1], incX: [708, 725], eqX: 728,
      resVals: [6, 0, 0], resX: [740, 758], resColor: GREENV, backX: 774 } },
  { sub: "2", mat: ["1", "2", "1"], matColor: RED,
    gVals: [6, 0, 0], dEq: "6", action: "Keep same Weight",
    arrowColor: BLACK, wX: 687, eqX: 400 },
  { sub: "3", mat: ["1", "1", "2"], matColor: RED,
    gVals: [6, 0, 0], dEq: "6", action: "Keep same Weight",
    arrowColor: BLACK, wX: 687, eqX: 400 },
  { sub: "4", mat: ["1", "5", "4"], matColor: BLUE,
    gVals: [6, 0, 0], dEq: "6", action: "Update Weight",
    arrowColor: RED, wX: 609, eqX: 400, wUnderline: true,
    updateEq: { op: "- 2 *", opColor: BLUE, opX: 655,
      incVals: [1, 5, 4], incX: [687, 702], eqX: 708,
      resVals: [4, -10, -8], resX: [717, 751], resColor: GREENV, backX: 771 } },
  { sub: "5", mat: ["1", "6", "5"], matColor: BLUE,
    gVals: [4, -10, -8], dEq: "-96", action: "Keep same Weight",
    arrowColor: BLACK, wX: 720, eqX: 417 },
  { sub: "6", mat: ["1", "6", "6"], matColor: BLUE,
    gVals: [4, -10, -8], dEq: "-104", action: "Keep same Weight",
    arrowColor: BLACK, wX: 725, eqX: 417 },
];

// frame-measured ink anchors (frame px)
const LBL_X = 283;       // "d(x_i) =" label left
const BAR1_X = 327;      // opening | bar
const MAT_CX = [337, 354.5, 372];  // matrix digit centres (pitch ~17.5)
const BAR2_X = 379;      // closing | bar
const EQ_XS = null;      // per-row eqX in ROWS
const ARROW_X = 473;     // ⇒
const ACT_X = 495;       // action text left edge (ink x495..625)

// per-box tall-vector geometry: y-span and digit row tops (PIL-measured)
const VSPAN = [
  { y0: 152, y1: 192, rows: [152, 168, 183] },
  { y0: 218, y1: 258, rows: [218, 234, 249] },
  { y0: 281, y1: 320, rows: [281, 297, 312] },
  { y0: 347, y1: 386, rows: [348, 363, 378] },
  { y0: 410, y1: 454, rows: [413, 429, 444] },
  { y0: 476, y1: 522, rows: [479, 495, 510] },
];

// lineA text band tops (ink starts ~2px below box top)
const BAND_A = [166, 232, 295, 361, 427, 493];

// draw a tall parenthesized 3-row column vector
function tallVec(xl, xr, y0, y1, rows, vals, color) {
  [xl, xr].forEach((x) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(x), y: px(y0), w: 0, h: px(y1 - y0),
      line: { color, width: 1 },
    });
  });
  [[y0, xl + 1], [y1, xr - 7]].forEach(([y, hx]) => {
    slide.addShape(pptx.ShapeType.line, {
      x: px(hx), y: px(y), w: px(6), h: 0,
      line: { color, width: 1 },
    });
  });
  vals.forEach((d, ri) => {
    txt(String(d), xl + 2, rows[ri] - 2, xr - xl - 4, 12, {
      fontSize: 10, color, align: "center", valign: "middle",
    });
  });
}

ROWS.forEach((r, i) => {
  const a = BAND_A[i];
  const v = VSPAN[i];

  // d(x_i) = — one text run (frame shows a single unbroken label)
  slide.addText(
    [
      { text: "d(x", options: {} },
      { text: r.sub, options: { subscript: true, fontSize: 9 } },
      { text: ") =", options: {} },
    ],
    { x: px(LBL_X), y: px(a - 3), w: px(34), h: px(14), fontSize: 13,
      color: BLACK, valign: "middle", wrap: false }
  );

  // | 1 xi1 xi2 |  — box1: red curved parens at superscript height (read_dx1,
  // tinted 041-cert P3 PNGs, ink span ~y149..166); other boxes: single-row
  // bars hugging the digit band (a-17..a-2), red (x2/x3) or blue (x4..x6)
  if (r.matParens) {
    const P = path.join(ASSETS, "parens042");
    const sc = 17 / 29.88;
    [[`${P}/paren_z_lp_red.png`, `${P}/paren_z_lp.json`, 330],
     [`${P}/paren_z_rp_red.png`, `${P}/paren_z_rp.json`, 380]]
      .forEach(([img, meta, tipX]) => {
        const j = JSON.parse(fs.readFileSync(meta, "utf8"));
        slide.addImage({
          path: img,
          x: px(tipX - j.ink_right_px * 0.12 * sc),
          y: px(149 - j.ink_top_px * 0.12 * sc),
          w: (j.px_w * 0.12 * sc) / 72,
          h: (j.px_h * 0.12 * sc) / 72,
        });
      });
  } else {
    [BAR1_X, BAR2_X].forEach((x) => {
      slide.addShape(pptx.ShapeType.line, {
        x: px(x), y: px(a - 17), w: 0, h: px(15),
        line: { color: r.matColor, width: 1 },
      });
    });
  }
  r.mat.forEach((d, ci) => {
    txt(d, MAT_CX[ci] - 7, a - 15, 14, 11, {
      fontSize: 10, color: r.matColor, align: "center", valign: "middle",
    });
  });

  // green d-result vector (tall, spans the box)
  tallVec(382, 397, v.y0, v.y1, v.rows, r.gVals, GREENV);

  // = value
  txt("= " + r.dEq, r.eqX, a - 3, 56, 14, { fontSize: 12, color: BLACK, valign: "middle" });

  // ⇒ action  (update rows' ⇒ is red)
  txt("\u21D2", r.arrowX || ARROW_X, a - 3, 16, 14, {
    fontSize: 12, color: r.arrowColor, align: "center", valign: "middle",
  });
  txt(r.action, r.actX || ACT_X, a - 3, 140, 14, {
    fontSize: 13, color: BLACK, valign: "middle", wrap: false,
  });

  // W = (black W vector, tall); update rows carry the family's W̲ bold+underline
  if (r.wUnderline) {
    slide.addText([
      { text: "W", options: { bold: true, underline: true } },
      { text: " =" },
    ], { x: px(r.wX), y: px(a - 3), w: px(30), h: px(14), fontSize: 11,
      color: BLACK, valign: "middle", wrap: false, fontFace: FONT, margin: 0 });
  } else {
    txt("W =", r.wX, a - 3, 20, 14, { fontSize: 11, color: BLACK, valign: "middle" });
  }
  const wGeo = [
    { xl: 646, xr: 672 }, { xl: 713, xr: 727 }, { xl: 713, xr: 728 },
    { xl: 634, xr: 651 }, { xl: 746, xr: 776 }, { xl: 752, xr: 782 },
  ][i];
  tallVec(wGeo.xl, wGeo.xr, v.y0, v.y1, v.rows, r.gVals, BLACK);

  // update rows: W = <W-vec> ± 2 * <inc-vec> = <result-vec>, red ⇐ far right
  // (box1 anchors from frame ink clusters; box3 keeps its certified positions)
  if (r.updateEq) {
    const u = r.updateEq;
    txt(u.op, u.opX, a - 3, 34, 14, { fontSize: 11, color: u.opColor, valign: "middle" });
    tallVec(u.incX[0], u.incX[1], v.y0, v.y1, v.rows, u.incVals, BLACK);
    txt("=", u.eqX, a - 3, 12, 14, { fontSize: 11, color: BLACK, valign: "middle" });
    tallVec(u.resX[0], u.resX[1], v.y0, v.y1, v.rows, u.resVals, u.resColor);
    txt("\u21D0", u.backX, a - 3, 20, 15, {
      fontSize: 12, color: RED, align: "center", valign: "middle",
    });
  }
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
