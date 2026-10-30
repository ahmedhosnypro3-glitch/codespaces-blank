// Pattern: house-chrome (machine-learning family) + neural network diagram (slide 2)
// Slide: LAYOUT_WIDE 13.33x7.5in, bg E8E8E8; red frame 0.15in inset; yellow badge; title y=0.28

const pptxgen = require("pptxgenjs");

const NUM = 2;
const TITLE = "Neural Network Model";
const SUBTITLE = "(Each node consists of Summation + Activation)";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ============================================================
// HOUSE CHROME (non-negotiable, overrides any spec/judge)
// ============================================================
// 1. Outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral) - HOUSE CHROME
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
  fontSize: 40, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Subtitle (below title, centered) — with underlines per original
s.addText([
  { text: "(Each node consists of ", options: { fontSize: 24, bold: true, color: "0000CC", fontFace: FONT } },
  { text: "Summation", options: { fontSize: 24, bold: true, color: "0000CC", fontFace: FONT, underline: true } },
  { text: " + ", options: { fontSize: 24, bold: true, color: "0000CC", fontFace: FONT } },
  { text: "Activation", options: { fontSize: 24, bold: true, color: "0000CC", fontFace: FONT, underline: true } },
  { text: ")", options: { fontSize: 24, bold: true, color: "0000CC", fontFace: FONT } },
], {
  x: 0.6, y: 0.95, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  margin: 0,
});

// ============================================================
// SLIDE 2 CONTENT - Neural Network Diagram
// Scale: original 900x490px -> house content area 13.03x7.2in (inside frame)
// Content frame: x=0.15..13.18, y=0.15..7.35
// ============================================================

// Content area bounds (inside house frame)
const cx = 0.15;
const cy = 0.15;
const cw = W - 0.3;  // 13.03
const ch = H - 0.3;  // 7.2

// Scale factors: 900px -> 13.03in, 490px -> 7.2in
const sx = cw / 900;
const sy = ch / 490;

// Helper: convert original pixel coords to inches
function px(x, y) {
  return { x: cx + x * sx, y: cy + y * sy };
}
function pw(px) { return px * sx; }
function ph(py) { return py * sy; }

// Colors from analysis
const BEIGE = "E8E4DC";
const PANEL_BORDER = "A6A6A6";
const PINK = "FF99FF";
const MAGENTA = "FF00FF";
const RED = "FF0000";
const BLUE_FILL = "DDEBF7";
const BLUE_BORDER = "6699FF";
const GREEN_FILL = "E2EFDA";
const GREEN_BORDER = "66CC66";
const ORANGE_FILL = "FCE4D6";
const ORANGE_BORDER = "FFA64D";
const WHITE = "FFFFFF";
const BLACK = "000000";
const GRAY_LIGHT = "C0C0C0";
const DARK_RED = "990000";
const WHITE_TEXT = "FFFFFF";
const GREEN_LIGHT = "DFF0D8";
const GREEN_BORDER2 = "70AD47";
const BLUE_BORDER2 = "4472C4";
const ORANGE_BORDER2 = "ED7D31";

// Rich text helper for subscript labels
function subLabel(base, sub, opts = {}) {
  const baseOpts = { bold: true, color: RED, fontFace: FONT, fontSize: 9, margin: 0 };
  const subOpts = { ...baseOpts, subscript: true, fontSize: 7 };
  return [
    { text: base, options: baseOpts },
    { text: sub, options: subOpts }
  ];
}

function blueSubLabel(base, sub, opts = {}) {
  const baseOpts = { bold: true, italic: true, color: "0000FF", fontFace: FONT, fontSize: 8, margin: 0 };
  const subOpts = { ...baseOpts, subscript: true, fontSize: 6 };
  return [
    { text: base, options: baseOpts },
    { text: sub, options: subOpts }
  ];
}

function magentaSubLabel(base, sub, opts = {}) {
  const baseOpts = { bold: true, italic: true, color: MAGENTA, fontFace: FONT, fontSize: 8, margin: 0 };
  const subOpts = { ...baseOpts, subscript: true, fontSize: 6 };
  return [
    { text: base, options: baseOpts },
    { text: sub, options: subOpts }
  ];
}

// ============================================================
// STEP 5: Input/Target connector strip (upper band)
// ============================================================
const inputBox = px(62, 113);
s.addShape(pres.shapes.RECTANGLE, {
  x: inputBox.x, y: inputBox.y,
  w: pw(56), h: ph(29),
  fill: { color: PINK }, line: { color: MAGENTA, width: 1 },
});
s.addText("Input\nSample", {
  x: inputBox.x, y: inputBox.y, w: pw(56), h: ph(29),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

const targetBox = px(772, 113);
s.addShape(pres.shapes.RECTANGLE, {
  x: targetBox.x, y: targetBox.y,
  w: pw(58), h: ph(29),
  fill: { color: PINK }, line: { color: MAGENTA, width: 1 },
});
s.addText("Target\nLabel", {
  x: targetBox.x, y: targetBox.y, w: pw(58), h: ph(29),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

const lineY = cy + 127 * sy;
const lineX1 = cx + 118 * sx;
const lineX2 = cx + 772 * sx;
s.addShape(pres.shapes.LINE, {
  x: lineX1, y: lineY,
  w: lineX2 - lineX1, h: 0,
  line: { color: MAGENTA, width: 1.5, dashType: "dash" },
});
s.addShape(pres.shapes.LEFT_ARROW, {
  x: lineX1 - 0.08, y: lineY - 0.04,
  w: 0.08, h: 0.08,
  fill: { color: MAGENTA }, line: { color: MAGENTA, width: 0.5 },
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: lineX2, y: lineY - 0.04,
  w: 0.08, h: 0.08,
  fill: { color: MAGENTA }, line: { color: MAGENTA, width: 0.5 },
});

// ============================================================
// STEP 6: Main panel (beige rectangle with gray border)
// ============================================================
const panel = px(60, 150);
s.addShape(pres.shapes.RECTANGLE, {
  x: panel.x, y: panel.y,
  w: pw(680), h: ph(255),
  fill: { color: BEIGE }, line: { color: PANEL_BORDER, width: 1 },
});

// ============================================================
// STEP 7: Connection web (draw FIRST so nodes overlay)
// ============================================================
const nodeRadius = 15 * sx;
const nodeDiameter = 30 * sx;

const layerX = {
  input: cx + 150 * sx,
  blue: cx + 243 * sx,
  green: cx + 400 * sx,
  orange: cx + 550 * sx,
  ellipsis1: cx + 185 * sx,
  ellipsis2: cx + 197 * sx,
  ellipsis3: cx + 209 * sx,
  ellipsis4: cx + 580 * sx,
  ellipsis5: cx + 592 * sx,
  ellipsis6: cx + 604 * sx,
  output: cx + 630 * sx,
  outputBox: cx + 675 * sx,
};
const rowY = [
  cy + 192 * sy,
  cy + 258 * sy,
  cy + 330 * sy,
];

function drawConnections(fromX, toX, fromYs, toYs) {
  for (let fy of fromYs) {
    for (let ty of toYs) {
      s.addShape(pres.shapes.LINE, {
        x: fromX + nodeRadius, y: fy,
        w: toX - fromX - 2 * nodeRadius, h: ty - fy,
        line: { color: "FF9999", width: 0.5 },
      });
      s.addShape(pres.shapes.OVAL, {
        x: fromX + nodeRadius - 0.03, y: fy - 0.03,
        w: 0.06, h: 0.06,
        fill: { color: RED }, line: { color: RED, width: 0 },
      });
      s.addShape(pres.shapes.OVAL, {
        x: toX - nodeRadius - 0.03, y: ty - 0.03,
        w: 0.06, h: 0.06,
        fill: { color: RED }, line: { color: RED, width: 0 },
      });
    }
  }
}

drawConnections(layerX.input, layerX.blue, rowY, rowY);
drawConnections(layerX.blue, layerX.green, rowY, rowY);
drawConnections(layerX.green, layerX.orange, rowY, rowY);
drawConnections(layerX.orange, layerX.output, rowY, rowY);

// ============================================================
// STEP 8: Input column magenta dots (far left of panel)
// ============================================================
const dotX = cx + 73 * sx;
s.addShape(pres.shapes.OVAL, {
  x: dotX - ph(4), y: cy + 230 * sy - ph(4),
  w: ph(8), h: ph(8),
  fill: { color: MAGENTA }, line: { color: MAGENTA, width: 0 },
});
[250, 270, 290].forEach((y, i) => {
  const size = ph(8 - i * 2);
  s.addShape(pres.shapes.OVAL, {
    x: dotX - size/2, y: cy + y * sy - size/2,
    w: size, h: size,
    fill: { color: MAGENTA }, line: { color: MAGENTA, width: 0 },
  });
});

// ============================================================
// Input layer - 3 white circles with Σ + f (sigmoid)
// ============================================================
rowY.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: layerX.input - nodeDiameter/2, y: y - nodeDiameter/2,
    w: nodeDiameter, h: nodeDiameter,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  // Σ on left, f on right
  s.addText([
    { text: "\u03A3", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
    { text: "f", options: { fontSize: 10, bold: true, color: BLACK, fontFace: FONT } }
  ], {
    x: layerX.input - nodeDiameter/2, y: y - nodeDiameter/2 + 0.01,
    w: nodeDiameter, h: nodeDiameter - 0.02,
    align: "center", valign: "middle",
    margin: 0,
  });
});

// ============================================================
// STEP 9: Ellipsis between input and blue (3 dots per row, 9 total)
// ============================================================
[layerX.ellipsis1, layerX.ellipsis2, layerX.ellipsis3].forEach(ex => {
  rowY.forEach(y => {
    s.addShape(pres.shapes.OVAL, {
      x: ex - ph(3), y: y - ph(3),
      w: ph(6), h: ph(6),
      fill: { color: GRAY_LIGHT }, line: { color: GRAY_LIGHT, width: 0 },
    });
  });
});

// ============================================================
// STEP 10: Blue hidden layer (3 nodes) - labels Net_i, O_i
// ============================================================
rowY.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: layerX.blue - nodeDiameter/2, y: y - nodeDiameter/2,
    w: nodeDiameter, h: nodeDiameter,
    fill: { color: BLUE_FILL }, line: { color: BLUE_BORDER, width: 1 },
  });
  s.addText([
    { text: "\u03A3", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
    { text: "f", options: { fontSize: 10, bold: true, color: BLACK, fontFace: FONT } }
  ], {
    x: layerX.blue - nodeDiameter/2, y: y - nodeDiameter/2 + 0.01,
    w: nodeDiameter, h: nodeDiameter - 0.02,
    align: "center", valign: "middle",
    margin: 0,
  });
  // O_i label above each
  s.addText(subLabel("O", "i"), {
    x: layerX.blue - 0.3, y: y - 0.3,
    w: 0.6, h: 0.25,
    align: "center", valign: "bottom",
    margin: 0,
  });
});
// Net_i above top node
s.addText(subLabel("Net", "i"), {
  x: layerX.blue - 0.3, y: cy + 160 * sy - 0.25,
  w: 0.6, h: 0.25,
  align: "center", valign: "bottom",
  margin: 0,
});

// ============================================================
// STEP 11: Weight labels w_ji between blue and green
// ============================================================
s.addText(blueSubLabel("w", "ji"), {
  x: cx + 315 * sx - 0.2, y: cy + 182 * sy - 0.15,
  w: 0.4, h: 0.2,
  align: "center", valign: "middle",
  margin: 0,
});
[210, 240, 270].forEach(y => {
  s.addText(blueSubLabel("w", "ji"), {
    x: cx + 310 * sx - 0.2, y: cy + y * sy - 0.1,
    w: 0.4, h: 0.2,
    align: "center", valign: "middle",
    margin: 0,
  });
});

// ============================================================
// STEP 12: Green hidden layer - labels Net_j, O_j
// ============================================================
rowY.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: layerX.green - nodeDiameter/2, y: y - nodeDiameter/2,
    w: nodeDiameter, h: nodeDiameter,
    fill: { color: GREEN_FILL }, line: { color: GREEN_BORDER, width: 1 },
  });
  s.addText([
    { text: "\u03A3", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
    { text: "f", options: { fontSize: 10, bold: true, color: BLACK, fontFace: FONT } }
  ], {
    x: layerX.green - nodeDiameter/2, y: y - nodeDiameter/2 + 0.01,
    w: nodeDiameter, h: nodeDiameter - 0.02,
    align: "center", valign: "middle",
    margin: 0,
  });
  s.addText(subLabel("O", "j"), {
    x: layerX.green - 0.3, y: y - 0.3,
    w: 0.6, h: 0.25,
    align: "center", valign: "bottom",
    margin: 0,
  });
});
s.addText(subLabel("Net", "j"), {
  x: layerX.green - 0.3, y: cy + 160 * sy - 0.25,
  w: 0.6, h: 0.25,
  align: "center", valign: "bottom",
  margin: 0,
});

// ============================================================
// STEP 13: Weight labels w_kj between green and orange + w_lk [?]
// ============================================================
s.addText(blueSubLabel("w", "kj"), {
  x: cx + 470 * sx - 0.2, y: cy + 182 * sy - 0.15,
  w: 0.4, h: 0.2,
  align: "center", valign: "middle",
  margin: 0,
});
[210, 240, 270].forEach(y => {
  s.addText(blueSubLabel("w", "kj"), {
    x: cx + 465 * sx - 0.2, y: cy + y * sy - 0.1,
    w: 0.4, h: 0.2,
    align: "center", valign: "middle",
    margin: 0,
  });
});
// w_lk [?] - uncertain item, small near (505, 215)
s.addText([
  { text: "w", options: { fontSize: 7, bold: true, italic: true, color: "0000FF", fontFace: FONT } },
  { text: "l", options: { fontSize: 5, bold: true, italic: true, color: "0000FF", fontFace: FONT, subscript: true } },
  { text: "k", options: { fontSize: 5, bold: true, italic: true, color: "0000FF", fontFace: FONT, subscript: true } },
  { text: " [?]", options: { fontSize: 7, bold: true, italic: true, color: "0000FF", fontFace: FONT } }
], {
  x: cx + 505 * sx - 0.25, y: cy + 215 * sy - 0.1,
  w: 0.5, h: 0.2,
  align: "center", valign: "middle",
  margin: 0,
});

// ============================================================
// STEP 14: Orange hidden layer - labels Net_k, O_k
// ============================================================
rowY.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: layerX.orange - nodeDiameter/2, y: y - nodeDiameter/2,
    w: nodeDiameter, h: nodeDiameter,
    fill: { color: ORANGE_FILL }, line: { color: ORANGE_BORDER, width: 1 },
  });
  s.addText([
    { text: "\u03A3", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
    { text: "f", options: { fontSize: 10, bold: true, color: BLACK, fontFace: FONT } }
  ], {
    x: layerX.orange - nodeDiameter/2, y: y - nodeDiameter/2 + 0.01,
    w: nodeDiameter, h: nodeDiameter - 0.02,
    align: "center", valign: "middle",
    margin: 0,
  });
  s.addText(subLabel("O", "k"), {
    x: layerX.orange - 0.3, y: y - 0.3,
    w: 0.6, h: 0.25,
    align: "center", valign: "bottom",
    margin: 0,
  });
});
s.addText(subLabel("Net", "k"), {
  x: layerX.orange - 0.3, y: cy + 160 * sy - 0.25,
  w: 0.6, h: 0.25,
  align: "center", valign: "bottom",
  margin: 0,
});

// ============================================================
// STEP 15: Ellipsis between orange and output (9 dots)
// ============================================================
[layerX.ellipsis4, layerX.ellipsis5, layerX.ellipsis6].forEach(ex => {
  rowY.forEach(y => {
    s.addShape(pres.shapes.OVAL, {
      x: ex - ph(3), y: y - ph(3),
      w: ph(6), h: ph(6),
      fill: { color: GRAY_LIGHT }, line: { color: GRAY_LIGHT, width: 0 },
    });
  });
});

// Output layer (3 white circles)
rowY.forEach((y, i) => {
  s.addShape(pres.shapes.OVAL, {
    x: layerX.output - nodeDiameter/2, y: y - nodeDiameter/2,
    w: nodeDiameter, h: nodeDiameter,
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText([
    { text: "\u03A3", options: { fontSize: 14, bold: true, color: BLACK, fontFace: FONT } },
    { text: "f", options: { fontSize: 10, bold: true, color: BLACK, fontFace: FONT } }
  ], {
    x: layerX.output - nodeDiameter/2, y: y - nodeDiameter/2 + 0.01,
    w: nodeDiameter, h: nodeDiameter - 0.02,
    align: "center", valign: "middle",
    margin: 0,
  });
});

// ============================================================
// STEP 16: Output boxes with red arrowheads
// ============================================================
const outputs = ["Output 1", "Output 2", "Output m"];
rowY.forEach((y, i) => {
  s.addShape(pres.shapes.RIGHT_ARROW, {
    x: cx + 670 * sx - 0.06, y: y - 0.04,
    w: 0.06, h: 0.08,
    fill: { color: RED }, line: { color: RED, width: 0 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: layerX.outputBox, y: y - ph(10),
    w: pw(60), h: ph(20),
    fill: { color: WHITE }, line: { color: BLACK, width: 1 },
  });
  s.addText(outputs[i], {
    x: layerX.outputBox, y: y - ph(10),
    w: pw(60), h: ph(20),
    align: "center", valign: "middle",
    fontSize: 8, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// ============================================================
// STEP 17: Bias nodes (purple circles with white '1')
// ============================================================
const PURPLE_BIAS = "8A2BE2";
// Blue layer bias at (245, 373)
s.addShape(pres.shapes.OVAL, {
  x: cx + 245 * sx - 0.1, y: cy + 373 * sy - 0.1,
  w: 0.2, h: 0.2,
  fill: { color: PURPLE_BIAS }, line: { color: PURPLE_BIAS, width: 0 },
});
s.addText("1", {
  x: cx + 245 * sx - 0.1, y: cy + 373 * sy - 0.1,
  w: 0.2, h: 0.2,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
// Green layer bias at (400, 373)
s.addShape(pres.shapes.OVAL, {
  x: cx + 400 * sx - 0.1, y: cy + 373 * sy - 0.1,
  w: 0.2, h: 0.2,
  fill: { color: PURPLE_BIAS }, line: { color: PURPLE_BIAS, width: 0 },
});
s.addText("1", {
  x: cx + 400 * sx - 0.1, y: cy + 373 * sy - 0.1,
  w: 0.2, h: 0.2,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
// Pink lines up to layers
s.addShape(pres.shapes.LINE, {
  x: cx + 245 * sx, y: cy + 373 * sy,
  w: 0, h: cy + 330 * sy - (cy + 373 * sy),
  line: { color: "FF9999", width: 1 },
});
s.addShape(pres.shapes.LINE, {
  x: cx + 400 * sx, y: cy + 373 * sy,
  w: 0, h: cy + 330 * sy - (cy + 373 * sy),
  line: { color: "FF9999", width: 1 },
});
// Legend at panel bottom-left: purple circle + "Node Bias"
s.addShape(pres.shapes.OVAL, {
  x: cx + 75 * sx - 0.08, y: cy + 396 * sy - 0.08,
  w: 0.16, h: 0.16,
  fill: { color: PURPLE_BIAS }, line: { color: PURPLE_BIAS, width: 0 },
});
s.addText("1", {
  x: cx + 75 * sx - 0.08, y: cy + 396 * sy - 0.08,
  w: 0.16, h: 0.16,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("Node Bias", {
  x: cx + 75 * sx + 0.1, y: cy + 396 * sy - 0.05,
  w: 0.8, h: 0.15,
  align: "left", valign: "middle",
  fontSize: 8, bold: true, italic: true, color: PURPLE_BIAS, fontFace: FONT, margin: 0,
});

// ============================================================
// STEP 18: Error bar (dark red vertical with rotated white text)
// ============================================================
s.addShape(pres.shapes.RECTANGLE, {
  x: cx + 745 * sx, y: cy + 160 * sy,
  w: pw(20), h: ph(195),
  fill: { color: DARK_RED }, line: { color: DARK_RED, width: 0 },
});
s.addText("Error Error Error", {
  x: cx + 745 * sx, y: cy + 160 * sy,
  w: pw(20), h: ph(195),
  align: "center", valign: "middle",
  fontSize: 7, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  textDirection: "vert270",
});

// ============================================================
// STEP 19: Class boxes (light green, aligned with outputs)
// ============================================================
const classes = ["Class 1", "Class 2", "Class m"];
rowY.forEach((y, i) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: cx + 775 * sx, y: y - ph(10),
    w: pw(55), h: ph(20),
    fill: { color: GREEN_LIGHT }, line: { color: GREEN_BORDER2, width: 1 },
  });
  s.addText(classes[i], {
    x: cx + 775 * sx, y: y - ph(10),
    w: pw(55), h: ph(20),
    align: "center", valign: "middle",
    fontSize: 8, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});

// ============================================================
// STEP 20-21: Bottom callout row (arrows + boxes)
// ============================================================
const arrowY1 = cy + 395 * sy;
const boxY1 = cy + 425 * sy;
// Blue arrow + box (Previous Layer (Layer i))
s.addShape(pres.shapes.UP_ARROW, {
  x: cx + 245 * sx - 0.1, y: arrowY1,
  w: 0.2, h: ph(25),
  fill: { color: WHITE }, line: { color: BLUE_BORDER2, width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: cx + 205 * sx, y: boxY1,
  w: pw(82), h: ph(27),
  fill: { color: BLUE_FILL }, line: { color: BLUE_BORDER2, width: 1 },
});
s.addText([
  { text: "Previous Layer", options: { fontSize: 8, color: "4472C4", fontFace: FONT } },
  { text: "\n(Layer i)", options: { fontSize: 8, color: "4472C4", fontFace: FONT } }
], {
  x: cx + 205 * sx, y: boxY1,
  w: pw(82), h: ph(27),
  align: "center", valign: "middle",
  margin: 0,
});

// Green arrow + box (Current Layer (You are here))
s.addShape(pres.shapes.UP_ARROW, {
  x: cx + 400 * sx - 0.1, y: arrowY1,
  w: 0.2, h: ph(25),
  fill: { color: GREEN_FILL }, line: { color: GREEN_BORDER2, width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: cx + 358 * sx, y: boxY1,
  w: pw(85), h: ph(27),
  fill: { color: GREEN_FILL }, line: { color: GREEN_BORDER2, width: 1 },
});
s.addText("Current Layer\n(You are here)", {
  x: cx + 358 * sx, y: boxY1,
  w: pw(85), h: ph(27),
  align: "center", valign: "middle",
  fontSize: 8, bold: false, color: "70AD47", fontFace: FONT, margin: 0,
});

// Orange arrow + box (Next Layer (Layer k))
s.addShape(pres.shapes.UP_ARROW, {
  x: cx + 550 * sx - 0.1, y: arrowY1,
  w: 0.2, h: ph(25),
  fill: { color: ORANGE_FILL }, line: { color: ORANGE_BORDER2, width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: cx + 525 * sx, y: boxY1,
  w: pw(60), h: ph(27),
  fill: { color: ORANGE_FILL }, line: { color: ORANGE_BORDER2, width: 1 },
});
s.addText([
  { text: "Next Layer", options: { fontSize: 8, color: "ED7D31", fontFace: FONT } },
  { text: "\n(Layer k)", options: { fontSize: 8, color: "ED7D31", fontFace: FONT } }
], {
  x: cx + 525 * sx, y: boxY1,
  w: pw(60), h: ph(27),
  align: "center", valign: "middle",
  margin: 0,
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_002_recreated.pptx"
}).then(() => console.log("wrote slide_002_recreated.pptx"));