// slide_023 — "Effect of Selecting Threshold Value on Model Performance"
// Frame-measured build: original 960x540 px, 1px = 1pt, x_in = px/72.
// House chrome per root AGENTS.md (frame/badge/title override everything).
// Content from pool_run/image_analysis/slide_023_analysis.txt (authoritative)
// cross-checked against analysis/slide_023_raw.json + PIL measurements of
// unique_slides/slide_023.jpg. Matrix1 (top-left) is symbolic TP/FN/FP/TN per
// the fresh frame read + doc-parse; matrix2 (lower-left) is numeric 4/1/1/5.
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", YELLOW = "FFF9C4", DARK = "333333";
const BLUE = "0000FF", BLACK = "000000", WHITE = "FFFFFF", GRAY = "7F7F7F";
const CREAM = "FFFDE0", MODEL_RED = "A61C1C", PALE_YELLOW = "FFF2CC";
const PALE_PINK = "FDE8E8", GREEN_OVAL = "B7E1CD", PINK_OVAL = "FFC0E0";
const PIE_PINK = "E9A7CE", PIE_MAGENTA = "C71585", FONT = "Arial";
const P = (px) => px / 72; // frame px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("23", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- divider under title band (original full-width red line at y=82) ----
s.addShape(pptx.shapes.LINE, {
  x: P(59), y: P(82), w: P(841), h: 0, line: { color: RED, width: 1.5 },
});

// ---- helper: confusion-matrix grid (cellFills: "col,row" -> hex) ----
function confusionMatrix(x0, y0, cw, rh, opts) {
  const fills = opts.cellFills || {};
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      s.addShape(pptx.shapes.RECTANGLE, {
        x: P(x0 + cw * c), y: P(y0 + rh * r), w: P(cw), h: P(rh),
        fill: { color: fills[c + "," + r] || opts.fill }, line: { type: "none" },
      });
    }
  }
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(x0), y: P(y0), w: P(cw * 3), h: P(rh * 3),
    fill: { type: "none" }, line: { color: RED, width: 1 },
  });
  for (let i = 1; i < 3; i++) {
    s.addShape(pptx.shapes.LINE, {
      x: P(x0 + cw * i), y: P(y0), w: 0, h: P(rh * 3),
      line: { color: RED, width: 1 },
    });
    s.addShape(pptx.shapes.LINE, {
      x: P(x0), y: P(y0 + rh * i), w: P(cw * 3), h: 0,
      line: { color: RED, width: 1 },
    });
  }
}
function cellText(cx, cy, w, h, txt, color, size, bold) {
  s.addText(txt, {
    x: P(cx - w / 2), y: P(cy - h / 2), w: P(w), h: P(h),
    align: "center", valign: "middle",
    fontSize: size, bold: bold, color: color, fontFace: FONT, margin: 0,
  });
}
function rotatedLabel(cx, cy, vw, vh, txt, color, size) {
  // visual bbox: w=vw h=vh; declare unrotated swapped, rotate 270 (reads bottom-to-top)
  s.addText(txt, {
    x: P(cx) - P(vh) / 2, y: P(cy) - P(vw) / 2, w: P(vh), h: P(vw),
    align: "center", valign: "middle", rotate: 270, wrap: false,
    fontSize: size, bold: true, color: color, fontFace: FONT, margin: 0,
  });
}

// ---- matrix 1 (top-left, symbolic TP/FN/FP/TN) ----
// grid x82..204 (cw 41/40), y97..150 (rh ~17.7); "Predicted as" above at y86..96
s.addText("Predicted as", {
  x: P(82), y: P(84), w: P(122), h: P(11),
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: RED, fontFace: FONT, margin: 0,
});
rotatedLabel(73, 120, 26, 14, "Actual", RED, 8);
confusionMatrix(82, 95, 41, 17, {
  fill: WHITE,
  cellFills: { "1,1": "C6E0B4", "2,2": "C6E0B4", "2,1": PALE_YELLOW }, // TP, TN green; FN pale yellow
});
// header row (y95..112): P, N in cols 2,3 — dark per frame (no blue ink there)
cellText(143, 103, 30, 14, "P", DARK, 10, true);
cellText(183, 103, 30, 14, "N", DARK, 10, true);
// row labels col1
cellText(102, 120, 30, 14, "P", DARK, 9, true);
cellText(102, 137, 30, 14, "N", DARK, 9, true);
// cells
cellText(143, 120, 30, 14, "TP", DARK, 10, true);
cellText(183, 120, 30, 14, "FN", DARK, 10, true);
cellText(143, 137, 30, 14, "FP", DARK, 10, true);
cellText(183, 137, 30, 14, "TN", DARK, 10, true);

// ---- Threshold=0.4 callout (x240..310, y108..136; pale-yellow fill per frame) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(234), y: P(108), w: P(84), h: P(28),
  fill: { color: "F0E0C0" }, line: { color: RED, width: 1.5 },
});
s.addText("Threshold=0.4", {
  x: P(234), y: P(108), w: P(84), h: P(28),
  align: "center", valign: "middle", wrap: false,
  fontSize: 9.5, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- matrix 2 (lower-left, numeric 4/1/1/5) ----
// grid x81..229 (cw ~49), y176..222 (rh ~15.3); "Predicted as" above, clear of matrix 1
s.addText("Predicted as", {
  x: P(81), y: P(149), w: P(148), h: P(12),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});
rotatedLabel(73, 199, 30, 14, "Actual", RED, 8);
confusionMatrix(81, 176, 49, 15, { fill: WHITE });
cellText(154, 183, 30, 12, "P", BLUE, 11, true);
cellText(204, 183, 30, 12, "N", BLUE, 11, true);
cellText(105, 191, 30, 12, "P", BLUE, 10, true);
cellText(105, 207, 30, 12, "N", BLUE, 10, true);
cellText(154, 199, 30, 13, "4", BLUE, 12, true);
cellText(204, 199, 30, 13, "1", RED, 12, true);
cellText(154, 214, 30, 13, "1", RED, 12, true);
cellText(204, 214, 30, 13, "5", BLUE, 12, true);

// ---- pipeline panel (cream, x324..845 y99..198) ----
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(324), y: P(99), w: P(521), h: P(99),
  fill: { color: CREAM }, line: { color: RED, width: 1.5 }, adjustValue: 0.08,
});
// Test Sample label (two lines) + small plane sketch
s.addText("Test\nSample", {
  x: P(340), y: P(100), w: P(72), h: P(26),
  align: "center", valign: "top", lineSpacing: 12,
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// propeller-plane sketch (gray line art), centered at (cx,cy) in px
function drawPlane(cx, cy, wpx) {
  const w = P(wpx), h = w * 0.42, X = P(cx), Y = P(cy);
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: X - w / 2, y: Y - h * 0.10, w: w, h: h * 0.20,
    fill: { color: WHITE }, line: { color: GRAY, width: 1 }, adjustValue: 0.5,
  });
  s.addShape(pptx.shapes.OVAL, {
    x: X + w / 2 - h * 0.24, y: Y - h * 0.10, w: h * 0.24, h: h * 0.20,
    fill: { color: WHITE }, line: { color: GRAY, width: 1 },
  });
  s.addShape(pptx.shapes.LINE, {
    x: X + w / 2, y: Y - h * 0.32, w: 0, h: h * 0.64, line: { color: GRAY, width: 1.25 },
  });
  s.addShape(pptx.shapes.LINE, {
    x: X + w / 2 - h * 0.09, y: Y, w: h * 0.18, h: 0, line: { color: GRAY, width: 1 },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X + w * 0.10, y: Y + h * 0.05, w: w * 0.22, h: h * 0.46,
    fill: { color: WHITE }, line: { color: GRAY, width: 1 }, rotate: 210,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X + w * 0.10, y: Y - h * 0.51, w: w * 0.22, h: h * 0.46,
    fill: { color: WHITE }, line: { color: GRAY, width: 1 }, rotate: 150,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X - w * 0.46, y: Y + h * 0.04, w: w * 0.18, h: h * 0.36,
    fill: { color: WHITE }, line: { color: GRAY, width: 1 }, rotate: 195,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: X - w * 0.46, y: Y - h * 0.40, w: w * 0.18, h: h * 0.36,
    fill: { color: WHITE }, line: { color: GRAY, width: 1 }, rotate: 165,
  });
}
drawPlane(388, 133, 46);

// block arrows (white fill, red outline)
function blockArrow(x0, y0, wpx, hpx) {
  s.addShape(pptx.shapes.RIGHT_ARROW, {
    x: P(x0), y: P(y0), w: P(wpx), h: P(hpx),
    fill: { color: WHITE }, line: { color: RED, width: 1 },
  });
}
blockArrow(415, 126, 30, 16);

// Model box (dark red) x447..571 y121..155 + yellow subtitle + pie icon
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(447), y: P(121), w: P(124), h: P(34),
  fill: { color: MODEL_RED }, line: { color: RED, width: 1 },
});
s.addText("Model", {
  x: P(447), y: P(121), w: P(124), h: P(22),
  align: "center", valign: "middle",
  fontSize: 16, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (0, +1)", {
  x: P(449), y: P(144), w: P(120), h: P(10),
  align: "center", valign: "middle",
  fontSize: 6.5, bold: false, color: "FFFF00", fontFace: FONT, margin: 0,
});
// pie icon at right end of Model box: 600dpi PNG embedded at exact size (w = px/600 in)
s.addImage({
  path: "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/pie_023.png",
  x: P(546), y: P(127), w: 150 / 600, h: 150 / 600,
});

blockArrow(576, 126, 30, 16);

// Predicted Value label (two lines) above the (0 → -1) box
s.addText("Predicted\nValue", {
  x: P(606), y: P(112), w: P(75), h: P(26),
  align: "center", valign: "top", lineSpacing: 12,
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(612), y: P(138), w: P(66), h: P(24),
  fill: { color: WHITE }, line: { color: BLUE, width: 1.25 }, adjustValue: 0.3,
});
s.addText("(0 --- 1)", {
  x: P(612), y: P(138), w: P(66), h: P(24),
  align: "center", valign: "middle", wrap: false,
  fontSize: 10, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

blockArrow(682, 126, 14, 16);

// Threshold vertical box (pale salmon fill per frame, red border) x694..729 y108..190, rotated label
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(694), y: P(108), w: P(35), h: P(82),
  fill: { color: "F6D5B4" }, line: { color: RED, width: 1.25 }, adjustValue: 0.25,
});
rotatedLabel(711, 149, 28, 76, "Threshold (e.g. 0.5)", RED, 7);

// Class ovals + branch arrows from threshold box
s.addShape(pptx.shapes.OVAL, {
  x: P(759), y: P(119), w: P(78), h: P(20),
  fill: { color: GREEN_OVAL }, line: { color: BLACK, width: 0.75 },
});
s.addText("Class I", {
  x: P(759), y: P(119), w: P(78), h: P(20),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: P(759), y: P(152), w: P(78), h: P(28),
  fill: { color: PINK_OVAL }, line: { color: BLACK, width: 0.75 },
});
s.addText("Class II", {
  x: P(759), y: P(152), w: P(78), h: P(28),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// thin red arrows: threshold right edge -> Class I (up-right) and Class II (down-right)
s.addShape(pptx.shapes.LINE, {
  x: P(734), y: P(131), w: P(23), h: P(10), flipV: true,
  line: { color: RED, width: 1, endArrowType: "triangle" },
});
s.addShape(pptx.shapes.LINE, {
  x: P(734), y: P(162), w: P(23), h: P(10),
  line: { color: RED, width: 1, endArrowType: "triangle" },
});

// ---- strip plot ----
// axis line y=436, x89..877, red, arrowhead at right
s.addShape(pptx.shapes.LINE, {
  x: P(89), y: P(436), w: P(788), h: 0, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  // visual: x877..889 y431..441 pointing right; declare unrotated swapped, rotate 90
  x: P(883) - P(10) / 2, y: P(436) - P(12) / 2, w: P(10), h: P(12),
  fill: { color: RED }, line: { type: "none" }, rotate: 90,
});
// 11 ticks at 0.1 steps
for (let i = 0; i <= 10; i++) {
  const x = 89 + 78.8 * i;
  s.addShape(pptx.shapes.LINE, {
    x: P(x), y: P(436), w: 0, h: P(8), line: { color: RED, width: 1.5 },
  });
}
// tick labels 0.0 / 0.5 / 1.0 (bold red) at y450..466
function tickLabel(f, txt) {
  const x = 89 + 788 * f;
  s.addText(txt, {
    x: P(x - 20), y: P(450), w: P(40), h: P(16),
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
}
tickLabel(0, "0.0"); tickLabel(0.5, "0.5"); tickLabel(1, "1.0");
// full-width red line at y=500
s.addShape(pptx.shapes.LINE, {
  x: P(59), y: P(500), w: P(841), h: 0, line: { color: RED, width: 2 },
});
// two dashed gray-lavender verticals at threshold 0.4 (x397 / x400.5), y210..495 per frame
for (const dx of [397, 400.5]) {
  s.addShape(pptx.shapes.LINE, {
    x: P(dx), y: P(210), w: 0, h: P(285),
    line: { color: "7F7F9F", width: 1.25, dashType: "dash" },
  });
}
// 11 airplane samples: [axis_fraction, y_px, dot_color]
const planes = [
  [0.05, 340, RED], [0.25, 300, RED], [0.03, 360, RED], [0.17, 380, RED],
  [0.365, 332, RED], [0.62, 320, RED],
  [0.34, 240, BLUE], [0.55, 385, BLUE], [0.72, 310, BLUE],
  [0.89, 260, BLUE], [0.99, 370, BLUE],
];
for (const [f, y, dot] of planes) {
  const x = 89 + 788 * f;
  drawPlane(x, y, 34);
  s.addShape(pptx.shapes.OVAL, {
    x: P(x + 13), y: P(y - 6), w: P(7), h: P(7),
    fill: { color: dot }, line: { color: dot, width: 0.5 },
  });
}

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_023_recreated.pptx"
}).then(() => console.log("done"));
