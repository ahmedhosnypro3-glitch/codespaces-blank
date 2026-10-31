// Build slide 018: Saturation Problem in Activation Functions (badge 18)
//
// All geometry measured from unique_slides/slide_018.jpg (960x540) with PIL.
// The original frame's slide content occupies x 57..903, y 43..517; that box
// maps onto the house frame rectangle (0.15in inset, 13.03 x 7.2 in).
//
// Measured layout (original-frame px):
//   outer red frame   x  57..903  y  43..517
//   left eq card      x  78..375  y 109..159   (pale pink fill, coral border)
//   right eq card     x 550..855  y 107..158
//   eq block L        brace x 285..289, values x=292, conditions x=314, y 116..155
//   eq block R        brace x 742..746, values x=750, conditions x=783, y 114..154
//   left step pane    x  70..340  y 168..274
//   right step pane   x 509..780  y 168..274
//   callout           x 342..498  y 194..248  (sits in the gap between the panes)
//   bottom charts     x  74..335 / 390..634 / 655..890, y 322..478
//   caption row       y 486..503, centred at x 200 / 506 / 773
//   dashed connector  x 201..208, y 274..321 (uni-polar pane -> sigmoid pane)
// The black band at the very bottom of the original is a lecture-capture
// artifact and is omitted. Equations are 600-dpi 2D PNGs (professional format).
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";

const OX0 = 57, OX1 = 903, OY0 = 43, OY1 = 517;
const IX0 = 0.15, IX1 = 0.15 + 13.03, IY0 = 0.15, IY1 = 0.15 + 7.2;
function mx(px) { return IX0 + (px - OX0) / (OX1 - OX0) * (IX1 - IX0); }
function my(py) { return IY0 + (py - OY0) / (OY1 - OY0) * (IY1 - IY0); }
function sw(px0, px1) { return (px1 - px0) / (OX1 - OX0) * (IX1 - IX0); }
function sh(py0, py1) { return (py1 - py0) / (OY1 - OY0) * (IY1 - IY0); }

const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const MANIFEST = require(BUILD + "/gen_slide_018_manifest.json");

// ---- HOUSE CHROME (house frame rule - overrides spec and judge) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("18", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Saturation Problem in Activation Functions", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- TOP ROW: definition cards ----
// Measured card fill is pale pink (median 250,233,215) with a coral border.
function eqCard(px0, px1, py0, py1, term, eqKey, headEnd) {
  const x = mx(px0), y = my(py0), w = sw(px0, px1), h = sh(py0, py1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.08,
    fill: { color: "FAE9D7" },
    line: { color: "FF4D4D", width: 1.5 },
  });
  // heading is right-aligned so it ends just left of the brace
  s.addText([
    { text: "F(x) = " },
    { text: term, options: { color: "C00000" } },
    { text: " Unit Step =" },
  ], {
    x: mx(px0 + 8), y: my(118), w: sw(px0 + 8, headEnd), h: sh(118, 141),
    align: "right", valign: "middle",
    fontSize: 13, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  // 2D piecewise equation (600-dpi PNG) placed at its measured frame box
  const eq = MANIFEST.equations[eqKey];
  const b = eq.box;
  s.addImage({
    path: BUILD + "/" + eq.image,
    x: mx(b[0]), y: my(b[1]), w: eq.w_in, h: eq.h_in,
  });
}
eqCard(78, 375, 109, 159, "Uni-polar", "unipolar", 281);
eqCard(550, 855, 107, 158, "Bi-polar", "bipolar", 738);

// ---- MIDDLE ROW: step-function panes ----
function stepPane(key) {
  const c = MANIFEST.charts[key];
  const b = c.box;
  s.addImage({
    path: BUILD + "/" + c.image,
    x: mx(b[0]), y: my(b[1]), w: sw(b[0], b[2]), h: sh(b[1], b[3]),
  });
}
stepPane("unipolar_step");
stepPane("bipolar_step");

// ---- CENTER CALLOUT (in the gap between the two step panes) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: mx(342), y: my(194), w: sw(342, 498), h: sh(194, 248),
  fill: { color: "F0FDE1" },
  line: { color: "FF4D4D", width: 1.5 },
});
s.addText("Saturation Problem", {
  x: mx(348), y: my(199), w: sw(348, 492), h: sh(199, 214),
  align: "center", valign: "middle",
  fontSize: 14, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Same Output value", options: { breakLine: true } },
  { text: "for Different input values" },
], {
  x: mx(348), y: my(214), w: sw(348, 492), h: sh(214, 243),
  align: "center", valign: "middle",
  fontSize: 13, color: "1F6FC0", fontFace: FONT, margin: 0,
});

// ---- DASHED RED CONNECTOR ----
// The original has exactly ONE dashed red arrow: a vertical dashed segment at
// x 201..208 running from the uni-polar pane's bottom edge (y=274) down to the
// sigmoid pane's top edge (y=321). Pixel traces of the reanalysis' "Y-fork"
// diagonals (610,268)->(483,307) and (610,268)->(730,307) contain no ink at
// all, so no fork is drawn.
s.addShape(pres.shapes.LINE, {
  x: mx(205), y: my(274), w: 0, h: sh(274, 321),
  line: { color: "C0392B", width: 1.25, dash: "dash", endArrowType: "triangle" },
});

// ---- BOTTOM ROW: three chart panels ----
function chart(key) {
  const c = MANIFEST.charts[key];
  const b = c.box;
  s.addImage({
    path: BUILD + "/" + c.image,
    x: mx(b[0]), y: my(b[1]), w: sw(b[0], b[2]), h: sh(b[1], b[3]),
  });
}
chart("sigmoid");
chart("tanh");
chart("arctan");

// ---- CAPTIONS below each panel ----
function caption(cx, text) {
  s.addText([
    { text: "f(x) = " },
    { text: text, options: { color: "C00000" } },
  ], {
    x: mx(cx) - 1.15, y: my(485), w: 2.3, h: sh(485, 504),
    align: "center", valign: "middle",
    fontSize: 20, italic: true, color: "000000", fontFace: "Times New Roman", margin: 0,
  });
}
caption(200, "Sigmoid(x)");
caption(506, "tanh(x)");
caption(773, "tan⁻¹(x)");

const outPath = "slide_018_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));
