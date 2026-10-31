const pptxgen = require("pptxgenjs");

// Slide 029: Neural Network Model
// All geometry measured with PIL from unique_slides/slide_029.jpg (960x540 -> 72 px/in).
const NUM = 29;
const TITLE = "Neural Network Model";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const GRAY = "808080";
const MAGENTA_FILL = "E6A0E6";
const MAGENTA_BORDER = "9932CC";
const BLUE = "0070C0";
const DARK_GREEN = "00B050";
const LIGHT_GREEN_BG = "D9EAD3";
const LIGHT_BLUE_BG = "DDEBF7";
const LIGHT_GREEN_BG2 = "E2EFDA";
const PALE_YELLOW = "FFFDE7";
const LIGHT_BEIGE = "F2E4D0";

const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";

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

// 2. Slide-number badge - HOUSE CHROME LAW (yellow circle at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Input Sample box x0.889-1.764 y1.347-1.736 ; Target Label box x8.500-9.361 y1.319-1.736
// Both carry their wording on TWO lines with the internal space preserved.
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.889, y: 1.333, w: 0.875, h: 0.41,
  fill: { color: MAGENTA_FILL }, line: { color: MAGENTA_BORDER, width: 1.5 },
});
s.addText([
  { text: "Input ", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT } },
  { text: "Sample", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT, breakLine: true } },
], {
  x: 0.889, y: 1.333, w: 0.875, h: 0.41,
  align: "center", valign: "middle",
  margin: 0, lineSpacingMultiple: 0.85,
});

s.addShape(pres.shapes.RECTANGLE, {
  x: 8.500, y: 1.319, w: 0.861, h: 0.417,
  fill: { color: MAGENTA_FILL }, line: { color: MAGENTA_BORDER, width: 1.5 },
});
s.addText([
  { text: "Target ", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT } },
  { text: "Label", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT, breakLine: true } },
], {
  x: 8.500, y: 1.319, w: 0.861, h: 0.417,
  align: "center", valign: "middle",
  margin: 0, lineSpacingMultiple: 0.85,
});

// Dashed magenta arrow from the Input Sample box to the Target Label box.
s.addShape(pres.shapes.LINE, {
  x: 1.764, y: 1.52, w: 6.56, h: 0,
  line: { color: MAGENTA_BORDER, width: 1.5, dashType: "dash" },
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 8.34, y: 1.47, w: 0.16, h: 0.10,
  fill: { color: MAGENTA_BORDER }, line: { color: MAGENTA_BORDER, width: 0.5 },
});

// 5. Neural network panel: generated image, x0.931-7.569 y1.917-5.361 (6.638 x 3.444 in).
// The panel holds ONLY the network - the error bar and class column are separate shapes.
s.addImage({
  path: `${BUILD}/slide_029_diagram.png`,
  x: 0.931, y: 1.917, w: 6.638, h: 3.444,
});

// 6. Vertical dark-red "Error Error Error" bar x7.708-7.931 y2.097-5.028 (ONE only).
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.708, y: 2.097, w: 0.223, h: 2.931,
  fill: { color: RED }, line: { color: RED, width: 0 },
});
s.addImage({
  path: `${BUILD}/slide_029_errlabel.png`,
  x: 7.708, y: 2.097, w: 0.223, h: 2.931,
});

// 7. Class labels: pale-green boxes x8.000-8.900, centres y2.46 / 3.43 / 4.62.
const class_y = [2.46, 3.43, 4.62];
const class_labels = ["Class 1", "Class 2", "Class m"];
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.000, y: class_y[i] - 0.19, w: 0.90, h: 0.38,
    fill: { color: LIGHT_GREEN_BG }, line: { color: DARK_GREEN, width: 1.5 },
  });
  s.addText(class_labels[i], {
    x: 8.000, y: class_y[i] - 0.19, w: 0.90, h: 0.38,
    align: "center", valign: "middle",
    fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// 8. Legend box: beige fill, red border, x9.06-12.39 y1.93-3.24.
// Three lines, ink rows centred at y2.33 / 2.62 / 2.99.
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.06, y: 1.93, w: 3.33, h: 1.31,
  fill: { color: LIGHT_BEIGE }, line: { color: RED, width: 1.5 },
});
const legend_items = [
  { symbol: "Net_j", meaning: "Summation at Node j" },
  { symbol: "O_j", meaning: "Output at Node j" },
  { symbol: "w_ji", meaning: "Weight from Node i to Node j" },
];
let legend_text_y = 2.19;
for (const item of legend_items) {
  s.addText([
    { text: item.symbol + " ", options: { color: RED, bold: true, italic: true, fontSize: 11, fontFace: FONT } },
    { text: "\u21d2 ", options: { color: BLACK, fontSize: 11, fontFace: FONT } },
    { text: item.meaning, options: { color: BLACK, fontSize: 11, fontFace: FONT } },
  ], {
    x: 9.17, y: legend_text_y, w: 3.10, h: 0.26,
    align: "left", valign: "middle",
    fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
  });
  legend_text_y += 0.29;
}

// 9. Node-count note box: white, red border, x8.750-12.333 y3.778-4.431.
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.750, y: 3.778, w: 3.583, h: 0.653,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
s.addText([
  { text: "Number of I/P Nodes = Input Vector Length", options: { breakLine: true } },
  { text: "Number of O/P Nodes = Number of classes" },
], {
  x: 8.87, y: 3.86, w: 3.35, h: 0.49,
  align: "left", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0, lineSpacingMultiple: 0.95,
});

// 10. Layer callouts beneath the panel.
// Blue: hollow up-arrow x3.57-3.75 y5.33-5.54 ; box x3.07-4.28 y5.56-5.99.
s.addImage({
  path: `${BUILD}/slide_029_arrow_blue.png`,
  x: 3.57, y: 5.33, w: 0.18, h: 0.21,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.07, y: 5.56, w: 1.21, h: 0.43,
  fill: { color: LIGHT_BLUE_BG }, line: { color: BLUE, width: 1.5 },
});
s.addText([
  { text: "Previous Layer", options: { fontSize: 9, color: BLACK, fontFace: FONT, breakLine: true } },
  { text: "Layer (i)", options: { fontSize: 9, color: BLACK, fontFace: FONT } },
], {
  x: 3.07, y: 5.56, w: 1.21, h: 0.43,
  align: "center", valign: "middle", margin: 0, lineSpacingMultiple: 0.85,
});
// Green: hollow up-arrow x5.85-6.04 y5.28-5.54 ; box x5.33-6.58 y5.56-5.99.
s.addImage({
  path: `${BUILD}/slide_029_arrow_green.png`,
  x: 5.85, y: 5.28, w: 0.19, h: 0.26,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.33, y: 5.56, w: 1.25, h: 0.43,
  fill: { color: LIGHT_GREEN_BG2 }, line: { color: DARK_GREEN, width: 1.5 },
});
s.addText([
  { text: "Current Layer", options: { fontSize: 9, color: BLACK, fontFace: FONT, breakLine: true } },
  { text: "(You are here)", options: { fontSize: 9, color: BLACK, fontFace: FONT } },
], {
  x: 5.33, y: 5.56, w: 1.25, h: 0.43,
  align: "center", valign: "middle", margin: 0, lineSpacingMultiple: 0.85,
});

// 11. Bottom formula row.
// LEFT   white header "For Layer j" x1.028-2.681 y6.028-6.319
//        pale-yellow formula box x1.028-3.403 y6.417-6.931
// CENTER pale-yellow formula box x4.097-6.944 y6.361-6.917
// RIGHT  white header x9.222-11.833 y5.833-6.111
//        pale-yellow formula box x9.222-12.083 y6.250-6.958
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.028, y: 6.028, w: 1.653, h: 0.291,
  fill: { color: WHITE }, line: { color: GRAY, width: 1 },
});
s.addText("For Layer \u201cj\u201d", {
  x: 1.028, y: 6.028, w: 1.653, h: 0.291,
  align: "center", valign: "middle",
  fontSize: 10, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.028, y: 6.417, w: 2.375, h: 0.514,
  fill: { color: PALE_YELLOW }, line: { color: GRAY, width: 1 },
});
s.addImage({
  path: `${BUILD}/slide_029_eq_net.png`,
  x: 1.028 + (2.375 - 1.427) / 2, y: 6.417 + (0.514 - 0.472) / 2,
  w: 1.427, h: 0.472,
});

s.addShape(pres.shapes.RECTANGLE, {
  x: 4.097, y: 6.361, w: 2.847, h: 0.556,
  fill: { color: PALE_YELLOW }, line: { color: GRAY, width: 1 },
});
s.addImage({
  path: `${BUILD}/slide_029_eq_sigmoid.png`,
  x: 4.097 + (2.847 - 2.195) / 2, y: 6.361 + (0.556 - 0.327) / 2,
  w: 2.195, h: 0.327,
});

s.addShape(pres.shapes.RECTANGLE, {
  x: 9.222, y: 5.833, w: 2.611, h: 0.278,
  fill: { color: WHITE }, line: { color: GRAY, width: 1 },
});
s.addText("If Layer \u201cj\u201d is Output Layer:", {
  x: 9.222, y: 5.833, w: 2.611, h: 0.278,
  align: "center", valign: "middle",
  fontSize: 10, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.222, y: 6.250, w: 2.861, h: 0.708,
  fill: { color: PALE_YELLOW }, line: { color: GRAY, width: 1 },
});
s.addImage({
  path: `${BUILD}/slide_029_eq_error.png`,
  x: 9.222 + (2.861 - 1.655) / 2, y: 6.250 + (0.708 - 0.503) / 2,
  w: 1.655, h: 0.503,
});

// Write the PPTX
pres.writeFile({
  fileName: `${BUILD}/slide_029_recreated.pptx`
}).then(() => console.log("wrote slide_029_recreated.pptx"));
