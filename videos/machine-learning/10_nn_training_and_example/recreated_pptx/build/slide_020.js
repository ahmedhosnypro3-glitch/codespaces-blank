// slide_020.js — Hidden-layer backprop weight-update rule (slide 20)
// Geometry measured from unique_slides/slide_020.jpg (960x540) by PIL scans.
const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const CYAN = "E8FCFA";
const TAN = "D8CEC0";
const CREAM = "FBFDE8";
const PEACH = "F7DEC0";
const PEACH_BORDER = "F4A460";
const STRIP = "FAF0E4";
const PURPLE = "9C27B0";
const GREEN = "4CAF50";
const YELLOW = "F1C40F";
const ORANGE = "FF9800";
const RED = "C00000";
const TEXT = "000000";
const SERIF = "Times New Roman";
const FONT = "Arial";
const EQBASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/eq_slide_020/";

let s = pptx.addSlide();
s.background = { color: BG };

// ===== HOUSE CHROME =====
s.addShape(pptx.ShapeType.rect, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2, line: { color: "C00000", width: 1.5 },
});
s.addShape(pptx.ShapeType.ellipse, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 1.5 },
});
s.addText("20", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ===== TOP-LEFT: dependency chain box (x 0.66-5.36, y 0.64-3.24) =====
s.addShape(pptx.ShapeType.rect, {
  x: 0.66, y: 0.64, w: 4.70, h: 2.60, fill: { color: CYAN },
});

const stmt = (runs) => runs.map((r) => ({
  text: r[0],
  options: Object.assign(
    { fontSize: 16, color: TEXT, fontFace: SERIF, italic: true },
    r[1] || {}),
}));

const NETK = (k) => ([
  ["Net"], ["k=" + k, { subscript: true }], [", "],
]);
const stmtY = [0.96, 1.57, 2.18, 2.79];
const arrow = (ch) => [ch, { color: RED, italic: false, bold: true }];

s.addText(stmt([
  ["W"], ["ji", { subscript: true }], [" Affects "], ["Net"], ["j", { subscript: true }],
  [" "], arrow("⇒"),
]), { x: 0.78, y: stmtY[0], w: 4.45, h: 0.34, margin: 0, align: "left", valign: "top" });

s.addText(stmt([
  ["Net"], ["j", { subscript: true }], [" Affects "], ["O"], ["j", { subscript: true }],
  [" "], arrow("⇒"),
]), { x: 0.78, y: stmtY[1], w: 4.45, h: 0.34, margin: 0, align: "left", valign: "top" });

s.addText(stmt([
  ["O"], ["j", { subscript: true }], [" Affects (Net"],
  ["k=1", { subscript: true }], [", Net"], ["k=2", { subscript: true }],
  [", ..., Net"], ["k=m", { subscript: true }], [") "], arrow("⇒"),
]), { x: 0.78, y: stmtY[2], w: 4.45, h: 0.34, margin: 0, align: "left", valign: "top" });

s.addText(stmt([
  ["(Net"], ["k=1", { subscript: true }], [", Net"], ["k=2", { subscript: true }],
  [", ..., Net"], ["k=m", { subscript: true }], [") Affect Error"],
]), { x: 0.78, y: stmtY[3], w: 4.45, h: 0.34, margin: 0, align: "left", valign: "top" });

// ===== TOP-RIGHT: neural-network diagram on tan canvas (x 5.58-11.20, y 0.66-3.26) =====
const dX = 5.58, dY = 0.66, dW = 5.62, dH = 2.60;
s.addShape(pptx.ShapeType.rect, { x: dX, y: dY, w: dW, h: dH, fill: { color: TAN } });

const rowC = [1.15, 1.85, 2.55];      // row centers
const nr = 0.14;                       // node radius

// input layer: purple circles with white Sigma
const inX = 5.86;
rowC.forEach((cy) => {
  s.addShape(pptx.ShapeType.ellipse, { x: inX, y: cy - nr, w: 0.28, h: 0.28, fill: { color: PURPLE } });
  s.addText("Σ", { x: inX, y: cy - nr, w: 0.28, h: 0.28, align: "center", valign: "middle",
    fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });
});

// connecting arrows (bidirectional pairs, approximated by two opposing arrows)
const pairs = [[inX + 0.30, 7.10], [7.40, 8.28], [8.58, 9.46]];
pairs.forEach(([xa, xb]) => {
  rowC.forEach((cy) => {
    s.addShape(pptx.ShapeType.rightArrow, { x: xa, y: cy - 0.14, w: xb - xa, h: 0.10, fill: { color: "555555" } });
    s.addShape(pptx.ShapeType.leftArrow, { x: xa, y: cy + 0.04, w: xb - xa, h: 0.10, fill: { color: "555555" } });
  });
});

// hidden layer: green circles labelled 1,2,3
const hidX = 7.10;
rowC.forEach((cy, i) => {
  s.addShape(pptx.ShapeType.ellipse, { x: hidX, y: cy - 0.16, w: 0.32, h: 0.32, fill: { color: GREEN } });
  s.addText(String(i + 1), { x: hidX, y: cy - 0.16, w: 0.32, h: 0.32, align: "center", valign: "middle",
    fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });
  s.addText("Net", { x: hidX - 0.02, y: cy - 0.38, w: 0.4, h: 0.18, fontSize: 8, color: TEXT,
    fontFace: FONT, margin: 0, align: "center" });
});

// second hidden layer: yellow circles
const hid2X = 8.28;
rowC.forEach((cy) => {
  s.addShape(pptx.ShapeType.ellipse, { x: hid2X, y: cy - 0.16, w: 0.32, h: 0.32, fill: { color: YELLOW } });
});

// output layer: orange circles labelled Output
const outX = 9.46;
rowC.forEach((cy) => {
  s.addShape(pptx.ShapeType.ellipse, { x: outX, y: cy - 0.16, w: 0.32, h: 0.32, fill: { color: ORANGE } });
  s.addText("Output", { x: outX + 0.36, y: cy - 0.10, w: 0.75, h: 0.22, fontSize: 8, color: TEXT,
    fontFace: FONT, margin: 0, align: "left" });
});

// Error bar (vertical red) at x 11.15
s.addShape(pptx.ShapeType.rect, { x: 11.15, y: dY + 0.12, w: 0.30, h: dH - 0.24, fill: { color: RED } });
s.addText("Error", { x: 11.15, y: dY + 0.12, w: 0.30, h: dH - 0.24, align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });

// class labels in small boxes at x 11.52
const classes = ["Class 1", "Class 2", "Class m"];
classes.forEach((c, i) => {
  const cy = rowC[i];
  s.addShape(pptx.ShapeType.rect, { x: 11.52, y: cy - 0.12, w: 0.85, h: 0.24, fill: { color: "FFFFFF" }, line: { color: "808080", width: 0.75 } });
  s.addText(c, { x: 11.52, y: cy - 0.12, w: 0.85, h: 0.24, align: "center", valign: "middle",
    fontSize: 8, color: TEXT, fontFace: FONT, margin: 0 });
});

// "Node Mode" caption bottom-left of diagram
s.addText("Node Mode", { x: 5.70, y: 2.92, w: 1.3, h: 0.22, fontSize: 9, color: TEXT, fontFace: FONT, margin: 0 });

// ===== MIDDLE: two chain-rule equation rows (2D mathtext PNGs) =====
// measured ink bands: row1 y 3.49-4.05, row2 y 4.38-4.94
s.addImage({ path: EQBASE + "eq_mid1.png", x: 0.67, y: 3.42, w: 6.667, h: 0.438 });
s.addImage({ path: EQBASE + "eq_mid2.png", x: 0.67, y: 4.32, w: 6.808, h: 0.675 });

// ===== BOTTOM-RIGHT: cream panel with 4 derivative lines =====
// panel x 9.07-12.67, y 3.30-6.75; line bands y 3.41-3.90, 4.23-4.72, 5.05-5.59, 5.90-6.41
s.addShape(pptx.ShapeType.rect, { x: 9.07, y: 3.30, w: 3.60, h: 3.45, fill: { color: CREAM } });
const rY = [3.44, 4.26, 5.08, 5.93];
const rW = [1.087, 2.483, 2.825, 2.288];
const rH = [0.285, 0.447, 0.345, 0.427];
["eq_r1.png", "eq_r2.png", "eq_r3.png", "eq_r4.png"].forEach((f, i) => {
  s.addImage({ path: EQBASE + f, x: 9.22, y: rY[i], w: rW[i], h: rH[i] });
});

// ===== BOTTOM-LEFT: peach box with delta-rule equation =====
// box x 0.80-6.13, y 5.85-6.77; delta ink band y 5.93-6.74
s.addShape(pptx.ShapeType.rect, {
  x: 0.80, y: 5.85, w: 5.33, h: 0.92, fill: { color: PEACH }, line: { color: PEACH_BORDER, width: 1.5 },
});
s.addImage({ path: EQBASE + "eq_delta.png", x: 0.95, y: 5.95, w: 4.313, h: 0.530 });

// ===== BOTTOM STRIP: cream strip with Where clause =====
// strip x 0.67-8.93, y 6.70-7.42; where ink y 6.79-7.36
s.addShape(pptx.ShapeType.rect, { x: 0.67, y: 6.70, w: 8.26, h: 0.72, fill: { color: STRIP } });
s.addImage({ path: EQBASE + "eq_where.png", x: 0.85, y: 6.82, w: 4.977, h: 0.423 });

pptx.writeFile({
  fileName: "videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_020_recreated.pptx"
}).then(() => console.log("done: slide_020_recreated.pptx"));
