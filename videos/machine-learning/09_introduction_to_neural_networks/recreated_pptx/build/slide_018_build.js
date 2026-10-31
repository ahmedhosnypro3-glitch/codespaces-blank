// Build slide 018: Saturation Problem in Activation Functions (badge 18)
//
// Frame-measured geometry (unique_slides/slide_018.jpg 960x540, PIL line detection):
//   outer red frame   x  57..903  y  43..517
//   left eq card      x  76..377  y 104..158
//   right eq card     x 548..857  y 104..158
//   left step pane    x  70..340  y 168..274
//   right step pane   x 509..780  y 168..274
//   callout           x 347..496  y 195..246
//   bottom charts     x  74..336 / 390..635 / 655..890, y 324..478
//   caption row       y 485..503, centred at x 200 / 512 / 772
// The black band at y 518..539 is a lecture capture artifact repeated on every
// frame of this lecture; it is omitted. Equations render as 600-dpi 2D PNGs.
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
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- TOP ROW: definition cards ----
function eqCard(px0, px1, py0, py1, term, eqKey) {
  const x = mx(px0), y = my(py0), w = sw(px0, px1), h = sh(py0, py1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: "F5E6D5" },
    line: { color: "FF4D4D", width: 1.5 },
  });
  // heading sits on the first case line: "F(x) = " + term + " Unit Step ="
  const hy = my(130.5) - sh(0, 22) / 2;
  s.addText([
    { text: "F(x) = " },
    { text: term, options: { color: "C00000" } },
    { text: " Unit Step =" },
  ], {
    x: mx(86), y: hy, w: sw(86, 281), h: sh(0, 22),
    align: "left", valign: "middle",
    fontSize: 13, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
  // 2D piecewise equation (600-dpi PNG), first case line aligned with the heading
  const eq = MANIFEST.equations[eqKey];
  const ew = eq.w_in;
  const eh = eq.h_in;
  const ex = mx(283);
  const ey = my(130.5) - eq.line1_frac * eh;
  s.addImage({ path: BUILD + "/" + eq.image, x: ex, y: ey, w: ew, h: eh });
}
eqCard(76, 377, 104, 158, "Uni-polar", "unipolar");
eqCard(548, 857, 104, 158, "Bi-polar", "bipolar");

// ---- MIDDLE ROW: step-function panes ----
function stepPane(px0, px1, key) {
  const c = MANIFEST.charts[key];
  const w = sw(px0, px1), h = w * (c.h_px / c.w_px);
  s.addImage({
    path: BUILD + "/" + c.image,
    x: mx(px0), y: my(168), w: w, h: h,
  });
}
stepPane(70, 340, "unipolar_step");
stepPane(509, 780, "bipolar_step");

// ---- CENTER CALLOUT ----
s.addShape(pres.shapes.RECTANGLE, {
  x: mx(347), y: my(195), w: sw(347, 496), h: sh(195, 246),
  fill: { color: "FFF9EC" },
  line: { color: "FF4D4D", width: 1.5 },
});
s.addText("Saturation Problem", {
  x: mx(350), y: my(200), w: sw(350, 493), h: sh(200, 214),
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Same Output value" },
  { text: " for Different input values", options: { italic: true } },
], {
  x: mx(350), y: my(215), w: sw(350, 493), h: sh(215, 240),
  align: "center", valign: "middle",
  fontSize: 10, color: "1F6FC0", fontFace: FONT, margin: 0,
});

// ---- DASHED RED CONNECTORS (left arrow + right Y-fork) ----
const DASH = { color: "C0392B", width: 1.25, dash: "dash", endArrowType: "triangle" };
s.addShape(pres.shapes.LINE, {
  x: mx(195), y: my(274), w: 0, h: sh(274, 322), line: DASH,
});
s.addShape(pres.shapes.LINE, {
  x: mx(610), y: my(274), w: 0, h: sh(274, 292), line: { color: "C0392B", width: 1.25, dash: "dash" },
});
s.addShape(pres.shapes.LINE, {
  x: mx(483), y: my(292), w: sw(483, 610), h: sh(292, 322),
  flipH: true, line: DASH,
});
s.addShape(pres.shapes.LINE, {
  x: mx(610), y: my(292), w: sw(610, 730), h: sh(292, 322), line: DASH,
});

// ---- BOTTOM ROW: three chart panels ----
function chart(px0, px1, py0, py1, key) {
  const c = MANIFEST.charts[key];
  const w = sw(px0, px1), h = w * (c.h_px / c.w_px);
  s.addImage({
    path: BUILD + "/" + c.image,
    x: mx(px0), y: my(py0), w: w, h: h,
  });
}
chart(74, 336, 324, 478, "sigmoid");
chart(390, 635, 324, 478, "tanh");
chart(655, 890, 324, 478, "arctan");

// ---- CAPTIONS below each panel ----
function caption(cx, text) {
  s.addText([
    { text: "f(x) = " },
    { text: text, options: { color: "C00000" } },
  ], {
    x: mx(cx) - 0.9, y: my(485), w: 1.8, h: sh(485, 503),
    align: "center", valign: "middle",
    fontSize: 12, italic: true, color: "000000", fontFace: "Times New Roman", margin: 0,
  });
}
caption(200, "Sigmoid(x)");
caption(512, "tanh(x)");
caption(772, "tan⁻¹(x)");

const outPath = "slide_018_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));
