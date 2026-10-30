const pptxgen = require("pptxgenjs");
const { newPres, addHouseChrome, addPlotShell, addDot, addCluster, W, H, FONT } = require("./shared.js");

const NUM = 43;
const TITLE = null;

const pres = newPres();
const s = pres.addSlide();
addHouseChrome(pres, s, NUM, TITLE);

// Main plot area with red border
// From analysis: x 0-40, y -10 to 40, decision regions filled with colored dots
const PX = 1.8, PY = 0.8, PW = 4.5, PH = 3.6;
const X_MIN = 0, X_MAX = 40;
const Y_MIN = -10, Y_MAX = 40;

const mapper = addPlotShell(pres, s, PX, PY, PW, PH, X_MIN, X_MAX, Y_MIN, Y_MAX, "", "");

// Decision regions (background colored dots) - these are dense grids of small dots
// Blue region: x≈0-20, y≈20-40
// Red region: x≈20-30, y≈20-30
// Cyan region: x≈30-40, y≈20-30
// Yellow region: x≈0-10, y≈10-20
// Green region: x≈0-10, y≈0-10
// Magenta region: x≈10-30, y≈0-10
// Black region: x≈30-40, y≈0-10

// Helper to fill a region with small dots
function fillRegion(pres, slide, mapper, x1, x2, y1, y2, color, density = 0.5) {
  const step = density;
  for (let x = x1; x <= x2; x += step) {
    for (let y = y1; y <= y2; y += step) {
      addDot(pres, slide, mapper, x, y, color, 0.02);
    }
  }
}

// Decision regions
fillRegion(pres, s, mapper, 0, 20, 20, 40, "0000FF", 1.0);   // blue
fillRegion(pres, s, mapper, 20, 30, 20, 30, "FF0000", 1.0);  // red
fillRegion(pres, s, mapper, 30, 40, 20, 30, "00FFFF", 1.0);  // cyan
fillRegion(pres, s, mapper, 0, 10, 10, 20, "FFFF00", 1.0);   // yellow
fillRegion(pres, s, mapper, 0, 10, 0, 10, "00FF00", 1.0);    // green
fillRegion(pres, s, mapper, 10, 30, 0, 10, "FF00FF", 1.0);   // magenta
fillRegion(pres, s, mapper, 30, 40, 0, 10, "000000", 1.0);   // black

// Seven clusters on top of decision regions
const CLUSTERS = [
  {cx: 15, cy: 25, color: "00008B", spread: 5, count: 30},   // dark blue
  {cx: 22, cy: 23, color: "FF0000", spread: 4, count: 25},   // red
  {cx: 33, cy: 22, color: "00FFFF", spread: 4, count: 25},   // cyan
  {cx: 8, cy: 12, color: "FFFF00", spread: 3, count: 15},    // yellow
  {cx: 7, cy: 3, color: "00FF00", spread: 2, count: 12},     // green
  {cx: 17, cy: 7, color: "FF00FF", spread: 6, count: 25},    // magenta
  {cx: 33, cy: 7, color: "000000", spread: 4, count: 20},    // black
];

CLUSTERS.forEach(c => {
  addCluster(pres, s, mapper, c.cx, c.cy, c.spread, c.count, c.color, 0.05);
});

pres.writeFile({ fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_043_recreated.pptx" })
  .then(() => console.log("wrote slide_043_recreated.pptx"))
  .catch(e => console.error(e));