const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.333, H = 7.5;

let slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// House chrome: gray panel, red strokes (L/R/bottom only), badge numeral "16"
drawHouseChrome(pres, slide, { numeral: "16" });

/*
 * SLIDE-SPECIFIC CONTENT — rebuilt from PIL measurement of slide_016.jpg.
 * Frame px (960x540, 1px=1pt=1/72in) for every line y-mid, left edge,
 * colour span and mark. See scratch/tmp/geom016.py.
 */

const FONT = "Arial";

// Inner white content frame with thin blue border (original border cores x82..83 / x832..833, y91..92 / y532..533)
const boxX = 83.5 / 72, boxY = 92.5 / 72;
const boxW = 750 / 72, boxH = 440 / 72;
slide.addShape("rect", {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: "FFFFFF" },
  line: { color: "2B237A", width: 1.5 },
});

// Yellow highlight behind "better generalization" (original x287..456, y176..197)
slide.addShape("rect", {
  x: 287 / 72, y: 176 / 72, w: (456 - 287) / 72, h: (197 - 176) / 72,
  fill: { color: "FFFF00" },
});

// Red underline beneath "customized weigh factor" (original x110..300, y296..297)
slide.addShape("rect", {
  x: 110 / 72, y: 296.5 / 72, w: (300 - 110) / 72, h: 1 / 72,
  fill: { color: "C00000" },
});

// Short dark underline beneath "Length" on the last bullet (original x109..163, y525)
slide.addShape("rect", {
  x: 109 / 72, y: 525 / 72, w: (163 - 109) / 72, h: 1 / 72,
  fill: { color: "333333" },
});

// Black underline beneath "Small number of samples" on b5a (original x446..640, y500)
slide.addShape("rect", {
  x: 445 / 72, y: 500 / 72, w: (641 - 445) / 72, h: 1 / 72,
  fill: { color: "333333" },
});

// Black underline beneath "Large vector" on b5a (original x710..806, y500)
slide.addShape("rect", {
  x: 709 / 72, y: 500 / 72, w: (807 - 709) / 72, h: 1 / 72,
  fill: { color: "333333" },
});

// Title (measured: original ink x312..621, y61..86 -> ~27pt bold, centred at x466.5, mid-y 73)
slide.addText("L\u2081 and L\u2082 Regularization", {
  x: 0.479, y: 0.612, w: 12.0, h: 0.75,
  align: "center", valign: "middle",
  fontSize: 27, bold: true, color: "8B0000",
  fontFace: FONT, margin: 0,
});

// Body text: one box per original line, at the measured mid-y and left edge
// h1: y112 x110
slide.addText([
  { text: "Regularizers are based on:", options: { color: "C00000", fontSize: 17, bold: true, fontFace: "Arial" } },
], {
  x: 110 / 72, y: 1.3819, w: 10.0000, h: 0.3472,
  margin: 0, valign: "middle",
});

// h2: y137 x146
slide.addText([
  { text: "Penalize large values of W", options: { color: "0000FF", fontSize: 17, bold: true, fontFace: "Arial" } },
  { text: " (model parameters)", options: { color: "000000", fontSize: 17, bold: true, fontFace: "Arial" } },
], {
  x: 146 / 72, y: 1.7292, w: 9.5000, h: 0.3472,
  margin: 0, valign: "middle",
});

// b1: y187 x95
slide.addText([
  { text: "\u2022 This have the effect of better generalization of the model", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 95 / 72, y: 2.4236, w: 10.2083, h: 0.3472,
  margin: 0, valign: "middle",
});

// b2a: y239 x95
slide.addText([
  { text: "\u2022 Since there is a contradiction between model training (using training dataset) and model", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 95 / 72, y: 3.1458, w: 10.2083, h: 0.3472,
  margin: 0, valign: "middle",
});

// b2b: y264 x110
slide.addText([
  { text: "generalization, the regularization term is added to the objective loss function with a", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 110 / 72, y: 3.4931, w: 10.0000, h: 0.3472,
  margin: 0, valign: "middle",
});

// b2c: y289 x110
slide.addText([
  { text: "customized weigh factor (do regularization to what extent)", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 110 / 72, y: 3.8403, w: 10.0000, h: 0.3472,
  margin: 0, valign: "middle",
});

// b3a: y341 x95
slide.addText([
  { text: "\u2022 Penalization may be applied on the ", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: "Squared Norm of the Weight Vector", options: { color: "C00000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 95 / 72, y: 4.5625, w: 10.2083, h: 0.3472,
  margin: 0, valign: "middle",
});

// b3b: y366 x146
slide.addText([
  { text: "This is called ", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: "L\u2082 regularization", options: { color: "0000FF", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: " (also know as ", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: "Ridge Regularization )", options: { color: "0000FF", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 146 / 72, y: 4.9097, w: 9.5000, h: 0.3472,
  margin: 0, valign: "middle",
});

// b4a: y417 x95
slide.addText([
  { text: "\u2022 Penalization may also be applied on the ", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: "sum of Absolute values of the Weight Vector", options: { color: "C00000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 95 / 72, y: 5.6181, w: 10.2083, h: 0.3472,
  margin: 0, valign: "middle",
});

// b4b: y442 x146
slide.addText([
  { text: "This is called ", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: "L\u2081 regularization", options: { color: "0000FF", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 146 / 72, y: 5.9653, w: 9.5000, h: 0.3472,
  margin: 0, valign: "middle",
});

// b5a: y493 x95
slide.addText([
  { text: "\u2022 Regularization is particularly important for Small number of samples ", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: "(N)", options: { color: "C00000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: " and Large vector", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 95 / 72, y: 6.6736, w: 10.2083, h: 0.3472,
  margin: 0, valign: "middle",
});

// b5b: y516 x110
slide.addText([
  { text: "Length ", options: { color: "000000", fontSize: 18, bold: false, fontFace: "Arial" } },
  { text: "(d)", options: { color: "C00000", fontSize: 18, bold: false, fontFace: "Arial" } },
], {
  x: 110 / 72, y: 6.9931, w: 10.0000, h: 0.3472,
  margin: 0, valign: "middle",
});

const outPath = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_016_recreated.pptx";
pres.writeFile({ fileName: outPath }).then(() => console.log("done"));
