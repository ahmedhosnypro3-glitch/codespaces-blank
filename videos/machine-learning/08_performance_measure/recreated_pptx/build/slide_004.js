// Slide 004 — Radar Shooting of Positive Target (Enemy plane)
// Rebuild v2 from PIL measurements of unique_slides/slide_004.jpg (960x540 px, 1px = 1pt = 1/72 in).
// Authoritative content: pool_run/image_analysis/slide_004_analysis.txt + analysis/reanalysis/slide_004_raw.json.
// Frame notes: original's own outer red border (x58-902 y42-517) is replaced by house chrome per root
// AGENTS.md; black bar below y=517 is a video letterbox artifact and is omitted.
// v2 fixes vs v1 (judge_attempt_6 FAIL): closed tan panel around left diagram (was open gray lines,
// right edge missing); matrix boxes are BLUE-bordered single boxes x669-872 (no gray strip / extra
// divider); inner matrix grid lines dark red; tree edges navy with solid colored heads; plane edges
// red/green; title underlines "Positive" (measured underline x389-470 = the word Positive only).
const pptxgenpkg = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const FRAME = "C00000";
const BADGE = "FFF9C4";
const INK = "333333";
const BLACK = "000000";
const RED = "C0392B";        // red text (headers, title, Actual labels)
const CIRC_RED = "A00000";   // red circles (measured core #9F0000)
const CIRC_GREEN = "0B843D"; // green circles (measured core #09873E)
const GREEN_TXT = "1E8449";  // "Negative" header (measured #2C774C)
const CELL_GREEN = "86FF08"; // TP/TN/18/60 cell fill (measured ~#86FF00)
const PURPLE = "8E44AD";     // Correctly Classified arrows/labels (measured #7F2C86)
const NAVY = "000061";       // Confusion Matrix caption (measured core #000061)
const MBLUE = "110980";      // matrix border + "Predicted as" (measured core #110980)
const GRID_RED = "881A27";   // matrix inner grid lines (measured core #881A27)
const TAN = "886D50";        // left diagram panel (measured core #886D50)
const EDGE = "1A0F66";       // tree connector lines (measured core ~#190F65)
const PLANE_RED = "9F0000";  // plane -> 30 edge (measured #9F0000)
const PLANE_GREEN = "09873E";// plane -> 70 edge (measured #09873E)
const BLUE = "312886";       // "Model Output" vertical label
const WHITE = "FFFFFF";
const FONT = "Arial";

const ASSETS = path.join(__dirname, "assets");
const PLANE_POS = path.join(ASSETS, "slide004_plane_positive.png"); // 89x66 px at abs origin (308,132)
const PLANE_NEG = path.join(ASSETS, "slide004_plane_negative.png"); // 93x62 px at abs origin (510,136)

const px = (v) => v / 72;
const s = pptx.addSlide();
s.background = { color: BG };

// ---------- house chrome (root AGENTS.md 2026-10-09) ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("4", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Radar Shooting of ", options: { fontSize: 21, bold: true, color: RED, fontFace: FONT } },
  { text: "Positive", options: { fontSize: 21, bold: true, color: RED, fontFace: FONT, underline: true } },
  { text: " Target (Enemy plane)", options: { fontSize: 21, bold: true, color: RED, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle", margin: 0,
});

// ---------- helpers ----------
function rect(x0, y0, x1, y1, fill, lineColor, lineW) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: fill },
    line: lineColor ? { color: lineColor, width: lineW || 1.25 } : { type: "none" },
  });
}
function hline(x0, x1, y, color, w) {
  s.addShape(pptx.shapes.LINE, { x: px(x0), y: px(y), w: px(x1 - x0), h: 0, line: { color: color || BLACK, width: w || 1 } });
}
function vline(x, y0, y1, color, w) {
  s.addShape(pptx.shapes.LINE, { x: px(x), y: px(y0), w: 0, h: px(y1 - y0), line: { color: color || BLACK, width: w || 1 } });
}
function diag(x0, y0, x1, y1, color, w) {
  s.addShape(pptx.shapes.LINE, { x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0), line: { color: color, width: w || 1.5 } });
}
function text(str, x0, y0, x1, y1, size, color, opts) {
  const o = Object.assign({
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    align: "center", valign: "middle", fontSize: size, bold: true,
    color: color, fontFace: FONT, margin: 0,
  }, opts || {});
  s.addText(str, o);
}
function node(cx, cy, d, fill, label) {
  s.addShape(pptx.shapes.OVAL, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill },
  });
  text(label, cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2, 13, WHITE);
}
// solid down-pointing arrowhead at (cx,cy) (tip at bottom)
function downHead(cx, cy, fill) {
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - 5), y: px(cy - 8), w: px(10), h: px(8),
    fill: { color: fill }, line: { color: fill, width: 1 }, flipV: true,
  });
}

// ---------- left diagram: CLOSED tan panel x68-648 y93-435 + mid divider y250 ----------
// PIL on the original y435: bottom rule runs x69-261, x277-474, x491-647 — gaps only where
// the two purple callout arrows cross (x262-276, x475-490).
// PIL on the original: a vertical label-strip rule exists at x98-99 (color ~#A58D7A),
// y93-433, broken only where the y250 divider crosses; rotated labels sit left of it.
rect(68, 93, 648, 435, BG, TAN, 1.5);
vline(98, 93, 249, "A58D7A", 1.5);
vline(98, 252, 435, "A58D7A", 1.5);
hline(68, 648, 250, TAN, 1.5);
hline(68, 261, 435, TAN, 1.5);
hline(277, 474, 435, TAN, 1.5);
hline(491, 648, 435, TAN, 1.5);

// rotated row labels in the narrow left column (x 68-108)
function vlabel(str, cx, cy, len, color) {
  s.addText(str, {
    x: px(cx - len / 2), y: px(cy - 10), w: px(len), h: px(20),
    align: "center", valign: "middle", fontSize: 13, bold: true, color: color,
    fontFace: FONT, margin: 0, rotate: 270,
  });
}
vlabel("Actual", 85, 171, 70, RED);
vlabel("Model Output", 85, 342, 115, BLUE);

// ---------- column headers ----------
text("Positive", 300, 102, 390, 128, 18, RED);
text("Negative", 505, 102, 595, 128, 18, GREEN_TXT);

// ---------- plane icons (cropped from the original frame, white->transparent) ----------
s.addImage({ path: PLANE_POS, x: px(308), y: px(132), w: px(89), h: px(66) });
s.addImage({ path: PLANE_NEG, x: px(510), y: px(136), w: px(93), h: px(62) });

// ---------- connectors ----------
// plane -> top circles: red edge to 30, green edge to 70
diag(345, 196, 340, 203, PLANE_RED, 1.5);
diag(552, 196, 545, 202, PLANE_GREEN, 1.5);
// tree edges: navy lines with solid heads colored like the target circle
diag(340, 233, 289, 264, EDGE, 1);   // 30 -> 18
diag(340, 233, 387, 264, EDGE, 1);   // 30 -> 12
diag(544, 233, 492, 264, EDGE, 1);   // 70 -> 60
diag(544, 233, 597, 264, EDGE, 1);   // 70 -> 10
// PIL on the original: arrowheads are the same navy as the shafts (re-check at y261-270:
// all four heads show navy/blue pixels, no red/green)
downHead(289, 268, EDGE);
downHead(387, 268, EDGE);
downHead(492, 268, EDGE);
downHead(597, 268, EDGE);

// ---------- tree nodes ----------
node(340, 216, 34, CIRC_RED, "30");
node(544, 215, 38, CIRC_GREEN, "70");
node(289, 289, 34, CIRC_RED, "18");
node(387, 290, 38, CIRC_GREEN, "12");
node(492, 290, 36, CIRC_GREEN, "60");
node(597, 289, 34, CIRC_RED, "10");

// ---------- bottom label rows (measured y-centers: 346 / 378 / 411, gaps 32/33) ----------
text("Classified as:", 109, 338, 200, 354, 12, INK, { align: "left", bold: false });
text("And classification is:", 111, 370, 240, 386, 12, INK, { align: "left", bold: false });
// PIL on the original: row1/row2 value words are BLACK-cored (black px 2-3x the red JPEG
// fringe); only the TP/FN/TN/FP row is red-cored (0 black px)
const clsCols = [286, 394, 500, 610];
["Positive", "Negative", "Negative", "Positive"].forEach((w, i) =>
  text(w, clsCols[i] - 45, 338, clsCols[i] + 45, 354, 12, INK, { bold: false }));
const tfCols = [276, 383, 487, 600];
["True", "False", "True", "False"].forEach((w, i) =>
  text(w, tfCols[i] - 30, 370, tfCols[i] + 30, 386, 12, INK, { bold: false }));
const tpCols = [271, 375, 482, 593];
["TP", "FN", "TN", "FP"].forEach((w, i) =>
  text(w, tpCols[i] - 30, 403, tpCols[i] + 30, 419, 13, RED));

// ---------- Correctly Classified purple up-arrows + labels (hollow heads) ----------
// PIL on the original: shafts are long verticals x~268 / x~482 spanning y419-458 (through the
// gaps in the bottom rule), hollow heads at top; captions sit LEFT of their arrows
// (caption1 x137-255, caption2 x354-478, text y446-455)
function upArrow(cx) {
  // hollow shaft: two vertical lines at cx-5 / cx+5, y428-458 (original pixels)
  vline(cx - 5, 428, 458, PURPLE, 1.5);
  vline(cx + 5, 428, 458, PURPLE, 1.5);
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - 7), y: px(417), w: px(14), h: px(11),
    line: { color: PURPLE, width: 1.5 },
  });
}
upArrow(268);
upArrow(482);
text("Correctly Classified", 126, 440, 266, 458, 12, PURPLE, { bold: false });
text("Correctly Classified", 346, 440, 486, 458, 12, PURPLE, { bold: false });

// ---------- right confusion matrices: single blue-bordered boxes x669-872 ----------
// m1 y172-301, m2 y347-476; inner grid dark red at x708/750/804/860 and y199/229/261/291 (m1), y374/403/435/466 (m2)
function matrix(y0, y1, h1, h2, h3, h4, cells) {
  // blue border box, white fill
  rect(669, y0, 872, y1, WHITE, MBLUE, 3);
  // inner grid: header separator only over the data columns; label-column divider
  // only across the two data rows (corner cell stays open), per original pixels
  hline(750, 870, h1, GRID_RED, 1.25);
  [750, 804, 860].forEach((x) => vline(x, h1, y1 - 2, GRID_RED, 1.25));
  vline(708, h2, y1 - 2, GRID_RED, 1.25);
  [h2, h3, h4].forEach((y) => hline(708, 870, y, GRID_RED, 1.25));
  // "Predicted as" (dark red) in the top band, centered over the two data columns
  text("Predicted as", 750, y0 + 4, 870, h1 - 2, 13, "881A27");
  // column headers P / N
  text("P", 750, h1, 804, h2, 13, BLACK);
  text("N", 804, h1, 860, h2, 13, BLACK);
  // row labels P / N in the label column
  text("P", 708, h2, 750, h3, 13, BLACK);
  text("N", 708, h3, 750, h4, 13, BLACK);
  // rotated Actual in the leftmost strip
  s.addText("Actual", {
    x: px(690 - 30), y: px((y0 + y1) / 2 + 8), w: px(60), h: px(18),
    align: "center", valign: "middle", fontSize: 13, bold: true, color: "8B1A2B",
    fontFace: FONT, margin: 0, rotate: 270,
  });
  // cell fills + labels: cells = [x0,y0,x1,y1,fill,label]
  cells.forEach(([x0, c0, x1, c1, fill, label]) => {
    if (fill) rect(x0, c0, x1, c1, fill, null);
    if (label) text(label, x0, c0, x1, c1, 13, BLACK);
  });
}

matrix(172, 301, 199, 229, 261, 291, [
  [750, 229, 804, 261, CELL_GREEN, "TP"],
  [804, 229, 860, 261, null, "FN"],
  [750, 261, 804, 291, null, "FP"],
  [804, 261, 860, 291, CELL_GREEN, "TN"],
]);

text("Confusion Matrix", 707, 308, 861, 328, 16, NAVY);

matrix(347, 476, 374, 403, 435, 466, [
  [750, 403, 804, 435, CELL_GREEN, "18"],
  [804, 403, 860, 435, null, "12"],
  [750, 435, 804, 466, null, "10"],
  [804, 435, 860, 466, CELL_GREEN, "60"],
]);

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_004_recreated.pptx";
pptx.writeFile({ fileName: out })
  .then(() => console.log("wrote", out))
  .catch((e) => { console.error(e); process.exit(1); });
