// Build slide 018: Saturation Problem in Activation Functions (badge 18)
//
// Frame-measured geometry (unique_slides/slide_018.jpg, content region x 59..902, y 44..516):
//   left eq card       x  73..379  y 106..161   tan fill, red brace piecewise
//   right eq card      x 545..860  y 104..160
//   left step pane     x  70..340  y 168..275   blue border, red step, yellow ellipses
//   right step pane    x 509..779  y 168..275
//   callout            x 346..507  y 192..250   white fill, yellow border, blue italic "Different"
//   bottom panels      x 77..333 / 394..632 / 658..887, y 325..477
//   captions           x 143..258 / 460..553 / 725..821, y 481..505
// Black band at y 518..539 is a full-width black strip repeated identically across every
// frame of this lecture; OMinor artifact. Equations render as 600dpi 2D PNGs (never linear).
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";

// Original content region maps onto the house frame's inner area
const OX0 = 59, OX1 = 902, OY0 = 44, OY1 = 516;
const IX0 = 0.15, IX1 = 0.15 + 13.03, IY0 = 0.15, IY1 = 0.15 + 7.2;
function mx(px) { return IX0 + (px - OX0) / (OX1 - OX0) * (IX1 - IX0); }
function my(py) { return IY0 + (py - OY0) / (OY1 - OY0) * (IY1 - IY0); }
function mw(px) { return (px - OX0) / (OX1 - OX0) * (IX1 - IX0); }
function mh(py) { return (py - OY0) / (OY1 - OY0) * (IY1 - IY0); }

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
// Title - centered, starts y=0.28
s.addText("Saturation Problem in Activation Functions", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- SLIDE CONTENT ----
const EQ_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";

// TOP ROW: two equation cards with 2D piecewise equations
function eqCard(px0, px1, py0, py1, heading, eqImg, eqWIn, eqHIn) {
  const x = mx(px0), y = my(py0), w = mw(px1), h = mh(py1);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: "F5E9D7" },
    line: { color: "C9BFA8", width: 1 },
  });
  // heading: "F(x) = " red + term in dark red, single centered line
  s.addText(heading, {
    x: x + 0.05, y: y + 0.03, w: w - 0.1, h: 0.28,
    align: "left", valign: "middle",
    fontSize: 11, bold: true, color: "B03A2E", fontFace: FONT, margin: 0,
  });
  // 2D piecewise equation (600dpi PNG) at exact px/600 size
  const ex = x + 0.42, ey = y + 0.33;
  s.addImage({ path: EQ_DIR + "/" + eqImg, x: ex, y: ey, w: eqWIn, h: eqHIn });
}

// LEFT: Uni-polar  (measurements: heading ink x88..282, brace x285..298)
eqCard(78, 380, 106, 162, "F(x) = Uni-polar Unit Step", "eq_018_unipolar.png", 0.72, 0.22);
// RIGHT: Bi-polar
eqCard(540, 868, 104, 162, "F(x) = Bi-polar Unit Step", "eq_018_bipolar.png", 0.72, 0.22);

// MIDDLE ROW: step-graph panes (blue border drawn inside the generated PNGs)
s.addImage({
  path: EQ_DIR + "/slide_018_unipolar_step.png",
  x: mx(68), y: my(166), w: mw(342), h: mh(277),
});
s.addImage({
  path: EQ_DIR + "/slide_018_bipolar_step.png",
  x: mx(507), y: my(166), w: mw(781), h: mh(277),
});

// CENTER CALLOUT: white fill, yellow border, blue italic "Different"
(function callout() {
  const x = mx(346), y = my(190), w = mw(509), h = mh(252);
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: "FFFFFF" },
    line: { color: "F2E94E", width: 1.5 },
  });
  s.addText("Saturation Problem", {
    x: x + 0.03, y: y + 0.03, w: w - 0.06, h: 0.22,
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: "B03A2E", fontFace: FONT, margin: 0,
  });
  s.addText([
    { text: "Same Output value for " },
    { text: "Different", options: { italic: true, color: "4169E1" } },
    { text: " input values" },
  ], {
    x: x + 0.03, y: y + 0.24, w: w - 0.06, h: 0.42,
    align: "center", valign: "top",
    fontSize: 9, color: "333333", fontFace: FONT, margin: 0,
  });
})();

// Dashed red connectors from the callout fork down to the sigmoid / arctan panels
s.addShape(pres.shapes.LINE, {
  x: mx(411), y: my(250), w: 0, h: mh(331) - my(250),
  line: { color: "C0392B", width: 1.25, dash: "dash" },
});
s.addShape(pres.shapes.LINE, {
  x: mx(441), y: my(250), w: 0, h: mh(331) - my(250),
  line: { color: "C0392B", width: 1.25, dash: "dash" },
});

// BOTTOM ROW: three charts
s.addImage({
  path: EQ_DIR + "/slide_018_sigmoid.png",
  x: mx(75), y: my(323), w: mw(335), h: mh(479),
});
s.addImage({
  path: EQ_DIR + "/slide_018_tanh.png",
  x: mx(392), y: my(325), w: mw(634), h: mh(479),
});
s.addImage({
  path: EQ_DIR + "/slide_018_arctan.png",
  x: mx(656), y: my(326), w: mw(889), h: mh(479),
});
// Captions below each panel (measured y 481..505)
function caption(px0, px1, text) {
  s.addText(text, {
    x: mx(px0) - 0.1, y: my(480), w: mw(px1) - mx(px0) + 0.2, h: 0.26,
    align: "center", valign: "middle",
    fontSize: 11, color: "333333", fontFace: FONT, margin: 0,
  });
}
caption(140, 261, "f(x) = Sigmoid(x)");
caption(457, 556, "f(x) = tanh(x)");
caption(722, 824, "f(x) = tan\u207B\u00B9(x)");

const outPath = "slide_018_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("wrote", outPath));
