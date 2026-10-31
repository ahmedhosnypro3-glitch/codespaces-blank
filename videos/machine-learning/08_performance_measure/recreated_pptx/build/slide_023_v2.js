// slide_023 v2 — "Effect of Selecting Threshold Value on Model Performance"
// Re-fix of slide_023.js after corroboration FAIL (judge_verify_v2_1793420453_23.txt).
// PIL-adjudicated changes vs v1 (frame px, 960x540, 1px = 1pt):
//  - planes: detailed grayscale sketch PNG (plane_023.png), 11 planes at measured
//    original positions, darker ink; v1 white line-art replaced (MAJOR 1 fixed)
//  - plane count 11 with 6 red / 5 blue dots = original count (MAJOR 2 refuted by
//    PIL: original also has 11 planes; x375,y310 spot holds a RED dot, present in render)
//  - matrix1 moved to x92..230 y109..155 (rh 15.3), matrix2 x92..229 y155..221 (rh 22)
//    restoring original row heights (MINOR row compression fixed)
//  - "Actual" labels centered x79 (orig label ink x72..85, table edge x92)
//  - Threshold=0.4 callout: white fill, dark-red bold text, box x230..309 y109..135
//  - model pie disc: two-tone pie PNG (pie_023_v2.png) at x488..546 y125..167
//  - test sample: bordered rect + darker mini-plane sketch
//  - title fontSize 22 -> 26 (orig title ~661-707px wide vs render 607px)
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", YELLOW = "FFF9C4", DARK = "333333";
const BLUE = "0000FF", BLACK = "000000", WHITE = "FFFFFF";
const CREAM = "FFFDE0", MODEL_RED = "A61C1C";
const GREEN_OVAL = "B7E1CD", PINK_OVAL = "FFC0E0";
const FONT = "Arial";
const P = (px) => px / 72;

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
  fontSize: 26, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- original inner red content frame + divider under title band ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(59), y: P(63), w: P(841), h: P(453),
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.LINE, {
  x: P(59), y: P(82), w: P(841), h: 0, line: { color: RED, width: 1.5 },
});

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
  s.addText(txt, {
    x: P(cx) - P(vh) / 2, y: P(cy) - P(vw) / 2, w: P(vh), h: P(vw),
    align: "center", valign: "middle", rotate: 270, wrap: false,
    fontSize: size, bold: true, color: color, fontFace: FONT, margin: 0,
  });
}

// ---- matrix 1 (top-left, symbolic TP/FN/FP/TN): orig grid x92..230, y109..155 ----
s.addText("Predicted as", {
  x: P(92), y: P(88), w: P(138), h: P(11),
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: RED, fontFace: FONT, margin: 0,
});
rotatedLabel(79, 132, 26, 14, "Actual", RED, 8);
confusionMatrix(92, 109, 46, 15.3, { fill: WHITE });
cellText(161, 117, 30, 13, "P", RED, 10, true);
cellText(207, 117, 30, 13, "N", RED, 10, true);
cellText(115, 132, 30, 13, "P", RED, 9, true);
cellText(115, 147, 30, 13, "N", RED, 9, true);
const GREEN_INK = "3E8E22";
cellText(161, 132, 30, 13, "TP", GREEN_INK, 10, true);
cellText(207, 132, 30, 13, "FN", RED, 10, true);
cellText(161, 147, 30, 13, "FP", GREEN_INK, 10, true);
cellText(207, 147, 30, 13, "TN", RED, 10, true);

// ---- Threshold=0.4 callout: orig box x230..309, y109..135, white fill, dark-red text ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(230), y: P(109), w: P(79), h: P(26),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
s.addText("Threshold=0.4", {
  x: P(230), y: P(109), w: P(79), h: P(26),
  align: "center", valign: "middle", wrap: false,
  fontSize: 10, bold: true, color: "8B0000", fontFace: FONT, margin: 0,
});

// ---- matrix 2 (lower-left, numeric 4/1/1/5): orig grid x92..229, y155..221 ----
s.addText("Predicted as", {
  x: P(92), y: P(144), w: P(137), h: P(11),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});
rotatedLabel(79, 188, 30, 14, "Actual", RED, 8);
confusionMatrix(92, 155, 46, 22, { fill: WHITE });
cellText(161, 166, 30, 12, "P", RED, 11, true);
cellText(207, 166, 30, 12, "N", RED, 11, true);
cellText(115, 188, 30, 12, "P", RED, 11, true);
cellText(115, 210, 30, 12, "N", RED, 11, true);
cellText(161, 188, 30, 14, "4", BLUE, 12, true);
cellText(207, 188, 30, 14, "1", RED, 12, true);
cellText(161, 210, 30, 14, "1", RED, 12, true);
cellText(207, 210, 30, 14, "5", BLUE, 12, true);

// ---- pipeline panel (cream) x324..845 y99..198 ----
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(324), y: P(99), w: P(521), h: P(99),
  fill: { color: CREAM }, line: { color: "746337", width: 1.5 }, adjustValue: 0.08,
});
// Test Sample label + bordered sketch box with darker mini-plane
s.addText("Test\nSample", {
  x: P(340), y: P(100), w: P(72), h: P(26),
  align: "center", valign: "top", lineSpacing: 12,
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(360), y: P(104), w: P(56), h: P(30),
  fill: { color: WHITE }, line: { color: "808080", width: 1 },
});
s.addImage({
  path: "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/plane_023.png",
  x: P(362), y: P(109), w: P(52), h: P(52 * 417 / 792),
});

function blockArrow(x0, y0, wpx, hpx) {
  s.addShape(pptx.shapes.RIGHT_ARROW, {
    x: P(x0), y: P(y0), w: P(wpx), h: P(hpx),
    fill: { color: WHITE }, line: { color: RED, width: 1 },
  });
}
blockArrow(415, 126, 30, 16);

// Model box (dark red) x447..569 y120..179 + yellow subtitle + two-tone pie disc
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(447), y: P(120), w: P(122), h: P(59),
  fill: { color: MODEL_RED }, line: { color: RED, width: 1 },
});
s.addText("Model", {
  x: P(447), y: P(120), w: P(122), h: P(26),
  align: "center", valign: "middle",
  fontSize: 16, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (0,+1)", {
  x: P(449), y: P(162), w: P(118), h: P(11),
  align: "center", valign: "middle", wrap: false,
  fontSize: 8, bold: false, color: "FFFF00", fontFace: FONT, margin: 0,
});
s.addImage({
  path: "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/pie_023_v2.png",
  x: P(488), y: P(125), w: P(58), h: P(42),
});

blockArrow(574, 144, 36, 12);

// Predicted Value label above the (0 → -1) box
s.addText("Predicted\nValue", {
  x: P(606), y: P(112), w: P(75), h: P(26),
  align: "center", valign: "top", lineSpacing: 12,
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(619), y: P(137), w: P(51), h: P(22),
  fill: { color: WHITE }, line: { color: BLUE, width: 1.25 }, adjustValue: 0.3,
});
s.addText("(0 --- 1)", {
  x: P(619), y: P(137), w: P(51), h: P(22),
  align: "center", valign: "middle", wrap: false,
  fontSize: 10, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

blockArrow(676, 144, 14, 12);

// Threshold vertical box + rotated label
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(694), y: P(108), w: P(35), h: P(82),
  fill: { color: "F6D5B4" }, line: { color: RED, width: 1.25 }, adjustValue: 0.25,
});
rotatedLabel(711, 149, 28, 76, "Threshold (e.g. 0.5)", RED, 7);

// Class ovals + branch arrows
s.addShape(pptx.shapes.OVAL, {
  x: P(759), y: P(119), w: P(78), h: P(20),
  fill: { color: GREEN_OVAL }, line: { color: BLACK, width: 0.75 },
});
s.addText("Class I", {
  x: P(759), y: P(119), w: P(78), h: P(20),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "006100", fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: P(759), y: P(152), w: P(78), h: P(28),
  fill: { color: PINK_OVAL }, line: { color: BLACK, width: 0.75 },
});
s.addText("Class II", {
  x: P(759), y: P(152), w: P(78), h: P(28),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: "C71585", fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.LINE, {
  x: P(734), y: P(131), w: P(23), h: P(10), flipV: true,
  line: { color: RED, width: 1, endArrowType: "triangle" },
});
s.addShape(pptx.shapes.LINE, {
  x: P(734), y: P(162), w: P(23), h: P(10),
  line: { color: RED, width: 1, endArrowType: "triangle" },
});

// ---- strip plot ----
s.addShape(pptx.shapes.LINE, {
  x: P(89), y: P(436), w: P(788), h: 0, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: P(883) - P(10) / 2, y: P(436) - P(12) / 2, w: P(10), h: P(12),
  fill: { color: RED }, line: { type: "none" }, rotate: 90,
});
for (let i = 0; i <= 10; i++) {
  const x = 89 + 78.8 * i;
  s.addShape(pptx.shapes.LINE, {
    x: P(x), y: P(436), w: 0, h: P(8), line: { color: RED, width: 1.5 },
  });
}
function tickLabel(f, txt) {
  const x = 89 + 788 * f;
  s.addText(txt, {
    x: P(x - 20), y: P(450), w: P(40), h: P(16),
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
}
tickLabel(0, "0.0"); tickLabel(0.5, "0.5"); tickLabel(1, "1.0");
s.addShape(pptx.shapes.LINE, {
  x: P(59), y: P(500), w: P(841), h: 0, line: { color: RED, width: 2 },
});
for (const dx of [397, 400]) {
  s.addShape(pptx.shapes.LINE, {
    x: P(dx), y: P(210), w: 0, h: P(285),
    line: { color: "7F7F9F", width: 1.25, dashType: "dash" },
  });
}
// 11 aircraft at PIL-measured original positions: [center_x, center_y, dot_x, dot_y, dot_color]
const planes = [
  [163, 258, 128, 248, RED],
  [380, 257, 347, 230, BLUE],
  [814, 263, 776, 266, BLUE],
  [248, 306, 281, 296, RED],
  [535, 312, 572, 299, RED],
  [707, 322, 653, 311, BLUE],
  [399, 334, 375, 302, RED],
  [155, 354, 110, 342, RED],
  [820, 369, 855, 357, BLUE],
  [250, 381, 222, 372, RED],
  [555, 386, 518, 376, BLUE],
];
for (const [cx, cy, dx, dy, dot] of planes) {
  s.addImage({
    path: "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/plane_023.png",
    x: P(cx - 47.5), y: P(cy - 25), w: P(95), h: P(50),
  });
  s.addShape(pptx.shapes.OVAL, {
    x: P(dx - 4), y: P(dy - 4), w: P(8), h: P(8),
    fill: { color: dot }, line: { color: dot, width: 0.5 },
  });
}

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_023_recreated.pptx"
}).then(() => console.log("done"));
