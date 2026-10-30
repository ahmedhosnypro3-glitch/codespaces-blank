// Slide 004 — Radar Shooting of Positive Target (Enemy plane)
// Rebuilt from PIL measurements of unique_slides/slide_004.jpg (960x540 px, 1px = 1pt = 1/72 in).
// Authoritative content: pool_run/image_analysis/slide_004_analysis.txt + analysis/reanalysis/slide_004_raw.json.
// Frame notes: original's own red border (x58-901 y43-515) is replaced by house chrome per root AGENTS.md;
// black bar below y=516 is a video letterbox artifact and is omitted.
const pptxgenpkg = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const FRAME = "C00000";
const BADGE = "FFF9C4";
const INK = "333333";
const BLACK = "000000";
const RED = "C0392B";        // red text (measured title/hdr ~#AE4C57, JPEG-darkened)
const CIRC_RED = "A00000";   // red circles (measured core #940000/#A00007)
const CIRC_GREEN = "0B843D"; // green circles (measured core #30834D/#0F8C3E)
const GREEN_TXT = "1E8449";  // "Negative" header (measured #3F865C)
const CELL_GREEN = "86FF08"; // TP/TN/18/60 cell fill (measured ~#86FF00)
const PURPLE = "8E44AD";     // Correctly Classified arrows/labels (measured #7C337F)
const NAVY = "00008B";       // Confusion Matrix caption (measured core #00005D)
const BLUE = "312886";       // "Model Output" vertical label (measured #312886)
const STRIP_BLUE = "110980"; // matrix label-strip divider (measured #110980)
const STRIP_GRAY = "E7E8EC"; // matrix label strip fill (measured #E7E8EC)
const TABLE_LINE = "808080"; // left table rules (measured ~#95744B olive-gray)
const CONN = "404040";       // tree connector lines
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
s.addText("Radar Shooting of Positive Target (Enemy plane)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
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

// ---------- left table rules ----------
hline(68, 901, 93, TABLE_LINE, 1);     // content top rule (full width)
vline(68, 93, 435, TABLE_LINE, 1);     // left edge / label column separator
hline(68, 600, 250, TABLE_LINE, 1);    // Actual | Model Output divider
hline(68, 600, 435, TABLE_LINE, 1);    // table bottom

// rotated row labels in the narrow left column (x 68-98)
s.addText("Actual", {
  x: px(70), y: px(136), w: px(30), h: px(92),
  align: "center", valign: "middle", fontSize: 13, bold: true, color: RED,
  fontFace: FONT, margin: 0, rotate: 270,
});
s.addText("Model Output", {
  x: px(70), y: px(277), w: px(30), h: px(120),
  align: "center", valign: "middle", fontSize: 13, bold: true, color: BLUE,
  fontFace: FONT, margin: 0, rotate: 270,
});

// ---------- column headers ----------
text("Positive", 305, 104, 385, 126, 16, RED);
text("Negative", 510, 104, 590, 126, 16, GREEN_TXT);

// ---------- plane icons (cropped from the original frame, white->transparent) ----------
s.addImage({ path: PLANE_POS, x: px(308), y: px(132), w: px(89), h: px(66) });
s.addImage({ path: PLANE_NEG, x: px(510), y: px(136), w: px(93), h: px(62) });

// ---------- connectors (draw before circles) ----------
diag(353, 196, 340, 200, CONN, 1.5);   // positive plane -> 30
diag(556, 196, 544, 199, CONN, 1.5);   // negative plane -> 70
diag(340, 233, 289, 272, CONN, 1.5);   // 30 -> 18
diag(340, 233, 387, 272, CONN, 1.5);   // 30 -> 12
diag(544, 233, 492, 272, CONN, 1.5);   // 70 -> 60
diag(544, 233, 597, 272, CONN, 1.5);   // 70 -> 10

// ---------- tree nodes ----------
node(340, 216, 34, CIRC_RED, "30");
node(544, 215, 38, CIRC_GREEN, "70");
node(289, 289, 34, CIRC_RED, "18");
node(387, 290, 38, CIRC_GREEN, "12");
node(492, 290, 36, CIRC_GREEN, "60");
node(597, 289, 34, CIRC_RED, "10");

// ---------- bottom label rows ----------
text("Classified as:", 110, 340, 200, 352, 12, INK, { align: "left", bold: false });
text("And classification is:", 110, 372, 232, 384, 12, INK, { align: "left", bold: false });
const cols = [289, 387, 492, 597];
["Positive", "Negative", "Negative", "Positive"].forEach((w, i) =>
  text(w, cols[i] - 50, 340, cols[i] + 50, 352, 12, i % 2 === 0 ? RED : GREEN_TXT, { bold: false }));
["True", "False", "True", "False"].forEach((w, i) =>
  text(w, cols[i] - 50, 372, cols[i] + 50, 384, 12, INK, { bold: false }));
text("TP", 289 - 50, 403, 289 + 50, 417, 13, RED);
text("FN", 387 - 50, 403, 387 + 50, 417, 13, GREEN_TXT);
text("TN", 492 - 50, 403, 492 + 50, 417, 13, GREEN_TXT);
text("FP", 597 - 50, 403, 597 + 50, 417, 13, RED);

// ---------- Correctly Classified purple up-arrows + labels ----------
function upArrow(cx) {
  vline(cx, 425, 457, PURPLE, 1.5);
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: px(cx - 7), y: px(419), w: px(14), h: px(12),
    fill: { color: PURPLE }, line: { color: PURPLE, width: 1 },
  });
}
upArrow(264);
upArrow(478);
text("Correctly Classified", 138, 445, 254, 457, 12, PURPLE, { bold: false });
text("Correctly Classified", 354, 445, 472, 457, 12, PURPLE, { bold: false });

// ---------- right confusion matrices ----------
// grid box x 708..860; label strip x 644..708; M1 y 199..291 (hdr sep 228, mid 260); M2 y 374..466 (hdr sep 403, mid 436)
function matrix(y0, hy1, mid, y1, cells, predictedAsY) {
  // label strip
  rect(644, y0 - 23, 708, y1 + 4, STRIP_GRAY, null);
  vline(670, y0 - 23, y1 + 4, STRIP_BLUE, 2);
  s.addText("Actual", {
    x: px(678), y: px(y0 - 10), w: px(26), h: px(y1 - y0 + 20),
    align: "center", valign: "middle", fontSize: 13, bold: true, color: RED,
    fontFace: FONT, margin: 0, rotate: 270,
  });
  // grid box
  rect(708, y0, 860, y1, WHITE, RED, 1.5);
  // "Predicted as" above the box, over the P/N columns
  text("Predicted as", 750, predictedAsY, 860, predictedAsY + 14, 13, RED);
  // header letters P / N
  text("P", 750, y0, 804, hy1, 13, BLACK);
  text("N", 804, y0, 860, hy1, 13, BLACK);
  // row letters P / N in label col of grid
  text("P", 708, hy1, 750, mid, 13, BLACK);
  text("N", 708, mid, 750, y1, 13, BLACK);
  // cell fills
  cells.forEach(([x0, c0, x1, c1, fill]) => { if (fill) rect(x0, c0, x1, c1, fill, null); });
  // grid lines
  hline(708, 860, hy1, RED, 1);
  hline(708, 860, mid, RED, 1);
  vline(750, y0, y1, RED, 1);
  vline(804, y0, y1, RED, 1);
  // cell labels
  cells.forEach(([x0, c0, x1, c1, , label]) => { if (label) text(label, x0, c0, x1, c1, 13, BLACK); });
}

matrix(199, 228, 260, 291, [
  [750, 228, 804, 260, CELL_GREEN, "TP"],
  [804, 228, 860, 260, null, "FN"],
  [750, 260, 804, 291, null, "FP"],
  [804, 260, 860, 291, CELL_GREEN, "TN"],
], 182);

text("Confusion Matrix", 700, 310, 870, 324, 14, NAVY);

matrix(374, 403, 436, 466, [
  [750, 403, 804, 436, CELL_GREEN, "18"],
  [804, 403, 860, 436, null, "12"],
  [750, 436, 804, 466, null, "10"],
  [804, 436, 860, 466, CELL_GREEN, "60"],
], 358);

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_004_recreated.pptx";
pptx.writeFile({ fileName: out })
  .then(() => console.log("wrote", out))
  .catch((e) => { console.error(e); process.exit(1); });
