// Build: slide 042 — "Iteration 1" (Perceptron gradient-descent worked example)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GROUND TRUTH: unique_slides/slide_042.jpg (960x540, 1px = 1pt = 1/72in).
// Measurements: scratch/tmp/eq042/{meas_orig,meas_orig2,pixdump,blockmap,
// stack_struct,stack_boxes,stack_lines,green_zoom,ascii_stack,ascii_tl,
// ascii_center,ascii_lm,lm_bands,final_meas,box_edges,final_edges,meas4,meas5}.txt
// Spec cross-check: analysis/slide_042_final.json (frame wins on conflict).

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

const OUT = path.resolve(__dirname, "../slide_042_recreated.pptx");

const px = (v) => v / 72; // frame px -> inches

const RED = "FF0000";
const BLUE = "0000FF";      // frame-measured C00000-stroke blue is #0000FF
const BLACK = "000000";
const GREEN = "008000";
const WHITE = "FFFFFF";
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

// stacked digits, centred on cx, band top at yTop
function vecCol(digits, cx, yTop, size, color, bold) {
  const h = size * 1.18;
  digits.forEach((d, i) => {
    txt(String(d), cx - size, yTop + i * h, size * 2, h, {
      fontSize: size, color, bold, align: "center", valign: "middle",
    });
  });
}

// ---- house chrome (deck 03 values) -----------------------------------------
drawHouseChrome(pptx, slide, { numeral: 42 });

// ---------------------------------------------------------------------------
// white content areas (frame shows white boxes on the gray panel)
// ---------------------------------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: px(69), y: px(55), w: px(650), h: px(73), fill: { color: WHITE },
});

// right computation stack: five white boxes separated by panel-gray gaps
const STACK_BOXES = [
  [228, 261], [272, 327], [338, 393], [404, 459], [470, 527],
];
STACK_BOXES.forEach(([y0, y1]) => {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(276), y: px(y0), w: px(622), h: px(y1 - y0 + 1),
    fill: { color: WHITE },
  });
});

// ---------------------------------------------------------------------------
// 1. TOP-LEFT vector table  (inside the blue box, x68..720 y54..130)
// ---------------------------------------------------------------------------
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(54), w: px(653), h: px(77),
  fill: { type: "none" }, line: { color: BLUE, width: 1 },
});

// caption "x1..x6" — blue, one label per column (digit centres 95,117,139,161,184,206)
[95, 117, 139, 161, 184, 206].forEach((cx, i) => {
  txt("x" + (i + 1), cx - 9, 63, 18, 11, {
    fontSize: 10, color: BLUE, bold: true, align: "center", valign: "middle",
  });
});

// value rows: two digits stacked per column (a 2-D vector)
const TL_COLS = [[1, 1], [2, 1], [1, 2], [5, 4], [6, 5], [6, 6]];
TL_COLS.forEach((v, i) => {
  const cx = [95, 117, 139, 161, 184, 206][i];
  vecCol(v, cx, 78, 11, BLACK, true);
});

// class row y110..123: C1 C1 C1 C2 C2 C2
[["C1", 95], ["C1", 117], ["C1", 139], ["C2", 161], ["C2", 184], ["C2", 206]]
  .forEach(([lab, cx]) => {
    txt(lab, cx - 9, 109, 18, 15, {
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
txt("Initial W =", 262, 71, 70, 18, {
  fontSize: 14, color: BLACK, valign: "middle",
});
// 2x1 matrix with tall parentheses: frame ink x330..353, y64..102
txt("(", 328, 63, 14, 40, { fontSize: 34, color: BLACK, align: "center", valign: "middle" });
txt(")", 344, 63, 14, 40, { fontSize: 34, color: BLACK, align: "center", valign: "middle" });
txt("4", 338, 74, 14, 14, { fontSize: 13, color: BLACK, align: "center", valign: "middle" });
txt("-2", 335, 88, 18, 14, { fontSize: 13, color: BLACK, align: "center", valign: "middle" });

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
  txt("Z" + (i + 1), cx - 9, 62, 18, 13, {
    fontSize: 10, color: BLUE, bold: true, align: "center", valign: "middle",
  });
});
// Z vectors: col1 = (0;0), col2 = (7;6), col3 = (3;2); bands y83..94 / y99..108
[[0, 0], [7, 6], [3, 2]].forEach((v, i) => {
  vecCol(v, [601, 625, 645][i], 82, 11, BLACK, true);
});

// legend sentence x257..508 y110..123 — "C1" is BLACK in the frame (no red ink).
// Segment widths are calibrated so the measured ink lands on the frame's
// segment boundaries: black x257..302, blue C2 x310..326, black x330..378,
// green Zero x395..423, black x430..508.
const LEGEND = [
  { t: "C1 positive, ", c: BLACK, x: 257 },
  { t: "C2", c: BLUE, x: 310 },
  { t: " negative, ", c: BLACK, x: 330 },
  { t: "Zero", c: GREEN, x: 394 },
  { t: " is unaccepted", c: BLACK, x: 428 },
];
LEGEND.forEach((s) => {
  txt(s.t, s.x, 108, 90, 16, { fontSize: 13, color: s.c, valign: "middle" });
});

// ---------------------------------------------------------------------------
// 4. LEFT-MIDDLE "Upgraded Vectors (From Top)"
// ---------------------------------------------------------------------------
txt("Upgraded Vectors (From Top)", 79, 150, 168, 13, {
  fontSize: 11, color: BLUE, bold: true, valign: "middle",
});

const LM_CENTRES = [99, 121, 143, 166, 188, 211];
const LM_BANDS = [
  { y: 164, vals: [1, 1, 1, 2, 1, 1] },
  { y: 183, vals: [1, 1, 1, 1, 1, 1] },
  { y: 195, vals: [1, 1, 1, 1, 1, 1] },
  { y: 212, vals: [1, 2, 1, 5, 6, 6] },
];
// parentheses span the full four-band height (frame: "(" x93..94/114..116/
// 136..138/159..161/182..183/204..206, ")" x105..107/127..128/149..151/
// 172..174/195..196/218..219)
const LM_LPAREN = [92, 113, 135, 158, 181, 203];
const LM_RPAREN = [104, 126, 148, 171, 194, 217];
LM_BANDS.forEach((band) => {
  LM_CENTRES.forEach((cx, ci) => {
    txt(String(band.vals[ci]), cx - 5, band.y, 11, 11, {
      fontSize: 10, color: BLACK, align: "center", valign: "middle",
    });
  });
});
// parentheses span the full four-band height (frame: "(" x93..94/114..116/
// 136..138/159..161/182..183/204..206, ")" x105..107/127..128/149..151/
// 172..174/195..196/218..219)
LM_LPAREN.forEach((x) => txt("(", x, 164, 12, 60, { fontSize: 48, color: BLACK, align: "center", valign: "middle" }));
LM_RPAREN.forEach((x) => txt(")", x, 164, 12, 60, { fontSize: 48, color: BLACK, align: "center", valign: "middle" }));

// class row y231..243: C1 C1 C1 C2 C2 C2
[["C1", 95], ["C1", 117], ["C1", 139], ["C2", 161], ["C2", 184], ["C2", 206]]
  .forEach(([lab, cx]) => {
    txt(lab, cx - 10, 230, 20, 14, {
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
// 6. RIGHT COMPUTATION STACK — 5 white boxes, content inside
// ---------------------------------------------------------------------------
// measured (frame px): line A top / line B top per box, the action text at
// x~684..760 (box1) and x~611..739 (box3), the W line at x~384..726.
// font sizes calibrated from render-vs-frame width ratios (see
// scratch/tmp/eq042/calibrate.txt):
//   action text        ratio 1.90  -> 10pt x 1.9  = 16pt
//   matrix digits      ratio 1.52  -> 10pt x 1.5  = 11.5pt (punched to 11)
//   "d(x_i) =" label   ratio 1.52  -> 10pt x 1.5  = 15pt (punched to 14)
//   "= <value>"        ratio 1.52  -> 14pt
//   W line (full)      ratio 2.81  -> ~14pt across all parts
const ROWS = [
  {
    a: 231, b: 248, sub: "1", dMat: [[1, 1, 1, 4], [-2, 0, "", ""]],
    dEq: "0", action: "Update Weight", actionColor: RED, actionX: 682, actionW: 130,
    w: { mat: [[4], [-2]], op: "+", rh: [[1], [1]], eq: [[6], [0]] },
    greenRight: false,
  },
  {
    a: 296, b: 311, sub: "2", dMat: [[1, 2, 1, 6], [0, 0, "", ""]],
    dEq: "6", action: "Keep same Weight", actionColor: BLACK, actionX: 682, actionW: 130,
    w: { mat: [[6], [0]], op: null, eq: null },
    greenRight: false,
  },
  {
    a: 359, b: 375, sub: "3", dMat: [[1, 1, 2, ""], [0, 0, "", ""]],
    dEq: "6", action: "Keep same Weight", actionColor: BLACK, actionX: 682, actionW: 130,
    w: { mat: [[6], [0]], op: null, eq: null },
    greenRight: true,
  },
  {
    a: 428, b: 443, sub: "4", dMat: [[1, 5, 4, ""], [0, 0, "", ""]],
    dEq: "6", action: "Update Weight", actionColor: RED, actionX: 682, actionW: 130,
    w: { mat: [[6], [0]], op: "-", rh: [[1], [5]], eq: [[4], [-10]] },
    greenRight: true,
  },
  {
    a: 493, b: 502, sub: "5", dMat: [[1, 6, 5, ""], [-10, -98, "", ""]],
    dEq: "-96", action: "Keep same Weight", actionColor: BLACK, actionX: 682, actionW: 130,
    w: { mat: [[4], [-10]], op: null, eq: null },
    greenRight: true,
  },
];

const LBL_X = 400;       // d(x_i) label left, frame ink x400..417
const MAT_X = 489;       // matrix digit left edge, frame ink x489..601
const EQ_X = 606;        // "= 0" result
const W_X = 384;         // W line left (frame ink x384..726)
const ACT_X = 662;       // ⇒ + action left
const W_FONT = 13;       // calibrated W-line size

ROWS.forEach((r) => {
  // line A: d(x_i) = <matrix> = <value>   ⇒ <action>
  // the frame's label runs x400..417 total; the subscript digit is small and
  // sits at the baseline, so draw "d(x" + subscript + ") =" as adjacent boxes
  // instead of one string (the Unicode subscript glyph renders far too wide).
  txt("d(x", LBL_X, r.a - 4, 16, 14, { fontSize: 14, color: BLACK, valign: "middle" });
  txt(r.sub, LBL_X + 15, r.a - 1, 7, 10, { fontSize: 9, color: BLACK, align: "center", valign: "middle" });
  txt(") =", LBL_X + 20, r.a - 4, 14, 14, { fontSize: 14, color: BLACK, valign: "middle" });
  (r.dMat || []).forEach((row, ri) => {
    row.forEach((cell, ci) => {
      if (cell === "") return;
      txt(String(cell), MAT_X + ci * 13, r.a - 4 + ri * 11, 13, 11, {
        fontSize: 11, color: BLACK, align: "center", valign: "middle",
      });
    });
  });
  txt("= " + r.dEq, EQ_X, r.a - 4, 52, 14, { fontSize: 14, color: BLACK, valign: "middle" });
  txt("\u21D2", ACT_X, r.a - 4, 16, 14, {
    fontSize: 14, color: BLACK, align: "center", valign: "middle",
  });
  txt(r.action, r.actionX, r.a - 4, r.actionW, 14, {
    fontSize: 16, color: r.actionColor, valign: "middle",
  });

  // line B: W = <matrix> [op <vec> = <vec>]
  // the frame's line B occupies a single compact band (y249..258 in box1);
  // the two stacked matrix rows must not spill into the gray gap at y262.
  if (r.w) {
    txt("W =", W_X + 2, r.b - 5, 24, 12, { fontSize: W_FONT, color: BLACK, valign: "middle" });
    (r.w.mat || []).forEach((row, ri) => {
      row.forEach((cell) => {
        txt(String(cell), W_X + 26, r.b - 5 + ri * 11, 22, 11, {
          fontSize: W_FONT, color: BLACK, align: "center", valign: "middle",
        });
      });
    });
    if (r.w.op) {
      txt(r.w.op, W_X + 48, r.b - 5, 16, 12, { fontSize: W_FONT, color: BLACK, valign: "middle" });
      (r.w.rh || []).forEach((row, ri) => {
        txt(String(row[0]), W_X + 64, r.b - 5 + ri * 11, 22, 11, {
          fontSize: W_FONT, color: BLACK, align: "center", valign: "middle",
        });
      });
      txt("=", W_X + 88, r.b - 5, 14, 12, { fontSize: W_FONT, color: BLACK, valign: "middle" });
      (r.w.eq || []).forEach((row, ri) => {
        txt(String(row[0]), W_X + 102, r.b - 5 + ri * 11, 26, 11, {
          fontSize: W_FONT, color: BLACK, align: "center", valign: "middle",
        });
      });
    }
  }

  // green marks: one at the left of every box, plus one at the right in boxes 3-5
  txt("\u21D0", W_X - 4, r.b - 6, 16, 14, {
    fontSize: 12, color: GREEN, align: "center", valign: "middle",
  });
  if (r.greenRight) {
    txt("\u21D0", 738, r.b - 6, 16, 14, {
      fontSize: 12, color: GREEN, align: "center", valign: "middle",
    });
  }
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
