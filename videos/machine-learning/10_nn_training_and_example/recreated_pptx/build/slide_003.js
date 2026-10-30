// Build: recreated_pptx/build/slide_003.js
// Slide 3 — Neural Network Model (Each node consists of Summation + Activation)
// Source: unique_slides/slide_003.jpg (+ analysis/slide_003_final.json)
// House chrome: machine-learning family (red frame, yellow badge, title y=0.28)

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

// --- House chrome ------------------------------------------------------------
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

// --- Diagram panel -----------------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: px(50), y: px(88), w: px(860), h: px(267),
  fill: { color: "F5F5DC" }, line: { color: "CCCCCC", width: 0.5 },
});

// Purple highlight boxes: Input Sample (top-left), Target Label (top-right)
s.addShape(pres.shapes.RECTANGLE, { x: px(60), y: px(98), w: px(120), h: px(30),
  fill: { color: "800080" }, line: { color: "800080", width: 1 } });
s.addText("Input Sample", { x: px(60), y: px(98), w: px(120), h: px(30),
  align: "center", valign: "middle", fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: px(780), y: px(98), w: px(120), h: px(30),
  fill: { color: "800080" }, line: { color: "800080", width: 1 } });
s.addText("Target Label", { x: px(780), y: px(98), w: px(120), h: px(30),
  align: "center", valign: "middle", fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });

// Arrows from the purple boxes into the network
s.addShape(pres.shapes.LINE, { x: px(120), y: px(128), w: 0, h: px(37),
  line: { color: "000000", width: 1, headEndType: "triangle" } });
s.addShape(pres.shapes.LINE, { x: px(840), y: px(128), w: 0, h: px(17),
  line: { color: "000000", width: 1, headEndType: "triangle" } });

// Columns: input purple dots | red Sigma (i) | blue Sigma (j) | green Sigma (k)
const inX = px(78);
const sumX  = [px(335), px(450), px(565)];
const sumColors = ["8B0000", "0000FF", "008000"];
const layerSub = ["i", "j", "k"];

// Three node rows matching the original (source px y=180/255/330)
const rowsY = [px(180), px(255), px(330)];

// Node-Bias input node (purple circled 1) feeding the summation column
const biasX = px(78), biasY = px(140);
s.addShape(pres.shapes.OVAL, { x: biasX - px(11), y: biasY - px(11), w: px(22), h: px(22),
  fill: { color: "800080" }, line: { color: "800080" , width: 0 } });
s.addText("1", { x: biasX - px(11), y: biasY - px(11), w: px(22), h: px(22),
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.LINE, { x: biasX, y: biasY + px(11), w: sumX[0] - biasX,
  h: rowsY[0] - biasY - px(11), line: { color: "800080", width: 1 } });
rowsY.forEach((y) => {
  s.addShape(pres.shapes.OVAL, { x: inX - px(8), y: y - px(8), w: px(16), h: px(16),
    fill: { color: "800080" }, line: { color: "800080", width: 0 } });
  s.addShape(pres.shapes.LINE, { x: inX + px(8), y, w: sumX[0] - inX - px(8), h: 0,
    line: { color: "000000", width: 1, headEndType: "triangle" } });
});

// Summation nodes: circle + Sigma + Net/O labels
sumX.forEach((cx, li) => {
  rowsY.forEach((cy) => {
    s.addShape(pres.shapes.OVAL, { x: cx - px(15), y: cy - px(15), w: px(30), h: px(30),
      fill: { color: "FFFFFF" }, line: { color: sumColors[li], width: 2 } });
    s.addText("\u03a3", { x: cx - px(15), y: cy - px(15), w: px(30), h: px(30),
      align: "center", valign: "middle", fontSize: 17, bold: true,
      color: sumColors[li], fontFace: FONT, margin: 0 });
    s.addText("Net_" + layerSub[li], { x: cx - px(20), y: cy - px(34), w: px(40), h: px(17),
      align: "center", valign: "middle", fontSize: 10, bold: true,
      color: "8B0000", fontFace: FONT, margin: 0 });
    s.addText("O_" + layerSub[li], { x: cx - px(20), y: cy + px(21), w: px(40), h: px(17),
      align: "center", valign: "middle", fontSize: 10, bold: true,
      color: "8B0000", fontFace: FONT, margin: 0 });
  });
});

// f activation boxes between columns (drawn before the weight labels)
const fBoxX = [[sumX[0] + px(45)], [sumX[1] + px(45)]];
for (let li = 0; li < sumX.length - 1; li++) {
  const fx = sumX[li] + (sumX[li + 1] - sumX[li]) / 2 - px(10);
  rowsY.forEach((cy) => {
    s.addShape(pres.shapes.RECTANGLE, { x: fx, y: cy - px(10), w: px(20), h: px(20),
      fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });
    s.addText("f", { x: fx, y: cy - px(10), w: px(20), h: px(20),
      align: "center", valign: "middle", fontSize: 11, bold: true,
      color: "000000", fontFace: FONT, margin: 0 });
  });
}

// Connection lines + blue weight labels (labels drawn AFTER the f boxes)
for (let li = 0; li < sumX.length - 1; li++) {
  const x1 = sumX[li] + px(15), x2 = sumX[li + 1] - px(15);
  const midX = (x1 + x2) / 2;
  rowsY.forEach((cy) => {
    s.addShape(pres.shapes.LINE, { x: x1, y: cy, w: x2 - x1, h: 0,
      line: { color: "000000", width: 1, headEndType: "triangle" } });
  });
  rowsY.forEach((cy, ri) => {
    const wLabel = li === 0 ? "w_ji" : "w_jj";
    s.addText(wLabel, { x: midX - px(15), y: cy - px(19), w: px(30), h: px(16),
      align: "center", valign: "middle", fontSize: 10, bold: true,
      color: "0000FF", fontFace: FONT, margin: 0 });
  });
}

// Diagonal weight labels (top row) for each hop
for (let li = 0; li < sumX.length - 1; li++) {
  const wLabel = li === 0 ? "w_ji" : "w_jj";
  s.addText(wLabel, { x: sumX[li] + px(20), y: rowsY[0] - px(28), w: px(30), h: px(16),
    align: "center", valign: "middle", fontSize: 10, bold: true,
    color: "0000FF", fontFace: FONT, margin: 0 });
}

// Output labels (right of the green column)
const outX = sumX[2] + px(55);
rowsY.forEach((cy, i) => {
  s.addText(i === 2 ? "Output m" : "Output " + (i + 1), {
    x: outX, y: cy - px(9), w: px(90), h: px(18),
    align: "left", valign: "middle", fontSize: 13, color: "000000",
    fontFace: FONT, margin: 0 });
});

// Vertical dark-red Error bar ("Error Error")
const errX = px(789);
s.addShape(pres.shapes.RECTANGLE, { x: errX, y: px(148), w: px(22), h: px(215),
  fill: { color: "8B0000" }, line: { color: "8B0000", width: 0 } });
s.addText("Error\nError", { x: errX, y: px(150), w: px(22), h: px(212),
  align: "center", valign: "middle", fontSize: 10, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0 });

// Green Class boxes beside the error bar
const clsX = px(816);
[["Class 1", 0], ["Class 2", 1], ["Class m", 2]].forEach(([label, i]) => {
  s.addShape(pres.shapes.RECTANGLE, { x: clsX, y: rowsY[i] - px(12), w: px(72), h: px(24),
    fill: { color: "90EE90" }, line: { color: "000000", width: 0.75 } });
  s.addText(label, { x: clsX, y: rowsY[i] - px(12), w: px(72), h: px(24),
    align: "center", valign: "middle", fontSize: 12, color: "000000",
    fontFace: FONT, margin: 0 });
});

// --- Bottom annotation strip (source px y 405..515) ---------------------------
const stripY = px(405);

// 1. "For Layer "j"" cream box — shape BEFORE its equation images
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

// 2. "Previous Layer Layer (i)" light-blue box with up arrow i
const plX = px(320), plW = px(200), plH = px(58);
s.addShape(pres.shapes.RECTANGLE, { x: plX, y: stripY, w: plW, h: plH,
  fill: { color: "E6F3FF" }, line: { color: "000000", width: 1 } });
s.addText("Previous Layer\nLayer (i)", { x: plX + px(6), y: stripY + px(4),
  w: plW - px(40), h: plH - px(8), align: "center", valign: "top",
  fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("\u2191 i", { x: plX + plW - px(34), y: stripY + plH - px(26),
  w: px(28), h: px(22), align: "center", valign: "middle",
  fontSize: 13, bold: true, color: "000000", fontFace: FONT, margin: 0 });

// 3. "Current Layer is Output Layer (You are here)" green box with up arrow j
const clX = px(530), clW = px(200), clH = px(58);
s.addShape(pres.shapes.RECTANGLE, { x: clX, y: stripY, w: clW, h: clH,
  fill: { color: "98FB98" }, line: { color: "000000", width: 1 } });
s.addText("Current Layer is Output Layer\n(You are here)", { x: clX + px(6),
  y: stripY + px(4), w: clW - px(40), h: clH - px(8), align: "center", valign: "top",
  fontSize: 11, color: "000000", fontFace: FONT, margin: 0 });
s.addText("\u2191 j", { x: clX + clW - px(34), y: stripY + clH - px(26),
  w: px(28), h: px(22), align: "center", valign: "middle",
  fontSize: 13, bold: true, color: "000000", fontFace: FONT, margin: 0 });

// 4. "If Layer "j" is Output Layer:" cream box — shape BEFORE its equation image
const ilX = px(740), ilW = px(175), ilH = px(80);
s.addShape(pres.shapes.RECTANGLE, { x: ilX, y: stripY, w: ilW, h: ilH,
  fill: { color: "FFF8DC" }, line: { color: "000000", width: 1 } });
s.addText('If Layer "j" is Output Layer:', { x: ilX + px(8), y: stripY + px(4),
  w: ilW - px(16), h: px(22), align: "left", valign: "top",
  fontSize: 12, bold: true, color: "000000", fontFace: FONT, margin: 0 });
const eEqInfo = JSON.parse(fs.readFileSync(ASSETS + "/e_eq.png.meta.json", "utf8"));
s.addImage({ path: ASSETS + "/e_eq.png", x: ilX + px(8), y: stripY + px(26),
  w: eEqInfo.w_in, h: eEqInfo.h_in });

// 5. Node Bias marker (purple circled 2 + label) and the circled 1 marker
s.addShape(pres.shapes.OVAL, { x: px(73), y: px(370), w: px(24), h: px(24),
  fill: { color: "800080" }, line: { color: "800080", width: 0 } });
s.addText("2", { x: px(73), y: px(370), w: px(24), h: px(24),
  align: "center", valign: "middle", fontSize: 12, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0 });
s.addText("Node Bias", { x: px(101), y: px(372), w: px(70), h: px(20),
  align: "left", valign: "middle", fontSize: 11, color: "000000",
  fontFace: FONT, margin: 0 });
s.addShape(pres.shapes.OVAL, { x: px(395), y: px(365), w: px(23), h: px(23),
  fill: { color: "800080" }, line: { color: "800080", width: 0 } });
s.addText("1", { x: px(395), y: px(365), w: px(23), h: px(23),
  align: "center", valign: "middle", fontSize: 12, bold: true,
  color: "FFFFFF", fontFace: FONT, margin: 0 });

pres.writeFile({ fileName: VID + "/recreated_pptx/build/slide_003_recreated.pptx" })
  .then(() => console.log("wrote slide_003_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });
