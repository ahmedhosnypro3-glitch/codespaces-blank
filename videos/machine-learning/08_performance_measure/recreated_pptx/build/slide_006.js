// slide_006 — "Accuracy" (08_performance_measure). 1px of the 960x540 original = 1pt.
// Rebuild attempt 2: fixes judge_attempt_1 findings — title unclipped (taller box,
// valign middle, no overlay band), left boxes PIL-measured to original extents,
// "Accuracy of ALL Classes" inside the calc box, maroon rounded enclosure around the
// formula, real wide braces via mathtext PNG (assets/eq_006.png), rotated "Actual"
// labels with correct w/h, no stray pen slash, footer bar y515-540.
// Geometry measured from unique_slides/slide_006.jpg with PIL; text verbatim from
// pool_run/image_analysis/slide_006_analysis.txt + analysis/reanalysis/slide_006_raw.json
// + sources/slide_006_research.md.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const DRED = "8B0000";
const GREEN_TXT = "1E9C17";
const CIRC_RED = "A00000";
const CIRC_GREEN = "0B843D";
const GREEN_CELL = "8CFF08";
const PEACH = "F7D4B4";
const BLUE = "222067";
const QBLUE = "0000CC";
const PALE_Y = "F7FBD8";
const PALE_C = "EAF9F6";
const GRAY_BOX = "C9C9CB";
const BADGE = "FFF9C4";
const INK = "333333";
const BLACK = "000000";
const FONT = "Arial";

const px = (v) => v / 72;
const s = pptx.addSlide();
s.background = { color: BG };

// ---------- house chrome (root AGENTS.md 2026-10-09, overrides everything) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("6", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText("Accuracy", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.7, align: "center", valign: "middle",
  fontSize: 48, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- helpers ----------
function rect(x0, y0, x1, y1, fill, lineColor, lineW) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: fill ? { color: fill } : { type: "none" },
    line: lineColor ? { color: lineColor, width: lineW || 1.25 } : { type: "none" },
  });
}
function hline(x0, x1, y, color, w) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y), w: px(x1 - x0), h: 0, line: { color: color || BLACK, width: w || 1 },
  });
}
function vline(x, y0, y1, color, w) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x), y: px(y0), w: 0, h: px(y1 - y0), line: { color: color || BLACK, width: w || 1 },
  });
}
function text(str, x0, y0, x1, y1, size, color, opts) {
  const o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "center", valign: "middle", fontSize: size, bold: true,
    color: color, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(str, o);
}
function rtext(parts, x0, y0, x1, y1, size, opts) {
  const o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "left", valign: "middle", fontSize: size, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(parts.map(([t, c, b, i]) => ({
    text: t, options: { color: c, bold: b !== false, italic: !!i },
  })), o);
}

// ---------- gray definition box (x72-655, y111-177) ----------
rect(72, 111, 655, 177, GRAY_BOX, null);
text("Correctly Classified (Positive & Negative)", 72, 116, 655, 137, 16, BLACK);
hline(81, 644, 141, RED, 2);
text("Total Number of Samples", 72, 148, 655, 173, 16, BLACK);

// ---------- Meaning box (pale yellow, x68-664, y177-225) ----------
rect(68, 177, 664, 225, PALE_Y, null);
text("Meaning", 70, 180, 170, 200, 16, RED, { align: "left" });
rtext([
  ["How Accurate is the Classification (for Both ", BLACK],
  ["Positive", QBLUE],
  [" and ", BLACK],
  ["Negative", QBLUE],
  [" Classes)", BLACK],
], 70, 201, 660, 221, 14, { align: "left" });

// ---------- equation box (white, blue border, x63-445 y232-370) ----------
rect(63, 232, 445, 370, "FFFFFF", BLUE, 2);
// maroon rounded enclosure around the whole formula
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: px(70), y: px(238), w: px(368), h: px(126),
  fill: { type: "none" }, line: { color: DRED, width: 1.25 },
});
// composed mathtext equation PNG (600 dpi, exact size) with wide green braces
s.addImage({
  path: "build/assets/eq_006.png",
  x: px(88), y: px(238), w: 3.44, h: 1.555,
});

// ---------- calculation box (one pale box x73-536 y372-430) ----------
rect(73, 372, 536, 430, PALE_C, null);
text("Accuracy= (18+60)/(18+12+60+10)", 84, 377, 372, 397, 12, BLACK, { align: "left" });
rtext([["= 78/100 = ", BLACK], ["78%", RED]], 84, 399, 372, 420, 12, { align: "left" });
text("Accuracy of", 392, 378, 530, 398, 12, RED, { italic: true });
text("ALL Classes", 392, 400, 530, 424, 12, RED, { italic: true });

// ---------- questions / conclusion box (pale yellow, x75-516 y429-510) ----------
rect(75, 429, 516, 510, PALE_Y, null);
text("What About Precision of Positive Class ONLY  Results?", 85, 435, 510, 456, 13, QBLUE, { align: "left" });
text("What About Recall % of Positive Samples ?", 85, 459, 510, 480, 13, QBLUE, { align: "left" });
text("Conclusion: Accuracy is Good but Not Sufficient", 85, 484, 510, 505, 13, RED, { align: "left" });

// ---------- confusion matrix helper ----------
function matrix(px0, py0, px1, py1, gx0, cx, gx1, hy1, hy2, gy1, cells) {
  rect(px0, py0, px1, py1, "FFFFFF", BLUE, 1.5);
  const mid = (hy2 + gy1) / 2;
  text("Predicted as", cx, py0 + 3, gx1, hy1, 11, RED);
  text("P", cx, hy1, (cx + gx1) / 2, hy2, 13, BLACK);
  text("N", (cx + gx1) / 2, hy1, gx1, hy2, 13, BLACK);
  text("P", gx0, hy2, cx, mid, 13, BLACK);
  text("N", gx0, mid, cx, gy1, 13, BLACK);
  // rotated "Actual": box w = vertical span, h = strip thickness (pre-rotation)
  s.addText("Actual", {
    x: px(px0 + 4), y: px(hy1), w: px(gy1 - hy1), h: px(gx0 - px0 - 8),
    align: "center", valign: "middle", fontSize: 11, bold: true, color: RED,
    fontFace: FONT, margin: 0, rotate: 270,
  });
  cells.forEach(([x0, y0, x1, y1, fill]) => { if (fill) rect(x0, y0, x1, y1, fill, null); });
  hline(cx, gx1, hy1, BLACK, 1);
  hline(gx0, gx1, hy2, BLACK, 1);
  hline(gx0, gx1, mid, BLACK, 1);
  hline(gx0, gx1, gy1, BLACK, 1);
  vline(gx0, hy1, gy1, BLACK, 1);
  vline(cx, hy1, gy1, BLACK, 1);
  vline((cx + gx1) / 2, hy1, gy1, BLACK, 1);
  vline(gx1, hy1, gy1, BLACK, 1);
  cells.forEach(([x0, y0, x1, y1, , label]) => { if (label) text(label, x0, y0, x1, y1, 13, BLACK); });
}

// matrix 1 (symbolic): panel x673-867 y52-168
matrix(673, 52, 867, 168, 698, 738, 845, 73, 98, 151, [
  [738, 98, 791, 125, GREEN_CELL, "TP"],
  [791, 98, 845, 125, null, "FN"],
  [738, 125, 791, 151, null, "FP"],
  [791, 125, 845, 151, GREEN_CELL, "TN"],
]);

// matrix 2 (numeric): panel x673-867 y167-291
matrix(673, 167, 867, 291, 704, 746, 856, 191, 220, 283, [
  [746, 220, 800, 252, GREEN_CELL, "18"],
  [800, 220, 856, 252, PEACH, "12"],
  [746, 252, 800, 283, PEACH, "10"],
  [800, 252, 856, 283, GREEN_CELL, "60"],
]);
// blue rounded outline around the four numeric cells
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: px(744), y: px(218), w: px(114), h: px(67),
  fill: { type: "none" }, line: { color: BLUE, width: 1.5 },
});

// ---------- Positive/Negative tree (red border box x536-881 y291-502) ----------
rect(536, 291, 881, 502, "FFFFFF", RED, 1.5);
text("Positive", 556, 294, 680, 320, 16, RED);
text("Negative", 736, 294, 856, 320, 16, CIRC_GREEN);

// airplane icons above the parent circles
function plane(cx, cy, bodyColor) {
  const w = 56, h = 30;
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - w / 2), y: px(cy - 5), w: px(w), h: px(10),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - 9), y: px(cy + 2), w: px(18), h: px(16),
    fill: { color: bodyColor }, line: { color: bodyColor }, rotate: 180,
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - w / 2 + 3), y: px(cy - 12), w: px(13), h: px(9),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx + w / 2 - 9), y: px(cy - 3), w: px(6), h: px(6),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
}
plane(618, 352, "808080");
plane(800, 352, "C0C0C0");

// blue branch arrows with heads
function arrow(x0, y0, x1, y1) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: BLUE, width: 1.5, endArrowType: "triangle" },
  });
}
arrow(612, 406, 580, 442);
arrow(624, 406, 654, 442);
arrow(794, 406, 762, 442);
arrow(806, 406, 838, 442);

// tree nodes
function node(cx, cy, d, fill, label) {
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill },
  });
  text(label, cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2, 13, "FFFFFF");
}
node(618, 393, 32, CIRC_RED, "30");
node(800, 393, 32, CIRC_GREEN, "70");
node(573, 457, 32, CIRC_RED, "18");
node(661, 457, 32, CIRC_GREEN, "12");
node(755, 457, 32, CIRC_GREEN, "60");
node(845, 457, 32, CIRC_RED, "10");
// leaf labels
text("TP", 558, 476, 588, 496, 12, RED);
text("FN", 646, 476, 676, 496, 12, CIRC_GREEN);
text("TN", 740, 476, 770, 496, 12, CIRC_GREEN);
text("FP", 830, 476, 860, 496, 12, RED);

// ---------- black footer bar (bottom edge, over the frame line like the original) ----------
rect(38, 515, 922, 540, BLACK, null);

pptx.writeFile({
  fileName: "slide_006_recreated.pptx",
})
  .then(() => console.log("slide_006_recreated.pptx done"))
  .catch((e) => console.error("Error:", e));
