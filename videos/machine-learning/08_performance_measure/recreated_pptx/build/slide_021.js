const pptxgen = require("pptxgenjs");

// Slide 21 — Effect of Selecting Threshold Value on Model Performance
// v3 fixes from judge_attempt_2 (FAIL) adjudicated against frame pixels:
//  - panel drawn first (z-order), callout white fill + red border on top, no overlap
//  - confusion tables: explicit band heights (v2 let table2 bands overflow its bottom)
//  - data cells: 5 red bold + red circle, 0 red, 4 blue, 2 blue (judge read of original)
//  - vertical "Actual" adjacent to row labels; row labels P/N in label column
//  - class ovals (not rects) fully inside panel; threshold node tall w/ rotated text
//  - dashed blue line x=152 through lower-matrix TP cell, extending below axis
//  - axis x78..828 with right arrowhead, ticks 0.0/0.5/1.0, single line (no y499 rule)
//  - dropped extra vertical "Predicted" caption; bigger varied airplanes with dots/skulls
//  - Test Sample = caption + large unbordered sketch (no box)
// Legend green/yellow cell fills REJECTED: frame pixels show white/pink-tint cells only.
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const FONT = "Arial";
const DARKRED = "9C0006";
const DARKRED_LINE = "600000";
const BLUE = "0000FF";
const REDTXT = "FF0000";
const BLUETXT = "0000FF";
const BLUE_TXT = "1F3864";
const PANEL_FILL = "FFF2CC";
const PANEL_LINE = "BFA05A";
const GREEN_FILL = "D1F2DD";
const GREEN_LINE = "2E7D32";
const PLUM_FILL = "FBD5FE";
const PLUM_LINE = "8E24AA";
const GRAY = "404040";
const SIGPURPLE = "800080";
const SIGLAV = "E6C8F0";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("21", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});

const I = (px) => px / 72;
const T = (txt, x, y, w, h, size, color, bold, rot) => s.addText(txt, {
  x: I(x), y: I(y), w: I(w), h: I(h),
  align: "center", valign: "middle",
  fontSize: size, bold: !!bold, color: color, fontFace: FONT, margin: 0,
  ...(rot ? { rotate: rot } : {}),
});
const R = (x, y, w, h, fill, line, lw, shape) => s.addShape(shape || pptx.shapes.RECTANGLE, {
  x: I(x), y: I(y), w: I(w), h: I(h),
  ...(fill ? { fill: { color: fill } } : {}),
  line: { color: line, width: lw },
});

// ---- confusion-matrix table (x57..230; label col 67..129; cells c1 131..178, c2 180..228) ----
function confusionTable(topPx, bottomPx, cells, cellColors, circleCell) {
  const x0 = 57, xR = 230, xDiv1 = 129, xDiv2 = 178;
  const headerH = 27, colHeadH = 48;
  const rowsH = bottomPx - topPx - headerH - colHeadH;
  const rowH = rowsH / 2;
  const y0 = topPx, yHead = topPx + headerH, yCol = topPx + headerH + colHeadH, yMid = yCol + rowH, yB = bottomPx;
  R(x0, y0, xR - x0, yB - y0, "FFFFFF", RED, 1.5);
  // horizontal lines
  R(x0, yHead, xR - x0, 1.5, RED, RED, 0.5);
  R(x0, yCol, xR - x0, 1.5, RED, RED, 0.5);
  R(x0, yMid, xR - x0, 1.5, RED, RED, 0.5);
  // vertical lines (full height below header band for the cell split; label divider full height)
  R(xDiv1, y0, 1.5, yB - y0, RED, RED, 0.5);
  R(xDiv2, yHead, 1.5, yB - yHead, RED, RED, 0.5);
  // header
  T("Predicted as", xDiv1, y0 + 2, xR - xDiv1, headerH - 4, 11, RED, true);
  // column heads
  T("P", xDiv1 + 2, yHead + 2, xDiv2 - xDiv1 - 4, colHeadH - 4, 12, DARK, true);
  T("N", xDiv2 + 2, yHead + 2, xR - xDiv2 - 4, colHeadH - 4, 12, DARK, true);
  // row labels in label col (right part of it, next to the cells)
  T("P", 88, yCol + 2, 38, rowH - 4, 12, DARK, true);
  T("N", 88, yMid + 2, 38, rowH - 4, 12, DARK, true);
  // vertical "Actual" caption just left of the row labels
  T("Actual", 74 - 30, (yCol + yB) / 2 - 8, 60, 16, 10, RED, true, -90);
  // cells: order c1rowP, c2rowP, c1rowN, c2rowN
  const boxes = [
    [xDiv1 + 2, yCol + 2, xDiv2 - xDiv1 - 4, rowH - 4],
    [xDiv2 + 2, yCol + 2, xR - xDiv2 - 4, rowH - 4],
    [xDiv1 + 2, yMid + 2, xDiv2 - xDiv1 - 4, rowH - 4],
    [xDiv2 + 2, yMid + 2, xR - xDiv2 - 4, rowH - 4],
  ];
  cells.forEach((c, i) => {
    T(c, boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3], 15, cellColors[i], i === circleCell);
  });
  if (circleCell >= 0) {
    const b = boxes[circleCell];
    s.addShape(pptx.shapes.OVAL, {
      x: I(b[0] + b[2] / 2 - 24), y: I(b[1] + b[3] / 2 - 24), w: I(48), h: I(48),
      line: { color: REDTXT, width: 2.25 },
    });
  }
}

// legend (structure only): TP/FN ; FP/TN
confusionTable(81, 198, ["TP", "FN", "FP", "TN"], [DARK, DARK, DARK, DARK], -1);
// data: TP=5 (red, circled), FN=0 (red), FP=4 (blue), TN=2 (blue)
confusionTable(199, 300, ["5", "0", "4", "2"], [REDTXT, REDTXT, BLUETXT, BLUETXT], 0);

// ---- beige pipeline panel FIRST (z-order below callout) x285..835 y88..195 ----
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: I(285), y: I(88), w: I(550), h: I(107),
  fill: { color: PANEL_FILL }, line: { color: PANEL_LINE, width: 1 }, adjustValue: 0.08,
});

// ---- Threshold=0.1 callout (white fill, red border) x150..258 y105..135 ----
R(150, 105, 108, 30, "FFFFFF", RED, 1.5, pptx.shapes.ROUNDED_RECTANGLE);
T("Threshold=0.1", 150, 105, 108, 30, 11, RED, true);

// ---- flowchart ----
// Test Sample: caption + large unbordered sketch (no box)
T("Test Sample", 324, 106, 124, 18, 12, DARK, true);
function drawPlane(slide, cx, cy, w, dotColor, skull, rot) {
  const h = w * 0.40;
  const rotv = rot || 0;
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: cx - w / 2, y: cy - h * 0.10, w: w, h: h * 0.20,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, adjustValue: 0.5, rotate: rotv,
  });
  slide.addShape(pptx.shapes.OVAL, {
    x: cx + w / 2 - h * 0.24, y: cy - h * 0.11, w: h * 0.24, h: h * 0.22,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: rotv,
  });
  slide.addShape(pptx.shapes.LINE, { x: cx + w / 2 + 0.02, y: cy - h * 0.32, w: 0, h: h * 0.64, line: { color: GRAY, width: 1.75 }, rotate: rotv });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w * 0.14, y: cy + h * 0.05, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: 205 + rotv,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w * 0.14, y: cy - h * 0.50, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: 155 + rotv,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.44, y: cy + h * 0.04, w: w * 0.18, h: h * 0.36,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: 195 + rotv,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.44, y: cy - h * 0.40, w: w * 0.18, h: h * 0.36,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.5 }, rotate: 165 + rotv,
  });
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx + w * 0.06 + i * w * 0.11, y: cy - h * 0.05, w: h * 0.10, h: h * 0.10,
      fill: { color: "FFFFFF" }, line: { color: GRAY, width: 0.75 }, rotate: rotv,
    });
  }
  if (dotColor) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx - I(4), y: cy - h * 0.55 - I(4), w: I(8), h: I(8),
      fill: { color: dotColor }, line: { color: dotColor, width: 0.5 },
    });
  }
  if (skull) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx - I(6), y: cy - I(6), w: I(12), h: I(12),
      fill: { color: "000000" }, line: { color: "000000", width: 0.5 },
    });
    slide.addShape(pptx.shapes.LINE, { x: cx - I(7), y: cy - I(1), w: I(14), h: 0, line: { color: "FFFFFF", width: 1.25 } });
    slide.addShape(pptx.shapes.LINE, { x: cx - I(1), y: cy - I(7), w: 0, h: I(14), line: { color: "FFFFFF", width: 1.25 } });
  }
}
drawPlane(s, I(386), I(168), I(64), null, false, -6);

// arrow Test Sample -> Model
s.addShape(pptx.shapes.RIGHT_ARROW, { x: I(452), y: I(140), w: I(20), h: I(16), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });

// Model box x476..589 y119..181 dark red
R(476, 119, 113, 62, DARKRED, DARKRED_LINE, 1.5);
T("Model", 476, 122, 113, 18, 13, "FFFFFF", true);
// sigmoid icon
s.addShape(pptx.shapes.OVAL, { x: I(544), y: I(124), w: I(36), h: I(36), fill: { color: SIGLAV }, line: { color: SIGPURPLE, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: I(547), y: I(142), w: I(30), h: 0, line: { color: SIGPURPLE, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: I(562), y: I(127), w: 0, h: I(30), line: { color: SIGPURPLE, width: 0.75 } });
(function () {
  const steps = 16; let px = null, py = null;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps - 0.5) * 8;
    const sig = 1 / (1 + Math.exp(-t));
    const x = I(549) + (i / steps) * I(26);
    const y = I(156) - sig * I(26);
    if (px !== null) s.addShape(pptx.shapes.LINE, { x: px, y: py, w: x - px, h: y - py, line: { color: SIGPURPLE, width: 1 } });
    px = x; py = y;
  }
})();
// corrected annotation below Model box
T("[Any value] \u2192 (0, +1)", 476, 183, 113, 14, 8, RED, true);

// arrow Model -> blue box
s.addShape(pptx.shapes.RIGHT_ARROW, { x: I(593), y: I(140), w: I(18), h: I(16), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });

// blue box "(0 — 1)" x615..703 y119..181; "Predicted Value" above
T("Predicted Value", 615, 103, 88, 14, 10, BLUE_TXT, true);
R(615, 119, 88, 62, "DCE6F5", BLUE, 1.5);
T("(0 \u2014 1)", 615, 119, 88, 62, 13, BLUE, true);

// arrow blue -> threshold
s.addShape(pptx.shapes.RIGHT_ARROW, { x: I(707), y: I(140), w: I(18), h: I(16), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });

// threshold node: tall white rounded rect, red border, rotated text x729..765 y100..185
R(729, 100, 36, 85, "FFFFFF", RED, 1.5, pptx.shapes.ROUNDED_RECTANGLE);
T("Threshold (e.g. 0.5)", 747 - 45, 142 - 8, 90, 16, 9, RED, true, -90);

// branch arrows to class ovals
s.addShape(pptx.shapes.RIGHT_ARROW, { x: I(769), y: I(116), w: I(20), h: I(11), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: I(769), y: I(150), w: I(20), h: I(11), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });

// Class I / II ovals fully inside panel (panel right edge x835)
s.addShape(pptx.shapes.OVAL, { x: I(793), y: I(106), w: I(42), h: I(26), fill: { color: GREEN_FILL }, line: { color: GREEN_LINE, width: 1 } });
T("Class I", 793, 106, 42, 26, 9, DARK, true);
s.addShape(pptx.shapes.OVAL, { x: I(793), y: I(140), w: I(42), h: I(26), fill: { color: PLUM_FILL }, line: { color: PLUM_LINE, width: 1 } });
T("Class II", 793, 140, 42, 26, 9, DARK, true);

// ---- bottom scatter plot ----
const X0 = 78, X1 = 828, AX = 436;
// single red x-axis with right arrowhead
R(60, AX - 1, X1 - 60 + 14, 2.5, RED, RED, 0.5);
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
  x: I(X1 + 12), y: I(AX - 6), w: I(16), h: I(12),
  fill: { color: RED }, line: { color: RED, width: 0.5 }, rotate: 90,
});
for (let k = 0; k <= 20; k++) {
  const xc = X0 + (X1 - X0) * k / 20;
  const major = k % 10 === 0;
  R(xc, AX, 1.5, major ? 9 : 5, DARK, DARK, 0.5);
  if (major) T(k === 0 ? "0.0" : k === 10 ? "0.5" : "1.0", xc - 16, AX + 12, 32, 14, 10, RED, true);
}
// dashed blue vertical threshold line at x=152 (0.1 on 78..828 axis), through lower-matrix TP cell, below axis
(function () {
  for (let y = 199; y < AX + 28; y += 12) {
    R(151, y, 2, 7, BLUE, BLUE, 0.25);
  }
})();
// airplane scatter: ~11 larger varied planes with class dots, two skull-marked at right
const planes = [
  [150, 330, 78, "FF0000", false, -8], [235, 380, 92, "0000FF", false, 5],
  [330, 315, 70, "FF0000", false, -4], [425, 375, 85, "0000FF", false, 8],
  [520, 325, 75, "FF0000", false, -6], [610, 385, 95, "0000FF", false, 4],
  [700, 320, 68, "FF0000", false, -5], [790, 370, 88, "0000FF", true, 6],
  [860, 330, 80, "FF0000", true, -7], [370, 420, 72, "0000FF", false, 3],
  [560, 425, 82, "FF0000", false, -3],
];
planes.forEach(([cx, cy, w, dot, skull, rot]) => drawPlane(s, I(cx), I(cy), I(w), dot, skull, rot));

pptx.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_021_recreated.pptx"
}).then(() => console.log("done"));
