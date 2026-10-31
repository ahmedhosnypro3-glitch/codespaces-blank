// Slide 028 build: house chrome + backward-pass formulas, NN diagram, delta/W columns, gray sigmoid stack
// Geometry measured from unique_slides/slide_028.jpg (960x540; px/72 = in).
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const NUM = 28;
const HEADER = "Backward (Update Output Layer Weights)";
const FONT = "Arial";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const px = (v) => v / 72;

// ---- house chrome ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// Original heading sits at y[195-220]px (no house-style title row on this slide)
s.addText(HEADER, {
  x: px(51), y: px(193), w: px(400), h: px(24), align: "left", valign: "middle",
  fontSize: 18, bold: true, color: "000080", fontFace: FONT, margin: 0,
});
// Original has no house-style title row; its heading sits at y[195-220]px.

const T = (txt, x, y, w, h, o) => s.addText(txt, Object.assign({
  x, y, w, h, fontSize: 13, bold: false, color: "000000", fontFace: FONT, margin: 0,
}, o));

// ---- top-left formula box x[45-389] y[73-151] ----
s.addShape(pres.shapes.RECTANGLE, {
  x: px(45), y: px(73), w: px(344), h: px(78),
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});
function eq(name, xIn, baselineIn) {
  const side = JSON.parse(fs.readFileSync(`assets/${name}.json`));
  s.addImage({
    path: `assets/${name}.png`,
    x: xIn, y: baselineIn - side.baseline_frac * side.h_in,
    w: side.w_in, h: side.h_in,
  });
}
eq("eq28_delta_j", px(50), px(97));
eq("eq28_delta_w", px(50), px(138));

// ---- top-right diagram box x[401-920] y[52-184] ----
s.addShape(pres.shapes.RECTANGLE, {
  x: px(401), y: px(52), w: px(519), h: px(132),
  fill: { type: "none" }, line: { color: "FF0000", width: 1.5 },
});
function node(cx, cy, r, fill, stroke, label, lc) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
  T(label, px(cx - r), px(cy - r), px(2 * r), px(2 * r),
    { align: "center", valign: "middle", fontSize: 10, bold: true, color: lc || "000000" });
}
// inputs (X1=1, X2=5)
node(444, 88, 6, "000000", "000000", "");
node(444, 132, 6, "000000", "000000", "");
T("X₁", px(455), px(80), px(20), px(12), { fontSize: 10, bold: true });
T("X₂", px(455), px(124), px(20), px(12), { fontSize: 10, bold: true });
T("(1)", px(455), px(92), px(18), px(11), { fontSize: 9 });
T("(5)", px(455), px(136), px(18), px(11), { fontSize: 9 });
node(569, 177, 7, "00B0F0", "0000FF", "1", "FFFFFF");
T("Bias", px(520), px(168), px(34), px(11), { fontSize: 9, bold: true, color: "0000FF" });
// hidden 3,4,5
const HX = 567, HY = [75, 114, 151];
for (let i = 0; i < 3; i++) node(HX, HY[i], 11, "FFF2CC", "000000", String(i + 3));
// outputs 6,7
const OX = 703, OY = [97, 137];
for (let i = 0; i < 2; i++) node(OX, OY[i], 10, "FCE4D6", "C55A11", String(i + 6));
// labels
T("Input", px(419), px(60), px(31), px(12), { fontSize: 10, bold: true, color: "0000FF" });
T("Output", px(722), px(60), px(40), px(12), { fontSize: 10, bold: true, color: "0000FF" });
T("Target", px(846), px(60), px(38), px(12), { fontSize: 10, bold: true, color: "0000FF" });
T("t₆", px(755), px(88), px(16), px(11), { fontSize: 9 });
T("t₇", px(755), px(128), px(16), px(11), { fontSize: 9 });
T("0", px(786), px(93), px(10), px(12), { fontSize: 10, bold: true });
T("1", px(786), px(133), px(10), px(12), { fontSize: 10, bold: true });
T("[", px(856), px(82), px(8), px(70), { fontSize: 14, bold: true });
T("]", px(866), px(82), px(8), px(70), { fontSize: 14, bold: true });
T("η=5", px(818), px(165), px(40), px(12), { fontSize: 11, bold: true, color: "FF0000" });
T("Oᵢ", px(660), px(56), px(16), px(12), { fontSize: 9, italic: true });

// ---- diagram edges ----
function edge(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color: color, width: 1 },
  });
}
const GREEN = "008000", REDW = "FF0000", BLUEW = "0000FF";
for (let i = 0; i < 2; i++) {
  for (let j = 0; j < 3; j++) edge(450, [88, 132][i], HX - 11, HY[j], GREEN);
}
edge(572, 170, HX - 11, HY[0], BLUEW);
edge(572, 170, HX - 11, HY[1], BLUEW);
edge(572, 170, HX - 11, HY[2], BLUEW);
for (let j = 0; j < 3; j++) {
  for (let k = 0; k < 2; k++) edge(HX + 11, HY[j], OX - 10, OY[k], REDW);
}
edge(576, 172, OX - 10, OY[0], BLUEW);
edge(576, 172, OX - 10, OY[1], BLUEW);
edge(713, OY[0], 750, 93, REDW);
edge(713, OY[1], 750, 133, REDW);
// weight labels (green input->hidden, red hidden->output)
function wl(x, y, txt, color, size) {
  T(txt, px(x), px(y), px(26), px(11), { color: color, fontSize: size || 9, bold: true });
}
wl(468, 96, "0.1", GREEN); wl(520, 86, "0.2", GREEN); wl(488, 89, "0.3", GREEN);
wl(470, 118, "0.4", GREEN); wl(520, 114, "0.5", GREEN); wl(520, 139, "0.6", GREEN);
wl(576, 74, "0.3", REDW); wl(600, 104, "0.4", REDW); wl(578, 112, "0.5", REDW);
wl(576, 148, "0.2", REDW); wl(688, 133, "0.3", REDW); wl(707, 95, "0.5", REDW);

// ---- delta lines (red, 2D PNGs) ----
eq("eq28_delta6", px(57), px(243));
eq("eq28_delta7", px(57), px(266));

// ---- red delta-W column (left) ----
const dw6 = [
  "ΔW₆₃ = 5 * (−0.131) * 0.9 = −0.59",
  "ΔW₆₄ = 5 * (−0.131) * 0.943 = −0.618",
  "ΔW₆₅ = 5 * (−0.131) * 0.968 = −0.634",
  "ΔW₆b = 5 * (−0.131) * 1.0 = −0.655",
];
dw6.forEach((txt, i) => {
  T(txt, px(59), px(292 + i * 24), px(190), px(22), { color: "FF0000", fontSize: 12 });
});
const dw7 = [
  "ΔW₇₃ = 5 * (0.035) * 0.9 = 0.158",
  "ΔW₇₄ = 5 * (0.035) * 0.943 = 0.165",
  "ΔW₇₅ = 5 * (0.035) * 0.968 = 0.169",
  "ΔW₇b = 5 * (0.035) * 1.0 = 0.175",
];
dw7.forEach((txt, i) => {
  T(txt, px(64), px(421 + i * 27), px(190), px(22), { color: "FF0000", fontSize: 12 });
});

// ---- blue updated-W column ----
const u6 = [
  "W₆₃ = 0.3 − 0.59 = −0.29",
  "W₆₄ = 0.4 − 0.618 = −0.218",
  "W₆₅ = 0.5 − 0.634 = −0.134",
  "W₆b = 0.2 − 0.655 = −0.455",
];
u6.forEach((txt, i) => {
  T(txt, px(448), px(283 + i * 27), px(210), px(22), { color: "0000FF", fontSize: 12 });
});
const u7 = [
  "W₇₃ = 0.3 + 0.158 = 0.458",
  "W₇₄ = 0.4 + 0.165 = 0.565",
  "W₇₅ = 0.5 + 0.169 = 0.669",
  "W₇b = 0.2 + 0.175 = 0.375",
];
u7.forEach((txt, i) => {
  T(txt, px(452), px(420 + i * 27), px(210), px(22), { color: "0000FF", fontSize: 12 });
});

// ---- red double-headed arrows between columns ----
[[5.46, 4.78], [5.46, 6.44]].forEach(([x, y]) => {
  s.addShape(pres.shapes.LINE, {
    x, y, w: 0.67, h: 0,
    line: { color: "FF0000", width: 2, beginArrowType: "triangle", endArrowType: "triangle" },
  });
});

// ---- gray sigmoid stack (far right) ----
const grayY = [196, 233, 271, 324, 365];
const eqNames = ["eq28_o3", "eq28_o4", "eq28_o5", "eq28_o6", "eq28_o7"];
grayY.forEach((y0, i) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(706), y: px(y0), w: px(190), h: px(26),
    fill: { color: "C0C0C0" }, line: { color: "808080", width: 0.5 },
  });
  eq(eqNames[i], px(712), px(y0 + 24));
});

pres.writeFile({ fileName: "slide_028_recreated.pptx" })
  .then(() => console.log("wrote slide_028_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });
