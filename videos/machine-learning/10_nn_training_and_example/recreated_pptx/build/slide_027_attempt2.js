// Slide 027 rebuild (attempt2): house chrome + full weighted NN diagram + 2D sigmoid PNGs
// Geometry measured from unique_slides/slide_027.jpg (960x540; px/72 = in).
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const NUM = 27, TITLE = "Example", FONT = "Arial";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };  // house background
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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- diagram box x[173-865] y[58-255] ----
const DX = px(173), DY = px(58), DW = px(692), DH = px(197);
s.addShape(pres.shapes.RECTANGLE, {
  x: DX, y: DY, w: DW, h: DH, fill: { type: "none" },
  line: { color: "C00000", width: 2 },
});
const T = (txt, x, y, w, h, o) => s.addText(txt, Object.assign({
  x, y, w, h, fontSize: 13, bold: true, color: "000000", fontFace: FONT, margin: 0,
}, o));
// column labels (blue)
T("Input", px(200), px(71), px(45), px(14), { color: "0000FF" });
T("Output", px(651), px(71), px(58), px(14), { color: "0000FF" });
T("Target", px(872), px(71), px(42), px(14), { color: "0000FF" });

// ---- nodes ----
function node(cx, cy, r, fill, stroke, label, lcolor) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: stroke, width: 1.5 },
  });
  T(label, px(cx - r), px(cy - r), px(2 * r), px(2 * r),
    { align: "center", valign: "middle", fontSize: 13, color: lcolor || "000000" });
}
// input dots x1,x2 + bias (measured cx~224)
const INX = 224, INY = [113, 177, 233];
node(INX, INY[0], 7, "000000", "000000", "", "FFFFFF");
node(INX, INY[1], 7, "000000", "000000", "", "FFFFFF");
node(INX, INY[2], 8, "00B0F0", "0000FF", "1", "FFFFFF");
T("x₁", px(230), px(105), px(20), px(12), { fontSize: 12 });
T("x₂", px(230), px(169), px(20), px(12), { fontSize: 12 });
T("Bias", px(228), px(243), px(30), px(10), { fontSize: 10 });
T("(1)", px(256), px(107), px(18), px(13), { fontSize: 11, bold: false });
T("(5)", px(256), px(172), px(18), px(13), { fontSize: 11, bold: false });
// hidden 3,4,5 (yellow, cx~420, cy 93/151/207, r16)
const HX = 420, HY = [93, 151, 207];
for (let i = 0; i < 3; i++) {
  node(HX, HY[i], 16, "FFF2CC", "000000", String(i + 3));
  T("O" + "₃₄₅"[i], px(HX - 42), px(HY[i] - 8), px(16), px(14), { fontSize: 12, align: "right" });
}
// output 6,7 (pale orange, cx~623, cy 125/185, r14)
const OX = 623, OY = [125, 185];
for (let i = 0; i < 2; i++) {
  node(OX, OY[i], 14, "FCE4D6", "C55A11", String(i + 6));
  T("O" + "₆₇"[i], px(OX + 16), px(OY[i] - 8), px(16), px(14), { fontSize: 12 });
}
// target values far right
T("t₆=(0)", px(752), px(109), px(34), px(13), { fontSize: 11 });
T("t₇=(1)", px(752), px(169), px(34), px(13), { fontSize: 11 });
// eta
T("η=5", px(803), px(231), px(60), px(13), { color: "C00000", fontSize: 13 });

// ---- edges ----
function edge(x1, y1, x2, y2, color, width) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color: color, width: width || 0.75 },
  });
}
const GREEN = "008000", REDW = "C00000", BLUEW = "0000FF";
// input -> hidden (green)
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) edge(INX + 7, INY[i], HX - 16, HY[j], GREEN);
}
// bias -> hidden (blue, dashed look: plain blue)
edge(INX + 8, INY[2], HX - 16, HY[0], BLUEW);
edge(INX + 8, INY[2], HX - 16, HY[1], BLUEW);
edge(INX + 8, INY[2], HX - 16, HY[2], BLUEW);
// hidden -> output (red)
for (let j = 0; j < 3; j++) {
  for (let k = 0; k < 2; k++) edge(HX + 16, HY[j], OX - 14, OY[k], REDW);
}
// bias -> output (blue)
edge(INX + 8, INY[2], OX - 14, OY[0], BLUEW);
edge(INX + 8, INY[2], OX - 14, OY[1], BLUEW);

// ---- weight labels ----
function wl(x, y, txt, color) {
  T(txt, px(x), px(y), px(26), px(12), { color: color, fontSize: 10, align: "center" });
}
// green input->hidden weights (measured clusters x272-371 y96-247)
wl(276, 96, "0.1", GREEN); wl(300, 108, "0.2", GREEN); wl(325, 118, "0.3", GREEN);
wl(276, 186, "0.4", GREEN); wl(300, 172, "0.5", GREEN); wl(325, 160, "0.6", GREEN);
wl(240, 210, "0.1", GREEN); wl(268, 224, "0.1", GREEN); wl(296, 238, "0.1", GREEN);
// red hidden->output weights
wl(452, 92, "0.3", REDW); wl(492, 118, "0.4", REDW);
wl(452, 148, "0.4", REDW); wl(492, 172, "0.5", REDW);
wl(452, 204, "0.5", REDW);
wl(560, 200, "0.2", BLUEW); wl(560, 218, "0.2", BLUEW);

// ---- bottom half ----
T("Forward", px(51), px(256), px(94), px(16), { color: "0000FF", fontSize: 16 });
// white calc box 1: x[53-367] y[276-421]
s.addShape(pres.shapes.RECTANGLE, {
  x: px(53), y: px(276), w: px(314), h: px(145),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});
const netLines = [
  "Net₃ = 1*0.1+5*0.4+1*0.1 = 2.2",
  "Net₄ = 1*0.2+5*0.5+1*0.1 = 2.8",
  "Net₅ = 1*0.3+5*0.6+1*0.1 = 3.4",
];
netLines.forEach((txt, i) => {
  T(txt, px(58), px(288 + i * 40), px(304), px(24),
    { color: "C00000", fontSize: 13, bold: false });
});
// white calc box 2: x[54-607] y[435-528]
s.addShape(pres.shapes.RECTANGLE, {
  x: px(54), y: px(435), w: px(553), h: px(93),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});
["Net₆ = 0.9*0.3+0.943*0.4+0.968*0.5+1*0.2 = 1.3312",
 "Net₇ = 0.9*0.3+0.943*0.4+0.968*0.5+1*0.2 = 1.3312"].forEach((txt, i) => {
  T(txt, px(57), px(448 + i * 32), px(546), px(24),
    { color: "C00000", fontSize: 14, bold: false });
});
// green sigmoid boxes
function greenBox(x0, y0, x1, y1) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: "D9EAD3" }, line: { color: "006100", width: 1.5 },
  });
}
greenBox(646, 276, 895, 421);
greenBox(646, 435, 895, 528);
// 2D equation PNGs (exact size, px/600 in)
function eq(name, xIn, baselineIn) {
  const side = JSON.parse(fs.readFileSync(`assets/${name}.json`));
  s.addImage({
    path: `assets/${name}.png`,
    x: xIn, y: baselineIn - side.baseline_frac * side.h_in,
    w: side.w_in, h: side.h_in,
  });
}
eq("eq27_o3", px(677), px(311));
eq("eq27_o4", px(665), px(358));
eq("eq27_o5", px(665), px(405));
eq("eq27_o6", px(668), px(470));
eq("eq27_o7", px(668), px(517));

pres.writeFile({ fileName: "slide_027_recreated.pptx" })
  .then(() => console.log("wrote slide_027_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });
