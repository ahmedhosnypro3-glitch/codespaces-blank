// slide_039.js — "Bonus Assignment (SVM with Kernels)"
// Bullet points in blue-bordered box
// Run: NODE_PATH=$(npm root -g) node slide_039.js

const pptxgen = require("pptxgenjs");
const { newPres, addHouseChrome, W, H, FONT } = require("./shared.js");

const NUM = 39;
const TITLE = "Bonus Assignment (SVM with Kernels)";

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, TITLE);

// Blue-bordered content box
const boxX = 0.8;
const boxY = 1.1;
const boxW = 11.73;
const boxH = 5.6;

s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { type: "none" }, line: { color: "0000FF", width: 1.5 },
});

// Bullets inside the box (dark blue/navy)
const bullets = [
  { text: "Develop your own SVM library (from Scratch)", indent: 0 },
  { text: "You may use any Quadratic Programming solver (e.g. quadprog, CVXOPT, ..) to solve the Lagrangian Equation.", indent: 0 },
  { text: "Make use of Kernel functions (e.g. Quadratic , Polynomial, or RBF)", indent: 0 },
  { text: "For each of the given dataset (2-D):", indent: 0 },
  { text: "Draw the dataset points using color coding (assign same color to points belong to same class)", indent: 1 },
  { text: "Divide the background into grid, classify each point in the grid, give each point same color code of the class it belongs to.", indent: 1 },
];

const bulletObjs = bullets.map(b => ({
  text: b.text,
  options: {
    breakLine: true,
    bullet: { characterCode: "2022", indent: 15 },
    indentLevel: b.indent,
    fontSize: 16,
    color: "000080",
    fontFace: FONT,
    paraSpaceAfter: 8,
  },
}));

s.addText(bulletObjs, {
  x: boxX + 0.3, y: boxY + 0.3, w: boxW - 0.6, h: boxH - 0.6,
  align: "left", valign: "top",
  margin: 0,
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_039_recreated.pptx"
}).then(() => console.log("wrote slide_039_recreated.pptx"))
.catch(err => console.error(err));