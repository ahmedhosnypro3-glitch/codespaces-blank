const pptxgen = require("pptxgenjs");

// Slide 019 - sigmoid / tanh / tan / tan^-1 function graphs.
// Panel palette and geometry are PIL-matched to unique_slides/slide_019.jpg:
// white panel interiors, blue-purple borders, rose curves, faint dashed grid.
const NUM = 19;
const TITLE = "Sigmoid, tanh, tan, and tan\u207B\u00B9 Function Graphs";
const FONT = "Arial";
const BG = "E8E8E8", RED = "C00000", YELLOW = "FFF9C4";
const PEACH = "FCE4D6", PEACH_BORDER = "E6B8A2";
const GRAY = "D9D9D9", GRAY_BORDER = "A6A6A6", PANEL_BG = "FEFFFD";

const W = 13.33, H = 7.5;
const PANEL_W = 305 / 72, PANEL_H = 178 / 72;
const IX = 0.15, IW = 13.03, IY = 0.15, IH = 7.2;
const CAP_W = PANEL_W * 0.85, CAP_XOFF = PANEL_W * 0.075, CAP_H = 0.55, CAP_GAP = 0.10;
const EQ = {
  sigmoid: [2.94667, 0.52667], tanh: [2.44667, 0.53167],
  tan: [1.31667, 0.225], arctan: [1.55333, 0.26167],
};
const DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const GRAPH_DIR = DIR + "/graphs_slide_019";

const PANELS = [
  { key: "sigmoid", x: IX + 0.11 * IW, y: IY + 0.11 * IH, cap: PEACH, capLine: PEACH_BORDER, shift: 0 },
  { key: "tanh", x: IX + 0.52 * IW, y: IY + 0.11 * IH, cap: PEACH, capLine: PEACH_BORDER, shift: 0 },
  { key: "tan", x: IX + 0.11 * IW, y: IY + 0.55 * IH, cap: GRAY, capLine: GRAY_BORDER, shift: -0.097 },
  { key: "arctan", x: IX + 0.52 * IW, y: IY + 0.55 * IH, cap: PEACH, capLine: PEACH_BORDER, shift: 0 },
];
const ARROW = {
  x: IX + 0.11 * IW + PANEL_W + 0.125,
  y: IY + 0.55 * IH + PANEL_H / 2 - 0.15, w: 0.2, h: 0.3,
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: BG };

// House chrome: outer frame, slide-number badge, title box.
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
});

for (const p of PANELS) {
  // Panel backdrop; the embedded plot image carries the measured blue-purple border.
  s.addShape(pres.shapes.RECTANGLE, {
    x: p.x, y: p.y, w: PANEL_W, h: PANEL_H,
    fill: { color: PANEL_BG }, line: { color: PANEL_BG, width: 0.25 },
  });
  s.addImage({
    path: GRAPH_DIR + "/graph_" + p.key + ".png",
    x: p.x, y: p.y, w: PANEL_W, h: PANEL_H,
  });

  const capX = p.x + CAP_XOFF + p.shift;
  const capY = p.y + PANEL_H + CAP_GAP;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: capX, y: capY, w: CAP_W, h: CAP_H,
    fill: { color: p.cap }, line: { color: p.capLine, width: 1 },
  });
  const [ew, eh] = EQ[p.key];
  s.addImage({
    path: DIR + "/eq_" + p.key + ".png",
    x: capX + (CAP_W - ew) / 2, y: capY + (CAP_H - eh) / 2, w: ew, h: eh,
  });
}

// Hollow red arrow pointing from the tan graph to the arctan graph.
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: ARROW.x, y: ARROW.y, w: ARROW.w, h: ARROW.h,
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 },
});

pres.writeFile({ fileName: DIR + "/slide_019_recreated.pptx" })
  .then(() => console.log("wrote " + DIR + "/slide_019_recreated.pptx"));
