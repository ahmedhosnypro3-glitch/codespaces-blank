// Slide 013 — Classification of "XOR" Truth Table (rejudge wave-3 build).
// Geometry/colors: analysis/reanalysis_v2/slide_013_reanalysis.txt (fresh visual
// re-analysis). House chrome: project AGENTS.md house frame rule (overrides).
const pptxgen = require("pptxgenjs");
const path = require("path");

const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const OUT = path.join(BUILD_DIR, "slide_013_recreated.pptx");

// ---- mapping: original 960x540 frame content panel -> house frame interior ----
const PANEL_X0 = 55, PANEL_Y0 = 42, PANEL_X1 = 855, PANEL_Y1 = 490;
const FRAME_X = 0.15, FRAME_Y = 0.15, FRAME_W = 13.03, FRAME_H = 7.2;
const SX = FRAME_W / (PANEL_X1 - PANEL_X0);
const SY = FRAME_H / (PANEL_Y1 - PANEL_Y0);
const MX = (px) => FRAME_X + (px - PANEL_X0) * SX;
const MY = (py) => FRAME_Y + (py - PANEL_Y0) * SY;
const MW = (px) => px * SX;
const MH = (py) => py * SY;
const PT = (px) => px * (SX * 72); // px of original frame -> pt at recreation scale

const W = 13.33, H = 7.5;
const SANS = "Arial";
const SERIF = "Times New Roman";

const BG = "E8E8E8";        // house background
const HOUSE_RED = "C00000"; // house outer frame + title/caption text
const BLACK = "000000";
const GRAY_LINE = "A6A6A6";
const TABLE_BORDER = "FF3030";
const PINK = "E89898";
const CHIP0_FILL = "CCFFFF", CHIP0_TEXT = "0070C0";
const CHIP1_FILL = "CCFFCC", CHIP1_TEXT = "00A000";
const NODE_FILL = "E6F7FF", NODE_EDGE = "A0A0B8";
const ACTIVATION = "A020F0", GLYPH = "3F00FF";
const FAN = "C8C8D8", RED_ARROW = "FF0000", WEIGHT_BLUE = "0000FF";
const BIAS_RED = "FF0000";
const CAPTION_FILL = "FDE7E0";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: BG };

// ---------------------------------------------------------------- house chrome
s.addShape(pres.shapes.RECTANGLE, {
  x: FRAME_X, y: FRAME_Y, w: FRAME_W, h: FRAME_H,
  fill: { type: "none" }, line: { color: HOUSE_RED, width: 1.5 },
});

s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("13", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 18, bold: true,
  color: "333333", fontFace: SANS, margin: 0,
});

s.addText('Classification of \u201cXOR\u201d Truth Table', {
  x: 0.6, y: 0.28, w: 12.13, h: 0.82,
  align: "center", valign: "middle", fontSize: 30, bold: true,
  color: HOUSE_RED, fontFace: SERIF, margin: 0,
});

// ------------------------------------------------------------------- truth table
const T_X0 = 93, T_X1 = 300, T_Y0 = 131, T_Y1 = 295;
const COL_EDGES = [93, 165, 235, 300];
const ROW_H = (T_Y1 - T_Y0) / 5;

s.addShape(pres.shapes.RECTANGLE, {
  x: MX(T_X0), y: MY(T_Y0), w: MW(T_X1 - T_X0), h: MH(T_Y1 - T_Y0),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});

// internal gridlines (thin gray)
for (let r = 1; r < 5; r++) {
  const gy = MY(T_Y0 + r * ROW_H);
  s.addShape(pres.shapes.LINE, {
    x: MX(T_X0), y: gy, w: MW(T_X1 - T_X0), h: 0,
    line: { color: GRAY_LINE, width: 0.75 },
  });
}
for (let c = 1; c < 3; c++) {
  const gx = MX(COL_EDGES[c]);
  s.addShape(pres.shapes.LINE, {
    x: gx, y: MY(T_Y0), w: 0, h: MH(T_Y1 - T_Y0),
    line: { color: GRAY_LINE, width: 0.75 },
  });
}

const cellText = (txt, cx, cy, opts = {}) => {
  s.addText(txt, {
    x: MX(cx) - MW(40), y: MY(cy) - 0.13, w: MW(80), h: 0.26,
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: PT(16), color: BLACK, ...opts,
  });
};

// header row
cellText([{ text: "X", options: {} }, { text: "1", options: { subscript: true } }],
  (COL_EDGES[0] + COL_EDGES[1]) / 2, T_Y0 + ROW_H / 2);
cellText([{ text: "X", options: {} }, { text: "2", options: { subscript: true } }],
  (COL_EDGES[1] + COL_EDGES[2]) / 2, T_Y0 + ROW_H / 2);
cellText("O/P", (COL_EDGES[2] + COL_EDGES[3]) / 2, T_Y0 + ROW_H / 2);

const rows = [["0", "0", "0"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"]];
const opColCenter = (COL_EDGES[2] + COL_EDGES[3]) / 2;
rows.forEach((row, ri) => {
  const cy = T_Y0 + ROW_H * (ri + 1.5);
  cellText(row[0], (COL_EDGES[0] + COL_EDGES[1]) / 2, cy);
  cellText(row[1], (COL_EDGES[1] + COL_EDGES[2]) / 2, cy);
  // O/P cell holds a colored chip with the digit inside
  const isZero = row[2] === "0";
  const chipW = MW(22), chipH = MH(24);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: MX(opColCenter) - chipW / 2, y: MY(cy) - chipH / 2, w: chipW, h: chipH,
    fill: { color: isZero ? CHIP0_FILL : CHIP1_FILL },
    line: { type: "none" }, rectRadius: 0.06,
  });
  s.addText(row[2], {
    x: MX(opColCenter) - chipW / 2, y: MY(cy) - 0.12, w: chipW, h: 0.24,
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: PT(16),
    color: isZero ? CHIP0_TEXT : CHIP1_TEXT,
  });
});

// outer table border (bright red) on top
s.addShape(pres.shapes.RECTANGLE, {
  x: MX(T_X0), y: MY(T_Y0), w: MW(T_X1 - T_X0), h: MH(T_Y1 - T_Y0),
  fill: { type: "none" }, line: { color: TABLE_BORDER, width: 2 },
});

// ------------------------------------------------------------------ scatter plot
const P_X0 = 510, P_X1 = 800, P_Y0 = 107, P_Y1 = 355;
s.addImage({
  path: path.join(BUILD_DIR, "slide_013_scatter_v2.png"),
  x: MX(P_X0), y: MY(P_Y0), w: MW(P_X1 - P_X0), h: MH(P_Y1 - P_Y0),
});
s.addShape(pres.shapes.RECTANGLE, {
  x: MX(P_X0), y: MY(P_Y0), w: MW(P_X1 - P_X0), h: MH(P_Y1 - P_Y0),
  fill: { type: "none" }, line: { color: PINK, width: 0.75 },
});
// axis labels (red italic serif) beside the arrowheads
s.addText([{ text: "x", options: { italic: true } }, { text: "1", options: { italic: true, subscript: true } }], {
  x: MX(776), y: MY(332) - 0.12, w: 0.45, h: 0.24,
  align: "left", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: PT(15), color: HOUSE_RED,
});
s.addText([{ text: "x", options: { italic: true } }, { text: "2", options: { italic: true, subscript: true } }], {
  x: MX(520), y: MY(126) - 0.12, w: 0.45, h: 0.24,
  align: "left", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: PT(15), color: HOUSE_RED,
});

// ----------------------------------------------------------- perceptron diagram
const D_X0 = 135, D_X1 = 490, D_Y0 = 343, D_Y1 = 473;
s.addShape(pres.shapes.RECTANGLE, {
  x: MX(D_X0), y: MY(D_Y0), w: MW(D_X1 - D_X0), h: MH(D_Y1 - D_Y0),
  fill: { color: "FFFFFF" }, line: { color: PINK, width: 0.75 },
});

// fan lines from inputs into the summation node
const fanLines = [[210, 362, 288, 400], [210, 402, 288, 405], [210, 452, 288, 410]];
fanLines.forEach(([x0, y0, x1, y1]) => {
  const bx = MX(Math.min(x0, x1)), by = MY(Math.min(y0, y1));
  const bw = MW(Math.abs(x1 - x0)), bh = MH(Math.abs(y1 - y0));
  const flipV = (y1 - y0) * (x1 - x0) < 0;
  s.addShape(pres.shapes.LINE, {
    x: bx, y: by, w: bw, h: bh, flipV,
    line: { color: FAN, width: 1 },
  });
});

// red arrowhead into the node
s.addShape(pres.shapes.LINE, {
  x: MX(270), y: MY(405), w: MW(15), h: 0,
  line: { color: RED_ARROW, width: 1.5, endArrowType: "triangle" },
});

// summation node
s.addShape(pres.shapes.OVAL, {
  x: MX(285), y: MY(390), w: MW(30), h: MH(30),
  fill: { color: NODE_FILL }, line: { color: NODE_EDGE, width: 1 },
});
s.addText("\u03a3", {
  x: MX(285), y: MY(390), w: MW(30), h: MH(30),
  align: "center", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: PT(20), color: BLACK,
});

// input labels
const inputLabel = (runs, py, color) => {
  s.addText(runs, {
    x: MX(156), y: MY(py) - 0.12, w: 0.42, h: 0.24,
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: PT(12), color,
  });
};
inputLabel([{ text: "x", options: {} }, { text: "1", options: { subscript: true } }], 365, BLACK);
inputLabel([{ text: "x", options: {} }, { text: "2", options: { subscript: true } }], 405, BLACK);
inputLabel("1", 455, BIAS_RED);

// blue "?" weights (vertically offset from their input labels)
[[195, 359], [195, 414], [195, 455]].forEach(([px, py]) => {
  s.addText("?", {
    x: MX(px), y: MY(py) - 0.12, w: 0.3, h: 0.24,
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: PT(13), color: WEIGHT_BLUE,
  });
});

// arrow from node to activation box
s.addShape(pres.shapes.LINE, {
  x: MX(316), y: MY(405), w: MW(24), h: 0,
  line: { color: RED_ARROW, width: 1.5, endArrowType: "triangle" },
});

// activation box with a drawn step-function glyph
s.addShape(pres.shapes.RECTANGLE, {
  x: MX(342), y: MY(393), w: MW(38), h: MH(27),
  fill: { color: "FFFFFF" }, line: { color: ACTIVATION, width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: MX(347), y: MY(411), w: MW(16), h: 0,
  line: { color: GLYPH, width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: MX(363), y: MY(399), w: 0, h: MH(12),
  line: { color: GLYPH, width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: MX(363), y: MY(399), w: MW(12), h: 0,
  line: { color: GLYPH, width: 1.5 },
});

// arrow to output
s.addShape(pres.shapes.LINE, {
  x: MX(380), y: MY(405), w: MW(48), h: 0,
  line: { color: RED_ARROW, width: 1.5, endArrowType: "triangle" },
});
s.addText("O/P", {
  x: MX(445), y: MY(405) - 0.12, w: MW(30), h: 0.24,
  align: "left", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: PT(13), bold: true, color: BLACK,
});

// --------------------------------------------------------------------- callout
const C_X0 = 548, C_X1 = 740, C_Y0 = 396, C_Y1 = 442;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: MX(C_X0), y: MY(C_Y0), w: MW(C_X1 - C_X0), h: MH(C_Y1 - C_Y0),
  fill: { color: CAPTION_FILL }, line: { color: PINK, width: 1 }, rectRadius: 0.05,
});
s.addText("Not Linearly Separable", {
  x: MX(C_X0), y: MY(C_Y0), w: MW(C_X1 - C_X0), h: MH(C_Y1 - C_Y0),
  align: "center", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: PT(18), bold: true, italic: true, color: HOUSE_RED,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
