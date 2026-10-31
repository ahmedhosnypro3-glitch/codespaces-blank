const pptxgenpkg = require("pptxgenjs");

const NS = "videos/machine-learning/08_performance_measure";
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";        // title, tree border/panel3, red text accents, grid lines
const CIRC_RED = "A00000";   // red tree circles (measured #A0000A)
const CIRC_GREEN = "1E8640"; // green tree circles (measured #1A8641)
const GREEN = "86FF08";      // TP/TN/18/60 cell fill (measured #87FF0A)
const FN_FILL = "F8E3C8";    // FN / 12 cell + Total-Positive box fill (measured peach)
const FP_FILL = "F9FFC3";    // FP / 10 cell + Total-Negative box fill (measured pale yellow)
const BLUE = "3C3289";       // matrix panel borders (measured dark blue-violet)
const CONN = "2B2271";       // tree connector lines (measured dark blue)
const DEF_FILL = "D6FDF6";   // definition box fill (measured pale cyan)
const DEF_LINE = "404397";   // definition box border (measured)
const BADGE = "FFF9C4";
const INK = "333333";
const BLACK = "000000";
const WHITE = "FFFFFF";
const FONT = "Arial";

const px = (v) => v / 72;
const s = pptx.addSlide();
s.background = { color: BG };

// ---------- house chrome (root AGENTS.md 2026-10-09, overrides spec) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("5", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText(
  [
    { text: "Radar Shooting of " },
    { text: "Positive Target", options: { underline: true } },
    { text: " (Enemy plane)" },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle",
    fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
  }
);

// ---------- helpers ----------
function rect(x0, y0, x1, y1, fill, lineColor, lineW) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: fill },
    line: lineColor ? { color: lineColor, width: lineW || 1.25 } : { type: "none" },
  });
}
function rrect(x0, y0, x1, y1, fill) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: fill }, line: { color: fill, width: 0.75 },
  });
}
function hline(x0, x1, y, color, w) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y), w: px(x1 - x0), h: 0, line: { color: color || RED, width: w || 1 },
  });
}
function vline(x, y0, y1, color, w) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x), y: px(y0), w: 0, h: px(y1 - y0), line: { color: color || RED, width: w || 1 },
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
  s.addText(parts.map(([t, c, b]) => ({ text: t, options: { color: c, bold: b !== false } })), o);
}
// rotated label: declared in unrotated frame, spun 270 about its center —
// w must exceed the word length so the text never wraps
function vlabel(str, cx, cy, size, color) {
  const w = 110, h = size + 10;
  s.addText(str, {
    x: px(cx - w / 2), y: px(cy - h / 2), w: px(w), h: px(h),
    align: "center", valign: "middle", fontSize: size, bold: true, color: color,
    fontFace: FONT, margin: 0, rotate: 270,
  });
}

// confusion matrix: panel + label strip + header + 2x2 cells
// panel px0,py0..px1,py1; grid gx0..gx1 with col split cx; hlines hy1,hy2,gy1 (top of grid = gy0)
function matrix(px0, py0, px1, py1, gx0, gy0, cx, gx1, hy1, hy2, gy1, cells, vlines) {
  rect(px0, py0, px1, py1, WHITE, BLUE, 1.5);
  text("Predicted as", cx, py0 + 2, gx1, hy1 - 1, 13, RED, { bold: true });
  text("P", cx, hy1, (cx + gx1) / 2, hy2, 13, BLACK);
  text("N", (cx + gx1) / 2, hy1, gx1, hy2, 13, BLACK);
  text("P", gx0 + 30, hy2, cx, (hy2 + gy1) / 2, 13, BLACK);
  text("N", gx0 + 30, (hy2 + gy1) / 2, cx, gy1, 13, BLACK);
  vlabel("Actual", (px0 + gx0) / 2 + 4, (hy2 + gy1) / 2, 13, RED);
  cells.forEach(([x0, y0, x1, y1, fill]) => {
    if (fill) rect(x0, y0, x1, y1, fill, null);
  });
  hline(gx0, gx1, hy1, RED, 1);
  hline(gx0, gx1, hy2, RED, 1);
  hline(gx0, gx1, (hy2 + gy1) / 2, RED, 1);
  hline(gx0, gx1, gy1, RED, 1);
  (vlines || [gx0, cx, (cx + gx1) / 2, gx1]).forEach((vx) => vline(vx, hy1, gy1, RED, 1));
  cells.forEach(([x0, y0, x1, y1, , label]) => {
    if (label) text(label, x0, y0, x1, y1, 13, BLACK);
  });
}

// ---------- panel 1: top-left generic matrix (FN/FP white per frame) ----------
matrix(76, 88, 278, 216, 110, 112, 152, 263, 112, 142, 205, [
  [152, 142, 206, 174, GREEN, "TP"],
  [206, 142, 263, 174, null, "FN"],
  [152, 174, 206, 205, null, "FP"],
  [206, 174, 263, 205, GREEN, "TN"],
]);

// ---------- panel 2: bottom-left big matrix + totals in highlight boxes ----------
matrix(67, 240, 460, 398, 94, 270, 145, 280, 270, 306, 386, [
  [145, 306, 211, 346, GREEN, "TP"],
  [211, 306, 280, 346, FN_FILL, "FN"],
  [145, 346, 211, 385, FP_FILL, "FP"],
  [211, 346, 280, 385, GREEN, "TN"],
], [145, 211, 280]);
rrect(285, 309, 455, 343, FN_FILL);
rtext([["Total Positive = TP+FN", RED]], 291, 309, 450, 343, 12, { align: "left" });
rrect(285, 351, 455, 383, FP_FILL);
rtext([["Total Negative = FP+TN", RED]], 291, 351, 450, 383, 12, { align: "left" });

// ---------- definition box ----------
rect(66, 406, 460, 451, DEF_FILL, DEF_LINE, 1.25);
rtext([
  ["FN = ", BLACK], ["Actually Positive", RED], [", Miss-classified as ", BLACK], ["Negative", RED],
], 78, 412, 456, 429, 12, { align: "left" });
rtext([
  ["FP = ", BLACK], ["Actually Negative", RED], [", Miss-classified as ", BLACK], ["Positive", RED],
], 78, 431, 456, 448, 12, { align: "left" });

// ---------- panel 3: top-right radar tree ----------
rect(536, 104, 882, 315, WHITE, RED, 1.5);
text("Positive", 588, 108, 670, 126, 14, RED);
text("Negative", 772, 108, 856, 128, 14, CIRC_GREEN);
// dashed Actual/Predicted divider
s.addShape(pptx.shapes.LINE, {
  x: px(545), y: px(234), w: px(330), h: 0,
  line: { color: "808080", width: 1, dashType: "dash" },
});
text("Actual", 462, 200, 530, 216, 12, BLUE, { align: "center" });
text("Predicted", 462, 263, 531, 279, 12, BLUE, { align: "center" });

// hand-drawn plane sketches cropped from the original frame (960x540, 1px=1pt)
s.addImage({ path: NS + "/recreated_pptx/build/assets/plane_red.png", x: px(584), y: px(130), w: px(94), h: px(54) });
s.addImage({ path: NS + "/recreated_pptx/build/assets/plane_green.png", x: px(760), y: px(122), w: px(96), h: px(62) });

// plain branch connectors (no arrowheads), dark blue per frame
function conn(x0, y0, x1, y1) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: CONN, width: 1.5 },
  });
}
conn(628, 184, 620, 192);
conn(792, 184, 800, 192);
conn(618, 220, 576, 255);
conn(618, 220, 658, 255);
conn(799, 220, 758, 255);
conn(799, 220, 842, 255);

// tree nodes: circles with white numerals — 30 splits to 18 (left, red) / 12 (right, green);
// 70 splits to 60 (left, green) / 10 (right, red)
function node(cx, cy, d, fill, label) {
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill },
  });
  text(label, cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2, 13, WHITE);
}
node(618, 206, 31, CIRC_RED, "30");
node(799, 206, 31, CIRC_GREEN, "70");
node(573, 269, 31, CIRC_RED, "18");
node(661, 269, 31, CIRC_GREEN, "12");
node(755, 269, 31, CIRC_GREEN, "60");
node(845, 269, 31, CIRC_RED, "10");

// ---------- panel 4: bottom-right numeric matrix + totals in highlight boxes ----------
matrix(488, 335, 882, 471, 531, 365, 572, 683, 365, 394, 458, [
  [572, 394, 627, 427, GREEN, "18"],
  [627, 394, 683, 427, FN_FILL, "12"],
  [572, 427, 627, 458, FP_FILL, "10"],
  [627, 427, 683, 458, GREEN, "60"],
]);
rrect(688, 397, 870, 425, FN_FILL);
rtext([["Total Positive = 18+12=30", RED]], 694, 397, 866, 425, 12, { align: "left" });
rrect(688, 430, 870, 455, FP_FILL);
rtext([["Total Negative = 10+60=70", RED]], 694, 430, 866, 455, 12, { align: "left" });

pptx.writeFile({
  fileName: NS + "/recreated_pptx/slide_005_recreated.pptx",
})
  .then(() => console.log("slide_005_recreated.pptx done"))
  .catch((e) => console.error("Error:", e));
