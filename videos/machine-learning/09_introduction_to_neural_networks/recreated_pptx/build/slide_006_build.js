const pptxgen = require("pptxgenjs");

// Slide 006: Visualization of Single Layer Perceptron (Multi-Class)
const NUM = 6;
const TITLE = "Visualization of Single Layer Perceptron";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const GREEN = "008000";
const BORDER_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const PEACH = "FDEBD0";
const TAN = "E6D5B8";
const TAN_TEXT = "5C4A2A";
const LIGHT_BLUE = "C0C0FF";
const PURPLE = "D0B0FF";
const GRAY = "808080";
const INPUT_FILL = "E6F3FF";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
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
// Title: "Visualization of" (red), "Single Layer" (blue), "Perceptron" (red)
s.addText([
  { text: "Visualization of ", options: { color: RED, bold: true, fontSize: 30, fontFace: FONT } },
  { text: "Single Layer ", options: { color: BLUE, bold: true, fontSize: 30, fontFace: FONT } },
  { text: "Perceptron", options: { color: RED, bold: true, fontSize: 30, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Left column: Equation box (peach background, rounded rectangle)
// Position: left side, upper portion below title
const eq_x = 0.6;
let eq_y = 1.1;
const eq_w = 5.8;
const eq_h = 1.6;

s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: eq_x, y: eq_y, w: eq_w, h: eq_h,
  fill: { color: PEACH }, line: { color: "none" },
});

// Equation 1: d_1(X) = W_1^T X = w_{11}x_1 + w_{12}x_2 + ... + w_{1n}x_n + b_1 * 1
eq_y = eq_y + 0.15;
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/eq_s006_d1.png",
  x: eq_x + 0.15, y: eq_y, w: 6.12333, h: 0.345,
});

// Equation 2: d_2(X) = W_2^T X = w_{21}x_1 + w_{22}x_2 + ... + w_{2n}x_n + b_2 * 1
eq_y += 0.4;
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/eq_s006_d2.png",
  x: eq_x + 0.15, y: eq_y, w: 6.12333, h: 0.34667,
});

// Equation 3: d_m(X) = W_m^T X = w_{m1}x_1 + w_{m2}x_2 + ... + w_{mn}x_n + b_m * 1
eq_y += 0.4;
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/eq_s006_dm.png",
  x: eq_x + 0.15, y: eq_y, w: 6.465, h: 0.335,
});

// 5. Left column below equation box: "Multi-Class Classification" tan box
const class_x = 0.6;
const class_y = eq_y + 0.35 + 0.335;  // below last equation
const class_w = 5.8;
const class_h = 0.5;

s.addShape(pres.shapes.RECTANGLE, {
  x: class_x, y: class_y, w: class_w, h: class_h,
  fill: { color: TAN }, line: { color: "none" },
});
s.addText("Multi-Class Classification", {
  x: class_x + 0.15, y: class_y + 0.05, w: class_w - 0.3, h: class_h - 0.1,
  align: "center", valign: "middle",
  fontSize: 16, bold: false, color: TAN_TEXT, fontFace: FONT, margin: 0,
});

// 6. Right side: Embed the generated perceptron diagram
const diag_meta = require("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_perceptron_multiclass.json");
s.addImage({
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_perceptron_multiclass.png",
  x: diag_meta.position.x, y: diag_meta.position.y, w: diag_meta.position.w, h: diag_meta.position.h,
});

pres.writeFile({ 
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_recreated.pptx" 
}).then(() => console.log("wrote slide_006_recreated.pptx"));