const pptxgen = require("pptxgenjs");
const { newPres, addHouseChrome, addPlotShell, addDot, addCluster, W, H, FONT } = require("./shared.js");

const NUM = 42;
const TITLE = null;

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, TITLE);

// Main plot area with red border
// From analysis: scatter plot centered, x 0-40, y -10 to 40
// Measured position: plot spans ≈x215-655, y75-430 in 960x540
const PX = 1.8, PY = 0.8, PW = 4.5, PH = 3.6;
const X_MIN = 0, X_MAX = 40;
const Y_MIN = -10, Y_MAX = 40;

const mapper = addPlotShell(pres, s, PX, PY, PW, PH, X_MIN, X_MAX, Y_MIN, Y_MAX, "", "");

// Seven clusters
// blue upper-left (approx x 5-15, y 15-30)
// red upper-center (approx x 18-25, y 20-25)
// cyan upper-right (approx x 30-35, y 15-30)
// yellow mid-left (approx x 5-10, y 10-13)
// magenta center (approx x 10-25, y 5-12)
// green lower-left (approx x 5-8, y 2-5)
// black lower-right (approx x 30-35, y 5-10)
const CLUSTERS = [
  {cx: 10, cy: 22, color: "0000FF", spread: 8, count: 30},   // blue
  {cx: 22, cy: 23, color: "FF0000", spread: 6, count: 25},   // red
  {cx: 33, cy: 22, color: "00FFFF", spread: 5, count: 25},   // cyan
  {cx: 7, cy: 12, color: "FFFF00", spread: 4, count: 15},    // yellow
  {cx: 18, cy: 8, color: "FF00FF", spread: 12, count: 35},   // magenta
  {cx: 6, cy: 3, color: "00FF00", spread: 2, count: 12},     // green
  {cx: 33, cy: 7, color: "000000", spread: 4, count: 20},    // black
];

CLUSTERS.forEach(c => {
  addCluster(pres, s, mapper, c.cx, c.cy, c.spread, c.count, c.color, 0.04);
});

// Small black arrow annotation pointing toward red cluster from above
// Arrow made with lines
const arrX = mapper.toX(22);
const arrY = mapper.toY(30);
s.addShape(pres.shapes.LINE, { x: arrX, y: arrY, w: 0, h: 0.5, line: { color: "000000", width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: arrX - 0.1, y: arrY + 0.5, w: 0.1, h: 0, line: { color: "000000", width: 1.5 } });
s.addShape(pres.shapes.LINE, { x: arrX + 0.1, y: arrY + 0.5, w: -0.1, h: 0, line: { color: "000000", width: 1.5 } });

// Bottom black strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.15, w: W, h: 0.15,
  fill: { color: "000000" }, line: { color: "000000", width: 0 },
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_042_recreated.pptx" })
  .then(() => console.log("wrote slide_042_recreated.pptx"))
  .catch(e => console.error(e));