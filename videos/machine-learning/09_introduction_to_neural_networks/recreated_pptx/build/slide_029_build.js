const pptxgen = require("pptxgenjs");

// Slide 029: Neural Network Model
// Geometry from PIL measurement of unique_slides/slide_029.jpg (960x540 -> 13.33x7.5 in).
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
const BEIGE = "E8E0D0";
const LIGHT_BEIGE = "F2E4D0";

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
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 3. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Input Sample (x0.89-1.76) / Target Label (x8.48-9.37), y1.33-1.74, magenta
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.89, y: 1.33, w: 0.87, h: 0.41,
  fill: { color: MAGENTA_FILL }, line: { color: MAGENTA_BORDER, width: 1.5 },
});
s.addText([
  { text: "Input", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT } },
  { text: "Sample", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT } },
], {
  x: 0.89, y: 1.33, w: 0.87, h: 0.41,
  align: "center", valign: "middle",
  margin: 0, lineSpacingMultiple: 0.9,
});

s.addShape(pres.shapes.RECTANGLE, {
  x: 8.48, y: 1.32, w: 0.89, h: 0.42,
  fill: { color: MAGENTA_FILL }, line: { color: MAGENTA_BORDER, width: 1.5 },
});
s.addText([
  { text: "Target", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT } },
  { text: "Label", options: { fontSize: 12, bold: true, color: BLACK, fontFace: FONT } },
], {
  x: 8.48, y: 1.32, w: 0.89, h: 0.42,
  align: "center", valign: "middle",
  margin: 0, lineSpacingMultiple: 0.9,
});

// Dashed magenta arrow from Input Sample to Target Label at their mid-height (~1.53in)
s.addShape(pres.shapes.LINE, {
  x: 1.76, y: 1.53, w: 6.72, h: 0,
  line: { color: MAGENTA_BORDER, width: 1.5, dashType: "dash" },
  lineTail: true,
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 8.33, y: 1.48, w: 0.15, h: 0.1,
  fill: { color: MAGENTA_BORDER }, line: { color: MAGENTA_BORDER, width: 0.5 },
});

// 5. Neural network diagram - beige panel x0.94-7.55, y1.92-5.35 (generated image)
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_diagram.png",
  x: 0.94, y: 1.92, w: 6.61, h: 3.43,
});

// 6. Vertical dark-red "Error Error Error" bar + rotated white text (x7.71-7.94, y2.10-5.03).
// Text is pre-rotated to 600dpi PNG so LibreOffice/PowerPoint renders it reliably.
s.addShape(pres.shapes.RECTANGLE, {
  x: 7.71, y: 2.10, w: 0.23, h: 2.93,
  fill: { color: RED }, line: { color: RED, width: 0 },
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_errlabel.png",
  x: 7.705, y: 2.10, w: 0.24, h: 2.93,
});

// 7. Class labels: pale-green boxes x8.0-8.93, centered y 2.42 / 3.45 / 4.55
const class_y = [2.42, 3.45, 4.55];
const class_labels = ["Class 1", "Class 2", "Class m"];
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.00, y: class_y[i] - 0.19, w: 0.93, h: 0.38,
    fill: { color: LIGHT_GREEN_BG }, line: { color: DARK_GREEN, width: 1.5 },
  });
  s.addText(class_labels[i], {
    x: 8.00, y: class_y[i] - 0.19, w: 0.93, h: 0.38,
    align: "center", valign: "middle",
    fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// 8. Legend box: light beige, red border, x9.07-12.34, y1.93-3.44
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.07, y: 1.93, w: 3.27, h: 1.51,
  fill: { color: LIGHT_BEIGE }, line: { color: RED, width: 1.5 },
});
const legend_items = [
  { symbol: "Net_j", meaning: "Summation at Node j" },
  { symbol: "O_j", meaning: "Output at Node j" },
  { symbol: "w_ji", meaning: "Weight from Node i to Node j" },
];
let legend_text_y = 1.99;
for (const item of legend_items) {
  s.addText([
    { text: item.symbol + " ", options: { color: RED, bold: true, italic: true, fontSize: 11, fontFace: FONT } },
    { text: "\u21d2 ", options: { color: BLACK, fontSize: 11, fontFace: FONT } },
    { text: item.meaning, options: { color: BLACK, fontSize: 11, fontFace: FONT } },
  ], {
    x: 9.20, y: legend_text_y, w: 3.0, h: 0.45,
    align: "left", valign: "top",
    fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
  });
  legend_text_y += 0.47;
}

// 9. Node-count note box: white, red border, x8.75-12.33, y3.78-4.42
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.75, y: 3.78, w: 3.58, h: 0.64,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
s.addText([
  { text: "Number of I/P Nodes = Input Vector Length", options: { breakLine: true } },
  { text: "Number of O/P Nodes = Number of classes" },
], {
  x: 8.87, y: 3.84, w: 3.34, h: 0.52,
  align: "left", valign: "middle",
  fontSize: 10, color: BLACK, fontFace: FONT, margin: 0, lineSpacingMultiple: 0.95,
});

// 10. Layer callouts beneath the diagram panel.
// Blue callout box x3.11-4.21 y5.61-5.96 with a hollow up-arrow above it at y~5.30-5.58.
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_arrow_blue.png",
  x: 3.95, y: 5.22, w: 0.44, h: 0.36,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.11, y: 5.61, w: 1.10, h: 0.35,
  fill: { color: LIGHT_BLUE_BG }, line: { color: BLUE, width: 1.5 },
});
s.addText([
  { text: "Previous Layer", options: { fontSize: 9, color: BLACK, fontFace: FONT } },
  { text: "Layer (i)", options: { fontSize: 9, color: BLACK, fontFace: FONT } },
], {
  x: 3.11, y: 5.61, w: 1.10, h: 0.35,
  align: "center", valign: "middle", margin: 0, lineSpacingMultiple: 0.85,
});
// Green callout box x5.87-6.65 y5.61-5.96 with a hollow up-arrow above it.
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_arrow_green.png",
  x: 6.04, y: 5.22, w: 0.44, h: 0.36,
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 5.60, y: 5.61, w: 1.05, h: 0.35,
  fill: { color: LIGHT_GREEN_BG2 }, line: { color: DARK_GREEN, width: 1.5 },
});
s.addText([
  { text: "Current Layer", options: { fontSize: 9, color: BLACK, fontFace: FONT } },
  { text: "(You are here)", options: { fontSize: 9, color: BLACK, fontFace: FONT } },
], {
  x: 5.60, y: 5.61, w: 1.05, h: 0.35,
  align: "center", valign: "middle", margin: 0, lineSpacingMultiple: 0.85,
});

// 11. Bottom formula row, y6.25-6.96 (above the letterbox strip of the original)
// Left: header + Net_j summation
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.03, y: 6.25, w: 2.33, h: 0.30,
  fill: { color: WHITE }, line: { color: GRAY, width: 1 },
});
s.addText("For Layer \u201cj\u201d", {
  x: 1.03, y: 6.25, w: 2.33, h: 0.30,
  align: "center", valign: "middle",
  fontSize: 11, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_eq_net.png",
  x: 1.30, y: 6.57, w: 0.71, h: 0.23,
});
// Center: sigmoid formula in a pale-yellow box x4.11-6.93
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.11, y: 6.18, w: 2.82, h: 0.78,
  fill: { color: PALE_YELLOW }, line: { color: GRAY, width: 1 },
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_eq_sigmoid.png",
  x: 4.22, y: 6.34, w: 1.10, h: 0.16,
});
// Right: header + error formula, x9.22-12.07
s.addShape(pres.shapes.RECTANGLE, {
  x: 9.22, y: 6.25, w: 2.85, h: 0.30,
  fill: { color: WHITE }, line: { color: GRAY, width: 1 },
});
s.addText("If Layer \u201cj\u201d is Output Layer:", {
  x: 9.22, y: 6.25, w: 2.85, h: 0.30,
  align: "center", valign: "middle",
  fontSize: 11, italic: true, color: RED, fontFace: FONT, margin: 0,
});
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_eq_error.png",
  x: 9.35, y: 6.57, w: 0.83, h: 0.25,
});

// Write the PPTX
pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_029_recreated.pptx"
}).then(() => console.log("wrote slide_029_recreated.pptx"));
