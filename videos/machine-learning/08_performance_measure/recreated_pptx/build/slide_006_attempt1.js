// slide_006 — "Accuracy" (08_performance_measure). 1px of the 960x540 original = 1pt.
// Geometry measured from unique_slides/slide_006.jpg with PIL; text from the fresh
// image-analysis read (pool_run/image_analysis/slide_006_analysis.txt), cross-checked
// against analysis/reanalysis/slide_006_raw.json + sources/slide_006_research.md.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";        // title, frame, tree border, red accents (measured ~#BA0003)
const DRED = "8B0000";       // fraction terms (measured dark red ~#8F0000)
const GREEN_TXT = "1E9C17";  // green labels/braces (measured ~#1E9C17)
const CIRC_RED = "A00000";
const CIRC_GREEN = "0B843D";
const GREEN_CELL = "8CFF08"; // TP/TN/18/60 fills (measured ~#9FFF45 / #8CFF24)
const PEACH = "F7D4B4";      // 12/10 cells (measured ~#F7D4B4)
const BLUE = "222067";       // eq-box border + fraction bar + arrows (measured ~#222067)
const QBLUE = "0000CC";      // question lines (measured blue ink)
const PALE_Y = "F7FBD8";     // meaning + questions boxes (measured ~#F7FBD8)
const PALE_C = "DEFFFF";     // calc box (measured pale cyan)
const GRAY_BOX = "C8C8CA";   // definition box (measured ~#C8C8CA)
const PINK_BAND = "FCE4E4";  // header band (measured ~#FEE6E6)
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
  x: 0.6, y: 0.28, w: 12.13, h: 0.62, align: "center", valign: "middle",
  fontSize: 36, bold: true, color: RED, fontFace: FONT, margin: 0,
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
function dline(x0, y0, x1, y1, color, w) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0), line: { color: color, width: w || 1 },
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

// ---------- header band (pale pink) behind title ----------
rect(57, 44, 672, 110, PINK_BAND, null);

// ---------- gray definition box ----------
rect(61, 111, 671, 177, GRAY_BOX, null);
text("Correctly Classified (Positive & Negative)", 61, 118, 671, 137, 16, BLACK);
hline(80, 641, 140, RED, 2);
text("Total Number of Samples", 61, 150, 671, 172, 16, BLACK);

// ---------- Meaning box (pale yellow) ----------
rect(64, 177, 670, 225, PALE_Y, null);
text("Meaning", 67, 181, 160, 199, 16, RED, { align: "left" });
rtext([
  ["How Accurate is the Classification (for Both ", BLACK],
  ["Positive", QBLUE],
  [" and ", BLACK],
  ["Negative", QBLUE],
  [" Classes)", BLACK],
], 67, 201, 660, 219, 14, { align: "left" });

// ---------- equation box (white, blue border) ----------
rect(63, 232, 444, 370, "FFFFFF", BLUE, 2);
// green "Correctly Classified" label + brace over numerator
text("Correctly Classified", 188, 240, 300, 257, 12, GREEN_TXT, { italic: true });
text("}", 246, 252, 268, 284, 26, GREEN_TXT, { bold: false });
// Accuracy = (red bold) left of fraction
text("Accuracy =", 76, 283, 200, 302, 20, RED);
// numerator / blue fraction bar / denominator
text("TP + TN", 204, 282, 363, 300, 14, DRED);
hline(204, 363, 302, BLUE, 2.5);
text("TP + FP + TN + FN", 204, 306, 363, 326, 14, DRED);
// brace + "All Samples" under denominator
text("{", 246, 326, 268, 352, 26, GREEN_TXT, { bold: false });
text("All Samples", 264, 336, 364, 356, 12, GREEN_TXT, { italic: true });

// ---------- calculation box (pale cyan) ----------
rect(76, 372, 380, 427, PALE_C, null);
text("Accuracy= (18+60)/(18+12+60+10)", 84, 378, 376, 396, 12, BLACK, { align: "left", bold: true });
rtext([["= 78/100 = ", BLACK], ["78%", RED]], 84, 398, 376, 416, 12, { align: "left" });
// side note
text("Accuracy of ALL Classes", 535, 376, 640, 424, 12, RED, { italic: true });

// ---------- questions / conclusion box (pale yellow) ----------
rect(75, 429, 516, 510, PALE_Y, null);
text("What About Precision of Positive Class ONLY  Results?", 85, 438, 510, 459, 14, QBLUE, { align: "left" });
text("What About Recall % of Positive Samples ?", 85, 462, 510, 483, 14, QBLUE, { align: "left" });
text("Conclusion: Accuracy is Good but Not Sufficient", 85, 488, 510, 506, 14, RED, { align: "left" });

// ---------- confusion matrix helper ----------
function matrix(px0, py0, px1, py1, gx0, cx, gx1, hy1, hy2, gy1, cells) {
  rect(px0, py0, px1, py1, "FFFFFF", BLUE, 1.5);
  const mid = (hy2 + gy1) / 2;
  text("Predicted as", cx, py0 + 3, gx1, hy1, 11, RED);
  text("P", cx, hy1, (cx + gx1) / 2, hy2, 13, BLACK);
  text("N", (cx + gx1) / 2, hy1, gx1, hy2, 13, BLACK);
  text("P", gx0, hy2, cx, mid, 13, BLACK);
  text("N", gx0, mid, cx, gy1, 13, BLACK);
  s.addText("Actual", {
    x: px(px0 + 2), y: px(hy1), w: px(gx0 - px0 - 4), h: px(gy1 - hy1),
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

// matrix 1 (symbolic): panel x673-867 y52-168; label col 673-698; cells 738-791 / 791-845; rows 98-125 / 125-151
matrix(673, 52, 867, 168, 698, 738, 845, 73, 98, 151, [
  [738, 98, 791, 125, GREEN_CELL, "TP"],
  [791, 98, 845, 125, null, "FN"],
  [738, 125, 791, 151, null, "FP"],
  [791, 125, 845, 151, GREEN_CELL, "TN"],
]);

// matrix 2 (numeric): panel x673-867 y167-291; label col 673-704; cells 746-800 / 800-856; rows 220-252 / 252-283
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
// hand-drawn pen slash across the numeric matrix "N" header
dline(803, 219, 853, 193, "D2D82E", 2);

// ---------- Positive/Negative tree (red border box) ----------
rect(536, 291, 881, 502, "FFFFFF", RED, 1.5);
text("Positive", 556, 294, 680, 320, 16, RED);
text("Negative", 736, 294, 856, 320, 16, CIRC_GREEN);

// airplane icons above the parent circles
function plane(cx, cy, bodyColor) {
  const w = 56, h = 30;
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - w / 2), y: px(cy - 4), w: px(w), h: px(9),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - 10), y: px(cy + 3), w: px(20), h: px(15),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - w / 2 + 2), y: px(cy - 11), w: px(12), h: px(10),
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

// ---------- black footer bar (bottom edge, below house frame line) ----------
rect(38, 529, 921, 540, BLACK, null);

pptx.writeFile({
  fileName: "slide_006_recreated.pptx",
})
  .then(() => console.log("slide_006_recreated.pptx done"))
  .catch((e) => console.error("Error:", e));
