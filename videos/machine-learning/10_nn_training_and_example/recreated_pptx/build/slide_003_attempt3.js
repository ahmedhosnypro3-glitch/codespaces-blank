// Build: recreated_pptx/build/slide_003_attempt3.js
// Slide 3 — Neural Network Model (each node = Summation + Activation)
// Attempt 3 (b02): geometry corrected against PIL measurements of
// unique_slides/slide_003.jpg — 3 input dots (not 4), dot dia 5px (not 18),
// measured row/column centres, panel extent, header-box and bottom-strip
// positions. See qa/slide003/b02_pil_geometry.md.
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const ROOT = "/home/codespace/ai_llm_slides";
const VID = ROOT + "/videos/machine-learning/10_nn_training_and_example";
const ASSETS = VID + "/recreated_pptx/build/assets/slide_003";
const NUM = 3;
const S = 13.33 / 960;
function px(v) { return +(v * S).toFixed(4); }

const FONT = "Arial";
const TITLE = "Neural Network Model";
const SUBTITLE = "(Each node consists of Summation + Activation)";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// --- House chrome (measured from reference render) -------------------------
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
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText(SUBTITLE, {
  x: 0.6, y: 0.55, w: 12.13, h: 0.4, align: "center", valign: "top",
  fontSize: 16, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// --- Diagram panel (original beige, measured RGB 218/208/196) -------------
// measured panel extent: x 67..776, y 138..401
s.addShape(pres.shapes.RECTANGLE, {
  x: px(67), y: px(138), w: px(709), h: px(263),
  fill: { color: "DAD0C4" }, line: { color: "B8AE9E", width: 0.5 },
});

// Header boxes (original pink-magenta, measured RGB ~226/149/228)
s.addShape(pres.shapes.RECTANGLE, { x: px(58), y: px(61), w: px(60), h: px(30),
  fill: { color: "E595E4" }, line: { color: "C88AC6", width: 1 } });
s.addText("Input Sample", { x: px(58), y: px(61), w: px(60), h: px(30),
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "FFFFFF",
  fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: px(822), y: px(61), w: px(60), h: px(30),
  fill: { color: "E595E4" }, line: { color: "C88AC6", width: 1 } });
s.addText("Target Label", { x: px(822), y: px(61), w: px(60), h: px(30),
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "FFFFFF",
  fontFace: FONT, margin: 0 });

// Arrows from the header boxes into the network
s.addShape(pres.shapes.LINE, { x: px(88), y: px(91), w: 0, h: px(124),
  line: { color: "000000", width: 1, headEndType: "triangle" } });
s.addShape(pres.shapes.LINE, { x: px(852), y: px(91), w: 0, h: px(50),
  line: { color: "000000", width: 1, headEndType: "triangle" } });

// --- Input column: 3 magenta dots (measured x=78, y=224/247/270, dia 5px) --
// each dot fans in to all three red Sigma nodes (measured ink on every
// dot->sigma diagonal, inkfrac 0.32..0.88).
const rowsY = [181, 255, 330];          // original node rows (measured)
const redX = 163, blueX = 336, greenX = 550;
const dotY = [224, 247, 270];
const inX = px(78), dotR = px(2.5);
dotY.forEach((y) => {
  s.addShape(pres.shapes.OVAL, { x: inX - dotR, y: px(y) - dotR,
    w: dotR * 2, h: dotR * 2, fill: { color: "BC0AC2" },
    line: { color: "BC0AC2", width: 0 } });
});
rowsY.forEach((cy) => {
  dotY.forEach((y) => {
    s.addShape(pres.shapes.LINE, { x: inX + dotR, y: px(y),
      w: px(redX) - px(20) - inX - dotR, h: px(cy) - px(y),
      line: { color: "C0A898", width: 0.75 } });
  });
});

// --- Red Sigma column (layer feeding layer-(i)) ----------------------------
// measured: Sigma circles x 144..182 (centre 163); bias dot x 180..189
// (centre 185); activation box border x ~205, glyph "f" x 216..230 (centre 223)
const redR = px(19);
rowsY.forEach((cy) => {
  s.addShape(pres.shapes.OVAL, { x: px(redX) - redR, y: px(cy) - redR,
    w: redR * 2, h: redR * 2, fill: { color: "FFFFFF" },
    line: { color: "C8A878", width: 1.25 } });
  s.addText("\u03a3", { x: px(redX) - redR, y: px(cy) - redR, w: redR * 2, h: redR * 2,
    align: "center", valign: "middle", fontSize: 21, bold: true, color: "C01818",
    fontFace: FONT, margin: 0 });
  s.addShape(pres.shapes.OVAL, { x: px(185) - px(4), y: px(cy) - px(4),
    w: px(8), h: px(8), fill: { color: "8B0000" }, line: { color: "8B0000", width: 0 } });
  s.addShape(pres.shapes.LINE, { x: px(189), y: px(cy), w: px(6), h: 0,
    line: { color: "8B0000", width: 1.25, headEndType: "triangle" } });
  s.addShape(pres.shapes.RECTANGLE, { x: px(205), y: px(cy) - px(12),
    w: px(32), h: px(24), fill: { color: "FFFFFF" },
    line: { color: "D0B896", width: 1 } });
  s.addText("f", { x: px(205), y: px(cy) - px(12), w: px(32), h: px(24),
    align: "center", valign: "middle", fontSize: 17, bold: true, italic: true,
    color: "A01818", fontFace: FONT, margin: 0 });
  s.addShape(pres.shapes.OVAL, { x: px(240) - px(4), y: px(cy) - px(4),
    w: px(8), h: px(8), fill: { color: "C01818" }, line: { color: "C01818", width: 0 } });
  s.addShape(pres.shapes.LINE, { x: px(244), y: px(cy), w: px(14), h: 0,
    line: { color: "C01818", width: 1.25, headEndType: "triangle" } });
  [263, 277, 291].forEach((cx) => {
    s.addShape(pres.shapes.OVAL, { x: px(cx) - px(4.5), y: px(cy) - px(4.5),
      w: px(9), h: px(9), fill: { type: "none" },
      line: { color: "7A6E60", width: 0.75 } });
  });
  s.addShape(pres.shapes.LINE, { x: px(296), y: px(cy), w: px(blueX) - px(316) - px(20), h: 0,
    line: { color: "C0A898", width: 0.75 } });
});

// --- Blue Sigma column = layer (i): Net_i, activation block, O_i ----------
// measured: Sigma circles x 319..355 (centre 336), f-box x 394..416 (white)
const blueR = px(18);
rowsY.forEach((cy) => {
  s.addShape(pres.shapes.OVAL, { x: px(blueX) - blueR, y: px(cy) - blueR,
    w: blueR * 2, h: blueR * 2, fill: { color: "EAF0FD" },
    line: { color: "8080B4", width: 1.25 } });
  s.addText("\u03a3", { x: px(blueX) - blueR, y: px(cy) - blueR, w: blueR * 2, h: blueR * 2,
    align: "center", valign: "middle", fontSize: 21, bold: true, color: "C01818",
    fontFace: FONT, margin: 0 });
  s.addText("Net_i", { x: px(352), y: px(cy) - px(22), w: px(42), h: px(17),
    align: "left", valign: "middle", fontSize: 12, bold: true, italic: true,
    color: "C01818", fontFace: FONT, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: px(394), y: px(cy) - px(11),
    w: px(22), h: px(22), fill: { color: "FFFFFF" },
    line: { color: "8080B4", width: 1 } });
  s.addText("f", { x: px(394), y: px(cy) - px(11), w: px(22), h: px(22),
    align: "center", valign: "middle", fontSize: 17, bold: true, italic: true,
    color: "404040", fontFace: FONT, margin: 0 });
  s.addShape(pres.shapes.OVAL, { x: px(421) - px(4), y: px(cy) - px(4),
    w: px(8), h: px(8), fill: { color: "C8102E" }, line: { color: "C8102E", width: 0 } });
  s.addText("O_i", { x: px(425), y: px(cy) - px(22), w: px(24), h: px(17),
    align: "left", valign: "middle", fontSize: 12, bold: true, italic: true,
    color: "C01818", fontFace: FONT, margin: 0 });
});

// --- Fan-out: every layer-(i) node feeds every layer-(j) node. Measured
// cross-row link ink (band x 432..520, baseline mean 19.5 / max 40):
// SAME frac 0.84..1.00, CROSS frac 0.23..0.39 — cross-row diagonals are
// present but materially weaker, so draw them thinner. ----------------------
rowsY.forEach((cy) => {
  rowsY.forEach((ty) => {
    const same = cy === ty;
    s.addShape(pres.shapes.LINE, { x: px(432), y: px(cy),
      w: px(510) - px(432), h: px(ty) - px(cy),
      line: { color: "BCA294", width: same ? 1 : 0.5,
              headEndType: same ? "triangle" : "none" } });
  });
});

// Blue weight labels riding the diagonals (measured blue-ink centroids:
// w_ji near (470,167), w_jj near (464,197), w_jj near (516,296))
s.addText("w_ji", { x: px(454), y: px(157), w: px(34), h: px(16),
  align: "center", valign: "middle", fontSize: 12, bold: true, italic: true,
  color: "0000FF", fontFace: FONT, margin: 0, rotate: 335 });
s.addText("w_jj", { x: px(448), y: px(190), w: px(34), h: px(16),
  align: "center", valign: "middle", fontSize: 12, bold: true, italic: true,
  color: "0000FF", fontFace: FONT, margin: 0, rotate: 335 });
s.addText("w_jj", { x: px(500), y: px(289), w: px(34), h: px(16),
  align: "center", valign: "middle", fontSize: 12, bold: true, italic: true,
  color: "0000FF", fontFace: FONT, margin: 0, rotate: 300 });

// --- Green Sigma column = layer (j): Net_j, activation block, O_j ---------
const greenR = px(18);
rowsY.forEach((cy, i) => {
  s.addShape(pres.shapes.OVAL, { x: px(528) - px(4), y: px(cy) - px(4),
    w: px(8), h: px(8), fill: { color: "C8102E" }, line: { color: "C8102E", width: 0 } });
  s.addShape(pres.shapes.OVAL, { x: px(greenX) - greenR, y: px(cy) - greenR,
    w: greenR * 2, h: greenR * 2, fill: { color: "D6FFAF" },
    line: { color: "7CBB7C", width: 1.25 } });
  s.addText("\u03a3", { x: px(greenX) - greenR, y: px(cy) - greenR, w: greenR * 2, h: greenR * 2,
    align: "center", valign: "middle", fontSize: 21, bold: true, color: "C01818",
    fontFace: FONT, margin: 0 });
  s.addText("Net_j", { x: px(570), y: px(cy) - px(22), w: px(36), h: px(17),
    align: "left", valign: "middle", fontSize: 12, bold: true, italic: true,
    color: "C01818", fontFace: FONT, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: px(602), y: px(cy) - px(11),
    w: px(21), h: px(22), fill: { color: "E6FFD6" },
    line: { color: "7CBB7C", width: 1 } });
  s.addText("f", { x: px(602), y: px(cy) - px(11), w: px(21), h: px(22),
    align: "center", valign: "middle", fontSize: 16, bold: true, italic: true,
    color: "1E6B1E", fontFace: FONT, margin: 0 });
  s.addText("O_j", { x: px(629), y: px(cy) - px(23), w: px(24), h: px(17),
    align: "left", valign: "middle", fontSize: 12, bold: true, italic: true,
    color: "C01818", fontFace: FONT, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: px(627), y: px(cy), w: px(62), h: 0,
    line: { color: "C01818", width: 1.25, headEndType: "triangle" } });
  s.addShape(pres.shapes.RECTANGLE, { x: px(690), y: px(cy) - px(9),
    w: px(64), h: px(18), fill: { color: "FFFFFF" },
    line: { color: "9090C0", width: 1 } });
  s.addText(i === 2 ? "Output m" : "Output " + (i + 1), {
    x: px(690), y: px(cy) - px(9), w: px(64), h: px(18),
    align: "center", valign: "middle", fontSize: 11, bold: true, italic: true,
    color: "000000", fontFace: FONT, margin: 0 });
});

// Vertical dark-red Error bar
const errX = px(789);
s.addShape(pres.shapes.RECTANGLE, { x: errX, y: px(148), w: px(22), h: px(215),
  fill: { color: "9F0000" }, line: { color: "9F0000", width: 0 } });
s.addText("Error\nError", { x: errX, y: px(150), w: px(22), h: px(212),
  align: "center", valign: "middle", fontSize: 10, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0 });

// Green Class boxes beside the error bar
const clsX = px(816);
[["Class 1", 0], ["Class 2", 1], ["Class m", 2]].forEach(([label, i]) => {
  s.addShape(pres.shapes.RECTANGLE, { x: clsX, y: px(rowsY[i]) - px(12), w: px(72), h: px(24),
    fill: { color: "D9FFC9" }, line: { color: "8CCB7C", width: 0.75 } });
  s.addText(label, { x: clsX, y: px(rowsY[i]) - px(12), w: px(72), h: px(24),
    align: "center", valign: "middle", fontSize: 12, bold: true, italic: true,
    color: "000000", fontFace: FONT, margin: 0 });
});

// --- Bottom annotation strip (source px y 405..515) ------------------------
const stripY = px(405);

const flX = px(58), flW = px(250), flH = px(110);
s.addShape(pres.shapes.RECTANGLE, { x: flX, y: stripY, w: flW, h: flH,
  fill: { color: "FFF8DC" }, line: { color: "000000", width: 1 } });
s.addText('For Layer "j"', { x: flX + px(8), y: stripY + px(4), w: flW - px(16), h: px(22),
  align: "left", valign: "top", fontSize: 13, bold: true, color: "000000",
  fontFace: FONT, margin: 0 });
const netEqInfo = JSON.parse(fs.readFileSync(ASSETS + "/net_eq.png.meta.json", "utf8"));
s.addImage({ path: ASSETS + "/net_eq.png", x: flX + px(8), y: stripY + px(26),
  w: netEqInfo.w_in, h: netEqInfo.h_in });
const oEqInfo = JSON.parse(fs.readFileSync(ASSETS + "/o_eq.png.meta.json", "utf8"));
s.addImage({ path: ASSETS + "/o_eq.png", x: flX + px(8), y: stripY + px(30) + netEqInfo.h_in,
  w: oEqInfo.w_in, h: oEqInfo.h_in });

const plX = px(320), plW = px(200), plH = px(58);
s.addShape(pres.shapes.RECTANGLE, { x: plX, y: stripY, w: plW, h: plH,
  fill: { color: "E6F3FF" }, line: { color: "000000", width: 1 } });
s.addText("Previous Layer\nLayer (i)", { x: plX + px(6), y: stripY + px(4),
  w: plW - px(40), h: plH - px(8), align: "center", valign: "top",
  fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("\u2191 i", { x: plX + plW - px(34), y: stripY + plH - px(26),
  w: px(28), h: px(22), align: "center", valign: "middle",
  fontSize: 13, bold: true, color: "000000", fontFace: FONT, margin: 0 });

const clX = px(530), clW = px(200), clH = px(58);
s.addShape(pres.shapes.RECTANGLE, { x: clX, y: stripY, w: clW, h: clH,
  fill: { color: "98FB98" }, line: { color: "000000", width: 1 } });
s.addText("Current Layer is Output Layer\n(You are here)", { x: clX + px(6),
  y: stripY + px(4), w: clW - px(40), h: clH - px(8), align: "center", valign: "top",
  fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
s.addText("\u2191 j", { x: clX + clW - px(34), y: stripY + clH - px(26),
  w: px(28), h: px(22), align: "center", valign: "middle",
  fontSize: 13, bold: true, color: "000000", fontFace: FONT, margin: 0 });

const ilX = px(740), ilW = px(175), ilH = px(80);
s.addShape(pres.shapes.RECTANGLE, { x: ilX, y: stripY, w: ilW, h: ilH,
  fill: { color: "FFF8DC" }, line: { color: "000000", width: 1 } });
s.addText('If Layer "j" is Output Layer:', { x: ilX + px(8), y: stripY + px(4),
  w: ilW - px(16), h: px(22), align: "left", valign: "top",
  fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0 });
const eEqInfo = JSON.parse(fs.readFileSync(ASSETS + "/e_eq.png.meta.json", "utf8"));
s.addImage({ path: ASSETS + "/e_eq.png", x: ilX + px(8), y: stripY + px(26),
  w: eEqInfo.w_in, h: eEqInfo.h_in });

// Node Bias marker (original magenta-red) and the bottom-centre circled 1
s.addShape(pres.shapes.OVAL, { x: px(73), y: px(370), w: px(24), h: px(24),
  fill: { color: "B83060" }, line: { color: "B83060", width: 0 } });
s.addText("1", { x: px(73), y: px(370), w: px(24), h: px(24),
  align: "center", valign: "middle", fontSize: 12, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0 });
s.addText("Node Bias", { x: px(101), y: px(372), w: px(70), h: px(20),
  align: "left", valign: "middle", fontSize: 11, italic: true, color: "9E2A58",
  fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.OVAL, { x: px(395), y: px(365), w: px(23), h: px(23),
  fill: { color: "B83060" }, line: { color: "B83060", width: 0 } });
s.addText("1", { x: px(395), y: px(365), w: px(23), h: px(23),
  align: "center", valign: "middle", fontSize: 12, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0 });

pres.writeFile({ fileName: VID + "/recreated_pptx/build/slide_003_attempt2_recreated.pptx" })
  .then(() => console.log("wrote slide_003_attempt2_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });
