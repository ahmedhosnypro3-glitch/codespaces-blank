const pptxgen = require("pptxgenjs");

// Slide 020: Saturation Problem in Activation Functions
// Geometry measured from unique_slides/slide_020.jpg (960x540 px, 1px = 1/72in).
const NUM = 20;
const TITLE = "Saturation Problem in Activation Functions";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const RED_BRIGHT = "FF0000";
const BLUE = "0000FF";
const GREEN = "00B050";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const GRID = "D9D9D9";

const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const GRAPH_DIR = BUILD_DIR + "/graphs_slide_020";

// px -> inches (540 px tall = 7.5 in)
const P = (px) => px / 72.0;

// Measured chart panel boxes (px x0,y0,x1,y1)
const TOP_PANEL = { x: P(338), y: P(116), w: P(616 - 338), h: P(277 - 116) };
const PRELU_PANEL = { x: P(83), y: P(335), w: P(320 - 83), h: P(474 - 335) };
const ELU_PANEL = { x: P(362), y: P(336), w: P(592 - 362), h: P(473 - 336) };
const SOFTPLUS_PANEL = { x: P(638), y: P(336), w: P(876 - 638), h: P(473 - 336) };

// ReLU definition box (upper-left), measured red outline px 71..336 x 102..141
const DEFBOX = { x: P(71), y: P(102), w: P(336 - 71), h: P(141 - 102) };
// Saturation Problem callout, measured ink px 117..289 x 189..239
const CALLOUT = { x: P(117), y: P(189), w: P(289 - 117), h: P(239 - 189) };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. Bottom black bar (video-player overlay in the original frame)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: P(515), w: W, h: H - P(515),
  fill: { color: BLACK }, line: { type: "none" },
});

// 3. Slide-number badge - HOUSE CHROME LAW
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 4. Title - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 5. ReLU definition box (red-outlined white rectangle, upper-left)
s.addShape(pres.shapes.RECTANGLE, {
  ...DEFBOX,
  fill: { color: WHITE }, line: { color: RED_BRIGHT, width: 1 },
});
// "F(x) = Rectified Linear Unit ="  (black italic / red italic)
s.addText([
  { text: "F(x) = ", options: { italic: true, color: BLACK } },
  { text: "Rectified Linear Unit", options: { italic: true, color: RED_BRIGHT } },
  { text: " =", options: { italic: true, color: BLACK } },
], {
  x: DEFBOX.x + 0.08, y: DEFBOX.y + 0.04, w: 2.35, h: 0.30,
  align: "left", valign: "middle",
  fontSize: 11, fontFace: FONT, margin: 0,
});
// vertical divider between the name and the piecewise definition
s.addShape(pres.shapes.LINE, {
  x: DEFBOX.x + 2.45, y: DEFBOX.y + 0.05, w: 0, h: DEFBOX.h - 0.10,
  line: { color: BLACK, width: 0.75 },
});
// piecewise rows: value (red) + condition (green)
s.addText([
  { text: "0", options: { bold: true, color: RED_BRIGHT } },
  { text: " for x < 0", options: { bold: true, color: GREEN } },
], {
  x: DEFBOX.x + 2.52, y: DEFBOX.y + 0.02, w: 1.6, h: 0.22,
  align: "left", valign: "middle",
  fontSize: 11, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "x", options: { bold: true, color: RED_BRIGHT } },
  { text: " for x > 0", options: { bold: true, color: GREEN } },
], {
  x: DEFBOX.x + 2.52, y: DEFBOX.y + 0.24, w: 1.6, h: 0.22,
  align: "left", valign: "middle",
  fontSize: 11, fontFace: FONT, margin: 0,
});

// 6. "F(x) = ReLU" heading above the top chart (measured px 330..615, rows 91..117)
s.addText([
  { text: "F(x) = ", options: { bold: true, italic: true, color: BLACK } },
  { text: "ReLU", options: { bold: true, italic: true, color: RED_BRIGHT } },
], {
  x: P(330), y: P(88), w: P(290), h: 0.34,
  align: "center", valign: "middle",
  fontSize: 14, fontFace: FONT, margin: 0,
});

// 7. Four activation-function charts (generated PNGs with baked blue borders)
s.addImage({ path: GRAPH_DIR + "/graph_relu.png", ...TOP_PANEL });
s.addImage({ path: GRAPH_DIR + "/graph_prelu.png", ...PRELU_PANEL });
s.addImage({ path: GRAPH_DIR + "/graph_elu.png", ...ELU_PANEL });
s.addImage({ path: GRAPH_DIR + "/graph_softplus.png", ...SOFTPLUS_PANEL });

// 8. Saturation Problem callout (red-outlined white box, middle-left)
s.addShape(pres.shapes.RECTANGLE, {
  ...CALLOUT,
  fill: { color: WHITE }, line: { color: RED_BRIGHT, width: 1 },
});
s.addText("Saturation Problem", {
  x: CALLOUT.x, y: CALLOUT.y + 0.02, w: CALLOUT.w, h: 0.24,
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: RED_BRIGHT, fontFace: FONT, margin: 0,
});
s.addText("Same Output value", {
  x: CALLOUT.x, y: CALLOUT.y + 0.26, w: CALLOUT.w, h: 0.22,
  align: "center", valign: "middle",
  fontSize: 11, color: BLUE, underline: true, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "for ", options: { color: BLUE } },
  { text: "Different", options: { color: BLUE, underline: true } },
  { text: " Input values", options: { color: BLUE } },
], {
  x: CALLOUT.x, y: CALLOUT.y + 0.48, w: CALLOUT.w, h: 0.22,
  align: "center", valign: "middle",
  fontSize: 11, fontFace: FONT, margin: 0,
});

// 9. Solid red arrow from the callout to the yellow ellipse in the ReLU plot.
//    Callout right edge x=4.01in; ellipse centre px ~423 x, 257 y.
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: CALLOUT.x + CALLOUT.w + 0.03, y: P(255), w: P(430) - (CALLOUT.x + CALLOUT.w) - 0.03, h: 0.14,
  fill: { color: RED_BRIGHT }, line: { color: RED_BRIGHT, width: 0.5 },
});

// 10. Three dashed red connector arrows from the top chart down to the bottom row.
//     Top chart bottom-centre px ~477 x, 277 y -> each bottom chart top-centre.
function dashedArrow(x0, y0, x1, y1) {
  s.addShape(pres.shapes.LINE, {
    x: x0, y: y0, w: x1 - x0, h: y1 - y0,
    line: { color: RED_BRIGHT, width: 1.5, dashType: "dash", endArrowType: "triangle" },
  });
}
dashedArrow(P(477), P(279), P(201), P(333));
dashedArrow(P(477), P(279), P(477), P(334));
dashedArrow(P(477), P(279), P(757), P(334));

// 11. Captions below the bottom charts (measured row band 470..500)
const CAP_Y = P(478);
const capW = 2.6;
s.addText([
  { text: "F(x) = ", options: { bold: true, italic: true, color: BLACK } },
  { text: "Parametric", options: { bold: true, italic: true, color: BLUE } },
  { text: " ReLU", options: { bold: true, italic: true, color: RED_BRIGHT } },
], {
  x: PRELU_PANEL.x + (PRELU_PANEL.w - capW) / 2, y: CAP_Y, w: capW, h: 0.30,
  align: "center", valign: "middle",
  fontSize: 13, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "F(x) = ", options: { bold: true, italic: true, color: BLACK } },
  { text: "ELU", options: { bold: true, italic: true, color: RED_BRIGHT } },
], {
  x: ELU_PANEL.x + (ELU_PANEL.w - capW) / 2, y: CAP_Y, w: capW, h: 0.30,
  align: "center", valign: "middle",
  fontSize: 13, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "F(x) = ", options: { bold: true, italic: true, color: BLACK } },
  { text: "SoftPlus", options: { bold: true, italic: true, color: RED_BRIGHT } },
], {
  x: SOFTPLUS_PANEL.x + (SOFTPLUS_PANEL.w - capW) / 2, y: CAP_Y, w: capW, h: 0.30,
  align: "center", valign: "middle",
  fontSize: 13, fontFace: FONT, margin: 0,
});

const outPptx = BUILD_DIR + "/slide_020_recreated.pptx";
pres.writeFile({ fileName: outPptx }).then(() => console.log("wrote " + outPptx));
