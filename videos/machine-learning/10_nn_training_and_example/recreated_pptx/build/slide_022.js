// Slide 22: Back Propagation Training Algorithm
// Pattern: house-chrome + neural network diagram + step boxes
// House chrome (machine-learning family, ref slide 3) — OVERRIDES per-slide spec

const pptxgen = require("pptxgenjs");
const FONT = "Arial";
const NUM = 22;
const TITLE = "Back Propagation Training Algorithm";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ===== HOUSE CHROME (non-negotiable) =====
// 1. Outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});

// 2. Yellow badge (numeral = printed number on original = 22)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ===== CONTENT AREA (inside house frame) =====
const cx = 0.15, cy = 0.15, cw = W - 0.3, ch = H - 0.3;
// Scale: original 900x490px -> house content area 13.03x7.2in
const sx = cw / 900;
const sy = ch / 490;
function px(x, y) { return { x: cx + x * sx, y: cy + y * sy }; }
function pw(px) { return px * sx; }
function ph(py) { return py * sy; }

// Colors from analysis
const GRAY_BG = "F2F2F2";
const PURPLE = "800080";
const GREEN = "00FF00";
const RED = "FF0000";
const BLUE = "0000FF";
const WHITE = "FFFFFF";
const BLACK = "000000";
const D9D9D9 = "D9D9D9";
const YELLOW_BADGE = "FFFF00";

// ===== Neural Network Diagram (upper half) =====
// From analysis: network core top-left to middle-left; target/error boxes extend to far right
// Panel area approx: x=0.15..13.18, y=0.8..3.8 (below title to mid-slide)
const panelX = cx + 50 * sx;
const panelY = cy + 100 * sy;
const panelW = pw(800);
const panelH = ph(280);

// Network core positions (from analysis visual_elements)
// Input layer: purple dots on left
// Hidden: Sigma nodes middle
// Output: green Sigma nodes right
// Targets: green boxes to right of output
// Error: tall red box at far right
const inputX = panelX + pw(50);
const hiddenX = panelX + pw(280);
const outputX = panelX + pw(500);
const targetX = panelX + pw(650);
const errorX = panelX + pw(750);

const nodeY1 = panelY + ph(60);
const nodeY2 = panelY + ph(140);
const nodeY3 = panelY + ph(220);
const nodeYs = [nodeY1, nodeY2, nodeY3];
const nodeR = pw(15);

// Input layer (purple dots)
nodeYs.forEach(y => {
  s.addShape(pres.shapes.OVAL, {
    x: inputX - nodeR, y: y - nodeR, w: nodeR*2, h: nodeR*2,
    fill: { color: PURPLE }, line: { color: PURPLE, width: 0 },
  });
});

// Hidden layer (Sigma nodes)
nodeYs.forEach(y => {
  s.addShape(pres.shapes.OVAL, {
    x: hiddenX - nodeR, y: y - nodeR, w: nodeR*2, h: nodeR*2,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText("\u03A3", { // Sigma
    x: hiddenX - nodeR, y: y - nodeR, w: nodeR*2, h: nodeR*2,
    align: "center", valign: "middle", fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Output layer (green Sigma nodes)
nodeYs.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: outputX - nodeR, y: y - nodeR, w: nodeR*2, h: nodeR*2,
    fill: { color: GREEN }, line: { color: GREEN, width: 1 },
  });
  s.addText("\u03A3", {
    x: outputX - nodeR, y: y - nodeR, w: nodeR*2, h: nodeR*2,
    align: "center", valign: "middle", fontSize: 14, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
  // Output labels
  const labels = ["Output 1", "Output 2", "Output m"];
  s.addText(labels[i], {
    x: outputX + nodeR + pw(10), y: y - ph(10), w: pw(100), h: ph(20),
    align: "left", valign: "middle", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Connections (input->hidden->output)
nodeYs.forEach((y, i) => {
  // input -> hidden
  s.addShape(pres.shapes.LINE, {
    x: inputX + nodeR, y: y, w: hiddenX - inputX - nodeR*2, h: 0,
    line: { color: BLACK, width: 1 },
  });
  // hidden -> output
  s.addShape(pres.shapes.LINE, {
    x: hiddenX + nodeR, y: y, w: outputX - hiddenX - nodeR*2, h: 0,
    line: { color: BLACK, width: 1 },
  });
});

// Target boxes (green)
["Target 1", "Target 2", "Target m"].forEach((label, i) => {
  const y = nodeYs[i];
  s.addShape(pres.shapes.RECTANGLE, {
    x: targetX, y: y - ph(10), w: pw(80), h: ph(20),
    fill: { color: GREEN }, line: { color: GREEN, width: 1 },
  });
  s.addText(label, {
    x: targetX, y: y - ph(10), w: pw(80), h: ph(20),
    align: "center", valign: "middle", fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// Error box (tall red, far right)
s.addShape(pres.shapes.RECTANGLE, {
  x: errorX, y: nodeY1 - ph(20), w: pw(40), h: nodeY3 - nodeY1 + ph(40),
  fill: { color: RED }, line: { color: RED, width: 0 },
});
s.addText("Error 1\nError 2\nError m", {
  x: errorX, y: nodeY1 - ph(20), w: pw(40), h: nodeY3 - nodeY1 + ph(40),
  align: "center", valign: "middle", fontSize: 9, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// Made with draw.io logo
s.addText("Made with draw.io", {
  x: panelX + pw(10), y: panelY + panelH - ph(30), w: pw(150), h: ph(20),
  align: "left", valign: "top", fontSize: 8, color: D9D9D9, fontFace: FONT, margin: 0,
});

// ===== Step Boxes (bottom half) =====
// Blue-bordered box: steps [1]-[2], below diagram left
// Red-bordered box: steps [3]-[6], full width below blue box
const boxY1 = panelY + panelH + ph(20);
const boxW = cw * 0.45;
const boxH1 = ph(80);
const boxX1 = panelX + pw(20);

// Blue box
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX1, y: boxY1, w: boxW, h: boxH1,
  fill: { color: WHITE }, line: { color: BLUE, width: 2 },
});
s.addText("[1] Initialize all Weights with random values\n[2] Provide one training sample at a time (and its corresponding target label)", {
  x: boxX1 + pw(10), y: boxY1 + ph(5), w: boxW - pw(20), h: boxH1 - ph(10),
  align: "left", valign: "top", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// Red box (full width)
const boxY2 = boxY1 + boxH1 + ph(10);
const boxW2 = cw - pw(40);
const boxX2 = cx + pw(20);
const boxH2 = ph(280);

s.addShape(pres.shapes.RECTANGLE, {
  x: boxX2, y: boxY2, w: boxW2, h: boxH2,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

const redBoxText = `[3] Go Forward : Start from Input Layer, Calculate Net_j, O_j for each layer till reach output layer
[4] Go Backward : Start from Output Layer, Calculate \u0394w_ji, W_ji for each weights of Output layer
\u0394w_ji = \u03b7 O_i O_j(1-O_j) (t_j-O_j) Store: \u03b4_j = O_j(1-O_j) (t_j-O_j) (for each node at output Layer)
[5] Go Backward : go to previous Layer, Calculate \u0394w_ji, W_ji for each weights of Hidden layer
\u0394w_ji = \u03b7 O_i O_j(1-O_j) [\u03a3_k (\u03b4_k w_kj)] Store: \u03b4_j = O_j(1-O_j) [\u03a3_k (\u03b4_k w_kj)] (for each node at hidden Layer)
[6] Repeat [5] till reach first hidden layer
Remember: \u03b4_k = \u03b4_j of next layer ( which is already calculated in previous step )`;

s.addText(redBoxText, {
  x: boxX2 + pw(10), y: boxY2 + ph(5), w: boxW2 - pw(20), h: boxH2 - ph(10),
  align: "left", valign: "top", fontSize: 10, color: BLACK, fontFace: FONT, margin: 0,
});

// Write output — deliverable path: recreated_pptx/slide_NNN_recreated.pptx (single version)
const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_022_recreated.pptx";
pres.writeFile({ fileName: outPath })
  .then(() => console.log("wrote " + outPath))
  .catch(e => { console.error(e); process.exit(1); });