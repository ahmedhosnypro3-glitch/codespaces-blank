const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";        // title, tree border, red text accents
const CIRC_RED = "A00000";   // red tree circles
const CIRC_GREEN = "0B843D"; // green tree circles
const GREEN = "86FF08";      // TP/TN/18/60 cell fill (measured ~#86FF08)
const FN_FILL = "F8E3C8";    // FN / 12 cell fill (measured peach)
const FP_FILL = "F9FFC3";    // FP / 10 cell fill (measured pale yellow)
const PINK_FILL = "F4CCCC";  // small-matrix FN/FP fill (measured light pink)
const BLUE = "3C3289";       // matrix panel borders (measured dark blue-violet)
const DEF_FILL = "DEFFFF";   // definition box fill (measured pale cyan)
const DEF_LINE = "97ACED";   // definition box border (measured light blue)
const BADGE = "FFF9C4";
const INK = "333333";
const BLACK = "000000";
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
    { text: "Positive", options: { underline: true } },
    { text: " Target (Enemy plane)" },
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
  o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "center", valign: "middle", fontSize: size, bold: true,
    color: color, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(str, o);
}
function rtext(parts, x0, y0, x1, y1, size, opts) {
  o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "left", valign: "middle", fontSize: size, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(parts.map(([t, c, b]) => ({ text: t, options: { color: c, bold: b !== false } })), o);
}

// generic confusion matrix: panel + label col + header rows + 2x2 cells
// grid box: gx0..gx1 (incl. label col), gy0..gy1; col split at cx; header rows hy1 (below "Predicted as"), hy2 (below P/N)
function matrix(px0, py0, px1, py1, gx0, gy0, cx, gx1, hy1, hy2, gy1, cells) {
  rect(px0, py0, px1, py1, "FFFFFF", BLUE, 1.5);
  // header band text
  text("Predicted as", cx, py0 + 2, gx1, hy1 - 1, 13, RED, { bold: true });
  // P / N column letters
  text("P", cx, hy1, (cx + gx1) / 2, hy2, 13, BLACK);
  text("N", (cx + gx1) / 2, hy1, gx1, hy2, 13, BLACK);
  // row letters
  text("P", gx0, hy2, cx, (hy2 + gy1) / 2, 13, BLACK);
  text("N", gx0, (hy2 + gy1) / 2, cx, gy1, 13, BLACK);
  // rotated "Actual" in the label column strip left of gx0
  s.addText("Actual", {
    x: px(px0 + 2), y: px(hy1), w: px(gx0 - px0 - 4), h: px(gy1 - hy1),
    align: "center", valign: "middle", fontSize: 13, bold: true, color: RED,
    fontFace: FONT, margin: 0, rotate: 270,
  });
  // cell fills
  cells.forEach(([x0, y0, x1, y1, fill]) => {
    if (fill) rect(x0, y0, x1, y1, fill, null);
  });
  // grid lines
  hline(cx, gx1, hy1, BLACK, 1);
  hline(gx0, gx1, hy2, BLACK, 1);
  hline(gx0, gx1, (hy2 + gy1) / 2, BLACK, 1);
  hline(gx0, gx1, gy1, BLACK, 1);
  vline(gx0, hy1, gy1, BLACK, 1);
  vline(cx, hy1, gy1, BLACK, 1);
  vline((cx + gx1) / 2, hy1, gy1, BLACK, 1);
  vline(gx1, hy1, gy1, BLACK, 1);
  // cell labels
  cells.forEach(([x0, y0, x1, y1, , label]) => {
    if (label) text(label, x0, y0, x1, y1, 13, BLACK);
  });
}

// ---------- panel 1: top-left generic matrix ----------
// panel x76-278 y88-216; label col strip x76-110; grid gx0=110 gx1=263; cx=152; header hy1=142 hy2=174? measured rows: hdr 112-142 (P/N letters), rows 142-174, 174-205
matrix(76, 88, 278, 216, 110, 112, 152, 263, 112, 142, 205, [
  [152, 142, 206, 174, GREEN, "TP"],
  [206, 142, 263, 174, PINK_FILL, "FN"],
  [152, 174, 206, 205, PINK_FILL, "FP"],
  [206, 174, 263, 205, GREEN, "TN"],
]);
// "Predicted as" sits above grid inside panel top band (y97-107 over P/N cols)
// (matrix() already drew it in band py0..hy1 over cx..gx1)

// ---------- panel 2: bottom-left big matrix + totals ----------
// panel x67-460 y240-398; grid gx0=94 gx1=280; cx=145; header band 240-270, letters 270-306, rows 306-346, 346-386
matrix(67, 240, 460, 398, 94, 270, 145, 280, 270, 306, 386, [
  [145, 306, 210, 346, GREEN, "TP"],
  [210, 306, 280, 346, FN_FILL, "FN"],
  [145, 346, 210, 386, FP_FILL, "FP"],
  [210, 346, 280, 386, GREEN, "TN"],
]);
rtext([["Total Positive = TP+FN", RED]], 288, 318, 380, 334, 12, { align: "left" });
rtext([["Total Negative = FP+TN", RED]], 288, 357, 385, 374, 12, { align: "left" });

// ---------- definition box ----------
rect(66, 406, 460, 451, DEF_FILL, DEF_LINE, 1.25);
rtext([
  ["FN = ", BLACK], ["Actually Positive", RED], [", Miss-classified as ", BLACK], ["Negative", RED],
], 78, 412, 456, 429, 12, { align: "left" });
rtext([
  ["FP = ", BLACK], ["Actually Negative", RED], [", Miss-classified as ", BLACK], ["Positive", RED],
], 78, 431, 456, 448, 12, { align: "left" });

// ---------- panel 3: top-right radar tree ----------
// panel x536-882 y104-315 (red border)
rect(536, 104, 882, 315, "FFFFFF", RED, 1.5);
text("Positive", 590, 110, 668, 127, 14, RED);
text("Negative", 740, 110, 822, 127, 14, CIRC_GREEN);
// dashed divider between Actual and Predicted levels
s.addShape(pptx.shapes.LINE, {
  x: px(545), y: px(245), w: px(330), h: 0,
  line: { color: "9AA0A6", width: 1, dashType: "dash" },
});
// level labels left of panel
text("Actual", 462, 200, 530, 216, 12, BLUE, { align: "center" });
text("Predicted", 462, 263, 531, 279, 12, BLUE, { align: "center" });

// airplane icons (simple side-view shapes)
function plane(cx, cy, bodyColor) {
  const w = 64, h = 34;
  // fuselage
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - w / 2), y: px(cy - 5), w: px(w), h: px(10),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  // main wing
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - 12), y: px(cy + 2), w: px(24), h: px(18),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
  // tail wing
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - w / 2 + 2), y: px(cy - 12), w: px(14), h: px(12),
    fill: { color: bodyColor }, line: { color: bodyColor },
  });
}
plane(630, 152, CIRC_RED);   // enemy plane under Positive
plane(790, 152, CIRC_GREEN); // friendly plane under Negative

// connectors: plane -> 30/70 -> leaves
function arrow(x0, y0, x1, y1, color) {
  s.addShape(pptx.shapes.LINE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    line: { color: color, width: 1.5 },
  });
}
arrow(630, 168, 619, 191, CIRC_RED);
arrow(790, 168, 799, 191, CIRC_GREEN);
arrow(612, 221, 580, 254, CIRC_RED);
arrow(626, 221, 654, 254, CIRC_GREEN);
arrow(792, 221, 762, 254, CIRC_GREEN);
arrow(806, 221, 838, 254, CIRC_RED);

// tree nodes: circles with white numerals
function node(cx, cy, d, fill, label) {
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill },
  });
  text(label, cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2, 13, "FFFFFF");
}
node(619, 206, 33, CIRC_RED, "30");
node(799, 206, 33, CIRC_GREEN, "70");
node(573, 269, 33, CIRC_RED, "12");
node(661, 269, 33, CIRC_GREEN, "18");
node(755, 269, 33, CIRC_GREEN, "60");
node(845, 269, 33, CIRC_RED, "10");

// ---------- panel 4: bottom-right numeric matrix + totals ----------
// panel x488-882 y335-471; grid gx0=531 gx1=683; cx=572; header band 335-365, letters 365-394, rows 394-427, 427-458
matrix(488, 335, 882, 471, 531, 365, 572, 683, 365, 394, 458, [
  [572, 394, 627, 427, GREEN, "18"],
  [627, 394, 683, 427, FN_FILL, "12"],
  [572, 427, 627, 458, FP_FILL, "10"],
  [627, 427, 683, 458, GREEN, "60"],
]);
rtext([["Total Positive = 18+12=30", RED]], 690, 404, 860, 418, 12, { align: "left" });
rtext([["Total Negative = 10+60=70", RED]], 690, 436, 865, 449, 12, { align: "left" });

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_005_recreated.pptx",
})
  .then(() => console.log("slide_005_recreated.pptx done"))
  .catch((e) => console.error("Error:", e));
